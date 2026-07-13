import re, json
from bs4 import BeautifulSoup

with open('/workspace/index.html', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'lxml')
grid = soup.select_one('.fb-grid')
cards = grid.select('.fb-card')

out = []
for card in cards:
    svg = card.select_one('svg')
    h3 = card.select_one('h3')
    p = card.select_one('p')
    name = h3.get_text(strip=True)
    desc = p.get_text(strip=True)
    svg_html = str(svg)
    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    out.append({'slug': slug, 'name': name, 'desc': desc, 'svg': svg_html})

with open('/workspace/tools/instagram-fobias/data/fobias.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(len(out), 'fobias extraídas')
for o in out:
    print('-', o['slug'], '|', o['name'])
