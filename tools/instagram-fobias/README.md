# Vídeos de Instagram — animações de fobias

Gera **um vídeo vertical por animação** (1080×1920, Reels/Stories),
reaproveitando os desenhos SVG da página de fobias.

Inclui:

- **16 fobias do catálogo** (aranha, cobra, altura, avião…)
- **4 cenas educativas** (medo encolhe, alarme no corpo, ciclo da evitação, escada)

## Gerar tudo de uma vez

```bash
cd tools/instagram-fobias
./gerar-tudo.sh
```

Os vídeos finais ficam em `out/<slug>.mp4` e são copiados para
`videos/instagram-fobias/` (catálogo público no site).

**Catálogo online:** https://www.priscilapalomo.com/catalogo-videos.html  
**Narrativas:** [`LEGENDAS.md`](LEGENDAS.md)

Para gerar só algumas:

```bash
./gerar-tudo.sh aracnofobia cinofobia cena-medo-encolhe
```

## Passo a passo manual

```bash
cd tools/instagram-fobias
npm install
python3 extract.py          # atualiza data/fobias.json a partir do index.html
python3 generate.py         # render/<slug>.html (catálogo + cenas)
CHROME_PATH=/usr/bin/google-chrome-stable node capture.js
mkdir -p out
for d in frames/*/; do
  slug=$(basename "$d")
  ffmpeg -y -framerate 24 -i "frames/${slug}/frame_%04d.png" \
    -c:v libx264 -pix_fmt yuv420p -movflags +faststart "out/${slug}.mp4"
done
```

## Lista dos vídeos

### Catálogo

| Arquivo | Tema |
| --- | --- |
| `aracnofobia.mp4` | Medo de aranhas |
| `ofidiofobia.mp4` | Medo de cobras |
| `cinofobia.mp4` | Medo de cães |
| `acrofobia.mp4` | Medo de altura |
| `claustrofobia.mp4` | Medo de lugares fechados |
| `aerofobia.mp4` | Medo de voar |
| `hematofobia.mp4` | Medo de sangue |
| `tripanofobia.mp4` | Medo de agulhas |
| `astrafobia.mp4` | Medo de trovão/raio |
| `nictofobia.mp4` | Medo do escuro |
| `odontofobia.mp4` | Medo de dentista |
| `talassofobia.mp4` | Medo de mar profundo |
| `glossofobia.mp4` | Medo de falar em público |
| `fobia-social.mp4` | Fobia social |
| `agorafobia.mp4` | Agorafobia |
| `emetofobia.mp4` | Medo de vomitar |

### Cenas educativas

| Arquivo | Tema |
| --- | --- |
| `cena-medo-encolhe.mp4` | Aproximar-se encolhe o medo |
| `cena-alarme-corpo.mp4` | Alarme falso no corpo |
| `cena-ciclo-evitacao.mp4` | Ciclo da evitação |
| `cena-escada-exposicao.mp4` | Escada da exposição gradual |

## Observação

`render/`, `frames/` e `out/` não são versionados (artefatos gerados).
