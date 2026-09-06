/* Terap-ia OS — clínica, pacientes, agenda (Google + WhatsApp) */
(function () {
  const CLINIC_NAME = 'Priscila Palomo';

  const $ = (id) => document.getElementById(id);
  const app = $('app');

  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  function loadJSON(k, fb) {
    try {
      const raw = store.get(k);
      if (!raw) return fb;
      const v = JSON.parse(raw);
      return v == null ? fb : v;
    } catch (e) { return fb; }
  }

  function clinicLogin() {
    const sess = (store.get('tpos_session') || '').trim().toLowerCase();
    if (sess) return sess;
    try {
      for (let i = 0; i < localStorage.length; i++) {
        const k = localStorage.key(i);
        if (k && k.indexOf('tpos_db_') === 0) return k.slice(8);
      }
    } catch (e) {}
    return 'priscila';
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
      location: ev.place || 'Consultório / online',
      ctz: 'America/Sao_Paulo'
    });
    return 'https://www.google.com/calendar/render?' + q.toString();
  }

  function openTab(url) {
    const a = document.createElement('a');
    a.href = url;
    a.target = '_blank';
    a.rel = 'noopener';
    document.body.appendChild(a);
    a.click();
    a.remove();
  }

  const S = { view: 'desk', flash: '', err: '', draft: {}, lastLinks: null };

  function currentUser() {
    return { login: clinicLogin(), nome: CLINIC_NAME };
  }

  function go(view) { S.view = view; S.err = ''; S.flash = ''; render(); }

  function render() {
    const u = currentUser();
    if (S.view === 'pacientes') app.innerHTML = viewPacientes(u);
    else if (S.view === 'agenda') app.innerHTML = viewAgenda(u);
    else app.innerHTML = viewDesk(u);
    bind();
  }

  function flashBox() {
    if (S.err) return '<div class="err">' + esc(S.err) + '</div>';
    if (S.flash) return '<div class="ok">' + esc(S.flash) + '</div>';
    return '';
  }

  function chrome(u, body) {
    return `<div class="os">
      <div class="bar">
        <strong>Terap-ia OS</strong>
        <span class="who">${esc(u.nome)}</span>
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
      <p class="sub">Cadastro da clínica — nome e WhatsApp.</p>
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
        <form id="f-age" novalidate>
          <label class="fl" for="apaci">Paciente</label>
          <select class="inp" id="apaci" required>${opts || '<option value="">Cadastre um paciente primeiro</option>'}</select>
          <label class="fl" for="adata">Data</label>
          <input class="inp" id="adata" type="date" required>
          <label class="fl" for="ahora">Hora</label>
          <input class="inp" id="ahora" type="time" required>
          <label class="fl" for="alocal">Local</label>
          <input class="inp" id="alocal" placeholder="Online ou endereço">
          ${flashBox()}
          ${S.lastLinks ? `<div class="btnrow">
            <a class="btn orange" href="${esc(S.lastLinks.wa)}" target="_blank" rel="noopener">Enviar WhatsApp</a>
            <a class="btn" href="${esc(S.lastLinks.cal)}" target="_blank" rel="noopener">Abrir no Google Agenda</a>
          </div>` : ''}
          <div class="btnrow">
            <button class="btn orange" type="submit"${data.patients.length ? '' : ' disabled'}>Marcar e avisar</button>
            <a class="btn ghost" href="https://calendar.google.com/calendar/u/0/r" target="_blank" rel="noopener">Abrir Google Agenda</a>
          </div>
        </form>
      </div>
      <div class="list">${rows}</div>`);
  }

  function bind() {
    $('btn-desk')?.addEventListener('click', () => go('desk'));
    $('go-pac')?.addEventListener('click', () => go('pacientes'));
    $('go-age')?.addEventListener('click', () => go('agenda'));
    $('f-pac')?.addEventListener('submit', onPac);
    $('f-age')?.addEventListener('submit', onAge);
    document.querySelectorAll('[data-del-p]').forEach((b) => {
      b.addEventListener('click', () => delPac(+b.getAttribute('data-del-p')));
    });
  }

  function onPac(ev) {
    ev.preventDefault();
    const u = currentUser();
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
    const u = currentUser();
    const data = db(u.login);
    data.patients.splice(i, 1);
    saveDb(u.login, data);
    render();
  }

  function onAge(ev) {
    ev.preventDefault();
    const u = currentUser();
    const data = db(u.login);
    if (!data.patients.length) { S.err = 'Cadastre um paciente antes.'; render(); return; }
    const p = data.patients[+$('apaci').value];
    if (!p) { S.err = 'Escolha um paciente.'; render(); return; }
    if (!$('adata').value || !$('ahora').value) { S.err = 'Informe data e hora.'; render(); return; }
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
    const wa = waLink(p.fone, texto);
    const cal = gcalLink(evn);
    openTab(wa);
    openTab(cal);
    S.flash = 'Consulta salva. WhatsApp do paciente e Google Agenda abertos — se o navegador bloquear, use os links abaixo.';
    S.lastLinks = { wa, cal };
    S.view = 'agenda';
    render();
  }

  render();
})();
