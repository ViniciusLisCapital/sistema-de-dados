"""
Uma linha por reuniao do Copom: o que foi decidido para a Selic.

Contrapartida de `pm_copom_projecoes`, que guarda o que o Comite PROJETA. Esta guarda o que ele
FEZ -- e as duas juntas sao o par que permite ler a reacao: projecao acima da meta no horizonte
relevante contra o passo de juros da mesma reuniao.

## Por que a fonte e a serie de meta, e nao o texto do comunicado

O comunicado publica a decisao em prosa e `_copom_texto.py` ja a le, mas so da 206a reuniao
(2017-04) em diante -- antes disso o texto muda de forma varias vezes e a carga nao o cobre. A
**SGS 432** (meta Selic definida pelo Copom, diaria) comeca em **1999-03-05**, o inicio do regime
de metas, e cobre toda a historia relevante sem parser nenhum. O comunicado entra aqui como
CONFERENCIA independente, nao como fonte: `validar()` compara as duas e devolve as divergencias.

O passo de cada reuniao e a diferenca entre o nivel vigente NO DIA da decisao e o nivel que passa
a vigorar depois dela (a meta nova vale a partir do dia util seguinte, por isso a janela de
`_DIAS_VIGENCIA` dias). Nao e a diferenca entre o nivel decidido em duas reunioes consecutivas:
essas duas definicoes divergem quando a meta muda FORA de reuniao, e a segunda atribuiria a
mudanca a reuniao errada.

## O vies, que e a razao de existir a coluna `alterada_fora_da_reuniao`

Ate 2003 o comunicado podia sair com vies de alta ou de baixa, autorizando o presidente do BCB a
mover a meta entre reunioes. Medido na serie: **8 mudancas de nivel** caem a mais de 5
dias da reuniao anterior -- 6 em 1999 e 2 em 2000 (29/03 e 10/07, ambas de -50 pb) -- e marcam **4
reunioes**, a 35a, a 36a, a 46a e a 49a. A reuniao seguinte a um movimento de vies registra o passo
que ela mesma decidiu, que pode ser zero com razao; a coluna e o que avisa que o nivel de entrada
dela nao e o que a reuniao anterior deixou. Sem ela, uma queda de juros de verdade nao apareceria
em reuniao nenhuma e a serie de passos nao somaria o caminho da Selic.

## Cobertura

As reunioes 21a a 33a (1998-01 a 1999-03) ficam FORA: a meta Selic nao existia ainda, o
instrumento eram a TBC e a TBAN. A tabela comeca na **34a (14/04/1999)**.

## Banco

    CREATE TABLE macro_brasil.pm_copom_reuniao (
        nro_reuniao               SMALLINT      NOT NULL,
        date                      DATE          NOT NULL,
        selic_anterior            DECIMAL(6,2),
        selic_decidida            DECIMAL(6,2),
        variacao_bps              SMALLINT,
        decisao                   VARCHAR(12),
        alterada_fora_da_reuniao  TINYINT(1)    NOT NULL DEFAULT 0,
        PRIMARY KEY (nro_reuniao),
        KEY idx_date (date)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

Upsert: reprocessar a mesma reuniao corrige a linha em vez de duplicar.
"""

from __future__ import annotations

import datetime as dt

import pandas as pd

from connectors.bcb import BCB
from connectors.bcb_copom import calendario_reunioes
from connectors.mysql import insert_data_into_database
from domain.db.brasil.bcb import _copom_texto as ct

_DATABASE = "macro_brasil"
_TABLE = "pm_copom_reuniao"

_SGS_META_SELIC = 432
# SGS 432 e diaria e a API devolve 406 acima de ~10 anos por requisicao -- mesmo limite medido em
# domain/db/international/fred/diferenciais_juros.py.
_JANELA_DIAS = 8 * 365
# Janela para a meta nova aparecer na serie. A 432 e diaria de dia CORRIDO e sem buraco (10.036
# observacoes em 10.036 dias, medido), e a meta decidida vale do dia util seguinte -- mas um feriado
# emendado empurra isso: das 152 mudancas de nivel do periodo, 147 entram 1 dia depois da reuniao,
# 4 entram em 2 (reuniao de quarta com feriado na quinta: Corpus Christi de 2003/2007/2009 e o 7 de
# setembro de 2017) e 1 em 5 (20/04/2011, com Tiradentes na quinta e Sexta-feira Santa no dia
# seguinte). Os 8 movimentos por VIES, que nao pertencem a reuniao nenhuma, estao todos a 7 dias ou
# mais. Cinco dias separa as duas coisas exatamente: nao perde decisao nem captura vies.
_DIAS_VIGENCIA = 5
# Primeiro dia da serie 432; antes disso o instrumento era TBC/TBAN.
INICIO_META = dt.date(1999, 3, 5)


def meta_selic(inicio: str = "1999-01-01", fim: str | None = None) -> pd.Series:
    """SGS 432 (meta Selic, diaria) encadeada em janelas -> Series indexada por data."""
    bcb = BCB(timeout=90.0)
    a = pd.Timestamp(inicio)
    b = pd.Timestamp(fim) if fim else pd.Timestamp(dt.date.today())
    partes = []
    while a <= b:
        c = min(a + pd.Timedelta(days=_JANELA_DIAS), b)
        partes.append(bcb.get_sgs({"selic_meta": _SGS_META_SELIC},
                                  a.strftime("%d/%m/%Y"), c.strftime("%d/%m/%Y")))
        a = c + pd.Timedelta(days=1)
    df = pd.concat(partes, ignore_index=True)
    s = df.set_index(pd.to_datetime(df["date"]))["value"].astype(float)
    return s[~s.index.duplicated(keep="last")].sort_index()


def montar(cal: dict[int, str] | None = None, meta: pd.Series | None = None) -> pd.DataFrame:
    """Calendario de reunioes + meta Selic diaria -> DataFrame no shape da tabela."""
    cal = cal if cal is not None else calendario_reunioes()
    meta = meta if meta is not None else meta_selic()

    def nivel_em(d: pd.Timestamp) -> float | None:
        s = meta[meta.index <= d]
        return float(s.iloc[-1]) if len(s) else None

    linhas: list[dict] = []
    anterior_decidida: float | None = None
    for nro, iso in sorted(cal.items()):
        d = pd.Timestamp(iso)
        antes = nivel_em(d)
        depois = nivel_em(d + pd.Timedelta(days=_DIAS_VIGENCIA))
        if antes is None or depois is None:
            continue  # antes de 1999-03-05 nao havia meta; depois do fim da serie nao ha vigencia
        bps = round((depois - antes) * 100)
        linhas.append({
            "nro_reuniao": nro,
            "date": d.date(),
            "selic_anterior": round(antes, 2),
            "selic_decidida": round(depois, 2),
            "variacao_bps": bps,
            "decisao": "elevacao" if bps > 0 else ("reducao" if bps < 0 else "manutencao"),
            "alterada_fora_da_reuniao": int(
                anterior_decidida is not None and abs(antes - anterior_decidida) > 1e-9
            ),
        })
        anterior_decidida = depois

    return pd.DataFrame(linhas)


def validar(df: pd.DataFrame) -> list[str]:
    """Confere o passo derivado da SGS 432 contra a decisao que o comunicado escreve em prosa.

    Conferencia independente de verdade: as duas fontes nao compartilham nem o dado nem o codigo.
    Cobre so as reunioes que `_copom_texto` carrega (206a em diante) e que trazem a decisao no
    texto -- nas outras nao ha o que comparar.
    """
    por_nro = df.set_index("nro_reuniao")
    problemas: list[str] = []
    comparadas = 0
    for caminho in ct.arquivos():
        nro = int(caminho.name.split("_")[1])
        if nro not in por_nro.index:
            continue
        c = ct.parse(caminho.read_text(encoding="utf-8"), caminho.name)
        if c.decisao is None:
            continue
        comparadas += 1
        linha = por_nro.loc[nro]
        if c.decisao != linha["decisao"]:
            problemas.append(f"reuniao {nro}: comunicado diz '{c.decisao}', "
                             f"SGS 432 diz '{linha['decisao']}'")
        if (c.selic_decidida is not None
                and abs(c.selic_decidida - float(linha["selic_decidida"])) > 0.005):
            problemas.append(f"reuniao {nro}: comunicado diz Selic {c.selic_decidida}%, "
                             f"SGS 432 diz {linha['selic_decidida']}%")
    problemas.append(f"({comparadas} reunioes comparadas com o texto do comunicado)")
    return problemas


def run(inicio: str = "1999-01-01") -> None:
    """Atualiza macro_brasil.pm_copom_reuniao.

    Args:
        inicio: primeiro dia da janela da SGS 432. O default cobre a serie toda; passar uma data
                recente so acelera o fetch, e as reunioes anteriores a ela ficam de fora.
    """
    df = montar(meta=meta_selic(inicio=inicio))
    if df.empty:
        print(f"{_TABLE}: nada a inserir.")
        return

    n = df["decisao"].value_counts()
    fora = int(df["alterada_fora_da_reuniao"].sum())
    print(f"{_TABLE}: {len(df)} reunioes, {df['nro_reuniao'].min()}a ({df['date'].min()}) -> "
          f"{df['nro_reuniao'].max()}a ({df['date'].max()}). "
          f"{n.get('elevacao', 0)} elevacoes / {n.get('manutencao', 0)} manutencoes / "
          f"{n.get('reducao', 0)} reducoes; {fora} com meta alterada fora de reuniao.")

    for p in validar(df):
        print(f"  {p}")

    insert_data_into_database(_DATABASE, _TABLE, df)


if __name__ == "__main__":
    run()
