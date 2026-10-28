"""
Leiloes de titulos da DPMFi (oferta publica do Tesouro) -> macro_brasil.fisc_leiloes.

Fonte: planilha anual de resultados do Tesouro (`connectors/tesouro_leiloes.py`),
2000 em diante, atualizada no dia do leilao. Uma linha por leilao x titulo x
vencimento x volta -- exatamente o grao da fonte, nada agregado.

## Para que serve

As duas perguntas de funcionamento do mercado de titulos que nenhuma outra
tabela do banco responde:

- **Quanto o Tesouro colocou, e a que custo.** `aceita` contra `oferta` e a
  fracao colocada; `taxa_corte` contra `taxa_media` e a cauda do leilao; a taxa
  de corte contra a curva do dia anterior (`br_interest_rate`) e a concessao.
  A demanda propriamente dita -- o volume de propostas -- **nao e publicada**:
  o que existe e a oferta e o aceito.
- **Quando o Tesouro interveio.** `tipo` separa o leilao tradicional (`venda`)
  das recompras (`compra`), das trocas e dos leiloes extraordinarios
  (`extra_compra`, `extra_venda`), que sao a intervencao em dia de estresse.
  Na serie: 2015, 2018 (greve dos caminhoneiros), 2020 (pandemia), 2024 e 2026
  (16-18/03 e 26-27/10, depois do 2o turno).

## Tres decisoes de carga

- **Taxa em % a.a.** A planilha publica em decimal (0,1358); gravamos 13,58,
  a unidade de `br_interest_rate`. Na LFT a taxa e o agio/desagio sobre a
  Selic, e 0 e valor real (titulo vendido ao par, 348 casos).
- **Taxa 0 fora da LFT vira NULL.** Seis linhas de 2001-2010 (LTN e NTN-D)
  saem com taxa 0 e quantidade aceita, que e campo nao preenchido, nao juro zero.
  A 2a volta sem nada vendido, ao contrario, repete a taxa da 1a: isso e o que
  a fonte publica (a 2a volta e a preco da 1a) e fica como esta.
- **2009-05-12 vem duplicado na fonte**: seis NTN-B listadas duas vezes, iguais
  em quantidade e com centavos de diferenca no financeiro. Fica a primeira.

Banco: macro_brasil.fisc_leiloes --
PRIMARY KEY (date, titulo, tipo, volta, liquidacao, vencimento)
"""

from __future__ import annotations

import logging
import os

import mysql.connector
import pandas as pd

from connectors import tesouro_leiloes
from connectors.mysql import insert_data_into_database

logger = logging.getLogger(__name__)

_DATABASE = "macro_brasil"
_TABLE = "fisc_leiloes"

_TIPOS = {"Venda": "venda", "Compra": "compra", "Troca": "troca",
          "Extra Compra": "extra_compra", "Extra Venda": "extra_venda"}

# Taxa em % a.a., depois da conversao. Medido em 2000-2026: LFT -0,09 a 2,05;
# LTN ate 28,86 (2002-2003); NTN-B a partir de 0,75. Folga larga de proposito --
# o guarda existe para pegar coluna trocada ou unidade mudada (13,58 vs 0,1358
# vs 1358), nao para julgar o mercado.
_TAXA_MIN, _TAXA_MAX = -2.0, 40.0

_DDL = """
CREATE TABLE IF NOT EXISTS fisc_leiloes (
    date             DATE        NOT NULL COMMENT 'Data do leilao',
    titulo           VARCHAR(8)  NOT NULL COMMENT 'LTN | NTN-F | NTN-B | LFT | NTN-C | NTN-D',
    tipo             VARCHAR(16) NOT NULL COMMENT 'venda (oferta publica tradicional) | compra (recompra) | troca | extra_venda | extra_compra (leiloes extraordinarios, a intervencao do Tesouro em dia de estresse: 2015, 2018, 2020, 2024, 2026)',
    volta            TINYINT     NOT NULL COMMENT '1 ou 2. A 2a volta e vendida a taxa da 1a, e por isso repete a taxa mesmo quando nada foi aceito',
    liquidacao       DATE        NOT NULL COMMENT 'Data de liquidacao',
    vencimento       DATE        NOT NULL COMMENT 'Vencimento do titulo',
    oferta           BIGINT      NULL     COMMENT 'Quantidade de titulos ofertada (em compra: a quantidade que o Tesouro se dispos a recomprar). Nula em 243 linhas de 2003-2007, sem oferta publicada',
    aceita           BIGINT      NOT NULL COMMENT 'Quantidade aceita (vendida em venda, recomprada em compra). Fracao colocada = aceita / oferta. A quantidade DEMANDADA nao e publicada',
    taxa_media       DOUBLE      NULL     COMMENT 'Taxa media aceita, % a.a. (na LFT, agio/desagio sobre a Selic, e 0 e valor real). Nula onde a fonte deixou 0 fora da LFT',
    taxa_corte       DOUBLE      NULL     COMMENT 'Taxa de corte (a pior aceita para o Tesouro), % a.a. Cauda = taxa_corte - taxa_media',
    financeiro       DOUBLE      NULL     COMMENT 'Financeiro aceito, R$',
    aceita_bacen     BIGINT      NULL     COMMENT 'Quantidade vendida ao Banco Central fora do leilao competitivo. Nula na maior parte de 2000-2002',
    financeiro_bacen DOUBLE      NULL     COMMENT 'Financeiro vendido ao Banco Central, R$',
    PRIMARY KEY (date, titulo, tipo, volta, liquidacao, vencimento),
    KEY idx_tipo_date (tipo, date)
) COMMENT='Resultado dos leiloes de titulos da DPMFi do Tesouro Nacional, 2000 em diante, uma linha por leilao x titulo x vencimento x volta. Fonte: planilhas anuais historico-leiloes-{ano}.xlsx (sisweb.tesouro.gov.br), atualizadas no dia do leilao. Taxas convertidas de decimal para % a.a.'
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


def transformar(bruto: pd.DataFrame) -> pd.DataFrame:
    """Da planilha crua para as colunas da tabela. Separado para o teste."""
    df = bruto.copy()
    desconhecidos = set(df["tipo"]) - set(_TIPOS)
    if desconhecidos:
        raise ValueError(f"fisc_leiloes: tipo de leilao novo na fonte: {desconhecidos}")
    df["tipo"] = df["tipo"].map(_TIPOS)
    df["volta"] = df["volta"].astype(str).str.extract(r"^(\d)")[0].astype(int)

    for c in ("taxa_media", "taxa_corte"):
        df[c] = (df[c] * 100).round(6)     # sem o round, 0,0772 vira 7,720000000000001
        df.loc[(df[c] == 0) & (df["titulo"] != "LFT"), c] = None

    fora = df[(df.taxa_media < _TAXA_MIN) | (df.taxa_media > _TAXA_MAX)
              | (df.taxa_corte < _TAXA_MIN) | (df.taxa_corte > _TAXA_MAX)]
    if len(fora):
        raise ValueError(f"fisc_leiloes: {len(fora)} taxas fora de [{_TAXA_MIN}, "
                         f"{_TAXA_MAX}] % a.a.:\n{fora.head().to_string()}")

    chave = ["data", "titulo", "tipo", "volta", "liquidacao", "vencimento"]
    dup = df.duplicated(chave)
    if dup.any():
        logger.info("fisc_leiloes: %d linhas repetidas na fonte descartadas (%s)",
                    int(dup.sum()), sorted({d.date() for d in df.loc[dup, "data"]}))
        df = df[~dup]

    df = df.rename(columns={"data": "date"})
    for c in ("date", "liquidacao", "vencimento"):
        df[c] = df[c].dt.date
    for c in ("oferta", "aceita", "aceita_bacen"):
        df[c] = df[c].astype("Int64")
    return df[["date", "titulo", "tipo", "volta", "liquidacao", "vencimento", "oferta",
               "aceita", "taxa_media", "taxa_corte", "financeiro", "aceita_bacen",
               "financeiro_bacen"]].reset_index(drop=True)


def run(full: bool = False) -> None:
    """Atualiza macro_brasil.fisc_leiloes.

    Rotina: o ano corrente e o anterior (duas planilhas de ~60 KB; o anterior
    cobre a virada do ano). `full=True`: de 2000 em diante, ~20 mil linhas.
    """
    _garantir_tabela()
    ano = pd.Timestamp.today().year
    anos = range(tesouro_leiloes.PRIMEIRO_ANO, ano + 1) if full else range(ano - 1, ano + 1)
    df = transformar(tesouro_leiloes.get_anos(anos))
    logger.info("fisc_leiloes: %d linhas, %s -> %s; por tipo: %s", len(df),
                df["date"].min(), df["date"].max(), df["tipo"].value_counts().to_dict())
    insert_data_into_database(_DATABASE, _TABLE, df)
