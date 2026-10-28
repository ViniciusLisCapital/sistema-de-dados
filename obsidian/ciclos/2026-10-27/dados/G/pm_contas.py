"""Contas pequenas do report de política monetária, ciclo 2026-10-27. Lê só A/."""
import pandas as pd
from pathlib import Path

A = Path(__file__).resolve().parent.parent / "A"
bi = pd.read_csv(A / "br_interest_rate.csv.gz")
pv = bi.pivot_table(index="date", columns=["curve", "tenor"], values="value")
px = pd.read_csv(A / "cmb_ptax.csv.gz"); px = px[px.name == "ptax_venda"].set_index("date").value
cds = pd.read_csv(A / "cmb_risco_pais.csv.gz"); cds = cds[cds.name == "cds_5y_usd"].set_index("date").value
fo = pd.read_csv(A / "expc_focus.csv.gz")

selic, focus12 = 13.75, None
f12 = fo[(fo.indicador == "IPCA") & (fo.horizonte == "12m") & (fo.suavizada == "S") & (fo.base_calculo == 0)].sort_values("date")
focus12 = f12.mediana.iloc[-1]
real = ((1 + selic / 100) / (1 + focus12 / 100) - 1) * 100
print(f"Focus IPCA 12m (suav.) {f12.date.iloc[-1]}: {focus12:.2f} · Selic real ex-ante {real:.2f}")
print(f"  contra o neutro do Copom (5,00, RPM set/26): {real - 5.00:+.2f} p.p.")
rr10 = pv[("NTNBJS", "120M")]
anc = rr10.iloc[-1] + 3.00
print(f"Âncora do modelo (NTN-B 10a {rr10.iloc[-1]:.2f} + meta 3,00) = {anc:.2f}; Selic − âncora = {selic - anc:+.2f} p.p.")
anc23 = rr10.loc["2026-10-23"] + 3.00
print(f"  em 23/10: âncora {anc23:.2f}; Selic − âncora = {selic - anc23:+.2f} p.p.")
print(f"PTAX 26/10 {px.iloc[-1]:.4f} contra o condicionante do Copom (5,15): {(px.iloc[-1] / 5.15 - 1) * 100:+.1f}%")
print(f"PTAX 26/10 contra o fim do 3T26 (30/09, {px['2026-09-30']:.4f}): {(px.iloc[-1] / px['2026-09-30'] - 1) * 100:+.1f}%")
for a, b in [("2026-10-02", "2026-10-05"), ("2026-10-23", "2026-10-26")]:
    print(f"{a} -> {b}: PTAX {(px[b] / px[a] - 1) * 100:+.2f}% · CDS {cds[b] - cds[a]:+.1f} p.b. · "
          f"DI 2a {(pv.loc[b, ('DIPRE','24M')] - pv.loc[a, ('DIPRE','24M')]) * 100:+.0f} p.b. · "
          f"NTN-B 10a {(rr10[b] - rr10[a]) * 100:+.0f} p.b.")
def fwd5y5(d):
    r5, r10 = pv.loc[d, ("NTNBJS", "60M")] / 100, pv.loc[d, ("NTNBJS", "120M")] / 100
    return (((1 + r10) ** 10 / (1 + r5) ** 5) ** (1 / 5) - 1) * 100
for d in ["2026-10-02", "2026-10-23", "2026-10-26"]:
    print(f"NTN-B real 5a daqui a 5a ({d}): {fwd5y5(d):.2f}")
# Focus Selic implícita em termos reais ao fim do horizonte: Selic 2028 e IPCA 2028
fs = pd.read_csv(A / "expc_focus_periodo__selic.csv.gz"); fi = pd.read_csv(A / "expc_focus_periodo__ipca.csv.gz")
print(fs.columns.tolist())
last = fs.date.max()
for ano in [2027, 2028, 2029]:
    s = fs[(fs.date == last) & (fs.data_referencia.astype(str) == str(ano)) & (fs.base_calculo == 0)].mediana
    i = fi[(fi.date == fi.date.max()) & (fi.data_referencia.astype(str) == str(ano)) & (fi.base_calculo == 0)].mediana
    if len(s) and len(i):
        s, i = s.iloc[0], i.iloc[0]
        print(f"Focus {last} ano {ano}: Selic {s:.2f}, IPCA {i:.2f}, real {((1 + s/100)/(1 + i/100) - 1)*100:.2f}; NTN-B 10a 26/10 menos esse real: {rr10.iloc[-1] - ((1 + s/100)/(1 + i/100) - 1)*100:+.2f}")
print(f"Real 5a daqui a 5a, 23/10 -> 26/10: {(fwd5y5('2026-10-26') - fwd5y5('2026-10-23')) * 100:+.0f} p.b.")
print(f"Selic − âncora, 23/10 -> 26/10: {((selic - anc) - (selic - anc23)):+.2f} p.p.")
