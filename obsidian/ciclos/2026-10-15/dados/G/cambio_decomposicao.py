"""G · câmbio · ciclo 2026-10-15: de onde vem a variação da PTAX no cenário base do modelo.

Refaz a equação do câmbio com os pesos da mediana, sobre os caminhos do cenário base
(os mesmos de cambio_cenarios.py) e a Selic e a inflação que o modelo resolveu, e separa
a variação de cada trimestre (% em log) por canal: diferencial de inflação, constante,
inércia, CDS, dólar EM, carry/vol, S&P 500, IC-Br. Confere que a soma reproduz a PTAX do
modelo, e imprime o acumulado 3T26 → 4T26 e 3T26 → 1T28.
"""
import importlib.util
import math
import sys
from pathlib import Path

from analytics.agent_system import modelo

sys.stdout.reconfigure(encoding="utf-8")
G = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("cen", G / "cambio_cenarios.py")
# só os caminhos: lê o dicionário sem rodar o script inteiro
src = (G / "cambio_cenarios.py").read_text(encoding="utf-8")
ns = {}
exec(src.split("MULT =")[0], ns)
CEN, TRI = ns["CENARIOS"], ns["TRI"]

sim = modelo.carregar("2026-10-15")
p = sim["p"]
F = p["eq"]["F"]
i0 = p["i0"]
md, sd, logret = F["mediana"], F["sd"], set(F["log_ret"])

for nome in ("base", "worst", "best"):
    res = modelo.rodar(sim, caminhos=CEN[nome], faixa=False)
    ent = {k: v["caminho"] for k, v in res["entradas"].items()}
    selic = res["endogenas"]["selic"]["central"]
    infl_br = [100 * math.log(1 + x / 100) for x in res["endogenas"]["ipca_tri"]["central"]]
    prev = {c: F["nivel"][c][i0 - 1] for c in F["canais"]}
    de_ant = F["y"][i0 - 1]
    ptax = F["ptax"][i0 - 1]
    acum = {}
    print(f"\n== {nome}: contribuição por canal, % em log no trimestre ==")
    print("| tri | infl BR−US | const | inércia | CDS | dólar EM | carry/vol | S&P | IC-Br | total | PTAX conta | PTAX modelo |")
    for k in range(6):
        parts = {"infl BR−US": infl_br[k] - ent["infl_us"][k], "const": md["alpha"],
                 "inércia": md["phi"] * de_ant}
        for c in F["canais"]:
            cur = ((selic[k] - ent["ffr"][k]) / ent["vol"][k] if c == "carry_vol" else ent[c][k])
            dz = 100 * (math.log(cur) - math.log(prev[c])) if c in logret else cur - prev[c]
            parts[c] = md["b_" + c] * dz / sd[c]
            prev[c] = cur
        tot = sum(parts.values())
        de_ant = tot
        ptax *= math.exp(tot / 100)
        for kk, v in parts.items():
            acum.setdefault(kk, []).append(v)
        print(f"| {TRI[k]} | " + " | ".join(f"{v:+.2f}" for v in parts.values())
              + f" | {tot:+.2f} | {ptax:.4f} | {res['endogenas']['ptax']['central'][k]:.4f} |")
    print("acumulado 3T26→4T26:", {kk: round(v[0], 2) for kk, v in acum.items()})
    print("acumulado 3T26→1T28:", {kk: round(sum(v), 2) for kk, v in acum.items()},
          "total", round(sum(sum(v) for v in acum.values()), 2))
    print("acumulado 4T26→1T28:", {kk: round(sum(v[1:]), 2) for kk, v in acum.items()},
          "total", round(sum(sum(v[1:]) for v in acum.values()), 2))
