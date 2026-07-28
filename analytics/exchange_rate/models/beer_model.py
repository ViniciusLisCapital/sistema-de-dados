"""
BEER-style levels model -- USD/BRL (2026-07-24, user-specified equation):

    nominalPtax(t) = PPP(t) * exp( [alpha + sum(B_i * z(channel_i(t))) + eps(t)] / 100 )

i.e. deviation(t) = alpha + B_carry*z(carry(t)) + B_tot*z(tot(t))
                          + B_breakeven*z(breakeven(t)) + B_fiscal*z(fiscal(t))
                          + B_dxy*z(dxy(t)) + B_trade*z(trade_pct_gdp(t))
                          + B_ca*z(ca_pct_gdp(t)) + eps(t)

Distinct from state_space_model.py's "attempt two" in two structural ways,
both literal readings of the user's equation as given (no autoregressive
term, no delta transform written anywhere in it):
  - Channels enter as their own contemporaneous LEVEL (standardized), not a
    month-over-month delta -- attempt two's whole point was that financial
    variables move together in real time, so a lagged level would throw
    that away, but a DELTA was the specific fix for that, not the only one;
    the equation as given here asks for levels directly, a classic BEER/
    "pull factors" reading (deviation from fair value explained by the
    contemporaneous STATE of carry/risk/terms-of-trade/etc., not their
    monthly change).
  - No deviation(t-1)/phi term at all -- attempt two's AR(1)-with-regressors
    structure isn't part of what was asked for here. This is a plain
    static multivariate regression, deviation(t) explained entirely by the
    7 channels' current levels plus a constant and noise -- no persistence
    mechanism of its own. (A consequence: unlike attempt two, this model
    has no "half-life" concept -- there's no phi to derive one from.)

alpha is a deliberate addition beyond the literal equation as written (which
has no constant term) -- omitting it would force the model's unconditional
mean deviation to be exactly zero, an assumption not obviously true and not
stated by the user; kept in for the same reason state_space_model.py's own
alpha was kept (2026-07-24 "let the alpha stay" decision) rather than
assumed away. Flagged here explicitly since it's the one place this model
adds something not in the equation as given.

trade_pct_gdp/ca_pct_gdp are new channels (added to ppp_equilibrium.load_data()
the same day) -- 12m-trailing-sum trade balance / current account, both as %
of 12m-trailing-sum GDP-in-USD, matching generate_report.py's own "% PIB"
convention. A prior throwaway test (scratchpad, not committed) found neither
channel added signal in DELTA form against attempt two's AR(1) spec; this is
a different question -- whether their LEVEL, in a model with no AR term,
carries signal -- so that earlier null result doesn't settle this one.

Decomposition here is much simpler than attempt two's phi-discounted running
history: since deviation(t) has no dependence on deviation(t-1), the
regression IS the decomposition already -- each channel's contribution at
time t is just beta_i * z_i(t), no recursive unrolling needed. The nominal
(BRL/USD) bridge is the same sequential multiplicative conversion used by
every other decomposition chart in this dashboard.

Usage:
    uv run python -c "from analytics.exchange_rate.models.beer_model import run; run()"
"""

from __future__ import annotations

from pathlib import Path

import arviz as az
import numpy as np
import pandas as pd
import pymc as pm
import pytensor.tensor as pt
import statsmodels.api as sm

from analytics.exchange_rate.models.ppp_equilibrium import compute_deviation, compute_equilibrium, load_data
from analytics.exchange_rate.models.state_space_model import _standardize

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

_RESULTS_DIR = Path(__file__).parent / "beer_results"

_SAMPLE_KWARGS = dict(
    draws=2000, tune=1500, chains=4, progressbar=False, random_seed=42,
    target_accept=0.95, idata_kwargs={"log_likelihood": True},
)

_CHANNELS = ["carry", "tot", "breakeven", "fiscal", "dxy", "trade_pct_gdp", "ca_pct_gdp"]

# 5-channel reduced spec (2026-07-24, user request after both the flat-prior
# and regularized-horseshoe (p0=3 and p0=5) fits agreed): drop tot (HDI
# straddled zero in every version) and trade_pct_gdp (collinear with
# ca_pct_gdp -- trade is a large component of current account -- and the one
# channel with a sign contrary to naive expectation). ca_pct_gdp is kept
# over trade_pct_gdp: it matched the theoretically expected sign in every
# fit, trade_pct_gdp never did.
_CHANNELS_REDUCED = ["carry", "breakeven", "fiscal", "dxy", "ca_pct_gdp"]

# "Core 4" (2026-07-24, after a round of channel-swap comparisons): tot never
# showed signal in any spec; ca_pct_gdp FLIPPED SIGN once trade_pct_gdp was
# removed (the two are collinear -- trade is a large component of CA -- so
# CA's earlier "correct sign" wasn't an independent, robust finding);
# trade_pct_gdp itself stayed a stable, significant, "wrong sign" channel
# whether or not CA was present, but was still ultimately dropped by
# explicit user request for this rolling-window check, leaving these four,
# which have been the stable core across every variant tested so far.
_CHANNELS_CORE4 = ["carry", "breakeven", "fiscal", "dxy"]


def build_regressors(df: pd.DataFrame, base_month: str | None = None,
                      channels: list[str] | None = None) -> pd.DataFrame:
    """deviation(t) (level) plus each channel's own CONTEMPORANEOUS LEVEL
    (not a delta -- see module docstring)."""
    channels = _CHANNELS if channels is None else channels
    kwargs = {} if base_month is None else {"base_month": base_month}
    out = pd.DataFrame(index=df.index)
    out["deviation"] = compute_deviation(df, **kwargs)
    for col in channels:
        out[col] = df[col]
    return out


def fit(df: pd.DataFrame | None = None, label: str = "beer", channels: list[str] | None = None) -> dict:
    """deviation(t) = alpha + sum(beta_c * z(channel_c(t))) + eps(t), each
    channel's LEVEL standardized, no lag/AR term. See module docstring for
    why alpha is kept despite not appearing in the equation as given."""
    channels = _CHANNELS if channels is None else channels
    df = load_data() if df is None else df
    reg = build_regressors(df, channels=channels)
    sample = reg[["deviation"] + channels].dropna()
    z, stats = _standardize(sample, channels)

    with pm.Model():
        alpha = pm.Normal("alpha", 0, 10)
        betas = {c: pm.Normal(f"beta_{c}", 0, 2) for c in channels}
        mu = alpha + sum(betas[c] * z[c].values for c in channels)
        sigma = pm.HalfNormal("sigma", 5)
        pm.Normal("y", mu=mu, sigma=sigma, observed=sample["deviation"].values)

        idata = pm.sample(**_SAMPLE_KWARGS)
        idata.extend(pm.sample_posterior_predictive(idata, progressbar=False))

    var_names = ["alpha"] + [f"beta_{c}" for c in channels] + ["sigma"]
    summary = az.summary(idata, var_names=var_names)

    _RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    summary.to_csv(_RESULTS_DIR / f"{label}_summary.csv")
    idata.to_netcdf(_RESULTS_DIR / f"{label}_idata.nc")

    return {
        "label": label, "idata": idata, "summary": summary, "n": len(sample),
        "sample_range": (sample.index.min(), sample.index.max()), "stats": stats,
    }


def rolling_fit(df: pd.DataFrame | None = None, channels: list[str] | None = None,
                 window: int = 60, step: int = 1) -> pd.DataFrame:
    """Rolling-window estimate of the BEER equation -- 2026-07-24 user
    request, checking whether the "core 4" channels' coefficients are stable
    over time or drift/change regime, after a round of channel-swap
    comparisons settled on carry/breakeven/fiscal/dxy as the robust core
    (see _CHANNELS_CORE4's own comment for why tot/trade/ca were all
    dropped).

    OLS + HAC (maxlags=3) per window, NOT a full PyMC re-fit -- explicit
    user choice (asked directly given the wall-clock cost: a monthly step
    over ~220 months is up to ~160 windows, which would be well over an
    hour of full Bayesian re-sampling vs. seconds for OLS). Same OLS+HAC
    estimator carry_model.py already uses elsewhere in this project.

    Channels are standardized ONCE using the FULL SAMPLE's own mean/std, not
    re-standardized per window -- otherwise an apparent shift in a beta
    across windows could just reflect that window's own changing mean/std
    (a moving target), not a real change in the estimated relationship.
    window=60 months (5y) by default; step=1 means every window is
    evaluated (a new window starting each month), not skipped.
    """
    channels = _CHANNELS_CORE4 if channels is None else channels
    df = load_data() if df is None else df
    reg = build_regressors(df, channels=channels)
    sample = reg[["deviation"] + channels].dropna()
    z, _ = _standardize(sample, channels)
    z["deviation"] = sample["deviation"]

    n = len(z)
    rows = []
    for start in range(0, n - window + 1, step):
        win = z.iloc[start:start + window]
        X = sm.add_constant(win[channels])
        res = sm.OLS(win["deviation"], X).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
        ci = res.conf_int()
        row = {
            "window_start": win.index[0], "window_end": win.index[-1],
            "n": len(win), "r2": res.rsquared,
            "alpha": res.params["const"], "alpha_lo": ci.loc["const", 0], "alpha_hi": ci.loc["const", 1],
        }
        for c in channels:
            row[f"beta_{c}"] = res.params[c]
            row[f"beta_{c}_lo"] = ci.loc[c, 0]
            row[f"beta_{c}_hi"] = ci.loc[c, 1]
            row[f"pvalue_{c}"] = res.pvalues[c]
        rows.append(row)

    return pd.DataFrame(rows).set_index("window_end")


def fit_shrinkage(df: pd.DataFrame | None = None, label: str = "beer_hs", p0: float = 3.0,
                   slab_df: float = 4.0, slab_scale: float = 2.0, **sample_overrides) -> dict:
    """Same 7-channel BEER equation as fit(), but with the flat Normal(0,2)
    betas replaced by a REGULARIZED HORSEHOE prior (Piironen & Vehtari 2017)
    -- 2026-07-24 user request, motivated directly by the flat-prior fit's
    own flagged caveat: trade_pct_gdp/ca_pct_gdp are highly collinear (trade
    is a large component of CA) and the spec has no AR term/time-trend
    control, so a spurious or unstable coefficient on either is a real risk.
    Horseshoe shrinkage is the standard fix for "which of several correlated
    regressors actually matters": each beta gets its own local-shrinkage
    scale (lambda_c) alongside a shared global scale (tau), so channels with
    real signal (expected: dxy, fiscal, breakeven -- all decisively
    significant in the flat-prior fit) can escape shrinkage while weak/
    collinear ones (expected: tot, and possibly one or both of trade/ca) get
    pulled toward zero. The "regularized" (Finnish) variant caps each
    lambda_c so a spuriously huge one can't blow up its beta unboundedly --
    plain horseshoe has no such cap and can misbehave in exactly this kind
    of small-p, collinear regime.

        beta_c = tau * lambda_tilde_c * z_c,           z_c ~ Normal(0,1)   [non-centered]
        lambda_tilde_c^2 = c2 * lambda_c^2 / (c2 + tau^2 * lambda_c^2)
        lambda_c ~ HalfCauchy(1)                        (local shrinkage, one per channel)
        tau ~ HalfCauchy(tau0)                           (global shrinkage)
        c2 ~ InverseGamma(slab_df/2, slab_df/2 * slab_scale^2)   (slab variance, caps lambda_tilde)

    tau0 = p0/(p-p0) * sigma_guess/sqrt(n) sets the prior's expected number
    of "relevant" covariates to p0 (out of p=7 total) -- NOT re-estimated
    from the fit's own sigma (that would make the prior data-dependent in a
    circular way), just a plug-in guess (sample std of the deviation) used
    once to scale the hyperprior, per Piironen & Vehtari's own recommended
    construction. p0=3 here is a deliberately modest guess (fewer than half
    the 7 channels) rather than a claim about which ones -- the whole point
    of the shrinkage prior is to let the data decide that, not to encode it
    in tau0.

    Non-centered parameterization throughout (z_c ~ Normal(0,1), scale
    applied afterward) plus target_accept=0.99 and extra tuning -- horseshoe
    posteriors have a well-known funnel geometry that the default target
    of 0.95 tends to under-sample (visible as divergences).
    """
    df = load_data() if df is None else df
    reg = build_regressors(df)
    sample = reg[["deviation"] + _CHANNELS].dropna()
    z, stats = _standardize(sample, _CHANNELS)
    y = sample["deviation"].values
    n, p = len(sample), len(_CHANNELS)

    sigma_guess = float(np.std(y))
    tau0 = (p0 / (p - p0)) * (sigma_guess / np.sqrt(n))
    X = np.column_stack([z[c].values for c in _CHANNELS])

    with pm.Model():
        alpha = pm.Normal("alpha", 0, 10)

        tau = pm.HalfCauchy("tau", beta=tau0)
        c2 = pm.InverseGamma("c2", alpha=slab_df / 2, beta=slab_df / 2 * slab_scale ** 2)
        lam = pm.HalfCauchy("lam", beta=1, shape=p)
        lam_tilde = pt.sqrt(c2 * lam ** 2 / (c2 + tau ** 2 * lam ** 2))
        z_raw = pm.Normal("z_raw", 0, 1, shape=p)
        beta_vec = pm.Deterministic("beta_vec", z_raw * tau * lam_tilde)
        for i, c in enumerate(_CHANNELS):
            pm.Deterministic(f"beta_{c}", beta_vec[i])

        mu = alpha + pt.dot(pt.as_tensor_variable(X), beta_vec)
        sigma = pm.HalfNormal("sigma", 5)
        pm.Normal("y", mu=mu, sigma=sigma, observed=y)

        sample_kwargs = dict(draws=2000, tune=3000, chains=4, progressbar=False,
                              random_seed=42, target_accept=0.99)
        sample_kwargs.update(sample_overrides)
        idata = pm.sample(**sample_kwargs)

    var_names = ["alpha"] + [f"beta_{c}" for c in _CHANNELS] + ["tau", "sigma"]
    summary = az.summary(idata, var_names=var_names)

    _RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    summary.to_csv(_RESULTS_DIR / f"{label}_summary.csv")
    idata.to_netcdf(_RESULTS_DIR / f"{label}_idata.nc")

    return {
        "label": label, "idata": idata, "summary": summary, "n": len(sample),
        "sample_range": (sample.index.min(), sample.index.max()), "stats": stats,
        "tau0": tau0, "p0": p0,
    }


def sign_probability(idata, coef_name: str, expected_positive: bool) -> float:
    draws = idata.posterior[coef_name].values.flatten()
    return float((draws > 0).mean()) if expected_positive else float((draws < 0).mean())


def run() -> dict:
    df = load_data()
    print("=" * 78)
    print("BEER-STYLE LEVELS MODEL -- nominal ptax, 7 channels (levels, no AR term)")
    result = fit(df, label="beer")
    print(result["summary"])
    print(f"n={result['n']}  range={[d.strftime('%Y-%m') for d in result['sample_range']]}")
    return result


# ---------------------------------------------------------------------------
# Dashboard tab: diagnostics, historical fit, decomposition, posteriors
# ---------------------------------------------------------------------------

def load_saved(label: str = "beer"):
    path = _RESULTS_DIR / f"{label}_idata.nc"
    if not path.exists():
        raise FileNotFoundError(f"{path} not found -- run beer_model.run() first.")
    return az.from_netcdf(path)


def _posterior_hist(draws: np.ndarray, bins: int = 40) -> dict:
    counts, edges = np.histogram(draws, bins=bins)
    return {
        "counts": counts.tolist(),
        "edges": [round(float(e), 4) for e in edges],
        "mean": round(float(draws.mean()), 4),
    }


def build_dashboard_payload(label: str = "beer", channels: list[str] | None = None) -> dict:
    """Everything a BEER-model dashboard tab needs, built from the already-
    saved posterior trace -- no refit. See module docstring: since there's
    no AR term, the decomposition needs no recursive unrolling -- it's
    exactly the regression itself, term by term."""
    channels = _CHANNELS if channels is None else channels
    idata = load_saved(label)
    df = load_data()
    reg = build_regressors(df, channels=channels)
    sample = reg[["deviation"] + channels].dropna()
    z, _ = _standardize(sample, channels)

    months = [d.strftime("%Y-%m") for d in sample.index]

    post = idata.posterior
    alpha_draws = post["alpha"].values.reshape(-1)
    beta_draws = {c: post[f"beta_{c}"].values.reshape(-1) for c in channels}
    sigma_draws = post["sigma"].values.reshape(-1)

    # --- diagnostics table ---
    var_names = ["alpha"] + [f"beta_{c}" for c in channels] + ["sigma"]
    summary = az.summary(idata, var_names=var_names)
    spec_rows = summary.reset_index().rename(columns={"index": "param"}).round(4).to_dict("records")

    # --- historical fit (level, log-percent deviation) ---
    X = np.column_stack([z[c].values for c in channels])                        # (n_obs, p)
    Bmat = np.column_stack([beta_draws[c] for c in channels])                   # (n_draws, p)
    fitted_draws = alpha_draws[:, None] + Bmat @ X.T                              # (n_draws, n_obs)
    fitted_mean = fitted_draws.mean(axis=0)
    fitted_lo, fitted_hi = np.percentile(fitted_draws, [3, 97], axis=0)
    actual = sample["deviation"].values

    # --- historical fit (nominal ptax), point estimate ---
    equilibrium_level = compute_equilibrium(df).reindex(sample.index).values
    actual_ptax = df["ptax"].reindex(sample.index).values
    fitted_ptax_mean = equilibrium_level * np.exp(fitted_mean / 100)

    # --- decomposition (point estimate, posterior means) --- no AR term, so
    # this is just the regression's own terms, no recursive unrolling needed.
    alpha_mean = alpha_draws.mean()
    beta_mean = {c: beta_draws[c].mean() for c in channels}
    channel_contrib = {c: beta_mean[c] * z[c].values for c in channels}
    fitted_point = alpha_mean + sum(channel_contrib.values())
    residual = actual - fitted_point

    decomposition = {
        "alpha": [round(float(alpha_mean), 4) for _ in range(len(sample))],
        **{c: [round(float(v), 4) for v in channel_contrib[c]] for c in channels},
        "residual": [round(float(v), 4) for v in residual],
    }

    # --- nominal (BRL/USD) bridge decomposition ---
    level_decomposition = {"equilibrium": [round(float(v), 4) for v in equilibrium_level]}
    running = equilibrium_level
    prev = running
    running = running * np.exp(np.full(len(sample), alpha_mean) / 100)
    level_decomposition["alpha"] = [round(float(v), 4) for v in (running - prev)]
    for c in channels:
        prev = running
        running = running * np.exp(channel_contrib[c] / 100)
        level_decomposition[c] = [round(float(v), 4) for v in (running - prev)]
    prev = running
    running = running * np.exp(residual / 100)  # == actual_ptax exactly, up to floating point
    level_decomposition["residual"] = [round(float(v), 4) for v in (running - prev)]
    level_decomposition["actual"] = [round(float(v), 4) for v in actual_ptax]

    # --- posterior histograms ---
    posteriors = {}
    for coef, draws in {"alpha": alpha_draws, **{f"beta_{c}": beta_draws[c] for c in channels},
                         "sigma": sigma_draws}.items():
        posteriors[coef] = _posterior_hist(draws)

    # --- coefficient plot (betas only) ---
    coef_plot = []
    for c in channels:
        row = next(r for r in spec_rows if r["param"] == f"beta_{c}")
        coef_plot.append({"param": f"beta_{c}", "mean": row["mean"], "lo": row["hdi_3%"], "hi": row["hdi_97%"]})

    return {
        "n": int(len(sample)),
        "sample_range": [months[0], months[-1]],
        "months": months,
        "spec": spec_rows,
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


def build_rolling_payload(channels: list[str] | None = None, window: int = 60, step: int = 1,
                           whole_sample_label: str = "beer_core4") -> dict:
    """Dashboard payload for the "Rolling Window" tab (2026-07-24 user
    request, after settling on the core-4 channel set): rolling_fit()'s
    output plus the corresponding whole-sample fit's own posterior means,
    so the dashboard can draw each rolling parameter against its whole-
    sample reference line -- same comparison as the earlier scratchpad
    artifact, just re-embedded as dashboard data instead of a separate page.
    whole_sample_label must point at an already-saved fit() run on the SAME
    channel set (default: beer_core4, the 4-channel carry/breakeven/fiscal/
    dxy spec that survived the tot/trade/ca elimination rounds)."""
    channels = _CHANNELS_CORE4 if channels is None else channels
    roll = rolling_fit(channels=channels, window=window, step=step)
    whole = load_saved(whole_sample_label)

    out = {
        "window_months": window,
        "n_windows": len(roll),
        "window_end": [d.strftime("%Y-%m") for d in roll.index],
        "r2": [round(float(v), 4) for v in roll["r2"]],
        "alpha": {
            "mean": [round(float(v), 4) for v in roll["alpha"]],
            "lo": [round(float(v), 4) for v in roll["alpha_lo"]],
            "hi": [round(float(v), 4) for v in roll["alpha_hi"]],
            "whole_sample": round(float(whole.posterior["alpha"].values.mean()), 4),
        },
        "channels": {},
    }
    for c in channels:
        out["channels"][c] = {
            "mean": [round(float(v), 4) for v in roll[f"beta_{c}"]],
            "lo": [round(float(v), 4) for v in roll[f"beta_{c}_lo"]],
            "hi": [round(float(v), 4) for v in roll[f"beta_{c}_hi"]],
            "whole_sample": round(float(whole.posterior[f"beta_{c}"].values.mean()), 4),
        }
    return out


if __name__ == "__main__":
    run()
