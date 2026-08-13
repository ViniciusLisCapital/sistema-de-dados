"""
PIM - Pesquisa Industrial Mensal (Producao Fisica), por Grandes Categorias Economicas

Agregado : 8887 -- "Producao Fisica Industrial, por grandes categorias economicas"
Variaveis: 12606 (NSA), 12607 (SA)
Banco    : macro_brasil.atv_pim_uso

Perspectiva por categoria de uso (bens de capital / intermediarios / consumo), complementar
a atv_pim.py (que classifica por secao/atividade CNAE). Mesmas variaveis (12606/12607),
mesma base (2022=100), mesma tabela de PK -- so muda o agregado/classificacao de origem
(543, nao 544). Categorias coletadas (classificacao 543):
  129278 - Bens de capital                              -> bens_capital
  129280 -   Bens de capital, exceto equip. transporte   -> bens_capital_exceto_transporte
  129282 -   Equipamentos de transporte industrial       -> bens_capital_transporte_industrial
  129283 - Bens intermediarios                           -> bens_intermediarios
  129285 -   Alim./beb. basicos p/ industria              -> intermediarios_alim_beb_basicos
  129287 -   Alim./beb. elaborados p/ industria            -> intermediarios_alim_beb_elaborados
  129289 -   Insumos industriais basicos                  -> insumos_industriais_basicos
  129291 -   Insumos industriais elaborados                -> insumos_industriais_elaborados
  129293 -   Combustiveis e lubrificantes basicos          -> combustiveis_lubrificantes_basicos
  129295 -   Combustiveis e lubrificantes elaborados       -> combustiveis_lubrificantes_elaborados
  129297 -   Pecas e acessorios p/ bens de capital          -> pecas_acessorios_bens_capital
  129299 -   Pecas e acessorios p/ equip. de transporte     -> pecas_acessorios_equip_transporte
  129300 - Bens de consumo                               -> bens_consumo
  129301 -   Bens de consumo duraveis                     -> bens_consumo_duraveis
  129302 -     Duraveis, exceto automoveis                  -> duraveis_exceto_automoveis
  129303 -     Automoveis para passageiros                  -> automoveis_passageiros
  129304 -     Equip. de transporte nao industrial          -> equip_transporte_nao_industrial
  129305 -   Bens de consumo semi e nao duraveis          -> bens_consumo_semi_nao_duraveis
  129306 -     Semiduraveis                                  -> consumo_semiduraveis
  129307 -     Nao duraveis                                  -> consumo_nao_duraveis
  129308 -     Alim./beb. basicos p/ consumo domestico       -> alim_beb_basicos_consumo
  129309 -     Alim./beb. elaborados p/ consumo domestico    -> alim_beb_elaborados_consumo
  129310 -     Gasolina para automovel                       -> gasolina_automovel
  129311 - Bens nao especificados anteriormente           -> bens_nao_especificados

Confirmado direto na API (metadados do agregado 8887) -- nao assumido de documentacao: a
hierarquia acima (nivel 0/1 por categoria) e exatamente essa, sem subdivisao adicional em
bens intermediarios (8 filhos diretos, todos folha).
"""

from datetime import datetime

import pandas as pd

from connectors.ibge import IBGE
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "atv_pim_uso"

_CATEGORIAS = {
    "129278": "bens_capital",
    "129280": "bens_capital_exceto_transporte",
    "129282": "bens_capital_transporte_industrial",
    "129283": "bens_intermediarios",
    "129285": "intermediarios_alim_beb_basicos",
    "129287": "intermediarios_alim_beb_elaborados",
    "129289": "insumos_industriais_basicos",
    "129291": "insumos_industriais_elaborados",
    "129293": "combustiveis_lubrificantes_basicos",
    "129295": "combustiveis_lubrificantes_elaborados",
    "129297": "pecas_acessorios_bens_capital",
    "129299": "pecas_acessorios_equip_transporte",
    "129300": "bens_consumo",
    "129301": "bens_consumo_duraveis",
    "129302": "duraveis_exceto_automoveis",
    "129303": "automoveis_passageiros",
    "129304": "equip_transporte_nao_industrial",
    "129305": "bens_consumo_semi_nao_duraveis",
    "129306": "consumo_semiduraveis",
    "129307": "consumo_nao_duraveis",
    "129308": "alim_beb_basicos_consumo",
    "129309": "alim_beb_elaborados_consumo",
    "129310": "gasolina_automovel",
    "129311": "bens_nao_especificados",
}

_ibge = IBGE()

def _fetch(variavel: int, seasonal_adjs: str, periodos) -> pd.DataFrame:
    """Busca uma variavel do PIM (grandes categorias economicas) e retorna DataFrame
    pronto para insercao. Mesma assinatura/logica de atv_pim.py._fetch(), so troca o
    agregado (8887) e a classificacao (543).

    Args:
        variavel:      ID da variavel IBGE. 12606 = NSA, 12607 = SA.
        seasonal_adjs: indicador de ajuste sazonal gravado no banco. "N" ou "Y".
        periodos:      periodo de busca -- qualquer formato aceito pelo connector.

    Returns:
        DataFrame com colunas: date, name, value, seasonal_adjs.
    """
    df = _ibge.get(
        agregado=8887,
        variaveis=variavel,
        classificacoes={543: [int(k) for k in _CATEGORIAS]},
        localidades={"N1": "all"},
        periodos=periodos,
    )
    df["name"]          = df["class_1_id"].map(_CATEGORIAS)
    df["seasonal_adjs"] = seasonal_adjs
    return df[["date", "name", "value", "seasonal_adjs"]]

def run(years_back: int = 2, periodos=None) -> None:
    """Atualiza macro_brasil.atv_pim_uso.

    Args:
        years_back: anos anteriores ao ano atual (default 2).
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

    nsa = _fetch(12606, "N", periodos)
    sa  = _fetch(12607, "Y", periodos)
    df  = pd.concat([nsa, sa], ignore_index=True)
    insert_data_into_database(_DATABASE, _TABLE, df)
