"""Mede, por página e por modo, a voz do site e o texto literal da tese, e confere as metas da revisão de voz de 05/11/2026.

Uso
    python3 ferramentas/medir_voz.py [docs]             # relatório
    python3 ferramentas/medir_voz.py docs --estrito     # sai com erro se alguma meta falhar
    python3 ferramentas/medir_voz.py docs --pagina roteiro/   # blocos de uma página, modo a modo

O texto integral fica fora, porque é a própria tese. As páginas de autor são catálogo e só valem para a Ciência.
"""
import collections
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

VAZIOS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
BLOCOS = {"h1", "h2", "h3", "h4", "p", "li", "dd", "dt", "blockquote", "figcaption"}
LITERAL = {"citacao", "citacao-longa", "canonica", "frase", "campo-def", "texto", "ficha", "titulo-tese", "notas", "quadro-literal"}
LEI = {"lei-texto", "leis-pagina", "artigos", "lei-oficial"}
ROTULOS = {"rotulo-ext", "rotulo-fonte", "sobrelinha", "sobrelinha-ext", "direito-titulo", "titulo-tese"}
FORA = {"fonte-par", "lateral", "lei-nota", "balao-ref", "ilustracao"}
TIRAR = {"pg", "pg-marca", "nota-ref", "lei-ref", "so-leitor", "balao-ref", "cita-sinal"}

# Limites da revisão de voz.
MAX_LITERAL_DOUTRINA = 15
MAX_PALAVRAS_CITACAO = 55
MAX_PAGINAS_CITACAO = 2
MAX_LINKS_TESE = 1
MAX_SEQUENCIA = 2

IMPERATIVO = re.compile(r"\b(Pense|Imagine|imagine|Repare|repare|Veja|Olhe|Suponha|Perceba|Considere|Lembre-se)\b")
TEORIA_IDEIA = re.compile(r"\b([Aa] ideia de Objeto|[Nn]ove ideias|[Ee]stas ideias|[Ee]ssa ideia|[Dd]essa ideia|[Dd]a ideia inteira|[Aa] ideia inteira|[Oo]utra ideia|[Aa]s ideias|[Vv]olte às ideias|Isso tem nome|[Tt]em nome,|[ÉE] o nome desse)\b")
ANAFORA = re.compile(r"^(\[\.\.\.\]|\[…\]|Ess[ae]s?\b|Est[ae]s?\b|Isso\b|Isto\b|Por isso\b|Assim\b|Daí\b|Nesse\b|Nessa\b|Neste\b|Nesta\b|Tal\b|Tais\b|Dessa\b|Desse\b|Desta\b|Deste\b|Ele\b|Ela\b|Eles\b|Elas\b|Portanto\b|Logo\b|Contudo\b|Porém\b|Entretanto\b|Todavia\b|Além disso\b|Por outro lado\b|Com isso\b|Aqui\b|Ali\b|O mesmo\b|A mesma\b|Também\b|Mais\b|Por sua vez\b|Em seguida\b|Só então\b|Fixad[oa]\b|A partir dessa\b|Sob essa\b|Nessa\b)")
PROPRIO_TEXTO = re.compile(r"\b(esta tese|presente tese|nesta tese|para esta tese|a tese|presente trabalho|neste trabalho|este trabalho|presente pesquisa|esta pesquisa|nesta pesquisa|presente investigação|esta investigação|nesta seção|esta seção|presente seção|seção seguinte|subseção|neste capítulo|este capítulo|capítulo \d|seção \d|[Aa] (primeira|segunda|terceira|quarta|quinta|sexta|sétima|oitava) seção|presente sistematização|sistematização|anteriormente|acima(?! d[oa]s?\b)|adiante|a seguir|como visto|como se viu|até aqui|passo seguinte|ora denominad\w+|doravante|mobilizad\w+|o que se afirma|sustenta-se|propõe-se|defende-se|adota-se|em chave|nessa chave|sob essa chave|nesse registro|nesse ponto|\d\.\d\.\d)\b")
TESE_NA_PROSA = re.compile(r"\b[Tt]eses?\b")


class No:
    __slots__ = ("tag", "classes", "pai", "filhos", "href", "num")

    def __init__(self, tag, classes, pai, href=None):
        self.tag, self.classes, self.pai, self.href = tag, classes, pai, href
        self.filhos = []

    def linha(self):
        n = self
        while n is not None:
            yield n
            n = n.pai


class Leitor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.raiz = No("#", set(), None)
        self.pilha = [self.raiz]
        self.minimo = 0
        self.pular = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "body":
            self.minimo = int(a.get("data-minimo") or 0)
        if tag in ("script", "style"):
            self.pular += 1
            return
        no = No(tag, set((a.get("class") or "").split()), self.pilha[-1], a.get("href"))
        self.pilha[-1].filhos.append(no)
        if tag not in VAZIOS:
            self.pilha.append(no)

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.pular = max(0, self.pular - 1)
            return
        if not any(n.tag == tag for n in self.pilha[1:]):
            return
        while self.pilha[-1].tag != tag:
            self.pilha.pop()
        self.pilha.pop()

    def handle_data(self, data):
        if not self.pular:
            self.pilha[-1].filhos.append(data)


def visivel(classes, modo):
    if "interno" in classes and modo == 0:
        return False
    if classes & {"arq", "ciencia"} and modo != 2:
        return False
    if "em-modo" in classes and f"modo-{modo}" not in classes:
        return False
    return True


def expansao_oculta(no, modo):
    """A expansão cujos trechos todos ficaram só na Ciência some fora dela."""
    if "expansao" not in no.classes or modo == 2:
        return False
    bqs = [f for f in no.filhos if isinstance(f, No) and f.tag == "blockquote"]
    return bool(bqs) and all("ciencia" in b.classes for b in bqs)


def texto(no, modo):
    partes = []
    for f in no.filhos:
        if isinstance(f, str):
            partes.append(f)
        elif visivel(f.classes, modo) and not f.classes & TIRAR and f.tag != "sup":
            partes.append(texto(f, modo))
    return "".join(partes)


def varrer(no, modo, saida, literal=False, lei=False, links=None):
    for f in no.filhos:
        if isinstance(f, str):
            continue
        if not visivel(f.classes, modo) or f.classes & FORA or f.tag == "nav" and "saidas" not in f.classes or expansao_oculta(f, modo):
            if f.tag == "nav" and visivel(f.classes, modo) and not f.classes & FORA:
                varrer_links(f, modo, links)
            continue
        if f.tag == "a" and f.href is not None:
            links.append((f.href, f.classes))
        lit = literal or bool(f.classes & LITERAL) or (f.tag == "blockquote" and not f.classes & LEI)
        le = lei or bool(f.classes & LEI)
        if f.tag in BLOCOS and not (f.tag in ("li", "dd") and any(isinstance(x, No) and x.tag in ("p", "blockquote", "ul", "ol", "dl") for x in f.filhos)):
            if not f.classes & TIRAR:
                t = re.sub(r"\s+", " ", texto(f, modo)).strip()
                if t:
                    if f.tag in ("h1", "h2", "h3", "h4", "dt") or f.classes & ROTULOS:
                        voz = "titulo"
                    elif le:
                        voz = "lei"
                    elif lit:
                        voz = "literal"
                    else:
                        voz = "site"
                    saida.append({"voz": voz, "texto": t, "tag": f.tag, "cl": f.classes})
                varrer_links(f, modo, links)
            continue
        varrer(f, modo, saida, lit, le, links)


def varrer_links(no, modo, links):
    for f in no.filhos:
        if isinstance(f, No) and visivel(f.classes, modo) and not f.classes & TIRAR:
            if f.tag == "a" and f.href is not None:
                links.append((f.href, f.classes))
            varrer_links(f, modo, links)


def achar(no, tag):
    for f in no.filhos:
        if isinstance(f, No):
            if f.tag == tag:
                return f
            r = achar(f, tag)
            if r:
                return r
    return None


def ler_pagina(arq):
    p = Leitor()
    p.feed(arq.read_text(encoding="utf-8"))
    p.close()
    return achar(p.raiz, "main"), p.minimo


def pal(t):
    return len(t.split())


def falhas_citacao(t):
    m = []
    if PROPRIO_TEXTO.search(t):
        m.append("fala do próprio texto")
    if ANAFORA.search(t):
        m.append("depende do que veio antes")
    if t[:1].islower():
        m.append("começa no meio")
    if not re.search(r"[.!?…”\")\]»]$", t):
        m.append("frase cortada")
    if pal(t) > MAX_PALAVRAS_CITACAO:
        m.append("longa")
    return m


def medir(raiz):
    paginas = []
    for arq in sorted(raiz.rglob("*.html")):
        rel = arq.relative_to(raiz).as_posix().replace("index.html", "")
        if rel.startswith(("tese/", "assets/")):
            continue
        main, minimo = ler_pagina(arq)
        if main is None:
            continue
        for modo in (0, 1, 2):
            if modo < minimo:
                continue
            blocos, links = [], []
            varrer(main, modo, blocos, links=links)
            paginas.append({"u": rel, "modo": modo, "blocos": blocos, "links": links, "minimo": minimo})
    return paginas


def resumo_pagina(p):
    c = collections.Counter()
    for b in p["blocos"]:
        c[b["voz"]] += pal(b["texto"])
    tot = c["site"] + c["literal"]
    p["site"], p["literal"], p["pct"] = c["site"], c["literal"], (100 * c["literal"] / tot if tot else 0)
    seq = maior = 0
    p["soltas"] = []
    corpo = [b for b in p["blocos"] if b["texto"] not in ("De onde vem", "Em texto literal", "De onde vem cada nome")]
    secao_lit = secao_site = 0
    titulo = None
    for b in corpo + [{"voz": "titulo", "texto": "", "tag": "h2", "cl": set()}]:
        if b["voz"] == "literal":
            seq += 1
            maior = max(maior, seq)
            secao_lit += 1
        else:
            if b["voz"] in ("site", "lei"):
                seq = 0
                secao_site += 1
            if b["voz"] == "titulo":
                seq = 0
                if titulo is not None and secao_lit and not secao_site:
                    p["soltas"].append(titulo)
                titulo, secao_lit, secao_site = b["texto"], 0, 0
    p["seq"] = maior
    p["ltese"] = sum(1 for h, cl in p["links"] if re.search(r"(^|/)tese/", h) and not cl & {"integral"})


def relatorio(paginas, estrito=False):
    for p in paginas:
        resumo_pagina(p)
    falhas = 0

    def fora_autor(p):
        return not p["u"].startswith(("autores/", "referencias/", "autor/", "404"))

    print("# Informação")
    info = [p for p in paginas if p["modo"] == 0 and fora_autor(p)]
    lit = sum(p["literal"] for p in info)
    tom = collections.Counter()
    ex = []
    for p in paginas:
        if p["modo"] > 1:
            continue
        for b in p["blocos"]:
            if b["voz"] in ("site", "titulo"):
                for padrao, nome in ((IMPERATIVO, "imperativo"), (TEORIA_IDEIA, "teoria como ideia")):
                    if padrao.search(b["texto"]):
                        tom[nome] += 1
                        ex.append((p["u"], b["texto"][:90]))
    print(f"  literal {lit} palavras. Tom {dict(tom)}")
    for e in sorted(set(ex))[:15]:
        print("   ", e)
    falhas += lit + sum(tom.values())

    print("\n# Doutrina")
    dou = [p for p in paginas if p["modo"] == 1 and fora_autor(p)]
    s, l = sum(p["site"] for p in dou), sum(p["literal"] for p in dou)
    print(f"  site {s}, literal {l}, {100 * l / max(s + l, 1):.0f}% literal")
    ruins = [p for p in dou if p["pct"] > MAX_LITERAL_DOUTRINA and p["literal"] > 40]
    print(f"  páginas acima de {MAX_LITERAL_DOUTRINA}%  {len(ruins)}")
    for p in sorted(ruins, key=lambda p: -p["literal"])[:25]:
        print(f"    {p['pct']:4.0f}%  {p['literal']:6}  {p['u']}")
    so = [(p["u"], t) for p in dou for t in p["soltas"]]
    print(f"  seções só de citação  {len(so)}")
    print(f"  sequências acima de {MAX_SEQUENCIA}  {sum(1 for p in dou if p['seq'] > MAX_SEQUENCIA)} páginas")
    print(f"  páginas com mais de {MAX_LINKS_TESE} link ao texto integral  {sum(1 for p in dou if p['ltese'] > MAX_LINKS_TESE)}")
    cit = collections.Counter()
    pgs = collections.defaultdict(set)
    motivos = collections.Counter()
    for p in dou:
        for b in p["blocos"]:
            if b["voz"] == "literal":
                cit[b["texto"]] += 1
                pgs[b["texto"]].add(p["u"])
    ruim_cit = 0
    for t in cit:
        for m in falhas_citacao(t):
            motivos[m] += 1
        if falhas_citacao(t):
            ruim_cit += 1
    rep = [t for t in pgs if len(pgs[t]) > MAX_PAGINAS_CITACAO]
    print(f"  citações distintas {len(cit)}, fora do critério {ruim_cit} {dict(motivos)}")
    print(f"  citações em mais de {MAX_PAGINAS_CITACAO} páginas  {len(rep)}")
    falhas += len(ruins) + len(so) + sum(1 for p in dou if p["seq"] > MAX_SEQUENCIA) + ruim_cit + len(rep) + sum(1 for p in dou if p["ltese"] > MAX_LINKS_TESE)
    # Desde 09/11/2026, por ordem do autor, a prosa do curso afirma a doutrina sem atribuí-la à tese.
    tese = [(p["u"], b["texto"][:90]) for p in dou if p["u"].startswith("doutrina/")
            for b in p["blocos"] if b["voz"] in ("site", "titulo") and TESE_NA_PROSA.search(b["texto"])]
    print(f"  tese na prosa do curso  {len(tese)}")
    for e in tese[:15]:
        print("   ", e)
    falhas += len(tese)

    print("\n# Ciência")
    cie = [p for p in paginas if p["modo"] == 2 and fora_autor(p)]
    sem = 0
    lista = collections.Counter()
    for p in cie:
        ant = None
        for b in p["blocos"]:
            if b["texto"] in ("De onde vem", "Em texto literal", "De onde vem cada nome"):
                continue
            if b["voz"] == "literal" and ant in (None, "titulo"):
                sem += 1
                lista[p["u"]] += 1
            ant = b["voz"]
    s, l = sum(p["site"] for p in cie), sum(p["literal"] for p in cie)
    print(f"  site {s}, literal {l}, {100 * l / max(s + l, 1):.0f}% literal")
    print(f"  trechos literais sem frase do site antes  {sem}  {lista.most_common(10)}")
    falhas += sem
    print(f"\nFalhas {falhas}")
    return falhas


def mostrar(paginas, alvo):
    for p in paginas:
        if p["u"] == alvo:
            print(f"\n== {p['u']} modo {p['modo']}")
            for b in p["blocos"]:
                print(f"  {b['voz'][:3]} {b['tag']:10} {pal(b['texto']):4}  {b['texto'][:150]}")


def main():
    args = sys.argv[1:]
    alvo = args[args.index("--pagina") + 1] if "--pagina" in args else None
    raiz = Path(next((a for a in args if not a.startswith("--") and a != alvo), "docs"))
    paginas = medir(raiz)
    if alvo is not None:
        mostrar(paginas, alvo)
        return 0
    falhas = relatorio(paginas)
    return 1 if ("--estrito" in args and falhas) else 0


if __name__ == "__main__":
    sys.exit(main())
