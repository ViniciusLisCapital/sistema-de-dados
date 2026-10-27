"""Expectativas, ciclo 2026-10-02: a equação (E) do cenário base, termo a termo, e o efeito da partida
pela média (e não pelo nível do fim) do 3T26.

E(t) = e1·E(t−1) + e2·I12(t) + (1 − e1 − e2)·Meta(t), com os pesos da mediana e os caminhos do
cenário base do modelo (padrão do simulador). Conferido contra a central de focus_12m."""
from analytics.agent_system import modelo
import pandas as pd
from pathlib import Path

sim = modelo.carregar("2026-10-02")
res = modelo.rodar(sim, faixa=False)
e1, e2 = 0.5811847410237976, 0.16174547108641338
E = [res["partida"]["focus_12m"]] + res["endogenas"]["focus_12m"]["central"][:6]
I = res["endogenas"]["ipca_12m"]["central"][:6]
M = res["entradas"]["meta_12m"]["caminho"]
print("meta caminho (início):", M[:8])
# a janela do caminho começa no primeiro projetado? alinhar: usa o tamanho
meta = M[-len(res["endogenas"]["focus_12m"]["central"]):][:6] if len(M) >= 12 else M[:6]
T = res["trimestres"][:6]
for j in range(6):
    a, b, c = e1 * E[j], e2 * I[j], (1 - e1 - e2) * meta[j]
    print(T[j], "e1·E(t−1)=", round(a, 3), "e2·I12=", round(b, 3), "(1−e1−e2)·Meta=", round(c, 3),
          "soma", round(a + b + c, 3), "modelo", round(E[j + 1], 3), "| E(t-1)", round(E[j], 3), "I12", round(I[j], 2), "Meta", meta[j])
print("peso da meta:", round(1 - e1 - e2, 3), "| repouso com I12 do 1T28:", round((e2 * I[5] + (1 - e1 - e2) * meta[5]) / (1 - e1), 2))

A = Path(__file__).resolve().parent.parent / "A"
v = pd.read_csv(A / "expc_focus__inflacao.csv.gz", parse_dates=["date"])
v = v[(v.indicador == "IPCA") & (v.horizonte == "12m") & (v.suavizada == "S") & (v.base_calculo == 0)].set_index("date")["mediana"].sort_index()
q3 = v["2026-07-01":"2026-09-30"]
ult_div = v[:"2026-09-25"].iloc[-1]
for nome, nivel in (("última divulgada em 02/10 (25/09)", ult_div), ("última do 3T26 (30/09)", q3.iloc[-1])):
    g = nivel - q3.mean()
    print(nome, round(nivel, 3), "− média 3T26", round(q3.mean(), 3), "=", round(g, 3),
          "| efeito via e1 no 4T26:", round(e1 * g, 2), "| e1^k·g, k=1..6:", [round(e1 ** k * g, 2) for k in range(1, 7)])
