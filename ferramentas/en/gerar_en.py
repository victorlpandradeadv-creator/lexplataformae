"""Gera a versão inglesa do site em docs/en/, a partir das páginas portuguesas já geradas em docs/.

Uso
    python3 ferramentas/gerar_site.py     # gera docs/ e chama este script no fim
    python3 ferramentas/en/gerar_en.py    # sozinho, se docs/ já estiver gerado

Cada segmento traduzível da página portuguesa é trocado pela tradução guardada em
traducao/saida/*.jsonl, pela chave do HTML interno exato. Segmento sem tradução fica
em português e entra no relatório traducao/faltam.json, que lotes.py transforma em
novos lotes. Nenhum texto em inglês nasce aqui, salvo os avisos de tradução abaixo.

Os trechos literais da tese e os textos de lei ganham a marca PT, que abre o original
em português. As páginas do texto integral abrem com o aviso de tradução por máquina.
As páginas portuguesas ganham o link para a versão inglesa e as marcas hreflang.
"""
import copy
import html
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

sys.path.insert(0, str(Path(__file__).parent))
from marcas import marcar, desmarcar, assinatura
from segmentos import unidades, interno, html_de, tem_texto, chave, ATRIBUTOS, META, textos_jsonld, CAMPOS_LD

RAIZ = Path(__file__).resolve().parents[2]
DOCS = RAIZ / "docs"
EN = DOCS / "en"
BASE = "https://lexplataformae.com.br"
T = RAIZ / "traducao"

# Avisos próprios da versão inglesa. Acréscimo posterior de 10/11/2026.
AVISO_TESE = ("This is a machine translation of the thesis, produced for this site and not reviewed by the author. "
              "The Portuguese original is the authoritative text.")
ROTULO_PT = "PT"
TITULO_PT = "Free translation. Show the Portuguese original"
TITULO_PT_LEI = "Unofficial translation. Show the Portuguese original"
ARQUIVOS_SUBIR = ("assets/", "dados/", "fontes/")


def memoria():
    mem = {}
    for arq in sorted((T / "saida").glob("*.jsonl")):
        for linha in arq.read_text(encoding="utf-8").splitlines():
            if linha.strip():
                d = json.loads(linha)
                mem[d["k"]] = d["en"]
    return mem


MEM = memoria()
FALTAM = {}


VERSAO_DA_MEMORIA = "0.11"
VERSAO_ATUAL = re.search(r'VERSAO = "([^"]+)"', (RAIZ / "ferramentas" / "gerar_site.py").read_text(encoding="utf-8")).group(1)
VERSAO_RE = re.compile(r"(?<=[Vv]ersão )(0\.\d+)")


def traduz_html(s, pagina):
    """A memória guarda as frases com a versão em que foram traduzidas. A versão atual entra de volta depois."""
    s = s.strip()
    atual = VERSAO_RE.search(s)
    if atual and atual.group(1) == VERSAO_ATUAL and VERSAO_ATUAL != VERSAO_DA_MEMORIA:
        t = traduz_html(VERSAO_RE.sub(VERSAO_DA_MEMORIA, s), pagina)
        return None if t is None else re.sub(r"(?<=[Vv]ersion )" + re.escape(VERSAO_DA_MEMORIA), atual.group(1), t)
    k = chave(s)
    en = MEM.get(k)
    if en is None:
        FALTAM.setdefault(k, {"k": k, "tipo": "html", "pt": s, "pagina": pagina})
        return None
    marcado, mapa = marcar(s)
    if assinatura(en) != assinatura(marcado):
        FALTAM.setdefault(k, {"k": k, "tipo": "html", "pt": s, "pagina": pagina})
        return None
    return desmarcar(en, mapa)


def traduz_attr(v, pagina):
    v2 = v.strip()
    if not tem_texto(v2):
        return v
    en = MEM.get(chave(v2))
    if en is None:
        FALTAM.setdefault(chave(v2), {"k": chave(v2), "tipo": "attr", "pt": v2, "pagina": pagina})
        return v
    return en


def fragmento(h):
    return list(BeautifulSoup(f"<div>{h}</div>", "html.parser").div.contents)


def texto_plano(el):
    c = copy.copy(el)
    for x in c.select(".pg, .nota-ref, .pg-marca, .cita-sinal, .lei-ref, sup"):
        x.decompose()
    return re.sub(r"\s+", " ", c.get_text(" ")).strip()


def e_pagina(alvo):
    """O destino relativo à raiz de docs/ é página (espelhada em en/) ou arquivo?"""
    alvo = alvo.split("#")[0].split("?")[0]
    if alvo.startswith(ARQUIVOS_SUBIR):
        return False
    if alvo == "" or alvo.endswith("/") or alvo.endswith(".html"):
        return True
    return not re.search(r"\.[a-z0-9]{2,5}$", alvo)


def resolve(rel_pagina, url):
    """Caminho do destino em relação à raiz de docs/."""
    base = rel_pagina.rsplit("/", 1)[0].split("/") if "/" in rel_pagina else []
    partes = base[:]
    for p in url.split("/"):
        if p == "..":
            if partes:
                partes.pop()
        elif p and p != ".":
            partes.append(p)
    fim = "/" if url.endswith("/") or url.split("#")[0].endswith("/") else ""
    return "/".join(partes) + fim


def ajusta_link(url, rel_pagina):
    if not url or url.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return url
    if url.startswith(BASE):
        resto = url[len(BASE):]
        caminho = resto.lstrip("/")
        return BASE + "/en/" + caminho if e_pagina(caminho) else url
    if re.match(r"^[a-z]+://", url):
        return url
    if url.startswith("/"):
        return "/en" + url if e_pagina(url.lstrip("/")) else url
    alvo = resolve(rel_pagina, url)
    if e_pagina(alvo):
        return url
    frag = "#" + url.split("#", 1)[1] if "#" in url else ""
    return prefixo_raiz(rel_pagina) + "../" + alvo.split("#")[0] + frag


def url_publica(rel):
    return BASE + "/" + (rel[:-len("index.html")] if rel.endswith("index.html") else rel)


def traduz_jsonld(d, pagina):
    if isinstance(d, dict):
        for k, v in list(d.items()):
            if k in CAMPOS_LD and isinstance(v, str) and tem_texto(v):
                d[k] = traduz_attr(v, pagina)
            elif k == "inLanguage" and v == "pt-BR":
                d[k] = "en"
            elif k in ("url", "@id", "isBasedOn", "mainEntityOfPage") and isinstance(v, str) and v.startswith(BASE):
                d[k] = ajusta_link(v, pagina)
            else:
                traduz_jsonld(v, pagina)
    elif isinstance(d, list):
        for v in d:
            traduz_jsonld(v, pagina)


def marca_original(bq, pt, lei=False):
    det = BeautifulSoup("", "html.parser").new_tag("details")
    det["class"] = ["original"]
    det["lang"] = "pt-BR"
    sm = BeautifulSoup("", "html.parser").new_tag("summary")
    sm["title"] = TITULO_PT_LEI if lei else TITULO_PT
    sm["aria-label"] = TITULO_PT_LEI if lei else TITULO_PT
    sm["lang"] = "en"
    sm.string = ROTULO_PT
    det.append(sm)
    p = BeautifulSoup("", "html.parser").new_tag("span")
    p["class"] = ["original-texto"]
    p.string = pt
    det.append(p)
    bq.append(det)


def link_idioma(sopa, href, rotulo, lang):
    topo = sopa.select_one("header.topo")
    if not topo:
        return
    if topo.select_one("a.idioma"):
        topo.select_one("a.idioma").decompose()
    a = sopa.new_tag("a", href=href)
    a["class"] = ["idioma"]
    a["hreflang"] = lang
    a["lang"] = lang
    a.string = rotulo
    topo.append(a)


def alternativas(sopa, rel):
    cab = sopa.head
    if not cab:
        return
    for l in cab.select('link[rel="alternate"][hreflang]'):
        l.decompose()
    pt, en = url_publica(rel), BASE + "/en/" + url_publica(rel)[len(BASE) + 1:]
    for lang, href in (("pt-BR", pt), ("en", en), ("x-default", pt)):
        l = sopa.new_tag("link", rel="alternate", href=href)
        l["hreflang"] = lang
        cab.append(l)


def prefixo_raiz(rel):
    return "../" * rel.count("/")


def traduz_pagina(arq, rel):
    fonte = arq.read_text(encoding="utf-8")
    sopa = BeautifulSoup(fonte, "lxml")
    for velho in sopa.select("a.idioma, link[hreflang], link[href$='en.css']"):
        velho.decompose()
    # Os originais dos trechos literais, antes da tradução
    originais = []
    for bq in sopa.select("blockquote.citacao, .lei-texto"):
        originais.append((bq, texto_plano(bq), "lei-texto" in (bq.get("class") or [])))
    # Segmentos em HTML
    for el, corrida in list(unidades(sopa)):
        s = interno(el) if corrida is None else html_de(corrida)
        if not s.strip() or not tem_texto(s):
            continue
        t = traduz_html(s, rel)
        if t is None:
            continue
        novos = fragmento(t)
        if corrida is None:
            el.clear()
            for n in novos:
                el.append(n)
        else:
            primeiro = corrida[0]
            for n in novos:
                primeiro.insert_before(n)
            for n in corrida:
                n.extract()
    # Atributos e metadados
    for el in sopa.find_all(True):
        for a in ATRIBUTOS:
            v = el.get(a)
            if isinstance(v, str) and tem_texto(v):
                el[a] = traduz_attr(v, rel)
        if el.name == "meta" and (el.get("name") in META or el.get("property") in META):
            el["content"] = traduz_attr(el.get("content", ""), rel)
        if el.name == "meta" and el.get("property") == "og:locale":
            el["content"] = "en_US"
        for a in ("href", "src", "action", "data-superficie", "poster"):
            v = el.get(a)
            if isinstance(v, str):
                el[a] = ajusta_link(v, rel)
        if el.has_attr("srcset"):
            el["srcset"] = ", ".join(" ".join([ajusta_link(p.split()[0], rel)] + p.split()[1:]) for p in el["srcset"].split(","))
    for sc in sopa.find_all("script", type="application/ld+json"):
        try:
            d = json.loads(sc.string or "")
        except Exception:
            continue
        traduz_jsonld(d, rel)
        sc.string = json.dumps(d, ensure_ascii=False)
    # Endereços públicos que aparecem como texto, como na citação sugerida
    for no in sopa.find_all(string=re.compile(re.escape(BASE) + r"/")):
        if no.parent.name in ("script", "style"):
            continue
        novo = re.sub(re.escape(BASE) + r"/(?!en/)([^\s<\"']*)", lambda m: BASE + "/en/" + m.group(1) if e_pagina(m.group(1)) else m.group(0), str(no))
        no.replace_with(novo)
    # Marca dos originais
    for bq, pt, lei in originais:
        if pt and texto_plano(bq) != pt:
            alvo = bq.find("p", recursive=False) if bq.name == "blockquote" and bq.find("p", recursive=False) else bq
            marca_original(alvo, pt, lei)
    html_el = sopa.html
    html_el["lang"] = "en"
    if rel.startswith("tese/"):
        conteudo = sopa.select_one("#conteudo-principal") or sopa.select_one("main") or sopa.body
        aviso = sopa.new_tag("p")
        aviso["class"] = ["aviso-traducao"]
        aviso.append(AVISO_TESE + " ")
        a = sopa.new_tag("a", href=prefixo_raiz(rel) + "../" + rel.replace("index.html", ""), hreflang="pt-BR", lang="pt-BR")
        a.string = "Ler em português"
        aviso.append(a)
        aviso.append(".")
        conteudo.insert(0, aviso)
    # Estilo dos acréscimos ingleses
    if sopa.head and not sopa.head.select_one('link[href$="en.css"]'):
        estilo = sopa.select_one('link[rel="stylesheet"]')
        if estilo:
            l = sopa.new_tag("link", rel="stylesheet", href=estilo["href"].replace("estilo.css", "en.css"))
            estilo.insert_after(l)
    alternativas(sopa, rel)
    volta = prefixo_raiz(rel) + "../" + rel.replace("index.html", "")
    link_idioma(sopa, volta, "Português", "pt-BR")
    return str(sopa)


def marca_portugues(arq, rel):
    sopa = BeautifulSoup(arq.read_text(encoding="utf-8"), "lxml")
    alternativas(sopa, rel)
    link_idioma(sopa, prefixo_raiz(rel) + "en/" + rel.replace("index.html", ""), "English", "en")
    if sopa.head and not sopa.head.select_one('link[href$="en.css"]'):
        estilo = sopa.select_one('link[rel="stylesheet"]')
        if estilo:
            estilo.insert_after(sopa.new_tag("link", rel="stylesheet", href=estilo["href"].replace("estilo.css", "en.css")))
    arq.write_text(str(sopa), encoding="utf-8")


def sitemap():
    arq = DOCS / "sitemap.xml"
    urls = re.findall(r"<loc>([^<]+)</loc>", arq.read_text(encoding="utf-8"))
    linhas = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for u in urls:
        en = BASE + "/en/" + u[len(BASE) + 1:]
        alt = (f'<xhtml:link rel="alternate" hreflang="pt-BR" href="{u}"/>'
               f'<xhtml:link rel="alternate" hreflang="en" href="{en}"/>')
        linhas.append(f"  <url><loc>{u}</loc>{alt}</url>")
        linhas.append(f"  <url><loc>{en}</loc>{alt}</url>")
    linhas.append("</urlset>")
    arq.write_text("\n".join(linhas) + "\n", encoding="utf-8")


CSS = """/* Acréscimos da versão inglesa e do link de idioma. 10/11/2026. */
.topo a.idioma { font-size: 0.8125rem; font-weight: 500; text-decoration: none; color: var(--texto-2, inherit); opacity: .8; margin-left: auto; padding: .25rem .5rem; border: 1px solid currentColor; border-radius: 2px; white-space: nowrap; align-self: center; }
.topo a.idioma:hover, .topo a.idioma:focus-visible { opacity: 1; }
details.original { display: inline-block; margin-left: .35em; vertical-align: baseline; }
details.original:not([open]) { white-space: nowrap; }
details.original > summary { display: inline-block; list-style: none; cursor: pointer; font-family: "IBM Plex Mono", monospace; font-size: .6875rem; letter-spacing: .04em; line-height: 1; padding: .15em .35em; border: 1px solid currentColor; border-radius: 2px; opacity: .65; vertical-align: .15em; }
details.original > summary::-webkit-details-marker { display: none; }
details.original > summary:hover, details.original > summary:focus-visible { opacity: 1; }
details.original[open] { display: block; margin: .6em 0 0; }
details.original .original-texto { display: block; margin-top: .4em; font-size: .9em; opacity: .85; font-style: normal; }
.aviso-traducao { font-size: .875rem; padding: .75rem 1rem; border: 1px solid currentColor; border-radius: 2px; margin: 0 0 1.5rem; opacity: .85; }
@media print { details.original > summary { display: none; } details.original .original-texto { display: block; } }
"""


def main():
    if EN.exists():
        import shutil
        shutil.rmtree(EN)
    paginas = [(p, p.relative_to(DOCS).as_posix()) for p in sorted(DOCS.rglob("*.html"))]
    (DOCS / "assets" / "en.css").write_text(CSS, encoding="utf-8")
    for arq, rel in paginas:
        saida = EN / rel
        saida.parent.mkdir(parents=True, exist_ok=True)
        saida.write_text(traduz_pagina(arq, rel), encoding="utf-8")
    for arq, rel in paginas:
        marca_portugues(arq, rel)
    sitemap()
    (T / "faltam.json").write_text(json.dumps(list(FALTAM.values()), ensure_ascii=False, indent=0), encoding="utf-8")
    palavras = sum(len(re.sub(r"<[^>]+>", " ", x["pt"]).split()) for x in FALTAM.values())
    print(f"{len(paginas)} páginas em docs/en/. Segmentos sem tradução {len(FALTAM)}, {palavras} palavras.")


if __name__ == "__main__":
    main()
