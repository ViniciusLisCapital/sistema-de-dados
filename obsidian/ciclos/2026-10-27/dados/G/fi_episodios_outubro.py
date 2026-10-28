"""fi: painel diário desde set/2026 — CDS, curva real e nominal, PTAX contra pares e variáveis globais.
Separa o que é doméstico do que é global nos dois saltos de outubro (05/10 e 26/10)."""
from pathlib import Path
import pandas as pd
A = Path(__file__).resolve().parent.parent / "A"
r = lambda f: pd.read_csv(A / f"{f}.csv.gz", parse_dates=["date"])
br = r("br_interest_rate")
col = {}
for cv, tn, nm in [("DIPRE", "12M", "DI1a"), ("DIPRE", "60M", "DI5a"), ("DIPRE", "120M", "DI10a"),
                   ("NTNBJS", "24M", "NB2a"), ("NTNBJS", "60M", "NB5a"), ("NTNBJS", "120M", "NB10a")]:
    col[nm] = br[(br.curve == cv) & (br.tenor == tn)].set_index("date").value
cds = r("cmb_risco_pais"); col["CDS"] = cds[cds.name == "cds_5y_usd"].set_index("date").value
pt = r("cmb_ptax"); col["PTAX"] = pt[pt.name == "ptax_venda"].set_index("date").value
fx = r("cmb_fx_latam")
for c in ["MX", "CL", "CO"]:
    col[c] = fx[fx.country_code == c].set_index("date").value
de = r("cmb_dollar_index_em"); col["DXYEM"] = de.set_index("date").value
us = r("us_interest_rate"); col["UST10"] = us[(us.curve != "POLICY") & (us.tenor == "120M")].set_index("date").value \
    if "120M" in us.tenor.unique() else None
print(us[us.curve != "POLICY"][["curve", "tenor"]].drop_duplicates().to_string())
bz = r("comm_brent"); col["Brent"] = bz.set_index("date").value
sp = r("cmb_equity_us"); col["SP"] = sp.set_index("date").value
p = pd.DataFrame({k: v for k, v in col.items() if v is not None})
p = p[p.index >= "2026-09-01"]
pd.set_option("display.width", 250)
print(p.round(3).to_string())
# variações nos dois episódios (último pregão antes -> primeiro depois)
def var(a, b):
    x, y = p.loc[a], p.loc[b]
    out = {}
    for k in p.columns:
        if k in ("PTAX", "MX", "CL", "CO", "DXYEM", "Brent", "SP"):
            out[k] = round(100 * (y[k] / x[k] - 1), 2)
        elif k == "CDS":
            out[k] = round(y[k] - x[k], 1)
        else:
            out[k] = round(100 * (y[k] - x[k]), 0)  # p.b.
    return out
print("05/10 contra 02/10:", var("2026-10-02", "2026-10-05"))
print("26/10 contra 23/10:", var("2026-10-23", "2026-10-26"))
print("26/10 contra 30/09:", var("2026-09-30", "2026-10-26"))
