"""
IPCA/IPCA-15 agregados: indices de precos e nucleos do BCB/SGS.

Series SGS coletadas (33 series):
  Headline   : ipca (433), ipca15 (7478), ipca_indice_difusao (21379)
  Componentes: administrado, livres, industriais, alimentacao, servicos,
               bens_nao_duraveis, bens_semi_duraveis, bens_duraveis,
               comercializaveis, nao_comercializaveis
  Grupos IPCA: alimentacao_bebidas, habitacao, artigos_residencia, vestuario,
               transporte, comunicacao, saude_cuidados_pessoais,
               despesas_pessoais, educacao
  Nucleos    : ex0, ex01, ex02, ex03, ex03_servicos, ex03_industriais, exfe,
               p55, dp, medias_aparadas, medias_aparadas_sem_suavizacao

Schema macro_brasil.inflc_agregados:
  PRIMARY KEY (date, name)
  Colunas: date DATE | name VARCHAR(80) | value DECIMAL(10,4)

Renomeada de "inflacao" em 2026-07, de "ipca_agregados" em 2026-07 (prefixo de
tema) e de "inflation_agregados" em 2026-07 (prefixo abreviado) — nomes de
series padronizados para minusculo (ex.: IPCA_nucleo_P55 -> ipca_nucleo_p55).
Ver macro_brasil.inflc_decomposicao para a decomposicao por subitem (tabela
separada, fonte IBGE em vez de BCB).

Documentacao das series tambem disponivel via MySQL (COMMENT da tabela e da
coluna `name` listam cada serie com seu codigo SGS — visivel em
`SHOW CREATE TABLE inflc_agregados` ou no editor de tabelas do Workbench).
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "inflc_agregados"

_SERIES = {
    # Headline e gerais
    "ipca":                                433,
    "ipca15":                             7478,
    "ipca_indice_difusao":               21379,
    # Componentes por tipo de bem/servico
    "ipca_administrado":                  4449,
    "ipca_livres":                       11428,
    "ipca_industriais":                  27863,
    "ipca_alimentacao":                  27864,
    "ipca_servicos":                     10844,
    "ipca_bens_nao_duraveis":            10841,
    "ipca_bens_semi_duraveis":           10842,
    "ipca_bens_duraveis":                10843,
    "ipca_comercializaveis":              4447,
    "ipca_nao_comercializaveis":          4448,
    # Grupos por finalidade (IPCA)
    "ipca_grupo_alimentacao_bebidas":     1635,
    "ipca_grupo_habitacao":               1636,
    "ipca_grupo_artigos_residencia":      1637,
    "ipca_grupo_vestuario":               1638,
    "ipca_grupo_transporte":              1639,
    "ipca_grupo_comunicacao":             1640,
    "ipca_grupo_saude_cuidados_pessoais": 1641,
    "ipca_grupo_despesas_pessoais":       1642,
    "ipca_grupo_educacao":                1643,
    # Nucleos de inflacao
    "ipca_nucleo_medias_aparadas":                 4466,
    "ipca_nucleo_medias_aparadas_sem_suavizacao": 11426,
    "ipca_nucleo_ex0":                            11427,
    "ipca_nucleo_ex01":                            16121,
    "ipca_nucleo_dp":                              16122,
    "ipca_nucleo_ex02":                            27838,
    "ipca_nucleo_ex03":                            27839,
    "ipca_nucleo_p55":                             28750,
    "ipca_nucleo_exfe":                            28751,
    "ipca_nucleo_ex03_servicos":                   29683,
    "ipca_nucleo_ex03_industriais":                29684,
}

_bcb = BCB()


def run(n_meses: int = 24, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.inflc_agregados.

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
