"""G do câmbio, ciclo 2026-10-02: a sazonalidade do fluxo cambial contratado no 4º trimestre.

Saldo financeiro e saldo total por mês (soma dos dias), e a média de out, nov e dez nos 10 anos
completos 2016-2025, contra a média dos outros meses. Também a intervenção do BC (à vista e
linhas) em dezembro de cada ano. Lê só ../A/."""
from pathlib import Path
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"
c = pd.read_csv(A / "cmb_cambio_contratado.csv.gz")
c["date"] = pd.to_datetime(c["date"])
m = c[c["name"].isin(["cc_fin_saldo", "cc_saldo_total", "cc_saldo_comercial"])]
m = m.pivot_table(index=m["date"].dt.to_period("M"), columns="name", values="value", aggfunc="sum") / 1000  # US$ bi
m = m[(m.index >= pd.Period("2016-01")) & (m.index <= pd.Period("2025-12"))]
mes = m.index.month
print("Média por mês, 2016-2025 (US$ bi):")
print(m.groupby(mes).mean().round(2).to_string())
q4 = m[mes >= 10].groupby(m[mes >= 10].index.year).sum()
print("\nSoma out-dez por ano (US$ bi):")
print(q4.round(1).to_string())
print("\nMédia da soma out-dez:", q4.mean().round(1).to_dict())
dez = m[mes == 12]
print("Dezembro, saldo financeiro: média", round(dez["cc_fin_saldo"].mean(), 1), "· mín", round(dez["cc_fin_saldo"].min(), 1), "· máx", round(dez["cc_fin_saldo"].max(), 1))

r = pd.read_csv(A / "cmb_reservas_bc.csv.gz")
r["date"] = pd.to_datetime(r["date"])
iv = r[r["name"].isin(["bcb_intervention_spot", "bcb_intervention_repo_lines"])]
iv = iv[iv["date"].dt.month == 12]
print("\nIntervenção do BC em dezembro (US$ bi; − = venda):")
print((iv.pivot_table(index=iv["date"].dt.year, columns="name", values="value", aggfunc="sum") / 1000).loc[2016:].round(1).to_string())

# a PTAX no 4º trimestre: variação (%) do fechamento de set ao de dez, contra os outros trimestres
p = pd.read_csv(A / "cmb_ptax.csv.gz")
p = p[p["name"] == "ptax_venda"]
p = p.set_index(pd.to_datetime(p["date"]))["value"].astype(float)
pq = p.resample("QE").last()
vq = 100 * pq.pct_change()
vq = vq[(vq.index.year >= 2006) & (vq.index.year <= 2025)]
g = vq.groupby(vq.index.quarter)
print("\nPTAX, variação no trimestre (%), 2006-2025: média, mediana, n de altas")
print(pd.DataFrame({"media": g.mean(), "mediana": g.median(), "altas": g.apply(lambda x: (x > 0).sum()), "n": g.size()}).round(2).to_string())
