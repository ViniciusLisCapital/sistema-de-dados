"""G do fiscal, ciclo 2026-10-02: o preço do risco.

1. CDS 5 anos: trajetória diária recente (jul-out/2026), mínimo e máximo das janelas.
2. Distribuição histórica da variação do CDS de fechamento de trimestre, em 1 a 6 trimestres
   (janelas: desde 2010 e últimos 10 anos), para as faixas da tese.
3. Quanto da variação mensal do CDS acompanha o global: regressão de ΔCDS mensal (fim de mês)
   em Δ dólar contra emergentes (%) e Δ Treasury 10 anos (p.p.), 2010-2026; e o último mês
   decomposto com os pesos estimados.
4. NTN-B 10 anos: trajetória diária recente, e distribuição da variação da média trimestral
   (rr_10a) em 1 a 6 trimestres.
5. O real contra os pares no último mês e nos últimos 3 meses (fim de período).
"""
import numpy as np
import pandas as pd

A = "obsidian/ciclos/2026-10-02/dados/A/"
CORTE = pd.Timestamp("2026-10-02")


def serie(arq, filtro=None):
    d = pd.read_csv(A + arq, parse_dates=["date"])
    if filtro:
        for k, v in filtro.items():
            d = d[d[k] == v]
    return d.set_index("date")["value"].sort_index()


cds = serie("cmb_risco_pais.csv.gz", {"name": "cds_5y_usd"})
cds = cds[cds.index <= CORTE]
ntnb = serie("br_interest_rate.csv.gz", {"curve": "NTNBJS", "tenor": "120M"})
ntnb = ntnb[ntnb.index <= CORTE]
dxy = serie("cmb_dollar_index_em.csv.gz", {"name": "dxy_em"})
ust = serie("us_interest_rate.csv.gz", {"curve": "US_TREASURY", "tenor": "10Y"})
ptax = serie("cmb_ptax.csv.gz", {"name": "ptax_venda"})
lat = pd.read_csv(A + "cmb_fx_latam.csv.gz", parse_dates=["date"]).pivot(
    index="date", columns="country_code", values="value").sort_index()

print("## 1. CDS diário, desde 2026-06-01")
rec = cds[cds.index >= "2026-06-01"]
print(rec.resample("W-FRI").last().round(1).to_string())
for ini in ["2026-07-01", "2026-09-01"]:
    s = cds[cds.index >= ini]
    print(f"desde {ini}: mín {s.min():.1f} ({s.idxmin().date()}), máx {s.max():.1f} ({s.idxmax().date()})")
s = cds[cds.index >= "2016-10-01"]
print(f"10 anos: mín {s.min():.1f} ({s.idxmin().date()}), máx {s.max():.1f} ({s.idxmax().date()})")
s = cds[cds.index >= "2024-01-01"]
print(f"desde 2024: mín {s.min():.1f} ({s.idxmin().date()}), máx {s.max():.1f} ({s.idxmax().date()})")

print("\n## 2. Variação do CDS de fechamento de trimestre (p.b.) em h trimestres")
cq = cds.resample("QE").last()
cq = cq[cq.index <= "2026-09-30"]
for ini in ["2010-01-01", "2016-10-01"]:
    q = cq[cq.index >= ini]
    print(f"janela desde {ini} ({len(q)} trimestres)")
    for h in range(1, 7):
        d = (q - q.shift(h)).dropna()
        pr = (q / q.shift(h) - 1).dropna() * 100
        print(f"  h={h}: n={len(d)} p.b. p10 {d.quantile(.1):+.0f} p25 {d.quantile(.25):+.0f} "
              f"p50 {d.quantile(.5):+.0f} p75 {d.quantile(.75):+.0f} p90 {d.quantile(.9):+.0f} | "
              f"% p10 {pr.quantile(.1):+.0f} p25 {pr.quantile(.25):+.0f} p75 {pr.quantile(.75):+.0f} p90 {pr.quantile(.9):+.0f}")
print("CDS de fechamento de trimestre abaixo de 120 p.b. desde 2010:",
      [f"{i.year}T{i.quarter} {v:.0f}" for i, v in cq[(cq.index >= '2010-01-01') & (cq < 120)].items()])

print("\n## 3. ΔCDS mensal contra o global (fim de mês, 2010-01 a 2026-09)")
m = pd.DataFrame({
    "cds": cds.resample("ME").last(),
    "dxy": dxy.resample("ME").last(),
    "ust": ust.resample("ME").last(),
}).dropna()
m = m[(m.index >= "2009-12-31") & (m.index <= "2026-09-30")]
dm = pd.DataFrame({
    "dcds": m["cds"].diff(),
    "ddxy": m["dxy"].pct_change() * 100,
    "dust": m["ust"].diff(),
}).dropna()
X = np.column_stack([np.ones(len(dm)), dm["ddxy"], dm["dust"]])
b, *_ = np.linalg.lstsq(X, dm["dcds"].values, rcond=None)
res = dm["dcds"].values - X @ b
r2 = 1 - res.var() / dm["dcds"].var()
print(f"n={len(dm)}; ΔCDS = {b[0]:+.2f} + {b[1]:+.2f}·Δ%dxy_em + {b[2]:+.2f}·ΔUST10 ; R² {r2:.2f}")
print(f"correlação ΔCDS com Δ%dxy_em: {dm['dcds'].corr(dm['ddxy']):.2f}; com ΔUST10: {dm['dcds'].corr(dm['dust']):.2f}")
# o mesmo desde 2016-10
dm2 = dm[dm.index >= "2016-10-31"]
X2 = np.column_stack([np.ones(len(dm2)), dm2["ddxy"], dm2["dust"]])
b2, *_ = np.linalg.lstsq(X2, dm2["dcds"].values, rcond=None)
res2 = dm2["dcds"].values - X2 @ b2
print(f"desde 2016-10, n={len(dm2)}: ΔCDS = {b2[0]:+.2f} + {b2[1]:+.2f}·Δ%dxy_em + {b2[2]:+.2f}·ΔUST10 ; "
      f"R² {1 - res2.var() / dm2['dcds'].var():.2f}")


def janela(ini, fim):
    c0, c1 = cds[:ini].iloc[-1], cds[:fim].iloc[-1]
    x0, x1 = dxy[:ini].iloc[-1], dxy[:fim].iloc[-1]
    u0, u1 = ust[:ini].iloc[-1], ust[:fim].iloc[-1]
    dd, du = (x1 / x0 - 1) * 100, u1 - u0
    glob = b2[1] * dd + b2[2] * du
    print(f"{ini} → {fim}: ΔCDS {c1 - c0:+.1f} p.b. ({c0:.1f} → {c1:.1f}); Δ%dxy_em {dd:+.2f}; ΔUST10 {du:+.2f}; "
          f"parte global (pesos desde 2016) {glob:+.1f}; resto {c1 - c0 - glob - b2[0]:+.1f}")


janela("2026-09-02", "2026-10-02")
janela("2026-07-02", "2026-10-02")
janela("2026-06-30", "2026-09-30")
janela("2025-10-02", "2026-10-02")

print("\n## 4. NTN-B 10 anos")
rn = ntnb[ntnb.index >= "2026-06-01"]
print(rn.resample("W-FRI").last().round(2).to_string())
s = ntnb[ntnb.index >= "2026-07-01"]
print(f"desde 2026-07-01: mín {s.min():.2f} ({s.idxmin().date()}), máx {s.max():.2f} ({s.idxmax().date()})")
s = ntnb[ntnb.index >= "2016-10-01"]
print(f"10 anos: mín {s.min():.2f} ({s.idxmin().date()}), máx {s.max():.2f} ({s.idxmax().date()})")
nq = ntnb.resample("QE").mean()
nq = nq[(nq.index <= "2026-09-30")]
for ini in ["2010-01-01", "2016-10-01"]:
    q = nq[nq.index >= ini]
    print(f"média trimestral, janela desde {ini} ({len(q)} trimestres)")
    for h in range(1, 7):
        d = (q - q.shift(h)).dropna()
        print(f"  h={h}: p10 {d.quantile(.1):+.2f} p25 {d.quantile(.25):+.2f} p50 {d.quantile(.5):+.2f} "
              f"p75 {d.quantile(.75):+.2f} p90 {d.quantile(.9):+.2f}")
# correlação das variações trimestrais de CDS (fechamento) e rr_10a (média) desde 2010
j = pd.DataFrame({"cds": cq, "rr": nq}).dropna()
j = j[j.index >= "2010-01-01"]
print(f"corr Δ trimestral CDS × Δ rr_10a (2010-2026): {j['cds'].diff().corr(j['rr'].diff()):.2f}")
jj = j[j.index >= "2016-10-01"]
print(f"corr desde 2016-10: {jj['cds'].diff().corr(jj['rr'].diff()):.2f}")
dd = j.diff().dropna()
bb = np.polyfit(dd["cds"], dd["rr"], 1)
print(f"Δrr_10a = {bb[1]:+.3f} + {bb[0]:+.4f}·ΔCDS (p.p. por p.b.), 2010-2026")
dd2 = jj.diff().dropna()
bb2 = np.polyfit(dd2["cds"], dd2["rr"], 1)
print(f"Δrr_10a = {bb2[1]:+.3f} + {bb2[0]:+.4f}·ΔCDS, desde 2016-10")

print("\n## 5. O real contra os pares (moeda por US$, fim de período, %)")
for ini in ["2026-09-02", "2026-07-02"]:
    linha = {"BRL": (ptax[:"2026-10-02"].iloc[-1] / ptax[:ini].iloc[-1] - 1) * 100}
    for c in lat.columns:
        s = lat[c].dropna()
        linha[c] = (s[:"2026-10-02"].iloc[-1] / s[:ini].iloc[-1] - 1) * 100
    print(ini, "→ 2026-10-02:", {k: round(v, 1) for k, v in linha.items()},
          "média dos pares", round(np.mean([linha[c] for c in lat.columns]), 1))
