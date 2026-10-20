"""
repository/ingestion/scripts/clean_code.py — Code-only cleaning (no AI).

Applies deterministic regex rules to raw PDF-extracted .md files.
Works in two passes:
  1. Tail-cut: once a known boilerplate section heading is found, discard to EOF.
  2. Line-level: remove individual lines (emails, phones, URLs, watermarks,
     known disclaimer phrases, chart garbage clusters).

Block-level removal is intentionally avoided because banks often embed
one-line disclaimers in the same paragraph block as content (no blank line
separator), which would cause an entire block-level match to erase content.

Limitations vs AI pipeline:
  - Continuation lines of multi-line disclaimers may partially survive.
  - Chart garbage (axis labels, table numbers) may partially survive.
  - Analyst contact info interleaved mid-sentence with content is hard to isolate.
"""

import re
from collections import Counter
from pathlib import Path


# ── Tail-cut triggers ────────────────────────────────────────────────────────
# First standalone line matching any of these → everything from that point to
# EOF is discarded. Reserved for sections that are always genuinely last in a
# document (legal/regulatory back-matter). Covers Goldman and Itaú disclosure
# sections.
_TAIL_TRIGGERS = re.compile(
    r"""^(
        Disclosure\s+Appendix |
        Reg\s+AC |
        Disclosures? |
        Regulatory\s+Disclosures? |
        Global\s+product[;,]?\s*(distributing\s+entities)? |
        General\s+Disclosures? |
        Relevant\s+Information
    )$""",
    re.IGNORECASE | re.VERBOSE,
)

# ── Block-cut triggers ───────────────────────────────────────────────────────
# First standalone line matching any of these → removed along with everything
# up to (not including) the NEXT heading-like line, rather than to EOF.
# References/Bibliography are not reliably the last section of a document —
# e.g. a CFA curriculum reading orders it Summary -> References -> Practice
# Problems -> Solutions, so a to-EOF cut here would wrongly swallow the
# Practice Problems/Solutions that follow. See _HEADING_LIKE_RE below.
_BLOCK_TRIGGERS = re.compile(
    r"""^
    # an optional section number: "6 References" (Holston et al. 2017, Favero & Giavazzi
    # 2004 under plumber), "8 - References" (Muinhos & Nakane 2006), "8. References"
    (\d{1,2}(\.\d{1,2})*\s*[-.–]?\s*)?
    (
        Bibliography |
        References?
    )$""",
    re.IGNORECASE | re.VERBOSE,
)

# A line that plausibly starts the NEXT section — used to know where a block
# trigger's removal should stop. Deliberately permissive (mostly-uppercase,
# short) since section headings in these raw extractions are reliably
# all-caps standalone lines (SUMMARY, PRACTICE PROBLEMS, SOLUTIONS, APPENDIX).
_HEADING_LIKE_RE = re.compile(r"^[A-Z][A-Z0-9 ,.&/'\-]{2,60}$")

# ...but not always all-caps. A Brookings paper follows its References with
# "Comments and Discussion" in mixed case, and without this list the cut ran to
# EOF and deleted the discussants' comments — ~1,150 lines of Campbell et al.
# (2012), a third of the document, with nothing reporting it (measured
# 2026-10-19). Mixed-case section starters that end a References block:
_NEXT_SECTION_RE = re.compile(
    r"""^(
        # (\s|:|$), not \b: a wrapped citation line 'Appendix," IMF Country Report ...'
        # (Belaisch 2003) is not a heading.
        (Online\s+|Data\s+|Technical\s+|Mathematical\s+)?Appendi(x|ces)(\s|:|$) |
        Comments?\s+and\s+Discussion\b |
        Comment\s+By\b |
        General\s+Discussion\b |
        Tables?\s*$ |
        Figures?\s*$ |
        (Tables?|Figures?)\s+(and|&)\s+(Tables?|Figures?)\s*$ |
        # Added 2026-10-19 from three monetary-policy papers whose content follows the list:
        # Mishkin (2000) "Endnotes", Kohlscheen (2014) "Data Sources" then "Figure 1 - ...",
        # Minella & Souza-Sobrinho (2013) appendix tables whose first line is "Coefficient"
        # (pymupdf puts the caption "Table 1." below the table body).
        (End|Foot)?notes\s*$ |
        Data\s+Sources?\s*$ |
        # A lettered appendix after the list (Miranda-Agrippino & Rey 2020):
        # "A Credit and Banking Data – For Online Publication", "A.1 Domestic and Cross-Border Credit"
        .*\bFor\s+Online\s+Publication\b |
        [A-Z]\.\d+\s+[A-Z] |
        (Table|Figure|Fig\.?|Chart|Graph|Exhibit)\s+[A-Z]?\d+\b |
        Coefficients?\s*$
    )""",
    re.IGNORECASE | re.VERBOSE,
)


def _ocr_references(s: str) -> bool:
    """An OCR misreading of the heading: "Refermces" (Calvo 1983). Starts with "Ref" so that
    "Preferences", a heading of its own in a model section, never matches."""
    import difflib
    w = s.strip(" .:").lower()
    return (w.startswith("ref") and " " not in w and w not in ("reference", "references")
            and difflib.SequenceMatcher(None, w, "references").ratio() >= 0.8)


def block_cut_spans(lines: list[str]) -> list[tuple[int, int, str]]:
    """Every References/Bibliography block the cleaner removes, as
    (start line, end line exclusive, the line that ended it or 'EOF').
    Shared by clean() and the QC report, so the report describes the cut the
    cleaner actually makes."""
    spans: list[tuple[int, int, str]] = []
    start = None
    # A running head is all caps too, and inside a long list it ended the cut after one page:
    # "POLICY IN THE OPEN ECONOMY" left ~100 reference lines of Gali (2015) ch. 8 in the text.
    running = _detect_running_headers(lines)
    for i, line in enumerate(lines):
        s = line.strip()
        if start is None:
            if s and (_BLOCK_TRIGGERS.match(s) or _ocr_references(s)):
                start = i
            continue
        # "CHAPTER 3" is Gali's even-page running head, too short for the detector.
        if s in running or _RUNNING_HEADER_RE.match(s) or re.match(r"^CHAPTER\s+\d+$", s):
            continue
        # A one-word ALL-CAPS line must be a word, not an acronym: pymupdf printed a reference
        # one word per line in Gali (2015) ch. 7, and "ECB" ended the cut 70 lines early.
        heading = _HEADING_LIKE_RE.match(s) and (" " in s or len(s) >= 6)
        if s and not _BLOCK_TRIGGERS.match(s) and (heading or _NEXT_SECTION_RE.match(s)):
            spans.append((start, i, s))
            start = None
    if start is not None:
        spans.append((start, len(lines), "EOF"))
    return spans

# ── Line-level removal ────────────────────────────────────────────────────────
# Known inline disclaimer sentence starters (first line of multi-line disclaimers).
# Continuation lines may survive — accepted trade-off vs. block-level removal,
# which risks erasing content when disclaimers are embedded without blank lines.
_INLINE_DISCLAIMER_RE = re.compile(
    r"""^(
        Investors\s+should\s+consider\s+this\s+report\s+as\s+only\s+a\s+single\s+factor |
        Please\s+refer\s+to\s+the\s+last\s+page\s+of\s+this\s+report\s+for\s+important |
        Itaú\s+Unibanco\s+or\s+its\s+subsidiaries\s+may\s+do\s+or\s+seek |
        This\s+report\s+has\s+been\s+prepared\s+and\s+released\s+by |
        The\s+exclusive\s+purpose\s+of\s+this\s+report\s+is\s+to\s+provide |
        The\s+opinions\s+contained\s+herein\s+reflect\s+exclusively |
        This\s+report\s+may\s+not\s+be\s+reproduced\s+or\s+redistributed |
        Additional\s+Note:\s+This\s+material\s+does\s+not\s+take\s+into\s+consideration |
        For\s+inquiries,\s+suggestions,\s+complaints |
        We,\s+\w+.*?\bhereby\s+certify\b |
        Unless\s+otherwise\s+stated,\s+the\s+individuals\s+listed\s+on\s+the\s+cover |
        Macro\s+Research\s+[–\-]\s+Itaú |
        Fernando\s+M\.\s+Goncalves |
        Julia\s+Gottlieb |
        Pedro\s+Schneider |
        Thales\s+Guimarães |
        Mario\s+Mesquita |
        # Continuation lines of known multi-line disclaimers
        certification\s+and\s+other\s+important\s+disclosures,\s+see\s+the\s+Disclosure |
        do\s+business\s+with\s+companies\s+covered\s+in\s+this\s+research\s+report |
        affect\s+the\s+objectivity\s+of\s+this\s+report
    )""",
    re.IGNORECASE | re.VERBOSE,
)

_EMAIL_RE   = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
_PHONE_RE   = re.compile(r"(\+\d[\d\s\(\)\-\.]{6,}\d|0800[\s\-]\d{3}[\s\-]\d{4})")
_URL_RE     = re.compile(r"(https?://|www\.)\S+")
_PAGE_NUM_RE = re.compile(r"^\s*\d{1,4}\s*$")
# "3 November 2025 2" — Goldman date+page footer
_DATE_PAGE_RE = re.compile(r"^\d{1,2}\s+\w+\s+\d{4}\s+\d{1,3}$")
# Goldman reversed watermark "PEDRO.LINZMEYER@LISCAPITAL.COM.BR" backwards
_WATERMARK_RE = re.compile(r"^RB\.MOC\.", re.IGNORECASE)
# MD5-like hash token
_HASH_RE = re.compile(r"^[a-f0-9]{32}$")
# "Source: ..." attribution lines
_SOURCE_RE = re.compile(r"^Source:\s*", re.IGNORECASE)
# Copyright symbols / lines. Not a bare "(": "(1995), Ireland (1996a), ..." is a body line
# that starts with a citation year, and 150 of them were deleted across the corpus (2026-10-19).
_COPYRIGHT_RE = re.compile(r"^(©|\(c\)|Copyright\b)\s*\d{4}\b", re.IGNORECASE)
# JSTOR download notices (appear on every page, embedded in content blocks)
_JSTOR_DOWNLOAD_RE = re.compile(r"^This\s+content\s+downloaded\s+from\s+\d+\.\d+", re.IGNORECASE)
_JSTOR_TNC_RE = re.compile(r"^All\s+use\s+subject\s+to\b", re.IGNORECASE)
# Journal / publisher attribution lines
_JOURNAL_ATTR_RE = re.compile(r"^\[Journal\s+of\s+Political\s+Economy", re.IGNORECASE)
# Textbook layout-software export stamps, e.g. "M17_KRUG9719_12_GE_C17.indd 542 17/11/2021 16:14"
_INDD_STAMP_RE = re.compile(r"\.indd\s+\d+.*\d{1,2}:\d{2}", re.IGNORECASE)

# Running headers — also matches JSTOR-style "Ii62 JOURNAL OF POLITICAL ECONOMY" prefixes
_RUNNING_HEADER_RE = re.compile(
    r"^(\w+\s+)?(Goldman\s+Sachs\s+FX\s+in\s+Focus|"
    r"Goldman\s+Sachs\s+Global\s+Investment\s+Research|"
    r"Macro\s+Vision\s*\|.*|"
    r"JOURNAL\s+OF\s+POLITICAL\s+ECONOMY|"
    r"EXPECTATIONS\s+AND\s+EXCHANGE\s+RATE\s+DYNAMICS\b.*)$",
    re.IGNORECASE,
)

# Marks of an equation: operators, brackets, Greek letters, math symbols, unmapped glyphs.
_MATH_RE = re.compile(r"[=+<>()\[\]{}^ˆͰ-Ͽ∀-⋿]|\(cid:")

# Reversed text fragments from Goldman's "For the exclusive use of" watermark
_REVERSED_WORDS = frozenset({"fo", "esu", "evisulcxe", "eht", "rof"})


def _is_chart_garbage(line: str) -> bool:
    """
    Detect space-fragmented single-char sequences from pdfplumber chart extraction.
    E.g.: 'S e l i c', '2 0 2 1 2 0 2 2', '6 .0 5 .0 4 .0'
    Heuristic: ≥5 tokens, ≥70% of them are 1-2 chars long.
    """
    stripped = line.strip()
    if len(stripped) < 5:
        return False
    # An equation has the same short tokens ("πt = κxt + υt", "r = p + .5y + .5(p - 2) + 2"),
    # and this rule deleted Taylor's rule from Taylor (1993) among ~870 lines (2026-10-19).
    if _MATH_RE.search(stripped):
        return False
    tokens = stripped.split()
    if len(tokens) < 5:
        return False
    # ...and prose with short words: "1 to t. In the equilibrium we" (Gertler & Karadi 2011).
    if any(sum(ch.isalpha() for ch in t) >= 4 for t in tokens):
        return False
    short = sum(1 for t in tokens if len(t) <= 2)
    return short / len(tokens) >= 0.70


def _line_should_remove(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    # _PAGE_NUM_RE is checked in clean(), which knows whether the line sits at a page edge.
    if _DATE_PAGE_RE.match(stripped):
        return True
    if _WATERMARK_RE.match(stripped):
        return True
    if _HASH_RE.match(stripped):
        return True
    # "Source:" lines are kept since 2026-10-19: under a paper's chart or table they say where
    # the data come from ("Source: Authors' calculations."), which is content.
    if _COPYRIGHT_RE.match(stripped):
        return True
    if _JSTOR_DOWNLOAD_RE.match(stripped):
        return True
    if _JSTOR_TNC_RE.match(stripped):
        return True
    if _JOURNAL_ATTR_RE.match(stripped):
        return True
    if _RUNNING_HEADER_RE.match(stripped):
        return True
    if _INLINE_DISCLAIMER_RE.match(stripped):
        return True
    if stripped.lower() in _REVERSED_WORDS:
        return True
    if _EMAIL_RE.search(stripped):
        return True
    if _PHONE_RE.search(stripped):
        return True
    if _URL_RE.search(stripped):
        return True
    if _INDD_STAMP_RE.search(stripped):
        return True
    if _is_chart_garbage(stripped):
        return True
    return False


def _strip_digits(s: str) -> str:
    # "'" and "`": OCR reads a page number as "49'" (Kydland & Prescott 1977)
    return re.sub(r"\d+", "", s).strip(" .-|'’`")


def _detect_running_headers(
    lines: list[str],
    min_occurrences: int = 3,
    min_len: int = 10,
    max_len: int = 120,
) -> set[str]:
    """
    Generic running-header/footer detector: finds short lines that recur many
    times across the document, tolerating a varying leading/trailing page
    number (e.g. "478 Canadian Journal of Economics and Political Science" and
    "Capital Mobility and Stabilization Policy 479" both normalize to the same
    digit-stripped key). Complements the hand-tuned _RUNNING_HEADER_RE, which
    only catches exact, already-known titles.

    Returns the set of original (stripped) line strings to remove. A generic
    heuristic like this can misfire on short repeated content that isn't a
    header (e.g. a subsection label reused verbatim) — accepted trade-off,
    same spirit as this module's existing block-level heuristics.
    """
    counts: Counter = Counter()
    originals: dict[str, set[str]] = {}
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        norm = _strip_digits(stripped)
        if not (min_len <= len(norm) <= max_len):
            continue
        # A running head is words. Rows of a numeric table share their digit-stripped shape
        # ("FF4 17.930 [6.675 22.673]" → "FF . [. .]") and were all deleted as one header.
        if sum(ch.isalpha() for ch in norm) < 6:
            continue
        counts[norm] += 1
        originals.setdefault(norm, set()).add(stripped)

    to_remove: set[str] = set()
    for norm, count in counts.items():
        if count >= min_occurrences:
            to_remove.update(originals[norm])
    return to_remove


def _is_axis_fragment(line: str) -> bool:
    s = line.strip()
    return _is_chart_garbage(s) or (len(s) <= 4 and s.replace(".", "").replace(",", "").replace("%", "")
                                    .replace("-", "").replace("–", "").replace("−", "").strip().replace(" ", "").isdigit())


def _block_is_garbage(lines: list[str]) -> bool:
    """
    Detect chart-artifact blocks: short blocks where most lines are numeric/
    single-char fragments from garbled chart axis labels.
    """
    if len(lines) < 4:
        return False
    return sum(1 for ln in lines if _is_axis_fragment(ln)) / len(lines) >= 0.6


def clean(text: str) -> str:
    """Apply all code-based rules. Returns cleaned text."""
    lines = text.splitlines()
    running_headers = _detect_running_headers(lines)
    cut = {i for a, b, _ in block_cut_spans(lines) for i in range(a, b)}

    # Pass 1: line-by-line — tail trigger + individual line removal.
    # Tail trigger is checked per-line (not per-block first-line) because bank
    # reports often put the trigger heading on line 2 of a block with no blank
    # line separator (e.g. "Goldman Sachs FX in Focus\nDisclosure Appendix").
    def at_page_edge(i: int) -> bool:
        # Pages are joined with a blank line (extract.py), so a page's first or last line
        # touches one. A bare number elsewhere is a table cell or an equation term, not a page
        # number: pymupdf prints one table cell per line, and every "0" and "1984" was deleted.
        return i == 0 or i == len(lines) - 1 or not lines[i - 1].strip() or not lines[i + 1].strip()

    def near_page_edge(i: int) -> bool:
        # A running head can sit one line in, next to its page number ("88" / "CHAPTER 3").
        return any(at_page_edge(j) for j in range(max(0, i - 1), min(len(lines), i + 2)))

    pass1: list[str] = []
    seen_headers: set[str] = set()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and _TAIL_TRIGGERS.match(stripped):
            break  # discard everything from here to EOF
        if i in cut:
            continue  # inside a References/Bibliography block (heading included)
        if not stripped:
            pass1.append("")
        elif stripped in running_headers and near_page_edge(i):
            # A running head sits at the top or bottom of a page. A repeated line inside a
            # page is content (a table's row label, "Adj. R-Squared" under every table) and
            # is kept. At the edge, keep the first copy anyway: a figure note repeated under
            # every chart page is content too, and one stray running head costs less.
            if stripped not in seen_headers:
                seen_headers.add(stripped)
                pass1.append(line)
        elif _PAGE_NUM_RE.match(stripped) and at_page_edge(i):
            continue
        elif not _line_should_remove(line):
            pass1.append(line)

    # Pass 2: garbage-cluster removal over the filtered lines.
    # Collect consecutive non-blank lines into blocks; drop blocks where ≥60%
    # of lines are chart-artifact garbage (space-fragmented single chars).
    pass2: list[str] = []
    block_buf: list[str] = []

    def _flush(buf: list[str]) -> None:
        if _block_is_garbage(buf):
            # Drop the axis fragments only, never the whole block: pymupdf returns a page as
            # one block, so a chart page took its caption and the prose around it along
            # (826 lines of Jarocinski & Karadi 2020 in a trial, 2026-10-19).
            pass2.extend(ln for ln in buf if not _is_axis_fragment(ln))
        else:
            pass2.extend(buf)

    for line in pass1:
        if line.strip() == "":
            if block_buf:
                _flush(block_buf)
                block_buf = []
            pass2.append("")
        else:
            block_buf.append(line)
    if block_buf:
        _flush(block_buf)

    # Collapse 3+ consecutive blank lines into 2
    output = "\n".join(pass2)
    output = re.sub(r"\n{3,}", "\n\n", output)
    return output.strip()


def clean_file(source: str | Path, output_dir: str | Path | None = None) -> Path:
    """
    Clean a single raw .md file with code-only rules.
    Strips '_raw' suffix from output filename (same convention as AI pipeline).
    Returns path to output file.
    """
    source = Path(source)
    text = source.read_text(encoding="utf-8")
    cleaned = clean(text)

    stem = source.stem
    base = stem[:-4] if stem.endswith("_raw") else stem

    dest_dir = Path(output_dir) if output_dir else source.parent
    dest_dir.mkdir(parents=True, exist_ok=True)
    out = dest_dir / f"{base}.md"
    out.write_text(cleaned, encoding="utf-8")
    return out
