"""Sensibilidade da Selic de fechamento do modelo a cada exógena que a regra e a IS leem, e
média do NTN-B 10 anos no 4T26 até 26/10 (ciclo 2026-10-27)."""
import pandas as pd
from pathlib import Path
from analytics.agent_system import modelo

A = Path(__file__).resolve().parent.parent / "A"
bi = pd.read_csv(A / "br_interest_rate.csv.gz")
n = bi[(bi.curve == "NTNBJS") & (bi.tenor == "120M")].set_index("date").value
print("NTN-B 10a média 4T26 até 26/10:", round(n[n.index >= "2026-10-01"].mean(), 3), "· pregões:", (n.index >= "2026-10-01").sum())
print("NTN-B 10a média 3T26:", round(n[(n.index >= "2026-07-01") & (n.index < "2026-10-01")].mean(), 3))
print("NTN-B 10a média out/26 até 23/10:", round(n[(n.index >= "2026-10-01") & (n.index <= "2026-10-23")].mean(), 3))

sim = modelo.carregar("2026-10-27")
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
def sf(res):
    s = res["saidas"]["selic_fim"]["central"] if "saidas" in res else None
    return s
res = modelo.rodar(sim)
print(type(res), list(res.keys())[:20])

def linha(nome, res):
    e = res["endogenas"]
    f = lambda k: " ".join(f"{v:6.2f}" if v is not None else "   —  " for v in e[k]["central"][:6])
    print(f"{nome:38s} selic_fim {f('selic_fim')} | ptax {f('ptax')} | ipca12 {f('ipca_12m')} | focus {f('focus_12m')} | hiato {f('hiato')}")

# média do 4T26 se o nível de 26/10 ficar até o fim do trimestre (62 pregões estimados no trimestre)
resto = 62 - 17
print("4T26 com 8,05 no resto do tri:", round((17 * 6.995 + resto * n.iloc[-1]) / 62, 2))
linha("padrão", modelo.rodar(sim))
linha("rr_10a 7,84 -> 8,84 (+1)", modelo.rodar(sim, caminhos={"rr_10a": {t: 8.84 for t in T}}))
linha("rr_10a 6,84 (-1)", modelo.rodar(sim, caminhos={"rr_10a": {t: 6.84 for t in T}}))
linha("fiscal 137", modelo.rodar(sim, caminhos={"fiscal": {t: 137.43 for t in T}}))
linha("fiscal 200 no 4T26", modelo.rodar(sim, caminhos={"fiscal": {"4T26": 200}}))
linha("meta 3,5", modelo.rodar(sim, caminhos={"meta_12m": {t: 3.5 for t in T}}))
linha("R.t3 x1,3", modelo.rodar(sim, mult={"R.t3": 1.3}))
