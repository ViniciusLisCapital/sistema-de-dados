"""
PNAD Continua - Pesquisa Nacional por Amostra de Domicilios

Dados coletados:
  ocup_*  - Pessoas ocupadas por posicao (agr 6320, var 4090, cls 11913)
  ocup_*  - Pessoas ocupadas por atividade (agr 6323, var 4090, cls 888)
  forca_* - Condicao na forca de trabalho (agr 6318, var 1641, cls 629)
  massa_* - Massa de rendimentos (agr 6392, vars 6293/6288, sem classificacao)
  rend_*  - Rendimento medio habitual por posicao (agr 6389, var 5932, cls 11913)
  rend_*  - Rendimento medio habitual por atividade (agr 6391, var 5932, cls 888)
  rend_efetivo_* - Rendimento medio efetivo (agr 6387 vars 5935/5931, agr 6388 var 5934, sem classificacao)

Banco: brasil.pnad
Nota: nomes prefixados por tipo (ocup_, rend_, forca_, massa_) para evitar
      colisao de chaves entre indicadores diferentes com mesma categoria.
"""

from datetime import datetime

import pandas as pd

from connectors.ibge import IBGE
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "pnad"

# --- Categorias base ---------------------------------------------------------

# Posicao na ocupacao (cls 11913) — compartilhada por 6320 e 6389
_POSICAO_BASE = {
    "31722": "priv_excl_domestico_com_carteira",
    "31723": "priv_excl_domestico_sem_carteira",
    "31725": "domestico_com_carteira",
    "31726": "domestico_sem_carteira",
    "31728": "pub_excl_militar_com_carteira",
    "31729": "pub_excl_militar_sem_carteira",
    "31730": "pub_militar_estatutario",
    "45934": "empregador_cnpj",
    "45935": "empregador_sem_cnpj",
    "45936": "conta_propria_cnpj",
    "45937": "conta_propria_sem_cnpj",
    "31731": "familiar_auxiliar",       # presente em ocupacao, ausente em rendimento
}

# Atividade principal (cls 888) — compartilhada por 6323 e 6391
_ATIVIDADE_BASE = {
    "47947": "agropecuaria",
    "47948": "industria_geral",
    "47949": "construcao",
    "47950": "comercio_rep_veiculo",
    "56622": "transporte_armazenagem_correio",
    "56623": "alojamento_alimentacao",
    "56624": "inform_comun_financ_imob_prof_adm",
    "60032": "admpub_educ_saude_segsoc",
    "56627": "outros_servicos",
    "56628": "servicos_domesticos",
}

# Condicao na forca de trabalho (cls 629)
_FORCA_BASE = {
    "32387": "ocupado",
    "32446": "desocupado",
    "32447": "fora_da_forca_trabalho",
}

# Massa de rendimentos — mapeados por variavel_id (6392, sem classificacao)
_MASSA_BASE = {
    "6293": "massa_real_habitual",
    "6288": "massa_nominal_habitual",
}

# --- Versoes com prefixo para o banco ----------------------------------------
# Prefixos separam o tipo de indicador e evitam conflito de chave primaria
# (ex.: ocup_industria_geral != rend_industria_geral)

_OCUP_POSICAO  = {k: f"ocup_{v}"  for k, v in _POSICAO_BASE.items()}
_OCUP_ATIVIDADE = {k: f"ocup_{v}" for k, v in _ATIVIDADE_BASE.items()}
_FORCA         = _FORCA_BASE          # nomes ja unicos (ocupado, desocupado, ...)
_MASSA         = _MASSA_BASE          # nomes ja unicos (massa_real_habitual, ...)
_REND_POSICAO  = {
    "96165": "rend_media_nacional",   # total presente so em rendimento
    **{k: f"rend_{v}" for k, v in _POSICAO_BASE.items() if k != "31731"},
}
_REND_ATIVIDADE = {k: f"rend_{v}" for k, v in _ATIVIDADE_BASE.items()}

# Rendimento efetivo — agr 6387 (todos os trabalhos) e 6388 (trabalho principal)
_REND_EFETIVO = {
    "5935": "rend_efetivo_real_todos_trabalhos",
    "5931": "rend_efetivo_nominal_todos_trabalhos",
    "5934": "rend_efetivo_real_trabalho_principal",
}

# -----------------------------------------------------------------------------

_ibge = IBGE()


def _fetch_cls(agregado: int, variavel: int,
               cls_id: int, cat_ids: dict, periodos) -> pd.DataFrame:
    """Busca indicador PNAD com uma classificacao e retorna DataFrame tidy.

    Args:
        agregado:  ID do agregado IBGE.
        variavel:  ID da variavel principal.
        cls_id:    ID da classificacao.
        cat_ids:   dict {str(cat_id): nome_curto} com as categorias a coletar.
        periodos:  qualquer formato aceito pelo connector IBGE:
                     "202001-202412"  range explicito
                     (2020, 2024)     tupla de anos
                     "last:24"        ultimos N periodos
                     "all"            serie historica completa

    Returns:
        DataFrame com colunas: date, name, value.
    """
    df = _ibge.get(
        agregado=agregado,
        variaveis=variavel,
        classificacoes={cls_id: [int(k) for k in cat_ids]},
        localidades={"N1": "all"},
        periodos=periodos,
    )
    df["name"] = df["class_1_id"].map(cat_ids)
    return df[["date", "name", "value"]]


def _fetch_massa(periodos) -> pd.DataFrame:
    """Busca massa de rendimentos habituais (agr 6392, sem classificacao).

    Coleta duas variaveis simultaneamente: real (6293) e nominal (6288).

    Args:
        periodos: qualquer formato aceito pelo connector IBGE.

    Returns:
        DataFrame com colunas: date, name, value.
    """
    df = _ibge.get(
        agregado=6392,
        variaveis=[6293, 6288],
        localidades={"N1": "all"},
        periodos=periodos,
    )
    df["name"] = df["variavel_id"].astype(str).map(_MASSA)
    return df[["date", "name", "value"]]


def _fetch_rend_efetivo(periodos) -> pd.DataFrame:
    """Busca rendimento medio efetivo de todos os trabalhos (agr 6387) e do
    trabalho principal (agr 6388).

    Args:
        periodos: qualquer formato aceito pelo connector IBGE.

    Returns:
        DataFrame com colunas: date, name, value.
    """
    df_todos = _ibge.get(
        agregado=6387,
        variaveis=[5935, 5931],
        localidades={"N1": "all"},
        periodos=periodos,
    )
    df_principal = _ibge.get(
        agregado=6388,
        variaveis=5934,
        localidades={"N1": "all"},
        periodos=periodos,
    )
    df = pd.concat([df_todos, df_principal], ignore_index=True)
    df["name"] = df["variavel_id"].astype(str).map(_REND_EFETIVO)
    return df[["date", "name", "value"]]


def run(years_back: int = 2, periodos=None) -> None:
    """Atualiza brasil.pnad (ocupacao, forca de trabalho, rendimento e massa salarial).

    Args:
        years_back: anos anteriores ao ano atual (default 2).
                    Ignorado se periodos for fornecido.
        periodos:   qualquer formato aceito pelo connector IBGE:
                      "202001-202412"  range explicito
                      (2020, 2024)     tupla de anos
                      "last:24"        ultimos N periodos
                      "all"            serie historica completa
    """
    if periodos is None:
        ano_fim  = datetime.now().year
        periodos = (ano_fim - years_back, ano_fim)

    frames = [
        _fetch_cls(6320, 4090, 11913, _OCUP_POSICAO,   periodos),
        _fetch_cls(6323, 4090,   888, _OCUP_ATIVIDADE, periodos),
        _fetch_cls(6318, 1641,   629, _FORCA,          periodos),
        _fetch_massa(periodos),
        _fetch_cls(6389, 5932, 11913, _REND_POSICAO,   periodos),
        _fetch_cls(6391, 5932,   888, _REND_ATIVIDADE, periodos),
        _fetch_rend_efetivo(periodos),
    ]
    df = pd.concat(frames, ignore_index=True)
    df["region"] = "Brasil"
    insert_data_into_database(_DATABASE, _TABLE, df)