# Vídeo "Draw myself" — minha história (doutorado)

Vídeo estilo **draw my life** (lousa branca, desenho à mão que se desenha
sozinho + marcador que segue o traço + legendas manuscritas), narrado em
português, contando a trajetória acadêmica da Priscila com base no documento
de doutorado da **Universitat de València** (embodiment, integração
multissensorial e transtornos da conduta alimentar; defesa em 2016 com
Sobresaliente Cum Laude e Menção Internacional).

Saída: `assets/videos/draw-minha-historia.mp4` (1920×1080, ~71s, narração pt-BR).

## Arquivos

- `script.json` — texto da narração de cada cena.
- `render/draw-historia.html` — a animação (SVG que se desenha), **determinística**
  via `window.__render(t)` / `window.__totalDuration` (permite captura frame a frame).
  As cenas e os desenhos ficam no array `SCENES`; as durações em `SCENE_DURMS`.
- `capture.js` — captura os frames com puppeteer-core + Chrome.
- `build.py` — pipeline completo (narração → durações → injeção → captura → MP4).

## Gerar do zero

```bash
cd tools/video-draw-historia
npm install
pip install edge-tts        # narração (voz neural pt-BR-FranciscaNeural)

python3 build.py            # narração + vídeo com áudio
# ou
python3 build.py --silent   # sem narração (usa as durações padrão do HTML)
```

O MP4 final é copiado automaticamente para `assets/videos/draw-minha-historia.mp4`.

## Editar o roteiro / os desenhos

- Texto da narração: `script.json`.
- Desenhos e legendas: array `SCENES` em `render/draw-historia.html`
  (cada cena tem `cap` = legenda manuscrita e `paths` = traços SVG desenhados na ordem).
- Rode `python3 build.py` de novo.

## Determinismo

Nada de `setTimeout`/`@keyframes` para a animação: tudo é função do tempo
virtual `window.__render(t)` (em ms). Assim a captura de frames dá exatamente
o mesmo resultado, independente da velocidade do processo de screenshot.
