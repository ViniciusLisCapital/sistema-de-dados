"""
NFSP - Necessidade de Financiamento do Setor Publico (% PIB, fluxo acumulado em
12 meses, sem desvalorizacao cambial) — "abaixo da linha", metodologia BCB.

Series SGS coletadas (6 series, mensal, % PIB, acum. 12m):
  Setor publico consolidado:
    resultado_primario_pct_pib_12m (5793)
    resultado_nominal_pct_pib_12m  (5727)
    juros_nominais_pct_pib_12m     (5760)
  Resultado primario por nivel:
    resultado_primario_governo_federal_bc_pct_pib_12m  (5783) — Governo Federal e Banco Central
    resultado_primario_estados_municipios_pct_pib_12m  (5786) — Governos estaduais e municipais
    resultado_primario_empresas_estatais_pct_pib_12m   (5789) — Empresas estatais (todos os niveis)

Complementa fisc_rtn.py (Tesouro Nacional, "acima da linha", so Governo Central):
NFSP cobre o setor publico consolidado (Governo Central + Estados/Municipios +
Empresas Estatais + Banco Central) pela metodologia "abaixo da linha" do BCB.

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
