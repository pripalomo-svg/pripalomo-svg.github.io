/* =========================================================
   Dra. Priscila Palomo — scripts compartilhados
   ========================================================= */

/* =========================================================
   👉 SEUS DADOS DE CONTATO E LINKS  (edite só o que está entre aspas)
   ========================================================= */
const WHATSAPP = '5511950690537';      // seu WhatsApp com DDD (só números)
const PIX_KEY  = '11950690537';        // sua chave Pix
const EMAIL    = 'contato@pripalomo.com';
const INSTAGRAM = 'pripalomo';         // seu @ do Instagram (sem o @). Deixe '' para esconder.

/* Lista de botões que aparecem na seção "Meus links e contatos".
   Para esconder um link, apague o bloco dele. Para mudar o texto,
   troque o que está entre aspas. */
const LINKS = [
  { ico:'💬', titulo:'WhatsApp',  sub:'Agende sua conversa',         href:'https://wa.me/'+WHATSAPP+'?text=Ol%C3%A1%20Dra.%20Priscila!' },
  { ico:'📸', titulo:'Instagram', sub:'@'+INSTAGRAM,                 href:INSTAGRAM ? 'https://instagram.com/'+INSTAGRAM : '' },
  { ico:'📚', titulo:'Materiais', sub:'E-books e guias em PDF',      href:'loja.html' },
  { ico:'⭐', titulo:'Programa',  sub:'Vencendo a Fobia',            href:'programa.html' },
  { ico:'✉️', titulo:'E-mail',    sub:EMAIL,                         href:'mailto:'+EMAIL },
];

/* Se a foto .jpg não existir, tenta .png; se não houver nenhuma, mostra o
   espaço reservado bonito. Assim funciona com qualquer um dos dois formatos. */
function photoFallback(img){
  if(!img.dataset.triedPng && img.dataset.base){
    img.dataset.triedPng = '1';
    img.src = img.dataset.base + '.png';
    return;
  }
  img.classList.add('no-img');
}

/* Monta os links na página (usado na home) */
function renderLinks(idAlvo){
  const alvo = document.getElementById(idAlvo);
  if(!alvo) return;
  alvo.innerHTML = LINKS.filter(l=>l.href).map(l => `
    <a class="link-item" href="${l.href}" ${/^https?:/.test(l.href)?'target="_blank" rel="noopener"':''}>
      <span class="ico">${l.ico}</span>
      <span><strong>${l.titulo}</strong><small>${l.sub}</small></span>
    </a>`).join('');
}

/* ----- Menu mobile ----- */
function toggleMenu(){
  document.querySelector('.nav-links')?.classList.toggle('open');
}
document.querySelectorAll('.nav-links a').forEach(a=>{
  a.addEventListener('click',()=>document.querySelector('.nav-links')?.classList.remove('open'));
});

/* ----- Animação de revelar ao rolar ----- */
const _obs=new IntersectionObserver((entries)=>{
  entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('vis');_obs.unobserve(e.target);}});
},{threshold:.12});
document.querySelectorAll('.rv').forEach(el=>_obs.observe(el));

/* ----- Ano dinâmico no rodapé ----- */
document.querySelectorAll('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());

/* ----- Modal de pagamento (loja) ----- */
function openPay(nome,preco){
  const m=document.getElementById('payModal');
  if(!m)return;
  m.querySelector('[data-prod]').textContent=nome;
  m.querySelector('[data-preco]').textContent=preco?('Investimento: '+preco):'';
  const msg=encodeURIComponent('Olá Dra. Priscila! Tenho interesse no material "'+nome+'"'+(preco?(' ('+preco+')'):'')+'. Pode me enviar mais informações?');
  m.querySelector('[data-wa]').href='https://wa.me/'+WHATSAPP+'?text='+msg;
  m.querySelector('.pix-box')?.classList.remove('show');
  m.classList.add('open');
  document.body.style.overflow='hidden';
}
function closePay(){
  document.getElementById('payModal')?.classList.remove('open');
  document.body.style.overflow='';
}
function togglePix(){
  document.querySelector('#payModal .pix-box')?.classList.toggle('show');
}
function copyPix(btn){
  navigator.clipboard.writeText(PIX_KEY).then(()=>{
    const t=btn.textContent;btn.textContent='Copiado!';
    setTimeout(()=>btn.textContent=t,2200);
  });
}
document.addEventListener('click',e=>{if(e.target.id==='payModal')closePay();});
document.addEventListener('keydown',e=>{if(e.key==='Escape')closePay();});

/* ----- Newsletter (sem backend — abre WhatsApp) ----- */
function subscribe(ev){
  ev.preventDefault();
  const email=ev.target.querySelector('input').value;
  const msg=encodeURIComponent('Olá Dra. Priscila! Quero receber seus conteúdos por e-mail: '+email);
  window.open('https://wa.me/'+WHATSAPP+'?text='+msg,'_blank');
  ev.target.reset();
  alert('Obrigada! Em breve entraremos em contato. 🤍');
}
