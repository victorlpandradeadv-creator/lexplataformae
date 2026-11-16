# coding: utf-8
from pathlib import Path
src=Path('work/linguagem-pi.py').read_text()
exec(src[:src.index('items=')].replace('linguagem-pi-lote-1','linguagem-pi-lote-3'))
def dash(points):
 out=[]
 for a,b in zip(points,points[1:]):
  length=math.dist(a,b)
  for start in range(0,int(length),16):
   end=min(start+9,length);out.append(line([(a[0]+(b[0]-a[0])*t/length,a[1]+(b[1]-a[1])*t/length) for t in (start,end)],'gray',2.5))
 return out
four=[]
for x,fn in [(0,cube),(96,sphere),(192,cylinder),(288,pyramid)]:
 four+=transform(fn(),.4,x,45)+[poly([(x+26,151),(x+37,144),(x+83,144),(x+83,154),(x+40,154),(x+31,160)])]
def gear(cx,cy,r):
 pts=[]
 for i in range(64):
  a=i*2*math.pi/64;rr=r if i%8 in [1,2,3,4] else r*.79;pts.append((cx+rr*math.cos(a),cy+rr*math.sin(a)))
 return [line(pts+[pts[0]],w=2),line(ellipse(cx,cy,r*.29,r*.29),w=2)]
technical=transform(sphere(),.65,0,32)+[line(ellipse(290,110,60,60)),line(ellipse(290,110,22,60),'gray',1.5)]
technical+=gear(272,105,24)+gear(313,123,20)
technical+=[poly([(82,205),(106,192),(362,192),(362,208),(110,208),(90,220)])]
# The protected scope remains fixed; only the platform boundary expands.
excess=transform(cube()+protect(),.65,0,18)+transform(sphere(),.36,227,16)+transform(cylinder(),.36,227,92)+flow()
excess+=dash([(14,22),(158,22),(158,170),(14,170),(14,22)])
excess+=dash([(5,12),(370,12),(370,233),(5,233),(5,12)])
# Construction of a boundary is a two-stage comparison, avoiding a hand as a new symbol.
scarcity=transform(cube(),.58,0,31)+transform(cube()+protect(),.58,205,31)
for x in [0,205]:scarcity += [poly([(x+83,186),(x+102,175),(x+184,175),(x+184,188),(x+107,188),(x+90,197)])]
items=[('pi-quatro-solidos','Quatro dimensões',four,'Da esquerda para a direita: cubo para expressão, esfera para solução técnica, cilindro para ornamento e pirâmide para distintividade. Cada dimensão acompanha uma faixa de uso. As formas são convenções e não equivalem automaticamente a direitos.'),('pi-esfera-tecnica','O funcionamento por dentro',technical,'A esfera inteira aparece à esquerda. À direita, a organização interna é exposta por duas engrenagens. Não há contorno de incidência: o desenho apresenta funcionamento, sem presumir proteção jurídica do mecanismo.'),('pi-latifundio','Controle além do recorte',excess,'O contorno duplo da exclusividade permanece rente ao cubo. Dois limites tracejados mostram a ampliação do controle da plataforma, até envolver outras dimensões e o uso. O contorno da proteção não se transforma em controle: são elementos distintos.'),('pi-escassez','A delimitação é acrescentada',scarcity,'Primeiro, o cubo aparece sem contorno de incidência; depois, o mesmo cubo recebe um contorno duplo. O uso permanece contínuo. A sequência representa a construção de uma delimitação, sem afirmar ausência de outras proteções na primeira situação.')]
tail=src[src.index('P='):].replace('linguagem-pi-lote-1','linguagem-pi-lote-3').replace('primeiro lote','terceiro lote').replace('— lote 1','— lote 3').replace('(1600,1050)','(1600,720)').replace('offset+800,1050','offset+800,720').replace('Quatro dimensões, uma linguagem comum.','Aprender a ler as relações.')
tail=tail[:tail.index("(O/'LEIA-ME.md')")]
exec(tail)
(O/'LEIA-ME.md').write_text('''# Linguagem geométrica — lote 3

Quatro estudos e uma página explicativa. As imagens são transparentes, sem texto visível. Pranchas e página contêm títulos externos aos desenhos. As versões claras e escuras usam a mesma geometria. Não publicado.

Ajustes de composição: esfera técnica sem contorno de proteção presumida; latifúndio distingue proteção fixa de expansão do controle; escassez mostra a adição do contorno em duas etapas, substituindo a mão por comparação direta. A prancha reúne quatro dimensões; a página nomeia cada uma separadamente.

SVGs destinam-se à inserção direta no HTML, com as descrições externas equivalentes. PNGs e WebPs transparentes são provas de 1200 × 780. A página é uma proposta editorial local, ainda sem integração ao gerador do site.

Pendente para a etapa seguinte: sequência da armadura canônica, ensaio com leitores, conferência das fontes jurídicas e integração. As aprovações visuais não substituem o ensaio de compreensão.
''')
# A standalone teaching page, without controls required to access explanations.
base=(O/'previa.html').read_text(); style=base[base.index('<style>'):base.index('</style>')+8]
style=style.replace('</style>','table{border-collapse:collapse;width:100%;font-size:16px}td,th{text-align:left;padding:14px 10px;border-bottom:1px solid #aaa;vertical-align:top}.lesson{max-width:1050px;margin:auto;padding:24px} .lesson svg{max-width:600px} @media(prefers-color-scheme:dark){body{background:#121416;color:#e9ebee;--traco:#b8bec5;--tese-linha:#497ef7}} </style>')
lessons=''
for id,title,s,desc in items:
 lessons+=f'<article class="lesson"><h2>{title}</h2><figure>{svg(s)}<figcaption>{desc}</figcaption></figure></article>'
body='''<header><p>LEX PLATAFORMAE · CIÊNCIA</p><h1>Como ler a linguagem geométrica</h1><p>Proposta de acréscimo autoral, datada de 15 de novembro de 2026. As formas abaixo são convenções de explicação. Não são uma classificação geométrica proposta pela tese.</p><p>Comece por uma distinção: a dimensão de um objeto, o alcance de uma exclusividade e o controle exercido pela plataforma são coisas diferentes.</p></header><div class="lesson"><h2>As quatro formas</h2><table><tr><th>Forma</th><th>Dimensão representada</th></tr><tr><td>Cubo</td><td>Expressão</td></tr><tr><td>Esfera</td><td>Solução técnica</td></tr><tr><td>Cilindro</td><td>Ornamento</td></tr><tr><td>Pirâmide</td><td>Distintividade</td></tr></table><p>Reconhecer uma forma não permite concluir que exista proteção jurídica. A incidência de um direito depende do caso e de seus requisitos.</p><h2>Linhas que dizem coisas diferentes</h2><table><tr><th>Elemento</th><th>Leitura</th></tr><tr><td>Contorno duplo</td><td>Alcance da exclusividade examinada naquele exemplo.</td></tr><tr><td>Limite tracejado</td><td>Controle contratual ou técnico da plataforma.</td></tr><tr><td>Faixa larga sem ponta</td><td>Uso ou resultado funcional. Uma lacuna indica interrupção.</td></tr><tr><td>Seta fina com ponta</td><td>Relação de identificação de origem.</td></tr><tr><td>Fundo da página</td><td>Espaço neutro. Não significa automaticamente domínio público.</td></tr></table></div>'''
prototype=Path('outputs/prototipo-pi/pi-uso-interrompido.svg').read_text()
body+='''<article class="lesson"><h2>Um exemplo de leitura</h2><figure>'''+prototype+'''<figcaption>O cubo mantém seu contorno duplo. O limite tracejado da plataforma cruza a faixa do uso, que aparece interrompida. A imagem distingue a proteção do objeto do controle sobre seu uso.</figcaption></figure></article>'''+lessons+'''<footer><h2>O que ainda precisa ser testado</h2><p>Depois desta apresentação, o leitor consegue distinguir proteção e controle? Consegue identificar o uso interrompido sem depender da cor? Reconhece que estar fora de um contorno não significa ausência de qualquer proteção?</p><p>Essas perguntas orientam um ensaio com pessoas. A aprovação visual e a revisão por IA não equivalem a esse ensaio. A conferência das fontes jurídicas antecede a publicação dos exemplos no site.</p></footer>'''
(O/'linguagem-geometrica.html').write_text('<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Como ler a linguagem geométrica</title>'+style+body+'</html>')
with zipfile.ZipFile(O.parent/'linguagem-pi-lote-3.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in O.iterdir():z.write(p,arcname=p.name)
print('Quatro peças, seis contextos de cor e página explicativa gerados.')
