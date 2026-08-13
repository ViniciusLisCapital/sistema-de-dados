"""
Divida publica bruta e liquida (% PIB).

Series SGS coletadas (6 series, mensal, % PIB):
  Bruta  : dbgg_pct_pib (13762) — Divida Bruta do Governo Geral, metodologia 2008+
  Liquida: dlsp_pct_pib (4513) — Divida Liquida do Setor Publico, Total, setor publico
           consolidado (governo geral + Banco Central + empresas estatais)
  Liquida por nivel:
    dlsp_governo_federal_pct_pib     (4504)
    dlsp_banco_central_pct_pib       (4505)
    dlsp_estados_municipios_pct_pib  (4506)
    dlsp_empresas_estatais_pct_pib   (4509)

DBGG so existe no conceito "governo geral" (nao inclui empresas estatais) — e por
isso mais estreito que a DLSP, que e "setor publico" (inclui BC e estatais).

Codigos confirmados via busca no catalogo dadosabertos.bcb.gov.br (nao apenas por
memoria) em 2026-08 — mesma pratica adotada apos o bug de codigo SGS em
cmb_balanco_pagmt (ver comm_icbr.py).

Banco: macro_brasil.fisc_divida — PRIMARY KEY (date, name)
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "fisc_divida"

_SERIES = {
    "dbgg_pct_pib":                    13762,
    "dlsp_pct_pib":                     4513,
    "dlsp_governo_federal_pct_pib":     4504,
    "dlsp_banco_central_pct_pib":       4505,
    "dlsp_estados_municipios_pct_pib":  4506,
    "dlsp_empresas_estatais_pct_pib":   4509,
}

_bcb = BCB()


def run(start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.fisc_divida.

    Args:
        start: data inicial "DD/MM/YYYY", ou "all" para serie completa desde o
               inicio real de cada serie (DBGG comeca mais tarde que a DLSP —
               a API SGS retorna o que existir, sem erro).
        end:   data final "DD/MM/YYYY". Default: hoje.
    """
    if start:
        df = _bcb.get_sgs(_SERIES, start=start, end=end)
    else:
        df = _bcb.get_sgs_ultimos(_SERIES, n=36)

    insert_data_into_database(_DATABASE, _TABLE, df)
