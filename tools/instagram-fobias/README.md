# Vídeos de Instagram — catálogo de fobias

Gera um vídeo vertical (1080×1920, formato Reels/Stories) para cada fobia do
catálogo animado em `index.html`, reaproveitando o mesmo desenho SVG e
animação CSS de cada card — em tamanho grande, com nome, descrição e a
marca da Priscila.

## Como gerar (do zero)

```bash
cd tools/instagram-fobias
npm install

# 1. Extrai ícone, nome e descrição de cada fobia direto do index.html
python3 extract.py

# 2. Gera um .html independente por fobia (render/<slug>.html)
python3 generate.py

# 3. Abre cada .html num Chrome headless e captura frames (4.5s, 24fps)
CHROME_PATH=/usr/bin/google-chrome-stable node capture.js

# 4. Junta os frames em .mp4 com ffmpeg
mkdir -p out
for d in frames/*/; do
  slug=$(basename "$d")
  ffmpeg -y -framerate 24 -i "frames/${slug}/frame_%04d.png" \
    -c:v libx264 -pix_fmt yuv420p -movflags +faststart "out/${slug}.mp4"
done
```

Os vídeos finais ficam em `out/<slug>.mp4`, prontos para publicar.

## Atualizando o catálogo

Se o catálogo de fobias em `index.html` mudar (novo texto, nova fobia, novo
ícone), basta rodar os 4 passos de novo — tudo é extraído automaticamente,
não precisa editar nada manualmente aqui.

## Observação

`render/`, `frames/` e `out/` não são versionados (são artefatos gerados).
