"""
Inflacao - Indices de precos e nucleos do BCB/SGS

Series SGS coletadas (29 series):
  Headline   : IPCA (433), IPCA15 (7478), Indice_Difusao (21379)
  Componentes: Administrado, Livres, Industriais, Alimentacao, Servicos,
               BensNaoDuraveis, SemiDuraveis, Duraveis
  Grupos IPCA: AlimentacaoBebidas, Habitacao, ArtigosResidencia, Vestuario,
               Transporte, Comunicacao, SaudeCuidadosPessoais,
               DespesasPessoais, Educacao
  Nucleos    : EX0, EX01, EX02, EX03, EXFE, P55, DP, MediasAparadasSuavizadas

Banco: brasil.inflacao
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "inflacao"

_SERIES = {
    # Headline e gerais
    "IPCA":                                433,
    "IPCA15":                             7478,
    "IPCA_indice_difusao":               21379,
    # Componentes por tipo de bem/servico
    "IPCA_administrado":                  4449,
    "IPCA_livres":                       11428,
    "IPCA_industriais":                  27863,
    "IPCA_alimentacao":                  27864,
    "IPCA_servicos":                     10844,
    "IPCA_bens_nao_duraveis":            10841,
    "IPCA_bens_semi_duraveis":           10842,
    "IPCA_bens_duraveis":                10843,
    # Grupos por finalidade (IPCA)
    "IPCA_grupo_alimentacao_bebidas":     1635,
    "IPCA_grupo_habitacao":               1636,
    "IPCA_grupo_artigos_residencia":      1637,
    "IPCA_grupo_vestuario":               1638,
    "IPCA_grupo_transporte":              1639,
    "IPCA_grupo_comunicacao":             1640,
    "IPCA_grupo_saude_cuidados_pessoais": 1641,
    "IPCA_grupo_despesas_pessoais":       1642,
    "IPCA_grupo_educacao":                1643,
    # Nucleos de inflacao
    "IPCA_nucleo_medias_aparadas":        4466,
    "IPCA_nucleo_EX0":                   11427,
    "IPCA_nucleo_EX01":                  16121,
    "IPCA_nucleo_DP":                    16122,
    "IPCA_nucleo_EX02":                  27838,
    "IPCA_nucleo_EX03":                  27839,
    "IPCA_nucleo_P55":                   28750,
    "IPCA_nucleo_EXFE":                  28751,
}

_bcb = BCB()


def run(n_meses: int = 24, start: str | None = None, end: str | None = None) -> None:
    """Atualiza brasil.inflacao.

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
