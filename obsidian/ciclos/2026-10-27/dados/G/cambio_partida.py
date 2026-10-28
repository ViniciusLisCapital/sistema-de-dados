"""G cambio (report final): o câmbio de partida da projeção do Copom de 04/11 (média da PTAX nos dez dias úteis
encerrados em 30/10, regra citada pela política monetária). O F tem a PTAX até 26/10: média dos dias que existem
e a média completa com os quatro pregões que faltam (27 a 30/10) em três níveis. Mais: distância ao condicionante."""
import pandas as pd
from pathlib import Path
A = Path(__file__).resolve().parent.parent / "A"
pt = pd.read_csv(A / "cmb_ptax.csv.gz", parse_dates=["date"])
pt = pt[pt.name == "ptax_venda"].set_index("date").value.sort_index()
dias = pt[(pt.index >= "2026-10-16") & (pt.index <= "2026-10-26")]
print(dias.to_string())
janela = pt[(pt.index >= "2026-10-19") & (pt.index <= "2026-10-26")]   # 19 a 26/10: 6 pregões
print("pregões na janela com dado:", len(janela), " média:", round(janela.mean(), 4))
for nivel in (5.35, 5.45, 5.50):
    m = (janela.sum() + 4 * nivel) / (len(janela) + 4)
    print(f"  27-30/10 a {nivel:.2f}: média de 10 dias {m:.4f}  contra 5,15: {100*(m/5.15-1):+.2f}%")
for v in (5.30, 5.427, 5.60):
    print(f"  {v:.3f} contra 5,15: {100*(v/5.15-1):+.2f}%")
