"""Expectativas: as contas pequenas citadas no report r1 (diferenças entre números de tabelas e de outros G).

Valores digitados aqui vêm do F_expectativas.md (23/10 e 26/10) e das saídas de xp_cenarios,
xp_trajetoria_pesquisa e xp_recente; a PTAX de 05/10 e a implícita são relidas de A/.
"""
from pathlib import Path
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"
modelo_base = [4.16, 3.97, 3.78, 3.67, 3.59, 3.52]
sem_revisao = [4.47, 4.17, 3.93, 3.88, 3.87, 3.70]
Q = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
print("trajetória sem revisão − central:", {q: round(a - b, 2) for q, a, b in zip(Q, sem_revisao, modelo_base)})
ipca_base = [5.28, 4.85, 4.33, 4.34, 4.23, 4.08]; ipca_up = [5.32, 4.99, 4.53, 4.58, 4.45, 4.24]
foc_up = [4.17, 4.00, 3.83, 3.74, 3.66, 3.59]
print("IPCA 12m upside − base:", [round(a - b, 2) for a, b in zip(ipca_up, ipca_base)])
print("Focus upside − base:", [round(a - b, 2) for a, b in zip(foc_up, modelo_base)])
print(f"PTAX upside/base 4T26: {(5.60/5.21-1)*100:.1f}%")
print(f"Focus câmbio 2026 (5,05) contra PTAX 26/10 (5,5007): {5.5007-5.05:.2f}")
print(f"Copom 1T28 3,2 contra Focus 4,03 e QPC 4,00: {4.03-3.2:.2f} e {4.00-3.2:.2f}")
print(f"faixa de cima contra upside com tempero: 4T26 {4.52-4.45:.2f}, 1T28 {4.53-3.75:.2f}")
pt = pd.read_csv(A / "cmb_ptax.csv.gz"); pt = pt[pt.name == "ptax_venda"].set_index("date").value
p02, p05, p23 = pt["2026-10-02"], pt["2026-10-05"], pt["2026-10-23"]
print(f"PTAX 02/10 {p02:.4f} → 05/10 {p05:.4f} ({(p05/p02-1)*100:+.2f}%) → 23/10 {p23:.4f}; devolvido {(p23-p05)/(p02-p05)*100:.0f}% da queda")
i02, i05, i23 = 5.89, 5.24, 5.46  # implícita 24M (xp_recente)
print(f"implícita 2a: queda {i05-i02:+.2f}, devolvido {(i23-i05)/(i02-i05)*100:.0f}%")
print(f"Selic 2028 Δ 4 sem −0,50 contra IPCA 2028 Δ −0,05; serviços painel 65 contra 124")
