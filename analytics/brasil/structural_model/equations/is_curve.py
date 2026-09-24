"""A equacao (H): a curva IS, de onde vem o aquecimento da economia.

    (H) H(t) = h1*H(t-1) + h2*g_rr(t-1) + d08 + d20 + eps

    H     hiato    hiato do produto do BCB, % do produto potencial
    g_rr  g_rr     inclinacao real 2a-10a (NTN-B), p.p. -- o aperto monetario
    d08            2008T4-2009T4        d20   2020T1-2020T4

Sem intercepto. O hiato nao tem nivel proprio de longo prazo: em repouso, com a
inclinacao em zero, a conta devolve ZERO, e `repouso()` afirma isso numericamente.
A media medida do hiato na amostra e -0,18 com desvio 1,68 -- perto de zero, e o
plano da pasta mandava conferir e reportar, entao esta reportado.

## Por que o aperto e uma INCLINACAO, e nao um juro contra um neutro

A forma usual poria `r(t) - RR*(t)`. Medido, ela nao sobrevive a nenhuma escolha de
`RR*` que seja constante ou quase. **Duas amostras, e a diferenca entre elas e so a
janela** -- a de 81 trimestres e a comum, que e a que `comparar_rr()` roda e a que a
pagina mostra, porque a curva da B3 comeca em 2006T1; a de 90 e a mais longa que cada
candidata sozinha permite, e existe aqui para mostrar que o veredito nao e do recorte:

    RR*                            81 tri (comum)    90 tri (cada uma na sua)
    constante 4,5%                 -0,052  (-1,44)   -0,016  (-0,63)
    a neutra declarada no RPM      -0,055  (-1,45)   -0,017  (-0,65)
    mediana das 5 medidas do boxe       --           -0,075  (-1,61)
    HP com cauda Focus             -0,231  (-4,42)   -0,173  (-3,75)
    a inclinacao 2a-10a (a daqui)  -0,164  (-2,62)        --

O HP ajusta MELHOR que a inclinacao, e isso esta na tabela em vez de escondido. O que
o desqualifica nao e o ajuste, sao duas coisas que a tabela nao mostra: ele e um filtro
de dois lados, entao para decidir qual era o equilibrio em 2010 ele usa dado de 2012 --
look-ahead que nao existia na epoca --, e o nivel dele hoje (7,7%) diz que a Selic de
15% quase nao aperta. A inclinacao nao tem nenhum dos dois.

O juro real ex-ante cai de 12,2% em 2001T4 a -0,9% em 2020T4 e volta a 8,5%; o hiato
nao tem essa tendencia. **O que decide a estimativa e o que REMOVE a tendencia, nao o
nivel escolhido** -- e e por isso que as duas candidatas fixas, que nao removem nada,
entregam um h2 tres vezes menor e indistinguivel de zero.

A inclinacao resolve isso sem precisar de `RR*` nenhum: e a diferenca
entre dois precos observados no mesmo pregao, mean-reverting por construcao, sem filtro,
sem pesquisa e sem look-ahead. A ponta de 2 anos carrega o ciclo de politica e a de 10
carrega a estrutural mais o premio; a diferenca e o aperto.

## Por que DEFASADA, e nao contemporanea

O plano pedia `g_rr(t)`. A defasagem de um trimestre e o pico nas DUAS convencoes de
trimestralizacao, o que e o que torna a escolha robusta em vez de garimpada:

    defasagem      media        fechamento
    L0        -0,113 (-1,97)  -0,069 (-1,18)
    L1        -0,164 (-2,62)  -0,177 (-2,65)
    L2        -0,122 (-1,90)  -0,137 (-2,19)

Duas razoes, e as duas apontam para a defasada:

- **E a forma do proprio BC.** A eq. (2) do modelo agregado dele e
  `h = b1*h(-1) - b2*r_hat(-1)/4 - b3*rp_hat + ...`, com o juro real DEFASADO.
- **A contemporanea tem simultaneidade, e ela e visivel no dado.** A correlacao bruta de
  `g_rr(t)` com o hiato e POSITIVA em todas as candidatas de `RR*` (+0,18 a +0,43), sinal
  trocado, porque o Copom aperta quando o hiato abre. Defasar quebra isso.
- **E com a media do trimestre ela nem seria predeterminada.** `g_rr(t)` na convencao de
  media e a media da curva DENTRO do trimestre que se quer explicar; `g_rr(t-1)` esta
  inteiro no passado. A defasagem e o que faz a convencao de media ser legitima.

A troca esta declarada na aba e a forma contemporanea continua estimada ao lado, em
`comparar()`, para a diferenca ser visivel em vez de argumentada.

## O que NAO entra, e por decisao do usuario

O hiato em tempo real (`pm_hiato_produto_vintages`) -- a coluna de robustez que o plano
previa. A serie usada e sempre a edicao CORRENTE do anexo do RPM, que o BCB reescreve a
cada trimestre. Isso atenua `h2` e infla `h1`, porque a edicao corrente e suavizada dos
dois lados; o tamanho disso esta em `pendencias_is_eq.md` como pendencia aberta, nao
medido.

Uso:
    uv run python -m analytics.brasil.structural_model.equations.is_curve
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

# A defasagem do aperto, em trimestres. Nomeada porque e uma DECISAO -- ver a docstring.
LAG_GRR = 1

# Janelas de crise, as mesmas do modelo agregado do BC.
CRISES = {
    "d08": (pd.Period("2008Q4", "Q"), pd.Period("2009Q4", "Q")),
    "d20": (pd.Period("2020Q1", "Q"), pd.Period("2020Q4", "Q")),
}

# (parametro, coluna) -- a ordem e a da equacao
TERMOS = [("h1", "hiato_l1"), ("h2", "g_rr_l")]

ROT = {
    "h1": "Hiato do trimestre anterior",
    "h2": "Aperto monetário do trimestre anterior",
    "d08": "Crise financeira de 2008-2009",
    "d20": "Pandemia de 2020",
}


def montar(df: pd.DataFrame | None = None, col_grr: str = "g_rr",
           lag: int = LAG_GRR) -> pd.DataFrame:
    """Painel -> matriz de regressao da equacao (H).

    So trimestres FECHADOS entram, pela coluna `completo` do painel.
    """
    if df is None:
        df = panel.construir()
    df = df[df["completo"].astype(bool)].copy()

    d = pd.DataFrame(index=df.index)
    d["hiato"] = df["hiato"]
    d["hiato_l1"] = df["hiato"].shift(1)
    d["g_rr_l"] = df[col_grr].shift(lag)
    d["g_rr"] = df[col_grr]
    for k, (a, b) in CRISES.items():
        d[k] = ((d.index >= a) & (d.index <= b)).astype(float)
    return d


def _meia_vida(phis: list[float], passos: int = 400) -> float | None:
    """Trimestres ate um hiato de 1 p.p. andar metade do caminho de volta a zero.

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


def estimar(d: pd.DataFrame | None = None, dummies: bool = True) -> dict:
    """Estima (H) por MQ sem intercepto, com erro-padrao HAC."""
    if d is None:
        d = montar()

    nomes = [p for p, _ in TERMOS] + (list(CRISES) if dummies else [])
    cols = [c for _, c in TERMOS] + (list(CRISES) if dummies else [])

    am = pd.concat([d["hiato"].rename("__y"), d[cols]], axis=1).dropna()
    yv = am["__y"].to_numpy(float)
    Xv = am[cols].to_numpy(float)

    res = sm.OLS(yv, Xv).fit(cov_type="HAC", cov_kwds={"maxlags": HAC_LAGS})
    coef = dict(zip(nomes, res.params))
    se = dict(zip(nomes, res.bse))
    tst = dict(zip(nomes, res.tvalues))
    pvl = dict(zip(nomes, res.pvalues))
    t_ols = dict(zip(nomes, sm.OLS(yv, Xv).fit().tvalues))

    obs = am["__y"]
    fit = pd.Series(Xv @ res.params, index=am.index)
    resid = obs - fit
    e = resid.to_numpy(float)
    sst = float(((obs - obs.mean()) ** 2).sum())
    ssr = float((e ** 2).sum())
    n, kk = len(obs), Xv.shape[1]
    lbt = acorr_ljungbox(e, lags=[4, 8], return_df=True)

    livre = 1.0 - coef["h1"]
    lp = float(coef["h2"] / livre) if livre > 0 else None

    return {
        "estimador": "MQ sem intercepto, erro-padrão HAC(%d)" % HAC_LAGS,
        "hac_lags": HAC_LAGS, "lag_grr": LAG_GRR,
        "n": n, "k": kk, "ini": am.index[0], "fim": am.index[-1],
        "coef": coef, "se": se, "t": tst, "p": pvl, "t_ols": t_ols,
        "termos": list(TERMOS), "dummies": list(CRISES) if dummies else [],
        "persistencia": float(coef["h1"]),
        "estavel": bool(abs(coef["h1"]) < 1.0),
        "meia_vida": _meia_vida([float(coef["h1"])]),
        "longo_prazo": {"h2": lp},
        "efeito_lp": lp,
        "r2": 1.0 - ssr / sst,
        "r2_ajustado": 1.0 - (1.0 - ssr / sst) * (n - 1) / (n - kk),
        "rmse": float(np.sqrt(ssr / n)),
        "erro_medio": float(np.abs(e).mean()),
        "acf": [float(pd.Series(e).autocorr(lag)) for lag in range(1, 7)],
        "lb_q4": float(lbt["lb_stat"].iloc[0]), "lb_p4": float(lbt["lb_pvalue"].iloc[0]),
        "lb_q8": float(lbt["lb_stat"].iloc[1]), "lb_p8": float(lbt["lb_pvalue"].iloc[1]),
        "idx": am.index, "obs": obs, "fit": fit, "resid": resid,
        "hiato_medio": float(d["hiato"].mean()), "hiato_sd": float(d["hiato"].std()),
    }


def rotulo(par: str) -> str:
    """Nome legivel de um parametro, para a tela nao imprimir `h1`."""
    return ROT.get(par, par)


def repouso(r: dict) -> dict:
    """Confere NUMERICAMENTE o que a ausencia de intercepto compra.

    Duas propriedades, e as duas sao afirmadas em vez de argumentadas:

    1. **Em repouso o hiato volta a ZERO.** Sem intercepto e com |h1| < 1, a conta nao
       tem nivel proprio de longo prazo -- o que e a definicao de um hiato.
    2. **O efeito de longo prazo de um aperto permanente bate com a formula**
       `h2 / (1 - h1)`, simulando em vez de confiar na algebra.
    """
    h1, h2 = r["coef"]["h1"], r["coef"]["h2"]
    if abs(h1) >= 1.0:
        raise AssertionError("h1 = %.4f: a equacao nao e estavel" % h1)

    def rodar(g: float, h0: float = 1.0) -> float:
        h = h0
        for _ in range(4000):
            h = h1 * h + h2 * g
        return h

    for h0 in (-3.0, -1.0, 1.0, 5.0):
        if abs(rodar(0.0, h0)) > 1e-8:
            raise AssertionError("repouso nao devolve zero partindo de %.1f" % h0)
    sim = rodar(1.0)
    if r["efeito_lp"] is not None and abs(sim - r["efeito_lp"]) > 1e-6:
        raise AssertionError("efeito simulado %.6f != formula %.6f" % (sim, r["efeito_lp"]))
    return {"volta_a_zero": True, "efeito_simulado": float(sim),
            "efeito_formula": r["efeito_lp"]}


# As leituras alternativas medidas ao lado. Nenhuma e a especificacao: elas existem para
# a pagina poder mostrar o que a escolha custou, em vez de a afirmar.
COMPARAR = {
    "base":    dict(desc="A conta da página: inclinação do trimestre anterior",
                    col="g_rr", lag=1, dummies=True),
    "cont":    dict(desc="A inclinação do trimestre corrente, como o plano pedia",
                    col="g_rr", lag=0, dummies=True),
    "lag2":    dict(desc="A inclinação de dois trimestres atrás",
                    col="g_rr", lag=2, dummies=True),
    "fim":     dict(desc="Pelo fechamento do trimestre, e não pela média",
                    col="g_rr_fim", lag=1, dummies=True),
    "sem_cri": dict(desc="Sem as duas crises marcadas",
                    col="g_rr", lag=1, dummies=False),
}


def comparar(df: pd.DataFrame | None = None) -> dict:
    """As leituras de COMPARAR na mesma amostra comum, para serem comparaveis.

    Sem a amostra comum a tabela mentiria: a leitura com duas defasagens perde um
    trimestre a mais, e um R2 medido em janela diferente nao se compara com o de cima.
    """
    if df is None:
        df = panel.construir()
    montadas = {k: montar(df, v["col"], v["lag"]) for k, v in COMPARAR.items()}

    comum = None
    for k, v in COMPARAR.items():
        cols = ["hiato", "hiato_l1", "g_rr_l"] + (list(CRISES) if v["dummies"] else [])
        ix = montadas[k][cols].dropna().index
        comum = ix if comum is None else comum.intersection(ix)

    out = {}
    for k, v in COMPARAR.items():
        r = estimar(montadas[k].loc[comum], dummies=v["dummies"])
        r["desc"] = v["desc"]
        out[k] = r
    return out


# ── A tabela de "e se o aperto fosse medido contra um juro de equilibrio?" ───
#
# Nao e robustez da especificacao: e o registro do que motivou a escolha da inclinacao.
# Cada linha troca o regressor por `r_ex_ante(t) - RR*(t)`, com uma definicao de RR*
# diferente, e mede o mesmo h2 na mesma janela.
#
# A neutra que o BC DECLARA no RPM, por reuniao. Transcrita em
# `monetary_policy/antecipa_copom.py` como `R_NEUTRA_BC`; aqui ela vira degrau
# trimestral pelas datas em que passou a valer.
NEUTRA_BC = [(pd.Period("2024Q2", "Q"), 4.75), (pd.Period("2024Q4", "Q"), 5.00)]
NEUTRA_BC_BASE = 4.50


def _juro_real_ex_ante() -> pd.Series:
    """Selic esperada em 12 meses menos IPCA esperado em 12 meses, trimestral.

    E o `r_focus` do modelo agregado do BC, montado das mesmas funcoes -- nao copiado.
    """
    from analytics.brasil.monetary_policy.modelo_painel import (
        focus_ipca_12m, focus_selic_12m)
    return (focus_selic_12m() - focus_ipca_12m()).dropna()


def comparar_rr(df: pd.DataFrame | None = None) -> list[dict]:
    """h2 sob cada definicao de RR*, mais a inclinacao, na mesma amostra comum."""
    from analytics.brasil.monetary_policy.modelo_painel import cauda_juro_real, hp

    if df is None:
        df = panel.construir()
    r = _juro_real_ex_ante()
    fim = r.index.max()

    dec = pd.Series(NEUTRA_BC_BASE, index=r.index, dtype=float)
    for ini, v in NEUTRA_BC:
        dec[dec.index >= ini] = v

    cands = [
        ("const", "uma taxa fixa de 4,5% ao ano", r - 4.5),
        ("bc", "a taxa que o Banco Central declara usar (5,0% hoje)", r - dec),
        ("hp", "um filtro estatístico sobre o próprio juro real observado",
         r - hp(r, "tend", fim, cauda_juro_real(fim)).reindex(r.index)),
        ("incl", "a inclinação da curva real: o juro de 2 anos menos o de 10",
         df["g_rr"]),
    ]

    # amostra comum: sem ela a linha do filtro, que alcanca mais tras, leria melhor so
    # por ter mais trimestres
    comum = None
    for _k, _d, g in cands:
        ix = montar(df).assign(__g=g.shift(LAG_GRR))[
            ["hiato", "hiato_l1", "__g"] + list(CRISES)].dropna().index
        comum = ix if comum is None else comum.intersection(ix)

    out = []
    for k, desc, g in cands:
        d = montar(df)
        d["g_rr_l"] = g.shift(LAG_GRR)
        rr = estimar(d.loc[comum])
        out.append({"key": k, "desc": desc, "escolhida": k == "incl",
                    "h2": float(rr["coef"]["h2"]), "t": float(rr["t"]["h2"]),
                    "r2": rr["r2"], "n": rr["n"]})
    return out


def _p(v, dec=4):
    return "%*.*f" % (dec + 4, dec, v)


def main() -> None:
    r = estimar()

    print("(H) curva IS -- %s" % r["estimador"])
    print("    %s a %s, %d trimestres" % (r["ini"], r["fim"], r["n"]))
    print("    o aperto entra defasado %d trimestre(s)" % r["lag_grr"])
    print()
    print("  parametro                                      peso       ee      t  t(MQ)"
          "      p   longo prazo")
    for par in [p for p, _ in r["termos"]] + r["dummies"]:
        lp = r["longo_prazo"].get(par)
        print("  %-42s %s %s %6.2f %6.2f %6.3f %s"
              % (rotulo(par), _p(r["coef"][par]), _p(r["se"][par]), r["t"][par],
                 r["t_ols"][par], r["p"][par],
                 "  -" if lp is None else "%9.3f" % lp))
    print()
    print("  R2 %.4f - RMSE %.4f - erro medio %.4f - Ljung-Box p %.3f / %.3f"
          % (r["r2"], r["rmse"], r["erro_medio"], r["lb_p4"], r["lb_p8"]))
    print("  meia-vida de um hiato: %.0f trimestres" % r["meia_vida"])
    print("  efeito de longo prazo de 1 p.p. de aperto: %.3f p.p. de hiato" % r["efeito_lp"])
    print("  hiato: media %.4f, desvio %.4f  (o plano mandava conferir a media)"
          % (r["hiato_medio"], r["hiato_sd"]))
    print("  repouso:", repouso(r))
    print("  acf do residuo (1..6):", " ".join("%5.2f" % a for a in r["acf"]))
    print()
    print("  leituras de comparacao, na amostra comum:")
    C = comparar()
    print("    %-52s %8s %6s %7s %7s" % ("", "h2", "t", "R2", "RMSE"))
    for k, rr in C.items():
        print("    %-52s %s %6.2f %7.4f %7.4f"
              % (rr["desc"], _p(rr["coef"]["h2"]), rr["t"]["h2"], rr["r2"], rr["rmse"]))
    print()
    print("  e se o aperto fosse o juro real contra um equilibrio, mesma janela:")
    for rr in comparar_rr():
        print("    %-52s %s %6.2f  (n=%d)"
              % (rr["desc"], _p(rr["h2"]), rr["t"], rr["n"]))
    print()
    print("  maiores residuos:")
    s = r["resid"].sort_values()
    for p, x in list(s.items())[:2] + list(s.items())[-2:]:
        print("    %s  %+6.2f  (observado %.2f, conta %.2f)"
              % (p, x, r["obs"].loc[p], r["fit"].loc[p]))


if __name__ == "__main__":
    main()
