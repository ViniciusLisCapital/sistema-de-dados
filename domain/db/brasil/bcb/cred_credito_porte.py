"""
Crédito do sistema financeiro — saldo a pessoas jurídicas por porte de empresa (BCB/SGS)

Series SGS coletadas (10 series = 4 metricas x porte, nem toda combinacao existe --
"Total" so tem codigo proprio para as 2 metricas de "saldo de maior risco", nao para
saldo/inadimplencia) -- Tabela 23 da publicacao mensal do BCB "Tabelas de Estatisticas
Monetarias e de Credito" (ver analytics/credit/fontes_dados.md).

Metricas:
  saldo                    -- saldo da carteira, R$ milhoes (so MPMe/Grande, sem Total)
  inadimplencia            -- carteira em atraso >90d, % (so MPMe/Grande, sem Total)
  saldo_maior_risco        -- % do saldo classificado em rating de maior risco (MPMe/Grande/Total)
  saldo_maior_risco_res4966 -- idem, sob a metodologia da Resolucao CMN 4.966 (MPMe/Grande/Total)

Disponivel via SGS desde 2012-01 -- corte por porte que nao existe em nenhuma outra
tabela ja na base.

Banco: macro_brasil.cred_credito_porte -- PRIMARY KEY (date, porte, metrica)
DDL:
  CREATE TABLE macro_brasil.cred_credito_porte (
      date    DATE          NOT NULL,
      porte   VARCHAR(20)   NOT NULL,
      metrica VARCHAR(30)   NOT NULL,
      value   DECIMAL(15,5),
      PRIMARY KEY (date, porte, metrica)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

import pandas as pd

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "cred_credito_porte"

_CODES_SALDO = {
    "mpme":   27701,
    "grande": 27702,
}
_CODES_INADIMPLENCIA = {
    "mpme":   27703,
    "grande": 27704,
}
_CODES_SALDO_MAIOR_RISCO = {
    "mpme":   27706,
    "grande": 27707,
    "total":  27705,
}
_CODES_SALDO_MAIOR_RISCO_RES4966 = {
    "mpme":   29582,
    "grande": 29583,
    "total":  29581,
}

_bcb = BCB()


def _fetch_metrica(metrica: str, codes: dict, start: str | None, end: str | None, n_meses: int) -> pd.DataFrame:
    if start:
        df = _bcb.get_sgs(codes, start=start, end=end)
    else:
        df = _bcb.get_sgs_ultimos(codes, n=n_meses)
    df = df.rename(columns={"name": "porte"})
    df["metrica"] = metrica
    return df[["date", "porte", "metrica", "value"]]


def run(n_meses: int = 24, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.cred_credito_porte.

    Args:
        n_meses: ultimos N meses (default 24). Ignorado se start/end fornecidos.
        start:   data inicial no formato "DD/MM/YYYY", ou "all" para serie completa.
        end:     data final no formato "DD/MM/YYYY". Default: hoje.
    """
    frames = [
        _fetch_metrica("saldo", _CODES_SALDO, start, end, n_meses),
        _fetch_metrica("inadimplencia", _CODES_INADIMPLENCIA, start, end, n_meses),
        _fetch_metrica("saldo_maior_risco", _CODES_SALDO_MAIOR_RISCO, start, end, n_meses),
        _fetch_metrica("saldo_maior_risco_res4966", _CODES_SALDO_MAIOR_RISCO_RES4966, start, end, n_meses),
    ]
    df = pd.concat(frames, ignore_index=True)
    insert_data_into_database(_DATABASE, _TABLE, df)
