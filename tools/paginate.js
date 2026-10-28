// Packs .unit elements from #src into fixed A4 pages with two columns (custom layout engine).
(function(){
const QMIN = 0.10;   // split a question's explanation card only if >=12% of the column would otherwise stay empty
const PMIN = 0.08;
function newPage(book, heading){
  const pg=document.createElement('div'); pg.className='page';
  if(heading){ pg.appendChild(heading); }
  const cols=document.createElement('div'); cols.className='cols2';
  const res=[];
  for(let k=0;k<2;k++){ const c=document.createElement('div'); c.className='col'; const i=document.createElement('div'); i.className='inner'; c.appendChild(i); cols.appendChild(c); res.push(i); }
  pg.appendChild(cols); book.appendChild(pg);
  return res;
}
function H(col){ return col.parentNode.clientHeight; }
function used(col){ return col.getBoundingClientRect().height; }
function fits(col){ return used(col) <= H(col) + 0.5; }
const CAN_SPLIT = el => el.nodeType===1 && el.childNodes.length>1 && el.matches('.q, .card, .passage, ul, ol, li, .card p, .card div:not(.ans), .ventry');
// Move as many (descendant) nodes of `el` into a shell appended to `target` as fit in `col`.
// Returns {placed: bool, rest: element|null}
function splitNode(el, target, col){
  const sh=el.cloneNode(false); target.appendChild(sh);
  const kids=Array.from(el.childNodes);
  for(let i=0;i<kids.length;i++){
    const k=kids[i];
    sh.appendChild(k);
    if(fits(col)) continue;
    sh.removeChild(k);
    let restChild=k;
    if(CAN_SPLIT(k)){
      const r=splitNode(k, sh, col);   // on failure k is left intact and nothing is added to sh
      if(r.placed) restChild=r.rest;
    }
    if(sh.childNodes.length===0){
      // nothing placed: undo, leave el intact
      target.removeChild(sh);
      for(const kk of kids) if(kk.parentNode!==el) el.appendChild(kk);
      return {placed:false, rest:null};
    }
    const rest=el.cloneNode(false); rest.classList.add('contd');
    if(restChild) rest.appendChild(restChild);
    for(let j=i+1;j<kids.length;j++) rest.appendChild(kids[j]);
    return {placed:true, rest: rest.childNodes.length? rest : null};
  }
  return {placed:true, rest:null};
}
function tryPlace(u,col,force){
  const backup=u.cloneNode(true);
  const r=splitNode(u,col,col);
  const head=col.lastChild;
  let ok=r.placed;
  if(ok && u.classList.contains('q') && !force){
    // the placed part must contain the whole question/options, exam line, answer line and some explanation
    const card=head.querySelector('.card');
    ok = !!(head.querySelector('.qhead') && head.querySelector('.exam') && card && card.querySelector('.ans') && (card.textContent.length - card.querySelector('.ans').textContent.length) > 8);
    if(ok && r.rest && r.rest.textContent.trim().length < 15) ok=true;
  }
  if(!ok){ if(r.placed) col.removeChild(head); return {ok:false, backup}; }
  return {ok:true, rest:r.rest};
}
function balance(cols){
  const [a,b]=cols;
  while(b.firstChild) a.appendChild(b.firstChild);
  if(fits(a) && a.childNodes.length<2) return;
  // move trailing children of a to b while that improves balance
  while(a.childNodes.length>1){
    const pa=used(a), pb=used(b);
    const last=a.lastChild; b.insertBefore(last,b.firstChild);
    if(!fits(b)){ a.appendChild(b.firstChild); break; }
    if(fits(a) && used(b) > used(a)){
      if(Math.abs(used(b)-used(a)) > Math.abs(pa-pb)) a.appendChild(b.firstChild);
      break;
    }
  }
}
window.paginate=function(){
  const src=document.getElementById('src'); const book=document.getElementById('book');
  const topicPages={};
  for(const sec of Array.from(src.children)){
    if(sec.classList.contains('static')){ const pg=document.createElement('div'); pg.className='page static'; while(sec.firstChild) pg.appendChild(sec.firstChild); book.appendChild(pg); continue; }
    const heading=sec.querySelector('.topic-head'); heading.remove();
    let cols=newPage(book, heading); let ci=0;
    topicPages[sec.id]=book.children.length;
    const queue=Array.from(sec.querySelectorAll(':scope > .unit'));
    const next=()=>{ ci++; if(ci>1){ cols=newPage(book,null); ci=0; } };
    let guard=0;
    while(queue.length){
      if(++guard>200000) throw new Error('loop');
      let u=queue.shift(); const col=cols[ci];
      col.appendChild(u);
      if(fits(col)) continue;
      col.removeChild(u);
      const empty = col.childNodes.length===0;
      if(u.dataset.free==='1' && !empty){
        let found=-1;
        for(let k=0;k<Math.min(queue.length,80);k++){
          const c=queue[k]; if(c.dataset.free!=='1') break;
          col.appendChild(c); const ok=fits(col); col.removeChild(c);
          if(ok){ found=k; break; }
        }
        if(found>=0){ const c=queue.splice(found,1)[0]; col.appendChild(c); queue.unshift(u); continue; }
      }
      const free=(H(col)-used(col))/H(col);
      const isQ=u.classList.contains('q');
      if(empty || (!u.classList.contains('ve') && free >= (isQ?QMIN:PMIN))){
        const t=tryPlace(u,col,empty);
        if(t.ok){ if(t.rest){ next(); queue.unshift(t.rest); } continue; }
        u=t.backup;
      }
      next(); queue.unshift(u);
    }
    balance(cols);
  }
  src.remove();
  const cnt={};
  document.querySelectorAll('#book .q:not(.contd)[data-free="1"]').forEach(q=>{ const t=q.dataset.topic; cnt[t]=(cnt[t]||0)+1; const n=q.querySelector('.qnum'); if(n) n.textContent='Q.'+cnt[t]; });
  return topicPages;
};
})();
