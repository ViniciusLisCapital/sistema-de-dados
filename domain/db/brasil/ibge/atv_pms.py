"""
PMS - Pesquisa Mensal de Servicos

Agregado : 8688
Variaveis: 7167 (NSA), 7168 (SA) - indice de volume de servicos
Banco    : macro_brasil.atv_pms

Categorias coletadas (classificacao 12355):
  Grupos principais: familias, informacao/comunicacao, prof/adm, transportes, outros
  Subcomponentes de cada grupo
"""

from datetime import datetime

import pandas as pd

from connectors.ibge import IBGE
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "atv_pms"

_CATEGORIAS = {
    "107071": "servicos_total",
    # Servicos prestados as familias
    "106869": "servicos_familias",
    "106870": "alojamento_alimentacao",
    "56692":  "alojamento",
    "56693":  "alimentacao",
    "31396":  "outros_servicos_familias",
    # Informacao e comunicacao
    "106874": "informacao_comunicacao",
    "31397":  "tic",
    "39321":  "telecomunicacoes",
    "39322":  "servicos_ti",
    "31398":  "audiovisual_edicao_noticias",
    # Profissionais, administrativos e complementares
    "31399":  "prof_adm_complementares",
    "31400":  "servicos_tecnico_profissionais",
    "31421":  "servicos_adm_complementares",
    "56694":  "alugueis_nao_imobiliarios",
    "56695":  "apoio_atividades_empresariais",
    # Transportes e correio
    "106876": "transportes_correio",
    "31422":  "transporte_terrestre",
    "56696":  "rodoviario_cargas",
    "56697":  "rodoviario_passageiros",
    "56698":  "outros_transporte_terrestre",
    "31423":  "transporte_aquaviario",
    "31424":  "transporte_aereo",
    "31425":  "armazenagem_aux_transportes_correio",
    # Outros servicos
    "31426":  "outros_servicos",
    "56699":  "esgoto_gestao_residuos",
    "56700":  "ativ_aux_financeiras",
    "56701":  "imobiliarias",
    "56702":  "outros_nao_especificados",
}

_ibge = IBGE()


def _fetch(variavel: int, seasonal_adjs: str, periodos) -> pd.DataFrame:
    """Busca uma variavel do PMS e retorna DataFrame pronto para insercao.

    Args:
        variavel:      7167 = NSA, 7168 = SA.
        seasonal_adjs: indicador de ajuste sazonal gravado no banco. "N" ou "Y".
        periodos:      qualquer formato aceito pelo connector IBGE:
                         "202001-202412"  range explicito
                         (2020, 2024)     tupla de anos
                         "last:36"        ultimos N periodos
                         "all"            serie historica completa

    Returns:
        DataFrame com colunas: date, name, value, seasonal_adjs.
        O campo name contem o nome curto do grupo/subcomponente de servicos.
    """
    df = _ibge.get(
        agregado=8688,
        variaveis=variavel,
        classificacoes={
            11046: [56726],                       # filtro: volume de servicos
            12355: [int(k) for k in _CATEGORIAS],
        },
        localidades={"N1": "all"},
        periodos=periodos,
    )
    # class_1 = 11046 (tipo de indice), class_2 = 12355 (grupo de servico)
    df["name"]          = df["class_2_id"].map(_CATEGORIAS)
    df["seasonal_adjs"] = seasonal_adjs
    return df[["date", "name", "value", "seasonal_adjs"]]


def run(years_back: int = 3, periodos=None) -> None:
    """Atualiza macro_brasil.atv_pms (NSA e SA, todos os grupos e subcomponentes).

    Args:
        years_back: anos anteriores ao ano atual (default 3).
                    Ignorado se periodos for fornecido.
        periodos:   qualquer formato aceito pelo connector IBGE:
                      "202001-202412"  range explicito
                      (2020, 2024)     tupla de anos
                      "last:36"        ultimos N periodos
                      "all"            serie historica completa
    """
    if periodos is None:
        ano_fim  = datetime.now().year
        periodos = (ano_fim - years_back, ano_fim)

    nsa = _fetch(7167, "N", periodos)
    sa  = _fetch(7168, "Y", periodos)
    df  = pd.concat([nsa, sa], ignore_index=True)
    insert_data_into_database(_DATABASE, _TABLE, df)
