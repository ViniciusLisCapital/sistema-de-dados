"""
RTN - Resultado do Tesouro Nacional (Governo Central, "acima da linha" e
"abaixo da linha"), Secretaria do Tesouro Nacional.

164 series do Tema 10 ("Resultado Fiscal do Governo Central - Valores
Mensais") da API de Series Temporais do Tesouro Nacional -- ver
connectors/tesouro_series_temporais.py. R$ milhoes, valores correntes,
mensal desde 1997-01. Subtemas 10.01-10.09 (Receitas, Transferencias,
Despesas, Resultado Primario, Ajustes Metodologicos, Discrepancia
Estatistica, Resultado Primario Abaixo da Linha, Juros Nominais, Resultado
Nominal) -- 10.99 (Itens de Memorando) fica de fora por ora, ver Pending em
analytics/fiscal_policy/CLAUDE.md.

Substitui a versao anterior (18 linhas via parsing de Excel, aba "1.1"
Resumida do workbook RTN, connectors/tesouro.py) por uma fonte mais rica:
cada linha do workbook resumido tinha uma so serie; a API expoe a mesma
informacao decomposta ate o 4o/5o nivel (ex: receita_administrada_rfb se
decompoe em imposto_de_importacao, ipi (e subitens por produto), imposto_de_
renda (e subitens IRPF/IRPJ/IRRF), cofins, csll etc.).

Os 17 nomes ja usados por analytics/fiscal_policy/report.html foram
preservados exatamente (mesma string, mesmo significado) para nao quebrar o
relatorio -- so a fonte por tras de cada um mudou de "linha de Excel" para
"id de serie". A 18a linha do formato antigo, resultado_primario_acima_linha
(a antiga linha "5." do workbook, "(3-4)"), nao tem serie propria equivalente
nessa API -- o subtema 10.07 e explicitamente "abaixo da linha" -- por isso
continua computada aqui mesmo, como receita_liquida - despesa_total, a mesma
identidade ja validada (ver Gotchas em analytics/fiscal_policy/CLAUDE.md).

Complementa fisc_nfsp.py (BCB SGS): RTN cobre so o Governo Central com o
detalhe de receita/despesa por rubrica; NFSP cobre o setor publico consolidado
(+ Estados/Municipios + Empresas Estatais) mas so o resultado agregado.

Banco: macro_brasil.fisc_rtn -- PRIMARY KEY (date, name). Coluna `name`
precisa ser VARCHAR(100), nao VARCHAR(60) como na versao anterior -- o rotulo
mais longo entre as 164 series (beneficios_de_prestacao_continuada_da_loas_
rmv_sentencas_judiciais_e_precatorios) tem 80 caracteres. ALTER TABLE
executado antes da primeira carga com essa versao do script.
"""

import os

import pandas as pd

from connectors.mysql import backup_table_before_truncate, insert_data_into_database, truncate_table
from connectors.tesouro_series_temporais import SeriesTemporais

_DATABASE = "macro_brasil"
_TABLE = "fisc_rtn"
_BACKUP_DIR = os.path.join(os.path.dirname(__file__), "_backups")

_LINE_ITEMS = {

    # --- 10.01 Receitas ---
    "receita_total": 7922,                      # 10.01.1 Receita Total
    "receita_administrada_rfb": 7923,           # 10.01.1.1 Receita Administrada pela Receita Federal do Brasil
    "imposto_de_importacao": 7924,              # 10.01.1.1.01 Imposto de Importação
    "ipi": 7925,                                # 10.01.1.1.02 IPI
    "ipi_fumo": 7926,                           # 10.01.1.1.02.1 IPI - Fumo
    "ipi_bebidas": 7927,                        # 10.01.1.1.02.2 IPI - Bebidas
    "ipi_automoveis": 7928,                     # 10.01.1.1.02.3 IPI - Automóveis
    "ipi_vinculado_a_importacao": 7929,         # 10.01.1.1.02.4 IPI - Vinculado a importação
    "ipi_outros": 7930,                         # 10.01.1.1.02.5 IPI - Outros
    "imposto_de_renda": 7931,                   # 10.01.1.1.03 Imposto de Renda
    "i_r_pessoa_fisica": 7932,                  # 10.01.1.1.03.1 I.R. - Pessoa Física
    "i_r_pessoa_juridica": 7933,                # 10.01.1.1.03.2 I.R. - Pessoa Jurídica
    "i_r_retido_na_fonte_irrf": 7934,           # 10.01.1.1.03.3 I.R. - Retido na fonte (IRRF)
    "irrf_rendimentos_do_trabalho": 7935,       # 10.01.1.1.03.3.1 IRRF - Rendimentos do Trabalho
    "irrf_rendimentos_do_capital": 7936,        # 10.01.1.1.03.3.2 IRRF - Rendimentos do Capital
    "irrf_remessas_ao_exterior": 7937,          # 10.01.1.1.03.3.3 IRRF - Remessas ao Exterior
    "irrf_outros_rendimentos": 7938,            # 10.01.1.1.03.3.4 IRRF - Outros Rendimentos
    "iof": 7939,                                # 10.01.1.1.04 IOF
    "cofins": 7940,                             # 10.01.1.1.05 Cofins
    "pis_pasep": 7941,                          # 10.01.1.1.06 PIS/Pasep
    "csll": 7942,                               # 10.01.1.1.07 CSLL
    "cpmf": 7943,                               # 10.01.1.1.08 CPMF
    "receita_da_cide_combustiveis": 7944,       # 10.01.1.1.09 Receita da CIDE Combustíveis
    "outras_administradas_pela_rfb": 7945,      # 10.01.1.1.10 Outras Administradas pela RFB
    "incentivos_fiscais": 7946,                 # 10.01.1.2 Incentivos Fiscais
    "arrecadacao_liquida_rgps": 7947,           # 10.01.1.3 Arrecadação Líquida para o RGPS
    "arrecadacao_liquida_para_o_rgps_urbana": 7948,  # 10.01.1.3.1 Arrecadação Líquida para o RGPS - Urbana
    "arrecadacao_liquida_para_o_rgps_rural": 7949,   # 10.01.1.3.2 Arrecadação Líquida para o RGPS - Rural
    "receitas_nao_administradas_rfb": 7950,     # 10.01.1.4 Receitas Não Administradas pela Receita Federal do Brasil
    "concessoes_e_permissoes": 7951,            # 10.01.1.4.1 Concessões e Permissões
    "dividendos_e_participacoes": 7952,         # 10.01.1.4.2 Dividendos e Participações
    "dividendos_e_participacoes_banco_do_brasil": 8381,  # 10.01.1.4.2.1 Dividendos e Participações - Banco do Brasil
    "dividendos_e_participacoes_bnb": 8382,     # 10.01.1.4.2.2 Dividendos e Participações - BNB
    "dividendos_e_participacoes_bndes": 8383,   # 10.01.1.4.2.3 Dividendos e Participações - BNDES
    "dividendos_e_participacoes_caixa_economica_federal": 8384,  # 10.01.1.4.2.4 Dividendos e Participações - Caixa Econômica Federal
    "dividendos_e_participacoes_correios": 8385,  # 10.01.1.4.2.5 Dividendos e Participações - Correios
    "dividendos_e_participacoes_eletrobras": 8386,  # 10.01.1.4.2.6 Dividendos e Participações - Eletrobrás
    "dividendos_e_participacoes_irb": 8387,     # 10.01.1.4.2.7 Dividendos e Participações - IRB
    "dividendos_e_participacoes_petrobras": 8388,  # 10.01.1.4.2.8 Dividendos e Participações - Petrobrás
    "demais_dividendos_participacoes_pagos_a_uniao": 8390,  # 10.01.1.4.2.9 Demais Dividendos/Participações Pagos à União
    "contr_plano_de_seguridade_social_do_servidor": 7953,  # 10.01.1.4.3 Contr. Plano de Seguridade Social do Servidor
    "receitas_de_exploracao_de_recursos_naturais": 7954,  # 10.01.1.4.4 Receitas de Exploração de Recursos Naturais
    "receitas_proprias_fontes_50_81_e_82": 7955,  # 10.01.1.4.5 Receitas Próprias (fontes 50, 81 e 82)
    "receita_de_contribuicao_do_salario_educacao": 7956,  # 10.01.1.4.6 Receita de Contribuição do Salário Educação
    "complemento_para_o_fgts_lc_n_110_01": 7957,  # 10.01.1.4.7 Complemento para o FGTS (LC nº 110/01)
    "demais_receitas_nao_administradas_pela_rfb": 7959,  # 10.01.1.4.8 Demais Receitas Não Administradas pela RFB
    "d_q_receitas_de_operacoes_com_ativos": 7958,  # 10.01.1.4.8.1 d/q Receitas de Operações com Ativos
    "receita_liquida": 7960,                    # 10.01.2 Receita Líquida (Receita Total - Transf. por Repartição de Receitas)

    # --- 10.02 Transferências ---
    "transferencias_reparticao_receita": 7961,  # 10.02.1 Transferências por Repartição de Receita
    "fpm_fpe_ipi_ee": 7962,                     # 10.02.1.1 FPM / FPE / IPI-EE
    "fundos_constitucionais": 7963,             # 10.02.1.2 Fundos Constitucionais
    "fundos_constitucionais_repasse_total": 7964,  # 10.02.1.2.1 Fundos Constitucionais - Repasse Total
    "fundos_constitucionais_superavit_dos_fundos": 7965,  # 10.02.1.2.2 Fundos Constitucionais - Superávit dos Fundos
    "transferencia_de_contribuicao_do_salario_educacao": 7966,  # 10.02.1.3 Transferência de Contribuição do Salário Educação
    "transferencias_de_exploracao_de_recursos_naturais": 7967,  # 10.02.1.4 Transferências de Exploração de Recursos Naturais
    "transferencia_da_cide_combustiveis": 7968,  # 10.02.1.5 Transferência da CIDE - Combustíveis
    "demais_transferencias_por_reparticao_de_receita": 7969,  # 10.02.1.6 Demais Transferências por Repartição de Receita

    # --- 10.03 Despesas ---
    "despesa_total": 7970,                      # 10.03.1 Despesa total
    "beneficios_previdenciarios": 7971,         # 10.03.1.1 Benefícios Previdenciários - Total
    "beneficios_previdenciarios_urbano": 7972,  # 10.03.1.1.1 Benefícios Previdenciários - Urbano
    "beneficios_previdenciarios_urbano_sentencas_judiciais_e_precatorios": 7973,  # 10.03.1.1.1.1 Benefícios Previdenciários - Urbano - Sentenças Judiciais e Precatórios
    "beneficios_previdenciarios_rural": 7974,   # 10.03.1.1.2 Benefícios Previdenciários - Rural
    "beneficios_previdenciarios_rural_sentencas_judiciais_e_precatorios": 7975,  # 10.03.1.1.2.1 Benefícios Previdenciários - Rural - Sentenças Judiciais e Precatórios
    "pessoal_encargos_sociais": 7976,           # 10.03.1.2 Pessoal e Encargos Sociais
    "pessoal_e_encargos_sociais_sentencas_judiciais_e_precatorios": 7977,  # 10.03.1.2.1 Pessoal e Encargos Sociais - Sentenças Judiciais e Precatórios
    "outras_despesas_obrigatorias": 7978,       # 10.03.1.3 Outras Despesas Obrigatórias - Total
    "abono_e_seguro_desemprego": 7979,          # 10.03.1.3.01 Abono e Seguro Desemprego
    "abono": 7980,                              # 10.03.1.3.01.1 Abono
    "seguro_desemprego": 7981,                  # 10.03.1.3.01.2 Seguro Desemprego
    "seguro_desemprego_seguro_defeso": 7982,    # 10.03.1.3.01.2.1 Seguro Desemprego - Seguro Defeso
    "anistiados": 7983,                         # 10.03.1.3.02 Anistiados
    "apoio_fin_municipios_estados": 7984,       # 10.03.1.3.03 Apoio Fin. Municípios/Estados
    "beneficios_de_legislacao_especial_e_indenizacoes": 7985,  # 10.03.1.3.04 Benefícios de Legislação Especial e Indenizações
    "beneficios_de_prestacao_continuada_da_loas_rmv": 7986,  # 10.03.1.3.05 Benefícios de Prestação Continuada da LOAS/RMV
    "beneficios_de_prestacao_continuada_da_loas_rmv_sentencas_judiciais_e_precatorios": 7988,  # 10.03.1.3.05.1 Benefícios de Prestação Continuada da LOAS/RMV - Sentenças Judiciais e Precatórios
    "complemento_do_fgts_lc_n_110_01": 7987,    # 10.03.1.3.06 Complemento do FGTS (LC nº 110/01)
    "creditos_extraordinarios_exceto_pac": 7989,  # 10.03.1.3.07 Créditos Extraordinários (exceto PAC)
    "compensacao_ao_rgps_pelas_desoneracoes_da_folha": 7990,  # 10.03.1.3.08 Compensação ao RGPS pelas Desonerações da Folha
    "fabricacao_de_cedulas_e_moedas": 7991,     # 10.03.1.3.09 Fabricação de Cédulas e Moedas
    "fundeb_complem_uniao": 7992,               # 10.03.1.3.10 FUNDEB (Complem. União)
    "fundo_constitucional_df": 7993,            # 10.03.1.3.11 Fundo Constitucional DF
    "legislativo_judiciario_mpu_dpu_custeio_e_capital": 7994,  # 10.03.1.3.12 Legislativo/Judiciário/MPU/DPU (Custeio e Capital)
    "lei_kandir_lc_n_87_96_e_102_00_e_fex": 7995,  # 10.03.1.3.13 Lei Kandir (LC nº 87/96 e 102/00) e FEX
    "sentencas_judiciais_e_precatorios_custeio_e_capital": 7996,  # 10.03.1.3.14 Sentenças Judiciais e Precatórios (Custeio e Capital)
    "subsidios_subvencoes_e_proagro": 7997,     # 10.03.1.3.15 Subsídios, Subvenções e Proagro
    "operacoes_oficiais_de_credito_e_reordenamento_de_passivos": 8003,  # 10.03.1.3.15.1 Operações Oficiais de Crédito e Reordenamento de Passivos
    "equalizacao_de_custeio_agropecuario": 8004,  # 10.03.1.3.15.1.01 Equalização de custeio agropecuário
    "equalizacao_de_invest_rural_e_agroindustrial": 8005,  # 10.03.1.3.15.1.02 Equalização de invest. rural e agroindustrial
    "politica_de_precos_agricolas_total": 8006,  # 10.03.1.3.15.1.03 Política de preços agrícolas - Total
    "politica_de_precos_agricolas_equalizacao_emprestimo_do_governo_federal": 8007,  # 10.03.1.3.15.1.03.1 Política de preços agrícolas - Equalização Empréstimo do Governo Federal
    "politica_de_precos_agricolas_equalizacao_aquisicoes_do_governo_federal": 8008,  # 10.03.1.3.15.1.03.2 Política de preços agrícolas - Equalização Aquisições do Governo Federal
    "politica_de_precos_agricolas_garantia_a_sustentacao_de_precos": 8009,  # 10.03.1.3.15.1.03.3 Política de preços agrícolas - Garantia à Sustentação de Preços
    "pronaf_total": 8010,                       # 10.03.1.3.15.1.04 Pronaf - Total
    "pronaf_equalizacao_emprestimo_do_governo_federal": 8011,  # 10.03.1.3.15.1.04.1 Pronaf - Equalização Empréstimo do Governo Federal
    "pronaf_concessao_de_financiamento": 8012,  # 10.03.1.3.15.1.04.2 Pronaf - Concessão de Financiamento
    "pronaf_aquisicao": 8013,                   # 10.03.1.3.15.1.04.3 Pronaf - Aquisição
    "proex_total": 8014,                        # 10.03.1.3.15.1.05 Proex - Total
    "proex_equalizacao_emprestimo_do_governo_federal": 8015,  # 10.03.1.3.15.1.05.1 Proex - Equalização Empréstimo do Governo Federal
    "proex_concessao_de_financiamento": 8016,   # 10.03.1.3.15.1.05.2 Proex - Concessão de Financiamento
    "programa_especial_de_saneamento_de_ativos_pesa": 8017,  # 10.03.1.3.15.1.06 Programa especial de saneamento de ativos (PESA)
    "alcool": 8018,                             # 10.03.1.3.15.1.07 Álcool
    "cacau": 8019,                              # 10.03.1.3.15.1.08 Cacau
    "programa_de_subsidio_a_habitacao_de_interesse_social_psh": 8020,  # 10.03.1.3.15.1.09 Programa de subsídio à habitação de interesse social (PSH)
    "securitizacao_da_divida_agricola_lei_9_138_1995": 8021,  # 10.03.1.3.15.1.10 Securitização da dívida agrícola (LEI 9.138/1995)
    "fundo_da_terra_incra": 8022,               # 10.03.1.3.15.1.11 Fundo da terra/ INCRA
    "funcafe": 8023,                            # 10.03.1.3.15.1.12 Funcafé
    "revitaliza": 8024,                         # 10.03.1.3.15.1.13 Revitaliza
    "programa_de_sustentacao_ao_investimento_psi": 8025,  # 10.03.1.3.15.1.14 Programa de Sustentação ao Investimento - PSI
    "operacoes_de_microcredito_produtivo_orientado_eqmpo": 8026,  # 10.03.1.3.15.1.15 Operações de Microcredito Produtivo Orientado (EQMPO)
    "operacoes_de_credito_destinadas_a_pessoas_com_deficiencia_eqpcd": 8027,  # 10.03.1.3.15.1.16 Operações de crédito destinadas a Pessoas com deficiência (EQPCD)
    "fundo_nacional_de_desenvolvimento_fnd": 8028,  # 10.03.1.3.15.1.17 Fundo nacional de desenvolvimento (FND)
    "fundo_setorial_audiovisual_fsa": 8029,     # 10.03.1.3.15.1.18 Fundo Setorial Audiovisual (FSA)
    "capitalizacao_a_emgea": 8030,              # 10.03.1.3.15.1.19 Capitalização à Emgea
    "subv_parcial_a_remuneracao_por_cessao_de_energia_eletrica_de_itaipu": 8031,  # 10.03.1.3.15.1.20 Subv. Parcial à Remuneração por Cessão de Energia Elétrica de Itaipu
    "subvencoes_economicas": 8032,              # 10.03.1.3.15.1.21 Subvenções Econômicas
    "equalizacao_dos_fundos_fda_fdne_fdco": 8033,  # 10.03.1.3.15.1.22 Equalização dos Fundos FDA/FDNE/FDCO
    "sudene": 8034,                             # 10.03.1.3.15.1.23 Sudene
    "receitas_de_recuperacao_de_subvencoes": 8035,  # 10.03.1.3.15.1.24 Receitas de Recuperação de Subvenções
    "proagro": 8036,                            # 10.03.1.3.15.2 Proagro
    "pnafe": 8037,                              # 10.03.1.3.15.3 PNAFE
    "demais_subsidios_e_subvencoes": 8038,      # 10.03.1.3.15.4 Demais Subsídios e Subvenções
    "transferencias_ana": 7998,                 # 10.03.1.3.16 Transferências ANA
    "transferencias_multas_aneel": 7999,        # 10.03.1.3.17 Transferências Multas ANEEL
    "impacto_primario_do_fies": 8000,           # 10.03.1.3.18 Impacto Primário do FIES
    "financiamento_de_campanha_eleitoral": 8001,  # 10.03.1.3.19 Financiamento de Campanha Eleitoral
    "demais_despesas_obrigatorias": 8002,       # 10.03.1.3.20 Demais Despesas Obrigatórias
    "auxilio_cde": 8039,                        # 10.03.1.3.20.1 Auxílio CDE
    "convenios": 8040,                          # 10.03.1.3.20.2 Convênios
    "doacoes": 8141,                            # 10.03.1.3.20.3 Doações
    "fda_fdne": 8160,                           # 10.03.1.3.20.4 FDA/FDNE
    "reserva_de_contingencia": 8380,            # 10.03.1.3.20.5 Reserva de Contingência
    "ressarc_est_mun_comb_fosseis": 8680,       # 10.03.1.3.20.6 Ressarc. Est/Mun. Comb. Fósseis
    "despesas_executivo_prog_financeira": 8041,  # 10.03.1.4 Despesas do Poder Executivo Sujeitas à Programação Financeira
    "obrigatorias_com_controle_de_fluxo": 8042,  # 10.03.1.4.1 Obrigatórias com Controle de Fluxo
    "obrigatorias_com_controle_de_fluxo_bolsa_familia": 8045,  # 10.03.1.4.1.2 Obrigatórias com Controle de Fluxo - Bolsa Família
    "obrigatorias_com_controle_de_fluxo_saude": 8046,  # 10.03.1.4.1.3 Obrigatórias com Controle de Fluxo - Saúde
    "demais_obrigatorias_com_controle_de_fluxo": 8047,  # 10.03.1.4.1.5 Demais Obrigatórias com Controle de Fluxo
    "obrigatorias_com_controle_de_fluxo_educacao": 8181,  # 10.03.1.4.1.4 Obrigatórias com Controle de Fluxo - Educação
    "obrigatorias_com_controle_de_fluxo_beneficios_a_servidores_publicos": 8391,  # 10.03.1.4.1.1 Obrigatórias com Controle de Fluxo - Benefícios a servidores públicos
    "despesas_discricionarias_do_poder_executivo": 8052,  # 10.03.1.4.2 Despesas Discricionárias do Poder Executivo
    "discricionarias_saude": 8392,              # 10.03.1.4.2.1 Discricionárias - Saúde
    "discricionarias_educacao": 8393,           # 10.03.1.4.2.2 Discricionárias - Educação
    "discricionarias_defesa": 8394,             # 10.03.1.4.2.3 Discricionárias - Defesa
    "discricionarias_transporte": 8395,         # 10.03.1.4.2.4 Discricionárias - Transporte
    "discricionarias_administracao": 8396,      # 10.03.1.4.2.5 Discricionárias - Administração
    "discricionarias_ciencia_e_tecnologia": 8397,  # 10.03.1.4.2.6 Discricionárias - Ciência e Tecnologia
    "discricionarias_seguranca_publica": 8398,  # 10.03.1.4.2.7 Discricionárias - Segurança Pública
    "discricionarias_assistencia_social": 8399,  # 10.03.1.4.2.8 Discricionárias - Assistência Social
    "discricionarias_demais": 8400,             # 10.03.1.4.2.9 Discricionárias - Demais

    # --- 10.04 Resultado Primário Governo Central ---
    "resultado_primario_governo_central": 8055,  # 10.04.1 Resultado Primário - Governo Central
    "resultado_primario_tesouro_nacional": 8056,  # 10.04.1.1 Resultado Primário - Tesouro Nacional
    "resultado_primario_previdencia_social": 8057,  # 10.04.1.2 Resultado Primário - Previdência Social
    "resultado_primario_previdencia_social_urbano": 8058,  # 10.04.1.2.1 Resultado Primário - Previdência Social - Urbano
    "resultado_primario_previdencia_social_rural": 8059,  # 10.04.1.2.2 Resultado Primário - Previdência Social - Rural
    "resultado_primario_banco_central": 8060,   # 10.04.1.3 Resultado Primário - Banco Central

    # --- 10.05 Ajustes Metodológicos ---
    "ajustes_metodologicos": 8953,              # 10.05.1 Ajustes Metodológicos
    "ajuste_metodologico_itaipu": 8954,         # 10.05.1.1 Ajuste Metodológico Itaipu
    "ajuste_metodologico_caixa_competencia": 8955,  # 10.05.1.2 Ajuste Metodológico Caixa-Competência
    "ajuste_metodologico_recursos_nao_sacados_do_pis_pasep": 9290,  # 10.05.1.3 Ajuste Metodológico Recursos Não Sacados do PIS/PASEP
    "ajuste_metodologico_compensacoes_lc_n_194_2022": 9306,  # 10.05.1.4 Ajuste Metodológico Compensações LC nº 194/2022

    # --- 10.06 Discrepância Estatística ---
    "discrepancia_estatistica": 8956,           # 10.06.1 Discrepância Estatística

    # --- 10.07 Resultado Primário (Abaixo da Linha) ---
    "resultado_primario_abaixo_linha": 8957,    # 10.07.1 Resultado Primário do Governo Central - Abaixo da Linha

    # --- 10.08 Juros Nominais ---
    "juros_nominais": 8958,                     # 10.08.1 Juros Nominais

    # --- 10.09 Resultado Nominal ---
    "resultado_nominal": 8959,                  # 10.09.1 Resultado Nominal do Governo Central
}

_st = SeriesTemporais()


def _compute_resultado_primario_acima_linha(df: pd.DataFrame) -> pd.DataFrame:
    """resultado_primario_acima_linha = receita_liquida - despesa_total.

    Nao existe como serie propria nessa API (a antiga linha "5. (3-4)" do
    workbook resumido) -- so o subtema 10.07, explicitamente "abaixo da
    linha", tem um resultado primario com serie propria. Identidade validada
    quando essa mesma linha ainda vinha do parsing de Excel -- ver Gotchas em
    analytics/fiscal_policy/CLAUDE.md.
    """
    wide = df.pivot(index="date", columns="name", values="value")
    calc = (wide["receita_liquida"] - wide["despesa_total"]).dropna()
    return pd.DataFrame({
        "date": calc.index,
        "name": "resultado_primario_acima_linha",
        "value": calc.values,
    })


def run(start: str | None = None) -> None:
    """Atualiza macro_brasil.fisc_rtn.

    Trunca a tabela antes de recarregar -- ver truncate_table() em
    connectors/mysql.py. Decisao explicita do usuario (2026-08): um upsert
    por chave (date, name) so atualiza linhas cuja chave bate exatamente com
    algo na nova carga; se a nova fonte um dia nao cobrir mais algum periodo
    antigo sob o mesmo nome, aquela linha antiga (da fonte anterior, via
    parsing de Excel) sobreviveria intacta e silenciosamente desatualizada.
    Seguro aqui porque fisc_rtn e alimentada por este script e nenhum outro
    (confirmado em jobs/update_db.py) e a fonte sempre distribui historico
    completo, nunca incremental -- truncar nao perde nenhum dado que nao
    seja imediatamente reescrito na mesma chamada.

    Antes de truncar, salva um snapshot CSV da tabela atual em `_BACKUP_DIR`
    (ultimos 5 mantidos, ver backup_table_before_truncate() em
    connectors/mysql.py) -- assim, se uma carga futura trouxer uma revisao
    abrupta ou errada da fonte, ainda existe "o que era antes desta rodada"
    para comparar. Decisao do usuario (2026-08), depois de eu ter truncado
    sem backup na migracao Excel->API deste script -- os valores antigos
    daquela migracao especifica ja se perderam, isso so cobre daqui em diante.

    Args:
        start: nao utilizado -- a API de Series Temporais so distribui cada
               serie como historico completo (sem parametro de range).
               Mantido por consistencia de assinatura com os demais scripts
               run().
    """
    df = _st.get_series_bulk(_LINE_ITEMS)
    derived = _compute_resultado_primario_acima_linha(df)
    df = pd.concat([df, derived], ignore_index=True)
    backup_table_before_truncate(_DATABASE, _TABLE, _BACKUP_DIR)
    truncate_table(_DATABASE, _TABLE)
    insert_data_into_database(_DATABASE, _TABLE, df)
