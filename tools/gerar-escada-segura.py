#!/usr/bin/env python3
"""Gera o livro ilustrado:
'Harry Potter e as Magias da Coragem — Um Capítulo para Cada Fobia'

Cada capítulo = um tipo de fobia + uma magia + historinha lúdica (início, meio, fim).
Inspirado nas aventuras de Harry Potter como modelo de determinação.
Psicoeducação baseada em Freud (caso Pequeno Hans, angústia × medo) e
Magalhães Coelho (resposta defensiva, evitamento, habituação).
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
MAGIC_BOX = HexColor("#FFF8E6")
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
        fontSize=23, textColor=INK, alignment=TA_CENTER, leading=28, spaceAfter=10,
    )
    s["cover_sub"] = ParagraphStyle(
        "cover_sub", parent=base["Normal"], fontName="Helvetica",
        fontSize=11.5, textColor=MUTED, alignment=TA_CENTER, leading=16, spaceAfter=6,
    )
    s["part"] = ParagraphStyle(
        "part", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=10, textColor=ORANGE, alignment=TA_LEFT, spaceBefore=0, spaceAfter=2,
    )
    s["h1"] = ParagraphStyle(
        "h1", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=16.5, textColor=NAVY, spaceBefore=0, spaceAfter=6, leading=20,
    )
    s["h2"] = ParagraphStyle(
        "h2", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=11.5, textColor=INK, spaceBefore=8, spaceAfter=4, leading=14,
    )
    s["prosa"] = ParagraphStyle(
        "prosa", parent=base["Normal"], fontName="Helvetica",
        fontSize=9.8, textColor=INK, alignment=TA_JUSTIFY, leading=14.8,
        spaceAfter=6, firstLineIndent=12,
    )
    s["prosa_first"] = ParagraphStyle(
        "prosa_first", parent=s["prosa"], firstLineIndent=0,
    )
    s["gancho_abertura"] = ParagraphStyle(
        "gancho_abertura", parent=base["Normal"], fontName="Helvetica-BoldOblique",
        fontSize=10.2, textColor=NAVY, alignment=TA_LEFT, leading=14.8,
        spaceAfter=8, firstLineIndent=0,
    )
    s["gancho_final"] = ParagraphStyle(
        "gancho_final", parent=base["Normal"], fontName="Helvetica-BoldOblique",
        fontSize=9.8, textColor=SHADOW, alignment=TA_LEFT, leading=14,
        spaceBefore=4, spaceAfter=2, leftIndent=10, rightIndent=10,
    )
    s["vilao_fala"] = ParagraphStyle(
        "vilao_fala", parent=base["Normal"], fontName="Helvetica-Oblique",
        fontSize=9.8, textColor=SHADOW, alignment=TA_CENTER, leading=14,
        spaceBefore=6, spaceAfter=6, leftIndent=16, rightIndent=16,
    )
    s["box_title"] = ParagraphStyle(
        "box_title", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=10.2, textColor=NAVY, alignment=TA_LEFT, leading=13,
    )
    s["box_body"] = ParagraphStyle(
        "box_body", parent=base["Normal"], fontName="Helvetica",
        fontSize=9, textColor=INK, alignment=TA_JUSTIFY, leading=13.2,
    )
    s["magia_spell"] = ParagraphStyle(
        "magia_spell", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=12, textColor=GOLD, alignment=TA_CENTER, leading=15,
        spaceBefore=4, spaceAfter=4,
    )
    s["small"] = ParagraphStyle(
        "small", parent=base["Normal"], fontName="Helvetica",
        fontSize=8.3, textColor=MUTED, leading=11.5, spaceAfter=4,
    )
    s["toc"] = ParagraphStyle(
        "toc", parent=base["Normal"], fontName="Helvetica",
        fontSize=8.8, textColor=INK, leading=13.5, spaceAfter=2,
    )
    return s


def hr():
    return HRFlowable(width="100%", thickness=1, color=LINE, spaceBefore=2, spaceAfter=8)


def ilustra(nome, largura=11.2 * cm):
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


def caixa(titulo, texto, s, bg=WARM_BOX, border=GOLD, prefix="✨"):
    header = [Paragraph(f"{prefix} <b>{titulo}</b>", s["box_title"])]
    body = [Paragraph(texto, s["box_body"])]
    conteudo = header + [Spacer(1, 3)] + body
    t = Table([[c] for c in conteudo], colWidths=[16.5 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 1, border),
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
            f"Harry Potter e as Magias da Coragem  ·  Dra. Priscila Palomo  ·  p. {page}"
        )
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.4)
        canvas.line(2 * cm, 1.5 * cm, A4[0] - 2 * cm, 1.5 * cm)
    canvas.restoreState()


def p(story, text, style):
    story.append(Paragraph(text, style))


def capitulo(story, c, s):
    p(story, f"CAPÍTULO {c['num']:02d} · {c['fobia'].upper()}", s["part"])
    p(story, c["titulo"], s["h1"])
    story.append(hr())
    if c.get("gancho_abertura"):
        p(story, c["gancho_abertura"], s["gancho_abertura"])
    if c.get("img"):
        story.append(ilustra(c["img"]))
        story.append(Spacer(1, 5))

    p(story, "O Começo", s["h2"])
    for i, texto in enumerate(c["inicio"]):
        p(story, texto, s["prosa_first"] if i == 0 else s["prosa"])

    p(story, "O Meio", s["h2"])
    for texto in c["meio"]:
        p(story, texto, s["prosa"])

    if c.get("fala_vilao"):
        p(story, f"🌑 <i>{c['fala_vilao']}</i>", s["vilao_fala"])

    p(story, "A Superação", s["h2"])
    for texto in c["fim"]:
        p(story, texto, s["prosa"])

    magia = c["magia"]
    magia_rows = [
        Paragraph(f"🪄 <b>A Magia deste Capítulo: {magia['nome']}</b>", s["box_title"]),
        Spacer(1, 4),
        Paragraph(f"<font color='#C8940A'><b>{magia['feitiço']}</b></font>", s["magia_spell"]),
        Paragraph(f"<i>{magia['gesto']}</i>", s["box_body"]),
        Spacer(1, 4),
        Paragraph(magia["significado"], s["box_body"]),
    ]
    t_magia = Table([[r] for r in magia_rows], colWidths=[16.5 * cm])
    t_magia.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MAGIC_BOX),
        ("BOX", (0, 0), (-1, -1), 1, GOLD),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(KeepTogether([t_magia, Spacer(1, 4)]))

    story.append(caixa(
        f"O Segredo da Mente: {c['psico_titulo']}",
        c["psico_texto"], s,
    ))

    if c.get("gancho_final"):
        story.append(Spacer(1, 2))
        p(story, f"➜ {c['gancho_final']}", s["gancho_final"])
    story.append(PageBreak())


# ═══════════════════════════════════════════════════════════════════════════
CAPITULOS = [
    dict(
        num=0, fobia="Prólogo",
        titulo="O Menino da Cicatriz e o Devorador de Coragem",
        gancho_abertura="Antes de aprender qualquer feitiço, você precisa conhecer o verdadeiro "
                        "inimigo de Harry Potter — e descobrir que ele não morava em nenhuma masmorra "
                        "do castelo.",
        img="hp_closet_dark",
        inicio=[
            "Harry Potter vivia no armário debaixo da escada, com óculos redondos, cabelo "
            "desgrenhado e uma cicatriz de raio na testa que todos achavam sinal de herói. "
            "Mas, sozinho à noite, Harry sabia outra coisa: tinha medo de quase tudo — do escuro, "
            "dos barulhos, das sombras que se mexiam no canto.",
            "Aquela sombra fina, com olhinhos de brasa, era o <b>Devorador de Coragem</b>. Ele "
            "não mordia de verdade; sussurrava. E cada vez que Harry fugia de um medo, a sombra "
            "engordava um pouquinho.",
        ],
        meio=[
            "Quando a carta de Hogwarts chegou, Harry achou que a magia resolveria tudo. "
            "Mas no primeiro dia de aula, descobriu que até bruxos famosos tremiam diante de "
            "aranhas, alturas, multidões, trovões e muitas outras coisas.",
            "Foi então que Hermione Granger — a menina dos livros grossos e do coração enorme — "
            "disse a frase que mudaria tudo: <i>“Harry, coragem não é não sentir medo. É sentir "
            "medo e dar um passinho mesmo assim.”</i>",
            "Ela explicou que, na Psicologia, cada medo tem nome. Quando damos nome ao medo, "
            "ele encolhe. E para cada tipo de medo existe uma <b>magia</b> — não de varinha, mas "
            "de atitude, respiração e prática repetida.",
        ],
        fala_vilao="Fica quietinho, Harry… Se você nunca arriscar, eu nunca vou embora.",
        fim=[
            "Harry olhou para a cicatriz no espelho embaçado do banheiro e decidiu: se ia ser "
            "herói de alguma história, seria o herói que aprende. Capítulo por capítulo, fobia "
            "por fobia, magia por magia.",
            "Nos capítulos seguintes, você vai acompanhar Harry enfrentando cada tipo de medo "
            "com início, meio e fim de superação — como nas grandes aventuras de Hogwarts, onde "
            "a determinação vale mais do que qualquer poção pronta.",
        ],
        magia=dict(
            nome="Lumos Interior",
            feitiço="Lumos Interior!",
            gesto="Mão no peito, respiração lenta, três vezes.",
            significado="Acende a luz que já existe dentro de você. Antes de enfrentar qualquer "
                        "medo lá fora, acenda a calma aqui dentro.",
        ),
        psico_titulo="Medo, Angústia e o Ciclo do Evitamento (Freud e Magalhães Coelho)",
        psico_texto="Freud observou, no caso do Pequeno Hans, que a angústia pode começar sem "
                    "objeto claro — só depois o medo se fixa em algo (como um cavalo). Magalhães "
                    "Coelho acrescenta: primeiro vem a resposta defensiva do corpo; depois, a emoção "
                    "de medo. E quando evitamos o que tememos, alimentamos a “besta” da ansiedade. "
                    "Superar não é eliminar o medo de uma vez — é deixar de obedecer a ele.",
        gancho_final="A primeira fobia que Harry enfrentaria de verdade tinha oito patas e morava "
                     "na Floresta Proibida — e ela estava esperando por ele na próxima aula de "
                     "Herbologia.",
    ),

    dict(
        num=1, fobia="Aracnofobia",
        titulo="A Teia que Parecia uma Prisão",
        gancho_abertura="Na Floresta Proibida, onde até as árvores sussurram segredos, Harry viu "
                        "algo se mover entre os galhos — e o coração dele disparou antes da cabeça "
                        "conseguir pensar.",
        img="hp_forest_spider",
        inicio=[
            "A turma ia colher raízes para a aula de Herbologia quando Ron gritou: “Olha o tamanho "
            "daquela aranha!” Era uma aranha enorme, pendurada numa teia prateada entre dois "
            "carvalhos. Harry sentiu o estômago gelar. Lembrava-se de ter visto aranhas no armário "
            "da Rua dos Alfeneiros e de ter passado a noite inteira acordado.",
            "Hermione notou o rosto pálido do amigo. — É aracnofobia, Harry. Medo de aranhas. "
            "Uma das fobias de animais mais comuns do mundo.",
        ],
        meio=[
            "O Devorador de Coragem sussurrou no ouvido de Harry: <i>“Corre. Nunca mais volte à "
            "floresta. Nunca.”</i> Harry recuou dois passos. Ron e Hermione foram em frente; Harry "
            "ficou parado, os pés colados no chão úmido.",
            "Hermione voltou sozinha. — No caso do Pequeno Hans, Freud mostrou que o medo pode "
            "se deslocar de um lugar para outro — da angústia sem nome para o cavalo, ou para a "
            "aranha. O importante é que o medo <b>tem nome</b> e pode ser treinado.",
            "Ela pediu que Harry olhasse a teia de longe: — Veja as linhas. É engenharia, não "
            "armadilha para você. A aranha não está vindo. Você está seguro aqui.",
        ],
        fala_vilao="Se você olhar, ela vai pular! Melhor fechar os olhos para sempre.",
        fim=[
            "Harry respirou fundo, pôs a mão no peito e murmurou o feitiço que Hermione ensinou. "
            "Deu um passo. Depois outro. Parou a três metros da teia, contou até dez, e viu: a "
            "aranha nem se mexeu para ele.",
            "— Eu senti medo — disse Harry, a voz ainda tremendo — mas não corri. A teia é só "
            "teia. Eu sou mais do que o meu medo.",
            "O Devorador encolheu um tiquinho na sombra das raízes. Era o primeiro degrau.",
        ],
        magia=dict(
            nome="Revelio Tela",
            feitiço="Revelio Tela!",
            gesto="Aponte a varinha (ou o dedo) para o medo e diga o nome da fobia em voz baixa.",
            significado="Revela que a teia do medo é feita de pensamentos, não de ferro. "
                        "Nomear a aracnofobia já quebra metade da ilusão.",
        ),
        psico_titulo="Fobia de Animais e Deslocamento do Medo (Freud)",
        psico_texto="No DSM-5, fobias de animais (aranhas, cobras, cães) formam uma família à "
                    "parte. Freud viu que o medo pode se fixar num objeto simbólico quando a "
                    "angústia original não encontra palavras. A TCC ensina exposição gradual: "
                    "foto → vídeo → distância segura → aproximação. Repetição ensina o cérebro "
                    "que o alarme estava exagerado.",
        gancho_final="Na semana seguinte, um sussurro diferente ecoaria nas paredes de pedra "
                     "do castelo — e Harry descobriria que nem todo medo de animal anda em oito patas.",
    ),

    dict(
        num=2, fobia="Ofidiofobia",
        titulo="O Sussurro na Língua das Cobras",
        gancho_abertura="Nas masmorras de Hogwarts, Harry ouviu um som que ninguém mais ouvia — "
                        "e isso quase o fez desistir de ser quem era.",
        img="hp_dungeon_tight",
        inicio=[
            "Durante a aula de Defesa Contra as Artes das Trevas, o professor mostrou um vídeo "
            "de cobras. Vários alunos acharam fascinante. Harry sentiu náusea. Não era só o bicho "
            "escamoso — era a memória de sons sibilantes em corredores escuros, de se sentir "
            "diferente por entender uma língua que os outros não entendiam.",
            "— Ofidiofobia — disse Hermione, sem drama. — Medo de cobras. Muito antigo no cérebro "
            "humano; nosso ancestral que fugia viveu para contar a história.",
        ],
        meio=[
            "O Devorador aproveitou: <i>“Você é estranho, Harry. Até as cobras gostam de você. "
            "Fique longe de todo mundo.”</i> Harry quis faltar à aula seguinte.",
            "Mas Hermione lembrou o caso de Hans: o medo do cavalo não era só do cavalo — era "
            "medo de coisas grandes que não se controlam. Com cobras, muitas vezes o medo mistura "
            "perigo real e fantasia.",
            "Ela propôs um plano: primeiro, desenhar uma cobra no papel. Depois, ver foto. Depois, "
            "vídeo com pausa. Um degrau por vez — como Harry subiu a escada do armário quando "
            "soube que Hogwarts existia.",
        ],
        fala_vilao="Uma cobra vai te morder. Você sabe que vai.",
        fim=[
            "Harry desenhou uma cobra pequena, verde, com olhos de botão. Riu do próprio desenho. "
            "No dia seguinte, assistiu a trinta segundos de vídeo e fechou o livro antes que o "
            "pânico chegasse a dez.",
            "— Parei quando precisava — disse a Hermione. — Mas voltei. Isso é determinação.",
            "Na terceira tentativa, ficou um minuto inteiro. O Devorador sibilou, mas Harry não "
            "obedeceu.",
        ],
        magia=dict(
            nome="Serpens Quieta",
            feitiço="Serpens Quieta!",
            gesto="Pés firmes no chão, ombros para baixo, olhar no horizonte — nunca fixo na boca.",
            significado="Acalma o corpo para que a mente possa pensar. A cobra no vídeo não está "
                        "aqui; o perigo real está distante.",
        ),
        psico_titulo="Medo Biológico e Exposição em Degraus (Magalhães Coelho)",
        psico_texto="Medos de cobras e aranhas têm componente evolutivo — o cérebro aprendeu a "
                    "reagir rápido. Mas fobia é quando a resposta defensiva dispara sem perigo "
                    "proporcional. Magalhães Coelho descreve a habituação: repetir encontros "
                    "seguros até o corpo parar de entrar em pânico. Evitar só alimenta a besta.",
        gancho_final="O próximo medo de Harry latia alto, tinha três cabeças e guardava um segredo "
                     "atrás da porta que Ron jurava não abrir.",
    ),

    dict(
        num=3, fobia="Cinofobia",
        titulo="Três Cabeças e Um Coração Acelerado",
        gancho_abertura="Diziam que, atrás da porta no terceiro andar, algo enorme roncava — e "
                        "Harry precisava passar por ali para salvar o que mais importava.",
        img="hp_three_headed_dog",
        inicio=[
            "Fluffy, o cachorro de três cabeças, guardava a passagem para a Pedra Filosofal. "
            "Harry tinha pavor de cães desde pequeno: um latido na rua, uma corrida na infância, "
            "a sensação de dentes perto demais.",
            "— Cinofobia — explicou Hermione. — Medo de cães. Muitas vezes começa com um susto "
            "que o corpo nunca esqueceu.",
        ],
        meio=[
            "Ron tremia também. O Devorador sussurrou para os dois: <i>“Voltem. Ninguém precisa "
            "disso.”</i> Mas Harry lembrava do relato de Magalhães Coelho: primeiro o corpo "
            "congela, depois vem o medo, depois a vontade de fugir.",
            "Hermione trouxe uma flauta. — Música acalma o cão. Nós não vamos lutar — vamos "
            "planejar. Determinação não é barulho; é estratégia.",
            "Harry tocou a flauta com mãos trêmulas. As três cabeças foram adormecendo, uma "
            "por uma. O coração dele ainda disparava — mas os pés não correram.",
        ],
        fala_vilao="Ele vai te morder. Cães sempre mordem.",
        fim=[
            "Passaram por Fluffy devagar, sem correr, sem gritar. Do outro lado, Harry encostou "
            "na parede e chorou de alívio — e de orgulho.",
            "— Eu tinha medo — disse. — E mesmo assim fui. Como quando enfrentei Quirrell. "
            "Como quando enfrento qualquer coisa.",
            "Hermione sorriu: — Isso se chama mestria. Quando você pratica, o medo não some "
            "de uma vez — mas deixa de mandar.",
        ],
        magia=dict(
            nome="Fidelis Amicus",
            feitiço="Fidelis Amicus!",
            gesto="Mão aberta, palma para fora, voz baixa e constante.",
            significado="Lembra o cérebro de que não todo cão é o mesmo cão do susto. Separa "
                        "memória antiga de momento presente.",
        ),
        psico_titulo="Memória do Susto e Generalização (Coelho)",
        psico_texto="Um episódio com cão agressivo pode generalizar para todos os cães. O corpo "
                    "grava cheiro, latido, velocidade. A terapia reescreve essa memória com "
                    "experiências novas e seguras — distância, controle, repetição. Como Harry "
                    "aprendeu: o cão da história não é todo cão do mundo.",
        gancho_final="Mais tarde, no topo da torre mais alta de Hogwarts, Harry olharia para baixo "
                     "e sentiria o chão sumir debaixo dos pés — mesmo estando firmemente em pé.",
    ),

    dict(
        num=4, fobia="Acrofobia",
        titulo="O Topo da Torre e o Chão que Sumiu",
        gancho_abertura="Da torre de astronomia, as estrelas pareciam ao alcance da mão — mas "
                        "para Harry, o abismo abaixo era mais real do que o céu.",
        img="hp_tower_moon",
        inicio=[
            "Harry subiu os degraus da torre para devolver um telescópio a um colega. Na última "
            "escada, a visão da quadra minúscula lá embaixo fez as pernas virarem gelo.",
            "— Acrofobia — disse Hermione, que tinha subido atrás dele. — Medo de altura. O "
            "corpo perde referência postural e o alarme dispara.",
        ],
        meio=[
            "Harry agachou, agarrado ao corrimão. O Devorador rugiu: <i>“Você vai cair. Sempre "
            "vai cair.”</i>",
            "Hermione citou Magalhães Coelho: medo de altura envolve postura e sensação de "
            "instabilidade — não só “pensamento errado”. Por isso a magia combina corpo e mente.",
            "Ela ensinou: olhar para um ponto fixo à frente, não para baixo; sentir os pés "
            "apertando o chão; contar quatro tempos na respiração.",
        ],
        fala_vilao="Não levante. Se levantar, morre.",
        fim=[
            "Harry ficou agachado até o pico da ansiedade baixar de oito para cinco. Aí levantou "
            "só até a altura do joelho. No dia seguinte, até a cintura. Na terceira visita, "
            "entregou o telescópio sem desmaiar.",
            "— Determinação — disse ele, olhando a cicatriz no reflexo do vidro — é subir um "
            "degrau por dia, não a torre inteira de uma vez.",
        ],
        magia=dict(
            nome="Altum Firmum",
            feitiço="Altum Firmum!",
            gesto="Pés bem abertos, pressione o chão, diga em voz firme: “O chão me segura.”",
            significado="Reconecta o corpo à superfície real. A altura existe; o perigo imaginado "
                        "encolhe quando os pés voltam a sentir apoio.",
        ),
        psico_titulo="Postura, Altura e Alarme Corporal",
        psico_texto="Em acrofobia, o sistema postural interpreta altura como queda iminente. "
                    "Exposição gradual em alturas protegidas, com repetição, recalibra o "
                    "equilíbrio entre perigo real e resposta defensiva — conceito central no "
                    "trabalho de Magalhães Coelho sobre medo de alturas.",
        gancho_final="Mas nem todo medo acontece no alto — alguns apertam por todos os lados, "
                     "como as paredes de um corredor sem janela.",
    ),

    dict(
        num=5, fobia="Claustrofobia",
        titulo="O Armário, o Elevador e a Porta que Não Abria",
        gancho_abertura="Harry conhecia lugares apertados melhor do que ninguém — afinal, tinha "
                        "morado num armário. Mas conhecer não significava gostar.",
        img="hp_dungeon_tight",
        inicio=[
            "O grupo precisava descer num elevador mágico estreito para chegar às aulas de Poções. "
            "As portas fecharam com um clique. Harry sentiu o ar sumir.",
            "— Claustrofobia — murmurou Hermione, segurando a mão dele. — Medo de espaços "
            "fechados. Elevador, túnel, ressonância magnética, avião.",
        ],
        meio=[
            "O Devorador sussurrou: <i>“Você vai ficar preso para sempre, como na Rua dos "
            "Alfeneiros.”</i> Harry bateu no botão de emergência com o joelho tremendo.",
            "Hermione lembrou Freud: a angústia sem objeto pode se colar a lugares onde a pessoa "
            "se sentiu sem saída. O armário da infância virava elevador na imaginação.",
            "— Conte comigo — disse ela. — Trinta segundos. Só trinta. Respira comigo.",
        ],
        fala_vilao="As paredes vão te esmagar. Não há saída.",
        fim=[
            "Harry contou até trinta. O elevador parou. As portas abriram. Ele saiu cambaleando "
            "— mas saiu.",
            "Na semana seguinte, entrou de novo voluntariamente por vinte segundos. Depois quarenta. "
            "O armário debaixo da escada ficou pequeno na memória, não no poder.",
            "— Eu determinei — disse Harry — que nenhum espaço fechado ia decidir minha vida.",
        ],
        magia=dict(
            nome="Aer Liberum",
            feitiço="Aer Liberum!",
            gesto="Inspire pelo nariz contando 4, segure 2, solte pela boca contando 6.",
            significado="Convence o corpo de que há ar e saída. A claustrofobia mente sobre "
                        "o tempo; a respiração devolve o relógio.",
        ),
        psico_titulo="Fobias Situacionais e Memória do Enclausuramento",
        psico_texto="Claustrofobia pertence às fobias situacionais do DSM-5. Experiências de "
                    "aprisionamento simbólico ou real alimentam o medo. A exposição interoceptiva "
                    "e situacional, em doses curtas e repetidas, ensina que a ansiedade sobe e "
                    "desce sem catástrofe.",
        gancho_final="Quando as portas se abriram para o céu aberto, Harry pensou que nada poderia "
                     "ser pior — até ver o voo de uma vassoura esperando por ele.",
    ),

    dict(
        num=6, fobia="Aerofobia",
        titulo="Vassoura, Nuvens e Coração na Garganta",
        gancho_abertura="Todo aluno de Hogwarts sonhava em voar. Harry sonhava em não cair.",
        img="hp_broom_sky",
        inicio=[
            "Na primeira aula de voo, Madam Hooch ordenou: “Mãos na vassoura!” Harry sentiu o "
            "estômago subir antes da vassoura. Não era só altura — era perder o chão, confiar "
            "no ar, depender de um pedaço de madeira.",
            "— Aerofobia — disse Hermione depois, na biblioteca. — Medo de voar. Mesmo sabendo "
            "que aviões e vassouras são seguros, o corpo não escuta o manual.",
        ],
        meio=[
            "O Devorador listou acidentes imaginários. Harry quis pedir dispensa médica.",
            "Hermione comparou com o Pequeno Hans: o medo parece irracional, mas tem lógica "
            "emocional — perder controle, depender de outros, não poder descer.",
            "Plano: sentar na vassoura sem decolar. No dia seguinte, hover de um palmo. Depois "
            "um metro. Harry assistiu outros alunos antes de tentar.",
        ],
        fala_vilao="Você vai despencar. O céu não perdoa.",
        fim=[
            "No terceiro dia, Harry flutuou até a altura dos ombros de Hermione. As mãos "
            "tremiam, mas ele segurou a vassoura.",
            "— Eu voei — disse, quase sem acreditar. — Pouco. Com medo. Mas voei.",
            "Madam Hooch assentiu: — Potter, coragem não é ausência de medo. É disciplina com "
            "o coração acelerado.",
        ],
        magia=dict(
            nome="Nubes Custodiant",
            feitiço="Nubes Custodiant!",
            gesto="Olhe para o horizonte, não para o vazio abaixo; diga: “As nuvens me carregam.”",
            significado="Troca a imagem mental de queda pela imagem de sustentação. O voo seguro "
                        "começa na imaginação treinada.",
        ),
        psico_titulo="Perda de Controle e Exposição Imaginativa",
        psico_texto="Aerofobia mistura altura, confinamento e falta de controle. A TCC combina "
                    "psicoeducação, relaxamento e exposição gradual — às vezes começando no "
                    "simulador ou na imaginação, como Harry no chão antes do ar.",
        gancho_final="De volta à terra, Harry enfrentaria algo que deixava muita gente pálida "
                     "sem precisar subir um centímetro.",
    ),

    dict(
        num=7, fobia="Hematofobia",
        titulo="A Poção Vermelha e o Chão que Rodou",
        gancho_abertura="Na aula de Poções, uma gota de corante vermelho caiu na bancada — e "
                        "o mundo de Harry inclinou de lado.",
        img="hp_hospital_needle",
        inicio=[
            "Harry viu o vermelho e lembrou do corte no joelho na infância, do cheiro de ferro, "
            "da visão turva. As pernas falharam.",
            "— Hematofobia — explicou Madam Pomfrey na enfermaria. — Medo de sangue e ferimentos. "
            "Pode vir com queda de pressão e desmaio — resposta vasovagal.",
        ],
        meio=[
            "O Devorador zombou: <i>“Você desmaia, Potter. Fraco.”</i>",
            "Hermione trouxe um livro de Magalhães Coelho: fobias de sangue-injeção-ferimentos "
            "são diferentes — o corpo pode baixar a pressão em vez de só acelerar o coração.",
            "Plano especial: deitar ao treinar; tensionar pernas e braços antes de ver imagens; "
            "subir devagar da posição horizontal.",
        ],
        fala_vilao="Sangue significa morte. Você não aguenta ver.",
        fim=[
            "Harry olhou fotos de gotas em cartão, deitado no sofá da sala comunal, pernas "
            "tensionadas. Depois um vídeo de cinco segundos. Não desmaiou.",
            "— Determinação também é conhecer o próprio corpo — disse. — E respeitar o ritmo.",
        ],
        magia=dict(
            nome="Vita Fluit",
            feitiço="Vita Fluit!",
            gesto="Deitado ou sentado, tensione músculos por 15 segundos, solte devagar.",
            significado="Mantém a pressão estável enquanto o olho aprende que ver sangue em "
                        "imagem não é estar ferido.",
        ),
        psico_titulo="Fobia Sangue-Injeção-Ferimentos e Resposta Vasovagal",
        psico_texto="No DSM-5, fobias BIF incluem sangue, injeção e ferimento. A resposta "
                    "vasovagal explica o desmaio. A exposição usa técnica aplicada de tensão "
                    "para evitar queda de pressão — como treinar um feitiço com gesto correto.",
        gancho_final="Na enfermaria, no dia seguinte, uma agulha reluzente esperava por ele — "
                     "e o medo era outro, ainda mais pontiagudo.",
    ),

    dict(
        num=8, fobia="Tripanofobia",
        titulo="A Agulha e o Coragem de um Segundo",
        gancho_abertura="Uma vacina mágica contra o resfriado do castelo deveria levar um segundo. "
                        "Para Harry, parecia uma eternidade.",
        img="hp_hospital_needle",
        inicio=[
            "Harry evitava a enfermaria há meses. Agulhas significavam dor, perda de controle, "
            "memória de hospital na infância muggle.",
            "— Tripanofobia — disse Hermione. — Medo de agulhas e injeções. Atrapalha vacinas "
            "e exames — mas tem tratamento.",
        ],
        meio=[
            "O Devorador sussurrou catástrofes médicas. Harry suou frio só de ver o algodão.",
            "Hermione propôs escada: algodão na pele → álcool no braço → agulha sem líquido "
            "encostando → vacina de verdade.",
            "Freud diria que o medo ganhou objeto claro — a agulha — para dar forma à angústia "
            "mais antiga de ser vulnerável.",
        ],
        fala_vilao="Vai doer horrores. Você não aguenta.",
        fim=[
            "Harry encostou a agulha fria no braço sem perfurar. Respirou. No dia seguinte, "
            "recebeu a vacina olhando para um adesivo de estrela que Hermione colou na blusa "
            "dele como ponto focal.",
            "— Um segundo — disse Madam Pomfrey. — Você aguentou a vida inteira até aqui.",
            "Harry riu nervoso e não desmaiou.",
        ],
        magia=dict(
            nome="Dolorem Brevis",
            feitiço="Dolorem Brevis!",
            gesto="Antes da agulha, conte até três; na perfuração, solte o ar devagar.",
            significado="O cérebro exagera a duração da dor. Contar e soltar o ar encurta a "
                        "experiência real.",
        ),
        psico_titulo="Dor Anticipada × Dor Real",
        psico_texto="A tripanofobia alimenta-se da antecipação. Exposição gradual e informação "
                    "correta reduzem a catastrofização. Como Harry: um degrau por vez, sempre "
                    "com plano de saída seguro — isso não é fuga, é estratégia.",
        gancho_final="Naquela noite, um trovão rasgou o céu sobre Hogwarts — e Harry sentiu o "
                     "medo antigo correr pelos corredores mais rápido que qualquer fantasma.",
    ),

    dict(
        num=9, fobia="Astrafobia",
        titulo="Quando o Céu Grita",
        gancho_abertura="CABUM! O trovão fez as janelas tremer e Harry se enfiou debaixo da "
                        "cama como quando tinha cinco anos.",
        img="hp_storm_window",
        inicio=[
            "Tempestades em Hogwarts eram espetaculares e assustadoras. Raios desenhavam "
            "veias douradas no céu. Harry cobria os ouvidos.",
            "— Astrafobia — disse Hermione, sentando no chão ao lado da cama. — Medo de trovões "
            "e tempestades. Muito comum em crianças — e em heróis cansados.",
        ],
        meio=[
            "O Devorador repetia cada estrondo como prova de perigo.",
            "Hermione lembrou: primeiro a resposta defensiva (pulo, coração), depois o medo "
            "interpretado. Harry podia treinar a segunda parte.",
            "Elas ouviram a tempestade juntas com chocolate quente — sem exigir que Harry "
            "ficasse na janela. Só que ficasse na sala, não debaixo da cama.",
        ],
        fala_vilao="O próximo raio vai acertar você. O céu está com raiva.",
        fim=[
            "No terceiro temporal, Harry ficou na cadeira ao lado da janela, coberto com um "
            "casaco, contando os segundos entre raio e trovão para saber a distância.",
            "— Está longe — disse. — Estou com medo. Mas estou aqui.",
            "O Devorador encolheu no canto, menor que a cicatriz na testa de Harry.",
        ],
        magia=dict(
            nome="Tonitru Protego",
            feitiço="Tonitru Protego!",
            gesto="Mãos nos ouvidos suavemente, depois abra; diga: “O castelo me protege.”",
            significado="Cria barreira simbólica entre estímulo e pânico. O trovão é barulho; "
                        "não é sentença.",
        ),
        psico_titulo="Medo de Estímulos Súbitos e Barulho",
        psico_texto="Astrafobia envolve saliência do estímulo — barulho imprevisível. A "
                    "habituação gradual a sons gravados e à presença segura durante temporais "
                    "reconecta o corpo ao presente. Evitar temporais inteiros mantém o medo.",
        gancho_final="Quando a tempestade passou, a escuridão ficou — e era nela que o medo de "
                     "Harry mais gostava de esconder-se.",
    ),

    dict(
        num=10, fobia="Nictofobia",
        titulo="A Noite sem Vela",
        gancho_abertura="Apagaram as velas do dormitório por um exercício de coragem — e Harry "
                        "sentiu o armário da infância voltar a respirar ao lado da cama.",
        img="hp_closet_dark",
        inicio=[
            "No escuro, cada rangido virava monstro. Harry acendia a varinha no meio da noite "
            "só para confirmar que não havia nada.",
            "— Nictofobia — murmurou Hermione. — Medo do escuro. Crianças e adultos. O escuro "
            "esconde o desconhecido — e o cérebro odeia desconhecido.",
        ],
        meio=[
            "O Devorador amava a noite: <i>“Aqui sou eu quem manda.”</i>",
            "Hermione citou Freud: angústia sem forma vira medo de algo — sombras, armários, "
            "corredores. Dar forma permite combater.",
            "Plano: luz baixa → penumbra → escuro com varinha na mão → escuro com Lumos "
            "Interior no peito, não na varinha.",
        ],
        fala_vilao="No escuro ninguém te acha. Fique pequenininho.",
        fim=[
            "Na quinta noite do treino, Harry dormiu dez minutos no escuro total antes de "
            "acordar e rir de si mesmo.",
            "— Ainda assustei — disse. — Mas dormi. Isso é vitória.",
            "A cicatriz na testa brilhou na escuridão como uma pequena estrela.",
        ],
        magia=dict(
            nome="Lumos Noctis",
            feitiço="Lumos Noctis!",
            gesto="Feche os olhos, imagine uma vela no peito, abra devagar.",
            significado="A luz que importa pode ser interna. O escuro deixa de ser armário "
                        "quando você carrega sua própria chama.",
        ),
        psico_titulo="Medo do Desconhecido e Angústia sem Objeto",
        psico_texto="Freud distingue angústia (sem objeto claro) de medo (com objeto). A "
                    "nictofobia fixa o medo no escuro. Exposição gradual à penumbra, com "
                    "previsibilidade e segurança, ensina que a ausência de luz não é ausência "
                    "de controle.",
        gancho_final="Na manhã seguinte, uma carta da clínica odontológica de Hogsmeade "
                     "esperava Harry na mesa do café — e ele engoliu seco.",
    ),

    dict(
        num=11, fobia="Odontofobia",
        titulo="A Cadeira que Parecia um Trono de Medo",
        gancho_abertura="Todo mundo ia ao dentista mágico para encantar os dentes. Harry ia "
                        "tremendo, como se fosse enfrentar um dragão sem varinha.",
        img="hp_hospital_needle",
        inicio=[
            "O consultório cheirava a menta e metal. A cadeira reclinava. Harry sentiu "
            "vulnerabilidade total — boca aberta, alguém com instrumentos perto do rosto.",
            "— Odontofobia — disse Hermione na sala de espera. — Medo do dentista. Muitas "
            "vezes é medo de dor, mas também de perder controle e de postura submissa.",
        ],
        meio=[
            "O Devorador sussurrou vergonha: <i>“Adulto com medo de dentista.”</i>",
            "Magalhães Coelho descreve medos ligados a postura e vulnerabilidade — deitar, "
            "abrir a boca, confiar em outro.",
            "O dentista, gentil, combinou sinal de mão para pausar. Harry entrou só para "
            "conhecer a sala. Na segunda visita, sentou na cadeira sem reclinar.",
        ],
        fala_vilao="Vai doer. Sempre dói. Você vai gritar.",
        fim=[
            "Na quarta visita, reclinou dez graus, depois trinta. Na quinta, limpeza simples "
            "com pausas.",
            "— Eu determinei o ritmo — disse Harry ao espelho. — Não o medo.",
            "Hermione bateu palmas na recepção. O Devorador ficou do tamanho de um bicho-de-pé.",
        ],
        magia=dict(
            nome="Curatio Dulcis",
            feitiço="Curatio Dulcis!",
            gesto="Mão no coração, depois sinal combinado com o profissional se precisar parar.",
            significado="Transforma a cadeira em parceria, não tortura. Você tem voz, mesmo "
                        "de boca aberta.",
        ),
        psico_titulo="Vulnerabilidade, Postura e Controle Compartilhado",
        psico_texto="Odontofobia mistura medo de dor e de submissão. Exposição com controle "
                    "retornado ao paciente (pausas, informação, degraus) quebra a catastrofização. "
                    "Determinação aqui é negociar — como Harry negociou com cada professor.",
        gancho_final="No fim da semana, o passeio até o Lago Negro faria o chão de Harry balançar "
                     "como navio em tempestade.",
    ),

    dict(
        num=12, fobia="Talassofobia",
        titulo="O Lago Negro e o Abraço Gelado",
        gancho_abertura="O Lago Negro era bonito de longe — e terrível de perto, como se a "
                        "profundidade puxasse Harry para baixo só de olhar.",
        img="hp_lake_cold",
        inicio=[
            "Na margem, Harry viu ondas escuras e imaginou o que havia embaixo. Grindylows, "
            "sereias, o desconhecido.",
            "— Talassofobia — disse Hermione. — Medo de água profunda, de afogamento, de não "
            "ver o fundo.",
        ],
        meio=[
            "O Devorador pintou imagens de afogamento. Harry recuou da beira.",
            "Hermione lembrou o Triwizard Tournament: Harry mergulhou antes — com magia e "
            "preparo. Medo não apaga história de coragem; só tenta apagar.",
            "Plano: sentar na margem → molhar os pés → caminhar até o joelho com corda na "
            "cintura e Ron segurando.",
        ],
        fala_vilao="A água vai te engolir. Profundo é morte.",
        fim=[
            "Harry entrou até o joelho, sentiu o frio, respirou Serpens Quieta adaptado para "
            "água — pés firmes na areia.",
            "— Não nadei — disse. — Mas entrei. E amanhã entro de novo.",
            "O lago continuou escuro. Harry continuou maior que o medo.",
        ],
        magia=dict(
            nome="Aqua Amica",
            feitiço="Aqua Amica!",
            gesto="Molhe as mãos, esfregue suavemente, diga: “A água me toca; não me leva.”",
            significado="Separa toque da imaginação de afogamento. Profundidade se enfrenta "
                        "em degraus, não de um salto.",
        ),
        psico_titulo="Medo de Ambiente Natural (Água)",
        psico_texto="Talassofobia entra nas fobias de ambiente natural. O medo mistura "
                    "profundidade, escuridão e perda de suporte. Exposição com segurança "
                    "física (corda, companhia, margem) permite habituação sem retraumatizar.",
        gancho_final="Mais tarde, no Salão Principal, mil olhos se voltariam para Harry — e "
                     "nenhum deles seria mais assustador que o próprio julgamento dele.",
    ),

    dict(
        num=13, fobia="Glossofobia",
        titulo="Mil Olhos no Salão Principal",
        gancho_abertura="O professor anunciou: cada aluno falaria sobre um feitiço na frente de "
                        "toda Hogwarts. Harry sentiu o café da manhã subir.",
        img="hp_great_hall_crowd",
        inicio=[
            "Glossofobia — medo de falar em público — não era exclusividade de Harry, mas "
            "parecia. O coração batia na garganta. As mãos suavam.",
            "Hermione, curiosamente, também tremia. Até a sabe-tudo tinha medo de errar na "
            "frente dos outros.",
        ],
        meio=[
            "O Devorador sussurrou: <i>“Vão rir da cicatriz. Vão rir do menino do armário.”</i>",
            "Freud diria que o medo do olhar do outro mistura vergonha e desejo de aprovação. "
            "Magalhães Coelho acrescenta: evitar falar alimenta a fobia social.",
            "Treino: falar para o espelho → para Hermione → para Ron e Hermione → para a "
            "torre vazia → para a turma pequena.",
        ],
        fala_vilao="Você vai gaguejar. Vai passar vergonha. Melhor ficar invisível.",
        fim=[
            "No dia da apresentação, Harry entrou com notas na mão, olhou para Hermione na "
            "primeira fila, e começou.",
            "A voz tremeu no meio — mas continuou. No final, não era o discurso perfeito. "
            "Era honesto.",
            "Aplausos. Harry sorriu: — Determinação é falar com o coração acelerado.",
        ],
        magia=dict(
            nome="Verbum Fortis",
            feitiço="Verbum Fortis!",
            gesto="Pés firmes, olhar em um amigo, primeira frase decorada devagar.",
            significado="A palavra forte não é sem medo — é dita mesmo assim. Um ouvinte "
                        "amigo basta para ancorar.",
        ),
        psico_titulo="Medo do Julgamento e Fobia Social",
        psico_texto="Glossofobia é forma específica de medo de avaliação negativa. A TCC "
                    "usa exposição a situações sociais temidas, ensaio e reestruturação de "
                    "pensamentos catastróficos. Como Harry: a plateia não é um monstro — "
                    "são pessoas que também tremem.",
        gancho_final="Depois de falar para mil, Harry achou que podia qualquer coisa — até "
                     "precisar sair sozinho pela vila cheia de ruas sem saída aparente.",
    ),

    dict(
        num=14, fobia="Agorafobia",
        titulo="A Vila que Parecia um Labirinto",
        gancho_abertura="Em Hogsmeade, as ruas iam de todos os lados — bonitas, movimentadas, "
                        "e para Harry, de repente, sem saída.",
        img="hp_hogsmeade_date",
        inicio=[
            "Multidão, becos, lojas cheias. Harry sentiu falta de ar — não de altura, não de "
            "animal: era medo de não conseguir escapar se algo der errado.",
            "— Agorafobia — disse Hermione, guiando-o para um banco. — Medo de situações onde "
            "achamos difícil sair ou pedir ajuda. Não é só “medo de rua”.",
        ],
        meio=[
            "O Devorador repetia: <i>“Fique no castelo. Lá você controla.”</i> Evitar virava prisão dourada.",
            "Hermione explicou o ciclo de Coelho: medo → evitação → alívio → medo maior amanhã.",
            "Plano: caminhar até a primeira loja com ela → esperar cinco minutos → voltar → "
            "no dia seguinte, duas lojas → depois, cinco minutos sozinho no beco perto da escola.",
        ],
        fala_vilao="Se você sair, vai entrar em pânico e ninguém vai te salvar.",
        fim=[
            "Harry ficou cinco minutos sozinho no beco ensolarado, costas no muro, respirando "
            "Aer Liberum. Nada aconteceu de ruim.",
            "— O mundo é grande — disse. — Mas eu também cresci.",
            "O Devorador, pela primeira vez, parecia com fome.",
        ],
        magia=dict(
            nome="Via Aperta",
            feitiço="Via Aperta!",
            gesto="Identifique uma saída antes de entrar; aponte mentalmente: “Se precisar, vou por ali.”",
            significado="Devolve o mapa ao cérebro. Agorafobia rouba a sensação de rota; "
                        "planejar a saída segura é coragem prática.",
        ),
        psico_titulo="Medo de Não Escapar e Evitamento que Prende",
        psico_texto="Agorafobia envolve medo de sintomas de pânico em lugares onde escapar "
                    "parece difícil. O tratamento combina exposição gradual a contextos temidos "
                    "e redução de comportamentos de segurança. Determinação é sair com plano — "
                    "não sem medo.",
        gancho_final="Com quase todas as magias aprendidas, faltava apenas uma coisa: Harry "
                     "precisava encarar o Devorador de Coragem face a face — no espelho.",
    ),

    dict(
        num=15, fobia="Epílogo",
        titulo="O Espelho, o Abraço e o Final Feliz",
        gancho_abertura="No Espelho de Ojesed, Harry não viu ouro nem família perdida — viu "
                        "a si mesmo de costas, encarando o Devorador sem fugir.",
        img="hp_mirror_erised",
        inicio=[
            "Todas as fobias tinham nome. Todas tinham magia. Harry tinha uma lista no diário: "
            "aranha, cobra, cão, altura, espaço fechado, voo, sangue, agulha, trovão, escuro, "
            "dentista, água profunda, plateia, rua sem saída.",
            "Não estava “curado” — às vezes ainda tremia. Mas tinha deixado de organizar a vida "
            "só para fugir.",
        ],
        meio=[
            "Hermione encontrou Harry na frente do espelho. — O Devorador é alimentado por "
            "evitação — disse. — Freud viu que o medo pode mudar de forma; Magalhães Coelho "
            "viu que evitar alimenta a besta. Você escolheu enfrentar. Isso é determinação de "
            "verdade.",
            "O Devorador sussurrou fraco: <i>“Ainda posso voltar…”</i>",
            "Harry respondeu em voz alta: — Pode. Mas eu também volto. Com magia. Com passos. "
            "Com amigos.",
        ],
        fala_vilao="Você nunca vai ser de verdade sem medo…",
        fim=[
            "Harry virou-se do espelho, abraçou Hermione (que corou e abraçou de volta), e "
            "sentiu o coração acelerado — não de pânico, de alegria.",
            "Anos depois, contariam que Harry Potter venceu trolls, basiliscos e bruxos das "
            "trevas. Mas ele sabia o segredo: tinha vencido, degrau a degrau, o medo de viver.",
            "E viveram felizes, com coragem ensaiada todo dia — porque determinação, como "
            "qualquer magia, precisa de prática.",
            "<b>FIM.</b>",
        ],
        magia=dict(
            nome="Coragem Perpetua",
            feitiço="Coragem Perpetua!",
            gesto="Mão no peito, mão na cicatriz, sorriso pequeno: “Um passo hoje.”",
            significado="A magia final não elimina o medo — ensina a dançar com ele. "
                        "Repita sempre que precisar.",
        ),
        psico_titulo="Determinação, Habituação e Vida Plena",
        psico_texto="Superar fobias é recalibrar o alarme interno com experiências repetidas "
                    "de segurança. Freud nos ensina a escutar o simbólico do medo; Magalhães "
                    "Coelho nos lembra que evitar alimenta a ansiedade. Harry mostra que "
                    "determinação é prática — uma fobia, uma magia, um capítulo de cada vez.",
        gancho_final=None,
    ),
]


def build():
    s = styles()
    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2.0 * cm,
        title="Harry Potter e as Magias da Coragem",
        author="Dra. Priscila Palomo",
    )
    story = []

    story.append(Spacer(1, 0.5 * cm))
    p(story, "DRA. PRISCILA PALOMO  ·  CRP 98007", s["cover_brand"])
    story.append(Spacer(1, 0.2 * cm))
    story.append(HRFlowable(width="40%", thickness=2, color=NAVY, spaceBefore=0, spaceAfter=8))
    p(story, "Harry Potter e as Magias da Coragem", s["cover_title"])
    p(story, "Nossa historinha original — usando a jornada de Harry Potter<br/>"
             "para ilustrar cada fobia e como vencê-la", s["cover_sub"])
    story.append(Spacer(1, 0.3 * cm))
    story.append(ilustra("hp_cover", 13 * cm))
    story.append(Spacer(1, 0.25 * cm))
    p(story, "“Determinação não é não sentir medo.<br/>"
             "É aprender a magia certa para cada medo — e usar.”", s["gancho_abertura"])
    story.append(Spacer(1, 0.2 * cm))
    p(story, "www.priscilapalomo.com", s["cover_brand"])
    story.append(PageBreak())

    p(story, "Carta aos Leitores Corajosos", s["h1"])
    story.append(hr())
    p(story, "Querido(a) leitor(a),", s["prosa_first"])
    p(story, "Este <b>não é um resumo dos livros de Harry Potter</b>. É uma "
      "<b>narrativa original</b> da Dra. Priscila Palomo — escrita para ser fácil "
      "de entender, organizada por tipo de fobia, com psicoeducação sobre como o medo "
      "funciona e como superá-lo.",
      s["prosa"])
    p(story, "Usamos a história mundialmente conhecida do bruxinho de óculos e cicatriz "
      "de raio como <b>enredo ilustrativo</b>: milhões de pessoas já sabem quem é Harry, "
      "e isso ajuda a lembrar que até quem parece herói sente medo — e aprende a vencer, "
      "passo a passo, com determinação.",
      s["prosa"])
    p(story, "Cada capítulo traz <b>começo, meio e fim de superação</b>, uma <b>magia</b> "
      "para treinar no dia a dia e a caixinha <b>O Segredo da Mente</b>, com ideias de "
      "Freud (caso Pequeno Hans, angústia e medo), de Magalhães Coelho "
      "(<i>Medos, Fobias e Ansiedades</i>: resposta defensiva, evitamento, habituação) "
      "e da TCC com exposição gradual.",
      s["prosa"])
    p(story, "<b>Nota:</b> material psicoeducativo. Não substitui psicoterapia. "
      "Se o medo for muito intenso ou estiver atrapalhando sua vida, procure ajuda "
      "profissional.",
      s["small"])
    story.append(Spacer(1, 4))
    p(story, "Com carinho,<br/><b>Dra. Priscila Palomo</b> — CRP 98007<br/>"
             "Especialista em Fobias e TCC · www.priscilapalomo.com", s["small"])
    story.append(PageBreak())

    p(story, "Índice — Uma Magia para Cada Medo", s["h1"])
    story.append(hr())
    for c in CAPITULOS:
        magia = c["magia"]["nome"]
        p(story, f"<b>Cap. {c['num']:02d}:</b> {c['fobia']} — <i>{c['titulo']}</i> "
             f"· magia: <font color='#C8940A'>{magia}</font>", s["toc"])
    story.append(PageBreak())

    for c in CAPITULOS:
        capitulo(story, c, s)

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"OK: {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
