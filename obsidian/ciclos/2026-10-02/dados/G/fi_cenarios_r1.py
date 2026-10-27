"""G do fiscal, ciclo 2026-10-02, rodada 1: os cenários do fiscal no Modelo Estrutural.

Exógenas do fiscal (tutela): `fiscal` (CDS 5a, fechamento), `rr_10a` (NTN-B 10a, média do
trimestre), `meta_12m` (nível 2). As outras no padrão do simulador (aguardam câmbio e externo).
Roda: padrão; base; base só com o CDS (isola o canal do câmbio); base só com o rr_10a (isola a
âncora); upside; downside; cauda de dominância (ilustrativa); e o upside com o CDS × 1,2 e × 1,5 em
F.b_fiscal (o argumento ao câmbio, que é quem aplica).
"""
from analytics.agent_system import modelo

sim = modelo.carregar("2026-10-02")
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]


def cam(v):
    return dict(zip(T, v))


CDS = {
    "base": cam([135, 140, 140, 140, 140, 140]),
    "upside": cam([165, 190, 195, 190, 185, 180]),
    "downside": cam([118, 112, 108, 105, 105, 105]),
    "dominancia": cam([200, 260, 280, 280, 270, 260]),
}
RR = {
    "base": cam([7.55, 7.60, 7.55, 7.50, 7.45, 7.40]),
    "upside": cam([7.90, 8.40, 8.50, 8.45, 8.40, 8.35]),
    "downside": cam([7.25, 7.10, 6.90, 6.80, 6.70, 6.60]),
    "dominancia": cam([8.20, 9.00, 9.30, 9.30, 9.20, 9.00]),
}
META = {"base": cam([3.0] * 6), "dominancia": cam([3.0, 3.0, 3.0, 3.5, 3.5, 3.5])}

runs = {
    "padrão do simulador": {},
    "base": {"fiscal": CDS["base"], "rr_10a": RR["base"], "meta_12m": META["base"]},
    "base, só o CDS": {"fiscal": CDS["base"]},
    "base, só o rr_10a": {"rr_10a": RR["base"]},
    "upside": {"fiscal": CDS["upside"], "rr_10a": RR["upside"], "meta_12m": META["base"]},
    "upside, só o CDS": {"fiscal": CDS["upside"]},
    "downside": {"fiscal": CDS["downside"], "rr_10a": RR["downside"], "meta_12m": META["base"]},
    "dominância (ilustrativa)": {"fiscal": CDS["dominancia"], "rr_10a": RR["dominancia"], "meta_12m": META["dominancia"]},
}
for nome, c in runs.items():
    print(f"\n######## {nome}")
    print(modelo.texto(modelo.rodar(sim, caminhos=c), trimestres=T))

for m in (1.2, 1.5):
    print(f"\n######## upside, CDS × {m} em F.b_fiscal (argumento ao câmbio)")
    print(modelo.texto(modelo.rodar(sim, caminhos=runs["upside"], mult={"F.b_fiscal": m}), trimestres=T))
