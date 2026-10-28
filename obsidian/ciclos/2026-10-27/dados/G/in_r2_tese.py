"""in_r2_tese: da etapa 1 à tese (seção 3.3 do report de inflação, ciclo 2026-10-27, rodada 2).

Lê só ../A/ (pesos de set/26). Os números do modelo vêm de in_r2_cenarios.py, copiados abaixo.
 1. Pesos de set/26: os quatro grupos do BC, os alimentos in natura, gasolina+diesel+GNV.
 2. Tamanho dos temperos (ii): peso x variação suposta, e o perfil na janela de 12 meses.
 3. Caudas com tempero, faixa e probabilidades; conferências (faixa contém a central, P soma 100,
    cada cauda com tempero fica fora da faixa).
 4. Os grupos do modelo em 12 meses (contribuição / peso) no 4T26, 1T27 e 1T28, contra o Copom
    (pm_copom_projecoes, reunião 281: livres e administrados) e quanto de cada um explica a
    diferença no 1T28.
 5. O JSON da rodada (impresso; o agente grava em caminhos/).
"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
A = Path(__file__).resolve().parent.parent / "A"
rd = lambda n: pd.read_csv(A / f"{n}.csv.gz")
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]

# 1 -------------------------------------------------------------------------------------------
dc = rd("inflc_decomposicao")
dim = rd("inflc_dim")
dc["subitem_codigo"] = dc["subitem_codigo"].astype(str)
dim["subitem_codigo"] = dim["subitem_codigo"].astype(str)
x = dc[(dc.indice == "IPCA") & (dc.date == "2026-09-01")].merge(
    dim[["subitem_codigo", "nome", "grupo", "subgrupo", "item"]], on="subitem_codigo", how="left")
tot = x.pesos.sum()
x["bc"] = x.apply(lambda r: "Monitorados" if r.grupo == "Monitorados" else
                  {"Alimentos": "Alimentação", "Bens Industriais": "Industriais",
                   "Serviços": "Serviços"}.get(r.subgrupo, "?"), axis=1)
w = (x.groupby("bc").pesos.sum() / tot * 100).to_dict()
w_nat = x[x.item == "Alimentos in natura"].pesos.sum() / tot * 100
w_comb = x[(x.grupo == "Monitorados") & x.nome.isin(["Gasolina", "Óleo diesel", "Gás veicular"])].pesos.sum() / tot * 100
w_ener = x[x.nome == "Energia elétrica residencial"].pesos.sum() / tot * 100
print("1. pesos (%):", {k: round(v, 2) for k, v in w.items()},
      f"in natura {w_nat:.2f} · combustíveis monitorados {w_comb:.2f} · energia {w_ener:.2f}")

# 2 -------------------------------------------------------------------------------------------
r2 = lambda v: round(v, 2)
comb5, comb3 = r2(0.05 * w_comb), r2(0.03 * w_comb)
nat5 = r2(0.05 * w_nat)
band = r2(0.025 * w_ener)
print(f"2. combustíveis +5% = {comb5}; −3% = {comb3}; in natura ±5% = {nat5}; energia ±2,5% = {band};"
      f" (energia ±5% seria {0.05*w_ener:.2f})")
# upside
comb_up = [r2(comb5 / 2), comb5, comb5, comb5, r2(comb5 / 2), 0.0]   # metade nov-dez/26, metade jan/27
band_up = [band, 0, 0, 0, 0, 0]                                    # um patamar acima em nov-dez
nat_up = [nat5, nat5, 0, 0, 0, 0]                                  # +5% no 4T26, devolvido no 2T27
sal_up = [0, 0, 0, 0, 0.10, 0.10]                                  # salário além do hiato
# downside
comb_dn = [0, 0, -comb3, -comb3, -comb3, -comb3]                   # −3% no 2T27
band_dn = [-band, 0, 0, 0, 0, 0]                                   # verde em nov-dez
nat_dn = [0, -nat5, -2 * nat5, -2 * nat5, -2 * nat5, -nat5]        # −5% no 1T27 e −5% no 2T27

# 3 -------------------------------------------------------------------------------------------
base = [5.320, 4.956, 4.483, 4.518, 4.382, 4.193]       # P1 = in_r2_cenarios, base
up_mod0 = [5.404, 5.218, 4.889, 5.007, 4.843, 4.532]    # upside, modelo
up_mod = [5.438, 5.325, 5.053, 5.200, 5.021, 4.662]     # upside, modelo + ia3, ii4 x 1,5
dn_mod0 = [5.242, 4.714, 4.081, 3.990, 3.842, 3.742]    # downside, modelo
dn_mod = [5.243, 4.707, 4.058, 3.950, 3.781, 3.664]     # downside, modelo + ia3, ii4 x 0,7, is2 x 1,5
up = [round(sum(v), 2) for v in zip(up_mod, comb_up, band_up, nat_up, sal_up)]
dn = [round(sum(v), 2) for v in zip(dn_mod, comb_dn, band_dn, nat_dn)]
print("3. | Tri | Central | Upside modelo → (i) → (ii) | Downside modelo → (i) → (ii) |")
for i, t in enumerate(T):
    print(f"   | {t} | {base[i]:.2f} | {up_mod0[i]:.2f} → {up_mod[i]:.2f} → {up[i]:.2f} |"
          f" {dn_mod0[i]:.2f} → {dn_mod[i]:.2f} → {dn[i]:.2f} |")
faixa = {"4T26": (5.15, 5.50), "1T27": (4.70, 5.25), "2T27": (4.15, 4.85),
         "3T27": (4.20, 4.90), "4T27": (4.05, 4.75), "1T28": (3.85, 4.55)}
prob = {"4T26": (65, 22, 13), "1T27": (58, 28, 14), "2T27": (57, 29, 14),
        "3T27": (57, 29, 14), "4T27": (57, 28, 15), "1T28": (58, 26, 16)}
for i, t in enumerate(T):
    lo, hi = faixa[t]
    assert lo <= base[i] <= hi, t
    assert sum(prob[t]) == 100, t
    assert up[i] > hi and dn[i] < lo, t
    print(f"   {t}: faixa {lo}–{hi} · central {base[i]:.2f} · acima da central {hi-base[i]:+.2f},"
          f" abaixo {lo-base[i]:+.2f} · assimetria {(prob[t][1]-prob[t][2])/100:+.2f}")

# 4 -------------------------------------------------------------------------------------------
contrib = {"4T26": (2.056, 0.999, 0.901, 1.367), "1T27": (1.960, 0.962, 0.832, 1.213),
           "1T28": (1.692, 0.637, 0.891, 0.973)}            # serv, alim, ind, mon (P1)
wl = w["Serviços"] + w["Alimentação"] + w["Industriais"]
cop = {"4T26": (5.2, 5.3), "1T27": (5.0, 4.5), "1T28": (3.2, 3.2)}   # livres, administrados
for t, (s, a, i_, m) in contrib.items():
    livres = (s + a + i_) / wl * 100
    mon = m / w["Monitorados"] * 100
    print(f"4. {t}: livres ≈ {livres:.2f}% (Copom {cop[t][0]}), monitorados ≈ {mon:.2f}% (Copom {cop[t][1]});"
          f" serviços ≈ {s/w['Serviços']*100:.2f}%, alimentação ≈ {a/w['Alimentação']*100:.2f}%,"
          f" industriais ≈ {i_/w['Industriais']*100:.2f}%")
s, a, i_, m = contrib["1T28"]
livres = (s + a + i_) / wl * 100
mon = m / w["Monitorados"] * 100
print(f"   1T28, diferença de 4,19 contra 3,2 = {4.19-3.2:.2f}: livres {(livres-3.2)*wl/100:.2f} p.p.,"
      f" monitorados {(mon-3.2)*w['Monitorados']/100:.2f} p.p.")
print(f"   modelo − Copom por trimestre: " + ", ".join(
    f"{t} {b - c:+.2f}" for t, b, c in zip(T, base, [5.2, 4.9, 4.5, 4.5, 3.9, 3.2])))
print(f"   com o câmbio do downside do câmbio (5,19 no 4T26), 1T28: {4.193 - 0.066:.2f}")

# 4b. contas do texto --------------------------------------------------------------------------
print(f"4b. IPCA set/26 contra a projeção mensal do Copom (0,65): {0.82-0.65:+.2f} p.p.")
ptax_p1 = [5.435, 5.503, 5.508, 5.495, 5.526, 5.565]
ptax_pad = [5.210, 5.247, 5.251, 5.237, 5.253, 5.278]
print("    PTAX P1 contra o padrão (%): " + "  ".join(f"{(a/b-1)*100:+.1f}" for a, b in zip(ptax_p1, ptax_pad)))
print("    PTAX P1 contra o condicionante do Copom, 5,15 (%): " + "  ".join(f"{(a/5.15-1)*100:+.1f}" for a in ptax_p1))
r1c = {"alim": [0.96, 0.88, 0.59, 0.64, 0.63, 0.61], "ind": [0.90, 0.81, 0.77, 0.80, 0.82, 0.81]}
p1c = {"alim": [0.999, 0.962, 0.691, 0.740, 0.694, 0.637], "ind": [0.901, 0.832, 0.825, 0.875, 0.911, 0.891]}
for g in r1c:
    print(f"    contribuição {g}, P1 − rodada 1 (p.p.): " + "  ".join(f"{a-b:+.2f}" for a, b in zip(p1c[g], r1c[g])))
med = {"I.IA.ia3": 0.08487585, "I.II.ii4": 0.03984321, "I.IS.is2": 0.09217197}
for k, v in med.items():
    print(f"    {k}: x1,5 = {v*1.5:.3f} · x0,7 = {v*0.7:.3f}")

# 5 -------------------------------------------------------------------------------------------
out = {
    "agente": "inflacao", "rodada": "r2", "ciclo": "2026-10-27",
    "caminhos": {},
    "tese": {"ipca_12m": {"trimestres": {
        t: {"central": round(base[i], 2), "faixa": list(faixa[t]), "p_faixa": prob[t][0],
            "p_upside": prob[t][1], "p_downside": prob[t][2]} for i, t in enumerate(T)}}},
    "nota": ("Rodada 2: central do P1 (caminhos dos principais), sem ajuste. Subordinado de "
             "icbr_agr_usd e icbr_met_usd, sem caminho de referência; principal de nenhuma exógena."),
}
print(json.dumps(out, ensure_ascii=False, indent=2))
