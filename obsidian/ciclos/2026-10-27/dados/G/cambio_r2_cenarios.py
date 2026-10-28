"""G cambio (rodada 2): os cenários no Modelo Estrutural com o base do P1.
Base: os caminhos usados no P1 (cada exógena do seu principal; vol do câmbio). Caudas: a história é doméstica,
então o bloco global fica no base do externo (P1) e mudam a vol (câmbio, principal) e o CDS e o rr_10a nos
caminhos de cauda do próprio principal (fiscal, report r1, seção 3.1). Variantes medem o S&P 500 e o rr_10a."""
import json
from pathlib import Path
from analytics.agent_system import modelo

T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
def cam(vals): return dict(zip(T, vals))

P = json.load(open(Path(__file__).resolve().parent.parent.parent / "P1.json", encoding="utf-8"))
base = {k: dict(v) for k, v in P["caminhos_usados"].items()}

def com(**mud):
    c = {k: dict(v) for k, v in base.items()}
    for k, v in mud.items():
        c[k] = cam(v)
    return c

VOL_UP = [24.0, 21.0, 18.0, 16.0, 15.0, 15.0]
VOL_DN = [13.0, 12.5, 12.0, 12.0, 12.0, 12.0]
CDS_UP = [165, 190, 200, 200, 195, 190]       # fiscal r1, upside
CDS_DN = [115, 110, 108, 106, 105, 105]       # fiscal r1, downside
RR_UP = [8.05, 8.80, 9.00, 9.00, 8.90, 8.80]
RR_DN = [7.35, 6.90, 6.80, 6.75, 6.70, 6.70]

sim = modelo.carregar("2026-10-27")
cen = {
    "base_P1": (base, {}),
    "base_sp_parado": (com(sp500=[7717] * 6), {}),
    "base_b_fiscal_1.2": (base, {"F.b_fiscal": 1.2}),
    "upside": (com(vol=VOL_UP, fiscal=CDS_UP, rr_10a=RR_UP), {"F.b_fiscal": 1.2}),
    "upside_sem_mult": (com(vol=VOL_UP, fiscal=CDS_UP, rr_10a=RR_UP), {}),
    "upside_mult_1.5": (com(vol=VOL_UP, fiscal=CDS_UP, rr_10a=RR_UP), {"F.b_fiscal": 1.5}),
    "upside_rr_base": (com(vol=VOL_UP, fiscal=CDS_UP), {"F.b_fiscal": 1.2}),
    "downside": (com(vol=VOL_DN, fiscal=CDS_DN, rr_10a=RR_DN), {}),
    "downside_rr_base": (com(vol=VOL_DN, fiscal=CDS_DN), {}),
}
for nome, (c, m) in cen.items():
    res = modelo.rodar(sim, caminhos=c, mult=m)
    print(f"\n######## {nome} ########")
    print(modelo.texto(res, trimestres=T))
