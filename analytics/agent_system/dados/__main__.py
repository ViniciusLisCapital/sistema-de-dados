"""
Gera o F(A) de um agente para um ciclo, e junto o retrato do conhecimento (conhecimento.py).

    uv run python -m analytics.agent_system.dados cambio
    uv run python -m analytics.agent_system.dados cambio --ciclo 2026-10-07
    uv run python -m analytics.agent_system.dados cambio --refazer
    uv run python -m analytics.agent_system.dados cambio --ciclo 2026-10-29 --sem-literatura

F(A) é fixo dentro do ciclo (IV.iv): se o F do agente já existe naquele ciclo, o gerador
para. `--refazer` extrai de novo o A das tabelas deste agente e reescreve o F; serve para
consertar um ciclo que ainda não começou, não para atualizar um que está correndo.
`--sem-literatura` vai para o retrato do conhecimento: só o mapa conceitual (e, na política
monetária, os documentos do Copom da camada 1).

O F é gravado por último, depois do retrato do conhecimento: um erro no meio não deixa um F
pela metade que faria a próxima rodada parar com "já existe".
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib
import sys

from analytics.agent_system.dados import motor

AGENTES = {"cambio": "analytics.agent_system.dados.cambio",
           "politica_monetaria": "analytics.agent_system.dados.politica_monetaria",
           "inflacao": "analytics.agent_system.dados.inflacao",
           "atividade": "analytics.agent_system.dados.atividade",
           "fiscal": "analytics.agent_system.dados.fiscal",
           "externo": "analytics.agent_system.dados.externo",
           "expectativas": "analytics.agent_system.dados.expectativas"}


def conferir_consultas() -> None:
    """Todo par de agentes de AGENTES: mesma tabela no mesmo arquivo de A, mesma consulta."""
    motor.conferir_consultas({a: importlib.import_module(m).TABELAS for a, m in AGENTES.items()})


def gerar(agente: str, ciclo: dt.date, refazer: bool = False, sem_literatura: bool = False):
    mod = importlib.import_module(AGENTES[agente])
    grupos = motor.ler_lista(mod.SECAO)
    motor.conferir(mod.TABELAS, grupos)
    conferir_consultas()
    pasta = motor.CICLOS / ciclo.isoformat() / "dados"
    saida = pasta / f"F_{agente}.md"
    if saida.exists() and not refazer:
        sys.exit(f"{saida} já existe: o F(A) é fixo no ciclo. Use --refazer para refazer.")
    anterior = motor.ciclo_anterior(agente, ciclo)
    if saida.exists():
        saida.unlink()                  # --refazer: o F antigo descreve o A que vai ser trocado
    motor.extrair(mod.TABELAS, pasta / "A", motor.pd.Timestamp(ciclo), refazer=refazer)
    # O retrato do Modelo Estrutural, que os G rodam (IV.vi): um por ciclo, como o A.
    from analytics.agent_system import modelo
    print(f"  modelo  {modelo.retratar(ciclo.isoformat(), refazer)}")
    (pasta / "G").mkdir(exist_ok=True)
    texto = motor.montar_f(agente, ciclo, grupos, mod.TABELAS, getattr(mod, "COMBINADAS", []),
                           pasta / "A", anterior, getattr(mod, "PIB", None))
    # O retrato do conhecimento (o que o agente pode ler), fixo no ciclo como o F(A). Vem antes
    # de gravar o F: se ele levantar, o F não fica no disco e rodar de novo funciona.
    from analytics.agent_system import conhecimento
    try:
        print(f"  conhecimento  {conhecimento.gerar(agente, ciclo, refazer, sem_literatura=sem_literatura)}")
    except FileExistsError as e:
        print(f"  conhecimento  {e}")
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
    ap.add_argument("--sem-literatura", action="store_true",
                    help="retrato do conhecimento só com o mapa (e o Copom, na política monetária)")
    a = ap.parse_args()
    gerar(a.agente, a.ciclo, a.refazer, a.sem_literatura)


if __name__ == "__main__":
    main()
