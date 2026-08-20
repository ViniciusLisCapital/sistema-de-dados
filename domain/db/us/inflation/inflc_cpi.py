"""
Niveis mensais do CPI dos EUA por item -- a tabela de fato do CPI.

Guarda NIVEL de indice, nao variacao. As variacoes (M/M, Y/Y, contribuicao) sao
calculadas na leitura, em `analytics/us/inflation/`, e nao gravadas: sao derivaveis
do nivel sem perda, e gravar as duas coisas abre espaco para elas discordarem.

**Nunca comparar niveis entre itens.** A base varia por item -- a maioria e
1982-84=100, mas varios comecam em dezembro de um ano especifico (`cu.base` tem o
periodo-base de cada um). Dois itens com o mesmo nivel nao estao "no mesmo preco";
so as variacoes sao comparaveis.

Quais itens: a uniao dos item_code de `macro_us.inflc_cpi_dim`, ou seja as duas
arvores (355 itens de despesa + os 6 agregados especiais que so existem na de
divulgacao) = 361 itens. Esta tabela e chaveada por item_code, sem coluna `arvore`
-- o nivel de `Apparel` e o mesmo nas duas arvores, so o lugar dele na hierarquia
muda. Cruzar com a dim resolve a arvore na leitura.

`ajuste` esta na CHAVE, nao virou coluna, porque a cobertura e desigual: dos 273
itens, praticamente todos tem NSA e so ~230 tem SA. Uma coluna `value_sa` ficaria
NULL em 40 itens e sugeriria que o par existe.

--------------------------------------------------------------------------------
PERIODOS: so M01-M12 entram
--------------------------------------------------------------------------------
A API do BLS devolve, no meio das observacoes mensais, periodos que sao MEDIAS e
nao meses: `M13` = media anual, `S03` = media anual (nas series semestrais),
`A01` = anual. Todos sao descartados aqui -- somar ou graficar junto com M01-M12
duplicaria o ano.

Cuidado com o caso vizinho: `S01`/`S02` (primeiro/segundo semestre) NAO sao medias
interpoladas, sao a frequencia real das series que o BLS so publica
semestralmente, e filtra-las apagaria dado de verdade. No universo desta tabela
isso nao aparece (todos os 361 itens do CPI-U U.S. city average sao mensais), mas
`_MENSAL` filtra por inclusao (`M01`-`M12`) e nao por exclusao, entao uma serie
semestral entrando aqui um dia seria descartada de forma visivel (contagem zero) em
vez de virar media anual disfarcada de mes.

--------------------------------------------------------------------------------
CUSTO E LIMITES
--------------------------------------------------------------------------------
Medido ao vivo (2026-08, chave registrada = 50 series / 20 anos por requisicao,
cota de 500/dia):

  historico completo, NSA (269 series, 1913-2026)   36 requisicoes,  53s,  154 mil linhas
  historico completo, SA  (230 series, 1913-2026)   30 requisicoes,  ~45s, ~124 mil linhas
  janela de rotina (3 anos, SA+NSA)                 11 requisicoes,  ~12s

Ou seja a carga fria inteira gasta ~13% da cota diaria e a rotina ~2%. `get_series`
avisa por `warnings.warn` se a chamada passar da cota.

--------------------------------------------------------------------------------
DDL
--------------------------------------------------------------------------------
  CREATE TABLE macro_us.inflc_cpi (
      date      DATE         NOT NULL,
      indice    VARCHAR(10)  NOT NULL,
      item_code VARCHAR(16)  NOT NULL,
      ajuste    VARCHAR(3)   NOT NULL,
      value     DOUBLE,
      series_id VARCHAR(24)  NOT NULL,
      PRIMARY KEY (date, indice, item_code, ajuste),
      KEY idx_item (item_code, ajuste, date)
  );
  -- COMMENTs de tabela e de coluna aplicados no MySQL (ver domain/db/CLAUDE.md).

Banco: macro_us.inflc_cpi -- PRIMARY KEY (date, indice, item_code, ajuste)
"""

from __future__ import annotations

import datetime as _dt

import pandas as pd

from connectors.bls import BLS
from connectors.mysql import MySQLDataRequester
from domain.db.us._gravar import gravar

_DATABASE = "macro_us"
_TABLE = "inflc_cpi"

_MENSAL = {f"M{m:02d}" for m in range(1, 13)}

# Prefixo de series id por indice x ajuste. O CPI-W nao publica SA para a media
# nacional; C-CPI-U (encadeado) so tem NSA por construcao.
_PREFIX = {
    ("CPI-U", "NSA"): "CUUR0000",
    ("CPI-U", "SA"): "CUSR0000",
    ("CPI-W", "NSA"): "CWUR0000",
    ("C-CPI-U", "NSA"): "SUUR0000",
}

_MIN_YEAR = 1913


def _item_codes() -> list[str]:
    """Uniao dos item_code das duas arvores da dim."""
    req = MySQLDataRequester(_DATABASE, _TABLE)
    req.connect()
    if req.connection is None:
        raise RuntimeError("sem conexao com o MySQL")
    try:
        df = pd.read_sql("SELECT DISTINCT item_code FROM inflc_cpi_dim", req.connection)
    finally:
        req.connection.close()
    if df.empty:
        raise RuntimeError(
            "macro_us.inflc_cpi_dim esta vazia -- rode inflc_cpi_dim.run() primeiro, "
            "e a lista de itens vem de la"
        )
    return sorted(df["item_code"].tolist())


def run(
    start_year: int | str | None = None,
    end_year: int | None = None,
    indice: str = "CPI-U",
    ajustes: tuple[str, ...] = ("NSA", "SA"),
) -> None:
    """Atualiza macro_us.inflc_cpi.

    Args:
        start_year: ano inicial. Default: 3 anos atras (janela de rotina, ~12s).
                    `"all"` para a serie completa desde 1913 (~2 min, 66 requisicoes).
        end_year:   ano final. Default: ano corrente.
        indice:     CPI-U (default) | CPI-W | C-CPI-U. Ver `_PREFIX` para quais
                    combinacoes indice x ajuste existem de fato.
        ajustes:    quais ajustes buscar. Default ambos; a cobertura de SA e menor
                    que a de NSA e isso e da fonte, nao falha de carga.
    """
    hoje = _dt.date.today()
    if start_year == "all":
        ini = _MIN_YEAR
    elif start_year is None:
        ini = hoje.year - 3
    else:
        ini = int(start_year)
    fim = int(end_year) if end_year else hoje.year

    codes = _item_codes()
    bls = BLS()
    print(f"{indice}: {len(codes)} itens, {ini}-{fim}, ajustes {list(ajustes)}")

    partes = []
    for ajuste in ajustes:
        prefix = _PREFIX.get((indice, ajuste))
        if prefix is None:
            print(f"  {ajuste}: combinacao {indice} x {ajuste} nao existe no BLS -- pulando")
            continue
        ids = [prefix + c for c in codes]
        df = bls.get_series(ids, start_year=ini, end_year=fim)
        if df.empty:
            print(f"  {ajuste}: nenhuma observacao")
            continue
        antes = len(df)
        df = df[df["period"].isin(_MENSAL)].copy()
        descartadas = antes - len(df)
        df["item_code"] = df["series_id"].str[len(prefix):]
        df["ajuste"] = ajuste
        df["indice"] = indice
        partes.append(df[["date", "indice", "item_code", "ajuste", "value", "series_id"]])
        print(f"  {ajuste}: {len(df):,} obs, {df['series_id'].nunique()}/{len(ids)} series, "
              f"{df['date'].min().date()} -> {df['date'].max().date()}"
              f"{f', {descartadas} medias anuais/semestrais descartadas' if descartadas else ''}")

    if not partes:
        print("nada a gravar")
        return

    out = pd.concat(partes, ignore_index=True)
    gravar(_DATABASE, _TABLE, out, sonda="item_code")
    print("  lembrete: rode inflc_cpi_dim.run() depois de uma carga fria, para "
          "preencher sa_begin/nsa_begin/nsa_end na dim")


if __name__ == "__main__":
    run()
