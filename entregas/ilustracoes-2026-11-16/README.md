# Entrega de ilustrações para integração posterior

16/11/2026. Envio autorizado pelo autor. Esta pasta entrega os arquivos produzidos na sessão; não substitui imagens em docs/assets nem altera páginas do site.

## Onde encontrar as versões atuais

| Pasta em atuais/ | Conteúdo | Estado na conversa |
|---|---|---|
| familia-1-nova | Seis portas; 12 WebPs de 480 × 480, mestres, pranchas e prova a 56px | Entregue para revisão; envio autorizado. Sem aprovação visual específica registrada após a entrega |
| familia-2-nova | Onze direitos; 22 WebPs e pacote completo com mestres e provas | Aprovado visualmente; integração pendente |
| familia-3-lote-1 | Seis peças do acervo; 12 WebPs e pacote completo | Grupo em revisão; família ainda incompleta |
| prototipo-pi | Comparação exclusividade / controle do uso | Aprovado visualmente |
| linguagem-pi-lote-1 | Quatro sólidos e duas relações | Aprovado visualmente |
| linguagem-pi-lote-2 | Seis relações explicativas | Aprovado visualmente |
| linguagem-pi-lote-3 | Quatro peças e página da linguagem | Aprovado visualmente |
| linguagem-pi-armadura-v2 | Três composições em cores planas, silhuetas idênticas entre temas | Aprovado visualmente; substitui a primeira sequência da armadura |

Os três lotes PI e a armadura são complementares ao planejamento principal de 73 composições. Há nomes de peças conceitualmente ajustados; usar os manifestos e descrições, não inferir relações jurídicas só pelo nome do arquivo.

## Como integrar

- Arquivos individuais PNG/WebP possuem transparência. Pranchas têm fundo e títulos apenas para revisão; não implantar pranchas como ilustrações.
- SVGs geométricos adaptáveis destinam-se à inserção direta no HTML. Quando inseridos via img, não herdam automaticamente as variáveis da página.
- Legendas são texto externo. Nenhuma letra ou número deve ser adicionado à arte.
- Azul do uso vem de tese-linha, não do acento da aba, que muda de cor na Doutrina.
- Respeitar modos e componentes reais. As provas nos seis fundos não autorizam repetir todas as imagens nos três modos.
- Os SVGs da armadura v2 incluem a mesma matriz e tratamento explícito em duas tintas; os WebPs já estão prontos. Não usar a variante generativa escura anterior.
- Imagens que reforçam títulos adjacentes usam alt vazio. Diagramas que acrescentam informação precisam das descrições externas equivalentes fornecidas.
- Nada aqui foi publicado, nem foi realizado teste de compreensão com leitores. Fontes jurídicas, responsividade e acessibilidade devem ser validadas antes da implantação.

## Histórico

historico-substituido contém os primeiros lotes de fundos opacos e a primeira sequência da armadura. Preservados a pedido de enviar tudo, mas NÃO usar na implementação nova. Na primeira entrega, os ZIPs locais não foram duplicados. A Família 2 nova inclui WebPs e SVGs avulsos e um pacote ZIP completo com PNGs, pranchas e provas.

planejamento reúne as instruções novas. PENDENTES.md lista as 50 composições restantes. fontes-producao guarda os scripts usados na sessão, que podem precisar de adaptação de caminhos locais. inventario-sha256.json permite verificar cada arquivo da entrega.

Para evitar dezenas de cópias da mesma imagem embutida, as matrizes PNG de SVGs e prévias HTML foram extraídas, sem alteração dos pixels, para matrizes-compartilhadas. Manter os caminhos relativos ao mover essas prévias. WebPs e PNGs finais continuam independentes.
