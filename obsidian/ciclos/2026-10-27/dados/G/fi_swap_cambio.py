"""fi: ordem de grandeza do resultado do swap cambial do BC com a alta da PTAX de outubro (posição de ago/26 ×
variação da PTAX), em R$ bi e % do PIB 12m; e a PTAX de ago/25 contra ago/26, para ler o sinal do ajuste cambial
da DLSP (fisc_dlsp_fatores) nos 12 meses até ago/26."""
from pathlib import Path
import pandas as pd
A = Path(__file__).resolve().parent.parent / "A"
r = lambda f: pd.read_csv(A / f"{f}.csv.gz", parse_dates=["date"])
pt = r("cmb_ptax"); pt = pt[pt.name == "ptax_venda"].set_index("date").value.sort_index()
res = r("cmb_reservas_bc"); print(res.name.unique() if "name" in res.columns else res.columns)
sw = res[res.name.str.contains("swap")].set_index("date").value.sort_index() if "name" in res.columns else None
print("swap último:", sw.index[-1].date(), sw.iloc[-1])
pm = r("atv_pib_mensal"); pm = pm[pm.name == "pib_mensal"].set_index("date").value
pib12 = pm.rolling(12).sum().iloc[-1]
pos = abs(sw.iloc[-1]) / 1000  # US$ milhões -> US$ bi
for a, b in [("2026-09-30", "2026-10-26"), ("2026-10-23", "2026-10-26")]:
    dp = pt.loc[b] - pt.loc[a]
    perda = pos * dp
    print(f"PTAX {a} {pt.loc[a]:.4f} -> {b} {pt.loc[b]:.4f}: Δ R$ {dp:.4f}/US$ · resultado do swap ≈ −R$ {perda:.1f} bi = {100*perda/(pib12/1000):.2f}% do PIB 12m")
m = pt.resample("ME").mean()
print("PTAX média de ago/25", round(m.loc["2025-08-31"], 4), "· ago/26", round(m.loc["2026-08-31"], 4), "· fim de ago/25", round(pt[:"2025-08-31"].iloc[-1], 4), "· fim de ago/26", round(pt[:"2026-08-31"].iloc[-1], 4))
