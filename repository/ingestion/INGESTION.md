# Ingestion Pipeline

Turns a PDF into the two text layers of the knowledge base: `repository/<topic>/raw_md/` (verbatim
extraction, the audit trail) and `obsidian/<topic>/clean_md/` (the same text minus the reference list
and known boilerplate, in the vault the agents read). It is a **mechanical process of the
system**, not a task of any topic agent (`SISTEMA_AGENTES.md` II.I.iv, decided 2026-10-19).

## How to use it

1. Save the PDF straight into **`repository/<topic>/raw_pdf/`** (top level), any name. The user
   does it; Claude does too when it finds literature on the web. The PDF never moves again.
2. Run **`/ingest`** (every topic) or **`/ingest <topic>`**. The command starts the ingestion agent
   (`.claude/agents/ingestion.md`, in its own context). It sweeps for **pending** PDFs — a PDF at the
   top level of `raw_pdf/` with no `raw_md/<name>.md` — and, for each: fixes the name, tries the
   extraction modes, checks the text against rendered pages, records any non-default setting,
   writes the files and verifies them. It returns a table plus a list of what needs attention.
3. The literature to-do, **`repository/agent_mapping/data_tracker.xlsx`**, is updated by every
   write: columns J–P of each "Qual - <Area>" tab and a "Literature summary" tab (`tracker.py`).
4. Afterwards, **`/vault [topic]`** starts the vault agent (`.claude/agents/vault.md`): a synthesis
   note per clean_md, the concept pages and the links, checked by `vault.py` (see
   `obsidian/CLAUDE.md`).

`/ingest <topic> "<file>.pdf" --overwrite` redoes a file already ingested, e.g. after a settings
change.

```
repository/<topic>/raw_pdf/<name>.pdf
  └─ run.py --list → qc.py try → page check (qc.py render/page) → settings.yaml → run.py → qc.py check
       ├─ repository/<topic>/raw_md/<name>.md
       ├─ obsidian/<topic>/clean_md/<name>.md
       ├─ repository/ingestion/LOG.md
       └─ repository/agent_mapping/data_tracker.xlsx
```

**What the sweep skips:** subfolders of `raw_pdf/` (`monetary_policy/raw_pdf/central_bank/` is the
Copom ETL's), `repository/mental_model/` (manager letters: only when named, `/ingest mental_model/<manager>`; they keep raw_md and clean_md in their own folder — see `repository/mental_model/MENTAL_MODELS.md`), topics listed under
`topics_on_hold` in `settings.yaml` (none since `trader` was released on 2026-10-20), and files marked
`status: needs_attention` there (a scan, a failed page check), which are listed, not retried.

**Naming:** `description_in_snake_case (Author, Year).pdf` — up to three surnames, four or more as
`First et al.`. `run.py` refuses any other name.

## The scripts (`scripts/`)

| Script | What it does |
|---|---|
| `extract.py` | PDF → text. Modes: `plumber` (pdfplumber, `x_tolerance` 1.5), `plumber_flow` (word-grouped, for letter-spaced PDFs), `pymupdf` (math symbols as Unicode), `ocr` (Tesseract on pages rendered at 300 dpi, for scans and broken font encodings; a sideways page is turned by confidence; needs `winget install UB-Mannheim.TesseractOCR`, English only). `decode_shift` reverses a font-encoding Caesar shift, page by page, only where it makes the page read as English. No AI. |
| `clean_code.py` | Regex cleaner, no AI, that removes only whole blocks and known boilerplate text: the References/Bibliography block (up to the next section heading, ALL CAPS or a known mixed-case starter such as "Appendix", "Comments and Discussion", "Endnotes", "Data Sources", a "Table N"/"Figure N" caption or a table's "Coefficient" header), bank disclosure tails, and fixed boilerplate lines (JSTOR notices, watermarks, `.indd` stamps, known disclaimers and running heads). Page numbers, running heads, chart numbers, URLs and contacts stay (see below). Also used by the RPM ETL (`domain/db/brasil/bcb/_rpm_projecoes.py`). |
| `qc.py` | `try` (every mode side by side, into a temp folder), `page` (one page's text), `render` (pages to PNG with PyMuPDF — no poppler needed), `check` (metrics of an ingested file, including whether the files reproduce from the PDF). Writes nothing into the repository. |
| `settings.py` + `../settings.yaml` | `files:` per-file settings when the default fails, or `status: needs_attention` for a file the tools cannot ingest, each with the measured reason; `topics_on_hold:`. A re-run reproduces the same text. |
| `run.py` | `--list [topic]`: the sweep (pending / needs attention / on hold per topic). `run.py --reclean [topic]`: after a cleaner change, rewrites every clean_md from its raw_md (no PDF re-extracted, raw_md untouched). `run.py <topic> <files>`: the commit step — extract with the file's settings, clean, write both files, append to `../LOG.md`, update the tracker. Refuses a bad name, a duplicate, a marked file, an existing output without `--overwrite`, and blocking QC flags without `--accept-flags`. |
| `tracker.py` | Rewrites columns J–P (File, Ingestion, Ingested on, Extraction, QC flags, Synthesis, Ingestion note) of every "Qual - <Area>" tab of `agent_mapping/data_tracker.xlsx`, sets "Do we have it?" to Yes where the PDF exists, appends a marked row for each PDF the curated list lacks, and rebuilds the "Literature summary" tab. Matches a PDF to a row by year + author surnames, with the title words as tie-break; never guesses a tie (with no author in common, e.g. "IMF" on the file and the staff names on the row, a unique match on year + two title words). Columns A–I, the Notes tab and the Quant tabs are the user's; the workbook is the only home of the literature and data lists. In git since 2026-10-20 (the one `*.xlsx` exception in `.gitignore`). |
| `vault.py` | The vault agent's helper, read-only: `--list [topic]` (clean_md files with no synthesis note; skips `clean_md/central_bank/` and topics on hold), `check <topic> <name>` (template sections, Source file, every number in the clean_md, every wikilink resolves, concepts link back), `context <topic> <name>` (the file's tracker row and its cluster's notes). The vault's `qc.py check`. Tests: `tests/test_vault.py`. |
| `publish.py`, `run_code.py`, `clean.py`, `compare.py` | Older tools, not part of the flow. `clean.py` (AI cleaner) must not be used: see below. |

**QC flags** (`qc.py`), with the thresholds measured on the 46 monetary-policy PDFs:
blocking — `no_text_layer` (a scan), `garbled` (common-word share < 0.15), `letter_spaced`
(one-letter share > 0.35), `run_together` (18+-letter tokens > 0.2%); informational —
`math_glyphs` (> 50 `(cid:N)` symbols pdfplumber cannot map), `heavy_removal` (> 25% removed),
`long_references_cut` (a cut > 300 lines, or to EOF over a quarter of the document),
`reversed_text` (3+ words on a page read backwards, "elbaT" for "Table": a rotated table or chart
axis; measured 2026-10-20 at 3-50 words a page, against at most 2 of OCR noise).

Tests: `uv run python tests/test_ingestion.py`.

## What the 2026-10-19 measurement found (why the tools are like this)

A read-only run of the old pipeline over the 46 monetary-policy PDFs (its outputs were kept in
`staging/` until the real ingestion was done, then deleted on 2026-10-20; git history has them):

- **Words glued together in ~20 files** with pdfplumber's default `x_tolerance=3`
  ("AnaturalinterpretationofthisevidenceisthatFOMC…"). 1.5 removed it in every file and made none
  worse.
- **The References cut deleted content.** It ran until the next ALL-CAPS line; Campbell et al.
  (2012, Brookings) follow References with "Comments and Discussion" in mixed case, so the cut ran
  to EOF and deleted the discussants' comments — 41% of the document removed, with nothing
  reporting it. Now 6%.
- **Math as `(cid:N)` in 22 files**; PyMuPDF maps it to Unicode, at the cost of equations spread
  over lines.
- **Five files needed special handling:** two scans with no text layer (Bernanke–Gertler–Gilchrist
  1999, Walsh 1995; the first was the NBER WP 6455 scan, replaced the same day by a
  Handbook-chapter copy that has a text layer), two Caesar-shifted files (Clarida–Galí–Gertler 1999 and 2000), one
  letter-spaced (Orphanides 2001).
- **No two-column layout** in the sampled body pages: the root CLAUDE.md's warning about reading
  order did not bite on this corpus, but the page check exists to catch it where it does.

## What the cleaner removes, and why so little (2026-10-20)

clean_md is raw_md minus three things: the References/Bibliography blocks, a bank report's
disclosure back-matter (from its heading to EOF), and lines whose text is fixed boilerplate
(JSTOR notices, the "For the exclusive use of" watermark, `.indd` stamps, known disclaimer
sentences, known running heads). No rule judges a line by its shape any more.

The shape rules (page numbers, repeated lines, chart debris and axis numbers, any line with a URL,
e-mail or phone number) were 2.1% of the removal and every silent content loss found in three
audits (2026-10-19, and twice on 2026-10-20). The last one, an independent check on a 16-file
sample, found:

- **table cells dropped as axis ticks.** In a block of mostly short numbers every number of up
  to 4 characters went: `0.83` was dropped and `-0.24` kept, so the surviving cells sat under the
  wrong row (Minella & Souza-Sobrinho 2013, Table 2; 717 of Rey 2013's 1,218 appendix cells);
- **sentences with a URL dropped whole** (~20 content lines in ~13 files: Garcia & Valpassos 1998
  "Therefore, the domestic interest rate is computed through the", Svensson 2010, `Source:` lines);
- **a table's totals row taken for a phone number** (`(1+2+3) 28.5 29.9 34.4 34.5`).

The knowledge base is read for its reasoning (synthesis first, the source only in a doubt case),
so a page number or a running head left in the text costs nothing, and a lost sentence or a
table whose cells moved costs the one reading that goes back to the source. Reduced to the block
cuts, the reclean of the 123 ingested files restored 15,521 lines (3,471 table cells) and took
the removal from 8.2% to 6.4%; nothing that was in clean_md before left it.

What the References cut learned, and still applies (each with a test in `tests/test_ingestion.py`):

- it ends at the next heading, ALL CAPS or a known mixed-case starter: Campbell et al. (2012)
  follow References with "Comments and Discussion", and the cut once ran to EOF and deleted the
  discussants' comments (41% of the document);
- a bare "Comment" heading ends it (Krugman 2000, IMF: Garber's comment);
- a footnote printed under the reference list survives and the cut resumes after it (Mundell
  1961 fn 9, BIS 2026 fn 10-11, Rey 2013 fn 18, Minella & Souza-Sobrinho 2013 fn 15);
- a running head, an acronym line or a wrapped citation tail ("FEDS 2001-53.") does not end it.

## Why there is no AI in the text path (2026-08 audit)

An AI cleaning pass (`clean.py`) was audited on 14 files against their PDFs and **every file was
corrupted**: long documents truncated mid-sentence (the per-chunk output budget), worked examples
deleted as "boilerplate", and prose paraphrased ("I argue" → "the paper argues", paragraphs turned
into bullets). The old outputs are kept in `raw_md/_legacy_ai_rewrite/` folders. Since then every
character of raw_md and clean_md comes from deterministic code; the ingestion agent's judgment goes
into choosing the extraction and checking it, never into writing the text.
