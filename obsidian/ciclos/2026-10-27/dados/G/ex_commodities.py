"""G externo, bloco Commodities: combinação do IC-Br total pelos grupos (regressão mensal em Δlog),
Brent diário recente e média do mês, ligação Brent -> IC-Br energia e Brent -> CPI energia dos EUA,
dispersão histórica das variações trimestrais (para as faixas), correlação com o dólar EM.
Lê só ../A/."""
import numpy as np, pandas as pd
from pathlib import Path
A = Path(__file__).resolve().parent.parent / "A"
pd.set_option("display.width", 250)

ic = pd.read_csv(A/"comm_icbr_usd.csv.gz", parse_dates=["date"]).pivot(index="date", columns="name", values="value")
ic.columns = [c.replace("icbr_","").replace("_usd","") for c in ic.columns]
ic = ic.rename(columns={"icbr":"total"}) if "icbr" in ic.columns else ic
print(ic.columns.tolist())
tot = "usd" if "usd" in ic.columns else "total"
ic = ic.rename(columns={tot:"total"})
dl = 100*np.log(ic).diff().dropna()

def ols(y, X):
    Xc = np.c_[np.ones(len(X)), X]
    b, *_ = np.linalg.lstsq(Xc, y, rcond=None)
    r = y - Xc@b
    r2 = 1 - (r**2).sum()/((y-y.mean())**2).sum()
    return b, r2
for ini in ["2010-01-01", "2018-01-01", "2022-01-01"]:
    d = dl.loc[ini:]
    b, r2 = ols(d["total"].values, d[["agropecuaria","metal","energia"]].values)
    print(f"Δlog total = a + b_agr + b_met + b_ene, mensal {ini[:4]}-2026/09: a={b[0]:.3f} agr={b[1]:.3f} met={b[2]:.3f} ene={b[3]:.3f} R2={r2:.3f} n={len(d)}")

br = pd.read_csv(A/"comm_brent.csv.gz", parse_dates=["date"]).set_index("date")["value"]
print("\n== Brent diário desde 15/set")
print(br.loc["2026-09-15":].round(2).to_string())
bm = br.resample("MS").mean()
print("\nBrent média de out/2026 até 20/10:", round(bm.iloc[-1],2), " máx 2026:", br.loc['2026'].max(), br.loc['2026'].idxmax())
print("Brent médias mensais 2026:", bm.loc['2026'].round(1).to_dict())
# Brent -> IC-Br energia, mensal em Δlog
d = pd.concat([dl["energia"], 100*np.log(bm).diff().rename("brent")], axis=1).dropna().loc["2010":]
b, r2 = ols(d["energia"].values, d[["brent"]].values)
print(f"\nΔlog IC-Br energia = a + b·Δlog Brent (média mensal), 2010-2026: a={b[0]:.3f} b={b[1]:.3f} R2={r2:.3f}")
# nível: razão energia / Brent recente
rat = (ic["energia"]/bm).dropna()
print("razão IC-Br energia / Brent médio, últimos 8 meses:", rat.iloc[-8:].round(3).to_dict())

# Brent -> CPI energia dos EUA (mensal Δlog), 2010-2026, sem o mês que atravessa out/25
cpi = pd.read_csv(A/"inflc_cpi.csv.gz", parse_dates=["date"]).pivot(index="date", columns="item_code", values="value")
e = 100*np.log(cpi["SA0E"]).diff()
e.loc["2025-11-01"] = np.nan
d2 = pd.concat([e.rename("cpi_ene"), 100*np.log(bm).diff().rename("brent"), 100*np.log(bm).diff().shift(1).rename("brent_l1")], axis=1).dropna().loc["2010":]
b, r2 = ols(d2["cpi_ene"].values, d2[["brent","brent_l1"]].values)
print(f"Δlog CPI energia = a + b0·ΔBrent + b1·ΔBrent(-1), mensal 2010-2026: a={b[0]:.3f} b0={b[1]:.3f} b1={b[2]:.3f} R2={r2:.3f}")

# convenção do modelo: grupos = média do tri; total = último mês
q = ic.resample("QS").mean(); qlast = ic.resample("QS").last()
q.index = [f"{(x.month-1)//3+1}T{str(x.year)[2:]}" for x in q.index]; qlast.index = q.index
print("\n== Médias trimestrais dos grupos e último mês do total")
print(pd.concat([q[["agropecuaria","metal","energia"]].add_suffix("_media"), qlast[["total"]].add_suffix("_ultimo")], axis=1).loc["1T24":].round(1).to_string())
# dispersão das variações trimestrais (log %) das médias e do total-último-mês, 2010-2026, por horizonte h
for col, s in [("agr_media", q["agropecuaria"]), ("met_media", q["metal"]), ("total_ultimo", qlast["total"])]:
    s = s.loc["1T10":]
    out = []
    for h in [1,2,3,4,5,6]:
        ch = 100*np.log(s).diff(h).dropna()
        out.append(f"h={h}: p10 {ch.quantile(.1):.1f} p25 {ch.quantile(.25):.1f} p75 {ch.quantile(.75):.1f} p90 {ch.quantile(.9):.1f}")
    print(col, " | ".join(out))

# correlação das variações mensais do IC-Br total e grupos com o dólar EM (fim do mês)
em = pd.read_csv(A/"cmb_dollar_index_em.csv.gz", parse_dates=["date"]).set_index("date")["value"]
emm = em.resample("MS").mean()
dd = pd.concat([dl, 100*np.log(emm).diff().rename("dxy_em")], axis=1).dropna()
for ini, fim in [("2010-01-01","2026-09-01"), ("2021-10-01","2026-09-01"), ("2024-10-01","2026-09-01")]:
    x = dd.loc[ini:fim]
    print(f"corr mensal com Δlog dólar EM (média do mês) {ini[:7]}–{fim[:7]}: " + ", ".join(f"{c} {x[c].corr(x['dxy_em']):+.2f}" for c in ["total","agropecuaria","metal","energia"]) + f" n={len(x)}")
# metais em 12 meses: de onde veio
print("\nMetal: média 3T25", round(ic['metal'].loc['2025-07-01':'2025-09-01'].mean(),1), " pico", ic['metal'].max(), ic['metal'].idxmax())
print("Agro: máx histórico", ic['agropecuaria'].max(), ic['agropecuaria'].idxmax())
