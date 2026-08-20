"""
Indicadores de condicoes financeiras das familias (BCB/SGS)

Series SGS coletadas (5 series — endividamento e servico da divida em % da renda):
  29037 - Endividamento das familias / renda acumulada (12 meses)
  29038 - Endividamento das familias sem financiamento imobiliario / renda acumulada (12 meses)
  29033 - Comprometimento da renda com juros
  29034 - Comprometimento da renda com servico da divida (juros + amortizacao)
  29035 - Comprometimento da renda com servico da divida, sem financiamento imobiliario

  As duas ultimas (endividamento_sem_imob/comp_renda_servico_sem_imob) completam a
  Tabela 27 da publicacao "Tabelas de Estatisticas Monetarias e de Credito" do BCB (ver
  analytics/brasil/credit/fontes_dados.md) -- as outras 2 series dessa tabela (endividamento_
  renda=29037, comp_renda_servico_total=29034) ja estavam aqui desde a primeira versao
  deste script. comp_renda_juros (29033) e uma serie SGS avulsa do mesmo tema, nao faz
  parte da Tabela 27.

  Fonte: Nota de Credito do BCB

Banco: macro_brasil.cred_credito_familias
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "cred_credito_familias"

_SERIES = {
    "endividamento_renda":            29037,
    "endividamento_sem_imob":         29038,
    "comp_renda_juros":               29033,
    "comp_renda_servico_total":       29034,
    "comp_renda_servico_sem_imob":    29035,
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
