"""
Novo CAGED -- saldo/admissões/desligamentos por setor de atividade (CNAE 2.0,
nível seção), direto do microdado não-identificado do FTP do PDET/MTE.

Complementa `mt_caged` (BCB SGS -- hoje só estoque, mal rotulado como saldo,
ver domain/db/brasil/bcb/mt_caged.py) com o dado que nenhum distribuidor
(BCB/IPEA) republica: saldo/admissões/desligamentos por setor, que só existe no
microdado bruto.

Rodar via `mt_caged_novo.run()` (orquestrador -- baixa cada release uma vez e
alimenta as 3 tabelas de corte no mesmo passe). O `run()` deste módulo existe
para atualizar só esta tabela, ao custo de baixar os mesmos arquivos de novo.

Banco: macro_brasil.mt_caged_setor -- PRIMARY KEY (date, categoria, metrica)
DDL:
  CREATE TABLE macro_brasil.mt_caged_setor (
      date      DATE          NOT NULL,
      categoria VARCHAR(60)   NOT NULL,
      metrica   VARCHAR(20)   NOT NULL,
      value     DECIMAL(12,0),
      PRIMARY KEY (date, categoria, metrica)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- VARCHAR(60): o slug mais longo (atividades_administrativas_servicos_complementares) tem 49 chars.

Disponível desde 2020-01 (início do Novo CAGED -- o CAGED antigo, pré-2020, usa
outro layout e fica fora de escopo deliberadamente, ver HANDOVER.md).
"""

import pandas as pd

from connectors.mysql import insert_data_into_database
from domain.db.brasil.mte._caged_core import processar, resolver_releases

_DATABASE = "macro_brasil"
TABLE = "mt_caged_setor"

# Seção CNAE 2.0 -> slug (tabela "seção" do layout_novo_caged.xlsx, confirmada ao vivo).
_SECAO = {
    "A": "agropecuaria",
    "B": "industria_extrativa",
    "C": "industria_transformacao",
    "D": "eletricidade_gas",
    "E": "agua_esgoto_residuos",
    "F": "construcao",
    "G": "comercio",
    "H": "transporte_armazenagem_correio",
    "I": "alojamento_alimentacao",
    "J": "informacao_comunicacao",
    "K": "atividades_financeiras_seguros",
    "L": "atividades_imobiliarias",
    "M": "atividades_profissionais_cientificas_tecnicas",
    "N": "atividades_administrativas_servicos_complementares",
    "O": "administracao_publica_defesa_seguridade_social",
    "P": "educacao",
    "Q": "saude_servicos_sociais",
    "R": "artes_cultura_esporte_recreacao",
    "S": "outras_atividades_servicos",
    "T": "servicos_domesticos",
    "U": "organismos_internacionais",
    "Z": "nao_identificado",
}


def categoria(df: pd.DataFrame) -> pd.Series:
    """Coluna de corte para este recorte (usada pelo orquestrador)."""
    return df["seção"].map(_SECAO).fillna("nao_identificado")


def run(n_meses: int = 6, start: str | None = None, end: str | None = None) -> None:
    """Atualiza só macro_brasil.mt_caged_setor.

    Args:
        n_meses: últimos N releases do FTP a reprocessar (default 6). Só as
                 competências dentro dessa janela são gravadas -- ver
                 _caged_core.py para por quê. Ignorado se start/end.
        start:   "AAAAMM" inicial, ou "all" para reconstrução completa desde 2020-01.
        end:     "AAAAMM" final (default: último release disponível no FTP).
    """
    releases = resolver_releases(n_meses, start, end)
    for _comp, resultado in processar(releases, {"setor": categoria}):
        insert_data_into_database(_DATABASE, TABLE, resultado["setor"])
