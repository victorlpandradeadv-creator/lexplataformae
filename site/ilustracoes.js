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
