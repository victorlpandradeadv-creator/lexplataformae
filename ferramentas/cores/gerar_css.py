"""Gera site/cores.css a partir de estrutura/cores.json.

As cores mudam com o modo de leitura e com a preferência clara ou escura do aparelho.
Informação é o modo 0, Doutrina o 1 e Ciência o 2, pelos botões de rádio da chave Modo.
O arquivo sai depois de extra.css no estilo do site, e por isso redefine os tokens do protótipo.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cor import lin_hex, lin_to_oklab, oklab_to_lin, hexa  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
C = json.loads((RAIZ / "estrutura" / "cores.json").read_text(encoding="utf-8"))
A, T, TESE, MARCA = C["areas"], C["telas"], C["tese"], C["marca"]
MODOS = ["informacao", "doutrina", "ciencia"]


def mistura(a, b, t):
    x, y = lin_to_oklab(*lin_hex(a)), lin_to_oklab(*lin_hex(b))
    return hexa(tuple(min(1, max(0, v)) for v in oklab_to_lin(*[x[i] * (1 - t) + y[i] * t for i in range(3)])))


def tokens_modo(modo, tom):
    t = T[modo][tom]
    oposto = T["informacao"]["escuro" if tom == "claro" else "claro"]
    escuro = tom == "escuro"
    tese_texto = TESE["texto_escuro"] if escuro else TESE["texto"]
    dir_texto = A["direito"]["texto_escuro"] if escuro else A["direito"]["texto"]
    dir_marca = A["direito"]["destaque_escuro"] if escuro else A["direito"]["destaque"]
    acento = {"informacao": tese_texto, "doutrina": dir_texto, "ciencia": t["tinta"]}[modo]
    modo_cor = {"informacao": TESE["chapado"], "doutrina": dir_marca, "ciencia": t.get("traco", t["tinta2"])}[modo]
    v = {
        "--papel": t["papel"], "--folha": t["folha"], "--tinta": t["tinta"], "--tinta-2": t["tinta2"], "--linha": t["linha"],
        "--campo": mistura(t["papel"], t["linha"], 0.35),
        "--grade": t.get("grade", "transparent"),
        "--acento": acento, "--acento-suave": mistura(t["papel"], acento, 0.10),
        "--traco": t.get("traco", t["tinta2"]), "--desnudo": t.get("traco", t["tinta2"]),
        "--marca": MARCA[tom], "--modo": modo_cor,
        "--modo-tinta": t["papel"] if modo == "ciencia" else "#ffffff",
        "--inv-papel": oposto["papel"], "--inv-tinta": oposto["tinta"],
        "--nota": mistura(t["papel"], MARCA[tom], 0.45), "--nota-borda": mistura(t["linha"], MARCA[tom], 0.6),
    }
    return v


def tokens_globais(tom):
    escuro = tom == "escuro"
    v = {"--tese": TESE["chapado"], "--tese-sobre": TESE["sobre_chapado"],
         "--tese-texto": TESE["texto_escuro"] if escuro else TESE["texto"],
         "--tese-linha": TESE["marca_escuro"] if escuro else TESE["chapado"]}
    for k, a in A.items():
        v[f"--a-{k}"] = a["destaque_escuro"] if escuro else a["destaque"]
        v[f"--a-{k}-t"] = a["texto_escuro"] if escuro else a["texto"]
        v[f"--a-{k}-f"] = a["fundo_escuro"] if escuro else a["fundo"]
    f = T["ficha"][tom]
    v.update({"--f-papel": f["papel"], "--f-tinta": f["tinta"], "--f-tinta-2": f["tinta2"], "--f-pauta": f["pauta"]})
    return v


def bloco(seletor, v, extra=""):
    linhas = "".join(f"  {k}: {val};\n" for k, val in v.items())
    return f"{seletor} {{\n{linhas}{extra}}}\n"


def main():
    partes = ["/* Gerado por ferramentas/cores/gerar_css.py a partir de estrutura/cores.json. Não editar à mão. */\n",
              "/* Tokens globais e o modo Informação, que é o padrão. */\n",
              bloco(":root", {**tokens_globais("claro"), **tokens_modo("informacao", "claro")}, "  color-scheme: light;\n"),
              "@media (prefers-color-scheme: dark) {\n"
              + bloco(':root:not([data-theme="light"])', {**tokens_globais("escuro"), **tokens_modo("informacao", "escuro")}, "  color-scheme: dark;\n")
              + "}\n",
              bloco(':root[data-theme="dark"]', {**tokens_globais("escuro"), **tokens_modo("informacao", "escuro")}, "  color-scheme: dark;\n")]
    for i, modo in enumerate(MODOS[1:], 1):
        sel = f"body:has(#nivel-{i}:checked)"
        partes.append(f"/* Modo {modo}. */\n")
        partes.append(bloco(sel, tokens_modo(modo, "claro")))
        partes.append("@media (prefers-color-scheme: dark) {\n" + bloco(f':root:not([data-theme="light"]) {sel}', tokens_modo(modo, "escuro")) + "}\n")
        partes.append(bloco(f':root[data-theme="dark"] {sel}', tokens_modo(modo, "escuro")))
    destino = RAIZ / "site" / "cores.css"
    destino.write_text("".join(partes), encoding="utf-8")
    print("site/cores.css gerado")


if __name__ == "__main__":
    main()
