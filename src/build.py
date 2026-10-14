#!/usr/bin/env python3
"""Monta o site estático da Maxtool (padrão QH4: SEO + AEO + GEO).

Uso:  python3 src/build.py

Gera:
  • index.html de cada página (/, /produtos/, /sobre/ ...) a partir de src/layout.html + src/sections/
  • HTML estático de produtos, etapas e reels (legível por buscadores e IAs que não executam JS)
  • schema.org em @graph por página (Organization, LocalBusiness, WebSite, WebPage, BreadcrumbList,
    FAQPage, ItemList/Product, HowTo, EventSeries)
  • sitemap.xml (com imagens), robots.txt (libera crawlers de IA), llms.txt, llms-full.txt, 404.html,
    site.webmanifest
Edite textos em src/sections/ e dados em src/data.py, depois rode de novo.
"""
import html as H
from urllib.parse import quote
import json
import re
from datetime import date
from pathlib import Path

from catalogo import MAT, ORDEM_CATEGORIAS, completar
from data import (CATEGORIAS, DIFERENCIAIS, EMPRESA as E, ERROS_COMUNS, ETAPAS, FAQS, GTM_ID, GUIA_MATERIAIS,
                  LINHA_COMPLETA, MATERIAIS, MTDAY, NIVEIS, REELS, REMOTE, SITE)

SRC = Path(__file__).parent
ROOT = SRC.parent
HOJE = date.today()
OG_IMAGE = f'{SITE}/assets/og/maxtool-og.jpg'

NAV = [
    ('/produtos/', 'Produtos'),
    ('/sobre/', 'A Maxtool'),
    ('/pecas/', 'Peças &amp; Assistência'),
    ('/max-tool-day/', 'Max Tool Day'),
    ('/onde-comprar/', 'Onde comprar'),
    ('/contato/', 'Contato'),
]

esc = H.escape


# =====================================================================
# Componentes HTML
# =====================================================================
def page_hero(eyebrow, title, lead, crumb, extra=''):
    return f'''  <section class="page-hero">
    <div class="page-hero-bg" aria-hidden="true"><img src="/assets/produtos/disco-mesh.webp" alt="" width="905" height="950"><div class="chevrons"></div></div>
    <div class="container">
      <nav class="crumbs" aria-label="Você está em"><a href="/">Início</a><span aria-hidden="true">/</span><span aria-current="page">{crumb}</span></nav>
      <p class="eyebrow">{eyebrow}</p>
      <h1 class="page-title">{title}</h1>
      <p class="lead">{lead}</p>
      {extra}
    </div>
  </section>
'''


def resumo(pergunta, resposta, dark=False):
    """Bloco 'Resposta rápida' — resposta direta para buscadores e IAs (AEO)."""
    return f'''  <section class="resumo{' resumo--dark' if dark else ''}" aria-label="Resposta rápida">
    <div class="container resumo-inner">
      <p class="resumo-tag">Resposta rápida</p>
      <h2 class="resumo-q">{pergunta}</h2>
      <p class="resumo-a">{resposta}</p>
    </div>
  </section>
'''


LINKS = [
    ('página Onde comprar', '/onde-comprar/'), ('localizador por CEP', '/onde-comprar/'),
    ('página Seja um revendedor', '/seja-um-revendedor/'), ('cadastro de revenda', '/seja-um-revendedor/'),
    ('página Peças &amp; Assistência', '/pecas/'), ('páginas Produtos', '/produtos/'),
]


def linkify(t):
    t = esc(t)
    for txt, href in LINKS:
        t = t.replace(txt, f'<a href="{href}">{txt}</a>', 1)
    return t


def faq_section(slug):
    itens = '\n'.join(
        f'        <details{" open" if i == 0 else ""}><summary>{esc(q)}</summary><p>{linkify(a)}</p></details>'
        for i, (q, a) in enumerate(FAQS[slug]))
    return f'''  <section class="section on-paper faq" aria-labelledby="faq-title">
    <div class="container faq-inner">
      <div>
        <p class="eyebrow">Dúvidas frequentes</p>
        <h2 id="faq-title">Perguntou,<br>respondemos.</h2>
        <p class="lead">Não achou o que procura? Chama a gente no WhatsApp.</p>
        <a class="btn btn-dark" href="https://wa.me/{E['whatsapp_digits']}?text=Ol%C3%A1!%20Vim%20pelo%20site%20da%20Maxtool." target="_blank" rel="noopener" data-track="whatsapp_faq"><svg><use href="#i-wa"/></svg> {E['whatsapp']}</a>
      </div>
      <div class="faq-list">
{itens}
      </div>
    </div>
  </section>
'''


PRODUTOS = completar(json.loads((SRC / 'catalogo_dims.json').read_text()))
PROD = {p['id']: p for p in PRODUTOS}
DESTAQUES = [p for p in PRODUTOS if p['destaque']]
slug = lambda t: re.sub(r'[^a-z0-9]+', '-', t.lower().translate(str.maketrans('áàâãéêíóôõúç', 'aaaaeeiooouc'))).strip('-')
NIVEL_ORDEM = {'Premium': 0, 'Pro': 1, None: 2, 'Std': 3}
ordenar = lambda lst: sorted(lst, key=lambda p: (not p['destaque'], NIVEL_ORDEM.get(p['nivel'], 2)))


def pic(p, alt='', eager=False):
    """<picture> com AVIF e PNG de reserva (ou a imagem única dos produtos antigos)."""
    load = '' if eager else ' loading="lazy"'
    img = f'<img src="{p["fallback"]}" alt="{esc(alt)}" width="{p["w"]}" height="{p["h"]}"{load} decoding="async">'
    if p['img'].endswith('.avif'):
        return f'<picture><source srcset="{p["img"]}" type="image/avif">{img}</picture>'
    return img


def tag_nivel(p):
    return f'<span class="tag is-{p["nivel"].lower()}">{p["nivel"]}</span>' if p.get('nivel') else (
        f'<span class="tag is-linha">{p["linha"]}</span>' if p.get('linha') else '')


GUIA_COD = {'marmore-granito': 'mg', 'porcelanato': 'por', 'quartzito': 'qtz', 'nanoglass': 'nano',
            'ultracompactos': 'ult', 'concreto-granilite': 'conc'}
GUIA_LINHAS = [
    ('Corte', lambda p: p['etapa'] == 0 and p['cat'] != 'Brocas Diamantadas', 0),
    ('Furo', lambda p: p['cat'] == 'Brocas Diamantadas', 0),
    ('Desbaste', lambda p: p['etapa'] == 1, 1),
    ('Polimento', lambda p: p['etapa'] == 2, 2),
    ('Acabamento', lambda p: p['etapa'] == 3, 3),
]


def guia_section():
    """A ferramenta certa para cada material (briefing, P30)."""
    tabs, panels = [], []
    for i, m in enumerate(GUIA_MATERIAIS):
        mid, nome, picto = m['id'], m['nome'], m['picto']
        sel = 'true' if i == 0 else 'false'
        tabidx = '' if i == 0 else ' tabindex="-1"'
        hidden = '' if i == 0 else ' hidden'
        tabs.append(f'<button role="tab" id="tab-mat-{mid}" aria-controls="mat-{mid}" aria-selected="{sel}"{tabidx}>'
                    f'<svg aria-hidden="true"><use href="#{picto}"/></svg>{nome}</button>')
        code = GUIA_COD[mid]
        linhas = []
        for etapa, filtro, eid in GUIA_LINHAS:
            itens = ordenar([pr for pr in PRODUTOS if code in pr['mats'] and filtro(pr)])
            if not itens:
                continue
            chips = []
            for pr in itens[:6]:
                chips.append(f'<button class="guia-prod" type="button" data-id="{pr["id"]}">{pic(pr)}'
                             f'<span><b>{esc(pr["nome"])}</b><small>{esc(pr["spec"])}</small></span>{tag_nivel(pr)}</button>')
            if len(itens) > 6:
                chips.append(f'<a class="guia-mais" href="/produtos/?material={code}&amp;etapa={eid}#destaques">+{len(itens) - 6}<small>ver todos</small></a>')
            linhas.append(f'<div class="guia-row"><h4>{etapa}<small>{len(itens)} {"produto" if len(itens) == 1 else "produtos"}</small></h4><div class="guia-itens">{"".join(chips)}</div></div>')
        pergunta = f'Olá! Qual ferramenta Maxtool usar para {nome}?'
        wa = 'https://wa.me/' + E['whatsapp_digits'] + '?text=' + quote(pergunta)
        desafio = esc(m['desafio'])
        corpo = ''.join(linhas)
        panels.append(f"""
        <div class="guia-panel" id="mat-{mid}" role="tabpanel" aria-labelledby="tab-mat-{mid}"{hidden}>
          <div class="guia-panel-head">
            <svg class="guia-picto" aria-hidden="true"><use href="#{picto}"/></svg>
            <div><h3>{nome}</h3><p>{desafio}</p></div>
            <a class="guia-total" href="/produtos/?material={code}#destaques"><b>{sum(1 for pr in PRODUTOS if code in pr['mats'])}</b><span>produtos do catálogo<br>para {nome.lower()}</span></a>
          </div>
          {corpo}
          <div class="guia-acts">
            <a class="btn btn-red btn-sm" href="/onde-comprar/" data-track="guia_onde_comprar">Onde comprar <svg><use href="#i-arrow"/></svg></a>
            <a class="btn btn-ghost btn-sm" href="{wa}" target="_blank" rel="noopener" data-track="guia_whatsapp"><svg><use href="#i-wa"/></svg> Tirar dúvida técnica</a>
          </div>
        </div>""")
    erros = ''.join(f'<li class="reveal"><b>{esc(t)}</b><span>{esc(d)}</span></li>' for t, d in ERROS_COMUNS)
    niveis = ''.join(f'<li><span class="tag is-{n.lower()}">{n}</span>{esc(d)}</li>' for n, d in NIVEIS)
    tabs_html, panels_html = ''.join(tabs), ''.join(panels)
    return f"""  <section class="section guia" id="ferramenta-por-material" aria-labelledby="guia-title">
    <div class="container">
      <div class="split-head">
        <div>
          <p class="eyebrow">Guia técnico</p>
          <h2 id="guia-title">A ferramenta certa<br>para cada <span class="red">material</span>.</h2>
        </div>
        <p class="lead">Disco ou lixa errada é peça lascada, ferramenta perdida e prejuízo. Escolha o material e veja o que a Maxtool tem para cada etapa do serviço.</p>
      </div>
      <div class="guia-ui">
        <div class="guia-tabs" role="tablist" aria-label="Escolha o material">{tabs_html}</div>
        <div class="guia-panels">{panels_html}</div>
      </div>
      <div class="guia-extra">
        <div class="guia-niveis">
          <h3>Qual nível escolher?</h3>
          <ul>{niveis}</ul>
        </div>
        <div class="guia-erros">
          <h3>Erros que estragam a peça e a ferramenta</h3>
          <ul>{erros}</ul>
        </div>
      </div>
    </div>
  </section>
"""


def diferenciais_section():
    itens = ''.join(f'<li class="reveal"><b>{esc(t)}</b><span>{esc(d)}</span></li>' for t, d in DIFERENCIAIS)
    return f'''  <section class="section diferenciais" aria-labelledby="dif-title">
    <div class="container">
      <div class="split-head">
        <div>
          <p class="eyebrow">Por que Maxtool</p>
          <h2 id="dif-title">Fornecedor que<br>trabalha junto.</h2>
        </div>
        <p class="lead">Mais do que vender produtos: estoque, suporte e condições para a revenda vender mais — e ferramenta certa para o marmorista produzir mais.</p>
      </div>
      <ul class="dif-grid">{itens}</ul>
    </div>
  </section>
'''


def downloads_section():
    maquinas = json.loads((ROOT / 'assets/pecas/pecas.json').read_text())
    pdfs = [('Catálogo 2026 — versão leve', f'{REMOTE}/catalogo/maxtool-catalogo-2026-leve.pdf', 'PDF · 8 MB'),
            ('Catálogo 2026 — alta resolução', f'{REMOTE}/catalogo/maxtool-catalogo-2026.pdf', 'PDF · 51 MB')]
    pdfs += [(f'Vista explodida — {m["nome"]} {m["modelo"]}', f'{REMOTE}/pecas/downloads/{m["slug"]}.pdf', 'PDF · peças')
             for m in maquinas]
    itens = ''.join(f'<li><a href="{u}" target="_blank" rel="noopener" data-track="download"><svg><use href="#i-download"/></svg><span><b>{esc(t)}</b><small>{d}</small></span></a></li>'
                    for t, u, d in pdfs)
    return f'''  <section class="section downloads" id="downloads" aria-labelledby="dl-title">
    <div class="container">
      <p class="eyebrow">Central de downloads</p>
      <h2 id="dl-title">Catálogo e fichas<br>num lugar só.</h2>
      <ul class="dl-list">{itens}</ul>
    </div>
  </section>
'''


def prod_card(p, i):
    mats = ' '.join(p['mats'])
    return f'''
    <button class="prod{' is-disc' if p.get('disc') else ''}" type="button" data-id="{p['id']}" data-etapa="{p['etapa'] if p['etapa'] is not None else ''}" data-nivel="{p.get('nivel') or ''}" data-cat="{slug(p['cat'])}" data-mats="{mats}" aria-label="Ver detalhes: {esc(p['nome'])}">
      <span class="prod-top"><span class="prod-idx">{i + 1:02d}</span>{tag_nivel(p)}</span>
      <span class="prod-media">{pic(p, p['nome'] + ' — ' + p['spec'])}</span>
      <span class="prod-info">
        <span class="prod-cat">{esc(p['cat'])}</span>
        <span class="prod-name">{esc(p['nome'])}</span>
        <span class="prod-spec">{esc(p['spec'])}</span>
        <span class="prod-more">Ver detalhes <svg><use href="#i-arrow"/></svg></span>
      </span>
    </button>'''


def showcase_cards():
    end = f'''
    <a class="prod-end" href="/produtos/#destaques" data-track="catalogo_vitrine">
      <b>+{len(PRODUTOS)}<br>produtos<br>no site</b>
      <span>Ver a linha completa <svg><use href="#i-arrow"/></svg></span>
    </a>'''
    return ''.join(prod_card(p, i) for i, p in enumerate(DESTAQUES)) + end


def prod_grid():
    ordem = {c: i for i, c in enumerate(ORDEM_CATEGORIAS)}
    lista = sorted(PRODUTOS, key=lambda p: (ordem.get(p['cat'], 99), NIVEL_ORDEM.get(p['nivel'], 2)))
    return ''.join(prod_card(p, i) for i, p in enumerate(lista))


def grid_filtros():
    cats = ''.join(f'<option value="{slug(c)}">{esc(c)} ({sum(1 for p in PRODUTOS if p["cat"] == c)})</option>' for c in ORDEM_CATEGORIAS)
    mats = ''.join(f'<option value="{k}">{v} ({sum(1 for p in PRODUTOS if k in p["mats"])})</option>' for k, v in MAT.items())
    return f'''<div class="filtros-sel">
        <label><span>Categoria</span><select id="f-cat"><option value="">Todas</option>{cats}</select></label>
        <label><span>Material</span><select id="f-mat"><option value="">Todos</option>{mats}</select></label>
        <label><span>Etapa</span><select id="f-etapa"><option value="">Todas</option><option value="0">Corte e furo</option><option value="1">Desbaste</option><option value="2">Polimento</option><option value="3">Acabamento</option></select></label>
        <label><span>Nível</span><select id="f-nivel"><option value="">Todos</option><option>Premium</option><option>Pro</option><option>Std</option></select></label>
      </div>'''


def etapas_panels():
    out = []
    for i, e in enumerate(ETAPAS):
        todos = ordenar([p for p in PRODUTOS if p['etapa'] == i])
        prods = ''.join(f'''
          <button class="etapa-prod" type="button" data-id="{p['id']}">
            {pic(p)}
            <b>{esc(p['nome'])}</b><small>{esc(p['spec'])}</small>
          </button>''' for p in todos[:8])
        mais = (f'<a class="etapa-mais" href="/produtos/?etapa={i}#destaques">Ver todos os {len(todos)} produtos de {e["nome"].lower()} '
                f'<svg><use href="#i-arrow"/></svg></a>') if len(todos) > 8 else ''
        cats = ''.join(f'<span>{esc(c)}</span>' for c in e['cats'])
        out.append(f'''
      <div class="etapa" id="etapa-{i}" role="tabpanel" aria-labelledby="tab-etapa-{i}"{'' if i == 0 else ' hidden'}>
        <div class="etapa-head">
          <div><h3>{e['nome']}</h3><p>{e['txt']}</p></div>
          <span class="etapa-num" aria-hidden="true">0{i + 1}</span>
        </div>
        <div class="etapa-cats">{cats}</div>
        <div class="etapa-prods">{prods}</div>
        {mais}
      </div>''')
    return ''.join(out)


def reels():
    one = ''.join(f'''
      <a class="reel" href="{url}" target="_blank" rel="noopener">
        <img src="/assets/instagram/{img}" alt="Reel Maxtool: {esc(cap)}" width="360" height="640" loading="lazy" decoding="async">
        <span class="play"><svg><use href="#i-play"/></svg></span>
        <span class="cap">{esc(cap)}</span>
      </a>''' for img, url, cap in REELS)
    dup = one.replace('<a class="reel"', '<a class="reel" aria-hidden="true" tabindex="-1"').replace(' alt="Reel Maxtool: ', ' alt="" data-alt="')
    return one + dup


# =====================================================================
# Páginas
# =====================================================================
PAGES = [
    dict(path='/', slug='home', crumb=None,
         title='Ferramentas para Marmoraria e Rochas | Maxtool Vitória-ES',
         description='Discos, serras e lixas diamantadas, máquinas e peças para mármore, granito, porcelanato e quartzito. +1.000 itens e 250+ revendas no Brasil desde 2010.',
         preload='<link rel="preload" as="image" href="/assets/produtos/serra-marmore-hero.webp" fetchpriority="high">',
         body=['hero', 'materiais',
               resumo('O que é a Maxtool?', E['resumo']),
               'manifesto', 'showcase', 'guia', 'diferenciais', 'niveis', 'mtday', 'embaixadores', 'instagram', 'faq:home', 'cta-band']),
    dict(path='/produtos/', slug='produtos', crumb='Produtos',
         title='Disco Diamantado, Serra e Lixa para Rocha | Maxtool',
         description='Disco para porcelanato que não lasca, serra para quartzito, lixa para polir granito, máquinas e peças. Guia da ferramenta certa por material.',
         body=[page_hero('Produtos', 'Ferramentas que<br>aguentam a <span class="red">obra</span>.',
                         'Mais de 1.000 itens para cada etapa do trabalho em rocha — do primeiro corte ao brilho final, em três níveis de performance.',
                         'Produtos',
                         f'<div class="actions"><a class="btn btn-red" href="{REMOTE}/catalogo/maxtool-catalogo-2026-leve.pdf" target="_blank" rel="noopener" data-track="catalogo_hero"><svg><use href="#i-download"/></svg> Catálogo 2026</a><a class="btn btn-ghost" href="#destaques">Ver destaques</a></div>'),
               'materiais',
               resumo('Quais ferramentas a Maxtool fabrica e distribui?',
                      'A Maxtool tem mais de 1.000 itens para marmoraria em 11 categorias: máquinas, discos de corte, serras diamantadas, lixas diamantadas (linhas SL, SLX, SLe e SLXe), polibordas, brocas diamantadas, desbaste, acabamento, ferramentas manuais, acessórios e bases — para mármore, granito, porcelanato, quartzito, nanoglass, ultracompactos, concreto e granilite.'),
               'guia', 'etapas', 'produtos-grid', 'niveis', 'catalogo', 'downloads', 'faq:produtos', 'cta-band']),
    dict(path='/sobre/', slug='sobre', crumb='A Maxtool',
         title='Sobre a Maxtool | Ferramentas para Rochas desde 2010',
         description='Importadora e distribuidora de ferramentas para marmoraria em Vitória/ES desde 2010. De 5 produtos a mais de 1.000 itens e 250+ revendas no Brasil.',
         body=[page_hero('Quem somos', 'Mais do que uma marca<br>de ferramentas.',
                         'Desde 2010 ao lado de quem vive da rocha — levando ao profissional brasileiro produtos selecionados para performar onde importa: na obra.',
                         'A Maxtool'),
               resumo('Quem é a Maxtool?', E['resumo'] + f' Razão social: {E["razao"]}, CNPJ {E["cnpj"]}.'),
               'sobre-historia', 'diferenciais', 'manifesto', 'embaixadores', 'instagram', 'faq:sobre', 'cta-band']),
    dict(path='/pecas/', slug='pecas', crumb='Peças &amp; Assistência',
         title='Peças de Reposição e Garantia de Máquinas | Maxtool',
         description='Vista explodida e lista de peças da serra mármore SM-MT-023, politrizes MT-023, MT-01 e PP-MT-023 e esmerilhadeira EA-MT-025. Saiba acionar a garantia.',
         body=[page_hero('Peças &amp; Assistência', 'Sua máquina aberta<br>na sua <span class="red">tela</span>.',
                         'Vista explodida e lista de peças de reposição de cada máquina Maxtool — para a oficina e para o marmorista que resolve com as próprias mãos.',
                         'Peças &amp; Assistência'),
               resumo('Como conseguir peça ou garantia de uma máquina Maxtool?',
                      'Encontre o número da peça na vista explodida abaixo e fale com a Maxtool pelo WhatsApp ' + E['whatsapp'] + ', com a nota fiscal em mãos. Em caso de defeito de fabricação, a Maxtool envia a peça sem custo e paga a mão de obra da oficina — ou você envia a máquina direto para a Maxtool.'),
               'pecas', 'downloads', 'faq:pecas', 'cta-band']),
    dict(path='/max-tool-day/', slug='mtday', crumb='Max Tool Day',
         title='Max Tool Day | Workshop de Marmoraria na Revenda | Maxtool',
         description='Max Tool Day: capacitação para marmoristas em 13/11/2026 na BSB Abrasivos, Vicente Pires-DF. Técnica ao vivo e ingresso que vira voucher.',
         body=['mtday',
               resumo('O que é o Max Tool Day?', dict(FAQS['mtday'])['O que é o Max Tool Day?']),
               'mtday-como', 'embaixadores', 'instagram', 'faq:mtday']),
    dict(path='/onde-comprar/', slug='onde', crumb='Onde comprar',
         title='Onde Comprar Maxtool | Revendas em Todo o Brasil',
         description='Encontre a revenda Maxtool mais próxima pelo CEP: são mais de 250 lojas parceiras no Brasil. A Maxtool vende só para revendas.',
         body=['onde',
               resumo('Onde comprar ferramentas Maxtool?',
                      'A Maxtool vende exclusivamente por revendas: são mais de 250 lojas parceiras em todo o Brasil. Digite seu CEP no localizador acima ou chame no WhatsApp ' + E['whatsapp'] + ' para saber qual revenda fica mais perto de você.'),
               'faq:onde', 'cta-band']),
    dict(path='/seja-um-revendedor/', slug='revenda', crumb='Seja um revendedor',
         title='Revenda Maxtool | Fornecedor de Ferramentas Diamantadas',
         description='Importadora e fornecedor de disco diamantado e lixa para revenda de marmoraria. Pronta entrega, todo o Brasil, pagamento a prazo. Cadastre sua loja.',
         body=['revenda',
               resumo('Como ser revendedor Maxtool?',
                      'Lojas do ramo de abrasivos e ferramentas para rochas, com CNPJ de revenda do ramo e compromisso com pedidos recorrentes, podem se cadastrar no formulário acima. A equipe comercial retorna com a política completa: pedido mínimo, prazos e condições para a região.', dark=True),
               'diferenciais', 'catalogo', 'faq:revenda']),
    dict(path='/politica-de-privacidade/', slug='privacidade', crumb='Política de Privacidade',
         title='Política de Privacidade | Maxtool',
         description='Como a Maxtool trata dados pessoais no site e nos avisos por WhatsApp, conforme a LGPD: o que coletamos, para quê, com quem compartilhamos e seus direitos.',
         body=[page_hero('Privacidade', 'Política de<br>Privacidade.',
                         'Respeito aqui não é só com a ferramenta: é com os seus dados também. Sem juridiquês, conforme a LGPD.',
                         'Política de Privacidade'),
               'privacidade']),
    dict(path='/contato/', slug='contato', crumb='Contato',
         title='Contato Maxtool | WhatsApp, Telefone e Endereço Vitória-ES',
         description=f'Fale com a Maxtool: WhatsApp {E["whatsapp"]}, {E["email"]}, (27) 3019-3040. Av. Paulino Muller, 945, Vitória-ES. Atendemos todo o Brasil.',
         body=[page_hero('Contato', 'Fale com<br>a gente.',
                         'Atendemos marmoristas e revendas de todo o Brasil. Escolha o canal e chame a gente.',
                         'Contato'),
               'contato-cards', 'faq:contato']),
]


# =====================================================================
# schema.org
# =====================================================================
ORG_ID, BIZ_ID, SITE_ID = f'{SITE}/#organization', f'{SITE}/#sede', f'{SITE}/#website'


def org_nodes():
    endereco = {'@type': 'PostalAddress', 'streetAddress': E['rua'], 'addressLocality': E['cidade'],
                'addressRegion': E['uf'], 'postalCode': E['cep'], 'addressCountry': 'BR'}
    return [
        {'@type': 'Organization', '@id': ORG_ID, 'name': E['nome'], 'legalName': E['razao'], 'taxID': E['cnpj'],
         'url': SITE + '/', 'logo': {'@type': 'ImageObject', 'url': f'{SITE}/assets/logos/maxtool-dark.svg'},
         'image': OG_IMAGE, 'slogan': E['slogan'], 'description': E['resumo'], 'foundingDate': E['fundacao'],
         'foundingLocation': {'@type': 'Place', 'name': 'Vitória, Espírito Santo, Brasil'},
         'address': endereco, 'areaServed': {'@type': 'Country', 'name': 'Brasil'},
         'knowsAbout': ['ferramentas para marmoraria', 'abrasivos diamantados', 'discos de corte diamantados',
                        'serras diamantadas', 'lixas diamantadas', 'polimento de rochas'] + MATERIAIS,
         'sameAs': [E['instagram']],
         'contactPoint': [
             {'@type': 'ContactPoint', 'contactType': 'sales', 'telephone': E['whatsapp'], 'email': E['email'],
              'areaServed': 'BR', 'availableLanguage': 'Portuguese', 'hoursAvailable': {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'opens': '08:00', 'closes': '17:00'}},
             {'@type': 'ContactPoint', 'contactType': 'customer service', 'telephone': E['telefone'],
              'areaServed': 'BR', 'availableLanguage': 'Portuguese'}]},
        {'@type': ['LocalBusiness', 'WholesaleStore'], '@id': BIZ_ID, 'name': 'Maxtool — Vitória/ES',
         'parentOrganization': {'@id': ORG_ID}, 'url': SITE + '/contato/', 'image': OG_IMAGE,
         'telephone': E['telefone'], 'email': E['email'], 'address': endereco,
         'geo': {'@type': 'GeoCoordinates', 'latitude': E['lat'], 'longitude': E['lng']},
         'hasMap': 'https://www.google.com/maps/search/?api=1&query=Av.+Paulino+Muller,+945+Jucutuquara+Vit%C3%B3ria+ES',
         'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'opens': '08:00', 'closes': '17:00'}],
         'areaServed': {'@type': 'Country', 'name': 'Brasil'}, 'priceRange': '$$'},
        {'@type': 'WebSite', '@id': SITE_ID, 'url': SITE + '/', 'name': 'Maxtool', 'inLanguage': 'pt-BR',
         'publisher': {'@id': ORG_ID}},
    ]


def product_node(p):
    node = {'@type': 'Product', '@id': f'{SITE}/produtos/#{p["id"]}', 'name': f'{p["nome"]} Maxtool' + (f' {p["nivel"]}' if p['nivel'] else ''),
            'image': SITE + p['fallback'], 'description': p['desc'],
            'brand': {'@type': 'Brand', 'name': 'Maxtool'}, 'manufacturer': {'@id': ORG_ID},
            'category': p['cat'],
            'additionalProperty': [{'@type': 'PropertyValue', 'name': k, 'value': v} for k, v in p['specs']]
            + [{'@type': 'PropertyValue', 'name': 'Material indicado', 'value': m} for m in p['materiais']]}
    modelo = dict(p['specs']).get('Modelo')
    if modelo:
        node['model'] = modelo
    return node


def page_graph(p, faq_items):
    url = SITE + p['path']
    nodes = org_nodes()
    webpage = {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': p['title'],
               'description': p['description'], 'inLanguage': 'pt-BR', 'isPartOf': {'@id': SITE_ID},
               'about': {'@id': ORG_ID}, 'primaryImageOfPage': OG_IMAGE,
               'dateModified': HOJE.isoformat(),
               'speakable': {'@type': 'SpeakableSpecification', 'cssSelector': ['h1', '.resumo-a']}}
    if p['crumb']:
        crumb = H.unescape(p['crumb'])
        nodes.append({'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': crumb, 'item': url}]})
        webpage['breadcrumb'] = {'@id': url + '#breadcrumb'}
    if p['slug'] == 'sobre':
        webpage['@type'] = 'AboutPage'
    if p['slug'] == 'contato':
        webpage['@type'] = 'ContactPage'
    nodes.append(webpage)
    if faq_items:
        nodes.append({'@type': 'FAQPage', '@id': url + '#faq', 'isPartOf': {'@id': url + '#webpage'},
                      'mainEntity': [{'@type': 'Question', 'name': q,
                                      'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq_items]})
    if p['slug'] in ('home', 'produtos'):
        lista = PRODUTOS if p['slug'] == 'produtos' else DESTAQUES
        nodes.append({'@type': 'ItemList', '@id': url + '#produtos',
                      'name': 'Produtos Maxtool' if p['slug'] == 'produtos' else 'Destaques da linha Maxtool',
                      'numberOfItems': len(lista), 'itemListElement': [
                          {'@type': 'ListItem', 'position': i + 1, 'item': product_node(x)}
                          for i, x in enumerate(lista)]})
    if p['slug'] == 'pecas':
        maquinas = json.loads((ROOT / 'assets/pecas/pecas.json').read_text())
        nodes.append({'@type': 'ItemList', 'name': 'Máquinas Maxtool com vista explodida e peças de reposição',
                      'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'item': {
                          '@type': 'Product', 'name': f'{m["nome"]} {m["modelo"]}', 'model': m['modelo'],
                          'brand': {'@type': 'Brand', 'name': 'Maxtool'},
                          'image': f'{SITE}/assets/pecas/{m["slug"]}.svg'}} for i, m in enumerate(maquinas)]})
        nodes.append({'@type': 'HowTo', 'name': 'Como acionar a garantia de uma máquina Maxtool',
                      'step': [
                          {'@type': 'HowToStep', 'position': 1, 'name': 'Separe a nota fiscal',
                           'text': 'Tenha em mãos a nota fiscal de compra da máquina.'},
                          {'@type': 'HowToStep', 'position': 2, 'name': 'Fale com a Maxtool',
                           'text': f'Chame a Maxtool no WhatsApp {E["whatsapp"]} para orientar o processo.'},
                          {'@type': 'HowToStep', 'position': 3, 'name': 'Escolha o caminho',
                           'text': 'Leve a máquina a uma oficina perto de você ou envie direto para a Maxtool.'},
                          {'@type': 'HowToStep', 'position': 4, 'name': 'Avaliação',
                           'text': 'Se for defeito de fabricação, a Maxtool envia a peça sem custo e paga a mão de obra da oficina. Em caso de mau uso, peça e mão de obra ficam por conta do cliente.'}]})
    if p['slug'] == 'mtday':
        serie = {'@type': 'EventSeries', '@id': url + '#serie', 'name': 'Max Tool Day', 'url': url,
                 'description': dict(FAQS['mtday'])['O que é o Max Tool Day?'],
                 'organizer': {'@id': ORG_ID}, 'image': f'{SITE}/assets/instagram/maxtool-day.jpg'}
        nodes.append(serie)
        nodes.append({'@type': 'Event', 'name': f"Max Tool Day — {MTDAY['local']} ({MTDAY['cidade']}-{MTDAY['uf']})",
                      'startDate': MTDAY['data'], 'eventStatus': 'https://schema.org/EventScheduled',
                      'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode',
                      'superEvent': {'@id': url + '#serie'}, 'organizer': {'@id': ORG_ID},
                      'description': 'Capacitação presencial para marmoristas com demonstração ao vivo de corte, desbaste e polimento. O ingresso volta como voucher de compra na loja.',
                      'image': f'{SITE}/assets/instagram/maxtool-day.jpg',
                      'location': {'@type': 'Place', 'name': MTDAY['local'],
                                   'address': {'@type': 'PostalAddress', 'addressLocality': MTDAY['cidade'],
                                               'addressRegion': MTDAY['uf'], 'addressCountry': 'BR'}}})
    return {'@context': 'https://schema.org', '@graph': nodes}


# =====================================================================
# Montagem
# =====================================================================
def section(name):
    return (SRC / 'sections' / f'{name}.html').read_text()


def accent_dots(html):
    """O ponto final do título acompanha a cor da palavra anterior:
    palavra em destaque (vermelha) -> ponto vermelho; palavra branca -> ponto branco."""
    def fix(m):
        open_tag, inner, close = m.group(1), m.group(2), m.group(3)
        inner = re.sub(r'(<span class="red">[^<]*?)</span>\.(\s*)$', r'\1.</span>\2', inner)
        inner = re.sub(r'(?<!</span>)(?<=[^>\s])<span class="red">\.</span>', '.', inner)
        return open_tag + inner + close
    return re.sub(r'(<h[1-3][^>]*>)(.*?)(</h[1-3]>)', fix, html, flags=re.S)


def head_meta(p):
    url = SITE + p['path']
    t, d = esc(p['title']), esc(p['description'])
    return f'''  <title>{t}</title>
  <meta name="description" content="{d}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="pt-BR" href="{url}">
  <link rel="alternate" hreflang="x-default" href="{url}">
  <meta name="author" content="Maxtool">
  <meta name="geo.region" content="BR-{E['uf']}">
  <meta name="geo.placename" content="{E['cidade']}">
  <meta name="geo.position" content="{E['lat']};{E['lng']}">
  <meta name="ICBM" content="{E['lat']}, {E['lng']}">
  <link rel="icon" type="image/svg+xml" href="/assets/logos/favicon.svg">
  <link rel="icon" type="image/png" sizes="192x192" href="/assets/icons/icon-192.png">
  <link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#0b0c0e">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Maxtool">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{d}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Serra mármore Maxtool com disco diamantado">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{t}">
  <meta name="twitter:description" content="{d}">
  <meta name="twitter:image" content="{OG_IMAGE}">
  <link rel="alternate" type="text/plain" title="Resumo para IAs (llms.txt)" href="/llms.txt">'''


def gtm():
    if not GTM_ID:
        return ('  <!-- Google Tag Manager: defina GTM_ID em src/data.py (GA4, Meta Pixel e Hotjar entram pelo GTM) -->', '')
    head = f'''  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{GTM_ID}');</script>'''
    body = f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>'
    return head, body


def site_data():
    return '<script>window.MAXTOOL_DATA = "/assets/catalogo/produtos.json";</script>'


def produtos_json():
    campos = ('id', 'img', 'fallback', 'nome', 'cat', 'nivel', 'linha', 'disc', 'spec', 'desc', 'specs', 'materiais', 'pagina')
    return json.dumps({'produtos': [{k: p.get(k) for k in campos} for p in PRODUTOS]}, ensure_ascii=False, separators=(',', ':'))


def versao(arquivo):
    """Hash curto do arquivo para quebrar cache do navegador a cada build."""
    import hashlib
    return hashlib.md5((ROOT / arquivo).read_bytes()).hexdigest()[:8]


COMPONENTES = {'guia': guia_section, 'diferenciais': diferenciais_section, 'downloads': downloads_section}


def render(p, layout):
    parts, faq_items = [], []
    for b in p['body']:
        if b.lstrip().startswith('<'):
            parts.append(b)
        elif b in COMPONENTES:
            parts.append(COMPONENTES[b]())
        elif b.startswith('faq:'):
            faq_items = FAQS[b[4:]]
            parts.append(faq_section(b[4:]))
        else:
            parts.append(section(b))
    content = '\n'.join(parts)
    for k, fn in {'{{linha_completa}}': lambda: ''.join(f'<span>{esc(c)}</span>' for c in LINHA_COMPLETA),
                  '{{showcase_cards}}': showcase_cards, '{{etapas_panels}}': etapas_panels,
                  '{{reels}}': reels, '{{prod_grid}}': prod_grid, '{{grid_filtros}}': grid_filtros,
                  '{{total_produtos}}': lambda: str(len(PRODUTOS))}.items():
        if k in content:
            content = content.replace(k, fn())
    content = content.replace('{{updated}}', HOJE.isoformat()).replace('{{updated_br}}', HOJE.strftime('%d/%m/%Y'))
    content = content.replace('{{showcase_total}}', f'{len(DESTAQUES) + 1:02d}')
    if p['slug'] == 'home':
        content = re.sub(r'\s*<a [^>]*data-page-only[^>]*>.*?</a>', '', content, flags=re.S)
    else:
        content = re.sub(r'\s*<a [^>]*data-home-only[^>]*>.*?</a>', '', content, flags=re.S)
    # seção reaproveitada como topo de página: o primeiro <h2> vira <h1>
    if 'class="page-hero"' not in content and p['slug'] != 'home':
        content = re.sub(r'<h2( [^>]*)>(.*?)</h2>', r'<h1\1>\2</h1>', content, count=1, flags=re.S)

    cur = ' aria-current="page"'
    nav = '\n      '.join(f'<a href="{href}"{cur if href == p["path"] else ""}>{label}</a>' for href, label in NAV)
    g_head, g_body = gtm()
    jsonld = json.dumps(page_graph(p, faq_items), ensure_ascii=False, separators=(',', ':'))
    html = layout
    for k, v in {
        '{{gtm_head}}': g_head, '{{gtm_body}}': g_body,
        '{{head_meta}}': head_meta(p) + f'\n  <script type="application/ld+json">{jsonld}</script>',
        '{{> icons}}': section('icons'), '{{slug}}': p['slug'], '{{preload}}': p.get('preload', ''),
        '{{nav}}': nav, '{{cta_current}}': cur if p['path'] == '/seja-um-revendedor/' else '',
        '{{site_data}}': site_data(), '{{updated}}': HOJE.isoformat(), '{{updated_br}}': HOJE.strftime('%d/%m/%Y'),
        '{{content}}': content,
    }.items():
        html = html.replace(k, v)
    html = html.replace('href="/css/style.css"', f'href="/css/style.css?v={versao("css/style.css")}"')
    html = html.replace('src="/js/main.js"', f'src="/js/main.js?v={versao("js/main.js")}"')
    return accent_dots(html)


# =====================================================================
# Arquivos de SEO / GEO
# =====================================================================
def sitemap():
    prio = {'/': '1.0', '/produtos/': '0.9', '/seja-um-revendedor/': '0.9', '/onde-comprar/': '0.8',
            '/pecas/': '0.8', '/max-tool-day/': '0.7', '/sobre/': '0.7', '/contato/': '0.6', '/politica-de-privacidade/': '0.2'}
    imgs = {'/': ['produtos/serra-marmore-hero.webp'], '/produtos/': [p['fallback'].replace('/assets/', '', 1) for p in PRODUTOS],
            '/max-tool-day/': ['instagram/maxtool-day.jpg'], '/seja-um-revendedor/': ['produtos/catalogo-capa.jpg']}
    urls = []
    for p in PAGES:
        im = ''.join(f'\n    <image:image><image:loc>{SITE}/assets/{i}</image:loc></image:image>' for i in imgs.get(p['path'], []))
        urls.append(f'''  <url>
    <loc>{SITE}{p['path']}</loc>
    <lastmod>{HOJE.isoformat()}</lastmod>
    <changefreq>{'weekly' if p['path'] in ('/', '/produtos/') else 'monthly'}</changefreq>
    <priority>{prio[p['path']]}</priority>{im}
  </url>''')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + '\n'.join(urls) + '\n</urlset>\n')


def robots():
    bots = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-User', 'Claude-SearchBot',
            'anthropic-ai', 'PerplexityBot', 'Perplexity-User', 'Google-Extended', 'Applebot-Extended',
            'Bingbot', 'meta-externalagent', 'CCBot', 'Amazonbot', 'DuckAssistBot', 'cohere-ai', 'MistralAI-User']
    ai = '\n'.join(f'User-agent: {b}' for b in bots)
    return f'''# Maxtool — {SITE}
# Buscadores e assistentes de IA são bem-vindos: o conteúdo público pode ser lido e citado.

User-agent: *
Allow: /
Disallow: /api/
Disallow: /src/

# Assistentes e buscadores de IA (GEO)
{ai}
Allow: /
Disallow: /api/

Sitemap: {SITE}/sitemap.xml
'''


def llms_txt():
    pages = '\n'.join(f'- [{H.unescape(p["title"])}]({SITE}{p["path"]}): {p["description"]}' for p in PAGES)
    return f'''# Maxtool

> {E['resumo']}

Fatos principais:
- Nome: Maxtool (razão social {E['razao']}, CNPJ {E['cnpj']})
- Fundação: {E['fundacao']}, em Vitória/ES — começou com 5 produtos
- Sede: {E['rua']}, {E['cidade']} - {E['uf']}, CEP {E['cep']}
- Modelo de venda: só para revendas (não vende direto ao consumidor final); 250+ revendas parceiras no Brasil
- Linha: +1.000 itens em 3 níveis — {'; '.join(f'{n}: {d}' for n, d in NIVEIS)}
- Materiais atendidos: {', '.join(MATERIAIS)}
- Categorias: {', '.join(CATEGORIAS)}
- Linha completa: {', '.join(LINHA_COMPLETA)}
- Diferenciais: {'; '.join(f'{t} ({d})' for t, d in DIFERENCIAIS)}
- Evento: Max Tool Day — capacitação presencial para marmoristas dentro das revendas parceiras; próxima edição em {MTDAY['data_br']}, na {MTDAY['local']} ({MTDAY['cidade']}-{MTDAY['uf']}); o ingresso volta como voucher de compra
- Entrega: todo o Brasil, por transportadoras · pronta entrega dos principais produtos · pagamento a prazo conforme análise cadastral
- Atendimento: {E['horario']}
- Avaliações no Google: {E['avaliacoes']}
- Embaixadores técnicos: Almeida (@almeidamarmorista) e John, do Mil Grau (@marmorista_milgrau)
- Contato: WhatsApp {E['whatsapp']} · {E['email']} · telefone {E['telefone']} · Instagram {E['instagram']}

## Páginas
{pages}

## Documentos
- [Catálogo 2026 (PDF, 8 MB)]({SITE}/catalogo/maxtool-catalogo-2026-leve.pdf): linha completa por categoria e nível
- [Versão completa deste resumo]({SITE}/llms-full.txt): produtos, especificações, peças de reposição e perguntas frequentes

## Optional
- [Instagram @maxtoolbr]({E['instagram']}): ferramenta em ação, bastidores e Max Tool Day
'''


def llms_full():
    blocos = []
    for c in ORDEM_CATEGORIAS:
        itens = [p for p in PRODUTOS if p['cat'] == c]
        linhas = []
        for p in itens:
            nv = f" — nível {p['nivel']}" if p['nivel'] else (f" — linha {p['linha']}" if p['linha'] else '')
            mats = f"; materiais: {', '.join(p['materiais'])}" if p['materiais'] else ''
            esp = '; '.join(f'{k}: {v}' for k, v in p['specs'])
            linhas.append(f"- {p['nome']}{nv}. {esp}{mats}.")
        blocos.append(f'### {c} ({len(itens)})\n' + '\n'.join(linhas) + '\n')
    prods = '\n'.join(blocos)
    etapas = '\n'.join(f'- {e["nome"]}: {e["txt"]} Categorias: {", ".join(e["cats"])}.' for e in ETAPAS)
    maquinas = json.loads((ROOT / 'assets/pecas/pecas.json').read_text())
    pecas = '\n'.join(
        f'### {m["nome"]} {m["modelo"]}\nPDF: {SITE}/pecas/downloads/{m["slug"]}.pdf\n'
        + '\n'.join(f'- {x["ref"]}. {x["nome"]}' + (f' (código {x["cod"]})' if x.get('cod') else '') for x in m['pecas']) + '\n'
        for m in maquinas)
    vistos, faqs = set(), []
    for lista in FAQS.values():
        for q, a in lista:
            if q not in vistos:
                vistos.add(q)
                faqs.append(f'### {q}\n{a}\n')
    guia = '\n'.join(
        f'### {m["nome"]}\n{m["desafio"]}\n' + '\n'.join(
            f'- {etapa}: ' + ', '.join(f'{PROD[i]["nome"]} ({PROD[i]["spec"]})' if i in PROD else i for i in itens)
            for etapa, itens in m['etapas']) + '\n' for m in GUIA_MATERIAIS)
    erros = '\n'.join(f'- {t}: {d}' for t, d in ERROS_COMUNS)
    return llms_txt() + f'''
---

## A ferramenta certa para cada material
{guia}
### Erros comuns
{erros}

## Etapas do trabalho em rocha
{etapas}

## Produtos do catálogo ({len(PRODUTOS)} itens no site; +1.000 no catálogo completo)
{prods}
## Garantia
Toda máquina Maxtool tem garantia contra defeitos de fabricação (não cobre mau uso, desgaste natural, aplicação incorreta ou uso fora das recomendações do produto). Com a nota fiscal em mãos, fale primeiro com a Maxtool pelo WhatsApp {E['whatsapp']}.
1. Na oficina perto de você: o mecânico identifica o defeito. Defeito de fabricação → a Maxtool envia a peça sem custo e paga a mão de obra. Mau uso → peça e mão de obra por conta do cliente.
2. Direto com a Maxtool: envie a máquina; a Maxtool cuida da avaliação, reparo e retorno.

## Como ser revendedor
Para: revendas especializadas, distribuidores, lojas de ferramentas e lojas de materiais de construção que vendem para marmoraria. Requisitos: CNPJ com CNAE de revenda do ramo; loja física ou histórico de vendas no segmento; compromisso com pedidos recorrentes. O pedido mínimo varia conforme negociação, perfil e região. Cadastro: {SITE}/seja-um-revendedor/

## Peças de reposição (vista explodida)
{pecas}
## Perguntas frequentes
{''.join(faqs)}'''


def page_404(layout):
    p = dict(path='/404.html', slug='404', crumb=None, title='Página não encontrada | Maxtool',
             description='A página que você procurou não existe. Veja os produtos Maxtool, encontre uma revenda ou fale com a gente.',
             body=[page_hero('Erro 404', 'Essa peça<br>não está <span class="red">aqui</span>.',
                             'A página que você procurou mudou de lugar ou não existe. Escolha um caminho:', 'Página não encontrada',
                             '<div class="actions"><a class="btn btn-red" href="/">Ir para o início</a><a class="btn btn-ghost" href="/produtos/">Ver produtos</a><a class="btn btn-ghost" href="/onde-comprar/">Onde comprar</a></div>'),
                   'cta-band'])
    html = render(p, layout).replace('content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"', 'content="noindex, follow"')
    return re.sub(r'\s*<link rel="(canonical|alternate)"[^>]*>', '', html)


def manifest():
    return json.dumps({
        'name': 'Maxtool — Ferramentas para marmoraria', 'short_name': 'Maxtool', 'lang': 'pt-BR',
        'start_url': '/', 'display': 'standalone', 'background_color': '#0b0c0e', 'theme_color': '#0b0c0e',
        'icons': [{'src': '/assets/icons/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                  {'src': '/assets/icons/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
                  {'src': '/assets/logos/favicon.svg', 'sizes': 'any', 'type': 'image/svg+xml'}]},
        ensure_ascii=False, indent=2)


def build():
    layout = (SRC / 'layout.html').read_text()
    for p in PAGES:
        out = ROOT / p['path'].strip('/') / 'index.html'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(p, layout))
        print('ok', out.relative_to(ROOT))
    for name, txt in {'404.html': page_404(layout), 'sitemap.xml': sitemap(), 'robots.txt': robots(),
                      'llms.txt': llms_txt(), 'llms-full.txt': llms_full(), 'site.webmanifest': manifest(),
                      'assets/catalogo/produtos.json': produtos_json()}.items():
        (ROOT / name).write_text(txt)
        print('ok', name)


PUBLICAR = ['index.html', '404.html', 'robots.txt', 'sitemap.xml', 'llms.txt', 'llms-full.txt', 'site.webmanifest',
            'css', 'js', 'assets', 'catalogo', 'pecas/downloads']

VERCEL = {
    '$schema': 'https://openapi.vercel.sh/vercel.json',
    'cleanUrls': True,
    'trailingSlash': True,
    'headers': [
        {'source': '/(.*)', 'headers': [
            {'key': 'X-Content-Type-Options', 'value': 'nosniff'},
            {'key': 'Referrer-Policy', 'value': 'strict-origin-when-cross-origin'},
            {'key': 'X-Frame-Options', 'value': 'SAMEORIGIN'},
            {'key': 'Permissions-Policy', 'value': 'camera=(), microphone=(), geolocation=()'},
            {'key': 'Strict-Transport-Security', 'value': 'max-age=63072000; includeSubDomains'}]},
        {'source': '/(css|js)/(.*)', 'headers': [{'key': 'Cache-Control', 'value': 'public, max-age=31536000, immutable'}]},
        {'source': '/assets/(.*)', 'headers': [{'key': 'Cache-Control', 'value': 'public, max-age=2592000, stale-while-revalidate=86400'}]},
        {'source': '/(catalogo|pecas/downloads)/(.*)', 'headers': [{'key': 'Cache-Control', 'value': 'public, max-age=604800'}]},
        {'source': '/(llms.txt|llms-full.txt|robots.txt)', 'headers': [{'key': 'Content-Type', 'value': 'text/plain; charset=utf-8'}]},
    ],
}


def publicar():
    """Copia só o que vai para o ar em deploy/ (pasta para subir na Vercel)."""
    import shutil
    dest = ROOT / 'deploy'
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir()
    for item in PUBLICAR:
        src = ROOT / item
        if src.is_dir():
            shutil.copytree(src, dest / item, ignore=shutil.ignore_patterns('.DS_Store'))
        else:
            shutil.copy2(src, dest / item)
    for p in PAGES:
        if p['path'] != '/':
            d = p['path'].strip('/')
            (dest / d).mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / d / 'index.html', dest / d / 'index.html')
    cfg = json.dumps(VERCEL, indent=2, ensure_ascii=False) + '\n'
    (dest / 'vercel.json').write_text(cfg)
    (ROOT / 'vercel.json').write_text(cfg)  # deploy pelo GitHub (raiz do repo; .vercelignore tira src/ e deploy/)
    total = sum(f.stat().st_size for f in dest.rglob('*') if f.is_file())
    print(f'ok deploy/  ({sum(1 for f in dest.rglob("*") if f.is_file())} arquivos, {total / 1e6:.1f} MB)')


if __name__ == '__main__':
    build()
    publicar()
