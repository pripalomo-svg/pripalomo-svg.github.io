#!/usr/bin/env python3
"""Gera o livro ilustrado:
'Harry Potter e a Magia da Coragem — A Batalha Secreta Contra o Devorador de Coragem
e o Amor que Ele Achava Impossível'

Uma historinha lúdica e envolvente, contada para crianças de 5 anos (e seus pais!),
sobre um bruxinho de óculos redondos e cicatriz de raio na testa que enfrenta o pior
inimigo que existe: o Devorador de Coragem, uma sombra sussurrante que vive de cada
medo evitado. A cada capítulo, Harry enfrenta uma fobia diferente, aprendendo com
Hermione um segredo real da Psicologia — e, ao mesmo tempo, escondendo um segredo do
coração: ele ama Hermione, mas tem certeza de que jamais seria correspondido.

Cada capítulo começa com um gancho para prender o leitor e termina com uma pista do
que vem a seguir. Sem folhas de exercício — só a história, do começo ao fim feliz.
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
GOLD = HexColor("#C8940A")
ORANGE = HexColor("#B8790A")
INK = HexColor("#111111")
MUTED = HexColor("#555555")
LINE = HexColor("#E4D9BE")
PALE = HexColor("#FBF7EE")
WARM_BOX = HexColor("#F6EFDD")
HEART_PINK = HexColor("#B23A63")
SHADOW = HexColor("#33302A")

ROOT_DIR = Path(__file__).resolve().parents[1]
IMG = ROOT_DIR / "assets" / "img" / "hp"
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
        fontSize=10.5, textColor=ORANGE, alignment=TA_LEFT, spaceBefore=0, spaceAfter=2,
    )
    s["h1"] = ParagraphStyle(
        "h1", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=17, textColor=NAVY, spaceBefore=0, spaceAfter=6, leading=21,
    )
    s["h2"] = ParagraphStyle(
        "h2", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=12, textColor=INK, spaceBefore=6, spaceAfter=3, leading=15,
    )
    s["prosa"] = ParagraphStyle(
        "prosa", parent=base["Normal"], fontName="Helvetica",
        fontSize=10, textColor=INK, alignment=TA_JUSTIFY, leading=15.3,
        spaceAfter=6.5, firstLineIndent=14,
    )
    s["prosa_first"] = ParagraphStyle(
        "prosa_first", parent=s["prosa"], firstLineIndent=0,
    )
    s["gancho_abertura"] = ParagraphStyle(
        "gancho_abertura", parent=base["Normal"], fontName="Helvetica-BoldOblique",
        fontSize=10.6, textColor=NAVY, alignment=TA_LEFT, leading=15.6,
        spaceAfter=8, firstLineIndent=0,
    )
    s["gancho_final"] = ParagraphStyle(
        "gancho_final", parent=base["Normal"], fontName="Helvetica-BoldOblique",
        fontSize=10, textColor=SHADOW, alignment=TA_LEFT, leading=14.5,
        spaceBefore=4, spaceAfter=2, leftIndent=10, rightIndent=10,
    )
    s["vilao_fala"] = ParagraphStyle(
        "vilao_fala", parent=base["Normal"], fontName="Helvetica-Oblique",
        fontSize=10, textColor=SHADOW, alignment=TA_CENTER, leading=14.5,
        spaceBefore=6, spaceAfter=6, leftIndent=16, rightIndent=16,
    )
    s["quote"] = ParagraphStyle(
        "quote", parent=base["Normal"], fontName="Helvetica-Oblique",
        fontSize=10, textColor=HEART_PINK, alignment=TA_CENTER, leading=14.5,
        spaceBefore=6, spaceAfter=6, leftIndent=12, rightIndent=12,
    )
    s["box_title"] = ParagraphStyle(
        "box_title", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=10.5, textColor=NAVY, alignment=TA_LEFT, leading=13,
    )
    s["box_body"] = ParagraphStyle(
        "box_body", parent=base["Normal"], fontName="Helvetica",
        fontSize=9.2, textColor=INK, alignment=TA_JUSTIFY, leading=13.7,
    )
    s["small"] = ParagraphStyle(
        "small", parent=base["Normal"], fontName="Helvetica",
        fontSize=8.5, textColor=MUTED, leading=12, spaceAfter=4,
    )
    s["toc"] = ParagraphStyle(
        "toc", parent=base["Normal"], fontName="Helvetica",
        fontSize=9, textColor=INK, leading=14, spaceAfter=3,
    )
    return s


def hr():
    return HRFlowable(width="100%", thickness=1, color=LINE, spaceBefore=2, spaceAfter=8)


def ilustra(nome, largura=11.5 * cm):
    for ext in (".jpg", ".png"):
        img_path = IMG / (nome + ext)
        if img_path.exists():
            img = Image(str(img_path))
            ratio = img.imageHeight / float(img.imageWidth)
            img.drawWidth = largura
            img.drawHeight = largura * ratio
            img.hAlign = "CENTER"
            return img
    return Spacer(1, 1)


def caixa_psico(titulo, texto, s):
    header = [Paragraph(f"✨ <b>O Segredo Mágico da Mente:</b> {titulo}", s["box_title"])]
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


def capitulo(story, num, tag, titulo, gancho_abertura, img, cena_paragrafos,
             fala_vilao, toque_romance, gancho_final, psico_titulo, psico_texto, s):
    p(story, f"CAPÍTULO {num:02d} · {tag.upper()}", s["part"])
    p(story, titulo, s["h1"])
    story.append(hr())
    if gancho_abertura:
        p(story, gancho_abertura, s["gancho_abertura"])
    if img:
        story.append(ilustra(img))
        story.append(Spacer(1, 6))
    for i, texto in enumerate(cena_paragrafos):
        p(story, texto, s["prosa_first"] if i == 0 else s["prosa"])
    if fala_vilao:
        p(story, f"🌑 <i>{fala_vilao}</i>", s["vilao_fala"])
    if toque_romance:
        p(story, f"💛 <i>{toque_romance}</i>", s["quote"])
    story.append(Spacer(1, 3))
    story.append(caixa_psico(psico_titulo, psico_texto, s))
    if gancho_final:
        story.append(Spacer(1, 2))
        p(story, f"➜ {gancho_final}", s["gancho_final"])
    story.append(PageBreak())


# ═════════════════════════════════════════════════════════════════════════
#  OS CAPÍTULOS
# ═════════════════════════════════════════════════════════════════════════

CAPITULOS = [

    # 01 ─────────────────────────────────────────────
    dict(
        num=1, tag="O Armário Debaixo da Escada",
        titulo="O Menino que Tinha um Inimigo Secreto",
        gancho_abertura="Antes de qualquer outra coisa, você precisa saber de um segredo: "
                        "o pior inimigo de Harry Potter não usava capa preta, nem tinha nome "
                        "temido em nenhum livro de magia. Ele era pequenininho, sussurrante, "
                        "e morava bem dentro do peito de Harry.",
        img="hp_closet_dark",
        cena=[
            "Na Rua dos Alfeneiros, número quatro, havia um armário debaixo da escada tão "
            "pequeno que mal cabia uma cama, um baú e um garotinho de óculos redondos, cabelos "
            "pretos completamente desarrumados e uma marquinha de raio na testa. Aquele "
            "garotinho se chamava Harry Potter, e todos que olhavam para ele achavam a mesma "
            "coisa: 'Nossa, que cicatriz misteriosa! Ele deve ser super corajoso!'.",
            "Ninguém sabia da verdade. Assim que as luzes se apagavam e a casa ficava em "
            "silêncio, alguma coisa se mexia nos cantos escuros do armário. Não era rato. "
            "Não era aranha. Era uma sombra fina como fumaça, com dois olhinhos cor de brasa "
            "apagando, que se enroscava nos pés da cama e sussurrava tão baixinho que só Harry "
            "conseguia ouvir:",
            "— Psss... Harry... tem alguma coisa se mexendo aí no canto... e se for um monstro "
            "de verdade? E se ele morder os seus pezinhos? Melhor você nem olhar. Melhor ficar "
            "bem quietinho, bem encolhidinho, para sempre...",
            "O coraçãozinho de Harry disparava feito um tambor de festa. Ele cobria a cabeça "
            "com três cobertores, prendia a respiração e ficava horas acordado, com muito medo "
            "de espiar para fora. Mas sabe de uma coisa engraçada? Quando ele finalmente "
            "ganhava coragem de acender o abajur, tremendo dos pés à cabeça... não havia "
            "monstro nenhum. Só a sombra da orelha do seu ursinho de pelúcia, balançando "
            "devagarinho com o vento da janela.",
            "A sombra sussurrante ficava uma pilha de raiva quando isso acontecia. Encolhia "
            "um tiquinho, resmungava e se escondia de novo no canto mais escuro, esperando "
            "a próxima chance de assustar o menino.",
            "Harry não sabia o nome daquela sombra. Só sabia de uma coisa: ela vivia "
            "grudada nele havia anos, e sempre encontrava um jeito novo de fazer seu coração "
            "bater descompassado — nas alturas, na água funda, nas agulhas do médico, nos "
            "latidos de cachorro, em qualquer lugar cheio de gente olhando para ele. Ele "
            "achava, no fundo do coração, que aquele era o seu destino: ser sempre o menino "
            "medroso, mesmo tendo uma cicatriz de herói.",
        ],
        fala_vilao="Fica quietinho, Harry. Comigo por perto, você nunca vai precisar arriscar nada... e nunca vai se machucar. Nem o coração.",
        toque_romance=None,
        gancho_final="Mas naquela mesma noite, bem quando Harry finalmente pegou no sono, "
                    "uma coruja gigantesca bateu com força na janela do armário, trazendo uma carta "
                    "que mudaria tudo — inclusive o destino da sombra sussurrante.",
        psico_titulo="O Alarme Falso da Amígdala (David H. Barlow)",
        psico_texto="Todo mundo tem, escondidinho dentro do cérebro, um alarme de perigo chamado "
                    "amígdala. Ele existe para nos proteger de verdade! Só que às vezes ele fica "
                    "sensível demais e dispara mesmo quando não há perigo nenhum — só a sombra de "
                    "um ursinho de pelúcia. Isso se chama alarme falso, e é exatamente o que faz o "
                    "nosso coração bater rápido à toa. A boa notícia é que, com carinho e prática, "
                    "esse alarme aprende a ficar mais calminho.",
    ),

    # 02 ─────────────────────────────────────────────
    dict(
        num=2, tag="O Expresso de Hogwarts",
        titulo="A Menina que Fez o Coração de Harry Dar um Solavanco",
        gancho_abertura="Harry nunca tinha visto um trem escarlate que soltava fumacinha "
                        "dourada, nem imaginava que, naquela manhã, ele fosse conhecer a pessoa "
                        "mais importante de toda a sua vida numa cabine pequena e apertada de "
                        "trem.",
        img=None,
        cena=[
            "A carta da coruja explicava tudo: Harry era um bruxinho de verdade! E aquele "
            "trem enorme, saindo bem da Plataforma Nove e Meia, levava crianças bruxas para "
            "uma escola chamada Hogwarts, escondida no alto de uma colina cheia de torres.",
            "Harry entrou timidamente numa cabine e encontrou uma menininha sentada, lendo um "
            "livro tão grosso quanto um tijolo, com cabelos cacheados e volumosos que pareciam "
            "uma nuvem de algodão-doce escura. Ela ergueu os olhos castanhos, sorriu um sorriso "
            "enorme e disse, sem nem respirar direito de tão animada:",
            "— Oi! Eu sou Hermione Granger! Já li sete livros sobre Hogwarts, sabia que o "
            "castelo tem cento e quarenta e dois lances de escada?! Nossa, que cicatriz "
            "interessante você tem na testa!",
            "Harry sentiu as bochechas esquentarem feito duas fogueirinhas. Ele nunca tinha "
            "visto ninguém falar tão rápido, tão animado e tão inteligente ao mesmo tempo. E "
            "quando os olhos dos dois se cruzaram por um segundinho a mais do que o necessário, "
            "algo estranho aconteceu dentro do peito de Harry: um friozinho gostoso, "
            "completamente diferente de qualquer medo que ele já tinha sentido.",
            "'Ela nunca vai reparar num menino que treme igual gelatina', pensou Harry logo "
            "em seguida, baixando os olhos para os próprios sapatos. 'Ela é inteligente "
            "demais, corajosa demais... e eu sou só o garoto do armário debaixo da escada.'",
            "A sombra sussurrante, enrolada dentro do bolso da capa de Harry como se fosse um "
            "lenço qualquer, deu uma risadinha seca e fria. Ela tinha acabado de descobrir um "
            "sabor novo de medo para se alimentar — e esse sabor era ainda mais gostoso do que "
            "todos os outros.",
        ],
        fala_vilao="Ora, ora... Coragem para enfrentar dragões é uma coisa. Coragem para dizer 'eu gosto de você' é outra bem diferente. Essa aqui, garoto, eu não vou deixar você usar nunca.",
        toque_romance="Harry guardou aquele momento — o sorriso de Hermione, os cabelos em nuvem, o cheiro de livro novo — como quem guarda um doce escondido para comer bem devagarinho, sozinho, mais tarde.",
        gancho_final="Nenhum dos dois sabia que aquela sombra sussurrante tinha um nome verdadeiro, "
                    "muito antigo e muito temido pelos bruxos mais sábios — e que Harry estava "
                    "prestes a descobri-lo, na primeira aula de voo de Hogwarts.",
        psico_titulo="A Timidez do Primeiro Encontro (Ansiedade Social)",
        psico_texto="Quando gostamos de alguém, é super comum o coração bater mais rápido, as "
                    "bochechas esquentarem e a vontade de fugir aparecer — mesmo sem perigo "
                    "nenhum! Isso acontece porque conhecer pessoas novas e mostrar quem "
                    "realmente somos é um tipo de coragem tão importante quanto enfrentar um "
                    "medo de altura ou de aranha. A vergonha do início quase sempre passa "
                    "quando a gente se permite continuar conversando, um pouquinho de cada vez.",
    ),

    # 03 ─────────────────────────────────────────────
    dict(
        num=3, tag="O Campo de Voo",
        titulo="A Vassoura que Não Queria Sair do Chão",
        gancho_abertura="Todo mundo em Hogwarts vivia dizendo que voar de vassoura era a "
                        "coisa mais divertida do mundo mágico. Ninguém tinha avisado Harry que, "
                        "para ele, seria também a coisa mais assustadora.",
        img="hp_broom_sky",
        cena=[
            "No gramado enorme atrás do castelo, a professora Madame Hooch alinhou as "
            "vassouras no chão e gritou: 'Mão direita sobre o cabo e digam: SUBA!'. Todas as "
            "vassouras saltaram obedientes para as mãos dos alunos, que subiram aos céus rindo "
            "e fazendo piruetas.",
            "A vassoura de Harry também saltou. Só que, assim que ele subiu um palmo do chão, "
            "a sombra sussurrante — que naquele dia tinha crescido do tamanho de um gato para o "
            "tamanho de um cachorro grande — enrolou-se em volta do seu pescoço e apertou "
            "gelado:",
            "— Olha lá embaixo, Harry! Tão longe... Se você subir mais um centímetro sequer, "
            "vai cair, vai quebrar cada ossinho do corpo e virar uma piada para a escola "
            "inteira. Melhor descer agora. Melhor nunca mais tentar.",
            "Harry congelou a um metro do chão, as mãos brancas de tanto apertar o cabo de "
            "madeira, o coração tentando fugir pela boca. Os outros alunos já estavam lá em "
            "cima, pequenininhos contra as nuvens.",
            "Foi então que Hermione desceu de sua própria vassoura, pousou ao lado dele na "
            "grama e disse, com a voz mais gentil que ele já tinha ouvido:",
            "— Harry, ninguém pede para você voar até as nuvens hoje. Que tal só a altura de "
            "uma formiguinha, para começar? Um dedinho hoje, dois amanhã. Eu fico bem "
            "aqui do seu lado o tempo que for preciso.",
            "Harry respirou fundo, subiu apenas a altura de uma maçã... e não caiu. A sombra "
            "sussurrante encolheu, furiosa, de volta ao tamanho de um gato.",
        ],
        fala_vilao="Isso não vale, garotinha metida! Eu quase tinha ele!",
        toque_romance="Quando Harry pousou de volta na grama, seguro e inteiro, Hermione bateu palminhas tão animada que os cabelos em nuvem balançaram, e Harry pensou consigo mesmo que aquele era, sem sombra de dúvida, o som mais bonito que já tinha escutado em toda a sua vida.",
        gancho_final="Só que, naquela mesma tarde, um velho amigo do guarda-caça Hagrid contaria a "
                    "Harry uma lenda arrepiante sobre uma criatura que se alimenta exatamente do "
                    "que ele mais temia perder — e o nome dela era mais antigo do que qualquer "
                    "feitiço que Harry já tinha aprendido.",
        psico_titulo="A Escadinha Mágica dos Medos (Dessensibilização Sistemática — Joseph Wolpe)",
        psico_texto="Ninguém precisa enfrentar o medo inteiro de uma vez só! O cientista Joseph "
                    "Wolpe descobriu que, se a gente divide um medo grande em pedacinhos "
                    "pequenininhos — como subir só um dedinho, depois dois — o corpo aprende, "
                    "devagar e com segurança, que aquilo não é perigoso. Isso se chama exposição "
                    "gradual: um degrau de cada vez, sem pressa nenhuma.",
    ),

    # 04 ─────────────────────────────────────────────
    dict(
        num=4, tag="A Floresta Proibida",
        titulo="O Nome Secreto da Sombra",
        gancho_abertura="Havia uma regra em Hogwarts que todo aluno conhecia de cor: nunca, "
                        "jamais, em hipótese alguma, entrar sozinho na Floresta Proibida à "
                        "noite. Harry estava prestes a descobrir por quê — e não era por causa "
                        "das criaturas da floresta.",
        img="hp_forest_spider",
        cena=[
            "Hagrid, o guarda-caça gigante e gentil, levou Harry e Hermione até a beira da "
            "floresta para coletar cogumelos brilhantes. No caminho, uma aranhazinha do "
            "tamanho de um grão de feijão desceu por um fio de teia bem na frente do rosto de "
            "Harry.",
            "Ele deu um pulo tão grande para trás que quase caiu sentado! A sombra sussurrante, "
            "aproveitando o susto, engordou mais um pouquinho e sibilou no ouvido dele:",
            "— Ela tem oito olhos e presas de monstro! Corre, Harry, corre antes que ela te "
            "devore inteirinho!",
            "— Harry — chamou Hagrid, com a voz grave mas gentil, agachando-se ao lado dele. — "
            "Eu vou te contar uma coisa que poucos bruxos sabem. Essa vozinha que grita dentro "
            "de você tem um nome. Os antigos a chamavam de <b>Devorador de Coragem</b>. Ele não "
            "come pessoas, nem come bolo, nem come nada que você possa ver. Ele só come uma "
            "coisa: toda vez que a gente foge de alguma coisa pequena, ele fica um "
            "pouquinho maior.",
            "Hermione arregalou os olhos, largou o livro na hora e sentou-se na grama ao lado "
            "dos dois, ansiosa para escutar cada palavra.",
            "— E como a gente faz ele encolher de novo? — perguntou Harry, com a voz "
            "tremendo só um tiquinho.",
            "— Olhando bem para aquilo que ele diz que é perigoso — respondeu Hagrid, "
            "pegando a aranhazinha com cuidado na palma enorme da mão — e descobrindo, com os "
            "próprios olhos, que não tinha perigo nenhum ali.",
            "Harry esticou o dedo, tremendo, e deixou a aranhazinha caminhar por cima. Ela era "
            "leve como uma pena e fazia cócegas. Nada de presas de monstro. Nada de devorar "
            "ninguém. A sombra sussurrante, furiosa, encolheu um bom pedaço, resmungando "
            "palavras feias que ninguém mais conseguia entender.",
        ],
        fala_vilao="Isso não conta! Um dia, Harry Potter, você vai encontrar um medo grande demais para olhar de frente — e nesse dia, eu vou comer tudo o que sobrar de você.",
        toque_romance="Hermione sorriu tão orgulhosa de Harry que ele sentiu vontade de segurar a mãozinha dela ali mesmo, na grama da floresta. Quase esticou os dedos. Quase. No último segundo, lembrou que meninas espertas como ela nunca se interessariam por um menino que tinha medo até de aranha, e enfiou as mãos frias nos bolsos.",
        gancho_final="Naquela noite, deitado na cama do dormitório, Harry repetiu baixinho para si "
                    "mesmo: 'Devorador de Coragem'. Ele não sabia ainda que aquele nome logo "
                    "seria sussurrado por toda a escola — porque o Devorador estava prestes a "
                    "atacar em cheio, bem no meio do Lago Negro.",
        psico_titulo="O Ciclo da Fuga (Reforço Negativo — O. H. Mowrer)",
        psico_texto="Toda vez que fugimos de algo que nos assusta, sentimos um alívio imediato — "
                    "e é exatamente esse alívio gostoso que ensina o cérebro, de um jeito "
                    "enganoso, que fugir 'funcionou'. Esse ciclo se chama reforço negativo, e é "
                    "ele que faz um medo pequeno crescer e crescer com o tempo. A boa notícia: "
                    "quando a gente para de fugir e olha de frente, o ciclo se quebra — e o medo "
                    "encolhe, exatamente como o Devorador de Hagrid.",
    ),

    # 05 ─────────────────────────────────────────────
    dict(
        num=5, tag="O Lago Negro",
        titulo="A Água que Fingia Estar Congelando",
        gancho_abertura="Ninguém avisou Harry que o Lago Negro de Hogwarts, quieto e "
                        "espelhado como vidro escuro, escondia debaixo da própria superfície "
                        "um truque tão poderoso quanto qualquer feitiço — e que o Devorador de "
                        "Coragem sabia exatamente como usá-lo contra ele.",
        img="hp_lake_cold",
        cena=[
            "Era um sábado quente e as três amizades — Harry, Hermione e o simpático Rony "
            "Weasley — decidiram fazer um piquenique na margem do lago. Enquanto os outros "
            "corriam animados para dentro d'água, Harry mergulhou só a pontinha do dedão do "
            "pé... e deu um pulo tão grande para trás que espirrou água em todo mundo.",
            "— BRRRR! ESTÁ CONGELANTE! — gritou ele. — Vou virar um picolé de bruxo!",
            "A sombra do Devorador, escondida dentro da manga da sua capa, sibilou animada:",
            "— Sente como está gelado? Vai ficar cada vez pior, Harry. Seu coração vai parar "
            "de bater de tanto frio. Fica aqui na areia, seguro e quentinho, olhando os "
            "outros se divertirem sem você.",
            "Hermione, já com os pés na água até os joelhos, estendeu a mão para ele.",
            "— Entra aqui comigo e segura minha mão. A gente conta até cem juntos sem sair. "
            "Prometo que vai acontecer uma mágica sem precisar de nenhuma varinha.",
            "Harry entrou tremendo feito uma gelatina. No primeiro minuto, bateu o queixo. "
            "No segundo, achou suportável. No quarto minuto, ele parou de repente e olhou "
            "para Hermione, maravilhado:",
            "— Ei... a água ficou quentinha!",
            "— A água continua igualzinha, bobinho — riu Hermione, apertando de leve a mão "
            "dele. — Foi o seu corpo que se acostumou. Essa é a mágica de verdade.",
            "A sombra do Devorador encolheu tanto que sumiu dentro da manga da capa, "
            "resmungando baixinho. Mas Harry, distraído demais olhando para os olhos "
            "castanhos de Hermione brilhando sob o sol, nem percebeu.",
        ],
        fala_vilao="Aproveita, garoto. Cedo ou tarde, você vai ter que soltar essa mão — e eu estarei bem ali, esperando você duvidar de novo.",
        toque_romance="Naquele instante, com a água quentinha em volta e a mão de Hermione ainda na sua, Harry sentiu uma vontade absurda de dizer alguma coisa importante. Mas as palavras enrolaram na garganta feito um nó, e tudo o que saiu foi um sorriso tímido e um 'obrigado'.",
        gancho_final="O que Harry não sabia é que, do outro lado do lago, um garoto mais velho "
                    "chamado Cedrico Diggory observava toda a cena com um sorriso curioso — e "
                    "que esse detalhe pequeno iria plantar, no coração de Harry, a maior dúvida "
                    "de toda a sua jornada.",
        psico_titulo="A Água Que Não Muda: A Habituação",
        psico_texto="Nosso corpo é surpreendente: quando sentimos frio ou medo, a primeira reação "
                    "é sempre mais forte. Mas se ficarmos ali, sem fugir, o corpo se acostuma "
                    "sozinho em poucos minutos! Isso se chama habituação. A água do lago nunca "
                    "esquenta de verdade — é a gente que aprende, aos poucos, que consegue "
                    "aguentar mais do que imaginava.",
    ),

    # 06 ─────────────────────────────────────────────
    dict(
        num=6, tag="A Ala Hospitalar",
        titulo="A Agulha Mais Assustadora do Mundo Mágico",
        gancho_abertura="Existem monstros de escamas, monstros de sombra e monstros de "
                        "presas afiadas. Mas para Harry Potter, o monstro mais aterrorizante de "
                        "Hogwarts tinha apenas dois centímetros de comprimento, brilhava sob a "
                        "luz e se chamava agulha.",
        img="hp_hospital_needle",
        cena=[
            "Madame Pomfrey, a enfermeira mais bondosa do castelo, avisou que todos os alunos "
            "precisavam tomar uma gotinha de Poção Protetora, aplicada com uma agulhinha "
            "minúscula. Assim que Harry viu aquele pontinho de metal brilhando na luz da "
            "enfermaria, seu rosto ficou branco feito giz, as pernas amoleceram e o mundo "
            "começou a girar.",
            "— Vou desmaiar — sussurrou ele, escorregando na cadeira.",
            "O Devorador de Coragem, sentindo o cheiro do pânico, cresceu instantaneamente do "
            "tamanho de um gato para o tamanho de um lobo, enroscando-se nos tornozelos de "
            "Harry:",
            "— É isso mesmo, Harry. Desmaia. Cai no chão na frente de todo mundo. Isso vai "
            "provar, de uma vez por todas, que você é fraco demais para ser corajoso.",
            "Hermione, que tinha lido justamente um capítulo sobre isso na noite anterior "
            "(é claro que tinha), correu e segurou os ombros dele com firmeza.",
            "— Harry, escuta rápido: aperte os músculos das pernas, da barriga e dos braços "
            "com toda a força, como se você fosse feito de pedra! Isso empurra o sangue de "
            "volta para a sua cabeça!",
            "Harry contraiu cada músculo do corpo por quinze segundos inteiros. As bochechas "
            "voltaram a ficar rosadas, a tontura sumiu — e quando a agulha finalmente tocou "
            "seu braço, pareceu só uma cutucadinha de formiga.",
            "O Devorador, frustrado, encolheu de volta ao tamanho de um gato arisco, "
            "escondendo-se atrás da cortina da enfermaria.",
        ],
        fala_vilao="Guarde este truque bem guardado, Harry. Ele só funciona contra mim quando você tem coragem de usá-lo NA HORA do susto — e eu sempre apareço bem quando você menos espera.",
        toque_romance="Hermione ficou segurando a mão de Harry mesmo depois que a picadinha já tinha acabado havia muito tempo. Nenhum dos dois pareceu notar. Ou talvez os dois tivessem notado exatamente demais, e por isso nenhum soltasse primeiro.",
        gancho_final="Só que aquela mesma noite, uma tempestade das grandes se formou sobre o "
                    "castelo — e o Devorador de Coragem, ainda dolorido pela derrota na "
                    "enfermaria, tinha um plano de vingança guardado exatamente para os "
                    "trovões.",
        psico_titulo="Técnica de Tensão Aplicada (Lars-Göran Öst)",
        psico_texto="O medo de agulha e sangue é diferente de todos os outros medos: em vez de só "
                    "acelerar o coração, ele pode fazer a pressão despencar de repente, causando "
                    "tontura ou desmaio. Por isso, relaxar é o conselho errado aqui! O cientista "
                    "Lars-Göran Öst descobriu que apertar os músculos com força por alguns "
                    "segundos empurra a pressão de volta para cima, e a tontura desaparece.",
    ),

    # 07 ─────────────────────────────────────────────
    dict(
        num=7, tag="A Noite de Trovões",
        titulo="O Freio Mágico Escondido Dentro do Peito",
        gancho_abertura="CABUM! Um trovão tão forte que fez os vidros das janelas do castelo "
                        "tremerem partiu a noite ao meio — e, junto com ele, veio a coisa que o "
                        "Devorador de Coragem mais adorava: o pânico puro.",
        img="hp_storm_window",
        cena=[
            "Harry se sentou de repente na cama, o coração disparado feito um cavalo "
            "galopando sem rédeas. Cada relâmpago iluminava sombras estranhas nas paredes de "
            "pedra do dormitório, e cada trovão parecia mais perto do que o anterior.",
            "O Devorador de Coragem, que adorava tempestades mais do que qualquer outra "
            "coisa no mundo, esticou-se pelo teto do dormitório inteiro, enorme como uma "
            "nuvem escura, sussurrando de todos os cantos ao mesmo tempo:",
            "— O castelo vai desabar! Os trovões vão te alcançar! Não há lugar seguro esta "
            "noite, Harry Potter!",
            "Foi quando uma batidinha suave soou na porta. Era Hermione, envolta num "
            "cobertor felpudo, segurando uma velinha perfumada de baunilha.",
            "— Vim porque imaginei que você estivesse acordado — disse ela, sentando-se ao "
            "lado dele no parapeito da janela. — Sabia que nosso corpo tem um freio mágico "
            "escondido? Ele se chama respiração.",
            "— Puxa o ar bem devagarinho pelo nariz, como se estivesse cheirando uma "
            "florzinha... um, dois, três, quatro. Agora solta pela boca ainda mais devagar, "
            "como quem sopra a velinha de aniversário sem querer apagar de uma vez... um, "
            "dois, três, quatro, cinco, seis.",
            "Harry repetiu dez vezes, seguindo o ritmo da voz calma de Hermione. Aos poucos, "
            "o cavalo galopante dentro do peito foi trotando mais devagar, até virar um "
            "passinho tranquilo. O Devorador, sem combustível para se alimentar, encolheu-se "
            "de volta para um cantinho escuro do teto, resmungando.",
        ],
        fala_vilao="Vocês dois vão continuar se encontrando escondidos toda noite de tempestade? Interessante... muito interessante mesmo.",
        toque_romance="Sentados lado a lado, enrolados no mesmo cobertor felpudo, ouvindo a chuva bater na vidraça, Harry pensou que aquele momento — pequeno, quentinho, silencioso — era mais mágico do que qualquer feitiço que já tinha aprendido em Hogwarts.",
        gancho_final="Na manhã seguinte, um cachorro imenso de três cabeças escapou pelo terceiro "
                    "andar do castelo — e todos os alunos, menos um, saíram correndo apavorados "
                    "na direção contrária.",
        psico_titulo="Respiração Lenta e o Freio do Corpo (Nervo Vago)",
        psico_texto="Quando respiramos rápido de susto, o corpo entra no modo 'perigo!'. Mas ao "
                    "soltar o ar bem devagarinho pela boca, ativamos um freio natural chamado "
                    "nervo vago, que avisa para o coração desacelerar. É como se o próprio corpo "
                    "tivesse um botão de calma — e a chave para apertá-lo é simplesmente respirar "
                    "devagar.",
    ),

    # 08 ─────────────────────────────────────────────
    dict(
        num=8, tag="O Terceiro Andar",
        titulo="O Cão de Três Cabeças que Só Queria Carinho",
        gancho_abertura="Havia um segredo trancado atrás de uma porta no terceiro andar de "
                        "Hogwarts, guardado por uma criatura tão grande que sua sombra sozinha "
                        "já bastava para fazer alunos desmaiarem de susto — mas Harry estava "
                        "prestes a descobrir que nem todo monstro é o que parece.",
        img="hp_three_headed_dog",
        cena=[
            "— UM CÃO DE TRÊS CABEÇAS?! — gritou Rony, correndo em disparada pelo corredor. "
            "— Fofo, dizem que ele se chama! Muito engraçado esse nome para uma coisa que "
            "poderia engolir a gente inteirinho!",
            "Harry, no entanto, ficou parado, olhando pela fresta da porta entreaberta. O "
            "cachorrão realmente era enorme — do tamanho de um elefante pequeno — mas suas "
            "seis orelhas estavam caídas, tristonhas, e as três bocas soltavam suspiros longos "
            "e solitários.",
            "O Devorador de Coragem, ansioso para engordar mais um pouco, sussurrou:",
            "— Ele vai te morder com as três bocas ao mesmo tempo! Corre, Harry, antes que "
            "seja tarde demais!",
            "Mas Hermione, sempre com um livro na cabeça cheio de respostas, sussurrou de "
            "volta:",
            "— Harry, olha bem: ele não está rosnando. Está com fome de atenção, não de "
            "gente. Animais grandes assustam porque a gente nunca chegou perto o suficiente "
            "para conhecer o jeitinho deles.",
            "No primeiro dia, olharam de longe. No segundo, chegaram três metros mais perto. "
            "No terceiro dia, Harry esticou a mão trêmula e ofereceu um biscoitinho de "
            "chocolate. Fofo abanou o rabo enorme com tanta força que derrubou uma armadura "
            "inteira no corredor, e lambeu a mão de Harry com as três línguas ao mesmo tempo, "
            "deixando-o completamente encharcado de baba — e de alegria.",
        ],
        fala_vilao="Argh! Cachorros felizes não me alimentam em nada! Isso é trapaça!",
        toque_romance="Hermione riu tanto da baba nas bochechas de Harry que quase caiu sentada no chão do corredor — e Harry, mesmo encharcado, achou que valeria a pena passar pelo mesmo susto mil vezes só para ouvir aquela risada de novo.",
        gancho_final="Só que, dias depois, uma aula de Adivinhação traria uma previsão sombria "
                    "envolvendo o próprio Harry — e, pela primeira vez, o Devorador não precisaria "
                    "inventar mentira nenhuma para deixá-lo apavorado.",
        psico_titulo="Aprender Vendo o Outro (Modelação Vicária — Albert Bandura)",
        psico_texto="O cientista Albert Bandura descobriu algo lindo: quando vemos uma pessoa "
                    "querida se aproximar com calma de algo que nos assusta, nosso cérebro aprende "
                    "por imitação que aquilo é seguro. Ter alguém corajoso ao nosso lado, mostrando "
                    "o caminho com carinho (e sem forçar nada), é uma das formas mais gentis de "
                    "vencer o medo.",
    ),

    # 09 ─────────────────────────────────────────────
    dict(
        num=9, tag="A Torre de Adivinhação",
        titulo="A Bola de Cristal que Mentia Demais",
        gancho_abertura="Na torre mais alta e enevoada do castelo, a professora Trelawney "
                        "prometeu que a bola de cristal revelaria o futuro de cada aluno. O que "
                        "ninguém esperava era que o futuro previsto para Harry fosse exatamente "
                        "o roteiro favorito do Devorador de Coragem.",
        img=None,
        cena=[
            "— Eu vejo... — murmurou a professora Trelawney, com os olhos enormes atrás dos "
            "óculos grossos, olhando fixamente para a névoa dentro da bola de cristal de "
            "Harry. — Vejo um coração partido! Vejo alguém escolhendo outro caminho, longe "
            "de você, meu caro!",
            "A sala inteira suspirou dramaticamente. Harry sentiu o estômago revirar. E, "
            "para piorar tudo, no fundo da sala, ele viu Cedrico Diggory se inclinar para "
            "perto de Hermione, rindo de alguma piada, os dois cabeças coladas sobre o "
            "mesmo pergaminho.",
            "O Devorador de Coragem, que tinha esperado semanas por uma oportunidade daquele "
            "tamanho, cresceu instantaneamente até preencher a sala inteira de sombra:",
            "— Viu só? Eu avisei. Ela vai escolher alguém mais corajoso, mais confiante, "
            "alguém que não trema feito gelatina toda vez que um trovão estala. Você nunca "
            "vai ser bom o suficiente, Harry Potter. Nem para dragões, nem para amores.",
            "Naquela noite, Harry escreveu e riscou dez vezes uma cartinha que nunca teve "
            "coragem de entregar. As palavras 'eu gosto de você' pareciam maiores e mais "
            "assustadoras do que qualquer aranha, qualquer altura, qualquer trovão que ele já "
            "tinha enfrentado.",
            "'Talvez seja mais fácil vencer um dragão de verdade do que dizer isso em voz "
            "alta', pensou ele, amassando o pergaminho e jogando no fundo do baú.",
        ],
        fala_vilao="Viu como eu sou generoso? Nem precisei mentir dessa vez. Alguns medos, Harry, são verdadeiros mesmo.",
        toque_romance="O que Harry não sabia — e é bem provável que você, leitor esperto, já esteja desconfiando — é que Hermione só estava rindo daquela piada de Cedrico porque, minutos antes, ela tinha ficado olhando para a porta da sala esperando Harry chegar, e continuava roubando olhadinhas para o lugar vazio ao seu lado.",
        gancho_final="Na manhã seguinte, Harry precisaria enfrentar o Salão Principal lotado para "
                    "uma apresentação em público — e, dessa vez, o Devorador prometeu que faria "
                    "questão de aparecer bem na frente de todo mundo.",
        psico_titulo="Pensamentos Não São Fatos (Aaron T. Beck)",
        psico_texto="Nossa mente adora inventar histórias de catástrofe antes mesmo delas "
                    "acontecerem — isso se chama pensamento automático. O cientista Aaron Beck "
                    "descobriu que, quando aprendemos a perguntar 'isso é realmente verdade, ou é "
                    "só o medo falando?', conseguimos separar os fatos reais das histórias "
                    "assustadoras que a ansiedade gosta de contar.",
    ),

    # 10 ─────────────────────────────────────────────
    dict(
        num=10, tag="O Salão Principal",
        titulo="A Voz que Sumiu na Frente de Todo Mundo",
        gancho_abertura="Existem mil jeitos de passar vergonha em Hogwarts: transformar o "
                        "próprio nariz num rabanete, tropeçar na barra da capa na frente da "
                        "escola inteira, ou — no caso de Harry Potter naquela manhã — subir num "
                        "banquinho para ler um poema e sentir a voz desaparecer completamente.",
        img="hp_great_hall_crowd",
        cena=[
            "O diretor Dumbledore pediu que cada aluno do quarto ano lesse um pequeno poema "
            "para toda a escola, reunida no Salão Principal sob o teto encantado que imitava "
            "o céu estrelado. Quando chamaram o nome de Harry, suas pernas viraram gelatina "
            "instantaneamente.",
            "O Devorador de Coragem, que adorava plateia, sentou-se confortavelmente em cima "
            "do ombro de Harry, sussurrando bem no ouvido dele:",
            "— E se sua voz sumir? E se você gaguejar feito um bobo e todo mundo rir? "
            "Melhor fingir que está doente. Melhor correr para o dormitório agora mesmo.",
            "Harry olhou para a plateia enorme e sentiu o pergaminho tremer nas mãos. Foi "
            "então que encontrou, na primeira fileira, o rosto de Hermione — sem nenhum "
            "Cedrico por perto — fazendo positivo com os dois polegares, sorrindo só para ele.",
            "— Você consegue, Harry — ela formou as palavras só com os lábios.",
            "Ele subiu no banquinho, respirou fundo e começou a ler. Na terceira linha, "
            "gaguejou uma palavra e sentiu o rosto pegar fogo de vergonha... mas, em vez de "
            "descer correndo, ele riu de si mesmo, pigarreou e continuou lendo até o final. "
            "O Salão Principal inteiro aplaudiu de pé.",
        ],
        fala_vilao="Argh! Gaguejar era para ser o começo do fim, não uma piadinha engraçada!",
        toque_romance="Quando Harry desceu do banquinho, Hermione correu pelo corredor entre as mesas e o abraçou tão apertado que ele sentiu o coração dela batendo tão rápido quanto o dele — e, por um segundo inteiro, permitiu-se imaginar, escondidinho, que talvez aquilo significasse alguma coisa.",
        gancho_final="Só que, na semana seguinte, uma aula na masmorra apertada do Professor Snape "
                    "prenderia Harry num espaço tão pequeno que nem a coragem recém-descoberta "
                    "pareceria suficiente.",
        psico_titulo="A Coragem de Errar em Público",
        psico_texto="Quase todo mundo tem medo de gaguejar, tremer a voz ou passar vergonha na "
                    "frente dos outros. Mas a verdade é que ninguém é perfeito o tempo todo — e as "
                    "pessoas costumam ser muito mais gentis com nossos deslizes do que a nossa "
                    "própria cabeça imagina. Aceitar que errar faz parte tira uma boa parte do "
                    "peso da vergonha.",
    ),

    # 11 ─────────────────────────────────────────────
    dict(
        num=11, tag="A Masmorra das Poções",
        titulo="A Salinha Sem Nenhuma Janela",
        gancho_abertura="'TRANC!' A porta pesada da masmorra de poções se fechou sozinha "
                        "com um vento frio, prendendo Harry, Hermione e um armário cheio de "
                        "ingredientes estranhos numa salinha de pedra tão pequena e sem "
                        "nenhuma janela que parecia ter sido feita sob medida para o próximo "
                        "ataque do Devorador de Coragem.",
        img="hp_dungeon_tight",
        cena=[
            "— O ar vai acabar! — pensou Harry, o peito apertando feito um cinto puxado "
            "demais. As paredes de pedra pareciam se aproximar devagarinho, centímetro por "
            "centímetro.",
            "O Devorador, esticando-se pelas frestas estreitas da sala, sussurrou animado:",
            "— Estamos presos aqui para sempre, Harry! Ninguém vai nos ouvir gritar!",
            "Hermione, em vez de sair batendo na porta feito louca, sentou-se no chão de "
            "pernas cruzadas e puxou Harry gentilmente para se sentar ao lado dela.",
            "— Harry, olha para mim. O ar não acaba numa sala fechada — tem oxigênio aqui "
            "para um mês inteiro. Vamos fazer um joguinho: me diga cinco coisas douradas que "
            "você consegue ver agora mesmo.",
            "— Um... um frasco dourado... o botão da sua capa... a luz da vela... — Harry "
            "foi contando, e a cada coisa nomeada, o aperto no peito ia afrouxando um "
            "pouquinho. — Seus olhos, quando a luz bate neles de um certo jeito...",
            "Hermione ficou completamente vermelha e desviou o olhar, fingindo examinar um "
            "frasco qualquer na prateleira mais próxima. Dois minutos depois, o professor "
            "Snape abriu a porta normalmente, sem entender por que os dois alunos estavam "
            "tão corados.",
        ],
        fala_vilao="Cinco coisinhas douradas apagaram meu plano inteiro. Isso é humilhante.",
        toque_romance="Harry passou o resto do dia se perguntando se tinha ido longe demais com aquele comentário sobre os olhos dela — e Hermione passou o resto do dia se perguntando por que ainda sentia as bochechas quentes horas depois.",
        gancho_final="Naquela mesma semana, a aula de Astronomia levaria os dois ao topo da torre "
                    "mais alta do castelo — e o Devorador de Coragem já estava esperando, "
                    "escondido entre os degraus em espiral.",
        psico_titulo="Ancoragem 5-4-3-2-1 (Técnica de Atenção Sensorial)",
        psico_texto="Em lugares fechados, a mente cria a sensação de que o ar vai faltar, mesmo "
                    "quando isso não é verdade. A técnica de ancoragem — nomear coisas que vemos, "
                    "tocamos ou ouvimos ao redor — traz a atenção de volta ao momento presente e "
                    "afasta o pensamento de perigo imaginado, trazendo calma rapidinho.",
    ),

    # 12 ─────────────────────────────────────────────
    dict(
        num=12, tag="A Torre de Astronomia",
        titulo="Cem Degraus e uma Lua Cheia Dourada",
        gancho_abertura="Cem degraus de pedra em espiral separavam o chão do castelo do "
                        "topo da Torre de Astronomia — e, para Harry Potter, cada um deles "
                        "parecia mais alto e mais assustador do que o anterior.",
        img="hp_tower_moon",
        cena=[
            "Harry parou logo no primeiro degrau, olhando para cima com a cabeça girando só "
            "de imaginar a altura lá no topo.",
            "— Se eu subir tudo isso, vou desmaiar de vertigem no meio do caminho — sussurrou "
            "ele, sentindo o Devorador se esticar por toda a escadaria como uma névoa escura.",
            "Hermione sentou-se no terceiro degrau, batendo de leve na pedra fria ao lado "
            "dela.",
            "— Harry, você não precisa subir os cem hoje. Suba só até aqui, comigo. A gente "
            "come um sapinho de chocolate e desce rindo, se você quiser.",
            "No primeiro dia, chegaram ao degrau três. No segundo, ao degrau vinte. No quinto "
            "dia, os dois estavam sentados exatamente no topo, o vento mexendo os cabelos em "
            "nuvem de Hermione, enquanto uma lua cheia enorme e dourada iluminava o céu "
            "inteiro de Hogwarts.",
            "— Consegui — sussurrou Harry, olhando para o horizonte com um misto de espanto e "
            "orgulho que ele nunca tinha sentido antes.",
            "— Você sempre foi capaz — respondeu Hermione, sem olhar para ele, olhando "
            "fixamente para a lua, com as mãos entrelaçadas no colo por puro nervosismo. — Só "
            "precisava de alguém que acreditasse nisso junto com você.",
            "Por um segundo inteiro, as mãos deles ficaram tão perto sobre a pedra fria que os "
            "dedos quase se tocaram. Nenhum dos dois teve coragem de dar aquele último "
            "centímetro.",
        ],
        fala_vilao="Interessante como vocês dois são corajosos com escadas... e covardes com centímetros.",
        toque_romance="Harry passou a noite inteira se lembrando daquele quase-toque, se perguntando se tinha imaginado o jeito como a respiração de Hermione tinha ficado presa por um segundo, exatamente como a dele.",
        gancho_final="Mas a próxima aula reservava algo completamente diferente: um guarda-roupa "
                    "que rangia sozinho no corredor do terceiro andar, escondendo dentro de si a "
                    "criatura mais estranha (e mais engraçada) que Hogwarts já tinha visto.",
        psico_titulo="Pequenas Vitórias Constroem Grande Confiança (Autoeficácia — Albert Bandura)",
        psico_texto="A confiança de verdade não nasce de discursos motivacionais — ela nasce de "
                    "pequenas vitórias, uma atrás da outra. Cada degrau conquistado, por menor "
                    "que seja, fica guardado no cérebro como uma prova real de capacidade. É por "
                    "isso que ninguém precisa vencer o medo inteiro de uma vez: basta um degrau "
                    "hoje, e mais um amanhã.",
    ),

    # 13 ─────────────────────────────────────────────
    dict(
        num=13, tag="O Bicho-Papão",
        titulo="O Monstro que Virou Motivo de Riso",
        gancho_abertura="No corredor do terceiro andar havia um velho guarda-roupa de "
                        "madeira que rangia e tremia sozinho — e o professor Lupin explicou, com "
                        "um sorriso misterioso, que dentro dele morava uma criatura chamada "
                        "Bicho-Papão, capaz de se transformar no pior medo de qualquer pessoa "
                        "que olhasse para ela.",
        img="hp_boggart_funny",
        cena=[
            "Quando chegou a vez de Harry, a porta do guarda-roupa se escancarou e, para "
            "surpresa de toda a turma, o Bicho-Papão se transformou exatamente na sombra "
            "sussurrante do Devorador de Coragem — enorme, escura, com olhos de brasa "
            "apagando.",
            "A sala inteira prendeu a respiração. Aquilo era assustador demais para uma aula "
            "qualquer.",
            "— Lembre-se do feitiço, Harry! — sussurrou Hermione da lateral da sala. — O medo "
            "só tem poder se a gente o leva a sério demais. Transforme-o em algo engraçado!",
            "Harry ergueu a varinha, com as mãos ainda tremendo, e gritou com toda a força que "
            "conseguiu reunir:",
            "— RIDDIKULUS!",
            "Na hora, a sombra enorme ganhou patins de rodinha, escorregou numa casca de "
            "banana gigante e caiu de bumbum usando um chapéu de aniversário com uma "
            "flor d'água espirrando na cabeça. A sala inteira explodiu numa gargalhada tão "
            "grande que ecoou pelos corredores do castelo.",
            "O Devorador de Coragem verdadeiro, escondido bem no fundo do peito de Harry, "
            "sentiu-se tão ridicularizado que encolheu de vergonha pela primeira vez em "
            "toda a sua existência.",
        ],
        fala_vilao="Um chapéu de aniversário?! ISSO É UMA OFENSA! Eu sou temido há séculos!",
        toque_romance="Hermione riu tanto que lágrimas brilharam nos olhinhos dela, e ela abraçou o pescoço de Harry na frente de toda a turma, sem se importar nenhum pouquinho com quem estivesse olhando: 'Você foi brilhante!'.",
        gancho_final="Só que aquela vitória tinha deixado o Devorador tão humilhado que ele "
                    "decidiu guardar sua vingança para uma criatura muito mais perigosa — um "
                    "dragãozinho recém-nascido, escondido na cabana de Hagrid.",
        psico_titulo="Rir do Medo sem Perder o Respeito por Ele (Desfusão Cognitiva)",
        psico_texto="Uma das formas mais poderosas de enfraquecer um pensamento assustador é "
                    "olhar para ele com um pouco de humor, sem fingir que ele não existe. Quando "
                    "conseguimos rir de um medo — sem menosprezá-lo — ele perde boa parte do "
                    "poder de nos paralisar. É a diferença entre lutar contra o monstro e "
                    "simplesmente tirar sarro dele.",
    ),

    # 14 ─────────────────────────────────────────────
    dict(
        num=14, tag="A Cabana de Hagrid",
        titulo="O Dragãozinho que Soltava Fumaça de Susto",
        gancho_abertura="Hagrid tinha um segredo guardado dentro de sua cabana de madeira: "
                        "um ovo enorme, quente como brasa, que naquela noite rachou ao meio e "
                        "revelou a criatura mais assustadora — e mais fofa — que Harry já tinha "
                        "visto de perto.",
        img="hp_dragon_baby",
        cena=[
            "O bebê dragão, batizado de Norberto, tinha escamas verdes brilhantes e soltava "
            "labaredas pequenas toda vez que se assustava — o que, para o desespero de Hagrid, "
            "era o tempo todo.",
            "Harry deu três passos para trás na primeira vez que Norberto rugiu, mas Hermione "
            "segurou seu braço com gentileza.",
            "— Não corra, Harry. Ele não está com raiva. Está com medo e com frio, exatamente "
            "como você já se sentiu tantas vezes.",
            "O Devorador de Coragem, ainda dolorido da humilhação do chapéu de aniversário, "
            "tentou uma última cartada, sibilando bem fraquinho:",
            "— E se ele soltar fogo em você? E se você se queimar para sempre?",
            "Mas Harry, para a própria surpresa, respirou fundo, deu três passos calmos para "
            "frente e estendeu a mão com um pedacinho de fruta. Norberto cheirou os dedos "
            "dele, parou de tremer e deitou a cabecinha escamosa no colo de Harry, ronronando "
            "feito um gatinho gigante.",
            "— Ele só precisava que alguém chegasse perto sem gritar — sussurrou Harry, "
            "maravilhado.",
            "Naquele instante, as mãos de Harry e Hermione se encontraram por cima das "
            "escamas quentinhas do dragão. Nenhum dos dois soltou.",
        ],
        fala_vilao="Argh! Chega de fofura! Eu preciso de MEDO DE VERDADE, não de dragõezinhos ronronando!",
        toque_romance="Foi o momento mais próximo que os dois já tinham chegado de um beijo — tão próximo que Harry sentiu o hálito quentinho de Hermione na bochecha — quando um barulho de passos na porta os fez pular para trás, corados feitos pimentões, fingindo que estavam completamente concentrados no dragão.",
        gancho_final="Aquela interrupção, pequena e boba, guardaria uma consequência enorme: "
                    "Harry passaria a semana inteira se perguntando se Hermione tinha ficado "
                    "aliviada ou desapontada com a intromissão — e o Devorador de Coragem sabia "
                    "exatamente como usar essa dúvida a seu favor.",
        psico_titulo="Acolher a Emoção em Vez de Lutar Contra Ela (David H. Barlow)",
        psico_texto="David H. Barlow descobriu algo importante: tentar empurrar um medo para "
                    "longe com força quase sempre faz ele voltar ainda maior. A verdadeira coragem "
                    "não é a ausência de medo — é aproximar-se dele com gentileza, respirando "
                    "fundo, permitindo que ele exista sem deixar que ele decida por nós.",
    ),

    # 15 ─────────────────────────────────────────────
    dict(
        num=15, tag="A Noite da Chuva",
        titulo="A Pior Noite de Harry Potter",
        gancho_abertura="Havia dias em que até o menino mais corajoso do mundo mágico se "
                        "sentia pequenininho de novo — e, para Harry Potter, aquela noite de "
                        "chuva fria seria a prova mais dolorosa disso.",
        img="hp_rain_relapse",
        cena=[
            "Cansado, com fome e sem ter dormido direito havia dias, Harry viu Hermione rindo "
            "animadamente com Cedrico Diggory no salão comunal, os dois debruçados sobre o "
            "mesmo livro de Herbologia.",
            "O Devorador de Coragem, sentindo a fraqueza perfeita para atacar, cresceu de "
            "repente até um tamanho que Harry nunca tinha visto antes, cobrindo o peito dele "
            "inteiro de escuridão gelada:",
            "— Viu? Eu avisei desde o primeiro dia no trem. Ela nunca vai escolher alguém "
            "como você. Ela merece alguém corajoso de verdade, não um menino que ainda treme "
            "com trovão.",
            "Harry saiu correndo para fora do castelo, sentou-se sozinho num degrau de pedra "
            "sob a garoa fina e dourada, e sentiu, pela primeira vez em semanas, que todo o "
            "progresso que tinha feito — a vassoura, a aranha, o lago, a agulha, os cem "
            "degraus da torre — não valia mais nada.",
            "— Eu sou um fracasso — sussurrou ele para a chuva, as lágrimas se misturando às "
            "gotas no rosto. — Vou ser sempre o menino medroso do armário.",
            "Foi então que a porta atrás dele se abriu, derramando um quadrado de luz dourada "
            "e quentinha na escuridão. Hermione, sem o livro de Herbologia, sem Cedrico, "
            "segurava duas canecas de chocolate quente fumegante.",
            "— Eu vi você sair correndo — disse ela, sentando-se ao lado dele na chuva fina, "
            "sem se importar em molhar o próprio vestido. — Harry, tropeçar no caminho não "
            "apaga todos os passos que você já deu. Você está cansado hoje. Amanhã, o "
            "Devorador vai estar pequeno de novo.",
        ],
        fala_vilao="Ela só veio atrás de você por pena, Harry. Não esqueça disso.",
        toque_romance="Harry queria perguntar, ali mesmo, debaixo da chuva, por que ela tinha vindo atrás dele em vez de ficar rindo com Cedrico — mas o medo de ouvir uma resposta que doesse ainda mais o fez engolir a pergunta inteira, junto com um gole de chocolate quente.",
        gancho_final="No dia seguinte, uma visita ao movimentado Beco Diagonal mostraria a Harry "
                    "que ele vinha carregando, sem perceber, um peso muito maior do que qualquer "
                    "mochila de escola.",
        psico_titulo="Tropeçar Não é Voltar ao Início (Prevenção de Recaída)",
        psico_texto="Dias de cansaço, fome ou tristeza deixam qualquer pessoa mais vulnerável a "
                    "sentir o medo antigo de novo — isso é absolutamente normal e não significa "
                    "que todo o progresso desapareceu. A ciência mostra que o aprendizado novo "
                    "continua guardado no cérebro; ele só precisa de descanso, carinho e um novo "
                    "dia para voltar a brilhar mais forte que o medo.",
    ),

    # 16 ─────────────────────────────────────────────
    dict(
        num=16, tag="O Beco Diagonal",
        titulo="A Mochila Pesada Demais para Carregar Sozinho",
        gancho_abertura="Para um passeio simples pelo movimentado Beco Diagonal, Harry "
                        "tinha enchido a mochila de amuletos, poções calmantes e um lenço da "
                        "tia Petúnia 'só por precaução' — sem perceber que aquele peso todo nas "
                        "costas era, na verdade, o próprio Devorador de Coragem disfarçado de "
                        "bagagem.",
        img=None,
        cena=[
            "— Harry, por que você está andando torto? — perguntou Hermione, observando-o "
            "carregar a mochila abarrotada pelas ruas de paralelepípedo cheias de lojas "
            "mágicas e gente acotovelando gente.",
            "— Se eu não tiver minhas coisinhas de segurança, vou passar mal no meio dessa "
            "multidão — confessou ele, apertando as alças com força.",
            "Hermione abriu a mochila com cuidado e tirou, um de cada vez, os itens "
            "guardados ali: um frasco de poção calmante sem receita nenhuma, um apito de "
            "emergência enferrujado, uma pedrinha 'da sorte' encontrada no jardim.",
            "— Harry, se você só consegue sair de casa com todas essas coisinhas, seu "
            "cérebro vai acreditar que são elas que são corajosas — não você. Vamos deixar o "
            "apito guardado hoje. Amanhã, deixamos a pedrinha.",
            "Harry hesitou, sentindo o Devorador se agarrar com força nas alças da mochila, "
            "sussurrando que ele jamais sobreviveria sem aquilo tudo. Mesmo assim, ele "
            "respirou fundo e entregou o apito para Hermione guardar.",
            "Andaram pelo Beco Diagonal inteiro, entre corujas, varinhas e sapos de "
            "chocolate saltitantes, com a mochila bem mais leve nas costas de Harry — e, "
            "para sua surpresa, ele continuou completamente seguro.",
        ],
        fala_vilao="Sem os seus amuletinhos, você vai descobrir rapidinho como é fraco de verdade... ou será que não?",
        toque_romance="Hermione entrelaçou o braço no braço de Harry 'só para não se perderem na multidão', segundo ela — e nenhum dos dois soltou até chegarem de volta ao Caldeirão Furado, horas mais tarde, com as bochechas doloridas de tanto sorrir.",
        gancho_final="De volta a Hogwarts, um espelho antigo e esquecido numa sala vazia estava "
                    "prestes a mostrar a Harry algo que ele nunca teve coragem de admitir nem "
                    "para si mesmo.",
        psico_titulo="Soltando as Muletas aos Poucos (Desmame de Comportamentos de Segurança)",
        psico_texto="Muletas de segurança — como amuletos, remédios sem necessidade ou rituais "
                    "de proteção — parecem ajudar no começo, mas impedem que a gente descubra a "
                    "nossa própria capacidade. Soltando uma de cada vez, com calma, aprendemos "
                    "que a verdadeira coragem sempre esteve dentro de nós, não dentro da mochila.",
    ),

    # 17 ─────────────────────────────────────────────
    dict(
        num=17, tag="A Sala Precisa",
        titulo="O Espelho que Mostrava Desejos Escondidos",
        gancho_abertura="Escondido numa sala secreta que só aparecia para quem realmente "
                        "precisava dela, havia um espelho dourado e imponente com uma inscrição "
                        "estranha na moldura — e o que ele mostrava a Harry Potter era exatamente "
                        "aquilo que ele nunca teve coragem de desejar em voz alta.",
        img="hp_mirror_erised",
        cena=[
            "Harry se aproximou devagar do Espelho de Ered e ficou paralisado: no reflexo, "
            "ele se via adulto, sorrindo, com uma capa de professor de Hogwarts, cercado de "
            "livros e risadas — e, ao seu lado, uma versão adulta de Hermione, de mãos dadas "
            "com ele, olhando-o com o mesmo brilho que ela tinha nos olhos naquele exato "
            "momento.",
            "O Devorador de Coragem, escondido atrás do espelho, sibilou com uma última "
            "tentativa desesperada:",
            "— Isso nunca vai acontecer de verdade, Harry. É só um desejo bobo, impossível. "
            "Guarde essa imagem escondida para sempre, como todos os outros segredos.",
            "Foi então que Hermione entrou na sala, procurando por ele, e parou ao seu lado "
            "diante do espelho.",
            "— O que você está vendo? — perguntou ela, curiosa.",
            "Harry engoliu em seco. Aquela era a pergunta mais assustadora que já tinha "
            "ouvido em toda a sua vida — mais assustadora que altura, que água funda, que "
            "agulha, que trovão. Ele podia contar a verdade e arriscar tudo, ou podia mentir "
            "e continuar seguro para sempre.",
            "— Eu... — começou ele, a voz tremendo mais do que nunca. — Eu vejo... um futuro "
            "que eu tenho medo demais de desejar.",
            "Hermione olhou para o espelho, depois para Harry, depois de volta para o "
            "espelho, com uma expressão que ele não conseguiu decifrar.",
        ],
        fala_vilao="Não conte. NÃO CONTE! Se você contar, eu não terei mais nada para roubar de você!",
        toque_romance="Naquele silêncio enorme entre os dois, com o coração de Harry batendo tão alto que ele tinha certeza de que Hermione podia ouvir, o Devorador de Coragem, pela primeira vez em toda a história, começou a tremer de verdadeiro medo — porque sabia que a coragem mais rara do mundo estava prestes a nascer.",
        gancho_final="Mas antes que Harry conseguisse dizer mais uma palavra, um sino tocou "
                    "anunciando a Grande Provação de Coragem de Hogwarts — o desafio mais "
                    "temido do ano — e o Devorador teve uma última cartada guardada para o "
                    "grande final.",
        psico_titulo="Coragem Vulnerável e Ação Guiada por Valores",
        psico_texto="Existe um tipo de coragem que ninguém fala muito sobre: a coragem de "
                    "mostrar os próprios sentimentos verdadeiros, mesmo sem garantia nenhuma de "
                    "que vai dar certo. Psicólogos chamam isso de vulnerabilidade — e, apesar de "
                    "parecer assustador, é exatamente essa coragem que constrói as conexões mais "
                    "verdadeiras e duradouras entre as pessoas.",
    ),

    # 18 ─────────────────────────────────────────────
    dict(
        num=18, tag="A Grande Provação",
        titulo="O Duelo Final Contra o Devorador de Coragem",
        gancho_abertura="A Grande Provação de Coragem de Hogwarts reunia, num único "
                        "circuito mágico, tudo o que qualquer aluno mais temia — e, para Harry "
                        "Potter, aquilo significava enfrentar de uma só vez a altura, o escuro, "
                        "os latidos, a multidão e, no fim de tudo, o próprio Devorador de "
                        "Coragem em sua forma verdadeira.",
        img="hp_cover",
        cena=[
            "O circuito levava os alunos por uma torre alta, um corredor totalmente escuro, "
            "e terminava num palco enorme na frente da escola inteira. No caminho, à espera "
            "de Harry no ponto mais alto da torre, o Devorador finalmente assumiu sua forma "
            "verdadeira: uma sombra gigantesca, do tamanho de um dragão, com olhos de brasa "
            "quase apagando de tanto ódio.",
            "— CHEGOU A HORA, HARRY POTTER — rugiu a criatura, sua voz ecoando por todo o "
            "castelo. — VOCÊ NUNCA SERÁ CORAJOSO O SUFICIENTE. NUNCA SERÁ AMADO O SUFICIENTE. "
            "SEMPRE SERÁ O MENINO PEQUENO DO ARMÁRIO!",
            "Harry sentiu a cicatriz de raio na testa latejar com força, quente e fria ao "
            "mesmo tempo — o alarme mais antigo do seu corpo, avisando que algo grande estava "
            "próximo. Mas, pela primeira vez, ele parou para pensar: será que esse alarme "
            "estava certo sobre o tamanho do perigo, ou só sobre a presença dele?",
            "Ele respirou fundo, contando até quatro. Soltou o ar devagar, contando até "
            "seis. Lembrou do lago que parou de parecer gelado, da agulha que virou "
            "cutucadinha de formiga, do cachorro de três cabeças que só queria carinho, do "
            "monstro que virou motivo de riso com um chapéu de aniversário.",
            "— Você está certo numa coisa — disse Harry, com a voz surpreendentemente firme. "
            "— Eu era o menino pequeno do armário. Mas esse menino subiu cem degraus de "
            "torre, entrou numa água que parecia gelada, ficou de pé na frente da escola "
            "inteira tremendo e continuou de pé mesmo assim. Meu medo é real. Mas ele não "
            "manda mais em mim.",
            "A sombra gigantesca vacilou, encolhendo um pouco. Do fundo da multidão reunida "
            "ao pé da torre, uma voz gritou, mais alta que todas as outras:",
            "— E ele não está sozinho! — era Hermione, subindo os cem degraus correndo, sem "
            "fôlego, parando ao lado dele com a mão estendida.",
            "Harry segurou a mão dela, sentiu a coragem dela somar-se à sua própria, e "
            "gritou, com toda a força do coração:",
            "— Eu não preciso que você desapareça para sempre! Eu só preciso que você pare "
            "de decidir por mim!",
            "A sombra gigantesca do Devorador de Coragem soltou um último grito arrastado e "
            "encolheu, encolheu, encolheu — até virar do tamanho de uma borboleta preta, "
            "pousando quietinha no ombro de Harry, pequena e inofensiva, como sempre deveria "
            "ter sido.",
        ],
        fala_vilao="Não... não pode ser... como você...",
        toque_romance="No alto da torre, de mãos dadas, com a plateia inteira aplaudindo lá embaixo, Harry olhou para Hermione e percebeu que o coração dele batia acelerado — mas, dessa vez, não era medo nenhum.",
        gancho_final="Com o Devorador finalmente do tamanho de uma borboleta, restava a Harry "
                    "enfrentar um último desafio — talvez o mais assustador e o mais doce de "
                    "todos: contar para Hermione, em voz alta, o que ele tinha visto no Espelho "
                    "de Ered.",
        psico_titulo="Exposição Culminante e a Vitória da Aceitação (Barlow & Craske)",
        psico_texto="Quando alguém enfrenta, um a um, todos os medos que vinha evitando, o "
                    "cérebro aprende uma lição definitiva: o perigo imaginado nunca era do "
                    "tamanho da sombra que ele projetava. A coragem não apaga o medo — ela apenas "
                    "o encolhe até um tamanho que cabe no bolso, sem nunca mais mandar em nossas "
                    "escolhas.",
    ),

    # 19 ─────────────────────────────────────────────
    dict(
        num=19, tag="Hogsmeade sob a Neve",
        titulo="A Caneca com Dois Canudinhos",
        gancho_abertura="Depois de vencer o pior monstro da sua vida, Harry Potter "
                        "descobriu que ainda existia um desafio capaz de deixar suas mãos "
                        "suadas: convidar Hermione Granger para um encontro a sós no vilarejo "
                        "coberto de neve de Hogsmeade.",
        img="hp_hogsmeade_date",
        cena=[
            "Harry passou uma hora inteira penteando os cabelos na frente do espelho (que "
            "continuaram exatamente tão desarrumados quanto sempre) e escolheu o cachecol "
            "mais bonito que tinha. Sentados numa mesinha da taverna, cercados por velinhas "
            "acesas e neve caindo lá fora, ele sentiu um friozinho gostoso na barriga.",
            "— Você está tremendo de novo? — perguntou Hermione, com um sorrisinho travesso. "
            "— É medo, Harry?",
            "— Não... — confessou ele, corando até as orelhas. — Esse frio na barriga é bem "
            "diferente de todos os outros. Esse eu gosto de sentir.",
            "Hermione cobriu a mão dele com a dela, por cima da mesa de madeira, sem nenhuma "
            "pressa de soltar.",
            "— O meu também está fazendo isso — sussurrou ela.",
            "Eles dividiram uma caneca enorme de chocolate quente com dois canudinhos, "
            "rindo baixinho toda vez que os narizes quase se esbarravam. Quando um "
            "pouquinho de espuma de caramelo ficou grudado no bigode de Hermione, Harry "
            "limpou com o guardanapo, devagar, sem tirar os olhos dos dela nem por um "
            "segundo.",
        ],
        fala_vilao=None,
        toque_romance="'Talvez', pensou Harry, olhando para a borboleta pretinha e pequena pousada tranquilamente no seu ombro, 'o Devorador de Coragem nunca tenha sido páreo para uma xícara de chocolate quente dividida com a pessoa certa'.",
        gancho_final="No caminho de volta ao castelo, atravessando uma velha ponte de pedra "
                    "coberta de neve, Harry sentiu que finalmente tinha chegado a hora de dizer, "
                    "em voz alta, as palavras que vinha guardando havia tanto tempo.",
        psico_titulo="Diferenciando o Medo da Paixão (Ativação Fisiológica Positiva)",
        psico_texto="O corpo usa sensações parecidas — coração acelerado, calor no rosto, "
                    "borboletas na barriga — tanto para o susto quanto para a alegria e o amor. "
                    "Aprender a perceber a diferença entre 'isso é perigo' e 'isso é emoção boa' é "
                    "um passo importante para viver as próprias emoções com mais leveza e menos "
                    "confusão.",
    ),

    # 20 ─────────────────────────────────────────────
    dict(
        num=20, tag="A Ponte Coberta de Neve",
        titulo="A Confissão que Parecia Impossível",
        gancho_abertura="No meio da ponte de pedra mais antiga de Hogsmeade, com flocos de "
                        "neve dourados brilhando no ar como se o próprio céu estivesse "
                        "aplaudindo, Harry Potter parou de andar — porque, finalmente, tinha "
                        "juntado toda a coragem que precisava.",
        img="hp_bridge_snow",
        cena=[
            "— Hermione — começou ele, a voz tremendo mais do que em qualquer altura, água "
            "fria ou trovão que já tivesse enfrentado. — No Espelho de Ered, eu vi a gente "
            "dois, mais velhos, de mãos dadas. E eu tenho medo — um medo enorme, do tamanho "
            "de um dragão de verdade — de contar isso para você, porque tenho certeza "
            "absoluta de que uma menina inteligente e corajosa como você jamais gostaria de "
            "um garoto que treme até de torradinha.",
            "Hermione ficou tão parada e tão quieta que, por um instante horrível, Harry "
            "achou que tinha estragado tudo. A borboletinha preta no seu ombro tremeu, "
            "assustada.",
            "Então ela começou a rir — não de zombaria, mas de um jeito surpreso e aliviado, "
            "quase incrédulo.",
            "— Harry Potter, seu bobo enorme! Eu decorei sete livros sobre Hogwarts antes de "
            "conhecer você, e nenhum deles me preparou para o dia em que eu ficaria acordada "
            "de noite pensando se você tinha gostado do jeito como eu ri de uma piada. Eu "
            "achava que VOCÊ nunca ia reparar em mim, porque eu sou só a menina chata que "
            "sabe tudo dos livros.",
            "— Você nunca foi chata — sussurrou Harry, o coração disparando de um jeito "
            "completamente novo. — Você foi a primeira pessoa que me olhou como se eu não "
            "fosse só o menino medroso.",
            "— E você foi o primeiro que me olhou como se eu não fosse só a sabe-tudo dos "
            "livros — respondeu ela, os olhos brilhando com lágrimas felizes.",
            "A neve continuou caindo, os lampiões da ponte brilharam mais dourados do que "
            "nunca, e Harry Potter, o garoto que tinha medo de quase tudo, teve coragem de "
            "dar aquele último centímetro que faltava. Encostou de leve a testa na dela — "
            "bem onde a cicatriz de raio brilhava suavemente — e sussurrou:",
            "— Posso?",
            "— Pode — respondeu Hermione.",
            "E ali, no meio da ponte coberta de neve, os dois se beijaram pela primeira vez, "
            "devagarinho e cheio de sorrisos tímidos no meio do beijo, enquanto a "
            "borboletinha preta no ombro de Harry se desfazia, finalmente, numa nuvem de "
            "poeira dourada que o vento levou embora para sempre.",
        ],
        fala_vilao=None,
        toque_romance="O amor que Harry jurava impossível nunca tinha sido não correspondido: ele só estava escondido atrás do mesmo tipo de medo que fazia Hermione duvidar de si mesma — e bastou um dos dois ter coragem de falar a verdade para descobrirem que os dois corações batiam, havia meses, exatamente no mesmo ritmo.",
        gancho_final="Faltava apenas um capítulo nesta história — o mais feliz de todos.",
        psico_titulo="Vínculo Seguro e a Coragem de Ser Vulnerável",
        psico_texto="Muitas vezes, o medo de não sermos amados nos faz esconder quem realmente "
                    "somos — e essa escondida pode durar anos sem necessidade nenhuma. Estudos "
                    "sobre vínculo afetivo mostram que relações verdadeiras e seguras nascem "
                    "exatamente quando alguém tem coragem de se mostrar por inteiro, medos e "
                    "tudo mais, permitindo que o outro faça o mesmo.",
    ),

    # 21 ─────────────────────────────────────────────
    dict(
        num=21, tag="O Casamento Mágico",
        titulo="Felizes Para Sempre na Casinha com Jardim",
        gancho_abertura="Diz a lenda que, muitos anos depois daquele beijo na ponte coberta "
                        "de neve, os bruxinhos mais novos de Hogwarts ainda contavam a história "
                        "do menino que venceu o Devorador de Coragem — mas a parte favorita de "
                        "todo mundo era sempre o final.",
        img="hp_wedding_final",
        cena=[
            "Os anos passaram voando como uma coruja apressada. Harry e Hermione cresceram, "
            "estudaram muito, riram muito mais, e se tornaram dois dos maiores bruxos de sua "
            "geração — não porque tivessem parado de sentir medo, mas porque aprenderam, "
            "juntos, a não deixar que ele decidisse suas vidas.",
            "Num lindo dia de primavera dourada, com o sol brilhando sobre o gramado do "
            "castelo e música suave flutuando no ar, Harry e Hermione se casaram debaixo de "
            "um arco de flores douradas. Hermione usava um vestido branco bordado com "
            "estrelinhas brilhantes, os cabelos em nuvem enfeitados com pequenas rosas; Harry "
            "usava sua melhor capa, a cicatriz de raio brilhando de leve na testa como um "
            "lembrete carinhoso de tudo o que ele tinha superado para chegar até ali.",
            "Hagrid chorava rios de lágrimas de felicidade num lenço do tamanho de uma toalha "
            "de mesa. Rony fez um discurso tão engraçado que todo mundo chorou de rir. E "
            "Norberto, o dragãozinho já bem crescido, voou baixinho sobre a cerimônia "
            "soprando fumacinha em formatinho de coração.",
            "— Aceito — disse Harry, olhando bem fundo nos olhos castanhos de Hermione, a "
            "mesma menina do trem, dos livros grossos e do sorriso que tinha feito seu "
            "coração dar um solavanco pela primeira vez.",
            "— Aceito — respondeu ela, sorrindo através das lágrimas.",
            "Eles construíram uma casinha de pedra clara nos arredores de Hogsmeade, com um "
            "jardim cheio de flores perfumadas, uma biblioteca enorme (é claro) e janelas "
            "sempre abertas para deixar o sol entrar. E, em noites de tempestade, quando os "
            "trovões faziam CABUM! contra as vidraças, Harry não corria mais para debaixo da "
            "cama — ele apenas abraçava Hermione no sofá, tomava um chocolate quente e "
            "sorria, porque sabia, com toda a certeza do mundo, que junto dela nenhum medo "
            "jamais seria grande demais.",
            "E assim, Harry Potter — o garoto do armário debaixo da escada, o menino que "
            "tinha medo de quase tudo e que um dia venceu o próprio Devorador de Coragem — "
            "viveu para sempre feliz ao lado da menina que sempre acreditou nele, mesmo "
            "quando ele ainda não tinha coragem de acreditar em si mesmo.",
            "FIM.",
        ],
        fala_vilao=None,
        toque_romance="E, se você prestar bem atenção nas noites de lua cheia sobre Hogwarts, dizem que ainda é possível ver uma borboletinha dourada esvoaçando tranquila pelos jardins do castelo — pequena, inofensiva, e completamente domada pelo amor.",
        gancho_final=None,
        psico_titulo="Resiliência, Amor Seguro e uma Vida Bem Vivida",
        psico_texto="Superar medos não significa nunca mais sentir nada de desconfortável — "
                    "significa ganhar a liberdade de escolher como viver, mesmo com o coração "
                    "acelerado às vezes. Quando essa coragem se une a um amor verdadeiro e "
                    "seguro, a vida ganha um tipo especial de leveza: a certeza de que, "
                    "acompanhados, nenhum medo precisa ser enfrentado sozinho.",
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
    story.append(Spacer(1, 0.6 * cm))
    p(story, "DRA. PRISCILA PALOMO  ·  CRP 98007", s["cover_brand"])
    story.append(Spacer(1, 0.25 * cm))
    story.append(HRFlowable(width="40%", thickness=2, color=NAVY, spaceBefore=0, spaceAfter=10))
    p(story, "Harry Potter e a Magia da Coragem", s["cover_title"])
    p(story, "A Batalha Secreta Contra o Devorador de Coragem<br/>"
             "e o Amor que Ele Achava Impossível", s["cover_sub"])
    story.append(Spacer(1, 0.35 * cm))
    story.append(ilustra("hp_cover", 13.5 * cm))
    story.append(Spacer(1, 0.35 * cm))
    p(story, "“O pior inimigo de Harry Potter não usava capa preta.<br/>"
             "Ele era um sussurro do tamanho do medo — e vivia dentro dele.”", s["quote"])
    story.append(Spacer(1, 0.3 * cm))
    p(story, "www.priscilapalomo.com", s["cover_brand"])
    story.append(PageBreak())

    # ═══════════ CARTA DE ABERTURA ═══════════
    p(story, "Uma Cartinha Especial para os Leitores", s["h1"])
    story.append(hr())
    p(story, "Querido(a) leitor(a),", s["prosa_first"])
    p(story, "Todo mundo acha que os heróis dos livros nunca sentem medo de nada. Mas a "
      "verdade é que ter medo é a coisa mais humana e mais corajosa do mundo — porque "
      "sentir medo e continuar em frente é exatamente isso: coragem de verdade.", s["prosa"])
    p(story, "Neste livro, você vai acompanhar <b>Harry Potter</b>, um bruxinho doce que "
      "carregava dentro de si um inimigo secreto chamado <b>Devorador de Coragem</b> — "
      "uma sombra sussurrante que crescia a cada vez que ele fugia de algo, e encolhia a "
      "cada vez que ele criava coragem de olhar de frente. Com a ajuda da sua melhor amiga "
      "(e grande amor escondido) <b>Hermione Granger</b>, Harry vai descobrir que não "
      "precisa de varinha mágica nenhuma para vencer o próprio medo: basta um degrau de "
      "cada vez, muito carinho, e a coragem de dizer a verdade — inclusive sobre o que "
      "sente no coração.", s["prosa"])
    p(story, "Ao final de cada capítulo, uma caixinha dourada chamada <b>O Segredo Mágico "
      "da Mente</b> vai explicar, de um jeito bem simples, o que a Psicologia de verdade "
      "ensina sobre aquele medo. E, no fim de cada capítulo, deixamos sempre uma pistinha do "
      "que vem a seguir — porque toda boa história merece um gostinho de quero mais!", s["prosa"])
    p(story, "<b>Aviso carinhoso:</b> este livro tem finalidade lúdica e psicoeducativa. Ele "
      "não substitui o acompanhamento de um psicólogo clínico quando o medo for muito "
      "intenso ou estiver atrapalhando a vida de alguém.", s["small"])
    story.append(Spacer(1, 6))
    p(story, "Com todo o carinho e muitas borboletas felizes na barriga,<br/>"
             "<b>Dra. Priscila Palomo</b> — Psicóloga Clínica (CRP 98007)<br/>"
             "Doutora em Psicologia · Especialista em Fobias e TCC · www.priscilapalomo.com", s["small"])
    story.append(PageBreak())

    # ═══════════ SUMÁRIO ═══════════
    p(story, "Índice dos Capítulos Encantados", s["h1"])
    story.append(hr())
    p(story, "<i>Acompanhe Harry Potter na batalha contra o Devorador de Coragem — e na "
             "descoberta de um amor que ele tinha certeza de ser impossível:</i>", s["small"])
    story.append(Spacer(1, 4))
    for c in CAPITULOS:
        p(story, f"<b>Capítulo {c['num']:02d}:</b> {c['titulo']} &nbsp;<i>({c['tag']})</i>", s["toc"])
    story.append(PageBreak())

    # ═══════════ OS CAPÍTULOS ═══════════
    for c in CAPITULOS:
        capitulo(
            story=story,
            num=c["num"],
            tag=c["tag"],
            titulo=c["titulo"],
            gancho_abertura=c["gancho_abertura"],
            img=c["img"],
            cena_paragrafos=c["cena"],
            fala_vilao=c["fala_vilao"],
            toque_romance=c["toque_romance"],
            gancho_final=c["gancho_final"],
            psico_titulo=c["psico_titulo"],
            psico_texto=c["psico_texto"],
            s=s,
        )

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"OK: {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
