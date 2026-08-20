# analytics/ — Overview

This is the applied/analytical layer: projects that consume the MySQL database (`macro_brasil`/`macro_international`, see [`domain/db/CLAUDE.md`](../domain/db/CLAUDE.md)) and turn it into data analysis, models, and the specific papers that structure them — self-contained HTML reports, a Power BI feed, and one macro-scoring thermometer. Distinct in purpose from `repository/`, which is the literature-curation/bibliography side (see root `CLAUDE.md`'s `repository/` section) — `analytics/` is where that theory gets tested against the actual database and turned into a deliverable. This file is the folder-level map; each project with enough of its own detail has its own `CLAUDE.md`.

## Layout: country > area (2026-08)

`analytics/` is organised **country first, area second** — `analytics/brasil/credit/`, not
`analytics/credit/`. Chosen over area-first (`analytics/credit/brasil/`) when the US branch was
opened: an area report is written against one country's schema, one country's release calendar and
one country's institutional detail, so the country is the stronger boundary; area-first would have
put two reports that share no code and no data in the same folder just because they share a name.
Python imports follow: `from analytics.brasil.credit import saldo_tab`.

**What stays at the root of `analytics/` instead of under a country:** anything whose input is not a
single country's schema — build-time scaffolding (`report_structure/`), the release-calendar monitor
(`release_calendar/`, mirroring `domain/release_calendar/`), and the thermometer (`oraculo/`, which
already carries its own internal `brasil/`+`us/` split around a shared `base/`). The test is the data
source, not the audience: a module that reads only `macro_brasil` belongs to `brasil/`; one that
reads both, or reads no schema at all, belongs at the root.

**`reports/` mirrors this.** A report's output goes to `reports/<country>/` — `analytics/brasil/credit/`
writes `reports/brasil/Credit.html`. Cross-country outputs stay at the root of `reports/`, which today
means only `release_calendar.html`. The reason is collision, not tidiness: Brazil and the US both
produce a report that wants to be called `Inflation.html`. The `run(output=...)` default in each
`generate_report.py` is the single place this is encoded; `render_report()` creates the country folder
if it doesn't exist, so a new country needs no setup step.

## Subfolders

| Folder | Produces | Docs |
|---|---|---|
| **`brasil/`** | | |
| `brasil/painel_setores/` | Sector panel, feeds Power BI directly | no dedicated `CLAUDE.md` yet — see below |
| `brasil/exchange_rate/` | Panorama Cambial (HTML report — 6 data tabs + the 3 model tabs fused in from the ex-standalone PPP dashboard, 2026-08) | [`brasil/exchange_rate/CLAUDE.md`](brasil/exchange_rate/CLAUDE.md) |
| `brasil/inflation/` | Panorama de Inflação (HTML report) | [`brasil/inflation/CLAUDE.md`](brasil/inflation/CLAUDE.md) |
| `brasil/monetary_policy/` | Phillips-curve estimation (`phillips_excel.py` → auditable xlsx) + reference material. **No HTML report** — the BCB small-model replication was removed 2026-08 | documented inline in root `CLAUDE.md` + [`brasil/monetary_policy/referencia/MODEL_REPLICATION_PLAN.md`](brasil/monetary_policy/referencia/MODEL_REPLICATION_PLAN.md) |
| `brasil/economic_activity/` | Panorama de Atividade Econômica (HTML report — PIB/PIM/PMC/PMS/IBC-Br) | [`brasil/economic_activity/CLAUDE.md`](brasil/economic_activity/CLAUDE.md) |
| `brasil/fiscal_policy/` | Panorama Fiscal (HTML report — receita/despesa GFSM+RTN, dívida líquida/DLSP, investimento federal por GND, impulso fiscal) | [`brasil/fiscal_policy/CLAUDE.md`](brasil/fiscal_policy/CLAUDE.md) |
| `brasil/credit/` | Panorama de Crédito (HTML report — novo, substitui `credit_stress/`) | [`brasil/credit/CLAUDE.md`](brasil/credit/CLAUDE.md) |
| `brasil/labor_market/` | Panorama de Mercado de Trabalho (HTML report — IBGE/PNAD + CAGED/MTE, só visualização) | [`brasil/labor_market/CLAUDE.md`](brasil/labor_market/CLAUDE.md) |
| **`us/`** | | |
| `us/inflation/` | US Inflation (HTML report — CPI-U, both of the CPI's published trees in one hierarchy-table structure). First report under `us/`, 2026-08 | [`us/inflation/CLAUDE.md`](us/inflation/CLAUDE.md) |
| **cross-country (root)** | | |
| `oraculo/` | Macro thermometer scores (1–10), feeds Power BI. Country split is *internal* (`oraculo/brasil/`, `oraculo/us/`, shared `oraculo/base/`), so it stays at the root | [`oraculo/CLAUDE.md`](oraculo/CLAUDE.md) |
| `release_calendar/` | Calendário de Divulgações (HTML report — forward-looking, reads a local YAML, not MySQL) | [`release_calendar/CLAUDE.md`](release_calendar/CLAUDE.md) |
| `report_structure/` | Nothing on its own — shared build-time scaffolding the report projects assemble from (theme CSS, `y_autofit.js`, `builder.py`, and `tree_helpers.py`) | [`report_structure/CLAUDE.md`](report_structure/CLAUDE.md) |

## Metric layers (read before adding a metric selector to any tab)

Every interactive table here exposes the same three orthogonal axes over its series — **aggregation
level** (native frequency → quarter/semester/12m/year, rolling or closed calendar), **nominal vs.
real**, and **modelling** (Nível / Y-Y / marginal / % PIB) — applied in a fixed order (deflate at the
native frequency → seasonally adjust → aggregate → compare). The spec, the degenerate combinations to
disable, the incomplete-period rule, which primitive to reuse, and the conventions still left open
(notably the `% PIB` denominator for flows): [`metric_layers.md`](metric_layers.md).

## Seasonal adjustment

Two methods available — STL (in-process, the incumbent, ~391 series) and X-13ARIMA-SEATS (US Census Bureau binary, installed 2026-08, not yet used in production). **Which one applies is decided case by case, not by a blanket rule** (explicit user decision, 2026-08). Full inventory of which series use which, the measured X-13-vs-STL scorecard against IBGE's official adjustment, X-13's practical failure modes, and the parallel-subprocess recipe: [`seasonal_adjustment.md`](seasonal_adjustment.md).

## Shared report pattern (all of `brasil/`'s report folders)

- `generate_report.py` loads MySQL tables (each `_load_*()` wrapped in its own try/except, so one missing/broken table only degrades that section instead of failing the whole report), serializes to JSON, and substitutes a `/*REPORT_DATA*/` marker inside `report.html` — no Jinja2, no build step. `exchange_rate/` additionally passes `extra_markers=` for its three model-tab payloads (`/*PPP_DATA*/`, `/*FXATTR_DATA*/`, `/*RIDGE_DATA*/`), the one report with more than one JSON marker.
- `report.html` is a fixed template: HTML + CSS + Plotly.js from CDN, tabs via JS `display` toggling, nothing server-side.
- Chart interaction is identical across all four: free pan/zoom on both axes (`dragmode:'pan'` + `scrollZoom:true`), plus a `_bindYAutofit()` helper that re-fits Y only when a rangeselector preset button moves X without an accompanying user gesture on Y — see [`.claude/rules/lis-dashboards.md`](../.claude/rules/lis-dashboards.md) for the full model and history. Same interaction, two implementations inside `exchange_rate/`: its model tabs came in with their own `_bindPlotlyYAutofit()`/`plotlyBaseLayout()`, kept as-is by the merge.
- `data/` vs `referencia/` convention: `data/` holds what the scripts actually read/write (e.g. `inflation/data/ipca_bcb_series.csv`); `referencia/` holds context nothing reads (PDFs, literature, the original BCB model spec). Same split, repo-wide since 2026-07. `economic_activity/` needs neither — everything it reads is already in MySQL, no local data files at all.
- **Since 2026-08, the boilerplate pieces of this pattern (the theme CSS, the `_bindYAutofit` JS, the substitution/write-out plumbing) live in [`report_structure/`](report_structure/CLAUDE.md) as shared build-time assets, not hand-copy-pasted per report.** `inflation/` (fully migrated) was the pilot; `exchange_rate/` is partially migrated (JS + harness, not theme CSS — needs the 2026-07 reskin first); `economic_activity/` was built directly onto both markers from the start, no migration needed — see `report_structure/CLAUDE.md`'s Migration status.

## `brasil/painel_setores/`

No dedicated `CLAUDE.md` yet. `painel_setores.py` fetches BCB/IBGE series directly (`Request_data_bcb()`, `connectors.ibge`) and feeds a Power BI file (`docs/PAINEL DE SETORES.pbix`) — no HTML report, no `/*REPORT_DATA*/` pattern, no MySQL involved. `docs/` here means "supporting Excel/Word/pbix files", a different sense of "docs" than `oraculo/docs/` below.

## `oraculo/` — two things not yet in `oraculo/CLAUDE.md`

See [`oraculo/CLAUDE.md`](oraculo/CLAUDE.md) for the module breakdown. Found while surveying this folder, not yet fixed (see Pending):

- `base/` and `docs/` both hold `Central_base.csv`/`d_table.xlsx`/`Weights.xlsx`. Only `base/` is a real package (`__init__.py`) and is what's actually produced/consumed — `docs/` is not referenced anywhere in code and hasn't been touched since the initial commit. Looks like a stale duplicate.
- `us/us/term_us.py` is an older copy of `us/term_us.py` — hardcoded to the pre-`analytics/`-migration path (`C:\...\oraculo\us\base\US_BASE.csv`) and missing the current version's `run()` entry point. Not imported anywhere.

## `brasil/monetary_policy/models/curva_juros/`

Legacy yield-curve material (`yield_curve.py`, `yield_curve_model.py`, DI/títulos/governo spreadsheets), moved here from `quarantine/` in 2026-08 and since reorganized under `guardar/dados/`. Never wired into anything, and `model.py` — the engine it was meant to join — was removed in 2026-08. Its imports (`DATABASE.MYSQL_CONECTOR`, `FUNCTIONS.func_Tratamento`) point at a package layout that no longer exists, so it cannot run as-is. See root `CLAUDE.md`'s Pendências.

## Pending

- **`analytics/brasil/credit/` (new, 2026-08)** — built, see [`credit/CLAUDE.md`](brasil/credit/CLAUDE.md) for full detail and its own Pending list (PJ/PF segment selector, the ~22 deferred BCB-workbook tabs, ICC not yet charted, real-browser confirmation).
- **Give `exchange_rate/` the 2026-07 LIS-dashboard CSS reskin, then migrate its theme onto `report_structure/theme.css`** — its JS/harness are already migrated (see `report_structure/CLAUDE.md` Migration status); only the theme CSS is left, and it needs the actual reskin first (navy header/`system-ui` font → the light Barlow theme `inflation/` already has), not a mechanical marker swap. Now doubles as cleanup for the 2026-08 PPP-dashboard merge: that report currently runs two design systems side by side, the fused-in model tabs scoped under `.ppp-scope`.
- **`oraculo/docs/` vs `oraculo/base/` duplication** — confirm `docs/` is dead and remove it, or document why both exist.
- **`oraculo/us/us/`** — looks safe to remove, superseded by `oraculo/us/term_us.py`.
- **`analytics/brasil/inflation/reservoirs.py`** — fetches ONS hydro reservoir levels (`EAR_DIARIO_RESERVATORIOS_*`), which has no obvious connection to inflation on its face. No `run()`/entry-point pattern like its sibling scripts, not imported anywhere, not mentioned in `inflation/CLAUDE.md`. Moved from `quarantine/` in this session's git history but not wired into any pipeline yet — confirm the intended destination/purpose (energy prices → administered-inflation component?) or remove.
