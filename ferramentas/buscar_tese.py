"""Busca na tese pela página impressa.

Uso
    python3 ferramentas/buscar_tese.py "expressão regular" [página inicial] [página final] [janela] [máximo]

Mostra cada ocorrência com o número da página impressa e um trecho em volta. Serve para achar o texto
exato antes de citar e para conferir se uma afirmação do site está na tese. A página impressa é a do PDF
menos 2. Requer pdftotext (poppler-utils), como o conferir_citacoes.py.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from conferir_citacoes import paginas  # noqa: E402

padrao = re.compile(sys.argv[1], re.I)
inicio = int(sys.argv[2]) if len(sys.argv) > 2 else -5
fim = int(sys.argv[3]) if len(sys.argv) > 3 else 9999
janela = int(sys.argv[4]) if len(sys.argv) > 4 else 300
maximo = int(sys.argv[5]) if len(sys.argv) > 5 else 40
achados = 0
for numero, texto in sorted(paginas().items()):
    if not inicio <= numero <= fim:
        continue
    texto = re.sub(r"\s+", " ", texto)
    for m in padrao.finditer(texto):
        print(f"[p. {numero}] …{texto[max(0, m.start() - janela):m.end() + janela]}…\n")
        achados += 1
        if achados >= maximo:
            sys.exit()
