"""
Crédito do sistema financeiro — saldo por tipo de cliente (BCB/SGS)

Series SGS coletadas (7 series, R$ milhoes) -- Tabela 25 da publicacao mensal do BCB
"Tabelas de Estatisticas Monetarias e de Credito" (ver analytics/credit/fontes_dados.md).
Uma unica metrica (saldo). Unico lugar da planilha que separa credito ao setor publico
(governo como TOMADOR de credito bancario -- diferente do que cred_credito_amplo/
fisc_divida medem, que sao o governo como EMISSOR de divida).

"total" (codigo 20539) e o mesmo codigo SGS de cred_credito_resumo.saldo_total_total --
mantido aqui porque e a propria coluna "Total" da Tabela 25 (ancora de reconciliacao:
setor_privado_total + setor_publico_total = total), nao uma serie nova.

Disponivel via SGS desde 2012-01.

Banco: macro_brasil.cred_credito_tipo_cliente -- PRIMARY KEY (date, name)
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "cred_credito_tipo_cliente"

_SERIES = {
    "setor_privado_pj":                          22047,
    "setor_privado_pf":                          22050,
    "setor_privado_total":                       22052,
    "setor_publico_governo_federal":              22025,
    "setor_publico_governos_estaduais_municipais": 22026,
    "setor_publico_total":                       22051,
    "total":                                      20539,
}

_bcb = BCB()


def run(n_meses: int = 24, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.cred_credito_tipo_cliente.

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
