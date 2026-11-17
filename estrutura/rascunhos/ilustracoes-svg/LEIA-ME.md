# Ilustrações interativas em SVG

Feito em 16/11/2026, por orientação do autor. Rascunho para revisão, nada aplicado ao site.

As cinco peças restantes da Família 3 saíram por código, em `ferramentas/ilustracoes.py`. Cada composição tem uma geometria só. O tema escuro troca apenas a paleta.

Cada peça da figura é tocável. Fora do modo desnudo, o toque abre a caixa da peça, logo abaixo da imagem. No modo desnudo aparecem os marcadores numerados e todas as caixas. No celular elas se empilham debaixo da figura. Na tela larga ficam ao lado.

A frase de cada caixa é a frase leiga que já está no site, copiada sem mudança. O trecho da tese só aparece a partir de Doutrina. As 15 citações passaram por `conferir_citacoes.py`, sem falha.

Arquivos.
- `<id>.svg` mestre semântico, com as cores do site.
- `<id>.html` fragmento pronto para o gerador.
- `<id>.webp` e `<id>-escuro.webp` entrega compatível, transparente.
- `prova.html` prancha nos seis fundos e em 320 pixels.
- `demo/` as páginas reais do site com a figura embutida. Abrir `demo/funcionalidade-cognitiva/index.html`.
- `site/ilustracoes.css` e `site/ilustracoes.js` o componente.
