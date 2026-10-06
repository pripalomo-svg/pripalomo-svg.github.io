/* Priscila Palomo — scripts compartilhados */

/* ----- Navegação ----- */
(function(){
  const header=document.querySelector('.site-header');
  const main=document.querySelector('.nav-main');
  const toggle=document.querySelector('.nav-toggle');
  const overlay=document.querySelector('.nav-overlay');
  const mq=window.matchMedia('(max-width: 1080px)');

  function setDrawer(open){
    if(!main)return;
    main.classList.toggle('open',open);
    overlay?.classList.toggle('show',open);
    toggle?.setAttribute('aria-expanded',String(open));
    document.body.classList.toggle('nav-open',open);
    if(!open)closeMenus();
  }
  function closeMenus(except){
    document.querySelectorAll('.nav-link[aria-expanded="true"]').forEach(b=>{if(b!==except)b.setAttribute('aria-expanded','false');});
  }
  toggle?.addEventListener('click',()=>setDrawer(!main.classList.contains('open')));
  overlay?.addEventListener('click',()=>setDrawer(false));

  document.querySelectorAll('.has-menu > .nav-link').forEach(btn=>{
    btn.addEventListener('click',e=>{
      e.preventDefault();
      const open=btn.getAttribute('aria-expanded')==='true';
      closeMenus(btn);
      btn.setAttribute('aria-expanded',String(!open));
    });
  });
  document.addEventListener('click',e=>{
    if(!e.target.closest('.has-menu'))closeMenus();
  });
  document.addEventListener('keydown',e=>{
    if(e.key==='Escape'){closeMenus();setDrawer(false);closePay();closeVideo();}
  });
  document.querySelectorAll('.nav-menu a, .nav-list > li > a').forEach(a=>a.addEventListener('click',()=>setDrawer(false)));
  mq.addEventListener?.('change',()=>setDrawer(false));

  if(header){
    const onScroll=()=>header.classList.toggle('scrolled',window.scrollY>8);
    onScroll();window.addEventListener('scroll',onScroll,{passive:true});
  }

  // Legado (Desk, Extrato): <nav> simples com .nav-links
  window.setMenu=function(open){
    const links=document.querySelector('.nav-links');
    if(!links)return;
    links.classList.toggle('open',open);
  };
  window.toggleMenu=function(){
    setMenu(!document.querySelector('.nav-links')?.classList.contains('open'));
  };
})();

/* ----- Revelar ao rolar ----- */
if('IntersectionObserver' in window){
  const _obs=new IntersectionObserver((entries)=>{
    entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('vis');_obs.unobserve(e.target);}});
  },{threshold:0,rootMargin:'0px 0px -5% 0px'});
  document.querySelectorAll('.rv').forEach(el=>_obs.observe(el));
  setTimeout(()=>document.querySelectorAll('.rv:not(.vis)').forEach(el=>el.classList.add('vis')),2500);
}else{
  document.querySelectorAll('.rv').forEach(el=>el.classList.add('vis'));
}

/* ----- Ano no rodapé ----- */
document.querySelectorAll('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());

/* ----- Toast ----- */
function toast(msg,ms){
  let t=document.querySelector('.toast');
  if(!t){t=document.createElement('div');t.className='toast';t.setAttribute('role','status');document.body.appendChild(t);}
  t.textContent=msg;
  requestAnimationFrame(()=>t.classList.add('show'));
  clearTimeout(t._h);t._h=setTimeout(()=>t.classList.remove('show'),ms||3200);
}

/* ----- Vídeo institucional (hero) ----- */
function openVideo(){
  const m=document.getElementById('videoModal');
  if(!m)return;
  const v=m.querySelector('video');
  document.querySelector('.hero-video video')?.pause();
  m.classList.add('open');
  document.body.style.overflow='hidden';
  if(v){v.currentTime=0;v.muted=false;v.play().catch(()=>{});}
  m.querySelector('.video-modal-close')?.focus();
}
function closeVideo(){
  const m=document.getElementById('videoModal');
  if(!m||!m.classList.contains('open'))return;
  m.querySelector('video')?.pause();
  m.classList.remove('open');
  document.body.style.overflow='';
  document.querySelector('.hero-video video')?.play().catch(()=>{});
}
document.addEventListener('click',e=>{if(e.target.id==='videoModal')closeVideo();});

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
  const m=document.getElementById('payModal');
  if(!m||!m.classList.contains('open'))return;
  m.classList.remove('open');
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

/* ----- Newsletter NeuroNews (sem backend: abre o WhatsApp com o e-mail) ----- */
function subscribe(ev){
  ev.preventDefault();
  const email=ev.target.querySelector('input').value;
  const msg=encodeURIComponent('Olá Priscila! Quero assinar a NeuroNews. Meu e-mail: '+email);
  window.open('https://wa.me/'+WHATSAPP+'?text='+msg,'_blank');
  ev.target.reset();
  toast('Inscrição enviada. Você começa a receber a NeuroNews na próxima edição.');
}
