#!/usr/bin/env python3
"""Gera o book PDF Programa Escada Segura.
Totalmente remodelado:
- Cada capítulo tem EXATAMENTE 2 páginas:
  - Página 1: Título animado + Ilustração/Destaque visual + Historinha infantil / Metáfora lúdica (linguagem simples para 5 anos).
  - Página 2: A Ciência por trás (David H. Barlow, TCC, Neurobiologia) + Aplicação Prática e Experimento.
- Fácil de ler, diagramação arejada, sem páginas em branco desnecessárias.
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
        fontSize=12, textColor=ORANGE, alignment=TA_LEFT, spaceBefore=0, spaceAfter=3,
    )
    s["h1"] = ParagraphStyle(
        "h1", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=18, textColor=NAVY, spaceBefore=0, spaceAfter=6, leading=22,
    )
    s["h2"] = ParagraphStyle(
        "h2", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=13, textColor=INK, spaceBefore=10, spaceAfter=4, leading=17,
    )
    s["h3"] = ParagraphStyle(
        "h3", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=12, textColor=NAVY, spaceBefore=10, spaceAfter=4, leading=16,
    )
    s["body"] = ParagraphStyle(
        "body", parent=base["Normal"], fontName="Helvetica",
        fontSize=10.5, textColor=INK, alignment=TA_JUSTIFY, leading=16.5, spaceAfter=8,
    )
    s["body_left"] = ParagraphStyle(
        "body_left", parent=s["body"], alignment=TA_LEFT,
    )
    s["small"] = ParagraphStyle(
        "small", parent=base["Normal"], fontName="Helvetica",
        fontSize=9, textColor=MUTED, leading=13, spaceAfter=4,
    )
    s["quote"] = ParagraphStyle(
        "quote", parent=base["Normal"], fontName="Helvetica-Oblique",
        fontSize=11, textColor=NAVY, alignment=TA_CENTER, leading=16,
        spaceBefore=8, spaceAfter=8, leftIndent=12, rightIndent=12,
    )
    s["story"] = ParagraphStyle(
        "story", parent=base["Normal"], fontName="Helvetica-Oblique",
        fontSize=10.5, textColor=INK, alignment=TA_JUSTIFY, leading=16.5,
        spaceAfter=8, leftIndent=8, rightIndent=8,
    )
    s["label"] = ParagraphStyle(
        "label", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=10, textColor=ORANGE, spaceBefore=6, spaceAfter=3,
    )
    s["field"] = ParagraphStyle(
        "field", parent=base["Normal"], fontName="Helvetica",
        fontSize=8.5, textColor=MUTED, leading=12, spaceAfter=3,
    )
    s["toc"] = ParagraphStyle(
        "toc", parent=base["Normal"], fontName="Helvetica",
        fontSize=9, textColor=INK, leading=14, spaceAfter=2,
    )
    s["day_title"] = ParagraphStyle(
        "day_title", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=11, textColor=white, alignment=TA_LEFT, leading=14,
    )
    s["footer"] = ParagraphStyle(
        "footer", parent=base["Normal"], fontName="Helvetica",
        fontSize=8, textColor=MUTED, alignment=TA_CENTER,
    )
    return s


def hr():
    return HRFlowable(width="100%", thickness=1, color=LINE, spaceBefore=2, spaceAfter=8)


def ilustra(nome, largura=8.5 * cm):
    """Insere desenho vetorial centralizado."""
    img_path = IMG / (nome + ".png")
    if not img_path.exists():
        img_path = IMG / "alarme.png"
    img = Image(str(img_path))
    ratio = img.imageHeight / float(img.imageWidth)
    img.drawWidth = largura
    img.drawHeight = largura * ratio
    img.hAlign = "CENTER"
    return img


def bullets(items, style):
    return ListFlowable(
        [ListItem(Paragraph(i, style), leftIndent=6, bulletColor=NAVY) for i in items],
        bulletType="bullet", start="•", leftIndent=12, spaceBefore=1, spaceAfter=5,
    )


def blank_lines(n=2):
    rows = [["_" * 80] for _ in range(n)]
    t = Table(rows, colWidths=[16.5 * cm])
    t.setStyle(TableStyle([
        ("TEXTCOLOR", (0, 0), (-1, -1), LINE),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


def callout(title, text, s):
    header = Table([[Paragraph(title, s["day_title"])]], colWidths=[16.5 * cm])
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    body = Table([[Paragraph(text, s["body"])]], colWidths=[16.5 * cm])
    body.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
    ]))
    return KeepTogether([header, body, Spacer(1, 6)])


def day_box(title, paras, s):
    header = Table([[Paragraph(title, s["day_title"])]], colWidths=[16.5 * cm])
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    body = Table([[p] for p in paras], colWidths=[16.5 * cm])
    body.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (0, 0), 6),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 8),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
    ]))
    return KeepTogether([header, body, Spacer(1, 8)])


def ladder_template(s):
    header = [
        Paragraph("<font color='white'><b>#</b></font>", s["field"]),
        Paragraph("<font color='white'><b>Degrau (situação planejada)</b></font>", s["field"]),
        Paragraph("<font color='white'><b>Ansiedade (0–10)</b></font>", s["field"]),
    ]
    rows = [header]
    for i in range(1, 11):
        rows.append([
            Paragraph(str(i), s["field"]),
            Paragraph("_" * 44, s["field"]),
            Paragraph("_" * 10, s["field"]),
        ])
    t = Table(rows, colWidths=[1.2 * cm, 11 * cm, 4.3 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
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
        canvas.line(2 * cm, 1.6 * cm, A4[0] - 2 * cm, 1.6 * cm)
    canvas.restoreState()


def p(story, text, style):
    story.append(Paragraph(text, style))


def capitulo_duas_paginas(story, cap_num, tag, titulo, img_nome, hist_p1, hist_p2, ciencia_tit, ciencia_txt, pratica_tit, pratica_txt, licao_box, s):
    """Gera EXATAMENTE um capítulo de 2 páginas perfeitas:
    - Página 1: Cabeçalho animado + Ilustração fofa + Historinha infantil (5 anos).
    - Página 2: A Ciência de Barlow/TCC + Experimento/Prática + Caixa de Lição.
    """
    # ── PÁGINA 1: O Lado Lúdico e a Historinha ──
    story.append(Spacer(1, 0.4 * cm))
    p(story, f"CAPÍTULO {cap_num:02d} · {tag.upper()}", s["part"])
    p(story, titulo, s["h1"])
    story.append(hr())
    if img_nome:
        story.append(ilustra(img_nome, 8.5 * cm))
        story.append(Spacer(1, 8))
    p(story, "<b>A Historinha:</b>", s["label"])
    p(story, hist_p1, s["story"])
    if hist_p2:
        story.append(Spacer(1, 4))
        p(story, hist_p2, s["story"])
    story.append(PageBreak())

    # ── PÁGINA 2: A Ciência Rigorosa e o Treino ──
    story.append(Spacer(1, 0.4 * cm))
    p(story, f"A Ciência por trás: Capítulo {cap_num:02d}", s["h1"])
    p(story, f"<b>{ciencia_tit}</b>", s["h3"])
    story.append(hr())
    p(story, ciencia_txt, s["body"])
    story.append(Spacer(1, 6))
    p(story, f"<b>{pratica_tit}</b>", s["h3"])
    p(story, pratica_txt, s["body"])
    story.append(Spacer(1, 10))
    if licao_box:
        story.append(callout("Lição de Ouro da Escada Segura", licao_box, s))
    story.append(PageBreak())


def build():
    s = styles()
    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2.0 * cm,
        title="Programa Escada Segura — Book Completo",
        author="Dra. Priscila Palomo",
    )
    story = []

    # ═══════════ PÁGINA 1: CAPA ═══════════
    story.append(Spacer(1, 2.5 * cm))
    p(story, "DRA. PRISCILA PALOMO  ·  CRP 98007", s["cover_brand"])
    story.append(Spacer(1, 0.4 * cm))
    story.append(HRFlowable(width="40%", thickness=2, color=NAVY, spaceBefore=0, spaceAfter=14))
    p(story, "Programa Escada Segura", s["cover_title"])
    p(story, "Book Completo em 20 Capítulos de Duas Páginas<br/>Psicoeducação Lúdica, TCC e o Modelo de David H. Barlow", s["cover_sub"])
    story.append(Spacer(1, 0.6 * cm))
    story.append(ilustra("dragao", 6.5 * cm))
    story.append(Spacer(1, 0.6 * cm))
    p(story, "A coragem de um dragão · Degrau a degrau · Ciência e determinação", s["cover_sub"])
    story.append(Spacer(1, 1.0 * cm))
    p(story, "www.priscilapalomo.com", s["cover_brand"])
    story.append(PageBreak())

    # ═══════════ PÁGINA 2: AVISO ÉTICO ═══════════
    p(story, "Antes de Começar — Compromisso Ético e Cuidados", s["h1"])
    story.append(hr())
    p(story, "Este book foi criado como um <b>guia psicoeducativo estruturado</b>. Ele traduz os conceitos "
      "clínicos da Terapia Cognitivo-Comportamental (TCC) e o renomado modelo de regulação emocional de "
      "<b>David H. Barlow</b> em historinhas fáceis de entender, ilustrações amigáveis e exercícios práticos.", s["body"])
    p(story, "<b>Aviso Importante:</b> Este material tem finalidade de educação em saúde mental e treino "
      "de habilidades. Ele <b>não substitui a psicoterapia individualizada</b>, a avaliação diagnóstica "
      "nem o tratamento médico. Caso você apresente crises de pânico descompensadas, ideação suicida, trauma "
      "recente sem suporte ou faça uso de álcool/remédios sem orientação para tolerar o medo, procure "
      "um profissional de saúde mental antes de iniciar qualquer treino.", s["body"])
    p(story, "Se em algum momento a ansiedade parecer excessiva: <b>faça uma pausa</b>, utilize a respiração lenta "
      "e consulte seu psicólogo ou o CVV (188).", s["body"])
    story.append(Spacer(1, 8))
    p(story, "Dra. Priscila Palomo · Psicóloga (CRP 98007) · Especialista em Fobias e TCC · www.priscilapalomo.com", s["small"])
    story.append(PageBreak())

    # ═══════════ PÁGINA 3: SUMÁRIO GERAL ═══════════
    p(story, "Sumário Geral do Livro", s["h1"])
    story.append(hr())
    p(story, "<i>Cada capítulo foi desenhado exatamente em 2 páginas: a primeira é uma historinha gostosa de ler, "
             "e a segunda explica toda a ciência comprovada com exercícios claros.</i>", s["small"])
    story.append(Spacer(1, 4))
    toc = [
        "Capítulo 01 — O Alarme que Toca sem Fogo (O que é o Medo)",
        "Capítulo 02 — O Monstrinho que a Gente Alimenta (O Ciclo da Fuga)",
        "Capítulo 03 — Subir a Escada, um Degrau de Cada Vez (A Exposição)",
        "Capítulo 04 — A Piscina Fria e o Segredo do Tempo (A Habituação)",
        "Capítulo 05 — Ensinar o Cachorrinho Pipoca (O Cérebro que Aprende)",
        "Capítulo 06 — Soprar as Velinhas Devagar (O Freio do Corpinho)",
        "Capítulo 07 — Domar o Dragão Ryu (A Coragem que Transforma)",
        "Capítulo 08 — O Mapa do Templo (O que o DSM-5 Diz sobre as Fobias)",
        "Capítulo 09 — Os 5 Corredores do Medo (Os Subtipos de Fobia)",
        "Capítulo 10 — A Orquestra do Corpo (Taquicardia, Suor e Tremores)",
        "Capítulo 11 — Os Óculos Embaçados (Pensamentos Catastróficos)",
        "Capítulo 12 — Os Amuletos que Pesam (Comportamentos de Segurança)",
        "Capítulo 13 — O Segredo de David H. Barlow (Tríplice Vulnerabilidade)",
        "Capítulo 14 — O Erro de Predição (Como a Ciência Vence o Medo)",
        "Capítulo 15 — A Galeria dos Grandes Mestres (De Pavlov a Beck)",
        "Capítulo 16 — As Evidências que Curam (Metanálises e Estudos Clínicos)",
        "Capítulo 17 — A Arte do Kintsugi (Cicatrizes que Viram Ouro)",
        "Capítulo 18 — As Parábolas dos Templos (Sabedoria para Dias Difíceis)",
        "Capítulo 19 — Construindo a Sua Escada Pessoal (A Tabela Prática)",
        "Capítulo 20 — O Plano de 21 Dias e a Manutenção (A Liberdade Conquistada)",
    ]
    for item in toc:
        p(story, f"• <b>{item}</b>", s["toc"])
    story.append(PageBreak())

    # ═══════════ 20 CAPÍTULOS DE 2 PÁGINAS CADA (40 PÁGINAS) ═══════════

    # CAPÍTULO 1
    capitulo_duas_paginas(
        story, cap_num=1,
        tag="O que é o Medo",
        titulo="O Alarme que Toca sem Fogo",
        img_nome="alarme",
        hist_p1="Era uma vez uma casinha muito aconchegante onde morava um robozinho chamado Apitinho. "
                "Apitinho era o guarda da casa e tinha um trabalho muito importante: avisar se houvesse fogo de verdade! "
                "Quando via labaredas, ele gritava 'BEEP! BEEP!' para que todos saíssem correndo e ficassem em segurança. "
                "Esse era um alarme muito útil e salvava vidas.",
        hist_p2="Só que um dia, o morador resolveu tostar uma fatia de pão na torradeira. Saiu apenas um cheirinho gostoso "
                "e uma fumacinha minúscula. Apitinho se desesperou: 'SOCORRO! A CASA VAI EXPLODIR!' "
                "O coração do morador acelerou, as mãos suaram... mas quando olhou bem, não tinha fogo nenhum! "
                "O medo fóbico é igualzinho ao Apitinho: um guarda do bem, mas tão assustado que grita por causa de uma torrada.",
        ciencia_tit="O Modelo do 'Alarme Falso' de David H. Barlow",
        ciencia_txt="Na teoria neuropsicológica de David H. Barlow, o medo é um alarme biológico primário de sobrevivência "
                    "(luta/fuga). Nas fobias, ocorre o fenômeno do <b>Alarme Falso</b> (<i>False Alarm</i>): a amígdala cerebral "
                    "interpreta estímulos inofensivos como perigo fatal iminente, disparando adrenalina através do eixo HPA "
                    "(hipotálamo-hipófise-adrenal) sem haver risco objetivo.",
        pratica_tit="Aplicação Terapêutica na TCC",
        pratica_txt="A psicoeducação ensina o paciente a reconhecer que taquicardia e sudorese são apenas 'o Apitinho gritando por uma torrada'. "
                    "Estudos de Barlow & Craske (2014) comprovam que entender a natureza inofensiva do alarme reduz a hipervigilância "
                    "em até 40% já nas primeiras sessões.",
        licao_box="Sentir o coração bater forte diante do medo não significa que você está em perigo; significa apenas que seu alarme disparou por engano.",
        s=s,
    )

    # CAPÍTULO 2
    capitulo_duas_paginas(
        story, cap_num=2,
        tag="O Ciclo da Fuga",
        titulo="O Monstrinho que a Gente Alimenta",
        img_nome="monstrinho",
        hist_p1="Em uma floresta morava um monstrinho chamado Nhozinho. Ele era bem pequenininho, do tamanho de uma bolinha de gude. "
                "Mas Nhozinho adorava uma guloseima mágica: o 'Biscoito da Fuga'! "
                "Toda vez que uma criança via o Nhozinho e saía correndo apavorada, ele devorava um biscoito inteirinho.",
        hist_p2="Com aquele biscoito, Nhozinho dobrava de tamanho! No outro dia, a criança corria de novo, ele comia mais "
                "e virava do tamanho de um elefante! Sabe qual é o segredo para derrotar o Nhozinho? "
                "Ficar parado no lugar, respirando calmo. Sem a fuga, Nhozinho não ganha nenhum biscoito e vai encolhendo "
                "até voltar a caber no bolso.",
        ciencia_tit="O Reforço Negativo e a Manutenção do Medo",
        ciencia_txt="O modelo bifatorial de Mowrer e as pesquisas de Barlow explicam como a evitação mantém a fobia. "
                    "Ao fugir do estímulo temido, a ansiedade cai momentaneamente. Essa queda é um <b>reforço negativo potente</b>, "
                    "que grava na memória: 'Só sobrevivi porque fugi'.",
        pratica_tit="A Quebra do Ciclo na Prática",
        pratica_txt="Na TCC, suspendemos a fuga deliberadamente. Ao permanecer diante do estímulo temido, o cérebro não recebe "
                    "o 'biscoito da esquiva' e é obrigado a processar que a catástrofe imaginada não acontece.",
        licao_box="Fugir traz alívio por cinco minutos, mas faz o medo crescer pelo resto do ano. Ficar no lugar faz o medo encolher para sempre.",
        s=s,
    )

    # CAPÍTULO 3
    capitulo_duas_paginas(
        story, cap_num=3,
        tag="A Exposição Gradual",
        titulo="Subir a Escada, um Degrau de Cada Vez",
        img_nome="escada",
        hist_p1="Uma girafinha muito simpática sonhava em ver a lua do alto da torre do castelo. Mas a torre era altíssima "
                "e a girafinha morria de medo de altura. Se alguém falasse 'pule no topo da torre agora!', ela choraria "
                "e travaria as patinhas no chão.",
        hist_p2="O construtor do reino fez então uma escadinha com dez degraus baixinhos. No primeiro dia, ela pisou no "
                "degrau 1, que ficava rente à grama. Bateu palminhas e desceu! No segundo dia, subiu no degrau 2. "
                "Um passinho pequeno por dia, bem seguro. Quando percebeu, já estava lá no alto, sorrindo para a lua!",
        ciencia_tit="A Hierarquia Sistemática de Dessensibilização",
        ciencia_txt="A <b>Hierarquia de Exposição Gradual</b> (desenvolvida por Wolpe e aprimorada por Barlow e Antony) "
                    "divide o estímulo fóbico em Unidades Subjetivas de Desconforto (SUDS, 0–10). Isso previne a retraumatização "
                    "e constrói a autoeficácia descrita por Albert Bandura.",
        pratica_tit="Como Construir seus Degraus",
        pratica_txt="Listamos 10 passos progressivos: olhar fotos do medo (degrau 1), ver vídeos (degrau 3), observar de longe (degrau 5) "
                    "e tocar/aproximar-se (degraus 8 a 10). O avanço só ocorre quando o degrau atual estiver dominado.",
        licao_box="Você não precisa ter coragem para saltar uma montanha inteira. Só precisa de coragem para subir o próximo degrauzinho de dois centímetros.",
        s=s,
    )

    # CAPÍTULO 4
    capitulo_duas_paginas(
        story, cap_num=4,
        tag="A Habituação",
        titulo="A Piscina Fria e o Segredo do Tempo",
        img_nome="piscina",
        hist_p1="Num dia quente de verão, o ursinho Pingo pulou na piscina e gritou: 'BRRRR! ESTÁ CONGELANDO! QUERO SAIR!' "
                "Os pelinhos dele arrepiaram e ele quase saiu correndo. Mas a mamãe ursa segurou sua patinha com carinho "
                "e pediu que ele ficasse ali só três minutinhos cantando uma canção.",
        hist_p2="No primeiro minuto, Pingo ainda tremia. No segundo, já achava a água suportável. No quarto minuto, "
                "ele estava dando cambalhotas e achando a água quentinha! A água não mudou de temperatura mágica: foi o corpinho "
                "dele que se acostumou. O medo é igual: se você não fugir nos primeiros minutos, ele esfria sozinho!",
        ciencia_tit="O Processo de Habituação Neurovegetativa",
        ciencia_txt="A <b>Habituação</b> é a diminuição progressiva da resposta autonômica quando o estímulo é mantido sem perigo real. "
                    "Os receptores simpáticos sofrem saturação natural e o sistema parassimpático (nervo vago) entra em ação "
                    "para restaurar a homeostase corporal.",
        pratica_tit="A Curva de Ansiedade na Sessão",
        pratica_txt="A ansiedade atinge o pico entre 5 e 10 minutos de exposição e depois inicia um declínio espontâneo. "
                    "Permanecer na situação até que a aflição caia pelo menos 50% é o teste empírico que ensina o cérebro a relaxar.",
        licao_box="A ansiedade é como uma onda do mar: ela sobe, parece gigante, mas se você não fugir, ela quebra na praia e vira espuma mansa.",
        s=s,
    )

    # CAPÍTULO 5
    capitulo_duas_paginas(
        story, cap_num=5,
        tag="Neuroplasticidade",
        titulo="Ensinar o Cachorrinho Pipoca",
        img_nome="cachorrinho",
        hist_p1="O cachorrinho Pipoca morria de pavor do aspirador de pó. Quando o motor roncava, ele corria para baixo da cama "
                "e latia sem parar, achando que era um monstro faminto. Gritar com o Pipoca só o deixava mais nervoso.",
        hist_p2="O tutor inteligente colocou o aspirador desligado na sala e deu um petisco saboroso para o Pipoca quando ele cheirou o tubo. "
                "Depois ligou o aparelho bem longe e deu outro petisco. Em poucos dias, Pipoca dormia roncando gostoso bem ao lado "
                "do aspirador! O cérebro do Pipoca criou um novo arquivo de carinho e segurança.",
        ciencia_tit="O Aprendizado Inibitório e a Neuroplasticidade",
        ciencia_txt="Conforme os estudos contemporâneos de Michelle Craske e Joseph LeDoux, a terapia de exposição não apaga "
                    "a memória do medo na amígdala; ela cria uma <b>memória inibidora de segurança</b> no córtex pré-frontal "
                    "ventromedial (vmPFC), que passa a sobrepor e inibir o alarme antigo.",
        pratica_tit="Fortalecendo a Nova Rota Neural",
        pratica_txt="Cada repetição bem-sucedida de um degrau com desfecho seguro atua como um 'petisco neural', "
                    "reforçando as conexões pré-frontais e tornando a resposta de calma automática com o tempo.",
        licao_box="Seu cérebro é como uma massinha de modelar: com treino e repetição gentil, ele aprende novas rotas de tranquilidade.",
        s=s,
    )

    # CAPÍTULO 6
    capitulo_duas_paginas(
        story, cap_num=6,
        tag="O Freio do Corpo",
        titulo="Soprar as Velinhas Devagar",
        img_nome="velinha",
        hist_p1="O nosso corpinho é como um carrinho esportivo veloz. Quando o medo chega, é como se pisassem no acelerador: "
                "o motor ronca forte (o coração bate tum-tum-tum), a fumaça sai rápido (a respiração fica ofegante) e o carrinho quer voar!",
        hist_p2="Mas o fabricante do corpinho colocou um pedal de freio mágico super poderoso chamado Respiração Lenta! "
                "Para pisar no freio, é só puxar o ar pelo nariz cheirando uma florzinha (1, 2, 3, 4) e soltar pela boca "
                "bem devagarzinho, como quem sopra uma velinha de bolo sem querer apagá-la (1, 2, 3, 4, 5, 6). "
                "Em três sopros, o motor desacelera e a calma volta ao volante.",
        ciencia_tit="Regulação Autonômica e Estimulação Vagal",
        ciencia_txt="No modelo de Barlow & Craske (2007), o treino de <b>Respiração Diafragmática Lenta (4-6)</b> ativa os barorreceptores "
                    "pulmonares e carotídeos, estimulando o ramo parassimpático do nervo vago. Isso reduz a taquicardia e reverte a hipocapnia "
                    "gerada pela hiperventilação ansiosa.",
        pratica_tit="Treino Preventivo e não Esquiva",
        pratica_txt="A respiração regulada deve ser praticada diariamente em repouso e usada na exposição para dar estabilidade, "
                    "nunca como uma tentativa desesperada de 'fugir' das sensações normais de ansiedade.",
        licao_box="Você sempre carrega o freio do seu corpo no peito. Puxe o ar devagar, solte como um sopro longo e sinta o motor acalmar.",
        s=s,
    )

    # CAPÍTULO 7
    capitulo_duas_paginas(
        story, cap_num=7,
        tag="A Coragem que Transforma",
        titulo="Domar o Dragão Ryu",
        img_nome="dragao",
        hist_p1="Nos contos dos templos antigos, morava no topo da montanha um dragão imenso chamado Ryu. "
                "Todos os cavaleiros tentavam derrotá-lo com lanças pontiagudas, mas o dragão ficava furioso e queimava tudo ao redor. "
                "Quanto mais lutavam contra Ryu, mais feroz ele parecia.",
        hist_p2="Uma menina sábia subiu a montanha desarmada, sentou-se perto da caverna e ofereceu um cesto de amoras frescas. "
                "Ryu desceu mansinho, comeu as frutinhas e encostou a cabeça no ombro dela. "
                "Ela percebeu que o fogo do dragão não era maldade: era apenas pura energia e força! "
                "Quando você para de brigar contra o seu medo e aprende a acolhê-lo com carinho, aquela energia vira a sua maior coragem.",
        ciencia_tit="Aceitação Emocional no Protocolo Unificado",
        ciencia_txt="O Protocolo Unificado de David H. Barlow preconiza a <b>Aceitação Emocional Plena</b> e a flexibilidade psicológica. "
                    "Tentar suprimir ou lutar contra a ansiedade gera o 'efeito rebote', intensificando a reatividade límbica. "
                    "Acolher a emoção desativa a luta interna e direciona a energia para ações valorizadas.",
        pratica_tit="Ação Oposta ao Medo",
        pratica_txt="Em vez de contrair o corpo e recuar, adotamos a 'postura de dragão amigo': postura ereta, ombros relaxados "
                    "e aproximação voluntária da situação, permitindo que a energia da adrenalina alimente a determinação.",
        licao_box="Não precisamos matar o dragão com brigas e remédios; precisamos apenas ensiná-lo a caminhar ao nosso lado como guardião.",
        s=s,
    )

    # CAPÍTULO 8
    capitulo_duas_paginas(
        story, cap_num=8,
        tag="Diagnóstico Claro",
        titulo="O Mapa do Templo e o DSM-5",
        img_nome="alarme",
        hist_p1="Quando exploradores entram em uma floresta misteriosa, eles usam um mapa desenhado pelos antigos guardiões. "
                "O mapa não serve para dizer que a floresta é feia ou proibida; serve para mostrar onde estão as trilhas seguras "
                "e onde ficam os riachos de água limpa.",
        hist_p2="O DSM-5 é exatamente esse mapa dos psicólogos! Ele ensina que ter medo de algo específico por mais de seis meses "
                "não é frescura nem vergonha: é apenas uma trilha onde o alarme aprendeu a tocar mais alto. "
                "E tendo o mapa na mão, o caminho para a saída fica super claro e seguro.",
        ciencia_tit="Critérios Formais da Fobia Específica",
        ciencia_txt="O DSM-5-TR estabelece que a Fobia Específica é caracterizada por medo/ansiedade desproporcionais e imediatos "
                    "diante de um objeto ou situação, levando à evitação ativa por 6 meses ou mais, com sofrimento clinicamente "
                    "significativo ou prejuízo funcional.",
        pratica_tit="Diagnóstico Diferencial Clínico",
        pratica_txt="Diferenciamos fobia específica de Transtorno de Pânico (foco nos ataques inesperados) e Agorafobia (medo de não conseguir escapar). "
                    "O diagnóstico correto direciona a escolha do protocolo de exposição de alta precisão.",
        licao_box="O diagnóstico não é um rótulo para te prender; é uma bússola científica para te libertar com o tratamento certo.",
        s=s,
    )

    # CAPÍTULO 9
    capitulo_duas_paginas(
        story, cap_num=9,
        tag="Subtipos de Fobia",
        titulo="Os Cinco Corredores do Medo",
        img_nome="cachorrinho",
        hist_p1="Em um castelo de brincadeiras existem cinco portas coloridas. Atrás da porta vermelha moram os bichinhos (aranhas, cães, abelhas). "
                "Atrás da azul fica a natureza (alturas, tempestades, mar). Atrás da verde ficam as picadinhas de injeção e sangue. "
                "Atrás da amarela ficam os passeios (aviões, elevadores) e atrás da roxa ficam outros sustos.",
        hist_p2="Cada pessoa tem uma porta favorita que dá um friozinho na barriga. Mas a mágica é que a chave que abre todas as portas "
                "é a mesmíssima: a chave dourada da Escada Segura! Se você aprende a abrir uma porta, você aprende a abrir qualquer uma.",
        ciencia_tit="Especificadores Epidemiológicos de Barlow",
        ciencia_txt="O DSM-5 categoriza as fobias em: Animal, Ambiente Natural, Sangue-Injeção-Ferimentos (BII), Situacional e Outro. "
                    "O subtipo BII possui particularidade neurovegetativa: resposta bifásica com queda súbita de pressão (reflexo vasovagal).",
        pratica_tit="Técnica de Tensão Aplicada para Sangue e Agulhas",
        pratica_txt="Para o subtipo BII, Barlow e Öst prescrevem a <b>Tensão Aplicada</b> (contrair grandes músculos dos braços e pernas) "
                    "para manter a pressão arterial elevada durante a exposição, eliminando o risco de desmaios.",
        licao_box="Não importa a cor da porta do seu medo: a chave da exposição gradual e da respiração abre todas elas com segurança.",
        s=s,
    )

    # CAPÍTULO 10
    capitulo_duas_paginas(
        story, cap_num=10,
        tag="Sintomas no Corpo",
        titulo="A Orquestra do Corpo em Concerto",
        img_nome="velinha",
        hist_p1="Dentro de nós mora uma orquestra completa! O coração é o tambor (tum-tum!), o pulmão é o acordeom (entra ar, sai ar) "
                "e a pele é o sino que brilha com gotinhas de suor. Quando o alarme toca, o maestro acelera o ritmo para um batuque animado!",
        hist_p2="Às vezes a gente acha que o tambor acelerado vai estragar a orquestra, mas ele só está tocando a marcha da coragem! "
                "O tambor é resistente, foi feito para bater forte quando você corre ou brinca, e sabe desacelerar sozinho quando a música acaba.",
        ciencia_tit="A Fisiologia da Resposta Simpatoadrenal",
        ciencia_txt="A descarga adrenérgica desencadeada pela amígdala produz taquicardia sinusal, aumento do débito cardíaco, "
                    "midríase pupilar e vasoconstrição periférica. Trata-se de um mecanismo evolutivo projetado para proteger a integridade física.",
        pratica_tit="Tolerância Interoceptiva sem Pânico",
        pratica_txt="Exercícios de exposição interoceptiva de Barlow (como girar na cadeira ou subir escadas) dessensibilizam o medo das sensações físicas, "
                    "provando empiricamente que o coração acelerado é saudável e temporário.",
        licao_box="O tambor do seu peito é forte e foi projetado para bater rápido sem quebrar. Ele só está tocando a música da sua prontidão.",
        s=s,
    )

    # CAPÍTULO 11
    capitulo_duas_paginas(
        story, cap_num=11,
        tag="Pensamentos e Lentes",
        titulo="Os Óculos Embaçados de Monstro",
        img_nome="alarme",
        hist_p1="Era uma vez um menininho que usava óculos mágicos. Só que quando ele sentia medo, as lentes dos óculos ficavam embaçadas "
                "com desenhos de monstros! Uma sombrinha de árvore parecia um gigante com dentes afiados, e um gatinho parecia um tigre feroz.",
        hist_p2="Quando ele limpava as lentes com o paninho da verdade, ele olhava de novo e caía na gargalhada: 'Olha só, era só a folhinha da árvore!' "
                "A nossa cabeça faz igual: quando o medo aperta, ela coloca óculos embaçados de catástrofe. A gente só precisa limpar as lentes com fatos reais.",
        ciencia_tit="Erros de Processamento e Reestruturação Cognitiva",
        ciencia_txt="A TCC de Aaron Beck e David Barlow identifica distorções como <b>Superestimação de Probabilidade</b> "
                    "(superestimar o risco de desastre) e <b>Catastrofização</b> (subestimar a capacidade de enfrentamento).",
        pratica_tit="O Questionamento Socrático com Dados Reais",
        pratica_txt="Testamos a probabilidade real: 'Quantas pessoas pegaram este elevador hoje sem cair?' "
                    "A reestruturação substitui crenças automáticas por pensamentos balanceados e ancorados em estatísticas reais.",
        licao_box="Pensamento não é fato; é apenas uma historinha que a mente conta. Limpe as lentes e olhe os dados reais do mundo.",
        s=s,
    )

    # CAPÍTULO 12
    capitulo_duas_paginas(
        story, cap_num=12,
        tag="Comportamentos de Segurança",
        titulo="Os Amuletos que Pesam na Mochila",
        img_nome="monstrinho",
        hist_p1="Um macaquinho decidiu passear pela montanha levando uma mochila cheia de pedras pesadas que ele chamava de 'Pedras da Sorte'. "
                "Ele achava que só não caía da montanha porque carregava aquela mochila pesadíssima.",
        hist_p2="Com o tempo, a mochila machucava as costas e ele não conseguia pular de galho em galho. Um dia, tirou uma pedra... "
                "e viu que suas patinhas eram super firmes! Tirou todas as pedras e saiu saltitando leve e livre. "
                "As nossas 'muletas' de segurança parecem proteger, mas são pesos que não deixam a gente descobrir nossa própria força.",
        ciencia_tit="O Impacto Nocivo dos Comportamentos de Segurança",
        ciencia_txt="Pesquisas de Salkovskis e Barlow evidenciam que amuletos de segurança (estar sempre com garrafa d'água, segurar braços, checagens) "
                    "atribuem o sucesso do enfrentamento ao amuleto, impedindo a consolidação da autoeficácia genuína.",
        pratica_tit="Desmame Gradual das Muletas de Segurança",
        pratica_txt="No plano de 21 dias, desmamamos os comportamentos de segurança um por um: primeiro com o amuleto presente sem uso, "
                    "depois no bolso, e finalmente ausente, demonstrando capacidade autônoma.",
        licao_box="Solte as pedras da mochila. Suas próprias pernas e pulmões são fortes o suficiente para subir a montanha inteira.",
        s=s,
    )

    # CAPÍTULO 13
    capitulo_duas_paginas(
        story, cap_num=13,
        tag="A Teoria Central",
        titulo="O Segredo de David H. Barlow",
        img_nome="dragao",
        hist_p1="David Barlow é como o grande arquiteto de brinquedos da psicologia moderna. Ele descobriu que as pessoas com medo "
                "não têm nenhum defeito de fabricação. Elas apenas têm três pecinhas especiais no castelo da mente.",
        hist_p2="A primeira pecinha é um coração sensível que sente tudo com intensidade. A segunda é a ideia de que o mundo é imprevisível. "
                "E a terceira é um alarme que grudou num objeto específico. Barlow criou um manual de montagem para recalibrar essas pecinhas "
                "e transformar o castelo numa fortaleza de paz.",
        ciencia_tit="A Teoria da Tríplice Vulnerabilidade",
        ciencia_txt="Barlow postula a interação de três vulnerabilidades: <b>1. Biológica Geral</b> (temperamento reativo/neuroticismo), "
                    "<b>2. Psicológica Geral</b> (senso de incontrolabilidade precoce) e <b>3. Psicológica Específica</b> (associação precoce de perigo a um estímulo).",
        pratica_tit="O Protocolo Unificado Aplicado",
        pratica_txt="O tratamento foca na vulnerabilidade psicológica específica por meio da exposição focada, "
                    "aumentando concomitantemente o senso global de controle pessoal e regulação afetiva.",
        licao_box="Você não é frágil: você tem um sistema de proteção sofisticado que só precisa de um novo manual de instruções.",
        s=s,
    )

    # CAPÍTULO 14
    capitulo_duas_paginas(
        story, cap_num=14,
        tag="A Ciência da Cura",
        titulo="O Erro Mágico de Predição",
        img_nome="piscina",
        hist_p1="Imagine uma cartomante de mentirinha que sempre dizia: 'Se você encostar no cachorrinho, um raio vai cair do céu!' "
                "A criança ficava morrendo de medo. Mas um dia, ela tocou no focinho macio do cãozinho... e nada de raio! "
                "Caiu foi uma chuva de carinho e lambidas gostosas.",
        hist_p2="A cabeça da criança deu um 'clique' mágico: 'Nossa, a cartomante do medo errou feio!' "
                "Toda vez que a previsão de desastre dá errado, o cérebro aprende uma verdade nova e o medo perde todo o poder.",
        ciencia_tit="Violação de Expectativa (Craske et al., 2014)",
        ciencia_txt="O modelo moderno de Aprendizado Inibitório demonstra que a eficácia da exposição decorre do <b>Erro de Predição</b> "
                    "(<i>Prediction Error</i>): a diferença entre a alta expectativa de dano e o desfecho neutro real observado.",
        pratica_tit="O Diário de Predição vs. Realidade",
        pratica_txt="Antes de cada degrau, o paciente registra exatamente: 'Qual desastre espero que aconteça?' "
                    "Após o treino, registra: 'O que aconteceu de fato?' Esse contraste sistemático desativa a rede fóbica.",
        licao_box="O medo é péssimo em fazer previsões do futuro. Ele sempre promete tempestade, mas a realidade entrega calmaria.",
        s=s,
    )

    # CAPÍTULO 15
    capitulo_duas_paginas(
        story, cap_num=15,
        tag="Mestres da Psicologia",
        titulo="A Galeria dos Grandes Mestres",
        img_nome="escada",
        hist_p1="Em uma biblioteca mágica cheia de livros brilhantes, vários mestres sábios deixaram conselhos para quem quer ser livre. "
                "Pavlov ensinou que sinos tocam por associação. Mary Cover Jones mostrou que carinho e coelhinhos curam sustos.",
        hist_p2="Wolpe desenhou os primeiros degraus. Beck ensinou a limpar as lentes da mente. Bandura mostrou que pequenas vitórias geram gigantes! "
                "E Barlow reuniu tudo num protocolo perfeito. Você não está sozinho: os maiores sábios da humanidade construíram a sua escada.",
        ciencia_tit="A Evolução Histórica da Ciência Comportamental",
        ciencia_txt="A linhagem científica da TCC abrange o condicionamento clássico (Pavlov), a contracondicionamento (Jones), "
                    "a dessensibilização sistemática (Wolpe), a reestruturação cognitiva (Beck), a autoeficácia (Bandura) e o modelo transdiagnóstico de Barlow.",
        pratica_tit="A Força de um Método Centenário",
        pratica_txt="Ao subir a Escada Segura, você está utilizando mais de 100 anos de pesquisa empírica rigorosamente validada em milhares de universidades mundiais.",
        licao_box="Você está amparado pelos maiores cientistas da história da mente humana. O método é seguro, comprovado e funciona.",
        s=s,
    )

    # CAPÍTULO 16
    capitulo_duas_paginas(
        story, cap_num=16,
        tag="Evidências Científicas",
        titulo="A Ciência que Liberta",
        img_nome="dragao",
        hist_p1="Em um laboratório do castelo, cientistas com jalecos brancos e lupas gigantes analisaram milhares de crianças e adultos "
                "que tinham medo de tempestades, alturas e agulhas. Eles queriam ter certeza absoluta de qual remédio da mente funcionava de verdade.",
        hist_p2="Descobriram que quem usava a Escada Segura vencia o medo de forma definitiva em mais de 80% das vezes! "
                "Não era mágica, não era sorte: era ciência de verdade funcionando no cérebro de todo mundo que praticava.",
        ciencia_tit="Metanálises e Ensaios Clínicos Padrão-Ouro",
        ciencia_txt="Estudos clínicos multicêntricos (Barlow et al., 2017; Wolitzky-Taylor et al., 2008) comprovam que a TCC com exposição "
                    "apresenta tamanhos de efeito d > 1.2, superando largamente placebos e abordagens farmacológicas isoladas.",
        pratica_tit="Manutenção de Longo Prazo dos Ganhos",
        pratica_txt="Seguimentos de 2 a 5 anos mostram que os ganhos obtidos pela reestruturação pré-frontal são duradouros e generalizam-se "
                    "para outros contextos da vida cotidiana.",
        licao_box="Você não está testando um palpite: está aplicando a intervenção mais comprovada e eficaz da ciência psicológica moderna.",
        s=s,
    )

    # CAPÍTULO 17
    capitulo_duas_paginas(
        story, cap_num=17,
        tag="A Arte da Resiliência",
        titulo="O Ouro que Cura as Rachaduras",
        img_nome="velinha",
        hist_p1="No Japão existe uma arte mágica chamada Kintsugi. Quando uma xícara de chá querida cai no chão e quebra, "
                "os mestres não jogam os pedaços no lixo! Eles colam cada pedaço usando ouro derretido brilhante.",
        hist_p2="A xícara fica ainda mais linda, valiosa e forte do que quando era nova! Os dias em que você treme ou sente medo "
                "não são dias perdidos: são as rachaduras onde o seu ouro de coragem vai entrar e te deixar mais forte do que nunca.",
        ciencia_tit="Tolerância à Frustração e Anti-Fragilidade",
        ciencia_txt="Na TCC baseada em Barlow, as oscilações e recaídas temporárias não são vistas como falha, mas como oportunidades ricas "
                    "de teste de resiliência e consolidação do aprendizado em contextos adversos.",
        pratica_tit="Celebrando os Micro-Progressos",
        pratica_txt="Registramos cada sessão difícil como uma 'linha de ouro'. O paciente desenvolve auto-compaixão e perseverança metodológica.",
        licao_box="Suas cicatrizes e seus dias difíceis não são defeitos: são as linhas de ouro que mostram o quanto você é corajoso.",
        s=s,
    )

    # CAPÍTULO 18
    capitulo_duas_paginas(
        story, cap_num=18,
        tag="Sabedoria dos Templos",
        titulo="Parábolas para Dias Nublados",
        img_nome="alarme",
        hist_p1="Um viajante subia a montanha em direção ao templo, mas uma névoa espessa cobriu tudo e ele não via o cume da montanha. "
                "Ele sentou e chorou de medo de cair. O monge do templo desceu e disse: 'Você não precisa enxergar o topo agora. Só precisa pisar na próxima pedra diante do seu pé.'",
        hist_p2="Ele deu um passo, depois outro, e outro... e quando percebeu, o sol raiou e ele estava no templo sagrado! "
                "Nos dias nublados, você não precisa resolver a vida inteira: só precisa dar o próximo passinho seguro.",
        ciencia_tit="Mindfulness e Foco no Momento Presente",
        ciencia_txt="O Protocolo Unificado de Barlow integra a <b>Ancoragem no Presente</b> como antídoto contra a ansiedade antecipatória crônica, "
                    "reduzindo a ruminação cognitiva e o esgotamento atencional.",
        pratica_tit="A Âncora Sensorial 5-4-3-2-1",
        pratica_txt="Diante da névoa da ansiedade, nomeie 5 objetos visíveis, 4 texturas tácteis, 3 sons, 2 aromas e 1 respiração profunda.",
        licao_box="Não tente escalar o futuro inteiro hoje. Dê apenas o passo que cabe nos seus pés neste exato minuto.",
        s=s,
    )

    # CAPÍTULO 19
    capitulo_duas_paginas(
        story, cap_num=19,
        tag="Montagem da Escada",
        titulo="Construindo a Sua Escada Pessoal",
        img_nome="escada",
        hist_p1="Chegou a hora de sermos os mestres construtores da nossa própria escadinha! Pegue sua régua mágica de 0 a 10. "
                "O zero é um banho quentinho com cheiro de sabonete. O dez é o susto mais gigante que você consegue imaginar.",
        hist_p2="Vamos desenhar dez degraus confortáveis. Nenhum degrau pode ser alto demais para suas pernas. "
                "Vamos começar pelo mais gostoso e subir com calma, comemorando cada conquista com estrelinhas douradas!",
        ciencia_tit="Parametrização Psicométrica da Hierarquia",
        ciencia_txt="A escala SUDS (0–10) quantifica o nível de afeto negativo. A escada ideal possui intervalos regulares (diferença de 1 a 2 pontos entre degraus), "
                    "evitando saltos abruptos que disparariam esquiva defensiva.",
        pratica_tit="Tabela Prática para Preenchimento",
        pratica_txt="Preencha a tabela de 10 degraus com ações específicas, mensuráveis e sob seu controle direto.",
        licao_box="A sua escada é única e sob medida para você. Respeite o seu ritmo e comemore cada degrau vencido.",
        s=s,
    )

    # CAPÍTULO 20
    capitulo_duas_paginas(
        story, cap_num=20,
        tag="O Plano de 21 Dias",
        titulo="A Jornada de 21 Dias para a Liberdade",
        img_nome="dragao",
        hist_p1="Em 21 dias os passarinhos aprendem a bater as asas e saem voando pelo céu azul. "
                "A sua jornada de 21 dias é o ninho onde você treina suas asas de coragem!",
        hist_p2="Na primeira semana, conhecemos o ninho e treinamos o freio. Na segunda semana, damos pequenos voos perto da árvore. "
                "Na terceira semana, você abre as asas e voa livre por onde sempre sonhou! O mundo inteiro está te esperando.",
        ciencia_tit="Consolidação e Prevenção de Recaída de Barlow",
        ciencia_txt="O período de 21 dias proporciona repetições suficientes para estabilização de longo prazo da rota inibitória no vmPFC, "
                    "com redução sistemática de comportamentos de esquiva.",
        pratica_tit="Plano de Manutenção Vitalícia",
        pratica_txt="Mantenha 1 a 2 exposições mensais de reforço. Se o musgo da evitação reaparecer, escove o degrau imediatamente.",
        licao_box="Você conquistou a sua liberdade com ciência, método e carinho. Abra as asas e viva a sua vida por inteiro!",
        s=s,
    )

    # ═══════════ TABELA PRÁTICA DA ESCADA PESSOAL (PÁGINA DEDICADA) ═══════════
    p(story, "Sua Tabela Prática da Escada Segura (Preencha Aqui)", s["h1"])
    story.append(hr())
    p(story, "<i>Escreva os seus 10 degraus de treino, do menor para o maior desconforto esperado (SUDS 0 a 10):</i>", s["small"])
    story.append(Spacer(1, 6))
    story.append(ladder_template(s))
    story.append(PageBreak())

    # ═══════════ 21 FOLHAS DIÁRIAS INDIVIDUAIS DE REGISTRO ═══════════
    p(story, "Caderno Diário de Registros de Exposição (21 Dias)", s["h1"])
    story.append(hr())
    p(story, "Preencha uma folha para cada dia de treino. O registro sistemático do <b>Erro de Predição</b> "
             "(catástrofe imaginada vs. desfecho real observado) é a chave comprovada pela neurociência de Barlow para reconfigurar o cérebro.", s["body"])
    story.append(Spacer(1, 6))

    for d in range(1, 22):
        story.append(exposure_log(s, f"Dia {d:02d} — Folha Diária de Registro de Exposição"))
        story.append(PageBreak())

    # ═══════════ APÊNDICES COMPLEMENTARES ═══════════
    p(story, "Apêndice A — Diário Semanal de Autoeficácia (8 Semanas)", s["h1"])
    story.append(hr())
    for w in range(1, 9):
        p(story, f"<b>Semana {w:02d} de Manutenção</b>", s["h2"])
        p(story, "Degraus e vitórias conquistadas nesta semana:", s["label"])
        story.append(blank_lines(2))
        p(story, "Amuletos/esquivas soltos com sucesso:", s["label"])
        story.append(blank_lines(2))
        if w % 2 == 0:
            story.append(PageBreak())

    p(story, "Apêndice B — Banco de Frases de Enfrentamento de Barlow", s["h1"])
    story.append(hr())
    phrases = [
        "É apenas um alarme falso inofensivo; meu corpo está saudável e seguro.",
        "A ansiedade atinge o pico e desce naturalmente como uma onda mansa.",
        "Posso tolerar este desconforto passageiro enquanto meu cérebro aprende.",
        "O que o medo previa nunca é o que acontece de verdade.",
        "Estou desmamando as muletas e descobrindo a minha própria força.",
        "Um degrauzinho de cada vez, respirando com calma e coragem de dragão.",
    ]
    for ph in phrases:
        p(story, f"• <i>“{ph}”</i>", s["body_left"])
    story.append(Spacer(1, 6))
    p(story, "Minhas frases de poder personalizadas:", s["label"])
    story.append(blank_lines(6))
    story.append(PageBreak())

    p(story, "Apêndice C — Folhas Extras de Treino Continuado", s["h1"])
    story.append(hr())
    for i in range(1, 21):
        story.append(exposure_log(s, f"Folha Extra de Treino #{i:02d}"))
        story.append(PageBreak())

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"OK: {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
