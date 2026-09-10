"""
Base scenarios for the Ridge model's exogenous channels.

Built 2026-09-08 at direct user request: "eu quero estressar alguns cenarios
para a taxa de cambio no Brasil ... temos as variaveis exogenas do nosso
modelo. Eu quero considerar alguns cenarios padrao para elas. Vamos comecar
com (i) CDS. Estamos em ano de eleicao e quero entender o comportamento do CDS
nos T-12 meses anteriores ao primeiro e segundo turno ... tambem quero estudar
o comportamento do CDS em momentos de crise, como a crise de 2008, 2015-2016,
2020. Para que fique claro, eu quero ter uma ordem de magnitude para os
movimentos dessa variavel."

The 12-Month Forecast card on the FX Model tab asks the reader to type twelve
levels per channel. Nothing on the page said what a *large* twelve months looks
like for any of them, so every entered path was a guess with no yardstick. This
module measures the yardstick from each channel's own history: a small library
of dated episodes, each reduced to a base level, a peak, a multiple and a
13-point ratio path the forecast boxes can take verbatim.

WHAT IS MEASURED, AND WHY IT IS MEASURED THIS WAY
=================================================

Every episode is reduced by the SAME four rules, so two episodes are
comparable:

1. `base` is the monthly close of the month the run-up starts FROM (the month
   before month 1 of the path). Every ratio in the path divides by it.
2. `peak` is the highest MONTHLY CLOSE inside the window -- not the highest
   daily print. The model this feeds is monthly, so a monthly path cannot
   represent an intraday spike, and quoting the spike as the scenario
   magnitude would promise the boxes something they cannot hold. The daily
   spike is carried separately (`spike`), because it is genuinely what the
   crisis looked like while it happened -- Brazil's CDS printed above 560 bps
   for four days in October 2008, peaking at 587, against a 316 bps close for
   that month and a 401 bps peak monthly close for the whole episode.
3. `path` is 13 ratios to `base`, month 0 = 1.0 by construction. Box h of the
   forecast card takes `path[h + 1]`.
4. Episodes are applied MULTIPLICATIVELY, and that is a measurement, not a
   convention (see below).

MULTIPLICATIVE, NOT ADDITIVE -- MEASURED
----------------------------------------
An episode has to be re-anchored on today's level, and the choice between
"add the historical bps" and "multiply by the historical ratio" is not
cosmetic: the three crises started from bases between 103 and 176 bps and the
2002 election from 1100, so the two rules diverge as soon as today's level
differs from the episode's.

Measured on this series' 299 monthly changes, split into level quartiles:

    level quartile   median level   mean |change|, bps   mean |change|, %
    62-136 bps           119               15.4              12.3
    136-180 bps          156               19.6              12.2
    180-277 bps          224               24.9              11.3
    277-3790 bps         460              128.5              14.2

The bps column runs 8x across the range; the % column moves by a fifth. Same
result as a correlation: corr(|d bps|, level) = +0.741, while
corr(|d log|, level) = +0.122. So the CDS moves proportionally, and the ratio
path is the transferable object. `is_multiplicative` carries this per channel
rather than assuming it for the next one -- a channel measured in percentage
points (a rate gap) will very likely test the other way.

Both columns were measured on the investing.com series before 2026-09-08 and
said the same thing far more weakly (+0.334 against +0.030, and a bps column
that merely doubled). The finding did not change; its evidence did, because
the old source topped out at 471 bps and this one reaches 3790, which is where
a proportional rule and an additive one actually part company.

THE ELECTION FINDING
--------------------
The user asked for the 12 months before the first round AND before the second.
On a monthly grid those are the SAME WINDOW: in all seven elections both rounds
fall in October, so "T-12 to R1" and "T-12 to R2" share every one of the twelve
months, and the ratio paths came out identical to the third decimal. Rather
than ship seven duplicated pairs, each election is one monthly path, and the
round-to-round question is answered where it is actually answerable -- on the
daily series, in `inter_round`.

That leg is the most consistent thing in the whole library: the CDS FELL
between the two rounds in all SIX completed elections (-298, -24, -12, -10,
-39, -33 bps; -8%, -18%, -11%, -5%, -16%, -11%). Adding 2002 and 2006 on
2026-09-08 was the first chance to test it out of the sample it was found in,
and it held in both.

The run-up is where the reading changed, and it inverted. On the old series
the honest headline was "elections peak at 1.0x-1.8x their T-12 base, crises
at 2.7x-3.3x" -- an election was reliably the smaller event. With 2002 in, the
largest episode in the library is an ELECTION, at 3.44x, above all three
crises (2.73x-3.07x); the range for elections is now 1.00x-3.44x and the
distribution is bimodal, not a band. Six of the seven sit at 1.00x-1.76x and
one is off on its own, which is a different claim from "elections are mild":
it is "elections are mild unless the market doubts the regime, and then they
are the largest thing here". 2002 was the election of a candidate the market
priced as a default risk, so the reader has a criterion rather than a range.

DO NOT DOUBLE-COUNT THE WORLD
-----------------------------
`concurrent` carries what the OTHER channels of the same regression did over
the same base-to-peak leg, and it exists because those channels are in the
regression too: applying the 2018 CDS path while leaving dxy_em flat is a
different scenario from what 2018 actually was, and the page has to say so.

The ordering is the claim here, not the magnitude. The two elections whose CDS
actually ran up came with the larger concurrent global moves -- 2022 (CDS
1.26x) with the Fed's broad-EM dollar index +6.9% and the S&P 500 -25.0%, and
2018 (1.76x) with +3.6% and +11.9% -- while the two quiet ones came with
essentially no dollar move at all: 2010 (1.04x) at -0.2% and 2014 (1.19x) at
+2.4%. Read against the crises, where the same leg carries dxy_em +17.6%
(GFC), +13.8% (2015-16) and +8.7% (COVID), an election's CDS run-up is the
part of the story that is least separable from the world's.

DATA CAVEATS THAT CHANGE A NUMBER
---------------------------------
None as of 2026-09-08. There were two, and both were properties of the old
source rather than of any episode -- which is why `caveat` and `flat_runs`
stay in the payload even though nothing populates them today: the next channel
to be filled in gets the same treatment, and an empty list is the measurement
that there is nothing to declare.

Both went away when the CDS series moved from manual investing.com exports to
a Bloomberg export (see domain/db/brasil/bloomberg/cmb_risco_pais.py for the
full comparison). Worth keeping in view, because each had moved a headline:

* The GFC episode's own base month was ONE FROZEN QUOTE, 121.65 repeated
  across 113 observations, so its 3.28x was measured off a stale number and
  the module hedged it as "somewhere between 3.28x and 2.16x". The real
  answer is 3.07x -- near the top of that range, not the middle of it.
* December 2015 was missing entirely (2 to 31 December), inside the 2015-16
  episode, so that month's "close" was 1 December's print of 436 bps. The
  month actually closed at 495.

`flat_runs` now returns an empty list on the whole 2001-2026 series at the
20-observation threshold: the longest repeated stretch in the Bloomberg data
is 3 days.

Consumed by ridge_deviation_model.build_dashboard_payload(), which attaches the
result as payload["exog_scenarios"]; the FX Model tab renders it as the "Base
scenarios for the exogenous channels" fold above Fit diagnostics.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from analytics.brasil.exchange_rate.models.ppp_equilibrium import _monthly_series, _read_table

# Brazilian general elections: first round is the first Sunday of October, the
# runoff the last Sunday. 2002 and 2006 were added on 2026-09-08, when the CDS
# series moved from investing.com (which started 2007-12) to a Bloomberg export
# starting 2001-10 -- the comment that used to sit here said 2006 had "no data
# to measure", which was true of the old source and is not true of this one.
# 2002 is the reason the addition mattered rather than being tidy: it is the
# largest episode in the library, election or crisis.
_ELECTIONS: dict[int, tuple[str, str]] = {
    2002: ("2002-10-06", "2002-10-27"),
    2006: ("2006-10-01", "2006-10-29"),
    2010: ("2010-10-03", "2010-10-31"),
    2014: ("2014-10-05", "2014-10-26"),
    2018: ("2018-10-07", "2018-10-28"),
    2022: ("2022-10-02", "2022-10-30"),
    2026: ("2026-10-04", "2026-10-25"),
}

_HORIZON = 12  # months in the forecast card's box grid

# Crisis windows are DECLARED, not detected. A peak-finder would date them
# from the same series and then be validated against the same series; these
# three are the episodes that were asked for, and the base month is the last
# monthly close before that episode's run-up began.
#
# Only the START is declared. The END is not a judgement at all: every window
# runs _HORIZON months from its base, exactly like the elections, because the
# library needs ONE ruler for two kinds of episode -- so a window closing
# never means the episode resolved. Two of these three end on or near their
# own peak, and the tab says so, derived from the measurement.
_CDS_CRISES: list[dict] = [
    {
        "id": "gfc_2008",
        "label": "Global financial crisis",
        "base_month": "2008-08",
        "note": "Lehman failed on 15 September 2008. The spread tripled in six monthly "
                "closes and gave almost all of it back inside the same twelve months, "
                "which is why its multiple at month 12 is close to 1.0x.",
    },
    {
        "id": "fiscal_2015",
        "label": "Fiscal crisis and downgrade (2015-16)",
        "base_month": "2014-09",
        "note": "The slowest of the three and the only one that is mostly domestic: twelve "
                "monthly closes of near-continuous widening into the September 2015 loss of "
                "investment grade, ending at its own peak rather than recovering inside the "
                "window.",
    },
    {
        "id": "covid_2020",
        "label": "COVID-19",
        "base_month": "2020-01",
        "note": "The fastest of the three: nearly all of the move landed in two monthly "
                "closes, and it is the slowest recovery of the three despite being the "
                "quickest shock, still well above its base a year on.",
    },
]

# Per-channel scenario specs. `fiscal` is built; the other four are declared
# with `pending` so the tab renders the fold and says what is coming rather
# than hiding the channel and leaving the reader to wonder whether it was
# forgotten. Filling one in is: source the series, pick the episodes, measure.
_CHANNEL_SPECS: dict[str, dict] = {
    "fiscal": {
        "label": "Fiscal risk (5y sovereign CDS, USD)",
        "unit": "bps",
        # Reader-facing, and it has to stay that way: this string is printed in
        # the fold's footer. The table it comes from is named in this module's
        # docstring, which is where an identifier belongs. The guard is
        # tests/test_exog_scenarios_js.js §8, which caught the first version of
        # this line printing "macro_brasil.cmb_risco_pais" on the page.
        "source": "Bloomberg, daily closing quote for Brazil's 5-year sovereign CDS in USD",
        "is_multiplicative": True,
        # Prosa de tela: entidades HTML, nao ASCII. A primeira versao usava
        # "--" e saiu literal na pagina.
        "scale_evidence": "<b>Why multiplying.</b> Split this channel's history into four bands by "
                          "level, and the average monthly move runs 15, 20, 25 and 129 bps as the "
                          "level rises &mdash; but 12.3%, 12.2%, 11.3% and 14.2% of the level "
                          "itself, which barely moves. So the move is proportional: an episode that "
                          "doubled a spread of 120 is a doubling, not a 120-point rise, and it is "
                          "re-anchored on today's level by multiplying.",
    },
    "dxy_em": {"label": "EM dollar index (Fed Broad-EM)", "unit": "index", "pending": True},
    "carry_vol": {"label": "Carry / FX vol", "unit": "ratio", "pending": True},
    "sp500": {"label": "S&P 500", "unit": "index", "pending": True},
    "icbr_usd": {"label": "Commodity index (IC-Br, USD)", "unit": "index", "pending": True},
}


def _last_at(daily: pd.Series, when: pd.Timestamp) -> tuple[pd.Timestamp | None, float | None]:
    """Last daily observation at or before `when` -- the reading someone had on
    the day itself, never an interpolation onto a date the market was shut."""
    sub = daily[daily.index <= when]
    if not len(sub):
        return None, None
    return sub.index[-1], float(sub.iloc[-1])


def _flat_runs(daily: pd.Series, min_len: int = 20) -> list[dict]:
    """Stretches where the source repeats one value. Reported rather than
    cleaned: a frozen quote is real in the file, and the reader has to know
    when an episode's base level is one of them."""
    grp = (daily != daily.shift()).cumsum()
    out = []
    for _, run in daily.groupby(grp):
        if len(run) >= min_len:
            out.append({
                "value": round(float(run.iloc[0]), 2),
                "n": int(len(run)),
                "start": run.index[0].strftime("%Y-%m-%d"),
                "end": run.index[-1].strftime("%Y-%m-%d"),
            })
    return out


def _measure(monthly: pd.Series, daily: pd.Series, base_month: pd.Timestamp,
             concurrent: dict[str, pd.Series]) -> dict:
    """The four rules from the module docstring, applied to one 13-month window.

    Returns {} when the base month itself has no reading -- the caller drops
    the episode rather than shifting the base, which would silently redefine
    what was measured.
    """
    idx = pd.date_range(base_month, periods=_HORIZON + 1, freq="MS")
    full = monthly.reindex(idx)
    if pd.isna(full.iloc[0]) or full.iloc[0] == 0:
        return {}
    base = float(full.iloc[0])

    # An in-progress episode (2026) is legitimately short. None past the end
    # of the data, never the last value carried forward: a flat tail on this
    # chart reads as "the CDS stopped moving", which is a measurement.
    levels = [None if pd.isna(v) else round(float(v), 2) for v in full.values]
    path = [None if pd.isna(v) else round(float(v / base), 4) for v in full.values]

    seg = full.dropna()
    peak_month, peak = seg.idxmax(), float(seg.max())
    out = {
        "base_month": base_month.strftime("%Y-%m"),
        "base": round(base, 2),
        "peak_month": peak_month.strftime("%Y-%m"),
        "peak": round(peak, 2),
        "peak_x": round(peak / base, 3),
        "months_to_peak": int((peak_month.year - base_month.year) * 12
                              + (peak_month.month - base_month.month)),
        "end_month": seg.index[-1].strftime("%Y-%m"),
        "end": round(float(seg.iloc[-1]), 2),
        "end_x": round(float(seg.iloc[-1]) / base, 3),
        "months_observed": int(len(seg) - 1),
        "complete": bool(len(seg) == _HORIZON + 1),
        "levels": levels,
        "path": path,
    }

    # Daily spike inside the same window: what the market actually printed,
    # which a monthly path cannot represent and must not be confused with.
    win_end = seg.index[-1] + pd.offsets.MonthEnd(0)
    dseg = daily[(daily.index >= base_month) & (daily.index <= win_end)]
    if len(dseg):
        out["spike"] = {
            "value": round(float(dseg.max()), 2),
            "date": dseg.idxmax().strftime("%Y-%m-%d"),
            "x": round(float(dseg.max()) / base, 3),
        }

    # Other channels of the same regression over BASE -> PEAK, not base ->
    # window end: the question this answers is "was the run-up Brazil or the
    # world", so it has to span the run-up. Measured to the window end
    # instead, a full 13-month episode reads as a round trip and says the
    # opposite -- COVID came out at dxy_em -0.3% (Jan 2020 to Jan 2021, the
    # dollar already given back) against +8.6% over the leg that actually
    # happened. Log change, so it reads on the same proportional footing as
    # the CDS ratio.
    conc = {}
    for name, ser in concurrent.items():
        a, b = base_month, peak_month
        if a in ser.index and b in ser.index and ser.get(a, 0) > 0 and ser.get(b, 0) > 0:
            conc[name] = round(float(100 * (np.log(ser[b]) - np.log(ser[a]))), 1)
    if conc:
        out["concurrent"] = conc
        out["concurrent_window"] = f"{base_month.strftime('%Y-%m')} to {peak_month.strftime('%Y-%m')}"
    return out


def _distribution(monthly: pd.Series) -> dict:
    """Where a hand-entered path sits against this channel's own history,
    proportionally. Percentiles of the k-month log change, in %, so a reader
    who types a path can be told it is a 1-in-20 twelve months instead of
    being left to feel it out."""
    logs = 100 * np.log(monthly.dropna())
    out = {}
    for k in (1, 3, 6, 12):
        ch = (logs - logs.shift(k)).dropna()
        out[f"{k}m"] = {
            "sd": round(float(ch.std()), 1),
            "p5": round(float(np.percentile(ch, 5)), 1),
            "p50": round(float(np.percentile(ch, 50)), 1),
            "p90": round(float(np.percentile(ch, 90)), 1),
            "p95": round(float(np.percentile(ch, 95)), 1),
            "p99": round(float(np.percentile(ch, 99)), 1),
            "max": round(float(ch.max()), 1),
            "n": int(len(ch)),
        }
    return out


def _election_episodes(monthly: pd.Series, daily: pd.Series,
                       concurrent: dict[str, pd.Series]) -> list[dict]:
    """One episode per election, plus the daily round-to-round leg.

    The base month is twelve months before the month the election falls in, so
    the path's last point IS the election month. Both rounds share that window
    -- see the module docstring -- which is why `inter_round` exists and why
    there is no second episode per year.
    """
    out = []
    for year, (r1, r2) in _ELECTIONS.items():
        r1, r2 = pd.Timestamp(r1), pd.Timestamp(r2)
        event_month = pd.Timestamp(r1.year, r1.month, 1)
        base_month = event_month - pd.DateOffset(months=_HORIZON)
        ep = _measure(monthly, daily, base_month, concurrent)
        if not ep:
            continue

        d1, v1 = _last_at(daily, r1)
        d2, v2 = _last_at(daily, r2)
        # Only a reading dated on or after the round itself is that round's
        # reading. For a future election `_last_at` happily returns today's
        # print, which would read as "the market's level on election day".
        seen_r1 = v1 is not None and d1 is not None and d1 >= r1 - pd.Timedelta(days=7)
        seen_r2 = v2 is not None and d2 is not None and d2 >= r2 - pd.Timedelta(days=7)

        ep.update({
            "id": f"election_{year}",
            "kind": "election",
            "label": f"{year} election",
            "event_month": event_month.strftime("%Y-%m"),
            "round1": r1.strftime("%Y-%m-%d"),
            "round2": r2.strftime("%Y-%m-%d"),
        })
        if seen_r1 and seen_r2:
            seg = daily[(daily.index >= d1) & (daily.index <= d2)]
            ep["inter_round"] = {
                "at_r1": round(v1, 2),
                "at_r2": round(v2, 2),
                "bps": round(v2 - v1, 1),
                "pct": round(100 * (v2 / v1 - 1), 1),
                "peak": round(float(seg.max()), 2) if len(seg) else None,
            }
        elif seen_r1:
            ep["inter_round"] = {"at_r1": round(v1, 2), "at_r2": None, "bps": None,
                                 "pct": None, "peak": None}

        # Post-election relief or continuation: three months past the runoff,
        # only when three months have actually elapsed.
        post = r2 + pd.DateOffset(months=3)
        dp, vp = _last_at(daily, post)
        if seen_r2 and dp is not None and daily.index[-1] >= post:
            ep["post"] = {"months": 3, "value": round(vp, 2), "bps": round(vp - v2, 1),
                          "pct": round(100 * (vp / v2 - 1), 1)}

        if not ep["complete"]:
            ep["note"] = (f"In progress. The window opened in "
                          f"{base_month.strftime('%b %Y')} and runs to the "
                          f"{event_month.strftime('%b %Y')} vote; "
                          f"{ep['months_observed']} of {_HORIZON} months are in.")
        out.append(ep)
    return out


def _crisis_episodes(monthly: pd.Series, daily: pd.Series,
                     concurrent: dict[str, pd.Series], specs: list[dict]) -> list[dict]:
    out = []
    for spec in specs:
        ep = _measure(monthly, daily, pd.Timestamp(spec["base_month"] + "-01"), concurrent)
        if not ep:
            continue
        ep.update({"id": spec["id"], "kind": "crisis", "label": spec["label"],
                   "note": spec["note"]})
        if spec.get("caveat"):
            ep["caveat"] = spec["caveat"]
        out.append(ep)
    return out


def build_fiscal() -> dict:
    """The CDS channel's own scenario library. Reads the daily series straight
    from macro_brasil.cmb_risco_pais rather than through
    ppp_equilibrium.load_data() -- that frame is already resampled to monthly
    and bounded by whichever of PTAX/IPCA/US CPI publishes slowest, and both
    the daily spikes and the round-to-round leg need the daily grid."""
    raw = _read_table("macro_brasil", "cmb_risco_pais")
    raw = raw[raw["name"] == "cds_5y_usd"].copy()
    raw["date"] = pd.to_datetime(raw["date"])
    daily = raw.set_index("date")["value"].astype(float).sort_index()
    daily = daily[~daily.index.duplicated()]
    monthly = daily.resample("MS").last()

    concurrent = {
        "dxy_em": _monthly_series("macro_international", "cmb_dollar_index_em", "dxy_em", "dxy_em"),
        "sp500": _monthly_series("macro_international", "cmb_equity_us", "sp500", "sp500"),
    }

    episodes = (_crisis_episodes(monthly, daily, concurrent, _CDS_CRISES)
                + _election_episodes(monthly, daily, concurrent))

    spec = dict(_CHANNEL_SPECS["fiscal"])
    spec.update({
        "key": "fiscal",
        "last_month": monthly.index[-1].strftime("%Y-%m"),
        "last_value": round(float(monthly.iloc[-1]), 2),
        "last_daily_date": daily.index[-1].strftime("%Y-%m-%d"),
        "history": {
            "months": [d.strftime("%Y-%m") for d in monthly.index],
            "values": [round(float(v), 2) for v in monthly.values],
        },
        "distribution": _distribution(monthly),
        "flat_runs": _flat_runs(daily),
        "episodes": episodes,
    })
    return spec


def build_payload() -> dict:
    """{channel key -> spec}. A channel that raises is dropped with a warning
    rather than taking the fold down with it -- same per-payload degradation
    the rest of this report uses."""
    channels: dict[str, dict] = {}
    builders = {"fiscal": build_fiscal}
    for key, spec in _CHANNEL_SPECS.items():
        if spec.get("pending"):
            channels[key] = {**spec, "key": key, "episodes": []}
            continue
        try:
            channels[key] = builders[key]()
        except Exception as exc:  # noqa: BLE001 -- degrade, never throw
            print(f"  Aviso: cenarios base de '{key}' sem dados — {exc}")
    return {"horizon": _HORIZON, "channels": channels,
            "order": list(_CHANNEL_SPECS.keys())}


if __name__ == "__main__":
    import json

    payload = build_payload()
    f = payload["channels"]["fiscal"]
    print(f"{f['label']}  last {f['last_value']} bps ({f['last_month']})")
    print(f"{len(f['episodes'])} episodes")
    for ep in f["episodes"]:
        print(f"  {ep['kind']:8s} {ep['label']:34s} base {ep['base']:6.1f} ({ep['base_month']})"
              f"  peak {ep['peak']:6.1f} ({ep['peak_month']}) = {ep['peak_x']:.2f}x"
              f" in {ep['months_to_peak']:2d}mo   {'' if ep['complete'] else '[partial]'}")
    print(json.dumps(payload["channels"]["fiscal"]["distribution"], indent=2))
