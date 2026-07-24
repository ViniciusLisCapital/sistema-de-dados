"""
Carry model -- USD/BRL, comparing interest-rate differential specifications.

Tests whether interest-rate differentials explain monthly USD/BRL depreciation
across two dimensions:
  horizon:      short-term policy rate (Selic - Fed Funds)   vs.  2-year point (BR 2y - US 2y)
  construction: nominal                                      vs.  real, ex-post (nominal minus
                                                                    trailing-12m realized inflation)

Four specifications in total: a_nominal, a_real, b_nominal, b_real.

Different question from uip_model.py: that script tests the specific UIP
restriction (beta=1) on the short-rate nominal spec alone, for the valuation
branch of this project. This script asks a broader, less restrictive question
-- across four constructions of "the interest differential", which one (if
any) helps explain FX moves at all -- as part of a separate predictor-testing
research track (see chat 2026-07-22).

Data and known sample-window constraint
----------------------------------------
a) Selic - Fed Funds (nominal and real ex-post): macro_international.diferenciais_juros,
   available 1999-03 -> today.
b) BR 2y - US 2y (nominal and real ex-post): BR leg from base_mercado.interest_rates
   (curve='PREJS', tenor='24M') -- an external LIS fund-ops schema, NOT part of this
   project's own ETL, read here directly rather than re-sourced. US leg fetched fresh
   from FRED (DGS2) rather than base_mercado's own US_TREASURY curve, since that one
   is truncated to 2016 -- DGS2 covers the same window as the BR leg with no gap.

   The BR 2y leg only starts 2006-01: verified directly against the Tesouro Direto
   historical bond file (connectors/not_in_production/tesouro.py) that the longest
   prefixado bond traded in 2004-2005 was under 1.6 years -- a 2-year point that far
   back would be extrapolated past any real bond, not interpolated between two.
   2006-01 is the real first date this instrument existed in observable form, not an
   artifact of when any particular feed started being pulled.

Both real legs use ex-post construction (nominal minus trailing-12m realized
inflation) rather than a market-priced real yield (e.g. NTNBJS for the BR 2y real
leg) -- deliberate, since NTNBJS's own 2-year point would itself be a modeled
extrapolation before short-dated NTN-B existed (no NTN-B under 9 years was trading
as late as Jan 2006), which would make the real leg less reliable than its nominal
counterpart. Ex-post construction only depends on the (verified reliable) nominal
yields plus realized inflation, so it inherits the nominal leg's own reliability
instead of adding a second, worse one.

All four differentials are divided by 12 (annualized % a.a. -> monthly-equivalent)
and lagged one month before being paired with ds, mirroring uip_model.py's own
justification: puts every regressor on the same horizon as the monthly return it's
meant to explain, and ensures it's known before the return period it explains.

Methodology: OLS with HAC standard errors (maxlags=3) only, for all four specs --
matches uip_model.py's baseline estimator. GARCH/Markov-switching deliberately left
for a later pass once this first comparison shows which spec(s) are worth the extra
estimation depth.

Two summary tables are produced: each spec fit on its own maximal available window
(1999-03 for a, 2006-01 for b), and a second comparison with all four restricted to
the common 2006-01 -> today window, so betas are directly comparable without a
different-sample-period confound.
"""

from __future__ import annotations

import os
from decimal import Decimal
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from dotenv import load_dotenv
from fredapi import Fred

from connectors.mysql import MySQLDataRequester

load_dotenv()

_SAMPLE_START_A      = "1999-01-01"   # diferenciais_juros (BR side) availability
_SAMPLE_START_B      = "2006-01-01"   # PREJS 2y availability -- see module docstring
_SAMPLE_START_US_2Y  = "1995-01-01"   # fed_funds availability -- gl_mc needs the US leg this far back,
                                       # independent of the BR-2y (PREJS) constraint on specs (b)
_COMMON_START        = "2006-01-01"
_REPORT_DIR = Path(__file__).resolve().parents[3] / "reports" / "fx_models"

_SPECS = {
    "a_nominal": "diff_a_nom_lag1",
    "a_real":    "diff_a_real_lag1",
    "b_nominal": "diff_b_nom_lag1",
    "b_real":    "diff_b_real_lag1",
}

# "Dynamic" spec (2026-07-22): what if it's not the differential's *level* that
# matters, but its *change* -- plus where the US itself sits in its own hiking/
# cutting cycle? Two regressors together:
#   diff_a_nom_chg_lag1 -- month-over-month CHANGE in Selic-Fed Funds (pp), not
#                          divided by 12: the /12 transform on the other specs
#                          converts an annualized LEVEL into a monthly-equivalent
#                          expected return (the UIP mechanics uip_model.py and
#                          this file's other 4 specs rely on); a month-over-month
#                          CHANGE is already a monthly-frequency quantity in its
#                          own right, so that rationale doesn't carry over here.
#   gl_mc_lag1          -- US 2y - Fed Funds ("global monetary cycle"): the US
#                          front-end curve slope. Positive/steepening when the
#                          market expects the Fed to hike (early-cycle), negative/
#                          inverted when it expects cuts (late-cycle/recession
#                          risk) -- independent of the BR-US level gap itself,
#                          this is a pure US-side proxy for the global dollar/
#                          risk cycle, which EM FX literature often finds matters
#                          as much as the simple differential.
_DYNAMIC_SPEC = ["diff_a_nom_chg_lag1", "gl_mc_lag1"]

# LIS Capital brand palette (see project_lis_brand_colors memory / other reports' CSS vars).
_COLOR_NOM     = "#1F2853"  # azul -- nominal series
_COLOR_REAL    = "#BB9B1D"  # dourado -- real series / OLS fit line
_COLOR_PTAX    = "#418791"  # verde -- PTAX level, primary data
_COLOR_SCATTER = "#1F2853"  # azul -- scatter points
_COLOR_GRID    = "#BFBFBF"  # cinza -- gridlines/zero lines
_COLOR_DEPREC  = "#EA523A"  # laranja -- ds > 0 (BRL depreciation)
_COLOR_APREC   = "#418791"  # verde -- ds <= 0 (BRL appreciation)


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

def _read_table(database: str, table: str) -> pd.DataFrame:
    req = MySQLDataRequester(database, table)
    req.connect()
    df = req.request_data()
    req.close_connection()
    # mysql.connector returns DECIMAL columns as decimal.Decimal -- normalize to
    # float so they mix freely with plain python floats downstream.
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, Decimal)).any():
            df[col] = df[col].astype(float)
    return df


def _fetch_us_2y(start_iso: str) -> pd.Series:
    """US 2y Treasury nominal yield, FRED DGS2, resampled to month-start (last obs)."""
    fred = Fred(api_key=os.environ.get("FRED_API_KEY", ""))
    raw = fred.get_series("DGS2", observation_start=start_iso)
    return raw.resample("MS").last().rename("us_2y")


def load_data() -> pd.DataFrame:
    """Monthly frame with ptax, ds, and the four lagged monthly-equivalent differentials."""
    # --- ds: PTAX monthly log return (same construction as uip_model.py) ---
    ptax = _read_table("macro_brasil", "cmb_ptax")
    ptax = ptax[ptax["name"] == "ptax_venda"]
    ptax_s = ptax.set_index(pd.to_datetime(ptax["date"]))["value"].sort_index()
    ptax_m = ptax_s.resample("MS").last().rename("ptax")

    # --- (a) short-term: diferenciais_juros already stores monthly nominal/real/raw-inflation series ---
    dj = _read_table("macro_international", "diferenciais_juros")
    dj_wide = dj.pivot_table(index="date", columns="name", values="value")
    dj_wide.index = pd.to_datetime(dj_wide.index)
    dj_m = dj_wide.resample("MS").last()

    # --- (b) 2y: BR leg from base_mercado (external, cross-schema -- see module docstring),
    #     US leg from FRED ---
    ir = _read_table("base_mercado", "interest_rates")
    prejs = ir[(ir["curve"] == "PREJS") & (ir["tenor"] == "24M")]
    prejs_s = prejs.set_index(pd.to_datetime(prejs["date"]))["value"].sort_index()
    prejs_m = prejs_s.resample("MS").last().rename("prejs_24m")

    us_2y_m = _fetch_us_2y(_SAMPLE_START_US_2Y)

    # --- Combine ---
    df = pd.concat([ptax_m, dj_m, prejs_m, us_2y_m], axis=1)
    df.index.name = "date"

    df["ds"] = np.log(df["ptax"]).diff() * 100

    df["diff_a_nom"]  = df["diferencial_nominal"]
    df["diff_a_real"] = df["diferencial_real"]
    df["diff_b_nom"]  = df["prejs_24m"] - df["us_2y"]
    df["diff_b_real"] = (df["prejs_24m"] - df["ipca_12m"]) - (df["us_2y"] - df["cpi_12m_us"])

    for col in ["diff_a_nom", "diff_a_real", "diff_b_nom", "diff_b_real"]:
        df[f"{col}_lag1"] = (df[col] / 12).shift(1)

    # --- "Dynamic" spec inputs -- see _DYNAMIC_SPEC comment above ---
    df["gl_mc"] = df["us_2y"] - df["fed_funds"]
    df["gl_mc_lag1"] = (df["gl_mc"] / 12).shift(1)

    df["diff_a_nom_chg"] = df["diff_a_nom"].diff()
    df["diff_a_nom_chg_lag1"] = df["diff_a_nom_chg"].shift(1)

    return df


# ---------------------------------------------------------------------------
# Estimation
# ---------------------------------------------------------------------------

def _fit_spec(df: pd.DataFrame, col: str) -> dict:
    sub = df[["ds", col]].dropna()
    X = sm.add_constant(sub[col])
    res = sm.OLS(sub["ds"], X).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
    return {
        "spec":   col.replace("_lag1", ""),
        "beta":   res.params[col],
        "pvalue": res.pvalues[col],
        "r2":     res.rsquared,
        "n":      int(res.nobs),
        "start":  sub.index.min().date(),
        "end":    sub.index.max().date(),
    }


def _fit_multi(df: pd.DataFrame, cols: list[str], label: str) -> dict:
    """Same OLS+HAC estimator as _fit_spec, generalized to >1 regressor."""
    sub = df[["ds", *cols]].dropna()
    X = sm.add_constant(sub[cols])
    res = sm.OLS(sub["ds"], X).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
    out = {
        "spec":  label,
        "r2":    res.rsquared,
        "n":     int(res.nobs),
        "start": sub.index.min().date(),
        "end":   sub.index.max().date(),
        "corr_between_regressors": sub[cols].corr().iloc[0, 1],
    }
    for c in cols:
        out[f"beta[{c}]"]   = res.params[c]
        out[f"pvalue[{c}]"] = res.pvalues[c]
    return out


def summarize(df: pd.DataFrame, common_start: str = _COMMON_START) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Returns (own_window, common_window) summary tables, one row per spec."""
    own_window = pd.DataFrame([_fit_spec(df, _SPECS[k]) for k in _SPECS])

    common_df = df[df.index >= common_start]
    common_window = pd.DataFrame([_fit_spec(common_df, _SPECS[k]) for k in _SPECS])

    return own_window, common_window


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------

def plot_levels(df: pd.DataFrame, out_path: Path) -> None:
    """Differential level(s) vs. PTAX level, stacked as small multiples.

    Never a dual-axis chart (% differential and R$/USD PTAX are different
    scales) -- each is its own panel, sharing only the x-axis (time), one
    column per horizon (short-term vs. 2y), each column sliced to its own
    valid window.
    """
    a_df = df[df.index >= _SAMPLE_START_A]
    b_df = df[df.index >= _SAMPLE_START_B]

    fig, axes = plt.subplots(2, 2, figsize=(13, 7), sharex="col")

    ax = axes[0, 0]
    ax.plot(a_df.index, a_df["diff_a_nom"], color=_COLOR_NOM, linewidth=1.3, label="Nominal (Selic - Fed Funds)")
    ax.plot(a_df.index, a_df["diff_a_real"], color=_COLOR_REAL, linewidth=1.3, label="Real ex-post")
    ax.axhline(0, color=_COLOR_GRID, linewidth=0.8)
    ax.set_title("Short-term differential (% a.a.)")
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    ax.grid(color=_COLOR_GRID, alpha=0.3, linewidth=0.5)

    ax = axes[1, 0]
    ax.plot(a_df.index, a_df["ptax"], color=_COLOR_PTAX, linewidth=1.3)
    ax.set_title("USD/BRL PTAX (R$)")
    ax.grid(color=_COLOR_GRID, alpha=0.3, linewidth=0.5)

    ax = axes[0, 1]
    ax.plot(b_df.index, b_df["diff_b_nom"], color=_COLOR_NOM, linewidth=1.3, label="Nominal (BR 2y - US 2y)")
    ax.plot(b_df.index, b_df["diff_b_real"], color=_COLOR_REAL, linewidth=1.3, label="Real ex-post")
    ax.axhline(0, color=_COLOR_GRID, linewidth=0.8)
    ax.set_title("2-year differential (% a.a.)")
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    ax.grid(color=_COLOR_GRID, alpha=0.3, linewidth=0.5)

    ax = axes[1, 1]
    ax.plot(b_df.index, b_df["ptax"], color=_COLOR_PTAX, linewidth=1.3)
    ax.set_title("USD/BRL PTAX (R$) -- 2006 onward")
    ax.grid(color=_COLOR_GRID, alpha=0.3, linewidth=0.5)

    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_ds(df: pd.DataFrame, out_path: Path) -> None:
    """The dependent variable on its own: ds, monthly log return of PTAX (%).

    Bars rather than a line -- ds is inherently a polarity quantity (positive =
    depreciation, negative = appreciation), so diverging color by sign carries
    that meaning directly instead of leaving it to a reader to infer from a
    single-color line crossing zero.
    """
    sub = df["ds"].dropna()
    colors = np.where(sub >= 0, _COLOR_DEPREC, _COLOR_APREC)

    fig, ax = plt.subplots(figsize=(14, 4.5))
    ax.bar(sub.index, sub.values, color=colors, width=20)
    ax.axhline(0, color=_COLOR_GRID, linewidth=0.8)
    ax.grid(color=_COLOR_GRID, alpha=0.3, linewidth=0.5)
    ax.set_title("USD/BRL PTAX -- monthly log return, ds (%)")
    ax.set_ylabel("ds, m/m (%)")

    from matplotlib.patches import Patch
    ax.legend(
        handles=[Patch(color=_COLOR_DEPREC, label="Depreciation (ds > 0)"),
                 Patch(color=_COLOR_APREC, label="Appreciation (ds <= 0)")],
        frameon=False, fontsize=8, loc="upper left",
    )

    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_scatter(df: pd.DataFrame, out_path: Path) -> None:
    """2x2 grid: ds (m/m %, y) vs. each lagged monthly-equivalent differential (x), OLS fit overlaid."""
    panels = [
        ("a_nominal", "diff_a_nom_lag1",  "Short-term, nominal"),
        ("a_real",    "diff_a_real_lag1", "Short-term, real"),
        ("b_nominal", "diff_b_nom_lag1",  "2-year, nominal"),
        ("b_real",    "diff_b_real_lag1", "2-year, real"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(11, 9))
    for ax, (spec, col, title) in zip(axes.flat, panels):
        sub = df[["ds", col]].dropna()
        fit = _fit_spec(df, col)

        ax.scatter(sub[col], sub["ds"], s=22, color=_COLOR_SCATTER, alpha=0.45, edgecolors="none",
                   label="Monthly observation")

        X = sm.add_constant(sub[col])
        plain_ols = sm.OLS(sub["ds"], X).fit()
        x_line = np.linspace(sub[col].min(), sub[col].max(), 50)
        y_line = plain_ols.params["const"] + plain_ols.params[col] * x_line
        ax.plot(x_line, y_line, color=_COLOR_REAL, linewidth=2, label="OLS fit")

        ax.axhline(0, color=_COLOR_GRID, linewidth=0.6)
        ax.axvline(0, color=_COLOR_GRID, linewidth=0.6)
        ax.grid(color=_COLOR_GRID, alpha=0.3, linewidth=0.5)
        ax.set_title(f"{title}  (β={fit['beta']:.2f}, p={fit['pvalue']:.2f}, R²={fit['r2']:.3f})", fontsize=10)
        ax.set_xlabel("Lagged differential, monthly-equiv. (%)", fontsize=8)
        ax.set_ylabel("ds, m/m (%)", fontsize=8)

    axes.flat[0].legend(frameon=False, fontsize=8, loc="upper right")
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run() -> dict:
    df = load_data()
    own_window, common_window = summarize(df)
    dynamic = _fit_multi(df, _DYNAMIC_SPEC, "dynamic (chg_diff_a_nom + gl_mc)")

    print(f"Own-window (each spec on its own maximal available sample):\n")
    print(own_window.to_string(index=False))
    print(f"\nCommon-window (all specs restricted to {_COMMON_START} -> today):\n")
    print(common_window.to_string(index=False))

    print(f"\nDynamic spec -- {dynamic['spec']}:")
    print(f"  window: {dynamic['start']} -> {dynamic['end']}  (n={dynamic['n']})")
    print(f"  R2: {dynamic['r2']:.4f}")
    print(f"  corr(diff_a_nom_chg_lag1, gl_mc_lag1): {dynamic['corr_between_regressors']:.3f}")
    for c in _DYNAMIC_SPEC:
        print(f"  {c}: beta={dynamic[f'beta[{c}]']:.4f}  pvalue={dynamic[f'pvalue[{c}]']:.4f}")

    plot_ds(df, _REPORT_DIR / "carry_ds.png")
    plot_levels(df, _REPORT_DIR / "carry_levels.png")
    plot_scatter(df, _REPORT_DIR / "carry_scatter.png")
    print(f"\nPlots saved to {_REPORT_DIR}")

    return {"data": df, "own_window": own_window, "common_window": common_window, "dynamic": dynamic}


if __name__ == "__main__":
    run()
