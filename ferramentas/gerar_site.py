"""Gera o site publicável em docs/, servido pelo GitHub Pages.

Uso
    python3 ferramentas/gerar_dados.py   # primeiro, para atualizar dados/atlas.json
    python3 ferramentas/gerar_site.py

Todo o conteúdo vem de dados/atlas.json, que vem das fichas conferidas.
Cada página sai com o texto completo no HTML, legível sem JavaScript, para
pessoas, buscadores e robôs de IA. O script só acrescenta interação.
"""
import html
import json
import re
import shutil
import unicodedata
from pathlib import Path

import disposicao

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "docs"
BASE = "https://lexplataformae.com.br"
REPO = "https://github.com/victorlpandradeadv-creator/lexplataformae"
VERSAO = "0.12"
# Histórico público das versões, pela lição do Code v2 de Lessig, por ordem do autor de 10/11/2026. A página versoes/ só existe na Ciência.
VERSOES = [
    ("0.3", "26/10/2026", "Primeira versão publicada, em construção, com o texto integral dividido em seções citáveis e uma página por conceito."),
    ("0.4", "27/10/2026", "Entram as situações do quadro de enquadramento e as famílias de plataforma."),
    ("0.5", "27/10/2026", "O site passa a se ler em três camadas, e o nome do autor fica por último."),
    ("0.6", "27/10/2026", "Entram o caminho da skin e a chave de leitura em três degraus."),
    ("0.7", "27/10/2026", "Entram a paleta, a chave Modo com Informação, Doutrina e Ciência, o menu por modo e o bloco do texto integral."),
    ("0.8", "03/11/2026", "Os capítulos 5 e 6 chegam completos à Informação e à Doutrina, com as páginas por problema e a auditoria de design."),
    ("0.9", "05/11/2026", "Revisão da disposição das páginas e da voz do site."),
    ("0.10", "09/11/2026", "Adequação das camadas, com a Doutrina em quinze capítulos, os 24 problemas da Informação e a página Como reclamar."),
    ("0.11", "10/11/2026", "Menu unificado, capa narrativa, identidade editorial, o Caminho, a citação sugerida em cada página e este histórico de versões."),
    ("0.12", "10/11/2026", "Entra a versão inglesa do site inteiro, com o texto integral da tese em tradução por máquina e os trechos literais com o original à mão."),
]
DATA_VERSAO = VERSOES[-1][1]
PDF_NOME = "andrade-2026-tese-oic-lex-plataformae.pdf"

# Marca de versão do estilo e do script, para que o navegador do leitor busque a versão nova logo depois de cada publicação.
import hashlib as _hashlib
VERSAO_ASSETS = _hashlib.sha1(b"".join((RAIZ / f).read_bytes() for f in (
    "site/extra.css", "site/cores.css", "site/atlas.js", "prototipo/modelo.html") if (RAIZ / f).exists())).hexdigest()[:10]

D = json.loads((RAIZ / "dados" / "atlas.json").read_text(encoding="utf-8"))
_corpus = RAIZ / "dados" / "corpus.json"
C = json.loads(_corpus.read_text(encoding="utf-8")) if _corpus.exists() else {"secoes": []}
SECOES = C["secoes"]
# Erros de digitação do texto da tese, achados na revisão do inglês e corrigidos por ordem do autor de 10/11/2026.
# A correção aparece marcada, com o que a tese registra no title, e o PDF continua sendo a fonte.
DATA_CORRECOES_TEXTO = "10/11/2026"
CORRECOES_TEXTO = [
    ("compreender experiências interativas estruturadas por controle técnico. Em A autora", "Em A autora", "A autora"),
    ("mecanismos tão automatizados quanto de recomposição", "mecanismos tão automatizados quanto de recomposição", "mecanismos de recomposição tão automatizados quanto a alteração"),
    ("Wada (20216)", "20216", "2016"),
    ("Filomeno tratar a vulnerabilidade", "Filomeno tratar", "Filomeno trata"),
    ("não configura ornamento se aproxima", "não configura ornamento se aproxima", "não configura ornamento e se aproxima"),
    ("Cédric Duran em", "Cédric Duran em", "Cédric Durand em"),
]


def _corrige(v):
    if isinstance(v, str):
        for ctx, errado, certo in CORRECOES_TEXTO:
            if ctx in v:
                marca = (f'<ins class="correcao" title="Correção posterior de {DATA_CORRECOES_TEXTO}. '
                         f'A tese registra: {errado}">{certo}</ins>').replace(": ", " ")
                v = v.replace(ctx, ctx.replace(errado, marca, 1))
        return v
    if isinstance(v, list):
        return [_corrige(x) for x in v]
    if isinstance(v, dict):
        return {k: _corrige(x) for k, x in v.items()}
    return v


SECOES = _corrige(SECOES)
POR_NUMERO = {s["n"]: s for s in SECOES if s["n"]}
POR_SLUG = {s["slug"]: s for s in SECOES}
PAG2SLUG = {}
for _s in SECOES:
    for _p in _s.get("paginas", []):
        PAG2SLUG.setdefault(_p, _s["slug"])
POR_ID = {c["id"]: c for c in D["conceitos"]}
EIXO = next(c for c in D["conceitos"] if c.get("eixo"))

# Os títulos de capítulo vêm do PDF em caixa alta, que é a convenção de impressão da tese. Na tela, a caixa alta grita no meio
# da trilha, dos links e da prosa, e o site mostra o mesmo título em caixa normal. Revisão de rótulos de 05/11/2026.
CAIXA_NORMAL = {
    "INTRODUÇÃO": "Introdução",
    "DO DESENHO METODOLÓGICO E DO PROTOCOLO DE OBSERVAÇÃO": "Do desenho metodológico e do protocolo de observação",
    "TECNOLOGIA, PLATAFORMAS E A ORDEM ECONÔMICA TECNO-MIDIÁTICA DO CONSUMO DIGITAL": "Tecnologia, plataformas e a ordem econômica tecno-midiática do consumo digital",
    "SEMIÓTICA E GOVERNANÇA DE FRUIÇÃO NO CONSUMO IMATERIAL CONTÍNUO": "Semiótica e governança de fruição no consumo imaterial contínuo",
    "DO REGIME JURÍDICO DO OBJETO IMATERIAL DE CONSUMO (OIC) SOB A LEX PLATAFORMAE": "Do regime jurídico do Objeto Imaterial de Consumo (OIC) sob a Lex Plataformae",
    "DA TUTELA DA VULNERABILIDADE SEMIÓTICA DO CONSUMIDOR À LUZ DA ORDEM CONSTITUCIONAL E ECONÔMICA DO BRASIL":
        "Da tutela da vulnerabilidade semiótica do consumidor à luz da ordem constitucional e econômica do Brasil",
    "DA TIPOLOGIA DOS MODELOS DE INCIDÊNCIA DO OBJETO IMATERIAL DE CONSUMO EM DIFERENTES CATEGORIAS FUNCIONAIS DE PLATAFORMA":
        "Da tipologia dos modelos de incidência do Objeto Imaterial de Consumo em diferentes categorias funcionais de plataforma",
    "CONCLUSÃO": "Conclusão",
    "REFERÊNCIAS": "Referências",
}
for _s in SECOES:
    if _s["titulo"] in CAIXA_NORMAL:
        _s["titulo"] = CAIXA_NORMAL[_s["titulo"]]
        _s["titulo_html"] = html.escape(f'{_s["n"]} {_s["titulo"]}'.strip())

TITULO_TESE = ("Do regime jurídico do Objeto Imaterial de Consumo (OIC) sob a Lex Plataformae: "
               "a tutela da vulnerabilidade semiótica do consumidor à luz da ordem constitucional e econômica do Brasil")


def esc(t):
    return html.escape(str(t), quote=True)


def _plano(h):
    h = re.sub(r'<sup class="nota-ref">.*?</sup>', "", h)
    h = re.sub(r'<span class="pg-marca"[^>]*>.*?</span>', " ", h)
    t = html.unescape(re.sub(r"<[^>]+>", "", h)).replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", t)


TEXTO_SECAO = {s["slug"]: _plano(" ".join(b["html"] for b in s["blocos"])) for s in SECOES}
NOTAS_SECAO = {s["slug"]: [(n["n"], n["pagina"], _plano(n["html"])) for n in s["notas"]] for s in SECOES}
SECOES_DA_PAGINA = {}
for _s in SECOES:
    for _p in _s.get("paginas", []):
        SECOES_DA_PAGINA.setdefault(_p, []).append(_s["slug"])


def destino_pagina(ref, prefixo, texto=None):
    """Endereço do trecho da tese a que a referência aponta.

    Quando a referência acompanha uma citação, procura a seção que contém o
    trecho, porque uma mesma página pode abrigar o fim de uma seção e o
    começo de outra.
    """
    if ref == "Resumo":
        return f"{prefixo}tese/#resumo"
    m = re.match(r"p\. (\d+)", ref)
    if not m or int(m.group(1)) not in PAG2SLUG:
        return None
    n = int(m.group(1))
    slug = PAG2SLUG[n]
    if texto:
        pedaco = re.sub(r"\s+", " ", max(texto.split("[...]"), key=len).strip(" .,").replace("“", '"').replace("”", '"'))[:60]
        for candidato in SECOES_DA_PAGINA.get(n, []):
            if pedaco and pedaco in TEXTO_SECAO[candidato]:
                return f"{prefixo}tese/{candidato}/#p{n}"
        # O trecho pode estar numa nota de rodapé da página.
        for slug_nota, notas in NOTAS_SECAO.items():
            for num, pagina_nota, texto_nota in notas:
                if pagina_nota == n and pedaco and pedaco in texto_nota:
                    return f"{prefixo}tese/{slug_nota}/#n{num}"
    return f"{prefixo}tese/{slug}/#p{n}"


def pg(ref, prefixo=None, texto=None):
    alvo = destino_pagina(ref, prefixo, texto) if prefixo is not None else None
    if alvo:
        return f'<a class="pg" href="{alvo}" data-arq="âncora · leva ao trecho exato da tese">{esc(ref)}</a>'
    return f'<span class="pg" data-arq="âncora · página da tese">{esc(ref)}</span>'


def com_ancoras(texto, prefixo=None):
    # O espaço antes da referência vai junto com ela, para que nada sobre antes do ponto quando a página fica oculta.
    return re.sub(r"\s*\((p\. [\d\-]+|Resumo)\)", lambda m: pg(m.group(1), prefixo), esc(texto))


def secao_de_lugar(lugar):
    """Encontra a seção da tese citada num item de 'Onde vive'."""
    m = re.match(r"(\d+(?:\.\d+)*)", lugar)
    if m and m.group(1) in POR_NUMERO:
        return POR_NUMERO[m.group(1)]
    if lugar.startswith("Introdução"):
        return POR_NUMERO.get("1")
    if lugar.startswith("Conclusão"):
        return POR_NUMERO.get("8")
    return None


def campo(c, rotulo):
    return next((f for f in c["campos"] if f["rotulo"] == rotulo), None)


def primeira_frase(texto):
    m = re.match(r"^(.*?[^p]\.)(?:\s|$)", texto or "")
    return m.group(1) if m else (texto or "")


def em_ordem(lista):
    return sorted(lista, key=lambda c: c["nome"].casefold())


def canonica(c):
    f = campo(c, "Definição canônica proposta")
    return f["citacoes"][0] if f and f["citacoes"] else None


def resumo(texto, limite=158):
    texto = re.sub(r"\s+", " ", texto).strip()
    if len(texto) <= limite:
        return texto
    corte = texto[:limite].rsplit(" ", 1)[0].rstrip(",;:")
    return corte + "…"


# Nome em português dos conceitos, para as telas Informação e Doutrina. A tese usa o nome em latim, que segue em Ciência
# e no nome do site. Decisão do autor de 27/10/2026, acréscimo posterior à tese.
NOME_COMUM = {"lex-plataformae": "lei da plataforma"}
DATA_NOME_COMUM = "27/10/2026"


def nome_comum(c, maiuscula=True):
    comum = NOME_COMUM.get(c["id"])
    if not comum:
        return c["nome"]
    return comum[0].upper() + comum[1:] if maiuscula else comum


def nome_html(c, maiuscula=True):
    """O nome do conceito como o leitor vê em cada modo. Só muda onde há nome em português."""
    if c["id"] not in NOME_COMUM:
        return esc(c["nome"])
    return (f'<span class="em-modo modo-0 modo-1">{esc(nome_comum(c, maiuscula))}</span>'
            f'<span class="em-modo modo-2">{esc(c["nome"])}</span>')


CAMPOS_SO_CIENCIA = {"Situação", "Lastro na tese"}  # inteiros na Ciência, com as citações
# O rótulo de cada campo da ficha como o técnico lê. Na Ciência fica o nome de trabalho, que diz como o site escolheu o trecho.
ROTULO_FICHA = {"Definição canônica proposta": "Definição", "Formulações concorrentes": "Outras formulações",
                "Formulação para o nível introdutório": "Em uma frase", "Formulação curta": "Em uma frase"}
PADRAO_META = re.compile(r"\btese\b|\b\d+\.\d+(?:\.\d+)*\b|decisão do autor", re.I)


def nome_titulo(c):
    """O nome para o título da aba e para os buscadores."""
    return f'{nome_comum(c)} ({c["nome"]})' if c["id"] in NOME_COMUM else c["nome"]


def url_conceito(cid):
    return f"{BASE}/conceitos/{cid}/"


def conceitos_do_atlas():
    return [c for c in D["conceitos"] if c["tipo"] == "conceito"]


LEGENDA = {
    "mista": ("Cada peça da página diz o que é e de onde vem, quando o mouse passa sobre ela, no toque ou no foco do teclado. "
              "As caixas com números de página levam ao trecho exato do texto integral."),
    "interna": "Cada peça da página diz o que é e de onde vem, quando o mouse passa sobre ela, no toque ou no foco do teclado.",
}

# A chave se chama Modo e tem três posições, com os nomes indicados pelo autor em 27/10/2026.
# Informação fala com o leigo que consome e quer saber seus direitos. Doutrina fala com o técnico que vai advogar.
# Ciência fala com o expert que quer testar a teoria e saber de onde saiu cada coisa, e só ela mostra a estrutura inteira.
DEGRAUS = ("Informação", "Doutrina", "Ciência")
# O nível mínimo de cada tipo de página. Escolher um modo abaixo dele leva à página de superfície indicada.
NIVEL_MINIMO = {"mista": 0, "externa": 0, "interna": 1, "ciencia": 2}


def chave_mestra(nivel):
    radios = "".join(
        f'<input type="radio" name="nivel" id="nivel-{i}" value="{i}"{" checked" if i == nivel else ""}>'
        f'<label for="nivel-{i}">{nome}</label>'
        for i, nome in enumerate(DEGRAUS))
    return (f'<div class="chave-mestra" role="radiogroup" aria-labelledby="chave-nome">'
            f'<span class="chave-nome" id="chave-nome">Modo</span><span class="degraus">{radios}</span></div>')


# O menu de cada modo. Rascunho de 27/10/2026, a pedido do autor, que critica depois.
# Cada item tem o endereço e os modos em que aparece. Em Ciência os itens dos outros modos aparecem numa segunda linha.
MENU = [
    ("Problemas", "problemas/", (0, 1)),
    ("Direitos", "direitos/", (0,)), ("Direitos", "roteiro/", (1,)),
    ("Caminho", "caminho/", (0,)), ("Caminho", "doutrina/", (1,)),
    ("Vocabulário", "conceitos/", (0, 1)), ("Plataformas", "plataformas/", (0, 1)), ("Legislação", "legislacao/", (1,)),
    ("Método", "metodo/", (2,)), ("Fundamentos", "fundamentos/", (2,)), ("Dogmática", "dogmatica/", (2,)),
    ("Objeto e instrumentos", "objeto-e-instrumentos/", (2,)), ("Autores", "autores/", (2,)), ("Referências", "referencias/", (2,)),
]
# Menu unificado, decisão do autor de 10/11/2026. Os mesmos nomes na Informação e na Doutrina, e o modo escolhe a profundidade.
MENU_SEGUNDA = [("Problemas", "problemas/"), ("Direitos", "roteiro/"), ("Caminho", "doutrina/"), ("Vocabulário", "conceitos/"),
                ("Plataformas", "plataformas/"), ("Legislação", "legislacao/")]


def menu_html(prefixo, atual=""):
    def existe(caminho):
        return caminho.startswith("#") or caminho in PAGINAS_PRONTAS
    def corrente(caminho):
        if atual == caminho:
            return ' aria-current="page"'
        return ' aria-current="location"' if atual.startswith(caminho) else ''
    itens = "".join(f'<li class="em-modo {" ".join(f"modo-{m}" for m in modos)}"><a href="{prefixo}{caminho}"{corrente(caminho)}>{esc(rotulo)}</a></li>'
                    for rotulo, caminho, modos in MENU if existe(caminho))
    segunda = "".join(f'<li><a href="{prefixo}{caminho}"{corrente(caminho)}>{esc(rotulo)}</a></li>' for rotulo, caminho in MENU_SEGUNDA if existe(caminho))
    return (f'<nav class="menu-modo" aria-label="Seções"><ul>{itens}</ul>'
            f'<ul class="em-modo modo-2 menu-segunda" aria-label="Os outros modos">{segunda}</ul></nav>')


# Páginas que o gerador escreve. O menu só mostra endereço que existe.
PAGINAS_PRONTAS = {"caminho/", "direitos/", "plataformas/", "roteiro/", "roteiro/diretrizes/", "metodo/", "fundamentos/", "dogmatica/", "legislacao/",
                   "autores/", "referencias/", "objeto-e-instrumentos/", "problemas/", "como-reclamar/", "doutrina/", "conceitos/"}


_BQ = re.compile(r'<blockquote class="citacao(?: nao-e)?"><p>(.*?)(?=<a class="pg"|<span class="pg"|</p>)', re.S)


def _chave_bq(t):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", t))).strip().lower()


def sem_citacao_repetida(corpo):
    """A mesma citação não aparece duas vezes na mesma tela. Na Doutrina, a repetida fica só na Ciência.

    Numa página de conceito, a ficha guarda o texto literal, e o trecho que se repete debaixo de um bloco simples sai da Doutrina.
    Nas demais páginas, a segunda ocorrência sai da Doutrina. Em Ciência tudo aparece, para o rastreio de cada bloco.
    """
    corte = corpo.find('<div class="interno arquitetura"')
    depois = {_chave_bq(m.group(1)) for m in _BQ.finditer(corpo, corte)} if corte >= 0 else set()
    vistos = set()
    # O texto literal corrido da tela, para que o fragmento que ele já traz por inteiro não apareça duas vezes.
    corrido = _chave_bq(" ".join(re.findall(r'<div class="texto">(.*?)</div>', corpo, re.S)))
    corrido = re.sub(r"[“”]", '"', corrido)

    def no_corrido(chave):
        partes = [x.strip(" .,") for x in re.sub(r"[“”]", '"', chave).split("[...]")]
        maior = max(partes, key=len)
        return len(maior) > 40 and maior in corrido

    def troca(m):
        chave = _chave_bq(m.group(1))
        na_ficha = corte >= 0 and m.start() < corte and any(chave in d for d in depois)
        # A citação que já apareceu inteira dentro de outra maior, na mesma tela, também conta como repetida.
        contida = len(chave) > 40 and any(chave in v for v in vistos if len(v) > len(chave))
        repetida = na_ficha or chave in vistos or contida or no_corrido(chave)
        if not na_ficha:
            vistos.add(chave)
        if not repetida or len(chave) <= 40:
            return m.group(0)
        return re.sub(r'<blockquote class="(citacao(?: nao-e)?)">', r'<blockquote class="\1 ciencia">', m.group(0), count=1)
    return _BQ.sub(troca, corpo)


# Rótulos de dado que se repetem item a item numa lista. O primeiro fica à vista e funciona como cabeçalho. Os demais ficam
# só para leitor de tela. Revisão de rótulos de 05/11/2026.
ROTULOS_DE_DADO = ("No site", "Cita", "Nos conceitos", "Nos parâmetros", "Bens protegidos", "Dispositivos", "Onde aparece no texto integral", "Conceitos que o trecho nomeia")


def rotulos_uma_vez(corpo):
    """Cada anúncio de voz e cada etiqueta da arquitetura aparece uma vez por página.

    De onde vem anuncia a primeira troca de voz da página, e a letra serifada com o filete carrega as seguintes. Quando a
    primeira expansão só aparece na Ciência, a primeira da Doutrina ganha o seu próprio rótulo. Em texto literal vale do mesmo
    jeito. Os rótulos repetidos não somem para o leitor de tela. Na Ciência, cada etiqueta igual aparece só na primeira peça,
    e as demais guardam o contorno tracejado.
    """
    oculto = 'class="rotulo-fonte so-leitor"'
    for rotulo in (ROTULO_FONTE, ROTULO_LITERAL):
        vistos = {"interno": False, "ciencia": False}
        pedacos = corpo.split(rotulo)
        saida = pedacos[0]
        for antes, depois in zip(pedacos[:-1], pedacos[1:]):
            abertura = re.findall(r'<(?:div|section|header|article)\b[^>]*class="([^"]*)"', saida[-600:])
            modo = "ciencia" if abertura and re.search(r"\bciencia\b|modo-2", abertura[-1]) else "interno"
            # A expansão cujos trechos todos ficaram só na Ciência some fora dela, e o rótulo dela não conta para a Doutrina.
            trecho = depois[:depois.find("</div>")] if "</div>" in depois else depois[:2000]
            classes = re.findall(r'<blockquote class="([^"]*)"', trecho)
            if classes and all(re.search(r"\bciencia\b", c) for c in classes):
                modo = "ciencia"
            if vistos["interno"] or (modo == "ciencia" and vistos["ciencia"]):
                saida += rotulo.replace('class="rotulo-fonte"', oculto)
            else:
                saida += rotulo
                vistos[modo] = True
            saida += depois
        corpo = saida
    for rotulo in ROTULOS_DE_DADO:
        marca = f'<span class="sobrelinha">{rotulo}</span>'
        primeiro = corpo.find(marca)
        if primeiro >= 0:
            corpo = corpo[:primeiro + len(marca)] + corpo[primeiro + len(marca):].replace(marca, f'<span class="sobrelinha so-leitor">{rotulo}</span>')
        marca_p = f'<p class="sobrelinha">{rotulo}</p>'
        primeiro = corpo.find(marca_p)
        if primeiro >= 0:
            corpo = corpo[:primeiro + len(marca_p)] + corpo[primeiro + len(marca_p):].replace(marca_p, f'<p class="sobrelinha so-leitor">{rotulo}</p>')
    vistas = set()

    def arq(m):
        valor = m.group(1)
        if valor.startswith("âncora") or valor not in vistas:
            vistas.add(valor)
            return m.group(0)
        return f'data-arq-mesmo="{valor}"'
    return re.sub(r'data-arq="([^"]*)"', arq, corpo)


def pagina(titulo, descricao, corpo, prefixo, caminho, jsonld=None, camada="interna", superficie=None, imagem=None, lei=True, irmas=None):
    """Monta a página.

    camada 'mista' abre em Informação e ganha conteúdo em Doutrina e estrutura em Ciência.
    camada 'interna' é página do técnico, que abre no mínimo em Doutrina. Escolher Informação leva à superfície.
    camada 'ciencia' é página do expert, que só existe em Ciência. Escolher outro modo leva à superfície.
    camada 'externa' não tem arquitetura própria a mostrar.
    """
    canonico = BASE + "/" + caminho
    descricao = resumo(descricao)
    # A coluna lateral sai dos títulos da própria página e das páginas irmãs. O índice nasce antes dos balões, com o texto limpo.
    corpo, indice = disposicao.ancorar_titulos(corpo)
    # Cada artigo citado com o nome da lei ganha o texto integral em rodapé. O texto integral da tese fica como está.
    # Cada citação de autor ou fonte da lista de referências vira balão. Vale também para o texto integral.
    corpo = sem_citacao_repetida(corpo)
    corpo = rotulos_uma_vez(corpo)
    corpo = com_autores(corpo, prefixo)
    if lei:
        PAGINA_ATUAL[0] = (caminho, titulo.split(" · ")[0].replace("Lex Plataformae", "Lei da plataforma"), camada)
        corpo = com_lei(corpo, prefixo)
        PAGINA_ATUAL[0] = None
    if 'id="leis-titulo"' in corpo:
        indice = indice + [{"id": "leis-titulo", "rotulo": "A lei citada nesta página", "nivel": 1, "classes": {"interno"}, "modos": {1, 2}}]
    corpo = disposicao.montar(corpo, indice, irmas)
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    minimo = NIVEL_MINIMO[camada]
    interna = minimo > 0
    inicio = prefixo or "./"
    sup = superficie if superficie is not None else inicio
    # Antes da primeira pintura, a página assume o modo que o leitor escolheu, nunca abaixo do mínimo da página.
    lembrar = ("<script>(function(){var n=0;try{n=parseInt(localStorage.getItem('lexp-nivel'),10)||0}catch(e){}"
               f"if(n<{minimo})n={minimo};if(n>2)n=2;var r=document.getElementById('nivel-'+n);if(r)r.checked=true;"
               "document.body.classList.toggle('aberto',n>0);document.body.classList.toggle('desnudo',n>1)})()</script>")
    legenda = LEGENDA["interna" if interna else "mista"]
    cartao = imagem if imagem and (RAIZ / "site" / "cartoes" / f"{imagem}.png").exists() else "inicio"
    # Na página do autor o percurso termina no LinkedIn, e a assinatura do rodapé não se repete.
    assinatura = "" if caminho == "autor/" else f'<p class="assinatura"><a href="{prefixo}autor/">Sobre o autor</a></p>'
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<script>try{{var t=localStorage.getItem('lexp-tema');if(t==='claro'||t==='escuro')document.documentElement.dataset.theme=t==='escuro'?'dark':'light'}}catch(e){{}}</script>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(descricao)}">
<meta name="author" content="Victor L. P. Andrade">
<link rel="canonical" href="{esc(canonico)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Lex Plataformae">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(descricao)}">
<meta property="og:url" content="{esc(canonico)}">
<meta property="og:locale" content="pt_BR">
<meta property="og:image" content="{BASE}/assets/cartoes/{cartao}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(titulo)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{prefixo}assets/estilo.css?v={VERSAO_ASSETS}">
<link rel="alternate" type="application/json" href="{prefixo}dados/atlas.json" title="Dados do Atlas">
{ld}
</head>
<body class="{'aberto' if interna else ''}{' desnudo' if minimo > 1 else ''}" data-camada="{camada}" data-minimo="{minimo}" data-superficie="{esc(sup)}">
<a class="pular-conteudo" href="#conteudo-principal">Ir para o conteúdo</a>
{chave_mestra(minimo)}
{lembrar}
<div class="moldura">
  <div class="faixa arq" data-arq="versão · o site cresce em público e cada mudança fica registrada">
    <span><a href="{prefixo}versoes/">Versão {VERSAO}</a> · em construção</span>
  </div>
  <header class="topo">
    <a class="topo-marca" href="{inicio}"><span class="topo-projeto">Projeto</span><span class="topo-nome">Lex Plataformae</span></a>
    {menu_html(prefixo, caminho)}
    <a class="integral ciencia" href="{prefixo}tese/">Texto integral</a>
    <button type="button" class="tema" aria-pressed="false" aria-label="Modo escuro" title="Modo escuro"><svg aria-hidden="true" viewBox="0 0 20 20" width="16" height="16"><circle cx="10" cy="10" r="7.5" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M10 2.5a7.5 7.5 0 0 1 0 15z" fill="currentColor"/></svg></button>
  </header>
  <div class="legenda-desnudo" role="note"><p>{esc(legenda)}</p><label for="arq-tudo"><input type="checkbox" id="arq-tudo"> Mostrar toda a arquitetura</label></div>
  <main id="conteudo-principal" tabindex="-1">
{corpo}
  </main>
  <footer class="rodape">
    <div class="ciencia rodape-citar" data-arq="como citar · referência pronta desta página na versão atual">
      <p class="rotulo-citar">Como citar esta página</p>
      <p class="referencia citar-pagina">ANDRADE, Victor L. P. {esc(titulo.split(" · ")[0])}. <i>Lex Plataformae</i>, versão {VERSAO}, {DATA_VERSAO}. Disponível em {esc(canonico)}</p>
    </div>
    <div class="ciencia rodape-estudo">
      <p><a href="{prefixo}tese/{PDF_NOME}">Texto integral em PDF</a>. Todo texto entre aspas é transcrição literal, com a página indicada. Acréscimos posteriores aparecem marcados e datados. Todos os direitos reservados até a definição da licença do projeto.</p>
    </div>
    {assinatura}
  </footer>
</div>
<script src="{prefixo}assets/atlas.js?v={VERSAO_ASSETS}" defer></script>
</body>
</html>
"""


# Camada externa. Texto simples da primeira vista, em conteudo/camada-externa.md, com os trechos que cada bloco condensa.
def carregar_externa():
    arq = RAIZ / "conteudo" / "camada-externa.md"
    dados, pag, campo_ = {}, None, None
    if not arq.exists():
        return dados
    for linha in arq.read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            pag, campo_ = linha[3:].strip(), None
            dados.setdefault(pag, {})
            continue
        if linha.startswith("### ") and pag:
            campo_, _, pergunta = linha[4:].strip().partition(" ")
            dados[pag][campo_] = {"paragrafos": [], "citacoes": [], "pergunta": pergunta.strip()}
            continue
        if not (pag and campo_):
            continue
        m = re.match(r"^> (.+?) \((p\. [\d\-]+|Resumo)\)\s*$", linha)
        if m:
            dados[pag][campo_]["citacoes"].append({"texto": m.group(1), "ref": m.group(2)})
        elif linha.strip():
            dados[pag][campo_]["paragrafos"].append(linha.strip())
    return dados


EXTERNA = carregar_externa()


# Doutrina. A prosa para quem vai operar, em conteudo/doutrina.md. Os trechos que a sustentam só ficam à vista na Ciência,
# e a citação de impacto, marcada com >!, aparece também na Doutrina. Revisão de voz de 05/11/2026.
def carregar_doutrina():
    arq = RAIZ / "conteudo" / "doutrina.md"
    dados, pag, sec = {}, None, None
    if not arq.exists():
        return dados
    for linha in arq.read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            pag, sec = linha[3:].strip(), None
            dados[pag] = []
            continue
        if linha.startswith("### ") and pag:
            sec = {"titulo": linha[4:].strip(), "paragrafos": [], "ancoras": [], "impacto": []}
            dados[pag].append(sec)
            continue
        if not sec:
            continue
        m = re.match(r"^>(!?) (.+?) \((p\. [\d\-]+|Resumo)\)\s*$", linha)
        if m:
            sec["impacto" if m.group(1) else "ancoras"].append({"texto": m.group(2), "ref": m.group(3)})
        elif linha.strip():
            sec["paragrafos"].append(linha.strip())
    return dados


DOUTRINA = carregar_doutrina()


def trechos_da_doutrina(chave):
    """Os trechos que a prosa da Doutrina já traz, para a ficha não repetir na Ciência."""
    return {q["texto"] for s in DOUTRINA.get(chave, []) for q in s["ancoras"] + s["impacto"]}


def doutrina_html(chave, prefixo, nivel="h2"):
    """As seções da Doutrina. Aparecem na Doutrina e na Ciência, e na Ciência trazem os trechos em que se apoiam."""
    secoes = []
    for s in DOUTRINA.get(chave, []):
        impacto = "".join(f'<blockquote class="citacao impacto"><p>{esc(q["texto"])}{pg(q["ref"], prefixo, q["texto"])}</p></blockquote>' for q in s["impacto"])
        cabeca = "" if s["titulo"] == "Texto" else f'<{nivel} class="rotulo-ext">{esc(s["titulo"])}</{nivel}>'
        secoes.append(f'<section class="ext bloco-doutrina">{cabeca}'
                      + "".join(f"<p>{esc(t)}</p>" for t in s["paragrafos"]) + impacto + expansao(s["ancoras"], prefixo, "ciencia") + "</section>")
    return "".join(secoes)


# Curso. A Doutrina como doutrina didática para juristas, em conteudo/doutrina/, um arquivo por capítulo. Adequação das camadas de 05/11/2026.
def carregar_curso():
    capitulos = []
    for arq in sorted((RAIZ / "conteudo" / "curso").glob("*.md")):
        cap = {"slug": arq.stem.split("-", 1)[1], "titulo": "", "abertura": "", "secoes_tese": [], "secoes": []}
        sec, par = None, None
        for linha in arq.read_text(encoding="utf-8").splitlines():
            if linha.startswith("# "):
                cap["titulo"] = linha[2:].strip()
            elif linha.startswith("abertura: "):
                cap["abertura"] = linha[10:].strip()
            elif linha.startswith("secoes: "):
                cap["secoes_tese"] = [x.strip() for x in linha[8:].split(",")]
            elif linha.startswith("## "):
                titulo = linha[3:].strip()
                caso = titulo.startswith("caso ")
                sec = {"titulo": titulo[5:] if caso else titulo, "caso": caso, "paragrafos": []}
                cap["secoes"].append(sec)
                par = None
            elif sec is not None and linha.strip():
                m = re.match(r"^>(!?) (.+?) \((p\. [\d\-]+|Resumo)\)\s*$", linha)
                if m:
                    if par is None:
                        raise SystemExit(f"Curso, {arq.name}. Trecho sem parágrafo antes, {linha[:60]}")
                    par["impacto" if m.group(1) else "ancoras"].append({"texto": m.group(2), "ref": m.group(3)})
                else:
                    par = {"texto": linha.strip(), "ancoras": [], "impacto": []}
                    sec["paragrafos"].append(par)
        capitulos.append(cap)
    return capitulos


CURSO = carregar_curso()

# O capítulo do curso de cada página da Doutrina, para que Situações, Parâmetros, Diretrizes, Limites, fichas e plataformas
# apontem para onde o tema se estuda a fundo. Adequação das camadas, etapa 4, 08/11/2026.
CURSO_CONCEITO = {
    "oic": "objeto", "feixe-de-fruicao-governada": "objeto", "lex-plataformae": "lei-da-plataforma",
    "vulnerabilidade-semiotica": "vulnerabilidade", "antecipacao-hipercuratorial": "informacao",
    "auditabilidade-aberta": "auditabilidade", "equivalencia-de-valor-funcional": "equivalencia",
    "teleologia-abusiva": "ilicito", "ilicito-de-arquitetura": "ilicito", "funcao-social-da-pi": "propriedade-intelectual",
    "recomposicao-funcional": "remedios", "cativeiro-identitario": "vulnerabilidade", "consentimento-viciado-por-sentido": "vulnerabilidade",
    "consumidor-cidadao": "lei-da-plataforma", "continuidade-biografica": "bens-protegidos", "integridade-pessoal": "bens-protegidos",
    "publicidade-enganosa-por-arquitetura": "vulnerabilidade", "transparencia-performatica": "vulnerabilidade",
    "teleologia-arquitetural": "economia", "dano-arquitetura": "ilicito",
}
# A situação g não tem enunciado próprio no 7.1.1. A sanção privada se estuda no capítulo sobre a lei da plataforma.
CURSO_SITUACAO = {"g": "lei-da-plataforma"}


def capitulo_curso(num=None, slug=None):
    for c in CURSO:
        if (slug and c["slug"] == slug) or (num and not slug and num in c["secoes_tese"]):
            return c
    return None


def link_curso(c, prefixo):
    return f'<a href="{prefixo}doutrina/{c["slug"]}/">{esc(c["titulo"])}, no caminho do jurista</a>' if c else ""


def no_curso_html(c, prefixo):
    """O caminho de uma página da Doutrina até o capítulo do curso que trata do mesmo tema."""
    if not c:
        return ""
    return (f'<section class="bloco no-curso"><h2>Onde estudar a fundo?</h2>'
            f'<p>No capítulo <a href="{prefixo}doutrina/{c["slug"]}/">{esc(c["titulo"])}</a>, no caminho do jurista.</p></section>')


def curso_paragrafo(par, prefixo):
    """Um parágrafo do curso. Na Doutrina, os trechos que o sustentam abrem no sinal ao lado dele, com a referência no balão.
    Na Ciência, ficam à vista. A citação de impacto aparece nos dois modos."""
    trechos = par["ancoras"] + par["impacto"]
    def citas(lista):
        return "".join(f'<blockquote class="citacao"><p>{esc(q["texto"])}{pg(q["ref"], prefixo, q["texto"])}</p></blockquote>' for q in lista)
    # Na Doutrina o texto corre sem sinal ao lado de cada parágrafo. Os trechos que o sustentam ficam na Ciência,
    # e a citação de impacto vira caixa de destaque, como nos portais jurídicos. Crítica do autor de 09/11/2026.
    impacto = "".join(f'<aside class="caixa-citacao"><blockquote class="citacao impacto"><p>{esc(q["texto"])}{pg(q["ref"], prefixo, q["texto"])}</p></blockquote></aside>' for q in par["impacto"])
    return f'<div class="par-curso"><p>{esc(par["texto"])}</p></div>' + impacto + expansao(par["ancoras"], prefixo, "ciencia")


def irmas_curso(atual, prefixo):
    return ("Caminho do jurista", [(esc(c["titulo"]), f'{prefixo}doutrina/{c["slug"]}/', c["slug"] == atual) for c in CURSO])


def gerar_curso():
    if not CURSO:
        return
    raiz = SAIDA / "doutrina"
    raiz.mkdir(parents=True, exist_ok=True)
    for i, c in enumerate(CURSO):
        prefixo = "../../"
        partes = []
        for s in c["secoes"]:
            corpo_sec = "".join(curso_paragrafo(p, prefixo) for p in s["paragrafos"])
            classe = "ext bloco-curso bloco-curso-caso" if s["caso"] else "ext bloco-curso"
            partes.append(f'<section class="{classe}"><h2 class="rotulo-ext">{esc(s["titulo"])}</h2>{corpo_sec}</section>')
        saidas = []
        if i + 1 < len(CURSO):
            saidas.append((f'A seguir, {CURSO[i + 1]["titulo"]}', f'{prefixo}doutrina/{CURSO[i + 1]["slug"]}/'))
        saidas += [("O caminho do jurista inteiro", f"{prefixo}doutrina/"), ("As situações, para consulta", f"{prefixo}roteiro/"), ("A legislação", f"{prefixo}legislacao/")]
        origem = " · ".join(f'<a href="{prefixo}tese/{POR_NUMERO[n]["slug"]}/">{esc(n)}</a>' for n in c["secoes_tese"] if n in POR_NUMERO)
        corpo = (f'<article class="folha curso-capitulo"><nav class="trilha" aria-label="Você está em"><a href="../">Caminho do jurista</a></nav>'
                 f'<header class="folha-cabeca"><h1>{esc(c["titulo"])}</h1><p class="folha-lema">{esc(c["abertura"])}</p></header>'
                 + "".join(partes) + saidas_html(saidas)
                 + f'<p class="ciencia nota-camada" data-arq="fonte · as seções da tese que o capítulo reescreve">As seções da tese reescritas aqui são {origem}.</p></article>')
        jsonld = {"@context": "https://schema.org", "@type": "Article", "headline": c["titulo"], "inLanguage": "pt-BR", "url": f'{BASE}/doutrina/{c["slug"]}/',
                  "isBasedOn": BASE + "/#tese", "author": {"@type": "Person", "name": "Victor Luiz Pereira de Andrade"}}
        destino = raiz / c["slug"]
        destino.mkdir(parents=True, exist_ok=True)
        (destino / "index.html").write_text(
            pagina(f'{c["titulo"]} · Caminho do jurista · Lex Plataformae', c["abertura"], corpo, prefixo, f'doutrina/{c["slug"]}/', jsonld,
                   camada="interna", superficie=prefixo, irmas=irmas_curso(c["slug"], prefixo)), encoding="utf-8")
    itens = "".join(f'<li><a href="{c["slug"]}/">{esc(c["titulo"])}</a><p>{esc(c["abertura"])}</p></li>' for c in CURSO)
    aplicacoes = "".join(f'<li><a href="../plataformas/{s}/">{esc(ext_texto(s, "titulo") or t)}</a></li>' for s, t in APLICACOES_CURSO)
    corpo = ('<article class="folha curso-indice"><header class="folha-cabeca"><h1>O caminho do jurista</h1>'
             '<p class="folha-lema">Este caminho reconstrói, para advogados, magistrados, membros do Ministério Público e estudantes, o regime jurídico do Objeto Imaterial de Consumo. '
             'Cada capítulo parte de um problema, mostra por que a leitura comum não basta e chega ao que se pode demonstrar e pedir.</p></header>'
             f'<section class="ext"><h2 class="rotulo-ext">Quais são os capítulos?</h2><ol class="curso-lista">{itens}</ol></section>'
             f'<section class="ext"><h2 class="rotulo-ext">Como o regime se aplica a outras plataformas?</h2><ul class="partes-curtas">{aplicacoes}</ul></section>'
             + saidas_html([("As situações, para consulta", "../roteiro/"), ("A legislação", "../legislacao/"), ("Os conceitos", "../conceitos/")]) + "</article>")
    jsonld = {"@context": "https://schema.org", "@type": "CreativeWork", "name": "O caminho do jurista", "inLanguage": "pt-BR", "url": f"{BASE}/doutrina/",
              "isBasedOn": BASE + "/#tese", "author": {"@type": "Person", "name": "Victor Luiz Pereira de Andrade"}}
    (raiz / "index.html").write_text(
        pagina("Caminho do jurista pelo regime do consumo digital · Lex Plataformae", "O regime do Objeto Imaterial de Consumo para juristas, do problema à prova e aos remédios, em quinze capítulos.",
               corpo, "../", "doutrina/", jsonld, camada="interna", superficie="../"), encoding="utf-8")


APLICACOES_CURSO = [("funcionalidade-cognitiva", "Assistentes de inteligência artificial"), ("infraestrutura-e-intermediacao", "Lojas virtuais e redes sociais"),
                    ("produtividade-gig-economy", "Trabalho por aplicativo"), ("administracao-de-confianca", "A administração da confiança"),
                    ("concorrencia", "A concorrência"), ("tutela-coletiva", "A tutela coletiva"), ("consumidor-equiparado", "O consumidor equiparado")]


# Percurso. A superfície conta a tese inteira a partir da compra de uma skin, em conteudo/percurso.md.
def carregar_percurso():
    arq = RAIZ / "conteudo" / "percurso.md"
    partes, atual, bloco = [], None, None
    if not arq.exists():
        return partes
    for linha in arq.read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            atual = {"slug": linha[3:].strip(), "titulo": "", "resumo": "", "pergunta": "", "blocos": []}
            partes.append(atual)
            bloco = None
            continue
        if linha.startswith("### ") and atual is not None:
            tipo, _, arg = linha[4:].strip().partition(" ")
            bloco = {"tipo": tipo, "arg": arg.strip(), "paragrafos": [], "citacoes": []}
            if tipo not in ("titulo", "resumo", "pergunta"):
                atual["blocos"].append(bloco)
            continue
        if not (atual and bloco) or not linha.strip():
            continue
        m = re.match(r"^> (.+?) \((p\. [\d\-]+|Resumo)\)\s*$", linha)
        if m:
            bloco["citacoes"].append({"texto": m.group(1), "ref": m.group(2)})
        elif bloco["tipo"] in ("titulo", "resumo", "pergunta"):
            atual[bloco["tipo"]] = (atual[bloco["tipo"]] + " " + linha.strip()).strip()
        else:
            bloco["paragrafos"].append(linha.strip())
    return partes


PERCURSO = carregar_percurso()


# Direitos. O que a plataforma deve e o que o leitor pode pedir, em conteudo/direitos.md, uma situação do quadro por bloco.
# Os campos de cada direito, na ordem em que aparecem, com o rótulo que o leitor vê.
CAMPOS_DIREITO = {"quando": "Como reconhecer esta situação?", "deve": "O que a plataforma deve assegurar neste caso?",
                  "mostrar": "Como demonstrar o que aconteceu?", "pedir": "Que solução pode caber neste caso?",
                  "limite": "Quais são os limites dessa proteção?"}

# Cada campo de cada direito tem pergunta própria, tirada do que o campo responde. As perguntas genéricas de CAMPOS_DIREITO
# só valem para direito novo que ainda não tenha as suas. Perguntas orientadoras, por escolha do autor de 28/10/2026.
# Revisão de rótulos de 05/11/2026, que trocou as três perguntas repetidas nos onze cartões por perguntas de cada situação.
PERGUNTAS_DIREITO = {
    "a": {"quando": "Quando o que você comprou depende da plataforma?", "deve": "O que a plataforma deve preservar?",
          "mostrar": "Como mostrar o que você comprou e como usa?", "pedir": "E se a empresa disser que é só serviço ou licença?",
          "limite": "Reconhecer o produto já resolve o caso?"},
    "b": {"quando": "Quando os sinais da tela pesam contra você?", "deve": "Como a plataforma deve montar a experiência?",
          "mostrar": "Como mostrar o caminho que levou à sua decisão?", "pedir": "O que pedir quando a culpa é do ambiente?",
          "limite": "Todo jogo complicado viola direitos?"},
    "c": {"quando": "Quando a informação existe, mas não orienta?", "deve": "Que informação a plataforma deve dar?",
          "mostrar": "Como mostrar o que foi informado e o que faltou?", "pedir": "O que pedir quando a informação falhou?",
          "limite": "A questão é se você leu o contrato?"},
    "d": {"quando": "Quando a propaganda passa a fazer parte da oferta?", "deve": "O que o anúncio obriga a plataforma a entregar?",
          "mostrar": "Como comparar a promessa com o que foi entregue?", "pedir": "O que pedir quando a promessa não se cumpre?",
          "limite": "Propaganda insistente já é problema?"},
    "e": {"quando": "Quando uma mudança precisa deixar rastro?", "deve": "Que rastro a plataforma deve guardar?",
          "mostrar": "Que registros permitem entender a mudança ou a punição?", "pedir": "O que pedir para reconstituir a mudança?",
          "limite": "Todo ajuste pequeno exige registro?"},
    "f": {"quando": "Quando a atualização tira a função do que você comprou?", "deve": "O que a plataforma deve preservar no item?",
          "mostrar": "Como mostrar o que mudou na utilidade do item?", "pedir": "Que solução pode recompor a utilidade perdida?",
          "limite": "O jogo fica proibido de mudar?"},
    "g": {"quando": "Quando a punição passa do ponto?", "deve": "O que a plataforma deve fazer antes de punir?",
          "mostrar": "Como documentar a punição e a tentativa de contestar?", "pedir": "Que revisão pode ser pedida para a punição?",
          "limite": "Então a plataforma não pode punir?"},
    "h": {"quando": "Quando a perda vira rotina do jogo?", "deve": "O que o desenho do jogo não pode buscar?",
          "mostrar": "Como mostrar que o problema forma um padrão?", "pedir": "Dá para pedir mais do que o conserto de um caso?",
          "limite": "Toda forma de vender e convencer é abusiva?"},
    "i": {"quando": "Quando a prova fica toda com a plataforma?", "deve": "O que a plataforma deve fazer com os registros?",
          "mostrar": "O que você pode mostrar e o que está com a plataforma?", "pedir": "Como distribuir a prova conforme o acesso aos registros?",
          "limite": "Você fica dispensado de contar o que aconteceu?"},
    "j": {"quando": "Quando os direitos sobre o jogo viram escudo?", "deve": "Como a empresa deve usar a exclusividade?",
          "mostrar": "Como avaliar a justificativa para a restrição?", "pedir": "O que pedir quando a empresa invoca a obra?",
          "limite": "A empresa perde os direitos sobre o jogo?"},
    "k": {"quando": "Quando a perda pede mais do que dinheiro?", "deve": "Que resposta a plataforma deve dar?",
          "mostrar": "Como ligar a perda ao que a plataforma fez?", "pedir": "Que solução pode restaurar o que foi perdido?",
          "limite": "E a indenização em dinheiro?"},
}


def carregar_direitos():
    arq = RAIZ / "conteudo" / "direitos.md"
    dados, atual, campo_ = {}, None, None
    if not arq.exists():
        return dados
    for linha in arq.read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            atual = dados.setdefault(linha[3:].strip(), {"titulo": "", "paragrafos": [], "citacoes": [], "partes": [], "ideias": [],
                                                          **{k: [] for k in CAMPOS_DIREITO}})
            campo_ = None
            continue
        if linha.startswith("### ") and atual is not None:
            campo_ = linha[4:].strip()
            continue
        if atual is None or not campo_ or not linha.strip():
            continue
        m = re.match(r"^> (.+?) \((p\. [\d\-]+)\)\s*$", linha)
        if m:
            atual["citacoes"].append({"texto": m.group(1), "ref": m.group(2)})
        elif campo_ == "titulo":
            atual["titulo"] = (atual["titulo"] + " " + linha.strip()).strip()
        elif campo_ in ("partes", "ideias"):
            atual[campo_] += [x.strip() for x in linha.split(",") if x.strip()]
        elif campo_ in CAMPOS_DIREITO:
            atual[campo_].append(linha.strip())
        else:
            atual["paragrafos"].append(linha.strip())
    return dados


DIREITOS = carregar_direitos()
LETRAS_DIREITOS = [k for k in DIREITOS if len(k) == 1]


def direito_html(letra, prefixo, nivel="h3", ancora=False):
    """Um direito, com o título, o texto simples e os trechos que ele condensa. Em Doutrina, o caminho até a situação inteira."""
    d = DIREITOS[letra]
    ident = f' id="{letra}"' if ancora else ""
    partes = "".join(f'<div class="direito-parte parte-{k}"><dt>{esc(PERGUNTAS_DIREITO.get(letra, {}).get(k, rotulo))}</dt><dd>' + "".join(f"<p>{esc(t)}</p>" for t in d[k]) + "</dd></div>"
                     for k, rotulo in CAMPOS_DIREITO.items() if d[k])
    # Na Doutrina, o próprio título leva à situação inteira, para quem vai operar. Revisão de rótulos de 05/11/2026.
    titulo = (f'<span class="em-modo modo-0">{esc(d["titulo"])}</span>'
              f'<a class="em-modo modo-1 modo-2" href="{prefixo}roteiro/#{letra}" title="A situação inteira, para quem vai operar">{esc(d["titulo"])}</a>')
    return (f'<section class="ext direito"{ident}><{nivel} class="direito-titulo">{titulo}</{nivel}>'
            + "".join(f"<p>{esc(t)}</p>" for t in d["paragrafos"])
            + (f'<dl class="direito-partes">{partes}</dl>' if partes else "")
            + expansao(d["citacoes"], prefixo) + "</section>")


ROTULO_EXIGIR = "O que você pode exigir?"
ORDINAIS_N = {7: "sete", 8: "oito", 9: "nove", 10: "dez"}


def secao_direitos(letras, prefixo):
    """O fecho de direitos de uma página do percurso ou de uma ideia."""
    if not letras:
        return (f'<section class="ext direitos-curto"><p class="rotulo-ext">{ROTULO_EXIGIR}</p>'
                f'<p class="ver-direitos"><a href="{prefixo}direitos/">Os seus direitos, um por um</a></p></section>')
    return (f'<section class="direitos" aria-label="{ROTULO_EXIGIR}"><p class="rotulo-ext">{ROTULO_EXIGIR}</p>'
            + "".join(direito_html(l, prefixo) for l in letras)
            + f'<p class="ver-direitos"><a href="{prefixo}direitos/">Todos os seus direitos, e até onde eles vão</a></p></section>')


# Para operar. O guia da Doutrina para cada situação do Roteiro, em conteudo/operar.md.
CAMPOS_OPERAR = {"fatos": "Quais fatos precisam ser examinados?", "demonstrar": "Como demonstrar o problema?",
                 "fundamento": "Qual é o fundamento jurídico?", "cuidados": "Quais pressupostos e limites precisam ser conferidos?",
                 "caso": "Como isso aparece em um caso concreto?"}


# Perguntas próprias para o guia de cada situação. Revisão de rótulos de 05/11/2026.
PERGUNTAS_OPERAR = {
    "a": {"fatos": "Que fatos indicam um produto que depende do ambiente?", "demonstrar": "Como demonstrar a dependência do ambiente?",
          "fundamento": "Em que norma o produto imaterial se apoia?", "cuidados": "O que fica fora do portão de entrada?"},
    "b": {"fatos": "Que fatos mostram o sentido governado pelo fornecedor?", "demonstrar": "Como reconstruir a jornada do consumidor?",
          "fundamento": "Que normas tratam a vulnerabilidade e a informação?", "cuidados": "A vulnerabilidade semiótica se presume?"},
    "c": {"fatos": "Que fatos mostram informação que existe, mas não orienta?", "demonstrar": "Como demonstrar que o sentido não era cognoscível?",
          "fundamento": "Que normas exigem informação clara e ostensiva?", "cuidados": "Basta provar que o texto estava lá?"},
    "d": {"fatos": "Que fatos mostram a publicidade dentro da oferta?", "demonstrar": "Como ligar a promessa à fruição posterior?",
          "fundamento": "Que normas tornam a oferta vinculante?", "cuidados": "A insistência da propaganda basta?"},
    "e": {"fatos": "Que fatos mostram alteração sem rastro?", "demonstrar": "Que registros pedir para reconstruir a alteração?",
          "fundamento": "De onde vem o dever de deixar rastro?", "cuidados": "Como evitar a pescaria processual?",
          "caso": "Até onde a governança chegou no caso Vanguard?"},
    "f": {"fatos": "Que fatos mostram a utilidade esvaziada?", "demonstrar": "Como comparar o antes e o depois da alteração?",
          "fundamento": "Que normas controlam a modificação unilateral?", "cuidados": "Toda mutação é ilícita?"},
    "g": {"fatos": "Que fatos mostram sanção opaca ou reversão assimétrica?", "demonstrar": "Que registros da sanção pedir?",
          "fundamento": "Que normas controlam a sanção sem motivo?", "cuidados": "A existência do poder de sancionar basta?",
          "caso": "O que o caso dos presentes irregulares mostra?"},
    "h": {"fatos": "Que fatos mostram mecanismos operando juntos?", "demonstrar": "Como demonstrar o padrão, e não só o episódio?",
          "fundamento": "Que normas alcançam o arranjo inteiro?", "cuidados": "Quais requisitos precisam estar presentes juntos?"},
    "i": {"fatos": "Que fatos mostram a prova concentrada na plataforma?", "demonstrar": "O que cabe a cada parte mostrar?",
          "fundamento": "Que normas redistribuem o ônus da prova?", "cuidados": "A redistribuição dispensa a verossimilhança?"},
    "j": {"fatos": "Que fatos mostram a exclusividade usada como escudo?", "demonstrar": "Como separar a proteção do ativo da imunização da governança?",
          "fundamento": "Que normas ligam a exclusividade ao interesse social?", "cuidados": "A propriedade intelectual é veto geral ao CDC?"},
    "k": {"fatos": "Que perdas pedem recomposição?", "demonstrar": "Como ligar a governança à perda funcional?",
          "fundamento": "Que normas sustentam a tutela específica?", "cuidados": "A indenização sai de cena?"},
}


def carregar_operar():
    arq = RAIZ / "conteudo" / "operar.md"
    dados, atual, campo_ = {}, None, None
    if not arq.exists():
        return dados
    for linha in arq.read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            atual = dados.setdefault(linha[3:].strip(), {"texto": [], "citacoes": [], **{k: [] for k in CAMPOS_OPERAR}})
            campo_ = None
            continue
        if linha.startswith("### ") and atual is not None:
            campo_ = linha[4:].strip()
            continue
        if atual is None or not campo_ or not linha.strip():
            continue
        m = re.match(r"^> (.+?) \((p\. [\d\-]+)\)\s*$", linha)
        if m:
            atual["citacoes"].append({"texto": m.group(1), "ref": m.group(2)})
        elif campo_ in atual:
            atual[campo_].append(linha.strip())
    return dados


OPERAR = carregar_operar()


def operar_html(letra, prefixo):
    """O guia para operar uma situação. Os trechos que ele condensa ficam à vista só na Ciência."""
    o = OPERAR.get(letra)
    if not o:
        return ""
    partes = "".join(f'<div class="operar-parte parte-{k}"><dt>{esc(PERGUNTAS_OPERAR.get(letra, {}).get(k, rotulo))}</dt><dd>' + "".join(f"<p>{esc(t)}</p>" for t in o[k]) + "</dd></div>"
                     for k, rotulo in CAMPOS_OPERAR.items() if o[k])
    return (f'<section class="operar" aria-label="Guia para operar">'
            f'<dl class="operar-partes">{partes}</dl>' + expansao(o["citacoes"], prefixo, "ciencia") + "</section>")


def direitos_da_parte(slug):
    return [l for l in LETRAS_DIREITOS if slug in DIREITOS[l]["partes"]]


def direitos_da_ideia(cid):
    return [l for l in LETRAS_DIREITOS if cid in DIREITOS[l]["ideias"]]


# Por problema. Páginas para quem chega com um problema concreto, em conteudo/problemas.md. Rascunho de 03/11/2026.
# Cada página junta blocos que já estão no percurso e os direitos que se aplicam. Só o título e a abertura são novos.
# Os campos de texto próprio de cada problema, na ordem da página. Cada um traz no cabeçalho a sua pergunta, como em
# `### guardar O que vale a pena guardar antes de reclamar?`. Adequação das camadas, etapa 5, 08/11/2026. A Informação
# responde ao que a pessoa vive, diz se é o caso dela, o que guardar, o que pedir, a quem recorrer e onde a proteção para.
CAMPOS_PROBLEMA = ("caso", "guardar", "pedir", "quem", "limite")


# Como reclamar. Os caminhos fora da plataforma, em conteudo/como-reclamar.md, com os textos oficiais em
# estrutura/canais-reclamacao.json. Acréscimo posterior à tese, de 08/11/2026, por ordem do autor de 05/11/2026.
def carregar_como_reclamar():
    arq = RAIZ / "conteudo" / "como-reclamar.md"
    canais_arq = RAIZ / "estrutura" / "canais-reclamacao.json"
    if not arq.exists() or not canais_arq.exists():
        return {}
    canais = json.loads(canais_arq.read_text(encoding="utf-8"))
    d = {"titulo": "", "abertura": [], "secoes": [], "acesso": canais["acesso"],
         "leis": {x["id"]: x for x in canais["dispositivos"]}, "servicos": {x["id"]: x for x in canais["servicos"]}}
    atual = None
    for linha in arq.read_text(encoding="utf-8").splitlines():
        if linha.startswith("### "):
            campo_, _, pergunta = linha[4:].strip().partition(" ")
            if campo_ in ("titulo", "abertura"):
                atual = campo_
            else:
                d["secoes"].append({"campo": campo_, "pergunta": pergunta.strip(), "paragrafos": [], "citacoes": [], "lei": []})
                atual = "secao"
            continue
        if not atual or not linha.strip():
            continue
        m = re.match(r"^> (.+?) \((p\. [\d\-]+)\)\s*$", linha)
        if atual == "titulo":
            d["titulo"] = linha.strip()
        elif atual == "abertura":
            d["abertura"].append(linha.strip())
        elif m:
            d["secoes"][-1]["citacoes"].append({"texto": m.group(1), "ref": m.group(2)})
        elif linha.startswith("lei:"):
            ids = [x.strip() for x in linha[4:].split(",") if x.strip()]
            faltam = [x for x in ids if x not in d["leis"] and x not in d["servicos"]]
            if faltam:
                raise SystemExit(f"Como reclamar, fonte oficial que não existe em canais-reclamacao.json: {faltam}")
            d["secoes"][-1]["lei"] += ids
        else:
            d["secoes"][-1]["paragrafos"].append(linha.strip())
    return d


COMO_RECLAMAR = carregar_como_reclamar()


def carregar_problemas():
    arq = RAIZ / "conteudo" / "problemas.md"
    dados, atual, campo_ = {}, None, None
    if not arq.exists():
        return dados
    for linha in arq.read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            slug = linha[3:].strip()
            atual = dados.setdefault(slug, {"slug": slug, "titulo": "", "abertura": [], "citacoes": [], "blocos": [], "direitos": [], "relacionados": [],
                                            "percurso": [], "campos": {}})
            campo_ = None
            continue
        if linha.startswith("### ") and atual is not None:
            campo_, _, pergunta = linha[4:].strip().partition(" ")
            if campo_ in CAMPOS_PROBLEMA:
                atual["campos"][campo_] = {"pergunta": pergunta.strip(), "paragrafos": [], "citacoes": []}
            continue
        if atual is None or not campo_ or not linha.strip():
            continue
        m = re.match(r"^> (.+?) \((p\. [\d\-]+)\)\s*$", linha)
        if m:
            alvo = atual["campos"][campo_]["citacoes"] if campo_ in CAMPOS_PROBLEMA else atual["citacoes"]
            alvo.append({"texto": m.group(1), "ref": m.group(2)})
        elif campo_ in CAMPOS_PROBLEMA:
            atual["campos"][campo_]["paragrafos"].append(linha.strip())
        elif campo_ == "titulo":
            atual["titulo"] = (atual["titulo"] + " " + linha.strip()).strip()
        elif campo_ == "abertura":
            atual["abertura"].append(linha.strip())
        elif campo_ == "blocos":
            parte, _, inicio = linha.partition("|")
            atual["blocos"].append((parte.strip(), inicio.strip()))
        elif campo_ in ("direitos", "relacionados", "percurso"):
            atual[campo_] += [x.strip() for x in linha.split(",") if x.strip()]
    return dados


PROBLEMAS = carregar_problemas()


def bloco_do_percurso(slug, inicio):
    """O bloco do percurso cuja primeira frase começa com o texto indicado, e o número da parte."""
    for i, parte in enumerate(PERCURSO, 1):
        if parte["slug"] != slug:
            continue
        for b in parte["blocos"]:
            if b["paragrafos"] and b["paragrafos"][0].startswith(inicio):
                return i, parte, b
    raise SystemExit(f"Problema com bloco que não existe no percurso  {slug}  {inicio}")


def cuidado_html(prefixo):
    """O aviso de Seus direitos de que nada é fórmula pronta nem garantia de resultado, com os trechos que o sustentam."""
    intro = DIREITOS.get("intro", {"paragrafos": [], "citacoes": []})
    texto = next((t for t in intro["paragrafos"] if t.startswith("Leia com um cuidado")), "")
    if not texto:
        return ""
    cits = [q for q in intro["citacoes"] if q["ref"] in ("p. 748", "p. 788")]
    return f'<section class="ext nota-cuidado" aria-label="O que isto não garante"><p>{esc(texto)}</p>{expansao(cits, prefixo)}</section>'


def lista_problemas(slugs, prefixo, classe="partes-curtas"):
    return (f'<ul class="{classe}">' + "".join(f'<li><a href="{prefixo}problemas/{s}/">{esc(PROBLEMAS[s]["titulo"])}</a></li>' for s in slugs) + "</ul>")


def gerar_problemas():
    if not PROBLEMAS:
        return
    raiz = SAIDA / "problemas"
    raiz.mkdir(parents=True, exist_ok=True)
    itens = "".join(f'<li><a href="{p["slug"]}/"><span class="parte-titulo">{esc(p["titulo"])}</span>'
                    f'<span class="parte-resumo">{esc(primeira_frase(p["abertura"][0]))}</span></a></li>' for p in PROBLEMAS.values())
    corpo = (f'<article class="folha problemas-pagina"><p class="sobrelinha-ext"><a href="../direitos/">Seus direitos</a></p>'
             f'<header class="folha-cabeca ext-cabeca"><h1>Qual é o seu problema?</h1></header>'
             f'<ul class="partes problemas-lista">{itens}</ul>'
             + (f'<p class="ver-reclamar"><a href="../como-reclamar/">{esc(COMO_RECLAMAR["titulo"])}</a></p>' if COMO_RECLAMAR else "")
             + cuidado_html("../")
             + f'<section class="ext duvida"><div class="acoes"><a class="botao" href="../direitos/">Todos os seus direitos</a>{botao_desnudar()}</div></section></article>')
    jsonld = {"@context": "https://schema.org", "@type": "CollectionPage", "headline": "Qual é o seu problema?", "inLanguage": "pt-BR",
              "url": f"{BASE}/problemas/", "isBasedOn": BASE + "/#tese", "author": {"@type": "Person", "name": "Victor Luiz Pereira de Andrade"}}
    (raiz / "index.html").write_text(
        pagina("Problemas comuns com contas, itens e jogos digitais · Lex Plataformae",
               "Conta bloqueada, item alterado, jogo encerrado e outros problemas comuns, com o que a plataforma deve e o que você pode pedir.",
               corpo, "../", "problemas/", jsonld, camada="mista", imagem="problemas"), encoding="utf-8")
    prefixo = "../../"
    for p in PROBLEMAS.values():
        blocos, partes = [], {}
        for slug, inicio in p["blocos"]:
            i, parte, b = bloco_do_percurso(slug, inicio)
            blocos.append(bloco_percurso(b, prefixo))
            partes.setdefault(i, parte)
        for slug in p["percurso"]:
            i, parte = next((i, x) for i, x in enumerate(PERCURSO, 1) if x["slug"] == slug)
            partes.setdefault(i, parte)
        # Com texto próprio, a página responde campo a campo e leva aos direitos pelo título, sem repetir o cartão inteiro.
        proprio = "".join(
            f'<section class="ext problema-campo campo-{k}"><h2 class="pergunta-secao">{esc(c["pergunta"])}</h2>'
            + "".join(f"<p>{esc(t)}</p>" for t in c["paragrafos"]) + expansao(c["citacoes"], prefixo)
            + (f'<p class="ver-reclamar"><a href="{prefixo}como-reclamar/">Os canais de reclamação e os prazos</a></p>' if k == "quem" and COMO_RECLAMAR else "")
            + "</section>"
            for k in CAMPOS_PROBLEMA if (c := p["campos"].get(k)))
        no_percurso = (f'<section class="ext no-percurso"><p class="rotulo-ext">{ROTULO_NO_PERCURSO}</p><ul class="partes-curtas">'
                       + "".join(f'<li><a href="{prefixo}caminho/{parte["slug"]}/"><span class="parte-num">{i}</span>{esc(parte["titulo"])}</a></li>'
                                 for i, parte in sorted(partes.items()))
                       + "</ul></section>")
        if proprio:
            direitos = (f'<section class="ext direitos-curtos"><p class="rotulo-ext">Os direitos por trás deste caso</p><ul class="partes-curtas">'
                        + "".join(f'<li><a href="{prefixo}direitos/#{l}">{esc(DIREITOS[l]["titulo"])}</a></li>' for l in p["direitos"])
                        + "</ul></section>") if p["direitos"] else ""
            blocos = []
        else:
            direitos = (f'<section class="direitos" aria-label="{ROTULO_EXIGIR}"><p class="rotulo-ext">{ROTULO_EXIGIR}</p>'
                        + "".join(direito_html(l, prefixo, "h2") for l in p["direitos"])
                        + f'<p class="ver-direitos"><a href="{prefixo}direitos/">Todos os seus direitos, e até onde eles vão</a></p></section>')
        outros = (f'<section class="ext outros-problemas"><p class="rotulo-ext">Outros problemas parecidos</p>{lista_problemas(p["relacionados"], prefixo)}'
                  f'<p class="ver-direitos"><a href="{prefixo}problemas/">Todos os problemas</a></p></section>') if p["relacionados"] else ""
        corpo = (f'<article class="folha problema-pagina">'
                 f'<p class="sobrelinha-ext"><a href="{prefixo}direitos/">Seus direitos</a> · <a href="{prefixo}problemas/">Por problema</a></p>'
                 f'<header class="folha-cabeca ext-cabeca"><h1>{esc(p["titulo"])}</h1></header>'
                 f'<section class="ext abertura-problema">' + "".join(f"<p>{esc(t)}</p>" for t in p["abertura"]) + expansao(p["citacoes"], prefixo) + "</section>"
                 + proprio + "".join(blocos) + direitos + (no_percurso if partes else "") + cuidado_html(prefixo) + outros
                 + f'<section class="ext duvida"><div class="acoes"><a class="botao" href="{prefixo}caminho/">Seguir a skin desde a compra</a>{botao_desnudar()}</div></section>'
                 + "</article>")
        jsonld = {"@context": "https://schema.org", "@type": "Article", "headline": p["titulo"], "inLanguage": "pt-BR",
                  "url": f'{BASE}/problemas/{p["slug"]}/', "isBasedOn": BASE + "/#tese", "author": {"@type": "Person", "name": "Victor Luiz Pereira de Andrade"}}
        destino = raiz / p["slug"]
        destino.mkdir(parents=True, exist_ok=True)
        (destino / "index.html").write_text(
            pagina(f'{p["titulo"]} · Lex Plataformae', " ".join(p["abertura"]), corpo, prefixo, f'problemas/{p["slug"]}/', jsonld, camada="mista",
                   imagem=f'problema-{p["slug"]}',
                   irmas=("Todos os problemas", [(esc(x["titulo"]), f'../{x["slug"]}/', x is p) for x in PROBLEMAS.values()])),
            encoding="utf-8")


MESES = ("janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro")


def gerar_como_reclamar():
    C = COMO_RECLAMAR
    if not C:
        return
    prefixo = "../"
    ano, mes, dia = C["acesso"].split("-")
    data = f'{int(dia)} de {MESES[int(mes) - 1]} de {ano}'

    def fontes_html(ids):
        partes = []
        for i in ids:
            if i in C["leis"]:
                l = C["leis"][i]
                partes.append(f'<details class="lei-texto"><summary>O que diz o {esc(l["rotulo"])}</summary><p>{esc(l["texto"])}</p>'
                              f'<p class="fonte-lei">{esc(l["lei"])}, no <a href="{l["fonte"]}">site do Planalto</a></p></details>')
            else:
                v = C["servicos"][i]
                partes.append(f'<details class="lei-texto"><summary>As regras do {esc(v["nome"])}</summary><ul>'
                              + "".join(f"<li>{esc(r)}</li>" for r in v["regras"]) + "</ul>"
                              + f'<p class="fonte-lei">Nas páginas oficiais do <a href="{v["fontes"][0]}">{esc(v["nome"])}</a> e do <a href="{v["fontes"][1]}">Ministério da Justiça</a></p></details>')
        return "".join(partes)

    secoes = "".join(
        f'<section class="ext reclamar-secao campo-{x["campo"]}"><h2 class="pergunta-secao">{esc(x["pergunta"])}</h2>'
        + "".join(f"<p>{esc(t)}</p>" for t in x["paragrafos"]) + fontes_html(x["lei"]) + expansao(x["citacoes"], prefixo) + "</section>"
        for x in C["secoes"])
    corpo = (f'<article class="folha reclamar-pagina">'
             f'<p class="sobrelinha-ext"><a href="{prefixo}direitos/">Seus direitos</a> · <a href="{prefixo}problemas/">Por problema</a></p>'
             f'<header class="folha-cabeca ext-cabeca"><h1>{esc(C["titulo"])}</h1></header>'
             f'<section class="ext abertura-problema">' + "".join(f"<p>{esc(t)}</p>" for t in C["abertura"])
             + f'<p class="nota-acrescimo">Informação acrescentada em {data}, a partir da lei e dos canais oficiais.'
             + '<span class="ciencia"> É acréscimo posterior à tese, que não trata dos canais de reclamação.</span></p></section>'
             + secoes
             + saidas_html([("Qual é o seu problema?", f"{prefixo}problemas/"), ("Seus direitos", f"{prefixo}direitos/"), ("Siga a skin desde a compra", f"{prefixo}caminho/")])
             + "</article>")
    jsonld = {"@context": "https://schema.org", "@type": "Article", "headline": C["titulo"], "inLanguage": "pt-BR", "url": f"{BASE}/como-reclamar/",
              "dateModified": C["acesso"], "author": {"@type": "Person", "name": "Victor Luiz Pereira de Andrade"}}
    destino = SAIDA / "como-reclamar"
    destino.mkdir(parents=True, exist_ok=True)
    (destino / "index.html").write_text(
        pagina(f'{C["titulo"]} Procon, Consumidor.gov.br, Juizado e prazos · Lex Plataformae', primeira_frase(C["abertura"][0]), corpo, prefixo,
               "como-reclamar/", jsonld, camada="mista", imagem="como-reclamar"),
        encoding="utf-8")


# Epígrafes. A página da trilha sonora, com a função das nove canções e o que cada uma anuncia, nas palavras do 2.6.
# Texto em conteudo/camada-externa.md, página epigrafes. Auditoria de estrutura de 04/11/2026.
def credito_epigrafe(e):
    """Artista, faixa e ano, com o diálogo que a quinta epígrafe de capítulo traz."""
    extra = next((x.get("dialogo") for x in D["epigrafes"]["epigrafes"] if x["ordem"] == e.get("ordem")), None) or e.get("dialogo")
    base = f'{esc(e["artista"])}, <cite>{esc(e["faixa"])}</cite> ({e["ano"]})'
    if extra:
        base += f', em diálogo com {esc(extra["artista"])}, <cite>{esc(extra["obra"])}</cite> ({extra["ano"]})'
    return base


def gerar_epigrafes():
    pag = EXTERNA.get("epigrafes")
    if not pag:
        return
    prefixo = "../"
    ep = D["epigrafes"]

    def secao(campo_, pergunta):
        b = pag.get(campo_)
        if not b:
            return ""
        return (f'<section class="ext"><h2 class="pergunta-secao">{esc(pergunta)}</h2>'
                + "".join(f"<p>{esc(t)}</p>" for t in b["paragrafos"]) + expansao(b["citacoes"], prefixo) + "</section>")

    itens = []
    for e in ep["epigrafes"]:
        b = pag.get(f'cancao-{e["ordem"]}', {"paragrafos": [], "citacoes": []})
        m = re.match(r"(\d+)\s+(.*)", e["abre"])
        sec = POR_NUMERO.get(m.group(1)) if m else None
        capitulo = (f'<p class="cancao-capitulo ciencia">{"Abre a tese, como epígrafe geral" if e["abre"] == "Abertura" else "Abre " + esc(e["abre"])} · '
                    + (f'<a href="{prefixo}tese/{sec["slug"]}/">A seção no texto integral</a> · ' if sec else f'<a href="{prefixo}tese/">O texto integral</a> · ')
                    + f'<a href="{prefixo}tese/{PDF_NOME}#page={e["pagina_pdf"]}">Ler a epígrafe no PDF</a></p>')
        itens.append(f'<li class="cancao" id="epigrafe-{e["ordem"]}"><p class="cancao-nome"><span class="parte-num">{e["ordem"]}</span><span>{credito_epigrafe(e)}</span></p>'
                     + capitulo + "".join(f"<p>{esc(t)}</p>" for t in b["paragrafos"]) + expansao(b["citacoes"], prefixo) + "</li>")
    player = (f'<section class="ext"><h2 class="pergunta-secao">Como ouvir?</h2>'
              f'<div class="epigrafes-player" data-embed="{esc(ep["playlist"]["embed"])}" data-arq="terceiro · o Spotify só carrega depois do clique">'
              '<div class="ouvir"><button type="button" class="botao epigrafes-carregar">Ouvir a playlist aqui</button>'
              f'<p class="aviso">Ao carregar o player, o Spotify passa a receber dados desta visita. Nada toca sem que você aperte o play. Se preferir, '
              f'<a href="{esc(ep["playlist"]["url"])}" rel="noopener">abra a playlist direto no Spotify</a>.</p></div></div></section>')
    sec26 = POR_NUMERO.get("2.6")
    corpo = (f'<article class="folha epigrafes-pagina"><p class="sobrelinha-ext">Trilha sonora</p>'
             f'<header class="folha-cabeca ext-cabeca"><h1>{esc(ext_texto("epigrafes", "titulo"))}</h1></header>'
             + f'<section class="ext">{ext_html("epigrafes", "abertura", prefixo)}</section>'
             + secao("moldura", "Para que servem as canções?")
             + secao("musas", "Por que nove?")
             + secao("idiomas", "Por que umas em inglês e outras em português?")
             + f'<section class="ext"><h2 class="pergunta-secao">Quais são as nove canções?</h2><ol class="cancoes">{"".join(itens)}</ol></section>'
             + secao("villain", "Por que uma delas foi feita pela própria empresa do jogo?")
             + secao("fermata", "Por que do medo à fermata?")
             + player
             + (f'<p class="nota-camada">O método das epígrafes está por inteiro na seção <a href="{prefixo}tese/{sec26["slug"]}/">{esc(rotulo_secao(sec26))}</a>. As letras estão no PDF, na página em que cada epígrafe abre a sua etapa.</p>' if sec26 else "")
             + saidas_html([("O método da pesquisa", f"{prefixo}metodo/"), ("O texto integral", f"{prefixo}tese/"), ("Os autores", f"{prefixo}autores/")])
             + '</article>')
    jsonld = {"@context": "https://schema.org", "@type": "Article", "headline": ext_texto("epigrafes", "titulo"), "inLanguage": "pt-BR",
              "url": f"{BASE}/epigrafes/", "isBasedOn": BASE + "/#tese", "author": {"@type": "Person", "name": "Victor Luiz Pereira de Andrade"}}
    destino = SAIDA / "epigrafes"
    destino.mkdir(parents=True, exist_ok=True)
    (destino / "index.html").write_text(
        pagina("Epígrafes musicais, o método do 2.6 da tese · Lex Plataformae", ext_texto("epigrafes", "abertura"), corpo, prefixo, "epigrafes/",
               jsonld, camada="ciencia", superficie=prefixo, imagem="epigrafes"), encoding="utf-8")


def gerar_direitos():
    prefixo = "../"
    intro = DIREITOS.get("intro", {"paragrafos": [], "citacoes": []})
    indice = "".join(f'<li><a href="#{l}">{esc(DIREITOS[l]["titulo"])}</a></li>' for l in LETRAS_DIREITOS)
    problemas = (f'<nav class="ext problemas-curto" aria-label="Por problema"><p class="rotulo-ext">Qual é o seu problema?</p>'
                 f'{lista_problemas(PROBLEMAS, prefixo)}'
                 + (f'<p class="ver-reclamar"><a href="{prefixo}como-reclamar/">{esc(COMO_RECLAMAR["titulo"])}</a></p>' if COMO_RECLAMAR else "")
                 + '</nav>') if PROBLEMAS else ""
    corpo = (f'<article class="folha direitos-pagina"><header class="folha-cabeca ext-cabeca"><h1>Seus direitos</h1></header>'
             f'<section class="ext">' + "".join(f"<p>{esc(t)}</p>" for t in intro["paragrafos"]) + expansao(intro["citacoes"], prefixo) + "</section>"
             + problemas +
             f'<nav class="direitos-indice" aria-label="Os direitos"><ol>{indice}</ol></nav>'
             + "".join(direito_html(l, prefixo, "h2", ancora=True) for l in LETRAS_DIREITOS)
             + f'<section class="ext duvida"><div class="acoes"><a class="botao" href="{prefixo}caminho/">Seguir a skin desde a compra</a>{botao_desnudar()}</div></section>'
             + "</article>")
    destino = SAIDA / "direitos"
    destino.mkdir(parents=True, exist_ok=True)
    jsonld = {"@context": "https://schema.org", "@type": "Article", "headline": "Seus direitos", "inLanguage": "pt-BR",
              "url": f"{BASE}/direitos/", "isBasedOn": BASE + "/#tese", "author": {"@type": "Person", "name": "Victor Luiz Pereira de Andrade"}}
    (destino / "index.html").write_text(
        pagina("Seus direitos ao comprar itens, contas e acessos digitais · Lex Plataformae",
               "O que a plataforma deve a quem compra itens, contas e acessos digitais, e o que você pode pedir quando alguma coisa dá errado.",
               corpo, prefixo, "direitos/", jsonld, camada="mista"), encoding="utf-8")


# Ilustrações conceituais. O plano fica em estrutura/ilustracoes.md e os arquivos em site/ilustracoes/<id>.webp.
# Sem arquivo, o lugar aparece só no degrau Despir, como ilustração prevista.
ILUSTRACOES_DIR = RAIZ / "site" / "ilustracoes"
EXTENSOES = (".webp", ".avif", ".png", ".jpg")
AVISO_IA = "Ilustração conceitual feita com IA."


def carregar_ilustracoes():
    arq = RAIZ / "estrutura" / "ilustracoes.md"
    pecas, atual, campo_ = {}, None, None
    if not arq.exists():
        return pecas
    for linha in arq.read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            atual = pecas.setdefault(linha[3:].strip(), {"citacoes": []})
            campo_ = None
            continue
        if linha.startswith("### ") and atual is not None:
            campo_ = linha[4:].strip()
            continue
        if atual is None or not campo_ or not linha.strip():
            continue
        m = re.match(r"^> (.+?) \((p\. [\d\-]+)\)\s*$", linha)
        if m:
            atual["citacoes"].append({"texto": m.group(1), "ref": m.group(2)})
        else:
            atual[campo_] = (atual.get(campo_, "") + " " + linha.strip()).strip()
    return pecas


ILUSTRACOES = carregar_ilustracoes()
ILUSTRACOES_USADAS = set()


def arquivo_ilustracao(ident):
    for ext in EXTENSOES:
        f = ILUSTRACOES_DIR / f"{ident}{ext}"
        if f.exists():
            return f
    return None


def figura(ident, prefixo, destaque=False):
    """A peça ilustrativa prevista para um lugar. Com arquivo, a figura. Sem arquivo, a marca no degrau Despir."""
    peca = ILUSTRACOES.get(ident)
    if not peca:
        return ""
    ILUSTRACOES_USADAS.add(ident)
    formato = "formato-4x3" if peca.get("formato", "").startswith("4") else "formato-16x9"
    arq = arquivo_ilustracao(ident)
    if not arq:
        return (f'<figure class="ilustracao prevista arq {formato}" data-arq="ilustração prevista · {esc(ident)}">'
                f'<p>{esc(peca.get("ideia", ""))}</p></figure>')
    from PIL import Image
    with Image.open(arq) as im:
        largura, altura = im.size
    # A identidade é clara em todos os aparelhos. Não selecionar uma arte escura
    # só porque o sistema operacional prefere escuro.
    carregamento = 'loading="eager" fetchpriority="high"' if destaque else 'loading="lazy"'
    return (f'<figure class="ilustracao {formato}"><picture>'
            f'<img src="{prefixo}assets/ilustracoes/{arq.name}" alt="{esc(peca.get("alt", ""))}" width="{largura}" height="{altura}" {carregamento} decoding="async"></picture>'
            f'<figcaption>{esc(peca.get("legenda", ""))} <span class="aviso-ia">{AVISO_IA}</span></figcaption>'
            + expansao(peca["citacoes"], prefixo) + "</figure>")
# O rótulo de cada bloco didático é a pergunta própria que vem no cabeçalho do bloco, em conteudo/percurso.md e em
# conteudo/camada-externa.md. Os rótulos abaixo são só reserva para bloco novo sem pergunta. Revisão de rótulos de 05/11/2026.
ROTULOS_PERCURSO = {"imagem": "Como imaginar isso?", "mecanismo": "Como isso funciona?", "caso": "Como isso aparece na prática?",
                    "nome": "", "limite": "Quais são os limites?", "teste": "Como saber se é o seu caso?",
                    "importa": "Por que isso importa?"}
# O termo emprestado de outro campo leva uma linha só, com o nome da área de onde vem, na cor dela. A linha é também o link
# para as outras palavras da mesma área. Revisão de rótulos de 05/11/2026.

# Cores e áreas. A proposta está em estrutura/cores.json e foi aprovada pelo autor em 27/10/2026.
CORES = json.loads((RAIZ / "estrutura" / "cores.json").read_text(encoding="utf-8"))
AREA_NOME = {k: a["nome"] for k, a in CORES["areas"].items()}
# Os dez conceitos que a tese deriva, fora dos nove. Ganharam estatuto próprio ao lado dos nove, por decisão do autor de 27/10/2026.
DERIVADOS = {"Teleologia arquitetural", "Cativeiro identitário", "Consumidor-cidadão", "Transparência performática",
             "Consentimento viciado por sentido", "Publicidade enganosa por arquitetura", "Continuidade biográfica",
             "Recomposição funcional", "Correção de regime", "Dano-arquitetura"}
FICHA_DERIVADO = {"Recomposição funcional": "recomposicao-funcional", "Correção de regime": "recomposicao-funcional"}


def slug_derivado(nome):
    return re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", nome.lower()).encode("ascii", "ignore").decode()).strip("-")


def caminho_derivado(nome):
    """A página de um conceito derivado. Os que já têm ficha apontam para ela."""
    return f'conceitos/{FICHA_DERIVADO.get(nome) or slug_derivado(nome)}/'


# A área de cada termo do percurso, pela seção da tese de onde vem o trecho e pelo lugar do autor decidido em 27/10/2026.
# As categorias jurídicas ficam no Direito. Os derivados são da tese. Nerf é palavra do próprio objeto.
AREA_TERMO = {
    "Valor como julgamento": "antropologia", "Consumo como ritual": "antropologia", "Transferência de significado": "antropologia",
    "Biografia das coisas": "antropologia",
    "Espetáculo": "semiotica", "Gamificação": "semiotica", "Simulacro": "semiotica", "Códigos de leitura": "semiotica",
    "Economia da atenção": "economia", "Tecnofeudalismo": "economia", "Economia de pedágio": "economia", "Trabalho invisível": "economia",
    "Lumpemproletariado digital": "economia", "Propriedade intelectual como cerca": "economia",
    "Arquitetura de escolha": "poder", "Psicopolítica": "poder", "Cidadania digital": "poder",
    "Autonomia da técnica": "tecnica", "Mídia como forma de vida": "tecnica", "Dessimbolização": "tecnica", "Código técnico": "tecnica",
    "Poder informacional": "direito", "Normatividade prática": "direito", "Categorias que acompanham a técnica": "direito",
    "Bens digitais": "direito", "Contratos cativos": "direito", "Padrões obscuros": "direito", "Vulnerabilidade do consumidor": "direito",
    "Lei do software": "direito", "Ordem econômica": "direito", "Eficácia horizontal dos direitos fundamentais": "direito",
    "Função social da propriedade intelectual": "direito", "Marco legal dos jogos": "direito", "Consumidor equiparado": "direito",
    "Concorrência": "direito", "Nerf": "laboratorio",
}


def estilo_area(area):
    return f' style="--area:var(--a-{area});--area-t:var(--a-{area}-t)"' if area else ""


def partes_com_ideia(cid):
    """As partes do percurso em que uma das nove ideias aparece com nome próprio."""
    return [(i, parte) for i, parte in enumerate(PERCURSO, 1)
            if any(b["tipo"] == "nome" and b["arg"] == cid for b in parte["blocos"])]


# A troca de voz. Todo trecho literal que aparece debaixo de um bloco na voz do site vem anunciado pelo mesmo rótulo,
# e o texto literal corrido das páginas de leitura, pelo seu. Auditoria de estrutura de 04/11/2026.
ROTULO_FONTE = '<p class="rotulo-fonte">De onde vem</p>'
# O nome da seção dos nove conceitos, pela p. 30, que pede um vocabulário capaz de tornar nomeáveis as decisões escondidas na
# técnica, e pelo trecho da página inicial sobre deslocar o poder para um regime de contestabilidade. Revisão de rótulos de 05/11/2026.
TITULO_VOCABULARIO = "Um vocabulário para contestar"
ROTULO_LITERAL = '<p class="rotulo-fonte">Em texto literal</p>'


def titulo_site(titulo):
    """O título de uma seção da tese na voz do site, para a Informação e a Doutrina. Sai a contração inicial do título
    acadêmico, e Lex Plataformae vira lei da plataforma, como decidiu o autor em 27/10/2026."""
    t = re.sub(r"^(?:D[oa]s?|Em)\s+", "", titulo.strip())
    t = t.replace("Lex Plataformae", "lei da plataforma")
    return t[:1].upper() + t[1:]


def titulo_por_modo(titulo):
    """O título no modo de cada leitor. O da tese fica na Ciência."""
    proprio = titulo_site(titulo)
    if proprio == titulo:
        return esc(titulo)
    return f'<span class="em-modo modo-0 modo-1">{esc(proprio)}</span><span class="em-modo modo-2">{esc(titulo)}</span>'


def saidas_html(itens, titulo="Para onde seguir?"):
    """O fim de cada página aponta para onde se resolve o que ela não responde."""
    if not itens:
        return ""
    return (f'<nav class="ext saidas" aria-label="{esc(titulo)}"><p class="rotulo-ext">{esc(titulo)}</p><ul class="partes-curtas">'
            + "".join(f'<li><a href="{href}">{esc(rotulo)}</a></li>' for rotulo, href in itens) + "</ul></nav>")


def expansao(cits, prefixo, modo="ciencia"):
    """Os trechos literais que um bloco simples condensa. Ficam à vista só na Ciência, pela revisão de voz de 05/11/2026."""
    if not cits:
        return ""
    return (f'<div class="{modo} expansao" data-arq="trechos literais · cada um com a página">{ROTULO_FONTE}'
            + "".join(f'<blockquote class="citacao"><p>{esc(q["texto"])}{pg(q["ref"], prefixo, q["texto"])}</p></blockquote>' for q in cits)
            + "</div>")


def ext_texto(pag, campo_):
    b = EXTERNA.get(pag, {}).get(campo_)
    return " ".join(b["paragrafos"]) if b else ""


def ext_html(pag, campo_, prefixo, classe=""):
    b = EXTERNA.get(pag, {}).get(campo_)
    if not b:
        return ""
    atributo = f' class="{classe}"' if classe else ""
    return "".join(f"<p{atributo}>{esc(t)}</p>" for t in b["paragrafos"]) + expansao(b["citacoes"], prefixo)


def botao_desnudar(doutrina=False):
    """O convite dentro da página leva ao modo seguinte que muda algo nela. Do último, volta à Informação.

    Percurso, problemas e direitos têm o mesmo texto na Doutrina, por isso o convite vai direto à Ciência, onde estão os trechos.
    """
    primeiro = ('<label class="botao convite-botao so-0" for="nivel-1" title="Abre o modo Doutrina">Ver a ficha para operar</label>' if doutrina
                else '<label class="botao convite-botao so-0" for="nivel-2" title="Abre o modo Ciência">Ver de onde vem</label>')
    return ('<span class="convite-botoes">' + primeiro +
            '<label class="botao convite-botao so-1" for="nivel-2" title="Abre o modo Ciência">Ver de onde vem</label>'
            '<label class="botao convite-botao so-2" for="nivel-0" title="Volta ao modo Informação">Voltar ao texto simples</label></span>')


def html_passo(passo, base):
    c = POR_ID.get(passo["id"])
    extra = D["passos"].get(passo["id"])

    def link(cid, nome):
        return f'<a href="{base}{cid}/">{esc(nome)}</a>'

    if c and c["tipo"] == "conceito":
        nome = link(c["id"], c["nome"])
        if passo.get("par") and passo["par"] in POR_ID:
            dica = "Formulação do autor, acréscimo posterior de 05/11/2026. O resumo da tese propõe o OIC enquanto feixe de fruição governada (p. 11)" if passo["id"] == "oic" else "A tese formula a teleologia abusiva como categoria de ilícito de arquitetura (p. 794)"
            nome = (f'<span class="gemeos">{link(c["id"], c["nome"])}<span class="gemeos-sinal" title="{esc(dica)}">'
                    f'{esc(passo["par_rotulo"])}</span>{link(passo["par"], POR_ID[passo["par"]]["nome"])}</span>')
        corpo, classe, arq = f'<span class="passo-nome">{nome}</span>', "passo", ""
    elif c and c["tipo"] == "roteiro":
        corpo = (f'<span class="passo-tipo">fora dos nove · enunciado dos Parâmetros · {esc(c["secao"])}</span>'
                 f'<span class="passo-nome">{link(c["id"], c["nome"])}</span>')
        classe, arq = "passo fantasma", ' data-arq="fora dos nove · segue como enunciado dos Parâmetros"'
    elif c and c["tipo"] == "bens":
        corpo = f'<span class="passo-tipo">bens protegidos · 5.1.4 e 6.1.3</span><span class="passo-nome">{link(c["id"], c["nome"])}</span>'
        classe, arq = "passo fantasma", ' data-arq="fora dos nove · camada de bens protegidos"'
    else:
        corpo = f'<span class="passo-tipo">enunciado dos Parâmetros · {esc(extra["secao"])}</span><span class="passo-nome">{esc(extra["nome"])}</span>'
        classe, arq = "passo fantasma", ' data-arq="fora dos nove · enunciado dos Parâmetros"'
    corpo += f'<span class="passo-papel">{esc(passo["papel"])}</span>'
    return f'<li class="{classe}" data-chave="{esc(passo["id"])}"{arq}><span class="passo-corpo">{corpo}</span></li>'


def mapa_percurso(base, contexto):
    """A lista das partes do percurso, com a pergunta e o resumo de cada uma."""
    if not PERCURSO:
        return ""
    itens = "".join(
        f'<li><a href="{base}{parte["slug"]}/"><span class="parte-num">{i}</span>'
        f'<span class="parte-titulo">{esc(parte["titulo"])}</span><span class="parte-resumo">{esc(parte["resumo"])}</span></a></li>'
        for i, parte in enumerate(PERCURSO, 1))
    cabeca = (f'<h2 class="campo-titulo" id="percurso-titulo">Siga a skin</h2>' if contexto == "inicio"
              else f'<h1 class="chamada" id="percurso-titulo">Siga a skin</h1>')
    return (f'<section class="secao percurso-mapa" id="percurso" aria-labelledby="percurso-titulo">'
            f'<div class="percurso-mapa-lado">{cabeca}'
            f'<div class="campo-texto">{ext_html("inicio", "percurso", "")}</div>'
            f'<p class="percurso-comecar"><a class="botao" href="{base}{PERCURSO[0]["slug"]}/">Começar pela compra</a></p></div>'
            f'<ol class="partes">{itens}</ol></section>')


ROTULO_NO_PERCURSO = "Onde o caminho conta mais?"


def no_percurso(cid, prefixo):
    achados = partes_com_ideia(cid)
    if not achados:
        return ""
    return (f'<section class="ext no-percurso"><p class="rotulo-ext">{ROTULO_NO_PERCURSO}</p><ul class="partes-curtas">'
            + "".join(f'<li><a href="{prefixo}caminho/{parte["slug"]}/"><span class="parte-num">{i}</span>{esc(parte["titulo"])}</a></li>'
                      for i, parte in achados)
            + "</ul></section>")


def bloco_percurso(b, prefixo):
    tipo, arg = b["tipo"], b["arg"]
    texto = "".join(f"<p>{esc(t)}</p>" for t in b["paragrafos"])
    exp = expansao(b["citacoes"], prefixo)
    # Nos blocos didáticos, o argumento do cabeçalho é a pergunta própria do bloco.
    rotulo = (arg if tipo in ("imagem", "mecanismo", "caso", "teste", "limite") and arg else ROTULOS_PERCURSO.get(tipo))
    if tipo == "nome":
        # O nome em destaque é o próprio link para a ideia inteira.
        c = POR_ID[arg]
        return (f'<section class="ext nome-ext"><h2 class="nome-conceito">'
                f'<a href="{prefixo}conceitos/{arg}/" title="A ficha do conceito">{nome_html(c)}</a></h2>{texto}{exp}</section>')
    if tipo == "termo":
        derivado = arg in DERIVADOS
        area = AREA_TERMO.get(arg)
        ident = f' id="termo-{slug_derivado(arg)}"'
        if derivado:
            # O derivado é nome que a teoria cunha. Na Doutrina, o nome leva à página dele.
            nome = (f'<span class="nome-derivado em-modo modo-0">{esc(arg)}</span>'
                    f'<a class="em-modo modo-1 modo-2" href="{prefixo}{caminho_derivado(arg)}" title="A página do conceito"><span class="nome-derivado">{esc(arg)}</span></a>')
            linha = ""
        else:
            nome = esc(arg)
            linha = (f'<a class="area-rotulo" href="{prefixo}instrumentos/#{area}" title="Outras palavras da mesma área">{esc(AREA_NOME[area])}</a>' if area else "")
        # Termo de outro campo do conhecimento. Na Informação e na Doutrina o bloco é só a explicação do fenômeno, sem título,
        # e o nome teórico com a área fica na Ciência. Adequação das camadas, etapa 5, 08/11/2026.
        if area and area != "direito" and not derivado:
            return (f'<section class="ext termo-fenomeno"{ident}{estilo_area(area)}><h2 class="nome-termo ciencia">{linha}{nome}</h2>'
                    f'{texto}{exp}</section>')
        return (f'<section class="ext termo{" derivado" if derivado else ""}"{ident}{estilo_area(area)}><h2 class="nome-termo">{linha}{nome}</h2>'
                f'{texto}{exp}</section>')
    if tipo == "familia":
        titulo = ext_texto(arg, "titulo") or arg
        return (f'<section class="ext termo familia"><h2 class="nome-termo">'
                f'<a href="{prefixo}plataformas/{arg}/">{esc(titulo)}</a></h2>{texto}{exp}</section>')
    if tipo == "ilustracao":
        return figura(arg, prefixo)
    if tipo in ("imagem", "mecanismo", "caso", "teste"):
        return f'<section class="ext didatico {tipo}"><p class="rotulo-ext">{esc(rotulo)}</p>{texto}{exp}</section>'
    if tipo == "limite":
        return f'<section class="ext limite"><p class="rotulo-ext">{esc(rotulo)}</p>{texto}{exp}</section>'
    return f'<section class="ext">{texto}{exp}</section>'


def gerar_percurso():
    total = len(PERCURSO)
    raiz = SAIDA / "caminho"
    raiz.mkdir(parents=True, exist_ok=True)
    corpo = f'<article class="folha percurso-indice">{mapa_percurso("", "indice")}</article>'
    (raiz / "index.html").write_text(
        pagina("Siga a skin, da compra ao que a lei pode fazer · Lex Plataformae", "Você comprou uma skin. Ela é sua? Onze perguntas, do clique de compra ao que a lei pode fazer.",
               corpo, "../", "caminho/", camada="mista", imagem="inicio"), encoding="utf-8")
    prefixo = "../../"
    for i, parte in enumerate(PERCURSO, 1):
        anterior = PERCURSO[i - 2] if i > 1 else None
        seguinte = PERCURSO[i] if i < total else None
        if seguinte:
            avancar = f'<a class="botao" href="../{seguinte["slug"]}/">Seguir para a parte {i + 1}</a>'
        else:
            avancar = f'<a class="botao" href="{prefixo}conceitos/">Ver o vocabulário inteiro</a>'
        vizinhos = ('<nav class="vizinhos" aria-label="Partes do caminho">'
                    + (f'<a href="../{anterior["slug"]}/">← {esc(anterior["titulo"])}</a>' if anterior else f'<a href="{prefixo}">← Início</a>')
                    + (f'<a href="../{seguinte["slug"]}/">{esc(seguinte["titulo"])} →</a>' if seguinte else "")
                    + "</nav>")
        corpo = (f'<article class="folha percurso-parte">'
                 f'<p class="sobrelinha-ext"><a href="{prefixo}caminho/">Caminho</a> · Parte {i} de {total}</p>'
                 f'<header class="folha-cabeca ext-cabeca"><h1>{esc(parte["titulo"])}</h1></header>'
                 + figura(f'parte-{parte["slug"]}', prefixo)
                 + "".join(bloco_percurso(b, prefixo) for b in parte["blocos"])
                 + secao_direitos(direitos_da_parte(parte["slug"]), prefixo)
                 + FERMATA + f'<section class="ext duvida"><p class="pergunta-final">{esc(parte["pergunta"])}</p>'
                 f'<div class="acoes">{avancar}{botao_desnudar()}</div></section>'
                 + vizinhos + "</article>")
        jsonld = {"@context": "https://schema.org", "@type": "Article", "headline": parte["titulo"], "inLanguage": "pt-BR",
                  "url": f'{BASE}/caminho/{parte["slug"]}/', "isBasedOn": BASE + "/#tese",
                  "author": {"@type": "Person", "name": "Victor Luiz Pereira de Andrade"}}
        destino = raiz / parte["slug"]
        destino.mkdir(parents=True, exist_ok=True)
        (destino / "index.html").write_text(
            pagina(f'{parte["titulo"]} · Siga a skin · Lex Plataformae', f'{parte["resumo"]} Parte {i} de {total} do caminho da skin.',
                   corpo, prefixo, f'caminho/{parte["slug"]}/', jsonld, camada="mista", imagem=f'percurso-{parte["slug"]}',
                   irmas=("O caminho", [(f'<span class="parte-num">{j}</span>{esc(x["titulo"])}', f'../{x["slug"]}/', x is parte) for j, x in enumerate(PERCURSO, 1)])),
            encoding="utf-8")


def gerar_inicio():
    padrao = "regime"
    oic_def = canonica(EIXO)
    integra = campo(EIXO, "Como integra os demais")
    gatilho = next((q for q in integra["citacoes"] if q["ref"] == "p. 719"), None) if integra else None
    gemeo = POR_ID[EIXO["par"]["id"]] if EIXO.get("par") else None
    independentes = em_ordem([c for c in conceitos_do_atlas() if c is not EIXO and not (gemeo and c is gemeo)])
    base = "conceitos/"

    opcoes = "".join(
        f'<input type="radio" name="percurso" id="percurso-{k}" value="{k}"{" checked" if k == padrao else ""}>'
        f'<label for="percurso-{k}"><b>{esc(p["nome"])}</b><span>{esc(p["onde"])} · {esc(p["fonte"])}</span></label>'
        for k, p in D["percursos"].items()
    )
    p = D["percursos"][padrao]
    passos = "".join(html_passo(s, base) for s in p["sequencia"])
    presentes = {s["id"] for s in p["sequencia"]} | {s["par"] for s in p["sequencia"] if s.get("par")}
    ordem_atlas = [c["id"] for c in em_ordem(conceitos_do_atlas())]
    ausentes = [cid for cid in ordem_atlas if cid not in presentes]
    fora = ("<p>Fora desta leitura</p><ul>" + "".join(f'<li><a href="{base}{cid}/">{esc(POR_ID[cid]["nome"])}</a></li>' for cid in ausentes) + "</ul>") if ausentes else ""

    dados_leituras = {
        "padrao": padrao,
        "percursos": D["percursos"],
        "passos": D["passos"],
        "ordem": ordem_atlas,
        "conceitos": {c["id"]: {"nome": c["nome"], "tipo": c["tipo"], "secao": c.get("secao")} for c in D["conceitos"]},
        "paginas": {str(k): v for k, v in PAG2SLUG.items()},
        "alvos": {k: destino_pagina(p["trecho"]["ref"], "", p["trecho"]["texto"]) for k, p in D["percursos"].items()},
    }

    ep = D["epigrafes"]
    musas = "".join(
        f'<li><div>{esc(e["artista"])}, <cite>{esc(e["faixa"])}</cite> ({e["ano"]})<small>abre {esc(e["abre"])}</small></div></li>'
        for e in ep["epigrafes"]
    )
    ab = D["abertura"]

    cart = EXTERNA.get("cartoes", {})

    def cartao(c, classe=""):
        bloco = cart.get(c["id"], {})
        frase = bloco.get("paragrafos", [""])[0] if bloco.get("paragrafos") else ""
        return (f'<li><a class="cartao cartao-ideia{classe}" href="{base}{c["id"]}/"><span class="cartao-frase">{esc(frase)}</span>'
                f'<b>{nome_html(c)}</b></a></li>')

    eixo_cartoes = cartao(EIXO, " cartao-eixo") + (cartao(gemeo, " cartao-eixo") if gemeo else "")
    cartoes = "".join(cartao(c) for c in independentes)
    # Os trechos de cada cartão saem de baixo dele e formam um bloco só, depois da grade, com o nome à frente de cada um.
    # O cartão do OIC dispensa trecho, porque a definição literal aparece logo abaixo dele. Revisão de rótulos de 05/11/2026.
    itens_fonte = "".join(
        f'<p class="fonte-nome">{nome_html(c)}</p>'
        + "".join(f'<blockquote class="citacao"><p>{esc(q["texto"])}{pg(q["ref"], "", q["texto"])}</p></blockquote>' for q in cart.get(c["id"], {}).get("citacoes", []))
        for c in ([gemeo] if gemeo else []) + independentes if cart.get(c["id"], {}).get("citacoes"))
    fontes_grade = (f'<div class="ciencia expansao expansao-nomeada" data-arq="trechos literais · um grupo por nome">'
                    f'<p class="rotulo-fonte">De onde vem cada nome</p>{itens_fonte}</div>') if itens_fonte else ""

    # A entrada pelo que aconteceu com a pessoa, na Informação, e pelo curso, na Doutrina. Adequação das camadas, etapa 6, 09/11/2026.
    entrada_inicio = (
        (f'<section class="campo entrada-problemas em-modo modo-0" aria-labelledby="entrada-titulo"><h2 class="campo-titulo" id="entrada-titulo">O que aconteceu com você?</h2>'
         f'{lista_problemas(list(PROBLEMAS), "", "partes-curtas lista-duas")}'
         + (f'<p class="ver-reclamar"><a href="como-reclamar/">{esc(COMO_RECLAMAR["titulo"])}</a></p>' if COMO_RECLAMAR else "")
         + '</section>' if PROBLEMAS else "")
        + (f'<section class="campo entrada-curso em-modo modo-1 modo-2" aria-labelledby="entrada-curso-titulo"><h2 class="campo-titulo" id="entrada-curso-titulo">O regime, em curso</h2>'
           f'<ol class="partes-curtas lista-duas">' + "".join(f'<li><a href="doutrina/{c["slug"]}/">{esc(c["titulo"])}</a></li>' for c in CURSO) + '</ol></section>' if CURSO else ""))
    # Capa narrativa, decisão do autor de 10/11/2026. A história desce em quatro telas e termina em três portas.
    # Na Doutrina a história some e a capa abre nas portas. O vocabulário completo mora em conceitos/.
    def cena(campo_, classe=""):
        return (f'<section class="cena {classe} em-modo modo-0 modo-2">{ext_html("inicio", campo_, "")}</section>')
    destaques = ["conta-bloqueada", "item-alterado", "servico-piorou", "jogo-encerrado", "crianca"]
    destaques = [d for d in destaques if d in PROBLEMAS]
    nomes_discretos = " · ".join(f'<a href="conceitos/{c["id"]}/">{nome_html(c)}</a>' for c in [EIXO] + ([gemeo] if gemeo else []) + independentes)
    corpo = f"""
    <section class="cena cena-titulo" aria-labelledby="titulo">
      <h1 class="chamada" id="titulo">{"".join(f'<span class="chamada-linha">{esc(f)}</span> ' for f in re.split(r"(?<=[.!?])\s+", ext_texto("inicio", "chamada"))).strip()}</h1>
      <nav class="atalhos-capa" aria-label="Escolha seu caminho">
        <a href="problemas/">Encontrar meu problema</a>
        <a href="#portas-titulo">Explorar os caminhos</a>
        <a href="metodo/" data-modo="2">Pesquisar as fontes</a>
      </nav>
    </section>
    {figura("inicio", "", destaque=True)}
    {cena("cena-compra")}
    {cena("cena-mudanca", "cena-incomodo")}
    {cena("cena-virada", "cena-virada")}

    <section class="portas" aria-labelledby="portas-titulo">
      <div class="portas-texto em-modo modo-0 modo-2">{ext_html("inicio", "portas", "")}</div>
      <h2 class="portas-titulo" id="portas-titulo" tabindex="-1">Por onde seguir</h2>
      <div class="portas-grade">
        <article class="porta porta-problema item-moldura">
          <p class="porta-rotulo">Aconteceu comigo</p>
          <h3><a href="problemas/">O que aconteceu com você?</a></h3>
          {lista_problemas(destaques, "", "partes-curtas")}
          <p class="porta-mais"><a href="problemas/">Todos os problemas</a>{f' · <a href="como-reclamar/">{esc(COMO_RECLAMAR["titulo"])}</a>' if COMO_RECLAMAR else ""}</p>
        </article>
        <article class="porta porta-percurso item-moldura">
          <p class="porta-rotulo">Quero entender</p>
          <h3><a href="caminho/o-desejo/">Siga a skin</a></h3>
          <p>{esc(ext_texto("inicio", "percurso"))}</p>
          <p class="porta-mais"><a href="caminho/o-desejo/">Continuar a história</a> · <a href="caminho/">As onze partes</a></p>
        </article>
        <article class="porta porta-direito item-moldura">
          <p class="porta-rotulo">Trabalho com Direito</p>
          <h3><a href="doutrina/" data-modo="1">O caminho do jurista</a></h3>
          <p>Os mesmos problemas, tratados como doutrina, com as situações para operar e a legislação.</p>
          <p class="porta-mais"><a href="doutrina/" data-modo="1">Abrir em Doutrina</a> · <a href="roteiro/" data-modo="1">As situações</a></p>
        </article>
      </div>
    </section>

    <section class="nomes-discretos" aria-labelledby="nomes-titulo">
      <h2 id="nomes-titulo">Isso tem nome</h2>
      <p>{nomes_discretos}</p>
      <p class="porta-mais"><a href="conceitos/">Todo o vocabulário</a></p>
    </section>

    <div class="inicio-fecho">
    <section class="convite" aria-label="Desnudar a arquitetura">
      {ext_html("inicio", "convite", "")}
      {botao_desnudar()}
    </section>

    <section class="secao ciencia" id="epigrafes" aria-labelledby="epigrafes-titulo">
      <h2 id="epigrafes-titulo">Epígrafes musicais</h2>
      {ext_html("inicio", "trilha", "")}
      <p><a class="botao" href="epigrafes/">{esc(ext_texto("epigrafes", "titulo") or "As nove canções")}</a></p>
    </section>
    </div>
"""
    termos = [{
        "@type": "DefinedTerm",
        "@id": url_conceito(c["id"]),
        "name": c["nome"],
        "description": canonica(c)["texto"],
        "url": url_conceito(c["id"]),
        "inDefinedTermSet": BASE + "/#atlas",
    } for c in conceitos_do_atlas()]
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Thesis",
                "@id": BASE + "/#tese",
                "name": TITULO_TESE,
                "author": {"@type": "Person", "name": "Victor Luiz Pereira de Andrade", "alternateName": "Victor L. P. Andrade"},
                "datePublished": "2026",
                "inSupportOf": "Doutorado em Direito",
                "sourceOrganization": {"@type": "CollegeOrUniversity", "name": "Universidade Estadual Paulista (UNESP)"},
                "inLanguage": "pt-BR",
                "url": f"{BASE}/tese/{PDF_NOME}",
                "keywords": ["objeto imaterial de consumo", "feixe de fruição governada", "vulnerabilidade semiótica",
                             "Lex Plataformae", "ordem constitucional e econômica", "direito do consumidor",
                             "função social da propriedade intelectual"],
            },
            {"@type": "DefinedTermSet", "@id": BASE + "/#atlas", "name": "Atlas Lex Plataformae",
             "inLanguage": "pt-BR", "isBasedOn": BASE + "/#tese", "hasDefinedTerm": termos},
        ],
    }
    desc = "Você comprou uma skin. Ela é sua? Um caminho pelo que acontece com o que se compra no mundo digital, e nove conceitos para contestar isso."
    corpo = f'<div class="pagina-inicio">{corpo}</div>'
    (SAIDA / "index.html").write_text(pagina("Lex Plataformae · Você comprou uma skin. Ela é sua?", desc, corpo, "", "", jsonld, camada="mista"), encoding="utf-8")

    # A página do vocabulário, em conceitos/. Antes era a seção #conceitos da capa. Decisão do autor de 10/11/2026.
    pre, base_v = "../", ""
    eixo_c = "".join(x.replace('href="conceitos/', 'href="') for x in [eixo_cartoes])
    cartoes_c = cartoes.replace('href="conceitos/', 'href="')
    fontes_c = fontes_grade.replace('href="tese/', 'href="../tese/')
    passos_v = "".join(html_passo(s_, base_v) for s_ in p["sequencia"])
    fora_v = fora.replace('href="conceitos/', 'href="')
    dados_v = dict(dados_leituras, alvos={k: destino_pagina(pp["trecho"]["ref"], pre, pp["trecho"]["texto"]) for k, pp in D["percursos"].items()})
    corpo_v = f"""<div class="pagina-vocabulario">
    <section class="campo" id="conceitos" aria-labelledby="conceitos-titulo">
      <h1 class="campo-titulo" id="conceitos-titulo">{TITULO_VOCABULARIO}</h1>
      <div class="campo-texto">{ext_html("inicio", "nome", pre)}</div>
      <ul class="eixo-cartoes" data-arq="eixo · o OIC organiza juridicamente o feixe de fruição governada">{eixo_c}</ul>
      <div class="campo-topo ciencia" data-arq="integração · conceitos independentes que funcionam integrados sob o OIC">
        {ROTULO_FONTE}<blockquote class="citacao"><p>{esc(oic_def["texto"])}{pg(oic_def["ref"], pre, oic_def["texto"])}</p></blockquote>
        {f'<blockquote class="citacao integra"><p>{esc(gatilho["texto"])}{pg(gatilho["ref"], pre, gatilho["texto"])}</p></blockquote>' if gatilho else ""}
      </div>
      <div class="campo-texto">{ext_html("inicio", "mapa", pre)}</div>
      <ul class="grade-conceitos" data-arq="conceitos independentes · sem ordem nem hierarquia">{cartoes_c}</ul>
      {fontes_c}
      <p class="ver-ideia"><a href="{pre}instrumentos/">Conceitos que vêm de outros campos</a></p>
    </section>

    <section class="secao leituras ciencia" aria-labelledby="leituras-titulo">
      <h2 id="leituras-titulo">Três leituras do texto integral</h2>
      <p>O texto integral também percorre os conceitos em três ordens. São leituras do texto, não hierarquia entre os conceitos.</p>
      <p class="nota-par">Acréscimo posterior de 05/11/2026. A etiqueta “organiza juridicamente o” é formulação do autor. O resumo da tese diz “enquanto feixe de fruição governada” (p. 11).</p>
      <fieldset class="percursos">
        <legend>Escolha uma leitura</legend>
        <div class="seletor">{opcoes}</div>
        <p class="logica" id="logica" aria-live="polite">{esc(p["logica"])} <q>{esc(p["trecho"]["texto"])}</q>{pg(p["trecho"]["ref"], pre, p["trecho"]["texto"])}</p>
      </fieldset>
      <ul class="sequencia" id="sequencia" data-base="{base_v}" aria-label="{esc(p["nome"])}" data-arq="leitura · ordem do texto, não hierarquia">{passos_v}</ul>
      <div class="fora" id="fora">{fora_v}</div>
      <script type="application/json" id="leituras-dados">{json.dumps(dados_v, ensure_ascii=False).replace("</", "<\\/")}</script>
    </section>

    </div>"""
    (SAIDA / "conceitos").mkdir(parents=True, exist_ok=True)
    (SAIDA / "conceitos" / "index.html").write_text(
        pagina("Vocabulário para contestar o consumo digital · Lex Plataformae",
               "Os nove nomes que respondem, cada um, por uma parte do que acontece com o que se compra no mundo digital.",
               corpo_v, pre, "conceitos/", {}, camada="mista"), encoding="utf-8")


def gerar_conceito(c):
    prefixo = "../../"
    base = "../"
    if c["tipo"] == "roteiro":
        sobre = f'Fora dos nove · enunciado dos Parâmetros · {c["secao"]}'
    elif c["tipo"] == "bens":
        sobre = "Bens protegidos · fora dos nove"
    else:
        sobre = "Conceito · eixo de integração dos demais" if c.get("eixo") else "Conceito"
    selos = f'<span class="selo" data-arq="versão · o conteúdo segue em revisão pelo autor">Versão {VERSAO}</span>'
    if c.get("par"):
        rot = "Em par com "
        selos += f'<a class="selo gemeo" href="{base}{c["par"]["id"]}/">{rot}{nome_html(POR_ID[c["par"]["id"]])}</a>'

    partes = []
    ja_na_doutrina = trechos_da_doutrina(f'conceito {c["id"]}')
    for f in c["campos"]:
        r = f["rotulo"]
        f = dict(f, citacoes=[q for q in f.get("citacoes", []) if not any(q["texto"] in trecho for trecho in ja_na_doutrina)])
        if not f["citacoes"] and not f.get("texto") and r != "Onde vive":
            continue
        if r == "Onde vive":
            itens = re.split(r",\s*(?![^()]*\))", f["texto"].rstrip("."))
            lis = []
            for i in itens:
                sec = secao_de_lugar(i.strip())
                rotulo = esc(i.strip())
                lis.append(f'<li><a href="{prefixo}tese/{sec["slug"]}/">{rotulo}</a></li>' if sec else f"<li>{rotulo}</li>")
            partes.append('<section class="bloco ciencia"><h2>Onde vive na tese</h2><ul class="lugares" data-arq="âncora · seções da tese, com link para o texto">'
                          + "".join(lis) + "</ul></section>")
            continue
        if r == "Nota do autor":
            partes.append('<section class="nota-autor" data-arq="acréscimo posterior · fora do texto da tese de 2026">'
                          f'<p class="sobrelinha">Nota do autor</p><p>{esc(f["texto"])}</p></section>')
            continue
        # Notas sobre a estrutura da tese e sobre decisões do site ficam na Ciência. A Doutrina não fica referenciando a tese.
        meta_inteiro = r in CAMPOS_SO_CIENCIA or (f["texto"] or "").startswith("Pendência")
        if r in CAMPOS_SO_CIENCIA or (meta_inteiro and not f["citacoes"]):
            bloco = f'<section class="bloco ciencia"><h2>{esc(r)}</h2>'
        else:
            rotulo_h = re.sub(r"\s+(d[oa]s?\s+\d+(?:\.\d+)+)$", r'<span class="ciencia"> \1</span>', esc(r))
            if r in ROTULO_FICHA:
                rotulo_h = f'<span class="em-modo modo-1">{esc(ROTULO_FICHA[r])}</span><span class="em-modo modo-0 modo-2">{esc(r)}</span>'
            bloco = f'<section class="bloco"><h2>{rotulo_h}</h2>'
        if f["texto"]:
            if meta_inteiro:
                bloco += f'<p class="ciencia">{com_ancoras(f["texto"], prefixo)}</p>'
            else:
                bloco += "<p>" + " ".join(
                    f'<span class="ciencia">{com_ancoras(fr, prefixo)}</span>' if PADRAO_META.search(fr) else com_ancoras(fr, prefixo)
                    for fr in re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚ"“])', f["texto"])) + "</p>"
        for q in f["citacoes"]:
            if r == "Definição canônica proposta":
                bloco += ('<blockquote class="canonica" data-arq="citação literal · definição proposta">'
                          f'<p><mark>{esc(q["texto"])}</mark>{pg(q["ref"], prefixo, q["texto"])}</p></blockquote>')
            else:
                classe = "citacao nao-e" if r == "O que não é" else "citacao"
                bloco += f'<blockquote class="{classe}"><p>{esc(q["texto"])}{pg(q["ref"], prefixo, q["texto"])}</p></blockquote>'
        partes.append(bloco + "</section>")

    linhas = []
    for p in D["percursos"].values():
        for s in p["sequencia"]:
            if s["id"] == c["id"] or s.get("par") == c["id"]:
                linhas.append(f'<li><b>{esc(p["nome"])}</b><span>{esc(s["papel"])}</span></li>')
    if linhas:
        partes.append('<section class="bloco ciencia"><h2>Nas leituras da tese</h2><ul class="nos-percursos">' + "".join(linhas) + "</ul></section>")
    elif c["tipo"] == "conceito":
        partes.append('<section class="bloco ciencia"><h2>Nas leituras da tese</h2><p>Não aparece em nenhuma das três sequências da tese.</p></section>')

    letras = [l for l, (_, ids) in ROTEIRO_MAPA.items() if c["id"] in ids]
    nomes = nomeacoes().get(c["id"], {})
    itens_rot = [f'<li><a href="{prefixo}roteiro/#{l}">{esc(SITUACOES.get(l, "Bloco " + l))}</a></li>' for l in letras] if POR_NUMERO.get("7.1.2") else []
    itens_rot += [f'<li><a href="{prefixo}{caminho}">{esc(rotulo)}</a> <span class="vezes">{esc(det)}</span></li>' for rotulo, caminho, det in nomes.get("Roteiro", [])]
    nas_situacoes = ""
    if itens_rot:
        nas_situacoes = ('<section class="bloco nas-situacoes"><h2>Nas situações</h2>'
                      + ('<p class="nota-camada ciencia">Os blocos seguem o enunciado do 7.1.1 a que cada um corresponde. As demais situações também operam com o conceito.</p>' if nomes.get("Roteiro") and letras else "")
                      + '<ul class="lugares">' + "".join(itens_rot) + "</ul></section>")
    if nomes.get("Laboratório"):
        partes.append('<section class="bloco ciencia"><h2>Nas plataformas</h2><p class="nota-camada">As famílias de plataforma em que o conceito opera.</p><ul class="lugares">'
                      + "".join(f'<li><a href="{prefixo}{caminho}">{esc(rotulo)}</a> <span class="vezes">{esc(det)}</span></li>' for rotulo, caminho, det in nomes["Laboratório"])
                      + "</ul></section>")

    outros_nav = ""
    if c["tipo"] == "conceito":
        outros = em_ordem([x for x in conceitos_do_atlas() if x is not c and not x.get("eixo")])
        lista = ([] if c.get("eixo") else [EIXO]) + outros
        outros_nav = (f'<nav class="outros" aria-label="Os outros {ORDINAIS_N[len(lista)]} nomes"><h2>Os outros {ORDINAIS_N[len(lista)]} nomes</h2><ul>'
                      + "".join(f'<li><a href="{base}{x["id"]}/">{nome_html(x)}</a></li>' for x in lista) + "</ul></nav>")

    e = EXTERNA.get(c["id"]) if c["tipo"] == "conceito" else None
    can = canonica(c)
    jsonld = {"@context": "https://schema.org", "@type": "DefinedTerm", "@id": url_conceito(c["id"]), "name": c["nome"],
              **({"alternateName": nome_comum(c, False)} if c["id"] in NOME_COMUM else {}),
              "description": can["texto"] if can else "", "url": url_conceito(c["id"]), "inLanguage": "pt-BR",
              "inDefinedTermSet": {"@type": "DefinedTermSet", "@id": BASE + "/#atlas", "name": "Atlas Lex Plataformae"},
              "author": {"@type": "Person", "name": "Victor Luiz Pereira de Andrade"}}
    destino = SAIDA / "conceitos" / c["id"]
    destino.mkdir(parents=True, exist_ok=True)

    if e:
        def bloco_ext(campo_, rotulo=None, classe=""):
            b = e.get(campo_)
            if not b:
                return ""
            rotulo = b.get("pergunta") or rotulo
            return (f'<section class="ext {classe}">' + (f'<p class="rotulo-ext">{esc(rotulo)}</p>' if rotulo else "")
                    + "".join(f"<p>{esc(t)}</p>" for t in b["paragrafos"]) + expansao(b["citacoes"], prefixo) + "</section>")
        nome_b = e.get("nome", {"paragrafos": [], "citacoes": []})
        resto = re.sub(r"^.*?[.!?]\s+", "", " ".join(nome_b["paragrafos"]), count=1)
        duvida = ext_texto(c["id"], "duvida")
        externo = (
            f'<a class="voltar" href="{prefixo}conceitos/">← Todo o vocabulário</a>'
            f'<header class="folha-cabeca ext-cabeca"><h1><span class="em-modo modo-0 modo-2">{esc(ext_texto(c["id"], "titulo"))}</span>'
            f'<span class="em-modo modo-1">{nome_html(c)}</span></h1></header>'
            '<div class="pilha em-modo modo-0 modo-2">'
            + bloco_ext("fenomeno", classe="fenomeno")
            + f'<section class="ext nome-ext"><h2 class="nome-conceito"><span class="chapado">{nome_html(c)}</span></h2>'
            + (f"<p>{esc(resto)}</p>" if resto else "") + expansao(nome_b["citacoes"], prefixo) + "</section>"
            + figura(f'ideia-{c["id"]}', prefixo)
            + bloco_ext("imagem", "Como imaginar isso?", "didatico imagem")
            + bloco_ext("mecanismo", "Como isso funciona?", "didatico mecanismo")
            + bloco_ext("caso", "Como isso aparece na prática?", "didatico caso")
            + bloco_ext("importa", "Por que isso importa?")
            + bloco_ext("limite", "Quais são os limites?", "limite")
            + (secao_direitos(direitos_da_ideia(c["id"]), prefixo) if direitos_da_ideia(c["id"]) else "")
            + no_percurso(c["id"], prefixo)
            + (f'<section class="ext duvida"><p class="pergunta-final">{esc(duvida)}</p>{botao_desnudar(True)}</section>' if duvida else "")
            + "</div>")
        doutrina = f'<div class="pilha doutrina em-modo modo-1 modo-2">{doutrina_html(f"conceito {c["id"]}", prefixo)}{nas_situacoes}{no_curso_html(capitulo_curso(slug=CURSO_CONCEITO.get(c["id"])), prefixo)}</div>'
        nota_nome = ""
        if c["id"] in NOME_COMUM:
            genitivo = "A variação “plataformae” corresponde ao genitivo singular de primeira declinação, sinalizando “da plataforma”"
            nota_nome = ('<section class="nota-autor ciencia" data-arq="acréscimo posterior · fora do texto da tese de 2026">'
                         f'<p class="sobrelinha">Nome em português · acréscimo de {DATA_NOME_COMUM}</p>'
                         f'<p>Desde {DATA_NOME_COMUM}, nos modos Informação e Doutrina, o site chama este conceito de {esc(nome_comum(c, False))}, '
                         f'a tradução literal do nome em latim. O nome {esc(c["nome"])} segue neste modo e no nome do site.</p>'
                         f'<blockquote class="citacao"><p>{esc(genitivo)}{pg("p. 27", prefixo, genitivo)}</p></blockquote></section>')
        arquitetura = (f'<div class="ciencia arquitetura" data-arq="arquitetura · o conceito no texto integral">'
                       f'<header class="folha-cabeca"><p class="sobrelinha"><span class="ciencia">{esc(sobre)}</span></p><h2 class="titulo-interno">{nome_html(c)}</h2><div class="selos ciencia">{selos}</div></header>'
                       + nota_nome + "".join(partes) + "</div>")
        corpo = f'<article class="folha conceito-pagina">{externo}{doutrina}{arquitetura}{outros_nav}</article>'
        desc = ext_texto("cartoes", c["id"]) or (resumo(can["texto"]) if can else c["nome"])
        (destino / "index.html").write_text(
            pagina(f'{nome_titulo(c)} · Conceitos · Lex Plataformae', desc, corpo, prefixo, f'conceitos/{c["id"]}/', jsonld, camada="mista", imagem=c["id"],
                   irmas=("O vocabulário", [(nome_html(x), f'../{x["id"]}/', x is c) for x in em_ordem(conceitos_do_atlas())])), encoding="utf-8")
        return

    corpo = (f'<article class="folha"><a class="voltar" href="{prefixo}conceitos/">← Todo o vocabulário</a>'
             f'<header class="folha-cabeca"><p class="sobrelinha ciencia">{esc(sobre)}</p><h1>{nome_html(c)}</h1><div class="selos ciencia">{selos}</div></header>'
             f'<div class="pilha doutrina">{doutrina_html(f"conceito {c["id"]}", prefixo)}{nas_situacoes}{no_curso_html(capitulo_curso(slug=CURSO_CONCEITO.get(c["id"])), prefixo)}</div>'
             '<div class="ciencia arquitetura">' + "".join(partes) + "</div>" + outros_nav + "</article>")
    desc = resumo(can["texto"]) if can else c["nome"]
    (destino / "index.html").write_text(
        pagina(f'{nome_titulo(c)} · Conceitos · Lex Plataformae', desc, corpo, prefixo, f'conceitos/{c["id"]}/', jsonld,
               irmas=("O vocabulário", [(nome_html(x), f'../{x["id"]}/', False) for x in em_ordem(conceitos_do_atlas())])), encoding="utf-8")


def conceitos_por_secao():
    """Para cada seção da tese, os conceitos do site que a citam em 'Onde vive'."""
    mapa = {}
    for c in D["conceitos"]:
        f = campo(c, "Onde vive")
        if not f:
            continue
        for i in re.split(r",\s*(?![^()]*\))", f["texto"].rstrip(".")):
            sec = secao_de_lugar(i.strip())
            if sec:
                mapa.setdefault(sec["slug"], [])
                if c not in mapa[sec["slug"]]:
                    mapa[sec["slug"]].append(c)
    return mapa


def ancestrais(sec):
    n = sec["n"]
    if not n:
        return []
    partes = n.split(".")
    return [POR_NUMERO[".".join(partes[:k])] for k in range(1, len(partes)) if ".".join(partes[:k]) in POR_NUMERO]


def irmas_da_secao(sec):
    """As seções do mesmo capítulo. Fora dos capítulos numerados, as partes de primeiro nível do texto integral."""
    if sec["n"]:
        cap = sec["n"].split(".")[0]
        return [x for x in SECOES if x["n"] and x["n"].split(".")[0] == cap]
    return [x for x in SECOES if not x["n"] or "." not in x["n"]]


def rotulo_secao(sec):
    return f'{sec["n"]} {sec["titulo"]}' if sec["n"] else sec["titulo"].capitalize()


def rotulo_secao_html(sec):
    """O rótulo da seção para a página. O número só aparece em Ciência, porque fora da tese ele atrapalha o raciocínio."""
    if not sec["n"]:
        return esc(sec["titulo"].capitalize())
    return f'<span class="num-secao">{esc(sec["n"])} </span>{esc(sec["titulo"])}'


PLANO_INICIOS = [("Após a exposição", ["1", "2"]), ("A terceira seção", ["3"]), ("A quarta seção", ["4"]),
                  ("Ao longo de tais seções", None), ("Na quinta seção", ["5"]), ("A sexta seção", ["6"]),
                  ("A sétima seção", ["7"]), ("Ao final, a oitava seção", ["8"])]
# O nome que o leitor vê para cada camada, como no menu de cada modo. As chaves internas continuam as mesmas.
ROTULO_CAMADA = {"Atlas": "Conceitos", "Roteiro": "Para operar", "Laboratório": "Plataformas"}
CAMADA_ENDERECO = {"Atlas": "", "Roteiro": "roteiro/", "Laboratório": "plataformas/", "Fundamentos": "fundamentos/", "Método": "metodo/", "Dogmática": "dogmatica/", "Epígrafes": "epigrafes/"}


def plano_da_tese(prefixo, usos, por_secao):
    """O plano da obra, nas palavras da introdução, com o lugar de cada seção primária no site."""
    intro = POR_NUMERO.get("1")
    if not intro:
        return ""
    blocos = intro["blocos"]
    i = next((k for k, b in enumerate(blocos) if "organiza-se em oito seções" in b["html"]), None)
    if i is None:
        return ""
    pagina_atual = intro["pagina_inicio"]
    for b in blocos[:i]:
        for m in re.finditer(r'id="p(\d+)"', b["html"]):
            pagina_atual = int(m.group(1))
    texto = " ".join(b["html"] for b in blocos[i:i + 4])
    padrao = "|".join(re.escape(x) for x, _ in PLANO_INICIOS)
    marca = r'<span class="pg-marca"[^>]*>[^<]*</span>\s*'
    pedacos = [p.strip() for p in re.split(f"(?=(?:{padrao}))", texto) if p.strip()]
    # Marca de página no fim de um pedaço pertence ao começo do seguinte.
    for k in range(len(pedacos) - 1):
        m = re.search(f"((?:{marca})+)$", pedacos[k])
        if m:
            pedacos[k], pedacos[k + 1] = pedacos[k][:m.start()].strip(), m.group(1) + pedacos[k + 1]
    itens = []
    for pedaco in pedacos:
        m = re.match(f"((?:{marca})+)", pedaco)
        if m:
            pagina_atual = int(re.findall(r'id="p(\d+)"', m.group(1))[-1])
        inicio_pag = pagina_atual
        for x in re.findall(r'id="p(\d+)"', pedaco[m.end() if m else 0:]):
            pagina_atual = int(x)
        ref = f"p. {inicio_pag}" if inicio_pag == pagina_atual else f"p. {inicio_pag}-{pagina_atual}"
        limpo = re.sub(marca, "", pedaco).strip()
        alvo = next((caps for inicio, caps in PLANO_INICIOS if limpo.startswith(inicio)), "lead")
        itens.append([alvo, limpo, ref])
    # O comentário sobre as seções 3 e 4 acompanha a quarta seção.
    juntos = []
    for alvo, limpo, ref in itens:
        if alvo is None and juntos:
            juntos[-1][1] += " " + limpo
        else:
            juntos.append([alvo, limpo, ref])
    lead = next((x for x in juntos if x[0] == "lead"), None)

    def camadas(cap):
        nomes = []
        for sec in SECOES:
            if sec["n"] == cap or (sec["n"] or "").startswith(cap + "."):
                if por_secao.get(sec["slug"]) and "Atlas" not in nomes:
                    nomes.append("Atlas")
                for camada, _, _ in usos.get(sec["slug"], []):
                    if camada in CAMADA_ENDERECO and camada not in nomes:
                        nomes.append(camada)
        return nomes

    lis = []
    for alvo, limpo, ref in juntos:
        if alvo == "lead":
            continue
        caps = "".join(f'<li><a href="{POR_NUMERO[c]["slug"]}/">{"Introdução" if c == "1" else f'<span class="num num-secao">Seção {c}</span> ' + esc(POR_NUMERO[c]["titulo"])}</a>'
                       f' <span class="pag ciencia">p. {POR_NUMERO[c]["pagina_inicio"]} a {POR_NUMERO[c]["pagina_fim"]}</span></li>'
                       for c in alvo if c in POR_NUMERO)
        nomes = []
        for c in alvo:
            for n in camadas(c):
                if n not in nomes:
                    nomes.append(n)
        no_site = ('<p class="plano-site"><span class="sobrelinha">No site</span> '
                   + " · ".join(f'<a href="{prefixo}{CAMADA_ENDERECO[n]}">{esc(ROTULO_CAMADA.get(n, n))}</a>' for n in nomes) + "</p>") if nomes else ""
        lis.append(f'<li><ul class="plano-caps">{caps}</ul><blockquote class="citacao"><p>{html_do_corpus(limpo, intro["slug"], prefixo)}{pg(ref, prefixo, _plano(limpo))}</p></blockquote>{no_site}</li>')
    abertura = f'<blockquote class="citacao"><p>{html_do_corpus(lead[1], intro["slug"], prefixo)}{pg(lead[2], prefixo, _plano(lead[1]))}</p></blockquote>' if lead else ""
    return (f'<section class="bloco plano" id="plano" data-arq="estrutura · o plano da obra nas palavras da introdução"><h2>O plano da tese</h2>{abertura}'
            f'<ol class="plano-lista">{"".join(lis)}</ol></section>')


def gerar_tese():
    if not SECOES:
        return
    pasta = SAIDA / "tese"
    pasta.mkdir(exist_ok=True)
    por_secao = conceitos_por_secao()
    usos = usos_por_secao()

    # Índice da tese, com resumo e sumário.
    itens = []
    for sec in SECOES:
        nivel = sec["n"].count(".") if sec["n"] else 0
        itens.append(f'<li class="nivel-{nivel}"><a href="{sec["slug"]}/"><span class="num num-secao">{esc(sec["n"])}</span>'
                     f'<span class="tit">{esc(sec["titulo"])}</span></a><span class="pag ciencia">p. {sec["pagina_inicio"]}</span></li>')
    resumo = C.get("resumo")
    bloco_resumo = ""
    if resumo:
        chaves = "".join(f"<li>{esc(k)}</li>" for k in resumo["palavras_chave"])
        bloco_resumo = (f'<section class="bloco" id="resumo"><h2>Resumo</h2><p>{esc(resumo["texto"])}</p>'
                        f'<ul class="lugares">{chaves}</ul></section>')
    abertura = "".join(f'<li>{esc(e["artista"])}, <cite>{esc(e["faixa"])}</cite> ({e["ano"]})</li>' for e in C.get("epigrafe_abertura", []))
    corpo = (
        '<article class="folha leitura">'
        '<header class="folha-cabeca"><p class="sobrelinha">Texto integral · seção por seção</p>'
        f'<h1>{esc(TITULO_TESE)}</h1>'
        f'<p><a class="botao" href="{PDF_NOME}">Baixar o texto integral em PDF</a></p></header>'
        f'{bloco_resumo}'
        '<section class="bloco"><h2>Como ler aqui</h2><p>O texto de cada seção é o do original, extraído do PDF e conferido por script. '
        'Em Ciência, cada página impressa aparece marcada no ponto em que começa. Nos outros modos, a página aparece ao passar o mouse ou tocar no parágrafo, '
        'com a referência pronta para copiar. As notas de rodapé vêm ao fim de cada seção. '
        '<span class="ciencia">As letras das epígrafes estão no PDF.</span>'
        + (f' <span class="ciencia">As duas epígrafes gerais são {" e ".join(credito_epigrafe(e) for e in C.get("epigrafe_abertura", []))}, e a segunda abre também a introdução.</span>' if C.get("epigrafe_abertura") else "")
        + ' <span class="ciencia">A página das <a href="../epigrafes/">epígrafes musicais</a> conta o que cada uma das nove anuncia.</span>' +
        '</p></section>'
        + plano_da_tese("../", usos, por_secao) +
        f'<nav class="bloco sumario" aria-label="Sumário"><h2>Sumário</h2><ol>{"".join(itens)}</ol></nav>'
        '</article>'
    )
    jsonld = {"@context": "https://schema.org", "@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE,
              "author": {"@type": "Person", "name": "Victor Luiz Pereira de Andrade"}, "datePublished": "2026",
              "inLanguage": "pt-BR", "abstract": resumo["texto"] if resumo else None,
              "keywords": resumo["palavras_chave"] if resumo else None, "url": BASE + "/tese/"}
    (pasta / "index.html").write_text(
        pagina("Texto integral · Do regime jurídico do Objeto Imaterial de Consumo (OIC) sob a Lex Plataformae", resumir_texto(resumo["texto"]) if resumo else TITULO_TESE, corpo, "../", "tese/", jsonld, camada="mista", lei=False),
        encoding="utf-8")

    # Uma página por seção.
    for i, sec in enumerate(SECOES):
        prefixo = "../../"
        trilha = ['<a href="../">Texto integral</a>'] + [f'<a href="../{a["slug"]}/">{rotulo_secao_html(a)}</a>' for a in ancestrais(sec)]
        faixa_pag = f'p. {sec["pagina_inicio"]}' + (f' a {sec["pagina_fim"]}' if sec["pagina_fim"] != sec["pagina_inicio"] else "")
        partes = []
        epigrafes_sec = list(sec.get("epigrafes", []))
        if sec["n"] == "1":
            epigrafes_sec += [e for e in C.get("epigrafe_abertura", []) if e.get("abre", "").startswith("1 ")]
        for e in epigrafes_sec:
            partes.append(f'<aside class="epigrafe-ref ciencia" data-arq="epígrafe · a letra está no PDF">'
                          f'<p class="sobrelinha">Epígrafe</p><p>{credito_epigrafe(e)}. '
                          f'<a href="{prefixo}epigrafes/#epigrafe-{e["ordem"]}">O que ela anuncia</a> · <a href="../{PDF_NOME}#page={e["pagina_pdf"]}">Ler a epígrafe no PDF</a>.</p></aside>')
        for b in sec["blocos"]:
            if b["tipo"] == "citacao":
                partes.append(f'<blockquote class="citacao-longa"{attrs_ref(b, prefixo)}>{b["html"]}</blockquote>')
            elif b["tipo"] == "tabela":
                partes.append(f'<div class="tabela-tese">{b["html"]}</div>')
            elif b["tipo"] == "marca":
                partes.append(f'<p class="marca-solta">{b["html"]}</p>')
            else:
                partes.append(f"<p{attrs_ref(b, prefixo)}>{b['html']}</p>")
        notas = ""
        if sec["notas"]:
            notas = ('<section class="notas" aria-labelledby="notas-titulo"><h2 id="notas-titulo">Notas</h2><ol>'
                     + "".join(f'<li id="n{n["n"]}" value="{n["n"]}">{n["html"]} <a class="volta" href="#r{n["n"]}" aria-label="Voltar à chamada da nota {n["n"]}">↩</a></li>' for n in sec["notas"])
                     + "</ol></section>")
        aqui = por_secao.get(sec["slug"], [])
        conceitos_aqui = ""
        for tipo, rotulo in (("conceito", "Conceitos nesta seção"), ("roteiro", "Parâmetros com ficha nesta seção"), ("bens", "Bens protegidos nesta seção")):
            deste = [c for c in aqui if c["tipo"] == tipo]
            if deste:
                conceitos_aqui += (f'<aside class="conceitos-aqui" data-arq="fichas · conceitos que vivem nesta seção">'
                                   f'<p class="sobrelinha">{rotulo}</p><ul>'
                                   + "".join(f'<li><a href="{prefixo}conceitos/{c["id"]}/">{nome_html(c)}</a></li>' for c in em_ordem(deste))
                                   + "</ul></aside>")
        if usos.get(sec["slug"]):
            conceitos_aqui += ('<aside class="conceitos-aqui camadas-aqui ciencia" data-arq="estrutura · páginas das camadas que trazem esta seção">'
                               '<p class="sobrelinha">Esta seção nas camadas do site</p><ul>'
                               + "".join(f'<li><a href="{prefixo}{caminho}">{esc(ROTULO_CAMADA.get(camada, camada))} · {esc(rotulo)}</a></li>' for camada, rotulo, caminho in usos[sec["slug"]])
                               + "</ul></aside>")
        ant = SECOES[i - 1] if i > 0 else None
        prox = SECOES[i + 1] if i + 1 < len(SECOES) else None
        viz = ('<nav class="vizinhos" aria-label="Seções vizinhas">'
               + (f'<a href="../{ant["slug"]}/">← {rotulo_secao_html(ant)}</a>' if ant else "<span></span>")
               + (f'<a href="../{prox["slug"]}/">{rotulo_secao_html(prox)} →</a>' if prox else "<span></span>") + "</nav>")
        titulo = sec.get("titulo_html") or esc(rotulo_secao(sec))
        if sec["n"] and titulo.startswith(sec["n"] + " "):
            titulo = f'<span class="num-secao">{esc(sec["n"])} </span>' + titulo[len(sec["n"]) + 1:]
        corpo = (f'<article class="folha leitura texto-integral"><nav class="trilha" aria-label="Você está em">{" › ".join(trilha)}</nav>'
                 f'<header class="folha-cabeca"><p class="sobrelinha ciencia">{"Seção " + esc(sec["n"]) if sec["n"] else "Referências"} · {faixa_pag}</p>'
                 f'<h1>{titulo}</h1>'
                 f'<p class="ler-pdf"><a href="../{PDF_NOME}#page={sec["pagina_inicio"] + C.get("deslocamento", 2)}">Ver esta seção no PDF</a></p></header>'
                 f'{conceitos_aqui}<div class="texto">{"".join(partes)}</div>{notas}{viz}</article>')
        texto_puro = html.unescape(re.sub(r"<[^>]+>", " ", " ".join(b["html"] for b in sec["blocos"][:3])))
        texto_puro = re.sub(r"\bp\. \d+\b", " ", texto_puro)
        jsonld = {"@context": "https://schema.org", "@type": "Chapter", "name": rotulo_secao(sec), "inLanguage": "pt-BR",
                  "pageStart": sec["pagina_inicio"], "pageEnd": sec["pagina_fim"], "url": f'{BASE}/tese/{sec["slug"]}/',
                  "isPartOf": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE},
                  "author": {"@type": "Person", "name": "Victor Luiz Pereira de Andrade"}}
        destino = pasta / sec["slug"]
        destino.mkdir(parents=True, exist_ok=True)
        (destino / "index.html").write_text(
            pagina(f'{rotulo_secao(sec)} · Texto integral · Lex Plataformae', resumir_texto(texto_puro), corpo, prefixo, f'tese/{sec["slug"]}/', jsonld, camada="mista", lei=False,
                   irmas=("Neste capítulo" if sec["n"] else "O texto integral", [(rotulo_secao_html(x), f'../{x["slug"]}/', x is sec) for x in irmas_da_secao(sec)])),
            encoding="utf-8")


def resumir_texto(t):
    return resumo(t)


# Roteiro. Os blocos de enquadramento do 7.1.2, na ordem da tese, todos em texto literal.
ROTEIRO_MAPA = {
    "a": ("7.1.1.1", ["oic", "feixe-de-fruicao-governada"]),
    "b": ("7.1.1.2", ["vulnerabilidade-semiotica"]),
    "c": ("7.1.1.3", []),
    "d": ("7.1.1.4", ["antecipacao-hipercuratorial"]),
    "e": ("7.1.1.5", ["auditabilidade-aberta"]),
    "f": ("7.1.1.6", ["equivalencia-de-valor-funcional"]),
    "g": (None, []),
    "h": ("7.1.1.7", ["teleologia-abusiva", "ilicito-de-arquitetura"]),
    "i": ("7.1.1.8", []),
    "j": ("7.1.1.9", ["funcao-social-da-pi"]),
    "k": ("7.1.1.10", ["recomposicao-funcional"]),
}
# Títulos por situação, para a tela do técnico. Rascunho do Claude de 27/10/2026, a pedido do autor, que critica depois.
# Cada título nasce do "Sempre que" do próprio bloco. Em Ciência aparece também o título da tese, com a letra.
SITUACOES = {
    "a": "Quando o que foi comprado depende do ambiente que a plataforma administra",
    "b": "Quando o consumidor só entende o que a interface deixa entender",
    "c": "Quando a informação existe, mas some no excesso",
    "d": "Quando a vitrine prometeu mais do que foi entregue",
    "e": "Quando a plataforma mudou as regras e não deixou rastro",
    "f": "Quando a atualização tirou o valor do que foi comprado",
    "g": "Quando punir é fácil e contestar é difícil",
    "h": "Quando a perda é rotina do desenho, e não acidente",
    "i": "Como provar quando a prova está com a plataforma",
    "j": "Quando a propriedade intelectual vira escudo",
    "k": "O que pedir, restaurar antes de indenizar",
}

PARTES_ROTEIRO = [
    ("Quando incide", r"Sempre que"),
    ("Dever de fornecimento", r"O dever (?:de fornecimento )?correspondente"),
    ("Prova mínima", r"A prova mínima exigível"),
    ("Qualificação jurídica", r"A qualificação jurídica"),
    ("Consequência institucional", r'A (?:<span class="pg-marca"[^>]*>[^<]*</span>\s*)?consequência institucional'),
]


def html_do_corpus(h, slug, prefixo):
    """Reaproveita um trecho do corpus noutra página. Marcas e notas viram links para o corpus, sem ids repetidos."""
    h = re.sub(r'<span class="pg-marca" id="p(\d+)"[^>]*>(p\. \d+)</span>',
               lambda m: f'<a class="pg-marca" href="{prefixo}tese/{slug}/#p{m.group(1)}">{m.group(2)}</a>', h)
    h = re.sub(r'<sup class="nota-ref"><a href="#n(\d+)" id="r\d+">(\d+)</a></sup>',
               lambda m: f'<sup class="nota-ref"><a href="{prefixo}tese/{slug}/#n{m.group(1)}">{m.group(2)}</a></sup>', h)
    return h


_NOTA = r'(?:<sup class="nota-ref">(?:(?!</sup>).)*</sup>)'
_MARCA = r'(?:<a class="pg-marca"[^>]*>[^<]*</a>|<span class="pg-marca"[^>]*>[^<]*</span>)'
_ENTRE = r"(?:\s|" + _MARCA + "|" + _NOTA + ")+"












# Termos do Atlas e do Roteiro que a tese nomeia num trecho. A contagem é mecânica, sobre o texto literal.
TERMOS = {
    "oic": r"\bOICs?\b|[Oo]bjetos? [Ii]materia(?:l|is) de [Cc]onsumo",
    "lex-plataformae": r"Lex\s+Plataformae",
    "vulnerabilidade-semiotica": r"[Vv]ulnerabilidades? semióticas?",
    "teleologia-abusiva": r"[Tt]eleologias? abusivas?",
    "ilicito-de-arquitetura": r"[Ii]lícitos? (?:de arquitetura|arquitetura(?:l|is))",
    "antecipacao-hipercuratorial": r"[Aa]ntecipaç(?:ão|ões) hipercuratoria(?:l|is)",
    "auditabilidade-aberta": r"[Aa]uditabilidade aberta",
    "equivalencia-de-valor-funcional": r"[Ee]quivalência (?:de valor )?funcional\b",
    "feixe-de-fruicao-governada": r"[Ff]eixes? de fruição",
    "funcao-social-da-pi": r"[Ff]unção social da propriedade intelectual",
    "recomposicao-funcional": r"[Rr]ecomposição funcional",
    "integridade-pessoal": r"[Ii]ntegridade pessoal",
}


def termos_em(texto):
    contagem = {}
    for cid, padrao in TERMOS.items():
        n = len(re.findall(padrao, texto))
        if n and cid in POR_ID:
            contagem[cid] = n
    return contagem


def texto_de(blocos):
    return _plano(" ".join(b["html"] for b in blocos))


def nomeados_html(contagem, prefixo):
    if not contagem:
        return ""
    ordem = sorted(contagem, key=lambda cid: (cid != EIXO["id"], POR_ID[cid]["nome"].casefold()))
    itens = "".join(f'<li><a href="{prefixo}conceitos/{cid}/">{nome_html(POR_ID[cid])}</a> <span class="vezes">{contagem[cid]}×</span></li>' for cid in ordem)
    return ('<aside class="nomeados ciencia" data-arq="contagem mecânica · conceitos e enunciados que o trecho nomeia">'
            f'<p class="sobrelinha">Conceitos que o trecho nomeia</p><ul>{itens}</ul></aside>')


def blocos_do_roteiro():
    sec = POR_NUMERO.get("7.1.2")
    if not sec:
        return None
    itens, atual, abertura, fecho = [], None, [], None
    for b in sec["blocos"]:
        t = html.unescape(re.sub(r"<[^>]+>", "", b["html"])).strip()
        m = re.match(r"^([a-k])\) (.+?)[;.]\s*$", t)
        if m:
            atual = {"letra": m.group(1), "titulo": m.group(2), "html": ""}
            itens.append(atual)
            continue
        if t.startswith("Esse quadro"):
            fecho = b["html"]
            continue
        if atual is None:
            if b["tipo"] == "p":
                abertura.append(b["html"])
            continue
        if not atual["html"] and ref_bloco(b):
            atual["inicio"] = ref_bloco(b)[2]
        atual["html"] += " " + b["html"]
    inicios = "|".join(f"(?:{r})" for _, r in PARTES_ROTEIRO)
    for it in itens:
        pedacos = [x.strip() for x in re.split(f"(?=(?:{inicios}))", it["html"]) if x.strip()]
        partes, pendente = [], ""
        for pedaco in pedacos:
            sem_marca = re.sub(r'^(<span class="pg-marca"[^>]*>[^<]*</span>\s*)+', "", pedaco)
            if not sem_marca.strip():
                pendente += pedaco + " "
                continue
            pedaco, pendente = pendente + pedaco, ""
            rotulo = next((r for r, padrao in PARTES_ROTEIRO if re.match(padrao, sem_marca)), None)
            if rotulo is None and partes:
                partes[-1][1] += " " + pedaco
            else:
                partes.append([rotulo or "Quando incide", pedaco])
        # A página em que cada parte começa e termina, pelas marcas de página do texto.
        atual_pag = it.get("inicio") or sec["pagina_inicio"]
        for parte in partes:
            marcas = [int(x) for x in re.findall(r'id="p(\d+)"', parte[1])]
            comeca = re.match(r'\s*<span class="pg-marca" id="p(\d+)"', parte[1])
            ini = int(comeca.group(1)) if comeca else atual_pag
            fim = marcas[-1] if marcas else ini
            parte.append(f"p. {ini}" if ini == fim else f"p. {ini}-{fim}")
            atual_pag = fim
        it["partes"] = partes
    return {"secao": sec, "abertura": abertura, "itens": itens, "fecho": fecho}


def gerar_roteiro():
    r = blocos_do_roteiro()
    if not r:
        return
    prefixo = "../"
    slug = r["secao"]["slug"]
    secoes = []
    for it in r["itens"]:
        num, ids = ROTEIRO_MAPA.get(it["letra"], (None, []))
        ligacoes = []
        cap = capitulo_curso(slug=CURSO_SITUACAO[it["letra"]]) if it["letra"] in CURSO_SITUACAO else capitulo_curso(num)
        if cap:
            ligacoes.append(link_curso(cap, prefixo))
        if num and num in POR_NUMERO:
            ligacoes.append(f'<a href="{prefixo}roteiro/parametros/#parametro-{it["letra"]}">O parâmetro</a>')
            ligacoes.append(f'<span class="ciencia"> · <a href="{prefixo}tese/{POR_NUMERO[num]["slug"]}/">Enunciado {num} na tese</a></span>')
        ligacoes += [f'<a href="{prefixo}conceitos/{i}/">{nome_html(POR_ID[i])}</a>' for i in ids if i in POR_ID]
        # O campo do quadro fala na voz do site, e o texto literal fica logo abaixo, só na Ciência. Revisão de voz de 05/11/2026.
        campos_site = {s["titulo"]: " ".join(s["paragrafos"]) for s in DOUTRINA.get(f'quadro {it["letra"]}', [])}
        # A tese marca a qualificação como possível de b a k. Em a, ela é a qualificação daí resultante. Segunda leitura de 05/11/2026.
        dl = "".join(f'<dt>{esc(rot + " possível" if rot == "Qualificação jurídica" and it["letra"] != "a" else rot)}</dt><dd>{esc(campos_site.get(rot, ""))}</dd>'
                     f'<dd class="quadro-literal ciencia" data-ref="{esc(ref)}" data-alvo="{prefixo}tese/{slug}/#p{re.match(r"p. (\d+)", ref).group(1)}">{html_do_corpus(h, slug, prefixo)}</dd>'
                     for rot, h, ref in it["partes"])
        secoes.append(
            f'<section class="bloco-roteiro" id="{it["letra"]}" aria-labelledby="titulo-{it["letra"]}">'
            f'<h2 id="titulo-{it["letra"]}">{esc(SITUACOES.get(it["letra"], it["titulo"]))}</h2>'
            f'<p class="titulo-tese ciencia"><span class="letra">{it["letra"]})</span> {esc(it["titulo"])}</p>'
            + operar_html(it["letra"], prefixo)
            + f'<dl class="partes quadro" data-arq="o quadro do 7.1.2 · cinco partes, na voz do site e em texto literal">{dl}</dl>'
            + (f'<p class="ligacoes">{"".join(l if k == 0 or l.startswith("<span") else " · " + l for k, l in enumerate(ligacoes))}</p>' if ligacoes else "")
            + "</section>")
    indice = "".join(f'<li><a href="#{it["letra"]}"><span class="letra ciencia">{it["letra"]})</span> {esc(SITUACOES.get(it["letra"], it["titulo"]))}</a></li>' for it in r["itens"])
    intro = OPERAR.get("intro")
    como_usar = (f'<section class="bloco como-usar"><h2>Como usar</h2>' + "".join(f"<p>{esc(t)}</p>" for t in intro["texto"])
                 + expansao(intro["citacoes"], prefixo, "ciencia") + "</section>") if intro else ""
    corpo = (
        '<article class="folha leitura roteiro">'
        '<header class="folha-cabeca"><p class="sobrelinha ciencia">Situações · 7.1.2 da tese</p><h1>Situações</h1>'
        '<p class="abertura-pagina">Onze situações em que o regime se aplica a um conflito com a plataforma. '
        'Cada uma traz o guia para operar e o quadro, com o que incide, o que se deve, o que provar e o que pedir.</p>'
        '</header>'
        + nav_roteiro("7.1.2", prefixo)
        + doutrina_html("situacoes abertura", prefixo)
        + como_usar
        + f'<nav class="bloco indice-roteiro" aria-label="As situações"><h2>As onze situações</h2><ol>{indice}</ol></nav>'
        + "".join(secoes)
        + doutrina_html("situacoes fecho", prefixo)
        + '</article>'
    )
    jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": "Situações · Lex Plataformae", "inLanguage": "pt-BR",
              "url": BASE + "/roteiro/", "isBasedOn": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE}}
    pasta = SAIDA / "roteiro"
    pasta.mkdir(exist_ok=True)
    desc = "Onze situações para quem vai advogar, cada uma com fatos típicos, prova, fundamento normativo, cuidados e o que pedir."
    (pasta / "index.html").write_text(pagina("Situações para operar em conflitos com plataformas digitais · Lex Plataformae", desc, corpo, prefixo, "roteiro/", jsonld, irmas=irmas_roteiro("7.1.2", prefixo)), encoding="utf-8")


# As partes do Roteiro, uma página para cada seção do 7.1 que a tese organiza como instrumento de aplicação.
ROTEIRO_PARTES = [("7.1.1", "roteiro/parametros/"), ("7.1.2", "roteiro/"), ("7.1.3", "roteiro/diretrizes/"), ("7.1.4", "roteiro/limites/")]
ORDINAIS = ["primeira", "segunda", "terceira", "quarta", "quinta", "sexta", "sétima", "oitava", "nona", "décima"]


ROTEIRO_ROTULOS = {"7.1.1": "Parâmetros", "7.1.2": "Situações", "7.1.3": "Diretrizes de controle", "7.1.4": "Limites ao poder da plataforma"}


def nav_roteiro(atual, prefixo, lema=""):
    """As quatro partes de Para operar ficam na coluna lateral. Revisão de disposição de 05/11/2026."""
    return lema


def irmas_roteiro(atual, prefixo):
    itens = []
    for num, caminho in ROTEIRO_PARTES:
        sec = POR_NUMERO.get(num)
        if not sec:
            continue
        itens.append((f'<span class="em-modo modo-0 modo-1">{esc(ROTEIRO_ROTULOS[num])}</span>'
                      f'<span class="em-modo modo-2"><span class="num">{esc(num)}</span> {esc(sec["titulo"])}</span>', f"{prefixo}{caminho}", num == atual))
    return ("Para operar", itens)


def diretrizes():
    """Separa o 7.1.3 em abertura, dez diretrizes e fecho, pela palavra que a própria tese usa para cada uma."""
    sec = POR_NUMERO.get("7.1.3")
    if not sec:
        return None
    abertura, itens, fecho = [], [], []
    for b in sec["blocos"]:
        t = _plano(b["html"]).strip().lower()
        m = re.search(r"\b(" + "|".join(ORDINAIS) + r") diretriz\b", t)
        if b["tipo"] == "p" and m and ORDINAIS.index(m.group(1)) == len(itens):
            itens.append([len(itens) + 1, m.group(1), [b]])
        elif t.startswith("essas diretrizes, em conjunto"):
            fecho.append(b)
        elif fecho:
            fecho.append(b)
        elif itens:
            itens[-1][2].append(b)
        else:
            abertura.append(b)
    return {"secao": sec, "abertura": abertura, "itens": itens, "fecho": fecho}






def gerar_parametros():
    """Os dez parâmetros, na voz do site, cada um com o título da situação que prepara. O literal fica no texto integral."""
    s71, s711 = POR_NUMERO.get("7.1"), POR_NUMERO.get("7.1.1")
    if not s71 or not s711:
        return
    prefixo = "../../"
    secoes, indice = [], []
    for letra, (num, _) in ROTEIRO_MAPA.items():
        sec = POR_NUMERO.get(num) if num else None
        if not sec:
            continue
        titulo = SITUACOES.get(letra, sec["titulo"])
        indice.append(f'<li><a href="#parametro-{letra}">{esc(titulo)}</a></li>')
        secoes.append(
            f'<section class="bloco-roteiro" id="parametro-{letra}" aria-labelledby="titulo-parametro-{letra}">'
            f'<h2 id="titulo-parametro-{letra}">{esc(titulo)}</h2>'
            f'<p class="titulo-tese ciencia"><span class="letra">{esc(num)}</span> {esc(sec["titulo"])}</p>'
            + doutrina_html(f"parametro {num}", prefixo)
            + f'<p class="ligacoes">{(link_curso(capitulo_curso(num), prefixo) + " · ") if capitulo_curso(num) else ""}<a href="{prefixo}roteiro/#{letra}">A situação no quadro</a><span class="ciencia"> · <a href="{prefixo}tese/{sec["slug"]}/">Ler no texto integral</a></span></p>'
            f'{nomeados_html(termos_em(texto_de(sec["blocos"])), prefixo)}</section>')
    corpo = (
        '<article class="folha leitura roteiro">'
        f'<header class="folha-cabeca"><p class="sobrelinha ciencia">7.1 e 7.1.1 · p. {s71["pagina_inicio"]} a {POR_NUMERO["7.1.1.10"]["pagina_fim"] if "7.1.1.10" in POR_NUMERO else s711["pagina_fim"]}</p>'
        f'<h1>Parâmetros</h1><p class="abertura-pagina">Os dez parâmetros organizam a leitura de cada caso, um por situação, na ordem em que a análise avança. '
        'Cada um diz o que controla, o que não basta e aonde leva.</p></header>'
        + doutrina_html("parametros abertura", prefixo)
        + f'<nav class="bloco indice-roteiro" aria-label="Os parâmetros"><h2>Os dez parâmetros</h2><ol>{"".join(indice)}</ol></nav>'
        + "".join(secoes)
        + saidas_html([("As situações, para operar", f"{prefixo}roteiro/"), ("As diretrizes de controle", f"{prefixo}roteiro/diretrizes/"),
                       ("Os conceitos", f"{prefixo}conceitos/")]) + "</article>")
    jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": "Parâmetros · Lex Plataformae", "inLanguage": "pt-BR",
              "url": BASE + "/roteiro/parametros/", "isBasedOn": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE}}
    destino = SAIDA / "roteiro" / "parametros"
    destino.mkdir(parents=True, exist_ok=True)
    desc = "Os dez parâmetros que preparam cada situação de conflito com plataformas digitais, com o que controlam, o que não basta e aonde levam."
    (destino / "index.html").write_text(pagina("Parâmetros para operar em conflitos com plataformas digitais · Lex Plataformae", desc, corpo, prefixo, "roteiro/parametros/", jsonld, irmas=irmas_roteiro("7.1.1", prefixo)), encoding="utf-8")


def gerar_diretrizes():
    sec = POR_NUMERO.get("7.1.3")
    if not sec:
        return
    prefixo = "../../"
    indice, secoes = [], []
    for n in range(1, 11):
        blocos = DOUTRINA.get(f"diretriz {n}", [])
        if not blocos:
            raise SystemExit(f"Falta a diretriz {n} em conteudo/doutrina.md")
        titulo = blocos[0]["titulo"]
        indice.append(f'<li><a href="#diretriz-{n}">{esc(titulo)}</a></li>')
        secoes.append(f'<div class="bloco-roteiro" id="diretriz-{n}">{doutrina_html(f"diretriz {n}", prefixo)}</div>')
    corpo = (
        '<article class="folha leitura roteiro">'
        '<nav class="trilha" aria-label="Você está em"><a href="../">Situações</a></nav>'
        f'<header class="folha-cabeca"><p class="sobrelinha ciencia">{esc(sec["n"])} · p. {sec["pagina_inicio"]} a {sec["pagina_fim"]}</p>'
        f'<h1><span class="em-modo modo-0 modo-1">{esc(ROTEIRO_ROTULOS["7.1.3"])}</span><span class="em-modo modo-2">{esc(sec["titulo"])}</span></h1>'
        '<p class="abertura-pagina">As dez diretrizes orientam o controle do desenho e da governança da plataforma. '
        'Cada uma diz o que examinar e o que o exame não pode aceitar como resposta.</p>'
        f'<p class="ler-pdf ciencia"><a href="{prefixo}tese/{sec["slug"]}/">Ler no texto integral</a></p></header>'
        + doutrina_html("diretrizes abertura", prefixo)
        + f'<nav class="bloco indice-roteiro" aria-label="As dez diretrizes"><h2>As dez diretrizes</h2><ol>{"".join(indice)}</ol></nav>'
        + "".join(secoes)
        + saidas_html(([(capitulo_curso("7.1.3")["titulo"] + ", no caminho do jurista", f'{prefixo}doutrina/{capitulo_curso("7.1.3")["slug"]}/')] if capitulo_curso("7.1.3") else [])
                      + [("As situações, para operar", f"{prefixo}roteiro/"), ("Os limites ao poder da plataforma", f"{prefixo}roteiro/limites/"),
                       ("A legislação citada", f"{prefixo}legislacao/")]) + "</article>")
    jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": sec["titulo"], "inLanguage": "pt-BR",
              "url": BASE + "/roteiro/diretrizes/", "isBasedOn": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE}}
    destino = SAIDA / "roteiro" / "diretrizes"
    destino.mkdir(parents=True, exist_ok=True)
    desc = "As dez diretrizes para o controle de arquitetura e governança em plataformas digitais, com o que examinar em cada uma."
    (destino / "index.html").write_text(pagina('Diretrizes de controle das plataformas digitais · Lex Plataformae', desc, corpo, prefixo, "roteiro/diretrizes/", jsonld, irmas=irmas_roteiro("7.1.3", prefixo)), encoding="utf-8")


def gerar_limites():
    sec = POR_NUMERO.get("7.1.4")
    if not sec:
        return
    prefixo = "../../"
    corpo = ('<article class="folha leitura roteiro">'
             '<nav class="trilha" aria-label="Você está em"><a href="../">Situações</a></nav>'
             f'<header class="folha-cabeca"><p class="sobrelinha">Para operar<span class="ciencia"> · {esc(sec["n"])} · p. {sec["pagina_inicio"]} a {sec["pagina_fim"]}</span></p>'
             f'<h1><span class="em-modo modo-0 modo-1">{esc(ROTEIRO_ROTULOS["7.1.4"])}</span><span class="em-modo modo-2">{esc(sec["titulo"])}</span></h1>'
             '<p class="abertura-pagina">O fornecimento pode alcançar condições práticas de participação e de permanência. O regime limita esse poder sem equiparar a plataforma ao Estado.</p>'
             f'<p class="ler-pdf ciencia"><a href="{prefixo}tese/{sec["slug"]}/">Ler no texto integral</a></p></header>'
             + doutrina_html("limites", prefixo)
             + saidas_html(([(capitulo_curso("7.1.4")["titulo"] + ", no caminho do jurista", f'{prefixo}doutrina/{capitulo_curso("7.1.4")["slug"]}/')] if capitulo_curso("7.1.4") else [])
                           + [("As situações, para operar", f"{prefixo}roteiro/"), ("As diretrizes de controle", f"{prefixo}roteiro/diretrizes/"),
                            ("A legislação citada", f"{prefixo}legislacao/")])
             + "</article>")
    jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": sec["titulo"], "inLanguage": "pt-BR",
              "url": BASE + "/roteiro/limites/", "isBasedOn": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE}}
    destino = SAIDA / "roteiro" / "limites"
    destino.mkdir(parents=True, exist_ok=True)
    desc = "Cidadania digital e limites ao poder privado de plataforma, com o que o regime controla e o que não equipara ao Estado."
    (destino / "index.html").write_text(pagina("Cidadania digital e limites ao poder da plataforma · Lex Plataformae", desc, corpo, prefixo, "roteiro/limites/", jsonld, irmas=irmas_roteiro("7.1.4", prefixo)), encoding="utf-8")


# Laboratório. As famílias de plataforma do 7.2, na sequência que a própria tese declara para cada uma.
FAMILIAS = [
    ("7.2.1", "funcionalidade-cognitiva"),
    ("7.2.2", "infraestrutura-e-intermediacao"),
    ("7.2.3", "produtividade-gig-economy"),
    ("7.2.7", "administracao-de-confianca"),
]
CAMPOS_FAMILIA = [
    ("Mecanismo de governança", None),
    ("Vulnerabilidade central, promessas e perdas", r"vulnerabilidade central"),
    ("Evidências, prova e pontos de cegueira", r"padrão probatório|evidência compatível"),
    ("Consequência dogmática possível", r"consequência dogmática possível"),
]
DESDOBRAMENTOS = [("7.2.4", "concorrencia"), ("7.2.5", "tutela-coletiva"), ("7.2.6", "consumidor-equiparado")]
ABERTURA_DESDOBRAMENTO = {
    "concorrencia": "A plataforma que governa a fruição também governa as condições perceptíveis de competição. O regime não substitui o direito concorrencial, mas dá a entrada para controlar essa governança.",
    "tutela-coletiva": "Há lesões cuja unidade está no desenho do fornecimento, e não na soma de episódios. Para elas, a resposta precisa alcançar o regime.",
    "consumidor-equiparado": "A tutela do consumidor pode alcançar quem, sem ser adquirente final clássico, está exposto à governança da plataforma. O critério é a sujeição real, e não o rótulo do contrato.",
}
LABORATORIO_ORIGEM = ["2.3", "5.2.2", "5.2.4", "6.1.2.1", "6.2.4.3.1"]


def locus_html(prefixo):
    """O recorte de aplicação ilustrativa, nas palavras da introdução (p. 36-37)."""
    intro = POR_NUMERO.get("1")
    if not intro:
        return ""
    for b in intro["blocos"]:
        m = re.search(r"No plano de aplicação ilustrativa.*?entre consumidores e fornecedor\.", b["html"], re.S)
        if m:
            return (f'<blockquote class="citacao"><p>{html_do_corpus(m.group(0), intro["slug"], prefixo)}'
                    f'{pg("p. 36-37", prefixo, _plano(m.group(0))[:80])}</p></blockquote>')
    return ""






def gerar_laboratorio():
    if not all(n in POR_NUMERO for n, _ in FAMILIAS):
        return
    pasta = SAIDA / "plataformas"
    pasta.mkdir(exist_ok=True)
    intro = POR_NUMERO.get("7.2")
    fecho = POR_NUMERO.get("7.3")
    sequencia = next((b["html"] for b in intro["blocos"] if "Para manter essa comparabilidade" in b["html"]), "") if intro else ""
    triade = next((b["html"] for b in fecho["blocos"] if "Ao manter distinguíveis" in b["html"]), "") if fecho else ""

    cartoes = []
    for num, slug in FAMILIAS:
        sec = POR_NUMERO[num]
        prefixo = "../../"
        e = EXTERNA.get(slug, {})
        externo = ""
        if e.get("titulo"):
            # Na Informação, cada família responde às perguntas que a página das plataformas promete, com a prova e a resposta
            # possíveis. Revisão de rótulos de 05/11/2026, que achou a página com dois parágrafos e seis saídas.
            def bloco_familia(campo_):
                b = e.get(campo_)
                if not b:
                    return ""
                # Linhas com hífen viram lista, e **trecho** no começo do parágrafo vira o destaque dele. 11/11/2026.
                partes_, lista_ = [], []
                def fecha_lista():
                    if lista_:
                        partes_.append("<ul>" + "".join(f"<li>{x}</li>" for x in lista_) + "</ul>")
                        lista_.clear()
                for t in b["paragrafos"]:
                    h = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", esc(t))
                    if t.startswith("- "):
                        lista_.append(h[2:])
                    else:
                        fecha_lista()
                        partes_.append(f"<p>{h}</p>")
                fecha_lista()
                return (f'<section class="ext familia-passo familia-{campo_}"><h2 class="rotulo-ext">{esc(b.get("pergunta", ""))}</h2>'
                        + "".join(partes_) + expansao(b["citacoes"], prefixo) + "</section>")
            externo = (f'<a class="voltar" href="../">← Todas as plataformas</a>'
                       f'<header class="folha-cabeca ext-cabeca"><h1><span class="em-modo modo-0 modo-2">{esc(ext_texto(slug, "titulo"))}</span>'
                       f'<span class="em-modo modo-1">{esc(titulo_site(sec["titulo"]))}</span></h1></header>'
                       '<div class="pilha em-modo modo-0 modo-2">'
                       f'<section class="ext">{ext_html(slug, "resumo", prefixo)}</section>'
                       + figura(f"familia-{slug}", prefixo) + "".join(bloco_familia(c_) for c_ in e if c_ not in ("titulo", "resumo")) + "</div>")
        outras = [(ext_texto(s2, "titulo"), f"../{s2}/") for _, s2 in FAMILIAS if s2 != slug and ext_texto(s2, "titulo")]
        fecho_familia = (saidas_html([("Seus direitos", f"{prefixo}direitos/"), ("Qual é o seu problema?", f"{prefixo}problemas/")] + outras)
                         + f'<section class="ext duvida">{botao_desnudar(True)}</section>')
        corpo = (f'<article class="folha leitura laboratorio">{externo}'
                 f'<div class="pilha doutrina em-modo modo-1 modo-2">{doutrina_html(f"familia {slug}", prefixo)}'
                 f'<p class="ler-pdf ciencia"><a href="{prefixo}tese/{sec["slug"]}/">Ler a seção no texto integral</a></p>'
                 + (f'<section class="bloco no-curso"><h2>Onde estudar a fundo?</h2><p>No <a href="{prefixo}doutrina/">curso para juristas</a>, que reconstrói o regime aplicado aqui.</p></section>' if CURSO else "")
                 + '</div>'
                 + fecho_familia + "</article>")
        jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": sec["titulo"], "inLanguage": "pt-BR",
                  "url": f"{BASE}/plataformas/{slug}/", "isBasedOn": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE}}
        destino = pasta / slug
        destino.mkdir(exist_ok=True)
        primeiro_txt = html.unescape(re.sub(r"<[^>]+>", " ", next((b["html"] for b in sec["blocos"] if b["tipo"] == "p"), "")))
        (destino / "index.html").write_text(
            pagina(f'{ext_texto(slug, "titulo") or sec["titulo"]} · Plataformas · Lex Plataformae', ext_texto(slug, "resumo") or resumo(re.sub(r"\bp\. \d+\b", " ", primeiro_txt)), corpo, prefixo, f"plataformas/{slug}/", jsonld, camada="mista", imagem=slug,
                   irmas=("As famílias de plataforma", [(esc(ext_texto(s2, "titulo")), f"../{s2}/", s2 == slug) for _, s2 in FAMILIAS if ext_texto(s2, "titulo")])),
            encoding="utf-8")
        cartoes.append(f'<li><a class="cartao" href="{slug}/"><span class="cartao-frase">{esc(ext_texto(slug, "titulo"))}</span><b>{esc(sec["titulo"])}</b></a></li>')

    # Os desdobramentos da tipologia, cada um em página própria, em texto integral.
    cartoes_desdob = []
    for num, slug in DESDOBRAMENTOS:
        sec = POR_NUMERO.get(num)
        if not sec:
            continue
        prefixo = "../../"
        corpo = ('<article class="folha leitura laboratorio">'
                 '<nav class="trilha" aria-label="Você está em"><a href="../">Plataformas</a></nav>'
                 f'<header class="folha-cabeca"><p class="sobrelinha">Desdobramento<span class="ciencia"> · {esc(sec["n"])} · p. {sec["pagina_inicio"]} a {sec["pagina_fim"]}</span></p>'
                 f'<h1>{titulo_por_modo(sec["titulo"])}</h1><p class="abertura-pagina">{esc(ABERTURA_DESDOBRAMENTO[slug])}</p>'
                 f'<p class="ler-pdf ciencia"><a href="{prefixo}tese/{sec["slug"]}/">Ler no texto integral, com as notas</a></p></header>'
                 + doutrina_html(f"desdobramento {slug}", prefixo)
                 + saidas_html([("As famílias de plataforma", "../"), ("O caminho do jurista", f"{prefixo}doutrina/"), ("As situações, para operar", f"{prefixo}roteiro/")])
                 + "</article>")
        jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": sec["titulo"], "inLanguage": "pt-BR",
                  "url": f"{BASE}/plataformas/{slug}/", "isBasedOn": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE}}
        destino = pasta / slug
        destino.mkdir(exist_ok=True)
        primeiro_txt = html.unescape(re.sub(r"<[^>]+>", " ", next((b["html"] for b in sec["blocos"] if b["tipo"] == "p"), "")))
        (destino / "index.html").write_text(
            pagina(f'{sec["titulo"]} · Plataformas · Lex Plataformae', resumo(re.sub(r"\bp\. \d+\b", " ", primeiro_txt)), corpo, prefixo, f"plataformas/{slug}/", jsonld, superficie="../",
                   irmas=("Os desdobramentos", [(titulo_por_modo(POR_NUMERO[n2]["titulo"]), f"../{s2}/", s2 == slug) for n2, s2 in DESDOBRAMENTOS if n2 in POR_NUMERO])),
            encoding="utf-8")
        cartoes_desdob.append(f'<li><a class="cartao" href="{slug}/"><b>{titulo_por_modo(sec["titulo"])}</b><span class="ciencia">{esc(sec["n"])} · p. {sec["pagina_inicio"]} a {sec["pagina_fim"]}</span></a></li>')

    origem = "".join(f'<li><a href="../tese/{POR_NUMERO[n]["slug"]}/">{esc(n)} {esc(POR_NUMERO[n]["titulo"])}</a></li>' for n in LABORATORIO_ORIGEM if n in POR_NUMERO)
    corpo = (
        '<article class="folha leitura laboratorio">'
        f'<header class="folha-cabeca ext-cabeca"><p class="sobrelinha-ext">Plataformas</p><h1><span class="em-modo modo-0 modo-2">{esc(ext_texto("laboratorio", "titulo"))}</span>'
        '<span class="em-modo modo-1">Plataformas</span></h1></header>'
        f'<div class="pilha em-modo modo-0 modo-2"><section class="ext">{ext_html("laboratorio", "abertura", "../")}</section>'
        + figura("laboratorio", "../") + "</div>"
        + f'<div class="pilha doutrina em-modo modo-1 modo-2">{doutrina_html("laboratorio abertura", "../")}</div>'
        + f'<section class="bloco"><h2>Quatro famílias de plataforma</h2><ul class="grade-conceitos">{"".join(cartoes)}</ul></section>'
        + (f'<section class="bloco interno"><h2>Desdobramentos</h2><ul class="grade-conceitos">{"".join(cartoes_desdob)}</ul></section>' if cartoes_desdob else "")
        + f'<div class="pilha doutrina em-modo modo-1 modo-2">{doutrina_html("laboratorio fecho", "../")}</div>'
        f'<section class="ext limite em-modo modo-0 modo-2"><p class="rotulo-ext">{esc(EXTERNA.get("laboratorio", {}).get("limite", {}).get("pergunta") or "Até onde vai")}</p>{ext_html("laboratorio", "limite", "../")}</section>'
        f'<section class="ext duvida">{botao_desnudar(True)}</section>'
        + (f'<section class="bloco ciencia" id="origem"><h2>O laboratório de origem</h2><p>A tipologia foi densificada num laboratório de origem, com recorte de aplicação ilustrativa. As seções abaixo o desenvolvem no texto integral.</p>{locus_html("../")}<ul class="lista-simples">{origem}</ul></section>' if origem else "")
        + "</article>")
    desc = "As famílias de plataforma em que a tese testa o regime do OIC, cada uma em quatro passos. Mecanismo, vulnerabilidade central, evidência e consequência dogmática possível."
    jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": "Laboratório · Lex Plataformae", "inLanguage": "pt-BR",
              "url": BASE + "/plataformas/", "isBasedOn": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE}}
    desc = ext_texto("laboratorio", "abertura") or desc
    (pasta / "index.html").write_text(pagina(f'{ext_texto("laboratorio", "titulo") or "Laboratório"} · Plataformas · Lex Plataformae', desc, corpo, "../", "plataformas/", jsonld, camada="mista", imagem="laboratorio"), encoding="utf-8")


def paragrafos(sec):
    """Blocos de texto da seção, cada um com a página em que começa e a página em que termina."""
    pagina_atual = sec["pagina_inicio"]
    saida = []
    for b in sec["blocos"]:
        marcas = [int(x) for x in re.findall(r'id="p(\d+)"', b["html"])]
        if b["tipo"] == "marca":
            pagina_atual = marcas[-1] if marcas else pagina_atual
            continue
        m = re.match(r'\s*<span class="pg-marca" id="p(\d+)"', b["html"])
        inicio = int(m.group(1)) if m else pagina_atual
        fim = marcas[-1] if marcas else inicio
        saida.append({"bloco": b, "inicio": inicio, "fim": fim,
                      "ref": f"p. {inicio}" if inicio == fim else f"p. {inicio}-{fim}"})
        pagina_atual = fim
    return saida


_REF_BLOCO = {}


def ref_bloco(b):
    """A página e o endereço de um bloco do corpus, pela marca de página que o precede."""
    if not _REF_BLOCO:
        for sec in SECOES:
            for par in paragrafos(sec):
                _REF_BLOCO[id(par["bloco"])] = (par["ref"], sec["slug"], par["inicio"])
    return _REF_BLOCO.get(id(b))


def attrs_ref(b, prefixo, ref=None):
    """Atributos que levam a página e o endereço ao balão de referência. A página só aparece em Ciência ou ao passar o mouse."""
    r = ref_bloco(b)
    if not r:
        return ""
    texto, slug, inicio = r
    if ref:
        texto = ref
        inicio = int(re.match(r"p\. (\d+)", ref).group(1))
    return f' data-ref="{esc(texto)}" data-alvo="{prefixo}tese/{slug}/#p{inicio}"'


def citado(par, sec, prefixo, html_trecho=None, classe="citacao"):
    """Um parágrafo da tese em citação, com a âncora da página que leva ao trecho exato."""
    h = html_trecho if html_trecho is not None else par["bloco"]["html"]
    # Na Ciência, o trecho vem precedido de uma frase do site que diz o que ele faz ali. Revisão de voz de 05/11/2026.
    inicio = _plano(h).strip()
    mediacao = next((s["paragrafos"][0] for s in DOUTRINA.get("ciencia", []) if inicio.startswith(s["titulo"])), "")
    frase = f'<p class="mediacao">{esc(mediacao)}</p>' if mediacao else ""
    return frase + f'<blockquote class="{classe}"><p>{html_do_corpus(h, sec["slug"], prefixo)} {pg(par["ref"], prefixo, _plano(h)[:90])}</p></blockquote>'


def ref_do_pedaco(h, inicio):
    marcas = [int(x) for x in re.findall(r'id="p(\d+)"', h)]
    m = re.match(r'\s*<span class="pg-marca" id="p(\d+)"', h)
    comeco = int(m.group(1)) if m else inicio
    fim = marcas[-1] if marcas else comeco
    return f"p. {comeco}" if comeco == fim else f"p. {comeco}-{fim}"


def paragrafo_por_inicio(sec, inicio):
    return next((p for p in paragrafos(sec) if _plano(p["bloco"]["html"]).strip().startswith(inicio)), None)


# Método. O capítulo 2, que a tese apresenta como os elementos que tornam a investigação auditável (p. 47).
METODO = ["2.1", "2.2", "2.3", "2.4", "2.4.1", "2.4.2", "2.4.3", "2.5", "2.6", "2.7"]
METODO_LIGACOES = {"2.3": ("O laboratório de origem", "plataformas/#origem"), "2.6": ("As epígrafes", "epigrafes/")}


def gerar_metodo():
    cap = POR_NUMERO.get("2")
    if not cap or not all(n in POR_NUMERO for n in METODO):
        return
    prefixo = "../"
    auditavel = paragrafo_por_inicio(cap, "Aqui são reunidos")
    objeto = paragrafo_por_inicio(cap, "Para manter controlável")
    camadas_info = paragrafo_por_inicio(POR_NUMERO["2.4"], "Para preservar proporcionalidade")
    itens = []
    for n in METODO:
        sec = POR_NUMERO[n]
        primeiro = next(iter(paragrafos(sec)), None)
        ligacao = ""
        if n in METODO_LIGACOES:
            rotulo, caminho = METODO_LIGACOES[n]
            ligacao = f' · <a href="{prefixo}{caminho}">{esc(rotulo)} no site</a>'
        nivel = n.count(".")
        itens.append(
            f'<li class="parte-metodo nivel-{nivel}" id="m{n.replace(".", "-")}">'
            f'<h3><span class="num">{esc(n)}</span> {esc(sec["titulo"])}</h3>'
            + (citado(primeiro, sec, prefixo) if primeiro else "")
            + f'<p class="ler-pdf"><a href="{prefixo}tese/{sec["slug"]}/">Ler a seção</a> · p. {sec["pagina_inicio"]} a {sec["pagina_fim"]}{ligacao}</p></li>')
    corpo = (
        '<article class="folha leitura metodo">'
        f'<header class="folha-cabeca"><p class="sobrelinha">Capítulo 2 da tese · p. {cap["pagina_inicio"]} a {POR_NUMERO["2.7"]["pagina_fim"]}</p><h1>Método</h1>'
        '<p class="abertura-pagina">Como a tese foi feita, para que cada passo possa ser refeito por quem lê. '
        'A página traz a distinção entre objeto e instrumentos e cada parte do protocolo de observação, pelo primeiro parágrafo da sua seção.</p>'
        + (citado(auditavel, cap, prefixo, classe="citacao") if auditavel else "")
        + f'<p class="ler-pdf"><a href="{prefixo}tese/{cap["slug"]}/">Ler a abertura do capítulo na tese</a></p></header>'
        + (f'<section class="bloco"><h2>Objeto e instrumentos</h2>{citado(objeto, cap, prefixo)}'
           f'<p class="nota-camada">Os autores que a tese mobiliza como instrumentos estão organizados em <a href="{prefixo}fundamentos/">Fundamentos</a>.</p></section>' if objeto else "")
        + '<section class="bloco"><h2>O protocolo</h2><p class="nota-camada">Cada parte do capítulo 2 aparece com o primeiro parágrafo da seção, na ordem da tese.</p>'
        + f'<ol class="lista-metodo">{"".join(itens)}</ol></section>'
        + (f'<section class="bloco"><h2>As três camadas de informação</h2>{citado(camadas_info, POR_NUMERO["2.4"], prefixo)}</section>' if camadas_info else "")
        + "</article>")
    desc = "O desenho metodológico e o protocolo de observação da tese, capítulo 2, em texto literal. Estratégia, recorte, fontes, procedimentos de leitura e limites."
    jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": "Método · Lex Plataformae", "inLanguage": "pt-BR",
              "url": BASE + "/metodo/", "isBasedOn": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE}}
    pasta = SAIDA / "metodo"
    pasta.mkdir(exist_ok=True)
    (pasta / "index.html").write_text(pagina("Método da pesquisa · Lex Plataformae", desc, corpo, prefixo, "metodo/", jsonld, camada="ciencia", superficie=prefixo), encoding="utf-8")


# Fundamentos. Os capítulos 3 e 4, organizados pelos conjuntos de autores e pelas funções que a abertura de cada capítulo declara.
# A contagem de citações é mecânica, pelo sobrenome no texto e nas notas de cada seção.
AUTORES = [
    ("Jacques Ellul", r"\bEllul\b", "ELLUL"), ("Neil Postman", r"\bPostman\b", "POSTMAN"),
    ("Willem H. Vanderburg", r"\bVanderburg\b", "VANDERBURG"), ("Andrew Feenberg", r"\bFeenberg\b", "FEENBERG"),
    ("Yanis Varoufakis", r"\bVaroufakis\b", "VAROUFAKIS"), ("Ladislau Dowbor", r"\bDowbor\b", "DOWBOR"),
    ("Karl Marx", r"\bMarx\b", "MARX"), ("Mary Douglas", r"\bDouglas\b", "DOUGLAS"),
    ("Baron Isherwood", r"\bIsherwood\b", "ISHERWOOD"), ("Arjun Appadurai", r"\bAppadurai\b", "APPADURAI"),
    ("Igor Kopytoff", r"\bKopytoff\b", "KOPYTOFF"), ("Grant McCraken", r"\bMcCrac?ken\b", "MCCRACKEN"),
    ("Umberto Eco", r"\bEco\b", "ECO"), ("Guy Debord", r"\bDebord\b", "DEBORD"),
    ("Jean Baudrillard", r"\bBaudrillard\b", "BAUDRILLARD"), ("Julie E. Cohen", r"\bCohen\b", "COHEN"),
    ("Luis Alberto Warat", r"\bWarat\b", "WARAT"), ("Maurizio Gnerre", r"\bGnerre\b", "GNERRE"),
    ("Samuel D. Warren II", r"\bWarren\b", "WARREN"), ("Louis D. Brandeis", r"\bBrandeis\b", "BRANDEIS"),
    ("Byung-Chul Han", r"\bHan\b", "HAN"), ("Eros Roberto Grau", r"\bGrau\b", "GRAU"),
]
# Onde começa cada conjunto ou eixo na abertura do capítulo. No capítulo 3 a tese os chama de conjuntos.
EIXOS = {
    "3": {"abertura": ["O consumo digital", "Essa ambiência"], "lema": "Para descrever esse pano de fundo",
          "eixos": [("Da técnica ao ambiente de vida", "O primeiro reconstrói"), ("A economia política das plataformas", "O segundo conjunto"),
                    ("Da economia política à semiótica do consumo", "O terceiro conjunto")],
          "fecho": ["Desse percurso resulta"]},
    "4": {"abertura": ["A ordem econômica tecno-midiática"], "lema": None,
          "eixos": [(None, "Para tornar esse regime cognoscível"), (None, "Esse plano semiótico"), (None, "A assimetria que interessa"), (None, "O problema jurídico se adensa")],
          "fecho": ["Nesse contexto, a assimetria", "O objetivo, aqui"]},
}


def contar(padrao, slug):
    """Ocorrências do padrão no texto e nas notas da seção."""
    return len(re.findall(padrao, TEXTO_SECAO[slug])) + sum(len(re.findall(padrao, t)) for _, _, t in NOTAS_SECAO[slug])


def citacoes_do_autor(padrao):
    """Seções em que o sobrenome aparece, no texto ou nas notas, na ordem da tese."""
    return [(sec, n) for sec in SECOES if sec["slug"] != "referencias" for n in [contar(padrao, sec["slug"])] if n]


def referencias_do_autor(chave):
    ref = next((s for s in SECOES if s["slug"] == "referencias"), None)
    if not ref:
        return []
    padrao = re.compile(rf"^{re.escape(chave)},|; {re.escape(chave)},")
    return [b["html"] for b in ref["blocos"] if b["tipo"] == "p" and padrao.search(_plano(b["html"]).strip())]


def autores_no_trecho(texto, lista=None):
    lista = AUTORES if lista is None else lista
    achados = [(texto.find(nome), nome, padrao, chave) for nome, padrao, chave in lista if nome in texto]
    return [(nome, padrao, chave) for _, nome, padrao, chave in sorted(achados)]


def html_autor(nome, padrao, chave, prefixo):
    """Um autor nomeado na abertura de capítulo, com as seções que o citam e as obras na lista de referências."""
    onde = citacoes_do_autor(padrao)
    lista_onde = ", ".join(f'<a href="{prefixo}tese/{s["slug"]}/">{esc(s["n"] or s["titulo"].capitalize())}</a> <span class="vezes">{n}×</span>' for s, n in onde)
    refs = "".join(f"<li>{h_ref}</li>" for h_ref in referencias_do_autor(chave))
    return (f'<div class="autor"><dt>{esc(nome)}</dt><dd><p class="onde"><span class="sobrelinha">Onde aparece no texto integral</span> {lista_onde}</p>'
            + (f'<ul class="refs" aria-label="Obras de {esc(nome)} na lista de referências">{refs}</ul>' if refs else "") + "</dd></div>")


def fichas_html(conc, prefixo):
    saida = ""
    for tipo, rotulo in (("conceito", "Nos conceitos"), ("roteiro", "Nos parâmetros"), ("bens", "Bens protegidos")):
        deste = [c for c in conc if c["tipo"] == tipo]
        if deste:
            saida += (f'<span class="cita"><span class="sobrelinha">{rotulo}</span> '
                      + ", ".join(f'<a href="{prefixo}conceitos/{c["id"]}/">{nome_html(c)}</a>' for c in em_ordem(deste)) + "</span>")
    return saida


def lista_secoes(num, prefixo, por_secao, autores, nota, extra=None):
    """As seções de um capítulo, com os autores da abertura que cada uma cita e as fichas que apontam para ela."""
    itens = []
    for sec in SECOES:
        if not (sec["n"] or "").startswith(num + "."):
            continue
        cont = sorted(((contar(padrao, sec["slug"]), nome) for nome, padrao, _ in autores), key=lambda x: -x[0])
        cont = [(n, nome) for n, nome in cont if n >= 2]
        cita = (f'<span class="cita"><span class="sobrelinha">Cita</span> ' + ", ".join(f'{esc(nome)} <span class="vezes">{n}×</span>' for n, nome in cont[:4]) + "</span>") if cont else ""
        mais = extra(sec) if extra else ""
        itens.append(f'<li class="nivel-{sec["n"].count(".")}"><a href="{prefixo}tese/{sec["slug"]}/"><span class="num">{esc(sec["n"])}</span> <span class="tit">{esc(sec["titulo"])}</span></a>'
                     f'<span class="pag">p. {sec["pagina_inicio"]} a {sec["pagina_fim"]}</span>{cita}{fichas_html(por_secao.get(sec["slug"], []), prefixo)}{mais}</li>')
    return (f'<nav class="secoes-cap" aria-label="Seções do capítulo {num}"><h3>As seções do capítulo</h3>'
            f'<p class="nota-camada">{nota}</p><ol>{"".join(itens)}</ol></nav>')


def gerar_fundamentos():
    if not all(n in POR_NUMERO for n in EIXOS):
        return
    prefixo = "../"
    por_secao = conceitos_por_secao()
    nao_exegese = paragrafo_por_inicio(POR_NUMERO["2"], "Nessa chave, a opção por uma abordagem não exegética")
    blocos_cap, mencionados = [], []
    for num, conf in EIXOS.items():
        cap = POR_NUMERO[num]
        pars = paragrafos(cap)
        abertura = "".join(citado(p, cap, prefixo) for inicio in conf["abertura"] for p in pars if _plano(p["bloco"]["html"]).strip().startswith(inicio))
        lema = ""
        cartoes = []
        for i, (rotulo, inicio) in enumerate(conf["eixos"]):
            par = next((p for p in pars if inicio in _plano(p["bloco"]["html"])), None)
            if not par:
                continue
            h = par["bloco"]["html"]
            if conf["lema"] and _plano(h).strip().startswith(conf["lema"]):
                corte = h.find(inicio)
                antes = h[:corte].strip()
                lema = citado({**par, "ref": ref_do_pedaco(antes, par["inicio"])}, cap, prefixo, antes)
                h = h[corte:]
                par = {**par, "ref": ref_do_pedaco(h, par["inicio"])}
            autores = autores_no_trecho(_plano(h))
            mencionados += [nome for nome, _, _ in autores]
            linhas = [html_autor(nome, padrao, chave, prefixo) for nome, padrao, chave in autores]
            titulo = rotulo or " · ".join(nome for nome, _, _ in autores)
            cartoes.append(f'<article class="eixo" id="eixo-{num}-{i + 1}" data-arq="abertura do capítulo {num} · texto literal e contagem mecânica">'
                           f'<h3>{esc(titulo)}</h3>{citado(par, cap, prefixo, h)}<dl class="autores">{"".join(linhas)}</dl></article>')
        fecho = "".join(citado(p, cap, prefixo) for inicio in conf["fecho"] for p in pars if _plano(p["bloco"]["html"]).strip().startswith(inicio))
        blocos_cap.append(
            f'<section class="bloco capitulo-fund" id="cap-{num}" aria-labelledby="titulo-cap-{num}">'
            f'<p class="sobrelinha">Capítulo {num} · p. {cap["pagina_inicio"]} a {cap["pagina_fim"]}</p>'
            f'<h2 id="titulo-cap-{num}"><a href="{prefixo}tese/{cap["slug"]}/">{esc(cap["titulo"])}</a></h2>'
            f'<div class="abertura-cap">{abertura}{lema}</div>'
            f'<div class="eixos">{"".join(cartoes)}</div>'
            f'<div class="fecho-cap">{fecho}</div>'
            + lista_secoes(num, prefixo, por_secao, AUTORES, "Autores da abertura citados ao menos duas vezes na seção, pela contagem do sobrenome, e fichas do site que apontam a seção como lugar do conceito.")
            + "</section>")
    indice = "".join(f'<li><a href="#cap-{n}">Capítulo {n} · {esc(POR_NUMERO[n]["titulo"])}</a></li>' for n in EIXOS)
    corpo = (
        '<article class="folha leitura fundamentos">'
        '<header class="folha-cabeca"><p class="sobrelinha">Capítulos 3 e 4 da tese</p><h1>Fundamentos</h1>'
        + f'<p class="abertura-pagina">Cada capítulo abre declarando os autores que mobiliza e a função de cada um. A página segue essa declaração, em texto literal. A distinção entre objeto e instrumentos está no <a href="{prefixo}metodo/">Método</a>.</p>'
        + (citado(nao_exegese, POR_NUMERO["2"], prefixo, classe="citacao") if nao_exegese else "")
        + f'<nav class="indice-roteiro" aria-label="Capítulos"><ol>{indice}</ol></nav></header>'
        + "".join(blocos_cap) + "</article>")
    desc = "Os capítulos 3 e 4 da tese, organizados pelos autores e funções que a abertura de cada capítulo declara, com as seções em que cada autor é citado e as obras da lista de referências."
    jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": "Fundamentos · Lex Plataformae", "inLanguage": "pt-BR",
              "url": BASE + "/fundamentos/", "isBasedOn": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE},
              "mentions": [{"@type": "Person", "name": nome} for nome in dict.fromkeys(mencionados)]}
    pasta = SAIDA / "fundamentos"
    pasta.mkdir(exist_ok=True)
    (pasta / "index.html").write_text(pagina("Fundamentos teóricos · Lex Plataformae", desc, corpo, prefixo, "fundamentos/", jsonld, camada="ciencia", superficie=prefixo), encoding="utf-8")


# Dispositivos. Artigos que a tese cita com o nome da lei na mesma frase. Remissões sem o nome da lei ficam de fora.
_DIPLOMA = (r"(?P<dip>CDC|Código de Defesa do Consumidor|Constituição(?: Federal| da República(?: Federativa do Brasil)?)?(?: de 1988)?"
            r"|Código Civil(?: de 2002)?|Código de Processo Civil|CPC|Lei n[ºo°]\.? ?[\d.]+/\d{4}|Decreto n[ºo°]\.? ?[\d.]+/\d{4})")
_NUM = r"\d+(?:-[A-Z])?\.?[ºo°]?"
_DET = (r"(?:\s*,?\s*(?:§\s*\d+\.?[ºo°]?|parágrafo único|caput|incisos?\s+[IVXLC]+(?:\s*(?:,|e|a)\s*[IVXLC]+)*"
        r"|[IVXLC]+\b(?:\s*(?:,|e|a)\s*[IVXLC]+\b)*|alínea\s+[a-z]))*")
PADRAO_DISPOSITIVO = re.compile(rf"\b(?:arts?\.|artigos?)\s*(?P<nums>{_NUM}(?:\s*(?:,|e|a)\s*{_NUM})*)(?P<det>{_DET})\s*,?\s*(?:d[oa]s?\s+|n[oa]s?\s+)?{_DIPLOMA}")
DIPLOMAS = [(r"CDC|Código de Defesa", "CDC", "Código de Defesa do Consumidor"), (r"Constituição", "Constituição", "Constituição Federal"),
            (r"Código Civil", "Código Civil", "Código Civil"), (r"CPC|Código de Processo", "CPC", "Código de Processo Civil")]


def _diploma(d):
    for padrao, curto, longo in DIPLOMAS:
        if re.match(padrao, d):
            return curto, longo
    d = re.sub(r"n[ºo°]\.? ?", "nº ", d)
    return d, d


_DISPOSITIVOS = {}


def dispositivos():
    """Para cada seção, os dispositivos citados. E o índice por lei e por artigo, com as seções."""
    if _DISPOSITIVOS:
        return _DISPOSITIVOS
    por_secao, indice = {}, {}
    for sec in SECOES:
        if sec["slug"] == "referencias":
            continue
        texto = TEXTO_SECAO[sec["slug"]] + " " + " ".join(t for _, _, t in NOTAS_SECAO[sec["slug"]])
        for m in PADRAO_DISPOSITIVO.finditer(texto):
            curto, longo = _diploma(m.group("dip"))
            det = re.sub(r"\s+", " ", re.sub(r"§\s*", "§ ", m.group("det"))).strip(" ,")
            nums = m.group("nums")
            if re.search(r"\sa\s", nums):
                itens = [(f"arts. {nums}", int(re.match(r"\d+", nums).group()), "")]
            else:
                lista = [x for x in re.split(r"\s*(?:,|\se\s)\s*", nums) if x]
                itens = [(f"art. {x}" + (f", {det}" if det and len(lista) == 1 else ""), int(re.match(r"\d+", x).group()), det if len(lista) == 1 else "") for x in lista]
            for rotulo, numero, d in itens:
                por_secao.setdefault(sec["slug"], {}).setdefault((curto, rotulo), 0)
                por_secao[sec["slug"]][(curto, rotulo)] += 1
                artigos = indice.setdefault(longo, {})
                artigos.setdefault((numero, d, rotulo), {}).setdefault(sec["slug"], 0)
                artigos[(numero, d, rotulo)][sec["slug"]] += 1
    _DISPOSITIVOS.update({"secao": por_secao, "indice": indice})
    return _DISPOSITIVOS


def dispositivos_da_secao_html(sec):
    d = dispositivos()["secao"].get(sec["slug"])
    if not d:
        return ""
    return ('<span class="cita"><span class="sobrelinha">Dispositivos</span> '
            + ", ".join(f'{esc(curto)}, {esc(rotulo)}' + (f' <span class="vezes">{n}×</span>' if n > 1 else "") for (curto, rotulo), n in d.items()) + "</span>")


# A lei na tela do técnico. Decisão do autor de 27/10/2026. Os artigos aparecem com o texto integral em rodapé,
# para que o técnico não precise abrir a lei. O texto vem das transcrições que a própria tese faz em nota,
# levantadas em estrutura/inventario-dispositivos-transcritos.json, e, para o que a tese cita sem transcrever,
# do site do Planalto, em estrutura/dispositivos-planalto.json, com data e marca de acréscimo posterior.
LEIS_ABNT = {
    "Brasil, [2022]": ("CDC", "Código de Defesa do Consumidor", "Lei nº 8.078, de 11 de setembro de 1990"),
    "Brasil, [2025]a": ("Constituição", "Constituição Federal", "Constituição da República Federativa do Brasil de 1988"),
    "Brasil, [2024]a": ("Código Civil", "Código Civil", "Lei nº 10.406, de 10 de janeiro de 2002"),
    "Brasil, [2025]b": ("CPC", "Código de Processo Civil", "Lei nº 13.105, de 16 de março de 2015"),
    "Brasil, [2026]a": ("Lei nº 13.709/2018", "Lei Geral de Proteção de Dados", "Lei nº 13.709, de 14 de agosto de 2018"),
    "Brasil, [2024]b": ("Lei nº 14.852/2024", "Marco legal da indústria de jogos eletrônicos", "Lei nº 14.852, de 3 de maio de 2024"),
    "Brasil, [2025]c": ("Lei nº 15.211/2025", "Estatuto Digital da Criança e do Adolescente", "Lei nº 15.211, de 17 de setembro de 2025"),
    "Brasil, [2025]d": ("Decreto nº 12.622/2025", "Decreto da autoridade de proteção de crianças e adolescentes em ambientes digitais", "Decreto nº 12.622, de 17 de setembro de 2025"),
    "Brasil, [2024]c": ("Lei nº 9.279/1996", "Lei de Propriedade Industrial", "Lei nº 9.279, de 14 de maio de 1996"),
    "Brasil, [2021]": ("Lei nº 9.610/1998", "Lei de Direitos Autorais", "Lei nº 9.610, de 19 de fevereiro de 1998"),
    "Brasil, [1998]": ("Lei nº 9.609/1998", "Lei do Software", "Lei nº 9.609, de 19 de fevereiro de 1998"),
}
ORDEM_LEIS = ["CDC", "Constituição", "Código Civil", "CPC", "Lei nº 13.709/2018", "Lei nº 14.852/2024", "Lei nº 15.211/2025",
              "Decreto nº 12.622/2025", "Lei nº 9.279/1996", "Lei nº 9.610/1998", "Lei nº 9.609/1998"]
NOME_LEI = {curto: (nome, oficial) for curto, nome, oficial in LEIS_ABNT.values()}
# Notas que transcrevem um dispositivo sem trazer o número do artigo no próprio trecho.
ARTIGO_DA_NOTA = {"484": 5, "710": 54}
# Notas que transcrevem um artigo sem constar do inventário, porque o trecho não começa por "Art.". A 488 traz o caput do art. 1º do CDC.
NOTAS_EXTRAS = {"488": ("Brasil, [2022]", 1)}
_LEIS = {}


def _texto_cru(h):
    h = re.sub(r'<sup class="nota-ref">.*?</sup>', "", h)
    h = re.sub(r'<span class="pg-marca"[^>]*>.*?</span>', " ", h)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h))).strip()


def leis():
    """Texto de cada artigo, por lei e número. Cada entrada traz as transcrições da tese e, se houver, o texto do Planalto."""
    if _LEIS:
        return _LEIS
    inv = json.loads((RAIZ / "estrutura" / "inventario-dispositivos-transcritos.json").read_text(encoding="utf-8"))
    notas = {str(n["n"]): (sec, n) for sec in SECOES for n in sec["notas"]}
    extras = [[POR_SLUG[next(sl for sl, ns in NOTAS_SECAO.items() if any(str(x[0]) == n for x in ns))]["n"], n, None, [str(a)], [chave], ""]
              for n, (chave, a) in NOTAS_EXTRAS.items()]
    for secao, nota, pagina_, arts, chaves, _ in inv + extras:
        chave = chaves[0] if chaves else "Brasil, [2022]"
        curto = LEIS_ABNT[chave][0]
        sec, n = notas[str(nota)]
        texto = _texto_cru(n["html"])
        trechos = re.findall(r"“([^”]+)”", texto)
        numeros = [int(a) for a in arts] or ([ARTIGO_DA_NOTA[str(nota)]] if str(nota) in ARTIGO_DA_NOTA else [])
        for a in numeros:
            proprios = [t for t in trechos if re.match(rf"\s*Art\. {a}\b", t)] or trechos
            for t in proprios:
                _LEIS.setdefault((curto, a), {"tese": [], "planalto": None})["tese"].append(
                    {"texto": t.strip(), "nota": str(nota), "pagina": n["pagina"], "slug": sec["slug"]})
    arq = RAIZ / "estrutura" / "dispositivos-planalto.json"
    if arq.exists():
        mapa = {"CDC": "CDC", "CF": "Constituição", "CC": "Código Civil"}
        dados = json.loads(arq.read_text(encoding="utf-8"))
        for d in dados["dispositivos"]:
            curto = mapa[d["sigla"]]
            inicio = int(re.match(r"\d+", d["artigo"]).group())
            _LEIS.setdefault((curto, inicio), {"tese": [], "planalto": None})["planalto"] = {
                "texto": d["texto"], "fonte": d["fonte"], "consulta": dados["consulta"], "artigo": d["artigo"]}
    return _LEIS


def texto_do_artigo(curto, numero, det=""):
    """O texto a mostrar para um artigo. Prefere a transcrição da tese que traz o inciso ou parágrafo citado, e senão a mais longa."""
    e = leis().get((curto, numero))
    if not e:
        return None
    if e["tese"]:
        partes = [x.strip() for x in re.split(r",", det) if x.strip()]

        def cobre(t):
            for parte in partes:
                m = re.match(r"§\s*(\d+)", parte)
                if m and not re.search(rf"§\s*{m.group(1)}\s*[º°o.]", t["texto"]):
                    return False
                m = re.match(r"(?:incisos?\s+)?([IVXLC]+)$", parte)
                if m and not re.search(rf"\b{m.group(1)}\s*[-–]", t["texto"]):
                    return False
            return True
        candidatos = [t for t in e["tese"] if cobre(t)] or e["tese"]
        return {"tipo": "tese", **max(candidatos, key=lambda t: len(t["texto"]))}
    if e["planalto"]:
        return {"tipo": "planalto", **e["planalto"]}
    return None


def html_texto_lei(t, prefixo):
    if t["tipo"] == "tese":
        return (f'<blockquote class="lei-texto" data-ref="p. {t["pagina"]}" data-alvo="{prefixo}tese/{t["slug"]}/#n{t["nota"]}"><p>“{esc(t["texto"])}”</p></blockquote>'
                f'<p class="lei-fonte ciencia">Na redação que a tese transcreve na nota {esc(t["nota"])}, p. {t["pagina"]}.</p>')
    linhas = "".join(f"<p>{esc(l)}</p>" for l in t["texto"])
    return (f'<blockquote class="lei-texto planalto">{linhas}</blockquote>'
            f'<p class="lei-fonte acrescimo">Texto em vigor copiado do <a href="{esc(t["fonte"])}" rel="noopener">site do Planalto</a> em 27/10/2026. Acréscimo posterior, fora da tese.</p>')


class _Leis:
    """Registro das notas de lei de uma página. Cada artigo citado ganha um número e o texto integral no rodapé."""

    def __init__(self, prefixo):
        self.prefixo, self.itens, self.chaves = prefixo, [], {}

    def nota(self, rotulo, artigos):
        norma = re.sub(r"\s+", " ", re.sub(r"§\s*", "§ ", rotulo.replace("Código de Defesa do Consumidor", "CDC"))).strip().lower()
        chave = (norma, tuple(t.get("nota") or t.get("artigo") for t in artigos))
        if chave not in self.chaves:
            self.itens.append((rotulo, artigos))
            self.chaves[chave] = len(self.itens)
        return self.chaves[chave]

    def html(self):
        if not self.itens:
            return ""
        lis = []
        for i, (rotulo, artigos) in enumerate(self.itens, 1):
            corpo = "".join(html_texto_lei(t, self.prefixo) for t in artigos)
            lis.append(f'<li id="lei-{i}"><p class="lei-rotulo">{esc(rotulo)} <a class="volta" href="#lei-r-{i}" aria-label="Voltar ao texto">↩</a></p>{corpo}</li>')
        return ('<section class="leis-pagina interno" aria-labelledby="leis-titulo"><h2 id="leis-titulo">A lei citada nesta página</h2>'
                f'<ol>{"".join(lis)}</ol></section>')


# Onde cada artigo aparece no site, para que a Legislação leve de volta às páginas que o usam. Auditoria de 04/11/2026.
LEI_USOS = {}
PAGINA_ATUAL = [None]


def com_lei(corpo, prefixo):
    """Acrescenta a nota de lei a cada artigo citado com o nome da lei na mesma frase, fora de links e scripts."""
    registro = _Leis(prefixo)
    pedacos = re.split(r"(<[^>]+>)", corpo)
    fora = 0
    usados = set()
    salta = ("script", "style", "a", "sup", "title", "h1", "h2", "h3", "figcaption")
    for i, pedaco in enumerate(pedacos):
        if pedaco.startswith("<"):
            m = re.match(r"<(/?)([a-zA-Z0-9]+)", pedaco)
            if m and m.group(2).lower() in salta and not pedaco.endswith("/>"):
                fora = max(0, fora + (-1 if m.group(1) else 1))
            continue
        if fora or "art" not in pedaco:
            continue

        def troca(m):
            curto, _ = _diploma(m.group("dip"))
            nums = m.group("nums")
            det = re.sub(r"\s+", " ", re.sub(r"§\s*", "§ ", m.group("det"))).strip(" ,")
            if re.search(r"\sa\s", nums):
                numeros = [int(re.match(r"\d+", nums).group())]
            else:
                numeros = [int(re.match(r"\d+", x).group()) for x in re.split(r"\s*(?:,|\se\s)\s*", nums) if x and re.match(r"\d+", x)]
            textos = [t for t in (texto_do_artigo(curto, n, det if len(numeros) == 1 else "") for n in numeros) if t]
            if not textos:
                return m.group(0)
            if PAGINA_ATUAL[0]:
                caminho_atual, titulo_atual, camada_atual = PAGINA_ATUAL[0]
                for n in numeros:
                    LEI_USOS.setdefault((curto, n), {}).setdefault(caminho_atual, (titulo_atual, camada_atual))
            rotulo = re.sub(r"\s+", " ", m.group(0)).strip()
            k = registro.nota(rotulo, textos)
            ident = f"lei-r-{k}" if k not in usados else ""
            usados.add(k)
            return m.group(0) + f'<sup class="lei-ref interno"><a href="#lei-{k}"{f" id={chr(34)}{ident}{chr(34)}" if ident else ""}>{k}</a></sup>'
        pedacos[i] = PADRAO_DISPOSITIVO.sub(troca, pedaco)
    novo = "".join(pedacos)
    rodape = registro.html()
    if not rodape:
        return corpo
    corte = novo.rfind("</article>")
    return novo[:corte] + rodape + novo[corte:] if corte >= 0 else novo + rodape


def gerar_legislacao():
    """A página de legislação do técnico. Cada artigo que a tese transcreve ou cita, com o texto integral, por lei."""
    prefixo = "../"
    dados = leis()
    indice = dispositivos()["indice"]
    longo_para_curto = {"Código de Defesa do Consumidor": "CDC", "Constituição Federal": "Constituição", "Código Civil": "Código Civil", "Código de Processo Civil": "CPC"}
    citado_em = {}
    for longo, artigos in indice.items():
        curto = longo_para_curto.get(longo, longo)
        for (numero, _, _), secs in artigos.items():
            citado_em.setdefault((curto, numero), set()).update(secs)
    for (curto, numero), e in dados.items():
        for t in e["tese"]:
            citado_em.setdefault((curto, numero), set()).add(t["slug"])
    grupos, nav = [], []
    for curto in ORDEM_LEIS:
        numeros = sorted(n for c, n in dados if c == curto)
        if not numeros:
            continue
        nome, oficial = NOME_LEI[curto]
        ancora_lei = "lei-" + re.sub(r"[^a-z0-9]+", "-", curto.lower()).strip("-")
        itens = []
        for n in numeros:
            e = dados[(curto, n)]
            rotulo = f"arts. {e['planalto']['artigo']}" if e["planalto"] and " a " in e["planalto"]["artigo"] else f"art. {n}{'º' if n < 10 else ''}"
            textos = []
            vistos = set()
            for t in sorted(e["tese"], key=lambda t: -len(t["texto"])):
                if t["texto"] in vistos or any(t["texto"] in v for v in vistos):
                    continue
                vistos.add(t["texto"])
                textos.append(html_texto_lei({"tipo": "tese", **t}, prefixo))
            if e["planalto"]:
                textos.append(html_texto_lei({"tipo": "planalto", **e["planalto"]}, prefixo))
            secs = sorted(citado_em.get((curto, n), []), key=lambda slug: SECOES.index(POR_SLUG[slug]))
            onde = ", ".join(f'<a href="{prefixo}tese/{slug}/">{esc(POR_SLUG[slug]["n"] or POR_SLUG[slug]["titulo"].capitalize())}</a>' for slug in secs)
            usos = LEI_USOS.get((curto, n), {})
            publicos = [f'<a href="{prefixo}{c}">{esc(t)}</a>' for c, (t, cam) in sorted(usos.items(), key=lambda x: x[1][0]) if cam != "ciencia"]
            estudo = [f'<a href="{prefixo}{c}">{esc(t)}</a>' for c, (t, cam) in sorted(usos.items(), key=lambda x: x[1][0]) if cam == "ciencia"]
            aparece = ""
            if publicos:
                aparece = ('<p class="lei-usos">Aparece em ' + ", ".join(publicos[:8])
                           + ("" if not estudo else f'<span class="ciencia">, {", ".join(estudo[:6])}</span>') + ".</p>")
            elif estudo:
                aparece = f'<p class="lei-usos ciencia">Aparece em {", ".join(estudo[:6])}.</p>'
            itens.append(f'<li class="artigo-lei" id="{ancora_lei}-{n}"><h3>{esc(rotulo)}</h3>{"".join(textos)}{aparece}'
                         + (f'<p class="lei-fonte ciencia">Citado em {onde}.</p>' if onde else "") + "</li>")
        nav.append(f'<li><a href="#{ancora_lei}">{esc(nome)}</a></li>')
        grupos.append(f'<section class="bloco lei-grupo" id="{ancora_lei}" aria-labelledby="{ancora_lei}-titulo">'
                      f'<h2 id="{ancora_lei}-titulo">{esc(nome)}</h2><p class="lei-oficial">{esc(oficial)}</p><ol class="artigos-lei">{"".join(itens)}</ol></section>')
    corpo = ('<article class="folha leitura legislacao">'
             '<header class="folha-cabeca"><p class="sobrelinha">Para operar</p><h1>Legislação</h1>'
             '<p class="abertura-pagina">Os artigos de lei que aparecem nas situações, nas diretrizes e nas plataformas, com o texto integral, para não precisar abrir a lei. '
             'Cada artigo leva de volta às páginas em que é usado.</p></header>'
             f'<nav class="bloco indice-roteiro" aria-label="Leis"><h2>Por lei</h2><ol>{"".join(nav)}</ol></nav>'
             + "".join(grupos)
             + saidas_html([("As situações, para operar", f"{prefixo}roteiro/"), ("As diretrizes de controle", f"{prefixo}roteiro/diretrizes/"),
                            ("Seus direitos", f"{prefixo}direitos/")]) + "</article>")
    jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": "Legislação · Lex Plataformae", "inLanguage": "pt-BR",
              "url": BASE + "/legislacao/", "isBasedOn": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE},
              "mentions": [{"@type": "Legislation", "name": NOME_LEI[c][1]} for c in ORDEM_LEIS if any(k[0] == c for k in dados)]}
    pasta = SAIDA / "legislacao"
    pasta.mkdir(exist_ok=True)
    desc = "Os artigos de lei que a tese usa, com o texto integral, organizados por lei, para quem vai advogar."
    (pasta / "index.html").write_text(pagina("Legislação citada, com o texto integral dos artigos · Lex Plataformae", desc, corpo, prefixo, "legislacao/", jsonld, superficie=prefixo, lei=False), encoding="utf-8")


# Autores e referências. A lista de referências da tese entra no site como está, em Ciência, com a área de cada entrada.
# As citações do texto viram balões. Em Informação e Doutrina, os parênteses da referência dão lugar a um sinal discreto
# com o nome do autor, e a referência completa aparece ao passar o mouse ou tocar. Em Ciência, os parênteses ficam por extenso.
_MARCA_REF = r'<span class="pg-marca" id="p(\d+)"[^>]*>p\. \d+</span>'
_INICIO_ENTRADA = re.compile(r"^\s*(?:<strong>)?[A-Z0-9ÁÉÍÓÚÂÊÔÃÕÇÜ][A-Z0-9ÁÉÍÓÚÂÊÔÃÕÇÜ'’&\-\. ]*?[A-Z0-9ÁÉÍÓÚÂÊÔÃÕÇÜ…\.](?:</strong>)?[,.]")
AREA_INVENTARIO = {"Direito": "direito", "Economia política": "economia", "Técnica e mídia": "tecnica", "Antropologia do consumo": "antropologia",
                   "Semiótica e linguagem": "semiotica", "Poder e subjetividade": "poder", "Imprensa e comunidade (laboratório)": "laboratorio"}
# Autores que o inventário de 27/10/2026 não alcançou, porque a entrada vinha colada a outra na virada de página ou fora da caixa alta.
AREA_EXTRA = {"FREITAS": "direito", "BURAWOY": "laboratorio", "WILDE": "laboratorio"}
# Grafias da tese que divergem da lista de referências.
GRAFIAS = {"VICENT": "VINCENT", "MCCRAKEN": "MCCRACKEN"}
_REFS = []
_AUTORES = {}
ENTIDADES = {"BRASIL": "Brasil", "RIOT GAMES": "Riot Games", "LEAGUE OF LEGENDS WIKI": "League of Legends Wiki"}


def _chave_nome(t):
    t = re.sub(r"\s*(?:et al\.?|…|\.\.\.)\s*$", "", t.strip())
    t = t.upper().strip(" .,…")
    return GRAFIAS.get(t, t)


def _chave_titulo(t):
    """Entrada que começa pelo título é citada pela primeira palavra, como CRASHS… ou COMO…."""
    return _chave_nome(t.split()[0]) if t else t


# Erros de dado da lista de referências da tese, corrigidos no site com marca datada. Crítica de 09/11/2026.
CORRECOES_REFS = [("WARREN, Samuel D.; BRANDEIS, Louis D.", "[201-?]", "1890")]
DATA_CORRECOES_REFS = "09/11/2026"


def referencias():
    """As entradas da lista de referências da tese, na ordem e na forma da tese, separadas também quando a virada de página as colou."""
    if _REFS:
        return _REFS
    ref = POR_SLUG.get("referencias")
    if not ref:
        return _REFS
    inv = json.loads((RAIZ / "estrutura" / "inventario-autores.json").read_text(encoding="utf-8"))["autores"]
    area_sob = {_chave_nome(a["sob"]): AREA_INVENTARIO.get(a["area"], "laboratorio") for a in inv}
    nome_sob = {a["sob"]: a["nome"] for a in inv}
    pagina_ = ref["pagina_inicio"]
    for b in ref["blocos"]:
        pedacos = re.split(f"({_MARCA_REF})", b["html"])
        atual, i = None, 0
        while i < len(pedacos):
            p_ = pedacos[i]
            if re.fullmatch(_MARCA_REF, p_ or ""):
                pagina_ = int(pedacos[i + 1])
                seguinte = pedacos[i + 2] if i + 2 < len(pedacos) else ""
                if atual is not None and _texto_cru(atual["html"]).endswith(".") and _INICIO_ENTRADA.match(seguinte):
                    _REFS.append(atual)
                    atual = None
                elif atual is not None:
                    atual["html"] += p_
                i += 2
                continue
            if p_.strip():
                if atual is None:
                    atual = {"html": p_.strip(), "pagina": pagina_}
                else:
                    atual["html"] += p_
            i += 1
        if atual is not None:
            _REFS.append(atual)
    for n, e in enumerate(_REFS, 1):
        for inicio, errado, certo in CORRECOES_REFS:
            if _texto_cru(e["html"]).startswith(inicio) and errado in e["html"]:
                e["html"] = (e["html"].replace(errado, certo)
                             + f' <span class="nota-par">Correção posterior de {DATA_CORRECOES_REFS}. A lista da tese registra {esc(errado)}.</span>')
        t = _texto_cru(e["html"])
        e.update(n=n, texto=t, id=f"ref-{n}")
        m = re.match(r"^([A-Za-zÁÉÍÓÚÂÊÔÃÕÇÜáéíóúâêôãõçü'\-\. ]+?), (?=[A-ZÁÉÍÓÚ][a-zà-ú]|[A-Z]\.)", t)
        pessoa = bool(m) and not t.startswith(("BRASIL", "RIOT GAMES", "LEAGUE OF LEGENDS"))
        primeira_parte = re.match(r"^([^,.]+)", t).group(1)
        titulo_na_frente = not pessoa and primeira_parte != primeira_parte.upper()
        e["chave"] = _chave_nome(m.group(1)) if pessoa else (_chave_titulo(primeira_parte) if titulo_na_frente else _chave_nome(primeira_parte))
        e["pessoa"] = pessoa
        e["anos"] = {a + l for a, l in re.findall(r"\[?(\d{4}\??|\d{3}-\?)\]?([a-z]?)(?![\w])", t)} | {a + l for a, l in re.findall(r"\[?(\d{4}|\d{3}-\?)\]?([a-z]?)\b", t)} | {a for a, l in re.findall(r"\[?(\d{4}|\d{3}-\?)\]?([a-z]?)\b", t)}
        if pessoa:
            # O bloco dos autores termina no primeiro ponto que não fecha uma inicial, ou onde começa o título em negrito.
            negrito = len(_texto_cru(e["html"].split("<strong>")[0])) if "<strong>" in e["html"] else len(t)
            corte = next((mm.start() for mm in re.finditer(r"\. ", t) if not re.search(r"(?:\b[A-Z]|\bJR|\bJr)$", t[:mm.start()])), len(t))
            if negrito < corte:
                corte = t.rfind(".", 0, negrito + 1)
            # Prenome com mais de cinco palavras é sinal de que o título começou depois de uma inicial.
            ultimo = t[:corte].split(";")[-1]
            if "," in ultimo and len(ultimo.split(",", 1)[1].split()) > 5:
                base = len(t[:corte]) - len(ultimo)
                inicial = re.search(r"\b[A-Z]\.\s", ultimo.split(",", 1)[1])
                if inicial:
                    corte = base + len(ultimo.split(",", 1)[0]) + 1 + inicial.end() - 2
            bloco_autores, resto = t[:corte + 1], t[corte + 1:].strip()
            nomes = []
            for parte in re.split(r";\s*", re.sub(r"\s*\((?:org|coord|ed|orgs|coords|eds)\.\)", "", bloco_autores)):
                if "," in parte:
                    sob, dado = [x.strip() for x in parte.split(",", 1)]
                    dado = dado.rstrip(".") + ("." if re.search(r"\b[A-Z]\.?$", dado.rstrip(".")) else "")
                    etal = bool(re.search(r"\bet al\.?$", dado))
                    dado = re.sub(r"\s*\bet al\.?$", "", dado)
                    sob_ex = nome_sob.get(sob.upper()) or " ".join(w if w.lower() in ("de", "da", "do", "dos", "das", "e") else (w.capitalize() if not w.upper().startswith("JR") else "Jr.") for w in sob.lower().split())
                    nomes.append(f"{dado} {sob_ex}".strip() + (" et al." if etal else ""))
                elif parte.strip():
                    nomes.append(parte.strip())
            e["nomes"] = nomes
            titulo = re.split(r"\.\s+(?=In:|[A-Z0-9])", resto, maxsplit=1)[0].strip(" .")
            e["titulo"] = titulo
            e["area"] = area_sob.get(e["chave"]) or AREA_EXTRA.get(e["chave"], "laboratorio")
        else:
            e["nomes"] = []
            primeira, _, resto = t.partition(". ")
            entidade = primeira == primeira.upper()
            e["titulo"] = (resto.split(". ")[0] if entidade and resto else primeira).strip(" .")
            e["area"] = "direito" if t.startswith("BRASIL") else "laboratorio"
            e["entidade"] = ENTIDADES.get(e["chave"], primeira.strip(" .")) if entidade else ""
        e["autoria"] = ((" e ".join([", ".join(e["nomes"][:-1]), e["nomes"][-1]]) if len(e["nomes"]) > 1 else e["nomes"][0])
                        if e["nomes"] else e.get("entidade", ""))
    return _REFS


def slug_autor(nome):
    import unicodedata
    t = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def autores_pessoas():
    """Cada primeiro autor pessoa da lista, com as entradas, a área e a página própria."""
    if _AUTORES:
        return _AUTORES
    for e in referencias():
        if not e["pessoa"]:
            continue
        a = _AUTORES.setdefault(e["chave"], {"chave": e["chave"], "entradas": [], "area": e["area"]})
        a["entradas"].append(e)
    for a in _AUTORES.values():
        primeiro = a["entradas"][0]["nomes"][0] if a["entradas"][0]["nomes"] else a["chave"].title()
        a["nome"] = re.sub(r"\s+et al\.$", "", primeiro)
        a["slug"] = slug_autor(a["nome"])
        # O próprio autor da tese aparece por último, na página do autor, e não ganha página entre os autores citados.
        a["proprio"] = a["chave"] == "ANDRADE" and a["nome"].startswith("Victor")
    return _AUTORES


def _entrada_para(chave, ano):
    candidatas = [e for e in referencias() if e["chave"] == chave]
    if not candidatas:
        return None
    ano_limpo = ano.replace("[", "").replace("]", "")
    for e in candidatas:
        if ano_limpo in e["anos"] or ano in e["anos"]:
            return e
    if len(candidatas) == 1:
        return candidatas[0]
    # A lista da tese às vezes não traz a letra que a citação usa, como em [202-?]h. O balão fica com a fonte, sem arriscar o título.
    base = candidatas[0]
    return {**base, "titulo": "", "id": base["id"], "incerta": True}


_ANO = r"(?<![\w-])(?:\[?\d{4}\??\]?[a-z]?|\[\d{3}-\?\][a-z]?)"


def unidades_citacao(conteudo, nome_antes=None):
    """As citações dentro de um parêntese, cada uma com a entrada da lista que ela indica."""
    achados, pendentes = [], []
    for tok in re.split(r";\s*", conteudo):
        tok = tok.strip()
        if not tok:
            continue
        m = re.match(rf"^(.*?)(?:,\s*|\s+)?({_ANO})(?:,\s*(.*))?$", tok)
        if m and re.search(r"\d", m.group(2)):
            nomes = m.group(1).strip(" ,")
            if " apud " in nomes:
                nomes = nomes.split(" apud ")[-1]
            principal = (pendentes[0] if pendentes else re.split(r",\s*| e ", nomes)[0]) if (nomes or pendentes) else nome_antes
            if principal and " apud " in principal:
                principal = principal.split(" apud ")[-1]
            pendentes = []
            if not principal:
                continue
            e = _entrada_para(_chave_nome(principal), m.group(2))
            if e:
                achados.append({"entrada": e, "pagina": (m.group(3) or "").strip()})
            continue
        if re.match(r"^\[?p\.|^\d", tok) and achados:
            achados[-1]["pagina"] = (achados[-1]["pagina"] + "; " + tok).strip("; ")
            continue
        if re.match(r"^[A-ZÁÉÍÓÚ][\wÀ-ú'\-\. ]{1,40}$", tok):
            pendentes.append(tok)
    return achados


def _dados_cita(achados, prefixo):
    itens = []
    for a in achados:
        e = a["entrada"]
        autor = autores_pessoas().get(e["chave"]) if e["pessoa"] else None
        if autor and autor.get("proprio"):
            url = f"{prefixo}autor/"
        elif autor:
            url = f'{prefixo}autores/{autor["slug"]}/'
        else:
            url = f'{prefixo}referencias/#{e["id"]}'
        obra = ", ".join(x for x in (e["autoria"], e["titulo"]) if x)
        itens.append({"autoria": e["autoria"], "obra": obra, "pagina": a["pagina"], "url": url, "area": e["area"], "pessoa": bool(e["pessoa"])})
    return itens


_NOME = r"[A-ZÁÉÍÓÚ][\wÀ-ú\-]+(?: Jr\.)?"


def _nome_antes(antes):
    """Na citação narrativa, como Douglas e Isherwood (1996, p. xxiv), o autor vem antes do parêntese. Vale o primeiro nome."""
    mm = re.search(rf"({_NOME})(?:,\s*{_NOME})*(?:\s+e\s+{_NOME})?(?: et al\.)?\s*$", antes)
    return mm.group(1) if mm else None


def com_autores(corpo, prefixo):
    """Marca as citações do texto. Fora de links, scripts e títulos. A cada parêntese com referência resolvida, um balão."""
    pedacos = re.split(r"(<[^>]+>)", corpo)
    fora = 0
    salta = ("script", "style", "a", "title", "h1", "h2", "h3", "figcaption", "button", "label")
    for i, pedaco in enumerate(pedacos):
        if pedaco.startswith("<"):
            m = re.match(r"<(/?)([a-zA-Z0-9]+)", pedaco)
            if m and m.group(2).lower() in salta and not pedaco.endswith("/>"):
                fora = max(0, fora + (-1 if m.group(1) else 1))
            continue
        if fora or "(" not in pedaco:
            continue

        def troca(m):
            conteudo = m.group(1)
            if not re.search(r"\d{3}", conteudo):
                return m.group(0)
            antes = pedaco[max(0, m.start() - 60):m.start()]
            nome_antes = None
            if re.match(rf"^\s*{_ANO}", conteudo):
                nome_antes = _nome_antes(antes)
            achados = unidades_citacao(conteudo, nome_antes)
            if not achados:
                return m.group(0)
            itens = _dados_cita(achados, prefixo)
            dados = esc(json.dumps(itens, ensure_ascii=False))
            area = itens[0]["area"]
            estilo = f' style="--area:var(--a-{area});--area-t:var(--a-{area}-t)"'
            sinal = "" if nome_antes else (
                f'<span class="cita-sinal" data-cita="{dados}"{estilo} aria-hidden="true">'
                # Pessoa aparece pelo sobrenome. Empresa, órgão ou site aparece pelo nome inteiro, que é como a citação o chama.
                + esc(" · ".join(dict.fromkeys((re.sub(r"^.* ", "", i_["autoria"]) if i_["pessoa"] else i_["autoria"]) if i_["autoria"] else "fonte" for i_ in itens[:2])))
                + ("" if len(itens) <= 2 else f" +{len(itens) - 2}") + "</span>")
            return f'{sinal}<span class="cita-grupo" data-cita="{dados}"{estilo}>{m.group(0)}</span>'
        pedacos[i] = re.sub(r"\(([^()<>]{3,400})\)", troca, pedaco)
    return "".join(pedacos)


_CITACOES = []


def citacoes_do_corpus():
    """Cada citação resolvida do texto integral, com a frase em que aparece, a página e o endereço exato."""
    if _CITACOES:
        return _CITACOES
    marca = re.compile(r'<span class="pg-marca" id="p(\d+)"[^>]*>[^<]*</span>')
    fronteira = re.compile(r'(?<=[a-zà-ú\)”"\]])[.?!]\s+(?=[A-ZÁÉÍÓÚ“"])')

    def frases(texto):
        cortes = [0] + [m.end() for m in fronteira.finditer(texto)] + [len(texto)]
        return [(cortes[k], cortes[k + 1]) for k in range(len(cortes) - 1)]

    def registra(texto, paginas, sec, ancora_de):
        for m in re.finditer(r"\(([^()]{3,400})\)", texto):
            conteudo = m.group(1)
            if not re.search(r"\d{3}", conteudo):
                continue
            nome_antes = _nome_antes(texto[max(0, m.start() - 60):m.start()]) if re.match(rf"^\s*{_ANO}", conteudo) else None
            achados = unidades_citacao(conteudo, nome_antes)
            if not achados:
                continue
            ini, fim = next(((a, b) for a, b in frases(texto) if a <= m.start() < b), (0, len(texto)))
            pagina_ = next((pg_ for pos, pg_ in reversed(paginas) if pos <= ini), paginas[0][1] if paginas else sec["pagina_inicio"])
            pagina_fim = next((pg_ for pos, pg_ in reversed(paginas) if pos < fim), pagina_)
            ref = f"p. {pagina_}" if pagina_fim == pagina_ else f"p. {pagina_}-{pagina_fim}"
            for a in achados:
                _CITACOES.append({"entrada": a["entrada"]["id"], "chave": a["entrada"]["chave"], "pessoa": a["entrada"]["pessoa"],
                                  "frase": texto[ini:fim].strip(), "pagina": pagina_, "ref": ref, "slug": sec["slug"], "ancora": ancora_de(pagina_),
                                  "secao": sec["n"] or sec["titulo"]})

    for sec in SECOES:
        if sec["slug"] == "referencias":
            continue
        for b in sec["blocos"]:
            if b["tipo"] == "marca":
                continue
            r = ref_bloco(b)
            inicio = r[2] if r else sec["pagina_inicio"]
            h = re.sub(r'<sup class="nota-ref">.*?</sup>', "", b["html"])
            texto, paginas, pos = "", [(0, inicio)], 0
            for parte in re.split(r'(<span class="pg-marca" id="p\d+"[^>]*>[^<]*</span>)', h):
                mm = marca.match(parte)
                if mm:
                    paginas.append((len(texto), int(mm.group(1))))
                    continue
                texto += html.unescape(re.sub(r"<[^>]+>", "", parte))
            texto = re.sub(r"\s+", " ", texto)
            registra(texto, paginas, sec, lambda pg_: f"#p{pg_}")
        for n in sec["notas"]:
            registra(_texto_cru(n["html"]), [(0, n["pagina"])], sec, lambda pg_, n=n: f'#n{n["n"]}')
    return _CITACOES


ORDEM_AREAS = ["direito", "economia", "tecnica", "antropologia", "semiotica", "poder", "laboratorio"]


def chip_area(area):
    return f'<span class="chip-area"{estilo_area(area)}>{esc(AREA_NOME[area])}</span>'


def ficha_citacao(c, nome, area, prefixo, autoria=None, obra=None):
    """Um balão de autor em forma de ficha. O nome pequeno em cima, o trecho da tese e a página."""
    return (f'<figure class="ficha"{estilo_area(area)}>' + (f'<figcaption class="autor">{esc(nome)}</figcaption>' if nome else "") +
            f'<blockquote data-ref="{esc(c["ref"])}" data-alvo="{prefixo}tese/{c["slug"]}/{c["ancora"]}"><p>{esc(c["frase"])}</p></blockquote>'
            f'<p class="ref"><a href="{prefixo}tese/{c["slug"]}/{c["ancora"]}">{esc(c["ref"])} · {esc(c["secao"])}</a></p></figure>')


def gerar_autores():
    """As páginas de autor, em Ciência. Uma por primeiro autor pessoa da lista de referências, com as obras e cada trecho que o cita."""
    autores = autores_pessoas()
    cits = citacoes_do_corpus()
    por_chave = {}
    for c in cits:
        if c["pessoa"]:
            por_chave.setdefault(c["chave"], []).append(c)
    declarados = {chave: nome for nome, _, chave in AUTORES + AUTORES_5}
    raiz = SAIDA / "autores"
    raiz.mkdir(exist_ok=True)
    grupos = {}

    def mesma_area(autor):
        return sorted((x for x in autores.values() if x["area"] == autor["area"] and not x.get("proprio")), key=lambda x: x["nome"])

    for chave, a in autores.items():
        if a.get("proprio"):
            continue
        grupos.setdefault(a["area"], []).append(a)
        prefixo = "../../"
        lista = por_chave.get(chave, [])
        vistos, fichas, autorias = set(), [], []
        for c in lista:
            k = (c["frase"], c["slug"])
            if k in vistos:
                continue
            vistos.add(k)
            e = next(x for x in a["entradas"] if x["id"] == c["entrada"])
            autorias.append((c, e))
        # Na página do próprio autor, o nome no balão só aparece quando a autoria muda de uma obra para outra.
        varias = len({e["autoria"] for _, e in autorias}) > 1
        for c, e in autorias:
            nome_balao = e["autoria"] if varias and e["autoria"] != a["nome"] else None
            fichas.append(ficha_citacao(c, nome_balao, a["area"], prefixo, obra=", ".join(x for x in (e["autoria"], e["titulo"]) if x)))
        autoria_unica = autorias[0][1]["autoria"] if autorias and not varias and autorias[0][1]["autoria"] != a["nome"] else None
        obras = "".join(f'<li id="{e["id"]}">{html_do_corpus(e["html"], "referencias", prefixo)}</li>' for e in a["entradas"])
        declarado = ""
        papel = ""
        if chave in declarados or chave.replace(" JR", " JR.") in declarados:
            cap = "fundamentos/" if any(chave.startswith(k.rstrip(".")) for _, _, k in AUTORES) else "dogmatica/"
            declarado = f'<p class="nota-camada">A abertura de capítulo que declara a função deste autor está em <a href="{prefixo}{cap}">{"Fundamentos" if cap.startswith("f") else "Dogmática"}</a>.</p>'
            # O parágrafo de abertura de capítulo que nomeia o autor diz o papel dele no argumento.
            padrao_nome = next((pd for _, pd, k in AUTORES + AUTORES_5 if k.rstrip(".") == chave.rstrip(".") or k == chave.replace(" JR", " JR.")), None)
            for numero_cap in ("3", "4", "5"):
                sec_cap = POR_NUMERO.get(numero_cap)
                if not (sec_cap and padrao_nome) or papel:
                    continue
                for par in paragrafos(sec_cap):
                    if par["bloco"]["tipo"] == "p" and re.search(padrao_nome, _plano(par["bloco"]["html"])):
                        papel = (f'<section class="bloco"><h2>O papel no argumento</h2>{citado(par, sec_cap, prefixo)}</section>')
                        break
        por_secao = {}
        for c in lista:
            por_secao[c["slug"]] = por_secao.get(c["slug"], 0) + 1
        maiores = sorted(por_secao, key=lambda x: -por_secao[x])[:3]
        # A abertura é uma linha de dados, com o número de trechos, a área e as seções em que mais aparece. Uma frase de molde
        # repetida em noventa páginas soava como máquina. Revisão de rótulos de 05/11/2026.
        links_onde = [f'<a href="{prefixo}tese/{x}/" title="{esc(POR_SLUG[x]["titulo"])}">{esc(POR_SLUG[x]["n"] or POR_SLUG[x]["titulo"])}</a>' for x in maiores if x in POR_SLUG]
        onde = ", ".join(links_onde[:-1]) + (" e " if len(links_onde) > 1 else "") + (links_onde[-1] if links_onde else "")
        area_txt = "Fontes do objeto e do laboratório" if a["area"] == "laboratorio" else AREA_NOME.get(a["area"], a["area"])
        dados_autor = [f'{len(fichas)} {"trecho" if len(fichas) == 1 else "trechos"} na tese', esc(area_txt)]
        if onde:
            dados_autor.append(f'{"mais presente em" if len(maiores) > 1 else "em"} {onde}')
        abertura_autor = f'<p class="abertura-pagina dados-autor">{" · ".join(dados_autor)}</p>'
        corpo = (f'<article class="folha leitura autor-citado"{estilo_area(a["area"])}>'
                 f'<nav class="trilha" aria-label="Você está em"><a href="../">Autores</a></nav>'
                 f'<header class="folha-cabeca"><p class="sobrelinha">{chip_area(a["area"])}</p><h1>{esc(a["nome"])}</h1>{abertura_autor}{declarado}</header>'
                 + papel +
                 f'<section class="bloco"><h2>Na lista de referências</h2><ul class="refs-autor">{obras}</ul></section>'
                 f'<section class="bloco"><h2>Onde aparece no texto integral</h2><p class="nota-camada">Na ordem da tese{f", todos de {esc(autoria_unica)}" if autoria_unica else ""}.</p>'
                 f'<div class="fichas">{"".join(fichas)}</div></section></article>')
        jsonld = {"@context": "https://schema.org", "@type": "ProfilePage", "url": f'{BASE}/autores/{a["slug"]}/',
                  "mainEntity": {"@type": "Person", "name": a["nome"]}, "isPartOf": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE}}
        destino = raiz / a["slug"]
        destino.mkdir(parents=True, exist_ok=True)
        a["citacoes"] = len(fichas)
        (destino / "index.html").write_text(
            pagina(f'{a["nome"]} · Autores · Lex Plataformae', f'{a["nome"]} na tese. As obras da lista de referências e os {len(fichas)} trechos em que a tese o cita.',
                   corpo, prefixo, f'autores/{a["slug"]}/', jsonld, camada="ciencia", superficie=prefixo,
                   irmas=(f'Também em {area_txt}', [(esc(x["nome"]), f'../{x["slug"]}/', x is a) for x in mesma_area(a)])), encoding="utf-8")
    secoes = []
    for area in ORDEM_AREAS:
        lista = sorted(grupos.get(area, []), key=lambda a: -a.get("citacoes", 0))
        if not lista:
            continue
        itens = "".join(f'<li><a href="{a["slug"]}/">{esc(a["nome"])}</a> <span class="vezes">{a.get("citacoes", 0)}</span></li>' for a in lista)
        secoes.append(f'<section class="bloco area-autores"{estilo_area(area)}><h2>{esc(AREA_NOME[area])}</h2><ul class="lista-autores">{itens}</ul></section>')
    corpo = ('<article class="folha leitura autores-indice"><header class="folha-cabeca"><h1>Autores</h1>'
             '<p>Os autores da lista de referências, pela área em que a tese os mobiliza.</p></header>'
             + "".join(secoes) + "</article>")
    jsonld = {"@context": "https://schema.org", "@type": "CollectionPage", "url": BASE + "/autores/", "name": "Autores · Lex Plataformae"}
    (raiz / "index.html").write_text(pagina("Autores citados, por área · Lex Plataformae", "Os autores que a tese cita, por área, com os trechos em que aparecem.",
                                            corpo, "../", "autores/", jsonld, camada="ciencia", superficie="../"), encoding="utf-8")


def gerar_referencias():
    """A lista de referências da tese, como está, com a área e as citações de cada entrada. As ampliações do site ficam à parte, com data."""
    prefixo = "../"
    cont = {}
    for c in citacoes_do_corpus():
        cont[c["entrada"]] = cont.get(c["entrada"], 0) + 1
    autores = autores_pessoas()
    itens = []
    for e in referencias():
        autor = autores.get(e["chave"]) if e["pessoa"] else None
        destino = ""
        if autor and autor.get("proprio"):
            destino = f'<a href="{prefixo}autor/">Sobre o autor</a>'
        elif autor:
            destino = f'<a href="{prefixo}autores/{autor["slug"]}/">Página do autor</a>'
        n = cont.get(e["id"], 0)
        meta = f'{chip_area(e["area"])} <span class="vezes">{n} {"citação" if n == 1 else "citações"}</span> {destino}'
        itens.append(f'<li id="{e["id"]}"{estilo_area(e["area"])}><p class="entrada">{html_do_corpus(e["html"], "referencias", prefixo)}</p><p class="meta-ref">{meta}</p></li>')
    corpo = ('<article class="folha leitura referencias"><header class="folha-cabeca"><h1>Referências</h1>'
             f'<p>A lista de referências da tese, na ordem e na forma em que está no <a href="{prefixo}tese/referencias/">texto integral</a>, '
             'com a área de cada entrada e o número de vezes em que o texto a cita.</p></header>'
             f'<section class="bloco"><h2>A lista da tese</h2><ol class="lista-referencias">{"".join(itens)}</ol></section>'
             '<section class="bloco" id="ampliacoes"><h2>Ampliações</h2><p>O que o site acrescentar à teoria depois da tese entra aqui, com data e marca de acréscimo posterior. Por enquanto, nada.</p></section>'
             "</article>")
    jsonld = {"@context": "https://schema.org", "@type": "WebPage", "url": BASE + "/referencias/", "name": "Referências · Lex Plataformae",
              "isBasedOn": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE}}
    pasta = SAIDA / "referencias"
    pasta.mkdir(exist_ok=True)
    (pasta / "index.html").write_text(pagina("Referências bibliográficas · Lex Plataformae", "A lista de referências da tese, com a área de cada entrada e as citações.",
                                             corpo, prefixo, "referencias/", jsonld, camada="ciencia", superficie=prefixo), encoding="utf-8")


def gerar_objeto_instrumentos():
    """O movimento metodológico da tese entre objeto e instrumentos, em Ciência. O objeto sem cor, as lentes na cor de cada área,
    a qualificação no vermelho do Direito e os conceitos da tese no azul Klein."""
    prefixo = "../"
    cap = POR_NUMERO.get("2")
    if not cap:
        return
    trechos = "".join(citado(par, cap, prefixo) for inicio in ("Para manter controlável", "Quando um conceito é mobilizado")
                      for par in [paragrafo_por_inicio(cap, inicio)] if par)
    onde = {}
    for parte in PERCURSO:
        for b in parte["blocos"]:
            if b["tipo"] == "termo":
                onde.setdefault(b["arg"], parte)
    def termo_link(nome, classe=""):
        parte = onde.get(nome)
        alvo = f'{prefixo}caminho/{parte["slug"]}/#termo-{slug_derivado(nome)}' if parte else None
        rotulo = f'<span class="{classe}">{esc(nome)}</span>' if classe else esc(nome)
        return f'<li><a href="{alvo}">{rotulo}</a></li>' if alvo else f"<li>{rotulo}</li>"
    autores = [a for a in autores_pessoas().values() if not a.get("proprio")]
    cont = {}
    for c in citacoes_do_corpus():
        if c["pessoa"]:
            cont[c["chave"]] = cont.get(c["chave"], 0) + 1
    def autores_da_area(area, limite=12):
        lista = sorted((a for a in autores if a["area"] == area), key=lambda a: -cont.get(a["chave"], 0))[:limite]
        return "".join(f'<li><a href="{prefixo}autores/{a["slug"]}/">{esc(a["nome"])}</a></li>' for a in lista)
    lentes = []
    for area in ("tecnica", "economia", "antropologia", "semiotica", "poder"):
        termos = sorted(t for t, ar in AREA_TERMO.items() if ar == area)
        lentes.append(f'<section class="lente"{estilo_area(area)}><h3>{esc(AREA_NOME[area])}</h3>'
                      f'<p class="rotulo-ext">Instrumentos no caminho</p><ul class="termos-lista">{"".join(termo_link(t) for t in termos)}</ul>'
                      f'<p class="rotulo-ext">Autores</p><ul class="autores-lista">{autores_da_area(area)}</ul></section>')
    juridicos = sorted(t for t, ar in AREA_TERMO.items() if ar == "direito")
    nove = "".join(f'<li><a class="chapado" href="{prefixo}conceitos/{c["id"]}/">{nome_html(c)}</a></li>' for c in [EIXO] + em_ordem([x for x in conceitos_do_atlas() if x is not EIXO]))
    dez = "".join(f'<li><a href="{prefixo}{caminho_derivado(t)}"><span class="nome-derivado">{esc(t)}</span></a></li>' for t in sorted(DERIVADOS))
    corpo = (
        '<article class="folha leitura objeto-instrumentos">'
        '<header class="folha-cabeca"><h1>Objeto e instrumentos</h1>'
        '<p class="abertura-pagina">O movimento de método da tese, em uma página. O objeto é o regime da plataforma visto no laboratório, '
        'e cada área do conhecimento entra como lente para lê-lo, até chegar à qualificação jurídica.</p>' + ROTULO_LITERAL + trechos + '</header>'
        '<div class="movimento-geral" aria-label="O movimento">'
        f'<div{estilo_area("laboratorio")}><small>Objeto</small><b>O regime da plataforma, visto no laboratório</b></div>'
        '<div style="--area:var(--a-economia)"><small>Lente</small><b>A área que o lê</b></div>'
        f'<div{estilo_area("direito")}><small>Qualificação</small><b>A categoria jurídica</b></div>'
        '<div style="--area:var(--tese-linha)"><small>Tese</small><b>O conceito que a tese nomeia</b></div></div>'
        f'<section class="bloco etapa"{estilo_area("laboratorio")}><h2>O objeto</h2>'
        f'<p>O laboratório de origem e as famílias de plataforma estão em <a href="{prefixo}plataformas/">Plataformas</a>. '
        f'A palavra do próprio objeto que o caminho usa é</p><ul class="termos-lista">{termo_link("Nerf")}</ul>'
        f'<p class="rotulo-ext">Fontes do laboratório</p><ul class="autores-lista">{autores_da_area("laboratorio", 8)}</ul></section>'
        f'<section class="bloco etapa"><h2>As lentes</h2><div class="lentes">{"".join(lentes)}</div></section>'
        f'<section class="bloco etapa"{estilo_area("direito")}><h2>A qualificação</h2><p class="rotulo-ext">Categorias jurídicas no caminho</p>'
        f'<ul class="termos-lista">{"".join(termo_link(t) for t in juridicos)}</ul><p class="rotulo-ext">Autores</p><ul class="autores-lista">{autores_da_area("direito", 16)}</ul></section>'
        '<section class="bloco etapa tese-etapa"><h2>A tese</h2><p class="rotulo-ext">Os nove conceitos</p>'
        f'<ul class="conceitos-lista">{nove}</ul><p class="rotulo-ext">Os dez conceitos derivados</p><ul class="termos-lista">{dez}</ul></section>'
        "</article>")
    jsonld = {"@context": "https://schema.org", "@type": "WebPage", "url": BASE + "/objeto-e-instrumentos/", "name": "Objeto e instrumentos · Lex Plataformae",
              "isBasedOn": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE}}
    pasta = SAIDA / "objeto-e-instrumentos"
    pasta.mkdir(exist_ok=True)
    (pasta / "index.html").write_text(pagina("Objeto e instrumentos · Lex Plataformae", "O movimento da tese entre o objeto e as lentes de outras áreas, até a qualificação jurídica e os conceitos da tese.",
                                             corpo, prefixo, "objeto-e-instrumentos/", jsonld, camada="ciencia", superficie=prefixo), encoding="utf-8")


# Dogmática. Os capítulos 5 e 6, pela abertura de cada um. A do capítulo 5 nomeia autores e a função de cada um, como as dos capítulos 3 e 4.
DOGMATICA = ["5", "6"]
AUTORES_5 = [
    ("Rizzatto Nunes", r"\bNunes\b", "NUNES"), ("Karl Larenz", r"\bLarenz\b", "LARENZ"),
    ("Tércio Sampaio Ferraz Jr.", r"\bFerraz\b", "FERRAZ JR."), ("Humberto Ávila", r"\bÁvila\b", "ÁVILA"),
    ("Claudia Lima Marques", r"\bMarques\b", "MARQUES"), ("Ricardo Morishita Wada", r"\bWada\b", "WADA"),
    ("Miguel Reale", r"\bReale\b", "REALE"), ("Roberto Mangabeira Unger", r"\bUnger\b", "UNGER"),
]
ORDEM_DIPLOMAS = ["Código de Defesa do Consumidor", "Constituição Federal", "Código Civil", "Código de Processo Civil"]


def gerar_dogmatica():
    if not all(n in POR_NUMERO for n in DOGMATICA + ["2.2"]):
        return
    prefixo = "../"
    por_secao = conceitos_por_secao()
    base = paragrafo_por_inicio(POR_NUMERO["2.2"], "A base normativa mobilizada")
    blocos_cap, mencionados = [], []
    for num in DOGMATICA:
        cap = POR_NUMERO[num]
        partes = []
        for i, par in enumerate(paragrafos(cap)):
            t = _plano(par["bloco"]["html"])
            autores = autores_no_trecho(t, AUTORES_5)
            mencionados += [nome for nome, _, _ in autores]
            nomeados = nomeados_html(termos_em(t), prefixo)
            if autores:
                partes.append(f'<article class="eixo" id="eixo-{num}-{i + 1}" data-arq="abertura do capítulo {num} · texto literal e contagem mecânica">'
                              f'<h3>{esc(" · ".join(nome for nome, _, _ in autores))}</h3>{citado(par, cap, prefixo)}'
                              f'<dl class="autores">{"".join(html_autor(nome, padrao, chave, prefixo) for nome, padrao, chave in autores)}</dl>{nomeados}</article>')
            else:
                partes.append(f'<div class="paragrafo-anotado">{citado(par, cap, prefixo)}{nomeados}</div>')
        nota = ("Autores da abertura do capítulo 5 citados ao menos duas vezes na seção, pela contagem do sobrenome, fichas do site que apontam a seção "
                "como lugar do conceito e dispositivos citados com o nome da lei.")
        blocos_cap.append(
            f'<section class="bloco capitulo-fund" id="cap-{num}" aria-labelledby="titulo-cap-{num}">'
            f'<p class="sobrelinha">Capítulo {num} · p. {cap["pagina_inicio"]} a {cap["pagina_fim"]}</p>'
            f'<h2 id="titulo-cap-{num}"><a href="{prefixo}tese/{cap["slug"]}/">{esc(cap["titulo"])}</a></h2>'
            f'<div class="eixos">{"".join(partes)}</div>'
            + lista_secoes(num, prefixo, por_secao, AUTORES_5, nota, dispositivos_da_secao_html)
            + "</section>")
    # Índice dos dispositivos, em toda a tese.
    indice = dispositivos()["indice"]
    leis = sorted(indice, key=lambda l: (ORDEM_DIPLOMAS.index(l) if l in ORDEM_DIPLOMAS else len(ORDEM_DIPLOMAS), l))
    grupos = []
    for lei in leis:
        linhas = []
        for (numero, det, rotulo), secs in sorted(indice[lei].items(), key=lambda x: (x[0][0], x[0][1])):
            onde = ", ".join(f'<a href="{prefixo}tese/{slug}/">{esc(POR_SLUG[slug]["n"] or POR_SLUG[slug]["titulo"].capitalize())}</a>'
                             + (f' <span class="vezes">{n}×</span>' if n > 1 else "")
                             for slug, n in sorted(secs.items(), key=lambda x: SECOES.index(POR_SLUG[x[0]])))
            linhas.append(f'<li><span class="artigo">{esc(rotulo)}</span> <span class="onde">{onde}</span></li>')
        grupos.append(f'<div class="lei"><h3>{esc(lei)}</h3><ul class="artigos">{"".join(linhas)}</ul></div>')
    total = sum(n for lei in indice.values() for secs in lei.values() for n in secs.values())
    disp = (f'<section class="bloco dispositivos" id="dispositivos" data-arq="extração mecânica · artigo e lei na mesma frase">'
            f'<h2>Dispositivos citados</h2><p class="nota-camada">Os artigos que a tese cita com o nome da lei na mesma frase, em toda a tese, com as seções em que aparecem. '
            f'São {total} remissões a artigo. As remissões sem o nome da lei ficam de fora.</p>{"".join(grupos)}</section>')
    indice_cap = "".join(f'<li><a href="#cap-{n}">Capítulo {n} · {esc(POR_NUMERO[n]["titulo"])}</a></li>' for n in DOGMATICA) + '<li><a href="#dispositivos">Dispositivos citados</a></li>'
    corpo = (
        '<article class="folha leitura fundamentos dogmatica">'
        '<header class="folha-cabeca"><p class="sobrelinha">Capítulos 5 e 6 da tese</p><h1>Dogmática</h1>'
        + f'<p class="abertura-pagina">A página segue a abertura de cada capítulo, em texto literal. Os autores que a abertura do capítulo 5 nomeia aparecem com as seções que os citam e com as obras da lista de referências. Os conceitos de cada trecho levam ao <a href="{prefixo}conceitos/">vocabulário</a>.</p>'
        + (citado(base, POR_NUMERO["2.2"], prefixo) if base else "")
        + f'<nav class="indice-roteiro" aria-label="Partes da página"><ol>{indice_cap}</ol></nav></header>'
        + "".join(blocos_cap) + disp + "</article>")
    desc = "Os capítulos 5 e 6 da tese, pela abertura de cada um, com os autores declarados, os conceitos de cada trecho e o índice dos dispositivos legais citados."
    jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": "Dogmática · Lex Plataformae", "inLanguage": "pt-BR",
              "url": BASE + "/dogmatica/", "isBasedOn": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE},
              "mentions": [{"@type": "Person", "name": nome} for nome in dict.fromkeys(mencionados)]
              + [{"@type": "Legislation", "name": lei} for lei in leis]}
    pasta = SAIDA / "dogmatica"
    pasta.mkdir(exist_ok=True)
    (pasta / "index.html").write_text(pagina("Dogmática jurídica · Lex Plataformae", desc, corpo, prefixo, "dogmatica/", jsonld, camada="ciencia", superficie=prefixo), encoding="utf-8")


_NOMEACOES = {}


def nomeacoes():
    """Para cada conceito, as páginas das camadas em que a tese o nomeia, com a contagem mecânica."""
    if _NOMEACOES:
        return _NOMEACOES

    def anota(contagem, camada, rotulo, caminho, detalhe=None):
        for cid, n in contagem.items():
            _NOMEACOES.setdefault(cid, {}).setdefault(camada, []).append((rotulo, caminho, detalhe or f"{n}×"))

    d = diretrizes()
    if d:
        por_conceito = {}
        for n, ordinal, blocos in d["itens"]:
            for cid in termos_em(texto_de(blocos)):
                por_conceito.setdefault(cid, []).append(ordinal)
        for cid, ordinais in por_conceito.items():
            detalhe = (", ".join(ordinais[:-1]) + " e " + ordinais[-1] if len(ordinais) > 1 else ordinais[0]) + (" diretrizes" if len(ordinais) > 1 else " diretriz")
            anota({cid: 1}, "Roteiro", "Diretrizes de controle de arquitetura e governança", "roteiro/diretrizes/", detalhe)
    if POR_NUMERO.get("7.1.4"):
        anota(termos_em(texto_de(POR_NUMERO["7.1.4"]["blocos"])), "Roteiro", "Cidadania digital e limites ao poder privado", "roteiro/limites/")
    for num, slug in FAMILIAS:
        if num in POR_NUMERO:
            blocos = POR_NUMERO[num]["blocos"] + (POR_NUMERO["7.2.7.1"]["blocos"] if num == "7.2.7" and "7.2.7.1" in POR_NUMERO else [])
            anota(termos_em(texto_de(blocos)), "Laboratório", POR_NUMERO[num]["titulo"], f"plataformas/{slug}/")
    for num, slug in DESDOBRAMENTOS:
        if num in POR_NUMERO:
            anota(termos_em(texto_de(POR_NUMERO[num]["blocos"])), "Laboratório", POR_NUMERO[num]["titulo"], f"plataformas/{slug}/")
    return _NOMEACOES


def usos_por_secao():
    """Para cada seção da tese, as páginas das camadas que trazem o seu texto ou se ancoram nela."""
    usos = {}

    def junta(num, camada, rotulo, caminho):
        if num in POR_NUMERO:
            lista = usos.setdefault(POR_NUMERO[num]["slug"], [])
            if (camada, rotulo, caminho) not in lista:
                lista.append((camada, rotulo, caminho))

    junta("1", "A tese", "O plano da tese", "tese/#plano")
    junta("2", "Método", "Abertura do capítulo e objeto e instrumentos", "metodo/")
    junta("2", "Fundamentos", "O uso não exegético dos conceitos", "fundamentos/")
    for num in METODO:
        junta(num, "Método", "O protocolo", f"metodo/#m{num.replace('.', '-')}")
    junta("2.2", "Dogmática", "A base normativa", "dogmatica/")
    for cap in DOGMATICA:
        junta(cap, "Dogmática", f"Abertura do capítulo {cap}", f"dogmatica/#cap-{cap}")
        for sec in SECOES:
            if (sec["n"] or "").startswith(cap + "."):
                junta(sec["n"], "Dogmática", f"Seções do capítulo {cap}", f"dogmatica/#cap-{cap}")
    for slug in dispositivos()["secao"]:
        if POR_SLUG[slug]["n"]:
            junta(POR_SLUG[slug]["n"], "Dogmática", "Dispositivos citados", "dogmatica/#dispositivos")
    for cap in EIXOS:
        junta(cap, "Fundamentos", f"Abertura do capítulo {cap}", f"fundamentos/#cap-{cap}")
        for sec in SECOES:
            if (sec["n"] or "").startswith(cap + "."):
                junta(sec["n"], "Fundamentos", f"Seções do capítulo {cap}", f"fundamentos/#cap-{cap}")
    junta("1", "Laboratório", "O laboratório de origem", "plataformas/#origem")
    junta("2.6", "Epígrafes", "As nove epígrafes", "epigrafes/")
    junta("5.1.2.3", "Roteiro", "O portão de entrada", "roteiro/#isto-e-um-objeto-imaterial-de-consumo")
    junta("7.1", "Roteiro", "Partes do Roteiro", "roteiro/")
    junta("7.1.1", "Roteiro", "Por que a ordem importa", "roteiro/")
    for letra, (num, _) in ROTEIRO_MAPA.items():
        if num:
            junta(num, "Roteiro", f"Bloco {letra} do enquadramento", f"roteiro/#{letra}")
    junta("7.1.2", "Roteiro", "Os onze blocos de enquadramento", "roteiro/")
    junta("7.1", "Roteiro", "Parâmetros", "roteiro/parametros/")
    junta("7.1.1", "Roteiro", "Parâmetros", "roteiro/parametros/")
    for letra, (num, _) in ROTEIRO_MAPA.items():
        if num:
            junta(num, "Roteiro", "Parâmetros", f"roteiro/parametros/#parametro-{letra}")
    junta("7.1.3", "Roteiro", "As dez diretrizes de controle", "roteiro/diretrizes/")
    junta("7.1.4", "Roteiro", "Cidadania digital e limites", "roteiro/limites/")
    junta("7", "Laboratório", "O teste", "plataformas/")
    junta("7.2", "Laboratório", "A sequência de cada família", "plataformas/")
    for num, slug in FAMILIAS:
        if num in POR_NUMERO:
            junta(num, "Laboratório", "Família de plataforma", f"plataformas/{slug}/")
    junta("7.2.7.1", "Laboratório", "Subcaso da administração de confiança", "plataformas/administracao-de-confianca/#quando-o-rumor-entra-no-fornecimento")
    for num, slug in DESDOBRAMENTOS:
        junta(num, "Laboratório", "Desdobramento da tipologia", f"plataformas/{slug}/")
    junta("7.3", "Laboratório", "O que as famílias mostram", "plataformas/")
    for num in LABORATORIO_ORIGEM:
        junta(num, "Laboratório", "O laboratório de origem", "plataformas/#origem")
    for p in D["percursos"].values():
        alvo = destino_pagina(p["trecho"]["ref"], "", p["trecho"]["texto"])
        m = re.match(r"tese/([^/]+)/", alvo or "")
        if m:
            sec = next((s for s in SECOES if s["slug"] == m.group(1)), None)
            if sec and sec["n"]:
                junta(sec["n"], "Atlas", "Três leituras da tese", "conceitos/#leituras-titulo")
    return usos


def gerar_estilo():
    modelo = (RAIZ / "prototipo" / "modelo.html").read_text(encoding="utf-8")
    css = re.search(r"<style>(.*?)</style>", modelo, re.S).group(1)
    fontes = """@font-face { font-family: "Archivo"; font-style: normal; font-display: swap; font-weight: 100 900; font-stretch: 62% 125%; src: url(fontes/archivo-latin-wdth-normal.woff2) format("woff2"); }
@font-face { font-family: "Newsreader"; font-style: normal; font-display: swap; font-weight: 200 800; src: url(fontes/newsreader-latin-opsz-normal.woff2) format("woff2"); }
@font-face { font-family: "Newsreader"; font-style: italic; font-display: swap; font-weight: 200 800; src: url(fontes/newsreader-latin-opsz-italic.woff2) format("woff2"); }
@font-face { font-family: "IBM Plex Mono"; font-style: normal; font-display: swap; font-weight: 400; src: url(fontes/ibm-plex-mono-latin-400-normal.woff2) format("woff2"); }
@font-face { font-family: "IBM Plex Mono"; font-style: normal; font-display: swap; font-weight: 500; src: url(fontes/ibm-plex-mono-latin-500-normal.woff2) format("woff2"); }
/* Fontes sob a SIL Open Font License 1.1. Licenças em assets/fontes. */
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; }
img { max-width: 100%; }
"""
    extra = (RAIZ / "site" / "extra.css").read_text(encoding="utf-8")
    # As cores vêm de estrutura/cores.json, por ferramentas/cores/gerar_css.py, e entram por último.
    extra += "\n" + (RAIZ / "site" / "cores.css").read_text(encoding="utf-8")
    assets = SAIDA / "assets"
    (assets / "fontes").mkdir(parents=True, exist_ok=True)
    # O degrau Despir vale também sem JavaScript. body.desnudo passa a casar ainda com o terceiro degrau marcado.
    estilo = (fontes + css + "\n" + extra).replace("body.desnudo", ":is(body.desnudo, body:has(#nivel-2:checked))")
    (assets / "estilo.css").write_text(estilo, encoding="utf-8")
    for arq in (RAIZ / "ferramentas" / "fontes").iterdir():
        shutil.copy(arq, assets / "fontes" / arq.name)
    shutil.copy(RAIZ / "site" / "atlas.js", assets / "atlas.js")
    if ILUSTRACOES_DIR.exists():
        (assets / "ilustracoes").mkdir(exist_ok=True)
        for arq in ILUSTRACOES_DIR.iterdir():
            if arq.suffix in EXTENSOES:
                shutil.copy(arq, assets / "ilustracoes" / arq.name)
    if (RAIZ / "site" / "cartoes").exists():
        (assets / "cartoes").mkdir(exist_ok=True)
        for arq in (RAIZ / "site" / "cartoes").glob("*.png"):
            shutil.copy(arq, assets / "cartoes" / arq.name)


def gerar_auxiliares():
    (SAIDA / "CNAME").write_text("lexplataformae.com.br\n", encoding="utf-8")
    (SAIDA / ".nojekyll").write_text("", encoding="utf-8")
    (SAIDA / "robots.txt").write_text(
        "# O conteúdo deste site é para ser lido por pessoas, buscadores e modelos de IA.\n"
        "User-agent: *\nAllow: /\n\n"
        + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in ("GPTBot", "ClaudeBot", "Claude-Web", "anthropic-ai", "Google-Extended", "CCBot", "PerplexityBot", "Applebot-Extended"))
        + f"Sitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    urls = [BASE + "/conceitos/", BASE + "/doutrina/"] + [f'{BASE}/doutrina/{c["slug"]}/' for c in CURSO] + [BASE + "/instrumentos/", BASE + "/", BASE + "/caminho/", BASE + "/direitos/", BASE + "/problemas/", BASE + "/epigrafes/"] + ([BASE + "/como-reclamar/"] if COMO_RECLAMAR else []) + [f"{BASE}/problemas/{s}/" for s in PROBLEMAS] + [f'{BASE}/caminho/{parte["slug"]}/' for parte in PERCURSO] + [url_conceito(c["id"]) for c in D["conceitos"]] + [BASE + "/tese/"] + [f'{BASE}/tese/{x["slug"]}/' for x in SECOES] + [BASE + "/roteiro/", BASE + "/roteiro/parametros/", BASE + "/roteiro/diretrizes/", BASE + "/roteiro/limites/", BASE + "/plataformas/", BASE + "/fundamentos/", BASE + "/metodo/", BASE + "/dogmatica/", BASE + "/legislacao/", BASE + "/autores/", BASE + "/referencias/", BASE + "/objeto-e-instrumentos/", BASE + "/autor/", BASE + "/versoes/"] + [f'{BASE}/autores/{a["slug"]}/' for a in autores_pessoas().values() if not a.get("proprio")] + [f"{BASE}/plataformas/{slug}/" for _, slug in FAMILIAS + DESDOBRAMENTOS] + [f"{BASE}/{c}" for c in paginas_derivadas() if f"{BASE}/{c}" not in [url_conceito(x["id"]) for x in D["conceitos"]]]
    (SAIDA / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    linhas = [
        "# Lex Plataformae",
        "",
        "> Atlas do regime jurídico do Objeto Imaterial de Consumo (OIC) sob a Lex Plataformae, a partir da tese de doutorado "
        "de Victor Luiz Pereira de Andrade (Victor L. P. Andrade), UNESP, Franca, 2026. Toda citação do site é transcrição literal "
        "da tese, com a página indicada. Acréscimos posteriores à tese são marcados e datados.",
        "",
        "Os nove conceitos se articulam no regime do OIC. Nas palavras da tese, " + "“" + (lambda q: q["texto"] if q else "")(next((q for q in (campo(EIXO, "Como integra os demais") or {"citacoes": []})["citacoes"] if q["ref"] == "p. 719"), None)) + "” (p. 719)",
        "",
        "## Caminho",
        "",
        "A primeira vista do site conta a tese inteira a partir da compra de uma skin, em linguagem simples, com os trechos literais da tese por baixo de cada bloco.",
        "",
    ] + [f"- [{parte['titulo']}]({BASE}/caminho/{parte['slug']}/): {parte['resumo']}" for parte in PERCURSO] + [
        "",
        "## Seus direitos",
        "",
        f"- [Seus direitos]({BASE}/direitos/): o que a plataforma deve e o que o consumidor pode pedir, em linguagem simples, uma situação por bloco, com os trechos literais da tese por baixo.",
    ] + [f"- [{DIREITOS[l]['titulo']}]({BASE}/direitos/#{l})" for l in LETRAS_DIREITOS] + [
        "",
        "## Epígrafes musicais",
        "",
        f"- [Por que nove canções?]({BASE}/epigrafes/): o método das epígrafes, pela seção 2.6 da tese, com a função de cada uma e o que cada canção anuncia. Só no modo Ciência.",
        "",
        "## Por problema",
        "",
        f"- [Qual é o seu problema?]({BASE}/problemas/): problemas comuns de quem compra itens, contas e acessos digitais, cada um com os blocos do percurso e os direitos que se aplicam.",
    ] + [f"- [{p['titulo']}]({BASE}/problemas/{p['slug']}/)" for p in PROBLEMAS.values()] + [
        "",
        "## Conceitos",
        "",
    ]
    for c in [EIXO] + em_ordem([x for x in conceitos_do_atlas() if x is not EIXO]):
        can = canonica(c)
        linhas.append(f"- [{c['nome']}]({url_conceito(c['id'])}): {can['texto']} ({can['ref']})")
    linhas += ["", "## Conceitos complementares e instrumentais", "", f"- [Conceitos por área]({BASE}/instrumentos/): índice dos termos do percurso, com links para as explicações em contexto. Instrumentos e categorias jurídicas por área, derivados e vocabulário do objeto em grupos próprios."]
    linhas += ["", "## Conceitos derivados", "", "Dez conceitos que a tese nomeia ao lado dos nove, cada um com página própria na voz do site. Os trechos literais que os sustentam ficam à vista no modo Ciência."]
    linhas += [f"- [{t}]({BASE}/{caminho_derivado(t)})" for t in sorted(DERIVADOS)]
    linhas += ["", "## Situações", "", f"- [Situações]({BASE}/roteiro/): as onze situações do quadro do 7.1.2 da tese, com hipótese de incidência, dever de fornecimento, prova mínima, qualificação jurídica e consequência institucional, na voz do site. O texto literal fica à vista no modo Ciência.",
               f"- [Parâmetros]({BASE}/roteiro/parametros/): os dez enunciados operacionais do 7.1.1 da tese, em sequência, cada um ligado à situação do quadro que prepara, na voz do site, com o texto integral no modo Ciência.",
               f"- [Diretrizes de controle]({BASE}/roteiro/diretrizes/): as dez diretrizes do 7.1.3 para o controle de arquitetura e governança, na voz do site, com o texto integral no modo Ciência.",
               f"- [Cidadania digital e limites]({BASE}/roteiro/limites/): o 7.1.4, sobre os limites ao poder privado de plataforma, na voz do site, com o texto integral no modo Ciência."]
    linhas += ["", "## Plataformas", "", f"- [Plataformas]({BASE}/plataformas/): as famílias de plataforma em que a tese testa o regime do OIC, cada uma em quatro passos, na voz do site, com o texto integral no modo Ciência."]
    linhas += [f"- [{POR_NUMERO[n]['titulo']}]({BASE}/plataformas/{slug}/): seção {n} da tese" for n, slug in FAMILIAS if n in POR_NUMERO]
    linhas += [f"- [{POR_NUMERO[n]['titulo']}]({BASE}/plataformas/{slug}/): seção {n} da tese, desdobramento da tipologia" for n, slug in DESDOBRAMENTOS if n in POR_NUMERO]
    linhas += ["", "## Legislação", "", f"- [Legislação]({BASE}/legislacao/): os artigos de lei que a tese transcreve ou cita, com o texto integral, por lei. O que a tese cita sem transcrever vem do site do Planalto, com data e marca de acréscimo posterior."]
    linhas += ["", "## Método, fundamentos e dogmática", "",
               f"- [Dogmática]({BASE}/dogmatica/): os capítulos 5 e 6 da tese, pela abertura de cada um, com os autores declarados, os conceitos de cada trecho e o índice dos dispositivos legais citados com o nome da lei.",
               f"- [Fundamentos]({BASE}/fundamentos/): os capítulos 3 e 4 da tese, organizados pelos autores e funções que a abertura de cada capítulo declara, com as seções em que cada autor é citado e as obras da lista de referências.",
               f"- [Método]({BASE}/metodo/): o desenho metodológico e o protocolo de observação do capítulo 2, em texto literal."]
    linhas += ["", "## A tese, seção por seção", "", f"- [Sumário, resumo e plano da tese]({BASE}/tese/): texto integral da tese em HTML, com a página impressa marcada e as notas ao fim de cada seção."]
    linhas += [f"- [{rotulo_secao(x)}]({BASE}/tese/{x['slug']}/): p. {x['pagina_inicio']} a {x['pagina_fim']}" for x in SECOES]
    linhas += ["", "## Tese", "", f"- [Tese completa em PDF]({BASE}/tese/{PDF_NOME}): {TITULO_TESE}. Doutorado em Direito, UNESP, 2026.",
               f"- [Autor]({BASE}/autor/): Victor L. P. Andrade, a referência completa da tese e a trajetória do trabalho.",
               "", "## Dados", "", f"- [atlas.json]({BASE}/dados/atlas.json): conceitos, definições, critérios delimitadores, seções e leituras, em JSON.", ""]
    (SAIDA / "llms.txt").write_text("\n".join(linhas), encoding="utf-8")
    (SAIDA / "dados").mkdir(exist_ok=True)
    shutil.copy(RAIZ / "dados" / "atlas.json", SAIDA / "dados" / "atlas.json")
    shutil.copy(RAIZ / "dados" / "epigrafes.json", SAIDA / "dados" / "epigrafes.json")
    (SAIDA / "tese").mkdir(exist_ok=True)
    shutil.copy(RAIZ / "tese" / PDF_NOME, SAIDA / "tese" / PDF_NOME)
    corpo = ('<article class="folha"><header class="folha-cabeca"><p class="sobrelinha">Página não encontrada</p>'
             '<h1>Este endereço não existe</h1></header><p>A página que você procurou não está aqui, ou mudou de lugar. '
             '<a href="/">Volte ao começo</a> e siga pelo menu.</p></article>')
    (SAIDA / "404.html").write_text(pagina("Página não encontrada · Lex Plataformae", "Página não encontrada.", corpo, "/", "404.html", camada="externa"), encoding="utf-8")


# Perfis do autor, informados por ele em 27/10/2026. O ORCID fica para outro momento.
AUTOR_LATTES = "https://lattes.cnpq.br/3172009565979544"
AUTOR_LINKEDIN = "https://www.linkedin.com/in/victorlpandrade/"


def ocorrencias_do_nome(nome):
    """As seções do texto integral que usam o nome, no corpo e nas notas, com a contagem."""
    padrao = re.compile(re.escape(nome).replace(r"\ ", r"\s+").replace(r"\-", r"-\s*"), re.I)
    achados = []
    for sec in SECOES:
        n = len(padrao.findall(TEXTO_SECAO[sec["slug"]])) + sum(len(padrao.findall(t)) for _, _, t in NOTAS_SECAO[sec["slug"]])
        if n:
            achados.append((sec, n))
    return achados


PERGUNTA_TERMO = json.loads((RAIZ / "conteudo" / "perguntas-termos.json").read_text(encoding="utf-8"))


def gerar_instrumentos():
    """Índice de consulta por área, sem destacar as explicações do seu contexto."""
    prefixo = "../"
    termos = {}
    inventario = []
    for parte in PERCURSO:
        for bloco in parte["blocos"]:
            if bloco["tipo"] != "termo":
                continue
            nome = bloco["arg"]
            if nome not in AREA_TERMO and nome not in DERIVADOS:
                raise ValueError(f"Termo sem classificação de área ou derivação: {nome}")
            if not bloco["citacoes"] or not bloco["paragrafos"]:
                raise ValueError(f"Termo sem explicação ou fonte: {nome}")
            termos.setdefault(nome, []).append(parte)
            inventario.append({"nome": nome, "area": AREA_TERMO.get(nome), "derivado": nome in DERIVADOS,
                               "percurso": parte["slug"], "ancora": "termo-" + slug_derivado(nome),
                               "fontes": bloco["citacoes"]})
    def item(nome):
        # O link leva a pergunta que o próprio termo responde, e não o título da parte do caminho, que nem sempre fala dele.
        # Revisão dos botões-pergunta, por ordem do autor de 11/11/2026.
        pergunta_ = PERGUNTA_TERMO.get(nome)
        if not pergunta_:
            raise ValueError(f"Termo sem pergunta em conteudo/perguntas-termos.json: {nome}")
        links = "".join(f'<a href="{prefixo}caminho/{p["slug"]}/#termo-{slug_derivado(nome)}">{esc(pergunta_)}</a>' for p in termos[nome][:1])
        return f'<li><h3>{esc(nome)}</h3><p>{links}</p></li>'
    areas = [a for a in AREA_NOME if any(AREA_TERMO.get(n) == a for n in termos)]
    indice = "".join(f'<li{estilo_area(a)}><a class="chip-area" href="#{a}">{esc(AREA_NOME[a])}</a></li>' for a in areas)
    grupos = "".join(f'<section class="instrumentos-area" id="{a}"{estilo_area(a)}><h2>{esc(AREA_NOME[a])}</h2>'
                      f'<ul class="instrumentos-lista">{"".join(item(n) for n in sorted(termos) if AREA_TERMO.get(n) == a)}</ul></section>' for a in areas)
    derivados = "".join(item(n) for n in sorted(termos) if n in DERIVADOS)
    corpo = ('<article class="folha instrumentos-pagina"><header class="folha-cabeca"><h1><span class="em-modo modo-0">Palavras que vêm de outros campos</span>'
             '<span class="em-modo modo-1 modo-2">Conceitos por área do conhecimento</span></h1>'
             '<p>Escolha uma área e siga o link de cada conceito para ler a explicação no caminho da skin.</p></header>'
             f'<nav aria-label="Áreas dos conceitos"><ul class="instrumentos-indice">{indice}<li><a href="#derivados">Conceitos derivados</a></li></ul></nav>'
             + grupos + f'<section class="instrumentos-area derivados" id="derivados"><h2>Conceitos derivados</h2><ul class="instrumentos-lista">{derivados}</ul></section>'
             f'<nav class="acoes" aria-label="Outros caminhos"><a href="{prefixo}conceitos/">O vocabulário</a>'
             f'<a class="ciencia" href="{prefixo}objeto-e-instrumentos/">Objeto e instrumentos</a></nav></article>')
    pasta = SAIDA / "instrumentos"
    pasta.mkdir(exist_ok=True)
    (pasta / "index.html").write_text(pagina("Conceitos por área do conhecimento · Lex Plataformae",
        "Encontre os conceitos complementares, instrumentais e derivados e leia cada explicação no contexto do caminho da skin.",
        corpo, prefixo, "instrumentos/", camada="mista"), encoding="utf-8")
    (RAIZ / "estrutura" / "instrumentos-no-percurso.json").write_text(json.dumps(inventario, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def gerar_derivados():
    """Uma página para cada conceito derivado que a tese nomeia e que ainda não tem ficha.

    O texto da página é o literal da tese. A explicação simples fica no percurso, onde o termo aparece em contexto.
    """
    prefixo = "../../"
    onde = {}
    for parte in PERCURSO:
        for b in parte["blocos"]:
            if b["tipo"] == "termo" and b["arg"] in DERIVADOS:
                onde.setdefault(b["arg"], (parte, b))
    nomes = sorted(DERIVADOS)
    for nome in nomes:
        if nome in FICHA_DERIVADO or nome not in onde:
            continue
        slug = slug_derivado(nome)
        parte, bloco = onde[nome]
        no_percurso = f'{prefixo}caminho/{parte["slug"]}/#termo-{slug}'
        achados = ocorrencias_do_nome(nome)
        lista = "".join(f'<li><a href="{prefixo}tese/{sec["slug"]}/">{esc(rotulo_secao(sec))}</a> <span class="vezes">{n}×</span></li>' for sec, n in achados)
        corpo = (
            '<article class="folha leitura derivado-pagina">'
            f'<header class="folha-cabeca"><p class="sobrelinha">Conceito derivado<span class="ciencia"> · nomeado pela tese, ao lado dos nove</span></p>'
            f'<h1>{esc(nome)}</h1>'
            f'<p class="abertura-pagina">Em palavras simples, no caminho da skin. <a href="{no_percurso}">{esc(PERGUNTA_TERMO.get(nome, parte["titulo"]))}</a></p></header>'
            f'<div class="pilha doutrina">{doutrina_html(f"derivado {nome}", prefixo)}{no_curso_html(capitulo_curso(slug=CURSO_CONCEITO.get(slug)), prefixo)}</div>'
            + (f'<section class="bloco ciencia" data-arq="contagem mecânica do nome no corpo e nas notas"><h2>Onde o texto integral usa o nome</h2><ul class="secoes-lista">{lista}</ul></section>' if lista else "")
            + f'<p class="ver-nove"><a href="{prefixo}conceitos/">Os nove conceitos</a></p>'
            '</article>')
        url = f"{BASE}/{caminho_derivado(nome)}"
        com_nome = [q["texto"] for q in bloco["citacoes"] if nome.lower() in q["texto"].lower()]
        primeiro = (com_nome or [q["texto"] for q in bloco["citacoes"]] or [nome])[0]
        jsonld = {"@context": "https://schema.org", "@type": "DefinedTerm", "@id": url, "name": nome, "description": primeiro, "url": url,
                  "inLanguage": "pt-BR", "inDefinedTermSet": {"@type": "DefinedTermSet", "@id": BASE + "/#atlas", "name": "Atlas Lex Plataformae"},
                  "author": {"@type": "Person", "name": "Victor Luiz Pereira de Andrade"}}
        destino = SAIDA / "conceitos" / slug
        destino.mkdir(parents=True, exist_ok=True)
        (destino / "index.html").write_text(
            pagina(f"{nome} · Conceitos · Lex Plataformae", primeiro, corpo, prefixo, caminho_derivado(nome), jsonld,
                   superficie=f'{prefixo}caminho/{parte["slug"]}/',
                   irmas=("Os outros nove derivados", [(f'<span class="nome-derivado">{esc(t)}</span>', f'{prefixo}{caminho_derivado(t)}', False) for t in nomes if t != nome])), encoding="utf-8")


def paginas_derivadas():
    return sorted({caminho_derivado(t) for t in DERIVADOS})


def gerar_autor():
    """A camada mais interna. Quem chega aqui fica sabendo, por último, que tudo deriva de uma tese de doutorado."""
    prefixo = "../"
    corpo = (
        '<article class="folha autor-pagina">'
        '<header class="folha-cabeca ext-cabeca"><p class="sobrelinha-ext">Quem está por trás desta teoria</p><h1>Victor L. P. Andrade</h1></header>'
        '<section class="ext"><p>Tudo o que você leu neste site deriva de uma tese de doutorado em Direito, '
        'apresentada à Universidade Estadual Paulista e defendida em 30 de março de 2026, sob a orientação da Prof.ª Dr.ª Luciana Lopes Canavez.</p>'
        '<p class="referencia">ANDRADE, Victor Luiz Pereira de. <b>Do regime jurídico do Objeto Imaterial de Consumo (OIC) sob a Lex Plataformae</b>. '
        'A tutela da vulnerabilidade semiótica do consumidor à luz da ordem constitucional e econômica do Brasil. 2026. '
        'Tese (Doutorado em Direito). Universidade Estadual Paulista, Faculdade de Ciências Humanas e Sociais, Franca, 2026.</p>'
        f'<p class="acoes"><a class="botao" href="{prefixo}tese/{PDF_NOME}">Ler a tese completa em PDF</a> <a href="{prefixo}tese/">Ler seção por seção</a></p></section>'
        + doutrina_html("autor", prefixo)
        + '<section class="ext fim-percurso" aria-labelledby="fim-titulo"><h2 class="rotulo-ext" id="fim-titulo">Fim do caminho</h2>'
        f'<p>A trajetória acadêmica completa está no <a href="{AUTOR_LATTES}" rel="me noopener">Currículo Lattes</a>.</p>'
        '<p>Para conversar sobre esta teoria, o caminho é o LinkedIn.</p>'
        f'<p class="acoes"><a class="botao" href="{AUTOR_LINKEDIN}" rel="me noopener">Victor L. P. Andrade no LinkedIn</a></p></section>'
        + "</article>")
    jsonld = {"@context": "https://schema.org", "@type": "ProfilePage", "url": BASE + "/autor/",
              "mainEntity": {"@type": "Person", "name": "Victor Luiz Pereira de Andrade", "alternateName": "Victor L. P. Andrade",
                             "sameAs": [AUTOR_LATTES, AUTOR_LINKEDIN]},
              "about": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE}}
    pasta = SAIDA / "autor"
    pasta.mkdir(exist_ok=True)
    (pasta / "index.html").write_text(
        pagina("Victor L. P. Andrade · Lex Plataformae", "Sobre o autor. A tese de doutorado de onde vem tudo o que está no site.",
               corpo, prefixo, "autor/", jsonld, camada="externa", imagem="autor"), encoding="utf-8")


# Cobertura por modo. Cada citação dos textos de cada modo volta à seção da tese de onde vem.
FONTES_MODO = {
    "Informação": ["conteudo/percurso.md", "conteudo/camada-externa.md", "conteudo/direitos.md", "conteudo/problemas.md"],
    "Doutrina": ["conteudo/operar.md", "conceitos/ficha-canonica-v0.md", "conteudo/doutrina.md"],
}


def _norm_cob(t):
    t = unicodedata.normalize("NFC", t)
    for a, b in (("“", '"'), ("”", '"'), ("‘", "'"), ("’", "'"), ("\xad", "")):
        t = t.replace(a, b)
    t = re.sub(r'(?<=[A-Za-zÀ-úºª,;:"\.])\d{1,3}(?=[\s,\.;:])', "", t)
    return re.sub(r"\s+", " ", t).strip().lower()


def secao_da_citacao(texto, ref, textos):
    """A seção em que o trecho está. Procura o texto e, se não achar, usa a página."""
    pedacos = [f.strip() for f in re.split(r"\[\s*(?:\.\.\.|…)\s*\]", texto) if len(f.strip()) > 12]
    alvo = _norm_cob(max(pedacos, key=len) if pedacos else texto)[:70]
    achadas = [x for x in SECOES if alvo and alvo in textos[x["slug"]]]
    if not achadas:
        m = re.match(r"p\. (\d+)", ref or "")
        if m:
            pag = int(m.group(1))
            achadas = [x for x in SECOES if x["pagina_inicio"] <= pag <= x["pagina_fim"]]
    return max(achadas, key=lambda x: len(x["n"] or "")) if achadas else None


def cobertura_por_modo():
    textos = {x["slug"]: _norm_cob(TEXTO_SECAO[x["slug"]] + " " + " ".join(t for _, _, t in NOTAS_SECAO[x["slug"]])) for x in SECOES}
    contagem = {}
    for modo, arqs in FONTES_MODO.items():
        for arq in arqs:
            caminho = RAIZ / arq
            if not caminho.exists():
                continue
            for m in re.finditer(r"^>!? (.+?) \((p\. [\d\-]+|Resumo)\)\s*$", caminho.read_text(encoding="utf-8"), re.M):
                sec = secao_da_citacao(m.group(1), m.group(2), textos)
                if sec:
                    contagem.setdefault(sec["slug"], {}).setdefault(modo, 0)
                    contagem[sec["slug"]][modo] += 1
    # Seções que a Doutrina traz em texto integral.
    integral = set()
    return contagem, integral


def gerar_cobertura():
    """Escreve estrutura/cobertura.md, com o lugar de cada seção da tese nas camadas do site.
    O autor determinou em 27/10/2026 que tudo o que está na tese será trazido para a estrutura do site.
    Este mapa mostra o caminho percorrido e o que falta."""
    por_secao, usos = conceitos_por_secao(), usos_por_secao()
    por_modo, integral = cobertura_por_modo()
    linhas = ["# Cobertura da tese nas camadas do site", "",
              "Arquivo gerado por `ferramentas/gerar_site.py`. Não editar à mão.", "",
              "Toda seção está no corpus, em texto integral. Esta tabela mostra em que outras camadas cada seção já tem lugar. "
              "Seção sem camada ainda não foi trazida para a estrutura.", "",
              "As colunas Informação e Doutrina contam os trechos literais que os textos de cada modo condensam e que vêm da seção. "
              "Informação conta o percurso, as ideias e Seus direitos. Doutrina conta o Guia para operar e as fichas, e marca com integral "
              "as seções que a Doutrina traz inteiras, como as situações, as diretrizes e as plataformas.", "",
              "| Seção | Título | Páginas | Informação | Doutrina | Camadas |", "|---|---|---|---|---|---|"]
    com, sem = 0, []
    for sec in SECOES:
        if sec["slug"] == "referencias":
            continue
        camadas = []
        if por_secao.get(sec["slug"]):
            camadas.append("Fichas (" + ", ".join(c["nome"] for c in em_ordem(por_secao[sec["slug"]])) + ")")
        for camada, rotulo, _ in usos.get(sec["slug"], []):
            item = f"{camada} ({rotulo})"
            if item not in camadas:
                camadas.append(item)
        if camadas:
            com += 1
        else:
            sem.append(sec)
        titulo = sec["titulo"].replace("|", "/")
        pm = por_modo.get(sec["slug"], {})
        dout = "integral" if (sec["n"] or "") in integral else str(pm.get("Doutrina", 0))
        linhas.append(f'| {sec["n"] or "-"} | {titulo} | {sec["pagina_inicio"]} a {sec["pagina_fim"]} | {pm.get("Informação", 0)} | {dout} | {"; ".join(camadas) or "corpus apenas"} |')
    total = com + len(sem)
    sem_info = [x for x in SECOES if x["slug"] != "referencias" and not por_modo.get(x["slug"], {}).get("Informação")]
    sem_dout = [x for x in SECOES if x["slug"] != "referencias" and not por_modo.get(x["slug"], {}).get("Doutrina") and (x["n"] or "") not in integral]
    linhas[6:6] = [f"{com} de {total} seções já têm lugar em alguma camada. Faltam {len(sem)}.", "",
                   f"Na Informação, {total - len(sem_info)} de {total} seções têm algum trecho condensado. Na Doutrina, {total - len(sem_dout)} de {total}.", ""]
    (RAIZ / "estrutura").mkdir(exist_ok=True)
    (RAIZ / "estrutura" / "cobertura.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"Cobertura  {com} de {total} seções com lugar numa camada, {total - len(sem_info)} na Informação e {total - len(sem_dout)} na Doutrina")


# A fermata fecha cada parte do percurso, como suspensão antes da pergunta seguinte. Identidade de 10/11/2026.
FERMATA = ('<div class="fermata" aria-hidden="true"><svg viewBox="0 0 64 34" width="48" height="26">'
           '<path d="M4 30 A28 28 0 0 1 60 30" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>'
           '<circle cx="32" cy="24" r="4.2" fill="currentColor"/></svg></div>')

# Endereços antigos, renomeados em 10/11/2026 com o menu unificado. Cada um leva ao novo, para não quebrar link de fora.
ENDERECOS_ANTIGOS = {"curso": "doutrina", "laboratorio": "plataformas", "percurso": "caminho"}


def gerar_redirecionamentos():
    for velho, novo in ENDERECOS_ANTIGOS.items():
        for arq in (SAIDA / novo).rglob("index.html"):
            rel = arq.parent.relative_to(SAIDA / novo).as_posix()
            destino = f"/{novo}/" + (rel + "/" if rel != "." else "")
            alvo = SAIDA / velho / rel / "index.html"
            alvo.parent.mkdir(parents=True, exist_ok=True)
            alvo.write_text(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Mudou de endereço</title>'
                            f'<meta name="robots" content="noindex"><link rel="canonical" href="{BASE}{destino}">'
                            f'<meta http-equiv="refresh" content="0; url={destino}"></head>'
                            f'<body><p>Esta página mudou para <a href="{destino}">{BASE}{destino}</a>.</p></body></html>', encoding="utf-8")


def gerar_versoes():
    """O histórico das versões, na Ciência. Cada versão com data e o que mudou, para a evolução do site ficar à vista."""
    prefixo = "../"
    itens = "".join(f'<li><p><b>Versão {esc(v)}</b>, de {esc(d)}. {esc(t)}</p></li>' for v, d, t in reversed(VERSOES))
    corpo = ('<article class="folha">'
             '<header class="folha-cabeca"><p class="sobrelinha">Ciência</p><h1>Como o site mudou</h1></header>'
             '<section><p>O site cresce em público, e cada versão fica registrada com a data e o que mudou. '
             'A versão em vigor aparece no alto de cada página e na referência sugerida no rodapé.</p>'
             f'<ol class="versoes" reversed>{itens}</ol></section>'
             + saidas_html([("O texto integral", f"{prefixo}tese/"), ("O método", f"{prefixo}metodo/")])
             + '</article>')
    pasta = SAIDA / "versoes"
    pasta.mkdir(exist_ok=True)
    (pasta / "index.html").write_text(
        pagina("Histórico de versões do site · Lex Plataformae", "Cada versão do site, com a data e o que mudou.",
               corpo, prefixo, "versoes/", None, camada="ciencia", superficie=prefixo), encoding="utf-8")


def main():
    if SAIDA.exists():
        shutil.rmtree(SAIDA)
    SAIDA.mkdir()
    gerar_estilo()
    gerar_inicio()
    gerar_percurso()
    gerar_direitos()
    gerar_curso()
    gerar_problemas()
    gerar_como_reclamar()
    gerar_epigrafes()
    for c in D["conceitos"]:
        gerar_conceito(c)
    gerar_tese()
    gerar_roteiro()
    gerar_parametros()
    gerar_diretrizes()
    gerar_limites()
    gerar_laboratorio()
    gerar_fundamentos()
    gerar_metodo()
    gerar_dogmatica()
    gerar_autores()
    gerar_referencias()
    gerar_objeto_instrumentos()
    gerar_instrumentos()
    gerar_derivados()
    gerar_autor()
    gerar_legislacao()
    gerar_auxiliares()
    gerar_versoes()
    gerar_redirecionamentos()
    paginas = len(list(SAIDA.rglob("*.html")))
    print(f"{paginas} páginas geradas em docs/")
    prontas = sum(1 for i in ILUSTRACOES if arquivo_ilustracao(i))
    print(f"Ilustrações  {len(ILUSTRACOES)} previstas, {prontas} com arquivo, {len(ILUSTRACOES_USADAS)} com lugar no site")
    for i in sorted(set(ILUSTRACOES) - ILUSTRACOES_USADAS):
        print(f"Ilustração sem lugar no site  {i}")
    gerar_cobertura()
    # A versão inglesa sai das páginas portuguesas prontas, pela memória de tradução em traducao/. 10/11/2026.
    import subprocess, sys as _sys
    subprocess.run([_sys.executable, str(RAIZ / "ferramentas" / "en" / "gerar_en.py")], check=True)


if __name__ == "__main__":
    main()
