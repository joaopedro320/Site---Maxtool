"""Produtos do Catálogo Maxtool 2026 — fonte: catalogo/maxtool-catalogo-2026.pdf.

Materiais (ícones do catálogo): mg = Mármore e Granito · por = Porcelanato · qtz = Quartzito ·
nano = Nanoglass · ult = Ultracompactos · conc = Concreto e Granilite.
Imagens em assets/catalogo/<id>.avif (+ .png de reserva), recortadas das páginas do catálogo.
"""

MAT = {'mg': 'Mármore e Granito', 'por': 'Porcelanato', 'qtz': 'Quartzito', 'nano': 'Nanoglass',
       'ult': 'Ultracompactos', 'conc': 'Concreto e Granilite'}
TODOS = ['mg', 'por', 'qtz', 'nano', 'ult', 'conc']

# dimensões (px) das imagens exportadas
DIMS = {}


def _p(id, nome, cat, etapa, mats, specs, nivel=None, linha=None, destaque=False, disc=False, nota='',
       img=None, pagina=None):
    return dict(id=id, nome=nome, cat=cat, etapa=etapa, mats=mats, specs=specs, nivel=nivel, linha=linha,
                destaque=destaque, disc=disc, nota=nota, img=img, pagina=pagina)


def corte(id, nome, nivel, mats, diam, furo, seg, esp, cat='Discos de Corte', **kw):
    return _p(id, nome, cat, 0, mats, [['Diâmetro', diam], ['Furo central', furo], ['Altura do segmento', seg],
                                       ['Espessura', esp]], nivel=nivel, disc=True, **kw)


def lixa(id, nome, nivel, mats, diam, polimento, esp, graos, linha=None, cat='Lixas Diamantadas', **kw):
    specs = [['Diâmetro', diam], ['Polimento', polimento], ['Espessura', esp], ['Grãos', graos]]
    return _p(id, nome, cat, 2, mats, specs, nivel=nivel, linha=linha, **kw)


PRODUTOS = [
    # ---------------- Discos de corte · Premium (pág. 6–7) ----------------
    corte('disco-premium-continuo', 'Disco de Corte Contínuo', 'Premium', ['nano', 'mg'], '110 / 115 mm', '20 mm', '10 mm', '2,0 mm', pagina=6),
    corte('disco-premium-turbo-protegido', 'Disco de Corte Turbo Protegido', 'Premium', ['mg'], '115 mm', '20 mm', '8 mm', '2,4 mm', pagina=6),
    corte('disco-premium-curvo', 'Disco de Corte Curvo', 'Premium', ['mg'], '115 mm', '20 mm', '10 mm', '2,2 mm', pagina=6),
    corte('disco-premium-turbo-protegido-curvo', 'Disco de Corte Turbo Protegido Curvo', 'Premium', ['mg'], '125 mm', '20 mm', '7 mm', '2,8 mm', pagina=6),
    corte('disco-premium-turbo-narrow', 'Disco de Corte Turbo Narrow', 'Premium', ['mg'], '110 / 115 / 125 mm', '20 mm', '10 mm', '2,0 mm (110) · 2,4 mm (115) · 2,2 mm (125)', pagina=6),
    corte('disco-premium-mesh', 'Disco de Corte Mesh', 'Premium', ['por'], '75 / 110 / 115 mm', '8 mm (75) · 20 mm', '10 mm', '1,4 mm (75) · 1,2 mm (110) · 1,4 mm (115)',
          destaque=True, nota='Borda mesh para corte fino em porcelanato, sem lascar a peça.', pagina=6),
    corte('disco-premium-ultra-turbo', 'Disco de Corte Ultra Turbo', 'Premium', ['mg'], '115 mm', '20 mm', '15 mm', '2,2 mm', pagina=6),
    corte('disco-premium-ultracompactos', 'Disco de Corte Ultracompactos', 'Premium', ['ult'], '120 mm', '20 mm', '11 mm', '1,8 mm',
          destaque=True, nota='Feito para chapas densas de ultracompacto, que pedem corte preciso e controlado.', pagina=7),
    corte('disco-premium-segmentado', 'Disco de Corte Segmentado', 'Premium', ['mg'], '110 / 115 mm', '20 mm', '10 mm', '2,0 mm', pagina=7),
    # ---------------- Serras · Premium (pág. 8) ----------------
    corte('serra-premium-porcelanato', 'Serra Diamantada Porcelanato', 'Premium', ['por'], '250 / 300 / 350 mm', '50 mm', '10 mm', '2,2 / 2,4 / 2,6 mm', cat='Serras Diamantadas', pagina=8),
    corte('serra-premium-ultracompactos', 'Serra Diamantada Ultracompactos', 'Premium', ['qtz', 'ult'], '250 / 300 / 350 mm', '60 – 50 mm', '8 mm (250) · 10 mm', '2,2 / 2,6 / 3,2 mm', cat='Serras Diamantadas', pagina=8),
    corte('serra-premium-mesh', 'Serra Diamantada Mesh', 'Premium', ['por'], '250 / 300 / 350 mm', '50 mm', '10 mm', '2,0 / 2,2 / 2,4 mm', cat='Serras Diamantadas', pagina=8),
    corte('serra-premium-quartzito', 'Serra Diamantada Quartzito', 'Premium', ['qtz'], '250 / 300 / 350 mm', '50 mm', '20 mm', '3,2 mm', cat='Serras Diamantadas',
          destaque=True, nota='Segmento alto (20 mm) para o corte de quartzito, material duro e abrasivo.', pagina=8),
    corte('serra-premium-nanoglass', 'Serra Diamantada Nanoglass', 'Premium', ['nano', 'ult'], '250 / 300 / 350 mm', '50 mm', '10 mm', '2,0 / 2,2 / 2,6 mm', cat='Serras Diamantadas', pagina=8),
    corte('serra-premium-turbo-protegida', 'Serra Diamantada Turbo Protegida', 'Premium', ['qtz'], '180 / 230 mm', '25,4 mm', '8 mm', '2,8 mm', cat='Serras Diamantadas', pagina=8),
    corte('serra-premium-tree-step', 'Serra Diamantada Tree-Step', 'Premium', ['mg'], '250 / 350 mm', '50 mm', '15 mm', '3,6 mm', cat='Serras Diamantadas', destaque=True, pagina=8),
    # ---------------- Discos e serras · Pro (pág. 10–11) ----------------
    corte('disco-pro-continuo', 'Disco de Corte Contínuo', 'Pro', ['nano', 'mg'], '110 / 115 mm', '20 mm', '10 mm', '1,2 / 1,3 mm', pagina=10),
    corte('disco-pro-protegido', 'Disco de Corte Protegido', 'Pro', ['mg'], '115 mm', '20 mm', '8 mm', '2,4 mm', pagina=10),
    corte('disco-pro-turbo', 'Disco de Corte Turbo', 'Pro', ['mg'], '110 / 115 mm', '20 mm', '10 mm', '2,0 / 2,2 mm', destaque=True, pagina=10),
    corte('disco-pro-turbo-narrow', 'Disco de Corte Turbo Narrow', 'Pro', ['mg'], '110 / 115 mm', '20 mm', '10 mm', '1,8 / 2,0 mm', pagina=10),
    corte('disco-pro-turbo-extra-fino', 'Disco de Corte Turbo Extra Fino', 'Pro', ['mg', 'por'], '110 / 115 / 125 mm', '20 mm', '8 / 10 mm', '1,4 / 1,6 mm', pagina=10),
    corte('serra-pro-silenciosa', 'Serra Diamantada Silenciosa', 'Pro', ['mg'], '350 mm', '50 mm', '15 mm', '3,2 mm', cat='Serras Diamantadas', pagina=11),
    corte('serra-pro-silenciosa-tree-step', 'Serra Diamantada Silenciosa Tree-Step', 'Pro', ['mg'], '250 / 350 mm', '50 mm', '15 mm', '3,6 mm', cat='Serras Diamantadas', pagina=11),
    corte('serra-pro-ultracompacto', 'Serra Diamantada Ultracompacto', 'Pro', ['ult'], '350 mm', '50 mm', '10 mm', '2,9 mm', cat='Serras Diamantadas', pagina=11),
    corte('serra-pro-concreto-granilite', 'Serra Diamantada Concreto e Granilite', 'Pro', ['conc'], '300 mm', '25,4 mm', '12 mm', '3,2 mm', cat='Serras Diamantadas', pagina=11),
    # ---------------- Discos e serras · Std (pág. 12) ----------------
    corte('disco-std-continuo', 'Disco de Corte Contínuo', 'Std', ['nano', 'mg'], '110 mm', '20 mm', '8 mm', '2,0 mm', pagina=12),
    corte('disco-std-segmentado', 'Disco de Corte Segmentado', 'Std', ['mg'], '110 mm', '20 mm', '8 mm', '2,0 mm', pagina=12),
    corte('disco-std-turbo', 'Disco de Corte Turbo', 'Std', ['mg'], '110 mm', '20 mm', '8 mm', '2,0 mm', pagina=12),
    corte('disco-std-multiproposito', 'Disco de Corte Multipropósito', 'Std', ['por'], '100 / 115 mm', '22,23 mm', '10 mm', '1,5 / 1,8 mm', pagina=12),
    corte('serra-std-diamantada', 'Serra Diamantada', 'Std', ['mg'], '350 mm', '50 mm', '15 mm', '3,2 mm', cat='Serras Diamantadas', pagina=12),
    # ---------------- Máquinas (pág. 5, 15–17) ----------------
    _p('serra-marmore', 'Serra Mármore SM-MT-023', 'Máquinas', 0, ['mg'],
       [['Modelo', 'SM-MT-023'], ['Rotação máx.', '12.000 rpm'], ['Potência', '1.550 W'], ['Frequência', '50/60 Hz'], ['Disco', 'Ø110 mm'], ['Peso', '2,9 kg']],
       destaque=True, img='/assets/produtos/serra-marmore.webp', nota='Corte preciso e limpo em mármore e outras pedras, com vista explodida e peças de reposição no site.', pagina=5),
    _p('maquina-esmerilhadeira-ea-mt-025', 'Esmerilhadeira Angular EA-MT-025', 'Máquinas', 0, ['mg', 'conc'],
       [['Modelo', 'EA-MT-025'], ['Rotação máx.', '11.000 rpm'], ['Potência', '900 W'], ['Frequência', '50/60 Hz'], ['Disco', 'Ø125 mm'], ['Peso', '1,8 kg']],
       nota='Para corte, desbaste e acabamento em pedras, concreto e metais, com empunhadura auxiliar.', pagina=15),
    _p('maquina-politriz-mt-01', 'Politriz Elétrica Úmido MT-01', 'Máquinas', 2, ['mg'],
       [['Modelo', 'MT-01'], ['Rotação máx.', '6.000 rpm'], ['Potência', '1.200 W'], ['Frequência', '50/60 Hz'], ['Diâmetro', '100 a 180 mm'], ['Peso', '3,2 kg']], pagina=15),
    _p('maquina-politriz-mt-023', 'Politriz Elétrica Úmido MT-023', 'Máquinas', 2, ['mg'],
       [['Modelo', 'MT-023'], ['Rotação máx.', '8.500 rpm'], ['Potência', '1.400 W'], ['Frequência', '50/60 Hz'], ['Diâmetro', '100 a 180 mm'], ['Peso', '2,9 kg']],
       destaque=True, nota='Polimento a úmido em mármore e granito, com controle suave e brilho uniforme.', pagina=17),
    _p('maquina-politriz-pneumatica-pp-mt-023', 'Politriz Pneumática PP-MT-023', 'Máquinas', 2, ['mg'],
       [['Modelo', 'PP-MT-023'], ['Rotação máx.', '10.000 rpm'], ['Consumo de ar', '14 PCM'], ['Pressão', '90 PSI'], ['Peso', '2,6 kg']],
       nota='Alimentada a ar: leve, com menor aquecimento, para acabamentos finos em uso contínuo.', pagina=17),
    _p('maquina-politriz-vertical-pv-mt-025', 'Politriz Vertical PV-MT-025', 'Máquinas', 2, ['mg'],
       [['Modelo', 'PV-MT-025'], ['Rotação máx.', '4.500 rpm'], ['Potência', '710 W'], ['Frequência', '50/60 Hz'], ['Diâmetro', '150 mm'], ['Peso', '2,9 kg']],
       nota='Para polimento de grandes superfícies e trabalhos pesados.', pagina=17),
    # ---------------- Lixas · SLX / SL (pág. 18) ----------------
    lixa('lixa-slx-polimento', 'Lixa Diamantada SLX para Polimento', None, TODOS, '100 mm (4") / 125 mm (5")', 'seco ou úmido', '2,5 mm', '#50 a #3000', linha='SLX', destaque=True, pagina=18),
    lixa('lixa-sl-piso', 'Lixa Diamantada SL para Piso', None, ['mg'], '80 mm (3")', 'úmido', '10 mm', '#50 a #3000', linha='SL', pagina=18),
    lixa('lixa-sl-polimento', 'Lixa Diamantada SL para Polimento', None, ['mg', 'conc'], '100 mm (4") / 125 mm (5")', 'úmido', '2,5 mm', '#50 a #3000', linha='SL', pagina=18),
    lixa('lixa-sl-concreto', 'Lixa Diamantada SL para Concreto', None, ['conc'], '80 mm (3")', 'úmido', '10 mm', '#50 a #3000', linha='SL', pagina=18),
    # ---------------- Lixas · Premium (pág. 19–20) ----------------
    lixa('lixa-premium-3-passos', 'Lixa Diamantada 3 Passos', 'Premium', ['mg'], '100 mm (4")', 'seco ou úmido', '3 mm', '#1 #2 #3', destaque=True,
         nota='Polimento em 3 passos: menos trocas de lixa até o brilho.', pagina=19),
    lixa('lixa-premium-cfi', 'Lixa Diamantada CFI', 'Premium', ['conc'], '100 mm (4")', 'seco ou úmido', '6 mm', '#30 a #3000', pagina=19),
    lixa('lixa-premium-esponja', 'Lixa Esponja', 'Premium', ['mg', 'qtz', 'por'], '100 mm (4")', 'úmido', '12 mm', '#150 a #10000', pagina=19),
    lixa('lixa-premium-colmeia', 'Lixa Diamantada Colmeia', 'Premium', ['mg', 'nano', 'por'], '100 mm (4")', 'seco', '2 mm', '#50 a #3000', pagina=19),
    lixa('lixa-premium-concreto', 'Lixa Diamantada para Concreto', 'Premium', ['mg', 'conc'], '240 mm', 'úmido', '10 mm', '#50 a #3000', pagina=19),
    lixa('lixa-premium-5-passos', 'Lixa Diamantada 5 Passos', 'Premium', ['mg'], '100 mm (4")', 'seco ou úmido', '3 mm', '#1 a #5', pagina=19),
    _p('lixa-premium-barril', 'Barril de Polimento e Refil', 'Lixas Diamantadas', 2, ['mg'],
       [['Diâmetro', '25 / 50 mm'], ['Polimento', 'úmido'], ['Encaixe', 'M14'], ['Grãos', '#50 a #3000']], nivel='Premium', pagina=19),
    lixa('lixa-premium-super-floor', 'Lixa Diamantada Super Floor', 'Premium', ['mg', 'conc'], '100 mm (4")', 'úmido', '8 mm', '#30 a #3000', pagina=20),
    lixa('lixa-premium-rebaixo-italiano', 'Lixa Diamantada para Rebaixo Italiano', 'Premium', ['mg'], '100 mm (4")', 'úmido', '3 mm', '#50 a #3000', pagina=20),
    lixa('lixa-premium-buff', 'Lixa Diamantada Buff', 'Premium', ['mg'], '100 mm (4")', 'úmido', '2,7 mm', 'buff', pagina=20),
    lixa('lixa-premium-buff-colmeia', 'Lixa Diamantada Buff Colmeia', 'Premium', ['mg'], '100 mm (4")', 'seco', '2,0 mm', 'buff', pagina=20),
    lixa('lixa-premium-turbo', 'Lixa Diamantada Turbo', 'Premium', ['mg', 'conc'], '100 mm (4")', 'úmido', '3 mm', '#30 a #3000', pagina=20),
    lixa('lixa-premium-convexa', 'Lixa Diamantada Convexa', 'Premium', ['mg'], '100 mm (4")', 'úmido', '2,5 mm', '#50 a #3000', pagina=20),
    # ---------------- Lixas · Pro e Std (pág. 21) ----------------
    lixa('lixa-sle-polimento', 'Lixa Diamantada SLe para Polimento', 'Pro', ['mg'], '100 mm (4")', 'úmido', '2,5 mm', '#50 a #3000', linha='SLe', pagina=21),
    lixa('lixa-pro-3-passos', 'Lixa Diamantada 3 Passos', 'Pro', ['mg'], '100 mm (4")', 'seco ou úmido', '3 mm', '#1 #2 #3', pagina=21),
    lixa('lixa-slxe-polimento', 'Lixa Diamantada SLXe para Polimento', 'Pro', TODOS, '100 mm (4")', 'seco ou úmido', '2,5 mm', '#50 a #3000', linha='SLXe', pagina=21),
    lixa('lixa-std-espiral', 'Lixa Diamantada Espiral', 'Std', ['mg'], '100 mm (4")', 'úmido', '2,5 mm', '#50 a #3000', pagina=21),
    lixa('lixa-std-diamantada', 'Lixa Diamantada', 'Std', ['mg'], '100 mm (4") / 125 mm (5")', 'úmido', '2,5 mm', '#50 a #3000 · fundo branco ou colorido', pagina=21),
    # ---------------- Polibordas (pág. 22) ----------------
    lixa('poliborda-branco-face', 'Poliborda Branco (Face)', None, ['nano', 'mg'], '125 mm (5") / 150 mm (6")', 'úmido', '11 mm', '#50 a #3000', cat='Polibordas', pagina=22),
    lixa('poliborda-branco-bisote', 'Poliborda Branco (Bisote)', None, ['nano', 'mg'], '125 mm (5")', 'úmido', '7 mm', '#200 a #3000', cat='Polibordas', pagina=22),
    lixa('poliborda-red-face', 'Poliborda Red (Face)', None, ['nano', 'mg'], '125 mm (5")', 'úmido', '13 mm', '#50 a #3000', cat='Polibordas', pagina=22),
    lixa('poliborda-red-bisote', 'Poliborda Red (Bisote)', None, ['nano', 'mg'], '125 mm (5")', 'úmido', '14,5 mm', '#200 a #3000', cat='Polibordas', pagina=22),
    # ---------------- Brocas (pág. 23) ----------------
    _p('broca-marmore-granito', 'Broca Diamantada para Mármore e Granito', 'Brocas Diamantadas', 0, ['mg'],
       [['Encaixe', 'duplo encaixe / M14 (dispensa adaptadores)'], ['Diâmetros', '6 a 150 mm']], pagina=23),
    _p('broca-marmore-granito-escareador', 'Broca para Mármore e Granito com Escareador', 'Brocas Diamantadas', 0, ['mg'],
       [['Encaixe', 'duplo encaixe / M14'], ['Furo', '32 mm'], ['Rebaixo', '62 mm']], pagina=23),
    _p('broca-dekton', 'Broca Diamantada para Dekton (ultracompactos)', 'Brocas Diamantadas', 0, ['ult'],
       [['Encaixe', 'duplo encaixe / M14 (dispensa adaptadores)'], ['Diâmetros', '10 a 70 mm']], pagina=23),
    _p('broca-porcelanato', 'Broca Diamantada para Porcelanato', 'Brocas Diamantadas', 0, ['por'],
       [['Encaixe', 'duplo encaixe / M14 (dispensa adaptadores)'], ['Diâmetros', '6 a 70 mm']], destaque=True, pagina=23),
    _p('broca-nanoglass', 'Broca Diamantada para Nanoglass', 'Brocas Diamantadas', 0, ['nano'],
       [['Encaixe', 'duplo encaixe / M14 (dispensa adaptadores)'], ['Diâmetros', '6 a 40 mm']], pagina=23),
    _p('broca-haste-multiproposito', 'Broca Haste Multipropósito', 'Brocas Diamantadas', 0, TODOS,
       [['Diâmetros', '5 / 6 / 8 / 10 / 12 mm']], pagina=23),
    _p('broca-conica-chanfro', 'Broca Cônica Multipropósito para Chanfro', 'Brocas Diamantadas', 0, ['mg'],
       [['Encaixe', 'M14'], ['Medida', '38 × 45 mm']], pagina=23),
    _p('broca-conica-multiproposito', 'Broca Cônica Multipropósito', 'Brocas Diamantadas', 0, ['mg'],
       [['Encaixe', 'M14'], ['Medida', '35 mm']], pagina=23),
    # ---------------- Acabamento (pág. 24) ----------------
    _p('htc-husqvarna', 'HTC Husqvarna', 'Acabamento', 3, ['conc'], [['Medida', '50 × 55 × 75 mm'], ['Grãos', '#16 a #400']], pagina=24),
    _p('htc-soft', 'HTC Soft', 'Acabamento', 3, ['mg', 'conc'], [['Medida', '50 × 50 × 70 mm'], ['Grãos', '#30 #60 #120']], pagina=24),
    _p('htc-lvs', 'HTC LVS', 'Acabamento', 3, ['conc'], [['Medida', '73 × 69 × 55 mm'], ['Grãos', '#16 a #220']], pagina=24),
    _p('prato-diamantado-velcro', 'Prato Diamantado com Velcro', 'Acabamento', 3, ['mg', 'conc'],
       [['Diâmetro', '100 mm (4")'], ['Material', 'ferro com velcro'], ['Grãos', '#16 a #220']], pagina=24),
    _p('escova-tynex-m14-diamantada', 'Escova Tynex M14 Diamantada', 'Acabamento', 3, ['mg', 'conc'],
       [['Diâmetro', '110 mm'], ['Encaixe', 'M14 / caracol'], ['Rotação', '1.500 a 3.000 rpm'], ['Cerdas', 'diamante sintético e nylon'], ['Grãos', '#24 a #1200']],
       destaque=True, nota='Texturiza e dá acabamento escovado ou envelhecido à superfície da pedra.', pagina=24),
    _p('escova-tynex-frankfurt-diamantada', 'Escova Tynex Frankfurt Diamantada', 'Acabamento', 3, ['mg', 'conc'],
       [['Encaixe', 'frankfurt'], ['Rotação', '500 rpm'], ['Cerdas', 'diamante sintético e nylon'], ['Grãos', '#24 a #120']], pagina=24),
    _p('escova-tynex-m14-carbeto', 'Escova Tynex M14 Carbeto', 'Acabamento', 3, ['mg', 'conc'],
       [['Diâmetro', '110 mm (4") / 125 mm (5")'], ['Encaixe', 'M14 / caracol'], ['Rotação', '1.500 a 3.000 rpm'], ['Cerdas', 'carbeto de silício'], ['Grãos', '#24 a #1200']], pagina=24),
    _p('escova-tynex-frankfurt-carbeto', 'Escova Tynex Frankfurt Carbeto', 'Acabamento', 3, ['mg', 'conc'],
       [['Encaixe', 'frankfurt'], ['Rotação', '500 rpm'], ['Cerdas', 'carbeto de silício'], ['Grãos', '#24 a #120']], pagina=24),
    # ---------------- Desbaste (pág. 25) ----------------
    _p('desbaste-flat', 'Disco Diamantado de Desbaste Flat', 'Desbaste', 1, TODOS,
       [['Diâmetro', '100 mm (4")'], ['Encaixe', 'M14'], ['Material', 'ferro'], ['Grãos', '#36 #80 #120']], disc=True, pagina=25),
    _p('desbaste-curvo', 'Disco Diamantado de Desbaste Curvo', 'Desbaste', 1, TODOS,
       [['Diâmetro', '100 mm (4")'], ['Encaixe', 'M14'], ['Material', 'ferro'], ['Grão', '#36']], disc=True, destaque=True, pagina=25),
    _p('desbaste-acabamento', 'Disco Diamantado de Acabamento', 'Desbaste', 1, TODOS,
       [['Diâmetro', '100 mm (4")'], ['Espessura', '3 / 7 mm'], ['Encaixe', 'M14'], ['Material', 'ferro'], ['Grãos', '#36 a #220']], disc=True, pagina=25),
    _p('desbaste-disco', 'Disco Diamantado de Desbaste', 'Desbaste', 1, TODOS,
       [['Diâmetro', '100 / 115 / 150 / 180 mm'], ['Encaixe', 'M14'], ['Material', 'ferro'], ['Grãos', '#36 #60 #120']], disc=True, pagina=25),
    _p('prato-desbaste', 'Prato de Desbaste DDD', 'Desbaste', 1, [], [['Diâmetro', 'Ø115 mm'], ['Grão', '#60']],
       img='/assets/produtos/prato-desbaste.webp', nota='Prato diamantado para desbaste e nivelamento antes do polimento.'),
    _p('apicoador-frankfurt', 'Apicoador Frankfurt', 'Desbaste', 1, ['mg', 'conc', 'qtz', 'por'], [['Encaixe', 'frankfurt'], ['Rebolos', '1']], pagina=25),
    _p('sistema-apicoador', 'Sistema Apicoador', 'Desbaste', 1, ['mg', 'conc', 'qtz', 'por'], [['Diâmetro', '125 mm (5")'], ['Encaixe', 'M14'], ['Rebolos', '3']], pagina=25),
    _p('rebolo-apicoado', 'Rebolos para Apicoador Frankfurt', 'Desbaste', 1, ['mg', 'conc', 'qtz', 'por'],
       [['Efeitos', 'jateado, apicoado (45 e 99 dentes), arenoso rústico e arenoso leve'], ['Uso', 'Apicoador Frankfurt']], pagina=25),
    # ---------------- Bases e suportes (pág. 28) ----------------
    _p('base-meia-esquadria-premium', 'Base de Corte Meia Esquadria Maxtool Premium', 'Bases', 0, [], [['Compatível com', 'Serra Mármore Maxtool SM-MT-023']], nivel='Premium', pagina=28),
    _p('base-meia-esquadria-pro', 'Base de Corte Meia Esquadria Maxtool Pro', 'Bases', 0, [], [['Compatível com', 'Serra Mármore Maxtool SM-MT-023']], nivel='Pro', pagina=28),
    _p('base-meia-esquadria-makita', 'Base de Corte Meia Esquadria', 'Bases', 0, [], [['Compatível com', 'Makita profissional 4100NH2']], pagina=28),
    _p('suporte-esmerilhadeira', 'Suporte de Metal para Esmerilhadeira', 'Bases', 0, [], [['Medida', '125 mm'], ['Material', 'metal e plástico']], pagina=28),
    # ---------------- Ferramentas (pág. 26–27, 29) ----------------
    _p('ferr-sargento-45', 'Sargento 45° (Meia Esquadria)', 'Ferramentas Manuais', None, [], [['Medidas', '35 cm (abertura 27,5 cm) / 50 cm (abertura 43,5 cm)'], ['Material', 'aço carbono']], pagina=26),
    _p('ferr-sargento-pressao', 'Sargento de Pressão', 'Ferramentas Manuais', None, [], [['Medida', '6"'], ['Material', 'aço']], pagina=26),
    _p('ferr-grampo-rapido', 'Grampo Rápido', 'Ferramentas Manuais', None, [], [['Medidas', '4" / 6" / 8" / 10"'], ['Material', 'ferro e plástico']], pagina=26),
    _p('ferr-grampo-f', 'Grampo Tipo F', 'Ferramentas Manuais', None, [], [['Medida', '8"'], ['Material', 'aço e alumínio']], pagina=26),
    _p('ferr-sargento-grampo-c', 'Sargento Grampo C', 'Ferramentas Manuais', None, [], [['Medidas', '3" / 4" / 6"'], ['Material', 'ferro fundido']], pagina=26),
    _p('ferr-grampo-a', 'Grampo Tipo A', 'Ferramentas Manuais', None, [], [['Medidas', '4" / 6" / 7" / 9"'], ['Material', 'alumínio']], pagina=26),
    _p('ferr-esquadro-nicho', 'Esquadro para Nicho', 'Ferramentas Manuais', None, [], [['Medidas', '152 × 210 cm / 210 × 213 cm'], ['Material', 'alumínio']], pagina=26),
    _p('ferr-trena-maxtool', 'Trena Maxtool', 'Ferramentas Manuais', None, [], [['Medidas', '5 m / 7,5 m'], ['Material', 'PVC emborrachado']], pagina=27),
    _p('ferr-trena-abs', 'Trena 5 m', 'Ferramentas Manuais', None, [], [['Medida', '5 m'], ['Material', 'plástico ABS']], pagina=26),
    _p('ferr-guia-furo', 'Guia para Furo', 'Ferramentas Manuais', None, [], [['Aperto', '4 a 83 mm'], ['Material', 'plástico']], pagina=27),
    _p('ferr-metro-articulado', 'Metro Articulado', 'Ferramentas Manuais', None, [], [['Medida', '2 m, 12 dobras'], ['Marcação', 'em baixo relevo'], ['Material', 'nylon']], pagina=27),
    _p('ferr-metro-sueco', 'Metro Sueco Hultafors', 'Ferramentas Manuais', None, [],
       [['Versões', 'alumínio (2 m, 10 dobras); fibra de vidro (2 m, 12 dobras · 1 m, 6 dobras · 2 m, 10 dobras com escala invertida); madeira']], pagina=27),
    _p('ferr-esquadro-angular', 'Esquadro Angular', 'Ferramentas Manuais', None, [], [['Medida', '50 cm']], pagina=27),
    _p('ferr-esquadro-l', 'Esquadro Tipo L', 'Ferramentas Manuais', None, [], [['Medidas', '4" / 6" / 8"'], ['Material', 'ABS e fibra']], pagina=27),
    _p('ferr-mao-amiga', 'Mão Amiga', 'Ferramentas Manuais', None, ['mg'], [['Uso', 'carregamento de mármores e granitos'], ['Material', 'ferro e borracha']], pagina=27),
    _p('ferr-ventosa-45', 'Ventosa Dupla para 45°', 'Ferramentas Manuais', None, [], [['Peso', '2,2 kg'], ['Nivelamento', 'ajustável, não marca o material'], ['Material', 'alumínio']], pagina=29),
    _p('ferr-ventosa-nivelamento', 'Ventosa Dupla para Nivelamento', 'Ferramentas Manuais', None, [], [['Peso', '1,1 kg'], ['Capacidade', 'até 100 kg'], ['Material', 'alumínio']], pagina=29),
    _p('ferr-aplicador-silicone', 'Aplicador de Silicone', 'Ferramentas Manuais', None, [], [['Capacidade', '600 g'], ['Material', 'metal e plástico']], pagina=29),
    _p('ferr-aplicador-selante', 'Aplicador de Selante', 'Ferramentas Manuais', None, [], [['Capacidade', '400 g'], ['Material', 'metal']], pagina=29),
    _p('ferr-nivelador-porcelanato', 'Nivelador de Porcelanato', 'Ferramentas Manuais', None, ['por'], [['Material', 'metal']], pagina=29),
    _p('ferr-rolo-fibra', 'Rolo de Fibra para Reforço', 'Ferramentas Manuais', None, [], [['Medidas', '6,5 × 3 mm / 9,35 × 3 mm'], ['Material', 'fibra de vidro']], pagina=29),
    _p('ferr-avental', 'Avental', 'Ferramentas Manuais', None, [], [['Medida', '120 cm (A) × 75 cm (L)']], pagina=29),
    # ---------------- Acessórios (pág. 30–31) ----------------
    _p('ac-suporte-plastico-velcro', 'Suporte de Plástico com Velcro', 'Acessórios', None, [], [['Diâmetro', '100 mm (4") / 180 mm (7")'], ['Encaixe', 'M14'], ['Tipo', 'rígido / flexível']], pagina=30),
    _p('ac-suporte-plastico-sem-velcro', 'Suporte de Plástico sem Velcro', 'Acessórios', None, [], [['Diâmetro', '180 mm (7")'], ['Encaixe', 'porca cônica'], ['Tipo', 'rígido / flexível']], pagina=30),
    _p('ac-suporte-borracha-velcro', 'Suporte de Borracha com Velcro', 'Acessórios', None, [], [['Diâmetro', '100 mm (4") / 125 mm (5")'], ['Encaixe', 'M14'], ['Tipo', 'rígido / semi-rígido / flexível / super flexível']], pagina=30),
    _p('ac-suporte-borracha-concavo', 'Suporte de Borracha Côncavo com Velcro', 'Acessórios', None, [], [['Diâmetro', '100 mm (4")'], ['Encaixe', 'M14'], ['Tipo', 'semi-rígido']], pagina=30),
    _p('ac-suporte-borracha-flat', 'Suporte de Borracha Flat com Velcro', 'Acessórios', None, [], [['Diâmetro', '100 mm (4")'], ['Encaixe', 'M14'], ['Tipo', 'semi-rígido / super flexível']], pagina=30),
    _p('ac-suporte-espuma-velcro', 'Suporte de Plástico com Espuma e Velcro', 'Acessórios', None, [], [['Diâmetro', '100 mm (4") / 125 mm (5") / 180 mm (7")'], ['Encaixe', 'M14'], ['Tipo', 'rígido']], pagina=30),
    _p('ac-suporte-caracol-velcro', 'Suporte de Plástico Caracol com Velcro', 'Acessórios', None, [], [['Diâmetro', '125 mm (5")'], ['Encaixe', 'caracol'], ['Tipo', 'rígido']], pagina=30),
    _p('ac-suporte-caracol-aluminio', 'Suporte Caracol de Alumínio', 'Acessórios', None, [], [['Diâmetro', '100 mm (4") / 125 mm (5")'], ['Encaixe', 'M14 / caracol'], ['Material', 'alumínio e borracha']], pagina=30),
    _p('ac-feltro-velcro', 'Feltro com Velcro', 'Acessórios', None, [], [['Diâmetro', '100 mm / 180 mm'], ['Espessura', '15 mm']], pagina=30),
    _p('ac-roda-feltro', 'Roda de Feltro', 'Acessórios', None, [], [['Diâmetro', '100 mm (4")'], ['Encaixe', 'caracol'], ['Espessura', '20 mm']], pagina=31),
    _p('ac-refil-velcro', 'Refil de Velcro para Suporte de Lixas', 'Acessórios', None, [], [['Diâmetro', '100 mm (4") / 125 mm (5") / 180 mm (7")']], pagina=31),
    _p('ac-suporte-frankfurt', 'Suporte de Plástico Frankfurt', 'Acessórios', None, [], [['Encaixe', 'frankfurt'], ['Tipo', 'rígido']], pagina=31),
    _p('ac-adaptador-husqvarna', 'Adaptador Husqvarna', 'Acessórios', None, [], [['Medida', '73 × 69 × 55 mm'], ['Encaixe', 'LVS – Husqvarna'], ['Material', 'metal']], pagina=31),
    _p('ac-gaveta-lvs', 'Gaveta LVS', 'Acessórios', None, [], [['Encaixe', 'LVS'], ['Material', 'metal']], pagina=31),
    _p('ac-anel-redutor', 'Anel Redutor', 'Acessórios', None, [], [['Medida', '50 mm – 25,4 mm'], ['Espessura', '1,4 / 1,6 / 1,8 / 2,0 mm'], ['Material', 'cobre']], pagina=31),
    _p('ac-porca-aperto', 'Porca de Aperto', 'Acessórios', None, [], [['Encaixe', 'M14'], ['Material', 'alumínio']], pagina=31),
    _p('ac-pulverizador', 'Pulverizador para Serra Mármore', 'Acessórios', None, [], [['Mangueira', 'flexível'], ['Compatibilidade', 'universal'], ['Material', 'latão e metal']], pagina=31),
    _p('ac-dimmer', 'Dimmer 3000 W', 'Acessórios', None, [], [['Potência', '3.000 W'], ['Tensão', 'bivolt (110 V / 220 V)']], pagina=31),
]

ORDEM_CATEGORIAS = ['Discos de Corte', 'Serras Diamantadas', 'Brocas Diamantadas', 'Máquinas', 'Lixas Diamantadas',
                    'Polibordas', 'Desbaste', 'Acabamento', 'Bases', 'Ferramentas Manuais', 'Acessórios']


def _texto_mats(codes):
    nomes = [MAT[c] for c in codes]
    if not nomes:
        return ''
    if len(nomes) == len(MAT):
        return 'todos os materiais (mármore e granito, porcelanato, quartzito, nanoglass, ultracompactos, concreto e granilite)'
    return nomes[0].lower() if len(nomes) == 1 else ', '.join(n.lower() for n in nomes[:-1]) + ' e ' + nomes[-1].lower()


def completar(dims):
    """Preenche imagem, dimensões, linha de especificação e descrição de cada produto."""
    for p in PRODUTOS:
        if not p['img']:
            p['img'] = f"/assets/catalogo/{p['id']}.avif"
            p['fallback'] = f"/assets/catalogo/{p['id']}.png"
            p['w'], p['h'] = dims.get(p['id'], (500, 500))
        else:
            p['fallback'] = p['img']
            p['w'], p['h'] = {'serra-marmore': (950, 622), 'prato-desbaste': (950, 544)}.get(p['id'], (600, 600))
        principais = [v for k, v in p['specs'] if k in ('Diâmetro', 'Diâmetros', 'Medida', 'Medidas', 'Modelo', 'Disco')][:1]
        extra = [v for k, v in p['specs'] if k in ('Potência', 'Rotação máx.', 'Grãos', 'Grão', 'Espessura', 'Furo central', 'Encaixe')][:1]
        p['spec'] = ' · '.join((principais + extra)) or p['specs'][0][1]
        p['materiais'] = [MAT[c] for c in p['mats']]
        nivel = f" linha {p['nivel']}" if p['nivel'] else (f" linha {p['linha']}" if p['linha'] else '')
        uso = f" Indicado para {_texto_mats(p['mats'])}." if p['mats'] else ''
        base = p['nota'] or f"{p['nome']} Maxtool{nivel}."
        p['desc'] = (base + uso).strip()
    return PRODUTOS
