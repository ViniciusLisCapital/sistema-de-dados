"""Contas pequenas do report final (política monetária, ciclo 2026-10-27). Lê A/ e P2.json."""
import json
from pathlib import Path
import pandas as pd
CIC = Path(__file__).resolve().parent.parent.parent
P2 = json.loads((CIC / "P2.json").read_text(encoding="utf-8"))
P1 = json.loads((CIC / "P1.json").read_text(encoding="utf-8"))
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
sf2 = P2["modelo"]["endogenas"]["selic_fim"]["central"][:6]
sf1 = P1["modelo"]["endogenas"]["selic_fim"]["central"][:6]
print("P2 − P1:", [round(a - b, 2) for a, b in zip(sf2, sf1)])
rr = P2["caminhos_usados"]["rr_10a"]; ffr = P2["caminhos_usados"]["ffr"]
print(f"âncora 4T26 {rr['4T26']+3:.2f}; Selic 13,75 − âncora {13.75-(rr['4T26']+3):+.2f}")
print(f"Selic fim − Fed: 4T26 {sf2[0]-ffr['4T26']:.2f} · 1T28 {sf2[5]-ffr['1T28']:.2f} · pausa {13.75-ffr['4T26']:.2f}")
# câmbio de partida de 04/11: dez dias úteis de 19/10 a 30/10; seis no F, quatro faltando
p = pd.read_csv(CIC / "dados" / "A" / "cmb_ptax.csv.gz"); p = p[p.name == "ptax_venda"].set_index("date").value
k = p["2026-10-19":"2026-10-30"]
print("dias no F:", len(k), k.round(4).tolist())
for resto in (5.35, 5.50):
    m = (k.sum() + (10 - len(k)) * resto) / 10
    print(f"  resto a {resto:.2f}: média {m:.3f} · contra 5,15: {(m/5.15-1)*100:+.1f}%")
# alta em 09/12 condicionada a PTAX > 5,50 até lá: o estado pesa ~60% no regime de alta (0,70 de alta em dez)
# e ~40% na pausa (0,10 de alta em dez); julgamento deste agente sobre os pesos condicionais
print(f"P(alta em 09/12 | PTAX > 5,50): {0.6*0.70+0.4*0.10:.2f}")
# checagem: P(sinal de segunda ordem até 09/12) de 55% (expectativas_r2) × P(Copom sobe | sinal) 55%
print(f"0,55 × 0,55 = {0.55*0.55:.2f}")
# minha média menos a Focus (janeiro e março de 2027) e rr_10a do 1T28 do P2 contra o real Focus 2028
print(f"jan/27: {13.85-13.00:+.2f} · mar/27: {13.86-12.75:+.2f}")
print(f"rr_10a 1T28 P2 {rr['1T28']:.2f} − 6,02 = {rr['1T28']-6.02:+.2f}")
# cobrança C2: distância da central do PF* (4T26) até 13,75
pf = json.loads((CIC / "PF.json").read_text(encoding="utf-8"))
c = [t for t in pf["teses"] if t["agente"] == "politica_monetaria" and t["trimestre"] == "4T26"][0]["central_p"]
print(f"PF* 4T26 {c:.4f} · 13,75 − PF* = {13.75 - c:.2f} · em cortes de 25 p.b.: {(13.75 - c)/0.25:.2f}")
