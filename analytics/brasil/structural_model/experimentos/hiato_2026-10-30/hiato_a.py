"""Teste A do hiato -- chat C do Plano 2, 2026-10-30.

Decisao do usuario (coordenacao/C_modelo.md, "Decisoes", item 3a): no trecho em que o
hiato do BC ja quase nao e revisado, regredi-lo contra os insumos que o proprio BC usa
(PIB, CAGED, desocupacao, NUCI), e usar a regressao para estimar o hiato FINAL dos
trimestres recentes, que o BC ainda vai revisar.

Insumos, todos olhando so para tras (um filtro de dois lados reproduziria o problema
de fim de amostra que o teste quer evitar):

    nuci   NUCI da FGV, ind. de transformacao, dessazonalizada por X-13, media do tri
    desoc  taxa de desocupacao a.s. retropolada pelo BC (anexo do RPM), fim do tri
    pib    ciclo do log do PIB a.s. pelo filtro de Hamilton (2018): h=8, 4 defasagens
    caged  idem para o log do estoque do CAGED

O filtro de Hamilton e reestimado so com o dado que cada edicao via.

Tres partes:
    1. o tamanho da revisao do hiato por idade do trimestre (escolhe N);
    2. a regressao no trecho consolidado da edicao de hoje (R2, sinais, estabilidade);
    3. pseudo tempo real: em cada edicao, a regressao com o que ela sabia contra a
       primeira publicacao do BC, as duas medidas contra o valor final de hoje.

Rodar:  uv run python analytics/brasil/structural_model/experimentos/hiato_2026-10-30/hiato_a.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

from analytics.brasil.structural_model.modelo_agregado.modelo_painel import (
    _nivel_sa, nuci_fgv, para_q, q, serie)

AQUI = Path(__file__).parent
DATA = AQUI / "data"
N_PADRAO = 12
ESPECS = {
    "S1": ["nuci", "desoc", "pib", "caged"],
    "S2": ["nuci", "desoc", "pib", "caged", "desoc_l1", "caged_l1"],
    "S0": ["nuci", "desoc", "caged"],            # sem PIB: o trimestre da edicao
}


# ── dados ────────────────────────────────────────────────────────────────────
def _csv(nome: str, fn) -> pd.Series:
    p = DATA / nome
    if p.exists():
        s = pd.read_csv(p, index_col=0).iloc[:, 0]
        s.index = pd.to_datetime(s.index)
        return s
    DATA.mkdir(exist_ok=True)
    s = fn()
    s.to_frame("value").to_csv(p)
    return s


def vintages() -> pd.DataFrame:
    v = q("macro_brasil", "SELECT vintage, date, value FROM pm_hiato_produto_vintages "
                          "WHERE variavel='central'")
    v["vintage"] = pd.to_datetime(v["vintage"]).dt.to_period("Q")
    v["date"] = pd.to_datetime(v["date"]).dt.to_period("Q")
    v["value"] = v["value"].astype(float)
    return v.pivot(index="date", columns="vintage", values="value").sort_index()


def mensais() -> dict:
    nuci = _csv("nuci_fgv.csv", nuci_fgv)
    desoc = _csv("desoc_retro.csv", lambda: serie("macro_brasil", "mt_desocupacao_retro"))
    caged = _csv("caged_total.csv", lambda: serie("macro_brasil", "mt_caged", "caged_total"))
    d = q("macro_brasil", "SELECT date, value FROM atv_pib WHERE name='pib_pm' "
                          "AND seasonal_adjs='Y' ORDER BY date")
    pib = pd.Series(d["value"].astype(float).values,
                    index=pd.PeriodIndex(pd.to_datetime(d["date"]), freq="Q"))
    return {"nuci": nuci, "desoc": desoc, "caged": caged, "pib": pib}


def hamilton(logq: pd.Series, h: int = 8, p: int = 4) -> pd.Series:
    """Ciclo de Hamilton: o erro de prever y(t) com y(t-h), ..., y(t-h-p+1)."""
    y = logq.dropna()
    X = pd.concat([y.shift(h + i) for i in range(p)], axis=1)
    X.columns = ["l%d" % i for i in range(p)]
    am = pd.concat([y.rename("y"), X], axis=1).dropna()
    r = sm.OLS(am["y"], sm.add_constant(am[X.columns])).fit()
    return (am["y"] - r.fittedvalues).reindex(y.index)


def insumos(M: dict, corte: pd.Period, nuci_sa: pd.Series) -> pd.DataFrame:
    """Os regressores trimestrais com o que se sabia na edicao do trimestre `corte`.

    Uma edicao do RPM sai no fim do ultimo mes do trimestre. Nesse dia ha NUCI ate o
    mes anterior, desocupacao e CAGED ate dois meses antes, e PIB ate o trimestre
    anterior. Sem vintages desses dados, o valor e o de hoje: so o CORTE e respeitado.
    """
    fim_m = corte.asfreq("M", "end")

    def ate(s, defas):
        lim = (fim_m - defas).to_timestamp()
        return s[s.index <= lim]

    d = pd.DataFrame()
    d["nuci"] = para_q(ate(nuci_sa, 1), "media", completos=False)
    d["desoc"] = para_q(ate(M["desoc"], 2), "ultimo", completos=False)
    cg = para_q(ate(M["caged"], 2), "ultimo", completos=False)
    d["caged"] = hamilton(np.log(cg) * 100)
    pib = M["pib"][M["pib"].index <= corte - 1]
    d = d.join(hamilton(np.log(pib) * 100).rename("pib"), how="outer")
    d["desoc_l1"] = d["desoc"].shift(1)
    d["caged_l1"] = d["caged"].shift(1)
    return d.loc[pd.Period("2003Q4", "Q"):]


# ── 1. revisao por idade ─────────────────────────────────────────────────────
def revisao_por_idade(V: pd.DataFrame) -> pd.DataFrame:
    ult = V.columns.max()
    fin = V[ult]
    linhas = []
    for v in V.columns[:-1]:
        for t, x in V[v].dropna().items():
            idade_hoje = (ult - t).n
            if idade_hoje < N_PADRAO:          # o "final" ainda nao e final
                continue
            linhas.append({"edicao": v, "idade": (v - t).n, "rev": fin[t] - x,
                           "pos2024": v >= pd.Period("2024Q3", "Q")})
    return pd.DataFrame(linhas)


# ── 2. a regressao ──────────────────────────────────────────────────────────
def ajustar(y: pd.Series, X: pd.DataFrame):
    am = pd.concat([y.rename("y"), X], axis=1).dropna()
    r = sm.OLS(am["y"], sm.add_constant(am[X.columns])).fit(
        cov_type="HAC", cov_kwds={"maxlags": 4})
    return r, am


def prever(r, X: pd.DataFrame) -> pd.Series:
    return pd.Series(sm.add_constant(X, has_constant="add")[r.params.index].to_numpy() @
                     r.params.to_numpy(), index=X.index)


# ── 3. pseudo tempo real ─────────────────────────────────────────────────────
def pseudo_rt(V, M, nuci_sa, N, alvo_hoje: bool) -> pd.DataFrame:
    """Para cada edicao: estimativa da regressao contra a publicacao do BC.

    `alvo_hoje=False`: treina na propria edicao (o que se sabia).
    `alvo_hoje=True`: treina na edicao de HOJE truncada no corte da edicao -- isola a
    troca de metodologia do BC em 2024, que reescreveu a historia inteira e que a
    regressao nao tem como antecipar. O dado do treino continua sendo so o antigo.
    """
    ult = V.columns.max()
    fin = V[ult]
    linhas = []
    for v in V.columns:
        X = insumos(M, v, nuci_sa)
        y_tr = (fin if alvo_hoje else V[v]).copy()
        y_tr = y_tr[(y_tr.index <= v - N)]
        for idade in range(N):
            t = v - idade
            if (ult - t).n < N_PADRAO or t not in V.index or pd.isna(V.at[t, v]):
                continue                        # sem valor final para comparar
            espec = "S1" if not pd.isna(X["pib"].get(t, np.nan)) else "S0"
            r, _ = ajustar(y_tr, X[ESPECS[espec]])
            est = float(prever(r, X.loc[[t], ESPECS[espec]]).iloc[0])
            linhas.append({"edicao": v, "tri": t, "idade": idade, "espec": espec,
                           "bc": V.at[t, v], "reg": est, "final": fin[t]})
    out = pd.DataFrame(linhas)
    out["e_bc"] = out["bc"] - out["final"]
    out["e_reg"] = out["reg"] - out["final"]
    return out


def main() -> None:
    V = vintages()
    M = mensais()
    nuci_sa = _nivel_sa(M["nuci"])
    ult = V.columns.max()
    print(f"edicoes: {len(V.columns)} ({V.columns.min()} a {ult})")

    print("\n1. revisao |final - publicado| por idade, so trimestres ja consolidados hoje")
    R = revisao_por_idade(V)
    g = R.groupby("idade")["rev"].agg(n="count", media=lambda s: s.abs().mean(),
                                       vies="mean", maximo=lambda s: s.abs().max())
    print(g.loc[0:16].round(3).to_string())
    g2 = R[R.pos2024].groupby("idade")["rev"].agg(n="count", media=lambda s: s.abs().mean())
    print("   so edicoes desde 2024-09 (depois da troca de metodologia):")
    print("   " + "  ".join(f"{i}:{m:.2f}(n{n})" for i, (n, m) in g2.iterrows()))

    print(f"\n2. regressao na edicao de hoje ({ult}), trimestres com idade >= {N_PADRAO}")
    X = insumos(M, ult, nuci_sa)
    y = V[ult][V.index <= ult - N_PADRAO]
    for esp, cols in ESPECS.items():
        r, am = ajustar(y, X[cols])
        print(f"   {esp}: {am.index[0]}-{am.index[-1]} n={len(am)} R2={r.rsquared:.3f} "
              f"RMSE={np.sqrt(r.mse_resid):.3f}")
        print("      " + "  ".join(f"{c} {r.params[c]:+.3f} (t {r.tvalues[c]:+.1f})"
                                   for c in r.params.index))
    for nome, (a, b) in {"2004-2014": ("2004Q1", "2014Q4"),
                         "2015-2023": ("2015Q1", "2023Q4")}.items():
        yy = y[(y.index >= pd.Period(a, "Q")) & (y.index <= pd.Period(b, "Q"))]
        r, am = ajustar(yy, X[ESPECS["S1"]])
        print(f"   S1 {nome}: n={len(am)} R2={r.rsquared:.3f}  " +
              "  ".join(f"{c} {r.params[c]:+.3f}" for c in ESPECS["S1"]))
    sem20 = y[(y.index < pd.Period("2020Q1", "Q")) | (y.index > pd.Period("2020Q4", "Q"))]
    r, am = ajustar(sem20, X[ESPECS["S1"]])
    print(f"   S1 sem 2020: n={len(am)} R2={r.rsquared:.3f}  " +
          "  ".join(f"{c} {r.params[c]:+.3f}" for c in ESPECS["S1"]))

    for alvo_hoje, rot in ((False, "treino na propria edicao"),
                           (True, "treino na edicao de hoje truncada (metodologia atual)")):
        for N in (8, 12):
            P = pseudo_rt(V, M, nuci_sa, N, alvo_hoje)
            print(f"\n3. pseudo tempo real, {rot}, N={N}: |erro| medio contra o final")
            t = P.groupby("idade").agg(n=("e_bc", "size"),
                                       bc=("e_bc", lambda s: s.abs().mean()),
                                       reg=("e_reg", lambda s: s.abs().mean()),
                                       vies_bc=("e_bc", "mean"), vies_reg=("e_reg", "mean"))
            t["ganho"] = 1 - t["reg"] / t["bc"]
            print(t.round(3).to_string())
            caso = P[(P.tri >= pd.Period("2022Q4", "Q")) & (P.tri <= pd.Period("2024Q1", "Q"))
                     & (P.idade <= 2)]
            if len(caso):
                sinal_bc = (np.sign(caso.bc) == np.sign(caso.final)).mean()
                sinal_reg = (np.sign(caso.reg) == np.sign(caso.final)).mean()
                print(f"   2022T4-2024T1, idade 0-2: sinal certo BC {sinal_bc:.0%}, "
                      f"regressao {sinal_reg:.0%} (n={len(caso)})")
                print("   " + caso.sort_values(["tri", "idade"]).apply(
                    lambda r: f"{r.tri}/{r.idade}: bc {r.bc:+.2f} reg {r.reg:+.2f} fin {r.final:+.2f}",
                    axis=1).str.cat(sep=" | "))

    print(f"\n4. hoje: regressao treinada na edicao {ult} (idade >= {N_PADRAO}) nos trimestres recentes")
    r1, _ = ajustar(y, X[ESPECS["S1"]])
    r0, _ = ajustar(y, X[ESPECS["S0"]])
    for t in [ult - i for i in range(N_PADRAO - 1, -1, -1)]:
        tem_pib = not pd.isna(X["pib"].get(t, np.nan))
        r, esp = (r1, "S1") if tem_pib else (r0, "S0")
        est = float(prever(r, X.loc[[t], ESPECS[esp]]).iloc[0]) if t in X.index and \
            X.loc[t, ESPECS[esp]].notna().all() else float("nan")
        print(f"   {t} ({esp}): publicado {V.at[t, ult]:+.2f}  regressao {est:+.2f}")


if __name__ == "__main__":
    sys.exit(main())
