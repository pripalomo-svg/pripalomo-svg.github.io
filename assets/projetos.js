/* =========================================================
   Priscila Palomo — Projetos (cursos e materiais)
   Lê a fonte única de dados "dados/projetos.json" e monta
   os cards da loja (produtos.html) e dos cursos (cursos.html).

   >>> Você NÃO precisa editar este arquivo. <<<
   Para alterar títulos, preços e links, use o painel.html
   (ou edite dados/projetos.json direto no GitHub).
   ========================================================= */

async function carregarProjetos(){
  const res = await fetch('dados/projetos.json?v=' + Date.now());
  if(!res.ok) throw new Error('Falha ao ler dados/projetos.json (' + res.status + ')');
  return res.json();
}

/* Cria um elemento com classe e texto (sempre via textContent — sem injeção) */
function _el(tag, cls, texto){
  const e = document.createElement(tag);
  if(cls) e.className = cls;
  if(texto != null) e.textContent = texto;
  return e;
}

/* Botão de compra de acordo com os dados do projeto:
   1) linkPagina  -> leva à página do produto (ex.: escada-segura.html)
   2) arquivo     -> download direto (materiais gratuitos)
   3) linkCheckout-> abre o checkout (Hotmart, Mercado Pago etc.)
   4) nenhum      -> abre o modal de pagamento (WhatsApp / cartão / Pix) */
function _botaoCompra(p, rotuloComprar){
  if(p.linkPagina){
    const a = _el('a', 'btn btn-gold', 'Conhecer o programa');
    a.href = p.linkPagina;
    return a;
  }
  if(p.arquivo){
    const a = _el('a', 'btn btn-outline', 'Baixar grátis (PDF)');
    a.href = p.arquivo;
    a.target = '_blank';
    a.rel = 'noopener';
    return a;
  }
  if(p.linkCheckout){
    const a = _el('a', 'btn btn-gold', rotuloComprar);
    a.href = p.linkCheckout;
    a.target = '_blank';
    a.rel = 'noopener';
    return a;
  }
  const b = _el('button', 'btn btn-gold', rotuloComprar);
  b.type = 'button';
  b.addEventListener('click', () => openPay(p.titulo, p.preco || ''));
  return b;
}

/* Card da loja (produtos.html) */
function cardProduto(p){
  const art = _el('article', 'product rv vis');
  if(p.tag) art.appendChild(_el('span', 'post-tag', p.tag));
  art.appendChild(_el('h4', '', p.titulo));
  if(p.meta) art.appendChild(_el('div', 'product-pages', p.meta));
  art.appendChild(_el('p', 'desc', p.descricao || ''));

  const preco = _el('div', 'product-price');
  if(p.preco){
    preco.appendChild(_el('span', 'now', p.preco));
    if(p.precoDe) preco.appendChild(_el('span', 'old', p.precoDe));
  }else{
    preco.appendChild(_el('span', 'free', p.arquivo ? 'Grátis' : ''));
  }
  art.appendChild(preco);

  const acoes = _el('div', 'product-actions');
  acoes.appendChild(_botaoCompra(p, 'Comprar agora'));
  art.appendChild(acoes);
  return art;
}

/* Card de curso (cursos.html) */
function cardCurso(p){
  const art = _el('article', 'curso');
  art.appendChild(_el('span', 'curso-tag', p.tag || 'Curso online'));
  art.appendChild(_el('h3', '', p.titulo));
  art.appendChild(_el('p', '', p.descricao || ''));
  if(p.meta) art.appendChild(_el('div', 'curso-meta', p.meta));
  art.appendChild(_botaoCompra(p, 'Comprar curso'));
  const mini = p.preco
    ? 'Investimento: ' + p.preco + (p.precoDe ? ' (de ' + p.precoDe + ')' : '')
    : 'Valor e inscrição na Hotmart';
  art.appendChild(_el('span', 'curso-mini', mini));
  return art;
}

/* Monta a loja: todos os projetos visíveis que não são cursos */
async function montarLoja(container, msgVazio){
  try{
    const projetos = await carregarProjetos();
    const itens = projetos.filter(p => p.visivel !== false && p.tipo !== 'curso');
    container.innerHTML = '';
    if(!itens.length){
      container.appendChild(_el('p', 'loja-vazia', msgVazio || 'Novos materiais em breve!'));
      return;
    }
    itens.forEach(p => container.appendChild(cardProduto(p)));
  }catch(e){
    container.innerHTML = '';
    container.appendChild(_el('p', 'loja-vazia', 'Não foi possível carregar os materiais agora. Tente novamente em instantes.'));
  }
}

/* Monta os cursos: projetos visíveis do tipo "curso" */
async function montarCursos(container){
  try{
    const projetos = await carregarProjetos();
    const itens = projetos.filter(p => p.visivel !== false && p.tipo === 'curso');
    container.innerHTML = '';
    if(!itens.length){
      container.appendChild(_el('p', 'loja-vazia', 'Novos cursos em breve!'));
      return;
    }
    itens.forEach(p => container.appendChild(cardCurso(p)));
  }catch(e){
    container.innerHTML = '';
    container.appendChild(_el('p', 'loja-vazia', 'Não foi possível carregar os cursos agora. Tente novamente em instantes.'));
  }
}
