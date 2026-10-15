"""G · câmbio · ciclo 2026-10-15: os três cenários do câmbio no Modelo Estrutural.

Etapa 1: base, worst e best com os caminhos das exógenas da equação do câmbio, sem
multiplicador. Etapa 2, tipo (i): worst e best com o efeito do CDS × 1,2.
Os caminhos são níveis no fechamento do trimestre, na unidade do simulador.
"""
import json
import sys
from pathlib import Path

from analytics.agent_system import modelo

sys.stdout.reconfigure(encoding="utf-8")
TRI = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]


def cam(*v):
    return dict(zip(TRI, v))


CENARIOS = {
    "base": {
        "fiscal": cam(112, 112, 115, 118, 120, 120),
        "vol": cam(12.19, 12.19, 12.19, 12.19, 12.19, 12.19),
        "infl_us": cam(0.91, 0.91, 0.91, 0.91, 0.91, 0.91),
        "ffr": cam(3.875, 4.125, 4.125, 4.125, 4.125, 4.125),
        "dxy_em": cam(129.8, 129.8, 129.8, 129.8, 129.8, 129.8),
        "sp500": cam(7721, 7721, 7721, 7721, 7721, 7721),
        "icbr_usd": cam(210, 205, 200, 198, 195, 195),
    },
    "worst": {
        "fiscal": cam(150, 160, 170, 175, 180, 180),
        "vol": cam(16, 15, 15, 15, 15, 15),
        "infl_us": cam(1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
        "ffr": cam(4.125, 4.375, 4.375, 4.375, 4.375, 4.375),
        "dxy_em": cam(133, 134, 134, 134, 134, 134),
        "sp500": cam(7721, 7721, 7721, 7721, 7721, 7721),
        "icbr_usd": cam(205, 195, 190, 185, 185, 185),
    },
    "best": {
        "fiscal": cam(100, 95, 90, 90, 90, 90),
        "vol": cam(11, 10.5, 10.5, 10.5, 10.5, 10.5),
        "infl_us": cam(0.91, 0.91, 0.91, 0.91, 0.91, 0.91),
        "ffr": cam(3.875, 3.875, 3.875, 3.875, 3.875, 3.875),
        "dxy_em": cam(128, 127, 127, 127, 127, 127),
        "sp500": cam(7721, 7721, 7721, 7721, 7721, 7721),
        "icbr_usd": cam(212, 212, 212, 212, 212, 212),
    },
}
MULT = {"worst": {"F.b_fiscal": 1.2}, "best": {"F.b_fiscal": 1.2}}

sim = modelo.carregar("2026-10-15")
saida = {}
for nome, caminhos in CENARIOS.items():
    res = modelo.rodar(sim, caminhos=caminhos)
    print(f"\n=================== {nome} · etapa 1 (modelo) ===================\n")
    print(modelo.texto(res, TRI))
    saida[nome] = {k: res["endogenas"][k]["central"][:6] for k in ("ptax", "selic", "ipca_12m")}
    saida[nome]["ptax_lo"] = res["endogenas"]["ptax"]["lo"][:6]
    saida[nome]["ptax_hi"] = res["endogenas"]["ptax"]["hi"][:6]
    if nome in MULT:
        rm = modelo.rodar(sim, caminhos=caminhos, mult=MULT[nome])
        print(f"\n------------- {nome} · com o tipo (i): {MULT[nome]} -------------\n")
        print(modelo.texto(rm, TRI))
        saida[nome]["ptax_mult"] = rm["endogenas"]["ptax"]["central"][:6]

out = Path(__file__).with_name("cambio_cenarios_saida.json")
out.write_text(json.dumps(saida, indent=1), encoding="utf-8")
print("\ngravado:", out.name)
