"""G do externo, ciclo 2026-10-02: as contas pequenas que o texto do report cita.

Diferenças e variações entre valores lidos do A (ou impressos pelos outros G deste agente,
repetidos aqui como constantes com a origem ao lado). Lê só ../A/.
"""
from pathlib import Path
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"

def s(t, col="value"):
    d = pd.read_csv(A / f"{t}.csv.gz"); d["date"] = pd.to_datetime(d["date"])
    return d.set_index("date")[col].sort_index()

def em(serie, d):
    return float(serie[:d].iloc[-1])

c = pd.read_csv(A / "us_interest_rate__curva_completa.csv.gz"); c["date"] = pd.to_datetime(c["date"])
tr = c[c.curve == "US_TREASURY"].pivot_table(index="date", columns="tenor", values="value")
print("10a: 30/06 -> 02/10:", em(tr["10Y"], "2026-06-30"), "->", tr["10Y"].iloc[-1],
      f"Δ {tr['10Y'].iloc[-1] - em(tr['10Y'], '2026-06-30'):+.2f}")
print("2a:  30/06 -> 02/10:", em(tr["2Y"], "2026-06-30"), "->", tr["2Y"].iloc[-1],
      f"Δ {tr['2Y'].iloc[-1] - em(tr['2Y'], '2026-06-30'):+.2f}")
ei = pd.read_csv(A / "expc_inflacao.csv.gz"); ei["date"] = pd.to_datetime(ei["date"])
ei = ei.pivot_table(index="date", columns="tenor", values="value")
print(f"esperada 10a jun->set: {ei.loc['2026-06-01','10Y']:.2f} -> {ei.loc['2026-09-01','10Y']:.2f} "
      f"Δ {ei.loc['2026-09-01','10Y'] - ei.loc['2026-06-01','10Y']:+.2f}")
print(f"real ex-ante 10a 1,97 -> 2,70 (ex_relacoes.py, item 8): Δ {2.70 - 1.97:+.2f}")

em_ = s("cmb_dollar_index_em"); sp = s("cmb_equity_us"); cds = s("cmb_risco_pais")
print(f"dólar EM 31/08->30/09: {100*(em(em_,'2026-09-30')/em(em_,'2026-08-31')-1):+.2f}%")
print(f"CDS 31/08->30/09: {em(cds,'2026-09-30') - em(cds,'2026-08-31'):+.1f} p.b.")
print(f"S&P 02/10 vs máx 13/08: {100*(sp.iloc[-1]/sp['2026'].max()-1):+.2f}%")
print(f"S&P 27/02->30/03: {100*(em(sp,'2026-03-30')/em(sp,'2026-02-27')-1):+.2f}% | dólar EM: "
      f"{100*(em(em_,'2026-03-30')/em(em_,'2026-02-27')-1):+.2f}%")
# cenários contra o ponto de hoje / contra a base (valores de ex_cenarios_r1.py)
print(f"risk-off 4T26: dólar EM 134,5 vs 02/10 {100*(134.5/em_.iloc[-1]-1):+.2f}% e vs base 130 {100*(134.5/130-1):+.2f}%;"
      f" S&P 6.900 vs base 7.700 {100*(6900/7700-1):+.2f}% e vs 02/10 {100*(6900/sp.iloc[-1]-1):+.2f}%")
print(f"PTAX 4T26 risk-off 5,271 vs base 5,244: {100*(5.271/5.244-1):+.2f}% | S&P sozinho 5,115: {100*(5.115/5.244-1):+.2f}%")
print(f"Selic 1T28 commodities downside 12,18 vs base 12,29: {12.18-12.29:+.2f} p.p.")
print(f"IPCA 12m 1T28 commodities downside 3,68 vs base 4,12: {3.68-4.12:+.2f} p.p.")
br = s("comm_brent")
print(f"Brent 01/10->02/10: {100*(br.iloc[-1]/br.iloc[-2]-1):+.1f}%")
print(f"S&P base por trimestre: {100*((8200/7700)**(1/5)-1):+.2f}%/tri (4T26->1T28)")
print("Fed parado: 11/12/2025 -> 17/09/2026 =", (pd.Timestamp('2026-09-17') - pd.Timestamp('2025-12-11')).days, "dias")
