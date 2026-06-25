"""Cliente para a API de Agregados do IBGE v3.

Doc oficial: https://servicodados.ibge.gov.br/api/docs/agregados?versao=3

Exemplo de uso:

    from connectors.ibge2 import IBGE

    ibge = IBGE()

    df = ibge.get(
        agregado=8888,
        variaveis=12606,
        localidades={"N1": "all"},
        classificacoes={544: "all"},
        periodos="last:24",
    )

Saida (DataFrame tidy, ja tipado):

    date        localidade_id  localidade_nome  variavel_id  variavel_nome   unidade        class_1_id  class_1_nome       value
    2024-01-01  1              Brasil           12606        PIMPF - ...     Numero-indice  129314      1 Industria geral  93.75
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence, Union

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

BASE_URL = "https://servicodados.ibge.gov.br/api/v3/agregados"

_NA_SENTINELS = {"...", "..", "-", "X"}

_FREQ_BY_D2N = {
    "Mes": "mensal",
    "Mês": "mensal",
    "Trimestre": "trimestral",
    "Trimestre Movel": "mensal",
    "Trimestre Móvel": "mensal",
    "Semestre": "semestral",
    "Ano": "anual",
}

ListaIds = Union[str, int, Sequence[int]]  # "all", int, ou lista de ints


# ---------------------------------------------------------------------------
# Metadados
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Metadados:
    id: int
    nome: str
    pesquisa: str
    assunto: str
    frequencia: str               # mensal | trimestral | semestral | anual
    inicio: str
    fim: str
    niveis_territoriais: list[str]
    variaveis: dict[int, dict]
    classificacoes: dict[int, dict]
    raw: dict


# ---------------------------------------------------------------------------
# Cliente principal
# ---------------------------------------------------------------------------

class IBGE:
    """Cliente parametrico para a API de Agregados do IBGE v3."""

    def __init__(
        self,
        *,
        timeout: float = 30.0,
        session: requests.Session | None = None,
    ):
        self.timeout = timeout
        self._session = session or _build_session()
        self._meta_cache: dict[int, Metadados] = {}

    # -------- High-level --------------------------------------------------

    def get(
        self,
        agregado: int,
        variaveis: ListaIds,
        *,
        periodos: Union[str, int, tuple[int, int]] = "last:6",
        localidades: Mapping[str, ListaIds] | None = None,
        classificacoes: Mapping[int, ListaIds] | None = None,
    ) -> pd.DataFrame:
        """Retorna DataFrame tidy ja tipado.

        Args:
            agregado: ID do agregado (ex.: 8888 = PIM Producao Fisica).
            variaveis: ID, lista de IDs, ou "all".
            periodos: aceita formatos:
                - "last:N" ou int N  ->  ultimos N periodos
                - "all"              ->  serie historica completa
                - "YYYYMM-YYYYMM"    ->  range explicito
                - (ano_ini, ano_fim) ->  range em anos; sufixo inferido da frequencia
            localidades: dict {nivel: ids}. Ex.: {"N1": "all"}, {"N3": [33, 35]}.
                Default: {"N1": "all"} (Brasil).
            classificacoes: dict {id_classificacao: ids_categoria_ou_"all"}.

        Returns:
            DataFrame com colunas: date, localidade_id, localidade_nome,
            variavel_id, variavel_nome, unidade, class_1_id, class_1_nome,
            class_2_id, ..., value.
        """
        localidades = localidades or {"N1": "all"}
        # Tupla (ano_ini, ano_fim) precisa da frequencia para gerar YYYYMM-YYYYMM.
        # Se nao estiver em cache, busca os metadados antes de formatar o periodo.
        if isinstance(periodos, tuple):
            freq = self._frequencia_or_none(agregado) or self.metadados(agregado).frequencia
        else:
            freq = self._frequencia_or_none(agregado)
        periodos_str = _format_periodos(periodos, freq)

        url = (
            f"{BASE_URL}/{agregado}"
            f"/periodos/{periodos_str}"
            f"/variaveis/{_format_id_list(variaveis)}"
        )
        params: dict[str, str] = {
            "view": "flat",
            "localidades": _format_localidades(localidades),
        }
        if classificacoes:
            params["classificacao"] = _format_classificacoes(classificacoes)

        payload = self._get_json(url, params=params)
        return _parse_flat(payload)

    def metadados(self, agregado: int) -> Metadados:
        """Metadados do agregado (cached em memoria)."""
        if agregado in self._meta_cache:
            return self._meta_cache[agregado]
        raw = self._get_json(f"{BASE_URL}/{agregado}/metadados")
        meta = Metadados(
            id=raw["id"],
            nome=raw["nome"],
            pesquisa=raw["pesquisa"],
            assunto=raw["assunto"],
            frequencia=raw["periodicidade"]["frequencia"],
            inicio=str(raw["periodicidade"]["inicio"]),
            fim=str(raw["periodicidade"]["fim"]),
            niveis_territoriais=raw["nivelTerritorial"]["Administrativo"],
            variaveis={v["id"]: v for v in raw["variaveis"]},
            classificacoes={c["id"]: c for c in raw["classificacoes"]},
            raw=raw,
        )
        self._meta_cache[agregado] = meta
        return meta

    def periodos_disponiveis(self, agregado: int) -> list[str]:
        return [p["id"] for p in self._get_json(f"{BASE_URL}/{agregado}/periodos")]

    def localidades(self, agregado: int, nivel: str) -> list[dict]:
        return self._get_json(f"{BASE_URL}/{agregado}/localidades/{nivel}")

    def listar_variaveis(self, agregado: int) -> pd.DataFrame:
        """Tabela amigavel das variaveis disponiveis no agregado."""
        meta = self.metadados(agregado)
        return pd.DataFrame(meta.variaveis.values())

    def listar_classificacoes(self, agregado: int) -> pd.DataFrame:
        """Tabela achatada das classificacoes e categorias."""
        meta = self.metadados(agregado)
        rows = []
        for cls in meta.classificacoes.values():
            for cat in cls["categorias"]:
                rows.append({
                    "classificacao_id": cls["id"],
                    "classificacao_nome": cls["nome"],
                    "categoria_id": cat["id"],
                    "categoria_nome": cat["nome"],
                    "nivel": cat.get("nivel"),
                })
        return pd.DataFrame(rows)

    # -------- Low-level ---------------------------------------------------

    def _get_json(self, url: str, *, params: dict | None = None):
        logger.debug("GET %s params=%s", url, params)
        resp = self._session.get(url, params=params, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def _frequencia_or_none(self, agregado: int) -> str | None:
        """Retorna frequencia se ja cached. Nao faz request caso contrario."""
        m = self._meta_cache.get(agregado)
        return m.frequencia if m else None


# ---------------------------------------------------------------------------
# Session com retry e UA
# ---------------------------------------------------------------------------

def _build_session() -> requests.Session:
    s = requests.Session()
    s.headers["User-Agent"] = "lis-capital-ibge-connector/1.0"
    retry = Retry(
        total=6,
        backoff_factor=1.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET"]),
        respect_retry_after_header=True,
    )
    s.mount("https://", HTTPAdapter(max_retries=retry))
    return s


# ---------------------------------------------------------------------------
# Formatters de URL
# ---------------------------------------------------------------------------

def _format_periodos(p, freq: str | None) -> str:
    """Aceita varios formatos e retorna a string que vai na URL."""
    if isinstance(p, int):
        return f"-{p}"
    if isinstance(p, tuple) and len(p) == 2:
        y1, y2 = p
        if freq is None or freq == "anual":
            return f"{y1}-{y2}"
        # "trimestral móvel" (PNAD) usa formato YYYYMM igual ao mensal
        sufixo_fim = {
            "mensal": "12", "trimestral": "04",
            "semestral": "02", "trimestral móvel": "12",
        }[freq]
        return f"{y1}01-{y2}{sufixo_fim}"
    if isinstance(p, str):
        if p == "all":
            return "all"
        if p.startswith("last:"):
            return f"-{int(p.split(':', 1)[1])}"
        return p
    raise ValueError(f"periodos invalido: {p!r}")


def _format_id_list(v: ListaIds) -> str:
    if v == "all":
        return "all"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, Iterable):
        return "|".join(str(x) for x in v)
    raise ValueError(f"valor invalido: {v!r}")


def _format_localidades(loc: Mapping[str, ListaIds]) -> str:
    return "|".join(f"{nivel}[{_format_ids_bracket(v)}]" for nivel, v in loc.items())


def _format_classificacoes(cls: Mapping[int, ListaIds]) -> str:
    return "|".join(f"{cid}[{_format_ids_bracket(v)}]" for cid, v in cls.items())


def _format_ids_bracket(v: ListaIds) -> str:
    if v == "all":
        return "all"
    if isinstance(v, int):
        return str(v)
    return ",".join(str(x) for x in v)


# ---------------------------------------------------------------------------
# Parser da resposta view=flat
# ---------------------------------------------------------------------------

_PARSER_MENSAL = lambda c: pd.Timestamp(year=int(c[:4]), month=int(c[4:6]), day=1)
_PARSER_TRIM = lambda c: pd.Timestamp(
    year=int(c[:4]),
    month={1: 1, 2: 4, 3: 7, 4: 10}[int(c[4:6])],
    day=1,
)
_PARSER_SEM = lambda c: pd.Timestamp(
    year=int(c[:4]),
    month={1: 1, 2: 7}[int(c[4:6])],
    day=1,
)
_PARSER_ANUAL = lambda c: pd.Timestamp(year=int(c), month=1, day=1)

_DATE_PARSERS = {
    "mensal": _PARSER_MENSAL,
    "trimestral": _PARSER_TRIM,
    "semestral": _PARSER_SEM,
    "anual": _PARSER_ANUAL,
}


def _parse_flat(payload: list[dict]) -> pd.DataFrame:
    """Converte resposta view=flat em DataFrame tidy ja tipado."""
    if not payload:
        logger.warning("IBGE retornou payload vazio")
        return pd.DataFrame()

    header, *rows = payload
    if not rows:
        logger.warning("IBGE retornou apenas o cabecalho (sem dados)")
        return pd.DataFrame()

    freq = _infer_frequencia(header)
    parse_date = _DATE_PARSERS[freq]

    n_dims = _count_dimensoes(header)

    records = []
    for row in rows:
        rec = {
            "date": parse_date(row["D2C"]),
            "localidade_id": row["D1C"],
            "localidade_nome": row["D1N"],
            "variavel_id": int(row["D3C"]),
            "variavel_nome": row["D3N"],
            "unidade": row.get("MN"),
            "value": _parse_value(row.get("V")),
        }
        # D4+ sao classificacoes; renomeia para class_1, class_2, ...
        for i in range(4, n_dims + 1):
            ord_ = i - 3
            rec[f"class_{ord_}_id"] = row[f"D{i}C"]
            rec[f"class_{ord_}_nome"] = row[f"D{i}N"]
        records.append(rec)

    return pd.DataFrame(records)


def _infer_frequencia(header: dict) -> str:
    """Le D2N do cabecalho ('Mes', 'Trimestre', 'Semestre', 'Ano') e mapeia."""
    label = (header.get("D2N") or "").strip()
    freq = _FREQ_BY_D2N.get(label)
    if freq is None:
        # tenta sem acento como fallback
        normalized = re.sub(r"[-￿]", lambda m: m.group(), label)
        for k, v in _FREQ_BY_D2N.items():
            if k.lower() in normalized.lower():
                return v
        raise ValueError(f"Frequencia nao reconhecida no cabecalho D2N='{label}'")
    return freq


def _count_dimensoes(header: dict) -> int:
    """Conta quantas dimensoes D{i}C existem no cabecalho."""
    i = 1
    while f"D{i}C" in header:
        i += 1
    return i - 1


def _parse_value(v) -> float | None:
    if v is None or v in _NA_SENTINELS:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Compatibility shims for legacy scripts (ipca.py, ipca15.py)
# ---------------------------------------------------------------------------

def ibge_get(url: str, start_year: int, end_year: int, freq: str) -> pd.DataFrame:
    """Legacy compatibility: fills the period into a pre-built IBGE URL and returns
    a DataFrame with the old column format (variavel, localidade, Class_0, dt, serie)."""
    if freq == "M":
        period = f"{start_year}01-{end_year}12"
    elif freq == "Q":
        period = f"{start_year}01-{end_year}04"
    elif freq == "A":
        period = f"{start_year}-{end_year}"
    else:
        period = f"{start_year}01-{end_year}12"

    filled_url = url.replace("/periodos//", f"/periodos/{period}/")
    if "view=" not in filled_url:
        sep = "&" if "?" in filled_url else "?"
        filled_url += f"{sep}view=flat"

    session = _build_session()
    resp = session.get(filled_url, timeout=120)
    resp.raise_for_status()
    payload = resp.json()

    if not payload or len(payload) < 2:
        return pd.DataFrame(columns=["variavel", "localidade", "Class_0", "dt", "serie"])

    header, *rows = payload
    n_dims = _count_dimensoes(header)

    records = []
    for row in rows:
        rec = {
            "variavel": row.get("D3N"),
            "localidade": row.get("D1N"),
            "dt": row.get("D2C"),
            "serie": row.get("V"),
        }
        for i in range(4, n_dims + 1):
            rec[f"Class_{i - 4}"] = row.get(f"D{i}N")
        records.append(rec)

    return pd.DataFrame(records)


def TratarDataIbge(series: pd.Series, freq: str) -> pd.Series:
    """Legacy compatibility: converts IBGE period code strings to Timestamps."""
    if freq == "M":
        return pd.to_datetime(series.astype(str), format="%Y%m", errors="coerce")
    if freq == "Q":
        def _parse_q(s):
            try:
                y, q = int(str(s)[:4]), int(str(s)[4:6])
                return pd.Timestamp(year=y, month={1: 1, 2: 4, 3: 7, 4: 10}[q], day=1)
            except Exception:
                return pd.NaT
        return series.apply(_parse_q)
    if freq == "A":
        return pd.to_datetime(series.astype(str), format="%Y", errors="coerce")
    return series
