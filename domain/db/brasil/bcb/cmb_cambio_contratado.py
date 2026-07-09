"""
Câmbio contratado — movimento de câmbio entre bancos e clientes (BCB).

Fonte: BCB Indicadores Econômicos Selecionados, Tabelas 13 e 14.

Schema macro_brasil.cmb_cambio_contratado:
  PRIMARY KEY (date, sgs_code)
  Colunas: date DATE | sgs_code INT | name VARCHAR(100) | value DECIMAL(20,6)

DDL:
  DROP TABLE IF EXISTS macro_brasil.cmb_cambio_contratado;
  CREATE TABLE macro_brasil.cmb_cambio_contratado (
      date      DATE           NOT NULL,
      sgs_code  INT            NOT NULL,
      name      VARCHAR(100)   NOT NULL,
      value     DECIMAL(20,6),
      PRIMARY KEY (date, sgs_code)
  );

Tabela 13 — Movimento de câmbio contratado (DIÁRIO, desde set/2008, US$ milhões):
  13961  cc_saldo_total      — Saldo total c = (a+b)
  13962  cc_export_total     — Exportação de bens - Total
  13963  cc_export_acc       — Exportação - Adiantamento de Contrato de Câmbio (ACC)
  13964  cc_export_pa        — Exportação - Pagamento Antecipado (PA)
  13965  cc_export_outros    — Exportação - Demais
  13966  cc_import_total     — Importação de bens
  13967  cc_saldo_comercial  — Saldo comercial (a)
  13968  cc_fin_compras      — Financeiro - Compras (total)
  13969  cc_fin_vendas       — Financeiro - Vendas (total)
  13970  cc_fin_saldo        — Financeiro - Saldo (b)

Tabela 14 — Câmbio contratado financeiro detalhado (MENSAL, US$ milhões):
  11050  cc_fin_saldo_det  — Saldo financeiro detalhado (desde 2000)
  29561  cc_fin_servicos   — Serviços
  29562  cc_fin_rendas     — Rendas primária e secundária
  29563  cc_fin_cap_bras   — Capitais brasileiros
  29564  cc_fin_cap_ext    — Capitais estrangeiros

Séries diárias: API BCB rejeita janelas longas (406). Carga histórica usa
chunking anual via _fetch_daily_chunked().
"""

import logging
from datetime import datetime

import pandas as pd

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

logger = logging.getLogger(__name__)

_DATABASE = "macro_brasil"
_TABLE    = "cmb_cambio_contratado"

_SERIES_DAILY = {
    "cc_saldo_total":       13961,
    "cc_export_total":      13962,
    "cc_export_acc":        13963,
    "cc_export_pa":         13964,
    "cc_export_outros":     13965,
    "cc_import_total":      13966,
    "cc_saldo_comercial":   13967,
    "cc_fin_compras":       13968,
    "cc_fin_vendas":        13969,
    "cc_fin_saldo":         13970,
}

_SERIES_MONTHLY = {
    "cc_fin_saldo_det":     11050,
    "cc_fin_servicos":      29561,
    "cc_fin_rendas":        29562,
    "cc_fin_cap_bras":      29563,
    "cc_fin_cap_ext":       29564,
}

_DAILY_START_YEAR = 2008  # set/2008

_SERIES_ALL = {**_SERIES_DAILY, **_SERIES_MONTHLY}

_bcb = BCB()


def _add_sgs_code(df: pd.DataFrame, series_dict: dict) -> pd.DataFrame:
    df = df.copy()
    df["sgs_code"] = df["name"].map(series_dict)
    return df[["date", "sgs_code", "name", "value"]]


def _fetch_daily_chunked(start_year: int, end_year: int) -> pd.DataFrame:
    """Busca séries diárias em chunks anuais para evitar 406 da API BCB."""
    frames = []
    for year in range(start_year, end_year + 1):
        logger.info("Daily chunk year=%d", year)
        chunk = _bcb.get_sgs(_SERIES_DAILY,
                             start=f"01/01/{year}", end=f"31/12/{year}")
        if not chunk.empty:
            frames.append(chunk)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def run(n_meses: int = 3, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.cmb_cambio_contratado.

    Args:
        n_meses: últimos N meses para atualização rotineira (default 3).
                 Ignorado se start/end fornecidos.
        start:   "DD/MM/YYYY" ou "all" para série completa.
        end:     "DD/MM/YYYY". Default: hoje.
    """
    today = datetime.now()

    if start == "all":
        df_monthly = _bcb.get_sgs(_SERIES_MONTHLY, start="all")
        df_daily = _fetch_daily_chunked(_DAILY_START_YEAR, today.year)
        frames = [f for f in [df_monthly, df_daily] if not f.empty]
        df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    elif start:
        df_monthly = _bcb.get_sgs(_SERIES_MONTHLY, start=start, end=end)
        start_dt = datetime.strptime(start, "%d/%m/%Y")
        end_dt   = datetime.strptime(end, "%d/%m/%Y") if end else today
        if (end_dt - start_dt).days / 365 > 4:
            df_daily = _fetch_daily_chunked(start_dt.year, end_dt.year)
        else:
            df_daily = _bcb.get_sgs(_SERIES_DAILY, start=start, end=end)
        frames = [f for f in [df_monthly, df_daily] if not f.empty]
        df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    else:
        df = _bcb.get_sgs_ultimos(_SERIES_ALL, n=n_meses)

    df = _add_sgs_code(df, _SERIES_ALL)
    insert_data_into_database(_DATABASE, _TABLE, df)
