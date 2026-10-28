"""in_cenarios: os três cenários do report de inflação, ciclo 2026-10-27, rodada 1.

Base: todas as exógenas no padrão do simulador (nenhum principal publicou caminho na rodada 1).
Upside: a depreciação de 26/10 persiste. O modelo não aceita a PTAX como entrada (endógena);
  o único jeito de levá-la a ~5,50 no fechamento do 4T26 é pela exógena que mais a move, o
  risco fiscal (CDS), que é o que se faz aqui — um artifício de cenário, não uma tese sobre o
  CDS. Mais o IC-Br agropecuária em US$ 5% acima do padrão de 1T27 em diante.
Downside: a depreciação se desfaz, PTAX ~5,05 no fechamento do 4T26 (o nível de 23/10), pelo
  mesmo canal; IC-Br agropecuária em US$ 5% abaixo do padrão de 1T27 em diante.
Depois, os temperos (i): ia3 e ii4 × 1,5 no upside; × 0,7 no downside, e is2 × 1,5 no downside.
Também: sensibilidade da central a +10% no IC-Br metal e no agro (insumo de subordinado).
"""
import sys
from analytics.agent_system import modelo

sys.stdout.reconfigure(encoding="utf-8")
sim = modelo.carregar("2026-10-27")
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
TODOS = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28", "2T28", "3T28", "4T28", "1T29", "2T29", "3T29"]


def linha(res, k):
    e = res["endogenas"][k]
    return [e["central"][res["trimestres"].index(t)] for t in T]


def rodar(cam, mult=None):
    return modelo.rodar(sim, caminhos=cam, mult=mult or {}, faixa=False)


def ptax4(cds):
    r = rodar({"fiscal": {t: cds for t in TODOS}})
    return linha(r, "ptax")[0]


def busca(alvo, lo, hi):
    for _ in range(40):
        mid = (lo + hi) / 2
        if ptax4(mid) < alvo:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


base = rodar({})
print("chaves de res:", list(base.keys()))
print("endógenas:", list(base["endogenas"].keys()))

cds_up = busca(5.50, 131.0, 600.0)
cds_dn = busca(5.05, 0.0, 131.0)
print(f"CDS que leva a PTAX de fechamento do 4T26 a 5,50: {cds_up:.0f}; a 5,05: {cds_dn:.0f}")
agr0 = 200.53
up_cam = {"fiscal": {t: round(cds_up) for t in TODOS},
          "icbr_agr_usd": {"4T26": agr0, **{t: round(agr0 * 1.05, 2) for t in TODOS[1:]}}}
dn_cam = {"fiscal": {t: round(cds_dn) for t in TODOS},
          "icbr_agr_usd": {"4T26": agr0, **{t: round(agr0 * 0.95, 2) for t in TODOS[1:]}}}

cen = {
    "base": rodar({}),
    "upside (modelo)": rodar(up_cam),
    "upside (modelo + ia3, ii4 × 1,5)": rodar(up_cam, {"I.IA.ia3": 1.5, "I.II.ii4": 1.5}),
    "downside (modelo)": rodar(dn_cam),
    "downside (modelo + ia3, ii4 × 0,7)": rodar(dn_cam, {"I.IA.ia3": 0.7, "I.II.ii4": 0.7}),
    "downside (modelo + ia3, ii4 × 0,7, is2 × 1,5)": rodar(dn_cam, {"I.IA.ia3": 0.7, "I.II.ii4": 0.7,
                                                                   "I.IS.is2": 1.5}),
}
print("\ncaminhos upside:", up_cam)
print("caminhos downside:", dn_cam)
for k in ("ipca_12m", "ptax", "ipca_12m_servicos", "ipca_12m_alimentacao", "ipca_12m_industriais",
          "ipca_12m_monitorados", "ipca_tri", "focus", "selic", "hiato"):
    if k not in base["endogenas"]:
        continue
    print(f"\n{k} ({base['endogenas'][k]['nome']})")
    for n, r in cen.items():
        print(f"  {n:46s} " + "  ".join(f"{v:6.2f}" if v is not None else "  —   " for v in linha(r, k)))

print("\nSensibilidade (insumo de subordinado): IPCA 12m e contribuições, +10% de 4T26 em diante")
for chave, ult in (("icbr_agr_usd", 200.53), ("icbr_met_usd", 330.14)):
    r = rodar({chave: {t: round(ult * 1.10, 2) for t in TODOS}})
    for k in ("ipca_12m", "ipca_12m_alimentacao", "ipca_12m_industriais"):
        d = [a - b for a, b in zip(linha(r, k), linha(base, k))]
        print(f"  {chave} +10% · {k}: " + "  ".join(f"{v:+.2f}" for v in d))

print("\nTexto do upside (modelo) para conferência das exógenas:")
print(modelo.texto(modelo.rodar(sim, caminhos=up_cam), T))

print("\nIN-E1: só o câmbio (CDS 195, PTAX ~5,50 no 4T26), sem mexer no agro; diferença contra a base")
fx = rodar({"fiscal": {t: round(cds_up) for t in TODOS}})
fx15 = rodar({"fiscal": {t: round(cds_up) for t in TODOS}}, {"I.IA.ia3": 1.5, "I.II.ii4": 1.5})
for k in ("ptax", "ipca_12m", "ipca_12m_alimentacao", "ipca_12m_industriais", "ipca_12m_servicos",
          "ipca_12m_monitorados"):
    d = [a - b for a, b in zip(linha(fx, k), linha(base, k))]
    d15 = [a - b for a, b in zip(linha(fx15, k), linha(base, k))]
    print(f"  {k:24s} modelo: " + "  ".join(f"{v:+.2f}" for v in d)
          + " | × 1,5: " + "  ".join(f"{v:+.2f}" for v in d15))
print("  focus_12m base:", [round(v, 2) for v in linha(base, "focus_12m")])
