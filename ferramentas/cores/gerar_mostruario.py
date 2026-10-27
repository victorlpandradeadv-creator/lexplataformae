"""Gera estrutura/paletas.html, o mostruário das cores propostas. Lê estrutura/cores.json."""
import base64, html, itertools, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from cor import contraste, dist, simular

RAIZ = Path(__file__).resolve().parents[2]
C = json.loads((RAIZ / "estrutura/cores.json").read_text(encoding="utf-8"))
A, T, TESE, MARCA = C["areas"], C["telas"], C["tese"], C["marca"]
e = html.escape


def fonte(nome):
    return base64.b64encode((RAIZ / "ferramentas/fontes" / nome).read_bytes()).decode()


FONTES = f"""
@font-face {{ font-family: "Archivo"; font-weight: 100 900; font-stretch: 62% 125%; src: url(data:font/woff2;base64,{fonte('archivo-latin-wdth-normal.woff2')}) format("woff2"); }}
@font-face {{ font-family: "Newsreader"; font-style: normal; font-weight: 200 800; src: url(data:font/woff2;base64,{fonte('newsreader-latin-opsz-normal.woff2')}) format("woff2"); }}
@font-face {{ font-family: "Newsreader"; font-style: italic; font-weight: 200 800; src: url(data:font/woff2;base64,{fonte('newsreader-latin-opsz-italic.woff2')}) format("woff2"); }}
@font-face {{ font-family: "IBM Plex Mono"; font-weight: 400; src: url(data:font/woff2;base64,{fonte('ibm-plex-mono-latin-400-normal.woff2')}) format("woff2"); }}
@font-face {{ font-family: "IBM Plex Mono"; font-weight: 500; src: url(data:font/woff2;base64,{fonte('ibm-plex-mono-latin-500-normal.woff2')}) format("woff2"); }}
"""

ORDEM = ["direito", "economia", "tecnica", "antropologia", "semiotica", "poder", "laboratorio"]
AUTORES = {"direito": "Marques · Barbosa · Miragem", "economia": "Dowbor · Varoufakis · Marx",
           "tecnica": "Feenberg · Ellul · Vanderburg", "antropologia": "Douglas · Durkheim · Appadurai",
           "semiotica": "Eco · Debord · Baudrillard", "poder": "Han · Ribble · Lesnovski",
           "laboratorio": "Riot Games · LoL Wiki · Moonbell"}
PORQUE = {
    "direito": "Vermelho, por escolha do autor. É a cor do limite e da norma, e é no Direito que a leitura vira qualificação.",
    "economia": "Âmbar, a cor da moeda, da renda e do pedágio.",
    "tecnica": "Turquesa, a luz da tela, que essa área lê como ambiente de vida.",
    "antropologia": "Verde musgo, a vida social das coisas e a cultura material, que crescem devagar no uso.",
    "semiotica": "Violeta, a cor tradicional do signo e do imaginário, longe do vermelho e do âmbar.",
    "poder": "Magenta. O vermelho do Direito proíbe. O poder que a tese lê em Han não proíbe, convida, e por isso fica num vermelho que seduz em vez de vetar.",
    "laboratorio": "Cinza cru. O objeto ainda não passou por lente nenhuma, e por isso fica sem tinta. O texto vai em grafite.",
}
NOVE = ["Objeto Imaterial de Consumo", "Lex Plataformae", "vulnerabilidade semiótica", "teleologia abusiva",
        "ilícito de arquitetura", "antecipação hipercuratorial", "auditabilidade aberta",
        "equivalência de valor funcional", "feixe de fruição governada"]
DEZ = ["teleologia arquitetural", "cativeiro identitário", "consumidor-cidadão", "transparência performática",
       "consentimento viciado por sentido", "publicidade enganosa por arquitetura semiótica",
       "continuidade biográfica", "recomposição funcional", "correção de regime", "dano-arquitetura"]
MENU = {
    "informacao": ["Percurso", "Ideias", "Outras plataformas", "Seus direitos"],
    "doutrina": ["Situações", "Diretrizes", "Plataformas", "Conceitos", "Legislação"],
    "ciencia": ["Método", "Fundamentos", "Dogmática", "Objeto e instrumentos", "Autores", "Referências"],
}
NOME_MODO = {"informacao": "Informação", "doutrina": "Doutrina", "ciencia": "Ciência"}
REF_TESE = "Victor L. P. Andrade, Do regime jurídico do Objeto Imaterial de Consumo sob a Lex Plataformae, 2026"


def vars_tela(modo, tom):
    t = T[modo][tom]
    oposto = T["informacao"]["claro" if tom == "escuro" else "escuro"]
    v = {"--papel": t["papel"], "--folha": t.get("folha", t["papel"]), "--tinta": t["tinta"], "--tinta2": t["tinta2"],
         "--linha": t["linha"], "--inv-papel": oposto["papel"], "--inv-tinta": oposto["tinta"],
         "--tese-texto": TESE["texto"] if tom == "claro" else TESE["texto_escuro"],
         "--tese-linha": TESE["chapado"] if tom == "claro" else TESE["marca_escuro"],
         "--dir-texto": A["direito"]["texto"] if tom == "claro" else A["direito"]["texto_escuro"],
         "--dir-marca": A["direito"]["destaque"] if tom == "claro" else A["direito"]["destaque_escuro"],
         "--f-papel": T["ficha"][tom]["papel"], "--f-tinta": T["ficha"][tom]["tinta"],
         "--f-tinta2": T["ficha"][tom]["tinta2"], "--f-pauta": T["ficha"][tom]["pauta"]}
    if modo == "ciencia":
        v.update({"--traco": t["traco"], "--grade": t["grade"]})
    for k in ORDEM:
        v[f"--{k}"] = A[k]["destaque"] if tom == "claro" else A[k]["destaque_escuro"]
        v[f"--{k}-t"] = A[k]["texto"] if tom == "claro" else A[k]["texto_escuro"]
    v["--modo-cor"] = {"informacao": TESE["chapado"], "doutrina": v["--dir-marca"], "ciencia": v.get("--traco", t["tinta2"])}[modo]
    v["--modo-tinta"] = "#ffffff" if modo != "ciencia" else t["papel"]
    return ";".join(f"{k}:{val}" for k, val in v.items())


def topo(modo):
    itens = "".join(f"<span>{e(i)}</span>" for i in MENU[modo])
    return (f'<header class="t-topo"><span class="t-marca">Lex Plataformae</span><nav class="t-menu">{itens}</nav>'
            f'<span class="t-integral">Texto integral</span></header>')


def pe(modo):
    chips = "".join(f'<b class="ativo">{NOME_MODO[m]}</b>' if m == modo else f"<span>{NOME_MODO[m]}</span>" for m in NOME_MODO)
    return f'<footer class="t-modo"><span class="t-rotulo">Modo</span>{chips}</footer>'


def corpo_informacao():
    return """
<p class="t-sobre">Parte 1 · A compra</p>
<h3 class="t-titulo">O que você comprou, afinal?</h3>
<p>Você abriu a loja do jogo, escolheu a skin e apertou comprar. O dinheiro saiu da sua conta e a skin entrou no seu inventário, ao lado das outras, como numa coleção.</p>
<div class="t-nome"><p class="t-rot">Isso tem nome</p>
<p><span class="oic">Objeto Imaterial de Consumo</span></p>
<p>A lei brasileira já tinha deixado espaço para isso. Em 1990, o Código de Defesa do Consumidor disse que produto pode ser imaterial, e a frase ficou lá, como um terreno demarcado que ninguém ocupou.</p></div>
<p class="t-dica">Ao passar o mouse sobre uma frase, aparece só a página de onde ela vem.</p>
"""


def corpo_doutrina():
    return f"""
<p class="t-sobre t-vermelho">Situação</p>
<h3 class="t-titulo">Quando o que foi comprado depende do ambiente que a plataforma administra</h3>
<dl class="t-campos">
<dt>Quando se aplica</dt>
<dd><span class="t-trecho">Sempre que a utilidade consumida depender estruturalmente de ambiente administrado, modulado e mutável por governança privada, com impacto sobre acesso, permanência, inteligibilidade ou atualização da experiência, estará configurado o campo de incidência do OIC.</span>
<span class="t-balao"><span class="t-ref">{e(REF_TESE)}, p. 743.</span><span class="t-copiar">Copiar com referência</span></span></dd>
<dt>Qualificação</dt>
<dd>A qualificação jurídica daí resultante é a de produto imaterial submetido ao regime do art. 3º, § 1º, do CDC<sup>1</sup>, sem que a dimensão prestacional do vínculo afaste o controle da fruição como núcleo do fornecimento.</dd>
</dl>
<p class="t-rodape"><sup>1</sup> Art. 3º [...] § 1° Produto é qualquer bem, móvel ou imóvel, material ou imaterial.</p>
"""


def corpo_ciencia():
    return f"""
<div class="arq" data-arq="7.1.2 · bloco a · p. 743">
<p class="t-sobre">a) regime de fruição governada e incidência do OIC</p>
<p>Sempre que a utilidade consumida depender estruturalmente de ambiente administrado, modulado e mutável por governança privada, com impacto sobre acesso, permanência, inteligibilidade ou atualização da experiência, estará configurado o campo de incidência do OIC. <a class="pg">p. 743</a></p>
<p class="chips"><span class="oic">Objeto Imaterial de Consumo</span> <span class="derivado">consumidor-cidadão</span></p>
</div>
<figure class="ficha aberta" style="--area:var(--antropologia);--area-t:var(--antropologia-t)">
<figcaption class="autor">Douglas e Isherwood · Antropologia do consumo</figcaption>
<blockquote>A consequência conceitual é expressiva, uma vez que os bens deixam de ser lidos como coisas que apenas “servem” e passam a ser compreendidos como meio não verbal de elaboração cultural. <a class="pg">p. 248</a></blockquote>
<p class="ref">Mary Douglas e Baron Isherwood, The world of goods, Routledge, 1996, p. 40-41.</p>
</figure>
<div class="movimento" aria-label="Movimento entre objeto e instrumento, exemplo de forma">
<div style="--c:var(--laboratorio)"><small>Objeto</small><b>a skin na loja</b></div>
<div style="--c:var(--economia)"><small>Lente</small><b>economia de pedágio</b></div>
<div style="--c:var(--dir-marca)"><small>Qualificação</small><b>produto imaterial</b></div>
<div style="--c:var(--tese-linha)"><small>Tese</small><b>OIC</b></div>
</div>
"""


CORPOS = {"informacao": corpo_informacao, "doutrina": corpo_doutrina, "ciencia": corpo_ciencia}


def tela(modo, tom):
    return (f'<div class="tela {modo} {tom}" style="{vars_tela(modo, tom)}">{topo(modo)}'
            f'<main class="t-corpo">{CORPOS[modo]()}</main>{pe(modo)}</div>')


def cartao_area(k):
    a = A[k]
    claro, escuro = T["ciencia"]["claro"]["papel"], T["ciencia"]["escuro"]["papel"]
    ctc = min(contraste(a["texto"], T[m]["claro"]["papel"]) for m in T)
    cte = min(contraste(a["texto_escuro"], T[m]["escuro"]["papel"]) for m in T)
    return f"""<article class="area">
<div class="area-cor" style="background:{a['destaque']}"></div>
<h3>{e(a['nome'])}</h3>
<p class="porque">{e(PORQUE[k])}</p>
<div class="amostras">
<div class="amostra" style="background:{claro};color:{a['texto']};border-top:5px solid {a['destaque']}"><small>claro</small><b>{e(AUTORES[k])}</b></div>
<div class="amostra" style="background:{escuro};color:{a['texto_escuro']};border-top:5px solid {a['destaque_escuro']}"><small>escuro</small><b>{e(AUTORES[k])}</b></div>
</div>
<p class="hex">destaque {a['destaque']}{'' if a['destaque_escuro'] == a['destaque'] else ' · no escuro ' + a['destaque_escuro']}<br>texto {a['texto']} · no escuro {a['texto_escuro']}<br>contraste do texto, pior caso {ctc:.1f} no claro e {cte:.1f} no escuro</p>
</article>"""


NOMES_SIM = [("normal", "Visão comum"), ("protan", "Protanopia"), ("deutan", "Deuteranopia"), ("tritan", "Tritanopia")]


def daltonismo(tom):
    chave = "destaque" if tom == "claro" else "destaque_escuro"
    cores = {k: A[k][chave] for k in ORDEM}
    cores["tese"] = TESE["chapado"] if tom == "claro" else TESE["marca_escuro"]
    rotulo = {k: A[k]["nome"] for k in ORDEM} | {"tese": "A tese"}
    papel = T["ciencia"][tom]["papel"]
    linhas = []
    for s, nome in NOMES_SIM:
        sims = {k: simular(v, s) for k, v in cores.items()}
        d, x, y = min((dist(sims[a], sims[b]), a, b) for a, b in itertools.combinations(sims, 2))
        cel = "".join(f'<span class="sw" style="background:{sims[k]}" title="{e(rotulo[k])}"></span>' for k in cores)
        linhas.append(f'<div class="sim"><span class="sim-nome">{nome}</span><span class="sws">{cel}</span>'
                      f'<span class="sim-min">par mais próximo {e(rotulo[x])} e {e(rotulo[y])}, {d:.1f}</span></div>')
    curto = {"direito": "Dir", "economia": "Eco", "tecnica": "Téc", "antropologia": "Ant", "semiotica": "Sem", "poder": "Pod", "laboratorio": "Obj", "tese": "Tese"}
    legenda = "".join(f'<span title="{e(rotulo[k])}">{curto[k]}</span>' for k in cores)
    return f'<div class="dalt" style="background:{papel};color:{T["ciencia"][tom]["tinta"]}"><p class="dalt-tom">{tom}</p><div class="sws-legenda">{legenda}</div>{"".join(linhas)}</div>'


def tabela_contraste():
    linhas = []
    for m in ("informacao", "doutrina", "ciencia", "ficha"):
        for tom in ("escuro", "claro"):
            t = T[m][tom]
            nome = NOME_MODO.get(m, "Balões e páginas de autor")
            linhas.append(f'<tr><td>{nome}, {tom}</td><td><span class="sw" style="background:{t["papel"]}"></span>{t["papel"]}</td>'
                          f'<td>{contraste(t["tinta"], t["papel"]):.1f}</td><td>{contraste(t["tinta2"], t["papel"]):.1f}</td></tr>')
    return ('<table class="contraste"><thead><tr><th>Tela</th><th>Papel</th><th>Texto</th><th>Texto secundário</th></tr></thead><tbody>'
            + "".join(linhas) + "</tbody></table>")


chips_nove = "".join(f'<span class="oic">{e(n)}</span>' for n in NOVE)
chips_dez = "".join(f'<span class="derivado">{e(n)}</span>' for n in DEZ)
OR = T["informacao"]

pagina = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cores do Lex Plataformae</title>
<style>
{FONTES}
:root {{
  --papel:{OR['escuro']['papel']}; --folha:{OR['escuro']['folha']}; --tinta:{OR['escuro']['tinta']}; --tinta2:{OR['escuro']['tinta2']}; --linha:{OR['escuro']['linha']};
  --tese-texto:{TESE['texto_escuro']}; --tese-linha:{TESE['marca_escuro']};
  --f-display:"Archivo","Helvetica Neue",Arial,sans-serif; --f-texto:"Newsreader",Georgia,serif; --f-dado:"IBM Plex Mono",ui-monospace,monospace;
  color-scheme: dark;
}}
@media (prefers-color-scheme: light) {{
  :root:not([data-theme="dark"]) {{ --papel:{OR['claro']['papel']}; --folha:{OR['claro']['folha']}; --tinta:{OR['claro']['tinta']}; --tinta2:{OR['claro']['tinta2']}; --linha:{OR['claro']['linha']}; --tese-texto:{TESE['texto']}; --tese-linha:{TESE['chapado']}; color-scheme: light; }}
}}
:root[data-theme="light"] {{ --papel:{OR['claro']['papel']}; --folha:{OR['claro']['folha']}; --tinta:{OR['claro']['tinta']}; --tinta2:{OR['claro']['tinta2']}; --linha:{OR['claro']['linha']}; --tese-texto:{TESE['texto']}; --tese-linha:{TESE['chapado']}; color-scheme: light; }}
* {{ box-sizing: border-box; }}
html {{ -webkit-text-size-adjust: 100%; }}
body {{ margin:0; background:var(--papel); color:var(--tinta); font-family:var(--f-texto); font-size:1.0625rem; line-height:1.55; }}
.pagina {{ max-width:1180px; margin:0 auto; padding:2.5rem 16px 5rem; }}
h1 {{ font-family:var(--f-display); font-stretch:118%; font-weight:800; text-transform:uppercase; font-size:clamp(2rem,6vw,3.6rem); line-height:1; letter-spacing:-0.01em; margin:0.4rem 0 1rem; }}
h2 {{ font-family:var(--f-display); font-stretch:112%; font-weight:750; font-size:clamp(1.35rem,3vw,1.9rem); margin:3.5rem 0 0.6rem; }}
h3 {{ font-family:var(--f-display); font-weight:700; font-size:1.05rem; margin:0.2rem 0 0.4rem; }}
.sobrelinha {{ font-family:var(--f-dado); font-size:0.75rem; letter-spacing:0.06em; text-transform:uppercase; color:var(--tinta2); margin:0; }}
.lead {{ max-width:62ch; font-size:1.15rem; }}
.nota {{ max-width:66ch; color:var(--tinta2); }}
p {{ margin:0 0 0.8rem; }}
a {{ color:inherit; }}

/* a tese */
.klein {{ background:{TESE['chapado']}; color:#fff; border-radius:6px; padding:clamp(1.5rem,5vw,3.5rem); display:grid; gap:1.5rem; grid-template-columns: 1fr; }}
@media (min-width: 860px) {{ .klein {{ grid-template-columns: 1.1fr 1fr; align-items:end; }} }}
.klein .grande {{ font-family:var(--f-display); font-stretch:125%; font-weight:800; text-transform:uppercase; font-size:clamp(2.4rem,8vw,5.5rem); line-height:0.9; margin:0; }}
.klein p {{ max-width:52ch; }}
.klein .fonte {{ font-family:var(--f-dado); font-size:0.72rem; opacity:0.85; }}
.oic {{ display:inline-block; background:{TESE['chapado']}; color:#fff; font-family:var(--f-display); font-weight:700; font-size:0.86em; padding:0.12rem 0.45rem; border-radius:2px; margin:0 0.25rem 0.35rem 0; }}
.derivado {{ display:inline-block; border:1.5px solid var(--tese-linha); color:var(--tese-texto); font-family:var(--f-display); font-weight:650; font-size:0.86em; padding:0.08rem 0.42rem; border-radius:2px; margin:0 0.25rem 0.35rem 0; }}
.conceitos {{ display:grid; gap:1rem; grid-template-columns:1fr; margin-top:1.2rem; }}
@media (min-width: 860px) {{ .conceitos {{ grid-template-columns:1fr 1fr; }} }}
.conceitos > div {{ border:1px solid var(--linha); border-radius:6px; padding:1rem; background:var(--folha); }}

/* áreas */
.areas {{ display:grid; gap:1rem; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); margin-top:1.2rem; }}
.area {{ border:1px solid var(--linha); border-radius:6px; overflow:hidden; background:var(--folha); display:flex; flex-direction:column; }}
.area-cor {{ height:72px; }}
.area h3, .area .porque, .area .hex {{ padding:0 0.9rem; }}
.area h3 {{ margin-top:0.8rem; }}
.porque {{ font-size:0.95rem; }}
.amostras {{ display:grid; grid-template-columns:1fr 1fr; gap:0; margin:0.3rem 0 0.7rem; }}
.amostra {{ padding:0.55rem 0.7rem 0.7rem; }}
.amostra small {{ display:block; font-family:var(--f-dado); font-size:0.62rem; opacity:0.7; text-transform:uppercase; letter-spacing:0.06em; }}
.amostra b {{ font-family:var(--f-display); font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.04em; line-height:1.35; display:block; }}
.hex {{ font-family:var(--f-dado); font-size:0.68rem; color:var(--tinta2); margin-top:auto; padding-bottom:0.9rem !important; line-height:1.6; }}

/* telas */
.modo {{ margin-top:2rem; }}
.modo-cab {{ display:flex; flex-wrap:wrap; align-items:baseline; gap:0.3rem 1rem; }}
.modo-cab h3 {{ font-size:1.25rem; margin:0; }}
.modo-cab span {{ font-family:var(--f-dado); font-size:0.75rem; color:var(--tinta2); }}
.par {{ display:grid; gap:1rem; grid-template-columns:1fr; margin-top:0.8rem; }}
@media (min-width: 900px) {{ .par {{ grid-template-columns:1fr 1fr; }} }}
.tela {{ background:var(--papel); color:var(--tinta); border:1px solid var(--linha); border-radius:10px; overflow:hidden; display:flex; flex-direction:column; font-size:0.98rem; line-height:1.55; }}
.tela.ciencia {{ background-image:linear-gradient(var(--grade) 1px, transparent 1px), linear-gradient(90deg, var(--grade) 1px, transparent 1px); background-size:18px 18px; }}
.t-topo {{ display:flex; align-items:center; gap:0.5rem 1rem; flex-wrap:wrap; padding:0.7rem 0.9rem; border-bottom:1px solid var(--linha); background:var(--papel); }}
.t-marca {{ font-family:var(--f-display); font-stretch:125%; font-weight:800; font-size:0.7rem; letter-spacing:0.04em; text-transform:uppercase; }}
.t-menu {{ display:flex; gap:0.2rem 0.85rem; flex-wrap:wrap; font-family:var(--f-display); font-size:0.78rem; color:var(--tinta2); flex:1; }}
.t-integral {{ margin-left:auto; font-family:var(--f-display); font-weight:700; font-size:0.72rem; padding:0.35rem 0.6rem; border-radius:3px; background:var(--inv-papel); color:var(--inv-tinta); white-space:nowrap; }}
.t-corpo {{ padding:1.1rem 1rem 1.3rem; flex:1; }}
.t-sobre {{ font-family:var(--f-dado); font-size:0.68rem; letter-spacing:0.06em; text-transform:uppercase; color:var(--tinta2); margin:0 0 0.3rem; }}
.t-vermelho {{ color:var(--dir-texto); }}
.t-titulo {{ font-family:var(--f-display); font-stretch:108%; font-weight:780; font-size:1.3rem; line-height:1.18; margin:0 0 0.7rem; }}
.t-nome {{ border-left:4px solid {TESE['chapado']}; padding:0.2rem 0 0.2rem 0.8rem; margin:1rem 0; }}
.escuro .t-nome {{ border-left-color:{TESE['marca_escuro']}; }}
.t-rot {{ font-family:var(--f-dado); font-size:0.68rem; text-transform:uppercase; letter-spacing:0.06em; color:var(--tinta2); margin:0 0 0.3rem; }}
.t-dica {{ font-family:var(--f-dado); font-size:0.66rem; color:var(--tinta2); border-top:1px dashed var(--linha); padding-top:0.5rem; margin:1rem 0 0; }}
.t-campos {{ margin:0; }}
.t-campos dt {{ font-family:var(--f-display); font-weight:700; font-size:0.74rem; text-transform:uppercase; letter-spacing:0.05em; color:var(--dir-texto); margin-top:0.7rem; }}
.t-campos dd {{ margin:0.15rem 0 0; }}
.t-trecho {{ background:color-mix(in oklab, var(--dir-marca) 14%, transparent); box-decoration-break:clone; -webkit-box-decoration-break:clone; }}
.t-balao {{ display:flex; flex-wrap:wrap; gap:0.3rem 0.8rem; align-items:center; margin:0.45rem 0 0.2rem; padding:0.45rem 0.6rem; background:var(--inv-papel); color:var(--inv-tinta); border-radius:4px; font-family:var(--f-dado); font-size:0.66rem; line-height:1.45; }}
.t-copiar {{ font-family:var(--f-display); font-weight:700; font-size:0.68rem; border:1px solid currentColor; border-radius:3px; padding:0.1rem 0.4rem; }}
.t-rodape {{ border-top:1px solid var(--linha); margin-top:1rem; padding-top:0.6rem; font-size:0.85rem; color:var(--tinta2); }}
.t-modo {{ border-top:1px solid var(--linha); display:flex; gap:0.4rem; flex-wrap:wrap; padding:0.55rem 0.9rem; font-family:var(--f-dado); font-size:0.68rem; align-items:center; background:var(--papel); }}
.t-modo .t-rotulo {{ text-transform:uppercase; letter-spacing:0.08em; color:var(--tinta2); margin-right:0.3rem; }}
.t-modo span:not(.t-rotulo) {{ padding:0.15rem 0.5rem; border:1px solid var(--linha); border-radius:999px; color:var(--tinta2); }}
.t-modo .ativo {{ padding:0.15rem 0.55rem; border-radius:999px; background:var(--modo-cor); color:var(--modo-tinta); font-weight:500; }}
.arq {{ border:1px dashed var(--traco); position:relative; padding:1rem 0.8rem 0.5rem; margin:0.6rem 0 1.1rem; background:var(--papel); }}
.arq::before {{ content:attr(data-arq); position:absolute; top:-0.6rem; left:0.6rem; background:var(--papel); padding:0 0.35rem; font-family:var(--f-dado); font-size:0.62rem; color:var(--traco); }}
.pg {{ font-family:var(--f-dado); font-size:0.66rem; border:1px solid var(--traco); color:var(--traco); padding:0 0.3rem; border-radius:2px; text-decoration:none; white-space:nowrap; }}
.chips {{ margin:0.4rem 0 0; }}
.ficha {{ margin:0 0 1.1rem; background:var(--f-papel); color:var(--f-tinta); border-top:6px solid var(--area); border-radius:2px; padding:0.6rem 0.85rem 0.55rem;
 }}
.ficha .autor {{ font-family:var(--f-display); font-size:0.66rem; font-weight:750; letter-spacing:0.07em; text-transform:uppercase; color:var(--area-t); }}
.ficha blockquote {{ margin:0.35rem 0 0.45rem; font-size:0.98rem; line-height:1.6em; background-image:linear-gradient(to bottom, transparent calc(1.6em - 1px), var(--f-pauta) calc(1.6em - 1px)); background-size:100% 1.6em; }}
.ficha .ref {{ font-family:var(--f-dado); font-size:0.64rem; color:var(--f-tinta2); margin:0; border-top:1px dashed var(--f-tinta2); padding-top:0.35rem; }}
.ficha .pg {{ border-color:var(--f-tinta2); color:var(--f-tinta2); }}
.movimento {{ display:grid; grid-template-columns:repeat(4,1fr); gap:0.35rem; }}
.movimento div {{ border-top:5px solid var(--c); padding:0.35rem 0.4rem 0.4rem; background:var(--papel); border-left:1px solid var(--linha); border-right:1px solid var(--linha); border-bottom:1px solid var(--linha); }}
.movimento small {{ display:block; font-family:var(--f-dado); font-size:0.6rem; text-transform:uppercase; letter-spacing:0.06em; color:var(--tinta2); }}
.movimento b {{ font-family:var(--f-display); font-size:0.74rem; font-weight:700; line-height:1.25; display:block; }}
@media (max-width: 480px) {{ .movimento {{ grid-template-columns:1fr 1fr; }} }}

/* daltonismo e contraste */
.dalts {{ display:grid; gap:1rem; grid-template-columns:1fr; margin-top:1rem; }}
@media (min-width: 900px) {{ .dalts {{ grid-template-columns:1fr 1fr; }} }}
.dalt {{ border-radius:8px; padding:1rem; border:1px solid var(--linha); }}
.dalt-tom {{ font-family:var(--f-dado); font-size:0.7rem; text-transform:uppercase; letter-spacing:0.08em; margin:0 0 0.6rem; opacity:0.75; }}
.sws-legenda {{ display:grid; grid-template-columns:repeat(8,minmax(0,1fr)); gap:4px; font-family:var(--f-dado); font-size:0.56rem; line-height:1.2; margin-bottom:0.5rem; opacity:0.8; }}
.sim {{ margin-bottom:0.7rem; }}
.sim-nome {{ font-family:var(--f-display); font-size:0.78rem; font-weight:700; display:block; }}
.sws {{ display:grid; grid-template-columns:repeat(8,minmax(0,1fr)); gap:4px; margin:0.25rem 0; }}
.sws .sw {{ height:30px; border-radius:3px; }}
.sim-min {{ font-family:var(--f-dado); font-size:0.64rem; opacity:0.8; }}
.contraste {{ border-collapse:collapse; font-family:var(--f-dado); font-size:0.78rem; margin-top:1rem; width:100%; max-width:720px; }}
.contraste th, .contraste td {{ text-align:left; padding:0.4rem 0.6rem; border-bottom:1px solid var(--linha); }}
.contraste .sw {{ display:inline-block; width:0.9rem; height:0.9rem; border:1px solid var(--linha); vertical-align:-0.15rem; margin-right:0.4rem; }}
.lista {{ max-width:66ch; padding-left:1.1rem; }}
.lista li {{ margin-bottom:0.45rem; }}
.copia {{ font-family:var(--f-dado); font-size:0.8rem; background:var(--folha); border:1px solid var(--linha); border-radius:6px; padding:0.9rem 1rem; max-width:720px; white-space:pre-wrap; }}
.tabela-rolagem {{ overflow-x:auto; }}
</style>
</head>
<body>
<div class="pagina">
<p class="sobrelinha">Proposta para decisão do autor · 27/10/2026 · nada disto está no site</p>
<h1>As cores do site</h1>
<p class="lead">A tese ganha uma cor própria, fora de qualquer grupo. Cada área ganha um par, um destaque claro e um texto escuro. Cada modo de leitura ganha o seu papel e a sua tinta, e os balões de autor ganham a cara de ficha de biblioteca.</p>
<p class="nota">A página abre no escuro, que é como o Senhor vê o site. Cada modo aparece nas duas versões, escura e clara, porque hoje o site segue a preferência do aparelho de quem lê.</p>

<h2>A cor da tese</h2>
<section class="klein" aria-label="Azul Klein">
<div><p class="grande">Azul<br>Klein</p><p class="fonte">#002FA7 · aproximação em tela do International Klein Blue</p></div>
<div>
<p>Em 1959, Yves Klein começou a vender Zonas de Sensibilidade Pictórica Imaterial. O comprador pagava em ouro e recebia um recibo. No ritual completo, queimava o recibo e Klein jogava metade do ouro no Sena.</p>
<p>Em 1960, Klein registrou no instituto francês de propriedade industrial a técnica do seu azul, e não a cor. Para ele, o azul era o caminho do material ao imaterial.</p>
<p>É a história de um objeto imaterial vendido, com o recibo como única prova e a propriedade intelectual protegendo o processo, e não a coisa. A cor vem de fora do Direito e de fora de todas as áreas, como o autor pediu.</p>
<p class="fonte">Fontes. <a href="https://en.wikipedia.org/wiki/Zone_de_Sensibilit%C3%A9_Picturale_Immat%C3%A9rielle">Wikipedia, Zone de Sensibilité Picturale Immatérielle</a> · <a href="https://www.centrepompidou.fr/en/pompidou-plus/magazine/article/the-untold-story-of-the-international-klein-blue-ikb-of-yves-klein">Centre Pompidou, a história do IKB</a></p>
</div>
</section>
<p class="nota" style="margin-top:1rem">A tese aparece sempre chapada, como os monocromos de Klein. As áreas aparecem em filetes e nunca em bloco cheio. Assim a diferença entre o que é da tese e o que é instrumento não depende só da cor, depende também da forma.</p>
<div class="conceitos">
<div><h3>Os nove conceitos</h3><p class="nota">Chapados em azul Klein, com letra branca.</p>{chips_nove}</div>
<div><h3>Os dez derivados</h3><p class="nota">Ao lado dos nove, como o autor decidiu, no mesmo azul, só que em contorno.</p>{chips_dez}</div>
</div>

<h2>As áreas</h2>
<p class="nota">Cada área tem um destaque claro, para filetes e marcas, e um texto escuro e mais neutro, para nomes de autor e rótulos. No escuro, o texto vira a versão clara do mesmo tom. Nenhuma informação depende só da cor, porque o nome da área vai sempre junto.</p>
<div class="areas">{''.join(cartao_area(k) for k in ORDEM)}</div>

<h2>Os três modos</h2>
<p class="nota">Informação usa papel quente e só o azul da tese. Doutrina usa papel frio, de arquivo de trabalho, e o vermelho do Direito para o que é operação, como dever, prova, pedido e lei. Ciência é uma prancheta com grade, onde a estrutura aparece em tracejado neutro e todas as cores de área entram. O laranja de hoje sai.</p>
<p class="nota">O bloco do texto integral fica no canto superior direito e sempre contraria a página. Na página escura ele é claro com letra escura. Na página clara ele é escuro com letra clara.</p>
{''.join(f'<section class="modo"><div class="modo-cab"><h3>{NOME_MODO[m]}</h3><span>{ {"informacao": "o leigo que quer saber seus direitos", "doutrina": "o técnico que vai advogar", "ciencia": "o expert que quer testar a teoria"}[m] }</span></div><div class="par">{tela(m, "escuro")}{tela(m, "claro")}</div></section>' for m in ("informacao", "doutrina", "ciencia"))}

<h2>A referência na cópia</h2>
<p class="nota">Versão mínima, sem padrão de associação. Quem copia um trecho em Informação ou em Doutrina leva isto.</p>
<div class="copia">“Sempre que a utilidade consumida depender estruturalmente de ambiente administrado, modulado e mutável por governança privada, com impacto sobre acesso, permanência, inteligibilidade ou atualização da experiência, estará configurado o campo de incidência do OIC.”
{e(REF_TESE)}, p. 743.
lexplataformae.com.br/tese/7-1-2/#p743</div>
<p class="nota" style="margin-top:0.8rem">O botão de copiar avisa o que leva, para a cópia nunca surpreender o leitor.</p>

<h2>Daltonismo</h2>
<p class="nota">Os destaques das sete áreas e o azul da tese, simulados para os três tipos de daltonismo. O número é a distância entre o par mais parecido, numa escala em que 2 já se distingue lado a lado. O pior caso fica perto de 8, o que se separa bem, e mesmo assim o nome da área vai sempre junto.</p>
<div class="dalts">{daltonismo('escuro')}{daltonismo('claro')}</div>
<p class="nota" style="margin-top:0.8rem">Dir é Direito, Eco é Economia política, Téc é Técnica e mídia, Ant é Antropologia do consumo, Sem é Semiótica e linguagem, Pod é Poder e subjetividade e Obj é Objeto e laboratório.</p>

<h2>Contraste</h2>
<p class="nota">Razão de contraste do texto sobre o papel de cada tela. O mínimo para leitura confortável é 4,5, e o texto principal passa de 12 em todas.</p>
<div class="tabela-rolagem">{tabela_contraste()}</div>

<h2>O que sai e o que muda</h2>
<ul class="lista">
<li>O azul de hoje sai dos links e dos nomes das ideias, que passam ao azul Klein.</li>
<li>O laranja da arquitetura sai, porque brigaria com o âmbar e com o vermelho.</li>
<li>O amarelo de marcar trechos fica mais limão ({MARCA['claro']} no claro), para não se confundir com o âmbar da economia política.</li>
<li>O plano das ilustrações será refeito sobre esta paleta, depois da decisão.</li>
</ul>
</div>
</body>
</html>
"""
(RAIZ / "estrutura/paletas.html").write_text(pagina, encoding="utf-8")
print("ok", len(pagina) // 1024, "KB")
