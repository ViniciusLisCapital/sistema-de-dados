"""
Decomposicao do IPCA e IPCA-15 por subitem: variacao mensal, peso e contribuicao.

Schema macro_brasil.inflc_decomposicao:
  PRIMARY KEY (date, indice, subitem_codigo)
  Colunas: date DATE | indice VARCHAR(10) | subitem_codigo VARCHAR(10) |
           var_mensal DOUBLE | pesos DOUBLE | contribuicao DOUBLE

DDL:
  DROP TABLE IF EXISTS macro_brasil.inflc_decomposicao;
  CREATE TABLE macro_brasil.inflc_decomposicao (
      date            DATE          NOT NULL,
      indice          VARCHAR(10)   NOT NULL,
      subitem_codigo  VARCHAR(10)   NOT NULL,
      var_mensal      DOUBLE,
      pesos           DOUBLE,
      contribuicao    DOUBLE,
      PRIMARY KEY (date, indice, subitem_codigo)
  );

IBGE publica a decomposicao por subitem em agregados SIDRA diferentes por
vigencia de estrutura de ponderacao (cada atualizacao de POF ganha um
agregado novo, nao uma extensao do atual) — VIGENCIAS abaixo mapeia cada
vigencia ao(s) agregado(s)/variavel(is) corretos. IDs de variavel (var_mensal/
pesos) NUNCA mudam dentro de um indice (IPCA: 63/66 sempre; IPCA15: 355/357
sempre) — so o(s) agregado(s) muda(m) por vigencia. A classificacao usada em
todo esse intervalo (ago/1999-hoje) e sempre 315 ("Geral, grupo, subgrupo,
item e subitem"); classificacao 72 (pre-ago/1999) esta fora de escopo.

IMPORTANTE: pedir o ID de variavel errado para um agregado nao retorna 404 —
a API do IBGE responde 500 (bug deles), o que parece inicialmente um
problema de payload grande demais. Confirmar sempre via
ibge.metadados(agregado).variaveis antes de adicionar uma vigencia nova.

Deteccao de subitem: por comprimento do codigo (regex `^(\\d+)\\.` sobre
categoria_nome, subitem <=> len(code) == 7), NUNCA por `nivel` — `nivel` e
inconsistente entre agregados desta faixa (4 em alguns, 3 em outros, -1 em
todos os registros do agregado 1419, sem excecao).

Caso especial: a vigencia ago/1999-jun/2006 (IPCA) e a UNICA em que
var_mensal e pesos vem de agregados SEPARADOS (655 e 656, respectivamente) —
nao ha um agregado unico com as duas variaveis nesse periodo. Isso nao exige
tratamento especial no codigo: _fetch_vigencia() busca cada coluna
independentemente e faz merge por (date, subitem_codigo), que funciona
identicamente estejam as duas colunas no mesmo agregado ou em agregados
diferentes.

`pesos` ja vem dividido por 100 (a API retorna em pontos percentuais, ex.:
0.4988 = 0.4988% do indice). `contribuicao = var_mensal * pesos`; a soma das
contribuicoes dos subitens reproduz aproximadamente a variacao do indice
geral (ja armazenada em macro_brasil.inflc_agregados).

Nao armazena variacao 12 meses por subitem — ver mesma decisao documentada
antes: preferiu-se calcular acumulados/YoY a partir de var_mensal na camada
de consumo (generate_report.py) em vez de manter uma segunda fonte de
verdade no banco.

Validacao cruzada disponivel para ago/1999-set/2014: Thiago Sevilhano
Martinez (Ipea, TD 2056, 2015) compatibilizou uma serie por subitem para
esse periodo a partir de dados do proprio BCB (Coace/Depec) — ver
analytics/brasil/inflation/referencia/TD2056_IPEA_apendice_classificacoes.xlsx
(abas sub_var/sub_peso). Usado so como conferencia pontual, nao como fonte
dos dados em producao.

Uso:
    uv run python -c "from domain.db.brasil.ibge.inflc_decomposicao import run; run()"
    uv run python -c "from domain.db.brasil.ibge.inflc_decomposicao import backfill; backfill()"
"""

import logging
import re
from dataclasses import dataclass

import pandas as pd

from connectors.ibge import IBGE
from connectors.mysql import insert_data_into_database

logger = logging.getLogger(__name__)

_DATABASE = "macro_brasil"
_TABLE = "inflc_decomposicao"
_CLASSIFICACAO = 315
_CODE_RE = re.compile(r"^(\d+)\.")


@dataclass(frozen=True)
class Fonte:
    agregado: int
    variavel: int


@dataclass(frozen=True)
class Vigencia:
    inicio: str  # "YYYYMM"
    fim: str | None  # None = vigencia atual
    var_mensal: Fonte
    pesos: Fonte

    @property
    def agregados(self) -> tuple[int, ...]:
        return tuple(sorted({self.var_mensal.agregado, self.pesos.agregado}))


# Uma vigencia por atualizacao de estrutura de ponderacao do IBGE. Ordem
# cronologica importa: backfill() insere nessa ordem e o upsert faz a
# vigencia mais nova prevalecer em meses de sobreposicao (nao deveria haver,
# mas e a semantica correta se houver).
VIGENCIAS: dict[str, list[Vigencia]] = {
    "IPCA": [
        Vigencia("199908", "200606", Fonte(655, 63), Fonte(656, 66)),  # unico caso: var/pesos em agregados distintos
        Vigencia("200607", "201112", Fonte(2938, 63), Fonte(2938, 66)),
        Vigencia("201201", "201912", Fonte(1419, 63), Fonte(1419, 66)),
        Vigencia("202001", None, Fonte(7060, 63), Fonte(7060, 66)),
    ],
    "IPCA15": [
        Vigencia("200005", "200607", Fonte(1646, 355), Fonte(1646, 357)),
        Vigencia("200608", "201201", Fonte(1387, 355), Fonte(1387, 357)),
        Vigencia("201202", "202001", Fonte(1705, 355), Fonte(1705, 357)),
        Vigencia("202002", None, Fonte(7062, 355), Fonte(7062, 357)),
    ],
}

_ibge = IBGE()


def _extract_code(nome: str) -> str | None:
    m = _CODE_RE.match(str(nome))
    return m.group(1) if m else None


def _subitem_ids(agregado: int) -> list[int]:
    cls = _ibge.listar_classificacoes(agregado)
    cls = cls[cls["classificacao_id"] == _CLASSIFICACAO]
    is_subitem = cls["categoria_nome"].map(
        lambda n: (c := _extract_code(n)) is not None and len(c) == 7
    )
    return cls.loc[is_subitem, "categoria_id"].astype(int).tolist()


def _fetch_coluna(agregado: int, variavel: int, ids: list[int], periodos) -> pd.DataFrame:
    raw = _ibge.get(
        agregado=agregado,
        variaveis=variavel,
        classificacoes={_CLASSIFICACAO: ids},
        localidades={"N1": "all"},
        periodos=periodos,
    )
    if raw.empty:
        return pd.DataFrame(columns=["date", "subitem_codigo", "value"])
    raw = raw.assign(subitem_codigo=raw["class_1_nome"].map(_extract_code))
    raw = raw[raw["subitem_codigo"].str.len() == 7]
    return raw[["date", "subitem_codigo", "value"]]


def _fetch_vigencia(indice: str, vig: Vigencia, periodos) -> pd.DataFrame:
    ids_var = _subitem_ids(vig.var_mensal.agregado)
    var = _fetch_coluna(vig.var_mensal.agregado, vig.var_mensal.variavel, ids_var, periodos)
    var = var.rename(columns={"value": "var_mensal"})

    if vig.pesos.agregado == vig.var_mensal.agregado:
        ids_pesos = ids_var
    else:
        ids_pesos = _subitem_ids(vig.pesos.agregado)
    pesos = _fetch_coluna(vig.pesos.agregado, vig.pesos.variavel, ids_pesos, periodos)
    pesos = pesos.rename(columns={"value": "pesos"})

    wide = var.merge(pesos, on=["date", "subitem_codigo"], how="outer")
    if wide.empty:
        return wide
    wide["pesos"] = wide["pesos"] / 100
    wide["contribuicao"] = wide["var_mensal"] * wide["pesos"]
    wide["indice"] = indice
    return wide[["date", "indice", "subitem_codigo", "var_mensal", "pesos", "contribuicao"]]


def _salvar(frames: list[pd.DataFrame]) -> None:
    if not frames:
        logger.warning("Nenhum dado retornado.")
        return
    df = pd.concat(frames, ignore_index=True)
    insert_data_into_database(_DATABASE, _TABLE, df)


def run(periodos: str = "last:24") -> None:
    """Atualiza macro_brasil.inflc_decomposicao — vigencia atual apenas
    (7060/7062), mesmo comportamento de sempre. Uso rotineiro
    (jobs/update_db.py). Para carga historica completa, ver backfill().
    """
    frames = []
    for indice, vigs in VIGENCIAS.items():
        vig_atual = vigs[-1]
        logger.info("Buscando %s (agregados=%s, periodos=%s)...", indice, vig_atual.agregados, periodos)
        df = _fetch_vigencia(indice, vig_atual, periodos)
        logger.info("  %d registros", len(df))
        if not df.empty:
            frames.append(df)
    _salvar(frames)


def backfill(indices: list[str] | None = None) -> None:
    """Carga historica completa: todas as vigencias de cada indice (ago/1999
    para IPCA, mai/2000 para IPCA-15), cada uma buscada no(s) agregado(s)
    proprio(s). Uso unico/manual — nao entra em jobs/update_db.py (16
    chamadas a API do IBGE no total, custo alto para rotina).

    Args:
        indices: subconjunto de VIGENCIAS a rodar (ex.: ["IPCA"]). Default:
                 todos.
    """
    frames = []
    for indice in (indices or list(VIGENCIAS)):
        for vig in VIGENCIAS[indice]:
            logger.info(
                "Buscando %s %s-%s (agregados=%s)...", indice, vig.inicio, vig.fim or "atual", vig.agregados
            )
            df = _fetch_vigencia(indice, vig, periodos="all")
            logger.info("  %d registros", len(df))
            if not df.empty:
                frames.append(df)
    _salvar(frames)


if __name__ == "__main__":
    run()
