"""
Atualiza o banco de dados brasil com os dados mais recentes de todas as fontes.

Uso:
    .venv\\Scripts\\python jobs\\update_db.py

Cada script e independente: se um falhar, os demais continuam.
Exit code 1 se houver qualquer falha.
"""

import logging
import sys
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("update_db")

# IBGE
from domain.db.brasil.ibge import (
    atv_pib, atv_pim, atv_pmc, atv_pms, mt_pnad,
    inflc_decomposicao, inflc_dim,
)

# BCB
from domain.db.brasil.bcb import (
    atv_ibcbr, mt_caged, cred_credito_amplo, cred_credito_familias, expc_focus,
    inflc_agregados, cmb_cambio_contratado, cmb_reservas_bc, cmb_balanco_pagmt,
    cmb_fluxo_cambial, cmb_ptax,
)

# IPEA
from domain.db.brasil.ipea import cmb_termos_troca

# ---------------------------------------------------------------------------
# Scripts e parametros de atualizacao rotineira
# ---------------------------------------------------------------------------
# Cada entrada: (label, modulo, kwargs)
# Os defaults de cada run() ja cobrem as janelas adequadas para updates diarios:
#   SGS  → ultimos N meses  (range revisao tipica de cada serie)
#   IBGE → ultimos N anos   (idem)
#   Focus → ultimos 90 dias

_SCRIPTS = [
    # IBGE
    ("IBGE · GDP / Contas Nacionais",  atv_pib,               {}),
    ("IBGE · PIM / Prod. Industrial",  atv_pim,               {}),
    ("IBGE · PMC / Varejo",            atv_pmc,               {}),
    ("IBGE · PMS / Servicos",          atv_pms,               {}),
    ("IBGE · PNAD / Emprego",          mt_pnad,               {}),
    ("IBGE · IPCA Decomposicao",       inflc_decomposicao,    {}),
    ("IBGE · IPCA Dimensao",           inflc_dim,             {}),
    # BCB
    ("BCB  · IBC-Br",                  atv_ibcbr,             {}),
    ("BCB  · IPCA Agregados",          inflc_agregados,       {}),
    ("BCB  · CAGED",                   mt_caged,              {}),
    ("BCB  · Credito",                 cred_credito_amplo,    {}),
    ("BCB  · Indicadores Familias",    cred_credito_familias, {}),
    ("BCB  · Expectativas Focus",      expc_focus,            {}),
    ("BCB  · Reservas Internacionais", cmb_reservas_bc,       {}),
    ("BCB  · Balanco de Pagamentos",   cmb_balanco_pagmt,     {}),
    ("BCB  · Fluxo Cambial",           cmb_fluxo_cambial,     {}),
    ("BCB  · Cambio Contratado",       cmb_cambio_contratado, {}),
    ("BCB  · PTAX + Volume Interbanc.", cmb_ptax,              {}),
    ("IPEA · Termos de Troca (Funcex)", cmb_termos_troca,      {}),
]


def main() -> None:
    inicio = datetime.now()
    erros: list[tuple[str, str]] = []

    logger.info("Iniciando atualizacao — %d scripts", len(_SCRIPTS))

    for label, mod, kwargs in _SCRIPTS:
        try:
            logger.info("%-40s ...", label)
            mod.run(**kwargs)
            logger.info("%-40s OK", label)
        except Exception as exc:
            logger.error("%-40s FALHOU: %s", label, exc)
            erros.append((label, str(exc)))

    elapsed = (datetime.now() - inicio).seconds
    n_ok = len(_SCRIPTS) - len(erros)
    logger.info("Concluido em %ds — %d/%d OK", elapsed, n_ok, len(_SCRIPTS))

    if erros:
        logger.error("%d script(s) falharam:", len(erros))
        for label, err in erros:
            logger.error("  - %s: %s", label, err)
        sys.exit(1)


if __name__ == "__main__":
    main()
