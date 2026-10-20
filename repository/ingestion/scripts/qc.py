"""
Quality control for the ingestion pipeline. Reads, never writes into repository/ or obsidian/.

The numbers below are what separated a good extraction from a broken one on the 46
monetary-policy PDFs (2026-10-19). A healthy academic paper sits at a common-word
share of 0.20-0.32, under 0.3% of 18+-letter tokens and a cleaner removal under ~20%.

Subcommands:
    try    <pdf> [--modes plumber,pymupdf,...] [--decode-shift N]
           Extract with each mode into a temp folder, clean, and print the metrics side by
           side. Nothing is written to the repository. The temp paths are printed so the
           candidate raw/clean text can be read before choosing.
    page   <pdf> <n> [--mode ...] [--x-tolerance ...] [--decode-shift ...]
           Print the extracted text of page n (1-based) under the given settings (default:
           the file's entry in settings.yaml), to compare against the rendered image.
    render <pdf> <pages> [--out DIR] [--dpi 110]
           Render pages ("3", "3,7,12" or "3-5") to PNG and print their paths, for the Read
           tool. Uses PyMuPDF, so it does not need poppler.
    check  <topic> <name>
           Metrics of an ingested file (raw_md + clean_md + the PDF), including every
           References cut the cleaner made and the line that ended it.

    uv run python repository/ingestion/scripts/qc.py try "repository/monetary_policy/raw_pdf/x (A, 2001).pdf"
"""

import argparse
import json
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clean_code import block_cut_spans, clean  # noqa: E402
from extract import MODES, common_word_share, pages_text  # noqa: E402
from settings import settings_for  # noqa: E402

SCRIPTS = Path(__file__).resolve().parent
REPOSITORY = SCRIPTS.parent.parent
ROOT = REPOSITORY.parent

# Thresholds, from the 2026-10-19 measurement (see the module docstring).
EMPTY_PAGES_MAX = 0.20     # scanned PDFs: 100% empty; Gali & Monacelli has 13% (full-page figures)
COMMON_MIN = 0.15          # CGG shifted: 0.001; Orphanides letter-spaced: 0.088
ONE_LETTER_MAX = 0.35      # Orphanides: 0.98; Gali chapters (heavy math): up to 0.27
LONG_TOKEN_MAX = 0.002     # glued words at x_tolerance=3: 0.01-0.075
CID_INFO = 50              # math glyphs pdfplumber cannot map: informational, not an error
REMOVED_MAX = 25.0         # % of raw removed by the cleaner
CUT_LINES_MAX = 300        # one References cut longer than this deserves a look
REVERSED_MIN = 3           # backwards words on one page; noise in Chang (1998) reaches 2


def reversed_pages(pages: list[str]) -> list[tuple[int, list[str]]]:
    """Pages where pdfplumber read rotated text backwards ("elbaT" for "Table").
    A word counts when it is rare in the document read forwards and its reversal is common
    there, so the document is its own dictionary and Portuguese works as well as English.
    Measured 2026-10-20: rotated tables and chart axes give 3-50 such words on a page."""
    words = [re.findall(r"[A-Za-z]{4,}", p) for p in pages]
    vocab = Counter(w.lower() for ws in words for w in ws)
    out = []
    for n, ws in enumerate(words, 1):
        hits = [w for w in ws if vocab[w.lower()] <= 2 and vocab[w.lower()[::-1]] >= 3
                and w.lower() != w.lower()[::-1]]
        if len(hits) >= REVERSED_MIN:
            out.append((n, hits))
    return out


def text_metrics(text: str) -> dict:
    toks = re.findall(r"[A-Za-z]+", text)
    n = max(len(toks), 1)
    return {
        "chars": len(text),
        "common_word_share": round(common_word_share(text), 3),
        "one_letter_share": round(sum(1 for t in toks if len(t) == 1) / n, 3),
        "long_token_share": round(sum(1 for t in toks if len(t) >= 18) / n, 4),
        "cid_glyphs": len(re.findall(r"\(cid:\d+\)", text)),
    }


def cut_report(raw: str) -> list[dict]:
    lines = raw.splitlines()
    out = []
    for a, b, stop in block_cut_spans(lines):
        body = [l.strip() for l in lines[a + 1:b] if l.strip()]
        out.append({
            "from_line": a + 1, "to_line": b, "lines": b - a, "ended_by": stop[:70],
            "share_of_doc": round((b - a) / max(len(lines), 1), 3),
            "first": body[0][:90] if body else "", "last": body[-1][:90] if body else "",
        })
    return out


def flags(pages: list[str], raw: str, cleaned: str, cuts: list[dict]) -> list[str]:
    m = text_metrics(raw)
    f = []
    empty = sum(1 for t in pages if len(t.strip()) < 50) / max(len(pages), 1)
    if empty > EMPTY_PAGES_MAX:
        f.append(f"no_text_layer ({empty:.0%} of pages empty — scanned?)")
    if m["chars"] and m["common_word_share"] < COMMON_MIN:
        f.append(f"garbled (common-word share {m['common_word_share']})")
    if m["one_letter_share"] > ONE_LETTER_MAX:
        f.append(f"letter_spaced (one-letter share {m['one_letter_share']})")
    if m["long_token_share"] > LONG_TOKEN_MAX:
        f.append(f"run_together (long-token share {m['long_token_share']})")
    if m["cid_glyphs"] > CID_INFO:
        f.append(f"math_glyphs ({m['cid_glyphs']} unmapped symbols — consider pymupdf)")
    rev = reversed_pages(pages)
    if rev:
        f.append("reversed_text (" + ", ".join(f"p.{n}: {len(h)} words, e.g. {h[0]!r}" for n, h in rev[:5])
                 + (f", +{len(rev) - 5} pages" if len(rev) > 5 else "") + " — rotated text read backwards)")
    removed = 100 * (1 - len(cleaned) / len(raw)) if raw else 0
    if removed > REMOVED_MAX:
        f.append(f"heavy_removal ({removed:.0f}% removed by the cleaner)")
    for c in cuts:
        if c["lines"] > CUT_LINES_MAX or (c["ended_by"] == "EOF" and c["share_of_doc"] > 0.25):
            f.append(f"long_references_cut ({c['lines']} lines, ended by {c['ended_by']!r})")
    return f


def evaluate(pages: list[str]) -> dict:
    raw = "\n\n".join(t.strip() for t in pages if t.strip())
    cleaned = clean(raw)
    cuts = cut_report(raw)
    return {
        "pages": len(pages),
        "empty_pages": sum(1 for t in pages if len(t.strip()) < 50),
        **text_metrics(raw),
        "clean_chars": len(cleaned),
        "removed_pct": round(100 * (1 - len(cleaned) / len(raw)), 1) if raw else None,
        "references_cuts": cuts,
        "flags": flags(pages, raw, cleaned, cuts),
    }, raw, cleaned


def cmd_try(a):
    pdf = Path(a.pdf)
    modes = a.modes.split(",") if a.modes else list(MODES)
    work = Path(tempfile.gettempdir()) / "ingest_try" / pdf.stem
    work.mkdir(parents=True, exist_ok=True)
    print(f"# {pdf.name}\n")
    for mode in modes:
        res, raw, cleaned = evaluate(pages_text(pdf, mode, a.x_tolerance, a.decode_shift))
        (work / f"{mode}.raw.md").write_text(raw, encoding="utf-8")
        (work / f"{mode}.clean.md").write_text(cleaned, encoding="utf-8")
        cuts = res.pop("references_cuts")
        print(f"## mode={mode} x_tolerance={a.x_tolerance} decode_shift={a.decode_shift}")
        print(json.dumps(res, ensure_ascii=False))
        for c in cuts:
            print(f"   references cut: lines {c['from_line']}-{c['to_line']} ({c['lines']}), ended by {c['ended_by']!r}")
        print(f"   candidate: {work / (mode + '.raw.md')}\n")


def cmd_page(a):
    pdf = Path(a.pdf)
    s = settings_for(pdf.name)
    mode = a.mode or s["mode"]
    xt = a.x_tolerance if a.x_tolerance is not None else s["x_tolerance"]
    ds = a.decode_shift if a.decode_shift is not None else s["decode_shift"]
    pages = pages_text(pdf, mode, xt, ds)
    print(f"# page {a.n} of {len(pages)} · mode={mode} x_tolerance={xt} decode_shift={ds}\n")
    print(pages[a.n - 1])


def _parse_pages(spec: str) -> list[int]:
    out = []
    for part in spec.split(","):
        if "-" in part:
            lo, hi = part.split("-")
            out.extend(range(int(lo), int(hi) + 1))
        else:
            out.append(int(part))
    return out


def cmd_render(a):
    import fitz
    pdf = Path(a.pdf)
    out = Path(a.out) if a.out else Path(tempfile.gettempdir()) / "ingest_render" / pdf.stem
    out.mkdir(parents=True, exist_ok=True)
    with fitz.open(pdf) as doc:
        for n in _parse_pages(a.pages):
            if not 1 <= n <= len(doc):
                print(f"page {n}: out of range (1-{len(doc)})")
                continue
            p = out / f"p{n:03d}.png"
            doc[n - 1].get_pixmap(dpi=a.dpi).save(p)
            print(p)


def cmd_check(a):
    from run import paths                   # a manager's letters keep their clean_md in repository/
    pp = paths(a.topic, a.name)
    raw_p, clean_p, pdf_p = pp["raw"], pp["clean"], pp["pdf"]
    for p in (raw_p, clean_p, pdf_p):
        if not p.exists():
            sys.exit(f"missing: {p}")
    s = settings_for(pdf_p.name)
    pages = pages_text(pdf_p, s["mode"], s["x_tolerance"], s["decode_shift"])
    raw = raw_p.read_text(encoding="utf-8")
    cleaned = clean_p.read_text(encoding="utf-8")
    cuts = cut_report(raw)
    res = {
        "settings": s, "pages": len(pages), "empty_pages": sum(1 for t in pages if len(t.strip()) < 50),
        **text_metrics(raw), "clean_chars": len(cleaned),
        "removed_pct": round(100 * (1 - len(cleaned) / len(raw)), 1) if raw else None,
        "raw_reproduces_pdf": raw == "\n\n".join(t.strip() for t in pages if t.strip()),
        "clean_reproduces_raw": cleaned == clean(raw),
        "flags": flags(pages, raw, cleaned, cuts),
    }
    print(json.dumps(res, ensure_ascii=False, indent=1))
    for c in cuts:
        print(f"references cut: lines {c['from_line']}-{c['to_line']} ({c['lines']}), ended by {c['ended_by']!r}\n"
              f"   first: {c['first']}\n   last:  {c['last']}")


def main():
    # The Windows console is cp1252; a PDF's private-use bullet (U+F0B7) crashed `page`.
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("try"); t.add_argument("pdf"); t.add_argument("--modes")
    t.add_argument("--x-tolerance", type=float, default=1.5); t.add_argument("--decode-shift", type=int, default=0)
    p = sub.add_parser("page"); p.add_argument("pdf"); p.add_argument("n", type=int); p.add_argument("--mode", choices=MODES)
    p.add_argument("--x-tolerance", type=float); p.add_argument("--decode-shift", type=int)
    r = sub.add_parser("render"); r.add_argument("pdf"); r.add_argument("pages"); r.add_argument("--out"); r.add_argument("--dpi", type=int, default=110)
    c = sub.add_parser("check"); c.add_argument("topic"); c.add_argument("name")
    a = ap.parse_args()
    {"try": cmd_try, "page": cmd_page, "render": cmd_render, "check": cmd_check}[a.cmd](a)


if __name__ == "__main__":
    main()
