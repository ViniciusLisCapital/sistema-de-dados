"""
Monta o dataset da aba "Inadimplencia": reune inadimplencia (carteira em atraso >90d,
%) de TODOS os cortes que a publicam -- nao so a serie dedicada PJ
(cred_inadimplencia_pj) -- mais o corte de "saldo de maior risco" por porte de
empresa (classificacao de rating, nao inadimplencia realizada). Mesmo padrao bespoke
de taxa_tab.py (sem STL/deflacao/% PIB/variantes -- ja e um percentual, cada serie e
so {dates, values} bruto), mas com uma unica arvore (nao ha selecao Taxa|Spread aqui).

Cortes com inadimplencia disponiveis, todos incluidos:
  - cred_credito_resumo: inadimplencia_{recurso}_{segmento}, recurso=total/livre/
    direcionado x segmento=pj/pf/total (Tabelas 3-5) -- "Total Geral"/"Livre"/
    "Direcionado" da arvore.
  - cred_modalidade_{livre,direcionado}_{pj,pf}: inadimplencia por modalidade
    especifica (Tabelas 19-22) -- filhos de cada segmento acima. Cobertura de
    modalidade MENOR que Saldo/Concessao, confirmado direto nos codigos SGS de cada
    tabela (nao assumido a partir da arvore de Saldo):
      * livre_pj: "cartao_de_credito" e um UNICO codigo (sem quebra a_vista/
        parcelado/rotativo/total que Saldo tem).
      * livre_pf: "cartao_de_credito_total" so tem 2 filhos (parcelado/rotativo,
        sem "a vista"); sem os leaves "total_nao_rotativo"/"total_rotativo" que
        Saldo tem.
      * direcionado_pj/direcionado_pf: identica a Saldo/Taxa Media.
  - cred_credito_porte: inadimplencia (so MPMe/Grande, SEM codigo de total) --
    grupo "Por Porte de Empresa (PJ)", so cabecalho/expansor (sem serie propria --
    ver nota abaixo).
  - cred_credito_controle_capital: inadimplencia (publicas/privadas_nacionais/
    estrangeiras, SEM codigo de total) -- grupo "Por Controle de Capital", mesmo
    tratamento de cabecalho.
  - cred_inadimplencia_pj: atraso_pj (carteira em atraso 15-90 dias, PJ) -- metrica
    DIFERENTE de inadimplencia (>90d), mantida como leaf complementar separada, nao
    misturada com inadimplencia_total_pj (que ja vem do resumo acima, mesmo codigo
    SGS 21083 usado por cred_inadimplencia_pj.inadimplencia_pj).

Nos "cabecalho" (Por Porte de Empresa, Por Controle de Capital): nenhuma das duas
tabelas publica um codigo SGS de total para a metrica 'inadimplencia' (so para
saldo_maior_risco* -- ver abaixo), e inadimplencia e uma RAZAO (carteira em atraso /
carteira total) -- somar razoes de grupos diferentes nao e matematicamente valido
(diferente de somar NIVEL em R$, ver saldo_tab.py). Por isso esses 2 grupos usam uma
seriesKey que deliberadamente NAO existe em `series` (sufixo "_header") -- puro no
organizador/expansor, sem linha de dados propria. O JS trata isso maniendo o grupo
sem checkbox (sem dado para plotar), so com o triangulo de expandir/colapsar.

Saldo de Maior Risco (por Porte) -- ATENCAO, quebra de metodologia: a partir de uma
certa data (ver Apendice do relatorio para a data observada ao vivo nos dados), o BCB
trocou a classificacao de risco de carteira da Resolucao CMN 2.682 para a Resolucao
CMN 4.966 -- sao DUAS series com codigos SGS DIFERENTES publicadas lado a lado (nao
uma serie continua que mudou de codigo), exatamente como aparecem na planilha-fonte
do BCB (colunas "Saldo de maior risco (3)" vs "Saldo de maior risco (4) -- Res.
4.966"). Mantidas aqui como DOIS grupos de topo INDEPENDENTES -- nunca concatenadas/
emendadas numa serie so, o que fabricaria uma quebra de nivel artificial no grafico.
Ao contrario dos 2 grupos acima, esta tabela TEM codigo de total proprio para as 3
combinacoes (MPMe/Grande/Total), para as duas metodologias -- nao e soma sintetica.
"""
from analytics.report_structure import tree_helpers as th

_leaf, _group, _direct = th.leaf, th.group, th.direct

_RESUMO_INADIMPLENCIA_KEYS = [
    "inadimplencia_total_total",
    "inadimplencia_livre_total", "inadimplencia_direcionado_total",
    "inadimplencia_livre_pj", "inadimplencia_livre_pf",
    "inadimplencia_direcionado_pj", "inadimplencia_direcionado_pf",
]

_LIVRE_PJ_TREE = [
    _group("livre_pj", "capital_de_giro_total", "Capital de Giro", [
        _leaf("livre_pj", "capital_de_giro_prazo_maior_365_dias", "Prazo > 365 dias"),
        _leaf("livre_pj", "capital_de_giro_prazo_menor_365_dias", "Prazo ≤ 365 dias"),
        _leaf("livre_pj", "capital_de_giro_teto_rotativo", "Teto Rotativo"),
    ]),
    # Unico codigo para cartao aqui (sem quebra a_vista/parcelado/rotativo -- ver docstring do modulo).
    _leaf("livre_pj", "cartao_de_credito", "Cartão de Crédito"),
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
    # So 2 filhos aqui (parcelado/rotativo, sem "a vista" -- ver docstring do modulo).
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
    _leaf("livre_pf", "outros", "Outros"),
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

INADIMPLENCIA_TREE = [
    _direct("inadimplencia_total_total", "Total Geral"),
    _leaf("pj", "atraso_pj", "Atraso 15–90 dias (PJ, complementar)"),
    _direct("inadimplencia_livre_total", "Livre", [
        _direct("inadimplencia_livre_pj", "Pessoa Jurídica", _LIVRE_PJ_TREE),
        _direct("inadimplencia_livre_pf", "Pessoa Física", _LIVRE_PF_TREE),
    ]),
    _direct("inadimplencia_direcionado_total", "Direcionado", [
        _direct("inadimplencia_direcionado_pj", "Pessoa Jurídica", _DIRECIONADO_PJ_TREE),
        _direct("inadimplencia_direcionado_pf", "Pessoa Física", _DIRECIONADO_PF_TREE),
    ]),
    # Cabecalho puro (sem serie propria -- ver docstring do modulo): "porte___header"
    # nunca existe em `series`, o JS renderiza sem checkbox, so o expand/colapsar.
    _group("porte", "_header", "Por Porte de Empresa (PJ)", [
        _leaf("porte", "mpme", "MPME"),
        _leaf("porte", "grande", "Grande"),
    ]),
    _group("controle", "_header", "Por Controle de Capital", [
        _leaf("controle", "publicas", "Instituições Públicas"),
        _leaf("controle", "privadas_nacionais", "Privadas Nacionais"),
        _leaf("controle", "estrangeiras", "Estrangeiras"),
    ]),
    # Saldo de Maior Risco -- 2 grupos independentes, NUNCA emendar (ver docstring do
    # modulo). Ao contrario dos 2 grupos acima, aqui "total" e um codigo SGS real.
    _group("riscoant", "total", "Saldo de Maior Risco — Metodologia Anterior (Res. CMN 2.682)", [
        _leaf("riscoant", "mpme", "MPME"),
        _leaf("riscoant", "grande", "Grande"),
    ]),
    _group("riscores4966", "total", "Saldo de Maior Risco — Nova Metodologia (Res. CMN 4.966)", [
        _leaf("riscores4966", "mpme", "MPME"),
        _leaf("riscores4966", "grande", "Grande"),
    ]),
]

# Tabelas de modalidade (metrica='inadimplencia') e o prefixo de chave correspondente.
MODALIDADE_TABLES = [
    ("livre_pj", "cred_modalidade_livre_pj"),
    ("livre_pf", "cred_modalidade_livre_pf"),
    ("direcionado_pj", "cred_modalidade_direcionado_pj"),
    ("direcionado_pf", "cred_modalidade_direcionado_pf"),
]

# Tabela (date, porte, metrica, value) -- metrica='inadimplencia' (so mpme/grande).
PORTE_TABLE = ("porte", "cred_credito_porte")
# Tabela (date, controle, metrica, value) -- metrica='inadimplencia'.
CONTROLE_TABLE = ("controle", "cred_credito_controle_capital")
# Mesma tabela de PORTE_TABLE, metricas diferentes -- ver "Saldo de Maior Risco" acima.
RISCO_ANTERIOR_TABLE = ("riscoant", "cred_credito_porte")
RISCO_RES4966_TABLE = ("riscores4966", "cred_credito_porte")


def resumo_inadimplencia_keys() -> list:
    return list(_RESUMO_INADIMPLENCIA_KEYS)


def build(raw: dict, selic: dict) -> dict:
    """`raw`: {seriesKey: {"dates", "values"}} para toda chave usada em
    INADIMPLENCIA_TREE que tem dado real (os 2 nos-cabecalho "porte___header"/
    "controle___header" nao entram aqui, de proposito -- ver docstring do modulo).
    `selic`: serie bruta {"dates", "values"} (cred_inadimplencia_pj.selic) para a
    sobreposicao no grafico. Sem STL/deflacao/variantes (ja e um percentual) -- cada
    serie entra exatamente como veio do banco.
    """
    return {"tree": INADIMPLENCIA_TREE, "series": raw, "selic": selic}
