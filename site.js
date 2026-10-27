/* Comum a todas as páginas: topo, menu do celular, WhatsApp e galeria de fotos. */
(function(){
  var T = window.THIAGO || {};
  function wa(text){ return 'https://wa.me/' + T.whatsapp + '?text=' + encodeURIComponent(text); }
  window.waLink = wa;

  // Topo: sombra ao rolar
  var topo = document.getElementById('topo-fixo');
  function rolou(){ topo.classList.toggle('scrolled', window.scrollY > 10); }
  window.addEventListener('scroll', rolou, {passive:true}); rolou();

  // No início, no celular, o botão flutuante cobriria os cartões: aparece ao rolar
  var flut = document.querySelector('.wa-float');
  if (flut && document.querySelector('.hub')) {
    var ajusta = function(){ flut.classList.toggle('oculto', window.innerWidth <= 560 && window.scrollY < 160); };
    window.addEventListener('scroll', ajusta, {passive:true}); window.addEventListener('resize', ajusta); ajusta();
  }

  // Menu do celular
  var drawer = document.getElementById('menu-cel'), burger = document.querySelector('.burger');
  function menu(abrir){
    drawer.classList.toggle('aberto', abrir); drawer.setAttribute('aria-hidden', String(!abrir));
    burger.setAttribute('aria-expanded', String(abrir));
    document.body.style.overflow = abrir ? 'hidden' : '';
    if (abrir) drawer.querySelector('.fechar').focus(); else burger.focus();
  }
  burger.addEventListener('click', function(){ menu(true); });
  drawer.querySelector('.fechar').addEventListener('click', function(){ menu(false); });
  drawer.querySelector('.fundo').addEventListener('click', function(){ menu(false); });
  drawer.querySelectorAll('nav a, .wa-link').forEach(function(a){ a.addEventListener('click', function(){ menu(false); }); });
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape' && drawer.classList.contains('aberto')) menu(false); });

  // Links de WhatsApp: mensagem do link, senão a da página
  var padrao = document.body.dataset.msg || 'Olá, Thiago! Vim pelo site e quero mais informações.';
  document.querySelectorAll('.wa-link').forEach(function(a){ a.href = wa(a.dataset.msg || padrao); });

  // Crédito da foto de capa (THIAGO.creditoCapa em casas.js)
  var cred = document.getElementById('credito-capa');
  if (cred && T.creditoCapa) cred.textContent = T.creditoCapa;

  // Galeria de fotos
  var gal = document.getElementById('gal');
  if (!gal) return;
  var galImg = gal.querySelector('.stage img'), galCap = gal.querySelector('.cap');
  var itens = [], atual = 0, titulo = '';
  function mostrar(i){
    atual = (i + itens.length) % itens.length;
    galImg.src = itens[atual].src; galImg.alt = itens[atual].alt;
    galCap.textContent = titulo + (itens.length > 1 ? ' · ' + (atual + 1) + ' de ' + itens.length : '');
    gal.querySelector('.prev').hidden = gal.querySelector('.next').hidden = itens.length < 2;
  }
  window.abrirGaleria = function(lista, i, t){ itens = lista; titulo = t; mostrar(i); gal.showModal(); };
  gal.querySelector('.x').addEventListener('click', function(){ gal.close(); });
  gal.querySelector('.prev').addEventListener('click', function(){ mostrar(atual - 1); });
  gal.querySelector('.next').addEventListener('click', function(){ mostrar(atual + 1); });
  gal.addEventListener('click', function(e){ if (e.target === gal || e.target.classList.contains('stage')) gal.close(); });
  gal.addEventListener('keydown', function(e){ if (e.key === 'ArrowLeft') mostrar(atual - 1); if (e.key === 'ArrowRight') mostrar(atual + 1); });
  var x0 = null;
  gal.addEventListener('touchstart', function(e){ x0 = e.touches[0].clientX; }, {passive:true});
  gal.addEventListener('touchend', function(e){ if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 40) mostrar(atual + (dx < 0 ? 1 : -1)); x0 = null; });

  // Galerias simples da página (data-galeria="Título")
  document.querySelectorAll('[data-galeria]').forEach(function(box){
    var botoes = box.querySelectorAll('button');
    var lista = Array.prototype.map.call(botoes, function(b){ var im = b.querySelector('img'); return {src: im.getAttribute('src'), alt: im.alt}; });
    botoes.forEach(function(b, i){ b.addEventListener('click', function(){ window.abrirGaleria(lista, i, box.dataset.galeria); }); });
  });
})();
