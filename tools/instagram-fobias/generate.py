import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data"
RENDER = ROOT / "render"
RENDER.mkdir(exist_ok=True)

fobias = json.loads((DATA / "fobias.json").read_text(encoding="utf-8"))
anim_css = (DATA / "anim.css").read_text(encoding="utf-8")
anim_css = re.sub(r"@media \(prefers-reduced-motion:.*?\}\s*\}", "", anim_css, flags=re.S)

TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
:root {{
  --navy: #14324B;
  --ink: #111111;
  --paper: #FFFFFF;
  --line: rgba(17,17,17,.15);
  --tint: #F2F5F8;
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{
  width:1080px; height:1920px;
  background: var(--paper);
  font-family: Arial, Helvetica, sans-serif;
  overflow:hidden;
}}
.stage {{
  width:1080px; height:1920px;
  display:flex; flex-direction:column;
  align-items:center; justify-content:space-between;
  padding: 108px 90px 96px;
  position:relative;
}}
.stage::before {{
  content:''; position:absolute; inset:40px;
  border: 2px solid var(--ink); pointer-events:none;
}}
.top {{ display:flex; flex-direction:column; align-items:center; gap:20px; z-index:1; }}
.kicker {{
  font-size:28px; letter-spacing:.28em; text-transform:uppercase;
  color:var(--navy); font-weight:700;
}}
.kicker-line {{ width:70px; height:3px; background:var(--navy); }}
.middle {{ display:flex; flex-direction:column; align-items:center; gap:64px; z-index:1; }}
.icon-wrap {{
  width:660px; height:660px; border-radius:50%;
  background:var(--tint); border:5px solid var(--ink);
  display:flex; align-items:center; justify-content:center;
}}
.icon-wrap svg {{ width:390px; height:390px; overflow:visible; }}
.text-block {{ display:flex; flex-direction:column; align-items:center; gap:26px; }}
.name {{
  font-size:104px; font-weight:800; color:var(--ink);
  text-align:center; letter-spacing:-.01em; line-height:1.02;
}}
.desc {{
  font-size:44px; line-height:1.55; color:#333;
  text-align:center; max-width:860px;
}}
.bottom {{ display:flex; flex-direction:column; align-items:center; gap:12px; z-index:1; }}
.brand-line {{ width:70px; height:2px; background:var(--line); }}
.brand {{ font-size:32px; font-weight:700; color:var(--navy); letter-spacing:.02em; }}
.brand-sub {{
  font-size:24px; color:#666; letter-spacing:.1em; text-transform:uppercase;
}}
{anim_css}
</style>
</head>
<body>
  <div class="stage">
    <div class="top">
      <span class="kicker">Psicoeducação · Fobias</span>
      <div class="kicker-line"></div>
    </div>
    <div class="middle">
      <div class="icon-wrap">{svg}</div>
      <div class="text-block">
        <h1 class="name">{name}</h1>
        <p class="desc">{desc}</p>
      </div>
    </div>
    <div class="bottom">
      <div class="brand-line"></div>
      <span class="brand">Priscila Palomo</span>
      <span class="brand-sub">Psicóloga · CRP 98007 · Especialista em fobias</span>
    </div>
  </div>
</body>
</html>
"""

def fix_acrofobia_layering(svg):
    # A ponta navy da montanha ficava por baixo da nuvem quando ela passava
    # por cima em telas grandes; redesenhar depois da nuvem resolve.
    notch = '<path d="M26 18 L32 28 L26 30 L22 25 Z" fill="#14324B"></path>'
    if notch not in svg:
        return svg
    svg = svg.replace(notch, "")
    return svg.replace("</g>\n</svg>", f"</g>\n{notch}\n</svg>")


FIXUPS = {"acrofobia": fix_acrofobia_layering}

index = []
for f in fobias:
    svg = FIXUPS.get(f["slug"], lambda s: s)(f["svg"])
    html = TEMPLATE.format(anim_css=anim_css, svg=svg, name=f["name"], desc=f["desc"])
    out_path = RENDER / f"{f['slug']}.html"
    out_path.write_text(html, encoding="utf-8")
    index.append({"slug": f["slug"], "name": f["name"]})
    print("wrote", out_path.name)

(RENDER / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
print(len(index), "arquivos gerados em", RENDER)
