"""
Indice do dolar contra moedas de mercados emergentes — proxy de forca do
dolar especifico contra a cesta EM (nao e o mesmo basket da DXY/ICE, que e
dominada por moedas de paises desenvolvidos — EUR, JPY, GBP, CAD, SEK, CHF).

Serie FRED (diaria):
  dxy_em DTWEXEMEGS — Nominal Emerging Market Economies U.S. Dollar Index
                       (base Jan/2006=100)

Colocado em macro_international (nao macro_brasil) pela mesma logica aplicada
a cmb_dollar_index — nao e dado especifico do Brasil.

Banco: macro_international.cmb_dollar_index_em — PRIMARY KEY (date, name)
"""

from connectors.fred import FredUniFrame
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_international"
_TABLE    = "cmb_dollar_index_em"


def run(start: str = "2006-01-01", end: str | None = None) -> None:
    """Atualiza macro_international.cmb_dollar_index_em.

    Args:
        start: data inicial ISO "YYYY-MM-DD". Default: serie completa (inicio do FRED).
        end:   data final ISO "YYYY-MM-DD". Default: hoje.
    """
    from datetime import datetime
    end = end or datetime.now().strftime("%Y-%m-%d")

    df = FredUniFrame("dxy_em", "DTWEXEMEGS", start, end)
    df.columns = ["date", "value"]
    df["name"] = "dxy_em"
    df = df[["date", "name", "value"]].dropna(subset=["value"])

    insert_data_into_database(_DATABASE, _TABLE, df)
