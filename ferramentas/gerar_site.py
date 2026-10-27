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
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "docs"
BASE = "https://lexplataformae.com.br"
REPO = "https://github.com/victorlpandradeadv-creator/lexplataformae"
VERSAO = "0.7"
PDF_NOME = "andrade-2026-tese-oic-lex-plataformae.pdf"

D = json.loads((RAIZ / "dados" / "atlas.json").read_text(encoding="utf-8"))
_corpus = RAIZ / "dados" / "corpus.json"
C = json.loads(_corpus.read_text(encoding="utf-8")) if _corpus.exists() else {"secoes": []}
SECOES = C["secoes"]
POR_NUMERO = {s["n"]: s for s in SECOES if s["n"]}
POR_SLUG = {s["slug"]: s for s in SECOES}
PAG2SLUG = {}
for _s in SECOES:
    for _p in _s.get("paginas", []):
        PAG2SLUG.setdefault(_p, _s["slug"])
POR_ID = {c["id"]: c for c in D["conceitos"]}
EIXO = next(c for c in D["conceitos"] if c.get("eixo"))

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
    return re.sub(r"\((p\. [\d\-]+|Resumo)\)", lambda m: pg(m.group(1), prefixo), esc(texto))


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


def url_conceito(cid):
    return f"{BASE}/conceitos/{cid}/"


def conceitos_do_atlas():
    return [c for c in D["conceitos"] if c["tipo"] == "conceito"]


LEGENDA = {
    "mista": ("Arquitetura à mostra. Os contornos tracejados mostram as peças da página, e a etiqueta de cada uma diz o que ela é e de onde vem. "
              "As caixas com números de página levam ao trecho exato do texto integral."),
    "interna": ("Arquitetura à mostra. Os contornos tracejados mostram as peças da página, e a etiqueta de cada uma diz o que ela é e de onde vem. "
                "Para a leitura longa, sem etiquetas, volte ao modo Doutrina."),
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
    ("Percurso", "percurso/", (0,)), ("Ideias", "#conceitos", (0,)), ("Seus direitos", "direitos/", (0,)), ("Outras plataformas", "laboratorio/", (0,)),
    ("Situações", "roteiro/", (1,)), ("Diretrizes", "roteiro/diretrizes/", (1,)), ("Plataformas", "laboratorio/", (1,)),
    ("Conceitos", "#conceitos", (1,)), ("Legislação", "legislacao/", (1,)),
    ("Método", "metodo/", (2,)), ("Fundamentos", "fundamentos/", (2,)), ("Dogmática", "dogmatica/", (2,)),
    ("Objeto e instrumentos", "objeto-e-instrumentos/", (2,)), ("Autores", "autores/", (2,)), ("Referências", "referencias/", (2,)),
]
MENU_SEGUNDA = [("Percurso", "percurso/"), ("Ideias", "#conceitos"), ("Seus direitos", "direitos/"), ("Situações", "roteiro/"), ("Diretrizes", "roteiro/diretrizes/"),
                ("Plataformas", "laboratorio/"), ("Legislação", "legislacao/")]


def menu_html(prefixo):
    def existe(caminho):
        return caminho.startswith("#") or caminho in PAGINAS_PRONTAS
    itens = "".join(f'<li class="em-modo {" ".join(f"modo-{m}" for m in modos)}"><a href="{prefixo}{caminho}">{esc(rotulo)}</a></li>'
                    for rotulo, caminho, modos in MENU if existe(caminho))
    segunda = "".join(f'<li><a href="{prefixo}{caminho}">{esc(rotulo)}</a></li>' for rotulo, caminho in MENU_SEGUNDA if existe(caminho))
    return (f'<nav class="menu-modo" aria-label="Seções"><ul>{itens}</ul>'
            f'<ul class="em-modo modo-2 menu-segunda" aria-label="Os outros modos">{segunda}</ul></nav>')


# Páginas que o gerador escreve. O menu só mostra endereço que existe.
PAGINAS_PRONTAS = {"percurso/", "direitos/", "laboratorio/", "roteiro/", "roteiro/diretrizes/", "metodo/", "fundamentos/", "dogmatica/", "legislacao/",
                   "autores/", "referencias/", "objeto-e-instrumentos/"}


def pagina(titulo, descricao, corpo, prefixo, caminho, jsonld=None, camada="interna", superficie=None, imagem=None, lei=True):
    """Monta a página.

    camada 'mista' abre em Informação e ganha conteúdo em Doutrina e estrutura em Ciência.
    camada 'interna' é página do técnico, que abre no mínimo em Doutrina. Escolher Informação leva à superfície.
    camada 'ciencia' é página do expert, que só existe em Ciência. Escolher outro modo leva à superfície.
    camada 'externa' não tem arquitetura própria a mostrar.
    """
    canonico = BASE + "/" + caminho
    # Cada artigo citado com o nome da lei ganha o texto integral em rodapé. O texto integral da tese fica como está.
    # Cada citação de autor ou fonte da lista de referências vira balão. Vale também para o texto integral.
    corpo = com_autores(corpo, prefixo)
    if lei:
        corpo = com_lei(corpo, prefixo)
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
<link rel="stylesheet" href="{prefixo}assets/estilo.css">
<link rel="alternate" type="application/json" href="{prefixo}dados/atlas.json" title="Dados do Atlas">
{ld}
</head>
<body class="{'aberto' if interna else ''}{' desnudo' if minimo > 1 else ''}" data-camada="{camada}" data-minimo="{minimo}" data-superficie="{esc(sup)}">
{chave_mestra(minimo)}
{lembrar}
<div class="moldura">
  <div class="faixa arq" data-arq="versão · o site cresce em público e cada mudança fica registrada">
    <span>Versão {VERSAO} · em construção</span>
  </div>
  <header class="topo">
    <a class="topo-marca" href="{inicio}"><span class="topo-projeto">Projeto</span><span class="topo-nome">Lex Plataformae</span></a>
    {menu_html(prefixo)}
    <a class="integral" href="{prefixo}tese/">Texto integral</a>
  </header>
  <p class="legenda-desnudo" role="note">{esc(legenda)}</p>
  <main>
{corpo}
  </main>
  <footer class="rodape">
    <div class="interno rodape-estudo">
      <p><a href="{prefixo}tese/{PDF_NOME}">Texto integral em PDF</a>. Todo texto entre aspas é transcrição literal, com a página indicada. Acréscimos posteriores aparecem marcados e datados. O código do site e o histórico de cada alteração são públicos <a href="{REPO}">no GitHub</a>. Todos os direitos reservados até a definição da licença do projeto.</p>
    </div>
    {assinatura}
  </footer>
</div>
<script src="{prefixo}assets/atlas.js" defer></script>
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
            campo_ = linha[4:].strip()
            dados[pag][campo_] = {"paragrafos": [], "citacoes": []}
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
CAMPOS_DIREITO = {"quando": "Quando acontece", "deve": "O que a plataforma deve", "mostrar": "O que ajuda a mostrar",
                  "pedir": "O que você pode pedir", "limite": "Até onde vai"}


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
    partes = "".join(f'<div class="direito-parte parte-{k}"><dt>{rotulo}</dt><dd>' + "".join(f"<p>{esc(t)}</p>" for t in d[k]) + "</dd></div>"
                     for k, rotulo in CAMPOS_DIREITO.items() if d[k])
    return (f'<section class="ext direito"{ident}><{nivel} class="direito-titulo">{esc(d["titulo"])}</{nivel}>'
            + "".join(f"<p>{esc(t)}</p>" for t in d["paragrafos"])
            + (f'<dl class="direito-partes">{partes}</dl>' if partes else "")
            + expansao(d["citacoes"], prefixo)
            + f'<p class="ver-situacao interno"><a href="{prefixo}roteiro/#{letra}">A situação inteira, para quem vai operar</a></p></section>')


def secao_direitos(letras, prefixo):
    """O fecho de direitos de uma página do percurso ou de uma ideia."""
    if not letras:
        return (f'<section class="ext direitos-curto"><p class="rotulo-ext">O que você pode exigir</p>'
                f'<p class="ver-direitos"><a href="{prefixo}direitos/">Os seus direitos, um por um</a></p></section>')
    return ('<section class="direitos" aria-label="O que você pode exigir"><p class="rotulo-ext">O que você pode exigir</p>'
            + "".join(direito_html(l, prefixo) for l in letras)
            + f'<p class="ver-direitos"><a href="{prefixo}direitos/">Todos os seus direitos, e até onde eles vão</a></p></section>')


def direitos_da_parte(slug):
    return [l for l in LETRAS_DIREITOS if slug in DIREITOS[l]["partes"]]


def direitos_da_ideia(cid):
    return [l for l in LETRAS_DIREITOS if cid in DIREITOS[l]["ideias"]]


def gerar_direitos():
    prefixo = "../"
    intro = DIREITOS.get("intro", {"paragrafos": [], "citacoes": []})
    indice = "".join(f'<li><a href="#{l}">{esc(DIREITOS[l]["titulo"])}</a></li>' for l in LETRAS_DIREITOS)
    corpo = (f'<article class="folha direitos-pagina"><header class="folha-cabeca ext-cabeca"><h1>Seus direitos</h1></header>'
             f'<section class="ext">' + "".join(f"<p>{esc(t)}</p>" for t in intro["paragrafos"]) + expansao(intro["citacoes"], prefixo) + "</section>"
             f'<nav class="direitos-indice" aria-label="Os direitos"><ol>{indice}</ol></nav>'
             + "".join(direito_html(l, prefixo, "h2", ancora=True) for l in LETRAS_DIREITOS)
             + f'<section class="ext duvida"><div class="acoes"><a class="botao" href="{prefixo}percurso/">Seguir a skin desde a compra</a>{botao_desnudar()}</div></section>'
             + "</article>")
    destino = SAIDA / "direitos"
    destino.mkdir(parents=True, exist_ok=True)
    jsonld = {"@context": "https://schema.org", "@type": "Article", "headline": "Seus direitos", "inLanguage": "pt-BR",
              "url": f"{BASE}/direitos/", "isBasedOn": BASE + "/#tese", "author": {"@type": "Person", "name": "Victor Luiz Pereira de Andrade"}}
    (destino / "index.html").write_text(
        pagina("Seus direitos · Lex Plataformae",
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


def figura(ident, prefixo):
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
    escuro = next((ILUSTRACOES_DIR / f"{ident}-escuro{ext}" for ext in EXTENSOES if (ILUSTRACOES_DIR / f"{ident}-escuro{ext}").exists()), None)
    fonte = f'<source media="(prefers-color-scheme: dark)" srcset="{prefixo}assets/ilustracoes/{escuro.name}">' if escuro else ""
    return (f'<figure class="ilustracao {formato}"><picture>{fonte}'
            f'<img src="{prefixo}assets/ilustracoes/{arq.name}" alt="{esc(peca.get("alt", ""))}" width="{largura}" height="{altura}" loading="lazy" decoding="async"></picture>'
            f'<figcaption>{esc(peca.get("legenda", ""))} <span class="aviso-ia">{AVISO_IA}</span></figcaption>'
            + expansao(peca["citacoes"], prefixo) + "</figure>")
ROTULOS_PERCURSO = {"imagem": "Uma imagem", "mecanismo": "Como funciona", "caso": "Um caso",
                    "nome": "Isso tem nome", "termo": "Um nome para isso", "familia": "Fora do jogo",
                    "limite": "Até onde vai", "teste": "Como saber se é o seu caso"}

# Cores e áreas. A proposta está em estrutura/cores.json e foi aprovada pelo autor em 27/10/2026.
CORES = json.loads((RAIZ / "estrutura" / "cores.json").read_text(encoding="utf-8"))
AREA_NOME = {k: a["nome"] for k, a in CORES["areas"].items()}
# Os dez conceitos que a tese deriva, fora dos nove. Ganharam estatuto próprio ao lado dos nove, por decisão do autor de 27/10/2026.
DERIVADOS = {"Teleologia arquitetural", "Cativeiro identitário", "Consumidor-cidadão", "Transparência performática",
             "Consentimento viciado por sentido", "Publicidade enganosa por arquitetura", "Continuidade biográfica",
             "Recomposição funcional", "Correção de regime", "Dano-arquitetura"}
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


def expansao(cits, prefixo):
    """Os trechos literais que um bloco simples condensa. Aparecem a partir do degrau Verificar."""
    if not cits:
        return ""
    return ('<div class="interno expansao" data-arq="de onde vem · trechos literais, com a página">'
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


def botao_desnudar():
    """O convite dentro da página leva ao modo seguinte. Do último, volta à Informação."""
    return ('<span class="convite-botoes">'
            '<label class="botao convite-botao so-0" for="nivel-1">Abrir a Doutrina</label>'
            '<label class="botao convite-botao so-1" for="nivel-2">Abrir a Ciência</label>'
            '<label class="botao convite-botao so-2" for="nivel-0">Voltar à Informação</label></span>')


def html_passo(passo, base):
    c = POR_ID.get(passo["id"])
    extra = D["passos"].get(passo["id"])

    def link(cid, nome):
        return f'<a href="{base}{cid}/">{esc(nome)}</a>'

    if c and c["tipo"] == "conceito":
        nome = link(c["id"], c["nome"])
        if passo.get("par") and passo["par"] in POR_ID:
            dica = "O resumo da tese propõe o OIC enquanto feixe de fruição governada" if passo["par_rotulo"] == "enquanto" else "A tese trata os dois juntos em 5.1.3, 6.4 e 7.1.1.7"
            nome = (f'<span class="gemeos">{link(c["id"], c["nome"])}<span class="gemeos-sinal" title="{esc(dica)}">'
                    f'{esc(passo["par_rotulo"])}</span>{link(passo["par"], POR_ID[passo["par"]]["nome"])}</span>')
        corpo, classe, arq = f'<span class="passo-nome">{nome}</span>', "passo", ""
    elif c and c["tipo"] == "roteiro":
        corpo = (f'<span class="passo-tipo">fora do Atlas · passo do Roteiro · {esc(c["secao"])}</span>'
                 f'<span class="passo-nome">{link(c["id"], c["nome"])}</span>')
        classe, arq = "passo fantasma", ' data-arq="fora do Atlas · segue como passo do Roteiro"'
    elif c and c["tipo"] == "bens":
        corpo = f'<span class="passo-tipo">bens protegidos · 5.1.4 e 6.1.3</span><span class="passo-nome">{link(c["id"], c["nome"])}</span>'
        classe, arq = "passo fantasma", ' data-arq="fora do Atlas · camada de bens protegidos"'
    else:
        corpo = f'<span class="passo-tipo">passo do Roteiro · {esc(extra["secao"])}</span><span class="passo-nome">{esc(extra["nome"])}</span>'
        classe, arq = "passo fantasma", ' data-arq="fora do Atlas · passo do Roteiro"'
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
    return (f'<section class="secao percurso-mapa" id="percurso" aria-labelledby="percurso-titulo">{cabeca}'
            f'<div class="campo-texto">{ext_html("inicio", "percurso", "")}</div>'
            f'<ol class="partes">{itens}</ol>'
            f'<p><a class="botao" href="{base}{PERCURSO[0]["slug"]}/">Começar pela compra</a></p></section>')


def no_percurso(cid, prefixo):
    achados = partes_com_ideia(cid)
    if not achados:
        return ""
    return ('<section class="ext no-percurso"><p class="rotulo-ext">No percurso da skin</p><ul class="partes-curtas">'
            + "".join(f'<li><a href="{prefixo}percurso/{parte["slug"]}/"><span class="parte-num">{i}</span>{esc(parte["titulo"])}</a></li>'
                      for i, parte in achados)
            + "</ul></section>")


def bloco_percurso(b, prefixo):
    tipo, arg = b["tipo"], b["arg"]
    texto = "".join(f"<p>{esc(t)}</p>" for t in b["paragrafos"])
    exp = expansao(b["citacoes"], prefixo)
    rotulo = ROTULOS_PERCURSO.get(tipo)
    if tipo == "nome":
        c = POR_ID[arg]
        return (f'<section class="ext nome-ext"><h2 class="nome-conceito"><span class="rotulo-ext">{rotulo}</span>'
                f'<a href="{prefixo}conceitos/{arg}/">{esc(c["nome"])}</a></h2>{texto}'
                f'<p class="ver-ideia"><a href="{prefixo}conceitos/{arg}/">A ideia inteira</a></p>{exp}</section>')
    if tipo == "termo":
        derivado = arg in DERIVADOS
        area = AREA_TERMO.get(arg)
        nome = f'<span class="nome-derivado">{esc(arg)}</span>' if derivado else esc(arg)
        rot_area = (f' <span class="area-rotulo ciencia">· {esc(AREA_NOME[area])}</span>' if area
                    else ' <span class="area-rotulo ciencia">· conceito derivado da tese</span>' if derivado else "")
        return (f'<section class="ext termo{" derivado" if derivado else ""}"{estilo_area(area)}><h2 class="nome-termo"><span class="rotulo-ext">{rotulo}{rot_area}</span>{nome}</h2>'
                f'{texto}{exp}</section>')
    if tipo == "familia":
        titulo = ext_texto(arg, "titulo") or arg
        return (f'<section class="ext termo familia"><h2 class="nome-termo"><span class="rotulo-ext">{rotulo}</span>'
                f'<a href="{prefixo}laboratorio/{arg}/">{esc(titulo)}</a></h2>{texto}{exp}</section>')
    if tipo == "ilustracao":
        return figura(arg, prefixo)
    if tipo in ("imagem", "mecanismo", "caso", "teste"):
        return f'<section class="ext didatico {tipo}"><p class="rotulo-ext">{rotulo}</p>{texto}{exp}</section>'
    if tipo == "limite":
        return f'<section class="ext limite"><p class="rotulo-ext">{rotulo}</p>{texto}{exp}</section>'
    return f'<section class="ext">{texto}{exp}</section>'


def gerar_percurso():
    total = len(PERCURSO)
    raiz = SAIDA / "percurso"
    raiz.mkdir(parents=True, exist_ok=True)
    corpo = f'<article class="folha percurso-indice">{mapa_percurso("", "indice")}</article>'
    (raiz / "index.html").write_text(
        pagina("Siga a skin · Lex Plataformae", "Você comprou uma skin. Ela é sua? Onze perguntas, do clique de compra ao que a lei pode fazer.",
               corpo, "../", "percurso/", camada="mista", imagem="inicio"), encoding="utf-8")
    prefixo = "../../"
    for i, parte in enumerate(PERCURSO, 1):
        anterior = PERCURSO[i - 2] if i > 1 else None
        seguinte = PERCURSO[i] if i < total else None
        if seguinte:
            avancar = f'<a class="botao" href="../{seguinte["slug"]}/">Seguir para a parte {i + 1}</a>'
        else:
            avancar = f'<a class="botao" href="{prefixo}#conceitos">Ver as nove ideias</a>'
        vizinhos = ('<nav class="vizinhos" aria-label="Partes do percurso">'
                    + (f'<a href="../{anterior["slug"]}/">← {esc(anterior["titulo"])}</a>' if anterior else f'<a href="{prefixo}">← Início</a>')
                    + (f'<a href="../{seguinte["slug"]}/">{esc(seguinte["titulo"])} →</a>' if seguinte else "")
                    + "</nav>")
        corpo = (f'<article class="folha percurso-parte">'
                 f'<p class="sobrelinha-ext"><a href="{prefixo}#percurso">Percurso</a> · Parte {i} de {total}</p>'
                 f'<header class="folha-cabeca ext-cabeca"><h1>{esc(parte["titulo"])}</h1></header>'
                 + figura(f'parte-{parte["slug"]}', prefixo)
                 + "".join(bloco_percurso(b, prefixo) for b in parte["blocos"])
                 + secao_direitos(direitos_da_parte(parte["slug"]), prefixo)
                 + f'<section class="ext duvida"><p class="pergunta-final">{esc(parte["pergunta"])}</p>'
                 f'<div class="acoes">{avancar}{botao_desnudar()}</div></section>'
                 + vizinhos + "</article>")
        jsonld = {"@context": "https://schema.org", "@type": "Article", "headline": parte["titulo"], "inLanguage": "pt-BR",
                  "url": f'{BASE}/percurso/{parte["slug"]}/', "isBasedOn": BASE + "/#tese",
                  "author": {"@type": "Person", "name": "Victor Luiz Pereira de Andrade"}}
        destino = raiz / parte["slug"]
        destino.mkdir(parents=True, exist_ok=True)
        (destino / "index.html").write_text(
            pagina(f'{parte["titulo"]} · Lex Plataformae', f'{parte["resumo"]} Parte {i} de {total} do percurso da skin.',
                   corpo, prefixo, f'percurso/{parte["slug"]}/', jsonld, camada="mista", imagem=f'percurso-{parte["slug"]}'),
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
        # O cartão do OIC dispensa a expansão, porque a definição literal aparece logo abaixo dele.
        exp = "" if c is EIXO else expansao(bloco.get("citacoes", []), "")
        return (f'<li><a class="cartao cartao-ideia{classe}" href="{base}{c["id"]}/"><span class="cartao-frase">{esc(frase)}</span>'
                f'<b>{esc(c["nome"])}</b></a>{exp}</li>')

    eixo_cartoes = cartao(EIXO, " cartao-eixo") + (cartao(gemeo, " cartao-eixo") if gemeo else "")
    cartoes = "".join(cartao(c) for c in independentes)

    corpo = f"""
    <section class="abertura" aria-labelledby="titulo">
      <h1 class="chamada" id="titulo">{"".join(f'<span class="chamada-linha">{esc(f)}</span> ' for f in re.split(r"(?<=[.!?])\s+", ext_texto("inicio", "chamada"))).strip()}</h1>
      <div class="lema">{ext_html("inicio", "abertura", "")}</div>
      <blockquote class="frase interno" data-arq="citação literal · a frase que abre o percurso">“{esc(ab["texto"])}”{pg(ab["ref"], "", ab["texto"])}</blockquote>
    </section>

    {figura("inicio", "")}

    <section class="secao problema" aria-label="O problema">
      {ext_html("inicio", "problema", "")}
    </section>

    {mapa_percurso("percurso/", "inicio")}

    <section class="campo" id="conceitos" aria-labelledby="conceitos-titulo">
      <h2 class="campo-titulo" id="conceitos-titulo">As ideias</h2>
      <div class="campo-texto">{ext_html("inicio", "nome", "")}</div>
      <ul class="eixo-cartoes" data-arq="eixo · o OIC enquanto feixe de fruição governada">{eixo_cartoes}</ul>
      <div class="campo-topo interno" data-arq="integração · conceitos independentes que funcionam integrados sob o OIC">
        <p class="campo-def">“{esc(oic_def["texto"])}”{pg(oic_def["ref"], "", oic_def["texto"])}</p>
        {f'<blockquote class="citacao integra"><p>“{esc(gatilho["texto"])}”{pg(gatilho["ref"], "", gatilho["texto"])}</p></blockquote>' if gatilho else ""}
      </div>
      <div class="campo-texto">{ext_html("inicio", "mapa", "")}</div>
      <ul class="grade-conceitos" data-arq="conceitos independentes · sem ordem nem hierarquia">{cartoes}</ul>
    </section>

    <section class="convite" aria-label="Desnudar a arquitetura">
      {ext_html("inicio", "convite", "")}
      {botao_desnudar()}
    </section>

    <section class="secao leituras ciencia" aria-labelledby="leituras-titulo">
      <h2 id="leituras-titulo">Três leituras do texto integral</h2>
      <p>O texto integral também percorre os conceitos em três ordens. São leituras do texto, não hierarquia entre os conceitos. Elas vão compor o Roteiro.</p>
      <fieldset class="percursos">
        <legend>Escolha uma leitura</legend>
        <div class="seletor">{opcoes}</div>
        <p class="logica" id="logica" aria-live="polite">{esc(p["logica"])} <q>{esc(p["trecho"]["texto"])}</q>{pg(p["trecho"]["ref"], "", p["trecho"]["texto"])}</p>
      </fieldset>
      <ul class="sequencia" id="sequencia" data-base="{base}" aria-label="{esc(p["nome"])}" data-arq="leitura · ordem do texto, não hierarquia">{passos}</ul>
      <div class="fora" id="fora">{fora}</div>
      <script type="application/json" id="leituras-dados">{json.dumps(dados_leituras, ensure_ascii=False).replace("</", "<\\/")}</script>
    </section>

    <section class="secao" id="epigrafes" aria-labelledby="epigrafes-titulo">
      <h2 id="epigrafes-titulo">Trilha sonora</h2>
      {ext_html("inicio", "trilha", "")}
      <div class="ciencia" data-arq="epígrafes · uma canção abre cada etapa do texto integral">
        <p>Cada etapa do texto integral abre com uma destas canções. São nove, como as nove Musas. A ordem faz o mesmo percurso do argumento.{pg("p. 73-78", "")}</p>
        <ol class="epigrafes">{musas}</ol>
      </div>
      <div class="epigrafes-player" data-embed="{esc(ep["playlist"]["embed"])}" data-arq="terceiro · o Spotify só carrega depois do clique">
        <div class="ouvir">
          <button type="button" class="botao epigrafes-carregar">Ouvir a playlist aqui</button>
          <p class="aviso">Ao carregar o player, o Spotify passa a receber dados desta visita. Nada toca sem que você aperte o play. Se preferir, <a href="{esc(ep["playlist"]["url"])}" rel="noopener">abra a playlist direto no Spotify</a>.</p>
        </div>
      </div>
    </section>
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
    desc = "Você comprou uma skin. Ela é sua? Um percurso pelo que acontece com o que se compra no mundo digital, e nove ideias para dar nome a isso."
    corpo = f'<div class="pagina-inicio">{corpo}</div>'
    (SAIDA / "index.html").write_text(pagina("Lex Plataformae", desc, corpo, "", "", jsonld, camada="mista"), encoding="utf-8")


def gerar_conceito(c):
    prefixo = "../../"
    base = "../"
    if c["tipo"] == "roteiro":
        sobre = f'Fora do Atlas · passo do Roteiro · {c["secao"]}'
    elif c["tipo"] == "bens":
        sobre = "Bens protegidos · fora do Atlas"
    else:
        sobre = "Conceito · eixo de integração dos demais" if c.get("eixo") else "Conceito"
    selos = f'<span class="selo" data-arq="versão · o conteúdo segue em revisão pelo autor">Versão {VERSAO}</span>'
    if c.get("par"):
        rot = "Em par com "
        selos += f'<a class="selo gemeo" href="{base}{c["par"]["id"]}/">{rot}{esc(POR_ID[c["par"]["id"]]["nome"])}</a>'

    partes = []
    for f in c["campos"]:
        r = f["rotulo"]
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
        bloco = f'<section class="bloco"><h2>{esc(r)}</h2>'
        if f["texto"]:
            bloco += f"<p>{com_ancoras(f['texto'], prefixo)}</p>"
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
    if itens_rot:
        partes.append('<section class="bloco"><h2>Nas situações</h2>'
                      + ('<p class="nota-camada">Os blocos seguem o enunciado do 7.1.1 a que cada um corresponde. As demais páginas aparecem porque a tese nomeia o conceito no trecho.</p>' if nomes.get("Roteiro") and letras else "")
                      + '<ul class="lugares">' + "".join(itens_rot) + "</ul></section>")
    if nomes.get("Laboratório"):
        partes.append('<section class="bloco ciencia"><h2>No Laboratório</h2><p class="nota-camada">Páginas em que a tese nomeia o conceito, com o número de vezes.</p><ul class="lugares">'
                      + "".join(f'<li><a href="{prefixo}{caminho}">{esc(rotulo)}</a> <span class="vezes">{esc(det)}</span></li>' for rotulo, caminho, det in nomes["Laboratório"])
                      + "</ul></section>")

    outros_nav = ""
    if c["tipo"] == "conceito":
        outros = em_ordem([x for x in conceitos_do_atlas() if x is not c and not x.get("eixo")])
        lista = ([] if c.get("eixo") else [EIXO]) + outros
        outros_nav = ('<nav class="outros" aria-label="As outras ideias"><h2>As outras ideias</h2><ul>'
                      + "".join(f'<li><a href="{base}{x["id"]}/">{esc(x["nome"])}</a></li>' for x in lista) + "</ul></nav>")

    e = EXTERNA.get(c["id"]) if c["tipo"] == "conceito" else None
    can = canonica(c)
    jsonld = {"@context": "https://schema.org", "@type": "DefinedTerm", "@id": url_conceito(c["id"]), "name": c["nome"],
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
            return (f'<section class="ext {classe}">' + (f'<p class="rotulo-ext">{esc(rotulo)}</p>' if rotulo else "")
                    + "".join(f"<p>{esc(t)}</p>" for t in b["paragrafos"]) + expansao(b["citacoes"], prefixo) + "</section>")
        nome_b = e.get("nome", {"paragrafos": [], "citacoes": []})
        resto = re.sub(r"^.*?[.!?]\s+", "", " ".join(nome_b["paragrafos"]), count=1)
        duvida = ext_texto(c["id"], "duvida")
        externo = (
            f'<a class="voltar" href="{prefixo}#conceitos">← Todas as ideias</a>'
            f'<header class="folha-cabeca ext-cabeca"><h1>{esc(ext_texto(c["id"], "titulo"))}</h1></header>'
            + bloco_ext("fenomeno", classe="fenomeno")
            + f'<section class="ext nome-ext"><h2 class="nome-conceito"><span class="rotulo-ext">Isso tem nome</span><span class="chapado">{esc(c["nome"])}</span></h2>'
            + (f"<p>{esc(resto)}</p>" if resto else "") + expansao(nome_b["citacoes"], prefixo) + "</section>"
            + figura(f'ideia-{c["id"]}', prefixo)
            + bloco_ext("imagem", "Uma imagem", "didatico imagem")
            + bloco_ext("mecanismo", "Como funciona", "didatico mecanismo")
            + bloco_ext("caso", "Um caso", "didatico caso")
            + bloco_ext("importa", "Por que importa")
            + bloco_ext("limite", "Até onde vai", "limite")
            + (secao_direitos(direitos_da_ideia(c["id"]), prefixo) if direitos_da_ideia(c["id"]) else "")
            + no_percurso(c["id"], prefixo)
            + (f'<section class="ext duvida"><p class="pergunta-final">{esc(duvida)}</p>{botao_desnudar()}</section>' if duvida else ""))
        arquitetura = (f'<div class="interno arquitetura" data-arq="arquitetura · a ideia no texto integral">'
                       f'<header class="folha-cabeca"><p class="sobrelinha ciencia">{esc(sobre)}</p><h2 class="titulo-interno">{esc(c["nome"])}</h2><div class="selos ciencia">{selos}</div></header>'
                       + "".join(partes) + "</div>")
        corpo = f'<article class="folha conceito-pagina">{externo}{arquitetura}{outros_nav}</article>'
        desc = ext_texto("cartoes", c["id"]) or (resumo(can["texto"]) if can else c["nome"])
        (destino / "index.html").write_text(
            pagina(f'{c["nome"]} · Lex Plataformae', desc, corpo, prefixo, f'conceitos/{c["id"]}/', jsonld, camada="mista", imagem=c["id"]), encoding="utf-8")
        return

    corpo = (f'<article class="folha"><a class="voltar" href="{prefixo}#conceitos">← Todas as ideias</a>'
             f'<header class="folha-cabeca"><p class="sobrelinha ciencia">{esc(sobre)}</p><h1>{esc(c["nome"])}</h1><div class="selos ciencia">{selos}</div></header>'
             + "".join(partes) + outros_nav + "</article>")
    desc = resumo(can["texto"]) if can else c["nome"]
    (destino / "index.html").write_text(
        pagina(f'{c["nome"]} · Lex Plataformae', desc, corpo, prefixo, f'conceitos/{c["id"]}/', jsonld), encoding="utf-8")


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
CAMADA_ENDERECO = {"Atlas": "", "Roteiro": "roteiro/", "Laboratório": "laboratorio/", "Fundamentos": "fundamentos/", "Método": "metodo/", "Dogmática": "dogmatica/", "Epígrafes": "#epigrafes"}


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
                   + " · ".join(f'<a href="{prefixo}{CAMADA_ENDERECO[n]}">{esc(n)}</a>' for n in nomes) + "</p>") if nomes else ""
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
        'As letras das epígrafes não são reproduzidas no site. Elas estão no PDF.'
        + (f' A abertura da tese traz a epígrafe de {abertura.replace("<li>", "").replace("</li>", "")}.' if abertura else "") +
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
        pagina("Texto integral · Lex Plataformae", resumir_texto(resumo["texto"]) if resumo else TITULO_TESE, corpo, "../", "tese/", jsonld, camada="mista", lei=False),
        encoding="utf-8")

    # Uma página por seção.
    for i, sec in enumerate(SECOES):
        prefixo = "../../"
        trilha = ['<a href="../">Texto integral</a>'] + [f'<a href="../{a["slug"]}/">{rotulo_secao_html(a)}</a>' for a in ancestrais(sec)]
        faixa_pag = f'p. {sec["pagina_inicio"]}' + (f' a {sec["pagina_fim"]}' if sec["pagina_fim"] != sec["pagina_inicio"] else "")
        partes = []
        for e in sec.get("epigrafes", []):
            partes.append(f'<aside class="epigrafe-ref" data-arq="epígrafe · letra omitida no site">'
                          f'<p class="sobrelinha">Epígrafe</p><p>{esc(e["artista"])}, <cite>{esc(e["faixa"])}</cite> ({e["ano"]}). '
                          f'A letra não é reproduzida no site. <a href="../{PDF_NOME}#page={e["pagina_pdf"]}">Ler no PDF</a>.</p></aside>')
        for b in sec["blocos"]:
            if b["tipo"] == "citacao":
                partes.append(f'<blockquote class="citacao-longa"{attrs_ref(b, prefixo)}>{b["html"]}</blockquote>')
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
        for tipo, rotulo in (("conceito", "Conceitos do Atlas nesta seção"), ("roteiro", "Passos do Roteiro com ficha nesta seção"), ("bens", "Bens protegidos nesta seção")):
            deste = [c for c in aqui if c["tipo"] == tipo]
            if deste:
                conceitos_aqui += (f'<aside class="conceitos-aqui" data-arq="fichas · conceitos que vivem nesta seção">'
                                   f'<p class="sobrelinha">{rotulo}</p><ul>'
                                   + "".join(f'<li><a href="{prefixo}conceitos/{c["id"]}/">{esc(c["nome"])}</a></li>' for c in em_ordem(deste))
                                   + "</ul></aside>")
        if usos.get(sec["slug"]):
            conceitos_aqui += ('<aside class="conceitos-aqui camadas-aqui ciencia" data-arq="estrutura · páginas das camadas que trazem esta seção">'
                               '<p class="sobrelinha">Esta seção nas camadas do site</p><ul>'
                               + "".join(f'<li><a href="{prefixo}{caminho}">{esc(camada)} · {esc(rotulo)}</a></li>' for camada, rotulo, caminho in usos[sec["slug"]])
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
            pagina(f'{rotulo_secao(sec)} · Lex Plataformae', resumir_texto(texto_puro), corpo, prefixo, f'tese/{sec["slug"]}/', jsonld, camada="mista", lei=False),
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
PORTAO_TITULO = "Isto é um objeto imaterial de consumo?"

PARTES_ROTEIRO = [
    ("Quando incide", r"Sempre que"),
    ("Dever de fornecimento", r"O dever (?:de fornecimento )?correspondente"),
    ("Prova mínima exigível", r"A prova mínima exigível"),
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


# Destaques. Trechos literais que as páginas das camadas marcam no texto da tese.
# A lista fica em estrutura/destaques.md e é conferida pelo mesmo script das fichas.
def carregar_destaques():
    arq = RAIZ / "estrutura" / "destaques.md"
    mapa, chave = {}, None
    if not arq.exists():
        return mapa
    for linha in arq.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## (\S+)(?: / (\d+))?\s*$", linha)
        if m:
            chave = (m.group(1), int(m.group(2)) if m.group(2) else None)
            mapa.setdefault(chave, [])
            continue
        m = re.match(r"^> (.+?) \((p\. [\d\-]+)\)\s*$", linha)
        if m and chave:
            mapa[chave].append({"texto": m.group(1), "ref": m.group(2)})
    return mapa


DESTAQUES = carregar_destaques()
DESTAQUES_USADOS = set()


def destaques(numero, parte=None):
    return DESTAQUES.get((numero, parte), [])


_NOTA = r'(?:<sup class="nota-ref">(?:(?!</sup>).)*</sup>)'
_MARCA = r'(?:<a class="pg-marca"[^>]*>[^<]*</a>|<span class="pg-marca"[^>]*>[^<]*</span>)'
_ENTRE = r"(?:\s|" + _MARCA + "|" + _NOTA + ")+"


def _padrao_palavra(p):
    m = re.match(r"^(.*?)([.,;:!?)\]]*)$", p)
    nucleo, pont = m.group(1), m.group(2)

    def em_re(s):
        s = re.escape(html.escape(s, quote=False))
        return s.replace("“", '[“"]').replace("”", '[”"]')

    italico_abre, italico_fecha = r"(?:<(?:em|i)>)?", r"(?:</(?:em|i)>)?"
    return italico_abre + em_re(nucleo) + italico_fecha + _NOTA + "?" + (em_re(pont) + _NOTA + "?" if pont else "")


def _equilibrado(s):
    pilha = []
    for m in re.finditer(r"<(/?)(\w+)[^>]*>", s):
        if m.group(1):
            if not pilha or pilha[-1] != m.group(2):
                return False
            pilha.pop()
        else:
            pilha.append(m.group(2))
    return not pilha


def contador(prefixo="destaque"):
    n = [0]

    def proximo():
        n[0] += 1
        return f"{prefixo}-{n[0]}"
    return proximo


def marcar(h, trechos, proximo):
    """Marca no HTML de um parágrafo os trechos literais que ele contém. Devolve o HTML e os trechos marcados."""
    achados = []
    for t in trechos:
        padrao = _ENTRE.join(_padrao_palavra(p) for p in t["texto"].split())
        m = re.search(padrao, h)
        if not m:
            continue
        miolo = m.group(0)
        if not _equilibrado(re.sub(_MARCA + "|" + _NOTA, "", miolo)):
            print(f"Destaque não marcado, cruza uma etiqueta do HTML  {t['texto'][:60]}")
            continue
        ident = proximo()
        h = h[:m.start()] + f'<mark class="destaque" id="{ident}">{miolo}</mark>' + h[m.end():]
        achados.append((t, ident))
        DESTAQUES_USADOS.add((t["texto"], t["ref"]))
    return h, achados


def texto_marcado(blocos, slug, prefixo, trechos, proximo):
    """Texto literal de uma sequência de blocos do corpus, com os destaques marcados."""
    partes, achados = [], []
    for b in blocos:
        h = html_do_corpus(b["html"], slug, prefixo)
        if b["tipo"] == "marca":
            partes.append(f'<p class="marca-solta">{h}</p>')
            continue
        pendentes = [t for t in trechos if all(t is not x for x, _ in achados)]
        h, novos = marcar(h, pendentes, proximo)
        achados += novos
        partes.append(f'<blockquote class="citacao-longa"{attrs_ref(b, prefixo)}>{h}</blockquote>' if b["tipo"] == "citacao" else f"<p{attrs_ref(b, prefixo)}>{h}</p>")
    return "".join(partes), achados


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
    itens = "".join(f'<li><a href="{prefixo}conceitos/{cid}/">{esc(POR_ID[cid]["nome"])}</a> <span class="vezes">{contagem[cid]}×</span></li>' for cid in ordem)
    return ('<aside class="nomeados ciencia" data-arq="contagem mecânica · termos do Atlas e do Roteiro que o trecho nomeia">'
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
    campos = POR_NUMERO.get("5.1.2.3")
    portao = []
    if campos:
        texto = " ".join(b["html"] for b in campos["blocos"])
        for inicio in ("O primeiro campo", "O segundo campo", "O terceiro campo", "O quarto campo", "A incidência não se decide"):
            m = re.search(re.escape(inicio) + r".*?\.(?=\s|$)", texto)
            if m:
                portao.append(html_do_corpus(m.group(0), campos["slug"], prefixo))
    enunciados = POR_NUMERO.get("7.1.1")
    intro_711 = ""
    if enunciados:
        texto = " ".join(b["html"] for b in enunciados["blocos"])
        m = re.search(r"Os enunciados não devem ser lidos.*?passo subsequente\.", texto)
        if m:
            intro_711 = html_do_corpus(m.group(0), enunciados["slug"], prefixo)

    secoes = []
    for it in r["itens"]:
        num, ids = ROTEIRO_MAPA.get(it["letra"], (None, []))
        ligacoes = []
        if num and num in POR_NUMERO:
            ligacoes.append(f'<a class="ciencia" href="{prefixo}tese/{POR_NUMERO[num]["slug"]}/">Enunciado {num} na tese</a>')
        ligacoes += [f'<a href="{prefixo}conceitos/{i}/">{esc(POR_ID[i]["nome"])}</a>' for i in ids if i in POR_ID]
        dl = "".join(f'<dt>{esc(rot)}</dt><dd data-ref="{esc(ref)}" data-alvo="{prefixo}tese/{slug}/#p{re.match(r"p. (\d+)", ref).group(1)}">{html_do_corpus(h, slug, prefixo)}</dd>'
                     for rot, h, ref in it["partes"])
        secoes.append(
            f'<section class="bloco-roteiro" id="{it["letra"]}" aria-labelledby="titulo-{it["letra"]}">'
            f'<h2 id="titulo-{it["letra"]}">{esc(SITUACOES.get(it["letra"], it["titulo"]))}</h2>'
            f'<p class="titulo-tese ciencia"><span class="letra">{it["letra"]})</span> {esc(it["titulo"])}</p>'
            f'<dl class="partes" data-arq="texto literal do 7.1.2 · cinco partes da tese">{dl}</dl>'
            + (f'<p class="ligacoes">{" · ".join(ligacoes)}</p>' if ligacoes else "")
            + "</section>")
    lista_portao = "".join(f"<li>{x}</li>" for x in portao[:4])
    regra_portao = f"<p>{portao[4]}</p>" if len(portao) > 4 else ""
    indice = "".join(f'<li><a href="#{it["letra"]}"><span class="letra ciencia">{it["letra"]})</span> {esc(SITUACOES.get(it["letra"], it["titulo"]))}</a></li>' for it in r["itens"])
    grade = ""
    if POR_NUMERO.get("7.1"):
        s71 = POR_NUMERO["7.1"]
        primeiro = next((b["html"] for b in s71["blocos"] if b["tipo"] == "p"), "")
        m = re.search(r"A passagem do regime.*?contextos distintos\.", primeiro)
        if m:
            grade = f'<blockquote class="citacao"><p>{html_do_corpus(m.group(0), s71["slug"], prefixo)}{pg("p. 714", prefixo, _plano(m.group(0)))}</p></blockquote>'
    corpo = (
        '<article class="folha leitura roteiro">'
        '<header class="folha-cabeca"><p class="sobrelinha ciencia">Roteiro · 7.1.2 da tese</p><h1>Situações</h1>'
        + "".join(f"<p>{html_do_corpus(a, slug, prefixo)}</p>" for a in r["abertura"][1:2]) +
        '</header>'
        + nav_roteiro("7.1.2", prefixo, grade)
        + (f'<section class="bloco"><h2>Por que a ordem importa</h2><blockquote class="citacao"><p>{intro_711}</p></blockquote></section>' if intro_711 else "")
        + (f'<section class="bloco portao" id="portao" data-arq="portão · os quatro campos cumulativos do OIC"><h2>{esc(PORTAO_TITULO)}</h2><ol>{lista_portao}</ol>{regra_portao}</section>' if lista_portao else "")
        + f'<nav class="bloco indice-roteiro" aria-label="As situações"><h2>As onze situações</h2><ol>{indice}</ol></nav>'
        + "".join(secoes)
        + (f'<section class="bloco"><h2>O que este quadro não faz</h2><blockquote class="citacao"><p>{html_do_corpus(r["fecho"], slug, prefixo)}</p></blockquote></section>' if r["fecho"] else "")
        + '</article>'
    )
    jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": "Situações · Lex Plataformae", "inLanguage": "pt-BR",
              "url": BASE + "/roteiro/", "isBasedOn": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE}}
    pasta = SAIDA / "roteiro"
    pasta.mkdir(exist_ok=True)
    desc = "Onze situações para quem vai advogar, cada uma com quando incide, o dever do fornecedor, a prova mínima, a qualificação jurídica e a consequência, em texto literal."
    (pasta / "index.html").write_text(pagina("Situações · Lex Plataformae", desc, corpo, prefixo, "roteiro/", jsonld), encoding="utf-8")


# As partes do Roteiro, uma página para cada seção do 7.1 que a tese organiza como instrumento de aplicação.
ROTEIRO_PARTES = [("7.1.2", "roteiro/"), ("7.1.3", "roteiro/diretrizes/"), ("7.1.4", "roteiro/limites/")]
ORDINAIS = ["primeira", "segunda", "terceira", "quarta", "quinta", "sexta", "sétima", "oitava", "nona", "décima"]


ROTEIRO_ROTULOS = {"7.1.2": "Situações", "7.1.3": "Diretrizes de controle", "7.1.4": "Limites ao poder da plataforma"}


def nav_roteiro(atual, prefixo, lema=""):
    itens = []
    for num, caminho in ROTEIRO_PARTES:
        sec = POR_NUMERO.get(num)
        if not sec:
            continue
        atributo = ' aria-current="page"' if num == atual else ""
        itens.append(f'<li><a href="{prefixo}{caminho}"{atributo}><span class="em-modo modo-0 modo-1">{esc(ROTEIRO_ROTULOS[num])}</span>'
                     f'<span class="em-modo modo-2"><span class="num">{esc(num)}</span> {esc(sec["titulo"])}</span></a></li>')
    return ('<nav class="bloco partes-roteiro" aria-label="Partes do Roteiro" data-arq="navegação · uma página por seção do 7.1">'
            f'<h2>Para operar</h2>{lema}<ol>{"".join(itens)}</ol></nav>')


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


def blocos_simples(blocos, slug, prefixo):
    return "".join(
        f'<p class="marca-solta">{html_do_corpus(b["html"], slug, prefixo)}</p>' if b["tipo"] == "marca"
        else f'<blockquote class="citacao-longa"{attrs_ref(b, prefixo)}>{html_do_corpus(b["html"], slug, prefixo)}</blockquote>' if b["tipo"] == "citacao"
        else f'<p{attrs_ref(b, prefixo)}>{html_do_corpus(b["html"], slug, prefixo)}</p>' for b in blocos)


def indice_destaques(achados, titulo="Em frases da tese"):
    if not achados:
        return ""
    itens = "".join(f'<li><a href="#{ident}">{esc(t["texto"])}</a> {pg(t["ref"])}</li>' for t, ident in achados)
    return (f'<nav class="bloco indice-destaques" aria-label="{esc(titulo)}" data-arq="seleção editorial · trechos marcados no texto">'
            f'<h2>{esc(titulo)}</h2><p class="nota-camada">Os trechos marcados foram escolhidos pelo site.</p><ol>{itens}</ol></nav>')


def gerar_diretrizes():
    d = diretrizes()
    if not d or len(d["itens"]) != 10:
        print("7.1.3 sem as dez diretrizes, página não gerada")
        return
    sec, prefixo = d["secao"], "../../"
    proximo = contador()
    indice, secoes = [], []
    for n, ordinal, blocos in d["itens"]:
        texto, achados = texto_marcado(blocos, sec["slug"], prefixo, destaques("7.1.3", n), proximo)
        nome = ordinal.capitalize() + " diretriz"
        if achados:
            frase = " [...] ".join(t["texto"] for t, _ in achados)
            indice.append(f'<li><a href="#diretriz-{n}"><b>{esc(nome)}</b><span>{esc(frase)}</span></a> {pg(achados[0][0]["ref"])}</li>')
        else:
            indice.append(f'<li><a href="#diretriz-{n}"><b>{esc(nome)}</b></a></li>')
        secoes.append(
            f'<section class="bloco-roteiro" id="diretriz-{n}" aria-labelledby="titulo-diretriz-{n}">'
            f'<h2 id="titulo-diretriz-{n}">{esc(nome)}</h2><div class="texto">{texto}</div>'
            f'{nomeados_html(termos_em(texto_de(blocos)), prefixo)}</section>')
    corpo = (
        '<article class="folha leitura roteiro">'
        '<nav class="trilha" aria-label="Você está em"><a href="../">Roteiro</a></nav>'
        f'<header class="folha-cabeca"><p class="sobrelinha ciencia">Roteiro · {esc(sec["n"])} · p. {sec["pagina_inicio"]} a {sec["pagina_fim"]}</p>'
        f'<h1>{esc(sec["titulo"])}</h1><div class="texto">{blocos_simples(d["abertura"], sec["slug"], prefixo)}</div>'
        f'<p class="ler-pdf"><a href="{prefixo}tese/{sec["slug"]}/">Ler no texto integral</a></p></header>'
        + nav_roteiro("7.1.3", prefixo)
        + f'<nav class="bloco indice-roteiro indice-diretrizes" aria-label="As dez diretrizes" data-arq="seleção editorial · trechos marcados no texto"><h2>As dez diretrizes</h2><p class="nota-camada">Cada diretriz traz a frase que o site marcou no texto.</p><ol>{"".join(indice)}</ol></nav>'
        + "".join(secoes)
        + (f'<section class="bloco"><h2>As diretrizes em conjunto</h2><div class="texto">{blocos_simples(d["fecho"], sec["slug"], prefixo)}</div></section>' if d["fecho"] else "")
        + "</article>")
    jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": sec["titulo"], "inLanguage": "pt-BR",
              "url": BASE + "/roteiro/diretrizes/", "isBasedOn": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE}}
    destino = SAIDA / "roteiro" / "diretrizes"
    destino.mkdir(parents=True, exist_ok=True)
    desc = "As dez diretrizes da tese para o controle de arquitetura e governança em plataformas, em texto literal, com o trecho que enuncia cada uma."
    (destino / "index.html").write_text(pagina(f'Diretrizes de controle · Roteiro · Lex Plataformae', desc, corpo, prefixo, "roteiro/diretrizes/", jsonld), encoding="utf-8")


def pagina_lida(sec, prefixo, trilha, sobrelinha, chave, topo=""):
    """Seção da tese em texto integral, com os destaques marcados e o índice deles no alto."""
    texto, achados = texto_marcado(sec["blocos"], sec["slug"], prefixo, destaques(chave), contador())
    return (
        f'<nav class="trilha" aria-label="Você está em">{trilha}</nav>'
        f'<header class="folha-cabeca"><p class="sobrelinha">{esc(sobrelinha)}<span class="ciencia"> · {esc(sec["n"])} · p. {sec["pagina_inicio"]} a {sec["pagina_fim"]}</span></p>'
        f'<h1>{esc(sec["titulo"])}</h1><p class="ler-pdf"><a href="{prefixo}tese/{sec["slug"]}/">Ler no texto integral, com as notas</a></p></header>'
        + topo + indice_destaques(achados)
        + f'<section class="bloco"><h2>O texto da tese</h2><div class="texto">{texto}</div></section>'
        + nomeados_html(termos_em(texto_de(sec["blocos"])), prefixo))


def gerar_limites():
    sec = POR_NUMERO.get("7.1.4")
    if not sec:
        return
    prefixo = "../../"
    corpo = ('<article class="folha leitura roteiro">'
             + pagina_lida(sec, prefixo, '<a href="../">Roteiro</a>', "Roteiro", "7.1.4", nav_roteiro("7.1.4", prefixo))
             + "</article>")
    jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": sec["titulo"], "inLanguage": "pt-BR",
              "url": BASE + "/roteiro/limites/", "isBasedOn": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE}}
    destino = SAIDA / "roteiro" / "limites"
    destino.mkdir(parents=True, exist_ok=True)
    desc = "Cidadania digital e limites ao poder privado de plataforma, a seção que fecha o 7.1 da tese, em texto integral."
    (destino / "index.html").write_text(pagina("Cidadania digital e limites · Roteiro · Lex Plataformae", desc, corpo, prefixo, "roteiro/limites/", jsonld), encoding="utf-8")


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


def paragrafo_que_comeca(numero, inicio):
    sec = POR_NUMERO.get(numero)
    if not sec:
        return None, None
    for b in sec["blocos"]:
        if b["tipo"] == "p" and re.sub(r'^(?:<span class="pg-marca"[^>]*>[^<]*</span>\s*)+', "", b["html"]).startswith(inicio):
            return b["html"], sec
    return None, sec


def campos_da_familia(sec):
    """Distribui os parágrafos da seção pelos quatro passos que o 7.2 declara, sem cortar nenhum."""
    campos = [[rotulo, []] for rotulo, _ in CAMPOS_FAMILIA]
    atual = 0
    for b in sec["blocos"]:
        if b["tipo"] == "marca":
            continue
        t = html.unescape(re.sub(r"<[^>]+>", "", b["html"]))
        for i in range(len(CAMPOS_FAMILIA) - 1, atual, -1):
            padrao = CAMPOS_FAMILIA[i][1]
            if padrao and re.search(padrao, t, re.I):
                atual = i
                break
        campos[atual][1].append(b)
    return campos


def gerar_laboratorio():
    if not all(n in POR_NUMERO for n, _ in FAMILIAS):
        return
    pasta = SAIDA / "laboratorio"
    pasta.mkdir(exist_ok=True)
    intro = POR_NUMERO.get("7.2")
    fecho = POR_NUMERO.get("7.3")
    sequencia = next((b["html"] for b in intro["blocos"] if "Para manter essa comparabilidade" in b["html"]), "") if intro else ""
    triade = next((b["html"] for b in fecho["blocos"] if "Ao manter distinguíveis" in b["html"]), "") if fecho else ""

    cartoes = []
    for num, slug in FAMILIAS:
        sec = POR_NUMERO[num]
        prefixo = "../../"
        partes = []
        for rotulo, blocos in campos_da_familia(sec):
            if not blocos:
                continue
            corpo_campo = "".join(
                f'<blockquote class="citacao-longa"{attrs_ref(b, prefixo)}>{html_do_corpus(b["html"], sec["slug"], prefixo)}</blockquote>' if b["tipo"] == "citacao"
                else f'<p{attrs_ref(b, prefixo)}>{html_do_corpus(b["html"], sec["slug"], prefixo)}</p>' for b in blocos)
            partes.append(f'<section class="campo-caso" data-arq="passo declarado pelo 7.2 · texto literal"><h2>{esc(rotulo)}</h2><div class="texto">{corpo_campo}</div></section>')
        sub = ""
        if num == "7.2.7" and "7.2.7.1" in POR_NUMERO:
            s1 = POR_NUMERO["7.2.7.1"]
            texto_sub, achados = texto_marcado(s1["blocos"], s1["slug"], prefixo, destaques("7.2.7.1"), contador())
            lista = "".join(f'<li><a href="#{ident}">{esc(t["texto"])}</a> {pg(t["ref"])}</li>' for t, ident in achados)
            sub = (f'<section class="campo-caso subcaso" id="subcaso" data-arq="subcaso · texto integral do {esc(s1["n"])}"><h2>Subcaso · <span class="num-secao">{esc(s1["n"])} </span>{esc(s1["titulo"])}</h2>'
                   + (f'<nav class="indice-destaques" aria-label="O subcaso em frases da tese"><h3>Em frases da tese</h3><p class="nota-camada">Os trechos marcados foram escolhidos pelo site.</p><ol>{lista}</ol></nav>' if lista else "")
                   + f'<div class="texto">{texto_sub}</div>'
                   f'<p class="ler-pdf"><a href="{prefixo}tese/{s1["slug"]}/">Ler o subcaso no texto integral, com as notas</a></p></section>')
        notas = ""
        refs = set(re.findall(r'id="r(\d+)"', " ".join(b["html"] for b in sec["blocos"])))
        if refs:
            notas = f'<p class="ler-pdf"><a href="{prefixo}tese/{sec["slug"]}/#notas-titulo">Notas desta seção no texto integral</a></p>'
        e = EXTERNA.get(slug, {})
        externo = ""
        if e.get("titulo"):
            externo = (f'<a class="voltar" href="../">← Todas as plataformas</a>'
                       f'<header class="folha-cabeca ext-cabeca"><h1>{esc(ext_texto(slug, "titulo"))}</h1></header>'
                       f'<section class="ext">{ext_html(slug, "resumo", prefixo)}</section>'
                       + figura(f"familia-{slug}", prefixo) +
                       f'<section class="ext duvida">{botao_desnudar()}</section>')
        corpo = (f'<article class="folha leitura laboratorio">{externo}'
                 f'<div class="interno arquitetura" data-arq="arquitetura · a família de plataforma no texto integral">'
                 f'<header class="folha-cabeca"><p class="sobrelinha">Família de plataforma<span class="ciencia"> · {esc(sec["n"])} · p. {sec["pagina_inicio"]} a {sec["pagina_fim"]}</span></p>'
                 f'<h2 class="titulo-interno">{esc(sec["titulo"])}</h2><p class="ler-pdf"><a href="{prefixo}tese/{sec["slug"]}/">Ler a seção no texto integral</a></p>{notas}</header>'
                 + "".join(partes) + sub + "</div></article>")
        jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": sec["titulo"], "inLanguage": "pt-BR",
                  "url": f"{BASE}/laboratorio/{slug}/", "isBasedOn": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE}}
        destino = pasta / slug
        destino.mkdir(exist_ok=True)
        primeiro_txt = html.unescape(re.sub(r"<[^>]+>", " ", next((b["html"] for b in sec["blocos"] if b["tipo"] == "p"), "")))
        (destino / "index.html").write_text(
            pagina(f'{sec["titulo"]} · Laboratório · Lex Plataformae', ext_texto(slug, "resumo") or resumo(re.sub(r"\bp\. \d+\b", " ", primeiro_txt)), corpo, prefixo, f"laboratorio/{slug}/", jsonld, camada="mista", imagem=slug),
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
                 + pagina_lida(sec, prefixo, '<a href="../">Laboratório</a>', "Desdobramento da tipologia", num)
                 + "</article>")
        jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": sec["titulo"], "inLanguage": "pt-BR",
                  "url": f"{BASE}/laboratorio/{slug}/", "isBasedOn": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE}}
        destino = pasta / slug
        destino.mkdir(exist_ok=True)
        primeiro_txt = html.unescape(re.sub(r"<[^>]+>", " ", next((b["html"] for b in sec["blocos"] if b["tipo"] == "p"), "")))
        (destino / "index.html").write_text(
            pagina(f'{sec["titulo"]} · Laboratório · Lex Plataformae', resumo(re.sub(r"\bp\. \d+\b", " ", primeiro_txt)), corpo, prefixo, f"laboratorio/{slug}/", jsonld, superficie="../"),
            encoding="utf-8")
        cartoes_desdob.append(f'<li><a class="cartao" href="{slug}/"><b>{esc(sec["titulo"])}</b><span class="ciencia">{esc(sec["n"])} · p. {sec["pagina_inicio"]} a {sec["pagina_fim"]}</span></a></li>')

    teste, sec7 = paragrafo_que_comeca("7", "O teste, portanto")
    muda, _ = paragrafo_que_comeca("7.3", "O que emerge da análise dos modelos")
    origem = "".join(f'<li><a href="../tese/{POR_NUMERO[n]["slug"]}/">{esc(n)} {esc(POR_NUMERO[n]["titulo"])}</a></li>' for n in LABORATORIO_ORIGEM if n in POR_NUMERO)
    corpo = (
        '<article class="folha leitura laboratorio">'
        f'<header class="folha-cabeca ext-cabeca"><p class="sobrelinha-ext">Laboratório</p><h1>{esc(ext_texto("laboratorio", "titulo"))}</h1></header>'
        f'<section class="ext">{ext_html("laboratorio", "abertura", "../")}</section>'
        + figura("laboratorio", "../")
        + f'<section class="bloco"><h2>Quatro famílias de plataforma</h2><ul class="grade-conceitos">{"".join(cartoes)}</ul></section>'
        f'<section class="ext limite"><p class="rotulo-ext">Até onde vai</p>{ext_html("laboratorio", "limite", "../")}</section>'
        f'<section class="ext duvida">{botao_desnudar()}</section>'
        '<div class="interno arquitetura" data-arq="arquitetura · o laboratório no texto integral">'
        '<header class="folha-cabeca"><p class="sobrelinha ciencia">Laboratório · capítulo 7 do texto integral</p><h2 class="titulo-interno">A tipologia por dentro</h2>'
        + (f"<p>{html_do_corpus(sequencia, intro['slug'], '../')}</p>" if sequencia else "") + "</header>"
        + (f'<section class="bloco"><h2>O teste</h2><blockquote class="citacao"><p>{html_do_corpus(teste, sec7["slug"], "../")}</p></blockquote></section>' if teste else "")
        + (f'<section class="bloco"><h2>Desdobramentos da tipologia</h2><ul class="grade-conceitos">{"".join(cartoes_desdob)}</ul></section>' if cartoes_desdob else "")
        + (f'<section class="bloco"><h2>O que as famílias mostram</h2><blockquote class="citacao"><p>{html_do_corpus(triade, fecho["slug"], "../")}</p></blockquote></section>' if triade else "")
        + (f'<section class="bloco"><h2>O que muda quando o regime incide</h2><blockquote class="citacao"><p>{html_do_corpus(muda, fecho["slug"], "../")}</p></blockquote></section>' if muda else "")
        + (f'<section class="bloco ciencia" id="origem"><h2>O laboratório de origem</h2>{locus_html("../")}<ul class="lista-simples">{origem}</ul></section>' if origem else "")
        + "</div></article>")
    desc = "As famílias de plataforma em que a tese testa o regime do OIC, cada uma em quatro passos. Mecanismo, vulnerabilidade central, evidência e consequência dogmática possível, em texto literal."
    jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": "Laboratório · Lex Plataformae", "inLanguage": "pt-BR",
              "url": BASE + "/laboratorio/", "isBasedOn": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE}}
    desc = ext_texto("laboratorio", "abertura") or desc
    (pasta / "index.html").write_text(pagina("Laboratório · Lex Plataformae", desc, corpo, "../", "laboratorio/", jsonld, camada="mista", imagem="laboratorio"), encoding="utf-8")


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
    return f'<blockquote class="{classe}"><p>{html_do_corpus(h, sec["slug"], prefixo)} {pg(par["ref"], prefixo, _plano(h)[:90])}</p></blockquote>'


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
METODO_LIGACOES = {"2.3": ("O laboratório de origem", "laboratorio/#origem"), "2.6": ("As epígrafes", "#epigrafes")}


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
        f'<header class="folha-cabeca"><p class="sobrelinha">Método · capítulo 2 da tese · p. {cap["pagina_inicio"]} a {POR_NUMERO["2.7"]["pagina_fim"]}</p><h1>Método</h1>'
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
    (pasta / "index.html").write_text(pagina("Método · Lex Plataformae", desc, corpo, prefixo, "metodo/", jsonld, camada="ciencia", superficie=prefixo), encoding="utf-8")


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
          "eixos": [("Primeiro conjunto", "O primeiro reconstrói"), ("Segundo conjunto", "O segundo conjunto"), ("Terceiro conjunto", "O terceiro conjunto")],
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
    return (f'<div class="autor"><dt>{esc(nome)}</dt><dd><p class="onde"><span class="sobrelinha">Onde a tese o cita</span> {lista_onde}</p>'
            + (f'<ul class="refs" aria-label="Obras de {esc(nome)} na lista de referências">{refs}</ul>' if refs else "") + "</dd></div>")


def fichas_html(conc, prefixo):
    saida = ""
    for tipo, rotulo in (("conceito", "No Atlas"), ("roteiro", "No Roteiro"), ("bens", "Bens protegidos")):
        deste = [c for c in conc if c["tipo"] == tipo]
        if deste:
            saida += (f'<span class="cita"><span class="sobrelinha">{rotulo}</span> '
                      + ", ".join(f'<a href="{prefixo}conceitos/{c["id"]}/">{esc(c["nome"])}</a>' for c in em_ordem(deste)) + "</span>")
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
        '<header class="folha-cabeca"><p class="sobrelinha">Fundamentos · capítulos 3 e 4 da tese</p><h1>Fundamentos</h1>'
        + (citado(nao_exegese, POR_NUMERO["2"], prefixo, classe="citacao") if nao_exegese else "")
        + f'<p class="nota-camada">Cada capítulo abre declarando os autores que mobiliza e a função de cada um. A página segue essa declaração, em texto literal. A distinção entre objeto e instrumentos está no <a href="{prefixo}metodo/">Método</a>.</p>'
        + f'<nav class="indice-roteiro" aria-label="Capítulos"><ol>{indice}</ol></nav></header>'
        + "".join(blocos_cap) + "</article>")
    desc = "Os capítulos 3 e 4 da tese, organizados pelos autores e funções que a abertura de cada capítulo declara, com as seções em que cada autor é citado e as obras da lista de referências."
    jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": "Fundamentos · Lex Plataformae", "inLanguage": "pt-BR",
              "url": BASE + "/fundamentos/", "isBasedOn": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE},
              "mentions": [{"@type": "Person", "name": nome} for nome in dict.fromkeys(mencionados)]}
    pasta = SAIDA / "fundamentos"
    pasta.mkdir(exist_ok=True)
    (pasta / "index.html").write_text(pagina("Fundamentos · Lex Plataformae", desc, corpo, prefixo, "fundamentos/", jsonld, camada="ciencia", superficie=prefixo), encoding="utf-8")


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
        chave = (rotulo, tuple(t.get("nota") or t.get("artigo") for t in artigos))
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
            itens.append(f'<li class="artigo-lei" id="{ancora_lei}-{n}"><h3>{esc(rotulo)}</h3>{"".join(textos)}'
                         + (f'<p class="lei-fonte ciencia">Citado em {onde}.</p>' if onde else "") + "</li>")
        nav.append(f'<li><a href="#{ancora_lei}">{esc(nome)}</a></li>')
        grupos.append(f'<section class="bloco lei-grupo" id="{ancora_lei}" aria-labelledby="{ancora_lei}-titulo">'
                      f'<h2 id="{ancora_lei}-titulo">{esc(nome)}</h2><p class="lei-oficial">{esc(oficial)}</p><ol class="artigos-lei">{"".join(itens)}</ol></section>')
    corpo = ('<article class="folha leitura legislacao">'
             '<header class="folha-cabeca"><p class="sobrelinha">Para operar</p><h1>Legislação</h1>'
             '<p>Os artigos de lei que aparecem nas situações, nas diretrizes e nas plataformas, com o texto integral, para não precisar abrir a lei.</p></header>'
             f'<nav class="bloco indice-roteiro" aria-label="Leis"><h2>Por lei</h2><ol>{"".join(nav)}</ol></nav>'
             + "".join(grupos) + "</article>")
    jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": "Legislação · Lex Plataformae", "inLanguage": "pt-BR",
              "url": BASE + "/legislacao/", "isBasedOn": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE},
              "mentions": [{"@type": "Legislation", "name": NOME_LEI[c][1]} for c in ORDEM_LEIS if any(k[0] == c for k in dados)]}
    pasta = SAIDA / "legislacao"
    pasta.mkdir(exist_ok=True)
    desc = "Os artigos de lei que a tese usa, com o texto integral, organizados por lei, para quem vai advogar."
    (pasta / "index.html").write_text(pagina("Legislação · Lex Plataformae", desc, corpo, prefixo, "legislacao/", jsonld, superficie=prefixo, lei=False), encoding="utf-8")


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
        itens.append({"autoria": e["autoria"], "obra": obra, "pagina": a["pagina"], "url": url, "area": e["area"]})
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
                + esc(" · ".join(dict.fromkeys(re.sub(r"^.* ", "", i_["autoria"]) if i_["autoria"] else "fonte" for i_ in itens[:2])))
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
    return (f'<figure class="ficha"{estilo_area(area)}><figcaption class="autor">{esc(nome)}</figcaption>'
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
    for chave, a in autores.items():
        if a.get("proprio"):
            continue
        grupos.setdefault(a["area"], []).append(a)
        prefixo = "../../"
        lista = por_chave.get(chave, [])
        vistos, fichas = set(), []
        for c in lista:
            k = (c["frase"], c["slug"])
            if k in vistos:
                continue
            vistos.add(k)
            e = next(x for x in a["entradas"] if x["id"] == c["entrada"])
            fichas.append(ficha_citacao(c, e["autoria"], a["area"], prefixo, obra=", ".join(x for x in (e["autoria"], e["titulo"]) if x)))
        obras = "".join(f'<li id="{e["id"]}">{html_do_corpus(e["html"], "referencias", prefixo)}</li>' for e in a["entradas"])
        declarado = ""
        if chave in declarados or chave.replace(" JR", " JR.") in declarados:
            cap = "fundamentos/" if any(chave.startswith(k.rstrip(".")) for _, _, k in AUTORES) else "dogmatica/"
            declarado = f'<p class="nota-camada">A abertura de capítulo que declara a função deste autor está em <a href="{prefixo}{cap}">{"Fundamentos" if cap.startswith("f") else "Dogmática"}</a>.</p>'
        corpo = (f'<article class="folha leitura autor-citado"{estilo_area(a["area"])}>'
                 f'<nav class="trilha" aria-label="Você está em"><a href="../">Autores</a></nav>'
                 f'<header class="folha-cabeca"><p class="sobrelinha">{chip_area(a["area"])}</p><h1>{esc(a["nome"])}</h1>{declarado}</header>'
                 f'<section class="bloco"><h2>Na lista de referências</h2><ul class="refs-autor">{obras}</ul></section>'
                 f'<section class="bloco"><h2>Onde a tese o cita</h2><p class="nota-camada">{len(fichas)} trechos, na ordem da tese.</p>'
                 f'<div class="fichas">{"".join(fichas)}</div></section></article>')
        jsonld = {"@context": "https://schema.org", "@type": "ProfilePage", "url": f'{BASE}/autores/{a["slug"]}/',
                  "mainEntity": {"@type": "Person", "name": a["nome"]}, "isPartOf": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE}}
        destino = raiz / a["slug"]
        destino.mkdir(parents=True, exist_ok=True)
        a["citacoes"] = len(fichas)
        (destino / "index.html").write_text(
            pagina(f'{a["nome"]} · Autores · Lex Plataformae', f'{a["nome"]} na tese. As obras da lista de referências e os {len(fichas)} trechos em que a tese o cita.',
                   corpo, prefixo, f'autores/{a["slug"]}/', jsonld, camada="ciencia", superficie=prefixo), encoding="utf-8")
    secoes = []
    for area in ORDEM_AREAS:
        lista = sorted(grupos.get(area, []), key=lambda a: -a.get("citacoes", 0))
        if not lista:
            continue
        itens = "".join(f'<li><a href="{a["slug"]}/">{esc(a["nome"])}</a> <span class="vezes">{a.get("citacoes", 0)}</span></li>' for a in lista)
        secoes.append(f'<section class="bloco area-autores"{estilo_area(area)}><h2>{esc(AREA_NOME[area])}</h2><ul class="lista-autores">{itens}</ul></section>')
    corpo = ('<article class="folha leitura autores-indice"><header class="folha-cabeca"><h1>Autores</h1>'
             '<p>Os autores da lista de referências, pela área em que a tese os mobiliza, com o número de trechos que os citam.</p></header>'
             + "".join(secoes) + "</article>")
    jsonld = {"@context": "https://schema.org", "@type": "CollectionPage", "url": BASE + "/autores/", "name": "Autores · Lex Plataformae"}
    (raiz / "index.html").write_text(pagina("Autores · Lex Plataformae", "Os autores que a tese cita, por área, com os trechos em que aparecem.",
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
    (pasta / "index.html").write_text(pagina("Referências · Lex Plataformae", "A lista de referências da tese, com a área de cada entrada e as citações.",
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
        alvo = f'{prefixo}percurso/{parte["slug"]}/' if parte else None
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
                      f'<p class="rotulo-ext">Instrumentos no percurso</p><ul class="termos-lista">{"".join(termo_link(t) for t in termos)}</ul>'
                      f'<p class="rotulo-ext">Autores</p><ul class="autores-lista">{autores_da_area(area)}</ul></section>')
    juridicos = sorted(t for t, ar in AREA_TERMO.items() if ar == "direito")
    nove = "".join(f'<li><a class="chapado" href="{prefixo}conceitos/{c["id"]}/">{esc(c["nome"])}</a></li>' for c in [EIXO] + em_ordem([x for x in conceitos_do_atlas() if x is not EIXO]))
    dez = "".join(termo_link(t, "nome-derivado") for t in sorted(DERIVADOS))
    corpo = (
        '<article class="folha leitura objeto-instrumentos">'
        '<header class="folha-cabeca"><h1>Objeto e instrumentos</h1>' + trechos + '</header>'
        '<div class="movimento-geral" aria-label="O movimento">'
        f'<div{estilo_area("laboratorio")}><small>Objeto</small><b>O regime da plataforma, visto no laboratório</b></div>'
        '<div style="--area:var(--a-economia)"><small>Lente</small><b>A área que o lê</b></div>'
        f'<div{estilo_area("direito")}><small>Qualificação</small><b>A categoria jurídica</b></div>'
        '<div style="--area:var(--tese-linha)"><small>Tese</small><b>O conceito que a tese nomeia</b></div></div>'
        f'<section class="bloco etapa"{estilo_area("laboratorio")}><h2>O objeto</h2>'
        f'<p>O laboratório de origem e as famílias de plataforma estão em <a href="{prefixo}laboratorio/">Plataformas</a>. '
        f'A palavra do próprio objeto que o percurso usa é</p><ul class="termos-lista">{termo_link("Nerf")}</ul>'
        f'<p class="rotulo-ext">Fontes do laboratório</p><ul class="autores-lista">{autores_da_area("laboratorio", 8)}</ul></section>'
        f'<section class="bloco etapa"><h2>As lentes</h2><div class="lentes">{"".join(lentes)}</div></section>'
        f'<section class="bloco etapa"{estilo_area("direito")}><h2>A qualificação</h2><p class="rotulo-ext">Categorias jurídicas no percurso</p>'
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
        '<header class="folha-cabeca"><p class="sobrelinha">Dogmática · capítulos 5 e 6 da tese</p><h1>Dogmática</h1>'
        + (citado(base, POR_NUMERO["2.2"], prefixo) if base else "")
        + f'<p class="nota-camada">A página segue a abertura de cada capítulo, em texto literal. Os autores que a abertura do capítulo 5 nomeia aparecem com as seções que os citam e com as obras da lista de referências. Os conceitos de cada trecho levam ao <a href="{prefixo}">Atlas</a>.</p>'
        + f'<nav class="indice-roteiro" aria-label="Partes da página"><ol>{indice_cap}</ol></nav></header>'
        + "".join(blocos_cap) + disp + "</article>")
    desc = "Os capítulos 5 e 6 da tese, pela abertura de cada um, com os autores declarados, os conceitos de cada trecho e o índice dos dispositivos legais citados."
    jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": "Dogmática · Lex Plataformae", "inLanguage": "pt-BR",
              "url": BASE + "/dogmatica/", "isBasedOn": {"@type": "Thesis", "@id": BASE + "/#tese", "name": TITULO_TESE},
              "mentions": [{"@type": "Person", "name": nome} for nome in dict.fromkeys(mencionados)]
              + [{"@type": "Legislation", "name": lei} for lei in leis]}
    pasta = SAIDA / "dogmatica"
    pasta.mkdir(exist_ok=True)
    (pasta / "index.html").write_text(pagina("Dogmática · Lex Plataformae", desc, corpo, prefixo, "dogmatica/", jsonld, camada="ciencia", superficie=prefixo), encoding="utf-8")


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
            anota(termos_em(texto_de(blocos)), "Laboratório", POR_NUMERO[num]["titulo"], f"laboratorio/{slug}/")
    for num, slug in DESDOBRAMENTOS:
        if num in POR_NUMERO:
            anota(termos_em(texto_de(POR_NUMERO[num]["blocos"])), "Laboratório", POR_NUMERO[num]["titulo"], f"laboratorio/{slug}/")
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
    junta("1", "Laboratório", "O laboratório de origem", "laboratorio/#origem")
    junta("2.6", "Epígrafes", "As nove epígrafes", "#epigrafes")
    junta("5.1.2.3", "Roteiro", "O portão de entrada", "roteiro/#portao")
    junta("7.1", "Roteiro", "Partes do Roteiro", "roteiro/")
    junta("7.1.1", "Roteiro", "Por que a ordem importa", "roteiro/")
    for letra, (num, _) in ROTEIRO_MAPA.items():
        if num:
            junta(num, "Roteiro", f"Bloco {letra} do enquadramento", f"roteiro/#{letra}")
    junta("7.1.2", "Roteiro", "Os onze blocos de enquadramento", "roteiro/")
    junta("7.1.3", "Roteiro", "As dez diretrizes de controle", "roteiro/diretrizes/")
    junta("7.1.4", "Roteiro", "Cidadania digital e limites", "roteiro/limites/")
    junta("7", "Laboratório", "O teste", "laboratorio/")
    junta("7.2", "Laboratório", "A sequência de cada família", "laboratorio/")
    for num, slug in FAMILIAS:
        if num in POR_NUMERO:
            junta(num, "Laboratório", "Família de plataforma", f"laboratorio/{slug}/")
    junta("7.2.7.1", "Laboratório", "Subcaso da administração de confiança", "laboratorio/administracao-de-confianca/#subcaso")
    for num, slug in DESDOBRAMENTOS:
        junta(num, "Laboratório", "Desdobramento da tipologia", f"laboratorio/{slug}/")
    junta("7.3", "Laboratório", "O que as famílias mostram", "laboratorio/")
    for num in LABORATORIO_ORIGEM:
        junta(num, "Laboratório", "O laboratório de origem", "laboratorio/#origem")
    for p in D["percursos"].values():
        alvo = destino_pagina(p["trecho"]["ref"], "", p["trecho"]["texto"])
        m = re.match(r"tese/([^/]+)/", alvo or "")
        if m:
            sec = next((s for s in SECOES if s["slug"] == m.group(1)), None)
            if sec and sec["n"]:
                junta(sec["n"], "Atlas", "Três leituras da tese", "#leituras-titulo")
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
    urls = [BASE + "/", BASE + "/percurso/", BASE + "/direitos/"] + [f'{BASE}/percurso/{parte["slug"]}/' for parte in PERCURSO] + [url_conceito(c["id"]) for c in D["conceitos"]] + [BASE + "/tese/"] + [f'{BASE}/tese/{x["slug"]}/' for x in SECOES] + [BASE + "/roteiro/", BASE + "/roteiro/diretrizes/", BASE + "/roteiro/limites/", BASE + "/laboratorio/", BASE + "/fundamentos/", BASE + "/metodo/", BASE + "/dogmatica/", BASE + "/legislacao/", BASE + "/autores/", BASE + "/referencias/", BASE + "/objeto-e-instrumentos/", BASE + "/autor/"] + [f'{BASE}/autores/{a["slug"]}/' for a in autores_pessoas().values() if not a.get("proprio")] + [f"{BASE}/laboratorio/{slug}/" for _, slug in FAMILIAS + DESDOBRAMENTOS]
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
        "## Percurso",
        "",
        "A primeira vista do site conta a tese inteira a partir da compra de uma skin, em linguagem simples, com os trechos literais da tese por baixo de cada bloco.",
        "",
    ] + [f"- [{parte['titulo']}]({BASE}/percurso/{parte['slug']}/): {parte['resumo']}" for parte in PERCURSO] + [
        "",
        "## Seus direitos",
        "",
        f"- [Seus direitos]({BASE}/direitos/): o que a plataforma deve e o que o consumidor pode pedir, em linguagem simples, uma situação por bloco, com os trechos literais da tese por baixo.",
    ] + [f"- [{DIREITOS[l]['titulo']}]({BASE}/direitos/#{l})" for l in LETRAS_DIREITOS] + [
        "",
        "## Conceitos",
        "",
    ]
    for c in [EIXO] + em_ordem([x for x in conceitos_do_atlas() if x is not EIXO]):
        can = canonica(c)
        linhas.append(f"- [{c['nome']}]({url_conceito(c['id'])}): {can['texto']} ({can['ref']})")
    linhas += ["", "## Roteiro", "", f"- [Roteiro]({BASE}/roteiro/): os onze blocos de enquadramento do 7.1.2 da tese, com hipótese de incidência, dever de fornecimento, prova mínima, qualificação jurídica e consequência institucional, em texto literal.",
               f"- [Diretrizes de controle]({BASE}/roteiro/diretrizes/): as dez diretrizes do 7.1.3 para o controle de arquitetura e governança, em texto literal.",
               f"- [Cidadania digital e limites]({BASE}/roteiro/limites/): o 7.1.4, sobre os limites ao poder privado de plataforma, em texto integral."]
    linhas += ["", "## Laboratório", "", f"- [Laboratório]({BASE}/laboratorio/): as famílias de plataforma em que a tese testa o regime do OIC, cada uma em quatro passos, em texto literal."]
    linhas += [f"- [{POR_NUMERO[n]['titulo']}]({BASE}/laboratorio/{slug}/): seção {n} da tese" for n, slug in FAMILIAS if n in POR_NUMERO]
    linhas += [f"- [{POR_NUMERO[n]['titulo']}]({BASE}/laboratorio/{slug}/): seção {n} da tese, desdobramento da tipologia" for n, slug in DESDOBRAMENTOS if n in POR_NUMERO]
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
             '<h1>Este endereço não existe</h1></header><p>Talvez o conceito tenha mudado de endereço. '
             '<a href="/#conceitos">Volte às ideias</a> e procure por ele.</p></article>')
    (SAIDA / "404.html").write_text(pagina("Página não encontrada · Lex Plataformae", "Página não encontrada.", corpo, "/", "404.html", camada="externa"), encoding="utf-8")


TRAJETORIA = ["A percepção de que o consumo digital", "Esta tese não nasce", "Essa dificuldade de ignorar"]
# Perfis do autor, informados por ele em 27/10/2026. O ORCID fica para outro momento.
AUTOR_LATTES = "https://lattes.cnpq.br/3172009565979544"
AUTOR_LINKEDIN = "https://www.linkedin.com/in/victorlpandrade/"


def gerar_autor():
    """A camada mais interna. Quem chega aqui fica sabendo, por último, que tudo deriva de uma tese de doutorado."""
    prefixo = "../"
    intro = POR_NUMERO.get("1")
    trajetoria = ""
    if intro:
        pars = [p for p in paragrafos(intro) if any(_plano(p["bloco"]["html"]).strip().startswith(t) for t in TRAJETORIA)]
        trajetoria = "".join(citado(p, intro, prefixo) for p in pars)
    corpo = (
        '<article class="folha autor-pagina">'
        '<header class="folha-cabeca ext-cabeca"><p class="sobrelinha-ext">Quem está por trás destas ideias</p><h1>Victor L. P. Andrade</h1></header>'
        '<section class="ext"><p>Tudo o que você leu neste site deriva de uma tese de doutorado em Direito, '
        'apresentada à Universidade Estadual Paulista e defendida em 30 de março de 2026, sob a orientação da Prof.ª Dr.ª Luciana Lopes Canavez.</p>'
        '<p class="referencia">ANDRADE, Victor Luiz Pereira de. <b>Do regime jurídico do Objeto Imaterial de Consumo (OIC) sob a Lex Plataformae</b>. '
        'A tutela da vulnerabilidade semiótica do consumidor à luz da ordem constitucional e econômica do Brasil. 2026. '
        'Tese (Doutorado em Direito). Universidade Estadual Paulista, Faculdade de Ciências Humanas e Sociais, Franca, 2026.</p>'
        f'<p class="acoes"><a class="botao" href="{prefixo}tese/{PDF_NOME}">Ler a tese completa em PDF</a> <a href="{prefixo}tese/">Ler seção por seção</a></p></section>'
        + (f'<section class="bloco"><h2>Como este trabalho nasceu</h2>{trajetoria}</section>' if trajetoria else "")
        + '<section class="ext fim-percurso" aria-labelledby="fim-titulo"><h2 class="rotulo-ext" id="fim-titulo">Fim do percurso</h2>'
        f'<p>A trajetória acadêmica completa está no <a href="{AUTOR_LATTES}" rel="me noopener">Currículo Lattes</a>.</p>'
        '<p>Para conversar sobre estas ideias, o caminho é o LinkedIn.</p>'
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


def gerar_cobertura():
    """Escreve estrutura/cobertura.md, com o lugar de cada seção da tese nas camadas do site.
    O autor determinou em 27/10/2026 que tudo o que está na tese será trazido para a estrutura do site.
    Este mapa mostra o caminho percorrido e o que falta."""
    por_secao, usos = conceitos_por_secao(), usos_por_secao()
    linhas = ["# Cobertura da tese nas camadas do site", "",
              "Arquivo gerado por `ferramentas/gerar_site.py`. Não editar à mão.", "",
              "Toda seção está no corpus, em texto integral. Esta tabela mostra em que outras camadas cada seção já tem lugar. "
              "Seção sem camada ainda não foi trazida para a estrutura.", "",
              "| Seção | Título | Páginas | Camadas |", "|---|---|---|---|"]
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
        linhas.append(f'| {sec["n"] or "-"} | {titulo} | {sec["pagina_inicio"]} a {sec["pagina_fim"]} | {"; ".join(camadas) or "corpus apenas"} |')
    total = com + len(sem)
    linhas[6:6] = [f"{com} de {total} seções já têm lugar em alguma camada. Faltam {len(sem)}.", ""]
    (RAIZ / "estrutura").mkdir(exist_ok=True)
    (RAIZ / "estrutura" / "cobertura.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"Cobertura  {com} de {total} seções com lugar numa camada")


def main():
    if SAIDA.exists():
        shutil.rmtree(SAIDA)
    SAIDA.mkdir()
    gerar_estilo()
    gerar_inicio()
    gerar_percurso()
    gerar_direitos()
    for c in D["conceitos"]:
        gerar_conceito(c)
    gerar_tese()
    gerar_roteiro()
    gerar_diretrizes()
    gerar_limites()
    gerar_laboratorio()
    gerar_fundamentos()
    gerar_metodo()
    gerar_dogmatica()
    gerar_legislacao()
    gerar_autores()
    gerar_referencias()
    gerar_objeto_instrumentos()
    gerar_autor()
    gerar_auxiliares()
    paginas = len(list(SAIDA.rglob("*.html")))
    print(f"{paginas} páginas geradas em docs/")
    todos = {(t["texto"], t["ref"]) for lista in DESTAQUES.values() for t in lista}
    for texto, ref in sorted(todos - DESTAQUES_USADOS):
        print(f"Destaque sem lugar no site  {ref}  {texto[:70]}")
    print(f"{len(todos & DESTAQUES_USADOS)} de {len(todos)} destaques marcados no texto")
    prontas = sum(1 for i in ILUSTRACOES if arquivo_ilustracao(i))
    print(f"Ilustrações  {len(ILUSTRACOES)} previstas, {prontas} com arquivo, {len(ILUSTRACOES_USADAS)} com lugar no site")
    for i in sorted(set(ILUSTRACOES) - ILUSTRACOES_USADAS):
        print(f"Ilustração sem lugar no site  {i}")
    gerar_cobertura()


if __name__ == "__main__":
    main()
