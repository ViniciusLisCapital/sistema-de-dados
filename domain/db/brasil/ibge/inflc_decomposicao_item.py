"""
Decomposicao do IPCA e IPCA-15 por item (4 digitos): variacao mensal, peso e
contribuicao.

Schema macro_brasil.inflc_decomposicao_item:
  PRIMARY KEY (date, indice, item_codigo)
  Colunas: date DATE | indice VARCHAR(10) | item_codigo VARCHAR(10) |
           var_mensal DOUBLE | pesos DOUBLE | contribuicao DOUBLE

DDL:
  CREATE TABLE macro_brasil.inflc_decomposicao_item (
      date          DATE         NOT NULL,
      indice        VARCHAR(10)  NOT NULL,
      item_codigo   VARCHAR(10)  NOT NULL,
      var_mensal    DOUBLE,
      pesos         DOUBLE,
      contribuicao  DOUBLE,
      PRIMARY KEY (date, indice, item_codigo)
  );

Irma de inflc_decomposicao.py (mesmos agregados/vigencias, mesma API IBGE),
so muda o nivel hierarquico filtrado: item (4 digitos, ex. "1101.Cereais,
leguminosas e oleaginosas") em vez de subitem (7 digitos). Reusa VIGENCIAS/
Fonte/_extract_code/_ibge de inflc_decomposicao.py em vez de duplicar --
mesmos agregados servem os dois niveis, so o filtro de comprimento de codigo
muda (len(code) == 4 aqui, == 7 la).

Motivacao: os nucleos MA (medias aparadas sem suavizacao), MS (com
suavizacao) e DP (dupla ponderacao) da NT-57 (Nota Tecnica do BC no 57,
analytics/brasil/inflation/referencia/Nucleos_inflacao.pdf) operam no nivel de
ITEM, nao de subitem -- confirmado tanto pela formula da nota (N_t^I,
"numero de itens") quanto pela metadata do proprio IBGE (classificacao 315,
"Geral, grupo, subgrupo, item e subitem"; nivel=3 = item/4 digitos, nivel=4
= subitem/7 digitos). P55 e Difusao, por outro lado, operam no nivel de
subitem e ja sao computados a partir de inflc_decomposicao (ver
analytics/brasil/inflation/generate_report.py::_compute_p55/_compute_difusao) --
esta tabela nova existe so para dar a MA/MS/DP o nivel de granularidade que
eles exigem.

TRADE-OFF CONHECIDO (nao implementado): a NT-57 define proxies explicitos
(Tabelas 2-4 para DP, 6-8 para MS) para os primeiros 11/48 meses de cada
nova vigencia de estrutura, quando um item foi redefinido na transicao (ex.:
"8104.Cursos diversos" ganhou/perdeu "curso tecnico" em jan/2020). Este
modulo NAO implementa esses proxies -- o historico usado no calculo de
MS/DP (ver generate_report.py::_compute_ms/_compute_dp) e a concatenacao
simples do codigo atraves das vigencias, mesma logica ja aceita para
subitem em inflc_dim.py ("retroactive relabeling"). Efeito: para os poucos
itens listados nas Tabelas 2-8, a media/volatilidade fica levemente distorcida
nos ~11/48 meses seguintes a cada transicao relevante para o IPCA-15 (ago/2006,
jan/2020 -- jul/2006-dez/2011 nao precisa de proxy, ver nota 10 da NT-57;
jan/1991-jul/1999 nao existe para o IPCA-15). Nao afeta MA (sem janela
temporal). Ver Gotchas em analytics/brasil/inflation/CLAUDE.md para o tamanho
empirico desse efeito.

Uso:
    uv run python -c "from domain.db.brasil.ibge.inflc_decomposicao_item import run; run()"
    uv run python -c "from domain.db.brasil.ibge.inflc_decomposicao_item import backfill; backfill()"
"""

import logging

import pandas as pd

from connectors.mysql import insert_data_into_database
from domain.db.brasil.ibge.inflc_decomposicao import VIGENCIAS, Vigencia, _CLASSIFICACAO, _extract_code, _ibge

logger = logging.getLogger(__name__)

_DATABASE = "macro_brasil"
_TABLE = "inflc_decomposicao_item"


def _item_ids(agregado: int) -> list[int]:
    cls = _ibge.listar_classificacoes(agregado)
    cls = cls[cls["classificacao_id"] == _CLASSIFICACAO]
    is_item = cls["categoria_nome"].map(
        lambda n: (c := _extract_code(n)) is not None and len(c) == 4
    )
    return cls.loc[is_item, "categoria_id"].astype(int).tolist()


def _fetch_coluna(agregado: int, variavel: int, ids: list[int], periodos) -> pd.DataFrame:
    raw = _ibge.get(
        agregado=agregado,
        variaveis=variavel,
        classificacoes={_CLASSIFICACAO: ids},
        localidades={"N1": "all"},
        periodos=periodos,
    )
    if raw.empty:
        return pd.DataFrame(columns=["date", "item_codigo", "value"])
    raw = raw.assign(item_codigo=raw["class_1_nome"].map(_extract_code))
    raw = raw[raw["item_codigo"].str.len() == 4]
    return raw[["date", "item_codigo", "value"]]


def _fetch_vigencia(indice: str, vig: Vigencia, periodos) -> pd.DataFrame:
    ids_var = _item_ids(vig.var_mensal.agregado)
    var = _fetch_coluna(vig.var_mensal.agregado, vig.var_mensal.variavel, ids_var, periodos)
    var = var.rename(columns={"value": "var_mensal"})

    if vig.pesos.agregado == vig.var_mensal.agregado:
        ids_pesos = ids_var
    else:
        ids_pesos = _item_ids(vig.pesos.agregado)
    pesos = _fetch_coluna(vig.pesos.agregado, vig.pesos.variavel, ids_pesos, periodos)
    pesos = pesos.rename(columns={"value": "pesos"})

    wide = var.merge(pesos, on=["date", "item_codigo"], how="outer")
    if wide.empty:
        return wide
    wide["pesos"] = wide["pesos"] / 100
    wide["contribuicao"] = wide["var_mensal"] * wide["pesos"]
    wide["indice"] = indice
    return wide[["date", "indice", "item_codigo", "var_mensal", "pesos", "contribuicao"]]


def _salvar(frames: list[pd.DataFrame]) -> None:
    if not frames:
        logger.warning("Nenhum dado retornado.")
        return
    df = pd.concat(frames, ignore_index=True)
    insert_data_into_database(_DATABASE, _TABLE, df)


def run(periodos: str = "last:24") -> None:
    """Atualiza macro_brasil.inflc_decomposicao_item -- vigencia atual
    apenas (7060/7062), mesmo comportamento de inflc_decomposicao.run().
    Uso rotineiro (jobs/update_db.py). Para carga historica completa, ver
    backfill().
    """
    frames = []
    for indice, vigs in VIGENCIAS.items():
        vig_atual = vigs[-1]
        logger.info("Buscando %s item (agregados=%s, periodos=%s)...", indice, vig_atual.agregados, periodos)
        df = _fetch_vigencia(indice, vig_atual, periodos)
        logger.info("  %d registros", len(df))
        if not df.empty:
            frames.append(df)
    _salvar(frames)


def backfill(indices: list[str] | None = None) -> None:
    """Carga historica completa: todas as vigencias de cada indice, mesma
    logica de inflc_decomposicao.backfill(). Uso unico/manual -- nao entra
    em jobs/update_db.py.

    Args:
        indices: subconjunto de VIGENCIAS a rodar (ex.: ["IPCA"]). Default:
                 todos.
    """
    frames = []
    for indice in (indices or list(VIGENCIAS)):
        for vig in VIGENCIAS[indice]:
            logger.info(
                "Buscando %s item %s-%s (agregados=%s)...", indice, vig.inicio, vig.fim or "atual", vig.agregados
            )
            df = _fetch_vigencia(indice, vig, periodos="all")
            logger.info("  %d registros", len(df))
            if not df.empty:
                frames.append(df)
    _salvar(frames)


if __name__ == "__main__":
    run()
