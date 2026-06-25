"""
PMC - Pesquisa Mensal de Comercio

Agregados:
  8880 - Comercio varejista restrito  (totais)
  8881 - Comercio varejista ampliado  (totais)
  8883 - Comercio varejista ampliado  (por segmento)
Variaveis: 7169 (NSA), 7170 (SA) - indice de volume de vendas
Banco    : brasil.pmc
"""

from datetime import datetime

import pandas as pd

from connectors.ibge import IBGE
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "pmc"

# Segmentos de varejo (classificacao 85, agregado 8883)
_SEGMENTOS = {
    "90671":  "combustiveis_lubrificantes",
    "90672":  "hiper_super_alim_bebidas_fumo",
    "103154": "hipermercados_supermercados",
    "90673":  "tecidos_vestuario_calcados",
    "2759":   "moveis_eletrodomesticos",
    "31555":  "moveis",
    "31556":  "eletrodomesticos",
    "103155": "farma_medicos_perfumaria",
    "103156": "livros_jornais_papelaria",
    "103157": "equip_escritorio_informatica",
    "103158": "outros_artigos_pessoal_domest",
    "103159": "veiculos_motocicletas_pecas",
    "2762":   "material_construcao",
    "56741":  "atacado_alim_bebidas_fumo",
}

_ibge = IBGE()


def _fetch_segmentos(variavel: int, seasonal_adjs: str, periodos) -> pd.DataFrame:
    """Busca indice de volume por segmento do comercio varejista ampliado (8883).

    Args:
        variavel:      7169 = NSA, 7170 = SA.
        seasonal_adjs: indicador de ajuste sazonal gravado no banco. "N" ou "Y".
        periodos:      qualquer formato aceito pelo connector IBGE.

    Returns:
        DataFrame com colunas: date, name, value, seasonal_adjs.
        O campo name contem o nome curto do segmento (ex.: combustiveis_lubrificantes).
    """
    df = _ibge.get(
        agregado=8883,
        variaveis=variavel,
        classificacoes={
            11046: [56736],                     # filtro: volume de vendas ampliado
            85:    [int(k) for k in _SEGMENTOS],
        },
        localidades={"N1": "all"},
        periodos=periodos,
    )
    # class_1 = 11046 (tipo de indice), class_2 = 85 (segmento)
    df["name"]          = df["class_2_id"].map(_SEGMENTOS)
    df["seasonal_adjs"] = seasonal_adjs
    return df[["date", "name", "value", "seasonal_adjs"]]


def _fetch_total(agregado: int, cat_id: int, nome: str,
                 variavel: int, seasonal_adjs: str, periodos) -> pd.DataFrame:
    """Busca indice de volume total do comercio (restrito ou ampliado).

    Args:
        agregado:      8880 = restrito, 8881 = ampliado.
        cat_id:        56734 = volume restrito, 56736 = volume ampliado.
        nome:          nome curto gravado no banco (ex.: comercio_restrito_total).
        variavel:      7169 = NSA, 7170 = SA.
        seasonal_adjs: indicador de ajuste sazonal gravado no banco. "N" ou "Y".
        periodos:      qualquer formato aceito pelo connector IBGE.

    Returns:
        DataFrame com colunas: date, name, value, seasonal_adjs.
    """
    df = _ibge.get(
        agregado=agregado,
        variaveis=variavel,
        classificacoes={11046: [cat_id]},
        localidades={"N1": "all"},
        periodos=periodos,
    )
    df["name"]          = nome
    df["seasonal_adjs"] = seasonal_adjs
    return df[["date", "name", "value", "seasonal_adjs"]]


def run(years_back: int = 3, periodos=None) -> None:
    """Atualiza brasil.pmc (segmentos + totais restrito e ampliado, NSA e SA).

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

    frames = [
        # Segmentos ampliado
        _fetch_segmentos(7169, "N", periodos),
        _fetch_segmentos(7170, "Y", periodos),
        # Total comercio restrito
        _fetch_total(8880, 56734, "comercio_restrito_total", 7169, "N", periodos),
        _fetch_total(8880, 56734, "comercio_restrito_total", 7170, "Y", periodos),
        # Total comercio ampliado
        _fetch_total(8881, 56736, "comercio_ampliado_total", 7169, "N", periodos),
        _fetch_total(8881, 56736, "comercio_ampliado_total", 7170, "Y", periodos),
    ]
    df = pd.concat(frames, ignore_index=True)
    insert_data_into_database(_DATABASE, _TABLE, df)