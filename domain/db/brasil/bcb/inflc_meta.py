"""
Meta para a inflacao (CMN), usada pela regra de Taylor e pela paridade do
poder de compra (PPC) no modelo agregado de pequeno porte do BCB — ver
analytics/monetary_policy/referencia/MODEL_REPLICATION_PLAN.md.

Serie SGS (anual):
  meta_inflacao 13521 — Meta para a inflacao

Codigo confirmado via chamada direta a api.bcb.gov.br/dados/serie/bcdata.sgs.13521
em 2026-07 (valores 3.50/2022, 3.25/2023, 3.00/2024-2026, consistentes com o
regime de metas continuas vigente desde 2025).

Banco: macro_brasil.inflc_meta — PRIMARY KEY (date, name)
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "inflc_meta"

_SERIES = {
    "meta_inflacao": 13521,
}

_bcb = BCB()


def run(start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.inflc_meta.

    Args:
        start: data inicial "DD/MM/YYYY", ou "all" para serie completa (desde 1999).
        end:   data final "DD/MM/YYYY". Default: hoje.
    """
    start = "01/01/1999" if start == "all" else (start or "01/01/1999")
    df = _bcb.get_sgs(_SERIES, start=start, end=end)
    insert_data_into_database(_DATABASE, _TABLE, df)
