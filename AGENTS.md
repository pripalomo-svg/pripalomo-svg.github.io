# AGENTS.md

## Cursor Cloud specific instructions

This repository is a **static website** (the site of Dra. Priscila Palomo — a
psychology blog + PDF store). There is **no build step, no package manager, and
no dependencies to install**. It is plain HTML/CSS/JS served as static files.

### Running the site (dev)

Serve the repo root over HTTP (per `README.md`):

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

Do **not** open the `.html` files via `file://` — the JS uses `fetch()` which
requires an HTTP origin.

### Pages

- `index.html` — blog homepage; lists articles from `posts/*.md`.
- `post.html?p=<slug>` — renders a single article from `posts/<slug>.md`.
- `loja.html` — store; lists products from `produtos/*.md`.
- `programa.html` — landing page for the "Vencendo a Fobia" program.

### Non-obvious caveats

- **Listing depends on the GitHub public API + internet.** The blog and store
  listings (`assets/content.js` → `listarMarkdown()`) call
  `https://api.github.com/repos/pripalomo-svg/pripalomo-svg.github.io/contents/...?ref=main`,
  i.e. they list the files published on the **`main` branch of the live repo**,
  not your local working copy. So locally a brand-new `.md` file you add will
  **not** appear in the listing until it is committed/pushed to `main`. Internet
  access is required for the listings to populate; without it the page shows
  "Não foi possível carregar os artigos agora."
- **Individual pages read local files.** `post.html?p=...` and the product
  detail content are fetched from the local server, so they reflect your working
  copy regardless of the API.
- External assets (Google Fonts, `marked` via jsDelivr CDN) are loaded from the
  internet; `md2html()` has a basic fallback if `marked` fails to load.
- There are **no lint, automated test, or build commands** in this repo.

### Contact constants

WhatsApp number and Pix key live in `assets/app.js` (`WHATSAPP`, `PIX_KEY`).
