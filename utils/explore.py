# -*- coding: utf-8 -*-
"""Caminho curto entre uma tabela do MySQL e um grafico, para construir modelo.

Isto NAO gera relatorio: quem faz isso e o `generate_report.py` de cada area,
sobre `analytics/report_structure/`. Aqui o grafico e descartavel -- existe para
voce olhar enquanto estima, numa celula `#%%` do VS Code ou num script rodado
com `uv run python`. Por isso o modulo e deliberadamente pequeno: no dia em que
`plot()` comecar a receber argumento de cor, titulo de eixo e fonte, o trabalho
deixou de ser exploracao e passou a ser relatorio -- e ai ele muda de pasta.

Uso tipico:

    # %%
    from utils import explore as ex

    ex.tables("macro_brasil")                          # o que existe
    df = ex.load("macro_brasil", "atv_pib", wide=True, seasonal_adjs="Y")
    ex.peek(df)                                        # inicio, fim, n, ultimo
    ex.plot(df, ["industria", "servicos"])

Tres coisas que a `load()` resolve e que doem quando feitas a mao:

  - o MySQL devolve `value` como `Decimal` e `date` como `datetime.date`, os dois
    em coluna `object`. `numpy` e `statsmodels` quebram nisso, e o sintoma
    aparece longe da leitura -- nao no `SELECT`;
  - a maioria das tabelas vem em formato longo (`date`/`name`/`value`) e modelo
    se escreve sobre o largo;
  - as tabelas com dimensao extra (ajuste sazonal, indice, item) trazem a mesma
    serie mais de uma vez, entao o pivot cru levanta "duplicate entries" -- ou,
    quando a dimensao e ignorada, passa calado com a serie errada.
"""

from __future__ import annotations

import os
from decimal import Decimal

import mysql.connector
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

#: Passe para `fig.show(config=explore.CONFIG)` se quiser zoom de scroll --
#: o Plotly nao tem config default global, entao ela viaja na chamada.
CONFIG = {"scrollZoom": True, "displaylogo": False}

#: Paleta LIS, a mesma dos relatorios (ver a memoria `project-lis-brand-colors`).
CORES = ["#1F2853", "#BB9B1D", "#418791", "#A33B3B",
         "#6B7A99", "#7E6BA8", "#3E7A4C", "#C4772F"]

_LONGAS = ("date", "name", "value")


# -- Conexao -----------------------------------------------------------------

def _conn(schema: str | None = None):
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ.get("MYSQL_PASSWORD", ""),
        database=schema,
    )


def _coerce(df: pd.DataFrame) -> pd.DataFrame:
    """Decimal -> float, date/datetime -> Timestamp. Ver o docstring do modulo."""
    for col in df.columns:
        if df[col].dtype != object:
            continue
        amostra = df[col].dropna()
        if amostra.empty:
            continue
        primeiro = amostra.iloc[0]
        if isinstance(primeiro, Decimal):
            df[col] = pd.to_numeric(df[col], errors="coerce")
        elif hasattr(primeiro, "year"):          # date / datetime
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


# -- Descoberta --------------------------------------------------------------

def tables(schema: str | None = None) -> pd.DataFrame:
    """Sem argumento lista os schemas; com um schema, as tabelas dele.

    A contagem de linhas do InnoDB e uma ESTIMATIVA do proprio MySQL -- serve
    para achar a tabela, nao para conferir carga.
    """
    if schema is None:
        return q(
            "SELECT schema_name AS schema_ FROM information_schema.schemata "
            "WHERE schema_name NOT IN "
            "('information_schema','mysql','performance_schema','sys') "
            "ORDER BY schema_name"
        )
    return q(
        "SELECT table_name AS tabela, table_rows AS linhas_aprox "
        "FROM information_schema.tables WHERE table_schema = %(s)s "
        "ORDER BY table_name",
        params={"s": schema},
    )


def columns(schema: str, table: str) -> pd.DataFrame:
    """Colunas da tabela, com o COMMENT do MySQL (ver a memoria de documentacao)."""
    return q(
        "SELECT column_name AS coluna, column_type AS tipo, "
        "column_comment AS comentario FROM information_schema.columns "
        "WHERE table_schema = %(s)s AND table_name = %(t)s "
        "ORDER BY ordinal_position",
        params={"s": schema, "t": table},
    )


# -- Leitura -----------------------------------------------------------------

def q(sql: str, schema: str | None = None, params=None) -> pd.DataFrame:
    """Roda um SELECT qualquer e devolve DataFrame ja com os tipos corrigidos.

    E o que o `MySQLDataRequester` nao faz: ele so sabe `SELECT * FROM tabela`,
    entao join, filtro e agregacao passam por aqui.
    """
    cn = _conn(schema)
    try:
        cur = cn.cursor()
        cur.execute(sql, params or ())
        df = pd.DataFrame(cur.fetchall(), columns=list(cur.column_names))
        cur.close()
    finally:
        cn.close()
    return _coerce(df)


def load(schema: str, table: str, wide: bool | None = None, **filtros) -> pd.DataFrame:
    """Le uma tabela inteira, opcionalmente filtrada e pivotada para largo.

    `wide=None` (default) pivota apenas quando a tabela e exatamente
    `date`/`name`/`value`; havendo dimensao extra devolve longo, porque pivotar
    sem escolher a dimensao produziria serie duplicada.

    `wide=True` pivota de qualquer jeito e dobra a dimensao que sobrou dentro do
    nome da coluna (`industria | Y`), o que e explicito em vez de silencioso.

    Filtros viram `WHERE coluna = valor`, parametrizados:

        load("macro_brasil", "atv_pib", wide=True, seasonal_adjs="Y")
    """
    sql = f"SELECT * FROM `{table}`"
    params: dict = {}
    if filtros:
        clausulas = []
        for i, (col, val) in enumerate(filtros.items()):
            chave = f"p{i}"
            clausulas.append(f"`{col}` = %({chave})s")
            params[chave] = val
        sql += " WHERE " + " AND ".join(clausulas)
    df = q(sql, schema=schema, params=params or None)

    if df.empty or wide is False:
        return df

    # `name` e a convencao do macro_brasil; o macro_us identifica a serie por
    # varias colunas (indice, item_code, ajuste) e nao tem `name` nenhum.
    eixo = {"date", "value"}
    if not eixo.issubset(df.columns):
        if wide:
            raise ValueError(
                f"`{table}` nao tem colunas `date` e `value` (tem {list(df.columns)}); "
                "para pivotar uma tabela assim use `q()` e um `pivot` explicito"
            )
        return df

    dims = [c for c in df.columns if c not in _LONGAS]
    if wide is None and dims:
        return df

    # O rotulo cresce so enquanto a coluna acrescentada SEPARA mais series.
    # Isso tira de uma vez a dimensao fixada pelo filtro (que nao distingue
    # nada) e a redundante -- `series_id` repete `item_code` uma vez que o
    # indice e o ajuste ja foram escolhidos, e o legenda ficaria com os dois.
    uteis = (["name"] if "name" in df.columns else [])
    uteis += [c for c in dims if df[c].nunique(dropna=False) > 1]
    rotulo = None
    for col in uteis:
        if rotulo is None:
            rotulo = df[col].astype(str)
            continue
        candidato = rotulo + " | " + df[col].astype(str)
        if candidato.nunique() > rotulo.nunique():
            rotulo = candidato
    if rotulo is None:
        # Sem `name` e sem dimensao: sobrou uma serie so, e o rotulo honesto
        # e a propria tabela.
        rotulo = pd.Series(table, index=df.index)
    largo = df.assign(_rotulo=rotulo).pivot(
        index="date", columns="_rotulo", values="value"
    )
    largo.columns.name = None
    return largo.sort_index()


def peek(df: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por serie: inicio, fim, numero de pontos e ultimo valor.

    Serve aos dois formatos -- largo (colunas) e longo (`name`/`date`/`value`).
    """
    if set(_LONGAS).issubset(df.columns):
        vivo = df.dropna(subset=["value"]).sort_values("date")
        g = vivo.groupby("name")["date"]
        out = pd.DataFrame({"inicio": g.min(), "fim": g.max(), "n": g.count()})
        out["ultimo"] = vivo.groupby("name")["value"].last()
        return out.sort_index()

    linhas = {}
    for col in df.columns:
        s = df[col].dropna()
        if s.empty:
            linhas[col] = {"inicio": None, "fim": None, "n": 0, "ultimo": None}
        else:
            linhas[col] = {"inicio": s.index.min(), "fim": s.index.max(),
                           "n": int(s.size), "ultimo": s.iloc[-1]}
    return pd.DataFrame(linhas).T


# -- Grafico -----------------------------------------------------------------

def plot(df: pd.DataFrame, cols=None, title: str = "", log: bool = False,
         bars: bool = False):
    """Desenha e devolve a figura. Arrastar da pan; duplo clique reseta.

    Para zoom de scroll: `ex.plot(df).show(config=ex.CONFIG)` -- o Plotly nao
    aceita config default global, entao ela precisa viajar na chamada.
    """
    import plotly.graph_objects as go

    if set(_LONGAS).issubset(df.columns):
        df = df.pivot(index="date", columns="name", values="value").sort_index()
    if cols is not None:
        cols = [cols] if isinstance(cols, str) else list(cols)
        faltam = [c for c in cols if c not in df.columns]
        if faltam:
            raise KeyError(f"colunas ausentes: {faltam}")
        df = df[cols]

    fig = go.Figure()
    for i, col in enumerate(df.columns):
        cor = CORES[i % len(CORES)]
        if bars:
            traco = go.Bar(x=df.index, y=df[col], name=str(col), marker_color=cor)
        else:
            traco = go.Scatter(
                x=df.index, y=df[col], name=str(col), mode="lines",
                line=dict(color=cor, width=1.8,
                          dash=None if i < len(CORES) else "dash"),
            )
        fig.add_trace(traco)

    fig.update_layout(
        title=title or None,
        dragmode="pan",
        hovermode="x unified",
        template="plotly_white",
        margin=dict(l=55, r=20, t=45 if title else 20, b=40),
        legend=dict(orientation="h", y=-0.18, x=0),
        height=420,
    )
    if log:
        fig.update_yaxes(type="log")
    return fig
