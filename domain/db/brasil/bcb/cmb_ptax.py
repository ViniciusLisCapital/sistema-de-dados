"""
PTAX (cambio a vista) e volume interbancario de cambio.

Preenche a lacuna de "nenhuma serie de cambio a vista (PTAX) no banco"
identificada em repository/agent_mapping/recommended_data/exchange_rate_data_inventory.md.

Series SGS:
  1     ptax_venda          — Taxa de cambio - Livre - Dolar americano (venda) - diario; desde 01/07/1994
  20359 fx_interbank_vol_t1 — Volume interbancario de cambio - USD - T+1; desde 04/07/1994
  20205 fx_interbank_vol_t2 — Volume interbancario de cambio - USD - T+2; desde 04/07/1994

ptax_venda so e' carregada a partir da implantacao do Plano Real (01/07/1994).
A serie SGS 1 volta ate 28/11/1984, mas em moedas extintas (Cruzeiro Real e,
antes dela, Cruzeiro/Cruzado/Cruzado Novo) — confirmado no proprio banco pela
quebra de 1994-06-30 (2750.00, Cruzeiro Real) -> 1994-07-01 (1.00, Real),
exatamente a paridade fixa de lancamento (CR$2750 = R$1). Nao comparavel ao
periodo pos-Real sem fator de conversao, que este projeto nao carrega — por
isso o corte, nao um limite tecnico da API.

Banco: macro_brasil.cmb_ptax — PRIMARY KEY (date, name)

Serie diaria: a API BCB rejeita janelas > 10 anos (406). Carga historica usa
chunking anual via _fetch_chunked(), mesmo padrao de cmb_reservas_bc.py.
"""

import logging
from datetime import date, datetime, timedelta

import pandas as pd

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

logger = logging.getLogger(__name__)

_DATABASE = "macro_brasil"
_TABLE    = "cmb_ptax"

_SERIES = {
    "ptax_venda":          1,
    "fx_interbank_vol_t1": 20359,
    "fx_interbank_vol_t2": 20205,
}

_START_YEAR = {
    "ptax_venda":          1994,
    "fx_interbank_vol_t1": 1994,
    "fx_interbank_vol_t2": 1994,
}

# Real Plan cutoff — ptax_venda before this date is denominated in an extinct
# pre-Real currency (see module docstring). Applies only to the 1994 chunk;
# later years are unaffected.
_REAL_PLAN_START = date(1994, 7, 1)

_bcb = BCB()


def _fetch_chunked(start_year: int, end_year: int) -> pd.DataFrame:
    """Busca as tres series em chunks anuais para evitar 406 da API BCB."""
    frames = []
    for year in range(start_year, end_year + 1):
        series_this_year = {
            name: code
            for name, code in _SERIES.items()
            if _START_YEAR[name] <= year
        }
        if not series_this_year:
            continue
        chunk_start = f"01/01/{year}" if year > _REAL_PLAN_START.year else _REAL_PLAN_START.strftime("%d/%m/%Y")
        chunk_end   = f"31/12/{year}"
        logger.info("cmb_ptax chunk year=%d (%d series)", year, len(series_this_year))
        chunk = _bcb.get_sgs(series_this_year, start=chunk_start, end=chunk_end)
        if not chunk.empty:
            frames.append(chunk)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def run(n_dias: int = 90, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.cmb_ptax.

    Args:
        n_dias: ultimos N dias para atualizacao rotineira (default 90). Ignorado se start/end fornecidos.
        start:  data inicial no formato "DD/MM/YYYY", ou "all" para serie completa (desde 1984).
                Carga historica: run(start="all")
        end:    data final no formato "DD/MM/YYYY". Default: hoje.
    """
    today = datetime.now()

    if start == "all":
        df = _fetch_chunked(start_year=min(_START_YEAR.values()), end_year=today.year)
    elif start:
        start_dt = datetime.strptime(start, "%d/%m/%Y")
        end_dt   = datetime.strptime(end, "%d/%m/%Y") if end else today
        if (end_dt - start_dt).days / 365 > 9:
            df = _fetch_chunked(start_dt.year, end_dt.year)
        else:
            df = _bcb.get_sgs(_SERIES, start=start, end=end)
    else:
        start_dt = today - timedelta(days=n_dias)
        df = _bcb.get_sgs(_SERIES, start=start_dt.strftime("%d/%m/%Y"), end=today.strftime("%d/%m/%Y"))

    insert_data_into_database(_DATABASE, _TABLE, df)
