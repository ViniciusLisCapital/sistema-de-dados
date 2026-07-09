"""
IBC-Br - Indice de Atividade Economica do Banco Central

Series SGS coletadas (12 series — NSA e SA por componente):
  Total      : ibcbr_nsa (24363), ibcbr_sa (24364)
  Agropecuaria: ibcbr_agropecuaria_nsa (29601), ibcbr_agropecuaria_sa (29602)
  Industria  : ibcbr_industria_nsa (29603), ibcbr_industria_sa (29604)
  Servicos   : ibcbr_servicos_nsa (29605), ibcbr_servicos_sa (29606)
  Ex-Agrop.  : ibcbr_ex_agropecuaria_nsa (29607), ibcbr_ex_agropecuaria_sa (29608)
  Impostos   : ibcbr_impostos_nsa (29609), ibcbr_impostos_sa (29610)

Banco: macro_brasil.atv_ibcbr
Nota : seasonal_adjs derivado do sufixo do nome (_sa -> 'Y', _nsa -> 'N').
"""

from datetime import datetime, timedelta

import pandas as pd

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "atv_ibcbr"

_SERIES = {
    "ibcbr_nsa":              24363,
    "ibcbr_sa":               24364,
    "ibcbr_agropecuaria_nsa": 29601,
    "ibcbr_agropecuaria_sa":  29602,
    "ibcbr_industria_nsa":    29603,
    "ibcbr_industria_sa":     29604,
    "ibcbr_servicos_nsa":     29605,
    "ibcbr_servicos_sa":      29606,
    "ibcbr_ex_agropecuaria_nsa": 29607,
    "ibcbr_ex_agropecuaria_sa":  29608,
    "ibcbr_impostos_nsa":     29609,
    "ibcbr_impostos_sa":      29610,
}

_bcb = BCB()


def run(n_meses: int = 36, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.atv_ibcbr.

    Args:
        n_meses: ultimos N meses (default 36). Ignorado se start fornecido.
        start:   data inicial no formato "DD/MM/YYYY", ou "all" para serie completa.
        end:     data final no formato "DD/MM/YYYY". Default: hoje.
    """
    if start:
        df = _bcb.get_sgs(_SERIES, start=start, end=end)
    else:
        df = _bcb.get_sgs_ultimos(_SERIES, n=n_meses)

    df["seasonal_adjs"] = df["name"].str.endswith("_sa").map({True: "Y", False: "N"})
    insert_data_into_database(_DATABASE, _TABLE, df)
