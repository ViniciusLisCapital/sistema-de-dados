"""
Connector para as agendas de divulgacao das fontes americanas — BLS e BEA.

Contrapartida de `connectors/bcb_agenda.py` do lado dos EUA: e daqui que saem as
datas e HORAS que `domain/release_calendar/` grava para `inflc_cpi` (CPI do BLS) e
`inflc_pce` (PCE, do release "Personal Income and Outlays" do BEA).

Exemplo de uso:

    from connectors.us_agenda import BLSAgenda, BEAAgenda, FREDReleases

    bls = BLSAgenda()
    bls.releases()                    # os 13 slugs de release com pagina propria
    bls.schedule("cpi")               # [{'reference_period': '2026-08',
                                      #   'date': date(2026, 9, 11), 'time': '08:30',
                                      #   'tz': 'America/New_York'}, ...]

    bea = BEAAgenda()
    bea.eventos(summary_starts="Personal Income and Outlays")
    # [{'date': date(2026, 9, 30), 'time': '08:30', 'tz': 'America/New_York',
    #   'reference_period': '2026-08', 'summary': 'Personal Income and Outlays, August 2026'}, ...]

    FREDReleases().dates(10)          # conferencia independente (release 10 = CPI)

--------------------------------------------------------------------------------
AS TRES FONTES, E POR QUE SAO TRES
--------------------------------------------------------------------------------
Nenhuma sozinha entrega as tres coisas que o calendario precisa (DATA + HORA +
PERIODO DE REFERENCIA). Medido ao vivo em 2026-08-26:

| fonte                              | data | hora | periodo | horizonte        |
|------------------------------------|------|------|---------|------------------|
| BLS pagina por release (.htm)      |  sim |  sim |   SIM   | ano corrente     |
| BLS feed ICS (bls.ics)             |  sim |  sim |   nao   | 2025-01 -> 2026-12 |
| BEA feed ICS                       |  sim |  sim |   SIM   | 2025-01 -> 2026-12 |
| BEA pagina de agenda (HTML)        |  sim |  sim |   SIM   | so o futuro      |
| FRED /fred/release/dates           |  sim |  NAO |   nao   | 1948 -> +4 meses |

Dai a divisao de trabalho:

* **BLS**: a pagina por release e a fonte primaria, porque e a unica das duas do BLS
  que traz a coluna "Reference Month" — o ICS do BLS so tem o NOME do release no
  SUMMARY ("Consumer Price Index", sem mes). O ICS serve para (a) conferir as datas
  e (b) cobrir releases que nao tem pagina propria.
* **BEA**: o ICS e a fonte primaria, porque o periodo de referencia vem embutido no
  proprio titulo ("Personal Income and Outlays, August 2026"). A pagina HTML tem a
  mesma informacao, mas so olhando para frente (19 eventos em 2026-08-26, contra 119
  no ICS) — serve de conferencia.
* **FRED**: independente das duas, cobre 331 releases americanos com o mesmo formato
  e tem o historico completo (953 datas de CPI desde 1948). Nao tem hora nem periodo,
  entao nunca e primaria — e a terceira opiniao, e o caminho barato para descobrir a
  agenda de uma serie nova (`release_for_series("PPIACO")` -> release_id -> datas).

--------------------------------------------------------------------------------
GOTCHAS MEDIDOS AO VIVO (2026-08-26)
--------------------------------------------------------------------------------
1. **bls.gov responde 403 a User-Agent generico** — inclusive a `www.bls.gov`, nao
   so a `download.bls.gov`. Este connector reusa o `_UA` de `connectors/bls.py`
   (mesma decisao ja tomada no projeto) em vez de inventar outro.

2. **O TZID do ICS do BLS nao e nome IANA.** O feed emite
   `DTSTART;TZID=US-Eastern:20250115T083000`, e `ZoneInfo("US-Eastern")` levanta
   `ZoneInfoNotFoundError`. O bloco VTIMEZONE do proprio arquivo declara as regras
   (2o domingo de marco / 1o domingo de novembro), que sao exatamente as de
   `America/New_York` — dai o mapa `_TZID_ALIAS`.

3. **O ICS do BEA vem em UTC, com Z, e e o "Z" que carrega o horario de verao.**
   `20260930T123000Z` e 08:30 EDT; `20261125T133000Z` e 08:30 EST. As duas sao a
   mesma hora de parede. Ler o valor como ingenuo (que e o que
   `connectors/bcb_agenda._parse_dt` faz, correto para o BCB) erraria por 4-5 horas
   e mudaria ate o DIA em alguns eventos.

4. **`APIDatasetMetaData` do BEA tem `ReleaseDate` e `NextReleaseDate` por tabela, e
   os dois estao congelados em 2019.** Medido nas 386 tabelas do dataset NIPA e nas
   do NIUnderlyingDetail: `MetaDataUpdated = 2019-03-06T10:13`, e todas dizem
   `NextReleaseDate: Mar 28 2019 8:30AM`. E o unico campo da API do BEA que parece
   ser um calendario de divulgacao, e nao e. Nao usar.

5. **A API v2 do BLS nao tem endpoint de calendario.** Os quatro que existem sao
   `timeseries/data/`, `timeseries/popular`, `surveys` e `surveys/<id>`; "Release
   Calendar" aparece so na navegacao do site. O caminho e o ICS/HTML mesmo.

6. **Nenhuma das duas fontes tinha 2027 em 2026-08-26.** Os dois ICS terminam em
   dezembro/2026 e `/schedule/2027/home.htm` responde 404. O BLS costuma publicar o
   ano seguinte no outono; ver `domain/release_calendar/ROLLOVER.md`.

7. **O DTSTAMP do ICS do BEA e inutil como sinal de frescor**: os 119 eventos, de
   2025-01 a 2026-12, carregam todos `DTSTAMP:20250923T143030Z`. O conteudo esta em
   dia (conferido evento a evento contra a pagina HTML ao vivo), so o carimbo e que
   e de geracao unica.
"""

from __future__ import annotations

import html
import logging
import os
import re
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from connectors.bls import _UA

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------- fontes

_BLS_SCHEDULE = "https://www.bls.gov/schedule/news_release"
_BLS_ICS = f"{_BLS_SCHEDULE}/bls.ics"
_BEA_ICS = "https://www.bea.gov/news/schedule/ics/online-calendar-subscription.ics"
_BEA_HTML = "https://www.bea.gov/news/schedule"
_FRED = "https://api.stlouisfed.org/fred"

# Fuso em que as duas agencias divulgam. Guardado como nome IANA para o
# `release_time_tz` do calendario resolver o horario de verao por entrada.
TZ_FONTE = "America/New_York"

# O TZID do ICS do BLS nao e nome IANA (gotcha 2 do docstring).
_TZID_ALIAS = {
    "US-Eastern": "America/New_York",
    "US/Eastern": "America/New_York",
    "Eastern Standard Time": "America/New_York",
}

_MESES = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

_TRIMESTRES = {
    "first": 1, "1st": 1, "second": 2, "2nd": 2,
    "third": 3, "3rd": 3, "fourth": 4, "4th": 4,
}

# "November 2025" / "Third Quarter 2025" / "2nd Quarter 2026"
_RE_MES_ANO = re.compile(
    r"\b([A-Z][a-z]{2,8})\.?\s+(\d{4})\b"
)
_RE_TRIMESTRE = re.compile(
    r"\b(first|second|third|fourth|1st|2nd|3rd|4th)\s+quarter\s+(\d{4})\b", re.I
)
# "Dec. 18, 2025" / "May 12, 2026"
_RE_DATA = re.compile(r"\b([A-Z][a-z]{2})\.?\s+(\d{1,2}),\s*(\d{4})\b")
# "08:30 AM" / "8:30 AM"
_RE_HORA = re.compile(r"\b(\d{1,2}):(\d{2})\s*(AM|PM)\b", re.I)


class USAgendaError(RuntimeError):
    """Falha ao obter ou interpretar uma agenda do BLS/BEA."""


# --------------------------------------------------------------------- comuns


def _sessao(user_agent: str) -> requests.Session:
    s = requests.Session()
    s.headers["User-Agent"] = user_agent
    s.headers["Accept"] = "*/*"
    retry = Retry(
        total=4,
        backoff_factor=1.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET"]),
        respect_retry_after_header=True,
    )
    s.mount("https://", HTTPAdapter(max_retries=retry))
    return s


def _unfold(texto: str) -> list[str]:
    """Desfaz o line-folding do RFC 5545 (linha continuada comeca com espaco/tab).

    O ICS do BEA dobra titulos longos no meio de uma palavra
    ("...(Advance Estima\\n te)"); sem desdobrar, o periodo de referencia — que vive
    no fim do titulo — se perde.
    """
    linhas: list[str] = []
    for raw in texto.split("\n"):
        raw = raw.rstrip("\r")
        if raw[:1] in (" ", "\t") and linhas:
            linhas[-1] += raw[1:]
        else:
            linhas.append(raw)
    return linhas


def _desescapar(valor: str) -> str:
    """Desfaz o escaping de TEXT do RFC 5545 (`\\,` `\\;` `\\n`)."""
    return (
        valor.replace("\\,", ",")
        .replace("\\;", ";")
        .replace("\\n", " ")
        .replace("\\N", " ")
        .strip()
    )


def _dt_para_ny(valor: str, params: str) -> datetime | None:
    """Converte o DTSTART de um VEVENT em datetime aware no fuso da fonte.

    Trata as tres formas que aparecem nos dois feeds:

        `20260930T123000Z`              -> UTC (BEA), convertido
        `20250115T083000` + TZID=...    -> local no fuso do TZID (BLS)
        `20260930`                      -> dia inteiro, devolve 00:00 local

    Devolve None no que nao casar, para um evento malformado nao derrubar o parse
    inteiro — o chamador conta os descartes.
    """
    valor = valor.strip()
    tzid = None
    for p in params.split(";"):
        if p.upper().startswith("TZID="):
            tzid = p.split("=", 1)[1].strip()

    try:
        if valor.endswith("Z"):
            bruto = datetime.strptime(valor[:-1], "%Y%m%dT%H%M%S")
            return bruto.replace(tzinfo=timezone.utc).astimezone(ZoneInfo(TZ_FONTE))
        if "T" in valor:
            bruto = datetime.strptime(valor, "%Y%m%dT%H%M%S")
        else:
            bruto = datetime.strptime(valor, "%Y%m%d")
    except ValueError:
        logger.warning("DTSTART ininteligivel: %r", valor)
        return None

    nome = _TZID_ALIAS.get(tzid or "", tzid or TZ_FONTE)
    try:
        return bruto.replace(tzinfo=ZoneInfo(nome))
    except Exception:
        logger.warning("TZID desconhecido (%r); assumindo %s", tzid, TZ_FONTE)
        return bruto.replace(tzinfo=ZoneInfo(TZ_FONTE))


def _parse_ics(texto: str) -> list[dict]:
    """VEVENTs de um ICS, com DTSTART ja convertido para o fuso da fonte."""
    eventos: list[dict] = []
    atual: dict | None = None
    descartados = 0

    for linha in _unfold(texto):
        if linha.startswith("BEGIN:VEVENT"):
            atual = {}
        elif linha.startswith("END:VEVENT"):
            if atual is not None:
                dt = atual.get("_dt")
                if dt is None:
                    descartados += 1
                else:
                    eventos.append(
                        {
                            "date": dt.date(),
                            "time": dt.strftime("%H:%M"),
                            "tz": TZ_FONTE,
                            "summary": atual.get("SUMMARY", ""),
                            "uid": atual.get("UID", ""),
                        }
                    )
            atual = None
        elif atual is not None and ":" in linha:
            chave, _, valor = linha.partition(":")
            nome, _, params = chave.partition(";")
            nome = nome.upper()
            if nome == "DTSTART" and "_dt" not in atual:
                atual["_dt"] = _dt_para_ny(valor, params)
            elif nome in ("SUMMARY", "UID") and nome not in atual:
                atual[nome] = _desescapar(valor)

    if descartados:
        logger.warning("%d VEVENT(s) descartados por DTSTART ilegivel", descartados)
    return eventos


def _texto_visivel(pagina: str) -> list[str]:
    """Linhas de texto de uma pagina HTML, sem script/style e sem tags."""
    t = re.sub(r"<script.*?</script>", " ", pagina, flags=re.S | re.I)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S | re.I)
    t = html.unescape(re.sub(r"<[^>]+>", "\n", t))
    return [x.strip() for x in t.split("\n") if x.strip()]


def periodo_referencia(texto: str) -> str | None:
    """Extrai um `reference_period` no formato do calendario a partir de texto livre.

    Aceita as formas que as duas agencias usam nos rotulos:

        "November 2025"          -> "2025-11"
        "Third Quarter 2025"     -> "2025-Q3"
        "2nd Quarter 2026"       -> "2026-Q2"
        "2024"                   -> None

    O ultimo caso e deliberado: `sync.periodo_para_data` so data mensal, trimestral e
    diario, entao um release anual nao gera expectativa nenhuma — que e o
    comportamento correto (nao ha o que cobrar do banco todo mes).
    """
    if not texto:
        return None

    m = _RE_TRIMESTRE.search(texto)
    if m:
        return f"{m.group(2)}-Q{_TRIMESTRES[m.group(1).lower()]}"

    for m in _RE_MES_ANO.finditer(texto):
        mes = _MESES.get(m.group(1)[:3].lower())
        if mes:
            return f"{m.group(2)}-{mes:02d}"

    return None


def _parse_data(texto: str) -> date | None:
    m = _RE_DATA.search(texto)
    if not m:
        return None
    mes = _MESES.get(m.group(1)[:3].lower())
    if not mes:
        return None
    try:
        return date(int(m.group(3)), mes, int(m.group(2)))
    except ValueError:
        return None


def _parse_hora(texto: str) -> str | None:
    m = _RE_HORA.search(texto)
    if not m:
        return None
    h = int(m.group(1)) % 12
    if m.group(3).upper() == "PM":
        h += 12
    return f"{h:02d}:{int(m.group(2)):02d}"


def _filtrar(
    eventos: list[dict],
    start: date | None = None,
    end: date | None = None,
    summary_contains: str | None = None,
    summary_starts: str | None = None,
) -> list[dict]:
    out = []
    for e in eventos:
        if start and e["date"] < start:
            continue
        if end and e["date"] > end:
            continue
        if summary_contains and summary_contains.lower() not in e["summary"].lower():
            continue
        if summary_starts and not e["summary"].lower().startswith(summary_starts.lower()):
            continue
        out.append(e)
    return sorted(out, key=lambda e: (e["date"], e["time"]))


# ------------------------------------------------------------------------ BLS


class BLSAgenda:
    """Agenda de divulgacoes do BLS: paginas por release (.htm) + feed ICS.

    A pagina por release e a fonte primaria — e a unica com o periodo de referencia.
    """

    def __init__(self, session: requests.Session | None = None, timeout: float = 60.0):
        self.session = session or _sessao(_UA)
        self.timeout = timeout
        self._cache: dict[str, str] = {}

    # ------------------------------------------------------------- descoberta

    def releases(self) -> list[str]:
        """Slugs dos releases com pagina de agenda propria.

        Lidos da navegacao lateral da propria pagina, nao de uma lista fixa: quando
        o BLS adiciona um release, ele aparece aqui sozinho. 13 em 2026-08-26 —
        cew, cewbd, cpi, ecec, eci, empsit, jolts, laus, metro, ppi, prod2, realer,
        ximpim.
        """
        pagina = self._pagina("cpi")
        achados = re.findall(r'href="/schedule/news_release/([a-z0-9_]+)\.htm"', pagina)
        return sorted(set(achados))

    # ---------------------------------------------------------------- agendas

    def schedule(self, release: str) -> list[dict]:
        """Tabela de agenda de um release: periodo de referencia + data + hora.

        A tabela e sempre de 3 colunas (`Reference Month` / `Release Date` /
        `Release Time`) — conferido ao vivo nas paginas de CPI, PPI, Employment
        Situation, JOLTS, ECI e import/export prices, inclusive nas trimestrais,
        onde a primeira coluna vira "Third Quarter 2025" sem mudar de nome.

        O horizonte e o ano corrente mais o dezembro anterior (13 linhas no CPI em
        2026-08-26: dez/2025 a nov/2026 de referencia).
        """
        linhas = _texto_visivel(self._pagina(release))
        try:
            i = linhas.index("Release Time")
        except ValueError:
            raise USAgendaError(
                f"pagina de agenda do release {release!r} sem a coluna 'Release Time' "
                "— o layout do BLS mudou ou o slug nao existe"
            ) from None

        out: list[dict] = []
        for j in range(i + 1, len(linhas) - 2, 3):
            ref, quando, hora = linhas[j], linhas[j + 1], linhas[j + 2]
            d = _parse_data(quando)
            h = _parse_hora(hora)
            if d is None or h is None:
                break  # fim da tabela: as linhas seguintes sao o rodape da pagina
            out.append(
                {
                    "reference_period": periodo_referencia(ref),
                    "reference_label": ref,
                    "date": d,
                    "time": h,
                    "tz": TZ_FONTE,
                }
            )
        if not out:
            raise USAgendaError(f"nenhuma linha de agenda lida em {release!r}")
        return out

    def eventos(self, **filtros) -> list[dict]:
        """Eventos do feed ICS geral do BLS (313 em 2026-08-26, 2025-01 a 2026-12).

        Sem periodo de referencia: o SUMMARY e so o nome do release ("Consumer Price
        Index"). Serve para conferir `schedule()` e para releases sem pagina propria.
        """
        return _filtrar(_parse_ics(self._get(_BLS_ICS)), **filtros)

    # ------------------------------------------------------------------ interno

    def _pagina(self, release: str) -> str:
        if release not in self._cache:
            self._cache[release] = self._get(f"{_BLS_SCHEDULE}/{release}.htm")
        return self._cache[release]

    def _get(self, url: str) -> str:
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return resp.text


# ------------------------------------------------------------------------ BEA


class BEAAgenda:
    """Agenda de divulgacoes do BEA: feed ICS (primario) + pagina HTML (conferencia).

    O periodo de referencia vem do proprio titulo do evento, entao o ICS basta.
    """

    def __init__(self, session: requests.Session | None = None, timeout: float = 60.0):
        self.session = session or _sessao("lis-capital-us-agenda/1.0")
        self.timeout = timeout

    def eventos(self, **filtros) -> list[dict]:
        """Eventos do ICS, com `reference_period` extraido do titulo.

        119 eventos em 2026-08-26, de 2025-01 a 2026-12. O titulo tem a forma
        "<Release>, <Periodo>" — "Personal Income and Outlays, August 2026",
        "GDP (Advance Estimate), 3rd Quarter 2026".
        """
        eventos = _parse_ics(self._get(_BEA_ICS))
        for e in eventos:
            e["reference_period"] = periodo_referencia(e["summary"])
        return _filtrar(eventos, **filtros)

    def releases(self) -> list[str]:
        """Titulos distintos de release no feed, sem o periodo.

        O equivalente do `releases()` do BLS: e daqui que se descobre o `match` de
        uma serie nova (o titulo do release do BEA, nao um slug).
        """
        nomes = set()
        for e in self.eventos():
            nomes.add(e["summary"].split(",")[0].strip())
        return sorted(nomes)

    def schedule(self) -> list[dict]:
        """Agenda da pagina HTML — so o futuro, usada como conferencia do ICS.

        A tabela tem 3 colunas na ordem (data + hora juntas) / tipo / titulo, e o
        ano so aparece no cabecalho ("Year 2026"), nao em cada linha.
        """
        pagina = self._get(_BEA_HTML)
        ano = None
        m = re.search(r"Year\s+(\d{4})", pagina)
        if m:
            ano = int(m.group(1))

        out: list[dict] = []
        for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", pagina, re.S | re.I):
            celulas = [
                html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", c))).strip()
                for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", tr, re.S | re.I)
            ]
            if len(celulas) < 3:
                continue
            quando, _tipo, titulo = celulas[0], celulas[1], celulas[2]
            hora = _parse_hora(quando)
            m = re.match(r"([A-Z][a-z]+)\s+(\d{1,2})", quando)
            if hora is None or m is None or ano is None:
                continue
            mes = _MESES.get(m.group(1)[:3].lower())
            if not mes:
                continue
            out.append(
                {
                    "date": date(ano, mes, int(m.group(2))),
                    "time": hora,
                    "tz": TZ_FONTE,
                    "summary": titulo,
                    "reference_period": periodo_referencia(titulo),
                }
            )
        if not out:
            raise USAgendaError("nenhuma linha lida da agenda HTML do BEA")
        return sorted(out, key=lambda e: (e["date"], e["time"]))

    def _get(self, url: str) -> str:
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return resp.text


# ----------------------------------------------------------------------- FRED


class FREDReleases:
    """Datas de divulgacao pelo FRED — conferencia independente e caminho de descoberta.

    331 releases americanos no mesmo formato, com historico completo (953 datas de
    CPI, a primeira em 1948) e as futuras ja agendadas. NAO tem hora nem periodo de
    referencia, entao nunca substitui BLS/BEA — mas responde "que release publica
    esta serie?" para qualquer serie do FRED, que e o caminho barato para montar a
    agenda de uma serie nova.
    """

    def __init__(self, api_key: str | None = None, timeout: float = 60.0):
        self.api_key = api_key if api_key is not None else os.environ.get("FRED_API_KEY", "")
        self.timeout = timeout
        self.session = _sessao("lis-capital-us-agenda/1.0")

    def release_for_series(self, series_id: str) -> list[dict]:
        """[{id, name}] do release a que uma serie do FRED pertence."""
        d = self._get("series/release", series_id=series_id)
        return [{"id": r["id"], "name": r["name"]} for r in d.get("releases", [])]

    def dates(
        self,
        release_id: int,
        *,
        futuras: bool = True,
        limit: int = 1000,
    ) -> list[date]:
        """Datas de divulgacao de um release, em ordem crescente.

        `futuras=True` (default) liga `include_release_dates_with_no_data`, que e o
        que traz as datas JA AGENDADAS mas ainda sem dado — sem esse parametro o
        FRED devolve so o passado. Conferido contra o ICS das agencias: as 4 datas
        futuras de CPI e as 4 de PCE batem exatamente.
        """
        d = self._get(
            f"release/dates?release_id={release_id}",
            sort_order="asc",
            limit=limit,
            include_release_dates_with_no_data="true" if futuras else "false",
        )
        return [date.fromisoformat(x["date"]) for x in d.get("release_dates", [])]

    def releases(self) -> list[dict]:
        """Catalogo de releases do FRED ([{id, name}], 331 em 2026-08-26)."""
        d = self._get("releases", limit=1000)
        return [{"id": r["id"], "name": r["name"]} for r in d.get("releases", [])]

    def _get(self, caminho: str, **params) -> dict:
        if not self.api_key:
            raise USAgendaError("FRED_API_KEY nao configurada no .env")
        sep = "&" if "?" in caminho else "?"
        url = f"{_FRED}/{caminho}{sep}api_key={self.api_key}&file_type=json"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()
