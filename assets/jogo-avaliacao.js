/* =========================================================
   Jogo de autoavaliação — ansiedade e impulsividade
   Duas etapas: (1) tiro ao alvo  (2) blocos estilo Tetris
   ========================================================= */

const JOGO = {
  tela: 'intro',
  metrics: {
    alvos: {
      acertos: 0,
      erros: 0,          // clicou no alvo vermelho
      cliquesVazios: 0,
      alvosPerdidos: 0,  // alvo bom sumiu sem clique
      temposReacao: [],
      temposPorMetade: [[], []], // primeira vs segunda metade da sessão
      inicio: 0
    },
    blocos: {
      pecasColocadas: 0,
      linhas: 0,
      rotacoes: 0,
      movimentos: 0,
      quedasRapidas: 0,   // espaço ou botão soltar
      tentativasInvalidas: 0,
      temposColocacao: [],
      inicio: 0
    }
  }
};

/* ── Utilidades de tela ── */
function mostrarTela(id){
  document.querySelectorAll('.jogo-tela').forEach(el => el.classList.remove('ativa'));
  document.getElementById(id)?.classList.add('ativa');
  JOGO.tela = id.replace('tela-', '');
}

function iniciarJogo(){
  JOGO.metrics = {
    alvos: { acertos:0, erros:0, cliquesVazios:0, alvosPerdidos:0, temposReacao:[], temposPorMetade:[[],[]], inicio:0 },
    blocos: { pecasColocadas:0, linhas:0, rotacoes:0, movimentos:0, quedasRapidas:0, tentativasInvalidas:0, temposColocacao:[], inicio:0 }
  };
  mostrarTela('tela-alvos');
  iniciarAlvos();
}

/* =========================================================
   PARTE 1 — TIRO AO ALVO
   ========================================================= */
const ALVOS_DURACAO = 45; // segundos
let alvosTimer = null;
let alvosRestante = ALVOS_DURACAO;
let alvosSpawnTimer = null;
let alvosAtivos = new Map();
let alvoIdSeq = 0;
let alvosMetade = false;

function iniciarAlvos(){
  const area = document.getElementById('alvoArea');
  const feedback = document.getElementById('alvoFeedback');
  area.innerHTML = '';
  feedback.textContent = '';
  feedback.classList.remove('mostra');
  alvosRestante = ALVOS_DURACAO;
  alvosAtivos.clear();
  alvoIdSeq = 0;
  alvosMetade = false;
  JOGO.metrics.alvos.inicio = Date.now();
  atualizarBarraAlvos();

  area.onclick = (e) => {
    if(e.target === area){
      JOGO.metrics.alvos.cliquesVazios++;
      flashFeedback('—', area);
      atualizarBarraAlvos();
    }
  };

  alvosTimer = setInterval(() => {
    alvosRestante--;
    if(alvosRestante === Math.floor(ALVOS_DURACAO / 2)) alvosMetade = true;
    atualizarBarraAlvos();
    if(alvosRestante <= 0) encerrarAlvos();
  }, 1000);

  spawnAlvo();
  alvosSpawnTimer = setInterval(spawnAlvo, 900);
}

function spawnAlvo(){
  const area = document.getElementById('alvoArea');
  if(!area || alvosRestante <= 0) return;

  const pad = 40;
  const w = area.clientWidth, h = area.clientHeight;
  if(w < pad * 2 || h < pad * 2) return;

  const id = ++alvoIdSeq;
  const ruim = Math.random() < 0.28;
  const tamanho = ruim ? 52 : (44 + Math.random() * 20);
  const x = pad + Math.random() * (w - pad * 2);
  const y = pad + Math.random() * (h - pad * 2);
  const vida = ruim ? 2200 : (1400 + Math.random() * 800);

  const el = document.createElement('div');
  el.className = 'alvo ' + (ruim ? 'ruim' : 'bom');
  el.style.width = el.style.height = tamanho + 'px';
  el.style.left = x + 'px';
  el.style.top = y + 'px';
  el.textContent = ruim ? '✕' : '';
  el.dataset.id = id;
  el.dataset.ruim = ruim ? '1' : '0';
  el.dataset.spawn = Date.now();

  el.addEventListener('click', (e) => {
    e.stopPropagation();
    const spawn = +el.dataset.spawn;
    const rt = Date.now() - spawn;
    if(ruim){
      JOGO.metrics.alvos.erros++;
      flashFeedback('Ops!', area);
    }else{
      JOGO.metrics.alvos.acertos++;
      JOGO.metrics.alvos.temposReacao.push(rt);
      const metade = alvosMetade ? 1 : 0;
      JOGO.metrics.alvos.temposPorMetade[metade].push(rt);
      flashFeedback('✓', area);
    }
    removerAlvo(id, true);
    atualizarBarraAlvos();
  });

  area.appendChild(el);
  alvosAtivos.set(id, { el, timeout: setTimeout(() => removerAlvo(id, false), vida) });
}

function removerAlvo(id, clicado){
  const item = alvosAtivos.get(id);
  if(!item) return;
  clearTimeout(item.timeout);
  if(!clicado && item.el.dataset.ruim === '0'){
    JOGO.metrics.alvos.alvosPerdidos++;
    atualizarBarraAlvos();
  }
  item.el.classList.add('sumindo');
  setTimeout(() => item.el.remove(), 200);
  alvosAtivos.delete(id);
}

function flashFeedback(txt, area){
  const fb = document.getElementById('alvoFeedback');
  fb.textContent = txt;
  fb.classList.add('mostra');
  setTimeout(() => fb.classList.remove('mostra'), 280);
}

function atualizarBarraAlvos(){
  document.getElementById('alvosTimer').textContent = alvosRestante + 's';
  document.getElementById('alvosAcertos').textContent = JOGO.metrics.alvos.acertos;
  document.getElementById('alvosErros').textContent = JOGO.metrics.alvos.erros + JOGO.metrics.alvos.cliquesVazios;
}

function encerrarAlvos(){
  clearInterval(alvosTimer);
  clearInterval(alvosSpawnTimer);
  alvosAtivos.forEach((v, id) => removerAlvo(id, false));
  setTimeout(() => {
    mostrarTela('tela-blocos');
    iniciarBlocos();
  }, 800);
}

/* =========================================================
   PARTE 2 — BLOCOS (Tetris simplificado)
   ========================================================= */
const COLS = 10, ROWS = 16;
const CORES = ['#E27A2E','#0E4A57','#5A9E6F','#9B59B6','#3498DB','#C0641C','#2C3E50'];
const PECAS = {
  I: [[1,1,1,1]],
  O: [[1,1],[1,1]],
  T: [[0,1,0],[1,1,1]],
  L: [[1,0],[1,0],[1,1]],
  S: [[0,1,1],[1,1,0]],
  Z: [[1,1,0],[0,1,1]],
  J: [[0,1],[0,1],[1,1]]
};
const NOMES_PECAS = Object.keys(PECAS);

let blocosGrid = [];
let pecaAtual = null;
let pecaX = 0, pecaY = 0;
let pecaCor = 0;
let blocosLoop = null;
let blocosTimer = null;
let blocosRestante = 90;
let pecaInicioTempo = 0;
let blocosVelocidade = 650;
let blocosFim = false;

function criarGrid(){
  return Array.from({length: ROWS}, () => Array(COLS).fill(0));
}

function rotacionar(mat){
  const rows = mat.length, cols = mat[0].length;
  const out = Array.from({length: cols}, () => Array(rows).fill(0));
  for(let r = 0; r < rows; r++)
    for(let c = 0; c < cols; c++)
      out[c][rows - 1 - r] = mat[r][c];
  return out;
}

function novaPeca(){
  const nome = NOMES_PECAS[Math.floor(Math.random() * NOMES_PECAS.length)];
  const forma = PECAS[nome].map(row => [...row]);
  pecaCor = 1 + Math.floor(Math.random() * CORES.length);
  pecaAtual = forma;
  pecaX = Math.floor((COLS - forma[0].length) / 2);
  pecaY = 0;
  pecaInicioTempo = Date.now();
  if(colide(pecaAtual, pecaX, pecaY)){
    blocosFim = true;
    encerrarBlocos();
    return false;
  }
  renderizarProxima();
  return true;
}

function colide(forma, px, py){
  for(let r = 0; r < forma.length; r++){
    for(let c = 0; c < forma[r].length; c++){
      if(!forma[r][c]) continue;
      const nx = px + c, ny = py + r;
      if(nx < 0 || nx >= COLS || ny >= ROWS) return true;
      if(ny >= 0 && blocosGrid[ny][nx]) return true;
    }
  }
  return false;
}

function fixarPeca(){
  const tempo = Date.now() - pecaInicioTempo;
  JOGO.metrics.blocos.temposColocacao.push(tempo);
  JOGO.metrics.blocos.pecasColocadas++;

  for(let r = 0; r < pecaAtual.length; r++){
    for(let c = 0; c < pecaAtual[r].length; c++){
      if(!pecaAtual[r][c]) continue;
      const ny = pecaY + r, nx = pecaX + c;
      if(ny >= 0) blocosGrid[ny][nx] = pecaCor;
    }
  }
  limparLinhas();
  novaPeca();
  renderizarTabuleiro();
  atualizarBarraBlocos();
}

function limparLinhas(){
  let removidas = 0;
  for(let r = ROWS - 1; r >= 0; r--){
    if(blocosGrid[r].every(c => c > 0)){
      blocosGrid.splice(r, 1);
      blocosGrid.unshift(Array(COLS).fill(0));
      removidas++;
      r++;
    }
  }
  if(removidas){
    JOGO.metrics.blocos.linhas += removidas;
    blocosVelocidade = Math.max(320, blocosVelocidade - removidas * 25);
    reiniciarQueda();
  }
}

function moverPeca(dx, dy){
  if(!pecaAtual || blocosFim) return false;
  if(!colide(pecaAtual, pecaX + dx, pecaY + dy)){
    pecaX += dx; pecaY += dy;
    if(dx !== 0) JOGO.metrics.blocos.movimentos++;
    renderizarTabuleiro();
    return true;
  }
  if(dy > 0){
    fixarPeca();
    return false;
  }
  if(dy === 0 && dx !== 0) JOGO.metrics.blocos.tentativasInvalidas++;
  return false;
}

function rotacionarPeca(){
  if(!pecaAtual || blocosFim) return;
  const rot = rotacionar(pecaAtual);
  if(!colide(rot, pecaX, pecaY)){
    pecaAtual = rot;
    JOGO.metrics.blocos.rotacoes++;
    renderizarTabuleiro();
  }else{
    JOGO.metrics.blocos.tentativasInvalidas++;
  }
}

function quedaRapida(){
  if(!pecaAtual || blocosFim) return;
  JOGO.metrics.blocos.quedasRapidas++;
  while(moverPeca(0, 1)){}
}

function reiniciarQueda(){
  clearInterval(blocosLoop);
  blocosLoop = setInterval(() => moverPeca(0, 1), blocosVelocidade);
}

function renderizarTabuleiro(){
  const tab = document.getElementById('blocosTabuleiro');
  if(!tab) return;
  tab.innerHTML = '';
  tab.style.gridTemplateColumns = `repeat(${COLS}, 26px)`;

  const overlay = Array.from({length: ROWS}, (_, r) =>
    Array.from({length: COLS}, (_, c) => blocosGrid[r][c])
  );

  if(pecaAtual){
    for(let r = 0; r < pecaAtual.length; r++){
      for(let c = 0; c < pecaAtual[r].length; c++){
        if(!pecaAtual[r][c]) continue;
        const ny = pecaY + r, nx = pecaX + c;
        if(ny >= 0 && ny < ROWS && nx >= 0 && nx < COLS)
          overlay[ny][nx] = pecaAtual[r][c] ? pecaCor : overlay[ny][nx];
      }
    }
  }

  for(let r = 0; r < ROWS; r++){
    for(let c = 0; c < COLS; c++){
      const cell = document.createElement('div');
      cell.className = 'blocos-celula';
      if(overlay[r][c]){
        cell.classList.add('preenchida');
        const fixa = blocosGrid[r][c];
        const ativa = pecaAtual && !fixa && overlay[r][c] === pecaCor;
        if(ativa) cell.classList.add('ativa');
        cell.style.background = CORES[(overlay[r][c] - 1) % CORES.length];
      }
      tab.appendChild(cell);
    }
  }
}

function renderizarProxima(){
  const prox = document.getElementById('blocosProxima');
  if(!prox || !pecaAtual) return;
  prox.innerHTML = '';
  const rows = pecaAtual.length, cols = pecaAtual[0].length;
  prox.style.gridTemplateColumns = `repeat(${cols}, 18px)`;
  for(let r = 0; r < rows; r++){
    for(let c = 0; c < cols; c++){
      const cell = document.createElement('div');
      cell.className = 'blocos-celula';
      if(pecaAtual[r][c]){
        cell.classList.add('preenchida');
        cell.style.background = CORES[(pecaCor - 1) % CORES.length];
      }
      prox.appendChild(cell);
    }
  }
}

function iniciarBlocos(){
  blocosGrid = criarGrid();
  blocosRestante = 90;
  blocosVelocidade = 650;
  blocosFim = false;
  JOGO.metrics.blocos.inicio = Date.now();
  atualizarBarraBlocos();

  novaPeca();
  renderizarTabuleiro();
  reiniciarQueda();

  blocosTimer = setInterval(() => {
    blocosRestante--;
    atualizarBarraBlocos();
    if(blocosRestante <= 0) encerrarBlocos();
  }, 1000);

  const tab = document.getElementById('blocosTabuleiro');
  tab.onmousemove = (e) => {
    if(!pecaAtual || blocosFim) return;
    const rect = tab.getBoundingClientRect();
    const relX = e.clientX - rect.left;
    const col = Math.floor(relX / 26);
    const alvo = Math.max(0, Math.min(COLS - pecaAtual[0].length, col - Math.floor(pecaAtual[0].length / 2)));
    if(alvo !== pecaX){
      const dir = alvo > pecaX ? 1 : -1;
      moverPeca(dir, 0);
    }
  };
  tab.onclick = () => rotacionarPeca();

  document.onkeydown = (e) => {
    if(JOGO.tela !== 'blocos' || blocosFim) return;
    if(e.key === 'ArrowLeft'){ e.preventDefault(); moverPeca(-1, 0); }
    if(e.key === 'ArrowRight'){ e.preventDefault(); moverPeca(1, 0); }
    if(e.key === 'ArrowDown'){ e.preventDefault(); moverPeca(0, 1); }
    if(e.key === 'ArrowUp' || e.key === ' '){ e.preventDefault(); rotacionarPeca(); }
    if(e.key === 'Enter'){ e.preventDefault(); quedaRapida(); }
  };
}

function atualizarBarraBlocos(){
  document.getElementById('blocosTimer').textContent = blocosRestante + 's';
  document.getElementById('blocosLinhas').textContent = JOGO.metrics.blocos.linhas;
  document.getElementById('blocosPecas').textContent = JOGO.metrics.blocos.pecasColocadas;
}

function encerrarBlocos(){
  if(blocosFim && JOGO.tela === 'resultados') return;
  blocosFim = true;
  clearInterval(blocosLoop);
  clearInterval(blocosTimer);
  document.onkeydown = null;
  setTimeout(() => {
    mostrarTela('tela-resultados');
    exibirResultados();
  }, 600);
}

/* =========================================================
   PONTUAÇÃO E INTERPRETAÇÃO
   ========================================================= */
function media(arr){ return arr.length ? arr.reduce((a,b)=>a+b,0)/arr.length : 0; }
function desvio(arr){
  if(arr.length < 2) return 0;
  const m = media(arr);
  return Math.sqrt(arr.reduce((s,v)=>s+(v-m)**2,0)/(arr.length-1));
}

function calcularPontuacao(){
  const a = JOGO.metrics.alvos;
  const b = JOGO.metrics.blocos;
  const totalCliques = a.acertos + a.erros + a.cliquesVazios;
  const rtMedia = media(a.temposReacao);
  const rtDesvio = desvio(a.temposReacao);
  const cv = rtMedia > 0 ? rtDesvio / rtMedia : 0;

  const rt1 = media(a.temposPorMetade[0]);
  const rt2 = media(a.temposPorMetade[1]);
  const pioraTempo = rt1 > 0 ? Math.max(0, (rt2 - rt1) / rt1) : 0;

  const impulsivosRapidos = a.temposReacao.filter(t => t < 250).length;
  const taxaErro = totalCliques > 0 ? (a.erros + a.cliquesVazios) / totalCliques : 0;
  const taxaAcerto = (a.acertos + a.alvosPerdidos) > 0 ? a.acertos / (a.acertos + a.alvosPerdidos + a.erros) : 0;

  const tempoMedioBloco = media(b.temposColocacao);
  const pressaBlocos = b.pecasColocadas > 0 ? b.quedasRapidas / b.pecasColocadas : 0;

  /* Impulsividade 0–100 */
  let imp = 0;
  imp += Math.min(35, taxaErro * 100 * 0.35);
  imp += Math.min(25, (a.erros / Math.max(1, totalCliques)) * 100 * 0.8);
  imp += Math.min(20, (impulsivosRapidos / Math.max(1, a.acertos)) * 40);
  imp += Math.min(10, pressaBlocos * 30);
  imp += Math.min(10, (a.cliquesVazios / Math.max(1, totalCliques)) * 50);
  imp = Math.round(Math.min(100, Math.max(0, imp)));

  /* Ansiedade 0–100 */
  let ans = 0;
  ans += Math.min(30, cv * 80);
  ans += Math.min(25, pioraTempo * 60);
  ans += Math.min(20, (a.alvosPerdidos / Math.max(1, a.acertos + a.alvosPerdidos)) * 50);
  ans += Math.min(15, (b.tentativasInvalidas / Math.max(1, b.movimentos + b.rotacoes + 1)) * 40);
  if(tempoMedioBloco > 4000) ans += Math.min(10, (tempoMedioBloco - 4000) / 200);
  ans = Math.round(Math.min(100, Math.max(0, ans)));

  return {
    impulsividade: imp,
    ansiedade: ans,
    detalhes: {
      acertos: a.acertos,
      errosAlvo: a.erros,
      cliquesVazios: a.cliquesVazios,
      alvosPerdidos: a.alvosPerdidos,
      rtMedia: Math.round(rtMedia),
      rtDesvio: Math.round(rtDesvio),
      linhas: b.linhas,
      pecas: b.pecasColocadas,
      quedasRapidas: b.quedasRapidas,
      tempoMedioBloco: Math.round(tempoMedioBloco)
    }
  };
}

function nivelPontuacao(n){
  if(n <= 33) return { texto: 'Baixo', cls: 'baixo' };
  if(n <= 66) return { texto: 'Moderado', cls: 'moderado' };
  return { texto: 'Elevado', cls: 'elevado' };
}

function textoImpulsividade(n){
  if(n <= 33) return 'Seus cliques e decisões pareceram bastante controlados. Você equilibrou velocidade e precisão de forma consistente.';
  if(n <= 66) return 'Houve alguns momentos de pressa — cliques rápidos ou quedas antecipadas dos blocos. Isso é comum sob tempo limitado e vale observar no dia a dia.';
  return 'Os dados sugerem tendência a agir antes de avaliar: muitos cliques impulsivos, erros em alvos vermelhos ou quedas rápidas dos blocos. Pode ser útil praticar pausas curtas antes de decidir.';
}

function textoAnsiedade(n){
  if(n <= 33) return 'Seu ritmo foi estável ao longo das duas etapas. Pouca hesitação e desempenho relativamente uniforme — sinal de calma sob pressão.';
  if(n <= 66) return 'Notamos alguma variabilidade no tempo de reação e pequenas quedas de desempenho com o passar do tempo. Isso pode indicar tensão leve sob exigência.';
  return 'Houve bastante oscilação no tempo de resposta, alvos perdidos por hesitação ou piora ao longo da sessão. Isso pode refletir ansiedade ou autocobrança em situações de pressão.';
}

function exibirResultados(){
  const r = calcularPontuacao();
  const ni = nivelPontuacao(r.impulsividade);
  const na = nivelPontuacao(r.ansiedade);

  document.getElementById('notaImpulsividade').textContent = r.impulsividade;
  document.getElementById('nivelImpulsividade').textContent = ni.texto;
  document.getElementById('nivelImpulsividade').className = 'nivel ' + ni.cls;
  document.getElementById('textoImpulsividade').textContent = textoImpulsividade(r.impulsividade);

  document.getElementById('notaAnsiedade').textContent = r.ansiedade;
  document.getElementById('nivelAnsiedade').textContent = na.texto;
  document.getElementById('nivelAnsiedade').className = 'nivel ' + na.cls;
  document.getElementById('textoAnsiedade').textContent = textoAnsiedade(r.ansiedade);

  const d = r.detalhes;
  document.getElementById('tabelaDetalhes').innerHTML = `
    <tr><th>Alvos acertados</th><td>${d.acertos}</td></tr>
    <tr><th>Erros (alvo vermelho)</th><td>${d.errosAlvo}</td></tr>
    <tr><th>Cliques no vazio</th><td>${d.cliquesVazios}</td></tr>
    <tr><th>Alvos perdidos</th><td>${d.alvosPerdidos}</td></tr>
    <tr><th>Tempo médio de reação</th><td>${d.rtMedia} ms</td></tr>
    <tr><th>Variação do tempo de reação</th><td>${d.rtDesvio} ms</td></tr>
    <tr><th>Linhas completas (blocos)</th><td>${d.linhas}</td></tr>
    <tr><th>Peças colocadas</th><td>${d.pecas}</td></tr>
    <tr><th>Quedas rápidas</th><td>${d.quedasRapidas}</td></tr>
    <tr><th>Tempo médio por peça</th><td>${d.tempoMedioBloco} ms</td></tr>
  `;
}

function compartilharWhatsApp(){
  const r = calcularPontuacao();
  const ni = nivelPontuacao(r.impulsividade);
  const na = nivelPontuacao(r.ansiedade);
  const msg = encodeURIComponent(
    `Olá Dra. Priscila! Fiz o jogo de autoavaliação no seu site.\n\n` +
    `Impulsividade: ${r.impulsividade}/100 (${ni.texto})\n` +
    `Ansiedade: ${r.ansiedade}/100 (${na.texto})\n\n` +
    `Gostaria de conversar sobre esses resultados.`
  );
  window.open('https://wa.me/5511950690537?text=' + msg, '_blank');
}

function reiniciarTudo(){
  document.onkeydown = null;
  clearInterval(alvosTimer);
  clearInterval(alvosSpawnTimer);
  clearInterval(blocosLoop);
  clearInterval(blocosTimer);
  mostrarTela('tela-intro');
}
