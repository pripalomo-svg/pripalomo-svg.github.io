# AGENTS.md

## Cursor Cloud specific instructions

This repository is a **static, single-page website** (GitHub Pages site `pripalomo-svg.github.io`) — the
landing page for Dra. Priscila Palomo's "Vencendo a Fobia" program. There is no build system, package
manager, dependencies, tests, or lint configuration.

- The entire site is a single self-contained file: `index.html` (all CSS and JS are inline). `index.html.html`
  is an identical duplicate of `index.html`.
- External resources (Google Fonts, images) are loaded from CDNs over HTTPS, so an internet connection is
  needed for the page to look fully styled.
- **Run / develop:** serve the directory with any static file server, e.g. `python3 -m http.server 8000`,
  then open `http://localhost:8000/`. Edit `index.html` and refresh the browser (no hot-reload).
- There is nothing to install, build, lint, or test — the update script is intentionally a no-op.
