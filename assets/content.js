/* =========================================================
   Priscila Palomo — Carregador de conteúdo
   Lê os arquivos Markdown das pastas "posts/" e "produtos/"
   usando um índice estático (index.json) — sem depender de
   API externa.

   >>> Você NÃO precisa editar este arquivo. <<<
   Para publicar um post ou produto, crie o arquivo .md
   na pasta certa E adicione o slug no index.json da pasta.
   Veja o COMO-USAR.md para o passo a passo.
   ========================================================= */

const MESES = ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez'];

/* Lista os arquivos .md de uma pasta usando o index.json local.
   Formato do index.json: ["slug1","slug2",...] */
async function listarMarkdown(pasta){
  const res = await fetch(pasta + '/index.json?v=' + Date.now());
  if(!res.ok) throw new Error('Falha ao ler índice de ' + pasta + ' (' + res.status + ')');
  const slugs = await res.json();
  return slugs.map(slug => ({
    slug,
    name: slug + '.md',
    path: pasta + '/' + slug + '.md'
  }));
}

/* Lê um arquivo de texto relativo ao site */
async function lerArquivo(caminho){
  const sep = caminho.includes('?') ? '&' : '?';
  const res = await fetch(caminho + sep + 'v=' + Date.now());
  if(!res.ok) throw new Error('Falha ao ler ' + caminho);
  return res.text();
}

/* Separa o cabeçalho YAML (entre ---) do corpo do texto */
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
  const d = new Date(str + (str.length <= 10 ? 'T12:00:00' : ''));
  if(isNaN(d)) return str;
  return `${d.getDate()} ${MESES[d.getMonth()]} ${d.getFullYear()}`;
}

function tempoLeitura(corpo){
  const palavras = corpo.replace(/[#>*_`\-\[\]()!]/g,' ').split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(palavras / 200));
}

function resumoDe(corpo, max=150){
  const txt = corpo
    .replace(/^#.*$/gm,'')
    .replace(/[#>*_`]/g,'')
    .replace(/\[([^\]]+)\]\([^)]+\)/g,'$1')
    .replace(/\s+/g,' ')
    .trim();
  return txt.length > max ? txt.slice(0, max).trim() + '…' : txt;
}

function escapeHtml(s){
  return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function corValida(c){
  return ['','c-la','c-ou','c-vd'].includes(c) ? c : '';
}

/* Converte Markdown em HTML */
function md2html(md){
  if(window.marked){
    try{ return window.marked.parse(md); }catch(e){}
  }
  return md.split(/\n{2,}/).map(p => {
    if(/^##\s/.test(p))  return '<h2>' + escapeHtml(p.replace(/^##\s/,''))  + '</h2>';
    if(/^###\s/.test(p)) return '<h3>' + escapeHtml(p.replace(/^###\s/,'')) + '</h3>';
    if(/^#\s/.test(p))   return '<h2>' + escapeHtml(p.replace(/^#\s/,''))   + '</h2>';
    return '<p>' + escapeHtml(p) + '</p>';
  }).join('');
}
