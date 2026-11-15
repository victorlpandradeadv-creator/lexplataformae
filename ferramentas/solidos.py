"""Sólidos da linguagem geométrica da propriedade intelectual, lidos de estrutura/solidos.md.

Feito em 15/11/2026, a partir de estrutura/ilustracoes-pi.md. Cada peça sai em SVG, por projeção
isométrica fixa, com o mesmo ângulo e a mesma espessura de linha em todas as peças. As cores vêm
das variáveis do site (--tinta, --tinta-2, --papel e --sol-azul), de modo que o tema escuro sai sem
versão própria. Cada SVG traz título e descrição para leitor de tela.

Uso.
    python3 ferramentas/solidos.py            gera estrutura/rascunhos/solidos/*.svg e a prancha
    python3 ferramentas/solidos.py <id>       gera só a peça <id>

O gerador do site pode chamar svg(ident) para ter a peça pronta. Nenhuma frase nasce aqui. Os
rótulos e o texto alternativo vêm de estrutura/solidos.md.

Gramática (seção 5 do plano).
    sólido em traço simples      dimensão do objeto, antes de qualquer direito
    contorno de incidência       linha dupla fina em tinta, rente ao que protege
    fluxo azul                   faixa larga sem ponta, a fruição funcional
    vetor                        linha fina com ponta, identificação ou referência
    tracejado cinza              poder da plataforma sobre a fruição, que não decorre da exclusividade
"""
import math
import re
import sys
from html import escape
from pathlib import Path

from shapely.geometry import LineString, MultiPoint, Point, Polygon
from shapely.ops import unary_union

RAIZ = Path(__file__).resolve().parents[1]
PLANO = RAIZ / "estrutura" / "solidos.md"
SAIDA = RAIZ / "estrutura" / "rascunhos" / "solidos"

C30, S30 = math.cos(math.radians(30)), 0.5
TRACO = 1.6          # espessura do sólido
TRACO_FINO = 1.1     # contorno de incidência e linhas internas
FLUXO = 10           # largura da faixa azul
DUPLA = (7, 11)      # afastamento das duas linhas do contorno
TAM = 60             # aresta padrão


# ---------------------------------------------------------------- geometria

def iso(x, y, z=0.0):
    return ((x - y) * C30, (x + y) * S30 - z)


def _p(pts):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def _d(pts, fechar=False):
    if not pts:
        return ""
    s = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}" + "".join(f" L{x:.1f},{y:.1f}" for x, y in pts[1:])
    return s + (" Z" if fechar else "")


def _anel(geom):
    """Contorno exterior de um polígono shapely como caminho SVG."""
    if geom.is_empty:
        return ""
    polys = [geom] if geom.geom_type == "Polygon" else list(geom.geoms)
    return " ".join(_d(list(p.exterior.coords), True) for p in polys)


class Solido:
    """Um sólido posto no papel. (cx, cy) é o centro da base na tela."""

    def __init__(self, tipo, nome, cx, cy, tam=TAM, transparente=False):
        self.tipo, self.nome, self.cx, self.cy, self.a = tipo, nome, cx, cy, tam
        self.transparente = transparente
        self.visiveis, self.ocultas, self.silhueta = [], [], []
        self.extra = []          # caminhos SVG adicionais (padrão, sinal, mecanismo)
        getattr(self, "_" + tipo)()

    # coordenadas locais com a base centrada na origem
    def _t(self, x, y, z=0.0):
        X, Y = iso(x, y, z)
        return (self.cx + X, self.cy + Y)

    def _cubo(self):
        h = self.a / 2
        v = {(i, j, k): self._t(i * h, j * h, k * self.a) for i in (-1, 1) for j in (-1, 1) for k in (0, 1)}
        arestas = [((-1, -1, 0), (1, -1, 0)), ((-1, -1, 0), (-1, 1, 0)), ((-1, -1, 0), (-1, -1, 1)),
                   ((1, -1, 0), (1, 1, 0)), ((-1, 1, 0), (1, 1, 0)), ((1, -1, 0), (1, -1, 1)),
                   ((-1, 1, 0), (-1, 1, 1)), ((1, 1, 0), (1, 1, 1)), ((-1, -1, 1), (1, -1, 1)),
                   ((-1, -1, 1), (-1, 1, 1)), ((1, -1, 1), (1, 1, 1)), ((-1, 1, 1), (1, 1, 1))]
        for u, w in arestas:
            (self.ocultas if (-1, -1, 0) in (u, w) else self.visiveis).append([v[u], v[w]])
        self.silhueta = list(v.values())
        self.topo = self._t(0, 0, self.a)
        self.altura = self.a

    def _piramide(self):
        h, alt = self.a / 2, self.a * 1.15
        b = {(i, j): self._t(i * h, j * h) for i in (-1, 1) for j in (-1, 1)}
        ap = self._t(0, 0, alt)
        for u, w in [((-1, -1), (1, -1)), ((-1, -1), (-1, 1))]:
            self.ocultas.append([b[u], b[w]])
        for u, w in [((1, -1), (1, 1)), ((-1, 1), (1, 1))]:
            self.visiveis.append([b[u], b[w]])
        self.ocultas.append([b[(-1, -1)], ap])
        for k in [(1, -1), (1, 1), (-1, 1)]:
            self.visiveis.append([b[k], ap])
        self.silhueta = list(b.values()) + [ap]
        self.base = [b[(-1, -1)], b[(1, -1)], b[(1, 1)], b[(-1, 1)]]
        self.apice = ap
        self.topo = ap
        self.altura = alt

    def _elipse(self, r, z, t0=0.0, t1=360.0, n=72):
        return [self._t(r * math.cos(math.radians(t)), r * math.sin(math.radians(t)), z)
                for t in [t0 + (t1 - t0) * i / n for i in range(n + 1)]]

    def _cilindro(self):
        r, alt = self.a * 0.5, self.a * 1.05
        self.visiveis.append(self._elipse(r, alt))
        self.visiveis.append(self._elipse(r, 0, -45, 135, 36))
        self.ocultas.append(self._elipse(r, 0, 135, 315, 36))
        for t in (-45, 135):
            x, y = r * math.cos(math.radians(t)), r * math.sin(math.radians(t))
            self.visiveis.append([self._t(x, y, 0), self._t(x, y, alt)])
        self.silhueta = self._elipse(r, alt) + self._elipse(r, 0)
        self.r, self.topo, self.altura = r, self._t(0, 0, alt), alt

    def _esfera(self):
        r = self.a * 0.5
        R = r * math.sqrt(2) * C30
        cx, cy = self._t(0, 0, R)
        self.centro, self.R = (cx, cy), R
        circ = [(cx + R * math.cos(math.radians(t)), cy + R * math.sin(math.radians(t))) for t in range(0, 361, 5)]
        self.visiveis.append(circ)
        eq = [self._t(r * math.cos(math.radians(t)), r * math.sin(math.radians(t)), R) for t in range(-45, 136, 5)]
        eq_t = [self._t(r * math.cos(math.radians(t)), r * math.sin(math.radians(t)), R) for t in range(135, 316, 5)]
        self.visiveis.append(eq)
        self.ocultas.append(eq_t)
        self.silhueta = circ
        self.topo = (cx, cy - R)
        self.altura = 2 * R

    # forma e borda
    def forma(self):
        return MultiPoint(self.silhueta).convex_hull

    def ponto_saida(self, dx, dy):
        """Ponto da silhueta na direção (dx, dy), a partir do centro da forma."""
        f = self.forma()
        c = f.centroid
        n = math.hypot(dx, dy) or 1
        raio = LineString([(c.x, c.y), (c.x + dx / n * 900, c.y + dy / n * 900)])
        i = raio.intersection(f.exterior)
        if i.is_empty:
            return (c.x, c.y)
        pts = [i] if i.geom_type == "Point" else list(getattr(i, "geoms", [i]))
        p = max(pts, key=lambda q: q.distance(Point(c.x, c.y)))
        return (p.x, p.y)

    def svg(self):
        out = []
        if self.tipo == "esfera" and getattr(self, "aberta", False):
            return "".join(self.extra)
        for linha in self.ocultas:
            classe = "s-transp" if self.transparente else "s-oculta"
            out.append(f'<path class="{classe}" d="{_d(linha)}"/>')
        for linha in self.visiveis:
            out.append(f'<path class="s-linha" d="{_d(linha)}"/>')
        out.extend(self.extra)
        return "".join(out)


# ---------------------------------------------------------------- acessórios

def corte(s):
    """Esfera em corte, com um mecanismo simples de engrenagens dentro."""
    cx, cy, R = s.centro[0], s.centro[1], s.R
    s.aberta = True
    meia = [(cx + R * math.cos(math.radians(t)), cy + R * math.sin(math.radians(t))) for t in range(0, 181, 5)]
    tampa = [(cx + R * math.cos(math.radians(t)), cy + 0.38 * R * math.sin(math.radians(t))) for t in range(0, 361, 5)]
    tampa_atras = [(cx + R * math.cos(math.radians(t)), cy + 0.38 * R * math.sin(math.radians(t))) for t in range(180, 361, 5)]
    calota = [(cx + R * math.cos(math.radians(t)), cy - 0.25 * R + R * math.sin(math.radians(t)) * 0.9) for t in range(180, 361, 5)]
    out = [f'<path class="s-linha" d="{_d(meia)}"/>', f'<path class="s-linha" d="{_d(tampa, True)}"/>',
           f'<path class="s-oculta" d="{_d(calota)}"/>']
    engs = [(cx - R * 0.28, cy - R * 0.02, R * 0.3, 8), (cx + R * 0.3, cy + R * 0.02, R * 0.22, 6)]
    mec = []
    for ex, ey, er, dentes in engs:
        pts = []
        for i in range(dentes * 4):
            t = 2 * math.pi * i / (dentes * 4)
            rr = er if (i % 4) in (0, 1) else er * 0.78
            pts.append((ex + rr * math.cos(t), ey + rr * 0.42 * math.sin(t)))
        out.append(f'<path class="s-mec" d="{_d(pts, True)}"/>')
        out.append(f'<ellipse class="s-mec" cx="{ex:.1f}" cy="{ey:.1f}" rx="{er * 0.25:.1f}" ry="{er * 0.11:.1f}"/>')
        mec += pts
    s.extra = out
    s.mecanismo = MultiPoint(mec).convex_hull
    s.silhueta = meia + tampa


def padrao(s):
    """Linhas de padrão na superfície visível do cilindro."""
    out = []
    for frac in (0.25, 0.5, 0.75):
        z = s.altura * frac
        out.append(f'<path class="s-padrao" d="{_d(s._elipse(s.r, z, -45, 135, 36))}"/>')
    for t in (0, 45, 90):
        x, y = s.r * math.cos(math.radians(t)), s.r * math.sin(math.radians(t))
        out.append(f'<path class="s-padrao" d="{_d([s._t(x, y, 0), s._t(x, y, s.altura)])}"/>')
    s.extra += out


def pele(s, x, y):
    """A superfície do cilindro desenrolada num retângulo, com o mesmo padrão."""
    w, h = 2 * math.pi * s.r * 0.62, s.altura
    x0, y0 = x, y - h
    out = [f'<rect class="s-linha" x="{x0:.1f}" y="{y0:.1f}" width="{w:.1f}" height="{h:.1f}" fill="none"/>']
    for frac in (0.25, 0.5, 0.75):
        out.append(f'<path class="s-padrao" d="M{x0:.1f},{y0 + h * frac:.1f} H{x0 + w:.1f}"/>')
    for i in range(1, 8):
        out.append(f'<path class="s-padrao" d="M{x0 + w * i / 8:.1f},{y0:.1f} V{y0 + h:.1f}"/>')
    return "".join(out), Polygon([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)])


def sinal(s):
    """Figura simples na face frontal da pirâmide, círculo dentro de um quadrado."""
    b, ap = s.base, s.apice
    # face frontal direita, entre b[1], b[2] e o ápice
    p1, p2 = b[1], b[2]
    cx = (p1[0] + p2[0] + ap[0]) / 3
    cy = (p1[1] + p2[1] + ap[1]) / 3 + 4
    r = s.a * 0.12
    s.extra.append(f'<ellipse class="s-sinal" cx="{cx:.1f}" cy="{cy:.1f}" rx="{r:.1f}" ry="{r * 1.1:.1f}"/>')


def _seta(x0, y0, x1, y1, classe="s-vetor", ponta=7):
    ang = math.atan2(y1 - y0, x1 - x0)
    a1 = (x1 - ponta * math.cos(ang - 0.4), y1 - ponta * math.sin(ang - 0.4))
    a2 = (x1 - ponta * math.cos(ang + 0.4), y1 - ponta * math.sin(ang + 0.4))
    return (f'<path class="{classe}" d="M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}"/>'
            f'<path class="{classe}" d="M{a1[0]:.1f},{a1[1]:.1f} L{x1:.1f},{y1:.1f} L{a2[0]:.1f},{a2[1]:.1f}"/>')


def _fluxo_caminho(x0, y0, x1, y1):
    """Curva suave do sólido para o papel."""
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    cx, cy = mx - dy * 0.18, my + dx * 0.18
    return f"M{x0:.1f},{y0:.1f} Q{cx:.1f},{cy:.1f} {x1:.1f},{y1:.1f}", (cx, cy)


def _bezier(x0, y0, cx, cy, x1, y1, n=40):
    return [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1,
             (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1) for t in [i / n for i in range(n + 1)]]


# ---------------------------------------------------------------- composição

def _num(v):
    return float(v)


class Peca:
    def __init__(self, ident, campos):
        self.ident, self.campos = ident, campos
        self.solidos, self.camadas = {}, {"fundo": [], "tracejado": [], "solido": [], "contorno": [], "fluxo": [], "rotulo": []}
        self.formas = {}           # nome -> forma shapely, para contorno e tracejado
        self.fluxos = {}           # nome -> lista de pontos do fluxo
        self.limites = []

    def _forma(self, alvo):
        geoms = []
        for nome in alvo.split("+"):
            nome = nome.strip()
            if nome in self.formas:
                geoms.append(self.formas[nome])
            elif nome.startswith("fluxo:"):
                geoms.append(LineString(self.fluxos[nome[6:]]).buffer(FLUXO / 2 + 2))
            elif "." in nome:
                s, parte = nome.split(".", 1)
                geoms.append(getattr(self.solidos[s], parte))
            else:
                geoms.append(self.solidos[nome].forma())
        return unary_union(geoms)

    def executar(self, linha):
        tok = linha.split()
        cmd, args = tok[0], tok[1:]
        opc = {}
        pos = []
        i = 0
        while i < len(args):
            if args[i] in ("tam", "margem", "comprimento", "aneis", "largura"):
                opc[args[i]] = _num(args[i + 1])
                i += 2
            elif args[i] in ("transparente", "corta", "aberto", "desfeito", "fino", "contorno"):
                opc[args[i]] = True
                i += 1
            else:
                pos.append(args[i])
                i += 1
        if cmd == "solido":
            tipo, nome, x, y = pos[0], pos[1], _num(pos[2]), _num(pos[3])
            s = Solido(tipo, nome, x, y, opc.get("tam", TAM), opc.get("transparente", False))
            self.solidos[nome] = s
            self.formas[nome] = s.forma()
            self.limites.append(s.forma())
        elif cmd == "formacao":
            # sólido em formação, só em tracejado
            tipo, x, y = pos[0], _num(pos[1]), _num(pos[2])
            s = Solido(tipo, "_", x, y, opc.get("tam", TAM * 0.6))
            linhas = s.visiveis
            self.camadas["solido"].append("".join(f'<path class="s-formacao" d="{_d(l)}"/>' for l in linhas))
            self.limites.append(s.forma())
        elif cmd == "corte":
            corte(self.solidos[pos[0]])
            self.formas[pos[0]] = self.solidos[pos[0]].forma()
        elif cmd == "padrao":
            padrao(self.solidos[pos[0]])
        elif cmd == "pele":
            s = self.solidos[pos[0]]
            svg, forma = pele(s, _num(pos[1]), _num(pos[2]))
            self.camadas["solido"].append(svg)
            self.formas[pos[0] + ".pele"] = forma
            self.limites.append(forma)
        elif cmd == "sinal":
            sinal(self.solidos[pos[0]])
        elif cmd == "fluxo":
            s = self.solidos[pos[0]]
            dx, dy = _num(pos[1]), _num(pos[2])
            comp = opc.get("comprimento", 110)
            x0, y0 = s.ponto_saida(dx, dy)
            n = math.hypot(dx, dy) or 1
            x1, y1 = x0 + dx / n * comp, y0 + dy / n * comp
            _, (cx, cy) = _fluxo_caminho(x0, y0, x1, y1)
            self.fluxos[pos[0]] = _bezier(x0, y0, cx, cy, x1, y1)
            self.limites.append(LineString(self.fluxos[pos[0]]).buffer(FLUXO))
        elif cmd == "contorno":
            alvo = self._forma(pos[0])
            for d in DUPLA:
                self.camadas["contorno"].append(f'<path class="s-incidencia" d="{_anel(alvo.buffer(d, join_style=1))}"/>')
            if "aneis" in opc:
                for k in range(1, int(opc["aneis"]) + 1):
                    d = DUPLA[1] + 26 * k
                    self.camadas["contorno"].append(f'<path class="s-incidencia s-inchado" d="{_anel(alvo.buffer(d, join_style=1))}"/>')
                    self.camadas["contorno"].append(f'<path class="s-incidencia s-inchado" d="{_anel(alvo.buffer(d + 4, join_style=1))}"/>')
                self.limites.append(alvo.buffer(DUPLA[1] + 26 * int(opc["aneis"]) + 6))
        elif cmd == "contorno-linha":
            # contorno duplo ao longo de um vetor, para a pirâmide
            p = [tuple(map(float, q.split(","))) for q in pos[0:2]]
            g = LineString(p)
            for d in DUPLA:
                self.camadas["contorno"].append(f'<path class="s-incidencia" d="{_anel(g.buffer(d * 0.7, cap_style=1))}"/>')
        elif cmd == "base":
            s = self.solidos[pos[0]]
            g = Polygon(s.base)
            self.formas[pos[0] + ".base"] = g
        elif cmd == "vetor":
            s = self.solidos[pos[0]]
            x1, y1 = _num(pos[1]), _num(pos[2])
            x0, y0 = s.apice if hasattr(s, "apice") else s.topo
            self.camadas["fluxo"].append(_seta(x0, y0 - 2, x1, y1))
            if opc.get("contorno"):
                g = LineString([(x0, y0), (x1, y1)])
                for d in DUPLA:
                    self.camadas["contorno"].append(f'<path class="s-incidencia" d="{_anel(g.buffer(d * 0.8, cap_style=1))}"/>')
            self.camadas["fluxo"].append(f'<circle class="s-origem" cx="{x1:.1f}" cy="{y1:.1f}" r="3.2"/>')
            self.limites.append(Point(x1, y1).buffer(12))
        elif cmd == "vetorlargo":
            x0, y0, x1, y1 = map(_num, pos[:4])
            ang = math.atan2(y1 - y0, x1 - x0)
            w = opc.get("largura", 16)
            nx, ny = -math.sin(ang) * w / 2, math.cos(ang) * w / 2
            L = math.hypot(x1 - x0, y1 - y0) - 18
            bx, by = x0 + math.cos(ang) * L, y0 + math.sin(ang) * L
            pts = [(x0 + nx, y0 + ny), (bx + nx, by + ny), (bx + nx * 1.9, by + ny * 1.9), (x1, y1),
                   (bx - nx * 1.9, by - ny * 1.9), (bx - nx, by - ny), (x0 - nx, y0 - ny)]
            self.camadas["contorno"].append(f'<path class="s-largo" d="{_d(pts, True)}"/>')
            self.limites.append(Polygon(pts))
        elif cmd == "tracejado":
            alvo = self._forma(pos[0])
            g = alvo.convex_hull.buffer(opc.get("margem", 34), join_style=1)
            self.tracejado = g
            if opc.get("desfeito"):
                anel = g.exterior
                L = anel.length
                partes, t = [], 0.0
                k = 0
                while t < L:
                    tam = 14 if k % 3 else 6
                    seg = [anel.interpolate(t + u * tam / 6) for u in range(7)]
                    partes.append(f'<path class="s-plataforma s-desfeito" d="{_d([(p.x, p.y) for p in seg])}"/>')
                    t += tam + 22 + (k % 4) * 5
                    k += 1
                self.camadas["tracejado"].append("".join(partes))
            else:
                self.camadas["tracejado"].append(f'<path class="s-plataforma" d="{_anel(g)}"/>')
            self.limites.append(g)
        elif cmd == "etiqueta":
            x, y = _num(pos[0]), _num(pos[1])
            texto = " ".join(pos[2:])
            w = 10 + 7.4 * len(texto)
            self.camadas["rotulo"].append(
                f'<path class="s-fio" d="M{x:.1f},{y:.1f} l14,18"/>'
                f'<g transform="translate({x + 14:.1f},{y + 18:.1f}) rotate(-6)">'
                f'<path class="s-etiqueta" d="M0,0 h{w:.1f} v24 h-{w:.1f} l-8,-12 Z"/>'
                f'<circle class="s-linha" cx="2" cy="12" r="2"/>'
                f'<text class="s-etq" x="{w / 2 + 2:.1f}" y="16.5" text-anchor="middle">{escape(texto)}</text></g>')
            self.limites.append(Polygon([(x, y), (x + w + 30, y), (x + w + 30, y + 52), (x, y + 52)]))
        elif cmd == "ponte":
            nome = pos[0]
            x1, y1 = _num(pos[1]), _num(pos[2])
            fx, fy = self.fluxos[nome][-1]
            self.camadas["fluxo"].append(f'<path class="s-ponte" d="M{fx:.1f},{fy:.1f} L{x1:.1f},{y1:.1f}"/>')
            self.camadas["fluxo"].append(f'<rect class="s-chegada" x="{x1 - 16:.1f}" y="{y1 - 7:.1f}" width="32" height="14" rx="7"/>')
            self.limites.append(Point(x1, y1).buffer(20))
        elif cmd == "rotulo":
            alvo, texto = pos[0], " ".join(pos[1:])
            if alvo in self.solidos:
                s = self.solidos[alvo]
                f = s.forma()
                x, y = f.centroid.x, f.bounds[3] + 30
            else:
                x, y = map(float, alvo.split(","))
            self.camadas["rotulo"].append(f'<text class="s-rotulo" x="{x:.1f}" y="{y:.1f}" text-anchor="middle">{escape(texto)}</text>')
            self.limites.append(Polygon([(x - 4.2 * len(texto), y - 14), (x + 4.2 * len(texto), y - 14),
                                         (x + 4.2 * len(texto), y + 6), (x - 4.2 * len(texto), y + 6)]))
        elif cmd == "linha":
            # divisória discreta entre as metades de uma peça
            x0, y0, x1, y1 = map(_num, pos[:4])
            self.camadas["fundo"].append(f'<path class="s-divisa" d="M{x0},{y0} L{x1},{y1}"/>')
        else:
            raise ValueError(f"{self.ident}: comando desconhecido {cmd}")

    def _desenhar_fluxos(self):
        corta = getattr(self, "tracejado", None) if self.campos.get("_corta") else None
        for nome, pts in self.fluxos.items():
            if corta is not None and nome in self.campos.get("_corta"):
                linha = LineString(pts)
                dentro = linha.intersection(corta)
                fora = linha.difference(corta.buffer(6))
                if not dentro.is_empty:
                    self.camadas["fluxo"].append(f'<path class="s-fluxo s-fluxo-corte" d="{_d(list(dentro.coords))}"/>')
                if not fora.is_empty:
                    segs = [fora] if fora.geom_type == "LineString" else list(fora.geoms)
                    for sg in segs:
                        self.camadas["fluxo"].append(f'<path class="s-fluxo-oco" d="{_anel(sg.buffer(FLUXO / 2, cap_style=2))}"/>')
            else:
                self.camadas["fluxo"].append(f'<path class="s-fluxo" d="{_d(pts)}"/>')

    def svg(self):
        corta = [l.split()[1] for l in self.campos["desenho"] if l.startswith("fluxo") and " corta" in l]
        self.campos["_corta"] = corta
        for linha in self.campos["desenho"]:
            self.executar(linha)
        for s in self.solidos.values():
            self.camadas["solido"].append(s.svg())
        self._desenhar_fluxos()
        tudo = unary_union(self.limites)
        x0, y0, x1, y1 = tudo.bounds
        m = 18
        vb = f"{x0 - m:.0f} {y0 - m:.0f} {x1 - x0 + 2 * m:.0f} {y1 - y0 + 2 * m:.0f}"
        titulo = escape(self.campos.get("titulo", ""))
        alt = escape(self.campos.get("alt", ""))
        corpo = "".join(self.camadas[k] and "".join(self.camadas[k]) or "" for k in
                        ("fundo", "tracejado", "contorno", "fluxo", "solido", "rotulo"))
        return (f'<svg class="solidos" xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{x1 - x0 + 2 * m:.0f}" height="{y1 - y0 + 2 * m:.0f}" role="img" '
                f'aria-labelledby="{self.ident}-t {self.ident}-d" data-peca="{self.ident}">'
                f'<title id="{self.ident}-t">{titulo}</title><desc id="{self.ident}-d">{alt}</desc>'
                f'<style>{ESTILO}</style>{corpo}</svg>')


ESTILO = (
    ".solidos{--s-t:var(--tinta,#211c17);--s-t2:var(--tinta-2,#615953);--s-az:var(--sol-azul,#002fa7);--s-p:var(--papel,#faf6ef)}"
    ".solidos path,.solidos ellipse,.solidos rect,.solidos circle{fill:none;stroke-linecap:round;stroke-linejoin:round}"
    ".s-linha{stroke:var(--s-t);stroke-width:1.6}"
    ".s-oculta{stroke:var(--s-t2);stroke-width:1.1;stroke-dasharray:3 4}"
    ".s-transp{stroke:var(--s-t2);stroke-width:1.1}"
    ".s-mec{stroke:var(--s-t);stroke-width:1.1}"
    ".s-padrao{stroke:var(--s-t2);stroke-width:1.1}"
    ".s-sinal{stroke:var(--s-t);stroke-width:1.4}"
    ".s-incidencia{stroke:var(--s-t);stroke-width:1.1}"
    ".s-inchado{stroke-opacity:.75}"
    ".s-largo{stroke:var(--s-t);stroke-width:1.1}"
    ".s-plataforma{stroke:var(--s-t2);stroke-width:1.8;stroke-dasharray:7 6}"
    ".s-desfeito{stroke-dasharray:none;stroke-opacity:.7}"
    ".s-fluxo{stroke:var(--s-az);stroke-width:10}"
    ".s-fluxo-corte{stroke-linecap:butt}"
    ".s-fluxo-oco{stroke:var(--s-az);stroke-width:1.1;stroke-dasharray:3 3}"
    ".s-vetor{stroke:var(--s-t);stroke-width:1.2}"
    ".solidos .s-origem{fill:var(--s-t);stroke:none}"
    ".s-ponte{stroke:var(--s-az);stroke-width:1.6;stroke-dasharray:5 5}"
    ".solidos .s-chegada{stroke:var(--s-az);stroke-width:1.6}"
    ".s-formacao{stroke:var(--s-t2);stroke-width:1.1;stroke-dasharray:2 4}"
    ".s-divisa{stroke:var(--s-t2);stroke-width:1;stroke-opacity:.5}"
    ".s-fio{stroke:var(--s-t2);stroke-width:1}"
    ".solidos .s-etiqueta{fill:var(--s-p);stroke:var(--s-t);stroke-width:1.1}"
    ".s-rotulo,.s-etq{fill:var(--s-t2);font:14px/1 system-ui,sans-serif;stroke:none}"
    ".s-etq{font-size:12px;fill:var(--s-t)}"
)


# ---------------------------------------------------------------- plano

def carregar():
    pecas, atual, campo = {}, None, None
    if not PLANO.exists():
        return pecas
    for linha in PLANO.read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            atual = pecas.setdefault(linha[3:].strip(), {"desenho": []})
            campo = None
            continue
        if linha.startswith("### ") and atual is not None:
            campo = linha[4:].strip()
            continue
        if atual is None or not campo or not linha.strip():
            continue
        if campo == "desenho":
            if linha.startswith("- "):
                atual["desenho"].append(linha[2:].strip())
        else:
            atual[campo] = (atual.get(campo, "") + " " + linha.strip()).strip()
    return pecas


PECAS = carregar()


def svg(ident):
    return Peca(ident, dict(PECAS[ident], desenho=list(PECAS[ident]["desenho"]))).svg()


PRANCHA = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Linguagem geométrica da propriedade intelectual, prancha de conferência</title>
<style>
body{{margin:0;font:16px/1.5 system-ui,sans-serif;background:#ece7de;color:#211c17}}
header{{padding:1.5rem 2rem 0}} h1{{font-size:1.3rem;margin:0}} header p{{margin:.3rem 0 0;color:#615953;max-width:60rem}}
.peca{{display:grid;grid-template-columns:1fr 1fr;gap:1rem;padding:1.25rem 2rem;border-bottom:1px solid #d8d0c3}}
.peca h2{{grid-column:1/-1;margin:0;font-size:1rem}} .peca h2 code{{font-weight:400;color:#615953}}
.peca .lugar{{grid-column:1/-1;margin:-.6rem 0 0;font-size:.85rem;color:#615953}}
.tema{{padding:1.25rem;border-radius:6px;display:flex;align-items:center;justify-content:center;min-height:220px}}
.claro{{--papel:#faf6ef;--tinta:#211c17;--tinta-2:#615953;--sol-azul:#002fa7;background:#faf6ef}}
.escuro{{--papel:#17130f;--tinta:#ebe7e1;--tinta-2:#a9a49c;--sol-azul:#497ef7;background:#17130f}}
.tema svg{{max-width:100%;height:auto}}
.alt{{grid-column:1/-1;margin:0;font-size:.85rem;color:#615953}}
@media(max-width:800px){{.peca{{grid-template-columns:1fr}}}}
</style></head><body>
<header><h1>Linguagem geométrica da propriedade intelectual</h1>
<p>Prancha de conferência das peças em SVG de estrutura/ilustracoes-pi.md, geradas por ferramentas/solidos.py em {data}. Cada peça aparece no tema claro e no escuro, com o mesmo desenho. Rascunho, nada disto está no site.</p></header>
{pecas}
</body></html>"""


def prancha(ids):
    blocos = []
    for i in ids:
        p = PECAS[i]
        s = svg(i)
        blocos.append(f'<section class="peca"><h2>{escape(p.get("titulo", i))} <code>{i}</code></h2>'
                      f'<p class="lugar">{escape(p.get("lugar", ""))}</p>'
                      f'<div class="tema claro">{s}</div><div class="tema escuro">{s}</div>'
                      f'<p class="alt">Texto alternativo. {escape(p.get("alt", ""))}</p></section>')
    from datetime import date
    return PRANCHA.format(data=date.today().strftime("%d/%m/%Y"), pecas="".join(blocos))


if __name__ == "__main__":
    ids = sys.argv[1:] or list(PECAS)
    SAIDA.mkdir(parents=True, exist_ok=True)
    for i in ids:
        (SAIDA / f"{i}.svg").write_text(svg(i), encoding="utf-8")
    (SAIDA / "prancha.html").write_text(prancha(ids), encoding="utf-8")
    print(f"{len(ids)} peças em {SAIDA.relative_to(RAIZ)}")
