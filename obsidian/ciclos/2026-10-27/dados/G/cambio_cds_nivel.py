"""G cambio (rodada 2): o real reage mais a um p.b. de CDS quando o CDS está baixo?
Regressão da variação da PTAX (log, %) na variação do CDS (p.b.), com e sem o dólar contra emergentes,
por faixa de nível do CDS no início do período. Diária (2006-2026, com dxy_em) e trimestral (fim de
trimestre). Testa o argumento do fiscal para F.b_fiscal x 1,5 no upside. Mais: os níveis da PTAX
em torno de 02/10, 05/10, 23/10 e 26/10."""
import numpy as np
import pandas as pd
from pathlib import Path

A = Path(__file__).resolve().parent.parent / "A"
def serie(t, nome):
    d = pd.read_csv(A / f"{t}.csv.gz", parse_dates=["date"])
    return d[d.name == nome].set_index("date").value.sort_index()

pt = serie("cmb_ptax", "ptax_venda")
cds = serie("cmb_risco_pais", "cds_5y_usd")
em = serie("cmb_dollar_index_em", "dxy_em")

def ols(y, X):
    X = np.column_stack([np.ones(len(y))] + list(X))
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    s2 = e @ e / (len(y) - X.shape[1])
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    return b, se

# diário
d = pd.concat([pt.rename("pt"), cds.rename("cds"), em.rename("em")], axis=1).dropna()
d["dpt"] = np.log(d.pt).diff() * 100
d["dcds"] = d.cds.diff()
d["dem"] = np.log(d.em).diff() * 100
d["nivel"] = d.cds.shift(1)
d = d.dropna()
print("DIÁRIO (2006-2026): % de PTAX por 10 p.b. de CDS, controlando dxy_em")
for nome, m in [("todos", d.nivel > 0), ("CDS < 200", d.nivel < 200), ("CDS 200-400", (d.nivel >= 200) & (d.nivel < 400)),
                ("CDS >= 400", d.nivel >= 400), ("desde 2016", d.index >= "2016-01-01")]:
    s = d[m]
    b, se = ols(s.dpt.values, [s.dcds.values, s.dem.values])
    b2, se2 = ols(s.dpt.values, [s.dcds.values])
    print(f"  {nome:12s} N={len(s):5d}  com EM: {10*b[1]:.3f} (ep {10*se[1]:.3f})  sem EM: {10*b2[1]:.3f}  "
          f"nível médio {s.nivel.mean():.0f}  em log: {b[1]*s.nivel.mean():.3f} % por 1% de CDS")

# trimestral
q = pd.concat([pt.resample("QE").last().rename("pt"), cds.resample("QE").last().rename("cds"),
               em.resample("QE").last().rename("em")], axis=1)
q["dpt"] = np.log(q.pt).diff() * 100
q["dcds"] = q.cds.diff()
q["dem"] = np.log(q.em).diff() * 100
q["nivel"] = q.cds.shift(1)
qq = q.dropna(subset=["dpt", "dcds", "nivel"])
print("\nTRIMESTRAL (fim de trimestre, sem EM: 2002-2026; com EM: 2006-2026): % de PTAX por 10 p.b.")
for nome, m in [("todos", qq.nivel > 0), ("CDS < 200", qq.nivel < 200), ("CDS >= 200", qq.nivel >= 200)]:
    s = qq[m]
    b2, se2 = ols(s.dpt.values, [s.dcds.values])
    se_ = s.dropna(subset=["dem"])
    b, se = ols(se_.dpt.values, [se_.dcds.values, se_.dem.values])
    print(f"  {nome:10s} N={len(s):3d}  sem EM: {10*b2[1]:.3f} (ep {10*se2[1]:.3f})   N={len(se_):3d} com EM: {10*b[1]:.3f} (ep {10*se[1]:.3f})")

print("\nPTAX em datas do ciclo:")
for dia in ["2026-09-30", "2026-10-02", "2026-10-05", "2026-10-22", "2026-10-23", "2026-10-26"]:
    print(" ", dia, pt.loc[dia], " CDS", cds.get(pd.Timestamp(dia), np.nan))
p02, p05, p26, p30 = pt.loc["2026-10-02"], pt.loc["2026-10-05"], pt.loc["2026-10-26"], pt.loc["2026-09-30"]
print(f"05/10 contra 02/10: {100*(p05/p02-1):.2f}%   26/10 contra 02/10: {100*(p26/p02-1):.2f}%   02/10 contra 30/09: {100*(p02/p30-1):.2f}%")
print(f"CDS 02/10 -> 26/10: {cds.loc['2026-10-02']:.1f} -> {cds.loc['2026-10-26']:.1f}")
