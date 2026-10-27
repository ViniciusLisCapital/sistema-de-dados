"""G do externo, ciclo 2026-10-02, rodada 1: os caminhos dos três blocos e o que o modelo faz com eles.

Monta, mês a mês, os caminhos de Brent, núcleo do CPI e grupos do IC-Br de cada cenário, passa
para a convenção do modelo (modelo.CONVENCAO) e roda o Modelo Estrutural.

Relações usadas, todas medidas em ex_relacoes.py (janelas lá):
- CPI cheio mensal = 0,029 + 0,877·núcleo + 0,0093·ΔlogBrent + 0,0049·ΔlogBrent(-1)  (2015–ago/26)
- Δlog IC-Br energia = 0,464·ΔlogBrent + 0,067·ΔlogBrent(-1)                         (2010–ago/26)
- Δlog IC-Br = 0,663·Δagr + 0,185·Δmet + 0,173·Δene                                   (2023–ago/26)
Ponto de partida: o último mês que existia em 02/10 (CPI e IC-Br de ago); o mês de set é
projetado e comparado com o publicado depois do corte.
Lê só ../A/ e o retrato do modelo.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from analytics.agent_system import modelo

A = Path(__file__).resolve().parent.parent / "A"
CICLO = "2026-10-02"
TRI = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
MESES = pd.date_range("2026-09-01", "2028-03-01", freq="MS")  # set/26 a mar/28

def rd(t):
    d = pd.read_csv(A / f"{t}.csv.gz"); d["date"] = pd.to_datetime(d["date"]); return d

cpi = rd("inflc_cpi").pivot_table(index="date", columns="item_code", values="value")
ic = rd("comm_icbr_usd").pivot_table(index="date", columns="name", values="value")
br = rd("comm_brent").set_index("date")["value"]
brm = br.resample("MS").mean()

def mensal(trim_vals):
    """Valores trimestrais (média) -> mensais constantes dentro do trimestre, de out/26 a mar/28."""
    out = {}
    for i, q in enumerate(TRI):
        for k in range(3):
            out[pd.Timestamp("2026-10-01") + pd.DateOffset(months=3 * i + k)] = trim_vals[i]
    return out

# ---------------- cenários: Brent (US$/barril, média do mês), núcleo (%/mês), agro e metal (%/mês)
BRENT = {
    "base":     [128, 125, 120, 115, 110, 105, 102, 100, 98, 96, 95, 94, 92, 92, 92, 90, 90, 90],
    "upside":   [140, 145, 145, 140, 138, 135, 130, 130, 130, 122, 122, 122, 115, 115, 115, 110, 110, 110],
    "downside": [120, 100, 90, 85, 85, 85, 80, 80, 80, 80, 80, 80, 78, 78, 78, 78, 78, 78],
}
NUCLEO = {  # 100·Δlog mensal do núcleo, por trimestre
    "base": [0.25, 0.25, 0.23, 0.22, 0.22, 0.22],
    "upside": [0.30, 0.32, 0.30, 0.28, 0.26, 0.25],
    "downside": [0.20, 0.18, 0.18, 0.18, 0.18, 0.18],
}
AGR = {"base": -0.1, "upside": 0.5, "downside": -0.7}     # % ao mês a partir de set/26
MET = {"base": -0.2, "upside": 1.0, "downside": -1.5}

def caminhos_cmd(cen):
    meses_proj = pd.date_range("2026-10-01", periods=18, freq="MS")
    b = pd.Series(BRENT[cen], index=meses_proj)
    b = pd.concat([brm[:"2026-09-01"], b])
    dlb = 100 * np.log(b).diff()
    # energia: parte de ago (último publicado em 02/10), projeta set em diante
    ene = {pd.Timestamp("2026-08-01"): ic.loc["2026-08-01", "icbr_energia_usd"]}
    agr = {pd.Timestamp("2026-08-01"): ic.loc["2026-08-01", "icbr_agropecuaria_usd"]}
    met = {pd.Timestamp("2026-08-01"): ic.loc["2026-08-01", "icbr_metal_usd"]}
    tot = {pd.Timestamp("2026-08-01"): ic.loc["2026-08-01", "icbr_usd"]}
    prev = pd.Timestamp("2026-08-01")
    for t in pd.date_range("2026-09-01", "2028-03-01", freq="MS"):
        d_ene = 0.464 * dlb[t] + 0.067 * dlb[prev]
        if t == pd.Timestamp("2026-09-01"):
            d_agr, d_met = 0.0, 0.0  # set: sem informação dos grupos em 02/10 além do Brent
        else:
            d_agr, d_met = AGR[cen], MET[cen]
        ene[t] = ene[prev] * np.exp(d_ene / 100)
        agr[t] = agr[prev] * np.exp(d_agr / 100)
        met[t] = met[prev] * np.exp(d_met / 100)
        tot[t] = tot[prev] * np.exp((0.663 * d_agr + 0.185 * d_met + 0.173 * d_ene) / 100)
        prev = t
    df = pd.DataFrame({"brent": b, "ene": pd.Series(ene), "agr": pd.Series(agr),
                       "met": pd.Series(met), "tot": pd.Series(tot)}).loc["2026-08-01":]
    return df, dlb

def infl_us(cen, dlb):
    # CPI cheio: parte do publicado em ago (existia em 02/10); set projetado
    nuc = {}
    nuc[pd.Timestamp("2026-09-01")] = 0.25
    nuc.update(mensal(NUCLEO[cen]))
    m = {}
    for t, n in nuc.items():
        m[t] = 0.029 + 0.877 * n + 0.0093 * dlb[t] + 0.0049 * dlb[t - pd.DateOffset(months=1)]
    m = pd.Series(m).sort_index()
    q = {}
    for i, tq in enumerate(TRI):
        ini = pd.Timestamp("2026-10-01") + pd.DateOffset(months=3 * i)
        q[tq] = m[ini: ini + pd.DateOffset(months=2)].sum()
    q3 = 100 * np.log(cpi.loc["2026-08-01", "SA0"] / cpi.loc["2026-06-01", "SA0"]) + m[pd.Timestamp("2026-09-01")]
    return q, m, q3

def trimestral(df):
    out = {"icbr_usd": {}, "icbr_agr_usd": {}, "icbr_met_usd": {}, "brent_media": {}, "ene_media": {}}
    for i, tq in enumerate(TRI):
        ini = pd.Timestamp("2026-10-01") + pd.DateOffset(months=3 * i)
        fim = ini + pd.DateOffset(months=2)
        out["icbr_usd"][tq] = df.loc[fim, "tot"]
        out["icbr_agr_usd"][tq] = df.loc[ini:fim, "agr"].mean()
        out["icbr_met_usd"][tq] = df.loc[ini:fim, "met"].mean()
        out["brent_media"][tq] = df.loc[ini:fim, "brent"].mean()
        out["ene_media"][tq] = df.loc[ini:fim, "ene"].mean()
    return out

FFR = {
    "base":     [4.13, 4.13, 4.13, 4.13, 3.88, 3.88],
    "upside":   [4.38, 4.63, 4.88, 4.88, 4.88, 4.63],
    "downside": [3.88, 3.63, 3.38, 3.13, 3.13, 3.13],
}
DXY_EM = {
    "base":     [130.0, 130.0, 129.5, 129.0, 128.5, 128.5],
    "riskoff":  [134.5, 135.0, 134.0, 133.0, 132.0, 131.0],
    "riskon":   [127.0, 126.0, 125.5, 125.0, 124.5, 124.5],
}
SP500 = {
    "base":     [7700, 7800, 7900, 8000, 8100, 8200],
    "riskoff":  [6900, 6800, 7000, 7200, 7400, 7600],
    "riskon":   [8050, 8250, 8400, 8550, 8700, 8850],
}

def d(lst):
    return {q: round(float(v), 3) for q, v in zip(TRI, lst)}

caminhos = {}
print("=== Commodities e inflação americana por cenário")
for cen in ["base", "upside", "downside"]:
    df, dlb = caminhos_cmd(cen)
    t = trimestral(df)
    q, m, q3 = infl_us(cen, dlb)
    caminhos[cen] = {"infl_us": {k: round(v, 3) for k, v in q.items()},
                     "icbr_usd": {k: round(v, 2) for k, v in t["icbr_usd"].items()},
                     "icbr_agr_usd": {k: round(v, 2) for k, v in t["icbr_agr_usd"].items()},
                     "icbr_met_usd": {k: round(v, 2) for k, v in t["icbr_met_usd"].items()}}
    print(f"\n[{cen}]")
    print(pd.DataFrame({**{k: v for k, v in caminhos[cen].items()},
                        "brent_media": t["brent_media"], "ene_media": t["ene_media"]}).T.round(2))
    if cen == "base":
        print("set/26 projetado em 02/10 -> publicado depois do corte:")
        print("  energia", round(df.loc["2026-09-01", "ene"], 2), "->", ic.loc["2026-09-01", "icbr_energia_usd"],
              "| total", round(df.loc["2026-09-01", "tot"], 2), "->", ic.loc["2026-09-01", "icbr_usd"])
        print("  CPI cheio set 100·Δlog projetado", round(m[pd.Timestamp('2026-09-01')], 2), "-> publicado",
              round(100 * np.log(cpi.loc['2026-09-01', 'SA0'] / cpi.loc['2026-08-01', 'SA0']), 2),
              "| infl_us 3T26 projetado", round(q3, 2), "-> publicado 1,12")
        # 12m do CPI na base, fim de cada trimestre
        lv = cpi["SA0"].dropna()
        nivel = {pd.Timestamp("2026-08-01"): lv["2026-08-01"]}
        prev = pd.Timestamp("2026-08-01")
        for tt in m.index:
            nivel[tt] = nivel[prev] * np.exp(m[tt] / 100); prev = tt
        nv = pd.Series(nivel)
        allv = pd.concat([lv[:"2026-08-01"], nv.iloc[1:]])
        print("  CPI 12m na base (dez/26, jun/27, dez/27):",
              [round(100 * (allv[x] / allv[pd.Timestamp(x) - pd.DateOffset(years=1)] - 1), 2)
               for x in ["2026-12-01", "2027-06-01", "2027-12-01"]])

for k, v in FFR.items():
    caminhos.setdefault(k, {})["ffr"] = d(v)
for k, v in DXY_EM.items():
    caminhos.setdefault(k, {})["dxy_em"] = d(v)
for k, v in SP500.items():
    caminhos.setdefault(k, {})["sp500"] = d(v)

BLOCOS = {
    "politica": (["ffr", "infl_us"], "upside", "downside"),
    "risco": (["dxy_em", "sp500"], "riskoff", "riskon"),
    "commodities": (["icbr_usd", "icbr_agr_usd", "icbr_met_usd"], "upside", "downside"),
}
VARS = ["ffr", "infl_us", "dxy_em", "sp500", "icbr_usd", "icbr_agr_usd", "icbr_met_usd"]
base = {v: caminhos["base"][v] for v in VARS}
print("\n=== Caminhos base (JSON):")
print(base)
for cen in ["upside", "downside", "riskoff", "riskon"]:
    print(cen, {v: caminhos[cen][v] for v in caminhos[cen]})

sim = modelo.carregar(CICLO)

def resumo(res, rot):
    print(f"\n##### {rot}")
    print(modelo.texto(res))

rodadas = {"base": base}
for bloco, (vs, up, dn) in BLOCOS.items():
    for cen in (up, dn):
        c = dict(base); c.update({v: caminhos[cen][v] for v in vs})
        rodadas[f"{bloco}:{cen}"] = c
# combinado de estresse: Fed para cima, risk-off e petróleo para cima (commodities upside)
c = dict(base)
c.update({v: caminhos["upside"][v] for v in ["ffr", "infl_us", "icbr_usd", "icbr_agr_usd", "icbr_met_usd"]})
c.update({v: caminhos["riskoff"][v] for v in ["dxy_em", "sp500"]})
rodadas["combinado:estresse"] = c
# sp500 sozinho em queda (para mostrar o sinal condicional, mapa 2.5)
c = dict(base); c["sp500"] = caminhos["riskoff"]["sp500"]
rodadas["teste:sp500_sozinho"] = c

for rot, cam in rodadas.items():
    res = modelo.rodar(sim, caminhos=cam)
    resumo(res, rot)
