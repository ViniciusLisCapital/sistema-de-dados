"""
DI futuro e cupom de IPCA na B3, por pregao e codigo -> macro_brasil.br_juros_contratos.

Fonte: boletim de precos BVBG.086 do arquivo de pregao (`connectors/b3_precos.py`),
diario desde 2018-01-02. A logica comum -- download unico, posicao em aberto
gravada no fechamento, codigos fora do padrao -- esta em `_contratos_b3.py`.

Os precos do dia (abertura, minimo, maximo, medio, ultimo) estao em TAXA, % a.a. -- o DI e o DAP negociam em taxa.

Banco: macro_brasil.br_juros_contratos -- PRIMARY KEY (date, ticker)
"""

from __future__ import annotations

import logging
import os

import mysql.connector

from connectors.mysql import insert_data_into_database
from domain.db.brasil.b3 import _contratos_b3 as nucleo

logger = logging.getLogger(__name__)

_DATABASE = "macro_brasil"
_TABLE = "br_juros_contratos"
_DIAS_ROTINA = 10
ATIVOS = ('DI1', 'DAP')

_DDL = """
CREATE TABLE IF NOT EXISTS br_juros_contratos (
    date            DATE         NOT NULL COMMENT 'Pregao da B3',
    ticker          VARCHAR(16)  NOT NULL COMMENT 'Codigo de negociacao (DOLX26, DI1F27...)',
    ativo           VARCHAR(4)   NOT NULL COMMENT 'DI1 (DI de 1 dia futuro) | DAP (cupom de IPCA futuro)',
    tipo            VARCHAR(12)  NOT NULL COMMENT 'futuro',
    vencimento      DATE         NULL     COMMENT 'MES de vencimento (dia 1); o dia exato segue a regra do contrato (1o dia util do mes para o DI1; dia 15 para o DAP)',
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
    ajuste          DOUBLE       NULL     COMMENT 'Preco de ajuste, PU (100.000 no vencimento)',
    taxa_ajuste     DOUBLE       NULL     COMMENT 'Taxa de ajuste, % a.a.: DI x pre (base 252) no DI1; juro real (base 252) no DAP',
    PRIMARY KEY (date, ticker)
) COMMENT='Contratos de juros da B3 por pregao e vencimento -- DI1 e DAP: negocios, contratos, volume em R$ e US$, posicao em aberto no fechamento, taxas do dia e ajuste. A taxa de ajuste do DI1 e a mesma curva de br_di_grade (conferido). Fonte: boletim de precos BVBG.086 do arquivo de pregao (PR), desde 2018-01-02. Ver domain/db/brasil/b3/br_juros_contratos.py.'
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
    """Atualiza macro_brasil.br_juros_contratos.

    Args:
        full: True recarrega de 2018-01-02 (~2.200 pregoes; num cache vazio,
              horas -- o arquivo tem ate 12 MB zipado e a B3 aceita 2 conexoes).
        dias: dias uteis para tras no passe de rotina. Tem de ser > 1: a posicao
              do ultimo pregao so sai com o arquivo do seguinte.
    """
    _garantir_tabela()
    df = coletar(full=full, dias=dias)
    if df.empty:
        logger.warning("br_juros_contratos: nada a inserir")
        return
    logger.info("br_juros_contratos: %d linhas, %s -> %s", len(df), df.date.min(), df.date.max())
    insert_data_into_database(_DATABASE, _TABLE, df)
