"""Expectativas: a trajetória da Focus 12m SE NINGUÉM REVISAR, montada com a própria pesquisa de 2026-10-23.

Lê só A/expc_focus_periodo__inflacao.csv.gz e A/expc_focus__inflacao.csv.gz.
- Inflação mês a mês esperada: medianas mensais (base 0) de 10/2026 a 10/2028; Nov–Dez/2028
  pelo resto do ano de 2028 (anual 2028 descontado de Jan–Out/2028), igual por mês; 2029 pela
  anual de 2029, com o perfil sazonal das medianas mensais de 2028 escalado.
- Janela de 12 meses a partir do mês M: produto dos 12 meses M..M+11.
- Valida a convenção contra a Focus 12m publicada em 2026-10-23 (não suavizada e suavizada).
- Suavizada aproximada: média, ponderada pelo dia do mês, da janela que começa no mês corrente
  e da que começa no seguinte.
- Média do trimestre: média dos dias úteis (seg–sex) do trimestre, 4T26 a 1T28.
- Também: o IPCA em 4 trimestres no horizonte relevante do Copom (2T27–1T28), pelas medianas
  trimestrais, e o que as pesquisas restantes do 4T26 teriam de marcar para o trimestre fechar
  em cada valor.
"""
from pathlib import Path
import datetime as dt
import numpy as np
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"
d = pd.read_csv(A / "expc_focus_periodo__inflacao.csv.gz")
d = d[(d.date == "2026-10-23") & (d.indicador == "IPCA") & (d.base_calculo == 0)]
mens = d[d.periodicidade == "mensal"].copy()
mens["m"] = pd.to_datetime(mens.ref_date).dt.to_period("M")
mm = mens.set_index("m").mediana.sort_index()
anual = d[d.periodicidade == "anual"].set_index("data_referencia").mediana
anual.index = anual.index.astype(int)
tri = d[d.periodicidade == "trimestral"].set_index("data_referencia").mediana

serie = {p: v for p, v in mm.items()}
# Nov–Dez/2028
jan_out_28 = np.prod([1 + serie[pd.Period(f"2028-{k:02d}", "M")] / 100 for k in range(1, 11)])
resto = ((1 + anual[2028] / 100) / jan_out_28) ** (1 / 2) - 1
for k in (11, 12):
    serie[pd.Period(f"2028-{k:02d}", "M")] = resto * 100
# 2029: o perfil sazonal de 2028 (medianas mensais), escalado para compor a anual de 2029
perfil = [serie[pd.Period(f"2028-{k:02d}", "M")] for k in range(1, 13)]
lo, hi = 0.0, 3.0
for _ in range(60):
    fat = (lo + hi) / 2
    comp = np.prod([1 + fat * v / 100 for v in perfil]) - 1
    lo, hi = (fat, hi) if comp * 100 < anual[2029] else (lo, fat)
for k in range(1, 13):
    serie[pd.Period(f"2029-{k:02d}", "M")] = fat * perfil[k - 1]
print(f"2029: perfil de 2028 escalado por {fat:.3f}")
print(f"Nov–Dez/2028 por mês: {resto*100:.3f}")

def janela(M):
    return (np.prod([1 + serie[M + k] / 100 for k in range(12)]) - 1) * 100

out = pd.Period("2026-10", "M")
print(f"janela Out/26–Set/27: {janela(out):.3f} · Nov/26–Out/27: {janela(out+1):.3f}")
f = pd.read_csv(A / "expc_focus__inflacao.csv.gz")
f = f[(f.indicador == "IPCA") & (f.horizonte == "12m") & (f.base_calculo == 0) & (f.date == "2026-10-23")]
print("publicado 2026-10-23:", f[["suavizada", "mediana"]].to_string(index=False))

def suav(day):
    M = pd.Period(day, "M")
    dias = pd.Period(day, "M").days_in_month
    w = day.day / dias
    return (1 - w) * janela(M) + w * janela(M + 1)

print(f"suavizada aproximada em 2026-10-23: {suav(dt.date(2026,10,23)):.3f}")

print("\nTrimestre · média dos dias úteis da janela suavizada aproximada (sem revisão)")
quarters = [("4T26", "2026-10-01", "2026-12-31"), ("1T27", "2027-01-01", "2027-03-31"),
            ("2T27", "2027-04-01", "2027-06-30"), ("3T27", "2027-07-01", "2027-09-30"),
            ("4T27", "2027-10-01", "2027-12-31"), ("1T28", "2028-01-01", "2028-03-31")]
for q, a, b in quarters:
    dias = pd.bdate_range(a, b)
    v = np.mean([suav(x.date()) for x in dias])
    print(f"  {q}: {v:.2f}  (início {suav(dias[0].date()):.2f}, fim {suav(dias[-1].date()):.2f})")

# 4T26: o que já está dentro e o que falta
fq = pd.read_csv(A / "expc_focus__inflacao.csv.gz")
fq = fq[(fq.indicador == "IPCA") & (fq.horizonte == "12m") & (fq.suavizada == "S") &
        (fq.base_calculo == 0) & (fq.tipo_calculo == "geral")]
q4 = fq[fq.date >= "2026-10-01"].mediana
n_in, m_in = len(q4), q4.mean()
q3 = fq[(fq.date >= "2026-07-01") & (fq.date <= "2026-09-30")]
n_tot = 65  # o 3T26 teve 65 pesquisas (F); o 4T26 terá número parecido
print(f"\n4T26 até agora: {n_in} pesquisas, média {m_in:.3f}; 3T26 teve {len(q3)}")
for alvo in [4.16, 4.30, 4.40, 4.50, 4.60, 4.70]:
    for N in (62, 65):
        resto_med = (alvo * N - m_in * n_in) / (N - n_in)
        print(f"  4T26 fecha em {alvo:.2f} (N={N}) se as {N-n_in} restantes marcarem em média {resto_med:.2f}")

h = np.prod([1 + tri[k] / 100 for k in ["2/2027", "3/2027", "4/2027", "1/2028"]]) - 1
print(f"\nIPCA 2T27–1T28 pelas medianas trimestrais: {h*100:.2f}")
h2 = np.prod([1 + tri[k] / 100 for k in ["1/2027", "2/2027", "3/2027", "4/2027"]]) - 1
print(f"IPCA 1T27–4T27 pelas trimestrais: {h2*100:.2f} (anual 2027: {anual[2027]:.2f})")
