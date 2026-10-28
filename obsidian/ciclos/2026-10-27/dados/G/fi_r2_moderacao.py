"""fi (rodada 2, moderação): (a) sensibilidade trimestral da PTAX ao CDS em nível (p.b.) e em log, na amostra
inteira e com o CDS abaixo de 200 no início do trimestre — testa o × 1,2 no base; (b) o base revisto no Modelo
Estrutural (exógenas do P1 nas outras chaves)."""
import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from analytics.agent_system import modelo
sys.stdout.reconfigure(encoding="utf-8")
A = Path(__file__).resolve().parent.parent / "A"
pt = pd.read_csv(A / "cmb_ptax.csv.gz", parse_dates=["date"])
pt = pt[pt.name == "ptax_venda"].set_index("date").value.sort_index()
cds = pd.read_csv(A / "cmb_risco_pais.csv.gz", parse_dates=["date"]).set_index("date").sort_index().iloc[:, -1]
q = pd.DataFrame({"ptax": pt.resample("QE").last(), "cds": cds.resample("QE").last()}).dropna()
q = q[(q.index >= "2006-01-01") & (q.index <= "2026-09-30")]
d = pd.DataFrame({"dptax": 100 * np.log(q.ptax).diff(), "dcds": q.cds.diff(), "dlcds": 100 * np.log(q.cds).diff(),
                  "cds0": q.cds.shift(1)}).dropna()

def ols(y, x):
    X = np.column_stack([np.ones(len(x)), x]); b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b; s2 = e @ e / (len(y) - 2); se = np.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1])
    return b[1], b[1] / se, len(y)

for nome, m in [("amostra inteira", d.cds0 > 0), ("CDS < 200 no início", d.cds0 < 200), ("CDS >= 200 no início", d.cds0 >= 200),
                ("2016–2026", d.index >= "2016-01-01")]:
    s = d[m]
    b1, t1, n = ols(s.dptax.values, s.dcds.values)
    b2, t2, _ = ols(s.dptax.values, s.dlcds.values)
    print(f"{nome} (n={n}): ΔPTAX% por 10 p.b. = {10*b1:.2f} (t {t1:.1f}) · por 10% de CDS = {10*b2:.2f} (t {t2:.1f})"
          f" · 10% de CDS a 130 = {13:.0f} p.b. → {10*b2*1.0:.2f}% (log) contra {1.3*b1*10:.2f}% (nível)")

# (b) base revisto
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
P1 = json.loads((Path(__file__).resolve().parents[2] / "P1.json").read_text(encoding="utf-8"))
c = {k: dict(v) for k, v in P1["caminhos_usados"].items()}
TT = list(c["fiscal"].keys())
for k, vals in {"fiscal": [140, 142, 139, 135, 130, 125], "rr_10a": [7.72, 7.95, 7.90, 7.80, 7.75, 7.70]}.items():
    c[k] = dict(zip(TT, vals + [vals[-1]] * (len(TT) - len(vals))))
sim = modelo.carregar("2026-10-27")
print(modelo.texto(modelo.rodar(sim, caminhos=c), T))

# (c) diferenças citadas no report depois da moderação
f = lambda a, b: [round(x - y, 2) for x, y in zip(a, b)]
rr_new, rr_r2, rr_r1, rr_pm = [7.72, 7.95, 7.90, 7.80, 7.75, 7.70], [7.72, 8.00, 8.00, 7.95, 7.90, 7.85], [7.70, 7.80, 7.70, 7.60, 7.55, 7.50], [7.76, 8.05, 8.05, 8.05, 8.05, 8.05]
cds_new, cds_ex = [140, 142, 139, 135, 130, 125], [140, 140, 138, 132, 126, 120]
sel_new, sel_r1, sel_pmt = [13.43, 13.21, 12.87, 12.56, 12.32, 12.11], [13.34, 13.03, 12.67, 12.36, 12.12, 11.91], [13.49, 13.32, 13.04, 12.80, 12.58, 12.39]
print("rr novo − r1:", f(rr_new, rr_r1), "· PM(r1) − novo:", f(rr_pm, rr_new), "· 1T28 − 1T27:", round(rr_new[5] - rr_new[1], 2), "· 1T27 − 3T26:", round(rr_new[1] - 7.84, 2))
print("CDS novo − externo ref:", f(cds_new, cds_ex), "· variação trimestral:", f(cds_new, [131] + cds_new[:-1]))
print("Selic fim novo − r1:", f(sel_new, sel_r1), "· novo − tese PM:", f(sel_new, sel_pmt))
print("Selic média 1T27 novo base − downside:", round(13.37 - 12.72, 2), "· prêmio:", round(7.95 - 6.02, 2), round(7.95 - 6.28, 2))
print("PTAX: sensibilidade CDS<200 − amostra inteira, por 10 p.b.:", round(1.35 - 1.21, 2))
