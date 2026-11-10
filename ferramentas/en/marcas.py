"""Troca as etiquetas em linha de um segmento por marcas numeradas e desfaz a troca.

<span class="x">texto</span> vira <1>texto</1>. Etiqueta sem fechamento vira <2/>.
O tradutor devolve as mesmas marcas, e a volta repõe as etiquetas originais.
"""
import re

ETIQUETA = re.compile(r"""<(/?)([a-zA-Z][a-zA-Z0-9]*)((?:\s+[^\s=/>]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+))?)*)\s*(/?)>""")
VAZIAS = {"br", "img", "input", "wbr", "hr"}


def marcar(s):
    pilha, abre, fecha, n = [], {}, {}, 0
    saida, pos = [], 0
    for m in ETIQUETA.finditer(s):
        saida.append(s[pos:m.start()])
        pos = m.end()
        barra, nome = m.group(1), m.group(2).lower()
        if barra:
            i = pilha.pop() if pilha else None
            if i is None:
                raise ValueError("fechamento sem abertura")
            fecha[i] = m.group(0)
            saida.append(f"</{i}>")
        elif nome in VAZIAS or m.group(4):
            n += 1
            abre[n] = m.group(0)
            saida.append(f"<{n}/>")
        else:
            n += 1
            abre[n] = m.group(0)
            pilha.append(n)
            saida.append(f"<{n}>")
    saida.append(s[pos:])
    return "".join(saida), {"abre": abre, "fecha": fecha}


MARCA = re.compile(r"<(/?)(\d+)(/?)>")


def assinatura(s):
    return sorted(m.group(0) for m in MARCA.finditer(s))


def desmarcar(t, mapa):
    abre = {int(k): v for k, v in mapa["abre"].items()}
    fecha = {int(k): v for k, v in mapa["fecha"].items()}

    def troca(m):
        i = int(m.group(2))
        return fecha[i] if m.group(1) else abre[i]
    return MARCA.sub(troca, t)


if __name__ == "__main__":
    s = 'Veja <a href="x">o <b>link</b></a> e<br> <span class="pg" data-x=\'{"a": "<b>"}\'>p. 3</span>.'
    m, mp = marcar(s)
    print(m)
    assert desmarcar(m, mp) == s
