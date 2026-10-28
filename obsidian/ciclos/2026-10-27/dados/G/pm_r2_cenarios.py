"""Etapa 1 da rodada 2 (política monetária, ciclo 2026-10-27): os cenários no Modelo Estrutural.

Base: os caminhos usados no P1 (P1.json, "caminhos_usados"), isto é, o de cada principal; deve
reproduzir o selic_fim do P1. Caudas: os caminhos de cauda dos principais, como escritos nos
reports da rodada 1 — rr_10a e CDS do fiscal (fiscal_r1, seção 3.1), vol do câmbio (cambio_r1,
seção 3.1); o resto no caminho do P1. meta_12m (deste agente) em 3,00 nos três.
Mais o upside com R.t3 x 1,3 (tempero i, deste agente, dono da (R))."""
import json
from pathlib import Path
from analytics.agent_system import modelo

CIC = Path(__file__).resolve().parent.parent.parent
P1 = json.loads((CIC / "P1.json").read_text(encoding="utf-8"))
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
base = {k: {t: v[t] for t in T} for k, v in P1["caminhos_usados"].items()}

def com(**sub):
    c = {k: dict(v) for k, v in base.items()}
    for k, v in sub.items():
        c[k] = dict(zip(T, v))
    return c

cen = {
    "base (P1)": dict(caminhos=base),
    "upside": dict(caminhos=com(rr_10a=[8.05, 8.80, 9.00, 9.00, 8.90, 8.80],
                                fiscal=[165, 190, 200, 200, 195, 190],
                                vol=[24.0, 21.0, 18.0, 16.0, 15.0, 15.0])),
    "downside": dict(caminhos=com(rr_10a=[7.35, 6.90, 6.80, 6.75, 6.70, 6.70],
                                  fiscal=[115, 110, 108, 106, 105, 105],
                                  vol=[13.0, 12.5, 12.0, 12.0, 12.0, 12.0])),
}
cen["upside + R.t3 x1,3"] = dict(caminhos=cen["upside"]["caminhos"], mult={"R.t3": 1.3})
# sensibilidade: só a rr_10a de referência deste agente (r1) sobre o base do P1
cen["base com rr_10a 8,05 (ref. r1)"] = dict(caminhos=com(rr_10a=[7.76, 8.05, 8.05, 8.05, 8.05, 8.05]))

sim = modelo.carregar("2026-10-27")
print("P1 selic_fim:", [round(x, 2) for x in P1["modelo"]["endogenas"]["selic_fim"]["central"][:6]])
for nome, kw in cen.items():
    res = modelo.rodar(sim, **kw)
    print(f"\n===== {nome} =====")
    print(modelo.texto(res, trimestres=T))
