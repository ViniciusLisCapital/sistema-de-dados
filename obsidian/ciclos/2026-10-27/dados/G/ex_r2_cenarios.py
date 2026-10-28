"""G externo, rodada 2: os caminhos das sete exógenas por cenário e as rodadas do modelo.
Muda contra a r1 (ex_cenarios.py, que segue valendo para o Brent, o CPI, o Fed, o dólar EM, o S&P e os metais):
  - o agro sai do Brent e do dólar EM pela ligação mensal medida em ex_r2_agro_brent.py (2016-2026, defasagens
    0 a 6 do Brent e o dólar EM corrente, sem a constante), mais um componente próprio do cenário (alta: +4% em
    rampa até o 3T27; queda: −3%); o total do IC-Br sai dos grupos como na r1;
  - as exógenas que não escrevo vêm do P1 (meta, rr_10a e CDS do principal; vol do câmbio), não do padrão.
Também: o cenário de risco com o CDS do fiscal acrescido do componente global (diferença contra o base, pela
regressão 2016-2026 da r1), e o efeito no modelo de pôr no dólar EM o salto mecânico do real (+0,47%).
Lê só ../A/, o retrato do modelo e ../../P1.json."""
import json, sys
import numpy as np, pandas as pd
from pathlib import Path
from analytics.agent_system import modelo
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ex_cenarios as C
A = C.A; T = C.TRIS; MESES = C.MESES
P1 = json.loads((Path(__file__).resolve().parents[2]/"P1.json").read_text(encoding="utf-8"))
OUTROS = {k: {t: P1["caminhos_usados"][k][t] for t in T} for k in ["meta_12m", "rr_10a", "fiscal", "vol"]}

# ---- ligação agro <- Brent (0..6) + dólar EM, 2016-2026, mensal
ic = pd.read_csv(A/"comm_icbr_usd.csv.gz", parse_dates=["date"]).pivot(index="date", columns="name", values="value")
brm = pd.read_csv(A/"comm_brent.csv.gz", parse_dates=["date"]).set_index("date")["value"].resample("MS").mean()
emm = pd.read_csv(A/"cmb_dollar_index_em.csv.gz", parse_dates=["date"]).set_index("date")["value"].resample("MS").mean()
d = pd.DataFrame({"agr": ic["icbr_agropecuaria_usd"], "br": brm, "em": emm}).dropna()
r = 100*np.log(d).diff()
for k in range(7): r[f"br{k}"] = r.br.shift(k)
x = r.dropna().loc["2016-01-01":]; cols = [f"br{k}" for k in range(7)] + ["em"]
Xr = np.c_[np.ones(len(x)), x[cols].values]; bA, *_ = np.linalg.lstsq(Xr, x.agr.values, rcond=None)
BK, BEM = bA[1:8], bA[8]
print(f"agro: constante {bA[0]:.3f} (fora), Brent 0..6 = {np.round(BK,3)}, soma {BK.sum():.3f}; dólar EM {BEM:.3f}")
EXTRA = {"base": np.zeros(18), "up": np.minimum(np.arange(1, 19)/12, 1)*4.0, "down": -np.minimum(np.arange(1, 19)/12, 1)*3.0}

def em_mensal(q6):  # fechamentos trimestrais -> média mensal aproximada (interpolação linear entre fechamentos)
    pts = pd.Series([129.38] + list(q6), index=pd.to_datetime(["2026-09-30", "2026-12-31", "2027-03-31", "2027-06-30", "2027-09-30", "2027-12-31", "2028-03-31"]))
    dia = pts.resample("D").interpolate()
    return dia.resample("MS").mean().loc[MESES]

def agro(comm, risco="base"):
    b = C.brent_mensal(comm)
    bh = pd.concat([brm.loc["2026-01-01":"2026-09-01"], b])
    dlb = 100*np.log(bh).diff()
    e = em_mensal(C.DXY_EM[risco]); eh = pd.concat([emm.loc[["2026-09-01"]], e]); dle = 100*np.log(eh).diff().loc[MESES]
    lv = [ic.loc["2026-09-01", "icbr_agropecuaria_usd"]]
    for i, m in enumerate(MESES):
        pos = bh.index.get_loc(m)
        dl = sum(BK[k]*dlb.iloc[pos-k] for k in range(7)) + BEM*dle.loc[m]
        lv.append(lv[-1]*np.exp(dl/100))
    s = pd.Series(lv[1:], index=MESES)*np.exp(EXTRA[comm]/100)
    return s

def commodities(comm, risco="base"):
    b = C.brent_mensal(comm)
    ene = C.ene0*np.exp(0.481*np.log(b/C.br_set))
    agr = agro(comm, risco); met = pd.Series(C.MET[comm], index=MESES, dtype=float)
    lag = lambda s, s0: np.log(pd.concat([pd.Series([s0]), s.reset_index(drop=True)])).diff().iloc[1:].values*100
    dtot = 0.029 + 0.633*lag(agr, C.agr0) + 0.171*lag(met, C.met0) + 0.192*lag(ene, C.ene0)
    tot = pd.Series(C.tot0*np.exp(np.cumsum(dtot)/100), index=MESES)
    dd = pd.DataFrame({"agr": agr, "met": met, "ene": ene, "tot": tot, "brent": b}); dd["tri"] = C.tri(MESES)
    g = dd.groupby("tri", sort=False)
    return pd.DataFrame({"icbr_agr_usd": g.agr.mean(), "icbr_met_usd": g.met.mean(), "icbr_usd": g.tot.last(),
                         "energia_media": g.ene.mean(), "brent_media": g.brent.mean(), "agro_ultimo_mes": g.agr.last(), "total_out": g.tot.first()})

def caminhos(eua="base", risco="base", comm="base"):
    q = C.infl_us(eua); c = commodities(comm, risco)
    return {"ffr": dict(zip(T, C.FFR[eua])), "infl_us": {t: round(float(q.loc[t, "cheio"]), 2) for t in T},
            "dxy_em": dict(zip(T, C.DXY_EM[risco])), "sp500": dict(zip(T, C.SP500[risco])),
            "icbr_usd": {t: round(float(c.loc[t, "icbr_usd"]), 1) for t in T},
            "icbr_agr_usd": {t: round(float(c.loc[t, "icbr_agr_usd"]), 1) for t in T},
            "icbr_met_usd": {t: round(float(c.loc[t, "icbr_met_usd"]), 1) for t in T}}

def linha(res, chave):
    ln = [l for l in modelo.texto(res, T).splitlines() if l.startswith(chave)][0]
    return " ".join(cel.split(" [")[0].strip() for cel in ln.split("|")[3:9])

cds_b = [-9.58, 12.42, -0.674]
def cds_global(cam, ref):  # CDS do fiscal + (componente global do cenário − o do base), sem a constante
    out = {}
    for t in T:
        g = cds_b[1]*100*np.log(cam["dxy_em"][t]/129.38) + cds_b[2]*100*np.log(cam["sp500"][t]/7651.54)
        g0 = cds_b[1]*100*np.log(ref["dxy_em"][t]/129.38) + cds_b[2]*100*np.log(ref["sp500"][t]/7651.54)
        out[t] = round(OUTROS["fiscal"][t] + g - g0, 1)
    return out

if __name__ == "__main__":
    for c in ["base", "up", "down"]:
        print(f"\n== Commodities {c} (r2)"); print(commodities(c).round(1).to_string())
    sim = modelo.carregar("2026-10-27")
    base = caminhos()
    cen = {"base": base,
           "EUA up": caminhos(eua="up"), "EUA down": caminhos(eua="down"),
           "risk-off, CDS do fiscal": caminhos(risco="up"), "risk-on, CDS do fiscal": caminhos(risco="down"),
           "commodities alta": caminhos(comm="up"), "commodities queda": caminhos(comm="down"),
           "conjunto adverso (EUA up, risk-off, queda)": caminhos("up", "up", "down"),
           "conjunto petróleo (EUA up, risk-off, alta)": caminhos("up", "up", "up")}
    ro = dict(cen["risk-off, CDS do fiscal"]); ro["fiscal"] = cds_global(ro, base); cen["risk-off, CDS + componente global"] = ro
    rn = dict(cen["risk-on, CDS do fiscal"]); rn["fiscal"] = cds_global(rn, base); cen["risk-on, CDS + componente global"] = rn
    bm = dict(base); bm["dxy_em"] = {t: round(v*1.0047, 2) for t, v in base["dxy_em"].items()}; cen["base com o salto mecânico do real no dólar EM"] = bm
    json.dump(cen, open(Path(__file__).with_name("ex_r2_cenarios_caminhos.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("\nCDS + componente global, risk-off:", ro["fiscal"]); print("CDS + componente global, risk-on:", rn["fiscal"])
    print("\nsem caminhos meus (só os outros do P1):")
    r0 = modelo.rodar(sim, caminhos=dict(OUTROS))
    print("  PTAX", linha(r0, "| PTAX")); print("  IPCA", linha(r0, "| IPCA acumulado")); print("  Selic", linha(r0, "| Selic, média"))
    for nome, cam in cen.items():
        full = dict(OUTROS); full.update(cam)
        res = modelo.rodar(sim, caminhos=full)
        print(f"\n######## {nome}")
        for k in ["ffr", "infl_us", "dxy_em", "sp500", "icbr_usd", "icbr_agr_usd", "icbr_met_usd", "fiscal"]:
            if k in cam: print(f"  {k}: " + " ".join(f"{t}={cam[k][t]}" for t in T))
        print("  PTAX ", linha(res, "| PTAX")); print("  IPCA ", linha(res, "| IPCA acumulado")); print("  Selic", linha(res, "| Selic, média"))
    # decomposição: o base contra o base sem cada uma das minhas variáveis (segurada no padrão)
    print("\n## decomposição da PTAX (base − base sem a variável), 4T26 e 1T28")
    full = dict(OUTROS); full.update(base); rb = modelo.rodar(sim, caminhos=full)
    pb = [float(v.replace(",", ".")) for v in linha(rb, "| PTAX").split()]
    for k in ["ffr", "infl_us", "dxy_em", "sp500", "icbr_usd", "icbr_agr_usd", "icbr_met_usd"]:
        f2 = dict(full); f2.pop(k)
        pk = [float(v.replace(",", ".")) for v in linha(modelo.rodar(sim, caminhos=f2), "| PTAX").split()]
        print(f"  {k}: 4T26 {pb[0]-pk[0]:+.3f} · 1T28 {pb[5]-pk[5]:+.3f}")
