"""
GDP - Contas Nacionais Trimestrais (PIB) - Taxas de variacao oficiais do IBGE

Agregado : 5932 (Taxa de variacao do indice de volume trimestral)
Variaveis: 6561 (interanual, NSA por construcao), 6562 (acumulada em 4 trimestres, NSA),
           6563 (acumulada ao longo do ano, NSA), 6564 (T/T imediatamente anterior, SA por construcao)
Banco    : macro_brasil.atv_pib_taxas

IBGE publica essas 4 taxas diretamente (nao sao um indice que precisa ser convertido em taxa por
quem consome) -- uma unica tabela sem dimensao de ajuste sazonal: cada taxa e por definicao NSA
(6561/6562/6563, todas "em relacao ao mesmo periodo do ano anterior" -- a sazonalidade se cancela
por construcao) ou SA (6564, "T/T imediatamente anterior" so faz sentido sobre a serie
dessazonalizada). Preferir esta tabela a computar as mesmas taxas em cima de atv_pib -- e a fonte
oficial, exatamente o que IBGE/BCB divulgam, sem qualquer aproximacao por razao de indice.

Indicador (coluna indicador, valores fixos):
  yoy      - Taxa trimestral em relacao ao mesmo periodo do ano anterior (%)
  acum_4t  - Taxa acumulada em quatro trimestres (%)
  acum_ano - Taxa acumulada ao longo do ano (%)
  qoq      - Taxa trimestre contra trimestre imediatamente anterior, dessazonalizada (%)
"""

from datetime import datetime

import pandas as pd

from connectors.ibge import IBGE
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "atv_pib_taxas"

# Mesmo dict de atv_pib.py -- ver atv_pib_encadeado.py para o motivo de duplicar em vez de importar.
_CATEGORIAS = {
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
    "90705": "valor_adicionado",
    "90706": "impostos_liquidos",
    "90707": "pib_pm",
    "93404": "consumo_familias",
    "93405": "consumo_adm_publica",
    "93406": "fbcf",
    "93407": "exportacao",
    "93408": "importacao",
}

_VARIAVEIS = {
    6561: "yoy",
    6562: "acum_4t",
    6563: "acum_ano",
    6564: "qoq",
}

_ibge = IBGE()


def run(years_back: int = 5, periodos=None) -> None:
    """Atualiza macro_brasil.atv_pib_taxas (4 taxas oficiais, todas as categorias).

    Args:
        years_back: anos anteriores ao ano atual (default 5).
                    Ignorado se periodos for fornecido.
        periodos:   qualquer formato aceito pelo connector IBGE (ver atv_pib.py).
    """
    if periodos is None:
        ano_fim  = datetime.now().year
        periodos = (ano_fim - years_back, ano_fim)

    df = _ibge.get(
        agregado=5932,
        variaveis=list(_VARIAVEIS),
        classificacoes={11255: [int(k) for k in _CATEGORIAS]},
        localidades={"N1": "all"},
        periodos=periodos,
    )
    df["name"]      = df["class_1_id"].map(_CATEGORIAS)
    df["indicador"] = df["variavel_id"].map(_VARIAVEIS)
    df = df[["date", "name", "indicador", "value"]]
    insert_data_into_database(_DATABASE, _TABLE, df)
