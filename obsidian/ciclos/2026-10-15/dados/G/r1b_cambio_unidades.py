"""G r1b: confere a convenção (média x fim do trimestre) das exógenas do simulador contra as tabelas de A,
e mede o 4T26 até o corte nas mesmas unidades."""
from pathlib import Path
import pandas as pd
from analytics.agent_system import modelo

A = Path(__file__).resolve().parents[1] / "A"
sim = modelo.carregar("2026-10-15")
p = sim["p"]
rot = p["rot"]
for k in ["fiscal", "vol", "dxy_em", "sp500", "icbr_usd", "ffr", "infl_us"]:
    obs = p["var"][k]["obs"]
    print(k, [(str(r), None if v is None else round(v, 2)) for r, v in zip(rot[-6:], obs[-6:])])
print("ptax endo", [(str(r), None if v is None else round(v, 4)) for r, v in zip(rot[-6:], p["var"]["ptax"]["obs"][-6:])] if "ptax" in p["var"] else p["var"].keys())

def serie(tab, name, col="name"):
    d = pd.read_csv(A / f"{tab}.csv.gz", parse_dates=["date"])
    d = d[d[col] == name].set_index("date")["value"].sort_index()
    return d

ss = {
    "fiscal (cds)": serie("cmb_risco_pais", "cds_5y_usd"),
    "dxy_em": serie("cmb_dollar_index_em", "dxy_em"),
    "sp500": serie("cmb_equity_us", "sp500"),
    "ptax": serie("cmb_ptax", "ptax_venda"),
}
for nome, s in ss.items():
    for q0, q1 in [("2026-04-01", "2026-06-30"), ("2026-07-01", "2026-09-30"), ("2026-10-01", "2026-12-31")]:
        x = s[q0:q1]
        print(f"{nome} {q0[:7]}: média {x.mean():.2f} · fim {x.iloc[-1]:.2f} ({x.index[-1].date()}) · n {len(x)}")
