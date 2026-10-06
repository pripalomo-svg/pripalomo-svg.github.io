/* Terap-ia OS — abre direto, pacientes e agenda neste computador */
(function () {
  const CLINIC_NAME = 'Priscila Palomo';

  const $ = (id) => document.getElementById(id);
  const app = $('app');

  let data = { patients: [], appointments: [] };
  let useMemory = false;

  const S = { view: 'desk', flash: '', err: '', draft: {}, lastLinks: null, q: '', space: '' };

  function esc(s) {
    s = s == null ? '' : String(s);
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function digits(s) { return String(s || '').replace(/\D/g, ''); }

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
      if (S.view === 'desk') render();
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

  function go(view) { S.view = view; S.err = ''; S.flash = ''; render(); }

  function render() {
    if (S.view === 'pacientes') app.innerHTML = viewPacientes();
    else if (S.view === 'agenda') app.innerHTML = viewAgenda();
    else app.innerHTML = viewDesk();
    bind();
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

  function upcoming() {
    const t = todayISO();
    return data.appointments
      .filter((a) => a && a.date && a.date >= t)
      .slice()
      .sort((a, b) => (a.date + (a.time || '')).localeCompare(b.date + (b.time || '')))
      .slice(0, 6);
  }

  function viewDesk() {
    const next = upcoming();
    const rows = next.length
      ? next.map((a) => `<div class="rowitem">
          <div><strong>${a.date === todayISO() ? 'Hoje · ' : ''}${esc(a.who)}</strong><small>${esc(fmtDate(a.date))} · ${esc(a.time || '')}</small></div>
        </div>`).join('')
      : '<p class="hint">Nenhuma consulta a partir de hoje.</p>';
    return chrome(`
      <h2>Sua clínica</h2>
      <p class="sub">${data.patients.length} paciente(s) · ${data.appointments.length} consulta(s). Cabe mais de 1000 pacientes neste computador.</p>
      <p class="hint">${esc(S.space)} O banco fica neste navegador. Baixe um backup para não perder a lista.</p>
      <div class="btnrow">
        <button type="button" class="btn ghost" id="btn-backup">Baixar backup</button>
        <button type="button" class="btn ghost" id="btn-restore">Restaurar backup</button>
        <input type="file" id="file-backup" accept="application/json,.json" class="hidden">
      </div>
      <div class="tiles">
        <button type="button" class="tile" id="go-pac"><b>Pacientes</b><span>Cadastro, busca e telefone</span></button>
        <button type="button" class="tile" id="go-age"><b>Agenda</b><span>Google Agenda + WhatsApp</span></button>
      </div>
      <h2 style="margin-top:22px">Próximas consultas</h2>
      <div class="list">${rows}</div>`);
  }

  function filteredPatients() {
    const q = (S.q || '').trim().toLowerCase();
    return data.patients.map((p, i) => ({ p, i })).filter(({ p }) => {
      if (!q) return true;
      return (p.nome + ' ' + p.fone + ' ' + (p.nota || '')).toLowerCase().indexOf(q) >= 0;
    });
  }

  function viewPacientes() {
    const list = filteredPatients();
    const rows = list.length
      ? list.map(({ p, i }) => `<div class="rowitem">
          <div><strong>${esc(p.nome)}</strong><small>${esc(p.fone)} · ${esc(p.nota || 'sem nota')}</small></div>
          <button type="button" class="btn ghost" data-del-p="${i}">Apagar</button>
        </div>`).join('')
      : '<p class="hint">Nenhum paciente ainda.</p>';
    return chrome(`
      <button class="btn ghost" type="button" id="btn-desk">← Início</button>
      <h2 style="margin-top:16px">Pacientes</h2>
      <p class="sub">Busca instantânea. A lista cabe mais de 1000 nomes.</p>
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
      <label class="fl" for="q">Buscar</label>
      <input class="inp" id="q" value="${esc(S.q || '')}" placeholder="Nome, telefone ou nota" autocomplete="off">
      <div class="list" style="margin-top:12px">${rows}</div>`);
  }

  function viewAgenda() {
    const opts = data.patients.map((p, i) => `<option value="${i}">${esc(p.nome)}</option>`).join('');
    const rows = data.appointments.length
      ? data.appointments.map((a) => `<div class="rowitem">
          <div><strong>${a.date === todayISO() ? 'Hoje · ' : ''}${esc(a.who)}</strong><small>${esc(fmtDate(a.date))} · ${esc(a.time)}</small></div>
        </div>`).join('')
      : '<p class="hint">Nenhuma consulta marcada.</p>';
    return chrome(`
      <button class="btn ghost" type="button" id="btn-desk">← Início</button>
      <h2 style="margin-top:16px">Agenda</h2>
      <p class="sub">Ao marcar, abre o Google Agenda e o WhatsApp do paciente com a mensagem pronta.</p>
      <div class="panel">
        <form id="f-age" novalidate>
          <label class="fl" for="apaci">Paciente</label>
          <select class="inp" id="apaci" required>${opts || '<option value="">Cadastre um paciente primeiro</option>'}</select>
          <label class="fl" for="adata">Data</label>
          <input class="inp" id="adata" type="date" required value="${todayISO()}">
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
    $('q')?.addEventListener('input', onSearch);
    $('btn-backup')?.addEventListener('click', downloadBackup);
    $('btn-restore')?.addEventListener('click', () => $('file-backup').click());
    $('file-backup')?.addEventListener('change', restoreBackup);
    document.querySelectorAll('[data-del-p]').forEach((b) => {
      b.addEventListener('click', () => delPac(+b.getAttribute('data-del-p')));
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

  function onPac(ev) {
    ev.preventDefault();
    const nome = ($('pnome').value || '').trim();
    const fone = digits($('pfone').value);
    const nota = ($('pnota').value || '').trim();
    S.draft = { nome, fone, nota };
    if (!nome) { S.err = 'Informe o nome ou as iniciais.'; render(); return; }
    if (fone.length < 10) { S.err = 'Informe o WhatsApp com DDD (10 ou 11 números).'; render(); return; }
    data.patients.unshift({ nome, fone, nota });
    saveClinic();
    S.draft = {};
    S.q = '';
    S.flash = 'Paciente salvo.';
    render();
  }

  function delPac(i) {
    if (i < 0 || i >= data.patients.length) return;
    data.patients.splice(i, 1);
    saveClinic();
    render();
  }

  function onAge(ev) {
    ev.preventDefault();
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
    saveClinic();

    const dataBr = fmtDate(evn.date);
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

  function downloadBackup() {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'terapia-backup.json';
    document.body.appendChild(a);
    a.click();
    a.remove();
    S.flash = 'Backup baixado. Guarde o arquivo.';
    render();
  }

  function restoreBackup(ev) {
    const file = ev.target.files && ev.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const parsed = normalize(JSON.parse(String(reader.result || '')));
        if (!parsed.patients.length && !parsed.appointments.length) {
          S.err = 'Esse arquivo não tem pacientes nem consultas.';
          render();
          return;
        }
        data = parsed;
        saveClinic();
        S.flash = 'Backup restaurado: ' + parsed.patients.length + ' paciente(s).';
        S.view = 'desk';
        render();
      } catch (e) {
        S.err = 'Não consegui ler esse arquivo.';
        render();
      }
    };
    reader.readAsText(file);
  }

  app.innerHTML = '<div class="os"><div class="bar"><strong>Terap-ia OS</strong><span class="who">' + esc(CLINIC_NAME) + '</span></div><div class="desk"><p class="sub">Abrindo a clínica…</p></div></div>';
  loadClinic().then((d) => {
    data = d;
    render();
    readSpace();
  }).catch(() => {
    data = normalize(harvestLocal());
    useMemory = true;
    render();
  });
})();
