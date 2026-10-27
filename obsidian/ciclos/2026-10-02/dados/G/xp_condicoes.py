"""Expectativas, ciclo 2026-10-02: o tamanho das condições de cauda usadas em xp_cenarios_r1.py
(exógenas fora da tutela, só para medir), contra o último valor do simulador (3T26)."""
ult = {"icbr_agr_usd": 200.53, "fiscal": 131.21}
for k, v in (("icbr_agr_usd", 230.6), ("icbr_agr_usd", 180.5), ("fiscal", 200.0)):
    print(k, v, "contra", ult[k], "=", round(100 * (v / ult[k] - 1), 1), "%", "| Δ", round(v - ult[k], 1))
# diferenças entre o caminho sem revisão da pesquisa e o modelo base, por trimestre
m = {"4T26": 4.56, "1T27": 4.36, "2T27": 4.17, "3T27": 4.02, "4T27": 3.86, "1T28": 3.73}
b = {"4T26": 4.16, "1T27": 3.97, "2T27": 3.78, "3T27": 3.67, "4T27": 3.59, "1T28": 3.52}
up = {"4T26": 4.39, "1T27": 4.33, "2T27": 4.18, "3T27": 4.10, "4T27": 4.04, "1T28": 3.97}
print("pesquisa sem revisão − modelo base:", {q: round(m[q] - b[q], 2) for q in m})
print("modelo com e1×1,15 e e2×1,30 − modelo base:", {q: round(up[q] - b[q], 2) for q in m})
print("modelo base − meta:", {q: round(b[q] - 3.0, 2) for q in m})

# pesos da meta com os multiplicadores, e diferenças citadas no texto
e1, e2 = 0.5811847410237976, 0.16174547108641338
print("peso da meta: base", round(1 - e1 - e2, 3), "| e1×1,15 e2×1,30", round(1 - 1.15 * e1 - 1.30 * e2, 3),
      "| e1×0,85 e2×0,75", round(1 - 0.85 * e1 - 0.75 * e2, 3))
print("queda necessária no 4T26: 4,6475 − 4,163 =", round(4.6475 - 4.163, 2))
print("QPC 1T28 − Copom 1T28:", round(4.00 - 3.2, 2), "| Focus 2028 − Copom:", round(3.80 - 3.2, 2))
