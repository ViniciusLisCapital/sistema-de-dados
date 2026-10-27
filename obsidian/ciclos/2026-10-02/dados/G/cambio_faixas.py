"""G do câmbio, ciclo 2026-10-02: o tamanho histórico do movimento da PTAX em h trimestres
(para dimensionar a faixa base e as caudas) e o efeito de cada caminho do câmbio, um por vez,
sobre a central do modelo.

1) Variação (%) da PTAX de fechamento de trimestre em h = 1..6 trimestres, 2006T1-2026T3:
   percentis 20, 25, 75, 80 e o desvio-padrão.
2) Modelo: padrão do simulador, e cada um dos três caminhos base sozinho."""
from pathlib import Path
import numpy as np
import pandas as pd
from analytics.agent_system import modelo

A = Path(__file__).resolve().parent.parent / "A"
p = pd.read_csv(A / "cmb_ptax.csv.gz")
p = p[p["name"] == "ptax_venda"]
p = p.set_index(pd.to_datetime(p["date"]))["value"].astype(float)
pq = p.resample("QE").last()
pq = pq[(pq.index >= "2005-12-31") & (pq.index <= "2026-09-30")]
lp = np.log(pq)
print("h | p20 | p25 | p75 | p80 | dp (variação %, simples)")
for h in range(1, 7):
    v = 100 * (np.exp(lp.diff(h).dropna()) - 1)
    q = v.quantile([0.2, 0.25, 0.75, 0.8])
    print(h, *[round(x, 1) for x in q], round(v.std(), 1), f"n={len(v)}")
# o mesmo nos últimos 10 anos
print("\núltimos 10 anos (2016T4-2026T3):")
lp10 = lp[lp.index >= "2016-09-30"]
for h in range(1, 7):
    v = 100 * (np.exp(lp10.diff(h).dropna()) - 1)
    q = v.quantile([0.2, 0.25, 0.75, 0.8])
    print(h, *[round(x, 1) for x in q], round(v.std(), 1), f"n={len(v)}")

sim = modelo.carregar("2026-10-02")
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]


def ptax(res):
    t = modelo.texto(res)
    linha = [l for l in t.splitlines() if l.startswith("| PTAX")][0]
    cels = [c.strip() for c in linha.split("|")[2:-1]]
    return [c.split(" ")[0] for c in cels[1:7]]


print("\nPTAX central, 4T26..1T28")
print("padrão     ", ptax(modelo.rodar(sim)))
for k, v in {"vol": 12.7, "dxy_em": 129.7, "icbr_usd": 207.9}.items():
    print(f"só {k:8s}", ptax(modelo.rodar(sim, caminhos={k: {"4T26": v}})))
