# Vídeo "Minha vida" — draw my life, narrado

Vídeo ilustrado (1920×1080, ~92s) contando a jornada da Priscila como
estudante na Universidade de Valencia: chegada, laboratório de realidade
virtual, equipe de pesquisa, congressos, biblioteca, formatura cum laude e
volta ao Brasil — com narração em português (voz neural) e trilha
instrumental original de fundo.

## Pipeline

```
script.json            → texto de cada cena (roteiro da narração)
  ↓ gen_narracao.py     → audio/narracao/*.mp3 + audio/durations.json
  ↓ build_timeline.py   → timeline.json (quando cada cena começa/termina)
  ↓ build_narration_track.py → audio/narracao_completa.wav
  ↓ compose_music.py    → musica.mid (composição original) 
  ↓ fluidsynth           → musica_raw.wav → musica_final.wav (reverb + fade)
  ↓ mix (ffmpeg amix + sidechaincompress) → audio/mix_final.wav
  ↓ gen_render_html.py  → render/vida.html (Ken Burns determinístico)
  ↓ capture.js (puppeteer) → frames/vida/*.png
  ↓ ffmpeg (frames + mix_final.wav) → out/minha-vida.mp4
```

## Como gerar do zero

```bash
cd tools/video-vida
npm install
pip install edge-tts midiutil pillow

python3 gen_narracao.py            # narração (edge-tts, voz pt-BR-FranciscaNeural)
python3 build_timeline.py          # calcula os tempos de cada cena
python3 build_narration_track.py   # junta a narração num único wav com os delays certos
python3 compose_music.py           # compõe a trilha original (MIDI)

fluidsynth -ni /usr/share/sounds/sf2/FluidR3_GM.sf2 musica.mid -F musica_raw.wav -r 44100

TOTAL=$(python3 -c "import json;print(json.load(open('timeline.json'))['totalDurationMs']/1000)")
ffmpeg -y -i musica_raw.wav -af "aecho=0.8:0.7:40|60:0.28|0.18,lowpass=f=6000,afade=t=in:d=2,afade=t=out:st=$(python3 -c "print($TOTAL-3)"):d=3,atrim=0:$TOTAL,apad=whole_dur=$TOTAL" musica_final.wav

ffmpeg -y -i audio/narracao_completa.wav -i musica_final.wav -filter_complex "
[1:a]volume=17dB[music_boosted];
[music_boosted][0:a]sidechaincompress=threshold=0.04:ratio=10:attack=5:release=400:makeup=1[music_ducked];
[0:a][music_ducked]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[out]
" -map "[out]" audio/mix_final.wav

python3 gen_render_html.py
CHROME_PATH=/usr/bin/google-chrome-stable node capture.js

mkdir -p out
ffmpeg -y -framerate 24 -i frames/vida/frame_%05d.png -i audio/mix_final.wav \
  -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p -c:a aac -b:a 160k \
  -movflags +faststart -shortest out/minha-vida.mp4

cp out/minha-vida.mp4 ../../assets/videos/minha-vida.mp4
```

## Editar o roteiro

Edite `script.json` (texto de cada cena) e `build_timeline.py` (legendas,
imagem de cada cena) e rode o pipeline de novo. As ilustrações ficam em
`images/*.jpg` — foram geradas com um gerador de imagens a partir da foto
real da Priscila como referência de rosto, num estilo aquarela editorial
consistente.

## Renderização determinística

`render/vida.html` não usa `setTimeout`/CSS `@keyframes` para as
transições e o efeito Ken Burns — tudo é calculado a partir de um "tempo
virtual" (`window.__render(t)`), então a captura de frames funciona de
forma exatamente igual não importa quanto tempo o processo de screenshot
realmente leve (evita bugs de deriva de tempo).
