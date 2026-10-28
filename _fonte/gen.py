"""Gera as páginas do site (topo, menu e rodapé iguais em todas).
Uso: python3 gen.py <pasta de saída>"""
import sys, os, shutil

OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))

WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.1 5.1 0 0 0 1.1 2.7 11.7 11.7 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>'

def ico(path):
    return f'<i class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg></i>'

I_CASA = ico('<path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>')
I_ESCUDO = ico('<path d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7z"/><path d="M9 12l2 2 4-4"/>')
I_PIX = ico('<rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18M7 15h3"/>')
I_CHAT = ico('<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>')
I_PIN = ico('<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>')
I_REGUA = ico('<path d="M3 17L17 3l4 4L7 21H3z"/><path d="M14 6l2 2M11 9l2 2M8 12l2 2"/>')
I_LISTA = ico('<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4 6h.01M4 12h.01M4 18h.01"/>')
I_CALC = ico('<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 12h2M12 12h2M16 12h0M8 16h2M12 16h2"/>')
I_CAPACETE = ico('<path d="M4 16a8 8 0 0 1 16 0"/><path d="M2 16h20v3H2z"/><path d="M10 8V5h4v3"/>')
I_CARRINHO = ico('<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M3 4h2l2.5 11h11L21 7H6"/>')
I_RELOGIO = ico('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>')
I_CAMERA = ico('<rect x="3" y="6" width="18" height="14" rx="2"/><circle cx="12" cy="13" r="3.5"/><path d="M8 6l1.5-2h5L16 6"/>')

PAGES = [  # (arquivo, rótulo no menu)
    ('index.html', 'Início'),
    ('casas.html', 'Casas'),
    ('construcoes.html', 'Construções'),
    ('projetos.html', 'Projetos'),
    ('administracao.html', 'Administração'),
]

def nav(atual, cls=''):
    links = []
    for arq, rot in PAGES:
        cur = ' aria-current="page"' if arq == atual else ''
        links.append(f'<a href="{arq}"{cur}>{rot}</a>')
    links.append('<a href="#contato">Contato</a>')
    return '\n      '.join(links)

def head(titulo, descricao, capa, extra=''):
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{descricao}">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{descricao}">
<meta property="og:image" content="{capa}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta name="theme-color" content="#2b2b2b">
<meta name="color-scheme" content="only light">
<link rel="icon" type="image/png" href="favicon.png">
<link rel="apple-touch-icon" href="icon-192.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
{extra}</head>'''

BOTAO = {  # texto e destino do botão do topo, por página
    'index.html': ('Falar no WhatsApp', None, 'Olá, Thiago! Vim pelo site e quero mais informações.'),
    'casas.html': ('Reservar', '#casas', None),
    'construcoes.html': ('Pedir orçamento', None, 'Olá, Thiago! Quero um orçamento de obra.'),
    'projetos.html': ('Falar sobre meu projeto', None, 'Olá, Thiago! Quero conversar sobre um projeto.'),
    'administracao.html': ('Falar com o Thiago', None, 'Olá, Thiago! Tenho uma casa e quero falar sobre administração para locação.'),
}

def botao_topo(atual):
    texto, destino, msg = BOTAO[atual]
    if destino:
        return f'<a class="btn small" href="{destino}">{texto}</a>'
    return f'<a class="btn small wa-link" data-msg="{msg}" href="#" rel="noopener">{texto}</a>'

def topo(atual, msg):
    tema = atual.replace('.html', '').replace('index', 'inicio')
    return f'''<body class="tema-{tema}" data-msg="{msg}">

<div class="topbar">
  <div class="wrap">
    <span class="slogan">Confiança, qualidade e <em>resultados</em>.</span>
    <span class="info">
      <span class="hide-sm">🏖️ Aluguel por temporada · 🏗️ Construção · Projetos · Administração</span>
      <a class="hide-sm" href="https://www.instagram.com/thiago_veras_empreendimentos/" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>Instagram</a>
    </span>
  </div>
</div>

<header class="top" id="topo-fixo">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="Thiago Veras Empreendimentos, início"><img src="img/logo.png" alt="Thiago Veras Empreendimentos" width="90" height="64"></a>
    <nav class="menu" aria-label="Páginas">
      {nav(atual)}
    </nav>
    <div class="head-cta">
      {botao_topo(atual)}
      <button type="button" class="burger" aria-label="Abrir menu" aria-expanded="false" aria-controls="menu-cel"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    </div>
  </div>
</header>

<div class="drawer" id="menu-cel" aria-hidden="true">
  <div class="fundo"></div>
  <div class="painel" role="dialog" aria-label="Menu">
    <div class="topo"><img src="img/logo.png" alt="Thiago Veras Empreendimentos" width="76" height="54"><button type="button" class="fechar" aria-label="Fechar menu">×</button></div>
    <nav aria-label="Páginas">
      {nav(atual)}
    </nav>
    <a class="btn wa-link" href="#" rel="noopener">Falar no WhatsApp</a>
    <div class="rodape">
      <span>📍 Luís Correia, Piauí</span>
      <a href="https://www.instagram.com/thiago_veras_empreendimentos/" rel="noopener">@thiago_veras_empreendimentos</a>
    </div>
  </div>
</div>
'''

def page_hero(titulo, texto, img, alt, crumb=None):
    return f'''  <section class="page-hero" style="padding:0">
    <img src="{img}" alt="{alt}" fetchpriority="high">
    <div class="wrap">
      <p class="crumb"><a href="index.html">Início</a> › {crumb or titulo}</p>
      <h1>{titulo}</h1>
      <p>{texto}</p>
    </div>
  </section>
'''

def cta(titulo, texto, botao, msg=''):
    m = f' data-msg="{msg}"' if msg else ''
    return f'''  <section class="cta" id="contato">
    <div class="wrap">
      <h2>{titulo}</h2>
      <p>{texto}</p>
      <a class="btn wa-link"{m} href="#" rel="noopener">{botao}</a>
    </div>
  </section>
'''

def fim(scripts=''):
    links = ' · '.join(f'<a href="{a}">{r}</a>' for a, r in PAGES)
    return f'''</main>

<footer>
  <div class="wrap grid">
    <img src="img/logo.png" alt="Thiago Veras Empreendimentos" width="99" height="70">
    <div>
      <div><b>THIAGO V MUNIZ LTDA</b> · CNPJ 44.226.649/0001-09</div>
      <div>Avenida Prefeito Antonio de Padua da Costa Lima, 838, Centro · Luís Correia, PI · CEP 64220-000</div>
      <div>WhatsApp (86) 99866-2992</div>
      <div style="margin-top:8px">{links}</div>
    </div>
    <div class="links">
      <a href="https://www.instagram.com/thiago_veras_empreendimentos/" rel="noopener">Instagram</a>
      <a href="https://163-176-74-32.sslip.io/privacidade" rel="noopener">Política de privacidade</a>
    </div>
  </div>
</footer>

<a class="wa-float wa-link" href="#" rel="noopener" aria-label="Falar no WhatsApp">
  {WA_SVG}
</a>

<dialog id="gal" class="gal" aria-label="Fotos">
  <div class="stage"><img alt=""></div>
  <p class="cap"></p>
  <button type="button" class="icon-btn x" aria-label="Fechar">×</button>
  <button type="button" class="icon-btn prev" aria-label="Foto anterior">‹</button>
  <button type="button" class="icon-btn next" aria-label="Próxima foto">›</button>
</dialog>
{scripts}
<script src="casas.js"></script>
<script src="site.js"></script>
'''

def fechar(extra=''):
    return f'''{extra}</body>
</html>
'''

def galeria(titulo, fotos):
    bts = '\n'.join(f'        <button type="button"><img loading="lazy" src="{s}" alt="{a}"></button>' for s, a in fotos)
    return f'''      <div class="gallery" data-galeria="{titulo}">
{bts}
      </div>
'''

def servicos(itens):
    return '      <div class="servicos">\n' + '\n'.join(
        f'        <div class="servico">{i}<b>{t}</b><span>{d}</span></div>' for i, t, d in itens) + '\n      </div>\n'

JSONLD = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Thiago Veras Empreendimentos",
  "legalName": "THIAGO V MUNIZ LTDA",
  "taxID": "44.226.649/0001-09",
  "slogan": "Confiança, qualidade e resultados",
  "image": "img/capa.jpg",
  "telephone": "+55 86 99866-2992",
  "address": {"@type": "PostalAddress", "streetAddress": "Avenida Prefeito Antonio de Padua da Costa Lima, 838, Centro", "addressLocality": "Luís Correia", "addressRegion": "PI", "postalCode": "64220-000", "addressCountry": "BR"},
  "sameAs": ["https://www.instagram.com/thiago_veras_empreendimentos/"]
}
</script>
'''

def write(nome, html):
    with open(os.path.join(OUT, nome), 'w', encoding='utf-8') as f:
        f.write(html)

TRUST = f'''  <section class="trust" aria-label="Por que escolher a Thiago Veras">
    <ul>
      <li>{I_ESCUDO}<div>Empresa com CNPJ<span>Construtora &amp; Imobiliária</span></div></li>
      <li>{I_CASA}<div>Atendimento direto<span>Sem intermediários</span></div></li>
      <li>{I_PIN}<div>Luís Correia e região<span>Litoral do Piauí</span></div></li>
      <li>{I_CHAT}<div>WhatsApp<span>Resposta rápida</span></div></li>
    </ul>
  </section>
'''

# ---------------- Início ----------------
def area(n, arq, img, titulo, texto, botao):
    tema = arq.replace('.html', '')
    return f'''        <a class="area t-{tema}" href="{arq}" target="_blank" rel="noopener">
          <img src="{img}" alt="">
          <div class="txt"><span class="num">{n}</span><h3>{titulo}</h3><p>{texto}</p><span class="ir">{botao} <span>›</span></span></div>
        </a>'''

inicio = head('Thiago Veras Empreendimentos — Casas de temporada, construção e projetos em Luís Correia, PI',
              'Aluguel de casas de temporada, construção, projetos e administração de imóveis para temporada em Luís Correia e no litoral do Piauí.',
              'img/capa.jpg', JSONLD) + topo('index.html', 'Olá, Thiago! Vim pelo site e quero mais informações.') + f'''
<main id="topo">
  <section class="hub" style="padding:0">
    <img class="fundo" src="img/capa.jpg" alt="" fetchpriority="high">
    <div class="wrap">
      <div class="marca">
        <img class="marca-icone" src="img/logo-icone.png" alt="" width="130" height="74">
        <h1>Thiago <span class="leve">Veras</span><span class="emp">Empreendimentos</span></h1>
        <p class="slogan-g">Casas de temporada, construção e projetos no litoral do Piauí</p>
      </div>
      <p class="escolha">O que você procura?</p>
      <div class="areas">
{area('01', 'casas.html', 'img/casa-piscina-1.jpg', 'Casas', 'Casas de temporada com piscina, perto da praia. Reserve direto com o proprietário.', 'Ver casas')}
{area('02', 'construcoes.html', 'img/casa-fachada-2.jpg', 'Construções', 'Casas, sobrados, galpões e pontos comerciais, do início à entrega das chaves.', 'Ver obras')}
{area('03', 'projetos.html', 'img/casa-moderna-1.jpg', 'Projetos', 'Planejamento da sua obra: o que construir, em quais etapas e quanto vai custar.', 'Saiba mais')}
{area('04', 'administracao.html', 'img/casa-amarela-1.jpg', 'Administração', 'Você entrega a casa e cuidamos da locação: reservas, hóspedes, conservação e prestação de contas.', 'Saiba mais')}
      </div>
    </div>
    <span class="credit" id="credito-capa"></span>
  </section>

{TRUST}
  <section id="regiao" class="region">
    <div class="wrap grid">
      <div>
        <p class="eyebrow">A região</p>
        <h2>Luís Correia, o litoral do Piauí</h2>
        <p class="lead" style="margin-bottom:0">Praias de mar calmo e água morna, coqueirais e pôr do sol à beira-mar. Uma ótima base para conhecer o litoral piauiense e a região do Delta do Parnaíba.</p>
        <ul class="ticks">
          <li>Praias como Atalaia, Coqueiro e Macapá</li>
          <li>Perto de Parnaíba e da Pedra do Sal</li>
          <li>Passeios para o Delta do Parnaíba</li>
        </ul>
        <p style="margin-top:26px"><a class="btn" href="casas.html">Ver casas para alugar</a></p>
      </div>
      <div class="pics" id="pics-regiao">
        <div class="foto"><img loading="lazy" src="img/lugar-mar.jpg" alt="Praia de mar calmo e águas esverdeadas"></div>
        <div class="foto"><img loading="lazy" src="img/lugar-barracas.jpg" alt="Barracas de palha na faixa de areia"></div>
      </div>
    </div>
  </section>

{cta('Vamos conversar?', 'Seja para alugar uma casa na praia ou tirar a sua obra do papel, fale direto com o Thiago.', 'Falar no WhatsApp')}''' + fim() + fechar()
write('index.html', inicio)

# ---------------- Casas ----------------
casas = head('Casas de temporada em Luís Correia, PI — Thiago Veras Empreendimentos',
             'Casas de temporada com piscina em Luís Correia. Escolha a casa e as datas e reserve direto com o proprietário pelo WhatsApp.',
             'img/casa-piscina-1.jpg') + topo('casas.html', 'Olá, Thiago! Quero saber sobre as casas de temporada.') + f'''
<main id="topo">
{page_hero('Casas de temporada em Luís Correia', 'Piscina, espaço para a família e reserva direto com o proprietário, com pagamento por Pix.', 'img/capa.jpg', 'Praia de Luís Correia vista do alto', 'Casas')}
  <section class="trust" aria-label="Por que reservar com a gente">
    <ul>
      <li>{I_CASA}<div>Direto com o proprietário<span>Sem intermediários</span></div></li>
      <li>{I_ESCUDO}<div>Empresa com CNPJ<span>Construtora &amp; Imobiliária</span></div></li>
      <li>{I_PIX}<div>Pagamento por Pix<span>Entrada para garantir a data</span></div></li>
      <li>{I_CHAT}<div>Atendimento no WhatsApp<span>Resposta rápida</span></div></li>
    </ul>
  </section>

  <section id="casas">
    <div class="wrap">
      <p class="eyebrow">Casas de temporada</p>
      <h2>Escolha a sua casa</h2>
      <p class="lead">Toque na foto para ver mais imagens. Em “Reservar”, escolha as datas e finalize direto no WhatsApp do Thiago.</p>
      <div class="cards" id="lista-casas"></div>
    </div>
  </section>

  <section id="lugares" style="padding-top:0">
    <div class="wrap">
      <p class="eyebrow">O destino</p>
      <h2>Perto das casas</h2>
      <p class="lead">Praias de mar calmo, dunas e passeios para o Delta do Parnaíba. Pergunte ao Thiago a distância de cada casa até a praia.</p>
      <div class="lugares" id="lista-lugares"></div>
    </div>
  </section>

  <section id="como" style="padding-top:0">
    <div class="wrap">
      <p class="eyebrow">Simples e seguro</p>
      <h2>Como reservar</h2>
      <p class="lead">Em poucos minutos a sua data está encaminhada.</p>
      <div class="steps">
        <div class="step"><b>Escolha a casa e as datas</b><span>Veja as fotos, toque em “Reservar” e informe entrada, saída e número de pessoas.</span></div>
        <div class="step"><b>Finalize no WhatsApp</b><span>A mensagem já vai pronta para o Thiago, que confirma a disponibilidade e o valor.</span></div>
        <div class="step"><b>Pague a entrada por Pix</b><span>Com a entrada paga, a data fica garantida. O restante é combinado direto com ele.</span></div>
      </div>
    </div>
  </section>

  <section id="duvidas" style="padding-top:0">
    <div class="wrap">
      <p class="eyebrow">Dúvidas</p>
      <h2>Perguntas frequentes</h2>
      <div class="faq">
        <details><summary>Como faço a reserva?</summary><p>Escolha a casa, toque em “Reservar”, informe as datas e o número de pessoas e finalize no WhatsApp. O Thiago confirma a disponibilidade e o valor.</p></details>
        <details><summary>Quando a reserva fica garantida?</summary><p>Depois que o Thiago confirma a disponibilidade e você paga a entrada por Pix. Até lá, a data não está bloqueada.</p></details>
        <details><summary>Como é o pagamento?</summary><p>Uma entrada por Pix garante a data. A forma de pagar o restante é combinada direto com o Thiago no WhatsApp.</p></details>
        <details><summary>Posso ver mais fotos ou vídeos da casa?</summary><p>Sim. Peça no WhatsApp, que o Thiago envia mais imagens e tira suas dúvidas sobre a casa.</p></details>
        <details><summary>Qual o endereço das casas?</summary><p>As casas ficam em Luís Correia e região, no litoral do Piauí. A localização exata é enviada na confirmação da reserva.</p></details>
      </div>
    </div>
  </section>

{cta('Garanta sua data no litoral', 'Feriados e férias costumam lotar cedo. Chame o Thiago e confira a disponibilidade.', 'Falar no WhatsApp')}''' + fim() + fechar('''
<dialog id="book" class="book" aria-labelledby="book-titulo">
  <button type="button" class="xb" aria-label="Fechar">×</button>
  <form method="dialog" novalidate>
    <div><h3 id="book-titulo">Reservar</h3><p class="sub">Escolha as datas e finalize direto no WhatsApp do Thiago.</p></div>
    <input type="hidden" id="b-in"><input type="hidden" id="b-out">
    <div class="cal" id="cal" aria-label="Calendário de datas">
      <div class="cal-topo">
        <button type="button" class="cal-nav" id="cal-ant" aria-label="Mês anterior">‹</button>
        <strong id="cal-titulo" aria-live="polite"></strong>
        <button type="button" class="cal-nav" id="cal-prox" aria-label="Próximo mês">›</button>
      </div>
      <div class="cal-sem" aria-hidden="true"><span>D</span><span>S</span><span>T</span><span>Q</span><span>Q</span><span>S</span><span>S</span></div>
      <div class="cal-grade" id="cal-grade" role="grid"></div>
      <div class="cal-legenda"><span><i class="lg lg-livre"></i>Livre</span><span><i class="lg lg-ocup"></i>Ocupado</span><span><i class="lg lg-sel"></i>Sua escolha</span></div>
      <p class="cal-ajuda" id="cal-ajuda" role="status"></p>
    </div>
    <div class="two-col">
      <label>Pessoas<input type="number" id="b-pessoas" min="1" max="40" inputmode="numeric" placeholder="Ex.: 6"></label>
      <label>Seu nome<input type="text" id="b-nome" autocomplete="name" maxlength="60" placeholder="Ex.: Ana"></label>
    </div>
    <label>Seu WhatsApp (opcional)<input type="tel" id="b-whats" autocomplete="tel" inputmode="tel" maxlength="20" placeholder="(86) 99999-9999"></label>
    <p class="ocupadas" id="b-ocupadas" hidden></p>
    <div class="resumo" id="b-resumo" aria-live="polite">Escolha a entrada e a saída para ver o resumo.</div>
    <p class="erro" id="b-erro" role="alert" hidden></p>
    <a class="btn" id="b-final" href="#" rel="noopener" aria-disabled="true">Finalizar no WhatsApp</a>
    <p class="nota">Ao finalizar, as datas ficam seguras por algumas horas para você. A reserva só vale depois que o Thiago confirmar e você pagar a entrada.</p>
  </form>
</dialog>
<script src="reservas.js"></script>
''')
write('casas.html', casas)

# ---------------- Construções ----------------
OBRAS = [
    ('img/obra-sobrado.jpg', 'Sobrado em construção com andaime'),
    ('img/obra-casa.jpg', 'Casa em construção com entrada e calçada de pedra'),
    ('img/casa-moderna-1.jpg', 'Casa moderna entregue, com jardim e palmeira na entrada'),
    ('img/casa-moderna-2.jpg', 'Sala integrada com forro rebaixado e porcelanato'),
    ('img/casa-moderna-3.jpg', 'Cozinha com balcão de pedra escura'),
    ('img/casa-moderna-4.jpg', 'Fachada da casa moderna iluminada à noite'),
    ('img/obra-galpao.jpg', 'Fachada de galpão de blocos com portão de enrolar'),
    ('img/obra-galpao-interno.jpg', 'Interior de galpão amplo com telhado metálico'),
    ('img/obra-comercial.jpg', 'Fachada comercial iluminada à noite'),
]
construcoes = head('Construções em Luís Correia, PI — Thiago Veras Construtora & Imobiliária',
                   'Construção de casas, sobrados, galpões e pontos comerciais em Luís Correia e região, do início à entrega das chaves.',
                   'img/casa-fachada-2.jpg') + topo('construcoes.html', 'Olá, Thiago! Quero um orçamento de obra.') + f'''
<main id="topo">
{page_hero('Construção de casas, sobrados e galpões em Luís Correia', 'Do projeto à entrega das chaves, com acompanhamento em cada etapa.', 'img/casa-moderna-4.jpg', 'Fachada de casa construída pela Thiago Veras, iluminada à noite', 'Construções')}
  <section>
    <div class="wrap split">
      <div>
        <p class="eyebrow">Thiago Veras Construtora &amp; Imobiliária</p>
        <h2>Sua obra em boas mãos</h2>
        <p class="lead" style="margin-bottom:0">Construímos para quem vai morar, alugar ou abrir o próprio negócio, com acompanhamento em cada etapa.</p>
        <ul class="ticks">
          <li>Casas e sobrados residenciais</li>
          <li>Galpões e pontos comerciais</li>
          <li>Acompanhamento do início à entrega</li>
        </ul>
        <p style="margin-top:26px"><a class="btn wa-link" href="#" rel="noopener">Pedir orçamento</a></p>
      </div>
      <img loading="lazy" src="img/placa.jpg" alt="Fachada com a placa Thiago Veras Construtora e Imobiliária">
    </div>
  </section>

  <section class="build" id="obras">
    <div class="wrap">
      <p class="eyebrow">Portfólio</p>
      <h2>Obras realizadas</h2>
      <p class="lead">Toque em uma foto para ampliar.</p>
{galeria('Obras', OBRAS)}      <div class="video">
        <video controls playsinline preload="none" poster="video/obra.jpg" aria-label="Vídeo de uma obra em andamento">
          <source src="video/obra.mp4" type="video/mp4">
        </video>
        <div><h3 style="margin:0 0 6px">Veja uma obra em andamento</h3><p style="margin:0;color:#c9c1b8">Um passeio rápido pela construção de uma casa.</p></div>
      </div>
    </div>
  </section>

{cta('Vamos tirar sua obra do papel?', 'Conte o que você quer construir e receba um orçamento.', 'Pedir orçamento no WhatsApp')}''' + fim() + fechar()
write('construcoes.html', construcoes)

# ---------------- Projetos ----------------
projetos = head('Projetos — Thiago Veras Empreendimentos, Luís Correia, PI',
                'Planejamento e projeto da sua obra em Luís Correia e região: o que construir, em quais etapas e quanto vai custar.',
                'img/casa-piscina-3.jpg') + topo('projetos.html', 'Olá, Thiago! Quero conversar sobre um projeto.') + f'''
<main id="topo">
{page_hero('Projeto e planejamento da sua obra', 'Antes de construir, planejar: o que fazer, em quais etapas e quanto vai custar.', 'img/casa-piscina-3.jpg', 'Varanda ampla com forro rebaixado, rede e piscina ao fundo', 'Projetos')}
  <section>
    <div class="wrap">
      <p class="eyebrow">Do papel à obra</p>
      <h2>Como ajudamos no seu projeto</h2>
      <p class="lead">Tem um terreno ou uma ideia? Começamos entendendo o que você precisa e o quanto quer investir.</p>
{servicos([
    (I_REGUA, 'Projeto da obra', 'Casa, sobrado ou ponto comercial pensado para o seu terreno e para o seu uso.'),
    (I_CALC, 'Orçamento claro', 'Estimativa de custos por etapa, para você saber quanto vai investir.'),
    (I_LISTA, 'Planejamento das etapas', 'Ordem de execução e prazos, para a obra andar sem surpresas.'),
    (I_CHAT, 'Atendimento direto', 'Você conversa com quem vai construir, do início ao fim.'),
])}    </div>
  </section>

  <section class="region">
    <div class="wrap split">
      <img loading="lazy" src="img/casa-moderna-3.jpg" alt="Cozinha com balcão de pedra escura e porcelanato">
      <div>
        <h2>Projeto e obra com a mesma equipe</h2>
        <p class="lead" style="margin-bottom:0">Quem planeja também constrói. Assim o que foi combinado no projeto é o que sai na obra.</p>
        <p style="margin-top:26px"><a class="btn" href="construcoes.html">Ver obras realizadas</a></p>
      </div>
    </div>
  </section>

{cta('Conte sua ideia', 'Mande uma mensagem com o que você quer construir e onde fica o terreno.', 'Falar sobre meu projeto')}''' + fim() + fechar()
write('projetos.html', projetos)

# ---------------- Administração ----------------
administracao = head('Administração de imóveis para temporada — Thiago Veras Empreendimentos, Luís Correia, PI',
                     'Entregue sua casa para o Thiago administrar e cuidar da locação por temporada em Luís Correia, PI: reservas, hóspedes, limpeza e prestação de contas.',
                     'img/casa-amarela-1.jpg') + topo('administracao.html', 'Olá, Thiago! Tenho uma casa e quero falar sobre administração para locação.') + f'''
<main id="topo">
{page_hero('Administração de imóveis para locação por temporada', 'Você entrega a casa, a Thiago Veras cuida das reservas, dos hóspedes e da conservação.', 'img/casa-amarela-1.jpg', 'Casa amarela de dois andares com área externa ampla', 'Administração')}
  <section>
    <div class="wrap">
      <p class="eyebrow">Sua casa rendendo, sem dor de cabeça</p>
      <h2>O que a administração inclui</h2>
      <p class="lead">Ideal para quem tem casa em Luís Correia e não mora na cidade, não tem tempo ou não quer lidar com hóspedes no dia a dia.</p>
{servicos([
    (I_CASA, 'Divulgação e reservas', 'Sua casa anunciada, com calendário de datas e reservas organizadas.'),
    (I_CHAT, 'Atendimento aos hóspedes', 'Contato com os interessados, combinação das datas e recepção na entrada e na saída.'),
    (I_ESCUDO, 'Cuidado com o imóvel', 'Limpeza, conferência da casa e pequenos reparos entre uma locação e outra.'),
    (I_PIX, 'Prestação de contas', 'Você sabe quanto a casa rendeu e para onde foi cada valor.'),
])}    </div>
  </section>

  <section class="build">
    <div class="wrap">
      <p class="eyebrow">Exemplos de casas</p>
      <h2>Casas prontas para receber hóspedes</h2>
{galeria('Casas', [('img/casa-piscina-1.jpg', 'Casa com piscina e área gourmet'), ('img/casa-pergolado-1.jpg', 'Casa com jardim, pergolado e piscina'), ('img/casa-amarela-2.jpg', 'Casa amarela de dois andares'), ('img/casa-piscina-3.jpg', 'Varanda com rede e forro rebaixado')])}    </div>
  </section>

{cta('Tem uma casa para administrar?', 'Conte onde ela fica e como está, que o Thiago explica como funciona e combina os valores.', 'Falar no WhatsApp')}''' + fim() + fechar()
write('administracao.html', administracao)

shutil.copy(os.path.join(HERE, 'base.css'), os.path.join(OUT, 'style.css'))
shutil.copy(os.path.join(HERE, 'site.js'), os.path.join(OUT, 'site.js'))
shutil.copy(os.path.join(HERE, 'reservas.js'), os.path.join(OUT, 'reservas.js'))
print('ok:', ', '.join(a for a, _ in PAGES))
