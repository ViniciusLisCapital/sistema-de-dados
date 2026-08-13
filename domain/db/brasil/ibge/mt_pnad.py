"""
PNAD Continua - Pesquisa Nacional por Amostra de Domicilios

Dados coletados:
  ocup_*  - Pessoas ocupadas por posicao (agr 6320, var 4090, cls 11913)
  ocup_*  - Pessoas ocupadas por atividade (agr 6323, var 4090, cls 888)
  ocup_informal - Pessoas ocupadas em situacao de informalidade (agr 8501, var 4090, cls 1350)
  forca_* - Condicao na forca de trabalho (agr 6318, var 1641, cls 629)
  subutil_* - Tipo de medida de subutilizacao da forca de trabalho (agr 6438, var 1641, cls 604;
              so as 3 categorias primitivas novas, ver _SUBUTIL)
  massa_* - Massa de rendimento habitual (agr 6392, vars 6293/6288, sem classificacao)
  massa_efetiva_* - Massa de rendimento efetivamente recebido (agr 6393, vars 6295/6291, sem classificacao)
  rend_*  - Rendimento medio habitual por posicao (agr 6389, var 5932, cls 11913)
  rend_*  - Rendimento medio habitual por atividade (agr 6391, var 5932, cls 888)
  rend_habitual_*_todos_trabalhos - Rendimento medio habitual total, sem quebra (agr 6390, vars 5933/5929)
  rend_efetivo_* - Rendimento medio efetivo (agr 6387 vars 5935/5931, agr 6388 var 5934, sem classificacao)
  taxa_*, nivel_*, pct_* - Series de taxa/nivel/percentual sem classificacao, um agregado por
                           indicador (taxa_desocupacao, taxa_participacao, taxa_informalidade,
                           taxa_subutil_combinada_horas, taxa_subutil_combinada_potencial,
                           taxa_subutil_composta, taxa_subocupacao_horas, nivel_ocupacao,
                           nivel_desocupacao, pct_desalentados, pct_contribuintes_previdencia
                           - ver _SIMPLES)

Banco: macro_brasil.mt_pnad
Nota: nomes prefixados por tipo (ocup_, rend_, forca_, massa_, subutil_, taxa_, nivel_, pct_)
      para evitar colisao de chaves entre indicadores diferentes com mesma categoria.
"""

from datetime import datetime

import pandas as pd

from connectors.ibge import IBGE
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "mt_pnad"

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

# Situacao de informalidade (cls 1350) — agr 8501, var 4090 (mesma variavel de ocupados)
# So a categoria "Informais" (57303) — "Total" (57302) e redundante com o total ja
# coberto por forca_ocupado (agr 6318).
_INFORMAL_BASE = {
    "57303": "informal",
}

# Tipo de medida de subutilizacao da forca de trabalho (cls 604) — agr 6438, var 1641.
# So as 3 categorias primitivas novas: "Total" (31753) e "Desocupado" (31750) sao
# redundantes com forca_ocupado/forca_desocupado (agr 6318); as 4 categorias
# compostas (forca ampliada, forca ou desalentado, e as combinacoes com desocupado)
# sao somas derivaveis destas 3 e das ja existentes em _FORCA.
_SUBUTIL_BASE = {
    "31751": "subocupado_horas",
    "31752": "forca_potencial",
    "46254": "desalentado",
}

# --- Versoes com prefixo para o banco ----------------------------------------
# Prefixos separam o tipo de indicador e evitam conflito de chave primaria
# (ex.: ocup_industria_geral != rend_industria_geral)

_OCUP_POSICAO  = {k: f"ocup_{v}"  for k, v in _POSICAO_BASE.items()}
_OCUP_ATIVIDADE = {k: f"ocup_{v}" for k, v in _ATIVIDADE_BASE.items()}
_OCUP_INFORMAL = {k: f"ocup_{v}"  for k, v in _INFORMAL_BASE.items()}
_FORCA         = _FORCA_BASE          # nomes ja unicos (ocupado, desocupado, ...)
_SUBUTIL       = {k: f"subutil_{v}" for k, v in _SUBUTIL_BASE.items()}
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

# Rendimento habitual total, todos os trabalhos, sem quebra — agr 6390.
# Complementa rend_efetivo_*_todos_trabalhos (agr 6387), que ja existe.
_REND_HABITUAL_TOTAL = {
    "5933": "rend_habitual_real_todos_trabalhos",
    "5929": "rend_habitual_nominal_todos_trabalhos",
}

# Massa de rendimento efetivamente recebido, todos os trabalhos — agr 6393.
# Complementa massa_*_habitual (agr 6392), que ja existe.
_MASSA_EFETIVA = {
    "6295": "massa_efetiva_real",
    "6291": "massa_efetiva_nominal",
}

# Series "simples": um valor por agregado, sem classificacao.
# dict {nome: (agregado, variavel)}.
_SIMPLES = {
    "taxa_desocupacao":                 (6381, 4099),
    "taxa_participacao":                (5944, 4096),
    "taxa_informalidade":               (8513, 12466),
    "taxa_subutil_combinada_horas":     (6439, 4114),
    "taxa_subutil_combinada_potencial": (6440, 4116),
    "taxa_subutil_composta":            (6441, 4118),
    "taxa_subocupacao_horas":           (6785, 9819),
    "nivel_ocupacao":                   (6379, 4097),
    "nivel_desocupacao":                (6380, 4098),
    "pct_desalentados":                 (6807, 9869),
    "pct_contribuintes_previdencia":    (3919, 8463),
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


def _fetch_pares(agregado: int, variaveis_nomes: dict, periodos) -> pd.DataFrame:
    """Busca duas ou mais variaveis do mesmo agregado, sem classificacao.

    Uso tipico: pares real/nominal do mesmo indicador (ex.: massa habitual,
    rendimento habitual total, massa efetiva).

    Args:
        agregado:        ID do agregado IBGE.
        variaveis_nomes: dict {str(variavel_id): nome}.
        periodos:        qualquer formato aceito pelo connector IBGE.

    Returns:
        DataFrame com colunas: date, name, value.
    """
    df = _ibge.get(
        agregado=agregado,
        variaveis=[int(v) for v in variaveis_nomes],
        localidades={"N1": "all"},
        periodos=periodos,
    )
    df["name"] = df["variavel_id"].astype(str).map(variaveis_nomes)
    return df[["date", "name", "value"]]


def _fetch_simples(especificacoes: dict, periodos) -> pd.DataFrame:
    """Busca series de um valor por agregado, sem classificacao.

    Cada indicador vive em um agregado IBGE proprio (taxa de desocupacao,
    taxa de participacao, etc.) — nao da para combinar agregados diferentes
    numa unica chamada, entao itera um por um.

    Args:
        especificacoes: dict {nome: (agregado, variavel)}.
        periodos:        qualquer formato aceito pelo connector IBGE.

    Returns:
        DataFrame com colunas: date, name, value.
    """
    frames = []
    for nome, (agregado, variavel) in especificacoes.items():
        df = _ibge.get(
            agregado=agregado,
            variaveis=variavel,
            localidades={"N1": "all"},
            periodos=periodos,
        )
        df["name"] = nome
        frames.append(df[["date", "name", "value"]])
    return pd.concat(frames, ignore_index=True)


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
    """Atualiza macro_brasil.mt_pnad (ocupacao, forca de trabalho, subutilizacao,
    informalidade, rendimento, massa salarial e taxas/niveis agregados).

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
        _fetch_cls(8501, 4090,  1350, _OCUP_INFORMAL,  periodos),
        _fetch_cls(6318, 1641,   629, _FORCA,          periodos),
        _fetch_cls(6438, 1641,   604, _SUBUTIL,        periodos),
        _fetch_pares(6392, _MASSA,               periodos),
        _fetch_pares(6393, _MASSA_EFETIVA,       periodos),
        _fetch_cls(6389, 5932, 11913, _REND_POSICAO,   periodos),
        _fetch_cls(6391, 5932,   888, _REND_ATIVIDADE, periodos),
        _fetch_pares(6390, _REND_HABITUAL_TOTAL, periodos),
        _fetch_rend_efetivo(periodos),
        _fetch_simples(_SIMPLES, periodos),
    ]
    df = pd.concat(frames, ignore_index=True)
    df["region"] = "Brasil"
    insert_data_into_database(_DATABASE, _TABLE, df)