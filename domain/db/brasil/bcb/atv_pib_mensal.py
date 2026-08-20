"""
PIB mensal em R$ (BCB SGS 4380/4382)

Series SGS coletadas:
  pib_mensal    -- SGS 4380, "PIB mensal - valores correntes (R$ milhoes)"
  pib_acum_12m  -- SGS 4382, "PIB acumulado dos ultimos 12 meses - valores correntes
                   (R$ milhoes)" -- o mesmo denominador que o proprio BCB usa para
                   publicar `cred_credito_resumo.pct_pib_*` (confirmado ao vivo: saldo
                   / pib_acum_12m * 100 reproduz pct_pib_total_total exatamente, 55,76%
                   em 2026-06 nos dois casos).

Usado por analytics/brasil/credit/transforms.py's compute_pct_pib() para calcular "% do PIB"
para toda serie das abas Saldo/Concessao (nao so os totais agregados que ja vem prontos
em cred_credito_resumo) -- ver analytics/brasil/credit/CLAUDE.md.

Diferente de atv_pib_usd.py (SGS 4385, PIB mensal em dolar, alimenta o toggle % PIB de
analytics/brasil/exchange_rate/'s Balanco de Pagamentos) -- series/proposito separados, sem
relacao direta.

Banco: macro_brasil.atv_pib_mensal -- PRIMARY KEY (date, name)
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "atv_pib_mensal"

_SERIES = {
    "pib_mensal":   4380,
    "pib_acum_12m": 4382,
}

_bcb = BCB()


def run(n_meses: int = 36, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.atv_pib_mensal.

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
