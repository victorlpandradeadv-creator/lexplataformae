"""Ilustrações interativas em SVG, com uma geometria só para os dois temas.

Feito em 16/11/2026, por orientação do autor, para substituir a produção das peças restantes em
raster. Cada composição é desenhada uma vez, em peças nomeadas. Cada peça carrega a frase da
superfície que a explica e o trecho literal da tese que ancora essa frase, com a página.

Saídas, por composição, em estrutura/rascunhos/ilustracoes-svg/.
    <id>.svg            mestre semântico, com as cores das variáveis do site (herda modo e tema
                        quando embutido na página)
    <id>.html           fragmento pronto para o gerador do site, com a figura, os marcadores e as
                        caixas empilhadas que o modo desnudo revela
    <id>.webp           entrega compatível, paleta clara, fundo transparente
    <id>-escuro.webp    entrega compatível, paleta escura, mesma geometria
    prova.html          prancha de revisão com as seis combinações de modo e tema

Nenhuma frase nasce aqui. A frase leiga vem de conteudo/camada-externa.md ou de
conteudo/percurso.md, e o trecho da tese é literal, conferido por ferramentas/conferir_citacoes.py.

Uso.
    python3 ferramentas/ilustracoes.py            gera todas
    python3 ferramentas/ilustracoes.py <id>       gera só a composição <id>
"""
import json
import math
import subprocess
import sys
import tempfile
from html import escape
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "estrutura" / "rascunhos" / "ilustracoes-svg"

# Papéis de cor. No site, as variáveis do modo e do tema. Na exportação, a paleta do planejamento (seção 4).
PAPEIS = {
    "t1": ("--tinta", "#211c17", "#ebe7e1"),      # contorno principal
    "t2": ("--tinta-2", "#615953", "#a9a49c"),    # traço secundário, controles da plataforma
    "az": ("--il-azul", "#002fa7", "#497ef7"),    # objeto e posição do leitor
    "ap": ("--il-apoio", "#f1ebe1", "#241f1a"),   # pequena superfície de apoio
}
TRACO = {"t1": 12, "t2": 9, "az": 12}


# ---------------------------------------------------------------- primitivas

def linha(pts, papel="t1", tracejado=False, larg=None, fechado=False):
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + (" Z" if fechado else "")
    return caminho(d, papel, tracejado, larg)


def caminho(d, papel="t1", tracejado=False, larg=None, preenche=None):
    w = larg or TRACO.get(papel, 12)
    tr = f' stroke-dasharray="{w * 1.6:.0f} {w * 1.9:.0f}"' if tracejado else ""
    cls = f"s-{papel} f-{preenche}" if preenche else f"s-{papel}"
    f = "" if preenche else ' fill="none"'
    return f'<path d="{d}" class="{cls}"{f} stroke-width="{w}"{tr}/>'


def bloco(x, y, w, h, papel="az", r=4):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" class="f-{papel}"/>'


def caixa(x, y, w, h, papel="t1", r=6, larg=None, tracejado=False):
    lw = larg or TRACO.get(papel, 12)
    tr = f' stroke-dasharray="{lw * 1.6:.0f} {lw * 1.9:.0f}"' if tracejado else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="none" class="s-{papel}" stroke-width="{lw}"{tr}/>'


def circulo(cx, cy, r, papel="t1", cheio=False, larg=None):
    if cheio:
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" class="f-{papel}"/>'
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" class="s-{papel}" stroke-width="{larg or TRACO.get(papel, 12)}"/>'


def balao(x, y, w, h, cauda="esq", papel="t1"):
    """Balão de conversa em contorno, a mesma forma do Laboratório aprovado."""
    r = 10
    if cauda == "esq":
        cx = x + 40
        pts = f"M{x + r} {y} H{x + w - r} Q{x + w} {y} {x + w} {y + r} V{y + h - r} Q{x + w} {y + h} {x + w - r} {y + h} H{cx + 34} L{cx} {y + h + 40} V{y + h} H{x + r} Q{x} {y + h} {x} {y + h - r} V{y + r} Q{x} {y} {x + r} {y} Z"
    else:
        cx = x + w - 40
        pts = f"M{x + r} {y} H{x + w - r} Q{x + w} {y} {x + w} {y + r} V{y + h - r} Q{x + w} {y + h} {x + w - r} {y + h} H{cx} V{y + h + 40} L{cx - 34} {y + h} H{x + r} Q{x} {y + h} {x} {y + h - r} V{y + r} Q{x} {y} {x + r} {y} Z"
    return caminho(pts, papel)


def comando(cx, cy, r=46, ang=-40):
    """Comando externo da plataforma. Um botão giratório neutro, com a marca de posição."""
    a = math.radians(ang)
    return (circulo(cx, cy, r, "t2") +
            linha([(cx, cy), (cx + (r - 6) * math.cos(a), cy + (r - 6) * math.sin(a))], "t2") +
            circulo(cx, cy, 7, "t2", cheio=True))


def seta(x1, y1, x2, y2, papel="t2", tam=22):
    a = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - tam * math.cos(a - 0.5), y2 - tam * math.sin(a - 0.5))
    p2 = (x2 - tam * math.cos(a + 0.5), y2 - tam * math.sin(a + 0.5))
    return linha([(x1, y1), (x2, y2)], papel) + linha([p1, (x2, y2), p2], papel)


def perfil(x, y, s=1.0, olha="dir", papel="t1"):
    """Cabeça e ombros em perfil, sem rosto desenhado. Só nariz e queixo sugeridos pela linha."""
    m = 1 if olha == "dir" else -1
    P = lambda dx, dy: f"{x + m * dx * s:.1f} {y + dy * s:.1f}"
    d = (f"M{P(-150, 300)} C{P(-150, 220)} {P(-120, 190)} {P(-60, 175)} "
         f"L{P(-40, 130)} C{P(-110, 110)} {P(-120, 20)} {P(-90, -40)} "
         f"C{P(-60, -100)} {P(20, -110)} {P(60, -60)} "
         f"C{P(75, -40)} {P(78, -10)} {P(74, 8)} L{P(98, 40)} L{P(72, 48)} "
         f"C{P(74, 70)} {P(66, 92)} {P(40, 100)} L{P(30, 175)} "
         f"C{P(90, 190)} {P(120, 220)} {P(130, 300)}")
    return caminho(d, papel)


# ---------------------------------------------------------------- composições
# Cada peça: id, marcador (x, y), elementos, frase leiga e trecho da tese com página.

def familia_funcionalidade_cognitiva():
    pecas = [
        dict(id="pergunta", marca=(250, 205),
             svg=balao(130, 170, 360, 170, "esq"),
             leigo="Você pergunta, o assistente responde, e você usa a resposta para decidir alguma coisa, seja escrever um texto, resolver uma dúvida de trabalho ou entender um contrato.",
             tese="Trata-se de infraestrutura funcional que organiza como o usuário compreende o problema submetido, confia na resposta recebida, a incorpora à sua tomada de decisão, a revê, a corrige ou a reavalia diante de erro, oscilação ou mudança de desempenho.",
             pg="757"),
        dict(id="capacidade", marca=(470, 450),
             svg=balao(470, 450, 520, 210, "dir") + "".join(
                 bloco(520 + i * 105, 515, 80, 80) for i in range(3)) + caixa(835, 515, 80, 80, "t2", larg=8, tracejado=True),
             leigo="O que você usa depende de muita coisa que fica do lado de lá. Depende de o sistema continuar no ar, da tela continuar parecida, das condições de acesso, dos avisos que aparecem, da memória da conversa quando ela existe e das regras internas do serviço.",
             tese="Ela depende da continuidade do sistema, da estabilidade relativa da interface, da manutenção das condições de acesso, do modelo de apresentação das respostas, das advertências, dos limites contextuais, dos mecanismos de memória ou histórico quando existentes, e das regras privadas que estruturam o próprio campo de uso.",
             pg="759"),
        dict(id="comando", marca=(1010, 170),
             svg=comando(1010, 230) + linha([(1010, 276), (1010, 380), (875, 380), (875, 500)], "t2"),
             leigo="Você entra num ambiente regido por regras, políticas e diretrizes da empresa, que ela pode mudar, limitar e reorganizar quando quiser.",
             tese="Descreve ingresso em ecossistema de uso regulado, passível de condicionamento, limitação e reorganização por governança privada.",
             pg="758"),
    ]
    return dict(id="familia-funcionalidade-cognitiva", w=1200, h=900,
                titulo="Funcionalidade cognitiva",
                alt="Uma pergunta e uma resposta em balões. Dentro da resposta, três blocos azuis de capacidade e um lugar vazio. Um comando da plataforma, fora da conversa, liga-se a esse lugar.",
                pecas=pecas)


def familia_infraestrutura_e_intermediacao():
    ofertas = "".join(caixa(150, 230 + i * 170, 110, 110, "t1") for i in range(3))
    filtro = (linha([(560, 160), (560, 330)], "t2", larg=14) + linha([(560, 400), (560, 520)], "t2", larg=14) +
              linha([(560, 590), (560, 760)], "t2", larg=14) +
              linha([(275, 285), (545, 365)], "t2") + linha([(275, 455), (545, 455)], "t2") +
              linha([(275, 625), (545, 545)], "t2"))
    chega = (linha([(840, 230), (800, 230), (800, 680), (840, 680)], "t1") +
             linha([(1010, 230), (1050, 230), (1050, 680), (1010, 680)], "t1") +
             linha([(575, 365), (845, 355)], "t2") + bloco(860, 290, 130, 130) +
             linha([(575, 455), (865, 545)], "t2") + caixa(880, 500, 90, 90, "t1", larg=10) +
             linha([(575, 545), (640, 545)], "t2", tracejado=True, larg=8))
    pecas = [
        dict(id="ofertas", marca=(205, 175), svg=ofertas,
             leigo="Parece que você está olhando o mercado ou a conversa como eles são. Mas tudo chegou até você já escolhido, ordenado e destacado pela plataforma, com critérios que você não controla e quase nunca consegue conferir.",
             tese="Plataformas dessa natureza não apenas conectam. Elas selecionam, hierarquizam, destacam, ocultam, aproximam, retardam, priorizam e reorganizam a forma pela qual a realidade do ambiente se torna perceptível ao usuário.",
             pg="761"),
        dict(id="filtro", marca=(560, 110), svg=filtro,
             leigo="Compra e conversa são coisas diferentes, mas o mecanismo é o mesmo. Nos dois casos, a plataforma governa o lugar onde as coisas aparecem e prepara o espaço em que você vai decidir.",
             tese="Em ambos os casos, a plataforma governa o ambiente de aparição.",
             pg="762"),
        dict(id="chega", marca=(925, 175), svg=chega,
             leigo="Você não escolhe diante de um mercado transparente, com todas as ofertas lado a lado. Você escolhe dentro de um campo que a plataforma já interpretou para você.",
             tese="O consumidor não escolhe no vazio, diante de universo transparente e simétrico de ofertas. Ele escolhe dentro de um campo já pré-interpretado pela plataforma.",
             pg="762"),
    ]
    return dict(id="familia-infraestrutura-e-intermediacao", w=1200, h=900,
                titulo="Infraestrutura e intermediação",
                alt="Três ofertas iguais passam por um filtro da plataforma. Do outro lado, uma chega em destaque azul, outra chega pequena e a terceira não chega.",
                pecas=pecas)


def familia_produtividade_gig_economy():
    # Rota em três trechos. O do meio gira em torno de uma dobradiça comandada de fora.
    trabalhador = pessoa(250, 606, 0.85, passo=True, mochila=True)
    rota = (linha([(130, 720), (470, 720)], "az", larg=16) + linha([(800, 800), (1080, 800)], "az", larg=16))
    desvio = (linha([(470, 720), (800, 720), (1080, 720)], "t2", larg=7, tracejado=True) +
              linha([(470, 720), (800, 800)], "az", larg=16) + circulo(470, 720, 13, "t1"))
    cmd = comando(640, 250) + linha([(640, 296), (640, 420), (640, 760)], "t2")
    pecas = [
        dict(id="rota", marca=(300, 780), svg=trabalhador + rota,
             leigo="Parece que o aplicativo só paga por corrida, entrega ou tarefa. Mas o que ele fornece de verdade é o próprio lugar onde o seu trabalho se torna possível.",
             tese="O que se fornece, em termos funcionais, é uma infraestrutura privada de possibilidade econômica.",
             pg="765"),
        dict(id="comando", marca=(735, 200), svg=cmd,
             leigo="O que importa é que tudo de que você precisa para trabalhar é oferecido, ajustado e mudado por um sistema que você não controla.",
             tese="Trata-se de reconhecer que a utilidade funcional indispensável ao exercício da atividade econômica é oferecida, modulada e reconfigurada por arquitetura privada que o sujeito não controla.",
             pg="766"),
        dict(id="desvio", marca=(940, 650), svg=desvio,
             leigo="A pergunta é se o seu lugar no aplicativo continua valendo o mesmo que valia quando sustentava a sua expectativa de ganho e de continuar ali.",
             tese="O teste jurídico não pode ser apenas se a conta continua ativa. Precisa ser se a posição funcional do parceiro no ambiente permanece substancialmente equivalente àquela que estruturava sua expectativa legítima de ganho e permanência.",
             pg="767-768"),
    ]
    return dict(id="familia-produtividade-gig-economy", w=1200, h=900,
                titulo="Produtividade sob a gig economy",
                alt="Uma pessoa no começo de uma rota azul. Um comando da plataforma, acima, inclina o trecho do meio, e a rota segue mais baixa do que a linha tracejada que ela seguia antes.",
                pecas=pecas)


def familia_administracao_de_confianca():
    apoio = (caminho("M180 620 C260 560 520 560 640 620 L640 680 L180 680 Z", "t1", preenche="ap", larg=12))
    perda = bloco(365, 470, 90, 90) + seta(410, 300, 410, 440, "t2")
    limite = (linha([(820, 300), (820, 720)], "t2", larg=8, tracejado=True) +
              linha([(990, 300), (990, 720)], "t1", larg=14) + seta(840, 510, 960, 510, "t2"))
    pecas = [
        dict(id="apoio", marca=(240, 720), svg=apoio,
             leigo="Essa confiança não nasce sozinha do bom serviço. Muitas vezes ela é produzida, ajustada e mantida pelo desenho da tela e do atendimento.",
             tese="Em plataformas, a confiança não é subproduto espontâneo da boa execução do serviço. Frequentemente, ela é produzida, calibrada e mantida por desenho.",
             pg="781"),
        dict(id="perda", marca=(410, 250), svg=perda,
             leigo="Num serviço que você usa todo dia, pequenas frustrações vão sendo absorvidas e deixam de parecer um problema. Passam a parecer o funcionamento normal do sistema.",
             tese="A perda deixa de aparecer como evento excepcional e passa a ser metabolizada como parte do normal funcionamento do sistema.",
             pg="781"),
        dict(id="limite", marca=(990, 250), svg=limite,
             leigo="A confiança não precisa vir como garantia formal para ter efeito. Basta que ela leve você a aguentar atritos, aceitar justificativas vagas, achar normal uma perda e continuar usando o serviço mesmo quando ele já piorou.",
             tese="Basta que atue de maneira estável sobre a interpretação ordinária da experiência e sobre a disposição do usuário para suportar atritos, aceitar justificativas vagas, normalizar perdas e permanecer no ciclo de uso mesmo quando a fruição já foi funcionalmente degradada.",
             pg="781"),
    ]
    return dict(id="familia-administracao-de-confianca", w=1200, h=900,
                titulo="Administração de confiança",
                alt="Um bloco azul cai sobre uma superfície que amortece o contato. Ao lado, o limite do que se aceita foi empurrado para longe da posição que tinha antes.",
                pecas=pecas)


def parte_o_nome():
    ra = perfil(480, 420, 1.15, "dir") + circulo(480, 210, 62, "t2")
    isis = perfil(1120, 420, 1.15, "esq")
    nome = (caminho("M600 470 C700 400 900 400 1000 470", "az", larg=10) + circulo(800, 418, 22, "az", cheio=True))
    pecas = [
        dict(id="ra", marca=(350, 150), svg=ra,
             leigo="Rá, o deus Sol, reinava sobre todos, mas não era invulnerável.",
             tese="Seu interesse é forçar o sol a reconhecer que não é absoluto.",
             pg="792"),
        dict(id="isis", marca=(1250, 150), svg=isis,
             leigo="Ísis não queria destruir o Sol. Queria só que ele reconhecesse que não era absoluto.",
             tese="Ao mesmo tempo, Ísis não deseja aniquilar o sol.",
             pg="792"),
        dict(id="nome", marca=(800, 340), svg=nome,
             leigo="Uma vez nomeado, o poder deixa de ser pura presença, que simplesmente está lá, e passa a poder ser chamado, delimitado e obrigado a responder pelo que faz.",
             tese="Uma vez nomeado, o poder deixa de operar como pura presença natural e passa a ser invocável, delimitável e, portanto, obrigado a responder por seus atos.",
             pg="792"),
    ]
    return dict(id="parte-o-nome", w=1600, h=900, titulo="O nome",
                alt="Dois perfis frente a frente, Rá à esquerda, com o disco do Sol acima, e Ísis à direita. Entre eles, um vínculo azul com um ponto no meio, o nome.",
                pecas=pecas)



# ---------------------------------------------------------------- figura humana e módulo

def pessoa(x, y, s=1.0, segura=None, passo=False, mochila=False, papel="t1"):
    """Pessoa calma, sem rosto, em contorno. (x, y) é a cintura. segura='dir' ou 'esq' estende o braço."""
    S = lambda v: v * s
    out = circulo(x, y - S(158), S(34), papel)
    out += caminho(f"M{x - S(44)} {y} V{y - S(88)} Q{x - S(44)} {y - S(112)} {x - S(20)} {y - S(112)} "
                   f"H{x + S(20)} Q{x + S(44)} {y - S(112)} {x + S(44)} {y - S(88)} V{y}", papel)
    if passo:
        out += linha([(x - S(14), y), (x - S(52), y + S(112))], papel) + linha([(x + S(14), y), (x + S(46), y + S(112))], papel)
    else:
        out += linha([(x - S(18), y), (x - S(22), y + S(112))], papel) + linha([(x + S(18), y), (x + S(22), y + S(112))], papel)
    lados = {"dir": 1, "esq": -1}
    for lado, m in lados.items():
        if segura == lado:
            out += linha([(x + m * S(44), y - S(92)), (x + m * S(92), y - S(52))], papel)
        else:
            out += linha([(x + m * S(44), y - S(92)), (x + m * S(58), y - S(10))], papel)
    if mochila:
        out += caixa(x - S(104), y - S(108), S(54), S(64), papel, larg=10)
    return out


def modulo(x, y, t=70, papel="az"):
    """Módulo azul do leitor, centrado em (x, y). Não é logotipo, moeda nem botão."""
    return bloco(x - t / 2, y - t / 2, t, t, papel, r=6)


def corte(x, y, vertical=False, t=26):
    """Interrupção de uma ligação. Duas barras curtas paralelas."""
    if vertical:
        return linha([(x - t, y - 9), (x + t, y - 9)], "t1", larg=8) + linha([(x - t, y + 9), (x + t, y + 9)], "t1", larg=8)
    return linha([(x - 9, y - t), (x - 9, y + t)], "t1", larg=8) + linha([(x + 9, y - t), (x + 9, y + t)], "t1", larg=8)


# ---------------------------------------------------------------- textos tirados das fontes

import re as _re

_FONTES = {}


def _secao(arquivo, chave):
    if arquivo not in _FONTES:
        _FONTES[arquivo] = (RAIZ / "conteudo" / arquivo).read_text(encoding="utf-8")
    t = _FONTES[arquivo]
    if chave is None:
        return t
    m = _re.search(r"^## " + _re.escape(chave) + r"\s*$(.*?)(?=^## |\Z)", t, _re.M | _re.S)
    if not m:
        raise KeyError(f"{arquivo} sem seção {chave}")
    return m.group(1)


def F(arquivo, chave, leigo, tese=None):
    """Acha a frase leiga inteira que contém `leigo` e o trecho literal que contém `tese`.

    A frase leiga se estende até o ponto final. Pode-se pedir duas frases seguidas com ' + '.
    O trecho da tese vem inteiro, da linha que começa por '> ', com a página que ela traz.
    """
    sec = _secao(arquivo, chave)
    texto = " ".join(l for l in sec.split("\n") if l.strip() and not l.startswith((">", "#", "lei:")))
    frases = _re.split(r"(?<=[.?!])\s+", texto)
    partes = []
    for pedaco in leigo.split(" + "):
        achou = [f for f in frases if pedaco in f]
        if not achou:
            raise KeyError(f"frase leiga não achada em {arquivo}/{chave}: {pedaco}")
        partes.append(achou[0])
    out = {"leigo": " ".join(partes)}
    if tese:
        linhas = [l[2:].strip() for l in sec.split("\n") if l.startswith("> ") and tese in l]
        if not linhas:
            raise KeyError(f"trecho não achado em {arquivo}/{chave}: {tese}")
        m = _re.match(r"(.*?)\s*\(p\. ([\d\-–]+)\)\s*$", linhas[0])
        out["tese"], out["pg"] = m.group(1), m.group(2)
    else:
        out["tese"], out["pg"] = None, None
    return out


def P(id, marca, svg, fonte):
    return dict(id=id, marca=marca, svg=svg, **fonte)


# ---------------------------------------------------------------- Família 4, entradas

def direitos_continua():
    estrutura = caixa(250, 300, 240, 300, "t2") + linha([(250, 400), (490, 400)], "t2") + linha([(250, 500), (490, 500)], "t2")
    entrega = seta(520, 360, 900, 360, "t2") + pessoa(1180, 560, segura="esq") + modulo(1040, 500)
    vinculo = caminho("M490 540 C700 540 820 620 1004 520", "t1", larg=8) + "".join(
        circulo(x, y, 9, "t1", cheio=True) for x, y in ((600, 545), (740, 575), (880, 575)))
    f = "direitos.md"
    return dict(id="direitos-continua", w=1600, h=900, titulo="Os deveres continuam depois da compra",
                alt="Um módulo azul passa da estrutura da plataforma para as mãos de uma pessoa. Uma ligação continua ativa entre a estrutura e o módulo depois da entrega.",
                pecas=[
                    P("entrega", (700, 300), entrega, F(f, "intro", "Quando o que você compra só existe dentro de uma plataforma, a venda não termina no clique.", "Em consumo contínuo")),
                    P("vinculo", (740, 650), vinculo, F(f, "intro", "A empresa continua mantendo, mudando e controlando", "A fruição, aqui, não aparece")),
                    P("estrutura", (370, 250), estrutura, F(f, "intro", "O que muda é a forma de contar o conflito", "Muda a forma de narrar")),
                ])


def alem_do_consumo():
    banca = (linha([(590, 610), (590, 700)], "t1") + linha([(1010, 610), (1010, 700)], "t1") +
             modulo(650, 480, 56) + modulo(930, 480, 56) + caixa(972, 452, 56, 56, "t1", larg=10))
    vendedor = pessoa(790, 505, 0.9) + '<rect x="560" y="520" width="480" height="90" rx="4" class="s-t1 f-ap" stroke-width="12"/>'
    toldo = (linha([(540, 260), (1060, 260)], "t2", larg=12) + linha([(560, 260), (560, 300)], "t2") + linha([(1040, 260), (1040, 300)], "t2") +
             linha([(1060, 260), (1240, 260), (1240, 700)], "t2") + comando(1240, 190) +
             linha([(1180, 260), (1240, 320)], "t2"))
    f = "alem-do-consumo.md"
    return dict(id="alem-do-consumo", w=1600, h=900, titulo="Além do consumo",
                alt="Uma pessoa vende numa banca aberta. A cobertura da banca é sustentada por uma estrutura de fora, com um comando que a pessoa não alcança.",
                pecas=[
                    P("banca", (500, 600), banca, F(f, "pagina", "O que você construiu numa plataforma é um bem, mesmo sem corpo.")),
                    P("vendedor", (690, 210), vendedor, F(f, "pagina", "Quem vende numa loja virtual, trabalha por aplicativo")),
                    P("estrutura", (1330, 190), toldo, F(f, "pagina", "Você tem o bem, mas não controla as condições para usar o que tem")),
                ])


def como_reclamar():
    gente = pessoa(380, 560, segura="dir") + modulo(490, 508, 48)
    nos = [(900, 230), (1180, 360), (1180, 600), (900, 730)]
    caminhos = "".join(caminho(f"M530 508 C700 508 700 {y} {x - 46} {y}", "t2") + circulo(x, y, 44, "t1") for x, y in nos)
    f = "como-reclamar.md"
    return dict(id="como-reclamar", w=1600, h=900, titulo="Como reclamar",
                alt="Uma pessoa com um registro azul diante de quatro caminhos que levam a quatro pontos vazios, sem que um pareça mais forte que os outros.",
                pecas=[
                    P("pessoa", (300, 280), gente, F(f, "como-reclamar", "O primeiro caminho costuma ser a própria empresa")),
                    P("caminhos", (1040, 480), caminhos, F(f, "como-reclamar", "Cada caminho abre a chance de a empresa responder")),
                    P("registro", (560, 600), "", F(f, "como-reclamar", "Ajuda levar capturas de tela com data")),
                ])


# ---------------------------------------------------------------- Família 5, problemas

def _prob(id, titulo, alt, pecas):
    return dict(id=f"problema-{id}", w=1600, h=900, titulo=titulo, alt=alt, pecas=pecas)


def problema_conta_bloqueada():
    f, c = "problemas.md", "conta-bloqueada"
    ambiente = "".join(caixa(x - 40, y - 40, 80, 80, "t2", larg=9) for x, y in ((360, 300), (360, 600), (620, 450))) + \
        linha([(400, 300), (580, 430)], "t2") + linha([(400, 600), (580, 470)], "t2")
    ligacao = linha([(660, 450), (860, 450)], "t2") + corte(890, 450) + linha([(920, 450), (1060, 450)], "t2", tracejado=True, larg=8)
    posicao = pessoa(1240, 560, segura="esq") + modulo(1110, 500)
    return _prob("conta-bloqueada", "Conta bloqueada", "O ambiente da plataforma, à esquerda, liga-se a um módulo azul nas mãos de uma pessoa. A ligação está cortada, e o módulo continua inteiro e identificável.", [
        P("posicao", (1110, 400), posicao, F(f, c, "você perde também o acesso a tudo o que estava nela", "Se a conta é encerrada")),
        P("corte", (890, 360), ligacao, F(f, c, "O que se exige é que a punição tenha motivo verificável", "Em ecossistemas de plataforma, sanções")),
        P("ambiente", (360, 200), ambiente, F(f, c, "Muitas vezes a conta continua ativa, mas fica menos visível", "A punição relevante muitas vezes")),
    ])


def problema_item_alterado():
    f, c = "problemas.md", "item-alterado"
    antes = linha([(280, 420), (280, 560), (480, 560), (480, 420)], "t1") + modulo(380, 490, 100)
    depois = linha([(1040, 420), (1040, 560), (1180, 560), (1180, 470), (1240, 470), (1240, 420)], "t1") + modulo(1140, 440, 100)
    cmd = comando(1210, 230) + linha([(1210, 276), (1210, 400)], "t2")
    return _prob("item-alterado", "Item alterado", "O mesmo módulo azul em dois momentos. Antes, ele encaixa por inteiro na base. Depois, um comando de fora mudou a base, e o módulo continua igual mas já não encaixa.", [
        P("antes", (380, 340), antes + seta(560, 490, 940, 490, "t2"), F(f, c, "O caso típico é o do item que segue no inventário", "A força do critério")),
        P("encaixe", (1040, 640), depois, F(f, c, "O item continua lá, mas já não serve do mesmo jeito", "A permanência do item")),
        P("comando", (1300, 170), cmd, F(f, c, "Uma atualização, que é a mudança que a empresa faz", "A mutabilidade, por si")),
    ])


def problema_servico_piorou():
    f, c = "problemas.md", "servico-piorou"
    contrib = caixa(260, 300, 420, 70, "t1") + caixa(920, 300, 420, 70, "t1")
    entrega = bloco(260, 470, 420, 70) + bloco(920, 470, 190, 70) + caixa(1110, 470, 230, 70, "t2", larg=8, tracejado=True)
    marca = linha([(800, 260), (800, 640)], "t2", larg=7)
    return _prob("servico-piorou", "O serviço piorou", "Duas faixas comparáveis, antes e depois. A faixa de cima, do que você paga, é igual nas duas. A faixa azul de baixo, do que é entregue, encolheu, e o tracejado mostra o tamanho que ela tinha.", [
        P("contribuicao", (470, 240), contrib, F(f, c, "O nome e o preço ficaram iguais, e o que encolheu foi a entrega.", "A redução raramente")),
        P("entrega", (1225, 600), entrega, F(f, c, "A casca do serviço pode continuar intacta", "Em linguagem menos pomposa")),
        P("limite", (800, 690), marca, F(f, c, "Oscilação de um dia ou ajuste pequeno não bastam", "O gatilho não é qualquer mudança")),
    ])


def problema_presente_retirado():
    f, c = "problemas.md", "presente-retirado"
    origem = circulo(220, 450, 36, "t2") + linha([(256, 450), (330, 450)], "t2") + corte(360, 450) + linha([(390, 450), (520, 450)], "t2", tracejado=True, larg=8)
    canal = caixa(540, 390, 200, 120, "t1") + linha([(740, 450), (1020, 450)], "t2")
    presente = pessoa(1240, 560, segura="esq") + modulo(1110, 500)
    return _prob("presente-retirado", "Presente retirado", "Um presente azul já está com quem o recebeu. A ligação que o trouxe se interrompe muito longe, na origem, antes de passar pelo canal oficial.", [
        P("presente", (1110, 400), presente, F(f, c, "Você recebeu um item de presente pela função oficial do jogo", "A segunda camada")),
        P("origem", (360, 370), origem, F(f, c, "O que costuma estar por trás é o chargeback", "Em política oficial específica")),
        P("canal", (640, 330), canal, F(f, c, "Conta muito saber se a função era oficial.", "A função de presentes não operava")),
    ])


def problema_jogo_encerrado():
    f, c = "problemas.md", "jogo-encerrado"
    estrutura = linha([(260, 200), (1340, 200)], "t2", larg=14) + linha([(300, 200), (300, 140)], "t2") + linha([(1300, 200), (1300, 140)], "t2")
    xs = (480, 800, 1120)
    lig = "".join(linha([(x, 200), (x, 270)], "t2") + corte(x, 300, vertical=True) +
                  linha([(x, 330), (x, 400)], "t2", tracejado=True, larg=7) for x in xs)
    gente = "".join(pessoa(x, 690, 0.85, segura="dir") + modulo(x + 80, 640, 56) for x in xs)
    return _prob("jogo-encerrado", "Jogo encerrado", "Uma estrutura de serviço, no alto, deixa de sustentar três módulos azuis. As ligações estão cortadas, e cada módulo continua com uma pessoa.", [
        P("estrutura", (260, 130), estrutura, F(f, c, "Ela pode encerrar o negócio, mas esse direito não inclui apagar tudo", "O direito de explorar")),
        P("ligacoes", (870, 300), lig, F(f, c, "O que você comprou só funciona enquanto alguém mantém", "Quando o serviço apresenta")),
        P("acervo", (1260, 590), gente, F(f, c, "Vão junto fotos, históricos", "Fotografias, históricos")),
    ])


def problema_so_licenca():
    f, c = "problemas.md", "so-licenca"
    pos = pessoa(420, 560, segura="dir") + modulo(550, 500)
    lig = caminho("M586 500 C800 500 900 380 1080 380", "t1", larg=6)
    estrutura = caixa(1080, 300, 240, 300, "t2") + comando(1200, 450, 52)
    return _prob("so-licenca", "Só uma licença", "Uma pessoa segura um módulo azul. Uma ligação técnica fina sai dele e chega a uma estrutura com um comando, que regula o uso.", [
        P("modulo", (550, 400), pos, F(f, c, "Você pagou, o botão dizia comprar", "Os Termos de Serviço descrevem")),
        P("ligacao", (840, 520), lig, F(f, c, "É o quanto aquilo que você usa depende de um ambiente", "Sempre que a utilidade consumida")),
        P("estrutura", (1200, 240), estrutura, F(f, c, "O nome que o contrato dá não decide sozinho", "A lei não condiciona")),
    ])


def problema_promessa():
    f, c = "problemas.md", "promessa"
    ref = caixa(290, 360, 180, 180, "t1")
    prometido = caixa(820, 220, 460, 460, "t2", larg=9, tracejado=True)
    entregue = bloco(960, 360, 180, 180)
    return _prob("promessa", "A promessa não se cumpriu", "Um objeto de referência à esquerda. À direita, o contorno tracejado do que foi prometido é bem maior que o bloco azul entregue dentro dele.", [
        P("prometido", (1280, 220), prometido, F(f, c, "A oferta é aquilo que a empresa se compromete a entregar", "A promessa juridicamente relevante")),
        P("entregue", (1050, 450), entregue, F(f, c, "Você comprou depois de ver prévias", "Sempre que a fruição for precedida")),
        P("referencia", (380, 330), ref, F(f, c, "Uma frase solta e animada, sem peso na sua decisão, não basta.", "O controle da oferta")),
    ])


def problema_exclusivo_voltou():
    f, c = "problemas.md", "exclusivo-voltou"
    isolado = linha([(280, 600), (520, 600)], "t1") + linha([(310, 600), (310, 660)], "t1") + linha([(490, 600), (490, 660)], "t1") + modulo(400, 530, 110)
    serie = "".join(modulo(820 + i * 130, 560, 80) for i in range(5)) + linha([(760, 640), (1400, 640)], "t2")
    olhar = "".join(circulo(x, 300, 16, "t2", cheio=True) for x in (300, 400, 500)) + "".join(
        linha([(x, 320), (400, 460)], "t2", larg=6) for x in (300, 400, 500))
    return _prob("exclusivo-voltou", "O exclusivo voltou", "Um módulo azul aparece sozinho sobre uma base, à vista de outros. Depois, o mesmo módulo reaparece repetido em série.", [
        P("isolado", (400, 720), isolado, F(f, c, "Você pagou mais porque o item era raro", "Quando a plataforma vende um item")),
        P("serie", (1080, 450), serie, F(f, c, "Ele pode ter voltado numa loja alternativa", "Se, passado um período")),
        P("status", (590, 260), olhar, F(f, c, "Num item que os outros veem", "Em bens imateriais, especialmente")),
    ])



def folha(x, y, w=90, h=116, papel="t1", azul=False):
    """Registro simples. Folha com três linhas."""
    out = bloco(x, y, w, h, "az", r=6) if azul else caixa(x, y, w, h, papel, larg=9)
    cor = "ap" if azul else papel
    for i in range(3):
        out += linha([(x + 18, y + 30 + i * 26), (x + w - 18, y + 30 + i * 26)], cor if not azul else "ap", larg=7)
    return out


def problema_sorteio():
    f, c = "problemas.md", "sorteio"
    caixa_ = caixa(620, 220, 460, 460, "t1") + linha([(620, 450), (1080, 450)], "t2", larg=7)
    pos = []
    for i in range(4):
        for j in range(3):
            x, y = 1150 + j * 80, 270 + i * 100
            pos.append(bloco(x, y, 56, 56) if (i, j) in ((1, 2), (3, 0)) else caixa(x, y, 56, 56, "t2", larg=7))
    recorte = linha([(1080, 240), (1400, 240)], "t2", larg=7) + linha([(1080, 660), (1400, 660)], "t2", larg=7) + "".join(pos)
    entrada = circulo(330, 450, 30, "t1") + seta(380, 450, 590, 450, "t2")
    return _prob("sorteio", "Sorteio pago", "Uma caixa fechada recebe o pagamento. Num recorte ao lado aparecem muitas posições vazias e só duas azuis.", [
        P("caixa", (850, 160), caixa_, F(f, c, "Esse é um dos pontos mais sensíveis do consumo nos jogos", "Diferentemente de uma fase do jogo")),
        P("recorte", (1270, 720), recorte, F(f, c, "O valor do que você leva passa a depender de regras internas", "O ponto de maior sensibilidade")),
        P("entrada", (330, 370), entrada, F(f, c, "Quando a compra direta some e o sorteio vira obrigatório", "Esse desenho explicita uma perda")),
    ])


def problema_moeda():
    f, c = "problemas.md", "moeda"
    fichas = "".join(circulo(330, 600 - i * 64, 30, "az", cheio=True) for i in range(4))
    conversao = linha([(420, 560), (1100, 470)], "t1") + linha([(420, 560), (1100, 560)], "t2", larg=7, tracejado=True) + \
        circulo(420, 560, 12, "t1", cheio=True) + caixa(1130, 400, 140, 140, "t1")
    cmd = comando(860, 230) + linha([(860, 276), (860, 500)], "t2")
    return _prob("moeda", "A moeda mudou de valor", "Fichas azuis de um lado e um item do outro. Entre eles, uma relação de conversão que um comando de fora inclinou, e o tracejado mostra a posição de antes.", [
        P("fichas", (330, 330), fichas, F(f, c, "Você comprou moeda interna com dinheiro de verdade", "A Riot não descreve a moeda")),
        P("comando", (960, 180), cmd, F(f, c, "A empresa que vende a moeda é a mesma que fixa os preços", "O que se observa, porém")),
        P("conversao", (700, 640), conversao, F(f, c, "Cada moeda funciona como um idioma próprio", "O consumidor deixa de lidar")),
    ])


def problema_pressa():
    f, c = "problemas.md", "pressa"
    jan = linha([(240, 180), (1000, 400)], "t1") + linha([(240, 720), (1000, 500)], "t1") + linha([(1000, 400), (1000, 360)], "t1") + linha([(1000, 500), (1000, 540)], "t1")
    objeto = modulo(1260, 450, 110)
    canto = "".join(linha([(1180 + i * 40, 700), (1210 + i * 40, 700)], "t2", larg=6) for i in range(4))
    return _prob("pressa", "Fui apressado", "Uma passagem que se estreita da esquerda para a direita até uma fresta. O módulo azul, adiante, continua inteiro e disponível.", [
        P("janela", (560, 210), jan, F(f, c, "A contagem regressiva, a edição limitada", "A primeira família dessas técnicas")),
        P("objeto", (1260, 330), objeto, F(f, c, "Um item digital poderia ser vendido a todo mundo", "Em objetos digitais, o custo marginal")),
        P("canto", (1360, 760), canto, F(f, c, "A urgência fica em destaque, enquanto os limites de uso", "O fornecedor enfatiza urgência")),
    ])


def problema_regras_escondidas():
    f, c = "problemas.md", "regras-escondidas"
    camadas = ""
    for k in range(3):
        x, y = 340 + k * 70, 220 + k * 70
        camadas += f'<rect x="{x}" y="{y}" width="460" height="360" rx="6" class="s-t1 f-ap" stroke-width="12"/>'
    condicao = bloco(290, 600, 110, 36)
    gente = pessoa(1220, 560)
    return _prob("regras-escondidas", "A regra estava escondida", "Três folhas sobrepostas. Uma condição azul, decisiva, aparece só pela borda da folha de baixo. Uma pessoa olha de longe.", [
        P("camadas", (720, 180), camadas, F(f, c, "Pode haver texto demais, de modo que o essencial se perde", "A inadequação informacional, assim")),
        P("condicao", (250, 690), condicao, F(f, c, "Estar escrito em algum lugar não basta", "O ponto decisivo, portanto")),
        P("momento", (1220, 340), gente, F(f, c, "A pergunta, então, é se a regra apareceu de forma clara", "A pergunta juridicamente relevante")),
    ])


def problema_prova():
    f, c = "problemas.md", "prova"
    leitor = pessoa(330, 560, segura="dir") + folha(410, 440, azul=True)
    limite = linha([(720, 200), (720, 720)], "t1", larg=14)
    pilha = "".join(folha(900 + (k % 3) * 140, 260 + (k // 3) * 170) for k in range(6))
    return _prob("prova", "Quem guarda a prova", "Uma pessoa segura um registro azul. Do outro lado de um limite ficam vários registros que ela não alcança.", [
        P("registro", (455, 380), leitor, F(f, c, "Por isso o trabalho de provar pode ser dividido", "Quanto mais dependente")),
        P("registros", (1110, 200), pilha, F(f, c, "A empresa sabe o que mostrou a você", "Em OICs, o fornecedor não controla")),
        P("limite", (720, 140), limite, F(f, c, "Quando tudo isso fica só com ela", "Em ambientes de fruição governada")),
    ])


def problema_reclamacao_some():
    f, c = "problemas.md", "reclamacao-some"
    pedido = modulo(260, 450, 70)
    circuito = caminho("M300 450 H860 C980 450 980 250 860 250 H300", "t2") + seta(300, 250, 300, 395, "t2")
    resposta = circulo(1280, 450, 60, "t1") + linha([(1040, 450), (1210, 450)], "t2", larg=7, tracejado=True)
    return _prob("reclamacao-some", "A reclamação some", "Um pedido azul entra num circuito, dá a volta e retorna ao começo, sem chegar ao ponto de resposta, que fica adiante.", [
        P("pedido", (260, 360), pedido, F(f, c, "O atendimento é gentil, responde rápido e pede para aguardar", "Em ecossistemas governados por plataforma")),
        P("circuito", (640, 180), circuito, F(f, c, "A resposta parece explicar, mas não diz o que houve", "A plataforma pode, por exemplo")),
        P("resposta", (1280, 340), resposta, F(f, c, "É se o atendimento funciona de um jeito que desvia", "O que importa não é saber")),
    ])


def problema_sair():
    f, c = "problemas.md", "sair"
    origem = caixa(200, 300, 220, 300, "t2")
    acervo = linha([(420, 450), (500, 450)], "t2") + modulo(550, 400, 60) + modulo(550, 480, 60) + modulo(620, 440, 60)
    limite = linha([(860, 180), (860, 740)], "t1", larg=14)
    gente = pessoa(1150, 560, passo=True)
    return _prob("sair", "Quero sair e levar o que é meu", "Uma pessoa já atravessou um limite. O acervo azul dela ficou para trás, preso à estrutura de origem por uma ligação curta.", [
        P("pessoa", (1150, 330), gente, F(f, c, "Você pensa em largar o jogo, a rede ou o serviço", "A permanência passa a depender")),
        P("acervo", (590, 340), acervo + origem, F(f, c, "Aqui é diferente, porque o histórico, o ranque", "A barreira de saída")),
        P("limite", (860, 130), limite, F(f, c, "O sinal mais claro aparece quando a empresa muda as regras", "Em contratos cativos")),
    ])


def problema_historia_perdida():
    f, c = "problemas.md", "historia-perdida"
    seq = "".join(modulo(260 + i * 120, 400, 70) for i in range(4))
    perdidos = "".join(caixa(860 + i * 120 - 35, 470 + i * 26, 70, 70, "t2", larg=7, tracejado=True) for i in range(4))
    suporte = linha([(200, 460), (720, 460)], "t2", larg=14) + linha([(1060, 460), (1360, 460)], "t2", larg=14) + \
        linha([(720, 440), (720, 480)], "t1", larg=8) + linha([(1060, 440), (1060, 480)], "t1", larg=8)
    return _prob("historia-perdida", "Perdi a minha história", "Uma sequência de registros azuis apoiada num suporte. Um trecho do suporte foi retirado, e o que vinha depois perdeu a continuidade.", [
        P("sequencia", (440, 300), seq, F(f, c, "O que fica na conta ao longo dos anos não é só acesso", "Em ecossistemas governados por plataforma, o que")),
        P("suporte", (890, 380), suporte, F(f, c, "Um banimento, que é a expulsão definitiva da conta", "A cláusula 2.3")),
        P("continuidade", (1100, 680), perdidos, F(f, c, "Essa perda pode ir além do preço do que você comprou", "O que se perde, nesses casos")),
    ])



def problema_programa_no_aparelho():
    f, c = "problemas.md", "programa-no-aparelho"
    aparelho = caixa(220, 200, 760, 440, "t1", r=14) + linha([(160, 700), (1040, 700)], "t1") + linha([(220, 640), (160, 700)], "t1") + linha([(980, 640), (1040, 700)], "t1") + modulo(360, 420, 90)
    componente = caixa(700, 330, 180, 180, "t2") + comando(790, 420, 46)
    ligacao = linha([(880, 420), (1180, 420)], "t2") + caixa(1180, 300, 220, 240, "t2")
    return _prob("programa-no-aparelho", "Um programa no meu aparelho", "Dentro do contorno do aparelho, ao lado do que é da pessoa, há um componente de controle instalado, ligado a uma estrutura de fora.", [
        P("aparelho", (300, 150), aparelho, F(f, c, "Combater trapaça é legítimo, mas a palavra segurança", "A soberania privada da plataforma")),
        P("componente", (790, 260), componente, F(f, c, "Ele liga quando o computador liga", "Quando a proteção do ambiente")),
        P("ligacao", (1290, 240), ligacao, F(f, c, "A pergunta é se esse interesse basta", "O problema passa a ser de proporcionalidade")),
    ])


def problema_crianca():
    f, c = "problemas.md", "crianca"
    mecanismo = caixa(700, 180, 260, 560, "t2") + linha([(740, 300), (920, 300)], "t2") + circulo(830, 380, 40, "t2") + linha([(740, 470), (920, 470)], "t2")
    crianca = pessoa(560, 620, 0.62)
    adulto = pessoa(1180, 560)
    return _prob("crianca", "Meu filho gastou num jogo", "Uma criança diante de um mecanismo de decisão alto, feito na medida de um adulto. Um adulto está por perto.", [
        P("mecanismo", (830, 130), mecanismo, F(f, c, "Ela vem em pedaços, puxada por ciclos de retorno", "Em jogos operados como serviço")),
        P("crianca", (560, 400), crianca, F(f, c, "A lei já vê crianças e adolescentes", "O recorte por menores")),
        P("adulto", (1180, 330), adulto, F(f, c, "Eles podem chegar à família", "Os efeitos irradiam-se")),
    ])


def problema_assistente():
    f, c = "problemas.md", "assistente"
    resposta = balao(200, 300, 340, 170, "esq")
    orientacao = linha([(560, 385), (820, 385), (960, 500)], "az", larg=16) + linha([(960, 500), (1040, 566)], "az", larg=16) + linha([(1012, 596), (1068, 536)], "t1", larg=8)
    destino = circulo(1290, 680, 56, "t1") + linha([(1100, 615), (1230, 660)], "t2", larg=7, tracejado=True)
    return _prob("assistente", "O assistente errou", "Uma resposta em balão orienta por um caminho azul, que termina antes de chegar ao destino.", [
        P("resposta", (370, 240), resposta, F(f, c, "Você usou um assistente de inteligência artificial", "O serviço vale não apenas")),
        P("orientacao", (820, 320), orientacao, F(f, c, "Pode haver problema quando ela parece mais segura e completa", "Pode haver ruído informacional")),
        P("lacuna", (1290, 580), destino, F(f, c, "Pode bastar que ele troque a clareza por uma aparência de confiança", "Pode haver, ainda, assimetria")),
    ])


def problema_loja_virtual():
    f, c = "problemas.md", "loja-virtual"
    destaque = bloco(560, 300, 220, 220)
    secundarias = "".join(caixa(880 + i * 150, 420, 100, 100, "t2", larg=8) for i in range(3))
    filtro = linha([(520, 220), (1340, 220)], "t2", larg=14) + comando(1430, 220, 44) + linha([(520, 600), (1340, 600)], "t2")
    return _prob("loja-virtual", "A loja virtual escolheu por mim", "Uma vitrine em que uma oferta aparece grande e azul, à frente. As outras continuam ali, menores e de lado, sob uma barra que a plataforma regula.", [
        P("destaque", (670, 250), destaque, F(f, c, "Numa loja virtual com muitos vendedores", "O consumidor não escolhe no vazio")),
        P("secundarias", (1105, 360), secundarias, F(f, c, "Ela escolhe o que aparece primeiro", "Plataformas dessa natureza")),
        P("filtro", (1430, 150), filtro, F(f, c, "Quando a mesma empresa organiza a vitrine", "Em hipóteses mais graves")),
    ])


def problema_rede_social():
    f, c = "problemas.md", "rede-social"
    emissao = circulo(260, 450, 44, "az", cheio=True) + linha([(304, 450), (560, 450)], "az", larg=12)
    regulador = caixa(560, 370, 200, 160, "t2") + comando(660, 450, 44)
    pontos = [(1200, 200), (1290, 320), (1320, 450), (1290, 580), (1200, 700)]
    alcance = "".join((linha([(760, 450), (x - 30, y)], "t2") + circulo(x, y, 30, "t1")) if k in (1, 3) else circulo(x, y, 30, "t2", larg=7)
                      for k, (x, y) in enumerate(pontos))
    return _prob("rede-social", "A rede reduziu o meu alcance", "Uma emissão azul passa por um regulador da plataforma e chega a só dois dos pontos que poderia alcançar.", [
        P("emissao", (260, 360), emissao, F(f, c, "Numa rede social, o que você vê e quantas pessoas veem", "Os Termos de Serviço da Meta")),
        P("regulador", (660, 310), regulador, F(f, c, "Pode haver problema quando a mudança mexe na lógica de visibilidade", "A equivalência funcional, por sua vez")),
        P("pontos", (1400, 450), alcance, F(f, c, "O seu acesso, a sua permanência, a sua visibilidade", "Sempre que acesso, permanência")),
    ])


def problema_trabalho_por_app():
    f, c = "problemas.md", "trabalho-por-app"
    trab = pessoa(330, 606, 0.85, passo=True, mochila=True)
    rota = linha([(200, 720), (620, 720)], "az", larg=16)
    alterado = linha([(620, 720), (960, 600), (1360, 600)], "az", larg=16) + linha([(620, 720), (1360, 720)], "t2", larg=7, tracejado=True)
    cmd = comando(960, 240) + linha([(960, 286), (960, 590)], "t2")
    return _prob("trabalho-por-app", "Trabalho por aplicativo", "Uma pessoa segue andando por uma rota azul. Adiante, um comando de fora ergueu a rota numa subida, e o tracejado mostra o caminho plano de antes.", [
        P("trabalhador", (330, 360), trab + rota, F(f, c, "Você trabalha com entregas ou corridas por aplicativo", "O que se fornece, em termos funcionais")),
        P("comando", (1060, 190), cmd, F(f, c, "Quem distribui as chamadas, calcula o ganho", "A plataforma organiza acesso")),
        P("percurso", (1200, 520), alterado, F(f, c, "Mesmo assim, podem esvaziar de modo relevante", "Mudanças em critérios de distribuição")),
    ])


def problema_vendo_na_plataforma():
    f, c = "problemas.md", "vendo-na-plataforma"
    vendedor = pessoa(500, 505, 0.9) + '<rect x="300" y="520" width="460" height="90" rx="4" class="s-t1 f-ap" stroke-width="12"/>' + linha([(330, 610), (330, 700)], "t1") + modulo(390, 480, 56) + modulo(640, 480, 56)
    apoio = linha([(730, 610), (730, 700)], "t2") + caixa(705, 630, 50, 40, "t2", larg=8)
    cmd = comando(1280, 220) + linha([(1280, 266), (1280, 650), (755, 650)], "t2")
    return _prob("vendo-na-plataforma", "Vendo numa plataforma", "Uma pessoa vende numa bancada. Um lado da bancada depende de um apoio ajustado por um comando longe dali, fora do alcance dela.", [
        P("vendedor", (440, 230), vendedor, F(f, c, "Ter renda pela plataforma não tira, por si, essa proteção.", "A existência de interesse econômico")),
        P("apoio", (800, 700), apoio, F(f, c, "Quem vende depende do ranking, da reputação", "A plataforma não precisa expulsar")),
        P("comando", (1380, 170), cmd, F(f, c, "O que pesa é o quanto a plataforma governa a sua presença nela.", "O usuário profissionalizado")),
    ])


def problema_muita_gente():
    f, c = "problemas.md", "muita-gente"
    pos = [(300, 220), (260, 450), (300, 680), (560, 160), (560, 740), (720, 450)]
    caixas_ = "".join(caixa(x - 45, y - 45, 90, 90, "t1", larg=10) for x, y in pos)
    marcas = "".join(bloco(x + 5, y - 40, 34, 34) for x, y in pos)
    causa = circulo(1220, 450, 70, "t2") + comando(1220, 450, 40) + "".join(linha([(x + 45, y), (1150, 450)], "t2", larg=7) for x, y in pos)
    return _prob("muita-gente", "Aconteceu com muita gente", "Seis posições diferentes têm a mesma marca azul no mesmo canto, e todas se ligam a uma única causa comum.", [
        P("posicoes", (180, 120), caixas_, F(f, c, "O mesmo problema atingiu muita gente no mesmo serviço", "O atingimento não é homogêneo")),
        P("alteracao", (440, 450), marcas, F(f, c, "Os casos não precisam ser iguais", "A tutela coletiva se justifica")),
        P("causa", (1220, 330), causa, F(f, c, "O sinal é uma origem única", "Em ambientes de plataforma, a fonte lesiva")),
    ])


COMPOSICOES = [familia_funcionalidade_cognitiva, familia_infraestrutura_e_intermediacao,
               familia_produtividade_gig_economy, familia_administracao_de_confianca, parte_o_nome,
               direitos_continua, alem_do_consumo, como_reclamar,
               problema_conta_bloqueada, problema_item_alterado, problema_servico_piorou, problema_presente_retirado,
               problema_jogo_encerrado, problema_so_licenca, problema_promessa, problema_exclusivo_voltou,
               problema_sorteio, problema_moeda, problema_pressa, problema_regras_escondidas,
               problema_prova, problema_reclamacao_some, problema_sair, problema_historia_perdida,
               problema_programa_no_aparelho, problema_crianca, problema_assistente, problema_loja_virtual,
               problema_rede_social, problema_trabalho_por_app, problema_vendo_na_plataforma, problema_muita_gente]


# ---------------------------------------------------------------- montagem

def estilo(modo):
    """Classes de cor. modo 'var' usa as variáveis do site; 'claro' e 'escuro' fixam a paleta."""
    linhas = []
    for papel, (var, claro, escuro) in PAPEIS.items():
        cor = {"var": f"var({var}, {claro})", "claro": claro, "escuro": escuro}[modo]
        linhas.append(f".s-{papel}{{stroke:{cor}}} .f-{papel}{{fill:{cor}}}")
    return ("<style>" + " ".join(linhas) +
            " path,line,rect,circle{stroke-linecap:round;stroke-linejoin:round}</style>")


def svg(c, modo="var", marcas=False):
    pref = c["id"]
    grupos = []
    for n, p in enumerate(c["pecas"], 1):
        grupos.append(
            f'<g class="il-peca" id="{pref}-{p["id"]}" data-peca="{n}" tabindex="0" role="button" '
            f'aria-label="{n}. {escape(p["leigo"])}">{p["svg"]}'
            # área de toque invisível ao redor do marcador, para a peça sem traço próprio
            f'<circle cx="{p["marca"][0]}" cy="{p["marca"][1]}" r="44" fill="transparent" class="il-alvo"/></g>')
    mk = ""
    if marcas:
        mk = '<g class="il-marcas" aria-hidden="true">' + "".join(
            f'<g class="il-marca" data-peca="{n}"><circle cx="{p["marca"][0]}" cy="{p["marca"][1]}" r="46"/>'
            f'<text x="{p["marca"][0]}" y="{p["marca"][1]}" dy="0.36em">{n}</text></g>'
            for n, p in enumerate(c["pecas"], 1)) + "</g>"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {c["w"]} {c["h"]}" '
            f'role="img" aria-labelledby="{pref}-t {pref}-d" class="il-svg">'
            f'<title id="{pref}-t">{escape(c["titulo"])}</title><desc id="{pref}-d">{escape(c["alt"])}</desc>'
            f'{estilo(modo)}{"".join(grupos)}{mk}</svg>')


def fragmento(c):
    """Figura para o gerador do site. As caixas são texto real da página, abaixo da imagem.

    Sem JavaScript, as caixas aparecem no modo desnudo, empilhadas. Com JavaScript, tocar numa peça
    abre a caixa dela. O trecho da tese só aparece a partir de Doutrina, pela classe interno.
    """
    pref = c["id"]
    caixas = "".join(
        f'<li class="il-caixa" id="{pref}-caixa-{n}" data-peca="{n}">'
        f'<span class="il-num" aria-hidden="true">{n}</span>'
        f'<p class="il-leigo">{escape(p["leigo"])}</p>'
        + (f'<blockquote class="il-tese interno"><p>{escape(p["tese"])} <span class="pg">(p. {p["pg"]})</span></p></blockquote>' if p.get("tese") else '') +
        f'</li>' for n, p in enumerate(c["pecas"], 1))
    return (f'<figure class="il" data-il="{pref}">\n<div class="il-quadro">{svg(c, "var", marcas=True)}</div>\n'
            f'<ol class="il-caixas">{caixas}</ol>\n</figure>\n')


def exportar(c, pasta):
    for modo, sufixo in (("claro", ""), ("escuro", "-escuro")):
        with tempfile.TemporaryDirectory() as tmp:
            fonte = Path(tmp) / "a.svg"
            png = Path(tmp) / "a.png"
            fonte.write_text(svg(c, modo), encoding="utf-8")
            subprocess.run(["rsvg-convert", "-w", str(c["w"]), "-h", str(c["h"]), "-b", "none",
                            str(fonte), "-o", str(png)], check=True)
            im = Image.open(png).convert("RGBA")
            im.save(pasta / f"{c['id']}{sufixo}.png")
            im.save(pasta / f"{c['id']}{sufixo}.webp", "WEBP", quality=82, method=4)


FUNDOS = [("Informação", "#faf6ef", "#17130f"), ("Doutrina", "#f0f5f9", "#131a23"), ("Ciência", "#f7fbfc", "#121416")]


def prova(feitas, pasta):
    cel = []
    for c in feitas:
        for nome, claro, escuro in FUNDOS:
            for tema, fundo, suf in (("claro", claro, ""), ("escuro", escuro, "-escuro")):
                cel.append(f'<div class="c" style="background:{fundo}"><img src="{c["id"]}{suf}.webp" alt="">'
                           f'<span style="color:{"#000" if tema == "claro" else "#fff"}">{nome} · {tema}</span></div>')
        cel.append(f'<div class="c pq" style="background:#faf6ef"><img src="{c["id"]}.webp" alt="" style="width:320px">'
                   f'<span>320 px</span></div>')
    (pasta / "prova.html").write_text(
        "<!doctype html><meta charset=utf-8><title>Prova das ilustrações SVG</title><style>"
        "body{margin:0;font:12px system-ui;display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}"
        ".c{padding:12px;display:flex;flex-direction:column;gap:6px}.c img{width:100%}</style>" + "".join(cel),
        encoding="utf-8")


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    so = sys.argv[1] if len(sys.argv) > 1 else None
    feitas = []
    for f in COMPOSICOES:
        c = f()
        if so and c["id"] != so:
            continue
        (SAIDA / f"{c['id']}.svg").write_text(svg(c, "var"), encoding="utf-8")
        (SAIDA / f"{c['id']}.html").write_text(fragmento(c), encoding="utf-8")
        (RAIZ / "site" / "ilustracoes-svg").mkdir(exist_ok=True)
        (RAIZ / "site" / "ilustracoes-svg" / f"{c['id']}.html").write_text(fragmento(c), encoding="utf-8")
        exportar(c, SAIDA)
        feitas.append(c)
    (SAIDA / "manifesto.json").write_text(json.dumps(
        [{"id": c["id"], "largura": c["w"], "altura": c["h"], "alt": c["alt"],
          "pecas": [{"n": n, "id": p["id"], "leigo": p["leigo"], "tese": p["tese"], "pagina": p["pg"]}
                    for n, p in enumerate(c["pecas"], 1)]} for c in feitas], ensure_ascii=False, indent=1),
        encoding="utf-8")
    prova(feitas, SAIDA)
    print(f"{len(feitas)} composições em {SAIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
