"""
Connector para a API IPEADATA (OData v4).

Usado para series que a IPEA disponibiliza mas o BCB SGS nao tem — ex:
termos de troca (Funcex), cuja API expoe metadados e valores por SERCODIGO.

Documentacao: http://www.ipeadata.gov.br/api/

Nota tecnica: o filtro OData $filter=contains(...) retorna 400 nesta API —
usar substringof('valor', CAMPO) (sintaxe OData v3) no lugar.

Exemplo de uso:

    from connectors.ipeadata import IPEA

    ipea = IPEA()
    df = ipea.get_series("FUNCEX12_TTR12")
    # date (Timestamp), value (float)
"""

from __future__ import annotations

import pandas as pd
import requests

_BASE = "http://www.ipeadata.gov.br/api/odata4"


class IPEA:
    """Connector para a API OData da IPEADATA."""

    def __init__(self, *, timeout: float = 30.0):
        self.timeout = timeout

    def get_series(self, sercodigo: str) -> pd.DataFrame:
        """Busca a serie historica completa de um SERCODIGO da IPEADATA.

        Args:
            sercodigo: codigo da serie (ex: "FUNCEX12_TTR12").

        Returns:
            DataFrame tidy com colunas: date (Timestamp), value (float).
        """
        url = f"{_BASE}/ValoresSerie(SERCODIGO='{sercodigo}')"
        resp = requests.get(url, timeout=self.timeout)
        resp.raise_for_status()

        data = resp.json().get("value", [])
        df = pd.DataFrame(data)
        if df.empty:
            return pd.DataFrame(columns=["date", "value"])

        df["date"] = pd.to_datetime(df["VALDATA"], utc=True).dt.tz_convert(None).dt.normalize()
        df["value"] = pd.to_numeric(df["VALVALOR"], errors="coerce")
        return df[["date", "value"]].sort_values("date").reset_index(drop=True)

    def buscar_series(self, termo: str, campo: str = "SERNOME") -> pd.DataFrame:
        """Busca series por substring no nome ou codigo (util para descobrir SERCODIGO).

        Args:
            termo:  substring a procurar (case-sensitive na API).
            campo:  "SERNOME" (nome da serie) ou "SERCODIGO".

        Returns:
            DataFrame com SERCODIGO, SERNOME, PERNOME, FNTSIGLA.
        """
        url = f"{_BASE}/Metadados?$filter=substringof('{termo}',{campo})"
        resp = requests.get(url, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json().get("value", [])
        return pd.DataFrame(data)
