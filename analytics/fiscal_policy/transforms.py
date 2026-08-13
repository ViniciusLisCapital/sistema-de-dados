"""
Transformacoes genericas de series TRIMESTRAIS para os toggles Nivel/Y-Y/T-T x
Nominal/Real usados pela tabela hierarquica da aba Receitas e Despesas (GFSM) --
mesma ideia de analytics/credit/transforms.py (STL + deflacao IPCA + %PIB
pre-computados em Python, o browser so troca qual variante ja calculada e exibida),
adaptada de mensal para trimestral: STL usa period=4 (nao 12), Y/Y compara contra
4 trimestres atras (nao 12 meses), e nao ha variante M/M (dado ja e trimestral).

Nivel = valor bruto (NSA) do proprio trimestre -- mesma convencao do "Nivel" da aba
Saldo do relatorio de credito (nao um acumulado). Y/Y usa esse nivel bruto: variacao
interanual (trimestre t vs. mesmo trimestre um ano antes) ja cancela sazonalidade por
construcao, sem precisar de ajuste sazonal algum -- mesmo raciocinio do modulo irmao.

T/T (trimestre contra o trimestre imediatamente anterior) SIM precisa de ajuste
sazonal: series GFSM de receita/despesa por natureza economica tem um calendario de
execucao orcamentaria fortemente sazonal dentro do ano (13o salario, concentracao de
investimento no ultimo trimestre etc.) -- exatamente o problema ja identificado e
corrigido uma vez neste mesmo relatorio para o IEG (ver
domain/db/brasil/tesouro/fisc_efgg.py's consumidor,
analytics/fiscal_policy/generate_report.py's _load_ieg() docstring): um diff()
trimestral bruto reproduziria essa sazonalidade em vez de medir uma variacao real.
Aqui T/T = STL(period=4) + diff(1) sobre a base dessazonalizada -- o analogo direto
do "T/T = 3M/3M rolante sobre o nivel dessazonalizado" de credit/transforms.py, so
trocando a periodicidade mensal por trimestral. Diferente do modulo irmao, o fit do
STL aqui NAO usa a convencao "amostra anual congelada" (fatores fixados ate o ultimo
dezembro completo) -- a amostra e pequena (~65 trimestres, contra series mensais de
decadas em credit/), entao um fit unico sobre toda a serie disponivel a cada geracao
do relatorio e suficiente; T/T tambem e uma metrica secundaria aqui, nao o indicador
publicado (esse e o IEG, que ja tem sua propria logica validada em _load_ieg()).

"% do PIB" segue a convencao ja estabelecida no restante deste relatorio (fisc_nfsp,
IEG) -- acumulado em 4 trimestres (TTM) do proprio valor dividido pelo TTM do PIB --
e NAO a de credit/transforms.py (nivel de um mes sobre o PIB acumulado 12m), que
sub-estimaria a razao usual "despesa/receita como % do PIB" para uma serie de fluxo
trimestral (mostraria ~5% em vez de ~20% para uma categoria que de fato representa
~20% do PIB anual). Só a variante Nivel (mesma decisao do modulo irmao -- nao faz
sentido Y/Y de uma razao fluxo/PIB), sempre nominal (a razao nominal/PIB-nominal e
identica a real/PIB-real, o deflator cancela).

Todas as funcoes trabalham sobre listas paralelas {dates, values} (values pode conter
None) no mesmo formato que generate_report.py ja produz.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def stl_seasonal_adjust(dates: list[str], values: list, period: int = 4, min_obs: int = 8) -> list:
    """Dessazonaliza uma serie trimestral via STL, fit unico sobre toda a serie
    disponivel (ver docstring do modulo para por que nao ha convencao de "amostra
    congelada" aqui). Retorna lista alinhada a `dates`, com None onde o dado bruto e
    None/NaN ou a serie e curta/instavel demais para o STL.
    """
    from statsmodels.tsa.seasonal import STL

    vals = pd.Series(values, dtype="float64")
    if vals.count() < min_obs:
        return [None] * len(dates)

    vals_filled = vals.interpolate(limit_direction="both")
    if vals_filled.isna().any():
        return [None] * len(dates)

    try:
        fit = STL(vals_filled.to_numpy(), period=period, robust=True).fit()
    except Exception:
        return [None] * len(dates)

    sa = vals.to_numpy() - fit.seasonal
    return [None if np.isnan(v) else float(v) for v in sa]


def pct_change(values: list, periods: int) -> list:
    """Variacao percentual entre `values[i]` e `values[i-periods]`, em %. None onde
    nao ha par valido."""
    vals = pd.Series(values, dtype="float64")
    pct = vals.pct_change(periods=periods, fill_method=None) * 100
    return [None if np.isnan(v) else float(v) for v in pct]


def build_price_index(dates: list[str], monthly_pct: list) -> dict:
    """Indice de precos encadeado a partir da variacao mensal (%) do IPCA (base 100 no
    primeiro mes da serie de entrada). `dates` de EFGG (inicio de trimestre) sempre
    coincidem com um mes real desta serie (Jan/Abr/Jul/Out), entao o lookup em
    deflate_series() casa diretamente, sem precisar reamostrar para trimestral.
    """
    idx = 100.0
    out = {}
    for d, p in zip(dates, monthly_pct):
        if p is not None and not (isinstance(p, float) and np.isnan(p)):
            idx = idx * (1 + p / 100.0)
        out[d] = idx
    return out


def deflate_series(dates: list[str], nominal_values: list, price_index: dict, ref_date: str) -> list:
    """Converte `nominal_values` para reais constantes de `ref_date`, usando
    `price_index` (ver build_price_index)."""
    ref_idx = price_index.get(ref_date)
    if ref_idx is None:
        raise ValueError(f"ref_date {ref_date!r} nao encontrado no indice de precos")

    out = []
    for d, v in zip(dates, nominal_values):
        idx = price_index.get(d)
        if v is None or idx is None:
            out.append(None)
        else:
            out.append(v * ref_idx / idx)
    return out


def compute_pct_pib_ttm(dates: list[str], nominal_values: list, gdp_ttm: dict, window: int = 4) -> list:
    """Acumulado em `window` trimestres (TTM, default 4) do proprio `nominal_values`,
    dividido pelo TTM do PIB (`gdp_ttm`, ja pre-computado em generate_report.py como
    PIB_pm.rolling(4).sum() -- mesmo denominador usado por fisc_nfsp/IEG neste
    relatorio). None onde a janela TTM ainda nao esta completa ou o PIB naquela data
    nao existe.
    """
    vals = pd.Series(nominal_values, dtype="float64")
    ttm = vals.rolling(window=window, min_periods=window).sum()
    out = []
    for d, v in zip(dates, ttm):
        gdp = gdp_ttm.get(d)
        if pd.isna(v) or gdp is None or pd.isna(gdp):
            out.append(None)
        else:
            out.append(float(v) / float(gdp) * 100)
    return out


def compute_variants(
    dates: list[str], nominal_values: list, price_index: dict | None, ref_date: str | None,
    gdp_ttm: dict | None = None,
) -> dict:
    """Nivel/Y-Y/T-T para uma serie trimestral, em termos nominais e (se
    `price_index` for passado) reais, mais opcionalmente "% do PIB". Retorna:

        {"nominal": {"level": {...}, "yoy": {...}, "qoq_sa": {...}},
         "real":    {...},                                        # so se price_index
         "pctpib":  {"level": {...}}}                              # so se gdp_ttm

    Cada variante e {"dates": dates, "values": [...]}, sempre do mesmo tamanho que
    `dates` (None onde nao aplicavel).
    """
    def _variants(values):
        sa = stl_seasonal_adjust(dates, values)
        return {
            "level":  {"dates": dates, "values": values},
            "yoy":    {"dates": dates, "values": pct_change(values, 4)},
            "qoq_sa": {"dates": dates, "values": pct_change(sa, 1)},
        }

    out = {"nominal": _variants(nominal_values)}
    if price_index is not None:
        real_values = deflate_series(dates, nominal_values, price_index, ref_date)
        out["real"] = _variants(real_values)
    if gdp_ttm is not None:
        out["pctpib"] = {"level": {"dates": dates, "values": compute_pct_pib_ttm(dates, nominal_values, gdp_ttm)}}
    return out
