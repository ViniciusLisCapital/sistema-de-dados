"""in_rf_cenarios: os cenários do report final de inflação, ciclo 2026-10-27 (cópia de in_r2_cenarios
com os caminhos do P2 no base e as caudas dos principais na rodada 2).

Base: os caminhos de P1 (o do principal de cada exógena), sem multiplicador; reproduz o P1.
Upside: o choque de 26/10 se aprofunda (os caminhos de cauda do agente de câmbio: CDS, vol e
  dólar contra emergentes do upside dele) e as commodities sobem (os caminhos "alta" do agente
  externo: icbr_usd, icbr_agr_usd, icbr_met_usd). Depois, tempero (i): ia3 e ii4 x 1,5.
Downside: o prêmio de 26/10 se desfaz (downside do câmbio: CDS, vol, dólar EM) e as commodities
  caem (os caminhos "queda" do externo). Depois, tempero (i): ia3, ii4 x 0,7 e is2 x 1,5.
Também:
  - a atribuição da diferença entre o padrão do simulador (rodada 1) e o P1, bloco a bloco;
  - IN-E1: só o câmbio de cada cauda, commodities no base; diferença contra o base;
  - sensibilidade +10% em icbr_agr_usd e icbr_met_usd sobre o P1 (insumo de subordinado);
  - leitura do tempero do agente de expectativas (E.e1 x 1,2, decisão dele, não cenário meu):
    o que ele faz ao IPCA de 12 meses, só para dimensionar a assimetria;
  - os coeficientes de (I) com o intervalo de 90%.
"""
import sys

from analytics.agent_system import modelo

sys.stdout.reconfigure(encoding="utf-8")
sim = modelo.carregar("2026-10-27")
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
TT = T + ["2T28", "3T28", "4T28", "1T29", "2T29", "3T29"]


def cam(vals):
    """6 valores (4T26..1T28) -> 12 trimestres, o último segurado."""
    v = list(vals) + [vals[-1]] * (len(TT) - len(vals))
    return dict(zip(TT, v))


P1 = {  # caminhos usados no P2 (P2.md, seção 1), um por principal; o nome P1 ficou da cópia
    "meta_12m": cam([3.0] * 6),
    "rr_10a": cam([7.72, 7.95, 7.90, 7.80, 7.75, 7.70]),
    "fiscal": cam([140, 142, 139, 135, 130, 125]),
    "vol": cam([17.0, 15.5, 14.5, 14.0, 13.5, 13.5]),
    "infl_us": cam([0.86, 0.61, 0.61, 0.65, 0.63, 0.65]),
    "ffr": cam([4.13, 4.13, 4.13, 4.13, 4.13, 3.88]),
    "dxy_em": cam([130.5, 131.0, 130.5, 130.0, 129.5, 129.0]),
    "sp500": cam([7750, 7900, 8050, 8200, 8350, 8500]),
    "icbr_usd": cam([206.2, 202.6, 201.0, 199.9, 199.0, 198.3]),
    "icbr_agr_usd": cam([203.9, 200.9, 199.3, 198.4, 197.8, 197.4]),
    "icbr_met_usd": cam([331.7, 330.0, 330.0, 328.7, 327.3, 325.7]),
}
FX_UP = {"fiscal": cam([170, 205, 210, 205, 198, 190]),          # fiscal r2, upside
         "rr_10a": cam([8.15, 8.90, 9.10, 9.10, 9.00, 8.90]),
         "vol": cam([24.0, 21.0, 18.0, 16.0, 15.0, 15.0])}       # câmbio r2, upside
FX_DN = {"fiscal": cam([122, 115, 112, 110, 108, 106]),          # fiscal r2, downside
         "rr_10a": cam([7.36, 7.30, 7.15, 7.05, 7.00, 6.95]),
         "vol": cam([13.0, 12.5, 12.0, 12.0, 12.0, 12.0])}       # câmbio r2, downside
CO_UP = {"icbr_usd": cam([216.3, 217.1, 217.1, 216.8, 215.7, 215.3]),   # externo r2, alta
         "icbr_agr_usd": cam([208.1, 211.1, 211.9, 212.8, 212.4, 211.7]),
         "icbr_met_usd": cam([346.0, 358.0, 362.0, 362.0, 362.0, 362.0])}
CO_DN = {"icbr_usd": cam([197.3, 188.2, 184.3, 183.2, 183.5, 183.8]),   # externo r2, queda
         "icbr_agr_usd": cam([200.6, 192.0, 188.4, 186.6, 186.4, 186.8]),
         "icbr_met_usd": cam([320.0, 298.3, 283.3, 277.0, 275.0, 275.0])}

K = ["ipca_12m", "ipca_12m_servicos", "ipca_12m_alimentacao", "ipca_12m_industriais",
     "ipca_12m_monitorados", "ipca_12m_residuo", "ipca_tri", "ptax", "selic", "selic_fim",
     "focus_12m", "hiato"]


def rodar(c, mult=None, faixa=False):
    return modelo.rodar(sim, caminhos=c, mult=mult or {}, faixa=faixa)


def lin(r, k):
    e = r["endogenas"][k]
    return [e["central"][r["trimestres"].index(t)] for t in T]


def fmt(v):
    return "  -   " if v is None else f"{v:6.3f}"


def show(nome, r, ks=K):
    print(f"\n== {nome}")
    for k in ks:
        print(f"  {k:22s} " + "  ".join(fmt(v) for v in lin(r, k)))


def diff(a, b, k):
    return [x - y for x, y in zip(lin(a, k), lin(b, k))]


# coeficientes de (I) -----------------------------------------------------------------------

base = rodar(P1, faixa=True)
show("base (P1)", base)
e = base["endogenas"]["ipca_12m"]
print("  faixa 90% posterior:", [(round(e["lo"][i], 2), round(e["hi"][i], 2)) for i in range(6)])

# atribuição padrão -> P1 ---------------------------------------------------------------------
print("\n== atribuição: padrão do simulador (rodada 1) -> P1, acumulando bloco a bloco")
blocos = [("câmbio/fiscal (fiscal, vol)", ["fiscal", "vol"]),
          ("externo EUA e risco (infl_us, ffr, dxy_em, sp500)", ["infl_us", "ffr", "dxy_em", "sp500"]),
          ("commodities (icbr_usd, agr, met)", ["icbr_usd", "icbr_agr_usd", "icbr_met_usd"]),
          ("juro real e meta (rr_10a, meta_12m)", ["rr_10a", "meta_12m"])]
acc = {}
prev = rodar({})
show("padrão do simulador", prev, ["ipca_12m", "ptax", "selic", "focus_12m", "hiato"])
for nome, ks in blocos:
    for k in ks:
        acc[k] = P1[k]
    r = rodar(dict(acc))
    print(f"  + {nome}")
    for k in ("ipca_12m", "ipca_12m_alimentacao", "ipca_12m_industriais", "ipca_12m_servicos",
              "ipca_12m_monitorados", "ptax", "selic", "focus_12m"):
        print(f"      d {k:22s} " + "  ".join(f"{v:+.3f}" for v in diff(r, prev, k)))
    prev = r

# caudas --------------------------------------------------------------------------------------
up_c = {**P1, **FX_UP, **CO_UP}
dn_c = {**P1, **FX_DN, **CO_DN}
cen = {
    "upside modelo": rodar(up_c),
    "upside modelo + ia3, ii4 x 1,5": rodar(up_c, {"I.IA.ia3": 1.5, "I.II.ii4": 1.5}),
    "downside modelo": rodar(dn_c),
    "downside modelo + ia3, ii4 x 0,7, is2 x 1,5": rodar(dn_c, {"I.IA.ia3": 0.7, "I.II.ii4": 0.7,
                                                                 "I.IS.is2": 1.5}),
}
for n, r in cen.items():
    show(n, r)

# IN-E1: só o câmbio --------------------------------------------------------------------------
print("\n== IN-E1: só o câmbio de cada cauda (commodities no base), contra o base")
fx_up = rodar({**P1, **FX_UP})
fx_up15 = rodar({**P1, **FX_UP}, {"I.IA.ia3": 1.5, "I.II.ii4": 1.5})
fx_dn = rodar({**P1, **FX_DN})
for nome, r in (("FX upside", fx_up), ("FX upside x 1,5", fx_up15), ("FX downside", fx_dn)):
    pt = [100 * (a / b - 1) for a, b in zip(lin(r, "ptax"), lin(base, "ptax"))]
    print(f"  {nome}: PTAX " + "  ".join(f"{v:.3f}" for v in lin(r, "ptax"))
          + " | d% " + "  ".join(f"{v:+.1f}" for v in pt))
    for k in ("ipca_12m", "ipca_12m_alimentacao", "ipca_12m_industriais", "ipca_12m_servicos",
              "ipca_12m_monitorados", "focus_12m", "selic"):
        print(f"      d {k:22s} " + "  ".join(f"{v:+.3f}" for v in diff(r, base, k)))
fx_p1 = rodar({k: P1[k] for k in ("fiscal", "vol")})
d0 = rodar({})
print("  P1 contra o padrão, só fiscal+vol: PTAX " + "  ".join(f"{v:.3f}" for v in lin(fx_p1, "ptax")))
for k in ("ipca_12m", "ipca_12m_alimentacao", "ipca_12m_industriais"):
    print(f"      d {k:22s} " + "  ".join(f"{v:+.3f}" for v in diff(fx_p1, d0, k)))

# sensibilidade de subordinado ----------------------------------------------------------------
print("\n== +10% sobre o caminho do P1")
for key in ("icbr_agr_usd", "icbr_met_usd"):
    c = dict(P1)
    c[key] = {t: round(v * 1.10, 2) for t, v in P1[key].items()}
    r = rodar(c)
    for k in ("ipca_12m", "ipca_12m_alimentacao", "ipca_12m_industriais", "ptax"):
        print(f"  {key} d {k:22s} " + "  ".join(f"{v:+.3f}" for v in diff(r, base, k)))

# leitura do tempero do agente de expectativas ------------------------------------------------
print("\n== leitura: E.e1 x 1,2 (tempero do agente de expectativas, no base dele), contra o base")
re = rodar(P1, {"E.e1": 1.2})
for k in ("focus_12m", "ipca_12m", "ipca_12m_servicos", "ipca_12m_alimentacao",
          "ipca_12m_industriais", "ipca_12m_monitorados", "selic"):
    print(f"  {k:22s} nível " + "  ".join(f"{v:.2f}" for v in lin(re, k))
          + " | d " + "  ".join(f"{v:+.3f}" for v in diff(re, base, k)))
