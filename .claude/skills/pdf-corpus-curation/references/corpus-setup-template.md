# Corpus Setup Templates

Two things to create the first time a recurring PDF corpus is set up: a
`CURATION_SCOPE.md` (plain-language record of what this corpus's curation decisions
are, so they're never re-asked) and a `curate.py` starter skeleton (the reusable
scaffolding proven out on the Verde Asset corpus, minus anything corpus-specific).

## `CURATION_SCOPE.md` template

Write this into the corpus's own folder (next to `raw_pdf/`, `raw_md/`, `clean_md/`).
Keep it short and in plain language — it's read by a future session, not parsed by
code.

```markdown
# Curation scope — <corpus name>

## Purpose
<What the curated output feeds / is used for. E.g. "Feeds a macro/FX mental-model
synthesis — we want the manager's own reasoning and stated positions, not fund
administrivia.">

## Always keep
- <section/content type>
- <section/content type>

## Always drop
- <section/content type> — <why, if not obvious>
- <section/content type>

## Known PDF format eras / quirks
<Filled in incrementally as new formats are discovered — one bullet per era, with the
date/file range it covers and what's different about it. This is the changelog that
keeps curate.py's own comments from being the only record of WHY a piece of logic
exists.>

## Known unresolved limitations
<Files or format variants that couldn't be safely curated, what's specifically wrong,
and where the raw text still lives. Don't let this section imply "fixed later" if it
hasn't been revisited — update it when a limitation actually gets addressed, not
before.>
```

## `curate.py` starter skeleton

This is scaffolding, not a finished script — most of it will need reshaping around
whatever this corpus's actual documents look like. What's worth keeping as-is: the
normalization helper, the paragraph-reflow-by-gap logic, and the canonical-index
pattern for reconstructing any tabular/structured data. What needs replacing:
everything under `# --- CORPUS-SPECIFIC: fill in ---` markers.

```python
"""
Curate <corpus name>: raw_pdf/*.pdf -> raw_md/*.md (permanent, unedited) and
clean_md/*.md (curated per CURATION_SCOPE.md).

Positional signals available if the source has consistent formatting (verify
empirically against THIS corpus before relying on them, don't assume they transfer
from another corpus):
- Paragraph break within a page: vertical gap between consecutive lines above some
  threshold (tune GAP_THRESHOLD against a real sample -- don't guess a number).
- Chart/graphic noise: short tokens, high proportion of <=2-char tokens, or pure
  digit/punctuation lines with no label attached.
"""
import re
import unicodedata
from pathlib import Path
import pdfplumber
# import fitz  # PyMuPDF -- uncomment if this corpus has any broken-font PDFs;
#                see extraction-diagnostics.md's "(cid:NN)" section before using.


def normalize_key(s):
    """Accent-strip, lowercase, keep only [a-z0-9()+] -- also strips spaces, which is
    what makes this tolerant of both wide-inter-character-spacing and
    missing-inter-word-spacing corruption for free. Extend the allowed character set
    only if this corpus's real labels need punctuation this doesn't already keep."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9()+]", "", s.lower())


# --- CORPUS-SPECIFIC: fill in ---
# Canonical labels for any structured/tabular data this corpus's documents contain,
# and any known aliases (older terminology, different wording across format eras)
# mapped to the same canonical label. Verify against a handful of REAL files across
# the date range before assuming one era's wording -- don't guess from a single
# sample; see Core Rule 2 in SKILL.md.
KNOWN_LABELS = [
    # "Canonical Label Text",
]
LABEL_ALIASES = {
    # "Older or alternate wording": "Canonical Label Text",
}

HEADER_FOOTER_EXACT = {
    # exact lowercased strings of repeated page header/footer lines to strip,
    # e.g. a masthead line that repeats on every page
}
DISCLAIMER_ANCHORS = (
    # substrings that reliably open (or appear within) a legal/administrative
    # disclaimer block this corpus wants dropped. VERIFY where the anchor sits
    # relative to real wanted content before assuming "drop to end of page" is
    # correct -- confirmed in the Verde Asset corpus that this assumption broke on
    # a sub-era where real table data came AFTER the disclaimer on the same page.
)
# --- end corpus-specific ---


GAP_THRESHOLD = 10.0  # tune against this corpus's own real line-gap measurements


def build_label_matcher():
    """Exact match first across the WHOLE dictionary (including aliases), before any
    fuzzy match -- avoids a short canonical label falsely matching as a substring of
    a longer one regardless of dictionary ordering. Fuzzy fallback (substring in
    either direction) only kicks in for entries long enough that a coincidental
    match is unlikely; ambiguous fuzzy matches (more than one distinct candidate)
    return no match rather than guessing."""
    known = [normalize_key(l) for l in KNOWN_LABELS]
    alias_map = {normalize_key(a): c for a, c in LABEL_ALIASES.items()}

    def match_label(key):
        if key in alias_map:
            return alias_map[key]
        for canon, k in zip(KNOWN_LABELS, known):
            if key == k:
                return canon
        if len(key) >= 4:
            candidates = {canon for canon, k in zip(KNOWN_LABELS, known) if key in k or k in key}
            if len(candidates) == 1:
                return candidates.pop()
        return None

    return match_label


def is_header_footer(text):
    return text.strip().lower() in HEADER_FOOTER_EXACT


def reflow_page_paragraphs(lines):
    """Split one page's kept lines into paragraphs using in-page vertical gaps.
    `lines` is a list of {"text", "top", "bottom"} dicts (pdfplumber's
    extract_text_lines() shape). IMPORTANT: gaps are only meaningful WITHIN a page --
    pdfplumber resets y-coordinates per page, so never compare gaps across a page
    boundary (join cross-page paragraphs by a punctuation heuristic instead, e.g.
    "does the last kept line end in sentence-ending punctuation")."""
    paragraphs, current, prev_bottom = [], [], None
    for l in lines:
        gap = None if prev_bottom is None else (l["top"] - prev_bottom)
        if gap is not None and gap > GAP_THRESHOLD and current:
            paragraphs.append(" ".join(current))
            current = []
        current.append(l["text"].strip())
        prev_bottom = l["bottom"]
    if current:
        paragraphs.append(" ".join(current))
    return paragraphs


def reconstruct_structured_table(sub_lines, template):
    """Canonical-index-safe reconstruction for any tabular data whose labels or
    layout are too garbled for a simple one-line-per-row regex. `template` is the
    corpus's KNOWN_LABELS list (or a subset), in their real fixed order.

    THE ONE RULE THIS EXISTS TO ENFORCE: a reconstructed value must be written to
    its label's FIXED position in `template`, never to its position in the sequence
    of labels that happened to match successfully. Confirmed in the Verde Asset
    corpus that indexing by "position among successful matches" silently shifts
    every value after one unmatched/garbled label into the WRONG row -- a real,
    published-looking-but-wrong-number bug, not a hypothetical one.

    Returns (rows, missing) -- rows is a list of (label, value) tuples for whatever
    matched; missing is the list of template labels that were never found (reported,
    never guessed). Adapt the actual token-collection loop below to this corpus's
    real line/value layout -- this skeleton shows the INDEXING pattern, not a
    working parser for any particular table shape.
    """
    match_label = build_label_matcher()
    template_index = {normalize_key(l): i for i, l in enumerate(template)}
    row_at = {}

    # --- CORPUS-SPECIFIC: replace with this corpus's real token/value collection ---
    # for token in sub_lines:
    #     ...determine if `token` is a label or a value, matched via match_label()...
    #     idx = template_index.get(normalize_key(matched_label))
    #     if idx is not None and idx not in row_at:
    #         row_at[idx] = (matched_label, value)
    # --- end corpus-specific ---

    rows, missing = [], []
    for i, canon in enumerate(template):
        if i in row_at:
            rows.append(row_at[i])
        else:
            missing.append(canon)
    return rows, missing


def cross_validate(reconstructed_value, independent_value, tolerance):
    """The one universal safety gate: compare a reconstructed value against an
    independently-derived value elsewhere in the SAME document (e.g. a headline
    summary line vs. a detail table's own total). Anything beyond `tolerance` means
    the RECONSTRUCTION is wrong -- the caller should discard it and flag rather than
    publish either number. Tune `tolerance` to what's actually observed as benign
    rounding drift in this corpus's own real files, don't default it from another
    corpus."""
    return abs(float(reconstructed_value) - float(independent_value)) <= tolerance


def process_pdf(pdf_path: Path):
    """Main entry point: extract + curate one file. Return a dict with whatever this
    corpus's curated structure needs, plus a `report` dict of warnings/omissions so
    the caller can flag an incomplete result rather than silently claim success.
    Keep report entries specific enough that a future session (or a different Claude
    instance) can tell exactly what happened without re-reading this file's raw_md.
    """
    report = {"file": pdf_path.name, "warnings": []}
    # --- CORPUS-SPECIFIC: real extraction + curation logic goes here ---
    raise NotImplementedError("Fill in per this corpus's real document structure")


def render_md(pdf_name, data):
    """Render the curated markdown for one file. Always end with a Fonte/Source line
    pointing back to the raw_md file for that same document -- the curated file
    should never be the only record of where a number came from."""
    raise NotImplementedError("Fill in per this corpus's real desired output shape")
```
