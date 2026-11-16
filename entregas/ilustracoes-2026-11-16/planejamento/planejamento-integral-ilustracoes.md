# Planejamento integral de ilustrações — Lex Plataformae
Revisão conceitual de 15/11/2026. Proposta para produção, ainda sem validação com leitores.

## 1. Decisão editorial
Este documento substitui as instruções visuais anteriores para a nova produção. Os 73 assuntos e identificadores são preservados; suas soluções visuais são revistas. Nenhuma imagem dos lotes anteriores será remendada. O acervo de 29 peças também será recomposto em claro e escuro, em vez de receber apenas uma versão escura.

Objetivo: ajudar a reconhecer situações e compreender relações, preservando a estrutura de Informação, Doutrina e Ciência. Transparência é requisito de aplicação; a direção artística é construída em torno de relações visuais simples.

## 2. Aplicação no site
| Contexto | Função da imagem | Aplicação |
|---|---|---|
| Informação | Reconhecer a situação e escolher um caminho | Vinheta junto ao título; cena explicativa depois da apresentação do problema |
| Doutrina | Apoiar a qualificação e a operação | Preservar os esquemas existentes. Ilustração só quando acrescenta uma relação; não repetir automaticamente os cartões de Informação |
| Ciência | Permitir examinar a construção do argumento | Preservar fontes e citações. Distinguir metáfora ilustrativa de esquema explicativo ou evidência |
| Celular | Manter leitura e prioridade do texto | Sem imagem grande antes de toda chamada de ação; testar o cartão completo em 320, 360 e 390 pixels |
| Compartilhamento | Identificar uma página fora do site | Derivado separado, com fundo opaco deliberado; nunca usar esse derivado dentro da página |

As posições finais devem ser confirmadas no componente que consome cada arquivo. Os identificadores não autorizam inventar URLs ou inserir imagens em todos os modos. A página inicial já muda blocos ao mudar de modo: isso deve ser respeitado.

## 3. Sistema visual
Contorno editorial preciso, terminações arredondadas, perspectiva mínima. Espaço externo sempre transparente. Uma relação principal por peça; no máximo dois elementos secundários nas cenas grandes. Pessoas calmas, diversas, sem rosto identificável. Nenhuma pessoa real, personagem de jogo, marca, interface real, letra, número ou logotipo.

Não usar decoração jurídica genérica para representar qualquer direito. Balança, martelo, cadeado e corrente só seriam admissíveis se fossem o assunto literal; os novos conceitos dispensam esses atalhos. Não representar perda de função como destruição física. Não sugerir que toda mudança da plataforma é abusiva.

O azul identifica a posição, utilidade, registro ou objeto relevante para o leitor. Controles da plataforma permanecem neutros. A compreensão também deve sobreviver em escala de cinza: forma, posição e continuidade carregam o significado.

Vazios entre objetos, dentro de caminhos e dentro de formas declaradamente vazadas deixam a página aparecer. Preenchimentos de objetos são delimitados pela própria forma, nunca por um retângulo que simule o fundo da aba. Evitar papel creme pintado por conveniência. Se uma sobreposição exigir preenchimento, usar apenas uma pequena superfície de apoio.

Tracejado significa estrutura não visível, condição anterior ou vínculo técnico, conforme a peça. Não misturar dois desses sentidos numa mesma composição sem explicação externa. Setas indicam movimento ou relação, nunca substituem a demonstração visual.

## 4. Cor e temas
Os fundos do site não serão alterados. Referência observada em site/cores.css:
| Modo | Página clara | Página escura |
|---|---|---|
| Informação | #faf6ef | #17130f |
| Doutrina | #f0f5f9 | #131a23 |
| Ciência | #f7fbfc | #121416 |

Também testar sobre as superfícies dos cartões e folhas, que diferem do fundo da página.

| Papel visual | Claro | Escuro |
|---|---|---|
| Contorno principal | #211c17 | #ebe7e1 |
| Traço secundário | #615953 | #a9a49c |
| Objeto do leitor | #002fa7 | #497ef7 |
| Destaque excepcional | #3a63d0 | #a1bdf9 |
| Apoio pequeno, se indispensável | #f1ebe1 | #241f1a |
| Espaço externo | Transparente | Transparente |

Uma geometria comum recebe as duas paletas. Não regenerar a composição para produzir o tema escuro. O desenho não deve depender de branco como luz, de sombras projetadas ou de brilho. Nenhuma massa contínua deve ocupar mais de 20% da área total.

## 5. Formatos
- Vinhetas: 480 × 480; estudar primeiro em 56 × 56. Conteúdo dentro de círculo imaginário de 400 pixels, margem mínima de 40. Espessura inicial de 10–14 pixels no arquivo de 480, ajustada pela prova pequena; detalhes secundários não podem desaparecer.
- Aberturas: 1600 × 900; relação principal dentro da faixa central de 1200 × 630. Não cortar partes essenciais para caber no celular.
- Internas: 1200 × 900. Se a explicação não sobreviver à redução, simplificar a cena ou usar um esquema textual no site.
- Entrega compatível: WebP com alpha, qualidade 85 nas vinhetas e 82 nas demais. Manter mestre sem perdas e desenho editável quando houver.
- Nomes: id.webp e id-escuro.webp. Produzir em pasta de revisão, sem sobrescrever o site antes de aprovação.
- Vinhetas geométricas: preferir mestre SVG desenhado para essa função, com cores controladas; exportar os WebP exigidos. SVG inserido como imagem externa não herda automaticamente as cores do texto da página.
- Cenas editoriais: geração raster com transparência nativa ou desenho editorial próprio; não fabricar transparência apagando o papel de uma cena pronta.
- Cada imagem deve sair em arquivo próprio. Pranchas são instrumentos de revisão, não arquivos-mestres para recorte final.

## 6. Armadura e continuidade
A folha canônica estrutura/referencias-visuais/armadura.webp permanece a referência de identidade. Recomeçar as composições não autoriza inventar outra armadura. Preparar uma referência de produção sobre transparência, em ambas as paletas, conservando suas partes, proporções e silhueta. Conferir contra a folha original antes de qualquer cena com armadura.

Não usar armadura em todos os serviços digitais. Nas peças transversais, empregar um módulo azul simples. O módulo não é um logotipo, moeda, botão ou símbolo de empresa.

## 7. Fichas de produção
As fichas abaixo, combinadas com as regras anteriores, definem a nova composição. “Verificação” é uma condição de aceite específica. A formulação textual da página continua sendo a autoridade conceitual; a imagem não acrescenta uma conclusão jurídica.


## Família 1 — portas

### porta-acesso
- **Função:** Navegação e reconhecimento junto ao título.
- **Composição nova:** Limiar interrompe o caminho até um objeto azul intacto. Uma barra transversal, um objeto; sem fechadura ornamental.
- **Entrega:** 480 × 480; `porta-acesso.webp` e `porta-acesso-escuro.webp`, ambos transparentes.
- **Verificação:** o título e a silhueta permitem distinguir esta entrada das outras a 56 pixels; se o detalhe desaparecer, simplificar antes de aumentar a imagem.

### porta-mudou
- **Função:** Navegação e reconhecimento junto ao título.
- **Composição nova:** Dois módulos azuis idênticos: um encaixa no suporte; no outro, o suporte deslocou o encaixe. A mudança está na condição de uso.
- **Entrega:** 480 × 480; `porta-mudou.webp` e `porta-mudou-escuro.webp`, ambos transparentes.
- **Verificação:** o título e a silhueta permitem distinguir esta entrada das outras a 56 pixels; se o detalhe desaparecer, simplificar antes de aumentar a imagem.

### porta-empurrado
- **Função:** Navegação e reconhecimento junto ao título.
- **Composição nova:** Duas linhas comprimem um percurso até uma ficha circular. Sem relógios, moedas com cifras ou perspectiva.
- **Entrega:** 480 × 480; `porta-empurrado.webp` e `porta-empurrado-escuro.webp`, ambos transparentes.
- **Verificação:** o título e a silhueta permitem distinguir esta entrada das outras a 56 pixels; se o detalhe desaparecer, simplificar antes de aumentar a imagem.

### porta-sair
- **Função:** Navegação e reconhecimento junto ao título.
- **Composição nova:** Um pequeno acervo azul cruza uma saída; um vínculo curto ainda o liga à origem visível. Sem mala nem fios saindo do quadro.
- **Entrega:** 480 × 480; `porta-sair.webp` e `porta-sair-escuro.webp`, ambos transparentes.
- **Verificação:** o título e a silhueta permitem distinguir esta entrada das outras a 56 pixels; se o detalhe desaparecer, simplificar antes de aumentar a imagem.

### porta-decide
- **Função:** Navegação e reconhecimento junto ao título.
- **Composição nova:** Uma entrada azul e duas saídas desiguais ligadas a um seletor cujo trecho central não se revela. Sem balança judicial. Se não for compreendido junto ao título, redesenhar.
- **Entrega:** 480 × 480; `porta-decide.webp` e `porta-decide-escuro.webp`, ambos transparentes.
- **Verificação:** o título e a silhueta permitem distinguir esta entrada das outras a 56 pixels; se o detalhe desaparecer, simplificar antes de aumentar a imagem.

### porta-comum
- **Função:** Navegação e reconhecimento junto ao título.
- **Composição nova:** Um registro azul permanece guardado enquanto um segundo traço o conecta a um pedido de resposta. Uma folha e um balão vazio, sem interface.
- **Entrega:** 480 × 480; `porta-comum.webp` e `porta-comum-escuro.webp`, ambos transparentes.
- **Verificação:** o título e a silhueta permitem distinguir esta entrada das outras a 56 pixels; se o detalhe desaparecer, simplificar antes de aumentar a imagem.

## Família 2 — direitos

### direito-a
- **Função:** Navegação e reconhecimento junto ao título.
- **Composição nova:** Um volume azul delimitado apenas por arestas, reconhecível sem superfície material. Sem sombra como prova de existência.
- **Entrega:** 480 × 480; `direito-a.webp` e `direito-a-escuro.webp`, ambos transparentes.
- **Verificação:** o título e a silhueta permitem distinguir esta entrada das outras a 56 pixels; se o detalhe desaparecer, simplificar antes de aumentar a imagem.

### direito-b
- **Função:** Navegação e reconhecimento junto ao título.
- **Composição nova:** Um caminho chega a um limite com passagem interrompida em tracejado. Um ponto azul identifica a posição do leitor; eliminar o labirinto.
- **Entrega:** 480 × 480; `direito-b.webp` e `direito-b-escuro.webp`, ambos transparentes.
- **Verificação:** o título e a silhueta permitem distinguir esta entrada das outras a 56 pixels; se o detalhe desaparecer, simplificar antes de aumentar a imagem.

### direito-c
- **Função:** Navegação e reconhecimento junto ao título.
- **Composição nova:** Uma folha em contorno com três linhas curtas; a linha essencial azul aparece sem precisar abrir um rolo.
- **Entrega:** 480 × 480; `direito-c.webp` e `direito-c-escuro.webp`, ambos transparentes.
- **Verificação:** o título e a silhueta permitem distinguir esta entrada das outras a 56 pixels; se o detalhe desaparecer, simplificar antes de aumentar a imagem.

### direito-d
- **Função:** Navegação e reconhecimento junto ao título.
- **Composição nova:** Uma peça azul inteira atravessa uma abertura de entrega. Nenhum envelope ou estrela decorativa.
- **Entrega:** 480 × 480; `direito-d.webp` e `direito-d-escuro.webp`, ambos transparentes.
- **Verificação:** o título e a silhueta permitem distinguir esta entrada das outras a 56 pixels; se o detalhe desaparecer, simplificar antes de aumentar a imagem.

### direito-e
- **Função:** Navegação e reconhecimento junto ao título.
- **Composição nova:** Um percurso azul contínuo atravessa um limite aberto. Sem pegadas miúdas.
- **Entrega:** 480 × 480; `direito-e.webp` e `direito-e-escuro.webp`, ambos transparentes.
- **Verificação:** o título e a silhueta permitem distinguir esta entrada das outras a 56 pixels; se o detalhe desaparecer, simplificar antes de aumentar a imagem.

### direito-f
- **Função:** Navegação e reconhecimento junto ao título.
- **Composição nova:** Uma ligação azul recompõe a continuidade entre duas partes de um objeto simples. Não usar rachaduras ornamentais.
- **Entrega:** 480 × 480; `direito-f.webp` e `direito-f-escuro.webp`, ambos transparentes.
- **Verificação:** o título e a silhueta permitem distinguir esta entrada das outras a 56 pixels; se o detalhe desaparecer, simplificar antes de aumentar a imagem.

### direito-g
- **Função:** Navegação e reconhecimento junto ao título.
- **Composição nova:** Uma base normativa aberta em contorno sustenta um objeto azul. Sem martelo, que pode reduzir o direito à punição.
- **Entrega:** 480 × 480; `direito-g.webp` e `direito-g-escuro.webp`, ambos transparentes.
- **Verificação:** o título e a silhueta permitem distinguir esta entrada das outras a 56 pixels; se o detalhe desaparecer, simplificar antes de aumentar a imagem.

### direito-h
- **Função:** Navegação e reconhecimento junto ao título.
- **Composição nova:** Um percurso em degraus tem uma interrupção; o segmento necessário aparece em azul vazado. Apenas três degraus.
- **Entrega:** 480 × 480; `direito-h.webp` e `direito-h-escuro.webp`, ambos transparentes.
- **Verificação:** o título e a silhueta permitem distinguir esta entrada das outras a 56 pixels; se o detalhe desaparecer, simplificar antes de aumentar a imagem.

### direito-i
- **Função:** Navegação e reconhecimento junto ao título.
- **Composição nova:** Um registro azul é retirado de um conjunto de três fichas abertas. Sem móvel de arquivo.
- **Entrega:** 480 × 480; `direito-i.webp` e `direito-i-escuro.webp`, ambos transparentes.
- **Verificação:** o título e a silhueta permitem distinguir esta entrada das outras a 56 pixels; se o detalhe desaparecer, simplificar antes de aumentar a imagem.

### direito-j
- **Função:** Navegação e reconhecimento junto ao título.
- **Composição nova:** Um mecanismo de comando termina diante de um limite azul claro. Sem coroa: a ideia é limitação do poder.
- **Entrega:** 480 × 480; `direito-j.webp` e `direito-j-escuro.webp`, ambos transparentes.
- **Verificação:** o título e a silhueta permitem distinguir esta entrada das outras a 56 pixels; se o detalhe desaparecer, simplificar antes de aumentar a imagem.

### direito-k
- **Função:** Navegação e reconhecimento junto ao título.
- **Composição nova:** Duas partes complementares recompõem um módulo azul funcional. Uma única indicação de aproximação; sem estrela quebrada.
- **Entrega:** 480 × 480; `direito-k.webp` e `direito-k-escuro.webp`, ambos transparentes.
- **Verificação:** o título e a silhueta permitem distinguir esta entrada das outras a 56 pixels; se o detalhe desaparecer, simplificar antes de aumentar a imagem.

## Família 3 — recomposição integral do acervo

### inicio
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Armadura canônica apoiada em uma pequena plataforma suspensa; dois apoios chegam a pontos de controle visíveis. Sem terreno maciço ou céu.
- **Entrega:** 1600 × 900; `inicio.webp` e `inicio-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### parte-a-compra
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma peça canônica passa para as mãos do comprador, enquanto sua sustentação continua ligada ao fornecedor. Sem caixa ou fita decorativa.
- **Entrega:** 1600 × 900; `parte-a-compra.webp` e `parte-a-compra-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### imagem-catraca
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Figura de armadura permanece dentro de um circuito de uso; uma passagem regulável interrompe a continuidade. Sem jardim ou cenário.
- **Entrega:** 1200 × 900; `imagem-catraca.webp` e `imagem-catraca-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### imagem-estoque-fluxo
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Dois regimes lado a lado: unidades armazenadas e uma unidade sustentada por circulação. Mostrar a interrupção do fluxo sem destruir a peça.
- **Entrega:** 1200 × 900; `imagem-estoque-fluxo.webp` e `imagem-estoque-fluxo-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### parte-o-desejo
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Figura canônica central recebe três linhas de atenção de outras figuras; o valor relacional é a relação, não um halo.
- **Entrega:** 1600 × 900; `parte-o-desejo.webp` e `parte-o-desejo-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### parte-o-dono
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Pessoas sustentam com suas contribuições uma estrutura de controle elevada. Sem castelo, nuvens ou tijolos literais.
- **Entrega:** 1600 × 900; `parte-o-dono.webp` e `parte-o-dono-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### imagem-torneira
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Pequenas parcelas azuis sucessivas acumulam-se num recipiente em contorno. Uma entrada, uma acumulação; sem três símbolos por gota.
- **Entrega:** 1200 × 900; `imagem-torneira.webp` e `imagem-torneira-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### parte-as-regras
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Folhas abertas tornam-se limites de um percurso. Uma passagem regulada encerra o caminho; sem labirinto panorâmico.
- **Entrega:** 1600 × 900; `parte-as-regras.webp` e `parte-as-regras-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### parte-o-normal
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Um suporte técnico sustenta aquilo que parecia uma condição espontânea. Mostrar a junção entre aparência e construção, sem chuva ou teatro completo.
- **Entrega:** 1600 × 900; `parte-o-normal.webp` e `parte-o-normal-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### parte-a-mudanca
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Mesma armadura, mesmo contorno, duas condições de sustentação: conexões ativas e conexões interrompidas. Não representar dano físico.
- **Entrega:** 1600 × 900; `parte-a-mudanca.webp` e `parte-a-mudanca-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### parte-o-desenho
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Dois caminhos inicialmente distintos convergem para a mesma operação. Uma saída lateral permanece acessível só por trajeto mais difícil.
- **Entrega:** 1600 × 900; `parte-o-desenho.webp` e `parte-o-desenho-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### parte-a-lei
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Estrutura contemporânea conecta-se a uma fundação anterior por junções contínuas. Fundação e obra em contorno, sem massa de solo.
- **Entrega:** 1600 × 900; `parte-a-lei.webp` e `parte-a-lei-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### parte-a-resposta
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma mão recoloca um módulo azul no circuito de uso; uma compensação secundária fica ao lado, pequena. Recomposição é o foco.
- **Entrega:** 1600 × 900; `parte-a-resposta.webp` e `parte-a-resposta-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### parte-alem-do-jogo
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Três atividades distintas apoiam-se na mesma estrutura de controle. Reduzir cinco símbolos a três; sem rostos de interface.
- **Entrega:** 1600 × 900; `parte-alem-do-jogo.webp` e `parte-alem-do-jogo-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### parte-o-nome
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Encontro alegórico de Ísis e Rá em perfis simplificados com um vínculo que representa o nome. Sem imitar obra, escrita ou decoração egípcia. Exige legenda externa.
- **Entrega:** 1600 × 900; `parte-o-nome.webp` e `parte-o-nome-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### ideia-oic
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma posição azul começa a ser sustentada por uma estrutura aberta delimitada. Mesma base formal da peça parte-a-lei; não exigir cenário de terreno.
- **Entrega:** 1600 × 900; `ideia-oic.webp` e `ideia-oic-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### ideia-feixe-de-fruicao-governada
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma posição de uso azul depende de três vínculos controlados separadamente. Poucos fios, com começo e fim visíveis.
- **Entrega:** 1600 × 900; `ideia-feixe-de-fruicao-governada.webp` e `ideia-feixe-de-fruicao-governada-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### ideia-lex-plataformae
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma regra em folha aberta conecta-se diretamente a uma engrenagem executora. Regra e execução como duas partes do mesmo mecanismo.
- **Entrega:** 1600 × 900; `ideia-lex-plataformae.webp` e `ideia-lex-plataformae-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### ideia-vulnerabilidade-semiotica
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Um mesmo sinal azul chega ao leitor; a chave de interpretação está do outro lado de um limite. Sem duplicar etiquetas ilegíveis.
- **Entrega:** 1600 × 900; `ideia-vulnerabilidade-semiotica.webp` e `ideia-vulnerabilidade-semiotica-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### ideia-teleologia-abusiva
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Dois percursos comparáveis: o que leva à compra permanece contínuo, o que permite sair tem obstáculos repetidos. Sem régua numérica.
- **Entrega:** 1600 × 900; `ideia-teleologia-abusiva.webp` e `ideia-teleologia-abusiva-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### ideia-ilicito-de-arquitetura
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma sequência de passagens permite avançar e dificulta retornar. Uma única estrutura em corte, sem coleção de portas trancadas.
- **Entrega:** 1600 × 900; `ideia-ilicito-de-arquitetura.webp` e `ideia-ilicito-de-arquitetura-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### ideia-antecipacao-hipercuratorial
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma oferta azul é revelada parcialmente por uma abertura controlada; a espera depende do mesmo comando. Sem sala com muitas pessoas.
- **Entrega:** 1600 × 900; `ideia-antecipacao-hipercuratorial.webp` e `ideia-antecipacao-hipercuratorial-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### ideia-auditabilidade-aberta
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma abertura de inspeção revela a conexão relevante num mecanismo; um registro acompanha a observação. Não abrir a máquina inteira.
- **Entrega:** 1600 × 900; `ideia-auditabilidade-aberta.webp` e `ideia-auditabilidade-aberta-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### ideia-equivalencia-de-valor-funcional
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Dois objetos canônicos iguais por fora entregam extensões de uso distintas. Uma mesma base de comparação, sem balança como atalho universal.
- **Entrega:** 1600 × 900; `ideia-equivalencia-de-valor-funcional.webp` e `ideia-equivalencia-de-valor-funcional-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### laboratorio
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Três serviços distintos revelam a mesma conexão de controle sob um recorte de inspeção. Sem telas reais.
- **Entrega:** 1600 × 900; `laboratorio.webp` e `laboratorio-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### familia-funcionalidade-cognitiva
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma troca de mensagens em contorno tem sua capacidade azul regulada por um comando externo. Não personificar o assistente.
- **Entrega:** 1200 × 900; `familia-funcionalidade-cognitiva.webp` e `familia-funcionalidade-cognitiva-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### familia-infraestrutura-e-intermediacao
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Três ofertas passam por um filtro que altera sua visibilidade. Destacar o que chega ao usuário; sem pilha de lentes.
- **Entrega:** 1200 × 900; `familia-infraestrutura-e-intermediacao.webp` e `familia-infraestrutura-e-intermediacao-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### familia-produtividade-gig-economy
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Um trabalhador percorre uma rota azul cuja inclinação ou desvio depende de um comando externo. Sem mapa urbano completo.
- **Entrega:** 1200 × 900; `familia-produtividade-gig-economy.webp` e `familia-produtividade-gig-economy-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### familia-administracao-de-confianca
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma superfície de apoio realmente amortece o contato, mas desloca um limite de escolha. Mostrar benefício e expansão sem rosto sorridente.
- **Entrega:** 1200 × 900; `familia-administracao-de-confianca.webp` e `familia-administracao-de-confianca-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

## Família 4 — entradas

### direitos-continua
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Objeto azul passa ao usuário; um vínculo de prestação continua ativo depois da entrega. Sem fachada de loja ou cena noturna.
- **Entrega:** 1600 × 900; `direitos-continua.webp` e `direitos-continua-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### alem-do-consumo
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma atividade de venda se apoia numa estrutura governada por terceiro. Três elementos: banca aberta, vendedor, sustentação externa.
- **Entrega:** 1600 × 900; `alem-do-consumo.webp` e `alem-do-consumo-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### como-reclamar
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma pessoa dispõe de quatro caminhos de encaminhamento, sem hierarquia de eficácia inventada. Nós vazios, diferenciados por posição; nomes ficam no texto da página.
- **Entrega:** 1600 × 900; `como-reclamar.webp` e `como-reclamar-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

## Família 5 — problemas

### problema-conta-bloqueada
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma posição azul permanece identificável, mas sua conexão com o ambiente é interrompida. Uma pessoa, um limite, um objeto; sem multidão.
- **Entrega:** 1600 × 900; `problema-conta-bloqueada.webp` e `problema-conta-bloqueada-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-so-licenca
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Objeto azul nas mãos do usuário continua ligado a uma estrutura que regula seu uso. Ligação técnica fina, sem corrente.
- **Entrega:** 1600 × 900; `problema-so-licenca.webp` e `problema-so-licenca-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-jogo-encerrado
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma estrutura de serviço deixa de sustentar três posições azuis que permanecem com as pessoas. Sem prédio noturno ou apagamento dramático.
- **Entrega:** 1600 × 900; `problema-jogo-encerrado.webp` e `problema-jogo-encerrado-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-sair
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Pessoa atravessa um limite; seu acervo continua ligado à origem. Expandir a relação da vinheta, sem acrescentar quatro fios.
- **Entrega:** 1600 × 900; `problema-sair.webp` e `problema-sair-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-item-alterado
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Mesma peça canônica em duas condições: um encaixe externo foi modificado. Mostrar intervenção no sistema, sem armadura quebrada.
- **Entrega:** 1600 × 900; `problema-item-alterado.webp` e `problema-item-alterado-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-servico-piorou
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma contribuição permanece igual enquanto a extensão de serviço entregue diminui. Duas faixas comparáveis, sem dinheiro ou balança.
- **Entrega:** 1600 × 900; `problema-servico-piorou.webp` e `problema-servico-piorou-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-presente-retirado
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Presente azul já entregue depende de uma ligação anterior que se interrompe longe do destinatário. Mostrar distância causal, sem suspeita de crime.
- **Entrega:** 1600 × 900; `problema-presente-retirado.webp` e `problema-presente-retirado-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-promessa
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Contorno da função prometida é maior que a função entregue, com o mesmo objeto de referência. Sem anúncio fictício ou raios.
- **Entrega:** 1600 × 900; `problema-promessa.webp` e `problema-promessa-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-exclusivo-voltou
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Um objeto apresentado isoladamente reaparece em série. A comparação deve comunicar repetição, não preço baixo.
- **Entrega:** 1600 × 900; `problema-exclusivo-voltou.webp` e `problema-exclusivo-voltou-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-sorteio
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma escolha opaca contém muitas posições vazias e poucas azuis num recorte lateral. Não sugerir probabilidades numéricas reais.
- **Entrega:** 1600 × 900; `problema-sorteio.webp` e `problema-sorteio-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-moeda
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma ficha azul passa por uma relação de conversão que alguém pode reajustar. Dois lados, um comando; sem cifras.
- **Entrega:** 1600 × 900; `problema-moeda.webp` e `problema-moeda-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-pressa
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma janela de escolha se estreita enquanto o objeto permanece disponível. Pressão temporal por redução de espaço, sem calendário voador.
- **Entrega:** 1600 × 900; `problema-pressa.webp` e `problema-pressa-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-regras-escondidas
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma condição decisiva azul está escondida entre poucas camadas sobrepostas. Três camadas bastam, sem montanha de papéis.
- **Entrega:** 1600 × 900; `problema-regras-escondidas.webp` e `problema-regras-escondidas-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-prova
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Leitor possui um registro; os demais registros ficam atrás de um limite de acesso. Mostrar distribuição desigual, sem cenário cartorial.
- **Entrega:** 1600 × 900; `problema-prova.webp` e `problema-prova-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-reclamacao-some
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Um pedido percorre um circuito e retorna sem alcançar o ponto de resposta. Não confundir resposta negativa com desaparecimento.
- **Entrega:** 1600 × 900; `problema-reclamacao-some.webp` e `problema-reclamacao-some-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-historia-perdida
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma sequência de registros azuis perde sua continuidade após a retirada de um suporte. Sem mão apagando lembranças como violência.
- **Entrega:** 1600 × 900; `problema-historia-perdida.webp` e `problema-historia-perdida-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-programa-no-aparelho
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Um componente de controle externo se instala dentro do perímetro do aparelho. Corte técnico simples; sem pequeno guarda ou lanterna.
- **Entrega:** 1600 × 900; `problema-programa-no-aparelho.webp` e `problema-programa-no-aparelho-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-crianca
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Criança diante de um mecanismo de decisão dimensionado para adulto, com adulto próximo. Não usar botão azul como convite atraente.
- **Entrega:** 1600 × 900; `problema-crianca.webp` e `problema-crianca-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-assistente
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma orientação azul aponta para um percurso que não se completa. Separar recomendação de garantia, sem robô ou ponte perigosa.
- **Entrega:** 1600 × 900; `problema-assistente.webp` e `problema-assistente-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-loja-virtual
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Um filtro de visibilidade destaca uma oferta e deixa outras acessíveis mas secundárias. Sem cones de luz ou supermercado.
- **Entrega:** 1600 × 900; `problema-loja-virtual.webp` e `problema-loja-virtual-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-rede-social
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma emissão azul passa por um regulador de distribuição e chega a menos pontos. Sem palco, caixas de som ou punição teatral.
- **Entrega:** 1600 × 900; `problema-rede-social.webp` e `problema-rede-social-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-trabalho-por-app
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Trabalhador mantém o movimento enquanto um comando altera as condições do percurso. Sem mão gigantesca ou esteira azul decorativa.
- **Entrega:** 1600 × 900; `problema-trabalho-por-app.webp` e `problema-trabalho-por-app-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-vendo-na-plataforma
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Uma atividade de venda depende de um apoio cujo ajuste está fora do alcance do vendedor. Sem lona caindo sobre pessoa.
- **Entrega:** 1600 × 900; `problema-vendo-na-plataforma.webp` e `problema-vendo-na-plataforma-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

### problema-muita-gente
- **Função:** Explicação conceitual junto à apresentação do assunto.
- **Composição nova:** Seis posições distintas apresentam a mesma alteração azul e convergem para uma causa comum. Sem multidão de quarenta figuras.
- **Entrega:** 1600 × 900; `problema-muita-gente.webp` e `problema-muita-gente-escuro.webp`, ambos transparentes.
- **Verificação:** a relação descrita permanece legível numa largura de 320 pixels, sem depender de fundo pintado, legenda dentro da imagem ou detalhes de cenário.

## 8. Acessibilidade editorial
Vinheta que apenas reforça um título adjacente recebe alternativa vazia e não repete o nome do link. Ilustração que acrescenta uma relação recebe descrição alternativa curta dessa relação, escrita após o desenho aprovado. Não descrever cor como única informação. A legenda externa pode explicar a metáfora, mas não deve esconder uma composição incompreensível.

Em Ciência, identificar a peça como ilustração conceitual e informar o uso de IA quando aplicável. Não apresentar imagens como documentação de fatos. Os textos alternativos e legendas serão traduzidos para a versão inglesa; a arte será compartilhada, sem texto embutido.

Para os onze direitos, validar cada proposta contra o título e a explicação do direito correspondente antes de desenhar: os identificadores a–k não são significados jurídicos por si mesmos. Caso a metáfora herdada do inventário não corresponda ao texto, prevalece o texto e a ficha deve ser ajustada antes da produção.

## 9. Produção e aprovação
1. Confirmar a localização de cada peça no site e registrar página, componente, modos em que aparece e tamanho efetivo.
2. Fazer estudos da Família 1 no cartão real, com título e descrição. Comparar as seis juntas antes de finalizar.
3. Produzir a versão clara e aplicar a paleta escura à mesma geometria.
4. Conferir transparência compondo a arte sobre as superfícies reais dos três modos, nos dois temas. A prévia isolada do gerador não basta: pixels transparentes podem ter cores RGB invisíveis.
5. Mostrar a família completa lado a lado, com provas em contexto e a 56 pixels nas vinhetas. Esperar aprovação.
6. Repetir para Família 2; depois preparar a referência canônica de armadura e executar Família 3, Família 4 e Família 5.
7. Não avançar de família sem aprovação. Uma falha de leitura exige redesenho antes da apresentação, não correção cosmética do fundo.
8. Após aprovação dos arquivos, integrar em revisão isolada. Verificar os três modos, ambos os temas e o celular antes de publicar.

Dentro da Família 3, trabalhar em grupos coerentes: caminho narrativo; imagens internas; conceitos; laboratório e plataformas. Apresentar a família completa para aprovação final. Não confundir aprovação de um estudo com aprovação do acervo todo.

## 10. Conferência objetiva
- Inventário: 6 portas + 11 direitos + 29 peças do acervo + 3 entradas + 24 problemas = 73 composições.
- Entrega principal: 146 WebP, além da referência canônica de produção em duas paletas. Mestres, provas e eventuais cartões sociais são derivados adicionais, não novas composições.
- Dimensões, nomes, alpha e ausência de fundo retangular verificados por arquivo.
- Mesma geometria entre paletas, sem mudança de pose, proporção ou enquadramento.
- Sem texto, marca, número, interface real ou sinais que pareçam escrita.
- Azul restrito ao elemento semanticamente relevante.
- Nenhum detalhe essencial desaparece no tamanho de uso.
- Nenhuma ilustração exige mudar a cor da aba, do cartão ou da página.
- Prova em escala de cinza para distinguir formas e estados.
- Revisão com leitores: mostrar o cartão sem explicar a metáfora e perguntar o que esperam encontrar ao clicar. Registrar confusões; não declarar inteligibilidade comprovada apenas pela opinião de quem desenhou.
- Nas cenas, perguntar qual relação entre os elementos foi percebida. Se a resposta inverter controle e usuário, a composição falhou.

## 11. Integração e estado
Este planejamento não altera o site nem publica arquivos. As imagens antigas continuam no repositório até uma substituição aprovada. Os lotes produzidos nesta conversa não são aprovados para a nova direção.

A integração deve preservar dimensões reservadas para evitar deslocamento de conteúdo, trocar apenas a paleta com o tema e manter o mesmo desenho ao alternar modos quando a peça for compartilhada. Não aplicar inversão ou filtro genérico sobre a arte. Cartões sociais têm produção separada, com fundo deliberado.

## 12. Fontes de projeto
- [Instruções anteriores e inventário](https://github.com/victorlpandradeadv-creator/lexplataformae/blob/main/estrutura/ilustracoes-producao.md)
- [Plano consolidado anterior](https://github.com/victorlpandradeadv-creator/lexplataformae/blob/main/estrutura/ilustracoes-novas.md)
- [Cores dos modos](https://github.com/victorlpandradeadv-creator/lexplataformae/blob/main/site/cores.css)
- Observação da página inicial nos três modos nesta sessão.
- Orientação do autor nesta conversa: repensar do zero para funcionar na estrutura, sem remendar fundos.

As composições deste documento são propostas editoriais novas, não descrições de imagens existentes nem resultados já testados.

