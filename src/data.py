"""Dados do site Maxtool — fonte única para HTML, schema.org, llms.txt e JS."""

SITE = 'https://maxtool.com.br'
REMOTE = ''  # PDFs (catálogo, vistas) servidos pelo próprio site: /catalogo/ e /pecas/downloads/

# Google Tag Manager — preencher com o ID do contêiner (ex.: 'GTM-ABC1234').
# Vazio = o snippet não é inserido. GA4, Meta Pixel e Hotjar entram pelo GTM.
GTM_ID = 'GTM-WZNMHZJG'

EMPRESA = {
    'nome': 'Maxtool',
    'razao': 'ITRAC – Comércio, Importação, Exportação e Distribuição LTDA',
    'cnpj': '12.429.225/0001-47',
    'fundacao': '2010',
    'slogan': 'Mais do que uma marca de ferramentas.',
    'rua': 'Av. Paulino Muller, 945 — Jucutuquara',
    'cidade': 'Vitória', 'uf': 'ES', 'cep': '29040-715',
    # coordenada aproximada (nível de rua, OpenStreetMap) — conferir no Google Business Profile
    'lat': -20.3106, 'lng': -40.3207,
    'whatsapp': '+55 27 99201-9026', 'whatsapp_digits': '5527992019026',
    'telefone': '+55 27 3019-3040', 'email': 'comercial@maxtool.com.br',
    'instagram': 'https://www.instagram.com/maxtoolbr/',
    'avaliacoes': 'https://share.google/NqSkrHBz1zOAwQItD',  # Google Meu Negócio (briefing, P33)
    'horario': 'Segunda a sexta, das 8h às 17h',
    'resumo': ('A Maxtool é uma importadora e distribuidora brasileira de ferramentas, abrasivos e máquinas '
               'para marmoraria, com sede em Vitória/ES e atuação desde 2010. Tem mais de 1.000 itens em linha '
               '— discos de corte, serras e lixas diamantadas, polibordas, desbaste, acabamento e máquinas — '
               'em três níveis de performance (Premium, Pro e Std), e vende exclusivamente para mais de 250 '
               'revendas — lojas de ferramentas, distribuidores e lojas de materiais de construção — com entrega '
               'para todo o Brasil.'),
}

MATERIAIS = ['Mármore e Granito', 'Porcelanato', 'Quartzito', 'Nanoglass', 'Ultracompactos', 'Concreto e Granilite']
LINHA_COMPLETA = [
    'Politrizes elétricas', 'Politrizes pneumáticas', 'Serras mármore', 'Esmerilhadeiras',
    'Discos diamantados para corte', 'Discos para granito', 'Discos para mármore', 'Discos para quartzo',
    'Discos para porcelanato', 'Discos para ultracompactos', 'Discos de grande diâmetro', 'Discos silenciosos',
    'Ferramentas diamantadas para polimento', 'Lixas diamantadas', 'Lixas de 3 passos', 'Lixas resinadas',
    'Abrasivos para acabamento e polimento', 'Escovas diamantadas', 'Escovas Tynex', 'Ferramentas HTC',
    'Feltros para polimento', 'Acessórios para politrizes', 'Acessórios para serras', 'Peças de reposição',
    'Trenas', 'Metros de nylon', 'Instrumentos de medição', 'Ferramentas manuais', 'Consumíveis para marmoraria',
    'Acessórios para corte, acabamento e instalação',
]

DIFERENCIAIS = [
    ('Pronta entrega', 'Estoque relevante dos principais produtos, para a revenda não ficar sem.'),
    ('Entrega em todo o Brasil', 'Envio por transportadoras para todo o território nacional.'),
    ('Importação direta', 'Trabalhamos direto com fornecedores internacionais: mais portfólio e melhores condições.'),
    ('Marca própria', 'Identidade própria e linha desenvolvida para a marmoraria — não é revenda de terceiros.'),
    ('Ferramenta por material', 'Soluções específicas para granito, mármore, quartzo, porcelanato e ultracompactos.'),
    ('Peças e pós-venda', 'Peças de reposição e suporte em assistência, garantia e dúvidas de uso.'),
    ('Condições por perfil', 'Pagamento a prazo e condições conforme volume, mix e histórico de compras.'),
    ('Presença no setor', 'Feiras como a de Cachoeiro de Itapemirim, Max Tool Day e profissionais reais testando a linha.'),
]

CATEGORIAS = ['Máquinas', 'Discos de Corte', 'Serras Diamantadas', 'Lixas Diamantadas', 'Polibordas',
              'Brocas Diamantadas', 'Desbaste', 'Acabamento', 'Ferramentas Manuais', 'Acessórios', 'Bases']

NIVEIS = [
    ('Premium', 'Máxima performance para o profissional mais exigente.'),
    ('Pro', 'Equilíbrio entre performance e custo, para uso profissional contínuo.'),
    ('Std', 'Versatilidade e custo-benefício para o dia a dia.'),
]

# Produtos: ver src/catalogo.py (catálogo 2026 completo, com imagens e materiais).

ETAPAS = [
    dict(nome='Corte', txt='Corte reto e limpo, sem lascar — do granito ao porcelanato, do quartzito ao ultracompacto.',
         cats=['Máquinas', 'Discos de Corte', 'Serras Diamantadas', 'Brocas Diamantadas']),
    dict(nome='Desbaste', txt='Remover material, nivelar e dar forma à borda e à superfície com rapidez.',
         cats=['Desbaste', 'Bases', 'Máquinas']),
    dict(nome='Polimento', txt='Do grão grosso ao brilho: lixas diamantadas e polibordas para cada material.',
         cats=['Lixas Diamantadas SL · SLX · SLe · SLXe', 'Polibordas', 'Politrizes']),
    dict(nome='Acabamento', txt='Texturas, detalhes e o toque final que valoriza a peça entregue.',
         cats=['Acabamento', 'Ferramentas Manuais', 'Acessórios']),
]

REELS = [
    ('maxtool-day.jpg', 'https://www.instagram.com/maxtoolbr/reel/DaliFyXlNSO/', 'Max Tool Day: a 1ª edição entrou para a história'),
    ('historia.jpg', 'https://www.instagram.com/maxtoolbr/reel/DPgkmLGjuRd/', 'Nossa história: mais de 250 distribuidores pelo Brasil'),
    ('milgrau.jpg', 'https://www.instagram.com/marmorista_milgrau/reel/DRFCgdPjb8e/', 'Na obra com o parceiro @marmorista_milgrau'),
    ('entrega.jpg', 'https://www.instagram.com/maxtoolbr/reel/DLKsXiHMiCw/', 'Entrega rápida, compromisso levado a sério'),
    ('almeida.jpg', 'https://www.instagram.com/almeidamarmorista/reel/DaVugcpJObv/', 'Ferramenta em ação com @almeidamarmorista'),
    ('stone-fair.jpg', 'https://www.instagram.com/maxtoolbr/reel/C_MffjHIZUN/', 'Maxtool na Cachoeiro Stone Fair'),
    ('parcerias.jpg', 'https://www.instagram.com/maxtoolbr/reel/DLYNjcSscvW/', 'Mais do que vender ferramentas: construímos parcerias'),
    ('bastidores.jpg', 'https://www.instagram.com/maxtoolbr/reel/DNqST5OMxLH/', 'Bastidores: antes da ferramenta girar, tem gente pensando no seu resultado'),
]

# ---------- Perguntas frequentes (visíveis na página + FAQPage) ----------
F_DIRETO = ('A Maxtool vende direto para o consumidor?',
            'Não. A Maxtool vende exclusivamente para revendas. O marmorista compra na loja parceira mais próxima — use o localizador por CEP na página Onde comprar ou fale com a Maxtool pelo WhatsApp +55 27 99201-9026, que indica onde comprar.')
F_REVENDA = ('Como me torno revendedor Maxtool?',
             'Preencha o cadastro na página Seja um revendedor ou chame a equipe comercial no WhatsApp, informando os dados da empresa e o CNPJ. A Maxtool atende revendas especializadas, distribuidores regionais, lojas de ferramentas e lojas de materiais de construção que vendem para marmoraria. Após o cadastro, a equipe apresenta o portfólio e as condições comerciais.')
F_NIVEIS = ('Qual a diferença entre as linhas Premium, Pro e Std?',
            'São três níveis de performance. Premium entrega o máximo para o profissional mais exigente; Pro equilibra performance e custo para uso profissional contínuo; Std traz versatilidade e custo-benefício para o dia a dia.')
F_GARANTIA = ('Como acionar a garantia de uma máquina Maxtool?',
              'Toda máquina Maxtool tem garantia contra defeitos de fabricação (não cobre mau uso, desgaste natural, aplicação incorreta ou uso fora das recomendações do produto). Fale primeiro com a Maxtool pelo WhatsApp, com a nota fiscal em mãos. Você pode levar a máquina a uma oficina perto de você — se for defeito de fabricação, a Maxtool envia a peça sem custo e paga a mão de obra — ou enviar a máquina direto para a Maxtool.')
F_PECAS = ('Onde encontro peças de reposição das máquinas Maxtool?',
           'Na página Peças & Assistência há a vista explodida e a lista de peças da Serra Mármore SM-MT-023, das Politrizes MT-023, MT-01 e PP-MT-023 e da Esmerilhadeira EA-MT-025, com PDF para download. Para pedir a peça, informe o número da lista à Maxtool.')
MTDAY = dict(data='2026-11-13', data_br='13 de novembro de 2026', data_curta='13/11/2026',
             local='BSB Abrasivos', cidade='Vicente Pires', uf='DF')
F_MTDAY_INGRESSO = ('Como funciona o ingresso do Max Tool Day?',
                    'O valor do ingresso volta para o participante como voucher de compra na loja que recebe o evento.')
F_MTDAY = ('O que é o Max Tool Day?',
           'É o evento presencial de capacitação para marmoristas que a Maxtool faz dentro das revendas parceiras: demonstração ao vivo de corte, desbaste e polimento, técnica na prática e contato direto com o time Maxtool. A próxima edição é em 13 de novembro de 2026, na BSB Abrasivos, em Vicente Pires-DF.')
F_ONDE = ('Onde fica a Maxtool?',
          'A sede da Maxtool fica na Av. Paulino Muller, 945 — Jucutuquara, Vitória - ES, CEP 29040-715. A empresa atende revendas de todo o Brasil.')
F_CATALOGO = ('Onde vejo o catálogo completo da Maxtool?',
              'O catálogo 2026, com mais de 1.000 itens organizados por categoria e nível, pode ser baixado em PDF nas páginas Produtos e Seja um revendedor.')
F_PORCELANATO = ('Qual disco Maxtool usar para cortar porcelanato?',
    'Para porcelanato, a Maxtool tem o Disco de Corte Mesh Premium (75, 110 e 115 mm), com borda que corta sem lascar, o Disco Turbo Extra Fino Pro e o Disco Multipropósito Std. Na serra de bancada, as serras diamantadas Porcelanato e Mesh (250 a 350 mm); para furos, a broca diamantada para porcelanato (6 a 70 mm).')
F_ULTRA = ('Qual disco usar para ultracompactos?',
    'Para ultracompactos, a Maxtool tem o Disco de Corte Ultracompactos Premium (120 mm), as serras diamantadas Ultracompactos Premium (250 a 350 mm) e Pro (350 mm) e a broca diamantada para Dekton (10 a 70 mm).')
F_QUARTZITO = ('Qual serra usar para quartzito?',
    'Para quartzito, a Maxtool tem a Serra Diamantada Quartzito Premium (250, 300 e 350 mm, segmento de 20 mm). O catálogo também indica para quartzito a Serra Ultracompactos e a Serra Turbo Protegida Premium.')
F_MATERIAIS = ('Para quais materiais são as ferramentas Maxtool?',
               'Mármore e granito, porcelanato, quartzito, nanoglass, ultracompactos, concreto e granilite.')
F_MTDAY_LOJA = ('Como levar o Max Tool Day para a minha loja?',
                'Se você já é revendedor Maxtool, fale com a equipe pelo WhatsApp +55 27 99201-9026 para receber o evento na sua loja. Se ainda não é, comece pelo cadastro de revenda.')
F_SEM_LOJA = ('Não tem revenda Maxtool na minha cidade. E agora?',
              'Chame a Maxtool no WhatsApp +55 27 99201-9026: a equipe indica a revenda mais próxima. Você também pode indicar a loja onde já compra para que a Maxtool tente levar a marca até lá.')
F_OFICINA = ('Minha oficina pode ser parceira da Maxtool?',
             'Sim. Oficinas que consertam máquinas podem se cadastrar como oficina parceira na página Peças & Assistência e passam a receber indicações de marmoristas da região e as diretrizes técnicas e de garantia.')
F_PEDIDO = ('Qual é o pedido mínimo?',
            'O pedido mínimo varia conforme a negociação, o perfil do cliente, a região e as condições comerciais. A equipe comercial orienta cada revenda de acordo com a sua necessidade.')
F_DESDE = ('Desde quando a Maxtool existe?',
           'A Maxtool nasceu em 2010, em Vitória/ES, com 5 produtos. Hoje tem mais de 1.000 itens em linha e mais de 250 revendas parceiras.')
F_CONTATO = ('Como falar com a Maxtool?',
             'Pelo WhatsApp +55 27 99201-9026 (resposta mais rápida), pelo e-mail comercial@maxtool.com.br, pelo telefone (27) 3019-3040 ou pelo Instagram @maxtoolbr. O atendimento é de segunda a sexta, das 8h às 17h.')

F_ENTREGA = ('A Maxtool entrega para todo o Brasil?',
             'Sim. A Maxtool atende revendas em todo o território nacional por meio de transportadoras e demais modalidades de envio disponíveis para cada região.')
F_PRAZO = ('Qual o prazo de entrega?',
           'Varia conforme a cidade, o volume do pedido e a transportadora. No orçamento, a equipe informa as opções e a previsão de entrega.')
F_PRONTA = ('A Maxtool tem pronta entrega?',
            'Sim. Grande parte dos principais produtos tem estoque para pronta entrega. Alguns lançamentos ou itens específicos podem depender de disponibilidade.')
F_PAGAMENTO = ('Vocês trabalham com pagamento a prazo?',
               'Sim. As condições de pagamento variam conforme análise cadastral, histórico de compras e valor do pedido.')
F_TABELA = ('Vocês enviam catálogo e tabela de preços?',
            'O catálogo 2026 está disponível para download no site. A tabela de preços e as condições comerciais são enviadas pela equipe comercial após o cadastro da revenda.')
F_VOLUME = ('Vocês fazem preço especial para revenda ou volume?',
            'Sim. As condições podem ser diferenciadas conforme volume, mix de produtos, histórico de compras e perfil da revenda.')
F_MAQUINA = ('O disco ou a lixa serve em qualquer máquina?',
             'Não necessariamente. Cada produto tem especificação de rotação, diâmetro, encaixe ou tipo de equipamento. Confirme sempre a compatibilidade antes de usar — a equipe Maxtool ajuda a conferir.')
F_LIXA = ('Qual lixa usar para polir granito ou porcelanato?',
          'Depende do material, da etapa do polimento e do acabamento desejado. A Maxtool tem lixas diamantadas, lixas de 3 passos e lixas resinadas em diferentes granulometrias, e a equipe orienta a sequência certa para cada aplicação.')
F_COMPARAR = ('Como escolher entre dois produtos parecidos?',
              'A equipe comercial indica a opção de melhor resultado conforme o material, o tipo de uso, a frequência de trabalho e o custo-benefício desejado.')
F_DISCO_MATERIAL = ('Qual disco diamantado usar para cada material?',
                    'Depende do material e da aplicação. A Maxtool tem discos específicos para granito, mármore, quartzo, porcelanato, ultracompactos e outras superfícies — veja o guia A ferramenta certa para cada material, nas páginas Produtos.')

FAQS = {
    'home': [F_DIRETO, F_REVENDA, F_ENTREGA, F_DISCO_MATERIAL, F_NIVEIS, F_GARANTIA, F_MTDAY],
    'produtos': [F_DISCO_MATERIAL, F_PORCELANATO, F_ULTRA, F_QUARTZITO, F_LIXA, F_MAQUINA, F_NIVEIS, F_COMPARAR, F_CATALOGO, F_DIRETO],
    'sobre': [F_DESDE, F_ONDE, F_DIRETO, F_ENTREGA, F_REVENDA],
    'pecas': [F_GARANTIA, F_PECAS, F_MAQUINA, F_OFICINA],
    'mtday': [F_MTDAY, F_MTDAY_INGRESSO, F_MTDAY_LOJA],
    'onde': [F_DIRETO, F_SEM_LOJA, F_REVENDA],
    'revenda': [F_REVENDA, F_PEDIDO, F_PAGAMENTO, F_VOLUME, F_ENTREGA, F_PRAZO, F_PRONTA, F_TABELA, F_NIVEIS, F_MTDAY_LOJA, F_DIRETO],
    'contato': [F_CONTATO, F_ONDE, F_DIRETO, F_ENTREGA, F_GARANTIA, F_REVENDA],
}

# ---------- Guia "A ferramenta certa para cada material" (briefing, P30 — tema obrigatório) ----------
# Itens com id de produto viram card clicável; textos são categorias da linha (briefing, P09).
# Só associamos produto a material quando a especificação do produto confirma.
GUIA_MATERIAIS = [
    dict(id='marmore-granito', nome='Mármore e Granito', picto='px-marmore',
         desafio='Os materiais mais trabalhados da marmoraria: corte reto na bancada, borda bem acabada e brilho uniforme.',
         etapas=[('Corte', ['serra-marmore', 'Discos para granito', 'Discos para mármore', 'Discos silenciosos', 'Discos de grande diâmetro']),
                 ('Desbaste', ['prato-desbaste']),
                 ('Polimento', ['Lixas diamantadas', 'Lixas resinadas', 'Feltros para polimento', 'Politrizes elétricas e pneumáticas']),
                 ('Acabamento', ['escova-tynex', 'Escovas diamantadas'])]),
    dict(id='porcelanato', nome='Porcelanato', picto='px-porcelanato',
         desafio='Material duro e quebradiço, cada vez em formatos maiores. O maior medo é lascar a borda no corte.',
         etapas=[('Corte', ['disco-mesh', 'Discos para porcelanato']),
                 ('Furo', ['Brocas e coroas diamantadas']),
                 ('Polimento', ['Lixas diamantadas', 'Lixas de 3 passos'])]),
    dict(id='quartzito', nome='Quartzito', picto='px-quartzito',
         desafio='Um dos materiais mais duros e abrasivos: consome ferramenta rápido e exige segmento resistente.',
         etapas=[('Corte', ['serra-quartzito', 'Discos silenciosos']),
                 ('Polimento', ['Lixas diamantadas', 'Ferramentas diamantadas para polimento'])]),
    dict(id='nanoglass', nome='Nanoglass', picto='px-nanoglass',
         desafio='Superfície vitrificada e sensível: pede corte controlado e polimento cuidadoso para não marcar.',
         etapas=[('Corte', ['Discos diamantados para corte']),
                 ('Polimento', ['Lixas diamantadas', 'Feltros para polimento'])]),
    dict(id='ultracompactos', nome='Ultracompactos', picto='px-ultracompactos',
         desafio='Chapas densas e de alto valor: um erro no corte custa a peça inteira.',
         etapas=[('Corte', ['disco-ultracompacto', 'Discos para ultracompactos']),
                 ('Furo', ['Brocas e coroas diamantadas']),
                 ('Polimento', ['Lixas diamantadas'])]),
    dict(id='concreto-granilite', nome='Concreto e Granilite', picto='px-concreto',
         desafio='Superfícies de piso e bancada que pedem desbaste forte antes do acabamento.',
         etapas=[('Desbaste', ['prato-desbaste', 'Ferramentas HTC']),
                 ('Polimento', ['Ferramentas diamantadas para polimento', 'Lixas resinadas'])]),
]

ERROS_COMUNS = [
    ('Disco errado para o material', 'Resultado: peça lascada e ferramenta perdida. Use o disco indicado para o material que vai cortar.'),
    ('Pular grão na sequência de lixas', 'Os riscos do grão anterior aparecem no brilho. Siga a sequência do mais grosso ao mais fino.'),
    ('Ferramenta incompatível com a máquina', 'Confira rotação máxima, diâmetro e encaixe antes de montar o disco ou a lixa.'),
    ('Trabalhar sem EPI', 'Óculos, protetor auricular e máscara contra poeira de sílica em todo corte, desbaste e polimento.'),
]
