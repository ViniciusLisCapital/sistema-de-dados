"""Forward de referencia da PTAX e calibracao das faixas por trimestre (G do ciclo 2026-10-07).
Le so ../A/.
(1) Forward por paridade coberta aproximada: S x (1+DI)^(du/252) / (1+juro EUA)^(dc/365), com o DI
    interpolado na grade da B3 de 06/10/2026 e o juro dos EUA interpolado entre o Fed Funds (meta,
    ponto medio) e o Treasury de 2 anos. Aproximacao: o forward de mercado usa o cupom cambial, que
    nao esta no F.
(2) Distribuicao historica da variacao da PTAX no mesmo numero de dias uteis ate cada fechamento de
    trimestre (janelas sobrepostas, out/2016-out/2026): quantis e a massa dentro de faixas candidatas
    centradas na mediana historica."""
from pathlib import Path
import numpy as np
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"
rd = lambda t: pd.read_csv(A / f"{t}.csv.gz", parse_dates=["date"])
ptax = rd("cmb_ptax").query("name=='ptax_venda'").set_index("date")["value"].dropna()
S, d0 = ptax.iloc[-1], ptax.index[-1]
di = rd("br_di_grade"); g = di[di["date"] == d0].sort_values("dc")
us = rd("us_interest_rate")
ff = us.query("curve=='POLICY'").set_index("date")["value"]; ff = ff[ff.index <= d0].iloc[-1]
u2 = us.query("curve=='US_TREASURY' and tenor=='2Y'").set_index("date")["value"].dropna(); u2 = u2[u2.index <= d0].iloc[-1]
print(f"Spot {S} em {d0.date()} | Fed Funds {ff} | UST 2a {u2}")

qe = {"4T26": "2026-12-31", "1T27": "2027-03-31", "2T27": "2027-06-30",
      "3T27": "2027-09-30", "4T27": "2027-12-31", "1T28": "2028-03-31"}
dus = {}
print("\nForward de referencia:")
for q, d in qe.items():
    dc = (pd.Timestamp(d) - d0).days
    du = np.interp(dc, g["dc"], g["du"]); i_br = np.interp(dc, g["dc"], g["value"])
    i_us = ff + (u2 - ff) * min(dc / 730, 1)
    F = S * (1 + i_br / 100) ** (du / 252) / (1 + i_us / 100) ** (dc / 365)
    dus[q] = int(round(du))
    print(f"{q} {d}: dc={dc} du={du:.0f} DI={i_br:.2f} EUA={i_us:.2f} forward={F:.4f} ({100*(F/S-1):+.1f}%)")

lp = np.log(ptax[ptax.index >= "2016-10-01"])
print("\nDistribuicao da variacao da PTAX em h dias uteis (out/2016-out/2026), em %:")
cands = {"4T26": [(4.85, 5.20), (4.90, 5.25), (4.85, 5.25)],
         "1T27": [(4.85, 5.35), (4.80, 5.35)],
         "2T27": [(4.80, 5.45), (4.75, 5.45)],
         "3T27": [(4.75, 5.55), (4.75, 5.60)],
         "4T27": [(4.75, 5.65), (4.70, 5.65)],
         "1T28": [(4.75, 5.70), (4.70, 5.75)]}
cent = {"4T26": 5.05, "1T27": 5.08, "2T27": 5.10, "3T27": 5.13, "4T27": 5.16, "1T28": 5.18}
for q, h in dus.items():
    x = (lp.shift(-h) - lp).dropna()
    xd = x - x.median()
    qs = 100 * (np.exp(x.quantile([.1, .2, .25, .5, .75, .8, .9])) - 1)
    print(f"{q} h={h}: " + " ".join(f"p{int(k*100)}={v:+.1f}" for k, v in qs.items())
          + f" | desvio-padrao log={100*x.std():.1f}")
    for lo, hi in cands[q]:
        lvl = cent[q] * np.exp(xd)
        pin = ((lvl >= lo) & (lvl <= hi)).mean(); pab = (lvl > hi).mean(); pbe = (lvl < lo).mean()
        print(f"   central {cent[q]} faixa {lo}-{hi}: dentro {100*pin:.0f}% | acima {100*pab:.0f}% | abaixo {100*pbe:.0f}%")
