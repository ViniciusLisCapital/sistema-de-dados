# -*- coding: utf-8 -*-
"""Testa a leitura da curva DI reuniao a reuniao da aba Expectativas de Juros.

Roda com:
    uv run python tests/test_expectativas_juros.py

Script com asserts, nao pytest (mesmo padrao de tests/test_condicionais.py). As secoes 1, 2 e
5 nao tocam no banco; a 3, a 4 e a 6 leem `br_di_grade`, `pm_copom_reuniao` e
`pm_copom_calendario`.

A secao 4 e a conferencia de que a leitura da curva esta CERTA -- que o degrau de cada
reuniao cai na reuniao e nao na vizinha. Ela nao aparece na tela, por decisao do usuario
(2026-09-24): a aba mostra o que a pesquisa espera e o que a curva precifica, e nao pontua
nenhuma das duas contra o Copom. Mas a conferencia precisa existir em algum lugar, e o
lugar e aqui.

O que se testa, e cada item erra sem levantar nada se quebrar:

1. o calendario de dias uteis e o da EPOCA do pregao -- o 20 de novembro so conta depois da
   Lei 14.759 --, senao todo pregao de antes de 2024 le nov/2024 com um dia a menos;
2. sem suavizacao, `caminho_di()` devolve EXATAMENTE a escada que gerou uma curva sintetica,
   com a curva em todo dia util ou so nos vencimentos mensais, e com reuniao no fim do mes --
   um degrau que comecasse no dia da decisao em vez do seguinte ja nao fecharia. COM ela
   (o default), 1 p.b. a mais num contrato so deixa de virar um degrau, um ciclo de ritmo
   constante volta a menos de 3 p.b., e as taxas dos contratos continuam reproduzidas;
3. o calendario reproduz o `du` que a B3 publica em cada vertice;
4. no pregao do dia de cada decisao desde 2006, a taxa que a curva precifica para aquela
   reuniao fica a menos de 50 p.b. do que o Copom decidiu -- um deslocamento de uma reuniao
   erraria por um ciclo inteiro nos anos de ciclo;
5. com os contratos e as datas da tela de CDI implicito da Bloomberg de 24/09/2026, o
   caminho fica a menos de 2,5 p.b. do dela em toda reuniao ate dez/2027 -- e o gabarito
   externo da suavizacao, e o que impede o peso dela de mudar sem ninguem perceber;
6. as reunioes de 2027 saem nas datas que o BC publicou, e as estimadas caem numa quarta; e no
   pregao de 22/09/2026, cuja curva da B3 e exatamente a da tela da Bloomberg, o caminho da
   producao fica a menos de 2 p.b. do dela ate dez/2027.
"""
from __future__ import annotations

import datetime as dt
import sys

import numpy as np

from analytics.brasil.monetary_policy import expectativas_juros as ej

falhas = 0


def check(nome, cond, detalhe=""):
    global falhas
    if cond:
        print("  ok     " + nome)
    else:
        falhas += 1
        print("  FALHA  " + nome + (("  -- " + str(detalhe)) if detalhe else ""))


D = dt.date

print("1. calendario de dias uteis da epoca do pregao")
check("antes da Lei 14.759, 20/11/2024 nao e feriado",
      D(2024, 11, 20) not in ej.feriados(2024, D(2023, 6, 1)))
check("depois dela, e", D(2024, 11, 20) in ej.feriados(2024, D(2024, 1, 2)))
f26 = set(ej.feriados(2026, D(2026, 9, 23)))
check("carnaval, sexta-feira santa e Corpus Christi de 2026 saem da Pascoa",
      {D(2026, 2, 16), D(2026, 2, 17), D(2026, 4, 3), D(2026, 6, 4)} <= f26)
check("um pregao de 2021 conta nov/2024 com um dia util a mais que um de 2024",
      ej.dias_uteis(D(2024, 11, 1), D(2024, 12, 1), D(2021, 10, 13))
      == ej.dias_uteis(D(2024, 11, 1), D(2024, 12, 1), D(2024, 6, 3)) + 1)
check("dias uteis contam [a, b): 23/09/2026 a 01/10/2026 sao 6 (o du publicado pela B3)",
      ej.dias_uteis(D(2026, 9, 23), D(2026, 10, 1), D(2026, 9, 23)) == 6)


def curva_de(pregao, cdi0, degraus, ate_du, so_vencimentos=False):
    """A grade (du, taxa) que uma escada de CDI produz: `degraus` = [(decisao, cdi_depois)].
    O degrau vale a partir do overnight do dia util seguinte a decisao."""
    ini = [(ej.dias_uteis(pregao, d, pregao) + 1, r) for d, r in degraus]
    x = np.full(ate_du, np.log1p(cdi0 / 100) / 252)
    for s, r in ini:
        x[s:] = np.log1p(r / 100) / 252
    lnF = np.cumsum(x)                       # lnF[du-1] = soma dos du primeiros overnights
    du = np.arange(1, ate_du + 1)
    if so_vencimentos:
        venc = {ej.dias_uteis(pregao, t, pregao) for t in ej._primeiros_dias_uteis(pregao, 30)}
        manter = np.array([d == 1 or d in venc for d in du])
        du, lnF = du[manter], lnF[manter]
    taxa = np.expm1(lnF * 252 / du) * 100
    return du, taxa


print("2. sem suavizacao, a escada que gerou a curva volta exata")
P = D(2026, 9, 23)
SEM = 0.0
esc = [(D(2026, 11, 4), 13.40), (D(2026, 12, 9), 13.15), (D(2027, 1, 27), 12.90),
       (D(2027, 3, 17), 12.90), (D(2027, 5, 5), 12.65), (D(2027, 6, 16), 12.40),
       (D(2027, 7, 28), 12.40), (D(2027, 9, 15), 12.15)]
for nome, venc in (("curva em todo dia util", False), ("curva so nos vencimentos mensais", True)):
    du, tx = curva_de(P, 13.65, esc, 520, venc)
    c0, cam = ej.caminho_di(P, du, tx, [d for d, _ in esc], suavizacao=SEM)
    check(nome + ": o CDI do primeiro overnight e o de hoje", abs(c0 - 13.65) < 1e-9, c0)
    check(nome + ": todos os degraus voltam", len(cam) == len(esc), len(cam))
    check(nome + ": cada degrau exato", max(abs(a - r) for a, (_, r) in zip(cam, esc)) < 1e-6,
          [round(a - r, 8) for a, (_, r) in zip(cam, esc)])
# Reuniao no penultimo dia util do mes: o degrau dela cobre um dia so daquele mes, e so o
# mes seguinte o identifica.
esc_fim = [(D(2026, 10, 29), 13.40), (D(2026, 12, 9), 13.15), (D(2027, 1, 27), 13.15)]
du, tx = curva_de(P, 13.65, esc_fim, 400, True)
c0, cam = ej.caminho_di(P, du, tx, [d for d, _ in esc_fim], suavizacao=SEM)
check("reuniao no fim do mes: ainda exato", max(abs(a - r) for a, (_, r) in zip(cam, esc_fim)) < 1e-6,
      [round(a - r, 8) for a, (_, r) in zip(cam, esc_fim)])
# Reuniao alem do horizonte da conta: fica de fora em vez de receber numero.
longe = esc + [(D(2029, 6, 20), 10.0)]
du, tx = curva_de(P, 13.65, longe, 1200)
_, cam = ej.caminho_di(P, du, tx, [d for d, _ in longe])
check("reuniao alem de %d meses fica de fora" % ej.HORIZONTE_MESES, len(cam) == len(esc), len(cam))
# O degrau comeca no dia SEGUINTE a decisao: uma curva gerada com o degrau no proprio dia nao
# volta exata -- e o que prova que a convencao esta sendo exercida, nao so ecoada.
du, tx = curva_de(P, 13.65, [(d - dt.timedelta(1) if d.weekday() else d, r) for d, r in esc], 520)
_, cam = ej.caminho_di(P, du, tx, [d for d, _ in esc], suavizacao=SEM)
check("e uma escada deslocada de um dia nao volta exata (a convencao importa)",
      max(abs(a - r) for a, (_, r) in zip(cam, esc)) > 1e-4)

print("2b. com a suavizacao da producao")
dec8 = [d for d, _ in esc]


def taxas_da_escada(c0, cam, du):
    """A taxa de cada vencimento que uma escada implica -- para medir o quanto ela erra."""
    ini = [ej.dias_uteis(P, m, P) + 1 for m in dec8][:len(cam)]
    lo = np.array([0] + ini, float)[None, :]
    hi = np.array(ini + [np.inf], float)[None, :]
    n = np.clip(np.minimum(du.astype(float)[:, None], hi) - lo, 0, None)
    return np.expm1((n @ np.log1p(np.array([c0] + cam) / 100)) / du) * 100


# 1 p.b. a mais num contrato so, numa curva de Selic parada: sem suavizacao vira um degrau de
# varios p.b.; com ela, fica abaixo de 1. E o zigue-zague que a suavizacao existe para tirar.
du, tx = curva_de(P, 13.65, [(d, 13.65) for d in dec8], 520, True)
bump = tx.copy()
bump[8] += 0.01
_, sem = ej.caminho_di(P, du, bump, dec8, suavizacao=SEM)
_, com = ej.caminho_di(P, du, bump, dec8)
check("1 p.b. num contrato: vira degrau de %.1f p.b. sem suavizacao, %.1f com ela"
      % (100 * max(abs(v - 13.65) for v in sem), 100 * max(abs(v - 13.65) for v in com)),
      max(abs(v - 13.65) for v in sem) > 0.05 and max(abs(v - 13.65) for v in com) < 0.01)
# Um ciclo de ritmo constante e o caso que a suavizacao favorece: volta quase inteiro.
cic = [(d, 13.65 - 0.25 * (i + 1)) for i, d in enumerate(dec8)]
du, tx = curva_de(P, 13.65, cic, 520, True)
_, cam = ej.caminho_di(P, du, tx, dec8)
check("ciclo de 25 p.b. por reuniao volta a menos de 3 p.b.",
      max(abs(a - r) for a, (_, r) in zip(cam, cic)) < 0.03,
      [round(100 * (a - r), 1) for a, (_, r) in zip(cam, cic)])
# Com pausa no meio do ciclo, a reuniao pode sair alguns p.b. longe (a curva nao distingue
# pausa de ritmo constante a um ano de distancia), mas as taxas continuam reproduzidas.
du, tx = curva_de(P, 13.65, esc, 520, True)
c0, cam = ej.caminho_di(P, du, tx, dec8)
erro = np.abs(taxas_da_escada(c0, cam, du) - tx).max()
check("com pausa no ciclo, as taxas dos contratos voltam a menos de 1,5 p.b. (%.2f)" % (100 * erro),
      erro < 0.015)

print("3. o calendario reproduz o du que a B3 publica")
from analytics.brasil.monetary_policy.dados import q  # noqa: E402

g = q("macro_brasil", "SELECT g.date, g.dc, g.du FROM br_di_grade g JOIN "
                      "(SELECT MIN(date) d FROM br_di_grade GROUP BY YEAR(date), QUARTER(date)) w "
                      "ON g.date = w.d WHERE g.du <= 800")
ruins = [(r.date, r.dc, r.du) for r in g.itertuples()
         if ej.dias_uteis(r.date, r.date + dt.timedelta(int(r.dc)), r.date) != int(r.du)]
check("%d vertices de %d pregoes (o primeiro de cada trimestre desde 2006), ate 800 dias uteis"
      % (len(g), g["date"].nunique()), len(g) > 5000 and not ruins, ruins[:5])

print("4. no dia de cada decisao, a curva precifica a propria reuniao (conferencia, nao vai a tela)")
reun = ej.reunioes(2027)
dec = [r for r in reun if r["selic"] is not None and not r["est"]]
pregoes = q("macro_brasil", "SELECT DISTINCT date FROM br_di_grade")["date"].tolist()
pregoes = sorted(pregoes)
import bisect  # noqa: E402

erros, n = [], 0
for k, r in enumerate(dec[1:], 1):
    i = bisect.bisect_right(pregoes, r["date"]) - 1
    if i < 0 or pregoes[i] <= dec[k - 1]["date"]:
        continue
    p = pregoes[i]
    gg = q("macro_brasil", "SELECT du, value FROM br_di_grade WHERE date = '%s' ORDER BY du" % p)
    c0, cam = ej.caminho_di(p, gg["du"].to_numpy(), gg["value"].astype(float).to_numpy(),
                            [x["date"] for x in reun if x["date"] >= p])
    if not cam:
        continue
    vig = dec[k - 1]["selic"]
    n += 1
    erros.append((abs(cam[0] + (vig - c0) - r["selic"]), r["date"]))
pior = max(erros)
check("%d reunioes desde 2006: nenhuma a 50 p.b. ou mais da decisao (pior: %.0f p.b., %s)"
      % (n, pior[0] * 100, pior[1]), n > 150 and pior[0] < 0.5, pior)

# A tela "CDI Estimate" da Bloomberg em dois pregoes, lida de print enviado pelo usuario em
# 2026-09-25: o vencimento e a taxa "Last" de cada DI1, e o CDI depois de cada reuniao
# ("COPOM + CDI"), com a data de vigencia dela ("COPOM Eff", o dia util seguinte a decisao).
# O CDI de hoje e o BZDIOVRA da mesma tela.
BBG_VENC = [D(2026, 10, 1), D(2026, 11, 3), D(2026, 12, 1), D(2027, 1, 4), D(2027, 2, 1),
            D(2027, 3, 1), D(2027, 4, 1), D(2027, 5, 3), D(2027, 6, 1), D(2027, 7, 1),
            D(2027, 8, 2), D(2027, 9, 1), D(2027, 10, 1), D(2027, 11, 1), D(2027, 12, 1),
            D(2028, 1, 3), D(2028, 4, 3)]
BBG_VIGENCIA = [D(2026, 11, 5), D(2026, 12, 10), D(2027, 1, 28), D(2027, 3, 18), D(2027, 4, 29),
                D(2027, 6, 17), D(2027, 8, 5), D(2027, 9, 23), D(2027, 10, 28), D(2027, 12, 9)]
BBG = {
    D(2026, 9, 22): ([13.653, 13.654, 13.580, 13.532, 13.507, 13.505, 13.500, 13.495, 13.490,
                      13.497, 13.491, 13.488, 13.495, 13.489, 13.483, 13.485, 13.514],
                     [13.477, 13.429, 13.446, 13.468, 13.478, 13.480, 13.484, 13.505, 13.550,
                      13.619]),
    D(2026, 9, 24): ([13.653, 13.655, 13.592, 13.565, 13.535, 13.555, 13.580, 13.575, 13.585,
                      13.620, 13.615, 13.630, 13.655, 13.650, 13.635, 13.675, 13.720],
                     [13.516, 13.504, 13.573, 13.641, 13.693, 13.725, 13.746, 13.767, 13.800,
                      13.846]),
}
BBG_CDI = 13.65

print("5. com os contratos e as datas da Bloomberg, o caminho dela (gabarito da suavizacao)")
p, (taxas, caminho_bbg) = D(2026, 9, 24), BBG[D(2026, 9, 24)]
dec_bbg = [pd_ - dt.timedelta(1) for pd_ in BBG_VIGENCIA]      # todas de quinta: a decisao e a quarta
venc_du = np.array([1] + [ej.dias_uteis(p, t, p) for t in BBG_VENC])
_, cam = ej.caminho_di(p, venc_du, np.array([BBG_CDI] + taxas), dec_bbg)
dif = [100 * (a - b) for a, b in zip(cam, caminho_bbg)]
check("24/09/2026: as 10 reunioes ate dez/2027 a menos de 2,5 p.b. da Bloomberg (pior %.1f)"
      % max(map(abs, dif)), len(cam) >= 10 and max(map(abs, dif)) < 2.5, [round(x, 1) for x in dif])
_, cam = ej.caminho_di(p, venc_du, np.array([BBG_CDI] + taxas), dec_bbg, suavizacao=SEM)
dif0 = [100 * (a - b) for a, b in zip(cam, caminho_bbg)]
check("e sem suavizacao, nao fica (pior %.1f p.b.): e ela que a Bloomberg faz" % max(map(abs, dif0)),
      max(map(abs, dif0)) > 5)

print("6. datas oficiais, estimadas numa quarta, e a producao contra a Bloomberg")
cal = q("macro_brasil", "SELECT date FROM pm_copom_calendario WHERE YEAR(date) = 2027 ORDER BY date")
oficial = [x for x in cal["date"]]
de_2027 = [r for r in ej.reunioes(2028) if r["date"].year == 2027]
check("as 8 reunioes de 2027 saem nas datas que o BC publicou, marcadas como reais",
      len(oficial) == 8 and [r["date"] for r in de_2027] == oficial
      and not any(r["est"] for r in de_2027), [(r["date"], r["est"]) for r in de_2027])
check("e sao as da Bloomberg (a decisao e o dia util antes da vigencia)",
      oficial == dec_bbg[2:], (oficial, dec_bbg[2:]))
est = [r for r in ej.reunioes(2029) if r["est"]]
check("%d reunioes estimadas, todas numa quarta-feira" % len(est),
      len(est) >= 8 and all(r["date"].weekday() == 2 for r in est),
      [r["date"] for r in est if r["date"].weekday() != 2])
p = D(2026, 9, 22)
gg = q("macro_brasil", "SELECT du, value FROM br_di_grade WHERE date = '%s' ORDER BY du" % p)
cdi0, cam = ej.caminho_di(p, gg["du"].to_numpy(), gg["value"].astype(float).to_numpy(),
                          [r["date"] for r in ej.reunioes(2029) if r["date"] >= p])
dif = [100 * (a - b) for a, b in zip(cam, BBG[p][1])]
check("22/09/2026, curva da B3 e datas da producao: 10 reunioes a menos de 2 p.b. da Bloomberg "
      "(pior %.1f)" % max(map(abs, dif)), max(map(abs, dif)) < 2, [round(x, 1) for x in dif])

print("")
print(("%d FALHA(S)" % falhas) if falhas else "todos os asserts passaram")
sys.exit(1 if falhas else 0)
