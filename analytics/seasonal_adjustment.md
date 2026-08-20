# Seasonal adjustment — methods, scope, and practical notes

Two seasonal-adjustment methods are available in this project. **Which one to use is decided
case by case**, not by a blanket rule (explicit user decision, 2026-08). This file records what
each method is, how they differ, which series currently use which, and the practical obstacles
to applying X-13 at scale.

The measured comparison of the two against IBGE's own official adjustment is transcribed in
full in section (ii) — the interactive HTML version of it was a one-off and has been deleted.

---

## (i) The two methods

### STL — `statsmodels.tsa.seasonal.STL`

Seasonal-Trend decomposition using Loess. Pure Python, runs in-process, no external binary, no
install step. This is the incumbent: every seasonally-adjusted number the project produces today
comes from STL.

Four call sites, each with its own wrapper:

| Wrapper | Where | Period |
|---|---|---|
| `_saar_sa()` (inline in `run()`) | [`analytics/brasil/inflation/fetch_bcb.py`](brasil/inflation/fetch_bcb.py) | 12 |
| `stl_seasonal_adjust()` | [`analytics/brasil/credit/transforms.py`](brasil/credit/transforms.py) | 12 |
| `stl_seasonal_adjust()` | [`analytics/brasil/fiscal_policy/transforms.py`](brasil/fiscal_policy/transforms.py) | 4 (and 12 via `credit`'s) |
| `Score_SA()` | [`utils/thermometer.py`](../utils/thermometer.py) | 12 |

### X-13ARIMA-SEATS — `statsmodels.tsa.x13.x13_arima_analysis`

The US Census Bureau's official program, v1.1 Build 62, ascii build. A standalone Fortran
executable that statsmodels shells out to: it writes a `.spc` spec file, runs the binary, and
parses `seasadj`/`trend`/`irregular` back out.

Installed **machine-local, not in the repo**:

```
%LOCALAPPDATA%\x13as\x13as\x13as_ascii.exe   (+ a copy named x13as.exe)
X13PATH  = C:\Users\<user>\AppData\Local\x13as\x13as   (persistent User env var)
```

The `x13as.exe` copy exists because statsmodels probes `_binary_names` in order and `x13as.exe`
is the first entry. Call it with `prefer_x13=True` so the `X13PATH` variable is the one consulted:

```python
from statsmodels.tsa.x13 import x13_arima_analysis

r = x13_arima_analysis(s, x12path=X13PATH, prefer_x13=True, outlier=True, trading=True)
sa = pd.Series(np.asarray(r.seasadj), index=s.index)
```

`s` must be a monthly/quarterly `pd.Series` indexed by `PeriodIndex` with no gaps.

---

## (ii) How X-13 differs from STL, and where it wins

Three capabilities STL simply doesn't have:

1. **Forecast extension.** X-13 fits an ARIMA model and extends the series forward before
   decomposing, so the most recent months are adjusted with a two-sided filter instead of the
   one-sided window STL is forced into at the end of a series. This is the single most valuable
   difference in practice, because the end of the series is the part you actually read.
2. **Automatic outlier detection** — additive (AO), level shift (LS), and transitory change (TC),
   each with a t-statistic. STL's `robust=True` downweights outliers but never identifies or
   classifies them.
3. **Trading-day regressors** — corrects for how many Mondays, Saturdays etc. a given month
   contained, separately from the seasonal pattern itself.

### Measured results

Run 2026-08-17 with X-13 v1.1 Build 62. Two series were chosen because **IBGE publishes its own
seasonally-adjusted version of both** (`seasonal_adjs='Y'`), which turns a method-vs-method
comparison into a scored comparison against a real benchmark.

All statistics are computed on **month-over-month %**. `corr`/`rmse`/`mae` are against IBGE's
official SA series; `vol` is the series' own MoM standard deviation (the benchmark's own value is
the target, not zero — lower is not automatically better, since over-smoothing also lowers it);
`resid p` is the p-value of an F-test of calendar-month dummies on MoM, where **higher is better**
(low p = seasonality still left in the "adjusted" series); `gap max`/`gap 2020` are the largest
absolute MoM divergence from IBGE over the whole sample and within 2020.

**PMC — Comércio varejista restrito** (`atv_pmc.comercio_restrito_total`, 317 obs, 2000-01 → 2026-05):

| Method | corr | rmse | mae | vol | resid p | gap max | gap 2020 |
|---|---|---|---|---|---|---|---|
| Sem ajuste (NSA) | 0.164 | 12.203 | 8.058 | 12.360 | 0.000 | — | — |
| STL | 0.610 | 1.914 | 1.334 | 2.402 | 0.337 | 7.972 | 4.707 |
| X-13 | 0.710 | 1.700 | 1.266 | 2.417 | **0.779** | 6.812 | 3.206 |
| X-13 + trading day | **0.834** | **1.136** | **0.647** | **2.059** | 0.026 | **4.635** | **2.701** |
| IBGE oficial (benchmark) | 1.000 | 0.000 | 0.000 | 1.696 | 0.521 | — | — |

**PIM — Indústria geral** (`atv_pim.industria_geral`, 294 obs, 2002-01 → 2026-06):

| Method | corr | rmse | mae | vol | resid p | gap max | gap 2020 |
|---|---|---|---|---|---|---|---|
| Sem ajuste (NSA) | 0.394 | 6.056 | 4.870 | 6.588 | 0.000 | — | — |
| STL | 0.626 | 2.328 | 1.708 | 2.921 | 0.322 | 11.446 | 2.935 |
| X-13 | 0.713 | 2.173 | 1.778 | 3.101 | **0.954** | 6.885 | 2.826 |
| X-13 + trading day | **0.884** | **1.235** | **0.760** | **2.647** | 0.495 | **4.654** | **1.655** |
| IBGE oficial (benchmark) | 1.000 | 0.000 | 0.000 | 2.329 | 0.679 | — | — |

**Reading of the results.** X-13 + trading day beats STL on agreement (corr up from 0.61→0.83 and
0.63→0.88), on error (RMSE roughly halved on both, MAE cut by more than half), on divergence in
the hard 2020 window, and on volatility — its MoM volatility is the closest of the three to the
benchmark's own, meaning it is neither leaving noise in nor over-smoothing it out. The pattern is
the same on two independent surveys, which is what makes it more than sampling noise.

It does **not** win on every axis. On residual seasonality, plain X-13 is the best of the three on
both series (p = 0.78 and 0.95), but adding trading-day regressors makes PMC the **worst** of the
three (p = 0.026, against STL's 0.337) — there is still month-linked structure left in PMC's
adjusted series. PIM has no such problem (p = 0.495). Trading day is still the right default given
how much it wins on everything else, but PMC's residual seasonality is a real open defect, and
Brazilian moving holidays are the most likely cause — see (iv).

Endpoint stability, measured as the largest revision between a month's first print and its final
value across 24 vintages, on PIM: STL **3.02%**, X-13 **0.89%**. This came from a separate vintage
analysis, not from the table above, and was only run on PIM. It is the forecast extension doing
its job, and for reading a fresh macro print it is the difference that matters most.

**Outliers detected automatically** (X-13 + trading day). PMC — only 2, both the COVID collapse:

| Tag | Type | Coef | SE | t |
|---|---|---|---|---|
| `AO2020.Apr` | Additive (AO) | −0.1972 | 0.0147 | −13.38 |
| `AO2020.May` | Additive (AO) | −0.1044 | 0.0147 | −7.12 |

PIM — 6, spanning the 2008 crisis, the 2018 truckers' strike, and COVID:

| Tag | Type | Coef | SE | t |
|---|---|---|---|---|
| `AO2008.Nov` | Additive (AO) | −8.312 | 2.062 | −4.03 |
| `LS2008.Dec` | Level shift (LS) | −20.362 | 2.316 | −8.79 |
| `AO2018.May` | Additive (AO) | −11.163 | 1.709 | −6.53 |
| `AO2020.Apr` | Additive (AO) | −22.773 | 1.845 | −12.34 |
| `AO2020.May` | Additive (AO) | −16.697 | 1.935 | −8.63 |
| `AO2020.Jun` | Additive (AO) | −9.791 | 1.845 | −5.31 |

The `LS2008.Dec` level shift on PIM is worth noting on its own: X-13 identified the 2008 crisis as
a permanent step down in the level of industrial production, not a temporary dip. No STL-based
diagnostic in this project produces that distinction.

**Trading-day regressors cut PMC's outlier count from 7 to 2.** This was investigated against the
raw X-13 output and is substantive, not a parsing artefact: five of the seven "outliers" were
mis-attributed calendar effects, absorbed once weekday counts were modelled explicitly (Saturday
coefficient t = 5.08, χ² = 113.15, F = 18.36). Retail sales depend on how many Saturdays a month
contains, and without a trading-day term X-13 was booking that as anomalies.

**Weekday counts are calendar-universal, so `trading=True` is safe for Brazilian series.** Only
*holiday* regressors are US-specific, and those are not reachable through the statsmodels wrapper
at all — see (iv).

---

## (iii) Which series use which method

### Adjusted by us, with STL — ~391 series, ~760 STL fits per full pipeline run

| Consumer | Period | Series | Fits | Persisted? |
|---|---|---|---|---|
| [`inflation/fetch_bcb.py`](brasil/inflation/fetch_bcb.py) — `_SAAR_SERIES` + MA(3) | 12 | 20 | 20 | yes → `data/ipca_bcb_series.csv` as `*_ma3_sa` |
| [`credit/`](brasil/credit/) — Saldo (122), Concessão (72), Ampliado (21) | 12 | 215 | 430 | no, report-time |
| [`fiscal_policy/rtn_tab.py`](brasil/fiscal_policy/rtn_tab.py) — RTN Gov. Central | 12 | 35 | 70 | no |
| [`fiscal_policy/`](brasil/fiscal_policy/) — GFSM (108) + PIB/impulso | 4 | ~119 | 238 | no |
| [`oraculo/brasil/scores.py`](oraculo/brasil/scores.py) via `Score_SA` | 12 | 2 | 2 | as scores |

Fits ≈ 2 × series because `compute_variants()` adjusts the nominal and the IPCA-deflated version
separately — genuinely different inputs, so each needs its own fit. Only 12 of the 500 monthly
fits are refused for short history (minimum 8 observations, median 184).

### Adjusted by us, with X-13 — 0 series

Nothing in production uses X-13 yet. The only X-13 results produced so far are the ones
transcribed in (ii).

### Ingested already adjusted at source — 155 series

| Table | Source | SA series |
|---|---|---|
| `atv_pms` | IBGE | 29 |
| `atv_pim` | IBGE | 27 |
| `atv_pim_uso` | IBGE | 24 |
| `atv_pib` | IBGE | 22 |
| `atv_pib_taxas` (`indicador='qoq'`) | IBGE | 22 |
| `atv_pmc` | IBGE | 16 |
| `cred_credito_resumo` (`concessao_sa`) | BCB | 9 |
| `atv_ibcbr` (`*_sa`) | BCB | 6 |

Every IBGE survey stores a matched `seasonal_adjs='Y'`/`'N'` pair, so the NSA input always sits
next to the official SA benchmark — that pairing is what made the scorecard above possible.

### Deliberately not adjusted

[`labor_market/`](brasil/labor_market/) — visualisation only, no derived metric (explicit user decision).
[`economic_activity/`](brasil/economic_activity/) — consumes IBGE's own SA rather than computing any.

### Where X-13 is worth adopting first

The ~55 series that carry real analytical weight: the 20 SAAR aggregates in `inflation/` and the
35 RTN series in `fiscal_policy/`. At ~2.2s each that's about two minutes, and these are the
series where a fresh print gets read closely enough for endpoint stability to matter. The ~350
series in the credit and GFSM trees should stay on STL.

### Known inconsistency: four STL conventions

Not a blocker, but it means "the project's SA" is not one thing today:

- `inflation` and `credit` freeze the **mean** factor per calendar month over the whole in-sample
  window, so one "January factor" applies to January 2005 and January 2025 alike. Steady, never
  revises history, but blends regimes that no longer coexist.
- `fiscal_policy` keeps STL's **evolving** local `fit.seasonal` in-sample and freezes only the
  extrapolation into the incomplete current year. Explicit user request, 2026-08; the better of
  the two conventions, and the newer one.
- `utils/thermometer.py`'s `Score_SA` fits over the **entire** series with no cutoff and no
  freezing, so its factors revise retroactively every month a new observation arrives. This looks
  unintentional rather than chosen — it's the oldest of the four and predates the frozen-factor
  convention.

X-13 dissolves this trade-off rather than picking a side: it estimates drifting seasonality *and*
keeps the recent end stable.

---

## (iv) Practical problems with X-13

**Hard failures on noisy micro-series.** On 10 randomly sampled real IPCA subitems from
`inflc_decomposicao`, one failed outright:

```
X13Error: ERROR: Adding LS2007.Feb exceeds the number of regression effects allowed
```

Volatile series generate so many candidate outliers that X-13 hits its internal cap on
regression effects and refuses to finish. At a ~10% failure rate, a full 1.213-series sweep means
100+ series needing hand-written `.spc` files with capped outlier detection. **This, not compute
cost, is what rules out running X-13 unattended over the subitem tail.** Its auto-ARIMA plus
auto-outlier machinery is built for well-behaved published aggregates.

**It decomposes levels, not rates.** `inflc_decomposicao` stores `var_mensal` (% m/m), so the
rates must be chained into an index first:

```python
s = pd.Series(100 * (1 + d["var_mensal"].to_numpy() / 100).cumprod(),
              index=d["date"].dt.to_period("M"))
s = s[~s.index.duplicated()].asfreq("M").interpolate()
```

**Minimum 3 years of history.** Not binding for IPCA subitems (1.213 of 1.217 clear 36
observations, median 241), but it will bite on newer series.

**Brazilian moving holidays are out of reach through the wrapper.** Carnival and a moving Easter
need `genhol` plus a hand-written `.spc`, which `x13_arima_analysis()` does not expose. Only
weekday-count trading-day regressors are available. This is deferred as separate work — it is
also the most likely explanation for PMC's residual seasonality above.

**Machine-local install, not captured in the repo.** The binary is not a Python package, so
`uv sync` does not bring it — `X13PATH` is a User environment variable set per machine. A fresh
clone will not find it, and the call raises rather than falling back. Install steps and the
verification command are in [`AMBIENTE.md`](../AMBIENTE.md) ("Dependência de sistema opcional:
X-13ARIMA-SEATS").

**Runtime is highly variable** — 445 ms to 9.0 s per call in the sample. The slow calls are the
outlier-heavy ones, i.e. exactly the volatile series that also tend to fail.

**One subprocess and temp-file set per call.** Every call spawns the binary and writes a `.spc`
plus its outputs to a temp directory. Relevant to parallelism — see below.

---

## (v) Running X-13 faster: parallel subprocesses

Measured per-call cost on real IPCA subitems:

| Method | Mean | Range | Failures |
|---|---|---|---|
| STL | 36 ms | 14–64 ms | 0/10 |
| X-13 | 2.769 ms | 445–9.027 ms | 1/10 |
| X-13 + trading | 2.210 ms | 441–4.202 ms | 0/10 |

X-13 is roughly **60–76× slower per series** than STL. Extrapolated to all 1.213 subitem series
with sufficient history, serially: STL **44 s**, X-13 **56 min**, X-13 + trading **45 min**.

Because each call is a separate OS process, this parallelises almost linearly. With 8 worker
processes the full sweep drops to roughly **6 minutes** — an extrapolation from the per-call
timings, not a measured figure, but the work is subprocess-bound so it should hold closely.

`ProcessPoolExecutor`, not threads: the cost is in the child process and in `.spc` file I/O, so
threads would gain little and would contend on the temp directory. **Give every worker its own
`tempdir`** — concurrent calls sharing one directory can collide on output filenames.

```python
import os, tempfile
from concurrent.futures import ProcessPoolExecutor

X13PATH = os.path.join(os.environ["LOCALAPPDATA"], "x13as", "x13as")


def _sa_one(item):
    """Roda num processo filho -- tempdir proprio para nao colidir com os irmaos."""
    key, dates, values = item
    import numpy as np, pandas as pd
    from statsmodels.tsa.x13 import x13_arima_analysis

    s = pd.Series(values, index=pd.PeriodIndex(dates, freq="M"), dtype="float64")
    s = s[~s.index.duplicated()].asfreq("M").interpolate()
    with tempfile.TemporaryDirectory() as td:
        try:
            r = x13_arima_analysis(s, x12path=X13PATH, prefer_x13=True,
                                   outlier=True, trading=True, tempdir=td)
        except Exception as e:
            # "exceeds the number of regression effects allowed" cai aqui --
            # ~10% das series de subitem. Nunca deixar a excecao matar o lote.
            return key, None, f"{type(e).__name__}: {e}"
    return key, np.asarray(r.seasadj).tolist(), None


def sa_batch(items, workers=8):
    out, failed = {}, {}
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for key, sa, err in ex.map(_sa_one, items):
            (failed if err else out)[key] = err if err else sa
    return out, failed
```

Two rules for any batch use:

- **Never let one series kill the batch.** The `exceeds the number of regression effects` failure
  is expected at scale, not exceptional — catch per series and report the list.
- **Log what fell back.** A series that failed X-13 and silently reverted to STL is worse than a
  visible gap, because the resulting numbers are then a mix of two methods with no marker saying
  which is which.

---

## Open items

- **PMC's residual seasonality with trading day on** (p = 0.026) and the Brazilian moving-holiday
  regressors (`genhol` + a hand-written `.spc`) that would most likely fix it. The single most
  substantive defect in the results above.
- **The three divergent STL conventions** (see the end of (iii)) — in particular
  `utils/thermometer.py`'s `Score_SA`, which freezes nothing and revises its factors retroactively
  every month.
- **First production use of X-13** — nothing uses it yet. The ~55 series in (iii) are the intended
  starting point, one case at a time.
