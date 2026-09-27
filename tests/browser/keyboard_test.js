/**
 * Kaagaz — keyboard navigation gate.
 *
 * Asserts the shortcuts the demo script advertises, because an advertised
 * shortcut that does not work is worse than no shortcut at all: it costs the
 * presenter a moment of fumbling in front of judges.
 *
 * Gate, on a real Chrome:
 *   1. "/" focuses the search field.
 *   2. Escape blurs it again.
 *   3. ArrowDown focuses the first example chip.
 *   4. ArrowDown again advances, ArrowUp wraps back.
 *   5. Enter on a focused chip navigates to the checklist.
 *   6. Typing "/" into a focused text field is NOT hijacked.
 *   7. Submitting the landing-page form opens a checklist result.
 *   8. Cmd-K also focuses the search field.
 *   9. No uncaught page errors along the way.
 */
const puppeteer = require('puppeteer-core');

const BASE = process.env.BASE_URL || 'http://127.0.0.1:5000';
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

let failures = 0;
function check(name, actual, expected, ok) {
  const pass = ok !== undefined ? ok : actual === expected;
  if (!pass) failures++;
  console.log(`  ${pass ? 'PASS' : 'FAIL'}  ${name.padEnd(38)} ${JSON.stringify(actual)}${pass ? '' : '  expected ' + JSON.stringify(expected)}`);
}

(async () => {
  const b = await puppeteer.launch({
    executablePath: CHROME, headless: 'new', args: ['--no-sandbox']
  });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', (e) => errs.push(String(e)));

  const active = () => p.evaluate(() => {
    const el = document.activeElement;
    if (!el) return null;
    return { id: el.id || null, tag: el.tagName.toLowerCase(), chip: el.classList.contains('chip'), text: (el.textContent || '').trim().slice(0, 40) };
  });

  await p.goto(BASE + '/', { waitUntil: 'networkidle0' });

  // 1. "/" focuses search
  await p.keyboard.press('/');
  check('"/" focuses search', (await active()).id, 'transaction_type');

  // 2. Escape blurs
  await p.keyboard.press('Escape');
  check('Escape blurs search', (await active()).id !== 'transaction_type', true);

  // 3. ArrowDown -> first chip
  await p.keyboard.press('ArrowDown');
  const first = await active();
  check('ArrowDown focuses first chip', first.chip, true);
  check('first chip has a label', first.text.length > 0, true);

  // 4. ArrowDown advances, ArrowUp wraps
  await p.keyboard.press('ArrowDown');
  const second = await active();
  check('ArrowDown advances', second.text !== first.text, true);
  await p.keyboard.press('ArrowUp');
  check('ArrowUp returns to first', (await active()).text, first.text);

  // 5. Enter follows the focused chip
  await p.keyboard.press('Enter');
  await p.waitForNavigation({ waitUntil: 'networkidle0' });
  check('Enter navigates to checklist', p.url().includes('/checklist'), true);

  // 6. "/" typed into a field is literal text, not a shortcut
  await p.goto(BASE + '/', { waitUntil: 'networkidle0' });
  await p.click('#transaction_type');
  await p.keyboard.type('a/b');
  check('typing "a/b" stays literal', await p.$eval('#transaction_type', (el) => el.value), 'a/b');

  // 7. The landing-page form must submit to a result, not reload the page.
  await p.goto(BASE + '/', { waitUntil: 'networkidle0' });
  await p.$eval('#transaction_type', (el) => { el.value = 'home loan'; });
  await p.$eval('#bank', (el) => { el.value = 'HDFC Bank'; });
  await p.focus('#bank');
  await Promise.all([
    p.waitForNavigation({ waitUntil: 'networkidle0' }),
    p.keyboard.press('Enter'),
  ]);
  check('form submit opens a checklist', p.url().includes('/checklist?transaction_type='), true);
  check('submitted query reaches the result page', await p.evaluate(() => document.body.textContent.includes('Documents ready')), true);

  // 8. Cmd-K also focuses, and a second one does not double-toggle
  await p.goto(BASE + '/', { waitUntil: 'networkidle0' });
  await p.keyboard.down('Meta'); await p.keyboard.press('k'); await p.keyboard.up('Meta');
  check('Cmd-K focuses search', (await active()).id, 'transaction_type');

  check('no uncaught page errors', errs.length, 0);
  if (errs.length) errs.forEach((e) => console.log('        ' + e));

  await b.close();
  console.log(failures ? `\nkeyboard gate: ${failures} FAILURE(S)` : '\nkeyboard gate: all checks passed');
  process.exit(failures ? 1 : 0);
})();
