"""G do câmbio, ciclo 2026-10-02, rodada 1: as contas pequenas que o report cita.
- Brent de 01/10 a 02/10 (%), em `comm_brent`;
- o dólar contra emergentes do upside (134,9) e do downside (126,9) contra o de 02/10;
- a volatilidade do base (12,7) contra a segurada pelo simulador (12,19);
- o efeito no modelo de 20 p.b. de CDS: peso por desvio / desvio x 20 (coeficientes do retrato);
- o efeito do tempero (i) no upside, trimestre a trimestre (PTAX com e sem o multiplicador).
Lê só ../A/ e o retrato do simulador."""
import pathlib
import numpy as np
import pandas as pd
from analytics.agent_system import modelo

A = pathlib.Path(__file__).resolve().parent.parent / "A"
b = pd.read_csv(A / "comm_brent.csv.gz").set_index("date")["value"]
print("Brent 01/10 -> 02/10:", f"{100*(b['2026-10-02']/b['2026-10-01']-1):+.1f}%")
d = pd.read_csv(A / "cmb_dollar_index_em.csv.gz").set_index("date")["value"]
print("dxy_em upside vs 02/10:", f"{100*(134.9/d['2026-10-02']-1):+.1f}%", "· downside:", f"{100*(126.9/d['2026-10-02']-1):+.1f}%")
print("vol base - 12,19:", round(12.7 - 12.19, 2))

sim = modelo.carregar("2026-10-02")
coef = modelo.coeficientes(sim)
print(coef if not hasattr(coef, "items") else {k: v for k, v in coef.items() if k.startswith("F.b_fiscal")})
# peso por desvio-padrão da variação: 25,111 por 298,5 p.b. (do listar())
print("20 p.b. de CDS:", f"{25.111/298.5*20:.2f}% na PTAX")

src = pathlib.Path(__file__).with_name("cambio_cenarios_r1.py").read_text(encoding="utf-8")
ns = {}
exec(src.split("runs = {")[0], ns)


def ptax(res):
    linha = [l for l in modelo.texto(res).splitlines() if l.startswith("| PTAX")][0]
    cels = [c.strip() for c in linha.split("|")[2:-1]][1:7]
    return np.array([float(c.split(" ")[0].replace(",", ".")) for c in cels])


m = ptax(modelo.rodar(sim, caminhos=ns["upside"]))
i = ptax(modelo.rodar(sim, caminhos=ns["upside"], mult={"F.b_carry_vol": 1.5}))
print("tempero (i) no upside (%):", np.round(100 * (i / m - 1), 2))

# conferência no próprio modelo: +20 p.b. de CDS no 4T26 sobre o base
b0 = ptax(modelo.rodar(sim, caminhos=ns["base"]))
c = dict(ns["base"]); c["fiscal"] = {"4T26": 131.21 + 20}
b1 = ptax(modelo.rodar(sim, caminhos=c))
print("+20 p.b. de CDS no modelo (% na PTAX):", np.round(100 * (b1 / b0 - 1), 2))
