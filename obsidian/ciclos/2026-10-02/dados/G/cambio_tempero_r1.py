"""G do câmbio, ciclo 2026-10-02, rodada 1: a tabela 3.3 (do modelo à tese) e as faixas.

- Upside: modelo (caminhos do cenário) -> (i) F.b_carry_vol x1,5 -> (ii) o BC no mercado de
  câmbio, -1,0% no 4T26 e no 1T27 e -0,5% no 2T27 sobre o caminho com (i).
- Downside: modelo -> (ii) petróleo além do IC-Br, -0,5% no 4T26 e -1,5% do 1T27 em diante.
- Faixa base: central x (1 ± x_h), x_h = 0,67 x 12% x raiz(h/4), h = 1..6 trimestres (vol de 12%
  ao ano, a mediana de 10 anos da realizada de 63 dias; 0,67 desvio dá ~50% numa normal)."""
import numpy as np
from analytics.agent_system import modelo
import importlib.util, pathlib

spec = importlib.util.spec_from_file_location("c", pathlib.Path(__file__).with_name("cambio_cenarios_r1.py"))
# reaproveita os caminhos do G dos cenários sem rodar o print dele
src = pathlib.Path(__file__).with_name("cambio_cenarios_r1.py").read_text(encoding="utf-8")
ns = {}
exec(src.split("runs = {")[0], ns)
sim, base, upside, downside = ns["sim"], ns["base"], ns["upside"], ns["downside"]
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]


def ptax(res):
    linha = [l for l in modelo.texto(res).splitlines() if l.startswith("| PTAX")][0]
    cels = [c.strip() for c in linha.split("|")[2:-1]][1:7]
    return np.array([float(c.split(" ")[0].replace(",", ".")) for c in cels])


cb = ptax(modelo.rodar(sim, caminhos=base))
up_m = ptax(modelo.rodar(sim, caminhos=upside))
up_i = ptax(modelo.rodar(sim, caminhos=upside, mult={"F.b_carry_vol": 1.5}))
up_t = up_i * (1 + np.array([-0.010, -0.010, -0.005, 0, 0, 0]))
dn_m = ptax(modelo.rodar(sim, caminhos=downside))
dn_t = dn_m * (1 + np.array([-0.005, -0.015, -0.015, -0.015, -0.015, -0.015]))
x = 0.67 * 0.12 * np.sqrt(np.arange(1, 7) / 4)
print("tri | central | faixa | upside: modelo -> (i) -> (ii) | downside: modelo -> (ii) | x")
for i, t in enumerate(T):
    print(t, f"{cb[i]:.3f}", f"{cb[i]*(1-x[i]):.2f}-{cb[i]*(1+x[i]):.2f}",
          f"{up_m[i]:.3f} -> {up_i[i]:.3f} -> {up_t[i]:.3f}", f"{dn_m[i]:.3f} -> {dn_t[i]:.3f}", f"{100*x[i]:.1f}%")
print("\nupside com tempero contra a central (%):", np.round(100 * (up_t / cb - 1), 1))
print("downside com tempero contra a central (%):", np.round(100 * (dn_t / cb - 1), 1))
