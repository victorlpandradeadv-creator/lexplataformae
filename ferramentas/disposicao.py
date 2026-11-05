"""A disposição da página. Monta, a partir do corpo pronto, o título em toda a largura, a coluna de texto e a coluna lateral.

A coluna lateral só traz o que a página já tem. O índice sai dos títulos da própria página e a lista ao lado sai das páginas
irmãs. Nenhuma frase nasce aqui, e os dois links respeitam o modo em que o título aparece. Revisão de disposição de 05/11/2026.
"""
import html
import re
import unicodedata
from html.parser import HTMLParser

VAZIOS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
# As classes que dizem em que modo a peça aparece. O índice repete a mesma classe, para não apontar para o que está oculto.
CLASSES_DE_MODO = {"interno", "arq", "ciencia", "em-modo", "modo-0", "modo-1", "modo-2"}
# O que fica de fora do índice. Saídas e navegação já são links, as fichas se repetem item a item e os campos de um direito
# são perguntas internas do cartão, que o título do cartão já representa.
FORA_DO_INDICE = {"saidas", "no-percurso", "outros-problemas", "fichas", "direito-partes", "operar", "expansao", "nos-percursos"}
LIMITE_INDICE = 30
# Página cuja lista ocupa a largura toda, por isso não tem coluna lateral.
SEM_LATERAL = {"percurso-indice", "problemas-pagina", "pagina-404"}


class No:
    __slots__ = ("tag", "classes", "attrs", "ini", "fim_abre", "fecha", "fim", "pai", "filhos")

    def __init__(self, tag, attrs, ini, fim_abre, pai):
        self.tag, self.attrs, self.ini, self.fim_abre, self.pai = tag, attrs, ini, fim_abre, pai
        self.classes = set((attrs.get("class") or "").split())
        self.fecha = self.fim = fim_abre
        self.filhos = []

    def linhagem(self):
        no = self
        while no is not None:
            yield no
            no = no.pai


class Arvore(HTMLParser):
    """Lê o corpo guardando a posição de cada marca, para que a página possa ser cortada sem refazer o texto."""

    def __init__(self, texto):
        super().__init__(convert_charrefs=False)
        self.texto = texto
        self.inicios = [0]
        for m in re.finditer("\n", texto):
            self.inicios.append(m.end())
        self.raiz = No("#", {}, 0, 0, None)
        self.pilha = [self.raiz]
        self.todos = []
        self.feed(texto)
        self.close()
        for no in reversed(self.pilha[1:]):
            no.fecha = no.fim = len(texto)

    def _pos(self):
        linha, coluna = self.getpos()
        return self.inicios[linha - 1] + coluna

    def handle_starttag(self, tag, attrs):
        ini = self._pos()
        no = No(tag, dict(attrs), ini, ini + len(self.get_starttag_text()), self.pilha[-1])
        self.pilha[-1].filhos.append(no)
        self.todos.append(no)
        if tag not in VAZIOS:
            self.pilha.append(no)

    def handle_startendtag(self, tag, attrs):
        ini = self._pos()
        no = No(tag, dict(attrs), ini, ini + len(self.get_starttag_text()), self.pilha[-1])
        self.pilha[-1].filhos.append(no)
        self.todos.append(no)

    def handle_endtag(self, tag):
        if not any(n.tag == tag for n in self.pilha[1:]):
            return
        pos = self._pos()
        fim = self.texto.index(">", pos) + 1
        while self.pilha[-1].tag != tag:
            aberto = self.pilha.pop()
            aberto.fecha = aberto.fim = pos
        no = self.pilha.pop()
        no.fecha, no.fim = pos, fim


class _Rotulo(HTMLParser):
    """Tira do título o que não cabe num link, como outro link, a página e a chamada de nota. Guarda só a marca de modo."""
    PULAR = {"pg", "pg-marca", "nota-ref", "so-leitor", "chip-area", "vezes", "area-rotulo", "rotulo-ext"}

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.saida, self.plano, self.pular, self.pilha = [], [], 0, []

    def handle_starttag(self, tag, attrs):
        if tag in VAZIOS:
            return
        classes = set((dict(attrs).get("class") or "").split())
        de_modo = classes & CLASSES_DE_MODO
        if self.pular or classes & self.PULAR or tag == "sup":
            self.pular += 1
            self.pilha.append("pular")
        elif de_modo:
            self.saida.append(f'<span class="{" ".join(sorted(de_modo))}">')
            self.pilha.append("span")
        else:
            self.pilha.append("")

    def handle_endtag(self, tag):
        if tag in VAZIOS or not self.pilha:
            return
        topo = self.pilha.pop()
        if topo == "pular":
            self.pular -= 1
        elif topo == "span":
            self.saida.append("</span>")

    def handle_data(self, data):
        if not self.pular:
            self.saida.append(data)
            self.plano.append(data)

    def handle_entityref(self, name):
        self.handle_data(f"&{name};")

    def handle_charref(self, name):
        self.handle_data(f"&#{name};")


def rotulo_de(trecho):
    p = _Rotulo()
    p.feed(trecho)
    p.close()
    return "".join(p.saida).strip(), html.unescape("".join(p.plano)).strip()


def _slug(texto):
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:48].rstrip("-") or "secao"


def _modos(classes):
    """Em quais modos a peça com estas classes aparece."""
    modos = {0, 1, 2}
    if "interno" in classes:
        modos &= {1, 2}
    if classes & {"arq", "ciencia"}:
        modos &= {2}
    if "em-modo" in classes:
        modos &= {n for n in (0, 1, 2) if f"modo-{n}" in classes}
    return modos


def _candidato(no):
    if no.tag in ("h2", "h3"):
        return True
    return no.tag == "p" and "rotulo-ext" in no.classes


def ancorar_titulos(corpo):
    """Dá endereço aos títulos da página e devolve o índice. Roda antes dos balões, para o índice ficar só com o texto do título."""
    arvore = Arvore(corpo)
    artigo = next((n for n in arvore.todos if n.tag == "article" and "folha" in n.classes), None)
    if artigo is None or SEM_LATERAL & artigo.classes:
        return corpo, []
    usados = {n.attrs["id"] for n in arvore.todos if n.attrs.get("id")}
    itens, insercoes = [], []
    for no in arvore.todos:
        if not _candidato(no) or "so-leitor" in no.classes or "h1" == no.tag:
            continue
        linha = list(no.linhagem())
        if artigo not in linha:
            continue
        # O nome dentro de um cartão de direito é o único título que conta dentro dele.
        if any(n.classes & FORA_DO_INDICE or n.tag in ("nav", "aside", "details") for n in linha[1:] + [no]):
            continue
        marcado, plano = rotulo_de(corpo[no.fim_abre:no.fecha])
        if not plano:
            continue
        classes = set()
        for n in linha:
            classes |= n.classes & CLASSES_DE_MODO
        ident = no.attrs.get("id")
        if not ident:
            base = _slug(plano)
            ident, k = base, 2
            while ident in usados:
                ident, k = f"{base}-{k}", k + 1
            usados.add(ident)
            insercoes.append((no.fim_abre - 1 - (1 if corpo[no.fim_abre - 2] == "/" else 0), f' id="{ident}"'))
        nivel = 2 if (no.tag == "h3" or any("direito" in n.classes for n in linha)) else 1
        itens.append({"id": ident, "rotulo": marcado, "nivel": nivel, "classes": classes, "modos": _modos(classes)})
    for pos, texto in sorted(insercoes, reverse=True):
        corpo = corpo[:pos] + texto + corpo[pos:]
    if len(itens) > LIMITE_INDICE and sum(1 for i in itens if i["nivel"] == 1) >= 2:
        itens = [i for i in itens if i["nivel"] == 1]
    return corpo, itens


def _indice_html(itens):
    """O índice da página. Em cada modo só aparece se tiver ao menos dois títulos à vista."""
    if not itens:
        return "", set()
    sem_indice = {n for n in (0, 1, 2) if sum(1 for i in itens if n in i["modos"]) < 2}
    if len(sem_indice) == 3:
        return "", sem_indice
    linhas = []
    for i in itens:
        classes = " ".join(sorted(i["classes"] | {f'nivel-indice-{i["nivel"]}'}))
        linhas.append(f'<li class="{classes}"><a href="#{i["id"]}">{i["rotulo"]}</a></li>')
    esconde = "".join(f" esconde-{n}" for n in sorted(sem_indice))
    return (f'<nav class="lateral-bloco lateral-indice{esconde}" aria-label="Nesta página"><p class="lateral-titulo">Nesta página</p>'
            f'<ol>{"".join(linhas)}</ol></nav>'), sem_indice


def _irmas_html(irmas):
    if not irmas or not irmas[1]:
        return ""
    titulo, itens = irmas
    linhas = "".join(f'<li><a href="{href}"{" aria-current=\"page\"" if atual else ""}>{rotulo}</a></li>' for rotulo, href, atual in itens)
    curta = " lateral-curta" if len(itens) <= 12 else ""
    return (f'<nav class="lateral-bloco lateral-irmas{curta}" aria-label="{html.escape(titulo, quote=True)}"><p class="lateral-titulo">{html.escape(titulo)}</p>'
            f'<ol>{linhas}</ol></nav>')


def _frases(plano):
    return [f for f in re.split(r"(?<=[.!?])(?<!\s[A-Z]\.)\s+(?=[A-ZÀ-Ú])", plano) if f]


def _classe_titulo(corpo, h1):
    """O corpo do título segue o tamanho dele. Título de duas frases quebra entre elas, como o da página inicial."""
    _, plano = rotulo_de(re.sub(r'<span class="em-modo modo-1">.*?</span>(</span>)?', "", corpo[h1.fim_abre:h1.fecha], flags=re.S))
    frases = _frases(plano)
    if len(frases) > 1:
        maior = max(len(f) for f in frases)
        return " titulo-muito-longo" if maior > 50 else " titulo-longo" if maior > 42 else ""
    n = len(plano)
    return " titulo-muito-longo" if n > 110 else " titulo-longo" if n > 58 else ""


def _titulo_por_frases(interno):
    """Só mexe em título de texto puro. A quebra é visual, e o texto copiado continua igual."""
    if "<" in interno:
        return interno
    frases = _frases(interno)
    if len(frases) < 2:
        return interno
    return " ".join(f'<span class="titulo-frase">{f}</span>' for f in frases)


def montar(corpo, itens, irmas=None):
    """Corta o artigo em título, coluna de texto e coluna lateral. A abertura da página desce para a coluna de texto."""
    arvore = Arvore(corpo)
    artigo = next((n for n in arvore.todos if n.tag == "article" and "folha" in n.classes), None)
    if artigo is None or SEM_LATERAL & artigo.classes:
        return corpo
    # O título que vale é o primeiro filho do artigo com um h1 dentro, seja ele o próprio cabeçalho ou uma peça da página.
    filhos = artigo.filhos
    k = None
    for i, filho in enumerate(filhos):
        if filho.tag == "h1" or any(n.tag == "h1" and filho in n.linhagem() for n in arvore.todos):
            k = i
            break
    if k is None:
        k = -1
    indice, sem_indice = _indice_html(itens)
    irmas_html = _irmas_html(irmas)
    vazia = sem_indice if not irmas_html else set()
    if not itens and not irmas_html:
        vazia = {0, 1, 2}
    classes_vazia = "".join(f" sem-lateral-{n}" for n in sorted(vazia))
    lateral = (f'<aside class="lateral" data-arq="coluna lateral · índice e páginas irmãs"><div class="lateral-fixa">{indice}{irmas_html}</div></aside>'
               if (indice or irmas_html) else "")
    ini_corpo = filhos[k].fim if k >= 0 else artigo.fim_abre
    cabeca = corpo[artigo.fim_abre:ini_corpo]
    resto = corpo[ini_corpo:artigo.fecha]
    classe_titulo = ""
    if k >= 0:
        filho = filhos[k]
        h1 = filho if filho.tag == "h1" else next(n for n in arvore.todos if n.tag == "h1" and filho in n.linhagem())
        classe_titulo = _classe_titulo(corpo, h1)
        # O que vem depois do h1 no cabeçalho, como a abertura e os links, desce para a coluna de texto, ao lado da lateral.
        if filho.tag == "header" and h1.pai is filho and corpo[h1.fim:filho.fecha].strip():
            cabeca = corpo[artigo.fim_abre:h1.fim] + "</header>"
            classes_header = filho.attrs.get("class", "")
            resto = f'<div class="{classes_header} folha-abertura">{corpo[h1.fim:filho.fecha]}</div>' + resto
        cabeca = cabeca.replace(corpo[h1.ini:h1.fim], corpo[h1.ini:h1.fim_abre] + _titulo_por_frases(corpo[h1.fim_abre:h1.fecha]) + "</h1>", 1)
    abre = corpo[artigo.ini:artigo.fim_abre]
    if classe_titulo:
        abre = abre.replace('class="folha', f'class="folha{classe_titulo}', 1)
    grade = (f'<div class="folha-corpo{classes_vazia}{"" if lateral else " sem-lateral"}"><div class="folha-texto">{resto}</div>{lateral}</div>')
    return corpo[:artigo.ini] + abre + cabeca + grade + corpo[artigo.fecha:]
