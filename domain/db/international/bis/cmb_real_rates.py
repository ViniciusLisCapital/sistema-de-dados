"""
Taxa real de juros ex-post (policy rate - CPI YoY) — BIS Statistics API,
combinando WS_CBPOL (policy rate, mensal) e WS_LONG_CPI (CPI, variacao YoY).

Paises acompanhados: BR, MX, CL, CO, PE (Argentina excluida — BIS parou de
atualizar seu policy rate em meados de 2025, ver cmb_policy_rates.py).

Cada pais so tem dado a partir do inicio da sua propria serie de policy rate
no BIS (o fator limitante — o CPI do BIS cobre um periodo muito mais longo
para todos eles): BR 1994-07 (truncado por decisao do usuario, Plano Real,
mesmo criterio de cmb_policy_rates.py), CO 1995-04, CL 1997-02, MX 1998-11,
PE 2003-09.

Nota: Brasil ja tem uma serie de taxa real (Selic - IPCA) em
macro_international.diferenciais_juros, calculada com dados oficiais BCB
(Selic meta + IPCA 12m). Esta tabela recalcula BR com a mesma fonte/metodo
do BIS usada para os outros 4 paises, para comparabilidade cross-country
homogenea — nao substitui diferenciais_juros.

Banco: macro_international.cmb_real_rates
Schema: PRIMARY KEY (date, country_code, name)
  name in (policy_rate, cpi_yoy, real_rate_ex_post)
"""

import pandas as pd

from connectors.bis import BIS
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_international"
_TABLE    = "cmb_real_rates"

_COUNTRIES = ["BR", "MX", "CL", "CO", "PE"]
_BR_START = "1994-07"

_bis = BIS()


def run(start: str | None = None) -> None:
    """Atualiza macro_international.cmb_real_rates com taxa real ex-post do BIS.

    Args:
        start: "YYYY-MM" para filtrar a partir dessa data, ou None para serie
               completa. Default None busca toda a historia disponivel por
               pais (limitada pelo inicio do policy rate de cada um — ver
               docstring do modulo). Brasil e sempre truncado em 1994-07,
               mesmo se start for anterior a isso.
    """
    policy_df = _bis.get_policy_rates(countries=_COUNTRIES, freq="M", start=start)
    policy_df = policy_df[~((policy_df["country_code"] == "BR") & (policy_df["date"] < _BR_START))]
    policy_df = policy_df.rename(columns={"value": "policy_rate"})

    cpi_df = _bis.get_cpi(countries=_COUNTRIES, unit="yoy", start=start)
    cpi_df = cpi_df.rename(columns={"value": "cpi_yoy"})

    df = pd.merge(policy_df, cpi_df, on=["date", "country_code"], how="inner")
    df["real_rate_ex_post"] = df["policy_rate"] - df["cpi_yoy"]

    df_tidy = (
        df.melt(
            id_vars=["date", "country_code"],
            value_vars=["policy_rate", "cpi_yoy", "real_rate_ex_post"],
            var_name="name",
            value_name="value",
        )
        .dropna(subset=["value"])
    )

    insert_data_into_database(_DATABASE, _TABLE, df_tidy)
