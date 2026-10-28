"""
Dolar futuro, minidolar, cupom cambial, FRA de cupom, rolagem e casado na B3, por pregao e codigo -> macro_brasil.cmb_contratos_b3.

Fonte: boletim de precos BVBG.086 do arquivo de pregao (`connectors/b3_precos.py`),
diario desde 2018-01-02. A logica comum -- download unico, posicao em aberto
gravada no fechamento, codigos fora do padrao -- esta em `_contratos_b3.py`.

Unidade dos precos: DOL/WDO em R$ por US$ 1.000; DDI e FRC em taxa (% a.a., linear 360); DR1 e FRP em pontos.

Banco: macro_brasil.cmb_contratos_b3 -- PRIMARY KEY (date, ticker)
"""

from __future__ import annotations

import logging
import os

import mysql.connector

from connectors.mysql import insert_data_into_database
from domain.db.brasil.b3 import _contratos_b3 as nucleo

logger = logging.getLogger(__name__)

_DATABASE = "macro_brasil"
_TABLE = "cmb_contratos_b3"
_DIAS_ROTINA = 10
ATIVOS = ('DOL', 'WDO', 'DDI', 'FRC', 'DR1', 'FRP')

_DDL = """
CREATE TABLE IF NOT EXISTS cmb_contratos_b3 (
    date            DATE         NOT NULL COMMENT 'Pregao da B3',
    ticker          VARCHAR(16)  NOT NULL COMMENT 'Codigo de negociacao (DOLX26, DI1F27...)',
    ativo           VARCHAR(4)   NOT NULL COMMENT 'DOL (dolar cheio, US$ 50 mil) | WDO (minidolar, US$ 10 mil) | DDI (cupom cambial) | FRC (FRA de cupom) | DR1 (rolagem de dolar) | FRP (casado: forward points, a vista contra futuro)',
    tipo            VARCHAR(12)  NOT NULL COMMENT 'futuro | rolagem (DR1, o codigo traz as duas pernas e vencimento e a curta) | estruturada (FRP)',
    vencimento      DATE         NULL     COMMENT 'MES de vencimento (dia 1); o dia exato segue a regra do contrato (1o dia util do mes para DOL/WDO/DDI); NULL no FRP',
    negocios        INT          NULL     COMMENT 'Numero de negocios no dia',
    contratos       BIGINT       NULL     COMMENT 'Contratos negociados no dia (pregao regular + fora dele)',
    vol_brl         DOUBLE       NULL     COMMENT 'Volume financeiro do dia, R$',
    vol_usd         DOUBLE       NULL     COMMENT 'Volume financeiro do dia, US$ (conversao da B3)',
    posicao_aberto  BIGINT       NULL     COMMENT 'Contratos em aberto no FECHAMENTO do dia (lido da abertura do pregao seguinte; NULL enquanto ele nao sai); NULL para FRC/DR1/FRP, que nao carregam posicao propria (a do FRA cai no DDI)',
    abertura        DOUBLE       NULL     COMMENT 'Primeiro preco do dia, na unidade de cotacao do contrato',
    minimo          DOUBLE       NULL     COMMENT 'Preco minimo do dia',
    maximo          DOUBLE       NULL     COMMENT 'Preco maximo do dia',
    medio           DOUBLE       NULL     COMMENT 'Preco medio do dia',
    ultimo          DOUBLE       NULL     COMMENT 'Ultimo preco do dia',
    ajuste          DOUBLE       NULL     COMMENT 'Preco de ajuste: R$ por US$ 1.000 no DOL/WDO; PU no DDI',
    taxa_ajuste     DOUBLE       NULL     COMMENT 'Taxa de ajuste, % a.a.: cupom cambial (linear 360) no DDI e FRC',
    PRIMARY KEY (date, ticker)
) COMMENT='Contratos de cambio da B3 por pregao e codigo -- dolar cheio e mini, cupom cambial, FRA de cupom, rolagem e casado: negocios, contratos, volume em R$ e US$, posicao em aberto no fechamento e precos. Fonte: boletim de precos BVBG.086 do arquivo de pregao (PR), desde 2018-01-02. Ver domain/db/brasil/b3/cmb_contratos_b3.py.'
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
    """Atualiza macro_brasil.cmb_contratos_b3.

    Args:
        full: True recarrega de 2018-01-02 (~2.200 pregoes; num cache vazio,
              horas -- o arquivo tem ate 12 MB zipado e a B3 aceita 2 conexoes).
        dias: dias uteis para tras no passe de rotina. Tem de ser > 1: a posicao
              do ultimo pregao so sai com o arquivo do seguinte.
    """
    _garantir_tabela()
    df = coletar(full=full, dias=dias)
    if df.empty:
        logger.warning("cmb_contratos_b3: nada a inserir")
        return
    logger.info("cmb_contratos_b3: %d linhas, %s -> %s", len(df), df.date.min(), df.date.max())
    insert_data_into_database(_DATABASE, _TABLE, df)
