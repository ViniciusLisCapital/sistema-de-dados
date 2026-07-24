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


def _standardize(frame: pd.DataFrame, cols: list[str]) -> tuple[pd.DataFrame, dict]:
    stats = {}
    z = frame.copy()
    for c in cols:
        mu, sd = frame[c].mean(), frame[c].std()
        z[c] = (frame[c] - mu) / sd
        stats[c] = (mu, sd)
    return z, stats


def fit_regression(frame: pd.DataFrame, regressor_cols: list[str], student_t: bool = False, label: str = "", no_intercept: bool = False, raw_cols: list[str] | None = None) -> dict:
    """Fit delta_dev ~ regressor_cols (already differenced/lagged) via PyMC.
    Regressors are standardized before fitting so a single weakly-informative
    prior works regardless of native units — EXCEPT columns named in
    raw_cols, kept in their native units.

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
    z, stats = _standardize(sample, standardize_cols)
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
# Dashboard tab: descriptive stats, historical fit, decomposition, posteriors
# ---------------------------------------------------------------------------
# Reuses the already-fit, already-saved idata (bayesian_results/*.nc) rather
# than refitting — run() must have been run at least once first.

_SPEC_FILES = {
    "primary_breakeven": ["delta_carry", "delta_tot", "delta_breakeven", "delta_fiscal"],
    "primary_gap": ["delta_carry", "delta_tot", "delta_breakeven_gap", "delta_fiscal"],
    "primary_studentt": ["delta_carry", "delta_tot", "delta_breakeven", "delta_fiscal"],
    "robustness": ["delta_carry", "delta_tot"],
}


def load_saved(label: str):
    path = _RESULTS_DIR / f"{label}_idata.nc"
    if not path.exists():
        raise FileNotFoundError(f"{path} not found — run bayesian_deviation_model.run() first.")
    return az.from_netcdf(path)


def _summary_records(idata, regressor_cols: list[str], student_t: bool) -> list[dict]:
    var_names = ["alpha"] + [f"beta_{c}" for c in regressor_cols] + (["nu"] if student_t else [])
    summary = az.summary(idata, var_names=var_names)
    records = summary.reset_index().rename(columns={"index": "param"})
    return records.round(4).to_dict("records")


def build_dashboard_payload() -> dict:
    idatas = {label: load_saved(label) for label in _SPEC_FILES}
    df = load_data()
    deltas = build_deltas(df)

    # --- descriptive stats / diagnostics per spec, incl. each spec's own n/range ---
    specs = {}
    spec_meta = {}
    for label, cols in _SPEC_FILES.items():
        specs[label] = _summary_records(idatas[label], cols, student_t=(label == "primary_studentt"))
        spec_sample = deltas[["delta_dev"] + cols].dropna()
        spec_meta[label] = {
            "n": int(len(spec_sample)),
            "sample_range": [spec_sample.index.min().strftime("%Y-%m"), spec_sample.index.max().strftime("%Y-%m")],
        }

    # --- model comparison (Normal vs. Student-t), recomputed live from saved traces ---
    cmp = az.compare({"normal": idatas["primary_breakeven"], "student_t": idatas["primary_studentt"]})
    model_comparison = cmp.reset_index().rename(columns={"index": "model"}).round(4).to_dict("records")

    # --- historical fit + decomposition (primary_breakeven spec) ---
    regressor_cols = _SPEC_FILES["primary_breakeven"]
    sample = deltas[["delta_dev"] + regressor_cols].dropna()
    z, _ = _standardize(sample, regressor_cols)

    post = idatas["primary_breakeven"].posterior
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
    # actual rate: equilibrium(t) + baseline + carry + tot + breakeven +
    # fiscal + residual == ptax(t), exactly. Since the log pieces are
    # additive but the exchange rate is exp(equilibrium * deviation), the
    # conversion is inherently sequential/multiplicative (each channel's
    # BRL/USD contribution is "on top of" whatever came before it in the
    # chosen order) rather than a second independent additive split — a
    # well-known property of decomposing a multiplicative (log-additive)
    # process into level terms, not an approximation or extra source of
    # error. Order chosen to match the log decomposition above: baseline
    # (anchor + alpha) first, then carry/tot/breakeven/fiscal, residual last
    # (so it's always the exact plug, never hides misattribution elsewhere).
    equilibrium_level = compute_equilibrium(df).reindex(sample.index).values
    actual_ptax = df["ptax"].reindex(sample.index).values

    lvl_0 = equilibrium_level
    lvl_1 = lvl_0 * np.exp((anchor_level + cum_alpha) / 100)
    lvl_2 = lvl_1 * np.exp(cum_contrib["delta_carry"] / 100)
    lvl_3 = lvl_2 * np.exp(cum_contrib["delta_tot"] / 100)
    lvl_4 = lvl_3 * np.exp(cum_contrib["delta_breakeven"] / 100)
    lvl_5 = lvl_4 * np.exp(cum_contrib["delta_fiscal"] / 100)
    lvl_6 = lvl_5 * np.exp(cum_residual / 100)  # == actual_ptax exactly, up to floating point

    level_decomposition = {
        "equilibrium": [round(float(v), 4) for v in lvl_0],
        "baseline": [round(float(v), 4) for v in (lvl_1 - lvl_0)],
        "delta_carry": [round(float(v), 4) for v in (lvl_2 - lvl_1)],
        "delta_tot": [round(float(v), 4) for v in (lvl_3 - lvl_2)],
        "delta_breakeven": [round(float(v), 4) for v in (lvl_4 - lvl_3)],
        "delta_fiscal": [round(float(v), 4) for v in (lvl_5 - lvl_4)],
        "residual": [round(float(v), 4) for v in (lvl_6 - lvl_5)],
        "actual": [round(float(v), 4) for v in actual_ptax],
    }

    months = [d.strftime("%Y-%m") for d in sample.index]

    # --- posterior distributions (primary_breakeven: alpha, betas, sigma) ---
    posteriors = {}
    for coef, draws in {"alpha": alpha_draws, **{f"beta_{c}": beta_draws[c] for c in regressor_cols},
                         "sigma": post["sigma"].values.reshape(-1)}.items():
        counts, edges = np.histogram(draws, bins=40)
        posteriors[coef] = {
            "counts": counts.tolist(),
            "edges": [round(float(e), 4) for e in edges],
            "mean": round(float(draws.mean()), 4),
        }

    # --- forest plot: coefficient comparability across specs ---
    def _forest_row(label: str, param: str):
        rec = next((r for r in specs[label] if r["param"] == param), None)
        if rec is None:
            return None
        return {"spec": label, "mean": rec["mean"], "lo": rec["hdi_3%"], "hi": rec["hdi_97%"]}

    forest = {
        "delta_carry": [r for r in (_forest_row("primary_breakeven", "beta_delta_carry"),
                                     _forest_row("robustness", "beta_delta_carry")) if r],
        "delta_tot": [r for r in (_forest_row("primary_breakeven", "beta_delta_tot"),
                                   _forest_row("robustness", "beta_delta_tot")) if r],
        "delta_breakeven": [r for r in (_forest_row("primary_breakeven", "beta_delta_breakeven"),
                                         _forest_row("primary_gap", "beta_delta_breakeven_gap")) if r],
        "delta_fiscal": [r for r in (_forest_row("primary_breakeven", "beta_delta_fiscal"),
                                      _forest_row("primary_gap", "beta_delta_fiscal")) if r],
    }

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
        "posteriors": posteriors,
        "specs": specs,
        "spec_meta": spec_meta,
        "model_comparison": model_comparison,
        "forest": forest,
    }


def render_dashboard() -> None:
    """Regenerates referencia/ppp_dashboard.html with BOTH tabs — the PPP/data
    tab (ppp_equilibrium's own payload) and the Bayesian Model tab (this
    module's payload). This is now the canonical way to generate the full
    dashboard; ppp_equilibrium.run() alone still works but leaves the
    Bayesian tab empty (falls back to `null`, see ppp_equilibrium.render())."""
    from analytics.exchange_rate.models.ppp_equilibrium import _OUTPUT, build_payload, render

    df = load_data()
    ppp_payload = build_payload(df)
    bayes_payload = build_dashboard_payload()
    render(ppp_payload, bayes_payload=bayes_payload)
    print(f"Full dashboard (both tabs) written to {_OUTPUT}")


if __name__ == "__main__":
    run()
