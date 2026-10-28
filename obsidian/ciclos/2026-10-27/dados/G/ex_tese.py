"""G externo: a tabela da tese (central = caminho base; faixa = metade da distância até o caminho do cenário
de cauda, com uma meia-largura mínima por variável; probabilidades = as do cenário do bloco). Grava o rascunho
do JSON de caminhos em G/ex_tese_externo_r1.json (copiado depois para caminhos/). Lê ex_cenarios.py."""
import json
from pathlib import Path
import ex_cenarios as C
T = C.TRIS
cen = {"eua": {s: C.caminhos(eua=s) for s in ["base","up","down"]},
       "risco": {s: C.caminhos(risco=s) for s in ["base","up","down"]},
       "comm": {s: C.caminhos(comm=s) for s in ["base","up","down"]}}
BLOCO = {"ffr":"eua","infl_us":"eua","dxy_em":"risco","sp500":"risco","icbr_usd":"comm","icbr_agr_usd":"comm","icbr_met_usd":"comm"}
# probabilidades por bloco: (base, cenário 'up' do bloco, cenário 'down' do bloco)
PROB = {"eua": (50, 30, 20), "risco": (55, 25, 20), "comm": (55, 20, 25)}
# no bloco de risco, o cenário 'up' (risk-off) é o upside do dólar EM e o DOWNSIDE do S&P
INVERTE = {"sp500"}
MINHW = {"ffr": ("abs", 0.12), "infl_us": ("abs", 0.15), "dxy_em": ("rel", 0.010), "sp500": ("rel", 0.03),
         "icbr_usd": ("rel", 0.025), "icbr_agr_usd": ("rel", 0.020), "icbr_met_usd": ("rel", 0.030)}
CASAS = {"ffr":2,"infl_us":2,"dxy_em":1,"sp500":0,"icbr_usd":1,"icbr_agr_usd":1,"icbr_met_usd":1}
tese = {}; caminhos = {}
for v, bl in BLOCO.items():
    pb, pu, pd_ = PROB[bl]
    if v in INVERTE: pu, pd_ = pd_, pu
    caminhos[v] = {}; tese[v] = {"trimestres": {}}
    for t in T:
        b = cen[bl]["base"][v][t]; up = cen[bl]["up"][v][t]; dn = cen[bl]["down"][v][t]
        hi_s, lo_s = (dn, up) if v in INVERTE else (up, dn)
        kind, m = MINHW[v]; mh = m if kind == "abs" else m*b
        hi = max(b + (hi_s-b)/2, b + mh); lo = min(b - (b-lo_s)/2, b - mh)
        k = CASAS[v]; r = (lambda x: round(x, k) if k else int(round(x)))
        caminhos[v][t] = r(b)
        pf, pup, pdn = pb, pu, pd_
        if v == "infl_us" and t not in ("4T26", "1T27"):  # o ruído trimestral do CPI (dp 0,30) pesa mais que a distância entre cenários
            pf, pup, pdn = 45, 30, 25
        tese[v]["trimestres"][t] = {"central": r(b), "faixa": [r(lo), r(hi)], "p_faixa": pf, "p_upside": pup, "p_downside": pdn}
        print(f"{v:13s} {t}: central {r(b)} faixa {r(lo)} a {r(hi)} · P {pf}/{pup}/{pdn} · up-scen {hi_s} down-scen {lo_s}")
out = {"agente":"externo","rodada":"r1","ciclo":"2026-10-27","caminhos":caminhos,"tese":tese,
       "nota":"Rodada 1. Três blocos (Política dos EUA; Risco e dólar; Commodities), cada um com base/upside/downside. Caminhos montados por G (ex_cenarios.py) a partir de caminhos mensais de Brent, núcleo do CPI e grupos do IC-Br."}
Path(__file__).with_name("ex_tese_externo_r1.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
