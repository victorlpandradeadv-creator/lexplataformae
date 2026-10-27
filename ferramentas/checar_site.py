"""Confere o site gerado em docs/. Links internos, âncoras, ids repetidos, links aninhados e ordem de títulos."""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

RAIZ = Path(sys.argv[1] if len(sys.argv) > 1 else "docs").resolve()


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.hrefs, self.dup, self.aninhados, self.titulos = set(), [], [], 0, []
        self.dentro_a = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            if a["id"] in self.ids:
                self.dup.append(a["id"])
            self.ids.add(a["id"])
        if tag == "a":
            if self.dentro_a:
                self.aninhados += 1
            self.dentro_a += 1
            if a.get("href"):
                self.hrefs.append(a["href"])
        if tag in ("link", "script") and (a.get("href") or a.get("src")):
            self.hrefs.append(a.get("href") or a.get("src"))
        if re.fullmatch(r"h[1-6]", tag):
            self.titulos.append(int(tag[1]))

    def handle_endtag(self, tag):
        if tag == "a" and self.dentro_a:
            self.dentro_a -= 1


paginas = {}
for arq in RAIZ.rglob("*.html"):
    p = P()
    p.feed(arq.read_text(encoding="utf-8"))
    paginas[arq] = p

problemas = []
for arq, p in paginas.items():
    rel = arq.relative_to(RAIZ)
    if p.dup:
        problemas.append(f"ID REPETIDO {rel} {sorted(set(p.dup))[:5]}")
    if p.aninhados:
        problemas.append(f"LINK ANINHADO {rel} {p.aninhados}")
    anterior = 0
    for n in p.titulos:
        if anterior and n > anterior + 1:
            problemas.append(f"TÍTULO PULA {rel} h{anterior}→h{n}")
            break
        anterior = n
    for h in p.hrefs:
        u = urlparse(h)
        if u.scheme in ("http", "https", "mailto") or h.startswith("data:"):
            continue
        if h.startswith("/"):
            alvo = RAIZ / unquote(u.path).lstrip("/")
        else:
            alvo = (arq.parent / unquote(u.path)).resolve() if u.path else arq
        if alvo.is_dir():
            alvo = alvo / "index.html"
        if not alvo.exists():
            problemas.append(f"LINK QUEBRADO {rel} → {h}")
            continue
        if u.fragment and alvo.suffix == ".html":
            alvo_p = paginas.get(alvo)
            if alvo_p is not None and u.fragment not in alvo_p.ids:
                problemas.append(f"ÂNCORA AUSENTE {rel} → {h}")

print(f"{len(paginas)} páginas conferidas, {len(problemas)} problemas")
for x in problemas[:60]:
    print(x)
