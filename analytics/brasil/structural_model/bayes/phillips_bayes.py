# -*- coding: utf-8 -*-
"""A equacao (I), a curva de Phillips desagregada, estimada por MCMC -- as mesmas quatro
equacoes do MQ, uma por subindice do IPCA.

    (IS) servicos          (IA) alimentacao
    (II) bens industriais  (IM) monitorados

As formas estao na docstring de `equations/phillips_sub.py`, e nao sao repetidas aqui.

Existe pela mesma razao que os outros quatro modulos desta pasta: **o simulador precisa de
uma FAIXA, e MQ nao tem uma para dar**. A regra e do usuario, em 2026-09-25: *"no sistema
vamos sempre usar o bayes para todas as equacoes"*.

## A equacao e a MESMA, e isso e verificavel

Este modulo NAO remonta a matriz: ele chama `phillips_sub.matriz()`, a mesma que o MQ
usa, na mesma amostra comum das quatro (`phillips_sub.amostra_comum()`). O que muda e so o
estimador. `conferir()` mede a distancia entre a mediana e o MQ em desvios do posterior.

## Quatro posteriores independentes, e por que parear os desenhos e legitimo

O MQ estima as quatro separadamente, sem correlacao entre os residuos. Aqui tambem: prioris
independentes e verossimilhancas independentes fazem o posterior conjunto ser o PRODUTO dos
quatro, entao parear o desenho `s` de cada um e amostrar dele. E isso que permite medir,
desenho a desenho, o que so existe no sistema: o efeito do hiato no IPCA cheio, o repasse
cambial, a estabilidade das quatro juntas.

## A priori, autoescalada como a da (H) e da (F)

Os regressores vivem em unidades diferentes (desvio de inflacao, p.p. de hiato, % de cambio,
% de commodity, degraus soma-zero). `N(0, sd(y)/sd(x))` por termo, medido na amostra; a
variante `larga` multiplica tudo por 4 e existe para MEDIR se a priori pesa. O desvio do
residuo tem meia-normal de escala `2*sd(y)`, autoescalada tambem -- o residuo de alimentacao
e quatro vezes o de servicos, e uma escala fixa seria apertada numa e frouxa na outra.

## O que so existe no sistema, e com que pesos

Os pesos dos quatro grupos no IPCA sao os do ULTIMO trimestre da amostra -- os que o
simulador usaria partindo dali --, normalizados para somar 1 (somam 0,9999; sem isso o
estado estacionario do cheio erraria na quarta casa). Todas as leituras sao **com a
expectativa parada**: em equilibrio geral ela reage a inflacao, e isso e o simulador.

- `hiato_4t`:   1 p.p. de hiato mantido por quatro trimestres, somado ao IPCA de 12 meses.
- `hiato_lp`:   o mesmo hiato para sempre, em inflacao trimestral de estado estacionario.
- `repasse_4t`: de uma depreciacao de 1%, uma vez so, quanto chegou ao nivel do IPCA em um
                ano; `repasse_8t` em dois; `repasse_lp` no longo prazo, fechado.

Os de longo prazo carregam a indexacao dos monitorados ao cheio, que devolve parte do choque
ao proprio cheio: o multiplicador e `(1-im1) / (1-im1-im2*w_M)`. A forma fechada e conferida
contra a simulacao de 400 trimestres, desenho a desenho, nos desenhos rapidos.

E um numero que responde a pergunta que abriu esta estimacao: **o laco alimentacao <->
cambio dentro do trimestre**. A (IA) le o cambio do mesmo trimestre e a (F) le o diferencial
de inflacao do mesmo trimestre, com peso imposto em 1. O ganho do laco e `w_A * ia3`; resolver
os dois juntos em vez de em sequencia multiplica o efeito por `1/(1-ganho)`.

A estabilidade e medida no SISTEMA, nao por equacao: a (IM) le o IPCA cheio defasado, que
contem as outras tres, entao o raio espectral e o da matriz companheira das quatro juntas.

Uso:
    uv run python -m analytics.brasil.structural_model.bayes.phillips_bayes
"""
from __future__ import annotations

import json
import pathlib
import warnings

import numpy as np
import pandas as pd

from analytics.brasil.structural_model import panel
from analytics.brasil.structural_model.equations import phillips_sub as ph

DATA = pathlib.Path(__file__).resolve().parent / "data"

DRAWS, TUNE, CHAINS, SEED = 4000, 2000, 4, 20260928
TARGET_ACCEPT = 0.90
HDI = 0.90
N_DESENHOS = 1000
SIGMA_ESCALA = 2.0      # meia-normal de escala 2*sd(y), por equacao

VARIANTES = {
    "dado": dict(escala=1.0, ini=None,
                 desc="Priori autoescalada sd(y)/sd(x) por termo, amostra do MQ"),
    "larga": dict(escala=4.0, ini=None,
                  desc="A mesma priori com o desvio multiplicado por 4"),
    "desde2006": dict(escala=1.0, ini="2006Q2",
                      desc="A base, com a amostra a partir de 2006T2 (o inicio da (H) e da (F))"),
}
BASE = "dado"

# Ate onde uma simulacao de 400 trimestres basta para conferir a forma fechada: 0,95^400
# ~ 1e-9. Acima disso a forma continua valendo pela algebra -- a mesma licao do
# `repouso_draws()` da (H), que reprovava desenho LENTO e nao errado.
RAIO_RAPIDO = 0.95


def _par(chave: str, col: str) -> str | None:
    """O parametro de uma equacao pela COLUNA que ele multiplica -- o nome muda de
    equacao para equacao (is2, ia4, ii5 sao todos o hiato)."""
    for par, c, _ in ph.EQUACOES[chave]["regs"]:
        if c == col:
            return par
    return None


# ─────────────────────────────────────────────────────────────────────────────
# dados
# ─────────────────────────────────────────────────────────────────────────────
def dados(df: pd.DataFrame | None = None, ini: str | None = None) -> dict:
    """As quatro matrizes do MQ, pela mesma `phillips_sub.matriz()`, na amostra comum."""
    if df is None:
        df = panel.carregar()
    d = ph.montar(df)
    idx = ph.amostra_comum(d)
    if ini:
        idx = idx[idx >= pd.Period(ini, freq="Q")]
    eqs = {}
    for k in ph.ORDEM:
        m = ph.matriz(d, k, idx=idx)
        X = {p: m["X"][:, j] for j, p in enumerate(m["nomes"])}
        eqs[k] = {
            "y": m["y"], "X": X, "pars": list(m["nomes"]),
            "inercia": ph.EQUACOES[k]["inercia"],
            "restritos": [p for p, _c, _r in m["restritos"]],
            "regs": [p for p, _c, _r in m["regs"]],
            "sd": {p: float(np.std(X[p], ddof=1)) for p in m["nomes"]},
            "sd_y": float(np.std(m["y"], ddof=1)),
            "obs": d.loc[m["am"].index, m["dep"]],
            "n": len(m["y"]),
        }
    fim = idx[-1]
    w = {k: float(d.loc[fim, panel.PESO_COL[k.lower()]]) for k in ph.ORDEM}
    tot = sum(w.values())
    return {"d": d, "idx": idx, "eqs": eqs, "n": len(idx), "ini": idx[0], "fim": fim,
            "w": {k: v / tot for k, v in w.items()}, "w_soma_bruta": tot,
            "w_t": {k: d.loc[idx, panel.PESO_COL[k.lower()]] for k in ph.ORDEM},
            "pi_q": d.loc[idx, "pi_q"]}


def prioris(e: dict, escala: float = 1.0) -> dict:
    out = {}
    for p in e["pars"]:
        sdx = e["sd"][p]
        out[p] = ("N", 0.0, float(escala * e["sd_y"] / sdx) if sdx else 5.0)
    out["sigma"] = ("HN", float(SIGMA_ESCALA * e["sd_y"]))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# o modelo, um por equacao
# ─────────────────────────────────────────────────────────────────────────────
def construir_modelo(e: dict, escala: float):
    import pymc as pm

    pri = prioris(e, escala)
    with pm.Model() as m:
        b = {p: pm.Normal(p, pri[p][1], pri[p][2]) for p in e["pars"]}
        peso = 1.0 - b[e["inercia"]] - sum(b[p] for p in e["restritos"])
        pm.Deterministic("peso_e", peso)
        for p in e["regs"]:
            # a razao propagada desenho a desenho: a razao das medianas nao e a mediana
            # da razao
            pm.Deterministic("lp_" + p, b[p] / peso)
        if "s1" in b:
            pm.Deterministic("s4", -(b["s1"] + b["s2"] + b["s3"]))
        mu = sum(b[p] * e["X"][p] for p in e["pars"])
        sigma = pm.HalfNormal("sigma", pri["sigma"][1])
        pm.Normal("y_obs", mu=mu, sigma=sigma, observed=e["y"])
    return m


def amostrar(e: dict, escala: float, seed: int, draws: int = DRAWS, tune: int = TUNE,
             chains: int = CHAINS):
    import pymc as pm

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with construir_modelo(e, escala):
            return pm.sample(draws=draws, tune=tune, chains=chains, cores=1,
                             target_accept=TARGET_ACCEPT, random_seed=seed,
                             progressbar=False)


# ─────────────────────────────────────────────────────────────────────────────
# leitura do posterior, por equacao
# ─────────────────────────────────────────────────────────────────────────────
def _flat(idata, nome: str) -> np.ndarray:
    return np.asarray(idata.posterior[nome]).reshape(-1)


def _stats(x: np.ndarray) -> dict:
    import arviz as az
    x = np.asarray(x, float)
    fin = x[np.isfinite(x)]
    lo, hi = az.hdi(fin, hdi_prob=HDI)
    return {"media": float(fin.mean()), "sd": float(fin.std(ddof=1)),
            "mediana": float(np.median(fin)), "hdi_lo": float(lo), "hdi_hi": float(hi),
            "p_pos": float(np.mean(fin > 0))}


def resumo_eq(idata, e: dict, escala: float) -> dict:
    import arviz as az

    nomes = e["pars"] + ["sigma"]
    deriv = (["peso_e"] + ["lp_" + p for p in e["regs"]]
             + (["s4"] if "s1" in e["pars"] else []))
    post = {n: _flat(idata, n) for n in nomes + deriv}
    sm = az.summary(idata, var_names=nomes, hdi_prob=HDI)
    pri = prioris(e, escala)
    par = {}
    for n in nomes:
        s = _stats(post[n])
        s["rhat"] = float(sm.loc[n, "r_hat"])
        s["ess"] = float(sm.loc[n, "ess_bulk"])
        s["priori"] = list(pri[n])
        if pri[n][0] == "N":
            s["encolheu"] = float(s["sd"] / pri[n][2])
        par[n] = s
    for n in deriv:
        par[n] = _stats(post[n])

    # inercia, restritos e expectativa sao os pesos de uma media ponderada: todos >= 0
    # e o que torna a leitura "media de passado e expectativa" literal. Nada na priori
    # obriga, entao e medido.
    pesos = [post[e["inercia"]]] + [post[p] for p in e["restritos"]] + [post["peso_e"]]
    simplex = float(np.mean(np.all(np.vstack(pesos) >= 0, axis=0)))

    # ajuste na MEDIA do posterior; o residuo do desvio e o residuo do nivel
    resid = e["y"] - sum(par[p]["media"] * e["X"][p] for p in e["pars"])
    obs = e["obs"].to_numpy(float)
    sst = float(((obs - obs.mean()) ** 2).sum())
    return {"par": par, "nomes": nomes, "derivados": deriv,
            "rmse": float(np.sqrt((resid ** 2).mean())),
            "r2": float(1.0 - (resid ** 2).sum() / sst),
            "acf1": float(pd.Series(resid).autocorr(1)),
            "simplex": simplex,
            "rhat_max": float(max(par[n]["rhat"] for n in nomes)),
            "ess_min": float(min(par[n]["ess"] for n in nomes)),
            "div": int(np.asarray(idata.sample_stats["diverging"]).sum()),
            "_resid": pd.Series(resid, index=e["obs"].index),
            "_draws": post}


def conferir(r: dict, mq: dict, tol: float = 0.25) -> dict:
    """Mediana contra MQ, termo a termo, em DESVIOS DO POSTERIOR."""
    out, pior = {}, 0.0
    for p, v in mq["coef"].items():
        s = r["par"][p]
        dz = abs(s["mediana"] - float(v)) / s["sd"] if s["sd"] else float("nan")
        out[p] = {"bayes": s["mediana"], "mq": float(v), "t_mq": float(mq["t"][p]),
                  "d_sd": float(dz), "ok": bool(dz <= tol)}
        pior = max(pior, dz)
    return {"itens": out, "pior_d_sd": float(pior),
            "todos_ok": all(o["ok"] for o in out.values()), "tol": tol,
            "r2_mq": float(mq["r2"]), "rmse_mq": float(mq["rmse"]),
            "lb_p4_mq": float(mq["lb_p4"])}


# ─────────────────────────────────────────────────────────────────────────────
# o sistema, desenho a desenho
# ─────────────────────────────────────────────────────────────────────────────
# Estado s(t), em desvio de E/4 com a expectativa parada:
#   0..3  servicos       t, t-1, t-2, t-3   (a MM4 le quatro defasagens)
#   4     alimentacao    t
#   5..8  industriais    t, t-1, t-2, t-3
#   9     monitorados    t
_S, _A, _N, _M = 0, 4, 5, 9


def companheira(D: dict, w: dict) -> np.ndarray:
    """A matriz companheira das quatro juntas, uma por desenho: (n, 10, 10)."""
    n = D["IS"]["is1"].size
    M = np.zeros((n, 10, 10))
    a, b = D["IS"]["is1"], D["IS"]["is1b"] / 4.0
    M[:, 0, 0] = a + b
    M[:, 0, 1:4] = b[:, None]
    M[:, 1, 0] = M[:, 2, 1] = M[:, 3, 2] = 1.0
    M[:, 4, 4] = D["IA"]["ia1"]
    a, b = D["II"]["ii1"], D["II"]["ii1b"] / 4.0
    M[:, 5, 5] = a + b
    M[:, 5, 6:9] = b[:, None]
    M[:, 6, 5] = M[:, 7, 6] = M[:, 8, 7] = 1.0
    im1, im2 = D["IM"]["im1"], D["IM"]["im2"]
    M[:, 9, _S] = im2 * w["IS"]
    M[:, 9, _A] = im2 * w["IA"]
    M[:, 9, _N] = im2 * w["II"]
    M[:, 9, _M] = im1 + im2 * w["IM"]
    return M


def _cheio(s: np.ndarray, w: dict) -> np.ndarray:
    return w["IS"] * s[:, _S] + w["IA"] * s[:, _A] + w["II"] * s[:, _N] + w["IM"] * s[:, _M]


def sistema(D: dict, w: dict) -> dict:
    """As leituras que so existem com as quatro juntas, desenho a desenho."""
    ph_h = {k: _par(k, "hiato") for k in ("IS", "IA", "II")}
    ia3, ii4 = D["IA"][_par("IA", "de")], D["II"][_par("II", "de_l1")]
    pe = {k: D[k]["peso_e"] for k in ph.ORDEM}
    M = companheira(D, w)
    n = M.shape[0]

    raio = np.max(np.abs(np.linalg.eigvals(M)), axis=1)
    im1, im2 = D["IM"]["im1"], D["IM"]["im2"]
    mult = (1.0 - im1) / (1.0 - im1 - im2 * w["IM"])

    hiato_imp = sum(w[k] * D[k][ph_h[k]] for k in ph_h)
    hiato_lp = mult * sum(w[k] * D[k][ph_h[k]] / pe[k] for k in ph_h)
    repasse_lp = mult * (w["IA"] * ia3 / pe["IA"] + w["II"] * ii4 / pe["II"])
    laco = w["IA"] * ia3

    # Simulacao: (a) depreciacao de 1% uma vez so, no trimestre 0; (b) hiato de 1 p.p.
    # mantido sempre. Acumula o cheio.
    choque_h = np.zeros((n, 10))
    for k, pos in (("IS", _S), ("IA", _A), ("II", _N)):
        choque_h[:, pos] = D[k][ph_h[k]]
    s_c, s_h = np.zeros((n, 10)), np.zeros((n, 10))
    acum_c, acum_h = [], []
    ac_c = ac_h = np.zeros(n)
    # um desenho explosivo estoura antes dos 400 trimestres; ele so e lido nos quatro e
    # oito primeiros, e o aviso de overflow nao diz nada
    velho = np.seterr(over="ignore", invalid="ignore")
    for t in range(400):
        u = np.zeros((n, 10))
        if t == 0:
            u[:, _A] = ia3
        if t == 1:
            u[:, _N] = ii4
        s_c = np.einsum("nij,nj->ni", M, s_c) + u
        s_h = np.einsum("nij,nj->ni", M, s_h) + choque_h
        ac_c = ac_c + _cheio(s_c, w)
        acum_c.append(ac_c)
        if t < 4:
            ac_h = ac_h + _cheio(s_h, w)
            acum_h.append(ac_h)
    hiato_ss_sim = _cheio(s_h, w)
    np.seterr(**velho)

    rap = raio <= RAIO_RAPIDO
    conf = {
        "n_conferidos": int(rap.sum()),
        "repasse_pior": float(np.max(np.abs(acum_c[-1][rap] - repasse_lp[rap]))),
        "hiato_pior": float(np.max(np.abs(hiato_ss_sim[rap] - hiato_lp[rap]))),
    }
    conf["bate"] = bool(conf["repasse_pior"] <= 1e-6 and conf["hiato_pior"] <= 1e-6)

    est = raio < 1.0
    return {
        "raio": raio, "frac_explosivos": float(np.mean(~est)),
        "frac_lentos": float(np.mean((raio > RAIO_RAPIDO) & est)),
        "mult_im": mult,
        "hiato_impacto": hiato_imp, "hiato_4t": acum_h[3], "hiato_lp": hiato_lp,
        "repasse_impacto": laco, "repasse_4t": acum_c[3], "repasse_8t": acum_c[7],
        "repasse_lp": repasse_lp,
        "laco": laco, "laco_mult": 1.0 / (1.0 - laco),
        "forma_fechada": conf, "_estavel": est,
    }


SIS_ESTAT = ["raio", "mult_im", "hiato_impacto", "hiato_4t", "hiato_lp",
             "repasse_impacto", "repasse_4t", "repasse_8t", "repasse_lp",
             "laco", "laco_mult"]
# as de longo prazo so fazem sentido nos desenhos estaveis
_SO_ESTAVEL = {"hiato_lp", "repasse_lp", "mult_im"}


# ─────────────────────────────────────────────────────────────────────────────
# rodar e gravar
# ─────────────────────────────────────────────────────────────────────────────
def rodar(quais: list[str] | None = None, df: pd.DataFrame | None = None,
          draws: int = DRAWS, tune: int = TUNE, chains: int = CHAINS) -> dict:
    quais = list(VARIANTES) if quais is None else quais
    out = {}
    for iv, nome in enumerate(quais):
        v = VARIANTES[nome]
        dd = dados(df, v["ini"])
        res, D = {}, {}
        for ie, k in enumerate(ph.ORDEM):
            e = dd["eqs"][k]
            idata = amostrar(e, v["escala"], SEED + 10 * iv + ie, draws, tune, chains)
            r = resumo_eq(idata, e, v["escala"])
            r["confere"] = conferir(r, ph.estimar_uma(dd["d"], k, idx=dd["idx"]))
            res[k] = r
            D[k] = r["_draws"]
        sis = sistema(D, dd["w"])
        # o IPCA cheio reconstruido pelos quatro ajustes, com os pesos de cada trimestre
        fit = sum(dd["w_t"][k] * (dd["eqs"][k]["obs"] - res[k]["_resid"]) for k in ph.ORDEM)
        e = (fit - dd["pi_q"]).dropna().to_numpy(float)
        mq = ph.estimar(dd["d"]) if not v["ini"] else None
        out[nome] = {"dd": dd, "res": res, "sis": sis,
                     "cheio_rmse": float(np.sqrt((e ** 2).mean())),
                     "cheio_rmse_mq": float(mq["cheio"]["rmse"]) if mq else None}
    return out


def _sis_resumo(sis: dict) -> dict:
    est = sis["_estavel"]
    o = {}
    for k in SIS_ESTAT:
        x = sis[k][est] if k in _SO_ESTAVEL else sis[k]
        o[k] = _stats(x)
    o.update({k: sis[k] for k in ("frac_explosivos", "frac_lentos", "forma_fechada")})
    return o


def salvar(saida: dict, destino: pathlib.Path | None = None) -> pathlib.Path:
    destino = destino or (DATA / "phillips_bayes.json")
    destino.parent.mkdir(parents=True, exist_ok=True)
    limpo = {}
    for nome, s in saida.items():
        dd = s["dd"]
        limpo[nome] = {
            "desc": VARIANTES[nome]["desc"], "n": dd["n"],
            "ini": str(dd["ini"]), "fim": str(dd["fim"]), "pesos": dd["w"],
            "equacoes": {k: {kk: vv for kk, vv in r.items() if not kk.startswith("_")}
                         for k, r in s["res"].items()},
            "sistema": _sis_resumo(s["sis"]),
            "cheio_rmse": s["cheio_rmse"], "cheio_rmse_mq": s["cheio_rmse_mq"],
        }
    destino.write_text(json.dumps(limpo, indent=2, ensure_ascii=False, default=float),
                       encoding="utf-8")
    return destino


def salvar_desenhos(saida: dict, nome: str = BASE, n: int = N_DESENHOS,
                    destino: pathlib.Path | None = None) -> pathlib.Path:
    """1.000 desenhos afinados da variante base, PAREADOS entre as quatro equacoes -- o
    indice `s` e o mesmo nas quatro, que e o que o simulador vai ler."""
    destino = destino or (DATA / "phillips_draws.json")
    s = saida[nome]
    dd = s["dd"]
    tot = int(s["res"]["IS"]["_draws"]["sigma"].size)
    passo = max(1, tot // n)
    sel = np.arange(0, tot, passo)[:n]
    eqs = {}
    for k, r in s["res"].items():
        pars = r["nomes"]
        eqs[k] = {
            "pars": pars, "derivados": r["derivados"],
            "draws": {p: [round(float(v), 6) for v in r["_draws"][p][sel]]
                      for p in pars + r["derivados"]},
            "mediana": {p: r["par"][p]["mediana"] for p in pars + r["derivados"]},
            "hdi": {p: [r["par"][p]["hdi_lo"], r["par"][p]["hdi_hi"]]
                    for p in pars + r["derivados"]},
        }
    out = {"variante": nome, "desc": VARIANTES[nome]["desc"],
           "n_total": tot, "n_gravado": int(sel.size), "passo": int(passo),
           "gerado_de": {"n": dd["n"], "ini": str(dd["ini"]), "fim": str(dd["fim"])},
           "pesos": dd["w"], "hdi_prob": HDI, "equacoes": eqs,
           "sistema": _sis_resumo(s["sis"])}
    destino.write_text(json.dumps(out, ensure_ascii=False, default=float), encoding="utf-8")
    return destino


# ─────────────────────────────────────────────────────────────────────────────
# impressao
# ─────────────────────────────────────────────────────────────────────────────
def _rot(k: str, p: str) -> str:
    if p == "peso_e":
        return "Peso da expectativa"
    if p == "s4":
        return "4º trimestre (derivado)"
    if p.startswith("lp_"):
        return "  longo prazo de " + p[3:]
    if p == "sigma":
        return "Desvio do resíduo"
    return ph._rotulo(k, p)


def imprimir(saida: dict) -> None:
    for nome, s in saida.items():
        dd = s["dd"]
        print("=" * 100)
        print("[%s] %s" % (nome, VARIANTES[nome]["desc"]))
        print("  amostra %s a %s (%d trimestres); pesos no fim: %s"
              % (dd["ini"], dd["fim"], dd["n"],
                 "  ".join("%s %.3f" % (k, v) for k, v in dd["w"].items())))
        for k, r in s["res"].items():
            cf = r["confere"]
            print("-" * 100)
            print("(%s) %s" % (k, ph.EQUACOES[k]["nome"]))
            print("  %-46s %8s %20s %6s %7s %8s %6s" % ("", "mediana", "HDI 90%", "P(>0)",
                                                      "encolh", "MQ", "t MQ"))
            for p in r["nomes"] + r["derivados"]:
                st = r["par"][p]
                mq = cf["itens"].get(p)
                print("  %-46s %+8.4f  [%+7.4f, %+7.4f] %6.3f %7s %8s %6s"
                      % (_rot(k, p)[:46], st["mediana"], st["hdi_lo"], st["hdi_hi"],
                         st["p_pos"],
                         "%.2f" % st["encolheu"] if "encolheu" in st else "",
                         "%+.4f" % mq["mq"] if mq else "",
                         "%.2f" % mq["t_mq"] if mq else ""))
            print("  R2 %.4f (MQ %.4f)  RMSE %.4f (MQ %.4f)  acf1 %+.3f  LB(4) MQ p %.3f"
                  % (r["r2"], cf["r2_mq"], r["rmse"], cf["rmse_mq"], r["acf1"],
                     cf["lb_p4_mq"]))
            print("  R-hat max %.4f  ESS min %d  divergencias %d  pesos no simplex %.1f%%"
                  "  |  contra o MQ: pior %.3f desvio -> %s"
                  % (r["rhat_max"], r["ess_min"], r["div"], 100 * r["simplex"],
                     cf["pior_d_sd"], "ok" if cf["todos_ok"] else "FORA"))
        sis = _sis_resumo(s["sis"])
        print("-" * 100)
        print("SISTEMA (expectativa parada, pesos do fim da amostra)")
        rot = {"raio": "raio espectral das quatro juntas",
               "mult_im": "multiplicador da indexacao dos monitorados",
               "hiato_impacto": "hiato 1 p.p. -> IPCA do mesmo trimestre, p.p.",
               "hiato_4t": "hiato 1 p.p. por 4 tri -> IPCA 12m, p.p.",
               "hiato_lp": "hiato 1 p.p. sempre -> IPCA tri estacionario, p.p.",
               "repasse_impacto": "deprec. 1% -> IPCA no mesmo trimestre, %",
               "repasse_4t": "deprec. 1% -> nivel do IPCA em 4 tri, %",
               "repasse_8t": "deprec. 1% -> nivel do IPCA em 8 tri, %",
               "repasse_lp": "deprec. 1% -> nivel do IPCA no longo prazo, %",
               "laco": "ganho do laco alimentacao <-> cambio",
               "laco_mult": "multiplicador de resolver os dois juntos"}
        for k in SIS_ESTAT:
            st = sis[k]
            print("  %-52s %+8.4f  [%+7.4f, %+7.4f]  P(>0) %.3f"
                  % (rot[k], st["mediana"], st["hdi_lo"], st["hdi_hi"], st["p_pos"]))
        ff = sis["forma_fechada"]
        print("  explosivos %.2f%%  lentos (raio > %.2f) %.2f%%  |  forma fechada contra 400 "
              "trimestres simulados, %d desenhos: repasse %.1e, hiato %.1e -> %s"
              % (100 * sis["frac_explosivos"], RAIO_RAPIDO, 100 * sis["frac_lentos"],
                 ff["n_conferidos"], ff["repasse_pior"], ff["hiato_pior"],
                 "ok" if ff["bate"] else "NAO BATE"))
        print("  IPCA cheio reconstruido: RMSE %.4f%s"
              % (s["cheio_rmse"], " (MQ %.4f)" % s["cheio_rmse_mq"]
                 if s["cheio_rmse_mq"] is not None else ""))


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
