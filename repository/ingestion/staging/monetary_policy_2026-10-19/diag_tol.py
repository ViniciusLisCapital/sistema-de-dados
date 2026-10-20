"""Compare x_tolerance 3 (current) vs 1.5 across all PDFs, plus (cid:N) glyph counts."""
import re
from pathlib import Path

import pdfplumber

SRC = Path("repository/monetary_policy/raw_pdf/theorical_literature")


def stats(text):
    toks = re.findall(r"[A-Za-z]+", text)
    n = max(len(toks), 1)
    return (round(sum(1 for t in toks if len(t) >= 18) / n, 4),
            round(sum(1 for t in toks if len(t) == 1) / n, 3),
            len(re.findall(r"\(cid:\d+\)", text)))


print(f"{'file':60s} {'tol3 long/one/cid':>24s} {'tol1.5 long/one/cid':>24s}")
for pdf in sorted(SRC.glob("*.pdf")):
    with pdfplumber.open(pdf) as doc:
        a = "\n".join(p.extract_text() or "" for p in doc.pages)
        b = "\n".join(p.extract_text(x_tolerance=1.5) or "" for p in doc.pages)
    if not a.strip():
        continue
    print(f"{pdf.stem[:60]:60s} {str(stats(a)):>24s} {str(stats(b)):>24s}", flush=True)
