"""G externo, bloco Política dos EUA: CPI e PCE mês a mês, infl_us trimestral na convenção do modelo,
Fed Funds efetivo contra a meta, mudanças da meta, curva diária recente, payroll e juro real ex-ante.
Lê só ../A/."""
import numpy as np, pandas as pd
from pathlib import Path
A = Path(__file__).resolve().parent.parent / "A"
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)

cpi = pd.read_csv(A/"inflc_cpi.csv.gz", parse_dates=["date"]).pivot(index="date", columns="item_code", values="value")
cpi = cpi.rename(columns={"SA0":"cheio","SA0L1E":"nucleo","SACL1E":"bens_core","SASLE":"serv_sem_energia","SAH1":"shelter","SAF1":"alimentos","SA0E":"energia"})
# variação mensal (%); o mês ausente (out/2025) fica NaN, nov/2025 contra set/2025 é bimestral
mm = 100*np.log(cpi).diff()
mm.loc[mm.index.isin([pd.Timestamp("2025-11-01")])] = np.nan  # não é mensal
print("== CPI, variação mensal % (100·Δlog), últimos 14 meses (nov/25 omitido: atravessa out/25 ausente)")
print(mm.loc["2025-08-01":].round(2).to_string())
print("\n== CPI 2 meses set/25->nov/25 (100·Δlog):")
print((100*np.log(cpi.loc["2025-11-01"]/cpi.loc["2025-09-01"])).round(2).to_string())

# infl_us na convenção: 100·Δlog do último mês do tri anterior ao último mês deste
q = cpi["cheio"][cpi.index.month.isin([3,6,9,12])]
iq = 100*np.log(q).diff()
iq.index = [f"{(d.month-1)//3+1}T{str(d.year)[2:]}" for d in iq.index]
print("\n== infl_us por trimestre (convenção do modelo), 2T23 em diante")
print(iq.loc["2T23":].round(2).to_string())
qq = 100*np.log(cpi.loc[cpi.index.month.isin([3,6,9,12])]).diff()
for c in ["nucleo","energia","alimentos","shelter","serv_sem_energia","bens_core"]:
    s = qq[c].copy(); s.index = iq.index
    print(c, "3T26:", round(s.iloc[-1],2), " 2T26:", round(s.iloc[-2],2), " 1T26:", round(s.iloc[-3],2))
h = iq.loc["1T15":"4T19"]
print("\ninfl_us média 2015-2019:", round(h.mean(),2), " dp:", round(h.std(),2))
h2 = iq.loc["1T23":]
print("infl_us média 1T23-3T26:", round(h2.mean(),2), " dp:", round(h2.std(),2))
# relação energia -> cheio: regressão trimestral do cheio no núcleo e energia, 2010-2026
X = pd.DataFrame({"nucleo":qq["nucleo"],"energia":qq["energia"],"alim":qq["alimentos"]}).loc["2010":]
y = qq["cheio"].loc["2010":]
Z = pd.concat([X,y],axis=1).dropna()
b = np.linalg.lstsq(np.c_[np.ones(len(Z)),Z[["nucleo","energia","alim"]]], Z["cheio"], rcond=None)[0]
print("cheio_tri = a + b·núcleo + c·energia + d·alim (trimestral, 2010-2026):", np.round(b,3))

pce = pd.read_csv(A/"inflc_pce.csv.gz", parse_dates=["date"]).pivot(index="date", columns="code", values="value")
print("\n== PCE, variação mensal %, últimos 12 meses")
print((100*np.log(pce).diff()).loc["2025-09-01":].round(2).to_string())

dj = pd.read_csv(A/"diferenciais_juros__eua.csv.gz", parse_dates=["date"]).pivot(index="date", columns="name", values="value")
cur = pd.read_csv(A/"us_interest_rate__curva_completa.csv.gz", parse_dates=["date"])
pol = cur[cur.curve=="POLICY"].set_index("date")["value"]
ch = pol[pol.diff()!=0].loc["2023-01-01":]
print("\n== Mudanças da meta (ponto médio) desde 2023")
print(ch.to_string())
pm = pol.resample("MS").mean()
comp = pd.DataFrame({"efetivo":dj["fed_funds"], "meta_media_mes":pm}).loc["2024-01-01":]
comp["efetivo_menos_meta"] = comp.efetivo - comp.meta_media_mes
print("\n== Efetivo (média do mês) contra a meta (média do mês)")
print(comp.round(3).to_string())
sp = (dj["fed_funds"] - pm).dropna()
s2 = sp.loc["2023-01-01":]
print("spread efetivo-meta 2023+: média", round(s2.mean(),3), "mín", round(s2.min(),3), "máx", round(s2.max(),3))

tre = cur[cur.curve=="US_TREASURY"].pivot(index="date", columns="tenor", values="value")
print("\n== Treasuries, pregões selecionados desde jul/2026")
sel = tre.loc["2026-07-01":, ["3M","6M","1Y","2Y","5Y","10Y","30Y"]]
print(sel.iloc[::5].to_string()); print(sel.tail(5).to_string())
print("\n10Y: máx desde 2007:", tre["10Y"].loc["2007-01-01":].max(), tre["10Y"].loc["2007-01-01":].idxmax())
print("2Y máx 2026:", tre["2Y"].loc["2026"].max(), tre["2Y"].loc["2026"].idxmax())

ei = pd.read_csv(A/"expc_inflacao.csv.gz", parse_dates=["date"]).pivot(index="date", columns="tenor", values="value")
tm = tre.resample("MS").mean()
rr = pd.DataFrame({"10Y_nom":tm["10Y"], "10Y_infl_esp":ei["10Y"], "2Y_nom":tm["2Y"], "2Y_infl_esp":ei["2Y"]}).loc["2025-06-01":]
rr["10Y_real"] = rr["10Y_nom"]-rr["10Y_infl_esp"]; rr["2Y_real"] = rr["2Y_nom"]-rr["2Y_infl_esp"]
print("\n== Juro real ex-ante (Treasury média do mês − inflação esperada Cleveland Fed)")
print(rr.round(2).to_string())
r10 = (tm["10Y"]-ei["10Y"]).dropna()
print("10Y real ex-ante: pctl desde 2007 do último:", round((r10.loc['2007':]<=r10.iloc[-1]).mean()*100), " máx desde 2007:", round(r10.loc['2007':].max(),2), r10.loc['2007':].idxmax())

ces = pd.read_csv(A/"mt_ces.csv.gz", parse_dates=["date"])
pay = ces[(ces.categoria==0)&(ces.medida=="emprego")].set_index("date")["valor"]
print("\n== Payroll, criação mensal (mil)")
print(pay.diff().loc["2025-06-01":].to_string())
print("média 3m:", round(pay.diff().iloc[-3:].mean()), " média 6m:", round(pay.diff().iloc[-6:].mean()), " média 12m:", round(pay.diff().iloc[-12:].mean()))
