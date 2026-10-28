"""Atividade, rodada 2: a central do P1 e a distribuição revista (seções 1, 3 e 3.3).

- Base: o Modelo Estrutural com os caminhos usados no P1 (P1.json, caminhos_usados), sem multiplicador;
  confere que reproduz a central do P1.
- Aperto da (H) no base: Selic média − (rr_10a + meta_12m), com os caminhos do P1.
- Cenários de cauda: P1 + H.h2 x0,5 (upside) e P1 + H.h2 x1,5 (downside).
- Temperos (deslocamentos da média da distribuição do agente contra a central), por trimestre:
    partida: −0,15 p.p. no 3T26, levado pela inércia h1;
    resiliência: choque por trimestre na (H) = 0,02 (parte fora do fiscal: renda, emprego, direcionado, todo o
      horizonte) + 0,09 x impulso fiscal do agente fiscal (base, p.p. do PIB, FE-AT1 do fiscal_r1) + 0,02 de
      parafiscal no 4T26–2T27, acumulado pela inércia; 0,09 = (0,05 − 0,02) / 0,35, os +0,05 por trimestre da
      rodada 1 contra o impulso medido de ~+0,35;
    condições financeiras: −0,02 por trimestre no 4T26–1T27, −0,01 depois, acumulado;
    Selic da política monetária acima da do modelo (S-PM1): aperto extra de +0,30, +0,50, +0,40, +0,30, +0,20, +0,10
      p.p. no 4T26…1T28, que chega ao hiato no trimestre seguinte pelo H.h2, acumulado.
- Linha companheira: 2,50 + hiato(q) − hiato(q−4); hiato observado da edição set/26 até o 3T26.
- Distribuição: normal em torno de central + deslocamento; DP como na rodada 1 (at_tese.py).
"""
import json
import math
from pathlib import Path

import pandas as pd

from analytics.agent_system import modelo

CIC = Path(__file__).resolve().parents[2]
A = CIC / "dados" / "A"
Q = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
P1 = json.loads((CIC / "P1.json").read_text(encoding="utf-8"))
cam = P1["caminhos_usados"]

sim = modelo.carregar("2026-10-27")
base = modelo.rodar(sim, caminhos=cam)
up = modelo.rodar(sim, caminhos=cam, mult={"H.h2": 0.5})
dn = modelo.rodar(sim, caminhos=cam, mult={"H.h2": 1.5})
tr = base["trimestres"]


def serie(res, var, campo="central"):
    return [res["endogenas"][var][campo][tr.index(q)] for q in Q]


gap = serie(base, "hiato")
p1gap = [P1["modelo"]["endogenas"]["hiato"]["central"][P1["modelo"]["trimestres"].index(q)] for q in Q]
print("hiato base (rodado) :", " | ".join(f"{x:.3f}" for x in gap))
print("hiato P1 (arquivo)  :", " | ".join(f"{x:.3f}" for x in p1gap))
lo = serie(base, "hiato", "lo"); hi = serie(base, "hiato", "hi")
print("faixa90 pesos       :", " | ".join(f"[{a:.2f};{b:.2f}]" for a, b in zip(lo, hi)))
sel = serie(base, "selic")
rr = [cam["rr_10a"][q] for q in Q]; mt = [cam["meta_12m"][q] for q in Q]
print("Selic media         :", " | ".join(f"{x:.2f}" for x in sel))
print("aperto (H)          :", " | ".join(f"{s - r - m:.2f}" for s, r, m in zip(sel, rr, mt)))
print("IPCA 12m            :", " | ".join(f"{x:.2f}" for x in serie(base, "ipca_12m")))
print("hiato upside h2x0,5 :", " | ".join(f"{x:.2f}" for x in serie(up, "hiato")))
print("hiato downside x1,5 :", " | ".join(f"{x:.2f}" for x in serie(dn, "hiato")))
print("Selic up / down     :", " | ".join(f"{a:.2f}/{b:.2f}" for a, b in zip(serie(up, "selic"), serie(dn, "selic"))))
print("IPCA12m up / down   :", " | ".join(f"{a:.2f}/{b:.2f}" for a, b in zip(serie(up, "ipca_12m"), serie(dn, "ipca_12m"))))

h1 = 0.874689157807679
h2 = -0.07091757284446645


def acumula(choques):
    acc, out = 0.0, []
    for c in choques:
        acc = h1 * acc + c
        out.append(acc)
    return out


part = [-0.15 * h1 ** (k + 1) for k in range(6)]
imp = [0.1, 0.0, -0.1, -0.1, -0.2, -0.3]                 # fiscal_r1, FE-AT1, base
para = [0.02, 0.02, 0.02, 0.0, 0.0, 0.0]
fis_ch = [0.02 + 0.09 * i + p for i, p in zip(imp, para)]
fis = acumula(fis_ch)
cc = acumula([-0.02, -0.02, -0.01, -0.01, -0.01, -0.01])
extra = [0.30, 0.50, 0.40, 0.30, 0.20, 0.10]              # aperto extra (Selic da PM acima do modelo)
pm = acumula([0.0] + [h2 * e for e in extra[:-1]])         # chega no trimestre seguinte
shift = [a + b + c + d for a, b, c, d in zip(part, fis, cc, pm)]
print("\nchoque fiscal/tri   :", " | ".join(f"{x:+.3f}" for x in fis_ch))
print("desloc. partida     :", " | ".join(f"{x:+.2f}" for x in part))
print("desloc. fiscal      :", " | ".join(f"{x:+.2f}" for x in fis))
print("desloc. cond. fin.  :", " | ".join(f"{x:+.2f}" for x in cc))
print("desloc. Selic PM    :", " | ".join(f"{x:+.2f}" for x in pm))
print("desloc. total       :", " | ".join(f"{x:+.2f}" for x in shift))

# distribuicao (DP e larguras da rodada 1)
sd_H = [0.34, 0.45, 0.51, 0.56, 0.60, 0.62]
sd_part = [0.25 * h1 ** (k + 1) for k in range(6)]
sd_w = [(b - a) / 2 / 1.645 for a, b in zip(lo, hi)]
sd_gap = [math.sqrt(a * a + b * b + w * w) for a, b, w in zip(sd_H, sd_part, sd_w)]
w_gap = [0.30, 0.35, 0.40, 0.45, 0.45, 0.50]


def ncdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def probs(c, s, sd, w):
    mu = c + s
    l, h = round(c - w, 2), round(c + w, 2)
    pdn = round(ncdf((l - mu) / sd) * 100); pup = round((1 - ncdf((h - mu) / sd)) * 100)
    return l, h, 100 - pdn - pup, pup, pdn


tese = {"hiato": {}, "pib_yoy": {}}
print("\nHiato: central | sd | desl | faixa | P faixa/up/down | assim")
for k, q in enumerate(Q):
    c = round(gap[k], 2)
    l, h, pf, pu, pd_ = probs(c, shift[k], sd_gap[k], w_gap[k])
    tese["hiato"][q] = dict(central=c, faixa=[l, h], p_faixa=pf, p_upside=pu, p_downside=pd_)
    print(f"  {q}: {c:.2f} | {sd_gap[k]:.2f} | {shift[k]:+.2f} | [{l:.2f}; {h:.2f}] | {pf}/{pu}/{pd_} | {(pu-pd_)/100:+.2f}")

hp = pd.read_csv(A / "pm_hiato_produto.csv.gz", parse_dates=["date"])
cobs = hp[hp.variavel == "central"].set_index("date")["value"]
obs = {"4T25": cobs.loc["2025-10-01"], "1T26": cobs.loc["2026-01-01"], "2T26": cobs.loc["2026-04-01"], "3T26": cobs.loc["2026-07-01"]}
ordem = ["4T25", "1T26", "2T26", "3T26"] + Q
allg = {**obs, **{q: g for q, g in zip(Q, gap)}}
pib = {q: 2.50 + allg[q] - allg[ordem[ordem.index(q) - 4]] for q in Q}
sd_pot = 0.30
shift_all = {"4T25": 0, "1T26": 0, "2T26": 0, "3T26": -0.15, **{q: s for q, s in zip(Q, shift)}}
direto = {"4T26": -0.15, "1T27": -0.10}
w_pib = [0.35, 0.40, 0.45, 0.50, 0.50, 0.50]
print("\nPIB 4 tri: central (conta) | sd | desl | faixa | P | assim")
for k, q in enumerate(Q):
    q4 = ordem[ordem.index(q) - 4]
    base_sd = sd_gap[k] if k < 4 else math.sqrt(sd_H[3] ** 2 + sd_w[k] ** 2)
    sd = math.sqrt(base_sd ** 2 + sd_pot ** 2)
    sh = shift_all[q] - shift_all[q4] + direto.get(q, 0)
    c = round(pib[q], 2)
    l, h, pf, pu, pd_ = probs(c, sh, sd, w_pib[k])
    tese["pib_yoy"][q] = dict(central=c, faixa=[l, h], p_faixa=pf, p_upside=pu, p_downside=pd_)
    print(f"  {q}: {c:.2f} (2,50 + {allg[q]:.2f} - {allg[q4]:.2f}) | {sd:.2f} | {sh:+.2f} | [{l:.2f}; {h:.2f}] | {pf}/{pu}/{pd_} | {(pu-pd_)/100:+.2f}")

# 3.3: cenarios de cauda com tempero
gu, gd = serie(up, "hiato"), serie(dn, "hiato")
t_up = [a + b for a, b in zip(
    acumula([0.02 + 0.09 * i + p for i, p in zip([0.3, 0.3, 0.4, 0.4, 0.5, 0.3], [0.03, 0.03, 0.03, 0.02, 0.01, 0.0])]),
    acumula([0.0] + [0.5 * h2 * e for e in extra[:-1]]))]   # upside: impulso do upside fiscal; Copom para em 13,75
part_dn = [-0.45 * h1 ** (k + 1) for k in range(6)]
cc_dn = acumula([-0.035] * 6)
extra_dn = [0.50, 1.40, 1.80, 1.50, 1.20, 0.90]           # regime de alta da PM contra a Selic do modelo
pm_dn = acumula([0.0] + [1.5 * h2 * e for e in extra_dn[:-1]])
fis_dn = acumula([0.09 * i + p for i, p in zip(imp, para)])   # downside: impulso base, sem a parte fora do fiscal
print("\n3.3 hiato: base | upside modelo -> com tempero | downside modelo -> com tempero (partida, cc, Selic PM, fiscal)")
for k, q in enumerate(Q):
    d_all = gd[k] + part_dn[k] + cc_dn[k] + pm_dn[k] + fis_dn[k]
    print(f"  {q}: {gap[k]:.2f} | {gu[k]:.2f} -> {gu[k]+t_up[k]:.2f} | {gd[k]:.2f} -> {d_all:.2f} "
          f"({part_dn[k]:+.2f}, {cc_dn[k]:+.2f}, {pm_dn[k]:+.2f}, {fis_dn[k]:+.2f})")
gu_all = {**obs, **{q: gu[k] + t_up[k] for k, q in enumerate(Q)}}
gd_all = {**obs, "3T26": obs["3T26"] - 0.45,
          **{q: gd[k] + part_dn[k] + cc_dn[k] + pm_dn[k] + fis_dn[k] for k, q in enumerate(Q)}}
print("3.3 PIB 4 tri: base | upside | downside")
for q in Q:
    q4 = ordem[ordem.index(q) - 4]
    print(f"  {q}: {pib[q]:.2f} | {2.5 + gu_all[q] - gu_all[q4]:.2f} | {2.5 + gd_all[q] - gd_all[q4]:.2f}")

# BC (RPM set/26) projeta -0,4 no 1T28; o P1 contra ela
print(f"\nP1 1T28 {gap[-1]:.2f} contra -0,4 do RPM: {gap[-1] + 0.4:+.2f}")
(Path(__file__).with_suffix(".json")).write_text(json.dumps(tese, ensure_ascii=False, indent=1), encoding="utf-8")
