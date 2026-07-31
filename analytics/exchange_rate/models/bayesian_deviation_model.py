"""
Bayesian regression of the USD/BRL PPP deviation on carry / terms-of-trade /
long-term inflation expectations / fiscal risk — "attempt one", see
bayesian_deviation_model.md for the full design writeup and rationale.

Pre-registered decision (2026-07-23, before any model code was written):
run ADF + KPSS on the deviation series and all four candidate regressors,
and let the result decide levels vs. first-differences. Result (see
bayesian_deviation_model.md "Results" section for the full table):
`deviation`, `carry`, and `tot` all test as I(1) (ADF fails to reject a unit
root, KPSS rejects stationarity — both tests agree). `breakeven` and `fiscal`
test as I(0) in levels. Regressing an I(1) `deviation` on a mix of I(1) and
I(0) regressors risks the classic spurious-regression problem for the I(1)
pairs specifically — so per the pre-registered rule, this model uses the
**first-difference specification uniformly** (all five series differenced),
not a mixed levels/differences spec. That's a deliberate simplification for
"attempt one", not a claim that differencing `breakeven`/`fiscal` is
information-free — see the .md's Results section for the caveat.

    delta_D(t) = alpha + b1*delta_carry(t-1) + b2*delta_tot(t-1)
                       + b3*delta_breakeven(t-1) + b4*delta_fiscal(t-1) + eps(t)

Two specs (per the .md's sample-window plan):
  primary     all 4 regressors, sample = their overlap (fiscal is the binding
              constraint, ~2008-02 onward once diff+lag are applied)
  robustness  carry + tot only, much longer sample (~1999-05 onward)

Also fits the primary spec with `breakeven_gap` (breakeven - inflc_meta, the
de-anchoring gap) in place of raw `breakeven`, to resolve that open design
question, and compares Normal vs. Student-t error models on the primary spec.

Usage:
    uv run python -c "from analytics.exchange_rate.models.bayesian_deviation_model import run; run()"
"""

from __future__ import annotations

from pathlib import Path

import arviz as az
import numpy as np
import pandas as pd
import pymc as pm

from analytics.exchange_rate.models.ppp_equilibrium import compute_deviation, compute_equilibrium, load_data

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

_RESULTS_DIR = Path(__file__).parent / "bayesian_results"

_SAMPLE_KWARGS = dict(
    draws=2000, tune=1500, chains=4, progressbar=False, random_seed=42,
    target_accept=0.9, idata_kwargs={"log_likelihood": True},
)


def build_deltas(df: pd.DataFrame) -> pd.DataFrame:
    """First-differenced, 1-month-lagged regressors alongside delta_D(t).

    Also carries deviation_lag1 = deviation(t-1) — the lagged LEVEL, not a
    difference — for the error-correction spec added 2026-07-23 ("Option B"):
    delta_dev(t) = alpha + rho*deviation(t-1) + betas*(4 channel deltas) +
    eps(t). This is a Dickey-Fuller-type regression (a series' own first
    difference on its own lagged level), not a repeat of the spurious-
    regression risk the rest of this model's differencing avoids."""
    dev = compute_deviation(df)
    out = pd.DataFrame(index=df.index)
    out["delta_dev"] = dev.diff()
    out["deviation_lag1"] = dev.shift(1)
    for col in ("carry", "tot", "breakeven", "breakeven_gap", "fiscal"):
        out[f"delta_{col}"] = df[col].diff().shift(1)
    return out


def build_deltas_contemporaneous(df: pd.DataFrame) -> pd.DataFrame:
    """Same as build_deltas() but regressors enter as Δchannel(t) — no extra
    1-month lag — matching state_space_model.py's contemporaneous timing
    choice rather than this module's original lagged convention. Added
    2026-07-28 for the not-lagged carry/cds/breakeven_gap/dxy spec (see
    fit_contemp_spec()); also carries delta_dxy, which build_deltas() never
    needed since the original 4-channel spec didn't use it. delta_relative_carry
    added same day, alongside (not replacing) delta_carry — see
    fit_contemp_spec()'s docstring. curve_steep (BR nominal 10Y-2Y yield
    curve steepening, PREJS@120M-24M — see
    ppp_equilibrium._load_curve_steepening()) added 2026-07-30, an alternate
    market-based fiscal-risk proxy tested alongside the CDS-based `fiscal`
    channel in ridge_deviation_model.py's shrunk AR(1) spec. curve_steep_real
    (REAL 10Y-2Y steepening, NTNBJS@120M-24M) and dxy_em (Fed Broad-EM dollar
    index, FRED DTWEXEMEGS) added 2026-07-31, testing (i) whether the real
    term premium captures domestic fiscal risk CDS misses (Brazil's USD
    reserve buffer keeps external-default-priced CDS muted even when
    domestic debt dynamics worsen) and (ii) EM-specific FX co-movement
    alongside the broad/G10-heavy dxy channel."""
    dev = compute_deviation(df)
    out = pd.DataFrame(index=df.index)
    out["delta_dev"] = dev.diff()
    out["deviation_lag1"] = dev.shift(1)
    for col in ("carry", "relative_carry", "carry_vol", "relative_carry_vol", "tot", "breakeven", "breakeven_gap",
                "fiscal", "dxy", "dxy_em", "curve_steep", "curve_steep_real"):
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


_REFERENCE_START = "2000-01-01"


def _standardize_ext(sample: pd.DataFrame, reference: pd.DataFrame, cols: list[str]) -> tuple[pd.DataFrame, dict]:
    """Like _standardize(), but each column's mean/std comes from `reference`
    instead of from `sample` itself -- added 2026-07-28 at the user's direct
    request: the fitting sample (`sample`) is bound to the narrow overlap
    where ALL regressors are simultaneously available (fiscal/CDS, 2007-12+,
    forces the whole primary_contemp spec to start 2008-01), but carry/
    relative_carry/dxy all have much longer real history on their own --
    z-scoring them against only the narrow 2008+ window throws that longer
    history away for no reason tied to any actual data limitation of THOSE
    channels specifically.

    `reference` can be longer than `sample`, need not share its index, and
    each column's stats are computed independently over its own non-null
    rows in `reference` (dropna() per-column, not a single joint dropna()
    the way _standardize()/fit_regression()'s `sample` construction does)
    -- so e.g. delta_carry's mean/std reflect its own 2000-01+ history even
    though delta_fiscal's still effectively reflect only 2007-12+ (fiscal
    simply has no earlier data to draw on, reference window or not)."""
    stats = {}
    z = sample.copy()
    for c in cols:
        ref_col = reference[c].dropna()
        mu, sd = ref_col.mean(), ref_col.std()
        z[c] = (sample[c] - mu) / sd
        stats[c] = (mu, sd)
    return z, stats


def fit_regression(frame: pd.DataFrame, regressor_cols: list[str], student_t: bool = False, label: str = "", no_intercept: bool = False, raw_cols: list[str] | None = None, reference: pd.DataFrame | None = None) -> dict:
    """Fit delta_dev ~ regressor_cols (already differenced/lagged) via PyMC.
    Regressors are standardized before fitting so a single weakly-informative
    prior works regardless of native units — EXCEPT columns named in
    raw_cols, kept in their native units.

    reference: if given, standardization uses _standardize_ext() (each
    column's own mean/std computed from `reference`, e.g. a longer
    2000-01+ window) instead of _standardize() (mean/std from `sample`
    itself, i.e. the model's own narrow fitting-sample overlap). See
    _standardize_ext()'s docstring for why this matters.

    raw_cols matters: standardizing (z-scoring) a column always forces its
    sample mean to exactly 0, which mechanically prevents it from ever
    explaining a nonzero mean in the dependent variable — that mean can only
    land on alpha, or, with no_intercept, on the residual (found the hard way
    2026-07-23: the no-intercept spec below left the betas unchanged and
    just relabeled the drift as residual, because all 4 regressors are
    standardized). deviation_lag1 (the error-correction spec, "Option B") is
    passed via raw_cols for exactly this reason — its own sample mean is
    genuinely nonzero (+14.7 over the primary sample), which is precisely
    what would let it explain the drift, but only if that nonzero mean
    survives into the fit.

    no_intercept forces alpha to 0 (regression through the origin) — added
    2026-07-23 at the user's request, to test the claim "PPP should be the
    only systematic directional drift over time": if that's right, the betas
    on carry/tot/breakeven/fiscal should be able to explain the deviation's
    average monthly change without a free constant standing in for whatever
    they miss. See bayesian_deviation_model.md for the result."""
    raw_cols = raw_cols or []
    sample = frame[["delta_dev"] + regressor_cols].dropna()
    standardize_cols = [c for c in regressor_cols if c not in raw_cols]
    if reference is None:
        z, stats = _standardize(sample, standardize_cols)
    else:
        z, stats = _standardize_ext(sample, reference, standardize_cols)
    for c in raw_cols:
        z[c] = sample[c]
        stats[c] = (0.0, 1.0)  # identity — kept in native units, not standardized

    with pm.Model() as model:
        betas = {c: pm.Normal(f"beta_{c}", 0, 2) for c in regressor_cols}
        mu = sum(betas[c] * z[c].values for c in regressor_cols)
        if not no_intercept:
            alpha = pm.Normal("alpha", 0, 10)
            mu = alpha + mu

        if student_t:
            nu = pm.Gamma("nu", alpha=2, beta=0.1)
            sigma = pm.HalfNormal("sigma", 5)
            pm.StudentT("y", nu=nu, mu=mu, sigma=sigma, observed=z["delta_dev"].values)
        else:
            sigma = pm.HalfNormal("sigma", 5)
            pm.Normal("y", mu=mu, sigma=sigma, observed=z["delta_dev"].values)

        idata = pm.sample(**_SAMPLE_KWARGS)
        idata.extend(pm.sample_posterior_predictive(idata, progressbar=False))

    var_names = ([] if no_intercept else ["alpha"]) + [f"beta_{c}" for c in regressor_cols] + (["nu"] if student_t else [])
    summary = az.summary(idata, var_names=var_names)
    if label:
        _RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        summary.to_csv(_RESULTS_DIR / f"{label}_summary.csv")
        idata.to_netcdf(_RESULTS_DIR / f"{label}_idata.nc")
    return {
        "label": label,
        "idata": idata,
        "summary": summary,
        "n": len(sample),
        "sample_range": (sample.index.min(), sample.index.max()),
        "stats": stats,
        "regressor_cols": regressor_cols,
        "no_intercept": no_intercept,
    }


def fit_no_intercept_spec() -> dict:
    """Test spec, 2026-07-23 user request: refit the primary_breakeven spec
    with the intercept removed (forced through the origin), to see whether
    carry/tot/breakeven/fiscal can explain the deviation's average monthly
    move on their own, or whether a large drift persists even without a free
    constant available to absorb it."""
    df = load_data()
    deltas = build_deltas(df)
    print("=" * 78)
    print("NO-INTERCEPT SPEC — carry + tot + breakeven + fiscal, deltas, lag-1, alpha forced to 0")
    result = fit_regression(
        deltas, ["delta_carry", "delta_tot", "delta_breakeven", "delta_fiscal"],
        student_t=False, label="primary_no_alpha", no_intercept=True,
    )
    print(result["summary"])
    print(f"n={result['n']}  range={[d.strftime('%Y-%m') for d in result['sample_range']]}")
    return result


def fit_ecm_spec() -> dict:
    """Error-correction test spec, 2026-07-23 user request ("Option B", alpha
    kept): adds deviation_lag1 (the lagged deviation LEVEL) alongside the 4
    channel deltas. If PPP pulls deviations back toward zero over time, rho
    (beta_deviation_lag1) should come out reliably negative — the further
    the currency has drifted, the more it should correct the following
    month. Keeping alpha lets us see whether the drift found in the original
    primary_breakeven spec (alpha=0.219) shrinks once genuine mean-reversion
    is allowed for, or survives regardless."""
    df = load_data()
    deltas = build_deltas(df)
    print("=" * 78)
    print("ERROR-CORRECTION SPEC — deviation_lag1 (raw units) + carry/tot/breakeven/fiscal deltas (standardized), alpha kept")
    result = fit_regression(
        deltas, ["deviation_lag1", "delta_carry", "delta_tot", "delta_breakeven", "delta_fiscal"],
        student_t=False, label="primary_ecm", no_intercept=False, raw_cols=["deviation_lag1"],
    )
    print(result["summary"])
    print(f"n={result['n']}  range={[d.strftime('%Y-%m') for d in result['sample_range']]}")
    return result


def fit_contemp_spec() -> dict:
    """Not-lagged spec, 2026-07-28 user request: carry + fiscal (CDS) +
    breakeven_gap (de-anchoring) + DXY, contemporaneous deltas (no extra
    1-month lag) via build_deltas_contemporaneous() — replacing the tab's
    original carry/tot/breakeven/fiscal lagged spec, per direct user
    instruction ("it's not necessary to run the other specifications").
    DXY is new to this module (state_space_model.py/beer_model.py already
    use it); breakeven_gap over raw breakeven, matching the user's own
    "de-anchoring breakeven" framing. Saved under label "primary_contemp" —
    the dashboard's build_dashboard_payload() reads this and only this.

    relative_carry added same day, alongside (not replacing) carry, per
    direct user choice: Selic minus the equal-weighted MX/CL/CO/PE policy
    rate average (see ppp_equilibrium._load_relative_carry()) — testing
    whether Brazil's rate positioning RELATIVE TO ITS LATAM PEERS explains
    the deviation beyond the bilateral BR-US differential `carry` already
    captures.

    Standardization reference window changed 2026-07-28 (direct user
    request, after the tab-1 z-score toggle discussion surfaced the same
    question for this model): each regressor's mean/std for z-scoring now
    comes from `reference` = deltas from 2000-01 onward (_REFERENCE_START),
    NOT from `sample` (the model's own narrow 2008-01+ fitting overlap,
    forced by fiscal/CDS's late start). carry/relative_carry/dxy all have
    real history well before 2008 that was previously discarded for a
    reason (fiscal's start) unrelated to THEIR OWN data availability.
    fiscal/breakeven_gap are effectively unaffected (their own real start,
    2007-12/2006-01, is already later than 2000-01)."""
    df = load_data()
    deltas = build_deltas_contemporaneous(df)
    reference = deltas[deltas.index >= _REFERENCE_START]
    print("=" * 78)
    print("CONTEMPORANEOUS SPEC — carry + relative_carry + fiscal (CDS) + breakeven_gap (de-anchoring) + DXY, deltas, no lag")
    print(f"Standardization reference window: {_REFERENCE_START} -> latest (not the narrower fitting sample)")
    result = fit_regression(
        deltas, ["delta_carry", "delta_relative_carry", "delta_fiscal", "delta_breakeven_gap", "delta_dxy"],
        student_t=False, label="primary_contemp", reference=reference,
    )
    print(result["summary"])
    print(f"n={result['n']}  range={[d.strftime('%Y-%m') for d in result['sample_range']]}")
    return result


def sign_probability(idata, coef_name: str, expected_positive: bool) -> float:
    draws = idata.posterior[coef_name].values.flatten()
    return float((draws > 0).mean()) if expected_positive else float((draws < 0).mean())


def run() -> dict:
    df = load_data()
    deltas = build_deltas(df)

    results = {}

    print("=" * 78)
    print("PRIMARY SPEC (breakeven) — carry + tot + breakeven + fiscal, deltas, lag-1")
    results["primary_breakeven"] = fit_regression(
        deltas, ["delta_carry", "delta_tot", "delta_breakeven", "delta_fiscal"],
        student_t=False, label="primary_breakeven",
    )
    print(results["primary_breakeven"]["summary"])
    print(f"n={results['primary_breakeven']['n']}  range={[d.strftime('%Y-%m') for d in results['primary_breakeven']['sample_range']]}")

    print("=" * 78)
    print("PRIMARY SPEC (breakeven_gap) — carry + tot + breakeven_gap + fiscal, deltas, lag-1")
    results["primary_gap"] = fit_regression(
        deltas, ["delta_carry", "delta_tot", "delta_breakeven_gap", "delta_fiscal"],
        student_t=False, label="primary_gap",
    )
    print(results["primary_gap"]["summary"])

    print("=" * 78)
    print("PRIMARY SPEC (breakeven) — Student-t errors, same regressors")
    results["primary_studentt"] = fit_regression(
        deltas, ["delta_carry", "delta_tot", "delta_breakeven", "delta_fiscal"],
        student_t=True, label="primary_studentt",
    )
    print(results["primary_studentt"]["summary"])

    print("=" * 78)
    print("Normal vs. Student-t model comparison (LOO)")
    cmp = az.compare({"normal": results["primary_breakeven"]["idata"], "student_t": results["primary_studentt"]["idata"]})
    print(cmp)
    results["error_model_comparison"] = cmp

    print("=" * 78)
    print("ROBUSTNESS SPEC — carry + tot only, deltas, lag-1 (longer sample)")
    results["robustness"] = fit_regression(
        deltas, ["delta_carry", "delta_tot"],
        student_t=False, label="robustness",
    )
    print(results["robustness"]["summary"])
    print(f"n={results['robustness']['n']}  range={[d.strftime('%Y-%m') for d in results['robustness']['sample_range']]}")

    print("=" * 78)
    print("Sign checks (P(beta has expected sign)):")
    expected_signs = {
        "beta_delta_carry": None,  # no strong prior expectation, see .md
        "beta_delta_tot": False,   # expected negative
        "beta_delta_breakeven": True,
        "beta_delta_breakeven_gap": True,
        "beta_delta_fiscal": True,
    }
    for spec_name in ("primary_breakeven", "primary_gap", "robustness"):
        idata = results[spec_name]["idata"]
        for coef in results[spec_name]["regressor_cols"]:
            name = f"beta_{coef}"
            expected = expected_signs.get(name)
            if expected is None:
                continue
            p = sign_probability(idata, name, expected)
            print(f"  [{spec_name}] P({name} {'>' if expected else '<'} 0) = {p:.3f}")

    return results


# ---------------------------------------------------------------------------
# Dashboard tab: descriptive stats, historical fit, decomposition
# ---------------------------------------------------------------------------
# Reuses the already-fit, already-saved idata (bayesian_results/*.nc) rather
# than refitting — run() must have been run at least once first.

_SPEC_FILES = {
    "primary_contemp": ["delta_carry", "delta_relative_carry", "delta_fiscal", "delta_breakeven_gap", "delta_dxy"],
}


def load_saved(label: str):
    path = _RESULTS_DIR / f"{label}_idata.nc"
    if not path.exists():
        raise FileNotFoundError(f"{path} not found — run bayesian_deviation_model.fit_contemp_spec() first.")
    return az.from_netcdf(path)


def _summary_records(idata, regressor_cols: list[str]) -> list[dict]:
    var_names = ["alpha"] + [f"beta_{c}" for c in regressor_cols]
    summary = az.summary(idata, var_names=var_names)
    records = summary.reset_index().rename(columns={"index": "param"})
    return records.round(4).to_dict("records")


def build_dashboard_payload() -> dict:
    """Dashboard payload for the "Bayesian Model" tab — rebuilt 2026-07-28
    around the single not-lagged carry/cds/breakeven_gap/dxy spec
    ("primary_contemp") at direct user request, replacing the original
    4-spec (primary_breakeven/primary_gap/primary_studentt/robustness)
    comparison. Those specs' saved traces are untouched on disk but no
    longer read here — no cross-spec forest plot or Normal-vs-Student-t
    comparison, since both required multiple specs sharing a channel set
    that this replacement spec doesn't share with them. Posterior-
    distribution histograms also dropped, per explicit user request.
    relative_carry added alongside carry the same day (see
    fit_contemp_spec()) — still a single spec, now 5 regressors.
    Standardization reference window (2000-01+, not the narrow fitting
    sample) matched to fit_contemp_spec()'s own change, same day -- see
    _standardize_ext()'s docstring."""
    label = "primary_contemp"
    regressor_cols = _SPEC_FILES[label]
    idata = load_saved(label)
    df = load_data()
    deltas = build_deltas_contemporaneous(df)

    # --- descriptive stats / diagnostics (single spec) ---
    spec_summary = _summary_records(idata, regressor_cols)
    sample = deltas[["delta_dev"] + regressor_cols].dropna()
    spec_meta = {
        "n": int(len(sample)),
        "sample_range": [sample.index.min().strftime("%Y-%m"), sample.index.max().strftime("%Y-%m")],
    }

    # --- historical fit + decomposition (primary_contemp spec) ---
    # Must match fit_contemp_spec()'s own standardization exactly (same
    # reference window) -- otherwise the z-values fed into the point
    # decomposition below wouldn't correspond to the betas actually fit.
    reference = deltas[deltas.index >= _REFERENCE_START]
    z, _ = _standardize_ext(sample, reference, regressor_cols)

    post = idata.posterior
    alpha_draws = post["alpha"].values.reshape(-1)
    beta_draws = {c: post[f"beta_{c}"].values.reshape(-1) for c in regressor_cols}

    X = np.column_stack([z[c].values for c in regressor_cols])          # (n_obs, n_reg)
    B = np.column_stack([beta_draws[c] for c in regressor_cols])         # (n_draws, n_reg)
    fitted_draws = alpha_draws[:, None] + B @ X.T                        # (n_draws, n_obs)

    fitted_delta_mean = fitted_draws.mean(axis=0)
    fitted_delta_lo, fitted_delta_hi = np.percentile(fitted_draws, [3, 97], axis=0)
    actual_delta = sample["delta_dev"].values

    dev_full = compute_deviation(df)
    anchor_date = sample.index[0] - pd.DateOffset(months=1)
    anchor_level = float(dev_full.loc[anchor_date])  # dev_full is a continuous monthly ("MS") series, so this is an exact lookup

    fitted_level_draws = anchor_level + np.cumsum(fitted_draws, axis=1)  # (n_draws, n_obs)
    fitted_level_mean = fitted_level_draws.mean(axis=0)
    fitted_level_lo, fitted_level_hi = np.percentile(fitted_level_draws, [3, 97], axis=0)
    actual_level = dev_full.reindex(sample.index).values

    # point decomposition (posterior-mean betas): contribution_i(t) = beta_i_mean * z_i(t)
    beta_mean = {c: beta_draws[c].mean() for c in regressor_cols}
    alpha_mean = alpha_draws.mean()
    contributions = {c: beta_mean[c] * z[c].values for c in regressor_cols}
    fitted_point = alpha_mean + sum(contributions.values())
    residual = actual_delta - fitted_point

    cum_alpha = np.cumsum(np.full(len(actual_delta), alpha_mean))
    cum_contrib = {c: np.cumsum(contributions[c]) for c in regressor_cols}
    cum_residual = np.cumsum(residual)
    # sanity check: anchor_level + cum_alpha + sum(cum_contrib) + cum_residual == actual_level (exactly,
    # by construction — the residual absorbs whatever the point-estimate fit doesn't explain)

    # --- level (nominal-rate) decomposition: same log-space pieces above,
    # converted into a BRL/USD-denominated bridge from equilibrium to the
    # actual rate: equilibrium(t) + baseline + (one term per regressor) +
    # residual == ptax(t), exactly. Since the log pieces are additive but
    # the exchange rate is exp(equilibrium * deviation), the conversion is
    # inherently sequential/multiplicative (each channel's BRL/USD
    # contribution is "on top of" whatever came before it in the chosen
    # order) rather than a second independent additive split — a
    # well-known property of decomposing a multiplicative (log-additive)
    # process into level terms, not an approximation or extra source of
    # error. Order: baseline (anchor + alpha) first, then each regressor in
    # regressor_cols order, residual last (so it's always the exact plug,
    # never hides misattribution elsewhere). Looped over regressor_cols
    # (rather than named lvl_2..lvl_N variables) so this works unchanged
    # however many channels the spec has — same generalization
    # state_space_model.py's own level bridge already went through.
    equilibrium_level = compute_equilibrium(df).reindex(sample.index).values
    actual_ptax = df["ptax"].reindex(sample.index).values

    lvl_0 = equilibrium_level
    lvl_1 = lvl_0 * np.exp((anchor_level + cum_alpha) / 100)

    level_decomposition = {
        "equilibrium": [round(float(v), 4) for v in lvl_0],
        "baseline": [round(float(v), 4) for v in (lvl_1 - lvl_0)],
    }
    prev = lvl_1
    for c in regressor_cols:
        nxt = prev * np.exp(cum_contrib[c] / 100)
        level_decomposition[c] = [round(float(v), 4) for v in (nxt - prev)]
        prev = nxt
    lvl_final = prev * np.exp(cum_residual / 100)  # == actual_ptax exactly, up to floating point
    level_decomposition["residual"] = [round(float(v), 4) for v in (lvl_final - prev)]
    level_decomposition["actual"] = [round(float(v), 4) for v in actual_ptax]

    months = [d.strftime("%Y-%m") for d in sample.index]

    return {
        "n": int(len(sample)),
        "sample_range": [months[0], months[-1]],
        "months": months,
        "actual_delta": [round(float(v), 4) for v in actual_delta],
        "fitted_delta_mean": [round(float(v), 4) for v in fitted_delta_mean],
        "fitted_delta_lo": [round(float(v), 4) for v in fitted_delta_lo],
        "fitted_delta_hi": [round(float(v), 4) for v in fitted_delta_hi],
        "anchor_level": round(anchor_level, 4),
        "actual_level": [round(float(v), 4) for v in actual_level],
        "fitted_level_mean": [round(float(v), 4) for v in fitted_level_mean],
        "fitted_level_lo": [round(float(v), 4) for v in fitted_level_lo],
        "fitted_level_hi": [round(float(v), 4) for v in fitted_level_hi],
        "decomposition": {
            "alpha": [round(float(v), 4) for v in cum_alpha],
            **{c: [round(float(v), 4) for v in cum_contrib[c]] for c in regressor_cols},
            "residual": [round(float(v), 4) for v in cum_residual],
        },
        "level_decomposition": level_decomposition,
        "specs": {label: spec_summary},
        "spec_meta": {label: spec_meta},
    }


if __name__ == "__main__":
    run()
