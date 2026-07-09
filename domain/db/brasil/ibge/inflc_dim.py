"""
Dimensao do IPCA por subitem: Grupo/Subgrupo/Item (classificacao BCB), marcacao
de nucleo "Subjacente" (Alimentos/Servicos/Bens Industriais Subjacente), e
flags de pertencimento aos nucleos por exclusao oficiais do BC (EX-0/EX-01/
EX-02/EX-03/EX-FE + os dois subcomponentes do EX-03).

Schema macro_brasil.inflc_dim:
  PRIMARY KEY (subitem)
  Colunas: subitem VARCHAR(120) | grupo VARCHAR(60) | subgrupo VARCHAR(80) |
           item VARCHAR(150) | subjacente VARCHAR(60) |
           nucleo_ex0 TINYINT(1) | nucleo_ex01 TINYINT(1) |
           nucleo_ex02 TINYINT(1) | nucleo_ex03 TINYINT(1) |
           nucleo_ex03_servicos TINYINT(1) | nucleo_ex03_industriais TINYINT(1) |
           nucleo_exfe TINYINT(1)

DDL:
  DROP TABLE IF EXISTS macro_brasil.inflc_dim;
  CREATE TABLE macro_brasil.inflc_dim (
      subitem                 VARCHAR(120)  NOT NULL,
      grupo                   VARCHAR(60),
      subgrupo                VARCHAR(80),
      item                    VARCHAR(150),
      subjacente              VARCHAR(60),
      nucleo_ex0              TINYINT(1),
      nucleo_ex01             TINYINT(1),
      nucleo_ex02             TINYINT(1),
      nucleo_ex03             TINYINT(1),
      nucleo_ex03_servicos    TINYINT(1),
      nucleo_ex03_industriais TINYINT(1),
      nucleo_exfe             TINYINT(1),
      PRIMARY KEY (subitem)
  );

Duas fontes, duas naturezas distintas:
  - grupo/subgrupo/item: mapeamento mantido manualmente em
    analytics/inflation/data/tabela_dimensao_ipca.xlsx (sheet
    dimensao_bcb_2020). Este script sincroniza o xlsx para o banco; a fonte
    de verdade continua sendo o Excel.
  - nucleo_*: derivados de analytics/inflation/data/Vetores_NT_57.xlsx (sheet
    "jan20-presente"), arquivo de apoio da Nota Tecnica do Banco Central do
    Brasil no 57 (dez/2025) que lista o vetor de agregacao oficial (0/1) de
    cada nucleo por exclusao, por componente do IPCA em todos os niveis
    hierarquicos. Como a inclusao e marcada sempre no nivel hierarquico mais
    alto possivel (NT-57 Subsecao 2.1.2), _rollup_nucleo_flags() propaga o
    flag de cada nucleo do indice geral/grupo/subgrupo/item ate os subitens
    descendentes antes de gravar no banco — ver essa funcao para o algoritmo.
    Fonte 100% oficial, superior em precisao a qualquer classificacao manual.
  - subjacente: HIBRIDO desde 2026-07. Servicos Subjacente/Bens Industriais
    Subjacente agora SEGUEM nucleo_ex03_servicos/nucleo_ex03_industriais
    (oficial) em vez do xlsx manual — a comparacao entre as duas fontes
    revelou ~19 dos 377 subitens divergentes (a maioria bens industriais que
    a planilha manual nunca marcou, ex: madeira e taco, sabao liquido, papel
    toalha, bermuda/short, mochila, oculos de grau, livro didatico; mais 1
    caso inverso, "conselho de classe", marcado Servicos Subjacente na
    planilha mas fora do EX-03 Servicos no vetor oficial). Por instrucao
    explicita do usuario ("You should follow the official dimension"), o
    vetor oficial agora tem precedencia — ver _apply_official_subjacente().
    "Alimentos Subjacente" continua vindo do xlsx manual sem alteracao: o
    vetor da NT-57 nao tem uma coluna equivalente para o nucleo de
    alimentacao do EX2 (so publica Servicos/Industriais como series
    separadas — EX3 Servicos/Industriais, SGS 29683/29684), entao nao ha
    fonte oficial para reconciliar essa parte. Confirmado sem sobreposicao
    entre os 34 subitens "Alimentos Subjacente" e os flags oficiais de
    servicos/industriais antes de aplicar essa regra.

Compartilhado entre IPCA e IPCA-15 (IPCA-15 usa um subconjunto dos subitens
do IPCA — todo subitem do IPCA-15 tambem existe no IPCA).

Uso:
    uv run python -c "from domain.db.brasil.ibge.inflc_dim import run; run()"
"""

from pathlib import Path

import pandas as pd

from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE = "inflc_dim"
_DATA_DIR = Path(__file__).resolve().parents[4] / "analytics" / "inflation" / "data"
_XLSX = _DATA_DIR / "tabela_dimensao_ipca.xlsx"
_VETORES_XLSX = _DATA_DIR / "Vetores_NT_57.xlsx"

_VETOR_COLS = {
    "Núcleo EX-FE": "nucleo_exfe",
    "Núcleo EX0": "nucleo_ex0",
    "Núcleo EX1": "nucleo_ex01",
    "Núcleo EX2": "nucleo_ex02",
    "Núcleo EX3": "nucleo_ex03",
    "EX3 Serviços": "nucleo_ex03_servicos",
    "EX3 Industriais": "nucleo_ex03_industriais",
}


def _rollup_nucleo_flags() -> pd.DataFrame:
    """Deriva flags de pertencimento aos nucleos por exclusao, por subitem.

    Le o vetor de agregacao oficial (Vetores_NT_57.xlsx, sheet
    jan20-presente — mesma estrutura do IPCA vigente desde jan/2020, que e
    tambem o periodo coberto por inflc_decomposicao). Cada linha do arquivo
    e um componente do IPCA (indice geral, grupo, subgrupo, item ou
    subitem), com um 0/1 por nucleo. Por convencao da NT-57 (Subsecao
    2.1.2), a inclusao e marcada apenas no nivel hierarquico mais alto
    possivel — ou seja, um subitem pertence a um nucleo se ele proprio OU
    qualquer um dos seus ancestrais (item de 4 digitos, subgrupo de 2,
    grupo de 1, indice geral) tiver o flag ligado nessa coluna.
    """
    vet = pd.read_excel(_VETORES_XLSX, sheet_name="jan20-presente")
    name_col = vet.columns[0]
    vet["code"] = vet[name_col].astype(str).str.extract(r"^(\d+)\.")
    by_code = vet.set_index("code")

    def ancestors(code: str) -> list[str]:
        levels = ["0", code[:1], code[:2], code[:4]]
        return [lv for lv in levels if lv in by_code.index]

    subitens = vet[vet["code"].str.len() == 7].copy()
    for src_col, dst_col in _VETOR_COLS.items():
        subitens[dst_col] = subitens["code"].apply(
            lambda code, col=src_col: int(
                any(by_code.loc[a, col] == 1 for a in ancestors(code))
                or by_code.loc[code, col] == 1
            )
        )
    return subitens[["code"] + list(_VETOR_COLS.values())]


def _apply_official_subjacente(dim: pd.DataFrame) -> pd.DataFrame:
    """Faz nucleo_ex03_servicos/industriais (oficial) prevalecer sobre a
    marcacao manual de Servicos/Bens Industriais Subjacente.

    "Alimentos Subjacente" nao tem equivalente no vetor oficial (a NT-57 nao
    publica uma serie/coluna separada para o nucleo de alimentacao do EX2),
    entao essa marcacao continua vindo do xlsx manual sem alteracao.
    """
    dim = dim.copy()
    is_servicos = dim["nucleo_ex03_servicos"] == 1
    is_industriais = dim["nucleo_ex03_industriais"] == 1
    is_alimentos = dim["subjacente"] == "Alimentos Subjacente"

    dim["subjacente"] = None
    dim.loc[is_alimentos, "subjacente"] = "Alimentos Subjacente"
    dim.loc[is_servicos, "subjacente"] = "Serviços Subjacente"
    dim.loc[is_industriais, "subjacente"] = "Bens Industriais Subjacente"
    return dim


def run() -> None:
    """Sincroniza macro_brasil.inflc_dim a partir dos xlsx desta pasta."""
    dim = pd.read_excel(_XLSX, sheet_name="dimensao_bcb_2020")
    dim = dim.rename(columns={
        "Subitem": "subitem", "Grupo": "grupo", "Subgrupo": "subgrupo",
        "Item": "item", "Subjacente": "subjacente",
    })
    dim = dim[["subitem", "grupo", "subgrupo", "item", "subjacente"]]

    dim["code"] = dim["subitem"].astype(str).str.extract(r"^(\d{7})")
    nucleo_flags = _rollup_nucleo_flags()
    dim = dim.merge(nucleo_flags, on="code", how="left").drop(columns="code")
    dim = _apply_official_subjacente(dim)

    dim = dim.astype(object).where(pd.notna(dim), None)
    insert_data_into_database(_DATABASE, _TABLE, dim)
