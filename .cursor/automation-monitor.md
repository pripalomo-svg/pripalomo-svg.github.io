# Agente de melhoria contínua do site (rodar 1× por dia)

Você cuida do site estático www.priscilapalomo.com (HTML/CSS/JS puro, GitHub Pages,
branch `main`, sem build). Leia `AGENTS.md`, `MONITORAMENTO.md` e `ANALISE-NICHO.md`
antes de agir. A meta é deixar o site no nível dos sites mais acessados do mundo em
velocidade, SEO, acessibilidade e conversão — sem mudar o posicionamento
(saúde mental no trabalho com neurociência e evidência + clínica de fobias).

## Passo a passo

1. **Ler o diagnóstico de hoje.** Rode `gh issue list --label monitoramento` e leia o
   último comentário da issue "Monitoramento diário do site" (relatório do Lighthouse e
   da auditoria). Se não houver relatório das últimas 24 h, gere um:
   `python3 -m http.server 8000 &` e `python3 tools/auditoria/auditar.py --base http://localhost:8000`.
2. **Escolher UMA melhoria de maior impacto**, nesta ordem de prioridade:
   1. Itens ❌ (página fora do ar, link quebrado, sem title/h1, imagem sem alt).
   2. Core Web Vitals abaixo da meta (LCP > 2,5 s, CLS > 0,1): comprimir/converter imagens
      para WebP com `width`/`height`, `loading="lazy"` fora da dobra, `fetchpriority="high"`
      no hero, `font-display: swap`, remover CSS/JS não usado.
   3. Lighthouse SEO/Acessibilidade < 95: contraste, rótulos de formulário, ordem de
      headings, `aria-label`, descriptions dentro de 70–160 caracteres.
   4. Conversão: CTA do WhatsApp visível no mobile acima da dobra, clareza das ofertas da
      `loja.html`, prova social institucional (sem depoimentos de pacientes).
   5. Conteúdo: se nenhum item acima estiver pendente, escrever 1 artigo novo em
      `posts/<slug>.md` (+ `posts/index.json`) com uma palavra-chave de
      `marketing/seo-plano.md`, 900–1.400 palavras, com fontes.
3. **Implementar e testar.** Mudanças pequenas e seguras. Verifique com
   `python3 tools/auditoria/auditar.py --base http://localhost:8000` (sem itens ❌) e,
   se houver Node, `npx -y lighthouse http://localhost:8000 --output=json --chrome-flags="--headless"`.
   Confira visualmente com `google-chrome --headless=new --screenshot`.
4. **Abrir um PR** (nunca commit direto na `main`) com título
   `Melhoria diária: <o que mudou>` e, no corpo, o antes/depois dos indicadores.
5. **Comentar na issue de monitoramento**: o que foi feito, o número do PR e a próxima
   melhoria sugerida para amanhã.

## Regras

- Respeitar o Código de Ética do Psicólogo (art. 20): sem promessa de resultado, sem
  depoimentos de pacientes, sem sensacionalismo, sem preço como chamariz de serviço clínico.
- Não alterar `CNAME`, `.nojekyll`, `terapia-pro.html`, `dashboard.html`, `extrato-2026.html`.
- Manter o design system de `assets/style.css` (navy/teal, Sora + Inter) e o cabeçalho/rodapé
  idênticos em todas as páginas públicas.
- Uma melhoria por dia, bem feita, é melhor do que dez pela metade.
