"""G pm: quanto a Selic do modelo responde ao juro real de 10 anos (a âncora da regra), com as
outras exógenas no nível de hoje. Compara: NTN-B 10a no nível de 15/10 (6,87), mantida na média do
3T26 (7,84), e 1 p.p. a menos só a partir de 1T27. Ciclo 2026-10-15."""
from analytics.agent_system import modelo

TRI = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
OUTRAS = {"meta_12m": [3.00] * 6, "fiscal": [112] * 6, "ffr": [3.88] * 6, "dxy_em": [129.77] * 6,
          "icbr_usd": [205.70] * 6, "icbr_agr_usd": [201.80] * 6, "icbr_met_usd": [335.06] * 6}
sim = modelo.carregar("2026-10-15")


def run(rr):
    c = {k: dict(zip(TRI, v)) for k, v in (OUTRAS | {"rr_10a": rr}).items()}
    e = modelo.rodar(sim, caminhos=c, faixa=False)["endogenas"]
    return e["selic"]["central"][:6], e["selic_fim"]["central"][:6]


casos = {"rr 6,87 (hoje)": [6.89] + [6.87] * 5,
         "rr 7,84 (média 3T26)": [7.84] * 6,
         "rr 7,84 em 4T26, 6,84 depois": [7.84] + [6.84] * 5}
ref = None
for n, rr in casos.items():
    med, fim = run(rr)
    print(f"{n}: média " + " · ".join(f"{q} {v:.2f}" for q, v in zip(TRI, med)))
    print(f"{' ' * len(n)}  fecham. " + " · ".join(f"{q} {v:.2f}" for q, v in zip(TRI, fim)))
    if ref is None:
        ref = med
    else:
        print(f"{' ' * len(n)}  média − caso hoje " + " · ".join(f"{q} {a - b:+.2f}" for q, a, b in zip(TRI, med, ref)))
