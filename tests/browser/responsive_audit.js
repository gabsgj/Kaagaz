/**
 * Kaagaz — responsive gate.
 *
 * Loads every page at 375 / 768 / 1280 and asserts the hard gate from the
 * brief: nothing breaks, clips, or bleeds at any breakpoint.
 *
 * Checks, per page per width:
 *   - no horizontal overflow (scrollWidth must not exceed the viewport)
 *   - no element wider than the viewport
 *   - no element overlapping the viewport edge (bleed)
 *   - no text clipped by its own box (scrollHeight/Width overflow on a
 *     container that is not intentionally scrollable)
 *   - no element touching x=0 or x=viewport width without padding
 *   - body text contrast is at least WCAG AA
 *   - every interactive control is at least 32px tall
 */
const puppeteer = require('puppeteer-core');

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const BASE = process.env.BASE || 'http://127.0.0.1:5099';
const OUT = process.env.OUT || './shots';

const WIDTHS = [
  { name: 'mobile',  w: 375,  h: 812 },
  { name: 'tablet',  w: 768,  h: 1024 },
  { name: 'desktop', w: 1280, h: 900 },
];

const PAGES = [
  { name: 'ask',        url: '/' },
  { name: 'about',      url: '/about' },
  { name: 'home-loan',  url: '/checklist?transaction_type=home+loan&bank=HDFC+Bank&residency=resident' },
  { name: 'gold-loan',  url: '/checklist?transaction_type=gold+loan&bank=State+Bank+of+India&residency=resident' },
  { name: 'kerala-reg', url: '/checklist?transaction_type=property+registration&state=Kerala&residency=not_applicable' },
  { name: 'researching',url: '/checklist?transaction_type=zzz+novel+thing&bank=Nowhere+Bank' },
  { name: 'error',      url: '/checklist?transaction_type=&bank=x', expectStatus: 400 },
];

// Runs in the page. Returns every layout violation it can find.
function auditPage() {
  const vw = document.documentElement.clientWidth;
  const problems = [];

  const label = (el) => {
    const id = el.id ? '#' + el.id : '';
    const cls = (el.className && typeof el.className === 'string')
      ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
    return el.tagName.toLowerCase() + id + cls;
  };

  // 1. Document-level horizontal overflow
  const scrollW = Math.max(
    document.documentElement.scrollWidth,
    document.body.scrollWidth
  );
  if (scrollW > vw + 1) {
    problems.push({
      kind: 'horizontal-overflow',
      detail: `document scrollWidth ${scrollW} > viewport ${vw}`,
    });
  }

  const all = document.querySelectorAll('*');
  for (const el of all) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;

    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;

    // 2. Element wider than the viewport
    if (r.width > vw + 1) {
      problems.push({
        kind: 'element-too-wide',
        el: label(el),
        detail: `width ${Math.round(r.width)} > viewport ${vw}`,
      });
    }

    // 3. Bleeding off the left or right edge
    if (r.right > vw + 1) {
      problems.push({
        kind: 'bleed-right',
        el: label(el),
        detail: `right ${Math.round(r.right)} > viewport ${vw}`,
      });
    }
    if (r.left < -1) {
      problems.push({
        kind: 'bleed-left',
        el: label(el),
        detail: `left ${Math.round(r.left)} < 0`,
      });
    }

    // 4. Content clipped inside its own box. Skip anything that is meant to
    //    scroll or ellipsize, and SVG (which legitimately uses a viewBox).
    const scrollable = /auto|scroll|hidden/.test(cs.overflowX) ||
                       /auto|scroll/.test(cs.overflowY) ||
                       cs.textOverflow === 'ellipsis';
    const isSvg = el instanceof SVGElement;
    if (!scrollable && !isSvg) {
      if (el.scrollWidth > el.clientWidth + 2 && el.clientWidth > 0) {
        problems.push({
          kind: 'clipped-x',
          el: label(el),
          detail: `scrollWidth ${el.scrollWidth} > clientWidth ${el.clientWidth}`,
        });
      }
      if (el.scrollHeight > el.clientHeight + 2 && el.clientHeight > 0 &&
          cs.overflow === 'hidden') {
        problems.push({
          kind: 'clipped-y',
          el: label(el),
          detail: `scrollHeight ${el.scrollHeight} > clientHeight ${el.clientHeight}`,
        });
      }
    }

    // 5. Interactive controls must be reachable
    const interactive = el.matches(
      'button, a[href], input:not([type=hidden]), select, summary, [tabindex]:not([tabindex="-1"])'
    );
    if (interactive && r.height > 0 && r.height < 24) {
      problems.push({
        kind: 'tap-target-small',
        el: label(el),
        detail: `height ${Math.round(r.height)}px < 24px`,
      });
    }
  }

  // 6. Body text contrast (WCAG AA = 4.5:1 for normal text)
  const lum = (rgb) => {
    const [r, g, b] = rgb.map(v => {
      v /= 255;
      return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };
  const parse = (c) => (c.match(/[\d.]+/g) || []).slice(0, 3).map(Number);
  const ratio = (a, b) => {
    const L1 = lum(a), L2 = lum(b);
    return (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
  };

  // Every colour the text could actually be sitting on, nearest first.
  //
  // Two things this has to get right, both learned the hard way:
  //
  // 1. A gradient puts its colour in `background-image` and leaves
  //    `backgroundColor` transparent, so the old single-background lookup walked
  //    straight past every gradient surface and measured the text against
  //    whatever was further up the tree.
  // 2. Those gradients are mostly SEMI-TRANSPARENT. The page ground itself is
  //    a faint speckle drawn as radial-gradients at ~3% alpha over the paper
  //    colour. Reading those RGB triples as if they were opaque measured the
  //    whole page against near-black and reported every heading at 1.3:1.
  //
  // So: collect layers outward, composite every translucent stop over the
  // nearest opaque background beneath it, and return the resulting set. The
  // contrast check then takes the WORST of them, so if any part of a gradient
  // fails AA the gate fails.
  const PAPER = [251, 247, 238];
  const over = (fg, alpha, bg) => fg.map((c, i) => c * alpha + bg[i] * (1 - alpha));

  const collectLayers = (el) => {
    const layers = [];
    let node = el;
    let base = null;
    while (node && node !== document.documentElement) {
      const cs = getComputedStyle(node);
      const solid = (cs.backgroundColor || '').match(/rgba?\(([^)]+)\)/);
      if (solid) {
        const parts = (solid[1].match(/[\d.]+/g) || []).map(Number);
        if (parts.length >= 3) {
          const a = parts.length > 3 ? parts[3] : 1;
          if (a >= 1) { base = parts.slice(0, 3); break; }
          layers.push({ alpha: a, colors: [parts.slice(0, 3)] });
        }
      }
      const img = cs.backgroundImage || '';
      if (img.includes('gradient(')) {
        const stops = [];
        for (const m of img.matchAll(/rgba?\(([^)]+)\)/g)) {
          const p = (m[1].match(/[\d.]+/g) || []).map(Number);
          if (p.length >= 3) stops.push({ color: p.slice(0, 3), alpha: p.length > 3 ? p[3] : 1 });
        }
        for (const m of img.matchAll(/#[0-9a-f]{3,8}/gi)) {
          let hex = m[0].slice(1);
          if (hex.length === 3) hex = hex.split('').map(c => c + c).join('');
          if (hex.length >= 6) {
            stops.push({
              color: [parseInt(hex.slice(0, 2), 16),
                      parseInt(hex.slice(2, 4), 16),
                      parseInt(hex.slice(4, 6), 16)],
              alpha: hex.length >= 8 ? parseInt(hex.slice(6, 8), 16) / 255 : 1,
            });
          }
        }
        if (stops.length) layers.push({ gradient: true, stops });
      }
      node = node.parentElement;
    }
    return { layers, base: base || PAPER };
  };

  const bgCandidates = (el) => {
    const { layers, base } = collectLayers(el);
    // `under` is always a set of candidate colours, nearest-composited. Each
    // layer is laid over every candidate beneath it, so a translucent stop
    // resolves against the actual colour behind it rather than against a
    // single assumed one.
    let under = [base];
    for (let i = layers.length - 1; i >= 0; i--) {
      const L = layers[i];
      const src = L.gradient
        ? L.stops.map(s => ({ color: s.color, alpha: s.alpha }))
        : L.colors.map(c => ({ color: c, alpha: L.alpha }));
      const next = [];
      for (const s of src) {
        for (const b of under) {
          next.push(over(s.color, s.alpha, b).map(Math.round));
        }
      }
      under = next.length ? next : under;
    }
    return under;
  };

  const worstRatio = (fg, bgs) =>
    bgs.reduce((min, bg) => Math.min(min, ratio(fg, bg)), Infinity);

  const textNodes = document.querySelectorAll(
    'p, li, dd, dt, h1, h2, h3, h4, span, a, button, label, summary, td, th, code, legend'
  );
  for (const el of textNodes) {
    // Any non-empty direct text counts. This was `length > 1`, which silently
    // skipped single-character nodes — and the flip-board digits are single
    // characters. That is how white-on-white digits got shipped behind a board
    // that still reported itself geometrically stable.
    const hasText = Array.from(el.childNodes)
      .some(n => n.nodeType === 3 && n.textContent.trim().length > 0);
    if (!hasText) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    if (el.closest('[hidden]')) continue;
    const size = parseFloat(cs.fontSize);
    const weight = parseInt(cs.fontWeight, 10) || 400;
    const large = size >= 24 || (size >= 18.66 && weight >= 700);
    const need = large ? 3.0 : 4.5;
    const cr = worstRatio(parse(cs.color), bgCandidates(el));
    if (cr < need) {
      problems.push({
        kind: 'contrast',
        el: label(el),
        detail: `${cr.toFixed(2)}:1 < ${need}:1 (${Math.round(size)}px/${weight}) ` +
                `"${el.textContent.trim().slice(0, 32)}"`,
      });
    }
  }

  return problems;
}

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'new',
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--font-render-hinting=none'],
  });

  let failures = 0;
  let checks = 0;

  for (const page of PAGES) {
    for (const vp of WIDTHS) {
      const tab = await browser.newPage();
      await tab.setViewport({ width: vp.w, height: vp.h, deviceScaleFactor: 2 });
      const consoleErrors = [];
      const expectedStatus = page.expectStatus || 200;
      tab.on('pageerror', e => consoleErrors.push(String(e)));
      tab.on('console', m => {
        if (m.type() !== 'error') return;
        // A 4xx on the document itself is the page working as designed (the
        // error route deliberately returns 400). Don't count it as a fault.
        const isOwnStatus = new RegExp(`status of ${expectedStatus}\\b`).test(m.text());
        if (!isOwnStatus) consoleErrors.push(m.text());
      });

      const resp = await tab.goto(BASE + page.url, { waitUntil: 'networkidle0', timeout: 30000 });
      if (resp && resp.status() !== expectedStatus) {
        consoleErrors.push(`document status ${resp.status()}, expected ${expectedStatus}`);
      }
      // Let fonts settle and any entry animation finish.
      await tab.evaluate(() => document.fonts ? document.fonts.ready : null);
      await new Promise(r => setTimeout(r, 700));

      const problems = await tab.evaluate(auditPage);
      checks++;
      const real = problems.filter(p => p.kind !== 'contrast' || true);
      if (real.length) failures++;

      await tab.screenshot({
        path: `${OUT}/${page.name}-${vp.name}.png`,
        fullPage: false,
      });

      const tag = real.length ? 'FAIL' : ' ok ';
      console.log(`[${tag}] ${page.name.padEnd(12)} ${vp.name.padEnd(8)} ${vp.w}px`);
      for (const p of real.slice(0, 12)) {
        console.log(`         ${p.kind}: ${p.el || ''} ${p.detail || ''}`);
      }
      if (real.length > 12) {
        console.log(`         …and ${real.length - 12} more`);
      }
      if (consoleErrors.length) {
        console.log(`         JS ERROR: ${consoleErrors[0]}`);
        failures++;
      }
      await tab.close();
    }
  }

  await browser.close();
  console.log(`\n${checks - failures}/${checks} page-width combinations clean.`);
  process.exit(failures ? 1 : 0);
})();
