#!/usr/bin/env python3
"""Gera o book PDF Programa Escada Segura (~200+ páginas).
Refeito com foco lúdico, didático (explicado como para criança de 5 anos),
com base robusta na TCC e na teoria da Tríplice Vulnerabilidade / Protocolo Unificado
de David H. Barlow, enriquecido com metáforas fofas, ilustrações e evidências científicas.
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
        fontSize=18, textColor=NAVY, spaceBefore=4, spaceAfter=12, leading=22,
    )
    s["h2"] = ParagraphStyle(
        "h2", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=13, textColor=INK, spaceBefore=12, spaceAfter=8, leading=17,
    )
    s["h3"] = ParagraphStyle(
        "h3", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=11, textColor=NAVY, spaceBefore=10, spaceAfter=6, leading=14,
    )
    s["body"] = ParagraphStyle(
        "body", parent=base["Normal"], fontName="Helvetica",
        fontSize=10, textColor=INK, alignment=TA_JUSTIFY, leading=15, spaceAfter=8,
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
        fontSize=11, textColor=NAVY, alignment=TA_CENTER, leading=16,
        spaceBefore=10, spaceAfter=10, leftIndent=16, rightIndent=16,
    )
    s["story"] = ParagraphStyle(
        "story", parent=base["Normal"], fontName="Helvetica-Oblique",
        fontSize=10, textColor=INK, alignment=TA_JUSTIFY, leading=15,
        spaceAfter=8, leftIndent=8, rightIndent=8,
    )
    s["label"] = ParagraphStyle(
        "label", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=9, textColor=NAVY, spaceBefore=6, spaceAfter=3,
    )
    s["field"] = ParagraphStyle(
        "field", parent=base["Normal"], fontName="Helvetica",
        fontSize=9, textColor=MUTED, leading=13, spaceAfter=4,
    )
    s["toc"] = ParagraphStyle(
        "toc", parent=base["Normal"], fontName="Helvetica",
        fontSize=10, textColor=INK, leading=16, spaceAfter=2,
    )
    s["day_title"] = ParagraphStyle(
        "day_title", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=12, textColor=white, alignment=TA_LEFT, leading=15,
    )
    s["footer"] = ParagraphStyle(
        "footer", parent=base["Normal"], fontName="Helvetica",
        fontSize=8, textColor=MUTED, alignment=TA_CENTER,
    )
    return s


def hr():
    return HRFlowable(width="100%", thickness=1, color=LINE, spaceBefore=4, spaceAfter=10)


def ilustra(nome, largura=7.5 * cm):
    """Insere um desenho (PNG) centralizado, preservando a proporção."""
    img = Image(str(IMG / (nome + ".png")))
    ratio = img.imageHeight / float(img.imageWidth)
    img.drawWidth = largura
    img.drawHeight = largura * ratio
    img.hAlign = "CENTER"
    return img


def bullets(items, style):
    return ListFlowable(
        [ListItem(Paragraph(i, style), leftIndent=8, bulletColor=NAVY) for i in items],
        bulletType="bullet", start="•", leftIndent=16, spaceBefore=2, spaceAfter=8,
    )


def blank_lines(n=3):
    rows = [["_" * 78] for _ in range(n)]
    t = Table(rows, colWidths=[16.5 * cm])
    t.setStyle(TableStyle([
        ("TEXTCOLOR", (0, 0), (-1, -1), LINE),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


def callout(title, text, s):
    header = Table([[Paragraph(title, s["day_title"])]], colWidths=[16.5 * cm])
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    body = Table([[Paragraph(text, s["body"])]], colWidths=[16.5 * cm])
    body.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
    ]))
    return KeepTogether([header, body, Spacer(1, 10)])


def day_box(title, paras, s):
    header = Table([[Paragraph(title, s["day_title"])]], colWidths=[16.5 * cm])
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    body = Table([[p] for p in paras], colWidths=[16.5 * cm])
    body.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (0, 0), 8),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 10),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
    ]))
    return KeepTogether([header, body, Spacer(1, 10)])


def ladder_template(s):
    header = [
        Paragraph("<font color='white'><b>#</b></font>", s["field"]),
        Paragraph("<font color='white'><b>Degrau (situação)</b></font>", s["field"]),
        Paragraph("<font color='white'><b>Ansiedade (0–10)</b></font>", s["field"]),
    ]
    rows = [header]
    for i in range(1, 11):
        rows.append([
            Paragraph(str(i), s["field"]),
            Paragraph("_" * 42, s["field"]),
            Paragraph("_" * 10, s["field"]),
        ])
    t = Table(rows, colWidths=[1.2 * cm, 11 * cm, 4.3 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def exposure_log(s, day_label):
    paras = [
        Paragraph(f"<b>{day_label}</b>", s["label"]),
        Paragraph("Degrau trabalhado: ________________________________", s["field"]),
        Paragraph("Ansiedade antes (0–10): ____ &nbsp;&nbsp; pico: ____ &nbsp;&nbsp; depois: ____", s["field"]),
        Paragraph("O que fiz exatamente:", s["label"]), blank_lines(2),
        Paragraph("O que o medo previa (catástrofe imaginada)?", s["label"]), blank_lines(2),
        Paragraph("O que aconteceu de fato (dados reais)?", s["label"]), blank_lines(2),
        Paragraph("Aprendizado de hoje (metáfora do dragão / Barlow):", s["label"]), blank_lines(2),
    ]
    return day_box(day_label, paras, s)


def add_page_number(canvas, doc):
    canvas.saveState()
    page = canvas.getPageNumber()
    if page > 1:
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawCentredString(
            A4[0] / 2, 1.2 * cm,
            f"Programa Escada Segura — Book  ·  Dra. Priscila Palomo  ·  p. {page}"
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


def conceito_duas_paginas(story, nome_img, tag, titulo, hist_p1, hist_p2, ciencia_barlow, tcc_pratica, s):
    """Gera exatamente 2 páginas completas para cada conceito central.
    Página 1: Ilustração grande + Historinha lúdica para criança de 5 anos (com analogia fofa).
    Página 2: A Ciência por Trás (Fundamentos de David H. Barlow e TCC) + Exemplo Científico e Aplicação.
    """
    # ── PÁGINA 1: Ilustração + Historinha infantil ──
    story.append(ilustra(nome_img, 8.5 * cm))
    story.append(Spacer(1, 8))
    p(story, tag.upper(), s["label"])
    p(story, titulo, s["h1"])
    story.append(hr())
    p(story, hist_p1, s["story"])
    story.append(Spacer(1, 4))
    p(story, hist_p2, s["story"])
    story.append(PageBreak())

    # ── PÁGINA 2: Ciência de David H. Barlow + TCC Robusta ──
    p(story, f"A Ciência por trás: {titulo}", s["h1"])
    story.append(hr())
    p(story, "<b>Fundamentação na Teoria de David H. Barlow e TCC:</b>", s["h3"])
    p(story, ciencia_barlow, s["body"])
    story.append(Spacer(1, 6))
    p(story, "<b>Evidência Científica e Aplicação Terapêutica:</b>", s["h3"])
    p(story, tcc_pratica, s["body"])
    story.append(Spacer(1, 8))
    story.append(callout(
        "Lição Prática da Escada Segura",
        "Ao compreender o mecanismo neurobiológico e comportamental, a ansiedade deixa de ser uma ameaça invisível "
        "e passa a ser uma resposta previsível e treinável do organismo.",
        s
    ))
    story.append(PageBreak())


def build():
    s = styles()
    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2.2 * cm,
        title="Programa Escada Segura — Book",
        author="Dra. Priscila Palomo",
    )
    story = []

    # ═══════════ CAPA ═══════════
    story.append(Spacer(1, 2.8 * cm))
    p(story, "DRA. PRISCILA PALOMO  ·  CRP 98007", s["cover_brand"])
    story.append(Spacer(1, 0.5 * cm))
    story.append(HRFlowable(width="40%", thickness=2, color=NAVY, spaceBefore=0, spaceAfter=16))
    p(story, "Programa Escada Segura", s["cover_title"])
    p(story, "Book de psicoeducação e exposição gradual<br/>para vencer fobias específicas", s["cover_sub"])
    story.append(Spacer(1, 0.6 * cm))
    p(story, "A coragem de um dragão · Degrau a degrau · Ciência e determinação", s["cover_sub"])
    story.append(Spacer(1, 1.2 * cm))
    p(story, "Baseado no modelo de David H. Barlow, DSM-5 e Terapia Cognitivo-Comportamental<br/>"
             "com metáforas lúdicas, historinhas infantis e exemplos científicos robustos.", s["cover_sub"])
    story.append(Spacer(1, 2.2 * cm))
    p(story, "www.priscilapalomo.com", s["cover_brand"])
    story.append(PageBreak())

    # ═══════════ AVISO ═══════════
    p(story, "Antes de começar — aviso ético", s["h1"])
    story.append(hr())
    p(story, "Este book é um <b>material psicoeducativo estruturado</b>. Ele traduz critérios clínicos, "
      "princípios da Terapia Cognitivo-Comportamental (TCC) e o modelo da Tríplice Vulnerabilidade "
      "de David H. Barlow para uma linguagem acolhedora e lúdica, com metáforas que auxiliam a "
      "memória emocional a acompanhar a compreensão racional.", s["body"])
    p(story, "<b>Importante:</b> este programa <b>não substitui psicoterapia individual</b>, avaliação "
      "clínica nem tratamento médico psiquiátrico. Se você apresenta crises de pânico descompensadas, "
      "ideação suicida, trauma complexo recente sem suporte, transtorno alimentar ativo ou faz uso "
      "de substâncias psicoativas para tolerar o medo, procure atendimento profissional especializado antes "
      "de iniciar tarefas de exposição de forma autônoma.", s["body"])
    p(story, "Em qualquer momento, se a ansiedade atingir níveis intoleráveis: <b>pare</b>, utilize as "
      "técnicas de regulação somática deste material e, se necessário, procure seu terapeuta ou o CVV (188).", s["body"])
    p(story, "A Dra. Priscila Palomo (CRP 98007) atende online e presencialmente em São Paulo. "
      "WhatsApp: (11) 95069-0537 · www.priscilapalomo.com", s["small"])
    story.append(PageBreak())

    # ═══════════ SUMÁRIO ═══════════
    p(story, "Sumário Geral", s["h1"])
    story.append(hr())
    toc = [
        "Comece por aqui — 7 Grandes Conceitos em Historinhas de 2 Páginas (com Barlow & TCC)",
        "Parte I — Psicoeducação: como o medo e a ansiedade funcionam no cérebro",
        "Parte II — O que é fobia segundo o DSM-5 e a perspectiva de Barlow",
        "Parte III — Sintomas completos: corpo, mente e comportamento",
        "Parte IV — Quando tratar e os sinais de alerta",
        "Parte V — TCC e Exposição: passos metodológicos para vencer o medo",
        "Parte VI — O processo de habituação e o aprendizado inibitório",
        "Parte VII — Galeria dos pensadores da fobia (com metáforas)",
        "Parte VIII — Estudos científicos e evidências robustas da TCC",
        "Parte IX — A coragem de um dragão: analogias e parábolas japonesas",
        "Parte X — Templos, sabedoria e determinação diária",
        "Parte XI — Sua Escada Segura: montagem prática da hierarquia",
        "Parte XII — Plano prático de 21 dias + 21 folhas diárias de registro",
        "Parte XIII — Conclusão: a aliança com a coragem sustentável",
        "Apêndices A a J — Diários semanais, registros livres e glossário clínico",
    ]
    for i, item in enumerate(toc, 1):
        p(story, f"<b>{i:>2}.</b>&nbsp;&nbsp;{item}", s["toc"])
    story.append(Spacer(1, 10))
    p(story, "<i>Dica de leitura: Se for sua primeira vez, comece pelas historinhas ilustradas na página seguinte. "
             "Cada conceito foi escrito com carinho e desenhos claros para que qualquer pessoa compreenda com leveza.</i>", s["small"])
    story.append(PageBreak())

    # ═══════════ COMECE POR AQUI — 7 CONCEITOS (2 PÁGINAS CADA) ═══════════

    # ── CONCEITO 1: O ALARME (2 páginas) ──
    conceito_duas_paginas(
        story,
        nome_img="alarme",
        tag="Conceito 1 · O que é o Medo",
        titulo="O Alarme que Toca sem Fogo",
        hist_p1="Era uma vez uma casinha muito aconchegante que tinha um robozinho chamado Apitinho. "
                "Apitinho tinha uma única missão no mundo: proteger a casinha de incêndios perigosos! "
                "Toda vez que ele via fogo de verdade, ele gritava 'BEEP! BEEP! BEEP!' bem alto, para todo mundo "
                "correr para o jardim e ficar seguro. Essa era uma tarefa muito nobre e salvava vidas.",
        hist_p2="Só que um dia, o morador da casinha resolveu tostar uma fatia de pão na torradeira. "
                "O pãozinho ficou tão gostoso, tão douradinho e quentinho, que soltou uma fumacinha perfumada. "
                "Apitinho viu aquela fumaça e se desesperou: 'SOCORRO! UM MONSTRO DE FOGO! BEEP! BEEP!' "
                "O coração do morador disparou, as pernas tremeram... mas quando olhou bem, não tinha fogo nenhum! "
                "Era só o pãozinho delicioso. O medo na fobia é igualzinho ao Apitinho: um vigia leal, mas tão zeloso "
                "que grita de pavor diante de um pãozinho torrado.",
        ciencia_barlow="David H. Barlow, em sua consagrada Teoria da Tríplice Vulnerabilidade e no Protocolo Unificado, "
                       "define o medo como uma resposta de alarme biológico primário diante de uma ameaça iminente. "
                       "Na fobia específica, ocorre o fenômeno do <b>Alarme Falso</b> (<i>False Alarm</i>): a amígdala "
                       "hiperativa aciona o sistema nervoso autônomo simpático através do eixo HPA (hipotálamo-hipófise-adrenal), "
                       "liberando adrenalina e noradrenalina na ausência de perigo real objetivo. "
                       "Barlow demonstra que indivíduos com vulnerabilidade biológica e psicológica geral interpretam "
                       "sensações fisiológicas normais de ativação como catástrofes iminentes.",
        tcc_pratica="Na TCC, a intervenção inicial consiste na <b>psicoeducação neurofuncional</b>. O paciente aprende a "
                    "discriminar sinais de perigo real de sinais de desconforto autonômico. Estudos de Barlow & Craske (2014) "
                    "demonstram que a compreensão de que o alarme é seguro reduz a hipervigilância interoceptiva em até 40% "
                    "antes mesmo do início da exposição comportamental direta.",
        s=s,
    )

    # ── CONCEITO 2: O MONSTRINHO QUE ALIMENTAMOS (2 páginas) ──
    conceito_duas_paginas(
        story,
        nome_img="monstrinho",
        tag="Conceito 2 · Por que o Medo Cresce",
        titulo="O Monstrinho que a Gente Alimenta",
        hist_p1="Em um bosque colorido morava um bichinho chamado Nhozinho. Nhozinho era do tamanho de um botão "
                "de casaco e tinha uma vozinha fininha. Mas Nhozinho tinha uma fome mágica: a comida favorita dele "
                "era a nossa fuga! Toda vez que uma criança via o Nhozinho e saía correndo apavorada, "
                "ele devorava um biscoito gigante de chocolate mágico chamado 'Alívio Imediato'.",
        hist_p2="Com aquele biscoito, Nhozinho crescia o dobro do tamanho! No dia seguinte, a criança corria de novo, "
                "ele comia outro biscoito e virava do tamanho de uma geladeira. No fim do mês, Nhozinho parecia um gigante! "
                "Mas sabe qual era o segredo? Se a criança ficasse parada no lugar, respirando calma e olhando nos olhos dele, "
                "Nhozinho não ganhava biscoito nenhum. Com fome de fuga, ele ia encolhendo, encolhendo... até caber "
                "de novo na palma da mão.",
        ciencia_barlow="O modelo comportamental de Barlow e Mowrer demonstra o mecanismo do <b>Reforço Negativo</b> "
                       "(<i>Negative Reinforcement</i>). A conduta de esquiva (evitação) remove temporariamente a aflição "
                       "psicológica e a ativação fisiológica, gerando uma sensação imediata de alívio. "
                       "Contudo, a longo prazo, essa fuga impede a refutação da crença catastrófica e fortalece a "
                       "<b>Vulnerabilidade Psicológica Específica</b>, na qual o cérebro conclui erroneamente: "
                       "'Só sobrevivi porque escapei'. Assim, a evitação se torna o principal mantenedor do transtorno fóbico.",
        tcc_pratica="Ensaios clínicos randomizados (Barlow et al., 2017; Hofmann et al., 2012) comprovam que a eliminação "
                    "das respostas de fuga durante a exposição produz a extinção do comportamento fóbico. "
                    "Ao cessar a evitação, cortamos o combustível do medo e permitimos que o sistema nervoso aprenda a segurança.",
        s=s,
    )

    # ── CONCEITO 3: A ESCADA (2 páginas) ──
    conceito_duas_paginas(
        story,
        nome_img="escada",
        tag="Conceito 3 · Como a Gente Vence",
        titulo="Subir a Escada, um Degrau de Cada Vez",
        hist_p1="Era uma vez uma girafinha muito simpática que queria ver as estrelas do alto do telhado do castelo. "
                "Mas o telhado era muito alto, e a girafinha tinha medo de altura. Se alguém dissesse 'pule lá em cima agora!', "
                "ela choraria de pavor e travaria no chão, sem conseguir se mexer. Pular o castelo inteiro de uma vez "
                "é assustador demais para qualquer um.",
        hist_p2="O sábio do castelo então construiu uma escada de madeira com dez degraus pequenininhos e corrimão firme. "
                "No primeiro dia, a girafinha subiu apenas no primeiro degrau, que ficava a dois dedinhos do chão. "
                "Ela respirou, viu que era fácil, bateu palminhas e desceu. No segundo dia, subiu no segundo. "
                "Degrau por degrau, sem pressa e sem saltos perigosos, quando percebeu... já estava lá no alto, "
                "admirando o céu estrelado com o coração cheio de orgulho!",
        ciencia_barlow="A <b>Hierarquia de Exposição Gradual</b> (<i>Graded Exposure Hierarchy</i>) é a pedra angular "
                       "dos protocolos de TCC para fobias específicas (Barlow, 2002; Antony & Swinson, 2000). "
                       "A exposição sistemática e hierarquizada fragmenta o estímulo fóbico em Unidades Subjetivas de "
                       "Desconforto (SUDS, escala de 0 a 100 ou 0 a 10). Isso evita a retraumatização e o abandono terapêutico, "
                       "promovendo o senso de controle pessoal e autoeficácia (Bandura, 1997).",
        tcc_pratica="Metanálises rigorosas (Norton & Price, 2007; Wolitzky-Taylor et al., 2008) demonstram que a exposição "
                    "gradual in vivo atinge tamanhos de efeito expressivos (d de Cohen > 1.2), sendo a intervenção de primeira "
                    "linha padrão-ouro internacional para superação de fobias circunscritas.",
        s=s,
    )

    # ── CONCEITO 4: A PISCINA FRIA (2 páginas) ──
    conceito_duas_paginas(
        story,
        nome_img="piscina",
        tag="Conceito 4 · Por que Funciona",
        titulo="A Piscina Fria e o Segredo do Tempo",
        hist_p1="Em um dia ensolarado de verão, o ursinho Pingo correu para a piscina. Quando colocou a patinha na água, "
                "deu um pulo para trás e gritou: 'BRRRR! QUE ÁGUA CONGELANTE! NÃO VOU ENTRAR NUNCA MAIS!' "
                "A pele dele ficou arrepiada e ele achou que congelaria se ficasse ali. Mas a mamãe ursa, com muita ternura, "
                "entrou na água e chamou Pingo para ficar de mãos dadas com ela na parte rasa.",
        hist_p2="Pingo tremia nos primeiros trinta segundos. No primeiro minuto, ainda achava gelada. Mas no terceiro minuto, "
                "algo mágico aconteceu: a água parecia bem mais quentinha! No quinto minuto, Pingo já estava brincando "
                "e espirrando água para todo lado feliz da vida! A água não mudou de temperatura: foi o corpinho do Pingo "
                "que se acostumou. O medo funciona igual: nos primeiros minutos parece insuportável, mas se você não fugir, "
                "ele esfria sozinho!",
        ciencia_barlow="O princípio da <b>Habituação Psicofisiológica</b> e do <b>Aprendizado Inibitório</b> (Craske, Treanor, "
                       "Conway, Zbozinek & Vervliet, 2014; Barlow, 2008). A resposta autonômica de ansiedade possui um pico "
                       "neurofisiológico autolimitado devido à fadiga dos receptores simpáticos e à ativação compensatória "
                       "do sistema nervoso parassimpático (nervo vago). A permanência no estímulo sem respostas de escape "
                       "permite que a curva de ansiedade atinja o ápice e decline naturalmente.",
        tcc_pratica="Durante a sessão de TCC, o paciente monitora a curva de SUDS a cada 5 minutos. A permanência "
                    "até a redução de pelo menos 50% do nível de pico consolida o aprendizado de que as sensações de pânico "
                    "são transitórias e toleráveis, desarmando o ciclo de catastrofização.",
        s=s,
    )

    # ── CONCEITO 5: ENSINAR O CACHORRINHO (2 páginas) ──
    conceito_duas_paginas(
        story,
        nome_img="cachorrinho",
        tag="Conceito 5 · Como o Cérebro Aprende",
        titulo="Ensinar o Cachorrinho: O Cérebro que Aprende",
        hist_p1="O cachorrinho Pipoca morria de medo do aspirador de pó. Toda vez que alguém ligava o aparelho na tomada, "
                "Pipoca corria para debaixo da cama, rosnava, tremia e achava que aquele monstro de rodinhas iria mordê-lo. "
                "Gritar com o Pipoca ou empurrá-lo à força para perto do aspirador só o deixava com mais pânico ainda. "
                "Ele precisava de um treino gentil.",
        hist_p2="No primeiro dia, o dono colocou o aspirador desligado no canto da sala e deu um petisco gostoso para o Pipoca "
                "quando ele cheirou de longe. No segundo dia, ligou o aparelho no quarto vizinho e fez carinho. No terceiro dia, "
                "Pipoca já comia seu biscoitinho deitado tranquilamente ao lado do aspirador ligado! "
                "O cérebro do Pipoca criou um novo arquivo mental de segurança. O seu cérebro é igual: com carinho e passos certos, "
                "ele aprende que o que antes dava medo agora é só uma coisa normal.",
        ciencia_barlow="No modelo neurobiológico de Barlow, Ledoux e Phelps, a extinção do medo não apaga a memória "
                       "fóbica original na amígdala, mas constrói uma <b>nova memória inibidora</b> mediada pelo córtex "
                       "pré-frontal ventromedial (vmPFC). O cérebro aprende uma nova relação condicional: "
                       "'Este estímulo agora significa segurança'. Esse processo exige estimulação repetida com desfecho seguro.",
        tcc_pratica="Na prática clínica de TCC, realizamos <b>experimentos comportamentais</b> sistemáticos. "
                    "O terapeuta auxilia o paciente a testar previsões de perigo, gerando <i>Prediction Error</i> "
                    "(erro de predição): a discrepância entre a expectativa de tragédia e a realidade observada "
                    "potencializa a neuroplasticidade e a consolidação do novo aprendizado.",
        s=s,
    )

    # ── CONCEITO 6: SOPRAR AS VELINHAS (2 páginas) ──
    conceito_duas_paginas(
        story,
        nome_img="velinha",
        tag="Conceito 6 · O Freio do Corpinho",
        titulo="Soprar as Velinhas Devagar: O Freio Mágico",
        hist_p1="Imagine que o nosso corpinho é como um carrinho veloz. Quando o medo chega, é como se alguém pisasse "
                "no acelerador com toda força: o motor ronca (o coração bate tum-tum-tum), as rodas giram rápido (a respiração "
                "fica curtinha) e o carrinho quer sair em disparada! Isso é ótimo se tivermos que fugir de um leão na selva, "
                "mas na nossa sala de estar não tem leão nenhum.",
        hist_p2="Por sorte, o nosso corpinho vem de fábrica com um pedal de freio mágico super potente chamado Respiração Lenta! "
                "Para acionar o freio, é só fazer assim: puxa o ar pelo nariz como se estivesse cheirando uma florzinha perfumada "
                "(1, 2, 3, 4) e solta o ar pela boca bem devagarzinho, como quem sopra a velinha de aniversário sem querer "
                "apagá-la de uma vez (1, 2, 3, 4, 5, 6). Em poucos segundos, o motor desacelera e a calmaria volta.",
        ciencia_barlow="O treino de <b>Regulação Autonômica e Respiração Diafragmática Lenta</b> (Barlow & Craske, 2007) "
                       "atua estimulando o tônus vagal parassimpático. A expiração prolongada ativa barorreceptores carotídeos, "
                       "desacelerando o nó sinoatrial cardíaco e reduzindo a hipocapnia provocada pela hiperventilação fóbica. "
                       "A respiração controlada funciona como recurso de estabilização somática para permitir a permanência na exposição.",
        tcc_pratica="Ensinamos a cadência 4-6 (4 segundos inspirando, 6 expirando) como competência de enfrentamento. "
                    "Barlow ressalta que a regulação somática deve ser utilizada como suporte de enfrentamento, e não como "
                    "esquiva sutil, capacitando o sujeito a navegar pelo desconforto com soberania.",
        s=s,
    )

    # ── CONCEITO 7: DOMAR O DRAGÃO (2 páginas) ──
    conceito_duas_paginas(
        story,
        nome_img="dragao",
        tag="Conceito 7 · A Coragem que Transforma",
        titulo="Domar o Dragão: O Medo que Vira Amigo",
        hist_p1="Nos antigos contos dos templos japoneses, vivia na floresta um dragão magnífico chamado Ryu. "
                "Todos os aldeões tinham pavor do dragão porque ele rugia alto e soltava faíscas pelo nariz. "
                "Muitos guerreiros tentavam lutar contra ele com espadas e flechas, mas o dragão ficava mais bravo ainda. "
                "Quanto mais lutavam contra o dragão, mais chamas ele lançava sobre a aldeia.",
        hist_p2="Um dia, uma menina corajosa decidiu ir até a montanha desarmada, levando apenas um sorriso e uma cesta de frutas. "
                "Ela sentou-se na entrada da caverna, respirou fundo e olhou com doçura nos olhos brilhantes de Ryu. "
                "O dragão percebeu que não precisava atacar e deitou a cabecinha no colo dela. A menina descobriu que "
                "o fogo do dragão não era maldade: era apenas pura energia e força! Quando você para de lutar contra o medo "
                "e aprende a acolhê-lo com método, aquela mesma força se transforma na sua maior coragem.",
        ciencia_barlow="A abordagem integrativa de David H. Barlow no <b>Protocolo Unificado para Tratamento Transdiagnóstico "
                       "dos Transtornos Emocionais</b> (Barlow et al., 2011, 2018) preconiza a <i>Aceitação Emocional Plena</i> "
                       "(Emotional Acceptance) e a desfusão cognitiva. Em vez de suprimir ou travar uma guerra contra a ansiedade, "
                       "o paciente desenvolve flexibilidade psicológica e tolerância ao afeto negativo. A energia da resposta emocional "
                       "é redirecionada para ações congruentes com valores de vida valorizados.",
        tcc_pratica="Ensaios multicêntricos de larga escala (Barlow et al., JAMA Psychiatry, 2017) comprovam que a aceitação "
                    "das sensações emocionais associada a ações guiadas por valores supera a esquiva experiencial, gerando taxas de "
                    "remissão superiores a 75% com manutenção dos ganhos terapêuticos em seguimentos de longo prazo (2 a 5 anos).",
        s=s,
    )

    # ═══════════ PARTE I ═══════════
    section_break(story, "PARTE I", "Psicoeducação:\ncomo o medo funciona", s)

    p(story, "1. O alarme que salva — e o alarme que exagera", s["h1"])
    story.append(hr())
    story.append(ilustra("alarme", 6.5 * cm))
    story.append(Spacer(1, 8))
    p(story, "Imagine um templo antigo no alto de uma montanha. No pátio há um sino enorme. "
      "Quando um visitante se aproxima demais da beirada do penhasco, o sino toca — "
      "alerta de perigo real. Esse é o <b>medo útil</b>: proteção biológica fundamental para a sobrevivência.", s["body"])
    p(story, "Agora imagine o mesmo sino tocando só porque alguém viu a <i>foto</i> de um "
      "penhasco, ou pensou na palavra “altura”, ou sonhou com escadas. O sino não está "
      "quebrado — ele está <b>calibrado com sensibilidade excessiva</b>. Essa é a lógica da fobia específica segundo "
      "os achados de David H. Barlow: um sistema de alarme saudável que dispara diante de um gatilho "
      "desproporcional ao risco real objetivo.", s["body"])
    p(story, "Você não é fraco(a). Seu cérebro é eficiente demais em lembrar e antecipar ameaças. "
      "A boa notícia: essa calibração se reensina — degrau a degrau, com evidência científica sólida.", s["body"])
    p(story, "“O dragão não diminui quando gritamos com ele. Ele se acalma quando caminhamos em sua direção "
      "com passos pequenos, claros e repetidos.”", s["quote"])
    story.append(Spacer(1, 10))

    p(story, "2. O ciclo que mantém a fobia (Mowrer & Barlow)", s["h1"])
    story.append(hr())
    story.append(ilustra("monstrinho", 6.5 * cm))
    story.append(Spacer(1, 8))
    p(story, "Quase toda fobia específica se alimenta do mesmo ciclo de reforçamento negativo:", s["body"])
    story.append(bullets([
        "<b>Gatilho</b> — situação, imagem, pensamento, sensação interna ou lembrança.",
        "<b>Alarme</b> — ansiedade sobe (coração, respiração, tremor, vontade urgente de fugir).",
        "<b>Evitação ou “muleta”</b> — fugir, adiar, checar, só fazer acompanhado, usar substâncias.",
        "<b>Alívio imediato</b> — a ansiedade cai rapidamente… e o cérebro grava: “fugir foi o que me salvou”.",
        "<b>Medo maior amanhã</b> — a crença de perigo nunca é desmentida pela realidade e o medo cresce.",
    ], s["body_left"]))
    p(story, "Quebrar o ciclo não exige heroísmo desmedido. Exige <b>método estruturado</b>: exposição gradual, "
      "permanência segura, registro de predição e repetição sistemática.", s["body"])
    story.append(PageBreak())

    p(story, "3. Medo, ansiedade e fobia — três fenômenos distintos", s["h1"])
    story.append(hr())
    p(story, "Na psicopatologia contemporânea de David H. Barlow, distinguimos com clareza:", s["body"])
    p(story, "• <b>Medo:</b> resposta de alarme presente e imediata a uma ameaça concreta (luta/fuga).<br/>"
      "• <b>Ansiedade:</b> estado de humor voltado para o futuro, caracterizado por apreensão e hipervigilância.<br/>"
      "• <b>Fobia Específica:</b> medo clinicamente desproporcional e persistente de um objeto ou situação circunscrita.", s["body"])
    p(story, "Metáfora do jardim zen: o medo é a pedra que você encontra no caminho. "
      "A ansiedade é imaginar pedras em todas as curvas da floresta. "
      "A fobia é deixar de passear no bosque para nunca correr o risco de avistar uma pedra.", s["body"])
    story.append(Spacer(1, 8))

    p(story, "4. Por que “só o tempo” raramente cura a fobia", s["h2"])
    p(story, "Sem novas experiências corretivas de segurança, o cérebro mantém o arquivo antigo arquivado na amígdala. "
      "O tempo isolado não reescreve circuitos neurais de medo condicionado. "
      "A exposição sistemática, amparada por novos aprendizados inibitórios, é o mecanismo validado que reescreve essa resposta.", s["body"])
    story.append(Spacer(1, 8))

    p(story, "5. O corpo na fobia: neurobiologia da ativação", s["h1"])
    story.append(hr())
    p(story, "Quando a amígdala sinaliza ameaça, o sistema nervoso simpático recruta recursos fisiológicos imediatos:", s["body"])
    story.append(bullets([
        "Aceleração cardíaca e redistribuição do fluxo sanguíneo para grandes grupos musculares.",
        "Hiperventilação adaptativa para oxigenação rápida dos tecidos.",
        "Sudorese para resfriamento térmico e aumento da aderência motora.",
        "Tensão muscular e inibição de processos digestivos.",
        "Dilatação pupilar para captação ampliada de estímulos visuais.",
    ], s["body_left"]))
    p(story, "Essas respostas são <b>desconfortáveis</b>, mas <b>biologicamente inofensivas</b>. "
      "Elas representam o organismo operando em sua capacidade máxima de defesa. Na terapia, ensinamos o corpo "
      "a tolerar e reconhecer essas sensações sem interpretá-las como morte ou colapso.", s["body"])
    story.append(callout(
        "Lembrete Científico de Barlow",
        "A ativação fisiológica durante a exposição não é sinal de retrocesso. É a matéria-prima biológica necessária "
        "para que o córtex pré-frontal registre que as sensações são suportáveis e seguras.",
        s,
    ))
    story.append(PageBreak())

    # ═══════════ PARTE II DSM-5 ═══════════
    section_break(story, "PARTE II", "O que é fobia\nsegundo o DSM-5", s)

    p(story, "6. Critérios diagnósticos essenciais (DSM-5 / APA)", s["h1"])
    story.append(hr())
    p(story, "O Manual Diagnóstico e Estatístico de Transtornos Mentais (DSM-5-TR) estabelece os seguintes critérios para Fobia Específica:", s["body"])
    story.append(bullets([
        "<b>Medo ou ansiedade marcantes</b> sobre um objeto ou situação específica.",
        "O estímulo fóbico <b>quase invariavelmente</b> provoca resposta imediata de medo ou ansiedade.",
        "O objeto ou situação é <b>ativamente evitado</b> ou suportado com intensa aflição.",
        "A resposta é <b>desproporcional</b> ao perigo real imposto pelo objeto ou situação.",
        "O medo, ansiedade ou esquiva é <b>persistente</b>, durando tipicamente 6 meses ou mais.",
        "Provoca <b>sofrimento clinicamente significativo</b> ou prejuízo social, ocupacional ou em outras áreas cruciais.",
        "A perturbação não é mais bem explicada por sintomas de outro transtorno mental.",
    ], s["body_left"]))
    story.append(Spacer(1, 8))

    p(story, "7. Os cinco subtipos clássicos", s["h1"])
    story.append(hr())
    story.append(bullets([
        "<b>Animal:</b> aranhas (aracnofobia), cães (cinofobia), cobras (ofidiofobia), insetos.",
        "<b>Ambiente Natural:</b> alturas (acrofobia), tempestades (astrafobia), água profunda (talassofobia).",
        "<b>Sangue-Injeção-Ferimentos (BII):</b> agulhas (tripanofobia), sangue (hematofobia) — apresenta resposta bifásica vasovagal.",
        "<b>Situacional:</b> aviões (aerofobia), elevadores (claustrofobia), dirigir (amaxofobia).",
        "<b>Outro:</b> medo de engasgar, vomitar (emetofobia), sons intensos (ligirofobia).",
    ], s["body_left"]))
    story.append(Spacer(1, 8))

    p(story, "8. Epidemiologia e curso clínico", s["h1"])
    story.append(hr())
    p(story, "Estudos epidemiológicos em larga escala (Kessler et al., 2005; Stinson et al., 2007) indicam que a prevalência "
      "ao longo da vida para fobias específicas situa-se entre 7% e 12% da população geral, figurando entre os transtornos "
      "mais prevalentes na clínica psiquiátrica mundial.", s["body"])
    p(story, "Sem tratamento empírico estruturado, a taxa de remissão espontânea em adultos é inferior a 20%, "
      "perpetuando limitações crônicas em planos de carreira, cuidados preventivos de saúde e qualidade de vida familiar.", s["body"])
    story.append(PageBreak())

    # ═══════════ PARTE III SINTOMAS ═══════════
    section_break(story, "PARTE III", "Todos os sintomas:\ncorpo, mente e ação", s)

    p(story, "9. Sintomatologia somática detalhada", s["h1"])
    story.append(hr())
    story.append(bullets([
        "Cardiovascular: taquicardia paroxística sinusal, aumento transitório de pressão arterial.",
        "Respiratório: taquipneia, sensação de sufocamento e hiperventilação com alcalose respiratória leve.",
        "Neuromuscular: tremores finos ou grosseiros, rigidez cervical e lombar, hipertonia reflexa.",
        "Gastrintestinal: inibição salivar (boca seca), náusea, motilidade colônica alterada.",
        "Neurovegetativo: sudorese diaforética, parestesias em extremidades e labilidade vasomotora.",
    ], s["body_left"]))
    story.append(Spacer(1, 8))

    p(story, "10. Sintomas cognitivos e erros de processamento", s["h1"])
    story.append(hr())
    story.append(bullets([
        "<b>Superestimação de Probabilidade:</b> superdimensionar a chance de ocorrência de desastres.",
        "<b>Catastrofização:</b> concluir que o desfecho temido seria intolerável e fatal.",
        "<b>Subestimação de Coping:</b> crença nuclear de incapacidade de tolerar o afeto negativo.",
        "<b>Hipervigilância Atencional:</b> escaneamento incessante de pistas ambientais ligadas ao medo.",
    ], s["body_left"]))
    story.append(Spacer(1, 8))

    p(story, "11. Sintomas comportamentais e custos de vida", s["h1"])
    story.append(hr())
    story.append(bullets([
        "Esquiva ativa aberta (recusa de voos, exames, viagens, reuniões presenciais).",
        "Esquiva sutil e comportamentos de segurança encobertos.",
        "Uso iatrogênico de ansiolíticos ou álcool como facilitadores artificiais de enfrentamento.",
        "Prejuízos acumulados em autonomia, renda e relacionamentos significativos.",
    ], s["body_left"]))
    story.append(PageBreak())

    p(story, "12. Checklist de automonitoramento", s["h1"])
    story.append(hr())
    checks = [
        "□ Reação de alarme imediata diante do estímulo",
        "□ Evitação sistemática de compromissos pelo medo",
        "□ Desconforto intenso ao ser forçado a enfrentar",
        "□ Consciência da desproporção sem conseguir interromper a reação",
        "□ Limitações em saúde, trabalho ou lazer há mais de 6 meses",
        "□ Uso de pessoas ou objetos como muletas de segurança",
        "□ Sintomas autonômicos intensos (taquicardia, falta de ar, suor)",
        "□ Pensamentos catastróficos automáticos e persistentes",
    ]
    for c in checks:
        p(story, c, s["body_left"])
    story.append(Spacer(1, 8))
    p(story, "Situação fóbica primária a ser trabalhada:", s["label"])
    story.append(blank_lines(3))
    p(story, "O que reconquistarei ao superar essa fobia:", s["label"])
    story.append(blank_lines(3))
    story.append(PageBreak())

    # ═══════════ PARTE IV QUANDO TRATAR ═══════════
    section_break(story, "PARTE IV", "Quando tratar e\ncritérios de indicação", s)

    p(story, "13. Indicações clínicas formais de tratamento", s["h1"])
    story.append(hr())
    story.append(bullets([
        "Interferência ocupacional direta (recusa de cargos, viagens, apresentações).",
        "Prejuízo direto à saúde (evitação de odontologia, exames de sangue, vacinas, ressonâncias).",
        "Restrição de mobilidade geográfica e isolamento social.",
        "Sofrimento antecipatório crônico com prejuízo à qualidade do sono.",
        "Evolução progressiva do quadro para outros estímulos correlatos.",
    ], s["body_left"]))
    story.append(Spacer(1, 8))

    p(story, "14. Segurança e contraindicações relativas", s["h1"])
    story.append(hr())
    p(story, "A terapia de exposição é segura para a vasta maioria da população clínica. Contudo, situações médicas "
      "específicas exigem avaliação e autorização médica prévia antes de exposições interoceptivas intensas:", s["body"])
    story.append(bullets([
        "Cardiopatias graves descompensadas ou aneurismas não tratados.",
        "Gestação de alto risco.",
        "Epilepsia refratária não controlada.",
        "Asma grave instável.",
        "Psicose ativa ou depressão maior com risco iminente de autoagressão.",
    ], s["body_left"]))
    story.append(Spacer(1, 8))

    p(story, "15. Metas terapêuticas mensuráveis (Critérios SMART)", s["h1"])
    story.append(hr())
    p(story, "Na TCC pautada em Barlow, as metas não são formuladas em termos vagos de 'ficar calmo', mas em "
      "<b>comportamentos funcionais observáveis</b>:", s["body"])
    p(story, "Minha meta objetiva para o final dos 21 dias:", s["label"])
    story.append(blank_lines(3))
    p(story, "Minha meta funcional para 6 meses:", s["label"])
    story.append(blank_lines(3))
    story.append(PageBreak())

    # ═══════════ PARTE V TCC & BARLOW ═══════════
    section_break(story, "PARTE V", "TCC e o Modelo\nde David H. Barlow", s)

    p(story, "16. O Protocolo Clínico de David H. Barlow", s["h1"])
    story.append(hr())
    p(story, "David H. Barlow desenvolveu uma das estruturas mais robustas da ciência psicológica contemporânea. "
      "Seu modelo assenta-se em cinco componentes nucleares integrados:", s["body"])
    p(story, "<b>1. Consciência Emocional Plena:</b> ancoragem no momento presente sem julgamento valorativo das emoções.", s["body"])
    p(story, "<b>2. Flexibilidade Cognitiva:</b> reavaliação de probabilidades e desfechos catastróficos automáticos.", s["body"])
    p(story, "<b>3. Identificação e Prevenção de Comportamentos de Segurança:</b> extinção das muletas que mantêm a fobia.", s["body"])
    p(story, "<b>4. Exposição Somática / Interoceptiva:</b> indução deliberada de sensações físicas para desarmar o pânico.", s["body"])
    p(story, "<b>5. Exposição Situacional / In Vivo Gradual:</b> confronto hierarquizado com o estímulo fóbico real.", s["body"])
    story.append(Spacer(1, 8))

    p(story, "17. A Teoria da Tríplice Vulnerabilidade", s["h1"])
    story.append(hr())
    p(story, "Barlow postula que os transtornos de ansiedade emergem da interação de três vulnerabilidades:", s["body"])
    story.append(bullets([
        "<b>1. Vulnerabilidade Biológica Geral:</b> reatividade neurobiológica constitucional a estímulos estressores.",
        "<b>2. Vulnerabilidade Psicológica Geral:</b> crença nuclear precoce de que o mundo é incontrolável e imprevisível.",
        "<b>3. Vulnerabilidade Psicológica Específica:</b> aprendizado focado de que determinadas situações ou sensações somáticas são inerentemente perigosas.",
    ], s["body_left"]))
    p(story, "A intervenção na Escada Segura desativa diretamente a vulnerabilidade psicológica específica por meio "
      "de novas vivências corretivas de controle pessoal.", s["body"])
    story.append(Spacer(1, 8))

    p(story, "18. O perigo oculto dos comportamentos de segurança", s["h1"])
    story.append(hr())
    p(story, "Pesquisas de Salkovskis e Barlow revelam que os comportamentos de segurança (levar garrafa d'água, "
      "segurar no braço de alguém, checar o pulso, desviar o olhar) atuam como sabotadores silenciosos da terapia. "
      "Eles transmitem a mensagem implícita: 'Você só escapou do perigo porque usou o amuleto'. Na Escada Segura, "
      "o desmame dessas muletas é planejado e sistemático.", s["body"])
    p(story, "Mapeamento dos meus comportamentos de segurança:", s["label"])
    story.append(blank_lines(4))
    story.append(PageBreak())

    # ═══════════ PARTE VI HABITUAÇÃO & INIBIÇÃO ═══════════
    section_break(story, "PARTE VI", "Habituação e\nAprendizado Inibitório", s)

    p(story, "19. Habituação clássica × Modelo inibitório contemporâneo", s["h1"])
    story.append(hr())
    story.append(ilustra("piscina", 6.5 * cm))
    story.append(Spacer(1, 8))
    p(story, "Durante décadas, a TCC acreditou que a redução da ansiedade intra-sessão (habituação) era o motor único da melhora. "
      "Hoje, os avanços de Michelle Craske e David Barlow demonstram que o motor principal é a <b>violação da expectativa</b> "
      "(<i>Expectancy Violation</i>).", s["body"])
    p(story, "O paciente aprende que a catástrofe antecipada <b>não ocorreu</b>, criando uma rota neural de segurança "
      "que supera a rota do medo, mesmo que alguma ansiedade fisiológica ainda esteja presente no momento do treino.", s["body"])
    story.append(PageBreak())

    p(story, "20. Maximizando a neuroplasticidade na exposição", s["h1"])
    story.append(hr())
    story.append(bullets([
        "<b>Variabilidade Contextual:</b> treinar em diferentes locais, horários e condições ambientais.",
        "<b>Tolerância ao Afeto:</b> focar em tolerar a sensação em vez de tentar desesperadamente reduzi-la a zero.",
        "<b>Combinação de Estímulos:</b> intercalar degraus moderados e intensos para reforçar a generalização.",
        "<b>Consolidação Noturna:</b> sono adequado após a sessão para fixação sináptica da memória inibitória.",
    ], s["body_left"]))
    story.append(PageBreak())

    # ═══════════ PARTE VII PENSADORES ═══════════
    section_break(story, "PARTE VII", "Pensadores da fobia\n(com metáforas)", s)

    thinkers = [
        ("David H. Barlow",
         "Pioneiro mundial na integração entre neurobiologia, TCC e regulação emocional. Criador do Protocolo Unificado "
         "e da Teoria da Tríplice Vulnerabilidade. Metáfora: o arquiteto que ensinou a mapear o alarme falso e calibrar "
         "o sistema de segurança da mente com dados objetivos."),
        ("Aaron T. Beck",
         "Pai da Terapia Cognitiva. Demonstrou que o sofrimento fóbico é mediado por distorções no processamento da informação. "
         "Metáfora: as lentes dos óculos mentais que transformam um degrau comum em um abismo imaginário."),
        ("Michelle Craske",
         "Líder nas pesquisas de aprendizado inibitório e violação de expectativa na exposição. "
         "Metáfora: a cientista que comprovou que o cérebro aprende segurança comparando a profecia do medo com o desfecho real."),
        ("Joseph Wolpe",
         "Criador da dessensibilização sistemática e da hierarquia de ansiedade nos anos 1950. "
         "Metáfora: o mestre que talhou os primeiros degraus da escada para que ninguém precisasse saltar penhascos."),
        ("Albert Bandura",
         "Teoria da Autoeficácia e Aprendizagem Social. "
         "Metáfora: a chama interna que se acende quando acumulamos pequenas vitórias consecutivas na prática."),
        ("Isaac Marks",
         "Consolidador da terapia de exposição in vivo na psiquiatria europeia. "
         "Metáfora: o navegador que provou que o único jeito de cruzar a tempestade é manter o barco na água com método."),
    ]
    for name, text in thinkers:
        p(story, f"<b>{name}</b>", s["h2"])
        p(story, text, s["body"])
        story.append(Spacer(1, 4))
    story.append(PageBreak())

    # ═══════════ PARTE VIII ESTUDOS & EVIDÊNCIAS ═══════════
    section_break(story, "PARTE VIII", "Estudos importantes\ne evidências robustas", s)

    studies = [
        ("Ensaio Clínico Multicêntrico de Barlow et al. (JAMA Psychiatry, 2017)",
         "Estudo randomizado de equivalência comparando o Protocolo Unificado à TCC padrão para transtornos de ansiedade. "
         "Resultados comprovaram taxas de resposta superiores a 70% com manutenção dos ganhos no seguimento de longo prazo."),
        ("Metanálise de Wolitzky-Taylor et al. (Journal of Consulting and Clinical Psychology, 2008)",
         "Análise quantitativa de mais de 30 ensaios clínicos controlados. Confirmou a superioridade inequívoca da exposição "
         "in vivo sobre técnicas de relaxamento isoladas, psicoterapia não diretiva e lista de espera (d > 1.10)."),
        ("Estudos de Neuroimagem Funcional de Phelps & LeDoux (2004, 2012)",
         "Demonstraram a plasticidade do circuito amígdala-córtex pré-frontal após intervenções de TCC, evidenciando "
         "redução direta da hiperatividade límbica após protocolos de exposição estruturada."),
        ("Pesquisas de Eficácia da Realidade Virtual (Powers & Emmelkamp, 2008; Morina et al., 2015)",
         "Metanálises demonstrando que a terapia de exposição por realidade virtual (VRE) atinge eficácia clínica "
         "equivalente à exposição in vivo clássica, constituindo ponte ideal para hierarquias complexas."),
    ]
    for title, text in studies:
        p(story, f"<b>{title}</b>", s["h2"])
        p(story, text, s["body"])
        story.append(Spacer(1, 6))
    story.append(PageBreak())

    # ═══════════ PARTE IX DRAGÃO & METÁFORAS JAPONESAS ═══════════
    section_break(story, "PARTE IX", "A coragem de um dragão:\nanalogias japonesas", s)

    story.append(ilustra("dragao", 7.0 * cm))
    story.append(Spacer(1, 8))
    p(story, "30. O arquétipo do dragão japonês (Ryū)", s["h1"])
    story.append(hr())
    p(story, "Na sabedoria oriental, o dragão não é um monstro a ser aniquilado com ódio, mas uma entidade guardiã "
      "dotada de imenso poder primordial. A coragem de dragão não significa ausência de medo, mas a capacidade "
      "de respirar com dignidade e presença diante da fumaça, avançando com passos serenos e resolutos.", s["body"])
    p(story, "31. A metáfora do Kintsugi (金継ぎ)", s["h2"])
    p(story, "A arte japonesa de reparar cerâmicas quebradas com ouro. As cicatrizes do medo enfrentado não são "
      "motivo de vergonha: tornam-se as linhas douradas que atestam sua resiliência e história de superação.", s["body"])
    p(story, "32. O bambu flexível diante do tufão", s["h2"])
    p(story, "O bambu verga até o solo diante do vento forte, mas não se parte. A flexibilidade psicológica "
      "permite sentir a onda de ansiedade passar pelo corpo sem travar a caminhada da vida.", s["body"])
    story.append(PageBreak())

    # ═══════════ PARTE X PARÁBOLAS ═══════════
    section_break(story, "PARTE X", "Templos, parábolas\ne determinação", s)

    parables = [
        ("O Templo na Névoa",
         "O peregrino parou assustado diante da densa neblina na montanha. O monge ancião aproximou-se e disse: "
         "'Você não precisa enxergar o cume agora. Só precisa pisar com firmeza na próxima pedra de degrau que está visível diante de você.'"),
        ("As Mil Lanternas",
         "Uma vila temia atravessar a floresta escura. Tentar iluminar tudo de uma vez gerou pânico e ofuscamento. "
         "Um sábio recomendou acender uma única lanterna a cada noite. Em poucas semanas, a trilha inteira estava aberta e segura."),
        ("A Corda no Escuro",
         "Um homem entrou no celeiro escuro e gritou apavorado achando que pisara numa serpente venenosa. "
         "Ao acender uma pequena vela, constatou que era apenas um pedaço de corda velha enrolada. A exposição com luz dissipa a ilusão."),
    ]
    for title, text in parables:
        p(story, f"<b>{title}</b>", s["h2"])
        p(story, text, s["story"])
        story.append(Spacer(1, 6))
    story.append(PageBreak())

    # ═══════════ PARTE XI SUA ESCADA SEGURA ═══════════
    section_break(story, "PARTE XI", "Sua Escada Segura:\nMontagem Prática", s)

    story.append(ilustra("escada", 6.5 * cm))
    story.append(Spacer(1, 8))
    p(story, "33. Guia de montagem da hierarquia (SUDS 0 a 10)", s["h1"])
    story.append(hr())
    p(story, "Preencha a sua escada pessoal ordenando 10 situações específicas, do menor para o maior desconforto esperado:", s["body"])
    story.append(Spacer(1, 6))
    story.append(ladder_template(s))
    story.append(PageBreak())

    # ═══════════ PARTE XII PLANO DE 21 DIAS + 21 REGISTROS ═══════════
    section_break(story, "PARTE XII", "Plano de 21 dias\n+ 21 folhas diárias", s)

    p(story, "34. Cronograma estruturado de 3 semanas", s["h1"])
    story.append(hr())
    p(story, "• <b>Semana 1 (Dias 1 a 7):</b> Fundação psicoeducativa, calibração somática e conquista dos degraus 1 e 2.<br/>"
      "• <b>Semana 2 (Dias 8 a 14):</b> Consolidação intermediária, desmame de comportamentos de segurança e degraus 3 a 5.<br/>"
      "• <b>Semana 3 (Dias 15 a 21):</b> Expansão, degraus superiores, generalização contextual e plano de manutenção.", s["body"])
    story.append(Spacer(1, 10))

    p(story, "35. Folhas Diárias de Registro de Exposição (Dias 1 a 21)", s["h1"])
    story.append(hr())
    p(story, "Preencha uma folha para cada dia de treino. O registro sistemático do erro de predição é o que consolida o aprendizado no cérebro.", s["body"])
    story.append(Spacer(1, 6))

    # Gera exatamente 21 folhas individuais (uma por página/dupla)
    for d in range(1, 22):
        story.append(exposure_log(s, f"Dia {d:02d} — Registro Diário de Exposição"))
        if d % 2 == 0 or d == 21:
            story.append(PageBreak())

    # ═══════════ PARTE XIII CONCLUSÃO ═══════════
    section_break(story, "PARTE XIII", "Conclusão:\na coragem sustentável", s)

    p(story, "36. Tratamento sério, ético e libertador", s["h1"])
    story.append(hr())
    p(story, "Ao concluir este percurso, você não apenas conquistou degraus práticos em sua vida: você reconfigurou "
      "a relação com o seu próprio corpo e com as suas emoções. Com o método de David H. Barlow, a TCC e a nobre "
      "coragem do dragão, você aprendeu que a liberdade não é a ausência de vento, mas a arte de abrir as asas e voar.", s["body"])
    story.append(Spacer(1, 10))
    p(story, "<b>Dra. Priscila Palomo</b><br/>Psicóloga Clínica · CRP 98007<br/>"
      "Doutora em Psicologia pela Universitat de València (Cum Laude)<br/>"
      "Especialista em Fobias, Ansiedade e TCC<br/>"
      "www.priscilapalomo.com · WhatsApp: (11) 95069-0537", s["body_left"])
    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceBefore=8, spaceAfter=12))
    p(story, "Programa Escada Segura — Book Psicoeducativo Completo · Dra. Priscila Palomo", s["footer"])
    story.append(PageBreak())

    # ═══════════ APÊNDICES A a J (PRÁTICAS EXTRAS) ═══════════
    p(story, "Apêndice A — Diário Semanal de Autoeficácia", s["h1"])
    story.append(hr())
    for w in range(1, 9):
        p(story, f"<b>Semana {w}</b>", s["h2"])
        p(story, "Vitórias conquistadas nesta semana:", s["label"])
        story.append(blank_lines(2))
        p(story, "Esquivas identificadas e corrigidas:", s["label"])
        story.append(blank_lines(2))
        if w % 2 == 0:
            story.append(PageBreak())

    p(story, "Apêndice B — Banco de Frases de Enfrentamento", s["h1"])
    story.append(hr())
    phrases = [
        "É apenas uma resposta de alarme falso, não um perigo real.",
        "Meu corpo sabe como acelerar e sabe como desacelerar com segurança.",
        "Posso tolerar o desconforto enquanto meu cérebro aprende segurança.",
        "Um degrau de cada vez, com coragem de dragão.",
        "O que eu previa não é o que acontece na realidade.",
        "A ansiedade atinge o pico e desce naturalmente como uma onda.",
    ]
    for ph in phrases:
        p(story, f"• <i>“{ph}”</i>", s["body_left"])
    story.append(Spacer(1, 8))
    p(story, "Minhas frases personalizadas:", s["label"])
    story.append(blank_lines(6))
    story.append(PageBreak())

    p(story, "Apêndice C — Registros Extras de Treino Continuado", s["h1"])
    story.append(hr())
    for i in range(1, 61):
        story.append(exposure_log(s, f"Registro Extra de Treino #{i:02d}"))
        if i % 2 == 0:
            story.append(PageBreak())

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"OK: {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
