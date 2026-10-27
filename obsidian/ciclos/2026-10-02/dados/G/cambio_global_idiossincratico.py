"""G do câmbio, ciclo 2026-10-02: a divisão do movimento recente do real em global e
idiossincrático (Q3), e a volatilidade realizada do real em datas de referência.

Divisão: regressão dos retornos diários (log) do BRL sobre o DXY e a média simples dos quatro
pares (MXN, CLP, COP, PEN), estimada nos 12 meses que terminam no início de cada janela; a
parte global é o ajustado acumulado na janela, a idiossincrática é o resto. CLP e COP com a
taxa do dia útil seguinte (a formada no dia, Atenção do F). Lê só ../A/."""
from pathlib import Path
import numpy as np
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"


def serie(tab, col, val):
    d = pd.read_csv(A / f"{tab}.csv.gz")
    d = d[d[col] == val]
    return d.set_index(pd.to_datetime(d["date"]))["value"].astype(float).sort_index()


brl = serie("cmb_ptax", "name", "ptax_venda")
mx = serie("cmb_fx_latam", "country_code", "MX")
cl = serie("cmb_fx_latam", "country_code", "CL").shift(-1)
co = serie("cmb_fx_latam", "country_code", "CO").shift(-1)
pe = serie("cmb_fx_latam", "country_code", "PE")
dxy = serie("cmb_dollar_index", "name", "dxy")

df = pd.concat({"brl": brl, "mx": mx, "cl": cl, "co": co, "pe": pe, "dxy": dxy}, axis=1).dropna()
r = np.log(df).diff().dropna()
r["pares"] = r[["mx", "cl", "co", "pe"]].mean(axis=1)

for ini in ["2026-06-30", "2026-08-31"]:
    est = r[(r.index > pd.Timestamp(ini) - pd.DateOffset(years=1)) & (r.index <= ini)]
    X = np.column_stack([np.ones(len(est)), est["dxy"], est["pares"]])
    b, *_ = np.linalg.lstsq(X, est["brl"].values, rcond=None)
    res = est["brl"].values - X @ b
    r2 = 1 - res.var() / est["brl"].var()
    jan = r[r.index > ini]
    fit = b[1] * jan["dxy"] + b[2] * jan["pares"]  # sem a constante: é o que veio de fora
    tot = jan["brl"].sum()
    print(f"Janela {ini} -> {jan.index[-1].date()} ({len(jan)} pregões)")
    print(f"  betas (12m até {ini}): DXY {b[1]:.2f}, pares {b[2]:.2f}, R² {r2:.2f}")
    print(f"  BRL {100*tot:+.2f}% (log) · global {100*fit.sum():+.2f} · idiossincrático {100*(tot-fit.sum()):+.2f}")
    print(f"  DXY {100*jan['dxy'].sum():+.2f} · pares {100*jan['pares'].sum():+.2f}")

# volatilidade realizada do BRL (63 e 21 pregões, anualizada com 252), em datas de referência
rb = np.log(brl).diff().dropna()
for d in ["2026-03-31", "2026-06-30", "2026-09-30", "2026-10-02"]:
    x = rb[:d]
    print(f"vol realizada BRL em {d}: 63d {100*x.iloc[-63:].std()*np.sqrt(252):.1f} · 21d {100*x.iloc[-21:].std()*np.sqrt(252):.1f}")
# percentil da vol 63d de hoje nos últimos 10 anos
v63 = rb.rolling(63).std() * np.sqrt(252) * 100
v10 = v63["2016-10-02":]
print(f"vol 63d hoje {v10.iloc[-1]:.1f}; mediana 10a {v10.median():.1f}; pctl {100*(v10 < v10.iloc[-1]).mean():.0f}")
