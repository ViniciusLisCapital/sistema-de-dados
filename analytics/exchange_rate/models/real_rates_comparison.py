"""
Comparação histórica da taxa real de juros ex-post entre Brasil e pares
emergentes (MX, CL, CO, PE), mais um segundo gráfico comparando a taxa real
brasileira com o crescimento real do gasto do governo — HTML autocontido,
mesmo padrão /*REPORT_DATA*/ de exchange_rate/report.html.

Fontes:
  macro_international.cmb_real_rates (name='real_rate_ex_post') — ver
    domain/db/international/bis/cmb_real_rates.py.
  macro_brasil.atv_pib (name='consumo_adm_publica', seasonal_adjs='N') —
    Despesa de Consumo da Administração Pública, componente da ótica da
    despesa do PIB trimestral (IBGE, índice de volume encadeado). Var. 12
    meses (YoY) calculada aqui, não armazenada no banco (mesma convenção de
    diferenciais_juros/inflc_agregados: taxas de crescimento ficam na camada
    de consumo, não como segunda fonte de verdade no banco).
"""

from pathlib import Path

import pandas as pd

from analytics.report_structure.builder import render_report
from connectors.mysql import MySQLDataRequester

_TEMPLATE = Path(__file__).parent / "real_rates_comparison_template.html"

_COUNTRY_LABELS = {
    "BR": "Brasil",
    "MX": "México",
    "CL": "Chile",
    "CO": "Colômbia",
    "PE": "Peru",
}

_GOV_SPENDING_START = "2000-01-01"


def _load_real_rates() -> dict:
    requester = MySQLDataRequester("macro_international", "cmb_real_rates")
    requester.connect()
    df = requester.request_data()
    requester.close_connection()

    df = df[df["name"] == "real_rate_ex_post"].copy()
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

    series = {}
    for country, g in df.sort_values("date").groupby("country_code"):
        series[country] = {
            "dates": g["date"].tolist(),
            "values": [round(float(v), 3) for v in g["value"].tolist()],
        }
    return series


def _load_gov_spending_yoy() -> dict:
    requester = MySQLDataRequester("macro_brasil", "atv_pib")
    requester.connect()
    df = requester.request_data()
    requester.close_connection()

    df = df[(df["name"] == "consumo_adm_publica") & (df["seasonal_adjs"] == "N")].copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    df["yoy"] = df["value"].astype(float).pct_change(4) * 100

    df = df[df["date"] >= _GOV_SPENDING_START].dropna(subset=["yoy"])

    return {
        "dates": df["date"].dt.strftime("%Y-%m-%d").tolist(),
        "values": [round(float(v), 3) for v in df["yoy"].tolist()],
    }


def run(output: str = "reports/real_rates_comparison.html") -> None:
    data = {
        "series": _load_real_rates(),
        "labels": _COUNTRY_LABELS,
        "gov_spending_yoy": _load_gov_spending_yoy(),
    }
    out = render_report(_TEMPLATE, data, output)
    print(f"Relatorio salvo: {out}")
