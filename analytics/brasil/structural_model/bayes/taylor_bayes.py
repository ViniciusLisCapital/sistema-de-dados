# -*- coding: utf-8 -*-
"""Equacao (R) -- a regra de juros -- estimada por MCMC, com priori.

Mesma equacao, mesma amostra e mesma restricao de `equations/taylor.py`. O que muda e
o estimador: em vez de minimos quadrados, um posterior amostrado por NUTS. Duas coisas
saem disso que o MQ nao da, e as duas sao a razao de o modulo existir:

**1. O efeito de longo prazo deixa de ser uma razao sem margem.**

No MQ a equacao e escrita com o multiplicador FORA do colchete:

    y(t) = r1*y(t-1) + r1b*y(t-2) + r2*dI(t) + d08 + d20 + eps,   y = R - RR* - Meta

e o objeto comparavel ao `t3` publicado pelo BC e a razao `r2 / (1 - r1 - r1b)` -- uma
funcao nao linear de tres coeficientes, cuja margem de erro e a pendencia **R8**. E uma
razao com POLO: quando a soma das defasagens se aproxima de 1 o denominador vai a zero e
a distribuicao da razao ganha cauda pesada (o problema de Fieller), que o metodo delta,
por linearizar, nao representa.

**Medido em 2026-09-22, o polo NAO morde nesta amostra** e o metodo delta teria servido:
`soma = 0,864` com desvio 0,030 fica a mais de quatro desvios de 1, e o intervalo
propagado desenho a desenho, [1,224; 4,032], quase coincide com o do delta,
[1,209; 4,192]. Fica registrado assim, e nao como argumento, porque a expectativa
contraria era a minha -- ver o `CLAUDE.md` desta pasta.

O ganho do MCMC, entao, nao e a assimetria: e que ele permite estimar a equacao **na
parametrizacao do proprio BC**, com o multiplicador dentro do colchete:

    y(t) = t1*y(t-1) + t2*y(t-2) + (1 - t1 - t2)*t3*dI(t) + d08 + d20 + eps

Essa forma e nao linear nos parametros -- `(1-t1-t2)*t3` e um produto de coisas
estimadas -- e por isso MQ nao a estima. Para o amostrador nao custa nada. E com ela
`t3` passa a ser um parametro PRIMITIVO, com intervalo de credibilidade proprio, no
lugar de uma razao derivada. A comparacao com o `2,03 [1,47; 2,64]` publicado deixa de
depender de um metodo de aproximacao.

**2. A priori tem onde entrar, e a fonte dela e o proprio BC.**

Os numeros publicados da equacao (3) sao posteriores bayesianos com intervalo de
credibilidade de 90%: `t1 = 1,48 [1,41; 1,54]`, `t2 = -0,58 [-0,63; -0,52]`,
`t3 = 2,03 [1,47; 2,64]`. Convertidos em priori normal (desvio = semiamplitude / 1,645),
eles dizem o que se sabia antes de olhar para os nossos 80 trimestres.

**A ressalva que tem de vir junto, e e a principal deste modulo:** o BC estimou aqueles
posteriores em dados brasileiros que se sobrepoem quase inteiramente aos nossos. Usa-los
como priori **conta a mesma amostra duas vezes**, e o intervalo que sai e mais estreito
do que a informacao independente justifica. Nao e um defeito que se conserta com codigo;
e o preco de importar informacao de um estudo feito na mesma populacao. Por isso o modulo
roda as quatro variantes lado a lado, e a que responde "o que os NOSSOS dados dizem" e a
de priori difusa, nao a de priori do BC.

## As quatro variantes

    nome              forma      priori                  responde
    nossa_livre       r1,r1b,r2  difusa                  o espelho do MQ; e o controle
    bc_livre          t1,t2,t3   difusa                  R8: a margem de `t3` so com nosso dado
    bc_priori         t1,t2,t3   BC publicado            o exercicio bayesiano de verdade
    bc_priori_larga   t1,t2,t3   BC, desvio x4           quanto do posterior e a priori

`nossa_livre` e `bc_livre` sao o MESMO modelo em coordenadas diferentes, entao o
posterior de `r2/(1-soma)` na primeira tem de bater com o de `t3` na segunda. Nao e uma
identidade algebrica de graca -- as prioris difusas nao sao exatamente equivalentes sob
a mudanca de variavel --, entao a concordancia e conferida numericamente em `conferir()`
e o quanto elas divergem e reportado, nao escondido.

## O que NAO muda em relacao ao MQ

A restricao continua IMPOSTA e nao estimada: o peso da ancora e `1 - t1 - t2` por
construcao, e o que se regride e o desvio `y = R - RR* - Meta`, sem intercepto. `RR*` e a
NTN-B de 10 anos crua (`taylor.MM_RR = 1`) e `dI` e a Focus de 18 meses
(`taylor.DI_BASE`). A amostra e a mesma, pela mesma `taylor.montar()`.

O que a forma bayesiana **nao** conserta: nada aqui trata a simultaneidade entre `dI(t)`
e `R(t)`, que continua sendo equacao unica contra dado observado. Priori nao e
instrumento.

## Por que isto importa para o simulador

Um desenho do posterior e um vetor COMPLETO de parametros, coerente consigo mesmo. Rodar
a regra em cada desenho devolve uma nuvem de caminhos de Selic em vez de uma linha --
e a largura dela e a incerteza de parametro, medida, e nao um intervalo colado por fora.
E o efeito de longo prazo, que e onde a incerteza mais aperta, entra na nuvem com a cauda
que ele de fato tem.

Uso:
    uv run python -m analytics.brasil.structural_model.bayes.taylor_bayes
"""
from __future__ import annotations

import json
import pathlib
import warnings

import numpy as np
import pandas as pd

from analytics.brasil.structural_model import panel
from analytics.brasil.structural_model.equations import taylor

DATA = pathlib.Path(__file__).resolve().parent / "data"

# Amostragem. 4 cadeias e o que o PyMC recomenda para o R-hat ser confiavel.
DRAWS, TUNE, CHAINS, SEED = 4000, 2000, 4, 20260922
TARGET_ACCEPT = 0.95  # a forma direta tem produto de parametros; vale apertar

# Nivel do intervalo. **90%, e nao os 94% que o ArviZ usa por default**: e o nivel em
# que o BC publica os dele, e comparar um HDI de 94% com um IC de 90% erraria de leve
# e para o lado errado (o nosso pareceria mais incerto do que e).
HDI = 0.90

# Desvio-padrao implicito por um intervalo de credibilidade de 90% simetrico.
_Z90 = 1.6448536269514722


def _priori_bc() -> dict:
    """Priori normal por parametro, lida dos intervalos que o BC publica.

    Importa de `taylor.BCB`/`BCB_IC`, que por sua vez importam de
    `monetary_policy.modelo_agregado` -- nada e transcrito, em nenhum dos dois saltos.
    """
    out = {}
    for k in ("t1", "t2", "t3"):
        lo, hi = taylor.BCB_IC[k]
        out[k] = (float(taylor.BCB[k]), float((hi - lo) / 2.0 / _Z90))
    return out


PRIORI_BC = _priori_bc()

# Default de quem nao tem priori declarada na variante.
PRIORI_DUMMY = ("N", 0.0, 5.0)
PRIORI_SIGMA = ("HN", 2.0)  # meia-normal; o RMSE do MQ e 0,566

# ── as prioris, por variante ────────────────────────────────────────────────
# Cada entrada e uma tupla (familia, *parametros):
#     ("N", media, desvio)   normal
#     ("U", a, b)            uniforme no intervalo [a, b] -- suporte LIMITADO
#     ("HN", escala)         meia-normal, para o desvio do erro
#
# Uniforme nao e "sem informacao": ela afirma que o parametro NAO pode sair da caixa, e
# essa afirmacao e forte. Por isso `resumo()` mede, para cada uma, quanta massa do
# posterior encostou em cada borda -- uma borda que prende muda o resultado sem avisar.
PRIORIS = {
    # Escolhida pelo usuario em 2026-09-22, em caixas uniformes. Vale registrar que ela
    # reproduz a caixa do PROPRIO BC em dois dos tres: `modelo_agregado.CAIXA` traz
    # t1=(0,2) e t2=(-1,1) identicos, e t3=(0,4) -- o usuario abriu ate 5.
    "usuario": {"t1": ("U", 0.0, 2.0), "t2": ("U", -1.0, 1.0), "t3": ("U", 0.0, 5.0),
                "d08": ("U", -10.0, 0.0), "d20": ("U", -10.0, 0.0),
                "sigma": PRIORI_SIGMA},
    # Normais largas. Larga o bastante para o dado mandar, estreita o bastante para o
    # amostrador nao passear: a Selic em desvio da ancora anda em unidades de p.p.
    "livre": {"t1": ("N", 0.0, 1.0), "t2": ("N", 0.0, 1.0), "t3": ("N", 0.0, 5.0),
              "r1": ("N", 0.0, 1.0), "r1b": ("N", 0.0, 1.0), "r2": ("N", 0.0, 2.0)},
    "bc": {k: ("N", m, sd) for k, (m, sd) in PRIORI_BC.items()},
    "bc_larga": {k: ("N", m, sd * 4.0) for k, (m, sd) in PRIORI_BC.items()},
}

MODELOS = {
    "usuario": dict(
        forma="direta", priori="usuario",
        desc="Caixas uniformes escolhidas pelo usuário em 2026-09-22"),
    "nossa_livre": dict(
        forma="nossa", priori="livre",
        desc="Nossa parametrização, normais largas — o espelho do MQ"),
    "bc_livre": dict(
        forma="direta", priori="livre",
        desc="Parametrização do BC, normais largas — o que só o nosso dado diz"),
    "bc_priori": dict(
        forma="direta", priori="bc",
        desc="Parametrização do BC, priori do BC publicada"),
    "bc_priori_larga": dict(
        forma="direta", priori="bc_larga",
        desc="Idem, com o desvio da priori multiplicado por 4"),
}
BASE = "usuario"


# ─────────────────────────────────────────────────────────────────────────────
# dados
# ─────────────────────────────────────────────────────────────────────────────
def dados(df: pd.DataFrame | None = None, lags: int = taylor.LAGS,
          di: str = taylor.DI_BASE, k: int = taylor.MM_RR,
          dummies: bool = True) -> dict:
    """A MESMA matriz de regressao do MQ, pela mesma `taylor.montar()`.

    Ler o painel do CSV versionado e o default, para o modulo rodar sem banco e para
    duas execucoes darem o mesmo numero. `df=panel.construir()` usa o painel ao vivo.
    """
    if df is None:
        df = panel.carregar()
    d = taylor.montar(df, k=k, lags=lags, di=di)

    reg = ["r1"] + (["r1b"] if lags == 2 else []) + ["r2"]
    am = d[["y"] + reg + list(taylor.CRISES)].dropna()
    # A amostra e a MESMA com e sem dummies -- o `dropna` continua olhando as colunas de
    # crise, que nao tem buraco. Sem isso a comparacao seria entre amostras diferentes.
    usadas = [c for c in taylor.CRISES if dummies and am[c].sum() > 0]

    return {
        "y": am["y"].to_numpy(float),
        "X": {c: am[c].to_numpy(float) for c in reg + usadas},
        "reg": reg, "dummies": usadas, "lags": lags, "di": di, "mm_rr": k,
        "idx": am.index, "n": len(am),
        "ini": am.index[0], "fim": am.index[-1],
        "obs": am["y"], "d": d,
    }


# ─────────────────────────────────────────────────────────────────────────────
# o modelo
# ─────────────────────────────────────────────────────────────────────────────
def construir_modelo(dd: dict, forma: str = "direta", priori: str = "bc"):
    """Monta o modelo PyMC.

    `forma="nossa"`  -> r1, r1b, r2 primitivos; `t3` sai como quantidade derivada.
    `forma="direta"` -> t1, t2, t3 primitivos, com `(1-t1-t2)*t3` multiplicando `dI`;
                        `r2` sai como derivada. E a forma em que o BC escreve e a unica
                        em que a priori dele pode ser posta onde ela foi publicada.
    """
    import pymc as pm  # local: importar PyMC custa segundos, e nem todo uso precisa

    if priori not in PRIORIS:
        raise ValueError("priori desconhecida: %r" % priori)
    pri = PRIORIS[priori]

    def rv(nome, padrao=None):
        """Cria a variavel com a familia que a variante declarou para ela."""
        spec = pri.get(nome, padrao)
        if spec is None:
            raise KeyError("a priori %r nao declara %r" % (priori, nome))
        fam = spec[0]
        if fam == "N":
            return pm.Normal(nome, spec[1], spec[2])
        if fam == "U":
            return pm.Uniform(nome, lower=spec[1], upper=spec[2])
        if fam == "HN":
            return pm.HalfNormal(nome, spec[1])
        raise ValueError("familia de priori desconhecida: %r" % fam)

    X, y = dd["X"], dd["y"]
    tem_r1b = "r1b" in dd["reg"]

    with pm.Model() as m:
        if forma == "direta":
            t1 = rv("t1")
            t2 = rv("t2") if tem_r1b else 0.0
            t3 = rv("t3")
            soma = pm.Deterministic("soma", t1 + t2)
            r2 = pm.Deterministic("r2", (1.0 - soma) * t3)
            r1, r1b = t1, t2
        elif forma == "nossa":
            r1 = rv("r1")
            r1b = rv("r1b") if tem_r1b else 0.0
            r2 = rv("r2")
            soma = pm.Deterministic("soma", r1 + r1b)
            # A razao com polo. Ela e o objeto comparavel ao `t3` publicado, e e
            # justamente por ter polo que o metodo delta nao a representa bem.
            t3 = pm.Deterministic("t3", r2 / (1.0 - soma))
        else:
            raise ValueError("forma desconhecida: %r" % forma)

        mu = r1 * X["r1"] + r2 * X["r2"]
        if tem_r1b:
            mu = mu + r1b * X["r1b"]
        for c in dd["dummies"]:
            mu = mu + rv(c, PRIORI_DUMMY) * X[c]

        sigma = rv("sigma", PRIORI_SIGMA)
        pm.Normal("y_obs", mu=mu, sigma=sigma, observed=y)
    return m


def amostrar(dd: dict, forma: str = "direta", priori: str = "bc",
             draws: int = DRAWS, tune: int = TUNE, chains: int = CHAINS,
             seed: int = SEED, prior_pred: bool = True):
    """Roda o NUTS e devolve o `InferenceData`."""
    import pymc as pm

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with construir_modelo(dd, forma=forma, priori=priori):
            idata = pm.sample(draws=draws, tune=tune, chains=chains, cores=1,
                              target_accept=TARGET_ACCEPT, random_seed=seed,
                              progressbar=False)
            if prior_pred:
                idata.extend(pm.sample_prior_predictive(draws=2000, random_seed=seed))
            idata.extend(pm.sample_posterior_predictive(
                idata, random_seed=seed, progressbar=False))
    return idata


# ─────────────────────────────────────────────────────────────────────────────
# leitura do posterior
# ─────────────────────────────────────────────────────────────────────────────
def _flat(idata, nome: str, grupo: str = "posterior") -> np.ndarray:
    return np.asarray(getattr(idata, grupo)[nome]).reshape(-1)


def _meia_vida_draws(phis: np.ndarray, passos: int = 400) -> np.ndarray:
    """Meia-vida por desenho, pela MESMA regra simulada de `is_curve._meia_vida`.

    `phis` tem forma (n_draws, n_lags). Devolve NaN onde a resposta nao cai a metade
    dentro do horizonte -- o que acontece em qualquer desenho nao estacionario.
    """
    n, p = phis.shape
    hist = np.ones((n, p))
    out = np.full(n, np.nan)
    for t in range(passos):
        v = (hist[:, ::-1] * phis).sum(axis=1)
        hist = np.column_stack([hist[:, 1:], v]) if p > 1 else v.reshape(-1, 1)
        achou = np.isnan(out) & (np.abs(v) <= 0.5)
        out[achou] = t + 1
    return out


def _stats(x: np.ndarray, hdi: float = HDI) -> dict:
    """Media, desvio, mediana e HDI. O HDI e o intervalo mais CURTO com a massa pedida.

    Para um posterior assimetrico -- que e exatamente o caso do efeito de longo prazo --
    ele difere do intervalo de percentis, e e o que o BC publica.
    """
    import arviz as az
    x = np.asarray(x, float)
    fin = x[np.isfinite(x)]
    lo, hi = az.hdi(fin, hdi_prob=hdi)
    return {"media": float(fin.mean()), "sd": float(fin.std(ddof=1)),
            "mediana": float(np.median(fin)),
            "hdi_lo": float(lo), "hdi_hi": float(hi),
            "q05": float(np.percentile(fin, 5)), "q50": float(np.median(fin)),
            "q95": float(np.percentile(fin, 95)),
            "n_finito": int(fin.size), "n_total": int(x.size)}


def resumo(idata, dd: dict, forma: str, priori: str) -> dict:
    """Tudo o que a tela vai precisar, ja lido do posterior."""
    import arviz as az

    tem_r1b = "r1b" in dd["reg"]
    nomes = (["t1", "t2", "t3"] if forma == "direta" else ["r1", "r1b", "r2"])
    if not tem_r1b:
        nomes = [n for n in nomes if n not in ("t2", "r1b")]
    nomes = nomes + list(dd["dummies"]) + ["sigma"]

    post = {n: _flat(idata, n) for n in nomes}
    soma = _flat(idata, "soma")
    # Os dois lados da mesma moeda, sempre presentes: o que e primitivo numa forma e
    # derivado na outra, e a tabela imprime os dois para as formas serem comparaveis.
    t3 = _flat(idata, "t3") if forma == "nossa" else post["t3"]
    r2 = post["r2"] if forma == "nossa" else _flat(idata, "r2")
    r1 = post["t1"] if forma == "direta" else post["r1"]
    r1b = (post["t2"] if forma == "direta" else post["r1b"]) if tem_r1b else None

    phis = np.column_stack([r1, r1b]) if tem_r1b else r1.reshape(-1, 1)
    mv = _meia_vida_draws(phis)

    sm = az.summary(idata, var_names=nomes, hdi_prob=HDI)

    # Ajuste na media do posterior, para o RMSE ser comparavel ao do MQ.
    X = dd["X"]
    fit = np.zeros(dd["n"])
    fit += float(np.mean(r1)) * X["r1"] + float(np.mean(r2)) * X["r2"]
    if tem_r1b:
        fit += float(np.mean(r1b)) * X["r1b"]
    for c in dd["dummies"]:
        fit += float(np.mean(post[c])) * X[c]
    e = dd["y"] - fit
    sst = float(((dd["y"] - dd["y"].mean()) ** 2).sum())

    # Ljung-Box sobre o mesmo residuo, para o diagnostico ficar lado a lado com o do MQ.
    from statsmodels.stats.diagnostic import acorr_ljungbox
    lbt = acorr_ljungbox(e, lags=[4, 8], return_df=True)

    par = {n: _stats(post[n]) for n in nomes}
    par["soma"] = _stats(soma)
    par["efeito_lp"] = _stats(t3)
    par["meia_vida"] = _stats(mv)
    if forma == "direta":
        par["r2_derivado"] = _stats(r2)

    for n in nomes:
        par[n]["r_hat"] = float(sm.loc[n, "r_hat"])
        par[n]["ess"] = float(sm.loc[n, "ess_bulk"])

    # Encolhimento: quanto a priori estreitou em ver o dado. 1 = o dado nao mudou nada.
    pri_sd = {}
    if "prior" in idata.groups():
        for n in nomes:
            try:
                pri_sd[n] = float(np.std(_flat(idata, n, "prior"), ddof=1))
            except KeyError:
                pass
    for n, s in pri_sd.items():
        par[n]["priori_sd"] = s
        par[n]["encolhimento"] = float(par[n]["sd"] / s) if s > 0 else None

    # Uma caixa uniforme PRENDE, e isso nao levanta erro nenhum: se o posterior encosta
    # numa borda, o numero que sai e a borda e nao o dado.
    #
    # A medida tem de ser na escala do POSTERIOR, nao na da caixa. Uma primeira versao
    # deste diagnostico contava a massa nos 5% extremos da caixa, e numa caixa de
    # largura 10 com posterior em -0,47 isso acusava 58% -- a borda parecia estar
    # prendendo quando o que estava largo era a caixa. O que se mede aqui e a distancia
    # de cada borda ate a media, em desvios do posterior: acima de ~3 a borda e inerte,
    # abaixo de ~2 ela esta cortando cauda.
    espec = PRIORIS.get(priori, {})
    for n in nomes:
        sp = espec.get(n)
        if not sp or sp[0] != "U":
            continue
        a, b = float(sp[1]), float(sp[2])
        x = post[n]
        sd = par[n]["sd"] or 1e-12
        par[n]["caixa"] = [a, b]
        par[n]["z_inf"] = float((par[n]["media"] - a) / sd)
        par[n]["z_sup"] = float((b - par[n]["media"]) / sd)
        par[n]["massa_1sd_inf"] = float(np.mean(x < a + sd))
        par[n]["massa_1sd_sup"] = float(np.mean(x > b - sd))

    div = int(np.asarray(idata.sample_stats["diverging"]).sum())
    return {
        "modelo": "%s / %s" % (forma, priori),
        "forma": forma, "priori": priori,
        "n": dd["n"], "ini": str(dd["ini"]), "fim": str(dd["fim"]),
        "lags": dd["lags"], "di": dd["di"], "mm_rr": dd["mm_rr"],
        "draws": int(len(soma)), "divergencias": div,
        "r_hat_max": float(sm["r_hat"].max()), "ess_min": float(sm["ess_bulk"].min()),
        "par": par,
        "p_estavel": float(np.mean(np.abs(soma) < 1.0)),
        "p_t3_no_ic_bc": float(np.mean((t3 >= taylor.BCB_IC["t3"][0])
                                       & (t3 <= taylor.BCB_IC["t3"][1]))),
        "p_r2_positivo": float(np.mean(r2 > 0)),
        "rmse": float(np.sqrt((e ** 2).mean())),
        "r2_cent": float(1.0 - (e ** 2).sum() / sst),
        "lb_p4": float(lbt["lb_pvalue"].iloc[0]),
        "lb_p8": float(lbt["lb_pvalue"].iloc[1]),
        "acf1": float(pd.Series(e).autocorr(1)),
        "_t3": t3, "_soma": soma, "_fit": fit, "_resid": e,
        "_draws": dict({"r1": r1, "r1b": r1b, "r2": r2, "t3": t3, "soma": soma},
                       **{n: post[n] for n in nomes}),
    }


def conferir(res: dict, mq: dict, tol_ic: float = 0.10) -> dict:
    """Confere o que o modulo AFIRMA, em vez de deixar por conta do olho.

    1. **A restricao continua valendo**: o desvio volta a zero com `dI = 0`, na media
       do posterior. E a mesma `taylor.repouso()`, chamada com os coeficientes de ca.
    2. **`nossa_livre` e `bc_livre` sao o mesmo modelo** em coordenadas diferentes, e o
       posterior do efeito de longo prazo tem de concordar. Nao exatamente: uma priori
       difusa em `r2` nao e a mesma coisa que uma priori difusa em `t3` sob mudanca de
       variavel. A diferenca e devolvida, nao suprimida.
    3. **Cadeias convergidas**: R-hat < 1,01, ESS > 400, zero divergencias.
    """
    out = {"r_hat_ok": res["r_hat_max"] < 1.01,
           "ess_ok": res["ess_min"] > 400,
           "sem_divergencia": res["divergencias"] == 0}

    phis = [res["par"]["t1" if res["forma"] == "direta" else "r1"]["media"]]
    if res["lags"] == 2:
        phis.append(res["par"]["t2" if res["forma"] == "direta" else "r1b"]["media"])
    r2m = res["par"]["r2" if res["forma"] == "nossa" else "r2_derivado"]["media"]
    falso = {"phis": phis, "coef": {"r2": r2m},
             "efeito_lp": r2m / (1.0 - sum(phis))}
    try:
        rep = taylor.repouso(falso)
        out["volta_a_ancora"] = bool(rep["volta_a_ancora"])
        out["efeito_simulado"] = rep["efeito_simulado"]
    except AssertionError as exc:
        out["volta_a_ancora"] = False
        out["repouso_erro"] = str(exc)

    out["mq_efeito_lp"] = mq["efeito_lp"]
    out["mq_dentro_do_hdi"] = bool(res["par"]["efeito_lp"]["hdi_lo"] <= mq["efeito_lp"]
                                   <= res["par"]["efeito_lp"]["hdi_hi"])
    return out


def leque(res: dict, di: float = 1.0, h: int = 20, hdi: float = HDI) -> dict:
    """A resposta da Selic a um desvio PERMANENTE de `di` p.p., desenho a desenho.

    E a demonstracao do que o posterior da ao simulador e o MQ nao da. Cada desenho e
    um vetor completo e coerente de parametros, entao rodar a regra em todos eles
    devolve uma NUVEM de caminhos: a mediana e o caminho central, e a largura da faixa
    e a incerteza de parametro propagada pela dinamica -- que cresce com o horizonte,
    porque a mesma incerteza de `r1`/`r1b` se acumula a cada trimestre.

    Colar uma faixa constante em volta do caminho do MQ diria a coisa errada nos dois
    extremos: larga demais no impacto, estreita demais no longo prazo.
    """
    import arviz as az
    d = res["_draws"]
    r1, r2 = np.asarray(d["r1"]), np.asarray(d["r2"])
    r1b = np.asarray(d["r1b"]) if d["r1b"] is not None else None
    n = r1.size

    y = np.zeros((n, h + 1))
    for t in range(1, h + 1):
        v = r1 * y[:, t - 1] + r2 * di
        if r1b is not None and t >= 2:
            v = v + r1b * y[:, t - 2]
        y[:, t] = v

    linhas = []
    for t in range(h + 1):
        lo, hi = az.hdi(y[:, t], hdi_prob=hdi)
        linhas.append({"t": t, "mediana": float(np.median(y[:, t])),
                       "media": float(y[:, t].mean()),
                       "lo": float(lo), "hi": float(hi),
                       "largura": float(hi - lo)})
    return {"di": di, "h": h, "linhas": linhas,
            "lp": _stats(np.asarray(d["t3"]) * di, hdi)}


# ─────────────────────────────────────────────────────────────────────────────
# execucao
# ─────────────────────────────────────────────────────────────────────────────
def rodar(quais: list[str] | None = None, df: pd.DataFrame | None = None,
          draws: int = DRAWS, tune: int = TUNE, dummies: bool = True) -> dict:
    """Roda as variantes pedidas sobre a MESMA amostra e devolve os resumos."""
    dd = dados(df, dummies=dummies)
    mq = taylor.estimar(dd["d"], dummies=dummies)
    out = {"dd": dd, "mq": mq, "res": {}, "idata": {}}
    for nome in (quais or list(MODELOS)):
        cfg = MODELOS[nome]
        idata = amostrar(dd, forma=cfg["forma"], priori=cfg["priori"],
                         draws=draws, tune=tune)
        r = resumo(idata, dd, cfg["forma"], cfg["priori"])
        r["nome"], r["desc"] = nome, cfg["desc"]
        r["conferencia"] = conferir(r, mq)
        r["leque"] = leque(r)
        out["res"][nome], out["idata"][nome] = r, idata
    return out


# Quantos desenhos vao para o simulador. O posterior tem 16.000; o navegador nao
# precisa de todos para desenhar uma faixa de 90%. Vao AFINADOS por passo constante, e
# nao os primeiros 1.000: um bloco contiguo pegaria as cadeias em ordem, e a primeira
# cadeia sozinha nao e o posterior.
N_DESENHOS = 1000


def salvar_desenhos(saida: dict, nome: str = BASE, n: int = N_DESENHOS,
                    destino: pathlib.Path | None = None) -> pathlib.Path:
    """Grava os desenhos afinados da variante base, para o simulador do relatorio.

    O relatorio NAO roda MCMC: ele le este arquivo. Reestimar e um passo proprio, como
    os tres passos do `monetary_policy` -- o que o botao Regerar alcanca e a leitura.
    """
    destino = destino or (DATA / "taylor_draws.json")
    destino.parent.mkdir(parents=True, exist_ok=True)
    r = saida["res"][nome]
    d, dd = r["_draws"], saida["dd"]
    tot = int(np.asarray(d["t1"]).size)
    passo = max(1, tot // n)
    sel = np.arange(0, tot, passo)[:n]

    pars = ["t1", "t2", "t3"] + list(dd["dummies"]) + ["sigma"]
    out = {
        "variante": nome, "priori": r["priori"], "forma": r["forma"],
        "n_total": tot, "n_gravado": int(sel.size), "passo": int(passo),
        "gerado_de": {"n": dd["n"], "ini": str(dd["ini"]), "fim": str(dd["fim"]),
                      "di": dd["di"], "mm_rr": dd["mm_rr"], "lags": dd["lags"]},
        "pars": pars,
        "draws": {k: [round(float(v), 4) for v in np.asarray(d[k])[sel]] for k in pars},
        "mediana": {k: float(np.median(np.asarray(d[k]))) for k in pars},
        "media": {k: float(np.mean(np.asarray(d[k]))) for k in pars},
        "hdi": {k: [r["par"][k]["hdi_lo"], r["par"][k]["hdi_hi"]] for k in pars},
        "caixa": {k: r["par"][k].get("caixa") for k in pars},
        "hdi_prob": HDI,
    }
    destino.write_text(json.dumps(out, ensure_ascii=False, default=float),
                       encoding="utf-8")
    return destino


def salvar(saida: dict, destino: pathlib.Path | None = None) -> pathlib.Path:
    """Grava os resumos em JSON, sem as series pesadas."""
    destino = destino or (DATA / "taylor_bayes.json")
    destino.parent.mkdir(parents=True, exist_ok=True)
    limpo = {}
    for nome, r in saida["res"].items():
        limpo[nome] = {k: v for k, v in r.items() if not k.startswith("_")}
    mq = saida["mq"]
    limpo["_mq"] = {"coef": {k: float(v) for k, v in mq["coef"].items()},
                    "se": {k: float(v) for k, v in mq["se"].items()},
                    "t": {k: float(v) for k, v in mq["t"].items()},
                    "soma": mq["soma"], "efeito_lp": mq["efeito_lp"],
                    "meia_vida": mq["meia_vida"], "r2_cent": mq["r2_cent"],
                    "rmse": mq["rmse"], "lb_p4": mq["lb_p4"], "lb_p8": mq["lb_p8"],
                    "n": mq["n"], "ini": str(mq["ini"]), "fim": str(mq["fim"])}
    limpo["_bc"] = {"valor": taylor.BCB, "ic": {k: list(v) for k, v in
                                                taylor.BCB_IC.items()},
                    "priori_usada": {k: list(v) for k, v in PRIORI_BC.items()}}
    destino.write_text(json.dumps(limpo, indent=2, ensure_ascii=False,
                                  default=float), encoding="utf-8")
    return destino


def _lin(nome: str, s: dict, bc: tuple | None = None) -> str:
    alvo = ""
    if bc is not None:
        dentro = bc[1][0] <= s["media"] <= bc[1][1]
        alvo = "   %+6.3f [%+5.2f; %+5.2f] %s" % (bc[0], bc[1][0], bc[1][1],
                                                  "dentro" if dentro else " FORA ")
    enc = s.get("encolhimento")
    col = "  %5.2f" % enc if enc is not None else "      "
    return ("  %-12s %+7.3f  %6.3f   [%+7.3f; %+7.3f]%s%s"
            % (nome, s["media"], s["sd"], s["hdi_lo"], s["hdi_hi"], col, alvo))


def imprimir(saida: dict) -> None:
    dd, mq = saida["dd"], saida["mq"]
    print("=" * 96)
    print("EQUACAO (R) -- REGRA DE JUROS, ESTIMACAO BAYESIANA")
    print("=" * 96)
    print("amostra   %s a %s, %d trimestres   |   dI = %s, RR* = mm(%d), %d defasagens"
          % (dd["ini"], dd["fim"], dd["n"], dd["di"], dd["mm_rr"], dd["lags"]))
    print("HDI de %.0f%%, o mesmo nivel em que o BC publica os intervalos dele\n"
          % (HDI * 100))

    print("PRIORIS, por variante:")
    for nome, esp in PRIORIS.items():
        pecas = []
        for k in ("t1", "t2", "t3", "r1", "r1b", "r2", "d08", "d20"):
            sp = esp.get(k)
            if not sp:
                continue
            if sp[0] == "N":
                pecas.append("%s~N(%+.3f, %.3f)" % (k, sp[1], sp[2]))
            elif sp[0] == "U":
                pecas.append("%s~U[%+.1f, %+.1f]" % (k, sp[1], sp[2]))
        print("  %-16s %s" % (nome, "  ".join(pecas)))
    print("  (a do BC sai de %s, com desvio = semiamplitude do IC de 90%% / 1,645;"
          % ", ".join("%s %.2f [%.2f; %.2f]" % (k, taylor.BCB[k], *taylor.BCB_IC[k])
                      for k in ("t1", "t2", "t3")))
    print("   dummies e sigma nao declarados caem no default: N(0; 5) e meia-normal(2))")
    print()

    print("-" * 96)
    print("MQ, para comparar (%s)" % mq["estimador"])
    print("-" * 96)
    for c in mq["termos"] + mq["dummies"]:
        print("  %-12s %+7.3f  %6.3f   t %+6.2f"
              % (c, mq["coef"][c], mq["se"][c], mq["t"][c]))
    print("  %-12s %+7.3f            soma das defasagens" % ("soma", mq["soma"]))
    print("  %-12s %+7.3f            efeito de longo prazo = r2/(1-soma), SEM margem"
          % ("efeito_lp", mq["efeito_lp"]))
    print("  R2c %.4f   RMSE %.4f   Q(4) p %.3f   Q(8) p %.3f"
          % (mq["r2_cent"], mq["rmse"], mq["lb_p4"], mq["lb_p8"]))

    for nome, r in saida["res"].items():
        print("\n" + "-" * 96)
        print("%s  --  %s" % (nome.upper(), r["desc"]))
        print("-" * 96)
        cab = "  %-12s %7s  %6s   %-21s %6s   %s" % (
            "parametro", "media", "sd", "HDI %d%%" % (HDI * 100), "enc.",
            "BC publicado")
        print(cab)
        alvos = {"t1": ("t1",), "t2": ("t2",), "t3": ("t3",),
                 "r1": ("t1",), "r1b": ("t2",), "efeito_lp": ("t3",)}
        ordem = [k for k in ("t1", "t2", "t3", "r1", "r1b", "r2", "r2_derivado",
                             "soma", "efeito_lp", "meia_vida", "d08", "d20", "sigma")
                 if k in r["par"]]
        for k in ordem:
            a = alvos.get(k, (None,))[0]
            bc = (taylor.BCB[a], taylor.BCB_IC[a]) if a else None
            print(_lin(k, r["par"][k], bc))
        caixas = [(k, r["par"][k]) for k in ordem if "caixa" in r["par"][k]]
        if caixas:
            print("  caixas uniformes -- distancia de cada borda ate a media, "
                  "em desvios do posterior:")
            print("    %-5s %-18s %8s %8s   %s"
                  % ("", "caixa", "z(inf)", "z(sup)", "veredito"))
            for k, sdet in caixas:
                z = min(sdet["z_inf"], sdet["z_sup"])
                vd = ("INERTE" if z > 3 else
                      "corta a cauda" if z > 2 else "PRENDE -- a borda esta decidindo")
                print("    %-5s [%+7.1f; %+7.1f] %8.2f %8.2f   %s"
                      % (k, sdet["caixa"][0], sdet["caixa"][1], sdet["z_inf"],
                         sdet["z_sup"], vd))
        print("  soma publicada do BC: %+.2f (sem IC)" % taylor.BCB_SOMA)
        print("  P(estavel) %.3f   P(r2>0) %.3f   P(efeito de lp dentro do IC do BC) %.3f"
              % (r["p_estavel"], r["p_r2_positivo"], r["p_t3_no_ic_bc"]))
        print("  R2c %.4f   RMSE %.4f   Q(4) p %.3f   Q(8) p %.3f   acf(1) %+.2f"
              % (r["r2_cent"], r["rmse"], r["lb_p4"], r["lb_p8"], r["acf1"]))
        c = r["conferencia"]
        print("  cadeias: R-hat max %.4f   ESS min %.0f   divergencias %d   %s"
              % (r["r_hat_max"], r["ess_min"], r["divergencias"],
                 "ok" if all([c["r_hat_ok"], c["ess_ok"], c["sem_divergencia"]])
                 else "ATENCAO"))
        print("  restricao: volta a ancora com dI=0 -> %s   |   MQ (%.3f) dentro do HDI -> %s"
              % (c.get("volta_a_ancora"), c["mq_efeito_lp"], c["mq_dentro_do_hdi"]))

    # A concordancia entre as duas formas com priori difusa, medida.
    if "nossa_livre" in saida["res"] and "bc_livre" in saida["res"]:
        a = saida["res"]["nossa_livre"]["par"]["efeito_lp"]
        b = saida["res"]["bc_livre"]["par"]["efeito_lp"]
        print("\n" + "-" * 96)
        print("CONFERENCIA DE COORDENADAS -- o mesmo modelo escrito de dois jeitos")
        print("-" * 96)
        print("  efeito de longo prazo, razao derivada (nossa_livre): "
              "%.3f  [%.3f; %.3f]" % (a["mediana"], a["hdi_lo"], a["hdi_hi"]))
        print("  efeito de longo prazo, parametro direto (bc_livre):  "
              "%.3f  [%.3f; %.3f]" % (b["mediana"], b["hdi_lo"], b["hdi_hi"]))
        print("  diferenca da mediana: %.3f   das bordas: %.3f e %.3f"
              % (abs(a["mediana"] - b["mediana"]), abs(a["hdi_lo"] - b["hdi_lo"]),
                 abs(a["hdi_hi"] - b["hdi_hi"])))

        # A cauda que o metodo delta nao representa.
        t3 = saida["res"]["nossa_livre"]["_t3"]
        m, sd = float(np.mean(t3)), float(np.std(t3, ddof=1))
        print("\n  A ASSIMETRIA, que e o argumento contra o metodo delta:")
        print("    razao derivada: media %.3f, mediana %.3f, sd %.3f"
              % (m, float(np.median(t3)), sd))
        print("    HDI 90%%      : [%.3f; %.3f]  -> %.3f abaixo, %.3f acima da mediana"
              % (a["hdi_lo"], a["hdi_hi"], float(np.median(t3)) - a["hdi_lo"],
                 a["hdi_hi"] - float(np.median(t3))))
        print("    delta (simetrico, +-1,645 sd): [%.3f; %.3f]"
              % (m - _Z90 * sd, m + _Z90 * sd))

    # O que o posterior da ao simulador: uma nuvem, nao uma linha.
    alvo = BASE if BASE in saida["res"] else list(saida["res"])[0]
    lq = saida["res"][alvo].get("leque") or leque(saida["res"][alvo])
    outro = "bc_livre" if "bc_livre" in saida["res"] and alvo != "bc_livre" else None
    lq2 = (saida["res"][outro].get("leque") or leque(saida["res"][outro])) if outro else None
    mqr = saida["mq"]
    print("\n" + "-" * 96)
    print("O LEQUE DO SIMULADOR -- resposta da Selic a um desvio permanente de "
          "+1 p.p. (%s)" % alvo)
    print("-" * 96)
    print("  a faixa com a priori do BC (%s) e, ao lado, a que so o nosso dado sustenta"
          % alvo)
    print("  %6s  %9s  %19s  %8s   %19s  %8s"
          % ("trim.", "MQ", "faixa %d%% (%s)" % (HDI * 100, alvo), "largura",
             "faixa %d%% (%s)" % (HDI * 100, outro or "-"), "largura"))
    phis = mqr["phis"]
    ymq = [0.0]
    for t in range(1, lq["h"] + 1):
        v = phis[0] * ymq[t - 1] + mqr["coef"]["r2"]
        if len(phis) > 1 and t >= 2:
            v += phis[1] * ymq[t - 2]
        ymq.append(v)
    for i, ln in enumerate(lq["linhas"]):
        if ln["t"] not in (1, 2, 3, 4, 6, 8, 12, 16, 20):
            continue
        b = lq2["linhas"][i] if lq2 else None
        col2 = ("   [%+7.3f; %+7.3f]  %8.3f" % (b["lo"], b["hi"], b["largura"])
                if b else "")
        print("  %6d  %+9.3f  [%+7.3f; %+7.3f]  %8.3f%s"
              % (ln["t"], ymq[ln["t"]], ln["lo"], ln["hi"], ln["largura"], col2))
    c2 = ("   [%+7.3f; %+7.3f]  %8.3f"
          % (lq2["lp"]["hdi_lo"], lq2["lp"]["hdi_hi"],
             lq2["lp"]["hdi_hi"] - lq2["lp"]["hdi_lo"])) if lq2 else ""
    print("  %6s  %+9.3f  [%+7.3f; %+7.3f]  %8.3f%s"
          % ("lp", mqr["efeito_lp"], lq["lp"]["hdi_lo"], lq["lp"]["hdi_hi"],
             lq["lp"]["hdi_hi"] - lq["lp"]["hdi_lo"], c2))


def main() -> dict:
    saida = rodar()
    imprimir(saida)
    p = salvar(saida)
    q = salvar_desenhos(saida)
    print("")
    print("resumo    %s" % p)
    print("desenhos  %s -- e o que o simulador le" % q)
    return saida


if __name__ == "__main__":
    main()
