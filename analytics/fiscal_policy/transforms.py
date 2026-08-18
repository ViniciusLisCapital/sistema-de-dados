"""
Transformacoes genericas de series TRIMESTRAIS (GFSM) e o equivalente TTM reusado pela
RTN (mensal) para os toggles Nivel/Y-Y/T-T(/M-M) x Nominal/Real/%PIB x Bruto/(Trimestral/)
Acumulado usados pelas duas tabelas hierarquicas da aba Receitas e Despesas -- mesma ideia
de analytics/credit/transforms.py (STL + deflacao IPCA + %PIB pre-computados em Python, o
browser so troca qual variante ja calculada e exibida).

Duas (GFSM) ou tres (RTN) modelagens de "Nivel", todas pre-computadas e disponiveis lado a
lado via um toggle Bruto/(Trimestral/)Acumulado (2026-08, adicao -- nenhuma substitui as
outras):
  - Bruto (compute_variants()/RTN via analytics.credit.transforms.compute_variants()):
    Nivel = valor do proprio periodo (NSA). Y/Y compara com o mesmo periodo um ano
    antes sobre o nivel bruto (a variacao interanual ja cancela sazonalidade por
    construcao). T/T (GFSM, trimestre contra trimestre anterior) e M/M+T/T (RTN, mes
    contra mes anterior / 3M contra 3M) usam STL para dessazonalizar antes do diff --
    sem isso, reproduziriam o calendario de execucao orcamentaria (13o salario,
    concentracao de investimento no ultimo periodo do ano etc.) em vez de uma variacao
    real.
  - Trimestral (compute_variants_quarterly_step() abaixo, SO RTN, 2026-08): Nivel =
    soma do trimestre CALENDARIO corrente (Jan+Fev+Mar, Abr+Mai+Jun etc.), NAO movel --
    ao contrario do Acumulado abaixo, que e uma janela de 12 meses recalculada todo mes.
    Reamostra a serie mensal da RTN no mesmo corte trimestral, sem sobreposicao, que a
    GFSM ja usa nativamente -- viabiliza comparar as duas tabelas trimestre a trimestre
    (ver Apendice, "GFSM vs. RTN"). Y/Y (defasagem 12 meses) e T/T (defasagem 3 meses,
    chave "qoq_sa" por compatibilidade) comparam o degrau do trimestre contra o mesmo
    trimestre um ano antes / o trimestre imediatamente anterior. Sem M/M (nao faz
    sentido dentro de um degrau constante) -- o lado JS cai para T/T automaticamente.
  - Acumulado (compute_variants_ttm()/compute_variants_monthly_ttm() abaixo): Nivel =
    acumulado movel (TTM -- trailing twelve months, embora "meses" vire trimestres na
    GFSM) sobre `window` periodos (4 trimestres GFSM, 12 meses RTN). Como o acumulado
    sempre soma um ciclo anual inteiro, cancela sazonalidade por CONSTRUCAO -- Y/Y
    compara o acumulado terminado em t contra o acumulado terminado `window` periodos
    antes (mesma logica "ano-movel contra ano-movel anterior" ja usada pelo IEG e por
    fisc_nfsp's colunas *_pct_pib_12m); T/T (ou M/M, RTN) compara o acumulado terminado
    em t contra o terminado no periodo imediatamente anterior -- uma medida de
    aceleracao/desaceleracao do proprio acumulado, sem STL (o acumulado ja resolve a
    sazonalidade). Fica tambem na mesma escala que "% do PIB" ja usa neste relatorio
    (TTM/TTM).
  - Acum. no ano (compute_variants_ytd() abaixo, 2026-08, so a aba Investimento): Nivel
    = acumulado no ano CIVIL, zerando em cada janeiro (ytd_sum()) -- nem movel como o
    TTM, nem um degrau de largura fixa como o trimestral: a janela CRESCE ao longo do
    ano, entao o valor de junho e comparavel so com o junho de outro ano. Por isso so
    Y/Y (defasagem 12 meses, Jan..M contra Jan..M do ano anterior); M/M e T/T nao sao
    oferecidos, atravessariam o reset de janeiro -- ver a docstring da funcao.

"% do PIB" (2026-08, revisado -- reorganizacao dos 3 eixos de metrica a pedido do
usuario, ver report.html): NAO e mais sempre TTM/TTM. Segue o mesmo periodo do Nivel
selecionado -- Mensal/Trimestral comparam o valor do proprio periodo com o PIB do MESMO
periodo (compute_pct_pib_same_period() abaixo, SEM acumular nenhum dos dois lados);
so o Nivel Acumulado 12m continua comparando acumulado com acumulado
(compute_pct_pib_ttm(), TTM/TTM, mesma convencao ja usada por fisc_nfsp/IEG no resto do
relatorio -- usuario confirmou que Acumulado 12m deve manter %PIB TTM/TTM, so a
modelagem "Marginal" fica indisponivel nesse nivel). Por isso "pctpib" NAO e mais
compartilhado entre as modelagens de Nivel -- cada uma calcula o seu proprio (ver
rtn_tab.py/gfsm_tab.py). Em ambos os casos, %PIB so existe em termos NOMINAIS (usuario:
"por hora deixa % PIB somente para nominal") -- ver Pending em
analytics/fiscal_policy/CLAUDE.md para a duvida em aberto sobre se a variante Real
deveria dividir por um PIB real em vez de nominal.

Ajuste sazonal (2026-08, a pedido do usuario): STL com os fatores estimados so ate o
ULTIMO ANO CIVIL COMPLETO, congelados para o ano corrente incompleto -- ver a docstring
de stl_seasonal_adjust() para o mecanismo e para a divergencia deliberada em relacao a
convencao de analytics/credit/transforms.py.

Todas as funcoes trabalham sobre listas paralelas {dates, values} (values pode conter
None) no mesmo formato que generate_report.py ja produz.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def seasonal_cutoff_year(dates: list[str], values: list, period: int) -> str | None:
    """Ultimo ano CIVIL COMPLETO da serie -- o ano mais recente que ja tem as `period`
    observacoes do ano com valor (4 trimestres, ou 12 meses). Ver stl_seasonal_adjust().
    None se nenhum ano da serie esta completo.
    """
    counts: dict[str, int] = {}
    for d, v in zip(dates, values):
        if v is None or (isinstance(v, float) and np.isnan(v)):
            continue
        counts[d[:4]] = counts.get(d[:4], 0) + 1
    completos = [y for y, n in counts.items() if n >= period]
    return max(completos) if completos else None


def _season_position(dates: list[str], period: int) -> np.ndarray:
    """Posicao de cada data dentro do ciclo sazonal: 1-12 (mes) se period=12, 1-4
    (trimestre) se period=4."""
    months = pd.to_datetime(dates).month.to_numpy()
    if period == 12:
        return months
    if period == 4:
        return (months - 1) // 3 + 1
    raise ValueError(f"period {period} nao suportado (use 4 ou 12)")


def stl_seasonal_adjust(dates: list[str], values: list, period: int = 4, min_obs: int | None = None) -> list:
    """Dessazonaliza via STL com os fatores sazonais estimados SO ate o ultimo ano civil
    completo, aplicados congelados ao ano corrente incompleto (2026-08, a pedido explicito
    do usuario -- "I want to use the STL factors until the complete year. For example, we
    run the sazonal factor until 2025 and apply them into 2026. When we complete the 2026
    and need to adjust the 1Q/2027 we re-run incorporating 2026"). Antes, o fit rodava
    sobre TODA a serie disponivel, incluindo o ano corrente pela metade -- o que faz o
    componente sazonal de um trimestre/mes ser estimado a partir de um ano truncado (e
    muda retroativamente a cada nova observacao que chega no meio do ano).

    Como funciona:
      1. `seasonal_cutoff_year()` acha o ultimo ano com as `period` observacoes completas
         (ex.: gerando o relatorio em 2026 com dado ate 2026-06, o corte e 2025).
      2. O STL roda SO sobre a amostra ate o fim daquele ano.
      3. Datas DENTRO da amostra usam o proprio `fit.seasonal` (sazonalidade evolutiva --
         a razao de usar STL em vez de um fator fixo).
      4. Datas DEPOIS do corte (o ano corrente incompleto) recebem, congelado, o fator do
         ULTIMO ano da amostra na mesma posicao sazonal (mesmo trimestre/mes) -- extrapola
         sem deixar o ano incompleto influenciar o fit.

    Divergencia deliberada de analytics/credit/transforms.py (que congela a MEDIA do fator
    por mes sobre toda a amostra, achatando a sazonalidade evolutiva): aqui so a
    extrapolacao e congelada, o historico mantem o fit local do STL. Tambem menos
    conservador no corte -- credit/ so incorpora um ano quando o janeiro seguinte chega,
    enquanto aqui um ano entra na amostra assim que fecha (o que o usuario descreveu
    literalmente: "when we complete the 2026... we re-run incorporating 2026").

    `min_obs` default = 2 x period (8 trimestres / 24 meses), medido sobre a amostra ate o
    corte. Retorna lista alinhada a `dates`, com None onde o dado bruto e None/NaN ou a
    serie e curta/instavel demais para o STL.
    """
    from statsmodels.tsa.seasonal import STL

    if min_obs is None:
        min_obs = 2 * period

    vals = pd.Series(values, dtype="float64")
    if vals.count() < min_obs:
        return [None] * len(dates)

    cutoff_year = seasonal_cutoff_year(dates, values, period)
    if cutoff_year is None:
        return [None] * len(dates)

    in_mask = np.array([d[:4] <= cutoff_year for d in dates])
    vals_in = vals[in_mask].interpolate(limit_direction="both")
    if len(vals_in) < min_obs or vals_in.isna().any():
        return [None] * len(dates)

    try:
        fit = STL(vals_in.to_numpy(), period=period, robust=True).fit()
    except Exception:
        return [None] * len(dates)

    pos = _season_position(dates, period)
    pos_in = pos[in_mask]

    # Fator congelado para o ano corrente incompleto = fator do ULTIMO ano da amostra na
    # mesma posicao sazonal. Varre de tras para frente e fica com a primeira ocorrencia de
    # cada posicao -- assim nao depende de a amostra terminar exatamente em dezembro/T4.
    carry: dict[int, float] = {}
    for i in range(len(pos_in) - 1, -1, -1):
        p = int(pos_in[i])
        if p not in carry:
            carry[p] = float(fit.seasonal[i])

    seasonal = np.empty(len(dates), dtype="float64")
    j = 0
    for i in range(len(dates)):
        if in_mask[i]:
            seasonal[i] = fit.seasonal[j]
            j += 1
        else:
            seasonal[i] = carry.get(int(pos[i]), 0.0)

    sa = vals.to_numpy() - seasonal
    return [None if np.isnan(v) else float(v) for v in sa]


def rolling_sum(values: list, window: int) -> list:
    """Acumulado movel (soma) sobre as ultimas `window` observacoes (trailing -- a
    janela termina no proprio ponto t, olhando para tras). None enquanto a janela nao
    estiver completa ou algum ponto dela for None/NaN."""
    vals = pd.Series(values, dtype="float64")
    ttm = vals.rolling(window=window, min_periods=window).sum()
    return [None if pd.isna(v) else float(v) for v in ttm]


def pct_change(values: list, periods: int) -> list:
    """Variacao percentual entre `values[i]` e `values[i-periods]`, em %. None onde
    nao ha par valido.

    None TAMBEM quando a base e exatamente zero -- ver a docstring gemea em
    analytics/credit/transforms.py's pct_change() para o porque (o guard que
    analytics/metric_layers.md registrava como pendente, "Zero base -> Infinity";
    implementado 2026-08 nas duas copias da funcao ao mesmo tempo).
    """
    vals = pd.Series(values, dtype="float64")
    pct = vals.pct_change(periods=periods, fill_method=None) * 100
    return [None if not np.isfinite(v) else float(v) for v in pct]


def pp_diff(values: list, periods: int) -> list:
    """Diferenca simples (pontos percentuais) entre `values[i]` e `values[i-periods]`
    -- para series ja expressas em % (ex.: %PIB, taxas), onde uma variacao percentual
    (pct_change, "crescimento de um crescimento") nao faz sentido; usa-se a diferenca
    direta em p.p., mesma convencao do IEG e do impulso fiscal via resultado primario
    (ver compute_variants_quarterly_step() e generate_report.py's
    _load_fiscal_impulse_nfsp()). None onde nao ha par valido."""
    vals = pd.Series(values, dtype="float64")
    diff = vals.diff(periods=periods)
    return [None if pd.isna(v) else float(v) for v in diff]


def quarterly_step_level(dates: list[str], values: list) -> list:
    """Acumulado do TRIMESTRE CALENDARIO (nao movel -- Jan+Fev+Mar, Abr+Mai+Jun etc.),
    repetido ("degrau") nos 3 meses daquele trimestre -- alinhado ao mesmo array
    `dates` (mensal) de entrada, ao contrario de rolling_sum() (que e uma janela movel
    recalculada a cada mes). None em todo mes cujo trimestre nao tenha os 3 meses
    presentes (sem estimativa de trimestre incompleto). Usado pelo toggle "Trimestral"
    da RTN (ver compute_variants_quarterly_step()) -- torna a RTN (mensal) comparavel,
    trimestre a trimestre, com o valor NATIVO trimestral que a GFSM ja usa (a mesma
    janela de 3 meses corridos, sem sobreposicao), ao contrario do "Acumulado" (12m
    movel) ja existente.
    """
    idx = pd.to_datetime(dates)
    s = pd.Series(values, dtype="float64", index=idx)
    q_sum = s.resample("QS").sum(min_count=3)
    q_key = idx.to_period("Q").to_timestamp(how="start")
    mapped = q_sum.reindex(q_key)
    return [None if pd.isna(v) else float(v) for v in mapped.to_numpy()]


def _collapse_to_quarters(dates: list[str], step_values: list) -> tuple[list[str], list]:
    """Degrau mensal (ver quarterly_step_level()) -> (datas de inicio de trimestre, UMA
    observacao por trimestre). Espelha o collapseToQuarterStart() do lado JS."""
    qd, qv = [], []
    for d, v in zip(dates, step_values):
        if int(d[5:7]) in (1, 4, 7, 10):
            qd.append(d)
            qv.append(v)
    return qd, qv


def _quarter_start_of(date: str) -> str:
    mes = ((int(date[5:7]) - 1) // 3) * 3 + 1
    return f"{date[:4]}-{mes:02d}-01"


def quarterly_step_qoq_sa(dates: list[str], step_values: list) -> list:
    """T/T DESSAZONALIZADO de um degrau de trimestre calendario, alinhado de volta a
    grade mensal de `dates` (2026-08 -- fecha a lacuna que analytics/metric_layers.md
    registrava em "SA on an already-aggregated level": uma comparacao marginal sobre um
    agregado de calendario tem que ser ajustada no periodo DO AGREGADO).

    O STL roda `period=4` na serie TRIMESTRAL colapsada (1 observacao por trimestre) --
    NAO no degrau mensal. Rodar period=4 sobre o degrau trataria 4 observacoes
    consecutivas como um ciclo, e essas 4 observacoes sao 4 MESES (dos quais 3 sao o
    mesmo trimestre repetido), entao o STL estimaria a sazonalidade de um ciclo que nao
    existe. Depois do pct_change(sa, 1) trimestre-contra-trimestre, o resultado e
    re-expandido nos 3 meses de cada trimestre, para o collapseToQuarterStart() do JS
    reduzir de novo na exibicao.

    So o T/T e ajustado. Y/Y continua NSA por construcao (ver metric_layers.md, "(iii)
    Y/Y is NSA; marginal comparisons are SA").
    """
    qd, qv = _collapse_to_quarters(dates, step_values)
    sa = stl_seasonal_adjust(qd, qv, period=4)
    por_trimestre = dict(zip(qd, pct_change(sa, 1)))
    return [por_trimestre.get(_quarter_start_of(d)) for d in dates]


def ytd_sum(dates: list[str], values: list) -> list:
    """Acumulado no ano CIVIL corrente ("acum. no ano"), zerando em cada janeiro --
    ao contrario de rolling_sum() (janela movel de 12 meses, que atravessa a virada
    de ano) e de quarterly_step_level() (degrau trimestral). Em janeiro o acumulado
    e o proprio mes; em dezembro e o ano fechado.

    None se ALGUM mes do ano corrente ate `t` for None -- um acumulado no ano com um
    buraco no meio nao e o acumulado daquele periodo, e a soma de um subconjunto dele,
    e plotar os dois na mesma linha esconderia isso (mesma logica do min_periods de
    rolling_sum()). Volta a produzir valor no janeiro seguinte, quando o acumulador
    reseta.

    Deliberadamente NAO reusa `analytics.labor_market.transforms.ytd_sum()`, que tem a
    mesma ideia mas semantica numerica errada para uma serie em R$: aquela arredonda o
    acumulado para inteiro (correto para contagem de pessoas do CAGED, perde centavos
    aqui) e trata None como zero (aceitavel num contador de eventos, silenciosamente
    subestima um acumulado fiscal). Assume `dates` ordenado, como todo `_load_*` de
    generate_report.py ja produz.
    """
    out: list = []
    ano = None
    acc = 0.0
    furado = False
    for d, v in zip(dates, values):
        if d[:4] != ano:
            ano, acc, furado = d[:4], 0.0, False
        if v is None or (isinstance(v, float) and np.isnan(v)):
            furado = True
        else:
            acc += float(v)
        out.append(None if furado else acc)
    return out


def ytd_map(dates: list[str], values: list) -> dict:
    """Como ytd_sum(), mas {date: acumulado no ano} -- para reindexar contra um SEGUNDO
    array de datas, do mesmo jeito que quarterly_step_map() faz para o degrau trimestral.
    Usado para o PIB acumulado no ano (denominador do %PIB no Nivel "Acum. no ano", ver
    compute_variants_ytd())."""
    return dict(zip(dates, ytd_sum(dates, values)))


def compute_variants_ytd(
    dates: list[str], nominal_values: list, price_index: dict | None = None,
    ref_date: str | None = None, gdp_ytd: dict | None = None,
) -> dict:
    """Nivel(Acum. no ano)/Y-Y para uma serie MENSAL -- a quarta modelagem de Nivel,
    usada hoje so pela aba Investimento (2026-08, a pedido do usuario: "create 12m,
    Quarter and Year acumulation metrics"). Nivel = acumulado no ano civil (ver
    ytd_sum()). Y/Y = defasagem de 12 meses, que compara o acumulado Jan..M de um ano
    contra Jan..M do ano anterior -- a leitura padrao de "acumulado no ano" e a unica
    comparacao que faz sentido nesta janela.

    SEM M/M e SEM T/T, deliberadamente: as duas atravessariam o reset de janeiro. O
    acumulado de janeiro contra o de dezembro anterior nao e uma variacao mensal, e a
    queda artificial de um ano fechado para um mes; idem para a defasagem de 3 meses em
    janeiro/fevereiro/marco. O lado JS desabilita as duas quando este Nivel esta
    selecionado (ver `metricAvailability` em report.html), em vez de servir um numero
    que parece uma taxa de crescimento e nao e.

    "% do PIB" (se `gdp_ytd` for passado, ja acumulado no ano por ytd_map()) e
    YTD/YTD -- acumulado no ano da serie sobre acumulado no ano do PIB, os dois lados
    na mesma janela, mesma coerencia que compute_pct_pib_ttm() tem em TTM/TTM. Deflaciona
    ANTES de acumular (cada mes a precos de `ref_date`, depois soma), mesma ordem de
    _ttm_variants().
    """
    def _variants(values):
        base = ytd_sum(dates, values)
        return {
            "level": {"dates": dates, "values": base},
            "yoy":   {"dates": dates, "values": pct_change(base, 12)},
        }

    out = {"nominal": _variants(nominal_values)}
    if price_index is not None:
        out["real"] = _variants(deflate_series(dates, nominal_values, price_index, ref_date))
    if gdp_ytd is not None:
        ytd_vals = ytd_sum(dates, nominal_values)
        out["pctpib"] = {"level": {
            "dates": dates,
            "values": compute_pct_pib_same_period(dates, ytd_vals, gdp_ytd),
        }}
    return out


def build_price_index(dates: list[str], monthly_pct: list) -> dict:
    """Indice de precos encadeado a partir da variacao mensal (%) do IPCA (base 100 no
    primeiro mes da serie de entrada). Generico o bastante para alimentar tanto a serie
    trimestral da GFSM (cujas datas -- Jan/Abr/Jul/Out -- sempre coincidem com um mes
    real desta serie) quanto a mensal da RTN.
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


def compute_pct_pib_same_period(dates: list[str], nominal_values: list, gdp_map: dict) -> list:
    """Razao percentual do valor do PROPRIO periodo (SEM acumular) sobre o PIB do MESMO
    periodo (`gdp_map`: date -> PIB daquele periodo, tambem SEM acumular) -- ao
    contrario de compute_pct_pib_ttm() (sempre TTM/TTM). Usada pelos niveis Mensal
    (RTN, `gdp_map` = atv_pib_mensal.pib_mensal, SGS 4380) e Trimestral (RTN via
    quarterly_step_map() abaixo; GFSM via atv_pib_valores_correntes.pib_pm bruto, sem
    o rolling(4) que _load_pib_4t() aplica). None onde o valor ou o PIB daquela data
    nao existem.
    """
    out = []
    for d, v in zip(dates, nominal_values):
        gdp = gdp_map.get(d)
        if v is None or gdp is None:
            out.append(None)
        else:
            out.append(v / gdp * 100)
    return out


def quarterly_step_map(dates: list[str], values: list) -> dict:
    """Como quarterly_step_level() (abaixo), mas retorna um dict {date: valor} em vez
    de uma lista alinhada a `dates` -- para reindexar contra um SEGUNDO array de datas
    (ex.: o PIB mensal, atv_pib_mensal.pib_mensal, usado como denominador do %PIB
    Trimestral da RTN via compute_pct_pib_same_period(), cujas datas nao coincidem
    necessariamente com as da serie fiscal em fisc_rtn)."""
    step = quarterly_step_level(dates, values)
    return dict(zip(dates, step))


def compute_pct_pib_ttm(dates: list[str], nominal_values: list, gdp_ttm: dict, window: int = 4) -> list:
    """Acumulado em `window` periodos (TTM, default 4 trimestres) do proprio
    `nominal_values`, dividido pelo TTM do PIB (`gdp_ttm`, ja pre-computado em
    generate_report.py -- pib_4t para a GFSM, atv_pib_mensal.pib_acum_12m para a RTN
    com window=12). None onde a janela TTM ainda nao esta completa ou o PIB naquela
    data nao existe.
    """
    ttm = rolling_sum(nominal_values, window)
    out = []
    for d, v in zip(dates, ttm):
        gdp = gdp_ttm.get(d)
        if v is None or gdp is None:
            out.append(None)
        else:
            out.append(v / gdp * 100)
    return out


def compute_variants(
    dates: list[str], nominal_values: list, price_index: dict | None, ref_date: str | None,
    gdp_same_period: dict | None = None,
) -> dict:
    """Nivel(bruto)/Y-Y/T-T para uma serie trimestral (GFSM), em termos nominais e (se
    `price_index` for passado) reais, mais opcionalmente "% do PIB" (mesmo periodo,
    SEM acumular nenhum dos dois lados -- ver docstring do modulo). Retorna:

        {"nominal": {"level": {...}, "yoy": {...}, "qoq_sa": {...}},
         "real":    {...},                                        # so se price_index
         "pctpib":  {"level": {...}}}                              # so se gdp_same_period

    Cada variante e {"dates": dates, "values": [...]}, sempre do mesmo tamanho que
    `dates` (None onde nao aplicavel). Ver compute_variants_ttm() para a modelagem
    "Acumulado" (TTM) do mesmo Nivel/Y-Y/T-T, oferecida lado a lado via toggle no
    relatorio, nao em substituicao a esta -- essa outra modelagem usa
    compute_pct_pib_ttm() (TTM/TTM), nao esta funcao.
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
    if gdp_same_period is not None:
        out["pctpib"] = {"level": {"dates": dates, "values": compute_pct_pib_same_period(dates, nominal_values, gdp_same_period)}}
    return out


def compute_variants_quarterly_step(
    dates: list[str], nominal_values: list, price_index: dict | None = None, ref_date: str | None = None,
    seasonal: bool = False,
) -> dict:
    """Nivel(Trimestral)/Y-Y/T-T para uma serie MENSAL (RTN) reamostrada em trimestre
    calendario NAO movel (2026-08, adicao explicita do usuario -- terceira opcao do
    toggle Bruto/Trimestral/Acumulado, ao lado das outras duas, nao em substituicao).
    Nivel = soma do trimestre calendario corrente, repetida ("degrau") nos 3 meses
    desse trimestre (ver quarterly_step_level()) -- ao contrario de "Acumulado"
    (janela movel de 12 meses), este e o mesmo tipo de corte NAO sobreposto que a
    GFSM ja usa nativamente, o que torna as duas tabelas comparaveis trimestre a
    trimestre (ver Apendice, "GFSM vs. RTN"). Y/Y (defasagem 12 meses = 4 trimestres)
    compara contra o mesmo trimestre um ano antes. T/T ("qoq_sa" -- nome de chave
    mantido por compatibilidade com o lado JS, ainda que nao seja um STL aqui, ja que
    o degrau em si ja e uma serie SEM variacao dentro do trimestre) compara contra o
    trimestre imediatamente anterior (defasagem 3 meses). Sem "M/M" -- um mes contra
    o mes anterior dentro do mesmo degrau trimestral e sempre 0% (ou um salto
    artificial na virada de trimestre), entao essa variante nao e oferecida aqui (o
    lado JS cai para T/T automaticamente se M/M estiver selecionado ao trocar para
    este toggle). "% do PIB" nao e recalculada aqui -- rtn_tab.py reusa o mesmo dict
    ja computado para "Bruto" (ver docstring do modulo, "% do PIB" e sempre
    TTM/TTM, independente do toggle Bruto/Trimestral/Acumulado).

    `seasonal` (2026-08, default False): quando True, o T/T passa a ser dessazonalizado
    por quarterly_step_qoq_sa() (STL period=4 sobre a serie trimestral colapsada), que e
    o que analytics/metric_layers.md pede em "(iii) SA on an already-aggregated level" --
    a execucao orcamentaria federal e sistematicamente concentrada no 4o trimestre, entao
    o T/T cru le T1-contra-T4 como colapso todo ano. **Default False de proposito**: a
    aba Investimento liga (escolha explicita do usuario, 2026-08), a RTN NAO, para nao
    mexer nos numeros de uma aba que ninguem pediu para mudar. Com False, `qoq_sa`
    continua sendo um pct_change cru e o sufixo `_sa` segue sendo so nome de chave para o
    lado JS, nao uma afirmacao sobre o dado.
    """
    def _variants(values):
        step = quarterly_step_level(dates, values)
        qoq = quarterly_step_qoq_sa(dates, step) if seasonal else pct_change(step, 3)
        return {
            "level":  {"dates": dates, "values": step},
            "yoy":    {"dates": dates, "values": pct_change(step, 12)},
            "qoq_sa": {"dates": dates, "values": qoq},
        }

    out = {"nominal": _variants(nominal_values)}
    if price_index is not None:
        real_values = deflate_series(dates, nominal_values, price_index, ref_date)
        out["real"] = _variants(real_values)
    return out


def _ttm_variants(dates: list[str], values: list, window: int, lags: dict) -> dict:
    """Nivel = acumulado em `window` periodos; cada entrada de `lags` (nome ->
    defasagem em periodos) vira uma variante de crescimento pct_change() sobre esse
    acumulado -- ver compute_variants_ttm()/compute_variants_monthly_ttm()."""
    base = rolling_sum(values, window)
    out = {"level": {"dates": dates, "values": base}}
    for name, lag in lags.items():
        out[name] = {"dates": dates, "values": pct_change(base, lag)}
    return out


def compute_variants_ttm(
    dates: list[str], nominal_values: list, price_index: dict | None, ref_date: str | None,
    gdp_ttm: dict | None = None,
) -> dict:
    """Nivel(Acumulado 4T)/Y-Y/T-T para uma serie trimestral (GFSM) -- a modelagem
    "Acumulado" oferecida ao lado da bruta (compute_variants(), acima) via um toggle no
    relatorio (2026-08, adicao explicita do usuario -- nao substitui a bruta). Mesmo
    formato de retorno de compute_variants(). Nivel = acumulado nos ultimos 4
    trimestres (ver docstring do modulo). Y/Y = variacao do acumulado terminado no
    trimestre t contra o acumulado terminado 4 trimestres antes (defasagem 4). T/T
    ("qoq_sa" -- nome de chave mantido por compatibilidade com o lado JS, ainda que nao
    seja um STL aqui) = variacao do acumulado contra o acumulado do trimestre
    imediatamente anterior (defasagem 1). "% do PIB" e identica a de compute_variants()
    (mesma formula TTM/TTM, independente do toggle Bruto/Acumulado).
    """
    window = 4
    lags = {"yoy": 4, "qoq_sa": 1}

    out = {"nominal": _ttm_variants(dates, nominal_values, window, lags)}
    if price_index is not None:
        real_values = deflate_series(dates, nominal_values, price_index, ref_date)
        out["real"] = _ttm_variants(dates, real_values, window, lags)
    if gdp_ttm is not None:
        out["pctpib"] = {"level": {"dates": dates, "values": compute_pct_pib_ttm(dates, nominal_values, gdp_ttm, window=window)}}
    return out


def compute_variants_monthly_ttm(
    dates: list[str], nominal_values: list, price_index: dict | None, ref_date: str | None,
    gdp_ttm: dict | None = None,
) -> dict:
    """Nivel(Acumulado 12m)/Y-Y/M-M/T-T para uma serie mensal (RTN) -- a modelagem
    "Acumulado" oferecida ao lado da bruta (analytics.credit.transforms.compute_variants(),
    reusada por rtn_tab.py para o Bruto) via o mesmo toggle Bruto/Acumulado da GFSM.
    Nivel = acumulado nos ultimos 12 meses. Y/Y = variacao do acumulado terminado no
    mes t contra o acumulado terminado 12 meses antes (defasagem 12). M/M ("mom_sa") =
    variacao contra o acumulado do mes imediatamente anterior (defasagem 1). T/T
    ("qoq_sa") = variacao contra o acumulado de 3 meses antes (defasagem 3, mesma
    convencao "3M/3M rolante" ja usada em analytics/credit/). Nomes de chave mantidos
    por compatibilidade com o lado JS, ainda que nao sejam mais um STL aqui.
    """
    window = 12
    lags = {"yoy": 12, "mom_sa": 1, "qoq_sa": 3}

    out = {"nominal": _ttm_variants(dates, nominal_values, window, lags)}
    if price_index is not None:
        real_values = deflate_series(dates, nominal_values, price_index, ref_date)
        out["real"] = _ttm_variants(dates, real_values, window, lags)
    if gdp_ttm is not None:
        out["pctpib"] = {"level": {"dates": dates, "values": compute_pct_pib_ttm(dates, nominal_values, gdp_ttm, window=window)}}
    return out
