"""G r1b: sazonalidade de dezembro — fluxo financeiro contratado em dezembro x média dos outros meses
(2016-2025), e variação da PTAX em dezembro (último dia útil de nov -> último de dez)."""
from pathlib import Path
import pandas as pd

A = Path(__file__).resolve().parents[1] / "A"
c = pd.read_csv(A / "cmb_cambio_contratado.csv.gz", parse_dates=["date"])
f = c[c.name == "cc_fin_saldo"].set_index("date")["value"]
t = c[c.name == "cc_saldo_total"].set_index("date")["value"]
fm = f.resample("ME").sum() / 1000
tm = t.resample("ME").sum() / 1000
p = pd.read_csv(A / "cmb_ptax.csv.gz", parse_dates=["date"])
p = p[p.name == "ptax_venda"].set_index("date")["value"].resample("ME").last()
rows = []
for y in range(2016, 2026):
    dez = pd.Timestamp(f"{y}-12-31")
    outros = fm[str(y)].drop(dez, errors="ignore")
    rows.append({"ano": y, "fin_dez": fm.get(dez), "fin_outros_med": outros.mean(), "total_dez": tm.get(dez),
                 "ptax_dez_%": 100 * (p[dez] / p[pd.Timestamp(f'{y}-11-30')] - 1)})
d = pd.DataFrame(rows)
print(d.round(2).to_string(index=False))
print("médias:", d.drop(columns="ano").mean().round(2).to_dict())
print("anos com PTAX subindo em dez:", int((d["ptax_dez_%"] > 0).sum()), "de", len(d))
