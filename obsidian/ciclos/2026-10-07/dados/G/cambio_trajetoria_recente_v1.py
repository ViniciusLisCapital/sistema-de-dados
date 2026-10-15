"""G · câmbio · ciclo 2026-10-07 · trajetória recente, semana a semana.

Lê só ../A/. Imprime, para sextas-feiras (último dado disponível até a data) desde jun/2026:
PTAX, pares LatAm, DXY, dólar contra emergentes, DI 1 ano e 5 anos (interpolado em du),
CDS 5 anos, Brent, Treasury 10 anos. Também: intervenções diárias do BC em set-out/2026,
reservas diárias, fluxo cambial contratado semanal e COT semanal do BRL.
"""
from pathlib import Path

import numpy as np
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"
INI = "2026-06-01"


def rd(nome):
    return pd.read_csv(A / f"{nome}.csv.gz", parse_dates=["date"])


def serie(df, col, val, filtro=None):
    if filtro is not None:
        df = df[df[col] == filtro]
    return df.set_index("date")["value"].sort_index()


ptax = rd("cmb_ptax")
s = {"PTAX": serie(ptax, "name", "value", "ptax_venda")}
lat = rd("cmb_fx_latam")
for c in ["MX", "CL", "CO", "PE"]:
    s[c] = serie(lat, "country_code", "value", c)
s["DXY"] = serie(rd("cmb_dollar_index"), "name", "value", "dxy")
s["DXY_EM"] = serie(rd("cmb_dollar_index_em"), "name", "value", "dxy_em")
s["CDS"] = serie(rd("cmb_risco_pais"), "name", "value", "cds_5y_usd")
s["Brent"] = serie(rd("comm_brent"), "name", "value", "brent_usd")
ust = rd("us_interest_rate")
s["UST10"] = ust[ust.tenor == "10Y"].set_index("date")["value"].sort_index()
s["UST2"] = ust[ust.tenor == "2Y"].set_index("date")["value"].sort_index()

di = rd("br_di_grade")
di = di[di.date >= "2026-05-01"]


def di_du(g, alvo):
    g = g.sort_values("du")
    return float(np.interp(alvo, g["du"], g["value"]))


di1 = di.groupby("date").apply(lambda g: di_du(g, 252))
di5 = di.groupby("date").apply(lambda g: di_du(g, 1260))
s["DI1a"] = di1
s["DI5a"] = di5

df = pd.DataFrame(s)
df = df[df.index >= INI].ffill()
sem = df.resample("W-FRI").last()
pd.set_option("display.width", 250)
print("== Semanal (sexta, último dado até a data; pares e CDS com defasagem própria)")
print(sem.round(4).to_string())

print("\n== Diário desde 2026-09-15")
print(df[df.index >= "2026-09-15"].round(4).to_string())

# Variações em janelas fixas
def var(nome, d0, d1):
    x = df[nome]
    a = x[x.index <= d0].iloc[-1]
    b = x[x.index <= d1].iloc[-1]
    return a, b, 100 * (b / a - 1)

print("\n== Variação % de 2026-08-29 a último disponível (PTAX 06/10)")
for n in ["PTAX", "MX", "CL", "CO", "PE", "DXY", "DXY_EM", "Brent"]:
    a, b, v = var(n, "2026-08-29", "2026-10-07")
    print(f"{n:7s} {a:10.4f} -> {b:10.4f}  {v:+.2f}%")
print("\n== Variação % de 2026-08-29 a 2026-09-29 (janela comum com os pares)")
for n in ["PTAX", "MX", "CL", "CO", "PE", "DXY", "DXY_EM"]:
    a, b, v = var(n, "2026-08-29", "2026-09-29")
    print(f"{n:7s} {a:10.4f} -> {b:10.4f}  {v:+.2f}%")
print("\n== Variação % de 2026-09-29 a 2026-10-06")
for n in ["PTAX", "DXY", "DXY_EM"]:
    a, b, v = var(n, "2026-09-29", "2026-10-06")
    print(f"{n:7s} {a:10.4f} -> {b:10.4f}  {v:+.2f}%")

res = rd("cmb_reservas_bc")
res = res[res.date >= "2026-08-15"]
iv = res[res.name.isin(["bcb_intervention_spot", "bcb_intervention_repo_lines"])]
print("\n== Intervenções (linhas não nulas) desde 2026-08-15, US$ mi")
print(iv[iv.value != 0].sort_values("date").to_string())
rt = res[res.name == "reserves_total_daily"].set_index("date")["value"]
print("\n== Reservas totais diárias (US$ mi), semanal")
print(rt.resample("W-FRI").last().to_string())

cc = rd("cmb_cambio_contratado")
cc = cc[(cc.date >= "2026-07-01") & cc.name.isin(["cc_saldo_comercial", "cc_fin_saldo", "cc_saldo_total"])]
cc = cc.pivot_table(index="date", columns="name", values="value")
print("\n== Fluxo cambial contratado (US$ mi), observações desde jul/2026")
print(cc.round(0).to_string())

cot = rd("cmb_cot_fx")
cot = cot[(cot.currency == "BRL") & (cot.date >= "2026-06-01") & cot.name.isin(["lev_net", "asset_mgr_net", "open_interest"])]
print("\n== COT BRL")
print(cot.pivot_table(index="date", columns="name", values="value").to_string())
