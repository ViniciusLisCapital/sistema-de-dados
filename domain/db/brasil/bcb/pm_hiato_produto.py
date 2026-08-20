"""
Hiato do produto estimado pelo BCB -- serie corrente (ultima edicao publicada
do Relatorio de Politica Monetaria).

Fonte: anexo estatistico do RI/RPM, aba do "Grafico 2.2.x - Hiato do produto"
(ver connectors/bcb_rpm.py e o parser compartilhado em `_rpm_hiato.py`).
NAO existe no SGS: o hiato e uma estimativa de modelo do proprio BCB, publicada
so dentro do relatorio.

Esta tabela responde "qual e o hiato hoje, na melhor estimativa disponivel".
A pergunta irma -- "o que o BCB achava do mesmo trimestre em cada edicao
passada" -- e de `pm_hiato_produto_vintages`, que guarda o painel completo.
As duas leem a mesma fonte com o mesmo parser; esta aqui e a fatia da edicao
mais recente, materializada a parte porque e o que um grafico de nivel quer
consumir sem precisar filtrar por MAX(vintage) toda vez.

## Variaveis

    central     estimativa central -- 'Hiato' ate a edicao 2024-06,
                'Cenario de referencia' de 2024-09 em diante
    minimo      \\
    p25          | dispersao da suite de modelos; so nas edicoes de 2024-09
    p75          | em diante
    maximo      /
    banda_sup   \\ banda de +-2 desvios-padrao do modelo unico; so nas
    banda_inf   / edicoes ate 2024-06

Como a tabela guarda uma edicao so, na pratica ela tem `central` + os quatro
percentis enquanto a edicao corrente for do regime "suite". A coluna `vintage`
registra de qual edicao cada linha veio.

## Escala

Percentual do produto potencial (%). Positivo = demanda acima do potencial.
Nao anualizar, nao acumular: e um nivel, ja em pontos percentuais.

## Historico

A serie comeca em 2003T4 (2003T2 em tres edicoes) e vai ate o trimestre de
referencia da edicao. Nada antes de 2003 -- e onde o proprio BCB comeca o
grafico.

## Banco

macro_brasil.pm_hiato_produto -- PRIMARY KEY (date, variavel).
~90 trimestres x 5 variaveis ~= 450 linhas.

`run()` TRUNCA antes de recarregar, diferente da tabela de vintages (que faz
upsert). O motivo e semantico: aqui a tabela E uma edicao, e edicoes trocam de
grade. A edicao 2025-03 publica desde 2003T2 e a 2025-06 desde 2003T4 -- num
upsert, 2003T2/T3 ficariam para tras como linha orfa da edicao anterior,
misturando duas edicoes na tabela que existe justamente para conter uma. Um
snapshot CSV vai para `_backups/` antes do truncate (ultimos 5 mantidos).
"""

from __future__ import annotations

import datetime as dt
import os

import pandas as pd

from connectors.bcb_rpm import AnexoRPM
from connectors.mysql import (
    backup_table_before_truncate,
    insert_data_into_database,
    truncate_table,
)
from domain.db.brasil.bcb import _rpm_hiato

_DATABASE = "macro_brasil"
_TABLE = "pm_hiato_produto"
_BACKUP_DIR = os.path.join(os.path.dirname(__file__), "_backups")


def run(vintage: str | dt.date | None = None) -> None:
    """Atualiza macro_brasil.pm_hiato_produto com a edicao mais recente.

    Args:
        vintage: edicao a carregar, "YYYY-MM" ou date. None (default) descobre
                 a mais recente publicada -- o comportamento de rotina. Passar
                 uma edicao antiga aqui deixa a tabela deliberadamente
                 desatualizada; para comparar edicoes use
                 `pm_hiato_produto_vintages`, nao esta tabela.
    """
    anexo = AnexoRPM()

    if vintage is None:
        alvo = anexo.vintage_mais_recente()
        if alvo is None:
            raise RuntimeError(
                "nenhuma edicao do anexo estatistico do RPM respondeu -- "
                "conferir connectors/bcb_rpm.py (o BCB pode ter mudado a URL)."
            )
    else:
        alvo = vintage if isinstance(vintage, dt.date) else pd.Timestamp(vintage).date().replace(day=1)

    df, aba = _rpm_hiato.parse(anexo, alvo)
    df["vintage"] = alvo

    print(
        f"{_TABLE}: edicao {alvo:%Y-%m} (aba '{aba}'), {len(df)} linhas, "
        f"{df['date'].min()} -> {df['date'].max()}, "
        f"variaveis={sorted(df['variavel'].unique())}."
    )

    backup_table_before_truncate(_DATABASE, _TABLE, _BACKUP_DIR)
    truncate_table(_DATABASE, _TABLE)
    insert_data_into_database(_DATABASE, _TABLE, df)
