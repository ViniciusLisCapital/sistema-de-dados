"""Atividade, seção 1: a tese (hiato e PIB 4 trimestres) com a central do modelo e a distribuição do agente.

Central do hiato: modelo, cenário base (padrão do simulador), do retrato do ciclo.
Linha companheira (mecânica): PIB yoy(q) = potencial do F (2,50) + hiato(q) - hiato(q-4),
  hiato(q-4) observado na edição 2026-09 do RPM (pm_hiato_produto) ou do modelo.
Distribuição: normal em torno de central + deslocamento (os temperos), com DP por trimestre
  = raiz(erro da H sem crises^2 + partida^2 + pesos^2) para o hiato; para o PIB, + ruído do potencial implícito.
Carrego do IBC-Br: 4T26 contra 4T25 e 1T27 contra 1T26 se o índice dessaz. ficar no nível de agosto.
"""
import math
import numpy as np
import pandas as pd
from pathlib import Path
from analytics.agent_system import modelo

A = Path(__file__).resolve().parents[1] / "A"
Q = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
sim = modelo.carregar("2026-10-27")
res = modelo.rodar(sim)
tr = res["trimestres"]; hz = res["endogenas"]["hiato"]
gap = {q: hz["central"][tr.index(q)] for q in Q}
lo = {q: hz["lo"][tr.index(q)] for q in Q}; hi_ = {q: hz["hi"][tr.index(q)] for q in Q}

hp = pd.read_csv(A / "pm_hiato_produto.csv.gz", parse_dates=["date"])
c = hp[hp.variavel == "central"].set_index("date")["value"]
obs = {"4T25": c.loc["2025-10-01"], "1T26": c.loc["2026-01-01"], "2T26": c.loc["2026-04-01"], "3T26": c.loc["2026-07-01"]}
allg = {**obs, **gap}
ordem = ["4T25", "1T26", "2T26", "3T26"] + Q
pot = 2.50
pib = {q: pot + allg[q] - allg[ordem[ordem.index(q) - 4]] for q in Q}
print("Linha companheira (mecanica):")
for q in Q:
    q4 = ordem[ordem.index(q) - 4]
    print(f"  {q}: 2,50 + {allg[q]:.3f} - {allg[q4]:.3f} ({q4}) = {pib[q]:.3f}")

# ruido do potencial implicito (F, 8 trimestres 3T24-2T26)
pot_impl = [2.66, 2.60, 2.53, 2.19, 2.33, 2.53, 2.69, 3.19]
sd_pot = float(np.std(pot_impl, ddof=1))
print(f"DP do potencial implicito nos 8 trimestres do F: {sd_pot:.2f}")

# carrego do IBC-Br
ib = pd.read_csv(A / "atv_ibcbr.csv.gz", parse_dates=["date"])
sa = ib[ib.name == "ibcbr_sa"].set_index("date")["value"].sort_index()
ago = sa.loc["2026-08-01"]
ext = sa.copy()
for m in pd.date_range("2026-09-01", "2027-03-01", freq="MS"):
    ext.loc[m] = ago
ext = ext.sort_index()
qm = ext.resample("QS").mean()
for qq, qa in [("2026-07-01", "2025-07-01"), ("2026-10-01", "2025-10-01"), ("2027-01-01", "2026-01-01")]:
    print(f"carrego IBC-Br dessaz. (nivel de ago segurado), {qq[:7]} contra {qa[:7]}: {(qm.loc[qq]/qm.loc[qa]-1)*100:.2f}%")

# distribuicao
sd_H = [0.34, 0.45, 0.51, 0.56, 0.60, 0.62]           # at_residuos_H, sem crises
h1 = 0.874689157807679
sd_part = [0.25 * h1 ** (k + 1) for k in range(6)]     # partida: DP 0,25 em torno do deslocamento
sd_w = [(hi_[q] - lo[q]) / 2 / 1.645 for q in Q]       # pesos do posterior
sd_gap = [math.sqrt(a * a + b * b + w * w) for a, b, w in zip(sd_H, sd_part, sd_w)]
# deslocamentos (temperos): partida d=-0,15; residuo e=+0,05 acumulado; custo de capital -0,02 acumulado
part = [-0.15 * h1 ** (k + 1) for k in range(6)]
acc = 0.0; resid = []
for k in range(6):
    acc = h1 * acc + 0.05; resid.append(acc)
acc = 0.0; cc = []
for k in range(6):
    acc = h1 * acc - 0.02; cc.append(acc)
shift_gap = [a + b + d for a, b, d in zip(part, resid, cc)]
w_gap = [0.30, 0.35, 0.40, 0.45, 0.45, 0.50]


def ncdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def probs(central, shift, sd, w):
    mu = central + shift
    lo_, hi2 = central - w, central + w
    pdn = ncdf((lo_ - mu) / sd); pup = 1 - ncdf((hi2 - mu) / sd)
    pdn_r, pup_r = round(pdn * 100), round(pup * 100)
    return lo_, hi2, 100 - pdn_r - pup_r, pup_r, pdn_r


print("\nHiato: central | sd | deslocamento (partida, residuo, custo) | faixa | P faixa/up/down")
tese_gap = {}
for k, q in enumerate(Q):
    l, h, pf, pu, pd_ = probs(gap[q], shift_gap[k], sd_gap[k], w_gap[k])
    tese_gap[q] = (gap[q], l, h, pf, pu, pd_)
    print(f"  {q}: {gap[q]:.2f} | {sd_gap[k]:.2f} | {shift_gap[k]:+.2f} ({part[k]:+.2f}, {resid[k]:+.2f}, {cc[k]:+.2f}) | [{l:.2f}; {h:.2f}] | {pf}/{pu}/{pd_}  assim {pu-pd_:+d}")

# PIB yoy: deslocamento = desl. do hiato(q) - desl. do hiato(q-4) (zero no observado) + leitura direta do IBC-Br no 4T26 e 1T27
shift_all = {"4T25": 0, "1T26": 0, "2T26": 0, "3T26": -0.15}  # partida: 3T26 abaixo do nowcast
shift_all.update({q: s for q, s in zip(Q, shift_gap)})
direto = {"4T26": -0.15, "1T27": -0.10}  # IBC-Br: carrego abaixo da conta mecanica (ver acima)
sd_pib = []
for k, q in enumerate(Q):
    base_sd = sd_gap[k] if k < 4 else math.sqrt(sd_H[3] ** 2 + sd_w[k] ** 2)
    sd_pib.append(math.sqrt(base_sd ** 2 + sd_pot ** 2))
w_pib = [0.35, 0.40, 0.45, 0.50, 0.50, 0.50]
print("\nPIB yoy: central | sd | deslocamento | faixa | P faixa/up/down")
tese_pib = {}
for k, q in enumerate(Q):
    q4 = ordem[ordem.index(q) - 4]
    sh = shift_all[q] - shift_all[q4] + direto.get(q, 0)
    l, h, pf, pu, pd_ = probs(pib[q], sh, sd_pib[k], w_pib[k])
    tese_pib[q] = (pib[q], l, h, pf, pu, pd_)
    print(f"  {q}: {pib[q]:.2f} | {sd_pib[k]:.2f} | {sh:+.2f} | [{l:.2f}; {h:.2f}] | {pf}/{pu}/{pd_}  assim {pu-pd_:+d}")

# limites de cauda de referencia: percentis 5 e 95 da distribuicao do agente
print("\nPercentis 5/95 da distribuicao do agente (hiato | PIB):")
for k, q in enumerate(Q):
    mg = gap[q] + shift_gap[k]
    q4 = ordem[ordem.index(q) - 4]
    mp = pib[q] + shift_all[q] - shift_all[q4] + direto.get(q, 0)
    print(f"  {q}: hiato {mg-1.645*sd_gap[k]:.2f} a {mg+1.645*sd_gap[k]:.2f} | PIB {mp-1.645*sd_pib[k]:.2f} a {mp+1.645*sd_pib[k]:.2f}")

# 3.3: cenarios de cauda, modelo -> com tempero
up = modelo.rodar(sim, mult={"H.h2": 0.5}); dn = modelo.rodar(sim, mult={"H.h2": 1.5})
gu = [up["endogenas"]["hiato"]["central"][tr.index(q)] for q in Q]
gd = [dn["endogenas"]["hiato"]["central"][tr.index(q)] for q in Q]
acc = 0.0; t_up = []
for k in range(6):
    acc = h1 * acc + 0.05; t_up.append(acc)
part_dn = [-0.45 * h1 ** (k + 1) for k in range(6)]
acc = 0.0; cc_dn = []
for k in range(6):
    acc = h1 * acc - 0.035; cc_dn.append(acc)
print("\n3.3 hiato: base | upside modelo -> com tempero | downside modelo -> com tempero")
for k, q in enumerate(Q):
    print(f"  {q}: {gap[q]:.2f} | {gu[k]:.2f} -> {gu[k]+t_up[k]:.2f} | {gd[k]:.2f} -> {gd[k]+part_dn[k]+cc_dn[k]:.2f}")
# PIB yoy nos cenarios de cauda (mecanico, mesmo potencial), com o hiato do 3T26 do tempero no downside
gu_all = {**obs, **{q: gu[k] + t_up[k] for k, q in enumerate(Q)}}
gd_all = {**obs, "3T26": obs["3T26"] - 0.45, **{q: gd[k] + part_dn[k] + cc_dn[k] for k, q in enumerate(Q)}}
print("3.3 PIB yoy: base | upside com tempero | downside com tempero")
for q in Q:
    q4 = ordem[ordem.index(q) - 4]
    print(f"  {q}: {pib[q]:.2f} | {pot + gu_all[q] - gu_all[q4]:.2f} | {pot + gd_all[q] - gd_all[q4]:.2f}")
