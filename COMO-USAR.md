# Guia rápido — como atualizar meu site

Olá, Priscila! Tudo é feito pelo site do GitHub, no navegador — sem instalar nada.

> Endereço do projeto: https://github.com/pripalomo-svg/pripalomo-svg.github.io

**Seu painel (atualizar cursos e materiais):** https://www.priscilapalomo.com/painel.html  
*(Se ainda não estiver no ar, use o link que aparece no rodapé do site ou na seção de boas-vindas da home.)*

Sempre que você salvar ("Commit changes"), o site atualiza em 1 a 2 minutos.

---

## Atualizar cursos e materiais (o jeito fácil: painel)

Abra **www.priscilapalomo.com/painel.html** no navegador. Lá você consegue:

- Mudar título, descrição, preço e link de compra de cada curso/material;
- Ocultar ou mostrar um item no site (caixinha "Visível no site");
- Adicionar ou remover projetos;
- Ver atalhos para editar os artigos do blog.

Quando terminar, clique em **"Publicar no site"** — o site atualiza sozinho
em 1 a 2 minutos.

> **Primeira vez?** O botão "Publicar no site" precisa de um código de acesso
> do GitHub (token). O passo a passo para criar está dentro do próprio painel,
> em "Publicação com um clique". Você faz isso uma vez só; o código fica
> guardado no seu navegador.

Se preferir não usar o código, clique em **"Baixar projetos.json"** e suba o
arquivo baixado no GitHub, na pasta `dados`, substituindo o `projetos.json`.

Os produtos aparecem na página **Materiais** (`produtos.html`) e os cursos na
página **Cursos** (`cursos.html`). Nos itens **sem** link de compra, o botão
"Comprar agora" abre as opções de pagamento direto no site: WhatsApp, cartão
e Pix. Nos itens **com** link (Hotmart, Mercado Pago…), o botão leva o cliente
direto para o checkout.

---

## Escrever um novo artigo no blog

São **dois passos**: criar o arquivo do artigo e registrá-lo no índice.

### Passo 1 — Criar o arquivo do artigo

1. Entre na pasta **`posts`** no GitHub.
2. Clique em **"Add file" → "Create new file"**.
3. Dê um nome curto terminando em `.md`.
   Ex.: `ansiedade-no-trabalho.md` (use só letras minúsculas e hífens).
4. Cole o modelo abaixo e preencha com seu conteúdo:

```
---
titulo: Como lidar com a ansiedade no trabalho
data: 2026-07-12
tag: Ansiedade
resumo: Uma frase curta que aparece na lista do blog.
---

Escreva aqui o seu texto normalmente.

## Subtítulo

Você pode usar **negrito**, listas:

- item um
- item dois

E subtítulos com ##.
```

5. Clique em **"Commit changes"** para salvar.

### Passo 2 — Registrar no índice

1. Ainda na pasta `posts`, abra o arquivo **`index.json`**.
2. Clique no ícone de lápis (editar).
3. Adicione o nome do seu arquivo (sem o `.md`) no início da lista, entre aspas.

**Exemplo** — se você criou `ansiedade-no-trabalho.md`, o arquivo ficará assim:

```
["ansiedade-no-trabalho","vencendo-a-ansiedade","toc-pensamentos-intrusivos","entendendo-as-fobias","autoconhecimento-rotina"]
```

4. Clique em **"Commit changes"**.

Pronto! O artigo aparece no blog.

---

## O que significa cada linha do cabeçalho (entre os `---`)

| Linha | Para que serve | Obrigatório? |
| --- | --- | --- |
| `titulo` | Título do artigo | Sim |
| `data` | Data no formato `ano-mês-dia` (ex.: `2026-07-12`) | Sim |
| `tag` | Categoria (ex.: Ansiedade, Fobias, TOC) | Opcional |
| `resumo` | Frase curta que aparece na lista. Se não preencher, o site usa o início do texto. | Opcional |

---

## Mudar o WhatsApp ou a chave Pix

Abra o arquivo `assets/app.js` e edite as primeiras linhas:

```
const WHATSAPP = '5511950690537';
const PIX_KEY   = '11950690537';
```

---

## Formas de pagamento (WhatsApp, Pix e cartão de crédito)

Ao clicar em **Comprar agora** na página do Programa Escada Segura, aparecem
três opções: **WhatsApp**, **cartão de crédito** e **Pix**.

Para o **cartão de crédito**, abra `assets/app.js` e preencha a linha:

```
const CARTAO_LINK = '';
```

- Se você tem um link de checkout (ex.: **Mercado Pago**, **PagSeguro** ou
  **InfinitePay**), cole-o entre as aspas. O botão "Cartão de crédito" leva o
  cliente direto para esse pagamento.
- Se deixar vazio (`''`), o botão abre o WhatsApp com uma mensagem pronta
  pedindo o link de pagamento no cartão.

---

Qualquer dúvida, é só me chamar.
