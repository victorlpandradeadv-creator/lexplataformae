"""Versão escura das ilustrações, por negativo calculado. 15/11/2026, por ordem do autor.

Cada peça clara em site/ilustracoes/<id>.webp ganha <id>-escuro.webp. O papel creme vira o papel escuro do site, o traço
escuro vira a tinta clara do tema escuro, e o azul da armadura mantém o matiz, só com a claridade ajustada para o fundo
escuro. A conta é feita em OKLab, para que a troca de claridade não mude a cor. Peças novas devem nascer já com a versão
escura definida na encomenda, e este script serve ao acervo que já existe.
Uso: python3 ferramentas/negativo.py [id ...]
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

RAIZ = Path(__file__).resolve().parents[1]
PASTA = RAIZ / "site" / "ilustracoes"


def srgb_para_linear(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def linear_para_srgb(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(c, 1 / 2.4) - 0.055)


def para_oklab(rgb):
    l = srgb_para_linear(rgb)
    m1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929], [0.2119034982, 0.6806995451, 0.1073969566], [0.0883024619, 0.2817188376, 0.6299787005]])
    m2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468], [1.9779984951, -2.4285922050, 0.4505937099], [0.0259040371, 0.7827717662, -0.8086757660]])
    lms = np.cbrt(l @ m1.T)
    return lms @ m2.T


def de_oklab(lab):
    m2i = np.array([[1, 0.3963377774, 0.2158037573], [1, -0.1055613458, -0.0638541728], [1, -0.0894841775, -1.2914855480]])
    m1i = np.array([[4.0767416621, -3.3077115913, 0.2309699292], [-1.2684380046, 2.6097574011, -0.3413193965], [-0.0041960863, -0.7034186147, 1.7076147010]])
    lms = (lab @ m2i.T) ** 3
    return linear_para_srgb(lms @ m1i.T)


def hex_lab(h):
    rgb = np.array([[int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]])
    return para_oklab(rgb)[0]


PAPEL_CLARO, TINTA_CLARA = hex_lab("#faf6ef"), hex_lab("#211c17")
PAPEL_ESCURO, TINTA_ESCURA = hex_lab("#1e1a16"), hex_lab("#ebe7e1")


def negativo(arq):
    im = Image.open(arq).convert("RGB")
    rgb = np.asarray(im).astype(np.float64) / 255
    lab = para_oklab(rgb.reshape(-1, 3))
    L, a, b = lab[:, 0], lab[:, 1], lab[:, 2]
    croma = np.hypot(a, b)
    # Claridade invertida no intervalo do site. O papel claro cai no papel escuro e a tinta escura na tinta clara.
    t = (L - PAPEL_CLARO[0]) / (TINTA_CLARA[0] - PAPEL_CLARO[0])
    L_neutro = PAPEL_ESCURO[0] + t * (TINTA_ESCURA[0] - PAPEL_ESCURO[0])
    # O que tem cor guarda o matiz. A claridade sobe só o bastante para ler sobre o escuro.
    peso = np.clip((croma - 0.03) / 0.07, 0, 1)
    L_cor = np.clip(L * 0.85 + 0.18, 0, 0.82)
    L2 = (1 - peso) * L_neutro + peso * L_cor
    # O neutro ganha o tom quente do papel escuro, como o papel claro tinha o seu.
    a2 = (1 - peso) * (PAPEL_ESCURO[1] + (a - PAPEL_CLARO[1]) * 0.6) + peso * a
    b2 = (1 - peso) * (PAPEL_ESCURO[2] + (b - PAPEL_CLARO[2]) * 0.6) + peso * b
    out = de_oklab(np.stack([L2, a2, b2], axis=1)).reshape(rgb.shape)
    destino = arq.with_name(arq.stem + "-escuro.webp")
    Image.fromarray((out * 255 + 0.5).astype(np.uint8)).save(destino, "WEBP", quality=82, method=6)
    return destino


if __name__ == "__main__":
    alvos = sys.argv[1:] or sorted(p.stem for p in PASTA.glob("*.webp") if not p.stem.endswith("-escuro"))
    for ident in alvos:
        print(negativo(PASTA / f"{ident}.webp").name)
