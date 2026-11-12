# Leitura de continuidade da tese em inglês

Ordem do autor de 12/11/2026. A tradução integral da tese em inglês precisa ficar pronta como texto contínuo, e não só como segmentos revistos um a um. A revisão estrita de 10/11/2026 leu cada segmento contra o português. Esta leitura lê o capítulo inteiro em sequência, como um leitor de língua inglesa leria um livro acadêmico.

## O que fazer

1. Leia `traducao/glossario.md` e `traducao/instrucoes-revisor.md`, que dizem como a memória de tradução é editada (trava em `traducao/saida/.trava`, marcas numeradas intactas, chaves por segmento).
2. Leia em ordem, do começo ao fim, as páginas inglesas do seu trecho em `docs/en/tese/<seção>/index.html`, com o texto corrido e as notas. Abra o português correspondente em `docs/tese/<seção>/index.html` sempre que algo soar estranho.
3. Corrija na memória o que a leitura contínua revela e a leitura por segmento não pegava.
   - Termo técnico traduzido de dois jeitos no mesmo capítulo, ou fora do glossário.
   - Remissões internas incoerentes, como "as seen in section X" apontando para o lugar errado, ou "the former" e "the latter" trocados.
   - Conectivos entre parágrafos que não fazem a ligação que o português faz.
   - Repetição mecânica do mesmo começo de frase, como This, Thus, In this sense, em parágrafos seguidos.
   - Frases que quebram no meio por causa da divisão em segmentos.
   - Notas de rodapé com formatação ou tradução diferente das vizinhas.
   - Sentido trocado, ressalva perdida ou modal enfraquecido.
4. Não reescreva o que está bom. O tom é acadêmico, fluente e fiel. A pontuação da tese é preservada. Citações em língua estrangeira que a tese traz no original ficam como estão. Remissões às notas, marcas de página e marcas numeradas não mudam.
5. Não rode `gerar_site.py`. Outro processo cuida da geração.
6. Relate em inglês, em poucas linhas, quantos segmentos mudou, os problemas recorrentes e até cinco exemplos de antes e depois.

## Regras acrescentadas na segunda rodada

- Leitura integral. Leia cada parágrafo inteiro e cada nota inteira do seu trecho, em ordem. Não faça amostragem nem leitura por busca. Se a saída de uma ferramenta vier cortada, leia em pedaços menores até cobrir tudo. O relatório diz com honestidade o que foi e o que não foi lido.
- Pronome do consumidor, do usuário e da pessoa em geral. Use o singular they. He e his ficam só quando o texto fala de uma pessoa determinada, como um autor citado, ou de figura mítica, como Rá na conclusão.
- Termos já unificados na primeira rodada. "Tests of fit", "nominal restoration", "product-service dichotomy" com hífen, "See this section in the PDF", "electronic games".
