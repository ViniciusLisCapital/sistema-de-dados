# Report final: base = caminhos do P2; caudas do fiscal r2 (rr_10a, CDS) e do câmbio (vol).
"""Etapa 1 da report final (política monetária, ciclo 2026-10-27): os cenários no Modelo Estrutural.

Base: os caminhos usados no P1 (P1.json, "caminhos_usados"), isto é, o de cada principal; deve
reproduzir o selic_fim do P1. Caudas: os caminhos de cauda dos principais, como escritos nos
reports da rodada 1 — rr_10a e CDS do fiscal (fiscal_r1, seção 3.1), vol do câmbio (cambio_r1,
seção 3.1); o resto no caminho do P1. meta_12m (deste agente) em 3,00 nos três.
Mais o upside com R.t3 x 1,3 (tempero i, deste agente, dono da (R))."""
import json
from pathlib import Path
from analytics.agent_system import modelo

CIC = Path(__file__).resolve().parent.parent.parent
P1 = json.loads((CIC / "P2.json").read_text(encoding="utf-8"))
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
base = {k: {t: v[t] for t in T} for k, v in P1["caminhos_usados"].items()}

def com(**sub):
    c = {k: dict(v) for k, v in base.items()}
    for k, v in sub.items():
        c[k] = dict(zip(T, v))
    return c

cen = {
    "base (P2)": dict(caminhos=base),
    "upside": dict(caminhos=com(rr_10a=[8.15, 8.90, 9.10, 9.10, 9.00, 8.90],
                                fiscal=[170, 205, 210, 205, 198, 190],
                                vol=[24.0, 21.0, 18.0, 16.0, 15.0, 15.0])),
    "downside": dict(caminhos=com(rr_10a=[7.36, 7.30, 7.15, 7.05, 7.00, 6.95],
                                  fiscal=[122, 115, 112, 110, 108, 106],
                                  vol=[13.0, 12.5, 12.0, 12.0, 12.0, 12.0])),
}
cen["upside + R.t3 x1,3"] = dict(caminhos=cen["upside"]["caminhos"], mult={"R.t3": 1.3})

sim = modelo.carregar("2026-10-27")
print("P2 selic_fim:", [round(x, 2) for x in P1["modelo"]["endogenas"]["selic_fim"]["central"][:6]])
for nome, kw in cen.items():
    res = modelo.rodar(sim, **kw)
    print(f"\n===== {nome} =====")
    print(modelo.texto(res, trimestres=T))
