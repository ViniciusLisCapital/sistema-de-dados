"""Expectativas: os cenários do report (etapa 1) e os temperos (i) na própria equação (E).

Base = o padrão do simulador (rodada 1: expectativas não é principal de nenhuma exógena).
Upside e downside: caminhos de CDS (`fiscal`) e vol implícita (`vol`) como CONDIÇÃO das caudas;
não são deste agente e não vão para o JSON.
"""
from analytics.agent_system import modelo

sim = modelo.carregar("2026-10-27")
Q = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
cen = {
    "base": ({}, {}),
    "base · E.e1×1,2": ({}, {"E.e1": 1.2}),
    "upside (CDS 190, vol 18)": ({"fiscal": {"4T26": 190}, "vol": {"4T26": 18}}, {}),
    "upside · E.e1×1,3 e E.e2×1,3": ({"fiscal": {"4T26": 190}, "vol": {"4T26": 18}},
                                     {"E.e1": 1.3, "E.e2": 1.3}),
    "downside (CDS 110, vol 11)": ({"fiscal": {"4T26": 110}, "vol": {"4T26": 11}}, {}),
    "downside · E.e1×0,8": ({"fiscal": {"4T26": 110}, "vol": {"4T26": 11}}, {"E.e1": 0.8}),
}
for nome, (cam, mult) in cen.items():
    res = modelo.rodar(sim, caminhos=cam, mult=mult)
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
