# 💛 Guia rápido — como atualizar meu site

Olá, Dra. Priscila! Este guia mostra, de um jeito simples, como **escrever no blog**
e **adicionar seus produtos em PDF**. Tudo é feito pelo site do GitHub, no navegador
— você não precisa instalar nada nem mexer em código.

> Endereço do seu projeto:
> https://github.com/pripalomo-svg/pripalomo-svg.github.io

Sempre que você salvar uma alteração ("Commit changes"), o site se atualiza
sozinho em 1 a 2 minutinhos. ✨

---

## ✍️ Escrever um novo artigo no blog

Cada artigo é **um arquivo** na pasta `posts/`. Para criar um novo:

1. Entre na pasta **`posts`** no GitHub.
2. Clique em **"Add file" → "Create new file"**.
3. No nome do arquivo, escreva algo curto terminando em **`.md`**.
   Ex.: `ansiedade-no-trabalho.md` (use só letras minúsculas e hífens).
4. Cole o modelo abaixo e troque pelo seu conteúdo:

```
---
titulo: Como lidar com a ansiedade no trabalho
data: 2026-06-20
tag: Ansiedade
cor: c-la
---

Escreva aqui o seu texto normalmente.

Para criar um **subtítulo**, use duas cerquilhas:

## Meu subtítulo

Você pode deixar palavras em **negrito**, fazer listas:

- primeiro item
- segundo item

E também listas numeradas:

1. passo um
2. passo dois
```

5. Clique na aba **"Preview"** (no topo do editor) para ver como vai ficar.
6. Role até o fim e clique em **"Commit changes"**.

Pronto! O artigo aparece **sozinho** na página inicial do blog. Não precisa mexer
em mais nada. 🎉

### O que significa cada linha do topo (entre os `---`)

| Linha | Para que serve | Obrigatório? |
| --- | --- | --- |
| `titulo` | O título do artigo | ✅ Sim |
| `data` | Data no formato `ano-mês-dia` (ex.: `2026-06-20`) | ✅ Sim |
| `tag` | Etiqueta/categoria (ex.: Ansiedade, Fobias, TOC) | Opcional |
| `cor` | Cor da capa: deixe vazio (`""`) para azul, ou `c-la` (laranja), `c-ou` (dourado), `c-vd` (verde) | Opcional |
| `resumo` | Frase curta que aparece no cartão. Se não escrever, o site usa o começo do texto | Opcional |

O tempo de leitura é calculado automaticamente. 😉

---

## 🛒 Adicionar um produto em PDF na loja

São 2 passinhos: subir o PDF e criar a "ficha" do produto.

### Passo 1 — Subir o arquivo PDF

1. Entre na pasta **`pdfs`** no GitHub.
2. Clique em **"Add file" → "Upload files"**.
3. Arraste seu PDF e clique em **"Commit changes"**.

### Passo 2 — Criar a ficha do produto

1. Entre na pasta **`produtos`**.
2. Clique em **"Add file" → "Create new file"**.
3. Dê um nome terminando em `.md`. Ex.: `5-meu-novo-ebook.md`.
   (O número no começo define a ordem na loja: 1, 2, 3…)
4. Cole um dos modelos abaixo.

**Produto PAGO** (botão "Comprar agora" → pagamento por Pix/WhatsApp):

```
---
titulo: Guia da Ansiedade
tag: E-book
cor: c-la
paginas: 32 páginas
precoDe: R$ 49
preco: R$ 29
arquivo: ""
---
Descrição curta que aparece no cartão do produto.
```

**Produto GRÁTIS** (botão "Baixar PDF grátis" → download na hora):

```
---
titulo: Material Gratuito
tag: Grátis
cor: ""
paginas: 12 páginas
preco: ""
arquivo: pdfs/guia-da-ansiedade.pdf
---
Descrição curta do material gratuito.
```

5. Clique em **"Commit changes"**.

### A regrinha mais importante

- **Pago:** preencha `preco` (ex.: `R$ 29`) e deixe `arquivo: ""`.
- **Grátis:** deixe `preco: ""` e coloque o caminho do PDF em `arquivo`
  (ex.: `pdfs/meu-arquivo.pdf`).

> ⚠️ **Atenção:** arquivos na pasta `pdfs/` ficam públicos (qualquer pessoa com o
> link baixa). Por isso, para produtos **pagos**, o ideal é **não** subir o PDF
> aberto — entregue o arquivo pelo WhatsApp depois do pagamento, ou use uma
> plataforma como Hotmart/Eduzz/Gumroad. Para materiais **grátis**, pode subir
> tranquilamente.

---

## 📞 Mudar seu WhatsApp ou chave Pix

Esses dados ficam no arquivo `assets/app.js`, nas primeiras linhas:

```
const WHATSAPP = '5511950690537';
const PIX_KEY   = '11950690537';
```

É só editar os números entre aspas e salvar.

---

Qualquer dúvida, é só me chamar que eu ajusto para você. 💛
