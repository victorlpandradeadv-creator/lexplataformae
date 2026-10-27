/* Lex Plataformae. Interações do site.
   O conteúdo já chega completo no HTML. Este script só acrescenta três coisas.
   1. A chave que desnuda a arquitetura da página.
   2. A troca entre as três leituras da tese na página inicial.
   3. O player das epígrafes, que só carrega o Spotify depois do clique. */
(function () {
  var reduzir = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var chave = document.getElementById('desnudar');
  if (chave) {
    chave.addEventListener('change', function () { document.body.classList.toggle('desnudo', chave.checked); });
  }

  document.querySelectorAll('.epigrafes-player').forEach(function (caixa) {
    var botao = caixa.querySelector('.epigrafes-carregar');
    if (!botao) return;
    botao.addEventListener('click', function () {
      var quadro = document.createElement('iframe');
      quadro.src = caixa.getAttribute('data-embed');
      quadro.title = 'Playlist das epígrafes da tese no Spotify';
      quadro.allow = 'clipboard-write; encrypted-media; fullscreen; picture-in-picture';
      quadro.loading = 'lazy';
      caixa.replaceChildren(quadro);
    });
  });

  var fonte = document.getElementById('leituras-dados');
  var lista = document.getElementById('sequencia');
  if (!fonte || !lista) return;
  var D = JSON.parse(fonte.textContent);
  var base = lista.getAttribute('data-base') || '';

  function esc(t) {
    return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function pg(ref) {
    var m = /^p\. (\d+)/.exec(ref);
    var slug = m && D.paginas ? D.paginas[m[1]] : null;
    if (slug) return '<a class="pg" href="tese/' + slug + '/#p' + m[1] + '" data-arq="âncora · leva ao trecho exato da tese">' + esc(ref) + '</a>';
    return '<span class="pg" data-arq="âncora · página da tese">' + esc(ref) + '</span>';
  }
  function link(id, nome) { return '<a href="' + base + id + '/">' + esc(nome) + '</a>'; }

  function corpoDoPasso(passo) {
    var c = D.conceitos[passo.id];
    var extra = D.passos[passo.id];
    if (c && c.tipo === 'conceito') {
      var nome = link(passo.id, c.nome);
      if (passo.par && D.conceitos[passo.par]) {
        var dica = passo.par_rotulo === 'gêmeos' ? 'Gêmeos por decisão do autor' : 'A tese trata os dois juntos em 5.1.3, 6.4 e 7.1.1.7';
        nome = '<span class="gemeos">' + link(passo.id, c.nome) + '<span class="gemeos-sinal" title="' + esc(dica) + '">' + esc(passo.par_rotulo) + '</span>' + link(passo.par, D.conceitos[passo.par].nome) + '</span>';
      }
      return { classe: 'passo', arq: null, html: '<span class="passo-nome">' + nome + '</span><span class="passo-papel">' + esc(passo.papel) + '</span>' };
    }
    if (c && c.tipo === 'roteiro') {
      return { classe: 'passo fantasma', arq: 'fora do Atlas · segue como passo do Roteiro',
        html: '<span class="passo-tipo">fora do Atlas · passo do Roteiro · ' + esc(c.secao) + '</span><span class="passo-nome">' + link(passo.id, c.nome) + '</span><span class="passo-papel">' + esc(passo.papel) + '</span>' };
    }
    if (c && c.tipo === 'bens') {
      return { classe: 'passo fantasma', arq: 'fora do Atlas · camada de bens protegidos',
        html: '<span class="passo-tipo">bens protegidos · 5.1.4 e 6.1.3</span><span class="passo-nome">' + link(passo.id, c.nome) + '</span><span class="passo-papel">' + esc(passo.papel) + '</span>' };
    }
    return { classe: 'passo fantasma', arq: 'fora do Atlas · passo do Roteiro',
      html: '<span class="passo-tipo">passo do Roteiro · ' + esc(extra.secao) + '</span><span class="passo-nome">' + esc(extra.nome) + '</span><span class="passo-papel">' + esc(passo.papel) + '</span>' };
  }

  function mostrar(chaveLeitura) {
    var p = D.percursos[chaveLeitura];
    var antes = {};
    var existentes = {};
    Array.prototype.forEach.call(lista.children, function (li) {
      existentes[li.getAttribute('data-chave')] = li;
      if (!reduzir) antes[li.getAttribute('data-chave')] = li.getBoundingClientRect();
    });
    var frag = document.createDocumentFragment();
    p.sequencia.forEach(function (passo) {
      var li = existentes[passo.id] || document.createElement('li');
      var c = corpoDoPasso(passo);
      li.className = c.classe;
      li.setAttribute('data-chave', passo.id);
      if (c.arq) li.setAttribute('data-arq', c.arq); else li.removeAttribute('data-arq');
      li.innerHTML = '<span class="passo-corpo">' + c.html + '</span>';
      frag.appendChild(li);
    });
    lista.innerHTML = '';
    lista.appendChild(frag);
    lista.setAttribute('aria-label', p.nome);
    var alvo = D.alvos && D.alvos[chaveLeitura];
    var chip = alvo ? '<a class="pg" href="' + alvo + '" data-arq="âncora · leva ao trecho exato da tese">' + esc(p.trecho.ref) + '</a>' : pg(p.trecho.ref);
    document.getElementById('logica').innerHTML = esc(p.logica) + ' <q>' + esc(p.trecho.texto) + '</q>' + chip;

    var presentes = {};
    p.sequencia.forEach(function (s) { presentes[s.id] = 1; if (s.par) presentes[s.par] = 1; });
    var ausentes = D.ordem.filter(function (id) { return !presentes[id]; });
    document.getElementById('fora').innerHTML = ausentes.length
      ? '<p>Fora desta leitura</p><ul>' + ausentes.map(function (id) { return '<li>' + link(id, D.conceitos[id].nome) + '</li>'; }).join('') + '</ul>'
      : '';

    if (!reduzir) {
      Array.prototype.forEach.call(lista.children, function (li) {
        var a = antes[li.getAttribute('data-chave')];
        var b = li.getBoundingClientRect();
        if (a) li.animate([{ transform: 'translateY(' + (a.top - b.top) + 'px)' }, { transform: 'none' }], { duration: 420, easing: 'cubic-bezier(.2,.7,.2,1)' });
        else li.animate([{ opacity: 0, transform: 'translateX(-8px)' }, { opacity: 1, transform: 'none' }], { duration: 320, easing: 'ease-out' });
      });
    }
  }

  var salva = null;
  try { salva = localStorage.getItem('lex-leitura'); } catch (e) {}
  if (salva && D.percursos[salva] && salva !== D.padrao) {
    var r = document.getElementById('percurso-' + salva);
    if (r) { r.checked = true; mostrar(salva); }
  }
  document.querySelectorAll('input[name="percurso"]').forEach(function (r) {
    r.addEventListener('change', function () {
      try { localStorage.setItem('lex-leitura', r.value); } catch (e) {}
      mostrar(r.value);
    });
  });
})();
