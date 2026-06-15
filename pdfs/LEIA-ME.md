# 📄 Pasta de produtos em PDF

Coloque aqui os arquivos PDF que você quer vender ou disponibilizar na loja.

## Como adicionar um novo produto

1. **Suba o arquivo PDF** dentro desta pasta `pdfs/`.
   Ex.: `pdfs/diario-da-ansiedade.pdf`

2. **Abra o arquivo `loja.html`** (na raiz do site) e procure a lista
   `const PRODUTOS = [ ... ]` (perto do final do arquivo).

3. **Adicione ou edite um item** seguindo este modelo:

   ```js
   {
     titulo: "Nome do material",
     desc: "Descrição curta que aparece no card.",
     paginas: "24 páginas",
     tag: "E-book",            // etiqueta no topo da capa
     cor: "c-la",              // '' (azul) | 'c-la' (laranja) | 'c-ou' (dourado) | 'c-vd' (verde)
     capa: "pdfs/capa.jpg",    // opcional: imagem de capa
     precoDe: "R$ 49",         // opcional: preço antigo riscado
     preco: "R$ 29",           // vazio "" = produto GRÁTIS
     arquivo: "pdfs/meu-arquivo.pdf"  // PDF para download direto
   }
   ```

## Produto grátis x produto pago

- **Grátis:** deixe `preco: ""` e preencha `arquivo` com o caminho do PDF.
  O botão vira **"Baixar PDF grátis"** e o download é imediato.

- **Pago:** preencha `preco` (ex.: `"R$ 29"`) e deixe `arquivo: ""`.
  O botão vira **"Comprar agora"** e abre o pagamento por **Pix** ou **WhatsApp**.
  Depois de confirmar o pagamento, você envia o link/PDF para a pessoa.

  > Dica: se quiser entregar o PDF automaticamente após a venda, você pode
  > usar um serviço externo (ex.: Hotmart, Eduzz, Gumroad) e colocar o link
  > de checkout dentro de `arquivo` ou em um botão personalizado.

## Importante

Arquivos colocados nesta pasta ficam **públicos** no site (qualquer pessoa
com o link consegue baixar). Por isso, mantenha aqui apenas os materiais
gratuitos ou cujo acesso aberto não seja problema. Para produtos pagos com
entrega protegida, use uma plataforma de checkout externa.
