"""
Indicadores de condicoes financeiras das familias (BCB/SGS)

Series SGS coletadas (3 series — endividamento e servico da divida em % da renda):
  29037 - Endividamento das familias / renda acumulada (12 meses)
  29033 - Comprometimento da renda com juros
  29034 - Comprometimento da renda com servico da divida (juros + amortizacao)

  Fonte: Nota de Credito do BCB

Banco: macro_brasil.cred_credito_familias
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "cred_credito_familias"

_SERIES = {
    "endividamento_renda":      29037,
    "comp_renda_juros":         29033,
    "comp_renda_servico_total": 29034,
}

_bcb = BCB()


def run(n_meses: int = 24, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.cred_credito_familias.

    Args:
        n_meses: ultimos N meses (default 24). Ignorado se start/end fornecidos.
        start:   data inicial no formato "DD/MM/YYYY", ou "all" para serie completa.
        end:     data final no formato "DD/MM/YYYY". Default: hoje.
    """
    if start:
        df = _bcb.get_sgs(_SERIES, start=start, end=end)
    else:
        df = _bcb.get_sgs_ultimos(_SERIES, n=n_meses)

    insert_data_into_database(_DATABASE, _TABLE, df)
