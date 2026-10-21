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
5. a curva DI lida nos prazos redondos nao reproduz os vertices publicados;
6. a declaracao de politica monetaria diverge da V.II, ou um item de varias tabelas numa
   linha so ("`a`, `b`, `c`: papel") some da leitura da lista;
7. uma tabela que o cambio tambem le ganha outra consulta no MESMO arquivo de A, que e
   compartilhado no ciclo;
8. uma serie trimestral sai com Δ 1m e Δ 3m iguais (os dois contra o trimestre anterior);
9. uma tabela sem coluna de dimensao (dims=()) quebra o pivot;
10. o recorte do BC refeito dos subitens nao e a media ponderada pelo peso do mes;
11. o ciclo de juros em curso comeca no lugar errado.
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd

from analytics.agent_system.dados import cambio, motor
from analytics.agent_system.dados import politica_monetaria as pm
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

# 6. politica monetaria: a declaracao bate com a V.II
grupos = motor.ler_lista(pm.SECAO)
itens = [it for g in grupos for it in g["itens"]]
check("a declaracao de PM bate com a lista V.II", not levanta(lambda: motor.conferir(pm.TABELAS, grupos), ""))
check("V.II tem 69 entradas em 10 grupos", (len(itens), len(grupos)) == (69, 10), (len(itens), len(grupos)))
check("o grupo 'Fora da lista' nao entra na secao", not any("Fora" in g["nome"] for g in grupos))
comex = [it for it in itens if it["tabela"].startswith("cmb_comex")]
check("item com tres tabelas numa linha vira tres itens com o mesmo papel",
      len(comex) == 3 and len({it["papel"] for it in comex}) == 1, [it["tabela"] for it in comex])
check("so o grupo 'Endogeno' ganha a leitura completa",
      [g["nome"] for g in grupos if g["nome"] == "Endógeno"] == ["Endógeno"]
      and any(g["nome"].startswith("Endógeno de câmbio") for g in grupos))

# 7. A compartilhado: tabela que os dois leem tem a mesma consulta, ou outro arquivo
corte = pd.Timestamp("2026-10-15")
fx = {t.arquivo: motor._sql(t, corte) for t in cambio.TABELAS}
divergem = [t.arquivo for t in pm.TABELAS if t.arquivo in fx and motor._sql(t, corte) != fx[t.arquivo]]
check("mesma tabela e mesmo arquivo de A => mesma consulta do cambio", not divergem, divergem)
us = next(t for t in pm.TABELAS if t.nome == "us_interest_rate")
check("a curva americana inteira vai para outro arquivo (variante)",
      us.arquivo == "us_interest_rate__curva.csv.gz" and us.arquivo not in fx, us.arquivo)

# 8. serie trimestral: 1t e 4t, nao 1m/3m (que dariam o mesmo trimestre anterior)
idx = pd.date_range("2020-01-01", periods=12, freq="QS")
s = pd.Series(np.arange(100, 112, dtype=float), index=idx)
ctx = motor.Ctx(corte=idx[-1], anterior=None, pasta_a=None, tabelas=[], completo=False)
r = motor._nivel(motor.Serie("x", "x", "u", "dif"), s, ctx, pct=False)
check("trimestral: Δ 1t contra o trimestre anterior", r.get("Δ 1t") == "+1.00", r)
check("trimestral: Δ 4t contra 4 trimestres antes", r.get("Δ 4t") == "+4.00", r)
check("trimestral: sem colunas 1m/3m", "Δ 1m" not in r and "Δ 3m" not in r, list(r))

# 9. tabela sem coluna de dimensao (dims=()) vira uma serie so
t = motor.Tabela("x", dims=())
df = pd.DataFrame({"date": pd.to_datetime(["2026-01-01", "2026-02-01"]), "value": [5.0, 5.2]})
w = motor.largo(df, t)
check("dims=() da uma coluna, com o nome da coluna de valor", list(w.columns) == ["value"], list(w.columns))

# 10. recortes do BC refeitos dos subitens: media ponderada pelo peso do mes
dec = pd.DataFrame({"date": pd.to_datetime(["2026-09-01"] * 3), "subitem_codigo": [1, 2, 3],
                    "var_mensal": [1.0, 3.0, 10.0], "pesos": [0.3, 0.1, 0.6],
                    "contribuicao": [0.003, 0.003, 0.06]})
dim = pd.DataFrame({"subitem_codigo": [1, 2, 3], "subgrupo": ["Serviços", "Serviços", "Monitorados"],
                    "subjacente": ["Serviços Subjacente", None, None]})
cl = pm._por_classe(dec, dim)
check("servicos = (0,3·1 + 0,1·3)/0,4", abs(cl["Serviços"].iloc[-1] - 1.5) < 1e-12, cl["Serviços"].iloc[-1])
check("servicos subjacentes so com o subitem marcado", abs(cl["Serviços subjacentes"].iloc[-1] - 1.0) < 1e-12)

# 11. o ciclo de juros em curso
r = pd.DataFrame({"nro_reuniao": range(1, 8), "date": pd.date_range("2025-01-01", periods=7, freq="45D"),
                  "selic_decidida": [10.0, 10.5, 10.5, 10.25, 10.0, 10.0, 10.0],
                  "variacao_bps": [50, 50, 0, -25, -25, 0, 0]})
txt = pm.copom_decisoes(r, None)[-1]
check("ciclo de corte comeca no primeiro corte depois da ultima alta",
      "corte desde" in txt and "4 reuniões" in txt and "-50 p.b." in txt and "de 10.50%" in txt, txt)
check("e conta as manutencoes no fim", "últimas 2 reuniões mantiveram" in txt, txt)

print("")
print(("%d FALHA(S)" % falhas) if falhas else "todos os asserts passaram")
sys.exit(1 if falhas else 0)
