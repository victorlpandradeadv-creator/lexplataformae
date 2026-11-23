"""Monta o PDF da tradução inglesa da tese a partir das páginas de docs/en/thesis/.

Uso
    python3 ferramentas/en/pdf_en.py            # todas as seções
    python3 ferramentas/en/pdf_en.py 3-2-3      # só as seções pedidas, para conferir

Cada seção é impressa pelo Chromium (playwright) no modo Ciência, em que a referência entre parênteses,
a marca da página do original e as notas ficam à vista. Saem da impressão o cabeçalho e o rodapé do site,
a coluna lateral, a trilha, o link para o PDF, as camadas do site e a navegação entre seções.
O PDF ganha uma folha de rosto com o aviso da tradução, marcadores por seção e os metadados de autoria.

Feito em 22/11/2026. O PDF anterior, de 12/11/2026, saiu no modo Informação, sem a maior parte dos títulos,
sem as referências entre parênteses e com "See this section in the PDF" em cada seção.
"""
import html
import re
import sys
import tempfile
from pathlib import Path

import pymupdf
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parents[2]
EN = RAIZ / "docs" / "en" / "thesis"
SAIDA = RAIZ / "site" / "andrade-2026-thesis-ioc-lex-plataformae-en.pdf"
TITULO_EN = ("On the legal regime of the Immaterial Object of Consumption (IOC) under Lex Plataformae: "
             "protecting the consumer's semiotic vulnerability in light of Brazil's constitutional and economic order")
TITULO_PT = ("Do regime jurídico do Objeto Imaterial de Consumo (OIC) sob a Lex Plataformae: a tutela da vulnerabilidade "
             "semiótica do consumidor à luz da ordem constitucional e econômica do Brasil")

ESTILO = """
@page { size: A4; margin: 20mm 20mm 22mm 20mm; }
html, body { background: #fff !important; color: #111 !important; }
body { font-size: 10.5pt !important; }
.texto-integral, .texto-integral * { color: #111 !important; }
.texto-integral .texto p, .texto-integral .texto li, .texto-integral .notas li, .texto-integral .notas p { font-size: 10.5pt !important; line-height: 1.45 !important; }
.texto-integral .notas li, .texto-integral .notas p { font-size: 9pt !important; }
.texto-integral h1 { font-size: 15pt !important; line-height: 1.25 !important; margin: 0 0 8pt !important; max-width: none !important; }
.texto-integral h2, .texto-integral h3 { font-size: 11.5pt !important; }
.texto-integral .cita-grupo { text-decoration: none !important; }
.texto-integral .pg-marca { display: inline !important; font-size: 8pt !important; color: #555 !important; }
.texto-integral blockquote, .texto-integral .citacao { font-size: 9.5pt !important; }
.lexp-fora { display: none !important; }
.chave-mestra, .pular-conteudo { visibility: hidden !important; }
.lexp-caminho { display: block !important; max-width: none !important; width: auto !important; margin: 0 !important; padding: 0 !important;
                grid-template-columns: none !important; border: 0 !important; box-shadow: none !important; }
a { color: inherit !important; text-decoration: none !important; }
table { font-size: 8.5pt !important; break-inside: auto; }
"""

PREPARAR = """
() => {
  const n2 = document.getElementById('nivel-2');
  if (n2) { n2.checked = true; n2.dispatchEvent(new Event('change', {bubbles: true})); }
  document.body.classList.add('aberto', 'desnudo');
  const art = document.querySelector('article.texto-integral');
  if (!art) return false;
  // Do artigo até o corpo, tudo o que não leva ao artigo sai da impressão, salvo os botões do modo, que o CSS consulta.
  let el = art;
  while (el && el !== document.body) {
    el.classList.add('lexp-caminho');
    for (const irmao of el.parentElement.children) {
      if (irmao !== el && !irmao.querySelector('#nivel-2') && irmao.id !== 'nivel-2') irmao.classList.add('lexp-fora');
      if (irmao !== el && (irmao.querySelector('#nivel-2') || irmao.id === 'nivel-2')) irmao.style.cssText = 'position:absolute;left:-9999px;';
    }
    el = el.parentElement;
  }
  for (const s of ['nav.trilha', '.folha-abertura', '.ler-pdf', 'aside.conceitos-aqui', 'aside.camadas-aqui', 'nav.vizinhos', 'aside.lateral',
                   '.balao-ref', '.so-leitor', '.aviso-traducao', 'details.original > summary', '.cita-sinal']) {
    art.querySelectorAll(s).forEach(e => e.classList.add('lexp-fora'));
  }
  art.querySelectorAll('details').forEach(d => d.open = false);
  return true;
}
"""


def ordem():
    """As seções na ordem do sumário da página de entrada."""
    s = BeautifulSoup((EN / "index.html").read_text(encoding="utf-8"), "html.parser")
    vistos = []
    for a in s.select("nav.sumario a[href]"):
        slug = a["href"].strip("/").split("/")[-1]
        if (EN / slug / "index.html").exists() and slug not in vistos:
            vistos.append(slug)
    return vistos


def titulo_de(slug):
    s = BeautifulSoup((EN / slug / "index.html").read_text(encoding="utf-8"), "html.parser")
    h1 = s.select_one("article.texto-integral h1")
    return re.sub(r"\s+", " ", h1.get_text(" ")).strip() if h1 else slug


def folha_de_rosto(destino, pagina):
    aviso = ""
    s = BeautifulSoup((EN / "index.html").read_text(encoding="utf-8"), "html.parser")
    p = s.select_one("p.aviso-traducao")
    if p:
        for a in p.select("a"):
            a.unwrap()
        aviso = p.get_text(" ").strip()
        aviso = re.sub(r"\s*(Download this English translation as PDF|Ler em português)\.?\s*", " ", aviso).strip()
        aviso = re.sub(r"\s+\.$", "", aviso)
    resumo = s.select_one("section#resumo")
    resumo_html = ""
    if resumo:
        for a in resumo.select("a"):
            a.unwrap()
        titulo_r = resumo.select_one("h2")
        texto_r = " ".join(f"<p>{html.escape(x.get_text(' ').strip())}</p>" for x in resumo.select("p"))
        chaves = "; ".join(li.get_text(" ").strip() for li in resumo.select("li"))
        resumo_html = (f'<div class="resumo"><h2>{html.escape(titulo_r.get_text().strip()) if titulo_r else "Abstract"}</h2>{texto_r}'
                       + (f"<p><b>Keywords</b>. {html.escape(chaves)}.</p>" if chaves else "") + "</div>")
    doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><style>
@page {{ size: A4; margin: 30mm 25mm; }}
body {{ font-family: Georgia, 'Times New Roman', serif; color: #111; font-size: 11pt; line-height: 1.5; }}
h1 {{ font-size: 18pt; line-height: 1.3; margin: 40mm 0 10mm; }}
.pt {{ font-style: italic; margin-bottom: 14mm; }}
.aviso {{ margin-top: 30mm; font-size: 9.5pt; border-top: 1px solid #999; padding-top: 4mm; }}
.resumo {{ break-before: page; text-align: justify; }}
.resumo h2 {{ font-size: 13pt; text-align: center; margin: 0 0 6mm; }}
</style></head><body>
<p>Victor Luiz Pereira de Andrade</p>
<h1>{html.escape(TITULO_EN)}</h1>
<p class="pt">Original title. {html.escape(TITULO_PT)}</p>
<p>Doctoral thesis in Law. Universidade Estadual Paulista “Júlio de Mesquita Filho” (UNESP), Faculdade de Ciências Humanas e Sociais, Franca, 2026.
Advisor, Prof. Dr. Luciana Lopes Canavez.</p>
<p>This study was financed in part by the Coordenação de Aperfeiçoamento de Pessoal de Nível Superior - Brasil (CAPES) - Finance Code 001.</p>
<p class="aviso">{html.escape(aviso)} It is available at https://lexplataformae.com.br/tese/.
Page markers such as p. 208 refer to the printed pages of the original.</p>
{resumo_html}
</body></html>"""
    arq = Path(tempfile.mkdtemp()) / "rosto.html"
    arq.write_text(doc, encoding="utf-8")
    pagina.goto(arq.as_uri())
    pagina.pdf(path=str(destino), format="A4", print_background=False)


def main(pedidas):
    slugs = ordem()
    if pedidas:
        slugs = [s for s in slugs if s in pedidas]
    tmp = Path(tempfile.mkdtemp())
    final = pymupdf.open()
    toc = []
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pg = nav.new_page()
        pg.add_init_script("try{localStorage.setItem('lexp-nivel','2');localStorage.setItem('lexp-tema','claro')}catch(e){}")
        rosto = tmp / "000.pdf"
        folha_de_rosto(rosto, pg)
        final.insert_pdf(pymupdf.open(rosto))
        if final.page_count > 1:
            toc.append([1, "Abstract", 2])
        for i, slug in enumerate(slugs, 1):
            pg.goto((EN / slug / "index.html").as_uri(), wait_until="load")
            pg.emulate_media(media="print")
            if not pg.evaluate(PREPARAR):
                print("sem artigo", slug)
                continue
            pg.add_style_tag(content=ESTILO)
            arq = tmp / f"{i:03d}.pdf"
            pg.pdf(path=str(arq), format="A4", print_background=False, prefer_css_page_size=True,
                   display_header_footer=True, header_template="<span></span>",
                   footer_template='<div style="font-size:7pt;width:100%;text-align:center;color:#666;font-family:sans-serif">'
                                   '<span class="pageNumber"></span></div>')
            parte = pymupdf.open(arq)
            nivel = 1 if slug in ("referencias", "references") else slug.count("-") + 1
            toc.append([min(nivel, 4), titulo_de(slug), final.page_count + 1])
            final.insert_pdf(parte)
        nav.close()
    # Marcadores sem salto de nível, como o PDF exige.
    ajustado, anterior = [], 0
    for nivel, t, n in toc:
        nivel = min(nivel, anterior + 1)
        ajustado.append([nivel, t, n])
        anterior = nivel
    final.set_toc(ajustado)
    final.set_metadata({"title": TITULO_EN, "author": "Victor Luiz Pereira de Andrade",
                        "subject": "English translation of a doctoral thesis in Law (UNESP, Franca, 2026). Not reviewed by the author. The Portuguese original is the authoritative text.",
                        "keywords": "immaterial object of consumption; governed enjoyment bundle; semiotic vulnerability; Lex Plataformae; consumer law",
                        "creator": "lexplataformae.com.br"})
    destino = SAIDA if not pedidas else tmp / "teste.pdf"
    final.save(destino, garbage=4, deflate=True)
    print(destino, final.page_count, "páginas", destino.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main(sys.argv[1:])
