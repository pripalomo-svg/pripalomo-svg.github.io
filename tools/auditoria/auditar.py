#!/usr/bin/env python3
"""
Auditoria diária do site — compara cada página pública com as metas dos sites
mais bem acessados do mundo (Core Web Vitals, SEO on-page, acessibilidade básica,
peso e links). Só usa a biblioteca padrão.

Uso:
  python3 tools/auditoria/auditar.py                      # audita https://www.priscilapalomo.com
  python3 tools/auditoria/auditar.py --base http://localhost:8000
  python3 tools/auditoria/auditar.py --out relatorio.md --json relatorio.json

Saída: relatório Markdown (stdout ou --out) e, opcionalmente, JSON com os dados.
Código de saída 1 se houver falhas críticas (página fora do ar, link quebrado,
sem <title>, sem <h1>).
"""
import argparse, json, re, sys, time, urllib.request, urllib.error, urllib.parse
from html.parser import HTMLParser

PAGINAS = [
    "", "fobias.html", "pesquisa.html", "apresentacao.html", "blog.html",
    "cursos.html", "loja.html", "escada-segura.html",
]

# Metas inspiradas nos sites de referência (Google, Wikipedia, Apple, NYT):
METAS = {
    "html_kb_max": 120,          # HTML inicial enxuto
    "title_min": 30, "title_max": 65,
    "desc_min": 70, "desc_max": 160,
    "h1_exato": 1,
    "ttfb_ms_max": 800,          # tempo até o primeiro byte (CDN/estático)
    "img_sem_alt_max": 0,
    "links_quebrados_max": 0,
    "lighthouse_perf_min": 90, "lighthouse_seo_min": 95, "lighthouse_a11y_min": 95,
    "lcp_s_max": 2.5, "cls_max": 0.1, "inp_ms_max": 200,
}

class Coletor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""; self._in_title = False
        self.desc = ""; self.canonical = ""; self.viewport = False; self.lang = ""
        self.h1 = 0; self.imgs = 0; self.imgs_sem_alt = 0
        self.links = []; self.jsonld = False; self.og = 0; self.scripts_ext = 0
        self.lazy_imgs = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html": self.lang = a.get("lang", "")
        if tag == "title": self._in_title = True
        if tag == "meta":
            if a.get("name") == "description": self.desc = a.get("content", "")
            if a.get("name") == "viewport": self.viewport = True
            if (a.get("property") or "").startswith("og:"): self.og += 1
        if tag == "link" and a.get("rel") == "canonical": self.canonical = a.get("href", "")
        if tag == "h1": self.h1 += 1
        if tag == "img":
            self.imgs += 1
            if not a.get("alt") and a.get("alt") != "": self.imgs_sem_alt += 1
            if a.get("loading") == "lazy": self.lazy_imgs += 1
        if tag == "a" and a.get("href"): self.links.append(a["href"])
        if tag == "script":
            if a.get("type") == "application/ld+json": self.jsonld = True
            if a.get("src"): self.scripts_ext += 1
    def handle_endtag(self, tag):
        if tag == "title": self._in_title = False
    def handle_data(self, data):
        if self._in_title: self.title += data

def baixar(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "AuditoriaPriscila/1.0"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        primeiro = r.read(1); ttfb = (time.time() - t0) * 1000
        corpo = primeiro + r.read()
        return r.status, ttfb, corpo

def checar_link(url, cache):
    if url in cache: return cache[url]
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "AuditoriaPriscila/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r: ok = r.status < 400
    except urllib.error.HTTPError as e:
        ok = e.code < 400 or e.code in (403, 405, 999)  # alguns sites bloqueiam HEAD
    except Exception:
        ok = False
    cache[url] = ok
    return ok

def auditar(base, checar_externos=False):
    base = base.rstrip("/") + "/"
    cache = {}
    resultados = []; criticos = 0
    for p in PAGINAS:
        url = base + p
        item = {"pagina": p or "index.html", "url": url, "problemas": [], "avisos": []}
        try:
            status, ttfb, corpo = baixar(url)
        except Exception as e:
            item["problemas"].append(f"Fora do ar: {e}")
            criticos += 1; resultados.append(item); continue
        html = corpo.decode("utf-8", "replace")
        c = Coletor(); c.feed(html)
        kb = len(corpo) / 1024
        item.update({"status": status, "ttfb_ms": round(ttfb), "html_kb": round(kb, 1),
                     "title": c.title.strip(), "desc_len": len(c.desc), "h1": c.h1,
                     "imgs": c.imgs, "imgs_sem_alt": c.imgs_sem_alt, "jsonld": c.jsonld,
                     "og": c.og, "canonical": bool(c.canonical), "scripts_ext": c.scripts_ext})
        if not c.title: item["problemas"].append("Sem <title>"); criticos += 1
        elif not (METAS["title_min"] <= len(c.title.strip()) <= METAS["title_max"]):
            item["avisos"].append(f"Title com {len(c.title.strip())} caracteres (meta {METAS['title_min']}–{METAS['title_max']})")
        if not c.desc: item["problemas"].append("Sem meta description")
        elif not (METAS["desc_min"] <= len(c.desc) <= METAS["desc_max"]):
            item["avisos"].append(f"Description com {len(c.desc)} caracteres (meta {METAS['desc_min']}–{METAS['desc_max']})")
        if c.h1 != METAS["h1_exato"]:
            item["problemas"].append(f"{c.h1} <h1> (meta: 1)"); criticos += 1
        if not c.viewport: item["problemas"].append("Sem meta viewport")
        if not c.lang: item["avisos"].append("Sem atributo lang no <html>")
        if not c.canonical: item["avisos"].append("Sem link canonical")
        if c.og < 2: item["avisos"].append("Open Graph incompleto")
        if c.imgs_sem_alt > METAS["img_sem_alt_max"]: item["problemas"].append(f"{c.imgs_sem_alt} imagem(ns) sem alt")
        if kb > METAS["html_kb_max"]: item["avisos"].append(f"HTML com {kb:.0f} KB (meta ≤ {METAS['html_kb_max']} KB)")
        if ttfb > METAS["ttfb_ms_max"]: item["avisos"].append(f"TTFB {ttfb:.0f} ms (meta ≤ {METAS['ttfb_ms_max']} ms)")
        if p == "" and not c.jsonld: item["avisos"].append("Home sem dados estruturados (JSON-LD)")
        # links internos
        quebrados = []
        for h in set(c.links):
            if h.startswith(("#", "mailto:", "tel:", "javascript:")): continue
            alvo = urllib.parse.urljoin(url, h.split("#")[0])
            if alvo.startswith(base) or checar_externos:
                if alvo.startswith(base) or h.startswith("http"):
                    if not checar_link(alvo, cache): quebrados.append(h)
        if quebrados:
            item["problemas"].append("Links quebrados: " + ", ".join(sorted(quebrados)[:8])); criticos += 1
        item["links_quebrados"] = quebrados
        resultados.append(item)
    return resultados, criticos

def relatorio_md(base, resultados, criticos, lighthouse=None):
    linhas = [f"# Auditoria diária — {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}", "",
              f"Base: {base}  ", f"Problemas críticos: **{criticos}**", "",
              "## Metas de referência (sites mais acessados do mundo)", "",
              f"- Lighthouse: desempenho ≥ {METAS['lighthouse_perf_min']}, SEO ≥ {METAS['lighthouse_seo_min']}, acessibilidade ≥ {METAS['lighthouse_a11y_min']}",
              f"- Core Web Vitals: LCP ≤ {METAS['lcp_s_max']} s · CLS ≤ {METAS['cls_max']} · INP ≤ {METAS['inp_ms_max']} ms",
              f"- HTML inicial ≤ {METAS['html_kb_max']} KB · TTFB ≤ {METAS['ttfb_ms_max']} ms · 1 h1 por página · 0 imagens sem alt · 0 links quebrados", "",
              "## Páginas", "",
              "| Página | Status | TTFB | HTML | h1 | Imgs s/ alt | JSON-LD | Problemas | Avisos |", "|---|---|---|---|---|---|---|---|---|"]
    for r in resultados:
        linhas.append(f"| {r['pagina']} | {r.get('status','—')} | {r.get('ttfb_ms','—')} ms | {r.get('html_kb','—')} KB | {r.get('h1','—')} | {r.get('imgs_sem_alt','—')} | {'sim' if r.get('jsonld') else '—'} | {len(r['problemas'])} | {len(r['avisos'])} |")
    linhas.append("")
    for r in resultados:
        if r["problemas"] or r["avisos"]:
            linhas.append(f"### {r['pagina']}")
            for x in r["problemas"]: linhas.append(f"- ❌ {x}")
            for x in r["avisos"]: linhas.append(f"- ⚠️ {x}")
            linhas.append("")
    if lighthouse:
        linhas += ["## Lighthouse", "", "| URL | Desempenho | Acessibilidade | Boas práticas | SEO | LCP | CLS |", "|---|---|---|---|---|---|---|"]
        for lh in lighthouse:
            linhas.append(f"| {lh['url']} | {lh.get('performance','—')} | {lh.get('accessibility','—')} | {lh.get('best-practices','—')} | {lh.get('seo','—')} | {lh.get('lcp','—')} | {lh.get('cls','—')} |")
        linhas.append("")
    linhas += ["## Próximas ações sugeridas", "",
               "1. Corrigir todos os itens ❌ (bloqueiam indexação/experiência).",
               "2. Atacar o maior desvio de meta do Lighthouse (geralmente LCP: imagens em WebP/AVIF com `width/height`, `fetchpriority=\"high\"` no hero, fontes com `font-display: swap`).",
               "3. Publicar 1 conteúdo novo por semana (blog) mirando as palavras-chave de `marketing/seo-plano.md`.",
               "4. Revisar conversão: CTA visível acima da dobra, WhatsApp funcionando, formulário da NeuroNews.", ""]
    return "\n".join(linhas)

def ler_lighthouse(caminhos):
    out = []
    for c in caminhos:
        try:
            d = json.load(open(c))
            cats = d.get("categories", {}); aud = d.get("audits", {})
            out.append({"url": d.get("finalDisplayedUrl") or d.get("requestedUrl"),
                        **{k: round((cats.get(k, {}).get("score") or 0) * 100) for k in ("performance", "accessibility", "best-practices", "seo")},
                        "lcp": aud.get("largest-contentful-paint", {}).get("displayValue", "—"),
                        "cls": aud.get("cumulative-layout-shift", {}).get("displayValue", "—")})
        except Exception as e:
            out.append({"url": c, "performance": f"erro: {e}"})
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="https://www.priscilapalomo.com")
    ap.add_argument("--out"); ap.add_argument("--json")
    ap.add_argument("--lighthouse", nargs="*", default=[], help="arquivos .json do Lighthouse para incluir")
    ap.add_argument("--externos", action="store_true", help="também verifica links externos")
    a = ap.parse_args()
    res, crit = auditar(a.base, a.externos)
    lh = ler_lighthouse(a.lighthouse) if a.lighthouse else None
    md = relatorio_md(a.base, res, crit, lh)
    if a.out: open(a.out, "w", encoding="utf-8").write(md)
    else: print(md)
    if a.json: json.dump({"base": a.base, "criticos": crit, "paginas": res, "lighthouse": lh, "metas": METAS}, open(a.json, "w"), ensure_ascii=False, indent=2)
    sys.exit(1 if crit else 0)
