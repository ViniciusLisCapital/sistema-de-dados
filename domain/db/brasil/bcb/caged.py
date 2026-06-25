"""
Novo CAGED - Cadastro Geral de Empregados e Desempregados

Series SGS coletadas (14 series — saldo de admissoes menos demissoes):
  Total e por setor de atividade economica (CNAE 2.0)

Banco: brasil.caged
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "caged"

_SERIES = {
    "caged_total":                       28763,
    "caged_agropecuaria":                28764,
    "caged_ind_extrativa":               28765,
    "caged_ind_transformacao":           28766,
    "caged_SIUP":                        28767,
    "caged_eletricidade_gas":            28768,
    "caged_gestao_residuos":             28769,
    "caged_construcao":                  28770,
    "caged_comercio":                    28771,
    "caged_servicos":                    28772,
    "caged_transp_arm_correios":         28773,
    "caged_aloj_alimentacao":            28774,
    "caged_informacao_comunicacao":      28775,
    "caged_ativ_financeiras_seguros":    28776,
}

_bcb = BCB()


def run(n_meses: int = 24, start: str | None = None, end: str | None = None) -> None:
    """Atualiza brasil.caged.

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
