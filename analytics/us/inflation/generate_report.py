"""
US Inflation report -- reads macro_us (inflc_cpi / inflc_cpi_dim / inflc_cpi_pesos),
injects one JSON payload into report.html, writes a self-contained HTML file.

Same /*REPORT_DATA*/ + /*THEME_CSS*/ + /*Y_AUTOFIT_JS*/ pattern as the Brazil
reports (see analytics/report_structure/CLAUDE.md). First report under analytics/us/.

Two tabs, one per CPI tree, both driven by the same JS hierarchy-table factory
(`makeHierTab`) that analytics/brasil/credit and .../fiscal_policy use -- the
table-plus-chart structure that analytics/brasil/inflation does NOT have:

  Release Tree      Table 1 of the CPI news release -- 37 published rows over 5
                    levels (food / energy / core, core split into goods and services)
                    -- and, below each row where the release stops, the matching
                    branch of the expenditure tree, so Gasoline (all types) opens into
                    its three grades without the tab ceasing to be Table 1. Those
                    rows are flagged `detail`; the 37 published rows and their
                    `partial` badges are untouched. See `_arvore`.
  Expenditure Tree  355 items x 10 levels. The full statistical structure, down to
                    Gasoline unleaded midgrade and Bacon and related products. 83 of
                    those items have a published index but NO published weight (the
                    layer below the relative-importance table -- see inflc_cpi_dim's
                    docstring): they carry `noWeight` in the payload, the table
                    badges them, and Contribution is blank for them by construction,
                    not by accident.

--------------------------------------------------------------------------------
PAYLOAD SHAPE -- levels only, variations computed in the browser
--------------------------------------------------------------------------------
The payload ships the index LEVEL per (item, adjustment) and nothing else; Y/Y,
M/M, 3-month annualised and contribution are all computed in JS at render time.

That is a size decision, not a stylistic one. Shipping 4 pre-computed metrics x 2
adjustments x 355 items would be ~8x the numbers for information already implied by
the level. Two compressions on top, both borrowed from
analytics/brasil/fiscal_policy/dlsp_tab.py:

  1. **One shared monthly date grid per adjustment**, at the payload root. Each
     series is then a bare array aligned to that grid, with nulls where the item has
     no observation -- dates are not repeated 500+ times.
  2. **Two different history windows.** The 37 release-tree items ship full history
     (1913 for All items/Food/Electricity); the 355 expenditure items start at
     `_INICIO_DETALHE`. Full history for all 355 is ~1M numbers of mostly nulls,
     since most detail items begin in the 1990s or later anyway. The database keeps
     everything from 1913 either way -- this is a payload window, not a data window.

--------------------------------------------------------------------------------
CONTRIBUTION AND THE WEIGHT-CARRY CONVENTION
--------------------------------------------------------------------------------
`contribuicao` is NOT stored in the database (see inflc_cpi_pesos' docstring) -- it
is a join decision made here and re-made in JS: for a month in year Y, use the
December snapshot of year Y-1, falling back to the nearest earlier snapshot, and to
the earliest available one for months before the first snapshot.

That is the BLS's own construction: the file named `2025.xlsx` carries reference
period December 2025 and is what prices 2026. It is also measured to be the better
choice -- using each year's own snapshot instead of a single vector cuts the
headline reconciliation error by ~30% (0.0183 -> 0.0124 p.p. mean absolute, measured
against this database).

**Contribution is an approximation, never an identity**, and the report says so on
the face of the tab. Two independent reasons:
  - relative importance is a December snapshot of a quantity the BLS price-updates
    continuously, leaving ~0.015 p.p. of irreducible reconciliation error;
  - in the release tree, only levels 0-2 partition the index. 7 of its 13 parents
    show just their largest children, leaving 25.583 points of the index with no row
    at all, so contributions summed at level >= 3 do not add to the parent. The
    `decomposicao`/`peso_nao_exibido` columns carry that per node and the table
    renders it as a badge.

Como gerar:
    uv run python -c "from analytics.us.inflation.generate_report import run; run()"
    # Saida: reports/us/Inflation.html
"""

from __future__ import annotations

import datetime as _dt

import pandas as pd

from analytics.report_structure.builder import render_report

from connectors.mysql import MySQLDataRequester

_DATABASE = "macro_us"
_TEMPLATE = "analytics/us/inflation/report.html"

# Janela do payload para a arvore de despesa (267 itens). A de divulgacao (37) vem
# inteira. Ver "PAYLOAD SHAPE" na docstring.
_INICIO_DETALHE = "1990-01-01"

_INDICE = "CPI-U"


def _conn():
    req = MySQLDataRequester(_DATABASE, "inflc_cpi")
    req.connect()
    if req.connection is None:
        raise RuntimeError(
            "sem conexao com o MySQL. Este relatorio le macro_us direto do banco -- "
            "sem CSV/Excel local. Confira o .env."
        )
    return req.connection


def _load():
    conn = _conn()
    try:
        dim = pd.read_sql(
            "SELECT arvore, item_code, item_name, nivel, parent_item_code, caminho, "
            "       n_filhos, is_leaf, is_special_aggregate, tem_peso, decomposicao, "
            "       peso_nao_exibido, sort_order, sa_begin, nsa_begin, nsa_end "
            "FROM inflc_cpi_dim ORDER BY arvore, sort_order",
            conn,
        )
        obs = pd.read_sql(
            "SELECT date, item_code, ajuste, value FROM inflc_cpi "
            f"WHERE indice = '{_INDICE}' ORDER BY item_code, ajuste, date",
            conn,
        )
        pesos = pd.read_sql(
            "SELECT reference_period, item_code, secao, weight FROM inflc_cpi_pesos "
            f"WHERE indice = '{_INDICE}' AND item_code IS NOT NULL",
            conn,
        )
    finally:
        conn.close()

    obs["date"] = pd.to_datetime(obs["date"])
    pesos["reference_period"] = pd.to_datetime(pesos["reference_period"])
    return dim, obs, pesos


def _marcar(d: dict, r, ultimo_mes: str) -> None:
    """Flags que valem para no de qualquer uma das duas arvores."""
    # Sem peso publicado: contribuicao nao existe para o item. Marcado no no para a
    # tabela dizer por que a celula esta vazia em vez de parecer dado faltando.
    if not int(r["tem_peso"]):
        d["noWeight"] = 1
    # Serie sem observacao recente -- itens enxertados que o BLS parou de publicar,
    # mais 4 da planilha descontinuados em 2024. Sem isto a linha simplesmente para
    # no meio do grafico sem explicacao.
    #
    # Folga de 3 meses de proposito: 1 mes atrasado e lag de divulgacao, nao serie
    # encerrada (`Services by other medical professionals` estava 1 mes atras em
    # 2026-07 e continua viva). O rotulo diz "last <mes>", o fato observado, em vez
    # de afirmar que o BLS encerrou a serie.
    fim = r["nsa_end"]
    if isinstance(fim, str) and fim < _menos_meses(ultimo_mes, 3):
        d["stale"] = fim


def _menos_meses(ym: str, n: int) -> str:
    """'2026-07' menos n meses, como 'YYYY-MM'."""
    a, m = int(ym[:4]), int(ym[5:7])
    total = a * 12 + (m - 1) - n
    return f"{total // 12:04d}-{total % 12 + 1:02d}"


def _conta_nos(tree: list[dict]) -> int:
    return sum(1 + _conta_nos(n.get("children") or []) for n in tree)


def _maps(dim: pd.DataFrame, arvore: str):
    g = dim[dim["arvore"] == arvore]
    filhos: dict[str, list[str]] = {}
    for _, r in g.iterrows():
        if r["parent_item_code"]:
            filhos.setdefault(r["parent_item_code"], []).append(r["item_code"])
    return filhos, {r["item_code"]: r for _, r in g.iterrows()}


def _arvore(dim: pd.DataFrame, arvore: str, ultimo_mes: str,
            detalhe_de: str | None = None) -> list[dict]:
    """Monta a arvore aninhada {key, label, seriesKey, children} que o JS consome.

    Mesma forma que analytics/report_structure/tree_helpers.py produz para os
    relatorios do Brasil -- aqui e montada a partir das colunas de parentesco da
    dim em vez de escrita a mao, porque a hierarquia vem do banco.

    `detalhe_de` liga o DRILL-DOWN: onde a arvore principal termina (uma folha), o
    ramo correspondente da outra arvore continua abaixo, marcado `detail`. E o que
    faz a aba de divulgacao chegar aos 3 tipos de gasolina sem deixar de ser a
    Tabela 1: as 37 linhas publicadas e os badges `partial` delas ficam intocados --
    o enxerto entra SO abaixo de folha, nunca ao lado de um filho publicado. Por isso
    `Motor fuel` continua marcado `partial` (o release omite `Other motor fuels`, que
    e IRMAO de `Gasoline (all types)`, nao um nivel mais fundo) enquanto
    `Gasoline (all types)` abre nos 3 tipos.

    Sem custo de payload: os niveis desses itens ja viajam na aba de despesa e o JS
    procura a serie na aba que a tiver (ver `seriesSource` no template).
    """
    filhos, por_code = _maps(dim, arvore)
    raizes = [c for c, r in por_code.items() if not r["parent_item_code"]]
    det_filhos, det_por_code = _maps(dim, detalhe_de) if detalhe_de else ({}, {})
    proprios = set(por_code)

    def no_detalhe(code: str, visto: frozenset) -> dict:
        r = det_por_code[code]
        d = {"key": code, "label": r["item_name"], "seriesKey": code,
             "level": int(r["nivel"]), "detail": 1}
        _marcar(d, r, ultimo_mes)
        kids = [c for c in det_filhos.get(code, []) if c not in visto]
        if kids:
            d["children"] = [no_detalhe(c, visto | {code}) for c in kids]
        return d

    def no(code: str, visto: frozenset) -> dict:
        r = por_code[code]
        d = {
            "key": code,
            "label": r["item_name"],
            "seriesKey": code,
            "level": int(r["nivel"]),
        }
        if r["decomposicao"]:
            d["decomp"] = r["decomposicao"]
        if r["peso_nao_exibido"] is not None and not pd.isna(r["peso_nao_exibido"]):
            d["unshown"] = round(float(r["peso_nao_exibido"]), 3)
        if int(r["is_special_aggregate"]):
            d["special"] = 1
        _marcar(d, r, ultimo_mes)
        kids = [c for c in filhos.get(code, []) if c not in visto]
        if kids:
            d["children"] = [no(c, visto | {code}) for c in kids]
        elif code in det_filhos:
            # A arvore principal para aqui; a outra continua. Nunca sobrescreve um
            # filho publicado, e um codigo que ja exista nesta arvore fica de fora
            # (nao ha caso hoje -- a assercao guarda contra um release novo que crie).
            kids = [c for c in det_filhos[code] if c not in proprios]
            assert len(kids) == len(det_filhos[code]), (
                f"drill-down em {code}: {set(det_filhos[code]) & proprios} ja existe "
                f"na arvore '{arvore}' -- duplicaria linha"
            )
            if kids:
                d["children"] = [no_detalhe(c, frozenset({code})) for c in kids]
        return d

    return [no(c, frozenset()) for c in raizes]


def _grade(obs: pd.DataFrame, codes: list[str], inicio: str | None):
    """Grade mensal comum + um array de valores por (item, ajuste) alinhado a ela."""
    sub = obs[obs["item_code"].isin(codes)]
    if inicio:
        sub = sub[sub["date"] >= inicio]
    grades, series = {}, {}
    for ajuste, g in sub.groupby("ajuste"):
        datas = pd.DatetimeIndex(sorted(g["date"].unique()))
        grades[ajuste] = [d.strftime("%Y-%m-%d") for d in datas]
        pos = {d: i for i, d in enumerate(datas)}
        for code, gi in g.groupby("item_code"):
            vals = [None] * len(datas)
            for d, v in zip(gi["date"], gi["value"]):
                vals[pos[d]] = None if pd.isna(v) else float(v)
            series.setdefault(code, {})[ajuste] = vals
    return grades, series


def _pesos_payload(pesos: pd.DataFrame, codes: set[str]) -> dict:
    """{item_code: {ano_do_snapshot: peso}} -- o JS escolhe o snapshot por data.

    Um item_code pode aparecer nas duas secoes da planilha (expenditure e
    special_aggregate). Quando aparece, o peso e o mesmo numero; ainda assim a
    escolha e explicita (`expenditure` primeiro) para nao depender da ordem das
    linhas.
    """
    p = pesos[pesos["item_code"].isin(codes)].copy()
    p["ordem"] = (p["secao"] != "expenditure").astype(int)
    p = p.sort_values(["item_code", "reference_period", "ordem"])
    p = p.drop_duplicates(["item_code", "reference_period"], keep="first")
    out: dict[str, dict[str, float]] = {}
    for code, g in p.groupby("item_code"):
        out[code] = {
            str(rp.year): round(float(w), 4)
            for rp, w in zip(g["reference_period"], g["weight"])
            if not pd.isna(w)
        }
    return out


def build_payload() -> dict:
    dim, obs, pesos = _load()

    rel_codes = dim.loc[dim["arvore"] == "divulgacao", "item_code"].tolist()
    exp_codes = dim.loc[dim["arvore"] == "despesa", "item_code"].tolist()

    rel_grades, rel_series = _grade(obs, rel_codes, None)
    exp_grades, exp_series = _grade(obs, exp_codes, _INICIO_DETALHE)

    todos = set(rel_codes) | set(exp_codes)
    pesos_pl = _pesos_payload(pesos, todos)

    ultimo = obs["date"].max()
    cobertura = dim.set_index(["arvore", "item_code"])

    n_drill = _conta_nos(_arvore(dim, "divulgacao", ultimo.strftime("%Y-%m"),
                                 detalhe_de="despesa")) - len(rel_codes)
    print(f"  release tree:     {len(rel_codes)} linhas publicadas + {n_drill} de drill-down, "
          f"grade {len(rel_grades.get('NSA', []))} meses NSA / {len(rel_grades.get('SA', []))} SA")
    sem_peso = int((dim[(dim["arvore"] == "despesa") & (dim["tem_peso"] == 0)]).shape[0])
    print(f"  expenditure tree: {len(exp_codes)} itens ({sem_peso} sem peso publicado), grade "
          f"{len(exp_grades.get('NSA', []))} meses NSA / {len(exp_grades.get('SA', []))} SA "
          f"(desde {_INICIO_DETALHE[:4]})")
    print(f"  pesos: {len(pesos_pl)} itens com peso, snapshots "
          f"{sorted({a for v in pesos_pl.values() for a in v})}")

    return {
        "meta": {
            "indice": _INDICE,
            "gerado_em": _dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "ultimo_mes": ultimo.strftime("%Y-%m"),
            "inicio_detalhe": _INICIO_DETALHE[:4],
            "n_release": len(rel_codes),
            "n_release_drill": _conta_nos(
                _arvore(dim, "divulgacao", ultimo.strftime("%Y-%m"), detalhe_de="despesa")
            ) - len(rel_codes),
            "n_expenditure": len(exp_codes),
            "n_expenditure_sem_peso": int(
                (dim[(dim["arvore"] == "despesa") & (dim["tem_peso"] == 0)]).shape[0]
            ),
            "niveis_expenditure": int(dim.loc[dim["arvore"] == "despesa", "nivel"].max()) + 1,
            "fonte": "BLS -- API v2, cu.item, Table 1 do news release, relative importance",
        },
        "tabs": {
            "release": {
                "tree": _arvore(dim, "divulgacao", ultimo.strftime("%Y-%m"),
                                detalhe_de="despesa"),
                "dates": rel_grades,
                "series": rel_series,
                "anchor": "SA0",
                "defaultChecked": ["SAF1", "SA0E", "SA0L1E"],
            },
            "expenditure": {
                "tree": _arvore(dim, "despesa", ultimo.strftime("%Y-%m")),
                "dates": exp_grades,
                "series": exp_series,
                "anchor": "SA0",
                "defaultChecked": ["SAF", "SAH", "SAT", "SAM"],
            },
        },
        "weights": pesos_pl,
        "coverage": {
            code: {
                "nsa_begin": None if pd.isna(row["nsa_begin"]) else int(row["nsa_begin"]),
                "sa_begin": None if pd.isna(row["sa_begin"]) else int(row["sa_begin"]),
            }
            for (arv, code), row in cobertura.iterrows()
            if arv == "divulgacao" or code in set(exp_codes)
        },
    }


def run(output: str = "reports/us/Inflation.html") -> None:
    """Gera o relatorio de inflacao dos EUA.

    Args:
        output: caminho de saida. Default "reports/us/Inflation.html" -- reports/
                espelha o layout pais > area de analytics/ (ver analytics/CLAUDE.md),
                e sem isso o Inflation.html do Brasil e o dos EUA colidiriam.
    """
    print(f"Lendo {_DATABASE} ({_INDICE})...")
    data = build_payload()
    out = render_report(_TEMPLATE, data, output)
    print(f"Relatorio salvo: {out}")


if __name__ == "__main__":
    run()
