"""
GDP - Contas Nacionais Trimestrais (PIB)

Agregados: 1620 (NSA), 1621 (SA)
Variaveis: 583 (NSA), 584 (SA) - serie encadeada do indice de volume trimestral
Banco    : macro_brasil.atv_pib

Categorias coletadas (classificacao 11255):
  Otica Oferta  : agropecuaria, industria, servicos e subcomponentes
  Otica Demanda : consumo_familias, consumo_adm_publica, fbcf, exportacao, importacao
  Agregados     : pib_pm, valor_adicionado, impostos_liquidos
"""

from datetime import datetime

import pandas as pd

from connectors.ibge import IBGE
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "atv_pib"

_CATEGORIAS = {
    # Otica Oferta
    "90687": "agropecuaria",
    "90691": "industria",
    "90692": "ind_extrativas",
    "90693": "ind_transformacao",
    "90695": "eletricidade_gas_agua",
    "90694": "construcao",
    "90696": "servicos",
    "90697": "comercio",
    "90698": "transporte_correio",
    "90699": "informacao_comunicacao",
    "90700": "financeiras_seguros",
    "90702": "imobiliarias",
    "90701": "outros_servicos",
    "90703": "adm_saude_educacao_pub",
    # Agregados
    "90705": "valor_adicionado",
    "90706": "impostos_liquidos",
    "90707": "pib_pm",
    # Otica Demanda
    "93404": "consumo_familias",
    "93405": "consumo_adm_publica",
    "93406": "fbcf",
    "93407": "exportacao",
    "93408": "importacao",
}

_ibge = IBGE()


def _fetch(agregado: int, variavel: int, seasonal_adjs: str, periodos) -> pd.DataFrame:
    """Busca uma variavel das Contas Nacionais e retorna DataFrame pronto para insercao.

    Args:
        agregado:      1620 = NSA, 1621 = SA.
        variavel:      583 = NSA, 584 = SA.
        seasonal_adjs: indicador de ajuste sazonal gravado no banco. "N" ou "Y".
        periodos:      qualquer formato aceito pelo connector IBGE:
                         "200101-202504"  range explicito (YYYYQQ)
                         (2015, 2024)     tupla de anos
                         "last:20"        ultimos N trimestres
                         "all"            serie historica completa

    Returns:
        DataFrame com colunas: date, name, value, seasonal_adjs.
    """
    df = _ibge.get(
        agregado=agregado,
        variaveis=variavel,
        classificacoes={11255: [int(k) for k in _CATEGORIAS]},
        localidades={"N1": "all"},
        periodos=periodos,
    )
    df["name"]          = df["class_1_id"].map(_CATEGORIAS)
    df["seasonal_adjs"] = seasonal_adjs
    return df[["date", "name", "value", "seasonal_adjs"]]


def run(years_back: int = 5, periodos=None) -> None:
    """Atualiza macro_brasil.atv_pib (NSA e SA).

    Args:
        years_back: anos anteriores ao ano atual (default 5).
                    Ignorado se periodos for fornecido.
        periodos:   qualquer formato aceito pelo connector IBGE:
                      "200101-202504"  range explicito
                      (2015, 2024)     tupla de anos
                      "last:20"        ultimos N trimestres
                      "all"            serie historica completa
    """
    if periodos is None:
        ano_fim  = datetime.now().year
        periodos = (ano_fim - years_back, ano_fim)

    nsa = _fetch(1620, 583, "N", periodos)
    sa  = _fetch(1621, 584, "Y", periodos)
    df  = pd.concat([nsa, sa], ignore_index=True)
    insert_data_into_database(_DATABASE, _TABLE, df)
