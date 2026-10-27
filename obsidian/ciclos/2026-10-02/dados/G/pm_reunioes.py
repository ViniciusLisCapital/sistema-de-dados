"""pm, rodada 1: a trajetória reunião a reunião (julgamento do agente) e a distribuição da Selic no
fechamento de cada trimestre que ela implica.

A árvore é uma cadeia de Markov no ÚLTIMO PASSO decidido (estado = passo da reunião anterior).
As probabilidades de transição são julgamento (report §1 e §2, Q1), por fase:
  - 282ª (04/11/26): parte do estado "corte de 25" (a 281ª cortou 25).
  - 283ª a 285ª (dez/26 a mar/27): pausa provável enquanto o choque do petróleo não devolve.
  - 286ª em diante (abr/27 a dez/27, e duas reuniões supostas no 1T28): retomada gradual se o
    choque devolver; alta só com segunda ordem.
Calendário: pm_copom_calendario (A/). O 1T28 não está no calendário oficial: supõem-se duas reuniões.
Saída: a probabilidade de cada passo por reunião (incondicional) e, para cada trimestre, a
distribuição da Selic no fechamento, a média, e a massa em faixas dadas.
"""
from collections import defaultdict
from pathlib import Path

import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"
cal = pd.read_csv(A / "pm_copom_calendario.csv.gz", parse_dates=["date"])
reun = [d for d in cal.date if pd.Timestamp("2026-10-02") < d <= pd.Timestamp("2027-12-31")]
reun = [d.date().isoformat() for d in reun] + ["2028-01-26 (suposta)", "2028-03-15 (suposta)"]

S0, SELIC0 = -25, 13.75

# transições: {estado (último passo): {passo: prob}}
T_NOV = {-25: {0: .55, -25: .39, -50: .01, 25: .05}}
T_PAUSA = {0: {0: .78, -25: .14, -50: .00, 25: .08},
           -25: {0: .55, -25: .40, -50: .03, 25: .02},
           -50: {0: .30, -25: .40, -50: .30, 25: .00},
           25: {0: .50, -25: .00, -50: .00, 25: .50},
           50: {0: .50, -25: .00, -50: .00, 25: .50}}
T_RETOMADA = {0: {0: .62, -25: .30, -50: .03, 25: .05},
              -25: {0: .30, -25: .62, -50: .05, 25: .03},
              -50: {0: .15, -25: .45, -50: .40, 25: .00},
              25: {0: .45, -25: .00, -50: .00, 25: .50, 50: .05},
              50: {0: .40, -25: .00, -50: .00, 25: .55, 50: .05}}


def trans(k):
    if k == 0:
        return T_NOV
    if k <= 3:
        return T_PAUSA
    return T_RETOMADA


for T in (T_NOV, T_PAUSA, T_RETOMADA):
    for st, row in T.items():
        assert abs(sum(row.values()) - 1) < 1e-9, (st, row)

# distribuição conjunta (estado, selic)
dist = {(S0, SELIC0): 1.0}
por_reuniao, por_data = [], {}
for k, d in enumerate(reun):
    T = trans(k)
    nova, passos = defaultdict(float), defaultdict(float)
    for (st, sel), p in dist.items():
        for passo, q in T[st].items():
            if q == 0:
                continue
            nova[(passo, round(sel + passo / 100, 2))] += p * q
            passos[passo] += p * q
    dist = dict(nova)
    por_reuniao.append((d, dict(passos)))
    m = defaultdict(float)
    for (_, sel), p in dist.items():
        m[sel] += p
    por_data[d] = dict(m)

print("== passo por reunião (incondicional, %) ==")
for d, ps in por_reuniao:
    print(d, {f"{k:+d}": round(100 * v, 1) for k, v in sorted(ps.items())})

fech = {"4T26": "2026-12-09", "1T27": "2027-03-17", "2T27": "2027-06-16", "3T27": "2027-09-22",
        "4T27": "2027-12-08", "1T28": "2028-03-15 (suposta)"}
faixas = {"4T26": (13.00, 13.50), "1T27": (12.75, 13.50), "2T27": (12.50, 13.50),
          "3T27": (12.25, 13.25), "4T27": (12.00, 13.00), "1T28": (11.75, 13.00)}
print("\n== Selic no fechamento do trimestre ==")
for q, d in fech.items():
    m = por_data[d]
    media = sum(s * p for s, p in m.items())
    lo, hi = faixas[q]
    pf = sum(p for s, p in m.items() if lo <= s <= hi)
    pu = sum(p for s, p in m.items() if s > hi)
    pd_ = sum(p for s, p in m.items() if s < lo)
    acum = 0
    med = None
    for s in sorted(m):
        acum += m[s]
        if med is None and acum >= .5:
            med = s
    up_r, dn_r = round(100 * pu), round(100 * pd_)
    print(q, "média", round(media, 2), "mediana", med, "| faixa", lo, "a", hi,
          f"P {100 - up_r - dn_r} · up {up_r} · down {dn_r} · assimetria {(up_r - dn_r) / 100:+.2f}",
          f"| P(>=14,00) {100*sum(p for s, p in m.items() if s >= 14):.0f}")
    print("   ", {s: round(100 * p, 1) for s, p in sorted(m.items()) if p >= .005})


def arredonda_100(d):
    """Inteiros que somam 100, pelo maior resto."""
    base = {k: int(100 * v) for k, v in d.items()}
    falta = 100 - sum(base.values())
    for k in sorted(d, key=lambda k: 100 * d[k] - base[k], reverse=True)[:falta]:
        base[k] += 1
    return base


print("\n== passo por reunião, inteiros que somam 100 (para a tabela do report) ==")
for d, ps in por_reuniao[:4]:
    print(d, {f"{k:+d}": v for k, v in sorted(arredonda_100(ps).items())})
print("\n== Selic no fechamento, inteiros que somam 100 ==")
for q in ["4T26", "1T27"]:
    m = {s: p for s, p in por_data[fech[q]].items()}
    print(q, dict(sorted(arredonda_100(m).items())))
for q in ["4T26", "1T27"]:
    m = por_data[fech[q]]
    print(q, "P(<=13,00):", round(100 * sum(p for s, p in m.items() if s <= 13.0)),
          " P(>=14,00):", round(100 * sum(p for s, p in m.items() if s >= 14.0)))
