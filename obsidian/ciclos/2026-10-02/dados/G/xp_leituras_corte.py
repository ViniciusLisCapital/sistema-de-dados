"""Expectativas, ciclo 2026-10-02: revisões até a última Focus divulgada em 02/10 (coleta de 25/09),
contra 28/08 (4 semanas) e 26/06 (13 semanas); a inflação implícita da curva contra a Focus; o
PIB esperado por componente. Lê só ../A/."""
import pandas as pd
from pathlib import Path

A = Path(__file__).resolve().parent.parent / "A"
D, D4, D13 = (pd.Timestamp(x) for x in ("2026-09-25", "2026-08-28", "2026-06-26"))
nm = lambda s: s.encode("latin1", "ignore").decode("latin1")

fo = pd.read_csv(A / "expc_focus__inflacao.csv.gz", parse_dates=["date"])
fo = fo[(fo.suavizada == "S") & (fo.base_calculo == 0)].copy()
fo["ind"] = fo.indicador.map(nm)
print("== Focus por horizonte móvel: 25/09, Δ4 sem., Δ13 sem.")
for (ind, h), g in fo.groupby(["ind", "horizonte"]):
    g = g.set_index("date")["mediana"]
    print(ind[:28].ljust(28), h, round(g[D], 2), "Δ4", round(g[D] - g[D4], 2), "Δ13", round(g[D] - g[D13], 2))

pe = pd.read_csv(A / "expc_focus_periodo__inflacao.csv.gz", parse_dates=["date"])
an = pe[(pe.periodicidade == "anual") & (pe.base_calculo == 0)].copy()
an["ind"] = an.indicador.map(nm); an["ano"] = an.data_referencia.astype(str).str[:4].astype(int)
print("== Anos-calendário IPCA cheio e componentes: Δ13 sem. até 25/09")
for (ind, ano), g in an[an.ano.between(2026, 2029)].groupby(["ind", "ano"]):
    g = g.set_index("date")["mediana"]
    print(ind[:28].ljust(28), ano, round(g[D], 2), "Δ4", round(g[D] - g[D4], 2), "Δ13", round(g[D] - g[D13], 2))

pib = pd.read_csv(A / "expc_focus_periodo__pib.csv.gz", parse_dates=["date"])
pib = pib[(pib.periodicidade == "anual") & (pib.base_calculo == 0)].copy()
pib["ind"] = pib.indicador.map(nm); pib["ano"] = pib.data_referencia.astype(str).str[:4].astype(int)
print("== PIB por componente: 25/09, Δ13 sem.")
for (ind, ano), g in pib[pib.ano.between(2026, 2027)].groupby(["ind", "ano"]):
    g = g.set_index("date")["mediana"]
    if D in g.index and D13 in g.index:
        print(ind[:45].ljust(45), ano, round(g[D], 2), "Δ13", round(g[D] - g[D13], 2))

br = pd.read_csv(A / "br_interest_rate.csv.gz", parse_dates=["date"])
def impl(d, ten):
    x = br[(br.date == d) & (br.tenor == ten)].set_index("curve")["value"]
    return 100 * ((1 + x["DIPRE"] / 100) / (1 + x["NTNBJS"] / 100) - 1)
s = fo[fo.ind == "IPCA"].set_index(["horizonte", "date"])["mediana"]
D0 = pd.Timestamp("2026-10-02")
print("== Implícita (02/10) contra a Focus (25/09)")
i1, i2 = impl(D0, "12M"), impl(D0, "24M")
print("1 ano implícita", round(i1, 2), "− Focus 12m", round(s[("12m", D)], 2), "=", round(i1 - s[("12m", D)], 2))
# a implícita de 2 anos cobre os próximos 24 meses; a Focus composta de 12m e 24m (o 2º ano) é a comparação
f2 = 100 * ((1 + s[("12m", D)] / 100) * (1 + s[("24m", D)] / 100)) ** 0.5 - 100
print("2 anos implícita", round(i2, 2), "− Focus média anual dos 24 meses (12m e 24m compostos)", round(f2, 2), "=", round(i2 - f2, 2))
# a implícita a termo do 2º ano: (1+i2)^2/(1+i1) − 1
fw = 100 * ((1 + i2 / 100) ** 2 / (1 + i1 / 100) - 1)
print("implícita a termo, 2º ano", round(fw, 2), "− Focus 24m", round(s[("24m", D)], 2), "=", round(fw - s[("24m", D)], 2))
for d0 in ("2026-09-02", "2026-07-02"):
    print("implícita 1a em", d0, round(impl(pd.Timestamp(d0), "12M"), 2), "| 10a", round(impl(pd.Timestamp(d0), "120M"), 2))
print("Focus 12m: 28/08", round(s[("12m", D4)], 2), "| 26/06", round(s[("12m", D13)], 2))
