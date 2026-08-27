"""
Gerador do Panorama de Inflacao em HTML.

Le a decomposicao do IPCA e IPCA-15 por subitem de macro_brasil.inflc_decomposicao
(join com macro_brasil.inflc_dim), mescla com os agregados BCB/SGS (CSV) e
injeta no template report.html, gerando um arquivo HTML autocontido.

Uso:
    uv run python analytics/brasil/inflation/generate_report.py
    uv run python -c "from analytics.brasil.inflation.generate_report import run; run()"
"""

from datetime import datetime
from pathlib import Path

import pandas as pd

from analytics.brasil.inflation import inercia as _inercia
from analytics.brasil.inflation.fetch_bcb import _apply_stl_ma3
from analytics.report_structure.builder import render_report
from connectors.mysql import MySQLDataRequester

_HERE = Path(__file__).parent
_TEMPLATE = _HERE / "report.html"
_DATA = _HERE / "data"
_BCB_CSV = _DATA / "ipca_bcb_series.csv"

_DATABASE = "macro_brasil"

# Núcleos por exclusão computáveis em casa para o IPCA-15: BCB só publica
# núcleos (EX-0/EX-01/.../EXFE) para o IPCA cheio (ver Gotchas em
# analytics/brasil/inflation/CLAUDE.md), mas o vetor oficial de pertencimento
# (inflc_dim.nucleo_*, derivado da NT-57) cobre qualquer subitem do IPCA-15
# também, já que todo subitem do IPCA-15 existe no IPCA. P55 (subitem-level,
# ver _compute_p55) e Difusão (ver _compute_difusao) tambem sao computaveis
# em casa a partir dos mesmos dados de subitem, sem precisar deste dict de
# flags. Medias Aparadas (com e sem suavizacao) e Dupla Ponderacao operam no
# nivel de ITEM, nao subitem (ver NT-57 e CLAUDE.md Gotchas) -- vem de
# inflc_decomposicao_item via _compute_ma/_compute_ms/_compute_dp, nao deste
# dict.
_NUCLEO_FLAGS_15 = {
    "nucleo_ex0":              "IPCA15_nucleo_EX0",
    "nucleo_ex01":             "IPCA15_nucleo_EX01",
    "nucleo_ex02":             "IPCA15_nucleo_EX02",
    "nucleo_ex03":             "IPCA15_nucleo_EX03",
    "nucleo_ex03_servicos":    "IPCA15_nucleo_EX03_servicos",
    "nucleo_ex03_industriais": "IPCA15_nucleo_EX03_industriais",
    "nucleo_exfe":             "IPCA15_nucleo_EXFE",
}


def _load_decomposicao() -> pd.DataFrame:
    fatos = MySQLDataRequester(_DATABASE, "inflc_decomposicao")
    fatos.connect()
    df = fatos.request_data()
    fatos.close_connection()

    dimensao = MySQLDataRequester(_DATABASE, "inflc_dim")
    dimensao.connect()
    dim = dimensao.request_data()
    dimensao.close_connection()

    df["date"] = pd.to_datetime(df["date"])
    df["var_mensal"] = pd.to_numeric(df["var_mensal"]).round(5)
    # pesos/contribuicao rounded looser (5) than their smallest real values (~3e-6 /
    # ~6e-8) collapse low-weight subitems (e.g. "Fisioterapeuta", peixes exoticos) to
    # 0.0 -- since the front-end weighted average divides by sum(pesos), a zeroed
    # weight makes every month null and the Y/Y drilldown chart renders empty.
    for col in ["pesos", "contribuicao"]:
        df[col] = pd.to_numeric(df[col]).round(8)

    merged = df.merge(dim, on="subitem_codigo", how="left")
    # Reconstroi o mesmo formato "<codigo> <nome>" de sempre (ex.: "1101002 Arroz")
    # a partir do codigo (chave, estavel) + nome canonico de inflc_dim (sempre a
    # grafia mais recente do IBGE) -- report.html so consome "subitem" como string
    # opaca de exibicao/agrupamento, nunca a interpreta, entao nao precisa mudar.
    merged["subitem"] = (merged["subitem_codigo"] + " " + merged["nome"].fillna("")).str.strip()
    return merged


def _load_decomposicao_item() -> pd.DataFrame:
    """inflc_decomposicao_item (item/4-digit level) -- inputs for MA/MS/DP,
    which NT-57 defines at that granularity, not subitem (see CLAUDE.md
    Gotchas). Kept separate from _load_decomposicao(): no inflc_dim join
    needed (MA/MS/DP don't use Grupo/Subgrupo/núcleo membership at all).
    """
    fatos = MySQLDataRequester(_DATABASE, "inflc_decomposicao_item")
    fatos.connect()
    df = fatos.request_data()
    fatos.close_connection()
    df["date"] = pd.to_datetime(df["date"])
    df["var_mensal"] = pd.to_numeric(df["var_mensal"])
    df["pesos"] = pd.to_numeric(df["pesos"])
    return df


def _to_records(df: pd.DataFrame, indice: str) -> dict:
    sub = df[df["indice"] == indice].copy()
    if sub.empty:
        return {"records": [], "min_date": "", "max_date": ""}

    sub["dt"] = sub["date"].dt.strftime("%Y-%m")
    cols = ["dt", "subitem", "grupo", "subgrupo", "item", "subjacente", "comercializavel",
            "nucleo_ex0", "nucleo_ex01", "nucleo_ex02", "nucleo_ex03",
            "nucleo_ex03_servicos", "nucleo_ex03_industriais", "nucleo_exfe",
            "var_mensal", "pesos", "contribuicao"]
    out = sub[cols].astype(object).where(pd.notna(sub[cols]), None)
    dates = sorted(sub["dt"].dropna().unique().tolist())
    return {
        "records":  out.to_dict(orient="records"),
        "min_date": dates[0] if dates else "",
        "max_date": dates[-1] if dates else "",
    }


def _ibge_nomes(decomposicao: pd.DataFrame) -> dict:
    """Prefixo do codigo IBGE -> nome, para os 3 niveis acima do subitem.

    Deliberadamente NAO vai como coluna em cada registro: o codigo de 7
    digitos que report.html ja carrega em `subitem` ("1101002 Arroz") ja
    contem o parentesco por prefixo, entao o front-end recorta 1/2/4
    digitos e consulta este mapa. Sao ~80 entradas contra ~262 mil
    registros — a alternativa (3 strings por registro) engordaria um
    arquivo que ja tem ~99 MB em troca de nenhuma informacao nova.
    """
    dim = decomposicao.drop_duplicates("subitem_codigo")
    nomes: dict[str, str] = {}
    for corte, col in ((1, "ibge_grupo"), (2, "ibge_subgrupo"), (4, "ibge_item")):
        if col not in dim.columns:
            continue
        for codigo, nome in zip(dim["subitem_codigo"], dim[col]):
            if nome is None or pd.isna(nome):
                continue
            nomes.setdefault(str(codigo)[:corte], str(nome))
    return nomes


def _series_dict(df: pd.DataFrame) -> dict:
    result = {}
    for name, grp in df.groupby("name"):
        grp = grp.sort_values("dt")
        result[name] = {
            "dates":  grp["dt"].tolist(),
            "values": [None if pd.isna(v) else round(float(v), 5) for v in grp["value"]],
        }
    return result


def _load_bcb() -> dict:
    if not _BCB_CSV.exists():
        return {}
    df = pd.read_csv(_BCB_CSV, encoding="utf-8-sig")
    return _series_dict(df)


# Grupo/Subgrupo membership -> in-house IPCA-15 series name, same pattern as
# _NUCLEO_FLAGS_15 but keyed off inflc_dim's grupo/subgrupo columns instead
# of a nucleo_* flag. Naming mirrors the full-IPCA BCB series in
# ipca_bcb_series.csv (IPCA_livres/administrado/alimentacao/servicos/
# industriais) minus the "IPCA" prefix swapped for "IPCA15". No
# Comercializáveis/Não Comercializáveis equivalent: that's a real NT-57 axis,
# but inflc_dim never derived subitem-level flags for it (only
# grupo/subgrupo/item/subjacente/núcleo) -- out of scope here, see CLAUDE.md.
_GRUPO_FLAGS_15 = {
    "IPCA15_livres":       ("grupo", "Livres"),
    "IPCA15_administrado": ("grupo", "Monitorados"),
    "IPCA15_alimentacao":  ("subgrupo", "Alimentos"),
    "IPCA15_servicos":     ("subgrupo", "Serviços"),
    "IPCA15_industriais":  ("subgrupo", "Bens Industriais"),
}


def _weighted_avg_by_group(sub: pd.DataFrame, groups: dict[str, pd.Series]) -> pd.DataFrame:
    """Shared basis for _compute_ipca15_nucleos()/_compute_ipca15_grupos():
    for each (name -> boolean row mask) in `groups`, monthly value =
    sum(contribuicao)/sum(pesos) among the flagged rows for that month.

    contribuicao and var_mensal are both already on a "percent number" scale
    (var_mensal=-1.49 means -1.49%) — sum(contribuicao)/sum(pesos) lands on
    that same scale directly, no further *100. An earlier version of this
    function had that extra *100 (copied from the same bug in report.html's
    computeMonthlyFromRecords, found 2026-07 by actually executing the JS
    against real data) — values were 100x too large.

    Deliberately NOT rounded to 2 decimals here (unlike the analogous
    subgrupo/grupo computation in report.html's computeMonthlyFromRecords):
    this monthly value feeds both compute3mSAAR (STL) and, via D.bcb ->
    report.html's computeYoY, a 12-month chain-compounding — rounding each
    monthly value before chaining compounds that rounding into the final
    figure. Verified 2026-07 against an external BCB reference table for the
    equivalent grupo/subgrupo case: rounding-then-chaining was off by up to
    0.02pp on the 12m figure versus chaining unrounded and rounding only the
    final result (which matched exactly). Display-time rounding to 2dp
    already happens in report.html wherever these values are shown.
    """
    frames = []
    for name, mask in groups.items():
        flagged = sub[mask]
        grp = flagged.groupby("dt").agg(c=("contribuicao", "sum"), p=("pesos", "sum"))
        grp = grp[grp["p"] > 0]
        if grp.empty:
            continue
        value = grp["c"] / grp["p"]
        frames.append(pd.DataFrame({"name": name, "dt": value.index, "value": value.values}))
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=["name", "dt", "value"])


def _compute_ipca15_nucleos(decomposicao: pd.DataFrame) -> pd.DataFrame:
    """Monthly variation of each in-house IPCA-15 núcleo por exclusão -- see
    _weighted_avg_by_group() for the shared computation/rounding rationale."""
    sub = decomposicao[decomposicao["indice"] == "IPCA15"].copy()
    if sub.empty:
        return pd.DataFrame(columns=["name", "dt", "value"])
    sub["dt"] = sub["date"].dt.strftime("%Y-%m")
    groups = {name: sub[flag_col] == 1 for flag_col, name in _NUCLEO_FLAGS_15.items()}
    return _weighted_avg_by_group(sub, groups)


def _compute_ipca15_grupos(decomposicao: pd.DataFrame) -> pd.DataFrame:
    """Monthly variation of each in-house IPCA-15 grupo/subgrupo component
    (Livres/Monitorados/Alimentação/Serviços/Industriais) -- feeds the
    "Componentes — 3M SAAR" chart and the Heatmap's "Grupos" section for
    IPCA-15, neither of which had an IPCA-15 equivalent before 2026-07 (see
    CLAUDE.md Gotchas: report.html's renderCompSAAR/renderHeatmap were
    hardcoded to full-IPCA-only series). Same computation as
    _compute_ipca15_nucleos(), just grouped by grupo/subgrupo membership
    instead of núcleo flags -- see _weighted_avg_by_group(). Not separately
    re-validated: this is the exact sum(contribuicao)/sum(pesos)-by-month
    formula already validated against an external BCB reference table for
    grupo/subgrupo 12m figures earlier in the same work (see Gotchas)."""
    sub = decomposicao[decomposicao["indice"] == "IPCA15"].copy()
    if sub.empty:
        return pd.DataFrame(columns=["name", "dt", "value"])
    sub["dt"] = sub["date"].dt.strftime("%Y-%m")
    groups = {
        name: sub[col] == val
        for name, (col, val) in _GRUPO_FLAGS_15.items()
    }
    return _weighted_avg_by_group(sub, groups)


def _compute_p55(decomposicao: pd.DataFrame, indice: str) -> pd.DataFrame:
    """Weighted 55th-percentile subitem variation (NT-57 §2.5) for any índice.

    Per month: sort subitens by var_mensal ascending, walk the cumulative
    weight (renormalized to that month's own total, in case of any coverage
    gap), and take the var_mensal of the first subitem whose cumulative
    weight reaches 55% -- P55 is that single subitem's own value, not an
    average (unlike MA/MS/DP, which NT-57 defines at the item, i.e. 4-digit,
    level -- P55 is the one core BCB defines at subitem/7-digit granularity,
    see CLAUDE.md Gotchas).

    Validated 2026-07 against the official BCB series (IPCA_nucleo_P55) for
    full IPCA: exact match on all 318 months with both series available.
    Used in production only for IPCA15 (BCB doesn't publish a P55 for
    IPCA-15); the function stays index-agnostic so it can be validated
    against IPCA's own official series before being trusted for IPCA-15,
    which has no official reference to check against.
    """
    sub = decomposicao[decomposicao["indice"] == indice].dropna(subset=["var_mensal", "pesos"]).copy()
    if sub.empty:
        return pd.DataFrame(columns=["dt", "value"])
    sub["dt"] = sub["date"].dt.strftime("%Y-%m")

    def _p55(g: pd.DataFrame) -> float:
        g = g.sort_values("var_mensal")
        cum = g["pesos"].cumsum()
        idx = (cum >= 0.55 * g["pesos"].sum()).idxmax()
        return g.loc[idx, "var_mensal"]

    value = sub.groupby("dt").apply(_p55, include_groups=False)
    return pd.DataFrame({"dt": value.index, "value": value.values})


def _compute_difusao(decomposicao: pd.DataFrame, indice: str) -> pd.DataFrame:
    """Percentage of researched subitens with positive var_mensal (NT-57 §2.6), for any índice.

    Unweighted -- pesos play no role here, only the sign of var_mensal.
    Subitens not researched in a given month simply have no row in
    inflc_decomposicao for that month, matching NT-57's own "apenas os
    subitens efetivamente pesquisados" rule with no extra filtering needed.

    Validated 2026-07 against the official BCB series (IPCA_indice_difusao)
    for full IPCA: matches to within 0.005pp on all 318 months with both
    series available -- that gap is BCB's own 2-decimal display rounding
    (e.g. 59.375 -> 59.38), not a methodology difference.

    Deliberately NOT run through _apply_stl_ma3/computeYoY like the
    exclusion núcleos and P55: difusão isn't a price-change series, so
    chain-compounding it 12 months makes no sense. NT-57's own comparison
    charts (footnote 23) use a 12-month ARITHMETIC moving average instead --
    report.html's existing movingAvg() already does this for the
    Difusão-por-Categoria chart's 3M/6M lines; this series is meant for that
    same display path, not the SAAR/YoY one.
    """
    sub = decomposicao[decomposicao["indice"] == indice].dropna(subset=["var_mensal"]).copy()
    if sub.empty:
        return pd.DataFrame(columns=["dt", "value"])
    sub["dt"] = sub["date"].dt.strftime("%Y-%m")
    value = sub.groupby("dt")["var_mensal"].apply(lambda s: (s > 0).mean() * 100)
    return pd.DataFrame({"dt": value.index, "value": value.values})


def _trim_20_80(g: pd.DataFrame, value_col: str) -> float | None:
    """Shared MA/MS trimming step (NT-57 §2.3, steps i-v): sort ascending by
    value_col, drop items whose cumulative weight is entirely below 20% or
    entirely above 80%, correct the two boundary items' weights to their
    exact overlap with [20%, 80%], then take the weighted average of what's
    left. Used identically by MA (value_col='var_mensal') and MS
    (value_col='var_ms', the smoothed variation) -- MS's only difference
    from MA is which column gets trimmed, not the trimming logic itself.
    """
    g = g.sort_values(value_col).reset_index(drop=True)
    total = g["pesos"].sum()
    cum = g["pesos"].cumsum()
    prev = cum.shift(1).fillna(0.0)
    lo, hi = 0.20 * total, 0.80 * total
    excluded = (cum <= lo) | (prev >= hi)
    kept = g[~excluded].copy()
    if kept.empty:
        return None
    kept_cum, kept_prev = cum[~excluded], prev[~excluded]
    adj = kept["pesos"].copy()
    first_idx, last_idx = kept.index[0], kept.index[-1]
    adj.loc[first_idx] = kept_cum.iloc[0] - lo
    adj.loc[last_idx] = hi - kept_prev.iloc[-1]
    w = adj / adj.sum()
    return float((w * kept[value_col]).sum())


def _compute_ma(item: pd.DataFrame, indice: str) -> pd.DataFrame:
    """Médias Aparadas sem suavização (NT-57 §2.3) at the item level, for any índice.

    No rolling window, no proxy tables needed at vintage transitions --
    every month is self-contained. Validated 2026-07 against the official
    BCB series (IPCA_nucleo_medias_aparadas_sem_suavizacao) using live
    item-level data for the current vintage alone (agregado 7060,
    jan/2020-hoje): exact match to within 0.005pp (BCB's own display
    rounding) on all 78 months checked.
    """
    sub = item[item["indice"] == indice].dropna(subset=["var_mensal", "pesos"]).copy()
    if sub.empty:
        return pd.DataFrame(columns=["dt", "value"])
    sub["dt"] = sub["date"].dt.strftime("%Y-%m")
    value = sub.groupby("dt").apply(lambda g: _trim_20_80(g, "var_mensal"), include_groups=False)
    return pd.DataFrame({"dt": value.index, "value": value.values}).dropna()


# Itens de reajuste infrequente suavizados no núcleo MS (NT-57 Tabela 5).
# A lista varia por vigência (8104 só existe a partir de jul/2006; a
# vigência jan91-jul99 usa códigos diferentes -- 7301/5201 -- fora de
# escopo aqui, ver inflc_decomposicao.py). _compute_ms() usa só os códigos
# desta lista que de fato existem como coluna no pivot de cada índice, o
# que já resolve o caso 8104 automaticamente sem precisar de um if por
# vigência.
_ITENS_SUAVIZADOS = ["2201", "2202", "5101", "5104", "7101", "7202", "8101", "8104", "9101"]


def _compute_ms(item: pd.DataFrame, indice: str) -> pd.DataFrame:
    """Médias Aparadas com suavização (NT-57 §2.4) at the item level, for any índice.

    Same trimming as MA, but first replaces _ITENS_SUAVIZADOS's raw
    var_mensal with their trailing-12-month geometric-mean-annualized
    variation (NT-57 footnote 11). A month is only computable once all
    smoothed items present that month have a full 12-month window --
    matches NT-57's own MS start dates (dez/1991 for full IPCA, 11 months
    after IPCA's jan/1991 start).

    KNOWN GAP: NT-57 defines explicit proxies (Tabelas 6-8) to bridge this
    12-month window across a structural transition when an item's own
    definition changed at the boundary (e.g. "8104.Cursos diversos" vs.
    "curso técnico" in jan/2020). Not implemented -- this function simply
    concatenates each item code's history across vigências, same trade-off
    already accepted for subitem-level retroactive relabeling in
    inflc_dim.py. Bounded to the specific items in Tabelas 6-8, for ~11
    months after each transition; see CLAUDE.md Gotchas for the measured
    size of this gap against BCB's own official series.

    Validated 2026-07 against the official BCB series
    (IPCA_nucleo_medias_aparadas) using live item-level data for the
    current vintage alone (no transition in that window): exact match to
    within 0.005pp on 67/78 months (first 11 months of the vintage have no
    12-month window yet, correctly excluded).
    """
    sub = item[item["indice"] == indice].dropna(subset=["var_mensal", "pesos"]).copy()
    if sub.empty:
        return pd.DataFrame(columns=["dt", "value"])
    sub["dt"] = sub["date"].dt.strftime("%Y-%m")

    pivot = sub.pivot(index="dt", columns="item_codigo", values="var_mensal").sort_index()
    presentes = [c for c in _ITENS_SUAVIZADOS if c in pivot.columns]
    smoothed = pivot[presentes].apply(
        lambda col: 100 * ((1 + col / 100).rolling(12).apply(lambda w: w.prod()) ** (1 / 12) - 1)
    )

    sub["var_ms"] = sub["var_mensal"]
    for codigo in presentes:
        s12 = smoothed[codigo]
        mask = sub["item_codigo"] == codigo
        sub.loc[mask, "var_ms"] = sub.loc[mask, "dt"].map(s12)

    def _ms(g: pd.DataFrame) -> float | None:
        if g["var_ms"].isna().any():
            return None
        return _trim_20_80(g, "var_ms")

    value = sub.groupby("dt").apply(_ms, include_groups=False)
    return pd.DataFrame({"dt": value.index, "value": value.values}).dropna()


def _compute_headline(decomposicao: pd.DataFrame, indice: str) -> pd.Series:
    """Monthly headline variation reconstructed from subitem data (sum(contribuicao)/sum(pesos)),
    indexed by "YYYY-MM" -- used only as the reference series for núcleo DP's volatility term."""
    sub = decomposicao[decomposicao["indice"] == indice].dropna(subset=["contribuicao", "pesos"]).copy()
    sub["dt"] = sub["date"].dt.strftime("%Y-%m")
    grp = sub.groupby("dt").agg(c=("contribuicao", "sum"), p=("pesos", "sum"))
    return grp["c"] / grp["p"]


def _compute_dp(decomposicao: pd.DataFrame, item: pd.DataFrame, indice: str, headline: pd.Series) -> pd.DataFrame:
    """Dupla ponderação (NT-57 §2.2) at the item level, for any índice.

    Each item's weight is scaled by the inverse of its own 48-month
    rolling (ddof=1, matching NT-57 footnote 9) standard deviation of
    (item variation - `headline`), then renormalized; DP = weighted
    average of that month's item variations using those adjusted weights.

    `headline` is an explicit parameter, not always the same index's own
    headline: NT-57's formula (written only for full IPCA, which is what
    BCB actually publishes) diffs against "a do IPCA cheio" -- full IPCA's
    headline -- but BCB never defines an IPCA-15 version of DP at all. For
    the IPCA-15 production series (see run()), the deliberate choice is to
    diff against IPCA-15's OWN headline instead, for internal consistency
    within an in-house IPCA-15 extension (see CLAUDE.md Gotchas/Pending).

    Same known proxy-table gap as _compute_ms() (NT-57 Tabelas 2-4), over a
    48-month rather than 11-month window.

    Validated 2026-07 against the official BCB series (IPCA_nucleo_DP),
    diffing against full IPCA's own headline, using live item-level data
    for the current vintage alone (no transition in that 48-month window):
    exact match to within 0.005pp on 30/78 months (first 48 months of the
    vintage have no full 48-month window yet, correctly excluded).
    """
    sub = item[item["indice"] == indice].dropna(subset=["var_mensal", "pesos"]).copy()
    if sub.empty:
        return pd.DataFrame(columns=["dt", "value"])
    sub["dt"] = sub["date"].dt.strftime("%Y-%m")

    pivot = sub.pivot(index="dt", columns="item_codigo", values="var_mensal").sort_index()
    diffs = pivot.sub(headline, axis=0)
    vol48 = diffs.rolling(48).std(ddof=1).shift(1)  # sigma_{k,t-1}: window ending the PRIOR month

    def _dp(dt: str) -> float | None:
        if dt not in vol48.index:
            return None
        sigma = vol48.loc[dt].dropna()
        rows = sub[sub["dt"] == dt].set_index("item_codigo")
        common = rows.index.intersection(sigma.index)
        if common.empty:
            return None
        w = rows.loc[common, "pesos"] * (1 / sigma.loc[common])
        w = w / w.sum()
        return float((w * rows.loc[common, "var_mensal"]).sum())

    value = pd.Series({dt: _dp(dt) for dt in pivot.index}).dropna()
    return pd.DataFrame({"dt": value.index, "value": value.values})


def _splice_headline_15(sgs: dict | None, headline: pd.Series) -> pd.DataFrame:
    """IPCA-15 headline as one series: BCB/SGS 7478 where it exists, subitem
    reconstruction where it doesn't yet.

    Why this has to exist: every other IPCA-15 series on the 3M SAAR charts and
    the heatmap is computed in-house from `inflc_decomposicao`, so it lands the
    day IBGE publishes. The headline was the one exception -- it came only from
    the CSV, and SGS mirrors the IBGE release with about a day of lag. On
    release day that left `IPCA15_ma3_sa` one month short of every núcleo drawn
    beside it, which (a) cut the dotted "IPCA-15 (ref.)" line a month early and
    (b) silently dropped the newest month from the whole heatmap, whose 12
    columns are `compute3mSAAR('IPCA15').dates.slice(-12)`.

    SGS keeps priority for every month it covers, so published history stays
    exactly the official print -- only the not-yet-mirrored tail is
    reconstructed. That tail carries IBGE's subitem rounding (~0.006 p.p. mean
    deviation, 0.067 p.p. worst case over the 315 overlapping months; under
    0.005 p.p. in the last 18), i.e. below the 1-2 decimals anything displays,
    and it is replaced by the official value on the next fetch_bcb.py run.
    """
    recon = headline.dropna()
    if recon.empty:
        return pd.DataFrame(columns=["name", "dt", "value"])
    if sgs and sgs.get("dates"):
        official = pd.Series(sgs["values"], index=sgs["dates"]).dropna()
        merged = official.combine_first(recon)
    else:
        merged = recon
    return pd.DataFrame({"name": "IPCA15", "dt": merged.index, "value": merged.values})


def run(output: str = "reports/brasil/Inflation.html") -> None:
    print("Carregando dados...")
    decomposicao = _load_decomposicao()
    item = _load_decomposicao_item()

    ipca = _to_records(decomposicao, "IPCA")
    data = {
        "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "min_date":     ipca["min_date"],
        "max_date":     ipca["max_date"],
        "records":      ipca["records"],
    }
    print(f"  IPCA:    {len(data['records'])} registros ({data['min_date']} -> {data['max_date']})")

    ipca15 = _to_records(decomposicao, "IPCA15")
    data["records_ipca15"]  = ipca15["records"]
    data["min_date_ipca15"] = ipca15["min_date"]
    data["max_date_ipca15"] = ipca15["max_date"]
    print(f"  IPCA-15: {len(data['records_ipca15'])} registros ({data['min_date_ipca15']} -> {data['max_date_ipca15']})")

    data["ibge_nomes"] = _ibge_nomes(decomposicao)
    print(f"  Árvore IBGE: {len(data['ibge_nomes'])} nós de grupo/subgrupo/item")

    # Inércia: corr(yoy_t, yoy_t-12) por subitem, faixas de ~20% do peso.
    # Estimada no IPCA e herdada pelo IPCA-15 (ver analytics/brasil/inflation/inercia.py).
    data["inercia"] = _inercia.calcular(decomposicao)
    _f = data["inercia"]["faixas"]
    print(f"  Inércia: {data['inercia']['n_classificados']} subitens classificados em "
          f"{len(_f)} faixas ({', '.join(f'Q{x[chr(113)]}={x[chr(110)]}' for x in _f)}), "
          f"janela {data['inercia']['janela']['inicio']}→{data['inercia']['janela']['fim']}")

    data["bcb"] = _load_bcb()

    series15 = _compute_ipca15_nucleos(decomposicao)
    grupos15 = _compute_ipca15_grupos(decomposicao)
    if not grupos15.empty:
        series15 = pd.concat([series15, grupos15], ignore_index=True)

    p55_15 = _compute_p55(decomposicao, "IPCA15")
    if not p55_15.empty:
        p55_15 = p55_15.assign(name="IPCA15_nucleo_P55")[["name", "dt", "value"]]
        series15 = pd.concat([series15, p55_15], ignore_index=True)

    ma_15 = _compute_ma(item, "IPCA15")
    if not ma_15.empty:
        ma_15 = ma_15.assign(name="IPCA15_nucleo_medias_aparadas_sem_suavizacao")[["name", "dt", "value"]]
        series15 = pd.concat([series15, ma_15], ignore_index=True)

    ms_15 = _compute_ms(item, "IPCA15")
    if not ms_15.empty:
        ms_15 = ms_15.assign(name="IPCA15_nucleo_medias_aparadas")[["name", "dt", "value"]]
        series15 = pd.concat([series15, ms_15], ignore_index=True)

    headline_15 = _compute_headline(decomposicao, "IPCA15")
    dp_15 = _compute_dp(decomposicao, item, "IPCA15", headline_15)
    if not dp_15.empty:
        dp_15 = dp_15.assign(name="IPCA15_nucleo_DP")[["name", "dt", "value"]]
        series15 = pd.concat([series15, dp_15], ignore_index=True)

    ipca15_hl = _splice_headline_15(data["bcb"].get("IPCA15"), headline_15)
    if not ipca15_hl.empty:
        series15 = pd.concat([series15, ipca15_hl], ignore_index=True)

    if not series15.empty:
        sa15 = _apply_stl_ma3(series15, series=set(series15["name"].unique()))
        combined15 = pd.concat([series15, sa15], ignore_index=True) if not sa15.empty else series15
        data["bcb"].update(_series_dict(combined15))
        print(f"  IPCA-15 grupos/núcleos: {series15['name'].nunique()} séries computadas em casa (+ SAAR via STL)")

    difusao15 = _compute_difusao(decomposicao, "IPCA15")
    if not difusao15.empty:
        difusao15 = difusao15.assign(name="IPCA15_indice_difusao")[["name", "dt", "value"]]
        data["bcb"].update(_series_dict(difusao15))
        print(f"  IPCA-15 difusão: {len(difusao15)} meses")

    n_bcb = sum(len(v["dates"]) for v in data["bcb"].values())
    print(f"  BCB:     {n_bcb} obs ({len(data['bcb'])} series)")

    out = render_report(_TEMPLATE, data, output)
    print(f"Relatorio salvo: {out}")


if __name__ == "__main__":
    run()
