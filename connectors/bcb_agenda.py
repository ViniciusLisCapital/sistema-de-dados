"""
Connector para a agenda de divulgacoes do Banco Central do Brasil (feeds ICS).

Fonte das datas de divulgacao usadas em `domain/release_calendar/` — Copom, Focus,
notas mensais de estatisticas (fiscais / setor externo / monetarias e credito),
IBC-Br, IC-Br, PTC, RPM.

Exemplo de uso:

    from connectors.bcb_agenda import BCBAgenda

    ag = BCBAgenda()

    # Quais listas de calendario existem (29 em 2026-08)
    for item in ag.listas():
        print(item["lista"])

    # Eventos de uma lista, com janela e filtro por titulo
    eventos = ag.eventos(
        "Sondagens - PTC PEF",
        start="2026-08-01",
        end="2026-12-31",
        summary_contains="PTC",     # a lista traz PTC e PEF juntos
    )
    # [{'date': datetime.date(2026, 8, 20), 'time': '14:30',
    #   'summary': 'Pesquisa Trimestral de Condicoes de Credito - PTC'}, ...]

Detalhes tecnicos (confirmados ao vivo em 2026-08-17):
- `/api/exportarics/sitebcb/agendaics?lista=<Nome>` devolve um .ics de verdade. O
  horizonte e curto e limitado ao ANO CORRENTE na maioria das listas — medido em
  2026-08-17, 7 das 10 listas usadas pelo calendario terminavam em dez/2026; IBC-Br e
  ICBr chegavam a fev/2027; so `Reunioes do Copom` ia longe (dez/2027), porque esse
  calendario e publicado com anos de antecedencia por norma. Nao assumir 18 meses.
  **Nao** confundir com a rota `/acessoinformacao/calendariobc_ics`,
  que e SPA Angular e cujo conteudo esta morto no backend (SharePoint "File Not Found").
- Os nomes de `lista` sao enumeraveis via `/api/servico/sitebcb/calendario/catassociado`
  — nao chutar e nao pedir para o usuario ler da tela. Ver `listas()`.
- Ao contrario de outros endpoints `/api/servico/sitebcb/*` (copom/atas, rpm), estes
  **nao** exigem headers de browser: testados com User-Agent generico e sem User-Agent,
  ambos HTTP 200.
- O ICS tem que ser lido cru. Uma leitura "resumida" do feed do IBC-Br reportou
  2026-08-16 quando a data real era 2026-08-17, e resumos escondem os desvios de
  feriado (o Focus tem 3 divulgacoes que caem na terca em 2026).
"""

from __future__ import annotations

import logging
from datetime import date, datetime
from urllib.parse import quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

_BASE = "https://www.bcb.gov.br"
_ICS = f"{_BASE}/api/exportarics/sitebcb/agendaics"
_SERVICO = f"{_BASE}/api/servico/sitebcb/calendario"

# Nomes das listas do SharePoint que guardam os proprios metadados do calendario.
# Descobertos lendo o bundle Angular (calendario-card.component-*.js), que hardcoda
# identificador="calendario" + estes dois nomes.
_LISTA_CATEGORIAS = "CategoriasCalendario"
_LISTA_ASSOCIACAO = "CalendariosAssociacaoCategorias"

# Campos de VEVENT que interessam; o resto do ICS e ignorado.
_CAMPOS = ("DTSTART", "DTEND", "SUMMARY", "DESCRIPTION", "LOCATION")


class BCBAgenda:
    def __init__(self, session: requests.Session | None = None):
        self.session = session or _build_session()

    # ------------------------------------------------------------------ listas

    def categorias(self) -> list[str]:
        """Nomes das categorias do calendario (Copom, Estatisticas, ...)."""
        payload = self._get_json(
            f"{_SERVICO}/categorias", {"lista": _LISTA_CATEGORIAS}
        )
        return [c["nome"] for c in payload.get("conteudo", [])]

    def listas(self) -> list[dict]:
        """Todas as listas de calendario publicadas pelo BCB.

        Returns:
            list[dict]: `lista` (string exata a passar para `eventos()`),
                `categorias` (list[str]), `link` (pagina do assunto no site) e
                `e_evento` (True para agenda de eventos/seminarios, nao divulgacao
                de dado).
        """
        payload = self._get_json(
            f"{_SERVICO}/catassociado", {"lista": _LISTA_ASSOCIACAO}
        )
        out = []
        for item in payload.get("conteudo", []):
            out.append(
                {
                    "lista": item["lista"],
                    "categorias": [c["Title"] for c in item.get("cats") or []],
                    "link": (item.get("linkPadrao") or {}).get("Url"),
                    "e_evento": bool(item.get("eEvento")),
                }
            )
        return out

    # ------------------------------------------------------------------ eventos

    def ics(self, lista: str) -> str:
        """Texto cru do .ics de uma lista."""
        # `lista` vai na URL montada a mao: o nome tem acentos, espacos, parenteses
        # e en-dash (ex: "Indice de Commodities - Brasil (IC-Br)"), e precisa de
        # percent-encoding consistente.
        url = f"{_ICS}?lista={quote(lista)}"
        resp = self.session.get(url, timeout=60)
        resp.raise_for_status()
        resp.encoding = resp.encoding or "utf-8"
        return resp.text

    def eventos(
        self,
        lista: str,
        start: str | date | None = None,
        end: str | date | None = None,
        summary_contains: str | None = None,
    ) -> list[dict]:
        """Eventos de uma lista, ordenados por data.

        Args:
            lista: nome exato, como devolvido por `listas()`.
            start: data minima (inclusive). `None` = sem limite inferior.
            end: data maxima (inclusive). `None` = sem limite superior.
            summary_contains: filtra por substring do titulo, case-insensitive.
                Necessario quando uma lista mistura divulgacoes diferentes — a
                "Sondagens - PTC PEF" traz PTC e PEF, e a "Estatisticas
                macroeconomicas" traz 4 pesquisas trimestrais distintas.

        Returns:
            list[dict]: `date` (datetime.date), `time` ("HH:MM" ou None para
                evento de dia inteiro), `summary` (str), `date_end` (date ou None).
        """
        eventos = _parse_ics(self.ics(lista))

        lo = _coerce_date(start)
        hi = _coerce_date(end)
        needle = summary_contains.lower() if summary_contains else None

        out = [
            e
            for e in eventos
            if (lo is None or e["date"] >= lo)
            and (hi is None or e["date"] <= hi)
            and (needle is None or needle in e["summary"].lower())
        ]
        out.sort(key=lambda e: (e["date"], e["time"] or ""))
        return out

    # ------------------------------------------------------------------ interno

    def _get_json(self, url: str, params: dict) -> dict:
        resp = self.session.get(url, params=params, timeout=60)
        resp.raise_for_status()
        return resp.json()


# ---------------------------------------------------------------- parsing ICS


def _build_session() -> requests.Session:
    s = requests.Session()
    s.headers["User-Agent"] = "lis-capital-bcb-agenda/1.0"
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


def _unfold(text: str) -> list[str]:
    """Desfaz o line-folding do RFC 5545.

    Linha continuada comeca com espaco ou tab e pertence a linha anterior. Sem
    isso, um SUMMARY longo vira duas linhas e o parse perde metade do titulo.
    """
    linhas: list[str] = []
    for raw in text.split("\n"):
        raw = raw.rstrip("\r")
        if raw[:1] in (" ", "\t") and linhas:
            linhas[-1] += raw[1:]
        else:
            linhas.append(raw)
    return linhas


def _parse_dt(valor: str) -> tuple[date | None, str | None]:
    """Converte um DTSTART/DTEND em (date, "HH:MM").

    Aceita as duas formas que o BCB emite: `20260817T090000` (com TZID) e
    `20260817` (VALUE=DATE, dia inteiro). Devolve (None, None) no que nao casar,
    para o parse nao quebrar num evento malformado.
    """
    valor = valor.strip().rstrip("Z")
    try:
        if "T" in valor:
            dt = datetime.strptime(valor, "%Y%m%dT%H%M%S")
            return dt.date(), dt.strftime("%H:%M")
        return datetime.strptime(valor, "%Y%m%d").date(), None
    except ValueError:
        logger.warning("DTSTART/DTEND ininteligivel no ICS: %r", valor)
        return None, None


def _parse_ics(text: str) -> list[dict]:
    """Extrai os VEVENTs de um texto ICS."""
    eventos: list[dict] = []
    atual: dict | None = None

    for linha in _unfold(text):
        if linha.startswith("BEGIN:VEVENT"):
            atual = {}
        elif linha.startswith("END:VEVENT"):
            if atual is not None:
                d, hora = _parse_dt(atual.get("DTSTART", ""))
                if d is not None:
                    # DTEND e opcional e a maioria dos eventos do BCB nao tem —
                    # so parseia se existir, senao _parse_dt loga warning a esmo.
                    fim = _parse_dt(atual["DTEND"])[0] if "DTEND" in atual else None
                    eventos.append(
                        {
                            "date": d,
                            "time": hora,
                            "summary": atual.get("SUMMARY", "").strip(),
                            "date_end": fim if fim and fim != d else None,
                        }
                    )
            atual = None
        elif atual is not None and ":" in linha:
            chave, _, valor = linha.partition(":")
            nome = chave.split(";")[0].upper()
            if nome in _CAMPOS:
                atual.setdefault(nome, valor)

    return eventos


def _coerce_date(valor: str | date | None) -> date | None:
    if valor is None or isinstance(valor, date):
        return valor
    return date.fromisoformat(str(valor))
