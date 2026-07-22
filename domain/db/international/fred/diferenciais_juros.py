"""
Diferenciais de juros Brasil x EUA (nominal e real ex-post)

Series brutas:
  BCB SGS 432   — Selic — meta mensal (% a.a.)
  BCB SGS 13522 — IPCA acumulado 12 meses (%)
  FRED FEDFUNDS — Fed Funds effective rate (% a.a.)
  FRED CPIAUCSL — CPI EUA (indice, para calculo de variacao 12m)

Series derivadas (calculadas no script):
  diferencial_nominal — selic - fed_funds
  real_br_ex_post     — selic - ipca_12m
  real_us_ex_post     — fed_funds - cpi_12m_us
  diferencial_real    — real_br_ex_post - real_us_ex_post

Banco: macro_international.diferenciais_juros

Movida de macro_analytics em 2026-07 — schema dedicado a series "calculadas"
foi descontinuado (tinha essa unica tabela, e ela ja precisa de dados de mais
de um pais para existir, o que a qualifica para macro_international pela
propria regra original de organizacao). Ver domain/db/CLAUDE.md.

Nota: os inputs brutos (selic, ipca_12m, fed_funds, cpi_12m_us) sao armazenados
junto com os diferenciais para manter a tabela auto-contida para a analise
cambial — denormalizacao intencional.

TODO (proxima fase): diferenciais ex-ante usando Focus (macro_brasil.expc_focus)
e taxa implicita nos Fed Funds futuros.
"""

import os
from datetime import datetime, timedelta

import pandas as pd
from dotenv import load_dotenv
from fredapi import Fred

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

load_dotenv()

_DATABASE = "macro_international"
_TABLE    = "diferenciais_juros"

_BCB_SERIES = {
    "selic":    432,    # Selic meta mensal (% a.a.)
    "ipca_12m": 13522,  # IPCA acumulado 12 meses (%)
}

_SELIC_CHUNK_DAYS = 8 * 365  # janela segura: SGS 432 (serie diaria) retorna 406 acima de ~10 anos

_bcb = BCB()


def _to_fred_date(bcb_date: str) -> str:
    """Converte "DD/MM/YYYY" para "YYYY-MM-DD"."""
    return datetime.strptime(bcb_date, "%d/%m/%Y").strftime("%Y-%m-%d")


def _from_n_meses(n_meses: int) -> str:
    """Retorna data inicial em formato BCB para os ultimos N meses."""
    dt = datetime.now() - timedelta(days=n_meses * 31)
    return dt.strftime("%d/%m/%Y")


def _fetch_bcb_chunked(start_bcb: str) -> pd.DataFrame:
    """Busca Selic (432) + IPCA 12m (13522) do BCB, encadeando em janelas de
    ate ~8 anos quando o intervalo total excede isso.

    SGS 432 e serie diaria (meta Selic vigente por dia) e a API BCB retorna
    406 Not Acceptable para intervalos > ~10 anos nesse endpoint — 13522
    (mensal) nao tem esse problema, mas encadear os dois junto simplifica o
    codigo sem custo extra (poucas paginas mensais a mais nao pesam).
    """
    start_dt = datetime.strptime(start_bcb, "%d/%m/%Y")
    end_dt = datetime.now()

    if (end_dt - start_dt).days <= _SELIC_CHUNK_DAYS:
        return _bcb.get_sgs(_BCB_SERIES, start=start_bcb)

    frames = []
    chunk_start = start_dt
    while chunk_start < end_dt:
        chunk_end = min(chunk_start + timedelta(days=_SELIC_CHUNK_DAYS), end_dt)
        frames.append(
            _bcb.get_sgs(
                _BCB_SERIES,
                start=chunk_start.strftime("%d/%m/%Y"),
                end=chunk_end.strftime("%d/%m/%Y"),
            )
        )
        chunk_start = chunk_end + timedelta(days=1)

    return pd.concat(frames, ignore_index=True).drop_duplicates(subset=["date", "name"])


def run(n_meses: int = 36, start: str | None = None) -> None:
    """Atualiza macro_international.diferenciais_juros.

    Args:
        n_meses: ultimos N meses (default 36). Ignorado se start fornecido.
        start:   data inicial no formato "DD/MM/YYYY", ou "all" para serie completa.
    """
    start_bcb = start if start and start != "all" else (
        "01/01/1995" if start == "all" else _from_n_meses(n_meses)
    )
    start_iso = _to_fred_date(start_bcb)

    # CPI precisa de 12 meses extras para calcular variacao YoY
    cpi_start_iso = (
        datetime.strptime(start_iso, "%Y-%m-%d") - timedelta(days=400)
    ).strftime("%Y-%m-%d")

    # --- Fetch BCB (Selic + IPCA) ---
    bcb_df = _fetch_bcb_chunked(start_bcb)
    bcb_wide = bcb_df.pivot(index="date", columns="name", values="value")

    # --- Fetch FRED ---
    fred = Fred(api_key=os.environ.get("FRED_API_KEY", ""))
    fed_funds_raw = fred.get_series("FEDFUNDS", observation_start=start_iso)
    cpi_raw       = fred.get_series("CPIAUCSL", observation_start=cpi_start_iso)

    # Resample to month-start to align with BCB dates
    fed_funds_m = fed_funds_raw.resample("MS").last().rename("fed_funds")
    cpi_m       = cpi_raw.resample("MS").last()

    # CPI YoY % change
    cpi_yoy = (cpi_m.pct_change(12, fill_method=None) * 100).rename("cpi_12m_us")

    # Resample BCB series to month-start so all series share the same frequency
    # (Selic/432 uses COPOM meeting dates; IPCA/13522 uses period-end or similar)
    bcb_wide.index = pd.to_datetime(bcb_wide.index)
    bcb_ms = bcb_wide.resample("MS").last()

    # --- Combine into wide DataFrame ---
    df = pd.concat([bcb_ms, fed_funds_m, cpi_yoy], axis=1)
    df.index = pd.to_datetime(df.index)
    df.index.name = "date"

    # Filter to requested window (cpi_yoy extends further back due to 12m lag)
    df = df[df.index >= start_iso]

    # --- Derive differentials ---
    df["diferencial_nominal"] = df["selic"] - df["fed_funds"]
    df["real_br_ex_post"]     = df["selic"] - df["ipca_12m"]
    df["real_us_ex_post"]     = df["fed_funds"] - df["cpi_12m_us"]
    df["diferencial_real"]    = df["real_br_ex_post"] - df["real_us_ex_post"]

    # --- Unpivot to tidy format (date, name, value) ---
    df_tidy = (
        df.reset_index()
        .melt(id_vars="date", var_name="name", value_name="value")
        .dropna(subset=["value"])
    )
    df_tidy["date"] = pd.to_datetime(df_tidy["date"])

    insert_data_into_database(_DATABASE, _TABLE, df_tidy)
