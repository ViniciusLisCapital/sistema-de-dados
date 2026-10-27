"""at_ · (1) o aperto de (H) por trimestre no base; (2) a sensibilidade do hiato ao ponto de partida
(3T26); (3) a linha companheira com o potencial do BC (2,495) e com o da QPC (2,00); (4) o carrego do
IBC-Br para o 4T26 em termos interanuais. Coeficientes: medianas de modelo.listar (H.h1 0,875,
H.h2 -0,071). Selic média do base: saída de at_cenarios_r1.py."""
import pandas as pd
h1, h2 = 0.875, -0.071
TRI = ["3T26", "4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
selic = dict(zip(TRI, [14.06, 13.60, 13.26, 12.96, 12.70, 12.47, 12.27]))
rr, meta = 7.84, 3.00
print("(1) aperto = Selic média − (rr_10a + meta), padrão do simulador:")
for t in TRI:
    print(f"  {t}: {selic[t] - rr - meta:.2f}")
rrf = dict(zip(TRI[1:], [7.55, 7.60, 7.55, 7.50, 7.45, 7.40]))
self_ = dict(zip(TRI[1:], [13.31, 13.01, 12.67, 12.36, 12.08, 11.83]))
print("    com o rr_10a do fiscal:", {t: round(self_[t] - rrf[t] - meta, 2) for t in TRI[1:]})
T3 = selic["3T26"] - rr - meta
print("(2) hiato 4T26 = h1·hiato3T26 + h2·aperto3T26, e o efeito no 1T28 (h1^6 do desvio):")
for g in [0.41, 0.28, 0.10, -0.10, -0.30]:
    d = g - 0.41
    print(f"  hiato 3T26 = {g:+.2f} -> 4T26 {h1*g + h2*T3:+.2f}; desvio no 1T28 {d*h1**6:+.2f}")
# (3) linha companheira
hb = dict(zip(TRI[1:], [0.13, -0.08, -0.24, -0.36, -0.45, -0.51]))
obs = {"4T25": 0.74, "1T26": 0.60, "2T26": 0.51, "3T26": 0.41}
g = {**obs, **hb}
ant = {"4T26": "4T25", "1T27": "1T26", "2T27": "2T26", "3T27": "3T26", "4T27": "4T26", "1T28": "1T27"}
for pot in [2.495, 2.00]:
    print(f"(3) potencial {pot}: ", {t: round(pot + g[t] - g[ant[t]], 2) for t in ant})
# (4) carrego do IBC-Br para o 4T26: o nível de agosto mantido até dezembro, contra o 4T25 (dessaz.)
d = pd.read_csv("../A/atv_ibcbr.csv.gz", parse_dates=["date"])
for nome in ["ibcbr_sa", "ibcbr_ex_agropecuaria_sa"]:
    s = d[d.name == nome].set_index("date")["value"]
    q4 = s["2025-10-01":"2025-12-01"].mean(); q3_25 = s["2025-07-01":"2025-09-01"].mean()
    ago = s["2026-08-01"]
    print(f"(4) {nome}: agosto/26 mantido contra 4T25 {100*(ago/q4-1):+.2f}%; contra 3T25 {100*(ago/q3_25-1):+.2f}%")
