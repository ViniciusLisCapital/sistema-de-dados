"""A curva de Phillips desagregada nos quatro subindices do IPCA, em inflacao trimestral.

    (IS) IS(t) = is1*IS(t-1) + is1b*MM4(IS)(t-1) + (1-is1-is1b)*E(t-1)/4
                             + is2*H(t)                                       + saz
    (IA) IA(t) = ia1*IA(t-1) + (1-ia1)*E(t-1)/4
                             + ia2*IAGR(t) + ia3*F(t) + ia4*H(t)              + saz
    (II) II(t) = ii1*II(t-1) + ii1b*MM4(II)(t-1) + (1-ii1-ii1b)*E(t-1)/4
                             + ii2*IMET(t) + ii3*IMET(t-1) + ii4*F(t-1) + ii5*H(t) + saz
    (IM) IM(t) = im1*IM(t-1) + im2*I(t-1) + (1-im1-im2)*E(t-1)/4              + saz

    IS  pi_is_q   servicos           IA  pi_ia_q   alimentacao
    II  pi_ii_q   bens industriais   IM  pi_im_q   monitorados
    I   pi_q      IPCA cheio do trimestre -- so como ANCORA da indexacao em (IM)
    IAGR pi_agr_usd   IMET pi_met_usd   E pi_e (anual, entra /4)   H hiato   F de

Tudo em inflacao DO TRIMESTRE, em %, nao anualizada. Ver o `panel.py` para por que
a metrica e essa e nao acumulado em doze meses nem trimestre anualizado.

## A restricao, e como ela e imposta

Os pesos da inercia e da expectativa somam 1: a inflacao e media ponderada de passado e
expectativa, mais os choques. Impor isso DEPOIS de estimar descartaria informacao; impor
ANTES e reparametrizacao exata -- regride-se o desvio contra o desvio, SEM INTERCEPTO:

    IS(t) - E(t-1)/4 = is1*[IS(t-1) - E(t-1)/4] + is1b*[MM4(t-1) - E(t-1)/4]
                     + is2*H(t) + saz + e

Em (IS) e (II) ha DOIS termos dentro da restricao (a defasagem e a media movel) e em
(IM) tambem (a defasagem e a indexacao); o peso da expectativa e o que sobra de um.

## As dummies de trimestre, e por que soma-zero nao e convencao

A inflacao trimestral e sazonal: medido, o padrao explica 20% da variancia do cheio e
**32% da de servicos**, com amplitude de 3,9 p.p. anualizados no cheio e 10,3 em
alimentacao. Deixar isso no residuo joga o padrao -- que e autocorrelacionado -- direto
no coeficiente de inercia.

A codificacao e `1{Q=q} - 1{Q=4}`, tres colunas, e o quarto efeito e `-(s1+s2+s3)`.
Com ela os QUATRO efeitos somam zero dentro do ano, e e isso que preserva a restricao:
com dummies indicadoras comuns o estado estacionario viraria `E/4 + s_Q`, diferente em
cada trimestre e igual a expectativa em nenhum.

E a soma-zero e **implicada pela estrutura**, nao imposta a gosto. Escreva
`I(t) = I~(t) + sigma_q` com `I~` dessazonalizada e `sigma` o efeito deterministico do
trimestre; substituindo na equacao, o termo sazonal que sobra e
`s_q = sigma_q - i1*sigma_{q-1}`, e como `sigma` soma zero no ano, `s` tambem soma.

Corolario que a pagina tem de dizer: os coeficientes estimados **nao sao** a sazonalidade
da inflacao -- sao o padrao LIQUIDO do que a inercia ja propaga.

## Por que a media movel de 4 trimestres esta em (IS) e (II)

Nao foi copiada do BC, foi medida. (IS) era a unica equacao cujo residuo rejeitava
Ljung-Box (Q(4) = 19,1, p 0,0007), com o pico na defasagem 4. Acrescentando a MM4 da
propria inflacao dentro da restricao, o teste deixa de rejeitar (p 0,34), o R2 sobe de
0,546 para 0,626 -- e a **defasagem de um trimestre colapsa para 0,027 (t 0,23)**
enquanto a MM4 fica com 0,688 (t 4,73). A inercia de servicos nao e o trimestre passado,
e a media do ultimo ano. O hiato, que era t 3,47, vai a 5,07.

Em (II) as duas convivem: defasagem 0,542 (t 4,40) e MM4 0,266 (t 2,11), com o
Ljung-Box saindo de p 0,084 para 0,202. Em (IA) e (IM) a MM4 nao acrescenta nada
(t 0,83 e -1,03) e por isso nao entra. Bate com o BC, que poe media movel so na
equacao de servicos.

## Newey-West, agora por precaucao e nao por construcao

Na metrica de 12 meses o HAC era obrigatorio: a sobreposicao das janelas produzia MA(3)
mesmo com a especificacao perfeita. Aqui as janelas nao se sobrepoem e o Ljung-Box nao
rejeita em nenhuma das quatro equacoes -- o HAC(4) fica como margem conservadora, e a
tabela mostra o t de MQ ao lado para o leitor ver o quanto ele esta custando.

## A ancora da expectativa e o IPCA CHEIO nas quatro, e isso e uma restricao

`expc_focus` publica expectativa por subindice, mas so desde set/2021 -- 20 trimestres
contra os 91 da amostra. Entao a ancora das quatro e a do IPCA cheio, o que impoe que os
quatro convirjam ao MESMO numero: precos relativos constantes no longo prazo. Os dados
discordam, entao espera-se vies sistematico de sinal oposto em servicos e industriais.
E por isso que o residuo de cada uma tem de estar na tela.

## O que o modelo do BC faz, e onde esta especificacao difere

Fonte: "Novo modelo desagregado de pequeno porte", RI mar/2021, p.76-77 --
`referencia/modelo_agregado_bc/modelo_desagregado.pdf`.

- **O BC subtrai a meta da commodity e a deriva de PPC do cambio.** Aqui as duas entram
  brutas, por decisao explicita.
- **Os `A_t` sao passeios aleatorios nao observados**, um por setor, que acomodam a
  deriva de baixa frequencia das inflacoes setoriais. Sem eles -- que e o caso aqui --
  sobra vies sistematico de sinal oposto em servicos e industriais.
- **(II) do BC tem Brent** e **(IA) tem um bloco de clima**. Nao estao aqui.
- **O sazonal do BC e um filtro X-13 aplicado antes**; aqui e dummy dentro da equacao.
  A diferenca importa porque cinco filtros independentes quebram a aditividade: medido,
  a soma ponderada dos quatro reproduz o cheio com RMSE 0,025 no espaco cru e 0,086 no
  dessazonalizado por X-13 -- 3,4x pior, contra um piso de 0,025.
- **O sazonal de Q1 em servicos esta derivando**: -0,042 p.p. por ano (t -3,02). Uma
  dummy fixa e a aproximacao de ordem zero disso. O lugar certo da correcao e um sazonal
  estocastico no espaco de estados, junto com os `A_t` -- nao uma tendencia linear colada
  na regressao. Ver o CLAUDE.md da pasta.

Uso:
    uv run python -m analytics.brasil.structural_model.equations.phillips_sub
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.statespace.sarimax import SARIMAX

from analytics.brasil.structural_model import panel

warnings.filterwarnings("ignore")

# Defasagens do kernel de Bartlett. Ver a docstring: aqui e margem conservadora, nao
# correcao de um artefato de amostragem.
HAC_LAGS = 4

# As tres colunas soma-zero. A quarta e derivada: -(s1+s2+s3).
SAZ = ["s1", "s2", "s3"]
ROT_SAZ = {"s1": "1º trimestre", "s2": "2º trimestre",
           "s3": "3º trimestre", "s4": "4º trimestre"}

ORDEM = ["IS", "IA", "II", "IM"]

# Uma entrada por equacao. `inercia` e a defasagem propria; `restritos` sao os OUTROS
# termos que dividem a restricao com ela (a media movel, a indexacao); `regs` sao os
# choques, cujo valor de estado estacionario e zero por convencao.
EQUACOES = {
    "IS": dict(
        nome="Serviços",
        dep="pi_is_q",
        inercia="is1",
        restritos=[("is1b", "mm4_is", "Média dos 4 trimestres anteriores")],
        regs=[("is2", "hiato", "Hiato do produto")],
    ),
    "IA": dict(
        nome="Alimentação",
        dep="pi_ia_q",
        inercia="ia1",
        restritos=[],
        regs=[("ia2", "pi_agr_usd", "IC-Br agropecuária em dólar"),
              ("ia3", "de",         "Câmbio, mesmo trimestre"),
              ("ia4", "hiato",      "Hiato do produto")],
    ),
    "II": dict(
        nome="Bens industriais",
        dep="pi_ii_q",
        inercia="ii1",
        restritos=[("ii1b", "mm4_ii", "Média dos 4 trimestres anteriores")],
        regs=[("ii2", "pi_met_usd",    "IC-Br metálico em dólar"),
              ("ii3", "pi_met_usd_l1", "IC-Br metálico, defasado um trimestre"),
              ("ii4", "de_l1",         "Câmbio, defasado um trimestre"),
              ("ii5", "hiato",         "Hiato do produto")],
    ),
    "IM": dict(
        nome="Monitorados",
        dep="pi_im_q",
        inercia="im1",
        restritos=[("im2", "pi_q_l1", "Indexação ao IPCA cheio")],
        regs=[],
    ),
}

# As leituras possiveis do termo de commodity em (IA), testadas lado a lado. A eq. (2)
# do BC poe o IC-Br agropecuario SO defasado e o termo de duas defasagens esta na eq.
# (1), de bens industriais -- entao a referencia nao decide sozinha. `erro_ma1` e a
# outra leitura da frase "o BC poe um MA(1)": residuo MA(1) em vez de defasagem no
# regressor. E a unica que muda o estimador, e por isso o erro-padrao dela nao e HAC.
VARIANTES_IA = {
    "base": dict(
        desc="IC-Br agropecuário no mesmo trimestre (a especificação original)",
        regs=[("ia2", "pi_agr_usd", "IC-Br agropecuário em dólar")],
        erro_ma1=False,
    ),
    "defasagem_dist": dict(
        desc="IC-Br agropecuário em t e t-1 (a forma que o BC usa em bens industriais)",
        regs=[("ia2", "pi_agr_usd",     "IC-Br agropecuário em dólar"),
              ("ia2b", "pi_agr_usd_l1", "IC-Br agropecuário, defasado um trimestre")],
        erro_ma1=False,
    ),
    "so_defasado": dict(
        desc="IC-Br agropecuário só defasado (a forma literal da eq. (2) do BC)",
        regs=[("ia2", "pi_agr_usd_l1", "IC-Br agropecuário, defasado um trimestre")],
        erro_ma1=False,
    ),
    "erro_ma1": dict(
        desc="IC-Br no mesmo trimestre, com resíduo MA(1)",
        regs=[("ia2", "pi_agr_usd", "IC-Br agropecuário em dólar")],
        erro_ma1=True,
    ),
}

# As tres ancoras possiveis da indexacao em (IM), testadas lado a lado. Contrato de
# reajuste persegue inflacao de doze meses, entao as duas de horizonte longo sao as
# candidatas naturais -- e sao as que se comportam PIOR. Ver o CLAUDE.md.
ANCORAS_IM = {
    "trimestre": dict(desc="IPCA do trimestre anterior", col="pi_q_l1"),
    "doze_meses": dict(desc="IPCA acumulado em 12 meses, dividido por 4", col="mm4_pi"),
}


def _rotulo(chave: str, par: str) -> str:
    """Nome legivel de um parametro, para a tela nao imprimir `ia2`."""
    if par in ROT_SAZ:
        return ROT_SAZ[par]
    eq = EQUACOES[chave]
    if par == eq["inercia"]:
        return "Inércia (peso da inflação do trimestre anterior)"
    for p, _, rot in list(eq["restritos"]) + list(eq["regs"]):
        if p == par:
            return rot
    for v in VARIANTES_IA.values():
        for p, _, rot in v["regs"]:
            if p == par:
                return rot
    return par


def montar(df: pd.DataFrame | None = None) -> pd.DataFrame:
    """Painel -> matriz de regressao: defasagens, medias moveis e dummies de trimestre.

    So trimestres FECHADOS entram: a coluna `completo` do painel marca o trimestre da
    ponta, que carrega dois meses de IPCA e 2,5 de cambio. Um trimestre pela metade na
    ultima linha da amostra move coeficiente sem que nada no numero avise.
    """
    if df is None:
        df = panel.construir()
    df = df[df["completo"].astype(bool)].copy()

    d = pd.DataFrame(index=df.index)
    # a expectativa e ANUAL e entra na unidade do trimestre
    d["E4_l1"] = df["pi_e"].shift(1) / 4.0
    d["hiato"] = df["hiato"]
    d["de"] = df["de"]
    d["de_l1"] = df["de"].shift(1)
    for c in ("pi_agr_usd", "pi_met_usd"):
        d[c] = df[c]
        d[c + "_l1"] = df[c].shift(1)

    d["pi_q"] = df["pi_q"]
    d["pi_q_l1"] = df["pi_q"].shift(1)
    d["mm4_pi"] = df["pi_q"].rolling(4).mean().shift(1)
    for k in panel.CORTES:
        col = panel.SUB_COL[k]
        d[col] = df[col]
        d[col + "_l1"] = df[col].shift(1)
        d["mm4_" + k] = df[col].rolling(4).mean().shift(1)
        d[panel.PESO_COL[k]] = df[panel.PESO_COL[k]]

    qq = d.index.quarter
    for i in (1, 2, 3):
        d["s%d" % i] = (qq == i).astype(float) - (qq == 4).astype(float)
    return d


def _termos(chave: str, variante: str | None, ancora_im: str | None) -> tuple:
    """(restritos, regs, usa_ma1) depois de aplicar a variante pedida."""
    eq = EQUACOES[chave]
    restritos, regs, ma1 = list(eq["restritos"]), list(eq["regs"]), False
    if chave == "IA":
        v = VARIANTES_IA[variante or "base"]
        regs = list(v["regs"]) + [r for r in regs if not r[1].startswith("pi_agr")]
        ma1 = v["erro_ma1"]
    if chave == "IM" and ancora_im:
        a = ANCORAS_IM[ancora_im]
        restritos = [(p, a["col"], rot) for p, _, rot in restritos]
    return restritos, regs, ma1


def estimar_uma(d: pd.DataFrame, chave: str, com_saz: bool = True,
                idx: pd.Index | None = None, variante: str | None = None,
                ancora_im: str | None = None) -> dict:
    """Estima UMA das quatro equacoes.

    A restricao e imposta antes: regride-se `Ik(t) - E(t-1)/4` contra os desvios
    dos termos restritos, mais os choques e as dummies de trimestre, sem intercepto.
    O peso da expectativa e o que sobra de um.
    """
    eq = EQUACOES[chave]
    dep = eq["dep"]
    restritos, regs, ma1 = _termos(chave, variante, ancora_im)

    y = d[dep] - d["E4_l1"]
    X = pd.DataFrame({"__inercia": d[dep + "_l1"] - d["E4_l1"]})
    nomes = [eq["inercia"]]
    for i, (par, col, _) in enumerate(restritos):
        X["__r%d" % i] = d[col] - d["E4_l1"]
        nomes.append(par)
    for par, col, _ in regs:
        X[col] = d[col]
        nomes.append(par)
    if com_saz:
        for s in SAZ:
            X[s] = d[s]
            nomes.append(s)

    am = pd.concat([y.rename("__y"), X], axis=1).dropna()
    if idx is not None:
        am = am.loc[am.index.intersection(idx)]
    yv = am["__y"].to_numpy(float)
    Xv = am[X.columns].to_numpy(float)

    if ma1:
        # Maxima verossimilhanca com residuo MA(1). O erro-padrao deixa de ser HAC: a
        # correlacao serial passa a ser MODELADA em vez de corrigida, entao os dois
        # numeros respondem perguntas diferentes e a tabela tem de dizer qual e qual.
        from scipy.stats import norm
        res = SARIMAX(yv, exog=Xv, order=(0, 0, 1), trend="n",
                      enforce_invertibility=True).fit(disp=False)
        nk = Xv.shape[1]
        coef = dict(zip(nomes, res.params[:nk]))
        se = dict(zip(nomes, res.bse[:nk]))
        tst = dict(zip(nomes, res.params[:nk] / res.bse[:nk]))
        pvl = {k: float(2 * (1 - norm.cdf(abs(v)))) for k, v in tst.items()}
        t_ols = dict(tst)
        theta, theta_se = float(res.params[nk]), float(res.bse[nk])
    else:
        res = sm.OLS(yv, Xv).fit(cov_type="HAC", cov_kwds={"maxlags": HAC_LAGS})
        coef = dict(zip(nomes, res.params))
        se = dict(zip(nomes, res.bse))
        tst = dict(zip(nomes, res.tvalues))
        pvl = dict(zip(nomes, res.pvalues))
        t_ols = dict(zip(nomes, sm.OLS(yv, Xv).fit().tvalues))
        theta = theta_se = None

    dd = d.loc[am.index]
    peso_e = 1.0 - coef[eq["inercia"]]
    fit = coef[eq["inercia"]] * dd[dep + "_l1"]
    for par, col, _ in restritos:
        fit = fit + coef[par] * dd[col]
        peso_e -= coef[par]
    fit = fit + peso_e * dd["E4_l1"]
    for par, col, _ in regs:
        fit = fit + coef[par] * dd[col]
    if com_saz:
        for s in SAZ:
            fit = fit + coef[s] * dd[s]

    obs = dd[dep]
    resid = obs - fit
    e = resid.to_numpy(float)
    sst = float(((obs - obs.mean()) ** 2).sum())
    ssr = float((e ** 2).sum())
    n, kk = len(obs), Xv.shape[1]
    lbt = acorr_ljungbox(e, lags=[4, 8], return_df=True)

    # o longo prazo de um choque e beta / (peso da expectativa): em estado
    # estacionario os pesos restritos realimentam o proprio choque
    lp = {par: float(coef[par]) / peso_e for par, _, _ in regs} if peso_e else {}
    saz4 = None
    if com_saz:
        b = [float(coef[s]) for s in SAZ]
        saz4 = b + [-sum(b)]

    return {
        "chave": chave, "nome": eq["nome"], "com_saz": com_saz,
        "variante": (variante or "base") if chave == "IA" else None,
        "ancora_im": (ancora_im or "trimestre") if chave == "IM" else None,
        "ma1": ma1, "theta": theta, "theta_se": theta_se,
        "estimador": "MV, resíduo MA(1)" if ma1 else "MQ, erro-padrão HAC(%d)" % HAC_LAGS,
        "n": n, "k": kk, "ini": am.index[0], "fim": am.index[-1],
        "coef": coef, "se": se, "t": tst, "p": pvl, "t_ols": t_ols,
        "peso_expectativa": peso_e, "longo_prazo": lp, "saz": saz4,
        "restritos": restritos, "regs": regs,
        "r2": 1.0 - ssr / sst,
        "r2_ajustado": 1.0 - (1.0 - ssr / sst) * (n - 1) / (n - kk),
        "rmse": float(np.sqrt(ssr / n)),
        "acf": [float(pd.Series(e).autocorr(l)) for l in range(1, 7)],
        "lb_q4": float(lbt["lb_stat"].iloc[0]), "lb_p4": float(lbt["lb_pvalue"].iloc[0]),
        "lb_q8": float(lbt["lb_stat"].iloc[1]), "lb_p8": float(lbt["lb_pvalue"].iloc[1]),
        "idx": am.index, "obs": obs, "fit": fit, "resid": resid,
    }


def amostra_comum(d: pd.DataFrame, com_saz: bool = True,
                  variante_ia: str | None = None) -> pd.Index:
    """Trimestres em que as QUATRO equacoes tem todos os insumos.

    Estimar cada uma na amostra dela daria quatro periodos diferentes, e a soma
    ponderada deixaria de ser comparavel ao cheio nos trimestres em que faltasse uma.
    """
    idx = None
    for k in ORDEM:
        i = estimar_uma(d, k, com_saz,
                        variante=variante_ia if k == "IA" else None)["idx"]
        idx = i if idx is None else idx.intersection(i)
    return idx


def estimar(d: pd.DataFrame | None = None, com_saz: bool = True,
            variante_ia: str | None = None, ancora_im: str | None = None) -> dict:
    """As quatro equacoes na amostra comum, mais a reconstrucao do IPCA cheio."""
    if d is None:
        d = montar()
    idx = amostra_comum(d, com_saz, variante_ia)
    eqs = {k: estimar_uma(d, k, com_saz, idx=idx,
                          variante=variante_ia if k == "IA" else None,
                          ancora_im=ancora_im if k == "IM" else None)
           for k in ORDEM}

    w = {k: d.loc[idx, panel.PESO_COL[k.lower()]] for k in ORDEM}
    fit = sum(w[k] * eqs[k]["fit"].reindex(idx) for k in ORDEM)
    obs = d.loc[idx, "pi_q"]
    # a MESMA soma sobre os subindices REALIZADOS: o piso do erro de reconstrucao,
    # que e o que a identidade do IPCA deixa de fora ao agregar trimestre a trimestre
    agreg = sum(w[k] * eqs[k]["obs"].reindex(idx) for k in ORDEM)

    def _m(x):
        e = (x - obs).to_numpy(float)
        return {"rmse": float(np.sqrt((e ** 2).mean())),
                "r2": 1.0 - float((e ** 2).sum())
                      / float(((obs - obs.mean()) ** 2).sum()),
                "erro_medio": float(np.abs(e).mean()),
                "erro_max": float(np.abs(e).max())}

    return {
        "equacoes": eqs, "idx": idx, "com_saz": com_saz,
        "variante_ia": variante_ia or "base",
        "ancora_im": ancora_im or "trimestre",
        "cheio": {"obs": obs, "fit": fit, **_m(fit)},
        "erro_agregacao": {"serie": agreg, **_m(agreg)},
    }


def comparar_ia(d: pd.DataFrame, com_saz: bool = True) -> dict:
    """As quatro leituras do termo de commodity de (IA), na MESMA amostra."""
    idx = amostra_comum(d, com_saz)
    return {v: estimar_uma(d, "IA", com_saz, idx=idx, variante=v)
            for v in VARIANTES_IA}


def comparar_im(d: pd.DataFrame, com_saz: bool = True) -> dict:
    """As ancoras possiveis da indexacao de (IM), na MESMA amostra."""
    idx = amostra_comum(d, com_saz)
    return {a: estimar_uma(d, "IM", com_saz, idx=idx, ancora_im=a)
            for a in ANCORAS_IM}


def sem_sazonais(d: pd.DataFrame) -> dict:
    """O contrafactual que mede o que as dummies de trimestre valem, por equacao."""
    idx = amostra_comum(d, com_saz=True)
    return {k: estimar_uma(d, k, com_saz=False, idx=idx) for k in ORDEM}


def _print(r: dict) -> None:
    print("-" * 78)
    print("(%s) %s" % (r["chave"], r["nome"]))
    print("-" * 78)
    for par in r["coef"]:
        est = ("***" if r["p"][par] < .01 else "** " if r["p"][par] < .05
               else "*  " if r["p"][par] < .10 else "   ")
        print("  %-42s %8.4f %7.2f %s (MQ %6.2f)"
              % (_rotulo(r["chave"], par), r["coef"][par], r["t"][par], est,
                 r["t_ols"][par]))
    print("  %-42s %8.4f" % ("Peso da expectativa", r["peso_expectativa"]))
    if r["saz"]:
        print("  sazonais líquidos Q1..Q4: %s   (somam %.1e)"
              % (" ".join("%6.3f" % v for v in r["saz"]), sum(r["saz"])))
    print("  R2 %.4f   RMSE %.4f   n %d   Ljung-Box Q(4) %.2f p %.4f"
          % (r["r2"], r["rmse"], r["n"], r["lb_q4"], r["lb_p4"]))
    print("  ACF 1..6: %s" % " ".join("%6.3f" % v for v in r["acf"]))


# ── A leitura de 12 meses ───────────────────────────────────────
#
# A estimacao e trimestral, e e assim que ela tem de ser. Mas inflacao se le em doze
# meses, e um hiato de 0,09 por trimestre nao diz nada a quem pensa em 4,5% ao ano. As
# duas funcoes abaixo sao a TRADUCAO entre os dois espacos. Nao ha previsao nenhuma
# aqui, e a distincao importa: nada e simulado, nada realimenta, a defasagem e a media
# movel seguem sendo as REALIZADAS -- exatamente as mesmas da estimacao.
#
#   `acum12`      encadeia quatro trimestres de uma serie qualquer:
#                 (1+m1)(1+m2)(1+m3)(1+m4) - 1. Aplicado ao REALIZADO reproduz o IPCA de
#                 12 meses publicado com erro medio de 0,0024 p.p. (max 0,0056), e e
#                 esse o gabarito de que o encadeamento esta certo. SOMAR os quatro em
#                 vez de encadear erra 0,1491 (max 0,8614), 60x mais: a diferenca e o
#                 cruzado da composicao, que some em inflacao baixa e aparece em 2002 e
#                 2021.
#
#   `leitura_12m` aplica o mesmo encadeamento ao AJUSTE de cada equacao. Cada trimestre
#                 ajustado ja carrega a dummy do trimestre dele, entao os quatro
#                 encadeados sao o que aquele ano de variacoes trimestrais significa em
#                 doze meses -- com a sazonalidade somando zero dentro da janela, que e
#                 justamente o que a codificacao soma-zero garante.
#
# Corolario que a pagina tem de dizer: o erro de 12 meses ser maior que o trimestral
# NAO e o modelo piorando. E a mesma conta lida numa unidade cerca de quatro vezes
# maior, com os quatro erros trimestrais se somando dentro da janela.

JANELA = 4


def acum12(s: pd.Series) -> pd.Series:
    """Quatro trimestres encadeados: (prod(1+pi/100)-1)*100."""
    return ((1.0 + s / 100.0).rolling(JANELA).apply(np.prod, raw=True) - 1.0) * 100.0


def leitura_12m(R: dict) -> dict:
    """O ajuste trimestral lido em doze meses, por grupo e para o cheio.

    Indexado pelo trimestre que FECHA a janela; as tres primeiras janelas da amostra
    nao existem e saem fora. Devolve, por bloco, o realizado encadeado, o ajustado
    encadeado e o erro entre os dois.
    """
    idx = R["idx"]
    i12 = idx[JANELA - 1:]

    def _bloco(obs: pd.Series, fit: pd.Series) -> dict:
        o = acum12(obs.reindex(idx)).reindex(i12)
        a = acum12(fit.reindex(idx)).reindex(i12)
        e = (a - o).dropna()
        return {"obs12": o, "aj12": a,
                "rmse": float(np.sqrt((e ** 2).mean())),
                "erro_medio": float(e.abs().mean()),
                "vies": float(e.mean())}

    return {
        "idx": i12,
        "janela": JANELA,
        "cheio": _bloco(R["cheio"]["obs"], R["cheio"]["fit"]),
        "eq": {k: _bloco(R["equacoes"][k]["obs"], R["equacoes"][k]["fit"])
               for k in ORDEM},
    }


if __name__ == "__main__":
    d = montar()
    R = estimar(d)
    print("=" * 78)
    print("CURVA DE PHILLIPS DESAGREGADA -- inflacao do trimestre, %d trimestres (%s a %s)"
          % (len(R["idx"]), R["idx"][0], R["idx"][-1]))
    print("=" * 78)
    S = sem_sazonais(d)
    for k in ORDEM:
        _print(R["equacoes"][k])
        print("  sem as dummies de trimestre: R2 %.4f  RMSE %.4f"
              % (S[k]["r2"], S[k]["rmse"]))
    c, a = R["cheio"], R["erro_agregacao"]
    print()
    print("reconstrucao do IPCA cheio: RMSE %.4f  R2 %.4f   |  piso %.4f"
          % (c["rmse"], c["r2"], a["rmse"]))

    L = leitura_12m(R)
    print()
    print("a MESMA conta lida em doze meses (%d janelas, %s a %s)"
          % (len(L["idx"]), L["idx"][0], L["idx"][-1]))
    print("  %-18s %8s %8s %8s" % ("", "RMSE", "erro md", "vies"))
    for k in ORDEM + ["cheio"]:
        b = L["cheio"] if k == "cheio" else L["eq"][k]
        nome = "IPCA cheio" if k == "cheio" else EQUACOES[k]["nome"]
        print("  %-18s %8.3f %8.3f %8.3f"
              % (nome, b["rmse"], b["erro_medio"], b["vies"]))
    print("  (o trimestral do cheio, para comparar: RMSE %.3f)" % c["rmse"])
