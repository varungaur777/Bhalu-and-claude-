import json,re,sys,os,html,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from clean import plain
from common_css import CSS
W=os.path.dirname(os.path.abspath(__file__))
ORDER=["Synonyms","Antonyms","Idioms & Phrases","One Word Substitution","Spelling Errors","Fill in the Blanks","Error Spotting","Sentence Improvement","Active & Passive Voice","Direct & Indirect Speech","Para Jumbles","Cloze Test","Reading Comprehension"]
FILE_ORDER=lambda f:(f.split()[0], int(f.split()[1].split("/")[0]))
IMGMAP=json.load(open(W+"/imgmap.json")) if os.path.exists(W+"/imgmap.json") else {}
def fix_imgs(h):
    def rep(m):
        u=html.unescape(m.group(1))
        if u in IMGMAP and os.path.exists(IMGMAP[u]): return '<img src="file://%s">'%IMGMAP[u]
        return '<div class="imgmiss">[Image could not be downloaded: %s]</div>'%html.escape(u)
    return re.sub(r'<img src="([^"]+)">',rep,h)
def strip_p(h):
    h=re.sub(r"^\s*<p>","",h); h=re.sub(r"</p>\s*$","",h); return h
def fix_expl(h,topic):
    if topic!="Para Jumbles":
        h=re.sub(r"\(([A-D])\)",lambda m:"("+m.group(1).lower()+")",h)
    h=re.sub(r"<p>\s*<b>\s*Explanation\s*:?\s*</b>\s*</p>","",h,count=1)
    return h
def balanced(h):
    for t in("b","i","u","sup","sub","ul","ol","li"):
        if len(re.findall("<%s>"%t,h))!=len(re.findall("</%s>"%t,h)): return False
    return True
def to_paras(h):
    parts=re.split(r"</p>\s*<p>|<br>|</p>|<p>",h)
    parts=[p.strip() for p in parts if p.strip()]
    if all(balanced(p) for p in parts): return "".join("<p>%s</p>"%p for p in parts)
    return "<p>%s</p>"%h
def render_q(n,d,in_passage):
    qh=d["stem"] if in_passage else d["qhtml"]
    out=['<div class="unit q" data-topic="%s" data-free="%d"><div class="qhead">'%(html.escape(d["topic"]),0 if in_passage else 1)]
    out.append('<div class="qtext"><span class="qnum">Q.%d</span> %s</div>'%(n,fix_imgs(qh)))
    short=all(len(plain(o))<=22 and "<img" not in o for o in d["opts"])
    out.append('<ul class="opts%s">'%(" grid" if short else ""))
    for i,o in enumerate(d["opts"]):
        out.append('<li><span class="lab">(%s)</span><span class="ot">%s</span></li>'%("abcd"[i],fix_imgs(strip_p(o))))
    out.append('</ul></div>')
    out.append('<div class="exam">%s</div>'%html.escape(d["exam"]))
    ans=d["ans"]; at=strip_p(d["opts"]["abcd".index(ans)])
    out.append('<div class="card"><div class="ans">Explanation — Correct answer: (%s) %s</div>%s</div>'%(ans,re.sub(r"</?p>"," ",at).strip(),fix_imgs(fix_expl(d["expl"],d["topic"]))))
    out.append('</div>')
    return "".join(out)
def build(out_html):
    D=json.load(open(W+"/data.json"))
    by=collections.defaultdict(list)
    for d in D: by[d["topic"]].append(d)
    assert set(by)<=set(ORDER), set(by)-set(ORDER)
    body=[]; toc=[]; total=0
    for ti,t in enumerate(ORDER):
        L=sorted(by[t],key=lambda d:(FILE_ORDER(d["file"]),d["file"],d.get("pid",0),d["sn"]))
        body.append('<section class="topic" id="t%d"><div class="topic-head"><h1>%d. %s</h1><span class="cnt">%d questions</span></div>'%(ti,ti+1,html.escape(t),len(L)))
        n=0; seen=set(); pn=0
        for d in L:
            if d.get("pid"):
                if d["pid"] in seen: continue
                seen.add(d["pid"]); pn+=1
                grp=[x for x in L if x.get("pid")==d["pid"]]
                def bl(x):
                    m=re.search(r"blank\s*(?:number|no\.?)?\s*\(?(\d+)",plain(x["stem"]),re.I)
                    return int(m.group(1)) if m else 99
                grp.sort(key=lambda x:(bl(x),x["sn"]))
                body.append('<div class="unit passage"><div class="ph">%s %d (Q.%d–Q.%d)</div>%s<div class="pexam">%s</div></div>'%("Passage" if t=="Reading Comprehension" else "Cloze Passage",pn,n+1,n+len(grp),fix_imgs(to_paras(grp[0]["passage"])),html.escape(d["exam"])))
                for x in grp:
                    n+=1; body.append(render_q(n,x,True))
            else:
                n+=1; body.append(render_q(n,d,False))
        assert n==len(L),(t,n,len(L))
        total+=n
        body.append('</section>')
        toc.append('<tr><td><a href="#t%d">%d. %s</a></td><td class="n">%d</td><td class="n pg" data-t="t%d"></td></tr>'%(ti,ti+1,html.escape(t),len(L),ti))
    cover='''<div class="cover"><h1>SSC English<br>Topic-wise Question Book</h1><h2>Tier-2 / Mains Previous Year Questions<br>CGL · CHSL · CPO</h2>
<div class="meta">%d questions · 13 topics · with answers &amp; explanations<br><br>
<a href="https://t.me/NotesHub_Ssc">@NotesHub_Ssc</a> &nbsp;·&nbsp; <a href="https://t.me/StudyWars_Ssc">@StudyWars_Ssc</a></div></div>'''%total
    tocs='<div class="toc"><h1>Contents</h1><table><tr><td><b>Topic</b></td><td class="n"><b>Questions</b></td><td class="n"><b>Page</b></td></tr>%s<tr><td><b>Total</b></td><td class="n"><b>%d</b></td><td></td></tr></table></div>'%("".join(toc),total)
    doc='<!doctype html><html><head><meta charset="utf-8"><title>SSC English Topic-wise Question Book</title><style>%s</style><script>%s</script></head><body><div id="src"><section class="static">%s</section><section class="static">%s</section>%s</div><div id="book"></div></body></html>'%(CSS,open(W+"/paginate.js").read(),cover,tocs,"".join(body))
    open(out_html,"w").write(doc); print("questions",total,"html bytes",len(doc))
if __name__=="__main__": build(sys.argv[1])
