# AGENTS.md

Guia para agentes e devs que trabalham neste repositório.

## O que é

Site estático da **Priscila Palomo** — psicóloga (CRP 98007), doutora em
Neurociência e Comportamento (USP). Posicionamento atual: **saúde mental no
trabalho com base em neurociência e evidência** (B2B: diagnóstico psicossocial
NR-1, programas de regulação emocional, treinamento de lideranças, palestras e
consultoria científica para healthtechs), com a clínica de fobias e ansiedade
como frente B2C. A justificativa da escolha de nicho está em `ANALISE-NICHO.md`.
**Sem build, sem gerenciador de pacotes, sem dependências** para servir:
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

- `index.html` — **home B2B (empresas)**: hero, dados (NR-1, burnout, INSS),
  5 soluções, método em 4 etapas, calculadora de custo do adoecimento mental,
  credenciais, atalho para a clínica e CTA de diagnóstico.
- `fobias.html` — **clínica (pessoas)**: psicoeducação sobre fobias e ansiedade
  de desempenho (desenhos animados) + boas-vindas e newsletter. Era a antiga home.
- `pesquisa.html` — **ciência**: linhas de pesquisa, publicações selecionadas,
  laboratórios parceiros, docência, formação e consultoria para healthtechs.
- `blog.html` — **blog**: lista os artigos de `posts/*.md`.
- `post.html?p=<slug>` — renderiza um artigo de `posts/<slug>.md`.
- `cursos.html` — **cursos** (checkout na Hotmart; cards fixos no HTML).
- `apresentacao.html` — bio + vídeos "draw my life".
- `escada-segura.html` — landing do produto "Programa Escada Segura".
- `catalogo-videos.html` — catálogo interno de vídeos.
- `dashboard.html` — **Desk**: painel interno com o link e uma frase de status
  de cada projeto; atalhos em `desk/` para salvar no Desktop.
- `terapia-pro.html` — **Terap-ia OS**: sistema de banco da clínica (login/senha,
  pacientes, agenda Google + WhatsApp). Mensalidade R$ 100 (Pix `11950690537`
  ou PagSeguro/cartão). Sem tour de boas-vindas. Dados isolados por usuário
  no navegador; nuvem recomendada para 1000 clínicas: **Supabase** (auth +
  Postgres com RLS) + **Cloudflare R2** (arquivos, muito espaço).
  Estilos/JS em `assets/terapia-os.css` e `assets/terapia-os.js`.

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

- Paleta corporativa-científica: **navy `#0B1F3A`** (títulos/fundo escuro),
  **teal `#0E7C7B`** (ação/destaque), **sand `#F5F1EA`** (fundo claro) e
  **gold `#C9A227`** (detalhe). Definidas em `assets/style.css` como
  `--navy`, `--teal`, `--sand`, `--gold`; os nomes antigos (`--preto`,
  `--dourado`, `--creme`…) continuam como aliases para não quebrar páginas.
- Tipografia: **Sora** (títulos, `--font-title`) e **Inter** (texto,
  `--font-body`) via Google Fonts.
- Logo: monograma "PP" em `assets/logo.svg`.
- Navegação padrão em todas as páginas: Empresas · Fobias e ansiedade ·
  Ciência · Blog · Cursos · Sobre + CTA "Falar com a Priscila".
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
