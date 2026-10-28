"""Os três cenários da etapa 1 no Modelo Estrutural, e o upside com o tempero (i) da regra
(ciclo 2026-10-27, política monetária, rodada 1).

meta_12m: deste agente (principal). rr_10a: principal fiscal; o caminho é o de referência deste
agente como subordinado, rodado como "aguarda fiscal". fiscal (CDS): principal fiscal, "aguarda
fiscal". As outras exógenas no padrão do simulador."""
import pandas as pd
from pathlib import Path
from analytics.agent_system import modelo

A = Path(__file__).resolve().parent.parent / "A"
bi = pd.read_csv(A / "br_interest_rate.csv.gz")
n = bi[(bi.curve == "NTNBJS") & (bi.tenor == "120M")].set_index("date").value
q4 = n[n.index >= "2026-10-01"]
k, ult = len(q4), n.iloc[-1]
TOT = 62  # pregões estimados no 4T26 (out 21, nov 19, dez 22)
med_out = n[(n.index >= "2026-10-01") & (n.index <= "2026-10-23")].mean()
q4_base = (q4.sum() + (TOT - k) * ult) / TOT          # nível de 26/10 até o fim do trimestre
q4_down = (q4.sum() + (TOT - k) * med_out) / TOT      # volta à média de 01-23/10
q4_up = (q4.sum() + (TOT - k) * 8.60) / TOT           # sobe a 8,60 já em novembro
print(f"NTN-B 10a: último {ult:.3f} (26/10); média 01-23/10 {med_out:.3f}; 4T26 base {q4_base:.2f}, downside {q4_down:.2f}, upside {q4_up:.2f}")

T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
META = {t: 3.00 for t in T}
cen = {
    "base": dict(caminhos={"meta_12m": META,
                           "rr_10a": {"4T26": round(q4_base, 2), **{t: round(ult, 2) for t in T[1:]}},
                           "fiscal": {t: 137.43 for t in T}}),
    "upside": dict(caminhos={"meta_12m": META,
                             "rr_10a": {"4T26": round(q4_up, 2), **{t: 8.60 for t in T[1:]}},
                             "fiscal": {"4T26": 180, "1T27": 200, "2T27": 190, "3T27": 180, "4T27": 170, "1T28": 160}}),
    "downside": dict(caminhos={"meta_12m": META,
                               "rr_10a": {"4T26": round(q4_down, 2), **{t: round(med_out, 2) for t in T[1:]}},
                               "fiscal": {t: 115 for t in T}}),
}
cen["upside + R.t3 x1,3"] = dict(caminhos=cen["upside"]["caminhos"], mult={"R.t3": 1.3})
sim = modelo.carregar("2026-10-27")
out = {}
for nome, kw in cen.items():
    res = modelo.rodar(sim, **kw)
    out[nome] = res
    print(f"\n===== {nome} =====")
    print(modelo.texto(res, trimestres=T))
