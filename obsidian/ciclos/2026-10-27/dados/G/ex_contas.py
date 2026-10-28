"""G externo: as contas pequenas citadas no report (variações dos cenários contra o último dado, distâncias,
diferenças da decomposição da PTAX). Lê ../A/ e os números impressos pelos outros G (ex_cenarios, ex_decomp)."""
import numpy as np, pandas as pd
from pathlib import Path
A = Path(__file__).resolve().parent.parent / "A"
pct = lambda a, b: 100*(a/b-1)
sp = pd.read_csv(A/"cmb_equity_us.csv.gz", parse_dates=["date"]).set_index("date")["value"]
print(f"S&P 27/10 contra a máxima de 06/10: {pct(sp.iloc[-1], sp.max()):+.1f}%")
cur = pd.read_csv(A/"us_interest_rate__curva_completa.csv.gz", parse_dates=["date"])
t10 = cur[(cur.curve=="US_TREASURY")&(cur.tenor=="10Y")].set_index("date")["value"]
print(f"Treasury 10a 21/10 -> 22/10: {t10.loc['2026-10-22']-t10.loc['2026-10-21']:+.2f} p.p.")
br = pd.read_csv(A/"comm_brent.csv.gz", parse_dates=["date"]).set_index("date")["value"]
print(f"Brent 01/10 -> 02/10: {pct(br.loc['2026-10-02'], br.loc['2026-10-01']):+.1f}%")
print(f"metais: alta 362 contra 3T26 330,14: {pct(362,330.14):+.1f}% ; queda 275: {pct(275,330.14):+.1f}%")
print(f"agro: alta 215 contra 3T26 200,53: {pct(215,200.53):+.1f}% ; queda 185: {pct(185,200.53):+.1f}%")
print(f"S&P risk-off 6500 contra 7717 (27/10): {pct(6500,7717.26):+.1f}% ; base 8500 contra 7651,54 (3T26): {pct(8500,7651.54):+.1f}%")
print(f"S&P risk-on por trimestre: " + ", ".join(f"{pct(b,a):+.1f}%" for a,b in zip([7651.54,7950,8300,8650],[7950,8300,8650,8950])))
print(f"S&P base por trimestre: " + ", ".join(f"{pct(b,a):+.1f}%" for a,b in zip([7651.54,7750,7900,8050,8200,8350],[7750,7900,8050,8200,8350,8500])))
print(f"dólar EM risk-off 136,5 contra 130,21: {pct(136.5,130.21):+.1f}% ; risk-on 124 contra 130,21: {pct(124,130.21):+.1f}%")
print(f"agro 201,8 contra o recorde 203,94: {pct(201.8,203.94):+.1f}%")
dec = {"padrão":[5.210,5.247,5.251,5.237,5.253,5.278],"base":[5.288,5.388,5.418,5.426,5.466,5.502],
       "ffr":[5.274,5.374,5.403,5.412,5.451,5.497],"infl_us":[5.285,5.369,5.383,5.377,5.400,5.422],
       "dxy_em":[5.249,5.331,5.378,5.404,5.461,5.515],"sp500":[5.273,5.350,5.357,5.342,5.359,5.373],
       "icbr_usd":[5.283,5.376,5.401,5.406,5.442,5.475]}
for k in ["ffr","infl_us","dxy_em","sp500","icbr_usd"]:
    print(f"PTAX base − base sem {k}: " + " ".join(f"{b-x:+.3f}" for b, x in zip(dec["base"], dec[k])))
