# Sólidos da propriedade intelectual

Composições das peças em SVG de `estrutura/ilustracoes-pi.md`, lidas por `ferramentas/solidos.py`. Rascunho do Claude de 15/11/2026. É planejamento, e nada daqui está no site. O lugar, o objetivo e a âncora de cada peça ficam no plano. Aqui ficam só o desenho, o título e o texto alternativo.

Formato de cada entrada.

- `## <id>` abre a entrada, com o mesmo id do plano.
- `### lugar` repete o lugar do plano. Não vai ao site.
- `### titulo` é o título para leitor de tela.
- `### alt` é o texto alternativo do plano.
- `### desenho` traz uma ação por linha. As coordenadas são de tela, em pixels, e o centro da base do sólido é o ponto dado.

Ações do desenho.

- `solido <cubo|esfera|cilindro|piramide> <nome> <x> <y> [tam n] [transparente]`
- `contorno <alvo> [aneis n]`, linha dupla rente ao alvo. O alvo pode somar partes com `+`, como `C+C.pele`.
- `fluxo <nome> <dx> <dy> [comprimento n] [corta]`, faixa azul que sai do sólido na direção dada. Com `corta`, o tracejado da peça interrompe o fluxo.
- `tracejado <alvo> [margem n] [desfeito]`, poder da plataforma sobre a fruição.
- `vetor <nome> <x> <y> [contorno]`, linha fina com ponta que sai do vértice até a origem.
- `vetorlargo <x0> <y0> <x1> <y1> [largura n]`, a direção da exclusividade.
- `formacao <tipo> <x> <y> [tam n]`, sólido em formação, só em tracejado.
- `corte <esfera>`, `padrao <cilindro>`, `pele <cilindro> <x> <y>`, `sinal <piramide>` e `base <piramide>`.
- `etiqueta <x> <y> <texto>`, `ponte <nome> <x> <y>`, `rotulo <nome ou x,y> <texto>` e `linha <x0> <y0> <x1> <y1>`.

## pi-quatro-solidos

### lugar
Doutrina, capítulo Propriedade intelectual, depois do título Por que a propriedade intelectual da plataforma não é um bloco único?

### titulo
Quatro dimensões do objeto

### alt
Cubo, esfera, cilindro e pirâmide lado a lado, cada um com o nome da dimensão que representa.

### desenho
- solido cubo A 0 0
- solido esfera B 190 0
- solido cilindro C 380 0
- solido piramide D 570 0
- fluxo A 1 -0.9 comprimento 60
- fluxo B 1 -0.9 comprimento 60
- fluxo C 1 -0.9 comprimento 60
- fluxo D 1 -0.9 comprimento 60
- rotulo A expressão
- rotulo B solução técnica
- rotulo C ornamento
- rotulo D sinal distintivo

## pi-papel-dominio-publico

### lugar
Doutrina, capítulo Propriedade intelectual, depois do título Por que a questão não é ser contra ou a favor da propriedade intelectual?

### titulo
A exclusividade é um recorte no domínio público

### alt
Muitos sólidos soltos sobre o papel, com um só deles envolvido por um contorno duplo justo.

### desenho
- solido cubo a1 0 0 tam 30
- solido esfera a2 90 -30 tam 30
- solido piramide a3 170 10 tam 30
- solido cilindro a4 260 -20 tam 30
- solido esfera a5 350 15 tam 30
- solido piramide a6 30 90 tam 30
- solido cilindro a7 120 70 tam 30
- solido cubo X 215 95 tam 34
- solido esfera a9 300 85 tam 30
- solido cubo a10 380 100 tam 30
- solido cilindro a11 -40 50 tam 30
- solido piramide a12 440 40 tam 30
- contorno X
- rotulo 200,170 o papel é o domínio público

## pi-cubo-software

### lugar
Doutrina, capítulo Propriedade intelectual, depois do título O que a proteção do software autoriza e o que ela não autoriza?

### titulo
O código protegido, o método e o resultado fora do contorno

### alt
Cubo com contorno de proteção e, fora do contorno, uma esfera e um elemento azul.

### desenho
- solido cubo A 0 0 tam 70
- contorno A
- solido esfera M 120 -60 tam 34
- fluxo A 1 0.35 comprimento 120
- rotulo A código
- rotulo M método
- rotulo 175,85 resultado

## pi-esfera-tecnica

### lugar
Ciência, página da linguagem geométrica, na apresentação da esfera.

### titulo
A esfera se lê pelo que está dentro

### alt
Esfera inteira e a mesma esfera em corte, com o contorno de proteção só em volta do mecanismo interno.

### desenho
- solido esfera A 0 0 tam 100
- solido esfera B 200 0 tam 100
- corte B
- contorno B.mecanismo

## pi-cilindro-ornamento

### lugar
Doutrina, capítulo Propriedade intelectual, depois do título Por que a marca e o desenho industrial importam do lado do consumidor?

### titulo
A forma e o padrão, as duas faces do ornamento

### alt
Cilindro com padrão na superfície e, ao lado, a mesma superfície desenrolada, as duas com contorno de proteção.

### desenho
- solido cilindro C 0 0 tam 70
- padrao C
- pele C 80 35
- contorno C
- contorno C.pele

## pi-piramide-marca

### lugar
Doutrina, capítulo Propriedade intelectual, depois de pi-cilindro-ornamento.

### titulo
A marca protege a aptidão do sinal para apontar a origem

### alt
Pirâmide com um sinal na base e um vetor do vértice até a origem, com o contorno de proteção só nesses dois elementos.

### desenho
- solido piramide D 0 0 tam 80
- sinal D
- base D
- contorno D.base
- vetor D 150 -150 contorno
- rotulo 165,-125 origem

## pi-exclusividade-e-poder

### lugar
Doutrina, capítulo Propriedade intelectual, depois do título Onde está, afinal, a tensão entre exclusividade e proteção do consumidor?

### titulo
A mesma exclusividade, com e sem poder sobre a fruição

### alt
O mesmo sólido protegido duas vezes. Na primeira, o fluxo azul do uso sai livre. Na segunda, um tracejado cinza fecha e corta o fluxo.

### desenho
- solido cubo A 0 0
- contorno A
- fluxo A 1 0.25 comprimento 120
- linha 190 -110 190 90
- solido cubo B 290 0
- contorno B
- fluxo B 1 0.25 comprimento 120 corta
- tracejado B margem 46

## pi-licenca

### lugar
Doutrina, capítulo Propriedade intelectual, depois do título Chamar o vínculo de licença afasta o CDC?

### titulo
O nome licença não muda o desenho

### alt
O mesmo desenho da exclusividade e do poder da plataforma, com uma etiqueta de licença presa ao tracejado que não muda nada no resto.

### desenho
- solido cubo B 0 0
- contorno B
- fluxo B 1 0.25 comprimento 120 corta
- tracejado B margem 46
- etiqueta 40 -108 licença

## pi-funcao-social

### lugar
Doutrina, capítulo Propriedade intelectual, depois do título O que o art. 5º, XXIX, da Constituição exige da exclusividade?

### titulo
A exclusividade tem direção

### alt
Sólido protegido com um vetor que sai do contorno em direção a outros sólidos em formação no papel.

### desenho
- solido cubo A 0 0
- contorno A
- vetorlargo 62 -30 210 -30 largura 18
- formacao cubo 260 -10
- formacao esfera 320 -40
- formacao piramide 330 30
- fluxo A 0.5 1 comprimento 90

## pi-latifundio

### lugar
Ciência, página da linguagem geométrica, como contraexemplo.

### titulo
O contorno que cresce além do que protege

### alt
Sólido pequeno com o contorno de proteção inchado em anéis que cobrem outros sólidos à volta.

### desenho
- solido cubo A 0 0 tam 36
- contorno A aneis 4
- solido esfera b1 -95 -35 tam 26
- solido piramide b2 90 -55 tam 26
- solido cilindro b3 100 60 tam 26
- solido piramide b4 -90 70 tam 26
- fluxo A 1 0.4 comprimento 70

## pi-encerramento

### lugar
Doutrina, capítulo Propriedade intelectual, depois do título O que acontece quando o serviço é encerrado?

### titulo
O serviço acaba, a fruição tem passagem

### alt
Sólido protegido que continua com o contorno, enquanto o tracejado da plataforma se desfaz e o fluxo azul do uso permanece no papel.

### desenho
- solido cubo A 0 0
- contorno A
- tracejado A margem 46 desfeito
- fluxo A 1 0.25 comprimento 120
- ponte A 250 60

## pi-convivencia

### lugar
Doutrina, capítulo Propriedade intelectual, depois do título Como o CDC e a propriedade intelectual convivem no exame do caso?

### titulo
Os regimes incidem juntos sem perder a autonomia

### alt
Quatro sólidos sobrepostos em transparência, cada um com contorno próprio, com um só fluxo azul saindo do conjunto.

### desenho
- solido cubo A 0 0 tam 64 transparente
- solido esfera B 80 -40 tam 58 transparente
- solido cilindro C 30 60 tam 54 transparente
- solido piramide D 115 35 tam 60 transparente
- contorno A
- contorno B
- contorno C
- contorno D
- fluxo D 1 0.3 comprimento 110
