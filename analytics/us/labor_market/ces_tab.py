"""
Conteudo de dominio das duas abas da CES (payroll): medidas, arvore e cartoes.

Duas familias e nao uma, porque **as raizes sao diferentes**:

    emprego            raiz Total nonfarm     839 industrias
    horas e ganhos     raiz Total private     549 industrias, nenhuma de governo

A CES nao publica horas nem ganhos do setor publico, entao a arvore da segunda aba
comeca em Total private -- exatamente o mesmo formato do corte de tamanho do JOLTS, e
pelo mesmo motivo: uma aba unica com um seletor de medida faria o total mudar de
significado sem dizer.

--------------------------------------------------------------------------------
O QUE SOMA ENTRE INDUSTRIAS, E O QUE ISSO DESLIGA
--------------------------------------------------------------------------------
`aditivo` decide tres controles ao mesmo tempo (barras empilhadas, "% do total" e a
regra "pai marcado com filho marcado vira linha"):

    aditivo    emprego, horas agregadas, folha agregada, overtime agregado
    nao        toda MEDIA por trabalhador e todo INDICE

Somar ganho medio por hora de duas industrias nao da ganho medio de nada -- e media
ponderada pelo emprego, e o peso nao esta na serie. Empilhar indices de base 2007=100
tampouco.

**Nenhuma medida da CES acumula em 12 meses.** Emprego e estoque; horas e ganhos sao
taxas semanais; os agregados sao "de uma semana". Somar doze meses de folha semanal
agregada nao da a folha do ano. Por isso `y_acum` e None nas treze.

--------------------------------------------------------------------------------
A BORDA DIREITA IRREGULAR E CONTEUDO, NAO BUG
--------------------------------------------------------------------------------
A primeira divulgacao de um mes traz os niveis agregados; o detalhe vem com a
divulgacao seguinte. Medido em ago/2026: no mes mais recente **27 das 555 folhas** tem
dado, e os niveis 0-4 estao completos. `cobertura_mes` no payload diz, por mes e por
aba, quantas linhas da arvore ja existem -- para o cabecalho do grafico e a tabela
poderem dizer isso em vez de desenhar uma queda que e ausencia de dado.
"""

from __future__ import annotations

import pandas as pd

# ── as 13 medidas ────────────────────────────────────────────────────────────
# `familia` separa as duas abas. `aditivo` e o que governa barras/participacao.
# `y_share` so existe onde aditivo=1 (participacao de uma media nao e nada).
MEDIDAS: dict[str, dict] = {
    "emprego": {
        "label": "Employment", "short": "Employment", "familia": "emprego",
        "natureza": "estoque", "aditivo": 1,
        "dec": 1,
        "y_nivel": "employees on payrolls, thousands",
        "y_share": "share of {raiz} employment, %",
        "y_acum": None,
    },
    "horas_semana": {
        "label": "Weekly hours", "short": "Hours", "familia": "horas",
        "natureza": "media", "aditivo": 0,
        "dec": 1,
        "y_nivel": "average weekly hours per employee",
        "y_share": None, "y_acum": None,
    },
    "overtime_semana": {
        "label": "Overtime hours", "short": "Overtime", "familia": "horas",
        "natureza": "media", "aditivo": 0,
        "dec": 1,
        "y_nivel": "average weekly overtime hours per employee",
        "y_share": None, "y_acum": None,
    },
    "ganho_hora": {
        "label": "Hourly earnings", "short": "AHE", "familia": "horas",
        "natureza": "media", "aditivo": 0,
        "dec": 2,
        "y_nivel": "average hourly earnings, US$",
        "y_share": None, "y_acum": None,
    },
    "ganho_semana": {
        "label": "Weekly earnings", "short": "AWE", "familia": "horas",
        "natureza": "media", "aditivo": 0,
        "dec": 2,
        "y_nivel": "average weekly earnings, US$",
        "y_share": None, "y_acum": None,
    },
    "ganho_hora_real": {
        "label": "Real hourly earnings", "short": "Real AHE", "familia": "horas",
        "natureza": "media", "aditivo": 0,
        "dec": 2,
        "y_nivel": "average hourly earnings, constant 1982-84 US$",
        "y_share": None, "y_acum": None,
    },
    "ganho_semana_real": {
        "label": "Real weekly earnings", "short": "Real AWE", "familia": "horas",
        "natureza": "media", "aditivo": 0,
        "dec": 2,
        "y_nivel": "average weekly earnings, constant 1982-84 US$",
        "y_share": None, "y_acum": None,
    },
    "ganho_hora_ex_ot": {
        "label": "Hourly earnings ex-overtime", "short": "AHE ex-OT",
        "familia": "horas", "natureza": "media", "aditivo": 0,
        "dec": 2,
        "y_nivel": "average hourly earnings excluding overtime, US$",
        "y_share": None, "y_acum": None,
    },
    "horas_agreg": {
        "label": "Aggregate weekly hours", "short": "Agg. hours",
        "familia": "horas", "natureza": "agregado", "aditivo": 1,
        "dec": 0,
        "y_nivel": "hours worked in the week, thousands",
        "y_share": "share of {raiz} aggregate hours, %", "y_acum": None,
    },
    "folha_agreg": {
        "label": "Aggregate weekly payrolls", "short": "Agg. payrolls",
        "familia": "horas", "natureza": "agregado", "aditivo": 1,
        "dec": 0,
        "y_nivel": "payrolls for the week, thousands of US$",
        "y_share": "share of {raiz} aggregate payrolls, %", "y_acum": None,
    },
    "overtime_agreg": {
        "label": "Aggregate overtime hours", "short": "Agg. overtime",
        "familia": "horas", "natureza": "agregado", "aditivo": 1,
        "dec": 0,
        "y_nivel": "overtime hours in the week, thousands",
        "y_share": "share of {raiz} aggregate overtime, %", "y_acum": None,
    },
    "idx_horas": {
        "label": "Index of aggregate hours", "short": "Hours index",
        "familia": "horas", "natureza": "indice", "aditivo": 0,
        "dec": 1,
        "y_nivel": "index of aggregate weekly hours, 2007 = 100",
        "y_share": None, "y_acum": None,
    },
    "idx_folha": {
        "label": "Index of aggregate payrolls", "short": "Payrolls index",
        "familia": "horas", "natureza": "indice", "aditivo": 0,
        "dec": 1,
        "y_nivel": "index of aggregate weekly payrolls, 2007 = 100",
        "y_share": None, "y_acum": None,
    },
}

ORDEM_EMPREGO = ["emprego"]
ORDEM_HORAS = [
    "horas_semana", "ganho_hora", "ganho_semana", "ganho_hora_real",
    "ganho_semana_real", "ganho_hora_ex_ot", "overtime_semana",
    "horas_agreg", "folha_agreg", "overtime_agreg", "idx_horas", "idx_folha",
]

# A aba de horas/ganhos leva so os niveis 0-4 da arvore, por tamanho de payload: sao
# 94 industrias contra 549, e e a granularidade que as tabelas B-2/B-3/B-4 do proprio
# release publicam. O banco guarda as 549 -- o corte e do relatorio, nao do dado.
NIVEL_MAX_HORAS = 4

# ── cartoes de definicao ─────────────────────────────────────────────────────
# 839 industrias nao ganham texto escrito a mao. O `full` de cada linha e o nome
# OFICIAL do BLS (que quase sempre difere do rotulo curto, e e por isso que o cartao
# tem o que dizer), montado em `cartoes()`. O `desc` abaixo cobre so o que precisa de
# explicacao -- os agregados do topo, onde a definicao nao e obvia pelo nome.
DESC: dict[str, str] = {
    "00000000": (
        "All wage and salary jobs on nonfarm payrolls, counted from the establishment "
        "side. A person holding two jobs is counted twice, and the self-employed, "
        "unpaid family workers, farm workers and household workers are not counted at "
        "all — which is the main reason this level disagrees with the household "
        "survey's employment number by millions of people."
    ),
    "05000000": (
        "Total nonfarm minus government. The monthly change in this line is what "
        "commentary means by “private payrolls”."
    ),
    "06000000": (
        "Mining and logging, construction and manufacturing. Entirely private in this "
        "survey — government is never inside it, which is why it nests under Total "
        "private rather than beside it."
    ),
    "07000000": (
        "Everything that is not goods-producing, including government. It is published "
        "by the BLS but sits outside the tree on this page: it crosses the Total "
        "private boundary, so it cannot be a level of the same hierarchy without "
        "double-counting."
    ),
    "08000000": (
        "The seven private service supersectors. Total private minus goods-producing."
    ),
    "90000000": (
        "Federal, state and local government payrolls, including public education and "
        "public hospitals. Government has no hours or earnings in this survey, which "
        "is why the hours and earnings tree starts at Total private."
    ),
    "31000000": (
        "Manufacturing of goods expected to last three years or more — metals, "
        "machinery, electronics, vehicles, aerospace."
    ),
    "32000000": (
        "Manufacturing of goods consumed quickly — food, beverages, apparel, paper, "
        "chemicals, plastics."
    ),
    "60000000": (
        "Professional, scientific and technical services, management of companies, and "
        "administrative and waste services. Temporary help sits inside the third of "
        "these and is watched as an early cyclical signal."
    ),
    "65000000": (
        "Private education and health services. The public counterparts — state and "
        "local government education, public hospitals — are inside Government, not "
        "here."
    ),
    "90931611": (
        "Teachers and staff of public school districts. The largest single line inside "
        "local government, and the one whose seasonal pattern dominates the "
        "not-adjusted government series over the summer."
    ),
}

# As medidas tambem ganham cartao, na chave `medida_ces:<slug>`.
DESC_MEDIDA: dict[str, str] = {
    "emprego": (
        "The number of filled jobs on the payroll of the reporting establishment for "
        "the pay period that includes the 12th of the month. It is a stock — a "
        "position, not a flow — so the headline “payrolls rose by 89,000” is "
        "the month-over-month difference of this level, which is why the M/M reading "
        "exists."
    ),
    "horas_semana": (
        "Total hours paid for divided by the number of employees, so it includes paid "
        "leave and overtime. It moves before employment does in a downturn: firms cut "
        "hours before headcount."
    ),
    "overtime_semana": (
        "Overtime hours per employee, published for manufacturing only. Historically "
        "the earliest of the labour-market turning-point signals, and the reason it is "
        "reported separately at all."
    ),
    "ganho_hora": (
        "Payroll dollars divided by hours paid. It is not a wage rate for a fixed "
        "worker: a shift in the composition of employment toward better-paid "
        "industries raises it with no one getting a raise."
    ),
    "ganho_semana": (
        "Average hourly earnings times average weekly hours. It rises when hours rise "
        "even if the hourly rate does not, so it is the better read on take-home pay "
        "and the worse read on wage pressure."
    ),
    "ganho_hora_real": (
        "Average hourly earnings deflated by the CPI-U, in constant 1982-84 dollars, "
        "as the BLS publishes it. The comparison worth making is against the same "
        "series a year earlier: it answers whether pay beat inflation."
    ),
    "ganho_semana_real": (
        "Average weekly earnings in constant 1982-84 dollars. Falls when either the "
        "hourly rate loses to inflation or hours are cut."
    ),
    "ganho_hora_ex_ot": (
        "Average hourly earnings with overtime premia removed, published for "
        "manufacturing only. It separates a genuine wage increase from more hours at "
        "time-and-a-half."
    ),
    "horas_agreg": (
        "All hours worked in the reference week across the industry — employment times "
        "average weekly hours. Unlike the per-worker average, this one adds across "
        "industries, so it can be stacked and expressed as a share of the total."
    ),
    "folha_agreg": (
        "All payroll dollars for the reference week — employment times weekly "
        "earnings. It is the labour-income aggregate that feeds a consumption view, "
        "and it adds across industries."
    ),
    "overtime_agreg": (
        "All overtime hours in the reference week, manufacturing only."
    ),
    "idx_horas": (
        "Aggregate weekly hours as an index, 2007 = 100 — the form the release's "
        "table B-4 publishes. An index does not add across industries, so stacking and "
        "shares are unavailable here; the same quantity in thousands of hours is one "
        "measure up the list and does add."
    ),
    "idx_folha": (
        "Aggregate weekly payrolls as an index, 2007 = 100. Same caveat as the hours "
        "index: use the thousands-of-dollars version to compare or stack industries."
    ),
}


def _no(row: pd.Series) -> dict:
    return {
        "key": row["categoria"],
        "label": row["nome_curto"],
        "nivel": int(row["nivel"]),
        "agregavel": int(row["agregavel"]),
        "cobertura": None if pd.isna(row["cobertura"]) else round(float(row["cobertura"]), 2),
        "desvioSa": None if pd.isna(row["desvio_sa"]) else round(float(row["desvio_sa"]), 3),
    }


def arvore(dim: pd.DataFrame, raiz: str, nivel_max: int | None = None,
           exigir_horas: bool = False) -> list[dict]:
    """Aninha `mt_ces_dim` a partir de `raiz`, cortando por nivel e/ou tem_horas.

    Levanta se a raiz nao existe ou se um no fica orfao dentro do corte -- um no cujo
    pai foi cortado desapareceria da tabela sem erro nenhum.
    """
    d = dim[dim["alternativo"] == 0].copy()
    if nivel_max is not None:
        d = d[d["nivel"] <= nivel_max]
    if exigir_horas:
        d = d[(d["tem_horas"] == 1) | (d["categoria"] == raiz)]
    if raiz not in set(d["categoria"]):
        raise RuntimeError(f"raiz {raiz!r} nao esta na dimensao depois do corte")

    presentes = set(d["categoria"])
    filhos: dict[str, list[dict]] = {}
    for _, r in d.sort_values("ordem").iterrows():
        if r["categoria"] == raiz:
            continue
        pai = r["pai"]
        # Sob um corte por nivel/horas o pai imediato pode ter saido: sobe ate achar
        # um ancestral que ficou, o que preserva a arvore em vez de perder o ramo.
        cadeia = r["caminho"].split(" > ")
        while pai is not None and pai not in presentes:
            i = cadeia.index(pai) if pai in cadeia else -1
            pai = cadeia[i - 1] if i > 0 else None
        if pai is None:
            raise RuntimeError(
                f"{r['categoria']} ({r['nome_curto']}) ficou sem ancestral dentro do "
                f"corte (raiz {raiz}, nivel_max {nivel_max}, exigir_horas {exigir_horas})"
            )
        filhos.setdefault(pai, []).append(_no(r))

    def montar(no: dict) -> dict:
        fs = filhos.get(no["key"], [])
        if fs:
            no["children"] = [montar(f) for f in fs]
        return no

    r0 = d[d["categoria"] == raiz].iloc[0]
    return [montar(_no(r0))]


def achatar(tree: list[dict]) -> list[dict]:
    out: list[dict] = []

    def walk(ns):
        for n in ns:
            out.append(n)
            walk(n.get("children", []))
    walk(tree)
    return out


def cartoes(dim: pd.DataFrame, prefixo: str) -> dict[str, dict]:
    """`<prefixo>:<categoria>` -> {full, desc}, e `medida_ces:<slug>` -> {desc}.

    `full` e o nome oficial do BLS, e entra **so quando difere do rotulo curto** --
    um cartao que repete a linha nao informa nada (regra de
    .claude/rules/lis-dashboards.md).
    """
    info: dict[str, dict] = {}
    for _, r in dim[dim["alternativo"] == 0].iterrows():
        e: dict = {}
        if r["nome"].strip() != r["nome_curto"].strip():
            e["full"] = r["nome"].strip()
        if r["categoria"] in DESC:
            e["desc"] = DESC[r["categoria"]]
        if r["naics"] and r["naics"] != "-":
            e["naics"] = r["naics"]
        if e:
            info[f"{prefixo}:{r['categoria']}"] = e
    for slug, txt in DESC_MEDIDA.items():
        info[f"medida_ces:{slug}"] = {"desc": txt}
    return info


def full_redundante(info: dict[str, dict], rotulos: dict[str, str]) -> list[str]:
    """Entradas cujo `full` repete o rotulo curto que a linha ja mostra."""
    return sorted(k for k, e in info.items()
                  if e.get("full") and e["full"].strip() == (rotulos.get(k) or "").strip())
