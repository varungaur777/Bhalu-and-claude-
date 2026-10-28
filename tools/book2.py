import json,sys,os,html
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common_css import CSS
W=os.path.dirname(os.path.abspath(__file__))
E=html.escape
CSS2=CSS+r"""
.ve { margin: 0 0 5pt 0; padding: 0 0 4pt 0; border-bottom: 0.5pt dotted #c3ccd6; }
.ve .hw { font-weight:700; font-size:10pt; color:#1f4e79; }
.ve .pos { font-style:italic; color:#666; font-size:7.8pt; }
.ve .row { margin: 1pt 0 0 0; }
.ve .k { font-weight:700; color:#333; }
.ve .hi { font-family: "Noto Sans Devanagari","Noto Sans",sans-serif; }
.ve .mn { background:#fff7e6; border-left:2pt solid #e0a800; padding:1pt 4pt; margin-top:2pt; }
.ve .ex { font-style: italic; color:#222; }
.lh { font-size: 13pt; font-weight:700; color:#fff; background:#1f4e79; border-radius:2pt; padding:1pt 6pt; margin: 2pt 0 4pt 0; display:inline-block; }
"""
def entry(w,letter=None):
    lh='<div class="lh">%s</div>'%letter if letter else ""
    return ('<div class="unit ve">%s<div><span class="hw">%s</span> <span class="pos">(%s)</span></div>'
            '<div class="row"><span class="k">Meaning:</span> %s</div>'
            '<div class="row"><span class="k">Hindi:</span> <span class="hi">%s</span></div>'
            '<div class="row mn"><span class="k">Mnemonic:</span> %s</div>'
            '<div class="row ex"><span class="k">Example:</span> %s</div></div>')%(lh,E(w["word"]),E(w["pos"]),E(w["en"]),E(w["hi"]),E(w["mnemonic"]),E(w["example"]))
def build(out):
    V=json.load(open(W+"/vocab_final.json")); words,idioms=V["words"],V["idioms"]
    body=[]; last=None
    body.append('<section class="topic" id="t0"><div class="topic-head"><h1>Part A: Vocabulary Words</h1><span class="cnt">%d words</span></div>'%len(words))
    for w in words:
        L=w["word"][0].upper(); body.append(entry(w, L if L!=last else None)); last=L
    body.append('</section><section class="topic" id="t1"><div class="topic-head"><h1>Part B: Idioms &amp; Phrases</h1><span class="cnt">%d entries</span></div>'%len(idioms))
    last=None
    for w in idioms:
        L=w["word"][0].upper(); body.append(entry(w, L if L!=last else None)); last=L
    body.append('</section>')
    cover='''<div class="cover"><h1>SSC English<br>Vocabulary Book</h1><h2>Words &amp; Idioms from Tier-2 / Mains PYQs<br>CGL · CHSL · CPO</h2>
<div class="meta">%d words · %d idioms &amp; phrases<br>English meaning · Hindi meaning · Mnemonic · Example<br><br>
<a href="https://t.me/NotesHub_Ssc">@NotesHub_Ssc</a> &nbsp;·&nbsp; <a href="https://t.me/StudyWars_Ssc">@StudyWars_Ssc</a></div></div>'''%(len(words),len(idioms))
    toc='<div class="toc"><h1>Contents</h1><table><tr><td><b>Section</b></td><td class="n"><b>Entries</b></td><td class="n"><b>Page</b></td></tr><tr><td><a href="#t0">Part A: Vocabulary Words</a></td><td class="n">%d</td><td class="n pg" data-t="t0"></td></tr><tr><td><a href="#t1">Part B: Idioms &amp; Phrases</a></td><td class="n">%d</td><td class="n pg" data-t="t1"></td></tr></table></div>'%(len(words),len(idioms))
    doc='<!doctype html><html><head><meta charset="utf-8"><title>SSC English Vocabulary Book</title><style>%s</style><script>%s</script></head><body><div id="src"><section class="static">%s</section><section class="static">%s</section>%s</div><div id="book"></div></body></html>'%(CSS2,open(W+"/paginate.js").read(),cover,toc,"".join(body))
    open(out,"w").write(doc); print(len(words),len(idioms))
if __name__=="__main__": build(sys.argv[1])
