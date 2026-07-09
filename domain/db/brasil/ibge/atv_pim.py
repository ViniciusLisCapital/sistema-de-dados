"""
PIM - Pesquisa Industrial Mensal (Producao Fisica)

Agregado : 8888
Variaveis: 12606 (NSA), 12607 (SA)
Banco    : macro_brasil.atv_pim

Categorias coletadas (classificacao 544):
  129314 - Industria geral      -> industria_geral
  129315 - Industrias extrativas -> ind_extrativas
  129316 - Ind. de transformacao -> ind_transformacao
"""

from datetime import datetime

import pandas as pd

from connectors.ibge import IBGE
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "atv_pim"

_CATEGORIAS = {
    "129314": "industria_geral",
    "129315": "ind_extrativas",
    "129316": "ind_transformacao",
}

_ibge = IBGE()

def _fetch(variavel: int, seasonal_adjs: str, periodos) -> pd.DataFrame:
    """Busca uma variável do PIM e retorna DataFrame pronto para inserção.

    Args:
        variavel:     ID da variável IBGE. 12606 = NSA, 12607 = SA.
        seasonal_adjs: indicador de ajuste sazonal gravado no banco. "N" ou "Y".
        periodos:     período de busca — qualquer formato aceito pelo connector:
                        "202001-202412"  range explícito (YYYYMM-YYYYMM)
                        (2020, 2024)     tupla de anos
                        "last:36"        últimos N períodos
                        "all"            série histórica completa

    Returns:
        DataFrame com colunas: date, name, value, seasonal_adjs.
    """
    df = _ibge.get(
        agregado=8888,
        variaveis=variavel,
        classificacoes={544: [int(k) for k in _CATEGORIAS]},
        localidades={"N1": "all"},
        periodos=periodos,
    )
    df["name"]          = df["class_1_id"].map(_CATEGORIAS)
    df["seasonal_adjs"] = seasonal_adjs
    return df[["date", "name", "value", "seasonal_adjs"]]

def run(years_back: int = 2, periodos=None) -> None:
    """Atualiza macro_brasil.atv_pim.

    Args:
        years_back: anos anteriores ao ano atual (default 2).
                    Ignorado se periodos for fornecido.
        periodos:   qualquer formato aceito pelo connector IBGE:
                      "202001-202412"  range explícito
                      (2020, 2024)     tupla de anos
                      "last:36"        últimos N períodos
                      "all"            série histórica completa
    """
    if periodos is None:
        ano_fim  = datetime.now().year
        periodos = (ano_fim - years_back, ano_fim)

    nsa = _fetch(12606, "N", periodos)
    sa  = _fetch(12607, "Y", periodos)
    df  = pd.concat([nsa, sa], ignore_index=True)
    insert_data_into_database(_DATABASE, _TABLE, df)


