"""Segmentação do HTML gerado em docs/ para a tradução inglesa.

Um segmento é o conteúdo interno de um bloco folha (sem blocos dentro),
ou uma sequência de nós em linha dentro de um bloco misto. A chave é o
HTML interno exato. As etiquetas em linha ficam no segmento e precisam
voltar iguais na tradução.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag, Comment, Doctype, Declaration, ProcessingInstruction

RAIZ = Path(__file__).resolve().parents[2]
DOCS = RAIZ / "docs"

BLOCOS = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "dt", "dd", "td", "th", "figcaption", "caption",
          "summary", "label", "button", "blockquote", "legend", "title", "option", "div", "section", "article",
          "aside", "nav", "header", "footer", "main", "ul", "ol", "dl", "table", "tr", "thead", "tbody", "figure",
          "details", "form", "fieldset", "body", "html", "head", "pre"}
PULAR = {"script", "style", "noscript", "svg", "code", "iframe", "template"}
ATRIBUTOS = ("title", "aria-label", "alt", "placeholder", "data-arq", "data-titulo", "aria-description")
META = {"description", "og:title", "og:description", "twitter:title", "twitter:description", "og:image:alt"}
LETRA = re.compile(r"[A-Za-zÀ-ÿ]{2,}")


def tem_texto(s):
    t = re.sub(r"<[^>]+>", " ", s)
    t = re.sub(r"&[a-z#0-9]+;", " ", t)
    return bool(LETRA.search(t))


def chave(s):
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:16]


def tem_bloco(el):
    return any(isinstance(d, Tag) and d.name in BLOCOS for d in el.descendants)


def unidades(el):
    """Rende (lista de nós, eh_inteiro) para cada segmento sob el."""
    if not isinstance(el, Tag) or el.name in PULAR:
        return
    if not tem_bloco(el):
        if el.name in BLOCOS:
            yield el, None
        return
    corrida = []
    for filho in list(el.children):
        if isinstance(filho, (Comment, Doctype, Declaration, ProcessingInstruction)):
            continue
        if isinstance(filho, Tag) and (filho.name in BLOCOS or filho.name in PULAR or tem_bloco(filho)):
            if corrida:
                yield el, corrida
                corrida = []
            yield from unidades(filho)
        else:
            corrida.append(filho)
    if corrida:
        yield el, corrida


def html_de(nos):
    return "".join(str(n) for n in nos)


def interno(el):
    return el.decode_contents()


def segmentos_da_pagina(sopa):
    """Lista de (tipo, texto) traduzíveis."""
    saida = []
    for el, corrida in unidades(sopa):
        s = interno(el) if corrida is None else html_de(corrida)
        if s.strip() and tem_texto(s):
            saida.append(("html", s.strip()))
    for el in sopa.find_all(True):
        if el.name in PULAR:
            continue
        for a in ATRIBUTOS:
            v = el.get(a)
            if isinstance(v, str) and tem_texto(v):
                saida.append(("attr", v.strip()))
        if el.name == "meta" and (el.get("name") in META or el.get("property") in META):
            v = el.get("content", "")
            if tem_texto(v):
                saida.append(("attr", v.strip()))
    for sc in sopa.find_all("script", type="application/ld+json"):
        try:
            dado = json.loads(sc.string or "")
        except Exception:
            continue
        for v in textos_jsonld(dado):
            saida.append(("attr", v))
    return saida


CAMPOS_LD = {"name", "description", "headline", "alternativeName", "text", "abstract", "about", "inDefinedTermSet_name", "keywords"}


def textos_jsonld(d):
    if isinstance(d, dict):
        for k, v in d.items():
            if k in CAMPOS_LD and isinstance(v, str) and tem_texto(v):
                yield v.strip()
            else:
                yield from textos_jsonld(v)
    elif isinstance(d, list):
        for v in d:
            yield from textos_jsonld(v)


def paginas(tese=None):
    for p in sorted(DOCS.rglob("*.html")):
        rel = p.relative_to(DOCS).as_posix()
        if rel.startswith("en/"):
            continue
        e_tese = rel.startswith("tese/")
        if tese is None or tese == e_tese:
            yield p, rel


if __name__ == "__main__":
    grupo = sys.argv[1] if len(sys.argv) > 1 else "site"
    unicos = {}
    for p, rel in paginas(tese=(grupo == "tese")):
        sopa = BeautifulSoup(p.read_text(encoding="utf-8"), "lxml")
        for tipo, s in segmentos_da_pagina(sopa):
            k = chave(s)
            if k not in unicos:
                unicos[k] = {"k": k, "tipo": tipo, "pt": s, "pagina": rel}
    lista = list(unicos.values())
    palavras = sum(len(re.sub(r"<[^>]+>", " ", x["pt"]).split()) for x in lista)
    print(grupo, len(lista), "segmentos", palavras, "palavras")
    saida = RAIZ / "traducao" / f"segmentos-{grupo}.json"
    saida.parent.mkdir(exist_ok=True)
    saida.write_text(json.dumps(lista, ensure_ascii=False, indent=0), encoding="utf-8")
