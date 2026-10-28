const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + process.argv[2]); await p.evaluate(() => document.fonts.ready);
  const before = await p.evaluate(() => ({q: document.querySelectorAll('#src .q').length, len: document.getElementById('src').textContent.replace(/\s+/g,'').length}));
  await p.evaluate(() => window.paginate());
  const after = await p.evaluate(() => {
    const over=[]; document.querySelectorAll('.page').forEach((pg,i)=>pg.querySelectorAll('.inner').forEach(c=>{ if(c.getBoundingClientRect().height > c.parentNode.clientHeight+1) over.push(i+1); }));
    const sp=[]; document.querySelectorAll('.page').forEach((pg,i)=>{ if(pg.querySelector('.inner') && pg.querySelectorAll('.inner')[0].textContent.trim()==='' ) sp.push(i+1); });
    return {q: document.querySelectorAll('#book .q:not(.contd)').length, contd: document.querySelectorAll('#book .q.contd').length, pcontd: document.querySelectorAll('#book .passage.contd').length, len: document.getElementById('book').textContent.replace(/\s+/g,'').length, overflow: over, emptyPages: sp, pages: document.querySelectorAll('.page').length};
  });
  console.log(JSON.stringify({before, after}));
  await b.close();
})();
