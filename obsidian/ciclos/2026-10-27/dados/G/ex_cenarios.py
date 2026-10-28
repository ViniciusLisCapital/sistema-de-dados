"""G externo: monta os caminhos trimestrais das sete exógenas em cada cenário de cada bloco, na convenção
do modelo, a partir de caminhos MENSAIS (Brent, núcleo e alimentos do CPI, grupos do IC-Br), e roda o
Modelo Estrutural por cenário. Coeficientes de ligação medidos em ex_commodities.py e ex_eua_politica.py:
  - CPI energia mensal (Δlog) = 0,188 + 0,140·ΔBrent + 0,090·ΔBrent(-1)          (2010-2026)
  - CPI cheio tri = 0,002 + 0,756·núcleo + 0,079·energia + 0,157·alimentos        (2010-2026)
  - IC-Br energia (Δlog) = 0,481·ΔBrent médio mensal                              (2010-2026)
  - IC-Br total (Δlog) = 0,029 + 0,633·agro + 0,171·metal + 0,192·energia         (2022-2026)
Lê só ../A/ e o retrato do modelo."""
import json, sys
import numpy as np, pandas as pd
from pathlib import Path
from analytics.agent_system import modelo
A = Path(__file__).resolve().parent.parent / "A"
TRIS = ["4T26","1T27","2T27","3T27","4T27","1T28"]
MESES = pd.date_range("2026-10-01", "2028-03-01", freq="MS")  # 18 meses

br = pd.read_csv(A/"comm_brent.csv.gz", parse_dates=["date"]).set_index("date")["value"]
br_out_obs = br.loc["2026-10-01":]; n_obs = len(br_out_obs); out_obs = br_out_obs.mean()
dias_out = 22  # pregões de outubro (aprox.); os restantes vão ao nível do cenário
br_set = br.loc["2026-09"].mean()
cpi = pd.read_csv(A/"inflc_cpi.csv.gz", parse_dates=["date"]).pivot(index="date", columns="item_code", values="value")
ic = pd.read_csv(A/"comm_icbr_usd.csv.gz", parse_dates=["date"]).pivot(index="date", columns="name", values="value")
agr0, met0, ene0, tot0 = ic.loc["2026-09-01", ["icbr_agropecuaria_usd","icbr_metal_usd","icbr_energia_usd","icbr_usd"]]

def tri(m):  # índice mensal -> rótulo do trimestre
    return [f"{(d.month-1)//3+1}T{str(d.year)[2:]}" for d in m]

def expand(q6):  # 6 valores trimestrais -> 18 mensais
    return np.repeat(np.asarray(q6, float), 3)

# ---------- Brent mensal por cenário de commodities (out = observado até 20/10 + resto do mês no nível do cenário)
BRENT = {
  "base": [115, 112, 110, 107, 105, 103, 101, 99, 98, 97, 96, 95, 94, 93, 92, 92, 91, 90],
  "up":   [125, 130, 132, 132, 130, 128, 126, 124, 122, 120, 118, 116, 115, 113, 112, 110, 110, 110],
  "down": [112, 100, 92, 87, 84, 82, 80, 79, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78],
}
def brent_mensal(c):
    v = np.array(BRENT[c], float)
    v[0] = (out_obs*n_obs + v[0]*(dias_out-n_obs))/dias_out
    return pd.Series(v, index=MESES)

# ---------- bloco Política dos EUA: núcleo e alimentos do CPI (% ao mês) e Fed (efetivo, média do último mês)
CORE = {"base": [0.27,0.26,0.25,0.25,0.24,0.24], "up": [0.33,0.32,0.30,0.28,0.27,0.26], "down": [0.22,0.20,0.20,0.20,0.20,0.20]}
FOOD = {"base": [0.20]*6, "up": [0.30]*6, "down": [0.15]*6}
FFR  = {"base": [4.13,4.13,4.13,4.13,4.13,3.88], "up": [4.38,4.63,4.63,4.63,4.63,4.63], "down": [3.88,3.63,3.38,3.13,3.13,3.13]}
BRENT_DO_BLOCO_EUA = {"base":"base", "up":"up", "down":"down"}  # a história de cada cenário do Fed é a do petróleo

def infl_us(c):
    b = brent_mensal(BRENT_DO_BLOCO_EUA[c])
    bm = pd.concat([br.resample("MS").mean().loc[:"2026-09-01"], b])
    dl = 100*np.log(bm).diff()
    ene = 0.188 + 0.140*dl + 0.090*dl.shift(1)
    ene = ene.loc[MESES]
    core = pd.Series(expand(CORE[c]), index=MESES); food = pd.Series(expand(FOOD[c]), index=MESES)
    g = pd.DataFrame({"core":core,"ene":ene,"food":food}); g["tri"] = tri(MESES)
    q = g.groupby("tri", sort=False).sum()
    q["cheio"] = 0.002 + 0.756*q.core + 0.079*q.ene + 0.157*q.food
    return q

# ---------- bloco Commodities: grupos mensais
MET = {"base": [333,332,330,330,330,330,330,330,330,329,329,328,328,327,327,326,326,325],
       "up":   [340,346,352,356,358,360,362,362,362,362,362,362,362,362,362,362,362,362],
       "down": [328,320,312,305,298,292,287,283,280,278,277,276,275,275,275,275,275,275]}
AGR = {"base": [202]*18,
       "up":   [203,205,207,209,211,212,213,214,215,215,215,215,215,215,215,215,215,215],
       "down": [200,198,196,194,192,190,189,188,187,186,186,185,185,185,185,185,185,185]}
def commodities(c):
    b = brent_mensal(c)
    ene = ene0*np.exp(0.481*np.log(b/br_set))
    agr = pd.Series(AGR[c], index=MESES, dtype=float); met = pd.Series(MET[c], index=MESES, dtype=float)
    lag = lambda s, s0: np.log(pd.concat([pd.Series([s0]), s.reset_index(drop=True)])).diff().iloc[1:].values*100
    dtot = 0.029 + 0.633*lag(agr,agr0) + 0.171*lag(met,met0) + 0.192*lag(ene,ene0)
    tot = pd.Series(tot0*np.exp(np.cumsum(dtot)/100), index=MESES)
    d = pd.DataFrame({"agr":agr,"met":met,"ene":ene,"tot":tot,"brent":b}); d["tri"] = tri(MESES)
    g = d.groupby("tri", sort=False)
    return pd.DataFrame({"icbr_agr_usd":g.agr.mean(),"icbr_met_usd":g.met.mean(),"icbr_usd":g.tot.last(),
                         "energia_media":g.ene.mean(),"brent_media":g.brent.mean()})

# ---------- bloco Risco e dólar: fechamentos
DXY_EM = {"base": [130.5,131.0,130.5,130.0,129.5,129.0], "up": [133.5,136.5,135.5,134.5,133.5,132.5], "down": [128.5,127.0,126.0,125.0,124.5,124.0]}
SP500  = {"base": [7750,7900,8050,8200,8350,8500], "up": [7000,6500,6700,6950,7200,7450], "down": [7950,8300,8650,8950,9200,9450]}

def caminhos(eua="base", risco="base", comm="base"):
    q = infl_us(eua); c = commodities(comm)
    return {"ffr": dict(zip(TRIS, FFR[eua])), "infl_us": {t: round(float(q.loc[t,"cheio"]),2) for t in TRIS},
            "dxy_em": dict(zip(TRIS, DXY_EM[risco])), "sp500": dict(zip(TRIS, SP500[risco])),
            "icbr_usd": {t: round(float(c.loc[t,"icbr_usd"]),1) for t in TRIS},
            "icbr_agr_usd": {t: round(float(c.loc[t,"icbr_agr_usd"]),1) for t in TRIS},
            "icbr_met_usd": {t: round(float(c.loc[t,"icbr_met_usd"]),1) for t in TRIS}}

if __name__ == "__main__":
    print(f"Brent out/26 observado: média {out_obs:.2f} em {n_obs} pregões; set/26 média {br_set:.2f}")
    for c in ["base","up","down"]:
        q = infl_us(c); print(f"\n== EUA {c}: CPI por trimestre (núcleo, energia, alimentos, cheio)"); print(q.round(2).to_string())
        print(f"== Commodities {c}"); print(commodities(c).round(1).to_string())
    sim = modelo.carregar("2026-10-27")
    cen = {"base": caminhos(),
           "EUA up (Fed mais alto)": caminhos(eua="up"), "EUA down (Fed devolve)": caminhos(eua="down"),
           "Risco up (risk-off)": caminhos(risco="up"), "Risco down (risk-on)": caminhos(risco="down"),
           "Commodities up": caminhos(comm="up"), "Commodities down": caminhos(comm="down"),
           "Conjunto adverso (EUA up, risk-off, commodities down)": caminhos("up","up","down"),
           "Conjunto choque de petróleo (EUA up, risk-off, commodities up)": caminhos("up","up","up"),
           "Conjunto favorável (EUA down, risk-on, commodities base)": caminhos("down","down","base")}
    json.dump(cen, open(Path(__file__).with_name("ex_cenarios_caminhos.json"),"w"), indent=1, ensure_ascii=False)
    for nome, cam in cen.items():
        print(f"\n######## {nome}")
        for k, v in cam.items(): print(f"  {k}: " + " ".join(f"{t}={v[t]}" for t in TRIS))
        res = modelo.rodar(sim, caminhos=cam)
        txt = modelo.texto(res, TRIS)
        for ln in txt.splitlines():
            if ln.startswith("| PTAX") or ln.startswith("| Selic, média") or ln.startswith("| IPCA acumulado") or ln.startswith("| IPCA 12m: contribuição de alim") or ln.startswith("| IPCA 12m: contribuição de bens") or ln.startswith("| Hiato") or ln.startswith("| |"):
                print(ln)
