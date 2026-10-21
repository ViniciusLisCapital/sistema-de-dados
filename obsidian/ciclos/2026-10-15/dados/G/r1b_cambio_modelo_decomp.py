"""G r1b: quanto do movimento de outubro o modelo explica.
(a) PTAX 4T26 do modelo no padrão x com cada exógena levada, uma de cada vez, ao valor do corte;
(b) o multiplicador do efeito do CDS que levaria a PTAX 4T26 do modelo ao valor do corte (5,0441, cmb_ptax 14/10);
(c) efeito do CDS por p.b. no modelo (mediana) contra o observado de 30/09 a 14/10."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from analytics.agent_system import modelo
from r1b_cambio_modelo_base import BASE

sim = modelo.carregar("2026-10-15")
P = lambda cam, mult=None: modelo.rodar(sim, caminhos=cam, mult=mult or {})["endogenas"]["ptax"]["central"][0]
SPOT, P3T = 5.0441, 5.1809
p0 = P({})
pb = P(BASE)
print(f"(a) padrão 4T26 {p0:.4f} · base (corte) {pb:.4f} · Δ {100*(pb/p0-1):+.2f}% · observado 14/10 {SPOT} · Δ desde 30/09 obs {100*(SPOT/P3T-1):+.2f}%")
for k, v in BASE.items():
    pk = P({k: v})
    print(f"    só {k}: {pk:.4f} · contribuição {100*(pk/p0-1):+.2f}%")
print(f"    resíduo (observado 14/10 contra a base do modelo): {100*(SPOT/pb-1):+.2f}%")
print("(b) multiplicador do efeito do CDS, base:")
for m in [1.0, 1.22, 1.5, 2.0, 2.5, 3.0, 4.0]:
    print(f"    x{m}: 4T26 {P(BASE, {'F.b_fiscal': m}):.4f}")
# (c) efeito por p.b.: CDS +10 p.b. no 4T26 sobre a base
c10 = {**BASE, "fiscal": {t: v + 10 for t, v in BASE["fiscal"].items()}}
p10 = P(c10)
print(f"(c) modelo: +10 p.b. de CDS -> {100*(p10/pb-1):+.3f}% na PTAX 4T26 ({100*(p10/pb-1)/10:.3f}% por p.b.)")
print(f"    observado 30/09->14/10: CDS 131,21->112,19 (−19,0 p.b.), PTAX {100*(SPOT/P3T-1):+.2f}% ({100*(SPOT/P3T-1)/(112.19-131.21):.3f}% por p.b.)")
print(f"    observado 02/10->06/10: CDS 131,04->108,96 (−22,1 p.b.), PTAX 5,2244->4,9700 ({100*(4.9700/5.2244-1):+.2f}%, {100*(4.9700/5.2244-1)/(108.96-131.04):.3f}% por p.b.)")
