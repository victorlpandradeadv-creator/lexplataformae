/* Lex Plataformae. Interações do site.
   O conteúdo já chega completo no HTML. Este script só acrescenta interação.
   1. A chave Modo, com Informação, Doutrina e Ciência.
   2. A troca entre as três leituras da tese na página inicial.
   3. O player das epígrafes, que só carrega o Spotify depois do clique.
   4. O índice lateral, que marca o título em leitura. Sem script, ele continua sendo uma lista de links. */
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

  /* A arquitetura da Ciência. O controle fica guardado no navegador, e no toque a peça tocada acende. O CSS faz o resto, e o controle funciona sem script. */
  var arqTudo = document.getElementById('arq-tudo');
  if (arqTudo) {
    try { arqTudo.checked = localStorage.getItem('lexp-arq-tudo') === '1'; } catch (e) {}
    arqTudo.addEventListener('change', function () {
      try { localStorage.setItem('lexp-arq-tudo', arqTudo.checked ? '1' : '0'); } catch (e) {}
    });
    if (window.matchMedia && window.matchMedia('(hover: none)').matches) {
      document.addEventListener('click', function (e) {
        var acesa = document.querySelector('.arq-acesa');
        var peca = e.target.closest ? e.target.closest('[data-arq], [data-arq-mesmo]') : null;
        if (acesa) acesa.classList.remove('arq-acesa');
        if (peca && peca !== acesa && document.body.classList.contains('desnudo')) peca.classList.add('arq-acesa');
      });
    }
  }

  /* O balão de referência. Fora de Ciência a página não fica à vista. Ao passar o mouse, tocar ou chegar pelo teclado,
     o balão mostra a referência e oferece copiar o trecho com ela. O botão diz o que leva, e nada é acrescentado à cópia sem o clique. */
  var EN = (document.documentElement.lang || '').indexOf('en') === 0;
  var TX = EN ? { copiado: 'Copied', copiarRef: 'Copy with reference', copiarSo: 'Copy reference', autor: 'See the author', referencia: 'See the reference', trecho: 'Go to the passage', fonte: 'Source', livre: ' (free translation)' }
              : { copiado: 'Copiado', copiarRef: 'Copiar com referência', copiarSo: 'Copiar referência', autor: 'Ver o autor', referencia: 'Ver a referência', trecho: 'Ir ao trecho', fonte: 'Fonte', livre: '' };
  var REFERENCIA = 'Victor L. P. Andrade, Do regime jurídico do Objeto Imaterial de Consumo sob a Lex Plataformae, 2026';
  var conteineres = [];
  document.querySelectorAll('[data-ref], [data-cita]').forEach(function (el) { conteineres.push(el); });
  document.querySelectorAll('.pg').forEach(function (pg) {
    var c = pg.closest('blockquote, .campo-def, li, dd, p');
    if (c && !c.hasAttribute('data-ref') && conteineres.indexOf(c) < 0) conteineres.push(c);
  });
  var aberto = null, fechar = null;
  function dadosDe(c) {
    if (c.hasAttribute('data-cita')) {
      try { return { itens: JSON.parse(c.getAttribute('data-cita')) }; } catch (e) { return {}; }
    }
    var ref = c.getAttribute('data-ref'), alvo = c.getAttribute('data-alvo');
    var pg = c.querySelector(':scope > .pg, :scope > p > .pg, .pg');
    if (!ref && pg) { ref = pg.textContent.trim(); alvo = pg.getAttribute('href'); }
    return { ref: ref, alvo: alvo, autoria: c.getAttribute('data-autoria'), obra: c.getAttribute('data-obra') };
  }
  function textoDe(c) {
    var copia = c.cloneNode(true);
    copia.querySelectorAll('.pg, .nota-ref, .pg-marca, .balao-ref, .lei-ref, .cita-sinal, .original').forEach(function (e) { e.remove(); });
    return copia.textContent.replace(/\s+/g, ' ').replace(/^[“"]|[”"]$/g, '').trim();
  }
  function citacao(d) {
    if (d.obra) return d.obra + (d.ref ? ', ' + d.ref : '') + '.';
    return REFERENCIA + (d.ref ? ', ' + d.ref : '') + TX.livre + '.';
  }
  function copiar(texto, botao) {
    var feito = function () { botao.textContent = TX.copiado; setTimeout(function () { botao.textContent = TX.copiarRef; }, 1800); };
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
  function balaoDeAutores(c, itens) {
    var b = document.createElement('span');
    b.className = 'balao-ref balao-autores';
    b.setAttribute('role', 'note');
    var linhas = [];
    itens.forEach(function (i) {
      var l = document.createElement('span');
      l.className = 'balao-item';
      l.style.setProperty('--area', 'var(--a-' + i.area + ')');
      l.style.setProperty('--area-t', 'var(--a-' + i.area + '-t)');
      var a = document.createElement('span'); a.className = 'balao-autoria'; a.textContent = i.autoria || TX.fonte;
      var o = document.createElement('span'); o.className = 'balao-citacao'; o.textContent = (i.obra || '') + (i.pagina ? ', ' + i.pagina : '') + '.';
      var v = document.createElement('a'); v.href = i.url; v.textContent = /autores\/|autor\//.test(i.url) ? TX.autor : TX.referencia;
      l.appendChild(a); l.appendChild(o); l.appendChild(v);
      b.appendChild(l);
      linhas.push((i.obra || '') + (i.pagina ? ', ' + i.pagina : '') + '.');
    });
    var acoes = document.createElement('span'); acoes.className = 'balao-acoes';
    var botao = document.createElement('button'); botao.type = 'button'; botao.textContent = TX.copiarSo;
    botao.addEventListener('click', function (ev) {
      ev.stopPropagation();
      var bt = ev.currentTarget;
      var feito = function () { bt.textContent = TX.copiado; setTimeout(function () { bt.textContent = TX.copiarSo; }, 1800); };
      var texto = linhas.join('\n');
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(texto).then(feito, function () { reserva(texto); feito(); });
      else { reserva(texto); feito(); }
    });
    acoes.appendChild(botao); b.appendChild(acoes);
    return b;
  }
  function encaixar(b) {
    var r = b.getBoundingClientRect();
    if (r.right > window.innerWidth - 8) b.style.left = Math.min(0, window.innerWidth - 8 - r.right) + 'px';
    if (r.left < 8) b.style.left = (8 - r.left) + 'px';
  }
  function mostrarBalao(c) {
    if (aberto === c) { clearTimeout(fechar); return; }
    esconderBalao(true);
    var d = dadosDe(c);
    if (d.itens) {
      if (!d.itens.length) return;
      var ba = balaoDeAutores(c, d.itens);
      c.classList.add('com-ref');
      c.appendChild(ba);
      encaixar(ba);
      aberto = c;
      return;
    }
    if (!d.ref && !d.obra) return;
    var b = document.createElement('span');
    b.className = 'balao-ref';
    b.setAttribute('role', 'note');
    var url = d.alvo ? new URL(d.alvo, window.location.href).href : window.location.href;
    b.innerHTML = (d.autoria ? '<span class="balao-autoria"></span>' : '') + '<span class="balao-citacao"></span>' +
      '<span class="balao-acoes"><button type="button">' + TX.copiarRef + '</button>' + (d.alvo ? '<a>' + TX.trecho + '</a>' : '') + '</span>';
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
      quadro.title = EN ? 'Playlist of the thesis epigraphs on Spotify' : 'Playlist das epígrafes da tese no Spotify';
      quadro.allow = 'clipboard-write; encrypted-media; fullscreen; picture-in-picture';
      quadro.loading = 'lazy';
      caixa.replaceChildren(quadro);
    });
  });
  /* O índice lateral acompanha a leitura. Só rola a própria coluna, nunca a página. */
  var indice = document.querySelector('.lateral-indice');
  if (indice && 'IntersectionObserver' in window) {
    var caixa = document.querySelector('.lateral-fixa');
    var links = {};
    indice.querySelectorAll('a[href^="#"]').forEach(function (a) {
      links[decodeURIComponent(a.getAttribute('href').slice(1))] = a;
    });
    var alvos = Object.keys(links).map(function (id) { return document.getElementById(id); }).filter(Boolean);
    var marcar = function (id) {
      Object.keys(links).forEach(function (k) { links[k].removeAttribute('aria-current'); });
      var a = links[id];
      if (!a) return;
      a.setAttribute('aria-current', 'location');
      if (caixa && caixa.scrollHeight > caixa.clientHeight) {
        var ca = caixa.getBoundingClientRect(), la = a.getBoundingClientRect();
        if (la.top < ca.top || la.bottom > ca.bottom) caixa.scrollTop += la.top - ca.top - ca.height / 3;
      }
    };
    var observador = new IntersectionObserver(function () {
      var atual = null;
      alvos.forEach(function (el) {
        if (el.offsetParent !== null && el.getBoundingClientRect().top <= window.innerHeight * 0.3) atual = el;
      });
      if (atual) marcar(atual.id);
    }, { rootMargin: '-30% 0px -60% 0px', threshold: [0, 1] });
    alvos.forEach(function (el) { observador.observe(el); });
  }


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
        var dica = passo.id === 'oic' ? 'Formulação do autor, acréscimo posterior de 05/11/2026. O resumo da tese propõe o OIC enquanto feixe de fruição governada (p. 11)' : 'A tese formula a teleologia abusiva como categoria de ilícito de arquitetura (p. 794)';
        nome = '<span class="gemeos">' + link(passo.id, c.nome) + '<span class="gemeos-sinal" title="' + esc(dica) + '">' + esc(passo.par_rotulo) + '</span>' + link(passo.par, D.conceitos[passo.par].nome) + '</span>';
      }
      return { classe: 'passo', arq: null, html: '<span class="passo-nome">' + nome + '</span><span class="passo-papel">' + esc(passo.papel) + '</span>' };
    }
    if (c && c.tipo === 'roteiro') {
      return { classe: 'passo fantasma', arq: 'fora dos nove · segue como enunciado dos Parâmetros',
        html: '<span class="passo-tipo">fora dos nove · enunciado dos Parâmetros · ' + esc(c.secao) + '</span><span class="passo-nome">' + link(passo.id, c.nome) + '</span><span class="passo-papel">' + esc(passo.papel) + '</span>' };
    }
    if (c && c.tipo === 'bens') {
      return { classe: 'passo fantasma', arq: 'fora dos nove · camada de bens protegidos',
        html: '<span class="passo-tipo">bens protegidos · 5.1.4 e 6.1.3</span><span class="passo-nome">' + link(passo.id, c.nome) + '</span><span class="passo-papel">' + esc(passo.papel) + '</span>' };
    }
    return { classe: 'passo fantasma', arq: 'fora dos nove · enunciado dos Parâmetros',
      html: '<span class="passo-tipo">enunciado dos Parâmetros · ' + esc(extra.secao) + '</span><span class="passo-nome">' + esc(extra.nome) + '</span><span class="passo-papel">' + esc(passo.papel) + '</span>' };
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

// A chave de modo sai do caminho enquanto o leitor desce e volta quando ele sobe, para não cobrir o texto.
// Volta também no fim da página e quando recebe foco. Crítica de 09/11/2026.
(function () {
  var chave = document.querySelector('.chave-mestra');
  if (!chave) return;
  var ultimo = window.scrollY, pedido = false;
  function ajustar() {
    pedido = false;
    var y = window.scrollY, fim = y + window.innerHeight >= document.documentElement.scrollHeight - 80;
    if (fim || y < 80 || y < ultimo - 4) chave.classList.remove('recolhida');
    else if (y > ultimo + 4 && !chave.contains(document.activeElement)) chave.classList.add('recolhida');
    ultimo = y;
  }
  window.addEventListener('scroll', function () { if (!pedido) { pedido = true; requestAnimationFrame(ajustar); } }, { passive: true });
  chave.addEventListener('focusin', function () { chave.classList.remove('recolhida'); });
})();

// As portas da capa que levam ao jurista já abrem a página seguinte em Doutrina. Capa de 10/11/2026.
document.addEventListener('click', function (ev) {
  var a = ev.target.closest && ev.target.closest('a[data-modo]');
  if (!a) return;
  try { localStorage.setItem('lexp-nivel', a.getAttribute('data-modo')); } catch (e) {}
});

// Em telas menores o índice começa recolhido. Sem script todos os links seguem
// disponíveis, e abrir ou fechar o índice nunca muda a profundidade da leitura.
(function () {
  if (!window.matchMedia) return;
  var pequeno = window.matchMedia('(max-width: 899px)');
  var paineis = document.querySelectorAll('details[data-recolher-mobile]');
  function ajustarIndices() {
    paineis.forEach(function (painel) { painel.open = !pequeno.matches; });
  }
  ajustarIndices();
  if (pequeno.addEventListener) pequeno.addEventListener('change', ajustarIndices);
})();

/* Modo escuro. Sem escolha guardada, o site segue o aparelho. 10/11/2026. */
(function () {
  var raiz = document.documentElement;
  var EN = (raiz.lang || '').indexOf('en') === 0;
  function escuro() {
    if (raiz.dataset.theme) return raiz.dataset.theme === 'dark';
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  function pinta() {
    var e = escuro();
    var rotulo = e ? (EN ? 'Light mode' : 'Modo claro') : (EN ? 'Dark mode' : 'Modo escuro');
    document.querySelectorAll('.topo .tema').forEach(function (b) {
      b.setAttribute('aria-pressed', e ? 'true' : 'false'); b.setAttribute('aria-label', rotulo); b.title = rotulo;
    });
  }
  document.addEventListener('click', function (ev) {
    var b = ev.target.closest && ev.target.closest('.topo .tema');
    if (!b) return;
    var novo = escuro() ? 'claro' : 'escuro';
    raiz.dataset.theme = novo === 'escuro' ? 'dark' : 'light';
    try { localStorage.setItem('lexp-tema', novo); } catch (e) {}
    pinta();
  });
  if (window.matchMedia) { try { window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', pinta); } catch (e) {} }
  pinta();
})();

/* Quebras dos textos curtos. Em texto de até duas ou três linhas, cada frase que cabe inteira numa linha começa
   numa linha própria, e o que sobra se distribui sem palavra solta na última linha. Parágrafos longos ficam como estão.
   Revisão de quebras de 11/11/2026. */
(function () {
  var SEL = 'h1,h2,h3,h4,p,li,dt,dd,figcaption,summary,.porta a,.cartao a,td,th';
  var MAX = 240;
  var ABREV = /(?:\b(?:p|pp|art|arts|n|nº|cf|ex|Jr|Sr|Sra|Dr|Dra|v|vol|ed|No|Nos|e\.g|i\.e|etc))$/i;
  function linhas(el) {
    var tops = [], w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), no;
    while ((no = w.nextNode())) {
      if (!no.nodeValue.trim() || !no.parentElement.getClientRects().length) continue;
      var cs = getComputedStyle(no.parentElement);
      if (cs.visibility === 'hidden' || cs.position === 'absolute') continue;
      var r = document.createRange(); r.selectNodeContents(no);
      Array.prototype.forEach.call(r.getClientRects(), function (x) {
        if (x.width < 1) return;
        if (!tops.some(function (t) { return Math.abs(t - x.top) < x.height * 0.5; })) tops.push(x.top);
      });
    }
    return tops.length;
  }
  function limpa(el) {
    el.querySelectorAll('br.qf').forEach(function (b) { b.remove(); });
    el.normalize();
    el.classList.remove('curto');
  }
  function quebra(el) {
    var n = 0, w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), nos = [], t;
    while ((t = w.nextNode())) nos.push(t);
    nos.forEach(function (no) {
      var re = /([.?!])(\s+)(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ“"(¿¡])/g, m, s = no.nodeValue, cortes = [];
      while ((m = re.exec(s))) { if (!ABREV.test(s.slice(0, m.index))) cortes.push(m.index + 1); }
      for (var i = cortes.length - 1; i >= 0; i--) {
        var resto = no.splitText(cortes[i]);
        var br = document.createElement('br'); br.className = 'qf';
        resto.parentNode.insertBefore(br, resto); n++;
      }
    });
    return n;
  }
  function ajusta() {
    document.querySelectorAll(SEL).forEach(function (el) {
      if (!el.offsetParent || el.closest('.tese-texto, pre, code')) return;
      if (el.querySelector('p,li,div,ul,ol,h1,h2,h3,h4,br:not(.qf)')) return;
      limpa(el);
      var txt = (el.textContent || '').trim();
      if (txt.length > MAX) return;
      var antes = linhas(el);
      if (antes < 2) return;
      var frases = quebra(el);
      if (frases > 0 && frases <= 2 && linhas(el) === frases + 1) return;
      limpa(el);
      el.classList.add('curto');
    });
  }
  var espera;
  function agenda() { clearTimeout(espera); espera = setTimeout(ajusta, 120); }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(ajusta); else ajusta();
  window.addEventListener('resize', agenda);
  document.addEventListener('click', function () { setTimeout(ajusta, 60); });
})();
