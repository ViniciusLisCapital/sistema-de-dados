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


# ── 10. periodo de referencia TRIMESTRAL ─────────────────────────────────────
print("\n10. Referencia trimestral: a defasagem conta do FIM do trimestre")
# O grupo do PIB rotula por trimestre (`2026-Q2`). Duas coisas quebram se ele for tratado
# como mensal, e nenhuma levanta erro: `_ref` devolveria um mes que nao existe no indice
# trimestral da serie (a linha some), e a defasagem sairia contada do inicio do trimestre
# (o PIB do 2o tri sai ~3 meses depois de JUNHO, nao de abril).
_q = CC._ref("2026-Q2")
ok(_q is not None and str(_q.freqstr).startswith("Q"),
   "'2026-Q2' vira periodo TRIMESTRAL, nao mensal", str(_q) + " / " + str(_q and _q.freqstr))
ok(CC._mes_fim(_q) == (2026, 6), "e o mes-ancora dele e junho, o fim do trimestre",
   str(CC._mes_fim(_q)))
ok(CC._mes_fim(CC._ref("2026-07")) == (2026, 7),
   "num periodo mensal a ancora continua sendo o proprio mes")

_gpib = CC.grupos()["ibge_pib_trimestral"]
_r = CC.regra(_gpib)
ok(_r is not None, "a regra do grupo do PIB e ajustavel com referencia trimestral")
ok(_r and _r[0] == 3, "defasagem de 3 meses do fim do trimestre", str(_r and _r[0]))
_q2, _exata = CC.divulgacao(_gpib, CC._ref("2026-Q2"))
ok(_exata and _q2.date() == dt.date(2026, 9, 1),
   "2026-Q2 casa com a entrada exata do calendario (01/09)", str(_q2))
# E a que o calendario NAO tem sai pela regra, no lugar certo do calendario.
_q1, _exata1 = CC.divulgacao(_gpib, CC._ref("2025-Q4"))
ok((not _exata1) and _q1 is not None and _q1.date().month == 3 and _q1.date().year == 2026,
   "2025-Q4 e estimado em marco de 2026", str(_q1))

# A serie trimestral lida num corte: na reuniao de 10/12/2025 o PIB disponivel era o do
# 3o trimestre (divulgado em 02/12), e nao o do 4o, que so sai em marco.
_pib = CC.pib_acum_4t("pib_pm")
_ref3 = CC._valor_em(_pib, dt.datetime(2025, 12, 10, 18, 30), _gpib)["ref"]
ok(str(_ref3) == "2025Q3", "em 10/12/2025 o PIB disponivel e o 3T2025", str(_ref3))
_ref2 = CC._valor_em(_pib, dt.datetime(2025, 11, 5, 18, 30), _gpib)["ref"]
ok(str(_ref2) == "2025Q2", "e um mes antes ainda era o 2T2025", str(_ref2))


# ── 11. duas entradas para o mesmo periodo: vale a mais tarde ────────────────
print("\n11. Referencia duplicada no calendario: vale a divulgacao MAIS TARDE")
# Nao e hipotetico: `bcb_credit_note` carimba 2026-06 em 01/07 e de novo em 30/07, e a
# cadencia do grupo (abril->28/05, junho->30/07, julho->28/08) mostra que a primeira e um
# rotulo errado do ICS. Pegar a primeira faria o dado de junho aparecer um mes antes de
# existir -- o anacronismo que o modulo existe para nao cometer.
_falso = {"entries": [
    {"date": "2026-07-01", "reference_period": "2026-06", "time": "08:30"},
    {"date": "2026-07-30", "reference_period": "2026-06", "time": "08:30"},
    {"date": "2026-08-28", "reference_period": "2026-07", "time": "08:30"},
    {"date": "2026-09-29", "reference_period": "2026-08", "time": "08:30"},
]}
_qd, _ed = CC.divulgacao(_falso, pd.Period("2026-06", freq="M"))
ok(_ed and _qd.date() == dt.date(2026, 7, 30),
   "com duas entradas para 2026-06 vale 30/07, nao 01/07", str(_qd))
# E o ajuste da regra tambem usa uma so por referencia, senao o erro maximo do grupo
# explode e passa a marcar como ambigua toda celula que ele alimenta.
_rd = CC.regra(_falso)
ok(_rd is not None and _rd[2] <= 3,
   "o erro da regra fica pequeno porque a duplicata nao entra no ajuste",
   str(_rd and _rd[2]))
_gcred = CC.grupos()["bcb_credit_note"]
ok(CC.regra(_gcred)[2] <= 5,
   "e o grupo real de credito tambem (era 27 dias com a duplicata dentro)",
   str(CC.regra(_gcred)[2]))


# ── 12. a janela de reunioes ────────────────────────────────────────────────
print("\n12. janela_reunioes(): N passadas + a proxima, cortada em AGORA")
_agora = dt.datetime(2026, 9, 22, 10, 0)
_jan = CC.janela_reunioes(_agora, 8)
ok(len(_jan) == 9, "oito passadas mais a proxima", str(len(_jan)))
ok([r["futura"] for r in _jan] == [False] * 8 + [True],
   "so a ultima e futura")
ok(all(_jan[i]["date"] < _jan[i + 1]["date"] for i in range(len(_jan) - 1)),
   "em ordem crescente de data")
ok(all(r["corte"] <= _agora for r in _jan), "nenhum corte esta no futuro")
ok(_jan[-1]["corte"] == _agora,
   "o corte da coluna futura e AGORA, nao o fechamento da reuniao", str(_jan[-1]["corte"]))
ok(_jan[-1]["corte_reuniao"] > _agora,
   "mas o corte da reuniao fica guardado -- e dele que a agenda depende",
   str(_jan[-1].get("corte_reuniao")))
ok(all(r["corte"] == dt.datetime.combine(r["date"], CC.HORA_DECISAO) for r in _jan[:-1]),
   "as passadas sao cortadas as 18:30 do dia 2")
# A separacao e pelo CORTE: no proprio dia 2 antes das 18:30 a reuniao ainda e a proxima.
_antes = CC.janela_reunioes(dt.datetime(2026, 9, 16, 12, 0), 3)
ok(_antes[-1]["date"] == dt.date(2026, 9, 16) and _antes[-1]["futura"],
   "no dia da reuniao, antes do comunicado, ela ainda e a proxima",
   str(_antes[-1]["date"]))
_depois = CC.janela_reunioes(dt.datetime(2026, 9, 16, 19, 0), 3)
ok(_depois[-2]["date"] == dt.date(2026, 9, 16) and not _depois[-2]["futura"],
   "e depois do comunicado ela vira passada e a janela anda sozinha")
# Rotulo: e o que vai no cabecalho da coluna.
ok(CC._reuniao_label(dt.date(2026, 1, 28)) == "jan/26", "rotulo curto da coluna",
   CC._reuniao_label(dt.date(2026, 1, 28)))


# ── 13. inflacao implicita: Fisher, nao subtracao ───────────────────────────
print("\n13. Inflacao implicita e razao, nao diferenca")
# A subtracao e a aproximacao usual e erra onde os niveis sao altos, que e exatamente a
# faixa brasileira. A forma errada funciona na faixa em que se costuma olhar e quebra onde
# ninguem confere -- mesma licao da identidade produto/horas do relatorio de produtividade.
_n, _r = 14.0, 7.5
_certo = ((1 + _n / 100) / (1 + _r / 100) - 1) * 100
_errado = _n - _r
ok(abs(_certo - 6.0465) < 1e-3, "a 14% e 7,5% a forma correta da 6,05%", "%.4f" % _certo)
ok(abs(_errado - _certo) > 0.4,
   "e a subtracao erra mais de 0,4 p.p. -- maior que o movimento tipico de um mes",
   "%.4f" % (_errado - _certo))
_bei = CC.implicita("24M")
ok(len(_bei) > 1000, "a serie de implicita de 2 anos existe", str(len(_bei)))
_ult = _bei.index.max()
_nom = CC.curva_br("DIPRE", "24M").loc[_ult]
_rea = CC.curva_br("NTNBJS", "24M").loc[_ult]
ok(abs(float(_bei.loc[_ult]) - ((1 + _nom / 100) / (1 + _rea / 100) - 1) * 100) < 1e-9,
   "e ela e a razao das duas curvas, no ultimo pregao")
ok(abs(float(_bei.loc[_ult]) - (_nom - _rea)) > 1e-3,
   "estritamente diferente da subtracao", "%.4f vs %.4f" % (float(_bei.loc[_ult]), _nom - _rea))


# ── 14. horizonte relevante: quatro trimestres que TERMINAM seis a frente ───
print("\n14. Horizonte relevante: 4 trimestres compostos, 6 a frente da pesquisa")
_hr = CC.focus_ipca_hr()
ok(len(_hr) > 50, "a serie do horizonte relevante existe", str(len(_hr)))
_d = CC._focus_tri_ipca()
_ultd = _hr.index.max()
_g = _d[_d["date"] == _ultd].set_index("tri")["mediana"]
_alvo = pd.Period(_ultd, freq="Q") + CC.HR_TRIMESTRES
_jan4 = [_alvo - k for k in range(3, -1, -1)]
_esp = (float(np.prod([1 + _g.loc[t] / 100 for t in _jan4])) - 1) * 100
ok(abs(float(_hr.loc[_ultd]) - _esp) < 1e-9,
   "bate com a composicao dos quatro trimestres que terminam no alvo",
   "%.6f vs %.6f" % (float(_hr.loc[_ultd]), _esp))
ok(str(_alvo - pd.Period(_ultd, freq="Q")) == "<6 * QuarterEnds>" or
   (_alvo.ordinal - pd.Period(_ultd, freq="Q").ordinal) == 6,
   "e o alvo esta exatamente seis trimestres a frente da pesquisa",
   str(_alvo) + " vs " + str(pd.Period(_ultd, freq="Q")))
# Somar as quatro taxas em vez de compor erra pouco, mas erra -- e e de graca nao errar.
_soma = float(sum(_g.loc[t] for t in _jan4))
ok(abs(_soma - _esp) > 1e-4, "somar as quatro taxas nao e o mesmo que compor",
   "%.6f vs %.6f" % (_soma, _esp))
# A janela e ROLANTE: seis trimestres a frente SEMPRE, sem o dente de serra do
# ano-calendario, que encurta de 12 para 4 trimestres ao longo do proprio ano.
_dif = {(pd.Period(d, freq="Q") + CC.HR_TRIMESTRES).ordinal - pd.Period(d, freq="Q").ordinal
        for d in _hr.index}
ok(_dif == {6}, "a distancia ao alvo e a mesma em toda pesquisa", str(_dif))


# -- 15. a projecao do BC: uma observacao por REUNIAO -----------------------
print("\n15. Projecao do BC no horizonte relevante: uma linha por reuniao")
_pb = CC._proj_bc()
ok(len(_pb) > 12, "a serie do comunicado existe", str(len(_pb)))
ok(_pb.index.is_unique, "uma unica projecao por data de comunicado")
ok(_pb.index.is_monotonic_increasing, "e em ordem crescente")
# O filtro que define a linha: so o comunicado. O relatorio sai 7 a 28 dias depois da
# reuniao e e TRIMESTRAL, entao misturar os dois poe no mesmo indice pontos separados
# por ~45 dias e por ~90 -- e `_sigma` mede a variacao por POSICAO, nao por tempo.
_esp = CC.q("macro_brasil",
            "SELECT vintage, date, value FROM pm_copom_projecoes "
            "WHERE horizonte_relevante=1 AND indice='ipca' "
            "AND cenario='juros_esperado' AND documento='relatorio' "
            "AND regime='hr_aproximado'")
ok(len(_esp) > 50, "e ha mesmo um trecho de relatorio que poderia ter entrado",
   str(len(_esp)))
_dias = pd.Series(_pb.index).diff().dt.days.dropna()
ok(float(_dias.median()) < 60,
   "o espacamento mediano da serie escolhida e de uma reuniao, nao de um trimestre",
   "%.0f dias" % _dias.median())
_mix = pd.concat([_pb["value"].astype(float),
                  _esp.assign(vintage=pd.to_datetime(_esp["vintage"]))
                      .set_index("vintage")["value"].astype(float)])
_mix = _mix[~_mix.index.duplicated(keep="last")].sort_index()
_dmix = pd.Series(_mix.index).diff().dt.days.dropna()
ok(float(_dmix.median()) > float(_dias.median()) * 1.5,
   "com o relatorio dentro o espacamento mediano quase dobra",
   "%.0f vs %.0f dias" % (_dmix.median(), _dias.median()))
_s1 = CC._sigma(_pb["value"].astype(float), 1)
_s2 = CC._sigma(_mix, 1)
ok(_s1 is not None and _s2 is not None and _s2 > _s1 * 1.5,
   "e a escala tipica de uma variacao junto com ela -- a cor da linha sairia pela "
   "metade", "%.4f vs %.4f" % (_s2, _s1))

# O rotulo embaixo do valor e o TRIMESTRE PROJETADO, nao a data do comunicado: o
# indice diz quando o numero saiu e o rotulo diz sobre o que ele e.
_alvo = CC.proj_bc_hr_alvo()
_ult = _pb.index.max()
ok(len(_alvo) == len(_pb), "um rotulo de alvo por comunicado", str(len(_alvo)))
_tri = pd.Period(_pb.loc[_ult, "date"], freq="Q")
ok(_alvo[_ult] == CC._rotulo_ref(_tri), "e ele e o trimestre, no formato da tabela",
   _alvo[_ult])
# Duas reunioes seguidas projetam o MESMO trimestre com numeros diferentes -- e por
# isso que nesta linha o rotulo de referencia nao identifica a observacao, e a
# equivalencia "trocou de referencia <-> tem dado novo" que vale nas outras e falsa
# aqui. A aba marca a linha com `ref_alvo` exatamente para nao aplicar aquela regra.
_rot = [_alvo[i] for i in _pb.index[-8:]]
ok(len(set(_rot)) < len(_rot), "o alvo repete entre reunioes seguidas", str(_rot))

# `div_hora`: o indice desta serie E a data de publicacao, e dize-lo e o que poe a
# linha debaixo da mesma fronteira das outras. Sem isso a celula sai sem data de
# divulgacao e o teste do relatorio deixa de checa-la, em silencio.
_r = CC._valor_em(_pb["value"].astype(float),
                  dt.datetime.combine(_ult.date(), CC.HORA_DECISAO), None,
                  div_hora=CC.HORA_DECISAO)
ok(_r["divulgacao"] == _ult.strftime("%d/%m/%Y ") + CC.HORA_DECISAO.strftime("%H:%M"),
   "a leitura no fechamento da reuniao declara o comunicado daquele dia",
   str(_r["divulgacao"]))
ok(CC._valor_em(_pb["value"].astype(float),
                dt.datetime.combine(_ult.date(), CC.HORA_DECISAO), None)["divulgacao"]
   is None,
   "e sem `div_hora` nenhuma data e afirmada -- o default nao inventa publicacao")


print("\n" + ("%d FALHA(S)" % _falhas if _falhas else "todos os testes passaram"))
sys.exit(1 if _falhas else 0)
