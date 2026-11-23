"""Confere citações literais de arquivos Markdown contra o texto da tese.

Uso
    python3 ferramentas/conferir_citacoes.py conceitos/ficha-canonica-v0.md [outros.md ...]

Formatos reconhecidos
    > trecho citado (p. 123)
    > trecho citado (p. 123-124)
    > trecho citado (Resumo)
    "trecho citado" (p. 123)

Trechos suprimidos marcados com [...] são conferidos fragmento a fragmento.

Desde 22/11/2026 cada fragmento precisa estar também num fluxo só do corpus (dados/corpus.json), ou o
corpo do texto ou uma nota de rodapé. No texto da página, o pdftotext põe as notas logo depois do corpo,
e um trecho podia emendar o fim do corpo com o começo do rodapé sem que nada acusasse
(Trata-se de incapacidade controlada, p. 603).
A numeração de página é a impressa. No PDF da tese, página impressa = página do PDF - 2.
Requer o utilitário pdftotext (poppler-utils).
"""
import html
import json
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
        # (depois de ponto, só quando o ponto fecha uma palavra, para não comer decimais como 26.3, e depois de vírgula,
        # só quando a vírgula vem depois de palavra ou de parêntese, para não comer centavos como R$ 102,80)
        texto = re.sub(r'(?:(?<=[A-Za-zÀ-úºª;:")])|(?<=[A-Za-zÀ-úºª")],)|(?<=[A-Za-zÀ-úºª"]\.))\d{1,3}(?=[\s,\.\)])', "", texto)
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
    for m in re.finditer(r"^>!? (.+?) \((p\. [\d\-]+|Resumo)\)\s*$", markdown, re.M):
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


def fluxos():
    """Corpo do texto por página impressa e cada nota de rodapé à parte, a partir do corpus."""
    arquivo = RAIZ / "dados" / "corpus.json"
    if not arquivo.exists():
        return None
    dados = json.loads(arquivo.read_text(encoding="utf-8"))
    corpo, pagina = {}, None
    notas = []
    def limpar(h):
        h = re.sub(r'<sup class="nota-ref">.*?</sup>', "", h)
        h = re.sub(r'<span class="pg-marca"[^>]*>[^<]*</span>', lambda m: m.group(0), h)
        return h
    for sec in dados["secoes"]:
        titulo = re.sub(r"<[^>]+>", "", limpar(sec.get("titulo_html", "")))
        for b in sec["blocos"]:
            for parte in re.split(r'(<span class="pg-marca" id="p\d+"[^>]*>[^<]*</span>)', limpar(b["html"])):
                m = re.match(r'<span class="pg-marca" id="p(\d+)"', parte)
                if m:
                    pagina = int(m.group(1))
                    continue
                if pagina is not None:
                    texto = html.unescape(re.sub(r"<[^>]+>", " " if b["tipo"] == "tabela" else "", parte))
                    corpo.setdefault(pagina, []).append(texto)
            corpo.setdefault(pagina, [])
        for n in sec.get("notas", []):
            notas.append((n["pagina"], normalizar(html.unescape(re.sub(r"<[^>]+>", "", limpar(n["html"]))))))
    return {k: normalizar(" ".join(v)) for k, v in corpo.items()}, notas


def num_fluxo(fragmento, ref, fl):
    """O fragmento está inteiro no corpo das páginas citadas ou numa só nota delas."""
    if fl is None or ref == "Resumo":
        return True
    corpo, notas = fl
    numeros = [int(x) for x in ref[3:].split("-")]
    a, b = numeros[0], numeros[-1]
    if b < min(corpo):
        return True  # páginas anteriores à introdução, como o resumo, ficam fora do corpus
    if fragmento in " ".join(corpo.get(n, "") for n in range(a, b + 1)):
        return True
    return any(fragmento in t for p, t in notas if a - 3 <= p <= b)


def main(arquivos):
    versoes = (paginas(), paginas(manter_hifen=True))
    fl = fluxos()
    total = falhas = 0
    for arquivo in arquivos:
        for trecho, ref in citacoes(Path(arquivo).read_text(encoding="utf-8")):
            total += 1
            for fragmento in (f.strip(" .,") for f in trecho.split("[...]")):
                if len(fragmento) > 8 and not any(achado(normalizar(fragmento), ref, v) for v in versoes):
                    falhas += 1
                    print(f"NÃO ENCONTRADA  {arquivo}  {ref}  {fragmento[:100]}")
                elif len(fragmento) > 8 and not num_fluxo(normalizar(fragmento), ref, fl):
                    falhas += 1
                    print(f"EMENDA ENTRE CORPO E NOTA  {arquivo}  {ref}  {fragmento[:100]}")
    print(f"{total} citações conferidas, {falhas} não encontradas.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
