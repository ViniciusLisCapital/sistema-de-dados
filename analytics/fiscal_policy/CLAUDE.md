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

`fisc_efgg`, `fisc_rtn`, `atv_pib_valores_correntes`, `atv_pib_taxas`, `atv_pib_mensal`,
`inflc_agregados` are all in `jobs/update_db.py`'s routine run — no manual refresh needed.

## Current state — 3 tabs

**1. Receitas e Despesas** — default tab, **two independent hierarchical table+chart pairs, one per
methodology** (do not reconcile with each other by design — see the Apêndice's "GFSM vs. RTN — Duas
Metodologias" note).

- **GFSM** (`gfsm_tab.py`): same interaction pattern as `analytics/credit/`'s Saldo/Concessão —
  checkbox to plot, ▸/▾ to expand a GFSM category into its subcodes. Tree: Receita/Despesa by
  economic nature (GFSM 2014). An **Esfera** dropdown swaps the whole tree between Governo Geral
  (consolidated)/União/Estados/Municípios (`fisc_efgg`'s `geral_`/`central_`/`estados_`/`municipios_`
  namespaces); row check/expand state survives the switch.
- **RTN** (`rtn_tab.py`): same mechanics, Governo Central only, classified by rubrica orçamentária
  (benefícios previdenciários, pessoal, discricionárias por função, etc.), monthly. Tree (restructured
  2026-08, at user request) has 3 root nodes: **Receita Líquida** (→ Receita Total [with its own
  RFB/RGPS/incentivos/não-administradas children] + Transferências por Repartição), **Despesa Total**
  (→ benefícios previdenciários/pessoal/outras obrigatórias/discricionárias, unchanged), and
  **Resultado Primário** (`resultado_primario_governo_central`, 2026-08, STN code 8055 — confirmed
  identical to `receita_liquida − despesa_total`). Default checked series: `receita_liquida` +
  `despesa_total` + `resultado_primario_governo_central` (not `receita_total` — see Gotchas).
- **3 independent metric axes (reorganized 2026-08, at user request — replaces the old "Nível/Y-Y/T-T
  (or M/M) × Nominal/Real/%PIB × Bruto/(Trimestral/)Acumulado" framing)**, all pre-computed in Python
  (`analytics/fiscal_policy/transforms.py`) and switched client-side via `<select>` dropdowns (converted
  from pill-buttons 2026-08, at user request — "click drop" for each axis; same forcing/disabling logic,
  now via `<option disabled>` instead of a `.pill.disabled` class, see `makeHierTab()`'s `wireControls()`),
  none replacing another:
  - **(a) Nível — aggregation frequency**: GFSM offers **Trimestral** (native quarterly value,
    `compute_variants()`) / **Acumulado 12m** (`compute_variants_ttm()`, 4-quarter rolling sum); RTN
    additionally offers **Mensal** (native monthly value, via
    `analytics.credit.transforms.compute_variants()`) alongside its own **Trimestral**
    (`compute_variants_quarterly_step()`, calendar-quarter sum, NOT rolling — the same non-overlapping
    3-month cut GFSM uses natively, added so the two tables compare quarter-to-quarter, see Gotchas
    "double-check 1T/2026") and **Acumulado 12m** (`compute_variants_monthly_ttm()`, 12-month rolling
    sum). A series' own native frequency caps which options exist — you can reduce frequency (RTN
    monthly → quarterly/12m) but never invent a higher one (GFSM has no Mensal). Internal dict keys
    unchanged from before the relabeling: GFSM `{"bruto": ..., "acum": ...}`, RTN `{"bruto": ...,
    "trimestral": ..., "acum": ...}` (`"bruto"` = Mensal/Trimestral-native, just relabeled in the UI).
    **RTN Trimestral display (fixed 2026-08)**: the underlying `quarterly_step_level()` still repeats
    each quarter's value across its 3 calendar months (needed so the Y/Y=12/T-T=3-month `pct_change()`
    lags stay correct) — but `report.html`'s `makeHierTab()` now collapses the DISPLAYED dates/values
    down to one column per quarter (first month only, e.g. Jul/25 — "like GFSM"), via
    `collapseToQuarterStart()` + `opts.quarterlyStepAccum: 'trimestral'` (RTN_TAB only). Before this fix
    the table showed the same quarterly figure 3× in a row (Jul/25, Ago/25, Set/25 all identical) —
    user-reported (screenshot), verified against an independent manual quarterly sum via a Node harness
    (see Gotchas).
  - **(b) Nominal ou Real** — whether the Nível value is IPCA-deflated. Orthogonal to (a) and (c).
  - **(c) Modelagem**: **Nível** (raw value, no transform), **Y/Y** (same period last year), **Marginal**
    (immediately preceding period — resolves in JS to the underlying `mom_sa` key at Nível=Mensal or
    `qoq_sa` at Nível=Trimestral; **disabled entirely at Nível=Acumulado 12m**, where the only
    comparison offered is Y/Y — a "Marginal" of the accumulated base would measure the acumulado's own
    acceleration, not the trimestre-vs-trimestre reading the label implies, deliberately not offered to
    avoid conflating the two), or **% PIB** (nominal only — forces Nominal/disables Real in the UI when
    selected). **% PIB's own denominator now depends on Nível** (2026-08 change, was always TTM/TTM
    before): at Mensal/Trimestral, it's the *same-period* GDP, no accumulation on either side
    (`compute_pct_pib_same_period()` — RTN denominator `atv_pib_mensal.pib_mensal`, SGS 4380, raw
    monthly, vs. the already-used `pib_acum_12m`/SGS 4382 for Acumulado; GFSM denominator
    `atv_pib_valores_correntes.pib_pm` raw quarterly, vs. the rolled `pib_4t` for Acumulado); at
    Acumulado 12m, still TTM/TTM (`compute_pct_pib_ttm()`, unchanged, matching `fisc_nfsp`/IEG's own
    convention elsewhere in this report — user confirmed keeping this at Acumulado 12m rather than
    dropping %PIB there entirely). See Gotchas for the `incentivos_fiscais` sign/outlier quirk, more
    visible under Acumulado.
  - **Open question, not yet decided** (user asked this be recorded): should % PIB, when Real is
    selected, divide by a *real* GDP instead of nominal? For now % PIB is nominal-only regardless of
    the Nominal/Real toggle (deflator would cancel if it did divide by real GDP, so today's nominal-only
    answer is already numerically equivalent to "real ÷ real" — the open question is only whether a
    distinct real-GDP-denominator framing is ever worth exposing, not a live bug).

**2. Impulso Fiscal (IEG)** — Resende & Pires' (FGV/Tesouro, 2024) Impulso Estrutural do Gasto: fixed
multipliers (Folha 1.32 / Transferências 1.46 / Investimentos 1.66 / Outras 0.64) applied to the
change (% of GDP) of 4 `fisc_efgg` spending categories — `generate_report.py`'s `_load_ieg()` /
`_ieg_contrib_for_esfera()`. Two variants per category, `{"acum4t": ..., "quarter": ...}` (see "Quarter
(T/T) methodology" below) — no standalone IEG chart anymore, only through "Visão Combinada" and "IEG por
Esfera e Categoria" below (the old standalone "IEG" line chart and "IEG × PIB" comparison chart were
**removed 2026-08** at user request, redundant with those two). Multipliers are the paper's own
published values, **not re-estimated** for this project's data.

**Visão Combinada** — single chart at the TOP of the tab overlaying the tab's three metrics: IEG (total),
Impulso via Resultado Primário (total, see below), and GDP — switchable via one "Comparação" dropdown
(`impulso-combinado-view-select`) between **4T/12m Acumulado (Y/Y)** and **Trimestre (T/T)** (see below —
genuinely seasonally-adjusted since 2026-08, not a shortcut). GDP is always a **real** rate (IBGE
publishes these over the volume index): `acum_4t` (indicador 6563) under Acumulado — **changed 2026-08
from `yoy`, at user request**, so all three lines compare an annual window against the previous annual
window rather than mixing a point-to-point quarter comparison into a chart of accumulated ones — and
`qoq` (already SA at source) under Trimestre. `yoy` is still loaded but no longer plotted here. IEG/PB
impulse share the left y-axis (same p.p. unit); GDP gets its own right-hand `yaxis2` — `_bindYAutofit`
(`analytics/report_structure/y_autofit.js`) already groups by each trace's own `t.yaxis` generically, so
this dual-axis chart needed no changes to the shared autofit helper.

**Quarter (T/T) methodology (2026-08, rewritten a second time)** — first version (see git history) used
a T/T-on-TTM shortcut (a lag-1/lag-3 diff on the already-accumulated series, no STL) for both IEG and
the PB impulse, chosen to avoid new data ingestion. User later rejected this after seeing the combined
chart ("the metrics [aren't] talking to each other") and asked for genuine seasonal adjustment on both,
since the underlying data (`fisc_efgg`'s native quarterly cadence; BCB's *monthly* primary-result flow)
supports it. Current implementation:
  - **IEG**: `_ieg_contrib_for_esfera()` computes each category's RAW (non-accumulated) quarterly %GDP
    (`pib_pm`, not the rolled `pib_4t`), runs `transforms.stl_seasonal_adjust(period=4)`, then
    `.diff(1)*mult` on the seasonally-adjusted series — `_stl_on_valid_window()` fits STL only over that
    category's own dense (non-NaN) date range, never a `.reindex()`-padded one (see Gotchas — this was a
    real bug found live, not a style choice).
  - **PB impulse**: `fisc_nfsp` only ever stored the 12m-accumulated %GDP series — 6 new BCB SGS codes
    (raw monthly flow, R$ mi, `resultado_primario_fluxo_mensal` + 5 esfera counterparts) were added to
    `domain/db/brasil/bcb/fisc_nfsp.py` and backfilled (`run(start="all")`), confirmed live both by
    catalog search AND numeric reconciliation (rolling-12m-sum of the new flow ÷ 12m GDP matches the
    existing `*_pct_pib_12m` columns to <0.01pp) and by an identity check (coarse 3-way codes = sum of
    the finer esfera codes, same pattern as the existing accumulated series). `_impulso_quarter_via_stl()`
    (`generate_report.py`) takes a rolling 3-month sum of flow and of GDP first (raw monthly flow is too
    noisy — one-off payments can swing a single month by R$100bn+ — a naive month-to-month STL diff
    produced implausible ±7pp swings before this smoothing was added), divides, STL-adjusts
    (`period=12`), then `pp_diff(3)`.
  - GDP's own "quarter" reading is unchanged — `atv_pib_taxas`'s official `qoq` indicador (already
    seasonally adjusted by IBGE).
  - **Seasonal factors are frozen at the last complete calendar year (2026-08, user request)** —
    `transforms.stl_seasonal_adjust()` fits STL only on the sample ending at the last year that has all
    `period` observations (`seasonal_cutoff_year()`), and extrapolates into the incomplete current year
    by carrying that year's fitted factor forward per season position. In-sample dates keep STL's own
    local (evolving) factor; only the extrapolation is frozen. Re-run once the year closes. This
    diverges on purpose from `analytics/credit/transforms.py`, which freezes the whole-sample *mean*
    per month — here the seasonal pattern trends strongly (PB flow: Jan factor 2.22 in 2021 → 3.80 in
    2025, ~8pp amplitude), so a whole-sample or 3-year mean lags it by up to ~0.7pp. Effect on the
    published numbers: negligible over history (median shift 0.04pp IEG / 0.01pp PB impulse) but
    material at the recent end (median ~0.9pp / ~0.3pp since 2024, up to ~2pp at the latest
    observation) — which is exactly the region the old full-sample fit was contaminating with the
    half-finished current year. Applies to the GFSM/RTN tabs' "Marginal" modelagem too (same helper).

**Reconciliation changed by this rework — read before trusting cross-sums under "Trimestre"**: the
**4T/12m Acumulado** variant is unaffected and still reconciles exactly (linear TTM diffs) — category
sums to esfera total, esfera sums to the consolidated total, all within SGS/JSON rounding. The
**Trimestre** variant does NOT carry the same guarantee across independent STL fits: within one esfera,
category-sum-to-total is still exact (the total is *defined* as that Python sum, not independently
fit); but **cross-esfera** sums are not — IEG's União+Estados+Municípios vs. Geral, and the PB impulse's
5-esfera sum vs. the consolidated total, can diverge by a median of ~0.2pp and up to ~1-2pp in some
quarters (STL is not a linear operator). Documented in both report captions and the Apêndice, not
treated as a bug — see Gotchas.

**Both decomposition sections below share one JS factory, `makeImpulsoHierTab()`** (2026-08, replaced
the old `makeIegHierTab()` + chart-only PB section). Table with checkbox-to-plot and ▸/▾ expand, one
**Nível** dropdown, chart = `renderRelativeBarWithLine()` (every checked row is a `barmode:'relative'`
bar; a fixed total line on top, independent of what's checked). **Deliberately does NOT reuse
`makeHierTab()`** — that function's Nominal/Real/%PIB axes don't fit already-weighted p.p.
contributions. Checking a parent *and* its children double-stacks the same value; that's the reader's
call, not blocked.

**IEG por Esfera e Categoria** — tree is **Esfera › Categoria de despesa** (2026-08, restructured at
user request — "the hierarchy should be: Sphere > Expenditure categories… maintain just the 'Nível'
click-dropdown"): 4 esfera roots (Geral/União/Estados/Municípios), each expanding into the 4 spending
categories. The **Esfera dropdown is gone** — the esfera became the tree's first level. Fixed line =
IEG Governo Geral; default checked = União+Estados+Municípios (they stack exactly onto it under 4T
Acumulado). `_load_ieg()`'s payload: `{dates, ieg, ieg_quarter, tree, series}` — `series` is keyed by
**both** the bare esfera (`"geral"`, the parent's own total) and `"{esfera}__{categoria}"` (the
children), 20 keys total; the separate `esfera_total` dict was folded into `series` so both tree levels
resolve through one `seriesKey`. **No Banco Central esfera here** (unlike the PB impulse below) —
`fisc_efgg`/EFGG only covers Governo Geral/Central/Estados/Municípios.

**Impulso via Resultado Primário por Esfera** — same table+chart, but a **flat sphere list, no second
level** ("the same… but only with the spheres") — the BCB publishes no expenditure-category cut inside
each sphere. `fisc_nfsp`'s 5 esfera series (governo_federal excl. Banco Central/banco_central/estados/
municipios/empresas_estatais, both the `*_pct_pib_12m` accumulated codes and the `*_fluxo_mensal` raw
codes) feed it via `_load_fiscal_impulse_nfsp()`'s `tree` + `esfera` payload; fixed line = the
consolidated-public-sector total. Nível toggles **Acum. 12m (Y/Y)** (exact reconciliation) and
**Trimestre (T/T)** (independent per-esfera STL, see reconciliation note above). Banco Central's own
contribution is consistently ~0 (confirmed live), included anyway for completeness — uncheck it in the
table to drop it.

**3. Apêndice** — methodology notes for the two tabs above (accordion, `<details>`/`<summary>`).

**Historical, not current**: 3 earlier tabs (Visão Geral, Dívida Pública, Resultado Fiscal) were
deleted 2026-08 at the user's request to rebuild the report tab-by-tab; a separate, older RTN-based
Receita e Despesa tab was also deleted then and has since been reintroduced in a new form (`rtn_tab.py`,
above). `fisc_divida` (BCB SGS, DBGG/DLSP) is still untouched by `report.html` — updated by
`jobs/update_db.py` but not read here. `fisc_nfsp` now has 16 series total (10 `*_pct_pib_12m` +
6 `*_fluxo_mensal`, see above) — `resultado_nominal_pct_pib_12m`/`juros_nominais_pct_pib_12m` remain
unused by this report. Full detail on what the 3 still-deleted tabs looked like is in git history, not
duplicated here — see Pending.

## Excel audit workbook

`export_audit_excel.py` (`uv run python -c "from analytics.fiscal_policy.export_audit_excel import run; run()"`
→ `reports/fiscal_policy_audit.xlsx`) — original/adjusted series + every intermediate step of both
impulse metrics (IEG × 4 esferas × 4 categorias; PB impulso × 5 esferas + total), one sheet per
variant (Acumulado/Trimestre, both metrics) plus a Reconciliação sheet. Every pure-arithmetic step
(accumulation, %PIB ratio, diff, sign flip) is a **live Excel formula**, not a pasted number — only
the STL output itself is pasted (yellow-filled), since a LOESS decomposition isn't reproducible as a
native Excel formula. Deliberately duplicates `generate_report.py`'s computation (not imported wholesale)
so every intermediate has its own column instead of collapsing to the final result — but reuses the
same `transforms.py` primitives and `_stl_on_valid_window()`, and was verified cell-for-cell against
`_load_ieg()`/`_load_fiscal_impulse_nfsp()`'s actual output before shipping. Two rules the script must
keep:
- **Fit STL on each series' own native date window before aligning to the shared display grid** — same
  rule as the Gotchas entry above; aligning first would reintroduce that exact bug in the audit script
  itself. Go through `_stl_on_valid_window()` rather than `tf.stl_seasonal_adjust()` directly, or the
  leading NaNs of a rolling window get backfilled into the fit and the workbook stops matching the
  report.
- **A sheet's date grid must start early enough for its own lookback formulas to resolve.** The `PB
  Impulso - Trimestre (STL)` sheet deliberately runs on a *longer* grid than its Acum. 12m sibling (the
  union of the 6 monthly-flow series, 1998→, not `resultado_primario_pct_pib_12m`'s 2002-11→): its
  `SUM(...)`/`Δ3m` formulas look backwards **within the sheet**, so on the shorter grid the first 3
  rows came out blank even though the report publishes values there. An audit that can't reproduce the
  first published values isn't an audit.

## Data map

| Tab | Tables read |
|---|---|
| Receitas e Despesas — GFSM | `fisc_efgg` (all 27 GFSM codes × 4 esferas, 108 series), `atv_pib_valores_correntes.pib_pm` (%PIB denominator — raw quarterly for Nível=Trimestral, `rolling(4)` TTM for Nível=Acumulado 12m, see `_load_pib_4t()`/`_load_pib_pm_raw()`), `inflc_agregados.ipca` (Real deflator) |
| Receitas e Despesas — RTN | `fisc_rtn` (34 codes, Governo Central), `atv_pib_mensal` (both `pib_mensal`/SGS 4380 — raw monthly, %PIB denominator at Nível=Mensal/Trimestral — and `pib_acum_12m`/SGS 4382 — TTM, %PIB denominator at Nível=Acumulado 12m), `inflc_agregados.ipca` (Real deflator) |
| Impulso Fiscal — IEG | `fisc_efgg` (4 expense categories × 4 esferas), `atv_pib_valores_correntes` (`pib_pm` — both raw quarterly, for STL, and rolled TTM, for Acumulado), `atv_pib_taxas` (`acum_4t`+`qoq` indicadores — Visão Combinada; `yoy` loaded but unplotted) |
| Impulso Fiscal — via Resultado Primário (NFSP) | `fisc_nfsp` (`resultado_primario_pct_pib_12m` + 5 esfera `*_pct_pib_12m` — Acum. 12m; `resultado_primario_fluxo_mensal` + 5 esfera `*_fluxo_mensal` — Trimestre/STL), `atv_pib_mensal.pib_mensal` (raw monthly GDP, STL denominator) |
| Impulso Fiscal — Visão Combinada | Reads already-loaded `ieg`/`fiscal_impulse_nfsp`/`pib_yoy` payloads, no new table |

Full table schemas (SGS codes, PK patterns) are in [`domain/db/CLAUDE.md`](../../domain/db/CLAUDE.md)
and each script's own docstring — not duplicated here.

## Gotchas

- **NFSP impulse vs. RTN Resultado Primário — different series, don't cross-check directly** (found
  2026-08, real user confusion, not a bug): the Impulso Fiscal tab's "Impulso via Resultado Primário"
  uses `fisc_nfsp` (BCB, setor público consolidado). The RTN tab's own "Resultado Primário" row
  (`resultado_primario_governo_central`, %PIB Acum. 12m) is a DIFFERENT series (Governo Central only).
  Live-verified both are internally correct for the same month: RTN showed +0,11%→−1,08% (Jun/2025→
  Jun/2026, delta −1,19pp), NFSP showed +0,15%→−1,19% (same months, delta −1,34pp, impulso +1,34%) — a
  user read the RTN figure expecting it to explain the NFSP impulse number and got a mismatch that
  looked like a calc bug but wasn't. Both captions (section + Apêndice) now spell this out explicitly
  with the verified numbers — if this confusion recurs, the fix is clearer UI copy, not the formula.
- **GFSM tab, Governo Geral totals only**: `Receita`/`Despesa` (root nodes) sum the three esferas
  cell-by-cell without netting intergovernmental transfers (FPE/FPM, SUS, royalties) — inflates
  **both** totals (confirmed live: transfers ≈ R$1.36tri over the last 4 quarters, ~10% of GDP) by
  the same mechanism on both sides of the ledger (a transfer is simultaneously the paying sphere's
  expense and the receiving sphere's revenue — summing all 3 spheres without netting double-counts it
  on whichever side you're reading) vs. a proper netted consolidation. União/Estados/Municípios
  selected individually don't have this problem. Documented in the report's own Apêndice; not fixed
  (see Pending).
- **GFSM "Governo Geral" (default Esfera) vs. RTN "Governo Central" is NOT scope-comparable — this is
  the single biggest source of "these two tables don't add up" confusion** (confirmed live, 2026-08,
  after a user-reported ~800bi RTN vs. ~1.7tri GFSM gap for 1T/2026 Receita, ~53% of quarterly GDP).
  Two causes stack: (1) GFSM's default view is **Geral** (all 3 government levels combined), while
  RTN only ever covers **Governo Central** — comparing Geral against Central compares scopes of very
  different size by design; (2) Geral is further inflated by the intergovernmental-transfer
  double-count above. Controlling for scope (GFSM **União**, not Geral, vs. RTN) narrows the gap from
  ~2.2x to ~18% (1T/2026: GFSM União receita_total = R$918.6bi vs. RTN receita_total = R$776.1bi) — a
  residual attributable to source/classification differences (SIAFI+Siconfi consolidated by STN,
  GFSM 2014 classification, vs. Tesouro's own Série Temporais by rubrica orçamentária) not
  investigated further. **Always switch GFSM's Esfera to União (never leave it on Geral) and use
  RTN's Trimestral toggle (see above) before comparing any value between the two tables** — spelled
  out with the full numbers in the report's own Apêndice.
- **BCB SGS's NFSP series (`fisc_nfsp`) use the opposite sign convention** from "resultado
  primário/nominal" as normally reported — `domain/db/brasil/bcb/fisc_nfsp.py` flips sign at ingestion
  (`_FLIP_SIGN`). If a new series from this same SGS family is ever added, check for this inversion
  before trusting the sign.
- **`fisc_rtn.incentivos_fiscais` (RTN 10.01.1.2) is a deduction, not a revenue** — measures tax
  revenue foregone under LRF art. 14 (isenções/anistias/remissões/créditos presumidos), so it's
  structurally ≤ 0, unlike its 3 sibling children of `receita_total`. Confirmed live over the full
  series (1997-01→2026-06, 354 obs): 98 negative, 254 exactly zero, only 2 positive (rounding-scale).
  From 2024-01 onward it's zero every month (one exception, -R$1.4mi in 2025-12) — effectively dead
  for ~2.5 years, cause unconfirmed. Also has an isolated outlier at 2017-12 (-R$1,356mi, ~9x any
  other month) — likely a year-end catch-up entry. Under the **Acumulado** toggle (see above) that
  single-month outlier smears across the following 12 months of the accumulated series instead of
  appearing as one isolated spike (under **Bruto**, the default, it's an isolated single-month value
  as normal). **Found 2026-08, not fixed (pre-existing, out of scope of the session that found it):**
  because this series has been exactly 0 every month since 2024-01, `incentivos_fiscais`'s **Y/Y**
  under Nível=Mensal/Trimestral divides by that zero base for every date from ~2025-01 onward,
  producing `Infinity`/`-Infinity` (pandas' `pct_change()`, used by
  `analytics.credit.transforms.compute_variants()`, doesn't guard a zero denominator) — renders
  literally as "Infinity%" in the table/chart if a user expands to this row and selects Y/Y. No
  exception is thrown (`json.dumps` emits bare `Infinity`, which is valid as a JS literal but not
  strict JSON — only surfaces if something tries to `JSON.parse` the report's data blob). Same root
  cause likely affects any other series that ever hits an exact zero and is later compared Y/Y/M-M/T-T
  against it — not audited across the rest of this report or `analytics/credit/`, which shares the
  same `pct_change()`. Fix would be a `pct_change()`/`stl_seasonal_adjust()`-adjacent guard (return
  `None` instead of inf when the denominator is 0) in `analytics/credit/transforms.py`, shared by
  other reports — needs its own scoped pass, not a one-line patch here.
- **RTN's `receita_total` (gross) is not comparable to `despesa_total`** — use `receita_liquida`
  (already net of revenue-sharing transfers to states/municipalities). `receita_total` reconciles to
  nothing when compared directly to `despesa_total`. This is why the RTN tab's chart defaults to
  `receita_liquida`, not `receita_total`.
- **GFSM and RTN's %PIB figures for the "same" category don't converge, and shouldn't** — at Nível=
  Acumulado 12m both use the same TTM/TTM annualization convention (confirmed live, 2026-06: Despesa
  Total RTN [Governo Central] ≈ 20% of GDP vs. GFSM's União Despesa Total ≈ 33-35% of GDP for the same
  period), but the underlying scope differs: GFSM classifies constitutional transfers to states/
  municipalities (FPM/FPE/IPI-EE) as an *expense* of the paying sphere (GFSM code 26); RTN nets the
  same transfers out on the *revenue* side instead (`receita_liquida`) — a real, expected gap from
  classification, not a bug. Don't try to reconcile GFSM and RTN line items against each other, at any
  Nível.
- **%PIB is no longer always TTM/TTM (2026-08 change)** — it now follows whichever Nível is selected:
  same-period (no accumulation either side) at Mensal/Trimestral, TTM/TTM only at Acumulado 12m. A
  %PIB value read off the Trimestral toggle will look different in scale from the same series' %PIB
  under Acumulado 12m — that's by design (matches "PIB do mesmo período" as the user specified), not
  a bug; don't average or compare %PIB values across different Nível selections.
- **DBGG and DLSP are not directly comparable** — DBGG excludes Banco Central and state enterprises,
  DLSP includes them. Don't "reconcile" the two into one number.
- **No SICONFI/subnational data** — this report never had individual states'/municipalities' own
  revenue/expenditure line items, only Governo Central (RTN) and BCB SGS aggregates plus (now) GFSM by
  esfera. Would need SICONFI's RREO/RGF API, a materially different integration. This is also the
  reason RTN's own "Receitas e Despesas" table has no Esfera selector (a user asked why, 2026-08,
  after seeing GFSM's Esfera dropdown right above it in the same tab) — RTN **is** the Tesouro's own
  budget-execution report, so it structurally only ever covers Governo Central; there's no
  Estados/Municípios cut to add without a different data source entirely. GFSM already has the
  esfera cut for revenue/expenditure (via `fisc_efgg`) — the report's own RTN section caption now
  says this explicitly and points back to the GFSM selector, instead of leaving it unexplained.
- **Fitting STL on a `.reindex()`-padded series silently distorts the result far past the padded
  region — found and fixed live, 2026-08.** `_ieg_contrib_for_esfera()` originally reindexed every
  esfera's raw category series onto the full shared date grid (`idx`, 2006+) *before* running STL.
  `central_` has real data back to 2006, but `geral_`/`estados_`/`municipios_` only exist from 2010 —
  reindexing gave the latter 3 an artificial ~16-quarter leading NaN block, which
  `stl_seasonal_adjust()`'s `interpolate(limit_direction="both")` backfills with the first real 2010
  value. That flat, artificial prefix skews STL's trend/seasonal fit over the *entire* series, not just
  near the padding — confirmed live: before the fix, União+Estados+Municípios came out ~4-5x different
  from Geral in some quarters (e.g. 2025-Q3: 0.40 vs. 1.85), not the small residual expected from STL's
  non-linearity alone. Fixed by `_stl_on_valid_window()` — dropna() and fit STL only over each series'
  own dense range, reindex back to the full grid only after. If a similar per-esfera/per-cut STL is
  ever added elsewhere in this project, replicate this pattern, not the reindex-first one.
- **A Plotly trace with `x`/`y` undefined renders as nothing, silently — found 2026-08, had been
  shipping broken.** `impulsoRPEsfera()` returned `D.fiscal_impulse_nfsp.esfera[key][variant]`, which is
  a **bare value array** (all esferas share the payload's top-level `dates`), while the caller read
  `.dates`/`.values` off it — so all 5 esfera bars of "Impulso via Resultado Primário por Esfera" were
  drawn with `x: undefined, y: undefined` and only the total line (which came from a correctly-shaped
  `impulsoRPTotal()`) appeared. Plotly throws nothing for this. It survived a full round of
  verification because the reconciliation checks ran against the **Python payload**, never against the
  traces the chart actually receives — the v5 Node harness now asserts on `Plotly.react`'s captured
  trace objects (count, names, and that the bars stack onto the line) precisely to close that gap.
  Whenever a payload stores parallel arrays against one shared date axis, re-wrap to `{dates, values}`
  at the accessor, and assert on traces, not on the payload.
- **Chart CSS sizing bug — found live, 2026-08**: `#chart-impulso-rp` (now removed) and
  `#chart-impulso-rp-esfera` were missing from the CSS selector list that gives chart divs an explicit
  `width`/`height` (`.chart-card #chart-* { width: 100%; height: 560px; }`) — a `<div>` with no CSS
  sizing collapses to near-zero width, which is likely why the user described the esfera chart as
  "not by sphere" (bars rendered too narrow to read, not a data/methodology bug). Whenever a new
  `chart-*` div is added to this report, it MUST be added to that same selector list or it silently
  renders broken.
- **Actual browser rendering has not been visually confirmed** for any tab — verification here is a
  live DB run + a Node stub-`document`/`Plotly` harness against the real generated `<script>`, no real
  browser available in this sandbox.

## Pending

- **Guard `pct_change()` (`analytics/credit/transforms.py`) against a zero denominator** — see
  Gotchas' `incentivos_fiscais` entry for the concrete failure (`Infinity%` in the RTN table when
  Y/Y divides by that series' now-permanently-zero 12-months-ago base). Shared code, used by other
  reports too — needs its own scoped pass across callers, not a one-line fix here.
- **Rebuild the 3 deleted tabs (Visão Geral, Dívida Pública, Resultado Fiscal)** — not started, no
  design decided (`fisc_divida`/`fisc_nfsp` still unused by this report).
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
