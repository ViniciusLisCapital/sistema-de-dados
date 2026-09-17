"""Feature matrix, built only from things dated at or before the forecast origin.

`data.load_panel()` already guarantees that row ``m`` of the panel is what was
readable on the last business day of ``m``. This module therefore only has to
avoid one mistake: never use a ``.shift(-k)``, never centre a rolling window,
never fit a normalisation on the full sample. Every transform here is backward-
looking by construction, and the standardisation happens inside the backtest's
training window, not here.

Two kinds of feature, deliberately kept apart, because they answer different
questions and tend to work at different horizons:

- **Gaps** — a level measured against its own slow-moving reference (PPP,
  REER, real carry, CDS against its own 5y average). These are the ones the
  literature finds at 12+ months, and they are the reason a forecast can beat a
  random walk at all: they say "this level is far from where it usually sits".
- **Moves** — last month's, last quarter's, last year's change. Momentum and
  short-run reversal. These are what could work at h=1 if anything does.

`FEATURE_SETS` groups them into the specs the horse race actually runs. The
grouping matters for a reason that has nothing to do with economics: each block
has its own natural start (dxy_em 2006, contracted FX 2008, CFTC 2011), so a
spec that includes a late-starting block silently shortens the sample for every
model it is compared against. The backtest aligns origins across models before
scoring, but the sample a spec *can* reach is decided here.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from tests.fx_forecast_lab.data import load_panel


def _log(s: pd.Series) -> pd.Series:
    return np.log(s.replace(0, np.nan))


def build_features(panel: pd.DataFrame | None = None) -> pd.DataFrame:
    p = load_panel() if panel is None else panel
    f = pd.DataFrame(index=p.index)

    lp = _log(p["ptax"])

    # --- moves in the exchange rate itself -------------------------------
    f["mom_1"] = 100 * lp.diff(1)
    f["mom_3"] = 100 * lp.diff(3)
    f["mom_12"] = 100 * lp.diff(12)
    # Distance from own trailing average: the pure technical mean-reversion
    # term, and the one a random walk says must be worthless.
    f["ma_gap_12"] = 100 * (lp - lp.rolling(12).mean())
    f["ma_gap_60"] = 100 * (lp - lp.rolling(60).mean())

    # --- valuation gaps ---------------------------------------------------
    # Relative PPP: where the nominal rate would be if it had only tracked the
    # BR-US price ratio since the panel's first month, in logs. The base month
    # cancels out of any regression with an intercept, so its choice is not a
    # free parameter here.
    rel_price = _log(p["ipca_index"]) - _log(p["cpi_index"])
    f["ppp_gap"] = 100 * (lp - rel_price - (lp - rel_price).rolling(120, min_periods=60).mean())
    f["ppp_drift_12"] = 100 * rel_price.diff(12)

    lreer = _log(p["reer"])
    f["reer_gap_60"] = 100 * (lreer - lreer.rolling(60, min_periods=36).mean())
    f["reer_mom_12"] = 100 * lreer.diff(12)

    # --- carry / UIP ------------------------------------------------------
    carry = p["selic"] - p["fed_funds"]
    f["carry"] = carry
    f["carry_gap_60"] = carry - carry.rolling(60, min_periods=36).mean()
    # Carry per unit of risk. The classic reason a high nominal differential is
    # not automatically attractive.
    f["carry_vol"] = carry / p["vol_12m"]
    f["real_carry"] = ((p["selic"] - 100 * (_log(p["ipca_index"]).diff(12)))
                       - (p["fed_funds"] - 100 * (_log(p["cpi_index"]).diff(12))))

    # --- risk -------------------------------------------------------------
    lcds = _log(p["cds"])
    f["cds_gap_60"] = 100 * (lcds - lcds.rolling(60, min_periods=36).mean())
    f["cds_mom_3"] = 100 * lcds.diff(3)
    f["vol_3m"] = p["vol_3m"]
    f["vol_ratio"] = p["vol_3m"] / p["vol_12m"]

    # --- global dollar / equity ------------------------------------------
    f["dxy_mom_3"] = 100 * _log(p["dxy"]).diff(3)
    f["dxy_em_mom_3"] = 100 * _log(p["dxy_em"]).diff(3)
    f["dxy_em_gap_60"] = 100 * (_log(p["dxy_em"]) - _log(p["dxy_em"]).rolling(60, min_periods=36).mean())
    f["spx_mom_3"] = 100 * _log(p["sp500"]).diff(3)
    f["spx_mom_12"] = 100 * _log(p["sp500"]).diff(12)

    # --- commodities / terms of trade ------------------------------------
    f["brent_mom_3"] = 100 * _log(p["brent"]).diff(3)
    f["icbr_mom_3"] = 100 * _log(p["icbr_usd"]).diff(3)
    f["icbr_gap_60"] = 100 * (_log(p["icbr_usd"]) - _log(p["icbr_usd"]).rolling(60, min_periods=36).mean())
    f["tot_mom_12"] = 100 * _log(p["tot"]).diff(12)

    # --- peers ------------------------------------------------------------
    peers = pd.concat([_log(p["fx_mx"]), _log(p["fx_cl"]), _log(p["fx_co"])], axis=1)
    f["peer_mom_3"] = 100 * peers.diff(3).mean(axis=1)
    # BRL against the LatAm basket: is the real already cheap relative to its
    # peers, or has it simply moved with them?
    f["peer_rel_12"] = f["mom_12"] - 100 * peers.diff(12).mean(axis=1)

    # --- flow / positioning ----------------------------------------------
    # Contracted FX in USD millions is not comparable across two decades of a
    # growing economy; scaled by trailing turnover it is.
    cc12 = p["cc_total"].rolling(12).sum()
    f["cc_flow_12"] = cc12 / p["cc_total"].abs().rolling(12).sum()
    f["cc_flow_3"] = (p["cc_total"].rolling(3).sum()
                      / p["cc_total"].abs().rolling(12).sum())
    if "cot_lev_net" in p.columns:
        cot = p["cot_lev_net"]
        f["cot_z"] = (cot - cot.rolling(36, min_periods=24).mean()) / cot.rolling(36, min_periods=24).std()

    return f


# Blocks, named so a spec reads as a hypothesis rather than a column list.
BLOCKS = {
    "fx_moves": ["mom_1", "mom_3", "mom_12", "ma_gap_12", "ma_gap_60"],
    "valuation": ["ppp_gap", "ppp_drift_12", "reer_gap_60", "reer_mom_12"],
    "carry": ["carry", "carry_gap_60", "carry_vol", "real_carry"],
    "risk": ["cds_gap_60", "cds_mom_3", "vol_3m", "vol_ratio"],
    "global": ["dxy_mom_3", "dxy_em_mom_3", "dxy_em_gap_60", "spx_mom_3", "spx_mom_12"],
    "commodity": ["brent_mom_3", "icbr_mom_3", "icbr_gap_60", "tot_mom_12"],
    "peers": ["peer_mom_3", "peer_rel_12"],
    "flow": ["cc_flow_12", "cc_flow_3", "cot_z"],
}

FEATURE_SETS = {
    # Long sample (starts with PPP/REER/carry data, ~1999): the blocks the
    # literature actually claims predict FX, and nothing that starts late.
    "fundamentals": BLOCKS["valuation"] + BLOCKS["carry"],
    "technical": BLOCKS["fx_moves"],
    "fund_tech": BLOCKS["valuation"] + BLOCKS["carry"] + BLOCKS["fx_moves"],
    # Adds CDS (2001) and commodities (1998) — still no dxy_em/flow.
    "wide_2001": (BLOCKS["valuation"] + BLOCKS["carry"] + BLOCKS["fx_moves"]
                  + BLOCKS["risk"] + BLOCKS["commodity"]),
    # Everything except CFTC positioning: starts 2008 (contracted FX).
    "wide_2008": (BLOCKS["valuation"] + BLOCKS["carry"] + BLOCKS["fx_moves"]
                  + BLOCKS["risk"] + BLOCKS["commodity"] + BLOCKS["global"]
                  + BLOCKS["peers"] + ["cc_flow_12", "cc_flow_3"]),
    # The shipped FX Model's five channels, expressed as things known at T
    # rather than as realized contemporaneous moves. The point of comparison
    # with `models/ridge_vs_random_walk.md`.
    "shipped_lagged": ["cds_mom_3", "cds_gap_60", "dxy_em_mom_3", "carry_vol",
                       "spx_mom_3", "icbr_mom_3", "ppp_drift_12"],
}


def target(panel: pd.DataFrame, h: int) -> pd.Series:
    """Cumulative h-month log return in pp: 100*log(ptax[t+h]/ptax[t]).

    Same scored quantity as `models/ridge_vs_random_walk.md`, so the two notes'
    numbers sit on the same ruler — that one is the conditional bound, this one
    the unconditional. Positive = BRL depreciates.
    """
    lp = _log(panel["ptax"])
    return (100 * (lp.shift(-h) - lp)).rename(f"y_{h}")


if __name__ == "__main__":
    p = load_panel()
    f = build_features(p)
    print(f"{len(f.columns)} features, {len(f)} rows")
    for name, cols in FEATURE_SETS.items():
        sub = f[cols].dropna()
        print(f"  {name:<16} {len(cols):>2} cols  "
              f"{str(sub.index.min())[:7]} -> {str(sub.index.max())[:7]}  n={len(sub)}")
    print()
    print("first valid per feature:")
    for c in f.columns:
        print(f"  {c:<16} {str(f[c].first_valid_index())[:7]}  n={int(f[c].notna().sum())}")
