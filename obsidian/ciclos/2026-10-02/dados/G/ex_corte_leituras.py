"""G do externo, ciclo 2026-10-02: as leituras com o conjunto de informação de 02/10.

O F corta pela data de referência; aqui separo o que já tinha saído em 02/10:
CPI até ago (o de set saiu 14/10), IC-Br até ago (o de set saiu 07/10), inflação
esperada até set (o ponto de 01/10 é publicado depois). PCE ago (30/09), JOLTS ago
(29/09) e payroll set (02/10, 08:30) existiam.
Lê só ../A/.
"""
from pathlib import Path
import numpy as np
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"
pd.set_option("display.width", 200)

def rd(t):
    d = pd.read_csv(A / f"{t}.csv.gz")
    d["date"] = pd.to_datetime(d["date"])
    return d

# --- Fed: meta (ponto médio) diária, datas de mudança no último ano
c = rd("us_interest_rate__curva_completa")
pol = c[(c.curve == "POLICY")].sort_values("date")
print("tenors POLICY:", pol.tenor.unique())
p = pol.set_index("date")["value"]
mud = p[p.diff().abs() > 1e-9]
print("\nMudanças da meta desde 2024-06:")
print(mud[mud.index >= "2024-06-01"])

tr = c[c.curve == "US_TREASURY"].pivot_table(index="date", columns="tenor", values="value")
print("\nTreasuries em datas-chave:")
for d in ["2026-06-30", "2026-08-31", "2026-09-15", "2026-09-30", "2026-10-01", "2026-10-02"]:
    r = tr.loc[:d].iloc[-1]
    print(r.name.date(), r[["1M", "3M", "6M", "1Y", "2Y", "10Y", "30Y"]].to_dict())

# --- Fed funds efetivo mensal
dj = rd("diferenciais_juros__eua")
ff = dj[dj.name == "fed_funds"].set_index("date")["value"]
print("\nFed funds efetivo (média do mês):")
print(ff.tail(14))

# --- CPI: variação mensal (SA) até agosto e até setembro
cpi = rd("inflc_cpi").pivot_table(index="date", columns="item_code", values="value")
cpi = cpi.asfreq("MS")
names = {"SA0": "cheio", "SA0L1E": "nucleo", "SACL1E": "bens_nucl", "SASLE": "serv_s_energia",
         "SAH1": "shelter", "SAF1": "alimentos", "SA0E": "energia"}
m = 100 * np.log(cpi).diff()
print("\nCPI 100·Δlog mensal (SA), últimos 8 meses:")
print(m.rename(columns=names).tail(8).round(2))

def ann(df, end, k):
    a = df.loc[:end].dropna()
    return 100 * ((a.iloc[-1] / a.iloc[-1 - k]) ** (12 / k) - 1)

for end in ["2026-08-01", "2026-09-01"]:
    print(f"\nCPI anualizado até {end[:7]} (3m, 6m) e 12m:")
    cc = cpi.loc[:end].dropna()
    out = pd.DataFrame({
        "3m_anual": 100 * ((cc.iloc[-1] / cc.iloc[-4]) ** 4 - 1),
        "6m_anual": 100 * ((cc.iloc[-1] / cc.iloc[-7]) ** 2 - 1),
        "12m": 100 * (cc.iloc[-1] / cc.iloc[-13] - 1),
    }).rename(index=names)
    print(out.round(2))

# infl_us na convenção: 100·Δlog do último mês do trimestre anterior ao último deste
lv = cpi["SA0"]
print("\ninfl_us por trimestre (convenção):")
for q_end, q_prev in [("2025-12-01", "2025-09-01"), ("2026-03-01", "2025-12-01"),
                      ("2026-06-01", "2026-03-01"), ("2026-09-01", "2026-06-01")]:
    a, b = lv.get(pd.Timestamp(q_prev)), lv.get(pd.Timestamp(q_end))
    print(q_end[:7], round(100 * np.log(b / a), 3) if pd.notna(a) and pd.notna(b) else None)
print("3T26 parcial em 02/10 (jun->ago):", round(100 * np.log(lv["2026-08-01"] / lv["2026-06-01"]), 3))
print("CPI cheio 12m ago:", round(100 * (lv["2026-08-01"] / lv["2025-08-01"] - 1), 2))

# --- PCE
pce = rd("inflc_pce").pivot_table(index="date", columns="code", values="value")
print("\nPCE 100·Δlog mensal:")
print((100 * np.log(pce).diff()).tail(6).round(2))

# --- inflação esperada: set vs out
ei = rd("expc_inflacao").pivot_table(index="date", columns="tenor", values="value")
print("\nInflação esperada (Cleveland):")
print(ei[["1Y", "2Y", "5Y", "10Y", "30Y"]].tail(5).round(2))

# --- trabalho
ces = rd("mt_ces")
emp = ces[(ces.series_id == "CES0000000001")].set_index("date")["valor"]
print("\nPayroll Δ mensal (mil):")
print(emp.diff().tail(8))
print("média 3m:", emp.diff().tail(3).mean(), " média 12m:", emp.diff().tail(12).mean())

# --- IC-Br por grupo, até agosto
ic = rd("comm_icbr_usd").pivot_table(index="date", columns="name", values="value")
print("\nIC-Br US$ (mensal):")
print(ic.tail(8))
print("Média jul-ago:", ic.loc["2026-07-01":"2026-08-01"].mean().round(2).to_dict())

# --- Brent diário
br = rd("comm_brent").set_index("date")["value"]
print("\nBrent últimos 25 pregões:")
print(br.tail(25))
print("Brent média 3T26:", round(br["2026-07-01":"2026-09-30"].mean(), 2),
      " média set:", round(br["2026-09"].mean(), 2), " fim set:", br[:"2026-09-30"].iloc[-1])
print("Brent média por mês 2026:", br["2026"].resample("MS").mean().round(1).to_dict())

# --- dólar EM, DXY, S&P em datas
for t, nm in [("cmb_dollar_index_em", "dxy_em"), ("cmb_dollar_index", "dxy"), ("cmb_equity_us", "sp500")]:
    s = rd(t).set_index("date")["value"]
    print(f"\n{nm}:", {d: round(s[:d].iloc[-1], 2) for d in
                     ["2026-06-30", "2026-08-31", "2026-09-15", "2026-09-30", "2026-10-01", "2026-10-02"]})
    print(f"{nm} máx/mín 2026:", round(s["2026"].max(), 2), s["2026"].idxmax().date(),
          round(s["2026"].min(), 2), s["2026"].idxmin().date())

cds = rd("cmb_risco_pais").set_index("date")["value"]
print("\nCDS:", {d: round(cds[:d].iloc[-1], 1) for d in ["2026-06-30", "2026-08-31", "2026-09-30", "2026-10-02"]})
fx = rd("cmb_fx_latam").pivot_table(index="date", columns="country_code", values="value")
print("\nLatAm:", fx.loc[:"2026-08-31"].iloc[-1].round(3).to_dict(), fx.iloc[-1].round(3).to_dict())
