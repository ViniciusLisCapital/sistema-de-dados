# -*- coding: utf-8 -*-
"""Testa a resolucao de conjunto de informacao da aba Condicoes para a reuniao do Copom.

Roda com:
    uv run python tests/test_condicoes_copom.py

Segue o padrao de tests/test_eq5_expectativas.py: script executavel com asserts, nao
pytest (o projeto nao tem pytest configurado). **Nao toca no banco** -- tudo aqui roda
sobre o `calendar_2026.yaml` e sobre series sinteticas, que e justamente o que permite
testar cortes em datas escolhidas a mao.

O harness JS (secao 32 de tests/test_monetary_policy_js.js) cobre o payload ja pronto:
que nenhuma celula da coluna "na reuniao" veio de divulgacao posterior ao corte, que as
categorias do resumo particionam, que a cor sai do z. O que ele NAO alcanca e a mecanica
que produz aquelas datas -- e e ali que mora o risco, porque errar por um mes nao levanta
excecao nenhuma: devolve um numero plausivel do periodo errado.

O que se testa aqui:

1. contagem de dia util (ida e volta), que e a base da regra ajustada;
2. a regra ajustada de cada grupo reproduz as proprias entradas do calendario;
3. `divulgacao()` prefere a entrada exata e so estima onde nao ha;
4. o horario importa -- o IC-Br de julho saiu as 14:30 do dia da 280a reuniao, e
   move-lo para depois das 18:30 tira a linha do conjunto de informacao;
5. `ref_divulgado()` nao devolve periodo cuja divulgacao e posterior ao corte, varrido
   dia a dia por tres meses contra uma checagem independente;
6. a fronteira do IPCA: no dia da 280a reuniao o ultimo IPCA divulgado e o de junho, e o
   de julho so entra depois -- o anacronismo que a aba existe para nao cometer;
7. `reunioes()` separa por CORTE, nao por data: no proprio dia 2, antes das 18:30, a
   reuniao em curso ainda e a proxima;
8. o sigma robusto nao se deixa sequestrar por um outlier;
9. o ajuste sazonal reduz a variancia em vez de aumenta-la (a regressao que a janela de
   1980 causava).
"""
from __future__ import annotations

import datetime as dt
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1]))

from analytics.brasil.monetary_policy import condicoes_copom as CC  # noqa: E402

_falhas = 0


def ok(cond, nome, detalhe=""):
    global _falhas
    if cond:
        print("  ok   %s" % nome)
    else:
        _falhas += 1
        print("  FALHA %s%s" % (nome, ("  -- " + str(detalhe)) if detalhe else ""))


# ── 1. dia util ──────────────────────────────────────────────────────────────
print("\n1. Contagem de dia util")
# 2026-08-01 e sabado; o primeiro dia util de agosto/2026 e segunda, dia 3.
ok(CC._data_dia_util(2026, 8, 1) == dt.date(2026, 8, 3),
   "1o dia util de ago/2026 cai na segunda", CC._data_dia_util(2026, 8, 1))
ok(CC._dia_util(dt.date(2026, 8, 3)) == 1, "e a volta devolve 1")
# 9o dia util de agosto/2026: 3,4,5,6,7 (5), 10,11,12,13 (9) -> dia 13.
ok(CC._data_dia_util(2026, 8, 9) == dt.date(2026, 8, 13),
   "9o dia util de ago/2026 e o dia 13", CC._data_dia_util(2026, 8, 9))
# Ida e volta em 3 anos de dias uteis.
d = dt.date(2024, 1, 1)
bad = []
while d < dt.date(2027, 1, 1):
    if np.is_busday(np.datetime64(d, "D")):
        k = CC._dia_util(d)
        if CC._data_dia_util(d.year, d.month, k) != d:
            bad.append(d)
    d += dt.timedelta(days=1)
ok(not bad, "ida e volta fecha em todo dia util de 2024-2026", bad[:5])


# ── 2. a regra ajustada reproduz as entradas do calendario ───────────────────
print("\n2. A regra ajustada reproduz as proprias entradas do calendario")
GS = CC.grupos()
# Tolerancia MEDIDA, uma por grupo, nao um numero unico: IPCA e IPCA-15 sao ancorados no
# mes e fecham em poucos dias; o IC-Br sai em cadencia de 4-5 semanas ancorada em
# quarta-feira, que nenhuma regra mensal reproduz. Ver a docstring de `regra()`.
# `ibge_pnad_mensal` e `bcb_caged_sgs_mirror` entram aqui porque sao os dois grupos cuja
# ESTIMATIVA e de fato exercida: o calendario so os cobre de 27/08 em diante, e a coluna
# "na reuniao" de desocupacao e CAGED depende da regra ajustada acertar julho/2026.
LIMITE = {"ibge_ipca": 4, "ibge_ipca15": 4, "bcb_icbr": 5,
          "ibge_pnad_mensal": 4, "bcb_caged_sgs_mirror": 4, "bcb_ibcbr": 5}
for nome in ("ibge_ipca", "ibge_ipca15", "bcb_icbr", "ibge_pnad_mensal",
             "bcb_caged_sgs_mirror", "bcb_ibcbr"):
    g = GS[nome]
    r = CC.regra(g)
    ok(r is not None, "%s tem regra ajustada" % nome)
    if r is None:
        continue
    defas, dia, erro = r
    # `erro` e o proprio maximo medido; o teste cobra que ele seja REAL, nao otimista.
    pior = 0
    for e in g["entries"]:
        ref = CC._ref(e.get("reference_period"))
        if ref is None:
            continue
        m = ref + defas
        pior = max(pior, abs((CC._data_dia_util(m.year, m.month, dia)
                              - CC._data(e["date"])).days))
    ok(pior == erro, "%s: o erro declarado pela regra e o maximo medido" % nome,
       "%d vs %d" % (erro, pior))
    ok(erro <= LIMITE[nome], "%s: erro dentro do esperado (<=%d dias)" % (nome, LIMITE[nome]),
       "%d dias" % erro)
# A defasagem e o que separa os dois: o IPCA-15 do mes M sai DENTRO do mes M; o IPCA
# fechado, no mes seguinte. Trocar os dois deslocaria a coluna inteira em um mes.
ok(CC.regra(GS["ibge_ipca"])[0] == 1, "IPCA: defasagem de 1 mes",
   CC.regra(GS["ibge_ipca"])[0])
ok(CC.regra(GS["ibge_ipca15"])[0] == 0, "IPCA-15: divulgado no proprio mes de referencia",
   CC.regra(GS["ibge_ipca15"])[0])
ok(CC.regra(GS["bcb_icbr"])[0] == 1, "IC-Br: defasagem de 1 mes",
   CC.regra(GS["bcb_icbr"])[0])
# PNAD e CAGED saem no fim do mes SEGUINTE ao de referencia; o IBC-Br, dois meses depois.
# Errar isso deslocaria a coluna "na reuniao" das tres linhas de atividade em um mes.
ok(CC.regra(GS["ibge_pnad_mensal"])[0] == 1, "PNAD mensal: defasagem de 1 mes",
   CC.regra(GS["ibge_pnad_mensal"])[0])
ok(CC.regra(GS["bcb_caged_sgs_mirror"])[0] == 1, "CAGED (espelho SGS): defasagem de 1 mes",
   CC.regra(GS["bcb_caged_sgs_mirror"])[0])
ok(CC.regra(GS["bcb_ibcbr"])[0] == 2, "IBC-Br: defasagem de 2 meses",
   CC.regra(GS["bcb_ibcbr"])[0])
# E a estimativa que a aba realmente usa hoje: 06/2026 de PNAD e CAGED, que na 280a
# reuniao (05/08 18:30) ja tinha saido, e cuja divulgacao o arquivo nao cobre.
for nome in ("ibge_pnad_mensal", "bcb_caged_sgs_mirror"):
    q6, ex6 = CC.divulgacao(GS[nome], pd.Period("2026-06", "M"))
    ok(not ex6 and dt.date(2026, 7, 20) <= q6.date() <= dt.date(2026, 8, 4),
       "%s: 06/2026 estimado no fim de julho, antes do corte da 280a" % nome, q6)


# ── 3. exata vence estimada ──────────────────────────────────────────────────
print("\n3. divulgacao() prefere a entrada do calendario e so estima onde nao ha")
q, exata = CC.divulgacao(GS["bcb_icbr"], pd.Period("2026-07", "M"))
ok(exata and q == dt.datetime(2026, 8, 5, 14, 30),
   "IC-Br 07/2026 vem exato do calendario, com hora", "%s exata=%s" % (q, exata))
q, exata = CC.divulgacao(GS["ibge_ipca"], pd.Period("2026-08", "M"))
ok(exata and q.date() == dt.date(2026, 9, 11),
   "IPCA 08/2026 vem exato do calendario", "%s exata=%s" % (q, exata))
q, exata = CC.divulgacao(GS["ibge_ipca"], pd.Period("2026-06", "M"))
ok(not exata and q is not None,
   "IPCA 06/2026 (antes da cobertura do arquivo) sai estimado", "%s exata=%s" % (q, exata))
ok(dt.date(2026, 7, 1) <= q.date() <= dt.date(2026, 7, 20),
   "e a estimativa cai na primeira metade de julho", q)


# ── 4. o horario nao e enfeite ───────────────────────────────────────────────
print("\n4. O horario entra na comparacao")
corte_280 = dt.datetime(2026, 8, 5, 18, 30)
refs = pd.period_range("2025-01", "2026-12", freq="M")
ref, _ = CC.ref_divulgado(GS["bcb_icbr"], corte_280, refs)
ok(str(ref) == "2026-07",
   "IC-Br: 07/2026 saiu as 14:30 do dia da reuniao, entrou no conjunto", str(ref))
# Mesmo dia, decisao movida para as 12:00 -- o IC-Br ainda nao teria saido.
ref_cedo, _ = CC.ref_divulgado(GS["bcb_icbr"], dt.datetime(2026, 8, 5, 12, 0), refs)
ok(str(ref_cedo) == "2026-06",
   "com decisao ao meio-dia o IC-Br de julho fica de fora", str(ref_cedo))


# ── 5. ref_divulgado nunca devolve periodo do futuro ─────────────────────────
print("\n5. ref_divulgado() varrido dia a dia contra checagem independente")
for nome in ("ibge_ipca", "ibge_ipca15", "bcb_icbr", "ibge_pnad_mensal",
             "bcb_caged_sgs_mirror", "bcb_ibcbr"):
    g = GS[nome]
    ruins = []
    d = dt.date(2026, 7, 1)
    while d <= dt.date(2026, 9, 30):
        corte = dt.datetime.combine(d, dt.time(18, 30))
        ref, _ = CC.ref_divulgado(g, corte, refs)
        if ref is not None:
            quando, _ = CC.divulgacao(g, ref)
            seguinte, _ = CC.divulgacao(g, ref + 1)
            # O escolhido ja saiu, e o seguinte ainda nao: e a definicao de "ultimo".
            if quando > corte or (seguinte is not None and seguinte <= corte):
                ruins.append((str(d), str(ref)))
        d += dt.timedelta(days=1)
    ok(not ruins, "%s: escolha e sempre o ultimo ja divulgado" % nome, ruins[:5])


# ── 6. a fronteira do IPCA na 280a reuniao ───────────────────────────────────
print("\n6. A fronteira que a aba existe para respeitar")
ref_ipca, _ = CC.ref_divulgado(GS["ibge_ipca"], corte_280, refs)
ok(str(ref_ipca) == "2026-06",
   "na 280a reuniao (05/08) o ultimo IPCA divulgado e o de JUNHO", str(ref_ipca))
# O ingenuo -- ultimo ponto do banco com data <= reuniao -- daria julho, que so sai
# em ~13/08. Esse e o anacronismo.
ingenuo = [r for r in refs if r.to_timestamp() <= pd.Timestamp(corte_280)][-1]
ok(str(ingenuo) == "2026-08" and ingenuo != ref_ipca,
   "o corte ingenuo por data de referencia daria outro mes", str(ingenuo))
hoje_ref, _ = CC.ref_divulgado(GS["ibge_ipca"], dt.datetime(2026, 8, 25, 23, 59), refs)
ok(str(hoje_ref) == "2026-07", "e em 25/08 ja e o de julho", str(hoje_ref))


# ── 7. reunioes() separa por corte, nao por data ─────────────────────────────
print("\n7. reunioes() separa pelo corte da decisao")
ant, prox = CC.reunioes(dt.datetime(2026, 8, 25, 10, 0))
ok(ant["date"] == dt.date(2026, 8, 5) and prox["date"] == dt.date(2026, 9, 16),
   "em 25/08: 05/08 -> 16/09", "%s -> %s" % (ant["date"], prox["date"]))
# Dia 1 da 281a reuniao: a decisao ainda nao saiu.
ant, prox = CC.reunioes(dt.datetime(2026, 9, 15, 17, 0))
ok(prox["date"] == dt.date(2026, 9, 16) and ant["date"] == dt.date(2026, 8, 5),
   "no dia 1 da reuniao ela ainda e a PROXIMA", "%s -> %s" % (ant["date"], prox["date"]))
# Dia 2, antes das 18:30: idem.
ant, prox = CC.reunioes(dt.datetime(2026, 9, 16, 15, 0))
ok(prox["date"] == dt.date(2026, 9, 16),
   "no dia 2 antes das 18:30 tambem", "%s -> %s" % (ant["date"], prox["date"]))
# Dia 2, depois do comunicado: virou a anterior.
ant, prox = CC.reunioes(dt.datetime(2026, 9, 16, 19, 0))
ok(ant["date"] == dt.date(2026, 9, 16) and prox["date"] == dt.date(2026, 11, 4),
   "depois do comunicado ela vira a ANTERIOR e a aba se renova",
   "%s -> %s" % (ant["date"], prox["date"]))
ok(ant["corte"] == dt.datetime(2026, 9, 16, 18, 30), "corte e o dia 2 as 18:30", ant["corte"])
ok(ant["date_start"] == dt.date(2026, 9, 15), "date_start e o dia 1", ant["date_start"])


# ── 8. sigma robusto ─────────────────────────────────────────────────────────
print("\n8. Sigma robusto nao se deixa sequestrar por um outlier")
idx = pd.period_range("2010-01", "2026-07", freq="M")
rng = np.random.default_rng(7)
base = pd.Series(np.cumsum(rng.normal(0, 1.0, len(idx))), index=idx)
s_limpo = CC._sigma(base, 1)
sujo = base.copy()
sujo.iloc[100] += 60.0          # um choque tipo 2020
s_sujo = CC._sigma(sujo, 1)
ok(abs(s_sujo / s_limpo - 1) < 0.25,
   "um outlier de 60 sigma move a escala em menos de 25%%",
   "%.4f -> %.4f" % (s_limpo, s_sujo))
sd_sujo = float(sujo.diff(1).dropna().std())
ok(sd_sujo / s_sujo > 2.0,
   "enquanto o desvio-padrao simples mais que dobra com o mesmo outlier",
   "%.4f vs %.4f" % (sd_sujo, s_sujo))
ok(CC._sigma(base, 0) is None, "k=0 (sem dado novo) nao produz escala")
ok(CC._sigma(base.iloc[:3], 1) is None, "serie curta demais nao produz escala")


# ── 9. o ajuste sazonal reduz a variancia ────────────────────────────────────
print("\n9. STL com fatores congelados reduz a variancia")
m = np.arange(len(idx)) % 12
saz = np.array([0.4, 0.3, -0.1, -0.2, -0.1, 0.0, 0.1, -0.2, 0.0, -0.1, 0.0, 0.3])[m]
r = pd.Series(0.4 + saz + rng.normal(0, 0.10, len(idx)), index=idx)
r_sa = CC._sa(r)
ok(float(r_sa.std()) < float(r.std()),
   "a serie ajustada e menos volatil que a bruta",
   "%.4f vs %.4f" % (float(r_sa.std()), float(r.std())))
# Os fatores sao CONGELADOS: acrescentar meses novos nao pode reescrever o passado, ou a
# coluna "na reuniao passada" mudaria sozinha entre duas geracoes do relatorio.
r2 = pd.concat([r, pd.Series([0.9], index=pd.PeriodIndex(["2026-08"], freq="M"))])
r2_sa = CC._sa(r2)
comum = r_sa.index.intersection(r2_sa.index)
ok(float(np.abs(r_sa[comum] - r2_sa[comum]).max()) < 1e-12,
   "um mes novo no MESMO ano nao mexe em nenhum valor ja ajustado",
   float(np.abs(r_sa[comum] - r2_sa[comum]).max()))

print("\n" + ("%d FALHA(S)" % _falhas if _falhas else "todos os testes passaram"))
sys.exit(1 if _falhas else 0)
