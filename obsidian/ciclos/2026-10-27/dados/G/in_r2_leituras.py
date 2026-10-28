"""in_r2_leituras: contas de dado do report de inflação, ciclo 2026-10-27, rodada 2.

Lê só ../A/. Imprime:
 1. Pesos de set/26 dos quatro grupos do BC e dos subitens de combustível (gasolina, diesel,
    etanol, GNV), e se cada um é monitorado na classificação do BC.
 2. Energia elétrica residencial, IPCA e IPCA-15, mês a mês desde jan/2025.
 3. Meses em que a energia do IPCA caiu mais de 5%: a energia do IPCA-15 no mesmo mês e no
    seguinte (como uma queda de bandeira entra nas duas pesquisas), 2016-2026.
 4. Tomate, batata-inglesa e cebola no IPCA, mês a mês desde jul/2026, e no IPCA-15 de out/26.
 5. Plano de saúde no IPCA, mês a mês desde jan/2026.
"""
import sys
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
A = Path(__file__).resolve().parent.parent / "A"
rd = lambda n: pd.read_csv(A / f"{n}.csv.gz")

dc = rd("inflc_decomposicao")
dc["date"] = pd.to_datetime(dc["date"])
dim = rd("inflc_dim")
dim["subitem_codigo"] = dim["subitem_codigo"].astype(str)
dc["subitem_codigo"] = dc["subitem_codigo"].astype(str)
dc = dc.merge(dim[["subitem_codigo", "nome", "grupo", "subgrupo", "item"]], on="subitem_codigo", how="left")
dc["bc"] = dc.apply(lambda r: "Monitorados" if r.grupo == "Monitorados" else
                    {"Alimentos": "Alimentação", "Bens Industriais": "Industriais",
                     "Serviços": "Serviços"}.get(r.subgrupo, "?"), axis=1)

# 1
x = dc[(dc.indice == "IPCA") & (dc.date == "2026-09-01")]
tot = x.pesos.sum()
print("1. pesos set/26 (%):", (x.groupby("bc").pesos.sum() / tot * 100).round(2).to_dict())
for nome in ("Gasolina", "Óleo diesel", "Etanol", "Gás veicular", "Gás de botijão",
             "Energia elétrica residencial", "Plano de saúde"):
    t = x[x.nome == nome]
    if len(t):
        print(f"   {nome}: peso {t.pesos.sum()/tot*100:.2f}% · grupo {t.grupo.iloc[0]} · bc {t.bc.iloc[0]}"
              f" · set/26 {t.var_mensal.iloc[0]:+.2f}%")
mon = x[(x.grupo == "Monitorados") & (x.nome.isin(["Gasolina", "Óleo diesel", "Gás veicular"]))]
print(f"   gasolina+diesel+GNV (monitorados): {mon.pesos.sum()/tot*100:.2f}%")


def serie(ind, nome):
    t = dc[(dc.indice == ind) & (dc.nome == nome)].groupby("date")["var_mensal"].mean()
    return t.sort_index()


# 2
e = serie("IPCA", "Energia elétrica residencial")
e15 = serie("IPCA15", "Energia elétrica residencial")
print("\n2. Energia elétrica residencial (IPCA | IPCA-15)")
for d in pd.date_range("2025-01-01", "2026-10-01", freq="MS"):
    print(f"   {d:%Y-%m}: {e.get(d, float('nan')):6.2f} | {e15.get(d, float('nan')):6.2f}")

# 3
print("\n3. Quedas da energia do IPCA de mais de 5% (2016-2026): IPCA-15 do mesmo mês e do seguinte")
for d, v in e.loc["2016-01-01":].items():
    if v < -5:
        nx = d + pd.DateOffset(months=1)
        print(f"   {d:%Y-%m}: IPCA {v:6.2f} · IPCA-15 mesmo mês {e15.get(d, float('nan')):6.2f}"
              f" · IPCA-15 seguinte {e15.get(nx, float('nan')):6.2f} · IPCA seguinte {e.get(nx, float('nan')):6.2f}")
print("   Altas de mais de 5% (2016-2026):")
for d, v in e.loc["2016-01-01":].items():
    if v > 5:
        nx = d + pd.DateOffset(months=1)
        print(f"   {d:%Y-%m}: IPCA {v:6.2f} · IPCA-15 mesmo mês {e15.get(d, float('nan')):6.2f}"
              f" · IPCA-15 seguinte {e15.get(nx, float('nan')):6.2f} · IPCA seguinte {e.get(nx, float('nan')):6.2f}")

# 4
print("\n4. Hortaliças (IPCA desde jul/26; IPCA-15 out/26)")
for nome in ("Tomate", "Batata-inglesa", "Cebola"):
    s = serie("IPCA", nome).loc["2026-07-01":]
    s15 = serie("IPCA15", nome)
    print(f"   {nome}: " + "; ".join(f"{d:%m} {v:+.2f}" for d, v in s.items())
          + f" | IPCA-15 out {s15.get(pd.Timestamp('2026-10-01'), float('nan')):+.2f}")

# 5
s = serie("IPCA", "Plano de saúde").loc["2025-01-01":]
print("\n5. Plano de saúde (IPCA): " + "; ".join(f"{d:%y-%m} {v:.2f}" for d, v in s.items()))
