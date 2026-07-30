# PDF Extraction Diagnostics

Known failure signatures for text-layer PDF extraction (pdfplumber, PyMuPDF, or
equivalent), what actually causes each one, and the fix verified to work — drawn from
curating ~150 files across four PDF template eras (2010-2026) of the same document
series. Check a file's own output against these BEFORE trusting it; a tool returning
without an error is not the same as a tool returning correct text.

## Tool selection, first pass

| PDF shape | Tool | Why |
|---|---|---|
| Born-digital, single column | Plain-text extractor (pdfplumber / `utils/extract_pdf.py` in this project) | Cheapest, reliable reading order for single-column text |
| Multi-column academic/report layout | Read directly (Read tool / vision pass) | A plain extractor's default reading order interleaves columns line-by-line — see "Two-column interleaving" below |
| Scanned, no text layer | External OCR | Neither pdfplumber nor PyMuPDF can recover text that was never encoded as text |
| New, complex PDF in an automated (non-interactive) pipeline | An LLM API call (e.g. Claude Haiku) reading the PDF directly | When neither a plain extractor nor an interactive Read pass is available |

This project's root `CLAUDE.md` has this same table in more detail (with cost notes)
for the bibliography-ingestion use case — treat it as the default starting point, and
the sections below as what to do when the default tool's output turns out wrong.

## Failure signatures and fixes

### `(cid:NN)` glyph-index tokens
**Signature:** extracted text is literal strings like `(cid:65)(cid:32)(cid:112)...`
instead of real characters.
**Cause:** the PDF's embedded font has no usable ToUnicode CMap that the extractor can
decode — pdfplumber falls back to raw glyph indices.
**Fix:** re-extract that file with PyMuPDF (`fitz`) instead — confirmed empirically to
decode the SAME PDF correctly via its own font-handling, even when pdfplumber can't.
```python
import fitz
doc = fitz.open(pdf_path)
text = "\n\n".join(page.get_text() for page in doc)
```
For line-position-dependent downstream logic (gap-based paragraph reflow, etc.), use
`page.get_text("dict")` and pull `line["bbox"]` for top/bottom instead of plain
`get_text()`, then re-sort lines by top position (block order isn't guaranteed to
already be reading-order).
**Scope of the fix:** apply ONLY to files that actually show this signature. Detect
per-file (`"(cid:" in extracted_text`), never assume the whole corpus needs the
fallback tool just because one file did.
**Known residual limitation:** if a SINGLE PDF has some pages/regions decoded
correctly by the fallback tool and others still garbled (e.g. a broken SECOND font used
only in a footer or a differently-styled box), the fallback isn't a universal fix
within that one file either — validate the specific region you need, not just
"no `(cid:` found anywhere."

### Two-column interleaving
**Signature:** two unrelated sentences from adjacent columns land on the same output
line, or reading order jumps between columns mid-paragraph.
**Cause:** a plain-text extractor's default reading order is usually top-to-bottom
across the WHOLE page width, which merges side-by-side columns line-by-line instead of
finishing one column before starting the next.
**Fix:** re-extract with a layout-aware mode (e.g. pdfplumber's `layout=True`), or —
often more reliable and no more expensive for a one-off — read the PDF directly instead
of through a text-extraction tool. Not yet solved by a drop-in code fix in this
project's corpus (Kapitalo's post-2023 letters have this exact issue, still open).

### Character-repetition rendering glitch (e.g. "RRReeesssuuulll...")
**Signature:** every character in a region of text appears repeated a fixed number of
times in a row (commonly 3x), including digits and punctuation ("000...333555" for
"0.35").
**Cause:** a bold/emphasized text style rendered via multiple overlapping paint passes
(pseudo-bold via overprint) instead of a true bold font weight — the extractor sees
each stroke as a separate glyph occurrence.
**Fix (use cautiously, scope-limited):** group each maximal run of an identical
non-space character; if the run length is evenly divisible by the observed repeat
count (e.g. 3), collapse it to `length / repeat_count` copies of that character.
**Why this is risky enough to scope tightly:** a genuine, uncorrupted run of the same
digit (e.g. "1000" has three consecutive zeros) is indistinguishable from this
artifact by pattern alone. Only apply the collapse within a region already confirmed
to have the corruption (e.g. one specific table), never as a blanket pass over an
entire document, and verify the result against an independent value (see "Safety
gate" below) before trusting it.
**If the fix can't be safely scoped:** treat as unrecoverable for that region — omit
and flag per Core Rule 3, don't guess.

### Wide inter-character spacing ("R e s u l t a d o")
**Signature:** every glyph in a region is its own token, with spaces where there
shouldn't be any.
**Cause:** a specific font/kerning combination in some PDF template eras.
**Fix:** strip all internal spaces before matching against a known-label dictionary
(`re.sub(r"[^a-z0-9()+]", "", s.lower())`-style normalization handles this for free,
since it discards spaces along with everything else it strips).

### Missing inter-word spacing ("Dólarfuturo", "Cupomcambial")
**Signature:** words that should have a space between them are glued together.
**Cause:** different font-metrics quirk than the wide-spacing case above, seen in a
different PDF template era of the same document series — the extractor undercounts a
narrow word-gap as not being a real space.
**Fix:** same space-stripping normalization already used for the wide-spacing case
correctly matches this too (space-agnostic dictionary lookup handles both directions).
Genuinely unrecognized glued labels (not in the known dictionary, not a known alias)
are usually finer-grained sub-line-items an older template had that a newer one rolled
up into a summary row — keep them displayed as-is rather than forcing a match; they're
extra detail, not corruption.

### Chart/graphic noise
**Signature:** a scattering of short, loose numbers/characters with no clear structure
near where a pie/line/bar chart is in the original PDF.
**Cause:** chart tick labels, legend text, and axis values get extracted as text but
carry no structural relationship to each other once flattened out of the graphic.
**Fix:** not worth reconstructing — detect (short tokens, high proportion of ≤2-char
tokens, pure digit/punctuation lines) and drop, with a one-line note in the curated
output that a chart was omitted as visually-redundant with an adjacent table, if one
exists.

### Reading order scrambled across content blocks (labels and values in separate blocks)
**Signature:** a whole run of numeric values appears before ANY of their labels, or
vice versa — sequential "label then its own value(s)" pairing produces obviously wrong
matches.
**Cause:** some PDF generators draw a table's label column and value column as two
separate content-stream text objects; a simple top-to-bottom sort across the whole
page can end up putting one whole column before the other instead of interleaving them
row-by-row.
**Fix:** detect via a sanity guard (e.g. more than a handful of value tokens appear
before the first recognized label) and REFUSE to attempt positional pairing when
detected — this is the one signature where the safe answer is "this file's structured
data isn't recoverable this way," not a workaround. Omit and flag per Core Rule 3.

## The one universal safety mechanism: cross-validate, don't guess

Whenever a value is reconstructed from a garbled or ambiguous extraction (rather than
read cleanly off one unambiguous line), check it against an INDEPENDENT value elsewhere
in the same document if one exists — e.g. a headline summary line stating the same
figure in prose, versus a detail table's own total row. Use a small tolerance for
genuine rounding drift that can legitimately exist between two tables in the SAME
source PDF (confirmed real in this corpus, not an extraction artifact). Anything beyond
that tolerance means the reconstruction itself is wrong — discard that specific value
and flag it, never publish the "more plausible-looking" of two disagreeing numbers.

The single costliest correctness bug found in this corpus was NOT a case with no safety
net — it was a positional-pairing bug: when one label in a sequence failed to match,
every value read AFTER it silently shifted into the wrong row, because values were
paired by "position in the list of successfully-matched labels" rather than by a fixed
canonical index. The fix: always assign a reconstructed value to its label's FIXED
position in a known template, never to its position in the sequence of matches that
happened to succeed. A missing label should leave a visible gap, not shift everything
after it.

## A note on what ISN'T corruption

Windows terminal / pipe output showing `�` in place of accented characters is a
display-codepage artifact, not real data loss — verify by writing the extracted text
directly to a UTF-8 file and reading it back (e.g. via the Read tool) before concluding
anything is actually corrupted. Don't let a garbled terminal echo cause a false-positive
diagnosis.
