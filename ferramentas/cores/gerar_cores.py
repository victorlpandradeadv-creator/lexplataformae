"""Calcula a proposta de cores e grava estrutura/cores.json. Imprime contraste e separação sob daltonismo."""
import itertools, json, math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
RAIZ = Path(__file__).resolve().parents[2]
from cor import *
AREAS = {  # destaque (L,C,h), texto claro, texto escuro
 'direito':      ('Direito',                 (0.54,0.21,27),  (0.42,0.13,27),  (0.84,0.07,27)),
 'economia':     ('Economia política',       (0.82,0.15,72),  (0.43,0.08,65),  (0.86,0.07,75)),
 'tecnica':      ('Técnica e mídia',         (0.74,0.10,195), (0.42,0.06,200), (0.85,0.05,195)),
 'antropologia': ('Antropologia do consumo', (0.66,0.12,128), (0.40,0.06,130), (0.85,0.06,128)),
 'semiotica':    ('Semiótica e linguagem',   (0.54,0.16,300), (0.40,0.10,300), (0.83,0.07,300)),
 'poder':        ('Poder e subjetividade',   (0.52,0.17,345), (0.38,0.10,345), (0.84,0.06,345)),
 'laboratorio':  ('Objeto e laboratório',    (0.88,0.01,80),  (0.38,0.008,80), (0.84,0.005,80)),
}
TESE = dict(nome='A tese', chapado='#002fa7', sobre_chapado='#ffffff', texto='#002fa7', texto_escuro=(0.80,0.09,265), marca_escuro=(0.62,0.19,264))
TELAS = {
 'orientacao': {'claro': dict(papel=(0.975,0.010,85), folha=(0.99,0.005,85), tinta=(0.23,0.012,60), tinta2=(0.47,0.015,60), linha=(0.88,0.012,80)),
              'escuro':dict(papel=(0.19,0.010,60), folha=(0.22,0.010,60), tinta=(0.93,0.010,80), tinta2=(0.72,0.012,75), linha=(0.32,0.01,60))},
 'doutrina':{'claro': dict(papel=(0.968,0.007,240), folha=(0.99,0.003,240), tinta=(0.22,0.015,255), tinta2=(0.47,0.02,255), linha=(0.87,0.01,245)),
              'escuro':dict(papel=(0.215,0.02,252), folha=(0.245,0.02,252), tinta=(0.93,0.008,250), tinta2=(0.74,0.015,250), linha=(0.35,0.02,252))},
 'ciencia':   {'claro': dict(papel=(0.985,0.004,230), folha=(1.0,0,0), tinta=(0.20,0.01,250), tinta2=(0.46,0.012,250), linha=(0.88,0.01,240), traco=(0.45,0.01,250), grade=(0.91,0.02,230)),
              'escuro':dict(papel=(0.19,0.004,250), folha=(0.22,0.004,250), tinta=(0.94,0.005,250), tinta2=(0.75,0.01,250), linha=(0.34,0.008,250), traco=(0.80,0.012,250), grade=(0.245,0.006,250))},
 'ficha':    {'claro': dict(papel=(0.965,0.028,92), tinta=(0.24,0.015,60), tinta2=(0.46,0.02,60), pauta=(0.86,0.035,235)),
              'escuro':dict(papel=(0.26,0.018,80), tinta=(0.93,0.02,88), tinta2=(0.74,0.02,85), pauta=(0.36,0.03,235))},
}
MARCA = {'claro':(0.93,0.075,105), 'escuro':(0.42,0.07,100)}
def mistura(a,b,t):
    A=lin_to_oklab(*lin_hex(a)); B=lin_to_oklab(*lin_hex(b))
    L,aa,bb=[A[i]*(1-t)+B[i]*t for i in range(3)]
    return hexa(tuple(min(1,max(0,x)) for x in oklab_to_lin(L,aa,bb)))
out = {'descricao':'Proposta de cores do Claude, de 27/10/2026, para decisão do autor. Nada aplicado ao site. Valores em hexadecimal calculados a partir de OKLCH, guardados em fonte_oklch.', 'areas':{}, 'telas':{}, 'marca':{m:cor(*v) for m,v in MARCA.items()}, 'fonte_oklch':{'areas':{k:{'destaque':v[1],'texto':v[2],'texto_escuro':v[3]} for k,v in AREAS.items()}, 'telas':TELAS, 'marca':MARCA}}
for t,md in TELAS.items():
    out['telas'][t] = {m:{k:cor(*v) for k,v in d.items()} for m,d in md.items()}
for k,(nome,d,tc,te) in AREAS.items():
    dc = cor(*d)
    # destaque para fundo escuro: sobe a luminosidade até 3:1 sobre o papel escuro mais claro
    L,C,h = d; de = dc
    while min(contraste(de, out['telas'][t]['escuro']['papel']) for t in TELAS) < 3.0 and L < 0.95:
        L += 0.01; de = cor(L,C,h)
    out['areas'][k] = dict(nome=nome, destaque=dc, destaque_escuro=de, texto=cor(*tc), texto_escuro=cor(*te),
        fundo=mistura(cor(0.985,0,0), dc, 0.16),
        fundo_escuro=mistura(cor(0.25,0,0), de, 0.24))
out['tese'] = dict(nome='A tese', chapado=TESE['chapado'], sobre_chapado=TESE['sobre_chapado'], texto=TESE['texto'], texto_escuro=cor(*TESE['texto_escuro']), marca_escuro=cor(*TESE['marca_escuro']), referencia='International Klein Blue, aproximação em tela')
json.dump(out, open(RAIZ / 'estrutura' / 'cores.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
# relatório
for k,v in out['areas'].items():
    print(f"{k:13}", v['destaque'], v['destaque_escuro'], v['texto'], v['texto_escuro'], v['fundo'], v['fundo_escuro'],
      f"texto/fundo {contraste(v['texto'],v['fundo']):.1f} textoE/fundoE {contraste(v['texto_escuro'],v['fundo_escuro']):.1f}",
      'min texto claro', round(min(contraste(v['texto'],out['telas'][t]['claro']['papel']) for t in TELAS),1),
      'min texto escuro', round(min(contraste(v['texto_escuro'],out['telas'][t]['escuro']['papel']) for t in TELAS),1))
for t in out['telas']:
    for m,d in out['telas'][t].items():
        print(t,m,d, 'tinta', round(contraste(d['tinta'],d['papel']),1), 'tinta2', round(contraste(d['tinta2'],d['papel']),1))
t=out['tese']; print('tese', t, 'branco/IKB', round(contraste('#ffffff',t['chapado']),1), 'IKB/papel claro', round(min(contraste(t['texto'], out['telas'][x]['claro']['papel']) for x in out['telas']),1), 'texto escuro', round(min(contraste(t['texto_escuro'], out['telas'][x]['escuro']['papel']) for x in out['telas']),1), 'marca escuro', round(min(contraste(t['marca_escuro'], out['telas'][x]['escuro']['papel']) for x in out['telas']),1))
print('marca', out['marca'], 'tinta sobre marca', round(contraste(out['telas']['doutrina']['claro']['tinta'], out['marca']['claro']),1), round(contraste(out['telas']['doutrina']['escuro']['tinta'], out['marca']['escuro']),1))
print('marca x economia', round(dist(out['marca']['claro'], out['areas']['economia']['destaque']),1), 'deutan', round(dist(simular(out['marca']['claro'],'deutan'), simular(out['areas']['economia']['destaque'],'deutan')),1))
for modo,chave in (('claro','destaque'),('escuro','destaque_escuro')):
    for s in ('normal','protan','deutan','tritan'):
        sims={k:simular(v[chave],s) for k,v in out['areas'].items()}; sims['tese']=simular(out['tese']['chapado'] if modo=='claro' else out['tese']['marca_escuro'], s)
        pares=sorted((dist(sims[a],sims[b]),a,b) for a,b in itertools.combinations(sims,2))
        print(modo, s, ' '.join(f"{a}-{b}:{d:.1f}" for d,a,b in pares[:3]))
