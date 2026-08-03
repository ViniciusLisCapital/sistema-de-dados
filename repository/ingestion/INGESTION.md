# Ingestion Pipeline

Converts PDF research documents into clean, analysis-ready `.md` files for `repository/<topic>/raw_md/` and `repository/<topic>/clean_md/`. Lives inside `repository/` (moved here 2026-08, was a top-level `ingestion/` folder before) so the whole raw-PDF → raw_md → clean_md flow is self-contained in one place.

---

## How it works — one command

Drop a PDF into `repository/ingestion/land_space/<topic>/` (topic = one of `repository/`'s own topic names: `exchange_rate`, `monetary_policy`, `fiscal_policy`, `inflation`, ...), then:

```powershell
uv run python repository/ingestion/scripts/run.py
```

That's it. For that PDF, `run.py`:

```
repository/ingestion/land_space/<topic>/some_paper.pdf
 └─ [extract]      raw text extraction (pdfplumber, no AI)     → repository/<topic>/raw_md/some_paper.md
 └─ [clean_code]   deterministic regex cleaner (no AI)         → repository/<topic>/clean_md/some_paper.md
 └─ [move]         the PDF itself                              → repository/<topic>/raw_pdf/some_paper.pdf
```

The drop-zone folder ends up empty — everything lands organized under `repository/<topic>/`.

| Step | Script | Tool | What it does |
|---|---|---|---|
| Extract | `extract.py` | pdfplumber | Reads PDF pages, writes raw text. No AI, no rewriting risk. |
| Clean | `clean_code.py` | regex only | Removes boilerplate deterministically: page numbers, running headers/footers (both hand-tuned per-source patterns AND a generic "line repeats N+ times across the document, tolerating a varying page number" detector), emails/phones/URLs, chart-axis-label garbage, known disclaimer sentences, and References/Bibliography (bounded to that section only — not a to-EOF cut, so content that follows References in the source, like practice-problem solutions, survives). |
| Move | `run.py` | — | Moves the source PDF into `raw_pdf/` once extraction + cleaning succeed. |

**Boilerplate removed includes:** disclaimers, legal notices, regulatory disclosures, analyst contact details (phone numbers, emails), copyright notices, running headers/footers, table of contents, References/Bibliography sections, and blank filler pages. Footnotes and citations that aren't part of a References/Bibliography list are treated as content and kept.

**Safety behavior:** if `repository/<topic>/raw_md/<name>.md` already exists, `run.py` preserves it (moves it to `repository/<topic>/raw_md/_legacy_ai_rewrite/<name>.md`) rather than overwriting — see the audit finding below for why this matters. If `repository/<topic>/raw_pdf/<name>.pdf` already exists, the source PDF is left in the drop zone untouched rather than silently duplicated or overwritten.

### Usage

```powershell
# Process every topic folder in land_space/ that has PDFs waiting
uv run python repository/ingestion/scripts/run.py

# Process just one topic
uv run python repository/ingestion/scripts/run.py exchange_rate

# Reprocess even if clean_md already exists (e.g. after tuning a clean_code.py pattern)
# raw_md/raw_pdf are always legacy-preserved / never silently clobbered, regardless of this flag
uv run python repository/ingestion/scripts/run.py --overwrite
```

### If `clean_code.py` leaves obvious garbage in a new document

Inspect `repository/<topic>/raw_md/<name>.md`, find the pattern (a repeated header, a disclaimer sentence, a new bank's contact-info format), and add a targeted regex to `clean_code.py` next to the existing ones — same pattern as the Goldman/Itaú-specific rules already there. The generic running-header detector (`_detect_running_headers`) catches most page-number-varying headers automatically; hand-tuned patterns are for anything it misses (known disclaimer sentences, chart-garbage shapes, watermarks). Then re-run with `--overwrite` to regenerate `clean_md`.

### Adding a new topic

Just create the folder — no registration needed:

```powershell
mkdir repository/ingestion/land_space/labor_market
```

Drop PDFs into it and run `run.py` — `repository/labor_market/{raw_pdf,raw_md,clean_md}/` are created automatically.

---

## ⚠️ 2026-08 finding: the AI cleaning pass (`clean.py`) is unreliable — do not use it

A full audit (14 files across `exchange_rate`/`monetary_policy`/`fiscal_policy`/`inflation`, each verified against its source PDF) found that **every single file `clean.py` had produced was corrupted** in some way:
- **Truncation**: long documents got cut off mid-sentence, silently dropping entire back sections (Results, Conclusions, References, worked examples) — traced to the per-chunk `max_tokens=8096` output budget in `_call()` not being enough for a chunk whose "cleaned" output is still nearly as long as its input.
- **Overreach past "remove boilerplate"**: `_CLEAN_PROMPT` explicitly listed "Practice questions... and answers/solutions" as boilerplate to remove — that's substantive content, not garbage, and it silently deleted whole worked-example sections from CFA readings.
- **Paraphrasing**: `_STRUCTURE_PROMPT` never says "preserve wording verbatim" — Haiku took the liberty of rewriting voice (first-person "I argue" → third-person "the paper argues") and restructuring prose into bullet lists in several documents, which is not "cleaning," it's editing.

`clean_code.py` (deterministic, regex-based, zero AI calls) replaced it as the default — zero paraphrasing/truncation risk by construction. Its only failure mode is under/over-removal via an incomplete or over-broad pattern, which is auditable and fixable, unlike an LLM silently rewriting content. `clean.py` is kept in the repo for reference/possible future repair but is not called by `run.py`.

---

## Folder layout

```
repository/
  ingestion/
    land_space/                 ← DROP PDFs HERE — same topic names repository/ uses
      exchange_rate/
      monetary_policy/
      fiscal_policy/
      inflation/
      ...
    scripts/                     ← all pipeline code lives here
      extract.py                 ← Step 1: raw extraction (pdfplumber, no AI)
      clean_code.py               ← Step 2, recommended: deterministic regex cleaner (no AI)
      clean.py                    ← Step 2, NOT recommended: AI cleaner — see the warning above
      run.py                       ← THE entry point: drop-zone PDF -> raw_pdf + raw_md + clean_md, one command
      publish.py                   ← lower-level tool: publish an existing *_raw.md file/folder into
                                      raw_md/+clean_md/ without re-extracting — takes an explicit path,
                                      no default folder; most ingestion should just use run.py instead
      run_code.py                   ← lower-level tool: runs clean_code.py over an explicit <source>
                                      folder of *_raw.md, writes to an explicit <output> folder,
                                      inspection only — no default folders (see history below)
      compare.py                     ← optional, paid ($0.01/doc) AI spot-check: does clean_md preserve raw_md's substance?
    INGESTION.md                  ← this file

repository/<topic>/
  raw_pdf/                     ← source PDFs land here once ingested
  raw_md/                      ← FINAL raw output (verbatim, extraction artifacts only)
    _legacy_ai_rewrite/         ← old clean.py-produced files preserved (not deleted) when real raw_md replaced them
  clean_md/                    ← FINAL clean output (raw minus true garbage, no rewriting)
```

**2026-08 history**: this used to be a top-level `ingestion/` folder with an `inbox/<topic>/` drop zone (separate from `repository/`) and a multi-step manual workflow (`extract.py` → `ingestion/work/` → `publish.py` → `repository/`). It was consolidated into `repository/ingestion/` and flattened to a single `run.py` command, so the whole pipeline — drop zone, scripts, and final destination — lives in one place. `inbox/<topic>/` was renamed directly to `<topic>/` (dropping the extra nesting level), and its topic names were also fixed to match `repository/`'s exactly (previously used its own names like `exchange_rate_policy`, which caused a real misfiling — `em_food_inflation.pdf`, an inflation paper, had been sitting under `inbox/monetary_policy/`).

**Later 2026-08 — split into `land_space/` + `scripts/`**: the drop zone and the pipeline code originally sat as siblings directly under `repository/ingestion/` (`repository/ingestion/exchange_rate/` next to `repository/ingestion/run.py`). Per explicit request, separated the two concerns: every topic drop-zone folder now lives under `repository/ingestion/land_space/<topic>/`, and every script (`extract.py`, `clean_code.py`, `clean.py`, `run.py`, `publish.py`, `run_code.py`, `compare.py`, `__init__.py`) moved into `repository/ingestion/scripts/`. All path constants in the moved scripts were updated accordingly and the new layout was verified with a fully isolated scratch-tree smoke test (fresh ingest + legacy-preserve/duplicate-PDF re-ingest, both passing) before being applied to the real tree.

**Same day — `work/`, `test/`, `compare_report.md`, `ingestion_context.md` retired.** These four were all pre-`repository/`-move leftovers, checked and found redundant/stale rather than genuinely historical: `work/`'s 19 `*_raw.md` files were byte-identical to what's already in each topic's `raw_md/` (they were the source `publish.py` copied from — no unique content); `test/`'s 5 sample outputs actively **disagreed** with current `clean_md/` for 3 of them, since `clean_code.py` was tightened (the References block-cut fix, the generic running-header detector) after `test/` was generated — stale enough to mislead rather than inform; `compare_report.md` and `ingestion_context.md` were both dated 2026-06-26, predating even the `repository/`/`agent_bibliography/` rename, and referenced folders (`ingestion/work/exchange_rate_policy/`, `agent_bibliography/...`) that no longer exist. The one substantive open item from `ingestion_context.md` — the Fleming 1962 / Frenkel 1976 garbled-text safety-classifier block — was carried forward into its own section below before deletion, since it's still a real (if currently moot) limitation.

---

## Known limitation: garbled scanned-PDF text can block the AI cleaner

Two old JSTOR scans — `domestic_policy_exchange_rate_regimes (J. Marcus Fleming, 1962)` and `monetary_approach_exchange_rates (Frenkel, 1976)` — have such heavily garbled `pdfplumber` text (fused words, shifted spaces) that Claude's safety classifier blocks `clean.py`'s output outright, even after mitigation attempts (camelCase-fusion preprocessing, a contextual preamble, an academic-framing system prompt). This is moot for the current default path (`clean_code.py` is regex-only, makes no API call, so nothing to block) — it would only resurface if `clean.py` is ever repaired and used again on these two sources. If so, the remaining unexplored option is a "shifted space" heuristic keyed on common short English words (prepositions/articles: `in`, `on`, `of`, `to`, `from`, `at`, `by`, `an`, `the`) to catch the fusion pattern regex alone doesn't fix (e.g. `declinei n taxation`, `resultingf roma`) — or just read the source PDF directly in-session and hand-write the `.md`, per the root `CLAUDE.md`'s PDF-extraction routing table.

---

## Skip logic

`run.py` is safe to re-run: `clean_md` is skipped if it already exists (use `--overwrite` to force), `raw_md` is always preserved via the legacy-move behavior above, and a `raw_pdf` that already exists at the destination is left untouched in the drop zone (with a message) rather than silently duplicated.

---

## Cost

`extract.py` and `clean_code.py` make **zero API calls** — `run.py`'s whole path is free. `compare.py` (optional QC spot-check, not run automatically) calls `claude-haiku-4-5` once per pair, ~$0.01/doc.

---

## Requirements

- `ANTHROPIC_API_KEY` must be set in `.env` at the project root — only needed for `compare.py` (optional QC) or if `clean.py` is ever repaired and used again. `run.py` itself needs no API key.
- Run `uv pip install -e .` once after cloning or adding new packages.
