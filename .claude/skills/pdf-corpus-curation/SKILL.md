---
name: pdf-corpus-curation
description: >
  Extracts text from PDF(s) into a permanent raw markdown audit trail, then curates
  that raw text down to whatever a stated purpose actually needs (e.g. asset-manager
  monthly letters where only the manager commentary and performance table matter, not
  the legal disclaimer or fund-characteristics boilerplate). Use whenever the user wants
  to turn PDF(s) into markdown for downstream use, mentions raw_md/clean_md, asks to
  "extract and clean" a PDF or PDF collection, or wants a repeatable pipeline for a
  recurring document series (monthly letters, periodic filings, etc.). Not for a single
  ad-hoc read of one PDF's content in conversation — use the Read tool directly for that.
---

# PDF Corpus Curation

Turns PDF(s) into two layers: a **raw** extraction (permanent, unedited, the audit
trail) and a **curated** extraction (only what the stated purpose needs, everything
else dropped). Built from experience curating ~150 asset-manager letters across four
distinct PDF template eras, where the two costliest mistakes were (a) treating the
whole batch as one problem instead of one document at a time, and (b) guessing a value
that looked plausible instead of admitting extraction couldn't recover it safely.

## Core rules (apply throughout, not just at setup)

1. **Never lose or corrupt information.** The raw extraction is never hand-edited and
   never deleted — it's the fallback of record. The curated output may DROP sections
   (that's the point), but it must never show a value that isn't genuinely what the
   source says.
2. **One document is one document.** Evaluate, extract, and validate each PDF on its
   own. A file that breaks the usual extraction tool does not mean earlier or later
   files are suspect — and a file that extracts cleanly does not mean the next one
   will. Never assume corpus-wide success or failure from a single file's outcome.
3. **Never guess an ambiguous value.** If a number, label, or section can't be
   recovered with confidence, omit it from the curated output and add a visible note
   pointing back to the raw file for that specific item. A wrong-looking-right number
   is worse than a visible gap.
4. **Don't re-validate what's already done.** Once a file has a raw + curated output,
   leave it alone. Only reprocess a specific already-done file if there's concrete
   evidence — a visibly wrong value, an explicit bug report, an explicit user request —
   that ITS OWN output is actually wrong. A code change made while working on a
   different file/batch is not evidence the old batch is broken; don't sweep back over
   it "just in case."

## Step 0 — Scope: one-off or recurring?

Before anything else, determine (ask if not obvious from the request) whether this is:

- **A one-off.** A single PDF or small fixed batch, no expectation more will show up
  later. → Skip straight to Step 3 (per-file extract) then Step 4 (curate) for just
  those files. No folder convention to set up, no persistent script, no scope file —
  do the extraction and curation directly and move on.
- **A recurring corpus.** More documents will keep arriving over time (a fund's monthly
  letters, a recurring filing, an ongoing series). → Continue to Step 1. This is worth
  the extra setup because the SAME extraction/curation logic will run again on the next
  document, and future sessions need to pick it up without re-deriving everything from
  scratch.

If genuinely unclear which one this is, ask — the cost of guessing wrong is either
over-building infrastructure for a single file, or under-building it and redoing setup
work next month.

## Step 1 — Corpus setup (recurring only, first time on this collection)

1. **Confirm the folder layout.** If the PDFs already live somewhere with an existing
   convention (e.g. this project's `raw_pdf/` + `raw_md/` + `clean_md/` sibling-folder
   pattern used under `repository/mental_model/<manager>/`), follow it. Otherwise
   propose that same three-folder pattern next to wherever the source PDFs are, and
   confirm with the user before creating it.
2. **Ask about purpose and scope**, via AskUserQuestion, before writing any curation
   logic:
   - What will the curated output be used for? (This determines what "relevant" means —
     a mental-model/thesis-building use case cares about different things than a
     data-extraction-into-a-database use case.)
   - What should always be KEPT?
   - What should always be DROPPED? (Disclaimers and fund/company administrative
     boilerplate are dropped in the overwhelming majority of cases — say so as the
     likely default when asking, don't make the user spell out something this obvious
     from scratch.)
3. **Write `CURATION_SCOPE.md`** in the corpus's own folder recording the purpose, the
   keep list, and the drop list in plain language. This file is read (not re-asked)
   on every future run. See `references/corpus-setup-template.md` for the shape.
4. **Create a persistent `curate.py`** in the corpus's own folder (NOT in a scratch/temp
   directory — it must survive across sessions). Seed it from
   `references/corpus-setup-template.md`'s starter skeleton, which provides the
   reusable scaffolding (header/footer stripping, paragraph reflow by vertical gap,
   the canonical-index-safe table-reconstruction pattern, the cross-validation safety
   gate) proven out on the Verde Asset corpus. This script accumulates
   corpus-specific knowledge over time — new format quirks get ADDED to it
   incrementally as they're discovered, never rewritten wholesale.

## Step 2 — Figure out what's actually new (recurring only)

Diff `raw_pdf/` against `raw_md/` and `clean_md/`. Anything with both outputs already
present is done — per Core Rule 4, leave it alone unless there's concrete evidence it's
wrong. Only PDFs missing an output are this run's actual work.

## Step 3 — Per-file raw extraction

For each PDF to process:

1. **Pick a tool based on this file's own structure** — not a corpus-wide assumption.
   Default preference order: a plain-text extractor (e.g. `utils/extract_pdf.py` /
   pdfplumber in this project) for born-digital single-column text; direct reading
   (e.g. the Read tool, or a vision-capable pass) for complex multi-column layouts
   where a plain extractor's reading order can't be trusted; OCR only as a last resort
   for scanned pages with no text layer. This project's root `CLAUDE.md` has an
   existing PDF-routing table for the bibliography pipeline — use it as a starting
   point, but this skill's own diagnostics are the more complete reference for what to
   do when the primary tool fails. See `references/extraction-diagnostics.md`.
2. **Validate this file's own output** against the known failure signatures in
   `references/extraction-diagnostics.md` (broken-font glyph codes, two-column
   interleaving, character-repetition rendering glitches, wide inter-character
   spacing, chart/graphic noise). Don't just assume the tool worked because it didn't
   error.
3. **If a known signature is found, apply its documented fallback for THIS FILE ONLY**
   (e.g. swap to PyMuPDF for a broken-font signature). Never propagate a fix backward
   onto already-good files just because they're in the same batch.
4. **If no known fix resolves it**, still write whatever was extracted, but visibly
   flag that file's raw output as unreliable (a short header note is enough) so Step 4
   treats it cautiously — omit-and-flag rather than curate confidently.
5. **Write the raw extraction as-is, unedited, permanent.** This file is the audit
   trail; nothing downstream ever writes back into it.

## Step 4 — Curate

Apply the corpus's keep/drop scope (from `CURATION_SCOPE.md`, or from a one-off's
stated purpose) to turn the raw text into the curated output:

- Drop what the scope says to drop; keep what it says to keep. When something doesn't
  clearly fall into either bucket, prefer keeping it (dropping is the irreversible
  direction — the raw file is always there as a fallback, but the curated file is what
  gets used and read).
- **Cross-validate reconstructed or ambiguous structured data** against an independent
  value elsewhere in the same document when one exists (e.g. a headline summary line
  vs. a detail table's own total row). A small tolerance for genuine rounding drift
  already present in the source is fine; anything larger means the EXTRACTION is
  wrong, not that the source disagrees with itself — discard that piece and flag it
  rather than publish it.
- **Never guess.** A value or section that can't be safely determined gets omitted from
  the curated output, with a visible note pointing back to the raw file.
- **Update the corpus's `curate.py` and `CURATION_SCOPE.md` incrementally** whenever
  this file's PDF turns out to need a format variant or new curation rule not seen
  before — add a case, don't rewrite what already works.

## Step 5 — Report

Summarize the run: how many files processed, how many needed a fallback or came out
flagged/incomplete and why, where the outputs live. Don't claim a file is "done" if its
curated output has an omission note in it — say so plainly.

## Reference material

- `references/extraction-diagnostics.md` — known PDF extraction failure signatures,
  what causes each, and the fix that's actually been verified to work for it.
- `references/corpus-setup-template.md` — the `CURATION_SCOPE.md` template and the
  `curate.py` starter skeleton (helper functions for header/footer stripping,
  gap-based paragraph reflow, canonical-index-safe table reconstruction, and the
  cross-validation safety gate).
