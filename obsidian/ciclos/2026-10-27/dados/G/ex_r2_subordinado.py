"""G externo, rodada 2, como subordinado do CDS (principal: fiscal): o componente global do CDS no meu base
e nas caudas do bloco de risco (regressão trimestral 2016-2026 da r1, sem a constante, contra o fechamento do
3T26), o componente doméstico que o caminho do fiscal (P1) deixa implícito, o caminho de referência (o do fiscal
até o 2T27 e, depois, a variação do componente global desde o 2T27), e a probabilidade de a cauda de alta do
CDS acontecer se a cauda do fiscal e o meu risk-off forem independentes. Lê o P1.json e ex_r2_cenarios.py."""
import json, sys
import numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ex_r2_cenarios as R
T = R.T; f = R.OUTROS["fiscal"]; b1, b2 = 12.42, -0.674; cds0, em0, sp0 = 131.21, 129.38, 7651.54
g = lambda cam, t: b1*100*np.log(cam["dxy_em"][t]/em0) + b2*100*np.log(cam["sp500"][t]/sp0)
cb, co, cn = R.caminhos(), R.caminhos(risco="up"), R.caminhos(risco="down")
print("tri  | fiscal (P1) | global base | doméstico implícito | global risk-off | global risk-on | referência")
ref = {}
for t in T:
    gb = g(cb, t)
    ref[t] = f[t] if t in ("4T26", "1T27", "2T27") else round(f["2T27"] + gb - g(cb, "2T27"))
    print(f"{t} | {f[t]:.0f} | {gb:+.1f} | {f[t]-cds0-gb:+.1f} | {g(co, t):+.1f} | {g(cn, t):+.1f} | {ref[t]}")
print("referência:", ref)
P1 = json.loads((Path(__file__).resolve().parents[2]/"P1.json").read_text(encoding="utf-8"))
tf = json.loads((Path(__file__).resolve().parents[2]/"caminhos"/"fiscal_r1.json").read_text(encoding="utf-8"))["tese"]["fiscal"]["trimestres"]
for t in ["4T26", "1T27"]:
    pu = tf[t]["p_upside"]/100
    print(f"{t}: P(cauda de alta do CDS) com a do fiscal ({pu:.0%}) e o meu risk-off (25%) independentes = {1-(1-pu)*(1-0.25):.0%}")
