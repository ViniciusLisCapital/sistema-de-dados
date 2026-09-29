"""
ETL da grade CRUA da curva DI x pre da B3 -> macro_brasil.br_di_grade.

Fonte: o mesmo TaxaSwap.txt do arquivo de pregao que alimenta `br_interest_rate`
(connectors/b3_curvas.py), codigo `PRE`. Aquela tabela guarda a curva nos 9
vertices redondos (1M..240M), interpolados; esta guarda **todos os vertices que a
B3 publica** naquele pregao -- 65 no comeco de 2006, ~280 hoje --, sem interpolar nada.

## Por que uma segunda tabela da mesma curva

Os vertices redondos nao separam uma reuniao do Copom da seguinte: sao 8 reunioes
por ano e 5 vertices no primeiro ano. A grade publicada separa. A curva PRE e
construida pela B3 a partir dos contratos futuros de DI1, que vencem no primeiro
dia util de cada mes, e entre dois vencimentos ela e flat-forward (medido na grade
de 23/09/2026: o forward entre vertices consecutivos e constante dentro de cada mes
ate jan/2028) -- entao a grade carrega um forward por mes, que e a resolucao
necessaria para ler o caminho da Selic que o mercado precifica reuniao a reuniao
(ver `analytics/brasil/monetary_policy/expectativas_juros.py`).

Tabela separada, e nao uma quinta curva em `br_interest_rate`, por dois motivos:
a forma da chave e outra (o vertice e um prazo em dias, nao um rotulo de meses) e
o volume tambem (~1,2 M de linhas contra ~120 mil) -- `ppp_equilibrium.py` le
aquela tabela inteira, e passaria a ler dez vezes mais para descartar tudo.

## Colunas

`dc` e `du` sao os dois prazos que a propria B3 publica em cada vertice. **O `du`
e o da epoca do pregao**: a B3 conta dia util pelo calendario de feriados vigente
naquele dia, e o 20 de novembro so entrou nele em 21/12/2023 (Lei 14.759) -- um
pregao de 2021 conta nov/2024 com um dia util a mais do que um de hoje. Guardar o
publicado, e nao recalcular, e o que mantem isso visivel.

Banco: macro_brasil.br_di_grade -- PRIMARY KEY (date, dc)

DDL:
  CREATE TABLE macro_brasil.br_di_grade (
      date  DATE          NOT NULL COMMENT 'Pregao (dia util da B3)',
      dc    INT           NOT NULL COMMENT 'Prazo do vertice em dias corridos, como a B3 publica',
      du    INT           NOT NULL COMMENT 'Prazo do vertice em dias uteis, como a B3 publica -- pelo calendario de feriados vigente NAQUELE pregao',
      value DECIMAL(12,7) NOT NULL COMMENT 'Taxa DI x pre em % a.a., base 252 dias uteis, capitalizacao composta',
      PRIMARY KEY (date, dc)
  ) COMMENT='Grade crua da curva DI x pre (cod PRE do TaxaSwap.txt da B3): todos os vertices publicados em cada pregao, sem interpolacao. A versao nos 9 vertices redondos e a curva DIPRE de br_interest_rate.';
"""

from __future__ import annotations

import logging
import os

import pandas as pd

from connectors.b3_curvas import CACHE, baixar_muitos, grades
from connectors.mysql import MySQLDataRequester, insert_data_into_database

logger = logging.getLogger(__name__)

_DATABASE = "macro_brasil"
_TABLE = "br_di_grade"

# Mesmo inicio e mesma janela de rotina de br_interest_rate, pelas mesmas razoes
# (ver aquele modulo): 2006-01-02 e onde a serie de juros do banco comeca, e 10
# dias uteis por upsert fecham o atraso de a B3 publicar depois do fechamento.
_INICIO = "2006-01-02"
_DIAS_ROTINA = 10

# Faixa plausivel da taxa. Medido nos 1.228.529 vertices de 2006-01-02 a 2026-09-23:
# 1,86 (06/08/2020) a 18,15 (27/10/2008) -- nenhum pregao reprovado.
_PISO, _TETO = 1.0, 30.0
# Piso de vertices por pregao. Medido: 65 (02/01/2006) a 367.
_PISO_VERTICES = 40


def problemas(g: pd.DataFrame) -> list[str]:
    """O que esta errado com a grade de UM pregao. Vazio = passou.

    `g` tem as colunas dc, du, value. Levanta nada: quem decide e `coletar()`.
    """
    p = []
    if len(g) < _PISO_VERTICES:
        p.append(f"{len(g)} vertices, piso {_PISO_VERTICES}")
    g = g.sort_values("dc")
    # Os dois prazos andam juntos: um vertice mais distante em dias corridos nao
    # pode estar mais perto em dias uteis. E a checagem que pega um parse que
    # trocou as duas colunas de lugar -- nada mais o denunciaria.
    if not g["du"].is_monotonic_increasing or g["du"].duplicated().any():
        p.append("du nao cresce estritamente com dc")
    if ((g["du"] > g["dc"]) | (g["du"] <= 0)).any():
        p.append("du fora de (0, dc]")
    fora = g[(g["value"] < _PISO) | (g["value"] > _TETO)]
    if len(fora):
        p.append(f"{len(fora)} taxas fora de [{_PISO}, {_TETO}]")
    return p


def coletar(full: bool = False, dias: int = _DIAS_ROTINA, baixar: bool = True) -> pd.DataFrame:
    """Linhas (date, dc, du, value) dos pregoes da janela. Separado de run() para
    o teste exercitar sem tocar no banco. `baixar=False` le so o que ja esta no
    cache -- os ~235 feriados nacionais do periodo nao tem arquivo la, e sem isso
    uma recarga cheia bateria na B3 por cada um deles."""
    fim = pd.Timestamp.today().normalize()
    datas = list(pd.bdate_range(_INICIO, fim) if full else pd.bdate_range(end=fim, periods=dias))
    if baixar:
        baixar_muitos(datas)
    else:
        datas = [d for d in datas
                 if os.path.exists(os.path.join(CACHE, d.strftime("%y%m%d") + ".csv"))]

    partes, ruins = [], {}
    for d in datas:
        D = grades(d)
        if D is None:
            continue
        g = D[D["cod"] == "PRE"][["dc", "du", "taxa"]].rename(columns={"taxa": "value"})
        g = g.apply(pd.to_numeric, errors="coerce").dropna()
        if g.empty:
            continue
        probs = problemas(g)
        if probs:
            # Diferente de br_interest_rate, aqui o pregao com problema NAO entra: a
            # grade crua e o proprio insumo de uma conta reuniao a reuniao, e um
            # vertice trocado distorce a reuniao inteira em volta dele.
            ruins[d.date()] = probs
            continue
        g.insert(0, "date", d.date())
        partes.append(g)

    for data, probs in sorted(ruins.items()):
        logger.warning("br_di_grade: %s fora da carga -- %s", data, "; ".join(probs))
    if not partes:
        return pd.DataFrame(columns=["date", "dc", "du", "value"])
    df = pd.concat(partes, ignore_index=True)
    df["dc"] = df["dc"].astype(int)
    df["du"] = df["du"].astype(int)
    df["value"] = df["value"].round(7)
    return df


def _contar(datas) -> int:
    req = MySQLDataRequester(_DATABASE, _TABLE)
    req.connect()
    try:
        cur = req.connection.cursor()
        lo, hi = min(datas), max(datas)
        cur.execute(f"SELECT COUNT(*) FROM {_TABLE} WHERE date BETWEEN %s AND %s", (lo, hi))
        return int(cur.fetchone()[0])
    finally:
        req.close_connection()


def run(full: bool = False, dias: int = _DIAS_ROTINA, baixar: bool = True) -> None:
    """Atualiza macro_brasil.br_di_grade.

    Args:
        full: True recarrega de 2006-01-02 (5.131 pregoes, ~1,2 M de linhas). Usa o
              mesmo cache de domain/db/brasil/b3/cache/ que br_interest_rate; com
              baixar=True ainda tenta os feriados nacionais, que nao tem arquivo.
        dias: dias uteis para tras no passe de rotina. Default 10.
        baixar: False reconstroi so do cache, sem tocar na B3.
    """
    df = coletar(full=full, dias=dias, baixar=baixar)
    if df.empty:
        logger.warning("br_di_grade: nada a inserir")
        return
    logger.info("br_di_grade: %d linhas, %d pregoes, %s -> %s", len(df),
                df["date"].nunique(), df["date"].min(), df["date"].max())
    insert_data_into_database(_DATABASE, _TABLE, df, batch_size=5000)
    # insert_data_into_database imprime o erro e retorna normalmente (ver
    # domain/db/CLAUDE.md, `_gravar.py`); conferir no banco e o que impede um
    # "N linhas gravadas" de mentir.
    gravadas = _contar(df["date"].unique())
    if gravadas < len(df):
        raise RuntimeError(f"br_di_grade: {len(df)} linhas enviadas, {gravadas} no banco "
                           f"entre {df['date'].min()} e {df['date'].max()}")
