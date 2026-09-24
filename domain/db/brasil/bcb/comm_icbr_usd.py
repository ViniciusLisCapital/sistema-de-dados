"""
IC-Br (Indice de Commodities - Brasil) em USD -- BCB SGS 29042.

Distinto de comm_icbr.py (SGS 27574 etc.), que e denominado em REAIS. O BCB
converte precos internacionais de commodities para reais na construcao do
IC-Br "geral" -- adequado para o proposito original do indice (insumo da
curva de Phillips de precos livres do modelo agregado, onde o repasse
cambial e parte do que se quer capturar), mas isso o torna ENDOGENO ao
proprio USD/BRL, inadequado como regressor num modelo que explica o
USD/BRL (circularidade: o canal ja embute parte do movimento da variavel
dependente). SGS 29042 e a versao em dolar do mesmo indice, testada e
confirmada 2026-07-31 no ridge_deviation_model.py como canal USD-neutro de
precos globais de commodities -- melhorou o MSE out-of-sample (walk-forward)
em ~4.6% isoladamente sobre o spec ja embarcado, com coeficiente negativo e
estavel (quase nunca cruza zero nas 163 janelas rolantes) -- ver
analytics/brasil/exchange_rate/CLAUDE.md para o registro completo.

Codigo confirmado por identificacao direta do usuario (nao pela metadata
API do BCB, que exige sessao autenticada); corroborado indiretamente aqui
por retornar valores materialmente diferentes de SGS 27574 para os mesmos
meses (consistente com duas denominacoes distintas do mesmo indice
subjacente).

Series SGS (mensais, desde 1998-01). Os codigos NAO seguem a ordem dos
equivalentes em reais e nao sao sequenciais a partir do geral -- foram lidos da
tela de series do proprio SGS (2026-09-17), nao deduzidos:
  icbr_usd               29042 — IC-Br geral,        em USD   (27574 em BRL)
  icbr_agropecuaria_usd  29041 — IC-Br agropecuaria, em USD   (27575 em BRL)
  icbr_metal_usd         29040 — IC-Br metal,        em USD   (27576 em BRL)
  icbr_energia_usd       29039 — IC-Br energia,      em USD   (27577 em BRL)

O geral mantem o nome `icbr_usd` em vez de virar `icbr_geral`: ele ja e lido por
`analytics/brasil/exchange_rate/models/ridge_deviation_model.py` e pelo painel do
modelo estrutural, e renomear quebraria os dois sem ganho. Os tres novos levam o
sufixo `_usd` para que todo nome da tabela siga a mesma regra.

Conferido contra a construcao propria: IC-Br em reais dividido pela PTAX MEDIA DO
MES reproduz o 29042 com correlacao de 0,9989 nas variacoes mensais (erro medio
0,084 p.p.) em 343 meses; com PTAX de fim de mes a correlacao cai para 0,56. Serve
de gabarito caso alguma das series em dolar saia do ar.

Banco: macro_brasil.comm_icbr_usd — PRIMARY KEY (date, name)
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "comm_icbr_usd"

_SERIES = {
    "icbr_usd": 29042,
    "icbr_agropecuaria_usd": 29041,
    "icbr_metal_usd": 29040,
    "icbr_energia_usd": 29039,
}

_bcb = BCB()


def run(start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.comm_icbr_usd.

    Args:
        start: data inicial "DD/MM/YYYY", ou "all" para serie completa (desde 1998).
        end:   data final "DD/MM/YYYY". Default: hoje.
    """
    if start == "all":
        df = _bcb.get_sgs(_SERIES, start="01/01/1998", end=end)
    elif start:
        df = _bcb.get_sgs(_SERIES, start=start, end=end)
    else:
        df = _bcb.get_sgs_ultimos(_SERIES, n=36)

    insert_data_into_database(_DATABASE, _TABLE, df)
