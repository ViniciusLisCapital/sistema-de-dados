# -*- coding: utf-8 -*-
"""A equacao (H), a curva IS, estimada por MCMC -- a mesma equacao do MQ.

    (H) H(t) = h1*H(t-1) + h2*gap(t-1) + d08 + d20 + eps,   eps ~ N(0, sigma)

    gap = Selic - (rr_10a + meta_12m)   -- a mesma ancora da regra de juros

Existe pela mesma razao que os outros tres modulos desta pasta: **o simulador precisa de
uma FAIXA, e MQ nao tem uma para dar** que venha da propria dinamica. Decidido pelo
usuario em 2026-09-25, ao pedir a (H) no simulador: *"no sistema vamos sempre usar o
bayes para todas as equacoes"*.

## A equacao e a MESMA, e isso e verificavel

Este modulo NAO remonta a matriz: ele chama `is_curve.montar()`, a mesma funcao do MQ. O
que muda e so o estimador. `conferir()` mede a distancia entre a mediana do posterior e o
coeficiente de MQ, termo a termo, em desvios do posterior.

## A priori, e por que ela e AUTOESCALADA (como a da (F), e nao unica como a da (E))

Os quatro regressores vivem em unidades diferentes: `h1` multiplica o proprio hiato (sem
unidade), `h2` multiplica p.p. de gap, e as duas crises sao degraus de 0 ou 1. Uma priori
unica nao seria neutra -- `N(0, 1)` seria frouxa para a persistencia e apertada demais
para uma dummy, cujo efeito medido passa de um ponto. A regra e a da (F): `N(0,
sd(y)/sd(x))`, medida na amostra do ajuste -- *este termo sozinho poderia explicar toda a
variancia do hiato, mas nao muito mais que isso*. Para `h1` ela da exatamente `N(0, 1)`,
porque o regressor e o proprio hiato defasado. A variante `larga` multiplica tudo por 4 e
existe para MEDIR se a priori pesa, em vez de afirmar que nao pesa.

A (E) usou uma priori so porque la os dois pesos dividem unidade e o intervalo util e
[0, 1]. Aqui nao e o caso, e copiar a regra de la seria copiar a conclusao sem a razao.

## Duas coisas que valem DESENHO A DESENHO, porque e cada desenho que o simulador roda

- **Estabilidade.** Nada na priori obriga `|h1| < 1`. Um desenho explosivo faria um
  caminho do simulador divergir, e a faixa seria arrastada por ele. Quantos desenhos
  caem fora e MEDIDO (`fora_estavel`), nao imposto.
- **Repouso em zero.** Sem intercepto e com `|h1| < 1`, o hiato volta a zero com o aperto
  em zero. `repouso_draws()` afirma isso sobre a amostra inteira do posterior, nao so
  sobre a mediana.

Uso:
    uv run python -m analytics.brasil.structural_model.bayes.is_bayes
"""
from __future__ import annotations

import json
import pathlib
import warnings

import numpy as np
import pandas as pd

from analytics.brasil.structural_model import panel
from analytics.brasil.structural_model.equations import is_curve as eq_is

DATA = pathlib.Path(__file__).resolve().parent / "data"

# 4 cadeias, como o PyMC recomenda para o R-hat valer. Amostra pequena (81) e modelo
# linear com 5 parametros: roda em segundos.
DRAWS, TUNE, CHAINS, SEED = 4000, 2000, 4, 20260926
TARGET_ACCEPT = 0.90

# 90%, o mesmo nivel das outras tres -- as faixas aparecem na mesma tela.
HDI = 0.90

# Quantos desenhos o simulador le. O mesmo numero das outras tres.
N_DESENHOS = 1000

PRIORI_SIGMA = ("HN", 2.0)       # meia-normal; o RMSE do MQ e 0,636

VARIANTES = {
    "dado": dict(escala=1.0, desc="Priori autoescalada: sd(y)/sd(x) por termo"),
    "larga": dict(escala=4.0, desc="A mesma, com o desvio multiplicado por 4"),
}
BASE = "dado"

# (parametro, coluna), na ordem da equacao -- importados em vez de reescritos: duas
# listas divergem. As crises entram depois, com o nome da propria coluna.
TERMOS = list(eq_is.TERMOS) + [(k, k) for k in eq_is.CRISES]
PARS = [p for p, _c in TERMOS]


# ─────────────────────────────────────────────────────────────────────────────
# dados
# ─────────────────────────────────────────────────────────────────────────────
def dados(df: pd.DataFrame | None = None) -> dict:
    """A MESMA matriz do MQ, pela mesma `is_curve.montar()`.

    Ler o painel do CSV versionado e o default, para o modulo rodar sem banco e para
    duas execucoes darem o mesmo numero -- igual aos outros tres.
    """
    if df is None:
        df = panel.carregar()
    d = eq_is.montar(df)
    cols = [c for _p, c in TERMOS]
    am = pd.concat([d["hiato"].rename("__y"), d[cols]], axis=1).dropna()
    y = am["__y"].to_numpy(float)
    X = {p: am[c].to_numpy(float) for p, c in TERMOS}
    return {
        "y": y, "X": X, "pars": list(PARS),
        "sd": {p: float(np.std(X[p], ddof=1)) for p in PARS},
        "sd_y": float(np.std(y, ddof=1)),
        "idx": am.index, "n": len(am), "ini": am.index[0], "fim": am.index[-1],
        "col_aperto": eq_is.COL_APERTO, "lag": eq_is.LAG_GRR,
        "d": d,
    }


def prioris(dd: dict, escala: float = 1.0) -> dict:
    """A priori de cada parametro, ja resolvida em numeros, para o `main()` imprimir."""
    out = {}
    for p in PARS:
        sdx = dd["sd"][p]
        out[p] = ("N", 0.0, float(escala * dd["sd_y"] / sdx) if sdx else 5.0)
    out["sigma"] = PRIORI_SIGMA
    return out


# ─────────────────────────────────────────────────────────────────────────────
# o modelo
# ─────────────────────────────────────────────────────────────────────────────
def construir_modelo(dd: dict, variante: str = BASE):
    import pymc as pm  # local: importar PyMC custa segundos

    if variante not in VARIANTES:
        raise ValueError("variante desconhecida: %r" % variante)
    pri = prioris(dd, VARIANTES[variante]["escala"])

    def rv(nome):
        spec = pri[nome]
        if spec[0] == "N":
            return pm.Normal(nome, spec[1], spec[2])
        if spec[0] == "HN":
            return pm.HalfNormal(nome, spec[1])
        raise ValueError("familia de priori desconhecida: %r" % spec[0])

    with pm.Model() as m:
        b = {p: rv(p) for p in PARS}
        # A leitura que a aba publica, propagada em vez de calculada da mediana: e uma
        # razao, e a razao das medianas nao e a mediana da razao.
        pm.Deterministic("efeito_lp", b["h2"] / (1.0 - b["h1"]))
        mu = sum(b[p] * dd["X"][p] for p in PARS)
        sigma = rv("sigma")
        pm.Normal("y_obs", mu=mu, sigma=sigma, observed=dd["y"])
    return m


def amostrar(dd: dict, variante: str = BASE, draws: int = DRAWS, tune: int = TUNE,
             chains: int = CHAINS, seed: int = SEED):
    import pymc as pm

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with construir_modelo(dd, variante):
            idata = pm.sample(draws=draws, tune=tune, chains=chains, cores=1,
                              target_accept=TARGET_ACCEPT, random_seed=seed,
                              progressbar=False)
    return idata


# ─────────────────────────────────────────────────────────────────────────────
# leitura do posterior
# ─────────────────────────────────────────────────────────────────────────────
def _flat(idata, nome: str) -> np.ndarray:
    return np.asarray(idata.posterior[nome]).reshape(-1)


def _stats(x: np.ndarray, hdi: float = HDI) -> dict:
    import arviz as az
    x = np.asarray(x, float)
    fin = x[np.isfinite(x)]
    lo, hi = az.hdi(fin, hdi_prob=hdi)
    return {"media": float(fin.mean()), "sd": float(fin.std(ddof=1)),
            "mediana": float(np.median(fin)),
            "hdi_lo": float(lo), "hdi_hi": float(hi)}


def nomes_par() -> list:
    return list(PARS) + ["sigma"]


def _meia_vida_draws(h1: np.ndarray, passos: int = 400) -> np.ndarray:
    """Meia-vida por desenho, pela MESMA regra simulada de `is_curve._meia_vida`."""
    out = np.full(h1.shape, np.nan)
    h = np.ones_like(h1, dtype=float)
    vivo = np.ones_like(h1, dtype=bool)
    for t in range(passos):
        h = h1 * h
        atingiu = vivo & (np.abs(h) <= 0.5)
        out[atingiu] = t + 1
        vivo &= ~atingiu
        if not vivo.any():
            break
    return out


# Ate onde 4000 passos de simulacao bastam para AFIRMAR o repouso: 0,99^4000 ~ 3e-18.
# Acima disso a propriedade continua valendo pela algebra, mas uma simulacao finita nao
# a alcanca -- um desenho com h1 = 0,99997 ainda carrega 87% de um hiato depois de 4000
# trimestres. A primeira versao desta funcao nao separava os dois casos e reprovava o
# posterior inteiro por causa de meia duzia de desenhos LENTOS, nao errados.
H1_RAPIDO = 0.99


def repouso_draws(post: dict, tol: float = 1e-8) -> dict:
    """O hiato volta a ZERO em repouso, DESENHO A DESENHO, e o efeito de longo prazo
    simulado bate com `h2/(1-h1)` -- as duas propriedades do `repouso()` do MQ.

    Tres grupos, contados em vez de misturados:

    - **explosivos** (`|h1| >= 1`): nao tem repouso. Ficam no posterior -- tira-los seria
      impor estacionariedade como priori, que o dado nao pediu -- e o efeito deles em
      12 trimestres e medido pelo simulador, nao aqui.
    - **lentos** (`H1_RAPIDO < |h1| < 1`): voltam a zero pela algebra, e a simulacao
      finita nao consegue afirmar isso.
    - **o resto**: onde a afirmacao e feita, com a tolerancia de sempre.
    """
    h1, h2 = post["h1"], post["h2"]
    a = np.abs(h1)
    rap = a <= H1_RAPIDO
    h1r, h2r = h1[rap], h2[rap]
    pior0 = 0.0
    for h0 in (-3.0, -1.0, 1.0, 5.0):
        h = np.full(h1r.shape, h0)
        for _ in range(4000):
            h = h1r * h
        pior0 = max(pior0, float(np.nanmax(np.abs(h))))
    h = np.zeros(h1r.shape)
    for _ in range(4000):
        h = h1r * h + h2r * 1.0
    formula = h2r / (1.0 - h1r)
    d = float(np.nanmax(np.abs(h - formula)))
    return {"pior_desvio_de_zero": pior0, "volta_a_zero": bool(pior0 <= tol),
            "pior_lp": d, "lp_bate": bool(d <= 1e-5),
            "n_afirmados": int(rap.sum()),
            "frac_lentos": float(np.mean((a > H1_RAPIDO) & (a < 1.0))),
            "frac_explosivos": float(np.mean(a >= 1.0)),
            "h1_rapido": H1_RAPIDO}


def resumo(idata, dd: dict, variante: str) -> dict:
    """Tudo o que a tela precisa, ja lido do posterior."""
    import arviz as az

    nomes = nomes_par()
    post = {n: _flat(idata, n) for n in nomes + ["efeito_lp"]}
    sm = az.summary(idata, var_names=nomes, hdi_prob=HDI)
    pri = prioris(dd, VARIANTES[variante]["escala"])

    par = {}
    for n in nomes:
        s = _stats(post[n])
        s["rhat"] = float(sm.loc[n, "r_hat"])
        s["ess"] = float(sm.loc[n, "ess_bulk"])
        s["priori"] = list(pri[n])
        if pri[n][0] == "N":
            s["priori_sd"] = float(pri[n][2])
            s["encolheu"] = float(s["sd"] / pri[n][2]) if pri[n][2] else float("nan")
        par[n] = s

    est = np.abs(post["h1"]) < 1.0
    par["efeito_lp"] = _stats(post["efeito_lp"][est])
    mv = _meia_vida_draws(post["h1"])
    par["meia_vida"] = _stats(mv[np.isfinite(mv)])

    # ajuste na MEDIA do posterior, para o RMSE ser comparavel ao do MQ
    fit = sum(par[p]["media"] * dd["X"][p] for p in PARS)
    resid = dd["y"] - fit
    sqt = float(((dd["y"] - dd["y"].mean()) ** 2).sum())

    return {
        "variante": variante, "desc": VARIANTES[variante]["desc"],
        "par": par, "nomes": nomes, "derivados": ["efeito_lp", "meia_vida"],
        "n": dd["n"], "ini": str(dd["ini"]), "fim": str(dd["fim"]),
        "rmse": float(np.sqrt((resid ** 2).mean())),
        "r2": float(1.0 - (resid ** 2).sum() / sqt) if sqt else float("nan"),
        "acf1": float(pd.Series(resid).autocorr(1)),
        "rhat_max": float(max(par[n]["rhat"] for n in nomes)),
        "ess_min": float(min(par[n]["ess"] for n in nomes)),
        "div": int(np.asarray(idata.sample_stats["diverging"]).sum()),
        "fora_estavel": float(np.mean(~est)),
        # quanto da massa diz que o aperto ESFRIA o produto -- a pergunta da equacao
        "h2_negativo": float(np.mean(post["h2"] < 0)),
        "repouso": repouso_draws(post),
        "_draws": {n: post[n] for n in nomes + ["efeito_lp"]},
    }


def conferir(res: dict, mq: dict, tol: float = 0.25) -> dict:
    """A mediana do posterior contra o coeficiente de MQ, termo a termo, em DESVIOS DO
    POSTERIOR -- um termo de posterior largo pode discordar em muito sem que isso diga
    nada, e um apertado nao pode discordar quase nada."""
    out, pior = {}, 0.0
    for p in PARS:
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
    mq = eq_is.estimar(dd["d"])

    res = {}
    for nome in quais:
        idata = amostrar(dd, nome, draws=draws, tune=tune, chains=chains)
        res[nome] = resumo(idata, dd, nome)
        res[nome]["confere"] = conferir(res[nome], mq)
    return {"dd": dd, "res": res, "mq": mq}


def salvar_desenhos(saida: dict, nome: str = BASE, n: int = N_DESENHOS,
                    destino: pathlib.Path | None = None) -> pathlib.Path:
    """Os desenhos afinados da variante base, que e o que o simulador le.

    O relatorio NAO roda MCMC: ele le este arquivo. `efeito_lp` vai gravado junto para
    o navegador poder conferir a identidade em vez de confiar nela.
    """
    destino = destino or (DATA / "is_draws.json")
    destino.parent.mkdir(parents=True, exist_ok=True)
    r = saida["res"][nome]
    d, dd = r["_draws"], saida["dd"]
    pars = nomes_par()
    extras = ["efeito_lp"]
    tot = int(np.asarray(d["h1"]).size)
    passo = max(1, tot // n)
    sel = np.arange(0, tot, passo)[:n]

    out = {
        "variante": nome, "desc": VARIANTES[nome]["desc"],
        "n_total": tot, "n_gravado": int(sel.size), "passo": int(passo),
        "gerado_de": {"n": dd["n"], "ini": str(dd["ini"]), "fim": str(dd["fim"]),
                      "termos": [list(t) for t in TERMOS],
                      "col_aperto": dd["col_aperto"], "lag": dd["lag"],
                      "hac_lags": eq_is.HAC_LAGS},
        "pars": pars,
        "draws": {k: [round(float(v), 6) for v in np.asarray(d[k])[sel]]
                  for k in pars + extras},
        "mediana": {k: float(np.median(np.asarray(d[k]))) for k in pars + extras},
        "media": {k: float(np.mean(np.asarray(d[k]))) for k in pars + extras},
        "hdi": {k: [r["par"][k]["hdi_lo"], r["par"][k]["hdi_hi"]]
                for k in pars + extras},
        "priori": {k: list(r["par"][k]["priori"]) for k in pars},
        "meia_vida": r["par"]["meia_vida"],
        "repouso": r["repouso"],
        "fora_estavel": r["fora_estavel"],
        "h2_negativo": r["h2_negativo"],
        "hdi_prob": HDI,
    }
    destino.write_text(json.dumps(out, ensure_ascii=False, default=float),
                       encoding="utf-8")
    return destino


def salvar(saida: dict, destino: pathlib.Path | None = None) -> pathlib.Path:
    destino = destino or (DATA / "is_bayes.json")
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
        "meia_vida": mq["meia_vida"], "efeito_lp": mq["efeito_lp"],
        "r2": mq["r2"], "rmse": mq["rmse"],
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
    print("EQUACAO (H) -- CURVA IS, POR MCMC")
    print("  amostra   %s a %s (%d trimestres)" % (dd["ini"], dd["fim"], dd["n"]))
    print("  aperto    %s, defasado %d trimestre" % (dd["col_aperto"], dd["lag"]))
    print("  desenho   %d x %d cadeias, %d de aquecimento" % (DRAWS, CHAINS, TUNE))

    for nome, r in saida["res"].items():
        print("\n  [%s] %s" % (nome, r["desc"]))
        print("    %-10s %9s %9s %21s %8s %8s %8s"
              % ("parametro", "mediana", "desvio", "HDI %d%%" % round(HDI * 100),
                 "priori", "encolh.", "MQ"))
        for n in r["nomes"]:
            s = r["par"][n]
            alvo = "%+.4f" % mq["coef"][n] if n in mq["coef"] else ""
            pri = ("%.2f" % s["priori_sd"] if "priori_sd" in s
                   else "HN %.1f" % s["priori"][1])
            enc = "%.2f" % s["encolheu"] if "encolheu" in s else "-"
            print("    %-10s %+9.4f %9.4f  [%+8.4f, %+8.4f] %8s %8s %8s"
                  % (n, s["mediana"], s["sd"], s["hdi_lo"], s["hdi_hi"], pri, enc, alvo))
        for n, alvo in (("efeito_lp", mq["efeito_lp"]), ("meia_vida", mq["meia_vida"])):
            s = r["par"][n]
            print("    %-10s %+9.4f %9.4f  [%+8.4f, %+8.4f] %8s %8s %+8.4f"
                  % (n + " *", s["mediana"], s["sd"], s["hdi_lo"], s["hdi_hi"],
                     "derivado", "-", alvo))
        print("    R2 %.4f (MQ %.4f)   RMSE %.4f (MQ %.4f)   acf1 %+.3f"
              % (r["r2"], mq["r2"], r["rmse"], mq["rmse"], r["acf1"]))
        print("    R-hat max %.4f   ESS min %d   divergencias %d"
              % (r["rhat_max"], int(r["ess_min"]), r["div"]))
        print("    massa com |h1| >= 1 (explosiva): %.2f%%   massa com h2 < 0: %.1f%%"
              % (100 * r["fora_estavel"], 100 * r["h2_negativo"]))
        rp = r["repouso"]
        print("    repouso desenho a desenho, nos %d com |h1| <= %.2f: pior desvio de zero "
              "%.2e -> %s; longo prazo bate: %s"
              % (rp["n_afirmados"], rp["h1_rapido"], rp["pior_desvio_de_zero"],
                 "ok" if rp["volta_a_zero"] else "FORA",
                 "sim" if rp["lp_bate"] else "NAO"))
        print("    lentos demais para a simulacao afirmar: %.2f%%   explosivos: %.2f%%"
              % (100 * rp["frac_lentos"], 100 * rp["frac_explosivos"]))
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
