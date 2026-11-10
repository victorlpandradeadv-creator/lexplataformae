"""Grava traduções de um lote. Lê do stdin uma tradução por linha, em JSON {"k": ..., "en": ...}.

Uso
    python3 ferramentas/en/gravar.py site-03 < traducoes.jsonl
    python3 ferramentas/en/gravar.py site-03 --faltam      # lista o que falta, em ordem
Confere as marcas numeradas contra o original e recusa a linha que não bate.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from marcas import assinatura

RAIZ = Path(__file__).resolve().parents[2]
lote = sys.argv[1]
orig = {x["k"]: x for x in json.loads((RAIZ / "traducao" / "lotes" / f"{lote}.json").read_text())}
saida = RAIZ / "traducao" / "saida" / f"{lote}.jsonl"
saida.parent.mkdir(exist_ok=True)
feitos = {}
if saida.exists():
    for l in saida.read_text().splitlines():
        if l.strip():
            d = json.loads(l); feitos[d["k"]] = d["en"]
if "--faltam" in sys.argv:
    n = int(sys.argv[sys.argv.index("--faltam") + 1]) if len(sys.argv) > sys.argv.index("--faltam") + 1 else 60
    falta = [x for k, x in orig.items() if k not in feitos]
    print(f"# faltam {len(falta)} de {len(orig)}")
    for x in falta[:n]:
        print(json.dumps({"k": x["k"], "pagina": x["pagina"], "pt": x["pt"]}, ensure_ascii=False))
    sys.exit()
ok, ruins = 0, []
with saida.open("a") as f:
    for l in sys.stdin:
        l = l.strip()
        if not l:
            continue
        try:
            d = json.loads(l)
        except Exception as e:
            ruins.append(f"JSON inválido: {l[:80]}"); continue
        k, en = d.get("k"), d.get("en")
        if k not in orig or not isinstance(en, str) or not en.strip():
            ruins.append(f"chave desconhecida ou vazia: {k}"); continue
        if assinatura(en) != assinatura(orig[k]["pt"]):
            ruins.append(f"marcas diferentes em {k}: esperado {assinatura(orig[k]['pt'])}"); continue
        f.write(json.dumps({"k": k, "en": en}, ensure_ascii=False) + "\n"); feitos[k] = en; ok += 1
print(f"gravadas {ok}. recusadas {len(ruins)}. faltam {len(orig) - len(feitos)} de {len(orig)}.")
for r in ruins[:20]:
    print(" ", r)
