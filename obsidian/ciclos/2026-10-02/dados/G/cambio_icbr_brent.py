"""G do câmbio, ciclo 2026-10-02: quanto do choque do Brent chega ao IC-Br em dólar.

1) Pesos implícitos dos três subíndices no IC-Br em dólar: regressão, sem constante, da variação
   mensal (log) do índice cheio sobre a dos subíndices, nos últimos 5 anos.
2) Elasticidade do IC-Br energia ao Brent (média mensal), na mesma amostra.
3) O IC-Br em dólar de dezembro se o Brent ficar, em média, no nível de hoje (02/10) ou na média
   de outubro até 02/10, com os outros subíndices parados no de setembro.
Lê só ../A/."""
from pathlib import Path
import numpy as np
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"
ic = pd.read_csv(A / "comm_icbr_usd.csv.gz")
ic = ic.pivot(index="date", columns="name", values="value")
ic.index = pd.to_datetime(ic.index)
print(ic.tail(6).to_string())

br = pd.read_csv(A / "comm_brent.csv.gz")
br = br.set_index(pd.to_datetime(br["date"]))["value"]
brm = br.resample("MS").mean()

d = np.log(ic).diff().dropna()
d = d[d.index >= "2021-09-01"]
X = d[["icbr_agro_usd" if "icbr_agro_usd" in d else [c for c in d.columns if "agro" in c][0],
       "icbr_metal_usd", "icbr_energia_usd"]]
w, *_ = np.linalg.lstsq(X.values, d["icbr_usd"].values, rcond=None)
res = d["icbr_usd"].values - X.values @ w
print("pesos implícitos (agro, metal, energia):", np.round(w, 3), "R²", round(1 - res.var() / d["icbr_usd"].var(), 3))

e = pd.concat([np.log(ic["icbr_energia_usd"]).diff(), np.log(brm).diff()], axis=1, keys=["en", "brent"]).dropna()
e = e[e.index >= "2021-09-01"]
Xe = np.column_stack([np.ones(len(e)), e["brent"]])
be, *_ = np.linalg.lstsq(Xe, e["en"].values, rcond=None)
rr = e["en"].values - Xe @ be
print("elasticidade energia/Brent:", round(be[1], 3), "R²", round(1 - rr.var() / e["en"].var(), 3))

set_b = brm["2026-09-01"]
print("Brent média set", round(set_b, 2), "· média out até 02/10", round(br["2026-10"].mean(), 2), "· 02/10", br.iloc[-1])
icb = ic["icbr_usd"].iloc[-1]
for nome, nivel in [("Brent no nível de 02/10", br.iloc[-1]), ("Brent na média de out até 02/10", br["2026-10"].mean()),
                    ("Brent de volta à média de set", set_b), ("Brent na média de ago", brm["2026-08-01"])]:
    dl = np.log(nivel / set_b)
    di = w[2] * be[1] * dl
    print(f"{nome}: Δlog Brent {100*dl:+.1f}% -> IC-Br em dólar {icb*np.exp(di):.1f} ({100*(np.exp(di)-1):+.1f}%)")
