/* Terap-ia OS — clínica, agenda (Google + WhatsApp), prontuário da sessão */
(function () {
  const CLINIC_NAME = 'Priscila Palomo';

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
    const data = d && typeof d === 'object' ? d : { patients: [], appointments: [] };
    if (!Array.isArray(data.patients)) data.patients = [];
    if (!Array.isArray(data.appointments)) data.appointments = [];
    let dirty = false;
    data.patients.forEach((p) => {
      if (!p.id) { p.id = uid('p'); dirty = true; }
    });
    data.appointments.forEach((a) => {
      if (!a.id) { a.id = uid('a'); dirty = true; }
    });
    if (dirty) saveDb(login, data);
    return data;
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

  function uid(prefix) {
    return prefix + Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
  }
  function todayISO() {
    const d = new Date();
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
  }
  function isToday(a) { return a && a.date === todayISO(); }
  function fmtAppt(a) {
    if (!a || !a.date) return '';
    const [y, m, d] = a.date.split('-');
    return d + '/' + m + '/' + y + (a.time ? ' · ' + a.time : '');
  }

  const FLAGS = [
    { re: /n[ãa]o quero mais viver|n[ãa]o aguento mais viver|cansei de viver/i, tag: 'ideação suicida' },
    { re: /ataque de p[âa]nico|falta de ar|cora[çc][ãa]o disparado|achei que ia morrer/i, tag: 'pânico' },
    { re: /n[ãa]o consigo sair de casa|evito|deixei de ir/i, tag: 'esquiva' },
    { re: /chor(o|ando|ou|ar)|l[áa]grimas|solu[cç]o|me emocionei/i, tag: 'choro' },
    { re: /estou com raiva|fiquei brava|fiquei bravo|irritad/i, tag: 'raiva' },
    { re: /estou triste|me deu um vazio|vontade de chorar|ficou triste/i, tag: 'tristeza' }
  ];
  function quoteAround(text, re) {
    const i = text.search(re);
    if (i < 0) return text.slice(0, 120);
    return text.slice(Math.max(0, i - 24), Math.min(text.length, i + 90)).trim();
  }
  function scanTextFlags(text) {
    const found = [];
    FLAGS.forEach((f) => {
      if (f.re.test(text || '')) found.push({ tag: f.tag, quote: quoteAround(text, f.re) });
    });
    return found;
  }
  function localSummary(text, flags, plan) {
    const cry = (flags || []).filter((a) => a.tag === 'choro');
    const emo = (flags || []).filter((a) => ['choro', 'pânico', 'raiva', 'tristeza'].includes(a.tag));
    const sint = (flags || []).filter((a) => !['choro', 'raiva', 'tristeza'].includes(a.tag));
    const clip = (t) => (t || '').trim() ? ((t.trim().slice(0, 900)) + (t.trim().length > 900 ? '…' : '')) : 'Dados insuficientes.';
    return {
      sintomatologia: sint.length ? sint.map((a) => a.tag + ': "' + a.quote + '"').join('\n') : clip(text),
      emocoes: emo.length ? emo.map((a) => a.tag + ': "' + a.quote + '"').join('\n') : 'Não evidenciado de forma automática — revise o texto integral.',
      choro: cry.length ? cry.map((a) => '"' + a.quote + '"').join('\n') : 'Não evidenciado na transcrição.',
      dsm: 'Rascunho automático: use o texto integral para hipóteses DSM-5 (não fecha diagnóstico).',
      plano: (plan && plan.trim()) ? plan.trim() : 'Ainda não anotado pela profissional.'
    };
  }

  let _idb = null;
  function idbOpen() {
    if (_idb) return Promise.resolve(_idb);
    return new Promise((res, rej) => {
      const r = indexedDB.open('terapia-os', 1);
      r.onupgradeneeded = () => { if (!r.result.objectStoreNames.contains('audio')) r.result.createObjectStore('audio'); };
      r.onsuccess = () => { _idb = r.result; res(_idb); };
      r.onerror = () => rej(r.error);
    });
  }
  async function putAudio(id, blob) {
    const dbx = await idbOpen();
    return new Promise((res, rej) => {
      const t = dbx.transaction('audio', 'readwrite');
      t.objectStore('audio').put(blob, id);
      t.oncomplete = () => res();
      t.onerror = () => rej(t.error);
    });
  }
  async function getAudio(id) {
    try {
      const dbx = await idbOpen();
      return new Promise((res, rej) => {
        const q = dbx.transaction('audio').objectStore('audio').get(id);
        q.onsuccess = () => res(q.result || null);
        q.onerror = () => rej(q.error);
      });
    } catch (e) { return null; }
  }

  const S = {
    view: 'desk', flash: '', err: '', draft: {}, lastLinks: null,
    apptId: '', recording: false, rec: null, mediaRec: null,
    capDisplay: null, capMic: null, capCtx: null, audioChunks: [],
    saveTimer: null, t0: null, timer: null
  };

  function currentUser() {
    return { login: clinicLogin(), nome: CLINIC_NAME };
  }

  function go(view) { S.view = view; S.err = ''; S.flash = ''; render(); }

  function render() {
    const u = currentUser();
    if (S.view === 'pacientes') app.innerHTML = viewPacientes(u);
    else if (S.view === 'agenda') app.innerHTML = viewAgenda(u);
    else if (S.view === 'sessao') app.innerHTML = viewSessao(u);
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
        <button type="button" class="tile" id="go-age"><b>Agenda</b><span>Google, WhatsApp e gravação no dia</span></button>
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
      ? data.appointments.map((a) => {
          const today = isToday(a);
          return `<div class="rowitem ${today ? 'today' : ''}">
          <div>
            <strong>${today ? 'HOJE · ' : ''}${esc(a.who)}</strong>
            <small>${esc(fmtAppt(a))}${a.hasAudio ? ' · áudio salvo' : ''}${a.transcript ? ' · transcrição' : ''}</small>
          </div>
          <div class="btnrow" style="margin:0">
            ${today && !S.recording ? `<button type="button" class="btn orange" data-rec="${esc(a.id)}">Gravar áudio do computador</button>` : ''}
            <button type="button" class="btn ghost" data-open="${esc(a.id)}">Prontuário</button>
          </div>
        </div>`;
        }).join('')
      : '<p class="hint">Nenhuma consulta marcada.</p>';
    return chrome(u, `
      <button class="btn ghost" type="button" id="btn-desk">← Início</button>
      <h2 style="margin-top:16px">Agenda</h2>
      <p class="sub">Ao marcar, abre o Google Agenda e o WhatsApp. No dia da consulta, grave o áudio do computador — a transcrição entra no prontuário.</p>
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

  function viewSessao(u) {
    const data = db(u.login);
    const a = data.appointments.find((x) => x.id === S.apptId);
    if (!a) {
      return chrome(u, `<button class="btn ghost" type="button" id="btn-desk">← Início</button>
        <p class="sub" style="margin-top:16px">Consulta não encontrada.</p>`);
    }
    const today = isToday(a);
    const sum = a.summary || {};
    return chrome(u, `
      <button class="btn ghost" type="button" id="go-age">← Agenda</button>
      <h2 style="margin-top:16px">Prontuário · ${esc(a.who)}</h2>
      <p class="sub">${esc(fmtAppt(a))}${today ? ' · sessão de hoje' : ''}</p>
      ${flashBox()}
      <div class="panel ${today ? 'today-panel' : ''}">
        <div class="btnrow">
          ${today && !S.recording ? `<button type="button" class="btn orange" id="btn-rec">Gravar áudio do computador</button>` : ''}
          ${S.recording ? `<button type="button" class="btn orange" id="btn-stop">Encerrar e salvar no prontuário</button>` : ''}
          ${a.hasAudio ? `<button type="button" class="btn ghost" id="btn-play">Ouvir áudio</button>` : ''}
        </div>
        <p class="hint">Na janela do Chrome, escolha a aba da videochamada e marque <strong>Compartilhar áudio da aba</strong>. A transcrição é salva sozinha a cada poucos segundos.</p>
        <audio id="aud" class="hidden" controls style="width:100%;margin-top:10px"></audio>
      </div>
      <div class="panel">
        <label class="fl" for="tx">Transcrição integral — entra no prontuário</label>
        <textarea class="inp" id="tx" rows="8" placeholder="A transcrição aparece aqui. Você também pode digitar ou colar.">${esc(a.transcript || '')}</textarea>
        <label class="fl" for="plan">Planejamento da próxima sessão (sua escrita)</label>
        <textarea class="inp" id="plan" rows="3" placeholder="Objetivo, tarefa, o que retomar.">${esc(a.plan || '')}</textarea>
        <div class="btnrow">
          <button type="button" class="btn" id="btn-sum">Gerar resumo clínico agora</button>
        </div>
      </div>
      ${a.summary ? `<div class="panel">
        <h3>Sintomatologia</h3><p class="pre">${esc(sum.sintomatologia || '')}</p>
        <h3>Emoções observadas</h3><p class="pre">${esc(sum.emocoes || '')}</p>
        <h3>Momentos de choro ou ruptura afetiva</h3><p class="pre">${esc(sum.choro || '')}</p>
        <h3>Sugestões de rastreio DSM-5</h3><p class="pre">${esc(sum.dsm || '')}</p>
        <h3>Planejamento da próxima sessão</h3><p class="pre">${esc(sum.plano || '')}</p>
        <p class="hint">Rascunho de prontuário — revisar antes de incorporar ao registro oficial.</p>
      </div>` : ''}`);
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
    document.querySelectorAll('[data-open]').forEach((b) => {
      b.addEventListener('click', () => openSessao(b.getAttribute('data-open')));
    });
    document.querySelectorAll('[data-rec]').forEach((b) => {
      b.addEventListener('click', () => startSessRec(b.getAttribute('data-rec')));
    });
    $('btn-rec')?.addEventListener('click', () => startSessRec(S.apptId));
    $('btn-stop')?.addEventListener('click', stopSessRec);
    $('btn-play')?.addEventListener('click', () => playSessAudio(S.apptId));
    $('btn-sum')?.addEventListener('click', saveProntuario);
    $('tx')?.addEventListener('input', persistDraft);
    $('plan')?.addEventListener('input', persistDraft);
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
    data.patients.unshift({ id: uid('p'), nome, fone, nota });
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
    if (!data.patients.length) { S.err = 'Cadastre um paciente antes.'; render(); return; }
    const p = data.patients[+$('apaci').value];
    if (!p) { S.err = 'Escolha um paciente.'; render(); return; }
    if (!$('adata').value || !$('ahora').value) { S.err = 'Informe data e hora.'; render(); return; }
    const evn = {
      id: uid('a'),
      who: p.nome,
      fone: p.fone,
      date: $('adata').value,
      time: $('ahora').value,
      place: $('alocal').value.trim(),
      note: '',
      transcript: '',
      plan: '',
      summary: null,
      hasAudio: false
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

  function apptOf(u, id) {
    return db(u.login).appointments.find((x) => x.id === id) || null;
  }
  function openSessao(id) {
    S.apptId = id;
    S.view = 'sessao';
    S.err = '';
    S.flash = '';
    render();
  }
  function persistDraft() {
    const u = currentUser(); if (!u || !S.apptId) return;
    const data = db(u.login);
    const a = data.appointments.find((x) => x.id === S.apptId);
    if (!a) return;
    if ($('tx')) a.transcript = $('tx').value;
    if ($('plan')) a.plan = $('plan').value;
    a.flags = scanTextFlags(a.transcript || '');
    if (S.recording) a.status = 'gravando';
    saveDb(u.login, data);
  }
  function saveProntuario() {
    const u = currentUser(); if (!u || !S.apptId) { S.err = 'Abra uma consulta primeiro.'; render(); return; }
    persistDraft();
    const data = db(u.login);
    const a = data.appointments.find((x) => x.id === S.apptId);
    if (!a) return;
    a.summary = localSummary(a.transcript, a.flags, a.plan);
    a.status = 'registrada';
    saveDb(u.login, data);
    S.flash = 'Resumo clínico salvo no prontuário desta consulta.';
    render();
  }

  async function startSessRec(id) {
    const u = currentUser(); if (!u) return;
    S.apptId = id;
    const a = apptOf(u, id);
    if (!a) return;
    if (!confirm('A transcrição exige consentimento escrito. O Chrome vai pedir para compartilhar a aba da videochamada — marque "Compartilhar áudio da aba". Continuar?')) return;
    S.audioChunks = [];
    let gotSys = false;
    try {
      const display = await navigator.mediaDevices.getDisplayMedia({
        video: { frameRate: 1, width: 32, height: 32 },
        audio: true
      });
      display.getVideoTracks().forEach((t) => { t.enabled = false; t.stop(); });
      S.capDisplay = display;
      gotSys = display.getAudioTracks().length > 0;
      if (!gotSys) alert('Nenhum áudio do computador chegou. Na próxima, marque "Compartilhar áudio da aba". Vou gravar o microfone e transcrever mesmo assim.');
    } catch (e) {
      S.capDisplay = null;
      if (!confirm('Compartilhamento cancelado. Gravar só o microfone e transcrever?')) return;
    }
    try { S.capMic = await navigator.mediaDevices.getUserMedia({ audio: true }); } catch (e) { S.capMic = null; }

    if ((S.capDisplay && S.capDisplay.getAudioTracks().length) || S.capMic) {
      try {
        S.capCtx = new AudioContext();
        const dest = S.capCtx.createMediaStreamDestination();
        if (S.capDisplay && S.capDisplay.getAudioTracks().length) {
          S.capCtx.createMediaStreamSource(new MediaStream(S.capDisplay.getAudioTracks())).connect(dest);
        }
        if (S.capMic) S.capCtx.createMediaStreamSource(S.capMic).connect(dest);
        const mime = ['audio/webm;codecs=opus', 'audio/webm', 'audio/mp4'].find((m) => window.MediaRecorder && MediaRecorder.isTypeSupported(m)) || '';
        S.mediaRec = new MediaRecorder(dest.stream, mime ? { mimeType: mime } : {});
        S.mediaRec.ondataavailable = (ev) => { if (ev.data && ev.data.size) S.audioChunks.push(ev.data); };
        S.mediaRec.start(4000);
      } catch (e) { S.mediaRec = null; }
    }

    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SR) {
      S.rec = new SR();
      S.rec.lang = 'pt-BR';
      S.rec.continuous = true;
      S.rec.interimResults = true;
      let settled = (a.transcript || '') + (a.transcript ? ' ' : '');
      S.rec.onresult = (e) => {
        let interim = '';
        for (let i = e.resultIndex; i < e.results.length; i++) {
          const t = e.results[i][0].transcript;
          if (e.results[i].isFinal) settled += t + ' ';
          else interim += t;
        }
        const box = $('tx');
        if (box) box.value = settled;
        persistDraft();
      };
      S.rec.onend = () => { if (S.recording) { try { S.rec.start(); } catch (e) {} } };
      try { S.rec.start(); } catch (e) {}
    }

    S.recording = true;
    S.view = 'sessao';
    persistDraft();
    render();
  }

  async function stopSessRec() {
    persistDraft();
    S.recording = false;
    if (S.rec) { try { S.rec.stop(); } catch (e) {} }
    clearInterval(S.saveTimer);
    if (S.mediaRec && S.mediaRec.state !== 'inactive') {
      await new Promise((res) => {
        S.mediaRec.onstop = res;
        try { S.mediaRec.stop(); } catch (e) { res(); }
      });
    }
    if (S.capDisplay) S.capDisplay.getTracks().forEach((t) => t.stop());
    if (S.capMic) S.capMic.getTracks().forEach((t) => t.stop());
    if (S.capCtx) { try { S.capCtx.close(); } catch (e) {} }
    S.capDisplay = S.capMic = S.capCtx = S.mediaRec = null;

    const u = currentUser();
    if (u && S.apptId && S.audioChunks.length) {
      try {
        const blob = new Blob(S.audioChunks, { type: S.audioChunks[0].type || 'audio/webm' });
        await putAudio(S.apptId, blob);
        const data = db(u.login);
        const a = data.appointments.find((x) => x.id === S.apptId);
        if (a) { a.hasAudio = true; saveDb(u.login, data); }
      } catch (e) {}
    }
    S.audioChunks = [];
    saveProntuario();
  }

  async function playSessAudio(id) {
    const blob = await getAudio(id);
    if (!blob) { S.err = 'Áudio não encontrado neste navegador.'; render(); return; }
    const url = URL.createObjectURL(blob);
    const el = $('aud');
    if (!el) return;
    el.src = url;
    el.classList.remove('hidden');
    el.play().catch(() => {});
  }

  render();
})();
