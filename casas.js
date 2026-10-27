/*
 * Dados das casas e do contato. É só este arquivo que muda para atualizar
 * preços, capacidade e datas ocupadas.
 *
 *  diaria      valor da diária em reais (null = "valor a combinar", sem total)
 *  capacidade  máximo de pessoas (null = sem limite no formulário)
 *  minNoites   mínimo de diárias
 *  video       caminho do vídeo da casa, ex.: 'video/amarela.mp4' (opcional)
 *  poster      imagem de capa do vídeo, ex.: 'video/amarela.jpg' (opcional)
 *  videoHorizontal  true se o vídeo for na horizontal (padrão: vertical)
 *  bloqueios   períodos já ocupados: ["AAAA-MM-DD", "AAAA-MM-DD"] = entrada e saída
 *              (a noite da saída fica livre para outra reserva)
 */
window.THIAGO = { whatsapp: '5586998662992' };
window.CASAS = [
  { id: 'pergolado', nome: 'Casa com pergolado e piscina', diaria: null, capacidade: null, minNoites: 1, bloqueios: [] },
  { id: 'piscina',   nome: 'Casa com piscina e área gourmet', diaria: null, capacidade: null, minNoites: 1, bloqueios: [] },
  { id: 'amarela',   nome: 'Casa amarela', diaria: null, capacidade: null, minNoites: 1, bloqueios: [] },
  { id: 'moderna',   nome: 'Casa moderna', diaria: null, capacidade: null, minNoites: 1, bloqueios: [] },
  { id: 'garagem',   nome: 'Casa com garagem', diaria: null, capacidade: null, minNoites: 1, bloqueios: [] },
];
