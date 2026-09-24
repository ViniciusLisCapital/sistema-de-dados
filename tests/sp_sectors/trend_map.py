"""Mapa de tendencias do SPY — estado de cada pregao (alta / baixa / lateral) em dummies.

Duas leituras, porque a pergunta "no dia T estavamos em tendencia?" tem duas
respostas legitimas e elas NAO sao intercambiaveis:

A) ESTADO DIARIO (sem look-ahead) — regressao do log-preco no tempo sobre a
   janela dos ultimos N pregoes: inclinacao anualizada b e R2.
       alta    : b > +limiar  e  R2 >= r_min
       baixa   : b < -limiar  e  R2 >= r_min
       lateral : o resto (inclinacao pequena OU caminho sem direcao)
   Usa so dado passado, entao serve como regressor em qualquer teste que olhe
   para frente. E a coluna a usar se as dummies vao para uma regressao.

B) PERNAS (ex-post) — segmentacao por swing/zigzag: um pivo e confirmado quando
   o preco recua theta% do extremo corrente. Da o mapa das tendencias
   "relevantes" com inicio, fim, magnitude e as metricas de qualidade de
   trend_quality.py.
   ATENCAO: o pivo e datado RETROATIVAMENTE — so se sabe que 16/08/2022 era o
   topo depois da queda que o confirmou. Otimo para estudar a anatomia de uma
   perna, invalido como sinal em tempo real.

O zigzag nunca produz "lateral": ele sempre atribui direcao. Por isso o terceiro
estado so existe na leitura A, que mede direcao contra ruido em vez de so ligar
dois extremos.

Uso: uv run python tests/sp_sectors/trend_map.py [--janela 126] [--limiar 8] [--r2 0.30] [--theta 15]
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

_XLSX_IN = Path(__file__).parents[2] / "SPY e Setores S&P.xlsx"
_XLSX_OUT = Path(__file__).parents[2] / "SPY Tendencias.xlsx"


# ---------------------------------------------------------------- A) estado diario
def estado_diario(p: pd.Series, janela: int, limiar_aa: float, r2_min: float) -> pd.DataFrame:
    """Inclinacao anualizada e R2 da regressao do log-preco no tempo, janela movel."""
    lp = np.log(p.values)
    n = len(lp)
    x = np.arange(janela, dtype=float)
    xc = x - x.mean()
    sxx = (xc ** 2).sum()

    b = np.full(n, np.nan)
    r2 = np.full(n, np.nan)
    for i in range(janela - 1, n):
        y = lp[i - janela + 1:i + 1]
        yc = y - y.mean()
        sxy = (xc * yc).sum()
        syy = (yc ** 2).sum()
        b[i] = sxy / sxx                      # log por pregao
        r2[i] = (sxy ** 2) / (sxx * syy) if syy > 0 else np.nan

    b_aa = (np.exp(b * 252) - 1) * 100        # % a.a.
    # "indefinido" e a janela de aquecimento (os primeiros janela-1 pregoes).
    # Rotular explicitamente em vez de deixar em branco: no Excel o branco volta
    # como NaN e as tres dummies ficam 0, que se le como "nenhum estado" quando
    # na verdade e "ainda nao da para dizer".
    estado = np.where(np.isnan(b_aa), "indefinido",
             np.where((b_aa > limiar_aa) & (r2 >= r2_min), "alta",
             np.where((b_aa < -limiar_aa) & (r2 >= r2_min), "baixa", "lateral")))

    return pd.DataFrame({
        "inclinacao_pct_aa": b_aa, "r2": r2, "estado": estado,
        "d_alta": (estado == "alta").astype(int),
        "d_baixa": (estado == "baixa").astype(int),
        "d_lateral": (estado == "lateral").astype(int),
    }, index=p.index)


# ---------------------------------------------------------------- B) pernas (zigzag)
def zigzag(p: np.ndarray, theta: float) -> list:
    """Indices dos pivos alternados. Pivo confirmado quando o preco recua theta do extremo."""
    hi = lo = 0
    dirn = 0
    piv = []
    for i in range(1, len(p)):
        if dirn == 0:
            if p[i] > p[hi]:
                hi = i
            if p[i] < p[lo]:
                lo = i
            if p[i] <= p[hi] * (1 - theta):
                piv.append(hi); dirn = -1; lo = i
            elif p[i] >= p[lo] * (1 + theta):
                piv.append(lo); dirn = +1; hi = i
        elif dirn == +1:
            if p[i] > p[hi]:
                hi = i; lo = i                # novo topo zera o recuo em curso
            elif p[i] < p[lo]:
                lo = i
            if p[i] <= p[hi] * (1 - theta):
                piv.append(hi); dirn = -1; lo = i
        else:
            if p[i] < p[lo]:
                lo = i; hi = i
            elif p[i] > p[hi]:
                hi = i
            if p[i] >= p[lo] * (1 + theta):
                piv.append(lo); dirn = +1; hi = i
    # extremo corrente fecha a perna em aberto (ainda nao confirmada)
    piv.append(hi if dirn == +1 else (lo if dirn == -1 else len(p) - 1))
    return sorted(set([0] + piv))


def metricas_perna(p: pd.Series) -> dict:
    lp = np.log(p.values)
    d = np.diff(lp)
    ret = float(np.exp(lp[-1] - lp[0]) - 1)
    return {
        "ret_pct": ret * 100,
        "vel_pct_aa": (np.exp((lp[-1] - lp[0]) * 252 / len(d)) - 1) * 100,
        "efficiency_ratio": abs(lp[-1] - lp[0]) / np.abs(d).sum(),
        "r2": float(np.corrcoef(np.arange(len(lp)), lp)[0, 1] ** 2),
        "max_dd_pct": float((p / p.cummax() - 1).min()) * 100,
        "vol_pct_aa": float(d.std(ddof=1) * np.sqrt(252)) * 100,
    }


def pernas(p: pd.Series, theta: float) -> pd.DataFrame:
    piv = zigzag(p.values, theta)
    linhas = []
    for k, (a, b) in enumerate(zip(piv[:-1], piv[1:]), 1):
        seg = p.iloc[a:b + 1]
        m = metricas_perna(seg)
        linhas.append({
            "perna": k,
            "inicio": seg.index[0].date(), "fim": seg.index[-1].date(),
            "direcao": "alta" if m["ret_pct"] > 0 else "baixa",
            "pregoes": len(seg), "dias_corridos": (seg.index[-1] - seg.index[0]).days,
            "preco_ini": round(seg.iloc[0], 2), "preco_fim": round(seg.iloc[-1], 2),
            **m,
            "_ia": a, "_ib": b,
        })
    return pd.DataFrame(linhas)


def run(janela=126, limiar=8.0, r2_min=0.30, theta=15.0, ticker="SPY"):
    p = pd.read_excel(_XLSX_IN, sheet_name="adj_close", index_col=0, parse_dates=[0])[ticker].dropna()

    diario = estado_diario(p, janela, limiar, r2_min)
    lg = pernas(p, theta / 100)

    # dummies ex-post da perna, projetadas no dia
    dp = pd.Series("", index=p.index)
    for _, r in lg.iterrows():
        dp.iloc[r["_ia"]:r["_ib"] + 1] = r["direcao"]
    diario.insert(0, "preco", p)
    diario["perna_direcao"] = dp
    diario["dp_alta"] = (dp == "alta").astype(int)
    diario["dp_baixa"] = (dp == "baixa").astype(int)

    # bloco = trecho contiguo no mesmo estado, para contar duracao
    diario["bloco"] = (diario["estado"] != diario["estado"].shift()).cumsum()
    val = diario[diario["estado"] != "indefinido"]
    resumo = (val["estado"].value_counts(normalize=True) * 100).rename("pct_pregoes").to_frame()
    resumo["pregoes"] = val["estado"].value_counts()
    bl = val.groupby("bloco")["estado"].agg(["first", "size"])
    dur = bl.groupby("first")["size"].agg(blocos="count", mediana_pregoes="median", max_pregoes="max")
    resumo = resumo.join(dur)

    lg_out = lg.drop(columns=["_ia", "_ib"])
    with pd.ExcelWriter(_XLSX_OUT, engine="openpyxl", datetime_format="YYYY-MM-DD") as xl:
        diario.reset_index().to_excel(xl, sheet_name="diario", index=False)
        lg_out.to_excel(xl, sheet_name="pernas", index=False)
        resumo.reset_index().to_excel(xl, sheet_name="resumo", index=False)
        pd.DataFrame([{"ticker": ticker, "janela_pregoes": janela, "limiar_pct_aa": limiar,
                       "r2_min": r2_min, "theta_zigzag_pct": theta,
                       "inicio": p.index[0].date(), "fim": p.index[-1].date()}]
                     ).to_excel(xl, sheet_name="parametros", index=False)

    print(f"A) estado diario - janela {janela} pregoes, |b| > {limiar}% a.a., R2 >= {r2_min}")
    print(resumo.to_string(float_format=lambda v: f"{v:6.1f}"))
    print(f"\nB) pernas - zigzag theta = {theta}%  ({len(lg)} pernas)")
    cols = ["perna", "inicio", "fim", "direcao", "pregoes", "ret_pct", "vel_pct_aa",
            "efficiency_ratio", "r2", "max_dd_pct"]
    print(lg_out[cols].to_string(index=False, float_format=lambda v: f"{v:8.2f}"))
    print(f"\n{_XLSX_OUT}")
    return diario, lg_out, resumo


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--janela", type=int, default=126)
    ap.add_argument("--limiar", type=float, default=8.0)
    ap.add_argument("--r2", dest="r2_min", type=float, default=0.30)
    ap.add_argument("--theta", type=float, default=15.0)
    ap.add_argument("--ticker", default="SPY")
    a = ap.parse_args()
    run(a.janela, a.limiar, a.r2_min, a.theta, a.ticker)
