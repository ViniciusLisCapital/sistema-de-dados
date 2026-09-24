# -*- coding: utf-8 -*-
"""Equacao (R) do modelo estrutural -- a regra de juros.

    (R) R(t) = r1*R(t-1) + r1b*R(t-2) + (1-r1-r1b)*(RR*(t) + Meta(t))
               + r2*dI(t) + d08 + d20 + eps

`R` e a Selic media do trimestre, `RR*` uma taxa real de equilibrio, `Meta` a meta de
inflacao no horizonte de 12 meses e `dI` o desvio da inflacao esperada em relacao a
meta, medido na Focus de **18 meses**. A equacao diz duas coisas: o Copom move a taxa aos poucos (`r1`), e para onde ele
a leva quando a inflacao esperada esta na meta e `RR* + Meta`.

## A restricao e IMPOSTA, nao testada

O peso da ancora e `1 - r1 - r1b` por construcao, e a forma de impor isso e regredir o
DESVIO em relacao a ancora contra ele mesmo defasado:

    y(t) = r1*y(t-1) + r1b*y(t-2) + r2*dI(t) + ... + eps,  y = R - RR* - Meta

sem intercepto. Os coeficientes que saem ja sao `r1` e `r1b`, e o peso da ancora fica
sendo o resto sem precisar ser estimado. `repouso()` confere numericamente as duas consequencias: com
`dI = 0` a Selic converge para `RR* + Meta`, partindo de onde for, e o efeito de longo
prazo de um desvio permanente bate com a formula.

## RR*: o juro real de 10 anos, SEM media movel (decisao do usuario, 2026-09-21)

Duas decisoes, nesta ordem. Primeiro *"rr_star estou pensando em usar aqui uma media
movel da taxa de juros real de 10 anos"*, o que fixou a serie em `rr_10a` -- a NTN-B de
120 meses, a mesma ponta longa que a equacao (H) usa. Depois, vista a tabela abaixo,
*"nao quero perder essa amostra agora. Portanto, por hora vamos manter a relacao sem
media movel"*. Entao `MM_RR = 1`, que e a serie crua.

O que a tabela mostrava, e que e o porque de a escolha ter sido um trade-off e nao uma
preferencia. `corr(RR*, aperto)` e contra `g_rr`, a inclinacao da curva real que a
equacao (H) usa como medida de aperto monetario; as colunas de estimativa estao na
amostra comum as sete linhas, que a media de 7 anos limita a 53 trimestres
(2013T2-2026T2). A coluna `comeca em` e o inicio da amostra PROPRIA de cada janela,
ja com as duas defasagens:

    janela      corr(RR*, aperto)  nivel hoje  comeca em    lp    Q(4)
    crua (em uso)     +0,80          7,67%      2006T3      2,83   0,981
    MM4               +0,76          7,54%      2007T2      2,52   0,187
    MM8               +0,63          7,29%      2008T2      2,69   0,074
    MM12              +0,38          6,76%      2009T2      2,93   0,059
    MM16              +0,18          6,57%      2010T2      3,07   0,082
    MM20              -0,06          6,30%      2011T2      3,17   0,041
    MM28              -0,35          5,46%      2013T2      3,09   0,032

**O custo de suavizar e amostra**: a media de 5 anos, que e onde a correlacao com o
ciclo zera, precisa de 20 trimestres de NTN-B e por isso comeca em 2011T2 -- 19
trimestres a menos, e a crise de 2008 inteira fora, com a dummy `d08` perdendo suporte.
Ela ja perde suporte na media de 4 anos, nao so na de 5.
**O custo de nao suavizar e conceitual**: com a serie crua a RR* correlaciona +0,80 com
o aperto monetario, entao a ancora `RR* + Meta` se move junto com a propria politica e a
regra subestima o quanto ela esta apertada. E o mesmo defeito que reprovou o filtro HP
como RR* na equacao (H), e continua valendo -- fica registrado como pendencia, nao
resolvido.

O que a decisao comprou, medido depois de tomada: as duas dummies de crise voltam a ter
suporte e ficam firmes (t -2,50 e -4,82; da media de 4 anos em diante a de 2008 nem e
estimada, por nao ter nenhum trimestre na amostra), e o residuo fica **o mais limpo da
tabela por larga margem** -- Q(4) p 0,981, contra 0,041 com a media de 5 anos, que ja
rejeitaria a 5%. Na amostra PROPRIA de cada janela, a de 5 anos e a unica das sete que
rejeita (p 0,014) e a base da p 0,683. A amostra maior nao custou ajuste: melhorou os
dois diagnosticos ao mesmo tempo, e a serie crua deixou de ser a escolha de compromisso
para ser a melhor linha da tabela em residuo.

Note que a coluna `lp` acima esta na amostra comum as sete janelas (53 trimestres, que a
media de 7 anos limita); na amostra propria de 80 a forma base da **2,62**.

A tabela continua no modulo e vai para a pagina: a escolha e reversivel trocando uma
constante, e o que ela custa tem de estar visivel.

## dI: a Focus de 18 meses, e as outras duas ao lado

    dI_focus2a  Focus IPCA de 18 meses - meta 24m     <- a BASE
    dI_focus    Focus IPCA 12 meses - meta 12m        <- o que o BC usa
    dI_bcb      projecao do proprio Copom no horizonte relevante - meta 12m

Escolha do usuario em 2026-09-21, depois de as tres serem medidas: *"vamos usar o Focus
18 meses por enquanto, e deixa anotado nas pendencias para olharmos o de 12 meses
novamente."* O "por enquanto" esta como pendencia R5.

**Um objeto, dois nomes, e os dois estao certos.** O BC publica esta serie como "IPCA 24
meses a frente": e a inflacao acumulada em DOZE meses terminando daqui a vinte e quatro,
ou seja a janela [12, 24) meses. O CENTRO dela esta a **18 meses**, que e o horizonte
efetivo -- e e por isso que interpolar a curva anual do Focus acerta em h=1,5 ano. A tela
diz "18 meses", que e o horizonte; as colunas do painel (`pi_e_2a`, `meta_24m`) usam o
nome da fonte, que e o que se procura para conferir contra o BC.

A serie rolante publicada so comeca em **2021-03-31**, entao a do painel e reconstruida da
pesquisa ANUAL do Focus, que vai a 2000. Ela reproduz a publicada com erro medio de 0,071
p.p. nos 1.370 boletins em que as duas coexistem (ver `panel.focus_ipca_2a`). O trecho
2001-2021 nao tem gabarito, e isso e limitacao declarada, nao verificacao omitida.

O que a escolha do horizonte custa e compra, medido -- amostra comum as tres, 78
trimestres:

    dI                      r2      t     lp      R2c      RMSE    Q(4)
    Focus 18 meses (base)  0,312   2,20   2,36   0,9564   0,5458   0,535
    Focus 12 meses         0,263   3,15   1,78   0,9601   0,5217   0,625
    projecao do Copom      0,422   2,77   3,25   0,9590   0,5293   0,493

**O ajuste nao separa as tres**: 0,4% de R2 e 4,6% de RMSE entre a melhor e a pior, com
residuo limpo nas tres. O que separa e o efeito de longo prazo, e ali a de 18 meses fica
entre as outras duas.

A razao para a escolha nao esta nesta tabela, e sim na de baixo: **com a Focus de 18
meses os TRES parametros caem dentro dos intervalos que o BC publica**, o que nao
acontece com nenhuma das outras duas.

## O que NAO e comparavel com o numero publicado do BC, e o que e

A equacao (3) do boxe do BC poe o multiplicador DENTRO do colchete:

    i(t) = t1*i(t-1) + t2*i(t-2) + (1-t1-t2)*[rr + meta + t3*(pi^e - meta)] + eps

entao o `t3 = 2,03 [1,47; 2,64]` dele e o **efeito de longo prazo** de um desvio
permanente, nao o coeficiente contemporaneo. O nosso `r2` esta fora do colchete: o
objeto comparavel a `t3` e `r2 / (1 - soma das defasagens)`, e e ele que a pagina
imprime ao lado do publicado. Comparar `r2` com `t3` direto erraria por um fator de
`1 - t1 - t2 = 0,10`. Mesma classe do `h2` da equacao (H), que tambem nao era o `b2`
publicado.

Ja `r1` e `r1b` sao comparaveis direto com `t1` e `t2`, e a soma com `t1 + t2 = 0,90`.

E aqui esta o argumento que decidiu o horizonte de `dI`. Na forma base os tres objetos
comparaveis caem **dentro** dos intervalos publicados, os tres:

    parametro               nosso    BC publicado        com Focus 12m
    r1                     +1,434   +1,48 [1,41; 1,54]   +1,329  FORA
    r1b                    -0,570   -0,58 [-0,63; -0,52] -0,482  FORA
    efeito de longo prazo   2,62     2,03 [1,47; 2,64]    1,78   dentro
    soma das defasagens     0,865    0,90 (sem IC)        0,853

Com a Focus de 12 meses so o efeito de longo prazo entrava; os dois pesos de suavizacao
ficavam fora pelo lado de baixo. Trocar o horizonte da expectativa por um mais longo
alongou tambem a suavizacao estimada, e as tres pecas caem no lugar ao mesmo tempo.

**Duas ressalvas para nao superler isso.** O efeito de longo prazo, 2,62, encosta no teto
do intervalo (2,64) -- com margem propria ele certamente cruzaria a borda, e essa margem
ainda nao e calculada (pendencia R8). E o ajuste piora um pouco contra a Focus de 12
meses: R2 centrado 0,952 contra 0,957, RMSE 0,566 contra 0,537. Cair dentro de tres
intervalos publicados nao e o mesmo que ajustar melhor, e as duas coisas nao apontam para
o mesmo lado aqui.

## Duas defasagens, e a de uma so fica ao lado -- promovida em 2026-09-21

O plano punha uma defasagem na base e a de duas como *"coluna de robustez"*. A coluna de
robustez venceu todos os diagnosticos, e o usuario promoveu-a: *"pode colocar as duas
defasagens"*. A forma de uma continua medida, agora do outro lado da tabela.

O que decidiu, cada forma na sua amostra propria:

                              uma defasagem   duas defasagens    BC publicado
    n                              81              80
    soma das defasagens          0,849           0,865            0,90
    efeito de longo prazo         3,75            2,62        2,03 [1,47; 2,64]
    R2 centrado                  0,912           0,952
    RMSE                         0,763           0,566
    autocorrelacao do residuo     0,61           -0,00
    Ljung-Box Q(4)              p = 0,000       p = 0,683
    Ljung-Box Q(8)              p = 0,000       p = 0,438

Com uma defasagem so o residuo carrega 0,61 de autocorrelacao de primeira ordem e o
Ljung-Box rejeita nos dois horizontes -- nao e rejeicao de fronteira, e a conta nao
capturando a dinamica de suavizacao. Com duas, o residuo fica **indistinguivel de ruido
branco**.

E o perfil em corcova aparece sozinho: `r1 = +1,434` (t 14,0) e `r1b = -0,570` (t -5,5),
os dois **dentro** dos intervalos que o BC publica para `t1` e `t2`. Vindo de um
estimador completamente diferente do dele (MQ de equacao unica contra filtro de Kalman
bayesiano), e mais do que se poderia exigir. A soma, 0,865, fica um pouco abaixo dos 0,90
dele -- e o unico dos quatro numeros que nao encosta.

## Fora daqui, por decisao ou por escopo

- **Vintage**: a Selic e observada em tempo real e nao e revista, entao o problema que a
  equacao (H) tem com o hiato nao existe aqui. Ja `RR*` e uma media movel de dado de
  mercado, tambem nunca revisto. Esta e a unica das quatro equacoes sem pendencia de
  vintage.
- **A escolha de RR*** nao e robustez desta equacao: e uma premissa, e uma premissa que
  desloca os coeficientes porque a regressao nao tem intercepto para absorve-la. A
  tabela de janelas mede o tamanho disso: 2,2 p.p. de nivel entre a ponta crua e a media
  de 7 anos, e 0,61 de efeito de longo prazo (era 1,58 com uma defasagem so).
- **Sem termo de hiato** na regra. O BC tambem nao poe, e o plano nao pede.

Uso:
    uv run python -m analytics.brasil.structural_model.equations.taylor
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_ljungbox

from analytics.brasil.structural_model import panel
from analytics.brasil.structural_model.equations.is_curve import _meia_vida

HAC_LAGS = 4
# Janela da media movel de `rr_10a` que define RR*, em trimestres. 1 = sem media, a
# serie crua -- decisao do usuario em 2026-09-21, para nao perder amostra. Ver a
# docstring: a media de 5 anos limparia a correlacao com o ciclo e custaria 19
# trimestres, entre eles a crise de 2008 inteira.
MM_RR = 1
# Defasagens da Selic na coluna BASE. O plano mandava uma e a de duas era "coluna de
# robustez"; ela venceu todos os diagnosticos e o usuario promoveu-a em 2026-09-21
# (*"pode colocar as duas defasagens"*). A de uma continua medida ao lado, em `COMPARAR`.
LAGS = 2

CRISES = {"d08": (pd.Period("2008Q4", "Q"), pd.Period("2009Q4", "Q")),
          "d20": (pd.Period("2020Q1", "Q"), pd.Period("2020Q4", "Q"))}

# coluna do painel -> nome do desvio, para as tres leituras de dI
# Um nome, dois rotulos, e vale saber por que os dois estao certos. O BC publica esta
# serie como "IPCA 24 meses a frente": e a inflacao acumulada em DOZE meses terminando
# daqui a vinte e quatro, ou seja a janela [12, 24) meses. O CENTRO dessa janela esta a
# 18 meses, e e por isso que a interpolacao da curva anual acerta em h=1,5 ano. O
# usuario chama de "Focus 18 meses" (o horizonte efetivo) e a fonte chama de "24 meses"
# (o fim da janela). A tela usa o termo do usuario; as colunas do painel e a `meta_24m`
# usam o da fonte, que e o que se procura para conferir contra o BC.
DI = {
    "focus":   ("pi_e",    "meta_12m", "Focus de 12 meses contra a meta"),
    "focus2a": ("pi_e_2a", "meta_24m", "Focus de 18 meses contra a meta"),
    "bcb":     ("pi_bcb",  "meta_12m", "Projeção do próprio Copom contra a meta"),
}
# Escolhido pelo usuario em 2026-09-21: *"vamos usar o Focus 18 meses por enquanto"*.
# O "por enquanto" esta anotado como pendencia -- a de 12 meses e a que o BC usa na
# equacao (3) dele, e volta a ser olhada.
DI_BASE = "focus2a"

ROT = {
    "r1":  "Juros do trimestre anterior",
    "r1b": "Juros de dois trimestres atrás",
    "r2":  "Inflação esperada acima da meta",
    "d08": "Crise de 2008",
    "d20": "Pandemia",
}

# Os numeros publicados da equacao (3) do boxe do BC, importados e nao transcritos --
# duas copias divergiriam. `t3` e efeito de LONGO PRAZO; ver a docstring.
from analytics.brasil.monetary_policy import modelo_agregado as _mp  # noqa: E402

BCB = {k: _mp.BCB[k] for k in ("t1", "t2", "t3")}
BCB_IC = {k: _mp.BCB_IC[k] for k in ("t1", "t2", "t3")}
BCB_SOMA = BCB["t1"] + BCB["t2"]


def rr_star(df: pd.DataFrame, k: int = MM_RR) -> pd.Series:
    """RR* = media movel de `k` trimestres do juro real de mercado de 10 anos.

    `k = 1` devolve a serie crua, que e a forma em uso -- `rolling(1).mean()` e a
    identidade, entao a tabela de janelas compara o cru e as medias pelo mesmo caminho
    de codigo em vez de por um ramo separado.
    """
    return df["rr_10a"].rolling(k).mean()


def montar(df: pd.DataFrame | None = None, k: int = MM_RR, lags: int = LAGS,
           di: str = DI_BASE) -> pd.DataFrame:
    """Painel -> matriz de regressao da equacao (R).

    So trimestres FECHADOS entram, pela coluna `completo` do painel.

    A coluna `y` ja e o desvio em relacao a ancora `RR* + Meta`: e ela, e nao a Selic,
    que a regressao explica. E por isso que `1 - r1` nao precisa ser estimado.
    """
    if df is None:
        df = panel.construir()
    df = df[df["completo"].astype(bool)].copy()

    col_pi, col_meta, _ = DI[di]
    ancora = rr_star(df, k) + df["meta_12m"]

    d = pd.DataFrame(index=df.index)
    d["selic"] = df["selic"]
    d["rr_star"] = rr_star(df, k)
    d["ancora"] = ancora
    d["y"] = df["selic"] - ancora
    for i in range(1, lags + 1):
        d["r1" if i == 1 else "r1b"] = d["y"].shift(i)
    d["r2"] = df[col_pi] - df[col_meta]
    for nome, (a, b) in CRISES.items():
        d[nome] = ((d.index >= a) & (d.index <= b)).astype(float)
    return d


def estimar(d: pd.DataFrame | None = None, lags: int = LAGS,
            dummies: bool = True) -> dict:
    """Estima (R) por MQ sem intercepto sobre o desvio, com erro-padrao HAC."""
    if d is None:
        d = montar(lags=lags)

    reg = ["r1"] + (["r1b"] if lags == 2 else []) + ["r2"]
    am = d[["y"] + reg + list(CRISES)].dropna()

    # Uma dummy sem NENHUM trimestre na amostra nao e um efeito estimado em zero: e uma
    # coluna de zeros, que devolve coeficiente 0,000 com t indefinido e suja a tabela.
    # Com RR* de 5 anos a amostra comeca em 2011 e `d08` cai exatamente nisso.
    usadas = [c for c in CRISES if dummies and am[c].sum() > 0]
    fora = [c for c in CRISES if dummies and am[c].sum() == 0]
    cols = reg + usadas

    yv = am["y"].to_numpy(float)
    Xv = am[cols].to_numpy(float)
    res = sm.OLS(yv, Xv).fit(cov_type="HAC", cov_kwds={"maxlags": HAC_LAGS})

    coef = dict(zip(cols, res.params))
    obs = am["y"]
    fit = pd.Series(Xv @ res.params, index=am.index)
    resid = obs - fit
    e = resid.to_numpy(float)
    sst = float(((obs - obs.mean()) ** 2).sum())
    ssr = float((e ** 2).sum())
    n, kk = len(obs), Xv.shape[1]
    lbt = acorr_ljungbox(e, lags=[4, 8], return_df=True)

    phis = [float(coef["r1"])] + ([float(coef["r1b"])] if lags == 2 else [])
    soma = float(sum(phis))
    livre = 1.0 - soma
    lp = float(coef["r2"] / livre) if abs(livre) > 1e-9 else None

    return {
        "estimador": "MQ sem intercepto sobre o desvio, erro-padrão HAC(%d)" % HAC_LAGS,
        "hac_lags": HAC_LAGS, "lags": lags, "mm_rr": MM_RR,
        "n": n, "k": kk, "ini": am.index[0], "fim": am.index[-1],
        "coef": coef,
        "se": dict(zip(cols, res.bse)),
        "t": dict(zip(cols, res.tvalues)),
        "p": dict(zip(cols, res.pvalues)),
        "t_ols": dict(zip(cols, sm.OLS(yv, Xv).fit().tvalues)),
        "termos": reg, "dummies": usadas, "dummies_fora": fora,
        "phis": phis, "soma": soma,
        "estavel": bool(abs(soma) < 1.0),
        "meia_vida": _meia_vida(phis),
        "efeito_lp": lp,
        "r2_cent": 1.0 - ssr / sst,
        "r2_ajustado": 1.0 - (1.0 - ssr / sst) * (n - 1) / (n - kk),
        "rmse": float(np.sqrt(ssr / n)),
        "erro_medio": float(np.abs(e).mean()),
        "acf": [float(pd.Series(e).autocorr(lag)) for lag in range(1, 7)],
        "lb_q4": float(lbt["lb_stat"].iloc[0]), "lb_p4": float(lbt["lb_pvalue"].iloc[0]),
        "lb_q8": float(lbt["lb_stat"].iloc[1]), "lb_p8": float(lbt["lb_pvalue"].iloc[1]),
        "idx": am.index, "obs": obs, "fit": fit, "resid": resid,
        "selic": d["selic"].reindex(am.index),
        "ancora": d["ancora"].reindex(am.index),
        "rr_star": d["rr_star"].reindex(am.index),
        "selic_ajustada": d["ancora"].reindex(am.index) + fit,
    }


def rotulo(par: str) -> str:
    """Nome legivel de um parametro, para a tela nao imprimir `r1`."""
    return ROT.get(par, par)


def repouso(r: dict) -> dict:
    """Confere NUMERICAMENTE o que a restricao imposta afirma.

    Duas propriedades, as duas simuladas em vez de argumentadas:

    1. **Com a inflacao esperada na meta, a Selic converge para `RR* + Meta`.** E o
       estado estacionario que a forma restrita promete, e ele so existe porque a soma
       das defasagens e menor que 1 -- por isso a estabilidade e conferida antes.
    2. **O efeito de longo prazo de um desvio permanente de 1 p.p.** bate com a formula
       `r2 / (1 - soma)`, que e o objeto comparavel ao `t3` publicado.
    """
    phis, r2 = r["phis"], r["coef"]["r2"]
    soma = float(sum(phis))
    if abs(soma) >= 1.0:
        raise AssertionError("soma das defasagens = %.4f: a regra nao converge" % soma)

    def rodar(di: float, y0: float) -> float:
        hist = [y0] * len(phis)
        for _ in range(4000):
            hist.append(sum(p * hist[-i - 1] for i, p in enumerate(phis)) + r2 * di)
        return hist[-1]

    for y0 in (-5.0, -1.0, 1.0, 8.0):
        if abs(rodar(0.0, y0)) > 1e-8:
            raise AssertionError("com dI=0 o desvio nao zera partindo de %.1f" % y0)
    sim = rodar(1.0, 0.0)
    if r["efeito_lp"] is not None and abs(sim - r["efeito_lp"]) > 1e-6:
        raise AssertionError("efeito simulado %.6f != formula %.6f"
                             % (sim, r["efeito_lp"]))
    return {"volta_a_ancora": True, "efeito_simulado": float(sim),
            "efeito_formula": r["efeito_lp"],
            "bc_t3": BCB["t3"], "bc_t3_ic": list(BCB_IC["t3"]),
            "dentro_do_ic": bool(BCB_IC["t3"][0] <= sim <= BCB_IC["t3"][1])}


# As leituras alternativas medidas ao lado. Nenhuma e a especificacao: elas existem para
# a pagina poder mostrar o que a escolha custou, em vez de a afirmar.
COMPARAR = {
    "base":    dict(desc="A conta da página: duas defasagens, Focus de 18 meses",
                    lags=2, di="focus2a", dummies=True),
    "foc12":   dict(desc="O desvio medido na Focus de 12 meses",
                    lags=2, di="focus", dummies=True),
    "lag1":    dict(desc="Com uma defasagem só, como o plano pedia",
                    lags=1, di="focus2a", dummies=True),
    "bcb":     dict(desc="O desvio que o próprio Copom projetava",
                    lags=2, di="bcb", dummies=True),
    "sem_cri": dict(desc="Sem as duas crises marcadas",
                    lags=2, di="focus2a", dummies=False),
}


def comparar(df: pd.DataFrame | None = None) -> dict:
    """As leituras de COMPARAR na mesma amostra comum, para serem comparaveis.

    Sem a amostra comum a tabela mentiria: a leitura com duas defasagens perde um
    trimestre a mais, e um R2 medido em janela diferente nao se compara com o de cima.
    """
    if df is None:
        df = panel.construir()
    montadas = {k: montar(df, lags=v["lags"], di=v["di"]) for k, v in COMPARAR.items()}

    comum = None
    for k, v in COMPARAR.items():
        reg = ["r1"] + (["r1b"] if v["lags"] == 2 else []) + ["r2"]
        ix = montadas[k][["y"] + reg].dropna().index
        comum = ix if comum is None else comum.intersection(ix)

    out = {}
    for k, v in COMPARAR.items():
        r = estimar(montadas[k].loc[comum], lags=v["lags"], dummies=v["dummies"])
        r["desc"] = v["desc"]
        out[k] = r
    return out


# ── A tabela de janelas: o que a escolha de RR* custa ───────────────────────
JANELAS = [1, 4, 8, 12, 16, 20, 28]


def comparar_janela(df: pd.DataFrame | None = None) -> list[dict]:
    """A mesma equacao sob cada janela de media movel, na mesma amostra comum.

    Traz as duas metades da decisao na mesma linha: o que a janela faz com a estimativa,
    e o que ela faz com a propria RR* -- a correlacao com o aperto monetario, que e o
    criterio que decidiu, e o nivel de hoje, que e o que se pode confrontar com o 5,0%
    que o BC declara e com os ~6,45% da curva real descontado o premio.
    """
    if df is None:
        df = panel.construir()
    fechado = df[df["completo"].astype(bool)]

    # A intersecao tem de usar as MESMAS colunas que `estimar` exige, inclusive a
    # segunda defasagem. Sem `r1b` aqui, a janela mais longa perdia um trimestre a mais
    # dentro do `estimar` e a tabela dizia "mesma amostra" com 54 linhas em seis delas e
    # 53 na setima -- diferenca pequena e silenciosa, que e o pior tipo.
    cols = ["y", "r1", "r2"] + (["r1b"] if LAGS == 2 else [])
    comum = None
    for k in JANELAS:
        ix = montar(df, k=k)[cols].dropna().index
        comum = ix if comum is None else comum.intersection(ix)

    out = []
    for k in JANELAS:
        rr = rr_star(fechado, k)
        j = pd.concat([rr.rename("rr"), fechado["g_rr"]], axis=1).dropna()
        r = estimar(montar(df, k=k).loc[comum])
        out.append({
            "k": k, "escolhida": k == MM_RR,
            "rot": ("Sem média, a série crua" if k == 1
                    else "Média de %d ano%s" % (k // 4, "" if k == 4 else "s")),
            "corr_aperto": float(j["rr"].corr(j["g_rr"])),
            "nivel_hoje": float(rr.dropna().iloc[-1]),
            "inicio_livre": str(montar(df, k=k)[cols].dropna().index[0]),
            "r1": float(r["coef"]["r1"]), "t_r1": float(r["t"]["r1"]),
            "r2": float(r["coef"]["r2"]), "t_r2": float(r["t"]["r2"]),
            "efeito_lp": r["efeito_lp"], "r2_cent": r["r2_cent"],
            "lb_p4": r["lb_p4"], "n": r["n"],
        })
    return out


def _dentro(v: float, ic: tuple) -> str:
    return "dentro" if ic[0] <= v <= ic[1] else "FORA"


def main() -> None:
    df = panel.construir()
    r = estimar(montar(df))
    rep = repouso(r)

    print("=" * 78)
    print("(R) a regra de juros -- %s" % r["estimador"])
    print("    RR* = %s" % ("o juro real de mercado de 10 anos, sem média móvel"
                              if MM_RR == 1 else
                              "média móvel de %d trimestres do juro real de 10 anos" % MM_RR))
    print("    dI  = %s" % DI[DI_BASE][2])
    print("    amostra %s -> %s, %d trimestres" % (r["ini"], r["fim"], r["n"]))
    if r["dummies_fora"]:
        print("    fora por falta de suporte na amostra: %s" % ", ".join(r["dummies_fora"]))
    print()
    print("  %-34s %9s %9s %9s" % ("", "coef", "t (HAC)", "p"))
    for c in r["termos"] + r["dummies"]:
        print("  %-34s %9.4f %9.2f %9.3f"
              % (rotulo(c), r["coef"][c], r["t"][c], r["p"][c]))
    print()
    print("  soma das defasagens       %.4f   (BC publica %.2f)" % (r["soma"], BCB_SOMA))
    print("  meia-vida de um desvio    %s trimestres" % r["meia_vida"])
    print("  efeito de longo prazo     %.3f   (BC publica t3 = %.2f [%.2f; %.2f]) %s"
          % (r["efeito_lp"], BCB["t3"], BCB_IC["t3"][0], BCB_IC["t3"][1],
             "DENTRO" if rep["dentro_do_ic"] else "fora"))
    print("  R2 centrado               %.3f      RMSE %.3f p.p." % (r["r2_cent"], r["rmse"]))
    print("  Ljung-Box Q(4)            p = %.3f   Q(8) p = %.3f" % (r["lb_p4"], r["lb_p8"]))
    print("  repouso: com dI=0 a Selic volta para RR* + Meta  ->  %s" % rep["volta_a_ancora"])

    print()
    print("-- a janela da média móvel (mesma amostra) " + "-" * 34)
    print("  %-16s %7s %9s %8s %8s %8s %7s"
          % ("", "corr c/", "RR* hoje", "r1", "r2", "efeito", "LB(4)"))
    print("  %-16s %7s %9s %8s %8s %8s %7s"
          % ("", "aperto", "", "", "", "longo pz", "p"))
    for l in comparar_janela(df):
        print("  %-16s %+7.2f %8.2f%% %8.3f %8.3f %8.2f %7.3f%s"
              % (l["rot"], l["corr_aperto"], l["nivel_hoje"], l["r1"], l["r2"],
                 l["efeito_lp"], l["lb_p4"], "  <--" if l["escolhida"] else ""))

    print()
    print("-- formas testadas (mesma amostra comum) " + "-" * 36)
    comp = comparar(df)
    print("  %-52s %8s %8s %8s %7s" % ("", "r1", "r2", "efeito", "LB(4)"))
    for k, c in comp.items():
        print("  %-52s %8.3f %8.3f %8.2f %7.3f%s"
              % (c["desc"], c["coef"]["r1"], c["coef"]["r2"], c["efeito_lp"],
                 c["lb_p4"], "  <--" if k == "base" else ""))
    print()
    print("  a forma base, parametro a parametro contra o que o BC publica:")
    print("    r1   = %+.3f   (BC t1 = %+.2f [%.2f; %.2f])  %s"
          % (r["coef"]["r1"], BCB["t1"], BCB_IC["t1"][0], BCB_IC["t1"][1],
             _dentro(r["coef"]["r1"], BCB_IC["t1"])))
    print("    r1b  = %+.3f   (BC t2 = %+.2f [%.2f; %.2f])  %s"
          % (r["coef"]["r1b"], BCB["t2"], BCB_IC["t2"][0], BCB_IC["t2"][1],
             _dentro(r["coef"]["r1b"], BCB_IC["t2"])))
    print("    soma = %+.3f   (BC %.2f)" % (r["soma"], BCB_SOMA))
    print("    efeito de longo prazo = %.2f   (BC t3 = %.2f [%.2f; %.2f])  %s"
          % (r["efeito_lp"], BCB["t3"], BCB_IC["t3"][0], BCB_IC["t3"][1],
             _dentro(r["efeito_lp"], BCB_IC["t3"])))
    print("=" * 78)


if __name__ == "__main__":
    main()
