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

- Nove ou dez conceitos. A integridade pessoal entra no Atlas ou fica como camada de bens protegidos.
- Uma ordem canônica ou três percursos. A tese tem três ordens (5.1, 7.1.1 e conclusão).
- Definição canônica de cada conceito.
- Lacuna da antecipação hipercuratorial, que não tem critério negativo geral na tese.
- Licença. Até a decisão, todos os direitos reservados. Proposta em estudo, MIT para o código e CC BY 4.0 para o conteúdo próprio, com exclusão expressa de material de terceiros.
- Se rascunhos de conteúdo podem ficar públicos no repositório antes da revisão.

## Infraestrutura

- Hospedagem prevista no GitHub Pages, a partir deste repositório público.
- O DNS no Registro.br ainda não aponta para lugar nenhum. Antes de apontar, verificar o domínio no GitHub para evitar sequestro do domínio.
- Evitar proxy da Cloudflare, que bloqueia robôs de IA por padrão em domínios novos.
