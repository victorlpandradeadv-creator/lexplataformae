# Linguagem geométrica da propriedade intelectual

Segundo projeto de ilustrações, a executar depois do plano consolidado de `estrutura/ilustracoes-novas.md`. Rascunho do Claude de 15/11/2026, a partir da proposta do autor de linguagem geométrica para desmistificar a propriedade intelectual e das decisões tomadas na conversa do mesmo dia. É planejamento, e nada daqui está no site.

Os trechos citados passam pelo script, com `python3 ferramentas/conferir_citacoes.py estrutura/ilustracoes-pi.md`.

# 1. Natureza e estatuto

A linguagem dos sólidos é contribuição do autor posterior à tese. Entra no site como acréscimo datado de 15/11/2026, com a marca de acréscimo, como a página do OIFG. A tese não propõe ontologia geométrica da propriedade intelectual. O que ela afirma, e que cada peça ilustra, é a separação entre a exclusividade, que vale no seu plano próprio, e os poderes contratuais e técnicos da plataforma, que não decorrem dela. Toda peça que afirma uma relação jurídica se ancora num trecho da tese ou num dispositivo de lei. A geometria em si fica marcada como acréscimo.

O conceito é Objeto Imaterial de Consumo. A forma Objeto Intelectual de Consumo, que aparece na proposta original, não entra em nenhum texto do projeto.

# 2. Por que é um projeto separado

As 73 peças do primeiro projeto são cenas editoriais com figuras, e o azul marca o que é do leitor. Os sólidos formam outro sistema, abstrato e com semântica própria. Na mesma peça, as duas linguagens se anulariam. O que as une é a paleta, o traço, o papel e duas convenções que este projeto herda sem alterar, a do azul para a posição do consumidor e a do tracejado cinza para a estrutura escondida.

# 3. Os quatro sólidos

| sólido | o que representa | por que a geometria diz isso | operação |
|---|---|---|---|
| cubo | expressão | volume fechado, com faces e arestas definidas, que se identifica como manifestação particular | expressar e delimitar |
| esfera | solução técnica | o que importa está dentro, na estrutura que produz um resultado, e a forma externa é a mais comum de todas | funcionar |
| cilindro | ornamento | tem volume e uma superfície lateral que se desenrola num plano, como as duas formas do desenho industrial, a forma plástica e o padrão de linhas e cores aplicado a um produto | configurar a aparência |
| pirâmide | distintividade | a base é o sinal expressado, e o vértice converge para a origem a que ele aponta | distinguir e apontar origem |

O sólido nunca é o direito. O cubo não é direito autoral, a esfera não é patente, o cilindro não é desenho industrial e a pirâmide não é marca. Cada sólido é uma dimensão do objeto, e o direito é uma incidência possível sobre ela, quando os requisitos legais se cumprem.

A esfera fica só com a dimensão técnica. O ornamento sai dela e vai para o cilindro, para não aproximar visualmente desenho industrial e patente, que é a confusão que o sistema quer desfazer.

# 4. Gramática

| recurso | significado | convenção no desenho |
|---|---|---|
| o papel do site | domínio público, o campo que antecede e excede as exclusividades | nada é desenhado, o fundo é o próprio domínio público |
| sólido em traço simples | dimensão do objeto, antes de qualquer direito | tinta, linha fina, sem preenchimento |
| contorno de incidência | o alcance exato de uma exclusividade | linha dupla fina em tinta, rente ao que ela protege e só a ele |
| estrutura interna visível | organização técnica | corte da esfera com o mecanismo em linha fina |
| pele desenrolada | padrão ornamental separado do objeto | a superfície do cilindro aberta num retângulo ao lado |
| vetor | relação de identificação ou referência | seta fina saindo do vértice da pirâmide |
| transparência | dimensões que coexistem no mesmo objeto | sólidos sobrepostos com as linhas de trás visíveis |
| intersecção | elemento compartilhado entre manifestações | área comum sem contorno de incidência |
| tracejado cinza | poder contratual e técnico da plataforma, que não decorre da exclusividade | a mesma convenção de estrutura escondida do primeiro projeto |
| azul | posição jurídica do consumidor | a mesma convenção do primeiro projeto |
| superfície modificada | mudança de aparência ao longo do tempo | reservada para quando a peça falar da mudança depois da venda |

A cor nunca carrega sozinha o significado. Cada convenção também se distingue pela forma da linha, para funcionar em impressão em preto, para pessoas com baixa visão de cor e no tema escuro.

# 5. Meio de produção

Os sólidos são geometria exata e precisam ser idênticos em todas as aparições, o que é difícil de garantir num gerador de imagens. Por isso este projeto se divide em duas camadas.

A primeira camada são os componentes geométricos, desenhados por código em SVG, por uma ferramenta nova, `ferramentas/solidos.py`. Cada sólido, cada contorno e cada composição sai em vetor, herda as cores do tema, entra no tema escuro sem versão separada, quebra o texto vizinho como os esquemas e passa pelo leitor de tela. É a camada principal.

A segunda camada são poucas cenas editoriais, geradas pela IA, em que os sólidos aparecem dentro de uma situação concreta, como a skin ou a loja. Seguem as regras de produção de `estrutura/ilustracoes-producao.md`, com os sólidos desenhados como referência anexa a partir dos SVG da primeira camada.

# 6. Lugares

A linguagem fica concentrada onde a tese trata da propriedade intelectual, no capítulo Propriedade intelectual da Doutrina, em `doutrina/propriedade-intelectual/`, que segue a ordem do 6.5. Na Informação, a linguagem aparece em só três lugares, para que o leigo encontre o sistema sem precisar aprendê-lo inteiro. Na Ciência, ganha uma página própria que apresenta a gramática.

# 7. As peças

## pi-quatro-solidos

Lugar. Doutrina, capítulo Propriedade intelectual, depois do título Por que a propriedade intelectual da plataforma não é um bloco único?

Camada. SVG

Objetivo. Apresentar os quatro sólidos de uma vez, cada um com o seu nome comum, e mostrar que a propriedade intelectual da plataforma é feita de peças de natureza diferente.

Composição. Os quatro sólidos em linha, em traço simples, sobre o papel, sem nenhum contorno de incidência. Debaixo de cada um, o nome da dimensão, expressão, solução técnica, ornamento e sinal distintivo. Nenhum nome de direito aparece nesta peça.

> A infraestrutura de propriedade intelectual que sustenta a plataforma não é homogênea. Marcas, direitos autorais, software, sinais distintivos, interfaces e institutos conexos não conferem o mesmo tipo nem a mesma extensão de exclusividade. (p. 682)

Texto alternativo. Cubo, esfera, cilindro e pirâmide lado a lado, cada um com o nome da dimensão que representa.

## pi-papel-dominio-publico

Lugar. Doutrina, capítulo Propriedade intelectual, depois do título Por que a questão não é ser contra ou a favor da propriedade intelectual?

Camada. SVG

Objetivo. Fixar que a exclusividade é recorte dentro de um campo maior, e não o mundo dividido em lotes.

Composição. Muitos sólidos pequenos espalhados pelo papel, em traço simples. Um só deles recebe o contorno de incidência, justo, rente a ele. Os demais ficam livres em volta. Uma linha de legenda diz que o papel é o domínio público.

> O princípio continua sendo o da liberdade; a exclusividade é exceção funcionalmente delimitada (Barbosa, 2010, p. 84; p. 537; p. 547). (p. 697)

Texto alternativo. Muitos sólidos soltos sobre o papel, com um só deles envolvido por um contorno duplo justo.

## pi-cubo-software

Lugar. Doutrina, capítulo Propriedade intelectual, depois do título O que a proteção do software autoriza e o que ela não autoriza?

Camada. SVG

Objetivo. Mostrar que a proteção do código não alcança o método de funcionamento nem o resultado que o usuário experimenta.

Composição. Um cubo com o contorno de incidência rente às faces, que representam o código. De dentro dele sai uma esfera pequena, o método, que fica fora do contorno. Ao lado, o resultado da fruição em azul, também fora do contorno.

> A proteção autoral do software não se estende ao método de funcionamento em si mesmo, nem transforma o titular do código em titular absoluto do resultado funcional experimentado pelo usuário (Barbosa, 2017, p. 1890; p. 1899). (p. 687)

Texto alternativo. Cubo com contorno de proteção e, fora do contorno, uma esfera e um elemento azul.

## pi-esfera-tecnica

Lugar. Ciência, página da linguagem geométrica, na apresentação da esfera.

Camada. SVG

Objetivo. Ensinar a ler a esfera pelo que está dentro dela.

Composição. A esfera inteira à esquerda, em traço simples. À direita, a mesma esfera em corte, com um mecanismo simples de engrenagens em linha fina. O contorno de incidência envolve só o mecanismo, e não a casca.

Âncora. Sem trecho da tese. A peça só apresenta a convenção, e por isso é acréscimo datado sem afirmação jurídica.

Texto alternativo. Esfera inteira e a mesma esfera em corte, com o contorno de proteção só em volta do mecanismo interno.

## pi-cilindro-ornamento

Lugar. Doutrina, capítulo Propriedade intelectual, depois do título Por que a marca e o desenho industrial importam do lado do consumidor?

Camada. SVG

Objetivo. Mostrar as duas formas do desenho industrial e que o padrão se aplica ao produto sem se confundir com ele.

Composição. Um cilindro com um padrão de linhas na superfície. Ao lado, a mesma superfície desenrolada num retângulo plano, com o padrão inteiro. O contorno de incidência envolve o retângulo e a silhueta do cilindro, e não o espaço dentro dele.

Âncora. Art. 95 da Lei nº 9.279/1996, com o texto do Planalto copiado pelo navegador quando a peça entrar, como acréscimo.

Texto alternativo. Cilindro com padrão na superfície e, ao lado, a mesma superfície desenrolada, as duas com contorno de proteção.

## pi-piramide-marca

Lugar. Doutrina, capítulo Propriedade intelectual, depois do título Por que a marca e o desenho industrial importam do lado do consumidor?, logo depois de pi-cilindro-ornamento.

Camada. SVG

Objetivo. Mostrar que a marca protege a aptidão do sinal para apontar origem, e não tudo o que o sinal contém.

Composição. Uma pirâmide com uma figura simples desenhada na base. Do vértice sai um vetor fino até um ponto, a origem. O contorno de incidência segue a base e o vetor. A cor e a forma geométrica da figura, que são comuns, ficam fora do contorno.

> Sua proteção não recai apenas sobre uma palavra, figura ou suporte formalmente registrável, mas sobre a aptidão do sinal para apresentar, assinalar, identificar e distinguir produtos ou serviços no tráfego econômico. (p. 687-688)

Texto alternativo. Pirâmide com um sinal na base e um vetor do vértice até a origem, com o contorno de proteção só nesses dois elementos.

## pi-skin-composta

Lugar. Doutrina, capítulo Propriedade intelectual, no caso O que a cláusula de propriedade intelectual dos termos de um jogo revela?

Camada. Cena editorial pela IA, com os sólidos como referência.

Objetivo. Decompor um objeto concreto nas suas dimensões, para mostrar que a skin reúne regimes diferentes, cada um com o seu alcance.

Composição. A armadura canônica de pé, em azul. Em volta dela, em transparência, os quatro sólidos sobrepostos às partes correspondentes, o cubo na arte, a esfera no efeito técnico, o cilindro no padrão da superfície e a pirâmide no emblema. Cada sólido com o seu contorno de incidência. Por fora de tudo, um tracejado cinza mais largo envolve a armadura inteira, o controle da plataforma.

> A cláusula é reveladora porque mostra, sem rodeios, que o controle sobre signos, narrativas, jogabilidade, visuais e conteúdo não é periférico ao fornecimento. É parte da própria infraestrutura pela qual o ambiente é governado. (p. 684)

Texto alternativo. Armadura azul com quatro sólidos sobrepostos às suas partes, cada um com contorno próprio, e um tracejado cinza largo envolvendo tudo.

## pi-exclusividade-e-poder

Lugar. Doutrina, capítulo Propriedade intelectual, depois do título Onde está, afinal, a tensão entre exclusividade e proteção do consumidor? Na Informação, a mesma peça simplificada abre a página do direito j.

Camada. SVG

Objetivo. É a peça central do projeto. Mostra a diferença entre o que a exclusividade protege e o que a plataforma controla por contrato e por técnica.

Composição. Um sólido com o contorno de incidência justo. Em volta, um tracejado cinza muito maior, que alcança também uma figura azul, o consumidor, e o que ele usa. Entre o contorno justo e o tracejado largo fica uma faixa de papel, que é o espaço que a exclusividade não explica.

> A existência de exclusividade juridicamente protegida sobre conteúdos, signos, códigos, sistemas, ativos digitais ou estruturas de plataforma não equivale à legitimação irrestrita do modo como essa exclusividade é exercida no interior da relação de consumo. (p. 737)

Texto alternativo. Sólido com contorno justo de proteção, dentro de um tracejado cinza muito maior que alcança também a figura azul do consumidor.

## pi-licenca

Lugar. Doutrina, capítulo Propriedade intelectual, depois do título Chamar o vínculo de licença afasta o CDC? Na Informação, versão simplificada no problema A empresa diz que eu só tenho uma licença, depois da abertura editorial do primeiro projeto.

Camada. SVG

Objetivo. Mostrar que o nome licença não muda a natureza do que foi fornecido nem afasta a proteção do consumidor.

Composição. A composição de pi-exclusividade-e-poder, com uma etiqueta de papel presa ao tracejado cinza. A figura azul continua dentro, e a etiqueta não muda nenhuma linha do desenho.

> A qualificação jurídica possível preserva a validade da propriedade intelectual em seu plano próprio, mas afasta sua invocação como veto geral à incidência do CDC. (p. 747)

Texto alternativo. O mesmo desenho da exclusividade e do poder da plataforma, com uma etiqueta de licença presa ao tracejado que não muda nada no resto.

## pi-funcao-social

Lugar. Doutrina, capítulo Propriedade intelectual, depois do título O que o art. 5º, XXIX, da Constituição exige da exclusividade?

Camada. SVG

Objetivo. Mostrar que a exclusividade tem direção, e que a Constituição a subordina ao interesse social e ao desenvolvimento.

Composição. Um sólido com o contorno de incidência. Do contorno sai um vetor largo que aponta para fora, para o papel, onde há outros sólidos em formação. A exclusividade aparece como passagem, e não como muro.

> Ao contrário, subordina expressamente a garantia legal do privilégio sobre inventos industriais e da proteção às criações industriais, marcas, nomes de empresa e outros signos distintivos ao interesse social e ao desenvolvimento tecnológico e econômico do País (p. 702)

Texto alternativo. Sólido protegido com um vetor que sai do contorno em direção a outros sólidos em formação no papel.

## pi-latifundio

Lugar. Ciência, página da linguagem geométrica, como contraexemplo.

Camada. SVG

Objetivo. Mostrar o desvio que a linguagem quer evitar, o contorno que cresce além do que protege.

Composição. Um sólido pequeno, com um contorno de incidência que foi inchando em anéis sucessivos até cobrir boa parte do papel e outros sólidos que não lhe pertencem.

> A metáfora do “latifúndio jurídico”, em Dowbor, descreve uma disfunção teleológica interna ao regime de Propriedade Intelectual (p. 235)

Texto alternativo. Sólido pequeno com o contorno de proteção inchado em anéis que cobrem outros sólidos à volta.

## pi-encerramento

Lugar. Doutrina, capítulo Propriedade intelectual, depois do título O que acontece quando o serviço é encerrado?

Camada. SVG

Objetivo. Mostrar que a exclusividade continua íntegra quando o serviço acaba, mas não autoriza apagar o que o consumidor já tinha.

Composição. O contorno de incidência permanece em volta do sólido. O tracejado cinza da plataforma se desfaz. A figura azul continua no papel, com o que já era dela, sem o tracejado em volta.

> A função social da propriedade e da propriedade intelectual impede que a exclusividade opere como título bastante para legitimar o apagamento unilateral desses acervos sob o pretexto de liberdade empresarial, conveniência econômica ou reorientação estratégica do fornecedor. (p. 709)

Texto alternativo. Sólido protegido que continua com o contorno, enquanto o tracejado da plataforma se desfaz e a figura azul permanece no papel.

## pi-convivencia

Lugar. Doutrina, capítulo Propriedade intelectual, depois do título Como o CDC e a propriedade intelectual convivem no exame do caso?

Camada. SVG

Objetivo. Fechar o capítulo com a regra compositiva, a de que os regimes incidem juntos sobre o mesmo problema sem perder a autonomia.

Composição. Os quatro sólidos sobrepostos em transparência, cada um com o seu contorno, e a figura azul no meio. Nenhum contorno engole outro, e nenhum se funde com o tracejado.

> A Constituição, o Código de Defesa do Consumidor e os regimes de propriedade intelectual não incidem aqui como blocos estanques, disputando primazia abstrata, mas como fontes simultaneamente convocadas por um mesmo problema jurídico. (p. 503)

Texto alternativo. Quatro sólidos sobrepostos em transparência, cada um com contorno próprio, com a figura azul no meio.

## pi-escassez

Lugar. Informação, Caminho, parte A lei, ao lado do bloco que trata da propriedade intelectual como estrutura do ambiente.

Camada. SVG simplificado

Objetivo. Dar ao leigo a ideia mais simples do sistema, a de que a exclusividade é uma cerca posta pelo Direito num campo que, sem ela, circularia livre.

Composição. Um único cubo sobre o papel. Uma mão de fora do quadro desenha o contorno de incidência em volta dele. O resto do papel continua livre.

> A própria ideia de propriedade intelectual já nasce como construção normativa de escassez artificial, criada para tornar economicamente apropriável aquilo que, em seu estado natural, circularia sem barreiras equivalentes. (p. 682)

Texto alternativo. Mão desenhando um contorno em volta de um cubo, com o resto do papel livre.

## pi-pagina-linguagem

Lugar. Ciência, página nova `linguagem-geometrica/`, ligada pela página do capítulo Propriedade intelectual e pelas Referências, na seção Ampliações.

Camada. Página com os componentes SVG.

Objetivo. Apresentar a gramática inteira ao especialista, com a origem, os quatro sólidos, a tabela de convenções, os critérios de inteligibilidade e os problemas ainda abertos, para que o sistema possa ser testado e criticado.

Conteúdo. Texto do autor a partir da proposta de 15/11/2026, corrigido pelas decisões do mesmo dia, com a marca de acréscimo posterior. Traz pi-esfera-tecnica, pi-latifundio e uma versão de cada sólido com cada convenção.

# 8. Ferramenta

`ferramentas/solidos.py` desenha os sólidos em SVG por projeção isométrica fixa, com o mesmo ângulo e a mesma espessura de linha em todas as peças. Recebe uma composição descrita em texto, no mesmo espírito de `estrutura/esquemas.md`, com sólidos, posições, contornos, vetores e tracejados. Usa `currentColor` e as variáveis de cor do site, de modo que o tema escuro sai sem versão própria. Cada SVG traz título e descrição para leitor de tela, e o texto alternativo deste plano.

As peças entram pelo mesmo mecanismo dos esquemas, com o campo `pagina` e o campo `posicao` antes ou depois de um título.

# 9. Testes de inteligibilidade

Antes de a linguagem passar às cenas editoriais, cada convenção é testada sozinha. O teste mostra a peça sem legenda a leitores que não conhecem o sistema e pergunta o que ela diz. Uma convenção que precise de legenda em mais da metade das leituras é redesenhada. O leitor leigo simulado faz a primeira rodada, e o autor decide se convém um teste com pessoas reais.

# 10. Ordem de execução

Primeiro a ferramenta e os quatro sólidos isolados, vistos pelo autor no ar. Depois as peças da Doutrina, na ordem do capítulo. Depois a página da Ciência. Por último as três peças da Informação e a cena editorial da skin, que só sai depois que as convenções passarem no teste.

# 11. Problemas ainda abertos

O contorno duplo para a incidência precisa ser testado contra o contorno simples dos sólidos, porque os dois são linhas em tinta.

A intersecção sem contorno pode ser lida como área livre, quando a regra é que fora de uma exclusividade pode haver outra proteção. Talvez peça uma convenção própria.

A figura azul do consumidor é a única figura humana do sistema. Resta decidir se ela é um ponto, um sólido próprio ou uma silhueta.

O art. 95 da Lei de Propriedade Industrial ainda precisa entrar em `estrutura/dispositivos-planalto.json`, com o texto oficial.
