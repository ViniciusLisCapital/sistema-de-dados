"""G cambio: (1) os dois pregões de salto (05/10 e 26/10) em real, CDS, DI 1 e 2 anos, DXY, S&P 500;
(2) quanto do salto de 22/10 a 26/10 o Modelo Estrutural explica pelo CDS (4T26 com o CDS de 22/10 contra o de 26/10);
(3) a aritmética dos temperos (ii) sobre a saída do modelo; (4) Brent médio de setembro e de outubro."""
import pandas as pd
from pathlib import Path
from analytics.agent_system import modelo

A = Path(__file__).resolve().parent.parent / "A"
def ler(t): return pd.read_csv(A / f"{t}.csv.gz", parse_dates=["date"])
pt = ler("cmb_ptax"); pt = pt[pt.name == "ptax_venda"].set_index("date").value
cds = ler("cmb_risco_pais"); cds = cds[cds.name == "cds_5y_usd"].set_index("date").value
dxy = ler("cmb_dollar_index").set_index("date").value
sp = ler("cmb_equity_us").set_index("date").value
di = ler("br_di_grade")
def di_p(dc): return di[(di.dc >= dc-20) & (di.dc <= dc+20)].assign(x=lambda d: (d.dc-dc).abs()).sort_values("x").groupby("date").first().value
d1, d2 = di_p(365), di_p(730)
for a, b in [("2026-10-02", "2026-10-05"), ("2026-10-23", "2026-10-26")]:
    print(f"{a} -> {b}: BRL {100*(pt[b]/pt[a]-1):+.2f}% | CDS {cds[b]-cds[a]:+.1f} p.b. | DI1a {100*(d1[b]-d1[a]):+.0f} p.b. | DI2a {100*(d2[b]-d2[a]):+.0f} p.b. | DXY {100*(dxy[b]/dxy[a]-1):+.2f}% | S&P {100*(sp[b]/sp[a]-1):+.2f}%")
print(f"BRL de 05/10 a 22/10: {100*(pt['2026-10-22']/pt['2026-10-05']-1):+.2f}%; de 02/10 a 22/10: {100*(pt['2026-10-22']/pt['2026-10-02']-1):+.2f}%")

sim = modelo.carregar("2026-10-27")
T = ["4T26"]
r22 = modelo.rodar(sim, caminhos={"fiscal": {"4T26": float(cds["2026-10-22"])}})
r26 = modelo.rodar(sim, caminhos={"fiscal": {"4T26": float(cds["2026-10-26"])}})
def ptax4(r):
    t = modelo.texto(r, trimestres=T)
    linha = [l for l in t.splitlines() if l.startswith("| PTAX")][0]
    return float(linha.split("|")[3].split("[")[0].strip().replace(",", "."))
a, b = ptax4(r22), ptax4(r26)
print(f"\nModelo, 4T26 com CDS de 22/10 ({cds['2026-10-22']:.1f}): {a:.3f}; com CDS de 26/10 ({cds['2026-10-26']:.1f}): {b:.3f}; efeito {100*(b/a-1):+.2f}% contra {100*(pt['2026-10-26']/pt['2026-10-22']-1):+.2f}% observado")

print("\nTemperos (ii) sobre o modelo:")
up = {"4T26": 5.829, "1T27": 5.911}
print(f"upside 4T26: 5,829 × (1 + 2% posicionamento − 1,5% BC) = {5.829*(1+0.02-0.015):.3f}")
print(f"upside 1T27: 5,911 × (1 + 1% − 1%) = {5.911*(1+0.01-0.01):.3f}")
print(f"base 4T26 com a sazonalidade de dezembro (+2,1%, média do resíduo do 4T desde 2017): 5,381 × 1,021 = {5.381*1.021:.3f}")
print(f"base 4T27 idem: 5,350 × 1,021 = {5.350*1.021:.3f}")
print(f"spot 26/10 contra a central do 4T26: {100*(5.5007/5.381-1):+.2f}%")

br = ler("comm_brent").set_index("date").value
print(f"\nBrent médio set/26 {br['2026-09'].mean():.2f}; out/26 até {br.index.max().date()} {br['2026-10'].mean():.2f}; {100*(br['2026-10'].mean()/br['2026-09'].mean()-1):+.1f}%")
