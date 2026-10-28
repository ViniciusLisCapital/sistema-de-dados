"""G externo, bloco Risco e dólar: dólar EM, DXY e S&P 500 recentes; dispersão das variações por
horizonte trimestral (para as faixas); co-movimento trimestral dólar EM x S&P; o dólar EM em trimestres
de alta e de corte do Fed; prêmio dos T-bills sobre o Fed Funds efetivo. Lê só ../A/."""
import numpy as np, pandas as pd
from pathlib import Path
A = Path(__file__).resolve().parent.parent / "A"
pd.set_option("display.width", 250)
em = pd.read_csv(A/"cmb_dollar_index_em.csv.gz", parse_dates=["date"]).set_index("date")["value"]
sp = pd.read_csv(A/"cmb_equity_us.csv.gz", parse_dates=["date"]).set_index("date")["value"]
dx = pd.read_csv(A/"cmb_dollar_index.csv.gz", parse_dates=["date"]).set_index("date")["value"]
df = pd.concat([em.rename("dxy_em"), sp.rename("sp500"), dx.rename("dxy")], axis=1)
print("== diário desde 01/set (a cada 3 pregões) e últimos")
x = df.loc["2026-09-01":].ffill()
print(x.iloc[::3].round(2).to_string()); print(x.tail(4).round(2).to_string())
print("\nS&P máx histórico:", sp.max(), sp.idxmax(), " dólar EM máx 2026:", em.loc['2026'].max(), em.loc['2026'].idxmax(), " mín 2026:", em.loc['2026'].min(), em.loc['2026'].idxmin())
qe = df.resample("QE").last()
qe.index = [f"{(d.month-1)//3+1}T{str(d.year)[2:]}" for d in qe.index]
print("\n== fechamentos trimestrais 1T24-")
print(qe.loc["1T24":].round(2).to_string())
for col in ["dxy_em","sp500"]:
    s = qe[col].loc["1T07":"3T26"]
    out=[]
    for h in [1,2,3,4,5,6]:
        ch = 100*np.log(s).diff(h).dropna()
        out.append(f"h={h}: p10 {ch.quantile(.1):.1f} p25 {ch.quantile(.25):.1f} p50 {ch.quantile(.5):.1f} p75 {ch.quantile(.75):.1f} p90 {ch.quantile(.9):.1f}")
    print(col, "Δlog% 2007-2026 |", " | ".join(out))
dq = 100*np.log(qe[["dxy_em","sp500","dxy"]].loc["1T07":"3T26"]).diff().dropna()
print("\ncorr trimestral Δlog dólar EM x S&P, 2007-2026:", round(dq.dxy_em.corr(dq.sp500),2), "; 2016-2026:", round(dq.loc['1T16':].dxy_em.corr(dq.loc['1T16':].sp500),2))
b = np.polyfit(dq.sp500, dq.dxy_em, 1); print("regressão Δlog dólar EM = a + b·Δlog S&P, trimestral 2007-2026: b=", round(b[0],3), " a=", round(b[1],3))
# S&P em quedas de 10%+ no trimestre: dólar EM
big = dq[dq.sp500<=-8]; print("trimestres com S&P <= -8% (2007-2026):", len(big), " Δ dólar EM médio:", round(big.dxy_em.mean(),2), " mín/máx:", round(big.dxy_em.min(),2), round(big.dxy_em.max(),2))
print(big.round(1).to_string())

# Fed: trimestres de alta/corte do efetivo (último mês) e dólar EM no trimestre
dj = pd.read_csv(A/"diferenciais_juros__eua.csv.gz", parse_dates=["date"]).pivot(index="date", columns="name", values="value")
ff = dj["fed_funds"][dj.index.month.isin([3,6,9,12])]
ff.index = [f"{(d.month-1)//3+1}T{str(d.year)[2:]}" for d in ff.index]
z = pd.concat([ff.diff().rename("dff"), dq], axis=1).dropna()
for nome, m in [("alta (Δffr >= +0,20)", z.dff>=0.2), ("corte (Δffr <= -0,20)", z.dff<=-0.2), ("parado", z.dff.abs()<0.2)]:
    print(f"dólar EM em trimestres de {nome}: n={m.sum()}, Δlog médio {z.loc[m,'dxy_em'].mean():+.2f}%, mediana {z.loc[m,'dxy_em'].median():+.2f}%")

# prêmio dos T-bills sobre o efetivo
cur = pd.read_csv(A/"us_interest_rate__curva_completa.csv.gz", parse_dates=["date"])
tre = cur[cur.curve=="US_TREASURY"].pivot(index="date", columns="tenor", values="value").resample("MS").mean()
eff = dj["fed_funds"]
sprd = pd.DataFrame({k: tre[k]-eff for k in ["3M","6M","1Y"]}).dropna()
# meses em que o efetivo não mudou nos 12 meses seguintes (mais de 0,10): o spread aí é ~ só prêmio
fut = eff.shift(-12) - eff
calm = sprd[(fut.reindex(sprd.index).abs()<0.10)]
print("\nT-bill − efetivo em meses com o efetivo parado nos 12 meses seguintes (desde 2001):", calm.loc["2001":].mean().round(2).to_dict(), "n=", len(calm.loc['2001':]))
print("idem desde 2017:", calm.loc["2017":].mean().round(2).to_dict(), "n=", len(calm.loc['2017':]))
print("T-bill − efetivo, últimos 6 meses:"); print(sprd.iloc[-6:].round(2).to_string())
