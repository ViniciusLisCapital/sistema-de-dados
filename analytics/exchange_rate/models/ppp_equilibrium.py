"""
Relative-PPP equilibrium for USD/BRL — the first real-data building block for
referencia/equilibrium_model/state_space_equilibrium_model.md's measurement equation.

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

Also fetches the candidate channels for a future Bayesian model of the
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
  dxy     cmb_dollar_index.dxy (ICE US Dollar Index, DX-Y.NYB via Yahoo
          Finance, macro_international) from 1971 — a GLOBAL dollar-strength
          proxy, not bilateral BRL-specific like the other four channels.
          Added 2026-07-24 at the user's request to test whether it improves
          the state-space model's explicability alongside carry/tot/
          breakeven/fiscal.
  relative_carry  Selic minus the equal-weighted average policy rate of
          MX/CL/CO/PE (macro_international.cmb_policy_rates, BIS WS_CBPOL) --
          Brazil's rate advantage relative to its LatAm peers, rather than
          only against the US (`carry` above). AR excluded (BIS stopped
          updating it 2025-07; also a structural outlier vs. the other four
          inflation-targeters). Added 2026-07-28 to test whether REGIONAL
          relative positioning explains the deviation beyond the bilateral
          BR-US differential.
  carry_vol  carry / BRL's own trailing-6m annualized realized volatility
          (from daily PTAX, macro_brasil.cmb_ptax) -- a carry-to-volatility
          ("Sharpe-style") measure of Brazil's rate advantage per unit of
          FX risk. relative_carry_vol = carry_vol - mean(peer_carry_vol) for
          MX/CL/CO/PE, each peer's own carry_vol built the identical way
          (peer policy rate - Fed Funds, over that peer's own trailing-6m
          vol vs USD from the new macro_international.cmb_fx_latam, Yahoo
          Finance MXN=X/CLP=X/COP=X/PEN=X). Both added 2026-07-28, same
          equal-weight peer-average convention as relative_carry.
  dxy_em  macro_international.cmb_dollar_index_em.dxy_em (FRED DTWEXEMEGS,
          "Nominal Broad EM U.S. Dollar Index" — the Fed's own trade-weighted
          basket of ~19 EM currencies including BRL/CNY/MXN/KRW etc.) from
          2006-01. Added 2026-07-31 at the user's request, as an EM-specific
          co-movement proxy alongside (not replacing) `dxy` (the broad/DXY
          measure, mostly G10 currencies) -- the hypothesis being that BRL
          co-moves with the EM-FX complex specifically, a distinct channel
          from generic global-dollar strength. Already sitting in the DB,
          unused by any model until now.
  curve_steep_real  BR REAL yield-curve steepening, 10Y minus 2Y on the
          inflation-linked curve (NTNBJS @ 120M minus NTNBJS @ 24M,
          base_mercado.interest_rates -- same external schema/table
          curve_steep and breakeven already read). Added 2026-07-31 at the
          user's request, as an alternate fiscal-risk proxy to `curve_steep`
          (nominal) and `fiscal` (5y USD CDS): the hypothesis is that CDS,
          priced in USD against EXTERNAL default risk, understates domestic
          fiscal-sustainability risk given Brazil's large USD reserve
          buffer -- external default is remote even when the domestic
          debt/GDP trajectory looks worse. A real (inflation-linked) curve
          isolates the real term premium the market demands to hold
          long-dated BR government risk, net of inflation-expectations
          effects that contaminate the nominal steepening. Same
          `_PREJS_120M_BUG_WINDOWS`-style masking is unnecessary here --
          NTNBJS@120M is the confirmed-clean series (see _load_breakeven()'s
          docstring); only PREJS@120M has the bug. Real coverage starts
          2006-01, same as curve_steep.
  sp500   macro_international.cmb_equity_us.sp500 (Yahoo Finance ^GSPC, S&P
          500 index close) from 1990-01. Added 2026-07-31 at the user's
          request, testing a "competing for capital" hypothesis: a stronger
          US equity market pulls capital toward US assets, pressuring
          USD/BRL up independently of any Brazil-specific channel (same
          structural role as dxy/dxy_em, but from the equity side rather than
          FX/rates). Entered as its own monthly log-return in
          ridge_deviation_model.py (delta_sp500 = 100*diff(log(sp500)), NOT a
          plain level diff -- a price index's month-over-month change is
          properly a return, matching the convention already used for
          ptax/ipca_index/cpi_index elsewhere in this module). Tested
          alongside VIX (FRED VIXCLS) and the US 10Y real yield (FRED
          DFII10) as a joint "global risk/capital-competition" round --
          sp500 alone improved walk-forward OOS MSE ~4% with a stable,
          never-crosses-zero rolling coefficient; VIX and the real yield did
          NOT improve OOS MSE and were NOT ingested into the DB -- see
          ridge_deviation_model.py's module docstring and
          analytics/exchange_rate/CLAUDE.md for the full comparison. Read
          the finding narrowly: what carries signal is the S&P's own PRICE
          MOVE (a "competing for capital" / level-of-the-index effect), not
          general risk appetite/volatility -- VIX (the more direct risk-
          sentiment proxy) added nothing once sp500 was already in the
          regression.
  real_yield_diff  10Y REAL yield differential, BR minus US -- NTNBJS @ 120M
          (base_mercado.interest_rates, the same series curve_steep_real
          already reads) minus DFII10 (US 10Y TIPS real yield, FRED). Added
          2026-07-31 at the user's request, as a risk-premium measure. NOT
          the same test as the earlier "US 10Y real yield" entry above (that
          was DFII10 alone, a standalone US-level channel testing a global
          "competing for capital via rates" story, and it did NOT clear the
          walk-forward OOS bar) -- this is a BR-US DIFFERENTIAL, a genuinely
          different construction, tested 2026-07-31 and found to clear the
          bar cleanly (-1.7% OOS MSE alone, stable positive coefficient,
          never crosses zero across 163 rolling windows). Read the sign
          carefully: positive, meaning a WIDER BR-US real-rate gap moves
          delta_fx UP (BRL weaker) -- the opposite of a naive UIP/carry-
          attractiveness reading (which would expect a higher real yield to
          attract capital and strengthen BRL), but consistent with reading
          Brazil's own real yield as a RISK PREMIUM: a rising BR real yield
          often reflects the market demanding more compensation for BR risk,
          moving the same direction as fiscal/curve_steep rather than against
          it. Real coverage from 2006-01 (NTNBJS@120M's own start, the
          binding constraint here -- DFII10 itself goes back to 2003-01).
  icbr_usd  macro_brasil.comm_icbr_usd.icbr_usd (BCB SGS 29042) from 1998-01
          -- the USD-denominated IC-Br general commodity index, DISTINCT
          from comm_icbr (SGS 27574 etc., the BRL-denominated version
          already in the DB, used by analytics/monetary_policy/'s Phillips-
          curve model). The BRL version is UNSUITABLE as a regressor here:
          the BCB converts international commodity prices INTO REAIS as
          part of that index's own construction, so it already partly
          embeds USD/BRL's own move -- circular if used to explain delta_fx.
          SGS 29042 (user-identified; not independently confirmed via the
          BCB's own metadata API, which requires an authenticated session --
          corroborated only indirectly, by returning materially different
          values from SGS 27574 for the same months, consistent with two
          distinct denominations of the same underlying index) sidesteps
          that problem. Tested 2026-07-31: the single largest new channel
          this round -- reliably NEGATIVE across nearly the whole rolling
          history (mean -0.93, essentially never flips positive) and
          improved walk-forward OOS MSE ~4.6% alone. Sign makes clean sense:
          rising global commodity prices, Brazil being a major commodity
          exporter, strengthen BRL (delta_fx down) -- a genuine terms-of-
          trade/export-basket channel, distinct from `tot` (not currently in
          the shipped 7/9-channel spec) and from `sp500` (equities, not
          commodities).
  trade_pct_gdp / ca_pct_gdp  Trade balance and current account, both as %
          of GDP (cmb_balanco_pagmt.exportacao_bens - importacao_bens, and
          .conta_corrente respectively, both macro_brasil, BCB BOP BPM6) over
          atv_pib_usd.pib_usd (BCB SGS 4385, monthly GDP in USD). Same 12-
          month TRAILING-SUM-over-trailing-sum convention already used by
          analytics/exchange_rate/generate_report.py's own "% PIB" toggle
          (not a single month's noisy ratio) -- reused here rather than
          inventing a second convention for the same two series. From
          1995-01 (both series' own start), though the model's actual
          binding constraint remains fiscal (2007-12). Added 2026-07-24 for
          the "BEER-style levels" model (see beer_model.py) after a
          throwaway delta-channel test (scratchpad, not committed) found
          neither trade nor CA added signal in delta form.
          Data-quality fix carried over from referencia/equilibrium_model/state_space_equilibrium_model.md's
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
All ten are left-joined onto the core (ptax/ipca/cpi) monthly index, so
each column is simply null before its own series starts — no padding or
back-filling.

Not wired into generate_report.py — renders a standalone, self-contained
dashboard (models/ppp_dashboard_template.html -> reports/ppp_dashboard.html,
untracked/regenerate-only like every other report in reports/ — moved out of
referencia/ 2026-08, since it's a code-generated deliverable, not background
reading) with a client-side base-month selector, following the same
/*MARKER*/ + str.replace() templating convention as generate_report.py.

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
_OUTPUT = Path(__file__).parent.parent.parent.parent / "reports" / "ppp_dashboard.html"

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


def _load_interest_rate_curves() -> pd.DataFrame:
    """Raw base_mercado.interest_rates table, read once and shared by
    _load_breakeven() and _load_curve_steepening() -- both need PREJS@120M,
    and re-reading the same external table twice per load_data() call would
    be a wasted round-trip on a schema outside this project's own ETL --
    same precedent as _load_policy_rates_monthly() being shared by
    _load_relative_carry()/_load_carry_vol_metrics()."""
    curves = _read_table("base_mercado", "interest_rates")
    curves["date"] = pd.to_datetime(curves["date"])
    curves["value"] = curves["value"].astype(float)
    return curves


def _load_breakeven(curves: pd.DataFrame) -> pd.Series:
    """10y bond-implied breakeven inflation (PREJS - NTNBJS @ 120M), monthly,
    with the confirmed PREJS@120M bug windows masked and linearly interpolated."""
    prejs = curves[(curves["curve"] == "PREJS") & (curves["tenor"] == "120M")].set_index("date")["value"].sort_index()
    ntnbjs = curves[(curves["curve"] == "NTNBJS") & (curves["tenor"] == "120M")].set_index("date")["value"].sort_index()

    for start, end in _PREJS_120M_BUG_WINDOWS:
        prejs.loc[start:end] = pd.NA
    prejs = prejs.astype(float).interpolate(method="time")

    breakeven = (prejs - ntnbjs).dropna()
    return breakeven.resample("MS").last().rename("breakeven")


def _load_curve_steepening(curves: pd.DataFrame) -> pd.Series:
    """BR nominal yield-curve steepening, 10Y minus 2Y (PREJS @ 120M minus
    PREJS @ 24M, base_mercado.interest_rates -- same external fund-ops
    schema _load_breakeven() reads) -- added 2026-07-30, direct user request,
    as an alternate, market-based proxy for fiscal risk alongside (not
    replacing) the CDS-based `fiscal` channel: when markets price rising
    long-run fiscal risk (debt-sustainability concerns, monetization risk),
    long-dated rates move more than short, policy-anchored ones, steepening
    the curve independently of whether 5y CDS itself moves. PREJS@120M's
    confirmed bug windows (see _PREJS_120M_BUG_WINDOWS / _load_breakeven())
    are masked and interpolated here too, same treatment, same reason --
    isolated to that one curve/tenor, so PREJS@24M needs no equivalent
    masking. Real coverage starts 2006-01 (verified against Tesouro Direto
    -- no BR pre-fixed bond traded past ~1.6y maturity before then)."""
    prejs_120 = curves[(curves["curve"] == "PREJS") & (curves["tenor"] == "120M")].set_index("date")["value"].sort_index()
    prejs_24 = curves[(curves["curve"] == "PREJS") & (curves["tenor"] == "24M")].set_index("date")["value"].sort_index()

    for start, end in _PREJS_120M_BUG_WINDOWS:
        prejs_120.loc[start:end] = pd.NA
    prejs_120 = prejs_120.astype(float).interpolate(method="time")

    steepening = (prejs_120 - prejs_24).dropna()
    return steepening.resample("MS").last().rename("curve_steep")


def _load_curve_steepening_real(curves: pd.DataFrame) -> pd.Series:
    """BR REAL yield-curve steepening, 10Y minus 2Y on the inflation-linked
    curve (NTNBJS @ 120M minus NTNBJS @ 24M) -- added 2026-07-31, direct user
    request, as an alternate fiscal-risk proxy alongside `curve_steep`
    (nominal) and `fiscal` (CDS): isolates the real term premium, net of
    inflation-expectations effects that a nominal curve mixes in. No bug-
    window masking needed -- NTNBJS@120M is the confirmed-clean series (only
    PREJS@120M has the documented bug, see _PREJS_120M_BUG_WINDOWS)."""
    ntnbjs_120 = curves[(curves["curve"] == "NTNBJS") & (curves["tenor"] == "120M")].set_index("date")["value"].sort_index()
    ntnbjs_24 = curves[(curves["curve"] == "NTNBJS") & (curves["tenor"] == "24M")].set_index("date")["value"].sort_index()

    steepening = (ntnbjs_120 - ntnbjs_24).dropna()
    return steepening.resample("MS").last().rename("curve_steep_real")


def _load_real_yield_diff(curves: pd.DataFrame) -> pd.Series:
    """10Y REAL yield differential, BR minus US -- NTNBJS @ 120M
    (base_mercado.interest_rates, the same series curve_steep_real already
    reads, confirmed-clean, no bug-window masking needed) minus DFII10 (US
    10Y TIPS real yield, FRED). Added 2026-07-31, direct user request, as a
    risk-premium measure alongside the CDS/curve-based fiscal-risk proxies
    already in the model. Real coverage from 2006-01 (NTNBJS@120M's own
    start -- the binding constraint here; DFII10 itself goes back to
    2003-01, TIPS market inception). Tested 2026-07-31 in
    ridge_deviation_model.py: positive, stable coefficient (never crosses
    zero across 163 rolling windows) -- read as a RISK-PREMIUM signal (same
    direction as fiscal/curve_steep), not a carry-attractiveness one -- a
    rising BR-US real yield gap here moves WITH BRL depreciation rather than
    against it, opposite the naive UIP-style expectation that a wider real-
    rate advantage should attract capital and strengthen the currency."""
    ntnbjs_120 = curves[(curves["curve"] == "NTNBJS") & (curves["tenor"] == "120M")].set_index("date")["value"].sort_index()
    br_real10y_m = ntnbjs_120.resample("MS").last()

    us_real10y = FredUniFrame("us_real_10y", "DFII10", _FETCH_START, None)
    us_real10y_m = us_real10y.set_index(pd.to_datetime(us_real10y["Date"]))["us_real_10y"].sort_index().resample("MS").last()

    return (br_real10y_m - us_real10y_m).dropna().rename("real_yield_diff")


_LATAM_PEERS = ["MX", "CL", "CO", "PE"]


def _load_policy_rates_monthly() -> pd.DataFrame:
    """Wide monthly BIS policy rates (macro_international.cmb_policy_rates),
    one column per country_code (BR + the 4 LatAm peers, AR excluded -- see
    load_data()'s docstring) -- shared by _load_relative_carry() and
    _load_carry_vol_metrics() so the table is only read/pivoted once."""
    rates = _read_table("macro_international", "cmb_policy_rates")
    rates["date"] = pd.to_datetime(rates["date"])
    rates["value"] = rates["value"].astype(float)
    wide = rates.pivot_table(index="date", columns="country_code", values="value")
    return wide.resample("MS").last()


def _load_relative_carry() -> pd.Series:
    """relative_carry(t) = Selic(t) - mean(MX, CL, CO, PE policy rate)(t).

    Since Fed Funds cancels out of (Selic - FF) - mean(peer - FF), this is
    exactly Selic minus the equal-weighted peer level -- no need to net out
    the US rate a second time. AR excluded (see load_data()'s docstring)."""
    monthly = _load_policy_rates_monthly()
    peer_avg = monthly[_LATAM_PEERS].mean(axis=1)
    return (monthly["BR"] - peer_avg).rename("relative_carry")


def _load_daily_ptax() -> pd.Series:
    """Raw daily PTAX (macro_brasil.cmb_ptax, ptax_venda) -- NOT resampled,
    unlike every other loader in this module. Needed at daily frequency for
    _annualized_vol_6m(); the rest of the module only ever needs the
    already-monthly ptax_m built in load_data()."""
    ptax = _read_table("macro_brasil", "cmb_ptax")
    ptax = ptax[ptax["name"] == "ptax_venda"]
    return ptax.set_index(pd.to_datetime(ptax["date"]))["value"].astype(float).sort_index()


def _load_daily_peer_fx() -> pd.DataFrame:
    """Wide daily LatAm peer FX rates vs USD (macro_international.cmb_fx_latam,
    Yahoo Finance MXN=X/CLP=X/COP=X/PEN=X), one column per country_code."""
    fx = _read_table("macro_international", "cmb_fx_latam")
    fx["date"] = pd.to_datetime(fx["date"])
    fx["value"] = fx["value"].astype(float)
    return fx.pivot_table(index="date", columns="country_code", values="value").sort_index()


def _annualized_vol_6m(daily: pd.Series) -> pd.Series:
    """Trailing 6-month (126 trading-day) annualized realized volatility of
    a daily FX rate, in percent -- standard construction (log returns,
    sqrt(252) annualization), resampled to month-end (MS) to align with the
    rest of this module's monthly index. min_periods=90 lets the window
    start reporting before a full 126 observations accumulate, same
    tolerance the rest of this module applies to its own ramp-up periods."""
    log_ret = np.log(daily / daily.shift(1))
    vol = log_ret.rolling(window=126, min_periods=90).std() * np.sqrt(252) * 100
    return vol.resample("MS").last()


def _load_carry_vol_metrics(carry_m: pd.Series) -> pd.DataFrame:
    """carry_vol(t) = carry(t) / BRL's own trailing-6m annualized realized
    vol (from daily PTAX) -- a carry-to-volatility ("Sharpe-style") measure
    of Brazil's rate advantage per unit of FX risk taken, rather than the
    raw rate differential alone.

    relative_carry_vol(t) = carry_vol(t) - mean(peer_carry_vol(t)) for
    MX/CL/CO/PE, each peer's own carry_vol built identically (peer policy
    rate - Fed Funds, over that peer's own trailing-6m annualized vol vs
    USD from cmb_fx_latam) -- same equal-weight peer-average convention
    already used by relative_carry above, just applied to the risk-adjusted
    metric instead of the raw rate. Added 2026-07-28 at the user's request,
    to test whether the carry trade's RISK-ADJUSTED attractiveness (not
    just the level of the rate differential) explains the deviation, and
    whether that's a bilateral BR-US or a regional-peer-relative story."""
    brl_vol_m = _annualized_vol_6m(_load_daily_ptax())
    carry_vol = (carry_m / brl_vol_m).rename("carry_vol")

    rates_m = _load_policy_rates_monthly()
    fed_funds_m = _monthly_series("macro_international", "diferenciais_juros", "fed_funds", "fed_funds")
    peer_fx_daily = _load_daily_peer_fx()

    peer_carry_vols = []
    for peer in _LATAM_PEERS:
        peer_carry = rates_m[peer] - fed_funds_m
        peer_vol = _annualized_vol_6m(peer_fx_daily[peer])
        peer_carry_vols.append(peer_carry / peer_vol)
    peer_carry_vol_avg = pd.concat(peer_carry_vols, axis=1).mean(axis=1)

    relative_carry_vol = (carry_vol - peer_carry_vol_avg).rename("relative_carry_vol")
    return pd.concat([carry_vol, relative_carry_vol], axis=1)


def _load_bop_pct_gdp() -> pd.DataFrame:
    """Trade balance and current account, both as % of GDP -- 12m trailing
    sum of the flow over 12m trailing sum of pib_usd, same convention as
    generate_report.py's "% PIB" toggle. See load_data()'s docstring."""
    gdp = _monthly_series("macro_brasil", "atv_pib_usd", "pib_usd", "pib_usd")
    gdp_12m = gdp.rolling(12).sum()

    bop = _read_table("macro_brasil", "cmb_balanco_pagmt")
    bop_wide = bop.pivot_table(index="date", columns="name", values="value")
    bop_wide.index = pd.to_datetime(bop_wide.index)
    bop_wide = bop_wide.resample("MS").last()

    trade = bop_wide["exportacao_bens"] - bop_wide["importacao_bens"]
    ca = bop_wide["conta_corrente"]

    return pd.DataFrame({
        "trade_pct_gdp": 100 * trade.rolling(12).sum() / gdp_12m,
        "ca_pct_gdp": 100 * ca.rolling(12).sum() / gdp_12m,
    })


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
    # FRED CPIAUCSL has a genuine NaN at 2025-10-01 -- BLS didn't collect CPI
    # data during the Oct-Nov 2025 government shutdown and never published an
    # October 2025 report. Interpolated (not dropped) so this one confirmed
    # real-world gap doesn't delete the whole month from every downstream
    # chart via the dropna() below -- same "isolated known gap, fix it here"
    # precedent as the PREJS@120M bug window in _load_breakeven(). limit_area
    # ="inside" keeps this from ever extrapolating beyond real data at either
    # end of the series.
    cpi_m = cpi_m.interpolate(method="time", limit_area="inside")

    core = pd.concat([ptax_m, ipca_index, cpi_m], axis=1).dropna()

    carry_m = _monthly_series("macro_international", "diferenciais_juros", "diferencial_nominal", "carry")
    tot_m = _monthly_series("macro_brasil", "cmb_termos_troca", "termos_de_troca_funcex", "tot")
    fiscal_m = _monthly_series("macro_brasil", "cmb_risco_pais", "cds_5y_usd", "fiscal")
    curves = _load_interest_rate_curves()
    breakeven_m = _load_breakeven(curves)
    curve_steep_m = _load_curve_steepening(curves)
    curve_steep_real_m = _load_curve_steepening_real(curves)
    real_yield_diff_m = _load_real_yield_diff(curves)
    dxy_m = _monthly_series("macro_international", "cmb_dollar_index", "dxy", "dxy")
    dxy_em_m = _monthly_series("macro_international", "cmb_dollar_index_em", "dxy_em", "dxy_em")
    sp500_m = _monthly_series("macro_international", "cmb_equity_us", "sp500", "sp500")
    icbr_usd_m = _monthly_series("macro_brasil", "comm_icbr_usd", "icbr_usd", "icbr_usd")
    relative_carry_m = _load_relative_carry()
    carry_vol_df = _load_carry_vol_metrics(carry_m)
    bop_pct_gdp = _load_bop_pct_gdp()
    target_annual = _load_inflation_target()

    df = core.join(
        [carry_m, tot_m, fiscal_m, breakeven_m, curve_steep_m, curve_steep_real_m, real_yield_diff_m,
         dxy_m, dxy_em_m, sp500_m, icbr_usd_m,
         relative_carry_m, carry_vol_df, bop_pct_gdp, target_annual],
        how="left",
    )
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
        "dxy": _to_jsonable(df["dxy"]),
        "sp500": _to_jsonable(df["sp500"]),
        "icbr_usd": _to_jsonable(df["icbr_usd"]),
        "real_yield_diff": _to_jsonable(df["real_yield_diff"]),
        "relative_carry": _to_jsonable(df["relative_carry"]),
        "carry_vol": _to_jsonable(df["carry_vol"]),
        "relative_carry_vol": _to_jsonable(df["relative_carry_vol"]),
        "trade_pct_gdp": _to_jsonable(df["trade_pct_gdp"]),
        "ca_pct_gdp": _to_jsonable(df["ca_pct_gdp"]),
        "breakeven_gap": _to_jsonable(df["breakeven_gap"]),
        "default_base_month": default_base_month,
    }


def render(payload: dict, fxattr_payload: dict | None = None, ridge_payload: dict | None = None) -> None:
    """Fills the template's three markers. `/*PPP_DATA*/` always gets
    `payload`; `/*FXATTR_DATA*/` and `/*RIDGE_DATA*/` get their respective
    payload if given, else the literal `null` (so each tab's JS always has
    something valid to check against, whether or not that tab's data was
    generated this run).

    Down from eight markers/params to three, 2026-07-30, direct user request
    ("remove the other tabs") -- the Bayesian Model, State-Space (Attempt
    Two), Kalman Filter (η free), BEER Model (Levels), and Rolling Window
    (Core 4) tabs (and their `/*BAYES_DATA*/`/`/*STATESPACE_DATA*/`/
    `/*KALMAN_DATA*/`/`/*BEER_DATA*/`/`/*ROLLING_DATA*/` markers) were
    removed from the template entirely to declutter the dashboard down to
    Equilibrium & Data, FX Attribution, and Ridge. Their own modules
    (bayesian_deviation_model.py, state_space_model.py's build_dashboard_payload()/
    build_kalman_dashboard_payload(), beer_model.py) are untouched and still
    work standalone -- only the dashboard wiring was removed. This also
    retires the Kalman-tab staleness bug that used to force a surgical
    single-line RIDGE_DATA replacement instead of a full render_dashboard()
    call -- see CLAUDE.md."""
    template = _TEMPLATE.read_text(encoding="utf-8")
    html = template.replace("/*PPP_DATA*/", json.dumps(payload))
    html = html.replace("/*FXATTR_DATA*/", json.dumps(fxattr_payload) if fxattr_payload is not None else "null")
    html = html.replace("/*RIDGE_DATA*/", json.dumps(ridge_payload) if ridge_payload is not None else "null")
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
    for col in ("carry", "relative_carry", "carry_vol", "relative_carry_vol", "tot", "fiscal", "breakeven", "dxy", "trade_pct_gdp", "ca_pct_gdp", "target", "breakeven_gap"):
        s = df[col].dropna()
        print(f"  {col}: {s.index.min().date()} .. {s.index.max().date()}  (n={len(s)})")
    print(f"Dashboard written to {_OUTPUT}")

    return {"data": df, "payload": payload}


if __name__ == "__main__":
    run()
