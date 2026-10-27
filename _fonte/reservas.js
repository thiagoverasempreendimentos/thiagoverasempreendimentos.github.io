/* Página de casas: cartões montados de casas.js e reserva com mensagem pronta para o WhatsApp. */
(function(){
  var T = window.THIAGO, CASAS = window.CASAS || [];
  var brl = new Intl.NumberFormat('pt-BR', {style:'currency', currency:'BRL'});
  var brl0 = new Intl.NumberFormat('pt-BR', {style:'currency', currency:'BRL', maximumFractionDigits:0});
  var wa = window.waLink;
  function esc(s){ return String(s).replace(/[&<>"']/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }

  // Cartões das casas
  var lista = document.getElementById('lista-casas');
  var camIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="6" width="18" height="14" rx="2"/><circle cx="12" cy="13" r="3.5"/><path d="M8 6l1.5-2h5L16 6"/></svg>';
  CASAS.forEach(function(c){
    var info = [];
    if (c.quartos) info.push(c.quartos + (c.quartos === 1 ? ' quarto' : ' quartos'));
    if (c.capacidade) info.push('até ' + c.capacidade + ' pessoas');
    var el = document.createElement('article');
    el.className = 'card'; el.id = 'casa-' + c.id;
    el.innerHTML =
      '<button type="button" class="cover" aria-label="Ver fotos: ' + esc(c.nome) + '">' +
        '<img loading="lazy" src="' + esc(c.fotos[0]) + '" alt="' + esc(c.nome) + '">' +
        (c.fotos.length > 1 ? '<span class="count">' + camIcon + c.fotos.length + ' fotos</span>' : '') +
      '</button>' +
      '<div class="body">' +
        '<h3>' + esc(c.nome) + '</h3>' +
        ((c.cidade || info.length) ? '<p class="city">' + esc([c.cidade].concat(info).filter(Boolean).join(' · ')) + '</p>' : '') +
        '<p class="desc">' + esc(c.resumo || '') + '</p>' +
        '<div class="chips">' + (c.destaques || []).map(function(d){ return '<span>' + esc(d) + '</span>'; }).join('') + '</div>' +
        '<div class="foot">' +
          '<div class="price">' + (c.diaria ? 'Diária a partir de<br><b>' + brl0.format(c.diaria) + '</b>' : 'Valor<br><b>sob consulta</b>') + '</div>' +
          '<div class="acts"><button type="button" class="btn small reservar">Reservar</button></div>' +
        '</div>' +
      '</div>';
    lista.appendChild(el);
    el.querySelector('.cover').addEventListener('click', function(){ window.abrirGaleria(c.fotos.map(function(f){ return {src:f, alt:c.nome}; }), 0, c.nome); });
    el.querySelector('.reservar').addEventListener('click', function(){ abrirReserva(c); });
    if (c.video) {
      var v = document.createElement('video');
      v.controls = true; v.playsInline = true; v.preload = 'none';
      if (c.videoHorizontal) v.className = 'wide';
      if (c.poster) v.poster = c.poster;
      v.setAttribute('aria-label', 'Vídeo: ' + c.nome);
      var s = document.createElement('source'); s.src = c.video; s.type = 'video/mp4'; v.appendChild(s);
      el.querySelector('.chips').after(v);
    }
  });


  // Reserva: datas e mensagem pronta para o WhatsApp
  var dlg = document.getElementById('book');
  var inEl = document.getElementById('b-in'), outEl = document.getElementById('b-out'),
      pesEl = document.getElementById('b-pessoas'), nomeEl = document.getElementById('b-nome'),
      resumo = document.getElementById('b-resumo'), erro = document.getElementById('b-erro'),
      fin = document.getElementById('b-final'), tituloEl = document.getElementById('book-titulo');
  var casa = null;
  function iso(d){ return d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0'); }
  function parse(v){ var p = v.split('-'); return new Date(+p[0], +p[1]-1, +p[2]); }
  function br(d){ return String(d.getDate()).padStart(2,'0') + '/' + String(d.getMonth()+1).padStart(2,'0') + '/' + d.getFullYear(); }
  function noites(a, b){ return Math.round((b - a) / 86400000); }
  function show(msg){ erro.textContent = msg; erro.hidden = !msg; }
  function lock(msg){
    fin.setAttribute('aria-disabled', 'true'); fin.removeAttribute('href');
    fin.style.opacity = '.5'; fin.style.pointerEvents = 'none';
    if (msg) resumo.textContent = '—';
    show(msg || '');
  }
  function atualizar(){
    var a = inEl.value, b = outEl.value;
    if (!a || !b) { resumo.textContent = 'Escolha a entrada e a saída para ver o resumo.'; return lock(''); }
    var ci = parse(a), co = parse(b), hoje = parse(iso(new Date()));
    if (ci < hoje) return lock('A entrada não pode ser antes de hoje.');
    var n = noites(ci, co);
    if (n <= 0) return lock('A saída precisa ser depois da entrada.');
    if (n < casa.minNoites) return lock('Mínimo de ' + casa.minNoites + ' diárias nesta casa.');
    var pes = parseInt(pesEl.value, 10) || null;
    if (pes && casa.capacidade && pes > casa.capacidade) return lock('Esta casa acomoda até ' + casa.capacidade + ' pessoas.');
    for (var i = 0; i < casa.bloqueios.length; i++) {
      var bi = parse(casa.bloqueios[i][0]), bo = parse(casa.bloqueios[i][1]);
      if (ci < bo && co > bi) return lock('Já existe reserva nesse período. Escolha outras datas ou chame o Thiago.');
    }
    var total = casa.diaria ? n * casa.diaria : null;
    resumo.innerHTML = '<b>' + esc(casa.nome) + '</b><br>' + br(ci) + ' → ' + br(co) + ' · ' + n + (n === 1 ? ' diária' : ' diárias')
      + (pes ? ' · ' + pes + (pes === 1 ? ' pessoa' : ' pessoas') : '')
      + '<br>' + (total !== null ? 'Total estimado: <b>' + brl.format(total) + '</b>' : 'Valor: <b>a combinar com o Thiago</b>');
    var nome = nomeEl.value.trim();
    var linhas = ['Olá, Thiago! Quero reservar a *' + casa.nome + '*.', '',
      '📅 Entrada: ' + br(ci), '📅 Saída: ' + br(co) + ' (' + n + (n === 1 ? ' diária)' : ' diárias)')];
    if (pes) linhas.push('👥 ' + pes + (pes === 1 ? ' pessoa' : ' pessoas'));
    if (total !== null) linhas.push('💰 Total estimado: ' + brl.format(total));
    if (nome) linhas.push('', 'Meu nome: ' + nome);
    show('');
    fin.href = wa(linhas.join('\n'));
    fin.setAttribute('aria-disabled', 'false'); fin.style.opacity = ''; fin.style.pointerEvents = '';
  }
  function abrirReserva(c){
    casa = c;
    tituloEl.textContent = 'Reservar: ' + c.nome;
    var hoje = iso(new Date()); inEl.min = hoje; outEl.min = hoje;
    inEl.value = ''; outEl.value = '';
    pesEl.max = c.capacidade || 40;
    atualizar(); dlg.showModal();
  }
  inEl.addEventListener('change', function(){
    if (inEl.value) {
      var d = parse(inEl.value); d.setDate(d.getDate() + 1); outEl.min = iso(d);
      if (outEl.value && outEl.value <= inEl.value) outEl.value = '';
    }
    atualizar();
  });
  [outEl, pesEl, nomeEl].forEach(function(el){ el.addEventListener('input', atualizar); });
  dlg.querySelector('.xb').addEventListener('click', function(){ dlg.close(); });
  dlg.addEventListener('click', function(e){ if (e.target === dlg) dlg.close(); });
  dlg.querySelector('form').addEventListener('submit', function(e){ e.preventDefault(); });
  fin.addEventListener('click', function(e){ if (fin.getAttribute('aria-disabled') === 'true') e.preventDefault(); });
})();
