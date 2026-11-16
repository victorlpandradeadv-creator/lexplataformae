# coding: utf-8
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,zipfile,math,textwrap
src=Path('work/portas-novas.py').read_text();ns={};exec(src[:src.index('items=')],ns);exec(src[src.index('palettes='):src.index('for id,title,desc,shapes in items:')],ns)
L,P,circle,square=[ns[x] for x in ['L','P','circle','square']];svg,raster=ns['svg'],ns['raster'];palettes=ns['palettes']
O=Path('outputs/familia-2-nova');O.mkdir(exist_ok=True)
def box(x,y,w,h,c='ink'):return L([(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)],c)
def dash(a,b,c='gray'):
 length=math.dist(a,b);return [L([(a[0]+(b[0]-a[0])*t/length,a[1]+(b[1]-a[1])*t/length) for t in (st,min(st+18,length))],c,10) for st in range(0,int(length),36)]
items=[
('direito-a','O que você comprou é produto, mesmo sem nada nas mãos','Um volume reconhecível por suas arestas representa o objeto imaterial.',[L([(110,165),(240,90),(370,165),(370,315),(240,390),(110,315),(110,165)],'blue'),L([(110,165),(240,240),(370,165)],'blue'),L([(240,240),(240,390)],'blue')]),
('direito-b','A plataforma não pode montar a experiência para você não entender','O percurso do leitor chega a uma passagem cuja continuidade não fica clara.',[circle(100,300,23),L([(135,300),(210,300),(210,200)]),L([(140,150),(210,150)]),L([(310,150),(370,150)])]+dash((245,120),(245,200))+dash((285,120),(285,200))),
('direito-c','A informação precisa servir para alguma coisa','A informação essencial ganha destaque dentro de um registro simples, sem escrita.',[box(120,85,240,310),L([(165,160),(285,160)],'gray'),L([(165,235),(315,235)],'blue',18),L([(165,310),(265,310)],'gray')]),
('direito-d','O que foi prometido precisa ser entregue','O módulo azul inteiro atravessa a abertura de entrega.',[L([(230,90),(230,175)]),L([(230,305),(230,390)]),L([(100,240),(175,240)],'gray'),square(275,195,90),L([(370,310),(370,335),(275,335)],'gray')]),
('direito-e','Mudança relevante precisa deixar rastro','Dois estados são ligados a um registro preservado, permitindo reconstituir a mudança.',[square(105,100,65),P([(325,90),(370,135),(325,180),(280,135)]),L([(137,190),(137,240),(325,240),(325,195)]),L([(235,240),(235,285)],'gray'),box(185,285,100,100,'blue')]),
('direito-f','Mudou, tem que manter o que valia','Objetos de formas diferentes mantêm a mesma extensão de função, representada pelas faixas iguais.',[square(100,130,85),circle(325,172,48),L([(90,290),(195,290)],'blue',20),L([(270,290),(375,290)],'blue',20)]),
('direito-g','Punição precisa de motivo e de chance de defesa','Um registro da decisão se liga a um espaço aberto de contestação.',[box(100,105,110,165),L([(210,210),(270,210)],'gray'),L([(280,150),(380,150),(380,245),(325,245),(285,285),(285,245),(280,245),(280,150)],'blue'),L([(150,290),(150,340),(320,340),(320,300)],'gray')]),
('direito-h','Quando a perda é regra, o problema é o desenho','Três percursos sofrem a mesma interrupção num único limite, tornando visível o padrão.',[L([(245,110),(245,370)],w=16)]+[L([(100,y),(205,y)],'blue',16) for y in [155,240,325]]+[L([(285,y),(370,y)],'blue',16) for y in [155,240,325]]),
('direito-i','A prova que está com a plataforma tem que aparecer','Um registro azul é separado de um conjunto de fichas para poder ser apresentado.',[L([(100,300),(100,115),(230,115)]),L([(140,335),(140,155),(270,155)]),box(220,210,135,170,'blue'),L([(275,175),(275,190)],'gray')]),
('direito-j','Ser dona da obra não é desculpa para tudo','Um comando encontra um limite: a prerrogativa da plataforma não se estende sem restrição.',[circle(120,160,28,'ink',False),L([(140,180),(200,240),(275,240)]),L([(320,105),(320,375)],'blue',18)]),
('direito-k','A resposta deve recompor o que você perdeu','Duas partes complementares formam um módulo, com a união em evidência.',[P([(100,145),(225,145),(225,215),(195,215),(195,285),(225,285),(225,345),(100,345)]),P([(250,145),(375,145),(375,345),(250,345),(250,310),(220,310),(220,240),(250,240)])])]
cache={}
for id,title,desc,shapes in items:
 (O/f'{id}.svg').write_text(svg(shapes))
 for _,theme,bg,*cols in palettes[:2]:
  im=raster(shapes,cols);cache[id,theme]=im;name=id+('-escuro' if theme=='escuro' else '');im.save(O/f'{name}.png');im.save(O/f'{name}.webp',quality=85,method=6)
font='/System/Library/Fonts/Supplemental/Arial.ttf';f=ImageFont.truetype(font,20);head=ImageFont.truetype(font,24)
for mode in ['Informação','Doutrina','Ciência']:
 sheet=Image.new('RGB',(1600,2220));d=ImageDraw.Draw(sheet)
 for _,theme,bg,*cols in [p for p in palettes if p[0]==mode]:
  off=0 if theme=='claro' else 800;d.rectangle((off,0,off+800,2220),fill=bg);d.text((off+24,20),mode+' · '+theme,font=head,fill=cols[0])
  for i,(id,title,desc,shapes) in enumerate(items):
   x=off+(i%2)*400;y=70+(i//2)*355
   im=cache[id,theme].resize((250,250),Image.Resampling.LANCZOS);sheet.paste(im,(x+75,y),im)
   for j,t in enumerate(textwrap.wrap(title,34)):d.text((x+24,y+248+j*24),t,font=f,fill=cols[0])
 sheet.save(O/f'prancha-{dict(Informação="informacao",Doutrina="doutrina",Ciência="ciencia")[mode]}.png')
small=Image.new('RGB',(880,990));d=ImageDraw.Draw(small)
for i,theme in enumerate(['claro','escuro']):
 bg,ink=('#faf6ef','#211c17') if i==0 else ('#17130f','#ebe7e1');x=i*440;d.rectangle((x,0,x+440,990),fill=bg)
 for n,(id,title,desc,shapes) in enumerate(items):
  im=cache[id,theme].resize((56,56),Image.Resampling.LANCZOS);small.paste(im,(x+16,12+n*88),im)
  for j,t in enumerate(textwrap.wrap(title,30)):d.text((x+90,16+n*88+j*22),t,font=f,fill=ink)
small.save(O/'prova-56px.png');small.convert('L').save(O/'prova-cinza.png')
sections=[]
for mode,theme,bg,ink,gray,blue in palettes:
 cards=''.join(f'<article><div class="heading">{svg(shapes)}<h3>{title}</h3></div><p>{desc}</p></article>' for id,title,desc,shapes in items)
 sections.append(f'<section style="background:{bg};color:{ink};--traco:{gray};--tese-linha:{blue}"><h2>{mode} · {theme}</h2><div class="grid">{cards}</div></section>')
(O/'previa.html').write_text('''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Onze direitos — vinhetas</title><style>*{box-sizing:border-box}body{margin:0;font:18px/1.55 system-ui}header{padding:28px;max-width:1100px;margin:auto}section{padding:24px max(16px,calc((100vw - 1100px)/2))}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}article{padding:18px;border:1px solid currentColor}.heading{display:flex;gap:16px;align-items:center}.heading svg{width:56px;height:56px;flex-shrink:0}h3{font-size:19px;line-height:1.3}p{font-size:16px}@media(max-width:900px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:620px){.grid{grid-template-columns:1fr}}</style><header><h1>Os direitos, um por um</h1><p>Estudo com os títulos reais das páginas a–k. As descrições abaixo explicam as metáforas propostas; não substituem o texto jurídico do site. Os seis contextos são provas de cor.</p></header>'''+''.join(sections)+'</html>')
manifest=[]
for id,title,desc,shapes in items:
 a,b=cache[id,'claro'],cache[id,'escuro'];assert a.getchannel('A').tobytes()==b.getchannel('A').tobytes()
 for p in [O/f'{id}.webp',O/f'{id}-escuro.webp']:
  im=Image.open(p);assert im.size==(480,480) and im.mode=='RGBA';assert im.getpixel((0,0))[3]==0
 manifest.append({'id':id,'titulo':title,'descricao_da_metafora':desc,'fonte':f'https://lexplataformae.com.br/direitos/{id[-1]}/','alt':'','tamanho':[480,480],'alpha_identico':True})
(O/'manifesto.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(O/'LEIA-ME.md').write_text('''# Família 2 — nova direção, 16/11/2026

Onze vinhetas para os títulos reais dos direitos a–k, consultados em docs/direitos/index.html e nas onze páginas correspondentes. 22 WebPs transparentes de 480 × 480, qualidade 85; 22 mestres PNG e 11 SVGs. Cores planas, sem sombras nem escrita.

A ficha inicial foi corrigida onde divergia do texto: e agora mostra rastreabilidade; g, registro e contestação; h, repetição da perda num limite comum. f distingue equivalência funcional de identidade de aparência. Os desenhos a, c, d, i e j mantêm o sentido principal do planejamento; b e k foram simplificados para o tamanho de uso.

Alternativa vazia quando a vinheta apenas acompanha o título de navegação. A página atual utiliza direitos-indice com lista de links; os cartões da prévia são um estudo de leitura, não uma alteração implementada. Conferir o componente antes de inserir. Provas nos modos não significam repetição automática em todos eles.

Conferidos: dimensões, transparência dos WebPs, canais alfa iguais entre paletas, leitura visual a 56px e prova em cinza. Testes com leitores e integração permanecem pendentes. Estado: aguardando aprovação visual da família. Não publicar automaticamente.

Depois deste lote, restam 56 composições do planejamento principal: 29 acervo, 3 entradas e 24 problemas, equivalentes a 112 WebPs.
''')
with zipfile.ZipFile(O.parent/'familia-2-nova.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in O.iterdir():z.write(p,arcname=p.name)
print('Onze pares gerados e verificados.')
