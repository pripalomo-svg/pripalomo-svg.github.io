# Vídeo "Minha história"

Gera o vídeo horizontal (1920×1080) usado em `apresentacao.html`, contando a
trajetória da Priscila em cenas de texto com fade determinístico (não depende
de tempo real — cada frame é renderizado a partir de um instante virtual
calculado em JS, então a captura funciona de forma exata não importa quanto
tempo o processo de screenshot realmente leve).

## Como gerar

```bash
cd tools/video-historia
npm install
cp ../../assets/ilustracao-priscila.jpg render/ilustracao-priscila.jpg

CHROME_PATH=/usr/bin/google-chrome-stable node capture.js

mkdir -p out
ffmpeg -y -framerate 24 -i frames/minha-historia/frame_%05d.png \
  -c:v libx264 -pix_fmt yuv420p -movflags +faststart out/minha-historia.mp4

cp out/minha-historia.mp4 ../../assets/videos/minha-historia.mp4
```

## Editar o roteiro

As cenas (texto, ordem e duração) ficam no `<script>` no fim de
`render/minha-historia.html`, no objeto `HOLD` e na lista `order`. Edite o
texto de cada `<div class="scene" id="...">` e gere de novo.
