"""fi: quanto o Modelo Estrutural põe na PTAX de 4T26 por um CDS 18,2 p.b. acima (o salto de 26/10) e por
um CDS de 137 (o último dado), contra o padrão; e que multiplicador em F.b_fiscal faria o CDS de 26/10 explicar
a alta de 9,2% da PTAX no mesmo dia (cmb_ptax, 23/10 -> 26/10)."""
import sys
from analytics.agent_system import modelo
sys.stdout.reconfigure(encoding="utf-8")
sim = modelo.carregar("2026-10-27")
ptax = lambda res: res["endogenas"]["ptax"]["central"][0]
p0 = ptax(modelo.rodar(sim, faixa=False))
cds0 = 131.21
for nome, v in [("CDS +18,2 p.b. (salto de 26/10)", cds0 + 18.2), ("CDS 137,4 (26/10)", 137.43), ("CDS 140 (base)", 140)]:
    p1 = ptax(modelo.rodar(sim, caminhos={"fiscal": {"4T26": v}}, faixa=False))
    print(f"{nome}: PTAX 4T26 {p1:.3f} contra {p0:.3f} no padrão = {100*(p1/p0-1):+.2f}%")
for m in [1.2, 1.5, 2, 3, 4, 5, 6]:
    p1 = ptax(modelo.rodar(sim, caminhos={"fiscal": {"4T26": cds0 + 18.2}}, mult={"F.b_fiscal": m}, faixa=False))
    print(f"  x{m}: {100*(p1/p0-1):+.2f}%")
# o episódio de 05/10: CDS -12,2 p.b. e PTAX -4,55% (02/10 -> 05/10)
p1 = ptax(modelo.rodar(sim, caminhos={"fiscal": {"4T26": cds0 - 12.2}}, faixa=False))
print(f"CDS -12,2 p.b. (05/10): PTAX 4T26 {100*(p1/p0-1):+.2f}% no modelo, contra -4,55% no dia")
for nome, dp, dc in [("05/10", -4.55, -12.2), ("26/10", 9.19, 18.2)]:
    print(f"{nome}: PTAX por p.b. de CDS no dia = {dp/dc:.2f}% ; no modelo = {1.55/18.2:.3f}% ; razão = {(dp/dc)/(1.55/18.2):.1f}x")
