"""
IC-Br (Indice de Commodities - Brasil) em USD -- BCB SGS 29042.

Distinto de comm_icbr.py (SGS 27574 etc.), que e denominado em REAIS. O BCB
converte precos internacionais de commodities para reais na construcao do
IC-Br "geral" -- adequado para o proposito original do indice (insumo da
curva de Phillips de precos livres do modelo agregado, onde o repasse
cambial e parte do que se quer capturar), mas isso o torna ENDOGENO ao
proprio USD/BRL, inadequado como regressor num modelo que explica o
USD/BRL (circularidade: o canal ja embute parte do movimento da variavel
dependente). SGS 29042 e a versao em dolar do mesmo indice, testada e
confirmada 2026-07-31 no ridge_deviation_model.py como canal USD-neutro de
precos globais de commodities -- melhorou o MSE out-of-sample (walk-forward)
em ~4.6% isoladamente sobre o spec ja embarcado, com coeficiente negativo e
estavel (quase nunca cruza zero nas 163 janelas rolantes) -- ver
analytics/brasil/exchange_rate/CLAUDE.md para o registro completo.

Codigo confirmado por identificacao direta do usuario (nao pela metadata
API do BCB, que exige sessao autenticada); corroborado indiretamente aqui
por retornar valores materialmente diferentes de SGS 27574 para os mesmos
meses (consistente com duas denominacoes distintas do mesmo indice
subjacente).

Serie SGS (mensal, desde 1998-01):
  icbr_usd  29042 — IC-Br geral, em USD

Banco: macro_brasil.comm_icbr_usd — PRIMARY KEY (date, name)
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "comm_icbr_usd"

_SERIES = {
    "icbr_usd": 29042,
}

_bcb = BCB()


def run(start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.comm_icbr_usd.

    Args:
        start: data inicial "DD/MM/YYYY", ou "all" para serie completa (desde 1998).
        end:   data final "DD/MM/YYYY". Default: hoje.
    """
    if start == "all":
        df = _bcb.get_sgs(_SERIES, start="01/01/1998", end=end)
    elif start:
        df = _bcb.get_sgs(_SERIES, start=start, end=end)
    else:
        df = _bcb.get_sgs_ultimos(_SERIES, n=36)

    insert_data_into_database(_DATABASE, _TABLE, df)
