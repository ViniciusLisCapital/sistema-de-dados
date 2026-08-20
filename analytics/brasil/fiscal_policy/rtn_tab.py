"""
Monta o dataset da 2a tabela+grafico da aba "Receitas e Despesas": metodologia RTN
(Resultado do Tesouro Nacional, Tema 10 da API de Series Temporais do Tesouro --
fisc_rtn) ao lado da GFSM (gfsm_tab.py, ja na mesma aba) -- ver
analytics/brasil/fiscal_policy/reference/rtn_vs_efgg.md para a diferenciacao completa das
duas fontes. Mesmo padrao "tabela hierarquica + grafico" (makeHierTab() no lado JS),
mas RTN e mensal (nao trimestral) e cobre so Governo Central (nao tem corte por
esfera). Cada serie carrega as tres modelagens de Nivel lado a lado (toggle
Bruto/Trimestral/Acumulado -- ver analytics/brasil/fiscal_policy/transforms.py): Bruto reusa
analytics.brasil.credit.transforms.compute_variants() (STL mensal period=12, mesma convencao ja
usada pelas abas Saldo/Concessao do relatorio de credito); Trimestral (2026-08, adicao
explicita do usuario, para viabilizar comparacao direta com a GFSM -- ver Apendice)
usa fiscal_tf.compute_variants_quarterly_step() (soma do trimestre calendario, NAO
movel, mesmo corte que a GFSM ja usa nativamente); Acumulado usa
analytics.brasil.fiscal_policy.transforms.compute_variants_monthly_ttm() (janela TTM de 12
meses, mesma logica "acumulado" da GFSM, so a janela muda com a periodicidade).

Arvore (reestruturada 2026-08, a pedido do usuario -- "Receita liquida" como raiz, nao
mais irma de "Receita Total"): Receita Liquida (10.01.2 = Receita Total -
Transferencias) -> Receita Total (10.01.1, com seus subitens -- Receita Administrada
pela RFB [+ 8 subitens] / Arrecadacao Liquida RGPS / Incentivos Fiscais / Receitas Nao
Administradas pela RFB) + Transferencias por Reparticao de Receita (10.02.1, FPM/FPE/
IPI-EE etc.); Despesa Total (10.03.1) -> Beneficios Previdenciarios (Urbano/Rural) /
Pessoal e Encargos Sociais / Outras Despesas Obrigatorias / Despesas do Executivo
Sujeitas a Prog. Financeira (-> Obrigatorias com Controle de Fluxo / Discricionarias
por funcao -- Saude/Educacao/Defesa/Transporte/Administracao/Ciencia e Tecnologia/
Seguranca Publica/Assistencia Social/Demais); e Resultado Primario (10.04.1 = Receita
Liquida - Despesa Total, ver abaixo) -- os 3 nos-raiz da arvore.

Resultado Primario (2026-08, adicao a pedido do usuario -- "qual o problema com... faca
um double check nos numeros"): `resultado_primario_governo_central` (10.04.1, codigo STN
8055 -- serie propria publicada pelo Tesouro, Governo Central = Tesouro Nacional +
Previdencia Social + Banco Central). Confirmado ao vivo (2026-08) que essa serie e
IDENTICA, mes a mes, a `resultado_primario_acima_linha` (identidade ja computada em
fisc_rtn.py's run() = receita_liquida - despesa_total, ver docstring la) -- usa-se o
codigo oficial publicado em vez do derivado por ser a linha que o proprio Tesouro
divulga como "Resultado Primario", nao uma reconstrucao nossa (ainda que
matematicamente equivalentes aqui).

Linha default marcada no grafico: `receita_liquida` + `despesa_total` +
`resultado_primario_governo_central`, NAO `receita_total` + `despesa_total` --
`receita_total` (bruto) inclui transferencias por reparticao de receita a Estados/
Municipios (FPM/FPE) que nunca chegam a ser gasto pelo Governo Central, entao nao e
comparavel a `despesa_total` (ver Gotchas em analytics/brasil/fiscal_policy/CLAUDE.md, "RTN's
receita_total (gross) is not comparable to despesa_total"). `receita_liquida` e a linha
que de fato reconcilia com despesa.
"""
from analytics.report_structure import tree_helpers as th

_direct = th.direct

_RECEITA_ADMINISTRADA_CHILDREN = [
    _direct("imposto_de_importacao", "Imposto de Importação"),
    _direct("ipi", "IPI"),
    _direct("imposto_de_renda", "Imposto de Renda"),
    _direct("iof", "IOF"),
    _direct("cofins", "Cofins"),
    _direct("pis_pasep", "PIS/Pasep"),
    _direct("csll", "CSLL"),
    _direct("receita_da_cide_combustiveis", "CIDE Combustíveis"),
    _direct("outras_administradas_pela_rfb", "Outras Administradas pela RFB"),
]

_DISCRICIONARIAS_CHILDREN = [
    _direct("discricionarias_saude", "Saúde"),
    _direct("discricionarias_educacao", "Educação"),
    _direct("discricionarias_defesa", "Defesa"),
    _direct("discricionarias_transporte", "Transporte"),
    _direct("discricionarias_administracao", "Administração"),
    _direct("discricionarias_ciencia_e_tecnologia", "Ciência e Tecnologia"),
    _direct("discricionarias_seguranca_publica", "Segurança Pública"),
    _direct("discricionarias_assistencia_social", "Assistência Social"),
    _direct("discricionarias_demais", "Demais"),
]

_DESPESA_EXECUTIVO_CHILDREN = [
    _direct("obrigatorias_com_controle_de_fluxo", "Obrigatórias com Controle de Fluxo"),
    _direct("despesas_discricionarias_do_poder_executivo", "Discricionárias", _DISCRICIONARIAS_CHILDREN),
]

RTN_TREE = [
    _direct("receita_liquida", "Receita Líquida (Total − Transferências)", [
        _direct("receita_total", "Receita Total", [
            _direct("receita_administrada_rfb", "Receita Administrada pela RFB", _RECEITA_ADMINISTRADA_CHILDREN),
            _direct("arrecadacao_liquida_rgps", "Arrecadação Líquida para o RGPS"),
            _direct("incentivos_fiscais", "Incentivos Fiscais"),
            _direct("receitas_nao_administradas_rfb", "Receitas Não Administradas pela RFB"),
        ]),
        _direct("transferencias_reparticao_receita", "Transferências por Repartição de Receita (FPM/FPE/IPI-EE)"),
    ]),
    _direct("despesa_total", "Despesa Total", [
        _direct("beneficios_previdenciarios", "Benefícios Previdenciários", [
            _direct("beneficios_previdenciarios_urbano", "Urbano"),
            _direct("beneficios_previdenciarios_rural", "Rural"),
        ]),
        _direct("pessoal_encargos_sociais", "Pessoal e Encargos Sociais"),
        _direct("outras_despesas_obrigatorias", "Outras Despesas Obrigatórias"),
        _direct("despesas_executivo_prog_financeira", "Despesas do Executivo (Prog. Financeira)", _DESPESA_EXECUTIVO_CHILDREN),
    ]),
    _direct("resultado_primario_governo_central", "Resultado Primário (Receita Líquida − Despesa Total)"),
]

# Todos os codigos (nomes de coluna reais de fisc_rtn.name) usados na arvore acima --
# generate_report.py usa esta lista para montar `raw`.
CODES = [
    "receita_total", "receita_administrada_rfb", "imposto_de_importacao", "ipi",
    "imposto_de_renda", "iof", "cofins", "pis_pasep", "csll",
    "receita_da_cide_combustiveis", "outras_administradas_pela_rfb",
    "arrecadacao_liquida_rgps", "incentivos_fiscais", "receitas_nao_administradas_rfb",
    "transferencias_reparticao_receita", "receita_liquida", "resultado_primario_governo_central",
    "despesa_total", "beneficios_previdenciarios", "beneficios_previdenciarios_urbano",
    "beneficios_previdenciarios_rural", "pessoal_encargos_sociais",
    "outras_despesas_obrigatorias", "despesas_executivo_prog_financeira",
    "obrigatorias_com_controle_de_fluxo", "despesas_discricionarias_do_poder_executivo",
    "discricionarias_saude", "discricionarias_educacao", "discricionarias_defesa",
    "discricionarias_transporte", "discricionarias_administracao",
    "discricionarias_ciencia_e_tecnologia", "discricionarias_seguranca_publica",
    "discricionarias_assistencia_social", "discricionarias_demais",
]


def build(raw: dict, ipca_pct: dict, pib_acum_12m: dict, pib_mensal: dict) -> dict:
    """`raw`: {code: {"dates", "values"}} para todo codigo em CODES (nomes de coluna
    reais de fisc_rtn). `ipca_pct`: serie bruta {"dates", "values"} do IPCA mensal
    (inflc_agregados.ipca). `pib_acum_12m`: serie bruta {"dates", "values"} do PIB
    nominal acumulado 12m (atv_pib_mensal.pib_acum_12m, BCB SGS 4382) -- denominador do
    %PIB no nivel Acumulado (TTM/TTM). `pib_mensal`: serie bruta {"dates", "values"} do
    PIB nominal do PROPRIO mes, SEM acumular (atv_pib_mensal.pib_mensal, BCB SGS 4380,
    mesma tabela/fonte de `pib_acum_12m` -- 2026-08, adicionado para o %PIB "mesmo
    periodo" dos niveis Mensal/Trimestral, ver docstring do modulo) -- denominador do
    %PIB nos niveis Mensal e Trimestral.

    Cada serie carrega as tres modelagens de Nivel lado a lado (toggle
    Mensal/Trimestral/Acumulado 12m, ver docstring do modulo): "bruto" (Mensal) vem de
    credit_tf.compute_variants() (STL mensal, Nivel = valor bruto do proprio mes) para
    Y-Y/M-M/T-T, com "% do PIB" calculado a parte via
    fiscal_tf.compute_pct_pib_same_period() (valor do proprio mes / PIB do proprio mes,
    `pib_mensal`) -- nunca se passa `gdp_acum_12m` para credit_tf.compute_variants()
    aqui, so usamos essa funcao pelas variantes de crescimento, nao pelo pctpib nativo
    dela (que e a convencao de ESTOQUE/saldo de credito, nao serve para uma serie de
    FLUXO como receita/despesa do governo). "trimestral" vem de
    fiscal_tf.compute_variants_quarterly_step() (Nivel = soma do trimestre calendario,
    NAO movel) para Y-Y/T-T, com "% do PIB" proprio (soma do trimestre da propria serie
    / soma do trimestre do PIB, ambos via fiscal_tf.quarterly_step_level()/
    quarterly_step_map() sobre `pib_mensal`) -- NAO reusa mais o pctpib de "bruto" (ate
    2026-08 reusava; agora cada nivel tem seu proprio %PIB "mesmo periodo", ver
    docstring do modulo). "acum" vem de fiscal_tf.compute_variants_monthly_ttm() (Nivel
    = acumulado movel em 12 meses), cujo "% do PIB" continua TTM/TTM (`pib_acum_12m`,
    inalterado) -- unica modelagem de Nivel cujo %PIB nao mudou nesta reorganizacao.

    Retorna `series` chaveada diretamente pelo codigo (sem prefixo de esfera -- RTN so
    cobre Governo Central, ver docstring do modulo).
    """
    from analytics.brasil.credit import transforms as credit_tf
    from analytics.brasil.fiscal_policy import transforms as fiscal_tf

    price_index = fiscal_tf.build_price_index(ipca_pct["dates"], ipca_pct["values"])
    ref_date = ipca_pct["dates"][-1]
    gdp_ttm_map = credit_tf.to_date_map(pib_acum_12m)
    gdp_month_map = credit_tf.to_date_map(pib_mensal)
    gdp_quarter_step_map = fiscal_tf.quarterly_step_map(pib_mensal["dates"], pib_mensal["values"])

    series = {}
    for code in CODES:
        s = raw[code]
        bruto = credit_tf.compute_variants(s["dates"], s["values"], price_index, ref_date)
        bruto["pctpib"] = {"level": {
            "dates": s["dates"],
            "values": fiscal_tf.compute_pct_pib_same_period(s["dates"], s["values"], gdp_month_map),
        }}
        trimestral = fiscal_tf.compute_variants_quarterly_step(s["dates"], s["values"], price_index, ref_date)
        trimestral_step = fiscal_tf.quarterly_step_level(s["dates"], s["values"])
        trimestral["pctpib"] = {"level": {
            "dates": s["dates"],
            "values": fiscal_tf.compute_pct_pib_same_period(s["dates"], trimestral_step, gdp_quarter_step_map),
        }}
        acum = fiscal_tf.compute_variants_monthly_ttm(s["dates"], s["values"], price_index, ref_date, gdp_ttm=gdp_ttm_map)
        series[code] = {"bruto": bruto, "trimestral": trimestral, "acum": acum}

    return {"tree": RTN_TREE, "series": series, "ref_date": ref_date}
