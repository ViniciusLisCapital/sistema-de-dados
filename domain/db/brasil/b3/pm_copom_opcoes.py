"""
Opcoes digitais de Copom da B3 -> macro_brasil.pm_copom_opcoes.

Fonte: premio de referencia do arquivo RE do pregao (`connectors/b3_premio.py`,
`parse_copom()`), o mesmo arquivo de onde sai a vol do dolar. Uma linha por pregao,
reuniao e decisao.

## O que o numero e

Cada opcao e uma call digital sobre UMA decisao do Copom: paga 100 pontos se a meta
Selic decidida mudar exatamente o que o strike diz, e zero se nao. O strike e 100 +
variacao em p.p. -- 99,75 e o corte de 25 p.b., 100,00 a manutencao --, gravado aqui
ja como `variacao_bps` (-25, 0, ...). O vencimento e o dia util seguinte a reuniao.

O premio e o valor presente de "100 se acontecer": dividido por 100 e pelo fator de
desconto ate o vencimento, e a probabilidade que o mercado atribui a decisao (neutra a
risco). A soma dos premios de uma reuniao fica em geral perto de 100 x o fator de desconto
(mediana anual de 97 a 99,7), mas nao exatamente: cada premio e formado separadamente, e a
soma ja foi de 72 a 123 num pregao. Por isso a probabilidade de cada decisao e o premio dela
sobre a SOMA da reuniao, nunca sobre 100. Quem faz essa conta e o relatorio; a tabela guarda o
premio como a B3 publica.

O strike vem com tres decimais de 2020-08 a 2023-09 (`b3_premio.parse_copom` corrige).

Conferido contra duas decisoes conhecidas: na vespera da 281a (corte de 25) a opcao de
-25 valia 96,00 e a de manutencao 3,50; na da 280a, 95,50 e 3,25.

## Ressalvas da fonte

- O premio e TEORICO (manual de aprecamento da B3), e a decisao que ninguem espera fica
  no piso de 0,02-0,03 pontos, nao em zero: a soma carrega esses pisos, e a
  probabilidade de uma decisao fora da grade de strikes listados nao aparece.
- So calls: o arquivo nao traz put de Copom.
- A posicao em aberto e o volume estao no boletim de precos (arquivo PR): tabela irma
  `pm_copom_opcoes_negocios`, com a mesma chave, desde 2020-05.

Banco: macro_brasil.pm_copom_opcoes -- PRIMARY KEY (date, vencimento, variacao_bps)
"""

from __future__ import annotations

import logging
import os

import mysql.connector
import pandas as pd

from connectors import b3_premio
from connectors.mysql import insert_data_into_database

logger = logging.getLogger(__name__)

_DATABASE = "macro_brasil"
_TABLE = "pm_copom_opcoes"
# O CPM aparece no arquivo RE entre 2020-05-05 (nenhuma linha) e 2020-07-28 (17 linhas) --
# busca binaria de 2026-10-29. A carga comeca no limite de baixo; os pregoes sem CPM nao
# geram linha.
_INICIO = "2020-05-04"
_DIAS_ROTINA = 10
# Guardas de unidade/layout: um layout lido errado poe o premio na casa dos 10^16. A soma de
# uma reuniao NAO e sempre 100 x o desconto: cada premio e formado separadamente, e medido de
# 2020 a 2026 a mediana anual fica entre 97 e 99,7, mas ha pregoes de 72 e de 123. O guarda
# so pega layout; quem decide o que e reuniao legivel e a leitura (expectativas_juros.opcoes).
_PREMIO_MAX = 100.5
_SOMA_MAX = 130.0

_DDL = """
CREATE TABLE IF NOT EXISTS pm_copom_opcoes (
    date          DATE    NOT NULL COMMENT 'Pregao',
    vencimento    DATE    NOT NULL COMMENT 'Vencimento da opcao: o dia util seguinte a reuniao do Copom',
    variacao_bps  DECIMAL(6,1) NOT NULL COMMENT 'Decisao a que a opcao se refere: variacao da meta Selic em pontos-base (strike 100 + variacao em p.p.; -25 = corte de 25, 0 = manutencao; em 2020 houve strikes de -12,5 e -10)',
    premio        DOUBLE  NOT NULL COMMENT 'Premio de referencia em pontos; a opcao paga 100 se a decisao for esta',
    PRIMARY KEY (date, vencimento, variacao_bps)
) COMMENT='Opcoes digitais de Copom da B3 (CPM): premio de referencia de cada decisao possivel em cada reuniao, do arquivo RE do pregao. A opcao paga 100 pontos se a variacao decidida for a do strike; premio / soma dos premios da reuniao = probabilidade neutra a risco da decisao. Premio teorico, piso de 0,02-0,03 nas decisoes que ninguem espera. Ver domain/db/brasil/b3/pm_copom_opcoes.py.'
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


def linhas_do_pregao(P: pd.DataFrame, data) -> pd.DataFrame:
    """(date, vencimento, variacao_bps, premio) de um pregao. So vencimentos ainda por
    vir: no dia do vencimento a opcao ja e exercicio, nao preco."""
    data = pd.Timestamp(data).normalize()
    P = P[(P["tipo"] == "C") & (P["vencimento"] > data)]
    # A mesma correcao de parse_copom, de novo aqui: o cache gravado antes dela guarda o strike
    # de 2020-08 a 2023-09 multiplicado por dez.
    k = P["strike"].where(P["strike"] <= 200, P["strike"] / 10)
    out = pd.DataFrame({
        "date": data.date(),
        "vencimento": P["vencimento"].dt.date,
        # Uma casa: em 2020, com a Selic a 2%, a B3 listou o corte de 12,5 p.b. (99,875). No
        # layout de duas casas ele sai 99,88 (2020-08-06): todo strike vive na grade de 2,5 p.b.,
        # e e para ela que a variacao e levada.
        "variacao_bps": (((k - 100) * 100) / 2.5).round() * 2.5,
        "premio": P["premio"].astype(float),
    })
    return out.drop_duplicates(["vencimento", "variacao_bps"])


def coletar(full: bool = False, dias: int = _DIAS_ROTINA, inicio: str = _INICIO) -> pd.DataFrame:
    fim = pd.Timestamp.today().normalize()
    datas = list(pd.bdate_range(inicio, fim) if full else pd.bdate_range(end=fim, periods=dias))
    b3_premio.baixar_muitos(datas, mercadoria="CPM")
    partes = []
    for d in datas:
        P = b3_premio.premios(d, mercadoria="CPM")
        if P is not None:
            partes.append(linhas_do_pregao(P, d))
    if not partes:
        return pd.DataFrame(columns=["date", "vencimento", "variacao_bps", "premio"])
    df = pd.concat(partes, ignore_index=True)
    fora = df[(df.premio < 0) | (df.premio > _PREMIO_MAX)]
    if len(fora):
        raise ValueError(f"pm_copom_opcoes: {len(fora)} premios fora de [0, {_PREMIO_MAX}]:\n"
                         f"{fora.head().to_string()}")
    soma = df.groupby(["date", "vencimento"])["premio"].sum()
    if (soma > _SOMA_MAX).any():
        raise ValueError(f"pm_copom_opcoes: soma dos premios de uma reuniao acima de {_SOMA_MAX}:\n"
                         f"{soma[soma > _SOMA_MAX].head().to_string()}")
    # Fora da grade de 25 so os de 2020 (-12,5 e -10, com a Selic a 2%); um novo merece olhar.
    fora25 = df[(df.variacao_bps % 25 != 0) & (pd.to_datetime(df.date) >= "2021-01-01")]
    if len(fora25):
        logger.warning("pm_copom_opcoes: strike fora da grade de 25 p.b.: %s",
                       sorted(fora25.variacao_bps.unique()))
    return df


def run(full: bool = False, dias: int = _DIAS_ROTINA) -> None:
    """Atualiza macro_brasil.pm_copom_opcoes.

    Args:
        full: True recarrega desde o primeiro pregao com CPM (num cache vazio, horas --
              a B3 aceita 2 conexoes; o passe da vol do dolar enche o mesmo cache).
        dias: dias uteis para tras no passe de rotina.
    """
    _garantir_tabela()
    df = coletar(full=full, dias=dias)
    if df.empty:
        logger.warning("pm_copom_opcoes: nada a inserir")
        return
    logger.info("pm_copom_opcoes: %d linhas, %s -> %s", len(df), df.date.min(), df.date.max())
    insert_data_into_database(_DATABASE, _TABLE, df)
