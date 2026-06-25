"""
Gerador do Panorama IPCA em HTML.

Le os dados de decomposicao do IPCA e IPCA-15 (Excel), mescla com as tabelas de
dimensoes e injeta no template report.html, gerando um arquivo HTML autocontido.

Uso:
    uv run python analytics/ipca/generate_report.py
    uv run python -c "from analytics.ipca.generate_report import run; run()"
"""

import json
from datetime import datetime
from pathlib import Path

import pandas as pd

_HERE = Path(__file__).parent
_TEMPLATE = _HERE / "report.html"
_DATA = _HERE / "data"
_DADOS_IPCA   = _DATA / "variacao_peso_contribuicao_ipca.xlsx"
_DIM_IPCA     = _DATA / "tabela_dimensao_ipca.xlsx"
_DADOS_IPCA15 = _DATA / "variacao_peso_contribuicao_ipca15.xlsx"
_DIM_IPCA15   = _DATA / "dim_inflation_ipca15.xlsx"
_BCB_CSV      = _DATA / "ipca_bcb_series.csv"


def _load_data() -> dict:
    df = pd.read_excel(_DADOS_IPCA)
    df = df.rename(columns={"contribuição_mensal": "contribuicao"})
    df["dt"] = pd.to_datetime(df["dt"]).dt.to_period("M").astype(str)

    dim = pd.read_excel(_DIM_IPCA, sheet_name="dimensao_bcb_2020")
    merged = df.merge(
        dim[["Subitem", "Grupo", "Subgrupo", "Item", "Subjacente"]],
        on="Subitem", how="left",
    )
    for col in ["var_mensal", "pesos", "contribuicao"]:
        merged[col] = merged[col].round(5)
    merged = merged.rename(columns={
        "Subitem": "subitem", "Grupo": "grupo", "Subgrupo": "subgrupo",
        "Item": "item", "Subjacente": "subjacente",
    })
    cols = ["dt", "subitem", "grupo", "subgrupo", "item", "subjacente",
            "var_mensal", "pesos", "contribuicao"]
    out = merged[cols].astype(object).where(pd.notna(merged[cols]), None)
    dates = sorted(merged["dt"].dropna().unique().tolist())
    return {
        "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "min_date":  dates[0] if dates else "",
        "max_date":  dates[-1] if dates else "",
        "records":   out.to_dict(orient="records"),
    }


def _load_data_ipca15() -> dict:
    if not _DADOS_IPCA15.exists():
        return {"records": [], "min_date": "", "max_date": ""}
    try:
        df = pd.read_excel(_DADOS_IPCA15)
        df = df.rename(columns={"contribuição_mensal": "contribuicao"})
        if "Unnamed: 0" in df.columns:
            df = df.drop(columns=["Unnamed: 0"])
        df["dt"] = pd.to_datetime(df["dt"]).dt.to_period("M").astype(str)

        dim = pd.read_excel(_DIM_IPCA15, sheet_name="dim_bcb_view")
        dim_subj = pd.read_excel(_DIM_IPCA, sheet_name="dimensao_bcb_2020")[["Subitem", "Subjacente"]]
        merged = df.merge(
            dim[["Subitem", "Grupo", "Subgrupo", "Item"]],
            on="Subitem", how="left",
        ).merge(dim_subj, on="Subitem", how="left")
        for col in ["var_mensal", "pesos", "contribuicao"]:
            if col in merged.columns:
                merged[col] = merged[col].round(5)
        merged = merged.rename(columns={
            "Subitem": "subitem", "Grupo": "grupo", "Subgrupo": "subgrupo",
            "Item": "item", "Subjacente": "subjacente",
        })
        cols = ["dt", "subitem", "grupo", "subgrupo", "item", "subjacente",
                "var_mensal", "pesos", "contribuicao"]
        out = merged[cols].astype(object).where(pd.notna(merged[cols]), None)
        dates = sorted(merged["dt"].dropna().unique().tolist())
        return {
            "records":  out.to_dict(orient="records"),
            "min_date": dates[0] if dates else "",
            "max_date": dates[-1] if dates else "",
        }
    except Exception as e:
        print(f"  Aviso: IPCA-15 nao carregado — {e}")
        return {"records": [], "min_date": "", "max_date": ""}


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


def run(output: str = "reports/ipca_latest.html") -> None:
    print("Carregando dados...")
    data = _load_data()
    print(f"  IPCA:    {len(data['records'])} registros ({data['min_date']} -> {data['max_date']})")

    ipca15 = _load_data_ipca15()
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
