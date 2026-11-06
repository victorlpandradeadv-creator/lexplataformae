# Arquitetura das camadas

Etapa 3 da adequação das camadas, ordenada pelo autor em 05/11/2026. Sai da matriz em `estrutura/matriz/`. Toda seção da tese tem lugar nas duas camadas. A conferência roda com `python3 ferramentas/conferir_arquitetura.py`.

## Doutrina. Doutrina didática para juristas e correlatos

Um curso em capítulos, em `conteudo/curso/<nn>-<slug>.md`, publicado em `curso/<slug>/`, com índice em `curso/`. Cada capítulo ensina a pensar o problema. Situações e Legislação ficam como consulta, e Parâmetros, Diretrizes, Limites e fichas de Conceitos continuam nos mesmos endereços, apontando para o capítulo. As famílias e os desdobramentos do capítulo 7 da tese continuam em `laboratorio/<slug>/`, com a prosa da Doutrina aprofundada em `conteudo/doutrina.md`, e o índice do curso os traz como parte de aplicações.

Sequência de cada capítulo. O problema. Por que a leitura comum não basta. A construção, com o encadeamento. Requisitos ou critérios. Caso trabalhado. Objeções do fornecedor ou da doutrina e a resposta. Limites. Fundamento legal e autores. A sequência orienta e não é molde de títulos, porque os títulos são perguntas próprias do capítulo.

| Capítulo | slug | Seções da tese |
|---|---|---|
| Como ler este curso | como-ler | 1, 2, 2.1, 2.2, 2.3, 2.4, 2.4.1, 2.4.2, 2.4.3, 2.5, 2.7 |
| Por que a técnica muda a pergunta jurídica | tecnica | 3, 3.1, 3.1.1, 3.1.2, 3.1.3, 3.1.4, 3.1.5 |
| Como a plataforma extrai valor | economia | 3.2, 3.2.1, 3.2.2, 3.2.3, 3.2.5, 3.2.6 |
| O Objeto Imaterial de Consumo | objeto | 5, 5.1, 5.1.2, 5.1.2.1, 5.1.2.2, 5.1.2.3, 5.1.2.4, 5.2, 5.2.1, 5.2.2, 5.2.4, 6.2, 6.2.1, 6.2.1.1, 6.2.2, 6.2.3, 7, 7.1, 7.1.1, 7.1.1.1, 7.1.2 |
| A lei da plataforma | lei-da-plataforma | 4.2, 4.2.1, 4.2.4, 4.2.5, 7.1.4 |
| A vulnerabilidade semiótica | vulnerabilidade | 4, 4.1, 4.1.1, 4.1.5, 4.2.3, 4.2.6, 5.1.1, 6, 6.2.4, 6.2.4.1, 6.2.4.1.1, 6.2.4.2, 6.2.4.4, 6.2.4.5, 7.1.1.2 |
| Informação, publicidade e antecipação | informacao | 4.1.2, 4.1.3, 4.1.4, 6.2.5, 7.1.1.3, 7.1.1.4 |
| A auditabilidade aberta | auditabilidade | 5.1.5, 6.3, 6.3.1, 7.1.1.5 |
| A equivalência de valor funcional | equivalencia | 5.1.5, 6.3.2, 7.1.1.6 |
| A teleologia abusiva e o ilícito de arquitetura | ilicito | 5.1.3, 6.4, 6.4.1, 6.4.2, 6.4.3, 7.1.1.7, 7.1.3 |
| Os bens protegidos | bens-protegidos | 5.1.4, 6.1.3 |
| A ordem constitucional e o marco setorial | ordem-constitucional | 4.2.2, 5.2.3, 6.1, 6.1.1, 6.1.2, 6.1.2.1, 6.1.4 |
| A propriedade intelectual | propriedade-intelectual | 3.2.4, 6.5, 6.5.1, 6.5.2, 6.5.3, 7.1.1.9 |
| A prova | prova | 6.2.4.3, 6.2.4.3.1, 6.3.3, 7.1.1.8 |
| Os remédios | remedios | 7.1.1.10, 7.3, 8 |
| Aplicações, nas páginas de plataforma | laboratorio | 7.2, 7.2.1, 7.2.2, 7.2.3, 7.2.4, 7.2.5, 7.2.6, 7.2.7, 7.2.7.1 |
| Só na Ciência | epigrafes | 2.6 |

## Informação. Pedagogia difusa do mercado sobre os próprios direitos

A entrada é o que aconteceu com a pessoa. Cada página responde ao que ela vive, diz se é o caso dela, o que guardar, o que pedir, a quem recorrer e onde a proteção para.

- **Problemas**, `problemas/<slug>/`, o centro da camada, em `conteudo/problemas.md`, com texto próprio.
- **Seus direitos**, `direitos/`, o que a plataforma deve, em linguagem comum.
- **Como reclamar**, `como-reclamar/`, o caminho até Procon, consumidor.gov.br, Juizado e advogado, com os prazos. Acréscimo datado, por ordem do autor, com fonte oficial.
- **Percurso**, `percurso/<parte>/`, a leitura contínua a partir da skin, com a tese inteira recortada. Os termos de outros campos perdem o título e viram explicação do fenômeno, e o nome teórico fica na Ciência.
- **Vocabulário**, os nove conceitos, depois do fenômeno que cada um nomeia, em `conceitos/<id>/`.
- **Outros serviços**, `laboratorio/<slug>/`, as famílias na voz do consumidor.

Problemas previstos, cada um com base na matriz.

| slug | Pergunta da pessoa | Seções principais |
|---|---|---|
| conta-bloqueada | Minha conta foi bloqueada ou banida. E o que eu comprei? | 4.2.4, 6.2.4.3, 7.1.2 g |
| item-alterado | O que eu comprei mudou numa atualização. E agora? | 5.1.5, 6.3.2, 7.1.1.6 |
| servico-piorou | O serviço piorou, e o preço continua o mesmo. Posso reclamar? | 5.1.5, 6.3.2, 7.2 |
| presente-retirado | Um item que recebi de presente foi retirado da minha conta. E agora? | 6.2.4.3.1 |
| jogo-encerrado | O serviço vai acabar. O que acontece com o que eu comprei? | 6.5.3, 8 |
| so-licenca | A empresa diz que eu só tenho uma licença. Então eu não comprei nada? | 5.1.2, 6.2.2, 6.2.3 |
| promessa | O que foi anunciado não é o que eu recebi. E agora? | 6.2.5, 7.1.1.4 |
| exclusivo-voltou | Paguei caro por algo exclusivo, e ele voltou mais barato. Isso pode? | 3.2.3 |
| sorteio | Paguei por um sorteio ou por uma caixa de recompensa. O que preciso saber? | 4.1.3, 5.2.3, 6.1.4, 5.1.3 |
| moeda | A moeda do serviço passou a comprar menos. Isso é permitido? | 3.2.1, 3.2.3 |
| pressa | A oferta dizia última chance. Fui pressionado a comprar? | 4.1.4, 6.2.5, 6.4.2 |
| regras-escondidas | A regra que me prejudicou estava enterrada nos termos de uso. E agora? | 6.2.4.2, 7.1.1.3 |
| prova | Os registros estão com a empresa. Como eu provo o que aconteceu? | 6.3.3, 7.1.1.8 |
| reclamacao-some | Reclamo, e a resposta nunca resolve. O que fazer? | 7.2.7 |
| sair | Quero sair, mas perderia tudo o que construí ali. Isso conta? | 4.2.3, 5.1.4, 6.1.3 |
| historia-perdida | Perdi anos de histórico. Isso é mais do que um item? | 5.1.4, 6.1.3 |
| programa-no-aparelho | O serviço exige um programa que roda no meu aparelho. Posso questionar? | 6.1.2.1 |
| crianca | Meu filho ou minha filha gastou num jogo. O que a lei diz? | 5.2.3, 6.1.4 |
| assistente | O assistente de inteligência artificial mudou ou errou. O que posso exigir? | 7.2.1 |
| loja-virtual | A loja virtual esconde quem é pago e quem é confiável. Isso conta? | 7.2.2, 7.2.4 |
| rede-social | Meu alcance caiu ou fui punido numa rede social. Tenho o que pedir? | 7.2.2 |
| trabalho-por-app | Trabalho por aplicativo, e a regra mudou. Tenho o que pedir? | 7.2.3, 7.2.6 |
| vendo-na-plataforma | Vendo numa plataforma. A lei do consumidor me protege? | 7.2.6 |
| muita-gente | Aconteceu com muita gente. Dá para resolver de uma vez? | 7.2.5 |

Partes do percurso, todas com a matriz inteira como fonte, pelo caminho da skin.

| Parte | Seções |
|---|---|
| a-compra | 1, 5.1.2, 5.2.2, 6.2.1, 6.2.2, 6.2.3 |
| o-desejo | 3.2.6, 4.1, 4.1.1, 4.1.2, 4.1.3, 4.1.4 |
| o-dono | 3.2, 3.2.1, 3.2.2, 3.2.3, 3.2.4, 3.2.5 |
| as-regras | 4.2, 4.2.1, 4.2.2, 4.2.3, 4.2.4, 4.2.5, 5.1.4, 6.1.2 |
| o-normal | 3, 3.1, 3.1.1, 3.1.2, 3.1.3, 3.1.4, 3.1.5, 4, 4.1.5, 4.2.6, 5.1.1, 6.2.4 |
| a-mudanca | 5.1.5, 6.3, 6.3.1, 6.3.2, 7.1.1.5, 7.1.1.6 |
| o-desenho | 5.1.3, 6.1.3, 6.4, 6.4.1, 6.4.2, 6.4.3 |
| a-lei | 5, 5.1, 5.2.3, 6, 6.1, 6.1.1, 6.1.4, 6.2, 6.5, 6.5.1, 6.5.2, 6.5.3, 7.1.1.9 |
| a-resposta | 6.2.4.3.1, 6.3.3, 7, 7.1, 7.1.1, 7.1.2, 7.1.3, 7.1.1.8, 7.1.1.10, 7.3 |
| alem-do-jogo | 5.2, 5.2.1, 5.2.4, 7.2, 7.2.1, 7.2.2, 7.2.3, 7.2.4, 7.2.5, 7.2.6, 7.2.7, 7.2.7.1 |
| o-nome | 2, 2.1, 2.2, 2.3, 2.4, 2.5, 2.7, 7.1.4, 8 |
