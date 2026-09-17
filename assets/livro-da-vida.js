/* Livro da Vida — caderno local de pacientes e relatos, com importação de backup. */
(function (root) {
  const KEY = 'livrovida_db_v1';

  function loadJSON(k, fb) {
    try {
      const raw = localStorage.getItem(k);
      if (!raw) return fb;
      const v = JSON.parse(raw);
      return v == null ? fb : v;
    } catch (e) { return fb; }
  }

  function saveJSON(k, v) {
    localStorage.setItem(k, JSON.stringify(v));
  }

  function emptyDb() {
    return { patients: [], importedAt: null, source: '' };
  }

  function db() {
    const d = loadJSON(KEY, null);
    if (!d || typeof d !== 'object' || !Array.isArray(d.patients)) return emptyDb();
    return d;
  }

  function saveDb(data) { saveJSON(KEY, data); }

  function uid() {
    return 'p_' + Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
  }

  function asText(v) {
    if (v == null) return '';
    if (typeof v === 'string') return v.trim();
    if (typeof v === 'number' || typeof v === 'boolean') return String(v);
    return '';
  }

  function pick(obj, keys) {
    if (!obj || typeof obj !== 'object') return '';
    for (let i = 0; i < keys.length; i++) {
      const t = asText(obj[keys[i]]);
      if (t) return t;
    }
    return '';
  }

  function looksLikePatient(x) {
    if (!x || typeof x !== 'object' || Array.isArray(x)) return false;
    return !!(pick(x, ['nome', 'name', 'paciente', 'patient', 'iniciais', 'title', 'titulo'])
      || Array.isArray(x.relatos) || Array.isArray(x.stories) || Array.isArray(x.sessoes)
      || Array.isArray(x.notes) || Array.isArray(x.evolucoes) || Array.isArray(x.capitulos));
  }

  function looksLikeRelato(x) {
    if (!x || typeof x !== 'object' || Array.isArray(x)) return false;
    return !!(pick(x, ['texto', 'text', 'conteudo', 'content', 'relato', 'body', 'nota', 'note', 'evolucao', 'historia'])
      || pick(x, ['capitulo', 'chapter', 'titulo', 'title']));
  }

  function normalizeRelato(x, fallbackDate) {
    if (typeof x === 'string') {
      return { data: fallbackDate || '', capitulo: '', texto: x.trim() };
    }
    if (!x || typeof x !== 'object') return null;
    const texto = pick(x, ['texto', 'text', 'conteudo', 'content', 'relato', 'body', 'nota', 'note', 'evolucao', 'historia', 'resumo', 'summary']);
    const capitulo = pick(x, ['capitulo', 'chapter', 'titulo', 'title', 'tag', 'tema', 'secao']);
    const data = pick(x, ['data', 'date', 'createdAt', 'created_at', 'quando', 'dia']) || fallbackDate || '';
    if (!texto && !capitulo) return null;
    return { data, capitulo, texto: texto || capitulo };
  }

  function normalizePatient(x) {
    if (typeof x === 'string') {
      return { id: uid(), nome: x.trim(), fone: '', nota: '', relatos: [] };
    }
    if (!x || typeof x !== 'object') return null;
    const nome = pick(x, ['nome', 'name', 'paciente', 'patient', 'iniciais', 'title', 'titulo']) || 'Sem nome';
    const fone = pick(x, ['fone', 'telefone', 'phone', 'whatsapp', 'wa']);
    const nota = pick(x, ['nota', 'queixa', 'obs', 'observacao', 'observações', 'resumo']);
    const bags = [x.relatos, x.stories, x.sessoes, x.notes, x.evolucoes, x.capitulos, x.entries, x.historico, x.livro];
    const relatos = [];
    bags.forEach((bag) => {
      if (!Array.isArray(bag)) return;
      bag.forEach((r) => {
        const n = normalizeRelato(r);
        if (n) relatos.push(n);
      });
    });
    if (typeof x.relato === 'string' && x.relato.trim()) {
      relatos.push(normalizeRelato(x.relato, pick(x, ['data', 'date'])));
    }
    return { id: asText(x.id) || uid(), nome, fone, nota, relatos: relatos.filter(Boolean) };
  }

  function collectPatients(node, out, seen) {
    if (node == null) return;
    if (typeof node === 'string') {
      const t = node.trim();
      if ((t.startsWith('{') || t.startsWith('[')) && t.length > 2) {
        try { collectPatients(JSON.parse(t), out, seen); } catch (e) {}
      }
      return;
    }
    if (Array.isArray(node)) {
      if (node.length && node.every((x) => typeof x === 'string' || looksLikePatient(x))) {
        node.forEach((p) => {
          const n = normalizePatient(p);
          if (n && n.nome) out.push(n);
        });
        return;
      }
      node.forEach((x) => collectPatients(x, out, seen));
      return;
    }
    if (typeof node !== 'object') return;
    if (seen.has(node)) return;
    seen.add(node);

    if (looksLikePatient(node) && !node.patients && !node.pacientes) {
      const n = normalizePatient(node);
      if (n) out.push(n);
      return;
    }

    ['patients', 'pacientes', 'people', 'livros', 'books', 'records', 'items', 'data'].forEach((k) => {
      if (node[k] != null) collectPatients(node[k], out, seen);
    });

    Object.keys(node).forEach((k) => {
      if (k === 'patients' || k === 'pacientes') return;
      const v = node[k];
      if (v && (typeof v === 'object' || typeof v === 'string')) collectPatients(v, out, seen);
    });
  }

  function parseMaybe(text) {
    const t = String(text || '').trim();
    if (!t) throw new Error('Cole ou escolha um arquivo JSON.');
    try { return JSON.parse(t); } catch (e) {}
    const start = t.search(/[\[{]/);
    if (start >= 0) {
      try { return JSON.parse(t.slice(start)); } catch (e2) {}
    }
    throw new Error('O arquivo não é um JSON válido.');
  }

  function normalizeImport(raw) {
    const source = raw;
    const out = [];
    collectPatients(source, out, new WeakSet());
    const byName = new Map();
    out.forEach((p) => {
      const key = (p.nome || '').toLowerCase();
      if (!key) return;
      if (!byName.has(key)) { byName.set(key, p); return; }
      const prev = byName.get(key);
      if (p.fone && !prev.fone) prev.fone = p.fone;
      if (p.nota && !prev.nota) prev.nota = p.nota;
      prev.relatos = prev.relatos.concat(p.relatos);
    });
    return { patients: [...byName.values()] };
  }

  function mergeDb(current, incoming, mode) {
    const next = { patients: current.patients.slice(), importedAt: new Date().toISOString(), source: incoming.source || current.source };
    if (mode === 'replace') next.patients = incoming.patients.slice();
    else {
      incoming.patients.forEach((p) => {
        const i = next.patients.findIndex((x) => x.nome.toLowerCase() === p.nome.toLowerCase());
        if (i < 0) { next.patients.push(p); return; }
        const dest = next.patients[i];
        if (p.fone && !dest.fone) dest.fone = p.fone;
        if (p.nota && !dest.nota) dest.nota = p.nota;
        dest.relatos = dest.relatos.concat(p.relatos);
      });
    }
    return next;
  }

  function exportPayload(data) {
    return {
      app: 'livro-da-vida',
      exportedAt: new Date().toISOString(),
      patients: data.patients
    };
  }

  const api = {
    KEY, emptyDb, db, saveDb, uid, parseMaybe, normalizeImport, mergeDb, exportPayload, asText
  };

  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.LivroVida = api;

  if (typeof document === 'undefined') return;

  const $ = (id) => document.getElementById(id);
  const esc = (s) => String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

  const S = { view: 'home', flash: '', err: '', patientId: '', draft: {}, importPreview: null };

  function flashBox() {
    if (S.err) return '<div class="err">' + esc(S.err) + '</div>';
    if (S.flash) return '<div class="ok">' + esc(S.flash) + '</div>';
    return '';
  }

  function counts(data) {
    const relatos = data.patients.reduce((n, p) => n + (p.relatos ? p.relatos.length : 0), 0);
    return { patients: data.patients.length, relatos };
  }

  function go(view, extra) {
    S.view = view;
    S.err = '';
    S.flash = extra && extra.keepFlash ? S.flash : '';
    if (extra && extra.flash) S.flash = extra.flash;
    if (extra && extra.patientId) S.patientId = extra.patientId;
    render();
  }

  function viewHome() {
    const data = db();
    const c = counts(data);
    const rows = data.patients.length
      ? data.patients.map((p) => `<button type="button" class="rowitem rowbtn" data-open="${esc(p.id)}">
          <div><strong>${esc(p.nome)}</strong><small>${p.relatos.length} relato(s)${p.nota ? ' · ' + esc(p.nota) : ''}</small></div>
          <span class="muted">abrir</span>
        </button>`).join('')
      : '<p class="hint">Ainda não há pacientes neste caderno. Importe o JSON do Manus ou cadastre o primeiro relato.</p>';
    return `
      <section class="panel warn">
        <p class="kicker">Por que o link antigo não abre</p>
        <h2>O site do Manus foi despublicado.</h2>
        <p>O endereço <code>livrovida-rzekdihb.manus.space</code> responde <strong>404</strong>: a página não existe mais na nuvem do Manus. Isso aconteceu depois da mudança de serviço da plataforma (os sites hospedados lá saíram do ar em 23 de agosto de 2026 e só voltam se o backup oficial for restaurado na conta Manus).</p>
        <p>Os relatos <strong>não estão</strong> neste site nem em nenhum arquivo público. Eles ficaram no banco do Manus e, se o app salvava no navegador, também no Chrome/Safari que você usava.</p>
      </section>
      <section class="panel">
        <h2>Como recuperar os dados</h2>
        <ol class="steps">
          <li><strong>Manus (caminho principal).</strong> Entre em <a href="https://manus.im" target="_blank" rel="noopener">manus.im</a> com a mesma conta, abra a ferramenta de restauração e envie o <em>Task Data Backup</em>. Sites publicados voltam sozinhos depois disso. Se não tiver o arquivo, procure no e-mail, Google Drive ou OneDrive um pacote de backup do Manus (agosto de 2026). Sem esse arquivo, o Manus não devolve o banco.</li>
          <li><strong>Navegador (se você abriu o livro neste computador).</strong> Abra o link antigo mesmo em 404, pressione F12 → Application → Local Storage e IndexedDB de <code>livrovida-rzekdihb.manus.space</code>. Exporte as chaves (botão abaixo gera um JSON de tudo que o Chrome ainda guardar nesta origem, se você colar). Depois importe aqui.</li>
          <li><strong>Suporte Manus.</strong> Se o backup sumiu, escreva para <a href="mailto:support@manus.im">support@manus.im</a> com a URL do site e peça a restauração da tarefa WebDev.</li>
        </ol>
        <div class="btnrow">
          <a class="btn orange" href="https://manus.im" target="_blank" rel="noopener">Abrir Manus</a>
          <a class="btn ghost" href="https://help.manus.im/en/articles/16147895-service-change-overview-how-to-restore-your-data" target="_blank" rel="noopener">Guia de restauração</a>
          <button type="button" class="btn ghost" id="go-import">Importar JSON</button>
        </div>
      </section>
      <section class="panel">
        <h2>Caderno local</h2>
        <p class="sub">${c.patients} paciente(s) · ${c.relatos} relato(s) · os dados ficam só neste navegador até você exportar</p>
        ${flashBox()}
        <div class="btnrow">
          <button type="button" class="btn" id="go-novo">Novo paciente</button>
          <button type="button" class="btn ghost" id="btn-export">Exportar backup</button>
          <button type="button" class="btn ghost" id="go-import-2">Importar</button>
        </div>
        <div class="list" style="margin-top:16px">${rows}</div>
      </section>`;
  }

  function viewImport() {
    const prev = S.importPreview;
    const summary = prev
      ? `<div class="ok">Encontrei <strong>${prev.patients.length}</strong> paciente(s) e <strong>${prev.patients.reduce((n, p) => n + p.relatos.length, 0)}</strong> relato(s). Confira e mescle com o caderno local, ou substitua tudo.</div>
         <div class="list">${prev.patients.map((p) => `<div class="rowitem"><div><strong>${esc(p.nome)}</strong><small>${p.relatos.length} relato(s)${p.nota ? ' · ' + esc(p.nota) : ''}</small></div></div>`).join('')}</div>`
      : '';
    return `
      <button class="btn ghost" type="button" id="btn-home">← Voltar</button>
      <h2 style="margin-top:16px">Importar dados</h2>
      <p class="sub">Cole o JSON exportado do Manus, do localStorage ou de um backup. Nada é enviado a servidor: a leitura é só neste navegador.</p>
      <div class="panel">
        <form id="f-import" novalidate>
          <label class="fl" for="arquivo">Arquivo .json</label>
          <input class="inp" id="arquivo" type="file" accept=".json,application/json,text/plain">
          <label class="fl" for="colar">Ou cole o JSON</label>
          <textarea class="inp" id="colar" rows="10" placeholder='{"patients":[{"nome":"M.S.","relatos":[{"data":"2026-03-01","texto":"..."}]}]}'></textarea>
          ${flashBox()}
          ${summary}
          <div class="btnrow">
            <button class="btn" type="submit">Ler JSON</button>
            ${prev ? '<button class="btn orange" type="button" id="btn-merge">Mesclar no caderno</button><button class="btn ghost" type="button" id="btn-replace">Substituir caderno</button>' : ''}
          </div>
        </form>
      </div>`;
  }

  function viewNovo() {
    return `
      <button class="btn ghost" type="button" id="btn-home">← Voltar</button>
      <h2 style="margin-top:16px">Novo paciente</h2>
      <div class="panel">
        <form id="f-pac" novalidate>
          <label class="fl" for="pnome">Nome ou iniciais</label>
          <input class="inp" id="pnome" required placeholder="M.S.">
          <label class="fl" for="pfone">WhatsApp (opcional)</label>
          <input class="inp" id="pfone" type="tel" inputmode="numeric" placeholder="11999998888">
          <label class="fl" for="pnota">Nota</label>
          <input class="inp" id="pnota" placeholder="ex.: fobia de voo">
          ${flashBox()}
          <div class="btnrow"><button class="btn" type="submit">Salvar</button></div>
        </form>
      </div>`;
  }

  function viewPaciente() {
    const data = db();
    const p = data.patients.find((x) => x.id === S.patientId);
    if (!p) return `<p class="err">Paciente não encontrado.</p><button class="btn ghost" type="button" id="btn-home">← Voltar</button>`;
    const relatos = (p.relatos || []).map((r, i) => `<article class="relato">
        <header><strong>${esc(r.capitulo || 'Relato')}</strong><span>${esc(r.data || '')}</span>
          <button type="button" class="btn ghost" data-del-r="${i}">Apagar</button></header>
        <p>${esc(r.texto).replace(/\n/g, '<br>')}</p>
      </article>`).join('') || '<p class="hint">Nenhum relato ainda.</p>';
    return `
      <button class="btn ghost" type="button" id="btn-home">← Voltar</button>
      <h2 style="margin-top:16px">${esc(p.nome)}</h2>
      <p class="sub">${esc(p.fone || 'sem telefone')}${p.nota ? ' · ' + esc(p.nota) : ''}</p>
      <div class="panel">
        <form id="f-relato" novalidate>
          <label class="fl" for="rcap">Capítulo ou tema</label>
          <input class="inp" id="rcap" placeholder="infância, família, medo, sessão">
          <label class="fl" for="rdata">Data</label>
          <input class="inp" id="rdata" type="date">
          <label class="fl" for="rtexto">Relato</label>
          <textarea class="inp" id="rtexto" rows="8" required placeholder="Escreva o relato da vida ou da sessão."></textarea>
          ${flashBox()}
          <div class="btnrow">
            <button class="btn" type="submit">Guardar relato</button>
            <button class="btn ghost" type="button" id="btn-del-p">Apagar paciente</button>
          </div>
        </form>
      </div>
      <div class="list">${relatos}</div>`;
  }

  function render() {
    const app = $('app');
    if (S.view === 'import') app.innerHTML = viewImport();
    else if (S.view === 'novo') app.innerHTML = viewNovo();
    else if (S.view === 'paciente') app.innerHTML = viewPaciente();
    else app.innerHTML = viewHome();
    bind();
  }

  function downloadBackup() {
    const blob = new Blob([JSON.stringify(exportPayload(db()), null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'livro-da-vida-backup.json';
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(a.href);
    S.flash = 'Backup baixado. Guarde esse arquivo fora do navegador.';
    S.view = 'home';
    render();
  }

  function readImport(text) {
    const raw = parseMaybe(text);
    const norm = normalizeImport(raw);
    if (!norm.patients.length) {
      S.err = 'Não achei pacientes ou relatos nesse JSON. Confira se o arquivo veio do Manus ou do localStorage.';
      S.importPreview = null;
      render();
      return;
    }
    S.importPreview = norm;
    S.flash = '';
    S.err = '';
    render();
  }

  function applyImport(mode) {
    if (!S.importPreview) return;
    const next = mergeDb(db(), S.importPreview, mode);
    saveDb(next);
    S.importPreview = null;
    go('home', { flash: mode === 'replace' ? 'Caderno substituído pelos dados importados.' : 'Dados mesclados no caderno local.' });
  }

  function bind() {
    $('btn-home')?.addEventListener('click', () => go('home'));
    $('go-import')?.addEventListener('click', () => go('import'));
    $('go-import-2')?.addEventListener('click', () => go('import'));
    $('go-novo')?.addEventListener('click', () => go('novo'));
    $('btn-export')?.addEventListener('click', downloadBackup);
    document.querySelectorAll('[data-open]').forEach((b) => {
      b.addEventListener('click', () => go('paciente', { patientId: b.getAttribute('data-open') }));
    });
    $('f-pac')?.addEventListener('submit', (ev) => {
      ev.preventDefault();
      const nome = ($('pnome').value || '').trim();
      if (!nome) { S.err = 'Informe o nome ou as iniciais.'; render(); return; }
      const data = db();
      data.patients.unshift({
        id: uid(),
        nome,
        fone: ($('pfone').value || '').replace(/\D/g, ''),
        nota: ($('pnota').value || '').trim(),
        relatos: []
      });
      saveDb(data);
      go('home', { flash: 'Paciente salvo neste navegador. Exporte um backup quando puder.' });
    });
    $('f-relato')?.addEventListener('submit', (ev) => {
      ev.preventDefault();
      const data = db();
      const p = data.patients.find((x) => x.id === S.patientId);
      if (!p) return;
      const texto = ($('rtexto').value || '').trim();
      if (!texto) { S.err = 'Escreva o relato.'; render(); return; }
      p.relatos.unshift({
        capitulo: ($('rcap').value || '').trim(),
        data: $('rdata').value || new Date().toISOString().slice(0, 10),
        texto
      });
      saveDb(data);
      S.flash = 'Relato guardado. Lembre de exportar o backup.';
      render();
    });
    $('btn-del-p')?.addEventListener('click', () => {
      if (!confirm('Apagar este paciente e todos os relatos no caderno local?')) return;
      const data = db();
      data.patients = data.patients.filter((x) => x.id !== S.patientId);
      saveDb(data);
      go('home', { flash: 'Paciente apagado só deste navegador.' });
    });
    document.querySelectorAll('[data-del-r]').forEach((b) => {
      b.addEventListener('click', () => {
        const data = db();
        const p = data.patients.find((x) => x.id === S.patientId);
        if (!p) return;
        p.relatos.splice(+b.getAttribute('data-del-r'), 1);
        saveDb(data);
        render();
      });
    });
    $('arquivo')?.addEventListener('change', (ev) => {
      const f = ev.target.files && ev.target.files[0];
      if (!f) return;
      const reader = new FileReader();
      reader.onload = () => {
        try { readImport(String(reader.result || '')); }
        catch (e) { S.err = e.message || 'Não consegui ler o arquivo.'; render(); }
      };
      reader.readAsText(f);
    });
    $('f-import')?.addEventListener('submit', (ev) => {
      ev.preventDefault();
      try { readImport($('colar').value); }
      catch (e) { S.err = e.message || 'JSON inválido.'; render(); }
    });
    $('btn-merge')?.addEventListener('click', () => applyImport('merge'));
    $('btn-replace')?.addEventListener('click', () => {
      if (!confirm('Substituir todo o caderno local pelos dados importados?')) return;
      applyImport('replace');
    });
  }

  render();
})(typeof window !== 'undefined' ? window : globalThis);
