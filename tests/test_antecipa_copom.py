"""
Testes de `analytics/brasil/monetary_policy/antecipa_copom.py`.

Cada secao nasceu de um erro que custou uma rodada, e nenhum deles levantava excecao --
todos devolviam numero plausivel e errado. Precisa de MySQL (le as tabelas de projecao e a
Focus). Os insumos do cenario do modelo agregado (r*, curva de Selic, cambio) sairam para
`tests/test_antecipa_modelo.py` em 2026-09-24, junto com o modelo.

    uv run python tests/test_antecipa_copom.py
"""

from __future__ import annotations

import json
import sys

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
# Um trimestre so fecha quando sai o IPCA do ultimo mes dele.
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
# A era cresce uma reuniao a cada ~45 dias, entao a asserção e sobre onde ela COMECA, nao
# sobre um total escrito a mao -- o "17" daqui reprovou a 281a no dia em que ela entrou.
ok(len(hr) >= 17 and int(hr["nro_reuniao"].iloc[0]) == 264,
   "a era hr_6_trimestres comeca na 264a e so cresce", (len(hr), int(hr["nro_reuniao"].iloc[0])))
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
ok((rs.abs() <= 0.1001).mean() > 0.5,
   "a maioria das revisoes cabe num tique de arredondamento -- por isso o ingenuo e forte",
   "%d de %d" % (int((rs.abs() <= 0.1001).sum()), len(rs)))

print("\n7. Delta da Focus: o metodo que ganha do ingenuo")
# O NIVEL da Focus nao serve (4,02 contra 3,2 do BC para 2028T1); o DELTA serve.
f = ac.focus_4t(pd.Timestamp("2026-08-25"), pd.Period("2028Q1", "Q"))
ok(f is not None and 2.0 < f < 6.0, "focus_4t devolve um acumulado plausivel", f)
ok(f is not None and f > 3.5,
   "e ela roda ACIMA da projecao do BC (3,2), por isso so o delta e usavel", f)
# O acumulado e COMPOSTO, na escala do BC. Refeito aqui das quatro medianas cruas: a soma
# (a versao ate 2026-09-24) da ~0,06 a menos e passaria por qualquer faixa de plausibilidade.
_al = pd.Period("2028Q1", "Q")
_rots = "','".join("%d/%d" % ((_al - k).quarter, (_al - k).year) for k in range(4))
_m = ac.q("macro_brasil", f"""
    SELECT mediana FROM expc_focus_periodo
    WHERE indicador='IPCA' AND periodicidade='trimestral' AND base_calculo=0
      AND data_referencia IN ('{_rots}')
      AND date=(SELECT MAX(date) FROM expc_focus_periodo
                WHERE indicador='IPCA' AND periodicidade='trimestral'
                  AND base_calculo=0 AND date <= '2026-08-25')""")["mediana"].astype(float)
_comp = ((1 + _m / 100).prod() - 1) * 100
ok(len(_m) == 4 and f is not None and abs(f - _comp) < 1e-9,
   "focus_4t compoe os quatro trimestres, nao soma",
   (None if f is None else round(f, 4), round(_comp, 4), round(_m.sum(), 4)))
ok(f is not None and f > _m.sum() + 0.01,
   "e o composto fica visivelmente acima da soma -- a assercao que separa as duas",
   (None if f is None else round(f, 4), round(_m.sum(), 4)))
d = ac.delta_focus(pd.Timestamp("2024-12-11"), pd.Timestamp("2024-11-06"),
                   pd.Period("2026Q2", "Q"))
ok(d is not None and d > 0.2,
   "entre a 266a e a 267a a Focus subiu >0,2 p.p. -- a revisao real foi +0,4",
   None if d is None else round(d, 3))

print("\n9. Revisao x expansao de horizonte: os dois casos existem e alternam")
# A pergunta pratica e se o metodo so funciona quando o alvo JA tem numero publicado pelo
# comunicado. Nao: o RPM publica o caminho trimestral CONTIGUO, entao o trimestre que o
# comunicado esta estreando ja tem numero la, e e dali que a ancora vem nas 9 expansoes.
tipos = [ac.tipo_horizonte(pd.Period(r["date"], "Q"), pd.Timestamp(r["vintage"]), proj)
         for _, r in hr.iterrows()]
ok(tipos.count("expansao") + tipos.count("revisao") == len(tipos) and
   abs(tipos.count("expansao") - tipos.count("revisao")) <= 1,
   "so os dois tipos existem, e alternando as contagens diferem de no maximo uma",
   (tipos.count("expansao"), tipos.count("revisao")))
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
# A aba nao roda nada: ela le estes dois arquivos. Se eles sairem de sincronia com o que o
# modulo calcula, o relatorio mostra numero velho sem lancar excecao nenhuma.
B = pd.read_csv(ac._DATA / "antecipa_backtest.csv")
P = json.loads((ac._DATA / "antecipa_previsao.json").read_text(encoding="utf-8"))
ok(len(B) == len(hr), "o csv tem uma linha por reuniao da era declarada", (len(B), len(hr)))
ok({"tipo", "erro_ingenuo", "erro_focus", "ancora", "real"} <= set(B.columns),
   "e as colunas que a aba usa", sorted(B.columns))
# Desde 2026-09-24 o `salvar()` nao roda o modelo agregado: ate entao ele simulava o cenario
# do BC duas vezes por reuniao e o relatorio descartava o resultado. Se as colunas do modelo
# voltarem ao artefato de producao, voltou o custo junto.
ok(not ({"delta_modelo", "erro", "nivel_modelo"} & set(B.columns)) and not P.get("modelo"),
   "o artefato de producao nao carrega o modelo", sorted(B.columns))
ok(((B["ancora"] + B["delta_focus"] - B["real"]) - B["erro_focus"]).abs().max() < 1e-9,
   "erro da Focus = ancora + delta - publicado")
ok(B["erro_focus"].abs().mean() < B["erro_ingenuo"].abs().mean(),
   "e o delta da Focus ganha do ingenuo",
   (round(B["erro_focus"].abs().mean(), 4), round(B["erro_ingenuo"].abs().mean(), 4)))
ok(P["nro"] == int(hr["nro_reuniao"].iloc[-1]) + 1,
   "o json preve a reuniao seguinte a ultima com horizonte declarado", P["nro"])
# `previsto_focus` e nulo enquanto a Focus nao tiver o trimestre-alvo numa das duas datas
# do delta -- estado legitimo, e o de 2026-09-24. Sem esta guarda o teste estourava aqui em
# vez de reprovar regra nenhuma.
ok((P["delta_focus"] is None) == (P["previsto_focus"] is None),
   "sem delta nao ha previsto -- os dois nulos andam juntos",
   (P["delta_focus"], P["previsto_focus"]))
ok(P["previsto_focus"] is None or
   abs(P["previsto_focus"] - (P["ancora"] + P["delta_focus"])) < 1e-9,
   "e o previsto dele fecha com ancora + delta")

print("\n" + (str(falhas) + " FALHA(S)" if falhas else "todos os testes passaram"))
sys.exit(1 if falhas else 0)
