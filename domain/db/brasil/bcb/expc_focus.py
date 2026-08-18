"""
Expectativas Focus — HORIZONTE MOVEL suavizado (BCB/Olinda).

Endpoints `ExpectativasMercadoInflacao12Meses` e `...24Meses`: a pergunta e "quanto
nos proximos 12 (ou 24) meses contados desta data", entao o periodo de referencia
nunca precisa ser nomeado — ha uma data so, a da pesquisa. Isso e o que separa esta
tabela da `expc_focus_periodo`, onde o horizonte e fixo e nomeado ("quanto em 2027")
e por isso precisa de uma segunda data. Selic por reuniao do Copom vive na terceira,
`expc_focus_copom`.

Duas dimensoes que a tabela nao tinha antes de 2026-08 e que a API sempre expos:

  suavizada     S / N. A serie suavizada interpola as previsoes de ano-calendario
                para produzir a janela movel de 12 meses; a nao suavizada e a
                leitura crua da pesquisa. IPCA nao suavizado comeca 2001-11-07,
                cinco semanas antes do suavizado (2001-12-12).
  base_calculo  0 / 1. Nao sao duas pesquisas, e a mesma pesquisa com duas janelas
                de validade — cada instituicao submete quando quer e a estatistica
                do dia usa a ultima submissao de cada uma. Definicao do BCB:
                0 = submissoes a partir do 30o dia anterior ao calculo;
                1 = submissoes a partir do 4o dia util anterior.
                Base 0 e ampla mas carrega expectativa velha, base 1 e fresca mas
                magra (135 vs. 62 respondentes no IPCA 12m de 2026-08-14, com
                medianas de 4,3204 vs. 4,4108). A base 1 vira primeiro depois de um
                choque; a base 0 confirma semanas depois.
                **A base 1 nao cobre o historico todo**: nestes endpoints ela comeca
                em 2014-01-02, contra 2001-11-07 da base 0 (medido ao vivo, 2026-08).
                Serie de base 1 comparada com base 0 antes de 2014 nao existe — nao e
                falha de carga.

`tipo_calculo` existe com valor unico `geral` porque os endpoints Top5 (as 5
instituicoes mais assertivas) tem exatamente esta forma de chave mais essa dimensao
— incluir a coluna agora torna o Top5 um backfill de dados em vez de uma migracao
de schema. Nada popula 'CURTO_PRAZO'/'MEDIO_PRAZO'/'LONGO_PRAZO' ainda.

Indicadores: so os que a pesquisa ainda publica. A familia antiga de indices de
precos (IGP-DI, INPC, IPA-DI, IPA-M, IPC-Fipe, IPCA-15) foi encerrada em 2021-02-17
em todos os endpoints do Focus e nao esta aqui — decisao explicita de escopo, nao
esquecimento. Os cinco componentes do IPCA entraram na reformulacao de 2021-09-14.

Banco: macro_brasil.expc_focus
  PRIMARY KEY (date, indicador, horizonte, suavizada, base_calculo, tipo_calculo)
"""

from __future__ import annotations

import logging

import pandas as pd

from domain.db.brasil.bcb import _focus_core as core

logger = logging.getLogger(__name__)

_TABLE = "expc_focus"

_COMPONENTES_IPCA = [
    "IPCA Livres",
    "IPCA Administrados",
    "IPCA Serviços",
    "IPCA Bens industrializados",
    "IPCA Alimentação no domicílio",
]

# horizonte -> (endpoint, indicadores vivos, primeira data do endpoint)
#
# O endpoint de 24 meses so comeca em 2021-03 — sem esse limite por horizonte, a carga
# historica pede ~230 janelas mensais garantidamente vazias e o connector avisa em cada
# uma delas.
_HORIZONTES = {
    "12m": (
        "ExpectativasMercadoInflacao12Meses",
        ["IPCA", "IGP-M", *_COMPONENTES_IPCA],
        "2001-11-01",
    ),
    "24m": (
        "ExpectativasMercadoInflacao24Meses",
        ["IPCA", *_COMPONENTES_IPCA],
        "2021-03-01",
    ),
}

_START = min(inicio for _, _, inicio in _HORIZONTES.values())

_COLUNAS = [
    "date", "indicador", "horizonte", "suavizada", "base_calculo", "tipo_calculo",
    "media", "mediana", "desvio_padrao", "minimo", "maximo", "numero_respondentes",
]


def _transformar(horizonte: str, vivos: list[str], vistos: set[str]):
    permitidos = set(vivos)

    def fn(raw: pd.DataFrame) -> pd.DataFrame:
        df = raw[raw["indicador"].isin(permitidos)].copy()
        if df.empty:
            return df
        vistos.update(df["indicador"].unique())
        df["horizonte"] = horizonte
        df["tipo_calculo"] = "geral"
        return df[_COLUNAS]

    return fn


def run(start: str | None = None, end: str | None = None, n_dias: int = 90) -> None:
    """Atualiza macro_brasil.expc_focus.

    Args:
        start:  data inicial ISO "YYYY-MM-DD". Default: ultimos `n_dias` dias.
                Use start="all" para a carga historica completa (desde 2001-11).
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

    for horizonte, (endpoint, vivos, inicio_fonte) in _HORIZONTES.items():
        ini = max(start, inicio_fonte)
        if ini > end:
            continue
        vistos: set[str] = set()
        n = core.carregar(
            endpoint, _TABLE, _transformar(horizonte, vivos, vistos),
            start=ini, end=end,
        )
        logger.info("expc_focus %s: %d linhas, %d indicadores", horizonte, n, len(vistos))
        # Um indicador configurado que nao aparece em NENHUMA janela e quase sempre
        # erro de digitacao no nome (a API casa por string exata, acento incluso) --
        # avisar, senao a serie desaparece em silencio. Numa janela curta os
        # componentes do IPCA aparecem todos, entao o aviso nao e ruidoso.
        faltando = sorted(set(vivos) - vistos)
        if faltando:
            logger.warning("expc_focus %s: sem dados para %s", horizonte, faltando)
