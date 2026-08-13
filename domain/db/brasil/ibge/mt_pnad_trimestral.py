"""
PNAD Continua trimestral - Pesquisa Nacional por Amostra de Domicilios (pesquisa DD)

Complementa mt_pnad.py (que cobre a PNAD Continua mensal/trimestre movel, pesquisa BB)
com os cortes demograficos e ocupacionais que a mensal nao tem: sexo, grupo de idade,
nivel de instrucao, cor ou raca, posicao na ocupacao, atividade e grupamento ocupacional.
Cadencia trimestral "cheia" (nao trimestre movel) — por isso e uma tabela separada,
nao mais linhas em mt_pnad (mesmo raciocinio que ja separa inflc_decomposicao de
inflc_decomposicao_item: mesma pesquisa, granularidade diferente).

Primeira rodada (2026-08): so nivel Brasil (N1). Nivel UF (N3), suportado pela API para
quase todos os agregados abaixo, ficou de fora deliberadamente para nao multiplicar o
volume por ~27x nesta primeira passada — ver domain/db/CLAUDE.md.

Convencao: em cada agregado "rico" (condicao/taxas, subutilizacao, rendimento, massa,
populacao, horas), a categoria "Total" de cada classificacao e sempre excluida — ja
coberta nacionalmente sem quebra pelas series equivalentes de mt_pnad.

Dados coletados (nome = variavel_base + "_" + dimensao + "_" + categoria):
  taxa_participacao_*, nivel_ocupacao_*, nivel_desocupacao_*, taxa_desocupacao_*,
    taxa_informalidade_* - por sexo (agr 4093), idade (4094), instrucao (4095), raca (6402)
  taxa_subutil_combinada_horas_*, taxa_subutil_combinada_potencial_*, taxa_subutil_composta_*
    - por sexo (agr 6396), idade (6397)
  rend_habitual_trabalho_principal_*, rend_habitual_todos_trabalhos_*,
    rend_efetivo_trabalho_principal_*, rend_efetivo_todos_trabalhos_*
    - por sexo (5436), idade (5437), instrucao (5438), raca (6405)
  rend_habitual_trabalho_principal_*, rend_efetivo_trabalho_principal_*
    - por posicao (5439), atividade (5442), ocupacao (5444)
  massa_habitual, massa_efetiva - sem quebra (agr 5606)
  massa_habitual_posicao_*, massa_efetiva_posicao_* - por posicao (agr 6421)
  populacao_* - por sexo (5917), idade (5918), instrucao (5919), raca (6403)
  horas_habitual_trabalho_principal_*, horas_efetivo_trabalho_principal_*,
    horas_habitual_todos_trabalhos_*, horas_efetivo_todos_trabalhos_*
    - por sexo (6371), idade (6372), instrucao (6373), raca (6406)
  horas_habitual_trabalho_principal_*, horas_efetivo_trabalho_principal_*
    - por posicao (agr 6374)

Fora de escopo nesta rodada (ver domain/db/CLAUDE.md "Pendencias"):
  - Nivel UF (N3) para qualquer indicador acima.
  - Agr 5440 (rendimento por posicao+categoria do emprego detalhada) - redundante/mais
    confuso que 5439 (posicao simples), que ja cobre a distincao principal.
  - Agr 5947 (contribuicao previdencia) - sem quebra demografica nesta pesquisa, e a
    taxa nacional ja existe em mt_pnad (pct_contribuintes_previdencia).
  - Agregados "espelho" (6459-8529): mesma informacao dos agregados acima, so que
    formatados com colunas de variacao trimestral em vez de distribuicao percentual —
    seriam dados duplicados sob outro layout, nao trazem indicador novo.
  - Agregados de nicho (militares/setor publico por area, domesticos por numero de
    domicilios, tipo de contratacao, tempo de permanencia, numero de trabalhos).

Banco: macro_brasil.mt_pnad_trimestral
"""

from datetime import datetime

import pandas as pd

from connectors.ibge import IBGE
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "mt_pnad_trimestral"

# --- Dimensoes (categoria -> sufixo), "Total" sempre excluido ---------------

_DIM_SEXO = {"4": "homens", "5": "mulheres"}                              # cls 2

_DIM_IDADE = {                                                            # cls 58
    "114535": "14_17", "100052": "18_24", "108875": "25_39",
    "99127": "40_59", "3302": "60_mais",
}

_DIM_INSTRUCAO = {                                                        # cls 1568
    "120706": "sem_instrucao", "11779": "fund_incompleto",
    "11628": "fund_completo", "11629": "medio_incompleto",
    "11630": "medio_completo", "11631": "superior_incompleto",
    "11632": "superior_completo", "11626": "nao_determinado",
}

_DIM_RACA = {"2776": "branca", "2777": "preta", "2779": "parda"}          # cls 86

_DIM_POSICAO_SIMPLES = {                                                  # cls 12029 (agr 5439, 6421)
    "99163": "empregado", "99358": "empregador", "99357": "conta_propria",
}

_DIM_POSICAO_HORAS = {                                                    # cls 2399 (agr 6374)
    "35423": "empregado", "35426": "empregador",
    "98272": "conta_propria", "40089": "familiar_auxiliar",
}

_DIM_ATIVIDADE = {                                                        # cls 888 (agr 5442)
    "47947": "agropecuaria", "47948": "industria_geral",
    "60031": "industria_transformacao", "47949": "construcao",
    "47950": "comercio_rep_veiculo", "56622": "transporte_armazenagem_correio",
    "56623": "alojamento_alimentacao", "56624": "inform_comun_financ_imob_prof_adm",
    "60032": "admpub_educ_saude_segsoc", "56627": "outros_servicos",
    "56628": "servicos_domesticos", "60033": "atividades_mal_definidas",
}

_DIM_OCUPACAO = {                                                         # cls 694 (agr 5444)
    "33370": "diretores_gerentes", "33371": "profissionais_ciencias",
    "33372": "tecnicos_nivel_medio", "33373": "apoio_administrativo",
    "33374": "servicos_vendedores", "33375": "agropecuaria_qualificados",
    "33376": "construcao_qualificados", "33377": "operadores_maquinas",
    "33378": "ocupacoes_elementares", "33379": "forcas_armadas",
    "33380": "ocupacoes_mal_definidas",
}

# --- Variaveis por padrao de agregado ---------------------------------------

_VARS_CONDICAO_TAXAS = {          # agr 4093/4094/4095/6402
    "4096": "taxa_participacao",
    "4097": "nivel_ocupacao",
    "4098": "nivel_desocupacao",
    "4099": "taxa_desocupacao",
    "12466": "taxa_informalidade",
}

_VARS_SUBUTIL_TAXAS = {           # agr 6396/6397
    "4114": "taxa_subutil_combinada_horas",
    "4116": "taxa_subutil_combinada_potencial",
    "4118": "taxa_subutil_composta",
}

_VARS_REND_4 = {                  # agr 5436/5437/5438/6405
    "5932": "rend_habitual_trabalho_principal",
    "5933": "rend_habitual_todos_trabalhos",
    "5934": "rend_efetivo_trabalho_principal",
    "5935": "rend_efetivo_todos_trabalhos",
}

_VARS_REND_2 = {                  # agr 5439/5442/5444
    "5932": "rend_habitual_trabalho_principal",
    "5934": "rend_efetivo_trabalho_principal",
}

_VARS_MASSA_5606 = {"6293": "massa_habitual", "6295": "massa_efetiva"}
_VARS_MASSA_6421 = {"8745": "massa_habitual", "8747": "massa_efetiva"}

_VARS_POPULACAO = {"606": "populacao"}    # agr 5917/5918/5919/6403

_VARS_HORAS_4 = {                 # agr 6371/6372/6373/6406
    "8186": "horas_habitual_trabalho_principal",
    "8188": "horas_efetivo_trabalho_principal",
    "8190": "horas_habitual_todos_trabalhos",
    "8192": "horas_efetivo_todos_trabalhos",
}

_VARS_HORAS_2 = {                 # agr 6374
    "8186": "horas_habitual_trabalho_principal",
    "8188": "horas_efetivo_trabalho_principal",
}

# -----------------------------------------------------------------------------

_ibge = IBGE()


def _fetch_cls_dim(agregado: int, variaveis_nomes: dict, cls_id: int,
                    cat_ids: dict, dim_sufixo: str, periodos) -> pd.DataFrame:
    """Busca N variaveis de um agregado, cruzadas por uma classificacao (dimensao
    demografica/ocupacional).

    Args:
        agregado:        ID do agregado IBGE.
        variaveis_nomes: dict {str(variavel_id): nome_base}.
        cls_id:          ID da classificacao.
        cat_ids:         dict {str(cat_id): sufixo_categoria} — categorias a coletar
                          (a categoria "Total" da classificacao nunca entra aqui).
        dim_sufixo:      nome curto da dimensao (ex.: "sexo", "idade", "posicao").
        periodos:        qualquer formato aceito pelo connector IBGE.

    Returns:
        DataFrame com colunas: date, name, value.
        name = f"{nome_base}_{dim_sufixo}_{sufixo_categoria}"
    """
    df = _ibge.get(
        agregado=agregado,
        variaveis=[int(v) for v in variaveis_nomes],
        classificacoes={cls_id: [int(k) for k in cat_ids]},
        localidades={"N1": "all"},
        periodos=periodos,
    )
    var_nome = df["variavel_id"].astype(str).map(variaveis_nomes)
    cat_nome = df["class_1_id"].map(cat_ids)
    df["name"] = var_nome + "_" + dim_sufixo + "_" + cat_nome
    return df[["date", "name", "value"]]


def _fetch_pares(agregado: int, variaveis_nomes: dict, periodos) -> pd.DataFrame:
    """Busca duas ou mais variaveis do mesmo agregado, sem classificacao.

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


def run(years_back: int = 2, periodos=None) -> None:
    """Atualiza macro_brasil.mt_pnad_trimestral (cortes demograficos/ocupacionais
    da PNAD Continua trimestral).

    Args:
        years_back: anos anteriores ao ano atual (default 2).
                    Ignorado se periodos for fornecido.
        periodos:   qualquer formato aceito pelo connector IBGE:
                      "202001-202412"  range explicito
                      (2020, 2024)     tupla de anos
                      "last:8"         ultimos N periodos (trimestres)
                      "all"            serie historica completa
    """
    if periodos is None:
        ano_fim  = datetime.now().year
        periodos = (ano_fim - years_back, ano_fim)

    frames = [
        # Condicao na forca de trabalho + taxas/niveis + informalidade, por dimensao
        _fetch_cls_dim(4093, _VARS_CONDICAO_TAXAS, 2,    _DIM_SEXO,      "sexo",      periodos),
        _fetch_cls_dim(4094, _VARS_CONDICAO_TAXAS, 58,   _DIM_IDADE,     "idade",     periodos),
        _fetch_cls_dim(4095, _VARS_CONDICAO_TAXAS, 1568, _DIM_INSTRUCAO, "instrucao", periodos),
        _fetch_cls_dim(6402, _VARS_CONDICAO_TAXAS, 86,   _DIM_RACA,      "raca",      periodos),
        # Subutilizacao da forca de trabalho, por dimensao
        _fetch_cls_dim(6396, _VARS_SUBUTIL_TAXAS, 2,  _DIM_SEXO,  "sexo",  periodos),
        _fetch_cls_dim(6397, _VARS_SUBUTIL_TAXAS, 58, _DIM_IDADE, "idade", periodos),
        # Rendimento (habitual/efetivo, trabalho principal/todos), por dimensao demografica
        _fetch_cls_dim(5436, _VARS_REND_4, 2,    _DIM_SEXO,      "sexo",      periodos),
        _fetch_cls_dim(5437, _VARS_REND_4, 58,   _DIM_IDADE,     "idade",     periodos),
        _fetch_cls_dim(5438, _VARS_REND_4, 1568, _DIM_INSTRUCAO, "instrucao", periodos),
        _fetch_cls_dim(6405, _VARS_REND_4, 86,   _DIM_RACA,      "raca",      periodos),
        # Rendimento (habitual/efetivo, trabalho principal), por posicao/atividade/ocupacao
        _fetch_cls_dim(5439, _VARS_REND_2, 12029, _DIM_POSICAO_SIMPLES, "posicao",   periodos),
        _fetch_cls_dim(5442, _VARS_REND_2, 888,   _DIM_ATIVIDADE,       "atividade", periodos),
        _fetch_cls_dim(5444, _VARS_REND_2, 694,   _DIM_OCUPACAO,        "ocupacao",  periodos),
        # Massa de rendimento
        _fetch_pares(5606, _VARS_MASSA_5606, periodos),
        _fetch_cls_dim(6421, _VARS_MASSA_6421, 12029, _DIM_POSICAO_SIMPLES, "posicao", periodos),
        # Populacao, por dimensao demografica
        _fetch_cls_dim(5917, _VARS_POPULACAO, 2,    _DIM_SEXO,      "sexo",      periodos),
        _fetch_cls_dim(5918, _VARS_POPULACAO, 58,   _DIM_IDADE,     "idade",     periodos),
        _fetch_cls_dim(5919, _VARS_POPULACAO, 1568, _DIM_INSTRUCAO, "instrucao", periodos),
        _fetch_cls_dim(6403, _VARS_POPULACAO, 86,   _DIM_RACA,      "raca",      periodos),
        # Horas trabalhadas (habitual/efetivo, trabalho principal/todos), por dimensao demografica
        _fetch_cls_dim(6371, _VARS_HORAS_4, 2,    _DIM_SEXO,      "sexo",      periodos),
        _fetch_cls_dim(6372, _VARS_HORAS_4, 58,   _DIM_IDADE,     "idade",     periodos),
        _fetch_cls_dim(6373, _VARS_HORAS_4, 1568, _DIM_INSTRUCAO, "instrucao", periodos),
        _fetch_cls_dim(6406, _VARS_HORAS_4, 86,   _DIM_RACA,      "raca",      periodos),
        # Horas trabalhadas (habitual/efetivo, trabalho principal), por posicao
        _fetch_cls_dim(6374, _VARS_HORAS_2, 2399, _DIM_POSICAO_HORAS, "posicao", periodos),
    ]
    df = pd.concat(frames, ignore_index=True)
    df["region"] = "Brasil"
    insert_data_into_database(_DATABASE, _TABLE, df)
