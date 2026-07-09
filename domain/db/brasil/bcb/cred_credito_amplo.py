"""
Credito - Estatisticas de credito amplo ao setor nao financeiro (BCB/SGS)

Series SGS coletadas (17 series — divida por instrumento e setor institucional):
  Governo  : emprestimos SFN, titulos publicos, divida externa (3 instrumentos)
  Empresas : emprestimos SFN/OSF/fundos/externos, titulos privados/securitizados (6)
  Familias : emprestimos SFN/OSF/fundos/externos, titulos securitizados (5)

  Fonte: Nota de Politica Monetaria e Operacoes de Credito do BCB

Banco: macro_brasil.cred_credito_amplo
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "cred_credito_amplo"

_SERIES = {
    # Governo
    "gov_emprestimos_sfn":              28197,
    "gov_titulos_publicos":             28198,
    "gov_emprestimos_divida_externa":   28200,
    "gov_divida_ext_mercado_externo":   28201,
    "gov_divida_ext_mercado_interno":   28202,
    # Empresas
    "emp_emprestimos_sfn":              28848,
    "emp_emprestimos_osf":              28849,
    "emp_emprestimos_fundos_gov":       28850,
    "emp_titulos_divida_privado":       28852,
    "emp_titulos_divida_securitizado":  28853,
    "emp_divida_externa_mercado_ext":   28856,
    "emp_divida_externa_mercado_int":   28857,
    # Familias
    "fam_emprestimos_sfn":              28860,
    "fam_emprestimos_osf":              28861,
    "fam_emprestimos_fundos_gov":       28862,
    "fam_titulos_securitizado":         28863,
    "fam_emprestimos_divida_externa":   28864,
}

_bcb = BCB()


def run(n_meses: int = 24, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.cred_credito_amplo.

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
