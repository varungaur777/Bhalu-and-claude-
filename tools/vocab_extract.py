import json,re,sys,collections,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from clean import plain
from wordfreq import zipf_frequency as zf
D=json.load(open(sys.argv[1]))
VOC={"Synonyms","Antonyms","One Word Substitution","Spelling Errors","Fill in the Blanks","Cloze Test"}
words=collections.defaultdict(set); idioms=collections.defaultdict(set)
def add(w,src):
    w=w.strip(" .,;:!?\"'“”‘’()[]").strip()
    if not re.fullmatch(r"[A-Za-z][A-Za-z\-']*[A-Za-z]",w): return
    lw=w.lower()
    if zf(lw,"en")>=4.6: return   # too common
    if len(lw)<4: return
    words[lw].add(src)
for d in D:
    t=d["topic"]; src=d["exam"]; stem=d.get("stem") or d["qhtml"]
    vocab_q = t in VOC or re.search(r"synonym|antonym|meaning of the (given|underlined) word|opposite",plain(stem),re.I)
    if t=="Idioms & Phrases":
        u=re.findall(r"<u>(.*?)</u>",stem)
        if u: idioms[re.sub(r"\s+"," ",plain(u[0])).strip(" .")].add(src)
        else:
            lines=[l for l in plain(stem).split("\n") if l.strip()]
            idioms[lines[-1].strip(" .")].add(src)
        continue
    if not vocab_q: continue
    if t=="Spelling Errors":
        for i,o in enumerate(d["opts"]):
            if "abcd"[i]!=d["ans"] or "correct" in plain(stem).lower() and "incorrect" not in plain(stem).lower(): pass
        # include only correctly spelt words: in 'incorrectly spelt' qs, the answer is wrong -> skip it
        inc=re.search(r"incorrect|misspel|wrongly",plain(stem),re.I)
        for i,o in enumerate(d["opts"]):
            p=plain(o)
            if inc and "abcd"[i]==d["ans"]: continue
            if not inc and "abcd"[i]!=d["ans"]: continue
            for w in p.split(): add(w,src)
        continue
    toks=[]
    u=re.findall(r"<u>(.*?)</u>",stem); 
    if t in("Synonyms","Antonyms") or vocab_q and t!="Cloze Test" and t!="Fill in the Blanks":
        lines=[l for l in plain(stem).split("\n") if l.strip()]
        cand=u or ([lines[-1]] if lines else [])
        for c in cand: toks+=plain(c).split() if len(plain(c).split())<=2 else []
    for o in d["opts"]:
        p=plain(o)
        if len(p.split())<=2: toks+=p.split()
    for w in toks: add(w,src)
json.dump({"words":{k:sorted(v) for k,v in sorted(words.items())},"idioms":{k:sorted(v) for k,v in sorted(idioms.items(),key=lambda x:x[0].lower())}},open(sys.argv[2],"w"),ensure_ascii=False,indent=0)
print(len(words),len(idioms))
