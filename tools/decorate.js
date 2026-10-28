window.decorate=function(title, W){
  const pages=document.querySelectorAll('#book .page');
  const U1='https://t.me/NotesHub_Ssc', U2='https://t.me/StudyWars_Ssc';
  pages.forEach((pg,i)=>{
    const n=i+1;
    const add=h=>pg.insertAdjacentHTML('beforeend',h);
    const odd=n%2===1;
    add(`<a class="wm-c" href="${odd?U1:U2}"><img src="file://${W}/wm/center_${odd?1:2}.png"></a>`);
    add(`<a class="wm-l" href="${U1}"><img src="file://${W}/wm/side_left.png"></a>`);
    add(`<a class="wm-r" href="${U2}"><img src="file://${W}/wm/side_right.png"></a>`);
    if(n>1){
      add(`<div class="hdr"><span class="ht">${title}</span><span><a class="h1" href="${U1}">@NotesHub_Ssc</a> &nbsp;|&nbsp; <a class="h2" href="${U2}">@StudyWars_Ssc</a></span></div>`);
      add(`<div class="ftr"><a class="h1" href="${U1}">t.me/NotesHub_Ssc</a><span class="pn">${n}</span><a class="h2" href="${U2}">t.me/StudyWars_Ssc</a></div>`);
    }
  });
};
