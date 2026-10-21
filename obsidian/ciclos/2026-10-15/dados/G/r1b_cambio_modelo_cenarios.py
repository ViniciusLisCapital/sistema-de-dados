"""G r1b: cenários worst e best do Modelo Estrutural, sem e com o tempero (i) (efeito do CDS x1,5),
e a PTAX com os temperos (ii) do worst (posicionamento +2% no 4T26 e +1% no 1T27; BC −1% no 4T26).
Também roda a base com o tempero (i), que não move a central e entra só na assimetria."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from analytics.agent_system import modelo
from r1b_cambio_modelo_base import BASE, TRI

def cam(**kw):
    return {k: dict(zip(TRI, v)) for k, v in kw.items()}

WORST = cam(
    fiscal=[150, 160, 165, 170, 175, 180],
    vol=[16, 15, 14, 14, 14, 14],
    dxy_em=[132, 133, 134, 134, 134, 134],
    sp500=[7300] * 6,
    icbr_usd=[205.70] * 6,
    ffr=[4.125, 4.375, 4.375, 4.375, 4.375, 4.375],
    infl_us=[1.20, 1.20, 1.00, 0.91, 0.91, 0.91],
)
BEST = cam(
    fiscal=[100, 95, 90, 85, 85, 85],
    vol=[11] * 6,
    dxy_em=[128, 127, 127, 127, 127, 127],
    sp500=[7720.99] * 6,
    icbr_usd=[205.70] * 6,
    ffr=[3.875, 3.875, 3.625, 3.625, 3.625, 3.625],
    infl_us=[0.91, 0.80, 0.80, 0.80, 0.80, 0.80],
)
MULT = {"F.b_fiscal": 1.5}
II_WORST = [0.02 - 0.01, 0.01, 0, 0, 0, 0]  # posicionamento + BC, por trimestre

sim = modelo.carregar("2026-10-15")
def run(c, m=None):
    return modelo.rodar(sim, caminhos=c, mult=m or {})

out = {}
for nome, c in [("base", BASE), ("worst", WORST), ("best", BEST)]:
    for tag, m in [("modelo", None), ("x1,5", MULT)]:
        r = run(c, m)
        out[(nome, tag)] = r
        e = r["endogenas"]
        print(f"{nome} {tag}: PTAX " + " · ".join(f"{q} {v:.3f}" for q, v in zip(TRI, e["ptax"]["central"][:6])))
        print(f"      Selic média " + " · ".join(f"{v:.2f}" for v in e["selic"]["central"][:6])
              + " | IPCA 12m " + " · ".join(f"{v:.2f}" for v in e["ipca_12m"]["central"][:6]))
w = out[("worst", "x1,5")]["endogenas"]["ptax"]["central"][:6]
print("worst com (i) e (ii): " + " · ".join(f"{q} {v*(1+a):.3f}" for q, v, a in zip(TRI, w, II_WORST)))
print()
print(modelo.texto(out[("worst", "modelo")]))
print(modelo.texto(out[("best", "modelo")]))
