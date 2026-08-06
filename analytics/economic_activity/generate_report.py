"""
Gerador do Panorama de Atividade Economica em HTML.

Le PIB (atv_pib), Producao Industrial (atv_pim), Comercio (atv_pmc), Servicos
(atv_pms) e IBC-Br (atv_ibcbr) de macro_brasil, e injeta no template
report.html, gerando um arquivo HTML autocontido. Mesmo padrao
/*REPORT_DATA*/ de analytics/inflation/ e analytics/exchange_rate/ -- sem
Jinja2, via analytics.report_structure.builder.render_report().

Uso:
    uv run python analytics/economic_activity/generate_report.py
    uv run python -c "from analytics.economic_activity.generate_report import run; run()"
"""

from datetime import datetime
from pathlib import Path

import pandas as pd

from analytics.report_structure.builder import render_report
from connectors.mysql import MySQLDataRequester

_HERE = Path(__file__).parent
_TEMPLATE = _HERE / "report.html"

_DATABASE = "macro_brasil"

# Tabelas com coluna seasonal_adjs separada ("Y"/"N") -- o sufixo _sa/_nsa e
# adicionado ao nome aqui, na leitura, para virar a chave final da serie.
_SUFFIXED_TABLES = {
    "pib":     "atv_pib",
    "pib_enc": "atv_pib_encadeado",  # R$ mi a precos de 1995 -- insumo da decomposicao de crescimento
    "pim":     "atv_pim",
    "pmc":     "atv_pmc",
    "pms":     "atv_pms",
}

# atv_ibcbr ja grava o sufixo _sa/_nsa dentro do proprio "name" (ver
# domain/db/brasil/bcb/atv_ibcbr.py) -- nao precisa de sufixo adicional,
# so agrupar por name direto. O resultado final tem exatamente o mesmo
# formato de chave (<base>_sa / <base>_nsa) que as tabelas acima.
_FLAT_TABLES = {
    "ibcbr": "atv_ibcbr",
}


def _load_table(table: str) -> pd.DataFrame:
    req = MySQLDataRequester(_DATABASE, table)
    req.connect()
    df = req.request_data()
    req.close_connection()
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"])
    return df


def _series_dict(df: pd.DataFrame, key_fn) -> dict:
    result = {}
    for key, grp in df.groupby(df.apply(key_fn, axis=1)):
        grp = grp.sort_values("date")
        result[key] = {
            "dates":  grp["date"].dt.strftime("%Y-%m-%d").tolist(),
            "values": [None if pd.isna(v) else round(float(v), 4) for v in grp["value"]],
        }
    return result


def _load_suffixed(table: str) -> dict:
    df = _load_table(table)
    return _series_dict(df, lambda r: r["name"] + ("_sa" if r["seasonal_adjs"] == "Y" else "_nsa"))


def _load_flat(table: str) -> dict:
    df = _load_table(table)
    return _series_dict(df, lambda r: r["name"])


def _load_pib_taxas() -> dict:
    """atv_pib_taxas has (date, name, indicador, value) -- no seasonal_adjs column, since each
    indicador (yoy/acum_4t/acum_ano/qoq) is inherently NSA or SA by its own definition. Key format
    mirrors _load_suffixed()'s "<base>_sa"/"<base>_nsa" convention but with a double underscore
    separator (e.g. "pib_pm__qoq") to keep it visually distinct from that single-underscore one --
    report.html reads this group (D.pib_taxas) separately from D.pib.
    """
    df = _load_table("atv_pib_taxas")
    return _series_dict(df, lambda r: r["name"] + "__" + r["indicador"])


def run(output: str = "reports/economic_activity_latest.html") -> None:
    print("Carregando dados...")
    data = {"generated_at": datetime.now().strftime("%d/%m/%Y %H:%M")}

    for group, table in _SUFFIXED_TABLES.items():
        try:
            series = _load_suffixed(table)
            data[group] = series
            n_obs = sum(len(v["dates"]) for v in series.values())
            print(f"  {group:6s} ({table}): {len(series)} series, {n_obs} obs")
        except Exception as exc:
            print(f"  {group:6s} ({table}): FALHOU -- {exc}")
            data[group] = {}

    for group, table in _FLAT_TABLES.items():
        try:
            series = _load_flat(table)
            data[group] = series
            n_obs = sum(len(v["dates"]) for v in series.values())
            print(f"  {group:6s} ({table}): {len(series)} series, {n_obs} obs")
        except Exception as exc:
            print(f"  {group:6s} ({table}): FALHOU -- {exc}")
            data[group] = {}

    try:
        series = _load_pib_taxas()
        data["pib_taxas"] = series
        n_obs = sum(len(v["dates"]) for v in series.values())
        print(f"  pib_taxas (atv_pib_taxas): {len(series)} series, {n_obs} obs")
    except Exception as exc:
        print(f"  pib_taxas (atv_pib_taxas): FALHOU -- {exc}")
        data["pib_taxas"] = {}

    out = render_report(_TEMPLATE, data, output)
    print(f"Relatorio salvo: {out}")


if __name__ == "__main__":
    run()
