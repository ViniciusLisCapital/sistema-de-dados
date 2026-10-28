"""Expectativas, rodada 2: as contas pequenas do report contra a central do P1.

Lê A/expc_focus__inflacao.csv.gz e ../../P1.json (a central do P1 para focus_12m).
- 4T26: média das pesquisas já feitas no trimestre e o que as restantes (46 ou 49) teriam de
  marcar em média para o trimestre fechar na central do P1 e nos limites da faixa.
- A trajetória sem revisão da rodada 1 (G xp_trajetoria_pesquisa: 4,47 4,17 3,93 3,88 3,87 3,70)
  menos a central do P1, e menos a central do report da rodada 1 (4,16 3,97 3,78 3,67 3,59 3,52).
- Distância da central do P1 à meta (3,00) em cada trimestre.
"""
import json
from pathlib import Path
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"
P1 = json.loads((Path(__file__).resolve().parents[2] / "P1.json").read_text(encoding="utf-8"))
Q = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
fz = P1["modelo"]["endogenas"]["focus_12m"]
tri = P1["modelo"]["trimestres"]
cp1 = [round(fz["central"][tri.index(q)], 2) for q in Q]
print("central P1:", dict(zip(Q, cp1)))

f = pd.read_csv(A / "expc_focus__inflacao.csv.gz")
s = f[(f.indicador == "IPCA") & (f.horizonte == "12m") & (f.suavizada == "S") & (f.base_calculo == 0)
      & (f.tipo_calculo == "geral")].set_index("date").mediana.sort_index()
s.index = pd.to_datetime(s.index)
q4 = s[s.index >= "2026-10-01"]
n0, m0 = len(q4), q4.mean()
print(f"4T26 até {q4.index[-1].date()}: {n0} pesquisas, média {m0:.3f}")
for alvo in [cp1[0], 4.05, 4.45]:
    for N in (62, 65):
        print(f"  fecha em {alvo:.2f} (N={N}) se as {N-n0} restantes marcarem em média {(N*alvo - n0*m0)/(N-n0):.2f}")

semrev = [4.47, 4.17, 3.93, 3.88, 3.87, 3.70]
cr1 = [4.16, 3.97, 3.78, 3.67, 3.59, 3.52]
for q, a, b, c in zip(Q, semrev, cp1, cr1):
    print(f"{q}: sem revisão {a:.2f} − P1 {b:.2f} = {a-b:+.2f} · − r1 {c:.2f} = {a-c:+.2f} · P1 − r1 = {b-c:+.2f} · P1 − meta = {b-3:+.2f}")

# A (E) no 4T26 do P1, por termo (mediana do posterior; E(3T26) = 4,37 observado, I12 = o do P1)
pe = json.loads((A / "modelo_estrutural.json").read_text(encoding="utf-8"))["p"]["eq"]["E"]["mediana"]
e1, e2 = pe["e1"], pe["e2"]
i12 = P1["modelo"]["endogenas"]["ipca_12m"]["central"][tri.index("4T26")]
print(f"\n(E) 4T26 do P1: inércia {e1:.3f}×4,37 = {e1*4.37:.2f} · IPCA 12m {e2:.3f}×{i12:.2f} = {e2*i12:.2f} · "
      f"meta {1-e1-e2:.3f}×3 = {(1-e1-e2)*3:.2f} · soma {e1*4.37+e2*i12+(1-e1-e2)*3:.2f}")
print(f"contra 4,37: puxão da meta {(1-e1-e2)*(3-4.37):+.2f} · empurrão do IPCA {e2*(i12-4.37):+.2f}")
