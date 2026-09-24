"""
Gerador do Calendario de Divulgacoes em HTML.

Le domain/release_calendar/calendar_2026.yaml -- config estatico, nao MySQL,
ver domain/release_calendar/CLAUDE.md para o schema e o metodo de pesquisa --
e injeta no template report.html. Mesmo padrao /*REPORT_DATA*/ dos demais
relatorios em analytics/, via analytics.report_structure.builder.render_report(),
so que a fonte de dados e um arquivo local em vez de uma tabela MySQL.

Uso:
    uv run python analytics/release_calendar/generate_report.py
    uv run python -c "from analytics.release_calendar.generate_report import run; run()"
"""

from datetime import datetime
from pathlib import Path

import yaml

from analytics.report_structure.builder import render_report

_HERE = Path(__file__).parent
_TEMPLATE = _HERE / "report.html"
_YAML_PATH = _HERE.parent.parent / "domain" / "release_calendar" / "calendar_2026.yaml"


def _load_groups() -> list[dict]:
    with open(_YAML_PATH, encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    return doc["groups"]


# Pais de uma divulgacao. Nao e um campo do YAML: e derivado das TABELAS que o grupo
# alimenta, atraves do registry -- `domain/db/brasil/...` -> BR, `us/` -> US,
# `international/` -> INT. Essa e a divisao que o proprio sistema ja usa (sao os tres
# jobs: update_db, update_us, update_international), entao ela nao pode divergir do
# banco sem que o registry mude junto.
#
# Consequencia que vale saber ANTES de estranhar: FOMC e COT saem como INT, e nao como
# US, porque as tabelas que eles escrevem (diferenciais_juros, cmb_cot_fx) sao series
# entre paises e vivem no schema international. Quem publica e americano; o dado nao e
# de um pais so.
_AREA_PAIS = {"brasil": "BR", "us": "US", "international": "INT"}

# Fallback para grupo que nao alimenta tabela nenhuma -- hoje so a Ata do Copom. Sem
# tabela nao ha de onde derivar, entao a instituicao responde; um nome novo aqui levanta
# em _paises_dos_grupos() em vez de virar um badge em branco.
_INSTITUICAO_PAIS = {
    "IBGE": "BR",
    "BCB": "BR",
    "Tesouro Nacional": "BR",
    "MTE/PDET": "BR",
    "MDIC": "BR",
    "US Federal Reserve": "US",
    "BLS": "US",
    "BEA": "US",
    "CFTC": "US",
}

_ORDEM_PAIS = ["BR", "US", "INT"]


def _paises_dos_grupos(groups: list[dict]) -> dict[str, str]:
    """{slug do grupo: "BR" | "US" | "INT"}.

    Levanta se um grupo nao puder ser classificado, ou se as tabelas dele se
    espalharem por mais de um schema -- os dois casos sao ambiguidade de verdade, e
    um badge errado no calendario nao tem sintoma nenhum.
    """
    from domain.db.registry import tabelas

    mapa = tabelas()
    fora: dict[str, str] = {}
    for g in groups:
        areas = set()
        for t in g.get("tables", []):
            modulo = mapa.get(t)
            if modulo:
                areas.add(modulo.split(".")[2])
        paises = {_AREA_PAIS[a] for a in areas if a in _AREA_PAIS}
        if len(paises) == 1:
            fora[g["group"]] = paises.pop()
            continue
        if len(paises) > 1:
            raise ValueError(
                f"grupo {g['group']!r} alimenta tabelas de mais de um pais "
                f"({sorted(paises)}) — o calendario nao tem como rotular a linha"
            )
        pais = _INSTITUICAO_PAIS.get(g["institution"])
        if not pais:
            raise ValueError(
                f"grupo {g['group']!r} nao alimenta tabela conhecida e a instituicao "
                f"{g['institution']!r} nao esta em _INSTITUICAO_PAIS — acrescente-a"
            )
        fora[g["group"]] = pais
    return fora


def _hora_brasilia(entrada: dict, grupo: dict) -> str | None:
    """`"HH:MM"` de Brasilia para a entrada, ou None se o grupo nao declara horario."""
    from datetime import date as _date

    from domain.release_calendar.sync import hora_da_entrada

    try:
        quando = _date.fromisoformat(str(entrada["date"]))
    except (KeyError, ValueError):
        quando = None
    hora = hora_da_entrada(entrada, grupo, quando)
    return hora.strftime("%H:%M") if hora else None


def _flatten_entries(groups: list[dict], paises: dict[str, str]) -> list[dict]:
    """One row per dated entry, group/institution metadata denormalized onto it --
    report.html's table and timeline both consume this flat list directly, no
    lookup back into `groups` needed at render time."""
    flat = []
    for g in groups:
        for e in g.get("entries", []):
            flat.append({
                "date": e["date"],
                "date_end": e.get("date_end"),
                "reference_period": e.get("reference_period"),
                # Hora de Brasilia, opcional. A resolucao vive no sync.py (mesma
                # funcao que decide se a divulgacao ja saiu) para as duas nao poderem
                # divergir: `time:` da entrada vence o `release_time:` do grupo, e
                # grupo com `release_time_tz` tem a hora convertida da fonte para
                # Brasilia com a data desta entrada -- o COT e o FOMC mudam de hora
                # daqui quando os EUA entram e saem do horario de verao.
                "release_time": _hora_brasilia(e, g),
                "confirmed": e.get("confirmed", True),
                "note": e.get("note"),
                "group": g["group"],
                "country": paises[g["group"]],
                "institution": g["institution"],
                "name": g["name"],
                "tables": g["tables"],
                "cadence": g["cadence"],
                "source_url": g.get("source_url"),
            })
    flat.sort(key=lambda x: x["date"])
    return flat


def _recurring_groups(groups: list[dict]) -> list[dict]:
    """Groups with no dated `entries` list -- e.g. bcb_focus, a weekly cadence
    rule (every Monday) rather than a set of specific dates. Surfaced separately
    from the timeline/table, which are both date-indexed."""
    return [
        {
            "group": g["group"],
            "institution": g["institution"],
            "name": g["name"],
            "cadence": g["cadence"],
            "weekday": g.get("weekday"),
            "note": g.get("note"),
            "source_url": g.get("source_url"),
        }
        for g in groups
        if "entries" not in g
    ]


def _load_dashboards() -> list[dict]:
    """Estado dos dashboards para a aba "Status dashboard", ou [] se nao der.

    Esta e a UNICA parte do relatorio que toca MySQL, e por isso e a unica dentro de
    try/except: o resto sai do YAML e nao tem como falhar por banco fora do ar. O que
    vai embutido e um RETRATO -- no modo servido a aba refaz a consulta em
    /api/dashboards e substitui. Sem isso, o HTML aberto por fora (ou recebido por
    email) mostraria a estrutura de dependencias com a coluna de dado vazia.
    """
    try:
        from domain.dashboards.status import estado

        return estado()
    except Exception as exc:
        print(f"  Aviso: aba Status dashboard sem estado embutido — "
              f"{type(exc).__name__}: {exc}")
        return []


def run(output: str = "reports/release_calendar.html") -> None:
    print("Carregando calendario de divulgacoes...")
    groups = _load_groups()
    paises = _paises_dos_grupos(groups)
    entries = _flatten_entries(groups, paises)
    recurring = _recurring_groups(groups)
    institutions = sorted({g["institution"] for g in groups})
    # Ordem fixa (BR, US, INT) e nao alfabetica: o seletor de pais e uma lista de tres
    # itens, e a ordem em que se pensa neles nao e a do alfabeto.
    countries = [p for p in _ORDEM_PAIS if p in set(paises.values())]
    dashboards = _load_dashboards()

    data = {
        "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "reference_date": datetime.now().strftime("%Y-%m-%d"),
        "groups": groups,
        "entries": entries,
        "recurring": recurring,
        "institutions": institutions,
        "countries": countries,
        "dashboards": dashboards,
    }
    por_pais = {p: sum(1 for g in groups if paises[g["group"]] == p) for p in countries}
    print(f"  {len(groups)} grupos, {len(entries)} divulgacoes datadas, {len(recurring)} recorrentes (sem data fixa)")
    print("  por pais: " + " · ".join(f"{p} {n}" for p, n in por_pais.items()))
    if dashboards:
        atrasados = [d["name"] for d in dashboards if d["veredito"] == "desatualizado"]
        n_deps = sum(d["n_deps"] for d in dashboards)
        print(f"  {len(dashboards)} dashboards, {n_deps} dependencias declaradas"
              + (f" — {len(atrasados)} com dado novo na fonte: {', '.join(atrasados)}"
                 if atrasados else ""))

    out = render_report(_TEMPLATE, data, output)
    print(f"Relatorio salvo: {out}")


if __name__ == "__main__":
    run()
