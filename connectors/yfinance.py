"""Cliente parametrico para o Yahoo Finance (via pacote `yfinance`)."""

import pandas as pd
import yfinance as yf


def get_history(ticker: str, start: str, end: str | None = None) -> pd.DataFrame:
    """Baixa o historico diario de fechamento de um ticker do Yahoo Finance.

    Args:
        ticker: simbolo Yahoo Finance (ex: "DX-Y.NYB").
        start:  data inicial ISO "YYYY-MM-DD".
        end:    data final ISO "YYYY-MM-DD". Default: ate hoje.

    Returns:
        pd.DataFrame com colunas ["date", "value"] (value = Close).
    """
    df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=False)

    df = df["Close"][[ticker]].reset_index()
    df.columns = ["date", "value"]

    return df
