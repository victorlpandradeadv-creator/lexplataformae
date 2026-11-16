# coding: utf-8
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,zipfile
O=Path('outputs/linguagem-pi-armadura-v2')
for p in O.glob('pi-*.png'):
 im=Image.open(p).convert('RGBA');assert im.size==(2400,1800),im.size
 im=im.resize((1200,900),Image.Resampling.LANCZOS);im.save(p);im.save(p.with_suffix('.webp'),lossless=True)
checks=[]
for id in ['pi-skin-objeto','pi-skin-dimensoes','pi-skin-controle']:
 a=Image.open(O/f'{id}-claro.png');b=Image.open(O/f'{id}-escuro.png');equal=a.getchannel('A').tobytes()==b.getchannel('A').tobytes();assert equal;assert a.getpixel((0,0))[3]==0
 checks.append({'peca':id,'dimensoes':[1200,900],'alfa_identico':equal,'fundo_transparente':True})
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',24)
for mode,bgs,inks in [('informacao',['#faf6ef','#17130f'],['#211c17','#ebe7e1']),('doutrina',['#f0f5f9','#131a23'],['#161b22','#e4e8ed']),('ciencia',['#f7fbfc','#121416'],['#13161a','#e9ebee'])]:
 sheet=Image.new('RGB',(1600,1980));d=ImageDraw.Draw(sheet)
 for i,theme in enumerate(['claro','escuro']):
  x=i*800;d.rectangle((x,0,x+800,1980),fill=bgs[i]);d.text((x+24,18),mode.capitalize()+' · '+theme,font=font,fill=inks[i])
  for n,(id,title) in enumerate([('pi-skin-objeto','A armadura como objeto'),('pi-skin-dimensoes','Dimensões separadas'),('pi-skin-controle','Proteção e controle do uso')]):
   im=Image.open(O/f'{id}-{theme}.png').resize((800,600),Image.Resampling.LANCZOS);sheet.paste(im,(x,50+n*640),im);d.text((x+24,620+n*640),title,font=font,fill=inks[i])
 sheet.save(O/f'prancha-{mode}.png')
(O/'conferencia.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
(O/'LEIA-ME.md').write_text('''# Armadura — versão 2, cores planas

Substitui o estudo anterior. Uma única matriz clara é usada nos dois temas. A segunda imagem generativa foi descartada desta entrega.

A composição SVG usa uma classificação de cor em duas tintas e um recorte comum de opacidade. Esse tratamento remove gradientes, sombras e resíduos de transparência externa. As cores são #211c17 e #002fa7 no claro, #ebe7e1 e #497ef7 no escuro. O mesmo recorte é aplicado às duas versões; não há regeneração de pose ou contornos entre temas.

Exportação pelo navegador em resolução dupla e redução para 1200 × 900. PNG e WebP com transparência. A comparação dos canais alfa dos três pares é exatamente igual, registrada em conferencia.json. Os diagramas mantêm as coordenadas aprovadas. Pranchas são apenas provas sobre fundos; os arquivos individuais não têm fundo nem texto visível.

A matriz da armadura foi produzida pelo gerador integrado a partir da referência canônica do repositório, conforme prompt registrado na entrega anterior. O tratamento final é aplicado no SVG. A transparência foi conferida e as pranchas inspecionadas. A página continua local, sem publicação; teste com leitores e integração ao site permanecem pendentes.
''')
with zipfile.ZipFile(O.parent/'linguagem-pi-armadura-v2.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in O.iterdir():z.write(p,arcname=p.name)
print(checks)
