"""Expectativas, report final: os cenários (etapa 1) com os caminhos do P2 e os temperos (i) na (E).

Base = os caminhos usados no P2 (os dos principais, depois da moderação), lidos de ../../P2.json.
Upside e downside = o base do P1 com os caminhos de CAUDA que os próprios principais escreveram
na rodada 2: `fiscal` e `rr_10a` do agente fiscal (fiscal_r2.md, 3.1) e `vol` do agente de câmbio
(cambio_r2.md, 3.1). Este agente não escreve caminho de exógena: são a condição das caudas.
A posição de cada multiplicador no posterior da (E) sai na linha 'mult' de cada cenário.
"""
import json
from pathlib import Path
from analytics.agent_system import modelo

P1 = json.loads((Path(__file__).resolve().parents[2] / "P2.json").read_text(encoding="utf-8"))
base = P1["caminhos_usados"]
Q = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]

def com(**over):
    c = {k: dict(v) for k, v in base.items()}
    for k, serie in over.items():
        for q, x in zip(Q, serie):
            c[k][q] = x
        for q in list(c[k]):          # depois do 1T28, segura o último valor da cauda
            if q not in Q:
                c[k][q] = serie[-1]
    return c

up = com(fiscal=[170, 205, 210, 205, 198, 190], rr_10a=[8.15, 8.90, 9.10, 9.10, 9.00, 8.90],
         vol=[24.0, 21.0, 18.0, 16.0, 15.0, 15.0])
dn = com(fiscal=[122, 115, 112, 110, 108, 106], rr_10a=[7.36, 7.30, 7.15, 7.05, 7.00, 6.95],
         vol=[13.0, 12.5, 12.0, 12.0, 12.0, 12.0])

sim = modelo.carregar("2026-10-27")

cen = {
    "base (P2)": (base, {}),
    "base · E.e1×1,2": (base, {"E.e1": 1.2}),
    "base · E.e1×1,1": (base, {"E.e1": 1.1}),
    "upside (caudas de fiscal e câmbio)": (up, {}),
    "upside · E.e1×1,3 e E.e2×1,3": (up, {"E.e1": 1.3, "E.e2": 1.3}),
    "upside · E.e1×1,2 e E.e2×1,3": (up, {"E.e1": 1.2, "E.e2": 1.3}),
    "downside (caudas de fiscal e câmbio)": (dn, {}),
    "downside · E.e1×0,8": (dn, {"E.e1": 0.8}),
}
R = {}
for nome, (cam, mult) in cen.items():
    res = modelo.rodar(sim, caminhos=cam, mult=mult)
    R[nome] = res
    print(f"\n=== {nome} · voltas {res['voltas']}")
    if res["mult"]:
        print("mult:", res["mult"])
    tri = res["trimestres"]
    for k in ["focus_12m", "ipca_12m", "ptax", "selic", "hiato"]:
        e = res["endogenas"][k]
        linha = []
        for q in Q:
            j = tri.index(q)
            linha.append(f"{q} {e['central'][j]:.2f} [{e['lo'][j]:.2f}; {e['hi'][j]:.2f}]")
        print(f"  {k}: " + " | ".join(linha))

# Diferenças citadas no report (por trimestre, 4T26 a 1T28)
def serie(nome, k):
    res = R[nome]; tri = res["trimestres"]
    return [res["endogenas"][k]["central"][tri.index(q)] for q in Q]
def dif(a, b):
    return " ".join(f"{x-y:+.2f}" for x, y in zip(a, b))
b, u, ut = "base (P2)", "upside (caudas de fiscal e câmbio)", "upside · E.e1×1,2 e E.e2×1,3"
for k in ["ptax", "ipca_12m", "focus_12m"]:
    print(f"\nupside − base, {k}: {dif(serie(u, k), serie(b, k))}")
lim_cima = [4.45, 4.15, 3.95, 3.90, 3.90, 3.75]
print("upside com tempero − limite de cima:", dif(serie(ut, "focus_12m"), lim_cima))
print("upside com tempero − meta (3,00):", dif(serie(ut, "focus_12m"), [3.0] * 6))
ipca_p1 = [5.32, 4.96, 4.48, 4.52, 4.38, 4.19]   # IPCA 12m do P1 (P1.md)
print("IPCA 12m, P2 − P1:", dif(serie(b, "ipca_12m"), ipca_p1))
print("Focus, P2 − P1:", dif(serie(b, "focus_12m"), [4.17, 4.00, 3.82, 3.72, 3.64, 3.57]))
for nm in ["base · E.e1×1,2", "upside · E.e1×1,2 e E.e2×1,3", "downside · E.e1×0,8"]:
    print(nm, "− base:", dif(serie(nm, "focus_12m"), serie(b, "focus_12m")))
print("downside com tempero − limite de baixo [4,05 3,80 3,60 3,50 3,40 3,30]:", dif(serie("downside · E.e1×0,8", "focus_12m"), [4.05, 3.80, 3.60, 3.50, 3.40, 3.30]))
