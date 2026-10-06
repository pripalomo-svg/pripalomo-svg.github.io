#!/usr/bin/env python3
"""Aplica o cabeçalho, o rodapé, o skip link, os breadcrumbs e o botão
flutuante de WhatsApp em todas as páginas públicas.

    python3 tools/layout/injetar.py            # todas as páginas
    python3 tools/layout/injetar.py loja.html  # só algumas

Cada página tem um `<header class="site-header">…</header>` e um
`<footer class="site-footer">…</footer>` que são substituídos inteiros.
Os breadcrumbs são inseridos no primeiro `.container` do `.page-hero`
(se a página tiver um e ainda não tiver breadcrumbs).
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WA = 'https://wa.me/5511950690537?text=Ol%C3%A1%20Priscila!%20Quero%20conversar.'
WA_EMPRESA = 'https://wa.me/5511950690537?text=Ol%C3%A1%20Priscila!%20Quero%20agendar%20o%20diagn%C3%B3stico%20inicial%20gratuito%20para%20minha%20empresa.'

PAGINAS = {
    # arquivo: (item ativo, breadcrumbs)
    'index.html':            ('', []),
    'fobias.html':           ('voce', [('Fobias e ansiedade', None)]),
    'pesquisa.html':         ('ciencia', [('Ciência', None)]),
    'apresentacao.html':     ('sobre', [('Sobre', None)]),
    'blog.html':             ('blog', [('Blog', None)]),
    'post.html':             ('blog', []),
    'cursos.html':           ('loja', [('Cursos', None)]),
    'loja.html':             ('loja', [('Loja', None)]),
    'escada-segura.html':    ('loja', [('Loja', 'loja.html'), ('Livro Escada Segura', None)]),
    'catalogo-videos.html':  ('sobre', [('Vídeos', None)]),
    'divulgacao.html':       ('', [('Divulgação', None)]),
    'privacidade.html':      ('', [('Privacidade', None)]),
    'produtos/kit-nr1.html':                   ('loja', [('Loja', 'loja.html'), ('Kit NR-1', None)]),
    'produtos/playbook-lideranca-regulada.html':('loja', [('Loja', 'loja.html'), ('Playbook Liderança Regulada', None)]),
    'produtos/palestra-burnout.html':          ('loja', [('Loja', 'loja.html'), ('Palestra Burnout', None)]),
    'produtos/guia-medo-de-voar.html':         ('loja', [('Loja', 'loja.html'), ('Guia Medo de voar', None)]),
    'produtos/programa-falar-em-publico.html': ('loja', [('Loja', 'loja.html'), ('Falar em público', None)]),
    'produtos/mente-regulada-audios.html':     ('loja', [('Loja', 'loja.html'), ('Mente Regulada: áudios', None)]),
}

I = {
    'chev': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>',
    'clip': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/></svg>',
    'pulse': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
    'users': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    'mic': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>',
    'cpu': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M15 2v2M9 2v2M15 20v2M9 20v2M2 15h2M2 9h2M20 15h2M20 9h2"/></svg>',
    'calc': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" x2="16" y1="6" y2="6"/><line x1="16" x2="16" y1="14" y2="18"/><path d="M16 10h.01M12 10h.01M8 10h.01M12 14h.01M8 14h.01M12 18h.01M8 18h.01"/></svg>',
    'shield': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/></svg>',
    'plane': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/></svg>',
    'speak': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    'book': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>',
    'head': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 14h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a9 9 0 0 1 18 0v7a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3"/></svg>',
    'menu': '<svg class="ic-menu" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="4" x2="20" y1="7" y2="7"/><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="17" y2="17"/></svg>',
    'close': '<svg class="ic-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>',
    'wa': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.3-.6-.4zM12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2z"/></svg>',
    'in': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.4 2H3.6A1.6 1.6 0 0 0 2 3.6v16.8A1.6 1.6 0 0 0 3.6 22h16.8a1.6 1.6 0 0 0 1.6-1.6V3.6A1.6 1.6 0 0 0 20.4 2zM8 19H5V9h3zM6.5 7.7A1.7 1.7 0 1 1 8.2 6a1.7 1.7 0 0 1-1.7 1.7zM19 19h-3v-4.9c0-1.2 0-2.7-1.6-2.7s-1.9 1.3-1.9 2.6V19h-3V9h2.9v1.4a3.2 3.2 0 0 1 2.9-1.6c3 0 3.6 2 3.6 4.6z"/></svg>',
    'mail': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>',
    'arrow': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg>',
}

EMPRESAS = [
    ('index.html#diagnostico', 'clip', 'Diagnóstico NR-1', 'Mapeamento de riscos psicossociais para o PGR'),
    ('index.html#programa', 'pulse', 'Programa Mente Regulada', 'Oito semanas de regulação emocional, com medição'),
    ('index.html#lideranca', 'users', 'Liderança Regulada', 'Formação de gestores em neurociência do estresse'),
    ('index.html#palestras', 'mic', 'Palestras e SIPAT', 'Ciência traduzida em histórias, 60 a 90 minutos'),
    ('pesquisa.html#healthtech', 'cpu', 'Consultoria para healthtechs', 'Validação clínica e desenho de evidência'),
    ('index.html#calculadora', 'calc', 'Calculadora de custo', 'Quanto o adoecimento mental custa à empresa'),
]
VOCE = [
    ('fobias.html', 'shield', 'Fobias e ansiedade', 'Atendimento com exposição gradual e realidade virtual'),
    ('produtos/guia-medo-de-voar.html', 'plane', 'Guia: medo de voar', 'Programa de preparação para o próximo voo'),
    ('produtos/programa-falar-em-publico.html', 'speak', 'Falar em público', 'Programa de 21 dias para ansiedade de desempenho'),
    ('escada-segura.html', 'book', 'Livro Escada Segura', 'Fobias na infância, para pais e cuidadores'),
    ('produtos/mente-regulada-audios.html', 'head', 'Mente Regulada: áudios', 'Oito práticas guiadas de regulação emocional'),
]


def item(p, href, ic, t, d):
    return f'<a class="nav-item" href="{p}{href}"><span class="nav-item-ic">{I[ic]}</span><span><strong>{t}</strong><small>{d}</small></span></a>'


def header(p, active):
    def cls(k): return ' active' if k == active else ''
    emp = '\n              '.join(item(p, *x) for x in EMPRESAS)
    voc = '\n              '.join(item(p, *x) for x in VOCE)
    return f'''<header class="site-header">
  <div class="container nav">
    <a class="nav-logo" href="{p}index.html" aria-label="Priscila Palomo, página inicial">
      <img src="{p}assets/logo.svg" alt="" width="36" height="36">
      <span class="nav-logo-text">
        <span class="nav-logo-name">Priscila Palomo</span>
        <span class="nav-logo-sub">Psicóloga · PhD · CRP 98007</span>
      </span>
    </a>
    <nav class="nav-main" id="menu-principal" aria-label="Principal">
      <ul class="nav-list">
        <li class="has-menu">
          <button class="nav-link{cls('empresas')}" type="button" aria-expanded="false" aria-controls="menu-empresas">Para empresas {I['chev']}</button>
          <div class="nav-menu" id="menu-empresas">
            <div class="nav-menu-grid">
              {emp}
            </div>
            <div class="nav-menu-foot"><a href="{p}index.html#solucoes">Ver todas as soluções</a><a href="{WA_EMPRESA}" target="_blank" rel="noopener">Agendar diagnóstico gratuito</a></div>
          </div>
        </li>
        <li class="has-menu">
          <button class="nav-link{cls('voce')}" type="button" aria-expanded="false" aria-controls="menu-voce">Para você {I['chev']}</button>
          <div class="nav-menu nav-menu--single" id="menu-voce">
            <div class="nav-menu-grid">
              {voc}
            </div>
          </div>
        </li>
        <li><a class="nav-link{cls('ciencia')}" href="{p}pesquisa.html">Ciência</a></li>
        <li><a class="nav-link{cls('blog')}" href="{p}blog.html">Blog</a></li>
        <li><a class="nav-link{cls('loja')}" href="{p}loja.html">Loja</a></li>
        <li><a class="nav-link{cls('sobre')}" href="{p}apresentacao.html">Sobre</a></li>
      </ul>
      <div class="nav-mobile-cta">
        <a class="btn btn-primary" href="{WA}" target="_blank" rel="noopener">Agendar conversa</a>
        <a class="btn btn-outline" href="mailto:pripalomo@outlook.com">pripalomo@outlook.com</a>
      </div>
    </nav>
    <div class="nav-actions">
      <a class="btn btn-primary" href="{WA}" target="_blank" rel="noopener">Agendar conversa</a>
      <button class="nav-toggle" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="menu-principal">{I['menu']}{I['close']}</button>
    </div>
  </div>
  <div class="nav-overlay"></div>
</header>'''


def footer(p):
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <div class="footer-brand">
          <img src="{p}assets/logo.svg" alt="">
          <div><strong>Priscila Palomo</strong><span>Psicóloga · PhD · CRP 98007</span></div>
        </div>
        <p class="footer-desc">Saúde mental no trabalho com base em neurociência e evidência. Atendimento em São Paulo e online para todo o Brasil.</p>
        <div class="footer-social">
          <a href="https://www.linkedin.com/in/priscilapalomo" target="_blank" rel="noopener" aria-label="LinkedIn">{I['in']}</a>
          <a href="https://wa.me/5511950690537" target="_blank" rel="noopener" aria-label="WhatsApp">{I['wa']}</a>
          <a href="mailto:pripalomo@outlook.com" aria-label="E-mail">{I['mail']}</a>
        </div>
      </div>
      <div>
        <h4>Para empresas</h4>
        <ul class="footer-links">
          <li><a href="{p}index.html#diagnostico">Diagnóstico NR-1</a></li>
          <li><a href="{p}index.html#programa">Programa Mente Regulada</a></li>
          <li><a href="{p}index.html#lideranca">Liderança Regulada</a></li>
          <li><a href="{p}index.html#palestras">Palestras e SIPAT</a></li>
          <li><a href="{p}pesquisa.html#healthtech">Consultoria para healthtechs</a></li>
          <li><a href="{p}index.html#calculadora">Calculadora de custo</a></li>
        </ul>
      </div>
      <div>
        <h4>Para você</h4>
        <ul class="footer-links">
          <li><a href="{p}fobias.html">Fobias e ansiedade</a></li>
          <li><a href="{p}produtos/guia-medo-de-voar.html">Medo de voar</a></li>
          <li><a href="{p}produtos/programa-falar-em-publico.html">Falar em público</a></li>
          <li><a href="{p}escada-segura.html">Livro Escada Segura</a></li>
          <li><a href="{p}produtos/mente-regulada-audios.html">Áudios Mente Regulada</a></li>
        </ul>
      </div>
      <div>
        <h4>Conteúdo</h4>
        <ul class="footer-links">
          <li><a href="{p}pesquisa.html">Ciência e publicações</a></li>
          <li><a href="{p}blog.html">Blog</a></li>
          <li><a href="{p}cursos.html">Cursos online</a></li>
          <li><a href="{p}loja.html">Loja</a></li>
          <li><a href="{p}apresentacao.html">Sobre a Priscila</a></li>
        </ul>
      </div>
      <div>
        <h4>Contato</h4>
        <ul class="footer-links">
          <li><a href="https://wa.me/5511950690537" target="_blank" rel="noopener">+55 11 95069-0537</a></li>
          <li><a href="mailto:pripalomo@outlook.com">pripalomo@outlook.com</a></li>
          <li><a href="https://www.linkedin.com/in/priscilapalomo" target="_blank" rel="noopener">LinkedIn</a></li>
          <li><a href="http://lattes.cnpq.br/4124029805069326" target="_blank" rel="noopener">Currículo Lattes</a></li>
          <li><a href="https://orcid.org/0000-0003-4936-6479" target="_blank" rel="noopener">ORCID</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year></span> Priscila Palomo · Psicóloga CRP 06/98007 · São Paulo, SP</span>
      <span><a href="{p}privacidade.html">Privacidade</a><a href="{p}catalogo-videos.html">Vídeos</a><a href="{p}dashboard.html">Desk</a></span>
    </div>
  </div>
</footer>'''


def wa_float():
    return f'<a class="wa-float" href="{WA}" target="_blank" rel="noopener" aria-label="Falar pelo WhatsApp"><span class="wa-ic">{I["wa"]}</span><span>Falar no WhatsApp</span></a>\n'


def crumbs(p, trail):
    if not trail:
        return ''
    lis = [f'<li><a href="{p}index.html">Início</a></li>']
    for name, href in trail:
        lis.append(f'<li><a href="{p}{href}">{name}</a></li>' if href else f'<li aria-current="page">{name}</li>')
    return '<nav class="crumbs" aria-label="Você está aqui"><ol>' + ''.join(lis) + '</ol></nav>\n      '


def process(rel):
    path = ROOT / rel
    s = path.read_text(encoding='utf-8')
    p = '../' if '/' in rel else ''
    active, trail = PAGINAS.get(rel, ('', []))

    s = re.sub(r'<header class="site-header">.*?</header>', lambda m: header(p, active), s, count=1, flags=re.S)
    s = re.sub(r'<footer class="site-footer">.*?</footer>', lambda m: footer(p), s, count=1, flags=re.S)
    s = re.sub(r'\n?<a class="wa-float".*?</a>\n', '\n', s, flags=re.S)
    s = s.replace('<footer class="site-footer">', wa_float() + '<footer class="site-footer">', 1)

    if '<a class="skip-link"' not in s:
        s = re.sub(r'(<body[^>]*>\s*)', r'\1<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>\n', s, count=1)
    s = re.sub(r'<main>', '<main id="conteudo">', s, count=1)

    if trail and 'class="crumbs"' not in s:
        m = re.search(r'<section class="page-hero[^"]*"[^>]*>\s*<div class="container[^"]*">\s*', s)
        if m:
            s = s[:m.end()] + crumbs(p, trail) + s[m.end():]
    path.write_text(s, encoding='utf-8')
    print('ok', rel)


if __name__ == '__main__':
    alvos = sys.argv[1:] or list(PAGINAS)
    for rel in alvos:
        if (ROOT / rel).exists():
            process(rel)
        else:
            print('ignorado (não existe):', rel)
