"""G cambio: volatilidade implícita de 3 meses (série trimestral do retrato do Modelo Estrutural, A/modelo_estrutural.json)
contra a volatilidade realizada da PTAX (A/cmb_ptax) no fechamento de cada trimestre; relação histórica, leitura de hoje,
e o decaimento da implícita depois dos trimestres de pico."""
import json
import numpy as np
import pandas as pd
from pathlib import Path

A = Path(__file__).resolve().parent.parent / "A"
d = json.load(open(A / "modelo_estrutural.json", encoding="utf-8"))
p = d["p"]
rot = p["rot"]; vol = p["var"]["vol"]["obs"]
iv = pd.Series(vol, index=rot, dtype="float")

pt = pd.read_csv(A / "cmb_ptax.csv.gz", parse_dates=["date"])
pt = pt[pt.name == "ptax_venda"].set_index("date").value.sort_index()
r = np.log(pt).diff().dropna()
rv21 = r.rolling(21).std() * np.sqrt(252) * 100
rv63 = r.rolling(63).std() * np.sqrt(252) * 100

def fim(rotulo):
    a, q = int(rotulo[:4]), int(rotulo[-1])
    return pd.Timestamp(a, 3 * q, 1) + pd.offsets.MonthEnd(0)

linhas = []
for k in rot:
    t = fim(k)
    s21 = rv21[rv21.index <= t]; s63 = rv63[rv63.index <= t]
    linhas.append((k, iv[k], s21.iloc[-1] if len(s21) else np.nan, s63.iloc[-1] if len(s63) else np.nan))
df = pd.DataFrame(linhas, columns=["tri", "implicita", "real21", "real63"]).set_index("tri")
print(df.round(2).to_string())
ok = df.dropna()
print("\nN =", len(ok))
for c in ("real21", "real63"):
    b = np.polyfit(ok[c], ok.implicita, 1)
    res = ok.implicita - np.polyval(b, ok[c])
    print(f"implicita = {b[1]:.2f} + {b[0]:.3f}*{c}  (desvio do resíduo {res.std():.2f}); corr {ok[c].corr(ok.implicita):.2f}")
X = np.column_stack([np.ones(len(ok)), ok.real21, ok.real63])
coef, *_ = np.linalg.lstsq(X, ok.implicita, rcond=None)
res = ok.implicita - X @ coef
print(f"implicita = {coef[0]:.2f} + {coef[1]:.3f}*real21 + {coef[2]:.3f}*real63  (desvio do resíduo {res.std():.2f})")
print("razão implícita/real63: mediana", round((ok.implicita / ok.real63).median(), 2))
print("\nPercentis da implícita trimestral 2006-2026:", np.percentile(ok.implicita, [10, 25, 50, 75, 90, 95]).round(2))
print("\nHoje (último pregão):", rv21.index[-1].date(), "real21", round(rv21.iloc[-1], 2), "real63", round(rv63.iloc[-1], 2))
print("Hoje sem o pregão de 26/10 (até 23/10): real21", round(rv21.iloc[-2], 2), "real63", round(rv63.iloc[-2], 2))
for c in ("real21", "real63"):
    b = np.polyfit(ok[c], ok.implicita, 1)
    print(f"implícita ajustada por {c} hoje: {np.polyval(b, rv21.iloc[-1] if c=='real21' else rv63.iloc[-1]):.2f}")
print(f"implícita ajustada pelas duas hoje: {coef[0] + coef[1]*rv21.iloc[-1] + coef[2]*rv63.iloc[-1]:.2f}")
print("3T26 (30/09): real21", round(rv21[rv21.index <= '2026-09-30'].iloc[-1], 2), "real63", round(rv63[rv63.index <= '2026-09-30'].iloc[-1], 2),
      "→ implícita ajustada (duas)", round(coef[0] + coef[1]*rv21[rv21.index <= '2026-09-30'].iloc[-1] + coef[2]*rv63[rv63.index <= '2026-09-30'].iloc[-1], 2))

print("\nDecaimento: trimestres com implícita >= 20, e os 4 seguintes")
v = iv.dropna()
for i, k in enumerate(v.index):
    if v.iloc[i] >= 20 and (i == 0 or v.iloc[i-1] < 20):
        print(k, list(v.iloc[i:i+6].round(1)))
print("\nMaior retorno diário da PTAX (log, %), top 8:")
print((r * 100).sort_values(ascending=False).head(8).round(2).to_string())
