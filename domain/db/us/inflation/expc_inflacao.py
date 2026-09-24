"""
ETL da estrutura a termo de inflacao ESPERADA nos EUA -> macro_us.expc_inflacao.

Fonte: FRED, serie `EXPINF{n}YR` do **Federal Reserve Bank of Cleveland** (modelo
Haubrich-Pennacchi-Ritchken), 14 vertices de 1 a 30 anos, mensal desde 1982-01.
E a contraparte americana do que a Focus e do lado brasileiro: expectativa de
inflacao por horizonte, nao indice de preco -- dai o prefixo `expc_` e nao
`inflc_`, que neste schema guarda CPI e PCE.

## Por que esta tabela existe

O relatorio de politica monetaria pede "US - Juros Real 02Y/10Y - Ex ante" na
aba Condicoes, e o juro real ex-ante e nominal menos inflacao ESPERADA. O que ja
havia no banco (`macro_us.us_interest_rate`) e so nominal: `US_TREASURY`, os 11
vertices constant maturity, mais a meta do Fed.

**O Treasury nao publica TIPS de 2 anos** -- medido, nao lembrado: `DFII2` nao
existe no FRED ("The series does not exist"), e a curva de TIPS comeca em
`DFII5`. Entao o vertice de 2 anos nao tem taxa real negociada em mercado, e a
unica forma de te-lo e deflacionar o nominal por uma expectativa.

## E por que os DOIS vertices usam este metodo, e nao so o de 2 anos

O de 10 anos poderia sair do `DFII10`, que existe e e diario. Nao sai, e a razao
foi medida antes de decidir: nas 285 medias mensais de 2003-01 a 2026-09,
`DGS10 - EXPINF10YR` contra `DFII10` da erro medio +0,106 p.p., |erro| medio
0,258 p.p. e **maximo 1,369 p.p.** (nov/2008, o colapso de liquidez dos TIPS).
Os NIVEIS correlacionam 0,944, mas a **variacao mensal so 0,699** -- e a aba
colore pela variacao. Duas linhas vizinhas com metodos diferentes reagiriam
diferente a mesma noticia por razao metodologica, nao economica. Um metodo so
nas duas, e o custo dessa escolha dito no cartao de definicao da linha.

## Duas propriedades que quem consome precisa saber

**E MENSAL**, carimbada no dia 1 do mes de referencia (o FRED publica assim).
Quem cruza com serie diaria tem de decidir o alinhamento; o consumidor desta
casa (`analytics/brasil/monetary_policy/condicoes_copom.py`) desloca em 1 mes,
conservador, para nunca ler um valor antes de ele existir.

**E modelo, nao pesquisa.** O Cleveland combina TIPS, swaps de inflacao e
survey; o numero e uma estimativa deles, nao uma mediana de respostas como a
Focus. Revisa o historico quando o modelo e reestimado -- por isso a carga de
rotina reescreve uma janela, em vez de so acrescentar o mes novo.

Banco: macro_us.expc_inflacao -- PRIMARY KEY (date, tenor)
DDL:
  CREATE TABLE macro_us.expc_inflacao (
      date        DATE          NOT NULL,
      tenor       VARCHAR(10)   NOT NULL,
      tenor_years DECIMAL(8,6)  NOT NULL,
      value       DECIMAL(12,8),
      PRIMARY KEY (date, tenor)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

from __future__ import annotations

import logging
import os

import mysql.connector
import pandas as pd

from connectors.fred import _fred
from connectors.mysql import insert_data_into_database

logger = logging.getLogger(__name__)

_DATABASE = "macro_us"
_TABLE = "expc_inflacao"

# Os 14 vertices que o Cleveland publica. O rotulo segue a convencao de
# `us_interest_rate` -- anos, com "Y" --, e `tenor_years` e o que se usa para
# cruzar com qualquer outra curva; o texto e rotulo, nao chave de juncao.
_TENORES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30]

# Faixa de sanidade. A expectativa de 1 ano chegou a ~5% no inicio dos anos 80 e
# a **negativa** no fim de 2008 (-0,6% medido) -- por isso o piso e negativo, ao
# contrario da curva nominal do Treasury, que nunca fechou abaixo de zero.
_PISO, _TETO = -5.0, 15.0

# Meses reescritos no passe de rotina. Mais que o mes novo de proposito: o
# modelo do Cleveland revisa o historico recente quando e reestimado, e o upsert
# torna reescrever mes ja gravado inofensivo.
_MESES_ROTINA = 6

_DDL = """
CREATE TABLE IF NOT EXISTS expc_inflacao (
    date        DATE          NOT NULL,
    tenor       VARCHAR(10)   NOT NULL,
    tenor_years DECIMAL(8,6)  NOT NULL,
    value       DECIMAL(12,8),
    PRIMARY KEY (date, tenor)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
"""


def _garantir_tabela() -> None:
    """Cria a tabela se ela ainda nao existe.

    O resto do `domain/db/` documenta o DDL no docstring e cria a tabela a mao.
    Aqui ele tambem roda, e a diferenca e deliberada: e IF NOT EXISTS, entao e
    idempotente, e evita que uma maquina nova precise de um passo manual que
    nada no repositorio executa.
    """
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
        cur.close()
    finally:
        cnx.close()


def coletar(full: bool = False, meses: int = _MESES_ROTINA) -> pd.DataFrame:
    """Monta o DataFrame pronto para a tabela.

    Separado de `run()` para o teste poder exercitar a coleta sem tocar no banco
    -- mesma divisao de `us_interest_rate.py`.
    """
    fred = _fred()
    corte = None
    if not full:
        corte = (pd.Timestamp.today().normalize().replace(day=1)
                 - pd.DateOffset(months=meses))

    linhas = []
    for n in _TENORES:
        code = "EXPINF%dYR" % n
        s = fred.get_series(code).dropna()
        s.index = pd.to_datetime(s.index)
        s = s.astype(float)
        if corte is not None:
            s = s[s.index >= corte]
        rotulo = "%dY" % n
        for data, valor in s.items():
            linhas.append((data.date(), rotulo, round(float(n), 6),
                           round(float(valor), 8)))
        logger.info("  %-6s %-11s %4d obs", rotulo, code, len(s))

    df = pd.DataFrame(linhas,
                      columns=["date", "tenor", "tenor_years", "value"])
    if df.empty:
        return df

    fora = df[(df.value < _PISO) | (df.value > _TETO)]
    if len(fora):
        raise ValueError(
            "%d valores fora de [%s, %s]:\n%s"
            % (len(fora), _PISO, _TETO, fora.head(10).to_string(index=False)))
    if df.duplicated(["date", "tenor"]).any():
        raise ValueError("chave (date, tenor) duplicada na coleta")

    # A curva tem de ser lida como curva: se um mes vier com um vertice so, o
    # consumidor que interpola entre 2Y e 10Y silenciosamente usa o mesmo ponto
    # duas vezes. Levantar e melhor que devolver curva de um ponto.
    por_mes = df.groupby("date")["tenor"].nunique()
    incompletos = por_mes[por_mes != len(_TENORES)]
    if len(incompletos):
        raise ValueError(
            "%d mes(es) com curva incompleta (esperado %d vertices): %s"
            % (len(incompletos), len(_TENORES),
               ", ".join(str(d) for d in incompletos.index[:5])))
    return df


def run(full: bool = False, meses: int = _MESES_ROTINA) -> None:
    """Atualiza macro_us.expc_inflacao.

    Args:
        full: True carrega 1982-01 -> hoje nos 14 vertices (~7,5 mil linhas).
        meses: janela retroativa do passe de rotina. 6 cobre a revisao que o
               modelo do Cleveland aplica ao historico recente.
    """
    _garantir_tabela()
    df = coletar(full=full, meses=meses)
    if df.empty:
        logger.warning("expc_inflacao: nada a inserir")
        return
    logger.info("expc_inflacao: %d linhas, %d vertices, %s -> %s",
                len(df), df["tenor"].nunique(), df["date"].min(), df["date"].max())
    insert_data_into_database(_DATABASE, _TABLE, df)
