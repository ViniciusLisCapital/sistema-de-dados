"""
Gerador do relatório HTML de fundamentos cambiais.

Lê tabelas de macro_brasil e macro_international, injeta os dados no template
report.html e salva um único arquivo HTML autocontido em reports/fx_report.html.

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
        wide = _pivot("macro_international", "diferenciais_juros")
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
        df = _fetch("macro_international", "cmb_reer")
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
        print(f"  Aviso: erro em cmb_reer — {exc}")
        return {}


def _load_cot_fx() -> dict:
    try:
        df = _fetch("macro_international", "cmb_cot_fx")
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
        print(f"  Aviso: erro em cmb_cot_fx — {exc}")
        return {}


def _load_bcb_positioning() -> dict:
    """Reservas internacionais, posição de câmbio (BCB/bancos) e intervenções.

    Alimenta a aba "BCB Positioning". `cmb_reservas_bc` mistura frequências
    (mensal para reservas/swap, diária para reservas_liquidity/intervenções)
    numa única tabela — pivotar tudo junto criaria um índice de datas comum
    onde a maioria das linhas mensais ficaria cercada de nulls (a série
    "quebraria" visualmente com connectgaps=false). Em vez disso, cada
    subgrupo abaixo pivota só suas próprias séries e carrega seu próprio
    eixo "dates".
    """
    try:
        df = _fetch("macro_brasil", "cmb_reservas_bc")
        if df is None:
            return {}
        df["value"] = df["value"].astype(float)

        def _subgroup(names: list) -> dict:
            sub = df[df["name"].isin(names)]
            if sub.empty:
                return {}
            wide = sub.pivot(index="date", columns="name", values="value").sort_index()
            return {"dates": _dates(wide.index), **{n: _col(wide, n) for n in names}}

        return {
            "reserves": _subgroup(["reserves_liquidity_daily", "reserves_total_monthly"]),
            "gold":     _subgroup(["reserves_gold_usd"]),
            "swap":     _subgroup(["bcb_swap_cambial_position", "bank_fx_spot_position"]),
            "interventions": _subgroup([
                "bcb_intervention_spot",
                "bcb_intervention_forwards",
                "bcb_intervention_fx_loans_repos",
                "bcb_intervention_repo_lines",
            ]),
        }
    except Exception as exc:
        print(f"  Aviso: erro em cmb_reservas_bc — {exc}")
        return {}


def _load_fluxo() -> dict:
    try:
        wide = _pivot("macro_brasil", "cmb_fluxo_cambial")
        if wide is None:
            return {}
        if "comercial_entrada" in wide.columns and "comercial_saida" in wide.columns:
            wide["comercial_saldo"] = wide["comercial_entrada"] - wide["comercial_saida"]
        return {
            "dates":             _dates(wide.index),
            "total_saldo":       _col(wide, "total_saldo"),
            "total_entrada":     _col(wide, "total_entrada"),
            "total_saida":       _col(wide, "total_saida"),
            "comercial_saldo":   _col(wide, "comercial_saldo"),
            "comercial_entrada": _col(wide, "comercial_entrada"),
            "comercial_saida":   _col(wide, "comercial_saida"),
            "financeiro_saldo":  _col(wide, "financeiro_saldo"),
        }
    except Exception as exc:
        print(f"  Aviso: erro em cmb_fluxo_cambial — {exc}")
        return {}


def _load_bop() -> dict:
    """Balanço de Pagamentos — séries brutas (SGS) + agregados derivados.

    Os agregados abaixo foram cross-checados contra o quadro condensado
    oficial do BCB ("Financiamento Externo") em 5 meses (Jan-Mai/2026) —
    ver docstring de domain/db/brasil/bcb/cmb_balanco_pagmt.py para as
    fórmulas e a validação.
    """
    try:
        wide = _pivot("macro_brasil", "cmb_balanco_pagmt")
        if wide is None:
            return {}

        out = {"dates": _dates(wide.index)}
        for name in [
            "conta_corrente", "balanca_comercial_servicos", "exportacao_bens", "importacao_bens",
            "servicos", "viagens", "transportes", "aluguel_equipamentos",
            "renda_primaria", "remuneracao_empregados", "renda_secundaria", "conta_capital",
            "conta_financeira", "idp_exterior", "ide_saidas", "investimento_direto_liquido", "idp_ingressos",
            "portfolio_ativos", "portfolio_passivos", "acoes_passivos", "fundos_passivos",
            "titulos_dom", "titulos_externo_cp", "titulos_externo_lp",
            "derivativos", "ativos_reserva", "erros_omissoes",
        ]:
            out[name] = _col(wide, name)

        # Agregados validados contra o quadro oficial "Financiamento Externo"
        out["demais_servicos"] = _to_list(
            wide["servicos"] - wide["viagens"] - wide["transportes"] - wide["aluguel_equipamentos"]
        )
        out["juros"] = _to_list(
            wide["juros_intercompanhia"] + wide["juros_carteira_externo"]
            + wide["juros_carteira_domestico"] + wide["juros_outros_investimentos"] + wide["renda_reservas"]
        )
        out["lucros_dividendos"] = _to_list(
            wide["lucros_remetidos"] + wide["lucros_reinvestidos"] + wide["lucros_dividendos_carteira"]
        )
        out["investimentos_ativos"] = _to_list(
            wide["idp_exterior"] + wide["portfolio_ativos"] + wide["outros_inv_ativos"]
        )
        out["investimentos_passivos"] = _to_list(
            wide["investimento_direto_liquido"] + wide["portfolio_passivos"] + wide["outros_inv_passivos"]
        )
        out["acoes_totais"] = _to_list(wide["acoes_passivos"] + wide["fundos_passivos"])
        out["emprestimos_titulos_lp_externo"] = _to_list(
            wide["titulos_externo_lp"] + wide["emprestimos_lp_passivos"]
        )
        out["emprestimos_titulos_cp_externo"] = _to_list(
            wide["titulos_externo_cp"] + wide["emprestimos_cp_passivos"]
        )
        out["demais_passivos"] = _to_list(
            wide["portfolio_passivos"] + wide["outros_inv_passivos"]
            - wide["acoes_passivos"] - wide["fundos_passivos"] - wide["titulos_dom"]
            - wide["titulos_externo_lp"] - wide["emprestimos_lp_passivos"]
            - wide["titulos_externo_cp"] - wide["emprestimos_cp_passivos"]
        )
        return out
    except Exception as exc:
        print(f"  Aviso: erro em cmb_balanco_pagmt — {exc}")
        return {}


def _load_ptax() -> dict:
    try:
        wide = _pivot("macro_brasil", "cmb_ptax")
        if wide is None:
            return {}
        vol_total = None
        if "fx_interbank_vol_t1" in wide.columns and "fx_interbank_vol_t2" in wide.columns:
            vol_total = wide["fx_interbank_vol_t1"].fillna(0) + wide["fx_interbank_vol_t2"].fillna(0)
        return {
            "dates":       _dates(wide.index),
            "ptax_venda":  _col(wide, "ptax_venda"),
            "vol_t1":      _col(wide, "fx_interbank_vol_t1"),
            "vol_t2":      _col(wide, "fx_interbank_vol_t2"),
            "vol_total":   _to_list(vol_total) if vol_total is not None else None,
        }
    except Exception as exc:
        print(f"  Aviso: erro em cmb_ptax — {exc}")
        return {}


def _load_termos() -> dict:
    try:
        wide = _pivot("macro_brasil", "cmb_termos_troca")
        if wide is None:
            return {}
        return {
            "dates":                  _dates(wide.index),
            "termos_de_troca_funcex": _col(wide, "termos_de_troca_funcex"),
        }
    except Exception as exc:
        print(f"  Aviso: erro em cmb_termos_troca — {exc}")
        return {}


# ── Entry point ───────────────────────────────────────────────────────────────

def run(output: str = "reports/fx_report.html") -> None:
    """Gera o relatório HTML de fundamentos cambiais.

    Lê tabelas de macro_brasil e macro_international, injeta os dados no
    template report.html e salva um único arquivo HTML autocontido.

    Args:
        output: caminho de saída. Default "reports/fx_report.html".
    """
    print("Carregando dados de macro_brasil / macro_international...")
    report_data = {
        "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "ptax":            _load_ptax(),
        "diferenciais":    _load_diferenciais(),
        "reer":            _load_reer(),
        "cot_fx":          _load_cot_fx(),
        "bcb_positioning": _load_bcb_positioning(),
        "fluxo":           _load_fluxo(),
        "bop":             _load_bop(),
        "termos":          _load_termos(),
    }

    template = _TEMPLATE.read_text(encoding="utf-8")
    payload = json.dumps(report_data, ensure_ascii=False, default=str)
    html = template.replace("/*REPORT_DATA*/", f"const REPORT_DATA = {payload};")

    out = Path(output)
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"Relatório salvo: {out.resolve()}")
