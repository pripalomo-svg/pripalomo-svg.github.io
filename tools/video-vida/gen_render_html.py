import json
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
RENDER = ROOT / "render"
RENDER.mkdir(exist_ok=True)
(RENDER / "images").mkdir(exist_ok=True)

timeline = json.loads((ROOT / "timeline.json").read_text())

for sc in timeline["scenes"]:
    if sc["img"]:
        shutil.copy(ROOT / "images" / sc["img"], RENDER / "images" / sc["img"])
shutil.copy(ROOT.parent.parent / "assets" / "avatar-priscila.jpg", RENDER / "images" / "avatar-priscila.jpg")

FADE = timeline["fade"]

# Ken Burns: (escala inicial, tx inicial %, ty inicial %, escala final, tx final %, ty final %)
KB_DIRECTIONS = [
    (1.06, -1, -1, 1.16, 1.5, 1),
    (1.16, 1, 1, 1.05, -1.5, -1),
    (1.05, 0, -1.5, 1.15, 0, 1),
    (1.15, -1.5, 1, 1.05, 1, -1),
]

scenes_html = []
scenes_js = []
for i, sc in enumerate(timeline["scenes"]):
    if sc["img"]:
        body = f'''
      <div class="scene-media">
        <img src="images/{sc['img']}" class="kb-img" id="img-{sc['id']}">
        <div class="scrim"></div>
      </div>
      <div class="caption-box">
        <span class="caption-tag">{sc['caption']}</span>
      </div>'''
    else:
        body = f'''
      <div class="closing">
        <img src="images/avatar-priscila.jpg" class="closing-photo" alt="Priscila Palomo">
        <div class="closing-name">Priscila Palomo</div>
        <div class="closing-sub">Especialista em fobias · Doutora pela Universitat de València</div>
        <div class="closing-site">priscilapalomo.com</div>
      </div>'''
    scenes_html.append(f'''
    <div class="scene" id="s-{sc['id']}">{body}
    </div>''')

    kb = KB_DIRECTIONS[i % len(KB_DIRECTIONS)]
    visible_end = sc["holdEnd"] if sc["isLast"] else sc["fadeOutEnd"]
    scenes_js.append(
        "{"
        f"id:'s-{sc['id']}', imgId:'img-{sc['id']}', hasImg:{'true' if sc['img'] else 'false'}, "
        f"start:{sc['imageStart']}, fadeInEnd:{sc['fadeInEnd']}, "
        f"holdEnd:{sc['holdEnd']}, fadeOutEnd:{sc['fadeOutEnd']}, visibleEnd:{visible_end}, "
        f"isLast:{'true' if sc['isLast'] else 'false'}, "
        f"kb:{{s0:{kb[0]},tx0:{kb[1]},ty0:{kb[2]},s1:{kb[3]},tx1:{kb[4]},ty1:{kb[5]}}}"
        "}"
    )

html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1920px; height:1080px; background:#0c1116; overflow:hidden; font-family: Arial, Helvetica, sans-serif; }}
.stage {{ width:1920px; height:1080px; position:relative; }}

.scene {{ position:absolute; inset:0; opacity:0; }}
.scene-media {{ position:absolute; inset:0; overflow:hidden; }}
.kb-img {{ position:absolute; inset:-4%; width:108%; height:108%; object-fit:cover; will-change:transform; }}
.scrim {{
  position:absolute; inset:0;
  background: linear-gradient(180deg, rgba(0,0,0,.35) 0%, rgba(0,0,0,0) 22%, rgba(0,0,0,0) 68%, rgba(0,0,0,.55) 100%);
}}

.caption-box {{
  position:absolute; left:70px; bottom:56px;
  display:flex; align-items:center; gap:14px;
}}
.caption-tag {{
  font-size:26px; letter-spacing:.1em; color:#fff; font-weight:700;
  text-shadow: 0 2px 12px rgba(0,0,0,.6);
  border-left: 4px solid #E8B84B; padding-left:16px;
}}

.closing {{
  position:absolute; inset:0; background:#F2F5F8;
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:22px;
}}
.closing-photo {{
  width:220px; height:220px; border-radius:50%; object-fit:cover;
  border:6px solid #14324B;
}}
.closing-name {{ font-size:52px; font-weight:800; color:#14324B; }}
.closing-sub {{ font-size:24px; color:#444; }}
.closing-site {{ font-size:26px; font-weight:700; color:#2E8B57; letter-spacing:.04em; margin-top:6px; }}
</style>
</head>
<body>
<div class="stage">
  {''.join(scenes_html)}
</div>
<script>
const FADE = {FADE};
const timeline = [{','.join(scenes_js)}];

window.__totalDuration = {timeline['totalDurationMs']};

function lerp(a, b, t) {{ return a + (b - a) * t; }}

window.__render = function (t) {{
  timeline.forEach(({{id, imgId, hasImg, start, fadeInEnd, holdEnd, fadeOutEnd, visibleEnd, isLast, kb}}) => {{
    const el = document.getElementById(id);
    let op = 0;
    if (t < start) op = 0;
    else if (t < fadeInEnd) op = (t - start) / FADE;
    else if (t < holdEnd) op = 1;
    else if (isLast) op = 1;
    else if (t < fadeOutEnd) op = 1 - (t - holdEnd) / FADE;
    else op = 0;
    el.style.opacity = Math.max(0, Math.min(1, op));

    if (hasImg) {{
      const img = document.getElementById(imgId);
      const span = Math.max(1, visibleEnd - start);
      const progress = Math.max(0, Math.min(1, (t - start) / span));
      const s = lerp(kb.s0, kb.s1, progress);
      const tx = lerp(kb.tx0, kb.tx1, progress);
      const ty = lerp(kb.ty0, kb.ty1, progress);
      img.style.transform = `scale(${{s}}) translate(${{tx}}%, ${{ty}}%)`;
    }}
  }});
}};

window.__render(0);
</script>
</body>
</html>
"""

(RENDER / "vida.html").write_text(html, encoding="utf-8")
print("wrote", RENDER / "vida.html")
