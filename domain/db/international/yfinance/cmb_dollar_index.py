"""
Indice do dolar (DXY) — proxy de forca do dolar contra uma cesta de moedas
(EUR, JPY, GBP, CAD, SEK, CHF), usado como insumo de contexto cambial (nao e
especifico do Brasil).

Serie Yahoo Finance (diaria, fechamento):
  dxy DX-Y.NYB — ICE US Dollar Index

Preferido ao FRED DTWEXBGS (Nominal Broad U.S. Dollar Index) por ter historico
desde 1971 — o FRED so cobre a partir de 2006-01-02 na formulacao atual.

Colocado em macro_international (nao macro_brasil) pela mesma logica aplicada
a comm_brent e clima_oni — nao e dado especifico do Brasil.

Banco: macro_international.cmb_dollar_index — PRIMARY KEY (date, name)
"""

from connectors.yfinance import get_history
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_international"
_TABLE    = "cmb_dollar_index"
_TICKER   = "DX-Y.NYB"


def run(start: str = "1971-01-01", end: str | None = None) -> None:
    """Atualiza macro_international.cmb_dollar_index.

    Args:
        start: data inicial ISO "YYYY-MM-DD". Default: serie completa (inicio do Yahoo Finance).
        end:   data final ISO "YYYY-MM-DD". Default: hoje.
    """
    df = get_history(_TICKER, start=start, end=end)
    df["name"] = "dxy"
    df = df[["date", "name", "value"]].dropna(subset=["value"])

    insert_data_into_database(_DATABASE, _TABLE, df)
