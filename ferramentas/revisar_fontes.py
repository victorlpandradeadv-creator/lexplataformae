"""Revisão mecânica dos arquivos de origem e do site gerado, complementar à de revisar_site.py.

Uso
    python3 -I ferramentas/revisar_fontes.py

Confere seis pontos. Frases acima de 37 palavras no texto do leigo. Ponto e vírgula, dois pontos e travessão
na prosa dos arquivos de conteúdo, fora das citações. Cada ocorrência da forma longa do OIC, para a leitura humana
da regra das maiúsculas. Páginas sem nenhum link de entrada. Páginas fora do sitemap. Títulos repetidos e
descrições vazias ou acima de 158 caracteres. Feito em 03/11/2026.
"""
import re, sys, html, json
from pathlib import Path
from collections import Counter, defaultdict
R = Path(__file__).resolve().parent.parent
INFO = ['conteudo/percurso.md', 'conteudo/camada-externa.md', 'conteudo/direitos.md', 'conteudo/problemas.md', 'conteudo/como-reclamar.md']
TODOS = INFO + ['conteudo/operar.md']
IGN = {'partes', 'ideias', 'blocos', 'direitos', 'relacionados', 'cartoes'}
def prosa(arq):
    pag = campo = None
    for i, l in enumerate((R / arq).read_text(encoding='utf-8').splitlines(), 1):
        if l.startswith('## '): pag, campo = l[3:].strip(), None; continue
        if l.startswith('### '):
            campo, _, pergunta = l[4:].strip().partition(' ')
            # A pergunta própria do bloco, no cabeçalho, passa pelas mesmas regras do texto.
            if pag and campo not in IGN and pergunta.strip().endswith('?'): yield i, pag, campo, pergunta.strip()
            continue
        if not pag or not campo or campo in IGN or not l.strip() or l.startswith(('>', '#', 'lei:')): continue
        yield i, pag, campo, l.strip()
print('# 1. Frases acima de 37 palavras na Informação')
n = 0
for arq in INFO:
    for i, pag, campo, l in prosa(arq):
        for f in re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ"“])', l):
            k = len(re.findall(r"[\wÀ-ÿ]+(?:-[\wÀ-ÿ]+)*", f))
            if k > 37: n += 1; print(f'  {arq}:{i} [{pag}/{campo}] {k} palavras  {f[:90]}')
print(f'  total {n}')
print('# 2. Pontuação proibida nos arquivos de origem, fora das citações')
n = 0
for arq in TODOS:
    for i, pag, campo, l in prosa(arq):
        sem = re.sub(r'`[^`]*`', '', l)
        if re.search(r'[;—–]|\w:\s', sem): n += 1; print(f'  {arq}:{i} [{pag}/{campo}] {sem[:100]}')
print(f'  total {n}')
print('# 3. Forma longa do OIC na prosa')
for arq in TODOS:
    for i, pag, campo, l in prosa(arq):
        for m in re.finditer(r'[Oo]bjeto [Ii]material de [Cc]onsumo', l):
            print(f'  {arq}:{i} [{pag}/{campo}] {m.group(0)}  …{l[max(0,m.start()-60):m.end()+30]}…')
print('# 4. Páginas sem nenhum link de entrada')
D = R / 'docs'
paginas = {p.relative_to(D).as_posix() for p in D.rglob('index.html')}
entrada = Counter()
for p in D.rglob('*.html'):
    base = p.parent
    for href in re.findall(r'href="([^"#?]+)', p.read_text(encoding='utf-8')):
        if href.startswith(('http', 'mailto')): continue
        alvo = (base / href).resolve()
        try: rel = alvo.relative_to(D.resolve()).as_posix()
        except ValueError: continue
        if not rel.endswith('.html'): rel = (rel.rstrip('/') + '/index.html').lstrip('/')
        if rel.startswith('./'): rel = rel[2:]
        if (D / rel) != p: entrada[rel] += 1
orfas = sorted(x for x in paginas if entrada[x] == 0 and x != 'index.html')
print('  ', orfas[:30], len(orfas))
print('# 5. Sitemap')
sm = set(re.findall(r'<loc>https://lexplataformae.com.br/([^<]*)</loc>', (D / 'sitemap.xml').read_text()))
fora = sorted(x for x in paginas if x.replace('index.html', '') not in sm and x != '404/index.html')
print('   fora do sitemap', fora[:20], len(fora))
print('# 6. Títulos repetidos e descrições')
tit = defaultdict(list); longas = []
for p in paginas:
    s = (D / p).read_text(encoding='utf-8')
    t = html.unescape(re.search(r'<title>(.*?)</title>', s).group(1))
    tit[t].append(p)
    dsc = re.search(r'<meta name="description" content="([^"]*)"', s)
    if not dsc or not dsc.group(1).strip(): longas.append(('sem descrição', p))
    elif len(html.unescape(dsc.group(1))) > 158: longas.append(('longa', p))
rep = {t: ps for t, ps in tit.items() if len(ps) > 1}
print('   títulos repetidos', len(rep)); [print('    ', t, ps[:4]) for t, ps in list(rep.items())[:10]]
print('   descrições', longas[:10], len(longas))
