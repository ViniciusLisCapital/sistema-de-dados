"""pm2: leituras de mercado e de postura que o F não faz.

1. Caminho diário, 01/09 a 15/10/2026: NTN-B 10 anos, DI pré 2 e 10 anos, PTAX, CDS, Brent.
2. Onde o movimento de out/26 se concentrou: variações em janelas (até 02/10 e depois).
3. NTN-B 10 anos: média do 3T26, média de out/26 até o corte, e a média do 4T26 se ela
   ficar no último valor até 31/12 (a convenção do simulador é média do trimestre).
4. CDS: o último pregão do 3T26 (a convenção do simulador é fechamento).
5. Postura: Selic real ex-ante (do F) contra o neutro do Copom (5,00%, RPM set/26) e contra os
   neutros do QPC; Selic nominal contra a âncora do modelo (NTN-B 10a + meta).
6. Fed Funds: Treasury 3 meses contra a meta (ponto médio).
Só lê A/. Não escreve nada.
"""
from pathlib import Path

import numpy as np
import pandas as pd

A = Path(__file__).resolve().parents[1] / "A"

ir = pd.read_csv(A / "br_interest_rate.csv.gz", parse_dates=["date"])
cds = pd.read_csv(A / "cmb_risco_pais.csv.gz", parse_dates=["date"])
ptax = pd.read_csv(A / "cmb_ptax.csv.gz", parse_dates=["date"])
brent = pd.read_csv(A / "comm_brent.csv.gz", parse_dates=["date"])
us = pd.read_csv(A / "us_interest_rate__curva.csv.gz", parse_dates=["date"])


def serie(df, **filtros):
    m = pd.Series(True, index=df.index)
    for k, v in filtros.items():
        m &= df[k] == v
    return df[m].set_index("date")["value"].sort_index()


ntnb10 = serie(ir, curve="NTNBJS", tenor="120M")
ntnb2 = serie(ir, curve="NTNBJS", tenor="24M")
di2 = serie(ir, curve="DIPRE", tenor="24M")
di10 = serie(ir, curve="DIPRE", tenor="120M")
selic = serie(ir, curve="POLICY", tenor="1d")
cds5 = serie(cds, name="cds_5y_usd")
px = serie(ptax, name="ptax_venda")
br = serie(brent, name="brent_usd")

tab = pd.concat(
    {"NTNB10": ntnb10, "NTNB2": ntnb2, "DI2": di2, "DI10": di10, "PTAX": px, "CDS": cds5, "Brent": br},
    axis=1,
)
janela = tab.loc["2026-09-01":"2026-10-15"]
print("== 1. Caminho diário, 01/09 a 15/10/2026")
print(janela.round(3).to_string())

print("\n== 2. Variações em janelas")
def var(s, a, b, pct=False):
    s = s.dropna()
    va = s.loc[:a].iloc[-1]
    vb = s.loc[:b].iloc[-1]
    da = s.loc[:a].index[-1].date()
    db = s.loc[:b].index[-1].date()
    d = (vb / va - 1) * 100 if pct else vb - va
    return f"{da} {va:.3f} -> {db} {vb:.3f}: {d:+.2f}{' %' if pct else ''}"

for nome, s, pct in [("NTNB10", ntnb10, False), ("NTNB2", ntnb2, False), ("DI2", di2, False),
                     ("DI10", di10, False), ("PTAX", px, True), ("CDS", cds5, False), ("Brent", br, True)]:
    print(nome)
    print("   16/09 (Copom 281) -> 02/10:", var(s, "2026-09-16", "2026-10-02", pct))
    print("   02/10 -> 15/10          :", var(s, "2026-10-02", "2026-10-15", pct))
    print("   30/09 (fim do 3T) -> 15/10:", var(s, "2026-09-30", "2026-10-15", pct))

print("\n== 3. NTN-B 10 anos (rr_10a do simulador: média do trimestre)")
t3 = ntnb10.loc["2026-07-01":"2026-09-30"]
out = ntnb10.loc["2026-10-01":"2026-10-15"]
print(f"média 3T26: {t3.mean():.3f} ({len(t3)} pregões)")
print(f"média out/26 até 15/10: {out.mean():.3f} ({len(out)} pregões); último {ntnb10.iloc[-1]:.3f} em {ntnb10.index[-1].date()}")
bd = pd.bdate_range("2026-10-16", "2026-12-31")
n_rest = len(bd)
media_4t = (out.sum() + ntnb10.iloc[-1] * n_rest) / (len(out) + n_rest)
print(f"4T26 se ficar em {ntnb10.iloc[-1]:.3f} até 31/12 ({n_rest} dias úteis aprox.): média {media_4t:.3f}")
print(f"mín. e máx. da NTN-B 10a desde 2016: {ntnb10.loc['2016':].min():.2f} / {ntnb10.loc['2016':].max():.2f}")
# percentil histórico do recuo de 1 mês
m1 = (ntnb10 - ntnb10.shift(21)).dropna()
ult = m1.iloc[-1]
print(f"recuo de 21 pregões até o corte: {ult:+.2f} p.p.; percentil na amostra desde {m1.index[0].date()}: {(m1 <= ult).mean()*100:.1f}")
m1_10 = m1.loc["2016":]
print(f"   percentil desde 2016: {(m1_10 <= ult).mean()*100:.1f}")

print("\n== 4. CDS 5 anos")
c3 = cds5.loc[:"2026-09-30"]
print(f"último pregão do 3T26: {c3.index[-1].date()} {c3.iloc[-1]:.2f}")
print(f"média set/26: {cds5.loc['2026-09'].mean():.2f}; mín/máx set: {cds5.loc['2026-09'].min():.2f}/{cds5.loc['2026-09'].max():.2f}")
print(f"último: {cds5.index[-1].date()} {cds5.iloc[-1]:.2f}")

print("\n== 5. Postura")
selic_real = 8.88  # F, Leituras combinadas: Selic 13,75 com Focus 12m 4,48
for nome, neutro in [("Copom (RPM set/26)", 5.00), ("QPC 2a", 6.00), ("QPC 5a", 5.50), ("QPC curto prazo", 6.40)]:
    print(f"Selic real ex-ante 8,88 - neutro {nome} {neutro:.2f} = {selic_real - neutro:+.2f} p.p.")
# exato: com a fórmula de Fisher, como no F
sr = (1.1375 / 1.0448 - 1) * 100
print(f"conferência: (1,1375/1,0448 - 1) = {sr:.3f}")
ancora = ntnb10.iloc[-1] + 3.00
print(f"âncora do modelo hoje: NTN-B 10a {ntnb10.iloc[-1]:.2f} + meta 3,00 = {ancora:.2f}; Selic 13,75 - âncora = {13.75 - ancora:+.2f} p.p.")
anc3 = t3.mean() + 3.00
print(f"âncora média 3T26: {anc3:.2f}; Selic média 3T26 (simulador) 14,06 - âncora = {14.06 - anc3:+.2f} p.p.")
# juro real de mercado de 1 ano contra o neutro
print(f"NTN-B 1 ano 5,80 - neutro Copom 5,00 = {5.80-5.00:+.2f}; NTN-B 2 anos 6,80 - 5,00 = {6.80-5.00:+.2f}")

print("\n== 6. EUA")
t3m = serie(us, curve="US_TREASURY", tenor="3M")
print(f"Treasury 3M em 15/10: {t3m.iloc[-1]:.2f}; meta Fed (ponto médio) 3,875 -> diferença {t3m.iloc[-1]-3.875:+.2f} p.p.")
