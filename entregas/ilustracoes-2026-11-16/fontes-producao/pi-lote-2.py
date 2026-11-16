# coding: utf-8
from pathlib import Path
src=Path('work/linguagem-pi.py').read_text()
exec(src[:src.index('items=')].replace('linguagem-pi-lote-1','linguagem-pi-lote-2'))
def box(x,y,w,h,c='ink',sw=2):return line([(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)],c,sw)
def dash(points):
 out=[]
 for a,b in zip(points,points[1:]):
  length=math.dist(a,b)
  for start in range(0,int(length),16):
   end=min(start+9,length);out.append(line([(a[0]+(b[0]-a[0])*t/length,a[1]+(b[1]-a[1])*t/length) for t in (start,end)],'gray',2.5))
 return out
# Ornament: a repeated chevron appears on the surface and on its unfolded panel.
orn=transform(cylinder(),.80,0,14)
for y in [91,112,133]:orn.append(line([(57,y),(77,y+8),(97,y),(117,y+8),(137,y)],'gray',2))
orn += [line([(151,102),(202,102)],'gray',1.8),box(215,61,132,93),box(209,55,144,105,sw=2),box(203,49,156,117,sw=2)]
for y in [77,103,129]:orn.append(line([(225,y),(245,y+10),(265,y),(285,y+10),(305,y),(325,y+10),(337,y+4)],'gray',2))
orn+=flow()
# Mark: an abstract signal points to origin; no actual emblem, lettering or logo.
mark=transform(pyramid(),.83,2,13)+[line([(103,48),(103,30),(319,30),(319,89)],'gray',2),line([(313,81),(319,89),(325,81)],'gray',2),line(ellipse(319,105,13,13))]+flow()
# License: a blank tag changes the name, not the protected object's geometry.
lic=transform(cube()+protect(),.75,0,8)+dash([(26,21),(280,21),(280,226),(26,226),(26,21)])
lic += [line([(280,55),(305,55)],'gray',2),line([(305,55),(319,40),(364,40),(364,71),(319,71),(305,55)]),line(ellipse(320,55,3,3),w=1.5),poly([(174,205),(198,192),(264,192),(264,208),(202,208),(182,220)]),poly([(299,192),(362,192),(362,208),(299,208)])]
# Closure: preserve the exact protected form in both panels; remove the enclosure,
# and keep the continuous band. This is a proposed continuity relation, not an automatic outcome.
end=transform(cube()+protect(),.57,0,25)+transform(cube()+protect(),.57,208,25)
end+=dash([(15,30),(125,30),(125,156),(15,156),(15,30)])
end+=[poly([(88,179),(106,169),(177,169),(177,181),(109,181),(94,190)]),poly([(296,179),(314,169),(385,169),(385,181),(317,181),(302,190)])]
# Social purpose: results in succession instead of borrowing the origin arrow.
social=transform(cube()+protect(),.65,0,15)+transform(cube(),.34,178,40)+transform(cylinder(),.34,270,40)
social += [line([(211,142),(211,166),(311,166),(311,142)],'gray',2),line([(261,166),(261,184)],'gray',2)]+flow()
# Coexistence: four separate dimensions share a single band, with no overlay.
co=[]
for x,fn in [(0,cube),(96,sphere),(192,cylinder),(288,pyramid)]:co+=transform(fn(),.40,x,24)
co += [line([(48,112),(48,142),(336,142),(336,112)],'gray',2),line([(144,112),(144,142)],'gray',2),line([(240,112),(240,142)],'gray',2),line([(192,142),(192,174)],'gray',2),poly([(184,179),(200,169),(364,169),(364,185),(204,185),(192,194)])]
items=[
 ('pi-cilindro-superficie','Superfície e padrão',orn,'O mesmo padrão aparece na superfície curva e no plano aberto. O contorno duplo delimita o padrão examinado neste exemplo, sem declarar proteção de todo o objeto. Estudo visual; a hipótese jurídica e sua fonte serão especificadas na integração.'),
 ('pi-piramide-origem','Sinal e origem',mark,'A pirâmide se relaciona a um ponto de origem por uma seta fina. A faixa azul, larga e sem ponta, representa o uso. Esta peça ensina a relação de identificação, sem presumir a existência ou o alcance de um direito de marca.'),
 ('pi-licenca','O nome não muda a relação',lic,'A etiqueta vazia representa a denominação contratual, explicada aqui como licença. Ela se prende ao limite da plataforma. O contorno da proteção permanece igual, enquanto a faixa de uso aparece interrompida. A etiqueta não contém escrita.'),
 ('pi-encerramento','Preservar a continuidade',end,'À esquerda, o objeto protegido está dentro do limite tracejado da plataforma. À direita, o limite desaparece, mas o objeto e sua proteção permanecem. A faixa de uso continua nas duas situações. O desenho apresenta a continuidade a examinar, não uma solução técnica ou jurídica automática.'),
 ('pi-funcao-social','Proteção e resultados',social,'O objeto com contorno de proteção aparece ao lado de outras formas, agrupadas como resultados possíveis. A faixa de uso permanece contínua. A composição introduz a discussão da finalidade social; sua legenda editorial deverá explicitar a relação no caso tratado.'),
 ('pi-convivencia','Dimensões do mesmo objeto',co,'Cubo, esfera, cilindro e pirâmide ficam separados, ligados a uma mesma faixa de uso. Representam dimensões de um objeto comum. A ausência de contornos de proteção nesta introdução evita presumir que todos os regimes incidem automaticamente.')]
tail=src[src.index('P='):]
tail=tail.replace('linguagem-pi-lote-1','linguagem-pi-lote-2').replace('primeiro lote','segundo lote').replace('— lote 1','— lote 2').replace('Quatro dimensões, uma linguagem comum.','As dimensões em relação.')
tail=tail.replace('Seis estudos; aprovação anterior refere-se ao protótipo de exclusividade e controle do uso. Este lote apresenta as quatro convenções e duas primeiras relações. Não publicado.','Seis estudos complementares ao primeiro lote aprovado. Não publicado. Encerramento deve ser lido em sequência da esquerda para a direita; a legenda descreve os dois estados.')
tail=tail.replace('O nome histórico pi-papel-dominio-publico foi preservado para rastreabilidade; a composição agora se chama Uma exclusividade delimitada e o fundo não significa domínio público.','As peças de superfície e de origem ensinam relações sem afirmar que todo padrão ou sinal é juridicamente protegido. A composição de convivência representa dimensões do objeto, não equivalências entre sólidos e regimes jurídicos.')
exec(tail)
