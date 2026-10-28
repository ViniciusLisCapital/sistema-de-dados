"""G externo, rodada 2 (pedido da inflação: o Brent alto entra no caminho do agro?): regressão mensal do
Δlog do IC-Br agropecuária em dólar no Δlog do Brent (média do mês), corrente e defasado de 1 a 6 meses,
com e sem o Δlog do dólar EM, 2010-2026 e 2016-2026; e a soma dos coeficientes. Lê só ../A/."""
import numpy as np, pandas as pd
from pathlib import Path
A = Path(__file__).resolve().parent.parent / "A"
ic = pd.read_csv(A/"comm_icbr_usd.csv.gz", parse_dates=["date"]).pivot(index="date", columns="name", values="value")
br = pd.read_csv(A/"comm_brent.csv.gz", parse_dates=["date"]).set_index("date")["value"].resample("MS").mean()
em = pd.read_csv(A/"cmb_dollar_index_em.csv.gz", parse_dates=["date"]).set_index("date")["value"].resample("MS").mean()
d = pd.DataFrame({"agr": ic["icbr_agropecuaria_usd"], "br": br, "em": em}).dropna()
r = 100*np.log(d).diff()
L = 6
for k in range(L+1): r[f"br{k}"] = r.br.shift(k)
r = r.dropna()
def reg(x, cols, nome):
    X = np.c_[np.ones(len(x)), x[cols].values]; b, *_ = np.linalg.lstsq(X, x.agr.values, rcond=None)
    e = x.agr.values - X@b; V = (e**2).sum()/(len(x)-X.shape[1])*np.linalg.inv(X.T@X); se = np.sqrt(np.diag(V))
    ib = [cols.index(f"br{k}")+1 for k in range(L+1)]; soma = b[ib].sum(); se_soma = np.sqrt(V[np.ix_(ib, ib)].sum())
    r2 = 1 - (e**2).sum()/((x.agr-x.agr.mean())**2).sum()
    print(f"{nome} (n={len(x)}): Brent corrente {b[1]:.3f} (t {b[1]/se[1]:.1f}); soma de 0 a {L} meses {soma:.3f} (t {soma/se_soma:.1f}); R² {r2:.2f}"
          + (f"; dólar EM {b[-1]:.3f} (t {b[-1]/se[-1]:.1f})" if "em" in cols else ""))
    return soma
for ini in ["2010-01-01", "2016-01-01"]:
    x = r.loc[ini:]
    reg(x, [f"br{k}" for k in range(L+1)], f"Δlog agro em Δlog Brent 0..{L}, {ini[:4]}-2026")
    s = reg(x, [f"br{k}" for k in range(L+1)] + ["em"], f"  + dólar EM, {ini[:4]}-2026")
# o que a soma 2016-2026 daria para o Brent do base (set/26 114,2 -> 1T28 ~91) e da alta
br_set = br.loc["2026-09-01"]
for nome, b1 in [("base, Brent 1T28 ~91", 91.0), ("alta, Brent 4T26-1T27 ~130", 130.0), ("queda, Brent 78", 78.0)]:
    print(f"efeito no agro, {nome}: {s*100*np.log(b1/br_set):+.1f}% (soma 2016-2026 com dólar EM)")
