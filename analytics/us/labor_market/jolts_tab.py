"""
Conteudo de dominio da aba JOLTS: as 3 arvores, os rotulos de eixo e os cartoes
de definicao.

As **arvores nao sao escritas aqui** -- elas vem de `mt_jolts_dim`, que ja guarda
`pai`/`nivel`/`ordem` e cuja aditividade e validada na carga. `arvores()` so aninha
o que o banco tem. Escrever a hierarquia de novo neste modulo criaria uma segunda
fonte de verdade que envelheceria em silencio na primeira vez que o BLS mexesse na
lista de industrias.

O que E escrito aqui:

  MEDIDAS    as 6 medidas do release, com a natureza (estoque/fluxo) e o rotulo de
             eixo Y por tipo. O rotulo e uma DEFINICAO CURTA, nao o nome da unidade
             ("openings / (employment + openings), %" e nao "%"), conforme
             .claude/skills/lis-dashboard/references/design-system.md#unidades.
  INFO       cartoes de definicao, com chave em NAMESPACE. Ver abaixo.

--------------------------------------------------------------------------------
POR QUE A CHAVE DO INFO TEM NAMESPACE
--------------------------------------------------------------------------------
`00` e categoria em dois cortes com significados diferentes: no corte de tamanho e
*Total private, all size classes*; no de regiao e *Total US* (que inclui governo).
Um mapa de chave nua faria um cartao explicar o outro sem lancar nada -- o cartao
abre, com o texto errado. Mesmo achado de `analytics/brasil/fiscal_policy`
(2026-08-28), aqui com a agravante de os dois cortes terem **totais numericamente
diferentes** (6.461 contra 7.271 mil vagas em jul/2026).

--------------------------------------------------------------------------------
OS DENOMINADORES DAS TAXAS FORAM MEDIDOS, NAO COPIADOS DA DOCUMENTACAO
--------------------------------------------------------------------------------
A Nota Tecnica diz que a taxa de vagas divide por `emprego + vagas` e as outras
cinco por `emprego`. Isso e conferivel a partir do proprio banco, e foi: o emprego
implicito sai de `contratacoes_nivel / (contratacoes_taxa/100)`, e com ele

    vagas / (emprego + vagas)  reproduz a taxa publicada com erro medio de
                               0,038 p.p. (max 0,275) em 8.624 celulas
    vagas / emprego            erra 0,150 p.p. em media (max 1,483) -- 4x mais

e as cinco taxas de fluxo reproduzem com 0,027 a 0,035 p.p. de erro medio. O
residuo que sobra e o arredondamento a 1 decimal da taxa publicada, que e o que o
emprego implicito herda. Ou seja: os rotulos de eixo abaixo nao sao uma parafrase
da documentacao, sao uma afirmacao testada -- e o teste esta em
`tests/test_jolts.py`.
"""

from __future__ import annotations

import pandas as pd

# --------------------------------------------------------------------------- medidas
#
# `natureza` e o que decide como agregar: vagas e posicao no ultimo dia util do mes,
# as outras cinco sao tudo que passou pela folha durante o mes. Ver a docstring de
# domain/db/us/labor_market/mt_jolts.py.
#
# `y_nivel`/`y_taxa` sao os titulos de eixo -- numerador / denominador, unidade.
MEDIDAS = {
    "JO": {
        "label": "Job openings",
        "short": "Openings",
        "natureza": "estoque",
        "y_nivel": "job openings on the last business day, thousands",
        "y_taxa": "openings / (employment + openings), %",
        "y_share": "share of {raiz} job openings, %",
        # Sem `y_acum`: acumular um estoque nao produz quantidade nenhuma. E este
        # None que desliga a pill "12-month total" quando a medida e vagas.
        "y_acum": None,
    },
    "HI": {
        "label": "Hires",
        "short": "Hires",
        "natureza": "fluxo",
        "y_nivel": "hires during the month, thousands",
        "y_taxa": "hires / employment, %",
        "y_share": "share of {raiz} hires, %",
        "y_acum": "hires during the 12 months to the date, thousands",
    },
    "TS": {
        "label": "Total separations",
        "short": "Separations",
        "natureza": "fluxo",
        "y_nivel": "separations during the month, thousands",
        "y_taxa": "separations / employment, %",
        "y_share": "share of {raiz} separations, %",
        "y_acum": "separations during the 12 months to the date, thousands",
    },
    "QU": {
        "label": "Quits",
        "short": "Quits",
        "natureza": "fluxo",
        "y_nivel": "quits during the month, thousands",
        "y_taxa": "quits / employment, %",
        "y_share": "share of {raiz} quits, %",
        "y_acum": "quits during the 12 months to the date, thousands",
    },
    "LD": {
        "label": "Layoffs and discharges",
        "short": "Layoffs",
        "natureza": "fluxo",
        "y_nivel": "layoffs and discharges during the month, thousands",
        "y_taxa": "layoffs and discharges / employment, %",
        "y_share": "share of {raiz} layoffs and discharges, %",
        "y_acum": "layoffs and discharges during the 12 months to the date, thousands",
    },
    "OS": {
        "label": "Other separations",
        "short": "Other sep.",
        "natureza": "fluxo",
        "y_nivel": "other separations during the month, thousands",
        "y_taxa": "other separations / employment, %",
        "y_share": "share of {raiz} other separations, %",
        "y_acum": "other separations during the 12 months to the date, thousands",
    },
}

ORDEM_MEDIDAS = ["JO", "HI", "TS", "QU", "LD", "OS"]

CORTES = {
    "industria": {
        "label": "Industry",
        "col_label": "Industry",
        "raiz": "000000",
        "note": (
            "Tables 1&ndash;6 of the release. Four levels, and the levels are additive: "
            "children sum to their parent in <b>levels</b>, with a maximum residual of "
            "<b>3 thousand</b> on a 7.3 million total over the whole history &mdash; the "
            "rounding the BLS's own thousand-unit publication allows, nothing more. "
            "<b>Rates never add</b>: each one is a ratio against its own industry's "
            "employment."
        ),
    },
    "tamanho": {
        "label": "Establishment size",
        "col_label": "Establishment size class",
        "raiz": "00",
        "note": (
            "Table 7. <b>The root here is Total private, not Total nonfarm</b> &mdash; the "
            "BLS produces the size-class cut for the private sector only, and the gap is "
            "not cosmetic: 810 thousand government openings in July 2026 that this cut "
            "does not cover at all. The six classes sum to Total private (maximum residual "
            "2 thousand)."
        ),
    },
    "regiao": {
        "label": "Region",
        "col_label": "Region",
        "raiz": "00",
        "note": (
            "The four Census regions, Total nonfarm only &mdash; there is no industry "
            "breakdown by region in what the BLS publishes. They sum to Total US "
            "(maximum residual 2 thousand). <b>State estimates are deliberately absent</b>: "
            "all 51 series stop in December 2025, so they would be dead history in a "
            "report about the current month."
        ),
    },
}

# --------------------------------------------------------------------------- cartoes
#
# `namespace:categoria` -> {full, desc}. `full` entra no cartao SO quando difere do
# rotulo curto que a linha ja mostra (regra 3 do design system) -- por isso as
# entradas de Construction, Information, Manufacturing e Government nao tem `full`.
# As 6 medidas tambem nao: a pill ja mostra o nome oficial do BLS, entao o cartao
# existe ali so pela definicao. As 8 primeiras versoes deste mapa violavam a regra e
# foram pegas pela checagem de `generate_report.construir()`, nao pelo olho.
#
# A unidade nao esta aqui: e funcao dos seletores (medida x tipo x transformacao), e o
# template a monta com a MESMA string que vai para o titulo do eixo Y. Uma unidade fixa
# no cartao passaria a mentir no primeiro clique.
#
# Os codigos NAICS sao a identidade precisa de cada setor e por isso entram no lugar de
# uma parafrase -- e o que permite casar esta arvore com a do CES ou com a de qualquer
# outra pesquisa do BLS sem adivinhar.
INFO = {
    # ---- industria
    "industria:000000": {
        "desc": "All nonfarm establishments: the private sector plus federal, state and "
                "local government. Excludes agriculture, private households and the "
                "self-employed &mdash; the same universe as the CES payroll survey, which "
                "is what JOLTS is benchmarked to every month.",
    },
    "industria:100000": {
        "desc": "Every nonfarm industry except government. This is also the root of the "
                "establishment-size cut, which the BLS produces for the private sector only.",
    },
    "industria:110099": {
        "full": "Mining and logging",
        "desc": "NAICS 21 (mining, quarrying, and oil and gas extraction) plus logging "
                "(NAICS 1133). The smallest sector in the release &mdash; 22 thousand openings "
                "in July 2026 &mdash; so its monthly moves are mostly sampling noise.",
    },
    "industria:230000": {
        "desc": "NAICS 23. Highly seasonal in the unadjusted series, which is the clearest "
                "case on this page for looking at the seasonally adjusted view.",
    },
    "industria:300000": {
        "desc": "NAICS 31&ndash;33, split below into durable and nondurable goods.",
    },
    "industria:320000": {
        "full": "Durable goods manufacturing",
        "desc": "Wood products, metals, machinery, computers and electronics, "
                "transportation equipment, furniture (NAICS 321, 327, 331&ndash;337).",
    },
    "industria:340000": {
        "full": "Nondurable goods manufacturing",
        "desc": "Food, beverages and tobacco, textiles, apparel, paper, printing, "
                "petroleum and coal, chemicals, plastics and rubber (NAICS 311&ndash;316, "
                "322&ndash;326).",
    },
    "industria:400000": {
        "full": "Trade, transportation, and utilities",
        "desc": "Wholesale trade, retail trade, transportation and warehousing, and "
                "utilities (NAICS 42, 44&ndash;45, 48&ndash;49, 22). The largest private sector "
                "in the release.",
    },
    "industria:420000": {"desc": "NAICS 42."},
    "industria:440000": {"desc": "NAICS 44&ndash;45."},
    "industria:480099": {
        "full": "Transportation, warehousing, and utilities",
        "desc": "NAICS 48&ndash;49 plus utilities (NAICS 22). Warehousing is where the "
                "e-commerce cycle shows up in this release.",
    },
    "industria:510000": {
        "desc": "NAICS 51: publishing, motion picture and sound recording, broadcasting, "
                "telecommunications, data processing and web search.",
    },
    "industria:510099": {
        "desc": "Finance and insurance plus real estate, rental and leasing "
                "(NAICS 52 and 53).",
    },
    "industria:520000": {"full": "Finance and insurance", "desc": "NAICS 52."},
    "industria:530000": {
        "full": "Real estate and rental and leasing",
        "desc": "NAICS 53.",
    },
    "industria:540099": {
        "full": "Professional and business services",
        "desc": "Professional, scientific and technical services; management of companies; "
                "and administrative, support and waste services (NAICS 54, 55, 56). "
                "Includes temporary help, which makes this the sector that usually turns "
                "first in a hiring cycle.",
    },
    "industria:600000": {
        "full": "Private education and health services",
        "desc": "Private educational services plus health care and social assistance "
                "(NAICS 61 and 62). Public education is in Government, not here &mdash; the "
                "split matters, because the two have behaved very differently since 2020.",
    },
    "industria:610000": {
        "full": "Private educational services",
        "desc": "NAICS 61, private establishments only.",
    },
    "industria:620000": {
        "full": "Health care and social assistance",
        "desc": "NAICS 62. Carries the highest openings rate of any sector in the release "
                "(5.7% in July 2026).",
    },
    "industria:700000": {
        "full": "Leisure and hospitality",
        "desc": "Arts, entertainment and recreation plus accommodation and food services "
                "(NAICS 71 and 72). The highest-turnover sector: hires and separations "
                "rates near 5% a month, against ~3.2% for total nonfarm.",
    },
    "industria:710000": {
        "full": "Arts, entertainment, and recreation",
        "desc": "NAICS 71.",
    },
    "industria:720000": {
        "full": "Accommodation and food services",
        "desc": "NAICS 72.",
    },
    "industria:810000": {
        "desc": "NAICS 81 except public administration: repair and maintenance, personal "
                "and laundry services, religious, grantmaking, civic and professional "
                "organizations.",
    },
    "industria:900000": {
        "desc": "Federal, state and local government, including public education and "
                "public hospitals. Turnover is a third of the private sector's: a 1.3% "
                "hires rate against 3.5%.",
    },
    "industria:910000": {"full": "Federal government", "desc": "Federal government establishments."},
    "industria:920000": {
        "full": "State and local government",
        "desc": "State and local government, split below into education and everything else.",
    },
    "industria:923000": {
        "full": "State and local government education",
        "desc": "Public schools, colleges and universities. The largest single line inside "
                "government, and the one whose unadjusted series swings hardest with the "
                "school year.",
    },
    "industria:929000": {
        "full": "State and local government, excluding education",
        "desc": "Everything else state and local: administration, police and fire, public "
                "hospitals, transit, utilities.",
    },
    # ---- tamanho
    "tamanho:00": {
        "full": "Total private, all size classes",
        "desc": "The root of this cut. <b>Not Total nonfarm</b>: the BLS produces the "
                "size-class breakdown for the private sector only, so government &mdash; 810 "
                "thousand openings in July 2026 &mdash; is outside this table entirely.",
    },
    "tamanho:01": {
        "full": "1 to 9 employees",
        "desc": "Establishment, not firm: a size class counts employees at the physical "
                "location, so a small branch of a large company is counted here. That is "
                "why this is a read on local demand for labour rather than on small "
                "business as a sector.",
    },
    "tamanho:02": {"full": "10 to 49 employees", "desc": "Establishment size, not firm size."},
    "tamanho:03": {"full": "50 to 249 employees", "desc": "Establishment size, not firm size."},
    "tamanho:04": {"full": "250 to 999 employees", "desc": "Establishment size, not firm size."},
    "tamanho:05": {
        "full": "1,000 to 4,999 employees",
        "desc": "Establishment size, not firm size.",
    },
    "tamanho:06": {
        "full": "5,000 or more employees",
        "desc": "Establishment size, not firm size. The smallest class by level and the "
                "noisiest by rate &mdash; few establishments this large, so the sample behind "
                "it is thin.",
    },
    # ---- regiao
    "regiao:00": {
        "desc": "The national total, Total nonfarm &mdash; the same number as the root of the "
                "Industry tab, and <b>not</b> the same as the root of the Establishment "
                "size tab, which covers the private sector only.",
    },
    "regiao:NE": {
        "full": "Northeast region",
        "desc": "Census Northeast: New England plus New York, New Jersey and Pennsylvania.",
    },
    "regiao:SO": {
        "full": "South region",
        "desc": "Census South: South Atlantic, East South Central and West South Central, "
                "including Texas, Florida and the District of Columbia.",
    },
    "regiao:MW": {
        "full": "Midwest region",
        "desc": "Census Midwest: East North Central and West North Central.",
    },
    "regiao:WE": {
        "full": "West region",
        "desc": "Census West: Mountain and Pacific, including Alaska and Hawaii.",
    },
    # ---- medidas (o cartao mora no rotulo da pill)
    "medida:JO": {
        "desc": "All positions open on the <b>last business day</b> of the month. A job "
                "counts only if a specific position exists with work available, it could "
                "start within 30 days, and the establishment is actively recruiting from "
                "outside. <b>This is a stock, not a flow</b> &mdash; a snapshot of one day, "
                "which is why adding three months of it does not give a quarter.",
    },
    "medida:HI": {
        "desc": "All additions to the payroll <b>during the entire month</b>: new hires, "
                "rehires, recalls, transfers in, part-time and seasonal. A flow.",
    },
    "medida:TS": {
        "desc": "All separations from the payroll during the month, of any kind &mdash; the "
                "sum of quits, layoffs and discharges, and other separations. A flow.",
    },
    "medida:QU": {
        "desc": "Separations initiated by the <b>employee</b>. Because they are voluntary, "
                "the quits rate reads as a measure of workers' willingness or ability to "
                "leave a job &mdash; the release says so in as many words.",
    },
    "medida:LD": {
        "desc": "Involuntary separations initiated by the <b>employer</b>: layoffs from "
                "mergers, downsizing or closings, firings for cause, and the end of "
                "short-term or seasonal work.",
    },
    "medida:OS": {
        "desc": "Retirement, death, disability, and transfers to another location of the "
                "same firm. Small and slow-moving; it is here for completeness, since "
                "quits + layoffs + other is what adds up to total separations.",
    },
}


def arvores(dim: pd.DataFrame) -> dict:
    """Aninha `mt_jolts_dim` nas 3 arvores que o template consome.

    Args:
        dim: a tabela `mt_jolts_dim` inteira.

    Returns:
        `{corte: {label, col_label, note, anchor, tree, n_linhas, niveis}}`, com cada
        no no formato `{key, label, seriesKey, children?}` que a fabrica JS espera
        (o mesmo de `analytics/report_structure/tree_helpers.py`).

    Raises:
        RuntimeError: se um corte nao tiver exatamente uma raiz, ou se algum no ficar
            orfao. Sao os dois jeitos de a arvore sair torta sem que nada plote errado
            -- uma linha simplesmente nao aparece.
    """
    saida = {}
    for corte, cfg in CORTES.items():
        sub = dim[dim["corte"] == corte].sort_values("ordem")
        if sub.empty:
            raise RuntimeError(f"mt_jolts_dim nao tem nenhuma linha do corte {corte!r}")

        nos = {}
        for _, r in sub.iterrows():
            nos[r["categoria"]] = {
                "key": r["categoria"],
                "label": r["nome_curto"],
                "seriesKey": r["categoria"],
                "nivel": int(r["nivel"]),
            }

        raizes = []
        for _, r in sub.iterrows():
            no = nos[r["categoria"]]
            pai = r["pai"]
            if pai is None or (isinstance(pai, float) and pd.isna(pai)) or pai == "":
                raizes.append(no)
                continue
            if pai not in nos:
                raise RuntimeError(
                    f"{corte}/{r['categoria']}: pai {pai!r} nao esta na dim -- a linha "
                    "nao apareceria na tabela e nada levantaria"
                )
            nos[pai].setdefault("children", []).append(no)

        if len(raizes) != 1:
            raise RuntimeError(
                f"corte {corte!r} tem {len(raizes)} raizes ({[n['key'] for n in raizes]}), "
                "esperado exatamente 1"
            )
        if raizes[0]["key"] != cfg["raiz"]:
            raise RuntimeError(
                f"corte {corte!r}: a raiz na dim e {raizes[0]['key']!r} mas CORTES declara "
                f"{cfg['raiz']!r} -- se o BLS mudou a raiz do corte, o rotulo e a nota da "
                "aba tambem estao errados"
            )

        saida[corte] = {
            "label": cfg["label"],
            "colLabel": cfg["col_label"],
            "note": cfg["note"],
            "anchor": cfg["raiz"],
            "tree": [raizes[0]],
            "nLinhas": int(len(sub)),
            "niveis": int(sub["nivel"].max()) + 1,
        }
    return saida


def orfaos_info(arvs: dict) -> list[str]:
    """Chaves do INFO que nao resolvem contra nenhuma linha real das arvores.

    Existe porque um erro de digitacao numa chave produz um botao que **deixa de
    nascer**: sem erro, sem lacuna visivel, so um cartao que nunca abre. Ver a regra
    "teste a orfa, nao so o cartao" em `.claude/rules/lis-dashboards.md`.
    """
    validas = {f"medida:{m}" for m in MEDIDAS}
    for corte, cfg in arvs.items():
        def walk(ns):
            for n in ns:
                validas.add(f"{corte}:{n['key']}")
                walk(n.get("children") or [])
        walk(cfg["tree"])
    return sorted(set(INFO) - validas)


def rotulos(arvs: dict) -> dict:
    """Chave namespaced -> rotulo curto que a linha/pill de fato mostra."""
    saida = {f"medida:{m}": cfg["label"] for m, cfg in MEDIDAS.items()}
    for corte, cfg in arvs.items():
        def walk(ns):
            for n in ns:
                saida[f"{corte}:{n['key']}"] = n["label"]
                walk(n.get("children") or [])
        walk(cfg["tree"])
    return saida


def full_redundante(arvs: dict) -> list[str]:
    """Entradas cujo `full` so repete o rotulo curto que a linha ja mostra.

    Regra 3 do design system: o cartao nao deve abrir para dizer o que o leitor
    acabou de ler. Verificado contra os rotulos REAIS, nao contra o que este modulo
    acha que eles sao -- num port de ~50 entradas o olho para de pegar (no de
    `economic_activity` foram 31 violacoes na primeira rodada do teste).
    """
    labels = rotulos(arvs)
    return sorted(
        k for k, v in INFO.items()
        if v.get("full") and k in labels and v["full"] == labels[k]
    )
