#!/usr/bin/env python3
"""Gera o workbook PDF do Programa Escada Segura."""

from pathlib import Path

from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable, ListFlowable, ListItem,
)

NAVY = HexColor("#14324B")
INK = HexColor("#111111")
MUTED = HexColor("#555555")
LINE = HexColor("#CCCCCC")
PALE = HexColor("#F2F5F8")
ACCENT = HexColor("#2E8B57")

OUT = Path(__file__).resolve().parents[1] / "pdfs" / "programa-escada-segura.pdf"


def styles():
    base = getSampleStyleSheet()
    s = {}
    s["cover_brand"] = ParagraphStyle(
        "cover_brand", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=11, textColor=NAVY,
        alignment=TA_CENTER, letterSpacing=2, spaceAfter=8,
    )
    s["cover_title"] = ParagraphStyle(
        "cover_title", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=28, textColor=INK,
        alignment=TA_CENTER, leading=34, spaceAfter=14,
    )
    s["cover_sub"] = ParagraphStyle(
        "cover_sub", parent=base["Normal"],
        fontName="Helvetica", fontSize=12, textColor=MUTED,
        alignment=TA_CENTER, leading=18, spaceAfter=8,
    )
    s["h1"] = ParagraphStyle(
        "h1", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=18, textColor=NAVY,
        spaceBefore=6, spaceAfter=12, leading=22,
    )
    s["h2"] = ParagraphStyle(
        "h2", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=13, textColor=INK,
        spaceBefore=14, spaceAfter=8, leading=17,
    )
    s["h3"] = ParagraphStyle(
        "h3", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=11, textColor=NAVY,
        spaceBefore=10, spaceAfter=6, leading=14,
    )
    s["body"] = ParagraphStyle(
        "body", parent=base["Normal"],
        fontName="Helvetica", fontSize=10, textColor=INK,
        alignment=TA_JUSTIFY, leading=15, spaceAfter=8,
    )
    s["body_left"] = ParagraphStyle(
        "body_left", parent=s["body"], alignment=TA_LEFT,
    )
    s["small"] = ParagraphStyle(
        "small", parent=base["Normal"],
        fontName="Helvetica", fontSize=8.5, textColor=MUTED,
        leading=12, spaceAfter=6,
    )
    s["quote"] = ParagraphStyle(
        "quote", parent=base["Normal"],
        fontName="Helvetica-Oblique", fontSize=11, textColor=NAVY,
        alignment=TA_CENTER, leading=16, spaceBefore=10, spaceAfter=10,
        leftIndent=20, rightIndent=20,
    )
    s["disclaimer"] = ParagraphStyle(
        "disclaimer", parent=base["Normal"],
        fontName="Helvetica", fontSize=8.5, textColor=MUTED,
        alignment=TA_JUSTIFY, leading=12, spaceBefore=8, spaceAfter=8,
        backColor=PALE, borderPadding=8,
    )
    s["day_title"] = ParagraphStyle(
        "day_title", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=12, textColor=white,
        alignment=TA_LEFT, leading=15,
    )
    s["label"] = ParagraphStyle(
        "label", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=9, textColor=NAVY,
        spaceBefore=6, spaceAfter=3,
    )
    s["field"] = ParagraphStyle(
        "field", parent=base["Normal"],
        fontName="Helvetica", fontSize=9, textColor=MUTED,
        leading=13, spaceAfter=4,
    )
    s["toc"] = ParagraphStyle(
        "toc", parent=base["Normal"],
        fontName="Helvetica", fontSize=11, textColor=INK,
        leading=20, spaceAfter=2,
    )
    s["footer"] = ParagraphStyle(
        "footer", parent=base["Normal"],
        fontName="Helvetica", fontSize=8, textColor=MUTED,
        alignment=TA_CENTER,
    )
    return s


def hr():
    return HRFlowable(width="100%", thickness=1, color=LINE, spaceBefore=4, spaceAfter=10)


def bullet_list(items, style):
    return ListFlowable(
        [ListItem(Paragraph(i, style), leftIndent=8, bulletColor=NAVY) for i in items],
        bulletType="bullet",
        start="•",
        leftIndent=16,
        spaceBefore=2,
        spaceAfter=8,
    )


def day_box(title, content_paras, s):
    header = Table(
        [[Paragraph(title, s["day_title"])]],
        colWidths=[16.5 * cm],
    )
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    body_cells = [[p] for p in content_paras]
    body = Table(body_cells, colWidths=[16.5 * cm])
    body.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (0, 0), 8),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 10),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
    ]))
    return KeepTogether([header, body, Spacer(1, 10)])


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


def scale_table(s):
    data = [
        [Paragraph("<b>Nível</b>", s["field"]),
         Paragraph("<b>Sensação no corpo</b>", s["field"]),
         Paragraph("<b>O que fazer</b>", s["field"])],
        [Paragraph("0–2", s["field"]),
         Paragraph("Tranquilo / leve tensão", s["field"]),
         Paragraph("Bom ponto para treinar", s["field"])],
        [Paragraph("3–4", s["field"]),
         Paragraph("Desconforto manejável", s["field"]),
         Paragraph("Zona ideal de aprendizado", s["field"])],
        [Paragraph("5–6", s["field"]),
         Paragraph("Ansiedade alta, mas possível", s["field"]),
         Paragraph("Use técnicas e continue se seguro", s["field"])],
        [Paragraph("7–10", s["field"]),
         Paragraph("Muito intenso / panico", s["field"]),
         Paragraph("Desça 1–2 degraus e estabilize", s["field"])],
    ]
    t = Table(data, colWidths=[2.2 * cm, 6.5 * cm, 7.8 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("BACKGROUND", (0, 1), (-1, -1), PALE),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    # Fix header text color for Paragraphs
    data[0] = [
        Paragraph("<font color='white'><b>Nível</b></font>", s["field"]),
        Paragraph("<font color='white'><b>Sensação no corpo</b></font>", s["field"]),
        Paragraph("<font color='white'><b>O que fazer</b></font>", s["field"]),
    ]
    t = Table(data, colWidths=[2.2 * cm, 6.5 * cm, 7.8 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("BACKGROUND", (0, 1), (-1, -1), PALE),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def ladder_template(s):
    header = [
        Paragraph("<font color='white'><b>#</b></font>", s["field"]),
        Paragraph("<font color='white'><b>Degrau (situação)</b></font>", s["field"]),
        Paragraph("<font color='white'><b>Ansiedade esperada (0–10)</b></font>", s["field"]),
    ]
    rows = [header]
    for i in range(1, 11):
        rows.append([
            Paragraph(str(i), s["field"]),
            Paragraph("_" * 42, s["field"]),
            Paragraph("_" * 12, s["field"]),
        ])
    t = Table(rows, colWidths=[1.2 * cm, 10.5 * cm, 4.8 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("BACKGROUND", (0, 1), (-1, -1), white),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def exposure_log(s, day_label):
    paras = [
        Paragraph(f"<b>{day_label}</b>", s["label"]),
        Paragraph("Degrau trabalhado hoje: ________________________________", s["field"]),
        Paragraph("Ansiedade antes (0–10): ____ &nbsp;&nbsp; no pico: ____ &nbsp;&nbsp; depois: ____", s["field"]),
        Paragraph("O que fiz exatamente:", s["label"]),
        blank_lines(2),
        Paragraph("O que o medo previa que aconteceria?", s["label"]),
        blank_lines(2),
        Paragraph("O que de fato aconteceu?", s["label"]),
        blank_lines(2),
        Paragraph("Aprendizado de hoje:", s["label"]),
        blank_lines(2),
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
            f"Programa Escada Segura  ·  Dra. Priscila Palomo  ·  p. {page}"
        )
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.4)
        canvas.line(2 * cm, 1.7 * cm, A4[0] - 2 * cm, 1.7 * cm)
    canvas.restoreState()


def build():
    s = styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2.2 * cm,
        title="Programa Escada Segura",
        author="Dra. Priscila Palomo",
    )
    story = []

    # ── CAPA ──
    story.append(Spacer(1, 3.5 * cm))
    story.append(Paragraph("DRA. PRISCILA PALOMO  ·  CRP 98007", s["cover_brand"]))
    story.append(Spacer(1, 0.6 * cm))
    story.append(HRFlowable(width="40%", thickness=2, color=NAVY, spaceBefore=0, spaceAfter=16))
    story.append(Paragraph("Programa Escada Segura", s["cover_title"]))
    story.append(Paragraph(
        "Workbook de 21 dias para vencer fobias específicas<br/>com exposição gradual — passo a passo, no seu ritmo.",
        s["cover_sub"],
    ))
    story.append(Spacer(1, 1.2 * cm))
    story.append(Paragraph(
        "Material psicoeducativo baseado em Terapia Cognitivo-Comportamental (TCC).",
        s["cover_sub"],
    ))
    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph("www.priscilapalomo.com", s["cover_brand"]))
    story.append(PageBreak())

    # ── AVISO ÉTICO ──
    story.append(Paragraph("Antes de começar", s["h1"]))
    story.append(hr())
    story.append(Paragraph(
        "Este workbook é um <b>material psicoeducativo</b>. Ele ensina princípios "
        "científicos da exposição gradual para fobias específicas e oferece um "
        "plano estruturado de 21 dias para você praticar com segurança e consciência.",
        s["body"],
    ))
    story.append(Paragraph(
        "<b>Importante:</b> este programa <b>não substitui psicoterapia</b>, avaliação "
        "clínica nem tratamento médico. Se você tem crise de pânico intensa, ideação "
        "suicida, transtorno alimentar ativo, trauma recente sem acompanhamento, ou "
        "usa substâncias para enfrentar o medo, procure ajuda profissional antes de "
        "iniciar exposições sozinho(a).",
        s["body"],
    ))
    story.append(Paragraph(
        "Se em qualquer momento a ansiedade ficar incontrolável, <b>pare</b>, use as "
        "técnicas de regulação deste material e, se necessário, contate um profissional "
        "de saúde mental ou o CVV (188).",
        s["body"],
    ))
    story.append(Paragraph(
        "A Dra. Priscila Palomo (CRP 98007) atende online e presencialmente. "
        "WhatsApp: (11) 95069-0537 · www.priscilapalomo.com",
        s["small"],
    ))
    story.append(PageBreak())

    # ── SUMÁRIO ──
    story.append(Paragraph("Sumário", s["h1"]))
    story.append(hr())
    toc_items = [
        "1. Como o medo funciona",
        "2. O que é exposição gradual",
        "3. Sua Escada Segura — como montar",
        "4. Escala de ansiedade (0–10)",
        "5. Técnicas de regulação",
        "6. Regras de ouro do programa",
        "6b. Comportamentos de segurança",
        "7. Plano de 21 dias",
        "8. Folhas de registro diário",
        "9. Revisão final e próximos passos",
        "10. Modelos extras (imprimíveis)",
    ]
    for item in toc_items:
        story.append(Paragraph(item, s["toc"]))
    story.append(PageBreak())

    # ── 1. COMO O MEDO FUNCIONA ──
    story.append(Paragraph("1. Como o medo funciona", s["h1"]))
    story.append(hr())
    story.append(Paragraph(
        "O medo é um sistema de alarme do corpo. Ele existe para nos proteger. "
        "Em uma fobia específica, esse alarme dispara com força diante de algo que, "
        "na maior parte das vezes, <b>não representa perigo real proporcional</b> "
        "à reação que sentimos.",
        s["body"],
    ))
    story.append(Paragraph(
        "Quando o alarme toca, o sistema nervoso ativa a resposta de luta/fuga: "
        "coração acelerado, respiração curta, suor, tremor, vontade de fugir. "
        "Isso é fisiologia — não é “fraqueza” nem “falta de vontade”.",
        s["body"],
    ))
    story.append(Paragraph("O ciclo que mantém a fobia", s["h2"]))
    story.append(bullet_list([
        "<b>Gatilho</b> — situação, imagem, pensamento ou sensação ligada ao medo.",
        "<b>Alarme</b> — ansiedade sobe rápido.",
        "<b>Evitação</b> — você foge, adia ou pede “segurança” (alguém junto, remédio “por precaução”, checagens).",
        "<b>Alívio imediato</b> — a ansiedade cai… e o cérebro aprende: “fugir funcionou”.",
        "<b>Medo maior amanhã</b> — o monstro cresce porque nunca foi testado de verdade.",
    ], s["body_left"]))
    story.append(Paragraph(
        "A boa notícia: fobias específicas estão entre os quadros com <b>melhor resposta</b> "
        "à terapia baseada em evidência — especialmente a exposição gradual.",
        s["body"],
    ))
    story.append(Paragraph("Medo útil × medo desproporcional", s["h2"]))
    story.append(Paragraph(
        "Medo útil: você está em uma rua escura e acelera o passo. "
        "Medo desproporcional: a ideia de uma aranha pequena, um elevador ou falar em público "
        "dispara o mesmo nível de alarme de um perigo de vida — e você organiza a rotina "
        "inteira para não encontrar esse gatilho.",
        s["body"],
    ))
    story.append(Paragraph(
        "Fobia específica costuma ser <b>circunscrita</b>: há um alvo claro (altura, avião, "
        "agulha, animal, dentista, etc.). Quanto mais claro o alvo, mais fácil montar a escada.",
        s["body"],
    ))
    story.append(Paragraph("Por que “só esperar passar” raramente resolve", s["h2"]))
    story.append(Paragraph(
        "Sem novas experiências de segurança, o cérebro mantém o arquivo antigo: "
        "“isso é perigoso → fuja”. O tempo sozinho não reescreve esse arquivo. "
        "A exposição repetida e processada (com registro) reescreve.",
        s["body"],
    ))
    story.append(Paragraph(
        "“Você não precisa eliminar o medo de uma vez. Precisa ensinar o cérebro, "
        "degrau a degrau, que o alarme estava exagerado.”",
        s["quote"],
    ))
    story.append(PageBreak())

    # ── 2. EXPOSIÇÃO GRADUAL ──
    story.append(Paragraph("2. O que é exposição gradual", s["h1"]))
    story.append(hr())
    story.append(Paragraph(
        "Exposição gradual (também chamada de dessensibilização sistemática / exposição "
        "hierárquica) significa <b>enfrentar o medo em doses pequenas, planejadas e "
        "repetidas</b> — do mais fácil ao mais difícil — até a ansiedade baixar "
        "<i>dentro</i> da situação (habituação) e o cérebro atualizar a previsão de perigo "
        "(aprendizado inibitório).",
        s["body"],
    ))
    story.append(Paragraph("Exemplo clássico (medo de avião)", s["h2"]))
    story.append(bullet_list([
        "Ver fotos de aviões",
        "Assistir a um vídeo de decolagem",
        "Ir ao aeroporto só para observar",
        "Entrar em um avião parado (quando possível) ou simulador",
        "Voo curto com apoio planejado",
    ], s["body_left"]))
    story.append(Paragraph(
        "Cada degrau vencido “encolhe o monstro”. O segredo não é coragem cega — "
        "é <b>consistência + dose certa + reflexão depois</b>.",
        s["body"],
    ))
    story.append(Paragraph("O que este programa NÃO é", s["h2"]))
    story.append(bullet_list([
        "Não é “mergulhar de uma vez” no pior medo (flooding sem preparo).",
        "Não é se torturar até passar mal.",
        "Não é substituir acompanhamento profissional quando você precisa dele.",
    ], s["body_left"]))
    story.append(Paragraph("Exemplos de escadas (inspire-se, depois personalize)", s["h2"]))
    story.append(Paragraph("<b>Aerofobia (medo de voar)</b>", s["h3"]))
    story.append(bullet_list([
        "Ver fotos de cabine → vídeo de decolagem → ir ao aeroporto só para observar → "
        "passar pela segurança sem voar → sentar na área de embarque → voo curto.",
    ], s["body_left"]))
    story.append(Paragraph("<b>Acrofobia (medo de altura)</b>", s["h3"]))
    story.append(bullet_list([
        "Olhar fotos de varandas → vídeo em mirante → ficar perto de janela no 2º andar → "
        "3º andar → mirante com grade → caminhar próximo à borda protegida.",
    ], s["body_left"]))
    story.append(Paragraph("<b>Odontofobia (medo de dentista)</b>", s["h3"]))
    story.append(bullet_list([
        "Ver fotos da clínica → ligar e só marcar horário → visitar a recepção → "
        "sentar na cadeira sem procedimento → profilaxia simples → procedimento planejado.",
    ], s["body_left"]))
    story.append(Paragraph("<b>Glossofobia (medo de falar em público)</b>", s["h3"]))
    story.append(bullet_list([
        "Ler um texto em voz alta sozinho → gravar áudio → falar para 1 pessoa → "
        "para 3 pessoas → reunião curta → apresentação formal.",
    ], s["body_left"]))
    story.append(Paragraph(
        "Se a sua fobia for outra, use a mesma lógica: <b>símbolo → distância → proximidade → contato</b>.",
        s["body"],
    ))
    story.append(PageBreak())

    # ── 3. MONTAR A ESCADA ──
    story.append(Paragraph("3. Sua Escada Segura — como montar", s["h1"]))
    story.append(hr())
    story.append(Paragraph(
        "Antes dos 21 dias, você vai construir sua escada pessoal. "
        "Sem escada clara, a exposição vira improviso — e improviso aumenta o risco "
        "de abandono ou de saltos perigosos demais.",
        s["body"],
    ))
    story.append(Paragraph("Passo A — Defina o medo-alvo", s["h2"]))
    story.append(Paragraph(
        "Escreva com precisão. Em vez de “tenho medo de altura”, prefira: "
        "“medo de ficar perto da janela no 10º andar” ou “medo de subir escadas rolantes”.",
        s["body"],
    ))
    story.append(Paragraph("Minha fobia / medo-alvo:", s["label"]))
    story.append(blank_lines(3))
    story.append(Paragraph("O que eu evito por causa disso:", s["label"]))
    story.append(blank_lines(3))
    story.append(Paragraph("O que eu gostaria de conseguir em 21 dias (meta realista):", s["label"]))
    story.append(blank_lines(3))
    story.append(Paragraph("Passo B — Liste 8 a 12 situações", s["h2"]))
    story.append(Paragraph(
        "Do mais fácil (ansiedade ~2–3) ao mais difícil (ansiedade ~8–9). "
        "Inclua versões com foto, vídeo, observação à distância, aproximação e contato.",
        s["body"],
    ))
    story.append(Spacer(1, 6))
    story.append(ladder_template(s))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "Dica: o primeiro degrau deve ser tão fácil que você quase ache “bobagem”. "
        "Isso cria impulso e confiança.",
        s["small"],
    ))
    story.append(PageBreak())

    # ── 4. ESCALA ──
    story.append(Paragraph("4. Escala de ansiedade (0–10)", s["h1"]))
    story.append(hr())
    story.append(Paragraph(
        "Durante cada exposição, registre três números: <b>antes</b>, <b>pico</b> e "
        "<b>depois</b>. O objetivo não é zerar a ansiedade — é ver que ela sobe e "
        "<b>desce sem você fugir</b>.",
        s["body"],
    ))
    story.append(scale_table(s))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Regra prática: trabalhe preferencialmente nos degraus em que o pico fica "
        "entre <b>3 e 6</b>. Se passar de 7 com frequência, desça um ou dois degraus.",
        s["body"],
    ))
    story.append(PageBreak())

    # ── 5. TÉCNICAS ──
    story.append(Paragraph("5. Técnicas de regulação", s["h1"]))
    story.append(hr())
    story.append(Paragraph(
        "Use estas ferramentas <b>para permanecer</b> na exposição — não para evitar "
        "sentir. Sentir ansiedade (em dose tolerável) faz parte do aprendizado.",
        s["body"],
    ))
    story.append(Paragraph("5.1 Respiração diafragmática (4-6-8)", s["h2"]))
    story.append(bullet_list([
        "Inspire pelo nariz contando até 4 (barriga expandindo).",
        "Segure suavemente até 6 (se confortável; senão, pule a pausa).",
        "Solte pela boca contando até 8.",
        "Repita 4 ciclos. Ombros baixos, mandíbula solta.",
    ], s["body_left"]))
    story.append(Paragraph("5.2 Ancoragem 5-4-3-2-1", s["h2"]))
    story.append(Paragraph(
        "Nomeie: 5 coisas que vê · 4 que toca · 3 que ouve · 2 que cheira · 1 que "
        "pode saborear (ou um sabor na memória). Isso traz o cérebro de volta ao presente.",
        s["body"],
    ))
    story.append(Paragraph("5.3 Frase de enfrentamento", s["h2"]))
    story.append(Paragraph(
        "Escolha uma frase curta e verdadeira. Exemplos: “É ansiedade, não perigo.” · "
        "“Posso sentir e continuar.” · “Já passei por isso antes.”",
        s["body"],
    ))
    story.append(Paragraph("Minha frase de enfrentamento:", s["label"]))
    story.append(blank_lines(2))
    story.append(Paragraph("5.4 Após a exposição — consolidar o aprendizado", s["h2"]))
    story.append(Paragraph(
        "Sempre escreva: o que o medo previa × o que aconteceu de fato. "
        "Esse contraste é o “remédio” cognitivo da exposição.",
        s["body"],
    ))
    story.append(PageBreak())

    # ── 6. REGRAS DE OURO ──
    story.append(Paragraph("6. Regras de ouro do programa", s["h1"]))
    story.append(hr())
    story.append(bullet_list([
        "<b>Pequeno e frequente</b> vence grande e raro.",
        "<b>Não fuja no pico</b> — espere a curva baixar alguns pontos (mesmo que 10–20 minutos).",
        "<b>Repita o mesmo degrau</b> até a ansiedade cair ~50% em relação ao primeiro pico, depois suba.",
        "<b>Evite “muletas mágicas”</b> (álcool, checagens excessivas, só fazer se alguém “garantir” que está seguro) — elas sabotam o aprendizado.",
        "<b>Durma, coma e hidrate</b> — exposição com corpo exausto é mais difícil.",
        "<b>Celebre o processo</b>, não só o degrau final.",
        "<b>Peça ajuda profissional</b> se travar, se o medo for muito amplo (agorafobia/pânico) ou se houver trauma.",
    ], s["body_left"]))
    story.append(Paragraph(
        "Compromisso comigo mesmo(a): vou praticar ____ minutos, ____ dias por semana, "
        "nos próximos 21 dias.",
        s["body"],
    ))
    story.append(blank_lines(2))
    story.append(PageBreak())

    # ── Comportamentos de segurança ──
    story.append(Paragraph("6b. Comportamentos de segurança (e como soltá-los)", s["h1"]))
    story.append(hr())
    story.append(Paragraph(
        "Comportamentos de segurança são atalhos que <b>reduzem a ansiedade na hora</b>, "
        "mas impedem o cérebro de aprender que a situação era tolerável sozinha. "
        "Exemplos: só entrar no elevador com alguém, checar o coração toda hora, "
        "ensaiar mentalmente catástrofes, levar remédio “por precaução” sem indicação, "
        "distrair-se o tempo todo para “não sentir”.",
        s["body"],
    ))
    story.append(Paragraph(
        "Não precisa eliminar tudo no dia 1. O objetivo é <b>reduzir aos poucos</b> "
        "enquanto sobe a escada. Anote os seus:",
        s["body"],
    ))
    story.append(Paragraph("Meus comportamentos de segurança atuais:", s["label"]))
    story.append(blank_lines(4))
    story.append(Paragraph("Quais posso soltar nesta semana (1 ou 2):", s["label"]))
    story.append(blank_lines(3))
    story.append(Paragraph("Erros comuns (e correção)", s["h2"]))
    story.append(bullet_list([
        "<b>Subir degraus demais cedo</b> → volte 1–2 níveis e repita até estabilizar.",
        "<b>Fazer uma vez e parar</b> → o aprendizado pede repetição.",
        "<b>Interpretar ansiedade alta como fracasso</b> → ansiedade é o material de treino.",
        "<b>Comparar-se com outras pessoas</b> → sua escada é sua biografia.",
        "<b>Usar o workbook como único recurso em crise grave</b> → busque ajuda profissional.",
    ], s["body_left"]))
    story.append(PageBreak())

    # ── 7. PLANO 21 DIAS ──
    story.append(Paragraph("7. Plano de 21 dias", s["h1"]))
    story.append(hr())
    story.append(Paragraph(
        "O programa está dividido em três semanas. Ajuste os degraus à <b>sua</b> escada — "
        "os exemplos abaixo são um guia de ritmo, não uma receita rígida.",
        s["body"],
    ))

    # Semana 1
    story.append(Paragraph("Semana 1 — Fundação (dias 1–7)", s["h2"]))
    story.append(Paragraph(
        "Objetivo: psicoeducação aplicada, montar a escada, treinar regulação e "
        "vencer os primeiros degraus fáceis.",
        s["body"],
    ))
    week1 = [
        ("Dia 1 — Mapa do medo",
         "Leia as seções 1–2. Preencha medo-alvo, evitacoes e meta. Escreva 3 situações "
         "em que a fobia limitou sua vida no último mês."),
        ("Dia 2 — Escada rascunho",
         "Liste 10 degraus. Ordene do mais fácil ao mais difícil. Peça a alguém de confiança "
         "(ou a si mesmo com calma) para revisar se algum salto está grande demais."),
        ("Dia 3 — Treino de regulação",
         "Pratique respiração 4-6-8 e 5-4-3-2-1 três vezes no dia, sem exposição. "
         "Anote qual técnica funciona melhor para você."),
        ("Dia 4 — Degrau 1",
         "Exposição curta (5–15 min) no degrau mais fácil. Registre antes/pico/depois. "
         "Permaneça até a ansiedade cair pelo menos 2 pontos."),
        ("Dia 5 — Repetir Degrau 1",
         "Mesma situação. Observe se o pico já é menor. Se sim, prepare o Degrau 2."),
        ("Dia 6 — Degrau 2",
         "Suba um nível. Se o pico passar de 7, volte ao Degrau 1 e fortaleça."),
        ("Dia 7 — Revisão da semana",
         "O que funcionou? O que atrapalhou? Ajuste a escada. Descanse ou faça só "
         "uma exposição leve se estiver cansado(a)."),
    ]
    for title, text in week1:
        story.append(Paragraph(f"<b>{title}</b>", s["h3"]))
        story.append(Paragraph(text, s["body"]))

    story.append(PageBreak())
    story.append(Paragraph("Semana 2 — Consolidação (dias 8–14)", s["h2"]))
    story.append(Paragraph(
        "Objetivo: repetir degraus intermediários até a ansiedade ficar previsível e manejável.",
        s["body"],
    ))
    week2 = [
        ("Dia 8 — Degrau 3", "Exposição com registro completo. Use a frase de enfrentamento."),
        ("Dia 9 — Degrau 3 de novo", "Foque no contraste: previsão do medo × realidade."),
        ("Dia 10 — Degrau 4", "Aumente um pouco a dificuldade (tempo, proximidade ou duração)."),
        ("Dia 11 — Variar o contexto", "Mesmo degrau, outro horário/lugar/roupa/acompanhamento mínimo — generaliza o aprendizado."),
        ("Dia 12 — Degrau 5", "Se necessário, divida este degrau em dois microdegraus."),
        ("Dia 13 — Sessão dupla leve", "Duas exposições curtas no mesmo dia (manhã e fim de tarde), se o corpo aguentar."),
        ("Dia 14 — Revisão", "Liste 5 evidências de que você é capaz de sentir ansiedade e continuar."),
    ]
    for title, text in week2:
        story.append(Paragraph(f"<b>{title}</b>", s["h3"]))
        story.append(Paragraph(text, s["body"]))

    story.append(Paragraph("Semana 3 — Expansão (dias 15–21)", s["h2"]))
    story.append(Paragraph(
        "Objetivo: aproximar-se dos degraus altos com segurança e planejar manutenção.",
        s["body"],
    ))
    week3 = [
        ("Dia 15 — Degrau 6", "Exposição padrão + registro."),
        ("Dia 16 — Degrau 6/7", "Avance só se o pico da sessão anterior tiver caído de forma consistente."),
        ("Dia 17 — Ensaio da meta", "Monte um ensaio próximo da meta de 21 dias (ainda com rede de segurança se precisar)."),
        ("Dia 18 — Degrau alto (dose controlada)", "Tempo limitado, plano claro de saída segura (sair ≠ fugir no pico sem plano)."),
        ("Dia 19 — Integração", "Combine exposição com uma atividade valorizada (encontro, trabalho, lazer)."),
        ("Dia 20 — Ensaio final", "Faça o melhor ensaio possível da meta. Celebre o processo."),
        ("Dia 21 — Plano de manutenção", "Escreva como manter 1–2 exposições por semana nas próximas 4 semanas para não voltar à evitação."),
    ]
    for title, text in week3:
        story.append(Paragraph(f"<b>{title}</b>", s["h3"]))
        story.append(Paragraph(text, s["body"]))
    story.append(PageBreak())

    # ── 8. REGISTROS ──
    story.append(Paragraph("8. Folhas de registro diário", s["h1"]))
    story.append(hr())
    story.append(Paragraph(
        "Use uma folha por dia de exposição. Imprima ou copie à mão. "
        "Quanto mais concreto o registro, mais forte o aprendizado.",
        s["body"],
    ))

    # Generate enough log pages (~14 exposure days worth, 2 per page roughly)
    days_for_logs = [
        "Dia 4 — Registro", "Dia 5 — Registro", "Dia 6 — Registro",
        "Dia 8 — Registro", "Dia 9 — Registro", "Dia 10 — Registro",
        "Dia 11 — Registro", "Dia 12 — Registro", "Dia 13 — Registro",
        "Dia 15 — Registro", "Dia 16 — Registro", "Dia 17 — Registro",
        "Dia 18 — Registro", "Dia 19 — Registro", "Dia 20 — Registro",
        "Registro extra 1", "Registro extra 2", "Registro extra 3",
        "Registro extra 4", "Registro extra 5", "Registro extra 6",
        "Registro extra 7", "Registro extra 8",
    ]
    for i, d in enumerate(days_for_logs):
        story.append(exposure_log(s, d))
        if (i + 1) % 2 == 0 and i < len(days_for_logs) - 1:
            story.append(PageBreak())
    story.append(PageBreak())

    # ── 9. REVISÃO FINAL ──
    story.append(Paragraph("9. Revisão final e próximos passos", s["h1"]))
    story.append(hr())
    story.append(Paragraph("O que eu conquistei em 21 dias:", s["label"]))
    story.append(blank_lines(4))
    story.append(Paragraph("Degraus que ainda quero treinar:", s["label"]))
    story.append(blank_lines(3))
    story.append(Paragraph("Sinais de que estou voltando à evitação:", s["label"]))
    story.append(blank_lines(3))
    story.append(Paragraph("Meu plano de manutenção (próximas 4 semanas):", s["label"]))
    story.append(blank_lines(4))
    story.append(Paragraph(
        "Se quiser aprofundar com acompanhamento profissional — inclusive com "
        "exposição gradual e, quando indicado, recursos de realidade virtual — "
        "fale comigo pelo WhatsApp ou pelo site.",
        s["body"],
    ))
    story.append(Paragraph(
        "WhatsApp: (11) 95069-0537 · www.priscilapalomo.com · CRP 98007",
        s["small"],
    ))
    story.append(PageBreak())

    # ── 10. MODELOS EXTRAS ──
    story.append(Paragraph("10. Modelos extras (imprimíveis)", s["h1"]))
    story.append(hr())
    story.append(Paragraph("Escada em branco (versão 2)", s["h2"]))
    story.append(ladder_template(s))
    story.append(Spacer(1, 14))
    story.append(Paragraph("Checklist rápido antes de cada exposição", s["h2"]))
    story.append(bullet_list([
        "□ Sei qual degrau vou fazer (específico e mensurável)",
        "□ Defini tempo mínimo de permanência (ex.: 10 minutos)",
        "□ Tenho minha frase de enfrentamento",
        "□ Sei como medir ansiedade (0–10) antes / pico / depois",
        "□ Combinei comigo: não abandonar no pico sem plano",
        "□ Depois vou escrever previsão × realidade",
    ], s["body_left"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Registro livre", s["h2"]))
    story.append(exposure_log(s, "Registro livre"))
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceBefore=8, spaceAfter=12))
    story.append(Paragraph(
        "Programa Escada Segura · Material psicoeducativo · Não substitui psicoterapia · "
        "Dra. Priscila Palomo · CRP 98007 · www.priscilapalomo.com",
        s["footer"],
    ))

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"OK: {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
