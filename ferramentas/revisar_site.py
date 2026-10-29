"""Revisão mecânica do site gerado. Lê docs/ e aponta problemas de texto visível por modo.

Uso
    python3 -I ferramentas/revisar_site.py docs

Aponta, nas telas da Informação e da Doutrina, nomes antigos dos modos, resíduos de composição, pontuação
proibida na prosa do site, menções à tese, Lex Plataformae fora da Ciência e os nomes Laboratório e Roteiro,
que o menu não usa mais. Páginas que só existem na Ciência ficam de fora. O texto integral da tese fala da
tese e traz os títulos literais, e por isso as ocorrências em tese/ são esperadas.
"""
import re, sys, glob, html
from html.parser import HTMLParser
from collections import Counter, defaultdict

RAIZ = sys.argv[1]
VAZIOS = {"br", "img", "input", "meta", "link", "hr", "source", "wbr"}
CITACAO = {"blockquote", "q", "cite"}
CLASSES_CITA = {"ref", "refs", "balao", "balao-ref", "referencia", "obra", "obras", "lei-rotulo", "lei-fonte", "citacao", "citacao-longa", "canonica", "frase", "campo-def", "texto", "partes", "lei-texto", "titulo-tese", "trecho"}

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pilha = []
        self.textos = []  # (texto, conjunto de classes ancestrais, em_citacao, tags)
        self.em_script = 0
    def handle_starttag(self, tag, attrs):
        if tag in VAZIOS:
            return
        a = dict(attrs)
        self.pilha.append((tag, set((a.get("class") or "").split()), a))
        if tag in ("script", "style", "title"):
            self.em_script += 1
    def handle_endtag(self, tag):
        if tag in VAZIOS:
            return
        for i in range(len(self.pilha) - 1, -1, -1):
            if self.pilha[i][0] == tag:
                if tag in ("script", "style", "title"):
                    self.em_script -= 1
                del self.pilha[i:]
                break
    def handle_data(self, d):
        if self.em_script or not d.strip():
            return
        classes = set().union(*[c for _, c, _ in self.pilha]) if self.pilha else set()
        tags = [t for t, _, _ in self.pilha]
        cita = any(t in CITACAO for t in tags) or bool(classes & CLASSES_CITA)
        self.textos.append((d, classes, cita, tags))

MINIMO = [0]
def visivel_em(classes, modo):
    """Se um texto com essas classes ancestrais aparece no modo 0, 1 ou 2."""
    if modo < MINIMO[0]:
        return False
    if "ciencia" in classes or "arq" in classes:
        if modo < 2:
            return False
    if "interno" in classes and modo < 1:
        return False
    if "em-modo" in classes:
        mods = {int(c[5:]) for c in classes if re.fullmatch(r"modo-\d", c)}
        if mods and modo not in mods:
            return False
    for c in classes:
        m = re.fullmatch(r"so-(\d)", c)
        if m and int(m.group(1)) != modo:
            return False
    return True

achados = defaultdict(list)
versoes = Counter()
for f in sorted(glob.glob(RAIZ + "/**/*.html", recursive=True)):
    rel = f[len(RAIZ) + 1:]
    if rel.startswith("tese/") and rel != "tese/index.html":
        corpus = True
    else:
        corpus = False
    s = open(f, encoding="utf-8").read()
    for v in re.findall(r"Versão\s+(\d+\.\d+)", s):
        versoes[v] += 1
    p = P(); p.feed(s)
    m = re.search(r'data-minimo="(\d)"', s)
    minimo = int(m.group(1)) if m else 0
    if minimo >= 2:
        continue
    MINIMO[0] = minimo
    for d, classes, cita, tags in p.textos:
        t = re.sub(r"\s+", " ", d)
        # 1. Nomes antigos dos modos e verbos da chave antiga
        if re.search(r"\b(Conhecer|Verificar|Despir|Desnudar|desnudar|despir)\b", t) and not cita:
            achados["nome antigo de modo"].append((rel, t.strip()[:100]))
        # 2. Resíduos
        if re.search(r"\bTODO\b|\bTBD\b|XXX|\*\*|^#{2,}|\s[,.;:]\s|\.\.(?!\.)|\(\s*\)|\s{2,}\S", t):
            if not cita:
                achados["resíduo de composição"].append((rel, t.strip()[:100]))
        # 3. Pontuação proibida na prosa do site, fora de citação, nos modos 0 e 1
        if not cita and not corpus and (visivel_em(classes, 0) or visivel_em(classes, 1)):
            if re.search(r"[;—–]|\w:\s", t) and "pg" not in classes:
                achados["pontuação proibida na prosa"].append((rel, t.strip()[:110]))
        # 4. Menção à tese na prosa da Informação e da Doutrina
        if not cita and not corpus and re.search(r"\btese\b", t, re.I):
            if visivel_em(classes, 0) or visivel_em(classes, 1):
                if not any(x in rel for x in ("autor/", "404")):
                    achados["tese na prosa da Informação ou da Doutrina"].append((rel, t.strip()[:110]))
        # 5. Lex Plataformae na prosa da Informação e da Doutrina
        if not cita and not corpus and "Lex Plataformae" in t and "topo-nome" not in classes:
            if (visivel_em(classes, 0) or visivel_em(classes, 1)) and "a" not in tags[-1:]:
                achados["Lex Plataformae fora de Ciência"].append((rel, t.strip()[:110]))
        # 6. Laboratório onde o menu diz Plataformas
        if not cita and re.search(r"\bLaboratório\b", t) and (visivel_em(classes, 0) or visivel_em(classes, 1)):
            achados["Laboratório fora de Ciência"].append((rel, t.strip()[:110]))
        # 7. Roteiro como nome visível
        if not cita and re.search(r"\bRoteiro\b", t) and (visivel_em(classes, 0) or visivel_em(classes, 1)):
            achados["Roteiro visível fora de Ciência"].append((rel, t.strip()[:110]))

print("Versões", dict(versoes))
for k, v in achados.items():
    c = Counter(x[1] for x in v)
    print(f"\n## {k}  {len(v)} ocorrências, {len(c)} textos distintos")
    for texto, n in c.most_common(12):
        exemplo = next(r for r, t in v if t == texto)
        print(f"  {n:4d}  {texto}  [{exemplo}]")
