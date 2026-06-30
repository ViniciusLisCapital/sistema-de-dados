"""
Fluxo cambial do Brasil (Nota Cambial BCB)

Series SGS (valores em USD billions — confirmar unidade na BCB SGS):
  24352 — Fluxo cambial total — saldo
  24370 — Fluxo cambial total — entrada (gross inflows)
  24371 — Fluxo cambial total — saida  (gross outflows)
  24364 — Setor comercial — entrada (exportadores)
  24363 — Setor comercial — saida  (importadores)
  24369 — Setor financeiro — saldo

Banco: macro_brasil.fluxo_cambial

Nota: A BCB publica o fluxo cambial com maior granularidade (CEP/CBE sub-itens)
na Nota Cambial semanal. Os codigos SGS para esse nivel de detalhe nao foram
identificados com certeza na fase de pesquisa. Adicionar quando confirmados.

Nota 2: 24366 (setor comercial saldo) retornou timeout na pesquisa — pode ser
que o codigo exista; reprocessar futuramente. O saldo comercial pode ser derivado
como (entrada - saida) se necessario.
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "fluxo_cambial"

_SERIES = {
    # Total
    "total_saldo":          24352,
    "total_entrada":        24370,
    "total_saida":          24371,
    # Setor comercial
    "comercial_entrada":    24364,
    "comercial_saida":      24363,
    # Setor financeiro
    "financeiro_saldo":     24369,
}

_bcb = BCB()


def run(n_meses: int = 36, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.fluxo_cambial.

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
