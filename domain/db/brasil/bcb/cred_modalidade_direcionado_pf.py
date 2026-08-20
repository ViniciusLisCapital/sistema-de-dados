"""
Crédito do sistema financeiro — recursos direcionados, por modalidade, Pessoa Física (BCB/SGS)

Series SGS coletadas, por metrica x modalidade -- Tabelas 9, 13, 18, 22 da publicacao mensal
do BCB "Tabelas de Estatisticas Monetarias e de Credito" (ver
analytics/brasil/credit/fontes_dados.md para o mapeamento completo). A coluna "Total" de cada
tabela-fonte foi deliberadamente excluida daqui -- ja existe em macro_brasil.cred_credito_resumo
sob outro nome (ex: esta tabela nao repete o que cred_credito_resumo ja cobre).

Algumas celulas da planilha-fonte nao tem codigo SGS proprio (mostram "-" em vez de um
numero) -- confirmado ao vivo, nao e erro de extracao. Omitidas dos dicionarios abaixo,
nao inseridas com NULL.

Metricas coletadas:
  saldo -- Tabela 9 (10 modalidades)
  concessao -- Tabela 13 (10 modalidades)
  taxa_media -- Tabela 18 (9 modalidades)
  inadimplencia -- Tabela 22 (10 modalidades)

Banco: macro_brasil.cred_modalidade_direcionado_pf -- PRIMARY KEY (date, modalidade, metrica)
DDL:
  CREATE TABLE macro_brasil.cred_modalidade_direcionado_pf (
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
_TABLE    = "cred_modalidade_direcionado_pf"

_CODES_SALDO = {
    "credito_com_recursos_do_bndes_financiamento_agroindustrial": 20615,
    "credito_com_recursos_do_bndes_total": 20616,
    "credito_rural_taxas_de_mercado": 20607,
    "credito_rural_taxas_reguladas": 20608,
    "credito_rural_total": 20609,
    "financiamentos_imobiliarios_taxas_de_mercado": 20610,
    "financiamentos_imobiliarios_taxas_reguladas": 20611,
    "financiamentos_imobiliarios_total": 20612,
    "microcredito": 20620,
    "outros": 20621,
}

_CODES_CONCESSAO = {
    "credito_com_recursos_do_bndes_financiamento_agroindustrial": 20707,
    "credito_com_recursos_do_bndes_total": 20708,
    "credito_rural_taxas_de_mercado": 20699,
    "credito_rural_taxas_reguladas": 20700,
    "credito_rural_total": 20701,
    "financiamentos_imobiliarios_taxas_de_mercado": 20702,
    "financiamentos_imobiliarios_taxas_reguladas": 20703,
    "financiamentos_imobiliarios_total": 20704,
    "microcredito": 20712,
    "outros": 20713,
}

_CODES_TAXA_MEDIA = {
    "credito_com_recursos_do_bndes_financiamento_agroindustrial": 20777,
    "credito_com_recursos_do_bndes_total": 20778,
    "credito_rural_taxas_de_mercado": 20769,
    "credito_rural_taxas_reguladas": 20770,
    "credito_rural_total": 20771,
    "financiamentos_imobiliarios_taxas_de_mercado": 20772,
    "financiamentos_imobiliarios_taxas_reguladas": 20773,
    "financiamentos_imobiliarios_total": 20774,
    "microcredito": 20782,
}

_CODES_INADIMPLENCIA = {
    "credito_com_recursos_do_bndes_financiamento_agroindustrial": 21154,
    "credito_com_recursos_do_bndes_total": 21155,
    "credito_rural_taxas_de_mercado": 21146,
    "credito_rural_taxas_reguladas": 21147,
    "credito_rural_total": 21148,
    "financiamentos_imobiliarios_taxas_de_mercado": 21149,
    "financiamentos_imobiliarios_taxas_reguladas": 21150,
    "financiamentos_imobiliarios_total": 21151,
    "microcredito": 21159,
    "outros": 21160,
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
    """Atualiza macro_brasil.cred_modalidade_direcionado_pf.

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
