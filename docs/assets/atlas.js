/* Lex Plataformae. Interações do site.
   O conteúdo já chega completo no HTML. Este script só acrescenta interação.
   1. A chave Modo, com Informação, Doutrina e Ciência.
   2. A troca entre as três leituras da tese na página inicial.
   3. O player das epígrafes, que só carrega o Spotify depois do clique. */
(function () {
  var reduzir = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* A chave Modo tem três posições. 0 é Informação, para o leigo, 1 é Doutrina, para o técnico, e 2 é Ciência, para o expert.
     A escolha acompanha a navegação. Cada página tem um modo mínimo, e escolher um modo abaixo dele leva à página de superfície. */
  var degraus = document.querySelectorAll('input[name="nivel"]');
  if (degraus.length) {
    var minimo = parseInt(document.body.getAttribute('data-minimo') || '0', 10) || 0;
    var aplicar = function (n) {
      document.body.classList.toggle('aberto', n > 0);
      document.body.classList.toggle('desnudo', n > 1);
    };
    var lembrar = function (n) { try { localStorage.setItem('lexp-nivel', String(n)); } catch (e) {} };
    var atual = document.querySelector('input[name="nivel"]:checked');
    aplicar(atual ? parseInt(atual.value, 10) : 0);
    degraus.forEach(function (r) {
      r.addEventListener('change', function () {
        var n = parseInt(r.value, 10);
        lembrar(n);
        if (n < minimo) {
          window.location.href = document.body.getAttribute('data-superficie') || '/';
          return;
        }
        aplicar(n);
      });
    });
  }

  /* O balão de referência. Fora de Ciência a página não fica à vista. Ao passar o mouse, tocar ou chegar pelo teclado,
     o balão mostra a referência e oferece copiar o trecho com ela. O botão diz o que leva, e nada é acrescentado à cópia sem o clique. */
  var REFERENCIA = 'Victor L. P. Andrade, Do regime jurídico do Objeto Imaterial de Consumo sob a Lex Plataformae, 2026';
  var conteineres = [];
  document.querySelectorAll('[data-ref]').forEach(function (el) { conteineres.push(el); });
  document.querySelectorAll('.pg').forEach(function (pg) {
    var c = pg.closest('blockquote, .campo-def, li, dd, p');
    if (c && !c.hasAttribute('data-ref') && conteineres.indexOf(c) < 0) conteineres.push(c);
  });
  var aberto = null, fechar = null;
  function dadosDe(c) {
    var ref = c.getAttribute('data-ref'), alvo = c.getAttribute('data-alvo');
    var pg = c.querySelector(':scope > .pg, :scope > p > .pg, .pg');
    if (!ref && pg) { ref = pg.textContent.trim(); alvo = pg.getAttribute('href'); }
    return { ref: ref, alvo: alvo, autoria: c.getAttribute('data-autoria'), obra: c.getAttribute('data-obra') };
  }
  function textoDe(c) {
    var copia = c.cloneNode(true);
    copia.querySelectorAll('.pg, .nota-ref, .pg-marca, .balao-ref, .lei-ref, .autor-tag').forEach(function (e) { e.remove(); });
    return copia.textContent.replace(/\s+/g, ' ').replace(/^[“"]|[”"]$/g, '').trim();
  }
  function citacao(d) {
    if (d.obra) return d.obra + (d.ref ? ', ' + d.ref : '') + '.';
    return REFERENCIA + (d.ref ? ', ' + d.ref : '') + '.';
  }
  function copiar(texto, botao) {
    var feito = function () { botao.textContent = 'Copiado'; setTimeout(function () { botao.textContent = 'Copiar com referência'; }, 1800); };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(texto).then(feito, function () { reserva(texto); feito(); });
    } else { reserva(texto); feito(); }
  }
  function reserva(texto) {
    var t = document.createElement('textarea');
    t.value = texto; t.setAttribute('readonly', ''); t.style.position = 'fixed'; t.style.opacity = '0';
    document.body.appendChild(t); t.select();
    try { document.execCommand('copy'); } catch (e) {}
    t.remove();
  }
  function mostrarBalao(c) {
    if (aberto === c) { clearTimeout(fechar); return; }
    esconderBalao(true);
    var d = dadosDe(c);
    if (!d.ref && !d.obra) return;
    var b = document.createElement('span');
    b.className = 'balao-ref';
    b.setAttribute('role', 'note');
    var url = d.alvo ? new URL(d.alvo, window.location.href).href : window.location.href;
    b.innerHTML = (d.autoria ? '<span class="balao-autoria"></span>' : '') + '<span class="balao-citacao"></span>' +
      '<span class="balao-acoes"><button type="button">Copiar com referência</button>' + (d.alvo ? '<a>Ir ao trecho</a>' : '') + '</span>';
    if (d.autoria) b.querySelector('.balao-autoria').textContent = d.autoria;
    b.querySelector('.balao-citacao').textContent = citacao(d);
    if (d.alvo) b.querySelector('a').setAttribute('href', d.alvo);
    b.querySelector('button').addEventListener('click', function (ev) {
      ev.stopPropagation();
      copiar('“' + textoDe(c) + '”\n' + citacao(d) + '\n' + url, ev.currentTarget);
    });
    c.classList.add('com-ref');
    c.appendChild(b);
    aberto = c;
  }
  function esconderBalao(agora) {
    clearTimeout(fechar);
    var feche = function () { if (aberto) { var b = aberto.querySelector(':scope > .balao-ref'); if (b) b.remove(); aberto = null; } };
    if (agora) feche(); else fechar = setTimeout(feche, 280);
  }
  conteineres.forEach(function (c) {
    c.addEventListener('pointerenter', function (ev) { if (ev.pointerType === 'mouse') mostrarBalao(c); });
    c.addEventListener('pointerleave', function (ev) { if (ev.pointerType === 'mouse') esconderBalao(false); });
    c.addEventListener('focusin', function () { mostrarBalao(c); });
    c.addEventListener('focusout', function (ev) { if (!c.contains(ev.relatedTarget)) esconderBalao(false); });
    c.addEventListener('click', function (ev) {
      if (ev.target.closest('a, button, .balao-ref')) return;
      var sel = window.getSelection && String(window.getSelection());
      if (sel) return;
      if (aberto === c) esconderBalao(true); else mostrarBalao(c);
    });
  });
  document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') esconderBalao(true); });

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
        var dica = passo.par_rotulo === 'enquanto' ? 'O resumo da tese propõe o OIC enquanto feixe de fruição governada' : 'A tese trata os dois juntos em 5.1.3, 6.4 e 7.1.1.7';
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
