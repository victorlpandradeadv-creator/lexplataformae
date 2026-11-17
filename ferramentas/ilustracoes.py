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
    trabalhador = (circulo(170, 470, 34, "t1") + linha([(170, 510), (170, 610)], "t1") +
                   linha([(120, 690), (170, 610), (215, 690)], "t1") + linha([(125, 560), (215, 545)], "t1"))
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
    ra = perfil(1120, 420, 1.15, "esq") + circulo(1120, 210, 62, "t2")
    isis = perfil(480, 420, 1.15, "dir")
    nome = (caminho("M600 470 C700 400 900 400 1000 470", "az", larg=10) + circulo(800, 418, 22, "az", cheio=True))
    pecas = [
        dict(id="ra", marca=(1250, 150), svg=ra,
             leigo="Rá, o deus Sol, reinava sobre todos, mas não era invulnerável.",
             tese="Seu interesse é forçar o sol a reconhecer que não é absoluto.",
             pg="792"),
        dict(id="isis", marca=(350, 150), svg=isis,
             leigo="Ísis não queria destruir o Sol. Queria só que ele reconhecesse que não era absoluto.",
             tese="Ao mesmo tempo, Ísis não deseja aniquilar o sol.",
             pg="792"),
        dict(id="nome", marca=(800, 340), svg=nome,
             leigo="Uma vez nomeado, o poder deixa de ser pura presença, que simplesmente está lá, e passa a poder ser chamado, delimitado e obrigado a responder pelo que faz.",
             tese="Uma vez nomeado, o poder deixa de operar como pura presença natural e passa a ser invocável, delimitável e, portanto, obrigado a responder por seus atos.",
             pg="792"),
    ]
    return dict(id="parte-o-nome", w=1600, h=900, titulo="O nome",
                alt="Dois perfis frente a frente, Ísis à esquerda e Rá à direita, com o disco do Sol acima. Entre eles, um vínculo azul com um ponto no meio, o nome.",
                pecas=pecas)


COMPOSICOES = [familia_funcionalidade_cognitiva, familia_infraestrutura_e_intermediacao,
               familia_produtividade_gig_economy, familia_administracao_de_confianca, parte_o_nome]


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
        f'<blockquote class="il-tese interno"><p>{escape(p["tese"])} <span class="pg">(p. {p["pg"]})</span></p></blockquote>'
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
            im.save(pasta / f"{c['id']}{sufixo}.webp", "WEBP", quality=82, method=6)


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
