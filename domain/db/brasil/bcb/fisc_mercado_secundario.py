"""
Negociacao de titulos federais no mercado secundario -> macro_brasil.fisc_mercado_secundario.

Fonte: BCB/Demab, arquivos mensais NegT/NegE (`connectors/bcb_negociacoes.py`),
operacoes DEFINITIVAS registradas no Selic, uma linha por dia x titulo
(codigo Selic + vencimento).
2003-01 ate D-1.

## Para que serve

E o lado do mercado que os leiloes (`fisc_leiloes`) nao mostram: quanto cada
titulo girou depois de emitido, em quantas operacoes, e a dispersao de preco
dentro do dia. Liquidez e funcionamento do mercado, nao nivel de taxa -- para
a taxa de referencia, `br_interest_rate` (curvas da B3, que sao a indicativa).

## Os dois universos

`universo` = `todas` (NegT) ou `extragrupo` (NegE, so operacoes entre
conglomerados diferentes). A diferenca e o giro intragrupo -- titulo que
troca de mao dentro do mesmo grupo, sem formar preco. Para liquidez de mercado
o extragrupo e a leitura mais limpa; os dois sao gravados porque a razao entre
eles e informacao propria.

## O que a fonte avisa e a tabela preserva

- Taxa (min/med/max) so existe para LTN e LFT (e LFT-B); NTN-B e NTN-F vem com
  PU e sem taxa. Na LFT a taxa e o agio/desagio sobre a Selic.
- Desde 2006-10-02 os PUs excluem operacoes com broker; contagem e quantidade
  nao.
- `valor_negociado` foi descontinuado pelo BCB e so vem preenchido ate
  2006-09-29; volume financeiro = quantidade x pu_med.
- O arquivo inclui titulos do Banco Central (NBCE, LBC) no inicio da serie --
  "titulos federais" e mais largo que DPMFi.

## Carga

Rotina: mes corrente e anterior, nos dois universos (4 arquivos). `start=`
'AAAA-MM' ou 'all' (desde 2003-01, ~570 arquivos, minutos). Upsert: o BCB
fecha o mes corrente dia a dia, e o mes anterior cobre a virada.

Banco: macro_brasil.fisc_mercado_secundario --
PRIMARY KEY (date, universo, codigo, vencimento)
"""

from __future__ import annotations

import logging
import os
import time

import mysql.connector
import pandas as pd

from connectors import bcb_negociacoes
from connectors.mysql import insert_data_into_database

logger = logging.getLogger(__name__)

_DATABASE = "macro_brasil"
_TABLE = "fisc_mercado_secundario"

_DDL = """
CREATE TABLE IF NOT EXISTS fisc_mercado_secundario (
    date              DATE         NOT NULL COMMENT 'Dia da negociacao',
    universo          VARCHAR(10)  NOT NULL COMMENT 'todas (arquivo NegT) | extragrupo (NegE: so operacoes entre conglomerados diferentes, sem o giro intragrupo)',
    codigo            VARCHAR(10)  NOT NULL COMMENT 'Codigo Selic do papel (o tipo, nao o vencimento: todas as LTN sao 100000). Com vencimento, identifica o titulo',
    vencimento        DATE         NOT NULL COMMENT 'Vencimento',
    sigla             VARCHAR(10)  NOT NULL COMMENT 'LTN | NTN-F | NTN-B | LFT | NTN-C | ... e, no inicio da serie, titulos do BCB (NBCE, LBC)',
    isin              VARCHAR(12)  NULL     COMMENT 'Codigo ISIN do titulo. Nulo quando a fonte traz 000000000000 ou vazio -- acontece no dia da 1a emissao de um vencimento novo',
    emissao           DATE         NULL     COMMENT 'Data da primeira emissao',
    num_operacoes     INT          NOT NULL COMMENT 'Numero de operacoes definitivas no dia',
    quantidade        BIGINT       NOT NULL COMMENT 'Quantidade de titulos negociados. Volume em R$ = quantidade x pu_med',
    valor_negociado   DOUBLE       NULL     COMMENT 'Valor financeiro, R$ -- campo DESCONTINUADO pelo BCB: preenchido so ate 2006-09-29. Use quantidade x pu_med',
    pu_min            DOUBLE       NULL     COMMENT 'PU minimo. Desde 2006-10-02 exclui operacoes com broker',
    pu_med            DOUBLE       NULL     COMMENT 'PU medio. Desde 2006-10-02 exclui operacoes com broker',
    pu_max            DOUBLE       NULL     COMMENT 'PU maximo. Desde 2006-10-02 exclui operacoes com broker',
    pu_lastro         DOUBLE       NULL     COMMENT 'PU de lastro',
    valor_par         DOUBLE       NULL     COMMENT 'PU par',
    taxa_min          DOUBLE       NULL     COMMENT 'Taxa minima, % a.a. So LTN e LFT (na LFT, agio/desagio sobre a Selic)',
    taxa_med          DOUBLE       NULL     COMMENT 'Taxa media, % a.a. So LTN e LFT',
    taxa_max          DOUBLE       NULL     COMMENT 'Taxa maxima, % a.a. So LTN e LFT',
    num_operacoes_corretagem BIGINT NULL    COMMENT 'Operacoes por meio de corretagem. Publicado desde 2011-01-03',
    quantidade_corretagem    BIGINT NULL    COMMENT 'Quantidade negociada por meio de corretagem. Publicado desde 2011-01-03',
    PRIMARY KEY (date, universo, codigo, vencimento),
    KEY idx_sigla_date (sigla, date)
) COMMENT='Negociacao definitiva de titulos federais no mercado secundario, registrada no Selic (BCB/Demab, arquivos NegT/NegE), uma linha por dia x universo x titulo, 2003-01 em diante. Compromissadas NAO entram.'
"""

_COLUNAS = ["date", "universo", "codigo", "vencimento", "sigla", "isin", "emissao",
            "num_operacoes", "quantidade", "valor_negociado", "pu_min", "pu_med", "pu_max",
            "pu_lastro", "valor_par", "taxa_min", "taxa_med", "taxa_max",
            "num_operacoes_corretagem", "quantidade_corretagem"]


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


def _meses(start) -> list[pd.Timestamp]:
    hoje = pd.Timestamp.today().normalize()
    if start is None:
        ini = hoje.replace(day=1) - pd.DateOffset(months=1)
    elif start == "all":
        ini = pd.Timestamp(bcb_negociacoes.PRIMEIRO_MES)
    else:
        ini = pd.Timestamp(start).replace(day=1)
    return list(pd.date_range(ini, hoje.replace(day=1), freq="MS"))


def coletar(start=None) -> pd.DataFrame:
    partes, vazios = [], []
    for mes in _meses(start):
        for u in bcb_negociacoes.UNIVERSOS:
            df = bcb_negociacoes.get_mes(mes, u)
            if df is None:
                vazios.append(f"Neg{u}{mes:%Y%m}")
                continue
            partes.append(df)
            time.sleep(0.2)
    if vazios:
        logger.info("fisc_mercado_secundario: sem arquivo no BCB: %s", vazios)
    if not partes:
        return pd.DataFrame(columns=_COLUNAS)
    df = pd.concat(partes, ignore_index=True)

    # O ISIN nao serve de chave: no dia da 1a emissao de um vencimento novo a
    # fonte traz 000000000000 ou vazio (medido: 2005-06-01, 2006-07-07, 2018-07-09).
    # Codigo Selic + vencimento identificam o titulo sem essa lacuna.
    df.loc[~df["isin"].str.fullmatch(r"BR[A-Z0-9]{10}"), "isin"] = None
    chave = ["date", "universo", "codigo", "vencimento"]
    dup = df.duplicated(chave)
    if dup.any():
        raise ValueError(f"fisc_mercado_secundario: {int(dup.sum())} linhas com a mesma "
                         f"{chave}:\n{df[dup].head().to_string()}")

    for c in ("date", "emissao", "vencimento"):
        df[c] = df[c].dt.date
    for c in ("num_operacoes", "quantidade", "num_operacoes_corretagem",
              "quantidade_corretagem"):
        df[c] = df[c].astype("Int64")
    return df[_COLUNAS]


def run(start=None) -> None:
    """Atualiza macro_brasil.fisc_mercado_secundario.

    Args:
        start: None (mes corrente e anterior), 'AAAA-MM', ou 'all' (desde 2003-01).
    """
    _garantir_tabela()
    df = coletar(start)
    if df.empty:
        logger.warning("fisc_mercado_secundario: nada a inserir")
        return
    logger.info("fisc_mercado_secundario: %d linhas, %s -> %s", len(df),
                df["date"].min(), df["date"].max())
    insert_data_into_database(_DATABASE, _TABLE, df)
