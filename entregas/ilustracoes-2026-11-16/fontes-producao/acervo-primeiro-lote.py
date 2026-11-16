# coding: utf-8
from pathlib import Path
import re,json,shutil,xml.etree.ElementTree as ET
O=Path('outputs/familia-3-lote-1');O.mkdir(exist_ok=True)
# Use exactly the approved SVG armor matrix and its deterministic palette treatment.
base=Path('outputs/linguagem-pi-armadura-v2')
arm={}
for theme in ['claro','escuro']:
 s=(base/f'pi-skin-objeto-{theme}.svg').read_text()
 defs=re.search(r'<defs>.*?</defs>',s).group();im=re.search(r'<image .*?/>',s).group()
 m=re.search(r'data:image/png;base64,([A-Za-z0-9+/=]+)',im)
 if m:
  import base64
  (O/'matriz-armadura.png').write_bytes(base64.b64decode(m.group(1)))
  im=im.replace(m.group(0),'matriz-armadura.png')
 arm[theme]=(defs,im)
def armor(theme,x,y,w=240,h=560):return f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="290 45 220 510" overflow="hidden">{arm[theme][1]}</svg>'
def path(d,c='ink',w=7,dash=False):return f'<path d="{d}" stroke="{dict(ink="currentColor",gray="var(--traco)",blue="var(--tese-linha)")[c]}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"'+(' stroke-dasharray="16 14"' if dash else '')+'/>'
def circle(x,y,r=24):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="currentColor" stroke-width="7"/>'
def block(x,y,w=85,h=85):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="var(--tese-linha)"/>'
items=[
('inicio','Um objeto, uma sustentação governada',1600,'A armadura permanece sobre uma pequena plataforma suspensa. Dois apoios ligam a plataforma a pontos de controle visíveis. A sustentação do uso depende de uma estrutura externa.'),
('imagem-catraca','O circuito de uso pode ser interrompido',1200,'A armadura está intacta dentro de um circuito. Uma passagem regulável interrompe a continuidade do percurso, sem destruir o objeto.'),
('imagem-estoque-fluxo','Guardar unidades e sustentar um fluxo',1200,'À esquerda, três unidades permanecem armazenadas. À direita, uma unidade depende de um circuito que tem uma interrupção visível. A unidade continua inteira.'),
('parte-a-mudanca','O objeto permanece; a conexão muda',1600,'A mesma armadura aparece duas vezes sobre o mesmo suporte. Na primeira situação as conexões são contínuas; na segunda, elas são interrompidas. Não há dano físico à armadura.'),
('ideia-equivalencia-de-valor-funcional','A mesma aparência, menos uso',1600,'Duas armaduras idênticas acompanham faixas de uso de extensões diferentes. A aparência permanece igual, mas a utilidade representada diminui. As faixas não são uma medida numérica.'),
('ideia-feixe-de-fruicao-governada','Três vínculos sustentam a posição de uso',1600,'Uma armadura central depende de três vínculos ligados a controles separados. Cada ligação tem começo e fim visíveis. O desenho representa dependências, não fios físicos presentes no objeto.')]
def scene(id,t):
 if id=='inicio':
  return path('M 455 210 L 610 745 M 1145 210 L 990 745','gray')+circle(440,185)+circle(1160,185)+path('M 575 745 H 1025 V 772 H 575 Z')+armor(t,680,199,240,570)
 if id=='imagem-catraca':
  return path('M 395 210 H 300 Q 235 210 235 280 V 640 Q 235 715 310 715 H 890 Q 965 715 965 640 V 280 Q 965 210 890 210 H 735','gray',9)+path('M 425 210 H 535','blue',16)+path('M 640 210 H 705','blue',16)+path('M 585 155 V 265',w=12)+circle(585,125,20)+armor(t,455,260,200,425)
 if id=='imagem-estoque-fluxo':
  return block(205,410)+block(310,410)+block(258,305)+path('M 180 510 V 570 H 425 V 510')+block(850,350)+path('M 800 300 H 765 Q 705 300 705 360 V 590 Q 705 650 765 650 H 1000 Q 1050 650 1050 590 V 360 Q 1050 300 1000 300 H 950','gray',9)+path('M 795 300 H 850 M 910 300 H 950','blue',16)+path('M 880 255 V 345',w=10)+path('M 815 465 H 975')
 if id=='parte-a-mudanca':
  s=''
  for x in [410,1010]:
   s+=armor(t,x,199,180,430)+path(f'M {x-50} 610 H {x+230} V 635 H {x-50} Z')
   for dx in [0,180]:
    xx=x+dx;s+=circle(xx,735,21)
    s+=path(f'M {xx} 635 V 710' if x==410 else f'M {xx} 635 V 655 M {xx} 690 V 710','gray',8)
  return s
 if id=='ideia-equivalencia-de-valor-funcional':
  return armor(t,410,165,180,430)+armor(t,1010,165,180,430)+path('M 330 665 H 670 M 930 665 H 1070','blue',24)+path('M 330 715 H 670 M 930 715 H 1270','gray',5)
 if id=='ideia-feixe-de-fruicao-governada':
  return path('M 445 250 H 620 L 715 340 M 1155 250 H 980 L 885 340 M 800 730 V 627','gray',8)+circle(415,250)+circle(1185,250)+circle(800,760)+armor(t,700,175,200,465)
for id,title,width,desc in items:
 for t in ['claro','escuro']:
  ink,gray,blue=('#211c17','#615953','#002fa7') if t=='claro' else ('#ebe7e1','#a9a49c','#497ef7')
  name=id+('-escuro' if t=='escuro' else '')
  s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="900" viewBox="0 0 {width} 900" aria-hidden="true" style="color:{ink};--traco:{gray};--tese-linha:{blue}">{arm[t][0]}{scene(id,t)}</svg>'
  (O/f'{name}.svg').write_text(s)
(O/'manifesto.json').write_text(json.dumps([{'id':id,'titulo':title,'alt':desc,'largura':w,'altura':900,'estado':'estudo para aprovação; Família 3 parcial'} for id,title,w,desc in items],ensure_ascii=False,indent=2))
(O/'previa.html').write_text('''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Acervo — sustentação e uso</title><style>body{margin:0;font:18px/1.6 system-ui}header{padding:30px;max-width:1100px;margin:auto}section{padding:24px max(16px,calc((100vw - 1100px)/2))}figure{margin:0 0 40px}img{width:100%;height:auto}figcaption{max-width:65ch}.dark{background:#131a23;color:#e4e8ed}.light{background:#f0f5f9;color:#161b22}</style><header><h1>Sustentação, continuidade e valor de uso</h1><p>Primeiro grupo da Família 3. Os seis desenhos são metáforas conceituais; as legendas ficam fora da arte.</p></header>'''+''.join(f'<section class="{cl}"><h2>{title}</h2>'+''.join(f'<figure><img src="{id}{suffix}.webp" width="{w}" height="900" alt="{desc}"><figcaption>{name}</figcaption></figure>' for id,name,w,desc in items)+'</section>' for cl,title,suffix in [('light','Tema claro',''),('dark','Tema escuro','-escuro')])+'</html>')
print('Seis composições; doze matrizes SVG preparadas.')
