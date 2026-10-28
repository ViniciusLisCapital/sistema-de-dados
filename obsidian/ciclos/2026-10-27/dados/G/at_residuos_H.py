"""Atividade, sobre a (H): o que a curva IS do Modelo Estrutural errou na amostra recente.
Lê o retrato do modelo do ciclo (dados/A/modelo_estrutural.json via modelo.carregar).
- resíduo de um passo: hiato publicado (edição 2026-09) - ajuste de um passo da (H) com os pesos da mediana;
- caminho dinâmico: a (H) rodada sozinha a partir de 2T25 (e 4T24), com o aperto observado, contra o hiato publicado;
- aperto monetário (Selic média - rr_10a - meta) nos últimos 8 trimestres."""
import numpy as np
from analytics.agent_system import modelo

sim = modelo.carregar("2026-10-27")
p = sim["p"] if "p" in sim else sim
H = p["eq"]["H"]
rot = p["rot"]; y = np.array(H["y"], float); aj = np.array(H["ajuste"], dtype=float)
ap = np.array(H["gap_pub"], float)
h1, h2 = H["mediana"]["h1"], H["mediana"]["h2"]
res = y - aj
i1 = H["est_i1"]
print(f"h1={h1:.3f} h2={h2:.4f} sigma(mediana)={H['mediana']['sigma']:.3f}")
print("tri    hiato  ajuste  residuo  aperto")
for i in range(len(rot) - 10, len(rot)):
    print(f"{rot[i]}  {y[i]:6.2f}  {aj[i]:6.2f}  {res[i]:7.2f}  {ap[i]:6.2f}")
ok = ~np.isnan(res)
idx = [i for i in range(len(rot)) if ok[i] and not (rot[i].startswith("2008") or rot[i].startswith("2009") or rot[i].startswith("2020"))]
r = res[idx]
print(f"\nresiduo de um passo, amostra sem 2008-09 e 2020: n={len(r)} dp={r.std(ddof=1):.3f} media={r.mean():.3f}")
print(f"residuo, todos os trimestres com ajuste: n={ok.sum()} dp={np.nanstd(res, ddof=1):.3f}")
last8 = res[len(rot) - 8:]
print("ultimos 8 residuos:", np.round(last8, 2), " positivos:", int((last8 > 0).sum()), " media:", round(float(np.nanmean(last8)), 3))
r_ok = res[ok]
print("autocorrelacao de ordem 1 do residuo: %.2f" % np.corrcoef(r_ok[1:], r_ok[:-1])[0, 1])
# sequencias de 6+ residuos do mesmo sinal na amostra
sinais = np.sign(r_ok); runs = []; cur = 1
for a, b in zip(sinais[:-1], sinais[1:]):
    if a == b: cur += 1
    else: runs.append(cur); cur = 1
runs.append(cur)
print("maior sequencia de residuos do mesmo sinal:", max(runs), "; sequencia atual:", cur)

for ini in ["2024T4", "2025T2"]:
    k = rot.index(ini)
    g = y[k]; path = []
    for i in range(k + 1, len(rot)):
        g = h1 * g + h2 * ap[i - 1]
        path.append((rot[i], g, y[i]))
    print(f"\nH sozinha a partir de {ini} (hiato {y[k]:.2f}), aperto observado:")
    for t, gm, gp in path:
        print(f"  {t}: modelo {gm:6.2f}  publicado {gp:6.2f}  diferenca {gp-gm:+.2f}")

# erro de projecao da (H) sozinha, h passos, com o sigma da mediana (choques independentes)
s = H["mediana"]["sigma"]
acc = 0.0
print("\nDP do erro de projecao da (H), so pelo choque da equacao (sigma mediano), por trimestre a frente:")
for k in range(1, 7):
    acc += h1 ** (2 * (k - 1))
    print(f"  {k}: {s*np.sqrt(acc):.2f}")
s2 = r.std(ddof=1); acc = 0.0
print("idem com o dp do residuo sem crises:")
for k in range(1, 7):
    acc += h1 ** (2 * (k - 1))
    print(f"  {k}: {s2*np.sqrt(acc):.2f}")

# que multiplicador em h2 faria a (H), rodada desde 2025T2 com o aperto observado, acertar o 3T26 publicado?
k = rot.index("2025T2"); kT = rot.index("2026T3")
n = kT - k
termo_ini = h1 ** n * y[k]
soma_ap = sum(h1 ** (kT - 1 - j) * ap[j] for j in range(k, kT))
m = (y[kT] - termo_ini) / (h2 * soma_ap)
print(f"\nmultiplicador de h2 que acerta o 3T26 a partir de 2025T2: {m:.2f} (h2 efetivo {h2*m:.4f}; limite do posterior -0,023 = x{-0.023/h2:.2f})")
