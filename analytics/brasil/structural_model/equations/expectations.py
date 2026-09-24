"""A equacao (E): como a expectativa de inflacao se forma.

    (E) E(t) = e1*E(t-1) + e2*I12(t) + (1-e1-e2)*Meta(t) + eps

    E     pi_e       Focus IPCA 12 meses a frente, suavizada, % ao ano
    I12   ipca_12m   IPCA acumulado em 12 meses publicado (SGS 13522), % ao ano
    Meta  meta_12m   meta do CMN no horizonte de 12 meses, % ao ano

Esta e a especificacao do plano da pasta, sem acrescimo nenhum. O que ja foi medido e
ficou de fora esta listado em `pendencias.md` (secao 8), com o numero de cada coisa --
a decisao de incorporar ou nao vem depois de todas as equacoes estarem de pe.

Tudo em taxa ANUAL, ao contrario da curva de Phillips, que vive na unidade do
trimestre. O que esta equacao explica e uma expectativa de doze meses e o alvo dela e
a meta, que tambem e anual -- e por isso que `pi_e` entra inteiro aqui e dividido por
quatro la.

## A restricao, e o que ela garante de graca

Os pesos da inercia, da inflacao e da meta somam 1, e a consequencia e estrutural: em
repouso, com a inflacao na meta, a equacao devolve a META, quaisquer que sejam os
coeficientes. **A ancoragem nao e estimada, e imposta**; o que se estima e a VELOCIDADE
com que ela opera e o quanto a inflacao corrente desvia a expectativa pelo caminho. Sem
a restricao, a regressao poderia devolver um nivel de longo prazo diferente da meta,
que e uma afirmacao que a amostra nao sustenta.

A imposicao e reparametrizacao exata -- subtrai-se a meta dos dois lados e regride-se
o desvio contra o desvio, SEM INTERCEPTO:

    E(t) - Meta(t) = e1*[E(t-1) - Meta(t)] + e2*[I12(t) - Meta(t)] + eps

## As duas leituras que saem dos pesos

- **meia-vida**: quantos trimestres um desvio de 1 p.p. leva para andar metade do
  caminho de volta, com a inflacao na meta.
- **repasse de longo prazo**: `e2 / (1 - e1)`, quanto de uma inflacao permanentemente
  um ponto acima da meta a expectativa acaba incorporando.

## O residuo, e por que o erro-padrao e HAC

O regressando e uma expectativa de doze meses lida a cada tres, e o regressor e um
acumulado de doze meses amostrado a cada tres: trimestres vizinhos falam do mesmo
periodo em nove dos doze meses. A sobreposicao esta no OBJETO, nao na amostragem, entao
o residuo e autocorrelacionado por construcao e o erro-padrao tem de aguentar isso. O
Ljung-Box do residuo esta na pagina em vez de escondido.

## A meta e a do HORIZONTE, nao a do ano

A Focus de 12 meses suavizada e uma interpolacao entre a expectativa do ano corrente e
a do seguinte. Casar a meta com a MESMA convencao (`panel.META_W_Q`) e o que impede um
degrau de janeiro de entrar no desvio que a equacao explica.

## Onde isto difere da eq. (5) do BC, e por que

    (5) pi^e = f1*pi^e(-1) + f2*E_t[pi(t,t+4)] + f3*MA4(pi^IPCA) + (1-f1-f2-f3)*meta

`analytics/brasil/monetary_policy/modelo_agregado.py` replica essa, e as modas
publicadas sao f1 0,75 - f2 0,11 - f3 0,021 - meta 0,119. Duas diferencas, as duas
declaradas na aba:

- **Nao ha o termo de MA(4) do IPCA passado** (`f3`), que no BC ja e desprezivel: 0,021
  com IC [0; 0,049].
- **`f2` e a previsao DO PROPRIO MODELO** quatro trimestres a frente, e nao existe
  aqui: ela exige rodar o filtro a cada trimestre da amostra. O nosso `e2` e a inflacao
  REALIZADA, que olha para tras -- e por isso as duas colunas nao sao somaveis. Foi
  essa troca que eliminou a simultaneidade que no BC custou um estimador em dois
  passos (condicionar em pi^e observado em t leva f2 de 0,21 para 0,42).

Uso:
    uv run python -m analytics.brasil.structural_model.equations.expectations
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_ljungbox

from analytics.brasil.structural_model import panel

warnings.filterwarnings("ignore")

HAC_LAGS = 4

# (parametro, coluna do painel) -- os dois dividem a soma-um com a meta
TERMOS = [("e1", "pi_e_l1"), ("e2", "i12")]
META = "meta_12m"

ROT = {
    "e1": "Expectativa do trimestre anterior",
    "e2": "IPCA acumulado em 12 meses",
}


def montar(df: pd.DataFrame | None = None) -> pd.DataFrame:
    """Painel -> matriz de regressao da equacao (E).

    So trimestres FECHADOS entram, pela coluna `completo` do painel.
    """
    if df is None:
        df = panel.construir()
    df = df[df["completo"].astype(bool)].copy()

    d = pd.DataFrame(index=df.index)
    d["pi_e"] = df["pi_e"]
    d["pi_e_l1"] = df["pi_e"].shift(1)
    d["i12"] = df["ipca_12m"]
    d["meta_12m"] = df["meta_12m"]
    return d


def _meia_vida(phis: list[float], passos: int = 400) -> float | None:
    """Trimestres ate um desvio de 1 p.p. andar metade do caminho de volta.

    Simulado e nao pela raiz: com uma defasagem so os dois coincidem, mas a forma
    simulada continua valendo se a equacao ganhar uma segunda.
    """
    hist = [1.0] * len(phis)
    for t in range(passos):
        v = sum(p * hist[-i - 1] for i, p in enumerate(phis))
        hist.append(v)
        if abs(v) <= 0.5:
            return float(t + 1)
    return None


def estimar(d: pd.DataFrame | None = None) -> dict:
    """Estima (E). A restricao e imposta antes, nao depois."""
    if d is None:
        d = montar()
    meta = d[META]

    y = d["pi_e"] - meta
    X, nomes = pd.DataFrame(index=d.index), []
    for par, col in TERMOS:
        X["__" + par] = d[col] - meta
        nomes.append(par)

    am = pd.concat([y.rename("__y"), X], axis=1).dropna()
    yv = am["__y"].to_numpy(float)
    Xv = am[X.columns].to_numpy(float)

    res = sm.OLS(yv, Xv).fit(cov_type="HAC", cov_kwds={"maxlags": HAC_LAGS})
    coef = dict(zip(nomes, res.params))
    se = dict(zip(nomes, res.bse))
    tst = dict(zip(nomes, res.tvalues))
    pvl = dict(zip(nomes, res.pvalues))
    t_ols = dict(zip(nomes, sm.OLS(yv, Xv).fit().tvalues))

    dd = d.loc[am.index]
    mm = dd[META]
    peso_meta = 1.0 - sum(coef[p] for p, _ in TERMOS)
    fit = peso_meta * mm
    for par, col in TERMOS:
        fit = fit + coef[par] * dd[col]

    obs = dd["pi_e"]
    resid = obs - fit
    e = resid.to_numpy(float)
    sst = float(((obs - obs.mean()) ** 2).sum())
    ssr = float((e ** 2).sum())
    n, kk = len(obs), Xv.shape[1]
    lbt = acorr_ljungbox(e, lags=[4, 8], return_df=True)

    livre = 1.0 - coef["e1"]
    repasse = float(coef["e2"] / livre) if livre > 0 else None

    return {
        "estimador": "MQ, erro-padrão HAC(%d)" % HAC_LAGS,
        "hac_lags": HAC_LAGS,
        "n": n, "k": kk, "ini": am.index[0], "fim": am.index[-1],
        "coef": coef, "se": se, "t": tst, "p": pvl, "t_ols": t_ols,
        "termos": list(TERMOS),
        "peso_meta": float(peso_meta),
        "soma_inercia": float(coef["e1"]),
        "soma_infl": float(coef["e2"]),
        "longo_prazo": {"e2": repasse},
        "meia_vida": _meia_vida([float(coef["e1"])]),
        "repasse_lp": repasse,
        "r2": 1.0 - ssr / sst,
        "r2_ajustado": 1.0 - (1.0 - ssr / sst) * (n - 1) / (n - kk),
        "rmse": float(np.sqrt(ssr / n)),
        "erro_medio": float(np.abs(e).mean()),
        "acf": [float(pd.Series(e).autocorr(lag)) for lag in range(1, 7)],
        "lb_q4": float(lbt["lb_stat"].iloc[0]), "lb_p4": float(lbt["lb_pvalue"].iloc[0]),
        "lb_q8": float(lbt["lb_stat"].iloc[1]), "lb_p8": float(lbt["lb_pvalue"].iloc[1]),
        "idx": am.index, "obs": obs, "fit": fit, "resid": resid, "meta": mm,
    }


def rotulo(par: str) -> str:
    """Nome legivel de um parametro, para a tela nao imprimir `e1`."""
    return ROT.get(par, par)


def repouso(r: dict) -> dict:
    """Confere NUMERICAMENTE que a equacao devolve a meta em repouso.

    E teste de algebra e nao de dado -- mas e a propriedade que justifica a restricao,
    entao ela e afirmada em vez de argumentada. Depois mede o repasse de uma inflacao
    que fica permanentemente `x` acima da meta, que tem de bater com a formula.
    """
    e1, e2 = r["coef"]["e1"], r["coef"]["e2"]

    def rodar(alvo: float, x: float) -> float:
        h = alvo
        for _ in range(4000):
            h = e1 * h + e2 * (alvo + x) + r["peso_meta"] * alvo
        return h

    for alvo in (2.0, 3.0, 4.5, 8.5):
        if abs(rodar(alvo, 0.0) - alvo) > 1e-8:
            raise AssertionError("repouso nao devolve a meta em %.1f" % alvo)
    sim = rodar(3.0, 1.0) - 3.0
    if r["repasse_lp"] is not None and abs(sim - r["repasse_lp"]) > 1e-6:
        raise AssertionError("repasse simulado %.6f != formula %.6f"
                             % (sim, r["repasse_lp"]))
    return {"devolve_a_meta": True, "repasse_simulado": float(sim),
            "repasse_formula": r["repasse_lp"]}


def _p(v, dec=4):
    return "%*.*f" % (dec + 4, dec, v)


def main() -> None:
    r = estimar()

    print("(E) expectativa de inflacao -- %s" % r["estimador"])
    print("    %s a %s, %d trimestres" % (r["ini"], r["fim"], r["n"]))
    print()
    print("  parametro                                      peso       ee      t  t(MQ)"
          "      p   longo prazo")
    for par, _col in r["termos"]:
        lp = r["longo_prazo"].get(par)
        print("  %-42s %s %s %6.2f %6.2f %6.3f %s"
              % (rotulo(par), _p(r["coef"][par]), _p(r["se"][par]), r["t"][par],
                 r["t_ols"][par], r["p"][par],
                 "  -" if lp is None else "%9.3f" % lp))
    print("  %-42s %s   (o que sobra de 1)" % ("Peso da meta", _p(r["peso_meta"])))
    print()
    print("  R2 %.4f - RMSE %.4f - erro medio %.4f - Ljung-Box p %.3f / %.3f"
          % (r["r2"], r["rmse"], r["erro_medio"], r["lb_p4"], r["lb_p8"]))
    print("  meia-vida de um desvio: %.0f trimestres" % r["meia_vida"])
    print("  repasse de uma inflacao permanente: %.3f" % r["repasse_lp"])
    print("  repouso:", repouso(r))
    print("  acf do residuo (1..6):", " ".join("%5.2f" % a for a in r["acf"]))
    print()
    print("  maiores residuos:")
    s = r["resid"].sort_values()
    for p, x in list(s.items())[:2] + list(s.items())[-2:]:
        print("    %s  %+6.2f  (observado %.2f, conta %.2f)"
              % (p, x, r["obs"].loc[p], r["fit"].loc[p]))


if __name__ == "__main__":
    main()
