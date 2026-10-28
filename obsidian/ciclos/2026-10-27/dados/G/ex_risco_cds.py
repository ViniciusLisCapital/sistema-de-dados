"""G externo: o cenário de risco com o CDS carregando só o seu componente global (regressão trimestral
2016-2026 de ex_subordinado.py: ΔCDS = a + 12,42·Δlog dólar EM − 0,674·Δlog S&P, sem a constante), contra o
CDS no padrão do simulador. Ilustração para o fiscal (XS5) e o câmbio; não é caminho de referência."""
import numpy as np
from analytics.agent_system import modelo
import ex_cenarios as C
sim = modelo.carregar("2026-10-27"); T = C.TRIS
cds0, em0, sp0 = 131.21, 129.38, 7651.54  # 3T26, do retrato do modelo (listar)
def cds_global(cam):
    return {t: round(cds0 + 12.42*100*np.log(cam["dxy_em"][t]/em0) - 0.674*100*np.log(cam["sp500"][t]/sp0), 1) for t in T}
def linha(res, chave):
    ln = [l for l in modelo.texto(res, T).splitlines() if l.startswith(chave)][0]
    return " ".join(c.split(" [")[0].strip() for c in ln.split("|")[3:9])
for nome, cam in [("base", C.caminhos()), ("risk-off", C.caminhos(risco="up")), ("risk-on", C.caminhos(risco="down"))]:
    f = cds_global(cam)
    print(f"{nome}: CDS com componente global = " + " ".join(f"{t}={f[t]}" for t in T))
    print("   PTAX, CDS no padrão  :", linha(modelo.rodar(sim, caminhos=cam), "| PTAX"))
    c2 = dict(cam); c2["fiscal"] = f
    r = modelo.rodar(sim, caminhos=c2)
    print("   PTAX, CDS global     :", linha(r, "| PTAX"))
    print("   IPCA 12m, CDS global :", linha(r, "| IPCA acumulado"))
