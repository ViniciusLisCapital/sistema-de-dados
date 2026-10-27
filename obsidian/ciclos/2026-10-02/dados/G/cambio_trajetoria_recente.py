"""G do câmbio, ciclo 2026-10-02: a trajetória recente do real, dos pares, dos índices de dólar,
do Brent e do CDS, em pontos de referência (fim de jun, jul, ago, set e 02/10), e a variação
de cada um nas janelas que a seção Q3 usa. Lê só ../A/."""
from pathlib import Path
import numpy as np
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"


def serie(tab, filtro_col=None, filtro_val=None):
    d = pd.read_csv(A / f"{tab}.csv.gz")
    if filtro_col:
        d = d[d[filtro_col] == filtro_val]
    s = d.set_index(pd.to_datetime(d["date"]))["value"].astype(float).sort_index()
    return s


S = {
    "BRL (PTAX)": serie("cmb_ptax", "name", "ptax_venda"),
    "MXN": serie("cmb_fx_latam", "country_code", "MX"),
    # CLP e COP: a taxa datada em t é a formada em t-1 (Atenção do F). Desloca um dia útil.
    "CLP": serie("cmb_fx_latam", "country_code", "CL").shift(-1).dropna(),
    "COP": serie("cmb_fx_latam", "country_code", "CO").shift(-1).dropna(),
    "PEN": serie("cmb_fx_latam", "country_code", "PE"),
    "DXY": serie("cmb_dollar_index", "name", "dxy"),
    "dxy_em": serie("cmb_dollar_index_em", "name", "dxy_em"),
    "Brent": serie("comm_brent", "name", "brent_usd"),
    "CDS 5a": serie("cmb_risco_pais", "name", "cds_5y_usd"),
    "S&P 500": serie("cmb_equity_us", "name", "sp500"),
}

datas = ["2026-06-30", "2026-07-31", "2026-08-31", "2026-09-01", "2026-09-15", "2026-09-30", "2026-10-01", "2026-10-02"]
tab = {}
for k, s in S.items():
    tab[k] = [s[:d].iloc[-1] if len(s[:d]) else np.nan for d in datas]
print("Níveis (último dado até cada data):")
print(pd.DataFrame(tab, index=datas).T.round(4).to_string())

# variação em % (log não: % simples, como o F) contra cada referência; CDS em p.b.
print("\nVariação até 02/10 (%; CDS em p.b.):")
ref = {"desde 30/06": "2026-06-30", "desde 31/08": "2026-08-31", "desde 30/09": "2026-09-30"}
out = {}
for k, s in S.items():
    ult = s[:"2026-10-02"].iloc[-1]
    linha = {}
    for nome, d in ref.items():
        base = s[:d].iloc[-1]
        linha[nome] = (ult - base) if k == "CDS 5a" else 100 * (ult / base - 1)
    out[k] = linha
o = pd.DataFrame(out).T
print(o.round(2).to_string())
peers = ["MXN", "CLP", "COP", "PEN"]
print("\nMédia simples dos 4 pares:")
print(o.loc[peers].mean().round(2).to_string())
print("\nBRL menos média dos pares (p.p.):")
print((o.loc["BRL (PTAX)"] - o.loc[peers].mean()).round(2).to_string())

print("\nBrent, últimos 15 pregões:")
print(S["Brent"]["2026-09-10":].to_string())
print("\nPTAX, desde 15/09:")
print(S["BRL (PTAX)"]["2026-09-15":].to_string())
print("\nMXN, desde 25/08 (de 5 em 5):")
print(S["MXN"]["2026-08-25":].iloc[::3].to_string())
print("\nBrent média de set e média de out até 02/10:")
b = S["Brent"]
print(round(b["2026-09"].mean(), 2), round(b["2026-10"].mean(), 2), round(b["2026-08"].mean(), 2), round(b["2026-06"].mean(), 2))

# a PTAX nos últimos três meses: mínimo, máximo, média, e o valor de 02/09 (base do Δ 1m do F)
pt = S["BRL (PTAX)"]["2026-07-01":"2026-10-02"]
print("\nPTAX 01/07-02/10: mín", pt.min(), pt.idxmin().date(), "· máx", pt.max(), pt.idxmax().date(), "· média", round(pt.mean(), 4))
print("PTAX 02/09:", S["BRL (PTAX)"][:"2026-09-02"].iloc[-1], "· 03/09:", S["BRL (PTAX)"][:"2026-09-03"].iloc[-1])
