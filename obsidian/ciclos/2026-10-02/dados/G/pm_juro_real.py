"""pm: a postura (juro real ex-ante contra os neutros) e as distâncias que o report cita, com o que
existia em 02/10 (Focus da pesquisa de 25/09, publicada em 28/09).

Neutros: Copom 5,00% (RPM set/26, seção 2.2); QPC R279 (expc_qpc): 2a 6,00, 5a 5,50, curto 6,40;
âncora do Modelo Estrutural: rr_10a (NTN-B 10a) + meta.
"""
from pathlib import Path

import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"
rd = lambda t: pd.read_csv(A / f"{t}.csv.gz", parse_dates=["date"])

f = rd("expc_focus")
f12 = f[(f.base_calculo == 0) & (f.horizonte == "12m") & (f.suavizada == "S")
        & (f.indicador == "IPCA")].set_index("date")["mediana"]
r = rd("br_interest_rate")
g = lambda c, t: r[(r.curve == c) & (r.tenor == t)].set_index("date")["value"]
ntnb10, di1, ntnb1 = g("NTNBJS", "120M"), g("DIPRE", "12M"), g("NTNBJS", "12M")

selic, meta = 13.75, 3.00
pi = f12[:"2026-09-25"].iloc[-1]
real = 100 * ((1 + selic / 100) / (1 + pi / 100) - 1)
print("Focus 12m (25/09):", pi, " Selic real ex-ante:", round(real, 2))
for nome, n in [("Copom", 5.00), ("QPC 2a", 6.00), ("QPC 5a", 5.50), ("QPC curto", 6.40)]:
    print(f"  contra neutro {nome} {n}: {real - n:+.2f} p.p.")
rr = ntnb10[:"2026-10-02"].iloc[-1]
print("NTN-B 10a 02/10:", rr, " âncora nominal do modelo (rr+meta):", round(rr + meta, 2),
      " Selic − âncora:", round(selic - rr - meta, 2), " Selic real ex-ante − rr_10a:", round(real - rr, 2))
rr3 = ntnb10["2026-07-01":"2026-09-30"].mean()
print("âncora com rr_10a média 3T26:", round(rr3 + meta, 2), " Δ âncora (02/10 contra média 3T26):", round(rr - rr3, 2))
d1 = di1[:"2026-09-25"].iloc[-1]
print("DI 1a 25/09:", round(d1, 2), " real ex-ante com Focus 12m:", round(100 * ((1 + d1 / 100) / (1 + pi / 100) - 1), 2),
      " NTN-B 1a 25/09:", round(ntnb1[:"2026-09-25"].iloc[-1], 2))

pt = rd("cmb_ptax")
print(pt.name.unique()[:5])
pv = pt[pt.name == pt.name.unique()[0]].set_index("date")["value"]
for d in ["2026-09-04", "2026-09-16", "2026-09-25", "2026-10-02"]:
    print("PTAX", d, pv[:d].iloc[-1], " contra 5,15 (condicionante do Copom):",
          f"{100 * (pv[:d].iloc[-1] / 5.15 - 1):+.1f}%")
print("PTAX Δ% 16/09 -> 02/10:", f"{100 * (pv.iloc[-1] / pv[:'2026-09-16'].iloc[-1] - 1):+.1f}")

c = rd("cmb_risco_pais").set_index("date")["value"]
print("CDS Δ 16/09 -> 02/10:", round(c.iloc[-1] - c[:"2026-09-16"].iloc[-1], 1))

b = rd("comm_brent").set_index("date")["value"]
print("Brent 02/10 contra US$ 90 (ponto de partida do RPM):", f"{100 * (b.iloc[-1] / 90 - 1):+.0f}%",
      " média 3T26:", round(b["2026-07-01":"2026-09-30"].mean(), 1))

# Selic precificada: DI contra Focus (25/09) por reunião — o F traz o de 02/10
fc = rd("expc_focus_copom")
fc = fc[(fc.base_calculo == 0) & (fc.date == "2026-09-25")].set_index("reuniao")["mediana"]
curva = {"R7/2026": 13.60, "R8/2026": 13.54, "R1/2027": 13.55, "R2/2027": 13.57, "R3/2027": 13.57,
         "R4/2027": 13.58, "R5/2027": 13.61, "R6/2027": 13.68, "R7/2027": 13.79, "R8/2027": 13.95}
print("curva DI (02/10, F) − Focus (25/09), p.b.:",
      {k: round(100 * (v - fc[k])) for k, v in curva.items()})
