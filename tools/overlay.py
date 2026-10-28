import sys,io,os
from PIL import Image,ImageDraw,ImageFont
from pypdf import PdfReader,PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
W=os.path.dirname(os.path.abspath(__file__))
FR="/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"; FB="/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
pdfmetrics.registerFont(TTFont("NS",FR)); pdfmetrics.registerFont(TTFont("NSB",FB))
H1,H2="@NotesHub_Ssc","@StudyWars_Ssc"
U1,U2="https://t.me/NotesHub_Ssc","https://t.me/StudyWars_Ssc"
C1,C2=(21,101,192),(198,40,40)   # blue, red
def text_png(text,color,alpha,size,path,rot=0):
    f=ImageFont.truetype(FB,size)
    bb=f.getbbox(text); w,h=bb[2]-bb[0]+20,bb[3]-bb[1]+20
    im=Image.new("RGBA",(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.text((10-bb[0],10-bb[1]),text,font=f,fill=color+(alpha,))
    if rot: im=im.rotate(rot,expand=True,resample=Image.BICUBIC)
    im.save(path); return path
def make_pngs():
    os.makedirs(W+"/wm",exist_ok=True)
    P={}
    P["L"]=text_png(H1,C1,150,90,W+"/wm/side_left.png",90)     # reads bottom-to-top
    P["R"]=text_png(H2,C2,150,90,W+"/wm/side_right.png",-90)   # reads top-to-bottom
    P["C1"]=text_png(H1,C1,22,160,W+"/wm/center_1.png",45)
    P["C2"]=text_png(H2,C2,22,160,W+"/wm/center_2.png",45)
    return P
def overlay(inp,out,title):
    P=make_pngs(); r=PdfReader(inp); n=len(r.pages)
    pw,ph=float(r.pages[0].mediabox.width),float(r.pages[0].mediabox.height)
    buf=io.BytesIO(); c=canvas.Canvas(buf,pagesize=(pw,ph))
    imgs={k:ImageReader(v) for k,v in P.items()}
    sizes={k:Image.open(v).size for k,v in P.items()}
    for i in range(n):
        pg=i+1
        # center watermark (alternating)
        k="C1" if pg%2 else "C2"; url=U1 if pg%2 else U2
        iw,ih=sizes[k]; cw=125*mm; chh=cw*ih/iw
        x,y=(pw-cw)/2,(ph-chh)/2
        c.drawImage(imgs[k],x,y,cw,chh,mask="auto"); c.linkURL(url,(x+cw*0.25,y+chh*0.25,x+cw*0.75,y+chh*0.75),relative=0)
        # side watermarks
        for k,url,xx in (("L",U1,3.2*mm),("R",U2,pw-3.2*mm-7*mm)):
            iw,ih=sizes[k]; sw=7*mm; sh=sw*ih/iw
            yy=(ph-sh)/2
            c.drawImage(imgs[k],xx,yy,sw,sh,mask="auto"); c.linkURL(url,(xx,yy,xx+sw,yy+sh),relative=0)
        if pg>1:
            # header
            c.setStrokeColorRGB(.12,.31,.47); c.setLineWidth(.6)
            hy=ph-11*mm
            c.setFont("NSB",8); c.setFillColorRGB(.12,.31,.47); c.drawString(15*mm,hy,title)
            c.setFont("NSB",8)
            t2="Join: "; w2=c.stringWidth(H2,"NSB",8); w1=c.stringWidth(H1,"NSB",8); sep="  |  "; ws=c.stringWidth(sep,"NSB",8)
            xr=pw-15*mm-w2; c.setFillColorRGB(*[v/255 for v in C2]); c.drawString(xr,hy,H2); c.linkURL(U2,(xr,hy-2,xr+w2,hy+8),relative=0)
            c.setFillColorRGB(.4,.4,.4); c.drawString(xr-ws,hy,sep)
            x1=xr-ws-w1; c.setFillColorRGB(*[v/255 for v in C1]); c.drawString(x1,hy,H1); c.linkURL(U1,(x1,hy-2,x1+w1,hy+8),relative=0)
            c.line(15*mm,hy-2.5*mm,pw-15*mm,hy-2.5*mm)
            # footer
            fy=8*mm
            c.line(15*mm,fy+4*mm,pw-15*mm,fy+4*mm)
            c.setFont("NS",7.5)
            c.setFillColorRGB(*[v/255 for v in C1]); s="t.me/NotesHub_Ssc"; c.drawString(15*mm,fy,s); c.linkURL(U1,(15*mm,fy-2,15*mm+c.stringWidth(s,"NS",7.5),fy+8),relative=0)
            c.setFillColorRGB(*[v/255 for v in C2]); s="t.me/StudyWars_Ssc"; ws=c.stringWidth(s,"NS",7.5); c.drawString(pw-15*mm-ws,fy,s); c.linkURL(U2,(pw-15*mm-ws,fy-2,pw-15*mm,fy+8),relative=0)
            c.setFillColorRGB(.2,.2,.2); c.setFont("NSB",8); c.drawCentredString(pw/2,fy,"%d"%pg)
        c.showPage()
    c.save(); buf.seek(0)
    ov=PdfReader(buf); w=PdfWriter(clone_from=r)
    for i,p in enumerate(w.pages): p.merge_page(ov.pages[i])
    w.add_metadata({"/Title":title,"/Author":"@NotesHub_Ssc & @StudyWars_Ssc"})
    w.compress_identical_objects() if hasattr(w,"compress_identical_objects") else None
    w.write(out); print("pages",n)
if __name__=="__main__": overlay(sys.argv[1],sys.argv[2],sys.argv[3])
