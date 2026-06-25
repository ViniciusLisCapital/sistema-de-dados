"""
Balanco de Pagamentos do Brasil (BPM6)

Series SGS (valores em USD millions):
  22707 — Conta corrente — saldo
  22706 — Balanca comercial + servicos — saldo
  22708 — Exportacao de bens — ingressos
  22858 — Conta financeira — saldo
  22885 — Investimento direto no pais (IDP) — liquido
  22886 — Investimento direto no pais (IDP) — ingressos
  22867 — Investimento direto no exterior (IDE) — saidas
  22869 — Investimento em carteira — saldo
  22870 — Investimento em carteira — acoes — saldo
  22871 — Investimento em carteira — renda fixa — saldo

Banco: macro_cambio.balanco_pagamentos
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_cambio"
_TABLE    = "balanco_pagamentos"

_SERIES = {
    "conta_corrente":                22707,
    "balanca_comercial_servicos":    22706,
    "exportacao_bens":               22708,
    "conta_financeira":              22858,
    "investimento_direto_liquido":   22885,
    "idp_ingressos":                 22886,
    "ide_saidas":                    22867,
    "investimento_carteira":         22869,
    "carteira_acoes":                22870,
    "carteira_renda_fixa":           22871,
}

_bcb = BCB()


def run(n_meses: int = 36, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_cambio.balanco_pagamentos.

    Args:
        n_meses: ultimos N meses (default 36). Ignorado se start/end fornecidos.
        start:   data inicial no formato "DD/MM/YYYY", ou "all" para serie completa.
        end:     data final no formato "DD/MM/YYYY". Default: hoje.
    """
    if start:
        df = _bcb.get_sgs(_SERIES, start=start, end=end)
    else:
        df = _bcb.get_sgs_ultimos(_SERIES, n=n_meses)

    insert_data_into_database(_DATABASE, _TABLE, df)
