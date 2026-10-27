"""G do câmbio, ciclo 2026-10-02, rodada 1: o que leva às caudas de 3T27 a 1T28, onde os
cenários de upside e downside do 4T26 já ficam dentro da faixa base. Segunda perna:
- upside longo: o upside com o CDS subindo a 200 p.b. no 2T27 (aguarda fiscal), com (i);
- downside longo: o downside com o dólar contra emergentes caindo mais, a 122 no 2T27."""
import pathlib
import numpy as np
from analytics.agent_system import modelo

src = pathlib.Path(__file__).with_name("cambio_cenarios_r1.py").read_text(encoding="utf-8")
ns = {}
exec(src.split("runs = {")[0], ns)
sim, upside, downside = ns["sim"], ns["upside"], ns["downside"]

up2 = {k: dict(v) for k, v in upside.items()}
up2["fiscal"] = {"4T26": 150.0, "1T27": 155.0, "2T27": 200.0}
dn2 = {k: dict(v) for k, v in downside.items()}
dn2["dxy_em"] = {"4T26": 126.9, "2T27": 122.0}


def ptax(res):
    linha = [l for l in modelo.texto(res).splitlines() if l.startswith("| PTAX")][0]
    return [c.strip().split(" ")[0] for c in linha.split("|")[2:-1]][1:7]


print("upside longo, com (i):", ptax(modelo.rodar(sim, caminhos=up2, mult={"F.b_carry_vol": 1.5})))
r = ptax(modelo.rodar(sim, caminhos=dn2))
print("downside longo, modelo:", r)
v = np.array([float(x.replace(",", ".")) for x in r]) * (1 + np.array([-0.005, -0.015, -0.015, -0.015, -0.015, -0.015]))
print("downside longo, com (ii):", np.round(v, 3))
