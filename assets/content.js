/* =========================================================
   Dra. Priscila Palomo — Carregador de conteúdo
   Lê arquivos Markdown (.md) das pastas "posts/" e "produtos/"
   e monta o blog e a loja automaticamente.

   >>> Você NÃO precisa editar este arquivo. <<<
   Para escrever um post ou cadastrar um produto, basta criar
   um arquivo .md nas pastas correspondentes. Veja o COMO-USAR.md.
   ========================================================= */

const REPO = {
  owner: 'pripalomo-svg',
  name:  'pripalomo-svg.github.io',
  branch:'main'
};

const MESES = ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez'];

/* Lista os arquivos .md de uma pasta usando a API pública do GitHub.
   O resultado fica em cache por alguns minutos para evitar chamadas repetidas. */
async function listarMarkdown(pasta){
  const chaveCache = 'lista:'+pasta;
  try{
    const cru = sessionStorage.getItem(chaveCache);
    if(cru){
      const c = JSON.parse(cru);
      if(Date.now() - c.t < 5*60*1000) return c.itens;
    }
  }catch(e){}

  const url = `https://api.github.com/repos/${REPO.owner}/${REPO.name}/contents/${pasta}?ref=${REPO.branch}`;
  const res = await fetch(url, { headers: { 'Accept':'application/vnd.github+json' } });
  if(!res.ok) throw new Error('Falha ao listar '+pasta+' ('+res.status+')');
  const arr = await res.json();
  const itens = arr
    .filter(f => f.type==='file'
              && f.name.toLowerCase().endsWith('.md')
              && f.name.toLowerCase() !== 'leia-me.md'
              && f.name.toLowerCase() !== 'readme.md')
    .map(f => ({ slug: f.name.replace(/\.md$/i,''), name: f.name, path: pasta+'/'+f.name }));

  try{ sessionStorage.setItem(chaveCache, JSON.stringify({ t:Date.now(), itens })); }catch(e){}
  return itens;
}

/* Lê um arquivo de texto (relativo ao site, funciona local e publicado) */
async function lerArquivo(caminho){
  const sep = caminho.includes('?') ? '&' : '?';
  const res = await fetch(caminho + sep + 'v=' + Date.now());
  if(!res.ok) throw new Error('Falha ao ler '+caminho);
  return res.text();
}

/* Separa o "cabeçalho" (entre ---) do corpo do texto em Markdown */
function lerFrontMatter(texto){
  const m = texto.match(/^\uFEFF?---\s*\r?\n([\s\S]*?)\r?\n---\s*\r?\n?([\s\S]*)$/);
  const meta = {};
  let corpo = texto;
  if(m){
    corpo = m[2];
    m[1].split(/\r?\n/).forEach(linha => {
      const i = linha.indexOf(':');
      if(i > -1){
        const chave = linha.slice(0,i).trim();
        let valor = linha.slice(i+1).trim().replace(/^["']|["']$/g,'');
        if(chave) meta[chave] = valor;
      }
    });
  }
  return { meta, corpo: corpo.trim() };
}

function formatarData(str){
  if(!str) return '';
  const d = new Date(str + (str.length<=10 ? 'T12:00:00' : ''));
  if(isNaN(d)) return str;
  return `${d.getDate()} ${MESES[d.getMonth()]} ${d.getFullYear()}`;
}

function tempoLeitura(corpo){
  const palavras = corpo.replace(/[#>*_`\-\[\]()!]/g,' ').split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(palavras/200));
}

function resumoDe(corpo, max=150){
  const txt = corpo
    .replace(/^#.*$/gm,'')
    .replace(/[#>*_`]/g,'')
    .replace(/\[([^\]]+)\]\([^)]+\)/g,'$1')
    .replace(/\s+/g,' ')
    .trim();
  return txt.length > max ? txt.slice(0,max).trim()+'…' : txt;
}

function escapeHtml(s){
  return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function corValida(c){
  return ['','c-la','c-ou','c-vd'].includes(c) ? c : '';
}

/* Converte Markdown em HTML (usa marked se disponível, senão um fallback simples) */
function md2html(md){
  if(window.marked){
    try{ return window.marked.parse(md); }catch(e){}
  }
  // Fallback bem básico
  return md.split(/\n{2,}/).map(p=>{
    if(/^#\s/.test(p)) return '<h2>'+escapeHtml(p.replace(/^#\s/,''))+'</h2>';
    if(/^##\s/.test(p)) return '<h3>'+escapeHtml(p.replace(/^##\s/,''))+'</h3>';
    return '<p>'+escapeHtml(p)+'</p>';
  }).join('');
}
