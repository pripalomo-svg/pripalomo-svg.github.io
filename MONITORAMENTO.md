# Monitoramento diário do site

Objetivo: manter www.priscilapalomo.com competitivo com os sites mais bem
acessados do mundo em **velocidade, SEO, acessibilidade e conversão**, com
uma rotina automática que roda todo dia e um agente que implementa melhorias.

## Como funciona

```
06:00 BRT  GitHub Actions (.github/workflows/auditoria-diaria.yml)
           ├─ Lighthouse nas 5 páginas principais (desempenho, a11y, boas práticas, SEO, LCP, CLS)
           ├─ tools/auditoria/auditar.py  (title/description, h1, alt, canonical, OG, JSON-LD, peso, TTFB, links quebrados)
           └─ publica o relatório como comentário na issue "Monitoramento diário do site" (label `monitoramento`)

07:00 BRT  Agente agendado no Cursor (Automations) — prompt em .cursor/automation-monitor.md
           ├─ lê o relatório mais recente da issue
           ├─ escolhe a melhoria de maior impacto que ainda não foi feita
           ├─ implementa, testa localmente (python3 -m http.server) e abre um PR pequeno
           └─ comenta na issue o que mudou e o que ficou para amanhã
```

Nada disso depende de servidor próprio: o site continua estático no GitHub Pages.

## Metas de referência

| Indicador | Meta | Por quê |
|---|---|---|
| Lighthouse Desempenho | ≥ 90 | Faixa dos líderes (Google, Wikipedia, Apple) |
| Lighthouse SEO / Acessibilidade | ≥ 95 | Indexação completa e uso por todos |
| LCP (maior elemento visível) | ≤ 2,5 s | Core Web Vital que mais afeta ranking e conversão |
| CLS (estabilidade visual) | ≤ 0,1 | Evita "pulos" de layout |
| INP (resposta à interação) | ≤ 200 ms | Sensação de site rápido |
| HTML inicial | ≤ 120 KB | Primeira renderização rápida |
| TTFB | ≤ 800 ms | CDN/estático bem configurado |
| `<h1>` por página | exatamente 1 | Hierarquia clara para buscadores |
| Imagens sem `alt` / links quebrados | 0 | Acessibilidade e confiança |
| Conteúdo novo | 1 artigo/semana | Crescimento orgânico sustentado |

## Rodar a auditoria manualmente

```bash
# site publicado
python3 tools/auditoria/auditar.py

# versão local
python3 -m http.server 8000 &
python3 tools/auditoria/auditar.py --base http://localhost:8000

# com relatórios do Lighthouse (precisa de Node)
npx -y lighthouse https://www.priscilapalomo.com --output=json --output-path=./lh-home.json --chrome-flags="--headless"
python3 tools/auditoria/auditar.py --lighthouse lh-home.json --out relatorio.md
```

No GitHub, a aba **Actions → Auditoria diária do site → Run workflow** roda tudo na hora.

## Ativar o agente diário no Cursor (uma vez)

1. Cursor Dashboard → **Automations** → **New automation**.
2. Trigger: **Schedule**, diário, 07:00 (America/Sao_Paulo).
3. Repositório: `pripalomo-svg/pripalomo-svg.github.io`, branch `main`.
4. Prompt: cole o conteúdo de `.cursor/automation-monitor.md`.
5. Saída: **Create pull request** (nunca commit direto na `main`).

Enquanto a automação não estiver ativa, o workflow do GitHub já roda sozinho e
deixa o relatório pronto na issue; qualquer agente (ou pessoa) pode usar.

## Rotina semanal recomendada (15 min)

- Segunda: abrir a issue de monitoramento, ler o último relatório, aprovar/mesclar o PR do agente.
- Quarta: publicar o artigo da semana (`COMO-USAR.md`) com a palavra-chave de `marketing/seo-plano.md`.
- Sexta: conferir no Google Search Console as consultas que cresceram e ajustar títulos/descriptions.
