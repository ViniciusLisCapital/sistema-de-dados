"""Expectativas, ciclo 2026-10-02: calibração da distribuição da tese.

(a) Histórico da variável da tese (Focus IPCA 12m, suavizada, base 30 dias, mediana, média do
    trimestre): a variação de um trimestre para o seguinte e a distância entre a média de um
    trimestre e a última leitura do trimestre anterior, em janelas de 1, 2, ... 6 trimestres
    à frente. Desde 2002 e nos últimos 10 anos.
(b) O caminho "sem revisão" que a própria pesquisa implica: composição das medianas
    trimestrais de 2026-09-25 (a última divulgada em 02/10) para a janela de 4 trimestres que
    começa em cada trimestre da tese. Aproximação: a composição de medianas não é a mediana
    da composição, e a variável é média do trimestre, não o início dele.
Lê só ../A/."""
import numpy as np
import pandas as pd
from pathlib import Path

A = Path(__file__).resolve().parent.parent / "A"
fo = pd.read_csv(A / "expc_focus__inflacao.csv.gz", parse_dates=["date"])
v = fo[(fo.indicador == "IPCA") & (fo.horizonte == "12m") & (fo.suavizada == "S") & (fo.base_calculo == 0)]
v = v.set_index("date")["mediana"].sort_index()
v = v[:"2026-09-25"]
q = v.groupby(v.index.to_period("Q")).agg(["mean", "last", "count"])
q = q[q["count"] >= 20]
print("trimestres:", q.index.min(), "a", q.index.max(), len(q))
for nome, sub in (("hist", q), ("10a", q[q.index >= pd.Period("2016Q4")])):
    for k in range(1, 7):
        d = (sub["mean"].shift(-k) - sub["last"]).dropna()   # média de q+k menos a última leitura de q
        a = np.abs(d)
        print(nome, f"k={k}", "n", len(d), "dp", round(d.std(), 2), "p10/p50/p90", np.round(np.percentile(d, [10, 50, 90]), 2),
              "|d|<=0.15:", round((a <= 0.15).mean() * 100), "%", "|d|<=0.30:", round((a <= 0.30).mean() * 100), "%",
              "|d|<=0.50:", round((a <= 0.50).mean() * 100), "%", "queda >=0.45:", round((d <= -0.45).mean() * 100), "%")
# queda da média de q+1 contra a última leitura de q de pelo menos 0,45 p.p.: quando aconteceu
d1 = (q["mean"].shift(-1) - q["last"]).dropna()
print("quedas >= 0,45 (k=1):", d1[d1 <= -0.45].round(2).to_dict())

pe = pd.read_csv(A / "expc_focus_periodo__inflacao.csv.gz", parse_dates=["date"])
t = pe[(pe.periodicidade == "trimestral") & (pe.base_calculo == 0) & (pe.indicador == "IPCA") & (pe.date == "2026-09-25")]
t = t.set_index("data_referencia")["mediana"]
an = pe[(pe.periodicidade == "anual") & (pe.base_calculo == 0) & (pe.indicador == "IPCA") & (pe.date == "2026-09-25")]
an = an.set_index(an.data_referencia.astype(str).str[:4].astype(int))["mediana"]
print("trimestrais 09-25:", t.round(2).to_dict()); print("anuais 09-25:", an.round(2).to_dict())
def comp(vs):
    p = 1.0
    for x in vs: p *= 1 + x / 100
    return round(100 * (p - 1), 2)
ordem = ["4/2026", "1/2027", "2/2027", "3/2027", "4/2027", "1/2028", "2/2028"]
for i, lab in enumerate(["4T26", "1T27", "2T27", "3T27"]):
    print(lab, "janela", ordem[i:i + 4], "composto", comp([t[x] for x in ordem[i:i + 4]]))
print("4T27/1T28: anos 2028", an[2028], "e 2029", an[2029], "(sem trimestrais além de 2T28)")
