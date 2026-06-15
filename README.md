# Site da Dra. Priscila Palomo

Site oficial da Dra. Priscila Palomo — Psicóloga (CRP 98007). Inclui um **blog**
com artigos sobre psicologia e uma **loja de materiais em PDF**.

🔗 Publicado via GitHub Pages: https://pripalomo-svg.github.io

## Estrutura do site

| Arquivo / pasta | O que é |
| --- | --- |
| `index.html` | **Blog** (página inicial) com a lista de artigos |
| `posts/` | Páginas dos artigos do blog (um arquivo `.html` por post) |
| `loja.html` | **Loja** — vitrine dos produtos/materiais em **PDF** |
| `pdfs/` | Pasta onde ficam os arquivos PDF dos produtos |
| `programa.html` | Landing page do programa "Vencendo a Fobia" (mantida) |
| `assets/style.css` | Estilos compartilhados por todas as páginas |
| `assets/app.js` | Scripts (menu, pagamento, newsletter) |

## Como publicar (GitHub Pages)

O site é estático: basta os arquivos estarem no repositório com o GitHub Pages
ativado. Após o merge, as alterações aparecem em alguns minutos.
Para testar localmente:

```bash
python3 -m http.server 8000
# abra http://localhost:8000
```

## ✍️ Como adicionar um novo artigo no blog

1. Copie um arquivo de `posts/` (ex.: `posts/vencendo-a-ansiedade.html`) e
   renomeie (ex.: `posts/meu-novo-artigo.html`).
2. Edite o título, a data e o conteúdo dentro de `<div class="article-content">`.
3. Em `index.html`, duplique um bloco `<a class="post-card">...</a>` e aponte o
   `href` para o novo arquivo. Troque o título, a data e o resumo.

## 🛒 Como adicionar um produto em PDF na loja

1. Coloque o arquivo PDF dentro da pasta **`pdfs/`**.
2. Abra **`loja.html`** e edite a lista `const PRODUTOS = [ ... ]` (no final do
   arquivo). Veja instruções detalhadas em [`pdfs/LEIA-ME.md`](pdfs/LEIA-ME.md).

- **Produto grátis:** `preco: ""` + `arquivo: "pdfs/seu-arquivo.pdf"` → download direto.
- **Produto pago:** `preco: "R$ 29"` + `arquivo: ""` → abre pagamento via Pix/WhatsApp.

## Contato configurado

- WhatsApp: `5511950690537`
- Chave Pix (telefone): `11950690537`

Esses valores podem ser ajustados em `assets/app.js` (constantes `WHATSAPP` e `PIX_KEY`).
