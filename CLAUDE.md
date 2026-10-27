# Projeto lexplataformae

Site de difusão da tese de doutorado de Victor L. P. Andrade, "Do regime jurídico do Objeto Imaterial de Consumo (OIC) sob a Lex Plataformae", UNESP, Franca, 2026. Domínio lexplataformae.com.br, registrado no Registro.br.

Este arquivo é a memória do projeto. Toda sessão que trabalhar aqui deve lê-lo antes de qualquer coisa.

## Arquitetura

Desde 27/10/2026 (versão 0.5) o site se lê em três camadas, por orientação do autor.

- **Camada externa, a superfície.** Fala com o leigo. Página inicial, as nove ideias e o Laboratório com as quatro famílias, em texto simples, fenômeno antes do nome, sem nome do autor nem menção a tese. O texto vem de `conteudo/camada-externa.md`. No menu aparecem só Conceitos e Laboratório.
- **Camada interna, a arquitetura.** Fala com o jurista e com o especialista. Abre com a chave Desnudar a arquitetura, que fica fixa no pé da tela em todas as páginas. Debaixo de cada bloco simples aparecem os trechos literais que ele condensa, com a página. Aparecem também o conteúdo completo das fichas, as três leituras, as epígrafes por capítulo, a faixa de versão e os itens Método, Fundamentos, Dogmática, Roteiro e Texto integral no menu. As páginas que são só arquitetura (corpus, Roteiro, Método, Fundamentos, Dogmática, desdobramentos do Laboratório e fichas fora do Atlas) já abrem desnudas, sem os contornos tracejados, e desligar a chave leva de volta à superfície. A escolha do leitor fica guardada no navegador. Sem JavaScript a chave funciona pelo CSS.
- **Camada mais interna, o autor.** Em `docs/autor/`, alcançada pelo nome no rodapé de todas as páginas, sob a pergunta "Quem está por trás destas ideias?". Ali o leitor fica sabendo, por último, que tudo deriva da tese de doutorado. Traz a referência completa, o PDF e a trajetória do trabalho nas palavras da introdução (p. 21-22).

As partes do site, dentro dessas camadas.

1. **Corpus.** A tese dividida em seções citáveis, cada uma com endereço e página próprios. Feito em 26/10/2026, em `docs/tese/`. Toda âncora de página do Atlas leva ao trecho exato, no corpo ou na nota de rodapé. O índice da tese traz o plano da obra nas palavras da introdução (p. 42), com o lugar de cada capítulo no site. Cada seção mostra as páginas das camadas que a trazem.
2. **Atlas.** Uma página por conceito, com definição literal, função no regime, critério delimitador e seções de apoio. Os conceitos são os substantivos da tese.
3. **Roteiro.** Feito em 27/10/2026, em `docs/roteiro/`. Os onze blocos de enquadramento do 7.1.2 (a a k), na ordem da tese e em texto literal, cada um com as partes que a própria tese usa. Quando incide, dever de fornecimento, prova mínima exigível, qualificação jurídica e consequência institucional. O bloco k não traz consequência institucional em frase própria. Abre com o portão de entrada, os quatro campos cumulativos do OIC (p. 428-429), e com a passagem do 7.1.1 sobre a sequência decisória. Fecha com o parágrafo do 7.1.2 que diz que o quadro não mecaniza a decisão. Cada bloco liga ao enunciado do 7.1.1 e aos conceitos do Atlas, e cada ficha aponta de volta para o seu bloco. O bloco g não tem enunciado próprio no 7.1.1. Desde 27/10/2026 o Roteiro tem três partes, uma por seção do 7.1. Os blocos do 7.1.2 em `docs/roteiro/`, as dez diretrizes do 7.1.3 em `docs/roteiro/diretrizes/`, cada uma com o seu texto integral, e o 7.1.4 em `docs/roteiro/limites/`.
4. **Laboratório.** Feito em 27/10/2026, em `docs/laboratorio/`. As quatro famílias de plataforma do 7.2 que seguem a sequência declarada pela tese (7.2.1 funcionalidade cognitiva, 7.2.2 infraestrutura e intermediação, 7.2.3 produtividade sob a gig economy e 7.2.7 administração de confiança, com o 7.2.7.1 como subcaso). Cada uma em quatro passos, com os parágrafos da tese distribuídos sem corte. Mecanismo de governança. Vulnerabilidade central, promessas e perdas. Evidências, prova e pontos de cegueira. Consequência dogmática possível. A página inicial traz o teste da abertura do capítulo 7, a passagem do 7.3 sobre mecanismo, prova e recomposição e o laboratório de origem na Riot Games, com o recorte da introdução (p. 36-37). Os desdobramentos (7.2.4 concorrência, 7.2.5 tutela coletiva e 7.2.6 consumidor equiparado) têm página própria em texto integral. O subcaso 7.2.7.1 aparece inteiro na página do 7.2.7. Casos do autor, como o das loot boxes, só entram quando ele mandar. O laboratório nunca conclui que algo "é abusivo".
5. **Fundamentos.** Feito em 27/10/2026, em `docs/fundamentos/`. Os capítulos 3 e 4, organizados pela declaração que abre cada capítulo. No capítulo 3, os três conjuntos conceituais (p. 83-85). No capítulo 4, os quatro parágrafos que nomeiam autores e funções (p. 261-263). Cada conjunto traz o parágrafo literal, os autores que ele nomeia, as seções em que a tese cita cada um, pela contagem mecânica do sobrenome no texto e nas notas, e as obras do autor na lista de referências. Abre com a passagem do capítulo 2 sobre o uso não exegético dos conceitos (p. 47). Fecha cada capítulo com a lista das suas seções.
6. **Método.** Feito em 27/10/2026, em `docs/metodo/`. O capítulo 2, que a tese apresenta como os elementos que tornam a investigação auditável (p. 47). Traz a distinção entre objeto e instrumentos (p. 46-47), cada parte do protocolo com o primeiro parágrafo da sua seção, e as três camadas de informação do 2.4.
7. **Dogmática.** Feito em 27/10/2026, em `docs/dogmatica/`. Os capítulos 5 e 6, pela abertura de cada um, parágrafo a parágrafo e em texto literal. Os parágrafos da abertura do capítulo 5 que nomeiam autores (Rizzatto Nunes, Larenz, Ferraz Jr., Ávila, Claudia Lima Marques, Wada, Reale e Unger) trazem as seções que os citam e as obras na lista de referências. Cada parágrafo traz os conceitos do Atlas que nomeia. Abre com a base normativa do 2.2 (p. 54). Fecha com o índice dos dispositivos legais citados em toda a tese, só os que trazem o nome da lei na mesma frase.
8. **Leitura por máquina.** HTML estático, glossário estruturado, marcação de termos definidos, llms.txt e robots.txt aberto a robôs de IA.

## Regras inegociáveis

- Toda frase explicativa do site se ancora em página da tese. Não há relação entre conceitos sem página que a afirme.
- Citações são literais e conferidas por script contra o texto da tese antes de qualquer envio.
- Nada vai ao ar sem a leitura e a aprovação do autor. Desde 27/10/2026, enquanto o site não tiver tráfego relevante, o autor manda publicar e revisa no ar.
- Todo conteúdo que não esteja na tese de 2026 recebe data e marca de acréscimo posterior.
- Orientações do autor na conversa não viram texto do site. Servem para reler a tese e mostrar o que ela já diz. Só entra como acréscimo posterior o que o autor mandar publicar.
- O site não pode ter nenhum padrão escuro de interface. Deve passar nos próprios critérios de auditabilidade aberta e equivalência de valor funcional.
- A identidade do projeto é acadêmica. A assinatura é de Victor L. P. Andrade, mas desde 27/10/2026 o nome aparece por último, na camada mais interna (itens 2 e 3 da lista de desenvolvimento). Escritório e empresas, se aparecerem, ficam em segundo plano.

## Estilo

- A prosa do site e as mensagens ao autor não usam ponto e vírgula, dois pontos nem travessão. Frases curtas e separadas. Citações literais da tese ficam como estão.
- A conferência das citações por script aparece uma única vez no site, no "Como ler aqui" do texto integral. Nenhuma etiqueta, faixa ou nota repete essa informação. Orientação do autor de 27/10/2026.
- Português primeiro. Versão inglesa do glossário em etapa posterior, sob a mesma assinatura acadêmica.

## Lista de desenvolvimento

1. Feito em 27/10/2026, versão 0.5. Desnudar a arquitetura como protagonista do site. Orientação do autor. O site foi pensado para tornar a tese acessível e é propaganda de ideias, da tese em si. A primeira vista mostra só as ideias, numa versão limpa da teoria, simplificada o bastante para instruir e, ao mesmo tempo, para gerar dúvida, de modo que o leitor queira apertar o botão. Fundamentação, bases, referências, páginas e qualquer indicação de estrutura que não seja a própria ideia só aparecem quando o leitor aperta o botão. Ao desnudar, o texto se expande com as referências, as notas e as informações derivadas diretamente da tese. O site não pode se perder no personagem. Precisa entender o próprio conceito.
   - Leitura para execução, a confirmar com o autor. O botão deixa o canto do cabeçalho e vira o gesto central de cada página. Método, Fundamentos, Dogmática, o corpus, as âncoras de página, as notas, as contagens e o índice de dispositivos passam para o lado desnudo. O texto da primeira vista é escrito novo e fala em nome do autor. Cada frase dele aponta, no modo desnudo, para os trechos da tese que condensa, e passa pela leitura do autor antes de ir ao ar. A primeira vista pode provocar dúvida, mas não pode prometer o que a expansão não entrega. O botão é a auditabilidade aberta do próprio site, e a passagem de uma vista à outra tem de guardar equivalência de valor funcional.

2. Feito em 27/10/2026, versão 0.5. O nome do autor não é a primeira coisa que o leitor lê. A última coisa que o leitor fica sabendo é que tudo deriva de uma tese de doutorado do autor. Orientação do autor.
   - Leitura para execução, a confirmar com o autor. Saem da primeira vista o nome, a sobrelinha "Tese de doutorado · UNESP · 2026" e a referência completa do rodapé. Na camada interna a fonte aparece pelas páginas e pelo texto integral, sem destaque para autoria nem para a natureza de tese. O nome fica por último, mas nunca escondido. Há sempre um caminho visível até ele, e nada no site se apresenta como voz neutra ou de terceiro. Nos metadados para buscadores e robôs de IA a autoria continua declarada, para que a tese seja citada com o nome certo.
3. 27/10/2026. Três camadas. Orientação do autor. A camada externa simplifica e torna a teoria acessível. A camada interna aprofunda e embasa, e é a que o botão de desnudar abre. A camada mais interna se alcança explorando o nome e o perfil do autor no site. Ela mostra a trajetória do trabalho, liga a tese a outras obras da carreira do autor e encaminha o leitor, ao final, ao LinkedIn do autor, com links também para o Lattes e o ORCID.
   - Página do autor feita em 27/10/2026. Lattes (http://lattes.cnpq.br/3172009565979544) e LinkedIn (https://www.linkedin.com/in/victorlpandrade/) informados pelo autor em 27/10/2026 e publicados. A página termina no LinkedIn, e nela a assinatura do rodapé não se repete. Pendências para executar. O ORCID, que o autor deixou para outro momento. A lista das obras a ligar, que só entra com a palavra do autor. A assinatura Galvão D'Andrade fica fora do site, por decisão do autor de 27/10/2026.

4. Feito em 27/10/2026, versão 0.5. A solenidade metodológica fica por trás do botão. Até o leigo precisa entender minimamente o texto do site principal. O desnudamento é ferramenta de estudo e aprofundamento, sobretudo para juristas e para quem é da área temática. Orientação do autor.
   - Leitura para execução, a confirmar com o autor. Cada camada tem o seu leitor. A externa fala com o leigo. A interna fala com o jurista e com o especialista. A mais interna fala com quem quer saber de quem é a ideia. Os nomes dos nove conceitos também são vocabulário técnico, e na camada externa cada um chega depois do fenômeno que nomeia, contado em palavras comuns e com exemplo tirado da própria tese. A faixa de versão e de conferência por script, as âncoras de página, as contagens e a legenda técnica do modo desnudo saem da primeira vista. A legibilidade do texto externo pode ser medida pelo índice de Flesch adaptado ao português, com meta de leitura fácil, e conferida com pelo menos um leitor leigo.

## Decisões pendentes do autor

- Manter ou retirar as três leituras da tese na página do Atlas.
- Definição canônica de cada conceito.
- Lacuna da antecipação hipercuratorial, que não tem critério negativo geral na tese.
- Leitura proposta para ilícito de arquitetura e teleologia abusiva. O primeiro como gênero, a segunda como critério da finalidade. Nos percursos aparecem lado a lado, porque a tese nunca os separa nos títulos (5.1.3, 6.4, 7.1.1.7).
- Seleção dos destaques em `estrutura/destaques.md`. Feita pelo Claude em 27/10/2026, aguarda a revisão do autor.
- Licença. Até a decisão, todos os direitos reservados. Proposta em estudo, MIT para o código e CC BY 4.0 para o conteúdo próprio, com exclusão expressa de material de terceiros.

## Decisões tomadas

- 26/10/2026. Os nove conceitos do Atlas, sem numeração. Objeto Imaterial de Consumo (OIC), Lex Plataformae, vulnerabilidade semiótica, teleologia abusiva, ilícito de arquitetura, antecipação hipercuratorial, auditabilidade aberta, equivalência de valor funcional e feixe de fruição governada.
- 26/10/2026. Orientação do autor, que não é nota para publicar. Os conceitos são independentes e funcionam integrados sob o OIC. O site mostra isso só com o texto da tese. O OIC é o eixo da página inicial, com a passagem da p. 719 sobre os parâmetros que perdem aderência sem a qualificação do objeto. Cada ficha traz o campo "Sob o OIC" com os trechos que ligam o conceito ao OIC, e a do OIC traz "Como integra os demais". Os demais conceitos aparecem sem número, sem hierarquia e em ordem alfabética. A Lex Plataformae é um conceito como os outros.
- 26/10/2026. As três ordens da tese (5.1, 7.1.1 e conclusão) viram leituras, sem numeração, e pertencem ao Roteiro. A sequência decisória do 7.1.1 vale para os enunciados, não para os conceitos do Atlas.
- 26/10/2026. Função social da propriedade intelectual e recomposição funcional com correção de regime saem do Atlas e seguem como passos do Roteiro (7.1.1.9 e 7.1.1.10). Suas fichas ficam preservadas.
- 26/10/2026. O feixe de fruição governada é gêmeo do OIC e aparece colado a ele em todos os percursos.
- 26/10/2026. A integridade pessoal fica fora do Atlas, na camada de bens protegidos. Orientação do autor, que não é nota para publicar. Integridade pessoal se refere à integridade da personalidade civil, e tudo o que integra a personalidade civil pode integrá-la. O lastro na tese está sobretudo no 6.1.3 (p. 534-536).
- 27/10/2026. Tudo o que está na tese será trazido, com o tempo, para a estrutura do site. O corpus já tem o texto integral. As camadas devem chegar a todas as seções. O mapa do caminho está em `estrutura/cobertura.md`, refeito a cada geração do site. Em 27/10/2026, capítulo 7 e conclusão completos, 59 de 116 seções com lugar numa camada. No mesmo dia, com Fundamentos e Método, capítulos 2, 3 e 4 completos e 89 de 116. Com Dogmática, 116 de 116. Toda seção da tese tem lugar em alguma camada além do corpus.
- 26/10/2026. Rascunhos podem ficar públicos no repositório antes da revisão, desde que cada informação traga o rastreio do trecho da tese de onde veio. A tese é pública. O site é ferramenta de leitura e ilustração da tese, e não substitui edição em livro.

## Arquivos

- `tese/andrade-2026-tese-oic-lex-plataformae.pdf` é a fonte de verdade. Página impressa = página do PDF - 2.
- `conceitos/` guarda as fichas dos conceitos.
- `conceitos/percursos.md` guarda os trechos que fundamentam os três percursos e a frase de abertura.
- `ferramentas/gerar_dados.py` lê as fichas e gera `dados/atlas.json` e `prototipo/index.html`. Nenhum texto citado é escrito à mão no site.
- `ferramentas/extrair_corpus.py` extrai a tese em 117 seções para `dados/corpus.json`, com PyMuPDF. Separa corpo, citações longas e notas pelo tamanho da fonte. Marca o início de cada página impressa. Quando uma seção começa no meio de uma página, repete a marca no início da seção. Não transcreve as páginas de epígrafe. Conferência de 26/10/2026, 819 notas e 819 chamadas, todas pareadas, e todas as citações das fichas encontradas na página certa. O parágrafo que atravessa a virada de página fica num só bloco, com a marca da página no meio. A linha vazia antes das notas de rodapé não fecha o parágrafo. Conferência de 27/10/2026, cerca de 370 quebras falsas desfeitas, com texto, 903 âncoras de página e 819 notas idênticos aos de antes.
- `ferramentas/gerar_site.py` gera o site publicável em `docs/`, a partir de `dados/atlas.json`. Cada página sai com o texto completo no HTML, legível sem JavaScript. Rodar sempre depois de `gerar_dados.py`. Nunca editar `docs/` à mão.
- `site/atlas.js` e `site/extra.css` são as fontes do script e dos acréscimos de estilo do site. O estilo base vem do `<style>` de `prototipo/modelo.html`.
- `ferramentas/fontes/` guarda as fontes servidas pelo próprio site (Archivo, Newsreader e IBM Plex Mono, sob SIL Open Font License), para não haver requisição ao Google.
- Auditoria de design com o detector do Impeccable (`npx impeccable detect --json docs`), autorizada pelo autor em 26/10/2026, sempre com `DO_NOT_TRACK=1`. Falsos positivos conhecidos, a grade do modo de desnudar e termos em inglês citados pela própria tese. O detector lê mal `!important` em altura de linha, e por isso a superfície evita esse recurso.
- `conteudo/camada-externa.md` guarda o texto simples da superfície, página por página e bloco por bloco, cada bloco com os trechos literais que condensa. Rascunho do Claude de 27/10/2026, publicado para revisão do autor no ar. Em cada conceito, a primeira frase do bloco nome é o próprio nome.
- `ferramentas/gerar_cartoes.py` gera as imagens de compartilhamento, 1200 x 630, em `site/cartoes/`, a partir dos textos da superfície. Cada cartão traz a pergunta da página e o nome da ideia, sem o nome do autor, salvo o da página do autor. O gerador do site copia os cartões e declara cada um nas metatags. Rodar de novo sempre que a superfície mudar.
- `ferramentas/medir_legibilidade.py` mede a superfície pelo índice de Flesch adaptado ao português (Martins e colegas, 1996), com contagem de sílabas aproximada. Meta de leitura fácil, de 50 para cima. Em 27/10/2026, 16 de 16 páginas na meta e 72 no conjunto.
- `estrutura/destaques.md` guarda os trechos literais que as páginas das camadas marcam no texto da tese, por seção e, no 7.1.3, por diretriz. A seleção é do site e a página diz isso ao leitor. O texto é conferido por script.
- A lista dos autores declarados nas aberturas dos capítulos 3 e 4 fica em `AUTORES`, em `ferramentas/gerar_site.py`, com o nome como a abertura o escreve, o sobrenome que a contagem procura e a chave da lista de referências. Grant McCraken aparece com a grafia da abertura do capítulo 3. A lista de referências grafa MCCRACKEN.
- A lista dos autores da abertura do capítulo 5 fica em `AUTORES_5`. O índice de dispositivos usa `PADRAO_DISPOSITIVO`, em `ferramentas/gerar_site.py`, e só reconhece artigo com o nome da lei na mesma frase. Conferência de 27/10/2026, 53 frases e 57 remissões a artigo, em cinco leis.
- `estrutura/cobertura.md` é gerado por `gerar_site.py` e mostra em que camadas cada seção da tese já tem lugar. Não editar à mão.
- `ferramentas/conferir_citacoes.py` confere toda citação literal contra a tese. Rodar antes de qualquer commit com conteúdo, com `python3 ferramentas/conferir_citacoes.py conceitos/ficha-canonica-v0.md conceitos/percursos.md estrutura/destaques.md conteudo/camada-externa.md`. Commit só com zero falhas.

## Epígrafes

As nove epígrafes emulam as nove Musas e formam um arco "do medo à fermata" (p. 78). Abertura, Lily Allen, The Fear (2009). Introdução, Lorde, The Love Club (2012). Cap. 2, Danni Carlos, Coisas Que Eu Sei (2008). Cap. 3, Christina Aguilera, Birds of Prey (2010). Cap. 4, MARINA, Oh No! (2010). Cap. 5, K/DA, Villain (2020). Cap. 6, Zélia Duncan, Diz Nos Meus Olhos (Inclemência) (2005). Cap. 7, Marisa Monte, Infinito Particular (2006). Cap. 8, Pitty, Temporal (2003).

No site, as letras não são reproduzidas. A música entra por player incorporado do Spotify, a partir de playlist do autor. O player só carrega quando o visitante clica, para não rastrear ninguém antes do consentimento, e nunca toca sozinho.

- Playlist do autor, "Objeto Imaterial de Consumo (OIC)", em https://open.spotify.com/playlist/35U1fRVLPlpPGAlsmqyLAS. Ordem conferida contra a tese em 26/10/2026. Nove de nove, na mesma sequência.
- Dados em `dados/epigrafes.json`, com a página de cada epígrafe.
- Componente pronto em `componentes/player-epigrafes.html`. Testado. Nenhum pedido ao Spotify antes do clique.

## Infraestrutura

- Hospedagem no GitHub Pages, a partir da pasta `docs/` do ramo `main`. O arquivo `docs/CNAME` fixa o domínio.
- Leitura por máquina em `docs/robots.txt` (aberto a robôs de IA), `docs/sitemap.xml`, `docs/llms.txt`, `docs/dados/atlas.json` e marcação schema.org (Thesis, DefinedTermSet e DefinedTerm) em cada página.
- 26/10/2026. O autor autorizou a publicação da versão 0.3 em construção. Em 27/10/2026 a versão passou a 0.4, com Roteiro e Laboratório, e no mesmo dia a 0.5, com as três camadas.
- 27/10/2026. Site no ar em https://lexplataformae.com.br, com HTTPS, servido pelo GitHub Pages. Domínio verificado na conta do autor.
- O ambiente de trabalho do Claude não alcança o domínio pelo terminal. Para conferir o site no ar, usar a ferramenta de busca de páginas, que pede autorização ao autor.
- DNS no Registro.br. Registros A do domínio raiz para 185.199.108.153, 185.199.109.153, 185.199.110.153 e 185.199.111.153. CNAME de www para victorlpandradeadv-creator.github.io. TXT de verificação do GitHub Pages na conta do autor.
- Evitar proxy da Cloudflare, que bloqueia robôs de IA por padrão em domínios novos.
