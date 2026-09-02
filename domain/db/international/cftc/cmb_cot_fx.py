"""
Posicionamento especulativo em futuros de moedas — CFTC TFF (Traders in Financial Futures).

Moedas: BRL, MXN (bem cobertos); CLP, COP (esparsos — pode nao aparecer todos os anos)

Series armazenadas (campo 'name') -- desde 2026-09-01 as CINCO categorias de
participante do TFF, e nao so os fundos alavancados:

  open_interest    — Contratos em aberto (total)

  <p>_long / <p>_short / <p>_spread / <p>_net, com <p> em:
    dealer     — Dealer/Intermediario (sell side: bancos e swap dealers cobrindo
                 o livro de balcao que rodam para clientes)
    asset_mgr  — Asset Manager/Institucional (real money)
    lev        — Leveraged Funds (hedge funds e CTAs -- o dinheiro especulativo)
    other      — Other Reportables (tamanho reportavel, nenhum dos tres papeis)
    nonrept    — Nao-reportaveis (abaixo do limite de reporte da CFTC).
                 SEM coluna de spread na fonte, entao `nonrept_spread` nao existe.

Duas identidades fecham EXATAMENTE (conferido no arquivo BRL de 2025, residuo
zero nas 52 semanas, dos dois lados):

  open_interest = Σ_p (<p>_long + <p>_spread) = Σ_p (<p>_short + <p>_spread)
  Σ_p <p>_net   = 0

`spread` fica fora do liquido de proposito: uma posicao travada e comprada e
vendida ao mesmo tempo e cancela na exposicao direcional -- e o que faz os cinco
nets somarem zero.

Cobertura do BRL: o contrato so aparece no TFF a partir de **2011-04-05** (o
arquivo de 2010 nao tem uma linha de BRAZILIAN REAL), e tem 16 buracos maiores
que 8 dias ate 2015, incluindo um de 196 dias entre out/2011 e abr/2012. Nao ha
backfill possivel antes disso -- o dado nao existe na fonte.

Banco: macro_international.cmb_cot_fx
Schema: PRIMARY KEY (date, currency, name)
"""

from datetime import datetime

from connectors.cftc import CFTC
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_international"
_TABLE    = "cmb_cot_fx"

# CLP and COP do not appear in CFTC TFF file (no CME FX futures for these)
_CONTRACT_NAMES = [
    "BRAZILIAN REAL",
    "MEXICAN PESO",
]

_cftc = CFTC()


def run(years: list[int] | None = None, n_anos: int = 3) -> None:
    """Atualiza macro_international.cmb_cot_fx com posicionamento COT de moedas.

    Args:
        years:  Lista de anos a buscar. Se None, usa os ultimos n_anos incluindo o atual.
        n_anos: Quantos anos buscar quando years=None (default 3).

    Para recarga completa (o que a expansao de 2026-09-01 exigiu, ja que as series
    novas nao existiam nas linhas antigas): `run(years=list(range(2011, ANO + 1)))`.
    O BRL nao existe no TFF antes de 2011-04; o MXN comeca em 2010-07.
    """
    if years is None:
        current = datetime.now().year
        years = list(range(current - n_anos + 1, current + 1))

    df = _cftc.get_cot_fx(contract_names=_CONTRACT_NAMES, years=years)
    insert_data_into_database(_DATABASE, _TABLE, df)
