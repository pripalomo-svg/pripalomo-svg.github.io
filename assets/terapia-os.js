/* Terap-ia OS — login, ficha de pacientes, agenda (aviso opcional), cofre AES-GCM */
(function () {
  const PIX = '11950690537';
  const WA_DONA = '5511950690537';
  /* Cole aqui o link recorrente do PagBank/PagSeguro (R$ 100/mês, cartão). */
  const PAGSEGURO_LINK = '';
  const PRECO = 'R$ 100 / mês';
  const IDLE_MS = 30 * 60 * 1000;
  const LOCK_MAX = 5;
  const LOCK_MS = 15 * 60 * 1000;
  const PBKDF2_ITERS = 210000;
  const LEGACY_ITERS = 120000;

  const $ = (id) => document.getElementById(id);
  const app = $('app');
  const enc = new TextEncoder();
  const dec = new TextDecoder();

  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} },
    del(k) { try { localStorage.removeItem(k); } catch (e) {} }
  };

  const tab = {
    get(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} },
    del(k) { try { sessionStorage.removeItem(k); } catch (e) {} }
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

  function lockKey(login) { return 'tpos_lock_' + login; }
  function readLock(login) { return loadJSON(lockKey(login), { n: 0, until: 0 }); }
  function writeLock(login, o) { store.set(lockKey(login), JSON.stringify(o)); }
  function clearLock(login) { store.del(lockKey(login)); }

  function emptyDb() { return { patients: [], appointments: [] }; }

  function hex(buf) {
    return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
  }

  function b64(buf) {
    const u = new Uint8Array(buf);
    let s = '';
    for (let i = 0; i < u.length; i++) s += String.fromCharCode(u[i]);
    return btoa(s);
  }

  function fromB64(s) {
    const bin = atob(s);
    const u = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i);
    return u;
  }

  function randBytes(n) {
    const u = new Uint8Array(n);
    crypto.getRandomValues(u);
    return u;
  }

  function uid() {
    if (crypto.randomUUID) return crypto.randomUUID();
    return hex(randBytes(16));
  }

  function safeEq(a, b) {
    const aa = enc.encode(String(a || ''));
    const bb = enc.encode(String(b || ''));
    const n = Math.max(aa.length, bb.length, 1);
    let x = aa.length === bb.length ? 0 : 1;
    for (let i = 0; i < n; i++) x |= (aa[i] || 0) ^ (bb[i] || 0);
    return x === 0;
  }

  function weakPass(p) {
    if (!p || p.length < 8) return 'A senha precisa ter no mínimo 8 caracteres.';
    if (!/[A-Za-z]/.test(p) || !/\d/.test(p)) return 'Use letras e números na senha.';
    return '';
  }

  async function pbkdf2(pass, saltBytes, iters, bits) {
    const key = await crypto.subtle.importKey('raw', enc.encode(pass), 'PBKDF2', false, ['deriveBits']);
    return crypto.subtle.deriveBits(
      { name: 'PBKDF2', salt: saltBytes, iterations: iters, hash: 'SHA-256' },
      key, bits
    );
  }

  async function keysFromPass(pass, saltBytes) {
    const bits = await pbkdf2(pass, saltBytes, PBKDF2_ITERS, 512);
    const all = new Uint8Array(bits);
    const hash = hex(all.slice(0, 32));
    const aes = await crypto.subtle.importKey('raw', all.slice(32), 'AES-GCM', true, ['encrypt', 'decrypt']);
    return { hash, aes };
  }

  async function legacyHash(login, pass) {
    const bits = await pbkdf2(pass, enc.encode('terapia-os:' + login.toLowerCase()), LEGACY_ITERS, 256);
    return hex(bits);
  }

  async function encryptDb(key, obj) {
    const iv = randBytes(12);
    const ct = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, enc.encode(JSON.stringify(obj)));
    return { v: 2, iv: b64(iv), ct: b64(ct) };
  }

  async function decryptDb(key, blob) {
    const pt = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: fromB64(blob.iv) }, key, fromB64(blob.ct));
    const data = JSON.parse(dec.decode(pt));
    if (!data || typeof data !== 'object') return emptyDb();
    if (!Array.isArray(data.patients)) data.patients = [];
    if (!Array.isArray(data.appointments)) data.appointments = [];
    return data;
  }

  function vaultKey(login) { return 'tpos_vault_' + login; }
  function legacyDbKey(login) { return 'tpos_db_' + login; }

  function readPlainLegacy(login) {
    return loadJSON(legacyDbKey(login), emptyDb());
  }

  const mem = { login: '', key: null, data: null, last: 0 };

  async function persistVault() {
    if (!mem.login || !mem.key || !mem.data) return;
    const blob = await encryptDb(mem.key, mem.data);
    store.set(vaultKey(mem.login), JSON.stringify(blob));
    store.del(legacyDbKey(mem.login));
  }

  async function exportSession() {
    if (!mem.login || !mem.key) { tab.del('tpos_sess'); return; }
    const raw = await crypto.subtle.exportKey('raw', mem.key);
    tab.set('tpos_sess', JSON.stringify({ login: mem.login, k: b64(raw), t: Date.now() }));
  }

  function wipeMem() {
    mem.login = '';
    mem.key = null;
    mem.data = null;
    mem.last = 0;
    tab.del('tpos_sess');
  }

  async function openSession(login, key, data) {
    mem.login = login;
    mem.key = key;
    mem.data = data;
    mem.last = Date.now();
    await persistVault();
    await exportSession();
  }

  function touch() {
    if (!mem.login) return;
    mem.last = Date.now();
    exportSession();
  }

  function idleExpired() {
    if (!mem.login) return true;
    return Date.now() - mem.last > IDLE_MS;
  }

  function logout(msg) {
    wipeMem();
    S.view = 'login';
    S.editId = '';
    S.pending = null;
    S.draft = {};
    if (msg) S.flash = msg;
    render();
  }

  function currentUser() {
    if (!mem.login) return null;
    return users().find((u) => u.login === mem.login) || null;
  }

  function db() {
    return mem.data || emptyDb();
  }

  async function saveDb() {
    await persistVault();
  }

  function esc(s) {
    s = s == null ? '' : String(s);
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function digits(s) { return String(s || '').replace(/\D/g, ''); }

  function fmtFone(n) {
    const d = digits(n);
    if (d.length === 11) return '(' + d.slice(0, 2) + ') ' + d.slice(2, 7) + '-' + d.slice(7);
    if (d.length === 10) return '(' + d.slice(0, 2) + ') ' + d.slice(2, 6) + '-' + d.slice(6);
    return d || '—';
  }

  function fmtDate(iso) {
    if (!iso) return '—';
    const [y, m, d] = String(iso).split('-');
    if (!d) return iso;
    return d + '/' + m + '/' + y;
  }

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
      location: ev.place || 'Consultório / online',
      ctz: 'America/Sao_Paulo'
    });
    return 'https://www.google.com/calendar/render?' + q.toString();
  }

  const S = { view: 'login', flash: '', err: '', pay: '', draft: {}, editId: '', pending: null };

  const VIEWS = ['login', 'assinar', 'desk', 'pacientes', 'paciente-novo', 'agenda'];

  function go(view) {
    S.view = view;
    S.err = '';
    S.flash = '';
    if (view !== 'paciente-novo') S.editId = '';
    if (view !== 'agenda') S.pending = null;
    if (location.hash.replace('#', '') !== view) location.hash = view;
    render();
  }

  function render() {
    if (mem.login && idleExpired()) {
      wipeMem();
      S.view = 'login';
      S.flash = 'Sessão encerrada por inatividade (30 min). Entre de novo.';
    }

    const u = currentUser();
    if (u && S.view === 'login') S.view = 'desk';
    if (!u && ['desk', 'pacientes', 'paciente-novo', 'agenda'].indexOf(S.view) >= 0) S.view = 'login';

    if (S.view === 'login') app.innerHTML = viewLogin();
    else if (S.view === 'assinar') app.innerHTML = viewAssinar();
    else if (S.view === 'pacientes') app.innerHTML = viewPacientes(u);
    else if (S.view === 'paciente-novo') app.innerHTML = viewPacienteNovo(u);
    else if (S.view === 'agenda') app.innerHTML = viewAgenda(u);
    else app.innerHTML = viewDesk(u);
    bind();
  }

  function flashBox() {
    if (S.err) return '<div class="err" role="alert">' + esc(S.err) + '</div>';
    if (S.flash) return '<div class="ok" role="status">' + esc(S.flash) + '</div>';
    return '';
  }

  function viewLogin() {
    return `<div class="lock">
      <div class="lock-card">
        <div class="kicker">Terap-ia OS</div>
        <h1>Entrar</h1>
        <p class="lead">Banco da clínica com cofre no aparelho. Cada login enxerga só os próprios pacientes.</p>
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
        <p class="hint">Pix 11 95069-0537 · PagSeguro ou cartão. Sessão some ao fechar a aba e após 30 min parada.</p>
      </div>
    </div>`;
  }

  function viewAssinar() {
    const pix = S.pay === 'pix';
    return `<div class="lock">
      <div class="lock-card wide">
        <div class="kicker">Mensalidade</div>
        <h1>${PRECO}</h1>
        <p class="lead">Pague e crie o login. A ficha clínica fica cifrada com a sua senha.</p>
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
        <form id="f-criar" novalidate>
          <label class="fl" for="nlogin">Crie o usuário</label>
          <input class="inp" id="nlogin" required minlength="3" autocomplete="username" placeholder="ex.: clinica.silva">
          <label class="fl" for="nsenha">Crie a senha (8+ com letra e número)</label>
          <input class="inp" id="nsenha" type="password" required minlength="8" autocomplete="new-password">
          <label class="fl" for="nsenha2">Repita a senha</label>
          <input class="inp" id="nsenha2" type="password" required minlength="8" autocomplete="new-password">
          ${flashBox()}
          <div class="btnrow">
            <button class="btn orange full" type="submit">Já paguei · criar acesso</button>
            <button class="btn ghost full" type="button" id="btn-voltar">Voltar ao login</button>
          </div>
        </form>
        <div class="cloud">
          <b>O que este site já faz sozinho:</b>
          senha com PBKDF2, fichas em AES-GCM, sessão só nesta aba, bloqueio após 5 tentativas e aviso de consulta só se você mandar.
          <br><br>
          <b>Para 1000 clínicas de verdade, preciso que você abra e me passe:</b>
          conta <b>Supabase</b> (URL + chave anon) para login e Postgres com RLS;
          bucket <b>Cloudflare R2</b> (Account ID + access key) para arquivos;
          link recorrente do <b>PagBank/PagSeguro</b> de R$ 100;
          e, se quiser agenda nativa, um <b>Google Cloud OAuth</b> (client ID).
          Sem isso o cofre fica no navegador de cada profissional — seguro no aparelho, sem nuvem compartilhada.
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
    const data = db();
    return chrome(u, `
      <h2>Sua clínica</h2>
      <p class="sub">${data.patients.length} paciente(s) · ${data.appointments.length} consulta(s) · cofre cifrado</p>
      <div class="tiles">
        <button type="button" class="tile" id="go-novo"><b>Novo paciente</b><span>Ficha completa com telefone</span></button>
        <button type="button" class="tile" id="go-pac"><b>Pacientes</b><span>Lista e edição</span></button>
        <button type="button" class="tile" id="go-age"><b>Agenda</b><span>Marcar e escolher se avisa</span></button>
      </div>`);
  }

  function patientLabel(p) {
    const social = p.nomeSocial ? ' (' + p.nomeSocial + ')' : '';
    return (p.nome || 'Sem nome') + social;
  }

  function viewPacientes(u) {
    const data = db();
    const rows = data.patients.length
      ? data.patients.map((p) => `<div class="rowitem">
          <div>
            <strong>${esc(patientLabel(p))}</strong>
            <small>${esc(fmtFone(p.fone))}${p.email ? ' · ' + esc(p.email) : ''}${p.nascimento ? ' · nasc. ' + esc(fmtDate(p.nascimento)) : ''}</small>
          </div>
          <div class="row-actions">
            <button type="button" class="btn ghost" data-edit-p="${esc(p.id)}">Editar</button>
            <button type="button" class="btn ghost danger" data-del-p="${esc(p.id)}">Apagar</button>
          </div>
        </div>`).join('')
      : '<p class="hint">Nenhum paciente ainda. Abra a ficha para cadastrar.</p>';
    return chrome(u, `
      <button class="btn ghost" type="button" id="btn-desk">← Início</button>
      <h2 style="margin-top:16px">Pacientes</h2>
      <p class="sub">Fichas só desta clínica, cifradas neste aparelho.</p>
      <div class="btnrow" style="margin:0 0 16px">
        <button class="btn orange" type="button" id="go-novo">Adicionar paciente</button>
      </div>
      ${flashBox()}
      <div class="list">${rows}</div>`);
  }

  function field(id, label, type, val, extra) {
    const v = val == null ? '' : String(val);
    if (type === 'textarea') {
      return `<label class="fl" for="${id}">${label}</label>
        <textarea class="inp" id="${id}" rows="3">${esc(v)}</textarea>`;
    }
    if (type === 'checkbox') {
      return `<label class="check"><input type="checkbox" id="${id}"${v ? ' checked' : ''}> ${label}</label>`;
    }
    return `<label class="fl" for="${id}">${label}</label>
      <input class="inp" id="${id}" type="${type || 'text'}" value="${esc(v)}"${extra || ''}>`;
  }

  function viewPacienteNovo(u) {
    const data = db();
    const p = (S.editId && data.patients.find((x) => x.id === S.editId)) || S.draft || {};
    const edit = !!(S.editId && data.patients.some((x) => x.id === S.editId));
    return chrome(u, `
      <button class="btn ghost" type="button" id="btn-pacs">← Pacientes</button>
      <h2 style="margin-top:16px">${edit ? 'Editar paciente' : 'Adicionar paciente'}</h2>
      <p class="sub">Todos os dados da ficha, inclusive telefone. Obrigatórios: nome e telefone com DDD.</p>
      <form id="f-pac" class="panel" novalidate autocomplete="off">
        <div class="grid2">
          <div>${field('pnome', 'Nome completo', 'text', p.nome, ' autocomplete="name"')}</div>
          <div>${field('pnomeSocial', 'Nome social', 'text', p.nomeSocial)}</div>
          <div>${field('pnascimento', 'Data de nascimento', 'date', p.nascimento)}</div>
          <div>${field('pfone', 'Telefone / WhatsApp', 'tel', p.fone, ' inputmode="numeric" placeholder="11999998888"')}</div>
          <div>${field('pemail', 'E-mail', 'email', p.email, ' autocomplete="off"')}</div>
          <div>${field('pcpf', 'CPF (opcional)', 'text', p.cpf, ' inputmode="numeric" placeholder="somente números"')}</div>
          <div class="span2">${field('pendereco', 'Endereço', 'text', p.endereco)}</div>
          <div>${field('pcidade', 'Cidade', 'text', p.cidade)}</div>
          <div>${field('pcep', 'CEP', 'text', p.cep, ' inputmode="numeric"')}</div>
          <div>${field('pemergNome', 'Contato de emergência', 'text', p.emergNome)}</div>
          <div>${field('pemergFone', 'Telefone de emergência', 'tel', p.emergFone, ' inputmode="numeric"')}</div>
          <div>${field('pconvenio', 'Convênio / particular', 'text', p.convenio)}</div>
          <div>${field('pprofissao', 'Profissão', 'text', p.profissao)}</div>
        </div>
        ${field('pqueixa', 'Queixa principal / motivo', 'textarea', p.queixa)}
        ${field('pobs', 'Observações clínicas', 'textarea', p.obs)}
        ${field('pconsent', 'Paciente autorizou o cadastro destes dados para o atendimento (LGPD).', 'checkbox', p.consent)}
        ${flashBox()}
        <div class="btnrow">
          <button class="btn orange" type="submit">${edit ? 'Atualizar ficha' : 'Salvar paciente'}</button>
          <button class="btn ghost" type="button" id="btn-pacs-2">Cancelar</button>
        </div>
      </form>`);
  }

  function viewAgenda(u) {
    const data = db();
    const opts = data.patients.map((p) =>
      `<option value="${esc(p.id)}">${esc(patientLabel(p))} · ${esc(fmtFone(p.fone))}</option>`
    ).join('');
    const rows = data.appointments.length
      ? data.appointments.map((a) => `<div class="rowitem">
          <div>
            <strong>${esc(a.who)}</strong>
            <small>${esc(fmtDate(a.date))} · ${esc(a.time)}${a.place ? ' · ' + esc(a.place) : ''} · ${a.avisou === true ? 'paciente informado' : a.avisou === false ? 'sem aviso' : 'aviso pendente'}</small>
          </div>
        </div>`).join('')
      : '<p class="hint">Nenhuma consulta marcada.</p>';

    let pending = '';
    if (S.pending) {
      pending = `<div class="choice" role="region" aria-label="Informar o paciente">
        <h3>Consulta marcada</h3>
        <p>Pode informar <b>${esc(S.pending.who)}</b> no WhatsApp <b>${esc(fmtFone(S.pending.fone))}</b> sobre ${esc(fmtDate(S.pending.date))} às ${esc(S.pending.time)}?</p>
        <div class="btnrow">
          <button class="btn orange" type="button" id="btn-avisar-sim">Informar o paciente</button>
          <button class="btn ghost" type="button" id="btn-avisar-nao">Não informar</button>
        </div>
        <div class="btnrow">
          <a class="btn ghost" href="${esc(S.pending.cal)}" target="_blank" rel="noopener noreferrer">Colocar no Google Agenda</a>
        </div>
      </div>`;
    }

    return chrome(u, `
      <button class="btn ghost" type="button" id="btn-desk">← Início</button>
      <h2 style="margin-top:16px">Agenda</h2>
      <p class="sub">Marque a consulta. Depois você escolhe se informa o paciente ou não — nada é enviado sozinho.</p>
      ${pending}
      <div class="panel">
        <form id="f-age" novalidate>
          <label class="fl" for="apaci">Paciente</label>
          <select class="inp" id="apaci">${opts || '<option value="">Cadastre um paciente primeiro</option>'}</select>
          <label class="fl" for="adata">Data</label>
          <input class="inp" id="adata" type="date">
          <label class="fl" for="ahora">Hora</label>
          <input class="inp" id="ahora" type="time">
          <label class="fl" for="alocal">Local</label>
          <input class="inp" id="alocal" placeholder="Online ou endereço">
          ${flashBox()}
          <div class="btnrow">
            <button class="btn orange" type="submit"${data.patients.length ? '' : ' disabled'}>Marcar consulta</button>
            <a class="btn ghost" href="https://calendar.google.com/calendar/u/0/r" target="_blank" rel="noopener noreferrer">Abrir Google Agenda</a>
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
    $('btn-sair')?.addEventListener('click', () => logout('Você saiu. O cofre ficou fechado.'));
    $('btn-desk')?.addEventListener('click', () => go('desk'));
    $('btn-pacs')?.addEventListener('click', () => go('pacientes'));
    $('btn-pacs-2')?.addEventListener('click', () => go('pacientes'));
    $('go-pac')?.addEventListener('click', () => go('pacientes'));
    $('go-novo')?.addEventListener('click', () => { S.editId = ''; S.draft = {}; go('paciente-novo'); });
    $('go-age')?.addEventListener('click', () => go('agenda'));
    $('f-pac')?.addEventListener('submit', onPac);
    $('f-age')?.addEventListener('submit', onAge);
    $('btn-avisar-sim')?.addEventListener('click', () => decideNotify(true));
    $('btn-avisar-nao')?.addEventListener('click', () => decideNotify(false));
    document.querySelectorAll('[data-edit-p]').forEach((b) => {
      b.addEventListener('click', () => {
        S.editId = b.getAttribute('data-edit-p') || '';
        S.draft = {};
        go('paciente-novo');
      });
    });
    document.querySelectorAll('[data-del-p]').forEach((b) => {
      b.addEventListener('click', () => delPac(b.getAttribute('data-del-p')));
    });
  }

  function lockedUntil(login) {
    const L = readLock(login);
    if (L.until && Date.now() < L.until) return L.until;
    return 0;
  }

  function failLogin(login) {
    const L = readLock(login);
    L.n = (L.n || 0) + 1;
    if (L.n >= LOCK_MAX) {
      L.until = Date.now() + LOCK_MS;
      L.n = 0;
    }
    writeLock(login, L);
    if (L.until && Date.now() < L.until) {
      return 'Muitas tentativas. Aguarde 15 minutos e tente de novo.';
    }
    return 'Usuário ou senha incorretos.';
  }

  async function onLogin(ev) {
    ev.preventDefault();
    const login = $('login').value.trim().toLowerCase();
    const senha = $('senha').value;
    if (!login || !senha) { S.err = 'Informe usuário e senha.'; render(); return; }

    const until = lockedUntil(login);
    if (until) {
      S.err = 'Muitas tentativas. Aguarde 15 minutos e tente de novo.';
      render();
      return;
    }

    const u = users().find((x) => x.login === login);
    if (!u) { S.err = failLogin(login || 'unknown'); render(); return; }

    try {
      if (u.v === 2 && u.salt) {
        const { hash, aes } = await keysFromPass(senha, fromB64(u.salt));
        if (!safeEq(hash, u.hash)) { S.err = failLogin(login); render(); return; }
        const raw = store.get(vaultKey(login));
        let data = emptyDb();
        if (raw) {
          try { data = await decryptDb(aes, JSON.parse(raw)); }
          catch (e) { S.err = 'Cofre ilegível. A senha não abre estes dados.'; render(); return; }
        } else {
          data = readPlainLegacy(login);
        }
        clearLock(login);
        await openSession(login, aes, normalizePatients(data));
        go('desk');
        return;
      }

      const h = await legacyHash(login, senha);
      if (!safeEq(h, u.hash)) { S.err = failLogin(login); render(); return; }
      const salt = randBytes(16);
      const { hash, aes } = await keysFromPass(senha, salt);
      const list = users().map((x) => x.login === login
        ? { login, hash, salt: b64(salt), v: 2, at: x.at || new Date().toISOString(), plan: x.plan || 'mensal' }
        : x);
      saveUsers(list);
      clearLock(login);
      await openSession(login, aes, normalizePatients(readPlainLegacy(login)));
      go('desk');
    } catch (e) {
      S.err = 'Não foi possível abrir o cofre neste navegador.';
      render();
    }
  }

  function normalizePatients(data) {
    const d = data && typeof data === 'object' ? data : emptyDb();
    d.patients = (d.patients || []).map((p) => {
      if (p.id) return p;
      return Object.assign({ id: uid() }, p);
    });
    d.appointments = (d.appointments || []).map((a) => {
      if (a.id) return a;
      return Object.assign({ id: uid() }, a);
    });
    return d;
  }

  function onPix() {
    S.pay = 'pix';
    render();
  }

  function copyPix() {
    const done = () => { S.flash = 'Chave Pix copiada.'; render(); };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(PIX).then(done).catch(() => {
        S.flash = 'Chave Pix: ' + PIX; render();
      });
    } else {
      S.flash = 'Chave Pix: ' + PIX; render();
    }
  }

  function onCard() {
    if (PAGSEGURO_LINK) {
      window.open(PAGSEGURO_LINK, '_blank', 'noopener,noreferrer');
      return;
    }
    const msg = 'Olá Priscila! Quero assinar o Terap-ia OS (R$ 100/mês) no PagSeguro ou no cartão. Pode me enviar o link recorrente?';
    window.open(waLink(WA_DONA, msg), '_blank', 'noopener,noreferrer');
  }

  async function onCriar(ev) {
    ev.preventDefault();
    const login = $('nlogin').value.trim().toLowerCase();
    const senha = $('nsenha').value;
    const senha2 = $('nsenha2').value;
    if (!/^[a-z0-9._-]{3,32}$/.test(login)) {
      S.err = 'Use só letras, números, ponto ou hífen no usuário (3 a 32).'; render(); return;
    }
    const w = weakPass(senha);
    if (w) { S.err = w; render(); return; }
    if (senha !== senha2) { S.err = 'As senhas não coincidem.'; render(); return; }
    if (users().some((u) => u.login === login)) {
      S.err = 'Esse usuário já existe. Entre pelo login.'; render(); return;
    }
    const salt = randBytes(16);
    const { hash, aes } = await keysFromPass(senha, salt);
    const list = users();
    list.push({ login, hash, salt: b64(salt), v: 2, at: new Date().toISOString(), plan: 'mensal' });
    saveUsers(list);
    await openSession(login, aes, emptyDb());
    const msg = `Olá Priscila! Paguei a mensalidade do Terap-ia OS (R$ 100) no Pix ${PIX} ou no PagSeguro/cartão. Meu usuário: ${login}. Segue o comprovante.`;
    window.open(waLink(WA_DONA, msg), '_blank', 'noopener,noreferrer');
    go('desk');
  }

  function readFicha() {
    return {
      nome: ($('pnome').value || '').trim(),
      nomeSocial: ($('pnomeSocial').value || '').trim(),
      nascimento: $('pnascimento').value || '',
      fone: digits($('pfone').value),
      email: ($('pemail').value || '').trim(),
      cpf: digits($('pcpf').value),
      endereco: ($('pendereco').value || '').trim(),
      cidade: ($('pcidade').value || '').trim(),
      cep: digits($('pcep').value),
      emergNome: ($('pemergNome').value || '').trim(),
      emergFone: digits($('pemergFone').value),
      convenio: ($('pconvenio').value || '').trim(),
      profissao: ($('pprofissao').value || '').trim(),
      queixa: ($('pqueixa').value || '').trim(),
      obs: ($('pobs').value || '').trim(),
      consent: !!$('pconsent').checked
    };
  }

  async function onPac(ev) {
    ev.preventDefault();
    if (!currentUser()) return;
    const f = readFicha();
    S.draft = f;
    if (!f.nome) { S.err = 'Informe o nome completo.'; render(); return; }
    if (f.fone.length < 10 || f.fone.length > 13) {
      S.err = 'Informe o telefone com DDD (10 ou 11 números).'; render(); return;
    }
    if (f.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.email)) {
      S.err = 'E-mail inválido.'; render(); return;
    }
    if (f.cpf && f.cpf.length !== 11) {
      S.err = 'CPF deve ter 11 números, ou deixe em branco.'; render(); return;
    }
    if (!f.consent) {
      S.err = 'Marque o consentimento para guardar a ficha.'; render(); return;
    }
    const data = db();
    if (S.editId) {
      const i = data.patients.findIndex((p) => p.id === S.editId);
      if (i < 0) { S.err = 'Paciente não encontrado.'; render(); return; }
      data.patients[i] = Object.assign({}, data.patients[i], f, { id: S.editId, updatedAt: new Date().toISOString() });
      S.flash = 'Ficha atualizada.';
    } else {
      data.patients.unshift(Object.assign({ id: uid(), createdAt: new Date().toISOString() }, f));
      S.flash = 'Paciente salvo.';
    }
    await saveDb();
    S.draft = {};
    S.editId = '';
    S.view = 'pacientes';
    location.hash = 'pacientes';
    render();
  }

  async function delPac(id) {
    if (!currentUser()) return;
    const data = db();
    const p = data.patients.find((x) => x.id === id);
    if (!p) return;
    if (!window.confirm('Apagar a ficha de ' + patientLabel(p) + '? Esta ação não desfaz.')) return;
    data.patients = data.patients.filter((x) => x.id !== id);
    await saveDb();
    S.flash = 'Ficha apagada.';
    render();
  }

  async function onAge(ev) {
    ev.preventDefault();
    if (!currentUser()) return;
    const data = db();
    if (!data.patients.length) { S.err = 'Cadastre um paciente antes.'; render(); return; }
    const p = data.patients.find((x) => x.id === $('apaci').value);
    if (!p) { S.err = 'Escolha um paciente.'; render(); return; }
    if (!$('adata').value || !$('ahora').value) { S.err = 'Informe data e hora.'; render(); return; }
    const evn = {
      id: uid(),
      patientId: p.id,
      who: patientLabel(p),
      fone: p.fone,
      date: $('adata').value,
      time: $('ahora').value,
      place: $('alocal').value.trim(),
      note: '',
      avisou: null,
      createdAt: new Date().toISOString()
    };
    data.appointments.unshift(evn);
    await saveDb();

    const texto = `Olá, ${p.nomeSocial || p.nome}! Sua consulta está marcada para ${fmtDate(evn.date)} às ${evn.time}${evn.place ? ' · ' + evn.place : ''}. Qualquer dúvida, responda esta mensagem.`;
    S.pending = {
      id: evn.id,
      who: evn.who,
      fone: p.fone,
      date: evn.date,
      time: evn.time,
      wa: waLink(p.fone, texto),
      cal: gcalLink(evn)
    };
    S.flash = '';
    S.err = '';
    S.view = 'agenda';
    render();
    $('btn-avisar-sim')?.focus();
  }

  async function decideNotify(yes) {
    if (!S.pending || !currentUser()) return;
    const data = db();
    const a = data.appointments.find((x) => x.id === S.pending.id);
    if (a) a.avisou = !!yes;
    await saveDb();
    if (yes) {
      window.open(S.pending.wa, '_blank', 'noopener,noreferrer');
      S.flash = 'Consulta salva. WhatsApp aberto com a mensagem — envie só se confirmar o envio lá.';
    } else {
      S.flash = 'Consulta salva. O paciente não será informado.';
    }
    S.pending = null;
    render();
  }

  async function restoreSession() {
    const raw = tab.get('tpos_sess');
    if (!raw) return;
    try {
      const s = JSON.parse(raw);
      if (!s.login || !s.k || !s.t) return;
      if (Date.now() - s.t > IDLE_MS) { tab.del('tpos_sess'); return; }
      const u = users().find((x) => x.login === s.login && x.v === 2);
      if (!u) { tab.del('tpos_sess'); return; }
      const aes = await crypto.subtle.importKey('raw', fromB64(s.k), 'AES-GCM', true, ['encrypt', 'decrypt']);
      const blob = store.get(vaultKey(s.login));
      let data = emptyDb();
      if (blob) data = await decryptDb(aes, JSON.parse(blob));
      mem.login = s.login;
      mem.key = aes;
      mem.data = normalizePatients(data);
      mem.last = s.t;
    } catch (e) {
      wipeMem();
    }
  }

  function onHash() {
    const v = location.hash.replace('#', '');
    if (!v || VIEWS.indexOf(v) < 0) return;
    if (!mem.login && ['desk', 'pacientes', 'paciente-novo', 'agenda'].indexOf(v) >= 0) {
      S.view = 'login';
      render();
      return;
    }
    S.view = v;
    render();
  }

  document.addEventListener('click', touch, true);
  document.addEventListener('keydown', touch, true);
  window.addEventListener('hashchange', onHash);

  restoreSession().then(() => {
    const v = location.hash.replace('#', '');
    if (mem.login && VIEWS.indexOf(v) >= 0 && v !== 'login') S.view = v;
    render();
  });
})();
