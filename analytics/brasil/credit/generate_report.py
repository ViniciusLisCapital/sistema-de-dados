"""
Gerador do Panorama de Credito em HTML.

Le credito ampliado ao setor nao financeiro (cred_credito_amplo), resumo do
credito do sistema financeiro por recurso x segmento (cred_credito_resumo),
endividamento das familias (cred_credito_familias) e Selic + proxies de
estresse de credito PJ (cred_inadimplencia_pj) de macro_brasil, e injeta no
template report.html, gerando um arquivo HTML autocontido. Mesmo padrao
/*REPORT_DATA*/ de analytics/brasil/fiscal_policy/ e analytics/brasil/economic_activity/ --
sem Jinja2, via analytics.report_structure.builder.render_report().

Uso:
    uv run python analytics/brasil/credit/generate_report.py
    uv run python -c "from analytics.brasil.credit.generate_report import run; run()"
"""

from datetime import datetime
from pathlib import Path

import pandas as pd

from analytics.brasil.credit import (
    amplo_tab,
    concessao_tab,
    impulso_tab,
    inadimplencia_tab,
    ptc_tab,
    saldo_tab,
    taxa_tab,
)
from analytics.report_structure.builder import render_report
from connectors.mysql import MySQLDataRequester

_HERE = Path(__file__).parent
_TEMPLATE = _HERE / "report.html"

_DATABASE = "macro_brasil"

# Todas as 4 tabelas sao (date, name, value) simples -- sem coluna seasonal_adjs.
_TABLES = {
    "amplo":    "cred_credito_amplo",
    "resumo":   "cred_credito_resumo",
    "familias": "cred_credito_familias",
    "pj":       "cred_inadimplencia_pj",
}


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
        result[name] = {
            "dates":  grp["date"].dt.strftime("%Y-%m-%d").tolist(),
            "values": [None if pd.isna(v) else round(float(v), 4) for v in grp["value"]],
        }
    return result


# Abas interativas (Saldo, Concessao, ...): comeco comum para todas as series, mesmo as
# que tem historico mais longo na base (saldo_total_total vai a 1988-06,
# cred_modalidade_livre_pj/pf a 1994-07) -- decisao explicita do usuario (2026-08) para
# manter a tabela/grafico numa janela consistente entre modalidades em vez de cada linha
# comecar num ano diferente.
_TAB_MIN_DATE = "2000-01-01"


def _clip_from(series: dict, min_date: str) -> dict:
    dates, values = series["dates"], series["values"]
    idx = [i for i, d in enumerate(dates) if d >= min_date]
    return {"dates": [dates[i] for i in idx], "values": [values[i] for i in idx]}


def _load_by_metric(table: str, group_col: str, prefix: str, metrica: str) -> dict:
    """Le uma tabela (date, `group_col`, metrica, value) filtrando por `metrica`
    ('saldo'|'concessao'|'taxa_media'|'inadimplencia'|...), com chaves prefixadas por
    `prefix` (ex: 'livre_pj__capital_de_giro_total') para casar com a arvore da aba
    correspondente. `group_col` e 'modalidade' para cred_modalidade_*, 'porte' para
    cred_credito_porte -- mesmo shape de tabela, coluna de agrupamento com nome
    diferente."""
    req = MySQLDataRequester(_DATABASE, table)
    req.connect()
    df = req.request_data()
    req.close_connection()
    df = df[df["metrica"] == metrica].copy()
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"])

    result = {}
    for group_val, grp in df.groupby(group_col):
        grp = grp.sort_values("date")
        result[f"{prefix}__{group_val}"] = {
            "dates":  grp["date"].dt.strftime("%Y-%m-%d").tolist(),
            "values": [None if pd.isna(v) else round(float(v), 4) for v in grp["value"]],
        }
    return result


def _load_flat_prefixed(table: str, prefix: str, only_keys: list[str] | None = None) -> dict:
    """_load_flat() com chaves prefixadas por `prefix` -- para tabelas (date, name,
    value) simples que entram numa arvore de aba (cred_credito_atividade_economica,
    cred_credito_tipo_cliente). `only_keys` filtra para so essas chaves (sem prefixo)
    quando nem toda coluna da tabela e usada (ex: tipo_cliente.total, que duplica
    saldo_total_total e ja vem de outro lugar)."""
    flat = _load_flat(table)
    if only_keys is not None:
        flat = {k: v for k, v in flat.items() if k in only_keys}
    return {f"{prefix}__{k}": v for k, v in flat.items()}


def _load_saldo_tab_data(resumo_series: dict, pib_acum_12m: dict) -> dict:
    ipca = _load_flat("inflc_agregados")["ipca"]

    raw = {k: resumo_series[k] for k in saldo_tab.resumo_saldo_keys() if k in resumo_series}
    for prefix, table in saldo_tab.MODALIDADE_TABLES:
        raw.update(_load_by_metric(table, "modalidade", prefix, "saldo"))
    porte_prefix, porte_table = saldo_tab.PORTE_TABLE
    raw.update(_load_by_metric(porte_table, "porte", porte_prefix, "saldo"))
    ativ_prefix, ativ_table = saldo_tab.ATIVIDADE_ECONOMICA_TABLE
    raw.update(_load_flat_prefixed(ativ_table, ativ_prefix))
    tipocliente_prefix, tipocliente_table = saldo_tab.TIPO_CLIENTE_TABLE
    raw.update(_load_flat_prefixed(
        tipocliente_table, tipocliente_prefix, only_keys=saldo_tab.TIPO_CLIENTE_KEYS_EXCLUDING_TOTAL
    ))
    raw = {k: _clip_from(s, _TAB_MIN_DATE) for k, s in raw.items()}

    return saldo_tab.build(raw, ipca, pib_acum_12m)


def _load_concessao_tab_data(resumo_series: dict, pib_acum_12m: dict) -> dict:
    ipca = _load_flat("inflc_agregados")["ipca"]

    raw = {k: resumo_series[k] for k in concessao_tab.resumo_concessao_keys() if k in resumo_series}
    for prefix, table in concessao_tab.MODALIDADE_TABLES:
        raw.update(_load_by_metric(table, "modalidade", prefix, "concessao"))
    raw = {k: _clip_from(s, _TAB_MIN_DATE) for k, s in raw.items()}

    return concessao_tab.build(raw, ipca, pib_acum_12m)


def _load_impulso_tab_data(resumo_series: dict, pib_acum_12m: dict) -> dict:
    """Aba Impulso: so precisa do SALDO NOMINAL bruto + PIB 12m -- sem IPCA (a metrica
    ja e uma razao contra o PIB nominal, o deflator cancelaria) e sem STL (a diferenca
    de 12 meses ja cancela sazonalidade por construcao)."""
    raw = {k: resumo_series[k] for k in impulso_tab.resumo_impulso_keys() if k in resumo_series}
    porte_prefix, porte_table = impulso_tab.PORTE_TABLE
    raw.update(_load_by_metric(porte_table, "porte", porte_prefix, "saldo"))
    ativ_prefix, ativ_table = impulso_tab.ATIVIDADE_ECONOMICA_TABLE
    raw.update(_load_flat_prefixed(ativ_table, ativ_prefix, only_keys=impulso_tab.ATIVIDADE_KEYS))
    raw = {k: _clip_from(s, _TAB_MIN_DATE) for k, s in raw.items()}

    return impulso_tab.build(raw, pib_acum_12m)


def _load_ptc_tab_data() -> dict:
    """Aba PTC: le cred_ptc cru e so reagrupa por horizonte. Sem IPCA, sem STL, sem PIB
    -- indice de difusao nao aceita nenhuma dessas transformacoes (ver ptc_tab.py). Sem
    _clip_from(_TAB_MIN_DATE) tambem: a pesquisa comeca em 2011-04, ja dentro da janela.
    """
    return ptc_tab.build(_load_flat("cred_ptc"))


def _load_amplo_tab_data(amplo_series: dict, pib_acum_12m: dict) -> dict:
    ipca = _load_flat("inflc_agregados")["ipca"]

    raw = {f"amplo__{k}": v for k, v in amplo_series.items()}
    raw = {k: _clip_from(s, _TAB_MIN_DATE) for k, s in raw.items()}

    return amplo_tab.build(raw, ipca, pib_acum_12m)


def _load_taxa_tab_data(resumo_series: dict, selic: dict) -> dict:
    raw_taxa = {k: resumo_series[k] for k in taxa_tab.resumo_taxa_keys() if k in resumo_series}
    for prefix, table in taxa_tab.MODALIDADE_TABLES:
        raw_taxa.update(_load_by_metric(table, "modalidade", prefix, "taxa_media"))
    raw_taxa = {k: _clip_from(s, _TAB_MIN_DATE) for k, s in raw_taxa.items()}

    raw_spread = {k: resumo_series[k] for k in taxa_tab.resumo_spread_keys() if k in resumo_series}
    raw_spread = {k: _clip_from(s, _TAB_MIN_DATE) for k, s in raw_spread.items()}

    return taxa_tab.build(raw_taxa, raw_spread, selic)


def _load_inadimplencia_tab_data(resumo_series: dict, pj_series: dict, selic: dict) -> dict:
    raw = {k: resumo_series[k] for k in inadimplencia_tab.resumo_inadimplencia_keys() if k in resumo_series}
    for prefix, table in inadimplencia_tab.MODALIDADE_TABLES:
        raw.update(_load_by_metric(table, "modalidade", prefix, "inadimplencia"))
    porte_prefix, porte_table = inadimplencia_tab.PORTE_TABLE
    raw.update(_load_by_metric(porte_table, "porte", porte_prefix, "inadimplencia"))
    controle_prefix, controle_table = inadimplencia_tab.CONTROLE_TABLE
    raw.update(_load_by_metric(controle_table, "controle", controle_prefix, "inadimplencia"))
    riscoant_prefix, riscoant_table = inadimplencia_tab.RISCO_ANTERIOR_TABLE
    raw.update(_load_by_metric(riscoant_table, "porte", riscoant_prefix, "saldo_maior_risco"))
    riscores_prefix, riscores_table = inadimplencia_tab.RISCO_RES4966_TABLE
    raw.update(_load_by_metric(riscores_table, "porte", riscores_prefix, "saldo_maior_risco_res4966"))
    if "atraso_pj" in pj_series:
        raw["pj__atraso_pj"] = pj_series["atraso_pj"]
    raw = {k: _clip_from(s, _TAB_MIN_DATE) for k, s in raw.items()}

    return inadimplencia_tab.build(raw, selic)


def run(output: str = "reports/brasil/Credit.html") -> None:
    print("Carregando dados...")
    data = {"generated_at": datetime.now().strftime("%d/%m/%Y %H:%M")}

    for group, table in _TABLES.items():
        try:
            series = _load_flat(table)
            data[group] = series
            n_obs = sum(len(v["dates"]) for v in series.values())
            print(f"  {group:9s} ({table}): {len(series)} series, {n_obs} obs")
        except Exception as exc:
            print(f"  {group:9s} ({table}): FALHOU -- {exc}")
            data[group] = {}

    try:
        pib_acum_12m = _load_flat("atv_pib_mensal")["pib_acum_12m"]
    except Exception as exc:
        print(f"  pib_acum_12m (para % do PIB): FALHOU -- {exc}")
        pib_acum_12m = {"dates": [], "values": []}

    try:
        data["saldo"] = _load_saldo_tab_data(data.get("resumo", {}), pib_acum_12m)
        print(f"  saldo     (arvore de modalidades): {len(data['saldo']['series'])} series, STL + deflacao IPCA")
    except Exception as exc:
        print(f"  saldo     (arvore de modalidades): FALHOU -- {exc}")
        data["saldo"] = {"tree": [], "series": {}, "ref_date": None}

    try:
        data["concessao"] = _load_concessao_tab_data(data.get("resumo", {}), pib_acum_12m)
        print(f"  concessao (arvore de modalidades): {len(data['concessao']['series'])} series, STL+MM3M + deflacao IPCA")
    except Exception as exc:
        print(f"  concessao (arvore de modalidades): FALHOU -- {exc}")
        data["concessao"] = {"tree": [], "series": {}, "ref_date": None}

    try:
        data["impulso"] = _load_impulso_tab_data(data.get("resumo", {}), pib_acum_12m)
        print(f"  impulso   (3 tabelas de decomposicao): {len(data['impulso']['series'])} series")
    except Exception as exc:
        print(f"  impulso   (3 tabelas de decomposicao): FALHOU -- {exc}")
        data["impulso"] = {"trees": {}, "anchors": {}, "series": {}, "ref_date": None}

    try:
        data["amplo_hier"] = _load_amplo_tab_data(data.get("amplo", {}), pib_acum_12m)
        print(f"  amplo_hier (2a tabela da aba Saldo): {len(data['amplo_hier']['series'])} series")
    except Exception as exc:
        print(f"  amplo_hier (2a tabela da aba Saldo): FALHOU -- {exc}")
        data["amplo_hier"] = {"tree": [], "series": {}, "ref_date": None}

    selic = data.get("pj", {}).get("selic", {"dates": [], "values": []})

    try:
        data["taxa"] = _load_taxa_tab_data(data.get("resumo", {}), selic)
        n_taxa = len(data["taxa"]["taxa_media"]["series"]) + len(data["taxa"]["spread"]["series"])
        print(f"  taxa      (Taxa Media + Spread): {n_taxa} series")
    except Exception as exc:
        print(f"  taxa      (Taxa Media + Spread): FALHOU -- {exc}")
        data["taxa"] = {"taxa_media": {"tree": [], "series": {}}, "spread": {"tree": [], "series": {}}, "selic": {"dates": [], "values": []}}

    try:
        data["ptc"] = _load_ptc_tab_data()
        # 2 variantes vem do SGS (observada/esperada); desvio e desvio_ma4 sao derivadas
        n_ptc = sum(1 for v in data["ptc"]["series"].values() for k in ptc_tab.HORIZONTES if v.get(k))
        n_dv = sum(1 for v in data["ptc"]["series"].values() if v.get("desvio"))
        print(f"  ptc       (Pesquisa Trimestral de Condicoes de Credito): {n_ptc} series"
              f" + {n_dv} desvios (observada - esperada do trimestre anterior) + MA 4T de cada")
    except Exception as exc:
        print(f"  ptc       (Pesquisa Trimestral de Condicoes de Credito): FALHOU -- {exc}")
        data["ptc"] = {"tree": [], "anchor": None, "series": {}, "ref_date": None}

    try:
        data["inadimplencia"] = _load_inadimplencia_tab_data(data.get("resumo", {}), data.get("pj", {}), selic)
        print(f"  inadimplencia (Inadimplencia + Saldo de Maior Risco): {len(data['inadimplencia']['series'])} series")
    except Exception as exc:
        print(f"  inadimplencia (Inadimplencia + Saldo de Maior Risco): FALHOU -- {exc}")
        data["inadimplencia"] = {"tree": [], "series": {}, "selic": {"dates": [], "values": []}}

    out = render_report(_TEMPLATE, data, output)
    print(f"Relatorio salvo: {out}")


if __name__ == "__main__":
    run()
