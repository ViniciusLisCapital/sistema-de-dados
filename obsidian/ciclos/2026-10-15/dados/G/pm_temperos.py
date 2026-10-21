"""G pm: o efeito de cada multiplicador candidato a tempero (i) na Selic de fechamento derivada,
nos cenários do report (caminhos copiados de pm_cenarios.py). Só a central (sem faixa). Ciclo 2026-10-15."""
from analytics.agent_system import modelo

TRI = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]


def cam(**kw):
    return {k: dict(zip(TRI, v)) for k, v in kw.items()}


BASE = cam(meta_12m=[3.00] * 6, rr_10a=[6.89] + [6.87] * 5, fiscal=[112] * 6, ffr=[3.88] * 6,
           dxy_em=[129.77] * 6, icbr_usd=[205.70] * 6, icbr_agr_usd=[201.80] * 6, icbr_met_usd=[335.06] * 6)
WORST = cam(meta_12m=[3.00] * 6, rr_10a=[7.30] + [7.80] * 5, fiscal=[135] + [150] * 5,
            ffr=[3.88] + [4.13] * 5, dxy_em=[132] + [133] * 5, icbr_usd=[205.70] * 6,
            icbr_agr_usd=[206] + [212] * 5, icbr_met_usd=[335.06] * 6)
BEST = cam(meta_12m=[3.00] * 6, rr_10a=[6.75, 6.50] + [6.30] * 4, fiscal=[105] + [95] * 5,
           ffr=[3.88] + [3.63] * 5, dxy_em=[128] + [126] * 5, icbr_usd=[205.70] * 6,
           icbr_agr_usd=[198] + [192] * 5, icbr_met_usd=[335.06] * 6)
sim = modelo.carregar("2026-10-15")


def fim(c, m=None):
    r = modelo.rodar(sim, caminhos=c, mult=m or {}, faixa=False)
    return r["endogenas"]["selic_fim"]["central"][:6], r["mult"]


for nome, c, cands in [("worst", WORST, [{"R.t3": 1.3}, {"E.e2": 1.3}, {"R.t3": 1.3, "E.e2": 1.3}]),
                       ("best", BEST, [{"H.h2": 1.5}, {"E.e1": 0.8}, {"I.IS.is2": 1.5}])]:
    ref, _ = fim(c)
    print(f"{nome} sem tempero: " + " · ".join(f"{q} {v:.2f}" for q, v in zip(TRI, ref)))
    for m in cands:
        v, info = fim(c, m)
        pos = "; ".join(f"{i['chave']} {i['mediana']:.3f}→{i['multiplicado']:.3f}, intervalo {i['intervalo'][0]:.3f} a "
                        f"{i['intervalo'][1]:.3f}, percentil {i['percentil']:.0f}" for i in info)
        print(f"  {m}: " + " · ".join(f"{q} {a:.2f} ({a - b:+.2f})" for q, a, b in zip(TRI, v, ref)) + f"  [{pos}]")
