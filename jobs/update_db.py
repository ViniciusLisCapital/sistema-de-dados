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
from domain.db.brasil.ibge import gdp, pim, pmc, pms, pnad

# BCB
from domain.db.brasil.bcb import caged, credito, expectativas, ibc_br, indicadores_familias, inflacao

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
    ("IBGE · GDP / Contas Nacionais",  gdp,         {}),
    ("IBGE · PIM / Prod. Industrial",  pim,         {}),
    ("IBGE · PMC / Varejo",            pmc,         {}),
    ("IBGE · PMS / Servicos",          pms,         {}),
    ("IBGE · PNAD / Emprego",          pnad,        {}),
    # BCB
    ("BCB  · IBC-Br",                  ibc_br,      {}),
    ("BCB  · Inflacao",                inflacao,    {}),
    ("BCB  · CAGED",                   caged,       {}),
    ("BCB  · Credito",                 credito,              {}),
    ("BCB  · Indicadores Familias",    indicadores_familias, {}),
    ("BCB  · Expectativas Focus",      expectativas,         {}),
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
