"""
PIB mensal em dolares (BCB SGS 4385)

Serie SGS 4385 "PIB mensal - em dolar" (US$ milhoes) - estimativa mensal do
PIB brasileiro convertida a dolares pelo BCB (Depec). Fonte e frequencia
diferentes de `atv_pib` (PIB trimestral em R$, IBGE 1620/1621) - tabelas
separadas de proposito, sem relacao direta uma com a outra.

Uso: analytics/exchange_rate/generate_report.py consome esta serie para normalizar
as series de Balanco de Pagamentos (`cmb_balanco_pagmt`) como % do PIB na
aba "Balanco de Pagamentos" (botao de alternancia USD Bi / % PIB, 2026-07).
Nao alimenta nenhum outro relatorio.

Banco: macro_brasil.atv_pib_usd
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "atv_pib_usd"

_SERIES = {
    "pib_usd": 4385,
}

_bcb = BCB()


def run(n_meses: int = 36, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.atv_pib_usd.

    Args:
        n_meses: ultimos N meses (default 36). Ignorado se start/end fornecidos.
        start:   data inicial no formato "DD/MM/YYYY", ou "all" para serie completa.
        end:     data final no formato "DD/MM/YYYY". Default: hoje.
    """
    if start:
        df = _bcb.get_sgs(_SERIES, start=start, end=end)
    else:
        df = _bcb.get_sgs_ultimos(_SERIES, n=n_meses)

    insert_data_into_database(_DATABASE, _TABLE, df)
