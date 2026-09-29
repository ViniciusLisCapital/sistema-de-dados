# -*- coding: utf-8 -*-
"""Testa a mecanica do caminho da Selic da aba Acompanhamento Condicionais.

Roda com:
    uv run python tests/test_condicionais.py

Script com asserts, nao pytest (mesmo padrao de tests/test_condicoes_copom.py). **Nao toca no
banco**: so as funcoes puras de `analytics/brasil/monetary_policy/condicionais.py`, sobre datas
escolhidas a mao. O payload pronto -- que nenhuma pesquisa passa da sexta de corte, que o
primeiro degrau e a propria reuniao, que a ancora e a Selic vigente -- e coberto pela secao 35
de tests/test_monetary_policy_js.js.

O que se testa aqui, e cada item erra sem levantar nada se quebrar:

1. `sexta_anterior()` e ESTRITA: numa sexta devolve a da semana anterior, senao a pesquisa de
   uma reuniao de sexta seria a do proprio dia;
2. `posicoes()` numera por ano e levanta num ano com mais de oito reunioes -- uma
   extraordinaria deslocaria a posicao de todas as seguintes;
3. `data_da_posicao()` so estima o que nao conhece, e estima pela MESMA posicao no ultimo ano
   em que ela e conhecida, 52 semanas por ano depois -- o que mantem a data numa quarta. A
   regra anterior (a mediana do dia do ano) caia em sabado e domingo.
"""
from __future__ import annotations

import datetime as dt
import sys

from analytics.brasil.monetary_policy import condicionais as cn

falhas = 0


def check(nome, cond, detalhe=""):
    global falhas
    if cond:
        print("  ok     " + nome)
    else:
        falhas += 1
        print("  FALHA  " + nome + (("  -- " + str(detalhe)) if detalhe else ""))


D = dt.date

print("1. sexta-feira anterior")
check("quarta de decisao -> a sexta cinco dias antes",
      cn.sexta_anterior(D(2026, 9, 16)) == D(2026, 9, 11), cn.sexta_anterior(D(2026, 9, 16)))
check("numa sexta, a da semana ANTERIOR (estrita)",
      cn.sexta_anterior(D(2026, 9, 11)) == D(2026, 9, 4), cn.sexta_anterior(D(2026, 9, 11)))
check("num sabado, a da vespera", cn.sexta_anterior(D(2026, 9, 12)) == D(2026, 9, 11))
check("numa segunda, a de tres dias antes", cn.sexta_anterior(D(2026, 9, 14)) == D(2026, 9, 11))
check("sempre uma sexta, sempre antes, nunca mais de uma semana antes",
      all(cn.sexta_anterior(D(2026, 1, 1) + dt.timedelta(k)).weekday() == 4
          and 0 < ((D(2026, 1, 1) + dt.timedelta(k)) - cn.sexta_anterior(D(2026, 1, 1) + dt.timedelta(k))).days <= 7
          for k in range(400)))

print("2. posicao da reuniao no ano")
ano = [D(2025, m, 15) for m in (1, 3, 5, 6, 7, 9, 11, 12)]
pos = cn.posicoes(ano + [D(2026, 1, 28), D(2026, 3, 18)] + [D(2004, 5, 1)])
check("n-esima reuniao do ano, em ordem de data", pos[(2025, 1)] == D(2025, 1, 15) and pos[(2025, 8)] == D(2025, 12, 15))
check("a numeracao recomeca a cada ano", pos[(2026, 1)] == D(2026, 1, 28) and pos[(2026, 2)] == D(2026, 3, 18))
check("anos antes de PRIMEIRO_ANO ficam fora (a Focus rotulava diferente)", (2004, 1) not in pos)
check("datas repetidas contam uma vez", cn.posicoes(ano + ano) == cn.posicoes(ano))
try:
    cn.posicoes(ano + [D(2025, 10, 1)])
    check("um ano com nove reunioes levanta", False, "nao levantou")
except ValueError:
    check("um ano com nove reunioes levanta", True)

print("3. data real e data estimada")
# Quartas-feiras, como toda decisao do Copom desde 2006.
completo = {(a, n): D(a, 1, 1) + dt.timedelta(days=(2 - D(a, 1, 1).weekday()) % 7 + 42 * n)
            for a in range(2014, 2028) for n in range(1, 9)}
completo.pop((2027, 8))           # 2027 com a ultima reuniao ainda nao marcada
d, est = cn.data_da_posicao(2025, 3, completo)
check("posicao conhecida devolve a data real, sem marca", d == completo[(2025, 3)] and est is False)
d, est = cn.data_da_posicao(2028, 3, completo)
check("posicao desconhecida: a do ultimo ano conhecido, 52 semanas depois, marcada como estimada",
      est is True and d == completo[(2027, 3)] + dt.timedelta(weeks=52), d)
check("e cai no mesmo dia da semana (quarta)", d.weekday() == 2, d.weekday())
d, est = cn.data_da_posicao(2027, 8, completo)
check("ano com a posicao faltando usa o anterior dela, nao o vizinho de ano",
      est is True and d == completo[(2026, 8)] + dt.timedelta(weeks=52), d)
d, est = cn.data_da_posicao(2029, 8, completo)
check("tres anos alem do ultimo conhecido: 156 semanas depois dele",
      d == completo[(2026, 8)] + dt.timedelta(weeks=156) and est is True, d)

print("")
print(("%d FALHA(S)" % falhas) if falhas else "todos os asserts passaram")
sys.exit(1 if falhas else 0)
