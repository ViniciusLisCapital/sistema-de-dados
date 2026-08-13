"""
Connector para o RTN (Resultado do Tesouro Nacional) da Secretaria do Tesouro Nacional.

Fonte: workbook "Resultado do Tesouro Nacional - Serie Historica - Mensal" (XLSX),
publicado no CKAN da Tesouro Transparente. O nome do arquivo muda todo mes
(ex: seriehistoricamai26.xlsx) mas o id do dataset e do recurso sao estaveis —
por isso a URL de download e resolvida a cada chamada via package_show, nunca
hardcoded.

Dataset: https://www.tesourotransparente.gov.br/ckan/dataset/ab56485b-9c40-4efb-8563-9ce3e1973c4b

O workbook tem uma aba por tabela (indice na aba "Indice"). A aba "1.1" —
"Resultado Primario do Governo Central - Mensal - Resumida" — e wide-format:
coluna A = rotulo da linha (com prefixo hierarquico, ex: "1.1  Receita
Administrada pela RFB"), colunas B em diante = uma por mes desde 1997-01,
com a data no cabecalho (linha 5, indice 4).

Exemplo de uso:

    from connectors.tesouro import RTN

    rtn = RTN()
    df = rtn.get_series({"receita_total": "1.", "despesa_total": "4."})
    # date (Timestamp), name (str), value (float)
"""

from __future__ import annotations

import io

import pandas as pd
import requests

_CKAN_PACKAGE_API = "https://www.tesourotransparente.gov.br/ckan/api/3/action/package_show"
_PACKAGE_ID = "ab56485b-9c40-4efb-8563-9ce3e1973c4b"
_SHEET_NAME = "1.1"
_HEADER_LABEL = "Discriminação"


class RTN:
    """Connector para o workbook de series historicas do RTN."""

    def __init__(self, *, timeout: float = 60.0):
        self.timeout = timeout

    def _current_xlsx_url(self) -> str:
        """Resolve a URL atual do recurso 'Serie Historica - Mensal' via CKAN.

        Necessario porque o nome do arquivo (e por vezes o path) muda todo mes —
        so o id do recurso, obtido via package_show, e estavel.
        """
        resp = requests.get(_CKAN_PACKAGE_API, params={"id": _PACKAGE_ID}, timeout=self.timeout)
        resp.raise_for_status()
        resources = resp.json()["result"]["resources"]
        for r in resources:
            if r.get("format", "").upper() == "XLSX" and "Mensal" in r.get("name", ""):
                return r["url"]
        raise RuntimeError(
            "Recurso 'Resultado do Tesouro Nacional - Serie Historica - Mensal' "
            "nao encontrado no dataset RTN (CKAN pode ter mudado a estrutura)."
        )

    def get_series(self, line_items: dict[str, str]) -> pd.DataFrame:
        """Busca series mensais (R$ milhoes, valores correntes) da aba '1.1' do RTN.

        Args:
            line_items: mapa {nome_final: prefixo_hierarquico}, ex:
                {"receita_total": "1.", "receita_liquida": "3.", "despesa_total": "4."}.
                O prefixo e comparado contra o primeiro token do rotulo da linha
                (ex: "1. RECEITA TOTAL 1/" -> token "1."), nao por substring —
                evita que "1." capture "1.1"/"1.2" etc.

        Returns:
            DataFrame tidy com colunas: date (Timestamp), name (str), value (float).
        """
        url = self._current_xlsx_url()
        resp = requests.get(url, timeout=self.timeout)
        resp.raise_for_status()

        raw = pd.read_excel(io.BytesIO(resp.content), sheet_name=_SHEET_NAME, header=None)

        header_row = raw.index[raw[0] == _HEADER_LABEL][0]
        dates = pd.to_datetime(raw.iloc[header_row, 1:], errors="coerce")

        prefix_to_name = {prefix: name for name, prefix in line_items.items()}
        body = raw.iloc[header_row + 1 :]
        tokens = body[0].astype(str).str.strip().str.split().str[0]
        matched = body[tokens.isin(prefix_to_name)].copy()
        matched["name"] = tokens[tokens.isin(prefix_to_name)].map(prefix_to_name)

        long_df = matched.melt(id_vars="name", value_vars=matched.columns[1:], value_name="value")
        long_df["date"] = long_df["variable"].map(lambda i: dates.loc[i])
        long_df["value"] = pd.to_numeric(long_df["value"], errors="coerce")
        long_df = long_df.dropna(subset=["date", "value"])

        return long_df[["date", "name", "value"]].sort_values(["name", "date"]).reset_index(drop=True)
