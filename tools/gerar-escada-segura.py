#!/usr/bin/env python3
"""Gera o livro ilustrado e carinhoso:
'Harry Potter e a Magia da Coragem: As Aventuras de um Menino Medroso e seu Coração Apaixonado'

Contado em linguagem lúdica para criança de 5 anos:
- Protagonista: Harry Potter (um bruxinho bondoso com muitas fobias: escuro, altura,
  aranhas, barulhos, água funda, agulhas, ficar sozinho, cães, etc.).
- A cada capítulo: uma fobia mágica enfrentada por Harry com uma historinha fofa,
  seguida da explicação da Psicologia (TCC, David H. Barlow, Pavlov, Skinner,
  habituação, alarme falso, respiração, regulação, dessensibilização sistemática).
- Sem folhas de exercícios (leitura pura de romance ilustrado).
- Ao longo da jornada, a amizade com Hermione se transforma num romance bobinho,
  doce, cheio de bochechas vermelhas e frio gostoso na barriga.
- Termina com um casamento mágico e um 'Felizes Para Sempre'.
"""

from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable, Image,
)

NAVY = HexColor("#0E4A57")
GOLD = HexColor("#D48806")
ORANGE = HexColor("#E27A2E")
INK = HexColor("#111111")
MUTED = HexColor("#555555")
LINE = HexColor("#E0D6C8")
PALE = HexColor("#FBF7F0")
WARM_BOX = HexColor("#F5EFE6")
HEART_PINK = HexColor("#D84A75")

ROOT_DIR = Path(__file__).resolve().parents[1]
IMG = ROOT_DIR / "assets" / "img" / "escada"
OUT = ROOT_DIR / "pdfs" / "programa-escada-segura.pdf"


def styles():
    base = getSampleStyleSheet()
    s = {}
    s["cover_brand"] = ParagraphStyle(
        "cover_brand", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=11, textColor=NAVY, alignment=TA_CENTER, spaceAfter=6,
    )
    s["cover_title"] = ParagraphStyle(
        "cover_title", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=25, textColor=INK, alignment=TA_CENTER, leading=30, spaceAfter=10,
    )
    s["cover_sub"] = ParagraphStyle(
        "cover_sub", parent=base["Normal"], fontName="Helvetica",
        fontSize=12, textColor=MUTED, alignment=TA_CENTER, leading=17, spaceAfter=6,
    )
    s["part"] = ParagraphStyle(
        "part", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=11, textColor=ORANGE, alignment=TA_LEFT, spaceBefore=0, spaceAfter=2,
    )
    s["h1"] = ParagraphStyle(
        "h1", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=16, textColor=NAVY, spaceBefore=0, spaceAfter=5, leading=20,
    )
    s["h2"] = ParagraphStyle(
        "h2", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=12, textColor=INK, spaceBefore=6, spaceAfter=3, leading=15,
    )
    s["prosa"] = ParagraphStyle(
        "prosa", parent=base["Normal"], fontName="Helvetica",
        fontSize=10, textColor=INK, alignment=TA_JUSTIFY, leading=15.2,
        spaceAfter=6, firstLineIndent=14,
    )
    s["prosa_first"] = ParagraphStyle(
        "prosa_first", parent=s["prosa"], firstLineIndent=0,
    )
    s["quote"] = ParagraphStyle(
        "quote", parent=base["Normal"], fontName="Helvetica-Oblique",
        fontSize=10, textColor=HEART_PINK, alignment=TA_CENTER, leading=14,
        spaceBefore=6, spaceAfter=6, leftIndent=10, rightIndent=10,
    )
    s["box_title"] = ParagraphStyle(
        "box_title", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=10.5, textColor=NAVY, alignment=TA_LEFT, leading=13,
    )
    s["box_body"] = ParagraphStyle(
        "box_body", parent=base["Normal"], fontName="Helvetica",
        fontSize=9.2, textColor=INK, alignment=TA_JUSTIFY, leading=13.6,
    )
    s["small"] = ParagraphStyle(
        "small", parent=base["Normal"], fontName="Helvetica",
        fontSize=8.5, textColor=MUTED, leading=12, spaceAfter=4,
    )
    s["toc"] = ParagraphStyle(
        "toc", parent=base["Normal"], fontName="Helvetica",
        fontSize=9, textColor=INK, leading=13.5, spaceAfter=2,
    )
    return s


def hr():
    return HRFlowable(width="100%", thickness=1, color=LINE, spaceBefore=2, spaceAfter=6)


def ilustra(nome, largura=6.0 * cm):
    img_path = IMG / (nome + ".png")
    if not img_path.exists():
        return Spacer(1, 1)
    img = Image(str(img_path))
    ratio = img.imageHeight / float(img.imageWidth)
    img.drawWidth = largura
    img.drawHeight = largura * ratio
    img.hAlign = "CENTER"
    return img


def caixa_psico(titulo, texto, s):
    header = [Paragraph(f"🧠 <b>Segredo da Psicologia:</b> {titulo}", s["box_title"])]
    body = [Paragraph(texto, s["box_body"])]
    conteudo = header + [Spacer(1, 3)] + body
    t = Table([[c] for c in conteudo], colWidths=[16.5 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), WARM_BOX),
        ("BOX", (0, 0), (-1, -1), 1, GOLD),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return KeepTogether([t, Spacer(1, 4)])


def add_page_number(canvas, doc):
    canvas.saveState()
    page = canvas.getPageNumber()
    if page > 1:
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawCentredString(
            A4[0] / 2, 1.2 * cm,
            f"Harry Potter e a Magia da Coragem  ·  Dra. Priscila Palomo  ·  p. {page}"
        )
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.4)
        canvas.line(2 * cm, 1.5 * cm, A4[0] - 2 * cm, 1.5 * cm)
    canvas.restoreState()


def p(story, text, style):
    story.append(Paragraph(text, style))


def capitulo(story, num, tag, titulo, img, cena_paragrafos, psico_titulo, psico_texto, toque_romance, s):
    p(story, f"CAPÍTULO {num:02d} · {tag.upper()}", s["part"])
    p(story, titulo, s["h1"])
    story.append(hr())
    if img:
        story.append(ilustra(img, 5.0 * cm))
        story.append(Spacer(1, 4))
    for i, texto in enumerate(cena_paragrafos):
        p(story, texto, s["prosa_first"] if i == 0 else s["prosa"])
    if toque_romance:
        story.append(Spacer(1, 2))
        p(story, f"💖 <i>{toque_romance}</i>", s["quote"])
    story.append(Spacer(1, 4))
    story.append(caixa_psico(psico_titulo, psico_texto, s))
    story.append(PageBreak())


# ═════════════════════════════════════════════════════════════════════════
# DADOS DOS 20 CAPÍTULOS
# ═════════════════════════════════════════════════════════════════════════

CAPITULOS = [
    # 01
    dict(
        num=1,
        tag="O Armário debaixo da Escada",
        titulo="O Menino Bruxo que Tinha Medo de Tudo",
        img="alarme",
        cena=[
            "Era uma vez um bruxinho muito fofo chamado Harry Potter. Ele tinha cabelos pretos "
            "sempre despenteados, óculos redondos grandões e uma marquinha de raio na testa. "
            "Todo mundo achava que, por ser bruxo, Harry era o menino mais corajoso do planeta. "
            "Mas a verdade é que o coraçãozinho de Harry batia feito um tamborzinho assustado "
            "por quase qualquer coisinha!",
            "Quando a noite caía e as luzes se apagavam no seu quartinho debaixo da escada, "
            "Harry cobria a cabeça com três cobertores. Ele tinha pavor do escuro! Achava que "
            "monstrinhos de sombras iriam puxar seus pés de meia. Quando via uma sombra na parede, "
            "dava um gritinho: 'Socorro, um dragão gigante!'. Mas quando acendia o abajur... era só "
            "a orelha do seu ursinho de pelúcia.",
            "Um dia, uma menininha muito esperta de cabelos cacheados e cheios de folhinhas de livros, "
            "chamada Hermione Granger, bateu na porta do armário segurando uma velinha e uma maçã.",
            "— Harry, você não é covarde — disse ela, com a voz mais doce do castelo. — Seu "
            "alarminho interno só está apitando alto demais!",
        ],
        toque_romance="Hermione segurou a mão de Harry no escuro. As bochechas de Harry ficaram vermelhinhas como cerejas e ele sentiu borboletas fazendo piruetas na barriga.",
        psico_tit="O Alarme Falso da Amígdala (David H. Barlow)",
        psico_txt="Na Psicologia, o medo é um alarme que mora no cérebro (na amígdala). Quando temos uma fobia, esse alarme é como um sensor de incêndio que apita alto só porque alguém fez uma torradinha saborosa! Não tem fogo nenhum; é apenas um alarme falso que aprendeu a gritar à toa. A terapia ensina o cérebro a recalibrar o alarme com calma.",
    ),

    # 02
    dict(
        num=2,
        tag="A Aula de Voo",
        titulo="O Medo de Voar de Vassoura e Subir Alto",
        img="escada",
        cena=[
            "Na primeira aula de voo no castelo de Hogwarts, todos os alunos montaram em suas vassouras "
            "mágicas. Os outros bruxinhos subiram até as nuvens dando piruetas felizes, mas Harry "
            "ficou grudado no chão, segurando a vassoura com tanta força que os dedinhos ficaram brancos.",
            "— Se eu subir cinco centímetros, eu vou cair, quebrar todos os meus ossinhos e virar "
            "uma panqueca de bruxo! — pensava Harry, com os joelhinhos tremendo.",
            "Hermione desceu de sua vassoura, sentou na grama macia ao lado dele e disse:",
            "— Harry, ninguém precisa voar até as nuvens no primeiro dia. Que tal a gente subir só "
            "na altura de uma formiguinha? Um dedinho hoje, dois dedinhos amanhã, degrau por degrau!",
            "Harry subiu apenas a altura de uma maçã do chão. Respirou fundo... e viu que não caiu! "
            "Hermione bateu palminhas de alegria.",
        ],
        toque_romance="Hermione deu um sorrisinho tão brilhante que Harry esqueceu que tinha medo de altura. Ele só conseguia olhar para os olhinhos castanhos dela, com o coração dando pulinhos.",
        psico_tit="Hierarquia e Dessensibilização Sistemática (Joseph Wolpe)",
        psico_txt="A Terapia Cognitivo-Comportamental (TCC) ensina que para vencer um medo grande, a gente nunca pula no topo de uma vez. A gente constrói uma escadinha com degraus bem pequenininhos. Ao subir um degrau fácil por vez, o cérebro percebe que está seguro e a ansiedade vai embora sem sustos.",
    ),

    # 03
    dict(
        num=3,
        tag="A Floresta Proibida",
        titulo="A Aranha de Oito Patinhas Peludas",
        img="monstrinho",
        cena=[
            "Durante um passeio pelo jardim do castelo, Harry deu de cara com uma aranhinha "
            "minúscula, menor do que um grão de feijão, descendo por um fio de teia. Harry deu um pulo "
            "de dois metros para trás, gritou bem alto e quase subiu numa árvore!",
            "— Ela tem oito olhos e dentes de monstro! Ela vai me devorar todinho! — gritava ele, "
            "escondendo o rosto atrás da capa.",
            "Hermione pegou uma folha seca e deixou a aranhinha caminhar por ela devagarzinho.",
            "— Olha bem, Harry. Ela é do tamanho de uma pedrinha. O nome dela é Cotó e ela só "
            "gosta de comer mosquitinhos chatos. Toda vez que você sai correndo, seu cérebro acha "
            "que você só sobreviveu porque fugiu. Mas se você olhar para ela por três minutinhos, "
            "vai ver que ela não faz nada!",
            "Harry espiou por entre os dedos. A aranhinha bocejou e foi embora. Nada de ruim aconteceu!",
        ],
        toque_romance="Para dar coragem, Hermione colocou a mãozinha sobre a dele. Harry sentiu um calorzinho tão bom no peito que a aranha virou a coisa menos importante do mundo.",
        psico_tit="O Ciclo do Reforço Negativo (Mowrer & Skinner)",
        psico_txt="Quando a gente foge de uma coisinha que dá medo, sentimos um alívio na hora. Mas esse alívio engana o cérebro, fazendo ele achar que a fuga foi o que nos salvou. Isso se chama reforço negativo. Na terapia, aprender a ficar e observar desmonta essa armadilha e o medo encolhe até sumir.",
    ),

    # 04
    dict(
        num=4,
        tag="O Lago Negro",
        titulo="A Piscina Fria e o Segredo de Esperar",
        img="piscina",
        cena=[
            "Era um dia quente de sol em Hogwarts e todos foram brincar na beira do Lago Negro. "
            "Harry colocou apenas a pontinha do dedão do pé na água e deu um pulo para trás, "
            "arrepiado: 'BRRRR! ESTÁ CONGELANTE! VOU VIRAR UM PICOLÉ DE BRUXO!'.",
            "Hermione entrou na água até os joelhos, espirrou umas gotinhas nele e chamou com carinho:",
            "— Entra aqui comigo e segura minha mão, Harry. Vamos contar até cem sem sair. Você "
            "vai ver uma mágica que não precisa de varinha!",
            "Harry entrou tremendo. No primeiro minuto, bateu o queixo. No segundo minuto, achou suportável. "
            "No quarto minuto, olhou espantado para Hermione: 'Nossa... a água ficou quentinha!'.",
            "— A água continua igual, bobinho — riu Hermione. — Foi o seu corpinho que se acostumou!",
        ],
        toque_romance="Eles ficaram brincando de jogar água um no outro. Quando uma gotinha molhou o nariz de Hermione, ela soltou uma gargalhada tão linda que Harry desejou que aquela tarde durasse para sempre.",
        psico_tit="O Processo Natural de Habituação (Psicofisiologia)",
        psico_txt="O nosso corpo é incrível: quando sentimos medo ou frio, o coração acelera no começo, mas o organismo não consegue ficar acelerado para sempre. Se você ficar na situação sem fugir, a adrenalina baixa sozinha em poucos minutos. Isso se chama habituação. A água não esquenta: é você que se acostuma!",
    ),

    # 05
    dict(
        num=5,
        tag="A Aula de Poções",
        titulo="O Medo de Agulha e a Picadinha de Abelha",
        img="cachorrinho",
        cena=[
            "Madame Pomfrey, a enfermeira bondosa de Hogwarts, avisou que todos os bruxinhos "
            "precisavam tomar uma gotinha de poção protetora com uma agulhinha bem pequenina. "
            "Quando Harry viu aquela pontinha de metal brilhando, ficou pálido feito cera de vela, "
            "a pressão dele despencou e ele quase caiu desmaiado no chão!",
            "Hermione correu, colocou Harry sentado numa cadeira firme e disse bem rápido:",
            "— Harry, aperte todos os seus músculos com força! Aperte as perninhas, a barriguinha e os "
            "bracinhos como se você fosse um super-herói de pedra durão!",
            "Harry contraiu todos os músculos por quinze segundos. O sangue subiu de volta para as "
            "bochechas, o rosto ficou quentinho e a tontura sumiu na hora! Quando Madame Pomfrey deu a "
            "picadinha... parecia só uma mordidinha de formiga.",
        ],
        toque_romance="Hermione colocou um curativo com desenho de coraçãozinho no braço de Harry e deu um beijinho de sopro por cima. Harry ficou tão vermelho que parecia um pimentão feliz.",
        psico_tit="Técnica de Tensão Aplicada para Fobia de Sangue (Lars-Göran Öst)",
        psico_txt="A fobia de sangue e agulha é a única em que a pressão arterial pode cair de repente, causando desmaio. Por isso, relaxar é o conselho errado! A técnica certa, criada pelo cientista Lars-Göran Öst, é tencionar os músculos do corpo com força para empurrar a pressão para cima e não desmaiar.",
    ),

    # 06
    dict(
        num=6,
        tag="A Noite de Tempestade",
        titulo="Soprar as Velinhas e o Freio Mágico",
        img="velinha",
        cena=[
            "Certa noite, caiu um temporal enorme sobre o castelo. Trovões estrondosos faziam os "
            "vidros vibrarem: 'CABUM!'. Harry sentiu o coraçãozinho bater tão rápido no peito que "
            "parecia um cavalinho galopando sem freio. Ele respirava bem curtinho e achava que ia sufocar.",
            "Hermione acendeu uma velinha aromática de baunilha e sentou-se na frente dele.",
            "— Harry, nosso corpo tem um pedal de acelerador e um pedal de freio mágico! Toda vez que "
            "o susto pisa no acelerador, a gente pisa no freio soprando velinhas. Vamos juntos?",
            "— Puxa o ar pelo nariz cheirando uma florzinha perfumada... 1, 2, 3, 4! Agora solta pela "
            "boca soprando a velinha devagarinho sem querer apagar... 1, 2, 3, 4, 5, 6!",
            "Harry fez dez respirações mágicas com Hermione. Em poucos minutos, o cavalinho do coração "
            "desacelerou e a calmaria voltou para o peito.",
        ],
        toque_romance="Eles ficaram sentados lado a lado no parapeito da janela olhando os raios, enrolados no mesmo cobertor quentinho. Hermione encostou a cabecinha no ombro de Harry, e ele sentiu uma paz gigantesca.",
        psico_tit="Respiração Diafragmática e Ativação do Nervo Vago",
        psico_txt="Quando respiramos rápido de susto, o oxigênio fica desregulado no sangue e dá tontura. Mas ao soltar o ar pela boca bem devagarzinho (tempo prolongado), acionamos o nervo vago e o sistema parassimpático, que funciona como o freio biológico do corpo, diminuindo os batimentos cardíacos.",
    ),

    # 07
    dict(
        num=7,
        tag="O Cão de Três Cabeças",
        titulo="Fofo, o Cachorrão que Parecia Feroz",
        img="cachorrinho",
        cena=[
            "No terceiro andar do castelo morava Fofo, um cão enorme de três cabeças. Harry "
            "tinha tanto medo de cachorros que atravessava o corredor na ponta dos pés para não "
            "ouvir nem um latidinho. 'Cachorros mordem, pulam e rasgam calças!', pensava ele.",
            "Hermione descobriu que Fofo adorava ouvir historinhas e música suave. Ela levou uma "
            "harpa pequenina e sentou-se a cinco metros de distância, enquanto Harry observava seguro "
            "atrás de um pilar.",
            "Primeiro, Harry só olhou de longe. Depois, chegou a três metros. No terceiro dia, sentou "
            "ao lado de Hermione e ofereceu um biscoitinho saboroso para a cabeça do meio de Fofo. "
            "O cachorrão abanou o rabo enorme e deu uma lambidinha carinhosa na mão de Harry!",
            "— Ele só queria um carinho! — riu Harry, surpreso.",
        ],
        toque_romance="Hermione sorriu orgulhosa e ajeitou a franja de Harry com a pontinha dos dedos. O toque macio fez a espinha de Harry arrepiar de um jeito muito gostoso.",
        psico_tit="Extinção Respondente e Modelação Vicária (Bandura & Pavlov)",
        psico_txt="O cientista Albert Bandura provou que quando a gente vê outra pessoa querida se aproximando com calma de algo que dava medo, nosso cérebro aprende por imitação que aquilo é seguro. Junto com petiscos e carinho (reforço positivo), a resposta de pânico se extingue e dá lugar à amizade.",
    ),

    # 08
    dict(
        num=8,
        tag="A Aula de Adivinhação",
        titulo="Os Pensamentos de Catástrofe e a Bola de Cristal",
        img="monstrinho",
        cena=[
            "Na torre alta de Adivinhação, a professora pedia para olharem bolas de cristal. Toda vez "
            "que Harry olhava para a névoa, sua cabecinha inventava tragédias: 'Amanhã eu vou errar o "
            "feitiço na frente de todos, todo mundo vai rir de mim e eu serei expulso de Hogwarts!'.",
            "Hermione pegou um pedaço de pergaminho e uma pena mágica.",
            "— Harry, sua cabecinha está usando óculos mágicos de aumentar monstros! Vamos fazer o teste "
            "do detetive: quantas vezes você achou que ia ser expulso? Dez vezes. E quantas vezes você foi "
            "expulso de verdade? Zero!",
            "— É verdade... — pensou Harry. — O que eu imagino quase nunca acontece na vida real!",
            "— Pensamento não é fato, Harry. É só uma historinha que a cabeça conta quando está com medo.",
        ],
        toque_romance="Hermione escreveu no pergaminho: 'Você é o melhor bruxinho do mundo' com um coraçãozinho no final. Harry guardou o bilhete no bolso mais perto do coração.",
        psico_tit="Reestruturação Cognitiva e Erro de Predição (Aaron T. Beck)",
        psico_txt="Aaron Beck, o criador da Terapia Cognitiva, mostrou que o medo mente para nós criando pensamentos catastróficos automáticos. Na terapia, agimos como detetives: testamos se as profecias do medo são verdadeiras ou se são apenas distorções mentais. Quando a realidade desmente a catástrofe, a mente se liberta.",
    ),

    # 09
    dict(
        num=9,
        tag="O Salão Principal",
        titulo="Falar em Público e as Bochechas de Maçã",
        img="velinha",
        cena=[
            "O professor Dumbledore chamou Harry para ler um poema na frente de todos os alunos "
            "no Salão Principal. Harry sentiu as pernas virarem gelatina: 'E se minha voz sumir? "
            "E se eu gaguejar e todo mundo achar que sou um bobo?'. Ele queria se esconder embaixo da mesa!",
            "Hermione segurou suas duas mãos e olhou fundo nos olhos verdes dele:",
            "— Harry, todo mundo fica com vergonha às vezes. Se você gaguejar, não tem problema nenhum! "
            "Ninguém vai deixar de gostar de você por isso. Eu vou estar na primeira fila sorrindo para você.",
            "Harry subiu no banquinho com o coração a mil. Olhou para a primeira fila e viu Hermione acenando. "
            "Ele leu o poema todinho. Gaguejou numa palavrinha, riu de si mesmo... e o Salão inteiro "
            "aplaudiu de pé!",
        ],
        toque_romance="Quando Harry desceu do palco, Hermione correu e deu um abraço tão apertado nele que o perfume de baunilha dos cabelos dela ficou na capa dele o resto do dia.",
        psico_tit="Descatastrofização da Ansiedade Social e Aceitação",
        psico_txt="A timidez e o medo de falar em público vêm da crença de que precisamos ser perfeitos para sermos aceitos. Quando aceitamos que errar é normal e que as pessoas não nos julgam com a severidade que imaginamos, a vergonha perde o poder e a espontaneidade floresce.",
    ),

    # 10
    dict(
        num=10,
        tag="A Masmorra das Poções",
        titulo="Lugares Apertados e a Janelinha da Mente",
        img="escada",
        cena=[
            "Para a aula do professor Snape, eles precisaram entrar no depósito de ingredientes, "
            "uma salinha subterrânea pequena e sem janelas. A porta bateu com um vento: 'TRANC!'. "
            "Harry entrou em pânico claustrofóbico: 'O ar vai acabar! Estamos presos para sempre!'.",
            "Hermione não correu para forçar a fechadura. Ela sentou no chão de pernas cruzadas e disse:",
            "— Harry, o ar não acaba numa sala fechada. Tem ar aqui dentro para um mês inteiro! "
            "Senta comigo, respira o sopro da velinha e vamos olhar cinco coisas azuis na sala.",
            "Harry procurou: um frasco azul, um livro azul, o cachecol de Hermione... Ao focar a atenção "
            "no ambiente real em vez do pânico da cabeça, o aperto no peito foi sumindo. Dois minutos depois, "
            "o professor abriu a porta normalmente.",
        ],
        toque_romance="Enquanto estavam no quartinho, Hermione segurou a mão de Harry na penumbra. Harry pensou em segredo que ficaria preso naquele quartinho por cem anos se fosse com ela.",
        psico_tit="Técnica de Ancoragem Sensorial 5-4-3-2-1 e Claustrofobia",
        psico_txt="Em lugares fechados, a mente fóbica cria a ilusão de asfixia. A técnica de ancoragem traz a atenção de volta para os cinco sentidos (ver cores, tocar texturas, ouvir sons), tirando o cérebro do modo de pânico imaginado e restabelecendo a calma no momento presente.",
    ),

    # 11
    dict(
        num=11,
        tag="A Torre de Astronomia",
        titulo="O Medo de Altura e a Escadinha de Madeira",
        img="escada",
        cena=[
            "A aula de Astronomia era no ponto mais alto do castelo: a grande torre redonda. Harry "
            "olhou para a escada em espiral de cem degraus de pedra e travou no primeiro:",
            "— Minha cabeça gira só de olhar para cima! Se eu subir, o chão vai sumir!",
            "Hermione não puxou o braço dele. Ela subiu três degraus, sentou e bateu na madeira:",
            "— Harry, você não precisa subir tudo hoje. Sobe só até o degrau três comigo. Vamos comer "
            "um sapinho de chocolate aqui e descer rindo.",
            "No primeiro dia foram até o três. No segundo dia, até o degrau dez. No quinto dia, estavam "
            "no topo da torre admirando a lua cheia mais linda de todas!",
        ],
        toque_romance="No alto da torre sob a luz da lua, um ventinho frio soprou e Hermione se aconchegou perto de Harry. O coração de Harry bateu tão forte que ele achou que ela conseguiria ouvir o tum-tum apaixonado.",
        psico_tit="Exposição Gradual In Vivo e Autoeficácia (Bandura)",
        psico_txt="A autoeficácia é a confiança prática de que somos capazes de realizar algo. Ela não nasce de palestras, mas de pequenas vitórias acumuladas. Cada degrau conquistado com sucesso gera um registro neurológico de vitória que alimenta a coragem para o próximo passo.",
    ),

    # 12
    dict(
        num=12,
        tag="O Bicho-Papão no Guarda-Roupa",
        titulo="O Monstrinho que Vira Palhaço",
        img="monstrinho",
        cena=[
            "Na aula do professor Lupin, havia um guarda-roupa que balançava. Lá dentro morava o "
            "Bicho-Papão, um monstrinho travesso que se transformava no pior medo de quem olhasse para ele. "
            "Quando a porta abriu, Harry viu uma criatura escura e assustadora.",
            "— Lembre-se do feitiço, Harry! — sussurrou Hermione ao lado dele. — O medo só tem poder "
            "se a gente levar ele a sério demais. Transforme ele numa coisa engraçada!",
            "Harry ergueu a varinha e gritou: 'RIDDIKULUS!'. O monstrinho assustador ganhou patins de "
            "rodinhas nos pés, escorregou numa casca de banana e caiu de bumbum no chão usando um chapéu "
            "de palhaço com florzinha d'água!",
            "A sala inteira gargalhou e o monstrinho explodiu em fumaça de confetes coloridos.",
        ],
        toque_romance="Hermione riu tanto que lágrimas brilharam nos olhinhos dela. Ela abraçou o pescoço de Harry: 'Você foi brilhante!'. Harry sentiu que poderia voar até as estrelas sem vassoura.",
        psico_tit="Desfusão Cognitiva e Humor na TCC (Terapia de Aceitação e Compromisso)",
        psico_txt="A desfusão cognitiva ensina a olhar para os nossos pensamentos assustadores como meras palavras e imagens, e não como verdades absolutas. Ao usar o humor e a ludicidade para brincar com o monstro do medo, retiramos a carga aterrorizante e desarmamos o ciclo de ansiedade.",
    ),

    # 13
    dict(
        num=13,
        tag="A Cabana de Hagrid",
        titulo="O Dragãozinho Soltador de Fumaça",
        img="dragao",
        cena=[
            "Hagrid, o gigante de coração mole, adotou um dragãozinho bebê chamado Norberto. "
            "Toda vez que Norberto se assustava, soltava labaredas de fogo pelas ventas e rugia alto. "
            "Harry quase correu para a floresta de pavor.",
            "— Não corra, Harry! — ensinou Hermione, pegando uma bacia de frutinhas doces. — O dragão não "
            "está com raiva. Ele está assustado e com frio. Se a gente gritar e jogar água, ele cospe mais fogo. "
            "Se a gente respirar fundo e chegar com carinho, ele se acalma.",
            "Harry deu três passos calmos, respirou a florzinha e estendeu a mãozinha com uma maçã. "
            "O dragãozinho parou de soltar fogo, cheirou os dedos de Harry e deitou a cabecinha no colo dele, "
            "ronronando como um gatinho gigante.",
        ],
        toque_romance="Enquanto faziam carinho no dragão, as mãos de Harry e Hermione se tocaram sobre as escamas quentinhas. Eles entrelaçaram os dedinhos e trocaram um olhar tão doce que o dragãozinho soltou fumacinha em forma de coração.",
        psico_tit="Aceitação Emocional Plena vs. Supressão (David H. Barlow)",
        psico_txt="David Barlow explica no Protocolo Unificado que tentar lutar contra a ansiedade ou suprimi-la à força só aumenta a sua intensidade (efeito rebote). A verdadeira coragem consiste em acolher a emoção com gentileza e respirar junto com ela até que a energia se transforme em presença.",
    ),

    # 14
    dict(
        num=14,
        tag="A Prova na Floresta",
        titulo="O Dia em que Harry Tropeçou no Medo",
        img="alarme",
        cena=[
            "Num dia chuvoso e cansativo, Harry estava com sono e com fome. Ao ouvir um barulho de galho "
            "se quebrando na floresta, ele se assustou e saiu correndo desesperado até o castelo, "
            "trancando-se no quarto chorando:",
            "— Eu sou um fracasso! Achei que tinha ficado corajoso, mas o medo voltou todinho!",
            "Hermione bateu na porta, entrou com uma xícara de chocolate quente com canela e sentou na beirada da cama.",
            "— Harry, tropeçar no caminho não apaga os passos que você já deu. Você estava cansado e com fome. "
            "Ter medo de novo é super normal! A coragem não é uma linha reta; é como aprender a andar de "
            "bicicleta: às vezes a gente desequilibra, põe o pezinho no chão e monta de novo no dia seguinte.",
            "Harry bebeu o chocolate, limpou as lágrimas e sorriu.",
        ],
        toque_romance="Hermione limpou uma gotinha de chocolate do canto da boca de Harry com o polegar. Harry sentiu o estômago dar cambalhotas de amor e prometeu a si mesmo que nunca desistiria.",
        psico_tit="Prevenção de Recaídas e Normalização do Retorno do Medo",
        psico_txt="Na neurociência, a memória original do medo nunca é deletada; cria-se uma memória nova de segurança que passa a competir com ela. Em dias de estresse, cansaço ou privação de sono, o alarme antigo pode soar de novo. Isso não é fracasso nem volta à estaca zero: é apenas um tropeço passageiro do aprendizado.",
    ),

    # 15
    dict(
        num=15,
        tag="O Beco Diagonal",
        titulo="Os Amuletos de Segurança que Pesavam na Mochila",
        img="monstrinho",
        cena=[
            "Para passear no movimentado Beco Diagonal, Harry carregava uma mochila pesadíssima cheia "
            "de 'coisinhas mágicas de segurança': uma pedrinha da sorte, três poções calmantes no bolso, "
            "um apito de emergência e um lenço da tia.",
            "— Harry, por que sua mochila está tão pesada? — perguntou Hermione.",
            "— Se eu não tiver minha pedrinha e minhas poções, eu sinto que vou passar mal no meio da multidão!",
            "Hermione abriu a mochila com cuidado e tirou uma pedrinha por dia:",
            "— Se você só consegue sair com a pedrinha, seu cérebro acha que a pedrinha é que é corajosa, "
            "e não você! Vamos deixar o apito hoje? Amanhã deixamos a pedrinha. A coragem de verdade mora "
            "no seu peito, não no fundo da mochila.",
            "Harry andou pelo Beco de mãos vazias... e descobriu que continuava seguro!",
        ],
        toque_romance="Hermione segurou o braço dele para atravessar a rua movimentada. Harry sentiu que a melhor proteção do mundo era estar pertinho dela.",
        psico_tit="Desmame Gradual de Comportamentos de Segurança (Safety Behaviors)",
        psico_txt="Comportamentos de segurança são 'muletas' que a pessoa usa para tolerar a situação (levar remédio por garantia, só ir acompanhado, checar saídas). Eles impedem que o cérebro aprenda que a própria pessoa é capaz de suportar o desafio. O desmame progressivo dessas muletas consolida a cura.",
    ),

    # 16
    dict(
        num=16,
        tag="A Sala Precisa",
        titulo="O Espelho Mágico que Mostrava o Futuro",
        img="escada",
        cena=[
            "Na mágica Sala Precisa de Hogwarts, Harry encontrou um grande espelho dourado. "
            "Quando olhou para o vidro, não viu monstros nem fantasmas: viu a si mesmo adulto, "
            "vestindo uma capa bonita de professor de magia, rindo alto, viajando pelo mundo de navio "
            "e voando livre no céu sem nenhum pavor.",
            "— Olha, Hermione! — chamou Harry com os olhos brilhando. — Sou eu sem medo da vida!",
            "Hermione encostou ao lado dele e olhou no espelho. No reflexo, a versão adulta dela "
            "estava de mãos dadas com o Harry adulto, usando uma aliança dourada no dedo.",
            "— Essa é a vida linda que está te esperando, Harry — disse ela com a voz macia. — "
            "Cada degrau de medo que você vence hoje é uma porta aberta para o nosso futuro amanhã.",
        ],
        toque_romance="Harry olhou para Hermione no espelho e depois olhou para a Hermione real ao seu lado. As bochechas dos dois ficaram cor-de-rosa ao mesmo tempo e eles deram risadinhas tímidas.",
        psico_tit="Ação Guiada por Valores e Terapia Focada em Metas de Vida",
        psico_txt="Vencer o medo não é apenas diminuir sintomas: é recuperar a capacidade de viver aquilo que tem valor para nós. Ao conectar o esforço da terapia com sonhos reais (viajar, amar, trabalhar, brincar), a motivação para a mudança se torna inabalável.",
    ),

    # 17
    dict(
        num=17,
        tag="O Grande Salão do Torneio",
        titulo="A Grande Prova Final contra o Medo",
        img="dragao",
        cena=[
            "Chegou o dia do grande teste anual de coragem de Hogwarts. O desafio reunia tudo o que Harry "
            "mais temia: subir numa torre alta, atravessar um corredor escuro, passar ao lado de Fofo e "
            "apresentar uma magia na frente de todo o castelo.",
            "Antigamente, Harry teria fugido para debaixo da cama. Mas naquele dia, ele colocou a mãozinha "
            "no peito, sentiu o coraçãozinho bater forte e disse baixinho:",
            "— Meu alarme está tocando, mas não tem fogo nenhum. Eu sei respirar o freio da velinha, "
            "eu sei subir degrau por degrau e eu não preciso fugir!",
            "Harry entrou no circuito com passos firmes. Subiu a torre com calma, atravessou o escuro "
            "cantando, fez carinho no cachorrão Fofo e subiu no palco com um sorriso confiante. "
            "O castelo inteiro explodiu em aplausos ensurdecedores!",
        ],
        toque_romance="Hermione pulou da arquibancada, correu pelo corredor e pulou no colo de Harry com um abraço tão apertado que os dois giraram no chão rindo e comemorando.",
        psico_tit="Exposição Culminante e Consolidação da Memória Inibitória",
        psico_txt="Quando a pessoa acumula múltiplos ensaios bem-sucedidos e enfrenta o desafio completo, o circuito pré-frontal ventromedial consolida a nova regra de segurança como a resposta padrão do cérebro. O medo perde o controle e a autoeficácia atinge o nível máximo.",
    ),

    # 18
    dict(
        num=18,
        tag="O Jardim de Rosas",
        titulo="O Primeiro Encontro no Vilarejo de Hogsmeade",
        img="velinha",
        cena=[
            "No fim de semana seguinte, Harry convidou Hermione para tomar uma Cerveja Amanteigada "
            "quentinha no vilarejo nevado de Hogsmeade. Era o primeiro passeio a sós dos dois!",
            "Harry passou uma hora penteando os cabelos na frente do espelho (embora continuassem "
            "despenteados como sempre) e escolheu seu cachecol mais bonito. Sentado na mesinha da taverna "
            "cheia de velinhas acesas, ele sentiu um friozinho gostoso na barriga.",
            "— Harry, você está tremendo? — perguntou Hermione, com um sorrisinho travesso. — É medo de novo?",
            "— Não... — confessou Harry, corando até as orelhas. — Esse frio na barriga é diferente. "
            "É o coraçãozinho batendo feliz porque estou com você.",
            "Hermione cobriu a mãozinha dele com a dela na mesa de madeira.",
            "— O meu também está batendo bem rápido, Harry.",
        ],
        toque_romance="Eles tomaram a bebida quentinha dividindo a mesma caneca com dois canudinhos. Quando Hermione ficou com bigodinho de espuma de caramelo, Harry limpou com o guardanapo e os dois riram baixinho de mãos dadas.",
        psico_tit="Diferenciação entre Ansiedade Aversiva e Excitação Afetiva Positiva",
        psico_txt="O corpo usa circuitos semelhantes de ativação fisiológica (coração acelerado, calor, borboletas no estômago) tanto para o susto quanto para a paixão e a alegria. Aprender a discriminar e acolher as sensações gostosas do afeto sem confundi-las com perigo é um grande marco de saúde emocional.",
    ),

    # 19
    dict(
        num=19,
        tag="A Ponte de Pedra",
        titulo="O Primeiro Beijinho de Nariz",
        img="piscina",
        cena=[
            "Ao entardecer, eles caminharam de volta para o castelo pela ponte de pedra antiga. "
            "A neve caía suavemente em floquinhos brancos, brilhando sob os postes de luz dourada. "
            "Harry parou no meio da ponte — aquela mesma ponte alta que antigamente o fazia tremer de pavor. "
            "Mas agora ele não olhava para o abismo: olhava para Hermione.",
            "— Obrigado por me ensinar a ser corajoso, Hermione.",
            "— Você sempre foi corajoso, Harry. Só precisava de alguém que te mostrasse a escadinha.",
            "Harry deu um passinho para frente. O coraçãozinho dele deu um salto triplo de emoção. "
            "Ele fechou os olhinhos e deu um beijinho doce e macio na pontinha do nariz gelado de Hermione. "
            "Hermione deu uma risadinha gostosa, colocou as mãozinhas no rosto dele e deu um beijinho "
            "carinhoso na bochecha dele.",
        ],
        toque_romance="Eles ficaram abraçadinhos no meio da ponte vendo a neve cair, enquanto as lanternas do castelo se acendiam uma a uma como estrelinhas na terra.",
        psico_tit="Vínculo Seguro, Co-Regulação e Afeto Protetor (Teoria do Apego)",
        psico_txt="A teoria do apego de John Bowlby demonstra que ter uma base de apoio segura e afetuosa reduz a vulnerabilidade ao medo e potencializa a coragem exploratória. O amor e a conexão humana são os maiores reguladores emocionais da nossa espécie.",
    ),

    # 20
    dict(
        num=20,
        tag="O Casamento Mágico",
        titulo="Felizes Para Sempre na Casinha com Jardim",
        img="dragao",
        cena=[
            "Os anos passaram voando como pomba mágica no céu de Hogwarts. Harry e Hermione cresceram, "
            "estudaram muito e se tornaram os maiores bruxos do seu tempo.",
            "Num lindo dia de primavera, com o sol dourado brilhando sobre o gramado e música suave no ar, "
            "Harry e Hermione se casaram! Hermione usava um vestido branco bordado com estrelinhas brilhantes "
            "e Harry usava sua melhor capa com uma flor de laranjeira na lapela.",
            "Todos os amigos comemoravam: Hagrid chorava de emoção no lenço gigante, o dragãozinho Norberto "
            "soprava corações de fumaça colorida no céu e o cachorrão Fofo pulava alegre abanando os três rabinhos!",
            "Eles construíram uma linda casinha de pedra clara com um jardim cheio de flores perfumadas, "
            "uma biblioteca enorme de livros de magia e janelas abertas para o sol.",
            "E toda vez que uma noite de tempestade chegava e o trovão fazia 'CABUM!', Harry não corria "
            "mais para debaixo da cama. Ele abraçava Hermione no sofá, tomava um chá quentinho e sorria, "
            "sabendo que com amor, paciência e pequenos degraus de carinho, nenhum medo no mundo pode apagar "
            "a luz da nossa felicidade.",
            "E assim, Harry Potter e Hermione viveram felizes para todo o sempre!",
        ],
        toque_romance="Harry segurou a mão de Hermione, olhou nos olhos castanhos da sua esposa amada e deu um beijo apaixonado, selando a história de amor mais linda de todo o mundo mágico.",
        psico_tit="Resiliência Consolidada, Amor Sustentável e Bem-Estar Vitalício",
        psico_txt="A superação das fobias associada a um relacionamento amoroso seguro produz o que a Psicologia Positiva chama de florescimento humano (Flourishing). O indivíduo deixa de gastar energia defendendo-se de ameaças imaginárias e passa a investir plenamente na construção de uma vida com sentido, amor e alegria duradoura.",
    ),
]


def build():
    s = styles()
    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2.0 * cm,
        title="Harry Potter e a Magia da Coragem",
        author="Dra. Priscila Palomo",
    )
    story = []

    # ═══════════ CAPA ═══════════
    story.append(Spacer(1, 2.0 * cm))
    p(story, "DRA. PRISCILA PALOMO  ·  CRP 98007", s["cover_brand"])
    story.append(Spacer(1, 0.3 * cm))
    story.append(HRFlowable(width="40%", thickness=2, color=NAVY, spaceBefore=0, spaceAfter=14))
    p(story, "Harry Potter e a Magia da Coragem", s["cover_title"])
    p(story, "As Aventuras de um Menino Medroso e seu Coração Apaixonado", s["cover_sub"])
    story.append(Spacer(1, 0.5 * cm))
    story.append(ilustra("dragao", 7.5 * cm))
    story.append(Spacer(1, 0.5 * cm))
    p(story, "“Não existe feitiço mais poderoso do que subir um degrau de cada vez<br/>segurando a mão de quem a gente ama.”", s["quote"])
    story.append(Spacer(1, 0.5 * cm))
    story.append(HRFlowable(width="26%", thickness=1, color=LINE, spaceBefore=0, spaceAfter=12))
    p(story, "Uma linda historinha de superação contada para crianças de 5 anos (e seus pais!),<br/>"
             "ensinando a vencer todas as fobias com a Psicologia e a TCC,<br/>"
             "recheada de bochechas vermelhas, frio na barriga e um final Felizes Para Sempre.", s["cover_sub"])
    story.append(Spacer(1, 0.8 * cm))
    p(story, "www.priscilapalomo.com", s["cover_brand"])
    story.append(PageBreak())

    # ═══════════ CARTA DE ABERTURA / AVISO ÉTICO ═══════════
    p(story, "Uma Cartinha Especial para os Leitores", s["h1"])
    story.append(hr())
    p(story, "Querido(a) leitor(a),", s["prosa_first"])
    p(story, "Todo mundo acha que os heróis dos livros nunca sentem medo de nada. Mas a verdade é que "
      "ter medo é a coisa mais humana e natural do mundo! O medo é apenas um alarminho que o nosso corpo "
      "inventou para nos proteger.", s["prosa"])
    p(story, "Neste livro encantador, você vai acompanhar a história do bruxinho <b>Harry Potter</b>, um "
      "menino doce que tinha medo do escuro, de altura, de aranhas, de agulhas, de falar em público e de "
      "lugares apertados. Com a ajuda da sua melhor amiga e grande amor, <b>Hermione Granger</b>, Harry vai "
      "descobrir que não precisa de varinha mágica para ser valente: basta subir um degrauzinho de cada vez, "
      "respirar devagar e dar risada dos monstrinhos da cabeça.", s["prosa"])
    p(story, "Ao final de cada capítulo, você encontrará o <b>Segredo da Psicologia</b>, explicando de forma "
      "simples e científica como a Terapia Cognitivo-Comportamental (TCC) e os grandes pesquisadores da "
      "mente humana ajudam crianças e adultos a vencerem suas fobias na vida real.", s["prosa"])
    p(story, "<b>Aviso Ético:</b> Este livro tem finalidade lúdica e psicoeducativa. Ele não substitui "
      "o acompanhamento de um psicólogo clínico ou médico quando o sofrimento for intenso.", s["small"])
    story.append(Spacer(1, 8))
    p(story, "Com todo o carinho e votos de muitas borboletas felizes na barriga,<br/>"
             "<b>Dra. Priscila Palomo</b> — Psicóloga Clínica (CRP 98007)<br/>"
             "Doutora em Psicologia · Especialista em Fobias e TCC · www.priscilapalomo.com", s["small"])
    story.append(PageBreak())

    # ═══════════ SUMÁRIO ═══════════
    p(story, "Índice dos Capítulos Encantados", s["h1"])
    story.append(hr())
    p(story, "<i>Acompanhe a jornada de Harry Potter aprendendo a vencer o medo e se apaixonando por Hermione:</i>", s["small"])
    story.append(Spacer(1, 4))
    for c in CAPITULOS:
        p(story, f"<b>Capítulo {c['num']:02d}:</b> {c['titulo']} &nbsp;<i>({c['tag']})</i>", s["toc"])
    story.append(PageBreak())

    # ═══════════ OS 20 CAPÍTULOS ═══════════
    for c in CAPITULOS:
        capitulo(
            story=story,
            num=c["num"],
            tag=c["tag"],
            titulo=c["titulo"],
            img=c["img"],
            cena_paragrafos=c["cena"],
            psico_titulo=c["psico_tit"],
            psico_texto=c["psico_txt"],
            toque_romance=c["toque_romance"],
            s=s,
        )

    # ═══════════ CONTRACAPA / MENSAGEM FINAL ═══════════
    story.append(Spacer(1, 5.0 * cm))
    p(story, "E VIVERAM FELIZES PARA SEMPRE", s["cover_brand"])
    p(story, "O Fim da Fobia, o Começo do Amor", s["cover_title"])
    story.append(HRFlowable(width="34%", thickness=2, color=NAVY, spaceBefore=6, spaceAfter=14))
    p(story, "Que você leve no coração a certeza de que todo monstrinho encolhe<br/>"
             "quando a gente olha para ele com coragem, paciência e afeto.", s["cover_sub"])
    story.append(Spacer(1, 1.0 * cm))
    story.append(ilustra("dragao", 7.0 * cm))
    story.append(Spacer(1, 1.0 * cm))
    p(story, "Dra. Priscila Palomo  ·  CRP 98007<br/>www.priscilapalomo.com  ·  WhatsApp: (11) 95069-0537", s["cover_brand"])

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"OK: {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
