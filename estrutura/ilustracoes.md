# Ilustrações conceituais

Plano das peças ilustrativas que o site vai receber quando a estrutura estiver pronta. Orientação do autor de 27/10/2026. As peças serão produzidas com IA e entram nos lugares previstos aqui. Plano do Claude, à espera da revisão do autor. Em 27/10/2026, a direção de arte passou para a paleta aprovada, e duas peças foram refeitas. A da compra deixou de dizer que nada sai da loja, e a da teleologia abusiva deixou de sugerir intenção.

Em 12/11/2026, por ordem do autor de consolidar a estrutura antes da produção, cada peça passou a separar três informações. A ideia descreve o que a figura representa e é o único texto que aparece no lugar previsto, no modo Ciência. A legenda e o texto alternativo acompanham a figura pronta. O campo producao guarda as instruções para quem gera a imagem e nunca vai ao site. Na mesma data entraram as revisões de composição discutidas com o autor, todas conferidas contra o trecho que cada peça ilustra.

Em 17/11/2026, por decisão do autor, a linha de 16/11/2026 saiu do ar. Os pictogramas planos, as vinhetas das portas e dos direitos e as 32 composições SVG não comunicavam a situação da página. As 28 gravuras de 12/11/2026 voltaram, com as versões escuras de 15/11/2026 e o filtro do negativo parcial. A armadura suspensa da capa, de 16/11/2026, ficou. A linha única do site passa a ser a gravura editorial de 12/11/2026, salvo a linguagem geométrica da propriedade intelectual, que é código ensinado e fica só na Doutrina e na Ciência. O roteiro está em `estrutura/roteiro-ilustracoes-2026-11-17.md`.

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

Uma armadura azul de pé sobre uma plataforma estreita, suspensa no ar por dois cabos presos acima dela.

### legenda

Parece terreno seu, mas é chão emprestado.

### producao

Cena serena, sem ameaça nem queda. Os cabos sobem tensos e nenhuma mão os segura. Primeira aparição da armadura canônica.

### procedencia

Gerada com o ChatGPT na entrega de 16/11/2026, Família 3, com versão escura desenhada e fundo transparente. Substituiu a versão de 12/11/2026 e ficou no ar por decisão do autor de 17/11/2026, como única peça mantida dessa entrega.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

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

### procedencia

Gerada com o gerador de imagens do ChatGPT, da OpenAI, em 12/11/2026, a partir do campo producao desta peça e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça.

### estado

publicada

# Lote 2 do roteiro de 17/11/2026

Encomendas das seis portas da capa e das onze páginas de Seus direitos, escritas pelo Claude em 17/11/2026 a partir de `estrutura/roteiro-ilustracoes-2026-11-17.md`, por ordem do autor. Em 17/11/2026, por ordem do autor, o Claude gerou as dezessete peças no Canva a partir do campo producao e conferiu cada arquivo pelo critério de aceite antes de pôr no site. A versão escura sai pelo negativo calculado e pelo filtro do negativo parcial, salvo decisão diferente do autor.

## direito-a

### pagina

Seus direitos, página O que você comprou é produto, mesmo sem nada nas mãos, em direitos/a/, logo depois do título.

### formato

4 x 3

### prioridade

A

### ideia

Uma pessoa no sofá vê a armadura cair no inventário do celular. Ao lado, numa mesinha, a caixa aberta de um par de sapatos comprado numa loja comum. As duas compras têm o mesmo peso na cena.

> A qualificação jurídica daí resultante é a de produto imaterial submetido ao regime do art. 3º, § 1º, do CDC, sem que a dimensão prestacional do vínculo afaste o controle da fruição como núcleo do fornecimento. (p. 743)

### alt

Uma pessoa vê no celular o item que acabou de comprar, ao lado de uma caixa de sapatos aberta.

### legenda

As duas são compras.

### producao

Ilustração editorial em gravura a nanquim, traço fino e hachura discreta, sobre papel creme (#faf6ef), com fundo opaco. Uma só cor além do preto, o azul Klein chapado (#002fa7). O azul marca só a armadura na tela do celular, e nada mais. Estruturas escondidas em linhas tracejadas cinza (#615953). Nenhuma letra, número, logotipo, marca, interface real ou personagem conhecido. Telas mostram só ícones e linhas. Pessoas comuns, de idades e corpos variados, sem rosto detalhado. Formato 4:3, 1200 por 900 pixels, muito espaço livre, nada colado às bordas. Arquivo WebP de até 250 KB. Siga o traço das imagens de referência anexas, familia-produtividade-gig-economy.webp e parte-o-desenho.webp. A armadura é a da folha canônica anexa, armadura.webp, pequena e reconhecível. Cena. Uma pessoa sentada no sofá olha o celular. Na tela, a armadura acaba de cair no inventário, com um sinal de confirmação. Ao lado, numa mesinha, uma caixa de sapatos aberta, com o par dentro e o papel de seda. As duas compras ficam em pé de igualdade, com a mesma luz e o mesmo peso na composição. Evitar. Texto ou números na tela ou na caixa, marca de loja, nota fiscal legível.

### procedencia

Gerada com o gerador de imagens do Canva pelo Claude, em 17/11/2026, a partir do campo producao desta peça, das gravuras familia-produtividade-gig-economy e parte-o-desenho e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça e publicada por ordem do autor.

### estado

publicada

## direito-b

### pagina

Seus direitos, página A plataforma não pode montar a experiência para você não entender, em direitos/b/, logo depois do título.

### formato

4 x 3

### prioridade

A

### ideia

Duas mãos seguram um celular com uma loja de jogo na tela. O botão de compra é enorme, a armadura brilha e uma ampulheta corre no canto. O caminho para as condições é uma linha cinza quase invisível embaixo.

> Sempre que expectativa, percepção de valor, avaliação de risco ou capacidade de contestação dependerem de signos, interfaces, fluxos e trilhas informacionais controlados pelo fornecedor, haverá vulnerabilidade semiótica juridicamente relevante. (p. 744)

### alt

Num celular, uma loja de jogo com um botão de compra enorme e um relógio correndo, enquanto o acesso às condições é uma linha quase invisível.

### legenda

Tudo grande para comprar, tudo pequeno para entender.

### producao

Ilustração editorial em gravura a nanquim, traço fino e hachura discreta, sobre papel creme (#faf6ef), com fundo opaco. Uma só cor além do preto, o azul Klein chapado (#002fa7). O azul marca só a armadura na vitrine da tela, e nada mais. Estruturas escondidas em linhas tracejadas cinza (#615953). Nenhuma letra, número, logotipo, marca, interface real ou personagem conhecido. Telas mostram só ícones e linhas. Pessoas comuns, de idades e corpos variados, sem rosto detalhado. Formato 4:3, 1200 por 900 pixels, muito espaço livre, nada colado às bordas. Arquivo WebP de até 250 KB. Siga o traço das imagens de referência anexas, familia-produtividade-gig-economy.webp e parte-o-desenho.webp. A armadura é a da folha canônica anexa, armadura.webp, pequena e reconhecível. Cena. Close de um celular seguro por duas mãos. A tela é uma loja de jogo carregada. No centro, um botão enorme com um carrinho, a armadura em destaque com brilho e uma ampulheta correndo no canto. Embaixo, quase invisível, uma linha cinza minúscula com um pequeno ícone de documento, o caminho para as condições. O polegar está a caminho do botão grande. Linhas tracejadas finas mostram que a tela tem camadas por trás. Evitar. Interface real reconhecível, qualquer letra ou número na tela, ar de ameaça.

### procedencia

Gerada com o gerador de imagens do Canva pelo Claude, em 17/11/2026, a partir do campo producao desta peça, das gravuras familia-produtividade-gig-economy e parte-o-desenho e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça e publicada por ordem do autor.

### estado

publicada

## direito-c

### pagina

Seus direitos, página A informação precisa servir para alguma coisa, em direitos/c/, logo depois do título.

### formato

4 x 3

### prioridade

A

### ideia

A mesma pessoa aparece duas vezes. À esquerda, diante de um rolo de papel que desce do celular e se amontoa no chão. À direita, com um cartão pequeno de três sinais claros, um relógio, uma seta de mudança e um item riscado.

> A informação, no CDC, não cumpre sua função só porque existe em algum lugar, nem porque foi depositada em documentos extensos, remissões, FAQs ou históricos de atualização que o consumidor dificilmente localizará, compreenderá e conectará ao impacto (p. 641)

### alt

Uma pessoa soterrada por um rolo de termos e, ao lado, a mesma pessoa lendo um cartão curto com três sinais claros.

### legenda

Muita informação não é informação.

### producao

Ilustração editorial em gravura a nanquim, traço fino e hachura discreta, sobre papel creme (#faf6ef), com fundo opaco. Uma só cor além do preto, o azul Klein chapado (#002fa7). O azul marca só o cartão útil da metade direita, e nada mais. Estruturas escondidas em linhas tracejadas cinza (#615953). Nenhuma letra, número, logotipo, marca, interface real ou personagem conhecido. Telas mostram só ícones e linhas. Pessoas comuns, de idades e corpos variados, sem rosto detalhado. Formato 4:3, 1200 por 900 pixels, muito espaço livre, nada colado às bordas. Arquivo WebP de até 250 KB. Siga o traço das imagens de referência anexas, familia-produtividade-gig-economy.webp e parte-o-desenho.webp. Nesta cena não há armadura nenhuma. A pessoa é comum, de camiseta e calça do dia a dia, igual nas duas metades, e ninguém veste armadura, peça de metal ou roupa de cavaleiro. Cena. Duas metades. À esquerda, uma pessoa diante de um rolo de papel que desce do celular e se acumula no chão em montes, de tão comprido, coberto de linhas cinza. À direita, a mesma pessoa segura um cartão pequeno com três ícones grandes e claros, um relógio, uma seta de mudança e um item riscado. Evitar. Letras no papel ou no cartão, tom cômico exagerado.

### procedencia

Gerada com o gerador de imagens do Canva pelo Claude, em 17/11/2026, a partir do campo producao desta peça, das gravuras familia-produtividade-gig-economy e parte-o-desenho e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça e publicada por ordem do autor.

### estado

publicada

## direito-d

### pagina

Seus direitos, página O que foi prometido precisa ser entregue, em direitos/d/, logo depois do título.

### formato

4 x 3

### prioridade

A

### ideia

Um outdoor de rua mostra a armadura cercada de raios e faíscas. Embaixo dele, uma pessoa abre o celular e vê a mesma armadura sem nenhum efeito, opaca, e olha de uma para a outra.

> Sempre que a fruição for precedida por ciclos curados de antecipação, promessa, escassez sugerida, distinção simbólica ou equivalências insinuadas, a publicidade integrará materialmente a oferta. (p. 744-745)

### alt

Uma pessoa compara a armadura cheia de efeitos de um anúncio de rua com a armadura apagada que recebeu no celular.

### legenda

O anúncio também é promessa.

### producao

Ilustração editorial em gravura a nanquim, traço fino e hachura discreta, sobre papel creme (#faf6ef), com fundo opaco. Uma só cor além do preto, o azul Klein chapado (#002fa7). O azul marca só as duas armaduras, a do anúncio cheia de efeitos e a da tela sem brilho, e nada mais. Estruturas escondidas em linhas tracejadas cinza (#615953). Nenhuma letra, número, logotipo, marca, interface real ou personagem conhecido. Telas mostram só ícones e linhas. Pessoas comuns, de idades e corpos variados, sem rosto detalhado. Formato 4:3, 1200 por 900 pixels, muito espaço livre, nada colado às bordas. Arquivo WebP de até 250 KB. Siga o traço das imagens de referência anexas, familia-produtividade-gig-economy.webp e parte-o-desenho.webp. A armadura é a da folha canônica anexa, armadura.webp, pequena e reconhecível. Cena. Um outdoor de rua mostra a armadura cercada de raios, faíscas e efeitos. Embaixo do outdoor, uma pessoa abre o celular, e na tela a mesma armadura aparece sem nenhum dos efeitos, opaca. A pessoa olha de um para o outro. Evitar. Texto no outdoor, marca, preço.

### procedencia

Gerada com o gerador de imagens do Canva pelo Claude, em 17/11/2026, a partir do campo producao desta peça, das gravuras familia-produtividade-gig-economy e parte-o-desenho e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça e publicada por ordem do autor.

### estado

publicada

## direito-e

### pagina

Seus direitos, página Mudança relevante precisa deixar rastro, em direitos/e/, logo depois do título.

### formato

4 x 3

### prioridade

A

### ideia

Pegadas na neve atravessam um pátio até uma vitrine onde a armadura mudou de forma. Uma vassoura, que sai de uma porta lateral, apaga parte delas, e uma pessoa segue as que restam com o celular na mão.

> O dever de fornecimento correspondente é o de manter verificabilidade mínima sobre o que foi alterado, quando o foi, por que motivo foi justificado e quais efeitos funcionalmente relevantes produziu. (p. 745)

### alt

Pegadas na neve levam a uma vitrine onde a armadura mudou, e uma vassoura apaga parte delas.

### legenda

Quem muda deixa rastro. Ou deveria.

### producao

Ilustração editorial em gravura a nanquim, traço fino e hachura discreta, sobre papel creme (#faf6ef), com fundo opaco. Uma só cor além do preto, o azul Klein chapado (#002fa7). O azul marca só a armadura na vitrine, e nada mais. Estruturas escondidas em linhas tracejadas cinza (#615953). Nenhuma letra, número, logotipo, marca, interface real ou personagem conhecido. Telas mostram só ícones e linhas. Pessoas comuns, de idades e corpos variados, sem rosto detalhado. Formato 4:3, 1200 por 900 pixels, muito espaço livre, nada colado às bordas. Arquivo WebP de até 250 KB. Siga o traço das imagens de referência anexas, familia-produtividade-gig-economy.webp e parte-o-desenho.webp. A armadura é a da folha canônica anexa, armadura.webp, pequena e reconhecível. Cena. Neve fresca num pátio. Pegadas atravessam o pátio até uma vitrine onde a armadura mudou de forma. Uma das pegadas está sendo apagada por uma vassoura empunhada por uma mão que sai de uma porta lateral. Uma pessoa de casaco segue as pegadas que restam, com o celular na mão. Evitar. Clima de crime ou perseguição, rosto de quem varre.

### procedencia

Gerada com o gerador de imagens do Canva pelo Claude, em 17/11/2026, a partir do campo producao desta peça, das gravuras familia-produtividade-gig-economy e parte-o-desenho e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça e publicada por ordem do autor.

### estado

publicada

## direito-f

### pagina

Seus direitos, página Mudou, tem que manter o que valia, em direitos/f/, logo depois do título.

### formato

4 x 3

### prioridade

A

### ideia

Uma balança de feira equilibra a armadura antiga e a nova, de desenhos diferentes e do mesmo peso. Uma pessoa confere o fiel de perto, e na parede fica a sombra da armadura antiga.

> O dever de fornecimento correspondente é o de preservar, em termos substanciais, o papel funcional, relacional e, quando juridicamente relevante, simbólico do objeto na experiência do consumidor. (p. 745)

### alt

Uma balança equilibra a armadura antiga e a nova, de desenhos diferentes, e uma pessoa confere o equilíbrio.

### legenda

Pode mudar a forma. O valor tem de ficar.

### producao

Ilustração editorial em gravura a nanquim, traço fino e hachura discreta, sobre papel creme (#faf6ef), com fundo opaco. Uma só cor além do preto, o azul Klein chapado (#002fa7). O azul marca só as duas armaduras, e nada mais. Estruturas escondidas em linhas tracejadas cinza (#615953). Nenhuma letra, número, logotipo, marca, interface real ou personagem conhecido. Telas mostram só ícones e linhas. Pessoas comuns, de idades e corpos variados, sem rosto detalhado. Formato 4:3, 1200 por 900 pixels, muito espaço livre, nada colado às bordas. Arquivo WebP de até 250 KB. Siga o traço das imagens de referência anexas, familia-produtividade-gig-economy.webp e parte-o-desenho.webp. A armadura é a da folha canônica anexa, armadura.webp, pequena e reconhecível. Cena. Uma balança de feira de dois pratos. Num prato, a armadura antiga, cheia. No outro, a nova, com desenho claramente diferente e silhueta que se reconhece de longe, elmo aberto com crista, ombreiras pontudas, peito com outro recorte e capa curta, enquanto a antiga tem elmo fechado, ombreiras redondas e saia de placas. As duas têm o mesmo tamanho e o mesmo peso, e a balança fica em equilíbrio perfeito. Uma pessoa confere o fiel da balança de perto. Atrás, na parede, a sombra da armadura antiga. Evitar. Armadura oca ou quebrada, balança da justiça, venda nos olhos. Não repetir a composição da peça ideia-equivalencia-de-valor-funcional, em que uma das armaduras está oca.

### procedencia

Gerada com o gerador de imagens do Canva pelo Claude, em 17/11/2026, a partir do campo producao desta peça, das gravuras familia-produtividade-gig-economy e parte-o-desenho e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça e publicada por ordem do autor.

### estado

publicada

## direito-g

### pagina

Seus direitos, página Punição precisa de motivo e de chance de defesa, em direitos/g/, logo depois do título.

### formato

4 x 3

### prioridade

A

### ideia

Uma pessoa está trancada do lado de fora de uma porta de vidro com um cadeado grande, e lá dentro a armadura dela fica pendurada num armário. Ela aperta a campainha, e o fio dá a volta e retorna ao próprio botão.

> O dever de fornecimento correspondente é o de assegurar procedimentos minimamente inteligíveis, motivação verificável, possibilidade razoável de contestação e tratamento não arbitrário do usuário na administração da fruição. (p. 746)

### alt

Uma pessoa trancada do lado de fora vê a própria armadura atrás do vidro e aperta uma campainha cujo fio volta para ela mesma.

### legenda

Trancar exige motivo. E alguém do outro lado.

### producao

Ilustração editorial em gravura a nanquim, traço fino e hachura discreta, sobre papel creme (#faf6ef), com fundo opaco. Uma só cor além do preto, o azul Klein chapado (#002fa7). O azul marca só a armadura atrás do vidro, e nada mais. Estruturas escondidas em linhas tracejadas cinza (#615953). Nenhuma letra, número, logotipo, marca, interface real ou personagem conhecido. Telas mostram só ícones e linhas. Pessoas comuns, de idades e corpos variados, sem rosto detalhado. Formato 4:3, 1200 por 900 pixels, muito espaço livre, nada colado às bordas. Arquivo WebP de até 250 KB. Siga o traço das imagens de referência anexas, familia-produtividade-gig-economy.webp e parte-o-desenho.webp. A armadura é a da folha canônica anexa, armadura.webp, pequena e reconhecível. Cena. Uma pessoa diante de uma porta de vidro fechada, com um cadeado grande. Do outro lado do vidro, o inventário dela, com a armadura pendurada num armário. Na porta, uma campainha. A pessoa aperta a campainha, e o fio da campainha, em tracejado cinza, dá a volta e volta para o próprio botão, sem chegar a lugar nenhum. Evitar. Polícia, prisão, grades de cela, sinal de crime.

### procedencia

Gerada com o gerador de imagens do Canva pelo Claude, em 17/11/2026, a partir do campo producao desta peça, das gravuras familia-produtividade-gig-economy e parte-o-desenho e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça e publicada por ordem do autor.

### estado

publicada

## direito-h

### pagina

Seus direitos, página Quando a perda é regra, o problema é o desenho, em direitos/h/, logo depois do título.

### formato

4 x 3

### prioridade

A

### ideia

Uma fila de pessoas com moedas espera diante de uma máquina de garra. A armadura fica no alto, fora do alcance, e o mecanismo aparece por dentro, regulado para soltar, enquanto o pote de moedas transborda.

> O foco está na finalidade funcional objetivamente inscrita no arranjo, tal como se revela por sua replicabilidade, por sua coerência interna e por seu impacto reiterado sobre a experiência do consumidor. (p. 732)

### alt

Uma fila espera diante de uma máquina de garra em que a armadura fica fora do alcance, e o mecanismo aparece regulado para soltar.

### legenda

Quando ninguém consegue, o problema é a máquina.

### producao

Ilustração editorial em gravura a nanquim, traço fino e hachura discreta, sobre papel creme (#faf6ef), com fundo opaco. Uma só cor além do preto, o azul Klein chapado (#002fa7). O azul marca só a armadura dentro da máquina, e nada mais. Estruturas escondidas em linhas tracejadas cinza (#615953). Nenhuma letra, número, logotipo, marca, interface real ou personagem conhecido. Telas mostram só ícones e linhas. Pessoas comuns, de idades e corpos variados, sem rosto detalhado. Formato 4:3, 1200 por 900 pixels, muito espaço livre, nada colado às bordas. Arquivo WebP de até 250 KB. Siga o traço das imagens de referência anexas, familia-produtividade-gig-economy.webp e parte-o-desenho.webp. A armadura é a da folha canônica anexa, armadura.webp, pequena e reconhecível. Cena. Uma máquina de parque de diversões, de garra de pegar bichinho. Dentro, a armadura no alto, fora do alcance. A garra é desenhada frouxa, aberta demais. Ao lado, uma fila de pessoas com moedas na mão, e no chão um pote de moedas cheio. Linhas tracejadas cinza mostram o mecanismo da garra por dentro da máquina, regulado para soltar. Evitar. Dono da máquina rindo ou qualquer sinal de intenção pessoal. O que aparece é o padrão do mecanismo, não a vontade de alguém.

### procedencia

Gerada com o gerador de imagens do Canva pelo Claude, em 17/11/2026, a partir do campo producao desta peça, das gravuras familia-produtividade-gig-economy e parte-o-desenho e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça e publicada por ordem do autor.

### estado

publicada

## direito-i

### pagina

Seus direitos, página A prova que está com a plataforma tem que aparecer, em direitos/i/, logo depois do título.

### formato

4 x 3

### prioridade

A

### ideia

À esquerda, uma pessoa na mesa da cozinha com prints e o celular. À direita, uma sala de arquivos atrás de uma grade, com caixas em prateleiras altas. Entre as duas, uma mão de juiz aponta para a grade pedindo que ela abra.

> Quanto mais dependente da governança interna for a reconstrução do conflito, menos razoável será exigir do consumidor demonstração minuciosa de fatos cujo suporte documental e técnico jamais esteve sob seu alcance. (p. 736)

### alt

Uma pessoa com prints na mesa de casa, e ao lado uma sala de arquivos trancada, para a qual uma mão aponta pedindo abertura.

### legenda

Quem guarda a prova tem de mostrá-la.

### producao

Ilustração editorial em gravura a nanquim, traço fino e hachura discreta, sobre papel creme (#faf6ef), com fundo opaco. Uma só cor além do preto, o azul Klein chapado (#002fa7). O azul marca só uma das caixas na prateleira, a que guarda o registro do caso, e nada mais. Estruturas escondidas em linhas tracejadas cinza (#615953). Nenhuma letra, número, logotipo, marca, interface real ou personagem conhecido. Telas mostram só ícones e linhas. Pessoas comuns, de idades e corpos variados, sem rosto detalhado. Formato 4:3, 1200 por 900 pixels, muito espaço livre, nada colado às bordas. Arquivo WebP de até 250 KB. Siga o traço das imagens de referência anexas, familia-produtividade-gig-economy.webp e parte-o-desenho.webp. A armadura é a da folha canônica anexa, armadura.webp, pequena e reconhecível. Cena. Duas metades. À esquerda, uma pessoa sentada à mesa da cozinha com prints espalhados e o celular. À direita, uma sala de servidores atrás de uma grade, com caixas arquivadas em prateleiras altas. Entre as metades, uma mão de juiz, só a manga e a mão, aponta para a grade pedindo que ela abra. Evitar. Martelo, toga inteira, balança da justiça, letras nas caixas.

### procedencia

Gerada com o gerador de imagens do Canva pelo Claude, em 17/11/2026, a partir do campo producao desta peça, das gravuras familia-produtividade-gig-economy e parte-o-desenho e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça e publicada por ordem do autor.

### estado

publicada

## direito-j

### pagina

Seus direitos, página Ser dona da obra não é desculpa para tudo, em direitos/j/, logo depois do título.

### formato

4 x 3

### prioridade

A

### ideia

Num ateliê, pessoas usam as armaduras que compraram dentro de uma grande tela pintada. O artista, dono da obra, ergue um pano para cobrir a tela inteira, e uma moldura tracejada em volta das pessoas mostra o que não é só dele.

> O dever correspondente é o de exercer a exclusividade sem convertê-la em escudo para opacidade absoluta, mutabilidade degradante ou supressão arbitrária da fruição. (p. 747)

### alt

Um artista vai cobrir com um pano a tela em que pessoas usam as armaduras que compraram, e uma moldura em volta delas mostra o que não é só dele.

### legenda

A obra é da empresa. A compra é sua.

### producao

Ilustração editorial em gravura a nanquim, traço fino e hachura discreta, sobre papel creme (#faf6ef), com fundo opaco. Uma só cor além do preto, o azul Klein chapado (#002fa7). O azul marca só as armaduras das pessoas dentro da pintura, e nada mais. Estruturas escondidas em linhas tracejadas cinza (#615953). Nenhuma letra, número, logotipo, marca, interface real ou personagem conhecido. Telas mostram só ícones e linhas. Pessoas comuns, de idades e corpos variados, sem rosto detalhado. Formato 4:3, 1200 por 900 pixels, muito espaço livre, nada colado às bordas. Arquivo WebP de até 250 KB. Siga o traço das imagens de referência anexas, familia-produtividade-gig-economy.webp e parte-o-desenho.webp. A armadura é a da folha canônica anexa, armadura.webp, pequena e reconhecível. Cena. Um ateliê com uma grande tela pintada que é o cenário de um jogo. O artista, dono da obra, está ao lado. Dentro da pintura, pessoas que compraram a armadura a vestem e convivem. O artista ergue um pano para cobrir a tela inteira. Uma moldura tracejada cinza em volta das pessoas mostra que a parte delas não é dele cobrir. Evitar. Assinatura do artista, pintura famosa reconhecível, símbolo de copyright.

### procedencia

Gerada com o gerador de imagens do Canva pelo Claude, em 17/11/2026, a partir do campo producao desta peça, das gravuras familia-produtividade-gig-economy e parte-o-desenho e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça e publicada por ordem do autor.

### estado

publicada

## direito-k

### pagina

Seus direitos, página A resposta deve recompor o que você perdeu, em direitos/k/, logo depois do título.

### formato

4 x 3

### prioridade

A

### ideia

Duas mãos de restaurador, com luvas finas, encaixam de volta as peças quebradas da armadura numa mesa, guiadas por uma folha com o desenho dela inteira. Uma pessoa observa da porta.

> Sempre que a lesão atingir acesso, continuidade, equivalência, histórico, posição relacional ou densidade significativa da fruição, a resposta jurídica deverá priorizar recomposição funcional, reservando indenização pecuniária para hipóteses de inviabilidade ou insuficiência da restauração. (p. 748)

### alt

Mãos de restaurador encaixam as peças da armadura de volta, guiadas pelo desenho dela inteira.

### legenda

Responder é pôr de volta o que foi tirado.

### producao

Ilustração editorial em gravura a nanquim, traço fino e hachura discreta, sobre papel creme (#faf6ef), com fundo opaco. Uma só cor além do preto, o azul Klein chapado (#002fa7). O azul marca só as peças da armadura, e nada mais. Estruturas escondidas em linhas tracejadas cinza (#615953). Nenhuma letra, número, logotipo, marca, interface real ou personagem conhecido. Telas mostram só ícones e linhas. Pessoas comuns, de idades e corpos variados, sem rosto detalhado. Formato 4:3, 1200 por 900 pixels, muito espaço livre, nada colado às bordas. Arquivo WebP de até 250 KB. Siga o traço das imagens de referência anexas, familia-produtividade-gig-economy.webp e parte-o-desenho.webp. A armadura é a da folha canônica anexa, armadura.webp, pequena e reconhecível. Cena. Uma mesa de restaurador. As peças da armadura, que estavam quebradas, são encaixadas de volta por duas mãos com luvas finas. Ao lado, uma folha com o desenho da armadura inteira, que serve de molde. Uma pessoa observa da porta. Evitar. Dinheiro, cheque ou moedas na mesa.

### procedencia

Gerada com o gerador de imagens do Canva pelo Claude, em 17/11/2026, a partir do campo producao desta peça, das gravuras familia-produtividade-gig-economy e parte-o-desenho e da folha canônica da armadura. Conferida pelo Claude contra a ideia da peça e publicada por ordem do autor.

### estado

publicada

## porta-acesso

### pagina

Página inicial, cartão Perdi o acesso, no alto, na largura do cartão. Decorativa, sem legenda e com texto alternativo vazio no site.

### formato

4 x 3

### prioridade

A

### ideia

Uma pessoa, à noite, está diante da porta de vidro de um prédio com a chave na mão, mas a fechadura virou uma tampa lisa. Atrás do vidro, na sala iluminada, as coisas dela continuam nas prateleiras.

> Encerrada a conta, o usuário não terá mais acesso à conta, nem aos dados associados, nem ao Conteúdo Virtual, incluindo moeda do jogo, e a consequência é a perda definitiva sem reembolso quando o senhorio entende que havia motivo (p. 155)

### alt

Uma pessoa com a chave na mão diante de uma porta sem fechadura, vendo as próprias coisas do outro lado do vidro.

### producao

Ilustração editorial em gravura a nanquim, traço fino e hachura discreta, sobre papel creme (#faf6ef), com fundo opaco. Uma só cor além do preto, o azul Klein chapado (#002fa7). O azul marca só as coisas dela atrás do vidro, um controle de jogo, um álbum de fotos e uma caixa de compras, e nada mais. Estruturas escondidas em linhas tracejadas cinza (#615953). Nenhuma letra, número, logotipo, marca, interface real ou personagem conhecido. Telas mostram só ícones e linhas. Pessoas comuns, de idades e corpos variados, sem rosto detalhado. Formato 4:3, 1200 por 900 pixels, muito espaço livre, nada colado às bordas. Arquivo WebP de até 250 KB. Siga o traço das imagens de referência anexas, familia-produtividade-gig-economy.webp e parte-o-desenho.webp. Cena. Uma pessoa diante da porta de vidro de um prédio, à noite, com a chave na mão. A chave não entra, porque a fechadura foi trocada por uma tampa lisa. Através do vidro, na sala iluminada, as coisas dela continuam nas prateleiras, um controle de jogo, um álbum de fotos e uma caixa de compras. Evitar. Arrombamento, polícia, alarme, qualquer sinal de crime. A armadura do site não aparece.

### procedencia

Gerada com o gerador de imagens do Canva pelo Claude, em 17/11/2026, a partir do campo producao desta peça, das gravuras familia-produtividade-gig-economy e parte-o-desenho. Conferida pelo Claude contra a ideia da peça e publicada por ordem do autor.

### estado

publicada

## porta-mudou

### pagina

Página inicial, cartão O que comprei mudou, no alto, na largura do cartão. Decorativa, sem legenda e com texto alternativo vazio no site.

### formato

4 x 3

### prioridade

A

### ideia

Uma pessoa segura uma luminária de mesa que continua igual por fora, mas mal acende. Na parede, a sombra da luz antiga é grande e a de agora é pequena, ao lado da caixa aberta em que ela veio.

> A promessa de distinção permanece nominalmente na conta, mas deixa de encontrar, no mundo do jogo, o encaixe que conferia valor ao investimento de tempo, dinheiro e atenção. (p. 104)

### alt

Uma pessoa segura uma luminária que continua igual por fora, mas acende muito menos do que acendia quando foi comprada.

### producao

Ilustração editorial em gravura a nanquim, traço fino e hachura discreta, sobre papel creme (#faf6ef), com fundo opaco. Uma só cor além do preto, o azul Klein chapado (#002fa7). O azul marca só a luz, a antiga no halo grande da parede e a fraca na lâmpada, e nada mais. Estruturas escondidas em linhas tracejadas cinza (#615953). Nenhuma letra, número, logotipo, marca, interface real ou personagem conhecido. Telas mostram só ícones e linhas. Pessoas comuns, de idades e corpos variados, sem rosto detalhado. Formato 4:3, 1200 por 900 pixels, muito espaço livre, nada colado às bordas. Arquivo WebP de até 250 KB. Siga o traço das imagens de referência anexas, familia-produtividade-gig-economy.webp e parte-o-desenho.webp. Cena. Uma pessoa segura um objeto que comprou, uma luminária de mesa. A luminária continua igual por fora, mas a lâmpada, que acendia forte, agora mal acende. Ao lado, a caixa aberta em que ela veio. Na parede, o halo da luz antiga, grande, e o da luz de agora, pequeno. Evitar. Quebra visível. O objeto continua inteiro, e o que mudou foi o que ele faz. A armadura do site não aparece.

### procedencia

Gerada com o gerador de imagens do Canva pelo Claude, em 17/11/2026, a partir do campo producao desta peça, das gravuras familia-produtividade-gig-economy e parte-o-desenho. Conferida pelo Claude contra a ideia da peça e publicada por ordem do autor.

### estado

publicada

## porta-empurrado

### pagina

Página inicial, cartão Fui empurrado a pagar, no alto, na largura do cartão. Decorativa, sem legenda e com texto alternativo vazio no site.

### formato

4 x 3

### prioridade

A

### ideia

Uma pessoa está numa esteira rolante que termina num caixa, cercada de relógios e setas que apontam para ele. Ela tenta andar para trás e não sai do lugar, enquanto ao lado uma escada comum e vazia leva para fora.

> Ela tende a emergir como programa de funcionamento, isto é, como articulação entre múltiplos mecanismos que comprimem tempo de reflexão, reorganizam expectativa, aumentam custo de saída, dificultam reversão e tornam a fruição progressivamente dependente do próprio ambiente que a governa. (p. 670)

### alt

Uma pessoa numa esteira rolante que só leva ao caixa, cercada de relógios e setas, enquanto a saída fica de lado.

### producao

Ilustração editorial em gravura a nanquim, traço fino e hachura discreta, sobre papel creme (#faf6ef), com fundo opaco. Uma só cor além do preto, o azul Klein chapado (#002fa7). O azul marca só o cartão de pagamento na mão da pessoa, e nada mais. Estruturas escondidas em linhas tracejadas cinza (#615953). Nenhuma letra, número, logotipo, marca, interface real ou personagem conhecido. Telas mostram só ícones e linhas. Pessoas comuns, de idades e corpos variados, sem rosto detalhado. Formato 4:3, 1200 por 900 pixels, muito espaço livre, nada colado às bordas. Arquivo WebP de até 250 KB. Siga o traço das imagens de referência anexas, familia-produtividade-gig-economy.webp e parte-o-desenho.webp. Cena. Uma pessoa sobre uma esteira rolante de aeroporto que termina num caixa. Ela está virada de costas para o caixa, com o corpo inclinado e o pé de trás fazendo força, tentando andar no sentido contrário ao da esteira, e mesmo assim a esteira a leva para o caixa. O esforço dela tem de ser visível. Nas paredes da esteira, relógios correndo e setas grandes, todas apontando para o caixa. Ao lado da esteira, fora dela, uma escada comum, vazia, que leva para fora. Evitar. Vendedor empurrando a pessoa, letras ou preços nas placas. A armadura do site não aparece.

### procedencia

Gerada com o gerador de imagens do Canva pelo Claude, em 17/11/2026, a partir do campo producao desta peça, das gravuras familia-produtividade-gig-economy e parte-o-desenho. Conferida pelo Claude contra a ideia da peça e publicada por ordem do autor.

### estado

publicada

## porta-sair

### pagina

Página inicial, cartão Quero sair e levar o que é meu, no alto, na largura do cartão. Decorativa, sem legenda e com texto alternativo vazio no site.

### formato

4 x 3

### prioridade

A

### ideia

Uma pessoa está na porta de um apartamento com uma mala pequena, pronta para se mudar. Tudo o que ela juntou ficou dentro, preso ao chão, os livros, as fotos com amigos, os troféus e a mesa onde recebia gente.

> Sair significa abandonar histórico, reputação, biblioteca, itens, progressão, investimentos afetivos, redes de sociabilidade e, em certos casos, a própria capacidade de participar de comunidades que se organizam dentro daquele ecossistema. (p. 217)

### alt

Uma pessoa sai de casa com uma mala pequena, e tudo o que construiu lá dentro fica preso ao chão.

### producao

Ilustração editorial em gravura a nanquim, traço fino e hachura discreta, sobre papel creme (#faf6ef), com fundo opaco. Uma só cor além do preto, o azul Klein chapado (#002fa7). O azul marca só as coisas que ficam presas lá dentro, e nada mais. Estruturas escondidas em linhas tracejadas cinza (#615953). Nenhuma letra, número, logotipo, marca, interface real ou personagem conhecido. Telas mostram só ícones e linhas. Pessoas comuns, de idades e corpos variados, sem rosto detalhado. Formato 4:3, 1200 por 900 pixels, muito espaço livre, nada colado às bordas. Arquivo WebP de até 250 KB. Siga o traço das imagens de referência anexas, familia-produtividade-gig-economy.webp e parte-o-desenho.webp. Cena. Uma pessoa na porta de um apartamento, de mala pequena na mão, pronta para se mudar. Tudo o que ela juntou ficou dentro, preso ao chão por parafusos visíveis, os livros, as fotos com amigos, os troféus e a mesa onde recebia gente. Pela janela, um vizinho acena. Evitar. Despejo, oficial de justiça, briga. A armadura do site não aparece.

### procedencia

Gerada com o gerador de imagens do Canva pelo Claude, em 17/11/2026, a partir do campo producao desta peça, das gravuras familia-produtividade-gig-economy e parte-o-desenho. Conferida pelo Claude contra a ideia da peça e publicada por ordem do autor.

### estado

publicada

## porta-decide

### pagina

Página inicial, cartão A plataforma decide sobre mim sem explicar, no alto, na largura do cartão. Decorativa, sem legenda e com texto alternativo vazio no site.

### formato

4 x 3

### prioridade

A

### ideia

Um guichê de vidro fosco, sem ninguém visível do outro lado, entrega folhas carimbadas pela fresta. Atrás de quem recebe a sua, a fila traz um entregador de capacete, uma vendedora com uma caixa e alguém com o celular.

> A alteração de regra, o rebaixamento de alcance ou a suspensão sequer se transformam em objeto verificável e disputável no próprio sistema. (p. 381)

### alt

Um guichê de vidro fosco entrega folhas carimbadas a uma fila de pessoas, sem ninguém visível do outro lado.

### producao

Ilustração editorial em gravura a nanquim, traço fino e hachura discreta, sobre papel creme (#faf6ef), com fundo opaco. Uma só cor além do preto, o azul Klein chapado (#002fa7). O azul marca só as folhas carimbadas, e nada mais. Estruturas escondidas em linhas tracejadas cinza (#615953). Nenhuma letra, número, logotipo, marca, interface real ou personagem conhecido. Telas mostram só ícones e linhas. Pessoas comuns, de idades e corpos variados, sem rosto detalhado. Formato 4:3, 1200 por 900 pixels, muito espaço livre, nada colado às bordas. Arquivo WebP de até 250 KB. Siga o traço das imagens de referência anexas, familia-produtividade-gig-economy.webp e parte-o-desenho.webp. Cena. Um guichê de vidro fosco, sem rosto do outro lado. Pela fresta sai uma folha carimbada que cai na mão de uma pessoa. Atrás dela, uma fila com um entregador de capacete, uma vendedora com uma caixa e alguém com o celular, cada um com a sua folha carimbada. Evitar. Letras no carimbo ou nas folhas, bandeira, brasão. A armadura do site não aparece.

### procedencia

Gerada com o gerador de imagens do Canva pelo Claude, em 17/11/2026, a partir do campo producao desta peça, das gravuras familia-produtividade-gig-economy e parte-o-desenho. Conferida pelo Claude contra a ideia da peça e publicada por ordem do autor.

### estado

publicada

## porta-comum

### pagina

Página inicial, cartão Provar e reclamar, no alto, na largura do cartão. Decorativa, sem legenda e com texto alternativo vazio no site.

### formato

4 x 3

### prioridade

A

### ideia

Duas mãos fecham um envelope sobre uma mesa de cozinha cheia de prints impressos, o celular e um caderno de anotações. Pela janela, ao fundo, aparece um prédio público comum.

> Quanto mais dependente da governança interna for a reconstrução do conflito, menos razoável será exigir do consumidor demonstração minuciosa de fatos cujo suporte documental e técnico jamais esteve sob seu alcance. (p. 736)

### alt

Mãos fecham um envelope sobre uma mesa cheia de prints e anotações.

### producao

Ilustração editorial em gravura a nanquim, traço fino e hachura discreta, sobre papel creme (#faf6ef), com fundo opaco. Uma só cor além do preto, o azul Klein chapado (#002fa7). O azul marca só o envelope, e nada mais. Estruturas escondidas em linhas tracejadas cinza (#615953). Nenhuma letra, número, logotipo, marca, interface real ou personagem conhecido. Telas mostram só ícones e linhas. Pessoas comuns, de idades e corpos variados, sem rosto detalhado. Formato 4:3, 1200 por 900 pixels, muito espaço livre, nada colado às bordas. Arquivo WebP de até 250 KB. Siga o traço das imagens de referência anexas, familia-produtividade-gig-economy.webp e parte-o-desenho.webp. Cena. Uma mesa de cozinha com prints impressos, o celular, um caderno de anotações e um envelope sendo fechado por duas mãos. Ao fundo, pela janela, um prédio público comum. Evitar. Letras nos prints, no caderno ou no envelope, tribunal, martelo. A armadura do site não aparece.

### procedencia

Gerada com o gerador de imagens do Canva pelo Claude, em 17/11/2026, a partir do campo producao desta peça, das gravuras familia-produtividade-gig-economy e parte-o-desenho. Conferida pelo Claude contra a ideia da peça e publicada por ordem do autor.

### estado

publicada
