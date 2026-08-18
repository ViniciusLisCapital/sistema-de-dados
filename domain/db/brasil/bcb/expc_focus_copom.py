"""
Expectativas Focus — CAMINHO DA SELIC POR REUNIAO DO COPOM (BCB/Olinda).

Endpoint `ExpectativasMercadoSelic`. Cada data de pesquisa traz uma linha por reuniao
futura do Copom — hoje 16 delas, de R6/2026 a R5/2028 — o que e a curva de politica
monetaria implicita no consenso, nao um numero unico. Em 2026-08-14 o consenso ia de
13,75% nas tres reunioes seguintes a 11,00% em R5/2028.

Esta tabela existe porque a `expc_focus` nao tinha coluna `reuniao` e por isso destruia
o dado: o script antigo selecionava o campo `Reuniao`, `insert_data_into_database` o
descartava no `SHOW COLUMNS`, e as 16 linhas do dia colidiam todas no mesmo
PRIMARY KEY (date, 'Selic', 'eop'), sobrando uma so por upsert. A sobrevivente era a
reuniao mais distante, de painel mais fino (53 respondentes contra ~148 das proximas),
rotulada 'eop' — que nao descrevia nada. Aquelas 5.458 linhas foram apagadas na
migracao de 2026-08; nenhum consumidor as lia, entao nenhum relatorio publicou numero
errado.

`reuniao` vem como "R<n>/<ano>" (R1..R8 no ano, oito reunioes ordinarias). A ordem
cronologica NAO e alfabetica ("R10/2027" nao existe hoje, mas ordenar por string
quebraria se a numeracao passasse de 9) e tambem nao e derivavel da data da pesquisa
sem o calendario do Copom — quem precisa de "proxima reuniao" ordena por (ano, numero)
extraidos da string, ou cruza com `domain/release_calendar/` (grupo `bcb_copom`).

`base_calculo` 0 e 1 ambos carregados: e aqui que a diferenca entre a janela de 30 dias
e a de 4 dias uteis mais informa, porque "o mercado mudou de opiniao sobre o Copom
nesta semana" e exatamente o que a base 1 mostra antes da base 0. Ver a docstring de
`expc_focus.py` para a definicao das duas. **A base 1 so comeca em 2021-03-31** neste
endpoint (contra 2004-11-18 da base 0) — nao e falha de carga, o BCB nao publica antes
disso.

Quantas reunioes o Focus cota a frente cresceu com o tempo, e isso e propriedade da
fonte, nao da carga: 1 em 2004, ~9 entre 2007 e 2009, ~12 de 2010 a 2020, 16 desde
2021. Media por data de pesquisa, base 0.

`tipo_calculo` fica em 'geral' — o endpoint `ExpectativasMercadoTop5Selic` tem a mesma
forma de chave mais essa dimensao, ainda nao carregado.

Banco: macro_brasil.expc_focus_copom
  PRIMARY KEY (date, reuniao, base_calculo, tipo_calculo)
"""

from __future__ import annotations

import logging

import pandas as pd

from domain.db.brasil.bcb import _focus_core as core

logger = logging.getLogger(__name__)

_TABLE = "expc_focus_copom"

_ENDPOINT = "ExpectativasMercadoSelic"
_START    = "2004-11-01"   # primeira data do endpoint

_COLUNAS = [
    "date", "reuniao", "base_calculo", "tipo_calculo",
    "media", "mediana", "desvio_padrao", "minimo", "maximo", "numero_respondentes",
]


def _transformar(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    df["tipo_calculo"] = "geral"
    return df[_COLUNAS]


def run(start: str | None = None, end: str | None = None, n_dias: int = 90) -> None:
    """Atualiza macro_brasil.expc_focus_copom.

    Args:
        start:  data inicial ISO "YYYY-MM-DD". Default: ultimos `n_dias` dias.
                Use start="all" para a carga historica completa (desde 2004-11).
        end:    data final ISO. Default: hoje.
        n_dias: janela retroativa usada quando start=None (default 90).
    """
    hoje = pd.Timestamp.today().strftime("%Y-%m-%d")
    if start == "all":
        start, end = _START, end or hoje
    elif start is None:
        padrao_ini, padrao_fim = core.janela_default(n_dias)
        start, end = padrao_ini, end or padrao_fim
    else:
        end = end or hoje

    n = core.carregar(_ENDPOINT, _TABLE, _transformar, start=start, end=end)
    logger.info("expc_focus_copom: %d linhas", n)
