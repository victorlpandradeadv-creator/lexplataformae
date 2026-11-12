# Leitura final do português (12/11/2026)

O autor pediu uma leitura completa da versão portuguesa depois das mudanças dos últimos dias. Você recebe um arquivo de origem (ou um trecho dele) e lê tudo, frase a frase.

Leia antes CLAUDE.md, seções Regras inegociáveis, Estilo e as decisões de 10/11 e 11/11/2026.

## O que procurar e corrigir na prosa do site

- Erro de digitação, concordância, regência, crase, palavra repetida, frase truncada ou que não fecha.
- Percurso como nome da seção do leigo, que agora é Caminho (percurso decisório e usos comuns ficam).
- Objeto Imaterial de Consumo por extenso mais de uma vez por página, ou em minúsculas onde nomeia a categoria. Fora disso vale OIC ou objeto imaterial de consumo em minúsculas aplicado a coisa concreta.
- Ponto e vírgula, dois pontos ou travessão na prosa do site.
- Imperativo didático (Pense, Imagine, Repare, Veja) e frases que tratam a teoria como ideia ou atribuem a doutrina à tese na Doutrina.
- Frase do leigo acima de 37 palavras.
- Pergunta de título que não corresponde ao bloco que abre.
- Inconsistência de termo com o resto do site (Lei da plataforma na Informação e na Doutrina, Lex Plataformae só na Ciência, Problemas, Direitos, Caminho, Vocabulário, Plataformas).

## O que nunca mexer

- Texto citado da tese. Linhas que começam com > ou >!, e qualquer trecho entre aspas seguido de (p. n). Esses são literais conferidos por script.
- Estrutura do arquivo (cabeçalhos ##, ###, chaves, campos). Só o texto da prosa.
- Sentido jurídico, modais e ressalvas. Nunca transformar possibilidade em garantia.

## Como trabalhar

1. Edite o arquivo com a ferramenta de edição, uma correção por vez.
2. No fim, rode python3 ferramentas/conferir_citacoes.py <arquivo> e confirme zero falhas.
3. Não rode gerar_site.py nem git.

Responda em português, curto. Quantas correções, e até três exemplos de antes e depois. Se achar algo que depende do autor, diga em uma linha.
