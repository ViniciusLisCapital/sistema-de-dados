# -*- coding: utf-8 -*-
"""A equacao (E), as expectativas, estimada por MCMC -- a mesma equacao do MQ.

    (E) E(t) - Meta(t) = e1*[E(t-1) - Meta(t)] + e2*[I12(t) - Meta(t)] + eps
        eps ~ N(0, sigma)

Existe pela mesma razao que `taylor_bayes.py` e `fx_bayes.py`: **o simulador desenha uma
faixa, e ela tem de sair do posterior.** Com (R) e (F) ja carregando faixa de 90%,
entrar com a terceira equacao em linha pelada poria tres contas na mesma tela afirmando
coisas de tipos diferentes, sem nada explicando a diferenca.

## A equacao e a MESMA, e isso e verificavel

Este modulo NAO remonta a matriz: chama `expectations.montar()`, a mesma funcao que o MQ
usa, e impoe a restricao pela MESMA reparametrizacao (subtrai a meta dos dois lados,
regride desvio contra desvio, sem intercepto). O que muda e so o estimador.
`conferir()` mede a distancia entre a mediana do posterior e o coeficiente de MQ em
desvios do proprio posterior -- se as duas divergirem, ou a priori esta apertando ou a
matriz deixou de ser a mesma, e as duas hipoteses sao visiveis.

## A restricao continua IMPOSTA, e e ela que da o comportamento de repouso

Os tres pesos somam 1 por construcao: `peso_meta` nao e amostrado, ele e `1 - e1 - e2`.
A consequencia e estrutural e vale desenho a desenho -- **com a inflacao na meta, a
equacao devolve a meta**, quaisquer que sejam os coeficientes. Num simulador isso
importa mais do que na estimacao: e o que impede um desenho do posterior de produzir um
caminho que converge para um numero que nao e a meta.

`repouso_draws()` afirma isso sobre a AMOSTRA INTEIRA e nao sobre a mediana. A mediana
satisfazer uma identidade linear nao garante que cada desenho a satisfaca, e e cada
desenho que o simulador roda.

## A priori, e por que ela e UMA SO aqui

Ao contrario da (F), os dois regressores desta equacao estao na MESMA unidade -- pontos
percentuais de desvio contra a meta -- e os dois coeficientes sao PESOS, isto e, numeros
que se espera em torno de [0, 1]. Nao ha nada para autoescalar: `N(0, 1)` e larga o
bastante para cobrir o intervalo util varias vezes e estreita o bastante para o
amostrador nao passear. A variante `larga` multiplica por 4 e existe para medir isso em
vez de afirma-lo.

**A priori do BC NAO entra aqui, e a razao e o objeto e nao a data.** A equacao (5) do
boxe publica `f1 = 0,75`, `f2 = 0,11`, `f3 = 0,021` -- mas o `f2` de la multiplica a
previsao DO PROPRIO MODELO quatro trimestres a frente, e o nosso `e2` multiplica a
inflacao REALIZADA acumulada em doze meses. Sao regressores diferentes, entao as duas
colunas nao sao somaveis e transplantar o numero seria por a priori no lugar errado.
Isso ja esta escrito em `equations/expectations.py`; aqui ele tem a consequencia de o
modulo nao ter variante "bc".

**E os pesos NAO sao restritos ao simplex.** Nada na priori proibe `e1 < 0` ou
`e1 + e2 > 1`. Manter assim e o que faz esta estimacao ser o espelho exato do MQ -- uma
Dirichlet seria outro modelo, com outra amostra implicita. Que o posterior fique dentro
do simplex passa a ser uma MEDICAO (`fora_simplex` no resumo) em vez de uma suposicao.

Uso:
    uv run python -m analytics.brasil.structural_model.bayes.expectations_bayes
"""
from __future__ import annotations

import json
import pathlib
import warnings

import numpy as np
import pandas as pd

from analytics.brasil.structural_model import panel
from analytics.brasil.structural_model.equations import expectations as eq_exp

DATA = pathlib.Path(__file__).resolve().parent / "data"

# 4 cadeias, como o PyMC recomenda para o R-hat valer. Amostra pequena (98) e modelo
# linear com 3 parametros: roda em segundos.
DRAWS, TUNE, CHAINS, SEED = 4000, 2000, 4, 20260925
TARGET_ACCEPT = 0.90

# 90%, o mesmo nivel da (R) e da (F) -- as tres faixas aparecem na mesma tela.
HDI = 0.90

# Quantos desenhos o simulador le. O mesmo numero das outras duas.
N_DESENHOS = 1000

PRIORI_PESO = ("N", 0.0, 1.0)    # e1 e e2 sao PESOS: a escala util e [0, 1]
PRIORI_SIGMA = ("HN", 2.0)       # meia-normal; o RMSE do MQ e 0,569

VARIANTES = {
    "livre": dict(escala=1.0, desc="Normais N(0, 1) sobre os dois pesos"),
    "larga": dict(escala=4.0, desc="As mesmas, com o desvio multiplicado por 4"),
}
BASE = "livre"

# Os nomes dos dois pesos, na ordem em que a tela os le. Importados de `expectations`
# em vez de reescritos: duas listas divergem.
PARES = [p for p, _c in eq_exp.TERMOS]


# ─────────────────────────────────────────────────────────────────────────────
# dados
# ─────────────────────────────────────────────────────────────────────────────
def dados(df: pd.DataFrame | None = None) -> dict:
    """A MESMA matriz do MQ, pela mesma `expectations.montar()`.

    Ler o painel do CSV versionado e o default, para o modulo rodar sem banco e para
    duas execucoes darem o mesmo numero -- igual ao `taylor_bayes`.
    """
    if df is None:
        df = panel.carregar()
    d = eq_exp.montar(df)

    meta = d[eq_exp.META]
    y = (d["pi_e"] - meta).rename("__y")
    X = pd.DataFrame(index=d.index)
    for par, col in eq_exp.TERMOS:
        X[par] = d[col] - meta

    am = pd.concat([y, X], axis=1).dropna()
    dd = d.loc[am.index]

    return {
        "y": am["__y"].to_numpy(float),
        "X": {p: am[p].to_numpy(float) for p in PARES},
        "pares": list(PARES),
        "idx": am.index, "n": len(am),
        "ini": am.index[0], "fim": am.index[-1],
        "meta": dd[eq_exp.META].to_numpy(float),
        "pi_e": dd["pi_e"].to_numpy(float),
        "i12": dd["i12"].to_numpy(float),
        "pi_e_l1": dd["pi_e_l1"].to_numpy(float),
        "d": d,
    }


def prioris(escala: float = 1.0) -> dict:
    """A priori de cada parametro, ja resolvida em numeros.

    Devolvida em vez de embutida no modelo para o `main()` poder IMPRIMIR o desvio de
    cada uma ao lado do posterior: uma priori que aperta so se descobre comparando.
    """
    out = {p: ("N", 0.0, float(PRIORI_PESO[2] * escala)) for p in PARES}
    out["sigma"] = PRIORI_SIGMA
    return out


# ─────────────────────────────────────────────────────────────────────────────
# o modelo
# ─────────────────────────────────────────────────────────────────────────────
def construir_modelo(dd: dict, variante: str = BASE):
    import pymc as pm  # local: importar PyMC custa segundos

    if variante not in VARIANTES:
        raise ValueError("variante desconhecida: %r" % variante)
    pri = prioris(VARIANTES[variante]["escala"])

    def rv(nome):
        spec = pri[nome]
        if spec[0] == "N":
            return pm.Normal(nome, spec[1], spec[2])
        if spec[0] == "HN":
            return pm.HalfNormal(nome, spec[1])
        raise ValueError("familia de priori desconhecida: %r" % spec[0])

    X = dd["X"]
    with pm.Model() as m:
        e1 = rv("e1")
        e2 = rv("e2")
        # `peso_meta` NAO e amostrado: ele e o que sobra de 1. E isso que faz a equacao
        # devolver a meta em repouso desenho a desenho, e nao so na mediana.
        pm.Deterministic("peso_meta", 1.0 - e1 - e2)
        # As duas leituras que a aba publica, propagadas em vez de calculadas da
        # mediana: `e2/(1-e1)` e uma razao, e a razao das medianas nao e a mediana da
        # razao.
        pm.Deterministic("repasse_lp", e2 / (1.0 - e1))
        mu = e1 * X["e1"] + e2 * X["e2"]
        sigma = rv("sigma")
        pm.Normal("y_obs", mu=mu, sigma=sigma, observed=dd["y"])
    return m


def amostrar(dd: dict, variante: str = BASE, draws: int = DRAWS, tune: int = TUNE,
             chains: int = CHAINS, seed: int = SEED, prior_pred: bool = True):
    import pymc as pm

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with construir_modelo(dd, variante):
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


def _stats(x: np.ndarray, hdi: float = HDI) -> dict:
    import arviz as az
    x = np.asarray(x, float)
    fin = x[np.isfinite(x)]
    lo, hi = az.hdi(fin, hdi_prob=hdi)
    return {"media": float(fin.mean()), "sd": float(fin.std(ddof=1)),
            "mediana": float(np.median(fin)),
            "hdi_lo": float(lo), "hdi_hi": float(hi)}


def nomes_par() -> list:
    return list(PARES) + ["sigma"]


def _meia_vida_draws(e1: np.ndarray, passos: int = 400) -> np.ndarray:
    """Meia-vida por desenho, pela MESMA regra simulada de `expectations._meia_vida`.

    Simulada e nao pela raiz, para continuar valendo se a equacao ganhar uma segunda
    defasagem -- e, aqui, para a distribuicao sair do mesmo lugar de onde sai o numero
    que a aba do MQ imprime.
    """
    out = np.full(e1.shape, np.nan)
    h = np.ones_like(e1, dtype=float)
    vivo = np.ones_like(e1, dtype=bool)
    for t in range(passos):
        h = e1 * h
        atingiu = vivo & (np.abs(h) <= 0.5)
        out[atingiu] = t + 1
        vivo &= ~atingiu
        if not vivo.any():
            break
    return out


def repouso_draws(post: dict, alvos=(2.0, 3.0, 4.5, 8.5), tol: float = 1e-9) -> dict:
    """A equacao devolve a META em repouso, DESENHO A DESENHO.

    Teste de algebra e nao de dado -- mas e a propriedade que justifica a restricao, e
    num simulador ela vale por desenho e nao pela mediana: e cada desenho que roda.
    Afirmada em vez de argumentada, como o `repouso()` do modulo de MQ.
    """
    e1, e2 = post["e1"], post["e2"]
    pm_ = 1.0 - e1 - e2
    pior = 0.0
    for alvo in alvos:
        h = np.full(e1.shape, float(alvo))
        for _ in range(2000):
            h = e1 * h + e2 * alvo + pm_ * alvo
        pior = max(pior, float(np.nanmax(np.abs(h - alvo))))
    # e o repasse simulado contra a formula, no mesmo espirito
    h = np.full(e1.shape, 3.0)
    for _ in range(2000):
        h = e1 * h + e2 * 4.0 + pm_ * 3.0
    sim = h - 3.0
    formula = e2 / (1.0 - e1)
    d = np.abs(sim - formula)
    return {"pior_desvio_da_meta": pior, "devolve_a_meta": bool(pior <= tol),
            "pior_repasse": float(np.nanmax(d)),
            "repasse_bate": bool(np.nanmax(d) <= 1e-6)}


def resumo(idata, dd: dict, variante: str) -> dict:
    """Tudo o que a tela precisa, ja lido do posterior."""
    import arviz as az

    nomes = nomes_par()
    derivados = ["peso_meta", "repasse_lp"]
    post = {n: _flat(idata, n) for n in nomes + derivados}
    sm = az.summary(idata, var_names=nomes, hdi_prob=HDI)
    pri = prioris(VARIANTES[variante]["escala"])

    par = {}
    for n in nomes:
        s = _stats(post[n])
        s["rhat"] = float(sm.loc[n, "r_hat"])
        s["ess"] = float(sm.loc[n, "ess_bulk"])
        s["priori"] = list(pri[n])
        # Quanto a priori apertou: o posterior mais estreito que ela e o dado falando;
        # um posterior TAO largo quanto a priori e a priori falando sozinha.
        if pri[n][0] == "N":
            s["priori_sd"] = float(pri[n][2])
            s["encolheu"] = float(s["sd"] / pri[n][2]) if pri[n][2] else float("nan")
        par[n] = s
    for n in derivados:
        par[n] = _stats(post[n])

    mv = _meia_vida_draws(post["e1"])
    par["meia_vida"] = _stats(mv[np.isfinite(mv)])

    # ajuste na MEDIA do posterior, para o RMSE ser comparavel ao do MQ
    fit = par["e1"]["media"] * dd["X"]["e1"] + par["e2"]["media"] * dd["X"]["e2"]
    resid = dd["y"] - fit
    # DOIS R2, e eles nao sao o mesmo numero. `r2_cent` explica o DESVIO contra a meta,
    # que e a dependente desta regressao; `r2_pie` explica a propria expectativa,
    # somando a meta de volta -- e e este o comparavel ao que a aba do MQ publica.
    # Poe-los lado a lado sem dizer qual e qual e o modo classico de a prosa
    # contradizer a tabela ao lado dela (a (F) ja tinha pisado nisso).
    sqt = float(((dd["y"] - dd["y"].mean()) ** 2).sum())
    pie = dd["pi_e"]
    fit_pie = fit + dd["meta"]
    sqt_pie = float(((pie - pie.mean()) ** 2).sum())

    # Os pesos vivem no simplex? Nada na priori obriga -- entao isto e medicao.
    fora = float(np.mean((post["e1"] < 0) | (post["e2"] < 0) | (post["peso_meta"] < 0)))

    return {
        "variante": variante, "desc": VARIANTES[variante]["desc"],
        "par": par, "nomes": nomes, "derivados": derivados,
        "n": dd["n"], "ini": str(dd["ini"]), "fim": str(dd["fim"]),
        "rmse": float(np.sqrt((resid ** 2).mean())),
        "r2_cent": float(1.0 - (resid ** 2).sum() / sqt) if sqt else float("nan"),
        "r2_pie": float(1.0 - ((pie - fit_pie) ** 2).sum() / sqt_pie)
        if sqt_pie else float("nan"),
        "acf1": float(pd.Series(resid).autocorr(1)),
        "rhat_max": float(max(par[n]["rhat"] for n in nomes)),
        "ess_min": float(min(par[n]["ess"] for n in nomes)),
        "div": int(np.asarray(idata.sample_stats["diverging"]).sum()),
        "fora_simplex": fora,
        "repouso": repouso_draws(post),
        "_draws": {n: post[n] for n in nomes + derivados},
    }


def conferir(res: dict, mq: dict, tol: float = 0.25) -> dict:
    """A mediana do posterior contra o coeficiente de MQ, peso a peso.

    A tolerancia e em DESVIOS DO POSTERIOR e nao em por cento: um peso cujo posterior e
    largo pode discordar em muito sem que isso diga nada, e um peso apertado nao pode
    discordar quase nada. `tol` e a fracao de um desvio.
    """
    out, pior = {}, 0.0
    for p in PARES:
        s = res["par"][p]
        v = float(mq["coef"][p])
        dz = abs(s["mediana"] - v) / s["sd"] if s["sd"] else float("nan")
        out[p] = {"bayes": s["mediana"], "mq": v, "d_sd": float(dz),
                  "ok": bool(dz <= tol),
                  "sinal_igual": bool(np.sign(s["mediana"]) == np.sign(v))}
        pior = max(pior, dz)
    return {"itens": out, "pior_d_sd": float(pior),
            "todos_ok": all(o["ok"] for o in out.values()),
            "sinais_ok": all(o["sinal_igual"] for o in out.values()), "tol": tol}


# ─────────────────────────────────────────────────────────────────────────────
# rodar e gravar
# ─────────────────────────────────────────────────────────────────────────────
def rodar(quais: list[str] | None = None, df: pd.DataFrame | None = None,
          draws: int = DRAWS, tune: int = TUNE, chains: int = CHAINS) -> dict:
    quais = list(VARIANTES) if quais is None else quais
    dd = dados(df)
    mq = eq_exp.estimar(dd["d"])

    res = {}
    for nome in quais:
        idata = amostrar(dd, nome, draws=draws, tune=tune, chains=chains)
        res[nome] = resumo(idata, dd, nome)
        res[nome]["confere"] = conferir(res[nome], mq)
    return {"dd": dd, "res": res, "mq": mq}


def salvar_desenhos(saida: dict, nome: str = BASE, n: int = N_DESENHOS,
                    destino: pathlib.Path | None = None) -> pathlib.Path:
    """Os desenhos afinados da variante base, que e o que o simulador le.

    O relatorio NAO roda MCMC: ele le este arquivo. `peso_meta` vai gravado junto
    mesmo sendo `1 - e1 - e2`, para o navegador nao ter de refazer a conta e poder
    conferir a identidade.
    """
    destino = destino or (DATA / "exp_draws.json")
    destino.parent.mkdir(parents=True, exist_ok=True)
    r = saida["res"][nome]
    d, dd = r["_draws"], saida["dd"]
    pars = nomes_par()
    extras = ["peso_meta", "repasse_lp"]
    tot = int(np.asarray(d["e1"]).size)
    passo = max(1, tot // n)
    sel = np.arange(0, tot, passo)[:n]

    out = {
        "variante": nome, "desc": VARIANTES[nome]["desc"],
        "n_total": tot, "n_gravado": int(sel.size), "passo": int(passo),
        "gerado_de": {"n": dd["n"], "ini": str(dd["ini"]), "fim": str(dd["fim"]),
                      "termos": [list(t) for t in eq_exp.TERMOS],
                      "meta": eq_exp.META, "hac_lags": eq_exp.HAC_LAGS},
        "pars": pars,
        "draws": {k: [round(float(v), 5) for v in np.asarray(d[k])[sel]]
                  for k in pars + extras},
        "mediana": {k: float(np.median(np.asarray(d[k]))) for k in pars + extras},
        "media": {k: float(np.mean(np.asarray(d[k]))) for k in pars + extras},
        "hdi": {k: [r["par"][k]["hdi_lo"], r["par"][k]["hdi_hi"]]
                for k in pars + extras},
        "priori": {k: list(r["par"][k]["priori"]) for k in pars},
        "meia_vida": r["par"]["meia_vida"],
        "repouso": r["repouso"],
        "hdi_prob": HDI,
    }
    destino.write_text(json.dumps(out, ensure_ascii=False, default=float),
                       encoding="utf-8")
    return destino


def salvar(saida: dict, destino: pathlib.Path | None = None) -> pathlib.Path:
    destino = destino or (DATA / "exp_bayes.json")
    destino.parent.mkdir(parents=True, exist_ok=True)
    limpo = {}
    for nome, r in saida["res"].items():
        limpo[nome] = {k: v for k, v in r.items() if not k.startswith("_")}
    mq = saida["mq"]
    limpo["_mq"] = {
        "estimador": mq["estimador"], "hac_lags": mq["hac_lags"],
        "coef": {k: float(v) for k, v in mq["coef"].items()},
        "se": {k: float(v) for k, v in mq["se"].items()},
        "t": {k: float(v) for k, v in mq["t"].items()},
        "peso_meta": mq["peso_meta"], "repasse_lp": mq["repasse_lp"],
        "meia_vida": mq["meia_vida"], "r2": mq["r2"], "rmse": mq["rmse"],
        "lb_p4": mq["lb_p4"], "lb_p8": mq["lb_p8"],
        "n": mq["n"], "ini": str(mq["ini"]), "fim": str(mq["fim"]),
    }
    destino.write_text(json.dumps(limpo, indent=2, ensure_ascii=False, default=float),
                       encoding="utf-8")
    return destino


# ─────────────────────────────────────────────────────────────────────────────
# impressao
# ─────────────────────────────────────────────────────────────────────────────
def imprimir(saida: dict) -> None:
    dd, mq = saida["dd"], saida["mq"]
    print("EQUACAO (E) -- EXPECTATIVAS, POR MCMC")
    print("  amostra   %s a %s (%d trimestres)" % (dd["ini"], dd["fim"], dd["n"]))
    print("  desenho   %d x %d cadeias, %d de aquecimento" % (DRAWS, CHAINS, TUNE))
    print("  restricao os tres pesos somam 1; `peso_meta` NAO e amostrado")

    for nome, r in saida["res"].items():
        print("\n  [%s] %s" % (nome, r["desc"]))
        print("    %-14s %9s %9s %19s %8s %8s %7s"
              % ("parametro", "mediana", "desvio", "HDI %d%%" % round(HDI * 100),
                 "priori", "encolh.", "MQ"))
        for n in r["nomes"]:
            s = r["par"][n]
            alvo = "%+.3f" % mq["coef"][n] if n in mq["coef"] else ""
            pri = ("%.2f" % s["priori_sd"] if "priori_sd" in s
                   else "HN %.1f" % s["priori"][1])
            enc = "%.2f" % s["encolheu"] if "encolheu" in s else "-"
            print("    %-14s %+9.3f %9.3f  [%+8.3f, %+8.3f] %8s %8s %7s"
                  % (n, s["mediana"], s["sd"], s["hdi_lo"], s["hdi_hi"], pri, enc,
                     alvo))
        for n in r["derivados"] + ["meia_vida"]:
            s = r["par"][n]
            alvo = ""
            if n == "peso_meta":
                alvo = "%+.3f" % mq["peso_meta"]
            elif n == "repasse_lp":
                alvo = "%+.3f" % mq["repasse_lp"]
            elif n == "meia_vida":
                alvo = "%+.3f" % mq["meia_vida"]
            print("    %-14s %+9.3f %9.3f  [%+8.3f, %+8.3f] %8s %8s %7s"
                  % (n + " *", s["mediana"], s["sd"], s["hdi_lo"], s["hdi_hi"],
                     "derivado", "-", alvo))
        print("    R2 sobre a expectativa  %.4f (MQ %.4f)  <- o comparavel"
              % (r["r2_pie"], mq["r2"]))
        print("    R2 sobre o desvio       %.4f  (a dependente desta regressao)"
              % r["r2_cent"])
        print("    RMSE %.4f (MQ %.4f)   acf1 %+.3f"
              % (r["rmse"], mq["rmse"], r["acf1"]))
        print("    R-hat max %.4f   ESS min %d   divergencias %d"
              % (r["rhat_max"], int(r["ess_min"]), r["div"]))
        rp = r["repouso"]
        print("    repouso desenho a desenho: pior desvio da meta %.2e -> %s; "
              "repasse bate: %s" % (rp["pior_desvio_da_meta"],
                                    "ok" if rp["devolve_a_meta"] else "FORA",
                                    "sim" if rp["repasse_bate"] else "NAO"))
        print("    massa do posterior FORA do simplex: %.2f%%  "
              "(nao ha restricao obrigando)" % (100 * r["fora_simplex"]))
        cf = r["confere"]
        print("    contra o MQ: pior distancia %.3f desvio(s) do posterior  "
              "(tolerancia %.2f) -> %s; sinais %s"
              % (cf["pior_d_sd"], cf["tol"], "ok" if cf["todos_ok"] else "FORA",
                 "iguais" if cf["sinais_ok"] else "DIFERENTES"))


def main() -> dict:
    saida = rodar()
    imprimir(saida)
    p1 = salvar(saida)
    p2 = salvar_desenhos(saida)
    print("\n  gravado  %s" % p1)
    print("           %s  (%d desenhos)" % (p2, N_DESENHOS))
    return saida


if __name__ == "__main__":
    main()
