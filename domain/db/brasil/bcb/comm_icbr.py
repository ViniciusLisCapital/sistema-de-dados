"""
IC-Br (Indice de Commodities - Brasil) e seus sub-indices setoriais.

Insumo do modelo agregado de pequeno porte do BCB (curva de Phillips de
precos livres) — ver analytics/monetary_policy/referencia/MODEL_REPLICATION_PLAN.md.

Series SGS (mensal, desde 1998-02):
  icbr_geral        27574 — IC-Br geral
  icbr_agropecuaria 27575 — IC-Br Agropecuaria
  icbr_metal        27576 — IC-Br Metal
  icbr_energia      27577 — IC-Br Energia

Codigos confirmados via chamada direta a api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}
(nao apenas por busca/memoria) em 2026-07 — ver historico de bugs de codigo SGS
errado em cmb_balanco_pagmt (CAMBIO.md) que motivou essa verificacao.

Banco: macro_brasil.comm_icbr — PRIMARY KEY (date, name)
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "comm_icbr"

_SERIES = {
    "icbr_geral":        27574,
    "icbr_agropecuaria": 27575,
    "icbr_metal":        27576,
    "icbr_energia":      27577,
}

_bcb = BCB()


def run(start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.comm_icbr.

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
