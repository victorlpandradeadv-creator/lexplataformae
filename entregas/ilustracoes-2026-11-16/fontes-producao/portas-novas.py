# coding: utf-8
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math,json,zipfile
O=Path('outputs/familia-1-nova');O.mkdir(exist_ok=True)
def L(p,c='ink',w=12):return ('line',p,c,w)
def P(p,c='blue'):return ('poly',p,c,0)
def circle(x,y,r,c='blue',fill=True):
 p=[(x+r*math.cos(i*math.pi/60),y+r*math.sin(i*math.pi/60)) for i in range(121)];return P(p,c) if fill else L(p,c)
def square(x,y,s,c='blue'):return P([(x,y),(x+s,y),(x+s,y+s),(x,y+s)],c)
items=[
('porta-acesso','Perdi o acesso','A conta foi bloqueada, o presente sumiu ou o serviço anunciou que vai acabar, e o que estava lá dentro foi embora junto.',[L([(80,285),(205,285)]),L([(245,140),(245,350)],w=18),square(305,240,60)]),
('porta-mudou','O que comprei mudou','O que você comprou continua na conta, mas deixou de fazer o que fazia quando você pagou por ele.',[square(100,115,60),square(300,115,60),L([(80,225),(100,225),(100,285),(160,285),(160,225),(190,225)]),L([(265,225),(265,285),(325,285),(325,225),(380,225)])]),
('porta-empurrado','Fui empurrado a pagar','A oferta apressou, o sorteio escondeu as chances ou a regra que pesou contra você estava enterrada nos termos de uso.',[L([(95,125),(240,205),(285,205)]),L([(95,355),(240,275),(285,275)]),L([(90,240),(218,240)],'blue',18),circle(340,240,38)]),
('porta-sair','Quero sair e levar o que é meu','Sair parece livre, mas custa o histórico, a reputação, os itens e as pessoas que você conheceu ali. Esse custo também conta.',[L([(100,200),(100,280)]),L([(100,240),(285,240)],'gray',10),L([(230,100),(230,180)]),L([(230,300),(230,380)]),square(290,190,45),square(350,190,45),square(290,250,45)]),
('porta-decide','A plataforma decide sobre mim sem explicar','O alcance caiu, a regra do aplicativo mudou ou a loja puniu sem dizer por quê. Vale para quem compra, e também para quem vende ou trabalha ali.',[L([(85,240),(180,240)],'blue',18),L([(300,175),(350,175),(350,125)],w=12),L([(300,305),(395,305)],w=12),circle(350,110,15,'ink'),circle(405,305,15,'ink'),L([(215,165),(215,190)]),L([(215,215),(215,240)]),L([(215,265),(215,290)]),L([(215,315),(215,335)]),L([(270,165),(270,190)]),L([(270,215),(270,240)]),L([(270,265),(270,290)]),L([(270,315),(270,335)])]),
('porta-comum','Provar e reclamar','Seja qual for a porta, chega a hora de provar o que aconteceu e de reclamar onde a resposta conta.',[L([(95,140),(215,140),(215,330),(95,330),(95,140)],'blue'),L([(215,285),(255,285)],'gray',10),L([(260,155),(385,155),(385,250),(320,250),(285,285),(285,250),(260,250),(260,155)])])]
palettes=[('Informação','claro','#faf6ef','#211c17','#615953','#002fa7'),('Informação','escuro','#17130f','#ebe7e1','#a9a49c','#497ef7'),('Doutrina','claro','#f0f5f9','#161b22','#535c66','#002fa7'),('Doutrina','escuro','#131a23','#e4e8ed','#a4acb4','#497ef7'),('Ciência','claro','#f7fbfc','#13161a','#51565b','#002fa7'),('Ciência','escuro','#121416','#e9ebee','#b8bec5','#497ef7')]
def svg(shapes):
 out='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 480" aria-hidden="true">'
 for t,p,c,w in shapes:
  col={'ink':'currentColor','gray':'var(--traco, #615953)','blue':'var(--tese-linha, #002fa7)'}[c];points=' '.join(f'{x:.2f},{y:.2f}' for x,y in p)
  out+=f'<polygon points="{points}" fill="{col}"/>' if t=='poly' else f'<polyline points="{points}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
 return out+'</svg>'
def raster(shapes,cols):
 im=Image.new('RGBA',(1920,1920));d=ImageDraw.Draw(im);cm=dict(zip(['ink','gray','blue'],cols))
 for t,p,c,w in shapes:
  pts=[(x*4,y*4) for x,y in p]
  if t=='poly':d.polygon(pts,fill=cm[c])
  else:
   d.line(pts,fill=cm[c],width=int(w*4),joint='curve')
   for x,y in pts:d.ellipse((x-w*2,y-w*2,x+w*2,y+w*2),fill=cm[c])
 return im.resize((480,480),Image.Resampling.LANCZOS)
for id,title,desc,shapes in items:
 (O/f'{id}.svg').write_text(svg(shapes))
 for _,theme,bg,*cols in palettes[:2]:
  im=raster(shapes,cols);name=id+('-escuro' if theme=='escuro' else '');im.save(O/f'{name}.png');im.save(O/f'{name}.webp',quality=85,method=6)
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',20)
for mode in ['Informação','Doutrina','Ciência']:
 sheet=Image.new('RGB',(1440,1050));d=ImageDraw.Draw(sheet)
 for _,theme,bg,*cols in [p for p in palettes if p[0]==mode]:
  x0=0 if theme=='claro' else 720;d.rectangle((x0,0,x0+720,1050),fill=bg);d.text((x0+24,20),mode+' · '+theme,font=font,fill=cols[0])
  for i,(id,title,desc,shapes) in enumerate(items):
   x=x0+(i%2)*360;y=60+(i//2)*325;im=raster(shapes,cols).resize((280,280),Image.Resampling.LANCZOS);sheet.paste(im,(x+40,y),im)
   # Two title lines where needed, outside artwork.
   words=title.split();lines=['']
   for word in words:
    if len(lines[-1])+len(word)>29:lines.append(word)
    else:lines[-1]+=(' ' if lines[-1] else '')+word
   for j,t in enumerate(lines):d.text((x+22,y+265+j*23),t,font=font,fill=cols[0])
 sheet.save(O/f'prancha-{dict(Informação="informacao",Doutrina="doutrina",Ciência="ciencia")[mode]}.png')
small=Image.new('RGB',(720,540),'#faf6ef');d=ImageDraw.Draw(small)
for theme,bg,cols,x in [('claro','#faf6ef',['#211c17','#615953','#002fa7'],0),('escuro','#17130f',['#ebe7e1','#a9a49c','#497ef7'],360)]:
 d.rectangle((x,0,x+360,540),fill=bg)
 for i,(id,title,desc,shapes) in enumerate(items):
  im=raster(shapes,cols).resize((56,56),Image.Resampling.LANCZOS);small.paste(im,(x+18,20+i*85),im);d.text((x+90,35+i*85),id.replace('porta-',''),font=font,fill=cols[0])
small.save(O/'prova-56px.png')
sections=[]
for mode,theme,bg,ink,gray,blue in palettes:
 cards=''.join(f'<article><div class="heading">{svg(shapes)}<h3>{title}</h3></div><p>{desc}</p></article>' for id,title,desc,shapes in items)
 sections.append(f'<section style="background:{bg};color:{ink};--traco:{gray};--tese-linha:{blue}"><h2>{mode} · {theme}</h2><div class="grid">{cards}</div></section>')
(O/'previa.html').write_text('''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Seis portas — nova direção</title><style>*{box-sizing:border-box}body{margin:0;font:18px/1.55 system-ui}header{padding:28px;max-width:1100px;margin:auto}section{padding:24px max(16px,calc((100vw - 1100px)/2))}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}article{padding:18px;border:1px solid currentColor;border-radius:4px}.heading{display:flex;gap:16px;align-items:center}.heading svg{width:56px;height:56px;flex-shrink:0}h3{font-size:20px;line-height:1.3}p{font-size:16px}h2{font-size:22px}@media(max-width:900px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:620px){.grid{grid-template-columns:1fr}}</style><header><h1>Escolha o que aconteceu</h1><p>Estudo das vinhetas com os títulos e descrições atuais do site. Os contextos de Doutrina e Ciência abaixo são provas de cor, não propostas de inserir cartões onde hoje não existem.</p></header>'''+''.join(sections)+'</html>')
checks=[]
for id,title,desc,shapes in items:
 a=Image.open(O/f'{id}.png');b=Image.open(O/f'{id}-escuro.png');assert a.getchannel('A').tobytes()==b.getchannel('A').tobytes();assert a.size==(480,480)
 checks.append({'id':id,'dimensoes':[480,480],'alfa_identico':True,'alt':'','uso':'Vinheta decorativa junto ao título de navegação'})
(O/'manifesto.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
(O/'LEIA-ME.md').write_text('''# Família 1 — nova direção

Seis vinhetas redesenhadas; substituem os estudos anteriores de fundos opacos. SVGs editáveis, mestres PNG e 12 WebPs transparentes de 480 × 480, qualidade 85. Paleta clara seguida da escura aplicada à mesma geometria. Nenhum sombreado, fundo, texto ou marca nos desenhos.

Títulos e descrições conferidos em docs/index.html do repositório em 15/11/2026. Componente: artigos porta-perda em portas-grade grade-perda, modos 0 e 2; Doutrina possui conteúdo próprio. A prévia recria cartões com texto real, não altera o componente publicado. Vinhetas apresentadas a 56 pixels, com alternativa vazia por repetirem a função do título. Não há links simulados ou publicação.

Conferências: dimensões, canal alfa idêntico entre temas e prova visual. Teste com leitores ainda pendente. A prova de cores não autoriza inserir as vinhetas nos três modos indiscriminadamente.
''')
with zipfile.ZipFile(O.parent/'familia-1-nova.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in O.iterdir():z.write(p,arcname=p.name)
print('Família 1: seis pares, SVGs, pranchas, prova 56px e cartões com texto real.')
