"""
Gerador do Panorama de Inflacao em HTML.

Le a decomposicao do IPCA e IPCA-15 por subitem de macro_brasil.inflc_decomposicao
(join com macro_brasil.inflc_dim), mescla com os agregados BCB/SGS (CSV) e
injeta no template report.html, gerando um arquivo HTML autocontido.

Uso:
    uv run python analytics/inflation/generate_report.py
    uv run python -c "from analytics.inflation.generate_report import run; run()"
"""

import json
from datetime import datetime
from pathlib import Path

import pandas as pd

from connectors.mysql import MySQLDataRequester

_HERE = Path(__file__).parent
_TEMPLATE = _HERE / "report.html"
_DATA = _HERE / "data"
_BCB_CSV = _DATA / "ipca_bcb_series.csv"

_DATABASE = "macro_brasil"


def _load_decomposicao() -> pd.DataFrame:
    fatos = MySQLDataRequester(_DATABASE, "inflc_decomposicao")
    fatos.connect()
    df = fatos.request_data()
    fatos.close_connection()

    dimensao = MySQLDataRequester(_DATABASE, "inflc_dim")
    dimensao.connect()
    dim = dimensao.request_data()
    dimensao.close_connection()

    df["date"] = pd.to_datetime(df["date"])
    for col in ["var_mensal", "pesos", "contribuicao"]:
        df[col] = pd.to_numeric(df[col]).round(5)

    return df.merge(dim, on="subitem", how="left")


def _to_records(df: pd.DataFrame, indice: str) -> dict:
    sub = df[df["indice"] == indice].copy()
    if sub.empty:
        return {"records": [], "min_date": "", "max_date": ""}

    sub["dt"] = sub["date"].dt.strftime("%Y-%m")
    cols = ["dt", "subitem", "grupo", "subgrupo", "item", "subjacente",
            "nucleo_ex0", "nucleo_ex01", "nucleo_ex02", "nucleo_ex03",
            "nucleo_ex03_servicos", "nucleo_ex03_industriais", "nucleo_exfe",
            "var_mensal", "pesos", "contribuicao"]
    out = sub[cols].astype(object).where(pd.notna(sub[cols]), None)
    dates = sorted(sub["dt"].dropna().unique().tolist())
    return {
        "records":  out.to_dict(orient="records"),
        "min_date": dates[0] if dates else "",
        "max_date": dates[-1] if dates else "",
    }


def _load_bcb() -> dict:
    if not _BCB_CSV.exists():
        return {}
    df = pd.read_csv(_BCB_CSV, encoding="utf-8-sig")
    result = {}
    for name, grp in df.groupby("name"):
        grp = grp.sort_values("dt")
        result[name] = {
            "dates":  grp["dt"].tolist(),
            "values": [None if pd.isna(v) else round(float(v), 5) for v in grp["value"]],
        }
    return result


def run(output: str = "reports/inflation_latest.html") -> None:
    print("Carregando dados...")
    decomposicao = _load_decomposicao()

    ipca = _to_records(decomposicao, "IPCA")
    data = {
        "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "min_date":     ipca["min_date"],
        "max_date":     ipca["max_date"],
        "records":      ipca["records"],
    }
    print(f"  IPCA:    {len(data['records'])} registros ({data['min_date']} -> {data['max_date']})")

    ipca15 = _to_records(decomposicao, "IPCA15")
    data["records_ipca15"]  = ipca15["records"]
    data["min_date_ipca15"] = ipca15["min_date"]
    data["max_date_ipca15"] = ipca15["max_date"]
    print(f"  IPCA-15: {len(data['records_ipca15'])} registros ({data['min_date_ipca15']} -> {data['max_date_ipca15']})")

    data["bcb"] = _load_bcb()
    n_bcb = sum(len(v["dates"]) for v in data["bcb"].values())
    print(f"  BCB:     {n_bcb} obs ({len(data['bcb'])} series)")

    template = _TEMPLATE.read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False, default=str)
    html = template.replace("/*REPORT_DATA*/", f"const REPORT_DATA = {payload};")

    out = Path(output)
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"Relatorio salvo: {out.resolve()}")


if __name__ == "__main__":
    run()
