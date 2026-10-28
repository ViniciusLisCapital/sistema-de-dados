"""fi (rodada 2): os três cenários fiscais no Modelo Estrutural, com as outras exógenas no caminho do P1
(o dos principais), mais: o base com o caminho de referência de `rr_10a` da política monetária, o base do
rodada 1, e os dois multiplicadores de F.b_fiscal argumentados ao câmbio."""
import json
import sys
from pathlib import Path
from analytics.agent_system import modelo
sys.stdout.reconfigure(encoding="utf-8")
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
P1 = json.loads((Path(__file__).resolve().parents[2] / "P1.json").read_text(encoding="utf-8"))
base_p1 = P1["caminhos_usados"]
TT = list(base_p1["fiscal"].keys())

cen = {
    "base":     {"fiscal": [140, 143, 140, 137, 134, 130], "rr_10a": [7.72, 8.00, 8.00, 7.95, 7.90, 7.85]},
    "upside":   {"fiscal": [170, 205, 210, 205, 198, 190], "rr_10a": [8.15, 8.90, 9.10, 9.10, 9.00, 8.90]},
    "downside": {"fiscal": [122, 115, 112, 110, 108, 106], "rr_10a": [7.36, 7.30, 7.15, 7.05, 7.00, 6.95]},
    "base_r1":  {"fiscal": [140, 140, 138, 135, 135, 135], "rr_10a": [7.70, 7.80, 7.70, 7.60, 7.55, 7.50]},
    "base_rr_PM": {"fiscal": [140, 143, 140, 137, 134, 130], "rr_10a": [7.76, 8.05, 8.05, 8.05, 8.05, 8.05]},
}

def caminhos(d):
    c = {k: dict(v) for k, v in base_p1.items()}
    for k, vals in d.items():
        full = list(vals) + [vals[-1]] * (len(TT) - len(vals))
        c[k] = dict(zip(TT, full))
    return c

sim = modelo.carregar("2026-10-27")
lst = modelo.listar(sim)
print("\n".join(l for l in str(lst).splitlines() if "b_fiscal" in l or "fiscal" in l.lower()))
for n, d in cen.items():
    print(f"\n=== {n.upper()} ===")
    print(modelo.texto(modelo.rodar(sim, caminhos=caminhos(d), faixa=(n in ("base", "upside", "downside"))), T))
print("\n=== BASE com F.b_fiscal x 1,2 ===")
print(modelo.texto(modelo.rodar(sim, caminhos=caminhos(cen["base"]), mult={"F.b_fiscal": 1.2}, faixa=False), T))
print("\n=== UPSIDE com F.b_fiscal x 1,5 ===")
print(modelo.texto(modelo.rodar(sim, caminhos=caminhos(cen["upside"]), mult={"F.b_fiscal": 1.5}, faixa=False), T))
