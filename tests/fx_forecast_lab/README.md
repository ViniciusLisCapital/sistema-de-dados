# fx_forecast_lab — pure out-of-sample FX forecasting

Isolated sandbox for one question: **using only information available at T, what
is USD/BRL at T+h?** Nothing here imports, writes to, or otherwise touches
`analytics/brasil/exchange_rate/` — the shipped FX Model is untouched by
construction, and this lab re-reads the same MySQL tables rather than borrowing
its loaders, so an experiment can redefine a variable without any risk of
leaking back into production.

It is the complement `models/ridge_vs_random_walk.md` explicitly lists as **not
tested**: that note ran a *conditional* race, handing the model the realized
future path of its five channels and asking only that it translate fundamentals
into an FX path. It won by ~40% of RMSE, and its own closing caveat is the
reason this lab exists — the channels it was handed are themselves closer to
random walks than the exchange rate is, so the conditional premise is where the
whole difficulty had gone. Here nothing about the future is given.

```powershell
uv run python -m tests.fx_forecast_lab.data                   # rebuild the panel (hits MySQL + FRED)
uv run python -m tests.fx_forecast_lab.features               # feature inventory and per-spec samples
uv run python -m tests.fx_forecast_lab.test_lab_integrity     # the controls — run these first
uv run python -m tests.fx_forecast_lab.run                    # the horse race
uv run python -m tests.fx_forecast_lab.run --horizons 1,3 --specs fundamentals --window 0
```

---

## What makes it a *pure* forecast

Three rules, each of which is a place a leak would otherwise enter silently.

**1. Every panel row is as-of.** Row `m` of `cache/panel_monthly.csv` holds only
what a reader had on the last business day of `m`. Daily sources are collapsed
with an as-of cutoff (`month_end − pub_delay_days`), monthly sources are shifted
by whole months. IPCA and US CPI carry a one-month shift because both are
published mid-following-month; BCB contracted FX loses its last four calendar
days; FUNCEX terms of trade run two months behind. The lag applied to each
series, and the reason, live in `data.AVAILABILITY` and are written into
`cache/panel_meta.json` on every rebuild.

This is not a refinement. A month-end `resample().last()` on IPCA would hand the
model an inflation print that did not exist yet — and since relative PPP is the
one channel the conditional note measured as genuinely forecastable, that leak
would land exactly where it does the most damage.

**2. Direct, not iterated.** One model per horizon, regressing the cumulative
h-month log return on the state at the origin. The iterated alternative needs a
projected path for every regressor, which is the part the conditional note
measured as impossible. Direct forecasting lets the regression learn the h-month
mapping itself and never asks anyone to guess a CDS spread.

**3. No fold trains on an unresolved target.** A training row at `t` is admitted
at origin `T` only if `t + h <= T`. Without that filter the fold at `T` trains on
h months of returns that had not happened yet — the single easiest leak to ship,
and the one that makes a backtest look brilliant.

### Scored quantity and benchmark

`100·log(ptax[t+h]/ptax[t])`, in pp — deliberately the same quantity as
`models/ridge_vs_random_walk.md`, so the two notes sit on one ruler: that one is
the conditional upper bound, this one the unconditional reality. Positive means
the BRL depreciated.

The benchmark is the **driftless random walk** (forecast = 0), Meese-Rogoff's.
`rw_drift` — the training window's own mean — runs alongside as the harder
benchmark, since the sample covers a currency that lost most of its value.

Overlapping origins are corrected for everywhere: Bartlett-HAC variances with
bandwidth `h−1`, a moving-block bootstrap with block length `h`, and
Clark-West as the headline test rather than Diebold-Mariano, because the
driftless RW is *nested* inside every regression here and DM is undersized under
nesting.

---

## The controls, and why they come first

`test_lab_integrity.py` (11 checks, all passing as of 2026-09-14). A backtest
that reports "no better than a random walk" is worthless unless it can be shown
to recognise a model that *is* better — otherwise a broken harness and an honest
null are the same output. So the controls pull both ways:

- **Positive control**: a feature that is the answer plus noise must collapse U
  below 0.4 with CW p < 0.01. Measured: **U = 0.116**, CW p = 9e-10. The scoring
  can see a win.
- **Negative control**: five pure-noise regressors must land at U ≈ 1 with CW
  not firing, at h=1 and h=12. Measured: **1.013 and 1.110**, CW p = 0.46.
  Nothing leaks.

The rest pin the two alignment surfaces: that `ipca_index` at row `m` really is
the index for `m−1` *and is not* the index for `m`; that `ptax` at row `m` is the
real month-end print with no shift; that the contracted-FX month is genuinely
truncated rather than the full month a later reader would see; that
`target(panel, h)` is what it claims and leaves the last h rows NaN; and that the
training filter never admits an unresolved row. Two closed-form checks on the
statistics themselves (CW reduces to `mean(2·y·f)` against a zero benchmark;
HAC at bandwidth 0 equals the plain standard error).

---

## First result (2026-09-14) — the random walk wins

Six specs × four horizons (1, 3, 6, 12 months) × nine models against the
benchmark, rolling 120-month window refit every month, `min_train = 60`, models
in a cell scored on identical origins. 123–267 origins per cell.

**Of 216 model-spec-horizon cells, 15 have Theil U below 1, one has both U < 1
and Clark-West p < 0.05, and that one's bootstrap CI includes 1.** Under a pure
null you would expect ~11 cells at p < 0.05; this run produced 5. There is less
significance here than chance alone would manufacture.

Theil U by spec, for the three models worth reading (rolling 120m):

| spec | model | h=1 | h=3 | h=6 | h=12 |
|---|---|---|---|---|---|
| fundamentals | ridge | 1.017 | 1.138 | 1.355 | 1.776 |
| fundamentals | ridge_shrunk25 | 1.000 | 1.022 | 1.058 | 1.105 |
| technical | ridge | 1.017 | 1.081 | 1.189 | 1.340 |
| wide_2001 | ridge | 1.028 | 1.237 | **1.451** | 1.774 |
| wide_2001 | ridge_shrunk25 | 1.003 | 1.016 | **0.945** | 1.023 |
| wide_2008 | combo_shrunk50 | 0.997 | 0.991 | 1.005 | 1.036 |
| shipped_lagged | ridge_shrunk25 | 0.998 | 0.995 | 0.991 | 1.000 |
| fundamentals | rw_drift | 1.004 | 1.018 | 1.046 | 1.101 |

The single cell that cleared both bars — `wide_2001`, h=6, `ridge_shrunk25`,
U = 0.945, CW p = 0.0062 — does not survive inspection:

- its **bootstrap CI is [0.866, 1.026]**, which includes 1;
- its **DM p is 0.21**, i.e. the MSE gain itself is not significant;
- and switching the training window from rolling 120m to expanding moves it to
  **U = 0.992**. The conditional test's result was *indistinguishable* between
  the two window choices; this one is the whole effect.

### Four things the run establishes beyond the headline

**Shrinkage toward the random walk improves every regression, monotonically, at
every horizon — and the gradient does not stop before it reaches the benchmark.**
At `wide_2001`/h=6: ridge 1.451 → shrunk-50% 1.020 → shrunk-25% 0.945. The
direction is the finding. If the regressions carried signal, the optimum would
sit at an interior weight; it sits at the edge, which is what "these coefficients
are estimation noise" looks like from the outside.

**Unconstrained OLS is a catastrophe at long horizons**, reaching U = 3.07 at
h=12 on `wide_2008` with a bias of −33 pp. With ~20 regressors and ~120 training
rows of overlapping returns this is expected, and it is the reason the lineup
carries shrinkage and combination at all rather than one regression.

**The drift is not exploitable either.** `rw_drift` loses to the driftless RW at
every horizon in every one of the six specs, and gets worse as h grows (across
specs at h=12: 1.035 to 1.116). The BRL's long
depreciation is real and still not a tradable forecast at these horizons.

**Direction is not the same story as magnitude, and this is the one live thread.**
`wide_2008`/ridge gets the sign right on **60.7%** of h=6 origins and **57.7%** of
h=12 while losing badly on RMSE (1.74, 2.48); `wide_2001`/ridge hits 60.3% at h=6.
Right direction, wrong scale — the classic shape. RMSE was the agreed criterion
so this is not a result, but it is where a next round would look, and it would
need its own test (Pesaran-Timmermann) rather than these.

### A methodological gotcha found in the run

**Clark-West cannot tell a model from a shrunk copy of itself.** Against a
zero benchmark, CW's statistic reduces to `mean(2·y·f)/HAC_se(2·y·f)`; scaling
`f` by `w` scales numerator and denominator alike, so the t-statistic is
invariant. That is why `ridge`, `ridge_shrunk50` and `ridge_shrunk25` print
identical CW p-values in every cell above while their U ratios range from 1.45 to
0.94. CW answers "does the forecast point the right way beyond estimation
noise", never "does this model have lower MSE". **The MSE question belongs to DM
and to the bootstrap CI** — and for the one cell that mattered, both said no.
Worth knowing before quoting a CW p-value as evidence that a model beat a
benchmark.

---

## What is in each file

| file | what it owns |
|---|---|
| `data.py` | The as-of monthly panel. `AVAILABILITY` is the declaration of what each series costs in lag, and why. |
| `features.py` | Backward-looking transforms only, grouped into `BLOCKS` and assembled into `FEATURE_SETS`. `target(panel, h)` is the scored quantity. |
| `models.py` | `fit_predict(Xtr, ytr, xnow)`, one method, no dates. Standardisation is fitted inside the training window. |
| `backtest.py` | Walk-forward engine, HAC variance, Clark-West, DM-HLN, moving-block bootstrap, scoring. |
| `run.py` | The horse race; writes `results/horserace_<tag>.csv`. |
| `test_lab_integrity.py` | The controls. `_nopytest.py` shims the three pytest features they use, since pytest is not a dependency of this project. |

The feature blocks each have their own natural start (`dxy_em` 2006, contracted
FX 2008, CFTC 2011), which is why a spec that reaches wider reaches back less
far — `wide_2008` scores on 123 origins at h=12 against `technical`'s 245. The
engine intersects origins across models *within* a cell, so a U ratio never
compares two samples; it does **not** align across specs, so reading one spec's U
against another's is reading two different sample periods.

## Not tested

- **Anything below monthly.** A daily or weekly T+1, where market microstructure
  and flow data have far more to say, is a different panel and a different lab.
- **Directional / economic value.** Hit rates above 50% are in the output and
  were not tested for significance; a P&L rule with carry was not built.
- **Density forecasts.** Only the point forecast is scored, so nothing here says
  whether an interval would be calibrated.
- **Focus survey as predictor or benchmark.** `expc_focus` holds the market's own
  FX expectation at weekly frequency and is the obvious next regressor *and* the
  obvious second benchmark — "can we beat the consensus" is a different and more
  answerable question than "can we beat the random walk".
- **Non-linear models.** Everything here is linear in the features.
