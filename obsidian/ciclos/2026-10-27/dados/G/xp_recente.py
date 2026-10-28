"""Expectativas: trajetória diária recente de PTAX, CDS e inflação implícita (DIPRE/NTNBJS) por vértice.

Lê só A/. Imprime de 2026-09-24 até o último dado, para localizar QUANDO o salto aconteceu
(antes ou depois da última Focus, de 2026-10-23).
"""
from pathlib import Path
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"
ini = "2026-09-24"

ptax = pd.read_csv(A / "cmb_ptax.csv.gz")
ptax = ptax[(ptax.name == "ptax_venda") & (ptax.date >= ini)].set_index("date").value.rename("ptax")
cds = pd.read_csv(A / "cmb_risco_pais.csv.gz")
cds = cds[(cds.name == "cds_5y_usd") & (cds.date >= ini)].set_index("date").value.rename("cds")

r = pd.read_csv(A / "br_interest_rate.csv.gz")
r = r[r.date >= ini]
out = [ptax, cds]
for ten in ["12M", "24M", "60M", "120M"]:
    di = r[(r.curve == "DIPRE") & (r.tenor == ten)].set_index("date").value
    nb = r[(r.curve == "NTNBJS") & (r.tenor == ten)].set_index("date").value
    imp = ((1 + di / 100) / (1 + nb / 100) - 1) * 100
    out += [di.rename(f"di_{ten}"), nb.rename(f"ntnb_{ten}"), imp.rename(f"impl_{ten}")]
df = pd.concat(out, axis=1).sort_index()
pd.set_option("display.width", 250)
print(df.round(2).to_string())

# variação no último pregão e desde 2026-10-02 (ciclo anterior) e 2026-10-23 (última Focus)
for ref in ["2026-10-02", "2026-10-23"]:
    base = df.loc[:ref].ffill().iloc[-1]
    last = df.ffill().iloc[-1]
    print(f"\nÚltimo ({df.index[-1]}) contra {ref}:")
    for c in df.columns:
        if c == "ptax":
            print(f"  {c}: {base[c]:.4f} -> {last[c]:.4f}  ({(last[c]/base[c]-1)*100:+.2f}%)")
        else:
            print(f"  {c}: {base[c]:.2f} -> {last[c]:.2f}  ({last[c]-base[c]:+.2f})")
