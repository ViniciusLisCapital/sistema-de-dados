"""
Crédito do sistema financeiro — saldo por atividade econômica (BCB/SGS)

Series SGS coletadas (38 series, R$ milhoes) -- Tabela 24 da publicacao mensal do BCB
"Tabelas de Estatisticas Monetarias e de Credito" (ver analytics/brasil/credit/fontes_dados.md).
Uma unica metrica (saldo) -- quebra setorial mais fina de toda a planilha: agropecuaria,
~17 subsetores industriais (com total), ~15 subsetores de servicos (com total), outros,
total geral.

Disponivel via SGS desde 2012-01.

Banco: macro_brasil.cred_credito_atividade_economica -- PRIMARY KEY (date, name)
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "cred_credito_atividade_economica"

_SERIES = {
    "agropecuaria":                                          22027,
    "industria_siup":                                         22034,
    "industria_construcao":                                   22030,
    "industria_alimentos":                                    27743,
    "industria_acucar":                                       27744,
    "industria_textil_vestuario_couro_calcados":              27745,
    "industria_papel_celulose":                               27746,
    "industria_petroleo_gas_alcool":                           27747,
    "industria_metalurgia_siderurgia":                        27748,
    "industria_quimica_farmaceutica":                         27722,
    "industria_bens_capital":                                 27723,
    "industria_automobilistica":                              27724,
    "industria_mineracao":                                    27749,
    "industria_obras_infraestrutura":                         27725,
    "industria_outros_bens_consumo_duraveis":                 27726,
    "industria_embalagens":                                   27727,
    "industria_bens_consumo_nao_duraveis":                    27728,
    "industria_total":                                        22043,
    "servicos_transportes_total":                             22037,
    "servicos_transportes_via_terrestre_carga_passageiro":    27729,
    "servicos_transportes_meios_aquaviario_aereo":            27730,
    "servicos_transportes_dutoviario":                        27731,
    "servicos_comercio":                                      22036,
    "servicos_comercio_varejo_bens_nao_duraveis":              27732,
    "servicos_comercio_varejo_bens_duraveis":                 27733,
    "servicos_comercio_atacado_bens_duraveis_nao_duraveis":   27734,
    "servicos_comercio_geral_veiculos_automotores":           27735,
    "servicos_comercio_geral_bens_intermediarios":            27736,
    "servicos_comercio_geral_bens_capital":                   27737,
    "servicos_administracao_publica":                         22039,
    "servicos_imobiliarios":                                  27738,
    "servicos_informacao_comunicacao":                        27739,
    "servicos_demais_prestados_familias":                     27740,
    "servicos_demais_prestados_empresas":                     27741,
    "servicos_financeiros":                                   27742,
    "servicos_outros":                                        22041,
    "servicos_total":                                         22044,
    "outros":                                                 22042,
}

_bcb = BCB()


def run(n_meses: int = 24, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.cred_credito_atividade_economica.

    Args:
        n_meses: ultimos N meses (default 24). Ignorado se start/end fornecidos.
        start:   data inicial no formato "DD/MM/YYYY", ou "all" para serie completa.
        end:     data final no formato "DD/MM/YYYY". Default: hoje.
    """
    if start:
        df = _bcb.get_sgs(_SERIES, start=start, end=end)
    else:
        df = _bcb.get_sgs_ultimos(_SERIES, n=n_meses)

    insert_data_into_database(_DATABASE, _TABLE, df)
