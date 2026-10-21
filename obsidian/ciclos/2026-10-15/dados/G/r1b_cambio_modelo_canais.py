"""G r1b: de onde vem a subida da central (5,16 -> 5,22) com as exógenas paradas: o canal do carry/vol
(desligado com mult 0) e a inflação dos EUA (posta igual a 1,20% por trimestre, ~ o ritmo do IPCA)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from analytics.agent_system import modelo
from r1b_cambio_modelo_base import BASE, TRI

sim = modelo.carregar("2026-10-15")
P = lambda c, m=None: modelo.rodar(sim, caminhos=c, mult=m or {})["endogenas"]["ptax"]["central"][:6]
b = P(BASE)
nc = P(BASE, {"F.b_carry_vol": 0.0})
ius = P({**BASE, "infl_us": {t: 1.20 for t in TRI}})
fmt = lambda v: " · ".join(f"{q} {x:.3f}" for q, x in zip(TRI, v))
print("base            ", fmt(b), f"| 4T26->1T28 {100*(b[-1]/b[0]-1):+.2f}%")
print("sem carry/vol   ", fmt(nc), f"| 4T26->1T28 {100*(nc[-1]/nc[0]-1):+.2f}%")
print("infl EUA 1,20/tri", fmt(ius), f"| 4T26->1T28 {100*(ius[-1]/ius[0]-1):+.2f}%")
print("carry/vol: contribuição em 1T28", f"{100*(b[-1]/nc[-1]-1):+.2f}%")
