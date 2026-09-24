# -*- coding: utf-8 -*-
"""A equacao (F): o cambio, em frequencia trimestral.

    (F) de(t) = dppp(t) + alpha + phi*de(t-1) + sum_c beta_c*z(dc(t)) + eps

    de     100*dlog(PTAX) no trimestre, pelo FECHAMENTO
    dppp   100*dlog(IPCA/CPI) -- o diferencial de inflacao BR-US, com
           coeficiente IMPOSTO em 1 (offset, nao regressor)
    dc     variacao trimestral de cada canal: fiscal (CDS 5a, bps), dxy_em
           (dolar contra emergentes), carry_vol (carry sobre volatilidade),
           sp500 e icbr_usd (indices -> log-retorno)
    phi    AR(1) na propria variacao do cambio, em unidade nativa

Estimada por Ridge com lambda escolhido por validacao cruzada walk-forward,
exatamente como o modelo MENSAL que serve o FX Report. Este modulo NAO reescreve
aquele: importa `load_data`, `_standardize_ext`, `walk_forward_lambda` e
`fit_whole_sample` de la e monta a amostra trimestral por cima.

## Estado, 81 trimestres 2006T2-2026T2 (corte fixado em 2026T2)

    termo                        beta(sd)  t(HAC)  acum.pp   nativo
    risco fiscal (CDS 5a)         +27,03    9,82     -2,1   +0,0906 por bp
    dolar contra emergentes        +2,354   2,94    +20,2   +0,693  por ponto
    carry sobre volatilidade       -0,577  -1,35     -0,5   -2,275  por unidade
    bolsa americana                +1,898   3,34    +39,8   +0,227  por 1%
    commodities em dolar           -2,054  -3,44    -18,8   -0,275  por 1%
    cambio do trimestre anterior   -0,087  -1,32     -7,0
    constante (alpha)              -0,035  -0,08     -2,9   p.p./trimestre
    diferencial de inflacao      imposto=1           +58,0

R2 0,8115 - RMSE 3,59 p.p./tri - lambda 0,0100, o PISO da grade - residuo limpo
(autocorrelacao -0,02; Ljung-Box Q(4) p 0,822, Q(8) p 0,755). O cambio andou
+86,8 p.p. de log na amostra e a soma das contribuicoes devolve +86,8 exatamente.

Contra o mensal (n 245, 2006-02..2026-06, R2 0,6532), em unidade NATIVA -- que e
o numero comparavel entre frequencias, porque o sd se cancela: os SEIS
coeficientes tem o mesmo sinal nas duas, e o alpha e indistinguivel de zero nas
duas, que e o que o offset de PPP existe para produzir. O R2 sobe de 0,65 para
0,81 ao passar para trimestral -- parte do que e ruido mensal se cancela dentro
do trimestre.

## A ressalva que a decomposicao NAO diz sozinha

`sp500` e o unico canal cujo coeficiente tem sinal OPOSTO ao da sua correlacao
bruta com a dependente: corr -0,435, beta +1,898 (t 3,34). Nao e erro nem
artefato da frequencia -- o mensal publicado tem o mesmo padrao (-0,428 e +0,764)
-- e o mecanismo esta medido: `sp500` correlaciona -0,574 com o CDS e -0,606 com
o dolar EM, entao

    sp500 sozinho                 -3,542  (t -4,25)
    + dolar EM                    +0,290
    + fiscal                      +0,529
    + fiscal + dolar EM           +1,364
    o modelo inteiro              +1,907

Sozinha, bolsa subindo vem com real mais forte, porque bolsa subindo E risk-on, e
risk-on comprime o CDS e enfraquece o dolar contra emergentes. Segurados esses
dois, o que sobra move o real na direcao oposta. **A contribuicao acumulada de
+39,8 p.p. e um objeto CONDICIONAL**, e ela e 46% da desvalorizacao do periodo:
quem ler a barra como causa independente le errado. Pendencia F1.

## O que fica de fora, e esta declarado

Reselecao dos canais (o corte 8->5 foi medido em mensal), janela movel (81
trimestres nao comportam), e vol implicita de opcoes, que nao tem tabela no
banco. Tudo em `pendencias_fx_eq.md`, com o que cada um custa medido.

**Uma inconsistencia entre equacoes, nao um defeito desta:** aqui o cambio e
medido pelo FECHAMENTO do trimestre, e a coluna `de` do painel -- o `F(t)` que a
curva de Phillips usa -- e a variacao da MEDIA. Desvios de 8,32 contra 6,76. Cada
equacao usa a convencao que o seu desenho pede enquanto sao estimadas sozinhas; o
SIMULADOR que nao poderia ligar as duas sem declarar -- e ele saiu de escopo em
2026-09-22, entao F2 e hoje inconsistencia declarada e nao decisao pendente.

Uso:
    uv run python -m analytics.brasil.structural_model.equations.fx
"""
from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_ljungbox

from analytics.brasil.exchange_rate.models import ppp_equilibrium as _pe
from analytics.brasil.exchange_rate.models import ridge_deviation_model as _rd

warnings.filterwarnings("ignore")

# ── as decisoes, nomeadas ────────────────────────────────────────────────────

# Os 5 canais que o modelo mensal ship a. O corte 8->5 foi medido em mensal e nao
# foi refeito aqui -- e pendencia declarada, nao escolha desta amostra.
CANAIS = ["fiscal", "dxy_em", "carry_vol", "sp500", "icbr_usd"]

# Canais que sao INDICE de preco (milhares/centenas): a variacao e log-retorno.
# Todo o resto ja e taxa, spread ou diferencial, estacionario em nivel.
LOG_RET = {"sp500", "icbr_usd"}

# A fonte da volatilidade do `carry_vol`. `realizada_lag` termina no fechamento de
# t-1, o que torna o denominador PREDETERMINADO -- ver a secao de simultaneidade
# na docstring de `vol_trimestral`. `implicita` ainda nao tem tabela no banco.
VOL_SOURCE = "realizada_lag"
VOL_LAG_Q = 1

# Convencao de trimestralizacao dos NIVEIS, antes de diferenciar.
COMO = "last"

MIN_TRAIN = 16          # trimestres antes do primeiro fold da validacao cruzada
HAC_LAGS = 4
REF_INI = "2000-01-01"  # janela de referencia do desvio-padrao, como no mensal
OFFSET = "d_ppp"        # a coluna cujo coeficiente e imposto em 1

_DATA = Path(__file__).resolve().parents[1] / "data"
_CUTOFF = _DATA / "fx_fit_cutoff.json"

ROT = {
    "d_ppp": "Diferencial de inflação BR-US (imposto em 1)",
    "d_fiscal": "Risco fiscal (CDS de 5 anos)",
    "d_dxy_em": "Dólar contra emergentes",
    "d_carry_vol": "Carry sobre volatilidade",
    "d_sp500": "Bolsa americana",
    "d_icbr_usd": "Commodities em dólar",
    "de_l1": "Variação do câmbio do trimestre anterior",
}

UNID = {
    "d_fiscal": "bps",
    "d_dxy_em": "pontos do índice",
    "d_carry_vol": "p.p. por unidade de vol",
    "d_sp500": "% (log-retorno)",
    "d_icbr_usd": "% (log-retorno)",
    "de_l1": "p.p.",
    "d_ppp": "p.p.",
}


# ── os insumos trimestrais ───────────────────────────────────────────────────
def _mensal() -> pd.DataFrame:
    """O frame mensal do FX Report, cru. Cacheado no modulo -- sao ~15 consultas."""
    if not hasattr(_mensal, "_c"):
        _mensal._c = _pe.load_data()
    return _mensal._c


def _trimestres_cheios(idx: pd.DatetimeIndex) -> pd.PeriodIndex:
    """Os trimestres com os TRES meses presentes no indice mensal.

    Sem isso o ultimo trimestre entra com o que ja chegou dele: em 2026-08 o
    `resample('QS').last()` devolveria agosto como se fosse o fechamento de
    2026T3. E a mesma coluna `completo` que o painel desta pasta carrega.
    """
    p = pd.Series(1, index=idx).groupby(idx.to_period("Q")).sum()
    return pd.PeriodIndex(p[p == 3].index)


def _para_q(s: pd.Series, como: str = COMO) -> pd.Series:
    """Serie mensal -> trimestral, indexada por PeriodIndex."""
    g = s.dropna().groupby(s.dropna().index.to_period("Q"))
    return (g.last() if como == "last" else g.mean()).sort_index()


def vol_trimestral(lag: int = VOL_LAG_Q) -> pd.Series:
    """Volatilidade realizada do real, trimestral, DEFASADA `lag` trimestres.

    ## Por que defasar, e o que isso corrige

    `_annualized_vol_6m` e uma janela movel de 126 pregoes terminando em t. Em
    frequencia mensal ela ja cobre ~2 trimestres; em trimestral, o trimestre que
    se quer EXPLICAR esta inteiro dentro da janela do denominador. A variacao do
    cambio entra dos dois lados da regressao, e o coeficiente do `carry_vol`
    passa a medir parte da propria dependente.

    Defasar um trimestre elimina isso por construcao: a vol usada em t termina no
    ultimo pregao de t-1, entao e conhecida no inicio de t -- predeterminada, no
    sentido exato do termo. E a correcao padrao e nao custa amostra (a serie
    comeca em 1994, muito antes do canal que limita a amostra).

    **O que ela NAO resolve**, e fica declarado: vol realizada defasada continua
    sendo funcao da historia da propria variavel dependente. Para ESTIMAR isso
    basta, porque predeterminacao e o que a consistencia do MQ exige. Para
    SIMULAR um cenario fechado ela teria de ser atualizada a partir do caminho
    simulado -- e o simulador saiu de escopo em 2026-09-22, entao essa metade
    deixou de ter consumidor. A metade que valia para a ESTIMACAO ja esta
    resolvida pela defasagem.

    **Vol implicita de opcoes resolveria as duas metades** -- e prospectiva,
    observavel em t, e nao e funcao de realizacao passada. Nao ha tabela dela no
    banco (varredura completa em 2026-09); `VOL_SOURCE='implicita'` existe para a
    troca ser de serie e nao de equacao, e levanta ate a tabela existir.
    """
    if VOL_SOURCE == "implicita":
        raise NotImplementedError(
            "nao ha tabela de volatilidade implicita no banco. O destino recomendado e "
            "`macro_brasil.cmb_vol_implicita`, pelo caminho do conector Bloomberg que ja "
            "existe em domain/db/brasil/bloomberg/cmb_risco_pais.py"
        )
    if VOL_SOURCE != "realizada_lag":
        raise ValueError("VOL_SOURCE: 'realizada_lag' ou 'implicita', nao %r" % VOL_SOURCE)
    if not hasattr(vol_trimestral, "_c"):
        vol_trimestral._c = _para_q(_pe._annualized_vol_6m(_pe._load_daily_ptax()),
                                    como="last")
    return vol_trimestral._c.shift(lag)


def niveis(lag_vol: int = VOL_LAG_Q) -> pd.DataFrame:
    """Os niveis trimestrais de que a equacao precisa, no fechamento do trimestre.

    `carry_vol` e RECONSTRUIDO aqui em vez de trimestralizado do mensal, porque o
    mensal o constroi com vol contemporanea -- ver `vol_trimestral`.
    """
    m = _mensal()
    cheios = _trimestres_cheios(m.index)

    cols = ["ptax", "ipca_index", "cpi_index", "fiscal", "dxy_em", "sp500", "icbr_usd"]
    out = pd.DataFrame({c: _para_q(m[c]) for c in cols})
    out["carry_vol"] = _para_q(m["carry"]) / vol_trimestral(lag_vol)
    out["carry_vol_contemp"] = _para_q(m["carry_vol"])
    return out.reindex(cheios).sort_index()


# ── a matriz de regressao ────────────────────────────────────────────────────
def montar(canais: list[str] | None = None, ppp: bool = True, ar1: bool = True,
           lag_vol: int = VOL_LAG_Q, vol_contemp: bool = False,
           como: str = COMO) -> tuple[pd.DataFrame, dict, list[str]]:
    """Niveis trimestrais -> variacoes -> escala. Devolve (z, stats, regressores).

    A escala e `z = x / sd` e **nao centra**. A media de uma coluna em DIFERENCA e
    uma deriva, e subtrai-la injeta sinal constante em todo trimestre, inclusive
    naqueles em que o canal nao se mexeu. O ajuste nao muda (o intercepto do Ridge
    nao e penalizado), a ATRIBUICAO muda muito -- ver `_standardize_ext` no modulo
    mensal, onde isso esta medido.

    O `sd` sai da janela de referencia (%s em diante) e nao da amostra do ajuste,
    para um canal de historia longa nao ser reescalado por um canal que comeca
    tarde.
    """ % REF_INI
    canais = CANAIS if canais is None else canais
    n = niveis(lag_vol)
    if como != "last":
        m = _mensal()
        cheios = _trimestres_cheios(m.index)
        n2 = pd.DataFrame({c: _para_q(m[c], como=como)
                           for c in ("ptax", "ipca_index", "cpi_index", "fiscal",
                                     "dxy_em", "sp500", "icbr_usd")})
        n2["carry_vol"] = _para_q(m["carry"], como=como) / vol_trimestral(lag_vol)
        n2["carry_vol_contemp"] = _para_q(m["carry_vol"], como=como)
        n = n2.reindex(cheios).sort_index()

    out = pd.DataFrame(index=n.index)
    out["de"] = 100 * np.log(n["ptax"]).diff()
    out["d_ppp"] = 100 * (np.log(n["ipca_index"]) - np.log(n["cpi_index"])).diff()
    for c in canais:
        fonte = "carry_vol_contemp" if (c == "carry_vol" and vol_contemp) else c
        out["d_%s" % c] = (100 * np.log(n[fonte]).diff() if c in LOG_RET
                           else n[fonte].diff())
    out["de_l1"] = out["de"].shift(1)

    am = out.dropna()
    escalar = ["d_%s" % c for c in canais]
    ref = out[out.index >= pd.Period(REF_INI, "Q")]
    z, stats = _rd._standardize_ext(am, ref, escalar)

    # A AR(1) e o offset de PPP ficam em unidade NATIVA de proposito: o AR para o
    # coeficiente ser lido como persistencia, e o PPP porque o que ele existe para
    # carregar e a media -- que e exatamente o que a escala removeria.
    z["de_l1"] = am["de_l1"]
    stats["de_l1"] = (0.0, 1.0)
    z["de"] = am["de"]
    if ppp:
        z["d_ppp"] = am["d_ppp"]
        stats["d_ppp"] = (0.0, 1.0)

    reg = escalar + (["de_l1"] if ar1 else [])
    return z, stats, reg


# ── o corte da amostra, fixado em disco ──────────────────────────────────────
def corte(force: bool = False) -> str:
    """O ultimo trimestre que ENTRA no ajuste, fixado em disco.

    Existe pela mesma razao do `model_fit_cutoff.json` do modelo mensal: uma
    regeracao de rotina recarrega o banco, e sem um corte declarado os
    coeficientes andariam sozinhos no dia em que todos os canais alcancassem o
    mesmo trimestre. **E um arquivo SEPARADO do mensal de proposito** -- reestimar
    um nao pode mover o outro.
    """
    if not force and _CUTOFF.exists():
        return json.loads(_CUTOFF.read_text(encoding="utf-8"))["corte"]
    z, _, _ = montar()
    ult = str(z.index.max())
    _DATA.mkdir(parents=True, exist_ok=True)
    _CUTOFF.write_text(json.dumps({"corte": ult}, indent=2), encoding="utf-8")
    return ult


def estimar(z: pd.DataFrame | None = None, reg: list[str] | None = None,
            ppp: bool = True, lam: float | None = None,
            ate: str | None = None) -> dict:
    """Ridge no lambda escolhido por walk-forward, com t de HAC ao lado.

    **Os t sao de MQ com HAC(%d) sobre o MESMO desenho, nao erros-padrao de
    Ridge** -- Ridge e estimativa pontual e nao tem distribuicao a resumir. Eles
    sao legiveis porque o lambda escolhido pousa no PISO da grade, isto e, a
    penalidade e nominal; se um dia ele subir, esta coluna deixa de valer e a
    funcao diz isso no campo `t_valem`.
    """ % HAC_LAGS
    if z is None:
        z, _, reg = montar(ppp=ppp)
    if reg is None:
        raise ValueError("reg e obrigatorio quando z e passado")

    ate = corte() if ate is None else ate
    z = z[z.index <= pd.Period(ate, "Q")]

    off = OFFSET if ppp else None
    cv = _rd.walk_forward_lambda(z, reg, min_train=MIN_TRAIN, y_col="de", offset_col=off)
    lam = float(cv.iloc[0]["lambda"]) if lam is None else lam
    w = _rd.fit_whole_sample(z, reg, lam, y_col="de", offset_col=off)

    # o mesmo desenho por MQ, so para ter t e diagnostico de residuo
    y = z["de"].to_numpy(float) - (z[OFFSET].to_numpy(float) if ppp else 0.0)
    X = sm.add_constant(z[reg].to_numpy(float))
    ols = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": HAC_LAGS})
    nomes = ["alpha"] + reg

    fit = (z[OFFSET] if ppp else 0.0) + w["alpha"] + z[reg].to_numpy(float) @ np.array(
        [w["beta"][c] for c in reg])
    resid = z["de"] - fit

    # contribuicao acumulada de cada termo, em p.p. de log -- a leitura que a
    # barra do FX Report mostra. Soma exatamente a variacao explicada.
    contrib = {c: float(w["beta"][c] * z[c].sum()) for c in reg}
    if ppp:
        contrib[OFFSET] = float(z[OFFSET].sum())
    contrib["alpha"] = float(w["alpha"] * len(z))

    e = resid.to_numpy(float)
    lbt = acorr_ljungbox(e, lags=[4, 8], return_df=True)

    return {
        "estimador": "Ridge, lambda por walk-forward (min_train=%d)" % MIN_TRAIN,
        "lam": lam, "piso": bool(lam <= _rd._LAMBDA_GRID[0] * 1.001),
        "t_valem": bool(lam <= _rd._LAMBDA_GRID[0] * 1.001),
        "cv": cv, "n": w["n"], "ini": z.index[0], "fim": z.index[-1],
        "alpha": w["alpha"], "beta": w["beta"], "r2": w["r2"],
        "reg": reg, "ppp": ppp,
        "t": dict(zip(nomes, ols.tvalues)), "se": dict(zip(nomes, ols.bse)),
        "p": dict(zip(nomes, ols.pvalues)),
        "rmse": float(np.sqrt((resid ** 2).mean())),
        "sd_y": float(z["de"].std()),
        "acf1": float(pd.Series(e).autocorr(1)),
        "lb_p4": float(lbt["lb_pvalue"].iloc[0]),
        "lb_p8": float(lbt["lb_pvalue"].iloc[1]),
        "contrib": contrib,
        "de_total": float(z["de"].sum()),
        "z": z, "fit": fit, "resid": resid,
    }


def nativo(r: dict, stats: dict) -> dict:
    """beta em unidade NATIVA do canal: beta_z / sd. O sd se cancela na
    contribuicao acumulada, entao este e o numero que se compara entre duas
    frequencias -- e o unico que e propriedade do dado, nao da escala."""
    return {c: (r["beta"][c] / stats[c][1] if stats[c][1] else float("nan"))
            for c in r["reg"]}


def correlacoes(z: pd.DataFrame, reg: list[str]) -> dict:
    """Correlacao BRUTA de cada regressor com a dependente.

    Existe porque ela e a leitura que o publico faz sozinho, e num modelo com canais
    correlacionados ela pode ter sinal OPOSTO ao do coeficiente. Ver `anatomia`.
    """
    return {c: float(z[c].corr(z["de"])) for c in reg}


def anatomia(z: pd.DataFrame, canal: str = "d_sp500",
             ordem: list[str] | None = None) -> list[dict]:
    """O coeficiente de um canal a medida que os controles entram.

    E o que separa "o dado esta errado" de "o coeficiente e CONDICIONAL": se o sinal
    do canal sozinho e um e o do modelo inteiro e outro, a diferenca esta nos
    controles, e esta funcao mostra em qual deles.
    """
    ordem = ["d_dxy_em", "d_fiscal"] if ordem is None else ordem
    todos = [c for c in z.columns if c.startswith(("d_", "de_")) and c != OFFSET
             and c != "de"]
    y = z["de"] - (z[OFFSET] if OFFSET in z.columns else 0.0)

    conjuntos = [[canal]]
    for c in ordem:
        conjuntos.append([canal, c])
    conjuntos.append([canal] + ordem)
    conjuntos.append(todos)

    vistos, out = set(), []
    for sub in conjuntos:
        chave = tuple(sorted(sub))
        if chave in vistos:
            continue
        vistos.add(chave)
        r = sm.OLS(y, sm.add_constant(z[sub])).fit()
        out.append({
            "controles": [c for c in sub if c != canal],
            "n_controles": len(sub) - 1,
            "b": float(r.params[canal]),
            "t": float(r.tvalues[canal]),
            "todos": sub is todos or len(sub) == len(todos),
        })
    return out


# ── comparacoes ──────────────────────────────────────────────────────────────
FORMAS = {
    "base": dict(desc="base: fechamento, vol defasada, PPP imposto, AR(1)"),
    "vol_contemp": dict(desc="vol do carry CONTEMPORÂNEA (a do modelo mensal)",
                        vol_contemp=True),
    "media": dict(desc="níveis pela MÉDIA do trimestre, não pelo fechamento",
                  como="media"),
    "sem_ppp": dict(desc="sem o offset de PPP — o alpha absorve a tendência",
                    ppp=False),
    "sem_ar": dict(desc="sem AR(1)", ar1=False),
}


def comparar() -> dict:
    """Cada forma na mesma amostra comum, para a diferenca ser do desenho."""
    montados = {}
    for k, cfg in FORMAS.items():
        kw = {a: v for a, v in cfg.items() if a != "desc"}
        montados[k] = montar(ppp=kw.get("ppp", True), ar1=kw.get("ar1", True),
                             vol_contemp=kw.get("vol_contemp", False),
                             como=kw.get("como", COMO))
    comum = None
    for z, _, _ in montados.values():
        comum = z.index if comum is None else comum.intersection(z.index)

    out = {}
    for k, cfg in FORMAS.items():
        z, st, reg = montados[k]
        r = estimar(z.loc[comum], reg, ppp=cfg.get("ppp", True))
        r["desc"], r["nativo"] = cfg["desc"], nativo(r, st)
        out[k] = r
    return out


def mensal_ao_lado() -> dict:
    """O modelo MENSAL que serve o FX Report, no mesmo corte que ele publica.

    Roda a especificacao que ship a (5 canais, PPP imposto, AR(1)) e devolve os
    betas em unidade nativa, para a comparacao ser de grandeza e nao de escala.
    """
    z, st, reg = _rd.build_plain_regression_sample(
        channels=_rd._CHANNELS_5, include_ppp=False, ppp_offset=True)
    c = _rd._load_fit_cutoff()
    if c:
        z = z[z.index <= pd.Timestamp(c + "-01") + pd.offsets.MonthEnd(0)]
    cv = _rd.walk_forward_lambda(z, reg, y_col="delta_fx", offset_col="delta_ppp")
    lam = float(cv.iloc[0]["lambda"])
    w = _rd.fit_whole_sample(z, reg, lam, y_col="delta_fx", offset_col="delta_ppp")
    nat = {c2: (w["beta"][c2] / st[c2][1] if st[c2][1] else float("nan")) for c2 in reg}
    return {"lam": lam, "n": w["n"], "r2": w["r2"], "alpha": w["alpha"],
            "beta": w["beta"], "nativo": nat, "reg": reg,
            "ini": z.index.min(), "fim": z.index.max(), "corte": c}


def _eq(c: str) -> str:
    """Nome do regressor trimestral -> o nome equivalente no modulo mensal."""
    return {"de_l1": "delta_fx_lag1"}.get(c, c.replace("d_", "delta_", 1))


# ── saida ────────────────────────────────────────────────────────────────────
def main() -> None:
    z, st, reg = montar()
    r = estimar(z, reg)
    nat = nativo(r, st)

    print("=" * 78)
    print("(F) o câmbio trimestral -- %s" % r["estimador"])
    print("    de(t) = dppp(t) + alpha + phi*de(t-1) + soma(beta_c * z(dc(t)))")
    print("    amostra %s -> %s, %d trimestres (corte fixado em %s)"
          % (r["ini"], r["fim"], r["n"], corte()))
    print("    lambda %.4f%s" % (r["lam"], "  (piso da grade)" if r["piso"] else ""))
    print()
    print("  %-38s %9s %9s %9s %12s"
          % ("", "beta (sd)", "t (HAC)", "acum. pp", "nativo"))
    for c in reg:
        print("  %-38s %9.4f %9.2f %9.1f %12.4f"
              % (ROT.get(c, c), r["beta"][c], r["t"][c], r["contrib"][c], nat[c]))
    print("  %-38s %9.4f %9.2f %9.1f" % ("Constante (alpha), p.p./trimestre",
                                          r["alpha"], r["t"]["alpha"], r["contrib"]["alpha"]))
    if r["ppp"]:
        print("  %-38s %9.4f %9s %9.1f"
              % (ROT[OFFSET], 1.0, "imposto", r["contrib"][OFFSET]))
    print()
    print("  R2 %.4f   RMSE %.2f p.p./trimestre   n %d" % (r["r2"], r["rmse"], r["n"]))
    print("  resíduo: autocorrelação de 1a ordem %+.2f | Ljung-Box Q(4) p %.3f, Q(8) p %.3f"
          % (r["acf1"], r["lb_p4"], r["lb_p8"]))
    print("  o câmbio andou %+.1f p.p. de log na amostra; a soma das contribuições dá %+.1f"
          % (r["de_total"], sum(r["contrib"].values())))

    print()
    print("-- o modelo MENSAL ao lado, em unidade nativa " + "-" * 31)
    m = mensal_ao_lado()
    print("  mensal: n %d, %s -> %s, lambda %.4f, R2 %.4f"
          % (m["n"], m["ini"].date(), m["fim"].date(), m["lam"], m["r2"]))
    print("  %-38s %12s %12s %10s" % ("", "trimestral", "mensal", "unidade"))
    for c in reg:
        e = _eq(c)
        if e in m["nativo"]:
            print("  %-38s %12.4f %12.4f %10s"
                  % (ROT.get(c, c), nat[c], m["nativo"][e], UNID.get(c, "")))
    print("  %-38s %12.4f %12.4f %10s"
          % ("Constante (alpha)", r["alpha"], m["alpha"], "p.p./período"))

    print()
    print("-- formas testadas (mesma amostra comum) " + "-" * 36)
    comp = comparar()
    print("  (n = %d em todas)" % comp["base"]["n"])
    print("  %-52s %7s %7s %8s %7s %6s"
          % ("", "R2", "RMSE", "alpha", "t alpha", "LB(4)"))
    for k, c in comp.items():
        print("  %-52s %7.4f %7.2f %+8.3f %7.2f %6.3f%s"
              % (c["desc"], c["r2"], c["rmse"], c["alpha"], c["t"]["alpha"],
                 c["lb_p4"], "  <--" if k == "base" else ""))
    print("  o RMSE da linha da MÉDIA não é comparável com os outros: a dependente é")
    print("  outra, e mais lisa -- desvio de %.2f contra %.2f no fechamento."
          % (comp["media"]["sd_y"], comp["base"]["sd_y"]))
    print()
    print("  o que a defasagem da volatilidade custa, canal a canal (beta em sd):")
    b, v = comp["base"], comp["vol_contemp"]
    for c in b["reg"]:
        print("    %-36s %+8.4f -> %+8.4f" % (ROT.get(c, c), b["beta"][c], v["beta"][c]))
    print("=" * 78)


if __name__ == "__main__":
    main()
