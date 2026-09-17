"""Monthly panel for the pure-forecast lab, built so that every column at row
``m`` is something you could actually have read on the last business day of
month ``m``.

That property is the whole point of this module, and it is what separates this
lab from `analytics/brasil/exchange_rate/models/ridge_deviation_model.py` and
from the conditional horse race in `models/ridge_vs_random_walk.md`. That test
handed the model the *realized* future path of its channels; here nothing dated
after the forecast origin is allowed into the feature matrix, and a series that
is published with a lag is shifted by that lag before it ever reaches a
regression.

Two mechanisms, applied per series:

- **Daily sources** (PTAX, CDS, DXY, S&P, Brent, LatAm FX, contracted FX flow)
  are collapsed to monthly with an as-of rule: the value for month ``m`` is the
  last observation on or before ``month_end(m) - pub_delay_days``. For a market
  quote that delay is 0-1 days; for BCB's contracted-FX series, which posts on
  a ~2-business-day delay, it is 4 calendar days. Nothing is "the month's last
  print" unless that print was really on the tape by month end.
- **Monthly sources** (IPCA, US CPI, BIS REER, terms of trade, ICBr) carry an
  ``avail_lag`` in months and are shifted by it. Row ``m`` of ``ipca_index``
  therefore holds the index for month ``m - 1``, which is what you knew on the
  last day of ``m``: IBGE publishes IPCA for month ``m`` around the 10th of
  ``m + 1``.

The column names keep their natural meaning (``cds``, ``ipca_index``) — the
shift is already baked in, so downstream code never has to remember a lag. The
per-series lag actually applied is recorded in ``AVAILABILITY`` and written to
the cache header, so a future reader can audit it without re-deriving it.

Nothing here imports the shipped model. The lab reads the same tables and
rebuilds what it needs, deliberately, so an experiment can change a definition
without touching production.
"""

from __future__ import annotations

import json
import os
from decimal import Decimal

import numpy as np
import pandas as pd

from connectors.fred import FredUniFrame
from connectors.mysql import MySQLDataRequester

_HERE = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(_HERE, "cache")
PANEL_CSV = os.path.join(CACHE_DIR, "panel_monthly.csv")
PANEL_META = os.path.join(CACHE_DIR, "panel_meta.json")

FETCH_START = "1994-01-01"

# What each raw input costs in availability, and why. `pub_delay_days` applies
# to daily sources (calendar days subtracted from month end before taking the
# last print); `avail_lag` applies to monthly sources (whole months of shift).
AVAILABILITY = {
    "ptax": dict(kind="daily", pub_delay_days=0,
                 why="BCB PTAX is published the same afternoon."),
    "cds": dict(kind="daily", pub_delay_days=1,
                why="5y USD CDS quote; one day of slack for a stale tape."),
    "dxy": dict(kind="daily", pub_delay_days=1, why="FRED DTWEXBGS, ~1 day."),
    "dxy_em": dict(kind="daily", pub_delay_days=1, why="FRED DTWEXEMEGS, ~1 day."),
    "sp500": dict(kind="daily", pub_delay_days=0, why="Close, same day."),
    "brent": dict(kind="daily", pub_delay_days=0, why="Close, same day."),
    "fx_mx": dict(kind="daily", pub_delay_days=0, why="Spot close."),
    "fx_cl": dict(kind="daily", pub_delay_days=0, why="Spot close."),
    "fx_co": dict(kind="daily", pub_delay_days=0, why="Spot close."),
    "cc_total": dict(kind="daily", pub_delay_days=4,
                     why="BCB contracted FX posts on a ~2-business-day delay."),
    "cc_fin": dict(kind="daily", pub_delay_days=4, why="Same source as cc_total."),
    "cc_com": dict(kind="daily", pub_delay_days=4, why="Same source as cc_total."),
    "selic": dict(kind="monthly", avail_lag=0,
                  why="Policy rate — known continuously, no publication lag."),
    "fed_funds": dict(kind="monthly", avail_lag=0, why="Policy rate, as above."),
    "ipca_index": dict(kind="monthly", avail_lag=1,
                       why="IBGE publishes month m around the 10th of m+1."),
    "cpi_index": dict(kind="monthly", avail_lag=1,
                      why="BLS publishes month m mid-m+1 (FRED CPIAUCSL)."),
    "icbr_usd": dict(kind="monthly", avail_lag=1,
                     why="Monthly table in this repo; BCB posts early in m+1."),
    "reer": dict(kind="monthly", avail_lag=1,
                 why="BIS effective rates publish ~3rd week of m+1."),
    "tot": dict(kind="monthly", avail_lag=2,
                why="FUNCEX terms of trade run ~2 months behind."),
    "cot_lev_net": dict(kind="weekly", pub_delay_days=4,
                        why="CFTC: Tuesday positions released the following Friday."),
    "cot_asset_net": dict(kind="weekly", pub_delay_days=4, why="As above."),
}


def _read_table(database: str, table: str) -> pd.DataFrame:
    req = MySQLDataRequester(database, table)
    req.connect()
    df = req.request_data()
    req.close_connection()
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, Decimal)).any():
            df[col] = df[col].astype(float)
    return df


def _daily_series(database: str, table: str, where: dict) -> pd.Series:
    df = _read_table(database, table)
    for col, val in where.items():
        df = df[df[col] == val]
    s = df.set_index(pd.to_datetime(df["date"]))["value"].sort_index()
    return s[~s.index.duplicated(keep="last")]


def _asof_monthly(daily: pd.Series, pub_delay_days: int, name: str) -> pd.Series:
    """Value for month m = last print on or before month_end(m) - delay.

    A plain ``resample('M').last()`` would silently use a print that was not yet
    public on the last day of the month whenever the delay is non-zero, which is
    the one thing this lab cannot afford.
    """
    daily = daily.dropna().sort_index()
    if daily.empty:
        return pd.Series(dtype=float, name=name)
    months = pd.date_range(
        daily.index.min().to_period("M").to_timestamp(),
        daily.index.max().to_period("M").to_timestamp(),
        freq="MS",
    )
    cutoffs = (months + pd.offsets.MonthEnd(0)) - pd.Timedelta(days=pub_delay_days)
    out = daily.reindex(daily.index.union(cutoffs)).ffill().reindex(cutoffs)
    out.index = months
    return out.rename(name)


def _sum_monthly(daily: pd.Series, pub_delay_days: int, name: str) -> pd.Series:
    """Flow variables: sum of the month's prints that were public by month end.

    A month whose tail is still unpublished is therefore *understated*, not
    wrong — which is exactly the number a forecaster would have had. The
    alternative (waiting a month) throws away the other 95% of the month.
    """
    daily = daily.dropna().sort_index()
    if daily.empty:
        return pd.Series(dtype=float, name=name)
    months = pd.period_range(daily.index.min(), daily.index.max(), freq="M")
    vals = []
    for p in months:
        cutoff = p.to_timestamp("M") - pd.Timedelta(days=pub_delay_days)
        window = daily[(daily.index >= p.to_timestamp("D")) & (daily.index <= cutoff)]
        vals.append(window.sum() if len(window) else np.nan)
    return pd.Series(vals, index=months.to_timestamp(), name=name)


def _monthly_table(database: str, table: str, where: dict, avail_lag: int,
                   name: str) -> pd.Series:
    df = _read_table(database, table)
    for col, val in where.items():
        df = df[df[col] == val]
    s = df.set_index(pd.to_datetime(df["date"]))["value"].sort_index()
    s = s[~s.index.duplicated(keep="last")].resample("MS").last()
    return s.shift(avail_lag).rename(name)


def _realized_vol(daily_ptax: pd.Series, window_days: int, name: str) -> pd.Series:
    """Annualized realized vol of daily log returns, as of each month end."""
    r = np.log(daily_ptax).diff()
    v = r.rolling(window_days).std() * np.sqrt(252) * 100
    return _asof_monthly(v, 0, name)


def build_panel() -> pd.DataFrame:
    """Every column aligned to 'known on the last business day of the row's month'."""
    ptax_d = _daily_series("macro_brasil", "cmb_ptax", {"name": "ptax_venda"})
    cds_d = _daily_series("macro_brasil", "cmb_risco_pais", {"name": "cds_5y_usd"})
    dxy_d = _daily_series("macro_international", "cmb_dollar_index", {"name": "dxy"})
    dxyem_d = _daily_series("macro_international", "cmb_dollar_index_em", {"name": "dxy_em"})
    spx_d = _daily_series("macro_international", "cmb_equity_us", {"name": "sp500"})
    brent_d = _daily_series("macro_international", "comm_brent", {"name": "brent_usd"})

    latam = _read_table("macro_international", "cmb_fx_latam")
    latam["date"] = pd.to_datetime(latam["date"])
    fx_of = lambda cc: (latam[latam["country_code"] == cc]
                        .set_index("date")["value"].sort_index()
                        .pipe(lambda s: s[~s.index.duplicated(keep="last")]))

    cc = _read_table("macro_brasil", "cmb_cambio_contratado")
    cc["date"] = pd.to_datetime(cc["date"])
    cc_of = lambda n: (cc[cc["name"] == n].set_index("date")["value"].sort_index()
                       .pipe(lambda s: s[~s.index.duplicated(keep="last")]))

    cot = _read_table("macro_international", "cmb_cot_fx")
    cot["date"] = pd.to_datetime(cot["date"])
    cot_brl = cot[cot["currency"] == "BRL"] if "BRL" in set(cot["currency"]) else cot
    cot_of = lambda n: (cot_brl[cot_brl["name"] == n].set_index("date")["value"]
                        .sort_index().pipe(lambda s: s[~s.index.duplicated(keep="last")]))

    cols = [
        _asof_monthly(ptax_d, 0, "ptax"),
        _asof_monthly(cds_d, 1, "cds"),
        _asof_monthly(dxy_d, 1, "dxy"),
        _asof_monthly(dxyem_d, 1, "dxy_em"),
        _asof_monthly(spx_d, 0, "sp500"),
        _asof_monthly(brent_d, 0, "brent"),
        _asof_monthly(fx_of("MX"), 0, "fx_mx"),
        _asof_monthly(fx_of("CL"), 0, "fx_cl"),
        _asof_monthly(fx_of("CO"), 0, "fx_co"),
        _realized_vol(ptax_d, 63, "vol_3m"),
        _realized_vol(ptax_d, 252, "vol_12m"),
        _sum_monthly(cc_of("cc_saldo_total"), 4, "cc_total"),
        _sum_monthly(cc_of("cc_fin_saldo"), 4, "cc_fin"),
        _sum_monthly(cc_of("cc_saldo_comercial"), 4, "cc_com"),
        _monthly_table("macro_international", "diferenciais_juros",
                       {"name": "selic"}, 0, "selic"),
        _monthly_table("macro_international", "diferenciais_juros",
                       {"name": "fed_funds"}, 0, "fed_funds"),
        _monthly_table("macro_brasil", "comm_icbr_usd", {"name": "icbr_usd"}, 1, "icbr_usd"),
        _monthly_table("macro_international", "cmb_reer",
                       {"country_code": "BR", "reer_type": "real_broad"}, 1, "reer"),
        _monthly_table("macro_brasil", "cmb_termos_troca",
                       {"name": "termos_de_troca_funcex"}, 2, "tot"),
    ]

    for key, label in [("lev_net", "cot_lev_net"), ("asset_mgr_net", "cot_asset_net")]:
        s = cot_of(key)
        if len(s):
            cols.append(_asof_monthly(s, 4, label))

    # Prices, as index levels, shifted one month: relative PPP needs a level and
    # both statistical offices publish month m in the middle of m+1.
    ipca = _read_table("macro_brasil", "inflc_agregados")
    ipca = ipca[ipca["name"] == "ipca"]
    ipca_s = ipca.set_index(pd.to_datetime(ipca["date"]))["value"].sort_index()
    ipca_s = ipca_s[ipca_s.index >= FETCH_START]
    ipca_idx = ((ipca_s / 100 + 1).cumprod() * 100).resample("MS").last()
    cols.append(ipca_idx.shift(1).rename("ipca_index"))

    cpi = FredUniFrame("cpi_us", "CPIAUCSL", FETCH_START, None)
    cpi_s = cpi.set_index(pd.to_datetime(cpi["Date"]))["cpi_us"].sort_index()
    cpi_m = cpi_s.resample("MS").last()
    # Genuine hole: BLS never published an October 2025 CPI (shutdown). Same
    # treatment as ppp_equilibrium.load_data() — interpolate inside, never
    # extrapolate, so one real-world gap doesn't delete a month from the panel.
    cpi_m = cpi_m.interpolate(method="time", limit_area="inside")
    cols.append(cpi_m.shift(1).rename("cpi_index"))

    panel = pd.concat(cols, axis=1).sort_index()
    panel = panel[panel.index >= FETCH_START]
    return panel


def load_panel(refresh: bool = False) -> pd.DataFrame:
    if not refresh and os.path.exists(PANEL_CSV):
        df = pd.read_csv(PANEL_CSV, index_col=0, parse_dates=True)
        return df
    os.makedirs(CACHE_DIR, exist_ok=True)
    panel = build_panel()
    panel.to_csv(PANEL_CSV)
    meta = {
        "built_at": pd.Timestamp.now().isoformat(timespec="seconds"),
        "rows": int(len(panel)),
        "first": str(panel.index.min().date()),
        "last": str(panel.index.max().date()),
        "coverage": {c: [str(panel[c].first_valid_index()), str(panel[c].last_valid_index())]
                     for c in panel.columns},
        "availability": AVAILABILITY,
    }
    with open(PANEL_META, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False, default=str)
    return panel


if __name__ == "__main__":
    p = load_panel(refresh=True)
    print(p.tail(6).to_string())
    print()
    print("rows:", len(p), " span:", p.index.min().date(), "->", p.index.max().date())
    print()
    for c in p.columns:
        fv, lv = p[c].first_valid_index(), p[c].last_valid_index()
        print(f"  {c:<16} {str(fv)[:7]} -> {str(lv)[:7]}  n={int(p[c].notna().sum())}")
