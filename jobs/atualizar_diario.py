# -*- coding: utf-8 -*-
"""
Entry point da tarefa agendada `Macro - series diarias`.

E um envelope fino em volta de `update_db.main(["--continuous"])`: a lista de
tabelas continua vindo de `no_release.continuous` no
domain/release_calendar/calendar_2026.yaml, e a regeracao dos dashboards que
leem as tabelas escritas continua sendo a do proprio update_db. O que este
arquivo acrescenta e so o que uma execucao NAO INTERATIVA precisa -- log em
arquivo, poda e codigo de saida.

## Por que existe, e por que roda sob pythonw.exe

Pedido do usuario (2026-09-03): rodar de 30 em 30 minutos das 09:30 as 12:00
**sem abrir janela**. A janela vinha do `.bat`: um arquivo de lote e executado
pelo cmd.exe, que e um binario de console, entao a cada disparo pipocava um
prompt preto na frente de quem estivesse usando a maquina. `pythonw.exe` e a
variante do Python compilada para o subsistema GUI -- nao aloca console.

**E ai esta a armadilha, porque nao ter console significa nao ter stdout.**
Sob `pythonw`, `sys.stdout` e `sys.stderr` sao literalmente `None` -- medido
em 2026-09-03, nao suposto. E o que isso produz **nao e uma excecao, e
silencio**, o que e pior de diagnosticar:

  1. **`print()` com `sys.stdout is None` nao levanta: nao faz nada.** O
     `print` do CPython sai cedo quando o arquivo e None. Medido: `print()`,
     `logging.info()` e ate a seta U+2192 do bug de encoding de 2026-09-01
     (ver utils/console.py) todos passam sem erro e sem escrever nada.
  2. **`logging.basicConfig()` sem `stream=` fixa `sys.stderr` NA HORA DA
     CHAMADA**, e o `update_db` chama isso no topo do modulo, ou seja, no
     `import`. Medido: o handler nasce com `stream=None` e o `emit` falha
     em silencio, porque o proprio logging engole erro de handler.

Ou seja: sem o setup abaixo a tarefa **funcionaria** -- gravaria no banco,
regeraria os dashboards -- e nao deixaria uma linha de log. O dia em que
falhasse, nao haveria nada para ler. Nao e um crash a evitar, e uma cegueira.

Dai a ordem deste arquivo ser load-bearing: primeiro o log e aberto, depois
`sys.stdout`/`sys.stderr` passam a apontar para ele, depois o `basicConfig` e
feito por NOS (o do update_db vira no-op, porque o root logger ja tem handler),
e so entao o `update_db` e importado. Trocar a ordem dessas quatro coisas
devolve o modo de falha silencioso.

Verificado sob pythonw de ponta a ponta, incluindo um `generate_report` real
(`status.gerar("brasil_labor_market")`, 5,2s): os prints dele aparecem no log,
com a seta em UTF-8 correto (`e2 86 92` no arquivo).

## A janela retroativa nao e daqui

Cada script tem a sua, e nenhuma e configurada aqui -- e por isso que disparar
seis vezes de manha nao e desperdicio nem risco: toda insercao e upsert
(`ON DUPLICATE KEY UPDATE`), entao reescrever um dia que nao mudou nao produz
linha nova. Medido em 2026-09-03: um passe que nao encontra dado novo leva ~45s
e nao regera dashboard nenhum, porque `status.estado()` acha todo mundo em dia.

Uso:
    .venv\\Scripts\\pythonw.exe jobs\\atualizar_diario.py     # como a tarefa chama
    uv run python jobs/atualizar_diario.py                    # na mao, com saida no log
"""

from __future__ import annotations

import datetime as dt
import logging
import os
import pathlib
import sys
import traceback

RAIZ = pathlib.Path(__file__).resolve().parents[1]
LOGS = RAIZ / "logs"
DIAS_DE_LOG = 30


def _abrir_log():
    """Abre o log do dia em append. `buffering=1` (linha) de proposito: sem
    isso, um passe que travar no meio deixa o arquivo vazio, que e exatamente
    quando alguem vai querer le-lo."""
    LOGS.mkdir(exist_ok=True)
    caminho = LOGS / f"continuous_{dt.date.today().isoformat()}.log"
    return caminho.open("a", encoding="utf-8", errors="replace", buffering=1)


def _podar() -> None:
    """Mantem DIAS_DE_LOG dias de log."""
    limite = dt.datetime.now() - dt.timedelta(days=DIAS_DE_LOG)
    for f in LOGS.glob("continuous_*.log"):
        try:
            if dt.datetime.fromtimestamp(f.stat().st_mtime) < limite:
                f.unlink()
        except OSError:
            pass


def main() -> int:
    log = _abrir_log()

    # ORDEM IMPORTA -- ver a docstring. Estes dois vem antes de qualquer
    # import do projeto, senao um `basicConfig` de modulo captura o `None`.
    sys.stdout = log
    sys.stderr = log
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%H:%M:%S",
        stream=log,
    )

    log.write("\n" + "=" * 60 + "\n")
    log.write(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
              + f"  (pid {os.getpid()}, {pathlib.Path(sys.executable).name})\n")
    log.write("=" * 60 + "\n")

    # Os geradores gravam em caminhos relativos (`reports/...`). A tarefa ja
    # define o WorkingDirectory, mas nao custa nao depender disso.
    os.chdir(RAIZ)
    if str(RAIZ) not in sys.path:
        sys.path.insert(0, str(RAIZ))

    rc = 0
    try:
        from jobs.update_db import main as update_main
        update_main(["--continuous"])
    except SystemExit as exc:                # update_db sai 1 se algo falhou
        rc = int(exc.code or 0)
    except BaseException:                    # noqa: BLE001
        traceback.print_exc(file=log)
        rc = 2

    log.write(f"\n[fim] codigo de saida={rc}\n")
    log.flush()
    _podar()
    return rc


if __name__ == "__main__":
    sys.exit(main())
