"""pm2: o que o histórico de decisões do Copom diz sobre passos e pausas (pm_copom_reuniao),
e o passo implícito na curva convertido em probabilidade (br_di_grade via F), e o Brent
contra o condicionante do RPM de set/26.

Só lê A/. Janela dita em cada bloco.
"""
from pathlib import Path

import pandas as pd

A = Path(__file__).resolve().parents[1] / "A"
r = pd.read_csv(A / "pm_copom_reuniao.csv.gz", parse_dates=["date"]).sort_values("date").reset_index(drop=True)

print("== 1. Distribuição dos passos, todas as reuniões ordinárias desde 2006 (8 reuniões/ano)")
r06 = r[r.date >= "2006-01-01"]
print(r06.variacao_bps.value_counts().sort_index().to_string())
print(f"n = {len(r06)}")

print("\n== 2. Ciclos de corte desde 2003: sequência de reuniões entre o primeiro corte e a primeira alta")
# um ciclo de corte começa num corte precedido por manutenção ou alta, e termina na última reunião antes de uma alta
r03 = r[r.date >= "2003-01-01"].reset_index(drop=True)
ciclos = []
i = 0
while i < len(r03):
    if r03.variacao_bps[i] < 0 and (i == 0 or r03.variacao_bps[i - 1] >= 0):
        j = i
        while j + 1 < len(r03) and r03.variacao_bps[j + 1] <= 0:
            j += 1
        # corta as manutenções no fim do ciclo (o ciclo acaba no último corte)
        k = j
        while r03.variacao_bps[k] == 0:
            k -= 1
        ciclos.append(r03.iloc[i : k + 1])
        i = j + 1
    else:
        i += 1
for c in ciclos:
    passos = c.variacao_bps.tolist()
    pausas = sum(1 for p in passos if p == 0)
    print(f"{c.date.iloc[0].date()} a {c.date.iloc[-1].date()}: {c.selic_anterior.iloc[0]:.2f} -> {c.selic_decidida.iloc[-1]:.2f}, "
          f"total {sum(passos)} p.b. em {len(passos)} reuniões, pausas no meio {pausas}; passos {passos}")

print("\n== 3. Dentro dos ciclos de corte desde 2003: o passo da reunião seguinte a uma sequência de 5+ cortes iguais de 25")
casos = []
for c in ciclos:
    p = c.variacao_bps.tolist()
    for t in range(5, len(p) + 1):
        if all(x == -25 for x in p[t - 5 : t]):
            nxt = p[t] if t < len(p) else "fim do ciclo (manutenção ou alta)"
            casos.append((c.date.iloc[t - 1].date(), nxt))
for d, n in casos:
    print(f"   depois de {d}: {n}")

print("\n== 4. Ciclos de corte desde 2003: maior corte numa reunião, e reuniões com corte de 50+ p.b.")
for c in ciclos:
    p = c.variacao_bps
    print(f"   {c.date.iloc[0].year}: maior corte {p.min()} p.b.; cortes de 50+ em {int((p <= -50).sum())} de {len(p)} reuniões")

print("\n== 5. Passo implícito na curva -> probabilidade de -25 contra manter (só dois resultados)")
for reu, passo in [("2026-11-04", -18), ("2026-12-09", -19)]:
    print(f"   {reu}: passo {passo} p.b. -> P(-25) = {abs(passo)/25:.0%}, se a única alternativa for manter")
print("   (o passo vem do F, br_di_grade, pregão de 14/10; leva prêmio)")

print("\n== 6. Brent: média do 3T26 e de out/26 até o último dado, contra o ponto de partida do RPM de set/26 (US$ 90)")
b = pd.read_csv(A / "comm_brent.csv.gz", parse_dates=["date"]).set_index("date")["value"].sort_index()
print(f"   média 3T26: {b.loc['2026-07-01':'2026-09-30'].mean():.1f} ({b.loc['2026-07-01':'2026-09-30'].size} dias)")
print(f"   média 01/09 a 11/09 (antes do corte do RPM, 10 dias úteis aprox.): {b.loc['2026-08-28':'2026-09-11'].mean():.1f}")
print(f"   média out/26 até {b.index[-1].date()}: {b.loc['2026-10-01':].mean():.1f}")
print(f"   último {b.iloc[-1]:.2f} em {b.index[-1].date()}; contra 90: {(b.iloc[-1]/90-1)*100:+.0f}%")
print(f"   jul/26 média {b.loc['2026-07'].mean():.1f}; ago/26 média {b.loc['2026-08'].mean():.1f}; set/26 média {b.loc['2026-09'].mean():.1f}")
