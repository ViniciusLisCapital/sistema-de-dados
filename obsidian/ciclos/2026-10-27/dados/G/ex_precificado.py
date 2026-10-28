"""G externo: o caminho do Fed Funds efetivo que os T-bills de 23/10 precificam, descontado o prêmio
medido em meses de Fed parado (ex_risco_dolar.py), e a média implícita de cada janela. Lê só ../A/."""
import pandas as pd
from pathlib import Path
A = Path(__file__).resolve().parent.parent / "A"
cur = pd.read_csv(A/"us_interest_rate__curva_completa.csv.gz", parse_dates=["date"])
t = cur[(cur.curve=="US_TREASURY")&(cur.date=="2026-10-23")].set_index("tenor")["value"]
meta = 3.875; spread_efetivo = 0.005  # efetivo − meta desde mai/26 (ex_eua_politica.py)
eff0 = meta + spread_efetivo
for nome, prem in [("prêmio desde 2001", {"3M":-0.03,"6M":0.03,"1Y":0.10}), ("prêmio desde 2017", {"3M":0.05,"6M":0.08,"1Y":0.09}), ("sem prêmio", {"3M":0,"6M":0,"1Y":0})]:
    m3 = t["3M"]-prem["3M"]; m6 = t["6M"]-prem["6M"]; m12 = t["1Y"]-prem["1Y"]
    f36 = 2*m6-m3; f612 = 2*m12-m6
    print(f"{nome}: média 0-3m {m3:.2f} | 3-6m {f36:.2f} | 6-12m {f612:.2f} | média 12m {m12:.2f} | acima do efetivo de hoje ({eff0:.2f}): 0-3m {m3-eff0:+.2f}, 3-6m {f36-eff0:+.2f}, 6-12m {f612-eff0:+.2f} p.p. = {((f612-eff0)/0.25):.1f} altas de 25 p.b. no fim da janela")
