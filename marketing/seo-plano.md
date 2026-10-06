# Plano de SEO — 90 dias

Objetivo: captar quem já pesquisa no Google pelas dores que o site resolve,
nas duas frentes (empresas e clínica). Sem ferramenta paga: Google Search
Console, Google Business Profile e disciplina editorial.

**Situação técnica:** site estático no GitHub Pages, domínio próprio
(www.priscilapalomo.com), HTTPS, `sitemap.xml` e `robots.txt` na raiz,
páginas internas com `noindex`. Blog em Markdown renderizado no navegador
(`post.html?p=slug`), o que o Google indexa, mas com atraso; títulos e
descrições dos posts vêm do front-matter.

---

## 1. Vinte palavras-chave alvo

Volumes são estimativas qualitativas (alto/médio/baixo) para o Brasil;
validar no Search Console a partir do segundo mês.

| # | Palavra-chave | Intenção | Volume | Página correspondente |
| --- | --- | --- | --- | --- |
| 1 | riscos psicossociais NR-1 | Informacional/comercial (RH, SESMT) | Alto | `index.html#diagnostico` + artigo 1 |
| 2 | NR-1 saúde mental PGR | Informacional | Alto | Artigo 1 e 5 |
| 3 | diagnóstico de riscos psicossociais empresa | Comercial | Médio | `index.html#diagnostico` |
| 4 | avaliação psicossocial NR-1 como fazer | Informacional | Médio | Artigo 5 |
| 5 | consultoria saúde mental empresas | Comercial | Médio | `index.html` |
| 6 | palestra saúde mental SIPAT | Comercial | Médio (sazonal out/nov) | `index.html#palestras` + artigo 3 |
| 7 | palestra burnout empresa | Comercial | Baixo/médio | `index.html#palestras` + `loja.html` |
| 8 | programa de saúde mental corporativa | Comercial | Médio | `index.html#programa` |
| 9 | treinamento de liderança saúde mental | Comercial | Baixo/médio | `index.html#lideranca` + artigo 7 |
| 10 | mindfulness para empresas | Comercial/informacional | Médio | `index.html#programa` + artigo 4 |
| 11 | custo do afastamento por saúde mental | Informacional (RH, financeiro) | Baixo/médio | `index.html#calculadora` + artigo 2 |
| 12 | Lei 14.831 empresa promotora saúde mental | Informacional | Baixo/médio | Artigo 9 |
| 13 | psicóloga fobia São Paulo | Transacional local | Médio | `fobias.html` + Google Business Profile |
| 14 | tratamento medo de voar | Informacional/transacional | Alto | `fobias.html` + artigo 6 + `loja.html` |
| 15 | medo de falar em público tratamento | Informacional/transacional | Alto | `fobias.html` + artigo 8 |
| 16 | exposição gradual fobia o que é | Informacional | Médio | `fobias.html#entenda` + post existente "entendendo-as-fobias" |
| 17 | realidade virtual fobia tratamento | Informacional | Médio | `pesquisa.html` + `fobias.html` + artigo 10 |
| 18 | ansiedade de desempenho sintomas | Informacional | Médio | `fobias.html` + artigo 8 |
| 19 | psicólogo online fobia | Transacional | Médio | `fobias.html` |
| 20 | consultoria científica healthtech saúde mental | Comercial (nicho) | Baixo | `pesquisa.html#healthtech` + artigo 12 |

Palavras de marca a monitorar: "Priscila Palomo", "Priscila Palomo psicóloga",
"Mente Regulada programa", "Liderança Regulada".

---

## 2. Doze artigos de blog para três meses

Um por semana, 900 a 1.400 palavras, publicados como `posts/<slug>.md` com
front-matter (`titulo`, `data`, `tag`, `cor`, `resumo`) e slug adicionado em
`posts/index.json`. Cada artigo mira 1 ou 2 palavras-chave da tabela, cita
fontes, tem um CTA único e links internos para a página correspondente.

### Mês 1 (outubro) — fundação B2B

1. **O que são riscos psicossociais e o que a NR-1 exige no PGR (guia em linguagem simples)**
   Slug: `riscos-psicossociais-nr1-guia` · Palavras 1, 2 · Tag: Empresas
   Estrutura: definição, lista dos fatores, as 4 exigências, o que não serve, checklist. CTA: diagnóstico gratuito.

2. **Quanto custa o adoecimento mental para a sua empresa: a conta dos 6% da folha**
   Slug: `custo-adoecimento-mental-empresa` · Palavra 11 · Tag: Empresas
   Estrutura: 546 mil afastamentos, 196 dias, 6% da folha, exemplo com 500 pessoas, retorno R$ 3–7. CTA: calculadora.

3. **Palestra de saúde mental na SIPAT: como escolher o tema e medir o resultado**
   Slug: `palestra-saude-mental-sipat` · Palavras 6, 7 · Tag: Empresas
   Estrutura: o que a palestra faz e não faz, temas que funcionam, escala pré/pós, como integrar ao PGR. CTA: agenda de novembro.

4. **Mindfulness nas empresas: o que a ciência estuda e o que o mercado vende**
   Slug: `mindfulness-empresas-ciencia` · Palavra 10 · Tag: Ciência
   Estrutura: MBSR/MBCT, evidência, por que "já tentei e não funcionou", adaptações para o trabalho, medição. CTA: Programa Mente Regulada.

### Mês 2 (novembro) — profundidade B2B e abertura B2C

5. **Como fazer a avaliação de riscos psicossociais: instrumentos, etapas e erros comuns**
   Slug: `avaliacao-riscos-psicossociais-como-fazer` · Palavras 2, 4 · Tag: Empresas
   Estrutura: instrumentos validados no Brasil, amostragem, anonimato, cruzamento com indicadores, relatório, plano de ação. CTA: Kit NR-1 e diagnóstico.

6. **Medo de voar: o que acontece no corpo e como se trata (inclusive com realidade virtual)**
   Slug: `medo-de-voar-tratamento` · Palavras 14, 17 · Tag: Fobias
   Estrutura: fisiologia, ciclo da evitação, escada da exposição, RV, o que não ajuda, quando procurar ajuda. CTA: Guia Medo de Voar e conversa.

7. **O líder é o maior fator psicossocial do time: o que a neurociência diz e como formar gestores**
   Slug: `lideranca-fator-psicossocial` · Palavra 9 · Tag: Liderança
   Estrutura: cérebro social, líder imprevisível vs. regulado, o que se treina, indicadores de clima. CTA: Liderança Regulada e Playbook.

8. **Ansiedade de desempenho: por que a voz treme e o que fazer antes da próxima apresentação**
   Slug: `ansiedade-de-desempenho-falar-em-publico` · Palavras 15, 18 · Tag: Fobias
   Estrutura: mecanismo, sinais, o que não funciona, exposição em degraus, regulação treinada. CTA: Falar em Público em 21 dias e conversa.

### Mês 3 (dezembro) — autoridade e nichos

9. **Lei 14.831: o que é o Certificado Empresa Promotora da Saúde Mental e como pleitear**
   Slug: `lei-14831-certificado-saude-mental` · Palavra 12 · Tag: Empresas
   Estrutura: requisitos, relação com a NR-1, evidências necessárias, uso em marca empregadora. CTA: diagnóstico.

10. **Realidade virtual no tratamento de fobias: o que a pesquisa mostra e quais são os limites**
    Slug: `realidade-virtual-fobias-pesquisa` · Palavra 17 · Tag: Ciência
    Estrutura: bastidores do laboratório, evidência, riscos (crises em pessoas com ansiedade sem acompanhamento), uso clínico atual. CTA: aba Ciência e conversa.

11. **Saúde mental no orçamento de 2027: três linhas que todo RH deveria incluir**
    Slug: `saude-mental-orcamento-2027` · Palavras 5, 8 · Tag: Empresas
    Estrutura: ciclo anual, diagnóstico, formação de líderes, programa por área, como apresentar ao CFO. CTA: proposta em 48 h.

12. **IA em saúde mental: lupa, não substituto. O que uma healthtech precisa validar**
    Slug: `ia-saude-mental-healthtech-evidencia` · Palavra 20 · Tag: Tecnologia
    Estrutura: lições dos consórcios europeus, onde a IA ajuda, onde não, desenho de evidência, ética. CTA: consultoria científica.

Posts existentes para atualizar o front-matter com `resumo` orientado a busca
(sem editar o corpo agora): `entendendo-as-fobias`, `vencendo-a-ansiedade`,
`toc-pensamentos-intrusivos`.

---

## 3. Meta descriptions — orientações

Regras

- 140 a 155 caracteres, frase completa, verbo de ação, sem aspas duplas.
- Incluir a palavra-chave principal e a cidade quando for busca local.
- Dizer o que a pessoa ganha ao clicar; não repetir o título.
- Nenhuma promessa de resultado nem preço de atendimento clínico (vale a ética também aqui).
- Uma meta por página; páginas internas (`divulgacao.html`, `dashboard.html`, `kit-semana.html`, `terapia-pro.html`, `extrato-2026.html`) ficam com `noindex` e fora do sitemap.

Sugestões para quando as páginas forem revisadas (não alterar agora; registrar aqui)

- **index.html** (atual, 232 caracteres, longa): encurtar para "Diagnóstico de riscos psicossociais (NR-1), programas de regulação emocional com medição e formação de líderes. Saúde mental corporativa com ciência, por Priscila Palomo, PhD." (154)
- **fobias.html**: "Tratamento de fobias e ansiedade de desempenho com exposição gradual e realidade virtual. Psicóloga PhD, online e presencial na Vila Leopoldina, São Paulo." (152)
- **pesquisa.html**: "Pesquisa em neurociência, realidade virtual para fobias e mindfulness: publicações, laboratórios parceiros e consultoria científica para healthtechs." (150)
- **blog.html**: "Artigos sobre saúde mental no trabalho, NR-1, ansiedade, fobias e neurociência, escritos por Priscila Palomo, psicóloga e PhD." (124)
- **loja.html**: "Materiais digitais de Priscila Palomo: Kit NR-1, Playbook Liderança Regulada, palestra sobre burnout, guias sobre medo de voar e falar em público." (147)

Para artigos de blog, o campo `resumo` do front-matter funciona como meta
description; seguir as mesmas regras.

Títulos (`<title>`): até 60 caracteres, palavra-chave no início, marca no
fim ("… — Priscila Palomo").

---

## 4. Checklist técnico (semana 1)

- [x] `sitemap.xml` na raiz com URLs absolutas (index, fobias, pesquisa, blog, apresentacao, cursos, loja, escada-segura e 9 posts).
- [x] `robots.txt` permitindo tudo, bloqueando páginas internas e apontando o sitemap.
- [ ] Verificar propriedade no Google Search Console (método: arquivo HTML ou registro DNS) e enviar o sitemap.
- [ ] Bing Webmaster Tools (importa a configuração do Search Console).
- [ ] Google Business Profile: categoria "Psicólogo", endereço na Vila Leopoldina (ou área de atendimento), horário, site, fotos, descrição com "fobias e ansiedade" e "saúde mental no trabalho".
- [ ] Conferir que `post.html?p=slug` gera `<title>` e meta description dinâmicos a partir do front-matter (o Google renderiza JS, mas títulos ajudam no CTR).
- [ ] Imagens com `alt` descritivo (já presente nas principais).
- [ ] Core Web Vitals: site leve; manter fontes via Google Fonts com `display=swap` (já configurado).
- [ ] Schema.org: avaliar inclusão futura de `Person` (Priscila) e `LocalBusiness`/`MedicalBusiness` na home e em fobias.html.
- [ ] Links internos: cada artigo novo aponta para a página de serviço correspondente e para 1 artigo relacionado.

---

## 5. Rotina e métricas

- Publicar 1 artigo por semana (quarta, dentro do bloco de gravação quinzenal; nas semanas alternadas, o artigo é adaptado de posts do LinkedIn).
- Toda sexta: Search Console (impressões, cliques, posição média das 20 palavras) e Google Business (visualizações, cliques em ligar/rota/site).
- Meta até o fim de dezembro: 5 palavras-chave na primeira página; 1.500 cliques orgânicos acumulados; 30 cliques em WhatsApp vindos de busca.
- A partir de janeiro: atualizar os 3 artigos de melhor desempenho com dados novos e links para a loja.
