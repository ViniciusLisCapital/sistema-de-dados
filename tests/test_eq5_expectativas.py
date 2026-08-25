# -*- coding: utf-8 -*-
"""Testa o solucionador da equacao (5) do modelo agregado do BC.

Roda com:
    uv run python tests/test_eq5_expectativas.py

Segue o padrao do tests/test_sync_calendar.py: script executavel com asserts, nao
pytest (o projeto nao tem pytest configurado). Nao toca no banco -- le os paineis e os
parametros ja gravados em `analytics/brasil/monetary_policy/data/`.

O harness JS cobre o payload e as abas; nao alcanca o ponto fixo em si, que e a parte
com risco algoritmico de verdade: a expectativa de inflacao no cenario depende da
propria trajetoria simulada quatro trimestres a frente. O que se testa aqui:

1. a eq. (5) vale EXATAMENTE em todo trimestre do caminho resolvido -- se um termo for
   esquecido no simulador, a identidade quebra e nenhum grafico denuncia;
2. o resultado nao depende do buffer de horizonte (a condicao terminal e inocua);
3. a configuracao "premissa" nao mudou de comportamento (recursao causal);
4. um phi fora da regiao de estabilidade levanta erro em vez de devolver numero -- e a
   fronteira e real: acima dela dobrar o buffer muda a resposta em p.p. inteiros;
5. a eq. (4) com caminho de juros plano devolve exatamente o cambio de PPC;
6. a leitura de condicionantes e feita EM t0, nao no fim do painel -- e o que permite
   simular a partir de um trimestre do historico (o que `estimar_eq5` faz 81 vezes).
"""
from __future__ import annotations

import json
import sys

import numpy as np
import pandas as pd

from analytics.brasil.monetary_policy import modelo_agregado as M
from analytics.brasil.monetary_policy import modelo_painel as MP

falhas = 0


def ok(cond: bool, rot: str, extra: str = "") -> None:
    global falhas
    if cond:
        print("  ok   %s" % rot)
    else:
        falhas += 1
        print("  FALHA %s%s" % (rot, ("  -- " + extra) if extra else ""))


def prox(a: float, b: float, tol: float = 1e-10) -> bool:
    return abs(float(a) - float(b)) <= tol


if not (M.DATA / "modelo_params.json").exists():
    sys.exit("rode modelo_painel.py e modelo_agregado.py antes")

par = json.loads((M.DATA / "modelo_params.json").read_text(encoding="utf-8"))
P = MP.carregar("full")
S = M.estados(P, par)
PHI = {k: par[k] for k in ("f1", "f2", "f3")}
W_META = 1.0 - sum(PHI.values())
# o simulador para no ultimo trimestre com pi_L E selic, que pode ser anterior ao ultimo
# com selic -- ler os condicionantes de outro jeito aqui daria falso negativo
T0 = P[["pi_L", "selic"]].dropna().index.max()
I0 = M._em(P["selic"], T0)


def _meta(idx):
    """Como o simulador: reindexa, ffill e cai no ultimo valor valido em t0."""
    m = P["meta"].reindex(idx).ffill()
    return m.fillna(M._em(P["meta"], T0)).values


print("\n1. A eq. (5) vale como identidade no caminho resolvido")
# Uma unica rodada, longa: os leads dos primeiros trimestres saem dela mesma, entao a
# identidade e verificada contra o proprio caminho e nao contra outra simulacao.
N = 24
C = M.simular(P, par, S, n=N, expectativa="eq5", phi=PHI)
ipca = list(C["pi_IPCA"].values)
hist = list(P["pi_IPCA"][P["pi_IPCA"].index <= T0].dropna().iloc[-4:].values)
meta = _meta(C.index)
pie_ant = M._em(P["pi_e"], T0)
pior = 0.0
for k in range(N - 4):
    alvo = (PHI["f1"] * pie_ant + PHI["f2"] * sum(ipca[k + 1:k + 5])
            + PHI["f3"] * sum(hist[-4:]) + W_META * meta[k])
    pior = max(pior, abs(alvo - C["pi_e"].iloc[k]))
    pie_ant = C["pi_e"].iloc[k]
    hist.append(ipca[k])
ok(pior < 1e-9, "eq. (5) fecha em todos os %d trimestres" % (N - 4),
   "erro maximo %.2e" % pior)
ok(C.attrs["eq5_resid"] < 1e-11,
   "o sistema afim foi resolvido, nao iterado (residuo %.1e, cond %.1f)"
   % (C.attrs["eq5_resid"], C.attrs["eq5_cond"]))
ok(C.attrs["eq5_raio"] < 1.0,
   "raio espectral de G abaixo de 1 (solucao unica e limitada)",
   "%.4f" % C.attrs["eq5_raio"])


print("\n2. A condicao terminal e inocua")
a = M.simular(P, par, S, n=16, expectativa="eq5", phi=PHI)
b = M.simular(P, par, S, n=16, expectativa="eq5", phi=PHI, folga=2 * M.FOLGA)
d = float(np.nanmax(np.abs(a.values - b.values)))
ok(d < 1e-8, "dobrar o buffer default nao move o horizonte reportado",
   "maior dif %.2e" % d)


print("\n3. Com expectativa exogena a recursao e causal")
a = M.simular(P, par, S, n=16, folga=8)
b = M.simular(P, par, S, n=16, folga=48)
d = float(np.nanmax(np.abs(a.values - b.values)))
ok(d < 1e-12, "o buffer nao altera nada na configuracao 'premissa'", "maior dif %.2e" % d)


print("\n4. A fronteira de estabilidade e real, e fica logo acima do f2 estimado")
raios = {}
for f2 in (0.11, PHI["f2"], 0.45):
    ph = dict(f1=PHI["f1"], f2=f2, f3=PHI["f3"])
    try:
        raios[f2] = M.simular(P, par, S, n=8, expectativa="eq5", phi=ph).attrs["eq5_raio"]
    except RuntimeError:
        raios[f2] = None
ok(raios[0.11] is not None and raios[0.11] < raios[PHI["f2"]],
   "o raio cresce com f2 (e o peso da previsao do modelo que fecha o laco)",
   "%.3f -> %.3f" % (raios[0.11], raios[PHI["f2"]]))
ok(raios[PHI["f2"]] < 1.0, "o f2 estimado esta dentro da regiao estavel",
   "raio %.3f" % raios[PHI["f2"]])
ok(raios[0.45] is None, "f2 = 0,45 e recusado (raio > 1)")


print("\n5. eq. (4): cambio responde ao diferencial de juros, e so a ele")
C = M.simular(P, par, S, n=8, selic=I0, cambio="uip")
ok(np.allclose(C["de"].values, (_meta(C.index) - M.PI_EXT) / 4.0, atol=1e-12),
   "juro plano devolve exatamente o cambio de PPC")
ok(np.allclose(C["de_hat"].values, 0.0, atol=1e-12), "desvio do PPC e zero")

C = M.simular(P, par, S, n=8, selic=I0 + np.r_[np.ones(4), np.zeros(4)], cambio="uip")
ok(prox(C["de_hat"].iloc[0], -par["delta"]), "alta de 1 p.p. aprecia delta no trimestre")
ok(prox(C["de_hat"].iloc[1], 0.0), "sem nova variacao no diferencial, sem variacao cambial")
ok(prox(C["de_hat"].iloc[4], par["delta"]), "a volta do juro deprecia o mesmo delta")


print("\n6. Condicionantes lidos em t0, nao no fim do painel")
t = pd.Period("2015Q4", "Q")
ok(prox(M._em(P["selic"], t), float(P["selic"].loc[t])), "_em le o valor em t0")
C = M.simular(P, par, S, n=4, t0=t)
ok(C.index[0] == t + 1, "a simulacao comeca no trimestre seguinte a t0", str(C.index[0]))
ok(prox(C["selic"].iloc[0], float(P["selic"].loc[t])),
   "a Selic default e a de t0, nao a do fim do painel")
ok(np.isfinite(M._em(P["selic"], pd.Period("1999Q1", "Q"))),
   "_em antes do inicio da serie devolve numero finito")


print("\n7. A eq. (5) fortalece a transmissao, com o sinal certo")
ch = np.r_[np.ones(4), 0.8 ** np.arange(1, 14)]
base_p = M.simular(P, par, S, n=17, selic=I0)
alt_p = M.simular(P, par, S, n=17, selic=I0 + ch)
base_5 = M.simular(P, par, S, n=17, selic=I0, expectativa="eq5", phi=PHI)
alt_5 = M.simular(P, par, S, n=17, selic=I0 + ch, expectativa="eq5", phi=PHI)
pico_p = float((alt_p["ipca_4t"] - base_p["ipca_4t"]).min())
pico_5 = float((alt_5["ipca_4t"] - base_5["ipca_4t"]).min())
ok(pico_5 < pico_p - 0.01, "com a eq. (5) o pico e mais negativo",
   "%.3f -> %.3f" % (pico_p, pico_5))
dpie = float((alt_5["pi_e"] - base_5["pi_e"]).min())
ok(dpie < 0, "aperto monetario reduz a expectativa endogena", "%.4f p.p." % dpie)


print("\n" + ("%d FALHA(S)" % falhas if falhas else "todos os testes passaram"))
sys.exit(1 if falhas else 0)
