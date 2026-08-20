"""
Hiato do produto do BCB -- painel de VINTAGES: o que cada edicao do relatorio
publicou para cada trimestre.

Fonte: anexo estatistico do RI/RPM (ver connectors/bcb_rpm.py e o parser
compartilhado em `_rpm_hiato.py`, que documenta as cinco armadilhas da aba).

## Por que uma tabela so para isto

O hiato nao e medido, e estimado por um filtro de duas pontas -- entao cada
edicao reescreve o passado recente. `pm_hiato_produto` guarda a estimativa de
hoje; esta guarda todas as estimativas ja publicadas, uma linha por
(edicao, trimestre, variavel). E o que permite perguntar "quando o BCB percebeu
que a economia estava acima do potencial?", que a serie corrente sozinha nao
responde -- ela ja nasce revisada.

O que os dados mostram (medido na carga de 2026-08, 20 edicoes): entre edicoes
consecutivas a revisao media e de ~0,01 p.p. em todo o historico, mas se
concentra nos ultimos 6-8 trimestres de cada edicao. Todo trimestre de 2022T4 a
2024T1 foi publicado primeiro como hiato NEGATIVO e hoje esta positivo -- 2023T1
saiu de -1,30 para +0,33 ao longo de 14 edicoes. Doze dos 86 trimestres com pelo
menos 6 edicoes ja trocaram de sinal.

**Nem toda revisao e revisao de dado.** As passagens 2024-03 -> 2024-06
(+0,096 p.p. de media, maximo 0,77) e 2024-06 -> 2024-09 (+0,088, maximo 0,51)
sao as duas unicas fora do padrao e coincidem com mudanca de metodologia: a
edicao 2024-06 traz o boxe "Medidas de hiato do produto no Brasil" e a 2024-09
troca a apresentacao de "um modelo + banda" para "suite de modelos". Quem for
graficar revisao ao longo do tempo tem que marcar essa quebra, senao atribui a
leitura de conjuntura o que foi troca de modelo.

## Regimes

    ate 2024-06   central + banda_sup/banda_inf  (um modelo, banda +-2 d.p.)
    de 2024-09    central + minimo/p25/p75/maximo (dispersao entre modelos)

Nao ha coluna `regime`: ele e exatamente "esta edicao tem `minimo`?". A serie
comparavel entre todas as edicoes e `central` -- as bandas do regime antigo e a
dispersao do novo medem coisas diferentes (incerteza de um modelo vs. desacordo
entre modelos) e NAO devem ser plotadas como a mesma faixa.

## Cobertura

20 edicoes na carga inicial, 2021-09 -> 2026-06, ~6.300 linhas. O anexo
estatistico nao existe antes de 2021-09 (ver connectors/bcb_rpm.py), entao para
2003-2021 ha apenas a leitura corrente, ja revisada -- o painel de vintages so
tem sentido do fim de 2021 para frente.

## Banco

macro_brasil.pm_hiato_produto_vintages -- PRIMARY KEY (vintage, date, variavel).

`run()` faz upsert e, por default, so baixa as edicoes que ainda nao estao no
banco: uma edicao publicada nao muda mais, entao rebaixar as 20 a cada rotina
seria ~15MB de download para reescrever linhas identicas. `full=True` reprocessa
tudo -- usar quando o parser mudar, ou se houver suspeita de que o BCB
republicou um arquivo corrigido.
"""

from __future__ import annotations

import datetime as dt

import pandas as pd

from connectors.bcb_rpm import AnexoRPM
from connectors.mysql import MySQLDataRequester, insert_data_into_database
from domain.db.brasil.bcb import _rpm_hiato

_DATABASE = "macro_brasil"
_TABLE = "pm_hiato_produto_vintages"


def _vintages_no_banco() -> set[dt.date]:
    """Edicoes ja carregadas. Set vazio se a tabela nao existir/estiver vazia."""
    req = MySQLDataRequester(_DATABASE, _TABLE)
    req.connect()
    try:
        df = req.request_data()
    finally:
        req.close_connection()
    if df is None or df.empty:
        return set()
    return set(pd.to_datetime(df["vintage"]).dt.date)


def run(full: bool = False, desde: str | None = None) -> None:
    """Atualiza macro_brasil.pm_hiato_produto_vintages.

    Args:
        full: True reprocessa todas as edicoes disponiveis (~20 downloads,
              ~15MB). False (default) baixa so as que faltam no banco.
        desde: limita a varredura a edicoes a partir de "YYYY-MM". None
               (default) comeca em 2021-09, a primeira edicao com anexo.
    """
    anexo = AnexoRPM()
    inicio = pd.Timestamp(desde).date().replace(day=1) if desde else None
    janela = {"desde": inicio} if inicio else {}

    # As edicoes ja carregadas nao precisam ser confirmadas na rede -- so as que
    # faltam. Numa rotina em dia isso e 1 requisicao em vez de ~20; um buraco no
    # meio da serie continua sendo testado, porque ele nao esta em `ja_tem`.
    ja_tem = set() if full else _vintages_no_banco()
    disponiveis = anexo.vintages_disponiveis(ignorar=ja_tem, **janela)
    if not disponiveis:
        raise RuntimeError(
            "nenhuma edicao do anexo estatistico do RPM respondeu -- "
            "conferir connectors/bcb_rpm.py (o BCB pode ter mudado a URL)."
        )

    if full:
        alvos = disponiveis
    else:
        alvos = [v for v in disponiveis if v not in ja_tem]
        if not alvos:
            print(
                f"{_TABLE}: nada a fazer -- as {len(disponiveis)} edicoes disponiveis "
                f"(ate {disponiveis[-1]:%Y-%m}) ja estao no banco. Use full=True para reprocessar."
            )
            return

    print(f"{_TABLE}: processando {len(alvos)} edicao(oes) de {len(disponiveis)} disponivel(is).")

    frames = []
    for vintage in alvos:
        df, aba = _rpm_hiato.parse(anexo, vintage)
        df["vintage"] = vintage
        frames.append(df)
        print(
            f"  {vintage:%Y-%m}  aba '{aba}'  {len(df):>4d} linhas  "
            f"{df['date'].min()} -> {df['date'].max()}  "
            f"{'suite' if 'minimo' in set(df['variavel']) else 'banda'}"
        )

    todos = pd.concat(frames, ignore_index=True)
    todos = todos[["vintage", "date", "variavel", "value"]]

    print(
        f"{_TABLE}: {len(todos)} linhas, {todos['vintage'].nunique()} edicoes, "
        f"{todos['date'].min()} -> {todos['date'].max()}."
    )
    insert_data_into_database(_DATABASE, _TABLE, todos)
