"""
Relative-PPP equilibrium for USD/BRL — the first real-data building block for
referencia/state_space_equilibrium_model.md's measurement equation.

    equilibrium(t) = ptax(b) * [ipca_index(t)/ipca_index(b)] / [cpi_index(t)/cpi_index(b)]

b = a user-selected base month (default 1994-07, the first month with PTAX
data under the Real). The equilibrium line is forced to equal the actual
PTAX rate at b, then scaled by cumulative BRL inflation (headline IPCA, BCB
SGS 433, % monthly variation cumulated into an index) over cumulative USD
inflation (headline CPI, FRED CPIAUCSL, index level) since b.

This is deliberately headline-vs-headline, both NSA, both monthly — the
same series pairing used everywhere else in this project (diferenciais_juros
uses ipca_12m/cpi_12m_us) rather than a bespoke tradables-only or
seasonally-adjusted construction.

Also fetches the three candidate channels for a future Bayesian model of the
PPP deviation (not fit yet — 2026-07-23 decision: examine the raw series on
the dashboard first, decide on the regression afterward):
  carry   diferenciais_juros.diferencial_nominal (Selic - Fed Funds, macro_international)
          from 1999-03 (Selic-target regime start — no earlier data exists,
          not a fetch limitation)
  tot     cmb_termos_troca.termos_de_troca_funcex (Funcex PX/PM index via
          IPEADATA, macro_brasil), real data from 1978 but trimmed to
          1994-07+ to match the rest of this dashboard
  fiscal  cmb_risco_pais.cds_5y_usd (Brazil 5Y CDS in USD, manually
          ingested from investing.com exports, macro_brasil) from 2007-12
  breakeven  10y bond-implied inflation expectation, PREJS - NTNBJS @ 120M
          tenor, from base_mercado.interest_rates — an EXTERNAL schema (fund
          ops, not this project's own ETL, read live via MySQLDataRequester
          same as carry_model.py already does for its BR-2y carry spec).
          From 2006-01. Long-term-expectation proxy added 2026-07-23 at the
          user's request, after confirming BCB Focus's own longest horizon
          (IPCA 24m, macro_brasil.expc_focus) only goes back to 2021-03 —
          too short to be useful here.
          Data-quality fix carried over from referencia/state_space_equilibrium_model.md's
          "built and charted this session as a working proxy" note: PREJS@120M
          has two confirmed bad windows (2010-01-22..2010-02-05 and
          2010-03-02..2010-03-04, values ~3% vs. a true ~13%, isolated to this
          one curve/tenor — verified 60M and NTNBJS@120M are clean over the
          same period) — masked and linearly interpolated in _load_breakeven()
          below. This is now the real, documented fix the concept note asked
          for ("fix the bug in production for now"), not the prior throwaway
          plotting script — though note the fix still lives in this project's
          code, not in the external base_mercado table itself, since that
          table isn't ours to write to.
All four are left-joined onto the core (ptax/ipca/cpi) monthly index, so
each column is simply null before its own series starts — no padding or
back-filling.

Not wired into generate_report.py — renders a standalone, self-contained
dashboard (models/ppp_dashboard_template.html -> referencia/ppp_dashboard.html)
with a client-side base-month selector, following the same /*MARKER*/ +
str.replace() templating convention as generate_report.py.

Usage:
    uv run python -c "from analytics.exchange_rate.models.ppp_equilibrium import run; run()"
"""

import json
from decimal import Decimal
from pathlib import Path

import numpy as np
import pandas as pd

from connectors.fred import FredUniFrame
from connectors.mysql import MySQLDataRequester

_TEMPLATE = Path(__file__).parent / "ppp_dashboard_template.html"
_OUTPUT = Path(__file__).parent.parent / "referencia" / "ppp_dashboard.html"

_DEFAULT_BASE_MONTH = "1994-07"
_FETCH_START = "1994-01-01"  # a few months of headroom before the first PTAX print (1994-07-01)


def _read_table(database: str, table: str) -> pd.DataFrame:
    req = MySQLDataRequester(database, table)
    req.connect()
    df = req.request_data()
    req.close_connection()
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, Decimal)).any():
            df[col] = df[col].astype(float)
    return df


def _monthly_series(database: str, table: str, name: str, rename_to: str) -> pd.Series:
    df = _read_table(database, table)
    df = df[df["name"] == name]
    s = df.set_index(pd.to_datetime(df["date"]))["value"].sort_index()
    return s.resample("MS").last().rename(rename_to)


# Confirmed bad windows in PREJS@120M (base_mercado.interest_rates, external
# schema) — see load_data()'s docstring. Isolated to this one curve/tenor.
_PREJS_120M_BUG_WINDOWS = [
    ("2010-01-22", "2010-02-05"),
    ("2010-03-02", "2010-03-04"),
]


def _load_breakeven() -> pd.Series:
    """10y bond-implied breakeven inflation (PREJS - NTNBJS @ 120M), monthly,
    with the confirmed PREJS@120M bug windows masked and linearly interpolated."""
    curves = _read_table("base_mercado", "interest_rates")
    curves["date"] = pd.to_datetime(curves["date"])
    curves["value"] = curves["value"].astype(float)

    prejs = curves[(curves["curve"] == "PREJS") & (curves["tenor"] == "120M")].set_index("date")["value"].sort_index()
    ntnbjs = curves[(curves["curve"] == "NTNBJS") & (curves["tenor"] == "120M")].set_index("date")["value"].sort_index()

    for start, end in _PREJS_120M_BUG_WINDOWS:
        prejs.loc[start:end] = pd.NA
    prejs = prejs.astype(float).interpolate(method="time")

    breakeven = (prejs - ntnbjs).dropna()
    return breakeven.resample("MS").last().rename("breakeven")


def _load_inflation_target() -> pd.Series:
    """CMN inflation target (macro_brasil.inflc_meta, BCB SGS 13521) — one
    value per calendar year, dated Jan-1 of the target year. Returned as-is
    (annual); load_data() forward-fills it across each year's months after
    joining onto the monthly index."""
    target = _read_table("macro_brasil", "inflc_meta")
    target = target[target["name"] == "meta_inflacao"]
    return target.set_index(pd.to_datetime(target["date"]))["value"].sort_index().rename("target")


def load_data() -> pd.DataFrame:
    """Monthly frame (month-start index): ptax, ipca_index, cpi_index, plus the
    three raw candidate channels (carry, tot, fiscal) left-joined on — null
    wherever that channel's own data hasn't started yet."""
    ptax = _read_table("macro_brasil", "cmb_ptax")
    ptax = ptax[ptax["name"] == "ptax_venda"]
    ptax_s = ptax.set_index(pd.to_datetime(ptax["date"]))["value"].sort_index()
    ptax_m = ptax_s.resample("MS").last().rename("ptax")

    ipca = _read_table("macro_brasil", "inflc_agregados")
    ipca = ipca[ipca["name"] == "ipca"]
    ipca_s = ipca.set_index(pd.to_datetime(ipca["date"]))["value"].sort_index()
    ipca_s = ipca_s[ipca_s.index >= _FETCH_START]
    ipca_index = ((ipca_s / 100 + 1).cumprod() * 100).rename("ipca_index")

    cpi = FredUniFrame("cpi_us", "CPIAUCSL", _FETCH_START, None)
    cpi_s = cpi.set_index(pd.to_datetime(cpi["Date"]))["cpi_us"].sort_index()
    cpi_m = cpi_s.resample("MS").last().rename("cpi_index")

    core = pd.concat([ptax_m, ipca_index, cpi_m], axis=1).dropna()

    carry_m = _monthly_series("macro_international", "diferenciais_juros", "diferencial_nominal", "carry")
    tot_m = _monthly_series("macro_brasil", "cmb_termos_troca", "termos_de_troca_funcex", "tot")
    fiscal_m = _monthly_series("macro_brasil", "cmb_risco_pais", "cds_5y_usd", "fiscal")
    breakeven_m = _load_breakeven()
    target_annual = _load_inflation_target()

    df = core.join([carry_m, tot_m, fiscal_m, breakeven_m, target_annual], how="left")
    df["target"] = df["target"].ffill()
    df["breakeven_gap"] = df["breakeven"] - df["target"]
    return df


def compute_equilibrium(df: pd.DataFrame, base_month: str = _DEFAULT_BASE_MONTH) -> pd.Series:
    """equilibrium(t) = ptax(b) * [ipca_index(t)/ipca_index(b)] / [cpi_index(t)/cpi_index(b)].

    Same base-month invariance note as compute_deviation() below: this level
    itself DOES shift with the base month (it's anchored to ptax(b)), but the
    log-deviation built from it doesn't."""
    base_idx = df.index[df.index.strftime("%Y-%m") == base_month][0]
    base = df.loc[base_idx]
    eq = base["ptax"] * (df["ipca_index"] / base["ipca_index"]) / (df["cpi_index"] / base["cpi_index"])
    return eq.rename("equilibrium")


def compute_deviation(df: pd.DataFrame, base_month: str = _DEFAULT_BASE_MONTH) -> pd.Series:
    """D(t) = 100 * ln(ptax(t) / equilibrium(t; b)).

    Base-month choice only shifts the whole series by a constant — see
    bayesian_deviation_model.md's derivation — so any month present in df
    works here; it doesn't change the series' shape or dynamics."""
    eq = compute_equilibrium(df, base_month)
    return (100 * np.log(df["ptax"] / eq)).rename("deviation")


def _to_jsonable(series: pd.Series) -> list:
    return [None if pd.isna(v) else round(float(v), 6) for v in series]


def build_payload(df: pd.DataFrame, default_base_month: str = _DEFAULT_BASE_MONTH) -> dict:
    return {
        "months": [d.strftime("%Y-%m") for d in df.index],
        "ptax": _to_jsonable(df["ptax"]),
        "br_index": _to_jsonable(df["ipca_index"]),
        "us_index": _to_jsonable(df["cpi_index"]),
        "carry": _to_jsonable(df["carry"]),
        "tot": _to_jsonable(df["tot"]),
        "fiscal": _to_jsonable(df["fiscal"]),
        "breakeven": _to_jsonable(df["breakeven"]),
        "default_base_month": default_base_month,
    }


def render(payload: dict, bayes_payload: dict | None = None) -> None:
    """Fills both template markers. `/*PPP_DATA*/` always gets `payload`;
    `/*BAYES_DATA*/` gets `bayes_payload` if given, else the literal `null`
    (so the template's Bayesian-model tab always has valid JS to check
    against, whether or not that tab's data was generated this run)."""
    template = _TEMPLATE.read_text(encoding="utf-8")
    html = template.replace("/*PPP_DATA*/", json.dumps(payload))
    html = html.replace("/*BAYES_DATA*/", json.dumps(bayes_payload) if bayes_payload is not None else "null")
    _OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    _OUTPUT.write_text(html, encoding="utf-8")


def run() -> dict:
    df = load_data()
    payload = build_payload(df)
    render(payload)

    deviation = compute_deviation(df)
    print(f"Sample: {df.index.min().date()} .. {df.index.max().date()}  (n={len(df)})")
    print(f"Base month ({_DEFAULT_BASE_MONTH}): PTAX={df.loc[df.index.strftime('%Y-%m') == _DEFAULT_BASE_MONTH, 'ptax'].iloc[0]:.4f}")
    print(f"Latest ({df.index[-1].strftime('%Y-%m')}): actual PTAX={df['ptax'].iloc[-1]:.4f}, deviation={deviation.iloc[-1]:+.1f}%")
    for col in ("carry", "tot", "fiscal", "breakeven", "target", "breakeven_gap"):
        s = df[col].dropna()
        print(f"  {col}: {s.index.min().date()} .. {s.index.max().date()}  (n={len(s)})")
    print(f"Dashboard written to {_OUTPUT}")

    return {"data": df, "payload": payload}


if __name__ == "__main__":
    run()
