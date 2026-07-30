"""
Ridge-penalized, rolling-window deviation model (2026-07-30) -- the "modelo
proposto" from the same-day design note: keeps the dependent variable and
channel set already used elsewhere in this dashboard (delta_dev, channels in
z-score) but swaps the estimator for Ridge (L2 penalty), re-estimated
periodically on a rolling window so the coefficients can track regime change
rather than describing one average relationship across calm and crisis
periods.

    delta_dev(t) = alpha + sum(beta_c * z(delta_channel_c(t))) + eps(t),
    estimated by Ridge:  min sum(erro)^2 + lambda * sum(beta_c^2)

Started with two channels only (fiscal, DXY), by explicit user choice ("run
it with (i) fiscal and (ii) global USD (DXY). We increment later"). Grown
2026-07-30, same day, in two further rounds:
  - to six: carry, relative_carry, carry_vol, relative_carry_vol added
    alongside fiscal/DXY, all at once rather than one at a time -- direct
    user call, and the whole reason this model uses Ridge (L2) rather than
    OLS/Lasso in the first place (see below): the four carry variants are
    deliberately overlapping constructions of the same underlying signal
    (bilateral vs. relative-to-peers, raw vs. vol-adjusted), so a Ridge fit
    lets them share credit and reveals how they interact (e.g.
    bayesian_deviation_model.py already found that adding relative_carry
    alongside carry sharpens carry's own estimate once the peer component
    is partialled out -- an interaction only visible in a joint fit, not
    from testing each channel in its own separate univariate spec).
  - to eight: breakeven_gap (the breakeven-minus-CMN-target de-anchoring
    gap) and tot (terms of trade) added, same day, direct user request.
Reuses bayesian_deviation_model.py's
build_deltas_contemporaneous()/_standardize_ext() (2000-01+ reference
window) so the z-scored deltas here are identical, channel for channel, to
what primary_contemp already uses -- only the estimator and the
re-estimation scheme are new.

Three design choices, per the proposal:
  - L2 (Ridge), not L1 (Lasso): the goal is stabilizing coefficients between
    correlated channels, not zeroing any of them out -- collinearity isn't
    yet the live concern it will be once more channels are added, but the
    module is meant to grow into that.
  - lambda (regularization strength) is NOT fixed arbitrarily -- chosen by
    walk-forward temporal cross-validation: fit on an expanding window,
    score one step ahead (never used for fitting), walk forward across the
    whole history, and pick the lambda with the best average out-of-sample
    squared error.
  - Re-estimated on a rolling window (60 months, the same window
    beer_model.py's rolling_fit() uses) -- Ridge alone fixes collinearity,
    not regime change; a single whole-sample Ridge fit would still describe
    one average relationship between calm and crisis periods.

No posterior/HDI anywhere in this module -- Ridge is a point estimate, not a
Bayesian fit, so there's no distribution to summarize beyond the coefficient
itself (unlike every PyMC-based model elsewhere in this package).

Impulse-decay / lag structure (added 2026-07-30, same day, direct user
request): the contemporaneous-only spec above assumes a channel's shock
affects deviation only in the month it happens. The user's own observation
-- "a shock in interest rate have impact a continuing impact over the fx,
we do not capture it" -- pointed at two ways to add persistence: (1) a
single shared AR term (phi, deviation(t-1), the mechanism state_space_model.py
already uses), or (2) an explicit per-channel lag structure. Chosen: (2),
because (1)'s single phi forces EVERY channel to decay at the identical
rate -- verified directly: unrolling deviation(t)=phi*deviation(t-1)+beta_c*z_c(t)
for a one-time shock gives impulse response phi^k * beta_c at horizon k, so
phi sets a common decay SPEED for the whole system and beta_c only scales
its SIZE. A per-channel lag structure (z_c(t), z_c(t-1), ..., z_c(t-5), each
with its own beta) lets different channels decay at genuinely different
speeds, which is what the user was actually asking whether the model could
show. build_lagged_sample()/fit_lag_structure()/build_lag_dashboard_payload()
implement this as max_lag=6 months per channel (user's choice), fit via the
same Ridge + walk-forward-CV-for-lambda machinery as the rest of this module
-- WHOLE SAMPLE ONLY, no rolling window, also the user's own call once the
arithmetic was laid out: 8 channels x 6 lags = 48 regressors + alpha, and a
60-month rolling window would leave only ~11 degrees of freedom per window,
unreliable even under Ridge's penalty; a rolling window wide enough to be
comfortable (150+ months) would only yield a handful of windows across the
~220-month sample anyway, not enough to say anything about regime change.

Carry-in-level variant (added 2026-07-30, same day, direct user request "Run
with the carry in level"): an exploratory alternate spec, not wired into the
dashboard tab -- same role bayesian_deviation_model.py's own extra specs
(primary_gap, primary_studentt, robustness) play there, printed/compared but
not all promoted to a tab. Every channel except carry keeps its own
contemporaneous DELTA as in the main spec; carry alone is replaced by its raw
LEVEL (z-scored against the same 2000-01+ reference window), i.e. the nominal
BR-US policy rate differential itself (diferenciais_juros.diferencial_nominal),
not its month-to-month change. Motivation: a level regressor is the
parsimonious alternative to the lag structure above for capturing "a shock
has continuing impact" -- with delta_carry, a persistently high (but no
longer RISING) carry contributes nothing to delta_dev after the month it
stopped changing; with carry_level, a persistently high carry keeps pulling
delta_dev every single month for as long as the level stays high, with no
extra lag terms needed. build_sample_carry_level()/run_carry_level_variant()
implement this; reuses walk_forward_lambda()/fit_whole_sample()/rolling_fit()
unchanged, since none of those three assume anything about a column's name
beyond it being present in the sample.

Usage:
    uv run python -c "from analytics.exchange_rate.models.ridge_deviation_model import run; run()"
    uv run python -c "from analytics.exchange_rate.models.ridge_deviation_model import run_carry_level_variant; run_carry_level_variant()"
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge

from analytics.exchange_rate.models.bayesian_deviation_model import (
    _REFERENCE_START,
    _standardize_ext,
    build_deltas_contemporaneous,
)
from analytics.exchange_rate.models.ppp_equilibrium import compute_deviation, compute_equilibrium, load_data

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

_RESULTS_DIR = Path(__file__).parent / "ridge_results"

# Started as ["fiscal", "dxy"], grown same day to the four carry variants,
# then to breakeven_gap + tot (see module docstring for the two rounds).
# All eight already exist as delta_<channel> columns in
# build_deltas_contemporaneous().
_CHANNELS = ["fiscal", "dxy", "carry", "relative_carry", "carry_vol", "relative_carry_vol", "breakeven_gap", "tot"]

_LAMBDA_GRID = np.logspace(-2, 3, 25)  # 0.01 .. 1000, log-spaced

# Shrunk AR(1) spec (2026-07-30, direct user request): a + AR(t-1) +
# fiscal(t) + carry_vol(t) + dxy(t) + curve_steep(t) -- 4 channels instead
# of 8, curve_steep (BR nominal 10Y-2Y yield-curve steepening,
# ppp_equilibrium._load_curve_steepening()) tested as an alternate,
# market-based fiscal-risk proxy alongside the CDS-based `fiscal` channel,
# not in place of it. Exploratory only -- run via run_shrunk_ar1_variant(),
# NOT wired into build_dashboard_payload()/the dashboard tab, per direct
# user instruction ("do not include in the dashboard yet, let's test").
_CHANNELS_SHRUNK = ["fiscal", "carry_vol", "dxy", "curve_steep"]

# Lag structure (impulse-decay analysis) -- 6 months per channel, user's
# choice. min_train raised to 72 (vs. 36 for the contemporaneous-only spec
# above) specifically for this wider design: 8 channels x 6 lags = 48
# regressors, so the first few folds of a 36-month floor would be fitting
# more parameters than observations -- Ridge handles that numerically, but
# the resulting OOS score wouldn't be trustworthy this early.
_MAX_LAG = 6
_LAG_MIN_TRAIN = 72


def build_sample(df: pd.DataFrame | None = None, channels: list[str] | None = None) -> tuple[pd.DataFrame, dict]:
    """delta_dev plus each channel's z-scored CONTEMPORANEOUS delta,
    standardized against the same 2000-01+ reference window
    bayesian_deviation_model.py's primary_contemp spec uses (not this
    model's own narrower fitting-sample overlap) -- so a coefficient here
    stays comparable to that spec's if the two are ever set side by side."""
    channels = _CHANNELS if channels is None else channels
    df = load_data() if df is None else df
    delta_cols = [f"delta_{c}" for c in channels]
    deltas = build_deltas_contemporaneous(df)
    sample = deltas[["delta_dev"] + delta_cols].dropna()
    reference = deltas[deltas.index >= _REFERENCE_START]
    z, stats = _standardize_ext(sample, reference, delta_cols)
    z["delta_dev"] = sample["delta_dev"]
    return z, stats


def build_ar1_sample(df: pd.DataFrame | None = None,
                      channels: list[str] | None = None) -> tuple[pd.DataFrame, dict, list[str]]:
    """delta_dev(t) regressed on ITS OWN lag, delta_dev(t-1), plus every
    channel's contemporaneous z-scored delta (no per-channel lags) -- tests
    persistence option (1) from the module docstring (a single shared AR
    term) instead of option (2) (the per-channel 6-lag structure), which
    compare_lag_depths() showed does NOT survive walk-forward out-of-sample
    validation (OOS MSE rose monotonically with every added lag, depth 1
    was the best of 1-6). delta_dev_lag1 is kept in RAW units, not
    z-scored, alongside the standardized channels -- same raw_cols
    rationale bayesian_deviation_model.py's fit_ecm_spec() uses for
    deviation_lag1: standardizing a lagged-dependent-variable term would
    obscure phi's direct reading as "fraction of last month's change
    carried into this one," the whole point of testing it."""
    channels = _CHANNELS if channels is None else channels
    df = load_data() if df is None else df
    delta_cols = [f"delta_{c}" for c in channels]
    deltas = build_deltas_contemporaneous(df)

    sample = deltas[["delta_dev"] + delta_cols].copy()
    sample["delta_dev_lag1"] = deltas["delta_dev"].shift(1)
    sample = sample.dropna()

    reference = deltas[deltas.index >= _REFERENCE_START]
    z, stats = _standardize_ext(sample, reference, delta_cols)
    z["delta_dev_lag1"] = sample["delta_dev_lag1"]
    stats["delta_dev_lag1"] = (0.0, 1.0)  # identity -- kept in native units, not standardized
    z["delta_dev"] = sample["delta_dev"]

    reg_cols = delta_cols + ["delta_dev_lag1"]
    return z, stats, reg_cols


def run_ar1_variant(channels: list[str] | None = None, window: int = 60, label: str = "ar1") -> dict:
    """Fits and prints the AR(1) spec on build_ar1_sample() -- same
    walk-forward-lambda / whole-sample / rolling-fit sequence as run(),
    generic over `channels` so it also covers the shrunk 4-channel spec
    (channels=_CHANNELS_SHRUNK, label="ar1_shrunk") as well as the full
    8-channel one. Exploratory, not wired into build_dashboard_payload()."""
    channels = _CHANNELS if channels is None else channels
    z, stats, reg_cols = build_ar1_sample(channels=channels)

    print("=" * 78)
    print(f"RIDGE DEVIATION MODEL -- AR(1) VARIANT, channels={channels}")
    print("(delta_dev_lag1, raw units, plus each channel's own contemporaneous z-scored delta)")
    cv = walk_forward_lambda(z, reg_cols)
    lam = float(cv.iloc[0]["lambda"])
    print(cv.head(10).to_string(index=False))
    print(f"Selected lambda = {lam:.4f} (mean OOS MSE = {cv.iloc[0]['mse']:.4f})")

    whole = fit_whole_sample(z, reg_cols, lam)
    print("=" * 78)
    betas_fmt = {c: round(b, 4) for c, b in whole["beta"].items()}
    print(f"Whole-sample fit at lambda={lam:.4f}: alpha={whole['alpha']:+.4f}  "
          f"betas={betas_fmt}  R2={whole['r2']:.4f}  n={whole['n']}")

    roll = rolling_fit(z, reg_cols, lam, window=window)
    print("=" * 78)
    print(f"Rolling fit: {len(roll)} windows of {window} months, lambda={lam:.4f}")
    print(roll[[f"beta_{c}" for c in reg_cols] + ["r2"]].describe())

    _RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    cv.to_csv(_RESULTS_DIR / f"{label}_lambda_cv.csv", index=False)
    roll.reset_index().to_csv(_RESULTS_DIR / f"{label}_rolling.csv", index=False)
    pd.DataFrame([{"lambda": lam, "alpha": whole["alpha"], "r2": whole["r2"], "n": whole["n"],
                    **{f"beta_{c}": b for c, b in whole["beta"].items()}}]).to_csv(
        _RESULTS_DIR / f"{label}_whole_sample.csv", index=False)

    return {
        "channels": channels, "reg_cols": reg_cols, "lambda": lam, "cv": cv,
        "whole_sample": whole, "rolling": roll, "z": z, "stats": stats,
    }


def build_plain_regression_sample(df: pd.DataFrame | None = None,
                                   channels: list[str] | None = None,
                                   include_ppp: bool = True) -> tuple[pd.DataFrame, dict, list[str]]:
    """A genuinely different model from every other spec in this module --
    direct user request ("instead of considering the ppp as equilibrium,
    incorporate it in the regression as a channel... rerun without
    considering the deviation stuff, just the regression"). Every other
    spec here regresses delta_dev = 100*diff(log(ptax/equilibrium)), which
    FORCES a coefficient of exactly 1 on PPP's own implied move (ptax and
    equilibrium are subtracted in log space before anything is estimated).
    This one instead regresses the exchange rate's own log return directly
    --

        delta_fx(t) = 100*diff(log(ptax(t)))

    -- on PPP as ONE MORE CHANNEL alongside the others, with its
    coefficient freely estimated by Ridge instead of assumed: delta_ppp(t)
    = 100*diff(log(ipca_index(t)) - log(cpi_index(t))), the BR-US relative
    inflation differential for that month (exactly what compute_equilibrium()
    assumes moves the exchange rate 1-for-1; no base month needed here at
    all, since diff() cancels whatever constant a base month would
    otherwise introduce -- same base-month-invariance argument as the
    "base-month digression" earlier this session, just applied from the
    other direction). No compute_deviation()/compute_equilibrium() call
    anywhere in this function. delta_fx_lag1 (AR(1) on the exchange rate's
    own return, not delta_dev's) is kept raw/unstandardized, same
    convention as delta_dev_lag1 elsewhere. channels defaults to
    _CHANNELS_SHRUNK (fiscal, carry_vol, dxy, curve_steep) -- the same 4
    already shown to carry real signal in the deviation framework;
    swapping the dependent variable is the test here, not the channel set.

    include_ppp=False (2026-07-30, direct user follow-up "Remove the ppp
    entirely, let the alfa capture it") drops delta_ppp from the
    regressors altogether -- its whole-sample coefficient (+0.34) had
    already shown up as unstable in the rolling read (mean +0.04, ranging
    -0.86 to +1.48), so rather than keep a channel whose sign/size isn't
    trustworthy, PPP's average contribution (mostly just Brazil's average
    inflation being higher than the US's, a near-constant monthly drift
    over an 18-year sample) is left for alpha to absorb, same as every
    other spec in this file that doesn't have its own explicit PPP term."""
    channels = _CHANNELS_SHRUNK if channels is None else channels
    df = load_data() if df is None else df

    out = pd.DataFrame(index=df.index)
    out["delta_fx"] = 100 * np.log(df["ptax"]).diff()
    if include_ppp:
        out["delta_ppp"] = 100 * (np.log(df["ipca_index"]) - np.log(df["cpi_index"])).diff()
    for c in channels:
        out[f"delta_{c}"] = df[c].diff()
    out["delta_fx_lag1"] = out["delta_fx"].shift(1)

    sample = out.dropna()
    standardize_cols = (["delta_ppp"] if include_ppp else []) + [f"delta_{c}" for c in channels]
    reference = out[out.index >= _REFERENCE_START]
    z, stats = _standardize_ext(sample, reference, standardize_cols)
    z["delta_fx_lag1"] = sample["delta_fx_lag1"]
    stats["delta_fx_lag1"] = (0.0, 1.0)  # identity -- kept in native units, not standardized
    z["delta_fx"] = sample["delta_fx"]

    reg_cols = standardize_cols + ["delta_fx_lag1"]
    return z, stats, reg_cols


def run_plain_regression_variant(channels: list[str] | None = None, window: int = 60,
                                  label: str = "plain_regression", include_ppp: bool = True) -> dict:
    """Fits and prints build_plain_regression_sample()'s spec -- same
    walk-forward-lambda / whole-sample / rolling-fit sequence as the other
    run_*_variant() functions, with y_col="delta_fx" since the dependent
    variable here isn't delta_dev at all."""
    channels = _CHANNELS_SHRUNK if channels is None else channels
    z, stats, reg_cols = build_plain_regression_sample(channels=channels, include_ppp=include_ppp)

    print("=" * 78)
    print(f"RIDGE MODEL -- PLAIN REGRESSION ({'PPP as a channel' if include_ppp else 'PPP dropped, alpha absorbs it'}, not equilibrium), channels={channels}")
    print("delta_fx(t) = 100*diff(log(ptax)) ~ " + ("delta_ppp + " if include_ppp else "") + "channels + delta_fx_lag1 -- no compute_deviation()/compute_equilibrium() involved")
    cv = walk_forward_lambda(z, reg_cols, y_col="delta_fx")
    lam = float(cv.iloc[0]["lambda"])
    print(cv.head(10).to_string(index=False))
    print(f"Selected lambda = {lam:.4f} (mean OOS MSE = {cv.iloc[0]['mse']:.4f})")

    whole = fit_whole_sample(z, reg_cols, lam, y_col="delta_fx")
    print("=" * 78)
    betas_fmt = {c: round(b, 4) for c, b in whole["beta"].items()}
    print(f"Whole-sample fit at lambda={lam:.4f}: alpha={whole['alpha']:+.4f}  "
          f"betas={betas_fmt}  R2={whole['r2']:.4f}  n={whole['n']}")

    roll = rolling_fit(z, reg_cols, lam, window=window, y_col="delta_fx")
    print("=" * 78)
    print(f"Rolling fit: {len(roll)} windows of {window} months, lambda={lam:.4f}")
    print(roll[[f"beta_{c}" for c in reg_cols] + ["r2"]].describe())

    _RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    cv.to_csv(_RESULTS_DIR / f"{label}_lambda_cv.csv", index=False)
    roll.reset_index().to_csv(_RESULTS_DIR / f"{label}_rolling.csv", index=False)
    pd.DataFrame([{"lambda": lam, "alpha": whole["alpha"], "r2": whole["r2"], "n": whole["n"],
                    **{f"beta_{c}": b for c, b in whole["beta"].items()}}]).to_csv(
        _RESULTS_DIR / f"{label}_whole_sample.csv", index=False)

    return {
        "channels": channels, "reg_cols": reg_cols, "lambda": lam, "cv": cv,
        "whole_sample": whole, "rolling": roll, "z": z, "stats": stats,
    }


def build_level_sample(df: pd.DataFrame | None = None,
                        channels: list[str] | None = None) -> tuple[pd.DataFrame, dict]:
    """Level-space counterpart to build_sample(): the dependent variable is
    deviation(t) ITSELF (column "dev"), not delta_dev(t), and every channel
    enters as its own z-scored LEVEL (df[c]) rather than a delta -- direct
    user request ("run the model in level not difference") after the
    lag-structure/AR(1) work above, to see what the same Ridge/walk-forward-
    CV/rolling machinery finds against the untransformed series.

    Flagged deliberately, not just here but in CLAUDE.md: per
    bayesian_deviation_model.py's own pre-registered ADF/KPSS check,
    `deviation`, `carry`, and `tot` all test as I(1) (unit root) while
    `breakeven`/`fiscal` test as I(0) -- regressing a level, I(1) dependent
    variable on a mix of level regressors (some I(1)) is the textbook
    spurious-regression setup, which is the exact reason this whole module
    (and bayesian_deviation_model.py before it) works in first differences
    everywhere else. This function exists to show what that risk actually
    produces on this channel set, not to argue any resulting R2 is real
    explanatory power.

    Reuses walk_forward_lambda()/fit_whole_sample()/rolling_fit() via their
    y_col="dev" override -- same reference-window standardization (2000-01+)
    as every other variant in this module, just applied to df[c] instead of
    delta_c."""
    channels = _CHANNELS if channels is None else channels
    df = load_data() if df is None else df
    dev = compute_deviation(df)

    sample = pd.DataFrame(index=df.index)
    sample["dev"] = dev
    for c in channels:
        sample[c] = df[c]
    sample = sample.dropna()

    reference = sample[sample.index >= _REFERENCE_START]
    z, stats = _standardize_ext(sample, reference, channels)
    z["dev"] = sample["dev"]
    return z, stats


def run_level_variant(window: int = 60) -> dict:
    """Fits and prints the level-space variant -- same walk-forward-lambda /
    whole-sample / rolling-fit sequence as run(), on build_level_sample()'s
    sample (y_col="dev") instead of build_sample()'s (y_col="delta_dev",
    the default)."""
    channels = _CHANNELS
    z, stats = build_level_sample(channels=channels)

    print("=" * 78)
    print(f"RIDGE DEVIATION MODEL -- LEVEL VARIANT (dev ~ channel levels, not deltas), channels={channels}")
    print("WARNING: deviation/carry/tot test as I(1) -- see build_level_sample() docstring, spurious-regression risk")
    cv = walk_forward_lambda(z, channels, y_col="dev")  # default min_train=36, same as the 8-param contemporaneous spec
    lam = float(cv.iloc[0]["lambda"])
    print(cv.head(10).to_string(index=False))
    print(f"Selected lambda = {lam:.4f} (mean OOS MSE = {cv.iloc[0]['mse']:.4f})")

    whole = fit_whole_sample(z, channels, lam, y_col="dev")
    print("=" * 78)
    betas_fmt = {c: round(b, 4) for c, b in whole["beta"].items()}
    print(f"Whole-sample fit at lambda={lam:.4f}: alpha={whole['alpha']:+.4f}  "
          f"betas={betas_fmt}  R2={whole['r2']:.4f}  n={whole['n']}")

    roll = rolling_fit(z, channels, lam, window=window, y_col="dev")
    print("=" * 78)
    print(f"Rolling fit: {len(roll)} windows of {window} months, lambda={lam:.4f}")
    print(roll[[f"beta_{c}" for c in channels] + ["r2"]].describe())

    _RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    cv.to_csv(_RESULTS_DIR / "level_lambda_cv.csv", index=False)
    roll.reset_index().to_csv(_RESULTS_DIR / "level_rolling.csv", index=False)
    pd.DataFrame([{"lambda": lam, "alpha": whole["alpha"], "r2": whole["r2"], "n": whole["n"],
                    **{f"beta_{c}": b for c, b in whole["beta"].items()}}]).to_csv(
        _RESULTS_DIR / "level_whole_sample.csv", index=False)

    return {
        "channels": channels, "lambda": lam, "cv": cv,
        "whole_sample": whole, "rolling": roll, "z": z, "stats": stats,
    }


def build_sample_carry_level(df: pd.DataFrame | None = None,
                              channels: list[str] | None = None) -> tuple[pd.DataFrame, dict, list[str]]:
    """Like build_sample(), except the "carry" channel enters as its own
    z-scored LEVEL (carry_level = z(carry(t))) instead of z(delta_carry(t))
    -- see module docstring for the motivation. Every other channel is
    untouched, still its own contemporaneous delta. Returns (z, stats,
    reg_cols) -- reg_cols is channels' usual delta_<c> list with delta_carry
    swapped out for "carry_level", ready to hand straight to
    walk_forward_lambda()/fit_whole_sample()/rolling_fit() in place of
    delta_cols."""
    channels = _CHANNELS if channels is None else channels
    df = load_data() if df is None else df
    other = [c for c in channels if c != "carry"]
    delta_cols = [f"delta_{c}" for c in other]
    deltas = build_deltas_contemporaneous(df)

    sample = deltas[["delta_dev"] + delta_cols].copy()
    sample["carry_level"] = df["carry"]
    sample = sample.dropna()

    reference = deltas[deltas.index >= _REFERENCE_START][delta_cols].copy()
    reference["carry_level"] = df["carry"]

    reg_cols = delta_cols + ["carry_level"] if "carry" in channels else delta_cols
    z, stats = _standardize_ext(sample, reference, reg_cols)
    z["delta_dev"] = sample["delta_dev"]
    return z, stats, reg_cols


def run_carry_level_variant(window: int = 60) -> dict:
    """Fits and prints the carry-in-level variant side by side with nothing
    else (caller compares its own printed R2/betas against run()'s output) --
    same walk-forward-lambda / whole-sample / rolling-fit sequence as run(),
    just on build_sample_carry_level()'s sample instead of build_sample()'s."""
    channels = _CHANNELS
    z, stats, reg_cols = build_sample_carry_level(channels=channels)

    print("=" * 78)
    print(f"RIDGE DEVIATION MODEL -- CARRY-IN-LEVEL VARIANT, channels={channels}")
    print("(carry enters as z(carry_level(t)), every other channel unchanged: z(delta_c(t)))")
    cv = walk_forward_lambda(z, reg_cols)
    lam = float(cv.iloc[0]["lambda"])
    print(cv.head(10).to_string(index=False))
    print(f"Selected lambda = {lam:.4f} (mean OOS MSE = {cv.iloc[0]['mse']:.4f})")

    whole = fit_whole_sample(z, reg_cols, lam)
    print("=" * 78)
    betas_fmt = {c: round(b, 4) for c, b in whole["beta"].items()}
    print(f"Whole-sample fit at lambda={lam:.4f}: alpha={whole['alpha']:+.4f}  "
          f"betas={betas_fmt}  R2={whole['r2']:.4f}  n={whole['n']}")

    roll = rolling_fit(z, reg_cols, lam, window=window)
    print("=" * 78)
    print(f"Rolling fit: {len(roll)} windows of {window} months, lambda={lam:.4f}")
    print(roll[[f"beta_{c}" for c in reg_cols] + ["r2"]].describe())

    _RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    cv.to_csv(_RESULTS_DIR / "carry_level_lambda_cv.csv", index=False)
    roll.reset_index().to_csv(_RESULTS_DIR / "carry_level_rolling.csv", index=False)
    pd.DataFrame([{"lambda": lam, "alpha": whole["alpha"], "r2": whole["r2"], "n": whole["n"],
                    **{f"beta_{c}": b for c, b in whole["beta"].items()}}]).to_csv(
        _RESULTS_DIR / "carry_level_whole_sample.csv", index=False)

    return {
        "channels": channels, "reg_cols": reg_cols, "lambda": lam, "cv": cv,
        "whole_sample": whole, "rolling": roll, "z": z, "stats": stats,
    }


def build_lagged_sample(df: pd.DataFrame | None = None, channels: list[str] | None = None,
                         max_lag: int = _MAX_LAG) -> tuple[pd.DataFrame, list[str]]:
    """delta_dev plus, for each channel, its own z-scored contemporaneous
    delta shifted by lag 0..max_lag-1 (lag0 = the same z(delta_c(t))
    build_sample() uses; lag_k = z(delta_c(t-k))) -- a distributed-lag
    design letting each channel's effect on Δdeviation decay over several
    months instead of assuming it only matters the month it happens.

    Each channel is standardized ONCE, against the full history (same
    2000-01+ reference window as build_sample()), and every lag is a pure
    shift of that one z-scored series -- so all lags of a channel share one
    mean/std, and only which month's value lands in which row differs.
    Shifting then dropna() loses max_lag-1 extra months at the start of the
    already-lagged sample (on top of whichever channel's own start date is
    already binding), which is why this is a slightly shorter sample than
    build_sample()'s own contemporaneous-only one."""
    channels = _CHANNELS if channels is None else channels
    df = load_data() if df is None else df
    delta_cols = [f"delta_{c}" for c in channels]
    deltas = build_deltas_contemporaneous(df)
    reference = deltas[deltas.index >= _REFERENCE_START]
    z_full, _ = _standardize_ext(deltas, reference, delta_cols)

    out = pd.DataFrame(index=deltas.index)
    out["delta_dev"] = deltas["delta_dev"]
    lag_cols = []
    for dcol in delta_cols:
        for lag in range(max_lag):
            col = f"{dcol}_lag{lag}"
            out[col] = z_full[dcol].shift(lag)
            lag_cols.append(col)
    sample = out.dropna()
    return sample, lag_cols


def fit_lag_structure(channels: list[str] | None = None, max_lag: int = _MAX_LAG) -> dict:
    """Distributed-lag Ridge fit -- WHOLE SAMPLE ONLY, no rolling window (see
    module docstring for why). lambda chosen by the same walk-forward CV as
    the contemporaneous-only spec, refit specifically for this wider design
    (_LAG_MIN_TRAIN, not the shorter floor used above)."""
    channels = _CHANNELS if channels is None else channels
    sample, lag_cols = build_lagged_sample(channels=channels, max_lag=max_lag)
    cv = walk_forward_lambda(sample, lag_cols, min_train=_LAG_MIN_TRAIN)
    lam = float(cv.iloc[0]["lambda"])
    whole = fit_whole_sample(sample, lag_cols, lam)
    return {
        "channels": channels, "max_lag": max_lag, "lag_cols": lag_cols,
        "lambda": lam, "cv": cv, "whole_sample": whole, "sample": sample,
    }


def compare_lag_depths(channels: list[str] | None = None, max_lags: list[int] | None = None) -> pd.DataFrame:
    """Answers "do we actually need all 6 lags" directly via walk-forward OOS
    error, rather than eyeballing coefficient sizes off a single max_lag=6
    fit: refits the lag structure at every candidate depth (default 1..6),
    each with its OWN walk-forward-selected lambda (a deeper design needs
    more regularization, so reusing max_lag=6's lambda at a shallower depth
    would bias the comparison), and reports that depth's best OOS MSE
    alongside its whole-sample R2. Every depth's sample is restricted to the
    deepest depth's own date range first (`common_index` below) so every row
    is scored on the exact same set of held-out months -- otherwise a
    shallower depth's walk-forward fold count/date range would differ
    (fewer leading months lost to the lag shift), making the MSEs not
    comparable. If R2 keeps climbing with depth but OOS MSE flattens or
    turns back up, the extra lags are fitting in-sample noise, not adding
    real predictive value -- Ridge's L2 penalty shrinks a useless lag
    toward zero but never all the way to it, so R2 alone can't tell the two
    apart the way OOS error does."""
    channels = _CHANNELS if channels is None else channels
    max_lags = list(range(1, _MAX_LAG + 1)) if max_lags is None else max_lags

    samples, lag_cols_map = {}, {}
    for ml in max_lags:
        sample, lag_cols = build_lagged_sample(channels=channels, max_lag=ml)
        samples[ml] = sample
        lag_cols_map[ml] = lag_cols
    common_index = samples[max(max_lags)].index

    rows = []
    for ml in max_lags:
        sample = samples[ml].loc[common_index]
        lag_cols = lag_cols_map[ml]
        cv = walk_forward_lambda(sample, lag_cols, min_train=_LAG_MIN_TRAIN)
        lam = float(cv.iloc[0]["lambda"])
        oos_mse = float(cv.iloc[0]["mse"])
        whole = fit_whole_sample(sample, lag_cols, lam)
        rows.append({
            "max_lag": ml, "n_params": len(lag_cols), "lambda": lam,
            "oos_mse": oos_mse, "r2": whole["r2"], "n": whole["n"],
        })
    return pd.DataFrame(rows)


def build_lag_dashboard_payload(channels: list[str] | None = None, max_lag: int = _MAX_LAG) -> dict:
    """Reshapes fit_lag_structure()'s flat beta dict into one array of
    max_lag coefficients per channel, for the "Impulse Decay by Channel"
    chart -- index 0 is the contemporaneous effect, index k is the effect
    of a shock k months earlier."""
    channels = _CHANNELS if channels is None else channels
    result = fit_lag_structure(channels=channels, max_lag=max_lag)
    whole = result["whole_sample"]
    sample = result["sample"]

    by_channel = {}
    for c in channels:
        dcol = f"delta_{c}"
        by_channel[dcol] = [round(whole["beta"][f"{dcol}_lag{lag}"], 4) for lag in range(max_lag)]

    return {
        "max_lag": max_lag,
        "lambda": round(result["lambda"], 4),
        "lambda_cv": {
            "lambdas": [round(float(v), 6) for v in result["cv"]["lambda"]],
            "mse": [round(float(v), 6) for v in result["cv"]["mse"]],
        },
        "alpha": round(whole["alpha"], 4),
        "r2": round(whole["r2"], 4),
        "n": int(len(sample)),
        "sample_range": [sample.index.min().strftime("%Y-%m"), sample.index.max().strftime("%Y-%m")],
        "by_channel": by_channel,
    }


def walk_forward_lambda(z: pd.DataFrame, delta_cols: list[str], lambdas: np.ndarray | None = None,
                         min_train: int = 36, y_col: str = "delta_dev") -> pd.DataFrame:
    """Selects lambda by one-step-ahead walk-forward validation: for each
    candidate lambda, fit Ridge on z[:t] and score the squared error on
    z[t] (never used for that fit), for every t from min_train to the end,
    then average across t. min_train=36 (3 years) is a modest floor on how
    little data a 2-channel Ridge fit is trusted with -- arbitrary, not
    tuned to the answer.

    y_col defaults to "delta_dev" (every spec in this module until now has
    been delta-space) but can be overridden -- e.g. build_level_sample()
    passes y_col="dev" for the level-space variant, where the dependent
    variable isn't a delta at all.

    Returns one row per lambda (lambda, mean OOS squared error, fold count),
    sorted by error ascending -- best_lambda() just takes the top row."""
    lambdas = _LAMBDA_GRID if lambdas is None else lambdas
    X = z[delta_cols].values
    y = z[y_col].values
    n = len(z)

    rows = []
    for lam in lambdas:
        errors = []
        for t in range(min_train, n):
            model = Ridge(alpha=lam, fit_intercept=True)
            model.fit(X[:t], y[:t])
            pred = model.predict(X[t:t + 1])[0]
            errors.append((y[t] - pred) ** 2)
        rows.append({"lambda": float(lam), "mse": float(np.mean(errors)), "n_folds": len(errors)})
    return pd.DataFrame(rows).sort_values("mse").reset_index(drop=True)


def best_lambda(z: pd.DataFrame, delta_cols: list[str], lambdas: np.ndarray | None = None,
                 min_train: int = 36) -> float:
    cv = walk_forward_lambda(z, delta_cols, lambdas=lambdas, min_train=min_train)
    return float(cv.iloc[0]["lambda"])


def fit_whole_sample(z: pd.DataFrame, delta_cols: list[str], lam: float, y_col: str = "delta_dev") -> dict:
    """Single Ridge fit on the full available sample at the chosen lambda --
    the "whole-sample reference" line the rolling tab compares each window
    against, same role beer_model.py's own whole-sample fit plays for its
    rolling tab. y_col: see walk_forward_lambda()'s docstring."""
    X = z[delta_cols].values
    y = z[y_col].values
    model = Ridge(alpha=lam, fit_intercept=True)
    model.fit(X, y)
    fitted = model.predict(X)
    ss_res = float(np.sum((y - fitted) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return {
        "alpha": float(model.intercept_),
        "beta": {c: float(b) for c, b in zip(delta_cols, model.coef_)},
        "r2": r2,
        "n": len(z),
        "lambda": lam,
    }


def rolling_fit(z: pd.DataFrame, delta_cols: list[str], lam: float, window: int = 60,
                 step: int = 1, y_col: str = "delta_dev") -> pd.DataFrame:
    """Ridge coefficients re-estimated every `step` months on a trailing
    `window`-month sample -- same 60-month/monthly-step design as
    beer_model.py's rolling_fit(), swapped to a Ridge (not OLS+HAC)
    estimator, with lambda fixed at whatever walk_forward_lambda() already
    picked (chosen once, globally -- re-selecting lambda inside every one of
    ~160 windows would let lambda itself drift for reasons unrelated to the
    coefficients' own stability, which is the thing being tested here).
    y_col: see walk_forward_lambda()'s docstring."""
    X = z[delta_cols].values
    y = z[y_col].values
    n = len(z)

    rows = []
    for start in range(0, n - window + 1, step):
        win_X = X[start:start + window]
        win_y = y[start:start + window]
        model = Ridge(alpha=lam, fit_intercept=True)
        model.fit(win_X, win_y)
        fitted = model.predict(win_X)
        ss_res = float(np.sum((win_y - fitted) ** 2))
        ss_tot = float(np.sum((win_y - win_y.mean()) ** 2))
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
        row = {
            "window_start": z.index[start], "window_end": z.index[start + window - 1],
            "n": window, "r2": r2, "alpha": float(model.intercept_),
        }
        for c, b in zip(delta_cols, model.coef_):
            row[f"beta_{c}"] = float(b)
        rows.append(row)
    return pd.DataFrame(rows).set_index("window_end")


def run(channels: list[str] | None = None, window: int = 60) -> dict:
    channels = _CHANNELS if channels is None else channels
    delta_cols = [f"delta_{c}" for c in channels]
    z, stats = build_sample(channels=channels)

    print("=" * 78)
    print(f"RIDGE DEVIATION MODEL -- channels={channels}, walk-forward lambda selection")
    cv = walk_forward_lambda(z, delta_cols)
    lam = float(cv.iloc[0]["lambda"])
    print(cv.head(10).to_string(index=False))
    print(f"Selected lambda = {lam:.4f} (mean OOS MSE = {cv.iloc[0]['mse']:.4f})")

    whole = fit_whole_sample(z, delta_cols, lam)
    print("=" * 78)
    betas_fmt = {c: round(b, 4) for c, b in whole["beta"].items()}
    print(f"Whole-sample fit at lambda={lam:.4f}: alpha={whole['alpha']:+.4f}  "
          f"betas={betas_fmt}  R2={whole['r2']:.4f}  n={whole['n']}")

    roll = rolling_fit(z, delta_cols, lam, window=window)
    print("=" * 78)
    print(f"Rolling fit: {len(roll)} windows of {window} months, lambda={lam:.4f}")
    print(roll[[f"beta_{c}" for c in delta_cols] + ["r2"]].describe())

    _RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    cv.to_csv(_RESULTS_DIR / "lambda_cv.csv", index=False)
    roll.reset_index().to_csv(_RESULTS_DIR / "rolling.csv", index=False)
    pd.DataFrame([{"lambda": lam, "alpha": whole["alpha"], "r2": whole["r2"], "n": whole["n"],
                    **{f"beta_{c}": b for c, b in whole["beta"].items()}}]).to_csv(
        _RESULTS_DIR / "whole_sample.csv", index=False)

    print("=" * 78)
    print(f"IMPULSE-DECAY (LAG STRUCTURE) -- {_MAX_LAG} lags/channel, whole sample only")
    lag_result = fit_lag_structure(channels=channels, max_lag=_MAX_LAG)
    lag_whole = lag_result["whole_sample"]
    print(f"Selected lambda = {lag_result['lambda']:.4f}  alpha={lag_whole['alpha']:+.4f}  "
          f"R2={lag_whole['r2']:.4f}  n={lag_whole['n']}")
    for c in channels:
        dcol = f"delta_{c}"
        path = [round(lag_whole["beta"][f"{dcol}_lag{lag}"], 3) for lag in range(_MAX_LAG)]
        print(f"  {c:22s} lag0..lag{_MAX_LAG - 1}: {path}")
    lag_result["sample"].reset_index().to_csv(_RESULTS_DIR / "lag_structure_sample.csv", index=False)
    pd.DataFrame([{"lambda": lag_result["lambda"], "alpha": lag_whole["alpha"], "r2": lag_whole["r2"],
                    "n": lag_whole["n"], **{k: v for k, v in lag_whole["beta"].items()}}]).to_csv(
        _RESULTS_DIR / "lag_structure_whole_sample.csv", index=False)

    return {
        "channels": channels, "delta_cols": delta_cols, "lambda": lam, "cv": cv,
        "whole_sample": whole, "rolling": roll, "z": z, "stats": stats,
        "lag_structure": lag_result,
    }


# ---------------------------------------------------------------------------
# Dashboard tab: lambda-selection curve, historical fit, decomposition, and
# rolling-window coefficient paths -- built fresh each call rather than read
# from a saved trace, since fitting cost here is milliseconds, not the
# minutes-per-run every PyMC model in this package needs to amortize.
# ---------------------------------------------------------------------------

def build_dashboard_payload(channels: list[str] | None = None, window: int = 60) -> dict:
    """Payload for the "Ridge (Regularized, Rolling)" dashboard tab: the
    walk-forward lambda-selection curve, the whole-sample fit's own
    decomposition/level-bridge (same log-additive-then-multiplicative
    convention as every other tab), and the rolling-window coefficient paths
    against the whole-sample reference line.

    Model is build_plain_regression_sample()'s spec (include_ppp=False),
    switched 2026-07-30, same day, direct user instruction ("Wired it into
    the dashboard") following two immediately preceding decisions: (1)
    "instead of considering the ppp as equilibrium, incorporate it in the
    regression as a channel... just the regression" -- the dependent
    variable is now the exchange rate's OWN log return, delta_fx(t) =
    100*diff(log(ptax(t))), not delta_dev (no compute_deviation()/
    compute_equilibrium() involved in the fit itself); and (2) "Remove the
    ppp entirely, let the alfa capture it" -- PPP's own freely-estimated
    coefficient turned out unstable in the rolling read (whole-sample
    +0.34, rolling mean +0.04) and dropping it improved out-of-sample
    prediction, so it's excluded rather than included. Regressors:
    _CHANNELS_SHRUNK's 4 contemporaneous z-scored deltas (fiscal,
    carry_vol, dxy, curve_steep) plus delta_fx_lag1 (AR(1) on the
    exchange rate's own return, raw/unstandardized) -- reg_cols from
    build_plain_regression_sample() replaces the old delta_cols
    everywhere below.

    Level bridge is genuinely simpler than every earlier version of this
    payload: there's no PPP/equilibrium layer to bridge FROM anymore,
    since the model targets the FX level directly. The base layer is just
    a FLAT "anchor" series (the actual PTAX rate one month before the
    sample starts) instead of a time-varying equilibrium curve --
    anchor * exp(cum_alpha/100) * prod(exp(cum_contrib[c]/100)) *
    exp(cum_residual/100) reconstructs the actual PTAX rate exactly, same
    residual-absorbs-the-rest logic as every other tab's bridge, just one
    layer shorter."""
    channels = _CHANNELS_SHRUNK if channels is None else channels
    z, _, reg_cols = build_plain_regression_sample(channels=channels, include_ppp=False)
    delta_cols = reg_cols

    cv = walk_forward_lambda(z, delta_cols, y_col="delta_fx")
    lam = float(cv.iloc[0]["lambda"])
    whole = fit_whole_sample(z, delta_cols, lam, y_col="delta_fx")
    roll = rolling_fit(z, delta_cols, lam, window=window, y_col="delta_fx")

    df = load_data()
    months = [d.strftime("%Y-%m") for d in z.index]

    # --- historical fit (delta space), whole-sample point estimate ---
    X = z[delta_cols].values
    beta_vec = np.array([whole["beta"][c] for c in delta_cols])
    fitted_delta = whole["alpha"] + X @ beta_vec
    actual_delta = z["delta_fx"].values
    residual = actual_delta - fitted_delta

    # --- decomposition + level bridge (cumulative): anchor_level (actual
    # PTAX, not deviation) + cum_alpha + sum(cum_contrib) + cum_residual
    # reconstructs actual_ptax exactly, by definition of residual. ---
    actual_ptax_full = df["ptax"]
    anchor_date = z.index[0] - pd.DateOffset(months=1)
    anchor_level = float(actual_ptax_full.loc[anchor_date])
    actual_level = actual_ptax_full.reindex(z.index).values
    fitted_level = anchor_level * np.exp(np.cumsum(fitted_delta) / 100)

    contributions = {c: whole["beta"][c] * z[c].values for c in delta_cols}
    cum_alpha = np.cumsum(np.full(len(z), whole["alpha"]))
    cum_contrib = {c: np.cumsum(contributions[c]) for c in delta_cols}
    cum_residual = np.cumsum(residual)

    actual_ptax = actual_level

    anchor_series = np.full(len(z), anchor_level)
    lvl_0 = anchor_series
    lvl_1 = lvl_0 * np.exp(cum_alpha / 100)
    level_decomposition = {
        "anchor": [round(float(v), 4) for v in lvl_0],
        "baseline": [round(float(v), 4) for v in (lvl_1 - lvl_0)],
    }
    prev = lvl_1
    for c in delta_cols:
        nxt = prev * np.exp(cum_contrib[c] / 100)
        level_decomposition[c] = [round(float(v), 4) for v in (nxt - prev)]
        prev = nxt
    lvl_final = prev * np.exp(cum_residual / 100)  # == actual_ptax exactly, up to floating point
    level_decomposition["residual"] = [round(float(v), 4) for v in (lvl_final - prev)]
    level_decomposition["actual"] = [round(float(v), 4) for v in actual_ptax]

    return {
        "n": int(len(z)),
        "sample_range": [months[0], months[-1]],
        "months": months,
        "lambda": round(lam, 4),
        "lambda_cv": {
            "lambdas": [round(float(v), 6) for v in cv["lambda"]],
            "mse": [round(float(v), 6) for v in cv["mse"]],
        },
        "whole_sample": {
            "alpha": round(whole["alpha"], 4),
            "beta": {c: round(whole["beta"][c], 4) for c in delta_cols},
            "r2": round(whole["r2"], 4),
        },
        "fit_delta": {
            "actual": [round(float(v), 4) for v in actual_delta],
            "fitted": [round(float(v), 4) for v in fitted_delta],
        },
        "fit_level": {
            "anchor_level": round(anchor_level, 4),
            "actual": [round(float(v), 4) for v in actual_level],
            "fitted": [round(float(v), 4) for v in fitted_level],
        },
        "decomposition": {
            "alpha": [round(float(v), 4) for v in cum_alpha],
            **{c: [round(float(v), 4) for v in cum_contrib[c]] for c in delta_cols},
            "residual": [round(float(v), 4) for v in cum_residual],
        },
        "level_decomposition": level_decomposition,
        "rolling": {
            "window_months": window,
            "n_windows": len(roll),
            "window_end": [d.strftime("%Y-%m") for d in roll.index],
            "r2": [round(float(v), 4) for v in roll["r2"]],
            "alpha": {
                "mean": [round(float(v), 4) for v in roll["alpha"]],
                "whole_sample": round(whole["alpha"], 4),
            },
            "channels": {
                c: {
                    "mean": [round(float(v), 4) for v in roll[f"beta_{c}"]],
                    "whole_sample": round(whole["beta"][c], 4),
                }
                for c in delta_cols
            },
        },
    }


def render_dashboard() -> None:
    """Regenerates referencia/ppp_dashboard.html with the Ridge tab added
    alongside the other seven. Delegates to state_space_model.render_dashboard()
    for everything else so this stays the single entry point that keeps all
    tabs in sync, rather than duplicating that function's payload wiring."""
    from analytics.exchange_rate.models import state_space_model
    state_space_model.render_dashboard()


if __name__ == "__main__":
    run()
