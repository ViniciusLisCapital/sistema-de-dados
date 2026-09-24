"""Qualidade de uma tendencia — caso de estudo: SPY, 2022-06-17 -> 2022-08-16.

Uma perna de alta tem DUAS propriedades independentes, e confundi-las e o erro
central do assunto: quanto ela andou (magnitude) e quao limpo foi o caminho
(qualidade). +17% em 41 pregoes pode vir de uma reta ou de um ziguezague que
acabou no mesmo lugar — a mesma magnitude, qualidades opostas.

As cinco medidas abaixo sao todas de CAMINHO (invariantes a magnitude, exceto
onde dito), e nenhuma delas significa nada sozinha: um R2 de 0,90 e alto ou
baixo dependendo da distribuicao de R2 de todas as janelas de mesmo tamanho na
historia da serie. Por isso todo numero sai com o percentil ao lado, medido
contra as janelas de 41 pregoes de TODA a serie e contra o subconjunto de
janelas que tambem subiram (a comparacao honesta: uma perna de alta nao
compete com quedas).

Uso: uv run python tests/sp_sectors/trend_quality.py [--inicio 2022-06-17] [--fim 2022-08-16]
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

_XLSX = Path(__file__).parent / "sp_sector_etfs.xlsx"


def metricas(p: pd.Series) -> dict:
    """Metricas de caminho de uma perna, sobre a serie de precos `p` (inclusive nas pontas)."""
    lp = np.log(p.values)
    d = np.diff(lp)                       # retornos log diarios
    n = len(d)
    ret = float(np.exp(lp[-1] - lp[0]) - 1)

    # Efficiency ratio (Kaufman): deslocamento liquido / distancia percorrida.
    # 1,0 = reta perfeita (nenhum movimento contrario); 0 = puro ziguezague.
    er = abs(lp[-1] - lp[0]) / np.abs(d).sum()

    # R2 da regressao do log-preco no tempo: quanto do caminho e explicado por
    # uma reta. Mede linearidade da TRAJETORIA, nao ausencia de movimento contrario.
    x = np.arange(len(lp))
    r2 = float(np.corrcoef(x, lp)[0, 1] ** 2)

    # Maior recuo desde o topo corrente DENTRO da perna — o que o detentor
    # teve de aguentar sem que a tendencia se quebrasse.
    dd = float((p / p.cummax() - 1).min())

    pct_alta = float((d > 0).mean())
    # Maior sequencia de pregoes de baixa consecutivos.
    run, pior = 0, 0
    for v in d:
        run = run + 1 if v < 0 else 0
        pior = max(pior, run)

    vol = float(d.std(ddof=1) * np.sqrt(252))
    return {
        "ret_%": ret * 100,
        "ret_anual_%": (np.exp((lp[-1] - lp[0]) * 252 / n) - 1) * 100,
        "n_pregoes": n + 1,
        "efficiency_ratio": er,
        "r2_log_tempo": r2,
        "max_dd_%": dd * 100,
        "pct_dias_alta": pct_alta * 100,
        "maior_seq_baixa": pior,
        "vol_anual_%": vol * 100,
        "ret_sobre_vol": (np.exp((lp[-1] - lp[0]) * 252 / n) - 1) / vol,
    }


def percentis(serie: pd.Series, alvo: dict, n: int) -> pd.DataFrame:
    """Distribuicao das mesmas metricas em TODAS as janelas de `n` pregoes da serie."""
    vals = serie.values
    linhas = [metricas(pd.Series(vals[i:i + n], index=serie.index[i:i + n]))
              for i in range(len(vals) - n + 1)]
    todas = pd.DataFrame(linhas)
    subiu = todas[todas["ret_%"] > 0]

    campos = ["ret_%", "efficiency_ratio", "r2_log_tempo", "max_dd_%",
              "pct_dias_alta", "vol_anual_%", "ret_sobre_vol"]
    out = []
    for c in campos:
        v = alvo[c]
        out.append({
            "metrica": c,
            "valor": v,
            "pct_vs_todas": (todas[c] < v).mean() * 100,
            "pct_vs_altas": (subiu[c] < v).mean() * 100,
            "mediana_altas": subiu[c].median(),
        })
    return pd.DataFrame(out), todas, subiu


def run(inicio: str = "2022-06-17", fim: str = "2022-08-16", ticker: str = "SPY"):
    p = pd.read_excel(_XLSX, sheet_name="adj_close", index_col=0, parse_dates=[0])[ticker].dropna()
    leg = p.loc[inicio:fim]
    m = metricas(leg)

    print(f"{ticker}  {leg.index[0].date()} -> {leg.index[-1].date()}   "
          f"{leg.iloc[0]:.2f} -> {leg.iloc[-1]:.2f}")
    print(f"  {m['n_pregoes']} pregoes ({(leg.index[-1]-leg.index[0]).days} dias corridos)\n")

    tab, todas, subiu = percentis(p, m, m["n_pregoes"])
    tab.columns = ["metrica", "valor", "percentil (todas)", "percentil (so altas)", "mediana das altas"]
    print(tab.to_string(index=False, float_format=lambda v: f"{v:8.2f}"))
    print(f"\n  janelas de {m['n_pregoes']} pregoes na serie: {len(todas)}  "
          f"(destas, {len(subiu)} de alta, {len(subiu)/len(todas)*100:.0f}%)")
    print(f"  maior sequencia de baixas dentro da perna: {m['maior_seq_baixa']} pregoes")
    return m, tab


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--inicio", default="2022-06-17")
    ap.add_argument("--fim", default="2022-08-16")
    ap.add_argument("--ticker", default="SPY")
    a = ap.parse_args()
    run(a.inicio, a.fim, a.ticker)
