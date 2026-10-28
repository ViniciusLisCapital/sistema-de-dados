"""fi: o impulso que a mediana Focus do primário implica por ano (−Δ do primário, % do PIB), partindo do
primário consolidado de 2025 (NFSP, 12m em dez/25); e a distância do primário de hoje ao que estabiliza a DLSP."""
from pathlib import Path
import pandas as pd
A = Path(__file__).resolve().parent.parent / "A"
f = pd.read_csv(A / "expc_focus_periodo__fiscal__fiscal.csv.gz", parse_dates=["date"])
f = f[f.indicador.str.startswith("Resultado prim")]
for dia in ["2026-10-23", "2026-09-25"]:
    x = f[f.date == dia].set_index("data_referencia").mediana
    nf = pd.read_csv(A / "fisc_nfsp.csv.gz", parse_dates=["date"])
    p25 = nf[(nf.name == "resultado_primario_pct_pib_12m") & (nf.date == "2025-12-01")].value.iloc[0]
    seq = {2025: p25} | {a: x.get(a) for a in [2026, 2027, 2028, 2029]}
    print(f"Focus {dia}: primário", seq)
    anos = sorted(seq)
    print("  impulso implícito (−Δ, p.p.):", {a: round(-(seq[a] - seq[a - 1]), 2) for a in anos[1:]})
print("Distância do primário 12m de ago/26 (−0,62, NFSP) ao que estabiliza a DLSP (4,26, fi_contas.py):", round(4.26 - (-0.62), 2), "p.p.")
print("EFGG: Δ da despesa exceto juros +1,95 p.p.; dos quais precatórios (1,30 − 0,32):", round(1.30 - 0.32, 2), "p.p.; resto", round(1.95 - (1.30 - 0.32), 2))
print("Melhora que set-dez/26 precisa ter contra set-dez/25 para o primário 12m ir de −0,62 (ago/26) ao Focus 2026 (−0,48):", round(-0.48 - (-0.62), 2), "p.p. do PIB")
print("NTN-B 10a: 26/10 contra 3T26 médio (8,05 − 7,84):", round(8.05 - 7.84, 2), "· contra 23/10 (8,05 − 6,70):", round(8.054 - 6.700, 2))
print("Base rr_10a contra o padrão do simulador (7,84) em 4T26:", round(7.70 - 7.84, 2), "; upside 1T27:", round(8.80 - 7.84, 2))
