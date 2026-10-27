"""pm: leituras do ciclo 2026-10-02 que o F não traz prontas (só lê ../A/).

1. Brent: trajetória diária desde ago/26, média do 3T26, valor na data de corte do RPM (11/09),
   na reunião (16/09) e em 25/09 e 02/10.
2. Curvas: NTN-B 10a, DI 10a e inflação implícita 10a (DI − NTN-B, em forma composta) em datas-chave;
   médias do 3T26 e o que o 4T26 dá se o último valor ficar parado.
3. Focus conhecido em 02/10: a última pesquisa publicada até 02/10 é a de 25/09 (sai em 28/09).
   Selic por reunião, IPCA por ano, IPCA 12m suavizado, e o juro real ex-ante.
4. IPCA de agosto (12m) e IPCA-15 de setembro, os que existiam em 02/10.
"""
from pathlib import Path

import numpy as np
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"


def rd(t):
    return pd.read_csv(A / f"{t}.csv.gz", parse_dates=["date"])


print("== 1. Brent ==")
b = rd("comm_brent").set_index("date")["value"]
print(b["2026-08-25":].to_string())
print("média jul-set/26:", round(b["2026-07-01":"2026-09-30"].mean(), 2))
print("média ago/26:", round(b["2026-08"].mean(), 2), " média set/26:", round(b["2026-09"].mean(), 2))
for d in ["2026-09-11", "2026-09-16", "2026-09-25", "2026-10-01", "2026-10-02"]:
    print(d, b[:d].iloc[-1])
print("10 dias úteis até 11/09:", round(b[:"2026-09-11"].iloc[-10:].mean(), 2))
print("var % 25/09 -> 02/10:", round(100 * (b["2026-10-02"] / b[:"2026-09-25"].iloc[-1] - 1), 1))
print("var % 16/09 -> 02/10:", round(100 * (b["2026-10-02"] / b[:"2026-09-16"].iloc[-1] - 1), 1))
print("máximo histórico antes de 2026:", b[:"2025-12-31"].max(), b[:"2025-12-31"].idxmax().date())

print("\n== 2. Curvas ==")
r = rd("br_interest_rate")
ntnb = r[(r.curve == "NTNBJS") & (r.tenor == "120M")].set_index("date")["value"]
di = r[(r.curve == "DIPRE") & (r.tenor == "120M")].set_index("date")["value"]
ntnb5 = r[(r.curve == "NTNBJS") & (r.tenor == "60M")].set_index("date")["value"]
di5 = r[(r.curve == "DIPRE") & (r.tenor == "60M")].set_index("date")["value"]
ntnb2 = r[(r.curve == "NTNBJS") & (r.tenor == "24M")].set_index("date")["value"]
di2 = r[(r.curve == "DIPRE") & (r.tenor == "24M")].set_index("date")["value"]
bei = (100 * ((1 + di / 100) / (1 + ntnb / 100) - 1)).dropna()
bei5 = (100 * ((1 + di5 / 100) / (1 + ntnb5 / 100) - 1)).dropna()
bei2 = (100 * ((1 + di2 / 100) / (1 + ntnb2 / 100) - 1)).dropna()
for d in ["2026-06-30", "2026-09-11", "2026-09-16", "2026-09-25", "2026-09-30", "2026-10-02"]:
    print(d, "NTN-B10", round(ntnb[:d].iloc[-1], 2), "DI10", round(di[:d].iloc[-1], 2),
          "impl10", round(bei[:d].iloc[-1], 2), "| NTN-B5", round(ntnb5[:d].iloc[-1], 2),
          "impl5", round(bei5[:d].iloc[-1], 2), "| NTN-B2", round(ntnb2[:d].iloc[-1], 2),
          "impl2", round(bei2[:d].iloc[-1], 2))
for q, (i, f) in {"2T26": ("2026-04-01", "2026-06-30"), "3T26": ("2026-07-01", "2026-09-30")}.items():
    print(q, "média NTN-B10", round(ntnb[i:f].mean(), 3), " média impl10", round(bei[i:f].mean(), 2))
print("Δ 3m NTN-B10 (30/06 -> 02/10):", round(ntnb.iloc[-1] - ntnb[:"2026-06-30"].iloc[-1], 2),
      " Δ impl10:", round(bei.iloc[-1] - bei[:"2026-06-30"].iloc[-1], 2),
      " Δ DI10:", round(di.iloc[-1] - di[:"2026-06-30"].iloc[-1], 2))
print("Pctl 10a NTN-B10 hoje:", round(100 * (ntnb["2016-10-02":] <= ntnb.iloc[-1]).mean()))
print("NTN-B10 min/max 2025-2026:", round(ntnb["2025-01-01":].min(), 2), round(ntnb["2025-01-01":].max(), 2))
print("NTN-B 10a: média 2025:", round(ntnb["2025"].mean(), 2), " média 1S26:", round(ntnb["2026-01":"2026-06"].mean(), 2))
print(ntnb["2026-09-01":].round(2).to_string())

cds = rd("cmb_risco_pais").set_index("date")["value"]
for d in ["2026-06-30", "2026-09-16", "2026-09-25", "2026-10-02"]:
    print("CDS", d, round(cds[:d].iloc[-1], 1))

print("\n== 3. Focus conhecido em 02/10 (pesquisa de 25/09) ==")
fc = rd("expc_focus_copom")
fc = fc[(fc.base_calculo == 0)]
for d in ["2026-09-11", "2026-09-25", "2026-10-02"]:
    x = fc[fc.date == d][["reuniao", "mediana", "media", "minimo", "maximo"]]
    print(d); print(x.to_string(index=False))
fp = rd("expc_focus_periodo__ipca")
fp = fp[(fp.base_calculo == 0) & (fp.periodicidade == "anual")]
for d in ["2026-09-11", "2026-09-25", "2026-10-02"]:
    print(d, fp[fp.date == d][["data_referencia", "mediana"]].to_dict("records"))
fs = rd("expc_focus_periodo__selic")
fs = fs[(fs.base_calculo == 0)]
for d in ["2026-09-25", "2026-10-02"]:
    print("Selic anual", d, fs[fs.date == d][["data_referencia", "mediana"]].to_dict("records"))
f12 = rd("expc_focus")
f12 = f12[(f12.base_calculo == 0) & (f12.horizonte == "12m") & (f12.suavizada == "S")
          & (f12.indicador == "IPCA")].set_index("date")["mediana"]
for d in ["2026-09-11", "2026-09-25", "2026-10-02"]:
    v = f12[:d].iloc[-1]
    print("Focus IPCA 12m suav", d, v, " Selic real ex-ante (13,75):",
          round(100 * (1.1375 / (1 + v / 100) - 1), 2))
print("Focus IPCA 12m, média 3T26:", round(f12["2026-07-01":"2026-09-30"].mean(), 2))

# DI 1 ano contra o Focus 12m (ex-ante de mercado)
di1 = r[(r.curve == "DIPRE") & (r.tenor == "12M")].set_index("date")["value"]
for d in ["2026-09-25", "2026-10-02"]:
    print("DI 1a", d, round(di1[:d].iloc[-1], 2), " real ex-ante c/ Focus 12m:",
          round(100 * ((1 + di1[:d].iloc[-1] / 100) / (1 + f12[:d].iloc[-1] / 100) - 1), 2))

print("\n== 4. IPCA conhecido em 02/10 ==")
ia = rd("inflc_agregados")
for nm in ["ipca", "ipca15", "ipca_servicos", "ipca_livres", "ipca_administrados"]:
    s = ia[ia.name == nm].set_index("date")["value"]
    if s.empty:
        continue
    acc = lambda x: round(100 * (np.prod(1 + x / 100) - 1), 2)
    print(nm, "ago:", s.get(pd.Timestamp("2026-08-01")), " set:", s.get(pd.Timestamp("2026-09-01")),
          " 12m até ago:", acc(s[:"2026-08-01"].iloc[-12:]), " 12m até set:", acc(s[:"2026-09-01"].iloc[-12:]))
print(sorted(ia.name.unique())[:60])
