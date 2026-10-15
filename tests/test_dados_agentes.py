# -*- coding: utf-8 -*-
"""Testa o gerador do F(A) dos agentes (analytics/agent_system/dados/).

Roda com:
    uv run python tests/test_dados_agentes.py

Script com asserts, nao pytest (mesmo padrao de tests/test_condicionais.py). Nao toca no banco.
Cada item erra sem levantar nada se quebrar:

1. a declaracao do agente diverge da lista decidida no SISTEMA_AGENTES.md (V) -- o agente
   ganharia ou perderia uma tabela sem o usuario saber;
2. o mes em curso entra numa soma como se estivesse completo;
3. uma serie de eventos (intervencoes) trata mes sem linha como ausencia, nao como zero;
4. a variacao e o percentil saem da janela errada;
5. a curva DI lida nos prazos redondos nao reproduz os vertices publicados.
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd

from analytics.agent_system.dados import cambio, motor
from analytics.agent_system.dados.especiais import _taxa

sys.stdout.reconfigure(encoding="utf-8")
falhas = 0


def check(nome, cond, extra=""):
    global falhas
    print(("ok    " if cond else "FALHA ") + nome + (f"  [{extra}]" if not cond and extra != "" else ""))
    falhas += 0 if cond else 1


def levanta(fn, trecho):
    try:
        fn()
    except ValueError as exc:
        return trecho in str(exc)
    return False


# 1. declaracao x lista
grupos = motor.ler_lista(cambio.SECAO)
check("a declaracao do cambio bate com a lista V.I",
      not levanta(lambda: motor.conferir(cambio.TABELAS, grupos), ""))
check("tabela da lista sem declaracao levanta",
      levanta(lambda: motor.conferir([t for t in cambio.TABELAS if t.nome != "cmb_ptax"], grupos), "faltam"))
check("tabela declarada fora da lista levanta",
      levanta(lambda: motor.conferir(cambio.TABELAS + [motor.Tabela("tabela_nova")], grupos), "sobram"))

# 2. mes em curso
s = pd.Series(1.0, index=pd.bdate_range("2026-08-01", "2026-09-25"))
meses, parcial = motor.mensal(s)
check("setembro, que acaba em 25/09, fica fora das somas", meses.index[-1] == pd.Timestamp("2026-08-01"),
      meses.index[-1])
check("e aparece como parcial ate 25/09", parcial is not None and parcial[0] == pd.Timestamp("2026-09-25"))
check("agosto soma os dias uteis dele", meses.iloc[-1] == len(pd.bdate_range("2026-08-01", "2026-08-31")))

# 3. eventos
s = pd.Series([-1.0], index=[pd.Timestamp("2026-08-14")])
meses, parcial = motor.mensal(s, fim=pd.Timestamp("2026-09-30"))
check("mes sem intervencao e zero, ate o fim da tabela", list(meses) == [-1.0, 0.0], list(meses))

# 4. variacao e percentil
idx = pd.date_range("2010-01-01", periods=200, freq="MS")
s = pd.Series(np.arange(1, 201, dtype=float), index=idx)
ctx = motor.Ctx(corte=idx[-1], anterior=None, pasta_a=None, tabelas=[], completo=True)
r = motor._nivel(motor.Serie("x", "x", "u", "pct"), s, ctx, pct=True)
check("Δ% 12m contra o valor de 12 meses antes", r["Δ% 12m"] == f"{(200 / 188 - 1) * 100:+.1f}", r["Δ% 12m"])
check("o maior valor da historia tem percentil 100", r["Pctl hist."] == "100", r["Pctl hist."])
r = motor._nivel(motor.Serie("x", "x", "u", "dif"), s, ctx, pct=False)
check("Δ 3m em unidade da serie", r["Δ 3m"] == "+3.00", r["Δ 3m"])

# 5. curva
du, tx = np.array([21.0, 252.0, 504.0]), np.array([13.0, 12.5, 12.0])
check("a curva reproduz os vertices", all(abs(_taxa(du, tx, int(d)) - t) < 1e-9 for d, t in zip(du, tx)))
check("prazo alem do ultimo vertice nao e extrapolado", _taxa(du, tx, 600) is None)

print("")
print(("%d FALHA(S)" % falhas) if falhas else "todos os asserts passaram")
sys.exit(1 if falhas else 0)
