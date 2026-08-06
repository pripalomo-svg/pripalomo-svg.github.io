# Vídeo "Draw my life" — linha do tempo (baseado no Memorial)

Vídeo estilo **draw my life** em **formato linha do tempo** (lousa branca, desenho
à mão que se desenha sozinho, marcador seguindo o traço, legendas manuscritas e
uma linha do tempo com anos + ponto que avança), narrado em português.

Conta a trajetória da Priscila com base no **Memorial** (MEMORIAL out/2025):
nascimento em São Paulo (1983), infância de "criança cientista", os livros da
adolescência, a Psicologia, os mestrados na **Universidad de Salamanca**, o
doutorado na **Universitat de València** (Labpsitec, embodiment, realidade
virtual), os orientadores **Rosa María Baños**, **Ausiàs Cebolla** e **Marcelo
Demarzo**, o **Cum Laude / Doutora Internacional (2016)**, a volta ao Brasil como
professora — e, hoje, aos 43 anos, a família: duas mães e dois filhos.

Saída: `assets/videos/draw-minha-vida-linha-tempo.mp4` (1920×1080, ~114s, narração pt-BR).

## Arquivos

- `script.json` — narração de cada cena.
- `render/linha-tempo.html` — animação determinística (`window.__render(t)`), com
  helpers de desenho (pessoas, mãos, livros, coração, Espanha, óculos de RV, diploma…),
  legendas com nomes e a barra de linha do tempo. Cenas e desenhos no array `SCENES`.
- `capture.js` — captura de frames (puppeteer-core + Chrome).
- `build.py` — pipeline completo (narração → durações → injeção → captura → MP4).

## Gerar do zero

```bash
cd tools/video-linha-tempo
npm install
pip install edge-tts

python3 build.py            # narração + vídeo
python3 build.py --silent   # sem narração (durações padrão)
```

## Editar

- Texto: `script.json`.
- Desenhos/legendas/linha do tempo: array `SCENES` em `render/linha-tempo.html`.
  Cenas com `year` ganham uma marca na linha do tempo.
- Rode `python3 build.py` de novo.
