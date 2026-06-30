"""
Atualiza o banco de dados macro_analytics (series derivadas/calculadas).

Uso:
    uv run python jobs\\update_analytics.py

Cada script e independente: se um falhar, os demais continuam.
Exit code 1 se houver qualquer falha.

Fontes:
  FRED + BCB — Diferenciais de juros Brasil x EUA (nominal e real ex-post)
"""

import logging
import sys
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("update_analytics")

from domain.db.analytics.fred import diferenciais_juros

_SCRIPTS = [
    ("FRED · Diferenciais de Juros", diferenciais_juros, {}),
]


def main() -> None:
    inicio = datetime.now()
    erros: list[tuple[str, str]] = []

    logger.info("Iniciando atualizacao macro_analytics — %d scripts", len(_SCRIPTS))

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
