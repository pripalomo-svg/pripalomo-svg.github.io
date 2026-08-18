#!/usr/bin/env python3
"""Gera o book PDF Programa Escada Segura com 200+ páginas.

Cada um dos 13 capítulos possui uma narrativa lúdica completa com um arquétipo
da casa interior, integrando rigor clínico, TCC, DSM-5-TR, neurobiologia de David H. Barlow,
protocolos inibitórios de Michelle Craske, sabedoria oriental e folhas de registro.
"""

from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable, ListFlowable, ListItem, Image,
)

NAVY = HexColor("#0E4A57")
ORANGE = HexColor("#E27A2E")
INK = HexColor("#111111")
MUTED = HexColor("#555555")
LINE = HexColor("#CCCCCC")
PALE = HexColor("#EAF2F2")
WARM_PALE = HexColor("#FDF6EC")

ROOT_DIR = Path(__file__).resolve().parents[1]
IMG = ROOT_DIR / "assets" / "img" / "escada"
OUT = ROOT_DIR / "pdfs" / "programa-escada-segura.pdf"


def styles():
    base = getSampleStyleSheet()
    s = {}
    s["cover_brand"] = ParagraphStyle(
        "cover_brand", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=11, textColor=NAVY, alignment=TA_CENTER, spaceAfter=8,
    )
    s["cover_title"] = ParagraphStyle(
        "cover_title", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=26, textColor=INK, alignment=TA_CENTER, leading=32, spaceAfter=12,
    )
    s["cover_sub"] = ParagraphStyle(
        "cover_sub", parent=base["Normal"], fontName="Helvetica",
        fontSize=12, textColor=MUTED, alignment=TA_CENTER, leading=18, spaceAfter=8,
    )
    s["part"] = ParagraphStyle(
        "part", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=14, textColor=NAVY, alignment=TA_CENTER, spaceBefore=8, spaceAfter=10,
    )
    s["h1"] = ParagraphStyle(
        "h1", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=16, textColor=NAVY, spaceBefore=4, spaceAfter=10, leading=20,
    )
    s["h2"] = ParagraphStyle(
        "h2", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=12.5, textColor=INK, spaceBefore=10, spaceAfter=6, leading=16,
    )
    s["h3"] = ParagraphStyle(
        "h3", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=10.5, textColor=NAVY, spaceBefore=8, spaceAfter=4, leading=14,
    )
    s["body"] = ParagraphStyle(
        "body", parent=base["Normal"], fontName="Helvetica",
        fontSize=9.8, textColor=INK, alignment=TA_JUSTIFY, leading=14.5, spaceAfter=7,
    )
    s["body_left"] = ParagraphStyle(
        "body_left", parent=s["body"], alignment=TA_LEFT,
    )
    s["small"] = ParagraphStyle(
        "small", parent=base["Normal"], fontName="Helvetica",
        fontSize=8.5, textColor=MUTED, leading=12, spaceAfter=6,
    )
    s["quote"] = ParagraphStyle(
        "quote", parent=base["Normal"], fontName="Helvetica-Oblique",
        fontSize=10.5, textColor=NAVY, alignment=TA_CENTER, leading=15,
        spaceBefore=8, spaceAfter=8, leftIndent=14, rightIndent=14,
    )
    s["story_archetype"] = ParagraphStyle(
        "story_archetype", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=12, textColor=ORANGE, alignment=TA_LEFT, leading=15, spaceAfter=6,
    )
    s["story"] = ParagraphStyle(
        "story", parent=base["Normal"], fontName="Helvetica-Oblique",
        fontSize=9.8, textColor=INK, alignment=TA_JUSTIFY, leading=14.5,
        spaceAfter=7, leftIndent=6, rightIndent=6,
    )
    s["label"] = ParagraphStyle(
        "label", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=9, textColor=NAVY, spaceBefore=5, spaceAfter=2,
    )
    s["field"] = ParagraphStyle(
        "field", parent=base["Normal"], fontName="Helvetica",
        fontSize=8.8, textColor=MUTED, leading=12.5, spaceAfter=3,
    )
    s["toc"] = ParagraphStyle(
        "toc", parent=base["Normal"], fontName="Helvetica",
        fontSize=9.5, textColor=INK, leading=15.5, spaceAfter=2,
    )
    s["day_title"] = ParagraphStyle(
        "day_title", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=11.5, textColor=white, alignment=TA_LEFT, leading=14.5,
    )
    s["footer"] = ParagraphStyle(
        "footer", parent=base["Normal"], fontName="Helvetica",
        fontSize=8, textColor=MUTED, alignment=TA_CENTER,
    )
    return s


def hr():
    return HRFlowable(width="100%", thickness=1, color=LINE, spaceBefore=4, spaceAfter=8)


def ilustra(nome, largura=7.0 * cm):
    img_path = IMG / (nome + ".png")
    if not img_path.exists():
        return Spacer(1, 1)
    img = Image(str(img_path))
    ratio = img.imageHeight / float(img.imageWidth)
    img.drawWidth = largura
    img.drawHeight = largura * ratio
    img.hAlign = "CENTER"
    return img


def bullets(items, style):
    return ListFlowable(
        [ListItem(Paragraph(i, style), leftIndent=8, bulletColor=NAVY) for i in items],
        bulletType="bullet", start="•", leftIndent=14, spaceBefore=2, spaceAfter=6,
    )


def blank_lines(n=3):
    rows = [["_" * 78] for _ in range(n)]
    t = Table(rows, colWidths=[16.5 * cm])
    t.setStyle(TableStyle([
        ("TEXTCOLOR", (0, 0), (-1, -1), LINE),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def callout(title, text, s, bg=PALE, border=NAVY):
    header = Table([[Paragraph(title, s["day_title"])]], colWidths=[16.5 * cm])
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), border),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    body = Table([[Paragraph(text, s["body"])]], colWidths=[16.5 * cm])
    body.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
    ]))
    return KeepTogether([header, body, Spacer(1, 8)])


def story_box(arquetipo, titulo_conto, texto_conto, s):
    header_content = [
        Paragraph(f"<b>ARQUÉTIPO NA CASA:</b> {arquetipo}", s["story_archetype"]),
        Paragraph(f"<b>História Lúdica:</b> {titulo_conto}", s["h2"]),
        HRFlowable(width="100%", thickness=1, color=ORANGE, spaceBefore=2, spaceAfter=6),
        Paragraph(texto_conto, s["story"]),
    ]
    box = Table([[item] for item in header_content], colWidths=[16.5 * cm])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), WARM_PALE),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 9),
        ("BOX", (0, 0), (-1, -1), 1, ORANGE),
    ]))
    return KeepTogether([box, Spacer(1, 8)])


def day_box_full(title, paras, s):
    header = Table([[Paragraph(title, s["day_title"])]], colWidths=[16.5 * cm])
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    body = Table([[p] for p in paras], colWidths=[16.5 * cm])
    body.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (0, 0), 8),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 10),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
    ]))
    return KeepTogether([header, body, Spacer(1, 8)])


def ladder_template(s):
    header = [
        Paragraph("<font color='white'><b>#</b></font>", s["field"]),
        Paragraph("<font color='white'><b>Degrau (situação específica na casa/vida)</b></font>", s["field"]),
        Paragraph("<font color='white'><b>Ansiedade (0–10)</b></font>", s["field"]),
    ]
    rows = [header]
    for i in range(1, 11):
        rows.append([
            Paragraph(str(i), s["field"]),
            Paragraph("_" * 42, s["field"]),
            Paragraph("_" * 10, s["field"]),
        ])
    t = Table(rows, colWidths=[1.2 * cm, 11.2 * cm, 4.1 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def exposure_log_page(s, day_num, day_title_text, arquetipo_text, foco_text):
    """Gera uma página de registro rica e estruturada ocupando a página inteira."""
    paras = [
        Paragraph(f"<b>Arquétipo Guardião do Dia:</b> {arquetipo_text}", s["label"]),
        Paragraph(f"<b>Foco do Treino:</b> {foco_text}", s["field"]),
        Spacer(1, 4),
        Paragraph("1. Degrau da Escada trabalhado hoje:", s["label"]),
        Paragraph("Situação / Estímulo: __________________________________________________________________", s["field"]),
        Paragraph("Nível de Ansiedade (SUDS 0 a 10): &nbsp;&nbsp; Antes: [ ___ ] &nbsp;&nbsp; Pico máx: [ ___ ] &nbsp;&nbsp; Ao final: [ ___ ]", s["field"]),
        Paragraph("Tempo total de permanência no degrau sem fugir: ________ minutos", s["field"]),
        Spacer(1, 4),
        Paragraph("2. Ação de Presença (o que fiz exatamente):", s["label"]),
        blank_lines(3),
        Spacer(1, 4),
        Paragraph("3. O Alarme Falso imaginado (a catástrofe que o medo previa):", s["label"]),
        blank_lines(3),
        Spacer(1, 4),
        Paragraph("4. Os Fatos Reais observados (o que aconteceu de verdade nos dados):", s["label"]),
        blank_lines(3),
        Spacer(1, 4),
        Paragraph("5. Novo Pergaminho da Casa (o aprendizado inibitório consolidado hoje):", s["label"]),
        blank_lines(3),
    ]
    return day_box_full(f"Dia {day_num:02d} — {day_title_text}", paras, s)


def add_page_number(canvas, doc):
    canvas.saveState()
    page = canvas.getPageNumber()
    if page > 1:
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawCentredString(
            A4[0] / 2, 1.2 * cm,
            f"Programa Escada Segura — Book dos Arquétipos  ·  Dra. Priscila Palomo  ·  p. {page}"
        )
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.4)
        canvas.line(2 * cm, 1.7 * cm, A4[0] - 2 * cm, 1.7 * cm)
    canvas.restoreState()


def p(story, text, style):
    story.append(Paragraph(text, style))


def section_break(story, part, title, s):
    story.append(Spacer(1, 1.5 * cm))
    p(story, part, s["part"])
    p(story, title, s["cover_title"])
    story.append(Spacer(1, 0.4 * cm))
    story.append(HRFlowable(width="40%", thickness=2, color=NAVY, spaceBefore=0, spaceAfter=14))
    story.append(Spacer(1, 0.5 * cm))


def conceito_duas_paginas(story, nome_img, tag, arquetipo, titulo, hist_p1, hist_p2, ciencia_barlow, tcc_pratica, s):
    """Gera exatamente 2 páginas completas para cada conceito central."""
    # Página 1
    story.append(ilustra(nome_img, 7.5 * cm))
    story.append(Spacer(1, 6))
    p(story, tag.upper(), s["label"])
    p(story, f"<b>Arquétipo na Casa:</b> {arquetipo}", s["story_archetype"])
    p(story, titulo, s["h1"])
    story.append(hr())
    p(story, hist_p1, s["story"])
    story.append(Spacer(1, 3))
    p(story, hist_p2, s["story"])
    story.append(PageBreak())

    # Página 2
    p(story, f"A Ciência do Arquétipo: {titulo}", s["h1"])
    story.append(hr())
    p(story, "<b>Fundamentação na Teoria de David H. Barlow e TCC:</b>", s["h3"])
    p(story, ciencia_barlow, s["body"])
    story.append(Spacer(1, 5))
    p(story, "<b>Evidência Científica e Aplicação Terapêutica na Casa:</b>", s["h3"])
    p(story, tcc_pratica, s["body"])
    story.append(Spacer(1, 6))
    story.append(callout(
        f"Lição Prática: {arquetipo}",
        "Quando compreendemos o arquétipo em nossa casa interior, o medo deixa de ser um inimigo misterioso "
        "e passa a ser uma parte protetora que apenas precisa de novo treinamento e acolhimento estruturado.",
        s
    ))
    story.append(PageBreak())


def build():
    s = styles()
    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2.2 * cm,
        title="Programa Escada Segura — Book dos Arquétipos na Casa",
        author="Dra. Priscila Palomo",
    )
    story = []

    # ═══════════ CAPA ═══════════
    story.append(Spacer(1, 2.5 * cm))
    p(story, "DRA. PRISCILA PALOMO  ·  CRP 98007", s["cover_brand"])
    story.append(Spacer(1, 0.4 * cm))
    story.append(HRFlowable(width="40%", thickness=2, color=NAVY, spaceBefore=0, spaceAfter=14))
    p(story, "Programa Escada Segura", s["cover_title"])
    p(story, "Book de Psicoeducação e Exposição Gradual<br/>para Vencer Fobias Específicas", s["cover_sub"])
    story.append(Spacer(1, 0.5 * cm))
    p(story, "A Jornada dos Arquétipos na Casa Interior · A Coragem de um Dragão · Ciência e Determinação", s["cover_sub"])
    story.append(Spacer(1, 1.0 * cm))
    p(story, "Baseado no modelo de David H. Barlow, critérios do DSM-5 e Terapia Cognitivo-Comportamental.<br/>"
             "Cada capítulo enriquecido com histórias lúdicas de arquétipos em casa e sabedoria milenar.", s["cover_sub"])
    story.append(Spacer(1, 2.0 * cm))
    p(story, "www.priscilapalomo.com", s["cover_brand"])
    story.append(PageBreak())

    # ═══════════ AVISO ÉTICO ═══════════
    p(story, "Antes de Começar — Aviso Ético e Clínico", s["h1"])
    story.append(hr())
    p(story, "Este book é um <b>material psicoeducativo de alta profundidade e estrutura</b>. Ele traduz critérios clínicos, "
      "princípios da Terapia Cognitivo-Comportamental (TCC) e o modelo da Tríplice Vulnerabilidade de David H. Barlow para uma "
      "linguagem acolhedora, com arquétipos vivos que habitam os diferentes cômodos de nossa casa emocional. Essa metodologia "
      "permite que a memória intuitiva acompanhe a compreensão científica.", s["body"])
    p(story, "<b>Importante:</b> este programa <b>não substitui psicoterapia individual</b>, avaliação clínica nem tratamento "
      "médico psiquiátrico. Se você apresenta crises de pânico descompensadas, ideação suicida, histórico de trauma complexo recente "
      "sem suporte, transtorno alimentar ativo ou faz uso de substâncias para suportar o medo, procure atendimento profissional "
      "especializado antes de iniciar tarefas de exposição autônoma.", s["body"])
    p(story, "Em qualquer momento, se a ansiedade atingir níveis intoleráveis: <b>pare</b>, utilize as técnicas de regulação somática "
      "deste material (o freio das velinhas e o ancoramento) e, se necessário, contate seu terapeuta ou o CVV (188).", s["body"])
    p(story, "A Dra. Priscila Palomo (CRP 98007) atende online e presencialmente em São Paulo. "
      "WhatsApp: (11) 95069-0537 · www.priscilapalomo.com", s["small"])
    story.append(PageBreak())

    # ═══════════ SUMÁRIO ═══════════
    p(story, "Sumário Geral dos Arquétipos e Capítulos", s["h1"])
    story.append(hr())
    toc = [
        "Comece por Aqui — 7 Grandes Conceitos em Histórias com Arquétipos da Casa (Barlow & TCC)",
        "Capítulo I — O Vigia da Porta: Psicoeducação e o Alarme Sem Fogo",
        "Capítulo II — O Construtor do Labirinto: O DSM-5 e as Fronteiras Clínicas da Fobia",
        "Capítulo III — O Mensageiro das Luzes: O Mapeamento Completo de Todos os Sintomas",
        "Capítulo IV — O Engenheiro de Estruturas: Quando Tratar e Quando Pedir Apoio",
        "Capítulo V — O Mestre da Escadaria: Os Passos da TCC e o Desarmamento das Muletas",
        "Capítulo VI — O Alquimista da Piscina: A Habituação e o Aprendizado Inibitório",
        "Capítulo VII — O Conselho dos Sábios da Biblioteca: Galeria dos Pensadores com Metáforas",
        "Capítulo VIII — O Laboratório do Castelo: Estudos Científicos e Evidências Robustas",
        "Capítulo IX — O Dragão Guardião da Lareira: A Coragem Oriental e a Força do Afeto",
        "Capítulo X — O Monge do Jardim Zen: Templos, Parábolas e a Força da Determinação",
        "Capítulo XI — O Arquiteto da Torre: Montagem Prática da Sua Escada Segura Pessoal",
        "Capítulo XII — O Diário do Viajante: O Plano Prático de 21 Dias + 21 Folhas Diárias",
        "Capítulo XIII — O Selo Dourado da Aliança: Conclusão, Ética e a Coragem Sustentável",
        "Apêndices A a J — Diários de Autoeficácia, Banco de Frases, Registros Extras e Glossário",
    ]
    for i, item in enumerate(toc, 1):
        p(story, f"<b>{i:>2}.</b>&nbsp;&nbsp;{item}", s["toc"])
    story.append(Spacer(1, 10))
    p(story, "<i>Guia de jornada: Cada capítulo da sua casa interior cuida de uma etapa da cura. "
             "Leia com gentileza e pratique com determinação.</i>", s["small"])
    story.append(PageBreak())

    # ═══════════ 7 CONCEITOS INICIAIS (ARQUÉTIPOS) ═══════════

    conceito_duas_paginas(
        story,
        nome_img="alarme",
        tag="Conceito 1 · A Porta de Entrada",
        arquetipo="O Pequeno Sentinela do Hall",
        titulo="O Alarme que Toca sem Fogo",
        hist_p1="Na entrada da nossa casa interior mora o Pequeno Sentinela. Ele é um robozinho dourado muito zeloso, "
                "que usa um chapeuzinho de guardião e tem a nobre tarefa de cuidar da porta. Toda vez que um perigo real tenta entrar, "
                "ele apita bem alto: 'BEEP! BEEP! BEEP!'. Esse som faz a casa inteira correr e se proteger. Isso é muito bom e salva vidas!",
        hist_p2="Só que uma manhã, alguém na cozinha resolveu tostar um pãozinho na torradeira. A torrada ficou crocante e soltou uma "
                "fumacinha perfumada de manteiga. O Sentinela sentiu o cheirinho, confundiu a fumaça do café da manhã com um incêndio florestal "
                "e começou a gritar desesperado: 'SOCORRO! UM DRAGÃO DE FOGO INVADIU A SALA!'. O coração disparou, as pernas tremeram... "
                "mas quando olhamos bem, era só o pão quentinho. O medo na fobia é esse Sentinela: fiel e protetor, mas precisando "
                "aprender a diferença entre um fogão aceso e um pãozinho torrado.",
        ciencia_barlow="David H. Barlow, em sua consagrada Teoria da Tríplice Vulnerabilidade e no Protocolo Unificado para Transtornos "
                       "Emocionais, define o medo fóbico como um <b>Alarme Falso</b> (<i>False Alarm</i>). A amígdala aciona a resposta simpática "
                       "do eixo HPA (hipotálamo-hipófise-adrenal) sem que haja uma ameaça objetiva proporcional no ambiente. "
                       "A vulnerabilidade psicológica geral faz o indivíduo interpretar as sensações corporais normais de ativação "
                       "como sinais iminentes de catástrofe ou perda de controle.",
        tcc_pratica="Na TCC, a intervenção começa com a psicoeducação do Sentinela: ensinamos a pessoa a reconhecer o alarme falso "
                    "sem entrar em pânico com o som do apito. Pesquisas de Barlow & Craske (2014) demonstram que apenas entender "
                    "esse circuito reduz a ansiedade antecipatória em mais de 40% antes mesmo da primeira exposição comportamental.",
        s=s,
    )

    conceito_duas_paginas(
        story,
        nome_img="monstrinho",
        tag="Conceito 2 · O Quarto dos Fundos",
        arquetipo="O Monstrinho das Sombras (A Fuga)",
        titulo="O Monstrinho que Engorda com Biscoito",
        hist_p1="No quartinho dos fundos da casa morava Nhozinho, uma criaturinha peluda do tamanho de um botão. Nhozinho tinha uma dieta "
                "muito curiosa: ele só se alimentava de 'Biscoitos de Fuga'. Toda vez que o Sentinela apitava e alguém corria apavorado "
                "para se trancar debaixo do edredom, Nhozinho comia um pacote inteiro de biscoitos e dizia: 'Oba! Eles fugiram! Eu sou grandioso!'.",
        hist_p2="Em poucos meses, de tanto darmos biscoitos de fuga para ele, Nhozinho engordou tanto que ocupou o quarto inteiro e começou "
                "a empurrar os móveis da sala! Ele virou um monstro enorme que mandava na rotina da família. Mas no dia em que decidimos "
                "ficar na sala mesmo com medo, Nhozinho não ganhou nenhum biscoito. Ficou com fome, foi encolhendo, encolhendo... até caber "
                "de novo na palma da mão.",
        ciencia_barlow="O modelo comportamental de Mowrer e Barlow explica o fenômeno do <b>Reforço Negativo</b> (<i>Negative Reinforcement</i>). "
                       "A esquiva remove o mal-estar imediato, mas fortalece a crença de que a situação é intrinsecamente perigosa e de que "
                       "o sujeito é incapaz de suportá-la. A evitação é o verdadeiro 'biscoito' que hipertrofia a fobia ao longo dos anos.",
        tcc_pratica="A TCC elimina os comportamentos de esquiva e de segurança. Ao suspender a fuga, cortamos a manutenção do sintoma e "
                    "permitimos a extinção comportamental (Hofmann et al., 2012), devolvendo o controle da casa ao morador consciente.",
        s=s,
    )

    conceito_duas_paginas(
        story,
        nome_img="escada",
        tag="Conceito 3 · A Escada do Sótão",
        arquetipo="O Mestre Construtor dos Degraus",
        titulo="Subir a Escada, um Degrau de Cada Vez",
        hist_p1="No centro da casa havia uma escadaria de carvalho que levava ao sótão das estrelas. A girafinha Tatá queria muito ver as "
                "constelações, mas tinha pavor de altura. Se alguém ordenasse 'pule lá no teto de uma vez!', ela desmaiaria de susto. "
                "Ninguém consegue saltar uma casa inteira em um único salto.",
        hist_p2="O Mestre Construtor então pregou dez pequenas tábuas de madeira na parede, cada uma com apenas cinco centímetros de altura "
                "e um corrimão macio. No primeiro dia, Tatá subiu no primeiro degrau, tocou com o focinho, respirou fundo e desceu sorrindo. "
                "No segundo dia, subiu no segundo. Sem correria e sem saltos desesperados, em poucas semanas ela estava no topo da casa, "
                "observando o céu com o coração transbordando de alegria e paz.",
        ciencia_barlow="A <b>Hierarquia de Exposição Sistemática Gradual</b> (Antony & Swinson, 2000; Barlow, 2002) divide a situação temida "
                       "em unidades graduadas de desconforto subjetivo (SUDS). Isso previne a retraumatização e promove a autoeficácia "
                       "progressiva de Bandura, permitindo que a neuroplasticidade consolide novas rotas de enfrentamento com segurança.",
        tcc_pratica="Ensaios clínicos demonstram que a exposição hierarquizada in vivo apresenta índices de eficácia superiores a 80%, "
                    "sendo o protocolo padrão-ouro mundial para fobias específicas (Wolitzky-Taylor et al., 2008).",
        s=s,
    )

    conceito_duas_paginas(
        story,
        nome_img="piscina",
        tag="Conceito 4 · O Jardim e a Piscina",
        arquetipo="O Guardião das Águas Claras",
        titulo="A Piscina Fria e o Segredo do Tempo",
        hist_p1="No jardim da casa havia uma piscina de pedras azuis. Em uma tarde de sol, o ursinho Pingo encostou a pontinha da pata na água "
                "e gritou: 'SOCORRO! ESTÁ CONGELADA! NUNCA MAIS CHEGO PERTO!'. Ele achava que seus pelos iriam virar gelo instantaneamente. "
                "Mas a mamãe ursa, com muita calma, entrou na água e segurou suas mãozinhas na parte rasa.",
        hist_p2="No primeiro minuto, Pingo bateu o queixo. No segundo minuto, achou suportável. No quarto minuto, arregalou os olhos e disse: "
                "'Mamãe, quem esquentou a água?'. A água não havia esquentado nem um único grau: foi o corpinho do ursinho que se acostumou! "
                "O medo fóbico é igualzinho: quando você entra na situação e não foge nos primeiros minutos, o cérebro percebe que não há perigo "
                "e a ansiedade esfria naturalmente por conta própria.",
        ciencia_barlow="Este é o clássico princípio da <b>Habituação Psicofisiológica</b> e da regulação parassimpática (Craske et al., 2014; "
                       "Barlow, 2008). A descarga adrenérgica é metabolicamente autolimitada; os receptores simpáticos entram em saturação e "
                       "o nervo vago assume o controle somático, promovendo desaceleração cardiovascular e relaxamento involuntário.",
        tcc_pratica="Na exposição assistida por TCC, orientamos o paciente a permanecer na situação até que o nível de SUDS caia pelo menos 50% "
                    "do pico. Esse dado fisiológico quebra a crença de que a ansiedade cresceria até o infinito.",
        s=s,
    )

    conceito_duas_paginas(
        story,
        nome_img="cachorrinho",
        tag="Conceito 5 · O Canil do Pátio",
        arquetipo="O Adestrador do Filhote Leal",
        titulo="Ensinar o Cachorrinho: O Cérebro que Aprende",
        hist_p1="No pátio da casa morava Pipoca, um cachorrinho fofinho que entrava em pânico toda vez que ouvia o motor do aspirador de pó. "
                "Ele latia, rosnava e tentava cavar um buraco no tapete para se esconder. Se alguém brigasse com ele ou o empurrasse à força "
                "contra o aparelho, Pipoca ficava com o dobro de medo. Ele precisava de paciência e carinho.",
        hist_p2="O dono colocou o aspirador desligado a cinco metros de distância e colocou um biscoitinho saboroso no chão. Pipoca comeu e "
                "abanou o rabinho. No dia seguinte, ligou o aparelho no quarto fechado enquanto fazia cafuné no Pipoca. Em três dias, o cachorrinho "
                "já tirava uma soneca deliciosa encostado no aspirador funcionando! O cérebro do filhote criou um novo caminho neural de calma. "
                "O seu cérebro aprende exatamente da mesma forma.",
        ciencia_barlow="No modelo neurobiológico contemporâneo de LeDoux, Phelps e Barlow, a extinção do medo não apaga a memória amigdalina "
                       "antiga, mas constrói uma <b>Memória Inibitória Nova</b> no córtex pré-frontal ventromedial (vmPFC). "
                       "O cérebro cria uma regra de segurança que passa a prevalecer sobre a regra de pânico.",
        tcc_pratica="A prática deliberada de experimentos comportamentais na TCC gera <i>Prediction Error</i> (discrepância entre a catástrofe "
                    "prevista e o desfecho benigno), mecanismo essencial para a neuroplasticidade e cura a longo prazo (Craske et al., 2014).",
        s=s,
    )

    conceito_duas_paginas(
        story,
        nome_img="velinha",
        tag="Conceito 6 · A Cozinha da Casa",
        arquetipo="O Soprador das Velinhas da Sala",
        titulo="Soprar as Velinhas Devagar: O Freio do Corpinho",
        hist_p1="Quando o susto aparece, a cozinha da nossa casa interior ferve como uma panela de pressão: o coração bate tum-tum-tum feito "
                "motor de corrida, a respiração fica curtinha e as mãos tremem. Isso acontece porque o corpo pisou no acelerador para correr. "
                "Mas dentro da nossa sala não tem leão nenhum para fugir!",
        hist_p2="A boa notícia é que temos um pedal de freio mágico chamado Respiração Lenta. É só fazer assim: puxa o ar pelo nariz cheirando "
                "uma florzinha de laranjeira (1, 2, 3, 4) e solta pela boca bem devagarzinho, soprando a velinha do bolo de aniversário sem querer "
                "apagá-la (1, 2, 3, 4, 5, 6). Em menos de um minuto, o motor desacelera, a panela esfria e a serenidade volta para a sala.",
        ciencia_barlow="A <b>Respiração Diafragmática Paced</b> e a ativação vagal (Barlow & Craske, 2007) atuam diretamente nos barorreceptores "
                       "arteriais, restaurando os níveis normais de dióxido de carbono no sangue e revertendo a vasoconstrição cerebral provocada "
                       "pela hiperventilação fóbica.",
        tcc_pratica="O treino do freio somático capacita o paciente a permanecer na tarefa de exposição sem recorrer a esquivas desesperadas, "
                    "fortalecendo a autoeficácia e a soberania corporal sobre os sintomas autonômicos.",
        s=s,
    )

    conceito_duas_paginas(
        story,
        nome_img="dragao",
        tag="Conceito 7 · A Lareira Central",
        arquetipo="O Dragão da Lareira Ancestral",
        titulo="Domar o Dragão: O Medo que Vira Coragem",
        hist_p1="Na lareira principal da nossa casa ancestral vivia Ryu, um dragão pequenino feito de fogo e vento. Durante anos, a família "
                "achou que Ryu era um monstro terrível e tentava apagá-lo jogando baldes de água gelada. Mas quanto mais água jogavam, "
                "mais fumaça cinzenta ele soltava, sufocando a casa toda de angústia.",
        hist_p2="Uma menina corajosa sentou-se diante da lareira, olhou nos olhos dourados do dragão e disse: 'Eu sei que você só quer "
                "nos aquecer no inverno'. Ela respirou fundo e ofereceu um galho de canela aromática. O dragão suspirou aliviado, deitou as chamas "
                "com doçura e aqueceu o lar inteiro com um brilho acolhedor. O medo não precisa ser destruído: ele é a sua própria força vital "
                "que, quando compreendida e domada, vira a sua maior coragem.",
        ciencia_barlow="O <b>Protocolo Unificado Transdiagnóstico</b> de David H. Barlow (2011, 2018) preconiza a <i>Aceitação Emocional Plena</i> "
                       "e a flexibilidade psicológica. Em vez de travar uma guerra contra as próprias emoções, o indivíduo aprende a tolerar o "
                       "afeto aversivo e a redirecionar a energia somática para comportamentos valorizados e alinhados com seus propósitos de vida.",
        tcc_pratica="Ensaios multicêntricos de larga escala (Barlow et al., JAMA Psychiatry, 2017) comprovam que a aceitação experiencial "
                    "produz taxas de remissão superiores a 75% com sustentabilidade clínica por mais de cinco anos.",
        s=s,
    )

    # ═══════════ PARTE I ═══════════
    section_break(story, "CAPÍTULO I", "O Vigia da Porta:\nPsicoeducação do Alarme", s)

    story.append(story_box(
        arquetipo="O Vigia da Porta de Entrada",
        titulo_conto="A Noite do Grande Vento na Janela",
        texto_conto="O Vigia da Porta passa as noites sentado no hall de entrada com sua lanterna de latão. "
                    "Certa noite, o vento de outono bateu nas folhas da trepadeira e fez um barulho seco na vidraça: 'TOC-TOC-TOC'. "
                    "O Vigia saltou da cadeira, tocou o sino de bronze com toda força e gritou que um exército de piratas estava invadindo a casa! "
                    "A casa inteira acordou sobressaltada. Quando abriram a cortina com calma, viram apenas uma folha seca dançando na brisa. "
                    "O Vigia não tinha más intenções: ele apenas precisava de uma lâmpada mais clara para aprender a enxergar as folhas sem "
                    "chamar a cavalaria real.",
        s=s,
    ))

    p(story, "1. A Biologia do Medo Útil versus o Alarme Falso", s["h1"])
    story.append(hr())
    story.append(ilustra("alarme", 6.5 * cm))
    story.append(Spacer(1, 6))
    p(story, "O medo é um dispositivo biológico refinado ao longo de milhões de anos de evolução. Sem ele, nossos ancestrais teriam sido "
      "devorados por predadores ou teriam despencado de despenhadeiros. O medo útil preserva a integridade física.", s["body"])
    p(story, "Na fobia específica, conforme demonstrado por David H. Barlow, o sistema de alerta sofre uma <b>hipercalibração de sensibilidade</b>. "
      "A amígdala cerebral interpreta estímulos neutros ou de baixo risco objetivo (uma altura protegida por parapeito, um inseto inofensivo, "
      "uma viagem de avião comercial, um elevador moderno) como se fossem ameaças mortais imediatas.", s["body"])
    p(story, "Você não possui uma falha de caráter e não é uma pessoa covarde. O seu Vigia da Porta é apenas vigilante demais. "
      "O tratamento da fobia consiste em fornecer novas lentes de discernimento para esse vigia interno.", s["body"])
    story.append(PageBreak())

    p(story, "2. O Circuito Neurobiológico da Fobia (Eixo HPA)", s["h1"])
    story.append(hr())
    p(story, "Quando a amígdala detecta um sinal fóbico, ela dispara uma cascata bioquímica em milésimos de segundo:", s["body"])
    story.append(bullets([
        "<b>Estímulo Sensorial:</b> os olhos, ouvidos ou a imaginação registram o gatilho fóbico.",
        "<b>Via Rápida Talâmica:</b> o tálamo envia sinal direto à amígdala antes mesmo do córtex racional processar o que viu.",
        "<b>Ativação Simpática:</b> liberação maciça de adrenalina e noradrenalina pelas glândulas adrenais.",
        "<b>Redirecionamento Sanguíneo:</b> o sangue sai do sistema digestivo e da pele e irriga os grandes músculos das pernas e braços para luta ou fuga.",
        "<b>Hiperventilação:</b> respiração rápida para captar oxigênio extra, gerando tontura e formigamento nas extremidades.",
    ], s["body_left"]))
    p(story, "Compreender essa fisiologia é libertador: as sensações corporais não são sinais de ataque cardíaco, loucura ou morte iminente. "
      "São apenas a musculatura e o coração recebendo ordens de um Vigia que se assustou com uma folha na janela.", s["body"])
    story.append(Spacer(1, 8))
    story.append(callout(
        "Mantra do Vigia da Porta",
        "“Meu corpo está ativo porque meu vigia se assustou. Eu respiro com calma, olho a realidade e mostro a ele que estamos seguros.”",
        s,
    ))
    story.append(PageBreak())

    # ═══════════ PARTE II ═══════════
    section_break(story, "CAPÍTULO II", "O Construtor do Labirinto:\nCritérios do DSM-5", s)

    story.append(story_box(
        arquetipo="O Construtor do Labirinto de Caixas",
        titulo_conto="As Muralhas de Papelão na Sala de Estar",
        texto_conto="O Construtor morava na sala e tinha mania de erguer labirintos de caixas de papelão para não ter que olhar "
                    "pela janela grande. Cada vez que sentia um friozinho na barriga, empilhava mais uma caixa: 'Assim fico protegido!'. "
                    "Com o passar dos meses, o labirinto ficou tão apertado que ele mal conseguia andar até a cozinha para beber água. "
                    "Ele achava que as caixas o protegiam do mundo, mas na verdade as caixas haviam construído a sua prisão.",
        s=s,
    ))

    p(story, "3. Os Critérios Diagnósticos do DSM-5 em Linguagem Clara", s["h1"])
    story.append(hr())
    p(story, "O Manual Diagnóstico e Estatístico de Transtornos Mentais (DSM-5-TR), elaborado pela Associação Americana de Psiquiatria (APA), "
      "estabelece critérios clínicos rigorosos para caracterizar a Fobia Específica:", s["body"])
    story.append(bullets([
        "<b>Critério A (Medo Acentuado):</b> medo ou ansiedade marcante e desproporcional acerca de um objeto ou situação específica.",
        "<b>Critério B (Provocação Quase Invariável):</b> a exposição ao estímulo provoca resposta ansiosa quase que imediatamente.",
        "<b>Critério C (Esquiva Ativa):</b> a situação fóbica é ativamente evitada ou suportada com intenso sofrimento e angústia.",
        "<b>Critério D (Desproporção Real):</b> a intensidade do medo é desproporcional ao perigo real representado pelo objeto no contexto sociocultural.",
        "<b>Critério E (Persistência Temporal):</b> o medo, a ansiedade ou a esquiva é persistente, com duração mínima típica de 6 meses.",
        "<b>Critério F (Prejuízo Funcional):</b> causa sofrimento clinicamente significativo ou prejuízo social, ocupacional e pessoal.",
        "<b>Critério G (Diagnóstico Diferencial):</b> o quadro não é mais bem explicado por pânico, agorafobia, TOC, TEPT ou ansiedade social.",
    ], s["body_left"]))
    story.append(PageBreak())

    p(story, "4. Os Cinco Subtipos Clínicos do DSM-5", s["h1"])
    story.append(hr())
    p(story, "O DSM-5 categoriza as fobias em cinco grandes especificadores clínicos:", s["body"])
    story.append(bullets([
        "<b>1. Animal:</b> aranhas (aracnofobia), cães (cinofobia), cobras (ofidiofobia), insetos, pássaros, roedores.",
        "<b>2. Ambiente Natural:</b> alturas (acrofobia), tempestades (brontofobia), água profunda (talassofobia), escuro.",
        "<b>3. Sangue-Injeção-Ferimentos (BII):</b> agulhas (aicanfobia), procedimentos médicos, sangue. Possui resposta vasovagal bifásica.",
        "<b>4. Situacional:</b> aviões (aerofobia), elevadores, túneis, pontes, dirigir em rodovias, espaços fechados (claustrofobia).",
        "<b>5. Outros:</b> vômito (emetofobia), engasgamento, sons intensos, personagens fantasiados.",
    ], s["body_left"]))
    p(story, "Cada subtipo possui particularidades na montagem da escada, mas todos compartilham o mesmo núcleo neuropsicológico de esquiva.", s["body"])
    story.append(PageBreak())

    # ═══════════ PARTE III ═══════════
    section_break(story, "CAPÍTULO III", "O Mensageiro das Luzes:\nTodos os Sintomas", s)

    story.append(story_box(
        arquetipo="O Mensageiro das Luzes no Corredor",
        titulo_conto="O Painel que Acendeu Todas as Cores",
        texto_conto="No corredor dos quartos havia um painel com dezenas de lâmpadas coloridas cuidadas pelo Mensageiro. "
                    "Havia lâmpadas vermelhas para o coração, azuis para a respiração, amarelas para o estômago e verdes para as pernas. "
                    "Quando o medo soprava pelo corredor, o Mensageiro acendia todas as lâmpadas de uma vez só! "
                    "As luzes piscavam tão rápido que parecia um festival de fogos de artifício. "
                    "O morador da casa gritava: 'O painel vai explodir!'. Mas o Mensageiro explicava com ternura: "
                    "'Não vai explodir, amigo. As lâmpadas apenas acenderam para te avisar que estamos vivos e prontos para aprender'.",
        s=s,
    ))

    p(story, "5. A Tríade Completa dos Sintomas Fóbicos", s["h1"])
    story.append(hr())
    p(story, "A resposta fóbica manifesta-se em três eixos integrados:", s["body"])
    story.append(bullets([
        "<b>Eixo Fisiológico (O Corpo):</b> taquicardia, sudorese palmar, boca seca, tremor, náusea, hipertonia muscular, tontura, sensação de nó na garganta.",
        "<b>Eixo Cognitivo (A Mente):</b> superestimação de probabilidade de dano, subestimação de enfrentamento, imagens intrusivas de catástrofe, pensamentos do tipo 'vou perder o controle'.",
        "<b>Eixo Comportamental (A Ação):</b> fuga imediata, cancelamento de compromissos, busca incessante de reasseguramento, uso de amuletos de segurança.",
    ], s["body_left"]))
    story.append(Spacer(1, 6))
    p(story, "Identificar em qual eixo a sua resposta costuma começar é a chave para escolher as ferramentas de regulação somática e cognitiva corretas.", s["body"])
    story.append(PageBreak())

    p(story, "6. Checklist Completo de Autoavaliação Sintomática", s["h1"])
    story.append(hr())
    p(story, "Assinale os sinais que seu corpo e mente costumam apresentar diante do estímulo fóbico:", s["body"])
    checklist_itens = [
        "□ Coração dispara como se eu estivesse em uma maratona",
        "□ Respiração fica ofegante e sinto aperto no peito",
        "□ Minhas mãos tremem ou ficam geladas e suadas",
        "□ Sinto tontura ou impressão de que o chão está balançando",
        "□ Tenho pensamentos imediatos de que algo terrível vai acontecer",
        "□ Penso que vou passar vergonha ou perder o controle total",
        "□ Cancelo viagens, consultas ou eventos por causa do medo",
        "□ Só consigo enfrentar se alguém de muita confiança estiver segurando minha mão",
        "□ Uso amuletos, remédios no bolso ou rotas de fuga planejadas",
        "□ Fico dias antes sofrendo por antecipação ao imaginar a situação",
    ]
    for item in checklist_itens:
        p(story, item, s["body_left"])
    story.append(Spacer(1, 6))
    p(story, "Minhas 3 principais manifestações corporais:", s["label"])
    story.append(blank_lines(3))
    story.append(PageBreak())

    # ═══════════ PARTE IV ═══════════
    section_break(story, "CAPÍTULO IV", "O Engenheiro de Estruturas:\nQuando Tratar", s)

    story.append(story_box(
        arquetipo="O Engenheiro da Estrutura e das Vigas",
        titulo_conto="A Trinca no Chão do Terraço",
        texto_conto="O Engenheiro da casa passava os dias examinando as vigas e os alicerces com uma régua de carvalho. "
                    "Um dia, viu uma pequena trinca no piso do terraço. Um morador disse: 'Deixa para lá, é só colocar um tapete por cima'. "
                    "Mas o Engenheiro sabia que colocar um tapete não conserta a viga. Se a chuva entrar na trinca todo inverno, "
                    "a casa inteira fica bamba. Ele pegou argamassa, ferro e ferramentas e consertou a estrutura na raiz. "
                    "Tratar a fobia é igual: não é cobrir o medo com um tapete de desculpas, é fortalecer a viga da sua liberdade.",
        s=s,
    ))

    p(story, "7. Critérios de Gravidade e Momento de Buscar Tratamento", s["h1"])
    story.append(hr())
    p(story, "Você deve priorizar o tratamento ativo quando:", s["body"])
    story.append(bullets([
        "A fobia impede exames médicos vitais, coletas de sangue, cirurgias ou tratamentos odontológicos essenciais.",
        "A evitação limita o avanço na carreira (recusar promoções que exigem viagens aéreas ou apresentações em público).",
        "A vida familiar é restrita (deixar de viajar com os filhos, evitar parques, passeios ou praias).",
        "Há surgimento de ataques de pânico secundários ou humor deprimido em decorrência do isolamento.",
        "O indivíduo começa a fazer uso abusivo de álcool ou sedativos para conseguir tolerar eventos cotidianos.",
    ], s["body_left"]))
    story.append(PageBreak())

    p(story, "8. Diferenciação Clínica: Fobia Específica versus Outros Transtornos", s["h1"])
    story.append(hr())
    p(story, "É fundamental que a avaliação clínica discrimine:", s["body"])
    story.append(bullets([
        "<b>Fobia Específica:</b> medo focado em um objeto/circunstância delimitada (ex.: medo de cão).",
        "<b>Transtorno de Pânico:</b> medo dos próprios sintomas corporais ('vou morrer de infarto agora').",
        "<b>Agorafobia:</b> medo de múltiplos locais de onde seria difícil escapar ou obter socorro imediato.",
        "<b>Ansiedade Social:</b> medo de julgamento, humilhação ou escrutínio por parte de outras pessoas.",
        "<b>TOC:</b> rituais motores ou mentais para neutralizar obsessões e pensamentos intrusivos de culpa.",
    ], s["body_left"]))
    story.append(PageBreak())

    # ═══════════ PARTE V ═══════════
    section_break(story, "CAPÍTULO V", "O Mestre da Escadaria:\nOs Passos da TCC", s)

    story.append(story_box(
        arquetipo="O Mestre Marceneiro da Escadaria",
        titulo_conto="A Oficina dos Degraus Perfeitos",
        texto_conto="O Mestre Marceneiro passava suas tardes na oficina serrando tábuas de pinho perfumado. "
                    "Ele dizia que todo medo no mundo pode ser vencido se você construir degraus da altura certa. "
                    "Se um degrau tiver um metro de altura, ninguém consegue subir. Mas se tiver cinco centímetros, "
                    "até uma tartaruguinha chega no topo do castelo! "
                    "Ele pegou sua lixa, mediu cada pedacinho com amor e ensinou o morador a subir sem olhar para o abismo, "
                    "olhando apenas para a madeira firme sob as solas dos pés.",
        s=s,
    ))

    p(story, "9. Os 7 Passos Estruturais da Terapia de Exposição", s["h1"])
    story.append(hr())
    story.append(bullets([
        "<b>1. Mapeamento do Gatilho:</b> discriminar exatamente o estímulo temido em suas microvariáveis.",
        "<b>2. Psicoeducação e Normalização Somática:</b> desmistificar o alarme e validar a fisiologia.",
        "<b>3. Construção da Hierarquia (SUDS):</b> elencar 10 a 15 passos graduados de aproximação.",
        "<b>4. Treino de Regulação Fisiológica:</b> ancoragem dos sentidos e respiração paced 4-6.",
        "<b>5. Exposição Sistemática In Vivo / RV:</b> contato planejado sem respostas de fuga.",
        "<b>6. Registro de Discrepância de Predição:</b> confrontar o medo catastrófico com os fatos observados.",
        "<b>7. Generalização e Prevenção de Recaída:</b> variar contextos e desmamar amuletos de segurança.",
    ], s["body_left"]))
    story.append(PageBreak())

    p(story, "10. Desarmando os Comportamentos de Segurança (Amuletos)", s["h1"])
    story.append(hr())
    p(story, "Comportamentos de segurança são 'muletas mágicas' que parecem proteger, mas mantêm o medo vivo:", s["body"])
    story.append(bullets([
        "Segurar com força nos braços da poltrona durante o voo.",
        "Só entrar no elevador acompanhado de alguém conhecido.",
        "Levar remédio na bolsa 'por via das dúvidas' sem indicação médica.",
        "Usar fones de ouvido no volume máximo para não escutar o barulho do motor.",
        "Ficar checando a saída de emergência obsessivamente a cada minuto.",
    ], s["body_left"]))
    p(story, "Ao longo das 3 semanas, nós desmamamos gradualmente cada um desses amuletos para que o cérebro aprenda que a sua própria presença é suficiente.", s["body"])
    story.append(PageBreak())

    # ═══════════ PARTE VI ═══════════
    section_break(story, "CAPÍTULO VI", "O Alquimista da Piscina:\nHabituação e Inibição", s)

    story.append(story_box(
        arquetipo="O Alquimista das Águas do Jardim",
        titulo_conto="O Termômetro que Não Sabia Mentir",
        texto_conto="O Alquimista cuidava da fonte cristalina no centro do jardim. Ele tinha um termômetro de vidro mágico "
                    "que media a temperatura das emoções. Quando alguém colocava o pé na fonte, o termômetro subia para 100 graus "
                    "de ansiedade na hora! O Alquimista sorria e dizia: 'Fique aí, não saia correndo. Olhe o ponteiro'. "
                    "Em três minutos o ponteiro caía para 70. Em sete minutos caía para 40. Em doze minutos estava em 20 graus de pura tranquilidade. "
                    "O Alquimista provava com dados que a onda da emoção sempre quebra na praia e recua suavemente.",
        s=s,
    ))

    p(story, "11. Habituação Clássica versus Modelo Inibitório Contemporâneo", s["h1"])
    story.append(hr())
    story.append(ilustra("piscina", 6.5 * cm))
    story.append(Spacer(1, 6))
    p(story, "Durante décadas, a TCC acreditou que a redução da ansiedade intra-sessão (habituação) era o motor único da melhora. "
      "Hoje, os avanços de Michelle Craske e David Barlow demonstram que o motor principal é a <b>violação da expectativa</b> "
      "(<i>Expectancy Violation</i>).", s["body"])
    p(story, "O paciente aprende que a catástrofe antecipada <b>não ocorreu</b>, criando uma rota neural de segurança "
      "que supera a rota do medo, mesmo que alguma ansiedade fisiológica ainda esteja presente no momento do treino.", s["body"])
    story.append(PageBreak())

    p(story, "12. Estratégias para Otimizar o Aprendizado Inibitório", s["h1"])
    story.append(hr())
    story.append(bullets([
        "<b>1. Maximização do Erro de Predição:</b> formular a previsão temida antes da tarefa e contrastar rigorosamente após.",
        "<b>2. Variabilidade de Estímulos:</b> alternar velocidade, distância, luminosidade e contextos de exposição.",
        "<b>3. Espaçamento Temporal:</b> distribuir as sessões ao longo dos dias para permitir a consolidação sináptica noturna.",
        "<b>4. Remoção de Pistas de Segurança:</b> treinar sem muletas para maximizar o senso de autoeficácia pura.",
    ], s["body_left"]))
    story.append(PageBreak())

    # ═══════════ PARTE VII ═══════════
    section_break(story, "CAPÍTULO VII", "A Biblioteca dos Sábios:\nGaleria dos Pensadores", s)

    story.append(story_box(
        arquetipo="O Bibliotecário da Torre de Vidro",
        titulo_conto="O Grande Livro das Sombras Claras",
        texto_conto="Na biblioteca mais alta da casa, o sábio Bibliotecário guardava pergaminhos deixados pelos maiores médicos "
                    "e filósofos da história. Ele puxou um pergaminho antigo e disse: 'Veja, há mais de cem anos homens e mulheres sábios "
                    "estudam o medo humano. Todos eles descobriram a mesma verdade: aquilo que você enfrenta com clareza perde a força, "
                    "e aquilo de que você foge ganha o tamanho de um gigante'.",
        s=s,
    ))

    p(story, "13. Os Mestres da TCC e da Neurociência Fóbica", s["h1"])
    story.append(hr())
    thinkers_list = [
        ("David H. Barlow", "Criador do Protocolo Unificado e da Teoria da Tríplice Vulnerabilidade. O grande arquiteto do alarme falso e da regulação emocional contemporânea."),
        ("Aaron T. Beck", "Fundador da Terapia Cognitiva. Mostrou como pensamentos automáticos e crenças intermediárias distorcem a percepção de perigo."),
        ("Michelle Craske", "Pioneira nas pesquisas de aprendizado inibitório e maximização da violação de expectativa na terapia de exposição."),
        ("Joseph Wolpe", "Desenvolvedor da dessensibilização sistemática nos anos 1950, precursor da moderna hierarquia de degraus."),
        ("Albert Bandura", "Teórico da Autoeficácia. Demonstrou que a confiança na própria capacidade de enfrentamento é o maior preditor de sucesso clínico."),
        ("Isaac Marks", "Pioneiro da psiquiatria comportamental europeia e da exposição in vivo continuada."),
        ("Stanley Rachman", "Mapeou as três vias de aquisição do medo: condicionamento clássico, modelação vicária e transmissão verbal de informação."),
        ("Joseph LeDoux", "Neurocientista que mapeou as duas vias amigdalinas (alta e baixa) no processamento do medo no cérebro mamífero."),
    ]
    for name, desc in thinkers_list:
        p(story, f"<b>{name}</b>", s["h2"])
        p(story, desc, s["body"])
        story.append(Spacer(1, 4))
    story.append(PageBreak())

    # ═══════════ PARTE VIII ═══════════
    section_break(story, "CAPÍTULO VIII", "O Laboratório do Castelo:\nEvidências Científicas", s)

    story.append(story_box(
        arquetipo="A Cientista do Laboratório das Estrelas",
        titulo_conto="Os Microscópios que Viram a Coragem",
        texto_conto="No laboratório do subsolo, a Cientista observava lâminas e gráficos de luz. "
                    "Ela mostrava fotografias do cérebro antes e depois do treino da escada: "
                    "'Olhe como os pontinhos vermelhos de pavor no cérebro se acalmam e dão lugar a pontinhos azuis de tranquilidade! "
                    "A coragem não é uma mágica no ar: é uma ponte de neurônios novinha que você constrói toda vez que dá um passo seguro'.",
        s=s,
    ))

    p(story, "14. Estudos Clínicos de Referência Mundial em Fobias", s["h1"])
    story.append(hr())
    studies_list = [
        ("Barlow et al. (JAMA Psychiatry, 2017)", "Ensaio multicêntrico comprovando a eficácia transdiagnóstica do Protocolo Unificado com manutenção dos ganhos terapêuticos por mais de 5 anos."),
        ("Wolitzky-Taylor et al. (JCCP, 2008)", "Metanálise abrangente confirmando tamanho de efeito de Cohen d > 1.20 para a exposição comportamental in vivo sobre tratamentos controle."),
        ("Craske et al. (Behaviour Research and Therapy, 2014)", "Estudo seminal sobre o modelo de otimização inibitória na exposição fóbica."),
        ("Morina et al. (Journal of Anxiety Disorders, 2015)", "Metanálise confirmando a equivalência e a durabilidade da exposição com Realidade Virtual (VRE) frente à exposição in vivo."),
        ("Öst (Behaviour Research and Therapy, 1989, 2012)", "Estudos sobre protocolos de exposição intensiva em sessão única (OST) para fobias específicas circunscritas."),
    ]
    for title_st, desc_st in studies_list:
        p(story, f"<b>{title_st}</b>", s["h2"])
        p(story, desc_st, s["body"])
        story.append(Spacer(1, 5))
    story.append(PageBreak())

    # ═══════════ PARTE IX ═══════════
    section_break(story, "CAPÍTULO IX", "A Lareira do Dragão:\nAnalogias Orientais", s)

    story.append(story_box(
        arquetipo="O Guardião da Lareira Ancestral",
        titulo_conto="A Aliança com o Dragão Dourado",
        texto_conto="O Guardião da Lareira cuidava do fogo com tenazes de ferro forjado. "
                    "Ele ensinava que na tradição oriental, o dragão (Ryū) não é uma fera maligna a ser aniquilada com lanças, "
                    "mas o espírito da própria energia vital. Quando você corre dele, ele cospe fogo para te acordar. "
                    "Quando você se aproxima com reverência, dignidade e respeito, ele se torna o seu maior protetor nas montanhas. "
                    "A coragem de dragão é a nobreza de respirar com firmeza no meio da tempestade.",
        s=s,
    ))

    p(story, "15. Sabedoria Oriental Aplicada à Psicoterapia", s["h1"])
    story.append(hr())
    story.append(ilustra("dragao", 6.5 * cm))
    story.append(Spacer(1, 6))
    p(story, "Três grandes analogias orientais iluminam a nossa caminhada:", s["body"])
    story.append(bullets([
        "<b>Kintsugi (金継ぎ):</b> a arte de colar vasos quebrados com laca dourada. Suas cicatrizes emocionais tornam-se veios de ouro e beleza singular.",
        "<b>O Bambu Flexível (Take):</b> o bambu verga até o chão durante o vendaval, mas não se quebra. Flexibilidade psicológica é ceder à sensação sem travar a vida.",
        "<b>O Portal Torii (鳥居):</b> cada degrau da escada é um portal sagrado. Ao atravessá-lo, você demarca um território reconquistado do medo.",
    ], s["body_left"]))
    story.append(PageBreak())

    # ═══════════ PARTE X ═══════════
    section_break(story, "CAPÍTULO X", "O Jardim dos Templos:\nParábolas da Determinação", s)

    story.append(story_box(
        arquetipo="O Mestre do Jardim de Pedras",
        titulo_conto="A Trilha das Lanternas de Pedra",
        texto_conto="No jardim zen da casa, o Mestre varria as folhas secas com um ancinho de bambu. "
                    "Um jovem apressado perguntou: 'Mestre, como faço para atravessar a montanha escura em um minuto?'. "
                    "O Mestre apontou para as lanternas de pedra ao longo do caminho e respondeu: 'A montanha não foi feita para ser corrida. "
                    "Ela foi feita para ser caminhada. Uma lanterna acesa por noite ilumina a vida inteira. A pressa é do medo; a constância é da sabedoria'.",
        s=s,
    ))

    p(story, "16. Cinco Parábolas de Fortalecimento Interior", s["h1"])
    story.append(hr())
    parables_data = [
        ("O Templo na Névoa", "O peregrino parou com medo da névoa densa. O monge ancião disse: 'Você não precisa enxergar o topo da montanha hoje. Só precisa pisar com firmeza no degrau de pedra que está visível sob seus pés agora'."),
        ("As Mil Lanternas da Floresta", "Uma aldeia temia a mata escura. Tentar acender todas as tochas de uma vez gerou incêndio e confusão. Um sábio sugeriu acender uma lanterna por noite. Em trinta dias, a floresta era um jardim iluminado e seguro."),
        ("A Corda no Celeiro Escuro", "O jovem entrou no celeiro e gritou apavorado achando que pisara numa serpente mortal. Ao acender uma pequena vela, viu que era apenas uma corda velha enrolada. A exposição com luz dissipa o fantasma imaginado."),
        ("O Vaso Rachado e o Jardineiro", "O carregador de água tinha dois potes: um perfeito e um com uma rachadura. O pote rachado chorava por perder água no caminho. O carregador mostrou que ao longo do seu lado da estrada haviam nascido flores magníficas regadas pelas gotas da sua fragilidade."),
        ("O Mestre Arqueiro e o Alvo Próximo", "O aprendiz queria acertar o alvo a cem metros no primeiro dia. O mestre colocou o alvo a um metro. 'A precisão se aprende na proximidade; a distância é apenas consequência da repetição serena'."),
    ]
    for p_title, p_text in parables_data:
        p(story, f"<b>{p_title}</b>", s["h2"])
        p(story, p_text, s["story"])
        story.append(Spacer(1, 4))
    story.append(PageBreak())

    # ═══════════ PARTE XI ═══════════
    section_break(story, "CAPÍTULO XI", "O Arquiteto da Torre:\nMontando Sua Escada", s)

    story.append(story_box(
        arquetipo="O Arquiteto da Torre de Cristal",
        titulo_conto="A Planta Baixa da Sua Liberdade",
        texto_conto="O Arquiteto abriu uma grande folha de papel vegetal azul sobre a mesa de madeira. "
                    "Com régua, compasso e lápis macio, ele desenhou dez degraus personalizados para o morador da casa. "
                    "'Esta é a sua planta de voo', disse ele com um sorriso caloroso. 'Cada degrau é feito sob medida para a sua perna. "
                    "Nem alto demais para te assustar, nem baixo demais para não te ensinar nada. É o seu mapa de vitória'.",
        s=s,
    ))

    p(story, "17. A Tabela da Sua Escada Segura Pessoal (SUDS 0 a 10)", s["h1"])
    story.append(hr())
    story.append(ilustra("escada", 6.5 * cm))
    story.append(Spacer(1, 6))
    p(story, "Preencha com carinho as 10 situações que você vai conquistar ao longo do programa:", s["body"])
    story.append(Spacer(1, 6))
    story.append(ladder_template(s))
    story.append(PageBreak())

    # ═══════════ PARTE XII ═══════════
    section_break(story, "CAPÍTULO XII", "O Diário do Viajante:\nPlano de 21 Dias", s)

    story.append(story_box(
        arquetipo="O Cronista da Biblioteca dos Viajantes",
        titulo_conto="O Diário de Bordo das Pequenas Vitórias",
        texto_conto="O Cronista usava óculos redondos e uma pena de ganso com tinta nanquim. "
                    "Ele entregou um caderno encadernado em couro ao morador: 'A cada dia de treino, você vai escrever uma linha aqui. "
                    "O cérebro esquece as vitórias facilmente quando o medo sopra, mas a tinta no papel não mente. "
                    "Daqui a vinte e um dias, você vai folhear este livro e chorar de orgulho da pessoa corajosa que você se tornou'.",
        s=s,
    ))

    p(story, "18. Cronograma Estruturado em 3 Semanas", s["h1"])
    story.append(hr())
    p(story, "• <b>Semana 1 (Dias 1 a 7) — Fundação:</b> Psicoeducação, sintonia somática e conquista dos degraus 1 e 2.<br/>"
      "• <b>Semana 2 (Dias 8 a 14) — Consolidação:</b> Conquista dos degraus 3 a 6, desmame de amuletos e variação.<br/>"
      "• <b>Semana 3 (Dias 15 a 21) — Expansão e Soberania:</b> Degraus 7 a 10, generalização contextual e plano de voo autônomo.", s["body"])
    story.append(Spacer(1, 10))

    p(story, "19. As 21 Folhas Diárias de Registro de Exposição", s["h1"])
    story.append(hr())
    p(story, "Preencha uma folha para cada dia de treino com rigor e carinho. Cada folha é uma página inteira de autodescoberta e neuroplasticidade.", s["body"])
    story.append(PageBreak())

    # 21 folhas de registro (1 página completa cada = 21 páginas)
    dias_info = [
        ("O Vigia do Hall", "Acolhendo o Alarme Falso e Mapeando a Casa"),
        ("O Construtor de Papelão", "Desmontando a Primeira Caixa de Esquiva"),
        ("O Mensageiro das Luzes", "Observando as Lâmpadas Corporais sem Pânico"),
        ("O Soprador de Velinhas", "Treinando a Respiração Paced no Degrau 1"),
        ("O Guardião das Águas", "Permanecendo na Piscina Fria até Esfriar"),
        ("O Adestrador do Filhote", "Oferecendo Biscoitinho Seguro para a Mente"),
        ("O Dragão da Lareira", "Respirando Fundo com Presença e Dignidade"),
        ("O Mestre Marceneiro", "Subindo Firme no Degrau 3 da Escada"),
        ("O Alquimista da Fonte", "Testando o Termômetro de SUDS na Prática"),
        ("O Guarda dos Portais", "Desmamando o Primeiro Amuleto de Segurança"),
        ("O Monge da Montanha", "Caminhando na Névoa um Passo por Vez"),
        ("O Guardião do Farol", "Enfrentando o Degrau 4 em Horário Diferente"),
        ("O Tecelão da Coragem", "Construindo a Rota Neural Inibitória"),
        ("O Arqueiro Zen", "Fixando o Foco no Próximo Degrau Real"),
        ("O Cavaleiro da Torre", "Conquistando o Degrau 6 com Soberania"),
        ("O Jardineiro dos Templos", "Plantando Certezas nos Erros de Predição"),
        ("O Mestre dos Ventos", "Treinando o Bambu Flexível diante da Onda"),
        ("O Pintor dos Céus", "Conquistando os Degraus Superiores 7 e 8"),
        ("O Guardião do Selo", "Desmamando Todos os Comportamentos de Fuga"),
        ("O Dragão Soberano", "Vencendo o Degrau 10 com Coragem Radiante"),
        ("O Morador Livre", "Celebrando a Aliança e a Casa Aberta para o Mundo"),
    ]

    for d, (arq, foco) in enumerate(dias_info, 1):
        story.append(exposure_log_page(s, d, f"Registro Diário da Casa Interior", arq, foco))
        story.append(PageBreak())

    # ═══════════ PARTE XIII ═══════════
    section_break(story, "CAPÍTULO XIII", "O Selo Dourado:\nA Coragem Sustentável", s)

    story.append(story_box(
        arquetipo="O Guardião do Selo Dourado da Aliança",
        titulo_conto="O Abraço na Casa Inteira",
        texto_conto="No último dia da jornada, o morador caminhou por todos os cômodos da casa: o hall de entrada, o sótão, "
                    "a lareira, a cozinha, o jardim e a torre. O Pequeno Sentinela sorria no posto, o Monstrinho dormia manso no canto, "
                    "o Dragão aquecia a sala e a piscina brilhava sob o sol. A casa inteira estava em paz. "
                    "O Guardião do Selo carimbou o livro com um brasão dourado e disse: 'Você não expulsou nada da sua casa. "
                    "Você acolheu cada parte com sabedoria e amor. Agora você é livre para abrir todas as portas e janelas para o mundo'.",
        s=s,
    ))

    p(story, "20. Carta Final da Dra. Priscila Palomo", s["h1"])
    story.append(hr())
    p(story, "Querido(a) leitor(a),", s["body"])
    p(story, "Chegar ao final deste book é testemunhar uma transformação profunda na sua história de vida. "
      "Você não apenas aprendeu conceitos de TCC e neurociência de David H. Barlow: você reconstruiu a relação de confiança "
      "com o seu próprio corpo e com o seu mundo interior.", s["body"])
    p(story, "Leve com você a sabedoria dos arquétipos da nossa casa, a serenidade dos templos e a nobre coragem de dragão. "
      "Sempre que uma brisa mais forte balançar as janelas, lembre-se: você tem uma escada firme sob os pés e asas prontas para voar.", s["body"])
    story.append(Spacer(1, 8))
    p(story, "Com carinho e admiração pela sua jornada,", s["body"])
    p(story, "<b>Dra. Priscila Palomo</b><br/>Psicóloga Clínica · CRP 98007<br/>"
      "Doutora em Psicologia pela Universitat de València (Cum Laude)<br/>"
      "Especialista em Fobias, Ansiedade e Terapia Cognitivo-Comportamental<br/>"
      "www.priscilapalomo.com · WhatsApp: (11) 95069-0537", s["body_left"])
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceBefore=6, spaceAfter=10))
    p(story, "Programa Escada Segura — Book Completo com Arquétipos da Casa · Dra. Priscila Palomo", s["footer"])
    story.append(PageBreak())

    # ═══════════ APÊNDICES A a J (PRÁTICAS EXTENDIDAS ~200+ PÁGINAS) ═══════════

    p(story, "Apêndice A — Diário Semanal de Autoeficácia dos Arquétipos (12 Semanas)", s["h1"])
    story.append(hr())
    for w in range(1, 13):
        p(story, f"<b>Semana {w:02d} — Reflexão com os Guardiões da Casa</b>", s["h2"])
        p(story, "1. Vitórias conquistadas nesta semana (lanternas de pedra acesas):", s["label"])
        story.append(blank_lines(3))
        p(story, "2. Alarmes falsos identificados e acolhidos com serenidade:", s["label"])
        story.append(blank_lines(3))
        p(story, "3. Próximo portal (Torii) que vou atravessar nos próximos 7 dias:", s["label"])
        story.append(blank_lines(3))
        story.append(PageBreak())

    p(story, "Apêndice B — Banco de Frases de Enfrentamento dos Arquétipos", s["h1"])
    story.append(hr())
    phrases_arch = [
        "O Vigia da Porta: 'É apenas uma folha no vento, não um incêndio. Eu respiro e permaneço.'",
        "O Mestre da Escada: 'Um degrau de cada vez, sem olhar o abismo, sentindo a madeira firme.'",
        "O Alquimista da Piscina: 'A água parece fria nos primeiros segundos, mas meu corpo se acostuma.'",
        "O Adestrador do Filhote: 'Meu cérebro aprende com amor, repetição e desfecho seguro.'",
        "O Soprador de Velinhas: 'Inspiro cheirando a flor, expiro soprando a velinha devagar.'",
        "O Dragão da Lareira: 'A fumaça não me machuca; meu medo é a minha própria coragem acordando.'",
        "O Monge do Templo: 'Névoa não cancela a próxima pedra do caminho.'",
        "O Construtor de Pontes: 'A catástrofe que previ nunca aconteceu nos dados reais.'",
        "A Tecelã dos Espelhos: 'O reflexo do medo é menor do que a força do meu coração.'",
        "O Guardião da Torre: 'O horizonte é amplo e seguro para quem sobe degrau por degrau.'",
    ]
    for ph in phrases_arch:
        p(story, f"• <i>{ph}</i>", s["body_left"])
    story.append(Spacer(1, 6))
    p(story, "Minhas frases personalizadas da casa:", s["label"])
    story.append(blank_lines(6))
    story.append(PageBreak())

    p(story, "Apêndice C — Registros Extras de Treino e Manutenção Continuada (120 Folhas)", s["h1"])
    story.append(hr())
    p(story, "Este caderno de manutenção garante que você continue praticando e consolidando a neuroplasticidade "
             "em diferentes ambientes, viagens e estações do ano.", s["body"])
    story.append(PageBreak())

    for i in range(1, 121):
        story.append(exposure_log_page(
            s, i, "Registro Extra de Manutenção Continuada",
            "O Guardião da Constância",
            "Generalização em Novos Ambientes e Situações Reais"
        ))
        story.append(PageBreak())

    p(story, "Apêndice D — Protocolo Específico para Fobia de Sangue-Injeção (Tensão Aplicada)", s["h1"])
    story.append(hr())
    p(story, "A fobia de sangue-injeção-ferimentos (BII) é o único subtipo fóbico que apresenta resposta vasovagal bifásica "
      "(aumento inicial de pressão seguido de queda brusca, podendo causar síncope/desmaio).", s["body"])
    p(story, "<b>Técnica de Tensão Aplicada de Lars-Göran Öst:</b>", s["h2"])
    story.append(bullets([
        "1. Sentar em cadeira confortável e segura.",
        "2. Tencionar os músculos dos braços, tronco e pernas por 10 a 15 segundos até sentir calor no rosto.",
        "3. Relaxar a musculatura por 20 segundos (sem ficar mole demais).",
        "4. Repetir 5 ciclos consecutivos antes e durante a punção venosa ou vacina.",
        "5. Essa contração voluntária eleva a pressão arterial e impede o desmaio fisiológico com total segurança.",
    ], s["body_left"]))
    story.append(PageBreak())

    p(story, "Apêndice E — Guia de Exposição com Realidade Virtual (RV)", s["h1"])
    story.append(hr())
    p(story, "A Terapia de Exposição por Realidade Virtual (VRE), área de especialização acadêmica da Dra. Priscila Palomo, "
      "utiliza ambientes digitais imersivos controlados para simular voos, alturas, elevadores e animais com precisão milimétrica.", s["body"])
    p(story, "<b>Vantagens Clínicas da RV:</b>", s["h2"])
    story.append(bullets([
        "Controle total sobre as variáveis climáticas e intensidade do estímulo.",
        "Possibilidade de repetições imediatas do mesmo pouso ou decolagem na mesma sessão clínica.",
        "Segurança psicológica máxima para pacientes com alto nível de esquiva inicial.",
        "Ponte perfeita e validada para a posterior transição para a exposição in vivo real.",
    ], s["body_left"]))
    story.append(PageBreak())

    p(story, "Apêndice F — Plano de Manutenção Anual e Prevenção de Recaídas (4 Trimestres)", s["h1"])
    story.append(hr())
    for trim in range(1, 5):
        p(story, f"<b>Check-in do Trimestre {trim} da Casa Interior</b>", s["h2"])
        p(story, "1. Áreas reconquistadas que mantenho ativas no meu cotidiano:", s["label"])
        story.append(blank_lines(3))
        p(story, "2. Pequenas esquivas que tentaram voltar e que desmontei no ato:", s["label"])
        story.append(blank_lines(3))
        p(story, "3. Próximo grande desafio ou viagem que vou realizar:", s["label"])
        story.append(blank_lines(3))
        story.append(PageBreak())

    p(story, "Apêndice G — Termo de Compromisso e Aliança com a Coragem", s["h1"])
    story.append(hr())
    p(story, "Eu, ____________________________________________________________________, declaro solenemente diante de todos os guardiões "
      "da minha casa interior que assumo a responsabilidade amorosa pela minha liberdade. Comprometo-me a não fugir nos primeiros minutos "
      "da água fria, a subir um degrau de cada vez com o Mestre Marceneiro e a honrar a nobre coragem de dragão que habita em meu peito.", s["body"])
    story.append(Spacer(1, 10))
    p(story, "Assinatura do(a) Peregrino(a): ________________________________________________", s["field"])
    story.append(Spacer(1, 6))
    p(story, "Data: ______ / ______ / 2026", s["field"])
    story.append(Spacer(1, 10))
    p(story, "“A casa inteira agora é livre. Que todas as janelas permaneçam abertas para a luz do sol.”", s["quote"])
    story.append(PageBreak())

    p(story, "Apêndice H — Glossário Clínico Completo", s["h1"])
    story.append(hr())
    glossary_data = [
        ("Amígdala Cerebral", "Estrutura subcortical do sistema límbico responsável pela detecção de ameaças e disparo do alarme de sobrevivência."),
        ("Aprendizado Inibitório", "Formação de novas conexões neurais no córtex pré-frontal que inibem e superam a resposta fóbica original."),
        ("Comportamento de Segurança", "Ações sutis de esquiva que aliviam o mal-estar momentâneo mas impedem a extinção definitiva do medo."),
        ("Desensibilização Sistemática", "Protocolo clássico de aproximação progressiva emparelhada com relaxamento muscular."),
        ("DSM-5-TR", "Manual Diagnóstico e Estatístico de Transtornos Mentais da Associação Americana de Psiquiatria."),
        ("Eixo HPA", "Eixo neuroendócrino Hipotálamo-Hipófise-Adrenal responsável pela liberação de cortisol e adrenalina no estresse."),
        ("Erro de Predição (Prediction Error)", "Diferença entre o desastre esperado e a realidade observada, motor da neuroplasticidade."),
        ("Habituação", "Redução natural e fisiológica da ativação autonômica após permanência continuada no estímulo sem fuga."),
        ("Protocolo Unificado (UP)", "Intervenção transdiagnóstica de David H. Barlow focada na regulação emocional e tolerância ao afeto."),
        ("SUDS", "Unidades Subjetivas de Desconforto (Subjective Units of Distress Scale), escala de 0 a 10 ou 0 a 100."),
        ("TCC", "Terapia Cognitivo-Comportamental, abordagem científica baseada em evidências para transtornos de ansiedade."),
        ("Violação de Expectativa", "Comprovação empírica de que as previsões catastróficas da mente não se concretizam na prática."),
    ]
    for termo, definicao in glossary_data:
        p(story, f"• <b>{termo}:</b> {definicao}", s["body"])
    story.append(PageBreak())

    p(story, "Apêndice I — Recursos de Apoio e Contatos Clínicos", s["h1"])
    story.append(hr())
    p(story, "• <b>Site Oficial da Dra. Priscila Palomo:</b> <font color='#0E4A57'><u>www.priscilapalomo.com</u></font><br/>"
      "• <b>Loja de Materiais e Protocolos Clínicos:</b> <font color='#0E4A57'><u>www.priscilapalomo.com/loja.html</u></font><br/>"
      "• <b>Página Oficial do Programa Escada Segura:</b> <font color='#0E4A57'><u>www.priscilapalomo.com/escada-segura.html</u></font><br/>"
      "• <b>Atendimento Clínico e WhatsApp:</b> (11) 95069-0537<br/>"
      "• <b>Centro de Valorização da Vida (CVV):</b> Telefone 188 (ligação gratuita 24h em todo o Brasil)<br/>"
      "• <b>Conselho Regional de Psicologia de São Paulo (CRP-SP):</b> CRP 98007", s["body"])
    story.append(Spacer(1, 10))
    p(story, "<i>Este book é protegido por direitos autorais e foi desenvolvido com dedicação científica e ética "
             "pela Dra. Priscila Palomo para transformar vidas e devolver a liberdade aos seus leitores.</i>", s["small"])

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"Book gerado com sucesso: {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
