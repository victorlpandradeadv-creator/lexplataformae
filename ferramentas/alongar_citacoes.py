"""Alonga as citações que começam no meio da frase até o começo dela.

Uso
    python3 -I ferramentas/alongar_citacoes.py [--aplicar] arquivo.md [outros.md ...]

Para cada linha no formato "> trecho (p. N)" cujo trecho começa no meio de uma frase da tese,
o script acha a frase na página indicada e acrescenta o que vem antes, desde o começo da frase.
Quando faltam mais de 25 palavras até o começo da frase, o trecho passa a abrir com [...] e
com a oração que vem logo antes dele, para que o contexto imediato apareça.
Sem --aplicar, só relata. Depois de aplicar, rodar conferir_citacoes.py. Feito em 04/11/2026.
"""
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from conferir_citacoes import paginas  # noqa: E402

LIMITE = 25
ABREV = {"art", "arts", "p", "pp", "n", "nº", "cf", "al", "inc", "ex", "v", "sr", "sra", "dr", "dra", "ed", "org", "coord",
         "vol", "cap", "fl", "fls", "op", "cit", "ibid", "id", "etc", "séc", "aprox", "min", "rel", "j", "s", "ss"}
ASPAS = {'"': '["“”]', "“": '["“”]', "”": '["“”]', "'": "['‘’]", "‘": "['‘’]", "’": "['‘’]"}


def semi(texto):
    """Texto da página com espaços normalizados e sem chamadas de nota, mas com as aspas originais."""
    texto = unicodedata.normalize("NFC", texto).replace("\xad", "")
    texto = re.sub(r'(?:(?<=[A-Za-zÀ-úºª,;:"”’])|(?<=[A-Za-zÀ-úºª"”’]\.))\d{1,3}(?=[\s,\.])', "", texto)
    # A linha vazia do PDF separa parágrafos e títulos, e fica como quebra, que conta como começo de frase.
    texto = re.sub(r"[ \t]+", " ", texto)
    return re.sub(r" *\n[\s]*", "\n", texto).strip()


PAG = {k: semi(v) for k, v in paginas().items()}


def padrao(palavras):
    return r"\s+".join("".join(ASPAS.get(c, re.escape(c)) for c in w) for w in palavras)


def fronteira(texto, j):
    """True se a posição j (um ponto, interrogação ou exclamação) fecha uma frase."""
    if texto[j] == "\n":
        return True
    if texto[j] not in ".?!…":
        return False
    resto = texto[j + 1:j + 4]
    if not re.match(r'["”’)]?\s+["“(]?[A-ZÁÉÍÓÚÂÊÔÃÕÇÀÈÌÒÙ]', resto + texto[j + 4:j + 8]):
        return False
    if texto[j] == ".":
        antes = re.search(r"([\wºª]+)$", texto[max(0, j - 12):j])
        palavra = antes.group(1) if antes else ""
        if palavra.lower() in ABREV or (len(palavra) == 1 and palavra.isupper()) or palavra.isdigit():
            return False
    return True


def contexto(trecho, ref):
    """Devolve o que vem antes do trecho na frase da tese, ou None se não der para achar com segurança."""
    m = re.search(r"p\. (\d+)(?:-(\d+))?", ref)
    a, b = int(m.group(1)), int(m.group(2) or m.group(1))
    palavras = trecho.split()
    for n in (10, 7, 5):
        if len(palavras) < n:
            continue
        pat = padrao(palavras[:n])
        for pg in range(a, b + 1):
            texto = PAG.get(pg, "")
            achado = re.search(pat, texto)
            if not achado:
                continue
            i = achado.start()
            j = i - 1
            while j >= 0 and i - j < 1500:
                if fronteira(texto, j):
                    inicio = j + 1
                    while inicio < i and texto[inicio] in ' "”’)\n':
                        inicio += 1
                    antes = texto[inicio:i].strip()
                    # Contexto com resto de chamada de nota colado a número ou a parêntese fica de fora.
                    if re.search(r"\)\d|\b\d{5,}\b|art\. \d{4,}", antes):
                        return None
                    return antes.replace("\n", " ")
                j -= 1
            return None
    return None


def alongar(trecho, ref):
    t = trecho.strip()
    if t.startswith("[...]"):
        return None
    primeira = t.lstrip("“\"'(")[:1]
    antes = contexto(t, ref)
    if antes is None:
        return None
    ult = antes[-1:] if antes else ""
    if not (primeira.islower() or (ult and (ult.islower() or ult == ","))):
        return None
    if not antes:
        return None
    palavras = antes.split()
    if len(palavras) <= LIMITE:
        return f"{antes} {t}"
    def aceitavel(resto):
        return (4 <= len(resto.split()) <= LIMITE and not re.match(r'["“”(\[\d]', resto)
                and resto.count(")") <= resto.count("(") and resto.count("”") <= resto.count("“"))
    corte = None
    for m in re.finditer(r"[,;:]\s", antes):
        resto = antes[m.end():]
        if aceitavel(resto):
            corte = resto
            break
    if corte is None:
        for k in range(len(palavras) - LIMITE, len(palavras) - 3):
            resto = " ".join(palavras[k:])
            if aceitavel(resto):
                corte = resto
                break
    if corte is None:
        return None
    return f"[...] {corte} {t}"


def main(args):
    aplicar = "--aplicar" in args
    arquivos = [a for a in args if not a.startswith("--")]
    total = 0
    for arq in arquivos:
        p = Path(arq)
        linhas = p.read_text(encoding="utf-8").split("\n")
        n = 0
        for k, linha in enumerate(linhas):
            m = re.match(r"^> (.+?) \((p\. [\d\-]+)\)\s*$", linha)
            if not m:
                continue
            novo = alongar(m.group(1), m.group(2))
            if novo and novo != m.group(1):
                n += 1
                if not aplicar:
                    print(f"{arq}:{k + 1}\n   antes  {m.group(1)[:110]}\n   depois {novo[:160]}")
                linhas[k] = f"> {novo} ({m.group(2)})"
        total += n
        print(f"{arq}  {n} citações alongadas")
        if aplicar:
            p.write_text("\n".join(linhas), encoding="utf-8")
    print(f"total {total}")


if __name__ == "__main__":
    main(sys.argv[1:])
