"""fi: NTN-B 10a, DI 10a e CDS 5a diários desde set/2026 — confere a média de 4T26 (rr_10a) do F e o movimento de outubro."""
from pathlib import Path
import pandas as pd
A = Path(__file__).resolve().parent.parent / "A"
d = pd.read_csv(A / "br_interest_rate.csv.gz", parse_dates=["date"])
cds = pd.read_csv(A / "cmb_risco_pais.csv.gz", parse_dates=["date"])
print(cds.columns.tolist()); print(cds.tail(3))
s = d[(d.tenor == "120M") & d.curve.isin(["NTNBJS", "DIPRE"])].pivot_table(index="date", columns="curve", values="value")
s = s[s.index >= "2026-08-15"]
c = cds.set_index("date").iloc[:, -1]
s["CDS"] = c.reindex(s.index)
pd.set_option("display.width", 200)
print(s.to_string())
for q, (a, b) in {"3T26": ("2026-07-01", "2026-09-30"), "4T26": ("2026-10-01", "2026-12-31")}.items():
    x = d[(d.tenor == "120M") & (d.curve == "NTNBJS") & (d.date >= a) & (d.date <= b)]
    print(q, "NTNB120M média", round(x.value.mean(), 3), "n", len(x), "min", x.value.min(), "max", x.value.max())
