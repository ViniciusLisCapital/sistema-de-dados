"""
Contas Economicas Trimestrais - Renda, Poupanca e Capacidade de Financiamento

Agregado : 2072 (Contas economicas trimestrais)
Variaveis: 933, 934, 935, 936, 937, 938, 939, 940, 941, 6596, 942, 943 (uma por linha da
           tabela -- este agregado nao tem classificacoes, cada variavel JA E a categoria)
Banco    : macro_brasil.atv_renda_poupanca

Continuacao do PIB (atv_pib/atv_pib_valores_correntes) na distribuicao secundaria da renda e na
conta de capital -- o mesmo agregado que a pagina do SIDRA mostra como "Contas economicas
trimestrais, segundo os tipos de contas": PIB -> (+/-) itens com o exterior -> Renda Nacional Bruta
-> Renda Nacional Disponivel Bruta -> (-) consumo -> Poupanca Bruta -> (-/+) itens de capital ->
Capacidade/Necessidade Liquida de Financiamento. E uma cascata linear de subtotais (cada "(=)" e a
soma acumulada dos "(+)/(-)" anteriores), nao uma arvore que ramifica -- por isso a hierarquia da
tabela e so indentacao/ordem, sem nos irmaos.

R$ milhoes a precos correntes, NSA -- sem variante com ajuste sazonal (confirmado: este agregado e
os dois unicos "vizinhos" no mesmo assunto, 6726/6727, sao apenas as taxas de poupanca/investimento
em %, agregados proprios, nao uma variante SA deste).
"""

from datetime import datetime

import pandas as pd

from connectors.ibge import IBGE
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "atv_renda_poupanca"

# Ordem = ordem de apresentacao da tabela (topo ao fundo). variavel_id -> name.
_CATEGORIAS = {
    933:  "pib",
    934:  "salarios_exterior",
    935:  "rendas_propriedade_exterior",
    936:  "renda_nacional_bruta",
    937:  "transferencias_correntes_exterior",
    938:  "renda_nacional_disponivel_bruta",
    939:  "despesa_consumo_final",
    940:  "poupanca_bruta",
    941:  "formacao_bruta_capital",
    6596: "cessao_ativos_nao_financeiros",
    942:  "transferencias_capital_exterior",
    943:  "capacidade_liquida_financiamento",
}

_ibge = IBGE()


def run(years_back: int = 5, periodos=None) -> None:
    """Atualiza macro_brasil.atv_renda_poupanca.

    Args:
        years_back: anos anteriores ao ano atual (default 5).
                    Ignorado se periodos for fornecido.
        periodos:   qualquer formato aceito pelo connector IBGE ("all" para carga historica
                    completa desde 2000-Q1).
    """
    if periodos is None:
        ano_fim  = datetime.now().year
        periodos = (ano_fim - years_back, ano_fim)

    df = _ibge.get(
        agregado=2072,
        variaveis=list(_CATEGORIAS),
        localidades={"N1": "all"},
        periodos=periodos,
    )
    df["name"] = df["variavel_id"].map(_CATEGORIAS)
    df = df[["date", "name", "value"]]
    insert_data_into_database(_DATABASE, _TABLE, df)
