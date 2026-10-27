"""Extrai a tese em seções citáveis e grava dados/corpus.json.

Uso
    python3 ferramentas/extrair_corpus.py

Lê o PDF com PyMuPDF (pip install pymupdf). Separa corpo, citações longas e
notas de rodapé pelo tamanho da fonte e pela margem de cada página. Divide o
texto pelas entradas do sumário. Marca o início de cada página impressa, para
que toda referência do site possa apontar para o trecho exato.

As páginas de epígrafe não são transcritas. As letras das canções ficam fora
do site e aparecem apenas como referência, com remissão ao PDF.
"""
import html
import json
import re
import subprocess
import unicodedata
from pathlib import Path

import pymupdf

RAIZ = Path(__file__).resolve().parent.parent
PDF = RAIZ / "tese" / "andrade-2026-tese-oic-lex-plataformae.pdf"
SAIDA = RAIZ / "dados" / "corpus.json"
EPIGRAFES = json.loads((RAIZ / "dados" / "epigrafes.json").read_text(encoding="utf-8"))
DESLOCAMENTO = 2          # página impressa = página do PDF - 2
PRIMEIRA, ULTIMA = 21, 829  # páginas impressas do texto, da introdução ao fim das referências
SUMARIO_PDF = range(16, 21)  # páginas do PDF que trazem o sumário


def norm(t):
    t = unicodedata.normalize("NFC", t).replace("­", "")
    return re.sub(r"\s+", " ", t).strip()


def chave(t):
    """Forma reduzida para comparar títulos do sumário com títulos do texto."""
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(ch for ch in t if ch.isalnum())
    return t


def ler_sumario(doc):
    # O sumário é lido com o pdftotext, que preserva melhor os espaços das linhas pontilhadas.
    paginas = subprocess.run(["pdftotext", "-layout", "-f", str(SUMARIO_PDF.start), "-l", str(SUMARIO_PDF.stop - 1), str(PDF), "-"],
                             capture_output=True, text=True, check=True).stdout
    texto = paginas
    a = texto.index("SUMÁRIO")
    b = texto.index("REFERÊNCIAS", a)
    s = norm(texto[a + 7:b])
    s = re.sub(r"(?<=[A-Za-zÀ-ú])- (?=[A-Za-zÀ-ú])", "-", s)
    ents = re.findall(r"(\d+(?:\.\d+)*) (.+?)\s*(?:\.+\s*|(?<=[a-zà-ú]))(\d{2,3})(?= \d+(?:\.\d+)* [A-ZÀ-Ú]| ?$)", s)
    toc = [{"n": n, "titulo": t.strip().rstrip(".").strip(), "pagina": int(p)} for n, t, p in ents]
    toc.append({"n": "", "titulo": "REFERÊNCIAS", "pagina": 803})
    for i in range(len(toc) - 1):
        assert toc[i]["pagina"] <= toc[i + 1]["pagina"], f"sumário fora de ordem em {toc[i]['n']}"
    for t in toc:
        t["slug"] = t["n"].replace(".", "-") if t["n"] else "referencias"
    return toc


def estilo(span):
    f = span["font"]
    return ("Bold" in f, "Italic" in f)


def html_spans(spans, limite):
    """Converte spans em HTML mínimo. Números em corpo menor que o limite viram chamadas de nota."""
    saida = []
    for s in spans:
        t = s["text"]
        if not t:
            continue
        if s["size"] < limite and t.strip().isdigit():
            n = t.strip()
            saida.append(f'<sup class="nota-ref"><a href="#n{n}" id="r{n}">{n}</a></sup>')
            continue
        negrito, italico = estilo(s)
        trecho = html.escape(t, quote=False)
        if italico:
            trecho = f"<em>{trecho}</em>"
        if negrito:
            trecho = f"<strong>{trecho}</strong>"
        saida.append(trecho)
    h = "".join(saida)
    return h.replace("</em><em>", "").replace("</strong><strong>", "")


def juntar(atual, novo):
    if not atual:
        return novo.lstrip()
    limpo = re.sub(r"<[^>]+>", "", atual).rstrip()
    if limpo.endswith("-") and len(limpo) > 1 and limpo[-2].isalpha():
        return atual.rstrip() + novo.lstrip()
    return atual.rstrip() + " " + novo.lstrip()


def ler_resumo(doc):
    """Resumo e palavras-chave em português, transcritos da folha de resumo."""
    for i in range(8, 20):
        texto = doc[i].get_text()
        if "RESUMO" in texto and "Palavras-chave" in texto:
            corpo = texto[texto.index("RESUMO") + len("RESUMO"):texto.index("Palavras-chave")]
            chaves = texto[texto.index("Palavras-chave") + len("Palavras-chave"):].lstrip(": ")
            juntar_linhas = lambda t: norm(re.sub(r"(?<=[A-Za-zÀ-ú])-\s*\n\s*(?=[a-zà-ú])", "-", t))
            return {"pagina_pdf": i + 1, "texto": juntar_linhas(corpo),
                    "palavras_chave": [norm(k).rstrip(".") for k in juntar_linhas(chaves).split(";")]}
    return None


def main():
    doc = pymupdf.open(PDF)
    toc = ler_sumario(doc)
    paginas_epigrafe = {e["pagina_pdf"]: e for e in EPIGRAFES["epigrafes"]}

    secoes = []
    for t in toc:
        secoes.append({**t, "blocos": [], "pagina_inicio": t["pagina"], "pagina_fim": t["pagina"]})
    proxima = 0          # índice da próxima seção a abrir
    atual = None         # seção corrente
    bloco = None         # bloco de texto aberto
    marca_pendente = None
    notas = {}
    ultima_nota = None
    titulo_em_curso = None
    epigrafe_pendente = []

    def fechar_bloco():
        nonlocal bloco
        if bloco and bloco["html"].strip() and atual is not None:
            atual["blocos"].append(bloco)
        bloco = None

    def abrir_bloco(tipo):
        nonlocal bloco, marca_pendente
        fechar_bloco()
        bloco = {"tipo": tipo, "html": ""}
        if marca_pendente:
            bloco["html"] = marca_pendente
            marca_pendente = None

    def acrescentar(texto):
        nonlocal marca_pendente
        if marca_pendente:
            bloco["html"] = juntar(bloco["html"], marca_pendente)
            marca_pendente = None
        bloco["html"] = juntar(bloco["html"], texto)

    for pdf_n in range(PRIMEIRA + DESLOCAMENTO, ULTIMA + DESLOCAMENTO + 1):
        impressa = pdf_n - DESLOCAMENTO
        if pdf_n in paginas_epigrafe:
            epigrafe_pendente.append(paginas_epigrafe[pdf_n])
            continue
        pagina = doc[pdf_n - 1]
        linhas = []
        for b in pagina.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                spans = [s for s in l["spans"] if s["text"] != ""]
                if spans:
                    linhas.append((round(l["bbox"][1], 1), l["bbox"][0], spans))
        linhas.sort(key=lambda x: (x[0], x[1]))
        corpo12 = [round(x) for y, x, sp in linhas if y > 60 and any(abs(s["size"] - 12) < 0.3 and s["text"].strip() for s in sp)]
        margem = min((x for x in set(corpo12) if corpo12.count(x) > 3), default=85) if corpo12 else 85
        marca_pendente = f'<span class="pg-marca" id="p{impressa}">p. {impressa}</span>'
        em_notas = False

        for y, x, spans in linhas:
            if y < 60:
                continue
            visiveis = [s for s in spans if s["text"].strip()]
            texto = norm("".join(s["text"] for s in spans))
            primeiro = visiveis[0] if visiveis else spans[0]

            # Nota de rodapé que começa nesta linha.
            if visiveis and primeiro["size"] < 7.2 and primeiro["text"].strip().isdigit():
                em_notas = True
                n = primeiro["text"].strip()
                resto = spans[spans.index(primeiro) + 1:]
                notas[n] = {"n": n, "html": html_spans(resto, 0).strip(), "pagina": impressa}
                ultima_nota = n
                continue
            # Continuação de nota, nesta página ou vinda da anterior.
            if visiveis and abs(primeiro["size"] - 10.1) < 0.3 and abs(x - margem) < 4:
                if ultima_nota:
                    notas[ultima_nota]["html"] = juntar(notas[ultima_nota]["html"], html_spans(spans, 0).strip())
                em_notas = True
                continue
            if em_notas:
                continue
            if not visiveis:
                if titulo_em_curso is None:
                    fechar_bloco()
                continue

            # Título de seção, conferido contra o sumário.
            if proxima < len(secoes):
                alvo = secoes[proxima]
                rotulo = (alvo["n"] + " " + alvo["titulo"]) if alvo["n"] else alvo["titulo"]
                if titulo_em_curso is None and abs(impressa - alvo["pagina"]) <= 1 and chave(rotulo).startswith(chave(texto)[:12]) and chave(texto)[:6] == chave(rotulo)[:6]:
                    fechar_bloco()
                    atual = alvo
                    atual["pagina_inicio"] = impressa
                    proxima += 1
                    titulo_em_curso = chave(texto)
                    atual["titulo_html"] = html_spans(spans, 8.5).strip()
                    if epigrafe_pendente:
                        atual["epigrafes"] = epigrafe_pendente
                        epigrafe_pendente = []
                    if marca_pendente:
                        atual["blocos"].append({"tipo": "marca", "html": marca_pendente})
                        marca_pendente = None
                    else:
                        # A seção começa no meio da página. Repete a marca para que a página tenha âncora aqui também.
                        atual["blocos"].append({"tipo": "marca", "html": f'<span class="pg-marca" id="p{impressa}" title="Esta seção começa no meio da página {impressa}">p. {impressa}</span>'})
                    if len(titulo_em_curso) >= len(chave(rotulo)) - 2:
                        titulo_em_curso = None
                    continue
                if titulo_em_curso is not None:
                    titulo_em_curso += chave(texto)
                    atual["titulo_html"] = juntar(atual["titulo_html"], html_spans(spans, 8.5).strip())
                    if len(titulo_em_curso) >= len(chave(rotulo if proxima == 0 else (secoes[proxima - 1]["n"] + " " + secoes[proxima - 1]["titulo"]))) - 2:
                        titulo_em_curso = None
                    continue
            if atual is None:
                continue
            atual["pagina_fim"] = impressa

            h = html_spans(spans, 8.5)
            tamanho = primeiro["size"]
            if abs(tamanho - 10.1) < 0.3 and x >= margem + 40:
                if not bloco or bloco["tipo"] != "citacao":
                    abrir_bloco("citacao")
                acrescentar(h)
            elif abs(x - margem) < 4 and bloco and bloco["tipo"] == "p":
                acrescentar(h)
            else:
                abrir_bloco("p")
                acrescentar(h)
        if not em_notas and bloco is None and marca_pendente and atual is not None:
            atual["blocos"].append({"tipo": "marca", "html": marca_pendente})
            marca_pendente = None
    fechar_bloco()

    # Cada seção recebe as notas que chama.
    for s in secoes:
        chamadas = re.findall(r'id="r(\d+)"', s.get("titulo_html", ""))
        for b in s["blocos"]:
            chamadas += re.findall(r'id="r(\d+)"', b["html"])
        s["notas"] = [notas[n] for n in dict.fromkeys(chamadas) if n in notas]
        s["paginas"] = sorted({int(p) for b in s["blocos"] for p in re.findall(r'id="p(\d+)"', b["html"])})
    faltando = [s["n"] or s["titulo"] for s in secoes if not s["blocos"]]
    dados = {"fonte": PDF.name, "deslocamento": DESLOCAMENTO, "secoes": secoes, "resumo": ler_resumo(doc),
             "epigrafe_abertura": [e for e in EPIGRAFES["epigrafes"] if e["pagina_pdf"] < PRIMEIRA + DESLOCAMENTO]}
    SAIDA.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    total_notas = sum(len(s["notas"]) for s in secoes)
    print(f"{len(secoes)} seções, {total_notas} notas, {len(notas)} notas lidas. Seções vazias {faltando}")


if __name__ == "__main__":
    main()
