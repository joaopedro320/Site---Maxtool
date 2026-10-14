/* =========================================================
   Maxtool — interações e animações
   ========================================================= */
(() => {
  'use strict';

  const WHATSAPP = '5527992019026';
  const ASSET = '/assets/';
  const REMOTE = ''; // PDFs servidos pelo próprio site
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = matchMedia('(pointer: fine)').matches;
  const waLink = (msg) => `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(msg)}`;
  const esc = (t) => String(t ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

  /* ---------- Rastreamento (GTM / GA4 / Meta Pixel, se instalados) ---------- */
  window.dataLayer = window.dataLayer || [];
  function track(event, params = {}) {
    window.dataLayer.push({ event, ...params });
    if (typeof window.gtag === 'function') window.gtag('event', event, params);
    if (typeof window.fbq === 'function') {
      if (event === 'generate_lead') window.fbq('track', 'Lead', params);
      else if (event === 'contact') window.fbq('track', 'Contact', params);
      else window.fbq('trackCustom', event, params);
    }
  }
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a');
    if (!a) return;
    if (a.dataset.track) track('cta_click', { cta: a.dataset.track });
    if (a.href.includes('wa.me/')) track('contact', { method: 'whatsapp', cta: a.dataset.track || 'link' });
    if (a.href.startsWith('tel:')) track('contact', { method: 'phone' });
    if (a.href.startsWith('mailto:')) track('contact', { method: 'email' });
  });

  /* ---------- Dados ---------- */
  // dados gerados pelo build (src/data.py) — HTML de produtos, etapas e reels já vem pronto na página
  // dados completos dos produtos (catálogo) — carregados só quando o modal é aberto
  let PRODUTOS = null;
  const carregarProdutos = () => PRODUTOS ? Promise.resolve(PRODUTOS)
    : fetch(window.MAXTOOL_DATA || '/assets/catalogo/produtos.json').then((r) => r.json()).then((d) => (PRODUTOS = d.produtos));

  /* ---------- Header, menu, progresso ---------- */
  const header = $('.site-header');
  const toggle = $('.nav-toggle');
  const nav = $('#menu');
  const bar = $('.progress span');
  let lastY = 0;
  function onScroll() {
    const y = scrollY;
    header.classList.toggle('is-solid', y > 40);
    header.classList.toggle('is-hidden', y > 500 && y > lastY && !nav.classList.contains('open'));
    lastY = y;
    const max = document.documentElement.scrollHeight - innerHeight;
    bar.style.transform = `scaleX(${max > 0 ? y / max : 0})`;
  }
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  const closeMenu = () => {
    nav.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Abrir menu');
    document.body.style.overflow = '';
  };
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    document.body.style.overflow = open ? 'hidden' : '';
  });
  $$('a', nav).forEach((a) => a.addEventListener('click', closeMenu));
  addEventListener('keydown', (e) => { if (e.key === 'Escape' && nav.classList.contains('open')) closeMenu(); });

  $('#ano').textContent = new Date().getFullYear();

  /* ---------- Marquees (duplica a faixa para loop contínuo) ---------- */
  $$('.marquee').forEach((m) => {
    const track = $('.marquee-track', m);
    const dur = Number(m.dataset.speed) || 40;
    for (let i = 0; i < 2; i++) {
      const c = track.cloneNode(true);
      c.setAttribute('aria-hidden', 'true');
      m.appendChild(c);
    }
    $$('.marquee-track', m).forEach((t) => t.style.setProperty('--dur', dur + 's'));
  });

  /* ---------- Reels (loop contínuo: o HTML já traz a faixa duplicada) ---------- */
  const reels = $('#reels');
  if (reels) {
    const kf = document.createElement('style');
    kf.textContent = '@keyframes reelsLoop { to { transform: translateX(-50%); } }';
    document.head.appendChild(kf);
    reels.style.animationName = 'reelsLoop';
  }

  const trackEl = $('#showcase-track');

  // grade com filtros + busca (/produtos/) — aceita ?cat=&material=&etapa=&nivel=&q= na URL
  const grid = $('#prod-grid');
  if (grid) {
    const cards = $$('.prod', grid);
    const busca = $('#busca-prod');
    const vazio = $('#busca-vazia');
    const nEl = $('#grid-n');
    const limpar = $('#grid-limpar');
    const sel = { cat: $('#f-cat'), material: $('#f-mat'), etapa: $('#f-etapa'), nivel: $('#f-nivel') };
    const norm = (t) => t.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    const params = new URLSearchParams(location.search);
    Object.entries(sel).forEach(([k, el]) => { if (el && params.get(k)) el.value = params.get(k); });
    if (busca && params.get('q')) busca.value = params.get('q');
    const aplicar = (animar) => {
      const f = Object.fromEntries(Object.entries(sel).map(([k, el]) => [k, el?.value || '']));
      const q = norm(busca?.value.trim() || '');
      const shown = cards.filter((c) => (!f.cat || c.dataset.cat === f.cat)
        && (!f.material || c.dataset.mats.split(' ').includes(f.material))
        && (!f.etapa || c.dataset.etapa === f.etapa)
        && (!f.nivel || c.dataset.nivel === f.nivel)
        && (!q || norm(c.textContent).includes(q)));
      cards.forEach((c) => c.classList.toggle('is-out', !shown.includes(c)));
      if (nEl) nEl.textContent = shown.length;
      if (vazio) vazio.hidden = shown.length > 0;
      const ativo = Object.values(f).some(Boolean) || !!q;
      if (limpar) limpar.hidden = !ativo;
      const u = new URL(location.href);
      Object.entries(f).forEach(([k, v]) => (v ? u.searchParams.set(k, v) : u.searchParams.delete(k)));
      q ? u.searchParams.set('q', busca.value.trim()) : u.searchParams.delete('q');
      history.replaceState(null, '', u);
      if (animar && window.gsap && !reduced) gsap.fromTo(shown.slice(0, 12), { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: .5, stagger: .04, ease: 'power3.out' });
    };
    Object.entries(sel).forEach(([k, el]) => el?.addEventListener('change', () => {
      aplicar(true);
      track('filter_products', { filtro: k, valor: el.value });
    }));
    limpar?.addEventListener('click', () => {
      Object.values(sel).forEach((el) => { if (el) el.value = ''; });
      if (busca) busca.value = '';
      aplicar(true);
    });
    let tBusca;
    busca?.addEventListener('input', () => {
      aplicar(false);
      clearTimeout(tBusca);
      tBusca = setTimeout(() => busca.value.trim() && track('search', { search_term: busca.value.trim(), tipo: 'produtos' }), 900);
    });
    if ([...params.keys()].length) aplicar(false);
  }

  // guia: filtros por etapa e nível dentro de cada material
  const LIMITE_GUIA = 9;
  $$('.guia-panel').forEach((panel) => {
    const gridG = $('.guia-grid', panel);
    if (!gridG) return;
    const cardsG = $$('.guia-card', gridG);
    const vertodos = $('.guia-vertodos', panel);
    const vazio = $('.guia-vazio', panel);
    const code = gridG.dataset.material;
    const st = { etapa: $('.gf-etapa.is-on', panel)?.dataset.etapa || '', eid: $('.gf-etapa.is-on', panel)?.dataset.eid || '', nivel: '' };
    const aplicar = (animar) => {
      const match = cardsG.filter((c) => c.dataset.etapa === st.etapa && (!st.nivel || c.dataset.nivel === st.nivel));
      cardsG.forEach((c) => { c.hidden = true; });
      match.slice(0, LIMITE_GUIA).forEach((c) => { c.hidden = false; });
      vazio.hidden = match.length > 0;
      vertodos.hidden = match.length <= LIMITE_GUIA;
      if (match.length > LIMITE_GUIA) {
        $('b', vertodos).textContent = match.length;
        vertodos.href = `/produtos/?material=${code}&etapa=${st.eid}${st.nivel ? '&nivel=' + st.nivel : ''}#destaques`;
      }
      if (animar && window.gsap && !reduced) gsap.fromTo(match.slice(0, LIMITE_GUIA), { y: 16, opacity: 0 }, { y: 0, opacity: 1, duration: .4, stagger: .03, ease: 'power3.out' });
    };
    const marcar = (sel, btn) => $$(sel, panel).forEach((x) => { x.classList.toggle('is-on', x === btn); x.setAttribute('aria-pressed', String(x === btn)); });
    $$('.gf-etapa', panel).forEach((btn) => btn.addEventListener('click', () => {
      st.etapa = btn.dataset.etapa; st.eid = btn.dataset.eid; marcar('.gf-etapa', btn); aplicar(true);
      track('filter_guia', { material: code, etapa: st.etapa });
    }));
    $$('.gf-nivel', panel).forEach((btn) => btn.addEventListener('click', () => {
      st.nivel = btn.dataset.nivel; marcar('.gf-nivel', btn); aplicar(true);
      track('filter_guia', { material: code, nivel: st.nivel || 'todos' });
    }));
    $('.gf-reset', panel)?.addEventListener('click', () => { st.nivel = ''; marcar('.gf-nivel', $('.gf-nivel', panel)); aplicar(true); });
    aplicar(false);
  });

  // guia "a ferramenta certa para cada material"
  const guiaTabs = $$('.guia-tabs [role="tab"]');
  if (guiaTabs.length) {
    const guiaPanels = $$('.guia-panel');
    const showMat = (i, focus) => {
      guiaTabs.forEach((t, k) => { t.setAttribute('aria-selected', String(k === i)); t.tabIndex = k === i ? 0 : -1; });
      guiaPanels.forEach((pn, k) => { pn.hidden = k !== i; });
      if (focus) guiaTabs[i].focus();
      if (window.gsap && !reduced) gsap.from($$('.guia-panel-head, .guia-filtros, .guia-card:not([hidden]), .guia-acts', guiaPanels[i]), { y: 20, opacity: 0, duration: .45, stagger: .06, ease: 'power3.out' });
      track('select_content', { content_type: 'material', item_id: guiaTabs[i].textContent.trim() });
    };
    guiaTabs.forEach((t, i) => {
      t.addEventListener('click', () => showMat(i));
      t.addEventListener('keydown', (e) => {
        const d = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
        if (d) { e.preventDefault(); showMat((i + d + guiaTabs.length) % guiaTabs.length, true); }
      });
    });
  }

  /* ---------- Modal ---------- */
  const modal = $('#produto-modal');
  async function openProduct(id) {
    let lista;
    try { lista = await carregarProdutos(); } catch { return; }
    const p = lista.find((x) => x.id === id);
    if (!p) return;
    const img = $('#modal-img');
    img.onerror = () => { img.onerror = null; img.src = p.fallback; };
    img.src = p.img;
    img.alt = p.nome;
    img.classList.toggle('is-disc', !!p.disc);
    const nv = $('#modal-nivel');
    const rotulo = p.nivel || (p.linha ? 'Linha ' + p.linha : 'Linha Maxtool');
    nv.textContent = rotulo;
    nv.className = 'tag' + (p.nivel ? ' is-' + p.nivel.toLowerCase() : '');
    $('#modal-cat').textContent = p.cat;
    $('#modal-nome').textContent = p.nome;
    $('#modal-desc').textContent = p.desc;
    const linhas = p.specs.map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`);
    if (p.materiais?.length) linhas.push(`<dt>Indicado para</dt><dd>${esc(p.materiais.join(', '))}</dd>`);
    if (p.pagina) linhas.push(`<dt>Catálogo 2026</dt><dd><a href="/catalogo/maxtool-catalogo-2026-leve.pdf#page=${p.pagina}" target="_blank" rel="noopener">página ${p.pagina}</a></dd>`);
    $('#modal-specs').innerHTML = linhas.join('');
    if (typeof modal.showModal === 'function') modal.showModal(); else modal.setAttribute('open', '');
    track('view_item', { item_id: p.id, item_name: p.nome, item_category: p.cat });
  }
  document.addEventListener('click', (e) => {
    const b = e.target.closest('[data-id]');
    if (b) openProduct(b.dataset.id);
  });
  modal.addEventListener('click', (e) => {
    if (e.target === modal || e.target.closest('[data-close]')) modal.close();
  });

  /* ---------- Etapas (painéis estáticos; abas alternam) ---------- */
  const etapaTabs = $$('.etapas-tabs [role="tab"]');
  if (etapaTabs.length) {
    const panels = $$('.etapa');
    const rail = $('.etapas-rail span');
    const showEtapa = (i, focus) => {
      etapaTabs.forEach((t, k) => { t.setAttribute('aria-selected', String(k === i)); t.tabIndex = k === i ? 0 : -1; });
      panels.forEach((pn, k) => { pn.hidden = k !== i; });
      if (focus) etapaTabs[i].focus();
      rail.style.transform = `translateY(${i * 100}%)`;
      if (window.gsap && !reduced) {
        gsap.from($$('.etapa-head, .etapa-cats span, .etapa-prod', panels[i]), { y: 24, opacity: 0, duration: .5, stagger: .04, ease: 'power3.out' });
      }
    };
    etapaTabs.forEach((t, i) => {
      t.addEventListener('click', () => showEtapa(i));
      t.addEventListener('keydown', (e) => {
        const d = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
        if (d) { e.preventDefault(); showEtapa((i + d + etapaTabs.length) % etapaTabs.length, true); }
      });
    });
  }

  /* ---------- Contadores ---------- */
  const fmt = new Intl.NumberFormat('pt-BR');
  function runCounter(el) {
    const end = Number(el.dataset.count);
    const prefix = el.dataset.prefix || '';
    const plain = el.hasAttribute('data-plain');
    const out = (v) => prefix + (plain ? String(v) : fmt.format(v));
    if (reduced) { el.textContent = out(end); return; }
    const start = plain ? Math.max(0, end - 40) : 0;
    const dur = 1600; const t0 = performance.now();
    const step = (t) => {
      const k = Math.min(1, (t - t0) / dur);
      const e = 1 - Math.pow(1 - k, 4);
      el.textContent = out(Math.round(start + (end - start) * e));
      if (k < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }
  const cio = new IntersectionObserver((entries) => {
    entries.forEach((en) => { if (en.isIntersecting) { runCounter(en.target); cio.unobserve(en.target); } });
  }, { threshold: .6 });
  $$('[data-count]').forEach((el) => cio.observe(el));

  /* ---------- Texto do manifesto (palavra a palavra) ---------- */
  const scrub = $('.scrub-text');
  let wordEls = [];
  if (scrub) {
    const words = scrub.textContent.trim().split(/\s+/);
    const hlUntil = words.findIndex((w) => w.includes('prateleira')) + 1;
    scrub.innerHTML = words.map((w, i) => `<span class="w${i < hlUntil ? ' hl' : ''}">${esc(w)}</span>`).join(' ');
    wordEls = $$('.w', scrub);
  }

  /* ---------- Radar das revendas ---------- */
  const dots = $('#mapa-dots');
  if (dots) {
    const pts = [[30, 22], [62, 18], [78, 34], [70, 52], [84, 60], [58, 70], [44, 82], [30, 64], [20, 44], [50, 40], [38, 30], [66, 84], [24, 76], [88, 46], [48, 58]];
    dots.innerHTML = pts.map(([x, y], i) => `<i style="left:${x}%;top:${y}%;animation-delay:${(i * .37) % 2.4}s"></i>`).join('') + '<i class="hq" style="left:72%;top:60%"></i>';
  }

  /* ---------- Faíscas do disco (hero) ---------- */
  function sparks() {
    const cv = $('#sparks');
    if (!cv || reduced) return;
    const ctx = cv.getContext('2d');
    let w, h, dpr, parts = [], run = true;
    const resize = () => { dpr = Math.min(2, devicePixelRatio || 1); w = cv.clientWidth; h = cv.clientHeight; cv.width = w * dpr; cv.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); };
    resize(); addEventListener('resize', resize);
    new IntersectionObserver(([e]) => { run = e.isIntersecting; if (run) loop(); }).observe(cv);
    function spawn() {
      // ponto de contato do disco com a peça (canto inferior esquerdo da serra)
      const ox = w * .13, oy = h * .86;
      for (let i = 0; i < 4; i++) {
        const a = Math.PI * (1.02 + Math.random() * .32);
        const s = 4 + Math.random() * 9;
        parts.push({ x: ox, y: oy, vx: Math.cos(a) * s, vy: Math.sin(a) * s * .55 - Math.random() * 2, life: 1, len: 6 + Math.random() * 14 });
      }
    }
    function loop() {
      if (!run) return;
      ctx.clearRect(0, 0, w, h);
      spawn();
      parts = parts.filter((p) => p.life > 0);
      for (const p of parts) {
        p.vy += .32; p.x += p.vx; p.y += p.vy; p.life -= .022;
        const g = ctx.createLinearGradient(p.x, p.y, p.x - p.vx * p.len * .2, p.y - p.vy * p.len * .2);
        g.addColorStop(0, `rgba(255,${200 + Math.random() * 55 | 0},140,${p.life})`);
        g.addColorStop(1, 'rgba(228,33,58,0)');
        ctx.strokeStyle = g; ctx.lineWidth = 1.6;
        ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(p.x - p.vx * p.len * .2, p.y - p.vy * p.len * .2); ctx.stroke();
      }
      requestAnimationFrame(loop);
    }
    loop();
  }
  sparks();

  /* ---------- Tilt e botões magnéticos ---------- */
  if (finePointer && !reduced) {
    $$('.tilt').forEach((el) => {
      el.addEventListener('pointermove', (e) => {
        const r = el.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - .5;
        const y = (e.clientY - r.top) / r.height - .5;
        el.style.transform = `perspective(900px) rotateY(${x * 10}deg) rotateX(${-y * 10}deg) translateZ(0)`;
      });
      el.addEventListener('pointerleave', () => { el.style.transform = ''; });
    });
    $$('.magnetic').forEach((el) => {
      el.addEventListener('pointermove', (e) => {
        const r = el.getBoundingClientRect();
        el.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * .2}px, ${(e.clientY - r.top - r.height / 2) * .3}px)`;
      });
      el.addEventListener('pointerleave', () => { el.style.transform = ''; });
    });
    const hero = $('.hero');
    if (hero) {
      const hv = $('.hero-visual');
      const hp = $('.hero-produto');
      hero.addEventListener('pointermove', (e) => {
        const x = e.clientX / innerWidth - .5, y = e.clientY / innerHeight - .5;
        hp.style.translate = `${x * -24}px ${y * -18}px`;
        hv.style.rotate = `${x * 2}deg`;
      });
    }
  }

  /* ---------- Animações GSAP ---------- */
  function initGsap() {
    const showcase = $('.showcase');
    const viewport = showcase && $('.showcase-viewport');
    const cards = trackEl ? $$('.prod, .prod-end', trackEl) : [];
    const setProgress = (k) => {
      $('.showcase-bar span').style.transform = `scaleX(${k})`;
      $('.showcase-count b').textContent = String(Math.min(cards.length, Math.round(k * (cards.length - 1)) + 1)).padStart(2, '0');
    };
    const nativeShowcase = () => {
      showcase.classList.add('no-pin');
      const h = () => setProgress(viewport.scrollLeft / Math.max(1, viewport.scrollWidth - viewport.clientWidth));
      viewport.addEventListener('scroll', h, { passive: true });
      return () => { showcase.classList.remove('no-pin'); viewport.removeEventListener('scroll', h); };
    };

    if (!window.gsap || !window.ScrollTrigger || reduced) {
      $$('.reveal, .reveal-stagger > *').forEach((el) => { el.style.opacity = 1; el.style.transform = 'none'; });
      wordEls.forEach((w) => w.classList.add('on'));
      if (showcase) nativeShowcase();
      return;
    }
    gsap.registerPlugin(ScrollTrigger);
    const has = (s) => !!$(s);

    // intro da home
    if (has('.hero')) {
      const tl = gsap.timeline({ defaults: { ease: 'power4.out' } });
      tl.from('.hero-title .line > span', { yPercent: 110, duration: 1.1, stagger: .1 })
        .from('.hero .eyebrow, .hero-sub, .hero .actions, .hero-chips', { y: 30, opacity: 0, duration: .9, stagger: .08 }, '-=.7')
        .from('.hero-produto', { x: 120, opacity: 0, rotate: 6, duration: 1.4 }, .1)
        .from('.spec-tag', { scale: .6, opacity: 0, duration: .6, stagger: .12, ease: 'back.out(2)' }, '-=.7');
      const sc = { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true };
      gsap.to('.hero-visual', { yPercent: 18, ease: 'none', scrollTrigger: sc });
      gsap.to('.hero-copy', { yPercent: 30, opacity: .2, ease: 'none', scrollTrigger: { ...sc } });
      gsap.to('.hero-disc', { scale: 1.3, ease: 'none', scrollTrigger: { ...sc } });
    }

    // intro das páginas internas
    if (has('.page-hero')) {
      gsap.timeline({ defaults: { ease: 'power4.out' } })
        .from('.page-hero .crumbs, .page-hero .eyebrow', { y: 20, opacity: 0, duration: .7, stagger: .08 })
        .from('.page-title', { yPercent: 40, opacity: 0, duration: 1.1 }, '-=.4')
        .from('.page-hero .lead, .page-hero .actions', { y: 30, opacity: 0, duration: .8, stagger: .1 }, '-=.7')
        .from('.page-hero-bg img', { scale: .6, opacity: 0, duration: 1.6 }, 0);
    }
    const firstH1 = $('main > section:first-child h1:not(.hero-title):not(.page-title):not(.mtday-title)');
    if (firstH1) gsap.from(firstH1, { y: 60, opacity: 0, duration: 1.1, ease: 'power4.out' });

    // manifesto palavra a palavra
    if (scrub) {
      ScrollTrigger.create({
        trigger: scrub, start: 'top 80%', end: 'bottom 45%', scrub: true,
        onUpdate: (st) => {
          const n = Math.round(st.progress * wordEls.length);
          wordEls.forEach((w, i) => w.classList.toggle('on', i < n));
        },
      });
    }

    // reveals
    ScrollTrigger.batch('.reveal', {
      start: 'top 88%', once: true,
      onEnter: (els) => gsap.to(els, { opacity: 1, y: 0, duration: .9, stagger: .1, ease: 'power3.out' }),
    });
    $$('.reveal-stagger').forEach((g) => {
      gsap.to(g.children, { opacity: 1, y: 0, duration: .6, stagger: .04, ease: 'power3.out', scrollTrigger: { trigger: g, start: 'top 85%', once: true } });
    });
    gsap.utils.toArray('section h2:not(.scrub-text):not(.mtday-title)').forEach((h) => {
      gsap.from(h, { y: 50, opacity: 0, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: h, start: 'top 88%', once: true } });
    });

    // níveis
    if (has('.tiers')) {
      gsap.from('.tier-meter span', { scaleX: 0, duration: .6, stagger: .08, ease: 'power2.out', scrollTrigger: { trigger: '.tiers', start: 'top 80%', once: true } });
      gsap.from('.tier', { y: 60, opacity: 0, duration: .9, stagger: .12, ease: 'power3.out', clearProps: 'transform', scrollTrigger: { trigger: '.tiers', start: 'top 85%', once: true } });
    }
    if (grid) gsap.from($$('.prod', grid), { y: 50, opacity: 0, duration: .8, stagger: .06, ease: 'power3.out', scrollTrigger: { trigger: grid, start: 'top 85%', once: true } });
    if (has('.cta-grid')) gsap.from('.cta-card', { y: 60, opacity: 0, duration: .9, stagger: .12, ease: 'power3.out', clearProps: 'transform', scrollTrigger: { trigger: '.cta-grid', start: 'top 85%', once: true } });

    // Max Tool Day
    if (has('.mtday')) {
      gsap.from('.mtday-title', { yPercent: 30, opacity: 0, duration: 1.2, ease: 'power4.out', scrollTrigger: { trigger: '.mtday', start: 'top 70%', once: true } });
      gsap.to('.mtday-stripes', { backgroundPosition: '300px 0', ease: 'none', scrollTrigger: { trigger: '.mtday', start: 'top bottom', end: 'bottom top', scrub: true } });
    }

    // vitrine: horizontal pinado no desktop, rolagem nativa no mobile
    if (showcase) {
      const discImgs = $$('.prod.is-disc .prod-media img', trackEl);
      const mm = gsap.matchMedia();
      mm.add('(min-width: 901px)', () => {
        const dist = () => Math.max(0, trackEl.scrollWidth - innerWidth);
        const tween = gsap.to(trackEl, {
          x: () => -dist(), ease: 'none',
          scrollTrigger: {
            trigger: showcase, start: 'top top', end: () => '+=' + dist(), pin: true, scrub: .6, invalidateOnRefresh: true, anticipatePin: 1,
            onUpdate: (st) => {
              setProgress(st.progress);
              discImgs.forEach((im, i) => { im.style.rotate = `${st.progress * 540 * (i % 2 ? -1 : 1)}deg`; });
            },
          },
        });
        cards.forEach((c) => {
          gsap.from(c.querySelector('.prod-media img') || c, { scale: .7, opacity: .3, ease: 'none', scrollTrigger: { trigger: c, containerAnimation: tween, start: 'left 100%', end: 'left 55%', scrub: true } });
        });
        return () => { discImgs.forEach((im) => { im.style.rotate = ''; }); };
      });
      mm.add('(max-width: 900px)', nativeShowcase);
    }

    addEventListener('load', () => ScrollTrigger.refresh());
  }
  initGsap(); // scripts com defer: GSAP já carregou antes deste arquivo

  /* ---------- Peças: vista explodida com zoom/arraste ---------- */
  const vista = $('#vista');
  if (vista) {
    const stage = $('#vista-stage');
    const vImg = $('#vista-img');
    const vLoad = $('#vista-loading');
    const busca = $('#busca-peca');
    let maquinas = [], atual = null;
    const view = { s: 1, x: 0, y: 0, min: .1, max: 2 };
    const apply = () => { stage.style.transform = `translate(${view.x}px, ${view.y}px) scale(${view.s})`; };
    function fit() {
      if (!atual) return;
      const r = vista.getBoundingClientRect();
      view.s = Math.min(r.width / atual.w, r.height / atual.h) * .94;
      view.min = view.s * .8; view.max = view.s * 8;
      view.x = (r.width - atual.w * view.s) / 2;
      view.y = (r.height - atual.h * view.s) / 2;
      apply();
    }
    function zoomAt(f, cx, cy) {
      const ns = Math.min(view.max, Math.max(view.min, view.s * f));
      const k = ns / view.s;
      view.x = cx - (cx - view.x) * k; view.y = cy - (cy - view.y) * k; view.s = ns;
      apply();
    }
    function renderPecas(q = '') {
      if (!atual) return;
      const t = q.trim().toLowerCase();
      const hasCod = atual.pecas.some((p) => p.cod), hasQtd = atual.pecas.some((p) => p.qtd);
      $('#col-extra').textContent = hasCod ? 'Código' : hasQtd ? 'Qtd.' : '';
      const rows = atual.pecas
        .filter((p) => !t || p.nome.toLowerCase().includes(t) || String(p.ref) === t)
        .map((p) => `<tr><td>${esc(p.ref)}</td><td>${esc(p.nome)}</td><td>${esc(p.cod ?? p.qtd ?? '')}</td></tr>`);
      $('#pecas-corpo').innerHTML = rows.join('') || '<tr><td colspan="3">Nenhuma peça com esse nome nesta máquina.</td></tr>';
    }
    function selectMaquina(m) {
      atual = m;
      $$('.maquina-tab').forEach((t) => { const on = t.dataset.slug === m.slug; t.classList.toggle('is-ativa', on); t.setAttribute('aria-selected', String(on)); });
      vLoad.classList.remove('is-off');
      vImg.onload = () => { vLoad.classList.add('is-off'); fit(); };
      vImg.width = m.w; vImg.height = m.h;
      vImg.alt = `Vista explodida — ${m.nome} ${m.modelo}`;
      vImg.src = ASSET + 'pecas/' + m.slug + '.svg';
      busca.value = '';
      renderPecas();
      const pdf = $('#baixar-pdf');
      pdf.href = `${REMOTE}/pecas/downloads/${m.slug}.pdf`;
      pdf.dataset.track = 'pdf_pecas_' + m.slug;
    }
    // carrega a vista só quando a seção se aproxima
    new IntersectionObserver(([e], obs) => {
      if (!e.isIntersecting) return;
      obs.disconnect();
      fetch(ASSET + 'pecas/pecas.json').then((r) => r.json()).then((d) => {
        maquinas = d;
        $('#maquina-tabs').innerHTML = d.map((m) => `<button class="maquina-tab" role="tab" data-slug="${m.slug}" aria-selected="false">${esc(m.nome)} <em>${esc(m.modelo)}</em></button>`).join('');
        $$('.maquina-tab').forEach((b) => b.addEventListener('click', () => selectMaquina(maquinas.find((m) => m.slug === b.dataset.slug))));
        selectMaquina(d[0]);
      }).catch(() => { vLoad.textContent = 'Não foi possível carregar a vista agora.'; });
    }, { rootMargin: '400px' }).observe(vista);
    busca.addEventListener('input', () => renderPecas(busca.value));
    vista.addEventListener('wheel', (e) => {
      e.preventDefault();
      const r = vista.getBoundingClientRect();
      zoomAt(e.deltaY < 0 ? 1.15 : 1 / 1.15, e.clientX - r.left, e.clientY - r.top);
    }, { passive: false });
    const ptrs = new Map(); let pinch = 0;
    vista.addEventListener('pointerdown', (e) => {
      if (e.target.closest('.vista-ctrl')) return;
      vista.setPointerCapture(e.pointerId); ptrs.set(e.pointerId, { x: e.clientX, y: e.clientY });
    });
    vista.addEventListener('pointermove', (e) => {
      if (!ptrs.has(e.pointerId)) return;
      const prev = ptrs.get(e.pointerId);
      ptrs.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (ptrs.size === 2) {
        const [a, b] = [...ptrs.values()];
        const d = Math.hypot(a.x - b.x, a.y - b.y);
        if (pinch) { const r = vista.getBoundingClientRect(); zoomAt(d / pinch, (a.x + b.x) / 2 - r.left, (a.y + b.y) / 2 - r.top); }
        pinch = d;
      } else {
        view.x += e.clientX - prev.x; view.y += e.clientY - prev.y; apply();
      }
    });
    const up = (e) => { ptrs.delete(e.pointerId); if (ptrs.size < 2) pinch = 0; };
    vista.addEventListener('pointerup', up); vista.addEventListener('pointercancel', up);
    $$('.vista-ctrl button').forEach((b) => b.addEventListener('click', () => {
      const r = vista.getBoundingClientRect();
      if (b.dataset.zoom === 'reset') fit(); else zoomAt(b.dataset.zoom === 'in' ? 1.4 : 1 / 1.4, r.width / 2, r.height / 2);
    }));
    addEventListener('resize', () => atual && fit());
  }

  /* ---------- Máscaras ---------- */
  const masks = {
    tel: (d) => { d = d.slice(0, 11); const c = d.length > 10 ? 7 : 6; return d.length > 6 ? `(${d.slice(0, 2)}) ${d.slice(2, c)}-${d.slice(c)}` : d.length > 2 ? `(${d.slice(0, 2)}) ${d.slice(2)}` : d; },
    cnpj: (d) => { d = d.slice(0, 14); return d.replace(/^(\d{2})(\d)/, '$1.$2').replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3').replace(/\.(\d{3})(\d)/, '.$1/$2').replace(/(\d{4})(\d)/, '$1-$2'); },
    cep: (d) => { d = d.slice(0, 8); return d.length > 5 ? `${d.slice(0, 5)}-${d.slice(5)}` : d; },
  };
  document.addEventListener('input', (e) => {
    const m = e.target.dataset?.mask || (e.target.id === 'cep' ? 'cep' : null);
    if (m && masks[m]) e.target.value = masks[m](e.target.value.replace(/\D/g, ''));
    if (e.target.classList?.contains('is-invalid')) e.target.classList.remove('is-invalid');
    e.target.closest?.('.pills')?.classList.remove('is-invalid');
  });

  function validCnpj(v) {
    const c = v.replace(/\D/g, '');
    if (c.length !== 14 || /^(\d)\1+$/.test(c)) return false;
    const calc = (n) => { let s = 0, p = n - 7; for (let i = 0; i < n; i++) { s += c[i] * p--; if (p < 2) p = 9; } const r = s % 11; return r < 2 ? 0 : 11 - r; };
    return calc(12) === +c[12] && calc(13) === +c[13];
  }
  function validate(scope) {
    let ok = true; let first = null;
    $$('input[required]', scope).forEach((inp) => {
      let bad;
      if (inp.type === 'radio') {
        bad = !$(`input[name="${inp.name}"]:checked`, scope);
        if (bad) inp.closest('.pills')?.classList.add('is-invalid');
      } else {
        const v = inp.value.trim();
        bad = !v || (inp.type === 'email' && !/^\S+@\S+\.\S+$/.test(v))
          || (inp.dataset.mask === 'tel' && v.replace(/\D/g, '').length < 10)
          || (inp.dataset.mask === 'cnpj' && !validCnpj(v));
        inp.classList.toggle('is-invalid', bad);
      }
      if (bad) { ok = false; first = first || inp; }
    });
    if (first) {
      const target = first.type === 'radio' ? first.closest('.pills') : first;
      target.scrollIntoView({ behavior: 'smooth', block: 'center' });
      if (first.type !== 'radio') first.focus({ preventScroll: true });
    }
    return ok;
  }

  /* ---------- Formulários (revenda / oficina) ---------- */
  const LABELS = { nome: 'Nome', loja: 'Loja', oficina: 'Oficina', cnpj: 'CNPJ', cidade: 'Cidade/UF', whatsapp: 'WhatsApp', email: 'E-mail', tipo: 'Tipo de empresa', perfil: 'Vende para marmorarias', loja_fisica: 'Loja física', volume: 'Compra mensal', marcas: 'Marcas que revende' };
  const VALORES = { revenda: 'Revenda especializada', distribuidor: 'Distribuidor', ferramentas: 'Loja de ferramentas', construcao: 'Materiais de construção', principal: 'Sim, é o foco', parte: 'Sim, parte das vendas', nao: 'Ainda não', sim: 'Sim', online: 'Só online', abrindo: 'Abrindo', 'ate-5k': 'Até R$ 5 mil', '5-20k': 'R$ 5 a 20 mil', '20k+': 'Acima de R$ 20 mil' };
  $$('form[data-endpoint]').forEach((form) => {
    const status = $('.form-status', form);
    const steps = $$('.step', form);
    const dotsEl = $$('.steps span', form);
    const go = (n) => {
      steps.forEach((s, i) => s.classList.toggle('is-on', i === n));
      dotsEl.forEach((d, i) => d.classList.toggle('on', i <= n));
      if (n === 1) track('form_step', { form: form.dataset.lead, step: 2 });
    };
    $('[data-next]', form)?.addEventListener('click', () => { if (validate(steps[0])) go(1); });
    $('[data-prev]', form)?.addEventListener('click', () => go(0));
    let started = false;
    form.addEventListener('focusin', () => { if (!started) { started = true; track('form_start', { form: form.dataset.lead }); } });

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (steps.length && !validate(steps[0])) { go(0); return; }
      if (!validate(form)) return;
      const btn = $('button[type="submit"]', form);
      const label = btn.innerHTML;
      const dados = Object.fromEntries(new FormData(form));
      dados.origem = 'site-v2';
      const utm = new URLSearchParams(location.search);
      ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid', 'fbclid'].forEach((k) => { if (utm.get(k)) dados[k] = utm.get(k); });
      btn.disabled = true; btn.textContent = 'Enviando…';
      status.className = 'form-status'; status.textContent = '';
      try {
        const r = await fetch(form.dataset.endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(dados) });
        if (r.status === 429) throw new Error('rate');
        if (!r.ok) throw new Error('HTTP ' + r.status);
        track('generate_lead', { form: form.dataset.lead, tipo: dados.tipo || '', perfil: dados.perfil || '', volume: dados.volume || '', regiao: dados.cidade || '' });
        form.innerHTML = `<div class="form-ok"><h3>Cadastro recebido!</h3><p>Nossa equipe ${form.dataset.lead === 'oficina' ? 'técnica' : 'comercial'} entra em contato em breve pelo WhatsApp informado.</p></div>`;
      } catch (err) {
        const resumo = Object.entries(dados).filter(([k, v]) => v && LABELS[k]).map(([k, v]) => `${LABELS[k]}: ${VALORES[v] || v}`).join('\n');
        status.innerHTML = (err.message === 'rate' ? 'Muitos envios seguidos. ' : 'Não deu para enviar por aqui agora. ')
          + `<a href="${waLink(form.dataset.wa + '\n\n' + resumo)}" target="_blank" rel="noopener">Envie pelo WhatsApp</a> — os seus dados já vão preenchidos.`;
        status.classList.add('err');
        btn.disabled = false; btn.innerHTML = label;
      }
    });
  });

  /* ---------- Onde comprar (CEP) ---------- */
  const cepForm = $('#cep-form');
  if (cepForm) {
    const cepStatus = $('#cep-status');
    const lojas = $('#lojas');
    cepForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const cep = $('#cep').value.replace(/\D/g, '');
      cepStatus.className = 'form-status'; lojas.innerHTML = '';
      if (cep.length !== 8) { cepStatus.textContent = 'Digite os 8 números do seu CEP.'; cepStatus.classList.add('err'); return; }
      const btn = $('#cep-buscar'); btn.disabled = true; btn.textContent = 'Buscando…';
      track('search', { search_term: 'cep', tipo: 'onde_comprar' });
      const semLoja = (cidade) => `
        <article class="loja-card"><b>Ainda não temos revenda pertinho de você${cidade ? ' (' + esc(cidade) + ')' : ''}</b>
        <span>Fala com a gente: indicamos a revenda mais próxima ou onde comprar Maxtool online.</span>
        <div class="acts"><a href="${waLink(`Olá! Não encontrei um revendedor Maxtool perto de mim (CEP ${cep}). Pode me indicar onde comprar?`)}" target="_blank" rel="noopener">Chamar no WhatsApp →</a></div></article>`;
      try {
        const r = await fetch('/api/onde-comprar', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ cep, website: $('#oc-website').value }) });
        if (r.status === 404) { cepStatus.textContent = 'Não encontramos esse CEP. Confere os números?'; cepStatus.classList.add('err'); return; }
        if (r.status === 429) { cepStatus.textContent = 'Muitas consultas seguidas — aguarde alguns minutos.'; cepStatus.classList.add('err'); return; }
        if (!r.ok) throw new Error('HTTP ' + r.status);
        const d = await r.json();
        lojas.innerHTML = d.lojas?.length
          ? d.lojas.map((l, i) => `<article class="loja-card" style="animation-delay:${i * .08}s"><b>${esc(l.nome)}</b><span>${esc(l.cidade)}${l.dist != null ? ` · a ${esc(l.dist)} km de você` : ''}</span><div class="acts">${l.whatsapp ? `<a href="https://wa.me/${esc(String(l.whatsapp).replace(/\D/g, ''))}?text=${encodeURIComponent('Olá! Vi no site da Maxtool que vocês revendem a marca.')}" target="_blank" rel="noopener" data-track="loja_whatsapp">WhatsApp →</a>` : ''}${l.tel ? `<a href="tel:${esc(String(l.tel).replace(/\D/g, ''))}">${esc(l.tel)}</a>` : ''}</div></article>`).join('')
          : semLoja(d.cidade);
      } catch {
        lojas.innerHTML = semLoja('');
      } finally {
        btn.disabled = false; btn.textContent = 'Localizar';
      }
    });
  }
})();
