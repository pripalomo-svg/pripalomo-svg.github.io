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
- `cursos.html` — **cursos**: cards montados em runtime a partir de `dados/projetos.json` (itens `tipo: "curso"`; checkout na Hotmart).
- `produtos.html` — **loja "Materiais"**: cards montados a partir de `dados/projetos.json` (itens que não são curso). Botão de compra: `linkPagina` > `arquivo` (PDF grátis) > `linkCheckout` > modal `openPay` (WhatsApp/cartão/Pix).
- `painel.html` — **painel admin** (noindex, fora do menu público): edita `dados/projetos.json` e publica com um clique via GitHub Contents API (token fine-grained no `localStorage`, chave `pp_gh_token`); fallback "Baixar projetos.json". Também lista atalhos de edição do blog.
- `apresentacao.html` — bio + vídeos "draw my life".
- `escada-segura.html` — landing do produto "Programa Escada Segura".
- `catalogo-videos.html` — catálogo interno de vídeos.

## Conteúdo em Markdown (blog)

- `assets/content.js` → `listarMarkdown(pasta)` lê um **índice estático**
  `<pasta>/index.json` (uma lista de slugs) — **não** depende de API externa.
- **Para publicar um artigo:** crie `posts/<slug>.md` (com front-matter
  `titulo`, `data`, `tag`, `cor`, `resumo`) **e** adicione `"<slug>"` em
  `posts/index.json`. Veja `COMO-USAR.md`.
- Markdown é renderizado no navegador com `marked` (CDN jsDelivr); há fallback
 simples se a CDN falhar.
- Obs.: a pasta `produtos/*.md` é um resquício da antiga loja e não é mais
 lida por nenhuma página.

## Cursos e produtos (dados/projetos.json)

- **Fonte única**: `dados/projetos.json` — lista de projetos com `id`, `tipo`
 (`curso` | `ebook` | `programa` | `gratuito`), `titulo`, `descricao`, `tag`,
 `meta`, `preco`, `precoDe`, `linkCheckout`, `arquivo`, `linkPagina`, `visivel`.
- `assets/projetos.js` — `carregarProjetos()`, `montarLoja()` (produtos.html)
 e `montarCursos()` (cursos.html). Cards construídos via DOM (sem innerHTML
 com dados).
- Edição recomendada pelo `painel.html` (dashboard); publicação = commit de
 `dados/projetos.json` na `main` via GitHub Contents API.

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
