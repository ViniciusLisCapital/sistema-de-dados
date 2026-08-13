"""
Monta o dataset da aba "Saldo" do Panorama de Credito: arvore hierarquica de
modalidades de credito (Livre/Direcionado x PJ/PF x modalidade especifica) mais os
totais de cada nivel, com todas as variantes Nivel/Y-o-Y/M-o-M(SA)/T-o-T(SA) x
Nominal/Real ja pre-computadas em Python (ver analytics/credit/transforms.py) — o
toggle no browser so troca qual variante ja calculada e exibida, sem reimplementar
STL/deflacao em JS.

Arvore: recurso (Livre/Direcionado) -> segmento (PJ/PF) -> modalidade. Dentro de
cada segmento, uma modalidade vira um no "grupo" (com filhos expansiveis) SO quando
existe um codigo SGS proprio de "total" para aquele agrupamento na planilha-fonte do
BCB (capital_de_giro_total, cartao_de_credito_total etc. — ver
analytics/credit/fontes_dados.md) — nunca se soma series de crescimento/percentual
para fabricar um total sintetico. Modalidades sem um "total" agregador (ex:
arrendamento_mercantil_outros_bens/veiculos) ficam como folhas soltas, sem pai
artificial.
"""
from analytics.credit import transforms as tf
from analytics.credit import tree_helpers as th

_RESUMO_SALDO_KEYS = [
    "saldo_total_total",
    "saldo_livre_total", "saldo_direcionado_total",
    "saldo_livre_pj", "saldo_livre_pf",
    "saldo_direcionado_pj", "saldo_direcionado_pf",
]

# Aliases -- ver analytics/credit/tree_helpers.py (compartilhado com concessao_tab.py).
_leaf, _group, _direct = th.leaf, th.group, th.direct


_LIVRE_PJ_TREE = [
    _group("livre_pj", "capital_de_giro_total", "Capital de Giro", [
        _leaf("livre_pj", "capital_de_giro_prazo_maior_365_dias", "Prazo > 365 dias"),
        _leaf("livre_pj", "capital_de_giro_prazo_menor_365_dias", "Prazo ≤ 365 dias"),
        _leaf("livre_pj", "capital_de_giro_teto_rotativo", "Teto Rotativo"),
    ]),
    _group("livre_pj", "cartao_de_credito_total", "Cartão de Crédito", [
        _leaf("livre_pj", "cartao_de_credito_a_vista", "À Vista"),
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

# ── Por Porte de Empresa (PJ) — cred_credito_porte, metrica='saldo' (so mpme/grande,
# sem codigo de "total" -- ver docstring do modulo desse script). "porte__total" e uma
# SOMA (mpme+grande), nao um codigo SGS -- valida porque e soma de NIVEL (R$), nao de
# crescimento/percentual (ver docstring do modulo). Inadimplencia e os 2 cortes de
# saldo_maior_risco dessa mesma tabela ficam de fora aqui por pedido explicito do
# usuario (2026-08) -- vao para uma futura aba Inadimplencia, nao para o Saldo.
_PORTE_TREE = [
    _leaf("porte", "mpme", "MPME"),
    _leaf("porte", "grande", "Grande"),
]

# ── Por Atividade Economica (PJ) — cred_credito_atividade_economica, unica metrica
# (saldo), tabela (date, name, value) simples -- ver docstring do modulo desse script.
# "ativ__total" (soma dos 4 ramos abaixo) e sintetico pelo mesmo motivo de
# "porte__total" acima. industria_total/servicos_total/servicos_comercio/
# servicos_transportes_total SAO codigos SGS reais (nao sinteticos).
_ATIVIDADE_INDUSTRIA_TREE = [
    _leaf("ativ", "industria_siup", "SIUP (Energia, Água e Saneamento)"),
    _leaf("ativ", "industria_construcao", "Construção"),
    _leaf("ativ", "industria_alimentos", "Alimentos"),
    _leaf("ativ", "industria_acucar", "Açúcar"),
    _leaf("ativ", "industria_textil_vestuario_couro_calcados", "Têxtil, Vestuário, Couro e Calçados"),
    _leaf("ativ", "industria_papel_celulose", "Papel e Celulose"),
    _leaf("ativ", "industria_petroleo_gas_alcool", "Petróleo, Gás e Álcool"),
    _leaf("ativ", "industria_metalurgia_siderurgia", "Metalurgia e Siderurgia"),
    _leaf("ativ", "industria_quimica_farmaceutica", "Química e Farmacêutica"),
    _leaf("ativ", "industria_bens_capital", "Bens de Capital"),
    _leaf("ativ", "industria_automobilistica", "Automobilística"),
    _leaf("ativ", "industria_mineracao", "Mineração"),
    _leaf("ativ", "industria_obras_infraestrutura", "Obras de Infraestrutura"),
    _leaf("ativ", "industria_outros_bens_consumo_duraveis", "Outros Bens de Consumo Duráveis"),
    _leaf("ativ", "industria_embalagens", "Embalagens"),
    _leaf("ativ", "industria_bens_consumo_nao_duraveis", "Bens de Consumo Não Duráveis"),
]
_ATIVIDADE_SERVICOS_TREE = [
    _group("ativ", "servicos_transportes_total", "Transportes", [
        _leaf("ativ", "servicos_transportes_via_terrestre_carga_passageiro", "Via Terrestre (Carga e Passageiro)"),
        _leaf("ativ", "servicos_transportes_meios_aquaviario_aereo", "Aquaviário e Aéreo"),
        _leaf("ativ", "servicos_transportes_dutoviario", "Dutoviário"),
    ]),
    _group("ativ", "servicos_comercio", "Comércio", [
        _leaf("ativ", "servicos_comercio_varejo_bens_nao_duraveis", "Varejo — Bens Não Duráveis"),
        _leaf("ativ", "servicos_comercio_varejo_bens_duraveis", "Varejo — Bens Duráveis"),
        _leaf("ativ", "servicos_comercio_atacado_bens_duraveis_nao_duraveis", "Atacado — Bens Duráveis e Não Duráveis"),
        _leaf("ativ", "servicos_comercio_geral_veiculos_automotores", "Geral — Veículos Automotores"),
        _leaf("ativ", "servicos_comercio_geral_bens_intermediarios", "Geral — Bens Intermediários"),
        _leaf("ativ", "servicos_comercio_geral_bens_capital", "Geral — Bens de Capital"),
    ]),
    _leaf("ativ", "servicos_administracao_publica", "Administração Pública"),
    _leaf("ativ", "servicos_imobiliarios", "Imobiliários"),
    _leaf("ativ", "servicos_informacao_comunicacao", "Informação e Comunicação"),
    _leaf("ativ", "servicos_demais_prestados_familias", "Demais Prestados a Famílias"),
    _leaf("ativ", "servicos_demais_prestados_empresas", "Demais Prestados a Empresas"),
    _leaf("ativ", "servicos_financeiros", "Financeiros"),
    _leaf("ativ", "servicos_outros", "Outros"),
]
_ATIVIDADE_TREE = [
    _leaf("ativ", "agropecuaria", "Agropecuária"),
    _group("ativ", "industria_total", "Indústria", _ATIVIDADE_INDUSTRIA_TREE),
    _group("ativ", "servicos_total", "Serviços", _ATIVIDADE_SERVICOS_TREE),
    _leaf("ativ", "outros", "Outros"),
]

# ── Por Tipo de Cliente — cred_credito_tipo_cliente, unica metrica (saldo). "total"
# dessa tabela e o MESMO codigo SGS de saldo_total_total (ver docstring do modulo
# desse script) -- reusa a serie ja computada (`key=` distinto de `seriesKey`, ver
# tree_helpers.direct()) em vez de recarregar/reprocessar o mesmo dado.
_TIPO_CLIENTE_TREE = [
    _direct("tipocliente__setor_privado_total", "Setor Privado", [
        _leaf("tipocliente", "setor_privado_pj", "Pessoa Jurídica"),
        _leaf("tipocliente", "setor_privado_pf", "Pessoa Física"),
    ]),
    _direct("tipocliente__setor_publico_total", "Setor Público", [
        _leaf("tipocliente", "setor_publico_governo_federal", "Governo Federal"),
        _leaf("tipocliente", "setor_publico_governos_estaduais_municipais", "Governos Estaduais e Municipais"),
    ]),
]

SALDO_TREE = [
    _direct("saldo_total_total", "Total Geral"),
    _direct("saldo_livre_total", "Livre", [
        _direct("saldo_livre_pj", "Pessoa Jurídica", _LIVRE_PJ_TREE),
        _direct("saldo_livre_pf", "Pessoa Física", _LIVRE_PF_TREE),
    ]),
    _direct("saldo_direcionado_total", "Direcionado", [
        _direct("saldo_direcionado_pj", "Pessoa Jurídica", _DIRECIONADO_PJ_TREE),
        _direct("saldo_direcionado_pf", "Pessoa Física", _DIRECIONADO_PF_TREE),
    ]),
    _group("porte", "total", "Por Porte de Empresa (PJ)", _PORTE_TREE),
    _group("ativ", "total", "Por Atividade Econômica (PJ)", _ATIVIDADE_TREE),
    _direct("saldo_total_total", "Por Tipo de Cliente", _TIPO_CLIENTE_TREE, key="tipocliente__total"),
]

# Tabelas de modalidade (metrica='saldo') e o prefixo de chave correspondente na arvore.
MODALIDADE_TABLES = [
    ("livre_pj", "cred_modalidade_livre_pj"),
    ("livre_pf", "cred_modalidade_livre_pf"),
    ("direcionado_pj", "cred_modalidade_direcionado_pj"),
    ("direcionado_pf", "cred_modalidade_direcionado_pf"),
]

# Tabela (date, porte, metrica, value) -- so metrica='saldo' entra na aba Saldo.
PORTE_TABLE = ("porte", "cred_credito_porte")

# Tabela (date, name, value) simples -- unica metrica, sem filtro de metrica/modalidade.
ATIVIDADE_ECONOMICA_TABLE = ("ativ", "cred_credito_atividade_economica")

# Idem, tipo de cliente -- "total" (=saldo_total_total) e excluido do carregamento em
# generate_report.py (ja vem do grupo `resumo`), so as 6 chaves reais desta tabela.
TIPO_CLIENTE_TABLE = ("tipocliente", "cred_credito_tipo_cliente")
TIPO_CLIENTE_KEYS_EXCLUDING_TOTAL = [
    "setor_privado_pj", "setor_privado_pf", "setor_privado_total",
    "setor_publico_governo_federal", "setor_publico_governos_estaduais_municipais", "setor_publico_total",
]


def resumo_saldo_keys() -> list:
    return list(_RESUMO_SALDO_KEYS)


def build(raw: dict, ipca_pct: dict, pib_acum_12m: dict | None = None) -> dict:
    """`raw`: {seriesKey: {"dates": [...], "values": [...]}} para toda chave usada em
    SALDO_TREE, EXCETO os 2 totais sinteticos ("porte__total", "ativ__total"), que este
    metodo calcula por soma antes de rodar compute_variants() (ver comentarios da
    arvore acima). `ipca_pct`: serie bruta {"dates", "values"} da variacao mensal do
    IPCA (inflc_agregados.ipca). `pib_acum_12m`: serie bruta {"dates", "values"} do PIB
    acumulado 12m (atv_pib_mensal.pib_acum_12m) — se omitido, a variante "% do PIB" nao
    e calculada.
    """
    raw = dict(raw)
    raw["porte__total"] = tf.sum_series(raw["porte__mpme"], raw["porte__grande"])
    raw["ativ__total"] = tf.sum_series(
        raw["ativ__agropecuaria"], raw["ativ__industria_total"], raw["ativ__servicos_total"], raw["ativ__outros"]
    )

    price_index = tf.build_price_index(ipca_pct["dates"], ipca_pct["values"])
    ref_date = ipca_pct["dates"][-1]
    gdp_map = tf.to_date_map(pib_acum_12m) if pib_acum_12m is not None else None

    series = {}
    for key, s in raw.items():
        series[key] = tf.compute_variants(s["dates"], s["values"], price_index, ref_date, gdp_acum_12m=gdp_map)

    return {"tree": SALDO_TREE, "series": series, "ref_date": ref_date}
