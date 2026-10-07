#!/usr/bin/env python3
"""Pipeline do vídeo institucional (motion graphics).

Narração (edge-tts) → duração das cenas → injeção no render → captura de
frames (puppeteer) → trilha ambiente (numpy) → mixagem e MP4 (ffmpeg).

Uso:
    python3 build.py             # completo
    python3 build.py --silent    # sem narração (durações padrão do HTML)
    python3 build.py --no-capture  # reaproveita os frames já capturados

Saídas (em assets/videos/):
    institucional.mp4          1280×720, H.264 + AAC (hero e modal do site)
    institucional-poster.jpg   quadro de abertura para o atributo poster
"""
import asyncio, json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).parent
RENDER_HTML = ROOT / "render" / "institucional.html"
AUDIO_DIR = ROOT / "audio"
FRAMES_DIR = ROOT / "frames"
OUT_DIR = ROOT / "out"
ASSETS = ROOT.parent.parent / "assets" / "videos"

VOICE = "pt-BR-FranciscaNeural"
RATE = "-6%"
PAD_S = 0.9
FPS = 30
SILENT = "--silent" in sys.argv
NO_CAPTURE = "--no-capture" in sys.argv


def ffprobe_dur(p: Path) -> float:
    out = subprocess.check_output(["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)])
    return float(out.decode().strip())


async def gen_narracao(scenes):
    import edge_tts
    (AUDIO_DIR / "cenas").mkdir(parents=True, exist_ok=True)
    durs = []
    for sc in scenes:
        mp3 = AUDIO_DIR / "cenas" / f"{sc['id']}.mp3"
        await edge_tts.Communicate(sc["text"], VOICE, rate=RATE).save(str(mp3))
        durs.append(ffprobe_dur(mp3))
        print(f"  narração {sc['id']}: {durs[-1]:.2f}s")
    return durs


def read_default_durs():
    m = re.search(r"let SCENE_DURMS = \[(.*?)\];", RENDER_HTML.read_text())
    return [int(x) for x in m.group(1).split(",")]


def inject_durations(durs_ms):
    html = RENDER_HTML.read_text()
    arr = "[" + ", ".join(str(int(x)) for x in durs_ms) + "]"
    html = re.sub(r"/\*DUR_START\*/.*?/\*DUR_END\*/", f"/*DUR_START*/\nlet SCENE_DURMS = {arr};\n/*DUR_END*/", html, flags=re.S)
    RENDER_HTML.write_text(html)
    print("  durações:", arr)


def build_narration_track(scenes, durs_ms):
    parts = []
    for i, sc in enumerate(scenes):
        mp3 = AUDIO_DIR / "cenas" / f"{sc['id']}.mp3"
        padded = AUDIO_DIR / "cenas" / f"{sc['id']}_pad.wav"
        dur_s = durs_ms[i] / 1000.0
        # a fala começa 0,35 s depois do início da cena, para acompanhar a animação
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp3),
                               "-af", f"adelay=350|350,apad=whole_dur={dur_s},atrim=0:{dur_s},aresample=44100", str(padded)])
        parts.append(padded)
    lst = AUDIO_DIR / "concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    full = AUDIO_DIR / "narracao.wav"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-ac", "2", str(full)])
    return full


def build_mix(total_s, narr: Path | None):
    raw = AUDIO_DIR / "ambiente_raw.wav"
    subprocess.check_call(["python3", str(ROOT / "compose_ambient.py"), f"{total_s}", str(raw)])
    music = AUDIO_DIR / "ambiente.wav"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw),
                           "-af", f"aecho=0.6:0.5:120:0.18,afade=t=in:d=2,afade=t=out:st={max(0, total_s-3)}:d=3", str(music)])
    mix = AUDIO_DIR / "mix.wav"
    if narr is None:
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", str(music), "-af", "volume=0.6", str(mix)])
        return mix
    subprocess.check_call([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(narr), "-i", str(music),
        "-filter_complex",
        "[1:a]volume=0.30[m];"
        "[m][0:a]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=500:makeup=1[mk];"
        "[0:a]volume=1.1[v];"
        "[v][mk]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[out]",
        "-map", "[out]", str(mix)])
    return mix


def capture():
    env = os.environ.copy(); env.setdefault("CHROME_PATH", "/usr/bin/google-chrome-stable")
    subprocess.check_call(["node", str(ROOT / "capture.js")], env=env)


def encode(mix: Path, total_s: float, poster_t: float):
    OUT_DIR.mkdir(exist_ok=True); ASSETS.mkdir(parents=True, exist_ok=True)
    out = ASSETS / "institucional.mp4"
    subprocess.check_call([
        "ffmpeg", "-y", "-loglevel", "error",
        "-framerate", str(FPS), "-i", str(FRAMES_DIR / "frame_%05d.png"), "-i", str(mix),
        "-vf", "scale=1280:720:flags=lanczos,format=yuv420p",
        "-c:v", "libx264", "-preset", "slow", "-crf", "25", "-profile:v", "high", "-level", "4.0",
        "-movflags", "+faststart", "-c:a", "aac", "-b:a", "96k", "-shortest", str(out)])
    poster = ASSETS / "institucional-poster.jpg"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{poster_t:.2f}", "-i", str(out), "-frames:v", "1", "-q:v", "3", str(poster)])
    print("saída:", out, f"({out.stat().st_size/1e6:.2f} MB)", "·", poster)


def main():
    scenes = json.loads((ROOT / "script.json").read_text())
    if SILENT:
        durs_ms = read_default_durs(); narr = None
    else:
        print("1) narração")
        durs = asyncio.run(gen_narracao(scenes))
        durs_ms = [int((d + PAD_S + 0.35) * 1000) for d in durs]
        # mínimos para as animações completarem
        minimos = [4500, 5200, 8500, 7500, 5000, 5500, 4500]
        durs_ms = [max(a, b) for a, b in zip(durs_ms, minimos)]
        inject_durations(durs_ms)
        print("2) trilha de narração")
        narr = build_narration_track(scenes, durs_ms)
    total_s = sum(durs_ms) / 1000.0
    if not NO_CAPTURE:
        print("3) captura de frames")
        capture()
    print("4) trilha e mixagem")
    mix = build_mix(total_s, narr)
    print("5) codificação")
    encode(mix, total_s, poster_t=(durs_ms[0] + durs_ms[1] * 0.75) / 1000.0)


if __name__ == "__main__":
    main()
