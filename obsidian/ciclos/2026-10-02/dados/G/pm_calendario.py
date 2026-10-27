"""pm: quanto do 4T26 já está decidido pelo calendário (pm_copom_calendario).

A Selic decidida numa reunião vale a partir do dia útil seguinte; aqui, por simplicidade, do dia
seguinte à decisão (dias corridos). Calcula a fração do 4T26 em 13,75% até a 282ª (04/11), e a média
do trimestre para alguns caminhos das duas reuniões do trimestre (282ª e 283ª), para comparar com a
média do 4T26 que o Modelo Estrutural dá no cenário base (13,27, G pm_cenarios_r1.py)."""
import datetime as dt
from pathlib import Path

import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"
cal = pd.read_csv(A / "pm_copom_calendario.csv.gz", parse_dates=["date"])
r1, r2 = [d.date() for d in cal.date if dt.date(2026, 10, 1) <= d.date() <= dt.date(2026, 12, 31)]
ini, fim = dt.date(2026, 10, 1), dt.date(2026, 12, 31)
n = (fim - ini).days + 1
d0 = (r1 - ini).days + 1          # 01/10 a 04/11 em 13,75
d1 = (r2 - r1).days               # 05/11 a 09/12
d2 = (fim - r2).days              # 10/12 a 31/12
print("reuniões no 4T26:", r1, r2, "| dias:", n, "| em 13,75 até a 282ª:", d0, f"({100*d0/n:.0f}%)", "|", d1, d2)
for p1, p2 in [(0, 0), (-25, 0), (-25, -25), (-50, -25), (-50, -50), (-75, -75)]:
    s1, s2 = 13.75 + p1 / 100, 13.75 + (p1 + p2) / 100
    m = (13.75 * d0 + s1 * d1 + s2 * d2) / n
    print(f"passos {p1:+d}/{p2:+d}: fechamento {s2:.2f}, média do 4T26 {m:.2f}")
