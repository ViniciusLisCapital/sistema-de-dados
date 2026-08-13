"""
Novo CAGED -- saldo/admissões/desligamentos por UF, direto do microdado
não-identificado do FTP do PDET/MTE. Ver mt_caged_setor.py (mesmo padrão) e
domain/db/brasil/mte/_caged_core.py para a lógica de combinação MOV+FOR-EXC.

Banco: macro_brasil.mt_caged_uf -- PRIMARY KEY (date, categoria, metrica)
DDL:
  CREATE TABLE macro_brasil.mt_caged_uf (
      date      DATE          NOT NULL,
      categoria VARCHAR(5)    NOT NULL,
      metrica   VARCHAR(20)   NOT NULL,
      value     DECIMAL(12,0),
      PRIMARY KEY (date, categoria, metrica)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

`categoria` = sigla de 2 letras da UF (IBGE), ou "NI" para "não identificado".
Disponível desde 2020-01 (Novo CAGED).
"""

from domain.db.brasil.mte._caged_core import agregar_por_corte, carregar_releases, resolver_releases
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE = "mt_caged_uf"

# Código IBGE -> sigla (tabela "uf" do layout_novo_caged.xlsx, confirmada ao vivo).
_UF = {
    11: "RO", 12: "AC", 13: "AM", 14: "RR", 15: "PA", 16: "AP", 17: "TO",
    21: "MA", 22: "PI", 23: "CE", 24: "RN", 25: "PB", 26: "PE", 27: "AL",
    28: "SE", 29: "BA",
    31: "MG", 32: "ES", 33: "RJ", 35: "SP",
    41: "PR", 42: "SC", 43: "RS",
    50: "MS", 51: "MT", 52: "GO", 53: "DF",
    99: "NI",
}


def run(n_meses: int = 6, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.mt_caged_uf.

    Args:
        n_meses: últimos N releases do FTP a reprocessar (default 6). Ver
                 docstring de mt_caged_setor.run() -- mesma semântica.
        start:   "AAAAMM" inicial, ou "all" para a série completa desde 2020-01.
        end:     "AAAAMM" final (default: último release disponível no FTP).
    """
    releases = resolver_releases(n_meses, start, end)
    bruto = carregar_releases(releases)
    bruto["categoria"] = bruto["uf"].map(_UF).fillna("NI")
    df = agregar_por_corte(bruto, "categoria")
    insert_data_into_database(_DATABASE, _TABLE, df)
