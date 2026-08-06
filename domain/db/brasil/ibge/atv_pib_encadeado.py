"""
GDP - Contas Nacionais Trimestrais (PIB) - Valores encadeados a precos de 1995

Agregados: 6612 (NSA), 6613 (SA)
Variaveis: 9318 (NSA), 9319 (SA) - valores encadeados a precos medios de 1995, em R$ milhoes
Banco    : macro_brasil.atv_pib_encadeado

Mesmas categorias de atv_pib.py (classificacao 11255), mas em R$ milhoes a precos de 1995 em vez
de indice de volume (base 1995=100). Este e o insumo oficial do IBGE para decomposicao/contribuicao
de crescimento (ver analytics/economic_activity/CLAUDE.md "Growth decomposition"): por serem valores
monetarios (nao indices com bases arbitrarias por categoria), sao aditivos entre categorias em
periodos proximos ao ano de referencia -- o que um indice de volume encadeado NAO e. Metodologia:
contribuicao_i (p.p.) = (valor_i,t - valor_i,t-n) / valor_PIB,t-n * 100, com n=1 para T/T (usa a
serie SA/6613) e n=4 para interanual (usa a serie NSA/6612). Mesma logica do metodo BEA "contribution
to percent change" e da nota metodologica de Contas Nacionais Trimestrais do IBGE; replicada tambem
pelo BCB/IPEA em seus proprios comentarios de conjuntura.

Gotcha: agregado 6613 (SA) NAO tem a categoria 90706 (Impostos liquidos sobre produtos) -- IBGE nao
publica essa serie dessazonalizada separadamente. atv_pib_encadeado_sa fica sem
'impostos_liquidos_sa'; qualquer decomposicao T/T da otica da oferta precisa tratar esse componente
como parte do residuo/discrepancia, nao como uma contribuicao isolada (ver
analytics/economic_activity/CLAUDE.md).
"""

from datetime import datetime

import pandas as pd

from connectors.ibge import IBGE
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "atv_pib_encadeado"

# Mesmo dict de atv_pib.py -- mantido duplicado aqui de proposito (mesmo padrao de
# domain/db/brasil/ibge/atv_pim.py / atv_pmc.py / atv_pms.py, cada script e independente).
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
        agregado:      6612 = NSA, 6613 = SA.
        variavel:      9318 = NSA, 9319 = SA.
        seasonal_adjs: indicador de ajuste sazonal gravado no banco. "N" ou "Y".
        periodos:      qualquer formato aceito pelo connector IBGE (ver atv_pib.py).

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
    """Atualiza macro_brasil.atv_pib_encadeado (NSA e SA).

    Args:
        years_back: anos anteriores ao ano atual (default 5).
                    Ignorado se periodos for fornecido.
        periodos:   qualquer formato aceito pelo connector IBGE (ver atv_pib.py).
    """
    if periodos is None:
        ano_fim  = datetime.now().year
        periodos = (ano_fim - years_back, ano_fim)

    nsa = _fetch(6612, 9318, "N", periodos)
    sa  = _fetch(6613, 9319, "Y", periodos)
    df  = pd.concat([nsa, sa], ignore_index=True)
    insert_data_into_database(_DATABASE, _TABLE, df)
