# Metric layers — what THIS repo decided, and where the code is

**The taxonomy is not here.** What the metric layers are, in what order they compose, what decides
each one's options, and what to disable with which reason on screen all live in the
`lis-dashboard` skill:
[`design-system.md#metricas`](../../.claude/skills/lis-dashboard/references/design-system.md#metricas).
Read that **before** adding a metric selector to a new tab. It is general — it serves a macro report
and an ad-hoc CSV of positions alike — and it is the only copy.

This file holds what a skill cannot: the **register** of conventions this project settled (and the
ones still open), the **inventory** of which function to call and what each report offers today, and
the **measurements** behind the guards. Nothing here restates the taxonomy; if you find yourself
copying a rule from the skill into this file, that is the drift the split exists to prevent.

Companion files: [`seasonal_adjustment.md`](seasonal_adjustment.md) covers *which* adjustment method
(STL vs. X-13) and its scope; [`.claude/rules/lis-dashboards.md`](../../.claude/rules/lis-dashboards.md)
covers chart interaction (pan/zoom/quick-range); [`report_structure/CLAUDE.md`](../report_structure/CLAUDE.md)
covers the build-time scaffolding.

---

## The deflator (layer 1 — BASE)

- `inflc_agregados.ipca` (monthly %) → `build_price_index()` chains it into an index →
  `deflate_series()` rebases to `ref_date`. The index's base month is arbitrary; only ratios between
  two dates are used.
- **The reference date is the last available IPCA month** — constant reais of the most recent month,
  so the newest observation equals its own nominal value. Every call site computes it the same way
  (`ref_date = ipca_pct["dates"][-1]`) and ships it in the payload as `ref_date` for the report's own
  axis labels.
- **Which tabs deliberately have no Nominal/Real axis at all**: Taxa & Spread and Inadimplência in
  `credit/` — every series there is already a percentage. Never deflate `% PIB`, PNAD's `taxa_*`, or a
  series the source already publishes in real terms (`rend_*_real`).
- **`% PIB` needs no real counterpart** — the deflator cancels in the ratio, so real ÷ real GDP equals
  nominal ÷ nominal GDP. Selecting `% PIB` forces Nominal and disables Real, which `makeHierTab()`
  already does. Whether a distinct real-GDP-denominator framing is worth *exposing* is open question 2
  below.

---

## Seasonal adjustment (layer 2) — two conventions, both live

They must be labeled distinctly rather than merged into one selector:

| Convention | Definition | Where |
|---|---|---|
| **Rolling 3M/3M momentum** | `pct_change(sa, 3)` on the SA monthly level — month *t* vs. *t−3* | `credit/` (Saldo, Concessão), `atv_pim`/`atv_pim_uso` |
| **Calendar T/T** | Quarter vs. the immediately preceding calendar quarter, on an SA quarterly series | GFSM (native quarterly, STL `period=4`) |

Which STL freezing convention applies (whole-sample mean per month vs. last-complete-year factors
carried forward) is in [`seasonal_adjustment.md`](seasonal_adjustment.md); the divergence between
`credit/` and `fiscal_policy/` is in
[`fiscal_policy/CLAUDE.md`](../brasil/fiscal_policy/CLAUDE.md). Both fit only through the last
complete calendar year — never over a half-finished current year.

### SA on an already-aggregated level

- **Rolling 12m**: no SA, and none needed — a 12-month window spans every season. But the marginal
  reading changes meaning: the change in a 12-month accumulation measures the **acceleration of the
  window**, not this month against last month. Two reports resolve that differently on purpose — RTN
  disables Marginal at Acum. 12m; Investimento offers it with the acceleration reading spelled out in
  the caption and Apêndice. **Don't unify them without asking.**
- **Closed calendar quarter built from monthly data** *does* need SA at `period=4` (Q4 fiscal spending
  is systematically higher than Q1). Implemented 2026-08 as an opt-in:
  `compute_variants_quarterly_step(seasonal=True)` routes `qoq_sa` through `quarterly_step_qoq_sa()`;
  with the default `seasonal=False` it stays a bare `pct_change(step, 3)` and the `_sa` suffix remains
  just a JS-compatibility key name. **Investimento opts in; RTN deliberately does not** (user choice,
  2026-08 — closing the gap for the new tab without moving RTN's already-published numbers). A new tab
  adding a marginal comparison on a calendar-aggregated series should pass `seasonal=True`.
  - **Run the STL on the collapsed quarterly series, never on the monthly step.** The step repeats each
    quarter's value across its three months, so `period=4` over that array treats four consecutive
    *months* as one cycle and fits a seasonality that does not exist. `quarterly_step_qoq_sa()`
    collapses to one observation per quarter, fits `period=4` there, takes `pct_change(sa, 1)`, and
    re-expands onto the monthly grid for `collapseToQuarterStart()` to reduce again at display time.

---

## Windows (layer 3) — which primitive, and the two landmines

| Window | Primitive | Used by |
|---|---|---|
| Rolling | `rolling_sum(values, window)` | Acum. 12m everywhere; `compute_variants_ttm` (4Q), `compute_variants_monthly_ttm` (12M) |
| Closed calendar | `quarterly_step_level(dates, values)` | RTN/Investimento `Trimestral` |
| YTD | `ytd_sum(dates, values)` | Investimento `Acum. no ano`, CAGED `Acum. no ano` |

- **The quarterly step must be collapsed at display time.** `quarterly_step_level()` repeats the
  quarter's value across its three months so the `pct_change` lags (12 for Y/Y, 3 for T/T) stay
  arithmetically correct on a monthly index — the display then reduces it with
  `collapseToQuarterStart()` + `opts.quarterlyStepAccum`. A table showing the same figure three months
  in a row was a real user-reported bug, not a cosmetic one.
- **Incomplete windows are `None` in the primitives**: `quarterly_step_level()` uses `min_count=3` and
  `rolling_sum()` uses `min_periods=window`. `ytd_sum()` returns `None` for the rest of the year once
  any month is missing, because a sum that skips a month is not that period's accumulation.
- **Landmine: `labor_market/transforms.py` carries its own `rolling_sum`/`ytd_sum` pair that treats
  `None` as `0`.** Safe there only because `_load_caged_cut()` reindexes with `fill_value=0` first (a
  section with no hires genuinely had zero, not unknown). **Don't copy that pair into a series that can
  have genuinely missing values.**
- Degenerate combinations are enforced with `opts.metricAvailability` (per-`Nível` `<option>` disabling
  in `makeHierTab()`), never by silently returning nulls.
- **Semiannual is unimplemented.** Adding it means a `semester_step_level()` alongside
  `quarterly_step_level()`, same step-and-collapse pattern.

---

## Comparisons (layer 5) — the guards, and what they measured

- **Point difference vs. percent change** is carried as data, not re-derived:
  `labor_market/pnad_tab.py` ships a `rate_keys` list in the payload so the JS never has to guess
  whether a series is already a percentage.
- **Zero base → `Infinity`. Guarded since 2026-08** — both copies of `pct_change()` return `None`
  instead of `inf`. Before the fix the guard was `np.isnan(v)`, which does not catch `inf`, so a bare
  `Infinity` reached the payload and rendered literally in the table — and, worse, a single infinite
  point in a plotted trace collapses Plotly's y-autorange and `_bindYAutofit()`'s fitted range with it.
  Measured on the shipped report before the fix: **6,814 `Infinity` values** — 5,172 in Investimento
  (36 of its 78 series contain an exact zero, mostly budget functions that never receive an inversão
  financeira) and 1,642 in RTN (`incentivos_fiscais` has been exactly 0 every month since 2024-01, so
  its Y/Y went infinite from 2025-01 on). Both `credit/transforms.py` and `fiscal_policy/transforms.py`
  now guard with `np.isfinite`.
- **Sign-crossing flows get no percent change at all.** CAGED's `saldo` is a net flow that crosses zero
  (all 22 CNAE sections do; the national Y/Y reaches 696%), so that tab offers **Mensal / Acum. 12m /
  Acum. no ano** instead of growth rates — which is also how the MTE itself publishes.

---

## `% PIB` (layer 4) — open convention, and the register of who uses which

The ratio is always **nominal ÷ nominal**. What is *not* settled is the denominator's window, and the
choice **only exists for flows**:

- A **stock** over a single month's GDP is meaningless — stocks always go over 12-month GDP
  (`atv_pib_mensal.pib_acum_12m`, SGS 4382). This is also what the BCB itself does:
  `saldo_total_total ÷ pib_acum_12m` reproduces its published `cred_credito_resumo.pct_pib_total_total`
  exactly.
- A **flow** has two defensible denominators:

| | Option A — same window | Option B — always 12m GDP |
|---|---|---|
| Definition | Both sides of the ratio use the selected `Nível`'s window | Numerator follows `Nível`, denominator is always 12m GDP |
| Denominators | `pib_mensal` (4380) for Mensal/Trimestral/YTD, `pib_acum_12m` (4382) for Acum. 12m | `pib_acum_12m` (4382) always |
| Reads as | "this quarter's spending as a share of this quarter's output" | "this quarter's spending, annualized share of output" |
| Cost | Values are not comparable across `Nível` selections — scale shifts | Values are comparable across `Nível`, but a monthly flow over annual GDP is a small number needing explanation |

**Register — both are in use, split per tab:** `fiscal_policy/`'s GFSM and RTN tables use **A**
(adopted 2026-08 — `compute_pct_pib_same_period()` for Mensal/Trimestral/YTD, `compute_pct_pib_ttm()`
for Acum. 12m); `fiscal_policy/`'s **Investimento tab uses B** (user choice, 2026-08 —
`credit_tf.compute_pct_pib()` against `pib_acum_12m` for Mensal/Trimestral/YTD, and
`compute_variants_monthly_ttm(gdp_ttm=)` for Acum. 12m, which is the same ratio); `credit/` uses **B**
(matching the BCB's own published ratio); the DLSP tab uses **B** with a 12m-rolled numerator for its
flows, which preserves the stock–flow identity in %GDP terms.

**A third case, from 2026-09-01: when the numerator has no seasonally-adjusted variant, the window is
not a convention choice — it is the whole answer.** `economic_activity/`'s Renda e Poupança tab is on
**A** (both sides in the same window, both from the same table), but its window is exposed as the
user's own toggle with the **4-quarter sum as the default**, because the single-quarter ratio is
dominated by seasonality: measured on `atv_renda_poupanca` (IBGE Agregado 2072, NSA-only), Poupança
Bruta swings between **10,8% and 16,6% of GDP inside the last 8 quarters** raw, against **14,4% flat**
on the 4-quarter window. IBGE's own published taxa de poupança/taxa de investimento use the same
4-quarter convention. Two rules follow: **check for an SA variant before offering the native-frequency
ratio at all**, and **don't call the result the official rate** — the same window on a broader
numerator (here Formação Bruta de Capital, which includes inventories, vs. the FBCF the official taxa
de investimento uses) is a different number with the same name.

**Direction of travel is B**, chosen for the newest tab; GFSM/RTN were offered the retrofit and left on
A for now, so the same report currently serves both conventions. A tab on B must say so on its own
y-axis (Investimento's reads `% do PIB 12m (<Nível>)`) — otherwise its Mensal figure looks ~12x smaller
than the neighbouring tab's with no visible reason. When a new tab needs `% PIB` on a flow, **ask which
convention to use** rather than copying whichever neighbour was opened last, and record the answer
here. Under A, never average or compare `% PIB` values read off different `Nível` selections; under B
that comparison is exactly what the convention buys.

---

## The cube: pre-compute it, and keep it small

**Every combination is computed in Python and shipped in the payload; the browser only reads.** No
metric is derived client-side — that is what keeps the report a static file and the arithmetic
reviewable.

The cube multiplies fast: *series × levels × bases × metrics*. Investimento is 78 series × 4 levels × 2
bases × 5 metrics = 2,340 variants. At that size the payload shape matters more than the math:

- **Use the compact shared-dates shape** — `dates` once at the payload root, each variant a bare value
  array, and the scalar `0`/`null` for identically-zero or empty variants (re-expanded in JS). Measured
  on Investimento: **3.63 MB vs. 15.31 MB** for the same data in the `{dates, values}`-per-variant
  shape. `makeHierTab()` reads either, decided by `opts.sharedDates` — a payload and its opts must
  match, or traces render with `x: undefined` and the chart is silently blank.
- **Disable, don't null.** A degenerate combination should be an unselectable `<option>`
  (`opts.metricAvailability`), so the user never selects a reading that doesn't exist.
- **Sum levels, never rates.** A synthesized parent total is valid for R$ levels (`sum_series()`) and
  invalid for any percentage or growth child — a cut with no natively-published total gets a
  **header-only row** for those metrics: expandable, no checkbox, `seriesKey` deliberately absent from
  `series`.

---

## Primitives — reuse, don't reimplement

| Need | Function | Module |
|---|---|---|
| Chained IPCA index | `build_price_index()` | `credit/transforms.py`, `fiscal_policy/transforms.py` |
| Deflate to constant reais | `deflate_series()` | both of the above |
| Seasonal adjustment (monthly) | `stl_seasonal_adjust()` | `credit/transforms.py` (`period=12`) |
| Seasonal adjustment (quarterly) | `stl_seasonal_adjust(period=4)` | `fiscal_policy/transforms.py` |
| Rolling accumulation | `rolling_sum()` | `fiscal_policy/transforms.py` |
| Closed calendar quarter | `quarterly_step_level()` / `quarterly_step_map()` | `fiscal_policy/transforms.py` |
| YTD accumulation | `ytd_sum()` / `ytd_map()` | `fiscal_policy/transforms.py` |
| Percent change / point difference | `pct_change()` / `pp_diff()` | `fiscal_policy/transforms.py` |
| `% PIB`, same window | `compute_pct_pib_same_period()` | `fiscal_policy/transforms.py` |
| `% PIB`, 12m denominator | `compute_pct_pib_ttm()` / `compute_pct_pib()` | `fiscal_policy/` / `credit/` |
| Whole cube, native monthly | `compute_variants()` | `credit/transforms.py` |
| Whole cube, smoothed flow base | `compute_variants_ma3()` | `credit/transforms.py` |
| Whole cube, native quarterly | `compute_variants()` | `fiscal_policy/transforms.py` |
| Whole cube, closed quarter / 12m / YTD | `compute_variants_quarterly_step()` / `_ttm()` / `_monthly_ttm()` / `_ytd()` | `fiscal_policy/transforms.py` |
| Point-wise sum of series | `sum_series()` | `credit/transforms.py` |

The split across two modules is **historical, not principled** — `fiscal_policy/transforms.py`
re-implements `pct_change`/`build_price_index`/`deflate_series` that `credit/transforms.py` already had,
and `investimento_tab.py` imports from both (`credit_tf` for the native-monthly cube, `fiscal_tf` for the
aggregated ones). A new tab should do the same rather than write a third copy; consolidating them into a
single shared module is unclaimed work, not a decided plan.

---

## What each report offers today

| Report | Window | Basis | Comparison / denominator |
|---|---|---|---|
| `fiscal_policy/` GFSM | Trimestral, Acum. 12m | Nominal/Real | Nível, Y/Y, Marginal (SA), % PIB (A) |
| `fiscal_policy/` RTN | Mensal, Trimestral, Acum. 12m | Nominal/Real | Nível, Y/Y, Marginal (SA at Mensal), % PIB (A) — Marginal disabled at Acum. 12m |
| `fiscal_policy/` Investimento | Mensal, Trimestral (T/T SA at `period=4`), Acum. 12m, Acum. no ano | Nominal/Real | Nível, Y/Y, M/M, T/T, % PIB (**B**) |
| `fiscal_policy/` DLSP | native monthly (stock) / 12m (flows) | — | Nível, % PIB (B) |
| `credit/` Saldo | Mensal | Nominal/Real | Nível, Y/Y, M/M (SA), T/T (SA), % PIB (B) |
| `credit/` Concessão | Mensal, base is SA+MM3 | Nominal/Real | Nível, M/M, T/T, % PIB (B) |
| `credit/` Taxa & Spread, Inadimplência | Mensal | — (already %) | Nível only |
| `labor_market/` PNAD | native (monthly / quarterly) | — | Nível, Var. Curto Prazo, Var. Anual (p.p. or %) |
| `labor_market/` CAGED flows | Mensal, Acum. 12m, Acum. no ano | — | Nível only (sign-crossing) |
| `us/labor_market/` | Mensal (+ MM3/MM12/Acum. 12M/Y/Y fused in one pill) | — | Level, % of total — **pre-dates the 7-layer taxonomy, not yet migrated** |
| `economic_activity/`, `inflation/` | per-tab, see their own `CLAUDE.md` | | |

---

## Open conventions

Record additions here rather than resolving them silently in one tab:

1. **`% PIB` denominator for flows** — same-window (A) vs. always-12m (B). Still both in use: GFSM/RTN on
   A, Investimento/DLSP/`credit/` on B. Direction of travel is B, but the GFSM/RTN retrofit was offered
   and declined for now, so **keep asking before building**.
2. **Real GDP denominator** — whether a `% PIB` computed against real GDP is ever worth exposing
   (numerically identical today, since the deflator cancels).
3. **Deflator for capital spending** — Investimento deflates GND 4/5 by the IPCA, like every other tab.
   For works and equipment the INCC or the FBCF deflator would be more defensible. Raised 2026-08, not
   decided.
4. **Marginal comparison at Acum. 12m** — offered (Investimento) vs. disabled (RTN), both deliberate.
5. **Per-series suppression of percent change** — the sign-crossing guard is currently all-or-nothing per
   tab (CAGED drops growth rates entirely). Investimento has only 8 sign-crossing series out of 78
   (`ajuste_ordem_bancaria` is negative in 61 of 222 months), and the user chose 2026-08 to **keep the
   growth options available and document the caveat in the Apêndice** rather than build a per-series
   mask — same call `credit/` already makes for small-base modalities. If a tab ever needs the mask, it
   is a new mechanism and belongs in the skill's taxonomy first.
6. **Semiannual window** — legal on the frequency ladder, unimplemented.
7. **Migrating the existing tabs to the 7-layer taxonomy** — the skill's split of window from smoothing,
   and of `Δ` from `%`, is not retrofitted anywhere yet. `us/labor_market/` is the intended pilot,
   because it is where the fused pill makes "3-month average of the monthly change" unreachable.

*Resolved and moved out of this list*: SA on closed-calendar aggregates (now `seasonal=True`); the
zero-base `Infinity` guard (now enforced in both `pct_change()` copies); the taxonomy itself, which
moved to the skill on 2026-09-04 and is no longer duplicated here.

---

## When in doubt, ask

A new tab that would introduce a **new layer**, a **new window type**, a **different denominator**, or a
**different seasonal-adjustment rule** is a decision for the user, not a default to pick. Ask first,
then record the answer: the shape of the mechanism goes in the
[skill's taxonomy](../../.claude/skills/lis-dashboard/references/design-system.md#metricas), the choice
this repo made goes here.
