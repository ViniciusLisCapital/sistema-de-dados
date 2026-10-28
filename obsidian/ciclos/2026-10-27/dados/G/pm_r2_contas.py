"""Contas pequenas da rodada 2 (política monetária, ciclo 2026-10-27). Lê A/ e o P1.json."""
import json
from pathlib import Path

CIC = Path(__file__).resolve().parent.parent.parent
P1 = json.loads((CIC / "P1.json").read_text(encoding="utf-8"))
rr = P1["caminhos_usados"]["rr_10a"]
sf = P1["modelo"]["endogenas"]["selic_fim"]["central"]
sm = P1["modelo"]["endogenas"]["selic"]["central"]
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
for i, t in enumerate(T):
    anc = rr[t] + 3.00
    print(f"{t}: rr_10a {rr[t]:.2f} · âncora {anc:.2f} · Selic média P1 {sm[i]:.2f} (− âncora {sm[i]-anc:+.2f})"
          f" · Selic fim P1 {sf[i]:.2f} · contra 13,75: {(sf[i]-13.75)*100:+.0f} p.b.")
print(f"Selic 13,75 − âncora do 4T26 do P1: {13.75 - (rr['4T26'] + 3):+.2f} p.p.")
# r1 x P1, diferença de central
r1 = [13.49, 13.32, 13.04, 12.80, 12.58, 12.39]
print("P1 − r1:", [round(sf[i] - r1[i], 2) for i in range(6)])
# Focus 23/10: juro real de política esperado (Selic do ano contra o IPCA do ano)
for ano, s, p in [(2027, 11.75, 4.34), (2028, 10.00, 3.75), (2029, 10.00, 3.50)]:
    print(f"Focus {ano}: Selic {s:.2f}, IPCA {p:.2f} → real {((1+s/100)/(1+p/100)-1)*100:.2f}")
# curva DI de 26/10 contra a média da distribuição deste agente (pm_r2_distribuicao)
for r, curva, media in [("04/11", 13.73, 13.76), ("09/12", 14.02, 13.82), ("27/01", 14.45, 13.85), ("17/03", 14.84, 13.86)]:
    print(f"{r}: curva {curva:.2f} − média da distribuição {media:.2f} = {(curva-media)*100:+.0f} p.b.")
# central com o rr_10a de referência da r1 (pm_r2_cenarios) contra o P1
ref = [13.50, 13.33, 13.07, 12.84, 12.64, 12.46]
print("ref r1 − P1:", [round(ref[i] - sf[i], 2) for i in range(6)])
# diferencial contra o Fed (caminho do externo no P1)
ffr = P1["caminhos_usados"]["ffr"]
print(f"Selic fim − Fed: 4T26 {sf[0]-ffr['4T26']:.2f} · 1T28 {sf[5]-ffr['1T28']:.2f} · pausa 4T26 {13.75-ffr['4T26']:.2f}")
# rr_10a do 1T28 contra o juro real de política da Focus de 2028
print(f"rr_10a 1T28 {rr['1T28']:.2f} − real Focus 2028 6,02 = {rr['1T28']-6.02:+.2f}")
# peso do trecho de 1 a 2 anos na NTN-B de 10 anos: 1/10
for q in (100, 150):
    print(f"queda de {q} p.b. no termo de 1 a 2 anos → {q/10:.0f} p.b. na NTN-B 10a")
print(f"regime de cortes: Copom leniente 5 de 18 p.p. = {5/18*100:.0f}%")
