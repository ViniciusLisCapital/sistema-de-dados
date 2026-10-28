"""G cambio: resíduo da equação do câmbio (F) do Modelo Estrutural (y − ajuste, A/modelo_estrutural.json) por trimestre do ano,
para ver se o 4º trimestre (remessas de dezembro) deixa depreciação que o modelo não explica."""
import json
import numpy as np
import pandas as pd
from pathlib import Path

A = Path(__file__).resolve().parent.parent / "A"
p = json.load(open(A / "modelo_estrutural.json", encoding="utf-8"))["p"]
F = p["eq"]["F"]
df = pd.DataFrame({"tri": p["rot"], "y": F["y"], "aj": F["ajuste"]}).dropna()
df["res"] = df.y - df.aj
df["q"] = df.tri.str[-1]
g = df.groupby("q").res.agg(["mean", "median", "std", "count"])
g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
print(g.round(2).to_string())
print("\nResíduos do 4º trimestre:", df[df.q == "4"][["tri", "res"]].round(2).to_string(index=False))
print("\nResíduos recentes:", df.tail(8)[["tri", "y", "aj", "res"]].round(2).to_string(index=False))
q4r = df[(df.q == "4") & (df.tri >= "2017")].res
print(f"\n4º trimestre desde 2017: média {q4r.mean():.2f}, mediana {q4r.median():.2f}, positivos {int((q4r>0).sum())} de {len(q4r)}")
