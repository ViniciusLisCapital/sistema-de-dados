"""in_tese: da etapa 1 à tese (seção 3.3 do report de inflação, ciclo 2026-10-27, rodada 1).

Soma, trimestre a trimestre, a saída do modelo em cada cauda (de in_cenarios.py, com os
multiplicadores do tipo (i)) e os temperos do tipo (ii) (tamanhos de in_temperos.py), e imprime o
JSON de caminhos da rodada. Os temperos (ii) entram no IPCA de 12 meses enquanto o choque
está na janela de 12 meses.
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
base = [5.28, 4.85, 4.33, 4.34, 4.23, 4.08]
up_mod = [5.33, 5.11, 4.69, 4.76, 4.64, 4.34]      # upside, modelo com ia3 e ii4 × 1,5
dn_mod = [5.26, 4.71, 4.14, 4.12, 3.99, 3.94]      # downside, modelo com ia3 e ii4 × 0,7 e is2 × 1,5

# (ii) upside: combustíveis +5% (metade em nov-dez/26, metade em jan/27) → +0,30 p.p. na janela
comb_up = [0.15, 0.30, 0.30, 0.30, 0.15, 0.00]
# (ii) upside: bandeira tarifária mais cara em nov-dez (+5% na energia), devolvida no 1T27
band_up = [0.10, 0.00, 0.00, 0.00, 0.00, 0.00]
# (ii) upside: salários além do hiato em serviços, de 4T27 em diante (+0,10 p.p.)
sal_up = [0.00, 0.00, 0.00, 0.00, 0.10, 0.10]
# (ii) downside: combustíveis −3% no 2T27 (o Brent volta e a Petrobras repassa com defasagem)
#      → −0,18 p.p. por quatro trimestres
comb_dn = [0.00, 0.00, -0.18, -0.18, -0.18, -0.18]
# (ii) downside: bandeira mais barata em nov-dez (−5% na energia), devolvida no 1T27
band_dn = [-0.10, 0.00, 0.00, 0.00, 0.00, 0.00]
# (ii) downside: in natura −5% no 4T26 e −5% no 1T27 (a oferta normaliza) → −0,12 e −0,24 p.p.,
#      saindo da janela de 12 meses no 4T27 e no 1T28
nat_dn = [-0.12, -0.24, -0.24, -0.24, -0.12, 0.00]

up = [round(sum(x), 2) for x in zip(up_mod, comb_up, band_up, sal_up)]
dn = [round(sum(x), 2) for x in zip(dn_mod, comb_dn, band_dn, nat_dn)]
print("| Trimestre | Central | Upside: modelo → com tempero | Downside: modelo → com tempero |")
for i, t in enumerate(T):
    print(f"| {t} | {base[i]:.2f} | {up_mod[i]:.2f} → {up[i]:.2f} | {dn_mod[i]:.2f} → {dn[i]:.2f} |")

# A tese (decisão do agente; a central é a do modelo)
faixa = {"4T26": (5.10, 5.45), "1T27": (4.60, 5.15), "2T27": (4.05, 4.70),
         "3T27": (4.05, 4.75), "4T27": (3.95, 4.60), "1T28": (3.80, 4.40)}
prob = {"4T26": (65, 25, 10), "1T27": (58, 30, 12), "2T27": (58, 30, 12),
        "3T27": (58, 30, 12), "4T27": (58, 28, 14), "1T28": (60, 25, 15)}
for i, t in enumerate(T):
    lo, hi = faixa[t]
    assert lo <= base[i] <= hi, t
    assert sum(prob[t]) == 100, t
    print(f"{t}: tail up {up[i]:.2f} > {hi}? {up[i] > hi} · tail dn {dn[i]:.2f} < {lo}? {dn[i] < lo}"
          f" · assimetria {(prob[t][1]-prob[t][2])/100:+.2f}")

out = {
    "agente": "inflacao", "rodada": "r1", "ciclo": "2026-10-27",
    "caminhos": {},
    "tese": {"ipca_12m": {"trimestres": {
        t: {"central": base[i], "faixa": list(faixa[t]), "p_faixa": prob[t][0],
            "p_upside": prob[t][1], "p_downside": prob[t][2]} for i, t in enumerate(T)}}},
    "nota": ("Rodada 1: central do Modelo Estrutural com todas as exógenas no padrão do simulador "
             "(nenhum principal publicou caminho). Subordinado de icbr_agr_usd e icbr_met_usd sem "
             "caminho de referência."),
}
print(json.dumps(out, ensure_ascii=False, indent=2))  # o agente grava em caminhos/ (o G não escreve fora de G/)
