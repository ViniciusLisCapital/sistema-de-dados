"""fi (rodada 2): NTN-B 10a e CDS por mês em 2026 (onde o nível de 26/10 fica contra o ano), a média de
4T26 (`rr_10a`) sob cada nível suposto para os pregões restantes, e o primário do Focus contra a meta
fiscal noticiada (r1-19), em p.p."""
from pathlib import Path
import sys
import pandas as pd
sys.stdout.reconfigure(encoding="utf-8")
A = Path(__file__).resolve().parent.parent / "A"
d = pd.read_csv(A / "br_interest_rate.csv.gz", parse_dates=["date"])
n = d[(d.tenor == "120M") & (d.curve == "NTNBJS")].set_index("date").value.sort_index()
cds = pd.read_csv(A / "cmb_risco_pais.csv.gz", parse_dates=["date"]).set_index("date").sort_index().iloc[:, -1]

print("NTN-B 10a e CDS por mês, 2026: média, mín, máx, último")
for m in pd.period_range("2026-01", "2026-10", freq="M"):
    x = n[(n.index.to_period("M") == m)]
    c = cds[(cds.index.to_period("M") == m)]
    print(f"  {m}: NTN-B média {x.mean():.2f} mín {x.min():.2f} máx {x.max():.2f} último {x.iloc[-1]:.2f}"
          f" · CDS média {c.mean():.0f} mín {c.min():.0f} máx {c.max():.0f} último {c.iloc[-1]:.0f}")

print("\nDias de 2026 com NTN-B 10a >= 8,00:", int((n["2026-01-01":] >= 8.0).sum()),
      "· máx de 2026:", round(n["2026-01-01":].max(), 2), "em", n["2026-01-01":].idxmax().date())
print("Máx em 10 anos:", round(n["2016-10-27":].max(), 2), "em", n["2016-10-27":].idxmax().date())

# 4T26: pregões até 26/10 e restantes
q = n["2026-10-01":"2026-12-31"]
k, s = len(q), q.sum()
fer = pd.to_datetime(["2026-11-02", "2026-11-20", "2026-12-24", "2026-12-25", "2026-12-31"])
rest = [x for x in pd.bdate_range("2026-10-27", "2026-12-31") if x not in fer]
r = len(rest)
print(f"\n4T26: {k} pregões até {q.index.max().date()}, média {q.mean():.3f}; restantes {r}")
for lv in [7.40, 7.45, 7.50, 7.75, 7.90, 7.95, 8.00, 8.05, 8.25, 8.50, 8.60]:
    print(f"  restantes a {lv:.2f}: média 4T26 = {(s + r * lv) / (k + r):.3f}")

# Focus de primário contra a meta noticiada (r1-19): 2026 0,25 ± 0,25; 2027 0,50 ± 0,25
f = {"2026": -0.48, "2027": -0.30}
meta = {"2026": 0.25, "2027": 0.50}
print("\nFocus primário (expc_focus_periodo, 23/10) contra a meta noticiada:")
for a in f:
    print(f"  {a}: Focus {f[a]:+.2f} · meta {meta[a]:.2f} · piso {meta[a]-0.25:.2f} · Focus − meta {f[a]-meta[a]:+.2f}"
          f" · Focus − piso {f[a]-(meta[a]-0.25):+.2f}")
print("  RTN sem precatórios 12m ago/26 (+0,29, fi_precatorios) − meta 2026:", round(0.29 - 0.25, 2),
      "· − piso:", round(0.29 - 0.0, 2))
print("  RTN com precatórios 12m ago/26 (−0,53) − piso 2026:", round(-0.53 - 0.0, 2))
