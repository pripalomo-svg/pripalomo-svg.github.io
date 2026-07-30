import asyncio
import json
import subprocess
from pathlib import Path

import edge_tts

ROOT = Path(__file__).parent
VOICE = "pt-BR-FranciscaNeural"

async def synth(text, out_path):
    communicate = edge_tts.Communicate(text, VOICE, rate="-4%")
    await communicate.save(str(out_path))

async def main():
    script = json.loads((ROOT / "script.json").read_text(encoding="utf-8"))
    out_dir = ROOT / "audio" / "narracao"
    out_dir.mkdir(parents=True, exist_ok=True)

    durations = {}
    for item in script:
        out_path = out_dir / f"{item['id']}.mp3"
        await synth(item["text"], out_path)
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(out_path)],
            capture_output=True, text=True,
        )
        dur = float(result.stdout.strip())
        durations[item["id"]] = dur
        print(f"{item['id']}: {dur:.2f}s -> {out_path.name}")

    (ROOT / "audio" / "durations.json").write_text(
        json.dumps(durations, indent=2), encoding="utf-8"
    )
    print("total:", sum(durations.values()))

asyncio.run(main())
