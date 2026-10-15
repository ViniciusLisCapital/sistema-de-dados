"""Global x idiossincratico no movimento recente do real (G do ciclo 2026-10-07).
Le so ../A/. (1) variacao de PTAX, pares, DXY e dolar contra emergentes em janelas fixas;
(2) beta diario do real ao dolar contra emergentes e ao DXY, estimado em 01/07/2024-30/06/2026,
e o residuo (parte idiossincratica) acumulado em cada janela."""
from pathlib import Path
import numpy as np
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"
rd = lambda t: pd.read_csv(A / f"{t}.csv.gz", parse_dates=["date"])
ptax = rd("cmb_ptax").query("name=='ptax_venda'").set_index("date")["value"].rename("BRL")
dxy = rd("cmb_dollar_index").set_index("date")["value"].rename("DXY")
em = rd("cmb_dollar_index_em").set_index("date")["value"].rename("EM")
fx = rd("cmb_fx_latam").pivot(index="date", columns="country_code", values="value")
fx.columns = [{"MX": "MXN", "CL": "CLP", "CO": "COP", "PE": "PEN"}[c] for c in fx.columns]
lv = pd.concat([ptax, dxy, em, fx], axis=1)

def at(s, d):
    s = s.dropna(); s = s[s.index <= d]
    return s.index[-1], s.iloc[-1]

wins = {"3T26 (30/06-30/09)": ("2026-06-30", "2026-09-30"),
        "set (31/08-30/09)": ("2026-08-31", "2026-09-30"),
        "31/08-02/10 (antes do 1o turno)": ("2026-08-31", "2026-10-02"),
        "02/10-06/10 (sessoes pos 1o turno)": ("2026-10-02", "2026-10-06"),
        "30/06-06/10 (3 meses)": ("2026-06-30", "2026-10-06")}
print("Variacao % (moeda local por dolar; + = moeda se desvaloriza). Data efetiva final entre parenteses.")
for k, (a, b) in wins.items():
    row = []
    for c in lv.columns:
        da, va = at(lv[c], a); db, vb = at(lv[c], b)
        row.append(f"{c} {100*(vb/va-1):+.2f} ({db.date()})")
    print(k, "|", " ; ".join(row))

for g in ["EM", "DXY"]:
    # alinha os niveis nas datas em que as duas series existem, depois tira o log-retorno
    j = lv[["BRL", g]].dropna()
    r = np.log(j).diff().dropna()
    d = r["2024-07-01":"2026-06-30"]
    X = np.c_[np.ones(len(d)), d[g]]
    b = np.linalg.lstsq(X, d["BRL"], rcond=None)[0]
    res = d["BRL"] - X @ b
    r2 = 1 - res.var() / d["BRL"].var()
    print()
    print(f"Beta do real a {g} (01/07/2024-30/06/2026, n={len(d)}): beta={b[1]:.2f}, R2={r2:.2f}")
    for k, (a, bb) in wins.items():
        w = r[(r.index > a) & (r.index <= bb)]
        tot = w["BRL"].sum(); glob = b[1] * w[g].sum()
        print(f"  {k}: real {100*tot:+.2f} = global {100*glob:+.2f} + idiossincratico {100*(tot-glob):+.2f} (log %, {len(w)} sessoes, ate {w.index.max().date() if len(w) else '-'})")
