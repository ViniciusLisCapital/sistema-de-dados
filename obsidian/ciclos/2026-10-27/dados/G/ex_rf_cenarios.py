"""G externo, report final: as mesmas rodadas do modelo de ex_r2_cenarios.py (meus caminhos sem mudança),
agora com as exógenas que não escrevo vindas do P2 (rr_10a e CDS do fiscal revistos na moderação); o
componente doméstico que o CDS do fiscal (P2) deixa implícito contra o componente global do meu base; e as
contas de apoio do texto (salto mecânico do real com o fechamento de 27/10 noticiado, R$ 5,35).
Lê só ../A/, o retrato do modelo e ../../P2.json."""
import json, sys
import numpy as np
from pathlib import Path
from analytics.agent_system import modelo
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ex_r2_cenarios as R
T = R.T
P2 = json.loads((Path(__file__).resolve().parents[2]/"P2.json").read_text(encoding="utf-8"))
R.OUTROS = {k: {t: P2["caminhos_usados"][k][t] for t in T} for k in ["meta_12m", "rr_10a", "fiscal", "vol"]}
for k, v in R.OUTROS.items(): print(k, v)
sim = modelo.carregar("2026-10-27")
base = R.caminhos()
cen = {"base": base, "EUA up": R.caminhos(eua="up"), "EUA down": R.caminhos(eua="down"),
       "risk-off, CDS do fiscal": R.caminhos(risco="up"), "risk-on, CDS do fiscal": R.caminhos(risco="down"),
       "commodities alta": R.caminhos(comm="up"), "commodities queda": R.caminhos(comm="down"),
       "conjunto adverso": R.caminhos("up", "up", "down"), "conjunto petróleo": R.caminhos("up", "up", "up")}
ro = dict(cen["risk-off, CDS do fiscal"]); ro["fiscal"] = R.cds_global(ro, base); cen["risk-off, CDS + global"] = ro
rn = dict(cen["risk-on, CDS do fiscal"]); rn["fiscal"] = R.cds_global(rn, base); cen["risk-on, CDS + global"] = rn
bm = dict(base); bm["dxy_em"] = {t: round(v*1.0043, 2) for t, v in base["dxy_em"].items()}; cen["base + salto do real (0,43%)"] = bm
print("CDS + global risk-off:", ro["fiscal"]); print("CDS + global risk-on:", rn["fiscal"])
r0 = modelo.rodar(sim, caminhos=dict(R.OUTROS))
print("minhas sete no padrão: PTAX", R.linha(r0, "| PTAX"), "| IPCA", R.linha(r0, "| IPCA acumulado"), "| Selic", R.linha(r0, "| Selic, média"))
for nome, cam in cen.items():
    full = dict(R.OUTROS); full.update(cam); res = modelo.rodar(sim, caminhos=full)
    print(f"{nome}: PTAX {R.linha(res, '| PTAX')} | IPCA {R.linha(res, '| IPCA acumulado')} | Selic {R.linha(res, '| Selic, média')}")
full = dict(R.OUTROS); full.update(base); rb = modelo.rodar(sim, caminhos=full)
pb = [float(v.replace(",", ".")) for v in R.linha(rb, "| PTAX").split()]
for k in ["ffr", "infl_us", "dxy_em", "sp500", "icbr_usd", "icbr_agr_usd", "icbr_met_usd"]:
    f2 = dict(full); f2.pop(k)
    pk = [float(v.replace(",", ".")) for v in R.linha(modelo.rodar(sim, caminhos=f2), "| PTAX").split()]
    print(f"  decomp {k}: 4T26 {pb[0]-pk[0]:+.3f} · 1T28 {pb[5]-pk[5]:+.3f}")
# CDS do fiscal (P2) contra o componente global do meu base
g = lambda cam, t: 12.42*100*np.log(cam["dxy_em"][t]/129.38) - 0.674*100*np.log(cam["sp500"][t]/7651.54)
for t in T:
    print(f"  CDS {t}: fiscal {R.OUTROS['fiscal'][t]:.0f}, global {g(base, t):+.1f}, doméstico implícito {R.OUTROS['fiscal'][t]-131.21-g(base, t):+.1f}")
print(f"salto mecânico com o real a 5,35 (27/10, notícia) contra 5,0377 (23/10), peso 0,072: {0.072*100*np.log(5.35/5.0377):+.2f}%")
