"""
Taxa de desocupacao retropolada do BCB -- edicao corrente do anexo estatistico
do Relatorio de Politica Monetaria (RPM).

Fonte: anexo estatistico do RI/RPM, aba do "Grafico 1.2.x - Taxa de desocupacao"
(ver connectors/bcb_rpm.py). NAO existe no SGS: o trecho anterior a PNAD Continua
e uma ESTIMATIVA do proprio BCB, retropolada segundo Alves, S. A. L. e Fasolo,
A. M., "Not Just Another Mixed Frequency Paper", BCB Working Paper 400 (2015).
A nota de rodape da propria aba diz isso.

## Por que existe, se o projeto ja tem `mt_pnad`

Porque as duas cobrem periodos diferentes e nao sao a mesma medida:

    mt_pnad.taxa_desocupacao   IBGE, trimestre movel, SEM ajuste sazonal,
                               comeca em 2012-03
    esta tabela                BCB, MM3M, COM ajuste sazonal ("a.s."),
                               comeca em 2004-04

E a serie que o BCB usa na equacao de emprego do modelo agregado, entao a amostra
de estimacao (que comeca bem antes de 2012) so fecha com ela. Nao compare ponto a
ponto com a PNAD sem lembrar do ajuste sazonal: no trecho comum a diferenca e
sazonal, nao metodologica.

## Escala

Percentual da forca de trabalho (%), ja em media movel de 3 meses e
dessazonalizado. E nivel: nao anualizar, nao acumular, nao voltar a suavizar.

## Historico

2004-04 -> o mes de referencia da edicao (mensal). Nada antes de 2004-04 -- e
onde o proprio BCB comeca o grafico.

## Banco

macro_brasil.mt_desocupacao_retro -- PRIMARY KEY (date). ~265 linhas.

`run()` TRUNCA antes de recarregar, pelo mesmo motivo semantico de
`pm_hiato_produto`: a tabela E uma edicao, e o BCB republica a serie inteira
revisada a cada trimestre (a nota da aba diz "versao atualizada"). Num upsert,
um mes que sumisse da grade de uma edicao nova ficaria para tras como linha orfa
da anterior, misturando duas edicoes na tabela que existe para conter uma. Um
snapshot CSV vai para `_backups/` antes do truncate.
"""

from __future__ import annotations

import datetime as dt
import os

import pandas as pd

from connectors.bcb_rpm import AnexoRPM, normalizar
from connectors.mysql import (
    backup_table_before_truncate,
    insert_data_into_database,
    truncate_table,
)

_DATABASE = "macro_brasil"
_TABLE = "mt_desocupacao_retro"
_BACKUP_DIR = os.path.join(os.path.dirname(__file__), "_backups")

# Casa "Grafico 1.2.11 - Taxa de desocupacao" em qualquer edicao. O numero do
# grafico anda de edicao para edicao (o do hiato ja foi 2.2.3, 2.2.4, 2.2.6 e
# 2.2.8), entao localizar por nome de aba e furado -- `localizar_aba()` casa
# contra o titulo publicado no cabecalho da coluna A, ja normalizado.
_PADRAO_ABA = r"^grafico \d+\.\d+\.\d+ .*taxa de desocupacao"

# A celula de unidade tem que continuar dizendo estas tres coisas. Se o BCB
# trocar a serie por uma sem ajuste sazonal ou sem MM3M, os numeros mudam de
# significado sem mudar de forma -- o unico aviso e esta celula, entao ela e
# guarda e nao decoracao.
_UNIDADE_ESPERADA = ("%", "mm3m", "a.s.")


def _parse(anexo: AnexoRPM, vintage: dt.date) -> tuple[pd.DataFrame, str]:
    """Devolve (DataFrame com date/value, titulo da aba que casou)."""
    ws, titulo = anexo.localizar_aba(anexo.abrir(vintage), _PADRAO_ABA)
    g = anexo.grade(ws)

    if g.shape[1] < 2:
        raise RuntimeError(
            f"{_TABLE}: aba '{ws.title}' da edicao {vintage:%Y-%m} tem "
            f"{g.shape[1]} coluna(s); esperava data + serie."
        )

    # Bloco de dados: toda linha cuja coluna A e uma data de verdade. O
    # cabecalho ("Mes"/"Taxa de desocupacao") e a nota de rodape ficam de fora
    # por nao serem data -- mais robusto que contar linhas, que o BCB muda.
    dados = g[g[0].apply(lambda v: isinstance(v, (dt.date, dt.datetime, pd.Timestamp)))]
    if dados.empty:
        raise RuntimeError(
            f"{_TABLE}: nenhuma linha com data na coluna A da aba '{ws.title}' "
            f"({vintage:%Y-%m}). O BCB pode ter passado a rotular o mes como "
            f"texto ('abr/2004') -- conferir a aba e ajustar o parser."
        )

    # Unidade: uma das celulas da coluna B acima do bloco de dados. Procuramos a
    # que casa, em vez de fixar a linha -- na edicao 2026-06 a unidade esta na
    # linha 7 e o rotulo da serie ("Taxa de desocupacao") na 8, e o BCB ja
    # mostrou que mexe no numero de linhas de cabecalho entre edicoes.
    cabeca = [str(v) for v in g.loc[: dados.index[0] - 1, 1].dropna()]
    if not any(all(t in normalizar(c) for t in _UNIDADE_ESPERADA) for c in cabeca):
        raise RuntimeError(
            f"{_TABLE}: nenhuma celula de cabecalho da edicao {vintage:%Y-%m} "
            f"declara '%, MM3M, a.s.' (vi {cabeca}). A serie so entra no banco "
            f"enquanto for %, MM3M e dessazonalizada -- se o BCB trocou, a coluna "
            f"`value` passa a significar outra coisa e a decisao tem que ser "
            f"explicita."
        )

    out = pd.DataFrame({
        "date": pd.to_datetime(dados[0].values).normalize(),
        "value": pd.to_numeric(dados[1], errors="coerce").values,
    }).dropna(subset=["value"])
    out["date"] = out["date"].dt.date

    if out["date"].duplicated().any():
        raise RuntimeError(f"{_TABLE}: mes repetido na aba '{ws.title}' ({vintage:%Y-%m}).")

    return out.sort_values("date").reset_index(drop=True), titulo


def run(vintage: str | dt.date | None = None) -> None:
    """Atualiza macro_brasil.mt_desocupacao_retro com a edicao mais recente.

    Args:
        vintage: edicao a carregar, "YYYY-MM" ou date. None (default) descobre a
                 mais recente publicada -- o comportamento de rotina. Passar uma
                 edicao antiga deixa a tabela deliberadamente desatualizada.
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

    df, titulo = _parse(anexo, alvo)
    df["vintage"] = alvo

    print(
        f"{_TABLE}: edicao {alvo:%Y-%m} ('{titulo}'), {len(df)} linhas, "
        f"{df['date'].min()} -> {df['date'].max()}, "
        f"ultimo valor {df['value'].iloc[-1]:.2f}%."
    )

    backup_table_before_truncate(_DATABASE, _TABLE, _BACKUP_DIR)
    truncate_table(_DATABASE, _TABLE)
    insert_data_into_database(_DATABASE, _TABLE, df)


if __name__ == "__main__":
    run()
