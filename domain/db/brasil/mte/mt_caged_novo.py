"""
Novo CAGED -- orquestrador das 3 tabelas de corte (setor/UF/faixa salarial).

Ponto de entrada preferido para atualizar o Novo CAGED: baixa cada release do
FTP do PDET/MTE UMA vez e alimenta as 3 tabelas no mesmo passe. Rodar os 3
scripts de corte separadamente funciona, mas baixaria os mesmos arquivos 3x
(o download do CAGEDMOV, ~50MB/mês comprimido, domina o custo -- ~4GB para a
reconstrução histórica completa vs. ~12GB se rodados separados).

Espaço em disco: nada persiste além da extração temporária de um mês por vez
(~450MB), apagada antes do próximo release -- padrão "agregar-e-descartar".

Tabelas alimentadas (ver o DDL na docstring de cada módulo de corte):
  macro_brasil.mt_caged_setor    -- por seção CNAE 2.0
  macro_brasil.mt_caged_uf       -- por UF
  macro_brasil.mt_caged_salario  -- por faixa de salário (múltiplos de SM)

Métricas em todas: saldo, admissoes, desligamentos. Ver _caged_core.py para a
fórmula MOV+FOR-EXC e por que atualizações incrementais só gravam as
competências dentro da janela de releases processada.
"""

from connectors.mysql import insert_data_into_database
from domain.db.brasil.mte import mt_caged_salario, mt_caged_setor, mt_caged_uf
from domain.db.brasil.mte._caged_core import processar, resolver_releases

_DATABASE = "macro_brasil"

_CORTES = {
    "setor": (mt_caged_setor.categoria, mt_caged_setor.TABLE),
    "uf": (mt_caged_uf.categoria, mt_caged_uf.TABLE),
    "salario": (mt_caged_salario.categoria, mt_caged_salario.TABLE),
}


def run(n_meses: int = 6, start: str | None = None, end: str | None = None) -> None:
    """Atualiza as 3 tabelas de corte do Novo CAGED num único passe de download.

    Args:
        n_meses: últimos N releases do FTP a reprocessar (default 6). Só as
                 competências dentro dessa janela são gravadas -- ver
                 _caged_core.py. Ignorado se start/end fornecidos.
        start:   "AAAAMM" inicial, ou "all" para reconstrução completa desde
                 2020-01 (~4GB de download, job longo).
        end:     "AAAAMM" final (default: último release disponível no FTP).
    """
    releases = resolver_releases(n_meses, start, end)
    print(f"Novo CAGED: processando {len(releases)} release(s) ({releases[0]}..{releases[-1]})")

    cortes = {nome: fn for nome, (fn, _) in _CORTES.items()}
    for _comp, resultado in processar(releases, cortes):
        for nome, (_, tabela) in _CORTES.items():
            insert_data_into_database(_DATABASE, tabela, resultado[nome])
