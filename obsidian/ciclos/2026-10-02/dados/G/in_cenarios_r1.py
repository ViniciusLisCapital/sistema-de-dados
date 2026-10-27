"""in_cenarios_r1: os cenários do Modelo Estrutural para o report de inflação, ciclo 2026-10-02, r1,
e as contas dos temperos (ii), sobre os dados de ../A/.

Caminhos (só as duas exógenas de tutela: icbr_agr_usd e icbr_met_usd, média do trimestre, pontos):
  base     : a média do 3T26 segurada (agro 200,53; metal 330,14).
  upside   : agro e metal no p90 histórico da variação de 1 e 2 trimestres (Δlog das médias
             trimestrais desde 1998, in_leituras.py): +8,0% no 4T26 e +12,1% no 1T27 (agro);
             +12,3% e +21,3% (metal), contra a média do 3T26; segurado depois.
  downside : o p10: agro −6,1% e −8,6%; metal −6,9% e −11,7%.
Multiplicadores (tempero (i), equação (I), do inflação):
  upside   : I.IA.ia2 × 1,4 (repasse das commodities agrícolas a alimentos).
  downside : nenhum.
Tempero (ii), em p.p. do IPCA 12m, somado ao resultado do modelo:
  upside   : combustíveis (veículos +6%, peso 5,45; domésticos +5%, peso 1,39) = +0,40 do 4T26 ao
             3T27; +0,10 no 4T27 e 1T28 (o reajuste sai da janela; fica a 2ª rodada pela indexação).
  downside : energia elétrica −5% (peso 3,98) = −0,20 e alimentos in natura −0,08, do 4T26 ao 3T27.
"""
import math
from pathlib import Path
import pandas as pd
from analytics.agent_system import modelo

A = Path(__file__).resolve().parents[1] / "A"
sim = modelo.carregar("2026-10-02")
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]

agr3, met3 = 200.53, 330.14  # médias do 3T26 (listar)
def lv(base, pct):
    return round(base * math.exp(pct / 100), 2)

base = {"icbr_agr_usd": {t: agr3 for t in T}, "icbr_met_usd": {t: met3 for t in T}}
up = {"icbr_agr_usd": {"4T26": lv(agr3, 8.0), "1T27": lv(agr3, 12.1)},
      "icbr_met_usd": {"4T26": lv(met3, 12.3), "1T27": lv(met3, 21.3)}}
dn = {"icbr_agr_usd": {"4T26": lv(agr3, -6.1), "1T27": lv(agr3, -8.6)},
      "icbr_met_usd": {"4T26": lv(met3, -6.9), "1T27": lv(met3, -11.7)}}
print("caminhos upside:", up)
print("caminhos downside:", dn)

cen = {"base": (base, {}), "up_cam": (up, {}), "up": (up, {"I.IA.ia2": 1.4}), "down": (dn, {})}
R = {}
for nome, (cam, mult) in cen.items():
    R[nome] = modelo.rodar(sim, caminhos=cam, mult=mult)
    print(f"\n===== {nome} =====")
    print(modelo.texto(R[nome], trimestres=T))

def serie(res, k):
    tri = res["trimestres"]
    c = res["endogenas"][k]["central"]
    return {t: c[tri.index(t)] for t in T}

t_up = dict(zip(T, [0.40, 0.40, 0.40, 0.40, 0.10, 0.10]))
t_dn = dict(zip(T, [-0.28, -0.28, -0.28, -0.28, 0.0, 0.0]))
print("\n===== resumo IPCA 12m =====")
b, u, d = serie(R["base"], "ipca_12m"), serie(R["up"], "ipca_12m"), serie(R["down"], "ipca_12m")
for t in T:
    print(f"{t}: base {b[t]:.2f} | upside modelo {u[t]:.2f} -> com tempero {u[t]+t_up[t]:.2f} | "
          f"downside modelo {d[t]:.2f} -> com tempero {d[t]+t_dn[t]:.2f}")
print("\nendógenas do base, chaves:", list(R["base"]["endogenas"].keys()))
for k in ["ipca_12m_servicos", "ipca_12m_alimentacao", "ipca_12m_industriais", "ipca_12m_monitorados",
          "ipca_12m_residuo", "ptax_fim", "hiato", "focus_12m", "selic_fim", "ipca_tri"]:
    if k in R["base"]["endogenas"]:
        print(k, {t: (round(v, 3) if v is not None else None) for t, v in serie(R["base"], k).items()})

# comparação com Copom (pm_copom_projecoes, R281) e com o QPC implícito (in_corte.py)
copom = dict(zip(T, [5.2, 4.9, 4.5, 4.5, 3.9, 3.2]))
print("\nmodelo − Copom (p.p.):", {t: round(b[t] - copom[t], 2) for t in T})
print("modelo 4T26 − QPC implícito 4,94:", round(b["4T26"] - 4.94, 2), "; − Focus 2026 5,01:", round(b["4T26"] - 5.01, 2))
print("modelo 4T27 − Focus 2027 4,30:", round(b["4T27"] - 4.30, 2))
print("modelo 1T28 − QPC horizonte relevante 4,00:", round(b["1T28"] - 4.00, 2))

# --- contas dos temperos (ii) ---
w_veic, w_dom = 5.45, 1.39
for pv, pd_ in [(4, 3), (6, 5), (8, 6)]:
    print(f"combustíveis veículos +{pv}% e domésticos +{pd_}%: +{(w_veic*pv + w_dom*pd_)/100:.2f} p.p. no IPCA")
print("energia −5% (peso 3,98):", round(-3.98 * 5 / 100, 2), "p.p.")
dec = pd.read_csv(A / "inflc_decomposicao.csv.gz", parse_dates=["date"])
g = dec[(dec["indice"] == "IPCA") & (dec["subitem_codigo"] == 5104001)].set_index("date")["var_mensal"]
acc = (g.loc["2026-03-01":"2026-04-01"].add(100).div(100).prod() - 1) * 100
acc2 = (g.loc["2026-05-01":"2026-08-01"].add(100).div(100).prod() - 1) * 100
print("gasolina acumulada mar-abr/26:", round(acc, 2), "; mai-ago/26:", round(acc2, 2))
br = pd.read_csv(A / "comm_brent.csv.gz", parse_dates=["date"]).set_index("date")["value"]
bm = br.resample("MS").mean()
print("Brent média fev->abr/26:", round((bm["2026-04-01"] / bm["2026-02-01"] - 1) * 100, 1), "%;",
      "jul->set/26:", round((bm["2026-09-01"] / bm["2026-07-01"] - 1) * 100, 1), "%;",
      "02/10 contra média de jul:", round((135.51 / bm["2026-07-01"] - 1) * 100, 1), "%;",
      "02/10 contra 01/10:", round((135.51 / 114.82 - 1) * 100, 1), "%")
