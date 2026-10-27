# Projeto lexplataformae

Site de difusão da tese de doutorado de Victor L. P. Andrade, "Do regime jurídico do Objeto Imaterial de Consumo (OIC) sob a Lex Plataformae", UNESP, Franca, 2026. Domínio lexplataformae.com.br, registrado no Registro.br.

Este arquivo é a memória do projeto. Toda sessão que trabalhar aqui deve lê-lo antes de qualquer coisa.

## Arquitetura

O site tem cinco camadas.

1. **Corpus.** A tese dividida em seções citáveis, cada uma com endereço e página próprios.
2. **Atlas.** Uma página por conceito, com definição literal, função no regime, critério delimitador e seções de apoio. Os conceitos são os substantivos da tese.
3. **Roteiro.** Os dez enunciados do 7.1.1 como percurso guiado. Os enunciados são os verbos da tese. O portão de entrada são os quatro campos cumulativos do OIC (p. 428-429).
4. **Laboratório.** Casos em fichas de três campos, no formato do 7.3 (p. 788). Mecanismo de modulação lesiva, problema probatório e racionalidade de recomposição. O laboratório nunca conclui que algo "é abusivo".
5. **Leitura por máquina.** HTML estático, glossário estruturado, marcação de termos definidos, llms.txt e robots.txt aberto a robôs de IA.

## Regras inegociáveis

- Toda frase explicativa do site se ancora em página da tese. Não há relação entre conceitos sem página que a afirme.
- Citações são literais e conferidas por script contra o texto da tese antes de qualquer envio.
- Nada vai ao ar sem a leitura e a aprovação do autor.
- Todo conteúdo que não esteja na tese de 2026 recebe data e marca de acréscimo posterior.
- O site não pode ter nenhum padrão escuro de interface. Deve passar nos próprios critérios de auditabilidade aberta e equivalência de valor funcional.
- A identidade do projeto é acadêmica. A assinatura é de Victor L. P. Andrade. Escritório e empresas, se aparecerem, ficam em segundo plano.

## Estilo

- A prosa do site e as mensagens ao autor não usam ponto e vírgula, dois pontos nem travessão. Frases curtas e separadas. Citações literais da tese ficam como estão.
- Português primeiro. Versão inglesa do glossário em etapa posterior, sob a mesma assinatura acadêmica.

## Decisões pendentes do autor

- Uma ordem canônica ou três percursos. A tese tem três ordens (5.1, 7.1.1 e conclusão).
- Definição canônica de cada conceito.
- Lacuna da antecipação hipercuratorial, que não tem critério negativo geral na tese.
- Licença. Até a decisão, todos os direitos reservados. Proposta em estudo, MIT para o código e CC BY 4.0 para o conteúdo próprio, com exclusão expressa de material de terceiros.

## Decisões tomadas

- 26/10/2026. O Atlas tem nove conceitos. OIC, feixe de fruição governada, vulnerabilidade semiótica, antecipação hipercuratorial, teleologia abusiva, auditabilidade aberta, equivalência de valor funcional, função social da propriedade intelectual e recomposição funcional com correção de regime. A Lex Plataformae é o campo onde os nove acontecem e dá nome ao site. Esta última parte é leitura adotada, a confirmar com o autor.
- 26/10/2026. O feixe de fruição governada é gêmeo do OIC e aparece colado a ele em todos os percursos.
- 26/10/2026. A integridade pessoal fica fora do Atlas, na camada de bens protegidos. Nota do autor, a publicar como acréscimo posterior à tese. "Integridade pessoal se refere à integridade da personalidade civil. Tudo o que integra a personalidade civil pode integrá-la." O lastro na tese está sobretudo no 6.1.3 (p. 534-536).
- 26/10/2026. Rascunhos podem ficar públicos no repositório antes da revisão, desde que cada informação traga o rastreio do trecho da tese de onde veio. A tese é pública. O site é ferramenta de leitura e ilustração da tese, e não substitui edição em livro.

## Arquivos

- `tese/andrade-2026-tese-oic-lex-plataformae.pdf` é a fonte de verdade. Página impressa = página do PDF - 2.
- `conceitos/` guarda as fichas dos conceitos.
- `conceitos/percursos.md` guarda os trechos que fundamentam os três percursos e a frase de abertura.
- `ferramentas/gerar_dados.py` lê as fichas e gera `dados/atlas.json` e `prototipo/index.html`. Nenhum texto citado é escrito à mão no site.
- `ferramentas/conferir_citacoes.py` confere toda citação literal contra a tese. Rodar antes de qualquer commit com conteúdo, com `python3 ferramentas/conferir_citacoes.py <arquivos.md>`. Commit só com zero falhas.

## Epígrafes

As nove epígrafes emulam as nove Musas e formam um arco "do medo à fermata" (p. 78). Abertura, Lily Allen, The Fear (2009). Introdução, Lorde, The Love Club (2012). Cap. 2, Danni Carlos, Coisas Que Eu Sei (2008). Cap. 3, Christina Aguilera, Birds of Prey (2010). Cap. 4, MARINA, Oh No! (2010). Cap. 5, K/DA, Villain (2020). Cap. 6, Zélia Duncan, Diz Nos Meus Olhos (Inclemência) (2005). Cap. 7, Marisa Monte, Infinito Particular (2006). Cap. 8, Pitty, Temporal (2003).

No site, as letras não são reproduzidas. A música entra por player incorporado do Spotify, a partir de playlist do autor. O player só carrega quando o visitante clica, para não rastrear ninguém antes do consentimento, e nunca toca sozinho.

- Playlist do autor, "Objeto Imaterial de Consumo (OIC)", em https://open.spotify.com/playlist/35U1fRVLPlpPGAlsmqyLAS. Ordem conferida contra a tese em 26/10/2026. Nove de nove, na mesma sequência.
- Dados em `dados/epigrafes.json`, com a página de cada epígrafe.
- Componente pronto em `componentes/player-epigrafes.html`. Testado. Nenhum pedido ao Spotify antes do clique.

## Infraestrutura

- Hospedagem prevista no GitHub Pages, a partir deste repositório público.
- O DNS no Registro.br ainda não aponta para lugar nenhum. Antes de apontar, verificar o domínio no GitHub para evitar sequestro do domínio.
- Evitar proxy da Cloudflare, que bloqueia robôs de IA por padrão em domínios novos.
