"""
Transformacoes genericas de series mensais para os toggles Nivel / Crescimento
x Nominal/Real usados pelas tabelas interativas de analytics/brasil/credit/ (abas Saldo,
Concessao e futuras abas — Taxa, Inadimplencia — que devem reusar as mesmas funcoes
em vez de reimplementar STL/deflacao/media-movel por aba).

Duas variantes do "Nivel", escolhidas por aba conforme a natureza da serie (ver
compute_variants() vs. compute_variants_ma3() abaixo):
  - Series de estoque (saldo): Nivel = bruto (NSA); STL so entra para as variantes
    de crescimento M/M e T/T.
  - Series de fluxo (concessao etc.): Nivel = ja dessazonalizado (STL) + media movel
    de 3 meses — decisao explicita do usuario (2026-08), por essas series serem mais
    ruidosas mes a mes que um estoque. Crescimento (M/M, T/T) e calculado sobre essa
    base ja suavizada.

Convencao de ajuste sazonal (mesma de analytics/brasil/inflation/fetch_bcb.py — ver
.claude/rules/lis-dashboards.md e analytics/brasil/inflation/CLAUDE.md): STL com fatores
"amostra anual" — ajustados uma vez sobre o historico ate o ultimo dezembro completo
(auto-detectado), depois aplicados congelados a serie inteira, incluindo meses
posteriores ao corte. Os fatores só mudam quando um novo janeiro chega (dezembro fica
fora da amostra ate entao) — ex: gerando o relatorio em 2026, usa fatores ajustados
ate 2025-12.

T/T (trimestre contra trimestre) usa a convencao "3M/3M rolante" sobre o nivel
dessazonalizado (mes t vs. t-3), nao trimestre civil — decisao explicita do usuario,
2026-08 (mesma logica de "momentum trimestral" ja usada em atv_pim/atv_pim_uso).
Y/Y usa o nivel bruto (NSA) — variacao interanual ja cancela sazonalidade por
construcao, sem precisar de STL.

Todas as funcoes trabalham sobre listas paralelas {dates, values} (values pode conter
None), o mesmo formato que generate_report.py ja produz e que o `ser()`/`lastValid()`
do report.html ja consome — nenhuma serie perde posicoes, so ganha None onde a
transformacao nao pode ser calculada (ex: os primeiros 12 meses de uma serie de Y/Y).

"% do PIB" (opcional, `gdp_acum_12m` em compute_variants()/compute_variants_ma3(),
2026-08): so a variante "level" (decisao explicita do usuario — nao ha Y/Y/M-M/T-T de
uma razao credito/PIB nesta v1), calculada dividindo o proprio nivel nominal pelo PIB
acumulado nos ultimos 12 meses (BCB SGS 4382, `atv_pib_mensal.pib_acum_12m`) — mesmo
denominador que o BCB usa para publicar `cred_credito_resumo.pct_pib_*` (confirmado ao
vivo: bate exatamente com `pct_pib_total_total`).
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def seasonal_cutoff(dates: list[str]) -> str:
    """'YYYY-MM' do ultimo dezembro completo antes do fim da serie — ver docstring do
    modulo. `dates` no formato 'YYYY-MM-DD'.
    """
    last_year = int(max(dates)[:4])
    return f"{last_year - 1}-12"


def stl_seasonal_adjust(dates: list[str], values: list, min_obs: int = 24) -> list:
    """Dessazonaliza uma serie mensal via STL, fatores fixos amostrados ate o ultimo
    dezembro completo (ver docstring do modulo). Retorna lista alinhada a `dates`, com
    None onde o dado bruto e None/NaN ou a serie e curta/instavel demais para o STL.
    """
    from statsmodels.tsa.seasonal import STL

    vals = pd.Series(values, dtype="float64")
    if vals.count() < min_obs:
        return [None] * len(dates)

    cutoff = seasonal_cutoff(dates)
    month_num = pd.to_datetime([d[:7] + "-01" for d in dates]).month.to_numpy()
    in_mask = np.array([d[:7] <= cutoff for d in dates])

    vals_in = vals[in_mask].interpolate(limit_direction="both")
    if vals_in.count() < min_obs or vals_in.isna().any():
        return [None] * len(dates)

    try:
        fit = STL(vals_in.to_numpy(), period=12, robust=True).fit()
    except Exception:
        return [None] * len(dates)

    months_in = month_num[in_mask]
    seasonal_factor = {}
    for m in range(1, 13):
        idx = months_in == m
        if idx.any():
            seasonal_factor[m] = float(fit.seasonal[idx].mean())

    seasonal = np.array([seasonal_factor.get(m, 0.0) for m in month_num])
    sa = vals.to_numpy() - seasonal
    return [None if np.isnan(v) else float(v) for v in sa]


def pct_change(values: list, periods: int) -> list:
    """Variacao percentual entre `values[i]` e `values[i-periods]`, em %. None onde
    nao ha par valido (inicio da serie ou algum dos dois pontos ausente).

    None TAMBEM quando a base e exatamente zero: pandas emite `inf` nesse caso, e o
    guard antigo (`np.isnan`) nao pegava, entao um `Infinity` literal vazava para o
    JSON e renderizava na tabela (e destruia o range Y do grafico -- uma trace com um
    ponto infinito faz o autorange do Plotly e o `_bindYAutofit` colapsarem). E o guard
    que analytics/metric_layers.md registrava como pendente ("Zero base -> Infinity");
    implementado 2026-08. Uma variacao percentual sobre base zero e indefinida, nao
    infinita -- e uma serie esparsa (a maioria das 28 funcoes orcamentarias nunca recebe
    inversao financeira) esta cheia dessas transicoes.
    """
    vals = pd.Series(values, dtype="float64")
    pct = vals.pct_change(periods=periods, fill_method=None) * 100
    return [None if not np.isfinite(v) else float(v) for v in pct]


def build_price_index(dates: list[str], monthly_pct: list) -> dict:
    """Indice de precos encadeado a partir da variacao mensal (%) do IPCA (base 100 no
    primeiro mes da serie de entrada). So usado para razoes entre duas datas
    (deflacionar) — a base escolhida e arbitraria, nao afeta o resultado.
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
    `price_index` (ver build_price_index). None onde o valor nominal ou o indice de
    precos naquela data nao existem.
    """
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


def sum_series(*series: dict) -> dict:
    """Soma varias series {dates, values} ponto a ponto pela uniao das datas (nao
    assume calendarios identicos). Um valor None em qualquer serie naquela data produz
    None no total (nao trata None como zero) — mesma logica do sumSeries() client-side
    de report.html (usado pela antiga aba Credito Ampliado), agora em Python para poder
    alimentar compute_variants()/compute_variants_ma3(). Soma de NIVEIS (R$) e sempre
    matematicamente valida — o que nunca se deve fazer e somar series de crescimento/
    percentual (ver saldo_tab.py's docstring sobre "grupo sem total nativo")."""
    if not series:
        return {"dates": [], "values": []}
    all_dates = sorted(set().union(*[s["dates"] for s in series]))
    maps = [dict(zip(s["dates"], s["values"])) for s in series]
    values = []
    for d in all_dates:
        vs = [m.get(d) for m in maps]
        values.append(None if any(v is None for v in vs) else sum(vs))
    return {"dates": all_dates, "values": values}


def to_date_map(series: dict) -> dict:
    """{"dates": [...], "values": [...]} -> {date: value} -- forma que compute_pct_pib()
    (e build_price_index() indiretamente) esperam para lookup por data."""
    return dict(zip(series["dates"], series["values"]))


def compute_pct_pib(dates: list[str], level_values: list, gdp_acum_12m: dict) -> list:
    """`level_values[i]` / PIB acumulado nos 12 meses ate `dates[i]`, em % (mesmo
    denominador que o proprio BCB usa para publicar cred_credito_resumo.pct_pib_* —
    confirmado ao vivo: saldo_total_total / pib_acum_12m * 100 reproduz
    pct_pib_total_total exatamente, 55,76% em 2026-06 nos dois casos). None onde o
    valor ou o PIB naquela data nao existem.
    """
    out = []
    for d, v in zip(dates, level_values):
        gdp = gdp_acum_12m.get(d)
        if v is None or gdp is None:
            out.append(None)
        else:
            out.append(v / gdp * 100)
    return out


def compute_variants(
    dates: list[str], nominal_values: list, price_index: dict | None, ref_date: str | None,
    gdp_acum_12m: dict | None = None,
) -> dict:
    """Nivel/Y-Y/M-M(SA)/T-T(SA) para uma serie, em termos nominais e (se
    `price_index` for passado) reais, mais opcionalmente "% do PIB". Retorna:

        {"nominal": {"level": {...}, "yoy": {...}, "mom_sa": {...}, "qoq_sa": {...}},
         "real":    {...},                                        # so se price_index
         "pctpib":  {"level": {...}}}                              # so se gdp_acum_12m

    Cada variante e {"dates": dates, "values": [...]}, sempre do mesmo tamanho que
    `dates` (None onde nao aplicavel). Usado pela aba Saldo — series de estoque, onde o
    "Nivel" faz sentido como o saldo bruto (NSA), so dessazonalizado internamente para
    as variantes de crescimento M/M e T/T. Ver compute_variants_ma3() para series de
    fluxo (Concessao etc.), onde o proprio nivel exibido ja e dessazonalizado.

    "% do PIB" so tem a variante "level" (decisao explicita do usuario, 2026-08) — nao
    faz sentido "Y/Y de uma razao credito/PIB" no mesmo botao que "Y/Y de um saldo em
    R$", e a UI (makeHierTab) forca o metrico de volta para "level" ao escolher essa
    base. E sempre calculado sobre o nivel NOMINAL (a razao nominal/PIB-nominal e
    identica a real/PIB-real, ja que o deflator cancela — nao precisa de uma segunda
    versao "real" desta variante).
    """
    def _variants(values):
        sa = stl_seasonal_adjust(dates, values)
        return {
            "level":  {"dates": dates, "values": values},
            "yoy":    {"dates": dates, "values": pct_change(values, 12)},
            "mom_sa": {"dates": dates, "values": pct_change(sa, 1)},
            "qoq_sa": {"dates": dates, "values": pct_change(sa, 3)},
        }

    out = {"nominal": _variants(nominal_values)}
    if price_index is not None:
        real_values = deflate_series(dates, nominal_values, price_index, ref_date)
        out["real"] = _variants(real_values)
    if gdp_acum_12m is not None:
        out["pctpib"] = {"level": {"dates": dates, "values": compute_pct_pib(dates, nominal_values, gdp_acum_12m)}}
    return out


def moving_average(values: list, window: int) -> list:
    """Media movel trailing (janela termina no ponto atual — [t-window+1, t]), com
    None enquanto a janela nao estiver completa. Mesma convencao MA(3) ja usada em
    analytics/brasil/inflation/fetch_bcb.py's _apply_stl_ma3."""
    vals = pd.Series(values, dtype="float64")
    ma = vals.rolling(window=window, min_periods=window).mean()
    return [None if np.isnan(v) else float(v) for v in ma]


def compute_variants_ma3(
    dates: list[str], nominal_values: list, price_index: dict | None, ref_date: str | None, ma_window: int = 3,
    gdp_acum_12m: dict | None = None,
) -> dict:
    """Nivel/M-M/T-T para series de fluxo (Concessao etc.), em termos nominais e (se
    `price_index` for passado) reais, mais opcionalmente "% do PIB". Decisao explicita
    do usuario (2026-08): para essas series, a propria base ("Nivel") ja e a serie
    dessazonalizada (STL) + media movel de `ma_window` meses (MM3M por default) — nao o
    nivel bruto como em compute_variants(). As variantes de crescimento (M/M, T/T =
    3M/3M rolante) sao calculadas sobre essa base ja suavizada, nao sobre o bruto. Sem
    Y/Y aqui (nao pedido para esta aba). Retorna:

        {"nominal": {"level": {...}, "mom": {...}, "qoq": {...}}, "real": {...},
         "pctpib": {"level": {...}}}

    "% do PIB" (so "level", mesmo raciocinio de compute_variants()) usa a base
    NOMINAL ja suavizada (SA+MM3M) dividida pelo PIB acumulado 12m — nao o valor bruto
    do mes nem uma soma de 12 meses de concessao, para ficar na mesma unidade "nivel"
    que o resto da coluna/grafico ja mostra.
    """
    def _variants(values):
        sa = stl_seasonal_adjust(dates, values)
        base = moving_average(sa, ma_window)
        return base, {
            "level": {"dates": dates, "values": base},
            "mom":   {"dates": dates, "values": pct_change(base, 1)},
            "qoq":   {"dates": dates, "values": pct_change(base, 3)},
        }

    nominal_base, nominal_variants = _variants(nominal_values)
    out = {"nominal": nominal_variants}
    if price_index is not None:
        real_values = deflate_series(dates, nominal_values, price_index, ref_date)
        out["real"] = _variants(real_values)[1]
    if gdp_acum_12m is not None:
        out["pctpib"] = {"level": {"dates": dates, "values": compute_pct_pib(dates, nominal_base, gdp_acum_12m)}}
    return out
