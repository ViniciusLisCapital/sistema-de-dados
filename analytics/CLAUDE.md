# analytics/ — Overview

This is the applied/analytical layer: projects that consume the MySQL database (`macro_brasil`/`macro_international`, see [`domain/db/CLAUDE.md`](../domain/db/CLAUDE.md)) and turn it into data analysis, models, and the specific papers that structure them — self-contained HTML reports, a Power BI feed, and one macro-scoring thermometer. Distinct in purpose from `repository/`, which is the literature-curation/bibliography side (see root `CLAUDE.md`'s `repository/` section) — `analytics/` is where that theory gets tested against the actual database and turned into a deliverable. This file is the folder-level map; each project with enough of its own detail has its own `CLAUDE.md`.

## Subfolders

| Folder | Produces | Docs |
|---|---|---|
| `oraculo/` | Macro thermometer scores (1–10), feeds Power BI | [`oraculo/CLAUDE.md`](oraculo/CLAUDE.md) |
| `painel_setores/` | Sector panel, feeds Power BI directly | no dedicated `CLAUDE.md` yet — see below |
| `exchange_rate/` | Panorama Cambial (HTML report) | [`exchange_rate/CLAUDE.md`](exchange_rate/CLAUDE.md) |
| `inflation/` | Panorama de Inflação (HTML report) | [`inflation/CLAUDE.md`](inflation/CLAUDE.md) |
| `monetary_policy/` | BCB small-model replication (HTML report) | documented inline in root `CLAUDE.md` + [`monetary_policy/referencia/MODEL_REPLICATION_PLAN.md`](monetary_policy/referencia/MODEL_REPLICATION_PLAN.md) |
| `report_structure/` | Nothing on its own — shared build-time scaffolding the report projects above assemble from | [`report_structure/CLAUDE.md`](report_structure/CLAUDE.md) |

## Shared report pattern (`exchange_rate/`, `inflation/`, `monetary_policy/`)

- `generate_report.py` loads MySQL tables (each `_load_*()` wrapped in its own try/except, so one missing/broken table only degrades that section instead of failing the whole report), serializes to JSON, and substitutes a `/*REPORT_DATA*/` marker inside `report.html` — no Jinja2, no build step.
- `report.html` is a fixed template: HTML + CSS + Plotly.js from CDN, tabs via JS `display` toggling, nothing server-side.
- Chart interaction is identical across all three: free pan/zoom on both axes (`dragmode:'pan'` + `scrollZoom:true`), plus a `_bindYAutofit()` helper that re-fits Y only when a rangeselector preset button moves X without an accompanying user gesture on Y — see [`.claude/rules/lis-dashboards.md`](../.claude/rules/lis-dashboards.md) for the full model and history.
- `data/` vs `referencia/` convention: `data/` holds what the scripts actually read/write (e.g. `inflation/data/ipca_bcb_series.csv`); `referencia/` holds context nothing reads (PDFs, literature, the original BCB model spec). Same split, repo-wide since 2026-07.
- **Since 2026-08, the boilerplate pieces of this pattern (the theme CSS, the `_bindYAutofit` JS, the substitution/write-out plumbing) live in [`report_structure/`](report_structure/CLAUDE.md) as shared build-time assets, not hand-copy-pasted per report.** `inflation/` (fully migrated) is the pilot; `exchange_rate/` is partially migrated (JS + harness, not theme CSS — needs the 2026-07 reskin first); `monetary_policy/` is untouched, deferred on purpose — see `report_structure/CLAUDE.md`'s Migration status.

## `painel_setores/`

No dedicated `CLAUDE.md` yet. `painel_setores.py` fetches BCB/IBGE series directly (`Request_data_bcb()`, `connectors.ibge`) and feeds a Power BI file (`docs/PAINEL DE SETORES.pbix`) — no HTML report, no `/*REPORT_DATA*/` pattern, no MySQL involved. `docs/` here means "supporting Excel/Word/pbix files", a different sense of "docs" than `oraculo/docs/` below.

## `oraculo/` — two things not yet in `oraculo/CLAUDE.md`

See [`oraculo/CLAUDE.md`](oraculo/CLAUDE.md) for the module breakdown. Found while surveying this folder, not yet fixed (see Pending):

- `base/` and `docs/` both hold `Central_base.csv`/`d_table.xlsx`/`Weights.xlsx`. Only `base/` is a real package (`__init__.py`) and is what's actually produced/consumed — `docs/` is not referenced anywhere in code and hasn't been touched since the initial commit. Looks like a stale duplicate.
- `us/us/term_us.py` is an older copy of `us/term_us.py` — hardcoded to the pre-`analytics/`-migration path (`C:\...\oraculo\us\base\US_BASE.csv`) and missing the current version's `run()` entry point. Not imported anywhere.

## `monetary_policy/models/curva_juros/`

Legacy yield-curve material (`yield_curve.py`, `yield_curve_model.py`, DI/títulos/governo spreadsheets), moved here from `quarantine/` in 2026-08. Not wired into `model.py` or referenced by anything else under `analytics/` — see root `CLAUDE.md`'s Pendências.

## Pending

- **Give `exchange_rate/` the 2026-07 LIS-dashboard CSS reskin, then migrate its theme onto `report_structure/theme.css`** — its JS/harness are already migrated (see `report_structure/CLAUDE.md` Migration status); only the theme CSS is left, and it needs the actual reskin first (navy header/`system-ui` font → the light Barlow theme `inflation/` already has), not a mechanical marker swap.
- **Migrate `monetary_policy/` onto `report_structure/` entirely** — deferred on purpose, not started.
- **`oraculo/docs/` vs `oraculo/base/` duplication** — confirm `docs/` is dead and remove it, or document why both exist.
- **`oraculo/us/us/`** — looks safe to remove, superseded by `oraculo/us/term_us.py`.
- **`analytics/inflation/reservoirs.py`** — fetches ONS hydro reservoir levels (`EAR_DIARIO_RESERVATORIOS_*`), which has no obvious connection to inflation on its face. No `run()`/entry-point pattern like its sibling scripts, not imported anywhere, not mentioned in `inflation/CLAUDE.md`. Moved from `quarantine/` in this session's git history but not wired into any pipeline yet — confirm the intended destination/purpose (energy prices → administered-inflation component?) or remove.
