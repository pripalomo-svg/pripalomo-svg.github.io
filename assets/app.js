/* Dra. Priscila Palomo — scripts compartilhados */

// Menu mobile
function toggleMenu(){
  document.querySelector('.nav-links')?.classList.toggle('open');
}
document.querySelectorAll('.nav-links a').forEach(a=>{
  a.addEventListener('click',()=>document.querySelector('.nav-links')?.classList.remove('open'));
});

// Animação de revelar ao rolar
const _obs=new IntersectionObserver((entries)=>{
  entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('vis');_obs.unobserve(e.target);}});
},{threshold:.12});
document.querySelectorAll('.rv').forEach(el=>_obs.observe(el));

// Ano dinâmico no rodapé
document.querySelectorAll('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());

/* ----- Modal de pagamento (loja) ----- */
const WHATSAPP='5511950690537';
const PIX_KEY='11950690537';
// Link de checkout de cartão de crédito (ex.: Mercado Pago, PagSeguro, InfinitePay).
// Deixe vazio ('') para receber os pedidos com cartão pelo WhatsApp.
const CARTAO_LINK='';

function openPay(nome,preco){
  const m=document.getElementById('payModal');
  if(!m)return;
  m.querySelector('[data-prod]').textContent=nome;
  m.querySelector('[data-preco]').textContent=preco?('Investimento: '+preco):'';
  const msg=encodeURIComponent('Olá Dra. Priscila! Tenho interesse no material "'+nome+'"'+(preco?(' ('+preco+')'):'')+'. Pode me enviar mais informações?');
  m.querySelector('[data-wa]').href='https://wa.me/'+WHATSAPP+'?text='+msg;

  // Cartão de crédito: usa o link de checkout se configurado; senão, cai no WhatsApp.
  const card=m.querySelector('[data-card]');
  if(card){
    if(CARTAO_LINK){
      card.href=CARTAO_LINK;
    }else{
      const msgCartao=encodeURIComponent('Olá Dra. Priscila! Quero pagar o material "'+nome+'"'+(preco?(' ('+preco+')'):'')+' com cartão de crédito. Pode me enviar o link de pagamento?');
      card.href='https://wa.me/'+WHATSAPP+'?text='+msgCartao;
    }
    const sub=card.querySelector('[data-card-sub]');
    if(sub)sub.textContent=CARTAO_LINK?'Parcele em até 12x no checkout seguro':'Enviamos o link de pagamento pelo WhatsApp';
  }

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

// Newsletter (sem backend — abre WhatsApp)
function subscribe(ev){
  ev.preventDefault();
  const email=ev.target.querySelector('input').value;
  const msg=encodeURIComponent('Olá Dra. Priscila! Quero receber seus conteúdos por e-mail: '+email);
  window.open('https://wa.me/'+WHATSAPP+'?text='+msg,'_blank');
  ev.target.reset();
  alert('Obrigada! Em breve entraremos em contato.');
}
