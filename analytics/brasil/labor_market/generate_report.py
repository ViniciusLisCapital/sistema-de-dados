"""
Gerador do Panorama de Mercado de Trabalho em HTML -- so visualizacao (sem
metricas derivadas, ver pnad_tab.py/caged_tab.py).

Le mt_pnad + mt_pnad_trimestral (IBGE/PNAD, abas Taxas/Ocupacao/Rendimento),
mt_desocupacao_retro (a taxa de desocupacao do BCB, ao lado da do IBGE) e
mt_caged_setor/_uf/_salario + mt_caged (MTE/BCB, aba Emprego Formal) de
macro_brasil, injeta no template report.html, gerando um arquivo HTML
autocontido. Mesmo padrao /*REPORT_DATA*/ de analytics/brasil/fiscal_policy/ e
analytics/brasil/economic_activity/ -- sem Jinja2, via
analytics.report_structure.builder.render_report().

Uso:
    uv run python -c "from analytics.brasil.labor_market.generate_report import run; run()"
"""
from datetime import datetime
from pathlib import Path

import pandas as pd

from analytics.brasil.labor_market import caged_tab, pnad_tab
from analytics.report_structure.builder import render_report
from connectors.mysql import MySQLDataRequester

_HERE = Path(__file__).parent
_TEMPLATE = _HERE / "report.html"

_DATABASE = "macro_brasil"


def _load_flat(table: str) -> dict:
    req = MySQLDataRequester(_DATABASE, table)
    req.connect()
    df = req.request_data()
    req.close_connection()
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"])

    result = {}
    for name, grp in df.groupby("name"):
        grp = grp.sort_values("date")
        item = {
            "dates":  grp["date"].dt.strftime("%Y-%m-%d").tolist(),
            "values": [None if pd.isna(v) else round(float(v), 4) for v in grp["value"]],
        }
        # So `mt_caged` tem a coluna: ela marca com fonte='mte' os meses que o
        # BCB ainda nao publicou e o tampao reconstruiu somando o saldo do
        # microdado -- ver domain/db/brasil/bcb/mt_caged.py.
        if "fonte" in grp.columns:
            item["fonte"] = grp["fonte"].tolist()
        result[name] = item
    return result


def _load_caged_cut(table: str) -> dict:
    """Le uma das 3 tabelas de corte do Novo CAGED (formato longo: date,
    categoria, metrica, value) e devolve
    {"_dates": [...], categoria: {metrica: [valores]}} num eixo mensal COMUM.

    Reindexar e obrigatorio, nao cosmetico: `mt_caged_setor` tem buracos (uma
    secao sem nenhuma movimentacao num mes nao gera linha -- 5.103 linhas contra
    as 5.148 de 22x3x78). Sem alinhar, a soma dos cortes desalinharia no tempo e
    as janelas moveis de 12m escorregariam. Ausencia = zero movimentacoes, que e
    a leitura correta para uma contagem de eventos (nao um dado faltante)."""
    req = MySQLDataRequester(_DATABASE, table)
    req.connect()
    df = req.request_data()
    req.close_connection()
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"])

    eixo = sorted(df["date"].unique())
    dates = [pd.Timestamp(d).strftime("%Y-%m-%d") for d in eixo]

    out = {"_dates": dates}
    for (categoria, metrica), grp in df.groupby(["categoria", "metrica"]):
        serie = grp.set_index("date")["value"].reindex(eixo, fill_value=0.0)
        out.setdefault(categoria, {})[metrica] = [float(v) for v in serie]
    return out


def _load_desocupacao_bcb() -> dict:
    """mt_desocupacao_retro: serie unica, sem coluna `name`, uma edicao do RPM
    por vez (`vintage`). A edicao vai junto porque e ela que a linha da fonte
    do grafico cita -- a serie do BCB so anda quando sai um RPM novo, entao
    costuma terminar um ou dois meses antes da PNAD."""
    req = MySQLDataRequester(_DATABASE, "mt_desocupacao_retro")
    req.connect()
    df = req.request_data()
    req.close_connection()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    vintages = pd.to_datetime(df["vintage"]).dt.strftime("%Y-%m-%d").unique().tolist()
    if len(vintages) != 1:
        raise RuntimeError(f"mt_desocupacao_retro deveria ter uma edicao so, tem {vintages}")
    return {
        "dates":   df["date"].dt.strftime("%Y-%m-%d").tolist(),
        "values":  [round(float(v), 4) for v in pd.to_numeric(df["value"])],
        "vintage": vintages[0],
    }


def _load_pnad_tab_data() -> dict:
    """Abas Taxas/Ocupacao/Rendimento -- ver analytics/brasil/labor_market/pnad_tab.py."""
    mensal = _load_flat("mt_pnad")
    trimestral = _load_flat("mt_pnad_trimestral")
    # A serie do BCB e uma linha a mais numa tabela, nao a aba: se ela faltar, a
    # aba sai sem ela em vez de sair vazia.
    try:
        bcb = _load_desocupacao_bcb()
    except Exception as exc:
        print(f"  mt_desocupacao_retro: FALHOU -- {exc} (a tabela de desocupacao sai sem a linha do BCB)")
        bcb = None
    return pnad_tab.build(mensal, trimestral, bcb=bcb)


def _load_caged_tab_data() -> dict:
    """Aba Emprego Formal -- ver analytics/brasil/labor_market/caged_tab.py."""
    return caged_tab.build(
        setor=_load_caged_cut("mt_caged_setor"),
        uf=_load_caged_cut("mt_caged_uf"),
        salario=_load_caged_cut("mt_caged_salario"),
        estoque=_load_flat("mt_caged"),
    )


def run(output: str = "reports/brasil/Labor Market.html") -> None:
    print("Carregando dados...")
    data = {"generated_at": datetime.now().strftime("%d/%m/%Y %H:%M")}

    try:
        pnad = _load_pnad_tab_data()
        data["pnad"] = pnad
        print(f"  pnad (mt_pnad + mt_pnad_trimestral): {len(pnad['series'])} series")
    except Exception as exc:
        print(f"  pnad: FALHOU -- {exc}")
        data["pnad"] = {"tabs": [], "series": {}, "ref_date": None, "rate_keys": []}

    try:
        caged = _load_caged_tab_data()
        data["caged"] = caged
        print(f"  caged (mt_caged_setor/_uf/_salario + mt_caged): {len(caged['series'])} series")
    except Exception as exc:
        print(f"  caged: FALHOU -- {exc}")
        data["caged"] = {"tables": [], "series": {}, "ref_date": None}

    out = render_report(_TEMPLATE, data, output)
    print(f"Relatorio salvo: {out}")


if __name__ == "__main__":
    run()
