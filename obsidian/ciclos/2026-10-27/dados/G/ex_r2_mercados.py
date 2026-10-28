"""G externo, rodada 2:
(1) o componente global do CDS com datas casadas (o dólar EM só vai até 23/10; o CDS de 26/10 traz o pregão
    pós-eleição): 30/09 -> 23/10 e o pregão de 26/10 à parte; mesma regressão trimestral 2016-2026 da r1;
(2) o peso efetivo do real no dólar contra emergentes: regressão diária de Δlog dólar EM em Δlog BRL (PTAX),
    MXN, CLP, COP, PEN e DXY, 2016-2026 e 2023-2026; e o salto mecânico que o real de 26/10 dá ao índice;
(3) DXY e S&P de 23/10 a 27/10 e no pregão de 26/10;
(4) a média de dezembro do Fed Funds efetivo com uma alta de 25 p.b. em 28/10 ou em 09/12 (vigente no dia
    seguinte), com o spread efetivo − ponto médio medido desde mai/26.
Lê só ../A/ e o retrato do modelo."""
import numpy as np, pandas as pd
from pathlib import Path
from analytics.agent_system import modelo
A = Path(__file__).resolve().parent.parent / "A"
s = lambda f, col="value": pd.read_csv(A/f, parse_dates=["date"])
em = s("cmb_dollar_index_em.csv.gz").set_index("date")["value"]
dxy = s("cmb_dollar_index.csv.gz").set_index("date")["value"]
sp = s("cmb_equity_us.csv.gz").set_index("date")["value"]
cds = s("cmb_risco_pais.csv.gz").set_index("date")["value"]
pt = s("cmb_ptax.csv.gz"); brl = pt[pt.name == "ptax_venda"].set_index("date")["value"]
lat = s("cmb_fx_latam.csv.gz").pivot(index="date", columns="country_code", values="value")

# (1) CDS, componente global com datas casadas
p = modelo.carregar("2026-10-27")["p"]; idx = pd.to_datetime(p["x"])
obs = {k: pd.Series(p["var"][k]["obs"], index=idx, dtype=float) for k in ["fiscal", "dxy_em", "sp500"]}
c = pd.DataFrame(obs).dropna()
dc = pd.DataFrame({"cds": c.fiscal.diff(), "em": 100*np.log(c.dxy_em).diff(), "sp": 100*np.log(c.sp500).diff()}).dropna().loc["2016-01-01":]
X = np.c_[np.ones(len(dc)), dc[["em", "sp"]].values]; b, *_ = np.linalg.lstsq(X, dc.cds.values, rcond=None)
print(f"(1) ΔCDS = {b[0]:.2f} + {b[1]:.2f}·Δlog dólar EM + {b[2]:.3f}·Δlog S&P (trimestral 2016-2026T3)")
def janela(d0, d1, nome):
    e0, e1 = em.loc[:d0].iloc[-1], em.loc[:d1].iloc[-1]; s0, s1 = sp.loc[:d0].iloc[-1], sp.loc[:d1].iloc[-1]
    c0, c1 = cds.loc[:d0].iloc[-1], cds.loc[:d1].iloc[-1]
    g = b[1]*100*np.log(e1/e0) + b[2]*100*np.log(s1/s0)
    print(f"   {nome}: dólar EM {e0:.2f}->{e1:.2f} ({100*np.log(e1/e0):+.2f}%), S&P {s0:.0f}->{s1:.0f} ({100*np.log(s1/s0):+.2f}%), "
          f"CDS {c0:.1f}->{c1:.1f} ({c1-c0:+.1f} p.b.); global {g:+.1f} p.b.; resto {c1-c0-g:+.1f} p.b.")
janela("2026-09-30", "2026-10-23", "30/09 -> 23/10 (datas casadas)")
janela("2026-09-23", "2026-10-23", "23/09 -> 23/10 (um mês, datas casadas)")
janela("2026-09-30", "2026-10-02", "30/09 -> 02/10")
janela("2026-10-02", "2026-10-05", "02/10 -> 05/10 (1º turno)")
print(f"   CDS 23/10 -> 26/10: {cds.loc['2026-10-23']:.1f} -> {cds.loc['2026-10-26']:.1f} ({cds.loc['2026-10-26']-cds.loc['2026-10-23']:+.1f} p.b.); "
      f"S&P {sp.loc['2026-10-23']:.0f} -> {sp.loc['2026-10-26']:.0f}; dólar EM sem dado em 26/10")
print(f"   CDS mín/máx de 01/10 a 23/10: {cds.loc['2026-10-01':'2026-10-23'].min():.1f} / {cds.loc['2026-10-01':'2026-10-23'].max():.1f}")

# (2) peso efetivo do real no dólar EM
d = pd.DataFrame({"em": em, "brl": brl, "mx": lat.get("MX"), "cl": lat.get("CL").shift(-1), "co": lat.get("CO").shift(-1),
                  "pe": lat.get("PE"), "dxy": dxy}).dropna()
r = 100*np.log(d).diff().dropna()
for ini in ["2016-01-01", "2023-01-01"]:
    x = r.loc[ini:]
    Xr = np.c_[np.ones(len(x)), x[["brl", "mx", "cl", "co", "pe", "dxy"]].values]
    bb, *_ = np.linalg.lstsq(Xr, x.em.values, rcond=None)
    res = x.em.values - Xr@bb; s2 = (res**2).sum()/(len(x)-Xr.shape[1]); se = np.sqrt(np.diag(s2*np.linalg.inv(Xr.T@Xr)))
    r2 = 1 - (res**2).sum()/((x.em-x.em.mean())**2).sum()
    print(f"(2) Δlog dólar EM em BRL, MXN, CLP, COP, PEN, DXY ({ini[:4]}-2026, diário, n={len(x)}): "
          + ", ".join(f"{n} {v:.3f} (t {v/e:.1f})" for n, v, e in zip(["BRL","MXN","CLP","COP","PEN","DXY"], bb[1:], se[1:])) + f"; R² {r2:.2f}")
    if ini == "2023-01-01": w = bb[1]
salto = 100*np.log(brl.loc["2026-10-26"]/brl.loc["2026-10-23"])
print(f"   real 23/10 -> 26/10: {brl.loc['2026-10-23']:.4f} -> {brl.loc['2026-10-26']:.4f} ({salto:+.2f}%); "
      f"efeito mecânico no índice com o peso 2023-2026: {w*salto:+.2f}% = {em.iloc[-1]*w*salto/100:+.2f} ponto")

# (3) DXY e S&P depois de 23/10
for nome, ser in [("DXY", dxy), ("S&P", sp)]:
    a, b26, b27 = ser.loc["2026-10-23"], ser.loc["2026-10-26"], ser.loc["2026-10-27"]
    print(f"(3) {nome}: 23/10 {a:.2f} · 26/10 {b26:.2f} ({100*np.log(b26/a):+.2f}%) · 27/10 {b27:.2f} ({100*np.log(b27/a):+.2f}% desde 23/10)")
print(f"    S&P máximo de 2026: {sp.loc['2026'].max():.0f} em {sp.loc['2026'].idxmax().date()}; 27/10 a {100*(sp.iloc[-1]/sp.loc['2026'].max()-1):+.2f}% dele")

# (4) Fed Funds efetivo em dezembro com a alta em 28/10 ou 09/12
fe = pd.read_csv(A/"diferenciais_juros__eua.csv.gz", parse_dates=["date"])
fe = fe[fe.name == "fed_funds"].set_index("date")["value"]
cur = pd.read_csv(A/"us_interest_rate__curva_completa.csv.gz", parse_dates=["date"])
meta = cur[cur.curve == "POLICY"].set_index("date")["value"].resample("MS").mean()
spr = (fe - meta).dropna().loc["2026-05-01":"2026-08-01"]
print(f"(4) efetivo − ponto médio da meta, média mai-ago/26: {spr.mean():+.3f} p.p. ({spr.round(3).to_dict()})")
e_ant, e_dep = 3.875 + spr.mean(), 4.125 + spr.mean()
for nome, dias_ant in [("alta em 28/10", 0), ("alta em 09/12 (vigente em 10/12)", 9)]:
    print(f"    {nome}: média de dezembro {(dias_ant*e_ant + (31-dias_ant)*e_dep)/31:.3f}")
print(f"    duas altas (28/10 e 09/12): média de dezembro {(9*e_dep + 22*(e_dep+0.25))/31:.3f}; sem alta: {e_ant:.3f}")

# (5) contas de apoio do report: o salto mecânico com o real na central do câmbio (5,35-5,39, cambio_r1),
#     o S&P de 23/10 contra a máxima, o Brent do base no 2T27 contra a premissa do Copom (~84, RPM set/26)
for alvo in (5.35, 5.39):
    print(f"(5) real em {alvo} contra 5,0377 (23/10): efeito no índice {w*100*np.log(alvo/brl.loc['2026-10-23']):+.2f}%")
print(f"    S&P 23/10 contra a máxima de 06/10: {100*(sp.loc['2026-10-23']/sp.loc['2026'].max()-1):+.2f}%")
print(f"    Brent do base no 2T27 (99,3) menos a premissa do Copom (84): {99.3-84:+.1f} US$")
print(f"    agro do base contra o da r1 (202,0): 4T27 {100*(197.8/202-1):+.1f}%, 1T28 {100*(197.4/202-1):+.1f}%; 4T26 -> 1T28 {100*(197.4/203.9-1):+.1f}%")
print(f"    rr_10a: queda do fiscal em 2027 (7,80 -> 7,50) e a parte do Treasury (-0,07): {0.07/0.30:.0%}; PM 8,05 − fiscal 7,50 = {8.05-7.50:.2f}, upside +0,14 = {0.14/0.55:.0%} disso")
