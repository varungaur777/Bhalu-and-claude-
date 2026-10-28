import json,glob,re,html,os
Z=os.environ.get("SSC_ZIP_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","zip"))
def txt(h):
    h=re.sub(r"(?is)<style.*?</style>","",h or "")
    h=re.sub(r"(?i)<br\s*/?>|</p>|</div>|</li>","\n",h)
    h=re.sub(r"<[^>]+>","",h); h=html.unescape(h).replace("\xa0"," ")
    h=re.sub(r"[ \t]+"," ",h); h=re.sub(r"\n\s*\n+","\n",h)
    return h.strip()
def load():
    out=[]
    for f in sorted(glob.glob(Z+"/*/*.json")):
        d=json.load(open(f)); rel=os.path.relpath(f,Z)
        for q in d["questions"]:
            e=q["en"]
            if e["section_id"]!="208": continue
            out.append(dict(file=rel,title=d["title"],sn=q["serial_no"],ans=q["correct_option"],e=e))
    return out
