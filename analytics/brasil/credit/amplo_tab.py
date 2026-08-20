"""
Monta o dataset da segunda tabela da aba "Saldo": Credito Ampliado ao setor nao
financeiro (cred_credito_amplo) — Governo/Empresas/Familias por instrumento de divida
(emprestimos, titulos, divida externa). Mesmas metricas da tabela de modalidades
(Nivel/Y-Y/M-M(SA)/T-T(SA) x Nominal/Real/% PIB, ver saldo_tab.py/transforms.py) —
pedido explicito do usuario, 2026-08 ("pode considerar as mesmas metricas da outra
tabela de saldo").

Diferenca de saldo_tab.py: `cred_credito_amplo` nao publica nenhum codigo SGS de
"total" por setor (Governo/Empresas/Familias) nem um total geral — a antiga aba
"Credito Ampliado" (v1, removida na reconstrucao aba-por-aba) ja calculava esses 3
totais somando os leaves no proprio browser (sumSeries()). Aqui a soma e feita em
Python (tf.sum_series(), valida porque soma NIVEIS em R$, nao crescimento/percentual —
mesmo raciocinio de saldo_tab.py's "porte__total"/"ativ__total") para que os totais
tambem passem pelo pipeline STL/deflacao/% PIB como qualquer outra linha da arvore.
"""
from analytics.brasil.credit import transforms as tf
from analytics.report_structure import tree_helpers as th

_leaf, _group = th.leaf, th.group

_GOVERNO_TREE = [
    _leaf("amplo", "gov_emprestimos_sfn", "Empréstimos — Sistema Financeiro Nacional"),
    _leaf("amplo", "gov_titulos_publicos", "Títulos Públicos"),
    _leaf("amplo", "gov_emprestimos_divida_externa", "Empréstimos — Dívida Externa"),
    _leaf("amplo", "gov_divida_ext_mercado_externo", "Dívida Externa — Mercado Externo"),
    _leaf("amplo", "gov_divida_ext_mercado_interno", "Dívida Externa — Mercado Interno"),
]
_EMPRESAS_TREE = [
    _leaf("amplo", "emp_emprestimos_sfn", "Empréstimos — Sistema Financeiro Nacional"),
    _leaf("amplo", "emp_emprestimos_osf", "Empréstimos — Outras Instituições Financeiras"),
    _leaf("amplo", "emp_emprestimos_fundos_gov", "Empréstimos — Fundos e Programas Governamentais"),
    _leaf("amplo", "emp_titulos_divida_privado", "Títulos de Dívida — Privados"),
    _leaf("amplo", "emp_titulos_divida_securitizado", "Títulos de Dívida — Securitizados"),
    _leaf("amplo", "emp_divida_externa_mercado_ext", "Dívida Externa — Mercado Externo"),
    _leaf("amplo", "emp_divida_externa_mercado_int", "Dívida Externa — Mercado Interno"),
]
_FAMILIAS_TREE = [
    _leaf("amplo", "fam_emprestimos_sfn", "Empréstimos — Sistema Financeiro Nacional"),
    _leaf("amplo", "fam_emprestimos_osf", "Empréstimos — Outras Instituições Financeiras"),
    _leaf("amplo", "fam_emprestimos_fundos_gov", "Empréstimos — Fundos e Programas Governamentais"),
    _leaf("amplo", "fam_titulos_securitizado", "Títulos Securitizados"),
    _leaf("amplo", "fam_emprestimos_divida_externa", "Empréstimos — Dívida Externa"),
]

# "total"/"governo_total"/"empresas_total"/"familias_total" sao chaves sinteticas (soma
# dos leaves acima, ver build()) -- nao existem como colunas em cred_credito_amplo.
AMPLO_TREE = [
    _group("amplo", "total", "Total (Crédito Ampliado)", [
        _group("amplo", "governo_total", "Governo", _GOVERNO_TREE),
        _group("amplo", "empresas_total", "Empresas", _EMPRESAS_TREE),
        _group("amplo", "familias_total", "Famílias", _FAMILIAS_TREE),
    ]),
]

_LEAF_KEYS_BY_SETOR = {
    "governo_total":  [n["seriesKey"] for n in _GOVERNO_TREE],
    "empresas_total": [n["seriesKey"] for n in _EMPRESAS_TREE],
    "familias_total": [n["seriesKey"] for n in _FAMILIAS_TREE],
}


def build(raw: dict, ipca_pct: dict, pib_acum_12m: dict | None = None) -> dict:
    """`raw`: {"amplo__<serie>": {"dates", "values"}} para as 17 series brutas de
    cred_credito_amplo (sem os totais sinteticos, calculados aqui). `ipca_pct`/
    `pib_acum_12m`: mesmos parametros de saldo_tab.build()."""
    raw = dict(raw)
    for setor, leaf_keys in _LEAF_KEYS_BY_SETOR.items():
        raw[f"amplo__{setor}"] = tf.sum_series(*[raw[k] for k in leaf_keys])
    raw["amplo__total"] = tf.sum_series(
        raw["amplo__governo_total"], raw["amplo__empresas_total"], raw["amplo__familias_total"]
    )

    price_index = tf.build_price_index(ipca_pct["dates"], ipca_pct["values"])
    ref_date = ipca_pct["dates"][-1]
    gdp_map = tf.to_date_map(pib_acum_12m) if pib_acum_12m is not None else None

    series = {}
    for key, s in raw.items():
        series[key] = tf.compute_variants(s["dates"], s["values"], price_index, ref_date, gdp_acum_12m=gdp_map)

    return {"tree": AMPLO_TREE, "series": series, "ref_date": ref_date}
