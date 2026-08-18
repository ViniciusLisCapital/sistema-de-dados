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
Originally reused bayesian_deviation_model.py's build_deltas_contemporaneous()/
_standardize_ext() (2000-01+ reference window) so the z-scored deltas here
were identical, channel for channel, to what that module's primary_contemp
spec used. bayesian_deviation_model.py was retired 2026-08 (Bayesian
attempt-one superseded by this Ridge model); both helpers were inlined below
rather than deleted, since this module still needs them and they have no
other dependency on that module beyond compute_deviation() (already imported
here directly from ppp_equilibrium).

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

    # Advance the pinned fit cutoff to incorporate newer data into
    # alpha/beta/lambda (see refit_from_latest_data()'s own docstring) --
    # run this once you've decided the model should actually refit, NOT on
    # routine data-refresh regenerations (those leave the cutoff, and so the
    # fit, untouched by design):
    uv run python -c "from analytics.exchange_rate.models.ridge_deviation_model import refit_from_latest_data; refit_from_latest_data(force=True)"
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge

from analytics.exchange_rate.models.ppp_equilibrium import (
    compute_deviation,
    compute_equilibrium,
    load_channel_series,
    load_data,
    load_primitive_series,
)

# Which primitives (see ppp_equilibrium.load_primitive_series()) build each
# composite channel, and in what order -- used only by build_dashboard_payload()
# to tell the forecast tab's "break down into parts" panels what to fetch/
# show. br_real_10y appears in TWO entries deliberately (see
# load_primitive_series()'s own docstring on why it's one shared input, not
# two independent guesses of the same rate). The actual arithmetic
# (carry_vol = (selic - fed_funds) / fx_vol, etc.) lives client-side in
# the FX report's Ridge tab (analytics/exchange_rate/report.html), not here --
# this dict only says WHICH raw
# series feed which channel.
_COMPOSITE_PRIMITIVES = {
    "carry_vol": ["selic", "fed_funds", "fx_vol"],
    "real_yield_diff": ["br_real_10y", "us_real_10y"],
    "curve_steep_real": ["br_real_10y", "br_real_2y"],
}

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

_RESULTS_DIR = Path(__file__).parent / "ridge_results"

_REFERENCE_START = "2000-01-01"


def build_deltas_contemporaneous(df: pd.DataFrame) -> pd.DataFrame:
    """Contemporaneous (no extra 1-month lag) first-differenced regressors
    alongside delta_dev(t) -- inlined from the retired bayesian_deviation_model.py
    (see module docstring above). curve_steep/curve_steep_real (BR nominal/real
    10Y-2Y yield-curve steepening, PREJS/NTNBJS@120M-24M) and dxy_em (Fed
    Broad-EM dollar index, FRED DTWEXEMEGS) are carried alongside the original
    channel set for models that use them."""
    dev = compute_deviation(df)
    out = pd.DataFrame(index=df.index)
    out["delta_dev"] = dev.diff()
    out["deviation_lag1"] = dev.shift(1)
    for col in ("carry", "relative_carry", "carry_vol", "relative_carry_vol", "tot", "breakeven", "breakeven_gap",
                "fiscal", "dxy", "dxy_em", "curve_steep", "curve_steep_real"):
        out[f"delta_{col}"] = df[col].diff()
    return out


def _standardize_ext(sample: pd.DataFrame, reference: pd.DataFrame, cols: list[str]) -> tuple[pd.DataFrame, dict]:
    """Z-scores `sample` using each column's mean/std computed from `reference`
    instead of from `sample` itself -- inlined from the retired
    bayesian_deviation_model.py (see module docstring above). Lets channels
    with longer real history (e.g. carry, dxy) be standardized against their
    own full 2000-01+ window even when the fitting sample itself is bound to
    a narrower overlap forced by a late-starting channel (e.g. fiscal/CDS,
    2007-12+). `reference` need not share `sample`'s index; each column's
    stats are computed independently over its own non-null rows."""
    stats = {}
    z = sample.copy()
    for c in cols:
        ref_col = reference[c].dropna()
        mu, sd = ref_col.mean(), ref_col.std()
        z[c] = (sample[c] - mu) / sd
        stats[c] = (mu, sd)
    return z, stats

# Started as ["fiscal", "dxy"], grown same day to the four carry variants,
# then to breakeven_gap + tot (see module docstring for the two rounds).
# All eight already exist as delta_<channel> columns in
# build_deltas_contemporaneous().
_CHANNELS = ["fiscal", "dxy", "carry", "relative_carry", "carry_vol", "relative_carry_vol", "breakeven_gap", "tot"]

# 2026-07-31, direct user request: test (i) a Fed Broad-EM dollar index
# (dxy_em, EM-specific FX co-movement) alongside dxy, and (ii) a REAL
# (inflation-linked) yield-curve steepening (curve_steep_real,
# NTNBJS@120M-24M) alongside the nominal curve_steep already in
# _CHANNELS_SHRUNK -- hypothesis: 5y USD CDS (fiscal) understates domestic
# fiscal-sustainability risk given Brazil's large USD reserve buffer, and a
# real term premium isolates that risk net of inflation-expectations noise a
# nominal curve mixes in. Both new channels tested TOGETHER (not one at a
# time), same walk-forward-OOS standard as every prior variant round.
_CHANNELS_SHRUNK_EM_REAL = ["fiscal", "carry_vol", "dxy", "dxy_em", "curve_steep", "curve_steep_real"]

# 2026-07-31, same day, direct user request: test S&P 500 (sp500, "competing
# for capital" hypothesis), VIX, and the US 10Y real yield (FRED DFII10) as a
# joint global-risk/capital-competition round, one-at-a-time comparison
# after the joint test to isolate which channel actually carries signal.
# sp500 alone improved walk-forward OOS MSE ~4pct with a stable, never-
# crosses-zero rolling coefficient across all 163 windows; VIX and the real
# yield did NOT improve OOS MSE and were NOT added to _CHANNELS -- see
# ppp_equilibrium.py's sp500 docstring and analytics/exchange_rate/CLAUDE.md
# for the full comparison (walk-forward OOS MSE, one-at-a-time ablation).
# Read narrowly: what carries signal is sp500's own PRICE MOVE (a level-of-
# the-index/"competing for capital" effect), not general risk appetite --
# VIX (the more direct risk-sentiment proxy) added nothing once sp500 was
# already in the regression, which is why VIX/real-yield are absent here.
_CHANNELS_SHRUNK_EM_REAL_SP500 = _CHANNELS_SHRUNK_EM_REAL + ["sp500"]

# 2026-07-31, same day, direct user request: test the 10Y REAL yield
# differential (BR-US, real_yield_diff -- a risk-premium measure, distinct
# from testing the US real yield alone, which did NOT clear the bar in the
# round above) and a USD-denominated commodity-price index (icbr_usd, BCB
# SGS 29042) -- NOT comm_icbr (SGS 27574 etc.), which is BRL-denominated and
# unsuitable here since the BCB already converts it into reais, making it
# partly endogenous to USD/BRL itself. Both cleared the walk-forward OOS bar
# individually and together (real_yield_diff -1.7% alone, icbr_usd -4.6%
# alone, both together -6.1% vs. the 7-channel baseline) -- see
# ppp_equilibrium.py's real_yield_diff/icbr_usd docstrings and
# analytics/exchange_rate/CLAUDE.md for the full comparison.
_CHANNELS_SHRUNK_EM_REAL_SP500_RY_ICBR = _CHANNELS_SHRUNK_EM_REAL_SP500 + ["real_yield_diff", "icbr_usd"]

# 2026-07-31, same day, direct user request following a visual observation on
# the shipped Ridge tab's decomposition chart (large unexplained residual
# concentrated 2020-2022, alpha/PPP-type drift catching up only later):
# dropping curve_steep (nominal 10Y-2Y steepening) from the 9-channel spec
# above -- confirmed a clean, repeatedly-reproduced win across every round-4
# test this session (-1.4% OOS MSE, 7.0675->6.9677, essentially no change to
# any other channel's coefficient). Five candidate explanations for the
# residual concentration itself were tested and ALL failed walk-forward OOS
# validation against this 8-channel baseline: (1) short-term real yield as a
# BR-US differential (wrong construction, rejected before a full test), (2)
# short-term real yield as Selic-IPCA ex-post (`real_br_ex_post`, +0.5% worse),
# (3) standalone BR 1Y bond-implied real yield level (NTNBJS@12M, +0.5%
# worse, likely collinear with curve_steep_real), (4) BR-US 5Y breakeven
# inflation differential, contemporaneous delta (+0.8% worse, R2 flat), (5) a
# COVID-window dummy, tested both broad (2020-03 to 2021-12, +0.1% worse) and
# narrow/acute (2020-02 to 2020-05, +0.05% worse, small coefficient). None of
# these five is in this channel list -- see each scratch test's own docstring
# and analytics/exchange_rate/CLAUDE.md for the full record. The 2020-2022
# residual concentration remains unexplained; a genuinely different, more
# current finding surfaced while investigating it instead -- rolling R2 has
# been declining every year since 2022, reaching its weakest point in the
# most recent 2025-2026 windows, which argues against a COVID-specific
# structural break and toward a recent, ongoing fit degradation as the more
# actionable open thread.
_CHANNELS_SHRUNK_EM_REAL_SP500_RY_ICBR_NOSTEEP = [
    c for c in _CHANNELS_SHRUNK_EM_REAL_SP500_RY_ICBR if c != "curve_steep"
]

# Channels whose month-over-month change is a LOG-RETURN (100*diff(log(.))),
# not a plain level diff -- price indices in the thousands/hundreds, where a
# raw point change isn't the right transform (unlike every other channel
# here, which is already a rate/spread/differential, stationary in levels).
# Used by _deltas_with_extra_channels()/build_plain_regression_sample() below.
_LOG_RETURN_CHANNELS = {"sp500", "icbr_usd"}

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


def _deltas_with_extra_channels(df: pd.DataFrame, channels: list[str]) -> pd.DataFrame:
    """build_deltas_contemporaneous(df) plus delta_<c> for any channel in
    `channels` that function doesn't already compute (sp500, real_yield_diff,
    icbr_usd, and any future addition), WITHOUT touching
    bayesian_deviation_model.py (that module isn't part of the dashboard
    pipeline anymore -- Ridge is the only model wired into the FX report
    -- so new channels are added locally here instead of in its shared
    helper). Channels in _LOG_RETURN_CHANNELS (price indices in the
    thousands/hundreds) get a LOG-RETURN (100*diff(log(.))); everything else
    (rates, spreads, differentials -- already stationary in levels) gets a
    plain level diff, same convention build_deltas_contemporaneous() itself
    uses -- same special-casing build_plain_regression_sample() below
    applies independently for its own dependent-variable-free spec."""
    deltas = build_deltas_contemporaneous(df)
    for c in channels:
        col = f"delta_{c}"
        if col in deltas.columns:
            continue
        deltas[col] = 100 * np.log(df[c]).diff() if c in _LOG_RETURN_CHANNELS else df[c].diff()
    return deltas


def build_sample(df: pd.DataFrame | None = None, channels: list[str] | None = None) -> tuple[pd.DataFrame, dict]:
    """delta_dev plus each channel's z-scored CONTEMPORANEOUS delta,
    standardized against the same 2000-01+ reference window
    bayesian_deviation_model.py's primary_contemp spec uses (not this
    model's own narrower fitting-sample overlap) -- so a coefficient here
    stays comparable to that spec's if the two are ever set side by side."""
    channels = _CHANNELS if channels is None else channels
    df = load_data() if df is None else df
    delta_cols = [f"delta_{c}" for c in channels]
    deltas = _deltas_with_extra_channels(df, channels)
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
    deltas = _deltas_with_extra_channels(df, channels)

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
    other spec in this file that doesn't have its own explicit PPP term.

    Channels in _LOG_RETURN_CHANNELS (sp500, icbr_usd -- both 2026-07-31) are
    special-cased to a log-return (100*diff(log(.))), same as delta_fx/
    delta_ppp above -- both are price indices (thousands/hundreds), so a
    plain level diff() (correct for every other channel here, which are all
    rates/spreads/differentials already stationary in levels) would be the
    wrong transform. This module-local special-casing is deliberate --
    bayesian_deviation_model.py isn't part of the dashboard pipeline anymore
    (Ridge is the only model wired into the FX report), so new channels
    are handled entirely here, not in that module's own delta-builder."""
    channels = _CHANNELS_SHRUNK if channels is None else channels
    df = load_data() if df is None else df

    out = pd.DataFrame(index=df.index)
    out["delta_fx"] = 100 * np.log(df["ptax"]).diff()
    if include_ppp:
        out["delta_ppp"] = 100 * (np.log(df["ipca_index"]) - np.log(df["cpi_index"])).diff()
    for c in channels:
        if c in _LOG_RETURN_CHANNELS:
            out[f"delta_{c}"] = 100 * np.log(df[c]).diff()
        else:
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


_FORECAST_BANDS_CACHE = _RESULTS_DIR / "forecast_error_bands_w72.json"


def forecast_error_bands_w72(channels: list[str] | None = None, window: int = 72,
                              horizon: int = 12, force: bool = False) -> dict:
    """Per-forecast-step standard error for a W=72-month-trained, multi-step
    Ridge forecast -- 2026-07-31, direct user request, part 3 of the
    decomposition/forecast follow-up ("it's necessary to have a standard
    error for that forecast. the standard error should be base on the test
    we already have (run on the 72mo window -> forecast 12mo foward, compute
    the forecast error for each month and construct the interval from the
    next to 12 months horizon"). Reuses the exact walk-forward rolling-
    window / multi-step-simulation mechanism from the W x F grid test
    (analytics/exchange_rate/referencia/equilibrium_model/ridge_window_horizon_grid.md) at
    W=72 specifically -- own simulated AR(1) feedback (delta_fx_lag1) fed
    forward at every step, real realized channel deltas for those months --
    but where the grid test only scored the CUMULATIVE return at the end of
    each horizon F, this scores the error at EVERY intermediate step (1, 2,
    ..., 12 months ahead) separately, pooling each step's error across every
    rolling fold to build a step-indexed error curve. That per-step curve is
    what lets the dashboard draw a widening (not flat) confidence band on a
    forecast chart -- month 1 should be tighter than month 12, and a single
    cumulative-horizon number (what the grid test computed) can't express
    that on its own.

    Expensive (a full W=72-month rolling refit walked across the whole
    ~220-month sample, same cost class as the grid test's own W=72 cell,
    which took ~70-80s in that test) -- cached to
    ridge_results/forecast_error_bands_w72.json and only recomputed when
    force=True or the cache file doesn't exist yet, rather than on every
    build_dashboard_payload() call (which needs to stay cheap, since it also
    runs at render time)."""
    if not force and _FORECAST_BANDS_CACHE.exists():
        import json
        with open(_FORECAST_BANDS_CACHE) as fh:
            cached = json.load(fh)
        if cached.get("window") == window and cached.get("horizon") == horizon:
            return cached

    channels = _CHANNELS_SHRUNK_EM_REAL_SP500_RY_ICBR_NOSTEEP if channels is None else channels
    df = load_data()
    out = pd.DataFrame(index=df.index)
    out["ptax"] = df["ptax"]
    out["delta_fx"] = 100 * np.log(df["ptax"]).diff()
    out["delta_fx_lag1"] = out["delta_fx"].shift(1)
    delta_cols = []
    for c in channels:
        if c in _LOG_RETURN_CHANNELS:
            out[f"delta_{c}"] = 100 * np.log(df[c]).diff()
        else:
            out[f"delta_{c}"] = df[c].diff()
        delta_cols.append(f"delta_{c}")
    out = out.dropna(subset=["ptax", "delta_fx", "delta_fx_lag1"] + delta_cols)

    n = len(out)
    max_f = horizon
    step_errors = {h: [] for h in range(1, horizon + 1)}
    n_folds = n - window - max_f + 1

    for start in range(0, n_folds):
        train = out.iloc[start:start + window]
        future = out.iloc[start + window: start + window + max_f]

        reference = train[train.index >= _REFERENCE_START]
        if len(reference) < 12:
            reference = train
        z, stats = _standardize_ext(train, reference, delta_cols)
        z["delta_fx_lag1"] = train["delta_fx_lag1"]
        z["delta_fx"] = train["delta_fx"]
        reg_cols = delta_cols + ["delta_fx_lag1"]

        min_train = max(6, window // 2)
        cv = walk_forward_lambda(z, reg_cols, y_col="delta_fx", min_train=min_train)
        lam = float(cv.iloc[0]["lambda"])
        model = Ridge(alpha=lam, fit_intercept=True)
        model.fit(z[reg_cols].values, z["delta_fx"].values)

        z_future = pd.DataFrame(index=future.index)
        for c in delta_cols:
            mean, std = stats[c]
            z_future[c] = (future[c] - mean) / std if std > 0 else future[c] - mean

        seed_level = train["ptax"].iloc[-1]
        prev_delta_fx = train["delta_fx"].iloc[-1]
        cum_sim = 0.0
        for h, dt in enumerate(future.index, start=1):
            row = z_future.loc[dt, delta_cols].values
            x = np.concatenate([row, [prev_delta_fx]])
            delta_pred = model.predict(x.reshape(1, -1))[0]
            cum_sim += delta_pred
            prev_delta_fx = delta_pred

            sim_level = seed_level * np.exp(cum_sim / 100)
            real_level = future["ptax"].iloc[h - 1]
            pct_error = 100 * (sim_level - real_level) / real_level
            step_errors[h].append(pct_error)

    result = {
        "window": window,
        "horizon": horizon,
        "n_folds": n_folds,
        "steps": list(range(1, horizon + 1)),
        "std_error_pct": [round(float(np.std(step_errors[h])), 4) for h in range(1, horizon + 1)],
        "mean_error_pct": [round(float(np.mean(step_errors[h])), 4) for h in range(1, horizon + 1)],
    }

    _RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    import json
    with open(_FORECAST_BANDS_CACHE, "w") as fh:
        json.dump(result, fh, indent=2)
    return result


_FIT_CUTOFF_CACHE = _RESULTS_DIR / "model_fit_cutoff.json"


def _load_fit_cutoff() -> str | None:
    if not _FIT_CUTOFF_CACHE.exists():
        return None
    import json
    with open(_FIT_CUTOFF_CACHE) as fh:
        return json.load(fh)["cutoff_month"]


def refit_from_latest_data(channels: list[str] | None = None, force: bool = False) -> str:
    """Pins (or re-pins) the month through which build_dashboard_payload()'s
    Ridge fit (alpha/beta/lambda, the decomposition, the forecast tab's seed
    state) is computed -- persisted to disk so a plain report regeneration,
    which reloads fresh DB data every time, can never silently refit the
    model just because every channel happens to catch up to the same month
    at once. 2026-08, direct user request ("I still don't want to re-run the
    model" when only SOME regressors -- e.g. fiscal/CDS -- have new data out
    but others don't yet): without this, the fit sample was bounded only by
    build_plain_regression_sample()'s own dropna() (whichever channel lags
    furthest), which drifts forward on its own with no explicit signal, so
    a plain regeneration could in principle change alpha/beta by accident.

    A no-op (returns the existing pinned cutoff unchanged) when one is
    already saved and force=False -- this is what every ordinary
    build_dashboard_payload() call does, so routine regenerations never move
    the fit. Call with force=True only once you've decided the model should
    actually incorporate the newer data (advances the cutoff to the latest
    month every channel currently has in common) -- the dashboard's forecast
    tab then resets to a fresh 12-month horizon from that new cutoff, same
    as it always has. Data for months AFTER whatever cutoff is pinned here
    is still surfaced to the dashboard (build_dashboard_payload()'s own
    `nowcast` block, assessed independently per channel), just never fed
    into the coefficient fit until this is explicitly called."""
    if not force:
        existing = _load_fit_cutoff()
        if existing is not None:
            return existing

    channels = _CHANNELS_SHRUNK_EM_REAL_SP500_RY_ICBR_NOSTEEP if channels is None else channels
    z, _, _ = build_plain_regression_sample(channels=channels, include_ppp=False)
    latest = z.index.max().strftime("%Y-%m")

    _RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    import json
    with open(_FIT_CUTOFF_CACHE, "w") as fh:
        json.dump({"cutoff_month": latest}, fh, indent=2)
    return latest


# ---------------------------------------------------------------------------
# Dashboard tab: lambda-selection curve, historical fit, decomposition, and
# rolling-window coefficient paths -- built fresh each call rather than read
# from a saved trace, since fitting cost here is milliseconds, not the
# minutes-per-run every PyMC model in this package needs to amortize.
# ---------------------------------------------------------------------------

def build_dashboard_payload(channels: list[str] | None = None, window: int = 72) -> dict:
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
    layer shorter.

    Channel set grown 2026-07-31 across three rounds, same day: _CHANNELS_SHRUNK
    (4: fiscal, carry_vol, dxy, curve_steep) -> _CHANNELS_SHRUNK_EM_REAL (6:
    + dxy_em, curve_steep_real) -> _CHANNELS_SHRUNK_EM_REAL_SP500 (7: + sp500)
    -> _CHANNELS_SHRUNK_EM_REAL_SP500_RY_ICBR (9: + real_yield_diff, icbr_usd)
    -- direct user requests, every addition tested and confirmed to improve
    walk-forward OOS MSE before being wired in (see each constant's own
    comment and analytics/exchange_rate/CLAUDE.md for the full test record).
    Deviation vs. plain-regression framework choice was re-confirmed on the
    7-channel set before switching the default (not just assumed from the
    smaller-channel-set comparison earlier this session) -- OOS MSE came
    back very close (deviation 7.4708 vs. plain-regression 7.5297, a <1%
    gap) with nearly identical betas either way, so the framework this tab
    already shipped with (plain-regression, no PPP) was kept rather than
    switched, since the data didn't call for a change, only the channel set
    did. The framework choice was NOT re-tested again for the 9-channel set
    -- no reason to expect that <1% gap to flip with two more channels added
    identically to both frameworks.

    curve_steep DROPPED, same day, later round: confirmed a clean,
    repeatedly-reproduced win (-1.4% OOS MSE) across every round-4 residual-
    investigation test this session -- see
    _CHANNELS_SHRUNK_EM_REAL_SP500_RY_ICBR_NOSTEEP's own comment for the full
    list of what else was tried (and failed) against this same baseline
    while investigating the 2020-2022 decomposition residual.

    Rolling window default changed 60 -> 72 months (2026-07-31, direct user
    request, following the W x F training-window/forecast-horizon grid test
    in analytics/exchange_rate/referencia/equilibrium_model/ridge_window_horizon_grid.md): that
    grid found W=72 is the more robust single choice across forecast
    horizons (W=60 and W=72 are close at every horizon, but W=84 clearly
    degrades at F=12mo specifically) -- this payload's `window` default
    follows that finding for BOTH the Rolling Coefficient/R2 charts AND the
    "last window" parameters the decomposition toggle and forecast area
    (below) both key off of, so all three stay consistent with each other.

    last_window block + forecast/scenario area (2026-07-31, same day, direct
    user request, three-part follow-up): (1) the decomposition chart's bars
    always used the WHOLE-SAMPLE alpha/beta, even when a start/end month was
    picked -- `last_window` now exposes the MOST RECENT rolling window's own
    alpha/beta plus a parallel `contrib_monthly_last_window` (built exactly
    like `contrib_monthly` but from those coefficients instead), and the
    template's decomposition toggle switches which one feeds the bars,
    auto-restricting Start/End to that window's own date span when clicked.
    (2) `forecast` exposes what a client-side multi-step scenario simulator
    needs to run entirely in JS (last window's alpha/beta/lambda, each
    channel's reference mean/std for un-standardizing a user-entered raw-
    unit shock, and the seed level/AR state to start from) -- no server
    round-trip needed per scenario, since Ridge is just alpha + beta.x, cheap
    enough to re-run 12 steps forward in the browser on every input change.
    (3) `forecast_error_bands` are PRE-COMPUTED here (not simulated live) via
    forecast_error_bands_w72(): the same walk-forward-path-tracking
    mechanism as the W=72,F=12 cell of the grid test (own simulated AR
    feedback, real realized channels), but scored PER STEP (1..12 months
    ahead) rather than only at the cumulative 12-month horizon, pooling the
    per-step error across every rolling fold to get a step-indexed std-error
    curve. This is expensive (full W=72 rolling refit across the sample) so
    it's cached to a JSON file and only recomputed when the underlying
    sample/spec changes, not on every build_dashboard_payload() call -- see
    that function's own docstring."""
    channels = _CHANNELS_SHRUNK_EM_REAL_SP500_RY_ICBR_NOSTEEP if channels is None else channels
    z, stats, reg_cols = build_plain_regression_sample(channels=channels, include_ppp=False)
    delta_cols = reg_cols

    # Pinned fit cutoff (see refit_from_latest_data()'s own docstring): z
    # above is naturally bounded by whichever channel's data lags furthest
    # (build_plain_regression_sample()'s own dropna()), which drifts forward
    # on its own as new data lands. Truncating to the persisted cutoff here
    # decouples "what feeds the coefficient fit" from "what's in the DB
    # right now" -- alpha/beta/lambda/decomposition/forecast-seed below only
    # ever move when refit_from_latest_data(force=True) is called.
    cutoff_month = refit_from_latest_data(channels=channels)
    cutoff_period = pd.Period(cutoff_month, freq="M")
    z = z.loc[z.index.to_period("M") <= cutoff_period]

    cv = walk_forward_lambda(z, delta_cols, y_col="delta_fx")
    lam = float(cv.iloc[0]["lambda"])
    whole = fit_whole_sample(z, delta_cols, lam, y_col="delta_fx")
    roll = rolling_fit(z, delta_cols, lam, window=window, y_col="delta_fx")

    df = load_data()
    months = [d.strftime("%Y-%m") for d in z.index]

    # --- nowcast: real observed values beyond the pinned fit cutoff,
    # wherever the DB already has them, assessed INDEPENDENTLY per channel
    # (and for ptax) -- via load_channel_series(), NOT df/z above. df is
    # load_data()'s core-joined frame, bounded by whichever of ptax/IBGE
    # IPCA/FRED US CPI publishes slowest (confirmed 2026-08: routinely US
    # CPI, ~2-week lag past month-end, or IBGE IPCA -- NOT the channels
    # themselves), so df/z never even have ROWS beyond that bound no matter
    # how current an individual channel's own table is. Reading off
    # load_channel_series()'s raw, independently-indexed series instead
    # means a channel that's updated past the cutoff (e.g. fiscal/CDS)
    # surfaces its new month(s) even while core's slower series haven't
    # caught up, without touching alpha/beta/lambda at all. Consumed
    # client-side to lock the matching box(es) in the 12-month forecast
    # grid to their real value instead of a user guess. ---
    raw_series = load_channel_series(channels + ["ptax"])
    cutoff_ts = cutoff_period.to_timestamp()
    nowcast_ptax = raw_series["ptax"][raw_series["ptax"].index > cutoff_ts].dropna()
    nowcast_channels = {}
    for c in channels:
        s = raw_series[c][raw_series[c].index > cutoff_ts].dropna()
        nowcast_channels[c] = {
            "months": [d.strftime("%Y-%m") for d in s.index],
            "values": [round(float(v), 4) for v in s.values],
        }
    # current_month lets the client tell a FINAL nowcast month (already
    # fully elapsed -- safe to lock outright) from the CURRENT, still-
    # in-progress one (e.g. "2026-08" read from a source updated daily,
    # a few days into the month -- genuinely not yet the month's eventual
    # close). Stamped at generation time, not read live in the browser, so
    # every viewer of a given report build sees the same classification
    # regardless of their own clock/timezone. 2026-08, direct user request
    # ("July is close, but august it's not... let me estimate the end
    # month value") after noticing a same-day partial CDS print (1 trading
    # day into August) got hard-locked exactly like a fully-elapsed month.
    current_month = pd.Timestamp.today().strftime("%Y-%m")

    # --- primitive breakdown for carry_vol/real_yield_diff/curve_steep_real
    # (2026-08, direct user request: "some variables are less intuitive in
    # aggregate... start from bottom up") -- each primitive gets the same
    # history/nowcast split as the main channels above, so the forecast
    # tab's "break down into parts" panels can lock/flag them 'final'/
    # 'provisional' independently, exactly like any other box. See
    # load_primitive_series()'s docstring for why br_real_10y is one
    # series shared by two composites, not two independent ones. ---
    primitive_names = sorted({p for prims in _COMPOSITE_PRIMITIVES.values() for p in prims})
    raw_primitives = load_primitive_series(primitive_names)
    primitives_payload = {}
    for p in primitive_names:
        hist_s = raw_primitives[p][raw_primitives[p].index <= cutoff_ts].dropna()
        now_s = raw_primitives[p][raw_primitives[p].index > cutoff_ts].dropna()
        primitives_payload[p] = {
            "months": [d.strftime("%Y-%m") for d in hist_s.index],
            "values": [round(float(v), 4) for v in hist_s.values],
            "nowcast": {
                "months": [d.strftime("%Y-%m") for d in now_s.index],
                "values": [round(float(v), 4) for v in now_s.values],
            },
        }

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

    # --- "Baseline" bucket (2026-07-30, direct user request "consider as
    # one metric the anchor, the alfa and the AR(1)"): the anchor level,
    # alpha, and the AR(1) term are the three pieces of this model that
    # AREN'T one of the four actual economic channels -- a starting point,
    # a constant drift, and the exchange rate's own momentum. Bundled into
    # one combined bucket (still an ABSOLUTE level, same role the old
    # "anchor"/"equilibrium" bucket played in every version of this chart)
    # rather than shown as three separate bars, so the chart visually
    # separates "structural/mechanical" from "the four things the model
    # actually explains the move with." ---
    ar1_col = "delta_fx_lag1"
    channel_cols = [c for c in delta_cols if c != ar1_col]
    contributions = {c: whole["beta"][c] * z[c].values for c in delta_cols}
    baseline_monthly = np.full(len(z), whole["alpha"]) + contributions[ar1_col]
    cum_baseline = np.cumsum(baseline_monthly)
    cum_contrib = {c: np.cumsum(contributions[c]) for c in channel_cols}
    cum_residual = np.cumsum(residual)

    actual_ptax = actual_level

    anchor_series = np.full(len(z), anchor_level)
    lvl_1 = anchor_series * np.exp(cum_baseline / 100)
    level_decomposition = {
        "baseline": [round(float(v), 4) for v in lvl_1],
    }
    prev = lvl_1
    for c in channel_cols:
        nxt = prev * np.exp(cum_contrib[c] / 100)
        level_decomposition[c] = [round(float(v), 4) for v in (nxt - prev)]
        prev = nxt
    lvl_final = prev * np.exp(cum_residual / 100)  # == actual_ptax exactly, up to floating point
    level_decomposition["residual"] = [round(float(v), 4) for v in (lvl_final - prev)]
    level_decomposition["actual"] = [round(float(v), 4) for v in actual_ptax]

    # --- monthly (NON-cumulative) contributions, one number per bucket per
    # month -- lets the dashboard rebase the decomposition to any chosen
    # start month client-side (fresh cumsum from that index, anchored at
    # the actual PTAX rate the month before), direct user request ("I want
    # the option to select an initial date to make a decomposition...
    # understand how my model explains the performance since 2025") rather
    # than just slicing the whole-sample-anchored cumulative arrays above
    # (which would still carry pre-2025 residual/channel buildup into every
    # bar). ---
    contrib_monthly = {
        "baseline": [round(float(v), 4) for v in baseline_monthly],
        **{c: [round(float(v), 4) for v in contributions[c]] for c in channel_cols},
        "residual": [round(float(v), 4) for v in residual],
    }

    # --- last-window decomposition (2026-07-31, direct user request: "the
    # exchange rate decomposition consider the whole-sample parameters,
    # right? I want a option here to click and use the parameters of the
    # window... restrict the range to the window") -- same monthly-
    # contribution construction as contrib_monthly above, but using the
    # MOST RECENT rolling window's own alpha/beta (roll.iloc[-1], already
    # fitted on exactly that window) instead of the whole-sample fit, and
    # restricted to that window's own `window` months rather than the full
    # sample. The residual here is NOT the same quantity as the whole-
    # sample residual above -- it's this window-specific fit's own
    # in-sample residual over its own months, so the two decompositions
    # aren't directly comparable bar-for-bar, only each internally
    # consistent (each bridges its own anchor to the actual rate exactly). ---
    last_row = roll.iloc[-1]
    last_alpha = float(last_row["alpha"])
    last_beta = {c: float(last_row[f"beta_{c}"]) for c in delta_cols}
    last_window_months = months[-window:]
    z_last = z.iloc[-window:]

    X_last = z_last[delta_cols].values
    beta_vec_last = np.array([last_beta[c] for c in delta_cols])
    fitted_delta_last = last_alpha + X_last @ beta_vec_last
    actual_delta_last = z_last["delta_fx"].values
    residual_last = actual_delta_last - fitted_delta_last

    contributions_last = {c: last_beta[c] * z_last[c].values for c in delta_cols}
    baseline_monthly_last = np.full(len(z_last), last_alpha) + contributions_last[ar1_col]

    contrib_monthly_last_window = {
        "baseline": [round(float(v), 4) for v in baseline_monthly_last],
        **{c: [round(float(v), 4) for v in contributions_last[c]] for c in channel_cols},
        "residual": [round(float(v), 4) for v in residual_last],
    }

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
            "baseline": [round(float(v), 4) for v in cum_baseline],
            **{c: [round(float(v), 4) for v in cum_contrib[c]] for c in channel_cols},
            "residual": [round(float(v), 4) for v in cum_residual],
        },
        "level_decomposition": level_decomposition,
        "contrib_monthly": contrib_monthly,
        "last_window": {
            "window_months": window,
            "start": last_window_months[0],
            "end": last_window_months[-1],
            "start_index": len(months) - window,
            "end_index": len(months) - 1,
            "alpha": round(last_alpha, 4),
            "beta": {c: round(last_beta[c], 4) for c in delta_cols},
            "r2": round(float(last_row["r2"]), 4),
            "anchor_level": round(float(actual_ptax_full.loc[z_last.index[0] - pd.DateOffset(months=1)]), 4),
            "contrib_monthly": contrib_monthly_last_window,
        },
        "forecast": {
            "horizon": 12,
            "seed_level": round(float(actual_level[-1]), 4),
            "seed_delta_fx_lag1": round(float(z["delta_fx"].iloc[-1]), 4),
            "alpha": round(last_alpha, 4),
            "beta": {c: round(last_beta[c], 4) for c in delta_cols},
            "channel_stats": {
                c: {"mean": round(float(stats[c][0]), 6), "std": round(float(stats[c][1]), 6)}
                for c in channel_cols
            },
            # 2026-07-31, direct user follow-up after trying the forecast
            # area live ("I'm not seeing what I'm doing with the
            # regressors"): the shock inputs had no visible connection to
            # each channel's own actual recent values or units -- a bare
            # "+50" was meaningless without seeing what level that's
            # relative to. channel_history exposes each channel's own last
            # 24 months of RAW (native-unit) values so the template can
            # plot "actual history -> shocked path forward" per channel,
            # same idea as the main decomposition/forecast chart but for
            # the regressors themselves rather than the FX rate they drive.
            # is_log_return flags sp500/icbr_usd so the client projects
            # their shocked path multiplicatively (level*exp(shock/100)^h)
            # instead of additively (level+shock*h), matching how each is
            # actually differenced in build_plain_regression_sample().
            #
            # 2026-07-31, same day, direct user follow-up ("put a button
            # ... I can see the regressor graph (all history) + forecast
            # future (dot) - with the option to see the Z-score too") --
            # extended from the last 24 months to the FULL sample so the
            # expanded regressor chart can show all available history, not
            # just the tail the compact sparkline needed. level_mean/
            # level_std (NEW here -- distinct from channel_stats' own
            # mean/std, which standardize the DELTA, not the level) let the
            # template's Z-score toggle standardize the raw level itself:
            # confirmed via AskUserQuestion this should be a z-score of the
            # LEVEL (a new, distinct statistic), not of the delta the model
            # actually regresses on -- the two answer different questions
            # ("how unusual is this level" vs. "how big a signal is this
            # month's move"), and the level reading is what was asked for.
            "channel_history": {
                c: {
                    "months": months,
                    "values": [round(float(v), 4) for v in df[c].reindex(z.index).values],
                    "is_log_return": c in _LOG_RETURN_CHANNELS,
                    "level_mean": round(float(np.nanmean(df[c].reindex(z.index).values)), 6),
                    "level_std": round(float(np.nanstd(df[c].reindex(z.index).values, ddof=1)), 6),
                }
                for c in channels
            },
            "nowcast": {
                "fit_cutoff": cutoff_month,
                "current_month": current_month,
                "ptax": {
                    "months": [d.strftime("%Y-%m") for d in nowcast_ptax.index],
                    "values": [round(float(v), 4) for v in nowcast_ptax.values],
                },
                "channels": nowcast_channels,
            },
            "primitives": primitives_payload,
            "composite_primitives": _COMPOSITE_PRIMITIVES,
        },
        "forecast_error_bands": forecast_error_bands_w72(channels=channels, window=window, horizon=12),
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
    """Back-compat alias: regenerates the whole FX report, model tabs included.

    Was the entry point for the standalone reports/ppp_dashboard.html (itself a
    replacement for the retired state_space_model.render_dashboard() -- see the
    module docstring above for why that module is gone). Since 2026-08 that
    dashboard's three tabs live inside analytics/exchange_rate/report.html, so
    building only them is no longer a thing you can do: the single entry point
    is generate_report.run(), which calls this module's own
    build_dashboard_payload() alongside the other nine loaders.
    """
    from analytics.exchange_rate.generate_report import run as generate_fx_report

    generate_fx_report()


if __name__ == "__main__":
    run()
