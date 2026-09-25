/* Leitura do extrato 2026. Categorias e notas ficam só neste navegador. */
(function () {
  const D = window.EXTRATO;
  if (!D) return;

  const STORE = "priscila-extrato-2026-v1";
  const MESES = ["2026-01","2026-02","2026-03","2026-04","2026-05","2026-06","2026-07","2026-08","2026-09"];
  const MES_NOME = ["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro"];
  const MES_CURTO = ["jan","fev","mar","abr","mai","jun","jul","ago","set"];
  const SEMANA = [
    { d: 1, nome: "seg" }, { d: 2, nome: "ter" }, { d: 3, nome: "qua" },
    { d: 4, nome: "qui" }, { d: 5, nome: "sex" }, { d: 6, nome: "sáb" }, { d: 0, nome: "dom" }
  ];

  const SETORES = {
    salario_priscila: { nome: "Salário da Priscila", familia: "salario_priscila", natureza: "entrada" },
    aporte_priscila: { nome: "Transferência da Priscila", familia: "aporte_priscila", natureza: "entrada" },
    salario_luisa: { nome: "Salário da Luísa (McKinsey)", familia: "salario_luisa", natureza: "entrada" },
    outras_entradas: { nome: "Outras entradas", familia: "outras_entradas", natureza: "entrada" },
    estorno: { nome: "Estorno", familia: "outras_entradas", natureza: "entrada" },
    rendimento: { nome: "Rendimento", familia: "outras_entradas", natureza: "entrada" },
    cartao_black: { nome: "Cartão Black", familia: "cartao_black", natureza: "saida" },
    moradia: { nome: "Moradia", familia: "moradia", natureza: "saida" },
    educacao: { nome: "Educação", familia: "educacao", natureza: "saida" },
    pessoas: { nome: "Pessoas", familia: "pessoas", natureza: "saida" },
    para_priscila: { nome: "Enviado à Priscila", familia: "pessoas", natureza: "saida" },
    saude: { nome: "Saúde", familia: "dia_a_dia", natureza: "saida" },
    alimentacao: { nome: "Alimentação", familia: "dia_a_dia", natureza: "saida" },
    transporte: { nome: "Transporte", familia: "dia_a_dia", natureza: "saida" },
    compras: { nome: "Compras", familia: "dia_a_dia", natureza: "saida" },
    viagem: { nome: "Viagem", familia: "dia_a_dia", natureza: "saida" },
    lazer: { nome: "Lazer", familia: "dia_a_dia", natureza: "saida" },
    assinaturas: { nome: "Assinaturas", familia: "assinaturas", natureza: "saida" },
    impostos: { nome: "Impostos", familia: "oficiais", natureza: "saida" },
    boletos: { nome: "Boletos", familia: "oficiais", natureza: "saida" },
    investimentos: { nome: "Investimentos", familia: "investimentos", natureza: "saida" },
    transferencia_banco: { nome: "Outro banco", familia: "investimentos", natureza: "saida" },
    outros: { nome: "Outros", familia: "outros", natureza: "saida" },
    cofrinho: { nome: "Cofrinho", familia: "interna", natureza: "interna" },
    cdb: { nome: "CDB", familia: "interna", natureza: "interna" },
    tbi: { nome: "Mesma conta", familia: "interna", natureza: "interna" }
  };

  const FAMILIAS = [
    { id: "salario_priscila", nome: "Salário da Priscila", lado: "entrada", cor: "#0E4A57" },
    { id: "aporte_priscila", nome: "Transferências da Priscila", lado: "entrada", cor: "#5BA3B5" },
    { id: "salario_luisa", nome: "Salário da Luísa (McKinsey)", lado: "entrada", cor: "#2A9D8F" },
    { id: "outras_entradas", nome: "Outras entradas", lado: "entrada", cor: "#7FB3A6" },
    { id: "cartao_black", nome: "Cartão Black", lado: "saida", cor: "#1A1A1A" },
    { id: "moradia", nome: "Moradia", lado: "saida", cor: "#E27A2E" },
    { id: "educacao", nome: "Educação", lado: "saida", cor: "#C44536" },
    { id: "pessoas", nome: "Pessoas", lado: "saida", cor: "#6B4C9A" },
    { id: "assinaturas", nome: "Assinaturas", lado: "saida", cor: "#2F6F4E" },
    { id: "dia_a_dia", nome: "Dia a dia", lado: "saida", cor: "#E0A100" },
    { id: "oficiais", nome: "Impostos e boletos", lado: "saida", cor: "#8C5A3C" },
    { id: "investimentos", nome: "Investimentos e outros bancos", lado: "saida", cor: "#3D5A80" },
    { id: "outros", nome: "Outros", lado: "saida", cor: "#8A97A0" }
  ];
  const COR = Object.fromEntries(FAMILIAS.map((f) => [f.id, f.cor]));

  const RECORRENTES = [
    { nome: "Porto Seguro Vida", papel: "assinatura", cor: "#2F6F4E" },
    { nome: "VGBL", papel: "assinatura", cor: "#7DAB8E" },
    { nome: "Claro", papel: "assinatura", cor: "#0E4A57" },
    { nome: "Vivo", papel: "assinatura", cor: "#5BA3B5" },
    { nome: "Telefônica", papel: "assinatura", cor: "#163A44" },
    { nome: "Conselho profissional", papel: "assinatura", cor: "#9C3B24" },
    { nome: "Financiamento imobiliário", papel: "conta_fixa", cor: "#E27A2E" },
    { nome: "Ciranda", papel: "conta_fixa", cor: "#C44536" },
    { nome: "Condomínio Verana", papel: "conta_fixa", cor: "#C0641C" },
    { nome: "Energia elétrica", papel: "conta_fixa", cor: "#C9A227" },
    { nome: "Prefeitura / IPTU", papel: "conta_fixa", cor: "#8C5A3C" },
    { nome: "Boleto recorrente", papel: "conta_fixa", cor: "#6B4C9A" },
    { nome: "Compra de USDC", papel: "conta_fixa", cor: "#3D5A80" }
  ];

  const ABERTURA = [
    ["Alimentação", "#E0A100"],
    ["Transporte", "#3D5A80"],
    ["Saúde", "#C44536"],
    ["Compras", "#6B4C9A"],
    ["Lazer", "#E27A2E"],
    ["Viagem", "#2A9D8F"],
    ["Educação", "#0E4A57"],
    ["Outros", "#8A97A0"]
  ];

  const anim = { timer: 0, index: 0, playing: false };
  const reduzido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let edits = carregar();

  function vazio() {
    return { lancamentos: {}, apelidos: {}, notasNome: {}, notasMes: {}, black: {} };
  }

  function carregar() {
    try {
      const salvo = JSON.parse(localStorage.getItem(STORE) || "null");
      if (!salvo || typeof salvo !== "object") return vazio();
      return Object.assign(vazio(), salvo);
    } catch {
      return vazio();
    }
  }

  function save() {
    localStorage.setItem(STORE, JSON.stringify(edits));
    const el = document.getElementById("status-edicao");
    if (el) el.textContent = "Anotações salvas neste navegador.";
  }

  function esc(s) {
    return String(s ?? "").replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
    }[c]));
  }

  function brl(n) {
    const v = Number(n) || 0;
    return v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
  }

  function eixo(n) {
    const abs = Math.abs(n);
    const sinal = n < 0 ? "−" : "";
    if (abs >= 1000) return sinal + Math.round(abs / 1000).toLocaleString("pt-BR") + " mil";
    return sinal + Math.round(abs).toLocaleString("pt-BR");
  }

  function mesIdx(ym) { return Number(ym.slice(5)) - 1; }
  function mesLongo(ym) {
    const extra = ym === "2026-09" ? " (até o dia 25)" : "";
    return MES_NOME[mesIdx(ym)] + extra;
  }
  function mesCurto(ym) { return MES_CURTO[mesIdx(ym)] + (ym === "2026-09" ? "*" : ""); }

  function fimMes(ym) {
    if (ym === "2026-09") return "2026-09-25";
    const [y, m] = ym.split("-").map(Number);
    const dia = new Date(y, m, 0).getDate();
    return ym + "-" + String(dia).padStart(2, "0");
  }

  function diaSemana(iso) {
    const [y, m, d] = iso.split("-").map(Number);
    return new Date(y, m - 1, d).getDay();
  }

  function parseNum(s) {
    const texto = String(s ?? "").trim();
    if (!texto) return 0;
    const normal = texto.includes(",") ? texto.replace(/\./g, "").replace(",", ".") : texto;
    const n = Number(normal);
    return Number.isFinite(n) ? n : 0;
  }

  function aplicar(tx) {
    const ed = edits.lancamentos[tx.id] || {};
    const setor = SETORES[ed.setor] ? ed.setor : tx.setor;
    const meta = SETORES[setor];
    const natureza = meta.natureza === "interna" ? "interna" : (tx.valor > 0 ? "entrada" : "saida");
    return {
      ...tx,
      setor,
      natureza,
      familia: meta.familia,
      nota: ed.nota || "",
      nome: edits.apelidos[tx.contraparte] || tx.contraparte,
      nomeOriginal: tx.contraparte
    };
  }

  function saldoNo(iso) {
    const ponto = D.saldoDiario.find((d) => d.data === iso);
    return ponto ? ponto.saldo : 0;
  }

  function modelo() {
    const txs = D.lancamentos.map(aplicar);
    const mes = {};
    MESES.forEach((ym) => {
      mes[ym] = {
        entradas: 0, saidas: 0, internaEnt: 0, internaSai: 0,
        entradaFamilia: {}, saidaFamilia: {},
        recorrentes: {},
        saldo: saldoNo(fimMes(ym)),
        salario: 0, aportes: 0, luisa: 0, outras: 0,
        cofrinho: 0, cdb: 0, tbi: 0,
        fatura: 0, tarifa: 0
      };
    });
    let entrou = 0, saiu = 0, salario = 0, aportes = 0, luisa = 0, fatura = 0;
    txs.forEach((tx) => {
      const row = mes[tx.data.slice(0, 7)];
      if (!row) return;
      if (tx.origem === "fatura_black") { row.fatura += -tx.valor; fatura += -tx.valor; }
      if (tx.origem === "tarifa_black") row.tarifa += -tx.valor;
      if (tx.setor === "cofrinho") row.cofrinho += tx.valor;
      if (tx.setor === "cdb") row.cdb += tx.valor;
      if (tx.setor === "tbi") row.tbi += tx.valor;
      if (tx.natureza === "interna") {
        if (tx.valor > 0) row.internaEnt += tx.valor;
        else row.internaSai += -tx.valor;
        return;
      }
      if (tx.valor > 0) {
        row.entradas += tx.valor;
        entrou += tx.valor;
        row.entradaFamilia[tx.familia] = (row.entradaFamilia[tx.familia] || 0) + tx.valor;
        if (tx.setor === "salario_priscila") { row.salario += tx.valor; salario += tx.valor; }
        else if (tx.setor === "aporte_priscila") { row.aportes += tx.valor; aportes += tx.valor; }
        else if (tx.setor === "salario_luisa") { row.luisa += tx.valor; luisa += tx.valor; }
        else row.outras += tx.valor;
      } else {
        const abs = -tx.valor;
        row.saidas += abs;
        saiu += abs;
        row.saidaFamilia[tx.familia] = (row.saidaFamilia[tx.familia] || 0) + abs;
        if (tx.papel) row.recorrentes[tx.nomeOriginal] = (row.recorrentes[tx.nomeOriginal] || 0) + abs;
      }
    });
    return { txs, mes, entrou, saiu, salario, aportes, luisa, fatura };
  }

  function legenda(id, itens) {
    document.getElementById(id).innerHTML = itens.map((item) =>
      `<span><i style="background:${item.cor}"></i>${esc(item.nome)}</span>`
    ).join("");
  }

  function svgAbrir(w, h, rotulo) {
    return `<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(rotulo)}">`;
  }

  function desenharTotais(m) {
    const incluir = document.getElementById("toggle-internas").checked;
    const ent = MESES.map((ym) => m.mes[ym].entradas + (incluir ? m.mes[ym].internaEnt : 0));
    const sai = MESES.map((ym) => m.mes[ym].saidas + (incluir ? m.mes[ym].internaSai : 0));
    const saldos = MESES.map((ym) => m.mes[ym].saldo);
    const W = 920, H = 390;
    const pad = { l: 62, r: 62, t: 16, b: 36 };
    const iw = W - pad.l - pad.r, ih = H - pad.t - pad.b;
    const maxBar = Math.max(1, ...ent, ...sai);
    const minS = Math.min(...saldos), maxS = Math.max(...saldos);
    const yBar = (v) => pad.t + ih - (v / maxBar) * ih;
    const ySaldo = (v) => pad.t + ih - ((v - minS) / (maxS - minS || 1)) * ih;
    const gw = iw / MESES.length;
    let barras = "";
    let linha = "";
    MESES.forEach((ym, i) => {
      const x = pad.l + i * gw + gw / 2;
      const hE = (ent[i] / maxBar) * ih;
      const hS = (sai[i] / maxBar) * ih;
      barras += `<rect x="${(x - gw * 0.32).toFixed(1)}" y="${yBar(ent[i]).toFixed(1)}" width="${(gw * 0.26).toFixed(1)}" height="${hE.toFixed(1)}" fill="#1D6B45"><title>${esc(mesLongo(ym))}: entrou ${brl(ent[i])}</title></rect>`;
      barras += `<rect x="${(x + gw * 0.04).toFixed(1)}" y="${yBar(sai[i]).toFixed(1)}" width="${(gw * 0.26).toFixed(1)}" height="${hS.toFixed(1)}" fill="#E27A2E"><title>${esc(mesLongo(ym))}: saiu ${brl(sai[i])}</title></rect>`;
      const px = x.toFixed(1), py = ySaldo(saldos[i]).toFixed(1);
      linha += (i ? "L" : "M") + px + " " + py + " ";
      barras += `<circle cx="${px}" cy="${py}" r="3.5" fill="#0E4A57"><title>Saldo ${brl(saldos[i])}</title></circle>`;
      barras += `<text x="${px}" y="${H - 14}" text-anchor="middle" font-size="12" fill="#5A6B78">${mesCurto(ym)}</text>`;
    });
    let grades = "";
    [0, 0.5, 1].forEach((p) => {
      const y = (pad.t + ih - p * ih).toFixed(1);
      grades += `<line x1="${pad.l}" y1="${y}" x2="${W - pad.r}" y2="${y}" stroke="#E4EEEE"/>`;
      grades += `<text x="${pad.l - 8}" y="${Number(y) + 4}" text-anchor="end" font-size="11" fill="#5A6B78">${eixo(maxBar * p)}</text>`;
      const saldoTick = minS + (maxS - minS) * p;
      grades += `<text x="${W - pad.r + 8}" y="${Number(y) + 4}" font-size="11" fill="#0E4A57">${eixo(saldoTick)}</text>`;
    });
    document.getElementById("chart-totais").innerHTML = svgAbrir(W, H, "Entradas e saídas por mês em 2026") +
      grades + barras + `<path d="${linha}" fill="none" stroke="#0E4A57" stroke-width="2"/>` + "</svg>";
    legenda("legenda-totais", [
      { cor: "#1D6B45", nome: "Entradas" },
      { cor: "#E27A2E", nome: "Saídas" },
      { cor: "#0E4A57", nome: "Saldo no fim do mês (escala da direita)" }
    ]);
    const te = ent.reduce((a, b) => a + b, 0);
    const ts = sai.reduce((a, b) => a + b, 0);
    document.getElementById("nota-totais").textContent = incluir
      ? `Somando também cofrinho, CDB e a mesma conta: entrou ${brl(te)} e saiu ${brl(ts)}.`
      : `No recorte de verdade: entrou ${brl(te)} e saiu ${brl(ts)}. Resultado ${brl(te - ts)}.`;
  }

  function desenharFluxo(m) {
    const entradas = FAMILIAS.filter((f) => f.lado === "entrada");
    const saidas = FAMILIAS.filter((f) => f.lado === "saida");
    const pilhaE = MESES.map((ym) => entradas.reduce((s, f) => s + (m.mes[ym].entradaFamilia[f.id] || 0), 0));
    const pilhaS = MESES.map((ym) => saidas.reduce((s, f) => s + (m.mes[ym].saidaFamilia[f.id] || 0), 0));
    const max = Math.max(1, ...pilhaE, ...pilhaS);
    const W = 920, H = 460;
    const pad = { l: 62, r: 16, t: 16, b: 36 };
    const iw = W - pad.l - pad.r, ih = H - pad.t - pad.b;
    const mid = pad.t + ih / 2;
    const gw = iw / MESES.length;
    const bw = gw * 0.62;
    let formas = "";
    let grades = "";
    [1, 0.5, 0].forEach((p) => {
      const y = mid - (p * ih) / 2;
      grades += `<line x1="${pad.l}" y1="${y.toFixed(1)}" x2="${W - pad.r}" y2="${y.toFixed(1)}" stroke="${p === 0 ? "#0E4A57" : "#E4EEEE"}"/>`;
      grades += `<text x="${pad.l - 8}" y="${y + 4}" text-anchor="end" font-size="11" fill="#5A6B78">${eixo(max * p)}</text>`;
      if (p) {
        const y2 = mid + (p * ih) / 2;
        grades += `<line x1="${pad.l}" y1="${y2.toFixed(1)}" x2="${W - pad.r}" y2="${y2.toFixed(1)}" stroke="#E4EEEE"/>`;
        grades += `<text x="${pad.l - 8}" y="${y2 + 4}" text-anchor="end" font-size="11" fill="#5A6B78">${eixo(max * p)}</text>`;
      }
    });
    MESES.forEach((ym, i) => {
      const x = pad.l + i * gw + (gw - bw) / 2;
      let y = mid;
      entradas.forEach((f) => {
        const v = m.mes[ym].entradaFamilia[f.id] || 0;
        if (!v) return;
        const h = (v / max) * (ih / 2);
        y -= h;
        formas += `<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${bw.toFixed(1)}" height="${h.toFixed(1)}" fill="${f.cor}"><title>${esc(mesLongo(ym))} · ${esc(f.nome)}: ${brl(v)}</title></rect>`;
      });
      y = mid;
      saidas.forEach((f) => {
        const v = m.mes[ym].saidaFamilia[f.id] || 0;
        if (!v) return;
        const h = (v / max) * (ih / 2);
        formas += `<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${bw.toFixed(1)}" height="${h.toFixed(1)}" fill="${f.cor}"><title>${esc(mesLongo(ym))} · ${esc(f.nome)}: ${brl(v)}</title></rect>`;
        y += h;
      });
      formas += `<text x="${(x + bw / 2).toFixed(1)}" y="${H - 14}" text-anchor="middle" font-size="12" fill="#5A6B78">${mesCurto(ym)}</text>`;
    });
    document.getElementById("chart-fluxo").innerHTML = svgAbrir(W, H, "Entradas e saídas especificadas por mês") + grades + formas + "</svg>";
    legenda("legenda-fluxo", FAMILIAS);
  }

  function desenharDestinos(m) {
    const mapa = new Map();
    m.txs.forEach((tx) => {
      if (tx.natureza !== "saida") return;
      const atual = mapa.get(tx.nomeOriginal) || { nome: tx.nome, valor: 0 };
      atual.valor += -tx.valor;
      atual.nome = tx.nome;
      mapa.set(tx.nomeOriginal, atual);
    });
    const top = [...mapa.values()].sort((a, b) => b.valor - a.valor).slice(0, 8);
    const max = top[0] ? top[0].valor : 1;
    const W = 920, H = 36 + top.length * 36;
    let body = "";
    top.forEach((item, i) => {
      const y = 18 + i * 36;
      const w = Math.max(2, (item.valor / max) * 620);
      body += `<text x="210" y="${y + 16}" text-anchor="end" font-size="13" fill="#0E4A57">${esc(item.nome)}</text>`;
      body += `<rect x="222" y="${y}" width="${w.toFixed(1)}" height="22" fill="#E27A2E"><title>${esc(item.nome)}: ${brl(item.valor)}</title></rect>`;
      body += `<text x="${(230 + w).toFixed(1)}" y="${y + 16}" font-size="13" fill="#24383d">${esc(brl(item.valor))}</text>`;
    });
    document.getElementById("chart-destinos").innerHTML = svgAbrir(W, H, "Maiores saídas por destino") + body + "</svg>";
  }

  function desenharAssinaturas(m) {
    const soAssinatura = document.getElementById("toggle-assinaturas").checked;
    const series = RECORRENTES.filter((r) => !soAssinatura || r.papel === "assinatura");
    const totais = MESES.map((ym) => series.reduce((s, r) => s + (m.mes[ym].recorrentes[r.nome] || 0), 0));
    const max = Math.max(1, ...totais);
    const W = 920, H = 390;
    const pad = { l: 62, r: 16, t: 16, b: 36 };
    const iw = W - pad.l - pad.r, ih = H - pad.t - pad.b;
    const gw = iw / MESES.length, bw = gw * 0.62;
    let grades = "", formas = "";
    [0, 0.5, 1].forEach((p) => {
      const y = pad.t + ih - p * ih;
      grades += `<line x1="${pad.l}" y1="${y}" x2="${W - pad.r}" y2="${y}" stroke="#E4EEEE"/>`;
      grades += `<text x="${pad.l - 8}" y="${y + 4}" text-anchor="end" font-size="11" fill="#5A6B78">${eixo(max * p)}</text>`;
    });
    MESES.forEach((ym, i) => {
      const x = pad.l + i * gw + (gw - bw) / 2;
      let y = pad.t + ih;
      series.forEach((r) => {
        const v = m.mes[ym].recorrentes[r.nome] || 0;
        if (!v) return;
        const h = (v / max) * ih;
        y -= h;
        formas += `<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${bw.toFixed(1)}" height="${Math.max(h, 0.5).toFixed(1)}" fill="${r.cor}"><title>${esc(mesLongo(ym))} · ${esc(r.nome)}: ${brl(v)}</title></rect>`;
      });
      formas += `<text x="${(x + bw / 2).toFixed(1)}" y="${H - 14}" text-anchor="middle" font-size="12" fill="#5A6B78">${mesCurto(ym)}</text>`;
    });
    document.getElementById("chart-assinaturas").innerHTML = svgAbrir(W, H, "Assinaturas e contas recorrentes por mês") + grades + formas + "</svg>";
    legenda("legenda-assinaturas", series);
  }

  function fatia(cx, cy, r, a0, a1, cor, titulo) {
    const grande = a1 - a0 > Math.PI ? 1 : 0;
    const p = (a) => [cx + r * Math.cos(a), cy + r * Math.sin(a)];
    const [x0, y0] = p(a0);
    const [x1, y1] = p(a1);
    return `<path d="M ${x0} ${y0} A ${r} ${r} 0 ${grande} 1 ${x1} ${y1}" fill="none" stroke="${cor}" stroke-width="34"><title>${esc(titulo)}</title></path>`;
  }

  function donut(partes, centro, rotulo) {
    const total = partes.reduce((s, p) => s + p.valor, 0);
    const W = 260, H = 240, cx = 130, cy = 112, r = 72;
    if (total <= 0) {
      return svgAbrir(W, H, rotulo) + `<text x="${cx}" y="${cy}" text-anchor="middle" font-size="13" fill="#5A6B78">Sem valor</text></svg>`;
    }
    let ang = -Math.PI / 2;
    let paths = "";
    if (partes.length === 1 || partes.some((p) => p.valor / total > 0.999)) {
      const unico = partes.find((p) => p.valor / total > 0.999) || partes[0];
      paths = `<circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${unico.cor}" stroke-width="34"><title>${esc(unico.nome)}: ${brl(unico.valor)}</title></circle>`;
    } else {
      partes.forEach((p) => {
        if (p.valor <= 0) return;
        const passo = (p.valor / total) * Math.PI * 2;
        const folga = 0.03;
        paths += fatia(cx, cy, r, ang + folga / 2, ang + passo - folga / 2, p.cor, `${p.nome}: ${brl(p.valor)}`);
        ang += passo;
      });
    }
    paths += `<text x="${cx}" y="${cy - 4}" text-anchor="middle" font-size="15" font-weight="700" fill="#0E4A57">${esc(centro)}</text>`;
    paths += `<text x="${cx}" y="${cy + 16}" text-anchor="middle" font-size="11" fill="#5A6B78">${esc(brl(total))}</text>`;
    return svgAbrir(W, H, rotulo) + paths + "</svg>";
  }

  function desenharSetores(m) {
    const acc = {};
    m.txs.forEach((tx) => {
      if (tx.natureza !== "saida") return;
      acc[tx.familia] = (acc[tx.familia] || 0) + -tx.valor;
    });
    const partes = FAMILIAS.filter((f) => f.lado === "saida" && acc[f.id])
      .map((f) => ({ nome: f.nome, cor: f.cor, valor: acc[f.id] }))
      .sort((a, b) => b.valor - a.valor);
    const total = partes.reduce((s, p) => s + p.valor, 0);
    document.getElementById("chart-setores").innerHTML = donut(partes, "saídas", "Setores das saídas da conta em 2026");
    document.getElementById("lista-setores").innerHTML = partes.map((p) =>
      `<li><i style="background:${p.cor};width:10px;height:10px;display:inline-block"></i><span>${esc(p.nome)}</span><span class="num">${esc(brl(p.valor))}</span><span class="num">${Math.round(100 * p.valor / total)}%</span></li>`
    ).join("");
    const [a, b, c] = partes;
    document.getElementById("leitura-setores").textContent = a
      ? `O maior bloco é ${a.nome}, ${brl(a.valor)} (${Math.round(100 * a.valor / total)}% do que saiu). Depois vêm ${b ? b.nome : "—"} e ${c ? c.nome : "—"}.`
      : "";
  }

  function desenharBlack(m) {
    const fat = MESES.map((ym) => m.mes[ym].fatura);
    const tar = MESES.map((ym) => m.mes[ym].tarifa);
    const max = Math.max(1, ...MESES.map((_, i) => fat[i] + tar[i]));
    const W = 920, H = 320;
    const pad = { l: 62, r: 16, t: 16, b: 36 };
    const iw = W - pad.l - pad.r, ih = H - pad.t - pad.b;
    const gw = iw / MESES.length, bw = gw * 0.55;
    let grades = "", formas = "";
    [0, 0.5, 1].forEach((p) => {
      const y = pad.t + ih - p * ih;
      grades += `<line x1="${pad.l}" y1="${y}" x2="${W - pad.r}" y2="${y}" stroke="#E4EEEE"/>`;
      grades += `<text x="${pad.l - 8}" y="${y + 4}" text-anchor="end" font-size="11" fill="#5A6B78">${eixo(max * p)}</text>`;
    });
    const faturas = m.txs.filter((tx) => tx.origem === "fatura_black").sort((a, b) => a.data.localeCompare(b.data));
    const dias = faturas.map((tx) => Number(tx.data.slice(8)));
    MESES.forEach((ym, i) => {
      const x = pad.l + i * gw + (gw - bw) / 2;
      const hF = (fat[i] / max) * ih;
      const hT = (tar[i] / max) * ih;
      const yF = pad.t + ih - hF - hT;
      formas += `<rect x="${x.toFixed(1)}" y="${(yF + hT).toFixed(1)}" width="${bw.toFixed(1)}" height="${hF.toFixed(1)}" fill="#1A1A1A"><title>${esc(mesLongo(ym))}: fatura ${brl(fat[i])}</title></rect>`;
      if (hT) formas += `<rect x="${x.toFixed(1)}" y="${yF.toFixed(1)}" width="${bw.toFixed(1)}" height="${hT.toFixed(1)}" fill="#8A97A0"><title>Tarifa ${brl(tar[i])}</title></rect>`;
      formas += `<text x="${(x + bw / 2).toFixed(1)}" y="${H - 14}" text-anchor="middle" font-size="12" fill="#5A6B78">${mesCurto(ym)}</text>`;
    });
    document.getElementById("chart-black").innerHTML = svgAbrir(W, H, "Fatura do Cartão Black por mês") + grades + formas + "</svg>";
    legenda("legenda-black", [
      { cor: "#1A1A1A", nome: "Fatura" },
      { cor: "#8A97A0", nome: "Tarifa Personnalité" }
    ]);
    const freq = {};
    dias.forEach((d) => { freq[d] = (freq[d] || 0) + 1; });
    const ordem = Object.entries(freq).sort((a, b) => b[1] - a[1] || Number(a[0]) - Number(b[0]));
    const lista = dias.map((d) => "dia " + d).join(", ");
    document.getElementById("leitura-black").textContent =
      `A fatura foi debitada em ${lista}. O dia que mais se repete é o ${ordem[0] ? ordem[0][0] : "—"}. Esse é o dia em que o banco tira o total da fatura, não o dia de cada compra — o extrato não traz os lançamentos de dentro do cartão.`;
  }

  function valoresBlack(ym, m) {
    const salvo = edits.black[ym] || {};
    return ABERTURA.map(([nome, cor]) => ({ nome, cor, valor: Math.max(0, Number(salvo[nome]) || 0) }));
  }

  function desenharAbertura(m) {
    const sel = document.getElementById("black-mes");
    const ym = sel.value || MESES[0];
    const partes = valoresBlack(ym, m);
    const soma = partes.reduce((s, p) => s + p.valor, 0);
    const fatura = m.mes[ym].fatura;
    const resto = fatura - soma;
    let plot = partes.filter((p) => p.valor > 0);
    if (resto > 0.009) plot = plot.concat([{ nome: "Ainda não aberto", cor: "#1A1A1A", valor: resto }]);
    if (!plot.length) plot = [{ nome: "Sem fatura neste mês", cor: "#E4EEEE", valor: 1 }];
    document.getElementById("chart-black-split").innerHTML = donut(plot, MES_CURTO[mesIdx(ym)], "Abertura da fatura Black de " + mesLongo(ym));
    const box = document.getElementById("black-resto");
    if (resto < -0.009) {
      box.className = "resto alerta";
      box.textContent = `A soma passou da fatura em ${brl(-resto)}. A fatura deste mês é ${brl(fatura)}.`;
    } else if (soma <= 0) {
      box.className = "resto";
      box.textContent = `Fatura de ${brl(fatura)} ainda fechada. Distribua o valor se quiser ver os setores.`;
    } else {
      box.className = "resto";
      box.textContent = `Falta abrir ${brl(Math.max(0, resto))} de ${brl(fatura)}.`;
    }
  }

  function montarFormBlack(m) {
    const sel = document.getElementById("black-mes");
    const ym = sel.value || MESES[0];
    const salvo = edits.black[ym] || {};
    const foco = document.activeElement && document.getElementById("black-form").contains(document.activeElement);
    if (foco) {
      desenharAbertura(m);
      return;
    }
    document.getElementById("black-form").innerHTML = ABERTURA.map(([nome]) => {
      const val = salvo[nome] ? String(salvo[nome]).replace(".", ",") : "";
      return `<label>${esc(nome)}<input type="text" inputmode="decimal" data-black="${esc(nome)}" value="${esc(val)}" placeholder="0"></label>`;
    }).join("");
    desenharAbertura(m);
  }

  function gastosPorDia(m, semBlack) {
    const dias = Array(32).fill(0);
    const semana = Array(7).fill(0);
    m.txs.forEach((tx) => {
      if (tx.natureza !== "saida") return;
      if (semBlack && (tx.origem === "fatura_black" || tx.origem === "tarifa_black")) return;
      const dia = Number(tx.data.slice(8));
      dias[dia] += -tx.valor;
      semana[diaSemana(tx.data)] += -tx.valor;
    });
    return { dias, semana };
  }

  function topDias(dias, n) {
    return dias.map((v, i) => ({ dia: i, v })).filter((d) => d.dia >= 1).sort((a, b) => b.v - a.v).slice(0, n);
  }

  function desenharDias(m) {
    const semBlack = document.getElementById("toggle-sem-black").checked;
    const com = gastosPorDia(m, false);
    const sem = gastosPorDia(m, true);
    const uso = semBlack ? sem : com;
    const max = Math.max(1, ...uso.dias);
    const W = 920, H = 250;
    const pad = { l: 48, r: 10, t: 12, b: 28 };
    const iw = W - pad.l - pad.r, ih = H - pad.t - pad.b;
    const gw = iw / 31;
    let body = "";
    for (let dia = 1; dia <= 31; dia++) {
      const h = (uso.dias[dia] / max) * ih;
      const x = pad.l + (dia - 1) * gw;
      body += `<rect x="${x.toFixed(1)}" y="${(pad.t + ih - h).toFixed(1)}" width="${Math.max(gw - 3, 1).toFixed(1)}" height="${h.toFixed(1)}" fill="${semBlack ? "#0E4A57" : "#E27A2E"}"><title>Dia ${dia}: ${brl(uso.dias[dia])}</title></rect>`;
      body += `<text x="${(x + gw / 2).toFixed(1)}" y="${H - 10}" text-anchor="middle" font-size="10" fill="#5A6B78">${dia}</text>`;
    }
    document.getElementById("chart-dias").innerHTML = svgAbrir(W, H, "Gasto por dia do mês") + body + "</svg>";

    const maxS = Math.max(1, ...uso.semana);
    let semSvg = "";
    SEMANA.forEach((item, i) => {
      const w = (uso.semana[item.d] / maxS) * 640;
      const y = 16 + i * 32;
      semSvg += `<text x="70" y="${y + 14}" text-anchor="end" font-size="13" fill="#0E4A57">${item.nome}</text>`;
      semSvg += `<rect x="82" y="${y}" width="${w.toFixed(1)}" height="18" fill="#0E4A57"><title>${item.nome}: ${brl(uso.semana[item.d])}</title></rect>`;
    });
    document.getElementById("chart-semana").innerHTML = svgAbrir(760, 16 + SEMANA.length * 32, "Gasto por dia da semana") + semSvg + "</svg>";

    const rotuloDia = (lista, base) => lista.map((d) => {
      const nome = principalDoDia(m, d.dia, base);
      return `dia ${d.dia} (${brl(d.v)}${nome ? ", sobretudo " + nome : ""})`;
    }).join(", ");
    const a = rotuloDia(topDias(com.dias, 3), false);
    const b = rotuloDia(topDias(sem.dias, 3), true);
    const maiorSemana = SEMANA.slice().sort((p, q) => uso.semana[q.d] - uso.semana[p.d])[0];
    document.getElementById("leitura-dias").textContent = semBlack
      ? `Sem a fatura do Black, os dias com mais saída são ${b}. O dia da semana mais pesado neste recorte é ${maiorSemana.nome}.`
      : `Somando tudo, os dias com mais saída são ${a}. Sem a fatura do Black, a ordem muda para ${b}. O dia da semana mais pesado, neste recorte, é ${maiorSemana.nome}.`;

    const maxCal = Math.max(1, ...Array.from({ length: 31 }, (_, i) => {
      let pico = 0;
      MESES.forEach((ym) => { pico = Math.max(pico, gastoDoDia(m, ym, i + 1, semBlack)); });
      return pico;
    }));
    let cal = "<table class='cal'><tr><th></th>";
    for (let dia = 1; dia <= 31; dia++) cal += `<th>${dia}</th>`;
    cal += "</tr>";
    MESES.forEach((ym) => {
      cal += `<tr><th>${mesCurto(ym)}</th>`;
      for (let dia = 1; dia <= 31; dia++) {
        const [y, mo] = ym.split("-").map(Number);
        const existe = dia <= new Date(y, mo, 0).getDate() && `${ym}-${String(dia).padStart(2, "0")}` <= "2026-09-25";
        if (!existe) { cal += "<td></td>"; continue; }
        const v = gastoDoDia(m, ym, dia, semBlack);
        cal += `<td title="${esc(mesLongo(ym))} dia ${dia}: ${esc(brl(v))}" style="background:${corCalor(v, maxCal)}"></td>`;
      }
      cal += "</tr>";
    });
    cal += "</table>";
    document.getElementById("chart-cal").innerHTML = cal;
  }

  function principalDoDia(m, dia, semBlack) {
    const mapa = new Map();
    m.txs.forEach((tx) => {
      if (Number(tx.data.slice(8)) !== dia || tx.natureza !== "saida") return;
      if (semBlack && (tx.origem === "fatura_black" || tx.origem === "tarifa_black")) return;
      mapa.set(tx.nome, (mapa.get(tx.nome) || 0) + -tx.valor);
    });
    let melhor = "", valor = 0;
    mapa.forEach((v, nome) => { if (v > valor) { valor = v; melhor = nome; } });
    return melhor;
  }

  function gastoDoDia(m, ym, dia, semBlack) {
    const iso = ym + "-" + String(dia).padStart(2, "0");
    let total = 0;
    m.txs.forEach((tx) => {
      if (tx.data !== iso || tx.natureza !== "saida") return;
      if (semBlack && (tx.origem === "fatura_black" || tx.origem === "tarifa_black")) return;
      total += -tx.valor;
    });
    return total;
  }

  function corCalor(v, max) {
    if (v <= 0) return "#F4F1EA";
    const t = Math.min(1, v / max);
    return misturar(t < 0.55 ? ["#F8E7D4", "#E27A2E", t / 0.55] : ["#E27A2E", "#6A2E12", (t - 0.55) / 0.45]);
  }

  function misturar([a, b, t]) {
    const pa = [1, 3, 5].map((i) => parseInt(a.slice(i, i + 2), 16));
    const pb = [1, 3, 5].map((i) => parseInt(b.slice(i, i + 2), 16));
    const hex = pa.map((c, i) => Math.round(c + (pb[i] - c) * t).toString(16).padStart(2, "0"));
    return "#" + hex.join("");
  }

  function escalaAnim(m) {
    return Math.max(1, ...MESES.map((ym) => Math.max(m.mes[ym].entradas, m.mes[ym].saidas)));
  }

  function desenharLinha(ate) {
    const vals = D.saldoDiario.map((d) => d.saldo);
    const min = Math.min(...vals), max = Math.max(...vals);
    const W = 860, H = 120, pad = 10;
    const x = (i) => pad + (i / (D.saldoDiario.length - 1)) * (W - pad * 2);
    const y = (v) => pad + (1 - (v - min) / (max - min || 1)) * (H - pad * 2);
    let cheia = "", forte = "";
    D.saldoDiario.forEach((d, i) => {
      const cmd = (i ? "L" : "M") + x(i).toFixed(1) + " " + y(d.saldo).toFixed(1) + " ";
      cheia += cmd;
      if (d.data <= ate) forte += cmd;
    });
    document.getElementById("anim-linha").innerHTML = svgAbrir(W, H, "Saldo da conta ao longo de 2026") +
      `<path d="${cheia}" fill="none" stroke="rgba(255,255,255,.25)" stroke-width="2"/>` +
      `<path d="${forte}" fill="none" stroke="#E27A2E" stroke-width="2.5"/>` + "</svg>";
  }

  function mostrarMes(indice, base) {
    const m = base || modelo();
    const i = Math.max(0, Math.min(MESES.length - 1, indice));
    anim.index = i;
    const ym = MESES[i];
    const row = m.mes[ym];
    const max = escalaAnim(m);
    document.getElementById("anim-mes").textContent = mesLongo(ym);
    document.getElementById("anim-scrub").value = String(i);
    const barraEnt = document.getElementById("anim-bar-ent");
    const barraSai = document.getElementById("anim-bar-sai");
    const largura = (v) => Math.max(2, (v / max) * 100) + "%";
    if (reduzido) {
      barraEnt.style.width = largura(row.entradas);
      barraSai.style.width = largura(row.saidas);
    } else {
      barraEnt.style.width = "0%";
      barraSai.style.width = "0%";
      requestAnimationFrame(() => {
        barraEnt.style.transition = "width .7s ease";
        barraSai.style.transition = "width .7s ease";
        barraEnt.style.width = largura(row.entradas);
        barraSai.style.width = largura(row.saidas);
      });
    }
    document.getElementById("anim-entradas").textContent = brl(row.entradas);
    document.getElementById("anim-saidas").textContent = brl(row.saidas);
    const resultado = row.entradas - row.saidas;
    document.getElementById("anim-resultado").textContent = brl(resultado);
    document.getElementById("anim-saldo").textContent = brl(row.saldo);
    const eventos = m.txs.filter((tx) => tx.data.slice(0, 7) === ym && Math.abs(tx.valor) >= 1 && tx.setor !== "rendimento")
      .sort((a, b) => Math.abs(b.valor) - Math.abs(a.valor))
      .slice(0, 4);
    document.getElementById("anim-eventos").innerHTML = eventos.map((tx) =>
      `<li><span>${esc(tx.nome)}${tx.natureza === "interna" ? "<span class='tag-int'>entre contas</span>" : ""}</span><strong>${esc(brl(tx.valor))}</strong></li>`
    ).join("");
    desenharLinha(fimMes(ym));
    document.getElementById("anim-live").textContent =
      `${mesLongo(ym)}. Entrou ${brl(row.entradas)}. Saiu ${brl(row.saidas)}. Saldo ${brl(row.saldo)}.`;
  }

  function parar() {
    anim.playing = false;
    clearTimeout(anim.timer);
    document.getElementById("btn-play").textContent = "Reproduzir";
  }

  function reproduzir() {
    if (anim.playing) { parar(); return; }
    if (anim.index >= MESES.length - 1) anim.index = 0;
    anim.playing = true;
    document.getElementById("btn-play").textContent = "Pausar";
    passo();
  }

  function passo() {
    mostrarMes(anim.index);
    if (!anim.playing) return;
    if (anim.index >= MESES.length - 1) { parar(); return; }
    anim.timer = setTimeout(() => { anim.index += 1; passo(); }, 1700);
  }

  function tdNum(n, invertido) {
    const cls = n < -0.004 ? "neg" : n > 0.004 ? "pos" : "";
    return `<td class="num ${invertido ? "" : cls}">${esc(brl(n))}</td>`;
  }

  function desenharTabelas(m) {
    let html = `<table class="sheet"><thead><tr>
      <th>Mês</th><th class="num">Salário Priscila</th><th class="num">Pix/TED Priscila</th>
      <th class="num">Luísa McKinsey</th><th class="num">Outras entradas</th><th class="num">Saídas</th>
      <th class="num">Resultado</th><th class="num">Cofrinho, CDB, mesma conta</th><th class="num">Saldo</th><th>Nota</th>
    </tr></thead><tbody>`;
    const tot = { salario: 0, aportes: 0, luisa: 0, outras: 0, saidas: 0, interna: 0 };
    MESES.forEach((ym) => {
      const row = m.mes[ym];
      const resultado = row.entradas - row.saidas;
      const interna = row.cofrinho + row.cdb + row.tbi;
      tot.salario += row.salario; tot.aportes += row.aportes; tot.luisa += row.luisa;
      tot.outras += row.outras; tot.saidas += row.saidas; tot.interna += interna;
      html += `<tr><td>${esc(mesLongo(ym))}</td>${tdNum(row.salario)}${tdNum(row.aportes)}${tdNum(row.luisa)}${tdNum(row.outras)}<td class="num">${esc(brl(row.saidas))}</td>${tdNum(resultado)}${tdNum(interna)}${tdNum(row.saldo)}<td><span contenteditable="true" data-nota-mes="${ym}">${esc(edits.notasMes[ym] || "")}</span></td></tr>`;
    });
    html += `</tbody><tfoot><tr><td>Ano</td>${tdNum(tot.salario)}${tdNum(tot.aportes)}${tdNum(tot.luisa)}${tdNum(tot.outras)}<td class="num">${esc(brl(tot.saidas))}</td>${tdNum(tot.salario + tot.aportes + tot.luisa + tot.outras - tot.saidas)}${tdNum(tot.interna)}<td class="num">${esc(brl(D.saldoFinal))}</td><td></td></tr></tfoot></table>`;
    document.getElementById("tabela-mes").innerHTML = html;

    const minimo = Number(document.getElementById("f-min").value) || 0;
    const buscaNome = document.getElementById("f-nome").value.trim().toLocaleLowerCase("pt-BR");
    const grupos = new Map();
    m.txs.forEach((tx) => {
      const g = grupos.get(tx.nomeOriginal) || {
        original: tx.nomeOriginal, nome: tx.nome, setores: new Set(), n: 0, meses: new Set(), entrou: 0, saiu: 0
      };
      g.nome = tx.nome;
      g.setores.add(tx.setor);
      g.n += 1;
      g.meses.add(tx.data.slice(0, 7));
      if (tx.valor > 0) g.entrou += tx.valor;
      else g.saiu += -tx.valor;
      grupos.set(tx.nomeOriginal, g);
    });
    const linhas = [...grupos.values()]
      .filter((g) => g.entrou + g.saiu >= minimo)
      .filter((g) => !buscaNome || g.nome.toLocaleLowerCase("pt-BR").includes(buscaNome) || g.original.toLocaleLowerCase("pt-BR").includes(buscaNome))
      .sort((a, b) => (b.entrou + b.saiu) - (a.entrou + a.saiu));
    let quem = `<table class="sheet"><thead><tr>
      <th>Nome</th><th>Categoria</th><th class="num">Vezes</th><th class="num">Meses</th>
      <th class="num">Entrou</th><th class="num">Saiu</th><th>Nota</th>
    </tr></thead><tbody>`;
    linhas.forEach((g) => {
      const varios = g.setores.size > 1;
      const atual = varios ? "" : [...g.setores][0];
      quem += `<tr><td><span contenteditable="true" data-apelido="${esc(g.original)}">${esc(g.nome)}</span></td><td><select data-setor-nome="${esc(g.original)}">${opcoesSetor(atual, true)}</select></td><td class="num">${g.n}</td><td class="num">${g.meses.size}</td>${tdNum(g.entrou)}<td class="num">${esc(brl(g.saiu))}</td><td><span contenteditable="true" data-nota-nome="${esc(g.original)}">${esc(edits.notasNome[g.original] || "")}</span></td></tr>`;
    });
    quem += "</tbody></table>";
    document.getElementById("tabela-quem").innerHTML = quem;

    const fMes = document.getElementById("f-mes").value;
    const fSetor = document.getElementById("f-setor").value;
    const fTipo = document.getElementById("f-tipo").value;
    const fBusca = document.getElementById("f-busca").value.trim().toLocaleLowerCase("pt-BR");
    const esconder = document.getElementById("f-internas").checked;
    const visiveis = m.txs.filter((tx) => {
      if (fMes && tx.data.slice(0, 7) !== fMes) return false;
      if (fSetor && tx.setor !== fSetor) return false;
      if (fTipo && tx.natureza !== fTipo) return false;
      if (esconder && !fTipo && !fSetor && tx.natureza === "interna") return false;
      if (fBusca) {
        const bloco = (tx.desc + " " + tx.nome + " " + tx.nomeOriginal).toLocaleLowerCase("pt-BR");
        if (!bloco.includes(fBusca)) return false;
      }
      return true;
    }).slice().sort((a, b) => b.data.localeCompare(a.data) || b.valor - a.valor);
    document.getElementById("conta-lanc").textContent = `${visiveis.length} lançamentos nesta vista, de ${m.txs.length}.`;
    let lanc = `<table class="sheet"><thead><tr>
      <th>Data</th><th>Descrição</th><th>Nome</th><th>Categoria</th><th class="num">Valor</th><th>Nota</th>
    </tr></thead><tbody>`;
    visiveis.forEach((tx) => {
      const [y, mo, d] = tx.data.split("-");
      lanc += `<tr><td>${d}/${mo}/${y}</td><td>${esc(tx.desc)}</td><td>${esc(tx.nome)}</td><td><select data-setor-id="${esc(tx.id)}">${opcoesSetor(tx.setor, false)}</select></td>${tdNum(tx.valor)}<td><span contenteditable="true" data-nota-id="${esc(tx.id)}">${esc(tx.nota)}</span></td></tr>`;
    });
    lanc += "</tbody></table>";
    document.getElementById("tabela-lanc").innerHTML = lanc;
  }

  function opcoesSetor(atual, comOriginal) {
    const grupos = [
      ["Entradas", ["salario_priscila", "aporte_priscila", "salario_luisa", "outras_entradas", "estorno", "rendimento"]],
      ["Saídas", ["cartao_black", "moradia", "educacao", "pessoas", "para_priscila", "saude", "alimentacao", "transporte", "compras", "viagem", "lazer", "assinaturas", "impostos", "boletos", "investimentos", "transferencia_banco", "outros"]],
      ["Entre contas suas", ["cofrinho", "cdb", "tbi"]]
    ];
    let html = comOriginal
      ? `<option value="__original">Voltar à categoria do extrato</option><option value="" ${atual ? "" : "selected"} disabled>Várias categorias</option>`
      : "";
    grupos.forEach(([nome, ids]) => {
      html += `<optgroup label="${nome}">`;
      ids.forEach((id) => {
        html += `<option value="${id}" ${id === atual ? "selected" : ""}>${esc(SETORES[id].nome)}</option>`;
      });
      html += "</optgroup>";
    });
    return html;
  }

  function preencherFiltros() {
    const mes = document.getElementById("f-mes");
    MESES.forEach((ym) => {
      const o = document.createElement("option");
      o.value = ym;
      o.textContent = mesLongo(ym);
      mes.appendChild(o);
    });
    const setor = document.getElementById("f-setor");
    Object.entries(SETORES).forEach(([id, meta]) => {
      const o = document.createElement("option");
      o.value = id;
      o.textContent = meta.nome;
      setor.appendChild(o);
    });
    const black = document.getElementById("black-mes");
    MESES.forEach((ym) => {
      const o = document.createElement("option");
      o.value = ym;
      o.textContent = mesLongo(ym);
      black.appendChild(o);
    });
    black.value = "2026-09";
  }

  function kpis(m) {
    const por = (id, valor) => {
      const el = document.getElementById(id);
      el.textContent = brl(valor);
      el.dataset.valor = valor.toFixed(2);
    };
    por("kpi-entradas", m.entrou);
    por("kpi-saidas", m.saiu);
    por("kpi-resultado", m.entrou - m.saiu);
    por("kpi-saldo", D.saldoFinal);
    por("kpi-salario", m.salario);
    por("kpi-aportes", m.aportes);
    por("kpi-luisa", m.luisa);
    por("kpi-black", m.fatura);
    document.getElementById("kpi-saldo-ini").textContent = "em 31/12/2025 estava " + brl(D.saldoInicial);
    const temNota = Object.keys(edits.lancamentos).length || Object.keys(edits.apelidos).length || Object.keys(edits.notasMes).length || Object.keys(edits.notasNome).length || Object.keys(edits.black).length;
    document.getElementById("status-edicao").textContent = temNota
      ? "Anotações salvas neste navegador."
      : "Nada anotado ainda. Categoria, apelido e nota ficam só neste navegador.";
  }

  function render() {
    const y = window.scrollY;
    const m = modelo();
    kpis(m);
    desenharTotais(m);
    desenharFluxo(m);
    desenharDestinos(m);
    desenharAssinaturas(m);
    desenharSetores(m);
    desenharBlack(m);
    montarFormBlack(m);
    desenharDias(m);
    desenharTabelas(m);
    if (!anim.playing) mostrarMes(anim.index, m);
    window.scrollTo(0, y);
    window.__extrato = {
      entrou: m.entrou,
      saiu: m.saiu,
      salario: m.salario,
      aportes: m.aportes,
      luisa: m.luisa,
      fatura: m.fatura,
      saldo: D.saldoFinal,
      n: m.txs.length
    };
  }

  function csvSeguro(s) {
    const texto = String(s ?? "");
    const protegido = /^[=+\-@]/.test(texto) ? "'" + texto : texto;
    return `"${protegido.replace(/"/g, '""')}"`;
  }

  function baixar(nome, conteudo, tipo) {
    const blob = new Blob([conteudo], { type: tipo });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = nome;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(a.href);
  }

  let inputTimer = 0;

  document.body.addEventListener("change", (e) => {
    const t = e.target;
    if (t.id === "toggle-internas") { desenharTotais(modelo()); return; }
    if (t.id === "toggle-assinaturas") { desenharAssinaturas(modelo()); return; }
    if (t.id === "toggle-sem-black") { desenharDias(modelo()); return; }
    if (t.id === "black-mes") { montarFormBlack(modelo()); return; }
    if (t.dataset && t.dataset.setorId) {
      edits.lancamentos[t.dataset.setorId] = edits.lancamentos[t.dataset.setorId] || {};
      if (t.value === "__original") delete edits.lancamentos[t.dataset.setorId].setor;
      else edits.lancamentos[t.dataset.setorId].setor = t.value;
      save(); render(); return;
    }
    if (t.dataset && t.dataset.setorNome) {
      D.lancamentos.forEach((tx) => {
        if (tx.contraparte !== t.dataset.setorNome) return;
        edits.lancamentos[tx.id] = edits.lancamentos[tx.id] || {};
        if (t.value === "__original") delete edits.lancamentos[tx.id].setor;
        else if (t.value) edits.lancamentos[tx.id].setor = t.value;
      });
      save(); render(); return;
    }
    if (["f-min", "f-mes", "f-setor", "f-tipo", "f-internas"].includes(t.id)) render();
  });

  document.body.addEventListener("input", (e) => {
    const t = e.target;
    if (t.id === "f-nome" || t.id === "f-busca") {
      clearTimeout(inputTimer);
      inputTimer = setTimeout(render, 160);
    }
    if (t.dataset && t.dataset.black) {
      const ym = document.getElementById("black-mes").value;
      edits.black[ym] = edits.black[ym] || {};
      edits.black[ym][t.dataset.black] = parseNum(t.value);
      save();
      desenharAbertura(modelo());
    }
  });

  document.body.addEventListener("focusout", (e) => {
    const t = e.target;
    if (t.dataset && t.dataset.notaMes !== undefined) {
      edits.notasMes[t.dataset.notaMes] = t.textContent.trim();
      save();
    }
    if (t.dataset && t.dataset.notaNome !== undefined) {
      edits.notasNome[t.dataset.notaNome] = t.textContent.trim();
      save();
    }
    if (t.dataset && t.dataset.notaId !== undefined) {
      edits.lancamentos[t.dataset.notaId] = edits.lancamentos[t.dataset.notaId] || {};
      edits.lancamentos[t.dataset.notaId].nota = t.textContent.trim();
      save();
    }
    if (t.dataset && t.dataset.apelido !== undefined) {
      const nome = t.textContent.trim();
      if (nome && nome !== t.dataset.apelido) edits.apelidos[t.dataset.apelido] = nome;
      else delete edits.apelidos[t.dataset.apelido];
      save();
      render();
    }
  });

  document.body.addEventListener("paste", (e) => {
    if (!e.target.isContentEditable) return;
    e.preventDefault();
    const texto = (e.clipboardData || window.clipboardData).getData("text");
    document.execCommand("insertText", false, texto);
  });

  document.getElementById("btn-play").addEventListener("click", reproduzir);
  document.getElementById("anim-prev").addEventListener("click", () => { parar(); mostrarMes(anim.index - 1); });
  document.getElementById("anim-next").addEventListener("click", () => { parar(); mostrarMes(anim.index + 1); });
  document.getElementById("anim-scrub").addEventListener("input", (e) => { parar(); mostrarMes(Number(e.target.value)); });

  document.getElementById("btn-csv").addEventListener("click", () => {
    const m = modelo();
    const linhas = [["data", "descricao", "nome", "categoria", "valor", "nota"]];
    m.txs.forEach((tx) => linhas.push([tx.data, tx.desc, tx.nome, SETORES[tx.setor].nome, tx.valor.toFixed(2), tx.nota]));
    baixar("extrato-2026.csv", linhas.map((cols) => cols.map(csvSeguro).join(";")).join("\n"), "text/csv;charset=utf-8");
  });
  document.getElementById("btn-json").addEventListener("click", () => {
    baixar("anotacoes-extrato-2026.json", JSON.stringify(edits, null, 2), "application/json");
  });
  document.getElementById("btn-importar").addEventListener("click", () => document.getElementById("arquivo-json").click());
  document.getElementById("arquivo-json").addEventListener("change", async (e) => {
    const file = e.target.files && e.target.files[0];
    if (!file) return;
    try {
      const lido = JSON.parse(await file.text());
      if (!lido || typeof lido !== "object" || !lido.lancamentos) throw new Error("formato");
      edits = Object.assign(vazio(), lido);
      save();
      render();
    } catch {
      document.getElementById("status-edicao").textContent = "Não consegui ler esse arquivo de anotações.";
    }
    e.target.value = "";
  });
  document.getElementById("btn-reset").addEventListener("click", () => {
    if (!confirm("Apagar categorias, apelidos e notas salvas neste navegador?")) return;
    edits = vazio();
    localStorage.removeItem(STORE);
    render();
  });

  preencherFiltros();
  render();
  const params = new URLSearchParams(location.search);
  const pausa = reduzido || params.has("pausa");
  if (pausa) {
    parar();
    const pedido = Number(params.get("mes"));
    mostrarMes(Number.isFinite(pedido) && params.has("mes") ? pedido : (reduzido ? MESES.length - 1 : 0));
  } else {
    anim.playing = true;
    document.getElementById("btn-play").textContent = "Pausar";
    setTimeout(passo, 700);
  }
})();
