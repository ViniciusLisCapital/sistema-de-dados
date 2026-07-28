"""
Taxa de juros de politica monetaria (short-term/policy rate) — BIS Statistics
API (WS_CBPOL, Central Bank Policy Rates).

Paises acompanhados: BR, MX, CL, CO, PE, AR
Frequencia: diaria (end of period) — o dado mensal do BIS e apenas o
fechamento do mes da propria serie diaria, entao so a diaria e armazenada.

Nota: Argentina (AR) parou de ser atualizada pelo BIS em meados de 2025 —
gap esperado no final da serie, nao e falha do script.

Brasil (BR) e truncado em 1994-07-01 (Plano Real) por decisao explicita do
usuario — o BIS cobre desde 1986-06, mas o periodo de hiperinflacao anterior
(taxa chega a ~790.799% a.a. em 1990) nao e comparavel/util para analise.

Banco: macro_international.cmb_policy_rates
Schema: PRIMARY KEY (date, country_code)
"""

from connectors.bis import BIS
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_international"
_TABLE    = "cmb_policy_rates"

_COUNTRIES = ["BR", "MX", "CL", "CO", "PE", "AR"]

_BR_START = "1994-07-01"

_bis = BIS()


def run(start: str | None = None) -> None:
    """Atualiza macro_international.cmb_policy_rates com policy rates do BIS.

    Args:
        start: "YYYY-MM-DD" para filtrar a partir dessa data, ou None para serie completa.
               Default None busca toda a historia disponivel. Brasil e sempre
               truncado em 1994-07-01, mesmo se start for anterior a isso.
    """
    df = _bis.get_policy_rates(countries=_COUNTRIES, freq="D", start=start)
    df = df[~((df["country_code"] == "BR") & (df["date"] < _BR_START))]
    insert_data_into_database(_DATABASE, _TABLE, df)
