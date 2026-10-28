"""G cambio (report final): cenários no Modelo Estrutural com o base do P2.
Base: caminhos usados no P2. Caudas: vol (câmbio, principal) e CDS e rr_10a nos caminhos de cauda do fiscal r2
(seção 3.1); bloco global no base do externo (P2). Variantes: S&P parado, F.b_sp500 x 0,55, F.b_fiscal x 1,2,
NTN-B de cauda trocada pela do base. Imprime só PTAX, Selic de fechamento e IPCA 12m."""
import json
from pathlib import Path
from analytics.agent_system import modelo

T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
P = json.load(open(Path(__file__).resolve().parent.parent.parent / "P2.json", encoding="utf-8"))
base = {k: dict(v) for k, v in P["caminhos_usados"].items()}
def com(**mud):
    c = {k: dict(v) for k, v in base.items()}
    for k, v in mud.items(): c[k] = dict(zip(T, v))
    return c
VOL_UP = [24.0, 21.0, 18.0, 16.0, 15.0, 15.0]
VOL_DN = [13.0, 12.5, 12.0, 12.0, 12.0, 12.0]
CDS_UP = [170, 205, 210, 205, 198, 190]
CDS_DN = [122, 115, 112, 110, 108, 106]
RR_UP = [8.15, 8.90, 9.10, 9.10, 9.00, 8.90]
RR_DN = [7.36, 7.30, 7.15, 7.05, 7.00, 6.95]
sim = modelo.carregar("2026-10-27")
cen = [
    ("base_P2", base, {}),
    ("base_sp_parado", com(sp500=[7717] * 6), {}),
    ("base_sp_x0.55", base, {"F.b_sp500": 0.55}),
    ("upside_sem_mult", com(vol=VOL_UP, fiscal=CDS_UP, rr_10a=RR_UP), {}),
    ("upside_x1.2", com(vol=VOL_UP, fiscal=CDS_UP, rr_10a=RR_UP), {"F.b_fiscal": 1.2}),
    ("upside_x1.2_rr_base", com(vol=VOL_UP, fiscal=CDS_UP), {"F.b_fiscal": 1.2}),
    ("downside", com(vol=VOL_DN, fiscal=CDS_DN, rr_10a=RR_DN), {}),
    ("downside_sp_x0.55", com(vol=VOL_DN, fiscal=CDS_DN, rr_10a=RR_DN), {"F.b_sp500": 0.55}),
    ("downside_rr_base", com(vol=VOL_DN, fiscal=CDS_DN), {}),
]
for nome, c, m in cen:
    res = modelo.rodar(sim, caminhos=c, mult=m)
    linhas = [l for l in modelo.texto(res, trimestres=T).splitlines()
              if l.startswith("| PTAX") or l.startswith("| Selic, fech") or l.startswith("| IPCA acumulado")]
    print(f"\n## {nome}"); print("\n".join(linhas), flush=True)
