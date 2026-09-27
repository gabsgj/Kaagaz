// Click every example chip on the ask page and assert each lands on a
// rendered checklist (not the researching view) with sources.
const puppeteer = require('puppeteer-core');
(async () => {
  const b = await puppeteer.launch({ executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless:'new', args:['--no-sandbox'] });
  const p = await b.newPage();
  await p.setViewport({ width: 1280, height: 900 });
  await p.goto('http://127.0.0.1:5000/', { waitUntil: 'networkidle0' });
  const chips = await p.$$eval('.chips a.chip', as => as.map(a => ({ href: a.getAttribute('href'), label: a.textContent.trim() })));
  console.log(`${chips.length} example chips found\n`);
  let ok = 0;
  for (const c of chips) {
    await p.goto('http://127.0.0.1:5000' + c.href.replace(/&amp;/g, '&'), { waitUntil: 'domcontentloaded' });
    const r = await p.evaluate(() => ({
      working: !!document.querySelector('.board--working'),
      steps: document.querySelectorAll('.step').length,
      sources: document.querySelectorAll('.sources__link').length,
      researchRecord: document.body.textContent.includes('Show the exact research record'),
    }));
    const good = !r.working && r.steps > 0 && r.sources > 0 && r.researchRecord;
    if (good) ok++;
    console.log(`  ${good ? 'ok  ' : 'FAIL'} ${c.label.padEnd(38)} ${r.steps} steps, ${r.sources} sources${r.working ? '  <-- HIT RESEARCH PATH' : ''}`);
  }
  console.log(`\n${ok}/${chips.length} chips served a complete, sourced checklist from cache.`);
  await b.close();
  process.exit(ok === chips.length ? 0 : 1);
})();
