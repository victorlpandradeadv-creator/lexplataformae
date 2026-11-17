# Roteiro de alterações das ilustrações

Roteiro de 17/11/2026, escrito pelo Claude a pedido do autor, para abrir uma nova conversa de trabalho no repositório `lexplataformae`. A nova sessão deve ler o `CLAUDE.md` antes deste arquivo e seguir as regras dele. Todas as regras de estilo valem também aqui. A prosa do site não usa ponto e vírgula, dois pontos nem travessão. Toda frase explicativa se ancora em página da tese. Citações são literais e passam pelo `ferramentas/conferir_citacoes.py`. Toda mudança vai ao ar no `main` logo depois de conferida.

O autor viu `direitos/b/` no ar e disse que a linha de ilustrações atual não pode prosperar. Ele pediu um roteiro que corrigisse todos os pontos levantados e recriasse as ilustrações problemáticas, com a posição sustentada caso o todo devesse ser trocado. Este roteiro sustenta essa posição para a linha atual e propõe voltar a uma linha que o próprio site já teve.

## 1. Diagnóstico

### 1.1 O que está no ar hoje

No `main`, depois do commit `43cf9af2` (17/11/2026, Ilustrações da entrega de 16/11/2026 no site, com vinhetas nas portas e nos direitos), convivem cinco conjuntos.

1. **Pictogramas planos da entrega do GPT de 16/11** (Família 3), em `site/ilustracoes/`. Substituíram as 29 gravuras de 12/11 em `caminho/*`, `conceitos/<nove>/`, `plataformas/` e na capa. São quadrados azuis, traços, portões, pontos e a armadura azul solta no papel.
2. **Vinhetas quadradas de 480 px**, das Famílias 1 e 2 da mesma entrega. São `porta-*.webp` (seis, nos cartões da capa) e `direito-a.webp` a `direito-k.webp` (onze, no alto de `direitos/<letra>/`), postas pela função `vinheta()` de `ferramentas/gerar_site.py`.
3. **32 composições SVG interativas** desenhadas por código (`ferramentas/ilustracoes.py`, fragmentos em `site/ilustracoes-svg/`). Aparecem nos 24 problemas, nas quatro famílias de plataforma, em `caminho/o-nome/`, `direitos/`, `alem-do-consumo/` e `como-reclamar/`. A função `figura()` dá preferência ao SVG sobre o WebP quando os dois existem.
4. **Linguagem geométrica da propriedade intelectual** (`site/linguagem-pi/`, 19 peças) e as três peças `pi-skin-*.webp`, no capítulo `doutrina/propriedade-intelectual/` e na página `linguagem-geometrica/` da Ciência.
5. **Quatro gravuras das famílias** (`familia-*.webp`), que existem no disco, mas ficam escondidas porque o SVG da mesma peça ganha.

### 1.2 Por que a linha atual fracassa

1. **Fala um código privado.** O quadrado azul quer dizer skin, moeda, dado, loja, prova ou pedido, conforme a página. O portão, o ponto e o traço não têm significado fixo. O leigo não decodifica nada sem legenda, e a legenda não aparece na Informação. Em `direitos/b/`, cujo título é A plataforma não pode montar a experiência para você não entender, a imagem é um ponto azul e três traços.
2. **Não mostra o que a página conta.** As páginas falam de conta banida, item alterado, cronômetro de oferta, termos de uso e protocolo de atendimento. Os desenhos mostram relações abstratas entre formas. A ilustração devia ser o primeiro lugar onde o leitor reconhece o próprio caso.
3. **Três linguagens brigam no mesmo site.** Gravura com gente, armadura azul solta e pictograma plano. O leitor não sabe qual é a voz visual do projeto.
4. **Esconde o que era bom.** As gravuras de 12/11 saíram do ar. As quatro gravuras das famílias e a de Ísis e Rá ficam escondidas pelo SVG.
5. **Escala errada.** A vinheta de 480 px vira um glifo pequeno num vão vazio, como no alto de `direitos/b/`. Contraria a regra do autor de 05/11/2026 sobre texto e peça presos num canto sem nada do outro lado.
6. **Desrespeita o próprio plano.** O plano de `estrutura/ilustracoes.md` pede metáfora visual com lastro no trecho, gente sem rosto definido e azul só no objeto comprado ou prometido. As peças de 16/11 abandonaram a metáfora e espalharam o azul por todo elemento.

### 1.3 A posição

A linha atual deve ser trocada inteira, e não remendada. O problema não está numa peça ou outra. Está na gramática, que troca a cena pelo símbolo, e nenhum ajuste de cor, escala ou legenda corrige isso. Os pictogramas de 16/11, as vinhetas das portas e dos direitos e as 32 composições SVG saem do ar. A única exceção é a armadura suspensa da capa, que o autor manteve (2.0).

A troca não começa do zero. O site já teve a linha certa. As 29 gravuras de 12/11 (commit `62bc844e`, Publica as 29 ilustrações conceituais) seguem o plano, têm metáfora com lastro, gente, cenário e azul só no objeto. As quatro gravuras das famílias, feitas na mesma mão, provam que a linha se sustenta fora do caminho da skin. A nova linha única do site é essa gravura editorial, e tudo o que falta será desenhado nela.

Fica uma exceção, só a linguagem geométrica da propriedade intelectual. Ela é um código, mas um código ensinado, com página própria na Ciência que explica cada sólido. No capítulo da Doutrina ela funciona porque o leitor é jurista e a convenção vem explicada. Não vai para nenhuma página da Informação.

### 1.4 O critério de aceite de qualquer peça

Uma ilustração entra no site se cumprir as quatro condições.

1. Um leigo, sem ler legenda, consegue dizer que situação ela mostra.
2. Essa situação é a da página onde ela está, e não outra.
3. A cena se ancora num trecho literal da tese, conferido pelo script, ou, nas peças de acréscimo posterior, num fato documentado e datado.
4. O azul Klein marca só o objeto em jogo, aquilo que foi comprado, prometido ou perdido.

## 2. Fase 1. Restauração imediata

Objetivo. Tirar do ar o que não comunica e devolver o que já comunicava, sem produzir nada novo. Uma sessão, um commit, publicado no `main`.

### 2.0 A armadura suspensa da capa não muda

Por decisão do autor de 17/11/2026, a peça `inicio.webp` que está hoje na capa fica como está. É a armadura azul de pé sobre a plataforma presa por dois fios, da entrega de 16/11. O autor a considera a única peça decente dessa entrega, e ela passa no critério do 1.4, porque o leitor vê que o chão é sustentado por outro. Não recuperar a versão de 12/11 dessa peça, nem a escura. A legenda dela, Parece terreno seu, mas é chão emprestado, já ficou centrada sob a figura em 17/11/2026.

### 2.1 Devolver as 29 gravuras de 12/11

1. Recuperar do git os arquivos claros de `62bc844e` e os escuros de `8ce2572b` (15/11/2026, negativo calculado em OKLab), para os 28 ids abaixo. Exemplo `git show 62bc844e:site/ilustracoes/parte-a-compra.webp > site/ilustracoes/parte-a-compra.webp` e `git show 8ce2572b:site/ilustracoes/parte-a-compra-escuro.webp > site/ilustracoes/parte-a-compra-escuro.webp`.
   - Plataformas. `laboratorio`. A capa não entra, pelo 2.0.
   - Caminho. `parte-a-compra`, `parte-o-desejo`, `parte-o-dono`, `parte-as-regras`, `parte-o-normal`, `parte-a-mudanca`, `parte-o-desenho`, `parte-a-lei`, `parte-a-resposta`, `parte-alem-do-jogo`, `parte-o-nome`.
   - Peças dentro do caminho. `imagem-catraca`, `imagem-estoque-fluxo`, `imagem-torneira`.
   - Vocabulário. `ideia-oic`, `ideia-lex-plataformae`, `ideia-vulnerabilidade-semiotica`, `ideia-teleologia-abusiva`, `ideia-ilicito-de-arquitetura`, `ideia-antecipacao-hipercuratorial`, `ideia-auditabilidade-aberta`, `ideia-equivalencia-de-valor-funcional`, `ideia-feixe-de-fruicao-governada`.
   - Famílias. `familia-funcionalidade-cognitiva`, `familia-infraestrutura-e-intermediacao`, `familia-produtividade-gig-economy`, `familia-administracao-de-confianca`.
2. Devolver ao fim de `site/extra.css` o filtro do negativo parcial que o `43cf9af2` tirou, porque as versões escuras de 15/11 dependem dele.
   ```
   /* 15/11/2026. Negativo parcial no tema escuro, por ordem do autor. Fundo um tom acima do papel e traço menos claro. */
   :root[data-theme="dark"] .ilustracao .arte-escura { filter:brightness(1.55) contrast(.78); border-radius:3px; }
   @media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .ilustracao .arte-escura { filter:brightness(1.55) contrast(.78); border-radius:3px; } }
   ```
3. Conferir no navegador, nos dois temas, `caminho/a-compra/`, `conceitos/oic/` e `plataformas/funcionalidade-cognitiva/`.

### 2.2 Tirar os SVG interativos de todas as páginas

1. Em `figura()`, deixar de preferir `figura_svg()`. O WebP do plano vale sempre. A chamada de `figura_svg()` sai também do ramo em que a peça não está no plano.
2. Esvaziar `ILUSTRACAO_PAGINA` e tirar a inserção dos `problema-*` em `pagina()`. Os problemas, `direitos/`, `alem-do-consumo/` e `como-reclamar/` ficam sem ilustração até a Fase 3.
3. Não apagar `site/ilustracoes-svg/`, `site/ilustracoes.css`, `site/ilustracoes.js` nem `ferramentas/ilustracoes.py`. Mover os fragmentos para `estrutura/rascunhos/ilustracoes-svg/arquivo-2026-11-17/` e deixar de copiar o CSS e o JS do componente para `docs/` enquanto nenhuma página o usar. O componente de peças tocáveis pode voltar na Fase 5, sobre as gravuras.

### 2.3 Tirar as vinhetas

1. `vinheta()` deixa de ser chamada na capa (portas) e em `direitos/<letra>/`. Os arquivos `porta-*.webp` e `direito-*.webp` vão para `estrutura/rascunhos/vinhetas-2026-11-16/`.
2. Os pictogramas da Família 3 que as gravuras substituem não ficam no site, salvo `inicio`. Mover para `estrutura/rascunhos/familia-3-2026-11-16/` os que não forem sobrescritos pelo passo 2.1. Os `pi-skin-*.webp` ficam, porque pertencem ao capítulo de PI.

### 2.4 Registro e publicação

1. Em `estrutura/ilustracoes.md`, o campo `procedencia` das 28 peças devolvidas volta a dizer gerada com o ChatGPT em 12/11/2026. Acrescentar uma linha datada de 17/11/2026 que explica a devolução.
2. No `CLAUDE.md`, os itens 8 e 9 da lista de desenvolvimento ganham uma linha datada que diz que a linha de 16/11 saiu do ar por decisão do autor e que as gravuras de 12/11 voltaram. Acrescentar em Decisões tomadas a regra da linha única do 1.3 e o critério do 1.4.
3. Rodar `python3 ferramentas/gerar_site.py`, `python3 -I ferramentas/checar_site.py docs` e `python3 -I ferramentas/revisar_fontes.py`. Gerar os cartões se algum depender das ilustrações. Commit e push para `main` e para o ramo de trabalho.

## 3. Fase 2. Revisão das 29 gravuras devolvidas

Cada gravura foi lida pelo critério do 1.4. Vinte e sete ficam como estão. Duas devem ser refeitas, e uma terceira fica como candidata.

| Peça | Página | Decisão | Por quê |
|---|---|---|---|
| inicio | capa da Informação | fica a de 16/11 | A armadura suspensa por fios, que está no ar. Decisão do autor, pelo 2.0. O chão emprestado da p. 791 se lê sem legenda. |
| laboratorio | `plataformas/` | fica | Lente sobre quatro mesas de plataformas diferentes. Mostra o exame de vários ambientes. |
| parte-a-compra | `caminho/a-compra/` | fica | O elmo sai da caixa, e um fio volta para a loja (p. 408). |
| parte-o-desejo | `caminho/o-desejo/` | fica | A armadura no centro dos olhares. O valor vem de ser vista. |
| parte-o-dono | `caminho/o-dono/` | fica | O castelo de servidores sobre as pessoas que jogam. |
| parte-as-regras | `caminho/as-regras/` | fica | Labirinto de folhas de termos com o carimbo de uma mão de fora. |
| parte-o-normal | `caminho/o-normal/` | fica | Chuva fabricada por uma estrutura de palco, e todos de guarda-chuva como se fosse natural. |
| parte-a-mudanca | `caminho/a-mudanca/` | fica | A mesma armadura cheia e oca, lado a lado. |
| parte-o-desenho | `caminho/o-desenho/` | fica | A planta da loja com os caminhos que levam ao caixa. |
| parte-a-lei | `caminho/a-lei/` | **refazer** | O prédio azul sobre a fundação só se entende junto com ideia-oic. Sozinho, não diz que a lei já tem resposta. Ver 3.1. |
| parte-a-resposta | `caminho/a-resposta/` | fica | Mesa com balança, mapa e a peça azul devolvida. |
| parte-alem-do-jogo | `caminho/alem-do-jogo/` | fica | Os mesmos fios descendo de vários serviços para pessoas diferentes. |
| parte-o-nome | `caminho/o-nome/` | fica | Ísis e Rá. Composição solene, coerente com o traço. |
| imagem-catraca | `caminho/a-compra/` | fica | A catraca no caminho de quem quer continuar no jardim. |
| imagem-estoque-fluxo | `caminho/a-compra/` | fica | Gaveta parada ao lado do cano em fluxo. |
| imagem-torneira | `caminho/o-dono/` | fica | A torneira que pinga o valor no balde. |
| ideia-oic | `conceitos/oic/` | fica | Estrutura azul sobre fundação, com a armadura em cima. Na página do conceito a legenda explica. |
| ideia-lex-plataformae | `conceitos/lex-plataformae/` | **refazer** | O livro com engrenagens não mostra quem faz a regra nem sobre quem ela cai. Ver 3.2. |
| ideia-vulnerabilidade-semiotica | `conceitos/vulnerabilidade-semiotica/` | fica | A pessoa competente com o cartão de sinais e o vendedor com a lupa (p. 322). |
| ideia-teleologia-abusiva | `conceitos/teleologia-abusiva/` | fica | Portas em degraus que só levam à caixa azul, sem ninguém empurrando (p. 448 e 732). |
| ideia-ilicito-de-arquitetura | `conceitos/ilicito-de-arquitetura/` | fica | Corte de um prédio em que os caminhos levam sempre ao mesmo lugar. |
| ideia-antecipacao-hipercuratorial | `conceitos/antecipacao-hipercuratorial/` | fica | Sala de espera, relógio, porta fechada e o tapete azul (p. 314). |
| ideia-auditabilidade-aberta | `conceitos/auditabilidade-aberta/` | fica | Pessoas olhando o mecanismo por uma janela na caixa (p. 728). |
| ideia-equivalencia-de-valor-funcional | `conceitos/equivalencia-de-valor-funcional/` | fica | Balança com a armadura cheia e a oca. |
| ideia-feixe-de-fruicao-governada | `conceitos/feixe-de-fruicao-governada/` | fica | Feixe de fios azuis seguro pela pessoa e passando por roldanas da plataforma. |
| familia-funcionalidade-cognitiva | `plataformas/funcionalidade-cognitiva/` | fica | O balão de fala azul com um botão regulado por uma mão de fora. |
| familia-infraestrutura-e-intermediacao | `plataformas/infraestrutura-e-intermediacao/` | fica | Vitrine com lentes que realçam uns produtos e apagam outros. |
| familia-produtividade-gig-economy | `plataformas/produtividade-gig-economy/` | fica | A entregadora no mapa enquanto uma mão de fora desenha a rota. |
| familia-administracao-de-confianca | `plataformas/administracao-de-confianca/` | fica | O canto da mesa acolchoado com um sorriso, para ninguém perceber a quina. |

Candidata. `parte-o-desejo` funciona, mas os rostos de perfil em busto lembram estatuária e destoam do resto. Se o autor quiser, refazer com pessoas comuns num saguão de jogo, mantendo a armadura no centro.

### 3.1 parte-a-lei, nova versão

- **Página.** `caminho/a-lei/`, A lei já tem resposta?
- **Por que refazer.** A peça atual depende do díptico com ideia-oic. O leitor da parte 8 não viu ideia-oic.
- **Cena.** Uma pessoa sentada num balcão de atendimento público, de frente para uma atendente. Na mesa, o celular da pessoa com a armadura azul na tela, ao lado de um livro grosso aberto. Do livro saem linhas tracejadas cinza que chegam à armadura na tela, como se o livro já tivesse um lugar para ela. Atrás, a sala de um órgão público comum, sem bandeira nem brasão.
- **Azul.** Só a armadura na tela.
- **Âncora.** O trecho que abre a parte 8 em `conteudo/percurso.md`, sobre o CDC como infraestrutura (seção 6.2), conferido pelo script.
- **Evitar.** Tribunal, martelo, toga, balança de justiça, qualquer palavra no livro.
- **Alt.** Uma pessoa mostra o celular com a armadura a uma atendente, e um livro aberto na mesa liga-se à armadura por linhas finas.
- **Legenda.** A lei já tinha lugar para o que você comprou.

### 3.2 ideia-lex-plataformae, nova versão

- **Página.** `conceitos/lex-plataformae/`, a lei da plataforma.
- **Por que refazer.** O livro de engrenagens não mostra quem faz a regra, nem sobre quem ela cai, nem que ela muda com o jogo em andamento.
- **Cena.** Uma praça cercada, vista de cima e de lado, onde pessoas convivem, jogam e trocam objetos. Num muro da praça, um quadro de regras grande. Uma mão que vem de fora do quadro apaga uma linha e escreve outra, enquanto as pessoas continuam lá dentro sem parar. Algumas olham para o quadro, outras não percebem.
- **Azul.** Os objetos que as pessoas carregam.
- **Estrutura cinza tracejada.** Os fios do muro que ligam o quadro à mão de fora.
- **Âncora.** A glosa do nome na nota 5 da p. 27 e a passagem do capítulo 3 sobre o ambiente governado. A nova sessão escolhe o trecho literal com `ferramentas/buscar_tese.py` e confere.
- **Evitar.** Letras no quadro. Usar riscos e linhas como escrita ilegível.
- **Alt.** Numa praça cercada, uma mão de fora apaga e reescreve o quadro de regras enquanto as pessoas continuam lá dentro.
- **Legenda.** A regra muda com você dentro.

## 4. Fase 3. Peças novas

São as páginas que hoje ficariam sem imagem depois da Fase 1. Todas na linha única da gravura editorial.

### 4.1 Direção de arte comum às peças novas

Vale a direção de arte de `estrutura/ilustracoes.md`, com cinco acréscimos.

1. **Mesma mão das gravuras de 12/11.** Traço fino a nanquim, hachura discreta, papel quente (#faf6ef), azul Klein chapado (#002fa7) e estrutura escondida em tracejado cinza (#615953). A encomenda deve anexar duas gravuras de referência, `familia-produtividade-gig-economy.webp` e `parte-o-desenho.webp`, para o gerador copiar o traço.
2. **Telas sem texto.** Quando a cena precisa de uma tela de celular, o conteúdo dela é desenhado com sinais visuais, como cadeado, ampulheta, relógio, seta, carrinho, presente, estrela ou lixeira. Nenhuma letra ou número. Linhas cinza fazem as vezes de texto.
3. **Gente comum.** Idades, corpos e trabalhos variados, sem rosto detalhado e sem pessoa real. Uma mesma pessoa pode reaparecer na mesma página, mas não há personagem fixo no site.
4. **A armadura só onde a skin é o assunto.** Nos direitos e nos problemas de jogo, o objeto em jogo é a armadura canônica de `estrutura/referencias-visuais/armadura.webp`, pequena, na tela do celular ou no inventário. Nos problemas de outras plataformas, o objeto azul é o do próprio caso, como a comunidade, o pedido, a loja ou a conversa.
5. **Formatos.** Abertura de problema e de história, 16 x 9, 1600 por 900. Direito, 4 x 3, 1200 por 900, posto no alto da página como figura comum, e não como vinheta. Porta da capa, 4 x 3, 1200 por 900, na largura do cartão. Até 250 KB. Versão escura gerada pelo `ferramentas/negativo.py` e ajustada pelo filtro do negativo parcial, salvo decisão diferente do autor.

### 4.2 Modelo de encomenda

Cada peça nova entra em `estrutura/ilustracoes.md` antes da geração, com os campos `pagina`, `formato`, `prioridade`, `ideia`, o trecho literal com página (que o script confere), `alt`, `legenda`, `producao`, `procedencia` e `estado`. O pedido ao gerador de imagens segue este molde.

```
Ilustração editorial em gravura a nanquim, traço fino e hachura discreta, sobre papel creme (#faf6ef).
Uma só cor além do preto, o azul Klein chapado (#002fa7), usado apenas em [OBJETO AZUL].
Estruturas escondidas em linhas tracejadas cinza (#615953).
Nenhuma letra, número, logotipo, marca, interface real ou personagem conhecido. Telas mostram só ícones e linhas.
Pessoas comuns, de idades e corpos variados, sem rosto detalhado.
Formato [16:9 | 4:3 | 1:1], [LARGURA] por [ALTURA] pixels, muito espaço livre, nada colado às bordas.
Siga o traço das imagens de referência anexas.
Cena. [CENA]
Evitar. [EVITAR]
```

A nova sessão escreve o `producao` de cada peça a partir deste roteiro. O autor gera as imagens com o ChatGPT, como fez em 12/11. O Claude confere cada arquivo pelo critério do 1.4 antes de pôr no site.

### 4.3 Seus direitos, onze peças 4 x 3

Lugar. Alto de `direitos/<letra>/`, logo depois do título, por `figura("direito-<letra>")`. Os ids passam a `direito-a` a `direito-k` no plano, com arquivos novos.

**direito-a. O que você comprou é produto, mesmo sem nada nas mãos** (p. 743, 718, 435)
- **Falha atual.** Um cubo azul de contorno. Diz caixa, e não compra digital.
- **Cena.** Uma pessoa no sofá olhando o celular. Na tela, a armadura acaba de cair no inventário, com um sinal de confirmação. Ao lado, numa mesinha, a nota fiscal de papel de uma compra comum, uma caixa de sapato aberta. As duas compras estão em pé de igualdade na composição, com a mesma luz e o mesmo peso.
- **Azul.** A armadura na tela.
- **Alt.** Uma pessoa vê no celular o item que acabou de comprar, ao lado de uma caixa de sapatos aberta.
- **Legenda.** As duas são compras.

**direito-b. A plataforma não pode montar a experiência para você não entender** (p. 744, 719, 720, 607)
- **Falha atual.** Ponto azul e três traços. É a peça que o autor apontou.
- **Cena.** Close de um celular segurado por duas mãos. A tela é uma loja de jogo carregada. No centro, um botão enorme com um carrinho, a armadura em destaque com brilho e um relógio de areia correndo no canto. Embaixo, quase invisível, uma linha cinza minúscula com um pequeno ícone de documento, o caminho para as condições. O polegar está a caminho do botão grande.
- **Azul.** A armadura na vitrine da tela.
- **Estrutura cinza.** Linhas tracejadas finas mostram que a tela tem camadas por trás.
- **Alt.** Num celular, uma loja de jogo com um botão de compra enorme e um relógio correndo, enquanto o acesso às condições é uma linha quase invisível.
- **Legenda.** Tudo grande para comprar, tudo pequeno para entender.

**direito-c. A informação precisa servir para alguma coisa** (p. 744, 641, 401)
- **Falha atual.** Um documento com linhas. Não mostra informação inútil nem útil.
- **Cena.** Duas metades. À esquerda, uma pessoa diante de um rolo de papel que desce do celular e se acumula no chão em montes, de tão comprido. À direita, a mesma pessoa segurando um cartão pequeno com três ícones grandes e claros, um relógio, uma seta de mudança e um item riscado.
- **Azul.** O cartão útil.
- **Alt.** Uma pessoa soterrada por um rolo de termos e, ao lado, a mesma pessoa lendo um cartão curto com três sinais claros.
- **Legenda.** Muita informação não é informação.

**direito-d. O que foi prometido precisa ser entregue** (p. 744-745, 745)
- **Falha atual.** Quadrado e losango ligados a um quadrado vazio.
- **Cena.** Um outdoor de rua mostra a armadura cercada de raios, faíscas e efeitos. Embaixo do outdoor, uma pessoa abre o celular, e na tela a mesma armadura aparece sem nenhum dos efeitos, opaca. A pessoa olha de um para o outro.
- **Azul.** As duas armaduras, a do anúncio cheia e a da tela sem brilho.
- **Alt.** Uma pessoa compara a armadura cheia de efeitos de um anúncio de rua com a armadura apagada que recebeu no celular.
- **Legenda.** O anúncio também é promessa.

**direito-e. Mudança relevante precisa deixar rastro** (p. 745, 641, 648, 643, 642)
- **Falha atual.** Traços e um quadrado azul sem relação visível.
- **Cena.** Neve fresca num pátio. Pegadas atravessam o pátio até uma vitrine onde a armadura mudou de forma. Uma das pegadas está sendo apagada por uma vassoura empunhada por uma mão que sai de uma porta lateral. Uma pessoa, de casaco, segue as pegadas que restam com o celular na mão.
- **Azul.** A armadura na vitrine.
- **Alt.** Pegadas na neve levam a uma vitrine onde a armadura mudou, e uma vassoura apaga parte delas.
- **Legenda.** Quem muda deixa rastro. Ou deveria.

**direito-f. Mudou, tem que manter o que valia** (p. 745, 637, 635, 745-746, 746, 730)
- **Falha atual.** Quadrado e círculo sobre traços.
- **Cena.** Uma balança de feira. Num prato, a armadura antiga, cheia. No outro, a nova, com outro desenho, mas do mesmo peso, e a balança em equilíbrio. Uma pessoa confere o fiel da balança de perto. Atrás, na parede, a sombra da armadura antiga.
- **Azul.** As duas armaduras.
- **Alt.** Uma balança equilibra a armadura antiga e a nova, de desenhos diferentes, e uma pessoa confere o equilíbrio.
- **Legenda.** Pode mudar a forma. O valor tem de ficar.
- **Nota.** Evitar repetir a composição de ideia-equivalencia-de-valor-funcional. Aqui a balança está em equilíbrio e as armaduras diferem só na forma. No conceito, uma está oca.

**direito-g. Punição precisa de motivo e de chance de defesa** (p. 746, 749, 211, 408)
- **Falha atual.** Dois retângulos e um balão.
- **Cena.** Uma pessoa diante de uma porta de vidro fechada, com um cadeado grande. Do outro lado do vidro, o inventário dela, com a armadura, pendurado num armário. Na porta, uma campainha. A pessoa aperta a campainha, e o fio da campainha dá a volta e volta para o próprio botão, sem chegar a lugar nenhum.
- **Azul.** A armadura atrás do vidro.
- **Estrutura cinza.** O fio da campainha em laço.
- **Alt.** Uma pessoa trancada do lado de fora vê a própria armadura atrás do vidro e aperta uma campainha cujo fio volta para ela mesma.
- **Legenda.** Trancar exige motivo. E alguém do outro lado.

**direito-h. Quando a perda é regra, o problema é o desenho** (p. 746, 732, 746-747, 747)
- **Falha atual.** Linhas paralelas.
- **Cena.** Uma máquina de parque de diversões, tipo garra de pegar bichinho. Dentro, a armadura no alto, fora do alcance. A garra é desenhada frouxa, aberta demais. Do lado, uma fila de pessoas com moedas na mão, e no chão um pote de moedas cheio. Linhas tracejadas cinza mostram o mecanismo da garra por dentro da máquina, regulado para soltar.
- **Azul.** A armadura dentro da máquina.
- **Alt.** Uma fila espera diante de uma máquina de garra em que a armadura fica fora do alcance, e o mecanismo aparece regulado para soltar.
- **Legenda.** Quando ninguém consegue, o problema é a máquina.

**direito-i. A prova que está com a plataforma tem que aparecer** (p. 747, 736)
- **Falha atual.** Um círculo ligado a uma barra azul.
- **Cena.** Duas metades. À esquerda, uma pessoa sentada à mesa da cozinha com prints espalhados e o celular. À direita, uma sala de servidores atrás de uma grade, com caixas arquivadas em prateleiras altas. Entre as metades, uma mão de juiz, só a manga e a mão, aponta para a grade pedindo que ela abra.
- **Azul.** Uma das caixas na prateleira, a que guarda o registro do caso.
- **Alt.** Uma pessoa com prints na mesa de casa, e ao lado uma sala de arquivos trancada, para a qual uma mão aponta pedindo abertura.
- **Legenda.** Quem guarda a prova tem de mostrá-la.

**direito-j. Ser dona da obra não é desculpa para tudo** (p. 747, 702, 130, 54, 748, 709)
- **Falha atual.** Uma chave e uma barra.
- **Cena.** Um ateliê com uma grande tela pintada que é o cenário do jogo. O artista, dono da obra, está ao lado. Diante da tela, pessoas que compraram a armadura usam essa armadura dentro da pintura. O artista ergue um pano para cobrir a tela inteira. Uma moldura tracejada cinza em volta das pessoas mostra que a parte delas não é dele cobrir.
- **Azul.** As armaduras das pessoas dentro da pintura.
- **Alt.** Um artista vai cobrir com um pano a tela em que pessoas usam as armaduras que compraram, e uma moldura em volta delas mostra o que não é só dele.
- **Legenda.** A obra é da empresa. A compra é sua.

**direito-k. A resposta deve recompor o que você perdeu** (p. 748, 742)
- **Falha atual.** Um bloco azul recortado.
- **Cena.** Uma mesa de restaurador. As peças da armadura, que estavam quebradas, são encaixadas de volta por duas mãos com luvas finas. Ao lado, uma folha com o desenho da armadura inteira, que serve de molde. Uma pessoa observa da porta.
- **Azul.** As peças da armadura.
- **Alt.** Mãos de restaurador encaixam as peças da armadura de volta, guiadas pelo desenho dela inteira.
- **Legenda.** Responder é pôr de volta o que foi tirado.

### 4.4 Capa da Informação, seis portas

**O que há na capa hoje.** Lido em 17/11/2026, nos três modos.
- Seis vinhetas geométricas, uma em cada cartão de Comece pelo que aconteceu (`porta-acesso`, `porta-mudou`, `porta-empurrado`, `porta-sair`, `porta-decide`, `porta-comum`), postas por `vinheta()`. São a primeira imagem que o leitor vê depois do título, e nenhuma se lê. Saem na Fase 1 (2.3) e voltam aqui, refeitas.
- A armadura suspensa (`inicio.webp`), que fica, pelo 2.0.
- O mapa Qual destas é a sua história?, que é diagrama de navegação feito pelo gerador, e não ilustração. Fica fora desta revisão.
- Os quatro passos de Como a perda acontece e o convite ao jurista não têm imagem, e continuam sem.

**Lugar e formato.** Alto de cada cartão, ocupando a largura inteira do cartão, em 4 x 3, 1200 por 900. Sai o glifo pequeno no canto. No celular, o cartão vira coluna e a imagem continua na largura toda. As seis peças devem ter a mesma altura e o mesmo enquadramento, porque os cartões estão lado a lado (regra de 12/11/2026, cartões na mesma linha seguem o mesmo contrato).

**Regra própria das portas.** A capa da Informação é universal desde 17/11/2026, por crítica do autor. As portas não podem falar só de jogo. A armadura não aparece aqui. Cada porta mostra um objeto do dia a dia digital, e o conjunto das seis deve variar entre jogo, rede social, compra online, aplicativo de trabalho e assistente, para que qualquer leitor se ache em ao menos uma.

**Texto alternativo.** A imagem é decorativa dentro de um cartão que já tem título e frase, e por isso continua com `alt` vazio no site. O campo `alt` do plano fica preenchido para a encomenda e para a Ciência.

**porta-acesso. Perdi o acesso.**
- **Falha atual.** Um traço, uma barra vertical e um quadrado azul. Ninguém lê porta trancada.
- **Âncora.** p. 155, a perda da conta, dos dados e do conteúdo virtual com o encerramento.
- **Cena.** Uma pessoa diante da porta de vidro de um prédio, à noite, com a chave na mão. A chave não entra, porque a fechadura foi trocada por uma tampa lisa. Através do vidro, na sala iluminada, as coisas dela continuam nas prateleiras, um controle de jogo, um álbum de fotos e uma caixa de compras.
- **Azul.** As coisas dela atrás do vidro.
- **Evitar.** Arrombamento, polícia, alarme, qualquer sinal de crime.
- **Alt do plano.** Uma pessoa com a chave na mão diante de uma porta sem fechadura, vendo as próprias coisas do outro lado do vidro.

**porta-mudou. O que comprei mudou.**
- **Falha atual.** Dois quadrados azuis sobre suportes. Não mostra mudança nenhuma.
- **Âncora.** p. 104, a promessa que fica na conta e perde o encaixe que lhe dava valor.
- **Cena.** Uma pessoa segura um objeto que comprou, uma luminária de mesa. A luminária continua igual por fora, mas a lâmpada, que acendia forte na caixa aberta ao lado, agora mal acende. Na parede, a sombra da luz antiga, grande, e a da luz de agora, pequena.
- **Azul.** A luz, a antiga na sombra da parede e a fraca na lâmpada.
- **Evitar.** Quebra visível. O objeto continua inteiro. O que mudou foi o que ele faz.
- **Alt do plano.** Uma pessoa segura uma luminária que continua igual por fora, mas acende muito menos do que acendia quando foi comprada.

**porta-empurrado. Fui empurrado a pagar.**
- **Falha atual.** Duas linhas convergindo para um círculo azul.
- **Âncora.** p. 670, o programa de funcionamento que comprime o tempo de reflexão e dificulta a reversão.
- **Cena.** Uma pessoa sobre uma esteira rolante de aeroporto que termina num caixa. Ela tenta andar para trás e não sai do lugar. Nas paredes da esteira, relógios correndo e setas grandes, todas apontando para o caixa. Ao lado da esteira, fora dela, uma escada comum, vazia, que leva para fora.
- **Azul.** O cartão de pagamento na mão da pessoa.
- **Alt do plano.** Uma pessoa numa esteira rolante que só leva ao caixa, cercada de relógios e setas, enquanto a saída fica de lado.

**porta-sair. Quero sair e levar o que é meu.**
- **Falha atual.** Uma barra, um traço e três quadrados azuis.
- **Âncora.** p. 217, o custo de saída, que inclui histórico, reputação, biblioteca, itens e redes de sociabilidade.
- **Cena.** Uma pessoa na porta de um apartamento, de mala na mão, pronta para se mudar. Tudo o que ela juntou ficou dentro, preso ao chão, os livros, as fotos com amigos, os troféus e a mesa onde recebia gente. Pela janela, o vizinho acena.
- **Azul.** As coisas que ficam presas lá dentro.
- **Evitar.** Despejo, oficial de justiça, briga.
- **Alt do plano.** Uma pessoa sai de casa com uma mala pequena, e tudo o que construiu lá dentro fica preso ao chão.

**porta-decide. A plataforma decide sobre mim sem explicar.**
- **Falha atual.** Linhas tracejadas e dois pontos.
- **Âncora.** p. 381, a alteração de regra, o rebaixamento de alcance ou a suspensão que nem chegam a virar objeto verificável, e p. 780, a estrutura real da sujeição.
- **Cena.** Um guichê de vidro fosco, sem rosto do outro lado. Pela fresta sai uma folha carimbada que cai na mão de uma pessoa. Atrás dela, uma fila com um entregador de capacete, uma vendedora com uma caixa e alguém com o celular, cada um com a sua folha carimbada.
- **Azul.** As folhas carimbadas.
- **Evitar.** Letras no carimbo.
- **Alt do plano.** Um guichê de vidro fosco entrega folhas carimbadas a uma fila de pessoas, sem ninguém visível do outro lado.

**porta-comum. Provar e reclamar.**
- **Falha atual.** Um retângulo azul e um balão.
- **Âncora.** A frase do campo porta-comum em `conteudo/camada-externa.md` é acréscimo de acesso. A cena se ancora na distribuição da prova, p. 735-736, e em Como reclamar, acréscimo de 08/11/2026.
- **Cena.** Uma mesa de cozinha com prints impressos, o celular, um caderno de anotações e um envelope sendo fechado por duas mãos. Ao fundo, pela janela, um prédio público comum.
- **Azul.** O envelope.
- **Alt do plano.** Mãos fecham um envelope sobre uma mesa cheia de prints e anotações.

### 4.5 Problemas, vinte e quatro peças 16 x 9

Lugar. Logo depois do título de `problemas/<slug>/`, pela inserção em `pagina()` que hoje põe o SVG, agora com `figura("problema-<slug>")`. A cena mostra o momento em que a pessoa percebe o problema. As páginas na coluna da direita são as que a página já ancora, e a nova sessão escolhe o trecho literal da peça entre elas.

1. **conta-bloqueada. Minha conta foi bloqueada ou banida. E o que eu comprei?** (p. 375, 749, 373, 746) Uma pessoa sentada na cama de madrugada, à luz do celular. A tela mostra um cadeado grande sobre o inventário. Na parede atrás, a sombra das armaduras que ela tinha, enfileiradas, se apagando. Azul nas sombras das armaduras que ainda restam.
2. **item-alterado. O que eu comprei mudou numa atualização. E agora?** (p. 729, 730, 637, 650) Uma tela de celular dividida por uma barra de progresso de atualização. Do lado de cá, a armadura com todos os detalhes. Do lado de lá, a mesma armadura lisa. A pessoa segura o celular com as duas mãos, olhando a barra terminar. Azul nas duas armaduras.
3. **servico-piorou. O serviço piorou, e o preço continua o mesmo.** (p. 480, 479, 655, 756) Um restaurante. A mesma pessoa, a mesma mesa, o mesmo preço na conta sobre a mesa. Em dois quadros lado a lado, o prato antes era cheio e agora é quase só a louça. Azul na comida que restou. A cena da p. 745 pode servir de base se a nova sessão achar o trecho do curso que perde aulas.
4. **presente-retirado. Um item que recebi de presente foi retirado da minha conta.** (p. 610, 611, 615, 616) Duas pessoas, uma entrega um presente embrulhado à outra. Atrás, uma mão grande de fora do quadro puxa a fita do presente de volta, já desfazendo o laço. Azul na armadura que aparece pela abertura do embrulho.
5. **jogo-encerrado. O serviço vai acabar. O que acontece com o que eu comprei?** (p. 409, 709, 796) Um parque de diversões ao entardecer, com as luzes se apagando uma a uma. Um funcionário fecha o portão com corrente. Do lado de fora, uma pessoa segura a armadura nos braços, olhando o parque escurecer. Azul na armadura.
6. **so-licenca. A empresa diz que eu só tenho uma licença. Então eu não comprei nada?** (p. 401, 574, 743, 565) Uma pessoa com a armadura vestida, de pé numa vitrine. Uma mão de fora prende nela uma etiqueta de papel pendurada por um barbante, como as de aluguel. A pessoa olha a etiqueta, desconfiada. Azul na armadura. Sem texto na etiqueta.
7. **promessa. O que foi anunciado não é o que eu recebi.** (p. 744-745, 725, 724) Uma caixa de entrega aberta sobre a mesa. Na tampa, o desenho da armadura grandiosa. Dentro, uma armadura menor, mais simples. A pessoa segura a tampa numa mão e a peça na outra. Azul nas duas. Não repetir a cena de direito-d, que é rua e outdoor. Aqui é a entrega em casa.
8. **exclusivo-voltou. Paguei caro por algo exclusivo, e ele voltou mais barato.** (p. 213, 214, 209, 452-453) Uma vitrine com uma única armadura sob uma redoma, e uma pessoa que a leva com cuidado. Ao lado, a mesma vitrine, depois, cheia de cópias da mesma armadura empilhadas numa cesta de promoção. Azul nas armaduras.
9. **sorteio. Paguei por um sorteio ou por uma caixa de recompensa.** (p. 494-495, 449, 494, 495) Uma pessoa diante de uma parede de caixas fechadas, todas iguais, com uma moeda na mão. Uma caixa aberta no chão mostra pouco. Por trás da parede, em tracejado cinza, um mecanismo de engrenagens decide qual caixa contém a armadura. Azul só na armadura escondida, vista pelo tracejado.
10. **moeda. A moeda do serviço passou a comprar menos.** (p. 176, 179, 398, 397) Uma pessoa com uma pilha de moedas na mão, diante de um balcão. O balcão sobe devagar, por um macaco hidráulico em tracejado cinza, e a armadura no alto fica cada vez mais longe. Azul nas moedas e na armadura.
11. **pressa. A oferta dizia última chance.** (p. 670, 209, 670-671, 318) Uma pessoa correndo para uma porta que se fecha, com um grande relógio de parede marcando o fim. Na vitrine atrás da porta, a armadura. A porta é de enrolar e está descendo. Azul na armadura.
12. **regras-escondidas. A regra que me prejudicou estava enterrada nos termos de uso.** (p. 722, 601, 722-723) Um corte de terreno, como num livro de geologia. Na superfície, uma pessoa caminha tranquila. Em camadas de papel empilhadas como estratos, bem lá embaixo, uma única folha azul, a cláusula que pesou. Uma pá encostada na superfície. Azul na folha enterrada.
13. **prova. Os registros estão com a empresa.** (p. 659, 735, 736) Um quebra-cabeça montado sobre uma mesa, com metade das peças. A pessoa segura as peças que tem. As peças que faltam estão dentro de um cofre do outro lado da mesa, visível em tracejado. Azul nas peças do cofre. Não repetir a composição de direito-i.
14. **reclamacao-some. Reclamo, e a resposta nunca resolve.** (p. 780, 782, 781) Uma pessoa num balcão de atendimento muito acolhedor, com almofadas, flores e um atendente sorridente sem rosto definido. A pessoa entrega um papel. Atrás do atendente, o papel cai num triturador ligado a uma esteira circular que volta para a fila. Azul no papel da reclamação.
15. **sair. Quero sair, mas perderia tudo o que construí ali.** (p. 358-359, 359, 466) Uma pessoa na porta de uma casa grande, com uma mala pequena. Dentro, tudo o que ela construiu, estantes, quadros e a armadura, fica para trás, tudo pregado no chão. Azul na armadura que fica.
16. **historia-perdida. Perdi anos de histórico.** (p. 540-541, 543, 534, 537) Uma pessoa folheando um álbum de fotos. As páginas do começo estão cheias. As do meio em diante estão em branco, com marcas de onde as fotos estavam. Azul nas fotos que restam.
17. **programa-no-aparelho. O serviço exige um programa que roda no meu aparelho.** (p. 521, 522, 526) Um computador de mesa visto por dentro, com a tampa aberta. Entre as peças, um pequeno guardião de capacete instalado no fundo, com uma lanterna, vigiando tudo. A pessoa olha pela tampa aberta, surpresa. Azul no guardião. Evitar sugerir vírus ou ataque. É um vigia, não um invasor.
18. **crianca. Meu filho ou minha filha gastou num jogo.** (p. 494, 545, 544, 671) Uma sala de casa. Uma criança no tapete com o tablet, encantada, enquanto do tablet sai uma fila de moedas que sobe até a bolsa de um adulto pendurada na cadeira. O adulto, de costas, cozinhando. Azul nas moedas. Nenhuma marca no tablet.
19. **assistente. O assistente de inteligência artificial mudou ou errou.** (p. 758, 759, 487) Uma pessoa conversa com um balão de fala grande, como na gravura da família cognitiva. O balão responde com uma ponte desenhada que a pessoa começa a atravessar. A ponte acaba no meio, e lá embaixo há um rio. Azul no balão. Coerente com familia-funcionalidade-cognitiva.
20. **loja-virtual. A loja virtual esconde quem é pago e quem é confiável.** (p. 762, 761, 764) Uma prateleira de mercado. Uma mão de fora empurra alguns produtos para a frente, sob um holofote. Outros, iguais, ficam no fundo, na sombra. Uma pessoa com cesta olha só para os da frente. Azul nos produtos iluminados.
21. **rede-social. Meu alcance caiu ou fui punido numa rede social.** (p. 762, 763, 729, 764) Uma praça com uma pessoa falando de cima de um caixote, com público em volta. Atrás do público, uma parede de vidro fosco desce devagar e os ouvintes do fundo já não a veem. Azul no megafone da pessoa.
22. **trabalho-por-app. Trabalho por aplicativo, e a regra mudou.** (p. 765, 767-768, 766) Um entregador de bicicleta numa rua. A rua à frente dele é desenhada como um tabuleiro, e uma mão de fora reposiciona as casas, mudando o caminho e a distância até o destino. Coerente com familia-produtividade-gig-economy. Azul na caixa de entrega.
23. **vendo-na-plataforma. Vendo numa plataforma. A lei do consumidor me protege?** (p. 778, 779, 780, 763) Uma feira coberta. A banca de uma vendedora está bem montada, mas o corredor que leva até ela é fechado por um biombo móvel, posto por um funcionário da feira. Os fregueses passam pelo corredor principal sem vê-la. Azul nos produtos da banca.
24. **muita-gente. Aconteceu com muita gente. Dá para resolver de uma vez?** (p. 774, 776, 775) Uma praça com muitas pessoas, cada uma com o celular, e em todas as telas o mesmo cadeado. As pessoas começam a se aproximar umas das outras, formando um grupo só. Azul no cadeado das telas.

### 4.6 Páginas avulsas

- **alem-do-consumo. Quando a lei do consumidor não alcança.** (p. 434 e 780, e o Código Civil, como acréscimo de 15/11/2026) Uma vendedora de aplicativo no balcão da banca dela, na mesma feira de vendo-na-plataforma. Ao lado, apoiado na banca, um segundo livro, mais fino que o do consumidor, aberto na página que serve. Azul nos produtos da banca. Formato 16 x 9.
- **como-reclamar. Como reclamar.** (acréscimo de 08/11/2026) Quatro portas numa rua, em sequência, cada uma com um sinal visual próprio, um balcão de loja, um computador, um prédio público e um fórum sem brasão. Uma pessoa com um envelope azul caminha da primeira à quarta, e as pegadas mostram que ela entrou e saiu das três primeiras. Azul no envelope. Formato 16 x 9. O desenho não pode sugerir ordem obrigatória além da que a página diz.
- **direitos/ (índice).** Fica sem ilustração. A página é um índice, e o leitor já vê as onze peças nas páginas de cada direito.

### 4.7 Histórias do mapa, seis peças 16 x 9

Lugar. Logo depois do título de `siga/<slug>/`. A história da skin usa as peças do caminho. Cada peça mostra a cena da história em primeira pessoa do mapa.

1. **siga-comunidade. A rede derrubou a comunidade que eu criei.** (p. 135, 762, 763, 22) Um salão de festas cheio, com uma pessoa no centro que organizou tudo. Do teto, a estrutura do salão está presa por cabos a uma mão de fora, que começa a recolhê-los. As paredes já se inclinam. Azul nas bandeirinhas que a pessoa pendurou.
2. **siga-pedido. Paguei, veio errado e a loja disse que só intermedeia.** (p. 762, 761, 763, 764) Uma caixa de entrega aberta com o item errado. A pessoa olha para o balcão da loja, onde o atendente aponta para um vendedor distante, que aponta de volta. Azul no item esperado, visto na foto do pedido que a pessoa segura.
3. **siga-assistente. Confiei no assistente de IA e ele me deixou na mão.** (p. 757, 758, 760, 759) A pessoa segue um balão de fala que vai à frente como guia, numa trilha de montanha. O balão some numa curva e a pessoa fica sozinha na beira. Coerente com familia-funcionalidade-cognitiva. Azul no balão. Não repetir a ponte de problema-assistente.
4. **siga-corrida. O aplicativo cortou minhas corridas e o meu ganho.** (p. 765, 767, 766, 768) Um motorista no carro parado numa avenida vazia, à noite. No painel, o celular com um mapa sem nenhum ponto. Ao longe, outros carros recebem pontos de luz. Azul no celular.
5. **siga-loja. Minha loja sumiu da busca do aplicativo.** (p. 766, 771, 772, 769) Uma rua comercial vista de cima. A loja da pessoa está lá, aberta, mas uma mão de fora apaga a rua de acesso como quem usa uma borracha num mapa. Azul na fachada da loja.
6. **siga-reclamacao. Reclamei, fui bem atendido e nada aconteceu.** (p. 756, 781, 782, 780) A pessoa sai de uma sala de atendimento confortável, satisfeita, com um protocolo na mão. Atrás dela, pela porta entreaberta, o mesmo problema dela continua sobre a mesa, intocado. Azul no problema sobre a mesa. Não repetir problema-reclamacao-some, que mostra o triturador.

## 5. Fase 4. Integração

1. **Plano.** Cada peça nova entra em `estrutura/ilustracoes.md` com os campos do 4.2. Os trechos literais passam pelo `conferir_citacoes.py` antes do commit.
2. **Gerador.**
   - `figura("direito-<letra>")` no alto das páginas dos direitos, no lugar de `vinheta()`. A figura usa o formato 4 x 3 e a largura da coluna de texto.
   - Os cartões das portas recebem `figura("porta-<id>")` em 4 x 3, na largura inteira do cartão, com `alt` vazio e sem legenda.
   - `pagina()` põe `figura("problema-<slug>")` depois do título dos problemas e `figura("siga-<slug>")` depois do título das histórias.
   - `ILUSTRACAO_PAGINA` volta a ter `alem-do-consumo/` e `como-reclamar/`, agora com WebP.
3. **Tamanho na página.** A figura de abertura ocupa a largura da coluna de texto, nunca menos. Nenhuma peça fica isolada num vão. Conferir a 1.280, 1.000 e 390 px nos dois temas.
4. **Legendas e aviso de IA.** Seguem a decisão de 12/11/2026. Na Informação e na Doutrina, legenda sem aviso. Na Ciência, o aviso em cada legenda. Na página do autor, o aviso uma vez.
5. **Inglês.** Texto alternativo e legenda de cada peça entram na memória de tradução pelo fluxo de `ferramentas/en/`. Nenhum segmento novo pode ficar em português no site inglês. Os cartões de compartilhamento que mudarem são refeitos com `ferramentas/gerar_cartoes.py` e `--en`.
6. **Conferência e publicação.** A cada lote, rodar `gerar_site.py`, `checar_site.py`, `revisar_fontes.py` e `conferir_citacoes.py` com todos os arquivos do `CLAUDE.md`. Commit e push para `main` no mesmo passo.

## 6. Fase 5. Opcional, depois das peças prontas

O componente de peças tocáveis (`site/ilustracoes.js` e `site/ilustracoes.css`) pode voltar sobre as gravuras, com pontos de toque desenhados sobre o WebP, e não com o desenho refeito em SVG. Só com decisão do autor, depois de as gravuras estarem no ar.

## 7. Ordem de trabalho

1. **Lote 1.** Fase 1 inteira. Sem produção. Publicar no mesmo dia.
2. **Lote 2.** As seis portas da capa e as onze peças dos direitos. A capa é a primeira tela do site, e o direito b foi a página que o autor apontou. Encomendas escritas pelo Claude, imagens geradas pelo autor, conferência e publicação.
3. **Lote 3.** Os 24 problemas, em quatro grupos de seis, na ordem das famílias da capa.
4. **Lote 4.** As seis histórias e as duas avulsas.
5. **Lote 5.** As duas gravuras a refazer (parte-a-lei e ideia-lex-plataformae) e, se o autor quiser, a candidata parte-o-desejo.

São 49 peças novas e duas refeitas, 51 no total. As novas são onze direitos, seis portas, vinte e quatro problemas, duas avulsas e seis histórias. As refeitas são parte-a-lei e ideia-lex-plataformae. A candidata parte-o-desejo seria a 52ª.

## 8. Pontos que dependem do autor

1. Confirmar a linha única da gravura editorial e a saída do conjunto de 16/11 (seção 1.3), com a armadura suspensa da capa como única exceção.
2. Confirmar as cenas das portas da capa (4.4). A alternativa é cartão só com texto, mais sóbrio.
3. Decidir se a versão escura das peças novas sai pelo negativo calculado, como em 15/11, ou se cada peça nasce com a versão escura desenhada, como ele pediu para peças novas em 15/11/2026.
4. Decidir se parte-o-desejo entra no lote 5.
5. Gerar as imagens com o ChatGPT a partir das encomendas, como em 12/11.
