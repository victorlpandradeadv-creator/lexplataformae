from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import html, json
O=Path('outputs/prototipo-pi'); O.mkdir(exist_ok=True)
# A single coordinate source generates SVG masters and raster proof sheets.
W,H=400,260
cube=[(60,85),(120,50),(180,85),(180,155),(120,190),(60,155),(60,85)]
outer=[(50,79),(120,38),(190,79),(190,161),(120,202),(50,161),(50,79)]
inner=[(55,82),(120,44),(185,82),(185,158),(120,196),(55,158),(55,82)]
def shapes(blocked):
 s=[('line',cube,'ink',2.5),('line',[(60,85),(120,120),(180,85)],'ink',2.5),('line',[(120,120),(120,190)],'ink',2.5),('line',outer,'ink',2),('line',inner,'ink',2)]
 # Flow is offset below the protected contour; connection is spatial, not a breach in it.
 s += [('polygon',[(174,184),(198,171),(265 if blocked else 362,171),(265 if blocked else 362,187),(202,187),(182,199)],'blue',0)]
 if blocked:
  # Dashed enclosure is only platform control; gap in the band carries meaning without colour.
  pts=[(32,25),(280,25),(280,224),(32,224),(32,25)]
  s += [('dash',pts,'gray',3)]
  s += [('polygon',[(298,171),(362,171),(362,187),(298,187)],'blue',0)]
 return s

def svg(blocked):
 parts=[]
 for typ,pts,c,w in shapes(blocked):
  colour={'ink':'currentColor','blue':'var(--tese-linha, #002fa7)','gray':'var(--traco, #615953)'}[c]
  coords=' '.join(f'{x},{y}' for x,y in pts)
  if typ=='polygon': parts.append(f'<polygon points="{coords}" fill="{colour}"/>')
  else: parts.append(f'<polyline points="{coords}" fill="none" stroke="{colour}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'+(' stroke-dasharray="9 7"' if typ=='dash' else '')+'/>')
 return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 260" aria-hidden="true" focusable="false">'+''.join(parts)+'</svg>'
for b,name in [(False,'uso-continuo'),(True,'uso-interrompido')]: (O/f'pi-{name}.svg').write_text(svg(b))
palettes=[('Informação · claro','#faf6ef','#211c17','#615953','#002fa7'),('Informação · escuro','#17130f','#ebe7e1','#a9a49c','#497ef7'),('Doutrina · claro','#f0f5f9','#161b22','#535c66','#002fa7'),('Doutrina · escuro','#131a23','#e4e8ed','#a4acb4','#497ef7'),('Ciência · claro','#f7fbfc','#13161a','#51565b','#002fa7'),('Ciência · escuro','#121416','#e9ebee','#b8bec5','#497ef7')]
def render(blocked,pal,scale=3):
 im=Image.new('RGBA',(400*scale,260*scale)); d=ImageDraw.Draw(im); colors=dict(zip(['ink','gray','blue'],pal))
 for typ,pts,c,w in shapes(blocked):
  p=[(x*scale,y*scale) for x,y in pts]
  if typ=='polygon': d.polygon(p, fill=colors[c])
  elif typ=='line': d.line(p,fill=colors[c],width=round(w*scale),joint='curve')
  else:
   import math
   for a,b in zip(p,p[1:]):
    length=math.dist(a,b)
    for start in range(0,round(length),16*scale):
     end=min(start+9*scale,length)
     q=[(a[0]+(b[0]-a[0])*t/length,a[1]+(b[1]-a[1])*t/length) for t in (start,end)]
     d.line(q,fill=colors[c],width=round(w*scale))
 return im
font='/System/Library/Fonts/Supplemental/Arial.ttf'
f=ImageFont.truetype(font,22); small=ImageFont.truetype(font,18)
sheet=Image.new('RGB',(1600,1080)); d=ImageDraw.Draw(sheet)
sections=[]
for i,(label,bg,ink,gray,blue) in enumerate(palettes):
 x=(i%2)*800; y=(i//2)*360
 d.rectangle((x,y,x+800,y+360),fill=bg); d.text((x+26,y+18),label,font=f,fill=ink)
 for b,xx,title in [(False,0,'Uso contínuo'),(True,400,'Uso interrompido')]:
  im=render(b,(ink,gray,blue)); im=im.resize((400,260),Image.Resampling.LANCZOS); sheet.paste(im,(x+xx,y+54),im)
  d.text((x+xx+30,y+316),title,font=small,fill=ink)
  if i<2: render(b,(ink,gray,blue)).save(O/f"pi-{'uso-interrompido' if b else 'uso-continuo'}-{'escuro' if i else 'claro'}.png")
 figures=''.join('<figure>'+svg(b)+f'<figcaption><strong>{title}</strong><p>{desc}</p></figcaption></figure>' for b,title,desc in [(False,'Uso contínuo','O contorno duplo delimita a proteção representada. A faixa do uso permanece contínua.'),(True,'Uso interrompido','A proteção permanece igual. O limite tracejado da plataforma interrompe a faixa do uso.')])
 sections.append(f'<section style="--papel:{bg};--tinta:{ink};--traco:{gray};--tese-linha:{blue}"><h2>{label}</h2><div class="pair">{figures}</div></section>')
sheet.save(O/'comparacao-seis-contextos.png')
page='''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Exclusividade e controle do uso — protótipo</title><style>*{box-sizing:border-box}body{margin:0;font:18px/1.55 system-ui;background:#faf6ef;color:#211c17}header,footer{max-width:1000px;margin:auto;padding:32px 24px}h1{font:normal 36px/1.15 Georgia}h2{font-size:18px;font-weight:500}section{background:var(--papel);color:var(--tinta);padding:24px max(20px,calc((100vw - 1000px)/2))}.pair{display:grid;grid-template-columns:1fr 1fr;gap:24px}figure{margin:0;min-width:0}svg{width:100%;height:auto;display:block}figcaption{padding:0 16px}p{max-width:65ch}figcaption p{font-size:16px}strong{font-weight:600}@media(max-width:620px){.pair{grid-template-columns:1fr;gap:32px}h1{font-size:28px}}@media(forced-colors:active){section{--tinta:CanvasText!important;--traco:CanvasText!important;--tese-linha:CanvasText!important;background:Canvas;color:CanvasText}}</style><header><p>LEX PLATAFORMAE · ESTUDO VISUAL</p><h1>A mesma proteção. Duas situações de uso.</h1><p>O contorno duplo representa o alcance da exclusividade examinada; a faixa azul representa o uso. O tracejado representa o controle da plataforma. O fundo não recebe significado jurídico.</p><p>Protótipo para revisão. As legendas pertencem à página; os desenhos não contêm texto.</p></header>'''+''.join(sections)+'''<footer><p>Leitura no celular: as duas situações aparecem em sequência. A diferença também está na continuidade da faixa, não apenas na cor.</p><p>Esta é uma convenção visual em teste, não uma representação de todos os requisitos ou regimes de proteção.</p></footer></html>'''
(O/'previa.html').write_text(page)
# Verify output properties and contrast of meaningful strokes on the actual six backgrounds.
def lum(h):
 v=[int(h[i:i+2],16)/255 for i in (1,3,5)]; return sum(w*(c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4) for w,c in zip([.2126,.7152,.0722],v))
checks=[]
for label,bg,*cols in palettes:
 ratios=[(max(lum(bg),lum(c))+.05)/(min(lum(bg),lum(c))+.05) for c in cols]
 assert min(ratios)>=3
 checks.append({'contexto':label,'contrastes':[round(v,2) for v in ratios]})
assert '<text' not in svg(0) and '<rect' not in svg(0)
(O/'conferencia.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
print('Gerados SVGs, PNGs transparentes, prancha, prévia responsiva e conferência de contraste.')
