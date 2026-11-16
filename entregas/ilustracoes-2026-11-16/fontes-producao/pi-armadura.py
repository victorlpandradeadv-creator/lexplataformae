# coding: utf-8
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import base64,json,zipfile
O=Path('outputs/linguagem-pi-armadura')
base=Path('work/linguagem-pi.py').read_text(); ns={};exec(base[:base.index('items=')],ns)
cube,sphere,cylinder,pyramid,transform,poly,line,protect=[ns[x] for x in ['cube','sphere','cylinder','pyramid','transform','poly','line','protect']]
def dash(points):
 import math
 out=[]
 for a,b in zip(points,points[1:]):
  length=math.dist(a,b)
  for st in range(0,int(length),16):
   en=min(st+9,length);out.append(line([(a[0]+(b[0]-a[0])*t/length,a[1]+(b[1]-a[1])*t/length) for t in (st,en)],'gray',2.5))
 return out
pal=[('Informação','claro','#faf6ef','#211c17','#615953','#002fa7'),('Informação','escuro','#17130f','#ebe7e1','#a9a49c','#497ef7'),('Doutrina','claro','#f0f5f9','#161b22','#535c66','#002fa7'),('Doutrina','escuro','#131a23','#e4e8ed','#a4acb4','#497ef7'),('Ciência','claro','#f7fbfc','#13161a','#51565b','#002fa7'),('Ciência','escuro','#121416','#e9ebee','#b8bec5','#497ef7')]
# Shared coordinate system: 800 by 600. No labels are placed inside the image.
obj=[]
dims=[]
for dx,dy,fn in [(330,10,cube),(535,10,sphere),(330,285,cylinder),(535,285,pyramid)]:dims+=transform(fn(),.83,dx,dy)
ctrl=[]
for dy in [10,285]:
 ctrl+=transform(cube()+protect(),.75,345,dy)
 y=dy+183
 ctrl+=[poly([(490,y+14),(510,y),(635 if dy==285 else 755,y),(635 if dy==285 else 755,y+16),(515,y+16),(498,y+28)])]
 if dy==285:
  ctrl+=dash([(365,dy+10),(650,dy+10),(650,dy+240),(365,dy+240),(365,dy+10)])+[poly([(675,y),(755,y),(755,y+16),(675,y+16)])]
items=[('pi-skin-objeto','A armadura como objeto',obj,'A mesma armadura canônica, em vista frontal. Nenhum sinal distintivo, mecanismo ou ornamento novo foi acrescentado.'),('pi-skin-dimensoes','Dimensões separadas',dims,'Ao lado da armadura, cubo e esfera acima, cilindro e pirâmide abaixo: expressão, solução técnica, ornamento e distintividade. São perguntas de análise, não quatro proteções presumidas. A aparência da skin não comprova função técnica; esta referência não contém emblema.'),('pi-skin-controle','Proteção e controle do uso',ctrl,'Ao lado da armadura, duas situações com o mesmo cubo protegido. Acima, a faixa de uso é contínua. Abaixo, o limite tracejado da plataforma interrompe a faixa. O controle sobre o uso é representado separadamente da proteção examinada.')]
def svg(shapes,theme):
 image=base64.b64encode((O/f'armadura-{theme}.png').read_bytes()).decode()
 # Object plate centered; other panels reserve right side for geometry.
 xx=230 if not shapes else 0
 s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" aria-hidden="true"><image x="{xx}" y="20" width="340" height="560" preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{image}"/>'
 for t,p,c,w in shapes:
  col={'ink':'currentColor','gray':'var(--traco, #615953)','blue':'var(--tese-linha, #002fa7)'}[c];pts=' '.join(f'{x:.2f},{y:.2f}' for x,y in p)
  s+=f'<polygon points="{pts}" fill="{col}"/>' if t=='polygon' else f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"/>'
 return s+'</svg>'
def render(shapes,theme,colors):
 im=Image.new('RGBA',(1200,900));armor=Image.open(O/f'armadura-{theme}.png');armor.thumbnail((510,840),Image.Resampling.LANCZOS);x=(345 if not shapes else 0)+(510-armor.width)//2;y=30+(840-armor.height)//2;im.alpha_composite(armor,(x,y));d=ImageDraw.Draw(im);cm=dict(zip(['ink','gray','blue'],colors))
 for t,p,c,w in shapes:
  p=[(x*1.5,y*1.5) for x,y in p]
  if t=='polygon':d.polygon(p,fill=cm[c])
  else:d.line(p,fill=cm[c],width=round(w*1.5),joint='curve')
 return im
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',24)
for mode in ['Informação','Doutrina','Ciência']:
 sheet=Image.new('RGB',(1600,1980));d=ImageDraw.Draw(sheet)
 for _,theme,bg,*colors in [p for p in pal if p[0]==mode]:
  x=0 if theme=='claro' else 800;d.rectangle((x,0,x+800,1980),fill=bg);d.text((x+24,20),mode+' · '+theme,font=font,fill=colors[0])
  for n,(id,title,shapes,desc) in enumerate(items):
   im=render(shapes,theme,colors);small=im.resize((800,600),Image.Resampling.LANCZOS);sheet.paste(small,(x,50+n*640),small);d.text((x+24,620+n*640),title,font=font,fill=colors[0])
   if mode=='Informação':
    im.save(O/f'{id}-{theme}.png');im.save(O/f'{id}-{theme}.webp',lossless=True);(O/f'{id}-{theme}.svg').write_text(svg(shapes,theme))
 sheet.save(O/('prancha-'+{'Informação':'informacao','Doutrina':'doutrina','Ciência':'ciencia'}[mode]+'.png'))
sections=[]
for mode,theme,bg,ink,gray,blue in pal:
 cards=''.join('<figure>'+svg(shapes,theme)+'<figcaption><h3>'+title+'</h3><p>'+desc+'</p></figcaption></figure>' for id,title,shapes,desc in items)
 sections.append(f'<section style="background:{bg};color:{ink};--traco:{gray};--tese-linha:{blue}"><h2>{mode} · {theme}</h2>{cards}</section>')
(O/'previa.html').write_text('''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>A armadura — sequência</title><style>body{margin:0;font:18px/1.6 system-ui;background:#faf6ef;color:#211c17}header,footer{max-width:900px;margin:auto;padding:32px 24px}h1{font:36px Georgia}section{padding:24px max(20px,calc((100vw - 900px)/2))}figure{margin:0 0 48px}svg{display:block;width:100%;height:auto}figcaption{max-width:65ch}h3{margin-bottom:0}p{margin-top:8px}</style><header><h1>Uma skin, diferentes perguntas.</h1><p>Sequência editorial: reconhecer o objeto, separar as dimensões e distinguir proteção de controle do uso. Os textos pertencem à página e não aos desenhos.</p></header>'''+''.join(sections)+'<footer><p>Estudo para aprovação. A comparação geométrica preserva os contornos entre situações. A armadura foi gerada a partir da folha canônica. As variantes de cor devem ser conferidas também quanto à fidelidade da forma.</p></footer></html>')
(O/'manifesto.json').write_text(json.dumps([{'id':id,'titulo':title,'descricao':desc,'tamanho':[1200,900]} for id,title,s,desc in items],ensure_ascii=False,indent=2))
print('Sequência composta e exportada.')
