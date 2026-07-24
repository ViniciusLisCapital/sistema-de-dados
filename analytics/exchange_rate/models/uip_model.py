"""
Uncovered Interest Parity (UIP) for USD/BRL — OLS, GARCH(1,1), and 2-regime
Markov-switching versions of the CIP-proxied forward-premium regression.

Background: referencia/fx_forecasting_theory_vs_practice.md Part I S2, and
referencia/er_forecasting/ (Fama, 1984; Araujo et al., SciELO).

No forward FX rate exists in the DB, so — the same substitution the BRL
literature itself uses — the Selic-Fed Funds differential stands in for the
forward premium via covered interest parity (f - s ~= i - i*):

    ds(t) = alpha + beta * diff_monthly(t-1) + eps(t)

ds(t)          = monthly log return of PTAX (in %), positive = BRL depreciation
diff_monthly   = diferencial_nominal (Selic - Fed Funds, % a.a.) / 12, so the
                 regressor is on the same monthly horizon as ds — required for
                 UIP's null beta=1 to mean anything ("1pp more annualized carry
                 -> 1pp more expected monthly depreciation" would otherwise
                 compare an annualized rate to a monthly return).
                 Lagged one month so the differential is known before the
                 return period it's meant to explain (avoids look-ahead and
                 same-period simultaneity).

Under UIP: beta = 1. Fama (1984) found beta reliably negative; Araujo et al.
replicate this for BRL (2000-2014, GARCH beta = -2.94) and find regime
dependence via Markov-switching (-2.94 in low-vol months, >+1.00 in high-vol
months) - the sign-flip this script's Markov-switching fit is checked against.

Sample starts 1999-01 (post free-float; the pre-1999 crawling-peg/band regime
used a different exchange-rate mechanism than UIP describes).
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from arch import arch_model
from statsmodels.tsa.regime_switching.markov_regression import MarkovRegression

from connectors.mysql import MySQLDataRequester

_SAMPLE_START = "1999-01-01"
_REPORT_DIR = Path(__file__).resolve().parents[3] / "reports" / "fx_models"


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

def _read_table(database: str, table: str) -> pd.DataFrame:
    req = MySQLDataRequester(database, table)
    req.connect()
    df = req.request_data()
    req.close_connection()
    # mysql.connector returns DECIMAL columns as decimal.Decimal — normalize to
    # float so they mix freely with plain python floats downstream.
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, Decimal)).any():
            df[col] = df[col].astype(float)
    return df


def load_data(sample_start: str = _SAMPLE_START) -> pd.DataFrame:
    """Monthly frame: ptax, ds (% log return), diff (% a.a.), diff_lag1_m (monthly-equivalent, lagged)."""
    ptax = _read_table("macro_brasil", "cmb_ptax")
    ptax = ptax[ptax["name"] == "ptax_venda"]
    ptax_s = ptax.set_index(pd.to_datetime(ptax["date"]))["value"].sort_index()
    ptax_m = ptax_s.resample("MS").last()

    dj = _read_table("macro_international", "diferenciais_juros")
    diff = dj[dj["name"] == "diferencial_nominal"]
    diff_s = diff.set_index(pd.to_datetime(diff["date"]))["value"].sort_index()
    diff_m = diff_s.resample("MS").last()

    df = pd.DataFrame({"ptax": ptax_m, "diff": diff_m}).dropna()
    df["ds"] = np.log(df["ptax"]).diff() * 100  # monthly log return, in %
    df["diff_monthly"] = df["diff"] / 12  # annualized -> monthly-equivalent
    df["diff_lag1_m"] = df["diff_monthly"].shift(1)
    df = df.dropna(subset=["ds", "diff_lag1_m"])
    return df[df.index >= sample_start]


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def fit_ols(df: pd.DataFrame):
    X = sm.add_constant(df["diff_lag1_m"])
    return sm.OLS(df["ds"], X).fit(cov_type="HAC", cov_kwds={"maxlags": 3})


def fit_garch(df: pd.DataFrame):
    """GARCH(1,1) errors on the same mean equation (pure regression mean, no AR term)."""
    am = arch_model(df["ds"], x=df[["diff_lag1_m"]], mean="LS", vol="GARCH", p=1, q=1, dist="normal")
    return am.fit(disp="off")


def fit_markov_switching(df: pd.DataFrame):
    mod = MarkovRegression(
        df["ds"], k_regimes=2, exog=df[["diff_lag1_m"]],
        trend="c", switching_exog=True, switching_variance=True,
    )
    return mod.fit()


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def summarize(ols_res, garch_res, ms_res) -> pd.DataFrame:
    garch_beta = garch_res.params.get("diff_lag1_m", np.nan)
    garch_pvalue = garch_res.pvalues.get("diff_lag1_m", np.nan)

    # MarkovRegression doesn't keep the exog column name from a DataFrame — it
    # labels the (only) exog regressor "x1[<regime>]" and the variance "sigma2[<regime>]".
    ms_betas = {i: ms_res.params.get(f"x1[{i}]", np.nan) for i in range(ms_res.model.k_regimes)}
    ms_pvalues = {i: ms_res.pvalues.get(f"x1[{i}]", np.nan) for i in range(ms_res.model.k_regimes)}
    ms_sigma2 = {i: ms_res.params.get(f"sigma2[{i}]", np.nan) for i in range(ms_res.model.k_regimes)}
    low_vol_regime = min(ms_sigma2, key=ms_sigma2.get)
    high_vol_regime = max(ms_sigma2, key=ms_sigma2.get)

    rows = [
        {"model": "OLS", "beta": ols_res.params["diff_lag1_m"], "pvalue": ols_res.pvalues["diff_lag1_m"], "note": f"R2={ols_res.rsquared:.3f}"},
        {"model": "GARCH(1,1)", "beta": garch_beta, "pvalue": garch_pvalue, "note": "mean eq. beta, GARCH errors"},
        {"model": "Markov low-vol", "beta": ms_betas[low_vol_regime], "pvalue": ms_pvalues[low_vol_regime], "note": f"sigma2={ms_sigma2[low_vol_regime]:.3f}"},
        {"model": "Markov high-vol", "beta": ms_betas[high_vol_regime], "pvalue": ms_pvalues[high_vol_regime], "note": f"sigma2={ms_sigma2[high_vol_regime]:.3f}"},
    ]
    return pd.DataFrame(rows)


def plot_diagnostics(df: pd.DataFrame, ms_res, out_path: Path) -> None:
    high_vol_regime = int(np.argmax(ms_res.params[[f"sigma2[{i}]" for i in range(ms_res.model.k_regimes)]].values))
    high_vol_prob = ms_res.smoothed_marginal_probabilities[high_vol_regime]

    fig, axes = plt.subplots(3, 1, figsize=(11, 9), sharex=True)

    axes[0].plot(df.index, df["ds"], color="#1F2853", linewidth=1)
    axes[0].axhline(0, color="grey", linewidth=0.5)
    axes[0].set_title("USD/BRL monthly log return (%)")

    axes[1].plot(df.index, df["diff_lag1_m"], color="#BB9B1D", linewidth=1)
    axes[1].axhline(0, color="grey", linewidth=0.5)
    axes[1].set_title("Interest differential, monthly-equivalent, lagged 1m (Selic - Fed Funds)/12")

    axes[2].fill_between(df.index, high_vol_prob, color="#418791", alpha=0.6)
    axes[2].set_ylim(0, 1)
    axes[2].set_title("Smoothed probability of high-volatility regime (Markov-switching)")

    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run(sample_start: str = _SAMPLE_START) -> dict:
    df = load_data(sample_start)
    ols_res = fit_ols(df)
    garch_res = fit_garch(df)
    ms_res = fit_markov_switching(df)

    plot_diagnostics(df, ms_res, _REPORT_DIR / "uip_diagnostics.png")
    summary = summarize(ols_res, garch_res, ms_res)

    print(f"Sample: {df.index.min().date()} .. {df.index.max().date()}  (n={len(df)})\n")
    print(summary.to_string(index=False))
    print(f"\nDiagnostic plot saved to {_REPORT_DIR / 'uip_diagnostics.png'}")

    return {"data": df, "ols": ols_res, "garch": garch_res, "markov": ms_res, "summary": summary}


if __name__ == "__main__":
    run()
