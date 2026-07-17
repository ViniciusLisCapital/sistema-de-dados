"""
BCB aggregate small-scale model — forward simulation for short-horizon
conditional IPCA scenarios / decomposition.

Scope and simplifications are documented in
analytics/monetary_policy/referencia/MODEL_REPLICATION_PLAN.md. Summary:

- Fixed parameters (posterior mode from Table 1, Dez/2021 box) instead of
  re-estimating via Bayesian MCMC — read from macro_brasil.pm_parametros.
- Output gap (h_t) and neutral rate (r_eq_t) are SEEDED from BCB's own
  disclosed estimates (macro_brasil.pm_hiato_seed), not derived via a Kalman
  filter over PIB/Nuci/desocupacao/Caged. This is an open-loop forward
  simulation from that seed, not a self-correcting nowcast — fine for
  short-horizon conditional scenarios, but it will drift from BCB's own
  re-estimated truth if run far past the seed date without re-anchoring.
- Inflation expectations (pi^e_t,t+4|t) use the actual Focus IPCA-12m survey
  directly, instead of solving the model-consistent expectations equation
  (eq. 5 in the box) — avoids needing a full rational-expectations solver.
- Deferred terms (per the plan doc): CDS risk premium (UIP), IIE-Br
  uncertainty and cyclically-adjusted fiscal result and world output gap
  (all three IS curve terms) are set to zero — their data isn't sourced yet.
- Commodity weights (w_a, w_m, w_e) are not disclosed in the box's Table 1 —
  defaulted to equal weights (1/3 each), documented below.
- Administered prices are explicitly out of scope of this box (BCB uses a
  separate satellite model + specialist projections) — the headline-IPCA
  inertia term uses simulated free-prices inflation as a stand-in for
  administered prices once historical data runs out.
- i^e_{t,t+4|t} (the "expected Selic path over the next 4 quarters" used in
  the IS curve's real-rate gap) is approximated by the current/simulated
  i_t, since we only have a single point-in-time Focus Selic snapshot, not a
  forward curve. This means a Selic shock passes into the output gap at full
  strength every quarter it's held, instead of being partially discounted by
  a forward-looking market that anticipates the shock's eventual reversal.

KNOWN CALIBRATION GAP (checked 2026-07-13): replaying the box's own IRF
experiment (Selic +1pp for 4 quarters, then release to the Taylor rule) through
this engine produces a peak 4-quarter-accumulated pi_livres response of about
-1.5pp around quarter 9 — roughly 4-5x LARGER than the box's own published
result for the full IPCA (-0.33pp at quarter 6, Grafico 2b). Sign and rough
timing are right; magnitude is not. Root cause: the naive i^e proxy above
doesn't anticipate the policy reversal the way BCB's actual model-consistent
expectations would, so it overstates real-rate transmission. This is a direct
consequence of the deliberate decision to skip solving the model-consistent
expectations equation (eq. 5) — treat this engine's magnitudes as
directionally useful, not point-precise, until/unless that's revisited.

Source equations: analytics/monetary_policy/referencia/modelo_agregado.pdf
(Relatorio de Inflacao, Dez/2021, p.73-75).
"""

from __future__ import annotations

from decimal import Decimal

import pandas as pd

from connectors.mysql import MySQLDataRequester

_VINTAGE = "RI_2021T4_agregado"
_EXT_EQ_INFLATION = 2.0  # % a.a. — proxy for pi*ss (long-run US/external equilibrium inflation)
_COMMODITY_WEIGHTS = {"agro": 1 / 3, "metal": 1 / 3, "energia": 1 / 3}  # not disclosed by BCB — equal-weight default


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def _read_table(database: str, table: str) -> pd.DataFrame:
    req = MySQLDataRequester(database, table)
    req.connect()
    df = req.request_data()
    req.close_connection()
    # mysql.connector returns DECIMAL columns as decimal.Decimal — normalize to float
    # so they mix freely with plain python floats in the equations below.
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, Decimal)).any():
            df[col] = df[col].astype(float)
    return df


def load_parameters(vintage: str = _VINTAGE) -> dict[str, float]:
    df = _read_table("macro_brasil", "pm_parametros")
    df = df[df["vintage"] == vintage]
    if df.empty:
        raise ValueError(f"No pm_parametros rows for vintage={vintage!r}")
    return {row.parametro: float(row.moda) for row in df.itertuples()}


def load_seed() -> dict[str, tuple[float, pd.Timestamp]]:
    df = _read_table("macro_brasil", "pm_hiato_seed")
    df["as_of_date"] = pd.to_datetime(df["as_of_date"])
    latest = df.sort_values("as_of_date").groupby("variavel").tail(1)
    return {row.variavel: (float(row.value), row.as_of_date) for row in latest.itertuples()}


def _quarterly(df: pd.DataFrame, value_col: str, how: str) -> pd.Series:
    """Resample a (date, value) frame to quarter-start frequency."""
    s = df.set_index(pd.to_datetime(df["date"]))[value_col].sort_index()
    if how == "last":
        return s.resample("QS").last()
    if how == "mean":
        return s.resample("QS").mean()
    if how == "compound_pct":
        # compound monthly % rates within the quarter into one quarterly % rate
        return s.resample("QS").apply(lambda x: ((1 + x / 100).prod() - 1) * 100)
    raise ValueError(how)


def load_history(quarters_back: int = 32) -> pd.DataFrame:
    """Builds a quarterly-aligned history frame with everything the model needs."""
    ipca = _read_table("macro_brasil", "inflc_agregados")
    ptax = _read_table("macro_brasil", "cmb_ptax")
    ptax = ptax[ptax["name"] == "ptax_venda"]
    dj = _read_table("macro_international", "diferenciais_juros")
    focus = _read_table("macro_brasil", "expc_focus")
    icbr = _read_table("macro_brasil", "comm_icbr")
    meta = _read_table("macro_brasil", "inflc_meta")
    oni = _read_table("macro_international", "clima_oni")

    out = pd.DataFrame()
    out["pi_livres"] = _quarterly(ipca[ipca["name"] == "ipca_livres"], "value", "compound_pct")
    out["pi_ipca"] = _quarterly(ipca[ipca["name"] == "ipca"], "value", "compound_pct")
    out["selic"] = _quarterly(dj[dj["name"] == "selic"], "value", "last")
    out["fed_funds"] = _quarterly(dj[dj["name"] == "fed_funds"], "value", "last")
    out["fx"] = _quarterly(ptax, "value", "mean")
    out["meta_inflacao"] = _quarterly(meta, "value", "last").resample("QS").ffill()
    out["oni"] = _quarterly(oni[oni["name"] == "oni"], "value", "last")

    for label, series_name in [("agro", "icbr_agropecuaria"), ("metal", "icbr_metal"), ("energia", "icbr_energia")]:
        out[f"icbr_{label}"] = _quarterly(icbr[icbr["name"] == series_name], "value", "mean")

    focus_ipca = focus[(focus["indicador"] == "IPCA") & (focus["horizonte"] == "12m")]
    out["focus_ipca_12m"] = _quarterly(focus_ipca, "mediana", "last")

    out = out.ffill().dropna()
    return out.tail(quarters_back)


# ---------------------------------------------------------------------------
# Equations (aggregate model, Dez/2021 box)
# ---------------------------------------------------------------------------

def taylor_rule(coef, i_lag1, i_lag2, r_eq, meta, pi_e) -> float:
    th1, th2, th3 = coef["theta_1"], coef["theta_2"], coef["theta_3"]
    return th1 * i_lag1 + th2 * i_lag2 + (1 - th1 - th2) * (r_eq + meta + th3 * (pi_e - meta))


def uip_delta_e(coef, meta, i_dif, i_dif_lag1) -> tuple[float, float]:
    """Returns (delta_e, fx_gap) — fx_gap = delta_e - delta_e_ppc, the term used lagged-2 in the Phillips curve."""
    delta_e_ppc = (meta - _EXT_EQ_INFLATION) / 4  # quarterly-equivalent long-run PPP depreciation
    delta_e = delta_e_ppc - coef["delta"] * (i_dif - i_dif_lag1)
    return delta_e, delta_e - delta_e_ppc


def climate_term(coef, oni_lags: list[float]) -> float:
    """oni_lags[0] = ONI at lag 0 (current quarter), ... oni_lags[5] = lag 5.

    Difference between a recent 3-quarter average and an older 3-quarter
    average of the same El Nino/La Nina-weighted squared-anomaly construct —
    captures the transitory nature of climate shocks (eq. 1 in the box).
    """
    def shock(oni):
        dummy_el = coef["alpha_5"] if oni >= 0 else 0.0
        dummy_la = coef["alpha_6"] if oni < 0 else 0.0
        return (dummy_el + dummy_la) * oni ** 2

    recent = sum(shock(o) for o in oni_lags[0:3]) / 3
    older = sum(shock(o) for o in oni_lags[3:6]) / 3
    return recent - older


def commodity_deviation(coef, icbr_qoq: dict[str, float], meta_q: float) -> float:
    """Weighted deviation of commodity price inflation from the quarterly-equivalent target."""
    dev = {k: v - meta_q for k, v in icbr_qoq.items()}
    return sum(_COMMODITY_WEIGHTS[k] * dev[k] for k in dev)


def is_curve(coef, h_lag1, r_hat) -> float:
    """Output gap. Fiscal / uncertainty / world-gap terms deferred (set to 0) — see module docstring."""
    return coef["beta_1"] * h_lag1 - coef["beta_2"] * r_hat


def _annual_to_quarterly(rate_pct: float) -> float:
    """Converts a 12-month/annual rate to its quarterly-equivalent (compounding)."""
    return ((1 + rate_pct / 100) ** 0.25 - 1) * 100


def phillips_livres(coef, pi_livres_lag1, pi_ipca_avg4, pi_focus_12m, commodity_dev, fx_gap_lag2, h_t, climate) -> dict[str, float]:
    """pi_livres_lag1/pi_ipca_avg4 are RAW quarterly rates (not annualized) — matches
    how the box's own IRF charts report results ("acumulada em quatro trimestres",
    i.e. a rolling sum of quarterly rates, not an average of annualized rates).
    pi_focus_12m is Focus's 12-month/annual survey figure — converted to its
    quarterly-equivalent here so it's on the same basis as the other terms.

    Returns the per-term decomposition (Grafico 10 style) plus "total".
    """
    a1l, a1i = coef["alpha_1L"], coef["alpha_1I"]
    pi_e_quarterly = _annual_to_quarterly(pi_focus_12m)
    terms = {
        "inercia_propria": a1l * pi_livres_lag1,
        "inercia_ipca":    a1i * pi_ipca_avg4,
        "expectativas":    (1 - a1l - a1i) * pi_e_quarterly,
        "commodities":     coef["alpha_2"] * commodity_dev,
        "cambio":          coef["alpha_3"] * fx_gap_lag2,
        "hiato":           coef["alpha_4"] * h_t,
        "clima":           climate,
    }
    terms["total"] = sum(terms.values())
    return terms


# ---------------------------------------------------------------------------
# Simulation
# ---------------------------------------------------------------------------

def simulate(n_quarters: int, scenario: dict | None = None) -> pd.DataFrame:
    """Forward-simulates the aggregate model for n_quarters from the current seed/history.

    scenario (all optional, default = hold last observed value flat):
      selic_override:    {quarter_index: value}  — overrides the Taylor rule for a given quarter (policy shocks)
      focus_ipca_12m:    list[float] length n_quarters
      selic_expectation: list[float] length n_quarters — i^e_{t,t+4|t} proxy used in r_hat.
                          Default (if omitted): the just-determined i_t itself — a naive proxy that
                          doesn't discount for the market anticipating a shock's reversal. See
                          simulate_consistent() for a self-consistent alternative.
      fed_funds:      list[float] length n_quarters
      icbr_shock:     {"agro"|"metal"|"energia": list[float] length n_quarters}  — % QoQ change, additive to baseline 0
      oni:            list[float] length n_quarters — climate shock path (default: 0, no anomaly)
    """
    scenario = scenario or {}
    coef = load_parameters()
    seed = load_seed()
    hist = load_history()

    h = seed["output_gap"][0]
    r_eq = seed["neutral_rate"][0]

    i_lag1, i_lag2 = hist["selic"].iloc[-1], hist["selic"].iloc[-2]
    pi_livres_lag1 = hist["pi_livres"].iloc[-1]
    pi_ipca_hist = list(hist["pi_ipca"].iloc[-4:])
    fed_funds_lag1 = hist["fed_funds"].iloc[-1]
    i_dif_lag1 = hist["selic"].iloc[-1] - fed_funds_lag1
    fx_gap_history = [0.0, 0.0]  # last 2 quarters' fx_gap, needed for the lag-2 term
    oni_history = list(hist["oni"].iloc[-6:])
    meta_last = hist["meta_inflacao"].iloc[-1]
    focus_ipca_last = hist["focus_ipca_12m"].iloc[-1]

    rows = []
    for q in range(n_quarters):
        meta = meta_last  # target assumed unchanged over a short horizon
        pi_e = scenario.get("focus_ipca_12m", [focus_ipca_last] * n_quarters)[q]
        fed_funds = scenario.get("fed_funds", [fed_funds_lag1] * n_quarters)[q]
        oni_now = scenario.get("oni", [0.0] * n_quarters)[q]

        if q in scenario.get("selic_override", {}):
            i_t = scenario["selic_override"][q]
        else:
            i_t = taylor_rule(coef, i_lag1, i_lag2, r_eq, meta, pi_e)

        i_dif = i_t - fed_funds
        delta_e, fx_gap = uip_delta_e(coef, meta, i_dif, i_dif_lag1)

        # i^e_{t,t+4|t} (expected Selic path): naive default is the just-determined i_t
        # itself, which doesn't discount for the market anticipating a shock's reversal.
        # simulate_consistent() overrides this with a self-consistent path instead.
        i_e = scenario.get("selic_expectation", [None] * n_quarters)[q]
        r_hat = (i_e if i_e is not None else i_t) - pi_e - r_eq
        h = is_curve(coef, h, r_hat)

        # default (no shock) path: commodity prices rising exactly at the quarterly-equivalent
        # target, i.e. zero deviation — NOT 0% QoQ growth, which would itself be a (disinflationary) shock
        icbr_shock = scenario.get("icbr_shock", {})
        icbr_qoq = {k: icbr_shock.get(k, [meta / 4] * n_quarters)[q] for k in _COMMODITY_WEIGHTS}
        commodity_dev = commodity_deviation(coef, icbr_qoq, meta / 4)

        oni_history = [oni_now] + oni_history[:5]
        climate = climate_term(coef, oni_history)

        fx_gap_history = [fx_gap] + fx_gap_history[:1]
        fx_gap_lag2 = fx_gap_history[1] if len(fx_gap_history) > 1 else 0.0

        pi_ipca_avg4 = sum(pi_ipca_hist) / 4
        decomp = phillips_livres(coef, pi_livres_lag1, pi_ipca_avg4, pi_e, commodity_dev, fx_gap_lag2, h, climate)
        pi_livres = decomp["total"]

        rows.append({
            "quarter": q + 1, "selic": i_t, "fx_delta_pct": delta_e, "output_gap": h,
            "pi_livres_qoq": pi_livres, "fx_gap": fx_gap,
            **{f"decomp_{k}": v for k, v in decomp.items() if k != "total"},
        })

        i_lag2, i_lag1 = i_lag1, i_t
        pi_livres_lag1 = pi_livres
        pi_ipca_hist = [pi_livres] + pi_ipca_hist[:3]  # administered prices out of scope — see module docstring
        i_dif_lag1 = i_dif
        fed_funds_lag1 = fed_funds

    return pd.DataFrame(rows)


def _pad(values: list, length: int) -> list:
    """Extends a scenario list to `length` by repeating its last value (for the lookahead buffer)."""
    if len(values) >= length:
        return values[:length]
    return values + [values[-1]] * (length - len(values))


def simulate_forward_pi_e(n_quarters: int, scenario: dict | None = None) -> pd.DataFrame:
    """simulate(), but pi_e (inflation expectations) comes from the model's OWN
    4-quarter-forward inflation path instead of being held flat at the latest Focus
    print.

    This is deliberately a single refinement pass, NOT the iterated fixed point
    (simulate_consistent, tried and removed — see git history / conversation): a
    bootstrap pass with simulate()'s naive flat-Focus default, then one re-simulation
    using that bootstrap's own accumulated pi_livres over [t, t+3] (annual-equivalent,
    same convention as Focus's 12-month figure) as pi_e. It can't diverge, because
    there's no loop — but it's correspondingly a smaller fix than a true
    rational-expectations solution would be: i^e (the expected Selic path used in
    r_hat) is untouched, still the naive i_t proxy, so part of the ~4-5x IRF
    overstatement documented in simulate()'s docstring is expected to remain.
    """
    scenario = dict(scenario or {})
    buffer = 4
    total_q = n_quarters + buffer

    for key in ("focus_ipca_12m", "fed_funds", "oni"):
        if key in scenario:
            scenario[key] = _pad(scenario[key], total_q)
    if "icbr_shock" in scenario:
        scenario["icbr_shock"] = {k: _pad(v, total_q) for k, v in scenario["icbr_shock"].items()}

    bootstrap = simulate(total_q, scenario)

    pi_e_forward = []
    for t in range(total_q):
        window = bootstrap["pi_livres_qoq"].iloc[t:t + 4]
        pi_e_forward.append(window.sum() if len(window) == 4 else bootstrap["pi_livres_qoq"].iloc[t:].sum())

    next_scenario = {**scenario, "focus_ipca_12m": pi_e_forward}
    result = simulate(total_q, next_scenario)
    return result.iloc[:n_quarters].reset_index(drop=True)


if __name__ == "__main__":
    result = simulate_forward_pi_e(n_quarters=8)
    print(result.round(3).to_string(index=False))
