"""pm: a inflação que existia em 02/10 (IPCA até agosto, divulgado em 10/09; IPCA-15 de setembro,
divulgado em 25/09). O IPCA de setembro saiu em 09/10, depois do corte, e fica de fora aqui.
Acumulado em 12 meses dos núcleos, de serviços, de livres e de administrados até agosto, e a média
dos núcleos; serviços subjacentes do recorte do BC (inflc_decomposicao) até agosto."""
from pathlib import Path

import numpy as np
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"
ia = pd.read_csv(A / "inflc_agregados.csv.gz", parse_dates=["date"])
acc = lambda x: 100 * (np.prod(1 + x / 100) - 1)
nomes = ["ipca", "ipca_livres", "ipca_administrado", "ipca_servicos", "ipca_alimentacao", "ipca_industriais",
         "ipca_nucleo_ex0", "ipca_nucleo_ex03", "ipca_nucleo_medias_aparadas", "ipca_nucleo_p55",
         "ipca_nucleo_dp", "ipca_nucleo_exfe"]
nuc = []
for nm in nomes:
    s = ia[ia.name == nm].set_index("date")["value"].sort_index()
    a = s[:"2026-08-01"]
    v12, v12_3 = acc(a.iloc[-12:]), acc(a.iloc[-15:-3])
    v3 = acc(a.iloc[-3:])
    print(f"{nm:32s} ago {a.iloc[-1]:+.2f} | 3m {v3:.2f} | 12m até ago {v12:.2f} | 12m até mai {v12_3:.2f}")
    if "nucleo" in nm:
        nuc.append(v12)
print("média dos 6 núcleos, 12m até ago:", round(float(np.mean(nuc)), 2))
dif = ia[ia.name == "ipca_indice_difusao"].set_index("date")["value"]
print("difusão ago:", dif.get(pd.Timestamp("2026-08-01")), " média 12m até ago:", round(dif[:"2026-08-01"].iloc[-12:].mean(), 1))
i15 = ia[ia.name == "ipca15"].set_index("date")["value"].sort_index()
print("IPCA-15 set:", i15.iloc[-1], " 12m:", round(acc(i15.iloc[-12:]), 2))

dc = pd.read_csv(A / "inflc_decomposicao.csv.gz", parse_dates=["date"])
print(dc.columns.tolist()); print(dc.name.unique() if "name" in dc else dc.iloc[:, 1].unique()[:20])
