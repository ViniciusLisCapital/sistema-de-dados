"""
Gerador do relatório HTML de fundamentos cambiais.

Lê tabelas de macro_brasil, macro_international e macro_analytics, injeta os
dados no template report.html e salva um único arquivo HTML autocontido em
reports/cambio_latest.html.

Uso:
    uv run python -c "from analytics.cambio.generate_report import run; run()"
"""

import json
from datetime import datetime
from pathlib import Path

import pandas as pd

from connectors.mysql import MySQLDataRequester

_TEMPLATE = Path(__file__).parent / "report.html"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _dates(index: pd.DatetimeIndex) -> list:
    return [d.strftime("%Y-%m-%d") for d in index]


def _to_list(s: pd.Series) -> list:
    return [None if pd.isna(v) else float(v) for v in s]


def _col(wide: pd.DataFrame, name: str):
    if name not in wide.columns:
        return None
    return _to_list(wide[name])


def _fetch(database: str, table: str) -> pd.DataFrame | None:
    req = MySQLDataRequester(database, table)
    req.connect()
    if req.connection is None:
        print(f"  Aviso: sem conexão para {database}.{table}")
        return None
    df = req.request_data()
    req.close_connection()
    if df is None or df.empty:
        print(f"  Aviso: {database}.{table} vazia ou sem dados")
        return None
    df["date"] = pd.to_datetime(df["date"])
    return df


def _pivot(database: str, table: str) -> pd.DataFrame | None:
    """Lê tabela com schema (date, name, value) e pivota para wide."""
    df = _fetch(database, table)
    if df is None:
        return None
    df["value"] = df["value"].astype(float)
    return df.pivot(index="date", columns="name", values="value").sort_index()


# ── Data loaders ──────────────────────────────────────────────────────────────

def _load_diferenciais() -> dict:
    try:
        wide = _pivot("macro_analytics", "diferenciais_juros")
        if wide is None:
            return {}
        return {
            "dates":               _dates(wide.index),
            "selic":               _col(wide, "selic"),
            "fed_funds":           _col(wide, "fed_funds"),
            "ipca_12m":            _col(wide, "ipca_12m"),
            "cpi_12m_us":          _col(wide, "cpi_12m_us"),
            "diferencial_nominal": _col(wide, "diferencial_nominal"),
            "real_br_ex_post":     _col(wide, "real_br_ex_post"),
            "real_us_ex_post":     _col(wide, "real_us_ex_post"),
            "diferencial_real":    _col(wide, "diferencial_real"),
        }
    except Exception as exc:
        print(f"  Aviso: erro em diferenciais_juros — {exc}")
        return {}


def _load_reer() -> dict:
    try:
        df = _fetch("macro_international", "reer")
        if df is None:
            return {}
        df["value"] = df["value"].astype(float)
        rb = df[df["reer_type"] == "real_broad"].copy()
        wide = rb.pivot(index="date", columns="country_code", values="value").sort_index()
        return {
            "dates": _dates(wide.index),
            "BR":    _col(wide, "BR"),
            "MX":    _col(wide, "MX"),
            "CL":    _col(wide, "CL"),
            "CO":    _col(wide, "CO"),
        }
    except Exception as exc:
        print(f"  Aviso: erro em reer — {exc}")
        return {}


def _load_cot_fx() -> dict:
    try:
        df = _fetch("macro_international", "cot_fx")
        if df is None:
            return {}
        df["value"] = df["value"].astype(float)
        brl = df[df["currency"] == "BRL"].copy()
        wide = brl.pivot(index="date", columns="name", values="value").sort_index()
        return {
            "dates":         _dates(wide.index),
            "lev_net":       _col(wide, "lev_net"),
            "lev_long":      _col(wide, "lev_long"),
            "lev_short":     _col(wide, "lev_short"),
            "open_interest": _col(wide, "open_interest"),
        }
    except Exception as exc:
        print(f"  Aviso: erro em cot_fx — {exc}")
        return {}


def _load_reservas() -> dict:
    try:
        wide = _pivot("macro_brasil", "reservas")
        if wide is None:
            return {}
        return {
            "dates":                  _dates(wide.index),
            "reservas_liquidez_usd":  _col(wide, "reservas_liquidez_usd"),
        }
    except Exception as exc:
        print(f"  Aviso: erro em reservas — {exc}")
        return {}


def _load_fluxo() -> dict:
    try:
        wide = _pivot("macro_brasil", "fluxo_cambial")
        if wide is None:
            return {}
        if "comercial_entrada" in wide.columns and "comercial_saida" in wide.columns:
            wide["comercial_saldo"] = wide["comercial_entrada"] - wide["comercial_saida"]
        return {
            "dates":            _dates(wide.index),
            "total_saldo":      _col(wide, "total_saldo"),
            "comercial_saldo":  _col(wide, "comercial_saldo"),
            "financeiro_saldo": _col(wide, "financeiro_saldo"),
        }
    except Exception as exc:
        print(f"  Aviso: erro em fluxo_cambial — {exc}")
        return {}


def _load_bop() -> dict:
    try:
        wide = _pivot("macro_brasil", "balanco_pagamentos")
        if wide is None:
            return {}
        return {
            "dates":                       _dates(wide.index),
            "conta_corrente":              _col(wide, "conta_corrente"),
            "investimento_direto_liquido": _col(wide, "investimento_direto_liquido"),
            "conta_financeira":            _col(wide, "conta_financeira"),
            "investimento_carteira":       _col(wide, "investimento_carteira"),
        }
    except Exception as exc:
        print(f"  Aviso: erro em balanco_pagamentos — {exc}")
        return {}


def _load_termos() -> dict:
    try:
        wide = _pivot("macro_brasil", "termos_de_troca")
        if wide is None:
            return {}
        return {
            "dates":               _dates(wide.index),
            "termos_de_troca_a":   _col(wide, "termos_de_troca_a"),
            "termos_de_troca_b":   _col(wide, "termos_de_troca_b"),
        }
    except Exception as exc:
        print(f"  Aviso: erro em termos_de_troca — {exc}")
        return {}


# ── Entry point ───────────────────────────────────────────────────────────────

def run(output: str = "reports/cambio_latest.html") -> None:
    """Gera o relatório HTML de fundamentos cambiais.

    Lê todas as tabelas de macro_cambio, injeta os dados no template
    report.html e salva um único arquivo HTML autocontido.

    Args:
        output: caminho de saída. Default "reports/cambio_latest.html".
    """
    print("Carregando dados de macro_brasil / macro_international / macro_analytics...")
    report_data = {
        "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "diferenciais":  _load_diferenciais(),
        "reer":          _load_reer(),
        "cot_fx":        _load_cot_fx(),
        "reservas":      _load_reservas(),
        "fluxo":         _load_fluxo(),
        "bop":           _load_bop(),
        "termos":        _load_termos(),
    }

    template = _TEMPLATE.read_text(encoding="utf-8")
    payload = json.dumps(report_data, ensure_ascii=False, default=str)
    html = template.replace("/*REPORT_DATA*/", f"const REPORT_DATA = {payload};")

    out = Path(output)
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"Relatório salvo: {out.resolve()}")
