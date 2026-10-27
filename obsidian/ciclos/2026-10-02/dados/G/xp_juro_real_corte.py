"""Expectativas, ciclo 2026-10-02: o juro real que a Focus de 25/09 (última divulgada em 02/10) implica,
(1 + Selic do fim do ano)/(1 + IPCA do ano) − 1, a mesma conta do F (que usa 02/10)."""
import pandas as pd
from pathlib import Path
A = Path(__file__).resolve().parent.parent / "A"
D = pd.Timestamp("2026-09-25")
se = pd.read_csv(A / "expc_focus_periodo__selic.csv.gz", parse_dates=["date"])
pe = pd.read_csv(A / "expc_focus_periodo__inflacao.csv.gz", parse_dates=["date"])
se = se[(se.date == D) & (se.base_calculo == 0)].set_index("data_referencia")["mediana"]
ip = pe[(pe.date == D) & (pe.base_calculo == 0) & (pe.periodicidade == "anual") & (pe.indicador == "IPCA")]
ip = ip.set_index(ip.data_referencia.astype(str).str[:4].astype(int))["mediana"]
for a in range(2026, 2031):
    print(a, "Selic", se[a], "IPCA", round(ip[a], 2), "juro real", round(100 * ((1 + se[a] / 100) / (1 + ip[a] / 100) - 1), 2))
