"""G pm: os pontos 'com tempero' da seção 3.3 (ciclo 2026-10-15). Os do modelo vêm de pm_cenarios.py.
- Gradualismo (ii): o Copom move a Selic no máximo 25 p.b. por reunião a partir de 13,75 (duas
  reuniões por trimestre; 1T28 com duas reuniões supostas, fora do calendário oficial). O ponto
  com tempero é o maior entre o do modelo e esse piso, levado à grade de 25 p.b.
- Petróleo e efeitos de segunda ordem (ii), só no worst: a Selic fica em 13,75 em nov/26–mar/27;
  depois segue o worst (i) do modelo, sem cair mais que 25 p.b. por reunião."""
TRI = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
BASE = [12.47, 12.14, 11.86, 11.62, 11.41, 11.22]
WORST_I = [13.31, 13.37, 13.20, 13.03, 12.86, 12.68]
BEST_I = [12.16, 11.56, 11.13, 10.83, 10.57, 10.35]


def grade(x):
    return round(x * 4) / 4


piso = [13.75 - 0.25 * 2 * (k + 1) for k in range(6)]
print("piso a 25 p.b. por reunião: " + " · ".join(f"{q} {v:.2f}" for q, v in zip(TRI, piso)))
for nome, s in [("base", BASE), ("best (i)", BEST_I)]:
    com = [grade(max(m, p)) for m, p in zip(s, piso)]
    print(f"{nome}: modelo → com gradualismo " + " · ".join(f"{q} {m:.2f}→{c:.2f}" for q, m, c in zip(TRI, s, com)))
w, ant = [], 13.75
for k, m in enumerate(WORST_I):
    v = 13.75 if k < 2 else grade(max(m, ant - 0.50))
    w.append(v)
    ant = v
print("worst (i): modelo → com pausa por petróleo " + " · ".join(f"{q} {m:.2f}→{c:.2f}" for q, m, c in zip(TRI, WORST_I, w)))
