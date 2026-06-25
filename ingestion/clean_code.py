"""
ingestion/clean_code.py — Code-only cleaning (no AI).

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
from pathlib import Path


# ── Tail-cut triggers ────────────────────────────────────────────────────────
# First standalone line matching any of these → everything from that point to
# EOF is discarded. Covers Goldman, Itaú, and JSTOR academic papers.
_TAIL_TRIGGERS = re.compile(
    r"""^(
        Disclosure\s+Appendix |
        Reg\s+AC |
        Disclosures? |
        Regulatory\s+Disclosures? |
        Global\s+product[;,]?\s*(distributing\s+entities)? |
        General\s+Disclosures? |
        Relevant\s+Information |
        Bibliography |
        References?
    )$""",
    re.IGNORECASE | re.VERBOSE,
)

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
# Copyright symbols / lines
_COPYRIGHT_RE = re.compile(r"^[\(©]\s*\d{4}\b")
# JSTOR download notices (appear on every page, embedded in content blocks)
_JSTOR_DOWNLOAD_RE = re.compile(r"^This\s+content\s+downloaded\s+from\s+\d+\.\d+", re.IGNORECASE)
_JSTOR_TNC_RE = re.compile(r"^All\s+use\s+subject\s+to\b", re.IGNORECASE)
# Journal / publisher attribution lines
_JOURNAL_ATTR_RE = re.compile(r"^\[Journal\s+of\s+Political\s+Economy", re.IGNORECASE)

# Running headers — also matches JSTOR-style "Ii62 JOURNAL OF POLITICAL ECONOMY" prefixes
_RUNNING_HEADER_RE = re.compile(
    r"^(\w+\s+)?(Goldman\s+Sachs\s+FX\s+in\s+Focus|"
    r"Goldman\s+Sachs\s+Global\s+Investment\s+Research|"
    r"Macro\s+Vision\s*\|.*|"
    r"JOURNAL\s+OF\s+POLITICAL\s+ECONOMY|"
    r"EXPECTATIONS\s+AND\s+EXCHANGE\s+RATE\s+DYNAMICS\b.*)$",
    re.IGNORECASE,
)

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
    tokens = stripped.split()
    if len(tokens) < 5:
        return False
    short = sum(1 for t in tokens if len(t) <= 2)
    return short / len(tokens) >= 0.70


def _line_should_remove(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if _PAGE_NUM_RE.match(stripped):
        return True
    if _DATE_PAGE_RE.match(stripped):
        return True
    if _WATERMARK_RE.match(stripped):
        return True
    if _HASH_RE.match(stripped):
        return True
    if _SOURCE_RE.match(stripped):
        return True
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
    if _is_chart_garbage(stripped):
        return True
    return False


def _block_is_garbage(lines: list[str]) -> bool:
    """
    Detect chart-artifact blocks: short blocks where most lines are numeric/
    single-char fragments from garbled chart axis labels.
    """
    if len(lines) < 4:
        return False
    total = len(lines)
    garbled = sum(
        1 for ln in lines
        if _is_chart_garbage(ln) or (len(ln.strip()) <= 4 and ln.strip().replace(".", "").replace(",", "").replace("%", "").replace("-", "").strip().replace(" ", "").isdigit())
    )
    return garbled / total >= 0.6


def clean(text: str) -> str:
    """Apply all code-based rules. Returns cleaned text."""
    # Pass 1: line-by-line — tail trigger + individual line removal.
    # Tail trigger is checked per-line (not per-block first-line) because bank
    # reports often put the trigger heading on line 2 of a block with no blank
    # line separator (e.g. "Goldman Sachs FX in Focus\nDisclosure Appendix").
    pass1: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and _TAIL_TRIGGERS.match(stripped):
            break  # discard everything from here to EOF
        if not stripped:
            pass1.append("")
        elif not _line_should_remove(line):
            pass1.append(line)

    # Pass 2: garbage-cluster removal over the filtered lines.
    # Collect consecutive non-blank lines into blocks; drop blocks where ≥60%
    # of lines are chart-artifact garbage (space-fragmented single chars).
    pass2: list[str] = []
    block_buf: list[str] = []

    def _flush(buf: list[str]) -> None:
        if _block_is_garbage(buf):
            pass2.append("")  # replace whole cluster with a single blank
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
