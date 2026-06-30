"""
Taxa de Cambio Efetiva Real (REER) — BIS Statistics API.

Paises acompanhados: BR, MX, CL, CO
Tipos: real_broad, nominal_broad

Banco: macro_international.reer
Schema: PRIMARY KEY (date, country_code, reer_type)
"""

from connectors.bis import BIS
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_international"
_TABLE    = "reer"

_COUNTRIES = ["BR", "MX", "CL", "CO"]
_TYPES     = [("R", "B"), ("N", "B")]  # real_broad, nominal_broad

_bis = BIS()


def run(start: str | None = None) -> None:
    """Atualiza macro_international.reer com REER do BIS.

    Args:
        start: "YYYY-MM" para filtrar a partir dessa data, ou None para serie completa.
               Default None busca toda a historia disponivel.
    """
    df = _bis.get_eer(countries=_COUNTRIES, types=_TYPES, start=start)
    insert_data_into_database(_DATABASE, _TABLE, df)
