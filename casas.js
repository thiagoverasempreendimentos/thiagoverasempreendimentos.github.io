/*
 * Dados das casas e do contato. É só este arquivo que muda para atualizar
 * fotos, preços, capacidade e datas ocupadas. O site monta tudo a partir daqui.
 *
 *  codigo      código da casa no servidor de reservas (C01...), não mudar
 *  nome        nome que aparece no site e na mensagem do WhatsApp
 *  cidade      ex.: 'Luís Correia' (null = não mostra)
 *  resumo      uma frase sobre a casa
 *  destaques   o que a casa tem (aparece como etiquetas)
 *  fotos       caminhos das fotos; a primeira é a capa
 *  diaria      valor da diária em reais (null = "valor a combinar", sem total)
 *  capacidade  máximo de pessoas (null = não mostra nem limita)
 *  quartos     número de quartos (null = não mostra)
 *  minNoites   mínimo de diárias
 *  video       caminho do vídeo da casa, ex.: 'video/amarela.mp4' (opcional)
 *  poster      imagem de capa do vídeo, ex.: 'video/amarela.jpg' (opcional)
 *  videoHorizontal  true se o vídeo for na horizontal (padrão: vertical)
 *  bloqueios   períodos já ocupados: ["AAAA-MM-DD", "AAAA-MM-DD"] = entrada e saída
 *              (a noite da saída fica livre para outra reserva)
 */
// creditoCapa: crédito da foto de capa, se a licença pedir (ex.: 'Foto: Fulano / Unsplash')
// api: endereço do servidor de reservas (calendário e datas seguras). Vazio = só mensagem no WhatsApp.
window.THIAGO = {
  whatsapp: '5586998662992',
  instagram: 'https://www.instagram.com/thiago_veras_empreendimentos/',
  api: 'https://163-176-74-32.sslip.io',
};
window.CASAS = [
  {
    id: 'pergolado', codigo: 'C01', nome: 'Casa com pergolado e piscina', cidade: null,
    resumo: 'Jardim gramado, pergolado e piscina, com área coberta para a família toda.',
    destaques: ['Piscina', 'Jardim', 'Pergolado', 'Área coberta'],
    fotos: ['img/casa-pergolado-1.jpg', 'img/casa-pergolado-2.jpg'],
    diaria: null, capacidade: null, quartos: null, minNoites: 1, bloqueios: [],
  },
  {
    id: 'piscina', codigo: 'C02', nome: 'Casa com piscina e área gourmet', cidade: null,
    resumo: 'Varanda ampla, churrasqueira e piscina, com sala espaçosa e rede.',
    destaques: ['Piscina', 'Churrasqueira', 'Área gourmet', 'Varanda'],
    fotos: ['img/casa-piscina-1.jpg', 'img/casa-piscina-2.jpg', 'img/casa-piscina-3.jpg', 'img/casa-piscina-4.jpg'],
    diaria: null, capacidade: null, quartos: null, minNoites: 1, bloqueios: [],
  },
  {
    id: 'amarela', codigo: 'C03', nome: 'Casa amarela', cidade: null,
    resumo: 'Sobrado espaçoso com quintal amplo e área aberta.',
    destaques: ['Sobrado', 'Quintal amplo', 'Área aberta'],
    fotos: ['img/casa-amarela-1.jpg', 'img/casa-amarela-2.jpg'],
    diaria: null, capacidade: null, quartos: null, minNoites: 1, bloqueios: [],
  },
  {
    id: 'garagem', codigo: 'C04', nome: 'Casa com garagem', cidade: null,
    resumo: 'Fachada moderna com garagem coberta.',
    destaques: ['Garagem coberta'],
    fotos: ['img/casa-fachada-1.jpg', 'img/casa-fachada-2.jpg'],
    diaria: null, capacidade: null, quartos: null, minNoites: 1, bloqueios: [],
  },
];
