"""
Crédito do sistema financeiro — saldo, inadimplência e provisões por controle de
capital da instituição financeira (BCB/SGS)

Series SGS coletadas (9 series = 3 metricas x 3 controles) -- Tabela 26 da publicacao
mensal do BCB "Tabelas de Estatisticas Monetarias e de Credito" (ver
analytics/credit/fontes_dados.md).

Metricas:
  saldo         -- saldo da carteira, R$ milhoes
  inadimplencia -- carteira em atraso >90d, %
  provisoes     -- provisoes / saldo da carteira, %

Controles: publicas (instituicoes financeiras publicas), privadas_nacionais,
estrangeiras.

Banco: macro_brasil.cred_credito_controle_capital -- PRIMARY KEY (date, controle, metrica)
DDL:
  CREATE TABLE macro_brasil.cred_credito_controle_capital (
      date     DATE          NOT NULL,
      controle VARCHAR(30)   NOT NULL,
      metrica  VARCHAR(30)   NOT NULL,
      value    DECIMAL(15,5),
      PRIMARY KEY (date, controle, metrica)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

import pandas as pd

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "cred_credito_controle_capital"

_CODES_SALDO = {
    "publicas":            2007,
    "privadas_nacionais":  12106,
    "estrangeiras":        12150,
}
_CODES_INADIMPLENCIA = {
    "publicas":            13667,
    "privadas_nacionais":  13673,
    "estrangeiras":        13679,
}
_CODES_PROVISOES = {
    "publicas":            13666,
    "privadas_nacionais":  13672,
    "estrangeiras":        13678,
}

_bcb = BCB()


def _fetch_metrica(metrica: str, codes: dict, start: str | None, end: str | None, n_meses: int) -> pd.DataFrame:
    if start:
        df = _bcb.get_sgs(codes, start=start, end=end)
    else:
        df = _bcb.get_sgs_ultimos(codes, n=n_meses)
    df = df.rename(columns={"name": "controle"})
    df["metrica"] = metrica
    return df[["date", "controle", "metrica", "value"]]


def run(n_meses: int = 24, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.cred_credito_controle_capital.

    Args:
        n_meses: ultimos N meses (default 24). Ignorado se start/end fornecidos.
        start:   data inicial no formato "DD/MM/YYYY", ou "all" para serie completa.
        end:     data final no formato "DD/MM/YYYY". Default: hoje.
    """
    frames = [
        _fetch_metrica("saldo", _CODES_SALDO, start, end, n_meses),
        _fetch_metrica("inadimplencia", _CODES_INADIMPLENCIA, start, end, n_meses),
        _fetch_metrica("provisoes", _CODES_PROVISOES, start, end, n_meses),
    ]
    df = pd.concat(frames, ignore_index=True)
    insert_data_into_database(_DATABASE, _TABLE, df)
