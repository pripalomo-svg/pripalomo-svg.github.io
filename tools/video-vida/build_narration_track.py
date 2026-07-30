import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
timeline = json.loads((ROOT / "timeline.json").read_text())

inputs = []
filters = []
labels = []
for i, sc in enumerate(timeline["scenes"]):
    mp3 = ROOT / "audio" / "narracao" / f"{sc['narr']}.mp3"
    inputs += ["-i", str(mp3)]
    delay = sc["narrationStart"]
    filters.append(f"[{i}:a]adelay={delay}|{delay}[a{i}]")
    labels.append(f"[a{i}]")

total_s = timeline["totalDurationMs"] / 1000
mix = "".join(labels) + f"amix=inputs={len(labels)}:duration=longest:normalize=0[mixed]"
filter_complex = ";".join(filters) + ";" + mix + f";[mixed]apad=whole_dur={total_s}[aout]"

out_path = ROOT / "audio" / "narracao_completa.wav"
cmd = [
    "ffmpeg", "-y", "-loglevel", "error",
    *inputs,
    "-filter_complex", filter_complex,
    "-map", "[aout]",
    str(out_path),
]
print(" ".join(cmd))
subprocess.run(cmd, check=True)
print("wrote", out_path)
