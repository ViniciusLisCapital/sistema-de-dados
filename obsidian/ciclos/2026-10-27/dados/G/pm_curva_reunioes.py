"""Selic implícita na curva DI por reunião do Copom, em várias datas de pregão, e o salto de
22-23/10 para 26/10 (ciclo 2026-10-27). Lê só A/.

Método: DI × pré de `br_di_grade` (taxa base 252 por vértice, com dc e du); fator de desconto
interpolado com log linear em du (flat forward); a taxa a termo entre a vigência de uma decisão
(dia seguinte à reunião) e a da seguinte, mais 0,10 p.p. (o CDI fica 0,10 abaixo da meta Selic:
o vértice de 1 dia útil de 26/10 é 13,65 com a meta em 13,75)."""
import numpy as np
import pandas as pd
from pathlib import Path

A = Path(__file__).resolve().parent.parent / "A"
g = pd.read_csv(A / "br_di_grade.csv.gz")
cal = pd.read_csv(A / "pm_copom_calendario.csv.gz")

def implicita(pregao: str):
    x = g[g.date == pregao].sort_values("dc")
    d0 = pd.Timestamp(pregao)
    dc, du, r = x.dc.values, x.du.values, x.value.values / 100
    lnP = -du / 252 * np.log1p(r)
    def lnP_at(c):
        u = np.interp(c, np.r_[0, dc], np.r_[0, du])
        return u, np.interp(u, np.r_[0, du], np.r_[0, lnP])
    reun = [pd.Timestamp(s) for s in cal.date if pd.Timestamp(s) > d0]
    out = []
    for i, m in enumerate(reun):
        a = (m - d0).days + 1
        b = ((reun[i + 1] - d0).days + 1) if i + 1 < len(reun) else a + 42
        if b > dc.max():
            break
        ua, la = lnP_at(a); ub, lb = lnP_at(b)
        f = np.expm1((la - lb) / (ub - ua) * 252) * 100 + 0.10
        out.append((m.date().isoformat(), round(f, 2)))
    return dict(out)

datas = ["2026-09-25", "2026-10-21", "2026-10-22", "2026-10-23", "2026-10-26"]
tab = pd.DataFrame({d: implicita(d) for d in datas})
tab["salto 23->26 (pb)"] = ((tab["2026-10-26"] - tab["2026-10-23"]) * 100).round(0)
tab["salto 22->26 (pb)"] = ((tab["2026-10-26"] - tab["2026-10-22"]) * 100).round(0)
print("Selic implícita por reunião (% a.a.)")
print(tab.to_string())

# Pregão a pregão: PTAX, CDS, DI e NTN-B nos prazos redondos, inflação implícita
bi = pd.read_csv(A / "br_interest_rate.csv.gz")
px = pd.read_csv(A / "cmb_ptax.csv.gz"); px = px[px.name == "ptax_venda"].set_index("date").value
cds = pd.read_csv(A / "cmb_risco_pais.csv.gz"); cds = cds[cds.name == "cds_5y_usd"].set_index("date").value
em = pd.read_csv(A / "cmb_dollar_index_em.csv.gz").set_index("date").value
fx = pd.read_csv(A / "cmb_fx_latam.csv.gz"); mx = fx[fx.country_code == "MX"].set_index("date").value
pv = bi[bi.curve.isin(["DIPRE", "NTNBJS"])].pivot_table(index="date", columns=["curve", "tenor"], values="value")
cols = {("DIPRE", t): f"DI {t}" for t in ["12M", "24M", "60M", "120M"]}
cols.update({("NTNBJS", t): f"NTNB {t}" for t in ["12M", "24M", "60M", "120M"]})
d = pv[list(cols)].copy(); d.columns = list(cols.values())
for t in ["12M", "24M", "60M", "120M"]:
    d[f"impl {t}"] = ((1 + d[f"DI {t}"] / 100) / (1 + d[f"NTNB {t}"] / 100) - 1) * 100
d["PTAX"] = px; d["CDS"] = cds; d["DXY EM"] = em; d["MXN"] = mx
d = d[d.index >= "2026-10-01"]
pd.set_option("display.width", 250)
print("\nPregão a pregão desde 01/10")
print(d.round(3).to_string())
print("\nVariação 23/10 -> 26/10")
print((d.loc["2026-10-26"] - d.loc["2026-10-23"]).round(3).to_string())
print("PTAX % 23->26:", round((px["2026-10-26"] / px["2026-10-23"] - 1) * 100, 2),
      " % 22->26:", round((px["2026-10-26"] / px["2026-10-22"] - 1) * 100, 2))
print("PTAX últimos 30:", px.tail(30).round(4).to_dict())
