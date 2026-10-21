"""pm2: as contas pequenas que o report cita e o F não traz (diferenças e razões), e a inflação
implícita (DI contra NTN-B) antes e depois de 05/10. Só lê A/; os valores fixos citados vêm do F
ou dos documentos do Copom, indicados ao lado.
"""
from pathlib import Path

import pandas as pd

A = Path(__file__).resolve().parents[1] / "A"

print("== 1. Diferenças")
contas = [
    ("IPCA set/26 (inflc_agregados) - projeção do RPM set/26 p/ set (Tab. 2.1.2)", 0.82 - 0.65),
    ("IPCA set/26 - mediana do QPC 281 p/ set", 0.82 - 0.56),
    ("IPCA 12m set/26 - teto da meta (4,50)", 4.58 - 4.50),
    ("Serviços subjacentes 12m: set/26 - 3 meses antes (inflc_decomposicao)", 5.32 - 5.00),
    ("Industriais subjacentes 12m: set/26 - 3 meses antes", 3.70 - 4.14),
    ("Selic real ex-ante (8,88, F) - NTN-B 10a (6,87)", 8.88 - 6.87),
    ("Selic real ex-ante (8,88) - NTN-B 1a (5,80)", 8.88 - 5.80),
    ("Focus IPCA 2028 (3,79) - meta (3,00)", 3.79 - 3.00),
    ("Focus IPCA 24m (3,91) - meta", 3.91 - 3.00),
    ("Projeção Copom 1T28 (3,2) - meta", 3.2 - 3.0),
    ("Inflação implícita 5a (5,54, F) - Focus IPCA 2029 (3,50)", 5.54 - 3.50),
]
for nome, v in contas:
    print(f"   {nome}: {v:+.2f}")
print(f"   PTAX 14/10 (5,0441) contra o condicionante do Copom (5,15): {(5.0441/5.15-1)*100:+.1f}%")

print("\n== 2. Inflação implícita (Fisher, DI pré contra NTN-B no mesmo prazo), 02/10 e 15/10")
ir = pd.read_csv(A / "br_interest_rate.csv.gz", parse_dates=["date"])


def v(curve, tenor, data):
    s = ir[(ir.curve == curve) & (ir.tenor == tenor)].set_index("date")["value"].sort_index()
    return s.loc[:data].iloc[-1]


for tenor in ["24M", "60M", "120M"]:
    linha = []
    for d in ["2026-10-02", "2026-10-15"]:
        di, nb = v("DIPRE", tenor, d), v("NTNBJS", tenor, d)
        imp = ((1 + di / 100) / (1 + nb / 100) - 1) * 100
        linha.append((d, di, nb, imp))
    (d0, di0, nb0, i0), (d1, di1, nb1, i1) = linha
    print(f"   {tenor}: {d0} DI {di0:.2f} NTN-B {nb0:.2f} implícita {i0:.2f} -> {d1} DI {di1:.2f} NTN-B {nb1:.2f} implícita {i1:.2f}; "
          f"queda do DI {di1-di0:+.2f}, da NTN-B {nb1-nb0:+.2f}, da implícita {i1-i0:+.2f}")

print("\n== 3. Temperos e saídas do modelo (pm2_cenarios)")
print(f"   R.t3 mediana 1,9617 x 1,3 = {1.9617*1.3:.2f} (intervalo de 90%: 1,148 a 2,726)")
print(f"   R.t1 mediana 1,3359 x 0,95 = {1.3359*0.95:.3f} (intervalo de 90%: 1,201 a 1,484)")
print(f"   worst com R.t3 x1,3 + 25 p.b. do petróleo: 1T27 {13.46+0.25:.2f}; 2T27 {13.35+0.25:.2f}")
print(f"   base contra o padrão do simulador (NTN-B 10a 6,89 contra 7,84 = {6.89-7.84:+.2f}): Selic média 4T26 {12.65-13.60:+.2f}, fechamento 4T26 {12.47-13.43:+.2f}")
print("   mediana do caminho por reunião (pm2_reunioes) - central do modelo:")
for t, med, c in [("4T26", 13.25, 12.47), ("1T27", 13.00, 12.13), ("2T27", 12.50, 11.85), ("3T27", 12.25, 11.61), ("4T27", 11.75, 11.39), ("1T28", 11.25, 11.20)]:
    print(f"      {t}: {med:.2f} - {c:.2f} = {med-c:+.2f}")
print(f"   DI 2 anos (DIPRE 24M): 15/10 12,660 - 14/10 12,468 = {12.660-12.468:+.2f}")
print(f"   Brent 06/10 125,44 contra 02/10 135,51: {(125.44/135.51-1)*100:+.1f}%")
print(f"   CDS: 02/10 131,04 - 16/09 111,62 = {131.04-111.62:+.2f}; 14/10 112,19 - 16/09 111,62 = {112.19-111.62:+.2f}")
print(f"   PTAX 05/10 4,986 contra 02/10 5,224: {(4.986/5.224-1)*100:+.1f}%; DI 2a 05/10 12,587 - 02/10 13,687 = {12.587-13.687:+.2f}; NTN-B 10a 05/10 7,010 - 02/10 7,505 = {7.010-7.505:+.2f}")
print(f"   CDS 05/10 118,85 - 02/10 131,04 = {118.85-131.04:+.2f}")
