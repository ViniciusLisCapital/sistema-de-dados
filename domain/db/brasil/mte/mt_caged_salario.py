"""
Novo CAGED -- saldo/admissões/desligamentos por faixa de salário (em múltiplos
do salário mínimo vigente na competência), direto do microdado não-
identificado do FTP do PDET/MTE. Ver mt_caged_setor.py (mesmo padrão) e
domain/db/brasil/mte/_caged_core.py para a lógica de combinação MOV+FOR-EXC.

Faixas em múltiplos de SM (não em R$ nominal) -- é a classificação padrão
usada nas publicações agregadas oficiais do CAGED, porque bandas em R$
nominal perdem sentido com o tempo (a inflação salarial desloca a
distribuição). Usa o campo `salário` (salário mensal declarado, já em termos
mensais -- não `valorsalariofixo`+`unidadesaláriocódigo`, que seria a parte
fixa da remuneração numa unidade que pode não ser mensal).

`_SALARIO_MINIMO`: tabela histórica pesquisada ao vivo (2026-08) --
ver fontes no HANDOVER.md/git blame desta sessão. Precisa de manutenção
manual a cada reajuste anual (~janeiro, às vezes com um valor intermediário
como 2023, que teve dois reajustes no mesmo ano).

Banco: macro_brasil.mt_caged_salario -- PRIMARY KEY (date, categoria, metrica)
DDL:
  CREATE TABLE macro_brasil.mt_caged_salario (
      date      DATE          NOT NULL,
      categoria VARCHAR(20)   NOT NULL,
      metrica   VARCHAR(20)   NOT NULL,
      value     DECIMAL(12,0),
      PRIMARY KEY (date, categoria, metrica)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

Disponível desde 2020-01 (Novo CAGED).
"""

import numpy as np
import pandas as pd

from domain.db.brasil.mte._caged_core import agregar_por_corte, carregar_releases, resolver_releases
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE = "mt_caged_salario"

# (AAAAMM de início de vigência, valor em R$) -- ordenado, forward-fill até o próximo ponto.
_SALARIO_MINIMO = [
    ("202001", 1039.00),
    ("202002", 1045.00),
    ("202101", 1100.00),
    ("202201", 1212.00),
    ("202301", 1302.00),
    ("202305", 1320.00),
    ("202401", 1412.00),
    ("202501", 1518.00),
    ("202601", 1621.00),
]

_BANDAS = [
    "nao_identificado", "at_1sm", "de_1_a_1_5sm", "de_1_5_a_2sm", "de_2_a_3sm",
    "de_3_a_5sm", "de_5_a_7sm", "de_7_a_10sm", "de_10_a_15sm", "de_15_a_20sm",
    "mais_de_20sm",
]
_BINS = [-np.inf, 0, 1, 1.5, 2, 3, 5, 7, 10, 15, 20, np.inf]


def _sm_por_competencia(competencias: pd.Series) -> pd.Series:
    pontos = pd.DataFrame(_SALARIO_MINIMO, columns=["competencia", "sm"])
    tabela = pd.Series(index=competencias.astype(str).unique(), dtype="float64").sort_index()
    for comp in tabela.index:
        vigente = pontos.loc[pontos["competencia"] <= comp, "sm"]
        tabela[comp] = vigente.iloc[-1] if len(vigente) else pontos["sm"].iloc[0]
    return competencias.astype(str).map(tabela)


def run(n_meses: int = 6, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.mt_caged_salario.

    Args:
        n_meses: últimos N releases do FTP a reprocessar (default 6). Ver
                 docstring de mt_caged_setor.run() -- mesma semântica.
        start:   "AAAAMM" inicial, ou "all" para a série completa desde 2020-01.
        end:     "AAAAMM" final (default: último release disponível no FTP).
    """
    releases = resolver_releases(n_meses, start, end)
    bruto = carregar_releases(releases)

    sm = _sm_por_competencia(bruto["competênciamov"])
    multiplo = bruto["salário"] / sm
    bruto["categoria"] = pd.cut(multiplo, bins=_BINS, labels=_BANDAS, right=True).astype(str)
    bruto.loc[bruto["salário"] <= 0, "categoria"] = "nao_identificado"

    df = agregar_por_corte(bruto, "categoria")
    insert_data_into_database(_DATABASE, _TABLE, df)
