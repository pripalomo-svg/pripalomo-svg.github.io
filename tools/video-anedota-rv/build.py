#!/usr/bin/env python3
"""Pipeline do vídeo 'draw myself' da história da Priscila.

Gera a narração (edge-tts), calcula as durações de cada cena, injeta os tempos
no render HTML, captura os frames (puppeteer) e monta o MP4 com ffmpeg.

Uso:
    python3 build.py            # completo (narração + vídeo)
    python3 build.py --silent   # sem narração (usa durações padrão do HTML)
"""
import asyncio, json, subprocess, sys, re, shutil
from pathlib import Path

ROOT = Path(__file__).parent
RENDER_HTML = ROOT / "render" / "anedota.html"
AUDIO_DIR = ROOT / "audio"
FRAMES_DIR = ROOT / "frames"
OUT_DIR = ROOT / "out"
ASSET_OUT = ROOT.parent.parent / "assets" / "videos" / "anedota-rv.mp4"

VOICE = "pt-BR-FranciscaNeural"
PAD_S = 0.8          # respiro após cada narração
FPS = 24
SILENT = "--silent" in sys.argv


def ffprobe_dur(p: Path) -> float:
    out = subprocess.check_output([
        "ffprobe","-v","quiet","-show_entries","format=duration","-of","csv=p=0", str(p)
    ]).decode().strip()
    return float(out)


async def gen_narracao(scenes):
    import edge_tts
    AUDIO_DIR.mkdir(exist_ok=True)
    (AUDIO_DIR / "cenas").mkdir(exist_ok=True)
    durs = []
    for sc in scenes:
        mp3 = AUDIO_DIR / "cenas" / f"{sc['id']}.mp3"
        await edge_tts.Communicate(sc["text"], VOICE, rate="-4%").save(str(mp3))
        durs.append(ffprobe_dur(mp3))
        print(f"  narração {sc['id']}: {durs[-1]:.2f}s")
    return durs


def build_full_audio(scenes, scene_durs_ms):
    """Concatena as narrações, cada uma preenchida com silêncio até a duração da cena."""
    parts = []
    for i, sc in enumerate(scenes):
        mp3 = AUDIO_DIR / "cenas" / f"{sc['id']}.mp3"
        padded = AUDIO_DIR / "cenas" / f"{sc['id']}_pad.wav"
        dur_s = scene_durs_ms[i] / 1000.0
        subprocess.check_call([
            "ffmpeg","-y","-loglevel","error","-i",str(mp3),
            "-af", f"apad=whole_dur={dur_s},atrim=0:{dur_s},aresample=44100",
            str(padded)
        ])
        parts.append(padded)
    listfile = AUDIO_DIR / "concat.txt"
    listfile.write_text("".join(f"file '{p}'\n" for p in parts))
    full = AUDIO_DIR / "narracao_completa.wav"
    subprocess.check_call([
        "ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(listfile),
        "-af","afade=t=out:st=%s:d=0.6" % (sum(scene_durs_ms)/1000.0 - 0.6),
        str(full)
    ])
    return full


def build_music(total_ms):
    """Gera uma trilha pop-rock alegre (compose_rock.py) e a mistura sob a
    narração com ducking, mantendo a voz sempre à frente. Gera audio/mix_final.wav."""
    total_s = total_ms / 1000.0
    AUDIO_DIR.mkdir(exist_ok=True)
    raw = AUDIO_DIR / "musica_raw.wav"
    subprocess.check_call(["python3", str(ROOT / "compose_rock.py"), f"{total_s}", str(raw)])
    music = AUDIO_DIR / "musica.wav"
    # brilho + leve reverb + fades
    subprocess.check_call([
        "ffmpeg","-y","-loglevel","error","-i",str(raw),
        "-af", f"highpass=f=60,lowpass=f=9000,aecho=0.7:0.6:55:0.15,"
               f"afade=t=in:d=1.5,afade=t=out:st={max(0,total_s-2.5)}:d=2.5",
        str(music)
    ])
    narr = AUDIO_DIR / "narracao_completa.wav"
    mix = AUDIO_DIR / "mix_final.wav"
    # música viva, mas abaixo da voz: ducking forte quando há narração
    subprocess.check_call([
        "ffmpeg","-y","-loglevel","error","-i",str(narr),"-i",str(music),
        "-filter_complex",
        "[1:a]volume=0.42[m];"
        "[m][0:a]sidechaincompress=threshold=0.025:ratio=14:attack=5:release=320:makeup=1[mk];"
        "[0:a]volume=1.15[v];"
        "[v][mk]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[out]",
        "-map","[out]", str(mix)
    ])
    return mix


def inject_durations(scene_durs_ms):
    html = RENDER_HTML.read_text()
    arr = "[" + ",".join(str(int(x)) for x in scene_durs_ms) + "]"
    html = re.sub(r"/\*DUR_START\*/.*?/\*DUR_END\*/",
                  f"/*DUR_START*/\nlet SCENE_DURMS = {arr};\n/*DUR_END*/",
                  html, flags=re.S)
    RENDER_HTML.write_text(html)
    print("  durações injetadas:", arr)


def capture():
    env = {"CHROME_PATH": "/usr/bin/google-chrome-stable"}
    import os
    e = os.environ.copy(); e.update(env)
    subprocess.check_call(["node", str(ROOT / "capture.js")], env=e)


def encode(with_audio):
    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / "anedota-rv.mp4"
    audio_file = AUDIO_DIR / "mix_final.wav"
    if not audio_file.exists():
        audio_file = AUDIO_DIR / "narracao_completa.wav"
    cmd = ["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),
           "-i", str(FRAMES_DIR / "frame_%05d.png")]
    if with_audio:
        cmd += ["-i", str(audio_file)]
    cmd += ["-c:v","libx264","-preset","slow","-crf","21","-pix_fmt","yuv420p"]
    if with_audio:
        cmd += ["-c:a","aac","-b:a","160k","-shortest"]
    cmd += ["-movflags","+faststart", str(out)]
    subprocess.check_call(cmd)
    ASSET_OUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(out, ASSET_OUT)
    print("  vídeo:", out, "->", ASSET_OUT)


def main():
    scenes = json.loads((ROOT / "script.json").read_text())
    with_audio = False
    if not SILENT:
        try:
            durs = asyncio.run(gen_narracao(scenes))
            scene_durs_ms = [int(round((d + PAD_S) * 1000)) for d in durs]
            inject_durations(scene_durs_ms)
            build_full_audio(scenes, scene_durs_ms)
            with_audio = True
            try:
                build_music(sum(scene_durs_ms))
                print("  trilha musical suave adicionada e mixada.")
            except Exception as mex:
                print("!! música indisponível (%s); seguindo só com narração." % mex)
        except Exception as ex:
            print("!! narração indisponível (%s); seguindo sem áudio." % ex)
    if not with_audio:
        # usa as durações padrão já embutidas no HTML
        m = re.search(r"let SCENE_DURMS = (\[[^\]]+\])", RENDER_HTML.read_text())
        print("  usando durações padrão:", m.group(1) if m else "?")
    capture()
    encode(with_audio)
    print("OK")


if __name__ == "__main__":
    main()
