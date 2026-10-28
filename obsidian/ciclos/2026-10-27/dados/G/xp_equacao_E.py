"""Expectativas: a equação (E) no retrato do ciclo — ajuste de um passo, resíduos e ponto de repouso.

Lê só A/modelo_estrutural.json. Imprime: coeficientes (mediana, 90%), meia-vida, os últimos 12
trimestres de y (Focus 12m, média do trimestre), I12, meta e o ajuste de um passo, o resíduo,
o desvio-padrão dos resíduos na amostra inteira, e quantos dos últimos 8 resíduos são positivos.
Também o ponto de repouso da (E) dado um I12: E* = (e2*I12 + (1-e1-e2)*meta)/(1-e1).
"""
import json
from pathlib import Path
import numpy as np

A = Path(__file__).resolve().parent.parent / "A"
p = json.loads((A / "modelo_estrutural.json").read_text(encoding="utf-8"))["p"]
E = p["eq"]["E"]
print("mediana:", E["mediana"])
print("hdi:", E["hdi"])
print("meia_vida:", E["meia_vida"])
print("amostra:", E["amostra"])
print("pars:", E["pars"], "consome:", E["consome"], "lags:", E["lags"], "deriva:", E["deriva"])
rot = p["rot"]
y, aj, i12, meta = E["y"], E["ajuste"], E["i12_obs"], E["meta_obs"]
res = [(a - b) if (a is not None and b is not None) else None for a, b in zip(y, aj)]
r_ok = np.array([r for r in res if r is not None])
print(f"\nresíduos: n={len(r_ok)} média={r_ok.mean():.3f} dp={r_ok.std(ddof=1):.3f}")
print("\ntri      y      ajuste  resid   i12    meta")
for k in range(len(rot) - 14, len(rot)):
    f = lambda v: "   —  " if v is None else f"{v:6.2f}"
    print(rot[k], f(y[k]), f(aj[k]), f(res[k]), f(i12[k]), f(meta[k]))
ult8 = [r for r in res[-9:] if r is not None][-8:]
print("\núltimos 8 resíduos:", [round(r, 2) for r in ult8], "positivos:", sum(r > 0 for r in ult8),
      "soma:", round(sum(ult8), 2))
# percentil do último resíduo na amostra
last = [r for r in res if r is not None][-1]
print(f"último resíduo {last:.3f}, pctl {100*(r_ok < last).mean():.0f}")
e1, e2 = E["mediana"]["e1"], E["mediana"]["e2"]
for i12v in [4.58, 5.28, 4.85, 4.33, 4.08]:
    print(f"repouso com I12={i12v}: {(e2*i12v + (1-e1-e2)*3.0)/(1-e1):.2f}")
# 4T26 de um passo com o 3T26 observado
for i12v in [5.28]:
    for e_prev in [4.37]:
        print(f"E(4T26) = {e1:.3f}*{e_prev} + {e2:.3f}*{i12v} + {1-e1-e2:.3f}*3 = {e1*e_prev+e2*i12v+(1-e1-e2)*3:.3f}")

# Que multiplicador de e1 (e de e2) zera o viés dos resíduos de um passo nos últimos 8 trimestres
# (2024T4–2026T3)? Mesma conta do ajuste: E^ = e1*y(t-1) + e2*i12(t) + (1-e1-e2)*meta(t).
print("\nviés médio dos resíduos de um passo, 2024T4–2026T3, por multiplicador")
idx = list(range(len(rot) - 8, len(rot)))
print("  checagem (m=1 contra o ajuste do retrato):",
      round(np.mean([y[k] - aj[k] for k in idx]), 3),
      round(np.mean([y[k] - (e1*y[k-1] + e2*i12[k] + (1-e1-e2)*meta[k]) for k in idx]), 3))
for m1 in [1.0, 1.1, 1.2, 1.3, 1.4]:
    for m2 in [1.0, 1.3]:
        a1, a2 = e1 * m1, e2 * m2
        rr = [y[k] - (a1*y[k-1] + a2*i12[k] + (1-a1-a2)*meta[k]) for k in idx]
        print(f"  e1×{m1:.1f} (={a1:.3f}) e2×{m2:.1f} (={a2:.3f}) peso meta {1-a1-a2:.3f}: "
              f"viés {np.mean(rr):+.3f}, positivos {sum(r>0 for r in rr)}/8")

# Decomposição do 4T26 do cenário base: o que cada termo contribui, e contra ficar parado em 4,37
e_prev, i12_4t = 4.37, 5.28
print("\n4T26 base, por termo:",
      f"inércia {e1*e_prev:.2f} · IPCA 12m {e2*i12_4t:.2f} · meta {(1-e1-e2)*3.0:.2f} · soma {e1*e_prev+e2*i12_4t+(1-e1-e2)*3.0:.2f}")
print(f"contra 4,37: puxão da meta {(1-e1-e2)*(3.0-e_prev):+.2f} · empurrão do IPCA {e2*(i12_4t-e_prev):+.2f}")
