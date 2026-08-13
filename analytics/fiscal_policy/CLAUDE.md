# analytics/fiscal_policy/ — Panorama Fiscal

Self-contained HTML report on Brazilian fiscal data (`reports/fiscal_policy_latest.html`). Same
`/*REPORT_DATA*/` marker-substitution pattern as the other reports in `analytics/` — no Jinja2, no
build step — built on [`analytics/report_structure/`](../report_structure/CLAUDE.md) (`/*THEME_CSS*/`
and `/*Y_AUTOFIT_JS*/` markers).

## Generate the report

```powershell
uv run python -c "from analytics.fiscal_policy.generate_report import run; run()"
# Output: reports/fiscal_policy_latest.html
```

`fisc_efgg`, `atv_pib_valores_correntes`, `atv_pib_taxas`, `inflc_agregados` are all in
`jobs/update_db.py`'s routine run — no manual refresh needed.

## Current state — 3 tabs

**1. Receitas e Despesas (GFSM)** — default tab. Hierarchical table + chart (same pattern as
`analytics/credit/`'s Saldo/Concessão: checkbox to plot, ▸/▾ to expand a GFSM category into its
subcodes). Tree: Receita (Impostos + 3 other categories) and Despesa (Gasto Corrente + Investimento
Líquido, each with their own subcategories) — see `analytics/fiscal_policy/gfsm_tab.py`'s `GFSM_TREE`
for the exact codes. An **Esfera** dropdown swaps the whole tree between Governo Geral (consolidated)
/ União / Estados / Municípios (`fisc_efgg`'s `geral_`/`central_`/`estados_`/`municipios_`
namespaces — same data IEG's own esfera chart uses); row check/expand state survives the switch.
Metrics: Nível / Y-Y / T-T × Nominal / Real / % do PIB, pre-computed in
`analytics/fiscal_policy/transforms.py` (quarterly STL, see that module's docstring for the exact
Y-Y/T-T/deflate/%PIB conventions — deliberately different from `credit/transforms.py`'s monthly ones).

**2. Impulso Fiscal (IEG)** — Resende & Pires' (FGV/Tesouro, 2024) Impulso Estrutural do Gasto: fixed
multipliers (Folha 1.32 / Transferências 1.46 / Investimentos 1.66 / Outras 0.64) applied to the
year-over-year change (% of GDP, TTM-based to strip budget-execution seasonality) of 4 `fisc_efgg`
spending categories — `generate_report.py`'s `_load_ieg()`. Charts: IEG level, per-category
decomposition, IEG × PIB (selectable demand-side component), IEG por Ente Federado (União/Estados/
Municípios, sums exactly to the total). Multipliers are the paper's own published values, **not
re-estimated** for this project's data.

**3. Apêndice** — methodology notes for the two tabs above (accordion, `<details>`/`<summary>`).

**Historical, not current**: 3 earlier tabs (Visão Geral, Dívida Pública, Resultado Fiscal) plus an
older Receita e Despesa tab (RTN-based, Governo Central only) were deleted 2026-08 at the user's
request to rebuild the report tab-by-tab. Their underlying tables — `fisc_divida` (BCB SGS, DBGG/DLSP),
`fisc_nfsp` (BCB SGS, resultado primário/nominal/juros), `fisc_rtn` (Tesouro, RTN) — are untouched and
still updated by `jobs/update_db.py`; only `report.html` stopped reading them. Full detail on what
those tabs looked like is in git history, not duplicated here — see Pending for the rebuild status.

## Data map

| Tab | Tables read |
|---|---|
| Receitas e Despesas (GFSM) | `fisc_efgg` (all 27 GFSM codes × 4 esferas, 108 series), `atv_pib_valores_correntes` (%PIB denominator), `inflc_agregados.ipca` (Real deflator) |
| Impulso Fiscal | `fisc_efgg` (7 expense categories × 4 esferas), `atv_pib_valores_correntes`, `atv_pib_taxas` (PIB comparison overlay) |

Full table schemas (SGS codes, PK patterns) are in [`domain/db/CLAUDE.md`](../../domain/db/CLAUDE.md)
and each script's own docstring — not duplicated here.

## Gotchas

- **GFSM tab, Governo Geral totals only**: `Receita`/`Despesa` (root nodes) sum the three esferas
  cell-by-cell without netting intergovernmental transfers (FPE/FPM, SUS, royalties) — inflates both
  totals by ~10% of GDP vs. a proper netted consolidation (confirmed live). União/Estados/Municípios
  selected individually don't have this problem. Documented in the report's own Apêndice; not fixed
  (see Pending).
- **BCB SGS's NFSP series (`fisc_nfsp`) use the opposite sign convention** from "resultado
  primário/nominal" as normally reported — `domain/db/brasil/bcb/fisc_nfsp.py` flips sign at ingestion
  (`_FLIP_SIGN`). If a new series from this same SGS family is ever added, check for this inversion
  before trusting the sign.
- **RTN's `receita_total` (gross) is not comparable to `despesa_total`** — use `receita_liquida`
  (already net of revenue-sharing transfers to states/municipalities). `receita_total` reconciles to
  nothing when compared directly to `despesa_total`.
- **DBGG and DLSP are not directly comparable** — DBGG excludes Banco Central and state enterprises,
  DLSP includes them. Don't "reconcile" the two into one number.
- **No SICONFI/subnational data** — this report never had individual states'/municipalities' own
  revenue/expenditure line items, only Governo Central (RTN) and BCB SGS aggregates plus (now) GFSM by
  esfera. Would need SICONFI's RREO/RGF API, a materially different integration.
- **Actual browser rendering has not been visually confirmed** for any tab — verification here is a
  live DB run + a Node stub-`document`/`Plotly` harness against the real generated `<script>`, no real
  browser available in this sandbox.

## Pending

- **Rebuild the 3 deleted tabs (Visão Geral, Dívida Pública, Resultado Fiscal)** — not started, no
  design decided. Whether a Central-scope/RTN-based Receita e Despesa view is still wanted alongside
  the new GFSM tab is an open question, not settled.
- **Fix the GFSM Governo-Geral double-count** (see Gotchas) — needs `fisc_efgg.py`'s `_build_geral()`
  to net out intergovernmental transfers before summing; a dedicated reconciliation project, not a
  one-line fix.
- **Revenue-side fiscal-impulse multiplier — methodology undecided.** Data (`receita_*`, 44 series ×
  4 esferas) is ingested and charted in the GFSM tab, but there's no reliable multiplier to weight a
  revenue change into a combined fiscal-impulse index (the IEG paper itself excludes revenue —
  multipliers disagree even in sign across studies, endogeneity with the business cycle). Three options
  on the table, none chosen: borrow a published estimate, estimate our own (SVAR + narrative
  identification), or show revenue change as context only with no multiplier. See
  `analytics/fiscal_policy/reference/` for the underlying literature review.
- **IEG multiplier re-estimation** — deferred, not started. Current multipliers are Resende & Pires'
  own VAR estimate (sample 2010T1–2023T4); re-estimating against this project's own data would need its
  own VAR fit, no design decided.
- **MEFA** (Monitor de Expansão Fiscal Ampliada) — blocked on data sourcing (no live restos-a-pagar
  endpoint found as of 2026-08-06); re-verify live before trusting that verdict, since a prior "blocked"
  call on IEG turned out to be wrong.
- **Not integrated into `analytics/oraculo/`'s macro thermometer.**
- Open the report in an actual browser and confirm interactions feel right (see Gotchas).
