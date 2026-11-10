"""Divide os segmentos em lotes para os tradutores, por página, na ordem do site."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from marcas import marcar

RAIZ = Path(__file__).resolve().parents[2]
T = RAIZ / "traducao"
LIMITE = int(sys.argv[1]) if len(sys.argv) > 1 else 17000
mem = json.loads((T / "memoria.json").read_text()) if (T / "memoria.json").exists() else {}
(T / "lotes").mkdir(exist_ok=True)
vistos = set(mem)
ORDEM = ["index.html", "caminho", "problemas", "direitos", "como-reclamar", "conceitos", "plataformas", "doutrina", "roteiro",
         "legislacao", "instrumentos", "autor", "epigrafes", "metodo", "fundamentos", "dogmatica", "objeto-e-instrumentos", "autores", "referencias", "versoes"]
def peso(p):
    top = p.split("/")[0]
    return (ORDEM.index(top) if top in ORDEM else 50, p)
for grupo in ("site", "tese"):
    segs = [x for x in json.loads((T / f"segmentos-{grupo}.json").read_text()) if x["k"] not in vistos]
    vistos |= {x["k"] for x in segs}
    segs.sort(key=lambda x: peso(x["pagina"]))
    lotes, atual, w = [], [], 0
    for x in segs:
        m, _ = marcar(x["pt"]) if x["tipo"] == "html" else (x["pt"], None)
        n = len(re.sub(r"<[^>]+>", " ", m).split())
        if atual and w + n > LIMITE:
            lotes.append(atual); atual, w = [], 0
        atual.append({"k": x["k"], "pagina": x["pagina"], "pt": m}); w += n
    if atual: lotes.append(atual)
    for i, l in enumerate(lotes, 1):
        (T / "lotes" / f"{grupo}-{i:02d}.json").write_text(json.dumps(l, ensure_ascii=False, indent=1), encoding="utf-8")
    print(grupo, len(lotes), "lotes", sum(len(l) for l in lotes), "segmentos")
