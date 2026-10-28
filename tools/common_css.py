CSS = r"""
@page { size: A4; margin: 0; }
.page { width:210mm; height:297mm; padding:17mm 15mm 15mm 15mm; overflow:hidden; break-after: page; display:flex; flex-direction:column; position:relative; }
.page:last-child { break-after: auto; }
.cols2 { flex:1; min-height:0; display:flex; gap:7mm; background: linear-gradient(#c9d3de,#c9d3de) no-repeat center/0.5pt 100%; }
.col { flex:1; min-width:0; height:100%; overflow:hidden; }
.inner { display:flow-root; }
.contd > .card, .card.contd { border-top-style: dashed; }
.q.contd > .card::before, .card.contd::before { content:"Explanation (contd.)"; display:block; font-weight:700; color:#1f4e79; font-size:7.6pt; }
.passage.contd::before { content:"Passage (contd.)"; display:block; font-weight:700; color:#1f4e79; font-size:7.6pt; }
#src { width: 87.5mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin:0; font-family: "Noto Sans", "Noto Sans Devanagari", sans-serif; font-size: 8.6pt; line-height: 1.38; color:#111; }
p { margin: 0 0 2pt 0; }
ul, ol { margin: 1pt 0 2pt 0; padding-left: 12pt; }
li { margin: 0 0 1pt 0; }
li > p { margin:0; }
img { max-width: 100%; }
.topic-head { border-bottom: 2pt solid #1f4e79; margin: 0 0 6pt 0; padding: 0 0 3pt 0; display:flex; justify-content:space-between; align-items:baseline; }
.topic-head h1 { font-size: 15pt; margin:0; color:#1f4e79; }
.topic-head .cnt { font-size: 8.6pt; color:#555; }
.q { margin: 0 0 6pt 0; }
.q.contd { margin-top:0; }
.qtext { font-weight: 700; }
.qtext p, .qtext li { font-weight: 700; }
.qtext > p:first-of-type { display:inline; }
.card p { margin:0 0 1pt 0; }
.qnum { font-weight: 700; color:#1f4e79; }
.opts { margin: 2pt 0 0 0; padding: 0; list-style:none; }
.opts li { margin: 0 0 1pt 0; display:flex; gap:3pt; }
.opts.grid { display:grid; grid-template-columns: 1fr 1fr; column-gap:6pt; }
.opts .lab { font-weight: 700; min-width: 13pt; }
.opts .ot p { display:inline; margin:0; }
.exam { font-size: 7.4pt; color:#7a4b00; font-style: italic; margin: 2pt 0 2pt 0; }
.card { border: 0.6pt solid #9fb7cf; border-left: 2.4pt solid #2e7d32; background:#f3f8f3; border-radius: 2pt; padding: 3pt 5pt; font-size: 8.2pt; line-height:1.34; }
.card .ans { font-weight:700; color:#1b5e20; margin-bottom:1pt; }
.card .lbl { font-weight:700; color:#1f4e79; }
.passage p { margin:0 0 2pt 0; }
.passage { border: 0.6pt solid #b9c7d6; background:#f7f9fc; border-radius:2pt; padding: 4pt 5pt; margin: 0 0 5pt 0; text-align: justify; }
.passage .ph { font-weight:700; color:#1f4e79; margin-bottom:2pt; break-after: avoid; }
.passage .pexam { font-size:7.4pt; color:#7a4b00; font-style:italic; margin-top:2pt; }
.imgmiss { border:0.6pt dashed #b00; color:#b00; font-size:7.4pt; padding:2pt; margin:2pt 0; }
.cover { height: 100%; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; break-after: page; }
.cover h1 { font-size: 30pt; color:#1f4e79; margin: 0 0 8pt 0; line-height:1.15; }
.cover h2 { font-size: 15pt; color:#444; font-weight:500; margin:0 0 18pt 0; }
.cover .meta { font-size: 10pt; color:#333; line-height:1.7; }
.cover a { color:#1f4e79; text-decoration:none; font-weight:700; }
.toc { break-after: page; }
.toc h1 { font-size:15pt; color:#1f4e79; border-bottom:2pt solid #1f4e79; padding-bottom:3pt; }
.toc table { width:100%; border-collapse:collapse; font-size:10pt; }
.toc td { padding: 4pt 2pt; border-bottom: 0.5pt solid #ddd; }
.toc td.n { text-align:right; }
.toc a { color:#111; text-decoration:none; }
.wm-c { position:absolute; left:50%; top:50%; width:125mm; transform:translate(-50%,-50%); z-index:3; }
.wm-c img { width:100%; display:block; }
.wm-l, .wm-r { position:absolute; top:50%; width:7mm; transform:translateY(-50%); z-index:2; }
.wm-l { left:3.2mm; } .wm-r { right:3.2mm; }
.wm-l img, .wm-r img { width:100%; display:block; }
.cols2, .topic-head, .cover, .toc { position:relative; z-index:1; }
.hdr { position:absolute; left:15mm; right:15mm; top:7mm; height:6mm; display:flex; justify-content:space-between; align-items:flex-end; font-size:8pt; font-weight:700; border-bottom:0.6pt solid #1f4e79; padding-bottom:1.2mm; z-index:2; }
.hdr .ht { color:#1f4e79; }
.ftr { position:absolute; left:15mm; right:15mm; bottom:5mm; display:flex; justify-content:space-between; font-size:7.5pt; border-top:0.6pt solid #1f4e79; padding-top:1.2mm; z-index:2; }
.ftr .pn { font-weight:700; color:#333; }
a.h1 { color:#1565c0; text-decoration:none; } a.h2 { color:#c62828; text-decoration:none; }

"""
