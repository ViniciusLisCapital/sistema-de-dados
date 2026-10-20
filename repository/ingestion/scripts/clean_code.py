"""
repository/ingestion/scripts/clean_code.py — Code-only cleaning (no AI).

clean_md is raw_md minus three things, and nothing else:
  1. the References/Bibliography blocks (block_cut_spans), each reported by qc.py check;
  2. a bank report's disclosure back-matter, from its heading to EOF (_TAIL_TRIGGERS);
  3. lines whose text is fixed publisher or bank boilerplate (_is_boilerplate): JSTOR notices,
     watermarks, layout stamps, known disclaimer sentences, known running heads.

No rule judges a line by its shape. Page numbers, running heads not listed by name, chart axis
numbers, URLs and contact lines stay: the shape rules that removed them also removed content
(see "Known boilerplate lines" below). When in doubt, the cleaner keeps the line.
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
    # 2004 under plumber), "8 - References" (Muinhos & Nakane 2006), "8. References",
    # or a Roman one: "VII. References" (Garcia & Valpassos 1998), "XI. References" (Goldfajn 2000)
    ((\d{1,2}(\.\d{1,2})*|[IVX]{1,5})\s*[-.–]?\s*)?
    (
        Bibliography |
        References? |
        Literature\s+Cited    # Annual Review and older journals (Broz & Frieden 2001, Krugman 1979)
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
        # A Roman section number may precede it: "X. Appendix" (Goldfajn 2000) is the model
        # appendix that follows "XI. References" in the text order.
        ([IVX]{1,5}\.\s*)?(Online\s+|Data\s+|Technical\s+|Mathematical\s+)?Appendi(x|ces)(\s|:|$) |
        Comments?\s+and\s+Discussion\b |
        Comment\s+By\b |
        # The heading alone, the discussant on the next line: "Comment" / "BY PETER GARBER" in
        # Krugman (2000, IMF Staff Papers); the cut ran on and deleted the comment's first page.
        Comments?\s*$ |
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


def _lowercase_words(s: str) -> int:
    return sum(1 for w in s.split() if re.fullmatch(r"[a-z][a-z'’\-]*[,.;:]?", w))


def _footnote_end(lines: list[str], i: int) -> int | None:
    """If a body footnote starts at line i, the line after its last; else None.

    A page's footnotes print below the reference list on that page, and the cut deleted them:
    Mundell (1961) "9Other economists have advanced arguments in favor of balkanization...",
    BIS (2026) "10" / "The online appendix shows that...". A footnote is its number (alone, or
    fused to the text) and a sentence, "Word word ..." with 6+ lowercase words; a reference
    entry starts "Surname, X" and never matches. It runs over the lines that continue it in
    lowercase. Measured 2026-10-20: these 4 footnotes, nothing else in the 79 files.
    """
    s = lines[i].strip()
    m = re.fullmatch(r"(\d{1,3})\s*(.*)", s)
    if not m:
        return None
    text, j = m.group(2), i + 1
    if not text:   # the number alone on its line, the text on the next
        while j < len(lines) and not lines[j].strip() and j < i + 3:
            j += 1
        if j >= len(lines):
            return None
        text, j = lines[j].strip(), j + 1
    # Mostly lowercase words: a cited title in Title Case is not a footnote ("3 On the Existence of
    # a Consistent Course of Action when Tastes are Changing", JSTOR's linked citations, 6 of 13).
    low = _lowercase_words(text)
    if not (re.match(r"^[A-Z][a-z]+ [a-z]", text) and len(text) >= 60 and low >= 6
            and low >= 0.6 * len(text.split())):
        return None
    while j < len(lines) and re.match(r"^[a-z]", lines[j].strip()):
        j += 1
    return j


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
    resume = None   # the line after a footnote kept from inside the list: the cut goes on there
    for i, line in enumerate(lines):
        s = line.strip()
        if start is None:
            if i != resume:
                if s and (_BLOCK_TRIGGERS.match(s) or _ocr_references(s)):
                    start = i
                continue
            start = i   # and fall through: the next footnote can follow at once (BIS 2026: 10, 11)
        end = _footnote_end(lines, i)
        if end is not None:
            if i > start:
                spans.append((start, i, s[:60]))
            start, resume = None, end
            if end >= len(lines):
                break
            continue
        # "CHAPTER 3" is Gali's even-page running head, too short for the detector.
        if s in running or _RUNNING_HEADER_RE.match(s) or re.match(r"^CHAPTER\s+\d+$", s):
            continue
        # A one-word ALL-CAPS line must be a word, not an acronym: pymupdf printed a reference
        # one word per line in Gali (2015) ch. 7, and "ECB" ended the cut 70 lines early.
        heading = _HEADING_LIKE_RE.match(s) and (" " in s or len(s) >= 6)
        # A wrapped citation tail is all caps too: "FEDS 2001-53." ended the cut of Perrelli &
        # Roache (2014) with ~75 references to go. A heading does not end in a year and a period.
        if heading and re.search(r"\b(19|20)\d\d\b.*\.$", s):
            heading = None
        if s and not _BLOCK_TRIGGERS.match(s) and (heading or _NEXT_SECTION_RE.match(s)):
            spans.append((start, i, s))
            start = None
    if start is not None:
        spans.append((start, len(lines), "EOF"))
    return spans

# ── Known boilerplate lines ──────────────────────────────────────────────────
# Since 2026-10-20 the cleaner removes only whole blocks (the References list above, the bank
# disclosure tail) and lines whose TEXT is fixed publisher or bank boilerplate. It no longer
# guesses from a line's shape: the shape rules (chart debris, axis numbers, page numbers,
# repeated lines, any line carrying a URL, e-mail or phone number) were 2.1% of the removal and
# every silent content loss found in three audits (2026-10-19, -20 twice): table cells
# ("0.83" dropped as an axis tick while "-0.24" stayed, so the surviving cells sat under the
# wrong row: Minella & Souza-Sobrinho 2013 Table 2, 717 of Rey 2013's 1,218 appendix cells),
# sentences that held a URL (Garcia & Valpassos 1998: "Therefore, the domestic interest rate is
# computed through the"), a table's totals row taken for a phone number ("(1+2+3) 28.5 29.9"),
# equations, footnotes, "Source:" lines. The knowledge base is read for its reasoning, and a
# page number or a running head left in the text costs a reader nothing; a lost sentence or a
# table whose cells moved costs the one reading that goes back to the source.

# Known inline disclaimer sentence starters (first line of multi-line disclaimers).
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
        # Continuation lines of known multi-line disclaimers
        certification\s+and\s+other\s+important\s+disclosures,\s+see\s+the\s+Disclosure |
        do\s+business\s+with\s+companies\s+covered\s+in\s+this\s+research\s+report |
        affect\s+the\s+objectivity\s+of\s+this\s+report
    )""",
    re.IGNORECASE | re.VERBOSE,
)

_MONTHS = r"(January|February|March|April|May|June|July|August|September|October|November|December)"
# "3 November 2025 2" — Goldman date+page footer
_DATE_PAGE_RE = re.compile(rf"^\d{{1,2}}\s+{_MONTHS}\s+\d{{4}}\s+\d{{1,3}}$", re.IGNORECASE)
# Goldman's "For the exclusive use of <e-mail>" watermark, and the same mark printed backwards
_EXCLUSIVE_USE_RE = re.compile(r"^For\s+the\s+exclusive\s+use\s+of\s+\S+@\S+$", re.IGNORECASE)
_WATERMARK_RE = re.compile(r"^RB\.MOC\.", re.IGNORECASE)
_REVERSED_WORDS = frozenset({"fo", "esu", "evisulcxe", "eht", "rof"})
# MD5-like hash token
_HASH_RE = re.compile(r"^[a-f0-9]{32}$")
# Copyright lines. Not a bare "(": "(1995), Ireland (1996a), ..." is a body line that starts
# with a citation year.
_COPYRIGHT_RE = re.compile(r"^(©|\(c\)|Copyright\b)\s*\d{4}\b", re.IGNORECASE)
# JSTOR download notices (appear on every page, embedded in content blocks)
_JSTOR_DOWNLOAD_RE = re.compile(r"^This\s+content\s+downloaded\s+from\s+\d+\.\d+", re.IGNORECASE)
_JSTOR_TNC_RE = re.compile(r"^All\s+use\s+subject\s+to\b", re.IGNORECASE)
# Journal / publisher attribution lines
_JOURNAL_ATTR_RE = re.compile(r"^\[Journal\s+of\s+Political\s+Economy", re.IGNORECASE)
# Textbook layout-software export stamps, e.g. "M17_KRUG9719_12_GE_C17.indd 542 17/11/2021 16:14"
_INDD_STAMP_RE = re.compile(r"\.indd\s+\d+.*\d{1,2}:\d{2}", re.IGNORECASE)

# Running heads known by name. Used by block_cut_spans() so a head inside a reference list does
# not end the cut, and removed as boilerplate: each is a fixed title, not a guess.
_RUNNING_HEADER_RE = re.compile(
    r"^(\w+\s+)?(Goldman\s+Sachs\s+FX\s+in\s+Focus|"
    r"Goldman\s+Sachs\s+Global\s+Investment\s+Research|"
    r"Macro\s+Vision\s*\|.*|"
    r"JOURNAL\s+OF\s+POLITICAL\s+ECONOMY|"
    r"VOL\.\s*\d+\s+NO\.\s*\d+|"          # AER's even-page head; it ended the References cut of Walsh (1995)
    r"EXPECTATIONS\s+AND\s+EXCHANGE\s+RATE\s+DYNAMICS\b.*)$",
    re.IGNORECASE,
)

_BOILERPLATE = (_INLINE_DISCLAIMER_RE, _DATE_PAGE_RE, _EXCLUSIVE_USE_RE, _WATERMARK_RE, _HASH_RE,
                _COPYRIGHT_RE, _JSTOR_DOWNLOAD_RE, _JSTOR_TNC_RE, _JOURNAL_ATTR_RE, _RUNNING_HEADER_RE)


def _is_boilerplate(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    return (any(r.match(s) for r in _BOILERPLATE) or bool(_INDD_STAMP_RE.search(s))
            or s.lower() in _REVERSED_WORDS)


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
    Short lines that recur across the document, tolerating a varying leading/trailing page
    number ("478 Canadian Journal of Economics..." and "... Policy 479" share a key). Used by
    block_cut_spans() only, so that a running head inside a reference list does not end the
    cut; since 2026-10-20 nothing is removed for being repeated.
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
        # ("FF4 17.930 [6.675 22.673]" → "FF . [. .]").
        if sum(ch.isalpha() for ch in norm) < 6:
            continue
        counts[norm] += 1
        originals.setdefault(norm, set()).add(stripped)

    found: set[str] = set()
    for norm, count in counts.items():
        if count >= min_occurrences:
            found.update(originals[norm])
    return found


def clean(text: str) -> str:
    """The raw text minus three things: the References/Bibliography blocks (block_cut_spans),
    everything from a bank's disclosure heading to EOF (_TAIL_TRIGGERS), and lines of known
    boilerplate (_is_boilerplate). Every other line is kept as extracted."""
    lines = text.splitlines()
    cut = {i for a, b, _ in block_cut_spans(lines) for i in range(a, b)}
    out: list[str] = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Per line, not per block: a bank report can put the heading on line 2 of a block with
        # no blank line before it ("Goldman Sachs FX in Focus\nDisclosure Appendix").
        if stripped and _TAIL_TRIGGERS.match(stripped):
            break
        if i in cut or _is_boilerplate(stripped):
            continue
        out.append(line)
    output = re.sub(r"\n{3,}", "\n\n", "\n".join(out))
    return output.strip()


def clean_file(source: str | Path, output_dir: str | Path | None = None) -> Path:
    """
    Clean a single raw .md file. Strips a '_raw' suffix from the output file name.
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
