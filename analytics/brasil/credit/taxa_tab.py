"""
Monta o dataset da aba "Taxa & Spread": duas arvores independentes (o usuario alterna
entre elas com um seletor Taxa Media | Spread, nao um toggle de metrica/base como
Saldo/Concessao) mais a Selic para sobrepor no grafico como comparacao.

Pedido explicito do usuario (2026-08): "nao precisa de muitas metricas... coloque
somente a opcao de plotar a taxa Selic junto." Por isso, ao contrario de
saldo_tab.py/concessao_tab.py, NAO ha STL/deflacao/MM3M/% PIB aqui -- taxa de juros e
spread ja sao percentuais (taxa a.a., spread em p.p.), nao fazem sentido "real" (nao se
deflaciona uma taxa pelo IPCA da mesma forma que um valor em R$) nem "% do PIB". Cada
serie e so {dates, values} bruto, sem variantes.

Duas arvores, tamanhos bem diferentes:
  TAXA_MEDIA_TREE -- mesma forma de SALDO_TREE (recurso -> segmento -> modalidade),
    lendo metrica='taxa_media' das mesmas 4 tabelas cred_modalidade_*. Cobertura de
    modalidade MENOR que saldo/concessao -- confirmado direto nos codigos SGS de cada
    script, nao assumido: nenhuma das 4 tabelas publica taxa_media para "outros"
    (catch-all), e Livre PJ/PF tambem nao tem taxa_media para cartao "a vista" (nao e
    um produto que carrega juros da mesma forma que parcelado/rotativo).
  SPREAD_TREE -- so os 7 totais recurso x segmento de cred_credito_resumo (Total/Livre/
    Direcionado x PJ/PF/Total) -- a planilha do BCB NAO publica spread por modalidade
    especifica em nenhuma tabela, so agregado. Mesma forma de arvore (2 niveis), so sem
    filhos de modalidade.
"""
from analytics.report_structure import tree_helpers as th

_leaf, _group, _direct = th.leaf, th.group, th.direct

_RESUMO_TAXA_KEYS = [
    "taxa_juros_total_total",
    "taxa_juros_livre_total", "taxa_juros_direcionado_total",
    "taxa_juros_livre_pj", "taxa_juros_livre_pf",
    "taxa_juros_direcionado_pj", "taxa_juros_direcionado_pf",
]
_RESUMO_SPREAD_KEYS = [
    "spread_total_total",
    "spread_livre_total", "spread_direcionado_total",
    "spread_livre_pj", "spread_livre_pf",
    "spread_direcionado_pj", "spread_direcionado_pf",
]

_LIVRE_PJ_TREE = [
    _group("livre_pj", "capital_de_giro_total", "Capital de Giro", [
        _leaf("livre_pj", "capital_de_giro_prazo_maior_365_dias", "Prazo > 365 dias"),
        _leaf("livre_pj", "capital_de_giro_prazo_menor_365_dias", "Prazo ≤ 365 dias"),
        _leaf("livre_pj", "capital_de_giro_teto_rotativo", "Teto Rotativo"),
    ]),
    # So 2 filhos aqui (sem "A Vista", ver docstring do modulo).
    _group("livre_pj", "cartao_de_credito_total", "Cartão de Crédito", [
        _leaf("livre_pj", "cartao_de_credito_parcelado", "Parcelado"),
        _leaf("livre_pj", "cartao_de_credito_rotativo", "Rotativo"),
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
    _leaf("livre_pj", "repasse_externo", "Repasse Externo"),
    _leaf("livre_pj", "vendor", "Vendor"),
]

_LIVRE_PF_TREE = [
    # So 2 filhos aqui (sem "A Vista", ver docstring do modulo).
    _group("livre_pf", "cartao_de_credito_total", "Cartão de Crédito", [
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
]

TAXA_MEDIA_TREE = [
    _direct("taxa_juros_total_total", "Total Geral"),
    _direct("taxa_juros_livre_total", "Livre", [
        _direct("taxa_juros_livre_pj", "Pessoa Jurídica", _LIVRE_PJ_TREE),
        _direct("taxa_juros_livre_pf", "Pessoa Física", _LIVRE_PF_TREE),
    ]),
    _direct("taxa_juros_direcionado_total", "Direcionado", [
        _direct("taxa_juros_direcionado_pj", "Pessoa Jurídica", _DIRECIONADO_PJ_TREE),
        _direct("taxa_juros_direcionado_pf", "Pessoa Física", _DIRECIONADO_PF_TREE),
    ]),
]

# So 2 niveis (recurso -> segmento) -- sem filhos de modalidade, a planilha do BCB nao
# publica spread por modalidade especifica em nenhuma tabela (ver docstring do modulo).
SPREAD_TREE = [
    _direct("spread_total_total", "Total Geral"),
    _direct("spread_livre_total", "Livre", [
        _direct("spread_livre_pj", "Pessoa Jurídica"),
        _direct("spread_livre_pf", "Pessoa Física"),
    ]),
    _direct("spread_direcionado_total", "Direcionado", [
        _direct("spread_direcionado_pj", "Pessoa Jurídica"),
        _direct("spread_direcionado_pf", "Pessoa Física"),
    ]),
]

MODALIDADE_TABLES = [
    ("livre_pj", "cred_modalidade_livre_pj"),
    ("livre_pf", "cred_modalidade_livre_pf"),
    ("direcionado_pj", "cred_modalidade_direcionado_pj"),
    ("direcionado_pf", "cred_modalidade_direcionado_pf"),
]


def resumo_taxa_keys() -> list:
    return list(_RESUMO_TAXA_KEYS)


def resumo_spread_keys() -> list:
    return list(_RESUMO_SPREAD_KEYS)


def build(raw_taxa: dict, raw_spread: dict, selic: dict) -> dict:
    """`raw_taxa`: {seriesKey: {"dates", "values"}} para toda chave de TAXA_MEDIA_TREE
    (7 series de cred_credito_resumo + 58 modalidades). `raw_spread`: idem para as 7
    chaves de SPREAD_TREE. `selic`: serie bruta {"dates", "values"}
    (cred_inadimplencia_pj.selic) para a sobreposicao no grafico. Sem STL/deflacao/
    variantes aqui (ver docstring do modulo) -- as series entram exatamente como vieram
    do banco.
    """
    return {
        "taxa_media": {"tree": TAXA_MEDIA_TREE, "series": raw_taxa},
        "spread": {"tree": SPREAD_TREE, "series": raw_spread},
        "selic": selic,
    }
