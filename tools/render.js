const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
(async () => {
  const [,, inp, out, title] = process.argv;
  const W = path.dirname(inp);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + inp, { waitUntil: 'load', timeout: 600000 });
  await p.evaluate(() => document.fonts.ready);
  await p.addScriptTag({ content: fs.readFileSync(path.join(W, 'decorate.js'), 'utf8') });
  await p.evaluate(([title, W]) => { const tp = window.paginate(); document.querySelectorAll('td.pg').forEach(td => { td.textContent = tp[td.dataset.t] || ''; }); window.decorate(title, W); }, [title, W]);
  await p.evaluate(() => Promise.all(Array.from(document.images).filter(i => !i.complete).map(i => new Promise(r => { i.onload = i.onerror = r; }))));
  await p.pdf({ path: out, preferCSSPageSize: true, printBackground: true, timeout: 0, outline: true });
  await b.close();
})();
