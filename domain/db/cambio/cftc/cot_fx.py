"""
Posicionamento especulativo em futuros de moedas — CFTC TFF (Traders in Financial Futures).

Moedas: BRL, MXN (bem cobertos); CLP, COP (esparsos — pode nao aparecer todos os anos)

Series armazenadas (campo 'name'):
  open_interest  — Contratos em aberto (total)
  lev_long       — Posicao comprada: Leveraged Money (fundos especulativos)
  lev_short      — Posicao vendida: Leveraged Money
  lev_net        — Posicao liquida: lev_long - lev_short
  nonrept_long   — Posicao comprada: Nao-reportaveis
  nonrept_short  — Posicao vendida: Nao-reportaveis

Banco: macro_cambio.cot_fx
Schema: PRIMARY KEY (date, currency, name)
"""

from datetime import datetime

from connectors.cftc import CFTC
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_cambio"
_TABLE    = "cot_fx"

# CLP and COP do not appear in CFTC TFF file (no CME FX futures for these)
_CONTRACT_NAMES = [
    "BRAZILIAN REAL",
    "MEXICAN PESO",
]

_cftc = CFTC()


def run(years: list[int] | None = None, n_anos: int = 3) -> None:
    """Atualiza macro_cambio.cot_fx com posicionamento COT de moedas.

    Args:
        years:  Lista de anos a buscar. Se None, usa os ultimos n_anos incluindo o atual.
        n_anos: Quantos anos buscar quando years=None (default 3).
    """
    if years is None:
        current = datetime.now().year
        years = list(range(current - n_anos + 1, current + 1))

    df = _cftc.get_cot_fx(contract_names=_CONTRACT_NAMES, years=years)
    insert_data_into_database(_DATABASE, _TABLE, df)
