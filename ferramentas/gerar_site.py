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
VERSAO = "0.3"
PDF_NOME = "andrade-2026-tese-oic-lex-plataformae.pdf"

D = json.loads((RAIZ / "dados" / "atlas.json").read_text(encoding="utf-8"))
POR_ID = {c["id"]: c for c in D["conceitos"]}
EIXO = next(c for c in D["conceitos"] if c.get("eixo"))

TITULO_TESE = ("Do regime jurídico do Objeto Imaterial de Consumo (OIC) sob a Lex Plataformae: "
               "a tutela da vulnerabilidade semiótica do consumidor à luz da ordem constitucional e econômica do Brasil")


def esc(t):
    return html.escape(str(t), quote=True)


def pg(ref):
    return f'<span class="pg" data-arq="âncora · página da tese">{esc(ref)}</span>'


def com_ancoras(texto):
    return re.sub(r"\((p\. [\d\-]+|Resumo)\)", lambda m: pg(m.group(1)), esc(texto))


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


def pagina(titulo, descricao, corpo, prefixo, caminho, jsonld=None):
    canonico = BASE + "/" + caminho
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(descricao)}">
<link rel="canonical" href="{esc(canonico)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Lex Plataformae">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(descricao)}">
<meta property="og:url" content="{esc(canonico)}">
<meta property="og:locale" content="pt_BR">
<link rel="stylesheet" href="{prefixo}assets/estilo.css">
<link rel="alternate" type="application/json" href="{prefixo}dados/atlas.json" title="Dados do Atlas">
{ld}
</head>
<body>
<div class="moldura">
  <div class="faixa" data-arq="versão · o site cresce em público e cada mudança fica registrada">
    <span>Versão {VERSAO} · em construção</span>
    <span>Citações conferidas por script contra a tese</span>
  </div>
  <header class="topo">
    <a class="topo-marca" href="{prefixo}">Lex Plataformae</a>
    <nav aria-label="Seções">
      <ul>
        <li><a href="{prefixo}">Atlas</a></li>
        <li class="em-breve">Roteiro<small>em breve</small></li>
        <li class="em-breve">Laboratório<small>em breve</small></li>
        <li><a href="{prefixo}#epigrafes">Epígrafes</a></li>
        <li><a href="{prefixo}tese/{PDF_NOME}">Tese em PDF</a></li>
      </ul>
    </nav>
    <label class="chave" for="desnudar">
      <input type="checkbox" id="desnudar">
      Desnudar a arquitetura
    </label>
  </header>
  <p class="legenda-desnudo" role="note">Arquitetura à mostra. Cada contorno tracejado é uma peça da página, e a etiqueta diz o que ela é e de onde vem. As caixas em volta dos números de página são âncoras na tese. Nada nesta página afirma algo sem apontar a página que sustenta.</p>
  <main>
{corpo}
  </main>
  <footer class="rodape">
    <p>ANDRADE, Victor Luiz Pereira de. Do regime jurídico do Objeto Imaterial de Consumo (OIC) sob a Lex Plataformae. A tutela da vulnerabilidade semiótica do consumidor à luz da ordem constitucional e econômica do Brasil. 2026. Tese (Doutorado em Direito). Universidade Estadual Paulista, Faculdade de Ciências Humanas e Sociais, Franca, 2026. <a href="{prefixo}tese/{PDF_NOME}">Ler a tese completa em PDF</a>.</p>
    <p>Todo texto entre aspas é transcrição literal da tese, com a página indicada. Acréscimos posteriores à tese aparecem marcados e datados. O código do site e o histórico de cada alteração são públicos <a href="{REPO}">no GitHub</a>. Todos os direitos reservados até a definição da licença do projeto.</p>
  </footer>
</div>
<script src="{prefixo}assets/atlas.js" defer></script>
</body>
</html>
"""


def html_passo(passo, base):
    c = POR_ID.get(passo["id"])
    extra = D["passos"].get(passo["id"])

    def link(cid, nome):
        return f'<a href="{base}{cid}/">{esc(nome)}</a>'

    if c and c["tipo"] == "conceito":
        nome = link(c["id"], c["nome"])
        if passo.get("par") and passo["par"] in POR_ID:
            dica = "Gêmeos por decisão do autor" if passo["par_rotulo"] == "gêmeos" else "A tese trata os dois juntos em 5.1.3, 6.4 e 7.1.1.7"
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


def gerar_inicio():
    padrao = "regime"
    oic_def = canonica(EIXO)
    nota = campo(EIXO, "Nota do autor")
    nota_txt = re.sub(r"^Acréscimo posterior à tese, de [\d/]+\.\s*", "", nota["texto"]) if nota else ""
    gemeo = POR_ID[EIXO["par"]["id"]] if EIXO.get("par") else None
    independentes = em_ordem([c for c in conceitos_do_atlas() if c is not EIXO and not (gemeo and c is gemeo)])
    base = "conceitos/"

    cartoes = "".join(
        f'<li><a class="cartao" href="{base}{c["id"]}/"><b>{esc(c["nome"])}</b>'
        f'<span>{com_ancoras(primeira_frase((campo(c, "Função no regime") or {"texto": ""})["texto"]))}</span></a></li>'
        for c in independentes
    )
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
    }

    ep = D["epigrafes"]
    musas = "".join(
        f'<li><div>{esc(e["artista"])}, <cite>{esc(e["faixa"])}</cite> ({e["ano"]})<small>abre {esc(e["abre"])}</small></div></li>'
        for e in ep["epigrafes"]
    )
    ab = D["abertura"]

    corpo = f"""
    <section class="abertura" aria-labelledby="titulo">
      <p class="sobrelinha">Tese de doutorado · UNESP · 2026</p>
      <h1 class="marca" id="titulo">Lex Plataformae</h1>
      <p class="lema">Atlas do regime jurídico do Objeto Imaterial de Consumo. A partir da tese de Victor L. P. Andrade.</p>
      <blockquote class="frase" data-arq="citação literal · conferida por script contra a tese">“{esc(ab["texto"])}”{pg(ab["ref"])}</blockquote>
    </section>

    <section class="campo" aria-labelledby="eixo-nome" data-arq="integração · conceitos independentes que funcionam integrados sob o OIC">
      <div class="campo-topo">
        <p class="campo-rotulo">Sob o OIC</p>
        <h2 class="campo-nome" id="eixo-nome"><a href="{base}{EIXO["id"]}/">{esc(EIXO["nome"])}</a></h2>
        {f'<p class="campo-gemeo"><span class="gemeos-sinal">gêmeos</span> <a href="{base}{gemeo["id"]}/">{esc(gemeo["nome"])}</a></p>' if gemeo else ""}
        <p class="campo-def">“{esc(oic_def["texto"])}”{pg(oic_def["ref"])}</p>
        {f'<div class="nota-autor" data-arq="acréscimo posterior · fora do texto da tese de 2026"><p class="sobrelinha">Nota do autor · 26/10/2026</p><p>{esc(nota_txt)}</p></div>' if nota_txt else ""}
      </div>
      <ul class="grade-conceitos" data-arq="conceitos independentes · sem ordem nem hierarquia">{cartoes}</ul>
    </section>

    <section class="secao leituras" aria-labelledby="leituras-titulo">
      <h2 id="leituras-titulo">Três leituras da tese</h2>
      <p>A tese também percorre os conceitos em três ordens. São leituras do texto, não hierarquia entre os conceitos. Elas vão compor o Roteiro.</p>
      <fieldset class="percursos">
        <legend>Escolha uma leitura</legend>
        <div class="seletor">{opcoes}</div>
        <p class="logica" id="logica" aria-live="polite">{esc(p["logica"])} <q>{esc(p["trecho"]["texto"])}</q>{pg(p["trecho"]["ref"])}</p>
      </fieldset>
      <ul class="sequencia" id="sequencia" data-base="{base}" aria-label="{esc(p["nome"])}" data-arq="leitura · ordem do texto da tese, não hierarquia">{passos}</ul>
      <div class="fora" id="fora">{fora}</div>
      <script type="application/json" id="leituras-dados">{json.dumps(dados_leituras, ensure_ascii=False).replace("</", "<\\/")}</script>
    </section>

    <section class="secao" id="epigrafes" aria-labelledby="epigrafes-titulo">
      <h2 id="epigrafes-titulo">As nove epígrafes</h2>
      <p>A tese abre cada etapa com uma canção. São nove, como as nove Musas. Juntas, fazem o mesmo percurso do argumento, do medo à fermata. Seção 2.6 da tese{pg("p. 73-78")}</p>
      <ol class="epigrafes">{musas}</ol>
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
    desc = "Atlas do regime jurídico do Objeto Imaterial de Consumo (OIC) sob a Lex Plataformae, a partir da tese de doutorado de Victor L. P. Andrade (UNESP, 2026)."
    (SAIDA / "index.html").write_text(pagina("Lex Plataformae", desc, corpo, "", "", jsonld), encoding="utf-8")


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
        rot = "Gêmeo de " if c["par"]["rotulo"] == "gêmeos" else "Em par com "
        selos += f'<a class="selo gemeo" href="{base}{c["par"]["id"]}/">{rot}{esc(POR_ID[c["par"]["id"]]["nome"])}</a>'

    partes = []
    for f in c["campos"]:
        r = f["rotulo"]
        if r == "Onde vive":
            itens = re.split(r",\s*(?![^()]*\))", f["texto"].rstrip("."))
            partes.append('<section class="bloco"><h2>Onde vive na tese</h2><ul class="lugares" data-arq="âncora · seções da tese">'
                          + "".join(f"<li>{esc(i.strip())}</li>" for i in itens) + "</ul></section>")
            continue
        if r == "Nota do autor":
            partes.append('<section class="nota-autor" data-arq="acréscimo posterior · fora do texto da tese de 2026">'
                          f'<p class="sobrelinha">Nota do autor</p><p>{esc(f["texto"])}</p></section>')
            continue
        bloco = f'<section class="bloco"><h2>{esc(r)}</h2>'
        if f["texto"]:
            bloco += f"<p>{com_ancoras(f['texto'])}</p>"
        for q in f["citacoes"]:
            if r == "Definição canônica proposta":
                bloco += ('<blockquote class="citacao canonica" data-arq="citação literal · conferida por script contra a tese">'
                          f'<p><mark>{esc(q["texto"])}</mark>{pg(q["ref"])}</p></blockquote>')
            else:
                classe = "citacao nao-e" if r == "O que não é" else "citacao"
                bloco += f'<blockquote class="{classe}"><p>{esc(q["texto"])}{pg(q["ref"])}</p></blockquote>'
        partes.append(bloco + "</section>")

    linhas = []
    for p in D["percursos"].values():
        for s in p["sequencia"]:
            if s["id"] == c["id"] or s.get("par") == c["id"]:
                linhas.append(f'<li><b>{esc(p["nome"])}</b><span>{esc(s["papel"])}</span></li>')
    if linhas:
        partes.append('<section class="bloco"><h2>Nas leituras da tese</h2><ul class="nos-percursos">' + "".join(linhas) + "</ul></section>")
    elif c["tipo"] == "conceito":
        partes.append('<section class="bloco"><h2>Nas leituras da tese</h2><p>Não aparece em nenhuma das três sequências da tese.</p></section>')

    if c["tipo"] == "conceito":
        outros = em_ordem([x for x in conceitos_do_atlas() if x is not c and not x.get("eixo")])
        lista = ([] if c.get("eixo") else [EIXO]) + outros
        partes.append('<nav class="outros" aria-label="Os outros conceitos"><h2>Os outros conceitos</h2><ul>'
                      + "".join(f'<li><a href="{base}{x["id"]}/">{esc(x["nome"])}</a></li>' for x in lista) + "</ul></nav>")

    corpo = (f'<article class="folha"><a class="voltar" href="{prefixo}">← Voltar ao Atlas</a>'
             f'<header class="folha-cabeca"><p class="sobrelinha">{esc(sobre)}</p><h1>{esc(c["nome"])}</h1><div class="selos">{selos}</div></header>'
             + "".join(partes) + "</article>")
    can = canonica(c)
    desc = resumo(can["texto"]) if can else c["nome"]
    jsonld = {"@context": "https://schema.org", "@type": "DefinedTerm", "@id": url_conceito(c["id"]), "name": c["nome"],
              "description": can["texto"] if can else "", "url": url_conceito(c["id"]), "inLanguage": "pt-BR",
              "inDefinedTermSet": {"@type": "DefinedTermSet", "@id": BASE + "/#atlas", "name": "Atlas Lex Plataformae"}}
    destino = SAIDA / "conceitos" / c["id"]
    destino.mkdir(parents=True, exist_ok=True)
    (destino / "index.html").write_text(
        pagina(f'{c["nome"]} · Lex Plataformae', desc, corpo, prefixo, f'conceitos/{c["id"]}/', jsonld), encoding="utf-8")


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
    assets = SAIDA / "assets"
    (assets / "fontes").mkdir(parents=True, exist_ok=True)
    (assets / "estilo.css").write_text(fontes + css + "\n" + extra, encoding="utf-8")
    for arq in (RAIZ / "ferramentas" / "fontes").iterdir():
        shutil.copy(arq, assets / "fontes" / arq.name)
    shutil.copy(RAIZ / "site" / "atlas.js", assets / "atlas.js")


def gerar_auxiliares():
    (SAIDA / "CNAME").write_text("lexplataformae.com.br\n", encoding="utf-8")
    (SAIDA / ".nojekyll").write_text("", encoding="utf-8")
    (SAIDA / "robots.txt").write_text(
        "# O conteúdo deste site é para ser lido por pessoas, buscadores e modelos de IA.\n"
        "User-agent: *\nAllow: /\n\n"
        + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in ("GPTBot", "ClaudeBot", "Claude-Web", "anthropic-ai", "Google-Extended", "CCBot", "PerplexityBot", "Applebot-Extended"))
        + f"Sitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    urls = [BASE + "/"] + [url_conceito(c["id"]) for c in D["conceitos"]]
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
        "Os nove conceitos são independentes e, sob o OIC, funcionam de forma integrada (nota do autor, 26/10/2026).",
        "",
        "## Conceitos",
        "",
    ]
    for c in [EIXO] + em_ordem([x for x in conceitos_do_atlas() if x is not EIXO]):
        can = canonica(c)
        linhas.append(f"- [{c['nome']}]({url_conceito(c['id'])}): {can['texto']} ({can['ref']})")
    linhas += ["", "## Tese", "", f"- [Tese completa em PDF]({BASE}/tese/{PDF_NOME}): {TITULO_TESE}. Doutorado em Direito, UNESP, 2026.",
               "", "## Dados", "", f"- [atlas.json]({BASE}/dados/atlas.json): conceitos, definições, critérios delimitadores, seções e leituras, em JSON.", ""]
    (SAIDA / "llms.txt").write_text("\n".join(linhas), encoding="utf-8")
    (SAIDA / "dados").mkdir(exist_ok=True)
    shutil.copy(RAIZ / "dados" / "atlas.json", SAIDA / "dados" / "atlas.json")
    shutil.copy(RAIZ / "dados" / "epigrafes.json", SAIDA / "dados" / "epigrafes.json")
    (SAIDA / "tese").mkdir(exist_ok=True)
    shutil.copy(RAIZ / "tese" / PDF_NOME, SAIDA / "tese" / PDF_NOME)
    corpo = ('<article class="folha"><header class="folha-cabeca"><p class="sobrelinha">Página não encontrada</p>'
             '<h1>Este endereço não existe</h1></header><p>Talvez o conceito tenha mudado de endereço. '
             '<a href="/">Volte ao Atlas</a> e procure por ele.</p></article>')
    (SAIDA / "404.html").write_text(pagina("Página não encontrada · Lex Plataformae", "Página não encontrada.", corpo, "/", "404.html"), encoding="utf-8")


def main():
    if SAIDA.exists():
        shutil.rmtree(SAIDA)
    SAIDA.mkdir()
    gerar_estilo()
    gerar_inicio()
    for c in D["conceitos"]:
        gerar_conceito(c)
    gerar_auxiliares()
    paginas = len(list(SAIDA.rglob("*.html")))
    print(f"{paginas} páginas geradas em docs/")


if __name__ == "__main__":
    main()
