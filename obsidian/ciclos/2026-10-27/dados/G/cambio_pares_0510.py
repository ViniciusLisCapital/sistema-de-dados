"""G cambio (rodada 2): o pregão de 05/10 (1º turno) contra os pares e os índices de dólar, na mesma data
(peso chileno e colombiano deslocados um pregão, pela Atenção do F); e a ordem de grandeza da variação cambial
sobre o estoque de swaps do BC (pedido FS-CB2 do fiscal)."""
import pandas as pd
from pathlib import Path

A = Path(__file__).resolve().parent.parent / "A"
def ler(t): return pd.read_csv(A / f"{t}.csv.gz", parse_dates=["date"])
pt = ler("cmb_ptax"); pt = pt[pt.name == "ptax_venda"].set_index("date").value.rename("BRL")
lat = ler("cmb_fx_latam").pivot(index="date", columns="country_code", values="value")
for c in ("CL", "CO"):
    s = lat[c].dropna(); lat[c] = pd.Series(s.values[1:], index=s.index[:-1]).reindex(lat.index)
em = ler("cmb_dollar_index_em").set_index("date").value.rename("DXY_EM")
dxy = ler("cmb_dollar_index").set_index("date").value.rename("DXY")
df = pd.concat([pt, lat, em, dxy], axis=1)
w = df[(df.index >= "2026-09-29") & (df.index <= "2026-10-09")]
print(w.round(4).to_string())
print("\nVariação % de 02/10 para 05/10:")
for c in df.columns:
    a, b = df[c].get(pd.Timestamp("2026-10-02")), df[c].get(pd.Timestamp("2026-10-05"))
    print(f"  {c}: {100 * (b / a - 1):+.2f}%" if pd.notna(a) and pd.notna(b) else f"  {c}: sem dado")

sw = ler("cmb_reservas_bc")
print("\nséries de cmb_reservas_bc:", sw.name.unique() if "name" in sw else sw.columns.tolist())
estoque = 91.6   # US$ bi vendido, ago/26 (F_cambio, cmb_reservas_bc)
for ini, fim in [("2026-09-30", "2026-10-26"), ("2026-10-23", "2026-10-26")]:
    dv = pt.loc[fim] - pt.loc[ini]
    print(f"estoque x variação da PTAX {ini}->{fim}: {dv:.4f} R$/US$ -> R$ {estoque * dv:.1f} bi (perda do BC, só a variação cambial)")
