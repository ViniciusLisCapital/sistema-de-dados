"""
Termos de troca do Brasil

Series SGS:
  22099 — Termos de troca (indice, serie A)
  22100 — Termos de troca (indice, serie B)

Banco: macro_brasil.termos_de_troca

Nota: Verificar as descricoes exatas de cada serie na BCB SGS — os dois indices
podem representar metodologias distintas (ex: FOB vs CIF, ou diferentes cestas).
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "termos_de_troca"

_SERIES = {
    "termos_de_troca_a": 22099,
    "termos_de_troca_b": 22100,
}

_bcb = BCB()


def run(n_meses: int = 36, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.termos_de_troca.

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
