"""Moderação r2, item 5: quanto da Selic da base vem do prêmio de 26/10 que o modelo lê como neutro.
Base: caminhos do P1 com o rr_10a novo do fiscal (r2 moderado). Contrafactual: rr_10a na média de
01-23/10 (6,93, br_interest_rate), antes da eleição; o resto igual."""
import json
from pathlib import Path
from analytics.agent_system import modelo
CIC = Path(__file__).resolve().parent.parent.parent
P1 = json.loads((CIC / "P1.json").read_text(encoding="utf-8"))
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
base = {k: {t: v[t] for t in T} for k, v in P1["caminhos_usados"].items()}
sim = modelo.carregar("2026-10-27")
def fim(rr):
    c = {k: dict(v) for k, v in base.items()}; c["rr_10a"] = dict(zip(T, rr))
    r = modelo.rodar(sim, caminhos=c)
    return [round(x, 2) for x in r["endogenas"]["selic_fim"]["central"][:6]], [round(x, 2) for x in r["endogenas"]["hiato"]["central"][:6]]
a, ha = fim([7.72, 7.95, 7.90, 7.80, 7.75, 7.70])
b, hb = fim([6.93] * 6)
print("fiscal r2:", a, "hiato", ha)
print("rr 6,93 :", b, "hiato", hb)
print("prêmio na Selic:", [round(x - y, 2) for x, y in zip(a, b)])
