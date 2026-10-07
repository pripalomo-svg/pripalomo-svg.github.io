# AGENTS.md

Guia para agentes e devs que trabalham neste repositório.

## Como falar com a Priscila

A dona do site é psicóloga, não programadora. Ela usa o Cursor para cuidar do
site e acha confuso quando a resposta vem cheia de arquivo, branch, commit ou
código. O jeito prático está no Desk (`dashboard.html`, seção "Pedir uma
mudança"): recados prontos para copiar e colar.

- Responda em português do Brasil, em frases curtas.
- Ela pede do jeito que fala ("muda o preço", "publica um texto", "isso está
  confuso"). Entenda o pedido e altere o site.
- No fim, diga só o que mudou, em qual página, e que entra no ar quando a
  alteração for publicada. Não mostre código, a menos que ela peça.
- Não peça para ela editar arquivo no GitHub, rodar comando ou escolher branch.
- Se o pedido for vago, faça a melhoria mais concreta e útil e mostre o
  resultado. Não invente página, preço ou promessa clínica que ela não pediu.
- Tarefas comuns: artigo em `posts/` + slug em `posts/index.json`; texto das
  páginas HTML; WhatsApp, Pix e link de cartão em `assets/app.js`; frase de
  status no `dashboard.html`.

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

- `index.html` — **home**: hero com **vídeo institucional** (loop mudo +
  botão "Assistir com som" que abre `#videoModal`), faixa de instituições,
  **dois caminhos** (empresas / pessoas), dados (NR-1, burnout, INSS), 6 blocos
  de soluções (`.features`), método em 4 etapas, calculadora de custo,
  credenciais, sobre, faixa da clínica, NeuroNews e CTA. JSON-LD (Person +
  ProfessionalService + VideoObject + WebSite).
- `privacidade.html` — política de privacidade (LGPD; `noindex`).
- `loja.html` — **loja** de produtos digitais (checkout via modal `openPay`:
  Pix/WhatsApp/cartão). Landings em `produtos/<slug>.html`; conteúdo integral
  de cada produto em `produtos/conteudo/<slug>.md`.
- `divulgacao.html` — plano de divulgação (noindex; acessível pelo Desk).
  Materiais prontos em `marketing/`; resumo em `PLANO-DIVULGACAO.md`.
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
  de cada projeto; atalhos em `desk/` para salvar no Desktop; recados prontos
  para pedir uma mudança no Cursor sem falar de código.
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

## Layout e componentes (design system)

Cabeçalho, rodapé, skip link, breadcrumbs e botão flutuante de WhatsApp são
**gerados por `tools/layout/injetar.py`** e aplicados a todas as páginas
públicas (inclusive `produtos/*.html`, com prefixo `../`). Para mudar o menu
ou o rodapé, edite o script e rode `python3 tools/layout/injetar.py`. Para
uma página nova, deixe `<header class="site-header"></header>` e
`<footer class="site-footer"></footer>` vazios, cadastre-a em `PAGINAS`
(item ativo + breadcrumbs) e rode o script.

Menu: **Para empresas** (dropdown com 6 itens) · **Para você** (dropdown com
5 itens) · Ciência · Blog · Loja · Sobre + botão "Agendar conversa". No mobile
vira gaveta lateral com acordeões (`assets/app.js`).

Componentes em `assets/style.css`: `hero` (+ `hero-video`), `page-hero`,
`crumbs`, `paths`/`path`, `trust`, `features`/`feature`, `section`
(+ `--alt`, `--dark`, `--teal`, `--tight`), `section-head` (+ `--row`),
`kicker`, `lead`, `grid grid-2/3/4`, `split`, `card` (+ `--dark`, `--teal`,
`checks`, `card-foot`), `stats`/`stat`, `callout`, `steps`, `timeline`,
`cred-list`, `quote`, `band`, `calc`, `video-card`, `post-grid`/`post-card`,
`article`, `news`, `btn` (+ `-primary`, `-outline`, `-dark`, `-white`, `-lg`,
`-sm`), `wa-float`, `toast`, `video-modal`. Páginas internas (`dashboard.html`,
`extrato-2026.html`) usam `<nav>`/`<footer>` simples; há estilos legados no fim
do CSS; não remova.

Regras de estilo que mantêm o aspecto corporativo: uma única cor de ação
(`--brand`), títulos em `Inter Tight` com tracking negativo, sem gradientes
radiais, sem emojis na interface, ícones SVG de linha (24px, stroke 1.8),
kickers em caixa baixa e travessões evitados em títulos.

## Identidade visual

- Paleta: **navy `#0B2545`** (títulos, rodapé, fundos escuros), **brand
  `#0E7C76`** (botões, links, ícones; `--brand`), teal claro `#E6F4F2`, fundos
  `#F5F7FA`, dourado `#C99A2E` só em detalhes. Tokens em `assets/style.css`
  (`--navy`, `--brand`, `--bg-alt`…); `--teal`, `--teal-dark`, `--preto`,
  `--dourado`, `--creme`, `--sand` continuam como aliases.
- Tipografia: **Inter Tight** (títulos, `--font-title`) e **Inter** (texto,
  `--font-body`) via Google Fonts.
- Logo: monograma "P" em `assets/logo.svg`.
- SEO: toda página pública tem `canonical`, Open Graph, `theme-color`; title
  30–65 caracteres e description 70–160 (o auditor cobra isso).

## Contato e newsletter

- WhatsApp e chave Pix em `assets/app.js` (`WHATSAPP`, `PIX_KEY`).
- Newsletter **NeuroNews**: `subscribe()` em `app.js` (sem backend — abre o WhatsApp).

## Vídeos

- **Institucional** (`tools/video-institucional`): motion graphics em canvas
  determinístico (`render/institucional.html`, `window.__render(t)`), narração
  `edge-tts` (`script.json`), trilha ambiente própria (`compose_ambient.py`,
  numpy), captura com puppeteer e MP4 1280×720 via ffmpeg. Saída:
  `assets/videos/institucional.mp4` + `institucional-poster.jpg`, usados no
  hero da home. Regenerar: `npm install && pip install edge-tts && python3 build.py`.
- **"Draw my life"** (`tools/video-linha-tempo`, `video-historia`…): mesmo
  esquema, embutidos em `apresentacao.html`.

## Qualidade e monitoramento

- `python3 tools/auditoria/auditar.py --base http://localhost:8000` audita
  títulos, descriptions, h1, alt, canonical, OG, JSON-LD, peso, TTFB e links
  quebrados; sai com código 1 se houver item crítico. Rode antes de abrir PR.
- `.github/workflows/auditoria-diaria.yml` roda todo dia (Lighthouse + auditor)
  e publica o relatório na issue "Monitoramento diário do site".
- `MONITORAMENTO.md` explica as metas; `.cursor/automation-monitor.md` é o
  prompt do agente diário de melhoria (Cursor Automations).
- Ética (Código de Ética do Psicólogo, art. 20): sem promessa de resultado,
  sem depoimentos de pacientes, sem sensacionalismo, sem preço como chamariz
  de serviço clínico. Produtos digitais podem exibir preço de forma sóbria.

Não há build nem lint; o auditor acima é o único teste automatizado.
