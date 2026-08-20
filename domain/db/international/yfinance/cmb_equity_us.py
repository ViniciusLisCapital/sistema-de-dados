"""
S&P 500 (indice, fechamento) — proxy de "competicao por capital" para o modelo
cambial: um S&P mais forte atrai capital para equities americanas, pressionando
o USD/BRL para cima independentemente de qualquer canal especifico do Brasil
(mesmo papel estrutural que dxy/dxy_em jogam, mas do lado da renda variavel,
nao do cambio/juros).

Serie Yahoo Finance (diaria, fechamento):
  sp500 ^GSPC — S&P 500 Index

Preferido ao FRED SP500 por ter historico completo desde 1990 — a serie do
FRED so cobre uma janela rolante de ~10 anos (2016-08+ no momento em que isto
foi escrito), o que criaria uma restricao vinculante nova e desnecessaria
neste modelo.

Testado 2026-07-31 como canal exploratorio no ridge_deviation_model.py antes
de ser ingerido aqui — delta_sp500 (retorno log mensal) melhorou o MSE
out-of-sample (walk-forward) em ~4% sobre o modelo shrunk_em_real já
embarcado, com coeficiente positivo e estavel (nunca cruza zero em nenhuma das
163 janelas rolantes) — ver analytics/brasil/exchange_rate/CLAUDE.md para o registro
completo. VIX (FRED VIXCLS) e o rendimento real de 10 anos dos EUA (FRED
DFII10) foram testados junto mas NAO melhoraram o OOS MSE — nao ingeridos.

Colocado em macro_international (nao macro_brasil) pela mesma logica aplicada
a cmb_dollar_index/cmb_fx_latam — nao e dado especifico do Brasil.

Banco: macro_international.cmb_equity_us — PRIMARY KEY (date, name)
"""

from connectors.yfinance import get_history
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_international"
_TABLE    = "cmb_equity_us"
_TICKER   = "^GSPC"


def run(start: str = "1990-01-01", end: str | None = None) -> None:
    """Atualiza macro_international.cmb_equity_us.

    Args:
        start: data inicial ISO "YYYY-MM-DD". Default: serie completa (inicio do Yahoo Finance).
        end:   data final ISO "YYYY-MM-DD". Default: hoje.
    """
    df = get_history(_TICKER, start=start, end=end)
    df["name"] = "sp500"
    df = df[["date", "name", "value"]].dropna(subset=["value"])

    insert_data_into_database(_DATABASE, _TABLE, df)
