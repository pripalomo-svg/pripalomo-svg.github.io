#!/usr/bin/env python3
"""Gera o book PDF Programa Escada Segura.

Formato: ROMANCE DE JORNADA DO HERÓI.
A história de Íris Valente, que entra na Academia Escada Segura para enfrentar
o Senhor do Nunca — a entidade que se alimenta da fuga. Cada capítulo tem
exatamente 2 páginas:
  - Página 1: o capítulo do romance (a cena narrada).
  - Página 2: "O Grimório da Ciência" — DSM-5, TCC e o modelo de David H. Barlow
    explicando o que realmente aconteceu ali, mais o feitiço (técnica) e a prática.

Depois do romance vem o caderno de treino do leitor: escada pessoal, as 21
Provações com folhas de registro e os apêndices clínicos.
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
WARM = HexColor("#FDF6EC")

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
    s["ato"] = ParagraphStyle(
        "ato", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=13, textColor=NAVY, alignment=TA_CENTER, spaceBefore=6, spaceAfter=8,
    )
    s["part"] = ParagraphStyle(
        "part", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=10.5, textColor=ORANGE, alignment=TA_LEFT, spaceBefore=0, spaceAfter=3,
    )
    s["h1"] = ParagraphStyle(
        "h1", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=17, textColor=NAVY, spaceBefore=0, spaceAfter=6, leading=21,
    )
    s["h2"] = ParagraphStyle(
        "h2", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=12.5, textColor=INK, spaceBefore=8, spaceAfter=4, leading=16,
    )
    s["h3"] = ParagraphStyle(
        "h3", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=11, textColor=NAVY, spaceBefore=8, spaceAfter=4, leading=15,
    )
    s["body"] = ParagraphStyle(
        "body", parent=base["Normal"], fontName="Helvetica",
        fontSize=10, textColor=INK, alignment=TA_JUSTIFY, leading=15, spaceAfter=7,
    )
    s["body_left"] = ParagraphStyle(
        "body_left", parent=s["body"], alignment=TA_LEFT,
    )
    s["prosa"] = ParagraphStyle(
        "prosa", parent=base["Normal"], fontName="Helvetica",
        fontSize=10.2, textColor=INK, alignment=TA_JUSTIFY, leading=15.6,
        spaceAfter=7, firstLineIndent=14,
    )
    s["prosa_first"] = ParagraphStyle(
        "prosa_first", parent=s["prosa"], firstLineIndent=0,
    )
    s["fala"] = ParagraphStyle(
        "fala", parent=s["prosa"], fontName="Helvetica-Oblique", firstLineIndent=14,
    )
    s["small"] = ParagraphStyle(
        "small", parent=base["Normal"], fontName="Helvetica",
        fontSize=9, textColor=MUTED, leading=13, spaceAfter=4,
    )
    s["epigrafe"] = ParagraphStyle(
        "epigrafe", parent=base["Normal"], fontName="Helvetica-Oblique",
        fontSize=9.5, textColor=MUTED, alignment=TA_CENTER, leading=13.5,
        spaceBefore=2, spaceAfter=10, leftIndent=20, rightIndent=20,
    )
    s["quote"] = ParagraphStyle(
        "quote", parent=base["Normal"], fontName="Helvetica-Oblique",
        fontSize=11, textColor=NAVY, alignment=TA_CENTER, leading=16,
        spaceBefore=8, spaceAfter=8, leftIndent=12, rightIndent=12,
    )
    s["label"] = ParagraphStyle(
        "label", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=9.5, textColor=ORANGE, spaceBefore=6, spaceAfter=3,
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
        [ListItem(Paragraph(i, style), leftIndent=6, bulletColor=NAVY) for i in items],
        bulletType="bullet", start="•", leftIndent=12, spaceBefore=1, spaceAfter=5,
    )


def blank_lines(n=2):
    rows = [["_" * 80] for _ in range(n)]
    t = Table(rows, colWidths=[16.5 * cm])
    t.setStyle(TableStyle([
        ("TEXTCOLOR", (0, 0), (-1, -1), LINE),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


def caixa(title, text, s, bg=PALE, header_bg=NAVY):
    header = Table([[Paragraph(title, s["day_title"])]], colWidths=[16.5 * cm])
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), header_bg),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    body = Table([[Paragraph(text, s["body"])]], colWidths=[16.5 * cm])
    body.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
    ]))
    return KeepTogether([header, body, Spacer(1, 6)])


def callout(title, text, s):
    return caixa(title, text, s)


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
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def exposure_log(s, label):
    paras = [
        Paragraph("Data: ____ / ____ / ______ &nbsp;&nbsp;|&nbsp;&nbsp; Degrau trabalhado: _______________________________________", s["field"]),
        Paragraph("Ansiedade (0–10) &nbsp; antes: ____ &nbsp;&nbsp; pico: ____ &nbsp;&nbsp; ao final: ____ &nbsp;&nbsp;|&nbsp;&nbsp; permanência: ____ min &nbsp;&nbsp;|&nbsp;&nbsp; muleta usada: __________", s["field"]),
        Paragraph("O que eu fiz exatamente (a minha travessia de hoje):", s["label"]), blank_lines(4),
        Paragraph("O que o Senhor do Nunca previu (a catástrofe anunciada, com número e tempo):", s["label"]), blank_lines(3),
        Paragraph("O que realmente aconteceu (a Lanterna dos Fatos):", s["label"]), blank_lines(4),
        Paragraph("O que eu aprendi e levo comigo (novo pergaminho):", s["label"]), blank_lines(3),
    ]
    return day_box(label, paras, s)


def add_page_number(canvas, doc):
    canvas.saveState()
    page = canvas.getPageNumber()
    if page > 1:
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawCentredString(
            A4[0] / 2, 1.2 * cm,
            f"A Escada Segura — a jornada de Íris Valente  ·  Dra. Priscila Palomo  ·  p. {page}"
        )
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.4)
        canvas.line(2 * cm, 1.6 * cm, A4[0] - 2 * cm, 1.6 * cm)
    canvas.restoreState()


def p(story, text, style):
    story.append(Paragraph(text, style))


def prosa(story, paras, s):
    """Escreve os parágrafos do romance (o primeiro sem recuo)."""
    for i, texto in enumerate(paras):
        p(story, texto, s["prosa_first"] if i == 0 else s["prosa"])


def abertura_de_ato(story, ato, titulo, subtitulo, s):
    story.append(Spacer(1, 5.5 * cm))
    p(story, ato, s["ato"])
    p(story, titulo, s["cover_title"])
    story.append(HRFlowable(width="34%", thickness=2, color=NAVY, spaceBefore=6, spaceAfter=14))
    p(story, subtitulo, s["cover_sub"])
    story.append(PageBreak())


def capitulo(story, cap, ato, titulo, epigrafe, img, cena, grimorio_tit, grimorio,
             feitico_tit, feitico_txt, pratica, s):
    """Um capítulo do romance em exatamente 2 páginas."""
    # ── Página 1: o romance ──
    p(story, f"{ato} · CAPÍTULO {cap:02d}", s["part"])
    p(story, titulo, s["h1"])
    p(story, epigrafe, s["epigrafe"])
    story.append(hr())
    if img:
        story.append(ilustra(img, 5.6 * cm))
        story.append(Spacer(1, 8))
    prosa(story, cena, s)
    story.append(PageBreak())

    # ── Página 2: o grimório da ciência ──
    p(story, f"O Grimório da Ciência · Capítulo {cap:02d}", s["part"])
    p(story, grimorio_tit, s["h1"])
    story.append(hr())
    for bloco in grimorio:
        if isinstance(bloco, list):
            story.append(bullets(bloco, s["body_left"]))
        else:
            p(story, bloco, s["body"])
    story.append(Spacer(1, 4))
    story.append(caixa(f"O feitiço que você aprende aqui: {feitico_tit}", feitico_txt, s))
    p(story, "Sua vez, aprendiz", s["h3"])
    for prompt in pratica:
        p(story, prompt, s["label"])
        story.append(blank_lines(2))
    story.append(PageBreak())


# ═══════════════════════════════════════════════════════════════════
#  O ROMANCE — 24 capítulos em 4 atos
# ═══════════════════════════════════════════════════════════════════

CAPITULOS = [

    # ─────────────── ATO I — O CHAMADO ───────────────
    dict(
        cap=1, ato="ATO I — O CHAMADO",
        titulo="A vida que coube dentro de um quarto",
        epigrafe="“Ninguém percebe o dia exato em que o mundo começa a encolher.”",
        img=None,
        cena=[
            "Íris Valente tinha vinte e nove anos, um diploma de arquitetura pendurado na parede e um mundo "
            "que cabia em quatro paredes e meia. Não fora sempre assim. Houve um tempo em que ela subia em "
            "árvores, andava de bicicleta na ladeira e ria alto no último banco do ônibus escolar.",
            "A mudança foi silenciosa, como cupim em viga de madeira. Primeiro ela deixou de ir à sacada do "
            "apartamento da tia. Depois passou a evitar o elevador panorâmico do escritório, subindo os seis "
            "lances de escada com a bolsa apertada contra o peito. Depois recusou uma visita técnica a uma obra "
            "de doze andares e inventou uma gripe que não tinha. Cada recusa parecia pequena. Cada recusa "
            "parecia sensata. Cada recusa vinha acompanhada de um alívio morno e imediato, como um cobertor "
            "em noite fria.",
            "O que Íris não sabia é que alguém se alimentava daquele alívio.",
            "Naquela terça-feira, ela recebeu o e-mail que temia: o escritório havia sido escolhido para "
            "projetar a reforma do Edifício Aurora — vinte e dois andares, terraço de vidro, mirante aberto "
            "para a cidade inteira. Seu nome estava na primeira linha da equipe. Íris leu três vezes. "
            "Depois fechou o notebook, sentou no chão da cozinha com as costas na porta da geladeira e "
            "esperou o coração parar de bater na garganta.",
            "A cozinha era o cômodo mais seguro da casa dela, e Íris sabia disso com uma precisão "
            "constrangedora. Sem janela grande. Sem sacada. Chão a menos de um metro de qualquer coisa em que "
            "ela pudesse se apoiar. Nos últimos anos, ela havia transformado o apartamento inteiro num mapa "
            "de zonas: os lugares onde podia respirar e os lugares onde não convinha estar.",
            "— É só um projeto — disse em voz alta, para ninguém. — Eu recuso e pronto.",
            "E foi então que ela ouviu, num tom quase gentil, quase carinhoso, uma voz que parecia vir de "
            "dentro do próprio peito:",
            "— Recuse. Recuse tudo. Eu cuido de você.",
            "A voz era macia. A voz era boa. A voz tinha razão. E Íris, que sempre se achara uma mulher "
            "racional, não percebeu que acabara de ser apresentada, pela milésima vez na vida, ao seu inimigo.",
            "Ela escreveu a resposta ao e-mail em quatro minutos. Alegou sobrecarga de projetos. Releu duas "
            "vezes, achou convincente, apertou enviar — e sentiu, no segundo seguinte, aquela onda morna e "
            "deliciosa de alívio que sempre vinha depois de dizer não.",
            "O alívio durou quarenta minutos.",
            "Depois veio o resto: a vergonha discreta, a conta do que ela acabara de recusar, a lembrança "
            "incômoda da menina que subia em árvores. Íris lavou a louça já limpa, arrumou a estante já "
            "arrumada e foi dormir às nove da noite, porque dormir era o único lugar onde ninguém oferecia "
            "nada a ela.",
        ],
        grimorio_tit="Quando a esquiva vira o dono da casa",
        grimorio=[
            "O que Íris viveu não é falta de coragem: é o funcionamento previsível de um sistema de defesa "
            "bem calibrado que passou a operar com sensibilidade excessiva. A cada recusa, ela sentiu alívio "
            "imediato — e é exatamente esse alívio que ensina o cérebro a recusar de novo.",
            "Esse mecanismo tem nome técnico: <b>reforço negativo</b>. Descrito por O. H. Mowrer e integrado "
            "por <b>David H. Barlow</b> ao modelo contemporâneo dos transtornos de ansiedade, ele explica por "
            "que a fobia não some com o tempo. Fugir funciona — no curtíssimo prazo. E aquilo que funciona "
            "rápido é repetido; aquilo que é repetido vira hábito; aquilo que vira hábito, vira identidade.",
            "Barlow descreve ainda a <b>tríplice vulnerabilidade</b>: uma vulnerabilidade biológica geral "
            "(temperamento mais reativo, herdado), uma vulnerabilidade psicológica geral (a sensação precoce de "
            "que o mundo é imprevisível e de que eu não dou conta) e uma vulnerabilidade psicológica específica "
            "(aprender, por experiência direta, por observação ou por informação, que <i>este</i> objeto em "
            "particular é perigoso). Não é culpa. É história.",
            "O detalhe cruel: a esquiva cobra juros. Cada situação evitada hoje aumenta o custo da mesma "
            "situação amanhã. É por isso que o mundo encolhe em silêncio.",
        ],
        feitico_tit="O Inventário do Mundo Perdido",
        feitico_txt="Antes de enfrentar qualquer coisa, escreva o que o medo já tomou de você. Não para se "
                    "culpar — para medir o inimigo. Uma lista honesta de evitações é o primeiro mapa do território.",
        pratica=[
            "1. Escreva três coisas que você deixou de fazer nos últimos 12 meses por causa do medo:",
            "2. Qual foi o alívio imediato que você sentiu ao recusar? E o custo que veio depois?",
        ],
    ),

    dict(
        cap=2, ato="ATO I — O CHAMADO",
        titulo="A carta que entrou pela fresta da porta",
        epigrafe="“Toda travessia começa com um convite que dá vontade de rasgar.”",
        img=None,
        cena=[
            "O envelope apareceu na manhã de quinta-feira, encaixado na fresta debaixo da porta, como se "
            "alguém o tivesse empurrado com a ponta do sapato. Papel grosso, cor de areia, sem selo e sem "
            "remetente. Só o nome dela, escrito à mão com uma caligrafia inclinada e antiga:",
            "<i>Íris Valente — a que subiu em árvores.</i>",
            "Dentro, uma única folha:",
            "<i>“Cara Íris, existe uma casa no alto da Colina do Sino onde ensinamos uma coisa só: como "
            "atravessar aquilo que você vem contornando. Não prometemos que o medo vai sumir. Prometemos que "
            "ele vai deixar de mandar. As aulas começam na segunda-feira, às sete. Traga roupa confortável e "
            "uma lista honesta. — Mestre Barlovis, diretor.”</i>",
            "Íris riu. Depois releu. Depois riu de novo, um riso curto e sem graça, do tipo que a gente dá "
            "quando alguém acerta em cheio.",
            "— É golpe — disse ela.",
            "— É golpe — concordou a voz macia, e Íris sentiu o estômago gelar, porque a voz nunca havia "
            "concordado tão rápido com ela antes. — Fique. Aqui é seguro. Lá fora tem escada, tem elevador, "
            "tem varanda. Aqui tem café e cobertor.",
            "Foi essa concordância entusiasmada que a fez levantar. Anos depois, Íris diria em entrevistas "
            "que a decisão mais importante da sua vida não foi um ato de coragem: foi uma desconfiança. "
            "Ela desconfiou da voz que sempre lhe dava razão.",
            "Escrever a lista foi a parte mais difícil do fim de semana. Ela começou achando que teria três "
            "ou quatro itens. Parou no dezessete porque a caneta falhou, não porque a lista tivesse acabado.",
            "<i>Não subo em escada de casa. Não uso elevador panorâmico. Não vou à sacada da tia. Não aceito "
            "obra acima de quatro andares. Não atravesso passarela. Não sento em mesa perto de janela alta. "
            "Não viajo de avião desde 2019…</i>",
            "Cada linha era pequena. Juntas, formavam o desenho exato de uma vida encolhida — e Íris, que era "
            "arquiteta e sabia ler plantas, reconheceu na própria letra o projeto de uma casa sem janelas.",
            "Na segunda-feira, às seis e quarenta, ela estava no pé da Colina do Sino com uma mochila, "
            "um tênis velho e a folha dobrada no bolso.",
        ],
        grimorio_tit="A ambivalência é parte do tratamento, não um defeito seu",
        grimorio=[
            "Querer e não querer ao mesmo tempo é o estado normal de quem vai iniciar um tratamento de "
            "exposição. Em TCC chamamos isso de <b>ambivalência</b>, e ela não é sinal de falta de motivação: "
            "é sinal de que o cérebro está avaliando um custo real de curto prazo (desconforto) contra um "
            "ganho de longo prazo (liberdade).",
            "A decisão de Íris ilustra um princípio central da entrevista motivacional aplicada à ansiedade: "
            "a mudança raramente começa quando o medo acaba. Ela começa quando o <b>custo da evitação</b> "
            "fica maior, aos olhos da própria pessoa, do que o custo do enfrentamento.",
            "Repare também no que a voz fez: ela ofereceu segurança imediata. Toda esquiva se apresenta como "
            "cuidado. É por isso que ela é tão difícil de desmontar — não parece um inimigo, parece um amigo "
            "prudente. Barlow chama a atenção para esse ponto no Protocolo Unificado: é preciso aprender a "
            "reconhecer as <b>emoções orientadoras da ação</b> e escolher, deliberadamente, agir de forma "
            "contrária ao impulso quando o impulso não serve aos seus valores.",
            "Escrever a lista, como Íris fez, tem função clínica: transforma um sofrimento difuso em alvos "
            "concretos e mensuráveis. O que não é nomeado não pode ser treinado.",
        ],
        feitico_tit="A Balança dos Dois Custos",
        feitico_txt="De um lado, escreva o que a evitação te dá hoje (alívio, previsibilidade). Do outro, "
                    "o que ela te cobra este ano (oportunidades, vínculos, autoestima). Decisões duram mais "
                    "quando são tomadas com os dois lados à vista.",
        pratica=[
            "1. O que a minha esquiva me oferece de bom, honestamente?",
            "2. Qual é a fatura que ela me apresenta no fim de cada ano?",
        ],
    ),

    dict(
        cap=3, ato="ATO I — O CHAMADO",
        titulo="A Academia na Colina do Sino",
        epigrafe="“Aqui ninguém é empurrado. Aqui todo mundo caminha.”",
        img=None,
        cena=[
            "A casa era grande, de pedra clara, com janelas altas e um pátio de cascalho onde o vento fazia "
            "barulho de chuva. No alto do telhado havia um sino de bronze escurecido pelo tempo. Íris "
            "esperava um hospital. Encontrou algo mais parecido com uma escola antiga que alguém tivesse "
            "esquecido de fechar.",
            "No portão, dois aprendizes discutiam.",
            "— Eu <i>vou</i> chegar perto — dizia um rapaz magro, de cabelo desalinhado, apertando as alças "
            "da mochila. — Só não hoje. Hoje o cachorro tá muito acordado.",
            "— Téo, o cachorro tem quatro quilos e dorme dezoito horas por dia — respondeu a moça ao lado, "
            "de tranças e jaleco improvisado. — E antes que você pergunte: sim, eu ainda desmaio quando vejo "
            "agulha. Sou enfermeira. É engraçado até doer.",
            "— Nina — apresentou-se, estendendo a mão para Íris. — Aquele é o Téo. E você tem cara de quem "
            "não olha para baixo.",
            "Íris riu pela primeira vez em semanas.",
            "O Mestre Barlovis os recebeu no salão. Era um homem alto, de barba branca curta e olhos que "
            "pareciam achar graça em tudo. Não usava túnica nem varinha: usava um suéter cinza com o cotovelo "
            "puído e carregava um caderno de capa dura.",
            "— Regra um — disse ele, sem cumprimentar. — Ninguém aqui será empurrado, agarrado ou surpreendido. "
            "Nada acontece com vocês sem que vocês saibam antes. Regra dois: a gente não vem aqui para deixar "
            "de sentir medo. A gente vem para deixar de obedecer a ele. Regra três — e essa é a única que eu "
            "vou repetir todos os dias: <b>quem manda na escada é quem sobe</b>.",
            "Ele parou diante de Íris e olhou a folha dobrada que ela ainda segurava.",
            "— Dezessete? — perguntou.",
            "— Dezessete — respondeu ela.",
            "— Ótimo. Então temos dezessete degraus para construir.",
            "Íris esperava perguntas sobre a infância, sobre a origem do medo, sobre o dia em que tudo "
            "começou. Não veio nenhuma. Barlovis dobrou a folha, devolveu a ela e apontou para a janela do "
            "salão, onde se via o pátio de cascalho e o muro baixo.",
            "— A gente pode passar seis meses descobrindo por que o alarme foi calibrado assim. É "
            "interessante, e às vezes ajuda. Mas repare: saber por que o sino toca alto nunca fez o sino "
            "tocar mais baixo. — Ele coçou a barba. — Amanhã você começa a atravessar o pátio. Hoje você só "
            "precisa descansar e escolher a cama que fica mais longe da porta, porque o Téo ronca.",
            "Naquela noite, no dormitório escuro, Íris ouviu Téo roncar, Nina rir baixinho da própria "
            "insônia e o vento bater no sino sem que ele tocasse. Dormiu com a folha das dezessete linhas "
            "debaixo do travesseiro, como quem guarda um mapa.",
        ],
        grimorio_tit="Por que consentimento e previsibilidade são terapêuticos",
        grimorio=[
            "As três regras do Mestre Barlovis não são poesia: são requisitos éticos e técnicos da terapia "
            "de exposição baseada em evidências.",
            "<b>Nada de surpresas.</b> A exposição eficaz é <i>planejada, previsível e consentida</i>. "
            "Emboscadas terapêuticas (empurrar alguém para dentro do estímulo) aumentam a sensação de "
            "descontrole, elevam o risco de abandono do tratamento e podem reforçar a crença de que o mundo é "
            "imprevisível — exatamente a vulnerabilidade que queremos reduzir (Barlow, 2002).",
            "<b>O objetivo não é zerar o medo.</b> O objetivo é ampliar o repertório: sentir e ainda assim "
            "agir. Isso muda a métrica de sucesso — não medimos “quanto eu não senti”, medimos “o que eu "
            "consegui fazer sentindo”.",
            "<b>Quem manda na escada é quem sobe.</b> O senso de controle percebido é um preditor consistente "
            "de melhora. Quando a pessoa escolhe o degrau, o horário e o ritmo, a adesão sobe e a autoeficácia "
            "(Bandura, 1997) cresce a cada tarefa concluída.",
            "E há o ingrediente que Íris recebeu de graça no portão: <b>outras pessoas com o mesmo problema</b>. "
            "Saber que o próprio sofrimento tem nome, causa e estatística reduz vergonha — e vergonha é um dos "
            "principais motivos pelos quais fobias específicas ficam décadas sem tratamento.",
        ],
        feitico_tit="O Contrato de Três Regras",
        feitico_txt="Escreva e assine as suas: (1) nada acontece sem meu consentimento; (2) meu objetivo é agir, "
                    "não deixar de sentir; (3) eu escolho o degrau. Releia antes de cada treino.",
        pratica=[
            "1. Qual regra é a mais difícil de aceitar para mim, e por quê?",
            "2. Quem pode ser o meu “Téo” e a minha “Nina” nesta jornada (companhia honesta, sem resgate)?",
        ],
    ),

    dict(
        cap=4, ato="ATO I — O CHAMADO",
        titulo="O sino que toca sem fogo",
        epigrafe="“O seu alarme não está quebrado. Está exagerado — e alarme exagerado se recalibra.”",
        img="alarme",
        cena=[
            "A primeira aula foi no pátio, embaixo do sino.",
            "— Quem sabe para que serve isto? — perguntou Barlovis, batendo com o nó do dedo no bronze.",
            "— Avisar de incêndio — arriscou Téo.",
            "— Avisar de <i>perigo</i> — corrigiu o mestre. — E é a coisa mais generosa que existe nesta casa. "
            "Um sino que toca quando a viga cede salva vidas. O problema desta casa em particular… — ele deu "
            "dois passos e apontou para uma pequena janela da cozinha, de onde saía uma fumacinha branca — "
            "…é que o sino também toca quando alguém faz torrada.",
            "O sino tocou. Alto. Íris levou um susto tão grande que derrubou a garrafa de água.",
            "— Coração? — perguntou Barlovis, sem se virar.",
            "— Batendo na orelha — disse ela.",
            "— Mãos?",
            "— Geladas.",
            "— Alguma casa pegando fogo?",
            "Íris olhou em volta. A cozinheira acenou da janela, segurando uma torrada dourada.",
            "— Nenhuma — admitiu.",
            "— Então guarde esta frase, porque ela vai te acompanhar até o último dia: <b>o alarme tocou, "
            "e não havia fogo</b>. Isso não é loucura. Isso não é fraqueza. Isso é um sistema de proteção "
            "muito bom, com o sensor calibrado fino demais. E a boa notícia, Íris… — ele finalmente se virou, "
            "e havia algo quase alegre no rosto dele — …é que sensor se recalibra. Não com discurso. Com "
            "experiência repetida.",
            "Naquela noite, deitada no dormitório, Íris ouviu de novo a voz macia dizer que ali era perigoso, "
            "que ela devia voltar para casa. Pela primeira vez, ela respondeu em pensamento: <i>o alarme "
            "tocou, e não há fogo</i>. A voz não gostou.",
        ],
        grimorio_tit="Alarme falso: a neurobiologia do susto sem perigo",
        grimorio=[
            "O que Barlovis chama de sino é o circuito de detecção de ameaça. O estímulo chega ao tálamo e "
            "segue por duas vias descritas por <b>Joseph LeDoux</b>: uma via rápida e grosseira, direto para a "
            "<b>amígdala</b> (dispara antes de você entender o que viu), e uma via lenta e precisa, que passa "
            "pelo córtex (entende, contextualiza, corrige). O susto vem antes da análise — sempre.",
            "Ativada a amígdala, o <b>eixo HPA</b> e o sistema nervoso simpático fazem o resto: adrenalina e "
            "noradrenalina na corrente sanguínea, coração acelerado para bombear oxigênio, respiração rápida, "
            "sangue redirecionado da pele e do trato digestivo para os grandes músculos, pupilas dilatadas, "
            "sudorese para resfriar o corpo. Cada sintoma que assusta tem uma função de sobrevivência.",
            "Barlow chamou de <b>alarme falso</b> (<i>false alarm</i>) a ativação completa dessa resposta na "
            "ausência de perigo real. E de <b>alarme aprendido</b> (<i>learned alarm</i>) o passo seguinte: "
            "quando o corpo passa a disparar diante de pistas associadas — a foto de um penhasco, a palavra "
            "“terraço”, a porta do elevador se fechando.",
            "Por que a psicoeducação vem antes da exposição? Porque interpretar taquicardia como “vou ter um "
            "infarto” multiplica a ansiedade; interpretá-la como “é adrenalina, e adrenalina é segura” "
            "interrompe o ciclo de amplificação. A informação correta não cura a fobia, mas reduz a "
            "hipervigilância interoceptiva e prepara o terreno para o trabalho real.",
        ],
        feitico_tit="A Frase do Sino",
        feitico_txt="“O alarme tocou, e não há fogo.” Diga em voz alta na hora do pico. Não é pensamento "
                    "positivo: é discriminação entre <i>sinal de perigo</i> e <i>sensação de desconforto</i>.",
        pratica=[
            "1. Quais sensações do meu corpo eu costumo interpretar como catástrofe?",
            "2. Reescreva cada uma como função biológica (ex.: “coração acelerado = adrenalina, corpo pronto”):",
        ],
    ),

    dict(
        cap=5, ato="ATO I — O CHAMADO",
        titulo="O Espelho de Nunca-Foi",
        epigrafe="“Ele não te faz mal. Ele só te faz menor.”",
        img="monstrinho",
        cena=[
            "No fim do corredor norte havia uma porta que ninguém abria. Foi Nina quem contou, numa voz baixa, "
            "enquanto as três tigelas de sopa esfriavam:",
            "— Tem um espelho lá dentro. Dizem que ele mostra a vida que você teria se não tivesse recuado.",
            "Téo disse que era lenda. Íris foi lá naquela mesma noite.",
            "O espelho era alto, com moldura de madeira lascada, e a superfície não refletia o corredor: "
            "refletia uma mulher de cabelo mais curto, num terraço envidraçado, apontando uma planta baixa "
            "para três engenheiros. A mulher ria. Atrás dela, a cidade inteira acesa. Íris levou a mão à boca.",
            "— Bonita, não é? — disse a voz macia, agora fora dela, ao seu lado.",
            "Íris se virou. O que viu não era um monstro. Era uma figura de aparência confortável, quase "
            "simpática, do tamanho de uma criança, sentada numa poltrona que ela jurava não estar ali antes. "
            "Tinha o rosto tranquilo de quem nunca precisou correr.",
            "— Você sabe quem eu sou — disse a figura.",
            "— Não.",
            "— Sabe sim. Você me chama todos os dias. Eu sou o <b>Senhor do Nunca</b>. Nunca a sacada, nunca o "
            "elevador, nunca a obra, nunca a viagem. Eu te protejo de tudo isso. — Ele sorriu, e o sorriso era "
            "gentil de verdade, e isso era o pior. — Não sou seu inimigo, Íris. Sou seu seguro.",
            "— Por que você está engordando? — perguntou ela.",
            "O sorriso vacilou pela primeira vez.",
            "— Não sei do que você está falando.",
            "— Você era menor quando eu tinha vinte anos.",
            "Ele se recompôs, alisou o colete e disse, com uma doçura enregelante:",
            "— Eu cresço com o que você me dá. E você é muito generosa.",
        ],
        grimorio_tit="O ciclo que engorda o medo (e quem o alimenta)",
        grimorio=[
            "O Senhor do Nunca é a personificação de um processo mensurável. Ele engorda porque é alimentado "
            "com uma dieta específica: <b>evitação, fuga e comportamentos de segurança</b>.",
            "O ciclo tem cinco elos, e ele se fecha em segundos:",
            [
                "<b>Gatilho</b> — situação, imagem, pensamento ou sensação corporal.",
                "<b>Alarme</b> — ativação autonômica e previsão de catástrofe.",
                "<b>Evitação ou fuga</b> — sair, adiar, checar, só ir acompanhado, usar muletas.",
                "<b>Alívio imediato</b> — a ansiedade despenca em segundos; o cérebro registra recompensa.",
                "<b>Aumento do medo futuro</b> — a previsão catastrófica nunca é testada, então permanece intacta.",
            ],
            "O <b>Espelho de Nunca-Foi</b> tem função clínica: chama-se <i>custo da evitação</i>. Enquanto o "
            "sofrimento é medido apenas pela ansiedade sentida, fugir sempre parece o melhor negócio. Quando "
            "passamos a medir também a vida perdida — projetos, vínculos, papéis sociais, autoestima — a conta "
            "muda de sinal.",
            "Repare no diálogo: o vilão não mente. A esquiva realmente reduz o desconforto. É por isso que a "
            "TCC não tenta convencer ninguém de que fugir é ruim; ela organiza experiências em que <i>não "
            "fugir</i> se mostra, na prática, melhor.",
        ],
        feitico_tit="O Espelho de Duas Colunas",
        feitico_txt="Numa folha, coluna esquerda: “o que eu ganho ao evitar (hoje)”. Coluna direita: “o que "
                    "eu perco ao evitar (este ano)”. Guarde a folha e releia sempre que o Senhor do Nunca "
                    "parecer razoável.",
        pratica=[
            "1. Que cena aparece no meu Espelho de Nunca-Foi — a vida que eu teria sem a esquiva?",
            "2. Qual foi a última vez em que a fuga me pareceu “só bom senso”?",
        ],
    ),

    dict(
        cap=6, ato="ATO I — O CHAMADO",
        titulo="Os Sussurradores do corredor norte",
        epigrafe="“Eles não empurram ninguém. Eles só narram desastres.”",
        img=None,
        cena=[
            "Eles apareceram na manhã seguinte, e Íris entendeu por que ninguém andava sozinho pelo corredor "
            "norte. Não tinham corpo definido — eram como faixas de névoa cinzenta que se acomodavam nos "
            "ombros das pessoas e falavam no ouvido, muito baixinho, muito educadamente.",
            "<i>“E se você desmaiar na frente de todos?”</i>",
            "<i>“E se o vidro do terraço tiver uma trinca?”</i>",
            "<i>“Sentiu isso no peito? Não era assim ontem.”</i>",
            "— São os Sussurradores — explicou Barlovis, atravessando a névoa como quem atravessa fumaça de "
            "churrasco. — Não têm mãos. Não têm dentes. Só narram desastres com muita convicção. O erro que "
            "todo aprendiz comete é tentar calá-los discutindo.",
            "— E o que a gente faz? — perguntou Téo, encolhido.",
            "— Vocês agradecem e continuam andando.",
            "Barlovis pegou um pedaço de giz e escreveu na parede de pedra três palavras: <b>corpo</b>, "
            "<b>cabeça</b>, <b>pernas</b>.",
            "— O corpo acelera. A cabeça narra. As pernas fogem. É sempre esse trio. Enquanto vocês acharem "
            "que o problema é o corpo, vão passar a vida tentando controlar batimento cardíaco. Enquanto "
            "acharem que é a cabeça, vão passar a vida discutindo com névoa. O único elo que vocês controlam "
            "de verdade, hoje, agora, sem nenhum treino especial…",
            "Ele apontou para a terceira palavra.",
            "— …são as pernas.",
            "Íris olhou para os próprios pés. Depois olhou para o fim do corredor, a uns quinze metros. "
            "Os Sussurradores adensaram-se, ansiosos.",
            "Ela andou. Chegou ao fim. Não desmaiou. A névoa, atrás dela, pareceu um pouco mais fina.",
            "— Quantos passos? — perguntou Barlovis, do outro lado.",
            "— Vinte e três.",
            "— E quantas catástrofes?",
            "Íris abriu a boca para responder e percebeu, com um susto agradável, que a resposta era zero. "
            "Vinte e três passos, quatro previsões de desastre, nenhuma cumprida.",
            "— Anote isso — disse o mestre, entregando a ela um caderno pequeno de capa dura. — A partir de "
            "hoje, tudo o que eles prometerem que vai acontecer, você escreve de um lado. O que acontece de "
            "verdade, você escreve do outro. Em três semanas a gente lê os dois lados juntos.",
            "— E o que eu vou encontrar?",
            "— Não vou te contar. Se eu contar, é opinião minha. Se você descobrir, vira dado seu.",
        ],
        grimorio_tit="Os três eixos do sintoma fóbico",
        grimorio=[
            "A cena do corredor descreve com precisão a estrutura tríplice da resposta de medo, tal como "
            "avaliada na prática clínica:",
            [
                "<b>Eixo fisiológico (corpo):</b> taquicardia, aperto no peito, falta de ar, tontura, tremor, "
                "sudorese, boca seca, náusea, formigamento, tensão muscular, urgência urinária.",
                "<b>Eixo cognitivo (cabeça):</b> superestimação da probabilidade (“vai acontecer”), "
                "superestimação da gravidade (“seria insuportável”), subestimação da própria capacidade "
                "(“eu não dou conta”), imagens intrusivas de catástrofe, hipervigilância a sinais internos.",
                "<b>Eixo comportamental (pernas):</b> esquiva antecipatória, fuga, congelamento, checagem "
                "repetida, busca de reasseguramento, uso de muletas químicas ou humanas.",
            ],
            "A escolha estratégica de Barlovis — começar pelas pernas — reflete um princípio central da TCC: "
            "<b>o comportamento é a porta de entrada mais acessível do sistema</b>. Cognições e sensações são "
            "difíceis de alterar por vontade direta; ações são escolhíveis mesmo sob ansiedade alta.",
            "Sobre discutir com os Sussurradores: a tentativa de suprimir pensamentos intrusivos costuma "
            "aumentar sua frequência (efeito de reação paradoxal). A alternativa não é discutir nem obedecer — "
            "é <b>notar, nomear e seguir agindo</b>, estratégia que Barlow incorpora ao Protocolo Unificado "
            "como consciência emocional sem julgamento.",
        ],
        feitico_tit="Agradecer e Continuar Andando",
        feitico_txt="Ao ouvir a previsão catastrófica: “obrigada, cabeça, anotei” — e dê o próximo passo "
                    "físico. Você não precisa vencer a discussão para atravessar o corredor.",
        pratica=[
            "1. Escreva as três frases que os meus Sussurradores mais repetem:",
            "2. Qual é o menor passo físico que eu consigo dar hoje, mesmo ouvindo essas frases?",
        ],
    ),

    # ─────────────── ATO II — O APRENDIZADO ───────────────
    dict(
        cap=7, ato="ATO II — O APRENDIZADO",
        titulo="O mapa antigo do salão",
        epigrafe="“Dar nome não é rotular. É parar de lutar contra um fantasma sem forma.”",
        img=None,
        cena=[
            "No salão principal havia um mapa enorme pregado na parede, tão antigo que o papel amarelara nas "
            "bordas. Não era um mapa de terras: era um mapa de medos. Regiões desenhadas à mão, com nomes "
            "escritos em tinta preta e correções sobrepostas por várias gerações de mestres.",
            "— Cinquenta anos de observação cuidadosa — disse Barlovis, passando a mão pelo papel. — Cada "
            "linha aqui só foi desenhada depois que muita gente descreveu a mesma coisa, do mesmo jeito, em "
            "lugares diferentes do mundo. É assim que se faz um mapa que serve.",
            "— E o que ele diz de mim? — perguntou Íris.",
            "— Ele diz sete coisas. Preste atenção, porque a partir de hoje você vai reconhecer o seu inimigo "
            "pelo nome próprio.",
            "O mestre apontou para o primeiro selo do mapa, no canto superior esquerdo.",
            "— <i>Primeiro</i>: existe um medo intenso e persistente de uma coisa específica. Não de tudo. "
            "De uma coisa. No seu caso, altura. No do Téo, cães. <i>Segundo</i>: quando essa coisa aparece, o "
            "medo vem quase sempre, quase imediatamente — não é uma vez ou outra. <i>Terceiro</i>: você evita "
            "ativamente, ou suporta com muito sofrimento.",
            "Íris pensou nos seis lances de escada com a bolsa apertada contra o peito.",
            "— <i>Quarto</i>: o medo é desproporcional ao perigo real da situação. Não digo que altura não "
            "mata; digo que uma sacada com guarda-corpo de um metro e dez não mata. <i>Quinto</i>: isso dura "
            "meses — pelo menos seis. Não é o susto de uma semana ruim. <i>Sexto</i>: atrapalha sua vida de "
            "verdade — trabalho, afetos, planos. E <i>sétimo</i>: não é melhor explicado por outra coisa.",
            "— Que outra coisa? — perguntou Nina.",
            "— Muita gente chega aqui achando que tem fobia de elevador e na verdade tem pânico: teme as "
            "próprias sensações, não o elevador. Outros acham que têm fobia de festa e o que temem é o "
            "julgamento alheio. O tratamento muda conforme o nome. Por isso o mapa importa.",
            "Barlovis pegou um alfinete de cabeça vermelha e o entregou a Íris.",
            "— Marque o seu ponto. Sem drama e sem vergonha. Você não está sendo etiquetada: está sendo "
            "localizada. Ninguém traça uma rota sem saber de onde parte.",
            "Íris espetou o alfinete sobre a palavra <i>altura</i>. Foi menos doloroso do que ela imaginava. "
            "Na verdade, foi quase um alívio — o primeiro alívio, em anos, que não tinha sido oferecido pelo "
            "Senhor do Nunca.",
        ],
        grimorio_tit="Os critérios do DSM-5-TR para fobia específica",
        grimorio=[
            "O mapa do salão é o <b>DSM-5-TR</b>, manual da Associação Americana de Psiquiatria. Os sete "
            "selos apontados por Barlovis correspondem aos critérios diagnósticos:",
            [
                "<b>A.</b> Medo ou ansiedade acentuados acerca de um objeto ou situação específicos.",
                "<b>B.</b> O objeto ou situação quase invariavelmente provoca medo ou ansiedade imediatos.",
                "<b>C.</b> O objeto ou situação é ativamente evitado ou suportado com intensa ansiedade.",
                "<b>D.</b> O medo é desproporcional ao perigo real e ao contexto sociocultural.",
                "<b>E.</b> O quadro é persistente, tipicamente por seis meses ou mais.",
                "<b>F.</b> Causa sofrimento clinicamente significativo ou prejuízo funcional.",
                "<b>G.</b> Não é mais bem explicado por outro transtorno (pânico, agorafobia, ansiedade social, TOC, TEPT).",
            ],
            "O critério G merece atenção especial, porque muda a conduta clínica. Na <b>fobia específica</b>, o "
            "temido está fora: o cão, a agulha, o vão do elevador. No <b>transtorno de pânico</b>, o temido está "
            "dentro: as próprias sensações corporais e o que elas significariam. Na <b>ansiedade social</b>, o "
            "temido é a avaliação alheia. Tratar tudo como a mesma coisa é a receita mais comum de fracasso "
            "terapêutico.",
            "Diagnóstico bem feito não é rótulo: é orientação de rota. Ele indica qual protocolo aplicar, qual "
            "hierarquia montar e o que medir para saber se está funcionando.",
        ],
        feitico_tit="O Alfinete no Mapa",
        feitico_txt="Nomeie o seu medo com precisão cirúrgica. Não “sou ansiosa”, mas “tenho medo de estar a "
                    "mais de três andares do chão junto a superfícies de vidro”. Quanto mais específico o alvo, "
                    "mais preciso o treino.",
        pratica=[
            "1. Descreva o seu medo em uma frase específica (objeto, situação, condição):",
            "2. Quais dos sete critérios você reconhece em si? Escreva exemplos concretos:",
            "3. Há quanto tempo isso dura, e o que já atrapalhou na sua vida?",
        ],
    ),

    dict(
        cap=8, ato="ATO II — O APRENDIZADO",
        titulo="Os cinco corredores",
        epigrafe="“Portas diferentes, mesma dobradiça.”",
        img=None,
        cena=[
            "A ala oeste da Academia tinha cinco corredores que partiam de um mesmo saguão circular, como os "
            "dedos de uma mão.",
            "— Corredor dos Animais — anunciou Barlovis, apontando o primeiro. — Cães, aranhas, cobras, "
            "pombos, baratas, ratos. É o corredor mais cheio da casa e o mais antigo: nossos bisavós já "
            "tinham bons motivos para desconfiar de coisas que se mexem sozinhas.",
            "Téo levantou a mão, meio sem graça, e todos riram — inclusive ele.",
            "— Corredor do Ambiente Natural: alturas, tempestades, água funda, escuridão. É o seu, Íris. "
            "Corredor do Sangue, da Injeção e dos Ferimentos: agulhas, curativos, cirurgias, doação de sangue. "
            "Esse tem uma peculiaridade que nenhum outro tem, e a Nina conhece bem.",
            "— Eu desmaio — disse Nina, sem levantar os olhos.",
            "— Você desmaia — confirmou o mestre, com uma delicadeza que fez a moça enfim erguer o rosto. — "
            "E não é frescura, nem falta de treino: é um reflexo do seu corpo. Nos outros corredores a pressão "
            "sobe e fica alta. No seu, ela sobe e depois despenca. Por isso o seu treino é diferente do de "
            "todo mundo aqui. Você vai aprender a subir a pressão de propósito.",
            "— E os outros dois? — perguntou Íris.",
            "— Corredor Situacional: aviões, elevadores, túneis, pontes, trens, lugares fechados. E o "
            "corredor dos Outros: engasgo, vômito, sons altos, palhaços, máscaras, o que a vida inventar. — "
            "Barlovis abriu os braços. — Cinco corredores. Cinco portas. Mas reparem numa coisa.",
            "Ele apontou para o alto, onde as cinco passagens se encontravam no mesmo teto abobadado.",
            "— A dobradiça é a mesma. Em todos eles, o alarme dispara, a pessoa foge, o alívio ensina, o medo "
            "cresce. É por isso que a chave que abre o corredor da Nina abre também o seu. Muda a hierarquia, "
            "muda o ritmo, muda um detalhe técnico aqui e ali. Não muda o princípio.",
            "Íris passou a mão na parede do seu corredor. Estava frio, e cheirava a pedra molhada.",
            "— Quantos degraus até o fim?",
            "— Quantos você precisar. Nem um a menos, nem um a mais.",
        ],
        grimorio_tit="Os cinco especificadores — e por que a diferença importa",
        grimorio=[
            "O DSM-5-TR organiza a fobia específica em cinco especificadores. Eles não são categorias "
            "decorativas: orientam ajustes técnicos importantes no tratamento.",
            [
                "<b>Animal:</b> cães, aranhas, cobras, insetos, roedores, aves. Início tipicamente na infância.",
                "<b>Ambiente natural:</b> alturas, tempestades, água, escuro.",
                "<b>Sangue-injeção-ferimentos (BII):</b> resposta bifásica vasovagal, com risco de síncope. "
                "Exige a técnica de tensão aplicada (Öst) antes e durante a exposição.",
                "<b>Situacional:</b> aviões, elevadores, túneis, pontes, transporte público, espaços fechados.",
                "<b>Outros:</b> engasgo, vômito, sons intensos, personagens fantasiados, entre outros.",
            ],
            "A peculiaridade do subtipo BII é fisiológica e bem documentada: em vez do padrão simpático "
            "sustentado (pressão e frequência cardíaca elevadas), ocorre uma <b>resposta bifásica</b> — "
            "elevação inicial seguida de queda abrupta de pressão e bradicardia, podendo culminar em desmaio. "
            "Nesses casos, técnicas de relaxamento clássicas são contraindicadas durante a exposição, porque "
            "aprofundam a queda pressórica. O correto é o oposto: tensionar a musculatura.",
            "O que Barlovis chama de “dobradiça comum” é o mecanismo compartilhado: aquisição por "
            "condicionamento, manutenção por reforço negativo e extinção por exposição repetida com violação "
            "de expectativa. Mesmo princípio, aplicações distintas.",
        ],
        feitico_tit="Identificar o Corredor",
        feitico_txt="Descubra a qual subtipo o seu medo pertence. Se for sangue-injeção-ferimentos, "
                    "vá direto ao Apêndice D antes de qualquer exposição: o seu protocolo tem uma etapa "
                    "obrigatória a mais.",
        pratica=[
            "1. A qual dos cinco corredores pertence o meu medo principal?",
            "2. Tenho histórico de tontura ou desmaio diante do estímulo? (se sim, use o Apêndice D)",
            "3. Existe mais de um corredor na minha vida? Qual eu escolho enfrentar primeiro?",
        ],
    ),

    dict(
        cap=9, ato="ATO II — O APRENDIZADO",
        titulo="Os óculos de Mestre Bekhan",
        epigrafe="“Não é o abismo que assusta. É a lente com que você o mede.”",
        img=None,
        cena=[
            "Mestre Bekhan era baixo, meticuloso, e tinha uma oficina cheia de lentes penduradas em fios de "
            "náilon, como um moinho de vidro. Quando o vento entrava pela janela, tudo tilintava.",
            "— Prova de vista — disse ele, sem cerimônia, entregando a Íris um par de óculos de armação "
            "grossa. — Vá até a janela e olhe o pátio.",
            "Íris obedeceu. E recuou dois passos imediatamente: o pátio, três metros abaixo, parecia estar a "
            "trinta. O muro parecia mais baixo. As pedras, mais pontiagudas.",
            "— O que você viu?",
            "— Que eu ia cair.",
            "— Escreva a frase inteira. Do jeito que ela apareceu.",
            "Ela escreveu: <i>“Se eu chegar perto, eu vou perder o controle, cair e morrer, e todos vão ver.”</i>",
            "Bekhan pegou o papel, ajustou os próprios óculos e leu como quem examina um contrato.",
            "— Aqui tem quatro lentes empilhadas, moça. Uma que aumenta a <i>probabilidade</i>: você tratou "
            "como certo um evento que jamais aconteceu com você em vinte e nove anos. Uma que aumenta a "
            "<i>gravidade</i>: você saltou direto para a morte, pulando trinta desfechos intermediários. Uma "
            "que <i>encolhe você</i>: sumiu com a sua capacidade de segurar num corrimão, de recuar, de "
            "respirar. E uma de <i>plateia</i>: “todos vão ver” não tem nada a ver com altura, tem a ver com "
            "vergonha.",
            "Ele devolveu o papel com uma anotação na margem: <i>quatro lentes, nenhum fato</i>.",
            "— Vou tirar as lentes? — perguntou Íris.",
            "— Não. Eu não tiro lente de ninguém com argumento. Isso é conversa, e conversa perde para "
            "adrenalina. — Bekhan sorriu pela primeira vez. — Eu só te ensino a <i>ver que existem lentes</i>. "
            "Quem tira é a experiência, lá fora, no degrau. Meu trabalho é te dar a régua para você comparar, "
            "depois, o que a lente previu com o que a vida entregou.",
            "Ele pendurou o par de óculos de volta no fio, com cuidado, como quem guarda uma ferramenta "
            "perigosa.",
            "— A propósito: essa lente da plateia é a favorita do Senhor do Nunca. Ele adora quando a pessoa "
            "acha que o problema é altura, quando na verdade metade do problema é ser vista tremendo.",
        ],
        grimorio_tit="Distorções cognitivas e reestruturação: o que muda o quê",
        grimorio=[
            "As “lentes” de Bekhan são o que <b>Aaron T. Beck</b> descreveu como distorções no processamento "
            "da informação. Nas fobias, quatro operam quase sempre juntas:",
            [
                "<b>Superestimação da probabilidade:</b> tratar o improvável como iminente.",
                "<b>Catastrofização:</b> saltar direto ao pior desfecho, ignorando os intermediários.",
                "<b>Subestimação de recursos:</b> apagar da conta a própria capacidade de agir, pedir ajuda ou recuar.",
                "<b>Foco na avaliação alheia:</b> somar vergonha antecipada ao medo original.",
            ],
            "A recusa de Bekhan em “tirar as lentes com argumento” tem base empírica sólida. A reestruturação "
            "cognitiva isolada produz efeitos modestos nas fobias específicas; o que muda o prognóstico é a "
            "<b>exposição comportamental</b>. O papel do trabalho cognitivo é outro, e é indispensável: "
            "<i>explicitar a previsão</i> para que ela possa ser testada e, depois, confrontada com o "
            "resultado observado.",
            "Por isso a instrução é sempre escrever a previsão <b>antes</b>, em linguagem específica e "
            "falsificável (“vou desmaiar em até 5 minutos” em vez de “vai ser horrível”). Previsão vaga não "
            "pode ser refutada — e o que não pode ser refutado nunca perde força.",
        ],
        feitico_tit="A Lente Declarada",
        feitico_txt="Antes de cada degrau, escreva a previsão exata: o que vai acontecer, em quanto tempo e "
                    "com que intensidade. Depois compare com o que de fato ocorreu. A régua é o tratamento.",
        pratica=[
            "1. Escreva o pensamento automático mais frequente diante do seu medo:",
            "2. Quais das quatro lentes estão nele?",
            "3. Reescreva a previsão de forma específica e testável:",
        ],
    ),

    dict(
        cap=10, ato="ATO II — O APRENDIZADO",
        titulo="Os Grilhões de Conforto",
        epigrafe="“Nem toda corrente é feita para prender. Algumas são feitas para consolar.”",
        img=None,
        cena=[
            "Havia uma sala na Academia que parecia um brechó: prateleiras lotadas de objetos comuns, cada um "
            "com uma etiqueta de papel amarrada por barbante.",
            "Uma garrafinha de água. Um frasco de comprimidos vazio. Um par de fones de ouvido. Um terço. Uma "
            "pulseira de contas. Um bilhete com um número de telefone. Uma poltrona com marcas de dedos nos "
            "braços.",
            "— Bem-vindas ao depósito dos Grilhões de Conforto — disse Barlovis. — Cada objeto aqui pertenceu "
            "a alguém que jurava que só conseguia enfrentar a situação com ele.",
            "Íris sentiu o rosto quente. No bolso do casaco, os dedos dela estavam fechados em volta do "
            "próprio celular, com a tela aberta na conversa da irmã — aquela que ela ligava “só por precaução” "
            "sempre que precisava entrar num prédio alto.",
            "— Se ajuda, qual é o problema? — perguntou Téo.",
            "— Nenhum, no começo. Muletas ajudam a andar quando a perna está quebrada. O problema é quando a "
            "perna sara e a pessoa continua com a muleta: aí ela nunca descobre que já podia andar. — Barlovis "
            "pegou uma garrafinha da prateleira. — Quando você atravessa o corredor segurando isto e nada "
            "acontece, o que o seu cérebro aprende?",
            "— Que eu consegui — arriscou Nina.",
            "— Não. Ele aprende que <b>a garrafinha</b> conseguiu. E na próxima vez que você sair de casa sem "
            "ela, o medo volta inteirinho, com juros e correção.",
            "Íris tirou o celular do bolso e olhou para a tela por um tempo longo.",
            "— Eu não vou pedir que você jogue fora — disse o mestre, adivinhando. — Vou pedir que você faça "
            "uma lista, e que a gente vá soltando um de cada vez, na hora certa. Primeiro você aprende a subir "
            "com a muleta. Depois aprende a subir sem. Quem tira tudo no primeiro dia costuma cair — e quem "
            "cai feio, some.",
            "Ele amarrou uma etiqueta em branco no barbante e entregou a Íris.",
            "— Escreva o nome do seu. Sem julgamento. A gente devolve quando você não precisar mais dele para "
            "nada — e é sempre uma cerimônia bonita.",
        ],
        grimorio_tit="Comportamentos de segurança: a esquiva que se disfarça de estratégia",
        grimorio=[
            "Comportamentos de segurança são ações realizadas <i>dentro</i> da situação temida com a função de "
            "prevenir a catástrofe imaginada. Diferem da esquiva porque a pessoa <b>fica</b> — mas o efeito "
            "sobre o aprendizado é semelhante.",
            "O mecanismo é a <b>atribuição errada de segurança</b>: quando nada de ruim acontece, o desfecho "
            "benigno é creditado à muleta (“não caí porque estava segurando”), e não à ausência real de "
            "perigo. A crença central permanece intacta, e o medo retorna assim que o recurso não está "
            "disponível.",
            "Exemplos comuns na prática clínica:",
            [
                "Levar medicação ansiolítica no bolso “por precaução”, sem indicação de uso.",
                "Só entrar no elevador acompanhado, ou com o celular na mão em ligação aberta.",
                "Distração deliberada: fones em volume alto, olhos fechados, contar de trás para frente.",
                "Checagens repetidas (saída de emergência, pulso, sinal do celular, grades e travas).",
                "Álcool antes do evento; sentar sempre no corredor; ir sempre com a mesma pessoa.",
            ],
            "A retirada é <b>progressiva e planejada</b>, não abrupta. A literatura de exposição recomenda "
            "reduzir os recursos de segurança ao longo dos degraus (<i>fading</i>), garantindo que os últimos "
            "ensaios ocorram sem nenhuma muleta — é essa condição final que consolida a autoeficácia.",
        ],
        feitico_tit="A Etiqueta em Branco",
        feitico_txt="Liste todas as suas muletas e classifique de 1 a 5 pela dificuldade de abrir mão. "
                    "Solte da mais fácil para a mais difícil, uma por semana, registrando o que acontece.",
        pratica=[
            "1. Quais são as minhas muletas (objetos, pessoas, rituais, substâncias)?",
            "2. Qual delas eu consigo soltar já nesta semana?",
            "3. O que eu acredito que aconteceria sem ela? (previsão para testar)",
        ],
    ),

    dict(
        cap=11, ato="ATO II — O APRENDIZADO",
        titulo="A oficina de Mestre Volpo e a Escada de Prata",
        epigrafe="“Me dê um monstro e eu te devolvo dez degraus.”",
        img="escada",
        cena=[
            "A oficina ficava nos fundos, e cheirava a pinho recém-cortado. Mestre Volpo era um velho de mãos "
            "grossas que falava pouco e media muito.",
            "— O terraço do Edifício Aurora — disse Íris, entregando a ele a folha com o seu objetivo final. "
            "— Vinte e dois andares. Vidro dos dois lados.",
            "Volpo leu, coçou a barba e riu baixinho.",
            "— Isso não é um degrau. Isso é um penhasco. Ninguém sobe penhasco de uma vez; sobe quem já subiu "
            "quarenta degraus antes e nem percebeu que estava subindo.",
            "Ele pegou um pedaço de tábua e começou a serrar enquanto falava.",
            "— Um degrau bom tem três qualidades. <b>É específico</b>: não “lidar com altura”, mas “ficar dois "
            "minutos na sacada do segundo andar, com a mão no corrimão, olhando para frente”. <b>É repetível</b>: "
            "você consegue fazer hoje, amanhã e depois. E <b>é do tamanho certo</b>: se te dá zero de "
            "ansiedade, não ensina nada; se te dá dez, você foge e aprende que fugir salva. O ponto ideal fica "
            "entre quatro e sete.",
            "— E como eu sei em que altura serrar? — perguntou ela.",
            "— Você me diz. — Volpo apontou a serra para ela. — Eu não faço escada para ninguém. Eu faço "
            "<i>com</i>. Comece pelo topo, que é o que te trouxe aqui, e vá descendo até chegar em algo que "
            "você faria hoje, agora, sem discutir muito.",
            "Levaram duas horas. No fim, havia dez linhas escritas na tábua com lápis de carpinteiro. A "
            "primeira dizia: <i>“Olhar fotos aéreas da cidade por cinco minutos, sentada, sem fechar os olhos”</i>. "
            "A décima dizia: <i>“Apresentar o projeto de pé, no centro do terraço do Aurora, sem segurar em "
            "nada”</i>.",
            "Íris olhou para a linha número dez e sentiu o estômago descer.",
            "— Eu nunca vou chegar aí.",
            "— Provavelmente não hoje — concordou Volpo, sem levantar os olhos da tábua. — Mas você não vai "
            "chegar no dez. Você vai chegar no um. E depois no dois. O dez chega sozinho quando você não "
            "estiver olhando para ele.",
            "Ele entregou a tábua a ela, pesada como uma promessa.",
            "— A escada é sua. Quem manda nela é quem sobe.",
        ],
        grimorio_tit="A hierarquia de exposição: como se constrói uma escada que funciona",
        grimorio=[
            "A Escada de Prata é a <b>hierarquia de exposição gradual</b>, formalizada por <b>Joseph Wolpe</b> "
            "nos anos 1950 e refinada por décadas de pesquisa clínica. É o instrumento central do tratamento.",
            "Regras técnicas para construir a sua:",
            [
                "<b>Ancore o topo:</b> defina o objetivo funcional que te trouxe ao tratamento, em termos "
                "observáveis (o que você quer poder fazer).",
                "<b>Seja operacional:</b> cada degrau descreve situação, duração, distância e condições "
                "(sozinho ou acompanhado, com ou sem muleta).",
                "<b>Gradue por SUDS:</b> Unidades Subjetivas de Desconforto, de 0 a 10. Trabalhe na faixa de "
                "4 a 7 — desconforto suficiente para aprender, tolerável o bastante para permanecer.",
                "<b>Garanta repetibilidade:</b> um degrau que só pode ser feito uma vez por mês não treina nada.",
                "<b>Avance por critério, não por calendário:</b> suba quando o degrau atual cair "
                "consistentemente para 2 ou 3 em duas ou três repetições.",
            ],
            "A eficácia dessa abordagem é uma das mais bem estabelecidas da psicologia clínica. Metanálises "
            "de exposição in vivo para fobias específicas relatam tamanhos de efeito grandes frente a "
            "controles em lista de espera e a intervenções placebo (Wolitzky-Taylor et al., 2008), com ganhos "
            "mantidos em seguimentos de longo prazo.",
            "E há a razão pela qual Volpo não constrói a escada sozinho: participação ativa na definição dos "
            "degraus aumenta adesão, senso de controle e autoeficácia (Bandura, 1997) — três preditores "
            "consistentes de desfecho positivo.",
        ],
        feitico_tit="A Tábua dos Dez Degraus",
        feitico_txt="Escreva do degrau 10 (seu objetivo final) para o degrau 1 (o que você faria hoje). "
                    "Use o modelo do caderno no fim deste livro. Se o degrau 1 ainda assusta, corte-o ao meio.",
        pratica=[
            "1. Qual é o meu degrau 10 — o objetivo que me trouxe até aqui?",
            "2. Qual é o meu degrau 1 — algo que eu faria hoje, com SUDS entre 4 e 7?",
            "3. Que condições (tempo, companhia, distância) definem cada um deles?",
        ],
    ),

    dict(
        cap=12, ato="ATO II — O APRENDIZADO",
        titulo="O Feitiço do Sopro Lento",
        epigrafe="“O corpo tem acelerador e freio. Ninguém te ensinou onde fica o freio.”",
        img="velinha",
        cena=[
            "O primeiro degrau de Íris foi cumprido numa terça-feira à tarde: cinco minutos olhando fotos "
            "aéreas da cidade, sentada, sem fechar os olhos. Ela chegou ao quarto minuto e trinta e teve "
            "vontade de virar o rosto. Não virou.",
            "Quando terminou, as mãos tremiam.",
            "— Isso é bom sinal — disse Barlovis, acendendo uma vela sobre a mesa da cozinha. — Significa que "
            "não foi fácil demais. Agora venha cá: você vai aprender onde fica o freio.",
            "— Freio?",
            "— Você conhece muito bem o acelerador. Quando o alarme toca, seu corpo pisa fundo: coração, "
            "respiração, músculos. Isso é o sistema simpático. — Ele empurrou a vela até o centro da mesa. — "
            "O que quase ninguém aprende é que existe um pedal do outro lado, e ele é acionado de um jeito "
            "ridiculamente simples: <b>expirando devagar</b>.",
            "— Só isso?",
            "— Só isso, e não é pouco. Puxe o ar pelo nariz contando até quatro, como quem cheira uma laranja "
            "cortada. Depois solte pela boca contando até seis, como quem quase apaga esta vela sem apagar. "
            "A chama tem que se inclinar e continuar acesa. Faça dez vezes.",
            "Íris fez. Na terceira respiração, a chama se inclinou de leve e voltou. Na sétima, ela percebeu "
            "que as mãos tinham parado de tremer.",
            "— Agora a parte importante, e preste muita atenção — disse Barlovis, e o tom dele mudou. — Este "
            "feitiço tem um uso certo e um uso errado. O uso certo é <i>ficar</i>: você respira para conseguir "
            "permanecer no degrau. O uso errado é <i>sumir</i>: respirar desesperadamente para não sentir "
            "nada, com os olhos fechados, contando os segundos até acabar.",
            "— Qual é a diferença? O resultado não é o mesmo?",
            "— A diferença é tudo. No primeiro caso, você está presente e o seu cérebro aprende que a situação "
            "é segura. No segundo, você está fugindo por dentro, e quem come essa refeição é ele.",
            "Íris não precisou perguntar quem.",
        ],
        grimorio_tit="Respiração lenta: fisiologia, uso correto e a armadilha da esquiva sutil",
        grimorio=[
            "A respiração diafragmática com expiração prolongada é um recurso de <b>regulação autonômica</b>. "
            "A expiração lenta aumenta o tônus vagal, ativa barorreceptores e reduz a frequência cardíaca; "
            "além disso, corrige a hipocapnia (queda de CO₂) provocada pela hiperventilação, responsável por "
            "tontura, formigamento e sensação de irrealidade.",
            "Protocolo prático (cadência 4-6):",
            [
                "Inspire pelo nariz por 4 segundos, deixando o abdome expandir.",
                "Expire pela boca por 6 segundos, de forma contínua e sem forçar.",
                "Repita por 8 a 12 ciclos, mantendo os olhos abertos e o foco no ambiente real.",
            ],
            "A advertência de Barlovis é tecnicamente importante e frequentemente ignorada. Se a respiração "
            "for usada para <b>suprimir</b> a experiência emocional, ela se transforma em comportamento de "
            "segurança: a pessoa atribui o desfecho benigno à técnica (“só não desmaiei porque respirei"
            " certo”) e a crença de perigo permanece intacta.",
            "A distinção prática: use a respiração para <i>entrar e permanecer</i>, não para <i>anestesiar</i>. "
            "No modelo de aprendizado inibitório (Craske et al., 2014), tolerar alguma ativação durante a "
            "exposição não prejudica o resultado — e pode até fortalecê-lo.",
        ],
        feitico_tit="O Sopro da Velinha (4-6)",
        feitico_txt="Inspire em 4, expire em 6, olhos abertos, dez ciclos. Use antes e durante o degrau — "
                    "para ficar, nunca para desaparecer.",
        pratica=[
            "1. Pratique 10 ciclos agora e anote a ansiedade antes e depois (0 a 10):",
            "2. Em que situação do meu dia eu posso treinar isso preventivamente?",
            "3. Como eu vou perceber se estou usando a respiração para fugir em vez de para ficar?",
        ],
    ),

    dict(
        cap=13, ato="ATO II — O APRENDIZADO",
        titulo="O Lago Gelado da Permanência",
        epigrafe="“A água não esquentou. Você é que ficou.”",
        img="piscina",
        cena=[
            "O lago ficava atrás do pomar, e era gelado até em janeiro. Barlovis levou os três até a margem "
            "numa manhã de neblina, com uma prancheta na mão e um cronômetro pendurado no pescoço.",
            "— Ninguém vai ser empurrado — disse, antes que Téo perguntasse. — Entrem até a cintura, se "
            "quiserem entrar. E fiquem. Eu só vou pedir uma coisa: a cada minuto, vocês me dizem um número de "
            "zero a dez.",
            "Íris entrou. O choque foi tão grande que ela riu, uma risada aguda e involuntária.",
            "— Nove! — gritou.",
            "Anotado. Um minuto depois: oito. Dois minutos: sete. Aos quatro minutos, ela disse cinco e "
            "franziu a testa, desconfiada. Aos sete, disse três e olhou para as próprias mãos dentro da água, "
            "como quem procura um truque.",
            "— A água esquentou? — perguntou Barlovis, sem levantar os olhos da prancheta.",
            "— Não pode ter esquentado.",
            "— Não esquentou. Está exatamente na mesma temperatura de quando você entrou. — Ele virou a "
            "prancheta e mostrou a curva desenhada: uma linha que subia rápido, fazia um pico e descia sozinha, "
            "sem que ninguém fizesse nada. — O que mudou foi você. Isso se chama habituação, e é a coisa mais "
            "barata que a natureza te deu.",
            "Nina, ainda na margem com os pés na água, perguntou o que todos queriam perguntar:",
            "— E se a gente sair no minuto dois?",
            "— Aí você leva para casa o número oito. E amanhã, quando pensar no lago, o seu cérebro vai "
            "consultar o arquivo e encontrar oito. — Barlovis fechou o cronômetro. — Quem sai no pico ensina "
            "ao cérebro que o pico era o fim da história. Quem fica descobre que o pico era o meio.",
            "Íris ficou mais três minutos. Quando saiu, tremendo de frio e rindo à toa, teve uma sensação "
            "estranha e nova, que levaria semanas para nomear: não era coragem. Era competência.",
        ],
        grimorio_tit="Habituação: a curva que ninguém vê porque foge antes",
        grimorio=[
            "A curva desenhada na prancheta é o achado clínico mais replicado da terapia de exposição: mantida "
            "a permanência no estímulo, sem fuga e sem muletas, a resposta de ansiedade <b>sobe, atinge um "
            "pico e declina espontaneamente</b>.",
            "Isso ocorre por razões fisiológicas objetivas: a resposta adrenérgica é metabolicamente "
            "autolimitada, o sistema parassimpático entra em ação compensatória e a novidade do estímulo "
            "diminui a cada repetição (habituação intra e entre sessões).",
            "O problema clínico não é a curva — é o ponto em que a pessoa sai. Quem escapa no pico:",
            [
                "Registra o valor mais alto como se fosse o desfecho final da experiência.",
                "Recebe reforço negativo imediato pela fuga, fortalecendo a esquiva futura.",
                "Impede a coleta do dado que refutaria a crença (“a ansiedade cresce até me destruir”).",
            ],
            "Recomendação prática: permaneça até que a ansiedade caia pelo menos <b>40 a 50% do pico</b>, ou "
            "até que você consiga fazer algo que não conseguiria fazer no início (falar, olhar, soltar a mão "
            "do corrimão). Registre os números a cada minuto — o gráfico é terapêutico por si só, porque "
            "transforma sensação em dado.",
        ],
        feitico_tit="A Curva Anotada",
        feitico_txt="Durante o degrau, marque sua ansiedade a cada minuto. Só saia quando o número tiver "
                    "caído de forma consistente — e nunca no pico.",
        pratica=[
            "1. Na minha última exposição, qual foi o pico e quanto tempo até começar a cair?",
            "2. Em que minuto eu costumo desistir — e o que costuma acontecer logo depois?",
            "3. Qual critério de saída eu vou adotar a partir de agora?",
        ],
    ),

    dict(
        cap=14, ato="ATO II — O APRENDIZADO",
        titulo="O Pergaminho da Predição",
        epigrafe="“O que cura não é a calma. É a surpresa.”",
        img=None,
        cena=[
            "Mestra Kraskia era a mais nova dos mestres e a única que corrigia Barlovis em público.",
            "— Com licença, diretor, mas o senhor está vendendo a habituação como se ela fosse o motor — disse "
            "ela, entrando na aula sem bater. — Ela é o passageiro. O motor é outro.",
            "Ela virou-se para os três aprendizes e desenrolou sobre a mesa um pergaminho dividido em duas "
            "colunas. Na primeira estava escrito <b>O QUE EU PREVI</b>. Na segunda, <b>O QUE ACONTECEU</b>.",
            "— Íris. Antes de entrar no lago, o que você previu?",
            "— Que eu não ia aguentar mais de dois minutos.",
            "— E?",
            "— Fiquei dez.",
            "— Escreva. — Kraskia empurrou a pena. — Não escreva “fui bem”. Escreva os dois números, lado a "
            "lado. A distância entre eles é o remédio.",
            "Íris escreveu: <i>previ 2 minutos — fiquei 10</i>.",
            "— É isto que reconfigura o cérebro — disse a mestra, batendo o dedo na coluna da direita. — Não "
            "é ficar calmo. Não é gostar. É a <b>discrepância</b>. O seu cérebro fez uma aposta e perdeu; toda "
            "vez que ele perde uma aposta dessas, ele é obrigado a atualizar o mapa.",
            "— E se eu previr certo? — perguntou Téo. — Se eu previr que vou passar mal e passar mal?",
            "— Então a gente ajusta o degrau, porque ele estava alto demais. Mas repare no que quase sempre "
            "acontece: as pessoas preveem catástrofes com detalhes cinematográficos, e o que acontece é "
            "desconforto. Desconforto não é catástrofe. Anotar essa diferença mil vezes é o trabalho.",
            "Antes de sair, Kraskia deixou uma última instrução, e Íris a copiaria na primeira página do "
            "próprio caderno:",
            "— Varie tudo. Horário, lugar, companhia, ordem dos degraus. Cérebro que só treina numa sala "
            "aprende que aquela sala é segura. A gente não quer isso. A gente quer que ele aprenda que "
            "<i>você</i> é segura, em qualquer sala.",
        ],
        grimorio_tit="Aprendizado inibitório: por que a violação de expectativa é o motor",
        grimorio=[
            "O modelo contemporâneo da exposição, desenvolvido por <b>Michelle Craske</b> e colaboradores "
            "(2014), reposicionou o mecanismo terapêutico. A redução da ansiedade dentro da sessão "
            "(habituação) é um <i>correlato</i>, não o ingrediente ativo. O ingrediente ativo é a "
            "<b>violação de expectativa</b>: a discrepância entre o desfecho previsto e o observado.",
            "A extinção não apaga a memória de medo original. Ela cria uma <b>memória inibitória</b> nova, "
            "mediada por circuitos pré-frontais, que compete com a antiga. Por isso o medo pode reaparecer "
            "com o tempo, com a mudança de contexto ou após estresse — e por isso a forma como se treina "
            "importa tanto.",
            "Estratégias que fortalecem o aprendizado inibitório:",
            [
                "<b>Explicitar a previsão</b> antes e conferi-la depois, sempre por escrito.",
                "<b>Variar contextos</b>: locais, horários, companhias, condições.",
                "<b>Espaçar as repetições</b> ao longo dos dias, permitindo consolidação (inclusive durante o sono).",
                "<b>Remover pistas de segurança</b> nos ensaios finais.",
                "<b>Combinar estímulos</b> e alternar níveis de dificuldade, em vez de subir em linha reta.",
                "<b>Tolerar a ansiedade</b> durante a tarefa em vez de tentar zerá-la.",
            ],
            "Consequência prática: o registro escrito não é burocracia terapêutica. É o instrumento que "
            "produz o efeito.",
        ],
        feitico_tit="O Pergaminho de Duas Colunas",
        feitico_txt="Antes: “o que eu prevejo”. Depois: “o que aconteceu”. Guarde todos. Em três semanas, "
                    "releia a pilha inteira de uma vez — é aí que a ficha cai.",
        pratica=[
            "1. Previsão para o meu próximo degrau (específica, com número e tempo):",
            "2. O que realmente aconteceu:",
            "3. Como eu vou variar contexto, horário e companhia nas próximas repetições?",
        ],
    ),

    # ─────────────── ATO III — AS PROVAS ───────────────
    dict(
        cap=15, ato="ATO III — AS PROVAS",
        titulo="O filhote do pátio oeste",
        epigrafe="“Coragem não é o que se sente. É o que se faz com as pernas.”",
        img="cachorrinho",
        cena=[
            "O cão se chamava Bento, tinha quatro quilos, orelhas grandes demais para a cabeça e dormia "
            "dezoito horas por dia. Para Téo, era um lobo.",
            "A escada dele tinha sido serrada por Volpo em degraus tão finos que Íris achou graça no começo: "
            "olhar foto de cachorro; ver vídeo de cachorro; ficar na mesma sala com Bento dormindo, a dez "
            "metros, com a porta aberta; oito metros; cinco; três.",
            "Naquela manhã, o degrau era: <i>sentar-se a um metro de Bento acordado, por cinco minutos, sem "
            "sair da cadeira</i>.",
            "Téo sentou. Bento levantou a cabeça, olhou para ele com o desinteresse absoluto de quem já viu "
            "muita gente tremer, bocejou e deitou de novo. Téo, no entanto, estava branco.",
            "— Número? — perguntou Barlovis.",
            "— Nove.",
            "— Previsão?",
            "— Que ele vai pular em mim e me morder o rosto.",
            "— Anotado. Cinco minutos.",
            "No terceiro minuto, Téo estava em sete. No quinto, em cinco. No sétimo — porque ele mesmo pediu "
            "para ficar mais dois — estava em quatro, e disse, com a voz meio embargada:",
            "— Ele não fez nada. Ele nem me olhou direito.",
            "— Escreva as duas colunas — disse Kraskia, da porta.",
            "Téo escreveu: <i>previ ataque ao rosto em 5 minutos — recebi um bocejo</i>. E então aconteceu uma "
            "coisa que ninguém esperava: ele começou a rir. Um riso incontrolável, quase choro, com o corpo "
            "todo tremendo.",
            "— Dez anos — disse ele, enxugando o rosto. — Dez anos atravessando a rua por causa disso.",
            "Íris olhou para o amigo e sentiu, pela primeira vez desde que chegara, uma esperança concreta, "
            "quase grosseira de tão física: se aquilo tinha funcionado com o Téo, o mesmo mecanismo — o mesmo, "
            "exatamente o mesmo — funcionaria com ela.",
            "Foi nesse dia que ela parou de dizer “vou tentar” e começou a dizer “vou subir”.",
        ],
        grimorio_tit="Exposição in vivo, modelação e o valor de assistir alguém atravessar",
        grimorio=[
            "A cena de Téo reúne três mecanismos terapêuticos, todos bem documentados.",
            "<b>Exposição in vivo graduada:</b> contato real com o estímulo temido, em passos ordenados por "
            "SUDS, com permanência suficiente e sem fuga. É o padrão-ouro para fobias de animais, com taxas "
            "de resposta que chegam a 80–90% em protocolos bem conduzidos.",
            "<b>Violação de expectativa:</b> a previsão (“ataque ao rosto”) foi explicitada antes e refutada "
            "por dados observáveis (“um bocejo”). O riso incontrolável de Téo é uma reação comum e descrita "
            "clinicamente após uma discrepância grande — é o sistema recalibrando de uma vez.",
            "<b>Aprendizagem vicária:</b> Íris melhorou assistindo. <b>Albert Bandura</b> demonstrou que "
            "observar alguém semelhante enfrentando com sucesso aumenta a expectativa de autoeficácia do "
            "observador e reduz sua própria esquiva. Esse é um dos motivos pelos quais grupos terapêuticos e "
            "relatos de pacientes reais têm efeito clínico, e não apenas motivacional.",
            "Nota prática sobre fobia de animais: o treino nunca deve envolver contenção do animal contra sua "
            "natureza, sustos ou aproximação forçada. O animal precisa ser previsível, dócil e supervisionado "
            "— caso contrário, o risco real deixa de ser desprezível e o aprendizado se inverte.",
        ],
        feitico_tit="A Testemunha",
        feitico_txt="Assista a alguém parecido com você atravessando o que você teme — de perto, em vídeo ou "
                    "em relato detalhado. Depois escreva: “se funcionou com ele, o mecanismo é o mesmo comigo”.",
        pratica=[
            "1. Quem, na minha vida ou em relatos que eu conheça, já atravessou algo parecido?",
            "2. Que previsão minha já foi refutada por dados na última semana?",
            "3. Qual degrau eu subo hoje, mesmo que a sensação não mude nada?",
        ],
    ),

    dict(
        cap=16, ato="ATO III — AS PROVAS",
        titulo="A agulha de prata de Nina",
        epigrafe="“Para quem desmaia, relaxar é o conselho errado.”",
        img=None,
        cena=[
            "Nina era enfermeira havia seis anos e nunca tinha conseguido aplicar uma injeção sem se apoiar "
            "na maca. Duas vezes desmaiara em serviço. Na terceira, pediu transferência para a recepção e "
            "chorou no vestiário por uma hora.",
            "— Comigo é diferente, não é? — perguntou ela a Mestre Ostrom, um homem calvo de sotaque "
            "arrastado que cuidava da enfermaria da Academia.",
            "— É. E o pior conselho que já te deram foi “relaxa”.",
            "Ele explicou desenhando duas curvas no quadro. A primeira subia e se mantinha alta: o padrão de "
            "quase todo mundo. A segunda subia, e depois despencava abaixo da linha de base.",
            "— A sua pressão faz isso. Sobe, e cai. Quando cai demais, o cérebro fica sem irrigação suficiente "
            "e você apaga. Se, no meio dessa queda, alguém te manda relaxar e respirar fundo… você acelera o "
            "desmaio.",
            "— Então o que eu faço?",
            "— O contrário. Você <b>tensiona</b>.",
            "Ostrom a fez sentar-se numa cadeira firme e ensinou o exercício: contrair braços, tronco e pernas "
            "com força por quinze segundos, até sentir o calor subir ao rosto; soltar por vinte segundos, sem "
            "amolecer completamente; repetir cinco vezes.",
            "— Faça isso cinco vezes antes, e continue fazendo durante. Você vai sustentar a pressão na mão "
            "que o seu corpo quer deixar cair.",
            "Levaram nove dias. No décimo, Nina aplicou uma injeção de soro em uma laranja, depois em um "
            "simulador de braço, depois observou Ostrom coletar sangue de Íris — que se ofereceu sem pensar "
            "duas vezes e depois passou uma hora comemorando o próprio gesto.",
            "No décimo quarto dia, Nina fez uma coleta de verdade, num voluntário da cidade, com as pernas "
            "duras de tanto tensionar e o rosto quente.",
            "Não desmaiou.",
            "Guardou a seringa na bandeja, tirou as luvas com um estalo, olhou para as próprias mãos firmes e "
            "disse, com uma calma que assustou a todos:",
            "— Eu quero voltar para a emergência.",
        ],
        grimorio_tit="Tensão aplicada: o protocolo específico para o subtipo sangue-injeção-ferimentos",
        grimorio=[
            "A fobia de sangue-injeção-ferimentos (BII) é a exceção fisiológica entre as fobias específicas. "
            "Em vez da ativação simpática sustentada, ocorre uma <b>resposta bifásica vasovagal</b>: elevação "
            "inicial de frequência cardíaca e pressão arterial, seguida de queda abrupta, com bradicardia, "
            "palidez, náusea, sudorese fria e possível síncope.",
            "Por isso, técnicas de relaxamento e respiração lenta — úteis em outros subtipos — são "
            "<b>contraindicadas durante a exposição</b> nesses casos: aprofundam a hipotensão.",
            "O tratamento de escolha é a <b>tensão aplicada</b> (<i>applied tension</i>), desenvolvida por "
            "<b>Lars-Göran Öst</b>:",
            [
                "Sentar-se em posição estável e segura.",
                "Contrair vigorosamente a musculatura de braços, tronco e pernas por 10 a 15 segundos, até "
                "sentir calor no rosto (sem prender a respiração).",
                "Liberar a tensão por cerca de 20 segundos, sem relaxamento profundo.",
                "Repetir 5 ciclos, várias vezes ao dia, durante o treino.",
                "Aplicar os ciclos imediatamente antes e durante a exposição real (coleta, vacina, curativo).",
            ],
            "A manobra eleva transitoriamente a pressão arterial e mantém a perfusão cerebral, prevenindo a "
            "síncope. Combinada à exposição gradual, apresenta resultados robustos e frequentemente rápidos — "
            "há protocolos eficazes conduzidos em poucas sessões.",
            "Implicação prática: quem tem histórico de desmaio precisa aprender a tensão aplicada <b>antes</b> "
            "de iniciar qualquer degrau que envolva sangue, agulhas ou procedimentos.",
        ],
        feitico_tit="A Tensão que Sustenta",
        feitico_txt="Contraia todo o corpo por 15 segundos, solte por 20, cinco vezes. Antes e durante o "
                    "procedimento. É o oposto de relaxar — e é exatamente o que o seu corpo precisa.",
        pratica=[
            "1. Eu já tive tontura, palidez ou desmaio diante de sangue ou agulhas? Em que situações?",
            "2. Pratique 5 ciclos de tensão aplicada agora e descreva o que sentiu:",
            "3. Qual será o meu primeiro degrau deste corredor (foto, vídeo, simulador, acompanhamento)?",
        ],
    ),

    dict(
        cap=17, ato="ATO III — AS PROVAS",
        titulo="A recaída",
        epigrafe="“Ele não voltou porque você falhou. Ele voltou porque é assim que ele funciona.”",
        img="monstrinho",
        cena=[
            "Íris estava no degrau sete — <i>ficar cinco minutos na varanda do oitavo andar, sem segurar em "
            "nada</i> — quando tudo desandou.",
            "Foi uma sexta-feira. Ela tinha dormido mal, discutido com a irmã ao telefone e pulado o almoço. "
            "Subiu assim mesmo, com pressa, sem escrever a previsão, sem anotar o número. No terceiro minuto, "
            "uma rajada de vento bateu na lona da obra vizinha e fez um estalo alto.",
            "O corpo de Íris entendeu aquilo como queda.",
            "Ela agarrou o batente, desceu os oito andares pela escada sem parar, sentou no meio-fio e ficou "
            "quinze minutos com a cabeça entre os joelhos, ouvindo aquela voz — que andava tão magra nas "
            "últimas semanas — falar mais gorda do que nunca.",
            "— Viu? Você estava indo bem <i>porque eu deixei</i>. Volte para o degrau um. Volte para casa. "
            "Você não é dessas pessoas que sobem.",
            "Naquela noite, Íris não jantou com os outros. Ficou no dormitório com a tábua de Volpo no colo, "
            "olhando para as dez linhas e sentindo um cansaço antigo, do tipo que argumenta bem.",
            "Barlovis bateu na porta às onze e sentou-se no chão, de costas para a parede.",
            "— Sabe o que aconteceu hoje? — perguntou ele.",
            "— Eu voltei à estaca zero.",
            "— Não. Aconteceu <b>exatamente o que a ciência prevê que aconteça</b>. — Ele disse isso sem "
            "nenhuma dramaticidade, como quem lê a previsão do tempo. — Sono ruim, estômago vazio, estresse "
            "prévio, contexto novo, estímulo inesperado. Cinco fatores de risco no mesmo dia. Se você tivesse "
            "<i>não</i> se assustado, aí sim eu ficaria preocupado.",
            "— Eu desci correndo.",
            "— Desceu. E é isso que a gente vai consertar amanhã: não a queda, a descida. — Ele se levantou e "
            "parou na porta. — Recaída não apaga aprendizado. A memória nova continua aí; ela só perdeu uma "
            "disputa hoje, num dia em que estava com fome e sem dormir.",
            "— E se acontecer de novo?",
            "— Vai acontecer de novo. E de novo. Cada vez menor, cada vez mais curta, cada vez com menos "
            "poder de te convencer. O nome disso não é fracasso. É <b>a forma</b> como as pessoas melhoram.",
        ],
        grimorio_tit="Retorno do medo: renovação, reinstauração e recuperação espontânea",
        grimorio=[
            "A recaída de Íris não é falha de tratamento nem de caráter: é um fenômeno previsto pelo modelo "
            "de aprendizado inibitório. Como a extinção cria uma memória <i>nova</i> que compete com a antiga "
            "(em vez de apagá-la), o medo pode retornar em condições específicas:",
            [
                "<b>Renovação:</b> reencontro com o estímulo em um contexto diferente daquele em que se treinou.",
                "<b>Reinstauração:</b> ocorrência de um evento aversivo inesperado (o estalo, um susto real).",
                "<b>Recuperação espontânea:</b> reaparecimento após um período longo sem contato.",
                "<b>Estados de vulnerabilidade:</b> privação de sono, jejum, doença, estresse agudo, uso de álcool.",
            ],
            "Três consequências práticas, todas presentes na conversa do capítulo:",
            [
                "<b>Não treine em estado de alta vulnerabilidade</b> sem ajustar o degrau para baixo.",
                "<b>Trate a fuga, não o susto.</b> O evento clinicamente relevante não foi o medo — foi a "
                "descida correndo, que reforçou a esquiva.",
                "<b>Retome rápido.</b> A recomendação técnica após um episódio de fuga é voltar ao estímulo em "
                "até 24–48 horas, num degrau ligeiramente mais fácil, e completar a permanência.",
            ],
            "Normalizar o retorno do medo antes que ele aconteça reduz a chance de abandono do tratamento. "
            "Quem espera uma linha reta interpreta o primeiro tropeço como prova de que “não funciona”.",
        ],
        feitico_tit="O Protocolo do Tropeço",
        feitico_txt="Fugiu? Anote o que aconteceu sem julgamento, identifique os fatores de vulnerabilidade "
                    "do dia e volte em até 48 horas, um degrau abaixo, para completar. Tropeço não desfaz "
                    "escada.",
        pratica=[
            "1. Quais fatores costumam me deixar mais vulnerável (sono, fome, estresse, álcool, contexto novo)?",
            "2. Qual foi a minha última fuga e o que a antecedeu?",
            "3. Qual é o meu plano de retomada em 48 horas?",
        ],
    ),

    dict(
        cap=18, ato="ATO III — AS PROVAS",
        titulo="A noite em que Íris quis desistir",
        epigrafe="“Coragem não é uma fogueira. É uma fila de fósforos.”",
        img=None,
        cena=[
            "A mala estava pronta às cinco da manhã.",
            "Íris desceu com ela pelo corredor norte, e os Sussurradores vieram todos, animados como cães em "
            "hora de passeio: <i>você não é dessas pessoas; você perdeu tempo; vão rir de você; volte para a "
            "sua vida pequena, ela é confortável</i>.",
            "No saguão, encontrou Mestra Bandurá acendendo o fogão a lenha. Ela não olhou para a mala.",
            "— Antes de ir, me ajuda com uma conta? — pediu, apontando um caderno aberto sobre a mesa. — "
            "Estou fechando os registros da semana e me perdi.",
            "Íris se aproximou, contrariada. Era o caderno dela mesma.",
            "— Dia três: você olhou fotos aéreas por cinco minutos e previu que não aguentaria dois. Dia seis: "
            "sacada do segundo andar, dois minutos, previu tontura, não teve. Dia nove: quarto andar, cinco "
            "minutos, soltou a mão do corrimão por trinta segundos. Dia doze: quinto andar, sem o celular no "
            "bolso. Dia quinze: sexto andar, sozinha, sem avisar ninguém antes. — Bandurá levantou os olhos. "
            "— São dezenove entradas em vinte e um dias. Quantas dessas você teria dado como certas há um mês?",
            "Íris não respondeu.",
            "— A sexta-feira em que você desceu correndo está aqui também. Uma linha, entre dezenove. — A "
            "mestra fechou o caderno. — Você não está desistindo porque fracassou. Está desistindo porque a "
            "sua memória é seletiva quando está cansada. A dor pesa mais na balança que dezenove vitórias — "
            "e é por isso que a gente escreve.",
            "— Eu não sinto que sou capaz — disse Íris, e a voz saiu menor do que ela queria.",
            "— Sentimento não é dado. — Bandurá puxou uma cadeira e sentou. — E capacidade não se descobre "
            "sentindo, se descobre fazendo. Cada degrau cumprido acende um fósforo. Um fósforo sozinho não "
            "ilumina nada. Dezenove fósforos, um atrás do outro, iluminam a colina inteira. Você chegou aqui "
            "com zero. Tem dezenove no bolso.",
            "Íris ficou muito tempo em silêncio, com a mão na alça da mala.",
            "Depois soltou a alça.",
            "— O que tem no degrau oito? — perguntou.",
        ],
        grimorio_tit="Autoeficácia, viés de negatividade e por que o registro escrito é indispensável",
        grimorio=[
            "<b>Albert Bandura</b> definiu autoeficácia como a crença na própria capacidade de executar as "
            "ações necessárias para produzir um resultado. Não é autoestima nem otimismo: é uma estimativa "
            "específica, tarefa a tarefa — e é um dos preditores mais consistentes de desfecho em terapia de "
            "exposição.",
            "As quatro fontes de autoeficácia, todas presentes nesta história:",
            [
                "<b>Experiências de domínio</b> — os degraus cumpridos. É a fonte mais poderosa.",
                "<b>Aprendizagem vicária</b> — ver Téo e Nina atravessarem.",
                "<b>Persuasão verbal</b> — o mestre que aponta dados reais, não elogios vazios.",
                "<b>Estados fisiológicos e afetivos</b> — aprender a interpretar a ativação corporal como "
                "esforço, não como fracasso iminente.",
            ],
            "O movimento de Bandurá — mostrar o caderno em vez de argumentar — corrige um viés cognitivo "
            "conhecido: sob cansaço e afeto negativo, a recuperação de memórias congruentes com o humor é "
            "facilitada. Uma única falha recente fica mais disponível na memória do que dezenove êxitos.",
            "É por isso que o registro escrito tem função clínica dupla: gera a violação de expectativa "
            "(Craske) e produz um <b>arquivo objetivo de evidências</b> contra o desânimo. Em momentos de "
            "desistência, o caderno é o único interlocutor que não depende de como você está se sentindo.",
        ],
        feitico_tit="A Fila de Fósforos",
        feitico_txt="Ao fim de cada dia de treino, escreva uma linha com a data e o que você fez. Quando "
                    "pensar em desistir, leia a lista inteira em voz alta antes de decidir.",
        pratica=[
            "1. Liste todas as suas vitórias desde o início, mesmo as mínimas:",
            "2. Que evidência concreta contradiz a frase “eu não sou capaz”?",
            "3. O que eu diria a um amigo que estivesse na minha situação hoje?",
        ],
    ),

    dict(
        cap=19, ato="ATO III — AS PROVAS",
        titulo="A biblioteca dos retratos vivos",
        epigrafe="“Você não está inventando o caminho. Está caminhando por uma estrada calçada por muita gente.”",
        img=None,
        cena=[
            "A biblioteca ocupava a torre inteira, e os retratos ficavam no último andar, todos na mesma "
            "parede curva, olhando para uma única cadeira no centro.",
            "— Sente — disse Barlovis. — Hoje você não estuda. Hoje você é apresentada.",
            "Ele começou pelo retrato mais antigo, um homem de olhar severo e gravata torta.",
            "— <b>Joseph Wolpe</b>. Nos anos cinquenta, quando quase todo mundo achava que medo se resolvia "
            "escavando a infância, ele fez uma coisa simples: pediu que a pessoa se aproximasse do que temia "
            "aos poucos, em ordem crescente. Inventou a hierarquia. Toda escada desta casa é filha dele.",
            "— <b>Aaron Beck</b> — continuou, apontando um senhor de gravata-borboleta. — Descobriu que entre "
            "o acontecimento e a emoção há uma frase, e que essa frase pode ser examinada. Deu à psicologia "
            "uma régua para medir o pensamento.",
            "— <b>Albert Bandura</b>: provou que a confiança se constrói fazendo, e que a gente também aprende "
            "vendo o outro atravessar. — Barlovis sorriu. — Você experimentou isso com o Téo, sem saber.",
            "— <b>Joseph LeDoux</b>: mapeou os caminhos do susto dentro do cérebro e mostrou que o corpo "
            "reage antes de a consciência entender. Foi ele quem explicou por que “se acalme” nunca funcionou.",
            "— <b>Stanley Rachman</b>: mostrou que o medo se aprende de três formas — vivendo, vendo e sendo "
            "informado. Muita gente teme avião sem nunca ter voado.",
            "— <b>Isaac Marks</b>: levou a exposição para dentro dos hospitais e provou, em escala, que "
            "atravessar funciona melhor do que conversar sobre atravessar.",
            "— <b>Lars-Göran Öst</b>: o que salvou a Nina. Descobriu que quem desmaia precisa tensionar, não "
            "relaxar, e criou protocolos tão eficientes que muitas fobias cedem em pouquíssimas sessões.",
            "— <b>Michelle Craske</b>: reescreveu o motor do tratamento. Mostrou que não é ficar calmo que "
            "cura: é descobrir que a previsão estava errada.",
            "Faltava um retrato, e Íris já sabia de quem era.",
            "— <b>David H. Barlow</b> — disse Barlovis, e havia afeto na voz. — Juntou o corpo, o pensamento "
            "e a emoção numa teoria só. Explicou por que algumas pessoas são mais vulneráveis, por que o "
            "alarme dispara sem fogo e por que brigar com a emoção é sempre pior do que acolhê-la e agir "
            "assim mesmo.",
            "Íris olhou para a parede inteira, e a sensação de solidão que a acompanhava desde os vinte anos "
            "ficou, de repente, absurda.",
        ],
        grimorio_tit="Quem construiu a estrada — e o que cada um acrescentou",
        grimorio=[
            "Os retratos correspondem a contribuições reais e verificáveis:",
            [
                "<b>Joseph Wolpe (1958):</b> dessensibilização sistemática e hierarquia de ansiedade — "
                "a origem da exposição graduada.",
                "<b>Aaron T. Beck (1976):</b> terapia cognitiva; pensamentos automáticos e distorções no "
                "processamento da informação.",
                "<b>Albert Bandura (1977, 1997):</b> teoria da autoeficácia e aprendizagem social/vicária.",
                "<b>Joseph LeDoux (1996):</b> vias neurais do medo; papel da amígdala e das vias rápida e lenta.",
                "<b>Stanley Rachman (1977):</b> três vias de aquisição do medo — condicionamento direto, "
                "modelação vicária e transmissão de informação.",
                "<b>Isaac Marks (1987):</b> consolidação da exposição in vivo na prática clínica e hospitalar.",
                "<b>Lars-Göran Öst (1989, 2012):</b> tensão aplicada para fobia BII e tratamento em sessão única.",
                "<b>Michelle Craske et al. (2014):</b> modelo de aprendizado inibitório e otimização da exposição.",
                "<b>David H. Barlow (2002, 2011, 2018):</b> tríplice vulnerabilidade, alarmes falsos e "
                "aprendidos, e o Protocolo Unificado para transtornos emocionais.",
            ],
            "O ponto clínico da cena é a redução do isolamento. Fobias específicas afetam parcela expressiva "
            "da população ao longo da vida, e a maioria nunca busca tratamento — muitas por vergonha, muitas "
            "por acreditar que “é só do jeito que eu sou”. Saber que o caminho é conhecido e replicável muda "
            "a natureza da tarefa: deixa de ser heroísmo e passa a ser execução de procedimento.",
        ],
        feitico_tit="A Estrada Calçada",
        feitico_txt="Lembre-se, antes de cada degrau: você não está improvisando. Está aplicando um "
                    "procedimento testado em milhares de pessoas, com resultados medidos.",
        pratica=[
            "1. Qual dessas ideias mais muda a forma como eu enxergo o meu medo?",
            "2. Que crença antiga minha sobre “ser assim mesmo” eu preciso aposentar?",
            "3. O que eu ainda preciso entender melhor antes de subir o próximo degrau?",
        ],
    ),

    dict(
        cap=20, ato="ATO III — AS PROVAS",
        titulo="O observatório das provas",
        epigrafe="“Não acredite em mim. Olhe os números.”",
        img=None,
        cena=[
            "No alto da torre havia um observatório, e no observatório havia gavetas — centenas delas, cada "
            "uma com uma etiqueta, cada uma cheia de fichas escritas à mão.",
            "— Aqui a gente guarda as provas — disse Barlovis. — Todo mundo que passa por esta casa acaba "
            "perguntando a mesma coisa: “mas isso funciona mesmo, ou é só a senhora sendo simpática comigo?”. "
            "Boa pergunta. A melhor de todas, aliás.",
            "Ele abriu a primeira gaveta.",
            "— Exposição in vivo comparada a não fazer nada, a conversar sobre o assunto e a técnicas de "
            "relaxamento isoladas. Dezenas de estudos, milhares de pessoas. Resultado: a exposição ganha, e "
            "não ganha por pouco.",
            "Segunda gaveta.",
            "— Sessão única intensiva para fobias circunscritas. Uma pessoa que passou vinte anos fugindo de "
            "aranhas pode terminar uma tarde conseguindo segurar um pote com uma dentro. Não é milagre: é "
            "hierarquia bem feita, com permanência e sem fuga.",
            "Terceira gaveta.",
            "— Exposição por realidade virtual. Voos que decolam quando você quer, tempestades que você "
            "programa, elevadores que sobem no ritmo que você mandar. Os resultados se equiparam aos da "
            "exposição real, e servem de ponte para quem não conseguiria começar direto no mundo.",
            "Quarta gaveta — e essa ele abriu mais devagar.",
            "— Imagens de cérebro antes e depois do tratamento. A atividade daquela região que dispara o "
            "alarme diminui. O controle das áreas frontais aumenta. Quando você sobe um degrau, Íris, você "
            "não está apenas “se esforçando”. Você está alterando o funcionamento de um circuito.",
            "Íris passou a mão pelas etiquetas, uma a uma.",
            "— Por que o senhor me mostra isso agora, e não no primeiro dia?",
            "— Porque no primeiro dia você teria lido como propaganda. — Barlovis fechou a gaveta. — Agora "
            "você tem dezenove entradas no seu caderno. Agora esses números têm com o que conversar.",
        ],
        grimorio_tit="O que a literatura científica realmente mostra",
        grimorio=[
            "Um resumo honesto das evidências em fobias específicas:",
            [
                "<b>Exposição in vivo é o tratamento de primeira linha.</b> Metanálises (Wolitzky-Taylor et "
                "al., 2008) mostram superioridade consistente sobre lista de espera, placebo psicológico e "
                "relaxamento isolado, com tamanhos de efeito grandes e manutenção em seguimento.",
                "<b>Protocolos intensivos funcionam.</b> Öst demonstrou eficácia de tratamento em sessão "
                "única (2 a 3 horas, com exposição graduada e modelação) para fobias circunscritas, com "
                "ganhos mantidos por anos.",
                "<b>Realidade virtual é eficaz.</b> Metanálises (Powers & Emmelkamp, 2008; Morina et al., "
                "2015) indicam eficácia comparável à exposição in vivo, com boa transferência para situações "
                "reais — especialmente útil em fobia de voar e de alturas.",
                "<b>Há correlatos neurais.</b> Estudos de neuroimagem descrevem redução da reatividade "
                "amigdalar e maior recrutamento pré-frontal após tratamento bem-sucedido.",
                "<b>Medicação não é primeira linha</b> para fobia específica isolada. Ansiolíticos usados "
                "durante a exposição podem, inclusive, prejudicar o aprendizado por funcionarem como "
                "comportamento de segurança.",
            ],
            "Também é honesto dizer o que a literatura <i>não</i> promete: não promete ausência permanente de "
            "medo, não promete linha reta e não elimina o risco de retorno do sintoma. Promete algo mais útil "
            "— redução consistente da esquiva e recuperação da funcionalidade, com ferramentas para lidar com "
            "recaídas quando elas vierem.",
        ],
        feitico_tit="A Gaveta das Provas",
        feitico_txt="Quando duvidar do método, releia esta página. E some a ela a sua própria evidência: o "
                    "seu caderno de registros é o estudo de caso mais relevante que existe para você.",
        pratica=[
            "1. Que dúvida sobre o tratamento ainda me trava?",
            "2. Que evidência pessoal eu já acumulei nas últimas semanas?",
            "3. O que eu preciso testar para tirar a próxima dúvida da frente?",
        ],
    ),

    # ─────────────── ATO IV — O CONFRONTO ───────────────
    dict(
        cap=21, ato="ATO IV — O CONFRONTO",
        titulo="Ryu, o dragão do pátio leste",
        epigrafe="“Ele não veio te destruir. Ele veio te acompanhar.”",
        img="dragao",
        cena=[
            "Havia um dragão no pátio leste, e ninguém na Academia achava isso estranho.",
            "Ryu era do tamanho de um cavalo, tinha escamas cor de bronze e passava a maior parte do tempo "
            "dormindo enrolado ao redor da fonte. Quando alguém se aproximava com medo, ele acordava e "
            "soprava fumaça — não fogo, fumaça — e a fumaça fazia arder os olhos.",
            "— A regra é uma só — disse Barlovis. — Não brigue com ele.",
            "— E se ele soprar?",
            "— Ele vai soprar. Sopre você também, no seu ritmo, e continue andando.",
            "Íris atravessou o pátio devagar. A cinco metros, Ryu abriu um olho dourado. A três, soltou um "
            "bafo morno que fez o cabelo dela grudar na testa. O corpo dela quis correr — quis mesmo, com "
            "toda a força de dez anos de treino de fuga.",
            "Ela parou. Respirou em quatro. Soltou em seis. E disse, em voz alta, sentindo-se ridícula:",
            "— Eu sei que você está aí. Você pode ficar.",
            "O dragão a encarou por um tempo insuportavelmente longo. Depois pousou a cabeça enorme no chão, "
            "a um palmo dos pés dela, e soltou um suspiro que levantou a poeira do pátio.",
            "— Ele parou — sussurrou Íris.",
            "— Ele não parou — corrigiu Barlovis, atrás dela. — Ele continua sendo um dragão. Continua "
            "soprando fumaça quando se assusta. O que mudou é que você deixou de tentar apagá-lo. — O mestre "
            "se aproximou e coçou o queixo do bicho, que fechou os olhos de satisfação. — Este calor todo é a "
            "sua energia, Íris. A mesma coisa que te fazia descer oito andares correndo é a que vai te fazer "
            "subir vinte e dois. Não existe versão sua sem o dragão. Existe uma versão sua que anda ao lado "
            "dele.",
            "Naquela tarde, Íris subiu o degrau nove sem escrever a previsão de medo, mas escrevendo outra "
            "coisa no alto da folha: <i>o que eu quero fazer da minha vida se o medo vier junto?</i>",
        ],
        grimorio_tit="Aceitação emocional e ação guiada por valores no Protocolo Unificado",
        grimorio=[
            "A cena do dragão traduz o núcleo do <b>Protocolo Unificado para o Tratamento Transdiagnóstico "
            "dos Transtornos Emocionais</b>, de <b>David H. Barlow</b> e colaboradores.",
            "A premissa: emoções não são o problema. O problema é a <b>relação aversiva</b> com elas — a "
            "tentativa persistente de suprimir, controlar ou eliminar a experiência emocional. Essa luta "
            "consome recursos, amplifica o sintoma e restringe a vida.",
            "Componentes centrais do protocolo:",
            [
                "<b>Consciência emocional sem julgamento</b>, ancorada no presente.",
                "<b>Flexibilidade cognitiva</b> — considerar interpretações alternativas sem forçar otimismo.",
                "<b>Identificação de padrões de evitação emocional</b>, inclusive os sutis (distração, "
                "ruminação, comportamentos de segurança).",
                "<b>Ação contrária ao impulso emocional</b> — aproximar-se quando a emoção manda fugir.",
                "<b>Exposição interoceptiva</b> — provocar deliberadamente as sensações temidas (girar, "
                "hiperventilar de forma controlada, subir escadas rápido) para reduzir o medo do próprio corpo.",
                "<b>Exposição emocional</b> em situações reais, guiada por valores.",
            ],
            "A mudança de pergunta que Íris faz no fim do capítulo — de “como faço o medo ir embora?” para "
            "“o que eu quero fazer da minha vida mesmo com ele por perto?” — não é retórica. É a reorientação "
            "que sustenta os ganhos depois que o tratamento formal termina.",
        ],
        feitico_tit="A Frase do Dragão",
        feitico_txt="“Eu sei que você está aí. Você pode ficar.” Diga, respire e dê o passo. Aceitar a "
                    "presença da emoção não é resignação: é parar de gastar energia numa guerra impossível.",
        pratica=[
            "1. Como eu costumo tentar controlar ou suprimir a ansiedade?",
            "2. Qual seria a ação contrária ao meu impulso, hoje?",
            "3. O que eu quero fazer da minha vida mesmo que o medo venha junto?",
        ],
    ),

    dict(
        cap=22, ato="ATO IV — O CONFRONTO",
        titulo="O jardim de pedras",
        epigrafe="“A pressa é do medo. A constância é da cura.”",
        img=None,
        cena=[
            "O Monge Kaito varria o jardim de pedras todas as manhãs, e o jardim nunca ficava pronto.",
            "— Por que o senhor varre se amanhã cai folha de novo? — perguntou Íris, sentando-se no degrau "
            "de madeira.",
            "— Pela mesma razão que você sobe degrau se amanhã o medo volta.",
            "Ele apoiou o ancinho e sentou-se ao lado dela. O jardim tinha sete pedras grandes dispostas de "
            "tal maneira que, de qualquer ponto onde a pessoa se sentasse, uma delas ficava escondida.",
            "— Nunca se vê o jardim inteiro — disse o monge. — Sempre falta uma pedra. Isso é de propósito.",
            "— Para ensinar o quê?",
            "— Que você vai começar a travessia sem enxergar o fim dela. Todo mundo quer a garantia antes do "
            "primeiro passo. A garantia é a única coisa que esta casa não vende.",
            "Kaito pegou do bolso uma tigela pequena, rachada de um lado a outro, com as fissuras preenchidas "
            "por uma linha dourada e brilhante.",
            "— Quebrou faz doze anos. Um aprendiz derrubou. Eu poderia ter jogado fora e comprado outra igual "
            "por dois trocados. — Ele girou a tigela na luz. — Preferi colar com ouro. Agora ela vale mais e "
            "conta uma história melhor. Chamam isso de kintsugi.",
            "— O senhor está dizendo que eu devo ter orgulho do meu medo?",
            "— Estou dizendo que você não vai sair daqui como se nada tivesse acontecido. Vai sair com "
            "linhas douradas onde teve rachadura, e essas linhas vão ser exatamente a parte de você que outras "
            "pessoas vão procurar quando estiverem no chão. — Kaito devolveu a tigela ao bolso e pegou o "
            "ancinho de novo. — Ninguém pede conselho a quem nunca quebrou.",
            "Íris ficou sentada ali até o sol virar a esquina do muro. Depois se levantou, pegou um segundo "
            "ancinho encostado na parede e varreu o outro lado do jardim, em silêncio, junto com ele.",
            "— Amanhã vai cair folha de novo — avisou o monge.",
            "— Eu sei — disse ela. — Amanhã eu varro de novo.",
        ],
        grimorio_tit="Manutenção, tolerância à incerteza e a métrica certa de sucesso",
        grimorio=[
            "O jardim que nunca fica pronto descreve dois princípios clínicos de longo prazo.",
            "<b>Tolerância à incerteza.</b> A busca por garantias antes de agir é um mantenedor central da "
            "ansiedade: nenhuma quantidade de reasseguramento é suficiente, porque a certeza absoluta não "
            "existe. O objetivo terapêutico não é conseguir a garantia — é <b>agir sem ela</b>, o que se "
            "treina em cada degrau realizado com dúvida.",
            "<b>Manutenção ativa.</b> Ganhos em terapia de exposição se sustentam quando o repertório "
            "continua sendo praticado. Recomendações práticas de manutenção:",
            [
                "Uma a duas exposições de reforço por mês, mesmo sem sintomas.",
                "Não recusar oportunidades naturais de contato com o estímulo.",
                "Retomar em até 48 horas após qualquer fuga.",
                "Revisar o caderno de registros a cada trimestre.",
                "Reavaliar se muletas voltaram a aparecer de forma silenciosa.",
            ],
            "Sobre o kintsugi: o crescimento pós-adversidade é um fenômeno descrito na literatura, mas exige "
            "cuidado ético — ele não justifica o sofrimento nem deve ser usado para romantizá-lo. O uso "
            "clínico legítimo é outro: reduzir a vergonha e reposicionar a experiência dentro de uma "
            "narrativa de competência, o que favorece a manutenção do tratamento.",
        ],
        feitico_tit="O Ancinho de Amanhã",
        feitico_txt="Marque no calendário as suas exposições de manutenção do próximo trimestre. Cuidar da "
                    "escada é mais barato do que reconstruí-la.",
        pratica=[
            "1. Que garantia eu venho exigindo antes de agir — e que nunca vou conseguir?",
            "2. Como será a minha rotina de manutenção mensal?",
            "3. Que linha dourada eu já consigo reconhecer em mim?",
        ],
    ),

    dict(
        cap=23, ato="ATO IV — O CONFRONTO",
        titulo="A torre dos mil degraus",
        epigrafe="“O topo chega sozinho quando você para de olhar para ele.”",
        img="escada",
        cena=[
            "O dia da apresentação no Edifício Aurora amanheceu limpo, sem vento, o que Íris considerou uma "
            "gentileza do universo e Barlovis considerou irrelevante.",
            "— Se estivesse ventando, você faria igual — disse ele, entregando a ela a tábua de Volpo, agora "
            "com nove riscos de lápis marcando os degraus vencidos. — O décimo é hoje.",
            "Ela chegou ao prédio às nove. Vinte e dois andares. Elevador panorâmico de vidro dos dois lados.",
            "No térreo, escreveu a previsão no caderno, como fizera dezenove vezes antes: <i>“Vou entrar no "
            "elevador, a ansiedade vai chegar a 8, vou querer descer no quinto andar. Previsão de catástrofe: "
            "vou passar mal na frente dos clientes e ser retirada da equipe.”</i>",
            "Entrou. Segundo andar: seis. Quinto: sete. Nono: oito, e a mão foi sozinha para o corrimão — "
            "e ela deixou, porque ainda era o degrau nove.",
            "Décimo quinto andar: continuava oito. Décimo oitavo: sete e meio. Vigésimo segundo: sete.",
            "As portas abriram para um corredor comum, com carpete cinza e cheiro de café. Íris riu, porque "
            "não havia abismo nenhum: havia um corredor de escritório.",
            "O terraço era do outro lado da porta de vidro. Piso de madeira, guarda-corpo de aço e vidro, "
            "a cidade inteira aberta como uma planta baixa viva. Os três engenheiros já estavam lá, com os "
            "projetos abertos sobre uma mesa dobrável.",
            "Ela deu quatro passos e parou no centro. Não segurou em nada.",
            "Foi ali, em pé, com o coração a mil e a voz mais firme do que esperava, que Íris Valente "
            "apresentou o projeto do mirante — o mesmo mirante que, oito meses antes, a fizera sentar no chão "
            "da cozinha com as costas na porta da geladeira.",
            "Levou dezenove minutos. No minuto quatro, a ansiedade caiu para cinco. No minuto dez, para três. "
            "No minuto dezenove, ela já tinha esquecido de medir.",
            "Quando terminou, um dos engenheiros perguntou se ela topava descer até a borda para conferir a "
            "angulação do guarda-corpo. Íris olhou para o vão de vinte e dois andares, para a própria mão "
            "firme, e ouviu — muito, muito baixinho, quase educado — o Senhor do Nunca sugerir que talvez "
            "fosse melhor não.",
            "— Vamos — disse ela.",
        ],
        grimorio_tit="A exposição culminante: o que muda quando o degrau mais alto é vencido",
        grimorio=[
            "O capítulo descreve, com precisão técnica, uma exposição bem executada:",
            [
                "<b>Previsão registrada antes</b>, em termos específicos e testáveis.",
                "<b>Monitoramento contínuo</b> de SUDS ao longo do percurso.",
                "<b>Permanência</b> sem fuga durante a queda natural da curva.",
                "<b>Retirada progressiva de muletas</b> — o corrimão no degrau nove, nenhum apoio no dez.",
                "<b>Extensão espontânea</b> ao final (a ida até a borda), sinal clínico de consolidação.",
            ],
            "Dois detalhes merecem destaque. Primeiro: a ansiedade <b>não chegou a zero</b>. Ela entrou em "
            "sete e conduziu a apresentação inteira. O critério de sucesso em exposição é funcional — "
            "fazer o que importa — e não a ausência de sensação.",
            "Segundo: a ansiedade máxima observada (8) foi <b>menor</b> que a prevista para o pior cenário, e "
            "a catástrofe antecipada (passar mal e ser retirada da equipe) simplesmente não ocorreu. Esse "
            "contraste registrado é o que Craske chama de violação de expectativa — o dado que atualiza o "
            "modelo de perigo.",
            "Após uma exposição culminante bem-sucedida, é comum haver generalização rápida para situações "
            "correlatas não treinadas. O passo clínico seguinte não é comemorar e parar: é <b>consolidar</b>, "
            "repetindo em contextos variados antes que a memória inibitória perca competitividade.",
        ],
        feitico_tit="O Degrau Dez",
        feitico_txt="No dia do seu degrau mais alto: escreva a previsão, monitore o número, permaneça, não "
                    "segure em nada que não seja necessário e, se aparecer um convite para ir um pouco além, "
                    "aceite.",
        pratica=[
            "1. Qual é a minha apresentação no terraço — o meu degrau dez concreto?",
            "2. Que muletas ainda preciso soltar antes de chegar lá?",
            "3. Como vou consolidar o resultado nas duas semanas seguintes?",
        ],
    ),

    dict(
        cap=24, ato="ATO IV — O CONFRONTO",
        titulo="O duelo com o Senhor do Nunca",
        epigrafe="“Não houve luta. Houve jantar cancelado.”",
        img="monstrinho",
        cena=[
            "Ele a esperava no corredor norte, na noite em que ela voltou do Aurora.",
            "Íris quase não o reconheceu. A poltrona continuava lá, grande e confortável, mas a figura sentada "
            "nela tinha o tamanho de uma criança pequena. O colete sobrava nos ombros. A voz, quando veio, "
            "saiu fina.",
            "— Você me deixou com fome — disse ele.",
            "— Eu sei.",
            "— Isso é crueldade. Eu só queria te proteger.",
            "— Eu sei disso também. — Íris sentou-se no chão do corredor, de frente para ele, sem pressa. — "
            "E é por isso que eu não vim aqui te matar.",
            "O Senhor do Nunca ergueu o rosto, desconfiado.",
            "— Você não pode me matar.",
            "— Não posso. Já entendi. Você é a parte de mim que quer que eu chegue viva em casa, e essa parte "
            "é boa. O problema nunca foi você existir. O problema foi eu te deixar escolher a rota, o horário, "
            "a profissão, os amigos e o tamanho da minha vida.",
            "Ela puxou do bolso a folha dobrada que trouxera na primeira manhã, com as dezessete coisas que "
            "não fazia mais. Estava toda riscada. Restavam três linhas sem risco.",
            "— Ainda tenho essas — disse. — Vou levar mais um tempo nelas.",
            "— E enquanto isso você me deixa aqui, deste tamanho? — a voz dele era quase um lamento.",
            "— Enquanto isso eu te dou o lugar certo: você fica no banco do passageiro. Pode falar. Pode "
            "avisar. Pode até gritar quando eu chegar perto de uma escada de verdade sem corrimão, e aí eu "
            "vou te agradecer. — Íris levantou-se e limpou a poeira da calça. — O volante é meu.",
            "Os Sussurradores tentaram se adensar ao redor dela e falharam. Íris passou por eles como quem "
            "atravessa neblina de manhã cedo.",
            "Na porta do dormitório, olhou para trás pela última vez. A poltrona ainda estava lá, e o Senhor "
            "do Nunca continuava sentado nela: pequeno, cansado, ainda existindo — como sempre existiria.",
            "E foi tudo bem.",
        ],
        grimorio_tit="O objetivo real do tratamento: reposicionar o medo, não eliminá-lo",
        grimorio=[
            "O desfecho deste livro é deliberadamente antitriunfalista, e isso tem base clínica.",
            "A extinção não apaga a memória de medo original — cria uma memória inibitória concorrente. "
            "Consequência: a capacidade de sentir medo diante do estímulo pode permanecer, em alguma medida, "
            "por toda a vida. Prometer eliminação total é criar uma expectativa que a primeira recaída "
            "destrói.",
            "O que muda de fato após tratamento bem-sucedido:",
            [
                "A <b>esquiva</b> cai drasticamente — este é o alvo primário e o melhor indicador de melhora.",
                "A <b>intensidade e a duração</b> das respostas de medo diminuem.",
                "A <b>interferência funcional</b> desaparece ou se torna mínima.",
                "A pessoa passa a dispor de um <b>procedimento</b> para lidar com retornos do sintoma.",
                "A relação com a emoção muda: de inimigo a ser eliminado para sinal a ser considerado.",
            ],
            "A imagem final — o medo no banco do passageiro — resume a meta terapêutica com precisão: "
            "manter a função protetora do sistema de alarme e retirar dele o poder de decisão sobre a vida.",
            "É por isso que, em consultório, a pergunta de encerramento nunca é “você ainda sente medo?”. "
            "É: <b>“o que você voltou a fazer?”</b>",
        ],
        feitico_tit="O Volante",
        feitico_txt="Escreva a nova função do seu medo: o que ele pode continuar fazendo (avisar) e o que "
                    "ele não decide mais (para onde você vai). Releia sempre que ele tentar sentar no lugar "
                    "do motorista.",
        pratica=[
            "1. Quantas linhas da minha lista original já estão riscadas?",
            "2. Quais continuam de pé — e qual delas será a próxima?",
            "3. Qual é o novo lugar do medo na minha vida, escrito com as minhas palavras?",
        ],
    ),
]


def build():
    s = styles()
    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2.0 * cm,
        title="A Escada Segura — a jornada de Íris Valente",
        author="Dra. Priscila Palomo",
    )
    story = []

    # ═══════════ CAPA ═══════════
    story.append(Spacer(1, 1.6 * cm))
    p(story, "DRA. PRISCILA PALOMO  ·  CRP 98007", s["cover_brand"])
    story.append(Spacer(1, 0.3 * cm))
    story.append(HRFlowable(width="40%", thickness=2, color=NAVY, spaceBefore=0, spaceAfter=14))
    p(story, "A Escada Segura", s["cover_title"])
    p(story, "A jornada de Íris Valente contra o Senhor do Nunca", s["cover_sub"])
    story.append(Spacer(1, 0.5 * cm))
    story.append(ilustra("dragao", 8.5 * cm))
    story.append(Spacer(1, 0.5 * cm))
    p(story, "“Não prometemos que o medo vai sumir.<br/>Prometemos que ele vai deixar de mandar.”", s["quote"])
    story.append(Spacer(1, 0.5 * cm))
    story.append(HRFlowable(width="26%", thickness=1, color=LINE, spaceBefore=0, spaceAfter=12))
    p(story, "Um romance em 24 capítulos — e o programa clínico que existe por trás dele.<br/>"
             "Psicoeducação de fobias com DSM-5, Terapia Cognitivo-Comportamental,<br/>"
             "o modelo de David H. Barlow e um caderno de treino de 21 dias.", s["cover_sub"])
    story.append(Spacer(1, 0.7 * cm))
    p(story, "www.priscilapalomo.com", s["cover_brand"])
    story.append(PageBreak())

    # ═══════════ AVISO ÉTICO ═══════════
    p(story, "Antes de começar — compromisso ético e cuidados", s["h1"])
    story.append(hr())
    p(story, "Este livro conta uma história inventada para ensinar uma coisa verdadeira. Íris, Téo, Nina e a "
      "Academia na Colina do Sino são ficção. Já o <b>Grimório da Ciência</b> que fecha cada capítulo não é: "
      "ele traduz critérios do DSM-5-TR, procedimentos da Terapia Cognitivo-Comportamental e o modelo de "
      "regulação emocional de <b>David H. Barlow</b>, com as técnicas exatamente como são aplicadas em "
      "consultório.", s["body"])
    p(story, "<b>Aviso importante:</b> este material tem finalidade de educação em saúde mental e treino de "
      "habilidades. Ele <b>não substitui psicoterapia individual</b>, avaliação diagnóstica nem tratamento "
      "médico. Se você apresenta crises de pânico descompensadas, ideação suicida, trauma recente sem suporte, "
      "transtorno alimentar ativo ou usa álcool e medicamentos sem orientação para tolerar o medo, procure um "
      "profissional antes de iniciar qualquer exposição por conta própria.", s["body"])
    p(story, "Durante os treinos, vale a regra do Mestre Barlovis: <b>nada acontece sem o seu consentimento</b>. "
      "Se a ansiedade ficar intolerável, pare, use a respiração lenta e procure seu psicólogo ou o CVV (188).", s["body"])
    story.append(Spacer(1, 6))
    p(story, "Dra. Priscila Palomo · Psicóloga (CRP 98007) · Doutora em Psicologia pela Universitat de València · "
      "Especialista em fobias, TCC e exposição por realidade virtual · WhatsApp (11) 95069-0537", s["small"])
    story.append(PageBreak())

    # ═══════════ PERSONAGENS ═══════════
    p(story, "Quem é quem nesta história", s["h1"])
    story.append(hr())
    elenco = [
        ("Íris Valente", "Arquiteta, 29 anos. Teme alturas e elevadores. Recebeu a carta e subiu a colina. "
                         "É por onde você entra na história."),
        ("O Senhor do Nunca", "O vilão. Não ataca, não machuca, não grita: apenas oferece alívio. Engorda "
                              "com cada fuga e emagrece com cada travessia. É a evitação em pessoa."),
        ("Os Sussurradores", "Névoas que narram catástrofes ao pé do ouvido. São os pensamentos automáticos "
                             "e as previsões de desastre."),
        ("Os Grilhões de Conforto", "Objetos que parecem proteger e na verdade prendem: amuletos, muletas, "
                                    "rotas de fuga. Os comportamentos de segurança."),
        ("Mestre Barlovis", "Diretor da Academia. Ensina o alarme falso, a tríplice vulnerabilidade e a "
                            "aceitação da emoção. Inspirado no trabalho de David H. Barlow."),
        ("Mestre Volpo", "O marceneiro da Escada de Prata: divide qualquer monstro em degraus. "
                         "Inspirado em Joseph Wolpe."),
        ("Mestra Kraskia", "Guardiã do Pergaminho da Predição. Ensina que o que cura é a surpresa de descobrir "
                           "que a catástrofe não veio. Inspirada em Michelle Craske."),
        ("Mestre Bekhan", "O óptico da Academia: troca as lentes que aumentam o abismo. "
                          "Inspirado em Aaron T. Beck."),
        ("Mestra Bandurá", "Acende a chama da autoeficácia: coragem se constrói com vitórias pequenas e "
                           "repetidas. Inspirada em Albert Bandura."),
        ("Mestre Ostrom", "Cuida de quem desmaia diante de sangue e agulhas. Inspirado em Lars-Göran Öst."),
        ("Monge Kaito", "Varre o jardim de pedras e conta parábolas. Guarda a paciência da casa."),
        ("Ryu", "O dragão do pátio leste. Não é o inimigo — é a energia do medo esperando ser domada."),
        ("Téo e Nina", "Aprendizes e amigos de Íris. Téo teme cães; Nina, enfermeira, desmaia com agulhas."),
    ]
    for nome, desc in elenco:
        p(story, f"<b>{nome}</b> — {desc}", s["body"])
    story.append(PageBreak())

    # ═══════════ SUMÁRIO ═══════════
    p(story, "Sumário", s["h1"])
    story.append(hr())
    p(story, "<i>Cada capítulo tem duas páginas: na primeira, a história; na segunda, o Grimório da Ciência — "
             "o que a psicologia baseada em evidências diz sobre o que acabou de acontecer, com o feitiço "
             "(a técnica) e o seu exercício.</i>", s["small"])
    story.append(Spacer(1, 6))
    sumario = [
        ("Prólogo", "A noite em que o mundo coube num quarto"),
        ("ATO I — O CHAMADO", ""),
        ("01", "A vida que coube dentro de um quarto — o ciclo da esquiva"),
        ("02", "A carta que entrou pela fresta da porta — ambivalência e decisão"),
        ("03", "A Academia na Colina do Sino — consentimento e controle"),
        ("04", "O sino que toca sem fogo — o alarme falso e a amígdala"),
        ("05", "O Espelho de Nunca-Foi — o custo da evitação"),
        ("06", "Os Sussurradores do corredor norte — os três eixos do sintoma"),
        ("ATO II — O APRENDIZADO", ""),
        ("07", "O mapa antigo do salão — os critérios do DSM-5"),
        ("08", "Os cinco corredores — os subtipos de fobia"),
        ("09", "Os óculos de Mestre Bekhan — distorções cognitivas"),
        ("10", "Os Grilhões de Conforto — comportamentos de segurança"),
        ("11", "A oficina de Mestre Volpo — a Escada de Prata (hierarquia)"),
        ("12", "O Feitiço do Sopro Lento — respiração e freio parassimpático"),
        ("13", "O Lago Gelado da Permanência — habituação"),
        ("14", "O Pergaminho da Predição — aprendizado inibitório"),
        ("ATO III — AS PROVAS", ""),
        ("15", "O filhote do pátio oeste — a travessia de Téo"),
        ("16", "A agulha de prata de Nina — tensão aplicada"),
        ("17", "A recaída — quando o Senhor do Nunca volta maior"),
        ("18", "A noite em que Íris quis desistir — autoeficácia"),
        ("19", "A biblioteca dos retratos vivos — os mestres reais"),
        ("20", "O observatório das provas — o que dizem os estudos"),
        ("ATO IV — O CONFRONTO", ""),
        ("21", "Ryu, o dragão do pátio leste — aceitação emocional"),
        ("22", "O jardim de pedras — determinação e kintsugi"),
        ("23", "A torre dos mil degraus — a subida final"),
        ("24", "O duelo com o Senhor do Nunca — o fim da dieta"),
        ("Epílogo", "Um ano depois, no terraço do Edifício Aurora"),
        ("Caderno", "Sua Escada Segura, as 21 Provações e os apêndices clínicos"),
    ]
    for a, b in sumario:
        if b:
            p(story, f"<b>{a}</b> &nbsp;·&nbsp; {b}", s["toc"])
        else:
            p(story, f"<b>{a}</b>", s["h3"])
    story.append(PageBreak())

    # ═══════════ PRÓLOGO ═══════════
    p(story, "PRÓLOGO", s["part"])
    p(story, "A noite em que o mundo coube num quarto", s["h1"])
    story.append(hr())
    prosa(story, [
        "Existe um tipo de inimigo que nunca aparece de armadura.",
        "Ele não arromba a porta, não grita, não persegue ninguém por corredores escuros. Ele senta na sua "
        "sala, oferece um chá e diz, com muita doçura, que hoje talvez não seja um bom dia para sair. "
        "Amanhã você tenta. Amanhã está mais fresco. Amanhã você está mais preparada.",
        "Ele repete isso por dez anos.",
        "Quando percebe, você já não pega elevador, já não vai a festas no décimo andar, já não olha por "
        "cima da grade da ponte, já não aceita convites que envolvam avião, cachorro, agulha, túnel, palco "
        "ou mar aberto — e todo mundo à sua volta acha que você é assim mesmo, que é o seu jeito, que é "
        "questão de personalidade.",
        "Não é. É uma dieta.",
        "Este livro conta a história de uma mulher chamada Íris Valente, que descobriu tarde — mas não tarde "
        "demais — quem estava comendo à sua mesa. E conta, junto com a história, exatamente como se corta o "
        "alimento desse inimigo: não com força de vontade, não com discursos motivacionais, mas com um "
        "método antigo, testado em milhares de pessoas, que cabe numa palavra simples.",
        "Escada.",
        "Você vai encontrar aqui dois livros costurados um no outro. O primeiro é uma história: uma casa no "
        "alto de uma colina, mestres estranhos, um dragão no pátio leste e um vilão que só se alimenta de "
        "fuga. O segundo é um programa clínico sério, com critérios diagnósticos, técnicas de exposição "
        "gradual, protocolos de respiração, registro de predição e um plano de vinte e um dias.",
        "Leia a história pelo prazer de ler. Faça o programa pela liberdade de viver.",
        "E quando chegar ao último degrau — porque você vai chegar — lembre-se de olhar para trás e ver o "
        "tamanho que o seu Senhor do Nunca ficou.",
    ], s)
    story.append(Spacer(1, 8))
    p(story, "— Dra. Priscila Palomo, psicóloga (CRP 98007)", s["quote"])
    story.append(PageBreak())

    # ═══════════ OS CAPÍTULOS DO ROMANCE ═══════════
    ato_atual = None
    aberturas = {
        "ATO I — O CHAMADO": ("Onde Íris descobre o nome do que a persegue",
                              "A carta, a colina, o sino que toca sem fogo e o espelho que mostra a vida não vivida."),
        "ATO II — O APRENDIZADO": ("Onde se aprendem os feitiços que realmente funcionam",
                                   "O mapa do DSM-5, as lentes de Bekhan, a Escada de Prata, o sopro lento e o pergaminho da predição."),
        "ATO III — AS PROVAS": ("Onde a jornada quase termina antes da hora",
                                "As travessias de Téo e Nina, a recaída, a noite da desistência e as provas que a ciência guardou."),
        "ATO IV — O CONFRONTO": ("Onde o vilão descobre que a dieta acabou",
                                 "O dragão, o jardim de pedras, a torre dos mil degraus e o duelo final."),
    }
    for c in CAPITULOS:
        if c["ato"] != ato_atual:
            ato_atual = c["ato"]
            titulo_ato, sub_ato = aberturas[ato_atual]
            abertura_de_ato(story, ato_atual, titulo_ato, sub_ato, s)
        capitulo(
            story, c["cap"], c["ato"], c["titulo"], c["epigrafe"], c["img"], c["cena"],
            c["grimorio_tit"], c["grimorio"], c["feitico_tit"], c["feitico_txt"], c["pratica"], s,
        )

    # ═══════════ EPÍLOGO ═══════════
    p(story, "EPÍLOGO", s["part"])
    p(story, "Um ano depois, no terraço do Edifício Aurora", s["h1"])
    story.append(hr())
    prosa(story, [
        "O mirante ficou pronto em novembro.",
        "É uma plataforma de vidro que avança quatro metros para fora da fachada, no vigésimo segundo andar, "
        "com guarda-corpo de aço escovado e piso translúcido. Quem chega costuma parar na porta, respirar "
        "fundo e dar o primeiro passo com muito cuidado — e isso, garante a arquiteta responsável, foi "
        "projetado de propósito.",
        "— O corrimão está a noventa centímetros do vão, e não a um metro e vinte — explicou Íris Valente na "
        "reportagem que saiu no caderno de cidades. — Quem tem medo precisa poder chegar perto <i>aos poucos</i>. "
        "Uma estrutura que só serve para quem já não tem medo é uma estrutura mal projetada.",
        "Téo tem um cachorro. Chama-se Bento, como o primeiro, e dorme dezoito horas por dia na poltrona que "
        "não deveria ocupar. Nos primeiros meses, Téo ainda contava os segundos quando o bicho se aproximava "
        "rápido demais. Hoje ele conta outra coisa: quantos parques da cidade ainda faltam visitar.",
        "Nina voltou para a emergência. Aplica injeções, faz coletas, atende acidentes. Continua tensionando "
        "as pernas nos procedimentos mais longos, e não vê nisso nenhum motivo de vergonha — vê uma técnica, "
        "como qualquer outra do seu ofício. Treina novatos. Sempre pergunta, na primeira semana, quem ali "
        "sente tontura ao ver sangue. Sempre aparece alguém. Ela ensina.",
        "A Academia continua no alto da Colina do Sino. O sino continua tocando de vez em quando sem que haja "
        "fogo algum, e o Mestre Barlovis continua achando graça disso.",
        "Quanto ao Senhor do Nunca: ele ainda existe.",
        "Íris o encontra algumas vezes por ano — em vésperas de viagem, em dias de sono ruim, na primeira vez "
        "que subiu num andaime de obra. Ele aparece pequeno, senta no banco do passageiro e comenta o "
        "trajeto. Às vezes tem razão. Na maioria das vezes, não.",
        "Ela dirige assim mesmo.",
        "E é exatamente isso que este livro veio te oferecer: não uma vida sem medo — uma vida em que o medo "
        "vai junto, no banco do lado, sem nunca mais escolher o destino.",
    ], s)
    story.append(Spacer(1, 6))
    p(story, "FIM DA HISTÓRIA — COMEÇO DA SUA", s["quote"])
    story.append(PageBreak())

    # ═══════════ CARTA DA AUTORA ═══════════
    p(story, "Carta da autora", s["h1"])
    story.append(hr())
    prosa(story, [
        "Se você chegou até aqui, quero te dizer uma coisa com muita clareza: a Íris é inventada, mas a "
        "história dela é feita de pedaços reais. Trabalho com fobias há anos, em consultório e em pesquisa, "
        "inclusive com exposição por realidade virtual, e já acompanhei muitas pessoas descerem oito andares "
        "correndo numa sexta-feira e subirem vinte e dois numa terça.",
        "Escolhi contar em forma de romance por um motivo técnico, não estético. A informação clínica sozinha "
        "raramente muda comportamento — quem tem fobia normalmente <i>já sabe</i> que a situação é segura, e "
        "isso nunca foi suficiente. História é diferente: história cria imagem, imagem cria memória, e memória "
        "aparece na hora do aperto, que é quando você precisa dela.",
        "Então quando o seu coração disparar na porta do elevador, eu não espero que você lembre da expressão "
        "“reforço negativo”. Espero que você lembre de um sino tocando sem fogo, de um lago gelado que parou "
        "de ser gelado, de um vilão magro sentado numa poltrona grande demais.",
        "E que, lembrando, você fique mais um minuto.",
        "O caderno que começa na próxima página é a parte séria do trabalho: a sua escada, as suas vinte e "
        "uma provações e as folhas onde você vai anotar previsão e realidade, lado a lado, até a diferença "
        "entre elas ficar impossível de ignorar.",
        "Faça no seu ritmo. Não pule degraus. E, se puder, faça acompanhada de um profissional — este livro "
        "foi feito para caminhar ao lado da terapia, nunca no lugar dela.",
        "Boa travessia.",
    ], s)
    story.append(Spacer(1, 10))
    p(story, "<b>Dra. Priscila Palomo</b><br/>Psicóloga · CRP 98007<br/>"
             "Doutora em Psicologia pela Universitat de València<br/>"
             "www.priscilapalomo.com · WhatsApp (11) 95069-0537", s["body_left"])
    story.append(PageBreak())

    # ═══════════ CADERNO DO APRENDIZ ═══════════
    story.append(Spacer(1, 5.5 * cm))
    p(story, "SEGUNDA PARTE", s["ato"])
    p(story, "O Caderno do Aprendiz", s["cover_title"])
    story.append(HRFlowable(width="34%", thickness=2, color=NAVY, spaceBefore=6, spaceAfter=14))
    p(story, "Sua Escada Segura, as 21 Provações e os apêndices clínicos.<br/>"
             "A partir daqui, quem escreve a história é você.", s["cover_sub"])
    story.append(PageBreak())

    # ── A ESCADA PESSOAL ──
    p(story, "A sua Escada de Prata", s["h1"])
    story.append(hr())
    p(story, "Faça como Íris fez na oficina de Mestre Volpo: comece pelo degrau 10 — o objetivo que te trouxe "
      "até aqui — e vá descendo até chegar em algo que você faria hoje. Cada degrau precisa ser "
      "<b>específico</b> (situação, tempo, distância, com ou sem companhia), <b>repetível</b> e ficar entre "
      "<b>4 e 7</b> na sua escala de ansiedade de 0 a 10.", s["body"])
    p(story, "Se o degrau 1 ainda assusta demais, corte-o ao meio. Nunca existe degrau pequeno demais — "
      "existe escada mal serrada.", s["body"])
    story.append(Spacer(1, 6))
    story.append(ladder_template(s))
    story.append(Spacer(1, 8))
    p(story, "Meu degrau 10 (objetivo final, em uma frase concreta):", s["label"])
    story.append(blank_lines(2))
    story.append(PageBreak())

    # ── AS 21 PROVAÇÕES ──
    p(story, "As 21 Provações", s["h1"])
    story.append(hr())
    p(story, "Vinte e um dias, vinte e uma travessias. Cada provação tem o nome de um momento da história e "
      "uma tarefa concreta. Você não precisa cumprir todas na ordem sugerida: precisa cumprir todas com "
      "<b>previsão escrita antes</b> e <b>realidade escrita depois</b>.", s["body"])
    p(story, "<b>Semana 1 — Fundação:</b> conhecer o alarme, montar a escada, vencer os degraus 1 e 2.<br/>"
      "<b>Semana 2 — Consolidação:</b> degraus 3 a 6, soltar as primeiras muletas, variar contextos.<br/>"
      "<b>Semana 3 — Soberania:</b> degraus 7 a 10, retirar as muletas restantes e planejar a manutenção.", s["body"])
    story.append(Spacer(1, 4))
    story.append(caixa(
        "Regra das provações",
        "Permaneça até a ansiedade cair pelo menos 40% do pico — ou até conseguir fazer algo que não conseguia "
        "no primeiro minuto. Nunca saia no pico. Se fugir, volte em até 48 horas, um degrau abaixo.", s))

    provacoes = [
        ("A Lista Honesta", "Escreva as suas dezessete linhas: tudo que você deixou de fazer. Depois marque a que dói mais."),
        ("O Alfinete no Mapa", "Nomeie o seu medo com precisão e identifique o seu corredor (subtipo). Sem vergonha: localização."),
        ("O Sino sem Fogo", "Provoque de leve a sua ativação (subir escadas rápido, girar) e observe: alarme sem fogo."),
        ("A Serragem da Escada", "Monte os seus 10 degraus com Mestre Volpo. Específicos, repetíveis, entre 4 e 7."),
        ("O Primeiro Degrau", "Cumpra o degrau 1 inteiro, com previsão escrita antes e número anotado a cada minuto."),
        ("O Sopro da Velinha", "Treine 10 ciclos de 4-6 três vezes ao dia. Depois use durante o degrau 1 — para ficar, não para sumir."),
        ("A Repetição Teimosa", "Refaça o degrau 1 em outro horário e outro lugar. Contexto novo, mesmo degrau."),
        ("O Segundo Degrau", "Suba ao degrau 2. Escreva a previsão com número e tempo. Permaneça além do pico."),
        ("A Primeira Etiqueta", "Escolha a muleta mais fácil de soltar e faça o degrau 2 sem ela."),
        ("O Lago Gelado", "Escolha um degrau e fique o dobro do tempo habitual. Anote a curva minuto a minuto."),
        ("O Pergaminho Cheio", "Releia todos os registros até aqui. Some: quantas catástrofes previstas aconteceram?"),
        ("O Terceiro Degrau", "Suba ao degrau 3 e permaneça sem checagens, sem contar segundos, com os olhos abertos."),
        ("A Testemunha", "Assista alguém atravessar (ao vivo, em vídeo ou relato) e depois faça o seu degrau do dia."),
        ("O Quarto Degrau", "Suba ao degrau 4. Se possível, sem avisar ninguém antes — sem rede de resgate combinada."),
        ("O Dragão no Pátio", "Diga em voz alta: “eu sei que você está aí, você pode ficar” e avance no degrau 5."),
        ("Os Grilhões Soltos", "Refaça o degrau 5 sem nenhuma muleta. Nenhuma. Anote o que muda."),
        ("O Sexto Degrau", "Suba ao degrau 6 em um contexto diferente do treinado (outro prédio, outro horário, chuva)."),
        ("O Tropeço Previsto", "Se houve fuga nesta semana, retome hoje, um degrau abaixo, e complete a permanência."),
        ("O Sétimo e o Oitavo", "Encadeie dois degraus no mesmo dia, com intervalo curto entre eles."),
        ("A Véspera da Torre", "Prepare o degrau 10: escreva a previsão completa e revise a sua lista de vitórias."),
        ("A Torre dos Mil Degraus", "Cumpra o degrau 10. Sem apoio desnecessário. E, se houver convite para ir além, aceite."),
    ]

    p(story, "As 21 travessias, em resumo", s["h3"])
    linhas_indice = [[
        Paragraph("<font color='white'><b>#</b></font>", s["field"]),
        Paragraph("<font color='white'><b>Provação</b></font>", s["field"]),
        Paragraph("<font color='white'><b>Semana</b></font>", s["field"]),
    ]]
    for i, (nome, _t) in enumerate(provacoes, 1):
        semana = 1 if i <= 7 else (2 if i <= 14 else 3)
        linhas_indice.append([
            Paragraph(f"{i:02d}", s["field"]),
            Paragraph(nome, s["field"]),
            Paragraph(str(semana), s["field"]),
        ])
    tabela_indice = Table(linhas_indice, colWidths=[1.2 * cm, 12.8 * cm, 2.5 * cm])
    tabela_indice.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(tabela_indice)
    story.append(PageBreak())

    for i, (nome, tarefa) in enumerate(provacoes, 1):
        semana = 1 if i <= 7 else (2 if i <= 14 else 3)
        p(story, f"PROVAÇÃO {i:02d} · SEMANA {semana}", s["part"])
        p(story, nome, s["h1"])
        p(story, f"<b>Tarefa de hoje:</b> {tarefa}", s["body"])
        story.append(hr())
        story.append(exposure_log(s, f"Registro da Provação {i:02d} — {nome}"))
        story.append(PageBreak())

    # ── APÊNDICE A ──
    p(story, "Apêndice A — Diário semanal de autoeficácia (a fila de fósforos)", s["h1"])
    story.append(hr())
    p(story, "Toda semana, escreva as suas vitórias. Não para se elogiar: para ter um arquivo objetivo a "
      "que recorrer nos dias em que a sua memória ficar seletiva.", s["body"])
    for w in range(1, 13):
        p(story, f"<b>Semana {w:02d}</b>", s["h2"])
        p(story, "Degraus cumpridos e vitórias desta semana:", s["label"])
        story.append(blank_lines(2))
        p(story, "Muletas soltas / esquivas identificadas:", s["label"])
        story.append(blank_lines(2))
        p(story, "Próximo degrau da semana que vem:", s["label"])
        story.append(blank_lines(1))
        if w % 2 == 0:
            story.append(PageBreak())

    # ── APÊNDICE B ──
    p(story, "Apêndice B — Banco de frases da Academia", s["h1"])
    story.append(hr())
    frases = [
        "O alarme tocou, e não há fogo.",
        "Isto é adrenalina. Adrenalina é segura.",
        "Eu não preciso vencer a discussão para atravessar o corredor.",
        "O pico não é o fim da história — é o meio.",
        "A água não esquentou; eu é que fiquei.",
        "Previsão não é fato. Vou anotar os dois e comparar.",
        "Eu sei que você está aí. Você pode ficar.",
        "Quem manda na escada é quem sobe.",
        "Um degrau de cada vez, e o topo chega sozinho.",
        "Tropeço não desfaz escada.",
        "Coragem não é uma fogueira: é uma fila de fósforos.",
        "O medo pode ir junto — no banco do passageiro.",
    ]
    for f in frases:
        p(story, f"• <i>“{f}”</i>", s["body_left"])
    story.append(Spacer(1, 8))
    p(story, "Minhas próprias frases (as que funcionam comigo):", s["label"])
    story.append(blank_lines(8))
    story.append(PageBreak())

    # ── APÊNDICE C ──
    p(story, "Apêndice C — Folhas de treino continuado", s["h1"])
    story.append(hr())
    p(story, "As provações terminam; o treino, não. Use estas folhas para manutenção, para novos degraus e "
      "para os medos que você ainda não enfrentou. Cada folha é uma travessia registrada — e a pilha inteira "
      "é a prova de que você mudou.", s["body"])
    story.append(Spacer(1, 4))
    story.append(caixa("Como usar",
                       "Uma folha por exposição. Previsão escrita antes, realidade escrita depois. "
                       "Reserve o último campo para a frase que você quer levar consigo.", s))
    story.append(PageBreak())

    for i in range(1, 106):
        story.append(exposure_log(s, f"Folha de treino continuado #{i:02d}"))
        story.append(PageBreak())

    # ── APÊNDICE D ──
    p(story, "Apêndice D — Protocolo de tensão aplicada (fobia de sangue, injeção e ferimentos)", s["h1"])
    story.append(hr())
    p(story, "Se você já teve tontura, palidez, náusea ou desmaio diante de sangue, agulhas ou procedimentos, "
      "este apêndice é <b>obrigatório antes</b> de qualquer exposição do seu corredor.", s["body"])
    p(story, "A fobia de sangue-injeção-ferimentos apresenta resposta vasovagal bifásica: a pressão sobe e "
      "depois cai bruscamente, com risco de síncope. Por isso, relaxar durante a exposição é o conselho "
      "errado — o correto é o oposto.", s["body"])
    p(story, "<b>A técnica de Lars-Göran Öst, passo a passo:</b>", s["h3"])
    story.append(bullets([
        "Sente-se em uma cadeira firme, com apoio, em local seguro.",
        "Contraia com força os músculos de braços, tronco e pernas por 10 a 15 segundos, até sentir calor "
        "subir ao rosto. Não prenda a respiração.",
        "Solte a tensão por cerca de 20 segundos — sem relaxamento profundo, apenas aliviando.",
        "Repita 5 ciclos. Treine 3 a 5 vezes por dia durante a primeira semana.",
        "Aplique os ciclos imediatamente antes e durante o procedimento real (coleta, vacina, curativo).",
    ], s["body_left"]))
    p(story, "<b>Hierarquia sugerida para este corredor:</b> fotos → vídeos → manusear seringa fechada → "
      "assistir a uma coleta → aplicar em simulador → acompanhar alguém em coleta → realizar/receber o "
      "procedimento, sempre com tensão aplicada.", s["body"])
    story.append(Spacer(1, 6))
    p(story, "Meu registro de treino de tensão aplicada (dias e sensações):", s["label"])
    story.append(blank_lines(6))
    story.append(PageBreak())

    # ── APÊNDICE E ──
    p(story, "Apêndice E — Exposição com realidade virtual", s["h1"])
    story.append(hr())
    p(story, "As gavetas do observatório guardam uma linha de pesquisa específica: a exposição por realidade "
      "virtual (VRE), área de trabalho acadêmico da Dra. Priscila Palomo. Ambientes digitais imersivos "
      "reproduzem voos, alturas, elevadores e animais com controle total das variáveis.", s["body"])
    story.append(bullets([
        "<b>Controle preciso:</b> intensidade, clima, duração e repetição definidos passo a passo.",
        "<b>Repetição imediata:</b> a mesma decolagem pode ser refeita cinco vezes na mesma sessão.",
        "<b>Acesso:</b> permite começar quem não conseguiria dar o primeiro passo no mundo real.",
        "<b>Ponte validada:</b> metanálises indicam eficácia comparável à exposição in vivo, com boa "
        "transferência para situações reais.",
    ], s["body_left"]))
    p(story, "A realidade virtual não substitui a travessia real: ela constrói os primeiros degraus com "
      "segurança para que a travessia real aconteça.", s["body"])
    story.append(PageBreak())

    # ── APÊNDICE F ──
    p(story, "Apêndice F — Manutenção trimestral (o ancinho de amanhã)", s["h1"])
    story.append(hr())
    p(story, "Como o jardim de pedras do Monge Kaito, a sua liberdade precisa de manutenção. Faça este "
      "check-in a cada três meses.", s["body"])
    for t in range(1, 5):
        p(story, f"<b>Trimestre {t}</b>", s["h2"])
        p(story, "O que continuo fazendo que antes evitava:", s["label"])
        story.append(blank_lines(2))
        p(story, "Esquivas silenciosas que voltaram (e como vou desmontá-las):", s["label"])
        story.append(blank_lines(2))
        p(story, "Minhas exposições de reforço agendadas para os próximos 3 meses:", s["label"])
        story.append(blank_lines(2))
        if t % 2 == 0:
            story.append(PageBreak())

    # ── APÊNDICE G ──
    p(story, "Apêndice G — Termo de aliança com a coragem", s["h1"])
    story.append(hr())
    p(story, "Eu, ______________________________________________________________, declaro que li esta "
      "história e reconheci nela a minha própria. Assumo, a partir de hoje, três compromissos:", s["body"])
    story.append(bullets([
        "<b>Não sair no pico.</b> Vou permanecer até a curva descer, ou até conseguir fazer algo que não "
        "conseguia no primeiro minuto.",
        "<b>Escrever antes e depois.</b> Previsão de um lado, realidade do outro, sempre.",
        "<b>Voltar em 48 horas.</b> Se eu fugir, retomo em dois dias, um degrau abaixo, sem me castigar.",
    ], s["body_left"]))
    story.append(Spacer(1, 10))
    p(story, "Meu degrau 10 — a vida que eu vou reconquistar:", s["label"])
    story.append(blank_lines(3))
    story.append(Spacer(1, 10))
    p(story, "Assinatura: ______________________________________  &nbsp;&nbsp; Data: ____ / ____ / ________", s["field"])
    story.append(Spacer(1, 14))
    p(story, "“O volante é meu.”", s["quote"])
    story.append(PageBreak())

    # ── APÊNDICE H ──
    p(story, "Apêndice H — Glossário da Academia", s["h1"])
    story.append(hr())
    glossario = [
        ("Alarme falso", "Ativação completa da resposta de medo sem perigo real correspondente (Barlow)."),
        ("Amígdala", "Estrutura cerebral que detecta ameaça e dispara a resposta de medo antes da análise consciente."),
        ("Aprendizado inibitório", "Memória nova de segurança que compete com a memória antiga de medo; não a apaga."),
        ("Comportamento de segurança", "Ação feita dentro da situação temida para evitar a catástrofe imaginada; mantém o medo."),
        ("DSM-5-TR", "Manual diagnóstico da Associação Americana de Psiquiatria; define os critérios de fobia específica."),
        ("Eixo HPA", "Sistema hipotálamo-hipófise-adrenal, responsável pela resposta hormonal ao estresse."),
        ("Esquiva", "Evitar antecipadamente a situação temida; principal mantenedor da fobia."),
        ("Exposição in vivo", "Contato real, planejado e gradual com o estímulo temido — tratamento de primeira linha."),
        ("Habituação", "Redução espontânea da resposta de ansiedade com a permanência prolongada no estímulo."),
        ("Hierarquia (escada)", "Lista ordenada de situações do menos ao mais ansiogênico, base do tratamento."),
        ("Protocolo Unificado", "Tratamento transdiagnóstico de Barlow focado em regulação emocional e ação contrária."),
        ("Reforço negativo", "Aumento de um comportamento (fugir) por remover algo aversivo (a ansiedade)."),
        ("Retorno do medo", "Reaparecimento do sintoma por renovação, reinstauração ou recuperação espontânea."),
        ("SUDS", "Escala subjetiva de desconforto, de 0 a 10, usada para graduar e monitorar a exposição."),
        ("Tensão aplicada", "Técnica de Öst para fobia de sangue/injeção: contrair a musculatura para evitar síncope."),
        ("Violação de expectativa", "Descoberta de que a catástrofe prevista não ocorreu; motor do tratamento (Craske)."),
    ]
    for termo, definicao in glossario:
        p(story, f"• <b>{termo}:</b> {definicao}", s["body"])
    story.append(PageBreak())

    # ── APÊNDICE I ──
    p(story, "Apêndice I — Onde continuar", s["h1"])
    story.append(hr())
    p(story, "<b>Dra. Priscila Palomo</b> — Psicóloga, CRP 98007. Doutora em Psicologia pela Universitat de "
      "València. Especialista em fobias, Terapia Cognitivo-Comportamental e exposição por realidade virtual. "
      "Atendimento online e presencial em São Paulo.", s["body"])
    story.append(bullets([
        "Site: www.priscilapalomo.com",
        "Programa Escada Segura: www.priscilapalomo.com/escada-segura.html",
        "Materiais e protocolos: www.priscilapalomo.com/loja.html",
        "WhatsApp: (11) 95069-0537",
        "Em crise, ligue para o CVV: 188 (gratuito, 24 horas, em todo o Brasil).",
    ], s["body_left"]))
    story.append(Spacer(1, 10))
    p(story, "Leituras recomendadas: Barlow, D. H. — <i>Anxiety and Its Disorders</i> e <i>Unified Protocol</i>; "
      "Craske, M. et al. (2014) — <i>Maximizing exposure therapy: an inhibitory learning approach</i>; "
      "Öst, L.-G. — trabalhos sobre tensão aplicada e tratamento em sessão única; "
      "APA — <i>DSM-5-TR</i>.", s["small"])
    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceBefore=6, spaceAfter=10))
    p(story, "A Escada Segura — a jornada de Íris Valente · Dra. Priscila Palomo · CRP 98007", s["footer"])

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"OK: {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
