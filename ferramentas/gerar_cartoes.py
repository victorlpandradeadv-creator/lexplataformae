"""Gera as imagens de compartilhamento das páginas da superfície, 1200 x 630, em site/cartoes/.

Uso
    python3 ferramentas/gerar_cartoes.py

Cada cartão traz a pergunta ou a chamada da página, como está em conteudo/camada-externa.md
e em conteudo/percurso.md, e o nome da ideia ou a parte do percurso quando houver. Nenhum cartão traz o nome do autor, salvo o da página do autor.
O gerador do site copia os cartões para docs/assets/cartoes/ e declara cada um nas metatags.
Rodar de novo sempre que os textos da superfície mudarem.
"""
import html
import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "site" / "cartoes"
FONTES = RAIZ / "ferramentas" / "fontes"


def externa():
    dados, pag, campo = {}, None, None
    for linha in (RAIZ / "conteudo" / "camada-externa.md").read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            pag, campo = linha[3:].strip(), None
            dados.setdefault(pag, {})
        elif linha.startswith("### ") and pag:
            campo = linha[4:].strip()
            dados[pag][campo] = []
        elif pag and campo and linha.strip() and not linha.startswith(">"):
            dados[pag][campo].append(linha.strip())
    return dados


def percurso():
    partes, atual, campo = [], None, None
    for linha in (RAIZ / "conteudo" / "percurso.md").read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            atual = {"slug": linha[3:].strip(), "titulo": ""}
            partes.append(atual)
        elif linha.startswith("### "):
            campo = linha[4:].strip()
        elif atual and campo == "titulo" and linha.strip() and not atual["titulo"]:
            atual["titulo"] = linha.strip()
    return partes


def cartoes():
    e = externa()
    nomes = {c["id"]: c["nome"] for c in json.loads((RAIZ / "dados" / "atlas.json").read_text(encoding="utf-8"))["conceitos"]}
    lista = [("inicio", " ".join(e["inicio"]["chamada"]), "Um percurso pelo consumo digital")]
    partes = percurso()
    for i, parte in enumerate(partes, 1):
        lista.append((f"percurso-{parte['slug']}", parte["titulo"], f"Percurso da skin · parte {i} de {len(partes)}"))
    for cid in e.get("cartoes", {}):
        if cid in e and e[cid].get("titulo"):
            lista.append((cid, e[cid]["titulo"][0], nomes.get(cid, "")))
    lista.append(("laboratorio", e["laboratorio"]["titulo"][0], "Laboratório"))
    for fam in ("funcionalidade-cognitiva", "infraestrutura-e-intermediacao", "produtividade-gig-economy", "administracao-de-confianca"):
        if fam in e and e[fam].get("titulo"):
            lista.append((fam, e[fam]["titulo"][0], "Laboratório"))
    lista.append(("autor", "Quem está por trás destas ideias?", "Victor L. P. Andrade"))
    return lista


def pagina(frase, rotulo):
    f = FONTES.as_uri()
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>
@font-face {{ font-family: "Archivo"; font-weight: 100 900; font-stretch: 62% 125%; src: url({f}/archivo-latin-wdth-normal.woff2) format("woff2"); }}
@font-face {{ font-family: "Newsreader"; font-style: italic; font-weight: 200 800; src: url({f}/newsreader-latin-opsz-italic.woff2) format("woff2"); }}
@font-face {{ font-family: "IBM Plex Mono"; font-weight: 500; src: url({f}/ibm-plex-mono-latin-500-normal.woff2) format("woff2"); }}
html, body {{ margin: 0; width: 1200px; height: 630px; }}
body {{ box-sizing: border-box; padding: 64px 72px; background: #f4f5f8; color: #14161b; display: grid; grid-template-rows: auto 1fr auto; font-family: "Archivo", sans-serif;
  background-image: linear-gradient(rgba(20,22,27,0.045) 1px, transparent 1px), linear-gradient(90deg, rgba(20,22,27,0.045) 1px, transparent 1px); background-size: 30px 30px; }}
.marca {{ font-stretch: 125%; font-weight: 800; text-transform: uppercase; font-size: 26px; letter-spacing: 0.02em; }}
.frase {{ align-self: center; font-stretch: 108%; font-weight: 800; font-size: 72px; line-height: 1.08; letter-spacing: -0.01em; max-width: 980px; text-wrap: balance; margin: 0; }}
.pe {{ display: flex; justify-content: space-between; align-items: end; gap: 32px; border-top: 2px solid #14161b; padding-top: 22px; }}
.rotulo {{ font-family: "Newsreader", serif; font-style: italic; font-size: 32px; line-height: 1.2; color: #2b3fcc; }}
.url {{ font-family: "IBM Plex Mono", monospace; font-weight: 500; font-size: 22px; color: #555b69; white-space: nowrap; }}
.chave {{ display: inline-flex; align-items: center; gap: 12px; }}
.chave i {{ display: inline-block; width: 44px; height: 26px; border-radius: 99px; background: #c2410c; position: relative; }}
.chave i::after {{ content: ""; position: absolute; top: 4px; right: 4px; width: 18px; height: 18px; border-radius: 50%; background: #f4f5f8; }}
</style></head><body>
<div class="marca">Lex Plataformae</div>
<p class="frase" id="frase">{html.escape(frase)}</p>
<div class="pe"><span class="rotulo">{html.escape(rotulo)}</span><span class="url chave"><i></i>lexplataformae.com.br</span></div>
</body></html>"""


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        p = nav.new_page(viewport={"width": 1200, "height": 630})
        temp = SAIDA / "_cartao.html"
        for ident, frase, rotulo in cartoes():
            # Página em arquivo, para que as fontes locais carreguem.
            temp.write_text(pagina(frase, rotulo), encoding="utf-8")
            p.goto(temp.as_uri())
            p.evaluate("document.fonts.ready.then(() => true)")
            p.wait_for_timeout(150)
            # Frases longas descem de tamanho até caber em três linhas.
            for tamanho in (72, 64, 58, 52, 48):
                p.evaluate(f"document.getElementById('frase').style.fontSize = '{tamanho}px'")
                linhas = p.evaluate("(() => { const e = document.getElementById('frase'); return Math.round(e.getBoundingClientRect().height / parseFloat(getComputedStyle(e).lineHeight)); })()")
                if linhas <= 3:
                    break
            p.screenshot(path=str(SAIDA / f"{ident}.png"))
            print(f"{ident}.png  {frase[:60]}")
        nav.close()
        temp.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
