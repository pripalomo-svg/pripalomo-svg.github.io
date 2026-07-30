import json
from pathlib import Path

ROOT = Path(__file__).parent

FADE = 700       # crossfade entre cenas (ms)
LEAD_IN = 300    # pausa depois que a imagem aparece, antes da narração começar
TAIL = 600       # pausa depois que a narração termina, antes do crossfade
CLOSING_HOLD = 2600  # segura a última cena mais tempo no final

durations = json.loads((ROOT / "audio" / "durations.json").read_text())

scenes = [
    {"id": "chegada",    "img": "vida-01-chegada-valencia.jpg", "narr": "s1",
     "caption": "Valencia, Espanha"},
    {"id": "lab",        "img": "vida-02-laboratorio-rv.jpg",   "narr": "s2",
     "caption": "Laboratório de Realidade Virtual"},
    {"id": "equipe",     "img": "vida-03-equipe-lab.jpg",       "narr": "s3",
     "caption": "Equipe de pesquisa"},
    {"id": "congresso",  "img": "vida-04-congresso.jpg",        "narr": "s4",
     "caption": "Congressos científicos"},
    {"id": "biblioteca", "img": "vida-05-biblioteca.jpg",       "narr": "s5",
     "caption": "Horas de estudo"},
    {"id": "formatura",  "img": "vida-06-formatura.jpg",        "narr": "s6",
     "caption": "Cum laude — Universitat de València"},
    {"id": "volta",      "img": "vida-07-volta-brasil.jpg",     "narr": "s7",
     "caption": "De volta ao Brasil"},
    {"id": "fechamento", "img": None, "narr": "s8",
     "caption": "Hoje"},
]

timeline = []
cursor = 0
for i, sc in enumerate(scenes):
    is_last = i == len(scenes) - 1
    dur = int(durations[sc["narr"]] * 1000)
    image_start = cursor
    fade_in_end = image_start + FADE
    narration_start = fade_in_end + LEAD_IN
    narration_end = narration_start + dur
    hold_end = narration_end + TAIL
    fade_out_end = hold_end if is_last else hold_end + FADE
    timeline.append({
        **sc,
        "narrationDurMs": dur,
        "imageStart": image_start,
        "fadeInEnd": fade_in_end,
        "narrationStart": narration_start,
        "narrationEnd": narration_end,
        "holdEnd": hold_end,
        "fadeOutEnd": fade_out_end,
        "isLast": is_last,
    })
    cursor = hold_end

total_duration = cursor + CLOSING_HOLD

out = {
    "fade": FADE,
    "totalDurationMs": total_duration,
    "scenes": timeline,
}
(ROOT / "timeline.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Total duration: {total_duration}ms ({total_duration/1000:.1f}s)")
for s in timeline:
    print(f"  {s['id']:12s} narrationStart={s['narrationStart']:6d} dur={s['narrationDurMs']:6d} holdEnd={s['holdEnd']:6d}")
