"""G pm: a distribuição da Selic de fechamento de cada trimestre, a partir do julgamento do agente
reunião a reunião (ciclo 2026-10-15). O julgamento entra como probabilidades de cada passo,
condicionadas ao estado do ciclo (cortando, pausado, subindo); o G só agrega: probabilidade
incondicional de cada passo em cada reunião, a distribuição do fechamento por trimestre e a
probabilidade da faixa base e das caudas em torno da central do modelo (pm_cenarios.py)."""
from collections import defaultdict

SELIC0 = 13.75
REUNIOES = [("04/11/26", "4T26"), ("09/12/26", "4T26"), ("27/01/27", "1T27"), ("17/03/27", "1T27"),
            ("28/04/27", "2T27"), ("16/06/27", "2T27"), ("04/08/27", "3T27"), ("22/09/27", "3T27"),
            ("27/10/27", "4T27"), ("08/12/27", "4T27"),
            ("1ª de 2028 (fora do calendário)", "1T28"), ("2ª de 2028 (fora do calendário)", "1T28")]

# Julgamento: passo (p.b.) -> probabilidade, por estado do ciclo
NOV = {"C": {-25: .60, 0: .37, -50: .03}}
DEZ = {"C": {-25: .65, 0: .33, -50: .02}, "P": {0: .68, -25: .30, +25: .02}}
DEPOIS = {"C": {-25: .75, 0: .22, -50: .03}, "P": {0: .55, -25: .40, +25: .05}, "H": {+25: .50, 0: .50}}
PISO = {-25: .60, 0: .38, -50: .02}   # cortando com a Selic já em 12,00 ou menos: o ciclo desacelera


def tabela(i, estado, nivel):
    if i == 0:
        return NOV[estado]
    if i == 1:
        return DEZ[estado]
    if estado == "C" and nivel <= 12.00:
        return PISO
    return DEPOIS[estado]


def novo_estado(estado, passo):
    if passo < 0:
        return "C"
    if passo > 0:
        return "H"
    return "P"


dist = {("C", SELIC0): 1.0}
passos = []
fecha = {}
for i, (reu, tri) in enumerate(REUNIOES):
    nd, p_passo = defaultdict(float), defaultdict(float)
    for (est, niv), pr in dist.items():
        for passo, q in tabela(i, est, niv).items():
            nd[(novo_estado(est, passo), round(niv + passo / 100, 2))] += pr * q
            p_passo[passo] += pr * q
    dist = dict(nd)
    passos.append((reu, tri, dict(p_passo)))
    pmf = defaultdict(float)
    for (_, niv), pr in dist.items():
        pmf[niv] += pr
    fecha[tri] = dict(pmf)   # a última reunião do trimestre sobrescreve: é o fechamento

print("Probabilidade incondicional de cada passo, por reunião (p.b.: %):")
for reu, tri, pp in passos:
    print(f"  {reu} ({tri}): " + " · ".join(f"{k:+d} {v:.0%}" for k, v in sorted(pp.items())))

CENTRAL = {"4T26": 12.47, "1T27": 12.14, "2T27": 11.86, "3T27": 11.62, "4T27": 11.41, "1T28": 11.22}
print("\nFechamento por trimestre: média, moda, e a distribuição")
for tri, pmf in fecha.items():
    media = sum(k * v for k, v in pmf.items())
    moda = max(pmf, key=pmf.get)
    acum, q = 0, {}
    for k in sorted(pmf):
        acum += pmf[k]
        for p in (0.05, 0.25, 0.5, 0.75, 0.95):
            if p not in q and acum >= p:
                q[p] = k
    print(f"  {tri}: média {media:.2f} · moda {moda:.2f} · p5 {q[0.05]:.2f} p25 {q[0.25]:.2f} p50 {q[0.5]:.2f} "
          f"p75 {q[0.75]:.2f} p95 {q[0.95]:.2f}")
    print("     " + " · ".join(f"{k:.2f} {v:.1%}" for k, v in sorted(pmf.items()) if v >= 0.005))
    c = CENTRAL[tri]
    lo, hi = c - 0.375, c + 0.375
    base = sum(v for k, v in pmf.items() if lo <= k <= hi)
    worst = sum(v for k, v in pmf.items() if k > hi)
    best = sum(v for k, v in pmf.items() if k < lo)
    nos = [k for k in sorted(pmf) if lo <= k <= hi] or ["—"]
    print(f"     central {c:.2f}: faixa base (fechamentos entre {lo:.3f} e {hi:.3f}: {nos[0]} a {nos[-1]}) {base:.1%} · "
          f"worst (acima) {worst:.1%} · best (abaixo) {best:.1%} · Pbc−Pwc {best - worst:+.2f}")
