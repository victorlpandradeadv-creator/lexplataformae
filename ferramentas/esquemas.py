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
CAMPOS_META = {"molde", "modo", "lugar", "titulo", "nota"}


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


MOLDES = {"arvore": _arvore, "fluxo": _fluxo, "colunas": _colunas}


def esquema(ident, prefixo, esc, pg, expansao):
    p = ESQUEMAS.get(ident)
    if not p or p.get("molde") not in MOLDES:
        return ""
    USADOS.add(ident)
    modo = " interno" if p.get("modo") == "doutrina" else ""
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
