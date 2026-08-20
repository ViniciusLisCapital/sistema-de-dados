"""
Crédito do sistema financeiro — recursos direcionados, por modalidade, Pessoa Jurídica (BCB/SGS)

Series SGS coletadas, por metrica x modalidade -- Tabelas 8, 12, 17, 21 da publicacao mensal
do BCB "Tabelas de Estatisticas Monetarias e de Credito" (ver
analytics/brasil/credit/fontes_dados.md para o mapeamento completo). A coluna "Total" de cada
tabela-fonte foi deliberadamente excluida daqui -- ja existe em macro_brasil.cred_credito_resumo
sob outro nome (ex: esta tabela nao repete o que cred_credito_resumo ja cobre).

Algumas celulas da planilha-fonte nao tem codigo SGS proprio (mostram "-" em vez de um
numero) -- confirmado ao vivo, nao e erro de extracao. Omitidas dos dicionarios abaixo,
nao inseridas com NULL.

Metricas coletadas:
  saldo -- Tabela 8 (12 modalidades)
  concessao -- Tabela 12 (12 modalidades)
  taxa_media -- Tabela 17 (11 modalidades)
  inadimplencia -- Tabela 21 (12 modalidades)

Banco: macro_brasil.cred_modalidade_direcionado_pj -- PRIMARY KEY (date, modalidade, metrica)
DDL:
  CREATE TABLE macro_brasil.cred_modalidade_direcionado_pj (
      date       DATE          NOT NULL,
      modalidade VARCHAR(100)  NOT NULL,
      metrica    VARCHAR(30)   NOT NULL,
      value      DECIMAL(15,5),
      PRIMARY KEY (date, modalidade, metrica)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

import pandas as pd

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "cred_modalidade_direcionado_pj"

_CODES_SALDO = {
    "credito_com_recursos_do_bndes_capital_de_giro": 20601,
    "credito_com_recursos_do_bndes_financiamento_a_investimentos": 20602,
    "credito_com_recursos_do_bndes_financiamento_agroindustrial": 20603,
    "credito_com_recursos_do_bndes_total": 20604,
    "credito_rural_taxas_de_mercado": 20595,
    "credito_rural_taxas_reguladas": 20596,
    "credito_rural_total": 20597,
    "financiamentos_imobiliarios_taxas_de_mercado": 20598,
    "financiamentos_imobiliarios_taxas_reguladas": 20599,
    "financiamentos_imobiliarios_total": 20600,
    "outros": 20605,
    "programas_mpme": 29966,
}

_CODES_CONCESSAO = {
    "credito_com_recursos_do_bndes_capital_de_giro": 20693,
    "credito_com_recursos_do_bndes_financiamento_a_investimentos": 20694,
    "credito_com_recursos_do_bndes_financiamento_agroindustrial": 20695,
    "credito_com_recursos_do_bndes_total": 20696,
    "credito_rural_taxas_de_mercado": 20687,
    "credito_rural_taxas_reguladas": 20688,
    "credito_rural_total": 20689,
    "financiamentos_imobiliarios_taxas_de_mercado": 20690,
    "financiamentos_imobiliarios_taxas_reguladas": 20691,
    "financiamentos_imobiliarios_total": 20692,
    "outros": 20697,
    "programas_mpme": 29969,
}

_CODES_TAXA_MEDIA = {
    "credito_com_recursos_do_bndes_capital_de_giro": 20764,
    "credito_com_recursos_do_bndes_financiamento_a_investimentos": 20765,
    "credito_com_recursos_do_bndes_financiamento_agroindustrial": 20766,
    "credito_com_recursos_do_bndes_total": 20767,
    "credito_rural_taxas_de_mercado": 20758,
    "credito_rural_taxas_reguladas": 20759,
    "credito_rural_total": 20760,
    "financiamentos_imobiliarios_taxas_de_mercado": 20761,
    "financiamentos_imobiliarios_taxas_reguladas": 20762,
    "financiamentos_imobiliarios_total": 20763,
    "programas_mpme": 29975,
}

_CODES_INADIMPLENCIA = {
    "credito_com_recursos_do_bndes_capital_de_giro": 21140,
    "credito_com_recursos_do_bndes_financiamento_a_investimentos": 21141,
    "credito_com_recursos_do_bndes_financiamento_agroindustrial": 21142,
    "credito_com_recursos_do_bndes_total": 21143,
    "credito_rural_taxas_de_mercado": 21134,
    "credito_rural_taxas_reguladas": 21135,
    "credito_rural_total": 21136,
    "financiamentos_imobiliarios_taxas_de_mercado": 21137,
    "financiamentos_imobiliarios_taxas_reguladas": 21138,
    "financiamentos_imobiliarios_total": 21139,
    "outros": 21144,
    "programas_mpme": 29993,
}

_bcb = BCB()


def _fetch_metrica(metrica: str, codes: dict, start: str | None, end: str | None, n_meses: int) -> pd.DataFrame:
    if start:
        df = _bcb.get_sgs(codes, start=start, end=end)
    else:
        df = _bcb.get_sgs_ultimos(codes, n=n_meses)
    df = df.rename(columns={"name": "modalidade"})
    df["metrica"] = metrica
    return df[["date", "modalidade", "metrica", "value"]]


def run(n_meses: int = 24, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.cred_modalidade_direcionado_pj.

    Args:
        n_meses: ultimos N meses (default 24). Ignorado se start/end fornecidos.
        start:   data inicial no formato "DD/MM/YYYY", ou "all" para serie completa.
        end:     data final no formato "DD/MM/YYYY". Default: hoje.
    """
    frames = [
        _fetch_metrica("saldo", _CODES_SALDO, start, end, n_meses),
        _fetch_metrica("concessao", _CODES_CONCESSAO, start, end, n_meses),
        _fetch_metrica("taxa_media", _CODES_TAXA_MEDIA, start, end, n_meses),
        _fetch_metrica("inadimplencia", _CODES_INADIMPLENCIA, start, end, n_meses),
    ]
    df = pd.concat(frames, ignore_index=True)
    insert_data_into_database(_DATABASE, _TABLE, df)
