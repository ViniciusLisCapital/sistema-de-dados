"""
Connector para as APIs do Banco Central do Brasil.

APIs cobertas:
  SGS   - Sistema Gerenciador de Series Temporais (series macro: IBC-Br, CAGED, etc.)
  Focus - Expectativas de Mercado / Olinda (projecoes: IPCA, Selic, cambio, etc.)

Exemplo de uso:

    from connectors.bcb import BCB

    bcb = BCB()

    # SGS: IBC-Br SA e NSA dos ultimos 24 meses
    df = bcb.get_sgs_ultimos(
        series={"ibcbr_nsa": 24363, "ibcbr_sa": 24364},
        n=24,
    )
    # date (Timestamp), name (str), value (float)

    # SGS: por periodo
    df = bcb.get_sgs(
        series={"ibcbr_nsa": 24363, "ibcbr_sa": 24364},
        start="01/01/2022",
        end="31/12/2024",
    )

    # Focus: IPCA 12 meses (suavizado, base 0) desde 2023
    df = bcb.get_focus(
        endpoint="ExpectativasMercadoInflacao12Meses",
        indicador="IPCA",
        campos=["Data", "Media", "Mediana", "DesvioPadrao"],
        start="2023-01-01",
        filtros_extras="Suavizada eq 'S' and baseCalculo eq 0",
    )
    # date (Timestamp), media (float), mediana (float), desvio_padrao (float)

Endpoints Focus disponiveis:
    bcb.listar_endpoints_focus()
"""

from __future__ import annotations

import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Sequence

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

_SGS_BASE        = "https://api.bcb.gov.br/dados/serie/bcdata.sgs"
_SGS_ALL         = "01/01/1970"   # data sentinela: API retorna serie completa desde o inicio
_FOCUS_BASE      = "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata"
_FOCUS_PAGE_SIZE = 5_000   # maximo seguro por pagina (API suporta ate ~10k)
_SGS_MAX_WORKERS = 8       # threads para fetch paralelo de series SGS


class BCB:
    """Connector para as APIs SGS e Focus do Banco Central do Brasil."""

    def __init__(
        self,
        *,
        timeout: float = 30.0,
        session: requests.Session | None = None,
    ):
        self.timeout  = timeout
        self._session = session or _build_session()

    # -------------------------------------------------------------------------
    # SGS — Series Temporais
    # -------------------------------------------------------------------------

    def get_sgs(
        self,
        series: dict[str, int],
        start: str,
        end: str | None = None,
    ) -> pd.DataFrame:
        """Busca series do SGS em paralelo para um intervalo de datas.

        Passa start="01/01/1970" para obter a serie historica completa:
        a API retorna os dados a partir do primeiro ponto disponivel.

        Args:
            series: dict {nome_curto: codigo_sgs}.
                    Ex.: {"ibcbr_nsa": 24363, "ibcbr_sa": 24364}.
            start:  data inicial no formato "DD/MM/YYYY", ou "all" para
                    a serie historica completa desde o primeiro ponto disponivel.
            end:    data final no formato "DD/MM/YYYY". Default: data de hoje.

        Returns:
            DataFrame tidy com colunas: date (Timestamp), name (str), value (float).
        """
        from datetime import datetime
        if start == "all":
            start = _SGS_ALL
        if end is None:
            end = datetime.now().strftime("%d/%m/%Y")
        return self._fetch_sgs_parallel(
            series,
            base_params={"dataInicial": start, "dataFinal": end},
        )

    def get_sgs_ultimos(
        self,
        series: dict[str, int],
        n: int,
    ) -> pd.DataFrame:
        """Busca as ultimas N observacoes de cada serie do SGS em paralelo.

        Internamente usa o endpoint /dados?dataInicial=... porque o endpoint
        /ultimos/{n} da API SGS aceita no maximo ~24 periodos.

        Args:
            series: dict {nome_curto: codigo_sgs}.
            n:      quantidade de meses (ou pontos) mais recentes por serie.

        Returns:
            DataFrame tidy com colunas: date (Timestamp), name (str), value (float).
        """
        from datetime import datetime, timedelta
        end   = datetime.now()
        start = end - timedelta(days=n * 32)   # margem para cobrir meses completos
        return self._fetch_sgs_parallel(
            series,
            base_params={
                "dataInicial": start.strftime("%d/%m/%Y"),
                "dataFinal":   end.strftime("%d/%m/%Y"),
            },
        )

    # -------------------------------------------------------------------------
    # Focus / Olinda — Expectativas de Mercado
    # -------------------------------------------------------------------------

    def get_focus(
        self,
        endpoint: str,
        indicador: str,
        campos: Sequence[str],
        *,
        start: str | None = None,
        filtros_extras: str = "",
        orderby: str = "Data desc",
    ) -> pd.DataFrame:
        """Busca expectativas de mercado do Focus com paginacao automatica.

        Args:
            endpoint:       recurso OData. Ex.: "ExpectativasMercadoInflacao12Meses".
            indicador:      valor do filtro Indicador. Ex.: "IPCA".
            campos:         colunas a selecionar. Ex.: ["Data", "Media", "Mediana"].
                            "Data" e inserida automaticamente se ausente.
            start:          data inicial no formato ISO "YYYY-MM-DD". Opcional.
            filtros_extras: clausulas OData adicionais (sem 'and' prefixado).
                            Ex.: "Suavizada eq 'S' and baseCalculo eq 0".
            orderby:        clausula $orderby. Default: "Data desc".

        Returns:
            DataFrame com colunas em snake_case. "Data" e convertida para
            coluna "date" do tipo Timestamp. Valores numericos ja sao float.
        """
        select_fields = list(campos)
        if "Data" not in select_fields:
            select_fields.insert(0, "Data")

        filtro = f"Indicador eq '{indicador}'"
        if start:
            filtro += f" and Data ge '{start}'"
        if filtros_extras:
            filtro += f" and {filtros_extras}"

        pages: list[dict] = []
        skip = 0
        while True:
            data = self._focus_get(
                endpoint,
                top=_FOCUS_PAGE_SIZE,
                skip=skip,
                filter=filtro,
                select=",".join(select_fields),
                orderby=orderby,
                format="json",
            )
            page = data.get("value", [])
            if not page:
                break
            pages.extend(page)
            if len(page) < _FOCUS_PAGE_SIZE:
                break
            skip += _FOCUS_PAGE_SIZE

        if not pages:
            logger.warning("Focus: sem dados para %s / %s", endpoint, indicador)
            return pd.DataFrame()

        return _normalize_focus_df(pd.DataFrame(pages))

    def listar_endpoints_focus(self) -> list[str]:
        """Lista todos os recursos disponiveis na API Focus/Olinda."""
        data = self._get_json(f"{_FOCUS_BASE}?$format=json")
        return [ep["name"] for ep in data.get("value", [])]

    # -------------------------------------------------------------------------
    # Internals
    # -------------------------------------------------------------------------

    def _fetch_sgs_parallel(
        self,
        series: dict[str, int],
        base_params: dict,
        ultimos: int | None = None,
    ) -> pd.DataFrame:
        """Busca series SGS em threads paralelas e concatena resultado."""

        def fetch_one(name: str, code: int) -> pd.DataFrame:
            if ultimos is not None:
                url    = f"{_SGS_BASE}.{code}/dados/ultimos/{ultimos}"
                params = {"formato": "json"}
            else:
                url    = f"{_SGS_BASE}.{code}/dados"
                params = {"formato": "json", **base_params}

            resp = self._session.get(url, params=params, timeout=self.timeout)
            resp.raise_for_status()

            df = pd.DataFrame(resp.json())
            df["name"]  = name
            df["date"]  = pd.to_datetime(df["data"], format="%d/%m/%Y")
            df["value"] = pd.to_numeric(df["valor"], errors="coerce")
            return df[["date", "name", "value"]]

        frames: list[pd.DataFrame] = []
        failures: list[str] = []

        workers = min(_SGS_MAX_WORKERS, len(series))
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {
                pool.submit(fetch_one, name, code): name
                for name, code in series.items()
            }
            for fut in as_completed(futures):
                name = futures[fut]
                try:
                    frames.append(fut.result())
                    logger.debug("SGS OK: %s", name)
                except Exception as exc:
                    failures.append(name)
                    logger.error("SGS falha em '%s': %s", name, exc)

        if failures:
            logger.warning("SGS: %d serie(s) nao obtidas: %s", len(failures), failures)

        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    def _focus_get(self, endpoint: str, **params) -> dict:
        """Monta URL Focus com $-params literais e executa GET."""
        url = _build_focus_url(endpoint, **params)
        logger.debug("Focus GET %s", url)
        return self._get_json(url)

    def _get_json(self, url: str) -> dict:
        resp = self._session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()


# ---------------------------------------------------------------------------
# Helpers privados
# ---------------------------------------------------------------------------

def _build_session() -> requests.Session:
    s = requests.Session()
    s.headers["User-Agent"] = "lis-capital-bcb-connector/1.0"
    retry = Retry(
        total=4,
        backoff_factor=1.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET"]),
        respect_retry_after_header=True,
    )
    s.mount("https://", HTTPAdapter(max_retries=retry))
    return s


def _build_focus_url(endpoint: str, **params) -> str:
    """Constroi URL Focus com $-params literais.

    requests.get(params={}) percent-encodes '$' para '%24', o que faz a API
    OData do BCB retornar 400. A URL precisa ter '$top=...', nao '%24top=...'.
    """
    parts = [f"${k}={v}" for k, v in params.items()]
    return f"{_FOCUS_BASE}/{endpoint}?" + "&".join(parts)


_CAMEL_RE = re.compile(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")


def _to_snake(name: str) -> str:
    """Converte PascalCase ou camelCase para snake_case.

    Exemplos:
      "Media"               -> "media"
      "DesvioPadrao"        -> "desvio_padrao"
      "numeroRespondentes"  -> "numero_respondentes"
      "baseCalculo"         -> "base_calculo"
    """
    return _CAMEL_RE.sub("_", name).lower()


def _normalize_focus_df(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza DataFrame Focus: colunas para snake_case, Data para Timestamp."""
    df = df.rename(columns={c: _to_snake(c) for c in df.columns})
    if "data" in df.columns:
        df = df.rename(columns={"data": "date"})
        df["date"] = pd.to_datetime(df["date"])
    return df
