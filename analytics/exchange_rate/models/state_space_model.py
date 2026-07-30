"""
"Attempt two" -- Bayesian estimate of the USD/BRL PPP deviation's own
dynamics, cast directly from state_space_equilibrium_model.md's two-equation
system (2026-07-24 build, following the state_space_simulator.html design
discussion the same day):

    Measurement:  ptax(t) = equilibrium(t) * exp(deviation(t) / 100)
    Transition:   equilibrium(t) = equilibrium(t-1) + pi_diff(t)      [eta = 0]
    Deviation:    deviation(t) = alpha + phi*deviation(t-1)
                                + b_carry*z(delta_carry(t)) + b_tot*z(delta_tot(t))
                                + b_breakeven*z(delta_breakeven(t)) + b_fiscal*z(delta_fiscal(t))
                                + eps(t)

Y is the NOMINAL exchange rate (ptax), not REER -- explicit user call,
2026-07-24. This also resolves the sign-convention ambiguity that had been
open in the concept note: ppp_equilibrium.compute_equilibrium() is already
anchored to actual ptax (nominal), not BIS REER, so there's nothing to
reconcile here.

eta (equilibrium's own noise) was fixed at zero for the first build --
explicit user call, to avoid the "pile-up problem" (eta routinely collapsing
toward zero in finite samples for this model class) on a first pass. With
eta=0, equilibrium(t) is exactly ppp_equilibrium.compute_equilibrium() --
already known, not filtered -- so deviation(t) = compute_deviation(df) is
directly OBSERVED too, not latent. `fit()`/`run()` still implement that
version (kept as the primary spec -- "let the alpha stay", 2026-07-24 user
call, means both the with-alpha eta=0 fit and its comparison against a
no-intercept variant remain in place, see fit_no_alpha_spec()).

`fit_kalman()` (added 2026-07-24, "let's unleash the eta error") implements
the REAL two-state Kalman filter: eta freely estimated alongside phi, alpha,
the betas, and sigma. Measurement is still exact (y(t) = eq(t) + dev(t), no
separate observation noise) -- separate identification of eq/dev comes only
from their differing dynamics (eq: pure random walk driven by the actual
BR-US log inflation differential pi_diff(t); dev: mean-reverting AR(1)
driven by the four channels), the mechanism flagged as the identification
device back when eta=0 was chosen as the safer first cut. Hand-rolled via
pytensor.scan (no ready-made state-space package covers this shape -- degenerate
measurement noise, exogenous drivers in both state equations -- and
pymc_extras isn't installed here) -- validated against the eta=0 baseline
before being trusted: with sigma_eta forced near zero, the filtered states
reproduce compute_equilibrium()/compute_deviation() to ~1e-9. Initial state
(eq0, dev0) is anchored at the month before the regression sample with ZERO
prior uncertainty (P0=0, not diffuse) -- that anchor month is a real
historical month with known PTAX/IPCA/CPI, so both are exactly known facts,
not unknowns; model uncertainty (eta, eps) only accumulates forward from
there.

What IS new relative to bayesian_deviation_model.py ("attempt one"):
  - deviation(t) enters directly as a LEVEL regressed on its own lag (phi),
    replacing attempt one's differenced-plus-separate-ECM-spec patchwork
    (fit_regression() on delta_dev, then a separate fit_ecm_spec() bolting
    on deviation_lag1) with one coherent equation. phi is bounded to (0,1)
    by a Uniform prior, imposing stationarity a priori rather than
    reparametrizing rho = phi - 1 and hoping it comes out negative.
  - The four channels enter CONTEMPORANEOUSLY (delta_channel(t), no extra
    lag). bayesian_deviation_model.py's build_deltas() lags its deltas by
    one additional month (`.diff().shift(1)`, so delta_channel(t-1) predicts
    delta_dev(t)) -- confirmed by re-reading that module while building this
    one. That's the exact lagged-not-contemporaneous specification the
    state_space_simulator.html discussion (2026-07-24) argued against:
    financial variables move together in real time, so a lag mostly throws
    away the real relationship and keeps noise. This module fixes that for
    the state-space line of work; attempt one itself is left as-is (it was
    already fit and documented before this issue was identified).

DXY added as a 5th channel (2026-07-24, user request: "run the state space
Two (eta = 0) with adding it. I think can improve our model explicability"),
sourced from macro_international.cmb_dollar_index (ICE US Dollar Index,
Yahoo Finance DX-Y.NYB, newly ingested by the user). Unlike the other four
channels, DXY is a GLOBAL dollar-strength signal, not bilateral BRL-specific
-- it tests whether broad EM/dollar co-movement explains part of the
deviation that the bilateral channels miss. Scoped to the eta=0 primary
spec only, NOT the Kalman filter (fit_kalman() takes ~40 minutes per run,
vs. the primary spec's much cheaper regression-style fit) -- _CHANNELS
(shared default) now includes dxy, while _KALMAN_CHANNELS freezes the
original 4-channel list so build_kalman_dashboard_payload() keeps reading
correctly against its existing saved trace (kalman_idata.nc) without a
refit. Call fit_kalman(channels=_CHANNELS) and rebuild its dashboard
payload with the same channels to bring the Kalman tab up to date with
dxy, if/when wanted.

Usage:
    uv run python -c "from analytics.exchange_rate.models.state_space_model import run; run()"
"""

from __future__ import annotations

from pathlib import Path

import arviz as az
import numpy as np
import pandas as pd
import pymc as pm
import pytensor
import pytensor.tensor as pt

from analytics.exchange_rate.models.ppp_equilibrium import compute_deviation, compute_equilibrium, load_data

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

_RESULTS_DIR = Path(__file__).parent / "state_space_results"

_SAMPLE_KWARGS = dict(
    draws=2000, tune=1500, chains=4, progressbar=False, random_seed=42,
    target_accept=0.95, idata_kwargs={"log_likelihood": True},
)

_CHANNELS = ["carry", "tot", "breakeven", "fiscal", "dxy"]

# fit_kalman()'s already-saved posterior trace (state_space_results/kalman_idata.nc)
# was fit against the original 4-channel set, BEFORE dxy was added to _CHANNELS
# (2026-07-24, "run state space Two with DXY added" -- explicitly scoped to the
# eta=0 primary spec, not a Kalman refit, since fit_kalman() takes ~40 minutes).
# Keep the Kalman tab reading against this frozen list so it keeps rendering
# from its existing trace without a KeyError on a beta_delta_dxy that trace
# doesn't have; refit_kalman with channels=_CHANNELS to bring it up to date.
_KALMAN_CHANNELS = ["carry", "tot", "breakeven", "fiscal"]

# Posterior-sign expectations, carried over from bayesian_deviation_model.py's
# own sign_probability() checks -- same economic priors, now being tested
# against a contemporaneous rather than lagged specification.
_EXPECTED_POSITIVE = {
    "beta_delta_carry": None,   # no strong prior expectation either way
    "beta_delta_tot": False,    # expected negative
    "beta_delta_breakeven": True,
    "beta_delta_fiscal": True,
    "beta_delta_dxy": True,     # global dollar strength -> BRL depreciates too (broad EM co-movement)
}


def build_regressors(df: pd.DataFrame, base_month: str | None = None,
                      channels: list[str] | None = None) -> pd.DataFrame:
    """deviation(t) (level, from ppp_equilibrium.compute_deviation) plus
    deviation(t-1) and each channel's CONTEMPORANEOUS change -- no extra lag,
    unlike bayesian_deviation_model.py's build_deltas()."""
    channels = _CHANNELS if channels is None else channels
    kwargs = {} if base_month is None else {"base_month": base_month}
    dev = compute_deviation(df, **kwargs)
    out = pd.DataFrame(index=df.index)
    out["deviation"] = dev
    out["deviation_lag1"] = dev.shift(1)
    for col in channels:
        out[f"delta_{col}"] = df[col].diff()
    return out


def _standardize(frame: pd.DataFrame, cols: list[str]) -> tuple[pd.DataFrame, dict]:
    stats = {}
    z = frame.copy()
    for c in cols:
        mu, sd = frame[c].mean(), frame[c].std()
        z[c] = (frame[c] - mu) / sd
        stats[c] = (mu, sd)
    return z, stats


def fit(df: pd.DataFrame | None = None, label: str = "primary", no_intercept: bool = False) -> dict:
    """deviation(t) = alpha + phi*deviation(t-1) + sum(beta_c * z(delta_c(t))) + eps(t).

    phi ~ Uniform(0,1): bounds the fit to a stationary, mean-reverting
    process a priori (matches the whole point of a "deviation from
    equilibrium" concept -- an unbounded random walk here would mean
    "equilibrium" isn't pinning anything down). deviation_lag1 stays in its
    native log-percent units (not standardized) so its genuinely nonzero
    mean can explain part of the series' drift -- same reasoning
    bayesian_deviation_model.py's raw_cols argument documents for its own
    deviation_lag1 regressor. Channel deltas are standardized so one
    weakly-informative Normal(0,2) prior works regardless of native units.

    no_intercept (2026-07-24, user request: "can we remove the drift at
    all?") forces alpha to 0 -- theoretically motivated here, not just a
    robustness check: if PPP already captures the systematic drift (the
    whole point of anchoring equilibrium to it), deviation from PPP should
    be mean-zero in the long run, so a nonzero alpha in THIS equation would
    mean "there's an extra permanent drift PPP doesn't capture," an odd
    property for a supposedly-stationary error term. With alpha=0, the
    model's implied unconditional mean of deviation is exactly 0 (steady
    state: E[dev] = phi*E[dev] + 0 => E[dev] = 0 for phi != 1). Whether this
    changes anything or just relocates the same drift elsewhere is an
    empirical question, not assumed either way -- see run_no_alpha_spec()'s
    comparison against the with-intercept fit. Different mechanism from
    bayesian_deviation_model.py's own no-intercept test: that model's
    regressors were ALL standardized (mean 0 by construction, so none of
    them could ever explain delta_dev's nonzero mean without alpha);
    deviation_lag1 here is raw/non-zero-mean, so phi*deviation_lag1 may
    already carry what alpha used to.
    """
    df = load_data() if df is None else df
    reg = build_regressors(df)
    delta_cols = [f"delta_{c}" for c in _CHANNELS]
    sample = reg[["deviation", "deviation_lag1"] + delta_cols].dropna()

    z, stats = _standardize(sample, delta_cols)
    z["deviation_lag1"] = sample["deviation_lag1"]  # kept raw -- see docstring

    with pm.Model():
        phi = pm.Uniform("phi", 0, 1)
        mu = phi * z["deviation_lag1"].values
        if not no_intercept:
            alpha = pm.Normal("alpha", 0, 10)
            mu = alpha + mu
        betas = {c: pm.Normal(f"beta_{c}", 0, 2) for c in delta_cols}
        mu = mu + sum(betas[c] * z[c].values for c in delta_cols)
        sigma = pm.HalfNormal("sigma", 5)
        pm.Normal("y", mu=mu, sigma=sigma, observed=sample["deviation"].values)

        idata = pm.sample(**_SAMPLE_KWARGS)
        idata.extend(pm.sample_posterior_predictive(idata, progressbar=False))

    var_names = ([] if no_intercept else ["alpha"]) + ["phi"] + [f"beta_{c}" for c in delta_cols] + ["sigma"]
    summary = az.summary(idata, var_names=var_names)

    _RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    summary.to_csv(_RESULTS_DIR / f"{label}_summary.csv")
    idata.to_netcdf(_RESULTS_DIR / f"{label}_idata.nc")

    return {
        "label": label,
        "idata": idata,
        "no_intercept": no_intercept,
        "summary": summary,
        "n": len(sample),
        "sample_range": (sample.index.min(), sample.index.max()),
        "stats": stats,
        "delta_cols": delta_cols,
    }


def half_life_months(phi_draws: np.ndarray) -> np.ndarray:
    """ln(0.5)/ln(phi), elementwise. Well-defined everywhere here since phi
    is bounded to (0,1) by construction (Uniform(0,1) prior)."""
    return np.log(0.5) / np.log(phi_draws)


def sign_probability(idata, coef_name: str, expected_positive: bool) -> float:
    draws = idata.posterior[coef_name].values.flatten()
    return float((draws > 0).mean()) if expected_positive else float((draws < 0).mean())


def run() -> dict:
    df = load_data()
    print("=" * 78)
    print("STATE-SPACE DEVIATION MODEL ('attempt two') -- nominal ptax, eta=0, contemporaneous channels")
    result = fit(df, label="primary")
    print(result["summary"])
    print(f"n={result['n']}  range={[d.strftime('%Y-%m') for d in result['sample_range']]}")

    phi_draws = result["idata"].posterior["phi"].values.flatten()
    hl = half_life_months(phi_draws)
    print(f"Implied half-life: mean={np.mean(hl):.1f} months, median={np.median(hl):.1f} months "
          f"(94% HDI [{np.percentile(hl, 3):.1f}, {np.percentile(hl, 97):.1f}])")

    print("=" * 78)
    print("Sign checks (P(beta has expected sign)):")
    for name, expected in _EXPECTED_POSITIVE.items():
        if expected is None:
            continue
        p = sign_probability(result["idata"], name, expected)
        print(f"  P({name} {'>' if expected else '<'} 0) = {p:.3f}")

    return result


def fit_no_alpha_spec(df: pd.DataFrame | None = None) -> dict:
    """Refit with alpha forced to 0 -- 2026-07-24 user request ("can we
    remove the drift at all?") -- and compare phi/betas directly against the
    with-intercept primary spec, the same "test it, don't assume it" pattern
    bayesian_deviation_model.py's own no-intercept test followed. Saves under
    label "primary_no_alpha"."""
    df = load_data() if df is None else df
    print("=" * 78)
    print("NO-INTERCEPT SPEC -- alpha forced to 0")
    no_alpha = fit(df, label="primary_no_alpha", no_intercept=True)
    print(no_alpha["summary"])

    with_alpha_path = _RESULTS_DIR / "primary_idata.nc"
    if not with_alpha_path.exists():
        print("(no primary_idata.nc found -- run run() first to compare against the with-intercept spec)")
        return no_alpha

    with_alpha = az.from_netcdf(with_alpha_path)
    print("=" * 78)
    print("Comparison: with-intercept (primary) vs. no-intercept (primary_no_alpha)")
    delta_cols = [f"delta_{c}" for c in _CHANNELS]
    for name in ["phi"] + [f"beta_{c}" for c in delta_cols] + ["sigma"]:
        a = with_alpha.posterior[name].values.mean()
        b = no_alpha["idata"].posterior[name].values.mean()
        print(f"  {name}: with_alpha={a:+.4f}  no_alpha={b:+.4f}  diff={b - a:+.4f}")

    phi_no_alpha = no_alpha["idata"].posterior["phi"].values.flatten()
    hl = half_life_months(phi_no_alpha)
    hl = hl[np.isfinite(hl)]
    print(f"  implied half-life (no-intercept): median={np.median(hl):.1f} months "
          f"(94% HDI [{np.percentile(hl, 3):.1f}, {np.percentile(hl, 97):.1f}])")

    return no_alpha


# ---------------------------------------------------------------------------
# Kalman filter (eta freely estimated) -- the real two-state model
# ---------------------------------------------------------------------------

def build_kf_series(df: pd.DataFrame | None = None, channels: list[str] | None = None) -> dict:
    """Full-sample inputs for fit_kalman(): pi_diff(t), the actual monthly
    BR-US log inflation differential (not a stand-in -- this exactly
    reproduces ppp_equilibrium.compute_equilibrium()'s own construction when
    eta=0, verified to ~1e-13 by direct comparison against eq_log.diff());
    y(t) = 100*ln(ptax(t)); each channel's contemporaneous delta, standardized
    with the SAME stats as fit()'s eta=0 spec (so betas stay comparable); and
    the anchor (eq0, dev0) at the month before the regression sample -- a
    real historical month, so both are exactly known facts, not unknowns."""
    channels = _CHANNELS if channels is None else channels
    df = load_data() if df is None else df
    eq = compute_equilibrium(df)
    eq_log_full = 100 * np.log(eq)
    y_full = 100 * np.log(df["ptax"])
    pi_diff_full = eq_log_full.diff()

    reg = build_regressors(df, channels=channels)
    delta_cols = [f"delta_{c}" for c in channels]
    sample = reg[["deviation", "deviation_lag1"] + delta_cols].dropna()
    z, stats = _standardize(sample, delta_cols)
    anchor_date = sample.index[0] - pd.DateOffset(months=1)

    return {
        "months": [d.strftime("%Y-%m") for d in sample.index],
        "pi_diff": pi_diff_full.reindex(sample.index).values,
        "y": y_full.reindex(sample.index).values,
        "z": {c: z[c].values for c in delta_cols},
        "delta_cols": delta_cols,
        "eq0": float(eq_log_full.loc[anchor_date]),
        "dev0": float((y_full - eq_log_full).loc[anchor_date]),
        "eq_log_full": eq_log_full,
        "sample_index": sample.index,
    }


def fit_kalman(df: pd.DataFrame | None = None, label: str = "kalman",
                channels: list[str] | None = None, **sample_overrides) -> dict:
    """Two-state Kalman filter, eta freely estimated -- see module docstring
    for the full derivation/validation. State x(t) = (eq(t), dev(t)):

        eq(t)  = eq(t-1) + pi_diff(t) + eta(t),   eta  ~ N(0, sigma_eta^2)
        dev(t) = phi*dev(t-1) + alpha + sum(beta_c*z_c(t)) + eps(t)

    Hand-rolled scalar Kalman recursion (only 2 states, so covariance is
    just 3 numbers: Pee, Ped, Pdd) via pytensor.scan; its Gaussian
    prediction-error-decomposition log-likelihood is added with
    pm.Potential rather than an `observed=` likelihood, since there's no
    single observed random variable here -- which also means no
    posterior-predictive sampling and no per-observation log_likelihood
    group for LOO (not needed here; this isn't being compared against
    another model via information criteria).
    """
    df = load_data() if df is None else df
    S = build_kf_series(df, channels=channels)
    n = len(S["y"])
    delta_cols = S["delta_cols"]

    pi_diff_t = pt.as_tensor_variable(S["pi_diff"])
    y_t = pt.as_tensor_variable(S["y"])
    Z_t = {c: pt.as_tensor_variable(S["z"][c]) for c in delta_cols}

    with pm.Model():
        phi = pm.Uniform("phi", 0, 1)
        alpha = pm.Normal("alpha", 0, 10)
        betas = {c: pm.Normal(f"beta_{c}", 0, 2) for c in delta_cols}
        sigma_eps = pm.HalfNormal("sigma", 5)
        sigma_eta = pm.HalfNormal("sigma_eta", 5)

        c_dev = alpha + sum(betas[c] * Z_t[c] for c in delta_cols)  # (n,) tensor, one entry per month

        def step(pi_diff_i, c_dev_i, y_i, eqp, devp, Pee, Ped, Pdd, phi, sigma_eta, sigma_eps):
            eq_pred = eqp + pi_diff_i
            dev_pred = phi * devp + c_dev_i
            Pee_pred = Pee + sigma_eta ** 2
            Ped_pred = phi * Ped
            Pdd_pred = phi ** 2 * Pdd + sigma_eps ** 2

            v = y_i - (eq_pred + dev_pred)
            F = Pee_pred + 2 * Ped_pred + Pdd_pred
            K_eq = (Pee_pred + Ped_pred) / F
            K_dev = (Ped_pred + Pdd_pred) / F

            eq_new = eq_pred + K_eq * v
            dev_new = dev_pred + K_dev * v
            Pee_new = Pee_pred - K_eq ** 2 * F
            Pdd_new = Pdd_pred - K_dev ** 2 * F
            Ped_new = Ped_pred - K_eq * K_dev * F

            ll_i = -0.5 * (pt.log(2 * np.pi * F) + v ** 2 / F)
            return eq_new, dev_new, Pee_new, Ped_new, Pdd_new, ll_i

        eq0 = pt.constant(S["eq0"], dtype="float64")
        dev0 = pt.constant(S["dev0"], dtype="float64")
        zero = pt.constant(0.0, dtype="float64")

        (eq_seq, dev_seq, Pee_seq, Ped_seq, Pdd_seq, ll_seq), _ = pytensor.scan(
            fn=step,
            sequences=[pi_diff_t, c_dev, y_t],
            outputs_info=[eq0, dev0, zero, zero, zero, None],
            non_sequences=[phi, sigma_eta, sigma_eps],
        )

        pm.Potential("kf_loglik", ll_seq.sum())
        pm.Deterministic("eq_filtered", eq_seq)
        pm.Deterministic("dev_filtered", dev_seq)

        sample_kwargs = {k: v for k, v in _SAMPLE_KWARGS.items() if k != "idata_kwargs"}
        sample_kwargs.update(sample_overrides)
        idata = pm.sample(**sample_kwargs)

    var_names = ["alpha", "phi", "sigma_eta"] + [f"beta_{c}" for c in delta_cols] + ["sigma"]
    summary = az.summary(idata, var_names=var_names)

    _RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    summary.to_csv(_RESULTS_DIR / f"{label}_summary.csv")
    idata.to_netcdf(_RESULTS_DIR / f"{label}_idata.nc")

    return {
        "label": label,
        "idata": idata,
        "summary": summary,
        "n": n,
        "sample_index": S["sample_index"],
        "delta_cols": delta_cols,
    }


# ---------------------------------------------------------------------------
# Dashboard tab: diagnostics, historical fit, decomposition, posteriors
# ---------------------------------------------------------------------------
# Reuses the already-fit, already-saved idata (state_space_results/*.nc)
# rather than refitting -- run() must have been run at least once first.

def load_saved(label: str = "primary"):
    path = _RESULTS_DIR / f"{label}_idata.nc"
    if not path.exists():
        raise FileNotFoundError(f"{path} not found -- run state_space_model.run() first.")
    return az.from_netcdf(path)


def _posterior_hist(draws: np.ndarray, bins: int = 40, clip: tuple[float, float] | None = None) -> dict:
    d = draws if clip is None else np.clip(draws, clip[0], clip[1])
    counts, edges = np.histogram(d, bins=bins)
    return {
        "counts": counts.tolist(),
        "edges": [round(float(e), 4) for e in edges],
        "mean": round(float(draws.mean()), 4),
    }


def build_dashboard_payload(label: str = "primary", channels: list[str] | None = None) -> dict:
    """Everything the dashboard's "State-Space (Attempt Two)" tab needs, built
    from the already-saved posterior trace -- no refit.

    Because eta=0, deviation(t-1) is a real observed regressor (not a
    reconstruction from differences the way bayesian_deviation_model.py's
    anchor+cumsum trick is for its differenced spec), so the historical-fit
    reconstruction here is direct: fitted(t) = alpha + phi*deviation(t-1) +
    sum(beta_c * z_c(t)), evaluated per posterior draw.

    The decomposition attributes the deviation LEVEL itself (not just its
    month-to-month change) to each channel's own phi-discounted history --
    user's own catch, 2026-07-24: deviation(t-1) isn't an undifferentiated
    "mean" being reverted to, it's itself alpha + phi*deviation(t-2) +
    sum(beta*z(t-1)) + eps(t-1), i.e. built from the same channels one
    period back. Unrolling the AR(1) recursively, deviation(t) equals a
    phi-discounted sum of every past period's channel flows, drift, and
    shocks, plus the pre-sample initial condition decaying the same way --
    so instead of one lumped "mean-reversion" bucket, each channel gets its
    own running total: contrib_c(t) = phi*contrib_c(t-1) + beta_c*z_c(t),
    same recursion for alpha (drift), the residual (unexplained shocks), and
    the anchor (pre-sample history, now correctly decaying at rate phi
    instead of sitting as a constant baseline forever -- a second thing the
    old reversion-bucket version got wrong). Exact by induction: true at the
    anchor (t0-1), and each step preserves deviation(t) = phi*deviation(t-1)
    + alpha + sum(channel flows) + residual(t), so it reconstructs every
    deviation(t) exactly, not just the sample endpoint. The nominal (BRL/USD)
    bridge converts this same phi-discounted attribution into a level bridge
    from the PPP equilibrium up to the actual PTAX rate, same sequential/
    multiplicative-conversion logic as bayesian_deviation_model.py's own
    level_decomposition -- verified to reconstruct the actual rate exactly
    up to floating point.
    """
    channels = _CHANNELS if channels is None else channels
    idata = load_saved(label)
    df = load_data()
    reg = build_regressors(df, channels=channels)
    delta_cols = [f"delta_{c}" for c in channels]
    sample = reg[["deviation", "deviation_lag1"] + delta_cols].dropna()
    z, _ = _standardize(sample, delta_cols)
    z["deviation_lag1"] = sample["deviation_lag1"]

    months = [d.strftime("%Y-%m") for d in sample.index]

    post = idata.posterior
    alpha_draws = post["alpha"].values.reshape(-1)
    phi_draws = post["phi"].values.reshape(-1)
    beta_draws = {c: post[f"beta_{c}"].values.reshape(-1) for c in delta_cols}
    sigma_draws = post["sigma"].values.reshape(-1)

    # --- diagnostics table ---
    var_names = ["alpha", "phi"] + [f"beta_{c}" for c in delta_cols] + ["sigma"]
    summary = az.summary(idata, var_names=var_names)
    spec_rows = summary.reset_index().rename(columns={"index": "param"}).round(4).to_dict("records")

    # --- half-life ---
    hl = half_life_months(phi_draws)
    hl = hl[np.isfinite(hl)]
    half_life = {
        "mean": round(float(np.mean(hl)), 1),
        "median": round(float(np.median(hl)), 1),
        "hdi_lo": round(float(np.percentile(hl, 3)), 1),
        "hdi_hi": round(float(np.percentile(hl, 97)), 1),
    }
    counts, edges = np.histogram(np.clip(hl, 0, 300), bins=40)
    half_life["hist"] = {"counts": counts.tolist(), "edges": [round(float(e), 2) for e in edges], "capped_at": 300}

    # --- historical fit (level, log-percent deviation) ---
    X = np.column_stack([z[c].values for c in delta_cols])                          # (n_obs, 4)
    Bmat = np.column_stack([beta_draws[c] for c in delta_cols])                     # (n_draws, 4)
    dev_lag1 = z["deviation_lag1"].values                                            # (n_obs,)
    fitted_draws = alpha_draws[:, None] + phi_draws[:, None] * dev_lag1[None, :] + Bmat @ X.T   # (n_draws, n_obs)
    fitted_mean = fitted_draws.mean(axis=0)
    fitted_lo, fitted_hi = np.percentile(fitted_draws, [3, 97], axis=0)
    actual = sample["deviation"].values

    # --- historical fit (nominal ptax), point estimate ---
    equilibrium_level = compute_equilibrium(df).reindex(sample.index).values
    actual_ptax = df["ptax"].reindex(sample.index).values
    fitted_ptax_mean = equilibrium_level * np.exp(fitted_mean / 100)

    # --- decomposition (point estimate, posterior means) ---
    alpha_mean = alpha_draws.mean()
    phi_mean = phi_draws.mean()
    beta_mean = {c: beta_draws[c].mean() for c in delta_cols}

    channel_contrib = {c: beta_mean[c] * z[c].values for c in delta_cols}
    fitted_delta_point = alpha_mean + (phi_mean - 1) * dev_lag1 + sum(channel_contrib.values())
    actual_delta = sample["deviation"].values - sample["deviation_lag1"].values
    residual = actual_delta - fitted_delta_point

    anchor_level = float(sample["deviation_lag1"].iloc[0])

    # Historical (phi-discounted) attribution of the deviation LEVEL -- see
    # docstring. Each bucket is a running total: this period's flow plus
    # phi times last period's running total, so its influence fades at rate
    # phi per month rather than sitting fixed or resetting.
    n = len(sample)
    hist_anchor = np.empty(n)
    hist_alpha = np.empty(n)
    hist_eps = np.empty(n)
    hist_channels = {c: np.empty(n) for c in delta_cols}
    prev_anchor, prev_alpha, prev_eps = anchor_level, 0.0, 0.0
    prev_channels = {c: 0.0 for c in delta_cols}
    for i in range(n):
        hist_anchor[i] = phi_mean * prev_anchor
        hist_alpha[i] = phi_mean * prev_alpha + alpha_mean
        hist_eps[i] = phi_mean * prev_eps + residual[i]
        for c in delta_cols:
            hist_channels[c][i] = phi_mean * prev_channels[c] + channel_contrib[c][i]
        prev_anchor, prev_alpha, prev_eps = hist_anchor[i], hist_alpha[i], hist_eps[i]
        prev_channels = {c: hist_channels[c][i] for c in delta_cols}
    # sanity check: hist_anchor + hist_alpha + sum(hist_channels) + hist_eps == actual deviation level (exactly, by induction)

    decomposition = {
        "anchor": [round(float(v), 4) for v in hist_anchor],
        "alpha": [round(float(v), 4) for v in hist_alpha],
        **{c: [round(float(v), 4) for v in hist_channels[c]] for c in delta_cols},
        "residual": [round(float(v), 4) for v in hist_eps],
    }

    # --- nominal (BRL/USD) bridge decomposition ---
    # Sequential multiplicative bridge -- one factor per channel in delta_cols,
    # in whatever order that list is in, so this generalizes to any channel
    # set (4-channel Kalman tab, 5-channel eta=0 tab with dxy, etc.) without
    # hardcoding channel names.
    level_decomposition = {"equilibrium": [round(float(v), 4) for v in equilibrium_level]}
    running = equilibrium_level
    prev = running
    running = running * np.exp(hist_anchor / 100)
    level_decomposition["anchor"] = [round(float(v), 4) for v in (running - prev)]
    prev = running
    running = running * np.exp(hist_alpha / 100)
    level_decomposition["alpha"] = [round(float(v), 4) for v in (running - prev)]
    for c in delta_cols:
        prev = running
        running = running * np.exp(hist_channels[c] / 100)
        level_decomposition[c] = [round(float(v), 4) for v in (running - prev)]
    prev = running
    running = running * np.exp(hist_eps / 100)  # == actual_ptax exactly, up to floating point
    level_decomposition["residual"] = [round(float(v), 4) for v in (running - prev)]
    level_decomposition["actual"] = [round(float(v), 4) for v in actual_ptax]

    # --- posterior histograms ---
    posteriors = {}
    for coef, draws in {"alpha": alpha_draws, "phi": phi_draws,
                         **{f"beta_{c}": beta_draws[c] for c in delta_cols}, "sigma": sigma_draws}.items():
        posteriors[coef] = _posterior_hist(draws)

    # --- coefficient plot (betas only) ---
    coef_plot = []
    for c in delta_cols:
        row = next(r for r in spec_rows if r["param"] == f"beta_{c}")
        coef_plot.append({"param": f"beta_{c}", "mean": row["mean"], "lo": row["hdi_3%"], "hi": row["hdi_97%"]})

    return {
        "n": int(len(sample)),
        "sample_range": [months[0], months[-1]],
        "months": months,
        "spec": spec_rows,
        "half_life": half_life,
        "fit_level": {
            "actual": [round(float(v), 4) for v in actual],
            "fitted_mean": [round(float(v), 4) for v in fitted_mean],
            "fitted_lo": [round(float(v), 4) for v in fitted_lo],
            "fitted_hi": [round(float(v), 4) for v in fitted_hi],
        },
        "fit_nominal": {
            "actual_ptax": [round(float(v), 4) for v in actual_ptax],
            "equilibrium": [round(float(v), 4) for v in equilibrium_level],
            "fitted_ptax": [round(float(v), 4) for v in fitted_ptax_mean],
        },
        "decomposition": decomposition,
        "level_decomposition": level_decomposition,
        "posteriors": posteriors,
        "coef_plot": coef_plot,
    }


def build_kalman_dashboard_payload(label: str = "kalman", channels: list[str] | None = None) -> dict:
    """Dashboard payload for the free-eta Kalman filter tab (2026-07-24,
    "let's unleash the eta error").

    Because the measurement equation is exact (y(t) = eq_filtered(t) +
    dev_filtered(t), R=0), these two filtered series sum EXACTLY to the
    actual rate on every single posterior draw, not just on average
    (verified: max abs error ~5.7e-14 across all 8000 draws) -- a "fitted
    vs. actual" chart here would just be a tautology, unlike the eta=0
    tab's historical-fit chart (there, deviation was a genuine one-step-
    ahead prediction that could and did differ from the actual value). The
    informative comparison instead is how the filter's eq/dev SPLIT differs
    from the eta=0 model's rigid split (deterministic PPP equilibrium /
    compute_deviation()) -- that's what eq_compare/dev_compare below show.
    A direct consequence of the exact-sum identity: eq_filtered and
    dev_filtered are mirror images of each other across posterior draws --
    whatever pushes one up must push the other down by the same amount, on
    every draw, not just at the mean.
    """
    idata = load_saved(label)
    df = load_data()
    S = build_kf_series(df, channels=channels)
    delta_cols = S["delta_cols"]
    months = S["months"]
    n = len(months)

    post = idata.posterior
    phi_draws = post["phi"].values.reshape(-1)
    alpha_draws = post["alpha"].values.reshape(-1)
    beta_draws = {c: post[f"beta_{c}"].values.reshape(-1) for c in delta_cols}

    # --- diagnostics table ---
    var_names = ["alpha", "phi", "sigma_eta"] + [f"beta_{c}" for c in delta_cols] + ["sigma"]
    summary = az.summary(idata, var_names=var_names)
    spec_rows = summary.reset_index().rename(columns={"index": "param"}).round(4).to_dict("records")

    # --- half-life ---
    hl = half_life_months(phi_draws)
    hl = hl[np.isfinite(hl)]
    half_life = {
        "mean": round(float(np.mean(hl)), 1),
        "median": round(float(np.median(hl)), 1),
        "hdi_lo": round(float(np.percentile(hl, 3)), 1),
        "hdi_hi": round(float(np.percentile(hl, 97)), 1),
    }
    counts, edges = np.histogram(np.clip(hl, 0, 300), bins=40)
    half_life["hist"] = {"counts": counts.tolist(), "edges": [round(float(e), 2) for e in edges], "capped_at": 300}

    # --- filtered eq/dev paths: posterior mean + 94% band, vs. the eta=0 baseline ---
    eq_filtered = post["eq_filtered"].values.reshape(-1, n)   # log-percent units, (n_draws, n)
    dev_filtered = post["dev_filtered"].values.reshape(-1, n)  # log-percent units, (n_draws, n)

    eq_log_mean = eq_filtered.mean(axis=0)
    eq_log_lo, eq_log_hi = np.percentile(eq_filtered, [3, 97], axis=0)
    dev_mean = dev_filtered.mean(axis=0)
    dev_lo, dev_hi = np.percentile(dev_filtered, [3, 97], axis=0)

    equilibrium_det = compute_equilibrium(df).reindex(S["sample_index"]).values
    deviation_det = compute_deviation(df).reindex(S["sample_index"]).values
    actual_ptax = df["ptax"].reindex(S["sample_index"]).values

    eq_compare = {
        "actual_ptax": [round(float(v), 4) for v in actual_ptax],
        "deterministic_ppp": [round(float(v), 4) for v in equilibrium_det],
        "filtered_mean": [round(float(v), 4) for v in np.exp(eq_log_mean / 100)],
        "filtered_lo": [round(float(v), 4) for v in np.exp(eq_log_lo / 100)],
        "filtered_hi": [round(float(v), 4) for v in np.exp(eq_log_hi / 100)],
    }
    dev_compare = {
        "deterministic": [round(float(v), 4) for v in deviation_det],
        "filtered_mean": [round(float(v), 4) for v in dev_mean],
        "filtered_lo": [round(float(v), 4) for v in dev_lo],
        "filtered_hi": [round(float(v), 4) for v in dev_hi],
    }

    # --- historical decomposition of the FILTERED deviation, per posterior draw ---
    # Same phi-discounted attribution as the eta=0 tab, but dev_filtered(t)
    # isn't just alpha + phi*dev(t-1) + channels -- it also carries the
    # Kalman filter's own UPDATE each period (K_dev(t)*v(t), new information
    # the observed rate revealed beyond what the deterministic recursion
    # predicted). That update term isn't attributable to any channel, so it
    # gets its own bucket ("update") rather than being silently folded into
    # one of the real channels. It's backed out directly from what's already
    # in the trace (dev_filtered, alpha/phi/beta draws) -- no need to re-run
    # the filter or have saved the Kalman gain/innovation separately:
    #   update_flow(t) = dev_filtered(t) - [phi*dev_filtered(t-1) + alpha + sum(beta_c*z_c(t))]
    # Done per draw (not at posterior-mean parameters) because the Kalman
    # recursion is nonlinear in phi/sigma_eta/sigma_eps, so a plug-in mean
    # run would NOT exactly reconstruct dev_filtered's true posterior mean
    # the way it did in the eta=0 tab (there the model was linear in the
    # parameters given fixed regressors, so plug-in mean == mean of fits).
    # Averaging each bucket across draws after decomposing every draw
    # avoids that gap: verified to reconstruct dev_filtered.mean(axis=0) to
    # ~1e-13.
    dev0 = S["dev0"]
    hist_anchor_d = np.empty((eq_filtered.shape[0], n))
    hist_alpha_d = np.empty((eq_filtered.shape[0], n))
    hist_update_d = np.empty((eq_filtered.shape[0], n))
    hist_channels_d = {c: np.empty((eq_filtered.shape[0], n)) for c in delta_cols}
    prev_anchor = np.full(eq_filtered.shape[0], dev0)
    prev_alpha = np.zeros(eq_filtered.shape[0])
    prev_update = np.zeros(eq_filtered.shape[0])
    prev_channels = {c: np.zeros(eq_filtered.shape[0]) for c in delta_cols}
    prev_dev = np.full(eq_filtered.shape[0], dev0)
    for t in range(n):
        c_dev_t = alpha_draws + sum(beta_draws[c] * S["z"][c][t] for c in delta_cols)
        dev_pred_t = phi_draws * prev_dev + c_dev_t
        update_flow_t = dev_filtered[:, t] - dev_pred_t

        hist_anchor_d[:, t] = phi_draws * prev_anchor
        hist_alpha_d[:, t] = phi_draws * prev_alpha + alpha_draws
        hist_update_d[:, t] = phi_draws * prev_update + update_flow_t
        for c in delta_cols:
            hist_channels_d[c][:, t] = phi_draws * prev_channels[c] + beta_draws[c] * S["z"][c][t]

        prev_anchor = hist_anchor_d[:, t]
        prev_alpha = hist_alpha_d[:, t]
        prev_update = hist_update_d[:, t]
        prev_channels = {c: hist_channels_d[c][:, t] for c in delta_cols}
        prev_dev = dev_filtered[:, t]

    hist_anchor = hist_anchor_d.mean(axis=0)
    hist_alpha = hist_alpha_d.mean(axis=0)
    hist_update = hist_update_d.mean(axis=0)
    hist_channels = {c: hist_channels_d[c].mean(axis=0) for c in delta_cols}
    # sanity check: hist_anchor + hist_alpha + sum(hist_channels) + hist_update == dev_mean (exactly, up to floating point)

    decomposition = {
        "anchor": [round(float(v), 4) for v in hist_anchor],
        "alpha": [round(float(v), 4) for v in hist_alpha],
        **{c: [round(float(v), 4) for v in hist_channels[c]] for c in delta_cols},
        "update": [round(float(v), 4) for v in hist_update],
    }

    # --- nominal (BRL/USD) bridge, from the FILTERED equilibrium up to the actual rate ---
    # Same generic per-channel chain as build_dashboard_payload()'s bridge --
    # generalizes to any delta_cols set instead of hardcoding channel names.
    lvl_eq = np.exp(eq_log_mean / 100)  # filtered equilibrium (posterior mean), nominal -- same as eq_compare.filtered_mean
    level_decomposition = {"equilibrium": [round(float(v), 4) for v in lvl_eq]}
    running = lvl_eq
    prev = running
    running = running * np.exp(hist_anchor / 100)
    level_decomposition["anchor"] = [round(float(v), 4) for v in (running - prev)]
    prev = running
    running = running * np.exp(hist_alpha / 100)
    level_decomposition["alpha"] = [round(float(v), 4) for v in (running - prev)]
    for c in delta_cols:
        prev = running
        running = running * np.exp(hist_channels[c] / 100)
        level_decomposition[c] = [round(float(v), 4) for v in (running - prev)]
    prev = running
    running = running * np.exp(hist_update / 100)  # == actual_ptax exactly, up to floating point
    level_decomposition["update"] = [round(float(v), 4) for v in (running - prev)]
    level_decomposition["actual"] = [round(float(v), 4) for v in actual_ptax]

    # --- posterior histograms ---
    posteriors = {}
    for coef in var_names:
        draws = post[coef].values.reshape(-1)
        counts_p, edges_p = np.histogram(draws, bins=40)
        posteriors[coef] = {
            "counts": counts_p.tolist(),
            "edges": [round(float(e), 4) for e in edges_p],
            "mean": round(float(draws.mean()), 4),
        }

    # --- coefficient plot (betas only) ---
    coef_plot = []
    for c in delta_cols:
        row = next(r for r in spec_rows if r["param"] == f"beta_{c}")
        coef_plot.append({"param": f"beta_{c}", "mean": row["mean"], "lo": row["hdi_3%"], "hi": row["hdi_97%"]})

    return {
        "n": n,
        "sample_range": [months[0], months[-1]],
        "months": months,
        "spec": spec_rows,
        "half_life": half_life,
        "eq_compare": eq_compare,
        "dev_compare": dev_compare,
        "decomposition": decomposition,
        "level_decomposition": level_decomposition,
        "posteriors": posteriors,
        "coef_plot": coef_plot,
    }


def render_dashboard() -> None:
    """Regenerates referencia/ppp_dashboard.html with its three tabs: PPP/data
    (ppp_equilibrium), the FX cause-attribution tab (fx_attribution_model,
    manager-letter claims), and the Ridge-penalized regression
    (ridge_deviation_model). Requires at least one manager corpus
    hand-extracted under fx_attribution_model.DATA_ROOT to have been done at
    least once first (reads saved claim CSVs, doesn't re-extract) --
    ridge_deviation_model.build_dashboard_payload() needs no saved trace at
    all, cheap enough (milliseconds) to fit fresh on every call.

    Down from eight tabs to three, 2026-07-30, direct user request ("remove
    the other tabs"): the Bayesian Model, State-Space (Attempt Two), Kalman
    Filter (η free), BEER Model (Levels), and Rolling Window (Core 4) tabs
    were removed from the dashboard template entirely. Their own modules
    (bayesian_deviation_model.py, this module's own build_dashboard_payload()/
    build_kalman_dashboard_payload(), beer_model.py) are UNTOUCHED and still
    work standalone -- only the dashboard wiring (this function, and the
    template's markers/tab HTML/JS) was removed. This also retires the
    Kalman-tab staleness bug (build_kalman_dashboard_payload()'s saved trace
    no longer matching load_data()'s current sample length) that used to
    force a surgical single-line RIDGE_DATA replacement instead of calling
    this function directly -- see CLAUDE.md for the full history.

    (A 7th tab, core-4 + election-risk dummy rolling, was built and then
    REMOVED back on 2026-07-24, for unrelated reasons -- see beer_model.py's
    module docstring. That's a separate, earlier removal from this one.)"""
    from analytics.exchange_rate.models import fx_attribution_model
    from analytics.exchange_rate.models import ridge_deviation_model
    from analytics.exchange_rate.models.ppp_equilibrium import _OUTPUT, build_payload, render

    df = load_data()
    ppp_payload = build_payload(df)
    fxattr_payload = fx_attribution_model.build_dashboard_payload()
    ridge_payload = ridge_deviation_model.build_dashboard_payload()
    render(ppp_payload, fxattr_payload=fxattr_payload, ridge_payload=ridge_payload)
    print(f"Full dashboard (three tabs) written to {_OUTPUT}")


if __name__ == "__main__":
    run()
