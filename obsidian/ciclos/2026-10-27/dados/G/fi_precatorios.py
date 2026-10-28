"""fi: sentenças judiciais e precatórios no RTN (todas as linhas), por mês e por janela de 12 meses e de 4
trimestres, em % do PIB; e o impulso pelo primário do governo central SEM precatórios (12m e 3m).
Testa se a diferença entre as medidas de impulso vem do calendário de pagamento dos precatórios."""
from pathlib import Path
import pandas as pd
A = Path(__file__).resolve().parent.parent / "A"
r = lambda f: pd.read_csv(A / f"{f}.csv.gz", parse_dates=["date"])
rtn = r("fisc_rtn").pivot_table(index="date", columns="name", values="value")
prec_cols = [c for c in rtn.columns if "sentencas_judiciais" in c]
print("Linhas de precatórios:", prec_cols)
prec = rtn[prec_cols].fillna(0).sum(axis=1)
pm = r("atv_pib_mensal"); pm = pm[pm.name == "pib_mensal"].set_index("date").value
pib12 = pm.rolling(12).sum()
m = prec[prec.index >= "2023-01-01"]
print("\nPrecatórios por mês acima de R$ 5 bi (R$ bi):", (m[m > 5000] / 1000).round(1).to_dict())
p12 = prec.rolling(12).sum()
print("\nPrecatórios 12m, % do PIB:")
for d in ["2025-05-01", "2025-08-01", "2026-05-01", "2026-08-01"]:
    d = pd.Timestamp(d); print(f"  até {d.date()}: R$ {p12[d]/1000:.1f} bi = {100*p12[d]/pib12[d]:.2f}% do PIB")
# 4 trimestres até 2T25 e até 2T26 (a janela da EFGG)
for fim in ["2025-06-01", "2026-06-01"]:
    fim = pd.Timestamp(fim)
    print(f"  4 tri até {fim.date()}: R$ {p12[fim]/1000:.1f} bi = {100*p12[fim]/pib12[fim]:.2f}% do PIB")
pc = rtn["resultado_primario_governo_central"]
pex = pc + prec  # primário sem a despesa com precatórios
def pct12(s, d): return 100 * s.rolling(12).sum()[d] / pib12[d]
d0, dm3, dm12 = pd.Timestamp("2026-08-01"), pd.Timestamp("2026-05-01"), pd.Timestamp("2025-08-01")
print("\nPrimário do governo central 12m (% do PIB, + = superávit), RTN:")
for nome, s in [("com precatórios", pc), ("sem precatórios", pex)]:
    a, b, c = pct12(s, d0), pct12(s, dm3), pct12(s, dm12)
    print(f"  {nome}: ago/26 {a:.2f} · mai/26 {b:.2f} · ago/25 {c:.2f} · impulso 3m {-(a-b):+.2f} · impulso 12m {-(a-c):+.2f}")
# a mesma conta por trimestre: primário 12m sem precatórios no fim de cada trimestre
print("\nPrimário 12m sem precatórios no fim de cada trimestre (% do PIB) e impulso contra 4 trimestres antes:")
q_end = [pd.Timestamp(x) for x in ["2024-12-01","2025-03-01","2025-06-01","2025-09-01","2025-12-01","2026-03-01","2026-06-01","2026-08-01"]]
for d in q_end:
    a = pct12(pex, d); b = pct12(pex, d - pd.DateOffset(months=12)); a2 = pct12(pc, d); b2 = pct12(pc, d - pd.DateOffset(months=12))
    print(f"  {d.date()}: sem prec {a:+.2f} (impulso 12m {-(a-b):+.2f}) · com prec {a2:+.2f} (impulso 12m {-(a2-b2):+.2f})")
