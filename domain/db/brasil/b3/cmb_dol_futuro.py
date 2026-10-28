"""
Curva futura do dolar (USD/BRL a termo) em prazos fixos -> macro_brasil.cmb_dol_futuro.

Fonte: o TaxaSwap.txt da B3 (`connectors/b3_curvas.py`, o mesmo cache de
`br_interest_rate`) mais a PTAX de venda de D-1 (`cmb_ptax`). A B3 nao publica o
preco do futuro de dolar em arquivo aberto, mas publica as duas pernas de que ele
e feito -- a curva DI x pre (cod PRE) e o cupom cambial SUJO (cod DOL), que e
definido a partir do futuro de dolar contra a PTAX do dia anterior:

    F = PTAX(D-1) x (1 + DI)^(du/252) / (1 + cupom_sujo x dc/360)

DI composto em dias uteis, cupom LINEAR em dias corridos base 360. A forma foi
conferida contra o forward que sai da paridade put-call das opcoes de dolar da
B3 (`cmb_vol_implicita`), que e uma fonte independente: em 16 vencimentos de
2010, 2015, 2020 e 2026 as duas batem em ate 0,04 R$ por US$ 1.000 (5.036,19
contra 5.036,22). O cupom capitalizado em vez de linear erra ate 189 (2020-03-18,
14 dias) e trocar o `du` publicado por dc x 252/365 erra ate 8 -- por isso o
`du` vem da grade da B3, interpolado no prazo, e nao de uma conta de calendario.

Prazo fixo pela mesma regra de `br_interest_rate`: o alvo (meses x 30,44 dias
corridos) tem de cair DENTRO das tres grades do pregao (DI, cupom sujo e limpo) -- nada extrapolado. A
taxa e interpolada linear em dias corridos, como la.

`premio` e o premio a termo anualizado contra o spot DO DIA, pelo cupom LIMPO
(cod DOC): ((1+DI)^(du/252) / (1 + cupom_limpo x dc/360))^(365/dc) - 1. Nao pode
ser F / PTAX(D-1): o cupom sujo carrega a variacao do dolar de ontem para hoje, e
no 1M isso anualizado deu +134% e -32% em maio/2006. O limpo e referenciado ao
spot do dia, entao o premio e so juro -- o carry do real.

O 1M do premio e ruidoso perto do vencimento do primeiro contrato (1o dia util
do mes): |1M - 3M| passa de 5 p.p. em 17 dos 5.158 pregoes, com +34% em
2006-06-01 e +28% em 2008-10-13. O FORWARD do 1M nao tem esse problema -- e o
que foi conferido contra a paridade --, so a anualizacao de um prazo curto.
Para ler o carry, use de 3M em diante.

Banco: macro_brasil.cmb_dol_futuro -- PRIMARY KEY (date, prazo)
"""

from __future__ import annotations

import logging
import os

import mysql.connector
import numpy as np
import pandas as pd

from connectors.b3_curvas import DIAS_POR_MES, baixar_muitos, grades
from connectors.mysql import MySQLDataRequester, insert_data_into_database

logger = logging.getLogger(__name__)

_DATABASE = "macro_brasil"
_TABLE = "cmb_dol_futuro"
_INICIO = "2006-01-02"
_DIAS_ROTINA = 10

PRAZOS = [1, 2, 3, 6, 9, 12, 18, 24, 36, 60]

# Folga larga: pega unidade errada (R$ por US$ 1.000) ou PTAX trocada, nao julga
# o mercado. Medido 2006-2026: forward de 1,55 a 7,9; premio de -1 a +21% a.a.
_F_MIN, _F_MAX = 0.5, 20.0
_PREMIO_MIN, _PREMIO_MAX = -20.0, 60.0

_DDL = """
CREATE TABLE IF NOT EXISTS cmb_dol_futuro (
    date    DATE        NOT NULL COMMENT 'Pregao da B3',
    prazo   VARCHAR(4)  NOT NULL COMMENT '1M | 2M | 3M | 6M | 9M | 12M | 18M | 24M | 36M | 60M (meses x 30,44 dias corridos)',
    dc      INT         NOT NULL COMMENT 'Prazo em dias corridos',
    du      DOUBLE      NOT NULL COMMENT 'Prazo em dias uteis, interpolado da grade publicada pela B3 naquele pregao',
    value   DOUBLE      NOT NULL COMMENT 'Dolar futuro, reais por dolar (BRL/USD)',
    premio  DOUBLE      NOT NULL COMMENT 'Premio a termo anualizado contra o spot do dia, % a.a.: ((1+DI)^(du/252) / (1 + cupom limpo x dc/360))^(365/dc) - 1 -- o carry do real',
    PRIMARY KEY (date, prazo)
) COMMENT='Curva futura do dolar em prazos fixos, DERIVADA das duas pernas que a B3 publica no TaxaSwap.txt: F = PTAX(D-1) x (1+DI)^(du/252) / (1 + cupom sujo x dc/360). Confere com o forward da paridade put-call das opcoes de dolar da B3 em ate 0,04 R$ por US$ 1.000. Nada extrapolado: o prazo so existe se cair dentro das grades de DI e dos dois cupons do pregao. Ver domain/db/brasil/b3/cmb_dol_futuro.py.'
"""


def _conectar():
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ.get("MYSQL_PASSWORD", ""),
        database=_DATABASE,
    )


def _garantir_tabela() -> None:
    cnx = _conectar()
    try:
        cur = cnx.cursor()
        cur.execute(_DDL)
        cnx.commit()
    finally:
        cnx.close()


def _ptax() -> pd.Series:
    req = MySQLDataRequester(_DATABASE, "cmb_ptax")
    req.connect()
    try:
        P = req.request_data()
    finally:
        req.close_connection()
    P = P[P["name"] == "ptax_venda"]
    return pd.Series(P["value"].astype(float).values,
                     index=pd.to_datetime(P["date"])).sort_index()


def no_pregao(D: pd.DataFrame, ptax_d1: float, data) -> list[tuple]:
    """Linhas (date, prazo, dc, du, value, premio) de um pregao."""
    pre = D[D.cod == "PRE"].sort_values("dc")
    dol = D[D.cod == "DOL"].sort_values("dc")
    doc = D[D.cod == "DOC"].sort_values("dc")
    if len(pre) < 2 or len(dol) < 2 or len(doc) < 2:
        return []
    lo = max(pre.dc.min(), dol.dc.min(), doc.dc.min())
    hi = min(pre.dc.max(), dol.dc.max(), doc.dc.max())
    out = []
    for m in PRAZOS:
        dc = round(m * DIAS_POR_MES)
        if dc < lo or dc > hi:
            continue
        du = float(np.interp(dc, dol.dc, dol.du))
        di = float(np.interp(dc, pre.dc, pre.taxa)) / 100
        cs = float(np.interp(dc, dol.dc, dol.taxa)) / 100
        cl = float(np.interp(dc, doc.dc, doc.taxa)) / 100
        f = ptax_d1 * (1 + di) ** (du / 252) / (1 + cs * dc / 360)
        premio = 100 * (((1 + di) ** (du / 252) / (1 + cl * dc / 360)) ** (365 / dc) - 1)
        out.append((pd.Timestamp(data).date(), f"{m}M", int(dc), round(du, 4),
                    round(f, 6), round(premio, 6)))
    return out


def coletar(full: bool = False, dias: int = _DIAS_ROTINA) -> pd.DataFrame:
    fim = pd.Timestamp.today().normalize()
    datas = list(pd.bdate_range(_INICIO, fim) if full else pd.bdate_range(end=fim, periods=dias))
    baixar_muitos(datas)
    ptax = _ptax()
    linhas, sem_ptax = [], []
    for d in datas:
        D = grades(d)
        if D is None:
            continue
        anterior = ptax[ptax.index < d]
        # A PTAX de D-1 tem de ser de fato a do pregao anterior: mais de 5 dias
        # corridos para tras e a serie de PTAX que nao foi atualizada, nao feriado.
        if anterior.empty or (d - anterior.index[-1]).days > 5:
            sem_ptax.append(d.date())
            continue
        linhas.extend(no_pregao(D, float(anterior.iloc[-1]), d))
    if sem_ptax:
        logger.warning("cmb_dol_futuro: %d pregoes sem PTAX de D-1 em cmb_ptax: %s",
                       len(sem_ptax), sem_ptax[:5])
    df = pd.DataFrame(linhas, columns=["date", "prazo", "dc", "du", "value", "premio"])
    fora = df[(df.value < _F_MIN) | (df.value > _F_MAX)
              | (df.premio < _PREMIO_MIN) | (df.premio > _PREMIO_MAX)]
    if len(fora):
        raise ValueError(f"cmb_dol_futuro: {len(fora)} linhas fora das guardas:\n"
                         f"{fora.head().to_string()}")
    return df


def run(full: bool = False, dias: int = _DIAS_ROTINA) -> None:
    """Atualiza macro_brasil.cmb_dol_futuro.

    Args:
        full: True recarrega de 2006-01-02, do cache de br_interest_rate (minutos).
        dias: dias uteis para tras no passe de rotina.
    """
    _garantir_tabela()
    df = coletar(full=full, dias=dias)
    if df.empty:
        logger.warning("cmb_dol_futuro: nada a inserir")
        return
    logger.info("cmb_dol_futuro: %d linhas, %s -> %s", len(df), df.date.min(), df.date.max())
    insert_data_into_database(_DATABASE, _TABLE, df)
