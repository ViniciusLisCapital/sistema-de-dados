"""G cambio: fluxo cambial contratado (A/cmb_cambio_contratado) — outubro até a última data, por semana;
sazonalidade do saldo financeiro e total em novembro-dezembro (2010-2025); PTAX média de setembro contra a última;
carry ex-ante (DI 1 ano − ponto médio do Fed) em datas-chave; e COT do real nas últimas semanas."""
import numpy as np
import pandas as pd
from pathlib import Path

A = Path(__file__).resolve().parent.parent / "A"
pd.set_option("display.width", 200)
cc = pd.read_csv(A / "cmb_cambio_contratado.csv.gz", parse_dates=["date"])
d = cc[cc.name.isin(["cc_saldo_total", "cc_saldo_comercial", "cc_fin_saldo"])].pivot(index="date", columns="name", values="value") / 1000
out = d[d.index >= "2026-10-01"]
print("Outubro até a última data (US$ bi), acumulado:\n", out.sum().round(2).to_string())
print("Por semana:\n", out.resample("W-FRI").sum().round(2).to_string())
print("Última data:", out.index.max().date())
m = d.resample("MS").sum()
m = m[(m.index >= "2010-01-01") & (m.index < "2026-01-01")]
m["mes"] = m.index.month
g = m.groupby("mes").mean().round(2)
print("\nMédia por mês do ano 2010-2025 (US$ bi):\n", g.to_string())
nd = m[m.mes.isin([11, 12])].groupby(m[m.mes.isin([11, 12])].index.year).sum()[["cc_fin_saldo", "cc_saldo_total"]]
print("\nNov+Dez por ano (US$ bi):\n", nd.round(2).to_string())
print("Nov+Dez média 2010-2025:", nd.mean().round(2).to_dict(), "| média de dois meses quaisquer:", (m[["cc_fin_saldo","cc_saldo_total"]].mean()*2).round(2).to_dict())

pt = pd.read_csv(A / "cmb_ptax.csv.gz", parse_dates=["date"]); pt = pt[pt.name == "ptax_venda"].set_index("date").value
set_med = pt["2026-09-01":"2026-09-30"].mean()
print(f"\nPTAX média de setembro/2026: {set_med:.4f}; última {pt.iloc[-1]:.4f} ({pt.index[-1].date()}): {100*(pt.iloc[-1]/set_med-1):+.2f}%")

di = pd.read_csv(A / "br_di_grade.csv.gz", parse_dates=["date"])
di1 = di[(di.dc >= 345) & (di.dc <= 385)].assign(dist=lambda x: (x.dc-365).abs()).sort_values("dist").groupby("date").first().value
us = pd.read_csv(A / "us_interest_rate.csv.gz", parse_dates=["date"])
pol = us[us.curve == "POLICY"].set_index("date").value
for dt in ["2026-09-30", "2026-10-02", "2026-10-22", "2026-10-26"]:
    a = di1[di1.index <= dt].iloc[-1]; b = pol[pol.index <= dt].iloc[-1]
    print(f"carry ex-ante {dt}: DI 1a {a:.2f} − Fed {b:.3f} = {a-b:.2f} p.p.")

cot = pd.read_csv(A / "cmb_cot_fx.csv.gz", parse_dates=["date"])
c = cot[(cot.currency == "BRL") & cot.name.isin(["lev_net", "asset_mgr_net", "dealer_net", "open_interest"])].pivot(index="date", columns="name", values="value")
print("\nCOT BRL, últimas 10 semanas:\n", c.tail(10).to_string())
tot = c.lev_net + c.asset_mgr_net
print("Fundos alavancados + asset managers, último:", tot.iloc[-1], "pctl hist:", round(100*(tot <= tot.iloc[-1]).mean(), 0),
      "pctl 10a:", round(100*(tot[tot.index >= tot.index[-1]-pd.DateOffset(years=10)] <= tot.iloc[-1]).mean(), 0))
