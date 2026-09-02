# -*- coding: utf-8 -*-
"""Saida de console em UTF-8 para os entry points que rodam geradores e ETL.

Existe por causa de um bug medido em 2026-09-01: o console do Windows abre em cp1252, e
um `print` de progresso com um caractere que ele nao encodifica levanta
`UnicodeEncodeError` DENTRO do gerador. O resumo do relatorio de inflacao imprime uma
seta (U+2192), entao:

  - clicar em **Regerar** naquele dashboard, pelo `abrir_calendario.bat`, voltava erro e
    NAO reconstruia o arquivo;
  - `jobs/update_db.py --group ibge_ipca` terminava o ETL e morria na regeracao que ele
    mesmo dispara desde 2026-08-28.

Em ambos os casos a falha e a mensagem de progresso, nao o dado -- que e a pior forma de
perder uma operacao. Medido: `status.gerar('brasil_inflation')` num shell cp1252 estoura
no `'\\u2192'`; com `PYTHONIOENCODING=utf-8` termina em 19,9s.

`errors="replace"` de proposito: um caractere que o terminal nao desenha nunca deve
custar a operacao. E o `try` cobre o fluxo que nao tem `reconfigure` (redirecionado,
capturado em teste, `io.StringIO`).
"""

from __future__ import annotations

import sys


def stdout_utf8() -> None:
    """Poe `sys.stdout`/`sys.stderr` em UTF-8. Chame no inicio de cada `main()`."""
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except Exception:                                          # noqa: BLE001
            pass
