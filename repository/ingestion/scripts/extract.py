"""
Step 1 — Extract text from a PDF (or pass a .txt/.md through) into raw .md.

No AI and no rewriting: every character comes from the PDF's own text layer.
What can vary is HOW the text layer is read, because PDFs encode it in ways
that break a single default. The modes, all measured on the 46 monetary-policy
PDFs on 2026-10-19 (see repository/ingestion/CLAUDE.md):

  plumber       pdfplumber's extract_text, with x_tolerance (default 1.5).
                The library default (3) glued words together in ~20 of the 46
                files ("AnaturalinterpretationofthisevidenceisthatFOMC..."); 1.5
                removed it in all of them and made none worse.
  plumber_flow  pdfplumber's extract_words(use_text_flow=True), lines rebuilt
                by vertical position. For PDFs that place every letter as its
                own word (Orphanides 2001: one-letter share 98% -> 4.5%).
  pymupdf       PyMuPDF's get_text. Math symbols come out as Unicode (σ, β, π)
                where pdfplumber prints "(cid:12)", at the cost of equations
                spread over several lines. For math-heavy sources.
  ocr           Ignores the text layer: each page is rendered at 300 dpi
                (PyMuPDF) and read by Tesseract (`--psm 1`, which turns a
                rotated page upright first). For scans with no or a broken text
                layer, and for fonts whose encoding loses characters (Tambakis &
                Tarashev 2012 printed 0.005 as "0005"). Deterministic for a given
                Tesseract version, so the version is part of the setting; the
                text is still code's, not a model's. Tesseract is a program, not
                a Python package: `winget install UB-Mannheim.TesseractOCR`.

decode_shift=N reverses a font-encoding Caesar shift (every character code +N),
page by page and only where it helps: a page is decoded when the decoded text
has a higher share of common English words. Clarida-Gali-Gertler 1999/2000 need
N=3 ("wkh" -> "the").

Usage (CLI, for one file):
    uv run python repository/ingestion/scripts/extract.py <pdf> <dest.md> [--mode pymupdf] [--x-tolerance 1.5] [--decode-shift 3]
"""

import argparse
import re
from pathlib import Path

import pdfplumber

MODES = ("plumber", "plumber_flow", "pymupdf", "ocr")
OCR_DPI = 300
_TESSERACT_DEFAULT = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
SUPPORTED = {".pdf", ".txt", ".md"}

_COMMON = frozenset({"the", "and", "of", "to", "in", "is", "that", "a", "for", "on", "with", "as", "by", "this", "be"})


def common_word_share(text: str) -> float:
    toks = re.findall(r"[A-Za-z]+", text)
    return sum(1 for t in toks if t.lower() in _COMMON) / len(toks) if toks else 0.0


def _shift(text: str, n: int) -> str:
    # Shift only printable ASCII; a result below the space stays as it was.
    out = []
    for c in text:
        o = ord(c)
        out.append(chr(o - n) if 33 <= o <= 126 and o - n >= 32 else c)
    return "".join(out)


def _decode_page(text: str, n: int) -> str:
    dec = _shift(text, n)
    return dec if common_word_share(dec) > common_word_share(text) else text


def _flow_text(page, x_tolerance: float) -> str:
    words = page.extract_words(x_tolerance=x_tolerance, use_text_flow=True, keep_blank_chars=False)
    lines, cur, top = [], [], None
    for w in words:
        if top is not None and abs(w["top"] - top) > 3:
            lines.append(" ".join(cur))
            cur = []
        cur.append(w["text"])
        top = w["top"]
    if cur:
        lines.append(" ".join(cur))
    return "\n".join(lines)


def tesseract() -> str:
    import shutil
    exe = shutil.which("tesseract") or (str(_TESSERACT_DEFAULT) if _TESSERACT_DEFAULT.exists() else None)
    if not exe:
        raise RuntimeError("mode 'ocr' needs Tesseract: winget install UB-Mannheim.TesseractOCR")
    return exe


OCR_CONF_MIN = 60   # mean word confidence; an upright page reads 75-96, a sideways table 39


def _ocr_image(exe: str, page, angle: int, work: Path) -> tuple[str, float]:
    """(text, mean word confidence) of one page rendered at `angle` degrees."""
    import subprocess
    import fitz  # PyMuPDF
    png = page.get_pixmap(matrix=fitz.Matrix(OCR_DPI / 72, OCR_DPI / 72).prerotate(angle)).tobytes("png")
    base = work / "page"
    subprocess.run([exe, "stdin", str(base), "--psm", "1", "-l", "eng", "txt", "tsv"],
                   input=png, capture_output=True, check=True)
    conf = [float(c[10]) for c in (l.split("\t") for l in base.with_suffix(".tsv").read_text(encoding="utf-8").splitlines()[1:])
            if len(c) > 11 and c[11].strip() and float(c[10]) >= 0]
    text = base.with_suffix(".txt").read_text(encoding="utf-8").replace("\x0c", "")   # form feed at page end
    return text, (sum(conf) / len(conf) if conf else 0.0)


def _ocr_pages(path: Path) -> list[str]:
    import tempfile
    import fitz  # PyMuPDF
    exe = tesseract()
    out = []
    with fitz.open(path) as doc, tempfile.TemporaryDirectory() as d:
        for page in doc:
            # `--psm 1` turns most rotated pages upright by itself, but not a sideways table in a
            # degraded scan (Fama 1984, p.6: confidence 39 as is, 75 turned by 90 degrees). Below
            # OCR_CONF_MIN the other three orientations are tried and the most confident one kept.
            best = _ocr_image(exe, page, 0, Path(d))
            if best[1] < OCR_CONF_MIN:
                best = max([best] + [_ocr_image(exe, page, a, Path(d)) for a in (90, 180, 270)], key=lambda x: x[1])
            out.append(_ocr_tidy(best[0]))
    return out


def _ocr_tidy(text: str) -> str:
    # Tesseract puts a blank line between most lines of a scan (Walsh 1995). The cleaner reads a
    # blank line as a page edge and drops bare numbers there as page numbers, which in a table
    # read one column per line (Fama 1984, Table 2) would delete the numbers: the blank lines go,
    # and pages_text's joiner marks the real page edges, as in the other modes.
    text = "\n".join(l for l in text.splitlines() if l.strip())
    # Tesseract reads a minus sign as a dash: "—0.67***" in a table, "between —0.5 and —3.2" in
    # the text (Tambakis & Tarashev 2012). A dash glued to a number and not to a word is a minus;
    # "1990—2000" keeps its dash.
    return re.sub(r"(?<![\w.,)])[—–](?=\d)", "-", text)


def pages_text(path: Path, mode: str = "plumber", x_tolerance: float = 1.5, decode_shift: int = 0) -> list[str]:
    """One string per page, in page order (empty string for a page with no text layer)."""
    if mode not in MODES:
        raise ValueError(f"unknown mode {mode!r}; expected one of {MODES}")
    if mode == "ocr":
        pages = _ocr_pages(path)
    elif mode == "pymupdf":
        import fitz  # PyMuPDF
        with fitz.open(path) as doc:
            pages = [p.get_text() for p in doc]
    else:
        with pdfplumber.open(path) as pdf:
            if mode == "plumber":
                pages = [p.extract_text(x_tolerance=x_tolerance) or "" for p in pdf.pages]
            else:
                pages = [_flow_text(p, x_tolerance) for p in pdf.pages]
    # PyMuPDF emits a lone "\r" for some math glyphs. Reading the file back (universal newlines)
    # turns it into "\n" (and "\r\n" into "\n\n", since writing adds its own "\r"), so the text on
    # disk stopped matching a fresh extraction. Normalize here, to what the files written before
    # this fix already hold.
    pages = [t.replace("\r", "\n") for t in pages]
    if decode_shift:
        pages = [_decode_page(t, decode_shift) for t in pages]
    return pages


def extract_text(source: Path, mode: str = "plumber", x_tolerance: float = 1.5, decode_shift: int = 0) -> str:
    suffix = source.suffix.lower()
    if suffix == ".pdf":
        pages = pages_text(source, mode, x_tolerance, decode_shift)
        return "\n\n".join(t.strip() for t in pages if t.strip())
    if suffix in {".txt", ".md"}:
        return source.read_text(encoding="utf-8", errors="replace")
    raise ValueError(f"Unsupported file type: {suffix}")


def extract(source: Path, dest: Path, mode: str = "plumber", x_tolerance: float = 1.5, decode_shift: int = 0) -> int:
    """Write the extraction of one file to dest (.md). Returns the character count."""
    text = extract_text(Path(source), mode, x_tolerance, decode_shift)
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    return len(text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract one PDF/text file to raw .md.")
    parser.add_argument("source")
    parser.add_argument("dest")
    parser.add_argument("--mode", default="plumber", choices=MODES)
    parser.add_argument("--x-tolerance", type=float, default=1.5)
    parser.add_argument("--decode-shift", type=int, default=0)
    a = parser.parse_args()
    n = extract(Path(a.source), Path(a.dest), a.mode, a.x_tolerance, a.decode_shift)
    print(f"{n:,} chars -> {a.dest}")
