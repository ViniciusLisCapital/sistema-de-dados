"""
Expectativas - Pesquisa Focus de Expectativas de Mercado (BCB/Olinda)

Consultas configuradas (endpoint, indicador, horizonte, filtros):
  IPCA  12m  : ExpectativasMercadoInflacao12Meses — suavizado, base 0
  IPCA  24m  : ExpectativasMercadoInflacao24Meses — suavizado, base 0
  IGP-M 12m  : ExpectativasMercadoInflacao12Meses — suavizado, base 0
  Selic eop  : ExpectativasMercadoSelic           — base 0 (sem campo Suavizada)

Banco: brasil.expectativas (date, indicador, horizonte, media, mediana, ...)
"""

import pandas as pd

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "expectativas"

_CAMPOS_INFLACAO = [
    "Data", "Media", "Mediana", "DesvioPadrao", "Minimo", "Maximo", "numeroRespondentes",
]
_CAMPOS_SELIC = [
    "Data", "Reuniao", "Media", "Mediana", "DesvioPadrao", "Minimo", "Maximo", "numeroRespondentes",
]

# (endpoint, indicador, horizonte, campos, filtros_extras)
_CONSULTAS = [
    (
        "ExpectativasMercadoInflacao12Meses", "IPCA", "12m",
        _CAMPOS_INFLACAO,
        "Suavizada eq 'S' and baseCalculo eq 0",
    ),
    (
        "ExpectativasMercadoInflacao12Meses", "IGP-M", "12m",
        _CAMPOS_INFLACAO,
        "Suavizada eq 'S' and baseCalculo eq 0",
    ),
    (
        "ExpectativasMercadoInflacao24Meses", "IPCA", "24m",
        _CAMPOS_INFLACAO,
        "Suavizada eq 'S' and baseCalculo eq 0",
    ),
    (
        "ExpectativasMercadoSelic", "Selic", "eop",
        _CAMPOS_SELIC,
        "baseCalculo eq 0",   # endpoint Selic nao tem campo Suavizada
    ),
]

_bcb = BCB()


def run(start: str | None = None, n_dias: int = 90) -> None:
    """Atualiza brasil.expectativas para todos os indicadores configurados.

    Args:
        start:  data inicial no formato ISO "YYYY-MM-DD".
                Default: ultimos n_dias dias (atualizacao rotineira).
                Use start="2000-01-01" para carga historica completa.
        n_dias: janela retroativa usada quando start=None (default: 90 dias).
    """
    from datetime import datetime, timedelta
    if start is None:
        start = (datetime.now() - timedelta(days=n_dias)).strftime("%Y-%m-%d")
    frames = []
    for endpoint, indicador, horizonte, campos, filtros in _CONSULTAS:
        df = _bcb.get_focus(
            endpoint=endpoint,
            indicador=indicador,
            campos=campos,
            start=start,
            filtros_extras=filtros,
            orderby="Data asc",
        )
        if df.empty:
            continue
        df["indicador"] = indicador
        df["horizonte"] = horizonte
        frames.append(df)

    if not frames:
        return

    resultado = pd.concat(frames, ignore_index=True)
    insert_data_into_database(_DATABASE, _TABLE, resultado)
