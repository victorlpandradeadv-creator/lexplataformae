"""Mede a legibilidade dos textos da camada externa pelo índice de Flesch adaptado ao português.

Uso
    python3 ferramentas/medir_legibilidade.py [conteudo/camada-externa.md]

Fórmula de Martins e colegas (1996), adaptada ao português.
    248,835 - 1,015 x (palavras por frase) - 84,6 x (sílabas por palavra)
Faixas usuais. De 75 a 100, muito fácil. De 50 a 75, fácil. De 25 a 50, difícil. Abaixo de 25, muito difícil.

A contagem de sílabas é aproximada. Conta grupos de vogais e separa os encontros de vogais fortes,
que em português costumam formar hiato. Serve para comparar textos entre si e acompanhar a meta,
não para laudo. A meta da camada externa é a faixa fácil, de 50 para cima.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARQ = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "conteudo" / "camada-externa.md"
META = 50

VOGAIS = "aeiouáéíóúâêôãõàüy"
FORTES = set("aeoáéóâêôãõàíú")


def silabas(palavra):
    p = palavra.lower()
    grupos = re.findall(f"[{VOGAIS}]+", p)
    n = 0
    for g in grupos:
        n += 1
        for a, b in zip(g, g[1:]):
            if a in FORTES and b in FORTES and not (a in "ãõ" and b in "eo"):
                n += 1
    return max(n, 1)


def flesch(texto):
    frases = [f for f in re.split(r"[.!?]+(?:\s|$)", texto) if re.search(r"\w", f)]
    palavras = re.findall(r"[A-Za-zÀ-ÿ]+(?:-[A-Za-zÀ-ÿ]+)*", texto)
    if not frases or not palavras:
        return None, 0, 0
    sil = sum(silabas(w) for w in re.findall(r"[A-Za-zÀ-ÿ]+", texto))
    ppf = len(palavras) / len(frases)
    spp = sil / len(palavras)
    return 248.835 - 1.015 * ppf - 84.6 * spp, ppf, spp


def faixa(f):
    return "muito fácil" if f >= 75 else "fácil" if f >= 50 else "difícil" if f >= 25 else "muito difícil"


def blocos(arq):
    pagina, campo, saida = None, None, {}
    for linha in arq.read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            pagina, campo = linha[3:].strip(), None
            continue
        if linha.startswith("### "):
            campo = linha[4:].strip()
            continue
        if pagina and campo and linha.strip() and not linha.startswith(">"):
            saida.setdefault(pagina, {}).setdefault(campo, []).append(linha.strip())
    return saida


def main():
    dados = blocos(ARQ)
    todo, abaixo = [], []
    for pagina, campos in dados.items():
        texto = " ".join(" ".join(v) for v in campos.values())
        todo.append(texto)
        f, ppf, spp = flesch(texto)
        marca = "" if f >= META else "  abaixo da meta"
        if f < META:
            abaixo.append(pagina)
        print(f"{pagina:34} {f:6.1f}  {faixa(f):13} {ppf:5.1f} palavras por frase  {spp:4.2f} sílabas por palavra{marca}")
    f, ppf, spp = flesch(" ".join(todo))
    print(f"\n{'conjunto':34} {f:6.1f}  {faixa(f)}")
    print(f"{len(dados) - len(abaixo)} de {len(dados)} páginas na meta de leitura fácil" + (f". Abaixo  {', '.join(abaixo)}" if abaixo else ""))


if __name__ == "__main__":
    main()
