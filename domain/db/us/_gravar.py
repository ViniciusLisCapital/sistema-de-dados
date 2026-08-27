"""
Escrita verificada, para os scripts de macro_us.

Existe por causa de um comportamento de `connectors.mysql.insert_data_into_database`
que morde em silencio: ela captura `mysql.connector.Error`, IMPRIME a mensagem e
retorna normalmente. Quem chama nao tem como saber que a gravacao falhou -- e se
imprimir "N linhas gravadas" depois, mente.

Foi exatamente o que aconteceu ao carregar `inflc_cpi_pesos` pela primeira vez
(2026-08): a coluna `weights_year` estava NOT NULL, o BLS nao publica ano de cesta
para 2020/2021 (cesta bienal, "2019-2020 weights"), o INSERT morreu com
`1048 Column 'weights_year' cannot be null`, e o script anunciou "3.864 linhas
gravadas" numa tabela que ficou com zero.

`gravar()` faz a mesma insercao e depois CONFERE no banco, levantando se nao houver
nenhuma linha para os valores que acabaram de ser enviados. A conferencia nao pode
ser "contou mais linhas que antes": o insert e upsert (`ON DUPLICATE KEY UPDATE`),
entao reexecutar com os mesmos dados legitimamente adiciona zero. Por isso a sonda e
por VALOR de uma coluna-chave (`sonda`), nao por contagem total.

Nao mexe na helper compartilhada de proposito -- 60 scripts de `macro_brasil`
dependem do comportamento atual dela, e trocar para levantar excecao no meio de uma
sessao mudaria o comportamento de todos de uma vez. A correcao certa e essa mesma
verificacao migrar para lá algum dia; ate entao ela vive aqui, no ramo novo.
"""

from __future__ import annotations

import pandas as pd

from connectors.mysql import MySQLDataRequester, insert_data_into_database


def _conn(database: str):
    req = MySQLDataRequester(database, "")
    req.connect()
    if req.connection is None:
        raise RuntimeError(f"sem conexao com o MySQL (schema {database})")
    return req.connection


def contar(database: str, table: str) -> int:
    conn = _conn(database)
    try:
        return int(pd.read_sql(f"SELECT COUNT(*) AS n FROM {table}", conn)["n"].iloc[0])
    finally:
        conn.close()


def ler(database: str, sql: str) -> pd.DataFrame:
    """Roda um SELECT e devolve DataFrame, fechando a conexao.

    Existe porque o ramo de `macro_us` passou a LER do banco, e nao so a escrever:
    a arvore do PCE (`inflc_pce_dim`) so pode ser montada do xlsx, entao ela e
    gravada uma vez e nas rodadas seguintes e RELIDA daqui e revalidada contra a API,
    em vez de o arquivo de 12 MB ser baixado de novo a cada mes.

    Args:
        database: schema.
        sql:      a consulta.

    Returns:
        O resultado. Nao trata erro de conexao de proposito -- quem chama decide se
        cai para outro caminho (ver `inflc_pce_dim._estrutura_gravada`).
    """
    conn = _conn(database)
    try:
        return pd.read_sql(sql, conn)
    finally:
        conn.close()


def gravar(database: str, table: str, df: pd.DataFrame, sonda: str) -> int:
    """Grava `df` em `database`.`table` e confirma no banco que os dados chegaram.

    Args:
        database: schema.
        table:    tabela destino.
        df:       linhas a gravar, colunas com os nomes das colunas da tabela.
        sonda:    nome de uma coluna-chave de `df`. Depois do insert, conta no banco
                  as linhas cujos valores dessa coluna estao entre os enviados; se
                  der zero, levanta. E o que distingue "upsert que nao mudou nada"
                  (legitimo) de "insert que falhou inteiro" (nao).

    Returns:
        Total de linhas na tabela depois da gravacao.

    Raises:
        RuntimeError: se nenhuma das linhas enviadas estiver no banco depois.
    """
    if df.empty:
        print(f"  nada a gravar em {database}.{table}")
        return contar(database, table)

    if sonda not in df.columns:
        raise ValueError(f"coluna-sonda {sonda!r} nao esta em df ({list(df.columns)})")

    antes = contar(database, table)
    insert_data_into_database(database, table, df)

    valores = pd.Series(df[sonda].dropna().unique())
    if valores.empty:
        raise ValueError(f"coluna-sonda {sonda!r} so tem nulos -- nao da para verificar")
    amostra = valores.head(200).tolist()

    conn = _conn(database)
    try:
        marcadores = ", ".join(["%s"] * len(amostra))
        achadas = int(pd.read_sql(
            f"SELECT COUNT(*) AS n FROM {table} WHERE {sonda} IN ({marcadores})",
            conn, params=amostra,
        )["n"].iloc[0])
        depois = int(pd.read_sql(f"SELECT COUNT(*) AS n FROM {table}", conn)["n"].iloc[0])
    finally:
        conn.close()

    if achadas == 0:
        raise RuntimeError(
            f"{database}.{table}: o INSERT nao gravou nada -- zero linhas com "
            f"{sonda} entre os {len(amostra)} valores enviados. A mensagem de erro do "
            "MySQL aparece acima ('MySQL query error: ...'), impressa pela helper "
            "compartilhada, que engole a excecao em vez de levantar."
        )

    novas = depois - antes
    print(f"  {database}.{table}: {len(df):,} linhas enviadas, {achadas:,} conferidas no banco, "
          f"total {depois:,} ({novas:+,} novas, o resto atualizado)")
    return depois
