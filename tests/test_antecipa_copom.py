"""
Testes de `analytics/brasil/monetary_policy/antecipa_copom.py`.

Cada secao nasceu de um erro que custou uma rodada, e nenhum deles levantava excecao --
todos devolviam numero plausivel e errado. Precisa de MySQL (le as tabelas de projecao, a
Focus e a PTAX); nao roda o modelo, entao e rapido.

    uv run python tests/test_antecipa_copom.py
"""

from __future__ import annotations

import json
import sys

import numpy as np
import pandas as pd

from analytics.brasil.monetary_policy import antecipa_copom as ac

falhas = 0


def ok(cond, nome, detalhe=""):
    global falhas
    if cond:
        print("  ok   " + nome)
    else:
        falhas += 1
        print("  FALHA " + nome + ("  -- " + str(detalhe) if detalhe else ""))


print("\n1. t0: o ultimo trimestre FECHADO, nao o corrente")
# O modelo e trimestral e um trimestre so fecha quando sai o IPCA do ultimo mes dele.
# Usar o trimestre da reuniao poria dado que nao existe no conjunto de informacao.
ok(ac.t0_de(pd.Timestamp("2026-08-05")) == pd.Period("2026Q2", "Q"),
   "reuniao em agosto le ate 2026T2", ac.t0_de(pd.Timestamp("2026-08-05")))
ok(ac.t0_de(pd.Timestamp("2024-12-11")) == pd.Period("2024Q3", "Q"),
   "reuniao em dezembro ainda le 2024T3 (2024T4 nao fechou)",
   ac.t0_de(pd.Timestamp("2024-12-11")))
# fronteira: dia 14 de outubro o IPCA de setembro ja saiu (~dia 10), entao 3T fechou
ok(ac.t0_de(pd.Timestamp("2026-10-16")) == pd.Period("2026Q3", "Q"),
   "16/10 ja tem o 3T fechado", ac.t0_de(pd.Timestamp("2026-10-16")))
ok(ac.t0_de(pd.Timestamp("2026-10-05")) == pd.Period("2026Q2", "Q"),
   "05/10 ainda nao", ac.t0_de(pd.Timestamp("2026-10-05")))

print("\n2. r* e o valor ANUNCIADO pelo BC, degrau por reuniao")
# O BC fixa a neutra e avisa quando muda; nossa estimativa (7,81%) e outro objeto e poe
# 2028T1 0,4 p.p. acima. Confundir os dois foi o que separava 3,45 de 3,07.
ok(ac.r_neutra(262) == 4.50, "antes de jun/2024: 4,50%", ac.r_neutra(262))
ok(ac.r_neutra(263) == 4.75, "263a adota 4,75% (RPM jun/2024 p.74)", ac.r_neutra(263))
ok(ac.r_neutra(266) == 4.75, "segue 4,75% ate a 266a", ac.r_neutra(266))
ok(ac.r_neutra(267) == 5.00, "267a adota 5,00% (RPM dez/2024 p.59)", ac.r_neutra(267))
ok(ac.r_neutra(281) == 5.00, "e continua em 5,00% (reafirmado em jun/2026)",
   ac.r_neutra(281))

print("\n3. Curva de Selic: realizado ate o corte, esperado depois")
# A Focus DESCARTA da curva as reunioes que ja aconteceram -- em 21/08/2026 o primeiro
# rotulo e R6/2026, e a 280a (05/08) sumiu. Como t0 fica meses atras, a janela comeca no
# passado: uma versao anterior segurava um nivel fixo ali e ignorava decisoes ja tomadas.
t0 = pd.Period("2026Q2", "Q")
sel = ac.curva_selic(pd.Timestamp("2026-09-16"), t0, 7)
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

print("\n4. Ancora: 'ano civil' e 'trimestre' no T4 sao o MESMO objeto")
# `date` = 2026-10-01 significa o trimestre 2026T4 OU o ano civil 2026, que a tabela
# normaliza para o T4. O IPCA acumulado nos 4 trimestres ate o T4 E o ano civil, entao
# filtrar por periodo_tipo='trimestre' descarta a linha do comunicado da 270a e pega um
# relatorio dois meses mais velho, sem ganho nenhum.
proj = ac.projecoes_bc()
alvo = pd.Period("2026Q4", "Q")
a271 = ac._ancora(alvo, pd.Timestamp("2025-06-18"), proj)
ok(a271 is not None, "a 271a acha ancora para 2026T4")
if a271:
    ok(a271["documento"] == "comunicado" and a271["vintage"] == pd.Timestamp("2025-05-07"),
       "e a ancora e o comunicado da 270a, o mais recente",
       (a271["documento"], str(a271["vintage"].date())))
    ok(a271["periodo_tipo"] == "ano",
       "que e uma linha de ANO CIVIL -- e nao pode ser filtrada fora",
       a271["periodo_tipo"])

print("\n5. Toda reuniao da era declarada tem ancora, e ela e de UM intervalo atras")
hr = ac.reunioes_hr()
ok(len(hr) == 17, "17 reunioes na era hr_6_trimestres", len(hr))
saltos, lags, sem = [], [], []
for _, r in hr.iterrows():
    alv = pd.Period(r["date"], "Q")
    anc = ac._ancora(alv, pd.Timestamp(r["vintage"]), proj)
    if anc is None:
        sem.append(int(r["nro_reuniao"]))
        continue
    lags.append(anc["defasagem_dias"])
    saltos.append((alv - pd.Period(r["vintage"], "Q")).n)
ok(not sem, "nenhuma reuniao fica sem ancora", sem)
ok(set(saltos) == {6}, "o horizonte relevante e sempre 6 trimestres a frente",
   sorted(set(saltos)))
ok(lags and max(lags) <= 60, "a ancora nunca esta mais de um intervalo atras", max(lags))

print("\n6. O benchmark ingenuo e o numero que qualquer metodo tem de bater")
rev = []
for _, r in hr.iterrows():
    anc = ac._ancora(pd.Period(r["date"], "Q"), pd.Timestamp(r["vintage"]), proj)
    if anc:
        rev.append(float(r["value"]) - anc["valor"])
rs = pd.Series(rev)
ok(abs(rs.abs().mean() - 0.106) < 0.01,
   "|revisao media| ~ 0,106 p.p. (o MAE do ingenuo)", round(rs.abs().mean(), 4))
ok((rs.abs() <= 0.1001).sum() == 13,
   "13 das 17 revisoes cabem num tique de arredondamento",
   int((rs.abs() <= 0.1001).sum()))

print("\n7. Delta da Focus: o metodo que ganha do ingenuo")
# O NIVEL da Focus nao serve (4,02 contra 3,2 do BC para 2028T1); o DELTA serve.
f = ac.focus_4t(pd.Timestamp("2026-08-25"), pd.Period("2028Q1", "Q"))
ok(f is not None and 2.0 < f < 6.0, "focus_4t devolve um acumulado plausivel", f)
ok(f is not None and f > 3.5,
   "e ela roda ACIMA da projecao do BC (3,2), por isso so o delta e usavel", f)
d = ac.delta_focus(pd.Timestamp("2024-12-11"), pd.Timestamp("2024-11-06"),
                   pd.Period("2026Q2", "Q"))
ok(d is not None and d > 0.2,
   "entre a 266a e a 267a a Focus subiu >0,2 p.p. -- a revisao real foi +0,4",
   None if d is None else round(d, 3))

print("\n8. Cambio: observado ate o corte, PPC depois")
de = ac.curva_cambio(pd.Timestamp("2024-12-11"), pd.Period("2024Q3", "Q"), 7)
ok(len(de) == 7 and np.all(np.isfinite(de)), "um valor por trimestre, sem NaN")
ok(de[0] > 3.0, "2024T4 carrega a depreciacao observada do real", round(float(de[0]), 3))
ok(np.allclose(de[1:], de[1]), "e dai em diante e PPC, constante",
   np.round(de[1:], 4).tolist())
# 0,25 = (meta 3 - PI_EXT 2)/4, a mesma definicao de de_ppc dentro do simular()
ok(abs(de[-1] - 0.25) < 1e-9, "e o PPC vale (meta - 2)/4 = 0,25 por trimestre",
   round(float(de[-1]), 4))

print("\n9. Revisao x expansao de horizonte: os dois casos existem e alternam")
# A pergunta pratica e se o metodo so funciona quando o alvo JA tem numero publicado pelo
# comunicado. Nao: o RPM publica o caminho trimestral CONTIGUO, entao o trimestre que o
# comunicado esta estreando ja tem numero la, e e dali que a ancora vem nas 9 expansoes.
tipos = [ac.tipo_horizonte(pd.Period(r["date"], "Q"), pd.Timestamp(r["vintage"]), proj)
         for _, r in hr.iterrows()]
ok(tipos.count("expansao") == 9 and tipos.count("revisao") == 8,
   "9 expansoes e 8 revisoes nas 17", (tipos.count("expansao"), tipos.count("revisao")))
ok(all(tipos[i] != tipos[i - 1] for i in range(1, len(tipos))),
   "e elas alternam sem excecao (2 reunioes por trimestre, 1 RPM por trimestre)", tipos)
docs = [ac._ancora(pd.Period(r["date"], "Q"), pd.Timestamp(r["vintage"]), proj)["documento"]
        for _, r in hr.iterrows()]
ok(all(d == "relatorio" for t, d in zip(tipos, docs) if t == "expansao"),
   "na expansao a ancora e SEMPRE o relatorio -- nunca precisa extrapolar",
   [d for t, d in zip(tipos, docs) if t == "expansao"])
ok(all(d == "comunicado" for t, d in zip(tipos, docs) if t == "revisao"),
   "e na revisao e sempre o comunicado anterior",
   [d for t, d in zip(tipos, docs) if t == "revisao"])

print("\n10. Artefatos que a aba le")
# A aba nao roda o modelo: ela le estes dois arquivos. Se eles sairem de sincronia com o que
# o modulo calcula, o relatorio mostra numero velho sem lancar excecao nenhuma.
B = pd.read_csv(ac._DATA / "antecipa_backtest.csv")
P = json.loads((ac._DATA / "antecipa_previsao.json").read_text(encoding="utf-8"))
ok(len(B) == 17, "o csv tem as 17 reunioes", len(B))
ok({"tipo", "erro", "erro_ingenuo", "erro_focus", "ancora", "real"} <= set(B.columns),
   "e as colunas que a aba usa", sorted(B.columns))
ok(((B["ancora"] + B["delta_modelo"] - B["real"]) - B["erro"]).abs().max() < 1e-9,
   "erro do modelo = ancora + delta - publicado")
ok(((B["ancora"] + B["delta_focus"] - B["real"]) - B["erro_focus"]).abs().max() < 1e-9,
   "idem para a Focus")
ok(B["erro_focus"].abs().mean() < B["erro_ingenuo"].abs().mean() < B["erro"].abs().mean(),
   "e a ordem dos MAEs e focus < ingenuo < modelo",
   (round(B["erro_focus"].abs().mean(), 4), round(B["erro_ingenuo"].abs().mean(), 4),
    round(B["erro"].abs().mean(), 4)))
ok(P["nro"] == int(hr["nro_reuniao"].iloc[-1]) + 1,
   "o json preve a reuniao seguinte a ultima com horizonte declarado", P["nro"])
ok(abs(P["previsto_focus"] - (P["ancora"] + P["delta_focus"])) < 1e-9,
   "e o previsto dele fecha com ancora + delta")

print("\n" + (str(falhas) + " FALHA(S)" if falhas else "todos os testes passaram"))
sys.exit(1 if falhas else 0)
