"""G r1b: diferenças pontuais usadas no texto: COT do BRL na semana da eleição (29/09 -> 06/10),
diferencial DI 2a − Treasury 2a entre 14/09 e 13/10, movimento da PTAX e do DI 5a em 02/10 -> 05/10,
média dos pares desde 30/09 e em 1m (tabela "O real e os pares")."""
from pathlib import Path
import numpy as np
import pandas as pd

A = Path(__file__).resolve().parents[1] / "A"
rd = lambda t: pd.read_csv(A / f"{t}.csv.gz", parse_dates=["date"])

t = rd("cmb_cot_fx"); t = t[t.currency == "BRL"].pivot_table(index="date", columns="name", values="value")
a, b = t.loc["2026-09-29"], t.loc["2026-10-06"]
for k in ["lev_net", "lev_long", "lev_short", "asset_mgr_net", "dealer_net", "open_interest"]:
    print(f"COT {k}: {a[k]:.0f} -> {b[k]:.0f} · Δ {b[k]-a[k]:+.0f}")
print(f"COT lev_net 06/10 x 01/09: {t.loc['2026-10-06','lev_net']-t.loc['2026-09-01','lev_net']:+.0f}")

print(f"Diferencial DI2a−UST2a: 9,16 (14/09) -> 7,68 (13/10): Δ {7.68-9.16:+.2f} p.p. (níveis do G r1b_cambio_mercado)")

p = rd("cmb_ptax"); p = p[p.name == "ptax_venda"].set_index("date")["value"]
print(f"PTAX 02/10 -> 05/10: {p['2026-10-02']:.4f} -> {p['2026-10-05']:.4f} · {100*(p['2026-10-05']/p['2026-10-02']-1):+.2f}%")
print(f"PTAX 05/10 -> 14/10: {100*(p['2026-10-14']/p['2026-10-05']-1):+.2f}% · mínimo de out: {p['2026-10'].min():.4f} em {p['2026-10'].idxmin().date()}")
print(f"PTAX 17/09 (máx. set antes do fim) e 29/09: {p['2026-09-17']:.4f}, {p['2026-09-29']:.4f}; 17/09->29/09 {100*(p['2026-09-29']/p['2026-09-17']-1):+.2f}%")

di = rd("br_di_grade")
def di_at(d, du):
    g = di[di.date == d].sort_values("du"); return np.interp(du, g.du, g.value)
for du, nm in [(252, "1a"), (1260, "5a")]:
    x0, x1 = di_at("2026-10-02", du), di_at("2026-10-05", du)
    print(f"DI {nm} 02/10 -> 05/10: {x0:.2f} -> {x1:.2f} · Δ {100*(x1-x0):+.0f} p.b.")

fx = rd("cmb_fx_latam").pivot_table(index="date", columns="country_code", values="value")
peers = ["MX", "CL", "CO", "PE"]
base = fx[:"2026-09-30"].ffill().iloc[-1]
last = fx.ffill().iloc[-1]
ch = 100 * (last / base - 1)
print("Pares desde 30/09 (%):", ch[peers].round(2).to_dict(), "média", round(ch[peers].mean(), 2))
for c in ["MX", "CL", "CO", "PE"]:
    pass
print("Pares 1m (tabela O real e os pares): MXN +8,0 CLP +4,4 COP +3,3 PEN +2,8 -> média", round(np.mean([8.0, 4.4, 3.3, 2.8]), 2), "· BRL −2,4 -> diferença", round(-2.4 - np.mean([8.0, 4.4, 3.3, 2.8]), 2), "p.p.")
print("Pares 3m: MXN +4,8 CLP +5,8 COP −3,6 PEN +1,5 -> média", round(np.mean([4.8, 5.8, -3.6, 1.5]), 2), "· BRL −0,6 -> diferença", round(-0.6 - np.mean([4.8, 5.8, -3.6, 1.5]), 2), "p.p.")
print("PTAX desde 30/09 −2,64% x média pares", round(ch[peers].mean(), 2), "-> diferença", round(-2.64 - ch[peers].mean(), 2), "p.p.")
r = rd("cmb_reservas_bc")
s = r[r.name == "bcb_swap_cambial_position"].set_index("date")["value"]
print(f"Swap: jul {s['2026-07-01']/1000:.1f} -> ago {s['2026-08-01']/1000:.1f} bi")
# pares no pregão de 05/10 (contra 02/10)
for c in peers:
    x = fx[c].dropna()
    if pd.Timestamp("2026-10-05") in x.index:
        print(f"{c} 02/10 -> 05/10: {100*(x['2026-10-05']/x['2026-10-02']-1):+.2f}%")
