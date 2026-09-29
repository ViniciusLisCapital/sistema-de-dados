"""A equacao (H): a curva IS, de onde vem o aquecimento da economia.

    (H) H(t) = h1*H(t-1) + h2*gap(t-1) + d08 + d20 + eps

    H     hiato     hiato do produto do BCB, % do produto potencial
    gap   gap_juro  Selic - (rr_10a + meta_12m), p.p. -- o aperto monetario
    d08             2008T4-2009T4        d20   2020T1-2020T4

Sem intercepto. O hiato nao tem nivel proprio de longo prazo: em repouso, com o aperto
em zero, a conta devolve ZERO, e `repouso()` afirma isso numericamente. A media medida
do hiato na amostra e -0,18 com desvio 1,68 -- perto de zero, e o plano da pasta mandava
conferir e reportar, entao esta reportado.

## O aperto e a distancia ate a ANCORA da regra de juros

`rr_10a + meta_12m` e o mesmo juro nominal de equilibrio que a (R) persegue. Medir o
aperto como `Selic - ancora` e portanto dizer que **os dois blocos do modelo medem
distancia ate o mesmo ponto**: o Copom move a Selic na direcao da ancora, e o quanto ela
ficou longe dali e o que esfria ou aquece o produto.

Ate 2026-09-25 o aperto era a inclinacao real 2a-10a, `rr_2a - rr_10a`, e a docstring
daqui opunha "uma inclinacao" a "um juro contra um neutro". **A oposicao nao existe**, e
a algebra e o que mostra:

    inclinacao   = rr_2a          - rr_10a
    gap          = (Selic - meta) - rr_10a

O neutro e o MESMO nos dois. O que muda e a perna da politica: o juro real de 2 anos que
o mercado precifica, ou a Selic deflacionada pela meta. As duas pernas correlacionam
**+0,875** e as duas medidas do aperto, **+0,767**.

## O que a troca custou e comprou, medido

Mesmos 81 trimestres (2006T2-2026T2), so o regressor mudando:

    aperto                h1      h2    t(h2)   h2*dp   lp*dp      R2    RMSE   LB(4)
    inclinacao 2a-10a  0,886  -0,164   -2,62  -0,167  -1,468  0,8678   0,642   0,021
    gap da ancora      0,877  -0,071   -2,12  -0,185  -1,502  0,8703   0,636   0,070

**Os `h2` nao se comparam entre si** -- o gap tem desvio 2,60 e a inclinacao 1,02, entao
o coeficiente menor nao e efeito menor. Por desvio da propria medida os dois entregam
quase o mesmo, com o gap 11% mais forte. O que muda de verdade e o **residuo**: a forma
anterior REPROVAVA Ljung-Box(4) a 5% (p 0,021) e esta passa (p 0,070).

A defasagem de um trimestre continua sendo o pico (t -2,13 em L1, -2,01 em L0, -1,73 em
L2) e a convencao de fechamento da Selic fica marginalmente melhor (t -2,23); a media
fica, por ser a que a (R) do simulador produz.

## A ressalva, e ela e real

As duas nao sao historias rivais -- correlacionam 0,767, e postas no mesmo ajuste
nenhuma sobrevive (inclinacao t -0,99, gap t -1,23). Mas elas se separam por
subamostra, e ali a inclinacao ganha: em 2016T3-2026T2 sem a pandemia (n 32) a
inclinacao da -0,105 (t -2,94) e o gap da -0,006 (t -0,44). A significancia do gap na
amostra cheia vem sobretudo de 2006-2016. **Isso vai na aba**, nao aqui.

## E o que decidiu: com a inclinacao, a Selic nunca chega ao produto

A inclinacao e feita de dois precos de mercado, entao uma (H) escrita com ela e uma
equacao ESPECTADORA dentro do simulador -- recebe premissa e nao recebe nada da regra de
juros. Com o gap, `(R) -> (H)` e elo de verdade, e e ele que, com a curva de Phillips,
fecha o laço `H -> I -> E -> R -> H` que o plano da pasta preve desde o comeco.

## Por que DEFASADO, e nao contemporaneo

O plano pedia `g(t)`. A defasagem de um trimestre e o pico nas DUAS convencoes de
trimestralizacao, o que e o que torna a escolha robusta em vez de garimpada. Duas razoes,
e as duas apontam para a defasada:

- **E a forma do proprio BC.** A eq. (2) do modelo agregado dele e
  `h = b1*h(-1) - b2*r_hat(-1)/4 - b3*rp_hat + ...`, com o juro real DEFASADO.
- **A contemporanea tem simultaneidade, e ela e visivel no dado.** A correlacao bruta do
  aperto com o hiato e POSITIVA em todas as medidas (+0,18 a +0,43), sinal trocado,
  porque o Copom aperta quando o hiato abre. Defasar quebra isso.
- **E com a media do trimestre ele nem seria predeterminado.** `gap(t)` na convencao de
  media esta dentro do trimestre que se quer explicar; `gap(t-1)` esta inteiro no passado.

A troca esta declarada na aba e a forma contemporanea continua estimada ao lado, em
`comparar()`, para a diferenca ser visivel em vez de argumentada.

## As outras definicoes de equilibrio continuam medidas, e continuam perdendo

`comparar_rr()` roda `r_ex_ante - RR*` para uma taxa fixa de 4,5%, para a neutra que o
BC declara e para um filtro HP com cauda Focus, mais as duas medidas acima. As duas
fixas entregam um `h2` indistinguivel de zero porque nao removem a tendencia do juro
real ex-ante, que cai de 12,2% em 2001T4 a -0,9% em 2020T4 e volta a 8,5% -- e o hiato
nao tem essa tendencia. O HP ajusta bem e e desqualificado por duas coisas que a tabela
nao mostra: ele e filtro de dois lados, entao para dizer qual era o equilibrio em 2010
usa dado de 2012, e o nivel dele hoje (7,7%) diria que a Selic de 15% quase nao aperta.
**O gap nao tem nenhum dos dois problemas**: Selic, NTN-B de 10 anos e meta sao tres
numeros observaveis no proprio trimestre, sem filtro e sem pesquisa.

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

# A coluna do painel que mede o aperto monetario. `gap_juro` desde 2026-09-25; `g_rr`,
# a inclinacao real 2a-10a, continua estimada ao lado em `comparar()`.
COL_APERTO = "gap_juro"

# Janelas de crise, as mesmas do modelo agregado do BC.
CRISES = {
    "d08": (pd.Period("2008Q4", "Q"), pd.Period("2009Q4", "Q")),
    "d20": (pd.Period("2020Q1", "Q"), pd.Period("2020Q4", "Q")),
}

# (parametro, coluna) -- a ordem e a da equacao
TERMOS = [("h1", "hiato_l1"), ("h2", "ap_l")]

ROT = {
    "h1": "Hiato do trimestre anterior",
    "h2": "Aperto monetário do trimestre anterior",
    "d08": "Crise financeira de 2008-2009",
    "d20": "Pandemia de 2020",
}


def montar(df: pd.DataFrame | None = None, col: str = COL_APERTO,
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
    d["ap_l"] = df[col].shift(lag)
    d["ap"] = df[col]
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
    "base":    dict(desc="A conta da página: a Selic contra a âncora, um trimestre atrás",
                    col="gap_juro", lag=1, dummies=True),
    "cont":    dict(desc="O mesmo aperto no trimestre corrente, como o plano pedia",
                    col="gap_juro", lag=0, dummies=True),
    "lag2":    dict(desc="O aperto de dois trimestres atrás",
                    col="gap_juro", lag=2, dummies=True),
    "fim":     dict(desc="Pela Selic do fechamento do trimestre, e não pela média",
                    col="gap_juro_fim", lag=1, dummies=True),
    "incl":    dict(desc="A inclinação real 2 anos menos 10 anos no lugar da Selic",
                    col="g_rr", lag=1, dummies=True),
    "sem_cri": dict(desc="Sem as duas crises marcadas",
                    col="gap_juro", lag=1, dummies=False),
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
        cols = ["hiato", "hiato_l1", "ap_l"] + (list(CRISES) if v["dummies"] else [])
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
    from analytics.brasil.structural_model.modelo_agregado.modelo_painel import (
        focus_ipca_12m, focus_selic_12m)
    return (focus_selic_12m() - focus_ipca_12m()).dropna()


def comparar_rr(df: pd.DataFrame | None = None) -> list[dict]:
    """h2 sob cada definicao de RR*, mais a inclinacao, na mesma amostra comum."""
    from analytics.brasil.structural_model.modelo_agregado.modelo_painel import cauda_juro_real, hp

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
        ("gap", "a Selic contra o juro nominal de equilíbrio, a mesma âncora da regra "
                "de juros", df["gap_juro"]),
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
        d["ap_l"] = g.shift(LAG_GRR)
        rr = estimar(d.loc[comum])
        # `h2` sozinho nao compara duas medidas de dispersao diferente -- o gap tem
        # desvio 2,60 e a inclinacao 1,02. Por isso a tabela carrega tambem o efeito
        # por DESVIO da propria medida, que e o numero que se le lado a lado.
        sd = float(d.loc[comum, "ap_l"].std())
        out.append({"key": k, "desc": desc, "escolhida": k == "gap",
                    "h2": float(rr["coef"]["h2"]), "t": float(rr["t"]["h2"]),
                    "sd": sd, "h2_dp": float(rr["coef"]["h2"] * sd),
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
