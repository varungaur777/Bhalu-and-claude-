import sys,re,json,collections,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from load import load
from clean import clean, plain
from classify import classify
def exam_label(rel,title):
    folder=rel.split("/")[0]; exam,year=folder.split()
    tier="Tier 2"
    m=re.search(r"\(([^)]*\d[^)]*)\)",title) if exam!="CPO" and "T-2" in title else None
    date=None
    m1=re.match(r"(\d+ \w+ \d{4})",title)
    if m1: date=m1.group(1)
    m2=re.search(r"T-2 \((\d+ \w+)\)",title) or re.search(r"Tier-2 \((\d+ \w+)\)",title)
    if m2: date=m2.group(1).replace("apr","Apr")
    parts=["SSC %s %s"%(exam,tier),year]
    if date: parts.append(date)
    return " | ".join(parts)
LET="abcd"
def norm(s): return re.sub(r"[^a-z]","",s.lower())
def strip_answer_line(sol):
    # remove leading 'Correct Answer' paragraph
    sol=re.sub(r"^\s*<p>\s*(✅|✔️?|☑️?)?\s*(<b>)?\s*Correct (Answer|Option)\s*:?.*?</p>","",sol,count=1,flags=re.I|re.S)
    sol=re.sub(r"✅|✔️|✔|❌|☑️|✖️|👉|📌|💡|🔹|🔸|⭐|➡️","",sol)
    sol=re.sub(r"\b[Oo]ption\s*\(?([A-Da-d])\)?(?=[^A-Za-z]|$)",lambda m:"option (%s)"%m.group(1).lower(),sol)
    sol=re.sub(r"\*\*([^*<>]{1,80})\*\*",r"<b>\1</b>",sol)
    sol=re.sub(r"(?<![\w*])\*([^*<>\s][^*<>]{0,60}?)\*(?![\w*])",r"<i>\1</i>",sol)
    sol=re.sub(r"\*(?=(<[^>]+>)*[\"“])|(?<=[\"”.])((<[^>]+>)*)\*",r"\2",sol)
    sol=re.sub(r"(→\s*(?:Active:\s*)?|\.\s)\*(?=[A-Z(])",r"\1",sol)
    sol=re.sub(r"•\s*",r"• ",sol)
    sol=re.sub(r"(Top|Bottom) of Form","",sol)
    sol=re.sub(r"\b([Oo])ption\s*(?:no\.?\s*)?\(?([1-4])\)?(?![\d.])",lambda m:m.group(1)+"ption (%s)"%"abcd"[int(m.group(2))-1],sol)
    sol=re.sub(r"<p>\s*</p>","",sol)
    return sol.strip()
def stated_answer(sol):
    p=plain(sol)
    m=re.search(r"Correct (?:Answer|Option)\s*(?:is)?\s*:?\s*(?:Option)?\s*\(?([A-Da-d1-4])\)?",p)
    if not m: return None
    v=m.group(1).upper(); return "ABCD"["1234".index(v)] if v.isdigit() else v
def main(out):
    Q=load(); items=[]; issues=[]
    for q in Q:
        e=q["e"]; qh=clean(e["question"]); topic=classify(plain(qh))
        opts=[clean(e["option_%d"%i]) for i in range(1,5)]
        for i in range(5,11):
            if plain(clean(e["option_%d"%i])): issues.append(("extra_option",q["file"],q["sn"]))
        sol=clean(e["solution_text"])
        sa=stated_answer(sol)
        if sa and sa!=q["ans"]: issues.append(("answer_mismatch",q["file"],q["sn"],q["ans"],sa))
        if q["ans"] not in "ABCD":
            issues.append(("bad_ans",q["file"],q["sn"],q["ans"],sa,plain(qh)[:300],[plain(o) for o in opts],plain(sol)[:600]))
            q["ans"]=sa or {"CGL 2022/6 March 2022 (CGL 2022) English.json#32":"C"}[q["file"]+"#%d"%q["sn"]]
        if any(not plain(o) and "<img" not in o for o in opts): issues.append(("empty_option",q["file"],q["sn"]))
        imgs=[e[k] for k in ("solution_image_1","solution_image_2") if e[k]]
        items.append(dict(id=e["id"],file=q["file"],sn=q["sn"],exam=exam_label(q["file"],q["title"]),
            topic=topic,qhtml=qh,opts=opts,ans=LET["ABCD".index(q["ans"])],
            expl=strip_answer_line(sol)+"".join('<p><img src="%s"></p>'%u for u in imgs),raw_sol=sol))
    # passage grouping
    groups=collections.defaultdict(list)
    for it in items:
        if it["topic"] in("Reading Comprehension","Cloze Test"):
            groups[(it["file"],norm(plain(it["qhtml"]))[:300])].append(it)
    pid=0
    for k,g in groups.items():
        pid+=1
        if len(g)==1:
            issues.append(("single_passage",g[0]["file"],g[0]["sn"]))
        texts=[x["qhtml"] for x in g]
        # common prefix in html
        pre=os.path.commonprefix(texts) if len(g)>1 else texts[0]
        if len(g)==1:
            # split at last <br> or </p>
            cut=max(pre.rfind("<br>"),pre.rfind("<p>"))
            pre=pre[:cut] if cut>0 else pre
        else:
            # back off to a boundary
            cut=max(pre.rfind("<br>"),pre.rfind("</p>")+4 if pre.rfind("</p>")>=0 else -1)
            if cut>len(pre)*0.5: pre=pre[:cut]
        # move trailing instruction line shared by all into stems
        m=re.search(r"(<br>|<p>)\s*((?:Select|Choose|Identify|Pick|What|Which|Find)[^<]{0,200})(</p>)?\s*$",pre)
        if m and len(g)>1: pre=pre[:m.start()]
        for x in g:
            stem=x["qhtml"][len(pre):]
            x["pid"]=pid; x["passage"]=clean(pre); x["stem"]=clean(stem)
            if len(plain(x["stem"]))<5: issues.append(("short_stem",x["file"],x["sn"],plain(x["stem"])))
    json.dump(items,open(out,"w"),ensure_ascii=False,indent=0)
    c=collections.Counter(i[0] for i in issues); print(c)
    for i in issues:
        if i[0]!="single_passage": print(i)
    print(collections.Counter(i["topic"] for i in items)); print(sorted(set(i["exam"] for i in items)))
if __name__=="__main__": main(sys.argv[1])
