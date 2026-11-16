# coding: utf-8
from pathlib import Path
import re,base64,json
ns={};s=Path('work/pi-armadura.py').read_text();exec(s[:s.index("font=ImageFont")],ns)
O=Path('outputs/linguagem-pi-armadura-v2');source=Path('outputs/linguagem-pi-armadura/armadura-claro.png');data=base64.b64encode(source.read_bytes()).decode()
def rgb(h):return [int(h[i:i+2],16)/255 for i in (1,3,5)]
def drawing(shapes,theme,uid):
 raw=ns['svg'](shapes,'claro');ink,blue=('#211c17','#002fa7') if theme=='claro' else ('#ebe7e1','#497ef7');a,b=rgb(ink),rgb(blue)
 filt=f'<defs><filter id="{uid}" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="-1 0 1 0 0  -1 0 1 0 0  -1 0 1 0 0  0 0 0 1 0"/><feComponentTransfer><feFuncR type="discrete" tableValues="0 0 1 1 1 1 1 1 1 1"/><feFuncG type="discrete" tableValues="0 0 1 1 1 1 1 1 1 1"/><feFuncB type="discrete" tableValues="0 0 1 1 1 1 1 1 1 1"/><feFuncA type="discrete" tableValues="0 0 0 0 0 0 0 0 0 1"/></feComponentTransfer><feComponentTransfer>'+''.join(f'<feFunc{ch} type="table" tableValues="{a[i]} {b[i]}"/>' for i,ch in enumerate('RGB'))+'</feComponentTransfer></filter></defs>'
 raw=raw.replace('<image ',filt+f'<image filter="url(#{uid})" ',1)
 return raw
for id,title,shapes,desc in ns['items']:
 for theme in ['claro','escuro']:
  raw=drawing(shapes,theme,id+'-'+theme)
  colors=('color:#211c17;--traco:#615953;--tese-linha:#002fa7' if theme=='claro' else 'color:#ebe7e1;--traco:#a9a49c;--tese-linha:#497ef7')
  raw=raw.replace('viewBox=',f'width="1200" height="900" style="{colors}" viewBox=',1)
  (O/f'{id}-{theme}.svg').write_text(raw)
sections=[]
for mode,theme,bg,ink,gray,blue in ns['pal']:
 cards=''.join('<figure>'+drawing(shapes,theme,id+'-'+theme+'-'+mode)+f'<figcaption><h3>{title}</h3><p>{desc}</p></figcaption></figure>' for id,title,shapes,desc in ns['items'])
 sections.append(f'<section style="background:{bg};color:{ink};--traco:{gray};--tese-linha:{blue}"><h2>{mode} · {theme}</h2>{cards}</section>')
(O/'previa.html').write_text('<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Armadura — cores planas</title><style>body{margin:0;font:18px/1.6 system-ui}header{padding:24px;max-width:900px;margin:auto}section{padding:24px max(20px,calc((100vw - 900px)/2))}svg{width:100%;height:auto;display:block}figure{margin:0 0 48px}figcaption{max-width:65ch}</style><header><h1>A armadura em cores planas</h1><p>Uma única matriz, duas paletas. Sem sombreado, brilho ou fundo próprio. Legendas externas ao desenho.</p></header>'+''.join(sections)+'</html>')
print('Seis SVGs gerados a partir da mesma matriz, com o mesmo filtro de silhueta.')
