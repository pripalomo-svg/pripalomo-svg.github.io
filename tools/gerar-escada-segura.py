#!/usr/bin/env python3
"""Gera o book PDF Programa Escada Segura (~200 páginas)."""

from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable, ListFlowable, ListItem,
)

NAVY = HexColor("#14324B")
INK = HexColor("#111111")
MUTED = HexColor("#555555")
LINE = HexColor("#CCCCCC")
PALE = HexColor("#F2F5F8")

OUT = Path(__file__).resolve().parents[1] / "pdfs" / "programa-escada-segura.pdf"


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
        Paragraph("O que o medo previa?", s["label"]), blank_lines(2),
        Paragraph("O que aconteceu de fato?", s["label"]), blank_lines(2),
        Paragraph("Aprendizado de hoje (metáfora do dragão):", s["label"]), blank_lines(2),
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
    story.append(PageBreak())
    story.append(Spacer(1, 4 * cm))
    p(story, part, s["part"])
    p(story, title, s["cover_title"])
    story.append(Spacer(1, 0.5 * cm))
    story.append(HRFlowable(width="40%", thickness=2, color=NAVY, spaceBefore=0, spaceAfter=12))
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
    p(story, "Baseado em DSM-5, Terapia Cognitivo-Comportamental<br/>e o melhor da evidência científica — com metáforas e parábolas japonesas.", s["cover_sub"])
    story.append(Spacer(1, 2.2 * cm))
    p(story, "www.priscilapalomo.com", s["cover_brand"])
    story.append(PageBreak())

    # ═══════════ AVISO ═══════════
    p(story, "Antes de começar — aviso ético", s["h1"])
    story.append(hr())
    p(story, "Este book é um <b>material psicoeducativo</b>. Ele traduz critérios clínicos, "
      "princípios de TCC e evidências científicas para uma linguagem acessível, com "
      "metáforas e histórias que ajudam a memória emocional a acompanhar a memória racional.", s["body"])
    p(story, "<b>Importante:</b> este programa <b>não substitui psicoterapia</b>, avaliação "
      "clínica nem tratamento médico. Se você tem crises de pânico intensas, ideação "
      "suicida, trauma recente sem acompanhamento, transtorno alimentar ativo ou usa "
      "substâncias para enfrentar o medo, procure ajuda profissional antes de iniciar "
      "exposições sozinho(a).", s["body"])
    p(story, "Em qualquer momento, se a ansiedade ficar incontrolável: <b>pare</b>, use as "
      "técnicas de regulação deste material e, se necessário, contate um profissional "
      "de saúde mental ou o CVV (188).", s["body"])
    p(story, "A Dra. Priscila Palomo (CRP 98007) atende online e presencialmente. "
      "WhatsApp: (11) 95069-0537 · www.priscilapalomo.com", s["small"])
    story.append(PageBreak())

    # ═══════════ SUMÁRIO ═══════════
    p(story, "Sumário", s["h1"])
    story.append(hr())
    toc = [
        "Parte I — Psicoeducação: como o medo funciona",
        "Parte II — O que é fobia segundo o DSM-5",
        "Parte III — Sintomas: corpo, mente e comportamento",
        "Parte IV — Quando tratar",
        "Parte V — TCC: passos para vencer o medo",
        "Parte VI — O processo de habituação",
        "Parte VII — Pensadores da fobia (com metáforas)",
        "Parte VIII — Estudos importantes (didáticos e lúdicos)",
        "Parte IX — A coragem de um dragão: analogias japonesas",
        "Parte X — Templos, parábolas e determinação",
        "Parte XI — Sua Escada Segura (montar e treinar)",
        "Parte XII — Plano de 21 dias + registros",
        "Parte XIII — Conclusão: tratamento sério e seguro",
    ]
    for item in toc:
        p(story, item, s["toc"])
    story.append(PageBreak())

    # ═══════════ PARTE I ═══════════
    section_break(story, "PARTE I", "Psicoeducação:\ncomo o medo funciona", s)

    p(story, "1. O alarme que salva — e o alarme que exagera", s["h1"])
    story.append(hr())
    p(story, "Imagine um templo antigo no alto de uma montanha. No pátio há um sino enorme. "
      "Quando um visitante se aproxima demais da beirada do penhasco, o sino toca — "
      "alerta de perigo real. Esse é o <b>medo útil</b>: proteção.", s["body"])
    p(story, "Agora imagine o mesmo sino tocando só porque alguém viu a <i>foto</i> de um "
      "penhasco, ou pensou na palavra “altura”, ou sonhou com escadas. O sino não está "
      "quebrado — ele está <b>calibrado demais</b>. Essa é a lógica da fobia específica: "
      "um sistema de alarme saudável que aprendeu a disparar diante de um gatilho "
      "desproporcional ao risco real.", s["body"])
    p(story, "Você não é fraco(a). Seu cérebro é eficiente demais em lembrar ameaças. "
      "A boa notícia: eficiência também se reensina — degrau a degrau.", s["body"])
    p(story, "“O dragão não some quando gritamos. Ele diminui quando caminhamos em sua direção "
      "com passos pequenos e repetidos.”", s["quote"])

    p(story, "2. O ciclo que mantém a fobia", s["h1"])
    story.append(hr())
    p(story, "Quase toda fobia específica se alimenta do mesmo ciclo:", s["body"])
    story.append(bullets([
        "<b>Gatilho</b> — situação, imagem, pensamento, sensação ou lembrança.",
        "<b>Alarme</b> — ansiedade sobe (coração, respiração, tremor, vontade de fugir).",
        "<b>Evitação ou “muleta”</b> — fugir, adiar, checar, só fazer com alguém, usar álcool “para coragem”.",
        "<b>Alívio imediato</b> — a ansiedade cai… e o cérebro grava: “fugir funcionou”.",
        "<b>Medo maior amanhã</b> — o monstro cresce porque nunca foi testado de verdade.",
    ], s["body_left"]))
    p(story, "Quebrar o ciclo não exige heroísmo. Exige <b>método</b>: exposição gradual, "
      "permanência, registro e repetição. É a escada do templo — não o salto do penhasco.", s["body"])
    story.append(PageBreak())

    p(story, "3. Medo, ansiedade e fobia — três irmãos diferentes", s["h1"])
    story.append(hr())
    p(story, "<b>Medo</b> é resposta a uma ameaça presente e concreta. "
      "<b>Ansiedade</b> é antecipação de ameaça futura. "
      "<b>Fobia específica</b> é medo intenso e persistente de um objeto ou situação "
      "circunscrita, desproporcional, que gera evitação e sofrimento ou prejuízo.", s["body"])
    p(story, "Metáfora do jardim zen: o medo é a pedra que você vê no caminho. "
      "A ansiedade é imaginar pedras em todas as curvas seguintes. "
      "A fobia é desviar o caminho inteiro da vida só para não passar perto de uma "
      "pedra específica — mesmo quando ela já está marcada e segura.", s["body"])
    p(story, "4. Por que “só esperar passar” raramente resolve", s["h2"])
    p(story, "Sem novas experiências de segurança, o cérebro mantém o arquivo antigo: "
      "“isso é perigoso → fuja”. O tempo sozinho não reescreve esse arquivo. "
      "A exposição repetida e processada (com registro) reescreve.", s["body"])
    p(story, "Como no treino de um arqueiro no templo: não se fica bom olhando o alvo "
      "de longe por anos. Melhora-se atirando — primeiro perto, depois um pouco mais longe.", s["body"])
    story.append(PageBreak())

    p(story, "5. O corpo na fobia: o que acontece por dentro", s["h1"])
    story.append(hr())
    p(story, "Quando o alarme dispara, o sistema nervoso simpático acelera:", s["body"])
    story.append(bullets([
        "Coração acelerado, palpitações, pressão que sobe.",
        "Respiração curta ou sensação de falta de ar.",
        "Suor, tremor, formigamento, náusea, tontura.",
        "Tensão muscular, vontade de fugir ou “travar”.",
        "Em alguns casos: despersonalização leve (sentir-se “fora” do corpo).",
    ], s["body_left"]))
    p(story, "Essas sensações são <b>desconfortáveis</b>, não necessariamente perigosas. "
      "Elas são o corpo se preparando para luta/fuga — como um dragão que infla o peito "
      "antes de voar. Na exposição segura, você ensina o dragão a pousar sem incendiar a aldeia.", s["body"])
    story.append(callout(
        "Lembrete do templo",
        "Sentir ansiedade na exposição não é fracasso. É o material de treino. "
        "O objetivo não é zerar a sensação no primeiro dia — é permanecer até ela baixar "
        "e descobrir que a catástrofe prevista não veio.",
        s,
    ))
    story.append(PageBreak())

    # ═══════════ PARTE II DSM-5 ═══════════
    section_break(story, "PARTE II", "O que é fobia\nsegundo o DSM-5", s)

    p(story, "6. Critérios essenciais (DSM-5) — em linguagem clara", s["h1"])
    story.append(hr())
    p(story, "O Manual Diagnóstico e Estatístico de Transtornos Mentais (DSM-5), da "
      "American Psychiatric Association, descreve a <b>Fobia Específica</b> "
      "(Specific Phobia) aproximadamente assim:", s["body"])
    story.append(bullets([
        "<b>Medo ou ansiedade acentuados</b> diante de um objeto ou situação específicos "
        "(voar, alturas, animais, injeção, sangue, etc.).",
        "O objeto/situação <b>quase sempre</b> provoca medo ou ansiedade imediatos.",
        "Há <b>evitação ativa</b> ou enfrentamento com intenso sofrimento.",
        "O medo é <b>desproporcional</b> ao perigo real e ao contexto sociocultural.",
        "É <b>persistente</b> — tipicamente 6 meses ou mais.",
        "Causa <b>sofrimento clinicamente significativo</b> ou prejuízo em áreas da vida "
        "(trabalho, estudos, relacionamentos, cuidados de saúde).",
        "Não é melhor explicado por outro transtorno (pânico com agorafobia, TOC, TEPT, etc.).",
    ], s["body_left"]))
    p(story, "Metáfora: o DSM-5 não é uma “sentença”. É um mapa compartilhado entre "
      "profissionais — como a planta de um templo: ajuda a saber onde estamos e qual "
      "caminho de tratamento costuma funcionar melhor.", s["body"])
    story.append(PageBreak())

    p(story, "7. Especificadores — os “corredores” da fobia", s["h1"])
    story.append(hr())
    p(story, "O DSM-5 organiza fobias específicas em tipos comuns (especificadores):", s["body"])
    story.append(bullets([
        "<b>Animal</b> — cães, aranhas, insetos, pássaros, etc.",
        "<b>Ambiente natural</b> — alturas, tempestades, água, escuro.",
        "<b>Sangue-injeção-ferimentos</b> — agulhas, sangue, procedimentos médicos "
        "(pode incluir resposta vasovagal / desmaio).",
        "<b>Situacional</b> — aviões, elevadores, espaços fechados, dirigir.",
        "<b>Outros</b> — engasgar, vomitar, personagens fantasiados, etc.",
    ], s["body_left"]))
    p(story, "Também se indica se a fobia está presente em múltiplas situações. "
      "Quanto mais claro o “corredor” do templo em que você se perde, mais precisa "
      "fica a escada de exposição.", s["body"])

    p(story, "8. Fobia específica × outros quadros", s["h2"])
    p(story, "<b>Agorafobia</b> envolve medo de lugares de onde seria difícil escapar ou "
      "receber ajuda (multidões, transportes, espaços abertos) — não é só “medo de rua”. "
      "<b>Transtorno de pânico</b> centra-se em ataques de pânico recorrentes e medo "
      "dos próprios sintomas. <b>Ansiedade social</b> foca em avaliação negativa por outras "
      "pessoas. Podem coexistir — por isso avaliação profissional importa.", s["body"])
    story.append(PageBreak())

    p(story, "9. Prevalência e curso — o que a ciência observa", s["h1"])
    story.append(hr())
    p(story, "Fobias específicas estão entre os transtornos de ansiedade mais comuns. "
      "Muitas começam na infância ou adolescência; algumas surgem após um evento "
      "assustador (ou após ver alguém sofrer — aprendizado vicário). Sem tratamento, "
      "podem persistir por anos, “encolhendo” a vida em silêncio: não viajar, não ir ao "
      "dentista, não aceitar promoção que exige voar, evitar hospitais.", s["body"])
    p(story, "A boa notícia clínica: fobias específicas estão entre os quadros com "
      "<b>melhor resposta</b> a intervenções baseadas em exposição. Como um portão "
      "emperrado no templo: parece impossível — até lubrificar e abrir um pouco por dia.", s["body"])
    story.append(callout(
        "Nota didática",
        "Diagnóstico é ato clínico. Este book educa; não “fecha diagnóstico” pela internet. "
        "Use o texto para se reconhecer e buscar ajuda adequada.",
        s,
    ))
    story.append(PageBreak())

    # ═══════════ PARTE III SINTOMAS ═══════════
    section_break(story, "PARTE III", "Todos os sintomas:\ncorpo, mente e ação", s)

    p(story, "10. Sintomas físicos (o corpo em alarme)", s["h1"])
    story.append(hr())
    story.append(bullets([
        "Taquicardia, palpitações, sensação de aperto no peito.",
        "Falta de ar, hiperventilação, suspiros frequentes.",
        "Tremor, sudorese, mãos frias ou quentes.",
        "Tontura, visão turva, sensação de desmaio (especialmente em fobia de sangue/agulha).",
        "Náusea, “nó” no estômago, vontade de ir ao banheiro.",
        "Tensão no pescoço, ombros e mandíbula; dor de cabeça tensional.",
        "Boca seca, dificuldade de engolir, sensação de “bola na garganta”.",
        "Formigamentos (parestesias) em mãos, pés ou rosto.",
        "Sensação de irrealidade (desrealização) ou de estar fora de si (despersonalização).",
    ], s["body_left"]))
    p(story, "Metáfora: o corpo acende todas as lanternas do corredor do templo ao mesmo tempo. "
      "Na exposição, você aprende a caminhar com algumas lanternas acesas — sem precisar "
      "apagar todas para dar o próximo passo.", s["body"])
    story.append(PageBreak())

    p(story, "11. Sintomas cognitivos (a mente em previsão de catástrofe)", s["h1"])
    story.append(hr())
    story.append(bullets([
        "Pensamentos do tipo “vou morrer / enlouquecer / desmaiar / perder o controle”.",
        "Superestimação de probabilidade de dano (“se eu voar, o avião cai”).",
        "Subestimação da própria capacidade de lidar (“não vou aguentar nem 10 segundos”).",
        "Atenção hiperfocada no gatilho e nas sensações internas (hipervigilância).",
        "Imagens mentais catastróficas (filmes internos de horror).",
        "Lembranças intrusivas de experiências ruins relacionadas ao medo.",
        "Crenças fundadoras: “o mundo é perigoso”, “eu sou frágil”, “preciso de certeza total”.",
    ], s["body_left"]))
    p(story, "Na TCC, esses pensamentos não são tratados como “verdades absolutas”, "
      "mas como <b>hipóteses</b> a serem testadas na vida real — com a escada.", s["body"])

    p(story, "12. Sintomas emocionais e comportamentais", s["h2"])
    story.append(bullets([
        "Medo intenso, pavor, pânico situacional.",
        "Vergonha (“isso é ridículo, eu deveria controlar”).",
        "Raiva de si, frustração, tristeza por oportunidades perdidas.",
        "Evitação óbvia (não ir) e sutil (só ir com alguém, remédio “por precaução”, distração total).",
        "Busca de segurança (checagens, pesquisas infinitas na internet, rituais).",
        "Adiamento de cuidados de saúde, viagens, carreira, relacionamentos.",
    ], s["body_left"]))
    story.append(PageBreak())

    p(story, "13. Checklist de autobservação (não é diagnóstico)", s["h1"])
    story.append(hr())
    p(story, "Marque o que costuma acontecer com você diante do gatilho:", s["body"])
    checks = [
        "□ Medo imediato e intenso",
        "□ Evito a situação sempre que posso",
        "□ Se enfrento, sofro muito",
        "□ Sei que o medo é exagerado, mas não consigo “desligar”",
        "□ Isso atrapalha trabalho / estudos / saúde / lazer",
        "□ Dura há meses (ou anos)",
        "□ Já perdi oportunidades por causa disso",
        "□ Uso “muletas” (pessoa, álcool, checagem, escape garantido)",
        "□ Sintomas físicos fortes (coração, ar, tremor, náusea)",
        "□ Pensamentos catastróficos difíceis de questionar na hora",
    ]
    for c in checks:
        p(story, c, s["body_left"])
    story.append(Spacer(1, 8))
    p(story, "Minhas três situações mais evitadas hoje:", s["label"])
    story.append(blank_lines(4))
    p(story, "O que eu mais gostaria de voltar a fazer:", s["label"])
    story.append(blank_lines(3))
    story.append(PageBreak())

    # ═══════════ PARTE IV QUANDO TRATAR ═══════════
    section_break(story, "PARTE IV", "Quando tratar", s)

    p(story, "14. Sinais de que é hora de cuidar", s["h1"])
    story.append(hr())
    p(story, "Tratar não é “fraqueza”. É manutenção do templo. Considere buscar tratamento quando:", s["body"])
    story.append(bullets([
        "A evitação já muda rotina, carreira, saúde ou vínculos.",
        "Você sofre antecipando o gatilho dias antes.",
        "Há ataques de pânico ligados à situação.",
        "Você evita exames, dentista, aviões, elevadores ou locais necessários.",
        "O medo se espalhou (começou em um gatilho e agora há vários).",
        "Você usa substâncias ou comportamentos de risco para “aguentar”.",
        "Crianças/adolescentes: o medo impede escola, socialização ou desenvolvimento.",
    ], s["body_left"]))
    p(story, "Metáfora japonesa: não se espera o telhado cair para consertar uma telha. "
      "Quanto mais cedo a escada de exposição começa, menos o musgo da evitação cobre os degraus.", s["body"])

    p(story, "15. Quando priorizar acompanhamento profissional presencial/online", s["h2"])
    story.append(bullets([
        "Ideação suicida, autolesão, desespero intenso.",
        "Trauma recente ou TEPT associado.",
        "Fobia de sangue/agulha com desmaios frequentes (treino específico de tensão aplicada).",
        "Uso problemático de álcool/benzodiazepínicos para enfrentar.",
        "Múltiplos transtornos (depressão grave, TOC, bipolaridade) sem estabilidade.",
        "Crianças muito pequenas — o plano deve ser adaptado com responsáveis.",
    ], s["body_left"]))
    p(story, "Este book pode caminhar <b>junto</b> da terapia — como um caderno de treino "
      "entre sessões — não no lugar dela quando o caso é complexo.", s["body"])
    story.append(PageBreak())

    p(story, "16. Metas realistas de tratamento", s["h1"])
    story.append(hr())
    p(story, "Tratamento sério não promete “zero medo para sempre”. Promete algo mais "
      "valioso: <b>liberdade funcional</b> — fazer o que importa mesmo com algum desconforto, "
      "e ver esse desconforto encolher com a prática.", s["body"])
    p(story, "Como o dragão que ainda existe nos contos, mas deixa de governar a aldeia.", s["body"])
    p(story, "Minha meta de 21 dias (específica e observável):", s["label"])
    story.append(blank_lines(3))
    p(story, "Minha meta de 3 meses:", s["label"])
    story.append(blank_lines(3))
    story.append(PageBreak())

    # ═══════════ PARTE V TCC ═══════════
    section_break(story, "PARTE V", "TCC: passos para\nvencer o medo", s)

    p(story, "17. O mapa da Terapia Cognitivo-Comportamental", s["h1"])
    story.append(hr())
    p(story, "Na TCC para fobias específicas, o coração do tratamento é a "
      "<b>exposição</b> (gradual ou, em alguns protocolos, mais intensiva), "
      "combinada com <b>psicoeducação</b>, <b>reestruturação cognitiva</b> leve "
      "e redução de comportamentos de segurança.", s["body"])
    p(story, "Pense em sete portões do templo. Você não precisa arrombá-los todos no mesmo dia.", s["body"])

    steps = [
        ("Passo 1 — Psicoeducação",
         "Entender o ciclo medo → evitação → alívio → medo maior. Sem culpa. Com ciência."),
        ("Passo 2 — Definir o medo-alvo",
         "Especificar: não “tenho medo de tudo”, e sim “medo de ficar na janela do 10º andar”."),
        ("Passo 3 — Montar a hierarquia (escada)",
         "Listar 8–12 situações do mais fácil ao mais difícil, com notas de ansiedade 0–10."),
        ("Passo 4 — Técnicas de regulação",
         "Respiração, ancoragem, frase de enfrentamento — para permanecer, não para evitar sentir."),
        ("Passo 5 — Exposição repetida",
         "Enfrentar o degrau, permanecer até a ansiedade baixar, repetir até estabilizar, subir."),
        ("Passo 6 — Processar o aprendizado",
         "Escrever: o que o medo previa × o que aconteceu. Esse contraste reescreve a previsão."),
        ("Passo 7 — Manutenção e prevenção de recaída",
         "Continuar microexposições; reconhecer retorno da evitação; retomar a escada cedo."),
    ]
    for title, text in steps:
        p(story, f"<b>{title}</b>", s["h3"])
        p(story, text, s["body"])
    story.append(PageBreak())

    p(story, "18. Exposição: o que é e o que não é", s["h1"])
    story.append(hr())
    p(story, "<b>É:</b> contato planejado, repetido e seguro com o gatilho, em dose "
      "tolerável, até o cérebro atualizar a previsão de perigo.", s["body"])
    p(story, "<b>Não é:</b> se torturar; se jogar no pior medo sem preparo; usar o "
      "sofrimento como prova de valor; substituir avaliação médica/psicológica.", s["body"])
    p(story, "Metáfora do dragão: exposição não é matar o dragão com uma espada no primeiro "
      "encontro. É aproximar-se o suficiente, dia após dia, até perceber que ele cospe "
      "mais fumaça do que fogo — e que você consegue atravessar a ponte mesmo assim.", s["body"])

    p(story, "19. Comportamentos de segurança (as “amuletos” que sabotam)", s["h2"])
    p(story, "Amuletos parecem ajudar: só entrar no elevador com alguém; checar o coração; "
      "ensaiar catástrofes; levar remédio sem indicação; distrair-se o tempo todo. "
      "Eles reduzem ansiedade na hora — e impedem o aprendizado de que a situação era "
      "tolerável sozinha. Na escada, vamos soltando amuletos aos poucos.", s["body"])
    p(story, "Meus amuletos atuais:", s["label"])
    story.append(blank_lines(4))
    story.append(PageBreak())

    p(story, "20. Reestruturação cognitiva sem guerra interna", s["h1"])
    story.append(hr())
    p(story, "Não se trata de gritar “cala a boca, ansiedade”. Trata-se de perguntar:", s["body"])
    story.append(bullets([
        "Qual é a evidência real de que a catástrofe vai acontecer?",
        "Já enfrentei algo parecido? O que ocorreu de fato?",
        "Estou confundindo sensação ruim com perigo real?",
        "O que eu diria a alguém que amo nessa mesma situação?",
        "Qual é um pensamento mais equilibrado — não positivo falso, equilibrado?",
    ], s["body_left"]))
    p(story, "No templo, o monge não quebra o sino. Ele aprende quando o toque é alerta "
      "útil e quando é eco antigo.", s["body"])
    story.append(PageBreak())

    # ═══════════ PARTE VI HABITUAÇÃO ═══════════
    section_break(story, "PARTE VI", "O processo\nde habituação", s)

    p(story, "21. Habituação: o sino que cansa de tocar sozinho", s["h1"])
    story.append(hr())
    p(story, "<b>Habituação</b> é a diminuição natural da resposta de ansiedade quando você "
      "permanece diante do estímulo, sem fugir, por tempo suficiente e com repetição. "
      "O alarme sobe… e depois desce — mesmo sem a “fuga salvadora”.", s["body"])
    p(story, "Metáfora: um visitante toca o sino do templo toda vez que entra. No primeiro "
      "dia, todos se assustam. No décimo dia, o corpo já não salta igual. Não porque o "
      "sino mudou — porque o sistema nervoso aprendeu: “isso não exige fuga”.", s["body"])

    p(story, "22. Habituação × aprendizado inibitório (visão moderna)", s["h2"])
    p(story, "Modelos clássicos falavam sobretudo em habituação. Pesquisas mais recentes "
      "(como as linhas de trabalho de Craske e colaboradores) enfatizam também o "
      "<b>aprendizado inibitório</b>: criar novas associações de segurança que competem "
      "com a associação antiga de medo. Por isso registramos o contraste "
      "“previsão do medo × realidade”.", s["body"])
    p(story, "Em linguagem de parábola: não apagamos o pergaminho antigo do dragão. "
      "Escrevemos um pergaminho novo ao lado — e o lemos tantas vezes que ele passa a "
      "guiar a aldeia.", s["body"])
    story.append(PageBreak())

    p(story, "23. Condições que favorecem a habituação", s["h1"])
    story.append(hr())
    story.append(bullets([
        "<b>Dose certa</b> — ansiedade geralmente entre 3 e 6 no pico (não 0, não 10 constante).",
        "<b>Permanência</b> — não sair no auge sem plano; esperar a curva baixar alguns pontos.",
        "<b>Repetição</b> — uma vez não basta; o cérebro ama séries.",
        "<b>Variedade</b> — depois de dominar, variar contexto (hora, lugar, companhia mínima).",
        "<b>Menos amuletos</b> — reduzir comportamentos de segurança progressivamente.",
        "<b>Processamento</b> — escrever o aprendizado depois.",
        "<b>Sono, comida, hidratação</b> — corpo exausto habitua pior.",
    ], s["body_left"]))
    p(story, "24. Por que a ansiedade sobe no começo da exposição", s["h2"])
    p(story, "Porque o alarme ainda acredita no arquivo antigo. Subir não significa que "
      "você está piorando — significa que o treino começou. Como o dragão que rosna "
      "mais alto quando alguém se aproxima da caverna pela primeira vez em anos.", s["body"])
    story.append(PageBreak())

    p(story, "25. Curva típica de uma sessão de exposição", s["h1"])
    story.append(hr())
    p(story, "1) Antes: ansiedade antecipatória. 2) Contato: sobe para o pico. "
      "3) Permanência: oscila e começa a descer. 4) Depois: alívio + aprendizado. "
      "5) Nas repetições: o pico tende a ficar menor e cair mais rápido.", s["body"])
    p(story, "Desenhe de memória a última vez que enfrentou algo difícil:", s["label"])
    story.append(blank_lines(2))
    p(story, "Ansiedade no início: ____  no pico: ____  no fim: ____", s["field"])
    story.append(Spacer(1, 8))
    story.append(callout(
        "Regra de ouro da habituação",
        "Pequeno e frequente vence grande e raro. A escada do templo é sobe-se com os pés, "
        "não com um discurso motivacional no térreo.",
        s,
    ))
    story.append(PageBreak())

    # ═══════════ PARTE VII PENSADORES ═══════════
    section_break(story, "PARTE VII", "Pensadores da fobia\n(com metáforas)", s)

    thinkers = [
        ("Ivan Pavlov",
         "Mostrou condicionamento clássico: um estímulo neutro pode se ligar a uma resposta "
         "automática. Metáfora: o sino do templo que, após muitos jantares, faz a boca "
         "salivar só de tocar — mesmo sem comida. Na fobia, um elevador “neutro” vira sino de alarme."),
        ("John B. Watson (e o caso do Pequeno Albert — historicamente controverso)",
         "Demonstrou que medos podem ser aprendidos por associação. Metáfora didática "
         "(sem endossar ética da época): se um tambor assusta sempre que um animal aparece, "
         "a criança pode passar a temer o animal. Lição moderna: medos se aprendem — e, "
         "portanto, podem ser reaprendidos com cuidado ético."),
        ("Mary Cover Jones",
         "Pioneira em “descondicionar” medos infantis com aproximação gradual e "
         "acompanhamento positivo. Metáfora: aproximar a criança do coelho temido "
         "enquanto há lanche e segurança — degrau a degrau. Ancestral da exposição gradual."),
        ("Joseph Wolpe",
         "Sistematizou a dessensibilização sistemática: relaxamento + hierarquia + "
         "aproximação imaginária/real. Metáfora: ensinar o corpo a ficar em “modo templo” "
         "(calma) enquanto sobe a escada do medo."),
        ("Aaron T. Beck",
         "Fundamentos da terapia cognitiva: pensamentos influenciam emoções e comportamentos. "
         "Metáfora: as lanternas que você aponta determinam o que o corredor parece ser. "
         "Na fobia, lanternas catastróficas fazem um degrau parecer um abismo."),
        ("Albert Bandura",
         "Autoeficácia e aprendizado vicário: ver alguém enfrentar com sucesso ajuda; "
         "acreditar “eu posso, com treino” muda a persistência. Metáfora: o aprendiz que "
         "vê o mestre atravessar a ponte estreita ganha mapa interno de possibilidade."),
        ("Isaac Marks",
         "Fortaleceu a exposição como tratamento central de fobias. Metáfora: menos teoria "
         "no pátio, mais caminhada no corredor temido — com método."),
        ("Stanley Rachman",
         "Três caminhos do medo: condicionamento direto, aprendizado vicário e transmissão "
         "de informação (“isso é perigoso”). Metáfora: o dragão chega por três portas — "
         "ferida própria, ver a ferida de outro, ou ouvir lendas assustadoras."),
        ("David Barlow",
         "Modelos de ansiedade e tratamento baseado em evidência; importância de enfrentar "
         "sensações internas (interoceptivas) em alguns quadros. Metáfora: às vezes o "
         "templo assusta não pelo corredor, mas pelos ecos do próprio coração."),
        ("Lars-Göran Öst",
         "Protocolos eficientes, inclusive tratamentos de sessão única em algumas fobias "
         "específicas, com preparação cuidadosa. Metáfora: há dias em que se sobe muitos "
         "degraus com um mestre — mas a escada ainda precisa existir."),
        ("Michelle Craske",
         "Ênfase em aprendizado inibitório, violação de expectativa e variabilidade na "
         "exposição. Metáfora: não basta o sino cansar; é preciso escrever um novo sutra "
         "de segurança e lê-lo em vários salões do templo."),
        ("Edna Foa (exposição em transtornos relacionados)",
         "Contribuições amplas à terapia de exposição (incl. TEPT/TOC). Lição transferível: "
         "evitar mantém; processar e permanecer transforma. Metáfora: a porta trancada "
         "parece proteção — e vira prisão."),
    ]

    p(story, "26. Galeria didática dos pensadores", s["h1"])
    story.append(hr())
    p(story, "Abaixo, um resumo lúdico — não é biografia completa, é mapa de ideias "
      "úteis para quem sobe a Escada Segura.", s["body"])

    for i, (name, text) in enumerate(thinkers):
        p(story, f"<b>{name}</b>", s["h3"])
        p(story, text, s["body"])
        if (i + 1) % 3 == 0:
            story.append(PageBreak())
    if len(thinkers) % 3 != 0:
        story.append(PageBreak())

    p(story, "27. O que unir desses pensadores na prática", s["h1"])
    story.append(hr())
    story.append(bullets([
        "Medos se aprendem (associação, modelo, informação).",
        "Medos se desaprendem/reaprendem com exposição estruturada.",
        "Pensamentos catastróficos alimentam o alarme — e podem ser testados.",
        "Autoeficácia cresce com microvitórias repetidas.",
        "O aprendizado novo precisa ser claro: “eu previ X; aconteceu Y”.",
    ], s["body_left"]))
    p(story, "“No templo da mente, cada mestre deixou um degrau. Sua tarefa não é "
      "decorar os nomes — é subir.”", s["quote"])
    story.append(PageBreak())

    # ═══════════ PARTE VIII ESTUDOS ═══════════
    section_break(story, "PARTE VIII", "Estudos importantes\n(didáticos e lúdicos)", s)

    studies = [
        ("Estudo-metáfora 1 — O sino que aprende (condicionamento)",
         "Linha pavloviana / watsoniana (em versão ética moderna): estímulos podem "
         "ganhar poder de alarme. Lição lúdica: se toda vez que o gongo soa cai uma "
         "tempestade no conto, o corpo treme só com o gongo. Tratamento = novos "
         "encontros em que o gongo soa e a tempestade não vem."),
        ("Estudo-metáfora 2 — Mary Cover Jones e o coelho do corredor",
         "Aproximação gradual com segurança. Lição: medo infantil pode encolher quando "
         "a criança se aproxima em doses, com apoio. É a bisavó da sua escada."),
        ("Estudo-metáfora 3 — Wolpe e a escada com respiração",
         "Dessensibilização sistemática. Lição: hierarquia + calma relativa + passos. "
         "Como subir degraus carregando uma lanterna estável."),
        ("Estudo-metáfora 4 — Exposição ao vivo funciona",
         "Décadas de ensaios clínicos em fobias específicas mostram altas taxas de "
         "melhora com exposição in vivo. Lição lúdica: ler sobre natação ajuda; "
         "entrar na água rasa, repetidas vezes, ensina o corpo."),
        ("Estudo-metáfora 5 — Sessão única (Öst e linha relacionada)",
         "Em algumas fobias, protocolos intensivos bem conduzidos produzem ganhos "
         "rápidos. Lição: às vezes um dia longo no templo muda o mapa — desde que "
         "haja preparação, ética e acompanhamento."),
        ("Estudo-metáfora 6 — Realidade virtual como corredor seguro",
         "Pesquisas em RV para fobias (altura, voar, etc.) mostram que ambientes "
         "simulados podem servir de degraus intermediários. Lição: treinar na "
         "“maquete do templo” antes do templo real."),
        ("Estudo-metáfora 7 — Violação de expectativa (Craske et al.)",
         "Exposições que claramente desmentem a previsão catastrófica geram "
         "aprendizado mais forte. Lição: anote a profecia do medo antes; compare "
         "depois. O dragão odeia planilhas — e é por isso que usamos planilhas."),
        ("Estudo-metáfora 8 — Variabilidade ajuda a generalizar",
         "Treinar só num contexto pode deixar o medo “à espreita” em outro. Lição: "
         "depois do degrau estável, varie hora, lugar, companhia. Como visitar "
         "vários salões do mesmo templo."),
        ("Estudo-metáfora 9 — Comportamentos de segurança atrapalham",
         "Amuletos podem impedir o aprendizado de segurança. Lição: solte um amuleto "
         "por semana, não todos de uma vez se isso te arremessar do telhado."),
        ("Estudo-metáfora 10 — Fobia de sangue-injeção e tensão aplicada",
         "Protocolos específicos (applied tension) ajudam quando há desmaio vasovagal. "
         "Lição: há técnicas certas para dragões diferentes. Nem todo dragão se "
         "treina só com respiração lenta."),
        ("Estudo-metáfora 11 — Evitação mantém; aproximação transforma",
         "Consenso amplo da literatura de ansiedade. Lição de parábola: a ponte "
         "parece mais estreita cada ano que você não a cruza — não porque ela "
         "estreitou, mas porque sua memória de atravessar envelheceu."),
        ("Estudo-metáfora 12 — Autoeficácia prediz persistência",
         "Bandura e derivados: crer “eu posso com treino” aumenta adesão. Lição: "
         "celebre microvitórias. O dragão respeita quem volta amanhã."),
        ("Estudo-metáfora 13 — Modelagem (ver alguém enfrentar)",
         "Observar modelos competentes reduz medo. Lição: às vezes o primeiro degrau "
         "é assistir outra pessoa (ou um vídeo) fazer o que você teme."),
        ("Estudo-metáfora 14 — Recaída e retorno da evitação",
         "Melhora não é linha reta. Lição: se a evitação voltar, você não “zerou” — "
         "você encontrou musgo nos degraus. Escove cedo."),
        ("Estudo-metáfora 15 — Combinar psicoeducação + exposição",
         "Entender o “porquê” aumenta engajamento. Lição: mapa + caminhada. "
         "Templo sem planta confunde; planta sem caminhada não chega ao altar."),
    ]

    p(story, "28. Biblioteca lúdica de evidências", s["h1"])
    story.append(hr())
    p(story, "Em vez de citar apenas números frios, traduzimos achados em histórias de "
      "templo e dragão — fiéis à ideia científica, acessíveis à memória emocional.", s["body"])

    for i, (title, text) in enumerate(studies):
        p(story, f"<b>{title}</b>", s["h3"])
        p(story, text, s["body"])
        if (i + 1) % 3 == 0:
            story.append(PageBreak())
    if len(studies) % 3 != 0:
        story.append(PageBreak())

    p(story, "29. O que a ciência NÃO diz", s["h1"])
    story.append(hr())
    story.append(bullets([
        "Não diz que “é só ter força de vontade”.",
        "Não diz que metáforas substituem protocolo.",
        "Não diz que todo mundo melhora no mesmo ritmo.",
        "Não diz que material psicoeducativo sozinho resolve casos graves.",
        "Não diz que medo zero é obrigatório para uma vida boa.",
    ], s["body_left"]))
    story.append(PageBreak())

    # ═══════════ PARTE IX DRAGÃO ═══════════
    section_break(story, "PARTE IX", "A coragem de um dragão:\nanalogias japonesas", s)

    p(story, "30. O que é a coragem de um dragão", s["h1"])
    story.append(hr())
    p(story, "No imaginário japonês e do Leste Asiático, o dragão (龍 / ryū) muitas vezes "
      "não é só monstro: é força da natureza, guardião, sabedoria das águas e dos céus. "
      "A <b>coragem de um dragão</b>, neste book, não é agressividade. É "
      "<b>presença poderosa sem fuga descontrolada</b> — avançar com dignidade, mesmo "
      "com o peito ruidoso.", s["body"])
    p(story, "Sua exposição gradual é isso: o dragão que aprende a voar em círculos "
      "pequenos antes da travessia longa.", s["body"])

    p(story, "31. Analogia do katana e do polimento", s["h2"])
    p(story, "Uma lâmina não nasce afiada no primeiro golpe na pedra. O polimento "
      "(como nas tradições de espadas) é repetição paciente. Cada sessão de exposição "
      "é uma passada na pedra: parece mínima — e muda o fio.", s["body"])

    p(story, "32. Analogia do bambu na tempestade", s["h2"])
    p(story, "O bambu verga e não parte. Na ansiedade alta, vergar (usar respiração, "
      "abaixar um degrau) não é covardia: é inteligência estrutural. Partir seria "
      "fugir sem plano e abandonar o treino.", s["body"])
    story.append(PageBreak())

    p(story, "33. Analogia do torii (portal do santuário)", s["h1"])
    story.append(hr())
    p(story, "O torii marca a passagem do cotidiano ao espaço sagrado. Cada degrau da "
      "sua escada é um torii: ao atravessar, você declara — com o corpo — que aquele "
      "território não pertence mais só ao medo.", s["body"])
    p(story, "Não é preciso atravessar o torii mais alto no primeiro dia. Há portais "
      "menores no caminho da montanha.", s["body"])

    p(story, "34. Analogia do chá (chanoyu) e a atenção", s["h2"])
    p(story, "Na cerimônia do chá, gestos simples ganham presença total. Na exposição, "
      "a âncora 5-4-3-2-1 e a respiração são sua “cerimônia”: trazem a mente de volta "
      "ao agora, onde o perigo imaginado raramente está tão completo quanto o filme interno.", s["body"])

    p(story, "35. Analogia do kintsugi (quebra e ouro)", s["h2"])
    p(story, "Kintsugi repara a cerâmica com veios de ouro: a fratura vira parte da "
      "história, não vergonha escondida. Seus “fracassos” de exposição — dias difíceis, "
      "retornos da evitação — podem ser filetes de ouro se você registrar o que aprendeu "
      "e voltar à escada.", s["body"])
    p(story, "“A coragem de um dragão não é nunca tremer. É tremer e ainda assim "
      "guardar o pergaminho novo de segurança.”", s["quote"])
    story.append(PageBreak())

    p(story, "36. Diário do dragão — exercício", s["h1"])
    story.append(hr())
    p(story, "Hoje, meu dragão interior estava:", s["label"])
    story.append(blank_lines(2))
    p(story, "Ele cospia fogo (catástrofe) ou fumaça (desconforto)?", s["label"])
    story.append(blank_lines(2))
    p(story, "Qual microvoo (degrau) eu fiz?", s["label"])
    story.append(blank_lines(2))
    p(story, "Que pergaminho novo escrevi? (previsão × realidade)", s["label"])
    story.append(blank_lines(3))
    story.append(PageBreak())

    # ═══════════ PARTE X TEMPLOS ═══════════
    section_break(story, "PARTE X", "Templos, parábolas\ne determinação", s)

    parables = [
        ("Parábola do templo na névoa",
         "Um viajante precisava chegar ao templo no alto. A névoa era tão espessa que "
         "ele só via o próximo degrau de pedra. Um monge disse: “Não caminhe até o "
         "cume com os olhos. Caminhe até a próxima pedra com os pés.” "
         "Assim é a Escada Segura: névoa (ansiedade) não cancela o degrau visível."),
        ("Parábola das mil lanternas",
         "Uma aldeia temia a floresta. Acender mil lanternas de uma vez ofuscou a todos "
         "e causou pânico. Um ancião pediu: “Acendam uma lanterna por noite.” "
         "Em um mês, o caminho existia. Determinação não é explosão — é série."),
        ("Parábola do sino rachado",
         "O sino do templo rachou e ecoava alto demais. Quiseram jogá-lo fora. "
         "Uma artesã o reparou com metal novo (como kintsugi). O som ficou diferente — "
         "mais verdadeiro. Seu sistema de alarme também pode ser reparado, não descartado."),
        ("Parábola do jardineiro e o musgo",
         "Musgo cresceu nos degraus porque ninguém subia. O jardineiro não xingou o musgo: "
         "varreu um pouco por dia e voltou a caminhar. Evitação é musgo. Exposição é "
         "vassoura e pés."),
        ("Parábola do dragão no lago",
         "Dizia-se que um dragão vivia no lago e engolia barcos. Um pescador foi em um "
         "barco pequeno, perto da margem, todos os dias. Só viu vento e peixes. "
         "A lenda perdeu força não por discurso — por dados. Sua planilha de exposição "
         "é esse barco pequeno."),
        ("Parábola da ponte de corda",
         "A ponte balançava. Quem corria caía no medo. Quem atravessava lento, olhando "
         "a próxima tábua, chegava. Permanência > pressa."),
        ("Parábola do aprendiz e o mestre arqueiro",
         "O aprendiz queria acertar o alvo distante no primeiro dia. O mestre pôs o "
         "alvo a três passos. “Orgulho quer distância. Determinação quer precisão.” "
         "Comece fácil o suficiente para vencer."),
        ("Parábola do chá derramado",
         "Um samurai ansioso derramava chá ao servir. O mestre pediu que servisse "
         "todos os dias a mesma tigela, sem plateia. A mão aprendeu. Repetição em "
         "segurança precede desempenho em público."),
        ("Parábola do portão emperrado",
         "Empurrar com raiva quebrou a tranca. Empurrar um pouco, lubrificar, esperar, "
         "empurrar de novo — abriu. Exposição com autorraiva emperra; exposição com "
         "método abre."),
        ("Parábola das estações",
         "No inverno, a montanha parece impossível. Na primavera, o mesmo caminho "
         "existe. Seu humor e seu sono são estações: ajuste a dose da escada, "
         "não abandone o templo."),
        ("Parábola do mapa molhado",
         "A chuva molhou o mapa e as linhas borraram. O guia disse: “Então olhe as "
         "marcas no chão que seus pés já fizeram.” Seus registros de exposição são "
         "marcas no chão — quando a mente embacar, releia."),
        ("Parábola do último degrau",
         "Um peregrino quase desistiu no penúltimo degrau. Um ancião trouxe chá e "
         "disse: “Desistir aqui é carregar a montanha para sempre. Um degrau ainda "
         "é um degrau.” Determinação é voltar ao próximo ato possível."),
    ]

    p(story, "37. Doze parábolas para dias difíceis", s["h1"])
    story.append(hr())
    for i, (title, text) in enumerate(parables):
        p(story, f"<b>{title}</b>", s["h3"])
        p(story, text, s["story"])
        if (i + 1) % 2 == 0:
            story.append(PageBreak())
    if len(parables) % 2 != 0:
        story.append(PageBreak())

    p(story, "38. Ritual breve de determinação (2 minutos)", s["h1"])
    story.append(hr())
    story.append(bullets([
        "Postura de bambu: pés no chão, coluna longa, ombros baixos.",
        "Três ciclos de respiração 4-6-8.",
        "Frase: “É ansiedade, não sentença. Eu atravesso o próximo torii.”",
        "Escolher o degrau de hoje (só um).",
        "Depois: escrever uma linha de ouro (kintsugi) sobre o que aprendeu.",
    ], s["body_left"]))
    story.append(PageBreak())

    # ═══════════ PARTE XI ESCADA ═══════════
    section_break(story, "PARTE XI", "Sua Escada Segura", s)

    p(story, "39. Montar a escada — passo a passo", s["h1"])
    story.append(hr())
    p(story, "Sem escada clara, a exposição vira improviso. Improviso aumenta abandono "
      "ou saltos perigosos demais.", s["body"])
    p(story, "Minha fobia / medo-alvo (bem específico):", s["label"])
    story.append(blank_lines(3))
    p(story, "O que eu evito por causa disso:", s["label"])
    story.append(blank_lines(3))
    p(story, "Meta realista de 21 dias:", s["label"])
    story.append(blank_lines(3))
    story.append(PageBreak())

    p(story, "40. Escala de ansiedade 0–10", s["h1"])
    story.append(hr())
    data = [
        [Paragraph("<font color='white'><b>Nível</b></font>", s["field"]),
         Paragraph("<font color='white'><b>Sensação</b></font>", s["field"]),
         Paragraph("<font color='white'><b>O que fazer</b></font>", s["field"])],
        [Paragraph("0–2", s["field"]), Paragraph("Leve / tranquilo", s["field"]),
         Paragraph("Bom para treinar", s["field"])],
        [Paragraph("3–4", s["field"]), Paragraph("Desconforto manejável", s["field"]),
         Paragraph("Zona ideal", s["field"])],
        [Paragraph("5–6", s["field"]), Paragraph("Alta, porém possível", s["field"]),
         Paragraph("Use técnicas e siga se seguro", s["field"])],
        [Paragraph("7–10", s["field"]), Paragraph("Muito intenso", s["field"]),
         Paragraph("Desça 1–2 degraus", s["field"])],
    ]
    t = Table(data, colWidths=[2.2 * cm, 6.5 * cm, 7.8 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("BACKGROUND", (0, 1), (-1, -1), PALE),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))
    p(story, "41. Template da escada (10 degraus)", s["h2"])
    story.append(ladder_template(s))
    story.append(PageBreak())

    p(story, "42. Exemplos de escadas (inspire-se e personalize)", s["h1"])
    story.append(hr())
    examples = [
        ("Aerofobia", "Fotos de cabine → vídeo de decolagem → aeroporto só para observar → "
         "segurança sem voar → área de embarque → voo curto."),
        ("Acrofobia", "Fotos de varanda → vídeo de mirante → janela 2º andar → 3º → "
         "mirante com grade → caminhar perto da borda protegida."),
        ("Odontofobia", "Fotos da clínica → ligar e marcar → visitar recepção → sentar na "
         "cadeira sem procedimento → profilaxia → procedimento planejado."),
        ("Glossofobia", "Ler em voz alta sozinho → gravar áudio → falar para 1 pessoa → "
         "3 pessoas → reunião → apresentação."),
        ("Animal (ex.: cães)", "Fotos → vídeos → observar de longe → mesma calçada → "
         "aproximar com tutor → contato breve se seguro."),
    ]
    for title, text in examples:
        p(story, f"<b>{title}</b>", s["h3"])
        p(story, text, s["body"])
    story.append(PageBreak())

    p(story, "43. Técnicas de regulação", s["h1"])
    story.append(hr())
    p(story, "<b>Respiração 4-6-8:</b> inspire 4, segure 6 (se confortável), solte 8. "
      "4 ciclos. Ombros baixos.", s["body"])
    p(story, "<b>Ancoragem 5-4-3-2-1:</b> 5 coisas que vê, 4 que toca, 3 que ouve, "
      "2 que cheira, 1 que saboreia.", s["body"])
    p(story, "<b>Frase de enfrentamento:</b> “É ansiedade, não perigo.” · "
      "“Posso sentir e continuar.” · “Atravesso o próximo torii.”", s["body"])
    p(story, "Minha frase:", s["label"])
    story.append(blank_lines(2))
    story.append(PageBreak())

    # ═══════════ PARTE XII 21 DIAS ═══════════
    section_break(story, "PARTE XII", "Plano de 21 dias\n+ registros", s)

    p(story, "44. Visão geral das três semanas", s["h1"])
    story.append(hr())
    p(story, "<b>Semana 1 — Fundação:</b> mapa do medo, escada, regulação, degraus fáceis. "
      "<b>Semana 2 — Consolidação:</b> degraus intermediários e variação. "
      "<b>Semana 3 — Expansão:</b> degraus altos com segurança + manutenção.", s["body"])

    week_plan = [
        ("Dia 1 — Mapa do medo", "Leia Partes I–II. Preencha medo-alvo, evitacoes e meta."),
        ("Dia 2 — Escada rascunho", "Liste 10 degraus. Ordene. Evite saltos grandes."),
        ("Dia 3 — Treino de regulação", "Respiração e 5-4-3-2-1 três vezes, sem exposição."),
        ("Dia 4 — Degrau 1", "Exposição 5–15 min. Registre antes/pico/depois."),
        ("Dia 5 — Repetir Degrau 1", "Observe se o pico já é menor."),
        ("Dia 6 — Degrau 2", "Suba um nível. Se pico >7, volte e fortaleça."),
        ("Dia 7 — Revisão", "Ajuste a escada. Descanso ou exposição leve."),
        ("Dia 8 — Degrau 3", "Exposição + frase de enfrentamento."),
        ("Dia 9 — Degrau 3 de novo", "Foque previsão × realidade."),
        ("Dia 10 — Degrau 4", "Aumente tempo, proximidade ou duração."),
        ("Dia 11 — Variar contexto", "Mesmo degrau, outro horário/lugar."),
        ("Dia 12 — Degrau 5", "Se preciso, divida em microdegraus."),
        ("Dia 13 — Sessão dupla leve", "Duas exposições curtas se o corpo aguentar."),
        ("Dia 14 — Revisão", "Liste 5 evidências de capacidade."),
        ("Dia 15 — Degrau 6", "Exposição padrão + registro."),
        ("Dia 16 — Degrau 6/7", "Avance só com estabilidade prévia."),
        ("Dia 17 — Ensaio da meta", "Ensaio próximo da meta de 21 dias."),
        ("Dia 18 — Degrau alto (dose controlada)", "Tempo limitado, plano claro."),
        ("Dia 19 — Integração", "Exposição + atividade valorizada."),
        ("Dia 20 — Ensaio final", "Melhor ensaio possível. Celebre o processo."),
        ("Dia 21 — Manutenção", "Plano de 1–2 exposições/semana por 4 semanas."),
    ]
    for title, text in week_plan:
        p(story, f"<b>{title}</b>", s["h3"])
        p(story, text, s["body"])
    story.append(PageBreak())

    p(story, "45. Folhas de registro — use e imprima", s["h1"])
    story.append(hr())
    p(story, "Uma folha por dia de exposição. Quanto mais concreto, mais forte o aprendizado.", s["body"])

    log_days = [f"Dia {d} — Registro" for d in
                [4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20]]
    log_days += [f"Registro extra {i}" for i in range(1, 46)]
    for i, d in enumerate(log_days):
        story.append(exposure_log(s, d))
        if (i + 1) % 2 == 0 and i < len(log_days) - 1:
            story.append(PageBreak())
    story.append(PageBreak())

    p(story, "46. Escadas extras (imprimíveis)", s["h1"])
    story.append(hr())
    for n in range(1, 5):
        p(story, f"Escada em branco — versão {n}", s["h2"])
        story.append(ladder_template(s))
        story.append(Spacer(1, 10))
        if n % 2 == 0:
            story.append(PageBreak())
    if 4 % 2 != 0:
        story.append(PageBreak())

    p(story, "47. Checklist rápido antes de cada exposição", s["h1"])
    story.append(hr())
    for _ in range(6):
        story.append(bullets([
            "□ Degrau específico e mensurável",
            "□ Tempo mínimo de permanência definido",
            "□ Frase de enfrentamento pronta",
            "□ Escala 0–10 (antes / pico / depois)",
            "□ Combinado: não abandonar no pico sem plano",
            "□ Depois: escrever previsão × realidade",
            "□ Lembrete: coragem de dragão = presença, não pressa",
        ], s["body_left"]))
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # ═══════════ PARTE XIII CONCLUSÃO ═══════════
    section_break(story, "PARTE XIII", "Conclusão:\ntratamento sério e seguro", s)

    p(story, "48. O que é um tratamento sério", s["h1"])
    story.append(hr())
    p(story, "Tratamento sério de fobia específica é:", s["body"])
    story.append(bullets([
        "Baseado em evidência (exposição / TCC), não em milagre.",
        "Ético: sem humilhação, sem forçar o intolerável.",
        "Gradual o bastante para ser sustentável; firme o bastante para gerar aprendizado.",
        "Atento a comorbidades e a sinais de risco.",
        "Humilde: material ajuda; profissional acompanha quando necessário.",
        "Mensurável: registros, metas, revisão.",
    ], s["body_left"]))
    p(story, "Seguro não significa “sem desconforto”. Significa desconforto <b>com método, "
      "limites e rede de apoio</b>.", s["body"])

    p(story, "49. Sua aliança com a determinação", s["h2"])
    p(story, "As parábolas japonesas deste book não são enfeite. São âncoras de memória "
      "para os dias em que a névoa volta. Quando voltar — e ela volta — escolha a "
      "próxima pedra. Um torii. Um degrau. Um microvoo do dragão.", s["body"])
    p(story, "“A aldeia não precisa que você mate o dragão em público. "
      "Precisa que você atravesse a ponte o suficiente vezes para o caminho existir de novo.”", s["quote"])
    story.append(PageBreak())

    p(story, "50. Carta final a quem segura este book", s["h1"])
    story.append(hr())
    p(story, "Se você chegou até aqui, já praticou um ato raro: estudar o próprio medo "
      "com seriedade e imaginação. Isso é ciência e também coragem.", s["body"])
    p(story, "Use as folhas. Rabisque. Erre o degrau. Volte. Polir a lâmina. "
      "Acenda uma lanterna por noite. Repare com ouro o que rachar.", s["body"])
    p(story, "E se a montanha for alta demais sozinha, chame guia — terapia com "
      "profissional habilitado. Há sabedoria em pedir ajuda; há sabedoria em treinar; "
      "há sabedoria em fazer as duas coisas.", s["body"])
    p(story, "Com respeito ao seu ritmo,", s["body"])
    p(story, "<b>Dra. Priscila Palomo</b><br/>Psicóloga · CRP 98007<br/>"
      "Especialista em fobias<br/>www.priscilapalomo.com · WhatsApp (11) 95069-0537", s["body_left"])
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceBefore=8, spaceAfter=12))
    p(story, "Programa Escada Segura — Book · Material psicoeducativo · Não substitui psicoterapia · "
      "Dra. Priscila Palomo · CRP 98007", s["footer"])

    # Páginas extras de prática para aproximar 200 págs
    story.append(PageBreak())
    p(story, "Apêndice A — Diário semanal de determinação", s["h1"])
    story.append(hr())
    for week in range(1, 9):
        p(story, f"<b>Semana {week}</b>", s["h2"])
        p(story, "Vitórias (lanternas acesas):", s["label"])
        story.append(blank_lines(3))
        p(story, "Musgo da evitação que voltou:", s["label"])
        story.append(blank_lines(2))
        p(story, "Próximo torii:", s["label"])
        story.append(blank_lines(2))
        if week % 2 == 0:
            story.append(PageBreak())
    if 8 % 2 != 0:
        story.append(PageBreak())

    p(story, "Apêndice B — Banco de frases de enfrentamento", s["h1"])
    story.append(hr())
    phrases = [
        "É ansiedade, não perigo imediato.",
        "Posso sentir e continuar.",
        "Só o próximo degrau.",
        "O sino pode tocar; eu não preciso fugir.",
        "Dragão respira fumaça — eu atravesso mesmo assim.",
        "Previsão não é fato.",
        "Já estive aqui e desci a curva.",
        "Bamboo verga e segue.",
        "Um torii por vez.",
        "Kintsugi: rachadura com ouro.",
        "Pequeno e frequente.",
        "Eu sou o peregrino que volta amanhã.",
    ]
    for ph in phrases:
        p(story, f"□ {ph}", s["body_left"])
    p(story, "Minhas frases personalizadas:", s["label"])
    story.append(blank_lines(6))
    story.append(PageBreak())

    p(story, "Apêndice C — Registros livres adicionais", s["h1"])
    story.append(hr())
    for i in range(1, 41):
        story.append(exposure_log(s, f"Registro livre {i}"))
        if i % 2 == 0 and i < 40:
            story.append(PageBreak())
    story.append(PageBreak())

    # Apêndice D — aprofundamentos para chegar ao book completo
    p(story, "Apêndice D — Sintomas por tipo de fobia (guia prático)", s["h1"])
    story.append(hr())
    types_detail = [
        ("Animal", "Susto ao ver/ouvir; imagens intrusivas; evitação de parques/casas; "
         "pesquisa antecipatória de “onde pode aparecer”."),
        ("Ambiente natural", "Monitoramento do tempo; evitar janelas/varandas/praia; "
         "tontura em altura; plano de fuga mental constante."),
        ("Sangue-injeção-ferimentos", "Náusea, suor frio, visão escurecendo, desmaio; "
         "adiar exames e vacinas; medo de “passar mal na frente de todos”."),
        ("Situacional", "Evitação de elevador/avião/carro; chegar cedo demais ou não ir; "
         "necessidade de corredor livre / saída visível."),
        ("Outros", "Medo de engasgar/vomitar/personagens; restrição alimentar situacional; "
         "evitar festas infantis ou hospitais."),
    ]
    for title, text in types_detail:
        p(story, f"<b>{title}</b>", s["h3"])
        p(story, text, s["body"])
        p(story, "Meus sinais neste tipo (se aplicar):", s["label"])
        story.append(blank_lines(3))
    story.append(PageBreak())

    p(story, "Apêndice E — Mais parábolas de determinação", s["h1"])
    story.append(hr())
    more_parables = [
        ("A pedra do caminho",
         "Um monge tropeçava sempre na mesma pedra. No centésimo dia, em vez de xingar a pedra, "
         "ele a pintou de vermelho — lembrete. A pedra ainda estava lá; a cegueira não. "
         "Nomear o gatilho com clareza é pintar a pedra."),
        ("O guarda do portão",
         "Um guarda gritava com todos que se aproximavam. Um visitante foi todos os dias só "
         "para cumprimentá-lo, sem exigir entrar. No vigésimo dia, o guarda abriu. "
         "Às vezes a exposição começa com presença simples diante do alarme."),
        ("A montanha e o copo",
         "“Como mover uma montanha?” — “Copos de terra por dia.” Assim também a fobia."),
        ("O espelho embaciado",
         "Ansiedade embacia o espelho: você parece menor e o dragão maior. Respirar e "
         "registrar limpam o vapor o suficiente para ver o próximo degrau."),
        ("A corda de mil nós",
         "Desfazer um nó por vez. Quem puxa todos juntos aperta o emaranhado."),
        ("O farol na tempestade",
         "O farol não apaga a tempestade; marca o caminho. Sua frase de enfrentamento "
         "é farol — não controle do clima interno."),
        ("O aprendiz silencioso",
         "Falava tanto sobre coragem que não sobrava fôlego para treinar. O mestre "
         "proibiu discursos por uma semana — só ação pequena. A coragem voltou pelos pés."),
        ("A porta de papel",
         "Parecia muro. Era papel shoji. Muitos medos parecem pedra e são papel — "
         "descobertos só com o toque cuidadoso da exposição."),
    ]
    for title, text in more_parables:
        p(story, f"<b>{title}</b>", s["h3"])
        p(story, text, s["story"])
    story.append(PageBreak())

    p(story, "Apêndice F — Plano de manutenção (12 semanas)", s["h1"])
    story.append(hr())
    for w in range(1, 13):
        p(story, f"<b>Semana {w} de manutenção</b>", s["h3"])
        p(story, "Exposições planejadas (1–3): _______________________________", s["field"])
        p(story, "Amuletos soltos: _______________________________", s["field"])
        p(story, "Aprendizado-ouro (kintsugi):", s["label"])
        story.append(blank_lines(2))
        if w % 3 == 0:
            story.append(PageBreak())
    if 12 % 3 != 0:
        story.append(PageBreak())

    p(story, "Apêndice G — Página de compromisso do dragão", s["h1"])
    story.append(hr())
    p(story, "Eu, _______________________________, comprometo-me a treinar a Escada Segura "
      "com seriedade e gentileza: doses pequenas, repetição, registro e pedido de ajuda "
      "quando necessário. Escolho a coragem de um dragão — presença, não pressa.", s["body"])
    story.append(Spacer(1, 12))
    p(story, "Assinatura: ________________________  Data: ____/____/________", s["field"])
    story.append(Spacer(1, 16))
    p(story, "Testemunha (opcional): ________________________", s["field"])
    story.append(Spacer(1, 20))
    p(story, "“Um torii por vez. Um degrau por vez. Um pergaminho novo por vez.”", s["quote"])
    story.append(PageBreak())

    p(story, "Apêndice H — Glossário amigável", s["h1"])
    story.append(hr())
    glossary = [
        ("Ansiedade antecipatória", "Medo que aparece antes do evento, às vezes pior que o evento."),
        ("Aprendizado inibitório", "Nova aprendizagem de segurança que compete com o medo antigo."),
        ("Comportamento de segurança", "Atalho que reduz ansiedade na hora e enfraquece o aprendizado."),
        ("DSM-5", "Manual diagnóstico usado por profissionais para classificar transtornos."),
        ("Evitação", "Não entrar em contato com o gatilho; mantém a fobia."),
        ("Exposição", "Contato planejado e repetido com o gatilho temido."),
        ("Fobia específica", "Medo intenso e desproporcional de objeto/situação circunscrita."),
        ("Habituação", "Queda da ansiedade com permanência e repetição."),
        ("Hierarquia", "Escada de situações do mais fácil ao mais difícil."),
        ("Interocepção", "Percepção das sensações internas do corpo."),
        ("TCC", "Terapia Cognitivo-Comportamental."),
        ("Violação de expectativa", "Quando a realidade desmente a catástrofe prevista."),
    ]
    for term, meaning in glossary:
        p(story, f"<b>{term}:</b> {meaning}", s["body"])
    story.append(PageBreak())

    p(story, "Apêndice I — Leituras e caminhos seguintes", s["h1"])
    story.append(hr())
    p(story, "Se quiser aprofundar com profissional: busque psicólogo(a) com experiência "
      "em TCC e exposição para fobias. Se houver desmaios em sangue/agulha, mencione "
      "isso — há técnicas específicas. Se houver trauma, pânico amplo ou depressão, "
      "avalie um plano integrado.", s["body"])
    p(story, "Materiais complementares no site: www.priscilapalomo.com/loja.html", s["body"])
    p(story, "Landing do programa: www.priscilapalomo.com/escada-segura.html", s["body"])
    story.append(Spacer(1, 12))
    p(story, "Notas pessoais / perguntas para a próxima sessão de terapia:", s["label"])
    story.append(blank_lines(10))
    story.append(PageBreak())

    p(story, "Apêndice J — Últimas folhas de treino", s["h1"])
    story.append(hr())
    for i in range(1, 29):
        story.append(exposure_log(s, f"Treino final {i}"))
        if i % 2 == 0 and i < 28:
            story.append(PageBreak())

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"OK: {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
