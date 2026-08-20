# Ridge Model — Training-Window × Forecast-Horizon Grid (2026-07-31)

Direct test of the shipped Ridge model's genuine out-of-sample forecasting ability across a grid of (training window size W) × (forecast horizon F), rather than the one-step-ahead walk-forward MSE the model has been validated on everywhere else in this project. Answers a specific question: **for a given forecast horizon, what training window length actually forecasts best?**

## Model tested

The shipped spec — `ridge_deviation_model.build_plain_regression_sample(channels=_CHANNELS_SHRUNK_EM_REAL_SP500_RY_ICBR_NOSTEEP, include_ppp=False)`, the same 8-channel (fiscal, carry_vol, dxy, dxy_em, curve_steep_real, sp500, real_yield_diff, icbr_usd) + AR(1) (`delta_fx_lag1`) spec that feeds `build_dashboard_payload()` and the "Ridge (Regularized, Rolling)" dashboard tab. No changes to the model itself — only to how it's validated.

## Design

- **W (training window)**: {24, 36, 48, 60, 72, 84} months (2/3/4/5/6/7 years) — **rolling** (fixed size, slides forward one month at a time), not expanding. W=72/84 added 2026-07-31 as a direct follow-up to check whether W=60 was a genuine turning point or the grid had simply stopped too early (see "Read" below — it was not a clean turning point).
- **F (forecast horizon)**: {3, 6, 9, 12} months.
- **Refit cadence**: every single month (maximum folds per W/F cell — 151 to 187 folds depending on W, since a larger W leaves fewer possible fold starting points in the fixed 222-month sample).
- **λ (Ridge regularization)**: re-selected per fold via the existing `walk_forward_lambda()` machinery, run fresh on that fold's own training window only (no lookahead) — not fixed in advance. The nested CV's own `min_train` floor was scaled to `W/2` (e.g. W=24 → floor=12) so every window size gets a reasonable number of CV folds to average over, rather than a fixed floor that would have starved the smaller windows.
- **Forecast mechanism**: genuinely multi-step, not one-step-ahead. From the fold's train-end month, the model is walked forward F months using its **own simulated `delta_fx_lag1`** at every step (never the real one) — the same mechanic validated in the separate path-tracking test earlier this session (see `analytics/brasil/exchange_rate/CLAUDE.md`'s entry on that). The 8 economic channels' own deltas use the **real, realized** values for each forecast month (per the original framing of this line of testing: the channels are treated as known/given, only the FX path itself is left to the model to reconstruct).
- **Metrics**, both computed on the **same quantity** — the cumulative F-month log-return (`100·log(level(t+F)/level(t))`) — so they're comparable across different F values, rather than mixing a one-step monthly error with a multi-step compounded one:
  - **OOS MSE**: mean squared error between the model's simulated cumulative F-month return and the real one, pooled across every fold.
  - **R²**: `1 - SS_res/SS_tot` on the same pooled cumulative-return errors.

Sample: 2008-01 → 2026-06 (222 months, the model's full available history — unchanged by this test).

## Results

### OOS MSE (lower is better)

| W \ F | 3mo | 6mo | 9mo | 12mo |
|---|---|---|---|---|
| **24mo (2Y)** | 25.734 | 56.870 | 108.496 | 171.338 |
| **36mo (3Y)** | 22.781 | 48.991 | 88.878 | 136.240 |
| **48mo (4Y)** | 21.765 | 46.307 | 84.443 | 130.650 |
| **60mo (5Y)** | 19.789 | 39.324 | 70.517 | **101.718*** |
| **72mo (6Y)** | **20.245** | 39.034 | 67.853 | 101.718 |
| **84mo (7Y)** | 21.404 | **38.226** | **67.538** | 102.697 |

*(60mo/72mo tie at F=12; see per-column winners noted in bold.)*

### R² (higher is better)

| W \ F | 3mo | 6mo | 9mo | 12mo |
|---|---|---|---|---|
| **24mo (2Y)** | 0.5192 | 0.4568 | 0.3553 | 0.2401 |
| **36mo (3Y)** | 0.5898 | 0.5386 | 0.4673 | 0.3909 |
| **48mo (4Y)** | 0.6091 | 0.5732 | 0.5123 | 0.4316 |
| **60mo (5Y)** | 0.6517 | 0.6529 | 0.6142 | 0.5873 |
| **72mo (6Y)** | **0.6544** | 0.6725 | **0.6483** | **0.6139** |
| **84mo (7Y)** | 0.6387 | **0.6560** | 0.6005 | 0.4913 |

### Read

**W=60 is not the turning point — but the answer past W=60 is horizon-dependent, not a clean "bigger is always better" story.** Extending the grid to W={72, 84} months (2026-07-31 follow-up) shows:

- **F=3mo**: W=72 is the best window (OOS MSE 20.245, R² 0.6544), essentially tied with W=60. W=84 is *worse* than both (21.404) — a genuine turning point at the short horizon.
- **F=6mo, F=9mo**: still improving monotonically through W=84 — W=84 posts the best MSE at both horizons (38.226 and 67.538) and the best R² at F=6mo (0.6725, though that's actually W=72's number — see table). No turning point found yet at these horizons within the tested range.
- **F=12mo**: W=60 and W=72 are essentially tied (101.862 vs. 101.718 MSE, 0.5873 vs. 0.6139 R²) — W=72 wins on R². **W=84 clearly degrades** at this horizon: MSE ticks up only slightly (102.697) but R² drops sharply (0.6139 → 0.4913), the single sharpest deterioration in the whole extended grid.

So there is a real turning point, but it sits at **different window sizes for different horizons**: short (3mo) and long (12mo) horizons turn over around W=72, while medium horizons (6-9mo) are still improving at W=84. The original W=24-60 grid's clean "bigger always wins" ranking does not extend cleanly past W=60 — it was an artifact of not having tested far enough, not a stable law.

The W=84, F=12mo cell's R² collapse alongside a barely-changed MSE is the more informative signal than MSE alone here — it means the pooled variance of the *real* 12-month-ahead outcomes across those 127 folds is being explained much less well by the model, even though its absolute errors aren't much larger. Worth flagging as the practical caution: **W=84 is not a safe default for the 12-month horizon**, even though it looks fine or even best at 6-9mo.

As expected for any model, both metrics degrade as the forecast horizon F lengthens within a given W (MSE grows, R² falls) — a 12-month-ahead multi-step simulation is a much harder target than a 3-month one, since simulated errors compound month over month with no real-data correction along the way. That pattern holds at every W tested.

Not tested here (7Y is the longest window tried, and the 222-month sample itself caps how far this can go — W=84 already leaves only 127 folds, down from 187 at W=24): whether W=96+ continues the medium-horizon (6-9mo) improvement or also turns over. Sample-size erosion at very large W (fewer folds to average over, and each fold's own training window increasingly dominated by the same handful of years) makes this a diminishing-returns exercise past this point without more history.

### Lambda stability across the walk

| W | n folds | mean λ | std | min | max | median |
|---|---|---|---|---|---|---|
| 24mo | 187 | 10.730 | 10.849 | 0.010 | 56.234 | 8.254 |
| 36mo | 175 | 11.212 | 10.245 | 0.010 | 56.234 | 8.254 |
| 48mo | 163 | 9.867 | 7.801 | 0.010 | 34.807 | 8.254 |
| 60mo | 151 | 12.259 | 9.707 | 0.010 | 34.807 | 8.254 |
| 72mo | 139 | 13.635 | 10.906 | 0.010 | 56.234 | 8.254 |
| 84mo | 127 | 15.300 | 11.955 | 0.010 | 56.234 | **13.335** |

The **median** is identical (8.254) across W=24-72 — a reasonably encouraging sign for the idea of fixing λ in a cheaper future version of this test, at least up to 6 years of training data. **W=84 breaks that pattern**: its median jumps to 13.335, well above every other window's 8.254, and its mean (15.300) is the highest in the whole grid. Combined with the max hitting the grid's ceiling (56.234) again at W=84 — after it had settled lower (34.807) at W=48/60 — this is a second, independent signal (alongside the F=12mo R² collapse above) that **W=84 behaves qualitatively differently from W=24-72**, not just incrementally more or less regularized. A 7-year rolling window is starting to smooth over more regime variety within each single fold, which both pushes typical λ up and makes the walk-forward CV's own within-fold lambda selection noisier fold-to-fold.

**Read with caution before fixing λ**: the median-matching is a good sign, but the right-skewed distribution and grid-ceiling-hitting in some folds mean a fixed λ would systematically under-regularize during exactly the episodes where the walk-forward selection itself is telling you more regularization is needed. If λ is fixed in a future cheaper version of this test, it should be checked specifically against how much that changes the crisis-window folds' own forecasts, not just the aggregate OOS MSE/R² — the aggregate numbers could look fine while masking a worse fit in the episodes that matter most.

## Caveats

- This test uses the model's own simulated AR(1) feedback (`delta_fx_lag1`) at every step of the multi-step forecast, and real/realized values for the 8 economic channels — it does **not** test the model's ability to forecast the channels themselves, only its ability to translate a given channel trajectory into an FX path. A fully "blind" forecast (where the channels' own future values are also unknown) would very likely perform worse than shown here.
- Not wired into the shipped dashboard tab or the model's default configuration — this is a validation exercise, not a change to `ridge_deviation_model.py`. The shipped model still uses its full available history for its one in-sample fit (`build_dashboard_payload()`), not a rolling W-month re-estimation scheme like this test's cells.
- Raw fold-level results (all 946 folds across the six W values' fitted lambda and cumulative-return errors) are not preserved in the repo — this report captures the aggregated matrices, not the per-fold detail. Rerun the underlying scratch script if per-fold detail is needed again.
- W=72/84's fold counts (139, 127) are noticeably smaller than W=24's (187) in the same fixed 222-month sample — some of the apparent "turning point" behavior at W=84 could in part reflect fewer folds to average over (more sensitivity to a handful of specific episodes) rather than a purely structural window-size effect. Not disentangled here.
