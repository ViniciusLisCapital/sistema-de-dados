"""fi (rodada 2): diferenças entre os caminhos deste agente (r1 → r2) e os dos subordinados (PM em `rr_10a`;
o componente global do externo no CDS), e as diferenças de Selic no modelo entre os caminhos de `rr_10a`
(números de saída de fi_r2_cenarios)."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
rr_r1 = [7.70, 7.80, 7.70, 7.60, 7.55, 7.50]
rr_r2 = [7.72, 8.00, 8.00, 7.95, 7.90, 7.85]
rr_pm = [7.76, 8.05, 8.05, 8.05, 8.05, 8.05]
cds_r1 = [140, 140, 138, 135, 135, 135]
cds_r2 = [140, 143, 140, 137, 134, 130]
cds_ex = [141, 145, None, None, None, 120]   # componente global do externo (r1): ~141, ~145, ..., ~120
sel_fim = {"r2": [13.45, 13.28, 12.99, 12.71, 12.47, 12.26], "r1": [13.34, 13.03, 12.67, 12.36, 12.12, 11.91],
           "pm_path": [13.50, 13.33, 13.07, 12.84, 12.64, 12.46], "pm_tese": [13.49, 13.32, 13.04, 12.80, 12.58, 12.39]}
f = lambda a, b: [None if (x is None or y is None) else round(x - y, 2) for x, y in zip(a, b)]
print("rr_10a: PM − r1:", dict(zip(T, f(rr_pm, rr_r1))))
print("rr_10a: PM − r2:", dict(zip(T, f(rr_pm, rr_r2))))
print("rr_10a: r2 − r1:", dict(zip(T, f(rr_r2, rr_r1))))
print("rr_10a r2: 1T28 − 1T27:", round(rr_r2[5] - rr_r2[1], 2), "· 1T27 − 3T26 (7,84):", round(rr_r2[1] - 7.84, 2))
print("CDS: r2 − r1:", dict(zip(T, f(cds_r2, cds_r1))))
print("CDS: r2 − externo global:", dict(zip(T, f(cds_r2, cds_ex))))
print("CDS r2: variação por trimestre (fechamento), a partir de 3T26 = 131:",
      dict(zip(T, f(cds_r2, [131] + cds_r2[:-1]))))
print("Selic fim (modelo): r2 − r1:", dict(zip(T, f(sel_fim["r2"], sel_fim["r1"]))))
print("Selic fim (modelo): caminho PM − r2:", dict(zip(T, f(sel_fim["pm_path"], sel_fim["r2"]))))
print("Selic fim (modelo r2) − tese PM:", dict(zip(T, f(sel_fim["r2"], sel_fim["pm_tese"]))))
print("Selic fim (P1) − tese PM, para comparar:", dict(zip(T, f(sel_fim["r1"], sel_fim["pm_tese"]))))
# contas citadas no texto da seção 3.1 e de F5
print("Selic média 1T27: base − downside:", round(13.42 - 12.72, 2))
print("rr_10a upside 2T27 (9,10) − máx 10 anos (8,20):", round(9.10 - 8.20, 2), "· − 3T26 (7,84):", round(9.10 - 7.84, 2))
print("Prêmio sobre o juro real de política do Focus (PM): 8,00 − 6,02 =", round(8.00 - 6.02, 2), "· 8,00 − 6,28 =", round(8.00 - 6.28, 2))
