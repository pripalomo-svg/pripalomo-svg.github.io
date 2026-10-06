/* Terap-ia OS — abre direto. Paciente e consulta de hoje na primeira tela. */
(function () {
  const CLINIC_NAME = 'Priscila Palomo';
  const HOURS = ['08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00'];

  const $ = (id) => document.getElementById(id);
  const app = $('app');

  let data = { patients: [], appointments: [] };
  let useMemory = false;
  let writing = false;

  const S = {
    view: 'desk',
    flash: '',
    err: '',
    draft: {},
    lastLinks: null,
    q: '',
    hojeQ: '',
    ageKey: '',
    ageDate: '',
    place: '',
    customTime: '',
    space: '',
    focus: '',
    scrollTo: ''
  };

  function esc(s) {
    s = s == null ? '' : String(s);
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function digits(s) { return String(s || '').replace(/\D/g, ''); }

  function fold(s) {
    return String(s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }

  function uid() {
    return Math.random().toString(36).slice(2, 10) + Date.now().toString(36);
  }

  function matchesQuery(p, q) {
    const n = String(q || '').trim().toLowerCase();
    if (!n) return true;
    const raw = (p.nome + ' ' + p.fone + ' ' + (p.nota || '')).toLowerCase();
    if (raw.indexOf(n) >= 0) return true;
    if (fold(raw).indexOf(fold(n)) >= 0) return true;
    const d = digits(n);
    return d.length >= 3 && String(p.fone || '').indexOf(d) >= 0;
  }

  function normalize(raw) {
    const d = raw && typeof raw === 'object' ? raw : {};
    if (!Array.isArray(d.patients)) d.patients = [];
    if (!Array.isArray(d.appointments)) d.appointments = [];
    return d;
  }

  function harvestLocal() {
    try {
      const sess = (localStorage.getItem('tpos_session') || '').trim().toLowerCase();
      const keys = [];
      if (sess) keys.push('tpos_db_' + sess);
      keys.push('tpos_db_priscila');
      for (let i = 0; i < localStorage.length; i++) {
        const k = localStorage.key(i);
        if (k && k.indexOf('tpos_db_') === 0 && keys.indexOf(k) < 0) keys.push(k);
      }
      let best = null;
      let bestN = -1;
      keys.forEach((k) => {
        try {
          const d = JSON.parse(localStorage.getItem(k) || 'null');
          if (!d || typeof d !== 'object') return;
          const n = (d.patients || []).length + (d.appointments || []).length;
          if (n > bestN) { best = d; bestN = n; }
        } catch (e) {}
      });
      return best;
    } catch (e) { return null; }
  }

  function idbOpen() {
    return new Promise((res, rej) => {
      const r = indexedDB.open('terapia-os', 2);
      r.onupgradeneeded = () => {
        const db = r.result;
        if (!db.objectStoreNames.contains('kv')) db.createObjectStore('kv');
        if (!db.objectStoreNames.contains('audio')) db.createObjectStore('audio');
      };
      r.onsuccess = () => res(r.result);
      r.onerror = () => rej(r.error);
    });
  }

  function idbGet(db, store, key) {
    return new Promise((res, rej) => {
      const q = db.transaction(store).objectStore(store).get(key);
      q.onsuccess = () => res(q.result);
      q.onerror = () => rej(q.error);
    });
  }

  function idbPut(db, store, value, key) {
    return new Promise((res, rej) => {
      const t = db.transaction(store, 'readwrite');
      t.objectStore(store).put(value, key);
      t.oncomplete = () => res();
      t.onerror = () => rej(t.error);
    });
  }

  async function saveClinic() {
    if (!useMemory) {
      try {
        const db = await idbOpen();
        await idbPut(db, 'kv', data, 'clinic');
      } catch (e) { useMemory = true; }
    }
    try {
      const json = JSON.stringify(data);
      if (json.length < 4500000) localStorage.setItem('tpos_db_priscila', json);
    } catch (e) {}
  }

  function ensureIds() {
    let changed = false;
    data.patients.forEach((p) => {
      if (!p || typeof p !== 'object') return;
      if (!p.id) { p.id = uid(); changed = true; }
    });
    return changed;
  }

  async function loadClinic() {
    try {
      const db = await idbOpen();
      const saved = await idbGet(db, 'kv', 'clinic');
      if (saved && typeof saved === 'object' && (saved.patients || saved.appointments)) {
        return normalize(saved);
      }
    } catch (e) { useMemory = true; }
    const local = normalize(harvestLocal());
    data = local;
    if (!useMemory) await saveClinic();
    return local;
  }

  async function readSpace() {
    try {
      if (!navigator.storage || !navigator.storage.estimate) return;
      if (navigator.storage.persist) navigator.storage.persist().catch(() => {});
      const est = await navigator.storage.estimate();
      if (!est.quota) return;
      const gb = est.quota / 1024 / 1024 / 1024;
      S.space = 'Espaço neste computador: cerca de ' + gb.toFixed(1).replace('.', ',') + ' GB.';
      const line = $('space-line');
      if (line) line.textContent = S.space + ' O banco fica neste navegador. Baixe um backup para não perder a lista.';
      else if (S.view === 'desk') render();
    } catch (e) {}
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

  function openTab(url) {
    const a = document.createElement('a');
    a.href = url;
    a.target = '_blank';
    a.rel = 'noopener';
    document.body.appendChild(a);
    a.click();
    a.remove();
  }

  function todayISO() {
    const d = new Date();
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
  }

  function fmtDate(iso) {
    if (!iso || iso.indexOf('-') < 0) return iso || '';
    const [y, m, d] = iso.split('-');
    return d + '/' + m + '/' + y;
  }

  function normTime(t) {
    const m = /^(\d{1,2}):(\d{2})$/.exec(String(t || '').trim());
    if (!m) return '';
    const hh = parseInt(m[1], 10);
    const mm = parseInt(m[2], 10);
    if (hh > 23 || mm > 59) return '';
    return String(hh).padStart(2, '0') + ':' + String(mm).padStart(2, '0');
  }

  function hourLabel(h) {
    return String(parseInt(h.slice(0, 2), 10)) + 'h';
  }

  function go(view) { S.view = view; S.err = ''; S.flash = ''; render(); }

  function patientByKey(key) {
    if (!key) return null;
    return data.patients.find((p) => p && p.id === key) || null;
  }

  function pickerMatches() {
    const q = (S.hojeQ || '').trim();
    const all = data.patients.map((p, i) => ({ p, i })).filter(({ p }) => p && p.nome);
    const filtered = q ? all.filter(({ p }) => matchesQuery(p, q)) : all;
    const rows = filtered.slice(0, 8);
    const sel = patientByKey(S.ageKey);
    if (sel && !rows.some((r) => r.p.id === sel.id)) {
      const i = data.patients.findIndex((p) => p && p.id === sel.id);
      rows.unshift({ p: sel, i });
    }
    return { total: filtered.length, rows };
  }

  function syncSelection() {
    if (!data.patients.length) { S.ageKey = ''; return; }
    if (S.ageKey && !patientByKey(S.ageKey)) S.ageKey = '';
  }

  function render() {
    syncSelection();
    if (S.view === 'pacientes') app.innerHTML = viewPacientes();
    else if (S.view === 'agenda') app.innerHTML = viewAgenda();
    else app.innerHTML = viewDesk();
    bind();
    if (S.focus) {
      const el = $(S.focus);
      S.focus = '';
      if (el) el.focus();
    }
    if (S.scrollTo) {
      const el = $(S.scrollTo);
      S.scrollTo = '';
      if (el && el.scrollIntoView) el.scrollIntoView({ block: 'center' });
    }
  }

  function flashBox() {
    if (S.err) return '<div class="err">' + esc(S.err) + '</div>';
    if (S.flash) return '<div class="ok">' + esc(S.flash) + '</div>';
    return '';
  }

  function chrome(body) {
    return `<div class="os">
      <div class="bar">
        <strong>Terap-ia OS</strong>
        <span class="who">${esc(CLINIC_NAME)}</span>
      </div>
      <div class="desk">${body}</div>
    </div>`;
  }

  function linkRow() {
    if (!S.lastLinks) return '';
    return `<div class="btnrow">
      <a class="btn orange" href="${esc(S.lastLinks.wa)}" target="_blank" rel="noopener">Enviar WhatsApp</a>
      <a class="btn" href="${esc(S.lastLinks.cal)}" target="_blank" rel="noopener">Abrir no Google Agenda</a>
    </div>`;
  }

  function upcomingItems() {
    const t = todayISO();
    return data.appointments
      .map((a, i) => ({ a, i }))
      .filter((x) => x.a && x.a.date && x.a.date >= t)
      .sort((x, y) => (x.a.date + (x.a.time || '')).localeCompare(y.a.date + (y.a.time || '')))
      .slice(0, 8);
  }

  function apptRow(a, i) {
    const hoje = a.date === todayISO() ? 'Hoje · ' : '';
    return `<div class="rowitem">
      <div><strong>${hoje}${esc(a.who)}</strong><small>${esc(fmtDate(a.date))} · ${esc(a.time || '')}${a.place ? ' · ' + esc(a.place) : ''}</small></div>
      <button type="button" class="btn ghost small" data-del-a="${i}">Apagar</button>
    </div>`;
  }

  function viewDesk() {
    const next = upcomingItems();
    const rows = next.length
      ? next.map((x) => apptRow(x.a, x.i)).join('')
      : '<p class="hint">Nenhuma consulta a partir de hoje.</p>';
    return chrome(`
      <h2>Sua clínica</h2>
      <p class="sub">${data.patients.length} paciente(s) · ${data.appointments.length} consulta(s). Cabe mais de 1000 pacientes neste computador.</p>
      <p class="hint" id="space-line">${esc(S.space)} O banco fica neste navegador. Baixe um backup para não perder a lista.</p>
      ${flashBox()}
      <div class="quick">
        <div class="panel">
          <h3>Salvar paciente</h3>
          ${patientFields({ desk: true })}
        </div>
        <div class="panel" id="bloco-hoje">
          <h3>Agendar hoje</h3>
          <p class="sub">Hoje, ${esc(fmtDate(todayISO()))}. Um clique no horário marca e abre WhatsApp e Google Agenda.</p>
          ${patientPicker()}
          <form id="f-hoje" novalidate>
            <label class="fl">Horário</label>
            ${hourButtons('desk')}
            <label class="fl" for="hoje-hora">Outro horário</label>
            <input class="inp" id="hoje-hora" type="time" value="${esc(S.customTime || '')}">
            <label class="fl" for="hoje-local">Local (opcional)</label>
            <input class="inp" id="hoje-local" placeholder="Online ou endereço" value="${esc(S.place || '')}">
            ${linkRow()}
            <div class="btnrow"><button class="btn orange" type="submit">Agendar hoje</button></div>
          </form>
        </div>
      </div>
      <div class="btnrow">
        <button type="button" class="btn ghost" id="btn-backup">Baixar backup</button>
        <button type="button" class="btn ghost" id="btn-restore">Restaurar backup</button>
        <input type="file" id="file-backup" accept="application/json,.json" class="hidden">
      </div>
      <div class="tiles">
        <button type="button" class="tile" id="go-pac"><b>Pacientes</b><span>Cadastro, busca e telefone</span></button>
        <button type="button" class="tile" id="go-age"><b>Agenda</b><span>Outro dia, Google Agenda e WhatsApp</span></button>
      </div>
      <h2 style="margin-top:22px">Próximas consultas</h2>
      <div class="list">${rows}</div>`);
  }

  function patientFields(opts) {
    const hint = opts.desk
      ? 'Enter salva. Sem paciente selecionado, o horário salva e agenda hoje.'
      : 'Enter salva.';
    return `<form id="f-pac" novalidate>
      <label class="fl" for="pnome">Nome ou iniciais</label>
      <input class="inp" id="pnome" name="pnome" autocomplete="off" placeholder="M.S." value="${esc(S.draft.nome || '')}">
      <label class="fl" for="pfone">WhatsApp do paciente</label>
      <input class="inp" id="pfone" name="pfone" type="tel" inputmode="numeric" autocomplete="off" placeholder="11999998888" value="${esc(S.draft.fone || '')}">
      <label class="fl" for="pnota">Nota (pode ficar em branco)</label>
      <input class="inp" id="pnota" name="pnota" autocomplete="off" placeholder="ex.: fobia de voo" value="${esc(S.draft.nota || '')}">
      ${opts.desk ? '' : flashBox()}
      <div class="btnrow"><button class="btn" type="submit">Salvar paciente</button></div>
      <p class="hint">${hint}</p>
    </form>`;
  }

  function filteredPatients() {
    return data.patients.map((p, i) => ({ p, i })).filter(({ p }) => p && matchesQuery(p, S.q));
  }

  function viewPacientes() {
    const list = filteredPatients();
    const rows = list.length
      ? list.map(({ p, i }) => `<div class="rowitem">
          <div><strong>${esc(p.nome)}</strong><small>${esc(p.fone)} · ${esc(p.nota || 'sem nota')}</small></div>
          <div class="actions">
            <button type="button" class="btn orange small" data-hoje="${esc(p.id)}">Hoje</button>
            <button type="button" class="btn ghost small" data-del-p="${i}">Apagar</button>
          </div>
        </div>`).join('')
      : (data.patients.length
        ? '<p class="hint">Nenhum paciente encontrado.</p>'
        : '<p class="hint">Nenhum paciente ainda.</p>');
    return chrome(`
      <button class="btn ghost" type="button" id="btn-desk">← Início</button>
      <h2 style="margin-top:16px">Pacientes</h2>
      <p class="sub">A busca é imediata. Hoje leva para o horário desta data.</p>
      <div class="panel">
        ${patientFields({ desk: false })}
      </div>
      <label class="fl" for="q">Buscar</label>
      <input class="inp" id="q" value="${esc(S.q || '')}" placeholder="Nome, telefone ou nota" autocomplete="off">
      <div class="list" style="margin-top:12px">${rows}</div>`);
  }

  function patientPicker() {
    if (!data.patients.length) {
      return '<p class="hint">Nenhum paciente ainda. Use o nome e o WhatsApp ao salvar.</p>';
    }
    const { total, rows } = pickerMatches();
    const sel = patientByKey(S.ageKey);
    const picks = rows.map(({ p }) => {
      const on = p.id === S.ageKey ? ' on' : '';
      return `<button type="button" class="pick${on}" data-pick="${esc(p.id)}"><b>${esc(p.nome)}</b><small>${esc(p.fone)}</small></button>`;
    }).join('');
    const selectedLine = sel
      ? `<p class="sel">Selecionado: <strong>${esc(sel.nome)}</strong></p>`
      : '<p class="hint">Toque no nome. Se a busca achar só um, ele fica selecionado.</p>';
    const list = total
      ? `<div class="picks">${picks}</div>`
      : '<p class="hint">Nenhum paciente encontrado.</p>';
    const more = total > 8 ? '<p class="hint">Mostrando os primeiros. Continue digitando para achar.</p>' : '';
    return `
      <label class="fl" for="pac-q">Paciente</label>
      <input class="inp" id="pac-q" value="${esc(S.hojeQ || '')}" placeholder="Nome, telefone ou nota" autocomplete="off">
      ${selectedLine}
      ${list}
      ${more}`;
  }

  function hourButtons(scope) {
    return '<div class="hours">' + HOURS.map((h) =>
      `<button type="button" class="hour" data-hora="${h}" data-scope="${scope}" aria-label="Agendar às ${h}">${hourLabel(h)}</button>`
    ).join('') + '</div>';
  }

  function viewAgenda() {
    const rows = data.appointments.length
      ? data.appointments.map((a, i) => apptRow(a, i)).join('')
      : '<p class="hint">Nenhuma consulta marcada.</p>';
    return chrome(`
      <button class="btn ghost" type="button" id="btn-desk">← Início</button>
      <h2 style="margin-top:16px">Agenda</h2>
      <p class="sub">A data já vem em hoje. Um clique no horário abre o WhatsApp e o Google Agenda.</p>
      ${flashBox()}
      <div class="panel" id="bloco-hoje">
        ${patientPicker()}
        <form id="f-age" novalidate>
          <label class="fl" for="adata">Data</label>
          <div class="date-line">
            <input class="inp" id="adata" type="date" value="${esc(S.ageDate || todayISO())}">
            <button class="btn ghost" type="button" id="btn-data-hoje">Hoje</button>
          </div>
          <label class="fl">Horário</label>
          ${hourButtons('agenda')}
          <label class="fl" for="ahora">Outro horário</label>
          <input class="inp" id="ahora" type="time" value="${esc(S.customTime || '')}">
          <label class="fl" for="alocal">Local (opcional)</label>
          <input class="inp" id="alocal" placeholder="Online ou endereço" value="${esc(S.place || '')}">
          ${linkRow()}
          <div class="btnrow">
            <button class="btn orange" type="submit">Agendar</button>
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
    $('f-hoje')?.addEventListener('submit', (ev) => onSchedule(ev, 'desk'));
    $('f-age')?.addEventListener('submit', (ev) => onSchedule(ev, 'agenda'));
    $('q')?.addEventListener('input', onSearch);
    $('pac-q')?.addEventListener('input', onPacQuery);
    $('btn-backup')?.addEventListener('click', downloadBackup);
    $('btn-restore')?.addEventListener('click', () => $('file-backup').click());
    $('file-backup')?.addEventListener('change', restoreBackup);
    $('btn-data-hoje')?.addEventListener('click', () => { S.ageDate = todayISO(); render(); });
    $('adata')?.addEventListener('change', () => { S.ageDate = $('adata').value; });
    $('hoje-hora')?.addEventListener('input', () => { S.customTime = $('hoje-hora').value; });
    $('ahora')?.addEventListener('input', () => { S.customTime = $('ahora').value; });
    $('hoje-local')?.addEventListener('input', () => { S.place = $('hoje-local').value; });
    $('alocal')?.addEventListener('input', () => { S.place = $('alocal').value; });
    $('pnome')?.addEventListener('input', onNomeInput);
    $('pfone')?.addEventListener('input', () => { S.draft.fone = $('pfone').value; });
    $('pnota')?.addEventListener('input', () => { S.draft.nota = $('pnota').value; });
    document.querySelectorAll('[data-del-p]').forEach((b) => {
      b.addEventListener('click', () => delPac(+b.getAttribute('data-del-p')));
    });
    document.querySelectorAll('[data-del-a]').forEach((b) => {
      b.addEventListener('click', () => delAppt(+b.getAttribute('data-del-a')));
    });
    document.querySelectorAll('[data-hoje]').forEach((b) => {
      b.addEventListener('click', () => armHoje(b.getAttribute('data-hoje')));
    });
    document.querySelectorAll('[data-pick]').forEach((b) => {
      b.addEventListener('click', () => selectPatient(b.getAttribute('data-pick')));
    });
    document.querySelectorAll('[data-hora]').forEach((b) => {
      b.addEventListener('click', () => scheduleAt(b.getAttribute('data-scope'), b.getAttribute('data-hora')));
    });
  }

  function onSearch(ev) {
    S.q = ev.target.value;
    const pos = ev.target.selectionStart;
    render();
    const el = $('q');
    if (el) {
      el.focus();
      try { el.setSelectionRange(pos, pos); } catch (e) {}
    }
  }

  function onNomeInput(ev) {
    S.draft.nome = ev.target.value;
    if (!S.ageKey || !ev.target.value.trim()) return;
    S.ageKey = '';
    const pos = ev.target.selectionStart;
    render();
    const el = $('pnome');
    if (el) {
      el.focus();
      try { el.setSelectionRange(pos, pos); } catch (e) {}
    }
  }

  function onPacQuery(ev) {
    S.hojeQ = ev.target.value;
    const q = S.hojeQ.trim();
    if (q) {
      const found = data.patients.filter((p) => p && matchesQuery(p, q));
      if (found.length === 1) S.ageKey = found[0].id;
    }
    const pos = ev.target.selectionStart;
    render();
    const el = $('pac-q');
    if (el) {
      el.focus();
      try { el.setSelectionRange(pos, pos); } catch (e) {}
    }
  }

  function readPatientFields() {
    const nomeEl = $('pnome');
    const foneEl = $('pfone');
    const notaEl = $('pnota');
    return {
      nome: String(nomeEl ? nomeEl.value : (S.draft.nome || '')).trim(),
      fone: digits(foneEl ? foneEl.value : S.draft.fone),
      nota: String(notaEl ? notaEl.value : (S.draft.nota || '')).trim()
    };
  }

  function validatePatient(fields) {
    if (!fields.nome) return { err: 'Informe o nome ou as iniciais.', focus: 'pnome' };
    if (fields.fone.length < 10) return { err: 'Informe o WhatsApp com DDD (10 ou 11 números).', focus: 'pfone' };
    return null;
  }

  function addPatient(fields) {
    const id = uid();
    data.patients.unshift({ id, nome: fields.nome, fone: fields.fone, nota: fields.nota });
    S.draft = {};
    S.q = '';
    S.hojeQ = '';
    S.ageKey = id;
    return id;
  }

  async function onPac(ev) {
    ev.preventDefault();
    if (writing) return;
    const fields = readPatientFields();
    S.draft = fields;
    const v = validatePatient(fields);
    if (v) { S.err = v.err; S.flash = ''; S.focus = v.focus; render(); return; }
    writing = true;
    try {
      addPatient(fields);
      await saveClinic();
      S.err = '';
      if (S.view === 'desk') {
        S.flash = 'Paciente salvo. Clique no horário para agendar hoje.';
        S.scrollTo = 'bloco-hoje';
      } else {
        S.flash = 'Paciente salvo.';
        S.focus = 'pnome';
      }
      render();
    } finally { writing = false; }
  }

  function selectPatient(key) {
    S.ageKey = key;
    S.err = '';
    S.flash = '';
    render();
  }

  function armHoje(key) {
    S.ageKey = key;
    S.hojeQ = '';
    S.err = '';
    const p = patientByKey(key);
    S.flash = p ? 'Escolha o horário de hoje para ' + p.nome + '.' : '';
    S.view = 'desk';
    S.scrollTo = 'bloco-hoje';
    render();
  }

  function readPlace() {
    const el = $('hoje-local') || $('alocal');
    if (el) S.place = el.value.trim();
    return (S.place || '').trim();
  }

  function readDate(scope) {
    if (scope === 'desk') return todayISO();
    const el = $('adata');
    if (el && el.value) S.ageDate = el.value;
    return S.ageDate || todayISO();
  }

  function readCustomTime(scope) {
    const el = scope === 'agenda' ? $('ahora') : $('hoje-hora');
    if (el) S.customTime = el.value;
    return normTime(S.customTime);
  }

  async function onSchedule(ev, scope) {
    ev.preventDefault();
    await scheduleAt(scope, readCustomTime(scope));
  }

  async function scheduleAt(scope, time) {
    if (writing) return;
    writing = true;
    try {
      let created = false;
      let pending = null;
      if (scope === 'desk' && !patientByKey(S.ageKey)) {
        pending = readPatientFields();
        S.draft = pending;
        if (!pending.nome && !pending.fone) {
          S.err = 'Escolha um paciente ou preencha nome e WhatsApp.';
          S.flash = '';
          render();
          return;
        }
        const v = validatePatient(pending);
        if (v) { S.err = v.err; S.flash = ''; S.focus = v.focus; render(); return; }
      }
      const date = readDate(scope);
      const when = normTime(time);
      const place = readPlace();
      if (!pending && !patientByKey(S.ageKey)) { S.err = 'Escolha um paciente.'; S.flash = ''; render(); return; }
      if (!date || !when) { S.err = 'Escolha um horário.'; S.flash = ''; render(); return; }
      if (pending) { addPatient(pending); created = true; }
      const p = patientByKey(S.ageKey);
      if (!p) { S.err = 'Escolha um paciente.'; S.flash = ''; render(); return; }
      const evn = {
        who: p.nome,
        fone: p.fone,
        date: date,
        time: when,
        place: place,
        note: ''
      };
      data.appointments.unshift(evn);
      await saveClinic();
      const dataBr = fmtDate(evn.date);
      const texto = `Olá, ${p.nome}! Sua consulta está marcada para ${dataBr} às ${evn.time}${evn.place ? ' · ' + evn.place : ''}. Qualquer dúvida, responda esta mensagem.`;
      const wa = waLink(p.fone, texto);
      const cal = gcalLink(evn);
      openTab(wa);
      openTab(cal);
      const quando = evn.date === todayISO() ? 'hoje às ' + evn.time : 'para ' + dataBr + ' às ' + evn.time;
      S.flash = (created ? 'Paciente e consulta salvos ' : 'Consulta salva ') + quando + '. WhatsApp e Google Agenda abertos — se o navegador bloquear, use os links.';
      S.err = '';
      S.lastLinks = { wa, cal };
      S.ageKey = '';
      S.hojeQ = '';
      S.customTime = '';
      render();
    } finally { writing = false; }
  }

  async function delPac(i) {
    if (writing) return;
    if (i < 0 || i >= data.patients.length) return;
    writing = true;
    try {
      const p = data.patients[i];
      if (p && p.id === S.ageKey) S.ageKey = '';
      data.patients.splice(i, 1);
      await saveClinic();
      S.flash = 'Paciente apagado.';
      S.err = '';
      render();
    } finally { writing = false; }
  }

  async function delAppt(i) {
    if (writing) return;
    if (i < 0 || i >= data.appointments.length) return;
    writing = true;
    try {
      data.appointments.splice(i, 1);
      await saveClinic();
      S.flash = 'Consulta apagada.';
      S.err = '';
      S.lastLinks = null;
      render();
    } finally { writing = false; }
  }

  function downloadBackup() {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'terapia-backup.json';
    document.body.appendChild(a);
    a.click();
    a.remove();
    S.flash = 'Backup baixado. Guarde o arquivo.';
    S.err = '';
    render();
  }

  function restoreBackup(ev) {
    const input = ev.target;
    const file = input.files && input.files[0];
    input.value = '';
    if (!file) return;
    const reader = new FileReader();
    reader.onload = async () => {
      try {
        const parsed = normalize(JSON.parse(String(reader.result || '')));
        if (!parsed.patients.length && !parsed.appointments.length) {
          S.err = 'Esse arquivo não tem pacientes nem consultas.';
          S.flash = '';
          render();
          return;
        }
        data = parsed;
        ensureIds();
        await saveClinic();
        S.ageKey = '';
        S.hojeQ = '';
        S.q = '';
        S.draft = {};
        S.lastLinks = null;
        S.err = '';
        S.flash = 'Backup restaurado: ' + parsed.patients.length + ' paciente(s).';
        S.view = 'desk';
        render();
      } catch (e) {
        S.err = 'Não consegui ler esse arquivo.';
        S.flash = '';
        render();
      }
    };
    reader.readAsText(file);
  }

  app.innerHTML = '<div class="os"><div class="bar"><strong>Terap-ia OS</strong><span class="who">' + esc(CLINIC_NAME) + '</span></div><div class="desk"><p class="sub">Abrindo a clínica…</p></div></div>';
  loadClinic().then(async (d) => {
    data = d;
    if (ensureIds()) await saveClinic();
    render();
    readSpace();
  }).catch(() => {
    data = normalize(harvestLocal());
    useMemory = true;
    ensureIds();
    render();
  });
})();
