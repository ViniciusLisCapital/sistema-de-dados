"""
Atualiza o banco de dados macro_cambio com fundamentos do cambio.

Uso:
    .venv\\Scripts\\python jobs\\update_cambio.py

Cada script e independente: se um falhar, os demais continuam.
Exit code 1 se houver qualquer falha.

Fase 1 (BCB + FRED): reservas, balanco_pagamentos, fluxo_cambial,
                     termos_de_troca, diferenciais_juros
Fase 2 (BIS + CFTC): reer, cot_fx
"""

import logging
import sys
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("update_cambio")

# BCB
from domain.db.cambio.bcb import reservas, balanco_pagamentos, fluxo_cambial, termos_de_troca

# FRED
from domain.db.cambio.fred import diferenciais_juros

# BIS
from domain.db.cambio.bis import reer

# CFTC
from domain.db.cambio.cftc import cot_fx

_SCRIPTS = [
    ("BCB  · Reservas Internacionais",   reservas,            {}),
    ("BCB  · Balanco de Pagamentos",     balanco_pagamentos,  {}),
    ("BCB  · Fluxo Cambial",             fluxo_cambial,       {}),
    ("BCB  · Termos de Troca",           termos_de_troca,     {}),
    ("FRED · Diferenciais de Juros",     diferenciais_juros,  {}),
    ("BIS  · REER",                      reer,                {}),
    ("CFTC · COT FX Positioning",        cot_fx,              {}),
]


def main() -> None:
    inicio = datetime.now()
    erros: list[tuple[str, str]] = []

    logger.info("Iniciando atualizacao macro_cambio — %d scripts", len(_SCRIPTS))

    for label, mod, kwargs in _SCRIPTS:
        try:
            logger.info("%-45s ...", label)
            mod.run(**kwargs)
            logger.info("%-45s OK", label)
        except Exception as exc:
            logger.error("%-45s FALHOU: %s", label, exc)
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
