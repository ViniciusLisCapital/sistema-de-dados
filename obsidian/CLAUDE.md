# obsidian/ — Context for Claude

## Purpose

Obsidian vault: LIS's cross-linked macro knowledge base, organized by topic area (`exchange_rate`, `monetary_policy`, `inflation`, `fiscal_policy`, `labor_market`, `economic_activity`). This is the reader/agent-facing layer — wikilinked notes meant to be browsed and traversed, not a raw-material archive.

**Does not use and does not reconcile with** `repository/`'s own concept/synthesis layer (`agent_mapping/`) — deliberately parallel systems, per explicit user instruction. See [`repository/CLAUDE.md`](../repository/CLAUDE.md) for that side. The two trees do share extraction output as of 2026-08, at two tiers: full-text raw extractions (`repository/<topic>/raw_md/`) and this vault's own `sources/` tier is a direct copy of `repository/<topic>/clean_md/` (see "History" below) — but each tree's own curated/synthesis material (`sources/`'s condensation into `synthesis/` here; `agent_mapping/`'s conceptual maps there) stays independent.

`repository/ingestion/` (the PDF ingestion pipeline living inside `repository/`) is the thing that produces `clean_md/` in the first place — this vault's `sources/` tier is downstream of it (copy the output, once ingestion runs), not an independent process. See [`repository/ingestion/INGESTION.md`](../repository/ingestion/INGESTION.md) for how a PDF becomes `clean_md/`.

## Structure — three tiers per topic

```
obsidian/
  exchange_rate/
    concepts/    — atomic, cross-cutting theory notes (10 files)
    sources/     — populated (16 files) — one per repository/exchange_rate/clean_md/ source
    synthesis/   — condensed per-source notes (21 files)
  monetary_policy/    — concepts/ (0), sources/ (1), synthesis/ (1)
  inflation/          — concepts/ (1), sources/ (1), synthesis/ (1)
  fiscal_policy/      — concepts/ (1), sources/ (1), synthesis/ (1)
  labor_market/       — concepts/, sources/, synthesis/ — all empty, future pillar
  economic_activity/  — concepts/, sources/, synthesis/ — all empty, future pillar
```

### What each tier means

- **`concepts/`** — atomic, Zettelkasten-style notes, one per theoretical concept (e.g. `carry_trade.md`, `risk_premium.md`), densely cross-linked via `[[wikilinks]]` to other concepts, to `sources/` notes, and to `synthesis/` notes. Unchanged by the 2026-08 reorg.
- **`sources/`** — one note per original source (paper or manager corpus), holding the **full material with only garbage removed** — disclaimers, boilerplate, repeated legal text, anything not substantively about the topic. Nothing is condensed or summarized at this tier; it's the same completeness as the raw extraction, just cleaned. This is the vault-side equivalent of `repository/`'s `clean_md/` tier — populated as a straight copy of `repository/<topic>/clean_md/<name>.md`, same filename, no reformatting (see History below).
- **`synthesis/`** — condensed, distilled per-source notes: structured sections (context/motivation, core thesis, key mechanisms, main findings, limitations, connections), much shorter than the source. This tier already exists and is populated for `exchange_rate` (21 notes) and one file each for `monetary_policy`/`inflation`/`fiscal_policy`. Despite the folder name, every file here is tied to a **single** source (or a single manager's corpus) — none of them are yet a true cross-source narrative synthesis. Each carries a `**Source file:** [[...]]` line pointing at its `sources/` counterpart by filename (Obsidian resolves wikilinks by note name across the whole vault, regardless of folder).

### Intended agent/reader search path

concept → check `synthesis/` (is the condensation enough for the task?) → if not, go to `sources/` for the complete clean material. Raw, uncleaned extractions are not part of this path at all — that's why they were moved out of the vault (see History).

## History

**2026-08 — `raw/` removed, three-tier model adopted.** Each topic previously also had a `raw/` folder holding full, unclean, per-source extractions (e.g. `capital_mobility_exchange_rates_regimes (R. A. Mundell, 1963).md` — the complete text of the paper, reformatted with markdown headers but not trimmed at all). That duplicated `repository/<topic>/raw_md/`'s role once the `raw_pdf/raw_md/clean_md` convention was applied there the same day (see [`repository/CLAUDE.md`](../repository/CLAUDE.md)). So `raw/` was removed from every topic and its contents moved to `repository/<topic>/raw_md/`:

| Topic | Files moved | Notes |
|---|---|---|
| `exchange_rate` | 16 | 5 had a stray `_raw` suffix, stripped on move to match `raw_pdf/` basenames |
| `monetary_policy` | 1 | `monetary_policy_exchange_rates (BIS, 2026).md` |
| `fiscal_policy` | 1 | `fiscal_dominance (itau, 2025).md` — source PDF has since been moved into `repository/fiscal_policy/raw_pdf/` (was sitting in the old `ingestion/inbox/`, closed as part of the ingestion-pipeline move) |
| `inflation` | 1 | `em_food_inflation (goldamn, 2026).md` — same, now in `repository/inflation/raw_pdf/` |
| `labor_market` | 0 | folder was already empty |

**Later 2026-08 — `sources/` populated, broken wikilinks fixed.** All 19 `repository/<topic>/clean_md/` files that existed at the time (`exchange_rate` 16, `monetary_policy`/`fiscal_policy`/`inflation` 1 each) were copied verbatim into their matching `obsidian/<topic>/sources/<name>.md` — same filename as the source, no reformatting, consistent with "clean, not condensed." That fixed the wikilink gap flagged above: every `synthesis/` note's `**Source file:** [[...]]` line (relabeled from `**Raw file:**`, since the target is now the clean `sources/` tier, not a raw extraction) now resolves to a real note. Two things needed a direct fix rather than just copying files: the 5 `Krugman 2023 - ...` synthesis notes had a stray `_raw` suffix baked into their wikilink target from the old `raw/` era — stripped to match the actual `clean_md`/`sources/` basenames. `Fleming 1962` (in `synthesis/`) has no matching `sources/` note and stays unresolved — its source PDF is the one still blocked by `clean.py`'s safety-classifier issue on garbled scanned text (see [`repository/ingestion/INGESTION.md`](../repository/ingestion/INGESTION.md)'s "Known limitation" section), so no `clean_md` exists for it yet. The 4 `*_fx_mental_models.md` synthesis notes (asset-manager corpora, not single papers) were out of scope — they source from `repository/mental_model/`, not `repository/<topic>/clean_md/`.

## Pending

- **New sources arriving in `repository/<topic>/clean_md/`** (12 more `exchange_rate` PDFs and 35 `monetary_policy` PDFs still await ingestion — see `repository/CLAUDE.md`'s pending list) need the same copy-into-`sources/` treatment once they exist. Not automatic — redo the copy manually (or scripted) after each ingestion batch.
- **Fleming 1962 / Frenkel 1976** — no `sources/` note until their `clean_md` exists, which is blocked on the garbled-scan safety-classifier issue (see History above).
- **Reconcile with `repository/ingestion/`** — relationship between this vault's `sources/` tier and the ingestion pipeline's own folders is now simpler (ingestion writes `clean_md/`, this vault copies from it) but still not formalized as a repeatable step. Deferred.
- **`labor_market` / `economic_activity`** — fully empty, future pillars, same status as their `repository/` counterparts.
