"""G pm: os três cenários do Modelo Estrutural para a política monetária (ciclo 2026-10-15),
sem e com os temperos (i), e a saída que o report usa (Selic de fechamento derivada, Selic média,
IPCA 12m, Focus 12m, hiato, PTAX). Caminhos em nível e na unidade de cada cartão do simulador."""
from analytics.agent_system import modelo

TRI = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]


def cam(**kw):
    return {k: dict(zip(TRI, v)) for k, v in kw.items()}


# Base: o nível de hoje de cada exógena (pm_exogenas_hoje.py), mantido.
# rr_10a é média do trimestre: 4T26 = média até 15/10 com o último valor mantido até 31/12.
BASE = cam(
    meta_12m=[3.00] * 6,
    rr_10a=[6.89, 6.87, 6.87, 6.87, 6.87, 6.87],
    fiscal=[112] * 6,
    ffr=[3.88] * 6,
    dxy_em=[129.77] * 6,
    icbr_usd=[205.70] * 6,
    icbr_agr_usd=[201.80] * 6,
    icbr_met_usd=[335.06] * 6,
)
# Worst: a queda de outubro no juro real longo se desfaz (volta à média do 3T26), o CDS sobe,
# o Fed sobe mais uma vez, o dólar se fortalece contra emergentes, El Niño encarece alimentos.
WORST = cam(
    meta_12m=[3.00] * 6,
    rr_10a=[7.30, 7.80, 7.80, 7.80, 7.80, 7.80],
    fiscal=[135, 150, 150, 150, 150, 150],
    ffr=[3.88, 4.13, 4.13, 4.13, 4.13, 4.13],
    dxy_em=[132, 133, 133, 133, 133, 133],
    icbr_usd=[205.70] * 6,
    icbr_agr_usd=[206, 212, 212, 212, 212, 212],
    icbr_met_usd=[335.06] * 6,
)
# Best: a queda de outubro se aprofunda, o CDS cai, o Fed devolve a alta de setembro, o dólar
# enfraquece contra emergentes, commodities agrícolas cedem.
BEST = cam(
    meta_12m=[3.00] * 6,
    rr_10a=[6.75, 6.50, 6.30, 6.30, 6.30, 6.30],
    fiscal=[105, 95, 95, 95, 95, 95],
    ffr=[3.88, 3.63, 3.63, 3.63, 3.63, 3.63],
    dxy_em=[128, 126, 126, 126, 126, 126],
    icbr_usd=[205.70] * 6,
    icbr_agr_usd=[198, 192, 192, 192, 192, 192],
    icbr_met_usd=[335.06] * 6,
)
MULT_WORST = {"R.t3": 1.3}   # a regra reage mais ao desvio da expectativa
MULT_BEST = {"E.e1": 0.9}    # a expectativa converge à meta mais depressa (menos inércia)

sim = modelo.carregar("2026-10-15")
SAI = ["selic_fim", "selic", "ipca_12m", "focus_12m", "hiato", "ptax"]
res = {}
for nome, c, m in [("base", BASE, None), ("worst", WORST, None), ("worst (i)", WORST, MULT_WORST),
                   ("best", BEST, None), ("best (i)", BEST, MULT_BEST)]:
    r = modelo.rodar(sim, caminhos=c, mult=m or {})
    res[nome] = r
    e = r["endogenas"]
    print(f"== {nome}")
    for k in SAI:
        cen = e[k]["central"][:6]
        lo, hi = e[k].get("lo", [None] * 6)[:6], e[k].get("hi", [None] * 6)[:6]
        print(f"  {k:10s} " + " · ".join(
            f"{q} {v:.2f} [{a:.2f}; {b:.2f}]" for q, v, a, b in zip(TRI, cen, lo, hi)))

print()
print(modelo.texto(res["base"]))
for n in ["worst (i)", "best (i)"]:
    print(f"Multiplicadores ({n}):", res[n]["mult"])
