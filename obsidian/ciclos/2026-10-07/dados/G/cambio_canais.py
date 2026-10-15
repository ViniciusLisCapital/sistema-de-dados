"""Contas dos canais da tese (G do ciclo 2026-10-07). Le so ../A/.
(1) sessao de 05/10/2026: variacao do DI e dos Treasuries; variacoes desde 04/09;
(2) carry hoje e o caminho do diferencial com a Selic precificada na curva no fim de cada trimestre
    (Fed Funds parado em 3,875, premissa); carry / vol 63d com o Fed de hoje;
(3) diferencial de inflacao corrente e esperado;
(4) sazonalidade de dezembro: fluxo cambial e variacao da PTAX, 2016-2025;
(5) caminho central da tese contra spot, forward e Focus."""
from pathlib import Path
import numpy as np
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"
rd = lambda t: pd.read_csv(A / f"{t}.csv.gz", parse_dates=["date"])

di = rd("br_di_grade"); di = di[di["date"] >= "2026-08-25"]
def di_at(d, du):
    g = di[di["date"] == d].sort_values("du"); return np.interp(du, g["du"], g["value"])
print("(1) DI (p.b.)")
for du, nm in [(252, "1a"), (504, "2a"), (1260, "5a"), (2520, "10a")]:
    print(f"  DI {nm}: 02/10 {di_at('2026-10-02', du):.2f} -> 05/10 {di_at('2026-10-05', du):.2f} = {100*(di_at('2026-10-05', du)-di_at('2026-10-02', du)):+.0f} p.b.;"
          f" 04/09 -> 02/10 {100*(di_at('2026-10-02', du)-di_at('2026-09-04', du)):+.0f} p.b.")
us = rd("us_interest_rate")
for t in ["2Y", "10Y"]:
    s = us.query(f"curve=='US_TREASURY' and tenor=='{t}'").set_index("date")["value"].dropna()
    print(f"  UST {t}: 02/10 {s['2026-10-02']} -> 05/10 {s['2026-10-05']} = {100*(s['2026-10-05']-s['2026-10-02']):+.0f} p.b.; 04/09 -> 05/10 {100*(s['2026-10-05']-s['2026-09-04']):+.0f} p.b.")
ff = us.query("curve=='POLICY'").set_index("date")["value"]
print("  Fed Funds: mudancas em 2026:", ff[ff.diff() != 0]["2026-01-01":].to_dict())

print("\n(2) Carry")
ff0 = 3.875; selic = 13.75
print(f"  Selic {selic} - Fed Funds {ff0} = {selic-ff0:.3f} p.p.; / vol 63d 12,2 = {(selic-ff0)/12.2:.2f}")
cal = {"2026-12-09": 13.26, "2027-03-17": 12.83, "2027-06-16": 12.42, "2027-09-22": 12.18, "2027-12-08": 12.20}
for q, v in [("4T26", 13.26), ("1T27", 12.83), ("2T27", 12.42), ("3T27", 12.18), ("4T27", 12.20)]:
    print(f"  {q}: Selic na curva {v} - FF {ff0} = {v-ff0:.2f} p.p.")
print("  Focus Selic fim de 2026 13,50 / 2027 12,00:", 13.50 - ff0, 12.00 - ff0)

print("\n(3) Inflacao")
dj = rd("diferenciais_juros").pivot(index="date", columns="name", values="value")
last = dj[["ipca_12m", "cpi_12m_us"]].dropna().iloc[-1] if "ipca_12m" in dj else None
print("  colunas:", list(dj.columns))
ip, cp = 4.22, 3.35
print(f"  IPCA 12m {ip} - CPI 12m {cp} = {ip-cp:.2f} p.p.; Focus IPCA 2027 4,31 - CPI 3,35 = {4.31-cp:.2f}; Focus 2028 3,80 - 3,35 = {3.80-cp:.2f}")

print("\n(4) Dezembro, 2016-2025")
cc = rd("cmb_cambio_contratado")
m = cc[cc["name"].isin(["cc_saldo_total", "cc_fin_saldo", "cc_saldo_comercial"])]
m = m[m["sgs_code"].isin([13961, 13967, 13970])]
mm = m.groupby([m["date"].dt.to_period("M"), "name"])["value"].sum().unstack() / 1000
print("  conferencia ago/2026 (F: total -3,90; fin -9,09; com 5,18):", mm.loc[pd.Period("2026-08")].round(2).to_dict())
mm = mm[(mm.index >= pd.Period("2016-01")) & (mm.index <= pd.Period("2025-12"))]
dec = mm[mm.index.month == 12]; oth = mm[mm.index.month != 12]
print("  dezembro, media US$ bi:", dec.mean().round(2).to_dict())
print("  demais meses, media US$ bi:", oth.mean().round(2).to_dict())
print("  dezembro, ano a ano (total):", {str(k): round(v, 2) for k, v in dec["cc_saldo_total"].items()})
pt = rd("cmb_ptax").query("name=='ptax_venda'").set_index("date")["value"].dropna()
me = pt.resample("ME").last()
ch = 100 * me.pct_change()
chd = ch[(ch.index.month == 12) & (ch.index.year >= 2016) & (ch.index.year <= 2025)]
print("  PTAX em dezembro, % no mes:", {k.year: round(v, 2) for k, v in chd.items()}, "media", round(chd.mean(), 2),
      "| depreciou em", int((chd > 0).sum()), "de", len(chd))

print("\n(5) Caminho central")
S = 4.9698
cent = {"4T26": 5.05, "1T27": 5.08, "2T27": 5.10, "3T27": 5.13, "4T27": 5.16, "1T28": 5.18}
fwd = {"4T26": 5.0676, "1T27": 5.1657, "2T27": 5.2638, "3T27": 5.3600, "4T27": 5.4455, "1T28": 5.5338}
for q, c in cent.items():
    print(f"  {q}: central {c} vs spot {100*(c/S-1):+.1f}% | vs forward {100*(c/fwd[q]-1):+.1f}%")
print(f"  4T26 vs Focus 2026 5,20: {5.05-5.20:+.2f} | 4T27 vs Focus 2027 5,28: {5.16-5.28:+.2f}")
print(f"  PTAX 02/10 5,2238 vs central 4T26: {100*(5.05/5.2238-1):+.1f}%")

print("\n(6) Contra o condicionante do Copom (R$ 5,15, 281a reuniao)")
print(f"  PTAX 06/10 4,9698 vs 5,15: {100*(4.9698/5.15-1):+.1f}% | central 4T26 5,05 vs 5,15: {100*(5.05/5.15-1):+.1f}%")
print(f"  PTAX 02/10 5,2238 vs 5,15: {100*(5.2238/5.15-1):+.1f}%")
