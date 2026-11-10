"""Revisão do inglês de um lote. Mostra o original e a tradução atual e grava só as versões melhoradas.

Uso
    python3 ferramentas/en/revisar.py LOTE --proximos 40     # próximos trechos ainda não revistos
    python3 ferramentas/en/revisar.py LOTE --vistos k1 k2 ... # marca como revistos sem mudança
    python3 ferramentas/en/revisar.py LOTE <<'JSONL'          # grava versões novas e marca como revistas
    {"k": "...", "en": "..."}
    JSONL
A versão nova precisa trazer as mesmas marcas numeradas do original.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from marcas import assinatura

RAIZ = Path(__file__).resolve().parents[2]
lote = sys.argv[1]
orig = {x["k"]: x for x in json.loads((RAIZ / "traducao" / "lotes" / f"{lote}.json").read_text())}
arq = RAIZ / "traducao" / "saida" / f"{lote}.jsonl"
linhas = [json.loads(l) for l in arq.read_text().splitlines() if l.strip()]
atual = {d["k"]: d["en"] for d in linhas}
visto_arq = RAIZ / "traducao" / "revisao" / f"{lote}.txt"
visto_arq.parent.mkdir(exist_ok=True)
vistos = set(visto_arq.read_text().split()) if visto_arq.exists() else set()

def salva_vistos():
    visto_arq.write_text("\n".join(sorted(vistos)) + "\n")

if "--proximos" in sys.argv:
    n = int(sys.argv[sys.argv.index("--proximos") + 1])
    falta = [k for k in orig if k in atual and k not in vistos]
    print(f"# faltam {len(falta)} de {len(orig)}")
    for k in falta[:n]:
        print(json.dumps({"k": k, "pagina": orig[k]["pagina"], "pt": orig[k]["pt"], "en": atual[k]}, ensure_ascii=False))
    sys.exit()
if "--vistos" in sys.argv:
    ks = sys.argv[sys.argv.index("--vistos") + 1:]
    vistos |= {k for k in ks if k in orig}
    salva_vistos()
    print(f"marcados {len(ks)}. faltam {len([k for k in orig if k in atual and k not in vistos])}.")
    sys.exit()
ok, ruins = 0, []
for l in sys.stdin:
    l = l.strip()
    if not l:
        continue
    try:
        d = json.loads(l)
    except Exception:
        ruins.append(f"JSON inválido: {l[:80]}"); continue
    k, en = d.get("k"), d.get("en")
    if k not in orig or not isinstance(en, str) or not en.strip():
        ruins.append(f"chave desconhecida ou vazia: {k}"); continue
    if assinatura(en) != assinatura(orig[k]["pt"]):
        ruins.append(f"marcas diferentes em {k}"); continue
    atual[k] = en; vistos.add(k); ok += 1
arq.write_text("".join(json.dumps({"k": k, "en": atual[k]}, ensure_ascii=False) + "\n" for k in atual))
salva_vistos()
print(f"gravadas {ok}. recusadas {len(ruins)}. faltam {len([k for k in orig if k in atual and k not in vistos])}.")
for r in ruins[:20]:
    print(" ", r)
