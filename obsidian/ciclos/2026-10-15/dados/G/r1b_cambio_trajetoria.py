"""G r1b: trajetória diária de 01/08 a 15/10 da PTAX, CDS, DXY, dólar EM, pares, DI 1/5 anos e Brent,
para datar o movimento recente; variações desde o fim do 3T26 (30/09) e no pico/vale."""
from pathlib import Path
import numpy as np
import pandas as pd

A = Path(__file__).resolve().parents[1] / "A"
def s(tab, name, col="name"):
    d = pd.read_csv(A / f"{tab}.csv.gz", parse_dates=["date"])
    return d[d[col] == name].set_index("date")["value"].sort_index()

di = pd.read_csv(A / "br_di_grade.csv.gz", parse_dates=["date"])
di = di[di.date >= "2026-07-01"]
def di_prazo(du):
    out = {}
    for d, g in di.groupby("date"):
        g = g.sort_values("du")
        out[d] = np.interp(du, g.du, g.value)
    return pd.Series(out)

df = pd.DataFrame({
    "ptax": s("cmb_ptax", "ptax_venda"),
    "cds": s("cmb_risco_pais", "cds_5y_usd"),
    "dxy": s("cmb_dollar_index", "dxy"),
    "dxy_em": s("cmb_dollar_index_em", "dxy_em"),
    "mxn": s("cmb_fx_latam", "MX", "country_code"),
    "clp": s("cmb_fx_latam", "CL", "country_code"),
    "cop": s("cmb_fx_latam", "CO", "country_code"),
    "pen": s("cmb_fx_latam", "PE", "country_code"),
    "brent": s("comm_brent", "brent_usd"),
    "di1a": di_prazo(252), "di5a": di_prazo(1260),
})
df = df["2026-08-01":]
pd.set_option("display.width", 250)
print(df.round(3).to_string())

print("\nVariação desde 30/09 (fim do 3T26) até o último dado de cada série:")
for c in df.columns:
    x = df[c].dropna()
    base = x[:"2026-09-30"].iloc[-1]
    last = x.iloc[-1]
    if c.startswith("di") or c == "cds":
        print(f"  {c}: {base:.2f} -> {last:.2f} ({x.index[-1].date()}) · Δ {(last-base)*(100 if c.startswith('di') else 1):+.1f} {'p.b.' }")
    else:
        print(f"  {c}: {base:.4f} -> {last:.4f} ({x.index[-1].date()}) · {100*(last/base-1):+.2f}%")
