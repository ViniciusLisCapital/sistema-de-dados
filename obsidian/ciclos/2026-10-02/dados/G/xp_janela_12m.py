"""Expectativas, ciclo 2026-10-02: quanto da alta da Focus 12m desde julho é a janela andando e quanto é revisão.

Usa as medianas trimestrais da Focus (expc_focus_periodo, IPCA, trimestral, base 30 dias) em
2026-07-03 e 2026-09-25 (a última divulgada em 02/10). Para cada data, compõe as medianas de
cada trimestre (uma aproximação: composição de medianas não é a mediana da composição).
Lê só ../A/."""
import pandas as pd
from pathlib import Path

A = Path(__file__).resolve().parent.parent / "A"
pe = pd.read_csv(A / "expc_focus_periodo__inflacao.csv.gz", parse_dates=["date"])
t = pe[(pe.periodicidade == "trimestral") & (pe.base_calculo == 0) & (pe.indicador == "IPCA")]
def tab(d):
    x = t[t.date == pd.Timestamp(d)].set_index("data_referencia")["mediana"]
    return x
def comp(vals):
    p = 1.0
    for v in vals: p *= 1 + v / 100
    return 100 * (p - 1)
j, s = tab("2026-07-03"), tab("2026-09-25")
print("07-03:", j.to_dict()); print("09-25:", s.to_dict())
# janela de julho: 3T26..2T27 ; de setembro (fim do 3T, o 12m já pesa 4T26..3T27)
qa = ["3/2026", "4/2026", "1/2027", "2/2027"]; qb = ["4/2026", "1/2027", "2/2027", "3/2027"]
a = comp([j[q] for q in qa]); b = comp([s[q] for q in qb])
mesmos = comp([s[q] for q in qa if q in s.index]) if all(q in s.index for q in qa) else None
print("composto jul (3T26-2T27, em 07-03):", round(a, 2))
print("composto set (4T26-3T27, em 09-25):", round(b, 2))
print("revisão dos trimestres comuns 4T26-2T27:", {q: round(s[q] - j[q], 2) for q in qa[1:]})
print("3T26 em 07-03:", j["3/2026"], "| 3T27 em 09-25:", s["3/2027"])
# efeito de janela: troca 3T26 (julho) por 3T27 (setembro), com os comuns fixos em julho
jan = comp([j[q] for q in qa[1:]] + [s["3/2027"]])
print("efeito janela (comuns de julho, troca 3T26 por 3T27):", round(jan - a, 2), "| revisão dos comuns:", round(b - jan, 2))
