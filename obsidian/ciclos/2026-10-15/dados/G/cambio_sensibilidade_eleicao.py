"""G · câmbio · ciclo 2026-10-15: a sensibilidade do real ao CDS na janela do 1º turno,
contra a que o Modelo Estrutural estimou.

Janela: 02/10 (última sessão antes do 1º turno) → 06/10 e → 14/10. Compara a variação
da PTAX (em log, %) com o que a equação do câmbio daria, pelos pesos da mediana, para a
variação do CDS e do dólar contra emergentes na mesma janela. É uma conta de ordem de
grandeza: a equação é trimestral e a janela é de dias.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
A = Path(__file__).resolve().parents[1] / "A"


def serie(tab, nome=None):
    df = pd.read_csv(A / f"{tab}.csv.gz", parse_dates=["date"])
    if nome is not None:
        df = df[df["name"] == nome]
    return df.set_index("date")["value"].sort_index()


ptax_df = pd.read_csv(A / "cmb_ptax.csv.gz", parse_dates=["date"])
print("cmb_ptax colunas:", ptax_df.columns.tolist(), ptax_df["name"].unique()[:10] if "name" in ptax_df else "")
ptax = ptax_df[ptax_df["name"].str.contains("venda", case=False)] if "name" in ptax_df else ptax_df
ptax = ptax.set_index("date")["value"].sort_index()
cds = serie("cmb_risco_pais")
dem = serie("cmb_dollar_index_em")

p = json.loads((A / "modelo_estrutural.json").read_text(encoding="utf-8"))["p"]
F = p["eq"]["F"]
por_pb = F["mediana"]["b_fiscal"] / F["sd"]["fiscal"]          # % de PTAX por p.b. de CDS
por_dem = F["mediana"]["b_dxy_em"] / F["sd"]["dxy_em"]         # % de PTAX por ponto do índice
print(f"modelo: {por_pb:.4f}% de PTAX por p.b. de CDS; {por_dem:.4f}% por ponto do dólar EM")
print()

ini = pd.Timestamp("2026-10-02")
for fim in ("2026-10-06", "2026-10-14"):
    fim = pd.Timestamp(fim)
    d_ptax = 100 * np.log(ptax.asof(fim) / ptax.asof(ini))
    d_cds = cds.asof(fim) - cds.asof(ini)
    d_dem = dem.asof(fim) - dem.asof(ini)
    mod = por_pb * d_cds + por_dem * d_dem
    print(f"{ini.date()} → {fim.date()}: PTAX {ptax.asof(ini):.4f} → {ptax.asof(fim):.4f} "
          f"({d_ptax:+.2f}% em log); CDS {cds.asof(ini):.2f} → {cds.asof(fim):.2f} ({d_cds:+.2f} p.b.); "
          f"dólar EM {dem.asof(ini):.4f} → {dem.asof(fim):.4f} ({d_dem:+.4f}, até {dem.index[dem.index <= fim][-1].date()})")
    print(f"   modelo daria {mod:+.2f}% (CDS {por_pb * d_cds:+.2f}, dólar EM {por_dem * d_dem:+.2f}); "
          f"observado / modelo = {d_ptax / mod:.2f}; "
          f"sensibilidade implícita ao CDS, descontado o dólar EM: "
          f"{(d_ptax - por_dem * d_dem) / d_cds:.4f}%/p.b. = {((d_ptax - por_dem * d_dem) / d_cds) / por_pb:.2f}× o modelo")
print()
spot = ptax.iloc[-1]
print(f"PTAX última: {spot:.4f} em {ptax.index[-1].date()}; fechamento 3T26: {ptax.asof(pd.Timestamp('2026-09-30')):.4f}; "
      f"variação: {100 * (spot / ptax.asof(pd.Timestamp('2026-09-30')) - 1):+.2f}%")
