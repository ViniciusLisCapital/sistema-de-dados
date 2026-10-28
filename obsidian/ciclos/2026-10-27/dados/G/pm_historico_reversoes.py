"""Regularidades do Copom em pm_copom_reuniao (1999 em diante): passos, reversões de ciclo,
decisões fora de reunião e o que veio depois de um corte (ciclo 2026-10-27). Lê só A/."""
import pandas as pd
from pathlib import Path

A = Path(__file__).resolve().parent.parent / "A"
r = pd.read_csv(A / "pm_copom_reuniao.csv.gz").sort_values("date").reset_index(drop=True)
print("Amostra:", r.date.min(), "a", r.date.max(), "·", len(r), "decisões")
print("\nDistribuição dos passos (p.b.):")
print(r.variacao_bps.value_counts().sort_index().to_string())
print("\nDecisões fora de reunião ordinária (alterada_fora_da_reuniao=1):")
print(r[r.alterada_fora_da_reuniao == 1][["nro_reuniao", "date", "selic_anterior", "selic_decidida", "variacao_bps"]].to_string())

# Depois de um corte, o que vem na reunião seguinte
r["prox"] = r.variacao_bps.shift(-1)
c = r[r.variacao_bps < 0]
print("\nReunião seguinte a um corte: distribuição do passo")
print(c.prox.value_counts().sort_index().to_string())

# Reversões: primeira alta depois de um corte (sem ou com pausas no meio)
print("\nReversões de corte para alta (último corte -> primeira alta, pausas entre elas):")
ult_corte = None; pausas = 0
for i, row in r.iterrows():
    if row.variacao_bps < 0:
        ult_corte = row; pausas = 0
    elif row.variacao_bps == 0:
        pausas += 1
    elif row.variacao_bps > 0 and ult_corte is not None:
        print(f"  corte {ult_corte.date} ({ult_corte.variacao_bps:+d}) -> {pausas} manutenção(ões) -> alta {row.date} ({row.variacao_bps:+d}), Selic {row.selic_anterior} -> {row.selic_decidida}")
        ult_corte = None
# Fim de ciclos de corte: primeira manutenção depois de uma sequência de cortes
print("\nFim de ciclos de corte (primeira decisão não negativa após corte):")
for i in range(1, len(r)):
    if r.variacao_bps[i - 1] < 0 and r.variacao_bps[i] >= 0:
        print(f"  {r.date[i]}: {r.variacao_bps[i]:+d} após corte de {r.variacao_bps[i-1]:+d} em {r.date[i-1]}")
# 2002
print("\n2002-2003:")
print(r[(r.date >= "2002-06-01") & (r.date <= "2003-03-31")][["nro_reuniao", "date", "selic_anterior", "selic_decidida", "variacao_bps", "alterada_fora_da_reuniao"]].to_string())
print("\nPrimeiros passos de ciclos de alta (alta após manutenção ou corte):")
for i in range(1, len(r)):
    if r.variacao_bps[i] > 0 and r.variacao_bps[i - 1] <= 0:
        print(f"  {r.date[i]}: {r.variacao_bps[i]:+d}")
