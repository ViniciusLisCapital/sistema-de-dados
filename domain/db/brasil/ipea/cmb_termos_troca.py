"""
Termos de troca do Brasil (Funcex, via IPEADATA).

Substitui a fonte anterior (BCB SGS 22099/22100) — confirmado que esses dois
codigos NAO sao termos de troca cambiais, e sim series de Contas Nacionais
(PIB). A serie correta de termos de troca e publicada pela Funcex e
disponibilizada pela IPEADATA, nao pelo BCB SGS.

Serie IPEADATA:
  FUNCEX12_TTR12 — Termos de troca - indice mensal (media 2018=100)
                   PX/PM (indice de precos de exportacao / indice de precos de importacao)
                   Fonte: Funcex. Historico: 1978-01 -> hoje.

Banco: macro_brasil.cmb_termos_troca — PRIMARY KEY (date, name)
"""

from connectors.ipeadata import IPEA
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "cmb_termos_troca"
_SERIE    = "FUNCEX12_TTR12"
_NOME     = "termos_de_troca_funcex"

_ipea = IPEA()


def run(start: str | None = None) -> None:
    """Atualiza macro_brasil.cmb_termos_troca com a serie Funcex/IPEADATA.

    Args:
        start: nao utilizado — a API IPEADATA so retorna a serie historica
               completa (sem parametro de range). Mantido por consistencia
               de assinatura com os demais scripts run().
    """
    df = _ipea.get_series(_SERIE)
    df["name"] = _NOME
    df = df[["date", "name", "value"]]

    insert_data_into_database(_DATABASE, _TABLE, df)
