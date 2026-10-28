"""
Ibovespa futuro, cheio e mini na B3, por pregao e codigo -> macro_brasil.bolsa_ibov_futuro.

Fonte: boletim de precos BVBG.086 do arquivo de pregao (`connectors/b3_precos.py`),
diario desde 2018-01-02. A logica comum -- download unico, posicao em aberto
gravada no fechamento, codigos fora do padrao -- esta em `_contratos_b3.py`.

Precos em pontos do Ibovespa.

Banco: macro_brasil.bolsa_ibov_futuro -- PRIMARY KEY (date, ticker)
"""

from __future__ import annotations

import logging
import os

import mysql.connector

from connectors.mysql import insert_data_into_database
from domain.db.brasil.b3 import _contratos_b3 as nucleo

logger = logging.getLogger(__name__)

_DATABASE = "macro_brasil"
_TABLE = "bolsa_ibov_futuro"
_DIAS_ROTINA = 10
ATIVOS = ('IND', 'WIN')

_DDL = """
CREATE TABLE IF NOT EXISTS bolsa_ibov_futuro (
    date            DATE         NOT NULL COMMENT 'Pregao da B3',
    ticker          VARCHAR(16)  NOT NULL COMMENT 'Codigo de negociacao (DOLX26, DI1F27...)',
    ativo           VARCHAR(4)   NOT NULL COMMENT 'IND (Ibovespa futuro, R$ 1 por ponto) | WIN (mini, R$ 0,20 por ponto)',
    tipo            VARCHAR(12)  NOT NULL COMMENT 'futuro',
    vencimento      DATE         NULL     COMMENT 'MES de vencimento (dia 1); o dia exato segue a regra do contrato (quarta-feira mais proxima do dia 15, meses pares)',
    negocios        INT          NULL     COMMENT 'Numero de negocios no dia',
    contratos       BIGINT       NULL     COMMENT 'Contratos negociados no dia (pregao regular + fora dele)',
    vol_brl         DOUBLE       NULL     COMMENT 'Volume financeiro do dia, R$',
    vol_usd         DOUBLE       NULL     COMMENT 'Volume financeiro do dia, US$ (conversao da B3)',
    posicao_aberto  BIGINT       NULL     COMMENT 'Contratos em aberto no FECHAMENTO do dia (lido da abertura do pregao seguinte; NULL enquanto ele nao sai)',
    abertura        DOUBLE       NULL     COMMENT 'Primeiro preco do dia, na unidade de cotacao do contrato',
    minimo          DOUBLE       NULL     COMMENT 'Preco minimo do dia',
    maximo          DOUBLE       NULL     COMMENT 'Preco maximo do dia',
    medio           DOUBLE       NULL     COMMENT 'Preco medio do dia',
    ultimo          DOUBLE       NULL     COMMENT 'Ultimo preco do dia',
    ajuste          DOUBLE       NULL     COMMENT 'Preco de ajuste, pontos do indice',
    taxa_ajuste     DOUBLE       NULL     COMMENT 'Sempre NULL (o contrato nao tem taxa); a coluna existe para as tres tabelas de contrato terem o mesmo layout',
    PRIMARY KEY (date, ticker)
) COMMENT='Ibovespa futuro (IND e WIN) por pregao e vencimento: negocios, contratos, volume em R$ e US$, posicao em aberto no fechamento e precos em pontos. Unico dado de bolsa brasileira do banco. Fonte: boletim de precos BVBG.086 do arquivo de pregao (PR), desde 2018-01-02. Ver domain/db/brasil/b3/bolsa_ibov_futuro.py.'
"""


def _garantir_tabela() -> None:
    cnx = mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ.get("MYSQL_PASSWORD", ""),
        database=_DATABASE,
    )
    try:
        cur = cnx.cursor()
        cur.execute(_DDL)
        cnx.commit()
    finally:
        cnx.close()


def coletar(full: bool = False, dias: int = _DIAS_ROTINA):
    P = nucleo.painel(nucleo.datas(full, dias), ATIVOS)
    if P.empty:
        return P
    # as opcoes de dolar sao a outra tabela (cmb_opcoes_dolar)
    return P[P["tipo"] != "opcao"][nucleo.COLUNAS_CONTRATO]


def run(full: bool = False, dias: int = _DIAS_ROTINA) -> None:
    """Atualiza macro_brasil.bolsa_ibov_futuro.

    Args:
        full: True recarrega de 2018-01-02 (~2.200 pregoes; num cache vazio,
              horas -- o arquivo tem ate 12 MB zipado e a B3 aceita 2 conexoes).
        dias: dias uteis para tras no passe de rotina. Tem de ser > 1: a posicao
              do ultimo pregao so sai com o arquivo do seguinte.
    """
    _garantir_tabela()
    df = coletar(full=full, dias=dias)
    if df.empty:
        logger.warning("bolsa_ibov_futuro: nada a inserir")
        return
    logger.info("bolsa_ibov_futuro: %d linhas, %s -> %s", len(df), df.date.min(), df.date.max())
    insert_data_into_database(_DATABASE, _TABLE, df)
