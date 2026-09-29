"""
Acesso a dados do relatorio de Politica Monetaria: uma consulta SQL, uma serie `date, value`
e o painel anual da Focus.

Copiados de `analytics/brasil/structural_model/modelo_agregado/modelo_painel.py` em 2026-09-24,
quando o modelo agregado saiu desta pasta. A copia e deliberada: a pasta de Politica Monetaria
guarda so o relatorio, e importar estas tres funcoes de la faria o relatorio depender do
modelo de novo. Sao funcoes de leitura, sem estado de modelo nenhum.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from connectors.mysql import MySQLDataRequester


def q(db: str, sql: str) -> pd.DataFrame:
    req = MySQLDataRequester(db, "x")
    req.connect()
    try:
        df = pd.read_sql(sql, req.connection)
        df.columns = [str(c).lower() for c in df.columns]
        return df
    finally:
        req.close_connection()


def serie(db: str, tab: str, name: str | None = None) -> pd.Series:
    w = "" if name is None else " WHERE name='%s'" % name
    d = q(db, "SELECT date, value FROM %s%s ORDER BY date" % (tab, w))
    d["date"] = pd.to_datetime(d["date"])
    return d.set_index("date")["value"].astype(float).sort_index()


_FA: pd.DataFrame | None = None


def focus_anual() -> pd.DataFrame:
    """Painel anual do Focus (Selic, IPCA, PIB Total) com o horizonte em anos.

    Selic e fim de periodo -> horizonte (ref+1-ano); IPCA e PIB sao acumulados no ano
    -> horizonte (ref+0,5-ano).
    """
    global _FA
    if _FA is None:
        d = q("macro_brasil", "SELECT date, indicador, data_referencia, mediana "
                              "FROM expc_focus_periodo WHERE indicador IN "
                              "('Selic','IPCA','PIB Total') AND periodicidade='anual' "
                              "AND base_calculo=0 ORDER BY date")
        d["date"] = pd.to_datetime(d["date"])
        d["ref"] = d["data_referencia"].astype(int)
        d["mediana"] = d["mediana"].astype(float)
        ano = d["date"].dt.year + (d["date"].dt.dayofyear - 1) / 365.25
        d["h"] = np.where(d["indicador"] == "Selic", d["ref"] + 1.0, d["ref"] + 0.5) - ano
        _FA = d
    return _FA
