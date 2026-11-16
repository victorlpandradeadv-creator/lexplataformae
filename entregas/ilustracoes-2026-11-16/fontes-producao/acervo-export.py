# coding: utf-8
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,zipfile
O=Path('outputs/familia-3-lote-1');items=json.loads((O/'manifesto.json').read_text());checks=[]
for it in items:
 for suffix in ['','-escuro']:
  p=O/(it['id']+suffix+'.png');im=Image.open(p).convert('RGBA');assert im.size in [(it['largura']*2,1800),(it['largura'],900)]
  im=im.resize((it['largura'],900),Image.Resampling.LANCZOS);im.save(p);im.save(p.with_suffix('.webp'),quality=82,method=4)
 a=Image.open(O/(it['id']+'.png'));b=Image.open(O/(it['id']+'-escuro.png'));assert a.getchannel('A').tobytes()==b.getchannel('A').tobytes();assert a.getpixel((0,0))[3]==0
 checks.append({'id':it['id'],'tamanho':list(a.size),'alpha_identico':True})
f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',19)
for name,bgs,inks in [('informacao',['#faf6ef','#17130f'],['#211c17','#ebe7e1']),('doutrina',['#f0f5f9','#131a23'],['#161b22','#e4e8ed']),('ciencia',['#f7fbfc','#121416'],['#13161a','#e9ebee'])]:
 sheet=Image.new('RGB',(1440,2340));d=ImageDraw.Draw(sheet)
 for i,suffix in enumerate(['','-escuro']):
  x=i*720;d.rectangle((x,0,x+720,2340),fill=bgs[i]);d.text((x+24,16),name.capitalize()+' · '+('claro' if i==0 else 'escuro'),font=f,fill=inks[i])
  for n,it in enumerate(items):
   im=Image.open(O/(it['id']+suffix+'.png'));im.thumbnail((680,310),Image.Resampling.LANCZOS);sheet.paste(im,(x+(720-im.width)//2,55+n*380),im);d.text((x+24,365+n*380),it['titulo'],font=f,fill=inks[i])
 sheet.save(O/f'prancha-{name}.png')
small=Image.new('RGB',(680,1090),'#faf6ef');d=ImageDraw.Draw(small)
for n,it in enumerate(items):
 im=Image.open(O/(it['id']+'.png'));h=round(320*900/im.width);im=im.resize((320,h),Image.Resampling.LANCZOS);x=10+(n%2)*340;y=20+(n//2)*350;small.paste(im,(x,y),im)
 for j,line in enumerate(__import__('textwrap').wrap(it['titulo'],30)):d.text((x,y+245+j*24),line,font=f,fill='#211c17')
small.save(O/'prova-320px.png');small.convert('L').save(O/'prova-cinza.png')
(O/'conferencia.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
(O/'LEIA-ME.md').write_text('''# Família 3 — grupo inicial, 16/11/2026

Seis das 29 composições do acervo: inicio, imagem-catraca, imagem-estoque-fluxo, parte-a-mudanca, ideia-equivalencia-de-valor-funcional e ideia-feixe-de-fruicao-governada. Grupo coerente sobre sustentação e uso. A família não está concluída; aprovação final requer visão do conjunto.

Armadura reutilizada da matriz aprovada, sem alteração de identidade, pose ou proporções. Paletas aplicadas ao mesmo desenho; sem sombra, brilho, solo ou cenário opaco. Relações desenhadas em SVG editável; imagem da armadura compartilhada em matriz-armadura.png, necessária ao abrir os SVGs. PNGs e WebPs são autossuficientes.

Entregas: aberturas 1600 × 900, internas 1200 × 900; WebP com alpha, qualidade 82. Mestres PNG, SVGs, manifestos com descrições alternativas, prévia e pranchas. Provas a 320px e em cinza. Não há texto visível dentro da arte. As legendas da prancha não são parte dos arquivos individuais.

Conferidos canais alfa idênticos entre os temas, dimensões e transparência. Inspeção visual do grupo e das provas. Teste de compreensão por leitores ainda pendente. Não altera o site. As posições de integração devem seguir o componente que já consome cada identificador, sem duplicação automática entre modos.

Estado: aguardando aprovação visual deste grupo. Restam 23 peças da Família 3, 3 da Família 4 e 24 da Família 5: 50 composições / 100 versões.
''')
with zipfile.ZipFile(O.parent/'familia-3-lote-1.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in O.iterdir():z.write(p,arcname=p.name)
print('Seis pares exportados e conferidos.')
