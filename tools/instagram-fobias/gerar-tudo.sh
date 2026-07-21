#!/usr/bin/env bash
# Gera um vídeo vertical (1080×1920) por animação — catálogo + cenas educativas.
set -euo pipefail
cd "$(dirname "$0")"

CHROME_PATH="${CHROME_PATH:-/usr/bin/google-chrome-stable}"

if [[ ! -d node_modules ]]; then
  npm install
fi

echo "==> 1/4 extraindo catálogo do index.html (se bs4 disponível)"
if python3 -c 'import bs4' 2>/dev/null; then
  python3 extract.py
else
  echo "    (bs4 ausente — reusando data/fobias.json)"
fi

echo "==> 2/4 gerando HTMLs em render/"
python3 generate.py

echo "==> 3/4 capturando frames (Chrome headless)"
CHROME_PATH="$CHROME_PATH" node capture.js "$@"

echo "==> 4/4 codificando MP4s em out/"
mkdir -p out
slugs=("$@")
if [[ ${#slugs[@]} -eq 0 ]]; then
  mapfile -t slugs < <(python3 -c 'import json; print("\n".join(i["slug"] for i in json.load(open("render/index.json"))))')
fi
for slug in "${slugs[@]}"; do
  echo "    $slug.mp4"
  ffmpeg -y -framerate 24 -i "frames/${slug}/frame_%04d.png" \
    -c:v libx264 -pix_fmt yuv420p -movflags +faststart "out/${slug}.mp4" </dev/null 2>/dev/null
done

echo "==> sincronizando para videos/instagram-fobias/ (site público)"
PUBLIC_DIR="$(cd ../.. && pwd)/videos/instagram-fobias"
mkdir -p "$PUBLIC_DIR"
cp -f out/*.mp4 "$PUBLIC_DIR/"
echo
echo "Pronto."
echo "  Locais:  out/<slug>.mp4"
echo "  Site:    videos/instagram-fobias/<slug>.mp4"
echo "  Catálogo: /catalogo-videos.html"
ls -1 out/*.mp4 | wc -l | xargs -I{} echo "  {} vídeos"
