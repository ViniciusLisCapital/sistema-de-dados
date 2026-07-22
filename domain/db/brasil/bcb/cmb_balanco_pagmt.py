"""
Balanco de Pagamentos do Brasil (BPM6)

Series SGS (valores em USD millions). Codigos confirmados em 2026-07 contra
`analytics/exchange_rate/referencia/balance_payments_breakdown.xlsx` (mapeamento
oficial fornecido pelo usuario, aba "BreakDown the bcb provides") e
cross-checados numericamente contra os
5 meses (Jan-Mai/2026) da aba "the breakdown I want" — todas as formulas
abaixo batem com a API BCB dentro da tolerancia de arredondamento (<0.11).

Conta Corrente:
  22701 Transacoes correntes — saldo                    -> conta_corrente
  22704 Balanca comercial (bens) e Servicos — saldo      -> balanca_comercial_servicos
  22708 Exportacoes de bens                              -> exportacao_bens
  22709 Importacoes de bens                              -> importacao_bens
  22710 Balanca comercial (bens) — mercadorias em geral   -> mercadorias_gerais
  22711 Exportacoes de bens — mercadorias em geral        -> mercadorias_gerais_export
  22712 Importacoes de bens — mercadorias em geral        -> mercadorias_gerais_import
  22713 Balanca comercial (bens) — exportacoes sob merchanting -> merchanting
  22716 Balanca comercial (bens) — ouro nao monetario     -> ouro_nao_monetario
  22717 Exportacoes de bens — ouro nao monetario          -> ouro_nao_monetario_export
  22718 Importacoes de bens — ouro nao monetario          -> ouro_nao_monetario_import
  22719 Servicos — saldo                                 -> servicos
  22740 Viagens                                           -> viagens
  22728 Transportes                                       -> transportes
  22782 Aluguel de equipamentos                          -> aluguel_equipamentos
  22800 Renda primaria — saldo                            -> renda_primaria
  22803 Remuneracao de empregados                         -> remuneracao_empregados
  22812 Lucros e dividendos remetidos (IDP)                -> lucros_remetidos
  22815 Lucros reinvestidos (IDP)                          -> lucros_reinvestidos
  22818 Juros de operacoes intercompanhia (IDP)            -> juros_intercompanhia
  22824 Lucros e dividendos (investimento em carteira)     -> lucros_dividendos_carteira
  22827 Juros de titulos negociados no mercado externo (carteira) -> juros_carteira_externo
  22830 Juros de titulos negociados no mercado domestico — despesas (carteira) -> juros_carteira_domestico
  22831 Renda de outros investimentos (juros)              -> juros_outros_investimentos
  22834 Renda de reservas — receitas                       -> renda_reservas
  22838 Renda secundaria — saldo                           -> renda_secundaria
  22851 Conta capital — saldo                              -> conta_capital

Conta Financeira:
  22863 Conta Financeira: Concessoes liquidas (+) / Captacoes liquidas (-) -> conta_financeira
  22865 Investimentos diretos no exterior (IDP — ativos)   -> idp_exterior
  22867 Investimentos diretos no exterior — Saidas          -> ide_saidas
  22885 Investimentos diretos no pais (IDP — passivos)      -> investimento_direto_liquido
  22886 Investimentos diretos no pais — Ingressos           -> idp_ingressos
  22906 Investimentos em carteira — ativos                 -> portfolio_ativos
  22909 Investimentos em acoes — ativos                     -> acoes_ativos
  22912 Investimentos em fundos de investimento — ativos    -> fundos_ativos
  22918 Titulos de divida — ativos — curto prazo             -> titulos_ativos_cp
  22921 Titulos de divida — ativos — longo prazo             -> titulos_ativos_lp
  22924 Investimentos em carteira — passivos                -> portfolio_passivos
  22927 Investimentos em acoes — passivos                   -> acoes_passivos
  22936 Investimentos em fundos de investimento — passivos  -> fundos_passivos
  22942 Titulos de divida (passivos) negociados no mercado domestico -> titulos_dom
  22948 Titulos de divida (passivos) negociados no mercado externo — curto prazo -> titulos_externo_cp
  22951 Titulos de divida (passivos) negociados no mercado externo — longo prazo -> titulos_externo_lp
  22952 Titulos externo LP — Ingressos                      -> titulos_externo_lp_ingressos
  22953 Titulos externo LP — Saidas                          -> titulos_externo_lp_saidas
  22970 Outros investimentos — ativos                       -> outros_inv_ativos
  22971 Outros investimentos — passivos                      -> outros_inv_passivos
  22997 Emprestimos — passivos curto prazo                   -> emprestimos_cp_passivos
  22998 Emprestimos — passivos longo prazo                    -> emprestimos_lp_passivos
  22999 Emprestimos LP passivos — Ingressos                    -> emprestimos_lp_ingressos
  23000 Emprestimos LP passivos — Saidas                        -> emprestimos_lp_saidas
  22966 Derivativos — saldo                                  -> derivativos
  23043 Ativos de reserva                                     -> ativos_reserva
  23060 Erros e omissoes                                       -> erros_omissoes

Series derivadas (calculadas em analytics/exchange_rate/generate_report.py a partir
das series brutas acima, NAO armazenadas no banco — mesmo padrao ja usado
para `comercial_saldo` em cmb_fluxo_cambial):
  demais_servicos                  = servicos - viagens - transportes - aluguel_equipamentos
  juros                            = juros_intercompanhia + juros_carteira_externo + juros_carteira_domestico + juros_outros_investimentos + renda_reservas
  lucros_dividendos                = lucros_remetidos + lucros_reinvestidos + lucros_dividendos_carteira
    (lucros_reinvestidos/SGS 22815 tem lacuna real na fonte BCB entre 1999-01 e 2009-12 -
     confirmado via API, 404 "Value(s) not found" para essa janela; analytics/exchange_rate/generate_report.py
     trata isso com fillna(0) antes de somar, para não propagar NaN por uma década inteira)
  investimentos_ativos             = idp_exterior + portfolio_ativos + outros_inv_ativos
  investimentos_passivos           = investimento_direto_liquido + portfolio_passivos + outros_inv_passivos
  acoes_totais                     = acoes_passivos + fundos_passivos
  acoes_fundos_ativos               = acoes_ativos + fundos_ativos
    (portfolio_ativos = acoes_fundos_ativos + titulos_ativos_cp + titulos_ativos_lp,
     confirmado numericamente contra a API para Jan-Mai/2026)
  emprestimos_titulos_lp_externo   = titulos_externo_lp + emprestimos_lp_passivos
  emprestimos_titulos_cp_externo   = titulos_externo_cp + emprestimos_cp_passivos
  demais_passivos                  = portfolio_passivos + outros_inv_passivos - acoes_passivos - fundos_passivos
                                      - titulos_dom - titulos_externo_lp - emprestimos_lp_passivos
                                      - titulos_externo_cp - emprestimos_cp_passivos

Quebra da Balanca de Bens (2026-07, pedido do usuario, "like the services"):
mercadorias_gerais + merchanting + ouro_nao_monetario = exportacao_bens - importacao_bens
(confirmado numericamente contra a API para Jan-Mai/2026, bate exatamente — e' uma
particao aditiva oficial do BCB, nao uma aproximacao). Merchanting e' pequeno em
modulo (~USD 5-20 mi/mes vs ~USD 6-9 bi do total) e tem convencao de sinal atipica
no detalhamento bruto (22714/22715 — "importacoes sob merchanting" ja vem negativo
na fonte, ao contrario de importacao_bens); por isso so o liquido (22713) foi
ingerido, sem export/import proprios de merchanting.

Pendencia conhecida: a quebra "Ativos de bancos" vs "Demais ativos" (lado
ativo do balanco) e a quebra publico/privado/direto/demais emprestimos dos
titulos de LP externo (Ingressos e Amortizacoes) nao foram resolvidas — nao
ha codigo SGS correspondente em `analytics/exchange_rate/referencia/balance_payments_breakdown.xlsx`.
Ver analytics/exchange_rate/CLAUDE.md.

Correcao 2026-07: os codigos de 6 das 10 series originais estavam ERRADOS
(apontavam para sub-itens nao relacionados — ex: `conta_corrente` usava 22707,
que e "Balanca comercial (bens)", nao "Transacoes correntes"). Series afetadas:
conta_corrente, balanca_comercial_servicos, conta_financeira,
investimento_carteira, carteira_acoes, carteira_renda_fixa (as 3 ultimas foram
descontinuadas em favor de portfolio_ativos/portfolio_passivos/acoes_passivos/
fundos_passivos/titulos_dom, mais precisos). Linhas historicas sob os nomes
antigos foram removidas do banco (nunca representaram os conceitos que o nome
sugeria).

Banco: macro_brasil.cmb_balanco_pagmt
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "cmb_balanco_pagmt"

_SERIES = {
    # Conta corrente
    "conta_corrente":               22701,
    "balanca_comercial_servicos":   22704,
    "exportacao_bens":              22708,
    "importacao_bens":              22709,
    "mercadorias_gerais":           22710,
    "mercadorias_gerais_export":    22711,
    "mercadorias_gerais_import":    22712,
    "merchanting":                  22713,
    "ouro_nao_monetario":           22716,
    "ouro_nao_monetario_export":    22717,
    "ouro_nao_monetario_import":    22718,
    "servicos":                     22719,
    "viagens":                      22740,
    "transportes":                  22728,
    "aluguel_equipamentos":         22782,
    "renda_primaria":               22800,
    "remuneracao_empregados":       22803,
    "lucros_remetidos":             22812,
    "lucros_reinvestidos":          22815,
    "juros_intercompanhia":         22818,
    "lucros_dividendos_carteira":   22824,
    "juros_carteira_externo":       22827,
    "juros_carteira_domestico":     22830,
    "juros_outros_investimentos":   22831,
    "renda_reservas":               22834,
    "renda_secundaria":             22838,
    "conta_capital":                22851,
    # Conta financeira
    "conta_financeira":             22863,
    "idp_exterior":                 22865,
    "ide_saidas":                   22867,
    "investimento_direto_liquido":  22885,
    "idp_ingressos":                22886,
    "portfolio_ativos":             22906,
    "acoes_ativos":                 22909,
    "fundos_ativos":                22912,
    "titulos_ativos_cp":            22918,
    "titulos_ativos_lp":            22921,
    "portfolio_passivos":           22924,
    "acoes_passivos":               22927,
    "fundos_passivos":              22936,
    "titulos_dom":                  22942,
    "titulos_externo_cp":           22948,
    "titulos_externo_lp":           22951,
    "titulos_externo_lp_ingressos": 22952,
    "titulos_externo_lp_saidas":    22953,
    "outros_inv_ativos":            22970,
    "outros_inv_passivos":          22971,
    "emprestimos_cp_passivos":      22997,
    "emprestimos_lp_passivos":      22998,
    "emprestimos_lp_ingressos":     22999,
    "emprestimos_lp_saidas":        23000,
    "derivativos":                  22966,
    "ativos_reserva":               23043,
    "erros_omissoes":               23060,
}

# Series descontinuadas em 2026-07 (codigo SGS errado — nunca representaram o
# conceito que o nome sugeria). Removidas do banco na primeira execucao apos
# a correcao para nao deixar dado errado orfao.
_DEPRECATED_NAMES = ["investimento_carteira", "carteira_acoes", "carteira_renda_fixa"]

_bcb = BCB()


def run(n_meses: int = 36, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.cmb_balanco_pagmt.

    Args:
        n_meses: ultimos N meses (default 36). Ignorado se start/end fornecidos.
        start:   data inicial no formato "DD/MM/YYYY", ou "all" para serie completa.
        end:     data final no formato "DD/MM/YYYY". Default: hoje.
    """
    if start:
        df = _bcb.get_sgs(_SERIES, start=start, end=end)
    else:
        df = _bcb.get_sgs_ultimos(_SERIES, n=n_meses)

    insert_data_into_database(_DATABASE, _TABLE, df)
