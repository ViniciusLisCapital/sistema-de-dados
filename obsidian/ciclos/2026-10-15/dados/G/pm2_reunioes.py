"""pm2: o caminho reunião a reunião do agente (julgamento) convertido em probabilidades por
reunião e em distribuição da Selic no fechamento de cada trimestre; a média do 4T26 que cada
caminho implica; e a contagem de reuniões no 1º trimestre (para o 1T28, fora do calendário).

O julgamento entra como probabilidades de transição do passo (o passo de uma reunião depende do
da anterior), em duas fases. Não há dado aqui além de pm_copom_calendario e pm_copom_reuniao:
o resto é a aritmética do julgamento. Só lê A/.
"""
from collections import defaultdict
from pathlib import Path

import pandas as pd

A = Path(__file__).resolve().parents[1] / "A"
cal = pd.read_csv(A / "pm_copom_calendario.csv.gz")
reu = pd.read_csv(A / "pm_copom_reuniao.csv.gz", parse_dates=["date"])
print("colunas do calendário:", list(cal.columns))
print(cal.tail(12).to_string())

print("\n== 0. Reuniões por 1º trimestre, 2006-2026 (pm_copom_reuniao)")
r = reu[(reu.date >= "2006-01-01")]
cont = r[r.date.dt.quarter == 1].groupby(r.date.dt.year).size()
print(cont.value_counts().to_string())
print("meses:", sorted(set(r[r.date.dt.quarter == 1].date.dt.month)))

# reuniões da janela, com o trimestre de cada uma; 1T28 com duas reuniões supostas (jan e mar)
REUNIOES = [
    ("2026-11-04", "4T26"), ("2026-12-09", "4T26"),
    ("2027-01-27", "1T27"), ("2027-03-17", "1T27"),
    ("2027-04-28", "2T27"), ("2027-06-16", "2T27"),
    ("2027-08-04", "3T27"), ("2027-09-22", "3T27"),
    ("2027-10-27", "4T27"), ("2027-12-08", "4T27"),
    ("2028-01-xx", "1T28"), ("2028-03-xx", "1T28"),
]
PASSOS = [25, 0, -25, -50, -75]

# Fase A (nov/26 a mar/27): IPCA 12m acima do teto, choque do petróleo, guidance de calibração.
FASE_A = {
    25: {25: 0.30, 0: 0.65, -25: 0.05, -50: 0.0, -75: 0.0},
    0: {25: 0.03, 0: 0.52, -25: 0.40, -50: 0.05, -75: 0.0},
    -25: {25: 0.0, 0: 0.25, -25: 0.65, -50: 0.10, -75: 0.0},
    -50: {25: 0.0, 0: 0.05, -25: 0.45, -50: 0.47, -75: 0.03},
    -75: {25: 0.0, 0: 0.05, -25: 0.25, -50: 0.50, -75: 0.20},
}
# Fase B (abr/27 em diante): o IPCA 12m volta para baixo do teto (modelo, 2T27); espaço para acelerar.
FASE_B = {
    25: {25: 0.30, 0: 0.65, -25: 0.05, -50: 0.0, -75: 0.0},
    0: {25: 0.02, 0: 0.55, -25: 0.38, -50: 0.05, -75: 0.0},
    -25: {25: 0.0, 0: 0.30, -25: 0.55, -50: 0.15, -75: 0.0},
    -50: {25: 0.0, 0: 0.05, -25: 0.40, -50: 0.52, -75: 0.03},
    -75: {25: 0.0, 0: 0.05, -25: 0.20, -50: 0.55, -75: 0.20},
}
# Perto do fim do ciclo: com a Selic em 11,00 ou abaixo, o passo desacelera (a Focus põe 10,50 no fim de 2028).
PERTO_FIM = {0: 0.50, -25: 0.40, -50: 0.10}

for M in (FASE_A, FASE_B):
    for k, v in M.items():
        assert abs(sum(v.values()) - 1) < 1e-9, (k, v)


def trans(i, ant, selic):
    if selic <= 11.0:
        return PERTO_FIM
    return (FASE_A if i < 4 else FASE_B)[ant]


# estado: (selic, passo anterior) -> prob
estado = {(13.75, -25): 1.0}
marg = []
fech = {}
for i, (data, tri) in enumerate(REUNIOES):
    novo = defaultdict(float)
    m = defaultdict(float)
    for (s, ant), p in estado.items():
        for passo, q in trans(i, ant, s).items():
            if q == 0:
                continue
            s2 = round(s + passo / 100, 2)
            novo[(s2, passo)] += p * q
            m[passo] += p * q
    estado = dict(novo)
    marg.append((data, tri, dict(m)))
    dist = defaultdict(float)
    for (s, _), p in estado.items():
        dist[s] += p
    fech[tri] = dict(dist)  # sobrescreve: fica a da última reunião do trimestre

print("\n== 1. Probabilidade de cada passo, por reunião (marginal)")
for data, tri, m in marg:
    txt = " · ".join(f"{k:+d}: {v*100:.1f}%" for k, v in sorted(m.items(), reverse=True) if v >= 0.005)
    print(f"{data} ({tri}): {txt}")

MODELO = {"4T26": 12.47, "1T27": 12.13, "2T27": 11.85, "3T27": 11.61, "4T27": 11.39, "1T28": 11.20}
LARG = {"4T26": 0.30, "1T27": 0.40, "2T27": 0.50, "3T27": 0.55, "4T27": 0.60, "1T28": 0.65}

print("\n== 2. Fechamento do trimestre: distribuição, mediana, e probabilidades contra a faixa base em torno da central do modelo")
for tri, dist in fech.items():
    itens = sorted(dist.items())
    acum = 0
    med = None
    for s, p in itens:
        acum += p
        if med is None and acum >= 0.5:
            med = s
    c = MODELO[tri]
    lo, hi = c - LARG[tri], c + LARG[tri]
    # limites na grade de 25 p.b.
    grade_in = [s for s, _ in itens if lo <= s <= hi]
    p_in = sum(p for s, p in itens if lo <= s <= hi)
    p_hi = sum(p for s, p in itens if s > hi)
    p_lo = sum(p for s, p in itens if s < lo)
    media = sum(s * p for s, p in itens)
    print(f"{tri}: central {c:.2f}; faixa {lo:.2f}-{hi:.2f} (pontos da grade dentro: {grade_in}); "
          f"P base {p_in*100:.0f}% · acima {p_hi*100:.0f}% · abaixo {p_lo*100:.0f}% · Pbc-Pwc {p_lo-p_hi:+.2f}; "
          f"mediana {med:.2f}; média {media:.2f}")
    print("     " + " · ".join(f"{s:.2f}: {p*100:.1f}%" for s, p in itens if p >= 0.005))

print("\n== 3. Média do 4T26 que cada caminho de nov/dez implica (dias corridos; a taxa nova vale do dia seguinte à reunião)")
d1 = (pd.Timestamp("2026-11-04") - pd.Timestamp("2026-10-01")).days + 1
d2 = (pd.Timestamp("2026-12-09") - pd.Timestamp("2026-11-04")).days
d3 = (pd.Timestamp("2026-12-31") - pd.Timestamp("2026-12-09")).days
print(f"dias: {d1} a 13,75; {d2} depois de 04/11; {d3} depois de 09/12; total {d1+d2+d3}")
for nov, dez in [(0, 0), (-25, -25), (-50, -50), (-50, -75), (-75, -75), (-100, -100), (-150, -100)]:
    s1 = 13.75 + nov / 100
    s2 = s1 + dez / 100
    media = (13.75 * d1 + s1 * d2 + s2 * d3) / (d1 + d2 + d3)
    print(f"   nov {nov:+d}, dez {dez:+d}: fechamento {s2:.2f}, média do 4T26 {media:.2f}")

print("\n== 4. Caminho de referência a -25 por reunião, fechamento por trimestre")
s = 13.75
for data, tri in REUNIOES:
    s -= 0.25
    print(f"   {data} ({tri}): {s:.2f}")

print("\n== 5. Distâncias: central do modelo contra a Focus e a curva DI (fechamento do trimestre)")
FOCUS = {"4T26": 13.25, "1T27": 13.00, "2T27": 12.62, "3T27": 12.25, "4T27": 12.00}
DI = {"4T26": 13.38, "1T27": 12.99, "2T27": 12.58, "3T27": 12.25, "4T27": 12.13}
for t in FOCUS:
    print(f"   {t}: modelo {MODELO[t]:.2f}; Focus {FOCUS[t]:.2f} (modelo - Focus {MODELO[t]-FOCUS[t]:+.2f}); DI {DI[t]:.2f} (modelo - DI {MODELO[t]-DI[t]:+.2f})")
