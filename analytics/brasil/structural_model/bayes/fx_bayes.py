# -*- coding: utf-8 -*-
"""A equacao (F), o cambio, estimada por MCMC -- a mesma equacao do Ridge.

    (F) de(t) - dppp(t) = alpha + phi*de(t-1) + sum_c beta_c*z_c(t) + eps
        eps ~ N(0, sigma)

Existe pela mesma razao que `taylor_bayes.py`: **o simulador precisa de uma FAIXA, e
Ridge nao tem uma para dar.** Ridge e estimativa pontual; o que o `equations/fx.py`
imprime ao lado dela sao t de MQ com HAC, que sao legiveis so porque o lambda escolhido
pousa no piso da grade -- isto e, porque a penalidade e nominal. Uma faixa colada por
fora daquilo seria margem, e nao incerteza propagada pela dinamica.

Decidido pelo usuario em 2026-09-24, ao pedir o simulador rodando com as duas equacoes:
entre entrar com o coeficiente pontual e reestimar, reestimar -- *"as duas equacoes
passam a carregar o mesmo tipo de incerteza"*.

## A equacao e a MESMA, e isso e verificavel

Este modulo NAO remonta a matriz: ele chama `fx.montar()`, a mesma funcao que o Ridge
usa, e corta na mesma data (`fx.corte()`). O que muda e so o estimador. `conferir()`
mede a distancia entre a mediana do posterior e o beta do Ridge, canal a canal, e o
`main()` imprime as duas colunas lado a lado -- se elas divergirem muito, ou a priori
esta apertando ou a matriz deixou de ser a mesma, e as duas hipoteses sao visiveis.

## A priori, e por que ela e AUTOESCALADA

Os betas vivem em escalas muito diferentes mesmo depois da padronizacao, porque o `sd`
que escala cada canal vem da janela de referencia (2000 em diante) e nao da amostra:
o CDS tem 2002 dentro da referencia, entao o `sd` dele e grande e o beta correspondente
tambem (+25 contra +1,9 da bolsa). Uma priori unica -- `N(0, 5)` para todos -- nao seria
neutra: ela seria frouxa para a bolsa e apertaria o canal fiscal em mais de cinco
desvios.

A priori de cada canal e entao `N(0, sd(y)/sd(z_c))`, medida na amostra do ajuste. Em
palavras, ela afirma: *este canal sozinho poderia explicar toda a variancia do cambio,
mas nao muito mais que isso.* E a escala que o `rstanarm` chama de autoescalada, e ela
e fraca de proposito -- com 81 trimestres e 7 parametros, quem manda e o dado. A
variante `larga` multiplica todos por 4 e existe para medir isso em vez de afirma-lo.

**O que ela NAO e:** a priori implicita do Ridge. Ridge com lambda L equivale a uma
normal de desvio sigma/sqrt(L*n), e aqui L pousa no PISO da grade -- a priori implicita
e praticamente plana, entao reproduzi-la nao acrescentaria informacao nenhuma. O que
esta escrito acima e uma escolha, e esta declarada como tal.

## O offset de PPP continua imposto em 1

`d_ppp` nao e regressor: ele entra do lado esquerdo, como no Ridge. Isso e o que faz o
`alpha` ser lido como deriva residual e e o que mantem as duas estimacoes comparaveis.
O posterior de `alpha` medindo zero e uma afirmacao sobre o modelo, nao uma suposicao.

Uso:
    uv run python -m analytics.brasil.structural_model.bayes.fx_bayes
"""
from __future__ import annotations

import json
import pathlib
import warnings

import numpy as np
import pandas as pd

from analytics.brasil.structural_model.equations import fx

DATA = pathlib.Path(__file__).resolve().parent / "data"

# 4 cadeias, como o PyMC recomenda para o R-hat valer. A amostra e pequena (81) e o
# modelo e linear com 7 parametros, entao isto roda em segundos.
DRAWS, TUNE, CHAINS, SEED = 4000, 2000, 4, 20260924
TARGET_ACCEPT = 0.90

# 90%, o mesmo nivel da (R) -- as duas faixas aparecem na mesma tela.
HDI = 0.90

# Quantos desenhos o simulador le. O mesmo numero da (R), pelo mesmo motivo: 1000
# caminhos ja dao um contorno estavel e o JSON nao passa de alguns megabytes.
N_DESENHOS = 1000

# Priori de quem nao escala com canal nenhum.
PRIORI_ALPHA = ("N", 0.0, 5.0)     # p.p. por trimestre; o Ridge da -0,116
PRIORI_PHI = ("N", 0.0, 0.5)       # persistencia da propria variacao
PRIORI_SIGMA = ("HN", 5.0)         # meia-normal; o RMSE do Ridge e 3,45

VARIANTES = {
    "dado": dict(escala=1.0,
                 desc="Priori autoescalada: sd(y)/sd(z) por canal"),
    "larga": dict(escala=4.0,
                  desc="A mesma, com o desvio multiplicado por 4"),
}
BASE = "dado"

# O nome que cada coeficiente tem no payload do simulador. `b_<canal>` e nao `<canal>`
# para o par (coeficiente, caminho) nunca colidir no mesmo dicionario do navegador.
def _bname(col: str) -> str:
    return "b_" + col[2:] if col.startswith("d_") else "b_" + col


# ─────────────────────────────────────────────────────────────────────────────
# dados
# ─────────────────────────────────────────────────────────────────────────────
def dados(ate: str | None = None) -> dict:
    """A MESMA matriz do Ridge, pela mesma `fx.montar()`, no mesmo corte."""
    z, stats, reg = fx.montar()
    ate = fx.corte() if ate is None else ate
    z = z[z.index <= pd.Period(ate, "Q")]

    canais = [c for c in reg if c != "de_l1"]
    y = (z["de"] - z[fx.OFFSET]).to_numpy(float)

    return {
        "y": y,
        "X": {c: z[c].to_numpy(float) for c in reg},
        "reg": reg, "canais": canais,
        "sd": {c: float(stats[c][1]) for c in reg},
        "sd_y": float(np.std(y, ddof=1)),
        "idx": z.index, "n": len(z),
        "ini": z.index[0], "fim": z.index[-1],
        "corte": str(ate), "offset": fx.OFFSET,
        "vol_source": fx.VOL_SOURCE, "vol_lag": fx.VOL_LAG_Q,
        "vol_prazo": fx.VOL_PRAZO, "como": fx.COMO,
        "z": z,
    }


def prioris(dd: dict, escala: float = 1.0) -> dict:
    """A priori de cada parametro, ja resolvida em numeros.

    Devolvida em vez de embutida no modelo para o `main()` poder IMPRIMIR o desvio de
    cada uma ao lado do posterior: uma priori que aperta so se descobre comparando.
    """
    out = {"alpha": PRIORI_ALPHA, "phi": PRIORI_PHI, "sigma": PRIORI_SIGMA}
    for c in dd["canais"]:
        sd_z = float(np.std(dd["X"][c], ddof=1))
        largura = dd["sd_y"] / sd_z if sd_z > 0 else 10.0
        out[_bname(c)] = ("N", 0.0, float(largura * escala))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# o modelo
# ─────────────────────────────────────────────────────────────────────────────
def construir_modelo(dd: dict, variante: str = BASE):
    import pymc as pm

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

    X = dd["X"]
    with pm.Model() as m:
        alpha = rv("alpha")
        phi = rv("phi")
        mu = alpha + phi * X["de_l1"]
        for c in dd["canais"]:
            mu = mu + rv(_bname(c)) * X[c]
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


def nomes_par(dd: dict) -> list:
    return ["alpha", "phi"] + [_bname(c) for c in dd["canais"]] + ["sigma"]


def resumo(idata, dd: dict, variante: str) -> dict:
    """Tudo o que a tela precisa, ja lido do posterior."""
    import arviz as az

    nomes = nomes_par(dd)
    post = {n: _flat(idata, n) for n in nomes}
    sm = az.summary(idata, var_names=nomes, hdi_prob=HDI)
    pri = prioris(dd, VARIANTES[variante]["escala"])

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

    # ajuste na MEDIA do posterior, para o RMSE ser comparavel ao do Ridge
    fit = np.full(dd["n"], par["alpha"]["media"]) + par["phi"]["media"] * dd["X"]["de_l1"]
    for c in dd["canais"]:
        fit = fit + par[_bname(c)]["media"] * dd["X"][c]
    resid = dd["y"] - fit
    sqt = float(((dd["y"] - dd["y"].mean()) ** 2).sum())

    # DOIS R2, e eles nao sao o mesmo numero. `r2_cent` explica `de - dppp`, que e a
    # dependente desta regressao; `r2_de` explica `de`, somando o offset de volta --
    # e e este o comparavel ao que o Ridge imprime. Poe-los lado a lado sem dizer qual
    # e qual e o modo classico de a prosa contradizer a tabela ao lado dela.
    de = dd["z"]["de"].to_numpy(float)
    fit_de = fit + dd["z"][dd["offset"]].to_numpy(float)
    sqt_de = float(((de - de.mean()) ** 2).sum())

    return {
        "variante": variante, "desc": VARIANTES[variante]["desc"],
        "par": par, "nomes": nomes,
        "n": dd["n"], "ini": str(dd["ini"]), "fim": str(dd["fim"]),
        "rmse": float(np.sqrt((resid ** 2).mean())),
        "r2_cent": float(1.0 - (resid ** 2).sum() / sqt) if sqt else float("nan"),
        "r2_de": float(1.0 - ((de - fit_de) ** 2).sum() / sqt_de) if sqt_de else float("nan"),
        "acf1": float(pd.Series(resid).autocorr(1)),
        "rhat_max": float(max(par[n]["rhat"] for n in nomes)),
        "ess_min": float(min(par[n]["ess"] for n in nomes)),
        "div": int(np.asarray(idata.sample_stats["diverging"]).sum()),
        "_draws": {n: post[n] for n in nomes},
    }


def conferir(res: dict, rid: dict, dd: dict, tol: float = 0.25) -> dict:
    """A mediana do posterior contra o beta do Ridge, canal a canal.

    A tolerancia e em DESVIOS DO POSTERIOR e nao em por cento: um canal cujo posterior
    e largo pode discordar em muito sem que isso diga nada, e um canal apertado nao
    pode discordar quase nada. `tol` e a fracao de um desvio.
    """
    out, pior = {}, 0.0
    alvo = {"alpha": rid["alpha"], "phi": rid["beta"]["de_l1"]}
    for c in dd["canais"]:
        alvo[_bname(c)] = rid["beta"][c]
    for n, v in alvo.items():
        s = res["par"][n]
        dz = abs(s["mediana"] - v) / s["sd"] if s["sd"] else float("nan")
        out[n] = {"bayes": s["mediana"], "ridge": float(v), "d_sd": float(dz),
                  "ok": bool(dz <= tol),
                  "sinal_igual": bool(np.sign(s["mediana"]) == np.sign(v))}
        pior = max(pior, dz)
    return {"itens": out, "pior_d_sd": float(pior),
            "todos_ok": all(o["ok"] for o in out.values()),
            "sinais_ok": all(o["sinal_igual"] for o in out.values()), "tol": tol}


# ─────────────────────────────────────────────────────────────────────────────
# rodar e gravar
# ─────────────────────────────────────────────────────────────────────────────
def rodar(quais: list[str] | None = None, ate: str | None = None,
          draws: int = DRAWS, tune: int = TUNE, chains: int = CHAINS) -> dict:
    quais = list(VARIANTES) if quais is None else quais
    dd = dados(ate)
    z, stats, reg = fx.montar()
    rid = fx.estimar(z=z, reg=reg, ate=dd["corte"])

    res = {}
    for nome in quais:
        idata = amostrar(dd, nome, draws=draws, tune=tune, chains=chains)
        res[nome] = resumo(idata, dd, nome)
        res[nome]["confere"] = conferir(res[nome], rid, dd)
    return {"dd": dd, "res": res, "ridge": rid, "stats": stats}


def salvar_desenhos(saida: dict, nome: str = BASE, n: int = N_DESENHOS,
                    destino: pathlib.Path | None = None) -> pathlib.Path:
    """Os desenhos afinados da variante base, que e o que o simulador le.

    Junto vao o `sd` de cada canal e a regra de variacao (nivel ou log-retorno): sem
    eles o navegador nao consegue transformar o NIVEL que o leitor digita na coluna
    padronizada que o coeficiente multiplica, e a conta ficaria em outra unidade sem
    nada na tela avisando.
    """
    destino = destino or (DATA / "fx_draws.json")
    destino.parent.mkdir(parents=True, exist_ok=True)
    r = saida["res"][nome]
    d, dd = r["_draws"], saida["dd"]
    pars = nomes_par(dd)
    tot = int(np.asarray(d["alpha"]).size)
    passo = max(1, tot // n)
    sel = np.arange(0, tot, passo)[:n]

    out = {
        "variante": nome, "desc": VARIANTES[nome]["desc"],
        "n_total": tot, "n_gravado": int(sel.size), "passo": int(passo),
        "gerado_de": {"n": dd["n"], "ini": str(dd["ini"]), "fim": str(dd["fim"]),
                      "corte": dd["corte"], "offset": dd["offset"],
                      "vol_source": dd["vol_source"], "vol_lag": dd["vol_lag"],
                      "vol_prazo": dd.get("vol_prazo"),
                      "como": dd["como"], "canais": list(dd["canais"])},
        "pars": pars,
        "draws": {k: [round(float(v), 5) for v in np.asarray(d[k])[sel]] for k in pars},
        "mediana": {k: float(np.median(np.asarray(d[k]))) for k in pars},
        "media": {k: float(np.mean(np.asarray(d[k]))) for k in pars},
        "hdi": {k: [r["par"][k]["hdi_lo"], r["par"][k]["hdi_hi"]] for k in pars},
        "priori": {k: list(r["par"][k]["priori"]) for k in pars},
        "sd_canal": {c: dd["sd"][c] for c in dd["reg"]},
        "log_ret": sorted(fx.LOG_RET),
        "hdi_prob": HDI,
    }
    destino.write_text(json.dumps(out, ensure_ascii=False, default=float),
                       encoding="utf-8")
    return destino


def salvar(saida: dict, destino: pathlib.Path | None = None) -> pathlib.Path:
    destino = destino or (DATA / "fx_bayes.json")
    destino.parent.mkdir(parents=True, exist_ok=True)
    limpo = {}
    for nome, r in saida["res"].items():
        limpo[nome] = {k: v for k, v in r.items() if not k.startswith("_")}
    rid = saida["ridge"]
    limpo["_ridge"] = {
        "estimador": rid["estimador"], "lam": rid["lam"], "piso": rid["piso"],
        "alpha": rid["alpha"], "beta": {k: float(v) for k, v in rid["beta"].items()},
        "t": {k: float(v) for k, v in rid["t"].items()},
        "r2": rid["r2"], "rmse": rid["rmse"], "n": rid["n"],
        "ini": str(rid["ini"]), "fim": str(rid["fim"]),
    }
    destino.write_text(json.dumps(limpo, indent=2, ensure_ascii=False, default=float),
                       encoding="utf-8")
    return destino


# ─────────────────────────────────────────────────────────────────────────────
# impressao
# ─────────────────────────────────────────────────────────────────────────────
def imprimir(saida: dict) -> None:
    dd, rid = saida["dd"], saida["ridge"]
    print("EQUACAO (F) -- CAMBIO, POR MCMC")
    print("  amostra   %s a %s (%d trimestres), corte %s"
          % (dd["ini"], dd["fim"], dd["n"], dd["corte"]))
    print("  desenho   %d x %d cadeias, %d de aquecimento" % (DRAWS, CHAINS, TUNE))
    print("  offset    %s imposto em 1" % dd["offset"])

    for nome, r in saida["res"].items():
        print("\n  [%s] %s" % (nome, r["desc"]))
        print("    %-14s %9s %9s %19s %8s %8s %7s"
              % ("parametro", "mediana", "desvio", "HDI %d%%" % round(HDI * 100),
                 "priori", "encolh.", "Ridge"))
        for n in r["nomes"]:
            s = r["par"][n]
            alvo = ""
            if n == "alpha":
                alvo = "%+.3f" % rid["alpha"]
            elif n == "phi":
                alvo = "%+.3f" % rid["beta"]["de_l1"]
            elif n.startswith("b_"):
                col = "d_" + n[2:]
                if col in rid["beta"]:
                    alvo = "%+.3f" % rid["beta"][col]
            pri = "%.2f" % s["priori_sd"] if "priori_sd" in s else "HN %.1f" % s["priori"][1]
            enc = "%.2f" % s["encolheu"] if "encolheu" in s else "-"
            print("    %-14s %+9.3f %9.3f  [%+8.3f, %+8.3f] %8s %8s %7s"
                  % (n, s["mediana"], s["sd"], s["hdi_lo"], s["hdi_hi"], pri, enc, alvo))
        print("    R2 sobre de        %.4f (Ridge %.4f)  <- o comparavel"
              % (r["r2_de"], rid["r2"]))
        print("    R2 sobre de-dppp   %.4f  (a dependente desta regressao)"
              % r["r2_cent"])
        print("    RMSE %.3f (Ridge %.3f)   acf1 %+.3f"
              % (r["rmse"], rid["rmse"], r["acf1"]))
        print("    R-hat max %.4f   ESS min %d   divergencias %d"
              % (r["rhat_max"], int(r["ess_min"]), r["div"]))
        cf = r["confere"]
        print("    contra o Ridge: pior distancia %.3f desvio(s) do posterior  "
              "(tolerancia %.2f) -> %s; sinais %s"
              % (cf["pior_d_sd"], cf["tol"], "ok" if cf["todos_ok"] else "FORA",
                 "iguais" if cf["sinais_ok"] else "DIFERENTES"))


def main() -> dict:
    saida = rodar()
    imprimir(saida)
    p1 = salvar(saida)
    p2 = salvar_desenhos(saida)
    print("\n  gravado  %s" % p1)
    print("           %s  (%d desenhos)"
          % (p2, saida["res"][BASE]["_draws"]["alpha"].size and N_DESENHOS))
    return saida


if __name__ == "__main__":
    main()
