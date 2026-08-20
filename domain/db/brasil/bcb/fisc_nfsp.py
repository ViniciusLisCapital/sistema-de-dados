"""
NFSP - Necessidade de Financiamento do Setor Publico (% PIB, fluxo acumulado em
12 meses, sem desvalorizacao cambial) — "abaixo da linha", metodologia BCB.

Series SGS coletadas (10 series, mensal, % PIB, acum. 12m):
  Setor publico consolidado:
    resultado_primario_pct_pib_12m (5793)
    resultado_nominal_pct_pib_12m  (5727)
    juros_nominais_pct_pib_12m     (5760)
  Resultado primario por nivel (corte grosso, 3 grupos, pre-existente):
    resultado_primario_governo_federal_bc_pct_pib_12m  (5783) — Governo Federal e Banco Central
    resultado_primario_estados_municipios_pct_pib_12m  (5786) — Governos estaduais e municipais
    resultado_primario_empresas_estatais_pct_pib_12m   (5789) — Empresas estatais (todos os niveis)
  Resultado primario por esfera (corte fino, 2026-08, a pedido do usuario --
  "quero decompor [o impulso fiscal] por esfera: Governo Central, Estados e
  Municipios - nao Banco Central"): o BCB publica os 3 grupos acima JA
  desagregados nestas 4 series, entao nao ha corte novo a fazer no SGS, so
  colecionar series que ja existiam sem serem usadas aqui:
    resultado_primario_governo_federal_pct_pib_12m     (5784) — Governo Federal, SEM Banco Central
    resultado_primario_banco_central_pct_pib_12m       (5785) — Banco Central, sozinho
    resultado_primario_estados_pct_pib_12m             (5787) — Governos estaduais, sozinho
    resultado_primario_municipios_pct_pib_12m          (5788) — Governos municipais, sozinho
  Confirmado ao vivo (2026-08) que as 5 series de esfera (governo_federal +
  banco_central + estados + municipios + empresas_estatais) somam o total
  (resultado_primario_pct_pib_12m) a cada mes, a menos de arredondamento de
  +/-0,01pp (cada serie e publicada ja arredondada a 2 casas pelo SGS).

Complementa fisc_rtn.py (Tesouro Nacional, "acima da linha", so Governo Central):
NFSP cobre o setor publico consolidado (Governo Central + Estados/Municipios +
Empresas Estatais + Banco Central) pela metodologia "abaixo da linha" do BCB.

Fluxo mensal corrente (2026-08, a pedido do usuario -- "we have the monthly primary
result data from BCB... why not make the seasonal adjustments?", para o toggle
Trimestre do impulso fiscal via resultado primario em analytics/brasil/fiscal_policy/):
as 6 series de %PIB acumulado em 12m acima (resultado_primario + as 5 de esfera) sao
TODAS acumuladas -- fisc_nfsp nao guardava, ate agora, o fluxo MENSAL bruto (R$
milhoes, NAO acumulado, NAO %PIB) que as alimenta, o que so permitia dessazonalizar
via o atalho "T/T sobre o proprio acumulado" (ver _load_fiscal_impulse_nfsp() em
analytics/brasil/fiscal_policy/generate_report.py) em vez de rodar STL de verdade sobre uma
serie mensal genuina. Adicionadas 6 series novas, mesmo corte de esfera das 5+1
series acima, confirmadas ao vivo via busca no catalogo dadosabertos.bcb.gov.br
(nao so por nome -- por RECONCILIACAO numerica, o mesmo padrao ja usado para as
5 series de esfera acima):
    resultado_primario_fluxo_mensal                   (4649) -- Total (Setor Publico Consolidado)
    resultado_primario_governo_federal_fluxo_mensal    (4640) -- Governo Federal, SEM Banco Central
    resultado_primario_banco_central_fluxo_mensal      (4641) -- Banco Central, sozinho
    resultado_primario_estados_fluxo_mensal            (4643) -- Governos estaduais, sozinho
    resultado_primario_municipios_fluxo_mensal         (4644) -- Governos municipais, sozinho
    resultado_primario_empresas_estatais_fluxo_mensal  (4645) -- Empresas estatais (todos os niveis)
Confirmado ao vivo (2026-08) que estas 6 series sao a contraparte NAO acumulada
exata das 6 series acumuladas acima -- soma movel de 12 meses de
resultado_primario_fluxo_mensal (com o mesmo sinal invertido abaixo), dividida pelo
PIB acumulado em 12m (atv_pib_mensal.pib_acum_12m), reconcilia com
resultado_primario_pct_pib_12m a menos de 0,01pp em toda a janela testada (2026-01
a 2026-06) -- e a mesma identidade contabil que a BCB usa para publicar o
acumulado, so que ainda nao rodada (o acumulado ja vem pronto do SGS). As 6 series
NAO estao em %PIB (R$ milhoes brutos) -- dividir pelo PIB do MESMO mes
(atv_pib_mensal.pib_mensal) e responsabilidade de quem consome (ver
analytics/brasil/fiscal_policy/generate_report.py).

Codigos confirmados via busca no catalogo dadosabertos.bcb.gov.br (nao apenas por
memoria) em 2026-08 — mesma pratica adotada apos o bug de codigo SGS em
cmb_balanco_pagmt (ver comm_icbr.py).

**Inversao de sinal (2026-08, bug encontrado pelo usuario):** o SGS armazena essas
5 series (todas exceto juros_nominais_pct_pib_12m) na convencao "NFSP" —
necessidade de financiamento, positivo = deficit/precisa se financiar — que e o
INVERSO da convencao "resultado" usada nos nomes das colunas e em qualquer
divulgacao de mercado (positivo = superavit). Confirmado empiricamente: soma
bruta do SGS satisfaz resultado_nominal = resultado_primario + juros (identidade
de "necessidade", nao de "resultado" — a identidade correta seria resultado_nominal
= resultado_primario - juros). run() inverte o sinal dessas 5 series no momento da
gravacao para que a tabela armazene resultado_primario/nominal na convencao
convencional (positivo = superavit) — juros_nominais_pct_pib_12m fica como veio,
ja e um custo/despesa com sinal correto nas duas convencoes.

Banco: macro_brasil.fisc_nfsp — PRIMARY KEY (date, name)
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "fisc_nfsp"

_SERIES = {
    "resultado_primario_pct_pib_12m":                     5793,
    "resultado_nominal_pct_pib_12m":                       5727,
    "juros_nominais_pct_pib_12m":                          5760,
    "resultado_primario_governo_federal_bc_pct_pib_12m":   5783,
    "resultado_primario_estados_municipios_pct_pib_12m":   5786,
    "resultado_primario_empresas_estatais_pct_pib_12m":    5789,
    "resultado_primario_governo_federal_pct_pib_12m":      5784,
    "resultado_primario_banco_central_pct_pib_12m":        5785,
    "resultado_primario_estados_pct_pib_12m":              5787,
    "resultado_primario_municipios_pct_pib_12m":           5788,
    "resultado_primario_fluxo_mensal":                     4649,
    "resultado_primario_governo_federal_fluxo_mensal":     4640,
    "resultado_primario_banco_central_fluxo_mensal":       4641,
    "resultado_primario_estados_fluxo_mensal":             4643,
    "resultado_primario_municipios_fluxo_mensal":          4644,
    "resultado_primario_empresas_estatais_fluxo_mensal":   4645,
}

# Series SGS na convencao "necessidade de financiamento" (positivo = deficit) que
# precisam ser invertidas para a convencao "resultado" (positivo = superavit) —
# todas exceto juros_nominais_pct_pib_12m, ver docstring acima.
_FLIP_SIGN = set(_SERIES) - {"juros_nominais_pct_pib_12m"}

_bcb = BCB()


def run(start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.fisc_nfsp.

    Args:
        start: data inicial "DD/MM/YYYY", ou "all" para serie completa desde o
               inicio real de cada serie.
        end:   data final "DD/MM/YYYY". Default: hoje.
    """
    if start:
        df = _bcb.get_sgs(_SERIES, start=start, end=end)
    else:
        df = _bcb.get_sgs_ultimos(_SERIES, n=36)

    df.loc[df["name"].isin(_FLIP_SIGN), "value"] *= -1

    insert_data_into_database(_DATABASE, _TABLE, df)
