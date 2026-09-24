"""Baixa os ETFs dos subindices setoriais do S&P 500 (Select Sector SPDR) e salva em Excel.

Sandbox de teste — nao escreve no MySQL, nao entra no registry, nao alimenta dashboard.
Os 11 setores GICS + o SPY como referencia do indice cheio.

Duas series por ticker, e a distincao importa para qualquer teste de retorno:
  close      — fechamento bruto (o que `connectors.yfinance.get_history` devolve,
               `auto_adjust=False`). Retorno de PRECO: nao inclui dividendo.
  adj_close  — fechamento ajustado por dividendo e split. Retorno TOTAL.
Em setor a diferenca nao e detalhe: XLU/XLP/XLE rendem 3%+ a.a. em dividendo e
XLK rende ~0,7%, entao um ranking setorial montado sobre `close` erra o sinal
sistematicamente contra os setores de dividendo alto.

Uso:
    uv run python tests/sp_sectors/pull_sector_etfs.py [--start 1998-12-16] [--end YYYY-MM-DD]

Saida: tests/sp_sectors/sp_sector_etfs.xlsx
    close       — wide, data x ticker (fechamento bruto)
    adj_close   — wide, data x ticker (ajustado; base de retorno total)
    long        — formato longo (date, ticker, setor, close, adj_close)
    metadados   — ticker, setor, inicio/fim efetivos, n obs, fonte
"""

import argparse
from pathlib import Path

import pandas as pd
import yfinance as yf

from connectors.yfinance import get_history

# Select Sector SPDR — um ETF por setor GICS do S&P 500, mais o indice cheio.
# XLRE (2015-10) e XLC (2018-06) nasceram depois dos outros nove (1998-12),
# porque Real Estate e Communication Services sairam de Financials e de
# Technology/Consumer Discretionary em reclassificacoes posteriores do GICS.
_ETFS = {
    "SPY":  "S&P 500 (indice cheio)",
    "XLB":  "Materials",
    "XLC":  "Communication Services",
    "XLE":  "Energy",
    "XLF":  "Financials",
    "XLI":  "Industrials",
    "XLK":  "Information Technology",
    "XLP":  "Consumer Staples",
    "XLRE": "Real Estate",
    "XLU":  "Utilities",
    "XLV":  "Health Care",
    "XLY":  "Consumer Discretionary",
}

_OUT = Path(__file__).parent / "sp_sector_etfs.xlsx"


def _adj_close(ticker: str, start: str, end: str | None) -> pd.DataFrame:
    """Fechamento AJUSTADO (dividendo + split) — o connector so devolve o bruto.

    Mesma chamada de `connectors.yfinance.get_history`, com `auto_adjust=True`:
    ai o Yahoo devolve a serie ja ajustada na propria coluna `Close`.
    """
    df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
    df = df["Close"][[ticker]].reset_index()
    df.columns = ["date", "value"]
    return df


def run(start: str = "1998-12-16", end: str | None = None) -> Path:
    close_parts, adj_parts, meta = [], [], []

    for ticker, setor in _ETFS.items():
        bruto = get_history(ticker, start=start, end=end).dropna(subset=["value"])
        ajust = _adj_close(ticker, start=start, end=end).dropna(subset=["value"])

        close_parts.append(bruto.assign(ticker=ticker))
        adj_parts.append(ajust.assign(ticker=ticker))

        meta.append({
            "ticker": ticker,
            "setor": setor,
            "inicio": bruto["date"].min().date() if len(bruto) else None,
            "fim": bruto["date"].max().date() if len(bruto) else None,
            "n_obs": len(bruto),
            "fonte": "Yahoo Finance (connectors.yfinance)",
        })
        print(f"{ticker:<5} {setor:<28} {len(bruto):>6} obs  "
              f"{meta[-1]['inicio']} -> {meta[-1]['fim']}")

    close = pd.concat(close_parts).pivot(index="date", columns="ticker", values="value")
    adj = pd.concat(adj_parts).pivot(index="date", columns="ticker", values="value")
    # Ordem do dict, nao alfabetica: SPY primeiro, setores depois.
    cols = [t for t in _ETFS if t in close.columns]
    close, adj = close[cols], adj[cols]

    longo = (close.stack().rename("close").to_frame()
             .join(adj.stack().rename("adj_close"), how="outer")
             .reset_index())
    longo["setor"] = longo["ticker"].map(_ETFS)
    longo = longo[["date", "ticker", "setor", "close", "adj_close"]].sort_values(["date", "ticker"])

    with pd.ExcelWriter(_OUT, engine="openpyxl", datetime_format="YYYY-MM-DD") as xls:
        close.reset_index().to_excel(xls, sheet_name="close", index=False)
        adj.reset_index().to_excel(xls, sheet_name="adj_close", index=False)
        longo.to_excel(xls, sheet_name="long", index=False)
        pd.DataFrame(meta).to_excel(xls, sheet_name="metadados", index=False)

    print(f"\n{_OUT}  ({len(close)} pregoes, {len(cols)} tickers)")
    return _OUT


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--start", default="1998-12-16", help="data inicial ISO (default: inception dos 9 originais)")
    ap.add_argument("--end", default=None, help="data final ISO (default: hoje)")
    a = ap.parse_args()
    run(start=a.start, end=a.end)
