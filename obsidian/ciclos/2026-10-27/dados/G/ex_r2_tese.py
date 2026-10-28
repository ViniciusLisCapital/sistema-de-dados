"""G externo, rodada 2: a tabela da tese (central = caminho base de ex_r2_cenarios.py; faixa = metade da
distância até o caminho do cenário de cauda do bloco, com a meia-largura mínima da r1; probabilidades por
linha, as do cenário do bloco com os ajustes ditos no report). Grava G/ex_tese_externo_r2.json."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ex_r2_cenarios as R
T = R.T
cen = {"eua": {s: R.caminhos(eua=s) for s in ["base", "up", "down"]},
       "risco": {s: R.caminhos(risco=s) for s in ["base", "up", "down"]},
       "comm": {s: R.caminhos(comm=s) for s in ["base", "up", "down"]}}
BLOCO = {"ffr": "eua", "infl_us": "eua", "dxy_em": "risco", "sp500": "risco", "icbr_usd": "comm", "icbr_agr_usd": "comm", "icbr_met_usd": "comm"}
# (p_faixa, p_upside, p_downside) por variável; o sp500 tem o risk-off como downside
PROB = {"ffr": (55, 30, 15), "infl_us": (55, 30, 15), "dxy_em": (55, 28, 17), "sp500": (55, 20, 25),
        "icbr_usd": (55, 25, 20), "icbr_agr_usd": (55, 25, 20), "icbr_met_usd": (50, 20, 30)}
PROB_INFL_RUIDO = (50, 30, 20)  # infl_us de 2T27 em diante: o ruído trimestral do CPI pesa mais que a distância entre cenários
INVERTE = {"sp500"}
MINHW = {"ffr": ("abs", 0.12), "infl_us": ("abs", 0.15), "dxy_em": ("rel", 0.010), "sp500": ("rel", 0.03),
         "icbr_usd": ("rel", 0.025), "icbr_agr_usd": ("rel", 0.020), "icbr_met_usd": ("rel", 0.030)}
CASAS = {"ffr": 2, "infl_us": 2, "dxy_em": 1, "sp500": 0, "icbr_usd": 1, "icbr_agr_usd": 1, "icbr_met_usd": 1}
tese, caminhos = {}, {}
for v, bl in BLOCO.items():
    caminhos[v] = {}; tese[v] = {"trimestres": {}}
    for t in T:
        b = cen[bl]["base"][v][t]; up = cen[bl]["up"][v][t]; dn = cen[bl]["down"][v][t]
        hi_s, lo_s = (dn, up) if v in INVERTE else (up, dn)
        kind, m = MINHW[v]; mh = m if kind == "abs" else m*b
        hi = max(b + (hi_s-b)/2, b + mh); lo = min(b - (b-lo_s)/2, b - mh)
        k = CASAS[v]; r = (lambda x: round(x, k) if k else int(round(x)))
        pf, pu, pdn = PROB_INFL_RUIDO if (v == "infl_us" and t not in ("4T26", "1T27")) else PROB[v]
        if v == "icbr_agr_usd" and t == "4T26":  # no 4T26 os cenários do agro ainda caem dentro da faixa mínima: as caudas vêm do ruído
            pf, pu, pdn = 70, 15, 15
        caminhos[v][t] = r(b)
        tese[v]["trimestres"][t] = {"central": r(b), "faixa": [r(lo), r(hi)], "p_faixa": pf, "p_upside": pu, "p_downside": pdn}
        print(f"{v:13s} {t}: central {r(b)} faixa {r(lo)} a {r(hi)} · P {pf}/{pu}/{pdn} · up-scen {hi_s} down-scen {lo_s}")
out = {"agente": "externo", "rodada": "r2", "ciclo": "2026-10-27", "caminhos": caminhos, "tese": tese,
       "nota": "Rodada 2. Três blocos (Política dos EUA; Risco e dólar; Commodities). Muda contra a r1: o agro sai do Brent e do dólar EM pela ligação mensal medida (ex_r2_agro_brent.py), o que move o agro e o IC-Br total; probabilidades revistas com as notícias da rodada 1 (FOMC, Hormuz, minério) e o salto mecânico do real no dólar EM. O dólar EM é escrito sem o salto mecânico do real de 26/10."}
Path(__file__).with_name("ex_tese_externo_r2.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
