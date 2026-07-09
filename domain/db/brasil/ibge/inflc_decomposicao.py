"""
Decomposicao do IPCA e IPCA-15 por subitem: variacao mensal, peso e contribuicao.

Schema macro_brasil.inflc_decomposicao:
  PRIMARY KEY (date, indice, subitem)
  Colunas: date DATE | indice VARCHAR(10) | subitem VARCHAR(120) |
           var_mensal DOUBLE | pesos DOUBLE | contribuicao DOUBLE

DDL:
  DROP TABLE IF EXISTS macro_brasil.inflc_decomposicao;
  CREATE TABLE macro_brasil.inflc_decomposicao (
      date          DATE          NOT NULL,
      indice        VARCHAR(10)   NOT NULL,
      subitem       VARCHAR(120)  NOT NULL,
      var_mensal    DOUBLE,
      pesos         DOUBLE,
      contribuicao  DOUBLE,
      PRIMARY KEY (date, indice, subitem)
  );

Fonte: IBGE Agregados 7060 (IPCA) e 7062 (IPCA-15), classificacao 315
("Geral, grupo, subgrupo, item e subitem") — nivel 4 da arvore = subitem (folha).
Disponivel desde jan/2020 (IPCA) e fev/2020 (IPCA-15), base de ponderacao 2020.
IDs de subitem sao obtidos dinamicamente via listar_classificacoes() (nivel==4),
em vez de uma lista hardcoded — se o IBGE adicionar/remover subitens, o fetch
acompanha automaticamente.

IMPORTANTE: IPCA e IPCA-15 tem IDs de variavel DIFERENTES no mesmo agregado —
nao sao compartilhados. 7060 (IPCA): var_mensal=63, pesos=66. 7062 (IPCA-15):
var_mensal=355, pesos=357. Pedir o ID de variavel errado para um agregado nao
retorna 404 — a API do IBGE responde 500 (bug deles), o que pareceu
inicialmente um problema de payload grande demais. Confirmar sempre via
ibge.metadados(agregado).variaveis antes de adicionar um novo agregado aqui.

`pesos` ja vem dividido por 100 (a API retorna em pontos percentuais, ex.:
0.4988 = 0.4988% do indice). `contribuicao = var_mensal * pesos`; a soma das
contribuicoes dos subitens reproduz aproximadamente a variacao do indice geral
(ja armazenada em macro_brasil.inflc_agregados).

`subitem` usa o formato "<codigo> <nome>" (ex.: "1101002 Arroz") — o ponto do
codigo IBGE e trocado por espaco para casar com macro_brasil.inflc_dim.

Nao armazena variacao 12 meses por subitem — a API do IBGE fornece essa
variavel diretamente (63/66/2265 para IPCA, 355/357/1120 para IPCA-15), mas
foi removida em 2026-07: preferiu-se calcular acumulados/YoY a partir de
var_mensal na camada de consumo (ex.: generate_report.py ou um script de
analytics) em vez de manter uma segunda fonte de verdade no banco.

Uso:
    uv run python -c "from domain.db.brasil.ibge.inflc_decomposicao import run; run()"
    uv run python -c "from domain.db.brasil.ibge.inflc_decomposicao import run; run(periodos='all')"
"""

import logging

import pandas as pd

from connectors.ibge import IBGE
from connectors.mysql import insert_data_into_database

logger = logging.getLogger(__name__)

_DATABASE = "macro_brasil"
_TABLE = "inflc_decomposicao"

# nome -> (agregado, {variavel_id: coluna})
_AGREGADOS = {
    "IPCA":   (7060, {63: "var_mensal", 66: "pesos"}),
    "IPCA15": (7062, {355: "var_mensal", 357: "pesos"}),
}
_CLASSIFICACAO = 315
_NIVEL_SUBITEM = 4

_ibge = IBGE()


def _subitem_ids(agregado: int) -> list[int]:
    cls = _ibge.listar_classificacoes(agregado)
    cls = cls[(cls["classificacao_id"] == _CLASSIFICACAO) & (cls["nivel"] == _NIVEL_SUBITEM)]
    return cls["categoria_id"].astype(int).tolist()


def _fetch_indice(nome: str, agregado: int, variaveis: dict[int, str], periodos) -> pd.DataFrame:
    """Busca cada variavel separadamente (uma requisicao por variavel)."""
    ids = _subitem_ids(agregado)
    frames = []
    for var_id, col in variaveis.items():
        raw = _ibge.get(
            agregado=agregado,
            variaveis=var_id,
            classificacoes={_CLASSIFICACAO: ids},
            localidades={"N1": "all"},
            periodos=periodos,
        )
        if raw.empty:
            continue
        frames.append(raw[["date", "class_1_nome", "value"]].rename(columns={"value": col}))

    if not frames:
        return pd.DataFrame()

    wide = frames[0]
    for frame in frames[1:]:
        wide = wide.merge(frame, on=["date", "class_1_nome"], how="outer")
    wide = wide.rename(columns={"class_1_nome": "subitem"})
    wide["subitem"] = wide["subitem"].str.replace(".", " ", regex=False)
    wide["pesos"] = wide["pesos"] / 100
    wide["contribuicao"] = wide["var_mensal"] * wide["pesos"]
    wide["indice"] = nome
    return wide[["date", "indice", "subitem", "var_mensal", "pesos", "contribuicao"]]


def run(periodos: str = "last:24") -> None:
    """Atualiza macro_brasil.inflc_decomposicao.

    Args:
        periodos: formato aceito por connectors.ibge.IBGE.get() — "last:N", "all",
                  "YYYYMM-YYYYMM". Default: ultimos 24 meses.
                  Carga historica: run(periodos="all")  (disponivel desde jan/2020)
    """
    frames = []
    for nome, (agregado, variaveis) in _AGREGADOS.items():
        logger.info("Buscando %s (agregado %d, periodos=%s)...", nome, agregado, periodos)
        df = _fetch_indice(nome, agregado, variaveis, periodos)
        logger.info("  %d registros", len(df))
        if not df.empty:
            frames.append(df)

    if not frames:
        logger.warning("Nenhum dado retornado.")
        return

    df = pd.concat(frames, ignore_index=True)
    insert_data_into_database(_DATABASE, _TABLE, df)
