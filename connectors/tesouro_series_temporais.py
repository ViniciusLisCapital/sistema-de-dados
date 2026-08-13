"""
Connector para a API de Series Temporais do Tesouro Nacional.

Backend NAO documentado no catalogo CKAN da Tesouro Transparente -- descoberto
rastreando as chamadas de rede que a propria pagina publica faz:
https://www.tesourotransparente.gov.br/visualizacao/series-temporais-do-tesouro-nacional

Sem autenticacao, "Access-Control-Allow-Origin: *". Por nao ser documentado,
pode mudar sem aviso -- ver connectors/CLAUDE.md para o achado completo
(inclusive o teste ao vivo de que a API "oficial" listada no CKAN para o RTN,
apiapex.tesouro.gov.br, continua morta -- loop de redirecionamento).

Estrutura: Tema (ex: "10 - Resultado Fiscal do Governo Central - Valores
Mensais") -> Subtema (ex: "10.03 Despesas") -> arvore de series com plano de
contas hierarquico (ex: "10.03.1.1.02.1") e id proprio por serie.

Exemplo de uso:

    from connectors.tesouro_series_temporais import SeriesTemporais

    st = SeriesTemporais()
    temas = st.get_temas()                       # lista de temas (10-20)
    subtemas = st.get_subtemas(tema_id=1)         # subtemas do tema 10 (id interno, nao o codigo "10")
    arvore = st.get_arvore(subtema_id=3)          # arvore completa de series do subtema 10.03
    df = st.get_series(7970)                      # date/value de uma serie por id
    df = st.get_series_bulk({"despesa_total": 7970, "receita_total": 7922})  # varias, formato long
"""

from __future__ import annotations

import io
import time

import pandas as pd
import requests

_BASE = "https://series-temporais.tesouro.gov.br/backend-series-temporais/rest/Public/SerieGrafico"


class SeriesTemporais:
    """Cliente para a API de Series Temporais do Tesouro Nacional."""

    def __init__(self, *, timeout: float = 60.0, sleep_between: float = 0.15):
        self.timeout = timeout
        self.sleep_between = sleep_between
        self._session = requests.Session()

    def get_temas(self) -> list[dict]:
        """Lista todos os temas (10-20)."""
        r = self._session.get(f"{_BASE}/Temas", headers={"Accept": "application/json"}, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def get_subtemas(self, tema_id: int) -> list[dict]:
        """Lista os subtemas de um tema, dado o id INTERNO do tema (nao o codigoExterno "10").

        get_temas() retorna esse id junto com codigoExterno.
        """
        r = self._session.get(f"{_BASE}/Tema/{tema_id}", headers={"Accept": "application/json"}, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def get_arvore(self, subtema_id: int) -> list[dict]:
        """Arvore completa de series (todos os niveis) de um subtema.

        Cada folha tem: id, planoContas (ex: "10.03.1.1"), codigoExterno,
        nivel, descricao, periodicidade, descricaoUnidade, fontePrimaria,
        dataInicialSerie/dataFinalSerie (epoch ms), seriesFilhas (recursivo).
        """
        r = self._session.get(f"{_BASE}/Arvore/Subtema/{subtema_id}", headers={"Accept": "application/json"}, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    @staticmethod
    def flatten_arvore(arvore: list[dict]) -> list[dict]:
        """Achata a arvore recursiva de get_arvore() numa lista plana de series
        (todos os niveis, nao so as folhas -- os nos intermediarios tambem sao
        series com valor proprio, ex: "10.03.1 Despesa total" e a soma de
        "10.03.1.1"..."10.03.1.4", mas tem sua propria serie/id).
        """
        out = []

        def _walk(nodes):
            for n in nodes:
                if n.get("id") is not None and n.get("planoContas"):
                    out.append(n)
                if n.get("seriesFilhas"):
                    _walk(n["seriesFilhas"])

        _walk(arvore)
        return out

    def get_series(self, series_id: int) -> pd.DataFrame:
        """Baixa uma serie individual via Download/{id}.

        CSV ';'-delimitado, encoding latin-1, decimal ','. Retorna date
        (Timestamp, dia 1 do mes) / value (float).
        """
        r = self._session.get(f"{_BASE}/Download/{series_id}", timeout=self.timeout)
        r.raise_for_status()
        df = pd.read_csv(io.BytesIO(r.content), sep=";", encoding="latin1", decimal=",")
        df = df.rename(columns={"Data": "date", "Valor": "value"})
        df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
        df["value"] = pd.to_numeric(df["value"])
        return df[["date", "value"]].sort_values("date").reset_index(drop=True)

    def get_series_bulk(self, series_ids: dict[str, int]) -> pd.DataFrame:
        """Baixa varias series e concatena em formato long (date, name, value).

        series_ids: {nome_amigavel: id_da_serie}. Uma chamada HTTP por serie
        (a API nao tem endpoint de download em lote) -- sleep_between evita
        martelar o servidor numa carga de centenas de series.
        """
        frames = []
        for name, series_id in series_ids.items():
            df = self.get_series(series_id)
            df["name"] = name
            frames.append(df)
            time.sleep(self.sleep_between)
        return pd.concat(frames, ignore_index=True)[["date", "name", "value"]]
