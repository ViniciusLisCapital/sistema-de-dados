# repository/ — Context for Claude

**Naming note:** this folder was formerly named `agent_bibliography/` — treat that name as a synonym if it turns up elsewhere (git history, older docs).

## Purpose

Curated knowledge base feeding LIS's macro analysis agents: raw source PDFs organized by topic area, plus the "maps" derived from them (conceptual maps, bibliography candidate/gap lists, data inventories). Each area follows the reusable process in [`BIBLIOGRAPHY_METHODOLOGY.md`](BIBLIOGRAPHY_METHODOLOGY.md).

**Does not use and does not reconcile with** the `obsidian/` vault's own concept/synthesis pages — deliberately parallel systems, per explicit user instruction. That said, as of 2026-08 `obsidian/<topic>/raw_md/`-equivalent files (full untouched extractions, previously living in `obsidian/<topic>/raw/`) were consolidated here, into `repository/<topic>/raw_md/` — see [`obsidian/CLAUDE.md`](../obsidian/CLAUDE.md). So the two trees no longer overlap on raw extractions, even though their curated/synthesis layers stay independent.

**Does now interact with `ingestion/`** (updated 2026-08, reversing the earlier "deliberately parallel, no interaction" note) — the ingestion pipeline was moved to live inside this tree, at `repository/ingestion/`, the same day this was written; later the same day, split into a `land_space/` drop zone and a `scripts/` folder for the pipeline code (see below). Drop a PDF into `repository/ingestion/land_space/<topic>/` and run `repository/ingestion/scripts/run.py`: it populates this tree's `raw_pdf/`/`raw_md/`/`clean_md/` tiers in one command. See [`repository/ingestion/INGESTION.md`](ingestion/INGESTION.md) for the full pipeline and why its AI-based cleaner (`clean.py`) was found unreliable and replaced with a deterministic one (`clean_code.py`).

## Structure

```
repository/
  BIBLIOGRAPHY_METHODOLOGY.md   — reusable process, not the output of any single topic
  exchange_rate/                — raw_pdf/ (28), raw_md/ (16, genuine pdfplumber extractions via
                                  repository/ingestion/), clean_md/ (16, via clean_code.py) — complete;
                                  12 raw_pdf sources still await extraction
  monetary_policy/               — raw_pdf/ (36, incl. the ex-ingestion-inbox BIS file), raw_md/ (1),
                                  clean_md/ (1) — most candidates acquired, map not built yet; 35 raw_pdf
                                  sources still await extraction
  trader/                        — raw_pdf/ (26, Trading Global Macro Markets), raw_md/, clean_md/ — scope undecided
  economic_activity/             — raw_pdf/, raw_md/, clean_md/, all empty — future pillar
  fiscal_policy/                 — raw_pdf/ (1, ex-ingestion-inbox), raw_md/ (1), clean_md/ (1) — future pillar
  inflation/                     — raw_pdf/ (1, ex-ingestion-inbox), raw_md/ (1), clean_md/ (1) — future pillar
  labor_market/                  — raw_pdf/, raw_md/, clean_md/, all empty — future pillar
  ingestion/                     — the PDF ingestion pipeline itself (moved here 2026-08, was a
                                  top-level ingestion/ folder before) — land_space/ (drop-zone
                                  topic folders) + scripts/ (extract.py/clean_code.py/run.py/etc.),
                                  see repository/ingestion/INGESTION.md
  agent_mapping/
    conceptual_maps/            — <topic>_conceptual_map.md, one per area (only exchange_rate exists so far)
    recommended_bibliography/   — <topic>_bibliography_candidates.md / _gaps.md
    recommended_data/           — <topic>_data_inventory.md
    data_tracker.xlsx
  mental_model/                 — 291 files, raw sources (asset manager letters): kapitalo/ (83 PDF,
                                  raw_md/ + clean_md/ both complete and cross-validated across all
                                  three format eras — see CURATION_SCOPE.md), kinea/ (60 .md), kinea_insights/ (64 .md),
                                  spx_capital/ (7 PDF),
                                  verde_asset/ (raw_pdf/ growing — 1999-2026 pulled so far; see
                                  verde_asset/DOWNLOAD_PROCESS.md for the URL pattern/download process)
```

**`consolidated/` moved out of here in 2026-07** — the presentable exchange-rate synthesis now lives in [`team_materials/agent_materials/exchange_rate/`](../team_materials/agent_materials/exchange_rate/). See the root `CLAUDE.md` for the full three-branch distinction for exchange-rate material.

**`raw_pdf/`/`raw_md/`/`clean_md/` convention applied 2026-08** to every direct child of `repository/` except `agent_mapping/` — `exchange_rate`, `monetary_policy`, `trader`, `economic_activity`, `fiscal_policy`, `inflation`, `labor_market` — mirroring the per-source structure already used inside `mental_model/` (e.g. `mental_model/kapitalo/`). This was a pure file move (PDFs relocated into each topic's new `raw_pdf/`); no PDF→raw_md extraction or raw_md→clean_md curation has been done yet for `trader`, `economic_activity`, or `labor_market`.

**`raw_md/` initially backfilled from `obsidian/` the same day, then found to be corrupted, then genuinely fixed, then the whole ingestion pipeline moved inside this tree and reorganized — all same day (2026-08).** `exchange_rate` (16 files), `monetary_policy` (1), `fiscal_policy` (1), `inflation` (1) initially had their `raw_md/` populated from full-text notes sitting in `obsidian/<topic>/raw/` (see [`obsidian/CLAUDE.md`](../obsidian/CLAUDE.md) for the vault-side three-tier `concepts/sources/synthesis` rationale). **A full audit against each source PDF then found all 14 non-Krugman files in that batch had actually been produced by an AI rewriting pass at some earlier point** (not a raw extraction at all) — symptoms ranged from voice paraphrasing to, in several cases, whole sections silently missing (Conclusions, Results, References, worked examples). Root cause and fix: see [`repository/ingestion/INGESTION.md`](ingestion/INGESTION.md)'s "AI cleaning pass is unreliable" section. Fix applied: genuine `pdfplumber` raw extractions already existed, untouched, in the pipeline's `work/<topic>/*_raw.md` (left over from an earlier ingestion run) — these were published into `raw_md/`, and a deterministic regex cleaner (`clean_code.py`, enhanced the same day with a generic running-header detector and a References-block-cut fix) now populates `clean_md/` for the first time for these 19 files. **The previous AI-rewritten files were not deleted** — each was moved to `repository/<topic>/raw_md/_legacy_ai_rewrite/<name>.md` before being replaced. The whole ingestion pipeline (previously a top-level `ingestion/` folder, separate from `repository/`) was then moved to `repository/ingestion/` and simplified to a single-command workflow, per explicit request — the 3 source PDFs that had been sitting in the old `ingestion/inbox/{fiscal_policy,inflation,monetary_policy}/` (never copied into `repository/`) were moved into their proper `repository/<topic>/raw_pdf/` as part of that move, closing that gap. **Later the same day**, the drop zone and the pipeline code (which had briefly been siblings directly under `repository/ingestion/`) were split apart per explicit request: topic drop-zone folders moved into `repository/ingestion/land_space/<topic>/`, and every script into `repository/ingestion/scripts/` — see `INGESTION.md` for the layout.

## Status by topic

**Exchange rate — complete.** 28/28 sources processed into `exchange_rate_conceptual_map.md`, 9 theme clusters. 2 real gaps remain: FX options/volatility (Garman & Kohlhagen 1983) and non-Brazil EM depth (Eichengreen & Hausmann 1999) — see `exchange_rate_bibliography_gaps.md`. One source sitting in `monetary_policy/` (Tambakis & Tarashev 2012) also touches exchange rate — decide which map processes it.

**Monetary policy — in progress.** Nearly all 30 candidates already acquired in `monetary_policy/` (the candidates file itself still says "nothing acquired yet" — stale). Missing: the Cukierman (1992) book, specific chapters, and COPOM §8 primary materials (scope open). **No conceptual map built yet** — that's the real next step.

**Trader — scope undecided.** 15 chapters of *Trading Global Macro Markets* (Willer & Saunders, 2024) already in the standard naming convention, no `conceptual_map`/`bibliography_candidates`/`data_inventory` yet. Decide: full fourth topical pillar, or a different use (feeding a trading strategy/agent directly, no formal conceptual map)? Don't start chapter-by-chapter processing until decided.

**economic_activity / fiscal_policy / inflation / labor_market — placeholders.** Empty; candidates already listed in `agent_mapping/recommended_bibliography/`; nothing acquired yet.

**Workflow for adding sources:** see "Standard workflow per topic" in [`BIBLIOGRAPHY_METHODOLOGY.md`](BIBLIOGRAPHY_METHODOLOGY.md) — one PDF at a time, never in parallel (user's preferred workflow).

## Pending

- **Revisit `clean_md`'s definition (flagged 2026-08, not decided)**: current rule, enforced by `clean_code.py`, is strict — raw text minus true garbage only, zero rewriting/restructuring/condensation (this strictness was adopted *because* the earlier AI cleaner's restructuring silently corrupted content — see `INGESTION.md`'s "AI cleaning pass is unreliable" finding). User is now reconsidering: `clean_md` could instead mean an *organized* version of the raw text — reformatted into a cleaner, more readable structure (paragraph breaks, headers, etc. restoring what PDF extraction mangles) — while still preserving all content, i.e. organizing, not condensing or truncating. This is a real design question (how do you guarantee "reorganize but never drop/paraphrase content" without reintroducing the same failure mode?) that needs to be thought through before touching `clean_code.py`'s behavior. Same question applies to `obsidian/`'s `sources/` tier, which mirrors this definition — see [`obsidian/CLAUDE.md`](../obsidian/CLAUDE.md).
- **Ingestion process — extend to the rest of the corpus**: the 2026-08 fix (see above) only covered the 19 files that already had a genuine raw extraction sitting around. Still not run through `repository/ingestion/scripts/run.py`: 12 more `exchange_rate/raw_pdf/` sources, 35 more `monetary_policy/raw_pdf/` sources, and all of `trader/`. Same one-PDF-at-a-time workflow as `BIBLIOGRAPHY_METHODOLOGY.md`, just via `repository/ingestion/` instead of manual extraction — drop the PDF in `repository/ingestion/land_space/<topic>/`, run `scripts/run.py`.
- **`_legacy_ai_rewrite/` folders — decide final disposition**: `exchange_rate` (16), `fiscal_policy`/`inflation`/`monetary_policy` (1 each) now hold the old AI-rewritten files, kept but unused. No action needed unless/until `clean.py`'s bugs are fixed and it's worth comparing outputs.
- **Equation/symbol garbling in `raw_md`** (e.g. `expectations_and_exchange_rate_dynamics (Dornbusch, 1976)`): Greek letters/subscripts in numbered equations get mangled by `pdfplumber` on this era of scanned PDF — inherent to the raw extraction, not something either cleaner fixes. Would need a different (e.g. vision-based) extraction method if equation fidelity matters for a given source.
- **Exchange rate — 2 real gaps**: FX options/volatility (Garman & Kohlhagen 1983), non-Brazil EM depth (Eichengreen & Hausmann 1999). See `exchange_rate_bibliography_gaps.md`.
- **Monetary policy — build the conceptual map**: candidates acquired, still need to process them into `monetary_policy_conceptual_map.md` (doesn't exist yet), one at a time. Still need to acquire Cukierman (1992) and COPOM §8 materials. Decide where to process Tambakis & Tarashev (2012).
- **Trader — decide scope**: see above.
- **`mental_model/kapitalo/` — curation complete (2026-07-31)**: all 83 letters (Jul/2019–Mai/2026) have both `raw_md/` (permanent audit trail) and `clean_md/` (curated per `CURATION_SCOPE.md`, same purpose as the Verde Asset corpus — feeds FX/macro mental-model synthesis), all cross-validated against each letter's own performance-attribution table. Three PDF template eras identified and handled: era 1 "Carta K10" (Jul/2019–Aug/2023, single-column), era 2 "CARTA DO GESTOR" (Sep/2023–Fev/2025, two-column narrative — needed column-aware re-extraction, now fixed), era 3 (Mar/2025–present, same two-column narrative plus a further layout tweak: split section headers, relocated VaR footnote, wrapped table-row label — handled in `curate.py` via additive regex fallbacks). No further action needed unless a new letter arrives in a yet-unseen format.
