"""
O calendario OFICIAL das reunioes do Copom -> macro_brasil.pm_copom_calendario.

Fonte: a agenda publica do BCB, feed ICS "Reunioes do Copom"
(`connectors/bcb_agenda.py`). E a mesma fonte das datas de 2026 do
`domain/release_calendar/calendar_2026.yaml`, com uma diferenca que e a razao desta
tabela existir: aquele arquivo e o calendario DE UM ANO e nao recebe data de 2027
(`update_calendar.refresh` recusa, de proposito), enquanto o Copom publica o calendario
do ano seguinte com meses de antecedencia -- em 2026-09-25 o feed ja trazia as oito
reunioes de 2027. Quem precisa das reunioes FUTURAS (a leitura da curva DI e da
pesquisa Focus reuniao a reuniao, em `analytics/brasil/monetary_policy/`) le daqui.

As datas de 2027 que este feed publica sao exatamente as que a Bloomberg usa na tela de
CDI implicito (conferido em 2026-09-25: 27/01, 17/03, 28/04, 16/06, 04/08, 22/09, 27/10 e
08/12).

## O que a tabela guarda

Uma linha por reuniao, pelo DIA DA DECISAO (o dia 2 -- o feed emite os dois dias da
reuniao como eventos separados, e a decisao sai no fim do segundo). Sem numero da
reuniao (a agenda nao publica) e sem decisao (essa mora em `pm_copom_reuniao`, que so
tem reuniao ja realizada). O feed cobre de 2020-02 ao fim do calendario publicado.

Uma reuniao REMARCADA muda de data, e a chave e a data: a linha velha ficaria para tras.
Por isso cada carga apaga, dentro da janela que o feed cobre, as datas que ele deixou de
publicar -- e so depois de conferir que o feed veio inteiro, senao uma resposta vazia
apagaria o calendario.

Banco: macro_brasil.pm_copom_calendario -- PRIMARY KEY (date)

DDL:
  CREATE TABLE macro_brasil.pm_copom_calendario (
      date       DATE NOT NULL COMMENT 'Dia da decisao: o dia 2 da reuniao, como a agenda do BCB publica',
      date_start DATE NULL     COMMENT 'Dia 1 da reuniao; nulo se a agenda publicar um dia so',
      PRIMARY KEY (date)
  ) COMMENT='Calendario oficial das reunioes do Copom, da agenda publica do BCB (feed ICS Reunioes do Copom): as ja realizadas desde 2020 e as futuras que o BC ja marcou. Sem numero da reuniao e sem decisao -- a decisao esta em pm_copom_reuniao.';
"""

from __future__ import annotations

import datetime as dt
import logging

import pandas as pd

from connectors.bcb_agenda import BCBAgenda
from connectors.mysql import MySQLDataRequester, insert_data_into_database

logger = logging.getLogger(__name__)

_DATABASE = "macro_brasil"
_TABLE = "pm_copom_calendario"
_LISTA = "Reuniões do Copom"
# Menos que isto e resposta incompleta, nao calendario: o feed trazia 64 reunioes
# (2020-02 a 2027-12) em 2026-09-25. Abaixo do piso nada e gravado nem apagado.
_PISO_REUNIOES = 40


def _pares(datas: list[dt.date]) -> list[tuple[dt.date | None, dt.date]]:
    """Dias consecutivos viram (dia 1, dia 2); dia isolado vira (None, dia).

    Mesma regra de `domain/release_calendar/update_calendar._pair_days`, que le o
    mesmo feed para o calendario anual.
    """
    out, i = [], 0
    while i < len(datas):
        if i + 1 < len(datas) and datas[i + 1] - datas[i] == dt.timedelta(days=1):
            out.append((datas[i], datas[i + 1]))
            i += 2
        else:
            out.append((None, datas[i]))
            i += 1
    return out


def problemas(df: pd.DataFrame) -> list[str]:
    """O que impede a carga. Dia da semana fora de quarta so avisa: toda reuniao
    ordinaria desde 2006 decidiu numa quarta, mas uma extraordinaria pode nao decidir."""
    p = []
    if len(df) < _PISO_REUNIOES:
        p.append(f"so {len(df)} reunioes no feed (piso {_PISO_REUNIOES})")
    if df["date"].duplicated().any():
        p.append("data de decisao repetida")
    return p


def coletar(agenda: BCBAgenda | None = None) -> pd.DataFrame:
    """As reunioes do feed: colunas `date` (decisao) e `date_start`."""
    agenda = agenda or BCBAgenda()
    datas = sorted({e["date"] for e in agenda.eventos(_LISTA)})
    df = pd.DataFrame([{"date": d2, "date_start": d1} for d1, d2 in _pares(datas)],
                      columns=["date", "date_start"])
    fora = [d for d in df["date"] if d.weekday() != 2]
    if fora:
        logger.warning("pm_copom_calendario: decisao fora de quarta-feira em %s", fora)
    return df


def _executar(sql: str, args: tuple = ()) -> int:
    req = MySQLDataRequester(_DATABASE, _TABLE)
    req.connect()
    try:
        cur = req.connection.cursor()
        cur.execute(sql, args)
        req.connection.commit()
        return cur.rowcount
    finally:
        req.close_connection()


def _datas_no_banco(lo: dt.date, hi: dt.date) -> set[dt.date]:
    req = MySQLDataRequester(_DATABASE, _TABLE)
    req.connect()
    try:
        cur = req.connection.cursor()
        cur.execute(f"SELECT date FROM {_TABLE} WHERE date BETWEEN %s AND %s", (lo, hi))
        return {r[0] for r in cur.fetchall()}
    finally:
        req.close_connection()


def run() -> None:
    """Atualiza macro_brasil.pm_copom_calendario a partir da agenda do BCB."""
    df = coletar()
    probs = problemas(df)
    if probs:
        raise RuntimeError("pm_copom_calendario: carga recusada -- " + "; ".join(probs))
    lo, hi = df["date"].min(), df["date"].max()
    logger.info("pm_copom_calendario: %d reunioes, %s -> %s", len(df), lo, hi)
    insert_data_into_database(_DATABASE, _TABLE, df)
    # insert_data_into_database imprime o erro e retorna normalmente (ver
    # domain/db/CLAUDE.md, `_gravar.py`); conferir no banco e o que impede a carga de
    # mentir.
    no_banco = _datas_no_banco(lo, hi)
    faltam = set(df["date"]) - no_banco
    if faltam:
        raise RuntimeError(f"pm_copom_calendario: {len(faltam)} reunioes enviadas e ausentes "
                           f"no banco, a primeira {min(faltam)}")
    # Remarcacao: a data que o feed deixou de publicar dentro da janela dele sai.
    velhas = sorted(no_banco - set(df["date"]))
    for d in velhas:
        _executar(f"DELETE FROM {_TABLE} WHERE date = %s", (d,))
    if velhas:
        logger.warning("pm_copom_calendario: %d data(s) que o feed nao publica mais, removidas: %s",
                       len(velhas), velhas)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()
