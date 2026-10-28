"""A distribuição da Selic por reunião e no fechamento de cada trimestre, como mistura de três
regimes com passos por reunião (o julgamento deste agente, ciclo 2026-10-27, rodada 1).
Faixas base e probabilidades de cauda contra a central do modelo (pm_cenarios.py, base).

Regimes: C reversão do choque de 26/10 (cortes retomados), P pausa longa, H ciclo de alta.
Calendário: pm_copom_calendario até 08/12/2027; 1T28 com duas reuniões (2 por trimestre em
todos os trimestres de 2022 a 2027, mesmo arquivo)."""
from collections import defaultdict

S0 = 13.75
REUN = ["04/11/26", "09/12/26", "27/01/27", "17/03/27", "28/04/27", "16/06/27",
        "04/08/27", "22/09/27", "27/10/27", "08/12/27", "1T28 a", "1T28 b"]
FECHA = {"4T26": 1, "1T27": 3, "2T27": 5, "3T27": 7, "4T27": 9, "1T28": 11}  # índice da última reunião do trimestre
PESO = {"C": 0.20, "P": 0.45, "H": 0.35}
def rep(d, n): return [d] * n
PASSOS = {
    "C": [{-25: .40, 0: .60}] + rep({-25: .70, 0: .25, -50: .05}, 9) + rep({-25: .50, 0: .50}, 2),
    "P": [{0: .88, -25: .07, 25: .05}, {0: .85, 25: .10, -25: .05}] + rep({0: .80, -25: .12, 25: .08}, 2)
         + rep({0: .55, -25: .40, 25: .05}, 2) + rep({-25: .60, 0: .40}, 4) + rep({-25: .55, 0: .45}, 2),
    "H": [{0: .65, 25: .20, 50: .15}, {25: .35, 50: .35, 0: .30}, {25: .35, 50: .30, 0: .35},
          {25: .35, 50: .15, 0: .50}, {25: .25, 0: .75}, {0: .85, 25: .15}] + rep({0: .85, -25: .15}, 2)
         + rep({0: .65, -25: .35}, 2) + rep({0: .55, -25: .45}, 2),
}
for k, v in PASSOS.items():
    assert len(v) == len(REUN) and all(abs(sum(d.values()) - 1) < 1e-9 for d in v), k

# distribuição conjunta: nível (em p.b.) depois de cada reunião
marg_passo = [defaultdict(float) for _ in REUN]
nivel = [defaultdict(float) for _ in REUN]
for reg, w in PESO.items():
    dist = {round(S0 * 100): w}
    for i, d in enumerate(PASSOS[reg]):
        novo = defaultdict(float)
        for lv, p in dist.items():
            for st, q in d.items():
                novo[lv + st] += p * q
                marg_passo[i][st] += p * q
        dist = novo
        for lv, p in dist.items():
            nivel[i][lv] += p

print("Passo por reunião (probabilidade, %), marginal da mistura:")
for i, r in enumerate(REUN[:4]):
    print(" ", r, {f"{k:+d}": round(v * 100, 1) for k, v in sorted(marg_passo[i].items())},
          "· média do nível", round(sum(l * p for l, p in nivel[i].items()) / 100, 2))
for i, r in enumerate(REUN[:4]):
    print("  nível depois de", r, {f"{l/100:.2f}": round(p * 100, 1) for l, p in sorted(nivel[i].items()) if p > 0.004})

CENTRAL = {"4T26": 13.49, "1T27": 13.32, "2T27": 13.04, "3T27": 12.80, "4T27": 12.58, "1T28": 12.39}
FAIXA = {"4T26": (13.45, 13.80), "1T27": (13.25, 14.05), "2T27": (12.75, 14.05),
         "3T27": (12.50, 14.05), "4T27": (12.25, 14.05), "1T28": (12.00, 14.05)}
print("\nFechamento do trimestre:")
for q, i in FECHA.items():
    d = nivel[i]
    lo, hi = FAIXA[q]
    pf = sum(p for l, p in d.items() if lo <= l / 100 <= hi)
    pu = sum(p for l, p in d.items() if l / 100 > hi)
    pd_ = sum(p for l, p in d.items() if l / 100 < lo)
    media = sum(l * p for l, p in d.items()) / 100
    acum, med = 0, None
    for l in sorted(d):
        acum += d[l]
        if med is None and acum >= .5: med = l / 100
    p10 = next(l for l in sorted(d) if sum(d[x] for x in d if x <= l) >= .10) / 100
    p90 = next(l for l in sorted(d) if sum(d[x] for x in d if x <= l) >= .90) / 100
    print(f"  {q} ({REUN[i]}): central {CENTRAL[q]:.2f} · faixa {lo:.2f}-{hi:.2f}: P {pf*100:.1f} · up {pu*100:.1f} · down {pd_*100:.1f}"
          f" · média {media:.2f} · mediana {med:.2f} · p10 {p10:.2f} · p90 {p90:.2f}")
    print("     ", {f"{l/100:.2f}": round(p * 100, 1) for l, p in sorted(d.items()) if p > 0.01})
# por regime, média do nível no fechamento
for reg in PESO:
    dist = {round(S0 * 100): 1.0}; out = {}
    for i, d in enumerate(PASSOS[reg]):
        novo = defaultdict(float)
        for lv, p in dist.items():
            for st, q in d.items():
                novo[lv + st] += p * q
        dist = novo
        if i in FECHA.values():
            out[[q for q, j in FECHA.items() if j == i][0]] = round(sum(l * p for l, p in dist.items()) / 100, 2)
    print("  regime", reg, "média no fechamento:", out)

print("\nAlta e corte por reunião (soma dos passos) e Selic acima de 13,75 depois de cada uma:")
for i, r in enumerate(REUN[:4]):
    up = sum(p for s, p in marg_passo[i].items() if s > 0)
    dn = sum(p for s, p in marg_passo[i].items() if s < 0)
    acima = sum(p for l, p in nivel[i].items() if l > 1375)
    print(f"  {r}: alta {up*100:.1f} · corte {dn*100:.1f} · Selic acima de 13,75 {acima*100:.1f}")
