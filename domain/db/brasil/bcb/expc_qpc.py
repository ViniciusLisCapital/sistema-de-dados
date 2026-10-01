"""
Questionario Pre-Copom (QPC), resultados quantitativos agregados -> macro_brasil.expc_qpc.

Fonte: planilha do Depec publicada no dia seguinte a ata de cada reuniao
(`connectors/bcb_qpc.py`). O parser que transforma cada aba em linhas esta em
`_qpc.py`, com a lista dos blocos lidos e os formatos antigos que ele absorve.

## Por que expc_ e nao pm_

E expectativa de mercado -- as mesmas instituicoes do Focus respondendo antes da
reuniao --, nao estimativa nem decisao do BC. Mesmo prefixo das tres `expc_focus*`.
O que o QPC tem que o Focus nao tem: o "deveria fazer" ao lado do "fara", o vies de
risco, a leitura qualitativa de ambiente externo e fiscal, e o hiato do mercado.

## A tabela

Longa, uma linha por (edicao, bloco, variavel, periodo de referencia, categoria,
estatistica). Guarda o que o BCB publica, nada derivado:

    estatistica = respostas     contagem por faixa (so copom_decisao; o % publicado e
                                conferido contra ela na carga e nao e gravado)
                | fracao        participacao de 0 a 1 de cada categoria (vieses,
                                ambiente externo, situacao fiscal, prob_desvio)
                | p25 | mediana | p75 | media | n_respostas

Duas datas, como na `expc_focus_periodo`: `date` e o dia em que o resultado foi
PUBLICADO (lido da capa da planilha) e `ref_date` o 1o dia do periodo a que a
resposta se refere -- o mes, o trimestre, o ano ou o mes da reuniao-alvo. Quem quer
a historia da revisao fixa `referencia` e varre `nro_reuniao`.

`referencia` e texto no formato de cada bloco: `R282` (reuniao-alvo), `2026`,
`2026-09`, `2026T3`, um horizonte (`curto_prazo` | `2a` | `5a`, em juro_real_neutro,
pib_potencial e nairu -- ai `ref_date` e nulo), ou '' quando a pergunta nao tem periodo
(ambiente externo e situacao fiscal perguntam sobre a mudanca DESDE O ULTIMO COPOM). `categoria` e ''
quando nao se aplica, porque coluna de PK nao aceita NULL.

Unidades por bloco: copom_decisao em pontos-base (a faixa, em `categoria`) e numero
de respostas; ipca_curto_prazo em % a.m.; pib_trimestral e ipca_4t em %; hiato em %
do PIB potencial; juro_real_neutro em % a.a.; pib_potencial em % de crescimento ao ano;
nairu em % da forca de trabalho; fracao de 0 a 1.

## Carga

A rotina relê a ultima edicao do banco e busca as seguintes; `full=True` recarrega
da 238a. A lista de edicoes vem da listagem de atas do BCB
(`connectors/bcb_copom.calendario_reunioes`), que e exatamente o conjunto certo: o QPC
sai depois da ata. A 239a nao tem arquivo publicado e fica de fora.

Banco: macro_brasil.expc_qpc --
PRIMARY KEY (nro_reuniao, bloco, variavel, referencia, categoria, estatistica)
"""

from __future__ import annotations

import datetime as dt
import logging
import os

import mysql.connector
import pandas as pd

from connectors.bcb_copom import calendario_reunioes
from connectors.bcb_qpc import PRIMEIRA_EDICAO, QPC
from connectors.mysql import insert_data_into_database
from domain.db.brasil.bcb import _qpc

logger = logging.getLogger(__name__)

_DATABASE = "macro_brasil"
_TABLE = "expc_qpc"

_COLUNAS = ["nro_reuniao", "date", "bloco", "variavel", "referencia", "categoria",
            "estatistica", "valor", "ref_date"]

# Bloco -> primeira edicao em que ele deve existir. A falta dele numa edicao posterior
# e aviso, nao erro: o BCB pode tirar uma pergunta do questionario, e uma aba que o
# parser deixou de reconhecer tem a mesma cara. `copom_decisao` e a excecao -- sem ela
# o arquivo nao e o QPC que conhecemos, e a carga para.
_ESPERADOS = {"vies_ipca": 240, "vies_pib": 240, "ambiente_externo": 240,
              "situacao_fiscal": 242, "ipca_curto_prazo": 254}

_DDL = """
CREATE TABLE IF NOT EXISTS expc_qpc (
    nro_reuniao SMALLINT     NOT NULL COMMENT 'Edicao: a reuniao do Copom que o questionario antecede',
    date        DATE         NOT NULL COMMENT 'Dia em que o BCB publicou o resultado (capa da planilha), o dia seguinte a ata',
    bloco       VARCHAR(32)  NOT NULL COMMENT 'copom_decisao | vies_ipca | vies_pib | ambiente_externo | situacao_fiscal | ipca_curto_prazo | pib_trimestral | hiato | ipca_horizonte_relevante | juro_real_neutro | pib_potencial | nairu',
    variavel    VARCHAR(32)  NOT NULL COMMENT 'copom_decisao: fara | deveria. vies_*: ipca | pib. ipca_curto_prazo: ipca | servicos_subjacentes | media_nucleos. pib_trimestral: yoy | qoq_sa. hiato: hiato. ipca_horizonte_relevante: ipca_4t | prob_desvio. Demais (inclusive juro_real_neutro, pib_potencial, nairu): o proprio bloco',
    referencia  VARCHAR(16)  NOT NULL COMMENT 'Periodo a que a resposta se refere: R<n> (reuniao-alvo), AAAA, AAAA-MM, AAAATn, horizonte (curto_prazo | 2a | 5a) em juro_real_neutro/pib_potencial/nairu, ou vazio quando a pergunta e sobre a mudanca desde o ultimo Copom',
    categoria   VARCHAR(40)  NOT NULL COMMENT 'Faixa em p.b. (copom_decisao), opcao de resposta (vies, ambiente, fiscal) ou faixa de desvio (prob_desvio: abaixo_0_5pp | entre_0_5pp | acima_0_5pp, em relacao a PROPRIA projecao); vazio quando nao se aplica',
    estatistica VARCHAR(16)  NOT NULL COMMENT 'respostas (contagem) | fracao (0 a 1) | p25 | mediana | p75 | media | n_respostas',
    valor       DOUBLE       NOT NULL,
    ref_date    DATE         NULL     COMMENT '1o dia do periodo de referencia (mes da reuniao-alvo em copom_decisao); nulo sem periodo e nos horizontes',
    PRIMARY KEY (nro_reuniao, bloco, variavel, referencia, categoria, estatistica),
    KEY idx_revisao (bloco, variavel, referencia, nro_reuniao)
) COMMENT='Questionario Pre-Copom do BCB, resultados quantitativos agregados publicados desde a 238a reuniao (mai/2021): o que o mercado acha que o Copom fara e deveria fazer, vieses de risco, ambiente externo e fiscal, IPCA de curto prazo, PIB trimestral, hiato, juro real neutro, PIB potencial e Nairu. Expectativa de mercado, nao estimativa do BC.'
"""


def _conectar():
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ.get("MYSQL_PASSWORD", ""),
        database=_DATABASE,
    )


def _consultar(sql: str) -> list[tuple]:
    cnx = _conectar()
    try:
        cur = cnx.cursor()
        cur.execute(sql)
        return cur.fetchall()
    finally:
        cnx.close()


def _garantir_tabela() -> None:
    """IF NOT EXISTS, entao idempotente -- mesma escolha de `us/inflation/expc_inflacao.py`."""
    cnx = _conectar()
    try:
        cur = cnx.cursor()
        cur.execute(_DDL)
        cnx.commit()
    finally:
        cnx.close()


def coletar(edicoes: list[int], datas: dict[int, dt.date], qpc: QPC | None = None) -> pd.DataFrame:
    """Baixa e le as edicoes pedidas. Edicao sem arquivo publicado e pulada com aviso."""
    qpc = qpc or QPC()
    linhas: list[dict] = []
    for n in edicoes:
        url = qpc.localizar(n, datas[n])
        if url is None:
            logger.warning("expc_qpc: edicao %d sem arquivo publicado", n)
            continue
        wb = qpc.abrir(url)
        publicado = qpc.publicado_em(wb)
        if not datas[n] <= publicado <= datas[n] + dt.timedelta(days=30):
            # A capa da 246a diz 07/07/2022, a data da 247a -- copiada. O resultado sai
            # no dia seguinte a ata, 7 dias depois da decisao em todas as outras edicoes.
            corrigido = datas[n] + dt.timedelta(days=7)
            logger.warning("expc_qpc: edicao %d com capa datada %s, fora de [%s, +30d]; "
                           "gravando %s", n, publicado, datas[n], corrigido)
            publicado = corrigido
        rows = _qpc.parse(wb, n, datas[n])
        blocos = {r["bloco"] for r in rows}
        if "copom_decisao" not in blocos:
            raise RuntimeError(f"expc_qpc: edicao {n} sem a questao 1 ({url})")
        faltam = [b for b, desde in _ESPERADOS.items() if n >= desde and b not in blocos]
        if faltam:
            logger.warning("expc_qpc: edicao %d sem %s", n, faltam)
        for r in rows:
            r["date"] = publicado
        linhas += rows
        logger.info("expc_qpc: %d  publicado %s  %4d linhas  %s", n, publicado, len(rows),
                    ", ".join(sorted(blocos)))
    return pd.DataFrame(linhas, columns=_COLUNAS)


def run(full: bool = False) -> None:
    """Atualiza macro_brasil.expc_qpc.

    Rotina: a ultima edicao do banco (republicacao) e todas as seguintes que a listagem de
    atas ja tem. `full=True`: da 238a em diante.
    """
    _garantir_tabela()
    datas = {n: dt.date.fromisoformat(d) for n, d in calendario_reunioes().items()
             if n >= PRIMEIRA_EDICAO and d}
    ultima = None if full else (_consultar(f"SELECT MAX(nro_reuniao) FROM {_TABLE}")[0][0])
    edicoes = sorted(n for n in datas if ultima is None or n >= ultima)
    if not edicoes:
        logger.info("expc_qpc: nada a buscar")
        return
    df = coletar(edicoes, datas)
    if df.empty:
        logger.info("expc_qpc: nenhuma edicao nova publicada")
        return
    insert_data_into_database(_DATABASE, _TABLE, df)
    # insert_data_into_database imprime o erro e retorna normalmente (ver domain/db/CLAUDE.md);
    # conferir no banco e o que impede a carga de mentir.
    gravadas = {r[0]: r[1] for r in _consultar(
        f"SELECT nro_reuniao, COUNT(*) FROM {_TABLE} GROUP BY nro_reuniao")}
    for n, esperadas in df.groupby("nro_reuniao").size().items():
        if gravadas.get(n, 0) < esperadas:
            raise RuntimeError(f"expc_qpc: edicao {n} enviou {esperadas} linhas e o banco tem "
                               f"{gravadas.get(n, 0)}")
    logger.info("expc_qpc: %d linhas de %d edicoes (%d a %d)", len(df), df["nro_reuniao"].nunique(),
                df["nro_reuniao"].min(), df["nro_reuniao"].max())


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    run()
