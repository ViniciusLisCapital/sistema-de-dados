"""
Reservas internacionais do Brasil

Series SGS:
  3546 — Reservas internacionais — conceito liquidez (USD millions)

TODO: adicionar reservas_brutas_usd quando o codigo SGS correto for confirmado.
  - SGS 13127 retorna timeout consistente (serie pode nao existir nesse codigo)
  - BCB publica varios conceitos de reservas (caixa, liquidez, brutas)
  - Investigar via: https://www.bcb.gov.br/estatisticas/reservasinternacionais

Nota: A posicao de swap cambial do BCB nao esta disponivel no SGS.
Fonte alternativa: https://www4.bcb.gov.br/pom/demab/cronogramacambiais/vencdata.asp
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_cambio"
_TABLE    = "reservas"

_SERIES = {
    "reservas_liquidez_usd": 3546,
    # reservas_brutas_usd: codigo SGS pendente de confirmacao
}

_bcb = BCB()


def run(n_meses: int = 24, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_cambio.reservas.

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
