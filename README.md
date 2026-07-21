# Site da Dra. Priscila Palomo

Site oficial da Dra. Priscila Palomo — Psicóloga (CRP 98007). Inclui um **blog**
e a landing do produto **[Programa Escada Segura](escada-segura.html)**
(workbook de 21 dias, R$ 97).

🔗 No ar em: https://www.priscilapalomo.com (e https://pripalomo-svg.github.io)

> 👉 **Para atualizar o site no dia a dia, leia o [`COMO-USAR.md`](COMO-USAR.md).**
> Lá estão os passos simples para escrever artigos —
> tudo em Markdown, sem precisar mexer em código.

## Como funciona

O conteúdo é separado do layout. Você só cria arquivos `.md`:

- **Blog:** cada artigo é um arquivo em `posts/` (ex.: `posts/meu-artigo.md`).
  A página do blog (`blog.html`) lista os artigos **automaticamente**.

A listagem da pasta é feita pela API pública do GitHub e o texto Markdown é
renderizado no navegador (biblioteca `marked`), sem nenhum passo de build.

## Estrutura

| Arquivo / pasta | O que é |
| --- | --- |
| `index.html` | **Página de abertura** — psicoeducação sobre fobias |
| `blog.html` | Blog + apresentação (lista os artigos sozinha) |
| `post.html` | Página que exibe um artigo (abre via `post.html?p=nome-do-arquivo`) |
| `posts/` | Artigos do blog, **um arquivo `.md` por artigo** |
| `escada-segura.html` | Landing do **Programa Escada Segura** (produto pago) |
| `fobias.html` | Redireciona para a página inicial (`index.html`) |
| `assets/style.css` | Estilos compartilhados |
| `assets/app.js` | Scripts (menu, pagamento, newsletter) e dados de contato |
| `assets/content.js` | Carregador dos arquivos Markdown (não precisa editar) |
| `COMO-USAR.md` | **Guia simples** de como publicar artigos |

## Testar localmente

```bash
python3 -m http.server 8000
# abra http://localhost:8000
```

> Observação: localmente, a *listagem* de artigos usa a API do GitHub e
> mostra o que está publicado na branch `main`. As páginas individuais
> (`post.html?p=...`) leem os arquivos locais normalmente.

## Contato configurado

- WhatsApp: `5511950690537`
- Chave Pix (telefone): `11950690537`

Edite esses valores em `assets/app.js` (constantes `WHATSAPP` e `PIX_KEY`).
