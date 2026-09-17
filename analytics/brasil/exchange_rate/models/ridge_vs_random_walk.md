# Ridge vs. Random Walk — conditional out-of-sample horse race (2026-09-10)

Answers one question, asked directly: **does the shipped Ridge model beat a random
walk at 3, 6, 9 and 12 months, out of sample, when the exogenous channels are given
their realized values?** The framing is the user's own — *"se conseguimos estimar o
valor das variaveis exogenas, conseguiriamos prever o cambio"* — so this is a
**conditional** forecast test: the channels are treated as known, and only the FX path
is left for the model to reconstruct.

**Verdict: yes, at all four horizons, by roughly 40% of RMSE, significant at every
horizon under the correct test, and robust to the training-window choice.** Two
conditions bound how the result can be used, and one of them is the whole story —
see "The binding caveat" below.

This extends `referencia/equilibrium_model/ridge_window_horizon_grid.md` (2026-07-31),
which ran the same fold mechanism at the same four horizons but had **no benchmark**:
it reported MSE and R² without ever asking whether a random walk would have done
better. It also ran on the pre-2026-09-01 8-channel spec and the pre-2026-09-08
`fiscal` source, so its numbers are not comparable to these.

## Model tested

The shipped spec, unchanged — `_CHANNELS_5` (fiscal/CDS, dxy_em, carry_vol, sp500,
icbr_usd) + AR(1) on `delta_fx` + relative PPP as an **offset pinned at 1**, i.e.
exactly what `build_dashboard_payload()` feeds the FX Model tab.

**The harness is the shipped model, not a reimplementation of it.** It reuses
`forecast_error_bands_w72()`'s own fold loop, and that is verifiable: recomputing
`ridge_results/forecast_error_bands_w72.json`'s own quantity
(`sqrt(std_error_pct² + mean_error_pct²)`) from the harness's folds reproduces the
cached file to within 2×10⁻⁵ pp at all four horizons, on the same sample
(`2006-02..2026-07|n=246`) and the same 163 folds. Any discrepancy in this note is
therefore a discrepancy of the shipped model, not of the test.

| h | RMSE from cached JSON | RMSE from harness | diff |
|---|---|---|---|
| 3 | 4.6388 | 4.6388 | +0.000019 |
| 6 | 6.5093 | 6.5093 | −0.000015 |
| 9 | 8.5584 | 8.5584 | +0.000004 |
| 12 | 10.3850 | 10.3850 | +0.000013 |

## Design

- **Sample**: 2006-02 → 2026-07, n=246 months (post-`dropna`, the shipped sample).
- **Training window**: rolling 72 months, refit every month. 163 folds, forecast
  origins 2012-01 → 2025-07. Expanding-window variant run as a robustness check.
- **λ**: re-selected per fold by `walk_forward_lambda()` on that fold's **training
  window only**, `min_train = len(train)//2`. Never fixed in advance, never fit on a
  scored point.
- **Forecast**: genuinely multi-step. The AR(1) term is fed the model's **own**
  prediction at every step, never the realized one. The five channels and the
  inflation differential use their **realized** values for each forecast month — that
  is the conditional premise, not an oversight.
- **Scored quantity**: the cumulative h-month log return,
  `100·log(level(t+h)/level(t))`, so the four horizons are comparable to each other
  rather than mixing a one-step error with a compounded one. Level-space % error also
  reported.
- **All four horizons share the same 163 forecast origins** (every fold needs 12
  future months available), so cross-horizon comparisons are not confounded by
  different fold sets.

### Benchmarks

- **RW without drift** — forecast of the cumulative return is exactly 0, i.e. the level
  stays at its last observed value. The Meese-Rogoff benchmark, and the primary one.
- **RW with drift** — drift estimated as `mean(delta_fx)` over the fold's own training
  window, never the full sample. Included because a driftless RW is a soft benchmark
  against a currency that depreciated ~2.9× over the sample: giving the benchmark the
  trend is the harder test. It made almost no difference (see below), which is itself
  informative — the model is not beating the RW by knowing BRL drifts.

## Results — rolling 72m

RMSE and MAE in pp of cumulative log return; level RMSE in % of the realized level.

| h | RMSE Ridge | RMSE RW | RMSE RW+drift | **Theil U** | U vs RW+drift | R² | MAE Ridge | MAE RW |
|---|---|---|---|---|---|---|---|---|
| 3 | 4.591 | 7.745 | 7.773 | **0.593** | 0.591 | 0.622 | 3.672 | 6.021 |
| 6 | 6.459 | 11.148 | 11.211 | **0.579** | 0.576 | 0.618 | 5.067 | 8.439 |
| 9 | 8.382 | 14.358 | 14.512 | **0.584** | 0.578 | 0.598 | 6.759 | 10.658 |
| 12 | 10.135 | 16.861 | 16.926 | **0.601** | 0.599 | 0.557 | 8.222 | 12.883 |

| h | level RMSE Ridge | level RMSE RW | bias Ridge | bias RW | sign of move correct | \|err Ridge\| < \|err RW\| |
|---|---|---|---|---|---|---|
| 3 | 4.64% | 7.44% | +0.03 | −2.06 | 73.6% | 65.0% |
| 6 | 6.51% | 10.48% | +0.11 | −3.89 | 67.5% | 60.1% |
| 9 | 8.56% | 13.06% | +0.28 | −5.59 | 67.5% | 57.1% |
| 12 | 10.39% | 15.03% | +0.49 | −7.26 | 66.9% | 58.3% |

Two things in the second table are worth more than the U ratio. **The Ridge is
essentially unbiased and the RW is not** (−7.3 pp at 12m): that is the PPP offset
doing its job, and it is most of why the driftless and drifted RW score the same —
the drifted RW gets the trend but pays for it in variance. And **the win is not a
handful of lucky folds**: the Ridge is closer than the RW on 57-65% of origins, which
is a modest majority, so the 40% RMSE gain comes mostly from being far closer in the
folds where it wins rather than from winning nearly always.

### Significance: Clark-West, not Diebold-Mariano

| h | DM p (HLN-corrected) | **Clark-West p** | CW t | Theil U 95% CI (block bootstrap) |
|---|---|---|---|---|
| 3 | 0.0003 | **0.0001** | 3.87 | [0.484, 0.719] |
| 6 | 0.0045 | **0.0005** | 3.27 | [0.445, 0.753] |
| 9 | 0.0313 | **0.0045** | 2.61 | [0.413, 0.818] |
| 12 | 0.0758 | **0.0150** | 2.17 | [0.409, 0.887] |

**The driftless RW is nested inside the Ridge model** (all betas and the intercept at
zero), and in that case DM is known to be undersized — its null distribution is
non-standard. Clark-West is the right test, and it is the one to quote. The
distinction is not cosmetic: at h=12 DM says p=0.076 and CW says p=0.015. Both tests
use a Bartlett HAC variance with bandwidth h−1, because monthly origins with h-month
horizons make consecutive folds overlap by construction; DM additionally carries the
Harvey-Leybourne-Newbold small-sample correction.

The bootstrap CI is a moving-block bootstrap with block length h (the overlap), 5000
draws. **Its upper bound is below 1 at every horizon**, which is the cleanest single
statement of the result: even at 12 months, where the CI is widest, the interval runs
[0.41, 0.89].

### Robustness: expanding window

Same folds, training window expanding from the start of the sample instead of rolling 72.

| h | U (rolling 72m) | U (expanding) |
|---|---|---|
| 3 | 0.593 | 0.592 |
| 6 | 0.579 | 0.583 |
| 9 | 0.584 | 0.592 |
| 12 | 0.601 | 0.595 |

Indistinguishable. The result is not an artifact of the window length, which matters
because the grid note found the best window to be horizon-dependent — that
sensitivity shows up in the *absolute* MSE, not in whether the model beats a random
walk.

λ across the 163 folds: mean 6.30, median 5.11, range 0.010-21.54, only 12 distinct
values (the grid is log-spaced). 37 folds land on the grid floor, 0.010, and they are
**not** contiguous — the selected penalty rises steadily through the sample and then
falls back, by yearly mean of the origin: 0.01 (2012-13), 0.50 (2014), 4.7 (2015),
2.7-6.7 (2016-19), 12.1 → 13.3 → 17.4 (2020-22), 8.8-10.4 (2023-24), 1.06 (2025).
Two readings, and only the first is safe: the walk-forward selection is responding to
something real rather than picking noise (a noise-driven pick would not trend), and the
2020-22 peak is where it asks for the most shrinkage — the same window where the model's
edge is undetectable (below). The 2025 collapse back to the floor sits on 7 folds and
should not be read as a turn.

## Where it fails: 2020-2022

Broken out by the subperiod the forecast **originates** in:

| origins | folds | U 3m | U 6m | U 9m | U 12m | sd of realized 12m move |
|---|---|---|---|---|---|---|
| 2012-01..2015-12 | 48 | 0.543 | 0.487 | 0.486 | 0.481 | 17.60 pp |
| 2016-01..2019-12 | 48 | 0.632 | 0.549 | 0.571 | 0.618 | 14.79 pp |
| **2020-01..2022-12** | 36 | 0.630 | 0.930 | **1.142** | **1.286** | **8.46 pp** |
| 2023-01..2025-07 | 31 | 0.560 | 0.473 | 0.471 | 0.476 | 11.50 pp |

The raw ratio says the model **loses** to the RW at 9 and 12 months in that window.
Two measurements say to state that carefully rather than as a finding:

- **The BRL barely moved net over 12 months there** — sd 8.46 pp against 17.60 in
  2012-2015, mean −1.58 pp against +14.13. The RW's 12m RMSE is flat at ~8.4 across
  all four horizons in that window, i.e. the currency round-tripped. A driftless RW is
  near-optimal against a series that ends where it started, and no model that
  extrapolates fundamentals will match it.
- **36 heavily overlapping folds cannot establish the reversal.** Clark-West on that
  subperiod alone gives p=0.146 at 9m and p=0.240 at 12m — and the CW statistic is
  still *positive* (+1.06, +0.70), meaning that once the benchmark's estimation-noise
  advantage is corrected for, the point estimate still favors the Ridge. The honest
  reading is "in this window the model's edge is not detectable", not "the model was
  worse".

Worst individual folds, all four at 9-12m: origins 2015-09/2015-10 (the model missed
the post-impeachment-crisis reversal, erring +22 to +24 pp) and 2019-10 (missed a
+36.6 pp realized move, erring −22.8 pp).

## What carries the result: channel ablations

All four variants scored on the **same 163 origins** (the variants have different
natural sample starts, so aligning the fold sets is necessary — without it the
no-`dxy_em` run has 214 folds and the no-channel run 300, and the comparison is
confounded).

| variant | U 3m | U 6m | U 9m | U 12m | CW p at 12m |
|---|---|---|---|---|---|
| 0 channels — PPP offset + AR(1) only | 0.993 | 0.985 | 0.971 | 0.946 | 0.052 |
| 2 channels — fiscal + carry_vol | 0.601 | 0.593 | 0.579 | 0.584 | 0.012 |
| 4 channels — shipped minus dxy_em | 0.600 | 0.597 | 0.581 | 0.594 | 0.013 |
| **5 channels — shipped** | **0.593** | **0.579** | **0.584** | **0.601** | **0.015** |

Two readings, and the second one is a finding about the shipped model rather than
about this test:

- **Without channels the model does not beat the random walk.** U ≈ 0.95-0.99, R²
  negative at every horizon, CW not significant. So the result is *not* the inflation
  drift wearing a regression's clothes — which was the live alternative hypothesis,
  since the PPP offset is pinned at 1 and supplies a trend by construction. It is
  information in the channels.
- **`fiscal` + `carry_vol` deliver the entire result.** Adding sp500, icbr_usd and
  dxy_em on top moves U by less than 0.02 at every horizon, in both directions. Three
  of the five shipped channels pay nothing out of sample under this metric. That is
  worth a separate look before it is acted on — a channel can be worth keeping for a
  scenario tool even if it adds no unconditional accuracy, since the tab's purpose is
  letting a user push a specific channel and read the consequence.

### A leak I suspected, measured, and dismissed

`dxy_em` is FRED's `DTWEXEMEGS`, the Fed's trade-weighted broad EM dollar index —
**which has the BRL in its own basket**. Handing the model realized `dxy_em` therefore
hands it a small direct read on the realized answer, which would make part of the win
mechanical rather than economic. The channel is also the second most correlated
with `delta_fx` (+0.708, β=1.71, t=15.7, univariate R²=0.50), so the concern was not
idle.

Measured on the aligned folds it is not what drives the result: dropping the channel
moves U from 0.593→0.600 at 3m and 0.601→0.594 at 12m — in opposite directions, both
inside noise. Worth recording as a measured null, since the reasoning that motivates
the check is sound and will recur for any index-valued channel.

## The binding caveat: the channels are themselves random walks

This is the limit that decides how the result can be used, and it is the reason the
headline number should never be quoted without it.

Theil U of an AR(1) fit on **each channel's own** history (rolling 72m, same 163
origins, same cumulative-h-month metric — so directly comparable to the FX numbers
above). U ≥ 1 means the series is not forecastable from its own past at all.

| series | U 3m | U 6m | U 9m | U 12m | corr with `delta_fx` |
|---|---|---|---|---|---|
| fiscal (CDS) | **1.044** | **1.078** | **1.116** | **1.147** | +0.710 |
| dxy_em | 1.022 | 1.035 | 1.046 | 1.050 | +0.708 |
| carry_vol | 1.014 | 1.047 | 1.062 | 1.088 | −0.295 |
| icbr_usd | 1.020 | 1.048 | 1.065 | 1.093 | −0.403 |
| sp500 | 0.946 | 0.890 | 0.864 | 0.833 | −0.428 |
| **ppp (inflation differential)** | **0.714** | **0.682** | **0.632** | **0.611** | +0.173 |
| *delta_fx itself, for scale* | 1.009 | 1.011 | 1.015 | 1.012 | — |

Only the inflation differential is genuinely forecastable. And the two channels that
carry the entire result — `fiscal` and `carry_vol`, per the ablation above — are among
the **least** forecastable of the six: Brazil's CDS is *harder* to predict from its own
past than the exchange rate is.

So the conditional premise is not a mild simplification here, it is where the whole
difficulty went. **This test says the model translates a fundamentals path into an FX
path well. It does not say the model forecasts the exchange rate**, and nothing in it
contradicts Meese-Rogoff: an unconditional version, where the channels' own futures
also have to be guessed, would be a different test and should be expected to lose.

The legitimate use of these numbers is as the error ruler for the FX Model tab's
**conditional scenarios** — "if CDS goes to 250, where does the currency go, and
±how much" — which is what that tab already does. They are not a forecasting track
record.

## Not tested

- **Unconditional forecast.** The obvious complement, and the one that would answer
  whether any of this survives having to project the channels. Not run.
- **Whether the 5→2 channel cut should be made.** The ablation shows three channels
  add no unconditional accuracy on these 163 origins; it does not show they are
  useless for the scenario tool, and it was measured on one window/horizon design.
- **Anything about the *level* forecast beyond 12 months**, and any origin after
  2025-07 (each fold needs 12 realized future months).
- **Per-fold detail is not preserved in the repo**, matching the grid note's own
  convention — the harness lived in the session scratchpad. Reproducing it needs:
  `forecast_error_bands_w72()`'s fold loop with the scoring changed from per-step
  level error to cumulative h-month log return, plus the two benchmarks and the
  Clark-West/bootstrap machinery described under Design. Everything needed to rebuild
  it is in this note; the script itself was not committed.
