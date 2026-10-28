import re, html
from html.parser import HTMLParser
KEEP={"b","i","u","sup","sub","ul","ol","li","img","br","p"}
BLOCK={"p","div","li","ul","ol","h1","h2","h3","h4","h5","h6","tr","table"}
class San(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.out=[]; s.stack=[]; s.skip=0
    def handle_starttag(s,tag,attrs):
        a=dict(attrs); tag=tag.lower()
        if tag in("style","script"): s.skip+=1; return
        opened=[]
        st=(a.get("style") or "").lower().replace(" ","")
        if tag in("b","strong") or "font-weight:bold" in st or re.search(r"font-weight:(6|7|8|9)00",st): opened.append("b")
        if tag in("i","em") or "font-style:italic" in st: opened.append("i")
        if tag=="u" or "text-decoration:underline" in st: opened.append("u")
        if tag in("sup","sub"): opened.append(tag)
        if tag=="br": s.out.append("<br>"); return
        if tag=="img":
            if a.get("src"): s.out.append('<img src="%s">'%html.escape(a["src"],quote=True))
            return
        if tag in("ul","ol","li","p"): s.out.append("<%s>"%tag); opened.insert(0,"/"+tag)
        elif tag in BLOCK: s.out.append("<br>")
        for t in opened:
            if not t.startswith("/"): s.out.append("<%s>"%t)
        s.stack.append((tag,opened))
    def handle_endtag(s,tag):
        tag=tag.lower()
        if tag in("style","script"): s.skip=max(0,s.skip-1); return
        for i in range(len(s.stack)-1,-1,-1):
            if s.stack[i][0]==tag:
                for t,op in reversed(s.stack[i:]):
                    for o in reversed(op):
                        s.out.append("</%s>"%o.lstrip("/"))
                del s.stack[i:]; break
    def handle_data(s,d):
        if s.skip: return
        s.out.append(html.escape(d,quote=False))
def underline_combining(h):
    # chars followed by U+0332 -> <u>
    def rep(m): return "<u>"+m.group(0).replace("̲","")+"</u>"
    h=re.sub(r"(?:[^̲<>]̲)+(?: (?:[^̲<>]̲)+)*",rep,h)
    return h.replace("̲","")
def clean(h):
    if not h: return ""
    p=San(); p.feed(h); p.close()
    for t,op in reversed(p.stack):
        for o in reversed(op): p.out.append("</%s>"%o.lstrip("/"))
    h="".join(p.out).replace("\xa0"," ").replace("​","")
    h=underline_combining(h)
    h=re.sub(r"[ \t\r\n]+"," ",h)
    h=re.sub(r"<(b|i|u|sup|sub)>\s*</\1>","",h)
    h=re.sub(r"</(b|i|u)>(\s*)<\1>",r"\2",h)
    h=re.sub(r"<p>\s*(<br>\s*)*</p>","",h)
    h=re.sub(r"(\s*<br>\s*){2,}","<br>",h)
    h=re.sub(r"^(\s*<br>\s*)+|(\s*<br>\s*)+$","",h)
    h=re.sub(r"(<p>)\s*(<br>\s*)+",r"\1",h); h=re.sub(r"(\s*<br>)+\s*(</p>)",r"\2",h)
    return h.strip()
def plain(h):
    h=re.sub(r"<br>|</p>|</li>","\n",h); h=re.sub(r"<[^>]+>","",h); return html.unescape(h).strip()
