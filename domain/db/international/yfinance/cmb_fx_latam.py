"""
Cotacao diaria das moedas latino-americanas pares (MX/CL/CO/PE) contra o USD --
Yahoo Finance. Nao alimenta nenhum relatorio diretamente; e o insumo de
volatilidade cambial para o metrico carry/vol em
analytics/exchange_rate/models/ppp_equilibrium.py (relative_carry_vol),
o mesmo papel que cmb_ptax ja cumpre para o lado brasileiro.

Serie Yahoo Finance (diaria, fechamento), moeda local por USD -- mesma
convencao de cotacao do PTAX (maior = moeda local mais fraca):
  MX  MXN=X
  CL  CLP=X
  CO  COP=X
  PE  PEN=X

Nao inclui AR -- mesma exclusao ja aplicada em cmb_policy_rates.py (regime
idiossincratico, BIS parou de atualizar a taxa de politica monetaria em
2025-07; nao ha razao para tratar o cambio de forma diferente aqui).

Cobertura real por ticker no Yahoo Finance (verificado 2026-07-28):
  MXN=X desde 2003-12, CLP=X desde 2003-12, COP=X desde 2003-01,
  PEN=X desde 2001-05 -- todos anteriores a 2007-12, a restricao vinculante
  real do modelo Bayesiano (fiscal/CDS), entao nenhum encolhe a amostra.

Banco: macro_international.cmb_fx_latam
Schema: PRIMARY KEY (date, country_code)
"""

import pandas as pd

from connectors.yfinance import get_history
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_international"
_TABLE = "cmb_fx_latam"

_TICKERS = {"MX": "MXN=X", "CL": "CLP=X", "CO": "COP=X", "PE": "PEN=X"}


def run(start: str = "2000-01-01", end: str | None = None) -> None:
    """Atualiza macro_international.cmb_fx_latam.

    Args:
        start: data inicial ISO "YYYY-MM-DD". Default antecede o inicio real
               de todos os 4 tickers -- cada get_history() so retorna o que
               o Yahoo Finance realmente tem.
        end:   data final ISO "YYYY-MM-DD". Default: hoje.
    """
    frames = []
    for country, ticker in _TICKERS.items():
        df = get_history(ticker, start=start, end=end)
        df["country_code"] = country
        frames.append(df)

    out = pd.concat(frames, ignore_index=True)
    out = out[["date", "country_code", "value"]].dropna(subset=["value"])
    insert_data_into_database(_DATABASE, _TABLE, out)
