/* Terap-ia OS — login, pacientes, agenda (Google + WhatsApp), mensalidade */
(function () {
  const PIX = '11950690537';
  const WA_DONA = '5511950690537';
  /* Cole aqui o link recorrente do PagBank/PagSeguro (R$ 100/mês, cartão). */
  const PAGSEGURO_LINK = '';
  const PRECO = 'R$ 100 / mês';

  const $ = (id) => document.getElementById(id);
  const app = $('app');

  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} },
    del(k) { try { localStorage.removeItem(k); } catch (e) {} }
  };

  function loadJSON(k, fb) {
    try {
      const raw = store.get(k);
      if (!raw) return fb;
      const v = JSON.parse(raw);
      return v == null ? fb : v;
    } catch (e) { return fb; }
  }

  function users() { return loadJSON('tpos_users', []); }
  function saveUsers(list) { store.set('tpos_users', JSON.stringify(list)); }

  function session() { return store.get('tpos_session') || ''; }
  function setSession(login) {
    if (login) store.set('tpos_session', login);
    else store.del('tpos_session');
  }

  function dbKey(login) { return 'tpos_db_' + login.toLowerCase(); }
  function db(login) {
    const d = loadJSON(dbKey(login), null);
    return d && typeof d === 'object' ? d : { patients: [], appointments: [] };
  }
  function saveDb(login, data) { store.set(dbKey(login), JSON.stringify(data)); }

  function esc(s) {
    s = s == null ? '' : String(s);
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  async function hashPass(login, pass) {
    const enc = new TextEncoder();
    const key = await crypto.subtle.importKey('raw', enc.encode(pass), 'PBKDF2', false, ['deriveBits']);
    const bits = await crypto.subtle.deriveBits(
      { name: 'PBKDF2', salt: enc.encode('terapia-os:' + login.toLowerCase()), iterations: 120000, hash: 'SHA-256' },
      key, 256
    );
    return [...new Uint8Array(bits)].map((b) => b.toString(16).padStart(2, '0')).join('');
  }

  function digits(s) { return String(s || '').replace(/\D/g, ''); }

  function waLink(num, text) {
    let n = digits(num);
    if (n.length === 10 || n.length === 11) n = '55' + n;
    return 'https://wa.me/' + n + '?text=' + encodeURIComponent(text);
  }

  function gcalLink(ev) {
    const start = ev.date.replace(/-/g, '') + 'T' + ev.time.replace(':', '') + '00';
    const [hh, mm] = ev.time.split(':').map(Number);
    const endH = String((hh + 1) % 24).padStart(2, '0');
    const end = ev.date.replace(/-/g, '') + 'T' + endH + String(mm).padStart(2, '0') + '00';
    const q = new URLSearchParams({
      action: 'TEMPLATE',
      text: 'Consulta · ' + ev.who,
      dates: start + '/' + end,
      details: ev.note || 'Consulta — Terap-ia OS',
      location: ev.place || 'Consultório / online'
    });
    return 'https://calendar.google.com/calendar/render?' + q.toString();
  }

  const S = { view: 'login', flash: '', err: '', pay: '', draft: {} };

  function currentUser() {
    const login = session();
    if (!login) return null;
    return users().find((u) => u.login === login) || null;
  }

  function go(view) { S.view = view; S.err = ''; S.flash = ''; render(); }

  function render() {
    const u = currentUser();
    if (u && S.view === 'login') S.view = 'desk';
    if (!u && (S.view === 'desk' || S.view === 'pacientes' || S.view === 'agenda')) S.view = 'login';

    if (S.view === 'login') app.innerHTML = viewLogin();
    else if (S.view === 'assinar') app.innerHTML = viewAssinar();
    else if (S.view === 'pacientes') app.innerHTML = viewPacientes(u);
    else if (S.view === 'agenda') app.innerHTML = viewAgenda(u);
    else app.innerHTML = viewDesk(u);
    bind();
  }

  function flashBox() {
    if (S.err) return '<div class="err">' + esc(S.err) + '</div>';
    if (S.flash) return '<div class="ok">' + esc(S.flash) + '</div>';
    return '';
  }

  function viewLogin() {
    return `<div class="lock">
      <div class="lock-card">
        <div class="kicker">Terap-ia OS</div>
        <h1>Entrar</h1>
        <p class="lead">Banco de dados da sua clínica. Cada login enxerga só os próprios pacientes.</p>
        <form id="f-login" novalidate>
          <label class="fl" for="login">Usuário</label>
          <input class="inp" id="login" name="login" autocomplete="username" required>
          <label class="fl" for="senha">Senha</label>
          <input class="inp" id="senha" name="senha" type="password" autocomplete="current-password" required>
          ${flashBox()}
          <div class="btnrow">
            <button class="btn full" type="submit">Entrar</button>
            <button class="btn orange full" type="button" id="btn-assinar">Assinar · ${PRECO}</button>
          </div>
        </form>
        <p class="hint">Pix 11 95069-0537 · PagSeguro ou cartão. Até 1000 clínicas, cada uma com o seu banco.</p>
      </div>
    </div>`;
  }

  function viewAssinar() {
    const pix = S.pay === 'pix';
    return `<div class="lock">
      <div class="lock-card">
        <div class="kicker">Mensalidade</div>
        <h1>${PRECO}</h1>
        <p class="lead">Pague e crie o seu login. O banco fica separado por senha.</p>
        <div class="pay-grid">
          <button type="button" class="pay-opt" id="pay-pix">
            <strong>Pix</strong>
            <small>Chave ${PIX} · PagSeguro / transferência</small>
          </button>
          <button type="button" class="pay-opt" id="pay-card">
            <strong>PagSeguro ou cartão</strong>
            <small>Mensalidade no cartão, ambiente seguro do PagBank</small>
          </button>
        </div>
        ${pix ? `<div class="pix"><span>${PIX}</span><button type="button" class="btn ghost" id="copy-pix">Copiar</button></div>` : ''}
        <form id="f-criar">
          <label class="fl" for="nlogin">Crie o usuário</label>
          <input class="inp" id="nlogin" required minlength="3" autocomplete="username" placeholder="ex.: clinica.silva">
          <label class="fl" for="nsenha">Crie a senha</label>
          <input class="inp" id="nsenha" type="password" required minlength="6" autocomplete="new-password">
          ${flashBox()}
          <div class="btnrow">
            <button class="btn orange full" type="submit">Já paguei · criar acesso</button>
            <button class="btn ghost full" type="button" id="btn-voltar">Voltar ao login</button>
          </div>
        </form>
        <div class="cloud">
          <b>Nuvem recomendada para 1000 clínicas:</b>
          Supabase (login + banco isolado por usuário) e Cloudflare R2 (arquivos baratos, muito espaço, sem taxa de saída).
          Cabe terabytes. A receita de R$ 100/mês por clínica cobre a nuvem com folga.
        </div>
      </div>
    </div>`;
  }

  function chrome(u, body) {
    return `<div class="os">
      <div class="bar">
        <strong>Terap-ia OS</strong>
        <span class="who">${esc(u.login)}</span>
        <button class="btn ghost" type="button" id="btn-sair" style="padding:8px 12px">Sair</button>
      </div>
      <div class="desk">${body}</div>
    </div>`;
  }

  function viewDesk(u) {
    const data = db(u.login);
    return chrome(u, `
      <h2>Sua clínica</h2>
      <p class="sub">${data.patients.length} paciente(s) · ${data.appointments.length} consulta(s)</p>
      <div class="tiles">
        <button type="button" class="tile" id="go-pac"><b>Pacientes</b><span>Cadastro e telefone</span></button>
        <button type="button" class="tile" id="go-age"><b>Agenda</b><span>Google Agenda + WhatsApp</span></button>
      </div>`);
  }

  function viewPacientes(u) {
    const data = db(u.login);
    const rows = data.patients.length
      ? data.patients.map((p, i) => `<div class="rowitem">
          <div><strong>${esc(p.nome)}</strong><small>${esc(p.fone)} · ${esc(p.nota || 'sem nota')}</small></div>
          <button type="button" class="btn ghost" data-del-p="${i}">Apagar</button>
        </div>`).join('')
      : '<p class="hint">Nenhum paciente ainda.</p>';
    return chrome(u, `
      <button class="btn ghost" type="button" id="btn-desk">← Início</button>
      <h2 style="margin-top:16px">Pacientes</h2>
      <p class="sub">Só você vê esta lista.</p>
      <div class="panel">
        <form id="f-pac" novalidate>
          <label class="fl" for="pnome">Nome ou iniciais</label>
          <input class="inp" id="pnome" name="pnome" placeholder="M.S." value="${esc(S.draft.nome || '')}">
          <label class="fl" for="pfone">WhatsApp do paciente</label>
          <input class="inp" id="pfone" name="pfone" type="tel" inputmode="numeric" placeholder="11999998888" value="${esc(S.draft.fone || '')}">
          <label class="fl" for="pnota">Nota (opcional)</label>
          <input class="inp" id="pnota" name="pnota" placeholder="ex.: fobia de voo" value="${esc(S.draft.nota || '')}">
          ${flashBox()}
          <div class="btnrow"><button class="btn" type="submit">Salvar</button></div>
        </form>
      </div>
      <div class="list">${rows}</div>`);
  }

  function viewAgenda(u) {
    const data = db(u.login);
    const opts = data.patients.map((p, i) => `<option value="${i}">${esc(p.nome)}</option>`).join('');
    const rows = data.appointments.length
      ? data.appointments.map((a) => `<div class="rowitem">
          <div><strong>${esc(a.who)}</strong><small>${esc(a.date)} · ${esc(a.time)}</small></div>
        </div>`).join('')
      : '<p class="hint">Nenhuma consulta marcada.</p>';
    return chrome(u, `
      <button class="btn ghost" type="button" id="btn-desk">← Início</button>
      <h2 style="margin-top:16px">Agenda</h2>
      <p class="sub">Ao marcar, abre o Google Agenda e o WhatsApp do paciente com a mensagem pronta.</p>
      <div class="panel">
        <form id="f-age">
          <label class="fl" for="apaci">Paciente</label>
          <select class="inp" id="apaci" required>${opts || '<option value="">Cadastre um paciente primeiro</option>'}</select>
          <label class="fl" for="adata">Data</label>
          <input class="inp" id="adata" type="date" required>
          <label class="fl" for="ahora">Hora</label>
          <input class="inp" id="ahora" type="time" required>
          <label class="fl" for="alocal">Local</label>
          <input class="inp" id="alocal" placeholder="Online ou endereço">
          ${flashBox()}
          <div class="btnrow">
            <button class="btn orange" type="submit"${data.patients.length ? '' : ' disabled'}>Marcar e avisar</button>
            <a class="btn ghost" href="https://calendar.google.com/" target="_blank" rel="noopener">Abrir Google Agenda</a>
          </div>
        </form>
      </div>
      <div class="list">${rows}</div>`);
  }

  function bind() {
    $('f-login')?.addEventListener('submit', onLogin);
    $('btn-assinar')?.addEventListener('click', () => go('assinar'));
    $('btn-voltar')?.addEventListener('click', () => go('login'));
    $('pay-pix')?.addEventListener('click', onPix);
    $('pay-card')?.addEventListener('click', onCard);
    $('copy-pix')?.addEventListener('click', copyPix);
    $('f-criar')?.addEventListener('submit', onCriar);
    $('btn-sair')?.addEventListener('click', () => { setSession(''); go('login'); });
    $('btn-desk')?.addEventListener('click', () => go('desk'));
    $('go-pac')?.addEventListener('click', () => go('pacientes'));
    $('go-age')?.addEventListener('click', () => go('agenda'));
    $('f-pac')?.addEventListener('submit', onPac);
    $('f-age')?.addEventListener('submit', onAge);
    document.querySelectorAll('[data-del-p]').forEach((b) => {
      b.addEventListener('click', () => delPac(+b.getAttribute('data-del-p')));
    });
  }

  async function onLogin(ev) {
    ev.preventDefault();
    const login = $('login').value.trim().toLowerCase();
    const senha = $('senha').value;
    const u = users().find((x) => x.login === login);
    if (!u) { S.err = 'Usuário não encontrado. Assine para criar o acesso.'; render(); return; }
    const h = await hashPass(login, senha);
    if (h !== u.hash) { S.err = 'Senha incorreta.'; render(); return; }
    setSession(login);
    go('desk');
  }

  function onPix() {
    S.pay = 'pix';
    render();
  }

  function copyPix() {
    navigator.clipboard.writeText(PIX).then(() => { S.flash = 'Chave Pix copiada.'; render(); });
  }

  function onCard() {
    if (PAGSEGURO_LINK) {
      window.open(PAGSEGURO_LINK, '_blank', 'noopener');
      return;
    }
    const msg = 'Olá Priscila! Quero assinar o Terap-ia OS (R$ 100/mês) no PagSeguro ou no cartão. Pode me enviar o link recorrente?';
    window.open(waLink(WA_DONA, msg), '_blank', 'noopener');
  }

  async function onCriar(ev) {
    ev.preventDefault();
    const login = $('nlogin').value.trim().toLowerCase();
    const senha = $('nsenha').value;
    if (!/^[a-z0-9._-]{3,32}$/.test(login)) {
      S.err = 'Use só letras, números, ponto ou hífen no usuário.'; render(); return;
    }
    if (users().some((u) => u.login === login)) {
      S.err = 'Esse usuário já existe. Entre pelo login.'; render(); return;
    }
    const hash = await hashPass(login, senha);
    const list = users();
    list.push({ login, hash, at: new Date().toISOString(), plan: 'mensal', pix: PIX });
    saveUsers(list);
    saveDb(login, { patients: [], appointments: [] });
    const msg = `Olá Priscila! Paguei a mensalidade do Terap-ia OS (R$ 100) no Pix ${PIX} ou no PagSeguro/cartão. Meu usuário: ${login}. Segue o comprovante.`;
    window.open(waLink(WA_DONA, msg), '_blank', 'noopener');
    setSession(login);
    go('desk');
  }

  function onPac(ev) {
    ev.preventDefault();
    const u = currentUser(); if (!u) return;
    const nome = ($('pnome').value || '').trim();
    const fone = digits($('pfone').value);
    const nota = ($('pnota').value || '').trim();
    S.draft = { nome, fone, nota };
    if (!nome) { S.err = 'Informe o nome ou as iniciais.'; render(); return; }
    if (fone.length < 10) { S.err = 'Informe o WhatsApp com DDD (10 ou 11 números).'; render(); return; }
    const data = db(u.login);
    data.patients.unshift({ nome, fone, nota });
    saveDb(u.login, data);
    S.draft = {};
    S.flash = 'Paciente salvo.';
    render();
  }

  function delPac(i) {
    const u = currentUser(); if (!u) return;
    const data = db(u.login);
    data.patients.splice(i, 1);
    saveDb(u.login, data);
    render();
  }

  function onAge(ev) {
    ev.preventDefault();
    const u = currentUser(); if (!u) return;
    const data = db(u.login);
    const p = data.patients[+$('apaci').value];
    if (!p) { S.err = 'Cadastre um paciente antes.'; render(); return; }
    const evn = {
      who: p.nome,
      fone: p.fone,
      date: $('adata').value,
      time: $('ahora').value,
      place: $('alocal').value.trim(),
      note: ''
    };
    data.appointments.unshift(evn);
    saveDb(u.login, data);

    const [y, m, d] = evn.date.split('-');
    const dataBr = d + '/' + m + '/' + y;
    const texto = `Olá, ${p.nome}! Sua consulta está marcada para ${dataBr} às ${evn.time}${evn.place ? ' · ' + evn.place : ''}. Qualquer dúvida, responda esta mensagem.`;
    window.open(gcalLink(evn), '_blank', 'noopener');
    setTimeout(() => window.open(waLink(p.fone, texto), '_blank', 'noopener'), 500);
    S.flash = 'Consulta salva. Google Agenda e WhatsApp abertos.';
    S.view = 'agenda';
    render();
  }

  render();
})();
