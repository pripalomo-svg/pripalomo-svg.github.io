# Vídeo institucional (motion graphics)

Vídeo de ~68 s exibido no hero de `index.html` (loop mudo) e no modal
"Assistir com som". Sete cenas: abertura, posicionamento (com gráfico de
estresse caindo), cenário brasileiro (546 mil afastamentos, burnout 3×, NR-1),
método (medir → intervir → medir de novo), clínica de fobias (círculo que
respira + headset de RV), credenciais e encerramento.

## Arquivos

- `script.json` — narração de cada cena (pt-BR, voz `pt-BR-FranciscaNeural`).
- `render/institucional.html` — animação determinística em canvas
  (`window.__render(t)`); abra no navegador para pré-visualizar em loop.
- `compose_ambient.py` — trilha ambiente (pad + arpejo) gerada com numpy.
- `capture.js` — captura de frames 1920×1080 a 30 fps (puppeteer-core + Chrome).
- `build.py` — pipeline completo.

## Gerar

```bash
cd tools/video-institucional
npm install
pip install edge-tts numpy
python3 build.py              # completo
python3 build.py --no-capture # só reencoda (reaproveita frames/)
python3 build.py --silent     # sem narração
```

Saídas: `assets/videos/institucional.mp4` (1280×720, H.264 + AAC, ~2 MB) e
`assets/videos/institucional-poster.jpg`.
