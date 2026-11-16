# coding: utf-8
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math,json,html,zipfile
O=Path('outputs/linguagem-pi-lote-1');O.mkdir(exist_ok=True)
def line(p,c='ink',w=2.5):return ('line',p,c,w)
def poly(p,c='blue'):return ('polygon',p,c,0)
def ellipse(cx,cy,rx,ry):return [(cx+rx*math.cos(t*math.pi/60),cy+ry*math.sin(t*math.pi/60)) for t in range(121)]
def cube():return [line([(60,85),(120,50),(180,85),(180,155),(120,190),(60,155),(60,85)]),line([(60,85),(120,120),(180,85)]),line([(120,120),(120,190)])]
def sphere():return [line(ellipse(120,120,70,70)),line(ellipse(120,120,70,23)),line(ellipse(120,120,25,70))]
def cylinder():return [line(ellipse(120,65,62,22)),line([(58,65),(58,165)]),line([(182,65),(182,165)]),line([(120+62*math.cos(t*math.pi/60),165+22*math.sin(t*math.pi/60)) for t in range(61)])]
def pyramid():return [line([(120,42),(53,164),(120,197),(187,164),(120,42)]),line([(120,42),(120,197)]),line([(53,164),(120,133),(187,164)],'gray',1.8)]
def flow():return [poly([(174,205),(198,192),(362,192),(362,208),(202,208),(182,220)])]
def protect():return [line([(x,y) for x,y in p],w=2) for p in [[(50,79),(120,38),(190,79),(190,161),(120,202),(50,161),(50,79)],[(55,82),(120,44),(185,82),(185,158),(120,196),(55,158),(55,82)]]]
def transform(s,k,dx,dy):return [(t,[(x*k+dx,y*k+dy) for x,y in p],c,w) for t,p,c,w in s]
items=[('pi-cubo-expressao','Expressão',cube()+flow(),'O cubo representa a expressão do objeto. A faixa azul representa seu uso. A forma não declara, por si, a existência de um direito.'),('pi-esfera-solucao','Solução técnica',sphere()+flow(),'A esfera representa a dimensão técnica do objeto; suas linhas curvas indicam volume. A faixa representa o uso. Não há contorno de proteção nesta apresentação.'),('pi-cilindro-ornamento','Ornamento',cylinder()+flow(),'O cilindro apresenta uma superfície que pode receber uma configuração ornamental. A faixa representa o uso. A incidência de proteção não é presumida.'),('pi-piramide-distintividade','Distintividade',pyramid()+flow(),'A pirâmide representa a dimensão distintiva. A faixa azul representa o uso; não é uma seta de identificação de origem.'),('pi-cubo-software','Expressão e funcionamento',transform(cube()+protect(),.78,0,10)+transform(sphere(),.61,215,35)+[line([(165,104),(227,104)],'gray',2)]+flow(),'O cubo tem o contorno da proteção da expressão examinada. A esfera, apresentada separadamente, representa o funcionamento. Estar fora deste contorno não significa ausência de qualquer outra proteção.'),('pi-papel-dominio-publico','Uma exclusividade delimitada',transform(cube()+protect(),.68,5,35)+transform(sphere(),.43,210,-2)+transform(cylinder(),.43,210,95)+flow(),'Somente o cubo recebe o contorno da exclusividade examinada. As outras dimensões permanecem separadas desse contorno. O fundo é neutro; não representa automaticamente domínio público.')]
P=[('Informação','claro','#faf6ef','#211c17','#615953','#002fa7'),('Informação','escuro','#17130f','#ebe7e1','#a9a49c','#497ef7'),('Doutrina','claro','#f0f5f9','#161b22','#535c66','#002fa7'),('Doutrina','escuro','#131a23','#e4e8ed','#a4acb4','#497ef7'),('Ciência','claro','#f7fbfc','#13161a','#51565b','#002fa7'),('Ciência','escuro','#121416','#e9ebee','#b8bec5','#497ef7')]
def svg(s):
 out=[]
 for t,p,c,w in s:
  colour={'ink':'currentColor','gray':'var(--traco, #615953)','blue':'var(--tese-linha, #002fa7)'}[c]; pts=' '.join(f'{x:.2f},{y:.2f}' for x,y in p)
  out.append(f'<polygon points="{pts}" fill="{colour}"/>' if t=='polygon' else f'<polyline points="{pts}" fill="none" stroke="{colour}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
 return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 260" aria-hidden="true" focusable="false">'+''.join(out)+'</svg>'
def raster(s,pal):
 im=Image.new('RGBA',(1200,780));d=ImageDraw.Draw(im);colors=dict(zip(['ink','gray','blue'],pal))
 for t,p,c,w in s:
  p=[(x*3,y*3) for x,y in p]
  if t=='polygon':d.polygon(p,fill=colors[c])
  else:d.line(p,fill=colors[c],width=round(w*3),joint='curve')
 return im
font='/System/Library/Fonts/Supplemental/Arial.ttf'; f=ImageFont.truetype(font,22); small=ImageFont.truetype(font,18)
manifest=[]
for id,title,s,desc in items:
 (O/(id+'.svg')).write_text(svg(s))
 for _,theme,bg,*pal in P[:2]:
  im=raster(s,pal); im.save(O/f'{id}-{theme}.png');im.save(O/f'{id}-{theme}.webp',lossless=True)
  assert im.getpixel((0,0))[3]==0
 manifest.append({'id':id,'titulo':title,'descricao':desc,'largura':1200,'altura':780,'status':'estudo para aprovação','fundo':'transparente'})
for mode in ['Informação','Doutrina','Ciência']:
 sheet=Image.new('RGB',(1600,1050));d=ImageDraw.Draw(sheet)
 for _,theme,bg,*pal in [p for p in P if p[0]==mode]:
  offset=0 if theme=='claro' else 800
  d.rectangle((offset,0,offset+800,1050),fill=bg);d.text((offset+24,18),mode+' · '+theme,font=f,fill=pal[0])
  for n,(id,title,s,desc) in enumerate(items):
   x=offset+(n%2)*400;y=55+(n//2)*330
   im=raster(s,pal).resize((400,260),Image.Resampling.LANCZOS);sheet.paste(im,(x,y),im);d.text((x+24,y+265),title,font=small,fill=pal[0])
 sheet.save(O/('prancha-'+{'Informação':'informacao','Doutrina':'doutrina','Ciência':'ciencia'}[mode]+'.png'))
sections=[]
for mode,theme,bg,ink,gray,blue in P:
 cards=''.join('<figure>'+svg(s)+'<figcaption><h3>'+title+'</h3><p>'+desc+'</p></figcaption></figure>' for id,title,s,desc in items)
 sections.append(f'<section style="--bg:{bg};--ink:{ink};--traco:{gray};--tese-linha:{blue}"><h2>{mode} · {theme}</h2><div class="grid">{cards}</div></section>')
(O/'previa.html').write_text('''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Linguagem geométrica — primeiro lote</title><style>*{box-sizing:border-box}body{margin:0;background:#faf6ef;color:#211c17;font:18px/1.55 system-ui}header,footer{max-width:1050px;margin:auto;padding:32px 24px}h1{font:36px/1.2 Georgia}h2{font-size:22px}h3{font-size:19px}section{background:var(--bg);color:var(--ink);padding:24px max(20px,calc((100vw - 1050px)/2))}.grid{display:grid;grid-template-columns:1fr 1fr;gap:32px}figure{margin:0;min-width:0}svg{display:block;width:100%;height:auto}figcaption{padding:0 20px}figcaption p{font-size:16px}@media(max-width:620px){.grid{grid-template-columns:1fr}h1{font-size:28px}}@media(forced-colors:active){section{background:Canvas;color:CanvasText;--traco:CanvasText!important;--tese-linha:CanvasText!important}}</style><header><p>LEX PLATAFORMAE · LINGUAGEM GEOMÉTRICA</p><h1>Quatro dimensões, uma linguagem comum.</h1><p>As formas são convenções de leitura: cubo para expressão, esfera para solução técnica, cilindro para ornamento e pirâmide para distintividade. Nenhuma forma equivale automaticamente a um direito.</p><p>O contorno duplo delimita a exclusividade examinada. A faixa azul representa o uso. O fundo permanece neutro.</p></header>'''+''.join(sections)+'<footer><p>Estudos para aprovação. Textos externos aos desenhos. As descrições adjacentes fornecem a informação equivalente para leitores de tela. Fontes jurídicas e integração editorial devem ser conferidas antes da publicação.</p></footer></html>')
(O/'manifesto.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(O/'LEIA-ME.md').write_text('''# Linguagem geométrica — lote 1

Seis estudos; aprovação anterior refere-se ao protótipo de exclusividade e controle do uso. Este lote apresenta as quatro convenções e duas primeiras relações. Não publicado.

SVGs adaptáveis devem ser inseridos no HTML, acompanhados das descrições do manifesto. PNG e WebP são provas transparentes de 1200 × 780, não substituem a integração responsiva. Não há texto visível dentro dos desenhos. Pranchas têm títulos e fundos apenas para revisão.

O nome histórico pi-papel-dominio-publico foi preservado para rastreabilidade; a composição agora se chama Uma exclusividade delimitada e o fundo não significa domínio público.

Geometria única nos dois temas; cores dos seis contextos do site. Faixa de uso sem ponta; contorno duplo apenas onde se examina proteção. Os sólidos introdutórios não recebem contorno de incidência. Não há citações novas nem afirmação de validação jurídica.

No celular, a prévia organiza as peças em coluna. Inspeção visual das pranchas e verificação de transparência realizadas. Validação em navegador, leitores de tela e compreensão com pessoas ainda pendentes.
''')
with zipfile.ZipFile(O.parent/'linguagem-pi-lote-1.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in O.iterdir():z.write(p,arcname=p.name)
print('6 SVGs, 12 PNGs, 12 WebPs, 3 pranchas, prévia e pacote.')
