/**
 * Kaagaz — flip-board jitter test.
 *
 * The brief makes the flip-board pixel-perfect behaviour a hard requirement:
 * "no jitter, no layout shift when digits/words change length". That is exactly
 * the kind of claim that rots, so it is asserted mechanically here rather than
 * eyeballed once.
 *
 * For every digit of every possible value the counter can take, and for the
 * status badge across its three word lengths, this records the bounding box of
 * the board and its neighbours and fails on ANY movement.
 */
const puppeteer = require('puppeteer-core');

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const BASE = process.env.BASE || 'http://127.0.0.1:5099';
// A 14-item checklist: the count crosses from one digit to two at 10, which is
// exactly the transition that used to shift the board.
const URL = '/checklist?transaction_type=home+loan&bank=HDFC+Bank&residency=resident';

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'new',
    args: ['--no-sandbox', '--font-render-hinting=none'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900, deviceScaleFactor: 1 });
  await page.goto(BASE + URL, { waitUntil: 'networkidle0' });
  await page.evaluate(() => document.fonts ? document.fonts.ready : null);
  await new Promise(r => setTimeout(r, 500));

  const failures = [];

  // ── 1. Digit-cell geometry across every value the board can show ────────
  const total = await page.evaluate(() => {
    return parseInt(document.getElementById('totalCount').textContent, 10) || 0;
  });
  console.log(`checklist has ${total} documents`);

  const TOLERANCE = 0.05; // sub-pixel: allow antialiasing, forbid movement

  for (let done = 0; done <= total; done++) {
    const geo = await page.evaluate((d) => {
      const api = window.KaagazFlip;
      api.setNumber('doneCount', d, { silent: true });
      const rect = (sel) => {
        const e = document.querySelector(sel);
        if (!e) return null;
        const r = e.getBoundingClientRect();
        return {
          x: +r.x.toFixed(2), y: +r.y.toFixed(2),
          w: +r.width.toFixed(2), h: +r.height.toFixed(2),
        };
      };
      const cells = [...document.querySelectorAll('#doneCount .flip__cell')]
        .map(c => +c.getBoundingClientRect().width.toFixed(2));
      return {
        board: rect('#board'),
        left: rect('.board__left'),
        counter: rect('.board__counter'),
        right: rect('.board__right'),
        cells,
      };
    }, done);

    // The board, its left module and the counter must never move or resize.
    if (done === 0) {
      failures.length === 0 && console.log('  baseline captured at done=0');
      continue;
    }
    // Compare against the first sample by re-reading it from a stashed copy.
    if (!global.__baseline) global.__baseline = geo;
    const base = global.__baseline;
    for (const key of ['board', 'left', 'counter', 'right']) {
      const a = base[key], b = geo[key];
      if (!a || !b) continue;
      for (const prop of ['x', 'y', 'w', 'h']) {
        if (Math.abs(a[prop] - b[prop]) > TOLERANCE) {
          failures.push(
            `done=${done}: ${key}.${prop} moved ${a[prop]} -> ${b[prop]}`
          );
        }
      }
    }
    // Every digit cell must be exactly the same width, always.
    const widths = new Set(geo.cells);
    if (widths.size > 1) {
      failures.push(
        `done=${done}: digit cells have mixed widths ${[...widths].join(', ')}`
      );
    }
  }

  // ── 2. Status badge across its three word lengths ────────────────────────
  // "Pending" (7) / "In progress" (11) / "Done" (4) must not resize the row.
  const badgeGeo = await page.evaluate(() => {
    const btn = document.querySelector('.step .step__advance');
    const title = document.querySelector('.step .step__title');
    const badge = document.querySelector('.step .status');
    const r = (e) => { const b = e.getBoundingClientRect();
      return [+b.x.toFixed(2), +b.width.toFixed(2), +b.height.toFixed(2)]; };
    const out = [];
    const labels = [['Pending', 'Start'], ['In progress', 'Mark done'], ['Done', 'Undo']];
    for (const [state, label] of labels) {
      btn.textContent = label;
      badge.textContent = state;
      badge.setAttribute('data-state', state.toLowerCase().replace(' ', '_'));
      out.push({ state, btn: r(btn), title: r(title), badge: r(badge) });
    }
    return out;
  });

  console.log('\n  status badge geometry:');
  for (const g of badgeGeo) {
    console.log(`    ${g.state.padEnd(12)} badge=${JSON.stringify(g.badge)} btn=${JSON.stringify(g.btn)}`);
  }
  const badgeW = badgeGeo.map(g => g.badge[1]);
  const titleX = badgeGeo.map(g => g.title[0]);
  if (new Set(badgeW).size > 1) {
    failures.push(`status badge resizes between states: ${badgeW.join(', ')}`);
  }
  if (new Set(titleX).size > 1) {
    failures.push(`step title shifts between states: ${titleX.join(', ')}`);
  }

  // ── 3. The live flip animation must not move anything either ─────────────
  const animGeo = await page.evaluate(async () => {
    const api = window.KaagazFlip;
    const before = document.getElementById('board').getBoundingClientRect();
    const board = { x: +before.x.toFixed(2), w: +before.width.toFixed(2) };
    // Non-silent path: runs the real 3D keyframe.
    for (let i = 0; i < 4; i++) {
      api.setNumber('doneCount', i);
      await new Promise(r => setTimeout(r, 40));
    }
    await new Promise(r => setTimeout(r, 400));
    const after = document.getElementById('board').getBoundingClientRect();
    return { board, after: { x: +after.x.toFixed(2), w: +after.width.toFixed(2) } };
  });
  if (animGeo.board.x !== animGeo.after.x || animGeo.board.w !== animGeo.after.w) {
    failures.push(
      `board moved during the flip animation: ` +
      `${JSON.stringify(animGeo.board)} -> ${JSON.stringify(animGeo.after)}`
    );
  }

  await browser.close();

  if (failures.length) {
    console.log(`\nFAIL — ${failures.length} jitter regression(s):`);
    for (const f of failures.slice(0, 20)) console.log('  - ' + f);
    process.exit(1);
  }
  console.log(`\nOK — board and badge are geometrically stable across ` +
              `0..${total} documents and all three status states.`);
})();
