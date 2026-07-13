"""
Snapshot de dados cambiais para o agente de análise (cambio-analyst).

Reaproveita os loaders de generate_report.py (mesmo pacote, mesmas tabelas de
macro_brasil/macro_international) e resume cada série em último valor +
variações em janelas de calendário padrão. Sem interpretação — conectar os
dados a conceitos (UIP, carry trade, BOP etc.) é responsabilidade do agente
que consome este snapshot.

Uso:
    uv run python -c "from analytics.cambio.agent_data import get_fx_snapshot; import json; print(json.dumps(get_fx_snapshot(), ensure_ascii=False, default=str))"
"""

import json
from datetime import datetime

import pandas as pd

from analytics.cambio.generate_report import (
    _load_bcb_positioning,
    _load_bop,
    _load_cot_fx,
    _load_diferenciais,
    _load_fluxo,
    _load_ptax,
    _load_reer,
    _load_termos,
)

# Janelas em dias corridos (não em nº de observações) — necessário porque os
# grupos têm frequências diferentes (diária/semanal/mensal/variada).
_WINDOWS_DAYS = {"1m": 30, "3m": 90, "12m": 365}

# Gap máximo esperado entre a última observação e hoje antes de marcar como
# "stale" — aproximado pela frequência de publicação de cada grupo.
_EXPECTED_GAP_DAYS = {
    "ptax": 10,             # diária (dias úteis)
    "diferenciais": 45,    # mensal
    "reer": 60,            # mensal (BIS), publicação com defasagem
    "cot_fx": 14,           # semanal (CFTC, terças)
    "fluxo": 45,            # mensal
    "bop": 45,              # mensal
    "termos": 90,           # mensal, mas periodicidade "variada" (ver CAMBIO.md)
    "bcb_reserves": 15,     # diária (reserves_liquidity_daily)
    "bcb_gold": 45,         # mensal
    "bcb_swap": 45,         # mensal
    "bcb_interventions": 120,  # evento — BCB pode passar meses sem intervir; gap grande não é staleness
}


def _summarize_series(dates: list, values: list | None) -> dict | None:
    """Resume uma série (dates/values paralelos) em último valor + deltas."""
    if values is None:
        return None
    pairs = sorted(
        (pd.Timestamp(d), v) for d, v in zip(dates, values) if v is not None
    )
    if not pairs:
        return None
    s = pd.Series([v for _, v in pairs], index=[d for d, _ in pairs])

    latest_date = s.index[-1]
    latest_value = s.iloc[-1]
    deltas = {}
    for label, days in _WINDOWS_DAYS.items():
        prior = s.loc[: latest_date - pd.Timedelta(days=days)]
        deltas[label] = float(latest_value - prior.iloc[-1]) if not prior.empty else None

    return {
        "latest_date": latest_date.strftime("%Y-%m-%d"),
        "latest_value": float(latest_value),
        "deltas": deltas,
        "n_obs": int(len(s)),
    }


def _summarize_group(group_key: str, group: dict) -> dict:
    """Resume um dict no formato {"dates": [...], "serie_a": [...], ...}."""
    dates = group.get("dates", [])
    series = {
        name: _summarize_series(dates, values)
        for name, values in group.items()
        if name != "dates"
    }

    latest_dates = [pd.Timestamp(s["latest_date"]) for s in series.values() if s]
    if latest_dates:
        gap_days = (pd.Timestamp(datetime.now().date()) - max(latest_dates)).days
        stale = gap_days > _EXPECTED_GAP_DAYS.get(group_key, 45)
    else:
        gap_days = None
        stale = True

    return {"series": series, "data_gap_days": gap_days, "stale": stale}


def get_fx_snapshot() -> dict:
    """Snapshot cambial data-only: último valor + variações (1m/3m/12m) por
    série, agrupado como em generate_report.py (ptax, diferenciais, reer,
    cot_fx, bcb_positioning, fluxo, bop, termos).

    `bcb_positioning` é aninhado (reserves/gold/swap/interventions) porque
    `cmb_reservas_bc` mistura frequências — ver docstring de
    `_load_bcb_positioning` em generate_report.py.
    """
    flat_groups = {
        "ptax": _load_ptax(),
        "diferenciais": _load_diferenciais(),
        "reer": _load_reer(),
        "cot_fx": _load_cot_fx(),
        "fluxo": _load_fluxo(),
        "bop": _load_bop(),
        "termos": _load_termos(),
    }
    bcb = _load_bcb_positioning()
    return {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        **{key: _summarize_group(key, group) for key, group in flat_groups.items()},
        "bcb_positioning": {
            "reserves":      _summarize_group("bcb_reserves", bcb.get("reserves", {})),
            "gold":          _summarize_group("bcb_gold", bcb.get("gold", {})),
            "swap":          _summarize_group("bcb_swap", bcb.get("swap", {})),
            "interventions": _summarize_group("bcb_interventions", bcb.get("interventions", {})),
        },
    }


if __name__ == "__main__":
    import sys

    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(get_fx_snapshot(), ensure_ascii=False, default=str))
