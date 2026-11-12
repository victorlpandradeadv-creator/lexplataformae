# Ilustrações conceituais

Plano das peças ilustrativas que o site vai receber quando a estrutura estiver pronta. Orientação do autor de 27/10/2026. As peças serão produzidas com IA e entram nos lugares previstos aqui. Plano do Claude, à espera da revisão do autor. Em 27/10/2026, a direção de arte passou para a paleta aprovada, e duas peças foram refeitas. A da compra deixou de dizer que nada sai da loja, e a da teleologia abusiva deixou de sugerir intenção.

Em 12/11/2026, por ordem do autor de consolidar a estrutura antes da produção, cada peça passou a separar três informações. A ideia descreve o que a figura representa e é o único texto que aparece no lugar previsto, no modo Ciência. A legenda e o texto alternativo acompanham a figura pronta. O campo producao guarda as instruções para quem gera a imagem e nunca vai ao site. Na mesma data entraram as revisões de composição discutidas com o autor, todas conferidas contra o trecho que cada peça ilustra.

Cada peça tem um endereço fixo no site. Enquanto o arquivo não existe, o lugar aparece só no degrau Despir, como contorno tracejado com a etiqueta "ilustração prevista". Quando o arquivo chega em `site/ilustracoes/`, o gerador põe a figura no lugar, com o texto alternativo e a legenda daqui, sem mexer em mais nada.

Como toda frase explicativa do site, cada peça se ancora num trecho da tese, conferido por script junto com os demais (`python3 ferramentas/conferir_citacoes.py estrutura/ilustracoes.md`). A ilustração mostra a ideia do trecho. Não acrescenta afirmação nova.

# Direção de arte

Direção editorial revista em 10/11/2026. A família de imagens revela a estrutura que sustenta o objeto e acompanha o papel claro, os títulos serifados e a rubrica já adotados no site.

- Cada peça é uma metáfora visual da ideia, com poucos elementos e muito espaço vazio. As aberturas do caminho são cenas editoriais. Os conceitos mostram relações e mecanismos, sem repetir a cena narrativa.
- Traço de ilustração editorial, com linha fina e volumes chapados, sem fotorrealismo, sem brilho de videogame e sem estética de anúncio.
- Paleta do próprio site, refeita em 27/10/2026 sobre as cores aprovadas pelo autor. Fundo no papel quente do modo Informação (#faf6ef) e traço em tinta escura (#211c17). O azul Klein da tese (#002fa7), sempre chapado, marca só o que foi comprado ou prometido, como a armadura, o item ou o terreno. A estrutura escondida, como fios, engrenagens e linhas de projeto, vem em traço tracejado cinza (#615953), do jeito que a estrutura aparece no modo Ciência. Nenhuma cor de área entra nas ilustrações, porque as áreas são estrutura do modo Ciência.
- Nenhum texto dentro da imagem. Nada de palavras, números, logotipos, marcas, interfaces reais ou símbolos de empresas.
- Nenhum personagem, skin, mapa, item ou elemento visual de jogo real. A skin é sempre uma roupa ou armadura inventada, sem semelhança com personagens existentes. Nenhuma pessoa real.
- Pessoas aparecem como silhuetas ou figuras sem rosto definido, de idades e corpos variados.
- O site segue o aparelho e tem modo escuro desde 10/11/2026. Traço escuro sobre fundo transparente some no tema escuro, e por isso cada peça leva o papel quente do site como fundo próprio. A versão escura é opcional. Quando `<id>-escuro.webp` existe, o gerador a mostra no tema escuro e a clara no tema claro, inclusive quando o leitor troca o tema pelo botão.
- Perspectiva controlada, contornos precisos, hachuras discretas e poucas massas de cor. A aparência do objeto ocupa o primeiro plano e seus suportes ficam legíveis no segundo. Nenhuma textura atrás do texto da página.
- A rubrica vermelha (#b3161c) pertence à interface. O azul Klein permanece reservado ao objeto comprado ou prometido nas ilustrações. A unidade vem do desenho e da composição, sem alterar as cores científicas por área.
- A estrutura escondida das peças, inclusive as linhas de projeto da planta da loja, vem sempre em tracejado cinza. Nenhuma peça usa laranja.
- A armadura é uma só em todas as peças em que aparece (inicio, parte-a-compra, imagem-catraca, imagem-estoque-fluxo, parte-o-desejo, parte-a-mudanca, ideia-oic e ideia-equivalencia-de-valor-funcional). Antes delas sai a folha canônica, que fica em `estrutura/referencias-visuais/armadura.webp` e não vai ao site. A folha fixa silhueta, proporções, componentes e material, com frente, costas, perfil, vista parcial e luz variada, e os estados inteira, fosca, oca e peça isolada. A armadura é inventada, chapada no azul Klein, e continua reconhecível mesmo quando perde o que a torna valiosa.
- parte-a-lei e ideia-oic formam um díptico, porque ilustram o mesmo trecho da p. 24-25. O terreno, a fundação, o contorno e os marcos são idênticos nas duas.
- A cena do curso que corta metade das aulas e continua cobrando o mesmo preço fica como candidata à página da equivalência de valor funcional, onde o texto usa essa imagem. Ela só entra no plano quando o texto da página estiver consolidado.
- Ísis e Rá recebem composição mais solene, com maior espaço e escala, mantendo o mesmo traço. As HQs das epígrafes formam uma coleção artística separada.

# Especificação técnica

- Arquivo em `site/ilustracoes/<id>.webp`, com o id desta lista. A versão para modo escuro, se houver, fica em `site/ilustracoes/<id>-escuro.webp`.
- Peça de abertura de página na proporção 16 x 9, com 1600 por 900 pixels. Peça dentro do texto na proporção 4 x 3, com 1200 por 900 pixels. Até 250 KB por arquivo.
- O texto alternativo e a legenda saem daqui e passam pela leitura do autor.
- A procedência fica registrada no campo `procedencia` de cada peça quando ela for inserida, com a ferramenta, a data e o pedido usado. É a auditabilidade do próprio site.
- Legenda de transparência proposta para todas as peças, decisão do autor. "Ilustração conceitual feita com IA."
- Estados possíveis. prevista, encomendada, pronta e publicada.

# Peças

Prioridade A são as aberturas da página inicial, das onze partes do caminho e das nove ideias. Prioridade B são as peças dentro do texto e as de Plataformas. A primeira sequência de produção reúne inicio, parte-a-compra, parte-a-mudanca, parte-o-desenho e parte-o-nome. As peças continuam previstas até que os arquivos sejam efetivamente produzidos e conferidos.

## inicio

### pagina

Página inicial, logo depois do título e dos atalhos, antes da narrativa da compra.

### formato

16 x 9

### prioridade

A

### ideia

Uma figura com uma armadura inventada e brilhante está de pé sobre um pedaço de chão que flutua, sustentado por cabos que sobem para fora do quadro. Parece terreno dela, mas é um chão emprestado.

> A travessia realizada neste trabalho começou pela constatação de que existe um tipo de consumo em que o sujeito imagina estar em terreno próprio, mas só se move dentro de um chão concedido, revogável e reconfigurável. (p. 791)

### alt

Figura com armadura brilhante de pé sobre um pedaço de chão que flutua, preso por cabos que sobem para fora da imagem.

### legenda

Parece terreno seu, mas é chão emprestado.

### producao

Cena serena, sem ameaça nem queda. Os cabos sobem tensos e nenhuma mão os segura. Primeira aparição da armadura canônica.

### estado

prevista

## parte-a-compra

### pagina

Percurso, parte 1, A compra, na abertura.

### formato

16 x 9

### prioridade

A

### ideia

Alguém recebe uma caixa de presente com uma peça de armadura dentro. A peça chega às mãos de quem comprou, mas a fita da caixa é um cordão comprido que volta para a loja e não se solta.

> Campeões, skins, emotes e moeda do jogo integram o catálogo de bens que só se tornam fruíveis como licença de acesso associada à conta, e não como coisas transportáveis para fora dela (p. 408)

### alt

Mãos recebem uma caixa de presente cuja fita é um cordão comprido que volta para dentro de uma loja.

### legenda

Chegou até você, mas continua preso à loja.

### producao

A peça que sai da caixa é o elmo da armadura canônica. O cordão não pode parecer corrente nem algema. Nada escrito na caixa.

### estado

prevista

## imagem-catraca

### pagina

Percurso, parte 1, A compra, depois do bloco Uma imagem da catraca.

### formato

4 x 3

### prioridade

B

### ideia

Uma catraca na entrada de um jardim. Do lado de dentro, a figura de armadura brilhante. A catraca não fica na saída, fica no caminho de quem quer continuar lá dentro. A figura existe e é de quem a comprou, e a catraca só controla as condições de uso.

> como forma de mercadoria cuja fruição é subordinada a catracas contratuais e tecnológicas (p. 186)

### alt

Catraca na entrada de um jardim, com uma figura de armadura brilhante do lado de dentro.

### legenda

O que você comprou existe, mas só se usa do lado de dentro.

### producao

O jardim é aberto e continua além do quadro. A grade não pode lembrar prisão, e a figura fica à vontade.

### estado

prevista

## imagem-estoque-fluxo

### pagina

Percurso, parte 1, A compra, depois do bloco Uma imagem da gaveta e do cano.

### formato

4 x 3

### prioridade

B

### ideia

À esquerda, uma gaveta com moedas paradas. À direita, um cano transparente com água correndo e uma peça de armadura levada pela corrente. Se a torneira fecha, a peça para, inteira, e perde o brilho.

> O valor de uso do feixe, nessa condição, não é estoque, é fluxo. (p. 409)

### alt

Gaveta com moedas paradas ao lado de um cano transparente em que uma peça de armadura é levada pela água.

### legenda

O valor da skin não fica guardado, ele corre.

### producao

No trecho seco do cano, a peça fica inteira, só sem brilho. Ela não quebra nem some.

### estado

prevista

## parte-o-desejo

### pagina

Percurso, parte 2, O desejo, na abertura.

### formato

16 x 9

### prioridade

A

### ideia

Uma figura de armadura no centro de uma roda de silhuetas. O brilho da armadura não vem dela, vem dos olhares das pessoas em volta, que se cruzam e acendem a peça. Onde nenhum olhar alcança, a armadura fica fosca.

> o espetáculo não é conjunto de imagens, mas relação social entre pessoas mediada por imagens (p. 282)

### alt

Figura de armadura no centro de uma roda de silhuetas cujos olhares acendem o brilho da peça.

### legenda

O valor se acende no olhar dos outros.

### producao

As silhuetas não formam plateia hostil nem torcida de jogo real. As linhas dos olhares vão em tracejado.

### estado

prevista

## parte-o-dono

### pagina

Percurso, parte 3, O dono, na abertura.

### formato

16 x 9

### prioridade

A

### ideia

Um castelo feito de blocos de servidores sobre nuvens. Lá embaixo, pessoas jogam, e cada gesto delas sobe como um tijolo que aumenta o castelo. No alto, uma única janela acesa guarda o painel de onde se decide quanto tudo vale.

> Daí a força da imagem feudal: consumidores e usuários tornam-se “servos da nuvem” não porque deixam de consumir, mas porque sua participação passa a reproduzir o próprio capital que os governa. (p. 146)

### alt

Castelo de servidores sobre nuvens que cresce com tijolos levados pelas pessoas que jogam lá embaixo.

### legenda

Cada vez que você participa, o castelo cresce.

### producao

As pessoas jogam à vontade. Nada de correntes ou de esforço de carregar blocos, que dariam leitura de trabalho forçado.

### estado

prevista

## imagem-torneira

### pagina

Percurso, parte 3, O dono, depois do bloco Uma imagem da torneira.

### formato

4 x 3

### prioridade

B

### ideia

Uma torneira pingando. Cada gota carrega um objeto mínimo, uma moeda, um relógio pequeno, um coração pequeno, e o balde embaixo já está quase cheio.

> O motor de muitos ecossistemas digitais não é apenas a cobrança ostensiva, mas a drenagem por microeventos, microdecisões e microperdas, distribuídas em escala e diluídas a ponto de se tornarem quase invisíveis, embora cumulativamente relevantes. (p. 26)

### alt

Torneira pingando gotas que carregam moedas, relógios e corações pequenos num balde quase cheio.

### legenda

Gota a gota, a conta chega.

### estado

prevista

## parte-as-regras

### pagina

Percurso, parte 4, As regras, na abertura.

### formato

16 x 9

### prioridade

A

### ideia

Um labirinto visto de cima cujas paredes são páginas de um contrato em pé e telas acesas. Na única saída, uma mão segura um carimbo. O texto vira parede, e a parede vira punição.

> A regra interna só ganha densidade normativa quando se converte em condições de possibilidade por arquitetura e em consequências por enforcement. (p. 365)

### alt

Labirinto visto de cima com paredes feitas de páginas de contrato e de telas, e uma mão com um carimbo na saída.

### legenda

O texto vira parede, e a parede vira punição.

### producao

Nenhum texto legível nas páginas nem nas telas. O carimbo representa o enforcement do trecho da p. 365.

### estado

prevista

## parte-o-normal

### pagina

Percurso, parte 5, O normal, na abertura.

### formato

16 x 9

### prioridade

A

### ideia

Nuvens penduradas por fios num andaime, como cenário de teatro, e chuva caindo sobre pessoas de guarda-chuva que olham para baixo e não veem os fios.

> Ela fabrica fatos do consumo como quem fabrica clima em sequência previsível, com justificativa superficial e aparência de estrita normalidade. (p. 32)

### alt

Nuvens presas por fios a um andaime fazem chover sobre pessoas de guarda-chuva que não olham para cima.

### legenda

Ninguém reclama da chuva, e ela foi fabricada.

### producao

Os fios e o andaime ficam nítidos para quem olha a imagem. As pessoas da cena olham para baixo.

### estado

prevista

## parte-a-mudanca

### pagina

Percurso, parte 6, A mudança, na abertura.

### formato

16 x 9

### prioridade

A

### ideia

A mesma armadura duas vezes, lado a lado. A da esquerda está inteira. A da direita tem o mesmo contorno, mas por dentro está oca, só a linha do desenho.

> Um objeto pode continuar existindo e, ainda assim, já não ser, em sentido jurídico relevante, aquilo que foi adquirido. (p. 795)

### alt

Duas armaduras iguais lado a lado, a primeira inteira e a segunda só com o contorno, oca por dentro.

### legenda

Continua na conta, mas já não é a mesma.

### producao

A perda é por dentro. A armadura oca não fica quebrada nem enferrujada, e o contorno é idêntico ao da inteira.

### estado

prevista

## parte-o-desenho

### pagina

Percurso, parte 7, O desenho, na abertura.

### formato

16 x 9

### prioridade

A

### ideia

A planta baixa de uma loja em que todos os corredores, por caminhos diferentes, acabam no mesmo caixa. As linhas escondidas do projeto, com os pontos de atrito e a saída oculta atrás das prateleiras, aparecem em tracejado.

> Ela tende a emergir como programa de funcionamento (p. 670)

### alt

Planta baixa de uma loja em que todos os corredores levam ao mesmo caixa, com linhas de projeto em destaque.

### legenda

Cada peça parece banal, mas juntas formam um programa.

### producao

As linhas escondidas vão em tracejado cinza, pela regra geral da direção de arte. Planta genérica, sem loja real.

### estado

prevista

## parte-a-lei

### pagina

Percurso, parte 8, A lei, na abertura.

### formato

16 x 9

### prioridade

A

### ideia

Uma construção contemporânea vista em corte, sustentada por uma fundação anterior, já demarcada e pronta para receber suas estruturas. O azul destaca a construção imaterial e o traço revela a continuidade com a fundação. É o mesmo terreno da ilustração do Objeto Imaterial de Consumo, agora com a obra pronta.

> O Objeto Imaterial de Consumo (OIC) apresenta-se, nesse sentido, como o loteamento definitivo de um terreno que o legislador de 1990 já havia demarcado, embora a doutrina contemporânea o tenha mantido na condição de um terreno baldio. (p. 24-25)

### alt

Construção contemporânea em corte, com estruturas azuis apoiadas numa fundação anterior e demarcada.

### legenda

A construção se apoia no espaço que a lei já havia aberto em 1990.

### producao

Díptico com ideia-oic. O terreno, a fundação, o contorno e os marcos são idênticos nas duas peças, e a primeira gerada serve de referência para a segunda. O marco de 1990 fica na legenda, sem números dentro da imagem.

### estado

prevista

## parte-a-resposta

### pagina

Percurso, parte 9, A resposta, na abertura.

### formato

16 x 9

### prioridade

A

### ideia

Uma mão devolve a peça que faltava num mosaico, enquanto uma pilha arrumada de moedas fica ao lado, ao alcance.

> Em hipóteses de lesão arquitetural, a resposta jurídica deve privilegiar recomposição funcional e correção procedimental, em vez de recorrer automaticamente à monetização. (p. 751)

### alt

Mão encaixa a peça que faltava num mosaico, com uma pilha de moedas ao lado.

### legenda

Antes do dinheiro, devolver o que foi tirado.

### producao

As moedas ficam arrumadas e disponíveis, nunca jogadas ou empoeiradas. O trecho da p. 751 afasta a monetização automática, não a indenização.

### estado

prevista

## parte-alem-do-jogo

### pagina

Percurso, parte 10, Além do jogo, na abertura.

### formato

16 x 9

### prioridade

A

### ideia

Um controle de videogame, um balão de conversa, um carrinho de compras, uma bolsa de entrega e um rosto sorridente de interface, todos presos por fios que descem para a mesma estrutura escondida no chão.

> O ponto comum não está na superfície do ambiente, mas na forma pela qual a fruição é governada, a expectativa é administrada, a inteligibilidade é modulada e a contestação é tornada mais ou menos praticável por desenho privado. (p. 787)

### alt

Controle de videogame, balão de conversa, carrinho de compras, bolsa de entrega e rosto sorridente presos por fios à mesma estrutura escondida.

### legenda

Muda o ambiente, mas o jeito de governar é o mesmo.

### producao

Nenhuma interface ou marca reconhecível nos cinco objetos.

### estado

prevista

## parte-o-nome

### pagina

Percurso, parte 11, O nome, na abertura.

### formato

16 x 9

### prioridade

A

### ideia

Ísis diante de Rá, o deus Sol, em traço que lembra a pintura egípcia sem copiar obra existente. Aos pés do Sol, uma serpente pequena feita da mesma luz dele.

> Ísis produz a serpente a partir da substância do próprio Rá e, com isso, transforma o excesso de poder em instrumento de manifestação de seu limite. (p. 792)

### alt

Ísis diante de Rá, o deus Sol, com uma serpente pequena feita da mesma luz aos pés dele.

### legenda

O poder que tem nome pode ser chamado a responder.

### producao

Composição solene, com mais espaço e escala. Sem hieróglifos legíveis e sem cópia de papiro, tumba ou obra conhecida.

### estado

prevista

## ideia-oic

### pagina

Objeto Imaterial de Consumo, depois de Isso tem nome.

### formato

16 x 9

### prioridade

A

### ideia

Um terreno vazio demarcado com estacas e barbante, coberto de mato, e no meio dele a estrutura de uma construção começando a subir. É uma armação aberta, sem paredes, e no alto dela está a figura de armadura.

> O Objeto Imaterial de Consumo (OIC) apresenta-se, nesse sentido, como o loteamento definitivo de um terreno que o legislador de 1990 já havia demarcado, embora a doutrina contemporânea o tenha mantido na condição de um terreno baldio. (p. 24-25)

### alt

Terreno vazio demarcado com estacas e barbante, com uma armação começando a subir no meio e a figura de armadura no alto dela.

### legenda

O espaço estava demarcado desde 1990, só faltava construir.

### producao

Díptico com parte-a-lei, no mesmo terreno. A armação não pode lembrar casa nem lote à venda.

### estado

prevista

## ideia-feixe-de-fruicao-governada

### pagina

Feixe de fruição governada, depois de Isso tem nome.

### formato

16 x 9

### prioridade

A

### ideia

Um feixe de fios de cores e espessuras diferentes, preso embaixo pela mão de quem usa e em cima por um mecanismo de roldanas que puxa, solta e corta cada fio.

> o objeto pode ser descrito como feixe de funcionalidades e significações administradas ao longo da relação, acoplado a permissões e limites de uso, a regimes de visibilidade e ordenação, a métricas e sinais de reconhecimento, e a mecanismos de curadoria e enforcement executados por desenho. (p. 426)

### alt

Feixe de fios seguro por uma mão embaixo e por um mecanismo de roldanas em cima, que puxa e corta os fios.

### legenda

Cada fio do que você comprou passa por cima, pela mão de outro.

### estado

prevista

## ideia-lex-plataformae

### pagina

Lex Plataformae, depois de Isso tem nome.

### formato

16 x 9

### prioridade

A

### ideia

Um livro de regras aberto cujas páginas, vistas por trás, são engrenagens funcionando sozinhas. Ninguém vira as páginas, e o livro roda.

> A expressão Lex Plataformae pretende nomear, portanto, não um conjunto de cláusulas predispostas, mas uma ordenação privada tecnicamente executável, economicamente orientada e semioticamente naturalizada. (p. 27)

### alt

Livro de regras aberto com engrenagens girando atrás das páginas, sem ninguém por perto.

### legenda

Não é um contrato parado, é uma ordem que roda.

### producao

Nada de brasão, balança da justiça ou símbolo de lei estatal. Texto ilegível.

### estado

prevista

## ideia-vulnerabilidade-semiotica

### pagina

Vulnerabilidade semiótica, depois de Isso tem nome.

### formato

16 x 9

### prioridade

A

### ideia

Uma pessoa atenta lê com cuidado um cartão coberto de sinais nítidos. A lente que dá sentido aos sinais fica do outro lado de um balcão, na mão de quem atende, que não a empresta. Atrás do balcão, a mesma etiqueta pende de dois objetos diferentes.

> Há assimetria de sentido, ligada ao controle de códigos de leitura, categorias e classificações que definem o que conta como diferença relevante. (p. 322)

### alt

Pessoa atenta lê um cartão de sinais enquanto, do outro lado do balcão, uma mão guarda a lente que dá sentido a eles.

### legenda

O sentido das coisas está do outro lado do balcão.

### producao

A pessoa é competente e atenta, nunca confusa ou caricata. A fragilidade vem da posição dela, não dela.

### estado

prevista

## ideia-teleologia-abusiva

### pagina

Teleologia abusiva, depois de Isso tem nome.

### formato

16 x 9

### prioridade

A

### ideia

Uma escada vista de lado, com saídas laterais em cada patamar e uma vitrine iluminada no topo. O degrau mais alto está sempre logo antes de cada saída e nunca no caminho para a vitrine. Uma régua encostada mostra que a diferença se repete, sempre no mesmo lugar.

> O segundo requisito é a reprodução como padrão. O desvio não pode ser episódio isolado, erro contingente ou exceção operacional. (p. 448)
> O que se controla não é uma vontade íntima, mas um programa reconhecível (p. 732)

### alt

Escada vista de lado em que o degrau mais alto aparece sempre antes das saídas, e uma régua mede a diferença repetida.

### legenda

Não se procura uma intenção, e sim um programa reconhecível.

### producao

Nenhuma figura armando a escada. A finalidade aparece só pela direção do padrão.

### estado

prevista

## ideia-ilicito-de-arquitetura

### pagina

Ilícito de arquitetura, depois de Isso tem nome.

### formato

16 x 9

### prioridade

A

### ideia

Um prédio em corte com escadas que só descem, portas que só abrem para dentro, janelas pintadas na parede, a saída de emergência atrás de três portas trancadas e um corredor que volta ao começo. Nenhuma placa proíbe nada, e o desenho prende.

> O núcleo do parâmetro está em tratar a arquitetura como conduta. (p. 732)

### alt

Prédio em corte com escadas que só descem, portas que só abrem para dentro e janelas pintadas na parede.

### legenda

Nenhuma placa proíbe nada, mas o desenho prende.

### producao

Traço arquitetônico preciso. Nenhuma placa e nenhum tom de prisão ou de horror. As cinco peças formam um conjunto estável.

### estado

prevista

## ideia-antecipacao-hipercuratorial

### pagina

Antecipação hipercuratorial, depois de Isso tem nome.

### formato

16 x 9

### prioridade

A

### ideia

Uma sala de espera com cadeiras ocupadas e um relógio na parede. Por baixo de uma porta fechada vaza uma luz forte, e todos olham para ela. A luz é regulada por uma mão que sai pela fresta da porta, a mesma que move os ponteiros do relógio por um fio.

> O presente deixa de ser o lugar de uma entrega estabilizada e torna-se uma antecâmara governada (p. 314)

### alt

Sala de espera com pessoas olhando a luz que vaza por baixo de uma porta fechada, regulada por uma mão que também move o relógio.

### legenda

A espera também é vendida.

### producao

Ponteiros e senhas sem números legíveis. A sala lembra uma galeria arrumada.

### estado

prevista

## ideia-auditabilidade-aberta

### pagina

Auditabilidade aberta, depois de Isso tem nome.

### formato

16 x 9

### prioridade

A

### ideia

Uma caixa preta fechada com uma janela recortada num canto, por onde se veem algumas engrenagens. Não a caixa inteira aberta, só o bastante para ver o que mudou. Do lado de fora, preso à caixa, um livro de registro aberto, e mais de uma pessoa consegue olhar pela janela.

> Não transparência total, mas transparência suficiente. (p. 728)

### alt

Caixa preta com uma pequena janela por onde algumas pessoas veem as engrenagens, com um livro de registro aberto ao lado.

### legenda

Não é abrir tudo, é abrir o suficiente.

### producao

Quem olha pela janela pode incluir uma figura de toga e uma de jaleco, ao lado de uma pessoa comum. A janela não tem cortina do lado de dentro.

### estado

prevista

## ideia-equivalencia-de-valor-funcional

### pagina

Equivalência de valor funcional, depois de Isso tem nome.

### formato

16 x 9

### prioridade

A

### ideia

Uma balança de dois pratos com a mesma peça de armadura em cada um, a de antes e a de depois, idênticas por fora. A de depois é um pouco mais fosca, e o prato dela sobe, porque ela pesa menos.

> O que importa é a preservação substancial do papel exercido pelo objeto na experiência adquirida (p. 729)

### alt

Balança com duas peças de armadura iguais, em que o prato da peça de depois sobe por ela pesar menos.

### legenda

Igual por fora, mais leve por dentro.

### producao

Sem etiquetas de antes e depois. A diferença de brilho e a posição dos pratos bastam. Dialoga com parte-a-mudanca.

### estado

prevista

## laboratorio

### pagina

Laboratório, depois da abertura.

### formato

16 x 9

### prioridade

B

### ideia

Uma lupa sobre quatro telas diferentes, a de um assistente, a de uma loja, a de um aplicativo de entrega e a de um atendimento, e sob a lente as quatro mostram a mesma engrenagem. Fora da lente, cada tela mantém a sua aparência.

> A unidade do exame não está no ramo econômico nem na etiqueta mercadológica do serviço, mas no mecanismo predominante pelo qual a experiência do usuário é organizada, modulada, reconfigurada ou tornada contestável. (p. 755)

### alt

Lupa sobre quatro telas diferentes que, vistas pela lente, mostram a mesma engrenagem.

### legenda

Setores diferentes, o mesmo mecanismo.

### producao

Telas sem interface de produto real.

### estado

prevista

## familia-funcionalidade-cognitiva

### pagina

Laboratório, funcionalidade cognitiva, depois do resumo.

### formato

4 x 3

### prioridade

B

### ideia

Um balão de conversa seguro pela mão de quem usa, com um botão de regular intensidade, como os de luz, girado por outra mão, que vem de fora do quadro.

> O que se oferece é ambiente de orientação cognitiva. (p. 757)

### alt

Balão de conversa com um botão de intensidade girado por uma mão fora da imagem.

### legenda

Quem regula a resposta que você recebe?

### producao

Fica claro que quem gira o botão não é quem usa. Nada de rosto de robô ou símbolo de empresa de IA.

### estado

prevista

## familia-infraestrutura-e-intermediacao

### pagina

Laboratório, infraestrutura e intermediação, depois do resumo.

### formato

4 x 3

### prioridade

B

### ideia

Uma vitrine vista através de várias lentes empilhadas, cada uma escondendo ou aumentando uma parte do que está à venda.

> Plataformas dessa natureza não apenas conectam. Elas selecionam, hierarquizam, destacam, ocultam, aproximam, retardam, priorizam e reorganizam a forma pela qual a realidade do ambiente se torna perceptível ao usuário. (p. 761)

### alt

Vitrine vista por lentes empilhadas que escondem ou aumentam partes do que está à venda.

### legenda

Você vê o mercado pelos filtros de outro.

### estado

prevista

## familia-produtividade-gig-economy

### pagina

Laboratório, produtividade sob a gig economy, depois do resumo.

### formato

4 x 3

### prioridade

B

### ideia

Um mapa de cidade em que a rota de uma bicicleta de entrega é desenhada por uma mão enorme, com estrelas de avaliação flutuando sobre o caminho.

> A plataforma organiza acesso à demanda, distribuição de chamadas, previsibilidade mínima de remuneração, permanência no fluxo produtivo, critérios reputacionais, padrões de priorização, regras de aceitação e mecanismos de sanção. (p. 765)

### alt

Mão enorme desenha no mapa a rota de uma bicicleta de entrega, com estrelas de avaliação sobre o caminho.

### legenda

Quem desenha a rota é o aplicativo.

### producao

Quem pedala está em movimento e ativo, nunca preso por fios. Nenhum logotipo de aplicativo real.

### estado

prevista

## familia-administracao-de-confianca

### pagina

Laboratório, administração de confiança, depois do resumo.

### formato

4 x 3

### prioridade

B

### ideia

Uma capa macia e arredondada, com um rosto sorridente de interface, cobrindo a quina de uma mesa. A capa amortece de verdade, mas marcas no chão mostram que a mesa avança um pouco a cada dia sobre o caminho de quem passa.

> Funcionam como técnica de governo da percepção, organizando o limiar a partir do qual a perda será percebida como aceitável, o abuso será lido como falha menor e a contestação será percebida como desnecessária, prematura ou desproporcional. (p. 781)

### alt

Capa macia com rosto sorridente na quina de uma mesa que avança aos poucos sobre o caminho.

### legenda

O tom gentil também faz parte do desenho.

### producao

A proteção é real. A imagem mostra a perda que ela torna imperceptível, sem lâmina escondida e sem tom de armadilha.

### estado

prevista
