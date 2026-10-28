"""
Opcoes de dolar na B3, por pregao e serie (vencimento x call/put x strike) ->
macro_brasil.cmb_opcoes_dolar.

Fonte: boletim de precos BVBG.086 do arquivo de pregao (`connectors/b3_precos.py`),
diario desde 2018-01-02. A logica comum -- download unico, posicao em aberto
gravada no fechamento, codigos fora do padrao -- esta em `_contratos_b3.py`.

Uma linha por serie que teve negocio ou posicao em aberto naquele pregao: das
~2.100 series que a B3 lista hoje, ~500. E o que mostra em que nivel de dolar
esta a protecao (quantas calls a R$ 5,70, quantas puts a R$ 5,00).

Strike e precos em R$ por US$ 1.000, a unidade da B3 (strike 5700 = R$ 5,70).
A serie de EXERCICIO do dia do vencimento (sufixo E) fica fora: ver
`b3_precos.classificar`.

Diferente de `cmb_vol_implicita`, que vem do premio TEORICO de referencia de
toda serie autorizada (arquivo RE): aqui e o que foi NEGOCIADO.

Banco: macro_brasil.cmb_opcoes_dolar -- PRIMARY KEY (date, ticker)
"""

from __future__ import annotations

import logging
import os

import mysql.connector

from connectors.mysql import insert_data_into_database
from domain.db.brasil.b3 import _contratos_b3 as nucleo

logger = logging.getLogger(__name__)

_DATABASE = "macro_brasil"
_TABLE = "cmb_opcoes_dolar"
_DIAS_ROTINA = 10
ATIVOS = ("DOL", "WDO")

_DDL = """
CREATE TABLE IF NOT EXISTS cmb_opcoes_dolar (
    date            DATE         NOT NULL COMMENT 'Pregao da B3',
    ticker          VARCHAR(16)  NOT NULL COMMENT 'Codigo da serie (DOLZ26C005700)',
    ativo           VARCHAR(4)   NOT NULL COMMENT 'DOL (dolar cheio, US$ 50 mil) | WDO (minidolar, US$ 10 mil)',
    vencimento      DATE         NOT NULL COMMENT 'MES de vencimento (dia 1); vence no 1o dia util do mes',
    opcao           CHAR(1)      NOT NULL COMMENT 'C = call (compra) | P = put (venda)',
    strike          DOUBLE       NOT NULL COMMENT 'Preco de exercicio, R$ por US$ 1.000 (5700 = R$ 5,70)',
    negocios        INT          NULL     COMMENT 'Numero de negocios no dia',
    contratos       BIGINT       NULL     COMMENT 'Contratos negociados no dia',
    vol_brl         DOUBLE       NULL     COMMENT 'Volume financeiro do dia (premio pago), R$',
    vol_usd         DOUBLE       NULL     COMMENT 'Volume financeiro do dia, US$ (conversao da B3)',
    posicao_aberto  BIGINT       NULL     COMMENT 'Contratos em aberto no FECHAMENTO do dia (lido da abertura do pregao seguinte; NULL enquanto ele nao sai)',
    abertura        DOUBLE       NULL     COMMENT 'Primeiro premio negociado, R$ por US$ 1.000',
    minimo          DOUBLE       NULL     COMMENT 'Premio minimo do dia',
    maximo          DOUBLE       NULL     COMMENT 'Premio maximo do dia',
    medio           DOUBLE       NULL     COMMENT 'Premio medio do dia',
    ultimo          DOUBLE       NULL     COMMENT 'Ultimo premio do dia',
    PRIMARY KEY (date, ticker)
) COMMENT='Opcoes de dolar (DOL e WDO) negociadas na B3, uma linha por serie com negocio ou posicao em aberto no pregao: contratos, volume, posicao em aberto no fechamento e premios do dia. Strike e premio em R$ por US$ 1.000. Fonte: boletim de precos BVBG.086 do arquivo de pregao (PR), desde 2018-01-02. Ver domain/db/brasil/b3/cmb_opcoes_dolar.py.'
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
    return P[P["tipo"] == "opcao"][nucleo.COLUNAS_OPCAO]


def run(full: bool = False, dias: int = _DIAS_ROTINA) -> None:
    """Atualiza macro_brasil.cmb_opcoes_dolar.

    Args:
        full: True recarrega de 2018-01-02 (~2.200 pregoes, o mesmo cache das
              outras tres tabelas do boletim).
        dias: dias uteis para tras no passe de rotina (> 1, pela posicao).
    """
    _garantir_tabela()
    df = coletar(full=full, dias=dias)
    if df.empty:
        logger.warning("cmb_opcoes_dolar: nada a inserir")
        return
    logger.info("cmb_opcoes_dolar: %d linhas, %s -> %s", len(df), df.date.min(), df.date.max())
    insert_data_into_database(_DATABASE, _TABLE, df)
