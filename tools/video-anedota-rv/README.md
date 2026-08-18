# Vídeo "Uma história que eu vivi" — anedota (realidade virtual)

Vídeo curto estilo **draw my life** (lousa branca, desenho à mão, narração pt-BR
+ trilha pop-rock), contando uma **anedota** da vida da Priscila como psicóloga:
o primeiro dia no laboratório de realidade virtual em Valência, o susto de se ver
no topo de um prédio e a descoberta que definiu o seu trabalho com fobias.

Saída: `assets/videos/anedota-rv.mp4` (1920×1080, ~53s). Cores: azul petróleo + laranja.

## Arquivos
- `script.json` — narração de cada cena.
- `render/anedota.html` — animação determinística (`window.__render(t)`); cenas em `SCENES`.
- `capture.js` — captura de frames (puppeteer-core + Chrome).
- `compose_rock.py` — trilha pop-rock (numpy).
- `build.py` — pipeline (narração → durações → captura → música → MP4).

## Gerar
```bash
cd tools/video-anedota-rv
npm install
pip install edge-tts numpy
python3 build.py            # com narração + música
python3 build.py --silent   # sem narração
```

O MP4 vai para `assets/videos/anedota-rv.mp4` e é embutido em `apresentacao.html`.
