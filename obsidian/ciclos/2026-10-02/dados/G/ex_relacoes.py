"""G do externo, ciclo 2026-10-02: as regularidades que os cenários usam, medidas no A.

1. Prêmio dos T-bills sobre o Fed funds efetivo quando a meta não muda no prazo do bill.
2. Fed funds efetivo menos o ponto médio da meta (para ler o efetivo depois de 17/09).
3. CPI cheio mensal contra núcleo e Brent (para o infl_us dos cenários).
4. IC-Br total contra os grupos (os pesos implícitos) e o grupo energia contra o Brent.
5. Dólar EM contra commodities, e dólar EM contra S&P, em janelas.
6. O episódio de março de 2026 (Brent, S&P, dólar EM).
7. CPI 12m (por data) até ago e set.
Lê só ../A/. Janelas até ago/2026 quando o dado de set não existia em 02/10.
"""
from pathlib import Path
import numpy as np
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"

def rd(t):
    d = pd.read_csv(A / f"{t}.csv.gz")
    d["date"] = pd.to_datetime(d["date"])
    return d

def ols(y, X, const=True):
    X = np.column_stack([np.ones(len(X)), X]) if const else np.asarray(X)
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    s2 = e @ e / (len(y) - X.shape[1])
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    r2 = 1 - (e @ e) / ((y - y.mean()) @ (y - y.mean()))
    return b, se, r2, len(y)

# ---------- 1-2. Bills, meta e efetivo
c = rd("us_interest_rate__curva_completa")
pol = c[c.curve == "POLICY"].set_index("date")["value"].sort_index()
tr = c[c.curve == "US_TREASURY"].pivot_table(index="date", columns="tenor", values="value")
trm = tr.resample("MS").mean()
polm_end = pol.resample("MS").last()
ff = rd("diferenciais_juros__eua").query("name=='fed_funds'").set_index("date")["value"]

print("1. T-bill (média do mês) − Fed funds efetivo, em meses em que a meta no fim do prazo")
print("   é igual à do fim do mês (sem mudança no prazo do bill):")
for ten, k in [("1M", 1), ("3M", 3), ("6M", 6), ("1Y", 12)]:
    for ini in ["1990-01-01", "2010-01-01", "2017-01-01"]:
        df = pd.DataFrame({"bill": trm[ten], "ff": ff, "p0": polm_end, "pk": polm_end.shift(-k)}).dropna()
        df = df[df.index >= ini]
        # exclui o piso de zero (2009-2015, 2020-2021): o prêmio ali é outro objeto
        df = df[df.ff > 0.25]
        sem = df[(df.p0 - df.pk).abs() < 1e-9]
        sp = sem.bill - sem.ff
        print(f"   {ten} desde {ini[:4]}: média {sp.mean():+.2f} p.p., mediana {sp.median():+.2f}, "
              f"p10 {sp.quantile(.1):+.2f}, p90 {sp.quantile(.9):+.2f}, n={len(sp)}")

mid_m = pol.resample("MS").mean()
dif = (ff - mid_m).dropna()
print("\n2. Efetivo − ponto médio (média do mês), meses sem mudança da meta em 2026:")
print(dif["2026-01-01":"2026-08-01"].round(3).to_dict())
pre = 3.63; dias_pre = 17; dias = 30
print("   Efetivo implícito depois de 17/09 se a média de set é 3,75 (17 dias a 3,63):",
      round((3.75 * dias - pre * dias_pre) / (dias - dias_pre), 3),
      "| com média 3,745:", round((3.745 * dias - pre * dias_pre) / (dias - dias_pre), 3))
print("   Ponto médio + o desvio médio de 2026:", round(3.875 + dif["2026-01-01":"2026-08-01"].mean(), 3))

# ---------- 3. CPI cheio contra núcleo e Brent
cpi = rd("inflc_cpi").pivot_table(index="date", columns="item_code", values="value").asfreq("MS")
br = rd("comm_brent").set_index("date")["value"]
brm = br.resample("MS").mean()
m = pd.DataFrame({
    "cheio": 100 * np.log(cpi["SA0"]).diff(),
    "nucleo": 100 * np.log(cpi["SA0L1E"]).diff(),
    "energia": 100 * np.log(cpi["SA0E"]).diff(),
    "br0": 100 * np.log(brm).diff(),
})
m["br1"] = m["br0"].shift(1)
for ini in ["2000-01-01", "2015-01-01"]:
    d = m.loc[ini:"2026-08-01"].dropna()
    b, se, r2, n = ols(d.cheio.values, d[["nucleo", "br0", "br1"]].values)
    print(f"\n3. CPI cheio mensal = a + b·núcleo + c0·ΔlogBrent + c1·ΔlogBrent(-1), {ini[:4]}–ago/26:")
    print("   coef", np.round(b, 4), "ep", np.round(se, 4), f"R2 {r2:.2f} n {n}")
    b2, se2, r22, _ = ols(d.energia.values, d[["br0", "br1"]].values)
    print("   energia CPI = a + c0·ΔlogBrent + c1·(-1):", np.round(b2, 4), "ep", np.round(se2, 4), f"R2 {r22:.2f}")
d = m.loc["2015-01-01":"2026-08-01"].dropna()
B_CPI, *_ = ols(d.cheio.values, d[["nucleo", "br0", "br1"]].values)

# ---------- 4. IC-Br: pesos implícitos e energia contra Brent
ic = rd("comm_icbr_usd").pivot_table(index="date", columns="name", values="value").asfreq("MS")
dl = 100 * np.log(ic).diff()
for ini in ["2010-01-01", "2018-01-01"]:
    d = dl.loc[ini:"2026-08-01"].dropna()
    X = d[["icbr_agropecuaria_usd", "icbr_metal_usd", "icbr_energia_usd"]].values
    b, se, r2, n = ols(d.icbr_usd.values, X, const=False)
    print(f"\n4a. ΔlogIC-Br = w_agr·Δagr + w_met·Δmet + w_ene·Δene (sem constante), {ini[:4]}–ago/26:")
    print("   w", np.round(b, 3), "ep", np.round(se, 3), f"soma {b.sum():.3f} R2 {r2:.3f} n {n}")
# a combinação também nos níveis recentes (os pesos de um índice encadeado mudam: teste da janela curta)
d = dl.loc["2023-01-01":"2026-08-01"].dropna()
W, _, r2w, nw = ols(d.icbr_usd.values, d[["icbr_agropecuaria_usd", "icbr_metal_usd", "icbr_energia_usd"]].values, const=False)
print("   2023–ago/26:", np.round(W, 3), f"R2 {r2w:.3f} n {nw}")
# o mesmo com setembro, para o log
d9 = dl.loc["2023-01-01":"2026-09-01"].dropna()
W9, *_ = ols(d9.icbr_usd.values, d9[["icbr_agropecuaria_usd", "icbr_metal_usd", "icbr_energia_usd"]].values, const=False)
print("   2023–set/26 (com o dado divulgado depois do corte):", np.round(W9, 3))

e = pd.DataFrame({"ene": dl.icbr_energia_usd, "br0": 100 * np.log(brm).diff()})
e["br1"] = e.br0.shift(1)
for ini in ["2010-01-01", "2018-01-01"]:
    d = e.loc[ini:"2026-08-01"].dropna()
    b, se, r2, n = ols(d.ene.values, d[["br0", "br1"]].values)
    print(f"4b. Δlog IC-Br energia = a + c0·ΔlogBrent + c1·(-1), {ini[:4]}–ago/26:", np.round(b, 3),
          "ep", np.round(se, 3), f"R2 {r2:.2f} n {n}")
print("   razão IC-Br energia / Brent médio, 2026:", (ic.icbr_energia_usd / brm)["2026-01-01":].round(3).to_dict())

# ---------- 5. Dólar EM contra commodities e contra S&P
em = rd("cmb_dollar_index_em").set_index("date")["value"]
sp = rd("cmb_equity_us").set_index("date")["value"]
emm = em.resample("MS").mean()
x = pd.DataFrame({"em": 100 * np.log(emm).diff(), "ic": dl.icbr_usd, "agr": dl.icbr_agropecuaria_usd,
                  "met": dl.icbr_metal_usd, "ene": dl.icbr_energia_usd}).loc[:"2026-08-01"].dropna()
print("\n5a. Correlação mensal Δlog dólar EM (média do mês) × Δlog IC-Br e grupos:")
for lab, ini in [("12m", "2025-09-01"), ("36m", "2023-09-01"), ("10a", "2016-09-01"), ("desde 2006", "2006-02-01")]:
    z = x.loc[ini:]
    print(f"   {lab}: " + ", ".join(f"{k} {z.em.corr(z[k]):+.2f}" for k in ["ic", "agr", "met", "ene"]) + f" (n={len(z)})")

q = pd.DataFrame({"em": em.resample("QE").last(), "sp": sp.resample("QE").last()}).dropna()
qd = pd.DataFrame({"dem": 100 * np.log(q.em).diff(), "dsp": 100 * np.log(q.sp).diff()}).dropna()
qd = qd[qd.index <= "2026-09-30"]
print("\n5b. Trimestral: correlação Δlog dólar EM × Δlog S&P:",
      round(qd.dem.corr(qd.dsp), 2), "n", len(qd), "| desde 2016:", round(qd.loc["2016":].dem.corr(qd.loc["2016":].dsp), 2))
b, se, r2, n = ols(qd.dem.values, qd[["dsp"]].values)
print("   Δdólar EM = a + b·ΔS&P:", np.round(b, 3), "ep", np.round(se, 3), f"R2 {r2:.2f}")
print("   Trimestres com S&P ≤ −8%: Δdólar EM médio", round(qd[qd.dsp <= -8].dem.mean(), 2),
      "n", int((qd.dsp <= -8).sum()), "| datas", [str(i.date()) for i in qd[qd.dsp <= -8].index])
print("   Trimestres com S&P ≥ +8%: Δdólar EM médio", round(qd[qd.dsp >= 8].dem.mean(), 2), "n", int((qd.dsp >= 8).sum()))
print("   Distribuição da variação trimestral do dólar EM (%): p5 {:.2f} p10 {:.2f} p25 {:.2f} p50 {:.2f} p75 {:.2f} p90 {:.2f} p95 {:.2f}".format(
    *qd.dem.quantile([.05, .1, .25, .5, .75, .9, .95]).values))
print("   S&P trimestral (%): p5 {:.2f} p10 {:.2f} p25 {:.2f} p50 {:.2f} p75 {:.2f} p90 {:.2f} p95 {:.2f}".format(
    *qd.dsp.quantile([.05, .1, .25, .5, .75, .9, .95]).values))

# ---------- 6. Episódio de março de 2026
print("\n6. Episódio 2026:")
for s, nm in [(br, "Brent"), (sp, "S&P"), (em, "dólar EM")]:
    print(f"   {nm}:", {d: round(float(s[:d].iloc[-1]), 2) for d in
                        ["2026-02-27", "2026-03-30", "2026-04-30", "2026-06-30", "2026-08-31", "2026-10-02"]})
print("   S&P: máx antes de 30/03:", round(sp["2026-01-01":"2026-03-29"].max(), 1), sp["2026-01-01":"2026-03-29"].idxmax().date())

# ---------- 7. CPI 12m por data e núcleo
for end in ["2026-08-01", "2026-09-01"]:
    t0 = pd.Timestamp(end) - pd.DateOffset(years=1)
    print(f"\n7. 12m até {end[:7]}: cheio {100*(cpi.SA0[end]/cpi.SA0[t0]-1):.2f}, núcleo {100*(cpi.SA0L1E[end]/cpi.SA0L1E[t0]-1):.2f},"
          f" serviços s/ energia {100*(cpi.SASLE[end]/cpi.SASLE[t0]-1):.2f}, energia {100*(cpi.SA0E[end]/cpi.SA0E[t0]-1):.2f}")

# ---------- 8. Juro real de 10 anos ex-ante em set (com a inflação esperada de set, a que existia)
ei = rd("expc_inflacao").pivot_table(index="date", columns="tenor", values="value")
t10 = tr["10Y"]
print("\n8. Treasury 10a − inflação esperada 10a: set/26 (fim do mês e esp. de set)",
      round(t10[:"2026-09-30"].iloc[-1] - ei.loc["2026-09-01", "10Y"], 2),
      "| 02/10 com esp. de set", round(t10.iloc[-1] - ei.loc["2026-09-01", "10Y"], 2),
      "| jun/26", round(t10[:"2026-06-30"].iloc[-1] - ei.loc["2026-06-01", "10Y"], 2))
rr = (t10.resample("MS").mean() - ei["10Y"]).dropna()
print("   percentil do ex-ante de set/26 nos últimos 10 anos:", round(100 * (rr["2016-09-01":] <= rr["2026-09-01"]).mean()))
# inclinação 10a − 3m nas datas
print("   10a−2a: 30/06", round(tr.loc[:"2026-06-30"].iloc[-1]["10Y"] - tr.loc[:"2026-06-30"].iloc[-1]["2Y"], 2),
      "| 02/10", round(tr.iloc[-1]["10Y"] - tr.iloc[-1]["2Y"], 2))
