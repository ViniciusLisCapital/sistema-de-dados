"""Trajetoria diaria recente da PTAX e dos precos que a explicam (G do ciclo 2026-10-07).
Le so ../A/. Imprime: painel diario das ultimas ~60 sessoes; PTAX nos fechamentos de mes/trimestre;
variacoes da PTAX desde cada fechamento; max/min recentes."""
from pathlib import Path
import numpy as np
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"
rd = lambda t: pd.read_csv(A / f"{t}.csv.gz", parse_dates=["date"])

ptax = rd("cmb_ptax").query("name=='ptax_venda'").set_index("date")["value"].rename("ptax")
dxy = rd("cmb_dollar_index").set_index("date")["value"].rename("dxy")
em = rd("cmb_dollar_index_em").set_index("date")["value"].rename("dxy_em")
spx = rd("cmb_equity_us").set_index("date")["value"].rename("spx")
brent = rd("comm_brent").set_index("date")["value"].rename("brent")
us = rd("us_interest_rate")
ust2 = us.query("curve=='US_TREASURY' and tenor=='2Y'").set_index("date")["value"].rename("ust2")
ust10 = us.query("curve=='US_TREASURY' and tenor=='10Y'").set_index("date")["value"].rename("ust10")
cds = rd("cmb_risco_pais").set_index("date")["value"].rename("cds")

di = rd("br_di_grade")
di = di[di["date"] >= "2026-05-01"]
def di_at(du_target):
    out = {}
    for d, g in di.groupby("date"):
        g = g.sort_values("du")
        out[d] = np.interp(du_target, g["du"], g["value"])
    return pd.Series(out, name=f"di_{du_target}")
di1, di2, di5 = di_at(252), di_at(504), di_at(1260)

fx = rd("cmb_fx_latam").pivot(index="date", columns="country_code", values="value")

panel = pd.concat([ptax, dxy, em, spx, brent, ust2, ust10, cds, di1, di2, di5, fx], axis=1)
panel = panel[panel.index >= "2026-06-20"]
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 200)
print(panel.round(4).to_string())

print("\nPTAX em fechamentos (ultimo dado <= data):")
for d in ["2025-09-30", "2025-12-31", "2026-03-31", "2026-06-30", "2026-07-31", "2026-08-31", "2026-09-30", "2026-10-06"]:
    s = ptax[ptax.index <= d]
    print(d, s.index[-1].date(), s.iloc[-1])
last = ptax.iloc[-1]
print("\nVariacao da PTAX de 06/10/2026 contra:")
for d in ["2025-12-31", "2026-06-30", "2026-08-31", "2026-09-30"]:
    s = ptax[ptax.index <= d].iloc[-1]
    print(d, round(100 * (last / s - 1), 2), "%")
r = ptax[ptax.index >= "2026-07-01"]
print("\nMax/min desde 01/07/2026:", r.idxmax().date(), r.max(), "|", r.idxmin().date(), r.min())
r = ptax[ptax.index >= "2026-09-01"]
print("Max/min desde 01/09/2026:", r.idxmax().date(), r.max(), "|", r.idxmin().date(), r.min())
print("Min desde 2020:", ptax[ptax.index >= "2020-01-01"].idxmin().date(), ptax[ptax.index >= "2020-01-01"].min())
print("Ultima vez abaixo de 4,97:", ptax[(ptax < 4.9698) & (ptax.index < "2026-09-01")].index.max())
lr = np.log(ptax).diff().dropna()
print("\nMaiores variacoes diarias desde 01/09/2026 (%):")
print((100 * lr[lr.index >= "2026-09-01"]).round(2).sort_values().to_string())
