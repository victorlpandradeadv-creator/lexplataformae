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
from marcas import assinatura, marcar

RAIZ = Path(__file__).resolve().parents[2]
lote = sys.argv[1]
L = RAIZ / "traducao" / "revisao" / "lotes" / f"{lote}.json"
if not L.exists():
    L = RAIZ / "traducao" / "lotes" / f"{lote}.json"
orig = {x["k"]: x for x in json.loads(L.read_text())}
# A memória inteira, para achar o arquivo de cada trecho
ONDE, atual, ARQS = {}, {}, {}
for a in sorted((RAIZ / "traducao" / "saida").glob("*.jsonl")):
    ARQS[a] = [json.loads(l) for l in a.read_text().splitlines() if l.strip()]
    for d in ARQS[a]:
        if d["k"] in orig:
            ONDE[d["k"]] = a; atual[d["k"]] = d["en"]
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
vistos_novos = set()
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
    if assinatura(en) != assinatura(marcar(orig[k]["pt"])[0]):
        ruins.append(f"marcas diferentes em {k}"); continue
    atual[k] = en; vistos.add(k); vistos_novos.add(k); ok += 1
import fcntl
NOVOS = {k: atual[k] for k in vistos_novos}
with open(RAIZ / "traducao" / "saida" / ".trava", "w") as trava:
    fcntl.flock(trava, fcntl.LOCK_EX)
    for a in {ONDE[k] for k in NOVOS}:
        ds = [json.loads(l) for l in a.read_text().splitlines() if l.strip()]
        a.write_text("".join(json.dumps({"k": d["k"], "en": NOVOS.get(d["k"], d["en"])}, ensure_ascii=False) + "\n" for d in ds))
salva_vistos()
print(f"gravadas {ok}. recusadas {len(ruins)}. faltam {len([k for k in orig if k in atual and k not in vistos])}.")
for r in ruins[:20]:
    print(" ", r)
