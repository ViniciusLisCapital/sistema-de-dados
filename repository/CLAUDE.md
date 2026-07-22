# repository/ — Context for Claude

**Naming note:** this folder was formerly named `agent_bibliography/` — treat that name as a synonym if it turns up elsewhere (git history, older docs).

## Purpose

Curated knowledge base feeding LIS's macro analysis agents: raw source PDFs organized by topic area, plus the "maps" derived from them (conceptual maps, bibliography candidate/gap lists, data inventories). Each area follows the reusable process in [`BIBLIOGRAPHY_METHODOLOGY.md`](BIBLIOGRAPHY_METHODOLOGY.md).

**Does not use and does not reconcile with** the `obsidian/` vault (pre-existing concept pages) — deliberately parallel systems, per explicit user instruction. Also doesn't interact with the `ingestion/` pipeline.

## Structure

```
repository/
  BIBLIOGRAPHY_METHODOLOGY.md   — reusable process, not the output of any single topic
  exchange_rate/                — 28 raw PDFs + verde_fx_mental_models.md — complete
  monetary_policy/              — 35 raw PDFs — most candidates acquired, map not built yet
  trader/                       — 26 raw PDFs (Trading Global Macro Markets) — scope undecided
  economic_activity/            — empty, future pillar
  fiscal_policy/                — empty, future pillar
  inflation/                    — empty, future pillar
  labor_market/                 — empty, future pillar
  agent_mapping/
    conceptual_maps/            — <topic>_conceptual_map.md, one per area (only exchange_rate exists so far)
    recommended_bibliography/   — <topic>_bibliography_candidates.md / _gaps.md
    recommended_data/           — <topic>_data_inventory.md
    data_tracker.xlsx
  mental_model/                 — 291 files, raw sources (asset manager letters): kapitalo/ (83 PDF),
                                  kinea/ (60 .md), kinea_insights/ (64 .md), spx_capital/ (7 PDF),
                                  verde_asset/ (77 PDF)
```

**`consolidated/` moved out of here in 2026-07** — the presentable exchange-rate synthesis now lives in [`team_materials/agent_materials/exchange_rate/`](../team_materials/agent_materials/exchange_rate/). See the root `CLAUDE.md` for the full three-branch distinction for exchange-rate material.

## Status by topic

**Exchange rate — complete.** 28/28 sources processed into `exchange_rate_conceptual_map.md`, 9 theme clusters. 2 real gaps remain: FX options/volatility (Garman & Kohlhagen 1983) and non-Brazil EM depth (Eichengreen & Hausmann 1999) — see `exchange_rate_bibliography_gaps.md`. One source sitting in `monetary_policy/` (Tambakis & Tarashev 2012) also touches exchange rate — decide which map processes it.

**Monetary policy — in progress.** Nearly all 30 candidates already acquired in `monetary_policy/` (the candidates file itself still says "nothing acquired yet" — stale). Missing: the Cukierman (1992) book, specific chapters, and COPOM §8 primary materials (scope open). **No conceptual map built yet** — that's the real next step.

**Trader — scope undecided.** 15 chapters of *Trading Global Macro Markets* (Willer & Saunders, 2024) already in the standard naming convention, no `conceptual_map`/`bibliography_candidates`/`data_inventory` yet. Decide: full fourth topical pillar, or a different use (feeding a trading strategy/agent directly, no formal conceptual map)? Don't start chapter-by-chapter processing until decided.

**economic_activity / fiscal_policy / inflation / labor_market — placeholders.** Empty; candidates already listed in `agent_mapping/recommended_bibliography/`; nothing acquired yet.

**Workflow for adding sources:** see "Standard workflow per topic" in [`BIBLIOGRAPHY_METHODOLOGY.md`](BIBLIOGRAPHY_METHODOLOGY.md) — one PDF at a time, never in parallel (user's preferred workflow).

## Pending

- **Exchange rate — 2 real gaps**: FX options/volatility (Garman & Kohlhagen 1983), non-Brazil EM depth (Eichengreen & Hausmann 1999). See `exchange_rate_bibliography_gaps.md`.
- **Monetary policy — build the conceptual map**: candidates acquired, still need to process them into `monetary_policy_conceptual_map.md` (doesn't exist yet), one at a time. Still need to acquire Cukierman (1992) and COPOM §8 materials. Decide where to process Tambakis & Tarashev (2012).
- **Trader — decide scope**: see above.
