# repository/ — Context for Claude

**Naming note:** this folder was formerly named `agent_bibliography/` — treat that name as a synonym if it turns up elsewhere (git history, older docs).

## Purpose

The raw material behind the knowledge base, plus the acquisition planning. **No agent reads this
tree** (decided 2026-09-30): everything an analyst agent consumes lives in
[`obsidian/`](../obsidian/CLAUDE.md), including `clean_md/` and the conceptual maps, which used to
live here. The ingestion pipeline reads from here and
writes the clean text into the vault.

Each area follows the reusable process in [`BIBLIOGRAPHY_METHODOLOGY.md`](BIBLIOGRAPHY_METHODOLOGY.md).
The pipeline is documented in [`ingestion/INGESTION.md`](ingestion/INGESTION.md), including why its
AI-based cleaner was found unreliable and replaced with a deterministic one (`clean_code.py`).

## Structure

```
repository/
  BIBLIOGRAPHY_METHODOLOGY.md   — reusable process, not the output of any single topic
  <área>/raw_pdf/, raw_md/      — acquired PDFs and their untouched pdfplumber extraction
                                  (clean_md/ for these lives in obsidian/<área>/clean_md/)
    exchange_rate/              — 28 PDF, 16 raw_md; 12 PDFs still await extraction
    monetary_policy/            — raw_pdf/theorical_literature/ (36 papers, 1 extracted),
                                  central_bank_comunication/ (234 comunicados + 261 atas as
                                  raw_md, 82 ata PDFs), relatorio_politica_monetaria/ (110 RPM PDFs;
                                  raw_md holds only the projection pages the ETL parses) and
                                  raw_md/relatorio_politica_monetaria_integral/ (full text, last 3 years).
                                  Written by the Copom ETL, not by ingestion/
    trader/                     — 26 PDF (Trading Global Macro Markets), none extracted, scope undecided
    fiscal_policy/, inflation/  — 1 PDF each, extracted
    economic_activity/, labor_market/ — empty, future pillars
  mental_model/<gestora>/       — asset-manager letters: raw_pdf/ + raw_md/ + clean_md/. The letters
                                  are cross-area raw material, so their clean_md stays HERE; the
                                  syntheses built from them live in obsidian/<área>/mental_models/.
                                  kapitalo (83), verde_asset (200), kinea (60), kinea_insights (64),
                                  goldman_sachs (~80), spx_capital (7)
  ingestion/                    — land_space/<área>/ (drop zone) + scripts/ (run.py and friends)
  agent_mapping/                — acquisition planning, not agent knowledge:
    recommended_bibliography/   — <área>_bibliography_candidates.md / _gaps.md (what to source,
                                  with priority and suggested filename) and <área>_bibliography.md
                                  (the consolidated list: what exists and whether it was ingested)
    recommended_data/           — <área>_data_inventory.md
    data_tracker.xlsx
```

**`_legacy_ai_rewrite/`** folders inside some `raw_md/` hold the old AI-rewritten extractions, kept
but unused. See `INGESTION.md` for why they were replaced.

## Status by topic

**Exchange rate — complete.** 28 sources processed into
[`obsidian/exchange_rate/exchange_rate_conceptual_map.md`](../obsidian/exchange_rate/exchange_rate_conceptual_map.md),
9 clusters. 2 real gaps: FX options/volatility (Garman & Kohlhagen 1983) and non-Brazil EM depth
(Eichengreen & Hausmann 1999) — see `exchange_rate_bibliography_gaps.md`.

**Monetary policy — acquired, not processed.** 36 papers in `raw_pdf/theorical_literature/`, 1
extracted, no conceptual map. Missing: the Cukierman (1992) book and specific chapters. Decide
where to process Tambakis & Tarashev (2012), which also touches exchange rate.

**Trader — scope undecided.** Decide whether it is a topical pillar or feeds a trading
strategy/agent directly before processing chapters.

**economic_activity / fiscal_policy / inflation / labor_market — placeholders.** Candidates listed in
`agent_mapping/recommended_bibliography/`.

**Workflow for adding sources:** drop the PDF in `ingestion/land_space/<área>/`, run
`ingestion/scripts/run.py` — one PDF at a time, never in parallel (user's preferred workflow).

## Pending

- **Revisit `clean_md`'s definition** (flagged 2026-08, not decided) — see the same item in
  [`obsidian/CLAUDE.md`](../obsidian/CLAUDE.md).
- **Extend ingestion to the rest of the corpus**: 12 `exchange_rate`, 35 `monetary_policy` papers and
  all of `trader/`.
- **Equation/symbol garbling in `raw_md`** (e.g. Dornbusch 1976): inherent to pdfplumber on scanned
  PDFs of that era; would need a vision-based extraction if equation fidelity matters.
- **Monetary policy — build the conceptual map**, one source at a time.
