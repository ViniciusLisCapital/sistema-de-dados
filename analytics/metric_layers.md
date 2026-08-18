# Metric layers — the standard axes of an interactive series table

Every interactive table in `analytics/` exposes the same small set of **orthogonal axes** over the
same underlying series: how far the data is aggregated, whether it is inflation-adjusted, and what it
is compared against. This file is the spec for those axes — read it **before** adding a metric
selector to a new tab, so a new dashboard inherits the conventions instead of inventing a fourth
variant of them.

Companion files, different concerns: [`seasonal_adjustment.md`](seasonal_adjustment.md) covers *which*
adjustment method (STL vs. X-13) and its scope; [`.claude/rules/lis-dashboards.md`](../.claude/rules/lis-dashboards.md)
covers chart interaction (pan/zoom/quick-range); [`report_structure/CLAUDE.md`](report_structure/CLAUDE.md)
covers the build-time scaffolding. This file covers only **what the numbers mean**.

---

## The three layers

| Layer | Axis | Question it answers | Typical UI |
|---|---|---|---|
| **(i)** | Aggregation level | Over how long a window is the value summed? | `Nível`: Mensal / Trimestral / Acum. 12m / Acum. no ano |
| **(ii)** | Basis | Is the history adjusted to inflation? | `Nominal` / `Real` |
| **(iii)** | Modelling | Compared against what? | `Nível` / `Y/Y` / `Marginal` / `% PIB` |

The three are **independent** — none replaces another, and a selector for one must not silently move
another. Some *combinations* are degenerate and must be disabled (see the availability table below),
but that is a property of the combination, not a coupling between the axes.

---

## Order of operations (load-bearing)

```
native series (nominal, at its own published frequency)
   │
   ├─(ii) deflate ─────────────── at the NATIVE frequency, before any aggregation
   │
   ├─(iii-sa) seasonally adjust ─ only when a marginal comparison is requested
   │
   ├─(i) aggregate ───────────── rolling window / closed calendar / YTD
   │
   └─(iii) compare ───────────── Y/Y, marginal, % GDP
```

**Deflate before aggregating, never after.** `Σ(deflated monthly values) ≠ deflate(Σ nominal values)`
whenever inflation moves inside the window: the second form prices twelve months of spending as if it
all happened at the last month's price level. To get a real quarter from a monthly series, deflate the
months, then sum them. Every `transforms.py` in the project already does this — `deflate_series()`
runs on the native array and the aggregation happens *inside* the per-basis `_variants()` closure, so
the nominal and real branches each aggregate their own values.

**The reference date for the deflator is the last available IPCA month** — constant reais of the most
recent month, so the newest observation equals its own nominal value. Every call site computes it the
same way (`ref_date = ipca_pct["dates"][-1]`) and ships it in the payload as `ref_date` for the
report's own axis labels.

---

## (i) Aggregation level

### The frequency ladder — you may only reduce, never invent

A series can be aggregated **up to** any coarser window, and never down to a finer one. A monthly
series can be read monthly, quarterly, semiannually, 12-month or annually; a quarterly series has no
monthly reading at all.

| Native frequency | Legal `Nível` options |
|---|---|
| Daily | daily, monthly, quarterly, semiannual, 12m, annual |
| Monthly | monthly, quarterly, semiannual, 12m, annual |
| Quarterly | quarterly, semiannual, 12m (= 4 quarters), annual |
| Annual | annual only |

This is why the GFSM table (quarterly `fisc_efgg`) offers no *Mensal* while the RTN table (monthly
`fisc_rtn`) does, in the same tab — a difference in the source, not a UI inconsistency.

### Rolling vs. closed calendar

Two genuinely different windows, both legitimate, never interchangeable:

| Window | Definition | Primitive | Used by |
|---|---|---|---|
| **Rolling** | Sum of the last N periods ending at *t*, recomputed every period | `rolling_sum(values, window)` | Acum. 12m everywhere; `compute_variants_ttm` (4Q), `compute_variants_monthly_ttm` (12M) |
| **Closed calendar** | Sum of the fixed calendar block (Jan+Feb+Mar), non-overlapping | `quarterly_step_level(dates, values)` | RTN/Investimento `Trimestral`; makes a monthly series comparable to a natively-quarterly one |
| **YTD** | Sum from January of the current year, resetting each January | `ytd_sum(dates, values)` | Investimento `Acum. no ano`, CAGED `Acum. no ano` |

`quarterly_step_level()` repeats the quarter's value across its three months so the `pct_change` lags
(12 for Y/Y, 3 for T/T) stay arithmetically correct on a monthly index. **The display must collapse
that step to one column per quarter** (`collapseToQuarterStart()` + `opts.quarterlyStepAccum` in
`makeHierTab()`) — a table showing the same figure three months in a row was a real user-reported bug,
not a cosmetic one.

### Incomplete periods: blank until the window is complete

**Decision, 2026-08: a closed or rolling window with a missing period shows nothing.** Not a partial
sum, not a flagged estimate — `—`. `quarterly_step_level()` uses `min_count=3` and `rolling_sum()`
uses `min_periods=window`, both yielding `None`, and that is the standing convention for any new tab.
The reason is that a two-month "quarter" plotted on the same line as three-month quarters reads as a
collapse in the level, and no amount of footnoting undoes what the chart already showed.

**YTD is the deliberate exception**, and only because its comparison is like-for-like by construction:
Jan+Feb of this year is compared Y/Y against Jan+Feb of last year (lag 12 on a series that itself
resets each January), so the partial window is never measured against a full one. This is also why
YTD offers **only** Y/Y — M/M and T/T would cross the January reset, where a closed year becomes one
month.

A **hole in the middle** of a YTD window is a different case from an unfinished tail:
`fiscal_policy.transforms.ytd_sum()` returns `None` for the rest of the year once any month is
missing, because a sum that skips a month is not that period's accumulation. Note that
`labor_market/transforms.py` carries its own `rolling_sum`/`ytd_sum` pair that treats `None` as `0`
instead — safe there only because `_load_caged_cut()` reindexes with `fill_value=0` first (a section
with no hires genuinely had zero, not unknown). **Don't copy that pair into a series that can have
genuinely missing values.**

### Degenerate combinations to disable

Enforce these with `opts.metricAvailability` (per-`Nível` `<option>` disabling in `makeHierTab()`),
not by silently returning nulls:

| Level | Disable | Why |
|---|---|---|
| Trimestral (closed) | M/M | Constant inside the step: 0% for two months, an artificial jump at the turn |
| Acum. no ano | M/M, T/T | Both cross the January reset |
| Any accumulated level | — | Marginal is *allowed* but changes meaning — see (iii) |

Semiannual is legal on the ladder above but is **not implemented in any report yet** — adding it means
a `semester_step_level()` alongside `quarterly_step_level()`, same step-and-collapse pattern.

---

## (ii) Nominal vs. Real

- **Deflator**: `inflc_agregados.ipca` (monthly %) → `build_price_index()` chains it into an index →
  `deflate_series()` rebases to `ref_date`. The index's base month is arbitrary; only ratios between
  two dates are used.
- **Deflate at the native frequency**, before aggregation — see Order of operations.
- **Never deflate** a series that is already a ratio (rates, spreads, `% PIB`, PNAD's `taxa_*`), nor
  one the source already publishes in real terms (`rend_*_real`). The Real toggle should not exist on
  a tab whose series are all percentages — Taxa & Spread and Inadimplência in `credit/` have no
  Nominal/Real axis at all, deliberately.
- **Stock vs. flow** needs no special rule: a stock is deflated at its own point-in-time index, a flow
  at its own period's index and then summed. Both fall out of "deflate at native frequency".
- **`% PIB` needs no real counterpart** — the deflator cancels in the ratio, so real ÷ real GDP equals
  nominal ÷ nominal GDP. Selecting `% PIB` should force Nominal and disable Real (what `makeHierTab()`
  already does). Whether a distinct real-GDP-denominator framing is ever worth *exposing* is recorded
  as an open question in [`fiscal_policy/CLAUDE.md`](fiscal_policy/CLAUDE.md) — it is not a live bug.

---

## (iii) Modelling / comparison

### Y/Y is NSA; marginal comparisons are SA

Year-over-year cancels seasonality by construction, so it is computed on the **raw** level — adjusting
first would only inject the adjustment's own error. Lag is one full year in the series' own frequency:
12 monthly, 4 quarterly.

Marginal comparisons (M/M, T/T) compare adjacent periods and therefore **require seasonal
adjustment**. Two conventions are in use, and they must be labeled distinctly rather than merged into
one selector:

| Convention | Definition | Where |
|---|---|---|
| **Rolling 3M/3M momentum** | `pct_change(sa, 3)` on the SA monthly level — month *t* vs. *t−3* | `credit/` (Saldo, Concessão), `atv_pim`/`atv_pim_uso` |
| **Calendar T/T** | Quarter vs. the immediately preceding calendar quarter, on an SA quarterly series | GFSM (native quarterly, STL `period=4`) |

Which STL freezing convention applies (whole-sample mean per month vs. last-complete-year factors
carried forward) is documented in [`seasonal_adjustment.md`](seasonal_adjustment.md) and, for the
divergence between `credit/` and `fiscal_policy/`, in [`fiscal_policy/CLAUDE.md`](fiscal_policy/CLAUDE.md).
Both fit only through the last complete calendar year — never over a half-finished current year.

### SA on an already-aggregated level

- **Rolling 12m**: no SA, and none needed — a 12-month window spans every season. But the marginal
  reading changes meaning: the change in a 12-month accumulation measures the **acceleration of the
  window**, not this month against last month. Two reports resolve that differently on purpose — RTN
  disables Marginal at Acum. 12m; Investimento offers it with the acceleration reading spelled out in
  the caption and Apêndice. **Don't unify them without asking.**
- **Closed calendar quarter built from monthly data**: this one *does* need SA at `period=4` (Q4 fiscal
  spending is systematically higher than Q1). **Implemented 2026-08 as an opt-in** —
  `compute_variants_quarterly_step(seasonal=True)` routes `qoq_sa` through
  `quarterly_step_qoq_sa()`; with the default `seasonal=False` it stays a bare `pct_change(step, 3)`
  and the `_sa` suffix remains just a JS-compatibility key name. **Investimento opts in; RTN
  deliberately does not** (user choice, 2026-08 — closing the gap for the new tab without moving RTN's
  already-published numbers). A new tab adding a marginal comparison on a calendar-aggregated series
  should pass `seasonal=True`.
  - **Run the STL on the collapsed quarterly series, never on the monthly step.** The step repeats each
    quarter's value across its three months, so `period=4` over that array treats four consecutive
    *months* as one cycle and fits a seasonality that does not exist. `quarterly_step_qoq_sa()`
    collapses to one observation per quarter, fits `period=4` there, takes `pct_change(sa, 1)`, and
    re-expands onto the monthly grid for `collapseToQuarterStart()` to reduce again at display time.

### Units: percent change vs. percentage points

| Series is… | Comparison | Primitive |
|---|---|---|
| A level (R$, people, index) | percent change | `pct_change()` |
| Already a percentage (rate, `% PIB`, spread) | **point difference** | `pp_diff()` |

"Unemployment went from 7.5% to 7.0%" is **−0.5 p.p.**, never "−6.7%". `labor_market/pnad_tab.py`
carries this as a `rate_keys` list in the payload so the JS never re-derives it.

### Two guards a new tab must respect

- **Zero base → `Infinity`. Guarded since 2026-08 — both copies of `pct_change()` return `None`
  instead of `inf`.** Before the fix the guard was `np.isnan(v)`, which does not catch `inf`, so a bare
  `Infinity` reached the payload and rendered literally in the table — and, worse, a single infinite
  point in a plotted trace collapses Plotly's y-autorange and `_bindYAutofit()`'s fitted range with it.
  Measured on the shipped report before the fix: **6,814 `Infinity` values** — 5,172 in Investimento
  (36 of its 78 series contain an exact zero, mostly budget functions that never receive an inversão
  financeira) and 1,642 in RTN (`incentivos_fiscais` has been exactly 0 every month since 2024-01, so
  its Y/Y went infinite from 2025-01 on). Both `credit/transforms.py` and `fiscal_policy/transforms.py`
  now guard with `np.isfinite`. A percent change on a zero base is *undefined*, not infinite — `—` is
  the honest cell.
- **Sign-crossing flows get no percent change at all.** CAGED's `saldo` is a net flow that crosses zero
  (all 22 CNAE sections do; the national Y/Y reaches 696%), so that tab offers **Mensal / Acum. 12m /
  Acum. no ano** instead of growth rates — which is also how the MTE itself publishes. Percent change on
  a sign-flipping series is numerical noise, not a weak reading.

### `% PIB` — open convention

The ratio is always **nominal ÷ nominal** (see (ii)). What is *not* settled is the denominator's window,
and the choice **only exists for flows**:

- A **stock** over a single month's GDP is meaningless — stocks always go over 12-month GDP
  (`atv_pib_mensal.pib_acum_12m`, SGS 4382). This is also what the BCB itself does: `saldo_total_total ÷
  pib_acum_12m` reproduces its published `cred_credito_resumo.pct_pib_total_total` exactly.
- A **flow** has two defensible denominators:

| | Option A — same window | Option B — always 12m GDP |
|---|---|---|
| Definition | Both sides of the ratio use the selected `Nível`'s window | Numerator follows `Nível`, denominator is always 12m GDP |
| Denominators | `pib_mensal` (4380) for Mensal/Trimestral/YTD, `pib_acum_12m` (4382) for Acum. 12m | `pib_acum_12m` (4382) always |
| Reads as | "this quarter's spending as a share of this quarter's output" | "this quarter's spending, annualized share of output" |
| Cost | Values are not comparable across `Nível` selections — scale shifts | Values are comparable across `Nível`, but a monthly flow over annual GDP is a small number needing explanation |

**Currently in the codebase: both, and the split is now per-tab rather than per-folder.** `fiscal_policy/`'s
GFSM and RTN tables use **A** (adopted 2026-08 — `compute_pct_pib_same_period()` for Mensal/Trimestral/YTD,
`compute_pct_pib_ttm()` for Acum. 12m); `fiscal_policy/`'s **Investimento tab uses B** (user choice,
2026-08 — `credit_tf.compute_pct_pib()` against `pib_acum_12m` for Mensal/Trimestral/YTD, and
`compute_variants_monthly_ttm(gdp_ttm=)` for Acum. 12m, which is the same ratio); `credit/` uses **B**
(matching the BCB's own published ratio); the DLSP tab uses **B** with a 12m-rolled numerator for its
flows, which preserves the stock–flow identity in %GDP terms.

**Direction of travel is B**, chosen for the newest tab; GFSM/RTN were offered the retrofit and left on
A for now, so the same report currently serves both conventions. A tab on B must say so on its own y-axis
(Investimento's reads `% do PIB 12m (<Nível>)`) — otherwise its Mensal figure looks ~12x smaller than the
neighbouring tab's with no visible reason. When a new tab needs `% PIB` on a flow, **ask which convention
to use** rather than copying whichever neighbour was opened last, and record the answer here. Under A,
never average or compare `% PIB` values read off different `Nível` selections; under B that comparison is
exactly what the convention buys.

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
- **Disable, don't null.** A combination that is degenerate should be an unselectable `<option>`
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

| Report | (i) Aggregation | (ii) Basis | (iii) Modelling |
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
   is a new mechanism and belongs in this file first.
6. **Semiannual level** — legal on the ladder, unimplemented.

*Resolved and moved out of this list*: SA on closed-calendar aggregates (now `seasonal=True`, see (iii));
the zero-base `Infinity` guard (now enforced in both `pct_change()` copies).

---

## When in doubt, ask

These layers are conventions this project settled on, not arithmetic truths. A new tab that would
introduce a **fourth axis**, a **new window type**, a **different denominator**, or a **different
seasonal-adjustment rule** is a decision for the user, not a default to pick — ask first, then record
the answer in this file so the next dashboard inherits it.
