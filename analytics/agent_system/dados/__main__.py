"""
Gera o F(A) de um agente para um ciclo.

    uv run python -m analytics.agent_system.dados cambio
    uv run python -m analytics.agent_system.dados cambio --ciclo 2026-10-07
    uv run python -m analytics.agent_system.dados cambio --refazer

F(A) é fixo dentro do ciclo (IV.iv): se o F do agente já existe naquele ciclo, o gerador
para. `--refazer` extrai de novo o A das tabelas deste agente e reescreve o F; serve para
consertar um ciclo que ainda não começou, não para atualizar um que está correndo.
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib
import sys

from analytics.agent_system.dados import motor

AGENTES = {"cambio": "analytics.agent_system.dados.cambio"}


def gerar(agente: str, ciclo: dt.date, refazer: bool = False):
    mod = importlib.import_module(AGENTES[agente])
    grupos = motor.ler_lista(mod.SECAO)
    motor.conferir(mod.TABELAS, grupos)
    pasta = motor.CICLOS / ciclo.isoformat() / "dados"
    saida = pasta / f"F_{agente}.md"
    if saida.exists() and not refazer:
        sys.exit(f"{saida} já existe: o F(A) é fixo no ciclo. Use --refazer para refazer.")
    anterior = motor.ciclo_anterior(agente, ciclo)
    motor.extrair(mod.TABELAS, pasta / "A", motor.pd.Timestamp(ciclo), refazer=refazer)
    # O retrato do Modelo Estrutural, que os G rodam (IV.vi): um por ciclo, como o A.
    from analytics.agent_system import modelo
    print(f"  modelo  {modelo.retratar(ciclo.isoformat(), refazer)}")
    (pasta / "G").mkdir(exist_ok=True)
    texto = motor.montar_f(agente, ciclo, grupos, mod.TABELAS, getattr(mod, "COMBINADAS", []),
                           pasta / "A", anterior, getattr(mod, "PIB", None))
    saida.write_text(texto, encoding="utf-8")
    print(f"  F(A)  {saida}")
    return saida


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(prog="python -m analytics.agent_system.dados")
    ap.add_argument("agente", choices=sorted(AGENTES))
    ap.add_argument("--ciclo", type=dt.date.fromisoformat, default=dt.date.today())
    ap.add_argument("--refazer", action="store_true")
    a = ap.parse_args()
    gerar(a.agente, a.ciclo, a.refazer)


if __name__ == "__main__":
    main()
