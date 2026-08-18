"""
Nucleo compartilhado dos tres scripts de expectativas Focus (BCB/Olinda).

Os tres — `expc_focus` (horizonte movel), `expc_focus_copom` (caminho da Selic por
reuniao) e `expc_focus_periodo` (periodo de referencia fixo) — leem endpoints
diferentes, com chaves diferentes, mas compartilham a mesma mecanica de carga:

  1. varredura por janela de UM MES, nao por indicador. A API cobra `$skip` cada
     vez mais caro conforme a pagina avanca, e a ordenacao por `Data` nao tem
     desempate — paginar 2 milhoes de linhas com skip crescente e lento e nao da
     garantia de nao pular linha. Janela mensal cabe numa pagina so (o endpoint
     mais denso, `ExpectativaMercadoMensais`, da ~4.200 linhas/mes contra o
     `$top` de 5.000), entao na pratica o skip nunca sai de zero. O laco de
     paginacao do connector continua ali como rede de seguranca.
  2. insercao incremental, uma janela por vez. Carga historica completa da
     `expc_focus_periodo` sao ~2,3 milhoes de linhas e varias centenas de
     requests — se quebrar no meio, o que ja entrou fica (mesmo racional do
     `backfill()` de `domain/db/brasil/mdic/cmb_comex_pais.py`).

Nao expoe `_TABLE`/`run()` de proposito: o prefixo `_` mantem o arquivo fora da
varredura de `domain/db/registry.py`, como `domain/db/brasil/mte/_caged_core.py`.
"""

from __future__ import annotations

import logging
from typing import Callable

import pandas as pd

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

logger = logging.getLogger(__name__)

DATABASE = "macro_brasil"

# 120s (contra os 30s do default): as janelas sem filtro de indicador trazem
# milhares de linhas e o Olinda responde devagar sob carga.
_bcb = BCB(timeout=120.0)


def janelas_mensais(start: str, end: str) -> list[tuple[str, str]]:
    """Divide [start, end] em janelas de um mes calendario.

    A janela e ancorada no inicio do mes, entao um `start` no meio do mes puxa o
    mes inteiro. Isso e de proposito: a insercao e upsert, reprocessar alguns dias
    a mais nao custa nada, e alinhar as janelas ao calendario mantem o log
    comparavel entre execucoes.
    """
    ini = pd.Timestamp(start).normalize().replace(day=1)
    fim = pd.Timestamp(end).normalize()
    out: list[tuple[str, str]] = []
    while ini <= fim:
        prox = ini + pd.offsets.MonthBegin(1)
        ultimo = min(prox - pd.Timedelta(days=1), fim)
        out.append((ini.strftime("%Y-%m-%d"), ultimo.strftime("%Y-%m-%d")))
        ini = prox
    return out


def carregar(
    endpoint: str,
    table: str,
    transformar: Callable[[pd.DataFrame], pd.DataFrame],
    *,
    start: str,
    end: str,
    filtros_extras: str = "",
) -> int:
    """Varre `endpoint` mes a mes, aplica `transformar` e insere cada janela.

    Args:
        endpoint:       recurso OData do Focus.
        table:          tabela destino em `macro_brasil`.
        transformar:    recebe o DataFrame cru da janela (colunas em snake_case,
                        `date` como Timestamp) e devolve as linhas prontas para o
                        banco. Devolver DataFrame vazio descarta a janela.
        start / end:    limites ISO "YYYY-MM-DD".
        filtros_extras: clausulas OData adicionais repassadas ao connector.

    Returns:
        Total de linhas inseridas.
    """
    total = 0
    for ini, fim in janelas_mensais(start, end):
        raw = _bcb.get_focus(
            endpoint,
            start=ini,
            end=fim,
            filtros_extras=filtros_extras,
            orderby="Data asc",
        )
        if raw.empty:
            continue
        df = transformar(raw)
        if df.empty:
            continue
        insert_data_into_database(DATABASE, table, df)
        total += len(df)
        logger.info("%s %s: %d linhas (acumulado %d)", table, ini[:7], len(df), total)
    return total


def janela_default(n_dias: int) -> tuple[str, str]:
    """(start, end) para atualizacao rotineira: ultimos `n_dias` dias ate hoje."""
    hoje = pd.Timestamp.today().normalize()
    return (hoje - pd.Timedelta(days=n_dias)).strftime("%Y-%m-%d"), hoje.strftime("%Y-%m-%d")
