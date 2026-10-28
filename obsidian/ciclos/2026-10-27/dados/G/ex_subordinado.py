"""G externo, como subordinado de rr_10a e fiscal (principal: fiscal):
(1) quanto do juro real de 10 anos local (rr_10a, NTN-B, média do trimestre, do retrato do modelo) anda com o
    juro real ex-ante de 10 anos dos EUA (Treasury 10a − inflação esperada 10a do Cleveland Fed, média do tri);
(2) quanto da variação trimestral do CDS (fiscal, fechamento, do retrato do modelo) é comum ao dólar EM e ao S&P
    (fechamentos). Lê só ../A/ e o retrato do modelo."""
import numpy as np, pandas as pd
from pathlib import Path
from analytics.agent_system import modelo
A = Path(__file__).resolve().parent.parent / "A"
p = modelo.carregar("2026-10-27")["p"]
idx = pd.to_datetime(p["x"])
obs = {k: pd.Series(p["var"][k]["obs"], index=idx, dtype=float) for k in ["rr_10a","fiscal","dxy_em","sp500"]}
cur = pd.read_csv(A/"us_interest_rate__curva_completa.csv.gz", parse_dates=["date"])
t10 = cur[(cur.curve=="US_TREASURY")&(cur.tenor=="10Y")].set_index("date")["value"]
ei = pd.read_csv(A/"expc_inflacao.csv.gz", parse_dates=["date"])
e10 = ei[ei.tenor=="10Y"].set_index("date")["value"]
us_real = (t10.resample("MS").mean() - e10).dropna().resample("QS").mean()
us_nom = t10.resample("QS").mean()
d = pd.DataFrame({"rr_10a":obs["rr_10a"], "us_real10":us_real, "us_nom10":us_nom}).dropna()
print("níveis, últimos 6 trimestres:"); print(d.iloc[-6:].round(2).to_string())
dd = d.diff().dropna()
def reg(y, X, nome):
    Xc = np.c_[np.ones(len(X)), X]; b, *_ = np.linalg.lstsq(Xc, y, rcond=None)
    r = y - Xc@b; s2 = (r**2).sum()/(len(y)-Xc.shape[1]); se = np.sqrt(np.diag(s2*np.linalg.inv(Xc.T@Xc)))
    r2 = 1-(r**2).sum()/((y-y.mean())**2).sum()
    print(f"{nome}: b={np.round(b[1:],3)} t={np.round(b[1:]/se[1:],2)} R2={r2:.2f} n={len(y)}")
    return b
for ini in ["2006-01-01","2016-01-01"]:
    x = dd.loc[ini:]
    reg(x.rr_10a.values, x[["us_real10"]].values, f"Δrr_10a = a + b·Δ juro real 10a EUA, trimestral {ini[:4]}-2026T3")
    reg(x.rr_10a.values, x[["us_nom10"]].values, f"Δrr_10a = a + b·Δ Treasury 10a, trimestral {ini[:4]}-2026T3")
print("Δ juro real 10a EUA, 2T26->3T26:", round(dd.us_real10.iloc[-1],2), " Δrr_10a:", round(dd.rr_10a.iloc[-1],2))
print("juro real 10a EUA out/26 (média do mês) =", round((t10.resample('MS').mean()-e10).dropna().iloc[-1],2), " média 3T26 =", round(us_real.iloc[-1],2))
# CDS
c = pd.DataFrame({"cds":obs["fiscal"], "dxy_em":obs["dxy_em"], "sp500":obs["sp500"]}).dropna()
dc = pd.DataFrame({"cds":c.cds.diff(), "dxy_em":100*np.log(c.dxy_em).diff(), "sp500":100*np.log(c.sp500).diff()}).dropna()
for ini in ["2006-01-01","2016-01-01"]:
    x = dc.loc[ini:]
    b = reg(x.cds.values, x[["dxy_em","sp500"]].values, f"ΔCDS (p.b.) = a + b1·Δlog dólar EM + b2·Δlog S&P, trimestral {ini[:4]}-2026T3")
print("CDS fechamentos últimos 6 tri:", c.cds.iloc[-6:].round(1).to_dict())
# o que os cenários de risco implicam para o CDS pela regressão 2016-2026
x = dc.loc["2016-01-01":]; Xc = np.c_[np.ones(len(x)), x[["dxy_em","sp500"]].values]; b, *_ = np.linalg.lstsq(Xc, x.cds.values, rcond=None)
for nome, dem, dsp in [("risk-off 4T26+1T27 (dólar EM 129,4->136,5; S&P 7652->6500)", 100*np.log(136.5/129.38), 100*np.log(6500/7651.54)),
                       ("base 4T26 (dólar EM 129,4->130,5; S&P 7652->7750)", 100*np.log(130.5/129.38), 100*np.log(7750/7651.54)),
                       ("risk-on até 1T27 (dólar EM 129,4->127; S&P 7652->8300)", 100*np.log(127/129.38), 100*np.log(8300/7651.54))]:
    print(f"componente global do CDS, {nome}: {b[1]*dem + b[2]*dsp:+.1f} p.b. (sem a constante)")
# o que a regressão 2016-2026 diz dos movimentos recentes (dólar EM e S&P do F externo; CDS observado no F)
em = pd.read_csv(A/"cmb_dollar_index_em.csv.gz", parse_dates=["date"]).set_index("date")["value"]
sp = pd.read_csv(A/"cmb_equity_us.csv.gz", parse_dates=["date"]).set_index("date")["value"]
cds = pd.read_csv(A/"cmb_risco_pais.csv.gz", parse_dates=["date"]).set_index("date")["value"]
for nome, d0, d1 in [("3T26 (30/09) -> último", "2026-09-30", None), ("1 mês (26/09 -> 26/10 no CDS; 23/09 -> 23/10 no dólar EM)", "2026-09-25", None)]:
    e0 = em.loc[:d0].iloc[-1]; e1 = em.iloc[-1]; s0 = sp.loc[:d0].iloc[-1]; s1 = sp.loc[:"2026-10-23"].iloc[-1]
    c0 = cds.loc[:d0].iloc[-1]; c1 = cds.iloc[-1]
    prev = b[1]*100*np.log(e1/e0) + b[2]*100*np.log(s1/s0)
    print(f"{nome}: dólar EM {e0:.2f}->{e1:.2f}, S&P {s0:.0f}->{s1:.0f}, CDS {c0:.0f}->{c1:.0f} ({c1-c0:+.0f} p.b.); componente global previsto {prev:+.1f} p.b.")
# efeito em rr_10a de um deslocamento do Treasury 10a nos cenários (coeficiente 2006-2026, Δ Treasury 10a)
x = dd.loc["2006-01-01":]; Xc = np.c_[np.ones(len(x)), x[["us_nom10"]].values]; bt, *_ = np.linalg.lstsq(Xc, x.rr_10a.values, rcond=None)
for nome, dlt in [("upside, Treasury 10a +0,50 p.p.", 0.5), ("downside, Treasury 10a −0,60 p.p.", -0.6), ("base, Treasury 10a −0,25 p.p. até 1T28", -0.25)]:
    print(f"rr_10a, {nome}: {bt[1]*dlt:+.2f} p.p.")
