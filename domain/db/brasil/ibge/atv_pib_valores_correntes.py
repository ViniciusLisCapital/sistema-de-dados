"""
GDP - Contas Nacionais Trimestrais (PIB) - Valores a precos correntes

Agregado : 1846 (Valores a precos correntes)
Variavel : 585 - R$ milhoes, sem ajuste sazonal (nao existe variante SA para este agregado)
Banco    : macro_brasil.atv_pib_valores_correntes

Mesmas 22 categorias de atv_pib.py (classificacao 11255) mais uma exclusiva desta tabela:
"Variacao de estoque" (102880) -- a unica categoria da demanda que o IBGE NUNCA publica como
indice de volume (nem em atv_pib, nem em nenhum outro agregado de indice/taxa), porque um indice
nao faz sentido para uma serie que muda de sinal. So existe em valor corrente.

Uso: esta tabela e o insumo para o peso anual (nominal_i[ano y-1] / nominal_PIB[ano y-1]) usado no
metodo "alternativo ad hoc" da Nota Tecnica do Banco Central do Brasil no. 46 (Thiago Trafane
Oliveira Santos, ago/2018) para decompor a contribuicao de cada componente ao crescimento
trimestral do PIB -- ver analytics/brasil/economic_activity/CLAUDE.md "PIB tab methodology". O peso e
somado por ano civil (4 trimestres) a partir desta serie NSA; a taxa de crescimento real de cada
componente vem de atv_pib_taxas, nao desta tabela.

Substituiu atv_pib_encadeado.py (removida): aquela usava valores encadeados a precos FIXOS de
1995, uma base cada vez mais defasada (30 anos em 2026) -- a NT-46 do BCB usa peso nominal do ano
civil ANTERIOR (rolante, nunca mais que ~1 ano defasado), nao um ano fixo de referencia. Ver
CLAUDE.md Gotchas para a comparacao empirica entre os dois metodos.
"""

from datetime import datetime

import pandas as pd

from connectors.ibge import IBGE
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "atv_pib_valores_correntes"

# Mesmo dict de atv_pib.py (ver atv_pib_taxas.py para o motivo de duplicar em vez de importar) mais
# "variacao_estoque" (102880), exclusiva desta tabela.
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
    "102880": "variacao_estoque",
    "93407": "exportacao",
    "93408": "importacao",
}

_ibge = IBGE()


def run(years_back: int = 5, periodos=None) -> None:
    """Atualiza macro_brasil.atv_pib_valores_correntes.

    Args:
        years_back: anos anteriores ao ano atual (default 5).
                    Ignorado se periodos for fornecido.
        periodos:   qualquer formato aceito pelo connector IBGE (ver atv_pib.py).
    """
    if periodos is None:
        ano_fim  = datetime.now().year
        periodos = (ano_fim - years_back, ano_fim)

    df = _ibge.get(
        agregado=1846,
        variaveis=585,
        classificacoes={11255: [int(k) for k in _CATEGORIAS]},
        localidades={"N1": "all"},
        periodos=periodos,
    )
    df["name"] = df["class_1_id"].map(_CATEGORIAS)
    df = df[["date", "name", "value"]]
    insert_data_into_database(_DATABASE, _TABLE, df)
