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


def _flatten_entries(groups: list[dict]) -> list[dict]:
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


def run(output: str = "reports/release_calendar.html") -> None:
    print("Carregando calendario de divulgacoes...")
    groups = _load_groups()
    entries = _flatten_entries(groups)
    recurring = _recurring_groups(groups)
    institutions = sorted({g["institution"] for g in groups})

    data = {
        "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "reference_date": datetime.now().strftime("%Y-%m-%d"),
        "groups": groups,
        "entries": entries,
        "recurring": recurring,
        "institutions": institutions,
    }
    print(f"  {len(groups)} grupos, {len(entries)} divulgacoes datadas, {len(recurring)} recorrentes (sem data fixa)")

    out = render_report(_TEMPLATE, data, output)
    print(f"Relatorio salvo: {out}")


if __name__ == "__main__":
    run()
