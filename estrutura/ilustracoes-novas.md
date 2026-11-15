# Plano consolidado das ilustrações, versão 0.17

Rascunho do Claude de 15/11/2026, por ordem do autor, refeito no mesmo dia como plano consolidado de todas as peças do site, novas e antigas, para geração numa mesma sessão. É planejamento, e nada daqui está no site. As peças seguem a direção de arte de `estrutura/ilustracoes.md` e acrescentam as regras abaixo. Quando o autor aprovar, cada peça passa para `estrutura/ilustracoes.md` no mesmo formato de campos, e o gerador a lê de lá.

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

# 4. Inventário

Todas as peças do site, novas e antigas, para a mesma sessão de geração. Situação nova quer dizer desenhar as duas versões. Situação escura quer dizer desenhar só a versão escura a partir da clara publicada.

| id | lugar | família | situação |
|---|---|---|---|
| porta-acesso | capa, problemas e lateral | vinheta | nova |
| porta-mudou | capa, problemas e lateral | vinheta | nova |
| porta-empurrado | capa, problemas e lateral | vinheta | nova |
| porta-sair | capa, problemas e lateral | vinheta | nova |
| porta-decide | capa, problemas e lateral | vinheta | nova |
| porta-comum | capa, problemas e lateral | vinheta | nova |
| problema-conta-bloqueada | problemas/conta-bloqueada/ | abertura | nova |
| problema-item-alterado | problemas/item-alterado/ | abertura | nova |
| problema-servico-piorou | problemas/servico-piorou/ | abertura | nova |
| problema-presente-retirado | problemas/presente-retirado/ | abertura | nova |
| problema-jogo-encerrado | problemas/jogo-encerrado/ | abertura | nova |
| problema-so-licenca | problemas/so-licenca/ | abertura | nova |
| problema-promessa | problemas/promessa/ | abertura | nova |
| problema-exclusivo-voltou | problemas/exclusivo-voltou/ | abertura | nova |
| problema-sorteio | problemas/sorteio/ | abertura | nova |
| problema-moeda | problemas/moeda/ | abertura | nova |
| problema-pressa | problemas/pressa/ | abertura | nova |
| problema-regras-escondidas | problemas/regras-escondidas/ | abertura | nova |
| problema-prova | problemas/prova/ | abertura | nova |
| problema-reclamacao-some | problemas/reclamacao-some/ | abertura | nova |
| problema-sair | problemas/sair/ | abertura | nova |
| problema-historia-perdida | problemas/historia-perdida/ | abertura | nova |
| problema-programa-no-aparelho | problemas/programa-no-aparelho/ | abertura | nova |
| problema-crianca | problemas/crianca/ | abertura | nova |
| problema-assistente | problemas/assistente/ | abertura | nova |
| problema-loja-virtual | problemas/loja-virtual/ | abertura | nova |
| problema-rede-social | problemas/rede-social/ | abertura | nova |
| problema-trabalho-por-app | problemas/trabalho-por-app/ | abertura | nova |
| problema-vendo-na-plataforma | problemas/vendo-na-plataforma/ | abertura | nova |
| problema-muita-gente | problemas/muita-gente/ | abertura | nova |
| direitos-continua | direitos/ | abertura | nova |
| alem-do-consumo | alem-do-consumo/ | abertura | nova |
| como-reclamar | como-reclamar/ | abertura | nova |
| direito-a | direitos/ e direitos/a/ | vinheta | nova |
| direito-b | direitos/ e direitos/b/ | vinheta | nova |
| direito-c | direitos/ e direitos/c/ | vinheta | nova |
| direito-d | direitos/ e direitos/d/ | vinheta | nova |
| direito-e | direitos/ e direitos/e/ | vinheta | nova |
| direito-f | direitos/ e direitos/f/ | vinheta | nova |
| direito-g | direitos/ e direitos/g/ | vinheta | nova |
| direito-h | direitos/ e direitos/h/ | vinheta | nova |
| direito-i | direitos/ e direitos/i/ | vinheta | nova |
| direito-j | direitos/ e direitos/j/ | vinheta | nova |
| direito-k | direitos/ e direitos/k/ | vinheta | nova |
| inicio | Página inicial, logo depois do título e dos atalhos, antes da narrativa da compra | abertura | escura |
| parte-a-compra | Percurso, parte 1, A compra, na abertura | abertura | escura |
| imagem-catraca | Percurso, parte 1, A compra, depois do bloco Uma imagem da catraca | interna | escura |
| imagem-estoque-fluxo | Percurso, parte 1, A compra, depois do bloco Uma imagem da gaveta e do cano | interna | escura |
| parte-o-desejo | Percurso, parte 2, O desejo, na abertura | abertura | escura |
| parte-o-dono | Percurso, parte 3, O dono, na abertura | abertura | escura |
| imagem-torneira | Percurso, parte 3, O dono, depois do bloco Uma imagem da torneira | interna | escura |
| parte-as-regras | Percurso, parte 4, As regras, na abertura | abertura | escura |
| parte-o-normal | Percurso, parte 5, O normal, na abertura | abertura | escura |
| parte-a-mudanca | Percurso, parte 6, A mudança, na abertura | abertura | escura |
| parte-o-desenho | Percurso, parte 7, O desenho, na abertura | abertura | escura |
| parte-a-lei | Percurso, parte 8, A lei, na abertura | abertura | escura |
| parte-a-resposta | Percurso, parte 9, A resposta, na abertura | abertura | escura |
| parte-alem-do-jogo | Percurso, parte 10, Além do jogo, na abertura | abertura | escura |
| parte-o-nome | Percurso, parte 11, O nome, na abertura | abertura | escura |
| ideia-oic | Objeto Imaterial de Consumo, depois de Isso tem nome | abertura | escura |
| ideia-feixe-de-fruicao-governada | Feixe de fruição governada, depois de Isso tem nome | abertura | escura |
| ideia-lex-plataformae | Lex Plataformae, depois de Isso tem nome | abertura | escura |
| ideia-vulnerabilidade-semiotica | Vulnerabilidade semiótica, depois de Isso tem nome | abertura | escura |
| ideia-teleologia-abusiva | Teleologia abusiva, depois de Isso tem nome | abertura | escura |
| ideia-ilicito-de-arquitetura | Ilícito de arquitetura, depois de Isso tem nome | abertura | escura |
| ideia-antecipacao-hipercuratorial | Antecipação hipercuratorial, depois de Isso tem nome | abertura | escura |
| ideia-auditabilidade-aberta | Auditabilidade aberta, depois de Isso tem nome | abertura | escura |
| ideia-equivalencia-de-valor-funcional | Equivalência de valor funcional, depois de Isso tem nome | abertura | escura |
| laboratorio | Laboratório, depois da abertura | abertura | escura |
| familia-funcionalidade-cognitiva | Laboratório, funcionalidade cognitiva, depois do resumo | interna | escura |
| familia-infraestrutura-e-intermediacao | Laboratório, infraestrutura e intermediação, depois do resumo | interna | escura |
| familia-produtividade-gig-economy | Laboratório, produtividade sob a gig economy, depois do resumo | interna | escura |
| familia-administracao-de-confianca | Laboratório, administração de confiança, depois do resumo | interna | escura |

Total de 73 peças, 44 novas e 29 do acervo.

# 5. Peças novas da entrada

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

## como-reclamar

### pagina

Como reclamar, depois do primeiro parágrafo e antes do esquema I6.

### formato

16 x 9, abertura

### prioridade

B

### objetivo

Dizer à pessoa que ela não está sozinha diante da empresa, e que há portas além do atendimento. O esquema logo abaixo organiza as portas, e a imagem só abre a página.

### ideia

Uma pessoa diante de um corredor com quatro portas abertas, cada uma com uma luz diferente saindo. A primeira, a mais próxima, é a da própria empresa.

Acréscimo posterior, como a página. Não cita a tese, que não trata dos canais de reclamação.

### alt

Pessoa diante de um corredor com quatro portas abertas e iluminadas.

### legenda

Há mais de uma porta.

### producao

Corredor em perspectiva central, com quatro portas abertas, duas de cada lado, em distâncias crescentes. De cada uma sai um retângulo de luz no chão. Uma figura sem rosto, pequena, de costas, no começo do corredor. Sem placas, brasões ou símbolos de órgão público. Clara com luzes #f1ebe1 contornadas e a porta mais próxima em #002fa7. Escura com luzes #241f1a e porta #497ef7.

### estado

proposta

# 6. Aberturas dos outros problemas

Mesma família, formato e integração das aberturas de problema da seção 5. Cada uma vira também o cartão de compartilhamento da página.

## problema-item-alterado

### pagina

Problemas, O que eu comprei mudou numa atualização. E agora? Depois do primeiro parágrafo da abertura. Também o cartão.

### formato

16 x 9, abertura

### prioridade

A

### objetivo

Mostrar que a mudança depois da venda é o problema, e não a mudança em si, que pode ser legítima.

### ideia

Uma vitrine em que a mesma armadura aparece duas vezes, antes e depois de uma atualização. Uma mão de fora do quadro troca uma peça dela com uma chave de ferramenta.

> A mutabilidade, por si, não é ilícita. O problema começa quando ela deixa de operar como forma legítima de manutenção, aperfeiçoamento ou adaptação do fornecimento e passa a degradar, esvaziar ou desviar, de modo relevante, a função que justificou a aquisição e estruturou a expectativa legítima de fruição. (p. 729)

### alt

Mão que troca uma peça da armadura azul exposta numa vitrine, com a versão anterior ao lado.

### legenda

A peça que você comprou foi trocada depois.

### producao

Vitrine de museu com duas peanhas. Na da esquerda, a armadura canônica inteira. Na da direita, a mesma armadura, e uma mão sem corpo, vinda da borda de cima, ajusta uma ombreira com uma chave de ferramenta simples. A peça trocada fica em azul mais claro que o resto. Nada de dano. Clara com armadura #002fa7 e peça trocada #3a63d0. Escura com armadura #497ef7 e peça trocada #a1bdf9.

### estado

proposta

## problema-servico-piorou

### pagina

Problemas, O serviço piorou, e o preço continua o mesmo. Posso reclamar? Depois do primeiro parágrafo da abertura. Também o cartão.

### formato

16 x 9, abertura

### prioridade

B

### objetivo

Fazer a pessoa ver a redução que não aparece como corte, a de pagar o mesmo e receber menos.

### ideia

Uma balança de feira. No prato do preço, a mesma pilha de moedas de sempre. No prato do serviço, uma caixa azul que foi ficando menor, com o contorno antigo em tracejado em volta.

> A redução raramente aparece como corte explícito de “aulas”, mas pode se manifestar como perda de alcance, rebaixamento persistente de performance, restrição cumulativa de funcionalidades, compressão de limites, reordenação de visibilidade ou alterações estruturais que elevam o custo de fruir a mesma utilidade. A lógica é a mesma. Mantêm-se o rótulo e o preço, e rebaixa-se a entrega de valor. (p. 480)

### alt

Balança com a mesma pilha de moedas de um lado e, do outro, uma caixa menor dentro do contorno tracejado da caixa antiga.

### legenda

Mesmo preço, caixa menor.

### producao

Balança de dois pratos vista de frente. Prato da esquerda com uma pilha de moedas genéricas em tinta. Prato da direita com uma caixa azul pequena, e em volta dela o contorno tracejado de uma caixa maior. A balança pende para o lado das moedas. Clara com caixa #002fa7 e tracejado #615953. Escura com caixa #497ef7 e tracejado #a9a49c.

### estado

proposta

## problema-presente-retirado

### pagina

Problemas, Um item que recebi de presente foi retirado da minha conta. E agora? Depois do primeiro parágrafo da abertura. Também o cartão.

### formato

16 x 9, abertura

### prioridade

A

### objetivo

Mostrar que quem recebeu de presente não fez nada de errado, e que a falha estava antes, no caminho.

### ideia

Duas mãos trocam um pacote azul. Atrás delas, longe, a corrente que trouxe o pacote tem um elo rompido, fora do alcance das duas.

> A segunda camada é a do risco operacional já conhecido pela fornecedora. A Riot mantém, em mais de um título de seu portfólio, orientação específica para hipóteses de cobrança não autorizada, fraude financeira e contestação posterior de transações. Essas comunicações demonstram que o problema de chargeback e uso indevido de meios de pagamento não era fato externo, extraordinário ou imprevisível. Tratava-se de risco operacional reconhecido institucionalmente, com fluxos internos de apuração, reembolso e suspensão. (p. 610)

### alt

Duas pessoas trocando um presente azul, com uma corrente rompida ao fundo, longe delas.

### legenda

A falha estava antes de você.

### producao

Primeiro plano com duas figuras sem rosto, uma entregando à outra um pacote com laço, em azul. Ao fundo, uma corrente longa de tinta secundária atravessa o quadro na horizontal, com um elo aberto bem visível e distante das figuras. Clima de gentileza, não de crime. Clara com pacote #002fa7. Escura com pacote #497ef7 e corrente #a9a49c.

### estado

proposta

## problema-promessa

### pagina

Problemas, O que foi anunciado não é o que eu recebi. E agora? Depois do primeiro parágrafo da abertura. Também o cartão.

### formato

16 x 9, abertura

### prioridade

A

### objetivo

Separar o que foi mostrado antes da compra do que chegou depois.

### ideia

Um cartaz grande com a silhueta de uma armadura enorme e brilhante. Diante dele, uma pessoa abre uma caixa pequena com uma armadura menor e simples.

> Sempre que a fruição for precedida por ciclos curados de antecipação, promessa, escassez sugerida, distinção simbólica ou equivalências insinuadas, a publicidade integrará materialmente a oferta. (p. 744-745)

### alt

Pessoa abrindo uma caixa pequena diante de um cartaz com a silhueta de uma armadura muito maior.

### legenda

O cartaz prometeu outra coisa.

### producao

Cartaz retangular ao fundo, sem texto, com a silhueta da armadura canônica em azul em brilho, grande e com raios. Em primeiro plano, uma figura sem rosto segura uma caixa aberta, e dentro dela a armadura canônica pequena em azul chapado, sem brilho. Clara com cartaz #3a63d0 e armadura #002fa7. Escura com cartaz #a1bdf9, sem halo largo, e armadura #497ef7.

### estado

proposta

## problema-exclusivo-voltou

### pagina

Problemas, Paguei caro por algo exclusivo, e ele voltou mais barato. Isso pode? Depois do primeiro parágrafo da abertura. Também o cartão.

### formato

16 x 9, abertura

### prioridade

B

### objetivo

Mostrar a promessa de exclusividade desfeita pela volta do item mais barato.

### ideia

Uma vitrine com um único item azul sob redoma. Do lado de fora, o mesmo item empilhado em caixas numa banca de promoção.

> Quando a plataforma vende um item por valor elevado sob a promessa de exclusividade, ou apresenta a exclusividade como atributo relevante para justificar preço e dispêndio, ela incorpora essa qualidade ao conteúdo da oferta e à utilidade percebida do objeto. (p. 213)

### alt

Item sob redoma numa vitrine e, ao lado, o mesmo item empilhado numa banca.

### legenda

Era único. Voltou em pilha.

### producao

À esquerda, peanha com redoma de vidro e um único medalhão azul dentro. À direita, uma banca simples com seis ou sete medalhões iguais empilhados, em azul mais claro. Sem preço nem letreiro. Clara com medalhão da redoma #002fa7 e da banca #3a63d0. Escura com #497ef7 e #a1bdf9.

### estado

proposta

## problema-sorteio

### pagina

Problemas, Paguei por um sorteio ou por uma caixa de recompensa. O que preciso saber? Depois do primeiro parágrafo da abertura. Também o cartão.

### formato

16 x 9, abertura

### prioridade

A

### objetivo

Mostrar que a chance existe, mas está escondida de quem paga.

### ideia

Uma caixa fechada com uma alavanca. Dentro, visível só por um corte, uma roda com muitas casas vazias e poucas azuis.

> A discussão institucional tende, então, a concentrar-se em transparência mínima das condições de aquisição, proteção de públicos vulneráveis e controle de práticas de indução de consumo, não por moralização do setor, mas porque o fornecedor concentra critérios internos sobre disponibilidade, rotação, raridade e, quando aplicável, probabilidade, em condições de baixa reconstruibilidade externa. (p. 494-495)

### alt

Caixa com alavanca e, por um corte, uma roda com poucas casas azuis entre muitas vazias.

### legenda

A chance estava lá dentro, longe dos seus olhos.

### producao

Caixa de madeira com alavanca lateral, vista de três quartos. Um recorte técnico, em tracejado cinza, abre a lateral e mostra uma roda com vinte casas, só duas em azul chapado. Nada de cassino, cartas, dados ou moedas douradas. Clara com casas #002fa7 e recorte #615953. Escura com casas #497ef7 e recorte #a9a49c.

### estado

proposta

## problema-moeda

### pagina

Problemas, A moeda do serviço passou a comprar menos. Isso é permitido? Depois do primeiro parágrafo da abertura. Também o cartão.

### formato

16 x 9, abertura

### prioridade

B

### objetivo

Mostrar a moeda interna que a plataforma recalibra quando quer.

### ideia

Uma balança de mercearia que pesa moedas azuis. Uma mão de fora do quadro gira o parafuso de ajuste da balança.

> A Riot não descreve a moeda do jogo como simples meio de troca neutro. Ela a trata como parte de um circuito fechado, cuja equivalência pode ser recalibrada de modo unilateral. O termo admite que, “às vezes”, a empresa pode alterar o poder de compra da Moeda do Jogo, inclusive aumentando o número de moedas necessárias para adquirir produtos virtuais como skins, e coloca esse movimento sob a promessa genérica de aviso e de progressividade (Riot Games, 2024e). (p. 176)

### alt

Balança pesando moedas azuis enquanto uma mão gira o parafuso de ajuste.

### legenda

Quem fez a moeda também mexe na balança.

### producao

Balança de ponteiro de mercearia, de frente, com um prato cheio de fichas redondas azuis. Embaixo, um parafuso de calibragem que uma mão sem corpo, vinda da borda direita, gira com os dedos. O ponteiro aponta para menos. Clara com fichas #002fa7. Escura com fichas #497ef7.

### estado

proposta

## problema-pressa

### pagina

Problemas, A oferta dizia última chance. Fui pressionado a comprar? Depois do primeiro parágrafo da abertura. Também o cartão.

### formato

16 x 9, abertura

### prioridade

A

### objetivo

Dar forma à urgência fabricada, que comprime o tempo de pensar.

### ideia

Uma ampulheta grande diante de um balcão, com a areia caindo rápido. Atrás do balcão, um calendário com folhas já arrancadas voando.

> A primeira família dessas técnicas é a da escassez artificial e da urgência fabricada. Seu mecanismo é conhecido. Janelas curtas, rotação acelerada de ofertas, contadores regressivos, “edições limitadas”, eventos efêmeros e benefícios temporários são usados para deslocar a decisão do campo da comparação racional para o da resposta reativa. (p. 670)

### alt

Ampulheta com a areia caindo rápido diante de um balcão, e folhas de calendário voando ao fundo.

### legenda

A pressa também foi desenhada.

### producao

Balcão simples visto de frente. Sobre ele, uma ampulheta alta com areia azul caindo em fio grosso. Ao fundo, folhas de calendário sem números, soltas no ar, em tinta secundária. Nenhum relógio digital, sirene ou letreiro. Clara com areia #002fa7. Escura com areia #497ef7 e folhas #a9a49c.

### estado

proposta

## problema-regras-escondidas

### pagina

Problemas, A regra que me prejudicou estava enterrada nos termos de uso. E agora? Depois do primeiro parágrafo da abertura. Também o cartão.

### formato

16 x 9, abertura

### prioridade

A

### objetivo

Mostrar que muito texto não é o mesmo que informação.

### ideia

Uma pessoa diante de uma montanha de papéis. Lá no meio, uma única folha azul, quase coberta pelas outras.

> A simples acumulação de textos, links, avisos, políticas, termos e janelas explicativas não satisfaz, por si, a exigência de informação adequada. (p. 722)

### alt

Pessoa diante de uma montanha de papéis com uma única folha azul enterrada no meio.

### legenda

A regra estava lá. Debaixo de tudo.

### producao

Pilha enorme de folhas em tinta, ocupando dois terços do quadro, com traços de texto sem letras. No meio da pilha, uma folha azul aparece só pela ponta. À direita, uma figura sem rosto pequena olha para a pilha. Clara com folha #002fa7. Escura com folha #497ef7 e pilha só em contorno, sem massa chapada.

### estado

proposta

## problema-prova

### pagina

Problemas, Os registros estão com a empresa. Como eu provo o que aconteceu? Depois do primeiro parágrafo da abertura. Também o cartão.

### formato

16 x 9, abertura

### prioridade

A

### objetivo

Mostrar que os registros do que aconteceu estão do lado da empresa.

### ideia

Um arquivo de gavetas atrás de um balcão alto. Do lado de cá, uma pessoa segura um único papel pequeno.

> Em litígios sobre OICs, essa é precisamente a configuração normal: logs, trilhas de interface, históricos de alteração, critérios de sanção, comunicações internas de suporte e registros técnicos relevantes ficam concentrados no fornecedor. (p. 659)

### alt

Arquivo de gavetas atrás de um balcão alto e, do lado de cá, uma pessoa com um único papel.

### legenda

Os registros ficaram do outro lado do balcão.

### producao

Balcão alto ao centro, como de cartório. Atrás dele, uma parede de arquivos de gaveta, várias abertas, com fichas em azul. Do lado de cá, uma figura sem rosto segura um papel pequeno em tinta. Clara com fichas #002fa7. Escura com fichas #497ef7 e arquivos só em contorno.

### estado

proposta

## problema-reclamacao-some

### pagina

Problemas, Reclamo, e a resposta nunca resolve. O que fazer? Depois do primeiro parágrafo da abertura. Também o cartão.

### formato

16 x 9, abertura

### prioridade

B

### objetivo

Mostrar o atendimento que responde sem resolver.

### ideia

Uma pessoa coloca uma carta numa caixa de correio. Por trás da caixa, a carta sai de volta pela outra fenda, igual, com um carimbo azul.

> Em ecossistemas governados por plataforma, o conflito não começa quando o usuário decide litigar, reclamar ou formalizar inconformidade. Em muitos casos, ele é governado antes disso. (p. 780)

### alt

Carta entrando numa caixa de correio e saindo de volta pelo outro lado, só com um carimbo.

### legenda

Respondida. Não resolvida.

### producao

Caixa de correio simples de perfil, com duas fendas. Uma mão sem corpo coloca uma carta pela fenda da esquerda. Da fenda da direita sai a mesma carta, idêntica, agora com um carimbo redondo azul sem letras. Clara com carimbo #002fa7. Escura com carimbo #497ef7.

### estado

proposta

## problema-historia-perdida

### pagina

Problemas, Perdi anos de histórico. Isso é mais do que um item? Depois do primeiro parágrafo da abertura. Também o cartão.

### formato

16 x 9, abertura

### prioridade

A

### objetivo

Mostrar que o histórico é mais do que um item, porque guarda anos.

### ideia

Uma estante de álbuns de fotografia em que as lombadas vão do mais novo ao mais velho. Uma mão de fora do quadro apaga a estante com uma borracha grande.

> A cláusula 2.3 dos Termos de Serviço da Riot prevê que, encerrada a conta, o usuário perde acesso à conta, aos dados associados, à moeda do jogo e ao conteúdo virtual, sem reembolso em hipóteses de justa causa, com possibilidade ainda de cancelamento de outras contas e de acesso a outros serviços. A cláusula é valiosa porque desnuda o problema: não se perde apenas item isolado, mas a posição global de fruição, o histórico, o inventário, a trajetória e a continuidade prática de inserção no ecossistema (p. 540-541)

### alt

Estante de álbuns sendo apagada por uma borracha grande.

### legenda

Anos de história, uma borracha.

### producao

Estante de três prateleiras com álbuns de lombada larga em azul, alguns mais claros, de idades diferentes. Uma borracha grande, segurada por uma mão sem corpo vinda da direita, apagou a prateleira de baixo, que aparece só em tracejado. Clara com lombadas #002fa7 e #3a63d0. Escura com #497ef7 e #a1bdf9.

### estado

proposta

## problema-programa-no-aparelho

### pagina

Problemas, O serviço exige um programa que roda no meu aparelho. Posso questionar? Depois do primeiro parágrafo da abertura. Também o cartão.

### formato

16 x 9, abertura

### prioridade

B

### objetivo

Mostrar o programa da empresa que ocupa o aparelho da pessoa.

### ideia

Um computador de mesa aberto, como num desenho técnico. Dentro, entre as peças, um pequeno guarda com lanterna, que é da empresa.

> O que está em jogo é a redefinição das fronteiras materiais de soberania do usuário sobre seu próprio equipamento. (p. 521)

### alt

Computador aberto em desenho técnico, com um pequeno vigia de lanterna instalado entre as peças.

### legenda

O aparelho é seu. O vigia é deles.

### producao

Gabinete de computador visto em corte técnico, com placas e cabos em tinta. Num canto, uma figura minúscula sem rosto, com lanterna em azul, sentada como vigia. Linhas de projeto em tracejado cinza. Sem marca nem logotipo. Clara com vigia #002fa7. Escura com vigia #497ef7 e corte #a9a49c.

### estado

proposta

## problema-crianca

### pagina

Problemas, Meu filho ou minha filha gastou num jogo. O que a lei diz? Depois do primeiro parágrafo da abertura. Também o cartão.

### formato

16 x 9, abertura

### prioridade

A

### objetivo

Falar com o responsável, que vê a compra feita por quem ainda não entende o que paga.

### ideia

Uma criança alcança um botão azul alto, na ponta dos pés, enquanto um adulto chega por trás.

> O recorte por menores funciona, assim, como gatilho institucional para tornar visíveis assimetrias de compreensão e de capacidade de contestação em ambientes governados por arquitetura. (p. 494)

### alt

Criança na ponta dos pés alcançando um botão azul, com um adulto chegando por trás.

### legenda

Para quem ainda não entende o preço, o botão é só um botão.

### producao

Parede lisa com um único botão redondo azul, alto. Uma criança sem rosto, na ponta dos pés, estende a mão para ele. Atrás, entrando pela esquerda, um adulto sem rosto, sem expressão de bronca. Nada de tela, jogo ou marca. Clara com botão #002fa7. Escura com botão #497ef7.

### estado

proposta

## problema-assistente

### pagina

Problemas, O assistente de inteligência artificial mudou ou errou. O que posso exigir? Depois do primeiro parágrafo da abertura. Também o cartão.

### formato

16 x 9, abertura

### prioridade

A

### objetivo

Mostrar que o assistente vale porque orienta, e que o erro dele pesa por isso.

### ideia

Uma pessoa caminha seguindo uma lanterna azul que flutua à frente dela. A lanterna aponta para uma ponte que termina no meio.

> O serviço vale não apenas porque responde, mas porque induz o usuário a tratar a resposta como ponto relevante de orientação. (p. 758)

### alt

Pessoa seguindo uma lanterna azul que aponta para uma ponte interrompida.

### legenda

Você confiou porque ele orienta.

### producao

Paisagem aberta com uma ponte de tábuas que termina no meio do vão. Uma figura sem rosto caminha em direção à ponte, e à frente dela flutua uma lanterna em azul em brilho, sem rosto nem robô. Clara com lanterna #3a63d0. Escura com lanterna #a1bdf9.

### estado

proposta

## problema-loja-virtual

### pagina

Problemas, A loja virtual esconde quem é pago e quem é confiável. Isso conta? Depois do primeiro parágrafo da abertura. Também o cartão.

### formato

16 x 9, abertura

### prioridade

A

### objetivo

Mostrar a escolha que a plataforma já pré-interpretou.

### ideia

Um corredor de prateleiras em que alguns produtos estão sob holofotes azuis. Os holofotes estão presos a cabos que sobem para fora do quadro.

> O consumidor não escolhe no vazio, diante de universo transparente e simétrico de ofertas. Ele escolhe dentro de um campo já pré-interpretado pela plataforma. (p. 762)

### alt

Corredor de loja com produtos sob holofotes presos a cabos que sobem para fora do quadro.

### legenda

Quem acendeu essas luzes?

### producao

Corredor de supermercado em perspectiva central, com prateleiras dos dois lados e produtos genéricos sem rótulo. Três ou quatro produtos iluminados por cones de luz azul vindos de cima, de holofotes pendurados em cabos que somem na borda. Clara com luz #3a63d0. Escura com luz #a1bdf9, cones estreitos, sem massa larga.

### estado

proposta

## problema-rede-social

### pagina

Problemas, Meu alcance caiu ou fui punido numa rede social. Tenho o que pedir? Depois do primeiro parágrafo da abertura. Também o cartão.

### formato

16 x 9, abertura

### prioridade

A

### objetivo

Mostrar a voz que continua falando e deixou de ser ouvida.

### ideia

Uma pessoa fala num palco. Um painel de controle no canto vai baixando o volume das caixas de som, uma por uma.

> Os Termos de Serviço da Meta descrevem ambiente em que o uso do Facebook se submete a regras privadas de permanência, visibilidade, compartilhamento, moderação e organização do conteúdo circulante, de modo que a experiência do usuário é mediada por critérios internos de distribuição e gestão da interação social (Facebook, [202-?]). (p. 762)

### alt

Pessoa falando num palco enquanto as caixas de som se apagam uma a uma.

### legenda

Você continua falando. Quem baixou o volume?

### producao

Palco pequeno com uma figura sem rosto falando. Em volta, cinco caixas de som, as da esquerda com ondas azuis, as da direita só em tracejado. No canto inferior, um painel com controles deslizantes, um deles sendo puxado para baixo por uma mão sem corpo. Clara com ondas #002fa7. Escura com ondas #497ef7.

### estado

proposta

## problema-trabalho-por-app

### pagina

Problemas, Trabalho por aplicativo, e a regra mudou. Tenho o que pedir? Depois do primeiro parágrafo da abertura. Também o cartão.

### formato

16 x 9, abertura

### prioridade

A

### objetivo

Mostrar a infraestrutura de possibilidade econômica que muda sob os pés de quem trabalha.

### ideia

Uma pessoa pedala numa esteira. Uma mão de fora do quadro troca a esteira por uma mais íngreme, sem parar.

> O que se fornece, em termos funcionais, é uma infraestrutura privada de possibilidade econômica. (p. 765)

### alt

Pessoa pedalando numa esteira que uma mão inclina sem parar.

### legenda

A estrada é deles. O esforço é seu.

### producao

Figura sem rosto de bicicleta sobre uma esteira longa, de perfil. A esteira é azul chapado. Uma mão sem corpo, vinda da borda de cima, ergue a ponta da esteira, aumentando a inclinação. Sem logotipo, mochila de marca ou celular visível. Clara com esteira #002fa7. Escura com esteira #497ef7.

### estado

proposta

## problema-vendo-na-plataforma

### pagina

Problemas, Vendo numa plataforma. A lei do consumidor me protege? Depois do primeiro parágrafo da abertura. Também o cartão.

### formato

16 x 9, abertura

### prioridade

A

### objetivo

Mostrar que vender não torna a pessoa imune à dependência.

### ideia

Uma banca numa feira, com a lona presa a postes que pertencem a outro. Um poste está sendo afrouxado.

> O seller que depende de ranking, reputação, visibilidade e regras opacas de priorização não se torna imune à tutela consumerista apenas porque vende. (p. 778)

### alt

Banca de feira com a lona presa a postes de outro dono, um deles sendo afrouxado.

### legenda

A banca é sua. Os postes, não.

### producao

Banca de feira com mesa e mercadorias azuis, coberta por lona presa a quatro postes de tinta. Uma mão sem corpo, à direita, afrouxa o parafuso de um poste, e a lona já cede desse lado. A figura da banca, sem rosto, olha para cima. Clara com mercadorias #002fa7. Escura com mercadorias #497ef7.

### estado

proposta

## problema-muita-gente

### pagina

Problemas, Aconteceu com muita gente. Dá para resolver de uma vez? Depois do primeiro parágrafo da abertura. Também o cartão.

### formato

16 x 9, abertura

### prioridade

A

### objetivo

Mostrar que o problema que se repete vem do desenho, e não de cada caso.

### ideia

Uma multidão vista do alto, e cada pessoa tem uma pequena marca azul igual, como se a mesma peça tivesse caído sobre todas.

> Em ambientes de plataforma, a fonte lesiva pode residir no próprio desenho do regime de fornecimento, de modo que a unidade do problema não decorre primariamente da repetição empírica de episódios, mas da permanência de uma estrutura única, reiterável e funcionalmente expansiva de produção de perda, opacidade e assimetria. A lesão, então, não é apenas plural. É arquitetural. (p. 774)

### alt

Multidão vista do alto, com a mesma marca azul em cada pessoa.

### legenda

Não foi com você. Foi com todo mundo.

### producao

Vista de cima, em grade solta, de trinta a quarenta figuras sem rosto em tinta. Sobre o ombro de cada uma, um mesmo pequeno quadrado azul, como uma etiqueta. Linhas tracejadas cinza ligam as etiquetas a um único ponto fora do quadro, no alto. Clara com etiquetas #002fa7. Escura com etiquetas #497ef7 e linhas #a9a49c.

### estado

proposta

# 7. Vinhetas dos onze direitos

Família das vinhetas das portas, com os mesmos formatos e regras. O índice de Seus direitos passa de lista de faixas a grade de cartões, três por linha no computador e um por linha no celular, com a vinheta à esquerda do título. A mesma vinheta abre a página de cada direito, a 96 pixels, ao lado do título. Clara com azul #002fa7 e tinta #211c17 sobre #faf6ef. Escura com azul #497ef7 e tinta #ebe7e1 sobre #17130f.

## direito-a

### pagina

Seus direitos, cartão O que você comprou é produto, mesmo sem nada nas mãos, e a página direitos/a/.

### formato

1 x 1, vinheta

### prioridade

B

### objetivo

Dar ao direito o que você comprou é produto, mesmo sem nada nas mãos um sinal próprio, para que a pessoa o reconheça na grade e o reencontre na página.

### ideia

Uma caixa azul sem fundo, em pé sobre a mesa, com nada dentro. Mesmo assim, ela tem sombra.

> Sempre que a utilidade consumida depender estruturalmente de ambiente administrado, modulado e mutável por governança privada, com impacto sobre acesso, permanência, inteligibilidade ou atualização da experiência, estará configurado o campo de incidência do OIC. (p. 743)

### alt

Caixa azul vazia e sem fundo que projeta sombra.

### producao

Caixa azul sem tampa e sem fundo, vista de três quartos, com uma sombra curta de tinta secundária. É a única vinheta com sombra, porque a sombra diz que o objeto existe.

### estado

proposta

## direito-b

### pagina

Seus direitos, cartão A plataforma não pode montar a experiência para você não entender, e a página direitos/b/.

### formato

1 x 1, vinheta

### prioridade

B

### objetivo

Dar ao direito a plataforma não pode montar a experiência para você não entender um sinal próprio, para que a pessoa o reconheça na grade e o reencontre na página.

### ideia

Um labirinto pequeno visto de cima, com a saída desenhada só em tracejado.

> Sempre que expectativa, percepção de valor, avaliação de risco ou capacidade de contestação dependerem de signos, interfaces, fluxos e trilhas informacionais controlados pelo fornecedor, haverá vulnerabilidade semiótica juridicamente relevante. (p. 744)

### alt

Labirinto visto de cima com a saída em tracejado.

### producao

Labirinto quadrado de linhas de tinta, com um ponto azul no centro e a saída desenhada em tracejado cinza.

### estado

proposta

## direito-c

### pagina

Seus direitos, cartão A informação precisa servir para alguma coisa, e a página direitos/c/.

### formato

1 x 1, vinheta

### prioridade

B

### objetivo

Dar ao direito a informação precisa servir para alguma coisa um sinal próprio, para que a pessoa o reconheça na grade e o reencontre na página.

### ideia

Uma bula enrolada, com uma única linha em azul.

> Sempre que a plataforma substituir legibilidade por excesso textual, dispersão estratégica, fragmentação de trajetórias informacionais ou transparência apenas performática, haverá inadequação do dever de informar. (p. 744)

### alt

Papel enrolado com uma única linha azul.

### producao

Rolo de papel aberto pela metade, com linhas de texto sugeridas em tinta e uma única linha em azul chapado.

### estado

proposta

## direito-d

### pagina

Seus direitos, cartão O que foi prometido precisa ser entregue, e a página direitos/d/.

### formato

1 x 1, vinheta

### prioridade

B

### objetivo

Dar ao direito o que foi prometido precisa ser entregue um sinal próprio, para que a pessoa o reconheça na grade e o reencontre na página.

### ideia

Um envelope aberto do qual sai o objeto azul inteiro.

> Sempre que a fruição for precedida por ciclos curados de antecipação, promessa, escassez sugerida, distinção simbólica ou equivalências insinuadas, a publicidade integrará materialmente a oferta. (p. 744-745)

### alt

Envelope aberto com um objeto azul inteiro saindo dele.

### producao

Envelope aberto de frente, com uma estrela azul saindo pela aba, inteira e do mesmo tamanho do envelope.

### estado

proposta

## direito-e

### pagina

Seus direitos, cartão Mudança relevante precisa deixar rastro, e a página direitos/e/.

### formato

1 x 1, vinheta

### prioridade

B

### objetivo

Dar ao direito mudança relevante precisa deixar rastro um sinal próprio, para que a pessoa o reconheça na grade e o reencontre na página.

### ideia

Pegadas azuis que atravessam o quadro.

> Sempre que alterações relevantes de acesso, desempenho, utilidade, regra de funcionamento ou sanção incidirem sobre a fruição sem preservação de trilhas mínimas de reconstrução institucional, haverá violação do parâmetro de auditabilidade aberta. (p. 745)

### alt

Pegadas azuis atravessando o quadro.

### producao

Quatro pegadas pequenas em azul, em diagonal, do canto de baixo à esquerda ao canto de cima à direita.

### estado

proposta

## direito-f

### pagina

Seus direitos, cartão Mudou, tem que manter o que valia, e a página direitos/f/.

### formato

1 x 1, vinheta

### prioridade

B

### objetivo

Dar ao direito mudou, tem que manter o que valia um sinal próprio, para que a pessoa o reconheça na grade e o reencontre na página.

### ideia

Um vaso consertado, com as emendas em azul.

> Sempre que a plataforma alterar a experiência de modo a degradar, esvaziar ou desviar substancialmente a função que justificou a aquisição, haverá ruptura da equivalência de valor funcional. (p. 745)

### alt

Vaso consertado com emendas azuis.

### producao

Vaso simples em tinta, com duas linhas de emenda em azul que seguem o desenho do vaso, como o reparo que mantém o valor.

### estado

proposta

## direito-g

### pagina

Seus direitos, cartão Punição precisa de motivo e de chance de defesa, e a página direitos/g/.

### formato

1 x 1, vinheta

### prioridade

B

### objetivo

Dar ao direito punição precisa de motivo e de chance de defesa um sinal próprio, para que a pessoa o reconheça na grade e o reencontre na página.

### ideia

Um martelo de juiz pousado sobre um livro aberto.

> Sempre que acesso, permanência, visibilidade ou contestação forem condicionados por sanções opacas, fricções seletivas, custos de reação excessivos ou mecanismos assimétricos de reversão, haverá indício de governança abusiva do vínculo. (p. 746)

### alt

Martelo de juiz pousado sobre um livro aberto.

### producao

Martelo de madeira pousado sobre um livro aberto. O livro é azul, e o martelo em tinta, para dizer que a regra vem antes do golpe.

### estado

proposta

## direito-h

### pagina

Seus direitos, cartão Quando a perda é regra, o problema é o desenho, e a página direitos/h/.

### formato

1 x 1, vinheta

### prioridade

B

### objetivo

Dar ao direito quando a perda é regra, o problema é o desenho um sinal próprio, para que a pessoa o reconheça na grade e o reencontre na página.

### ideia

Uma planta de arquitetura com um degrau faltando, marcado em azul.

> Sempre que microfricções, perdas normalizadas, urgências fabricadas, escassezes artificiais, opacidade estratégica, equivalências elásticas e outros mecanismos operarem de modo coordenado para extrair valor da vulnerabilidade ou degradar a fruição como rotina do ambiente, haverá hipótese de teleologia abusiva. (p. 746)

### alt

Planta de escada com um degrau faltando, marcado em azul.

### producao

Planta técnica de uma escada vista de lado, em tracejado cinza, com o lugar de um degrau ausente marcado por um retângulo azul vazado.

### estado

proposta

## direito-i

### pagina

Seus direitos, cartão A prova que está com a plataforma tem que aparecer, e a página direitos/i/.

### formato

1 x 1, vinheta

### prioridade

B

### objetivo

Dar ao direito a prova que está com a plataforma tem que aparecer um sinal próprio, para que a pessoa o reconheça na grade e o reencontre na página.

### ideia

Uma gaveta entreaberta com fichas azuis aparecendo.

> Sempre que a plataforma concentrar os elementos essenciais para narrar, demonstrar e reconstruir o conflito, a disciplina probatória deverá reconhecer que a verificabilidade integra o próprio regime legítimo do fornecimento. (p. 747)

### alt

Gaveta entreaberta com fichas azuis aparecendo.

### producao

Gaveta de arquivo puxada até a metade, de frente, com fichas em azul chapado saindo da borda.

### estado

proposta

## direito-j

### pagina

Seus direitos, cartão Ser dona da obra não é desculpa para tudo, e a página direitos/j/.

### formato

1 x 1, vinheta

### prioridade

B

### objetivo

Dar ao direito ser dona da obra não é desculpa para tudo um sinal próprio, para que a pessoa o reconheça na grade e o reencontre na página.

### ideia

Uma coroa pequena dentro de um círculo de linha fina, como um limite.

> Sempre que a plataforma invocar titularidade exclusiva, segredo empresarial, licenciamento ou estrutura proprietária do ecossistema para resistir ao controle do modo de fornecimento, a compatibilização deverá ser feita à luz da função social e dos limites constitucionais do exercício das posições privadas. (p. 747)

### alt

Coroa dentro de um círculo de linha fina.

### producao

Coroa simples em tinta, centrada, envolvida por um círculo fino azul que não encosta nela.

### estado

proposta

## direito-k

### pagina

Seus direitos, cartão A resposta deve recompor o que você perdeu, e a página direitos/k/.

### formato

1 x 1, vinheta

### prioridade

B

### objetivo

Dar ao direito a resposta deve recompor o que você perdeu um sinal próprio, para que a pessoa o reconheça na grade e o reencontre na página.

### ideia

Duas metades de um objeto azul se reencaixando.

> Sempre que a lesão atingir acesso, continuidade, equivalência, histórico, posição relacional ou densidade significativa da fruição, a resposta jurídica deverá priorizar recomposição funcional, reservando indenização pecuniária para hipóteses de inviabilidade ou insuficiência da restauração. (p. 748)

### alt

Duas metades de um objeto azul se encaixando.

### producao

Uma estrela azul partida em duas metades, levemente afastadas, com duas setas curtas de tinta indicando o reencaixe.

### estado

proposta

# 8. Versão escura do acervo

As 29 peças publicadas mantêm a versão clara. A versão escura é desenhada de novo, a partir da clara, e substitui o negativo calculado. O pedido é o mesmo para todas, com a peça clara anexada, mais a nota própria de cada uma.

Pedido comum. Anexe a ilustração clara. Mesma composição, mesmas linhas, mesmo enquadramento e mesmas figuras. Troque só as cores pela tabela da seção 2.2. O fundo vira #17130f, o traço vira #ebe7e1, a hachura e o tracejado viram #a9a49c e o azul do objeto vira #497ef7. Céu, parede e chão ficam no fundo, sugeridos pelo traço, e nenhuma massa chapada passa de um quinto da área. Onde a clara usa luz pelo papel em branco, a escura usa #a1bdf9. Sem texto, sem logotipo, sem rubrica vermelha.

## inicio-escuro

Lugar. Página inicial, logo depois do título e dos atalhos, antes da narrativa da compra.

Formato. 16 x 9, igual à clara.

O que a versão escura precisa preservar. Uma figura com uma armadura inventada e brilhante está de pé sobre um pedaço de chão que flutua, sustentado por cabos que sobem para fora do quadro. Parece terreno dela, mas é um chão emprestado.

Estado. proposta

## parte-a-compra-escuro

Lugar. Percurso, parte 1, A compra, na abertura.

Formato. 16 x 9, igual à clara.

O que a versão escura precisa preservar. Alguém recebe uma caixa de presente com uma peça de armadura dentro. A peça chega às mãos de quem comprou, mas a fita da caixa é um cordão comprido que volta para a loja e não se solta.

Estado. proposta

## imagem-catraca-escuro

Lugar. Percurso, parte 1, A compra, depois do bloco Uma imagem da catraca.

Formato. 4 x 3, igual à clara.

O que a versão escura precisa preservar. Uma catraca na entrada de um jardim. Do lado de dentro, a figura de armadura brilhante. A catraca não fica na saída, fica no caminho de quem quer continuar lá dentro. A figura existe e é de quem a comprou, e a catraca só controla as condições de uso.

Estado. proposta

## imagem-estoque-fluxo-escuro

Lugar. Percurso, parte 1, A compra, depois do bloco Uma imagem da gaveta e do cano.

Formato. 4 x 3, igual à clara.

O que a versão escura precisa preservar. À esquerda, uma gaveta com moedas paradas. À direita, um cano transparente com água correndo e uma peça de armadura levada pela corrente. Se a torneira fecha, a peça para, inteira, e perde o brilho.

Estado. proposta

## parte-o-desejo-escuro

Lugar. Percurso, parte 2, O desejo, na abertura.

Formato. 16 x 9, igual à clara.

O que a versão escura precisa preservar. Uma figura de armadura no centro de uma roda de silhuetas. O brilho da armadura não vem dela, vem dos olhares das pessoas em volta, que se cruzam e acendem a peça. Onde nenhum olhar alcança, a armadura fica fosca.

Estado. proposta

## parte-o-dono-escuro

Lugar. Percurso, parte 3, O dono, na abertura.

Formato. 16 x 9, igual à clara.

O que a versão escura precisa preservar. Um castelo feito de blocos de servidores sobre nuvens. Lá embaixo, pessoas jogam, e cada gesto delas sobe como um tijolo que aumenta o castelo. No alto, uma única janela acesa guarda o painel de onde se decide quanto tudo vale.

Estado. proposta

## imagem-torneira-escuro

Lugar. Percurso, parte 3, O dono, depois do bloco Uma imagem da torneira.

Formato. 4 x 3, igual à clara.

O que a versão escura precisa preservar. Uma torneira pingando. Cada gota carrega um objeto mínimo, uma moeda, um relógio pequeno, um coração pequeno, e o balde embaixo já está quase cheio.

Estado. proposta

## parte-as-regras-escuro

Lugar. Percurso, parte 4, As regras, na abertura.

Formato. 16 x 9, igual à clara.

O que a versão escura precisa preservar. Um labirinto visto de cima cujas paredes são páginas de um contrato em pé e telas acesas. Na única saída, uma mão segura um carimbo. O texto vira parede, e a parede vira punição.

Estado. proposta

## parte-o-normal-escuro

Lugar. Percurso, parte 5, O normal, na abertura.

Formato. 16 x 9, igual à clara.

O que a versão escura precisa preservar. Nuvens penduradas por fios num andaime, como cenário de teatro, e chuva caindo sobre pessoas de guarda-chuva que olham para baixo e não veem os fios.

Estado. proposta

## parte-a-mudanca-escuro

Lugar. Percurso, parte 6, A mudança, na abertura.

Formato. 16 x 9, igual à clara.

O que a versão escura precisa preservar. A mesma armadura duas vezes, lado a lado. A da esquerda está inteira. A da direita tem o mesmo contorno, mas por dentro está oca, só a linha do desenho.

Estado. proposta

## parte-o-desenho-escuro

Lugar. Percurso, parte 7, O desenho, na abertura.

Formato. 16 x 9, igual à clara.

O que a versão escura precisa preservar. A planta baixa de uma loja em que todos os corredores, por caminhos diferentes, acabam no mesmo caixa. As linhas escondidas do projeto, com os pontos de atrito e a saída oculta atrás das prateleiras, aparecem em tracejado.

Estado. proposta

## parte-a-lei-escuro

Lugar. Percurso, parte 8, A lei, na abertura.

Formato. 16 x 9, igual à clara.

O que a versão escura precisa preservar. Uma construção contemporânea vista em corte, sustentada por uma fundação anterior, já demarcada e pronta para receber suas estruturas. O azul destaca a construção imaterial e o traço revela a continuidade com a fundação. É o mesmo terreno da ilustração do Objeto Imaterial de Consumo, agora com a obra pronta.

Estado. proposta

## parte-a-resposta-escuro

Lugar. Percurso, parte 9, A resposta, na abertura.

Formato. 16 x 9, igual à clara.

O que a versão escura precisa preservar. Uma mão devolve a peça que faltava num mosaico, enquanto uma pilha arrumada de moedas fica ao lado, ao alcance.

Estado. proposta

## parte-alem-do-jogo-escuro

Lugar. Percurso, parte 10, Além do jogo, na abertura.

Formato. 16 x 9, igual à clara.

O que a versão escura precisa preservar. Um controle de videogame, um balão de conversa, um carrinho de compras, uma bolsa de entrega e um rosto sorridente de interface, todos presos por fios que descem para a mesma estrutura escondida no chão.

Estado. proposta

## parte-o-nome-escuro

Lugar. Percurso, parte 11, O nome, na abertura.

Formato. 16 x 9, igual à clara.

O que a versão escura precisa preservar. Ísis diante de Rá, o deus Sol, em traço que lembra a pintura egípcia sem copiar obra existente. Aos pés do Sol, uma serpente pequena feita da mesma luz dele.

Estado. proposta

## ideia-oic-escuro

Lugar. Objeto Imaterial de Consumo, depois de Isso tem nome.

Formato. 16 x 9, igual à clara.

O que a versão escura precisa preservar. Um terreno vazio demarcado com estacas e barbante, coberto de mato, e no meio dele a estrutura de uma construção começando a subir. É uma armação aberta, sem paredes, e no alto dela está a figura de armadura.

Estado. proposta

## ideia-feixe-de-fruicao-governada-escuro

Lugar. Feixe de fruição governada, depois de Isso tem nome.

Formato. 16 x 9, igual à clara.

O que a versão escura precisa preservar. Um feixe de fios de cores e espessuras diferentes, preso embaixo pela mão de quem usa e em cima por um mecanismo de roldanas que puxa, solta e corta cada fio.

Estado. proposta

## ideia-lex-plataformae-escuro

Lugar. Lex Plataformae, depois de Isso tem nome.

Formato. 16 x 9, igual à clara.

O que a versão escura precisa preservar. Um livro de regras aberto cujas páginas, vistas por trás, são engrenagens funcionando sozinhas. Ninguém vira as páginas, e o livro roda.

Estado. proposta

## ideia-vulnerabilidade-semiotica-escuro

Lugar. Vulnerabilidade semiótica, depois de Isso tem nome.

Formato. 16 x 9, igual à clara.

O que a versão escura precisa preservar. Uma pessoa atenta lê com cuidado um cartão coberto de sinais nítidos. A lente que dá sentido aos sinais fica do outro lado de um balcão, na mão de quem atende, que não a empresta. Atrás do balcão, a mesma etiqueta pende de dois objetos diferentes.

Estado. proposta

## ideia-teleologia-abusiva-escuro

Lugar. Teleologia abusiva, depois de Isso tem nome.

Formato. 16 x 9, igual à clara.

O que a versão escura precisa preservar. Uma escada vista de lado, com saídas laterais em cada patamar e uma vitrine iluminada no topo. O degrau mais alto está sempre logo antes de cada saída e nunca no caminho para a vitrine. Uma régua encostada mostra que a diferença se repete, sempre no mesmo lugar.

Estado. proposta

## ideia-ilicito-de-arquitetura-escuro

Lugar. Ilícito de arquitetura, depois de Isso tem nome.

Formato. 16 x 9, igual à clara.

O que a versão escura precisa preservar. Um prédio em corte com escadas que só descem, portas que só abrem para dentro, janelas pintadas na parede, a saída de emergência atrás de três portas trancadas e um corredor que volta ao começo. Nenhuma placa proíbe nada, e o desenho prende.

Estado. proposta

## ideia-antecipacao-hipercuratorial-escuro

Lugar. Antecipação hipercuratorial, depois de Isso tem nome.

Formato. 16 x 9, igual à clara.

O que a versão escura precisa preservar. Uma sala de espera com cadeiras ocupadas e um relógio na parede. Por baixo de uma porta fechada vaza uma luz forte, e todos olham para ela. A luz é regulada por uma mão que sai pela fresta da porta, a mesma que move os ponteiros do relógio por um fio.

Estado. proposta

## ideia-auditabilidade-aberta-escuro

Lugar. Auditabilidade aberta, depois de Isso tem nome.

Formato. 16 x 9, igual à clara.

O que a versão escura precisa preservar. Uma caixa preta fechada com uma janela recortada num canto, por onde se veem algumas engrenagens. Não a caixa inteira aberta, só o bastante para ver o que mudou. Do lado de fora, preso à caixa, um livro de registro aberto, e mais de uma pessoa consegue olhar pela janela.

Estado. proposta

## ideia-equivalencia-de-valor-funcional-escuro

Lugar. Equivalência de valor funcional, depois de Isso tem nome.

Formato. 16 x 9, igual à clara.

O que a versão escura precisa preservar. Uma balança de dois pratos com a mesma peça de armadura em cada um, a de antes e a de depois, idênticas por fora. A de depois é um pouco mais fosca, e o prato dela sobe, porque ela pesa menos.

Estado. proposta

## laboratorio-escuro

Lugar. Laboratório, depois da abertura.

Formato. 16 x 9, igual à clara.

O que a versão escura precisa preservar. Uma lupa sobre quatro telas diferentes, a de um assistente, a de uma loja, a de um aplicativo de entrega e a de um atendimento, e sob a lente as quatro mostram a mesma engrenagem. Fora da lente, cada tela mantém a sua aparência.

Estado. proposta

## familia-funcionalidade-cognitiva-escuro

Lugar. Laboratório, funcionalidade cognitiva, depois do resumo.

Formato. 4 x 3, igual à clara.

O que a versão escura precisa preservar. Um balão de conversa seguro pela mão de quem usa, com um botão de regular intensidade, como os de luz, girado por outra mão, que vem de fora do quadro.

Estado. proposta

## familia-infraestrutura-e-intermediacao-escuro

Lugar. Laboratório, infraestrutura e intermediação, depois do resumo.

Formato. 4 x 3, igual à clara.

O que a versão escura precisa preservar. Uma vitrine vista através de várias lentes empilhadas, cada uma escondendo ou aumentando uma parte do que está à venda.

Estado. proposta

## familia-produtividade-gig-economy-escuro

Lugar. Laboratório, produtividade sob a gig economy, depois do resumo.

Formato. 4 x 3, igual à clara.

O que a versão escura precisa preservar. Um mapa de cidade em que a rota de uma bicicleta de entrega é desenhada por uma mão enorme, com estrelas de avaliação flutuando sobre o caminho.

Estado. proposta

## familia-administracao-de-confianca-escuro

Lugar. Laboratório, administração de confiança, depois do resumo.

Formato. 4 x 3, igual à clara.

O que a versão escura precisa preservar. Uma capa macia e arredondada, com um rosto sorridente de interface, cobrindo a quina de uma mesa. A capa amortece de verdade, mas marcas no chão mostram que a mesa avança um pouco a cada dia sobre o caminho de quem passa.

Estado. proposta

# 9. Ordem de produção

A geração acontece numa mesma sessão, na ordem abaixo, para que cada família saia homogênea e cada peça nova já tenha a vizinha como referência.

Primeiro as seis vinhetas das portas, juntas, e logo as onze dos direitos, que são da mesma família. Depois a folha canônica da armadura em versão escura, que serve de referência às peças escuras com armadura. Depois as 29 versões escuras do acervo, na ordem do Caminho, das ideias e de Plataformas. Depois as três aberturas das páginas de entrada, direitos-continua, alem-do-consumo e como-reclamar. Por último as 24 aberturas de problema, agrupadas pelas seis portas.

Ao fim de cada família, as peças são vistas lado a lado nas duas versões, e só então seguem para os critérios de aceite. O autor vê cada lote no ar.

# 10. Ajustes no site quando as peças chegarem

A peça inicio sai da capa da Informação e da Doutrina e fica na Ciência e no Caminho. As vinhetas entram na capa, em problemas, na lateral dos problemas, no índice de Seus direitos e em cada página de direito. Seus direitos passa a grade de cartões. O filtro de negativo parcial sai de `site/extra.css` quando a última versão escura desenhada entrar, e `ferramentas/negativo.py` fica só como reserva. Os cartões de compartilhamento das 24 páginas de problema passam a usar a abertura. Legendas e textos alternativos vão para a tradução inglesa no mesmo passo.
