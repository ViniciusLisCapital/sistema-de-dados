"""G cambio: os três cenários da rodada 1 no Modelo Estrutural (ciclo 2026-10-27).
vol: caminho do câmbio (principal). CDS, dólar contra emergentes, S&P 500, IC-Br: premissa 'aguarda fiscal/externo'
(rodada 1), com o 4T26 no nível do último dado do F; ffr e infl_us no padrão do simulador."""
from analytics.agent_system import modelo

T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
def cam(vals): return dict(zip(T, vals))

sim = modelo.carregar("2026-10-27")
cen = {
    "base": dict(caminhos={
        "vol": cam([17.0, 15.5, 14.5, 14.0, 13.5, 13.5]),
        "fiscal": cam([137] * 6), "dxy_em": cam([130.2] * 6), "sp500": cam([7717] * 6)}, mult={}),
    "upside": dict(caminhos={
        "vol": cam([24.0, 21.0, 18.0, 16.0, 15.0, 15.0]),
        "fiscal": cam([185, 200, 190, 175, 165, 160]), "dxy_em": cam([132.5] * 6), "sp500": cam([7717] * 6)},
        mult={"F.b_fiscal": 1.2}),
    "upside_sem_mult": dict(caminhos={
        "vol": cam([24.0, 21.0, 18.0, 16.0, 15.0, 15.0]),
        "fiscal": cam([185, 200, 190, 175, 165, 160]), "dxy_em": cam([132.5] * 6), "sp500": cam([7717] * 6)}, mult={}),
    "downside": dict(caminhos={
        "vol": cam([13.0, 12.5, 12.0, 12.0, 12.0, 12.0]),
        "fiscal": cam([118, 115, 115, 115, 115, 115]), "dxy_em": cam([128.5] * 6), "sp500": cam([7717] * 6),
        "icbr_usd": cam([210.0] * 6)}, mult={}),
    "base_vol_padrao": dict(caminhos={
        "fiscal": cam([137] * 6), "dxy_em": cam([130.2] * 6), "sp500": cam([7717] * 6)}, mult={}),
}
for nome, c in cen.items():
    res = modelo.rodar(sim, caminhos=c["caminhos"], mult=c["mult"])
    print(f"\n######## {nome} ########")
    print(modelo.texto(res, trimestres=T))
