"""Expectativas, ciclo 2026-10-02, rodada 1: a distribuição da tese.

1. O caminho "sem revisão" da própria pesquisa (Focus de 2026-09-25, a última divulgada em 02/10):
   a expectativa de 12 meses para uma janela que começa no trimestre s é
     - s = 4T26 .. 3T27: composição das medianas trimestrais + o hiato entre a suavizada de 12m
       e a composição na janela de 4T26 (método de suavização, suposto constante);
     - s = 4T27: a suavizada de 24 meses (janela que começa 12 meses à frente);
     - s = 1T28: a mediana do ano 2028; s = 2T28: média das medianas de 2028 e 2029.
   A variável da tese é a média das pesquisas do trimestre q, cuja janela começa, no meio do
   trimestre, entre q e q+1: m(q) = média das janelas que começam em q e em q+1.
2. Em torno de m(q): a dispersão histórica da variável, (média de q+k) − (última leitura de q),
   centrada na própria mediana, nos últimos 10 anos (k = 1..6), empírica (sem normal).
3. As probabilidades de cada faixa da tese, a partir dessa distribuição.
Lê só ../A/."""
import numpy as np
import pandas as pd
from pathlib import Path

A = Path(__file__).resolve().parent.parent / "A"
D = pd.Timestamp("2026-09-25")
fo = pd.read_csv(A / "expc_focus__inflacao.csv.gz", parse_dates=["date"])
fo = fo[(fo.indicador == "IPCA") & (fo.suavizada == "S") & (fo.base_calculo == 0)]
s12 = fo[(fo.horizonte == "12m") & (fo.date == D)]["mediana"].iloc[0]
s24 = fo[(fo.horizonte == "24m") & (fo.date == D)]["mediana"].iloc[0]
pe = pd.read_csv(A / "expc_focus_periodo__inflacao.csv.gz", parse_dates=["date"])
pe = pe[(pe.base_calculo == 0) & (pe.indicador == "IPCA") & (pe.date == D)]
t = pe[pe.periodicidade == "trimestral"].set_index("data_referencia")["mediana"]
an = pe[pe.periodicidade == "anual"]
an = an.set_index(an.data_referencia.astype(str).str[:4].astype(int))["mediana"]
def comp(vs):
    p = 1.0
    for x in vs: p *= 1 + x / 100
    return 100 * (p - 1)
ordem = ["4/2026", "1/2027", "2/2027", "3/2027", "4/2027", "1/2028", "2/2028"]
c = {s: comp([t[x] for x in ordem[i:i + 4]]) for i, s in enumerate(["4T26", "1T27", "2T27", "3T27"])}
gap = s12 - c["4T26"]
jan = {s: c[s] + gap for s in c}
jan["4T27"] = s24
jan["1T28"] = an[2028]
jan["2T28"] = (an[2028] + an[2029]) / 2
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
seq = T + ["2T28"]
m = {q: (jan[q] + jan[seq[i + 1]]) / 2 for i, q in enumerate(T)}
print("suavizada 12m", s12, "24m", s24, "| gap suavizada − composição", round(gap, 3))
print("janelas:", {k: round(v, 2) for k, v in jan.items()})
print("m(q), caminho sem revisão:", {k: round(v, 2) for k, v in m.items()})

v = pd.read_csv(A / "expc_focus__inflacao.csv.gz", parse_dates=["date"])
v = v[(v.indicador == "IPCA") & (v.horizonte == "12m") & (v.suavizada == "S") & (v.base_calculo == 0)]
v = v.set_index("date")["mediana"].sort_index()[:D]
q = v.groupby(v.index.to_period("Q")).agg(["mean", "last", "count"])
q = q[(q["count"] >= 20) & (q.index >= pd.Period("2016Q4"))]

# faixas da tese (lo, hi) e centrais do modelo, por trimestre
modelo = {"4T26": 4.16, "1T27": 3.97, "2T27": 3.78, "3T27": 3.67, "4T27": 3.59, "1T28": 3.52}
faixas = {"4T26": (4.10, 4.45), "1T27": (3.90, 4.25), "2T27": (3.70, 4.05),
          "3T27": (3.60, 4.00), "4T27": (3.50, 3.90), "1T28": (3.45, 3.85)}
print("\nq | m | central modelo | faixa | P(faixa) P(acima) P(abaixo) | pctl do modelo na distribuição | p10 p50 p90")
for k, lab in enumerate(T, start=1):
    d = (q["mean"].shift(-k) - q["last"]).dropna()
    d = d - d.median()
    x = m[lab] + d.values
    lo, hi = faixas[lab]
    pin = ((x >= lo) & (x <= hi)).mean() * 100
    pup = (x > hi).mean() * 100
    pdn = (x < lo).mean() * 100
    pm = (x < modelo[lab]).mean() * 100
    print(lab, round(m[lab], 2), modelo[lab], faixas[lab], round(pin), round(pup), round(pdn), "| pctl", round(pm),
          "|", np.round(np.percentile(x, [10, 50, 90]), 2), "n", len(x))
