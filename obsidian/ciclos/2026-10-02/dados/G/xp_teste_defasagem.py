"""Expectativas, ciclo 2026-10-02: teste da defasagem da (E). Média do trimestre anterior (como no
modelo) contra a ÚLTIMA leitura do trimestre anterior, na forma restrita da (E):
  E(q) − Meta(q) = e1·(Elag − Meta(q)) + e2·(I12(q) − Meta(q)),   MQO sem constante,
com I12 = IPCA 12m do último mês do trimestre (inflc_agregados) e Meta pesada como a Focus 12m
(2/12, 5/12, 8/12, 11/12 do ano seguinte, por trimestre). Amostra 2004T1–2026T2 (a de 3T26 fica de
fora: o IPCA de setembro saiu em 09/10). Não é a estimação bayesiana do modelo: é o teste proposto."""
import numpy as np
import pandas as pd
from pathlib import Path

A = Path(__file__).resolve().parent.parent / "A"
v = pd.read_csv(A / "expc_focus__inflacao.csv.gz", parse_dates=["date"])
v = v[(v.indicador == "IPCA") & (v.horizonte == "12m") & (v.suavizada == "S") & (v.base_calculo == 0)].set_index("date")["mediana"].sort_index()
q = v.groupby(v.index.to_period("Q")).agg(["mean", "last"])
ia = pd.read_csv(A / "inflc_agregados.csv.gz", parse_dates=["date"])
i12 = ia[ia.name == "ipca_12m"].set_index("date")["value"].sort_index()
i12 = i12.groupby(i12.index.to_period("Q")).last()
mt = pd.read_csv(A / "inflc_meta.csv.gz", parse_dates=["date"])
mt = dict(zip(mt.date.dt.year, mt.value)); ul = max(mt)
def meta12(p):
    w = {1: 2, 2: 5, 3: 8, 4: 11}[p.quarter] / 12
    return (1 - w) * mt.get(p.year, mt[ul]) + w * mt.get(p.year + 1, mt[ul])
df = pd.DataFrame({"E": q["mean"], "lag_media": q["mean"].shift(1), "lag_ultima": q["last"].shift(1), "I12": i12}).dropna()
df = df[(df.index >= pd.Period("2004Q1")) & (df.index <= pd.Period("2026Q2"))]
df["M"] = [meta12(p) for p in df.index]
y = df.E - df.M
for lag in ("lag_media", "lag_ultima"):
    X = np.column_stack([df[lag] - df.M, df.I12 - df.M])
    b, *_ = np.linalg.lstsq(X, y.values, rcond=None)
    r = y.values - X @ b
    rmse = np.sqrt((r ** 2).mean())
    rec = r[df.index >= pd.Period("2016Q1")]
    print(lag, "e1", round(b[0], 3), "e2", round(b[1], 3), "peso meta", round(1 - b.sum(), 3),
          "RMSE", round(rmse, 3), "RMSE desde 2016", round(np.sqrt((rec ** 2).mean()), 3), "n", len(df))
