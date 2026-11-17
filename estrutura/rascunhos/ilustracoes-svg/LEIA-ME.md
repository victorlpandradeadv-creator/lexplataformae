# Ilustrações interativas em SVG

Feito em 16/11/2026, por orientação do autor. Rascunho para revisão, nada aplicado ao site.

As 32 composições que faltavam saíram por código. São as cinco da Família 3, as três entradas da Família 4 e os 24 problemas da Família 5, em `ferramentas/ilustracoes.py`. Cada composição tem uma geometria só. O tema escuro troca apenas a paleta.

Cada peça da figura é tocável. Fora do modo desnudo, o toque abre a caixa da peça, logo abaixo da imagem. No modo desnudo aparecem os marcadores numerados e todas as caixas. No celular elas se empilham debaixo da figura. Na tela larga ficam ao lado.

A frase de cada caixa é a frase leiga que já está no site, copiada sem mudança, e o programa a busca na fonte pelo começo, para nada ser digitado à mão. Além do consumo e Como reclamar não trazem trecho da tese, porque a página se apoia no Código Civil e nos canais oficiais. O trecho da tese só aparece a partir de Doutrina. As 90 citações passaram por `conferir_citacoes.py`, sem falha.

Arquivos.
- `<id>.svg` mestre semântico, com as cores do site.
- `<id>.html` fragmento pronto para o gerador.
- `<id>.webp` e `<id>-escuro.webp` entrega compatível, transparente.
- `prova.html` prancha nos seis fundos e em 320 pixels.
- `demo/` as páginas reais do site com a figura embutida. Abrir `demo/funcionalidade-cognitiva/index.html`.
- `site/ilustracoes.css` e `site/ilustracoes.js` o componente.
