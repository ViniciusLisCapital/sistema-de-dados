"""
Monta o dataset da aba "Receitas e Despesas" (GFSM) do Panorama Fiscal: arvore
hierarquica de receita e despesa por natureza economica (classificacao GFSM 2014,
fisc_efgg) com as variantes Nivel/Y-Y/T-T x Nominal/Real/%PIB ja pre-computadas em
Python (ver analytics/fiscal_policy/transforms.py) -- mesmo padrao "tabela
hierarquica + grafico" ja usado por analytics/credit/'s saldo_tab.py/concessao_tab.py
(makeHierTab() no lado JS).

Arvore: Receita Total (1) -> Impostos (11) -> subitens (111-116); + Contribuicoes
Sociais (12)/Transferencias e Doacoes (13)/Outras Receitas (14) direto sob Receita
Total. Despesa Total (2M) -> Gasto (2) -> Remuneracao de Empregados (21) ->
Salarios e Vencimentos (211)/Contribuicoes Sociais do empregador (212); + Uso de
Bens e Servicos (22)/Consumo de Capital Fixo (23)/Juros (24)/Subsidios (25)/
Transferencias e Doacoes (26)/Beneficios Previdenciarios e Assistenciais (27)/
Outros Gastos (28) direto sob Gasto; e Investimento Liquido (31) -> Aquisicao (31.1)/
Venda (31.2)/Investimento-Consumo de Capital Fixo (31.3). Todos os nos sao codigos
GFSM reais (nenhum total sintetico por soma) -- ver domain/db/brasil/tesouro/
fisc_efgg.py para o mapa completo codigo->slug.

Corte por esfera (Uniao/Estados/Municipios/Governo Geral, 2026-08, resposta a "temos
dados para separar receitas e despesas por esfera?"): a arvore acima e a mesma para
as 4 esferas (os mesmos 27 codigos GFSM existem sob os 4 namespaces de fisc_efgg --
central_/estados_/municipios_/geral_), entao os nos da arvore usam o CODIGO GFSM NU
(sem prefixo de esfera) como seriesKey -- ex.: "receita_total", nao
"geral_receita_total". O lado JS (makeHierTab() em report.html) escolhe a esfera via
um dropdown e monta a chave de leitura combinando `esfera + "__" + code` em tempo de
render -- ver ESFERAS abaixo. Isso faz o estado de check/expand da tabela (chaveado
por `node.key` = o codigo nu) sobreviver a troca de esfera, em vez de resetar.
`build()` computa as 4 variantes (Nivel/Y-Y/T-T x Nominal/Real/%PIB) para as 4
esferas x 27 codigos = 108 series. "% do PIB" sempre divide pelo PIB TOTAL nacional
(gdp_ttm), nunca um "PIB da esfera" (nao existe tal conceito nesta base) -- mesma
convencao ja usada por _load_ieg()'s "IEG por Ente Federado" (Tabelas 8-12 do paper
Resende & Pires usam o mesmo PIB nacional como denominador tanto para Uniao quanto
Estados/Municipios).

Nota de nomenclatura: o codigo de despesa 212 ("contribuicoes_sociais", contribuicao
patronal do empregador) e o de receita 12 ("receita_contribuicoes_sociais",
arrecadacao de contribuicoes sociais) sao conceitos diferentes que compartilham
prefixo "contribuicoes sociais" -- rotulados de forma distinta na arvore
("Contribuições Sociais (Empregador)" vs. "Contribuições Sociais") para nao
confundir, mesma logica ja documentada no docstring de fisc_efgg.py. Como os slugs de
receita ja carregam o prefixo "receita_" embutido (decisao de fisc_efgg.py, para
exatamente essa razao), os codigos NUS ja saem unicos entre receita/despesa sem
trabalho extra aqui.
"""
from analytics.credit import tree_helpers as th

_direct = th.direct

_RECEITA_CHILDREN = [
    _direct("receita_impostos", "Impostos", [
        _direct("receita_impostos_renda", "Imposto de Renda"),
        _direct("receita_impostos_folha", "Impostos sobre Folha de Pagamentos"),
        _direct("receita_impostos_propriedade", "Impostos sobre Propriedade"),
        _direct("receita_impostos_bens_servicos", "Impostos sobre Bens e Serviços"),
        _direct("receita_impostos_comercio_internacional", "Impostos sobre Comércio Internacional"),
        _direct("receita_outros_impostos", "Outros Impostos"),
    ]),
    _direct("receita_contribuicoes_sociais", "Contribuições Sociais"),
    _direct("receita_transferencias_doacoes", "Transferências e Doações"),
    _direct("receita_outras_receitas", "Outras Receitas"),
]

_DESPESA_CHILDREN = [
    _direct("gasto", "Gasto Corrente", [
        _direct("remuneracao_empregados", "Remuneração de Empregados", [
            _direct("salarios_vencimentos", "Salários e Vencimentos"),
            _direct("contribuicoes_sociais", "Contribuições Sociais (Empregador)"),
        ]),
        _direct("uso_bens_servicos", "Uso de Bens e Serviços"),
        _direct("consumo_capital_fixo", "Consumo de Capital Fixo"),
        _direct("juros", "Juros"),
        _direct("subsidios", "Subsídios"),
        _direct("transferencias_doacoes", "Transferências e Doações"),
        _direct("beneficios_previdenciarios_assistenciais", "Benefícios Previdenciários e Assistenciais"),
        _direct("outros_gastos", "Outros Gastos"),
    ]),
    _direct("investimento_liquido", "Investimento Líquido", [
        _direct("aquisicao_ativos_nao_financeiros", "Aquisição de Ativos Não Financeiros"),
        _direct("venda_ativos_nao_financeiros", "Venda de Ativos Não Financeiros"),
        _direct("investimento_consumo_capital_fixo", "Investimento — Consumo de Capital Fixo"),
    ]),
]

# Nos-raiz rotulados "Receita"/"Despesa" (nao "Receita Total"/"Despesa Total" -- o
# rotulo mais curto ja deixa claro que e a raiz da arvore) -- seriesKey e o proprio
# codigo GFSM "total" nu (1/2M), sem esfera embutida (ver docstring do modulo).
GFSM_TREE = [
    _direct("receita_total", "Receita", _RECEITA_CHILDREN),
    _direct("despesa_total", "Despesa", _DESPESA_CHILDREN),
]

# Todos os codigos GFSM (nus, sem prefixo de esfera) usados na arvore -- ambas as
# raizes de GFSM_TREE reusam o mesmo codigo de _RECEITA_CHILDREN/_DESPESA_CHILDREN,
# so com uma label de linha diferente ("Receita"/"Despesa"), por isso nao aparecem
# duplicados aqui.
CODES = [
    "receita_total", "receita_impostos", "receita_impostos_renda",
    "receita_impostos_folha", "receita_impostos_propriedade",
    "receita_impostos_bens_servicos", "receita_impostos_comercio_internacional",
    "receita_outros_impostos", "receita_contribuicoes_sociais",
    "receita_transferencias_doacoes", "receita_outras_receitas",
    "despesa_total", "gasto", "remuneracao_empregados",
    "salarios_vencimentos", "contribuicoes_sociais", "uso_bens_servicos",
    "consumo_capital_fixo", "juros", "subsidios",
    "transferencias_doacoes", "beneficios_previdenciarios_assistenciais",
    "outros_gastos", "investimento_liquido", "aquisicao_ativos_nao_financeiros",
    "venda_ativos_nao_financeiros", "investimento_consumo_capital_fixo",
]

# Esferas de governo -- namespaces reais de fisc_efgg (ver domain/db/brasil/tesouro/
# fisc_efgg.py's _build_geral()). "geral" e o default (Governo Geral consolidado, o
# nivel que a aba usava antes do corte por esfera existir).
ESFERAS = ["geral", "central", "estados", "municipios"]

# {esfera}_{codigo} -- os nomes de coluna REAIS em fisc_efgg (o que generate_report.py
# le do banco). generate_report.py usa esta lista para montar `raw`.
DB_NAMES = [f"{esfera}_{code}" for esfera in ESFERAS for code in CODES]


def build(raw: dict, ipca_pct: dict, gdp_ttm: dict, gdp_same_period: dict) -> dict:
    """`raw`: {"{esfera}_{code}": {"dates": [...], "values": [...]}} para toda
    combinacao em DB_NAMES (nomes de coluna reais de fisc_efgg). `ipca_pct`: serie
    bruta {"dates", "values"} da variacao mensal do IPCA (inflc_agregados.ipca).
    `gdp_ttm`: {date: PIB acumulado em 4 trimestres} (ver generate_report.py's
    pib_4t, mesmo denominador de fisc_nfsp/IEG -- sempre o PIB NACIONAL, nao um PIB
    por esfera, para as 4 esferas igualmente) -- denominador do %PIB no nivel
    Acumulado (TTM/TTM). `gdp_same_period`: {date: PIB do PROPRIO trimestre, SEM
    acumular} (ver generate_report.py's `_load_pib_pm_raw()`, mesma serie
    `atv_pib_valores_correntes.pib_pm` que `pib_4t` rola em 4 trimestres -- 2026-08,
    adicionado para o %PIB "mesmo periodo" do nivel Trimestral, ver docstring de
    analytics/fiscal_policy/transforms.py) -- denominador do %PIB no nivel Trimestral.

    Retorna `series` chaveada por "{esfera}__{code}" (dois underscores, mesma
    convencao "{table}__{modalidade}" de analytics/credit/tree_helpers.py) -- o lado
    JS monta essa mesma chave combinando o dropdown de esfera com `node.seriesKey`
    (o codigo nu que a arvore carrega) em tempo de render. Cada serie carrega as duas
    modelagens de Nivel lado a lado (toggle Trimestral/Acumulado 12m no relatorio, ver
    analytics/fiscal_policy/transforms.py): `series[key]["bruto"]` (compute_variants(),
    Nivel = valor do proprio trimestre, %PIB = mesmo periodo) e `series[key]["acum"]`
    (compute_variants_ttm(), Nivel = acumulado em 4 trimestres, %PIB = TTM/TTM) -- o
    lado JS escolhe qual usar via `state.accum`.
    """
    from analytics.fiscal_policy import transforms as tf

    price_index = tf.build_price_index(ipca_pct["dates"], ipca_pct["values"])
    ref_date = ipca_pct["dates"][-1]

    series = {}
    for esfera in ESFERAS:
        for code in CODES:
            s = raw[f"{esfera}_{code}"]
            series[f"{esfera}__{code}"] = {
                "bruto": tf.compute_variants(s["dates"], s["values"], price_index, ref_date, gdp_same_period=gdp_same_period),
                "acum": tf.compute_variants_ttm(s["dates"], s["values"], price_index, ref_date, gdp_ttm=gdp_ttm),
            }

    return {"tree": GFSM_TREE, "series": series, "ref_date": ref_date, "esferas": ESFERAS}
