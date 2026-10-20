"""Test candidate fixes: extraction tolerance / pymupdf for spacing; Caesar decode; References block-cut length."""
import re
import sys
from pathlib import Path

import pdfplumber

SRC = Path("repository/monetary_policy/raw_pdf/theorical_literature")
D = Path(sys.argv[1])
sys.path.insert(0, str(Path("repository/ingestion/scripts").resolve()))
import clean_code  # noqa: E402

try:
    import fitz  # pymupdf
except ImportError:
    fitz = None
print("pymupdf available:", fitz is not None)


def long_share(text):
    toks = re.findall(r"[A-Za-z]+", text)
    return round(sum(1 for t in toks if len(t) >= 18) / max(len(toks), 1), 4), round(sum(1 for t in toks if len(t) == 1) / max(len(toks), 1), 3)


TARGETS = ["basic_nk_model_ch3 (Gali, 2015)", "information_effect_hf_identification (Nakamura & Steinsson, 2018)",
           "it_and_debt_brazil (Favero & Giavazzi, 2004)", "policy_rules_real_time_data (Orphanides, 2001)",
           "time_inconsistency_optimal_plans (Kydland & Prescott, 1977)"]
print("\n=== spacing: (long-token share, one-letter share) ===")
for stem in TARGETS:
    pdf = SRC / f"{stem}.pdf"
    res = {}
    with pdfplumber.open(pdf) as doc:
        pages = doc.pages[:12]
        for tol in (3, 1.5, 1):
            res[f"plumber x_tol={tol}"] = long_share("\n".join(p.extract_text(x_tolerance=tol) or "" for p in pages))
        res["plumber words(use_text_flow)"] = long_share("\n".join(
            " ".join(w["text"] for w in p.extract_words(x_tolerance=1.5, use_text_flow=True)) for p in pages))
    if fitz:
        with fitz.open(pdf) as doc:
            res["pymupdf"] = long_share("\n".join(doc[i].get_text() for i in range(min(12, len(doc)))))
    print(stem)
    for k, v in res.items():
        print(f"   {k:32s} {v}")

if fitz:
    with fitz.open(SRC / "basic_nk_model_ch3 (Gali, 2015).pdf") as doc:
        t = doc[2].get_text()
    print("\n=== pymupdf sample, Gali ch3 p3 ===\n", t[:900])

print("\n=== Caesar decode test (CGG 1999) ===")
txt = (D / "science_of_monetary_policy (Clarida, Gali & Gertler, 1999).raw.md").read_text(encoding="utf-8")
dec = "".join(chr(ord(c) + 29) if 0 < ord(c) < 128 and c not in "\n" else c for c in txt[:0])  # placeholder
print("raw sample:", repr(txt[3000:3200]))

print("\n=== References block-cut length per file (lines removed by the cut) ===")
for f in sorted(D.glob("*.raw.md")):
    lines = f.read_text(encoding="utf-8").splitlines()
    start = None
    for i, l in enumerate(lines):
        if clean_code._BLOCK_TRIGGERS.match(l.strip()):
            start = i
            break
    if start is None:
        continue
    end = None
    for j in range(start + 1, len(lines)):
        s = lines[j].strip()
        if s and clean_code._HEADING_LIKE_RE.match(s) and not clean_code._BLOCK_TRIGGERS.match(s):
            end = j
            break
    cut = (end or len(lines)) - start
    after = len(lines) - start
    stopped = lines[end].strip()[:40] if end else "EOF"
    # prose-like lines inside the cut that are not citations
    body = lines[start:(end or len(lines))]
    appendix = [k for k, l in enumerate(body) if re.match(r"^\s*(Appendix|APPENDIX|A\s*\.?\d?\s+[A-Z]|Table\s+\d|Figure\s+\d|TABLE|FIGURE)", l)]
    print(f"{f.stem[:-4][:70]:70s} cut {cut:5d} of {after:5d} lines after ref; stopped at: {stopped!r}; appendix/table/figure lines inside cut: {len(appendix)}")
