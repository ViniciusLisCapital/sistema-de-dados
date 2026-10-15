"""G · câmbio · ciclo 2026-10-15: o CDS de 5 anos no fechamento de cada trimestre
(`cmb_risco_pais`), para comparar com o nível que o Modelo Estrutural lê, e o desvio-padrão
da variação trimestral do CDS na amostra de estimação da equação do câmbio."""
import json
import sys
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
A = Path(__file__).resolve().parents[1] / "A"

cds = pd.read_csv(A / "cmb_risco_pais.csv.gz", parse_dates=["date"]).set_index("date")["value"]
fech = cds.resample("QE").last()
print("CDS no fechamento do trimestre (cmb_risco_pais):")
print(fech.loc["2025-04-01":].round(2).to_string())
print()
print("CDS de 22/09 a 14/10:")
print(cds.loc["2026-09-22":].round(2).to_string())
print()

p = json.loads((A / "modelo_estrutural.json").read_text(encoding="utf-8"))["p"]
F = p["eq"]["F"]
rot = p["rot"]
niv = pd.Series(F["nivel"]["fiscal"], index=rot, dtype="float")
i0, i1 = F["est_i0"], F["est_i1"]
d = niv.diff().iloc[i0:i1 + 1]
print("modelo: nível do CDS 2006T1..:", niv.iloc[i0 - 1:i0 + 4].round(1).to_dict())
print(f"sd da variação trimestral do CDS no modelo, {F['est_ini']} a {F['est_fim']}: "
      f"{d.std():.2f} (o modelo usa sd = {F['sd']['fiscal']:.2f})")
print(f"maior alta trimestral: {d.max():.1f} em {d.idxmax()}; maior queda: {d.min():.1f} em {d.idxmin()}")
