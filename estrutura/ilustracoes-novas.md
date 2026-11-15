# Ilustrações novas, versão 0.17

Rascunho do Claude de 15/11/2026, por ordem do autor, refeito no mesmo dia para ficar pronto para execução. É planejamento, e nada daqui está no site. As peças seguem a direção de arte de `estrutura/ilustracoes.md` e acrescentam as regras abaixo. Quando o autor aprovar, cada peça passa para `estrutura/ilustracoes.md` no mesmo formato de campos, e o gerador a lê de lá.

Os trechos citados aqui passam pelo script, com `python3 ferramentas/conferir_citacoes.py estrutura/ilustracoes-novas.md`.

# 1. Leitura das seções iniciais

Na versão 0.17, quem chega pela rede social não entra mais pela história da skin. Entra pela pergunta O que uma plataforma tirou de você? e escolhe entre seis portas. As páginas dos três primeiros cliques são a capa, a lista de problemas, a página do problema, Seus direitos, Como reclamar e Além do consumo. Nenhuma tem ilustração própria. A capa só guarda a peça inicio, da armadura, que é da história da skin e não responde à pergunta do alto.

A capa pede reconhecimento, e não explicação. A pessoa precisa achar a própria perda em poucos segundos, e as seis portas hoje são só texto, com títulos de mesmo peso. No celular formam uma coluna longa em que nada distingue uma porta da outra antes da leitura. Uma marca visual por porta acelera a escolha e dá à capa a cara de aplicativo pedida em 11/11/2026.

Uma imagem grande no alto da capa atrapalharia, porque no celular empurraria as portas para baixo da primeira tela. Por isso a capa da Informação não ganha imagem de abertura, e a peça inicio sai dela.

A página do problema é a que circula, porque é o link que alguém manda a um amigo. Ela abre por título-pergunta e texto denso, sem âncora visual, e o cartão de compartilhamento é só tipográfico. Uma abertura nos problemas mais procurados serve à página e ao cartão.

Seus direitos e Além do consumo carregam viradas abstratas, a de que a venda não termina no clique e a de que a proteção continua fora do consumo. Uma imagem no alto fixa a virada antes da lista.

Como reclamar já tem o esquema I6, que organiza os quatro caminhos melhor que uma figura. A Doutrina, as Situações, as fichas e a Ciência também não recebem peças, porque ali o esquema ou o texto cumpre o papel.

# 2. Regras de execução

## 2.1 Duas famílias

As aberturas seguem a família atual, de cena editorial com linha fina, volumes chapados, figuras sem rosto e muito espaço vazio.

As vinhetas das portas são uma família nova, de objeto único. Sem pessoa, sem cenário, sem chão desenhado, sem sombra projetada. Linha de espessura uniforme, cantos arredondados, no máximo três massas de cor. Precisam ser legíveis a 56 pixels e bonitas a 160.

## 2.2 Paleta, clara e escura

A versão escura é desenhada, e não calculada nem filtrada. Sai da mesma composição, na mesma encomenda, com as cores trocadas pela tabela abaixo.

| papel na peça | clara | escura |
|---|---|---|
| fundo | #faf6ef | #17130f |
| fundo um tom acima, para massas grandes | #f1ebe1 | #241f1a |
| tinta, traço principal | #211c17 | #ebe7e1 |
| tinta secundária, hachura e tracejado | #615953 | #a9a49c |
| azul do objeto comprado ou prometido | #002fa7 | #497ef7 |
| azul em brilho ou luz | #3a63d0 | #a1bdf9 |

Regras da versão escura. Nenhuma massa chapada maior que um quinto da área, porque no escuro ela vira bloco pesado. Céu, parede e chão ficam no próprio fundo, sugeridos só pelo traço. Luz e brilho, que na clara são o papel deixado em branco, na escura passam ao azul em brilho. O contraste entre tinta e fundo fica acima de 7 para 1, e o do azul acima de 3 para 1.

A rubrica vermelha não entra em nenhuma peça, nas duas versões.

## 2.3 Formatos e arquivos

| família | proporção | tamanho do arquivo | área segura | arquivo |
|---|---|---|---|---|
| abertura | 16 x 9 | 1600 x 900 | faixa central de 1200 x 630, para o cartão | `site/ilustracoes/<id>.webp` e `<id>-escuro.webp` |
| vinheta | 1 x 1 | 480 x 480 | círculo central de 400 pixels de diâmetro | `site/ilustracoes/<id>.webp` e `<id>-escuro.webp` |

Abertura em WebP de qualidade 82, até 250 KB. Vinheta em WebP de qualidade 85, até 40 KB, com fundo opaco na cor do papel de cada versão. Nas vinhetas a margem é de 40 pixels de cada lado, e nada encosta na borda.

## 2.4 Cartão de compartilhamento

Nas quatro páginas de problema que ganham abertura, o cartão de 1200 x 630 passa a ser o recorte da área segura da versão clara, com faixa inferior de 150 pixels no papel e a pergunta da página na Newsreader, como nos cartões atuais. Nos problemas sem abertura, o cartão leva a vinheta da porta à esquerda, a 360 pixels, e a pergunta à direita. Mudança em `ferramentas/gerar_cartoes.py`.

## 2.5 Pedido ao gerador de imagens

Cada peça tem o campo producao, que é o pedido pronto. Todo pedido começa pelo mesmo preâmbulo, para a família não variar entre sessões.

Preâmbulo das aberturas. Ilustração editorial em linha fina, volumes chapados, hachura discreta, perspectiva controlada, muito espaço vazio, sem texto, sem logotipos, sem interface real, sem rosto definido, sem elemento de jogo real. Fundo opaco na cor indicada. Só as cores indicadas.

Preâmbulo das vinhetas. Ícone ilustrado de objeto único, linha de espessura uniforme, cantos arredondados, no máximo três massas de cor, centralizado, sem chão, sem sombra, sem texto. Fundo opaco na cor indicada. Só as cores indicadas.

Depois do preâmbulo vêm a cena, as cores da versão e as proibições da peça. A versão escura se pede na mesma conversa, com a clara anexada, e com a frase Mesma composição, mesmas linhas, troque só as cores pela tabela.

A armadura, quando aparece, segue a folha canônica de `estrutura/referencias-visuais/armadura.webp`, anexada ao pedido.

## 2.6 Critérios de aceite

Uma peça só entra se passar por todos.

- Lida a 56 pixels (vinheta) ou a 390 pixels de largura (abertura), a ideia se entende sem a legenda.
- As duas versões têm o mesmo desenho, conferido por sobreposição.
- Nenhum texto, número, marca ou interface reconhecível.
- O azul marca só o que era do leitor ou o que foi prometido a ele.
- A escura não tem bloco chapado acima de um quinto da área, e o contraste passa na tabela.
- O arquivo respeita formato, peso e área segura.
- O Claude confere a peça contra a ideia, e o autor a aprova no ar.

# 3. Integração no site

## 3.1 Vinhetas

O gerador lê a vinheta pela chave `porta-<id>` e a põe em três lugares.

- Capa da Informação, no cartão de cada porta, à esquerda do título, a 72 pixels no computador e a 56 no celular. O título e a frase passam a correr ao lado da vinheta.
- Página de problemas, no título de cada família (`h2#porta-<id>`), a 56 pixels.
- Lateral de cada problema, no título da família, a 40 pixels.

A vinheta é decorativa, porque o título ao lado já diz tudo. Leva `alt=""` e `aria-hidden="true"`. A legenda não aparece. Na Ciência, como as demais peças, mostra a etiqueta `data-arq` com a ideia.

Sem arquivo, nada aparece, e o cartão da porta fica como hoje.

## 3.2 Aberturas

As aberturas usam o mecanismo atual de `figure.ilustracao formato-16x9`, com `arte-clara` e `arte-escura`.

- problema-<slug> entra na página `problemas/<slug>/`, depois do primeiro parágrafo da abertura e antes do primeiro título.
- direitos-continua entra em `direitos/`, depois do primeiro parágrafo.
- alem-do-consumo entra em `alem-do-consumo/`, depois do primeiro parágrafo e antes da nota de acréscimo.

Como as peças novas trazem versão escura desenhada, o filtro de negativo parcial do fim de `site/extra.css` deixa de valer para elas. A regra passa a mirar só as 29 peças antigas, por uma classe `negativo-calculado` que o gerador põe quando a peça vem de `ferramentas/negativo.py`.

## 3.3 Saída da peça inicio da capa

A peça inicio sai da capa da Informação e da Doutrina. Fica na capa da Ciência, junto das cenas da skin, e no Caminho, onde a história começa.

## 3.4 Versão inglesa

Legendas e textos alternativos entram na memória de tradução na mesma rodada, em `traducao/saida/ilustracoes-novas.jsonl`.

# 4. As peças

## porta-acesso

### pagina

Capa da Informação, cartão Perdi o acesso. Problemas, família Perdi o acesso. Lateral dos problemas da família.

### formato

1 x 1, vinheta

### prioridade

A

### objetivo

Fazer quem perdeu a conta ou o serviço se reconhecer antes de ler. O que se perdeu continua existindo, só que do outro lado.

### ideia

Uma porta fechada, vista de frente, com a fechadura do lado de fora. Pela fresta de baixo escapa uma luz azul.

> Encerrada a conta, o usuário não terá mais acesso à conta, nem aos dados associados, nem ao Conteúdo Virtual, incluindo moeda do jogo, e a consequência é a perda definitiva sem reembolso quando o senhorio entende que havia motivo (p. 155)

### alt

Porta fechada por fora, com luz azul escapando pela fresta.

### producao

Uma porta simples de madeira, fechada, vista de frente, ocupando dois terços da altura. Fechadura grande e visível do lado de quem olha. Da fresta embaixo da porta sai uma faixa curta de luz azul, a única cor da peça além da tinta. Nada de corrente, cadeado de filme ou placa. Clara com fundo #faf6ef, tinta #211c17, luz #3a63d0. Escura com fundo #17130f, tinta #ebe7e1, luz #a1bdf9.

### estado

proposta

## porta-mudou

### pagina

Capa da Informação, cartão O que comprei mudou. Problemas, família O que comprei mudou. Lateral dos problemas da família.

### formato

1 x 1, vinheta

### prioridade

A

### objetivo

Mostrar a mudança que não aparece no inventário. O item continua lá, mas perdeu o que fazia.

### ideia

O mesmo objeto desenhado duas vezes, lado a lado. O da esquerda é cheio de azul. O da direita tem o mesmo contorno e está oco.

> A promessa de distinção permanece nominalmente na conta, mas deixa de encontrar, no mundo do jogo, o encaixe que conferia valor ao investimento de tempo, dinheiro e atenção. (p. 104)

### alt

Dois objetos iguais por fora, o segundo vazio por dentro.

### producao

Dois escudos pequenos idênticos no contorno, lado a lado, com uma seta curta de tinta entre eles. O da esquerda preenchido de azul chapado. O da direita só com o contorno em azul e o miolo no fundo. Nenhum dano, rachadura ou quebra, porque a mudança é de função e não de estrago. Clara com azul #002fa7. Escura com azul #497ef7.

### estado

proposta

## porta-empurrado

### pagina

Capa da Informação, cartão Fui empurrado a pagar. Problemas, família Fui empurrado a pagar. Lateral dos problemas da família.

### formato

1 x 1, vinheta

### prioridade

A

### objetivo

Dar forma à pressão que vem da soma de mecanismos, e não de um gesto só.

### ideia

Um corredor visto de cima que se estreita até um único balcão. As paredes têm pequenos relógios.

> Ela tende a emergir como programa de funcionamento, isto é, como articulação entre múltiplos mecanismos que comprimem tempo de reflexão, reorganizam expectativa, aumentam custo de saída, dificultam reversão e tornam a fruição progressivamente dependente do próprio ambiente que a governa. (p. 670)

### alt

Corredor que se estreita até um balcão, com relógios nas paredes.

### producao

Planta vista de cima de um corredor em forma de funil, largo embaixo e estreito em cima, desenhado só por duas linhas de tinta. No fim estreito, um balcão pequeno em azul chapado. Ao longo das paredes, três ou quatro relógios de ponteiro bem pequenos. Nenhuma pessoa e nenhuma seta. Clara com balcão #002fa7. Escura com balcão #497ef7.

### estado

proposta

## porta-sair

### pagina

Capa da Informação, cartão Quero sair e levar o que é meu. Problemas, família Quero sair. Lateral dos problemas da família.

### formato

1 x 1, vinheta

### prioridade

A

### objetivo

Mostrar que sair é permitido, mas o que a pessoa quer levar fica amarrado ao lugar.

### ideia

Uma mala aberta, cheia de objetos pequenos. Cada objeto está preso por um fio fino que sai do quadro.

> Sair significa abandonar histórico, reputação, biblioteca, itens, progressão, investimentos afetivos, redes de sociabilidade e, em certos casos, a própria capacidade de participar de comunidades que se organizam dentro daquele ecossistema. (p. 217)

### alt

Mala aberta com objetos presos por fios que saem do quadro.

### producao

Mala de viagem aberta, vista de três quartos, com quatro ou cinco objetos genéricos dentro, um livro, uma estrela, um pequeno coração, uma medalha, em azul chapado. De cada objeto sai um fio de tinta secundária, tracejado, que se estende para a borda de cima e some. Nada de corrente nem de cadeado. Clara com objetos #002fa7 e fios #615953. Escura com objetos #497ef7 e fios #a9a49c.

### estado

proposta

## porta-decide

### pagina

Capa da Informação, cartão A plataforma decide sobre mim sem explicar. Problemas, família A plataforma decide. Lateral dos problemas da família.

### formato

1 x 1, vinheta

### prioridade

A

### objetivo

Mostrar a decisão que tem efeito, mas não pode ser conferida. Vale para quem compra, vende ou trabalha, e por isso não mostra ninguém.

### ideia

Uma balança atrás de um vidro fosco. Só a silhueta aparece, e um prato já desceu.

> A alteração de regra, o rebaixamento de alcance ou a suspensão sequer se transformam em objeto verificável e disputável no próprio sistema. (p. 381)

### alt

Balança atrás de vidro fosco, com um prato já abaixado.

### producao

Um painel retangular de vidro fosco, com moldura fina de tinta, ocupando o centro. Atrás dele, em silhueta difusa de tinta secundária, uma balança de dois pratos com um dos pratos claramente mais baixo. No prato baixo, um ponto azul pequeno e nítido, a única coisa que atravessa o vidro. Clara com vidro em #f1ebe1 e ponto #002fa7. Escura com vidro em #241f1a e ponto #497ef7.

### estado

proposta

## porta-comum

### pagina

Capa da Informação, cartão Provar e reclamar. Problemas, família Provar e reclamar. Lateral dos problemas da família.

### formato

1 x 1, vinheta

### prioridade

A

### objetivo

Marcar a porta por onde todas as outras passam. O objeto é o que a pessoa guarda, e não o que perdeu, e por isso a vinheta é mais calma que as outras.

### ideia

Uma pilha curta de papéis presa por um clipe, com uma captura de tela em azul por cima.

> A prova mínima exigível, do ponto de vista do consumidor, consiste em apresentação plausível da experiência lesiva, de sua inserção no ecossistema e dos elementos de contexto acessíveis (p. 747)

### alt

Papéis presos por clipe, com uma captura de tela por cima.

### producao

Três folhas levemente desalinhadas, com linhas de texto sugeridas por traços sem letra, presas por um clipe no canto. Por cima, um retângulo menor com cantos arredondados, como uma tela de celular, em azul chapado, sem nada desenhado dentro. Clara com tela #002fa7. Escura com tela #497ef7.

### estado

proposta

## problema-conta-bloqueada

### pagina

Problemas, Minha conta foi bloqueada ou banida, depois do primeiro parágrafo da abertura. Também o cartão de compartilhamento da página.

### formato

16 x 9, abertura

### prioridade

A

### objetivo

Ensinar, antes do texto, que a punição muitas vezes não é expulsar, e sim rebaixar. A pessoa pode estar punida sem ter saído.

### ideia

Uma praça cheia de figuras sem rosto. Uma delas continua no meio, mas desenhada só em tracejado, e as outras olham para outro lado. A armadura dela continua inteira e azul.

> A punição relevante muitas vezes não é expulsar, mas rebaixar, porque continuar dentro, porém menos visível, menos elegível e menos reconhecível, equivale a degradar a posição de fruição e a corroer o valor que dependia de comensurabilidade e validação em circuito. (p. 373)

### alt

Praça cheia de gente, com uma figura no meio desenhada só em tracejado e a armadura azul inteira.

### legenda

Continuar dentro, sem ser visto, também é punição.

### producao

Praça aberta vista de cima, em diagonal suave, com doze a quinze figuras sem rosto em traço cheio de tinta, em pequenos grupos conversando. No centro exato da área segura, uma figura com a armadura canônica, de pé, sozinha. O corpo dela é só contorno tracejado em tinta secundária, e a armadura continua em azul chapado e inteira. Ninguém olha para ela. Nada de cerca, grade ou guarda. Chão sugerido por poucas linhas. Clara com fundo #faf6ef e armadura #002fa7. Escura com fundo #17130f, figuras #ebe7e1, tracejado #a9a49c e armadura #497ef7.

### estado

proposta

## problema-so-licenca

### pagina

Problemas, A empresa diz que eu só tenho uma licença, depois do primeiro parágrafo. Também o cartão.

### formato

16 x 9, abertura

### prioridade

A

### objetivo

Responder à dúvida da pessoa sem negar a compra. O que ela levou é produto, e o que vem junto é o controle que continua.

### ideia

Um balcão de loja. Uma pessoa sai com o objeto azul nas mãos, e uma corrente fina liga o objeto ao chão da loja.

> A consequência institucional possível consiste na abertura dos filtros subsequentes do regime, impedindo que a controvérsia seja neutralizada pela alegação de mera prestação de serviço ou de simples licenciamento formal. (p. 743)

### alt

Pessoa saindo de uma loja com o objeto comprado, preso ao chão da loja por uma corrente fina.

### legenda

Você levou o que comprou. A corrente veio junto.

### producao

Interior de loja em perspectiva lateral. À esquerda, um balcão simples. Ao centro, uma figura sem rosto caminhando para a direita com uma caixa azul nas mãos, já fora da linha do balcão. Da caixa sai uma corrente fina de tinta que desce e se prende a uma argola no chão, junto ao balcão. A corrente fica frouxa, sem esticar, porque o controle é contínuo e não violento. Nenhum botão, preço ou letreiro. Clara com caixa #002fa7. Escura com caixa #497ef7 e corrente #ebe7e1.

### estado

proposta

## problema-jogo-encerrado

### pagina

Problemas, O serviço vai acabar, depois do primeiro parágrafo. Também o cartão.

### formato

16 x 9, abertura

### prioridade

A

### objetivo

Mostrar que encerrar a atividade não apaga o que as pessoas já tinham, e que essa passagem tem deveres.

### ideia

Um prédio à noite, com as janelas se apagando de cima para baixo. Na calçada, pessoas seguram caixas azuis que ainda brilham.

> O direito de explorar, encerrar ou reorganizar atividade econômica não se confunde com um suposto direito de aniquilar, sem deveres de transição, preservação ou transferência, a fruição funcional já estabilizada na esfera do consumidor. (p. 709)

### alt

Prédio com as janelas se apagando e pessoas na calçada segurando caixas que ainda brilham.

### legenda

O serviço pode acabar. O que já era seu pede uma passagem.

### producao

Prédio comum de vários andares, de frente, ocupando a metade esquerda. Janelas em grade, as de cima apagadas em tinta, as de baixo ainda acesas. Na calçada à direita, quatro ou cinco figuras sem rosto, de idades variadas, cada uma segurando uma caixa pequena azul com um leve halo. Nada de fumaça, ruína ou demolição. Clara com céu no próprio fundo #faf6ef, janelas acesas #f1ebe1 contornadas, caixas #002fa7 e halo #3a63d0. Escura com céu no fundo #17130f, janelas acesas #241f1a, caixas #497ef7 e halo #a1bdf9.

### estado

proposta

## problema-sair

### pagina

Problemas, problema sair, depois do primeiro parágrafo. Também o cartão.

### formato

16 x 9, abertura

### prioridade

B

### objetivo

Dar à porta de sair o mesmo peso visual das outras, com a cena grande da vinheta.

### ideia

A cena da vinheta porta-sair, ampliada. A pessoa está na soleira, e a mala ficou para trás, presa pelos fios.

> O poder não se estabiliza só por preço, mas por custo de saída. (p. 217)

### alt

Pessoa na soleira de uma porta, olhando a mala presa por fios que ficou para trás.

### legenda

Sair é livre. Levar o que é seu, nem sempre.

### producao

Cômodo visto de lado. À direita, uma porta aberta para um fundo vazio, e na soleira uma figura sem rosto, de costas para a saída, olhando para trás. No chão à esquerda, a mesma mala da vinheta, aberta, com os mesmos objetos azuis, e os fios tracejados que sobem e saem pela borda de cima. Clara com objetos #002fa7. Escura com objetos #497ef7 e fios #a9a49c.

### estado

proposta

## direitos-continua

### pagina

Seus direitos, depois do primeiro parágrafo e antes da lista dos onze direitos.

### formato

16 x 9, abertura

### prioridade

A

### objetivo

Fixar a virada que organiza a página inteira. A compra começa uma relação e não termina num instante. Sem isso, a lista dos onze deveres parece arbitrária.

### ideia

Uma loja à noite, já fechada para a rua. O balcão continua aceso, e um fio sai dele, atravessa a vitrine e chega à mão de uma pessoa que vai embora com o objeto azul.

> Em consumo contínuo, a aquisição inaugura uma posição no ecossistema e não uma entrega exaurida em um instante. (p. 428)

### alt

Loja fechada com o balcão aceso e um fio que vai dele até a mão de quem levou a compra.

### legenda

A loja fechou. O balcão continua aceso.

### producao

Fachada de loja à noite, de frente, com a porta fechada e a vitrine larga. Dentro, um balcão iluminado, a única luz do interior. Do balcão sai um fio de tinta, que passa pela vitrine sem quebrá-la e segue pela calçada até a mão de uma figura sem rosto que caminha para a direita com uma caixa azul. O fio continua contínuo e frouxo. A figura caminha tranquila. Clara com luz do balcão #f1ebe1 e caixa #002fa7. Escura com luz do balcão #a1bdf9, sem halo largo, e caixa #497ef7.

### estado

proposta

## alem-do-consumo

### pagina

Além do consumo, depois do primeiro parágrafo e antes da nota de acréscimo.

### formato

16 x 9, abertura

### prioridade

A

### objetivo

Fazer o vendedor ou o trabalhador se ver na primeira tela sem o nome OIFG, que a Informação não usa, e ligar a página ao resto do site pelo mesmo terreno.

### ideia

O terreno flutuante do díptico parte-a-lei e ideia-oic. Sobre ele, no lugar da figura de armadura, uma pessoa montou uma banca com prateleiras e clientes em volta. Os cabos que sustentam o terreno sobem para fora do quadro.

> O critério, portanto, não é a materialidade do suporte nem a nomenclatura empregada pelo fornecedor, mas a dependência estrutural da fruição em relação a um ambiente governado. (p. 719)

### alt

Pessoa com uma banca e clientes sobre um terreno flutuante, sustentado por cabos que sobem para fora da imagem.

### legenda

O que foi construído aqui também é de alguém.

### producao

Anexar parte-a-lei.webp como referência de terreno. Mesmo terreno, mesma fundação, mesmo contorno e mesmos cabos, na mesma posição. Sobre ele, uma banca simples de feira com duas prateleiras de objetos pequenos em azul, uma figura sem rosto atrás dela e três figuras em volta, como clientes. Nenhuma armadura. Os cabos sobem e somem na borda de cima, em tinta secundária. Clara com objetos #002fa7. Escura com objetos #497ef7, cabos #a9a49c e terreno só em contorno, sem massa chapada.

### estado

proposta

# 5. Ordem de produção

Primeiro as seis vinhetas, numa mesma sessão do gerador, para que a família saia homogênea. São as mais baratas e mudam a capa inteira. Antes de publicar, as seis são vistas juntas, lado a lado, nas duas versões.

Depois direitos-continua e alem-do-consumo, que fecham as páginas de entrada.

Por último as quatro aberturas de problema, com os cartões refeitos no mesmo passo.

Cada lote passa pelos critérios de aceite antes de entrar, e o autor o vê no ar.

# 6. Ficam fora, por ora

As vinhetas dos onze direitos ficam para depois. Só valem se o índice de Seus direitos virar grade de cartões, porque numa lista de faixas a vinheta pequena atrapalha a leitura.

Os outros vinte problemas usam a vinheta da porta no cartão de compartilhamento e não ganham abertura própria.

Como reclamar, Situações, capítulos da Doutrina, fichas dos conceitos e páginas da Ciência não recebem peças novas.
