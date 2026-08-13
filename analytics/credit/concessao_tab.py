"""
Monta o dataset da aba "Concessao" do Panorama de Credito: mesma estrutura de
arvore-tabela-grafico da aba Saldo (ver saldo_tab.py), lendo metrica='concessao' em vez
de 'saldo' das mesmas 4 tabelas cred_modalidade_* + cred_credito_resumo.

Metricas diferentes da aba Saldo (decisao explicita do usuario, 2026-08): concessao e
uma serie de fluxo (novos emprestimos no mes), bem mais ruidosa mes a mes que um
estoque como saldo -- por isso a propria base ("Nivel") ja e dessazonalizada (STL) e
suavizada por media movel de 3 meses (MM3M), tanto nominal quanto real. Crescimento e
M/M e T/T (T/T = 3M/3M rolante, mesma convencao da aba Saldo) sobre essa base ja
suavizada -- sem Y/Y aqui (nao pedido para esta aba). Ver
analytics/credit/transforms.py's compute_variants_ma3().

Arvore quase identica a SALDO_TREE (mesmo recurso -> segmento -> modalidade, mesmos
rotulos PT-BR), com uma diferenca real: a planilha-fonte do BCB nao publica codigo SGS
de concessao para "cartao_de_credito_parcelado"/"cartao_de_credito_rotativo" em
Livre-PJ (Tabela 10) -- so para "cartao_de_credito_a_vista" e o total do grupo -- ao
contrario de Livre-PJ saldo (Tabela 6), que tem as 3 quebras. Confirmado direto nos
codigos SGS de cred_modalidade_livre_pj.py, nao assumido.
"""
from analytics.credit import transforms as tf
from analytics.credit import tree_helpers as th

_leaf, _group, _direct = th.leaf, th.group, th.direct

_RESUMO_CONCESSAO_KEYS = [
    "concessao_total_total",
    "concessao_livre_total", "concessao_direcionado_total",
    "concessao_livre_pj", "concessao_livre_pf",
    "concessao_direcionado_pj", "concessao_direcionado_pf",
]

_LIVRE_PJ_TREE = [
    _group("livre_pj", "capital_de_giro_total", "Capital de Giro", [
        _leaf("livre_pj", "capital_de_giro_prazo_maior_365_dias", "Prazo > 365 dias"),
        _leaf("livre_pj", "capital_de_giro_prazo_menor_365_dias", "Prazo ≤ 365 dias"),
        _leaf("livre_pj", "capital_de_giro_teto_rotativo", "Teto Rotativo"),
    ]),
    # So 1 filho aqui -- ver docstring do modulo (Tabela 10 nao tem parcelado/rotativo).
    _group("livre_pj", "cartao_de_credito_total", "Cartão de Crédito", [
        _leaf("livre_pj", "cartao_de_credito_a_vista", "À Vista"),
    ]),
    _leaf("livre_pj", "acc", "ACC (Adiantamento de Contrato de Câmbio)"),
    _leaf("livre_pj", "antecipacao_de_faturas_de_cartao", "Antecipação de Faturas de Cartão"),
    _leaf("livre_pj", "aquisicao_de_outros_bens", "Aquisição de Outros Bens"),
    _leaf("livre_pj", "aquisicao_de_veiculos", "Aquisição de Veículos"),
    _leaf("livre_pj", "arrendamento_mercantil_outros_bens", "Arrendamento Mercantil — Outros Bens"),
    _leaf("livre_pj", "arrendamento_mercantil_veiculos", "Arrendamento Mercantil — Veículos"),
    _leaf("livre_pj", "cheque_especial", "Cheque Especial"),
    _leaf("livre_pj", "compror", "Compror"),
    _leaf("livre_pj", "conta_garantida", "Conta Garantida"),
    _leaf("livre_pj", "desconto_de_cheques", "Desconto de Cheques"),
    _leaf("livre_pj", "desconto_de_duplicatas_e_recebiveis", "Desconto de Duplicatas e Recebíveis"),
    _leaf("livre_pj", "financiamento_exportacoes", "Financiamento a Exportações"),
    _leaf("livre_pj", "financiamento_importacoes", "Financiamento a Importações"),
    _leaf("livre_pj", "outros", "Outros"),
    _leaf("livre_pj", "repasse_externo", "Repasse Externo"),
    _leaf("livre_pj", "vendor", "Vendor"),
]

_LIVRE_PF_TREE = [
    _group("livre_pf", "cartao_de_credito_total", "Cartão de Crédito", [
        _leaf("livre_pf", "cartao_de_credito_a_vista", "À Vista"),
        _leaf("livre_pf", "cartao_de_credito_parcelado", "Parcelado"),
        _leaf("livre_pf", "cartao_de_credito_rotativo", "Rotativo"),
    ]),
    _group("livre_pf", "credito_pessoal_consignado_total", "Crédito Pessoal Consignado", [
        _leaf("livre_pf", "credito_pessoal_consignado_beneficiarios_do_inss", "Beneficiários do INSS"),
        _leaf("livre_pf", "credito_pessoal_consignado_servidores_publicos", "Servidores Públicos"),
        _leaf("livre_pf", "credito_pessoal_consignado_trabalhadores_setor_privado", "Trabalhadores do Setor Privado"),
    ]),
    _group("livre_pf", "credito_pessoal_nao_consignado_total", "Crédito Pessoal Não Consignado", [
        _leaf("livre_pf", "credito_pessoal_nao_consignado_com_garantias", "Com Garantias"),
        _leaf("livre_pf", "credito_pessoal_nao_consignado_sem_garantias", "Sem Garantias"),
    ]),
    _leaf("livre_pf", "aquisicao_de_outros_bens", "Aquisição de Outros Bens"),
    _leaf("livre_pf", "aquisicao_de_veiculos", "Aquisição de Veículos"),
    _leaf("livre_pf", "arrendamento_mercantil_outros_bens", "Arrendamento Mercantil — Outros Bens"),
    _leaf("livre_pf", "arrendamento_mercantil_veiculos", "Arrendamento Mercantil — Veículos"),
    _leaf("livre_pf", "cheque_especial", "Cheque Especial"),
    _leaf("livre_pf", "composicao_de_dividas", "Composição de Dívidas"),
    _leaf("livre_pf", "desconto_de_cheques", "Desconto de Cheques"),
    _leaf("livre_pf", "outros", "Outros"),
    _leaf("livre_pf", "total_nao_rotativo", "Total Não Rotativo"),
    _leaf("livre_pf", "total_rotativo", "Total Rotativo"),
]

_DIRECIONADO_PJ_TREE = [
    _group("direcionado_pj", "credito_com_recursos_do_bndes_total", "Crédito com Recursos do BNDES", [
        _leaf("direcionado_pj", "credito_com_recursos_do_bndes_capital_de_giro", "Capital de Giro"),
        _leaf("direcionado_pj", "credito_com_recursos_do_bndes_financiamento_a_investimentos", "Financiamento a Investimentos"),
        _leaf("direcionado_pj", "credito_com_recursos_do_bndes_financiamento_agroindustrial", "Financiamento Agroindustrial"),
    ]),
    _group("direcionado_pj", "credito_rural_total", "Crédito Rural", [
        _leaf("direcionado_pj", "credito_rural_taxas_de_mercado", "Taxas de Mercado"),
        _leaf("direcionado_pj", "credito_rural_taxas_reguladas", "Taxas Reguladas"),
    ]),
    _group("direcionado_pj", "financiamentos_imobiliarios_total", "Financiamentos Imobiliários", [
        _leaf("direcionado_pj", "financiamentos_imobiliarios_taxas_de_mercado", "Taxas de Mercado"),
        _leaf("direcionado_pj", "financiamentos_imobiliarios_taxas_reguladas", "Taxas Reguladas"),
    ]),
    _leaf("direcionado_pj", "outros", "Outros"),
    _leaf("direcionado_pj", "programas_mpme", "Programas MPME"),
]

_DIRECIONADO_PF_TREE = [
    _group("direcionado_pf", "credito_com_recursos_do_bndes_total", "Crédito com Recursos do BNDES", [
        _leaf("direcionado_pf", "credito_com_recursos_do_bndes_financiamento_agroindustrial", "Financiamento Agroindustrial"),
    ]),
    _group("direcionado_pf", "credito_rural_total", "Crédito Rural", [
        _leaf("direcionado_pf", "credito_rural_taxas_de_mercado", "Taxas de Mercado"),
        _leaf("direcionado_pf", "credito_rural_taxas_reguladas", "Taxas Reguladas"),
    ]),
    _group("direcionado_pf", "financiamentos_imobiliarios_total", "Financiamentos Imobiliários", [
        _leaf("direcionado_pf", "financiamentos_imobiliarios_taxas_de_mercado", "Taxas de Mercado"),
        _leaf("direcionado_pf", "financiamentos_imobiliarios_taxas_reguladas", "Taxas Reguladas"),
    ]),
    _leaf("direcionado_pf", "microcredito", "Microcrédito"),
    _leaf("direcionado_pf", "outros", "Outros"),
]

CONCESSAO_TREE = [
    _direct("concessao_total_total", "Total Geral"),
    _direct("concessao_livre_total", "Livre", [
        _direct("concessao_livre_pj", "Pessoa Jurídica", _LIVRE_PJ_TREE),
        _direct("concessao_livre_pf", "Pessoa Física", _LIVRE_PF_TREE),
    ]),
    _direct("concessao_direcionado_total", "Direcionado", [
        _direct("concessao_direcionado_pj", "Pessoa Jurídica", _DIRECIONADO_PJ_TREE),
        _direct("concessao_direcionado_pf", "Pessoa Física", _DIRECIONADO_PF_TREE),
    ]),
]

# Mesmas 4 tabelas da aba Saldo, agora filtradas por metrica='concessao'.
MODALIDADE_TABLES = [
    ("livre_pj", "cred_modalidade_livre_pj"),
    ("livre_pf", "cred_modalidade_livre_pf"),
    ("direcionado_pj", "cred_modalidade_direcionado_pj"),
    ("direcionado_pf", "cred_modalidade_direcionado_pf"),
]


def resumo_concessao_keys() -> list:
    return list(_RESUMO_CONCESSAO_KEYS)


def build(raw: dict, ipca_pct: dict, pib_acum_12m: dict | None = None) -> dict:
    """`raw`: {seriesKey: {"dates": [...], "values": [...]}} para toda chave usada em
    CONCESSAO_TREE (7 series de cred_credito_resumo + 65 modalidades — 2 a menos que
    saldo_tab, ver docstring do modulo). `ipca_pct`: serie bruta {"dates", "values"} da
    variacao mensal do IPCA (inflc_agregados.ipca). `pib_acum_12m`: serie bruta
    {"dates", "values"} do PIB acumulado 12m (atv_pib_mensal.pib_acum_12m) — se
    omitido, a variante "% do PIB" nao e calculada.
    """
    price_index = tf.build_price_index(ipca_pct["dates"], ipca_pct["values"])
    ref_date = ipca_pct["dates"][-1]
    gdp_map = tf.to_date_map(pib_acum_12m) if pib_acum_12m is not None else None

    series = {}
    for key, s in raw.items():
        series[key] = tf.compute_variants_ma3(s["dates"], s["values"], price_index, ref_date, gdp_acum_12m=gdp_map)

    return {"tree": CONCESSAO_TREE, "series": series, "ref_date": ref_date}
