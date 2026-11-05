"""Imprime uma seção da tese em texto corrido, com as marcas de página e as notas de rodapé.

Uso: python3 ferramentas/ler_secao.py 6.3.1           só a seção
     python3 ferramentas/ler_secao.py 6.3 --inteira   a seção e as subseções
     python3 ferramentas/ler_secao.py --lista         números, títulos e palavras
Serve para consultar a tese na adequação das camadas. Feito em 05/11/2026.
"""
import json, re, sys
from pathlib import Path

D = json.loads((Path(__file__).resolve().parent.parent / "dados" / "corpus.json").read_text(encoding="utf-8"))
SECOES = D if isinstance(D, list) else D.get("secoes", D)

def limpo(h):
    h = re.sub(r'<sup[^>]*>(.*?)</sup>', lambda m: "[nota " + re.sub(r"<[^>]+>", "", m.group(1)) + "]", h, flags=re.S)
    h = re.sub(r'<[^>]*class="[^"]*pg[^"]*"[^>]*>\s*(?:p\.\s*)?(\d+)\s*</[a-z]+>', r" [p. \1] ", h)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h)).strip()

def numero(s):
    return str(s.get("n", s.get("numero", "")))

def imprimir(s):
    print(f"\n===== {numero(s)} {s.get('titulo', '')}\n")
    for b in s.get("blocos", []):
        print(limpo(b.get("html", "") if isinstance(b, dict) else b)); print()
    notas = s.get("notas") or []
    if notas:
        print("--- notas de rodapé ---")
        for n in notas:
            print(f"[{n.get('n', n.get('numero', ''))}] {limpo(n.get('html', n.get('texto', '')))}" if isinstance(n, dict) else limpo(n))

if "--lista" in sys.argv:
    for s in SECOES:
        t = " ".join((b.get("html", "") if isinstance(b, dict) else b) for b in s.get("blocos", []))
        print(numero(s), "|", s.get("titulo", ""), "|", len(re.sub(r"<[^>]+>", " ", t).split()))
    sys.exit()
alvo = sys.argv[1]
for s in SECOES:
    n = numero(s)
    if n == alvo or ("--inteira" in sys.argv and n.startswith(alvo + ".")):
        imprimir(s)
