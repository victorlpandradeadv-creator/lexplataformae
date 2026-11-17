"""Esquemas didáticos do site, lidos de estrutura/esquemas.md.

Feito em 12/11/2026. Cada esquema é HTML com a gramática comum, e não imagem. O texto quebra
sozinho, herda as cores do tema, entra na tradução inglesa pela memória de segmentos e é lido
por leitor de tela na ordem do raciocínio. A página da tese de cada caixa fica à vista só na
Ciência. No celular, as colunas viram uma coluna só, com as mesmas caixas e as mesmas relações.

O gerador do site chama esquema(ident, prefixo, esc, pg, expansao). Nenhuma frase nasce aqui.
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CAMPOS_META = {"molde", "modo", "lugar", "titulo", "nota", "pagina", "posicao", "rotulos"}


def carregar():
    arq = RAIZ / "estrutura" / "esquemas.md"
    pecas, atual, campo = {}, None, None
    if not arq.exists():
        return pecas
    for linha in arq.read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            atual = pecas.setdefault(linha[3:].strip(), {"grupos": {}, "ancoras": []})
            campo = None
            continue
        if linha.startswith("### ") and atual is not None:
            campo = linha[4:].strip()
            continue
        if atual is None or not campo or not linha.strip():
            continue
        if campo == "ancoras":
            m = re.match(r"^> (.+?) \((p\. [\d\-]+)\)\s*$", linha)
            if m:
                atual["ancoras"].append({"texto": m.group(1), "ref": m.group(2)})
        elif campo in CAMPOS_META:
            atual[campo] = (atual.get(campo, "") + " " + linha.strip()).strip()
        elif linha.startswith("- "):
            partes = [p.strip() for p in linha[2:].split("|")]
            partes += [""] * (3 - len(partes))
            atual["grupos"].setdefault(campo, []).append({"nome": partes[0], "texto": partes[1], "ref": partes[2]})
    return pecas


NUMERAIS = {2: "duas", 3: "três", 4: "quatro", 5: "cinco", 6: "seis"}


def _minuscula(t):
    return t[:1].lower() + t[1:] if t and not t[1:2].isupper() else t


ESQUEMAS = carregar()
USADOS = set()


def _ref(c, prefixo, pg):
    return f'<span class="esq-ref ciencia">{pg(c["ref"], prefixo)}</span>' if c.get("ref") else ""


def _caixa(c, prefixo, esc, pg, classe="", tag="div"):
    texto = f'<span class="esq-texto">{esc(c["texto"])}</span>' if c.get("texto") else ""
    return (f'<{tag} class="esq-caixa{" " + classe if classe else ""}"><span class="esq-nome">{esc(c["nome"])}</span>'
            f'{texto}{_ref(c, prefixo, pg)}</{tag}>')


def _grupo(itens, prefixo, esc, pg, classe=""):
    """A primeira linha do grupo é o cabeçalho da caixa e as demais são os itens dentro dela."""
    if not itens:
        return ""
    cab, resto = itens[0], itens[1:]
    texto = f'<span class="esq-texto">{esc(cab["texto"])}</span>' if cab.get("texto") else ""
    lista = ("<ul>" + "".join(f'<li>{esc(i["nome"])}{_ref(i, prefixo, pg)}</li>' for i in resto) + "</ul>") if resto else ""
    return (f'<div class="esq-caixa{" " + classe if classe else ""}"><span class="esq-nome">{esc(cab["nome"])}</span>'
            f'{texto}{_ref(cab, prefixo, pg)}{lista}</div>')


def _arvore(p, prefixo, esc, pg):
    perguntas = p["grupos"].get("perguntas", [])
    sim = p["grupos"].get("sim", [{}])[0]
    nao = p["grupos"].get("nao", [{}])[0]
    n = len(perguntas)
    partes = []
    for k, q in enumerate(perguntas):
        linha = 2 * k + 1
        partes.append(f'<div class="esq-q" style="grid-row:{linha}">'
                      + _caixa(q, prefixo, esc, pg, "pergunta").replace('<span class="esq-nome">', f'<span class="esq-nome"><span class="esq-num">{k + 1}.</span> ', 1)
                      + '</div>')
        partes.append(f'<div class="esq-lado" style="grid-row:{linha}" aria-hidden="true"><span>não<span class="so-estreito">, vá à última caixa</span></span></div>')
        partes.append(f'<div class="esq-desce" style="grid-row:{linha + 1}" aria-hidden="true"><span>sim</span></div>')
    partes.append(f'<div class="esq-sim-caixa" style="grid-row:{2 * n + 1}">{_caixa(sim, prefixo, esc, pg, "destaque")}</div>')
    partes.append(f'<div class="esq-nao-caixa" style="grid-row:1 / {2 * n}">{_caixa(nao, prefixo, esc, pg, "saida")}</div>')
    leitor = (f'<p class="so-leitor">Responda às {NUMERAIS.get(n, n)} perguntas em ordem. Com sim em todas, {esc(_minuscula(sim.get("nome", "")))}. '
              f'Com um não em qualquer delas, {esc(_minuscula(nao.get("nome", "")))}.</p>')
    return leitor + f'<div class="esq-corpo esq-arvore" style="--esq-n:{n}">{"".join(partes)}</div>'


def _fluxo(p, prefixo, esc, pg):
    portao = p["grupos"].get("portao", [])
    sim = p["grupos"].get("sim", [])
    nao = p["grupos"].get("nao", [])
    campos = "".join(f"<li>{_caixa(c, prefixo, esc, pg, tag='div')}</li>" for c in portao)
    leitor = (f'<p class="so-leitor">Os {NUMERAIS.get(len(portao), len(portao))} campos precisam estar presentes ao mesmo tempo. '
              f'Presentes, {esc(_minuscula(sim[0]["nome"]) if sim else "")}. Faltando um, {esc(_minuscula(nao[0]["nome"]) if nao else "")}.</p>')
    return (leitor + '<div class="esq-corpo esq-fluxo">'
            f'<ol class="esq-portao">{campos}</ol>'
            '<div class="esq-ramos" aria-hidden="true"><span class="esq-ramo sim">todos presentes</span>'
            '<span class="esq-ramo nao">falta um</span></div>'
            '<div class="esq-saidas">'
            '<div><p class="esq-ramo-rotulo so-estreito" aria-hidden="true">todos presentes</p>' + _grupo(sim, prefixo, esc, pg, "destaque") + '</div>'
            '<div><p class="esq-ramo-rotulo so-estreito" aria-hidden="true">falta um</p>' + _grupo(nao, prefixo, esc, pg, "saida") + '</div>'
            '</div></div>')


def _colunas(p, prefixo, esc, pg):
    g = p["grupos"]
    return ('<div class="esq-corpo esq-colunas">'
            + _grupo(g.get("esquerda", []), prefixo, esc, pg, "lado")
            + '<div class="esq-ponte">' + _grupo(g.get("centro", []), prefixo, esc, pg, "atencao") + '</div>'
            + _grupo(g.get("direita", []), prefixo, esc, pg, "lado")
            + '</div>')


def _etapas(p, prefixo, esc, pg):
    """Sequência vertical de etapas. Cada grupo é uma etapa, com cabeçalho e itens, e uma seta leva à seguinte."""
    etapas = [g for g in p["grupos"].values() if g]
    partes = []
    for k, g in enumerate(etapas):
        partes.append(f'<li class="esq-etapa"><span class="esq-etapa-num" aria-hidden="true">{k + 1}</span>{_grupo(g, prefixo, esc, pg, "destaque" if k == 0 else "")}</li>')
    return f'<ol class="esq-corpo esq-etapas">{"".join(partes)}</ol>'


def _grade(p, prefixo, esc, pg):
    """Caixas lado a lado, sem ordem entre elas. A primeira linha de cada grupo é o cabeçalho."""
    grupos = list(p["grupos"].items())
    n = len(grupos)
    return (f'<div class="esq-corpo esq-grade" style="--esq-cols:{min(n, 4)}">'
            + "".join(_grupo(g, prefixo, esc, pg, "destaque" if nome.startswith("destaque") else ("saida" if nome.startswith("saida") else "")) for nome, g in grupos)
            + "</div>")


def _constelacao(p, prefixo, esc, pg):
    """Um centro e satélites dos dois lados, cada um ligado ao centro por um traço."""
    centro = p["grupos"].get("centro", [])
    sats = p["grupos"].get("satelites", [])
    meio = (len(sats) + 1) // 2
    esq, dir_ = sats[:meio], sats[meio:]
    col = lambda itens, lado: (f'<ul class="esq-sats {lado}">' + "".join(f'<li>{_caixa(c, prefixo, esc, pg)}</li>' for c in itens) + "</ul>")
    return ('<div class="esq-corpo esq-constelacao">' + col(esq, "esq") + f'<div class="esq-centro">{_grupo(centro, prefixo, esc, pg, "destaque")}</div>'
            + col(dir_, "dir") + "</div>")


def _camadas(p, prefixo, esc, pg):
    """Faixas empilhadas, de cima para baixo. Cada grupo é uma faixa, com o nome à esquerda e o conteúdo à direita."""
    faixas = []
    for k, (nome, g) in enumerate(p["grupos"].items()):
        if not g:
            continue
        cab, resto = g[0], g[1:]
        itens = "".join(f'<li>{esc(i["nome"])}{(": " if False else "")}{_ref(i, prefixo, pg)}</li>' for i in resto)
        texto = f'<span class="esq-texto">{esc(cab["texto"])}</span>' if cab.get("texto") else ""
        faixas.append(f'<div class="esq-faixa{" destaque" if nome.startswith("destaque") else ""}"><div class="esq-faixa-nome"><span class="esq-nome">{esc(cab["nome"])}</span>{_ref(cab, prefixo, pg)}</div>'
                      f'<div class="esq-faixa-corpo">{texto}{("<ul>" + itens + "</ul>") if itens else ""}</div></div>')
    return f'<div class="esq-corpo esq-camadas">{"".join(faixas)}</div>'


def _comparacao(p, prefixo, esc, pg):
    """Linhas por dimensão, com a coluna do antes e a do depois. Cada linha é 'dimensão | antes | depois'."""
    rot = [x.strip() for x in p.get("rotulos", "Antes|Depois").split("|")]
    linhas = p["grupos"].get("linhas", [])
    cab = f'<div class="esq-cmp-cab" aria-hidden="true"><span></span><span>{esc(rot[0])}</span><span>{esc(rot[1])}</span></div>'
    corpo = "".join(f'<div class="esq-cmp-linha"><span class="esq-cmp-dim">{esc(l["nome"])}</span>'
                    f'<span class="esq-caixa"><span class="so-leitor">{esc(rot[0])}. </span>{esc(l["texto"])}</span>'
                    f'<span class="esq-caixa destaque"><span class="so-leitor">{esc(rot[1])}. </span>{esc(l["ref"])}</span></div>' for l in linhas)
    return f'<div class="esq-corpo esq-comparacao">{cab}{corpo}</div>'


def _ligacoes(p, prefixo, esc, pg):
    """Cada linha liga uma perda às respostas que podem atendê-la. Grupo 'linhas', com 'perda | resposta; resposta* | p. n'.
    A resposta marcada com * aparece em destaque."""
    rot = [x.strip() for x in p.get("rotulos", "|").split("|")]
    linhas = p["grupos"].get("linhas", [])
    cab = f'<div class="esq-lig-cab" aria-hidden="true"><span>{esc(rot[0])}</span><span>{esc(rot[1] if len(rot) > 1 else "")}</span></div>'
    def chips(t):
        out = []
        for r in [x.strip() for x in t.split(";") if x.strip()]:
            d = r.endswith("*")
            out.append(f'<li class="esq-chip{" destaque" if d else ""}">{esc(r.rstrip("*").strip())}</li>')
        return "<ul class=\"esq-chips\">" + "".join(out) + "</ul>"
    corpo = "".join(f'<div class="esq-lig-linha"><span class="esq-caixa esq-lig-perda"><span class="esq-nome">{esc(l["nome"])}</span></span>'
                    f'<span class="esq-lig-seta" aria-hidden="true"></span>{chips(l["texto"])}</div>' for l in linhas)
    return f'<div class="esq-corpo esq-ligacoes">{cab}{corpo}</div>'


def _portas(p, prefixo, esc, pg):
    """Uma origem que se abre em portas, e uma faixa comum embaixo que atravessa as portas."""
    g = p["grupos"]
    origem = _grupo(g.get("origem", []), prefixo, esc, pg, "destaque")
    portas = "".join(f'<li>{_caixa(c, prefixo, esc, pg)}</li>' for c in g.get("portas", []))
    comum = _grupo(g.get("comum", []), prefixo, esc, pg, "atencao")
    n = len(g.get("portas", []))
    return (f'<div class="esq-corpo esq-portas" style="--esq-cols:{n}"><div class="esq-origem">{origem}</div>'
            f'<div class="esq-leque" aria-hidden="true">{"<span></span>" * n}</div><ul class="esq-portas-lista">{portas}</ul>'
            f'<div class="esq-comum">{comum}</div></div>')


def _trilhas(p, prefixo, esc, pg):
    """Colunas paralelas, cada uma uma lista ordenada. A primeira linha do grupo é o nome da coluna."""
    cols = []
    for g in p["grupos"].values():
        if not g:
            continue
        cab, resto = g[0], g[1:]
        texto = f'<span class="esq-texto">{esc(cab["texto"])}</span>' if cab.get("texto") else ""
        cols.append(f'<div class="esq-caixa esq-trilha"><span class="esq-nome">{esc(cab["nome"])}</span>{texto}{_ref(cab, prefixo, pg)}'
                    f'<ol>' + "".join(f'<li>{esc(i["nome"])}{(" <span class=" + chr(34) + "esq-texto" + chr(34) + ">" + esc(i["texto"]) + "</span>") if i.get("texto") else ""}{_ref(i, prefixo, pg)}</li>' for i in resto) + "</ol></div>")
    return f'<div class="esq-corpo esq-trilhas" style="--esq-cols:{len(cols)}">{"".join(cols)}</div>'


MOLDES = {"arvore": _arvore, "fluxo": _fluxo, "colunas": _colunas, "etapas": _etapas, "grade": _grade, "constelacao": _constelacao,
          "camadas": _camadas, "comparacao": _comparacao, "ligacoes": _ligacoes, "portas": _portas, "trilhas": _trilhas}


def inserir(corpo, caminho, prefixo, esc, pg, expansao):
    """Põe na página os esquemas cujo campo pagina é este caminho. A posição é 'antes <texto de título>', 'depois <texto de título>'
    ou, sem posição, antes das saídas. Esquemas chamados pelo próprio gerador não usam esse campo."""
    for ident, p in ESQUEMAS.items():
        # Esquema sem página é chamado pelo próprio gerador. Sem esta guarda ele caía na capa, cujo caminho é vazio.
        if not p.get("pagina", "").strip() or p["pagina"].strip() != caminho:
            continue
        peca = esquema(ident, prefixo, esc, pg, expansao)
        pos = p.get("posicao", "")
        modo, _, alvo = pos.partition(" ")
        feito = False
        if alvo:
            achados = list(re.finditer(r"<h[23][^>]*>", corpo))
            for k, m in enumerate(achados):
                fim = corpo.find("</h", m.end())
                texto = re.sub(r"<[^>]+>", "", corpo[m.end():fim])
                if alvo.lower() in texto.lower():
                    if modo == "antes":
                        ini = corpo.rfind("<section", 0, m.start())
                        ini = ini if ini >= 0 and corpo.find("</section>", ini) > m.start() and corpo.find("<section", ini + 1, m.start()) < 0 else m.start()
                        corpo = corpo[:ini] + peca + corpo[ini:]
                    else:
                        fecha = corpo.find("</section>", m.end())
                        prox = achados[k + 1].start() if k + 1 < len(achados) else len(corpo)
                        alvo_pos = fecha + len("</section>") if 0 <= fecha < prox else prox
                        corpo = corpo[:alvo_pos] + peca + corpo[alvo_pos:]
                    feito = True
                    break
            if not feito:
                raise SystemExit(f"Esquema {ident}: título '{alvo}' não encontrado em {caminho}")
        if not feito:
            k = corpo.find('<nav class="ext saidas"')
            k = k if k >= 0 else corpo.rfind("</article>")
            corpo = corpo[:k] + peca + corpo[k:]
    return corpo



def esquema(ident, prefixo, esc, pg, expansao):
    p = ESQUEMAS.get(ident)
    if not p or p.get("molde") not in MOLDES:
        return ""
    USADOS.add(ident)
    modo = {"doutrina": " interno", "ciencia": " ciencia"}.get(p.get("modo"), "")
    tid = f"esquema-{ident}"
    nota = ""
    if p.get("nota"):
        m = re.match(r"^(.*?)\s*\((p\. [\d\-]+)\)\s*$", p["nota"])
        texto, ref = (m.group(1), m.group(2)) if m else (p["nota"], "")
        nota = f'<p class="esq-nota">{esc(texto)}.{(" " + _ref({"ref": ref}, prefixo, pg)) if ref else ""}</p>'
    return (f'<figure class="esquema esquema-{p["molde"]}{modo}" id="{tid}" aria-labelledby="{tid}-titulo" '
            f'data-arq="esquema · {esc(ident)}">'
            f'<figcaption class="esq-titulo" id="{tid}-titulo">{esc(p.get("titulo", ""))}</figcaption>'
            + MOLDES[p["molde"]](p, prefixo, esc, pg)
            + nota + expansao(p["ancoras"], prefixo)
            + '</figure>')
