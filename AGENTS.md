# AGENTS.md

Guia para agentes e devs que trabalham neste repositório.

## O que é

Site estático da **Priscila Palomo** — psicóloga (CRP 98007), especialista em
fobias. **Sem build, sem gerenciador de pacotes, sem dependências** para servir:
é HTML/CSS/JS puro publicado como arquivos estáticos via **GitHub Pages** a
partir da branch **`main`**, no domínio **www.priscilapalomo.com** (arquivo `CNAME`).

O arquivo **`.nojekyll`** desliga o Jekyll para que os arquivos `.md` sejam
servidos crus (o site os lê via `fetch`).

## Rodar localmente

```bash
python3 -m http.server 8000
# abra http://localhost:8000
```

Não abra os `.html` via `file://` — o JS usa `fetch()`, que exige origem HTTP.

## Páginas

- `index.html` — **home**: landing de psicoeducação sobre fobias (desenhos animados) + seção de boas-vindas e newsletter.
- `blog.html` — **blog**: lista os artigos de `posts/*.md`.
- `post.html?p=<slug>` — renderiza um artigo de `posts/<slug>.md`.
- `cursos.html` — **cursos** (checkout na Hotmart; cards fixos no HTML).
- `apresentacao.html` — bio + vídeos "draw my life".
- `escada-segura.html` — landing do produto "Programa Escada Segura".
- `catalogo-videos.html` — catálogo interno de vídeos.
- `terapia-pro.html` — **Terap-ia OS**: sistema da clínica (abre direto,
  sem tela de login). Pacientes, agenda Google + WhatsApp. Dados no
  navegador. Estilos/JS em `assets/terapia-os.css` e `assets/terapia-os.js`.

## Conteúdo em Markdown (blog)

- `assets/content.js` → `listarMarkdown(pasta)` lê um **índice estático**
  `<pasta>/index.json` (uma lista de slugs) — **não** depende de API externa.
- **Para publicar um artigo:** crie `posts/<slug>.md` (com front-matter
  `titulo`, `data`, `tag`, `cor`, `resumo`) **e** adicione `"<slug>"` em
  `posts/index.json`. Veja `COMO-USAR.md`.
- Markdown é renderizado no navegador com `marked` (CDN jsDelivr); há fallback
  simples se a CDN falhar.
- Obs.: a pasta `produtos/*.md` é um resquício da antiga loja (removida); os
  cursos hoje ficam fixos em `cursos.html`.

## Identidade visual

- Paleta: **azul petróleo `#0E4A57`** + **laranja `#E27A2E`**, definidos como
  variáveis em `assets/style.css` (`--preto`, `--dourado`, etc.).
- Estilos reutilizáveis: `.welcome` (boas-vindas), `.news` (newsletter NeuroNews).

## Contato e newsletter

- WhatsApp e chave Pix em `assets/app.js` (`WHATSAPP`, `PIX_KEY`).
- Newsletter **NeuroNews**: `subscribe()` em `app.js` (sem backend — abre o WhatsApp).

## Vídeos "draw my life"

Ficam em `tools/video-*` (ex.: `tools/video-linha-tempo`). Determinísticos
(`window.__render(t)`), narração via `edge-tts`, captura com puppeteer, montagem
com ffmpeg. Regenerar:

```bash
cd tools/video-linha-tempo && npm install && pip install edge-tts && python3 build.py
```

O MP4 final vai para `assets/videos/` e é embutido em `apresentacao.html`.

## Sem lint / testes / build

Não há comandos de lint, teste automatizado ou build neste repositório.
