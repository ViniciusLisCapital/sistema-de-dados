"""G do câmbio, ciclo 2026-10-02, rodada 1: os três cenários no Modelo Estrutural e o upside
com o tempero (i) no carry/vol.

Base: vol, dxy_em e icbr_usd do câmbio (tutela); CDS, S&P 500, Fed funds e CPI dos EUA no
padrão do simulador (aguarda fiscal e externo). Nas caudas, o CDS é uma premissa do câmbio,
declarada como aguarda fiscal (S6)."""
from analytics.agent_system import modelo

sim = modelo.carregar("2026-10-02")
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]


def segura(v):
    return {"4T26": v}


base = {
    "vol": segura(12.7),
    "dxy_em": segura(129.7),
    "icbr_usd": segura(207.9),
}
upside = {
    "vol": {"4T26": 16.0, "1T27": 15.0, "2T27": 14.0, "3T27": 13.5, "4T27": 13.0},
    "dxy_em": segura(134.9),
    "icbr_usd": segura(198.0),
    "fiscal": {"4T26": 150.0, "1T27": 155.0},
}
downside = {
    "vol": segura(11.0),
    "dxy_em": segura(126.9),
    "icbr_usd": segura(212.0),
    "fiscal": segura(120.0),
}

runs = {
    "base": modelo.rodar(sim, caminhos=base),
    "upside": modelo.rodar(sim, caminhos=upside),
    "upside, carry/vol x1,5": modelo.rodar(sim, caminhos=upside, mult={"F.b_carry_vol": 1.5}),
    "downside": modelo.rodar(sim, caminhos=downside),
    "base, carry/vol x1,5": modelo.rodar(sim, caminhos=base, mult={"F.b_carry_vol": 1.5}),
}
for nome, res in runs.items():
    print(f"\n######## {nome}")
    print(modelo.texto(res, trimestres=T) if "trimestres" in modelo.texto.__code__.co_varnames else modelo.texto(res))
