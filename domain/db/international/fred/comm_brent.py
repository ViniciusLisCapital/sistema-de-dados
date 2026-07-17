"""
Petroleo tipo Brent (USD/barril) — insumo de cenario de choque de
commodities no modelo agregado de pequeno porte do BCB (isolado do IC-Br
Energia, que ja embute a variacao cambial) — ver
analytics/monetary_policy/referencia/MODEL_REPLICATION_PLAN.md.

Serie FRED (diaria):
  brent_usd DCOILBRENTEU — Crude Oil Prices: Brent - Europe

Colocado em macro_international (nao macro_brasil) por nao ser especifico do
Brasil — mesma logica aplicada ao IC-Br (esse sim especifico do Brasil, em
BRL, publicado pelo BCB) e ao Oceanic Nino Index (clima_oni).

Banco: macro_international.comm_brent — PRIMARY KEY (date, name)
"""

from connectors.fred import FredUniFrame
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_international"
_TABLE    = "comm_brent"


def run(start: str = "1990-01-01", end: str | None = None) -> None:
    """Atualiza macro_international.comm_brent.

    Args:
        start: data inicial ISO "YYYY-MM-DD". Default: serie completa.
        end:   data final ISO "YYYY-MM-DD". Default: hoje.
    """
    from datetime import datetime
    end = end or datetime.now().strftime("%Y-%m-%d")

    df = FredUniFrame("brent_usd", "DCOILBRENTEU", start, end)
    df.columns = ["date", "value"]
    df["name"] = "brent_usd"
    df = df[["date", "name", "value"]].dropna(subset=["value"])

    insert_data_into_database(_DATABASE, _TABLE, df)
