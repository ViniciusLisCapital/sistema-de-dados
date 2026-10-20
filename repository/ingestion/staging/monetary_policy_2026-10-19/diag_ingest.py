"""Diagnostic: run the pipeline's extractor on every MP PDF (read-only, outputs in scratchpad)
and measure the failure modes the candidates file warns about."""
import json
import re
import sys
from pathlib import Path

import pdfplumber

sys.path.insert(0, str(Path("repository/ingestion/scripts").resolve()))
from clean_code import clean  # noqa: E402

SRC = Path("repository/monetary_policy/raw_pdf/theorical_literature")
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

COMMON = {"the", "and", "of", "to", "in", "is", "that", "a", "for", "on", "with", "as", "by", "this", "be"}


def gutter(page):
    """True if the page body has a vertical empty band near the centre (two columns)."""
    words = page.extract_words()
    if len(words) < 150:
        return None
    w = page.width
    lo, hi = 0.40 * w, 0.60 * w
    bins = [0] * 40
    for wd in words:
        a = max(int((wd["x0"] - lo) / (hi - lo) * 40), 0)
        b = min(int((wd["x1"] - lo) / (hi - lo) * 40), 39)
        for k in range(a, b + 1):
            if 0 <= k < 40:
                bins[k] += 1
    # an empty bin covered by < 3% of words => gutter
    return min(bins) <= 0.03 * len(words)


rows = []
for pdf in sorted(SRC.glob("*.pdf")):
    r = {"file": pdf.name}
    try:
        with pdfplumber.open(pdf) as doc:
            pages = doc.pages
            r["pages"] = len(pages)
            texts, gut = [], []
            for i, p in enumerate(pages):
                t = p.extract_text() or ""
                texts.append(t)
                if 1 <= i <= 6:  # sample body pages, skip the title page
                    g = gutter(p)
                    if g is not None:
                        gut.append(g)
        text = "\n\n".join(t.strip() for t in texts if t.strip())
        r["empty_pages"] = sum(1 for t in texts if len(t.strip()) < 50)
        r["chars"] = len(text)
        toks = re.findall(r"[A-Za-z]+", text)
        n = max(len(toks), 1)
        r["common_word_share"] = round(sum(1 for t in toks if t.lower() in COMMON) / n, 3)
        r["one_letter_share"] = round(sum(1 for t in toks if len(t) == 1) / n, 3)
        r["long_token_share"] = round(sum(1 for t in toks if len(t) >= 18) / n, 4)
        r["two_col_pages"] = f"{sum(gut)}/{len(gut)}"
        (OUT / f"{pdf.stem}.raw.md").write_text(text, encoding="utf-8")
        c = clean(text)
        (OUT / f"{pdf.stem}.clean.md").write_text(c, encoding="utf-8")
        r["clean_removed_pct"] = round(100 * (1 - len(c) / len(text)), 1) if text else None
    except Exception as e:  # noqa: BLE001
        r["error"] = repr(e)
    rows.append(r)
    print(json.dumps(r, ensure_ascii=False), flush=True)

(OUT / "_diag.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
