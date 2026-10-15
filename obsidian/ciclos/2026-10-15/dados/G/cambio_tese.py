"""G · câmbio · ciclo 2026-10-15: da saída do modelo à tabela da tese.

Lê `cambio_cenarios_saida.json` (gravado por cambio_cenarios.py) e faz:
  1. a faixa base: a central (modelo, base) ± 0,75 desvio-padrão, em log, onde o desvio
     junta o erro da equação do câmbio acumulado (σ = 3,63% por trimestre, raiz de h) com a
     incerteza dos pesos (a faixa de 90% do posterior lida como ±1,645 desvio); arredondada
     a R$ 0,05;
  2. as caudas com tempero: worst = modelo com o CDS × 1,2, mais os fatores (ii)
     (posicionamento +2% no 4T26 e +1% no 1T27; BC −1% no 4T26 e no 1T27);
     best = modelo com o CDS × 1,2;
  3. confere que os pontos das caudas caem fora da faixa base;
  4. Pbc − Pwc, das probabilidades escolhidas pelo agente;
  5. a PTAX de hoje contra a central do 4T26.
"""
import json
import math
import sys
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
G = Path(__file__).resolve().parent
A = G.parent / "A"
TRI = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
SIGMA_EQ = 3.6344521208411504          # erro da equação do câmbio, % por trimestre (retrato do ciclo)
K = 0.75                                # meia largura da faixa base, em desvios
POSIC = [0.02, 0.01, 0, 0, 0, 0]        # (ii) posicionamento, worst
BC = [-0.01, -0.01, 0, 0, 0, 0]         # (ii) o BC no mercado, worst
# probabilidades do agente, em %: (base, worst, best)
PROB = {"4T26": (48, 22, 30), "1T27": (48, 26, 26), "2T27": (47, 28, 25),
        "3T27": (46, 30, 24), "4T27": (45, 31, 24), "1T28": (45, 31, 24)}

s = json.loads((G / "cambio_cenarios_saida.json").read_text(encoding="utf-8"))
base, worst, best = s["base"], s["worst"], s["best"]


def r05(x):
    return round(x * 20) / 20


print("| Tri | central | σ eq | σ pesos | σ total | faixa exata | faixa 0,05 | worst modelo | worst ×1,2 | worst c/ tempero | best modelo | best ×1,2 | fora? | P base/worst/best | soma | Pbc−Pwc |")
for j, t in enumerate(TRI):
    c = base["ptax"][j]
    s_eq = SIGMA_EQ * math.sqrt(j + 1) / 100
    s_w = math.log(base["ptax_hi"][j] / base["ptax_lo"][j]) / (2 * 1.645)
    s_t = math.sqrt(s_eq ** 2 + s_w ** 2)
    lo, hi = c * math.exp(-K * s_t), c * math.exp(K * s_t)
    lo5, hi5 = r05(lo), r05(hi)
    wm, wx = worst["ptax"][j], worst["ptax_mult"][j]
    wt = wx * (1 + POSIC[j]) * (1 + BC[j])
    bm, bx = best["ptax"][j], best["ptax_mult"][j]
    fora = (wt > hi5) and (bx < lo5)
    pb, pw, pc = PROB[t]
    print(f"| {t} | {c:.3f} | {100*s_eq:.2f}% | {100*s_w:.2f}% | {100*s_t:.2f}% | {lo:.3f}–{hi:.3f} | "
          f"{lo5:.2f}–{hi5:.2f} | {wm:.3f} | {wx:.3f} | {wt:.3f} | {bm:.3f} | {bx:.3f} | {fora} | "
          f"{pb}/{pw}/{pc} | {pb+pw+pc} | {(pc-pw)/100:+.2f} |")

print()
print("Selic média e IPCA 12m por cenário (modelo, sem multiplicador):")
for nome in ("base", "worst", "best"):
    print(f"  {nome:5s} Selic", [f"{v:.2f}" for v in s[nome]["selic"]],
          " IPCA12m", [f"{v:.2f}" for v in s[nome]["ipca_12m"]])

print()
print("Variação da central do modelo contra o 3T26 observado (5,1809) e contra a PTAX de hoje:")
ptax = pd.read_csv(A / "cmb_ptax.csv.gz", parse_dates=["date"])
ptax = ptax[ptax["name"] == "ptax_venda"].set_index("date")["value"].sort_index()
hoje = ptax.iloc[-1]
for j, t in enumerate(TRI):
    c = base["ptax"][j]
    print(f"  {t}: central {c:.3f} · {100*(c/5.1809-1):+.2f}% contra 3T26 · {100*(c/hoje-1):+.2f}% contra {hoje:.4f} ({ptax.index[-1].date()})")
print()
for nome, k in (("worst", "ptax_mult"), ("best", "ptax_mult")):
    print(f"  {nome} ×1,2 contra a central:",
          [f"{100*(s[nome][k][j]/base['ptax'][j]-1):+.1f}%" for j in range(6)])
print("  worst c/ tempero contra a central:",
      [f"{100*(worst['ptax_mult'][j]*(1+POSIC[j])*(1+BC[j])/base['ptax'][j]-1):+.1f}%" for j in range(6)])
print("  efeito do ×1,2 sobre o modelo, worst:",
      [f"{100*(worst['ptax_mult'][j]/worst['ptax'][j]-1):+.2f}%" for j in range(6)],
      " best:", [f"{100*(best['ptax_mult'][j]/best['ptax'][j]-1):+.2f}%" for j in range(6)])

print()
print("Saídas arredondadas a duas casas (PTAX) para o report:")
for nome in ("base", "worst", "best"):
    for k in ("ptax", "ptax_mult", "ptax_lo", "ptax_hi"):
        if k in s[nome]:
            print(f"  {nome:5s} {k:9s}", [f"{v:.2f}" for v in s[nome][k]], [f"{v:.4f}" for v in s[nome][k]])
print("  worst c/ tempero", [f"{worst['ptax_mult'][j]*(1+POSIC[j])*(1+BC[j]):.2f}" for j in range(6)])

# massa de uma normal entre −K e +K desvios: o que a faixa base cobriria só com o erro da equação
print(f"\nP(|z| < {K}) numa normal = {math.erf(K / math.sqrt(2)):.3f}")
