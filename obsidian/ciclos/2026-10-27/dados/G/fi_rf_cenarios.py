"""fi (report final): os três cenários fiscais no Modelo Estrutural com as outras exógenas no caminho do P2,
e as diferenças citadas no report final (base contra downside, para a pergunta S12 da PM; Selic contra a tese
da PM; rf contra P2)."""
import json
import sys
from pathlib import Path
from analytics.agent_system import modelo
sys.stdout.reconfigure(encoding="utf-8")
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
P2 = json.loads((Path(__file__).resolve().parents[2] / "P2.json").read_text(encoding="utf-8"))
base_p2 = P2["caminhos_usados"]
TT = list(base_p2["fiscal"].keys())
cen = {
    "base":     {"fiscal": [140, 142, 139, 135, 130, 125], "rr_10a": [7.75, 7.95, 7.90, 7.80, 7.75, 7.70]},
    "upside":   {"fiscal": [170, 205, 210, 205, 198, 190], "rr_10a": [8.15, 8.90, 9.10, 9.10, 9.00, 8.90]},
    "downside": {"fiscal": [122, 115, 112, 110, 108, 106], "rr_10a": [7.36, 7.30, 7.15, 7.05, 7.00, 6.95]},
}
def caminhos(d):
    c = {k: dict(v) for k, v in base_p2.items()}
    for k, vals in d.items():
        c[k] = dict(zip(TT, list(vals) + [vals[-1]] * (len(TT) - len(vals))))
    return c
sim = modelo.carregar("2026-10-27")
out = {}
for n, d in cen.items():
    r = modelo.rodar(sim, caminhos=caminhos(d), faixa=(n == "base"))
    print(f"\n=== {n.upper()} ===")
    print(modelo.texto(r, T))
print("\n=== UPSIDE com F.b_fiscal x 1,2 (o tempero que o câmbio aplica) ===")
print(modelo.texto(modelo.rodar(sim, caminhos=caminhos(cen["upside"]), mult={"F.b_fiscal": 1.2}, faixa=False), T))

f = lambda a, b: [round(x - y, 2) for x, y in zip(a, b)]
b, dn = cen["base"], cen["downside"]
print("\nS12 — base − downside: rr_10a", f(b["rr_10a"], dn["rr_10a"]), "· CDS", f(b["fiscal"], dn["fiscal"]))
print("Impulso base − downside (p.p. do PIB):", f([0.1, 0.0, -0.1, -0.1, -0.2, -0.3], [0.0, -0.2, -0.3, -0.4, -0.5, -0.5]))
print("rr_10a rf − P2 (4T26):", round(7.75 - 7.72, 2), "· 1T27 − 3T26 (7,84):", round(7.95 - 7.84, 2),
      "· 1T28 − 1T27:", round(7.70 - 7.95, 2), "· prêmio 1T27 sobre o Focus 2028–29:", round(7.95 - 6.02, 2), round(7.95 - 6.28, 2))
print("RTN sem precatórios 12m (+0,29) − meta 2026 (0,25):", round(0.29 - 0.25, 2), "· − piso (0,00):", 0.29)
