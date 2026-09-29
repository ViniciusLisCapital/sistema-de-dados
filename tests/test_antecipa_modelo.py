"""
Testes de `analytics/brasil/structural_model/modelo_agregado/antecipa_modelo.py`: os insumos
do cenario de referencia que o modelo agregado simula para tentar antecipar a projecao do BC.

Sairam de `tests/test_antecipa_copom.py` em 2026-09-24, quando o modelo saiu da pasta de
Politica Monetaria. Cada secao nasceu de um erro que devolvia numero plausivel e errado sem
levantar excecao. Precisa de MySQL; nao roda o modelo, entao e rapido.

    uv run python tests/test_antecipa_modelo.py
"""

from __future__ import annotations

import sys

import numpy as np
import pandas as pd

from analytics.brasil.structural_model.modelo_agregado import antecipa_modelo as am

falhas = 0


def ok(cond, nome, detalhe=""):
    global falhas
    if cond:
        print("  ok   " + nome)
    else:
        falhas += 1
        print("  FALHA " + nome + ("  -- " + str(detalhe) if detalhe else ""))


print("\n2. r* e o valor ANUNCIADO pelo BC, degrau por reuniao")
# O BC fixa a neutra e avisa quando muda; nossa estimativa (7,81%) e outro objeto e poe
# 2028T1 0,4 p.p. acima. Confundir os dois foi o que separava 3,45 de 3,07.
ok(am.r_neutra(262) == 4.50, "antes de jun/2024: 4,50%", am.r_neutra(262))
ok(am.r_neutra(263) == 4.75, "263a adota 4,75% (RPM jun/2024 p.74)", am.r_neutra(263))
ok(am.r_neutra(266) == 4.75, "segue 4,75% ate a 266a", am.r_neutra(266))
ok(am.r_neutra(267) == 5.00, "267a adota 5,00% (RPM dez/2024 p.59)", am.r_neutra(267))
ok(am.r_neutra(281) == 5.00, "e continua em 5,00% (reafirmado em jun/2026)",
   am.r_neutra(281))

print("\n3. Curva de Selic: realizado ate o corte, esperado depois")
# A Focus DESCARTA da curva as reunioes que ja aconteceram -- em 21/08/2026 o primeiro
# rotulo e R6/2026, e a 280a (05/08) sumiu. Como t0 fica meses atras, a janela comeca no
# passado: uma versao anterior segurava um nivel fixo ali e ignorava decisoes ja tomadas.
t0 = pd.Period("2026Q2", "Q")
sel = am.curva_selic(pd.Timestamp("2026-09-16"), t0, 7)
ok(len(sel) == 7, "devolve um valor por trimestre do horizonte", len(sel))
ok(np.all(np.isfinite(sel)), "sem NaN")
# 2026T3 contem a 280a, que cortou para 14,00 em 05/08. A media do trimestre tem de ficar
# ENTRE o nivel anterior (14,25) e o decidido, nunca fora.
ok(14.00 <= sel[0] <= 14.25,
   "2026T3 fica entre o nivel anterior e o decidido na 280a", round(float(sel[0]), 3))
# e o trimestre e MEDIA, nao fim de trimestre: se fosse fim, daria exatamente 14,00
ok(abs(sel[0] - 14.00) > 1e-6, "e a agregacao e media, nao fim de trimestre",
   round(float(sel[0]), 4))
ok(sel[-1] < sel[0], "a curva da Focus esta em queda no horizonte",
   (round(float(sel[0]), 2), round(float(sel[-1]), 2)))

print("\n8. Cambio: observado ate o corte, PPC depois")
de = am.curva_cambio(pd.Timestamp("2024-12-11"), pd.Period("2024Q3", "Q"), 7)
ok(len(de) == 7 and np.all(np.isfinite(de)), "um valor por trimestre, sem NaN")
ok(de[0] > 3.0, "2024T4 carrega a depreciacao observada do real", round(float(de[0]), 3))
ok(np.allclose(de[1:], de[1]), "e dai em diante e PPC, constante",
   np.round(de[1:], 4).tolist())
# 0,25 = (meta 3 - PI_EXT 2)/4, a mesma definicao de de_ppc dentro do simular()
ok(abs(de[-1] - 0.25) < 1e-9, "e o PPC vale (meta - 2)/4 = 0,25 por trimestre",
   round(float(de[-1]), 4))


print("\n" + (str(falhas) + " FALHA(S)" if falhas else "todos os testes passaram"))
sys.exit(1 if falhas else 0)
