import json,re,os,hashlib,subprocess,sys
W=os.path.dirname(os.path.abspath(__file__)); D=json.load(open(W+"/data.json"))
urls=set()
for d in D:
    for h in [d["qhtml"],d["expl"]]+d["opts"]+[d.get("passage","")]:
        urls.update(re.findall(r'<img src="([^"]+)"',h or ""))
os.makedirs(W+"/img",exist_ok=True); m={}; fails=[]
for u in sorted(urls):
    import html; uu=html.unescape(u)
    p=W+"/img/"+hashlib.md5(uu.encode()).hexdigest()+os.path.splitext(uu)[1][:5]
    if not os.path.exists(p) or os.path.getsize(p)==0:
        r=subprocess.run(["curl","-sSfL","-m","30","-o",p,uu],capture_output=True)
        if r.returncode!=0:
            if os.path.exists(p): os.remove(p)
            fails.append(uu); continue
    m[uu]=p
json.dump(m,open(W+"/imgmap.json","w"),indent=0)
print("images",len(urls),"downloaded",len(m),"failed",len(fails))
