"""
Reservas internacionais e intervenções cambiais do BCB.

Schema macro_brasil.reservas:
  PRIMARY KEY (date, sgs_code)
  Colunas: date DATE | sgs_code INT | name VARCHAR | value DECIMAL

  sgs_code é o identificador canônico (imutável); name é rótulo legível.

DDL:
  DROP TABLE IF EXISTS macro_brasil.reservas;
  CREATE TABLE macro_brasil.reservas (
      date      DATE           NOT NULL,
      sgs_code  INT            NOT NULL,
      name      VARCHAR(100)   NOT NULL,
      value     DECIMAL(20,6),
      PRIMARY KEY (date, sgs_code)
  );

Series SGS — reservas mensais (M):
  3546  reserves_total_monthly          — Total - monthly (USD MM)
  3547  reserves_fx_total               — Foreign currency reserves (convertible) - Total (USD MM)
  3548  reserves_fx_securities          — Foreign currency reserves - Securities (USD MM)
  3549  reserves_fx_currency_deposits   — Foreign currency reserves - Currency and deposits (USD MM)
  3550  reserves_imf_position           — IMF reserve position (USD MM)
  3551  reserves_sdrs                   — SDRs (USD MM)
  3552  reserves_gold_usd               — Gold incl. deposits (USD MM)
  3553  reserves_gold_volume            — Gold volume (troy oz thousand) ← unidade diferente
  3554  reserves_other_total            — Other reserve assets - Total (USD MM)
  3555  reserves_other_derivatives      — Other reserve assets - Financial derivatives (USD MM)
  3556  reserves_other_loans            — Other reserve assets - Loans to nonbank nonresidents (USD MM)
  7323  reserves_other_reverse_repo     — Other reserve assets - Reverse Repo (USD MM)
  21195 bank_fx_spot_position           — Posição de câmbio dos bancos no mercado à vista — net (USD MM)
  29533 bcb_swap_cambial_position        — Swap cambial BCB — posição líquida (USD MM); negativo = BCB vendeu swap ao mercado
  29534 bcb_fx_stock_repos_loans        — Stock of repurchase lines, loans and repos in FX (USD MM)
  29535 bcb_fx_other_assets_liabilities — Other assets/liabilities on BCB balance sheet (USD MM)

Series SGS — reservas diárias (D):
  13621 reserves_total_daily            — Total - daily (USD MM); desde 1998
  13982 reserves_liquidity_daily        — Liquidity concept - Total - daily (USD MM); desde 2008

Series SGS — intervenções BCB diárias (D):
  17843 bcb_intervention_spot           — Spot net interventions – settled (USD MM); desde 1999
  24425 bcb_intervention_forwards       — Forwards net interventions – settled (USD MM); desde 1999
  24427 bcb_intervention_fx_loans_repos — FX loans and FX repos – settled (USD MM); desde 1999
  24448 bcb_intervention_repo_lines     — Repo lines of credit – settled (USD MM); desde 1999

Frequências mistas numa única tabela: a PK (date, sgs_code) acomoda sem conflito.
Intervenções BCB são líquidas (net): positivo = BCB comprando USD, negativo = vendendo.
Séries diárias: a API BCB rejeita janelas muito longas (406). Carga histórica usa
chunking anual via _fetch_daily_chunked().
"""

import logging
from datetime import datetime, timedelta

import pandas as pd

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

logger = logging.getLogger(__name__)

_DATABASE = "macro_brasil"
_TABLE    = "reservas"

_SERIES_MONTHLY = {
    "reserves_total_monthly":           3546,
    "reserves_fx_total":                3547,
    "reserves_fx_securities":           3548,
    "reserves_fx_currency_deposits":    3549,
    "reserves_imf_position":            3550,
    "reserves_sdrs":                    3551,
    "reserves_gold_usd":                3552,
    "reserves_gold_volume":             3553,
    "reserves_other_total":             3554,
    "reserves_other_derivatives":       3555,
    "reserves_other_loans":             3556,
    "reserves_other_reverse_repo":      7323,
    "bank_fx_spot_position":            21195,
    "bcb_swap_cambial_position":        29533,
    "bcb_fx_stock_repos_loans":         29534,
    "bcb_fx_other_assets_liabilities":  29535,
}

_SERIES_DAILY = {
    "reserves_total_daily":             13621,
    "reserves_liquidity_daily":         13982,
    "bcb_intervention_spot":            17843,
    "bcb_intervention_forwards":        24425,
    "bcb_intervention_fx_loans_repos":  24427,
    "bcb_intervention_repo_lines":      24448,
}

# Earliest available year per daily series (to avoid unnecessary empty chunks)
_DAILY_START_YEAR = {
    "reserves_total_daily":             1998,
    "reserves_liquidity_daily":         2008,
    "bcb_intervention_spot":            1999,
    "bcb_intervention_forwards":        1999,
    "bcb_intervention_fx_loans_repos":  1999,
    "bcb_intervention_repo_lines":      1999,
}

_SERIES_INTERVENTION = {
    "bcb_intervention_spot",
    "bcb_intervention_forwards",
    "bcb_intervention_fx_loans_repos",
    "bcb_intervention_repo_lines",
}

_SERIES_ALL = {**_SERIES_MONTHLY, **_SERIES_DAILY}

_bcb = BCB()


def _add_sgs_code(df: pd.DataFrame, series_dict: dict) -> pd.DataFrame:
    df = df.copy()
    df["sgs_code"] = df["name"].map(series_dict)
    return df[["date", "sgs_code", "name", "value"]]


def _drop_zero_interventions(df: pd.DataFrame) -> pd.DataFrame:
    """Remove linhas com value == 0 apenas nas séries de intervenção BCB.

    Intervenções diárias têm zero na maioria dos dias (BCB não intervém todo dia).
    Zeros são ruído — só armazenamos os dias em que houve intervenção efetiva.
    Séries de nível (reservas diárias) são mantidas intactas.
    """
    mask_intervention = df["name"].isin(_SERIES_INTERVENTION)
    mask_zero = df["value"] == 0
    return df[~(mask_intervention & mask_zero)].reset_index(drop=True)


def _fetch_daily_chunked(start_year: int, end_year: int) -> pd.DataFrame:
    """Busca séries diárias em chunks anuais para evitar 406 da API BCB."""
    frames = []
    for year in range(start_year, end_year + 1):
        chunk_start = f"01/01/{year}"
        chunk_end   = f"31/12/{year}"
        # Only fetch series whose history begins on or before this year
        series_this_year = {
            name: code
            for name, code in _SERIES_DAILY.items()
            if _DAILY_START_YEAR.get(name, 1970) <= year
        }
        if not series_this_year:
            continue
        logger.info("Daily chunk year=%d (%d series)", year, len(series_this_year))
        chunk = _bcb.get_sgs(series_this_year, start=chunk_start, end=chunk_end)
        if not chunk.empty:
            frames.append(chunk)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def run(n_meses: int = 3, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.reservas.

    Args:
        n_meses: ultimos N meses para atualização rotineira (default 3).
                 Para séries diárias, 3 meses ≈ 65 obs por série.
                 Ignorado se start/end fornecidos.
        start:   data inicial no formato "DD/MM/YYYY", ou "all" para série completa.
                 Carga histórica: run(start="all")
        end:     data final no formato "DD/MM/YYYY". Default: hoje.
    """
    today = datetime.now()

    if start == "all":
        # Mensais: fetch completo desde o início (sem problema de 406)
        df_monthly = _bcb.get_sgs(_SERIES_MONTHLY, start="all")

        # Diárias: chunking anual para evitar 406
        min_start_year = min(_DAILY_START_YEAR.values())
        df_daily = _fetch_daily_chunked(
            start_year=min_start_year,
            end_year=today.year,
        )
        frames = [f for f in [df_monthly, df_daily] if not f.empty]
        df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    elif start:
        # Range específico: mensais normal, diárias com chunk anual se range > 4 anos
        df_monthly = _bcb.get_sgs(_SERIES_MONTHLY, start=start, end=end)

        start_dt = datetime.strptime(start, "%d/%m/%Y")
        end_dt   = datetime.strptime(end, "%d/%m/%Y") if end else today
        years_span = (end_dt - start_dt).days / 365

        if years_span > 4:
            df_daily = _fetch_daily_chunked(start_dt.year, end_dt.year)
        else:
            df_daily = _bcb.get_sgs(_SERIES_DAILY, start=start, end=end)

        frames = [f for f in [df_monthly, df_daily] if not f.empty]
        df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    else:
        # Rotina: janela recente, sem problema de 406
        df = _bcb.get_sgs_ultimos(_SERIES_ALL, n=n_meses)

    df = _add_sgs_code(df, _SERIES_ALL)
    df = _drop_zero_interventions(df)
    insert_data_into_database(_DATABASE, _TABLE, df)
