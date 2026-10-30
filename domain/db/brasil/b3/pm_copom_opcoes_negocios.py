"""
Negocios e posicao em aberto das opcoes digitais de Copom da B3 -> macro_brasil.pm_copom_opcoes_negocios.

Fonte: boletim de precos do pregao (arquivo PR, `connectors/b3_precos.precos_cpm()`), o mesmo de
`cmb_contratos_b3`. Complementa `pm_copom_opcoes`, que guarda o premio de referencia (arquivo RE):
aquela diz o que o mercado PRECIFICA para cada decisao, esta quanto dinheiro ha atras disso.
Mesma chave, entao as duas se juntam linha a linha.

## O que cada coluna e

- `negocios`, `contratos`, `volume_brl`: os totais do dia na serie, como a B3 publica. Serie sem
  negocio no dia tem os tres em zero.
- `valor_contrato`: quanto um contrato paga se a decisao for a do strike, em R$. **A B3 trocou o
  tamanho do contrato no pregao de 2025-05-26**: era R$ 10.000 e passou a R$ 100, para todas as
  series de uma vez. Medido no proprio boletim, nao lido em documento: volume / (contratos x preco
  medio) da 100 em toda linha antes e 1 em toda linha depois, e a posicao em aberto somada pula de
  23.124 para 2.130.000 de um pregao para o outro. O preco continua em pontos de 0 a 100, entao
  volume = contratos x preco x valor_contrato / 100 (conferido em 29/10/2026: 135.940 contratos a
  68,92 = R$ 9.369.090 na manutencao da 282a). Contagem de contratos de antes e de depois so se
  compara convertida -- quem le multiplica por valor_contrato / 100.
- `oi_abertura`: a posicao em aberto que o arquivo do dia traz, que e a do INICIO do pregao
  (fechamento de D-1) -- ver o docstring de `connectors/b3_precos.py`.
- `oi_fechamento`: a do fim do dia, lida no arquivo do pregao SEGUINTE; NULL ate ele sair, e no
  ultimo pregao de uma reuniao (a serie some no vencimento). Mesma convencao de `_contratos_b3`.
  Fica na unidade do PROPRIO pregao: em 2025-05-23 o arquivo seguinte ja vem em contratos de R$ 100,
  e a leitura e convertida.

## O vencimento

O codigo de negociacao so traz o MES do vencimento (CPMX26C099750: novembro/2026). A data exata
-- a chave de `pm_copom_opcoes` -- vem do arquivo RE do mesmo pregao (`b3_premio`), onde cada
reuniao tem uma linha por vencimento. Nunca ha duas reunioes do Copom no mesmo mes, entao o mes
identifica a reuniao. O RE de um dia as vezes nao traz uma reuniao que o PR ja lista (169 pregoes
de 2023-2026 com uma serie distante assim): o vencimento entao vem do RE de outro pregao da mesma
janela, e so o que nenhum RE alcanca fica de fora, com aviso -- em vez de virar uma data inventada.

## Cobertura

Desde o primeiro CPM (2020-05-25). A historia foi carregada em 2026-10-30 com `run(full=True)`
(~1.600 boletins de ~11 MB, ~1h20 com as 2 conexoes que a B3 aceita); o cache `cache_precos_cpm/`
guarda so o CPM, entao refazer a carga dali leva minutos.

Banco: macro_brasil.pm_copom_opcoes_negocios -- PRIMARY KEY (date, vencimento, variacao_bps)
"""

from __future__ import annotations

import logging
import os
import re

import mysql.connector
import pandas as pd

from connectors import b3_precos, b3_premio
from connectors.mysql import insert_data_into_database

logger = logging.getLogger(__name__)

_DATABASE = "macro_brasil"
_TABLE = "pm_copom_opcoes_negocios"
_INICIO = "2020-05-04"   # o mesmo de pm_copom_opcoes: o primeiro CPM
_DIAS_ROTINA = 10
_TROCA_TAMANHO = pd.Timestamp("2025-05-26")   # contrato de R$ 10.000 -> R$ 100 (ver docstring)
_RE_CPM = re.compile(r"^CPM([FGHJKMNQUVXZ])(\d\d)C(\d{6})$")
_MESES = dict(zip("FGHJKMNQUVXZ", range(1, 13)))

_DDL = """
CREATE TABLE IF NOT EXISTS pm_copom_opcoes_negocios (
    date           DATE    NOT NULL COMMENT 'Pregao',
    vencimento     DATE    NOT NULL COMMENT 'Vencimento da opcao: o dia util seguinte a reuniao do Copom (a mesma chave de pm_copom_opcoes)',
    variacao_bps   DECIMAL(6,1) NOT NULL COMMENT 'Decisao a que a opcao se refere: variacao da meta Selic em pontos-base (-25 = corte de 25, 0 = manutencao)',
    negocios       INT     NOT NULL COMMENT 'Numero de negocios no dia',
    contratos      BIGINT  NOT NULL COMMENT 'Contratos negociados no dia, como a B3 publica (cada um paga valor_contrato se a decisao for esta)',
    valor_contrato DOUBLE  NOT NULL COMMENT 'R$ que um contrato paga se a decisao for esta: 10.000 ate 2025-05-23, 100 desde 2025-05-26 (a B3 trocou o tamanho)',
    volume_brl     DOUBLE  NOT NULL COMMENT 'Volume financeiro do dia em R$ (contratos x preco x valor_contrato / 100, preco em pontos de 0 a 100)',
    preco_medio    DOUBLE  NULL     COMMENT 'Preco medio dos negocios do dia, em pontos (NULL sem negocio)',
    ultimo         DOUBLE  NULL     COMMENT 'Ultimo preco do dia, em pontos (NULL sem negocio)',
    oi_abertura    BIGINT  NOT NULL COMMENT 'Posicao em aberto no INICIO do pregao (fechamento de D-1), como o arquivo do dia traz',
    oi_fechamento  BIGINT  NULL     COMMENT 'Posicao em aberto no fim do dia, do arquivo do pregao seguinte; NULL ate ele sair',
    PRIMARY KEY (date, vencimento, variacao_bps)
) COMMENT='Negocios e posicao em aberto das opcoes digitais de Copom da B3 (CPM), do boletim de precos (arquivo PR). Complementa pm_copom_opcoes (premio de referencia, arquivo RE), com a mesma chave. Desde 2020-05. Contrato de R$ 10.000 ate 2025-05-23 e de R$ 100 depois (valor_contrato). Ver domain/db/brasil/b3/pm_copom_opcoes_negocios.py.'
"""


def _conectar():
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ.get("MYSQL_PASSWORD", ""),
        database=_DATABASE,
    )


def _garantir_tabela() -> None:
    cnx = _conectar()
    try:
        cur = cnx.cursor()
        cur.execute(_DDL)
        # A tabela nasceu (2026-10-30) sem valor_contrato: as linhas de entao sao todas de R$ 100.
        cur.execute("SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=%s AND "
                    "TABLE_NAME=%s AND COLUMN_NAME='valor_contrato'", (_DATABASE, _TABLE))
        if cur.fetchone()[0] == 0:
            cur.execute("ALTER TABLE pm_copom_opcoes_negocios ADD COLUMN valor_contrato DOUBLE NOT NULL "
                        "DEFAULT 100 COMMENT 'R$ que um contrato paga se a decisao for esta: 10.000 ate "
                        "2025-05-23, 100 desde 2025-05-26 (a B3 trocou o tamanho)' AFTER contratos")
        cnx.commit()
    finally:
        cnx.close()


def _valor_contrato(data) -> float:
    return 10000.0 if pd.Timestamp(data) < _TROCA_TAMANHO else 100.0


def _vencimentos(data) -> dict[tuple[int, int], pd.Timestamp]:
    """(ano, mes) -> vencimento exato, do arquivo RE do mesmo pregao. O mes do codigo e o da
    REUNIAO, e o vencimento e o dia util seguinte a ela -- que cai no mes seguinte quando a
    reuniao e no fim do mes (31/07/2024 -> CPMN24, vencimento 01/08/2024). A chave e o mes da
    vespera do vencimento; o do proprio vencimento fica de reserva."""
    P = b3_premio.premios(data, mercadoria="CPM")
    if P is None:
        return {}
    out: dict = {}
    vs = [pd.Timestamp(v) for v in P["vencimento"].unique().tolist()]
    for v in vs:
        r = v - pd.offsets.BDay(1)
        out[(r.year, r.month)] = v
    for v in vs:
        out.setdefault((v.year, v.month), v)
    return out


def linhas_do_pregao(C: pd.DataFrame, data, venc: dict, oi_seguinte: dict | None,
                     data_seguinte=None) -> pd.DataFrame:
    """As series CPM de um pregao com negocio ou posicao. `oi_seguinte`: ticker -> oi_abertura
    do pregao seguinte (None se ele ainda nao saiu), convertida para a unidade deste pregao."""
    data = pd.Timestamp(data).normalize()
    valor = _valor_contrato(data)
    fator = 1.0 if data_seguinte is None else valor / _valor_contrato(data_seguinte)
    linhas, sem_venc = [], set()
    for r in C.itertuples():
        m = _RE_CPM.match(str(r.ticker))
        if not m:
            continue
        neg = 0 if pd.isna(r.negocios) else int(r.negocios)
        oi0 = 0 if pd.isna(r.oi_abertura) else int(r.oi_abertura)
        oi1 = None if oi_seguinte is None else oi_seguinte.get(r.ticker)
        if oi1 is not None:
            oi1 = round(oi1 / fator)
        if neg == 0 and oi0 == 0 and not oi1:
            continue
        chave = (2000 + int(m[2]), _MESES[m[1]])
        v = venc.get(chave)
        if v is None:
            sem_venc.add(chave)
            continue
        if v <= data:   # no dia do vencimento a serie ja e exercicio, nao negocio
            continue
        k = int(m[3]) / 1000
        linhas.append({
            "date": data.date(), "vencimento": v.date(),
            "variacao_bps": round(((k - 100) * 100) / 2.5) * 2.5,
            "negocios": neg,
            "contratos": 0 if pd.isna(r.contratos) else int(r.contratos),
            "valor_contrato": valor,
            "volume_brl": 0.0 if pd.isna(r.vol_brl) else float(r.vol_brl),
            "preco_medio": None if pd.isna(r.medio) else float(r.medio),
            "ultimo": None if pd.isna(r.ultimo) else float(r.ultimo),
            "oi_abertura": oi0,
            "oi_fechamento": None if oi1 is None else int(oi1),
        })
    if sem_venc:
        logger.warning("pm_copom_opcoes_negocios %s: mes de vencimento sem reuniao no arquivo RE: %s",
                       data.date(), sorted(sem_venc))
    return pd.DataFrame(linhas)


def coletar(full: bool = False, dias: int = _DIAS_ROTINA) -> pd.DataFrame:
    fim = pd.Timestamp.today().normalize()
    datas = list(pd.bdate_range(_INICIO, fim) if full else pd.bdate_range(end=fim, periods=dias))
    b3_precos.baixar_muitos(datas, cpm=True)
    dias_cpm = [(d, b3_precos.precos_cpm(d)) for d in datas]
    dias_cpm = [(d, C) for d, C in dias_cpm if C is not None]
    vencs = {d: _vencimentos(d) for d, _ in dias_cpm}
    # Reuniao que o PR de um dia lista e o RE daquele dia nao traz: o vencimento vem do RE de
    # outro pregao da janela (o mes identifica a reuniao).
    todos: dict = {}
    for v in vencs.values():
        for k, x in v.items():
            todos.setdefault(k, x)
    partes = []
    for k, (d, C) in enumerate(dias_cpm):
        seg = dias_cpm[k + 1] if k + 1 < len(dias_cpm) else None
        oi_seg = None if seg is None else dict(zip(seg[1]["ticker"], seg[1]["oi_abertura"].fillna(0)))
        if not vencs[d]:
            logger.warning("pm_copom_opcoes_negocios %s: sem arquivo RE, pregao fora", d.date())
            continue
        partes.append(linhas_do_pregao(C, d, {**todos, **vencs[d]}, oi_seg, None if seg is None else seg[0]))
    partes = [p for p in partes if len(p)]
    if not partes:
        return pd.DataFrame()
    df = pd.concat(partes, ignore_index=True)
    # Guarda de layout: preco em pontos de 0 a 100, e o volume tem de ser contratos x preco x
    # valor_contrato / 100 -- e e esta conta que pega uma nova troca de tamanho do contrato.
    ruim = df[(df.preco_medio.notna()) & ((df.preco_medio < 0) | (df.preco_medio > 100.5))]
    if len(ruim):
        raise ValueError(f"pm_copom_opcoes_negocios: preco fora de [0, 100]:\n{ruim.head().to_string()}")
    com = df[df.contratos > 0]
    desvio = ((com.volume_brl - com.contratos * com.preco_medio * com.valor_contrato / 100).abs()
              / com.volume_brl.clip(lower=1))
    if (desvio > 0.01).any():
        raise ValueError("pm_copom_opcoes_negocios: volume != contratos x preco medio x valor / 100:\n"
                         f"{com[desvio > 0.01].head().to_string()}")
    return df


def run(full: bool = False, dias: int = _DIAS_ROTINA) -> None:
    """Atualiza macro_brasil.pm_copom_opcoes_negocios.

    Args:
        full: True carrega desde o primeiro CPM (2020-05) -- ~1.600 boletins; minutos do cache.
        dias: dias uteis para tras no passe de rotina.
    """
    _garantir_tabela()
    df = coletar(full=full, dias=dias)
    if df.empty:
        logger.warning("pm_copom_opcoes_negocios: nada a inserir")
        return
    logger.info("pm_copom_opcoes_negocios: %d linhas, %s -> %s", len(df), df.date.min(), df.date.max())
    insert_data_into_database(_DATABASE, _TABLE, df)
