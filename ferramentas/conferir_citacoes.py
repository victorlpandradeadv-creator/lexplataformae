"""Confere citações literais de arquivos Markdown contra o texto da tese.

Uso
    python3 ferramentas/conferir_citacoes.py conceitos/ficha-canonica-v0.md [outros.md ...]

Formatos reconhecidos
    > trecho citado (p. 123)
    > trecho citado (p. 123-124)
    > trecho citado (Resumo)
    "trecho citado" (p. 123)

Trechos suprimidos marcados com [...] são conferidos fragmento a fragmento.
A numeração de página é a impressa. No PDF da tese, página impressa = página do PDF - 2.
Requer o utilitário pdftotext (poppler-utils).
"""
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PDF = RAIZ / "tese" / "andrade-2026-tese-oic-lex-plataformae.pdf"
DESLOCAMENTO = 2


def normalizar(texto, fonte=False):
    texto = unicodedata.normalize("NFC", texto)
    for a, b in (("“", '"'), ("”", '"'), ("‘", "'"), ("’", "'"), ("­", "")):
        texto = texto.replace(a, b)
    if fonte:
        # remove chamadas de nota de rodapé coladas ao texto
        # (depois de ponto, só quando o ponto fecha uma palavra, para não comer decimais como 26.3)
        texto = re.sub(r'(?:(?<=[A-Za-zÀ-úºª,;:"])|(?<=[A-Za-zÀ-úºª"]\.))\d{1,3}(?=[\s,\.])', "", texto)
    return re.sub(r"\s+", " ", texto).strip()


def paginas(manter_hifen=False):
    """Texto de cada página impressa. O hífen no fim da linha some ao juntar as linhas, como na
    separação silábica. Com manter_hifen, ele fica, como nas palavras compostas (vale-tudo)."""
    bruto = subprocess.run(
        ["pdftotext", "-layout", str(PDF), "-"], capture_output=True, text=True, check=True
    ).stdout.split("\f")
    resultado = {}
    for indice, pagina in enumerate(bruto):
        impressa = indice + 1 - DESLOCAMENTO
        texto = ""
        for linha in (l.strip() for l in pagina.split("\n")):
            if not linha:
                texto += "\n"
                continue
            if texto.endswith("-") and not texto.endswith(" -"):
                texto = (texto if manter_hifen else texto[:-1]) + linha
            else:
                texto += (" " if texto and not texto.endswith("\n") else "") + linha
        texto = re.sub(r"^\s*" + str(impressa) + r"\s*\n", "", texto)
        resultado[impressa] = texto
    return resultado


def citacoes(markdown):
    for m in re.finditer(r"^> (.+?) \((p\. [\d\-]+|Resumo)\)\s*$", markdown, re.M):
        yield m.group(1), m.group(2)
    for m in re.finditer(r'"([^"\n]{15,}?)"\s*\((p\. [\d\-]+)\)', markdown):
        yield m.group(1), m.group(2)


def atravessa_pagina(fragmento, ref, por_pagina):
    """Aceita trecho contínuo que a virada de página separa com notas de rodapé no meio.

    Exige que a primeira parte esteja na página N e a segunda na página N+1.
    """
    if ref == "Resumo" or "-" not in ref:
        return False
    numeros = [int(x) for x in ref[3:].split("-")]
    palavras = fragmento.split(" ")
    for n in range(numeros[0], numeros[-1]):
        antes = normalizar(por_pagina.get(n, ""), fonte=True)
        depois = normalizar(por_pagina.get(n + 1, ""), fonte=True)
        for k in range(3, len(palavras) - 2):
            if " ".join(palavras[:k]) in antes and " ".join(palavras[k:]) in depois:
                return True
    return False


def achado(fragmento, ref, por_pagina):
    if ref == "Resumo":
        palheiro = normalizar(" ".join(por_pagina.values()), fonte=True)
    else:
        numeros = [int(x) for x in ref[3:].split("-")]
        palheiro = normalizar(
            " ".join(por_pagina.get(n, "") for n in range(numeros[0], numeros[-1] + 1)),
            fonte=True,
        )
    return fragmento in palheiro or atravessa_pagina(fragmento, ref, por_pagina)


def main(arquivos):
    versoes = (paginas(), paginas(manter_hifen=True))
    total = falhas = 0
    for arquivo in arquivos:
        for trecho, ref in citacoes(Path(arquivo).read_text(encoding="utf-8")):
            total += 1
            for fragmento in (f.strip(" .,") for f in trecho.split("[...]")):
                if len(fragmento) > 8 and not any(achado(normalizar(fragmento), ref, v) for v in versoes):
                    falhas += 1
                    print(f"NÃO ENCONTRADA  {arquivo}  {ref}  {fragmento[:100]}")
    print(f"{total} citações conferidas, {falhas} não encontradas.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
