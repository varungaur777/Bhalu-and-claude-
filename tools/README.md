# Book build tools

Scripts that generate the two PDFs in `books/` from `CHSL, CPO, CGL English.zip`.

1. Unzip the archive and set `SSC_ZIP_DIR` to the extracted folder.
2. `python3 build.py data.json` – extracts English (section 208) questions, cleans HTML, classifies topics, groups passages.
3. `python3 fetch_images.py` – downloads question/solution images (writes `imgmap.json`).
4. `python3 vocab_extract.py data.json vocab_raw.json` – candidate vocabulary words (entries were then written and proofread into `vocab_final.json`).
5. `python3 book1.py book1.html && node render.js $PWD/book1.html $PWD/book1.pdf "SSC English Topic-wise PYQ Book (Tier-2)"`
6. `python3 book2.py book2.html && node render.js $PWD/book2.html $PWD/book2.pdf "SSC English Vocabulary Book"`

Requires Chromium + Playwright (Node), Noto Sans / Noto Sans Devanagari fonts, and `wordfreq` for step 4.
Run the scripts from a working copy that also holds `data.json`, `vocab_final.json` and `wm/`.
