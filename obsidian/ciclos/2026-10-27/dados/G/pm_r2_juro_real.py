"""Insumo de subordinado em rr_10a (rodada 2): quanto da alta da NTN-B de 10 anos é caminho de
política (os dois primeiros anos) e quanto é prêmio longo. Lê só A/.

A NTN-B de 10 anos é, aproximadamente, a média dos juros reais a termo nos dez anos:
10·r10 ≈ 1·r1 + 1·f(1,2) + 3·f(2,5) + 5·f(5,10) (em log). A contribuição de cada trecho para a
variação de r10 é peso/10 × variação do termo do trecho. Também: o juro real de política que a
Focus espera (Selic do ano contra o IPCA do ano) e a distância da NTN-B 10a até ele."""
import numpy as np
import pandas as pd
from pathlib import Path

A = Path(__file__).resolve().parent.parent / "A"
bi = pd.read_csv(A / "br_interest_rate.csv.gz")
pv = bi.pivot_table(index="date", columns=["curve", "tenor"], values="value")
n = {y: pv[("NTNBJS", t)] for y, t in [(1, "12M"), (2, "24M"), (5, "60M"), (10, "120M")]}

def lg(d, y):
    return np.log1p(n[y].loc[d] / 100) * y

def trechos(d):
    out = {"0-1": lg(d, 1), "1-2": lg(d, 2) - lg(d, 1), "2-5": (lg(d, 5) - lg(d, 2)) / 3,
           "5-10": (lg(d, 10) - lg(d, 5)) / 5}
    return {k: (np.expm1(v) * 100) for k, v in out.items()}

W = {"0-1": 1, "1-2": 1, "2-5": 3, "5-10": 5}
for a, b in [("2026-10-23", "2026-10-26"), ("2026-09-30", "2026-10-26"), ("2026-10-02", "2026-10-05")]:
    ta, tb = trechos(a), trechos(b)
    d10 = (n[10].loc[b] - n[10].loc[a]) * 100
    print(f"\n{a} -> {b}: NTN-B 10a {n[10].loc[a]:.2f} -> {n[10].loc[b]:.2f} ({d10:+.0f} p.b.)")
    soma = 0
    for k in W:
        c = W[k] / 10 * (tb[k] - ta[k]) * 100
        soma += c
        print(f"  trecho {k:>4} anos: termo {ta[k]:.2f} -> {tb[k]:.2f} ({(tb[k]-ta[k])*100:+.0f} p.b.) · contribuição {c:+.0f} p.b.")
    print(f"  soma das contribuições {soma:+.0f} p.b. (aproximação em log)")

# média do 3T26 e do 4T26 até 26/10
r10 = n[10]
print(f"\nNTN-B 10a: média 3T26 {r10['2026-07-01':'2026-09-30'].mean():.2f} · média 01-23/10 {r10['2026-10-01':'2026-10-23'].mean():.2f}"
      f" · média 4T26 até 26/10 {r10['2026-10-01':].mean():.2f} ({len(r10['2026-10-01':])} pregões)")

# juro real de política esperado pela Focus (pesquisa de 23/10)
fs = pd.read_csv(A / "expc_focus_periodo__selic.csv.gz")
fi = pd.read_csv(A / "expc_focus_periodo__ipca.csv.gz")
print("\nFocus 23/10, colunas:", fs.columns.tolist())
