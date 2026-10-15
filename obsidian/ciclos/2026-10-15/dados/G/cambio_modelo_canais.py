"""G · câmbio · ciclo 2026-10-15: o que a equação do câmbio do Modelo Estrutural lê.

Imprime, do retrato do ciclo (A/modelo_estrutural.json): o desvio-padrão e a regra de
variação de cada canal, os níveis dos últimos trimestres da grade, a amostra de
estimação; e, das tabelas de A, os últimos dados diários das mesmas séries, para
comparar a convenção do modelo (fechamento do trimestre) com o dado de hoje.
"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
A = Path(__file__).resolve().parents[1] / "A"

p = json.loads((A / "modelo_estrutural.json").read_text(encoding="utf-8"))["p"]
F = p["eq"]["F"]
rot = p["rot"]
print("amostra de estimação:", F["est_ini"], "a", F["est_fim"])
print("canais:", F["canais"], "| log_ret:", F["log_ret"])
print("sd por canal:", F["sd"])
print("mediana:", F["mediana"])
print()
print("níveis dos últimos 6 trimestres da grade:")
for c in F["canais"]:
    print(f"  {c:10s}", [(r, v) for r, v in zip(rot[-6:], F["nivel"][c][-6:])])
print("  ptax      ", list(zip(rot[-6:], F["ptax"][-6:])))
print("  de (%)    ", list(zip(rot[-6:], F["y"][-6:])))
for k in ("ffr", "infl_us", "infl_br", "selic"):
    print(f"  {k:10s}", list(zip(rot[-6:], p["var"][k]["obs"][-6:])))
print()

# efeito, em % de PTAX no trimestre, de um movimento redondo de cada canal (pesos da mediana)
print("efeito no câmbio (% no trimestre, mediana) de:")
for c, mov, desc in (("fiscal", 10, "+10 p.b. no CDS"),
                     ("dxy_em", 1, "+1 ponto no dólar contra emergentes"),
                     ("sp500", 5, "+5% no S&P 500"),
                     ("icbr_usd", 5, "+5% no IC-Br em dólar"),
                     ("carry_vol", 0.1, "+0,1 no carry/vol")):
    print(f"  {desc}: {F['mediana']['b_' + c] * mov / F['sd'][c]:+.3f}")
print()


def ultimos(tab, n=8):
    df = pd.read_csv(A / f"{tab}.csv.gz")
    print(tab, list(df.columns))
    print(df.tail(n).to_string())
    print()


for tab in ("cmb_risco_pais", "cmb_dollar_index_em", "cmb_equity_us", "comm_icbr_usd",
            "us_interest_rate"):
    ultimos(tab)

# fechamento de 3T26 e média do trimestre do CDS na tabela do F
cds = pd.read_csv(A / "cmb_risco_pais.csv.gz")
print(cds.columns.tolist())
