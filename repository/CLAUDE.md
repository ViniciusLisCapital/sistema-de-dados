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
    exchange_rate/              — 29 PDF, 29 raw_md (2026-10-29, after the move to the owners' folders)
    monetary_policy/            — literature flat at the top of raw_pdf/ (58 PDFs, all ingested; the
                                  theorical_literature/ subfolder was dissolved 2026-10-19), and
                                  central_bank/, the same tree as the vault's
                                  clean_md/central_bank/: raw_pdf/central_bank/{atas (82),
                                  rpm (110, 1999-06 on)} and raw_md/central_bank/{comunicados (234),
                                  atas (261), rpm (full text, last 3 years), rpm_paginas_projecao
                                  (110, only the projection pages the ETL parses)}.
                                  Written by the Copom ETL, not by ingestion/
    trader/                     — 26 PDF, all ingested 2026-10-20: chapters of two Willer et al.
                                  books (Trading Global Macro Markets, 2024; Trading Fixed Income
                                  and FX in Emerging Markets, 2020), literature of a new trader agent
    fiscal_policy/ (10), inflation/ (8), economic_activity/ (5), external/ (13), expectations/ (6)
                                — the literature of the five new agents: their layer 1, all ingested
                                  and synthesized 2026-10-29 (SISTEMA_AGENTES II.IV), plus what came
                                  from exchange_rate/ and monetary_policy/ when every source went to
                                  its owner's folder the same day; external/ and expectations/ are
                                  new topics, their Qual tabs were created by tracker.py
    labor_market/               — empty, future pillar
  mental_model/<gestora>/       — asset-manager letters: raw_pdf/ + raw_md/ + clean_md/. The letters
                                  are cross-area raw material, so their clean_md stays HERE; the
                                  syntheses built from them live in obsidian/<área>/mental_models/.
                                  Process: mental_model/MENTAL_MODELS.md (/ingest → /mental)
                                  kapitalo (83), verde_asset (200), kinea (60), kinea_insights (64),
                                  goldman_sachs (~80), spx_capital (7)
  ingestion/                    — scripts/ + settings.yaml (per-file settings, files needing
                                  attention, topics on hold) + LOG.md; run by /ingest [topic], which
                                  sweeps <área>/raw_pdf/ for PDFs without raw_md. See INGESTION.md
  agent_mapping/                — acquisition planning, not agent knowledge:
    data_tracker.xlsx           — THE list, the only one (since 2026-10-19 the .md lists of
                                  recommended_bibliography/ and recommended_data/ live here):
                                  "Qual - <Area>" = literature (candidates, acquired, dropped;
                                  acquisition priority, suggested file and where to get it in
                                  Comments), "Quant - <Area>" = data inventory, "Notes" = the
                                  reasoning per cluster / data section (scope, open gaps,
                                  acquisition order, why a category matters). Columns A–I and
                                  Notes are hand-kept, and so are J–L of the Qual tabs
                                  (Dono, Camada, Fila: owner agent, layer and queue position,
                                  SISTEMA_AGENTES I.III.xvi–xvii); M–S of the Qual tabs,
                                  "Literature summary", "Mental Models" (one row per
                                  area × manager document and per letter) and "Copom" (one row per
                                  statement, minutes, RPM, with the layer-1 rule) are rewritten
                                  by tracker.py, run after every ingestion, /mental done and Copom
                                  load (since 2026-10-21). In git
                                  since 2026-10-20 (the one *.xlsx exception in .gitignore)
```

**`_legacy_ai_rewrite/`** folders inside some `raw_md/` hold the old AI-rewritten extractions, kept
but unused. See `INGESTION.md` for why they were replaced.

## Status by topic

**Exchange rate — complete.** 28 sources processed into
[`obsidian/exchange_rate/exchange_rate_conceptual_map.md`](../obsidian/exchange_rate/exchange_rate_conceptual_map.md),
9 clusters. 2 real gaps: FX options/volatility (Garman & Kohlhagen 1983) and non-Brazil EM depth
(Eichengreen & Hausmann 1999, ingested since and, like the capital-flow sources, in external/ with
the external agent as owner).

**Monetary policy — ingested (2026-10-20).** 58 PDFs in `raw_pdf/` since the move to the owners'
folders (2026-10-29), all with raw_md and clean_md; 49 have a synthesis note. The conceptual map is
`obsidian/monetary_policy/monetary_policy_conceptual_map.md`. The list is the Qual - Monetary Policy tab
(12 clusters plus the legal sources and the Copom track); still missing is Brainard (1967), paywalled on
JSTOR, and three books were dropped. Since 2026-10-21 the agents grow by layers (`PRINCIPIOS_AGENTES.md`
I.VI): the 9 sources without synthesis are only synthesized if they fall in layer 1 or get promoted. The
extraction quirks (the two Caesar-shifted CGG files, one here and the 2000 one in external/, letter
spacing) are handled by `ingestion/settings.yaml`.

**Trader — ingested, for a new agent.** Decided 2026-10-20: the literature of a new trader agent,
not a topical pillar (`SISTEMA_AGENTES.md` I.II.vii). All 26 chapters ingested the same day; the
2020 book's chapters use `pymupdf` (plumber leaves 40-180 cid glyphs each), the 2024 book's the
default (pymupdf splits the drop cap). Known loss: rotated chart labels read backwards in the 2024
chapters, body text intact. The Qual - Trader tab is curated (8 clusters by asset class), Notes has
the scope. Next: `/vault trader`.

**fiscal_policy / external / inflation / economic_activity / expectations — layer 1 in (2026-10-29).**
One source per channel of each conceptual map, owner and layer in the Qual tabs; the rest of each tab is
the stock for promotion.

**Every source sits in its owner's folder (since 2026-10-29).** The owner is the tracker's Dono; the
folder follows it. `ingestion/scripts/owner.py --move` moves a source whose Dono's folder is not its
tab's: PDF, raw_md, clean_md, synthesis, the vault's wikilinks (the frozen cycle snapshots in
`obsidian/ciclos/` excepted), its LOG.md lines and its tracker row (merged into the owner's own row
when the owner's list already had the source). `tracker.py` prints the sources out of place after
every run, so a Dono changed by hand is noticed. 17 moved on 2026-10-29: from exchange_rate/ to
external/ (7), inflation/ (3) and monetary_policy/ (Mundell 1963); from monetary_policy/ to
exchange_rate/ (4), external/ (2) and inflation/ (Calvo 1983).
**labor_market — placeholder.** Candidates in its Qual tab.

**The Quant tabs date from July (2026-07-22, the inventories' last real revision; exchange rate
and monetary policy to Sep).** Many gaps they list have since been closed — the Copom decision
table (`pm_copom_reuniao`), the DI curve (`br_di_grade`), the policy rates (`br_interest_rate`
POLICY, `cmb_policy_rates`), the inflation target (`inflc_meta`), the fiscal tables (`fisc_*`),
commodity prices (`comm_*`). A refresh against `domain/db/registry.py` is pending.

**Workflow for adding sources:** save the PDF in `<área>/raw_pdf/`, run `/ingest` (or
`/ingest <área>`). The agent goes one PDF at a time, never in parallel (user's preferred workflow);
the status lands in `agent_mapping/data_tracker.xlsx`.

## Pending

- **Revisit `clean_md`'s definition** (flagged 2026-08, not decided) — see the same item in
  [`obsidian/CLAUDE.md`](../obsidian/CLAUDE.md).
- **`/vault trader`** (synthesis and concepts) and the design of the trader agent; the base is one
  author team, worth widening (tracker Notes).
- **Low priority — two file names list only one author** (breaks the naming rule, not the tracker
  match): `depreciation_pass_through (Goldfajn, 2000)` is Goldfajn & Werlang, and
  `padrao_transmissao_cambial (Cortapasso, 2023)` is Araújo, Caldarelli & Cortapasso. Renaming
  means the PDF, raw_md, clean_md, synthesis note, the wikilinks to it, settings.yaml and LOG.md.
- **Equation/symbol garbling in `raw_md`** (e.g. Dornbusch 1976): inherent to pdfplumber on scanned
  PDFs of that era; would need a vision-based extraction if equation fidelity matters. For
  born-digital PDFs the `pymupdf` mode maps math symbols to Unicode (2026-10-19).
- **The 16 exchange-rate files ingested before 2026-10-19** (some now in external/, inflation/ and
  monetary_policy/, their owners' folders) used `x_tolerance=3` and the old References cut; re-run
  with `/ingest <topic> "<file>" --overwrite` if one shows glued words or a missing appendix.
- **One file name with a typo**, kept so links don't break: `fiscal_dominance (itau, 2025)`
  (Itaú, lowercase). Its synthesis note carries the same name since 2026-10-19, so the tracker
  matches it exactly. The other one, `em_food_inflation (goldamn, 2026)`, was renamed to
  `(Goldman, 2026)` on 2026-10-20, with its raw_md, clean_md, synthesis note and wikilinks.
