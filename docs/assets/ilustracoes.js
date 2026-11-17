// Ilustrações interativas. Feito em 16/11/2026, por orientação do autor.
// Tocar numa peça abre a caixa dela. Tocar de novo, ou apertar Esc, fecha.
// No modo desnudo as caixas já estão abertas, e o toque só leva até a caixa e a acende.
(function () {
  function desnudo() { return document.body.classList.contains('desnudo') || !!document.querySelector('#nivel-2:checked'); }

  function acender(fig, n, liga) {
    fig.querySelectorAll('[data-peca="' + n + '"]').forEach(function (el) { el.classList.toggle('acesa', liga); });
  }

  function alternar(fig, peca) {
    var n = peca.getAttribute('data-peca');
    var caixa = fig.querySelector('.il-caixa[data-peca="' + n + '"]');
    if (!caixa) return;
    if (desnudo()) {
      fig.querySelectorAll('.il-caixa.acesa').forEach(function (c) { c.classList.remove('acesa'); });
      caixa.classList.add('acesa');
      caixa.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      return;
    }
    var abrir = !caixa.classList.contains('aberta');
    fig.querySelectorAll('.il-caixa.aberta').forEach(function (c) { c.classList.remove('aberta'); });
    fig.querySelectorAll('.il-peca.ativa').forEach(function (p) { p.classList.remove('ativa'); p.setAttribute('aria-expanded', 'false'); });
    if (abrir) {
      caixa.classList.add('aberta');
      peca.classList.add('ativa');
      peca.setAttribute('aria-expanded', 'true');
      caixa.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
  }

  document.querySelectorAll('figure.il').forEach(function (fig) {
    fig.querySelectorAll('.il-peca').forEach(function (peca) {
      var n = peca.getAttribute('data-peca');
      peca.setAttribute('aria-expanded', 'false');
      peca.setAttribute('aria-controls', fig.getAttribute('data-il') + '-caixa-' + n);
      peca.addEventListener('click', function () { alternar(fig, peca); });
      peca.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); alternar(fig, peca); }
        if (e.key === 'Escape' && peca.classList.contains('ativa')) alternar(fig, peca);
      });
      peca.addEventListener('mouseenter', function () { acender(fig, n, true); });
      peca.addEventListener('mouseleave', function () { acender(fig, n, false); });
    });
    fig.querySelectorAll('.il-caixa').forEach(function (c) {
      var n = c.getAttribute('data-peca');
      c.addEventListener('mouseenter', function () { acender(fig, n, true); });
      c.addEventListener('mouseleave', function () { acender(fig, n, false); });
    });
  });
})();

// 17/11/2026, por ordem do autor. O desenho ocupa o quadro inteiro. O viewBox se ajusta ao que está desenhado, com folga.
(function () {
  document.querySelectorAll('svg.il-svg').forEach(function (svg) {
    try {
      var x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
      Array.prototype.forEach.call(svg.children, function (el) {
        if (!el.getBBox || /^(style|title|desc|defs)$/i.test(el.tagName)) return;
        var b = el.getBBox();
        if (!b.width && !b.height) return;
        x0 = Math.min(x0, b.x); y0 = Math.min(y0, b.y); x1 = Math.max(x1, b.x + b.width); y1 = Math.max(y1, b.y + b.height);
      });
      if (!isFinite(x0)) return;
      var f = 48;
      svg.setAttribute('viewBox', (x0 - f) + ' ' + (y0 - f) + ' ' + (x1 - x0 + 2 * f) + ' ' + (y1 - y0 + 2 * f));
    } catch (e) {}
  });
})();
