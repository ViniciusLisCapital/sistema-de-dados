# analytics/release_calendar/ — Calendário de Divulgações

Self-contained HTML report showing when Brazilian macro data is expected to be released for the rest
of 2026 — a forward-looking calendar, not a historical-values report like its `analytics/` siblings.
Same `/*REPORT_DATA*/` marker-substitution pattern (`analytics.report_structure.builder.render_report()`),
but the data source is a local YAML file, not MySQL — see
[`domain/release_calendar/CLAUDE.md`](../../domain/release_calendar/CLAUDE.md) for the schema and how
it was researched.

## Generate

```powershell
uv run python -c "from analytics.release_calendar.generate_report import run; run()"
# Output: reports/release_calendar.html
```

No DB connection needed — `generate_report.py` only reads `domain/release_calendar/calendar_2026.yaml`.
Re-run whenever that file is updated (new dates confirmed, next year's calendar added).

## Architecture

- `generate_report.py` — `_load_groups()` parses the YAML; `_flatten_entries()` denormalizes each
  group's `entries` into one flat list with institution/name/tables copied onto every row (what
  `report.html`'s timeline and table both consume directly, no lookup back into `groups` needed);
  `_recurring_groups()` pulls out groups with no dated `entries` (currently only `bcb_focus`, a weekly
  cadence rule rather than a set of specific dates).
- `report.html` — filter bar (institution pills, month pills, and a "Divulgação" dropdown listing every
  release group by name — all computed from whatever institutions/months/groups are actually present in
  the data, not hardcoded, so a future year's YAML still works unchanged), 3 stat cards (next release,
  releases this month, confirmed vs. estimated count — all computed against `reference_date`, the date
  the report was generated, not the viewer's local clock), and a table grouped by month. **No chart** —
  the "Linha do Tempo" Plotly timeline was removed 2026-08 at user request in favor of the three filters
  (institution/month/divulgação) plus the table alone; Plotly is no longer loaded by this report at all.

## Data map

| Element | Source |
|---|---|
| Table, stat cards | `domain/release_calendar/calendar_2026.yaml`'s `groups[].entries[]`, flattened |
| Recurring-releases strip | `groups[]` entries with no `entries` list (just `bcb_focus` today) |

No MySQL table is read by this report — see the parent `domain/release_calendar/` folder for why the
underlying data lives in a YAML file instead of the database (release dates are provenance/timing
metadata, not a time series with a natural DB row per observation, and change only a few times a year).

## Gotchas

- **Institution color mapping is hardcoded in `report.html`** (`INSTITUTION_COLORS`) — used for the
  table's institution badge only now (was also used by the removed timeline). If a 6th institution is
  ever added to the YAML, add its color there too or it falls back to `--muted` gray.
- **`date`/`date_end` window entries** (used for `confirmed: false` estimates) only render in the table
  now, as `"DD/MM – DD/MM"` in the date column — there's no separate window visualization since the
  timeline was removed.
- **No browser has visually confirmed this report** — same caveat as every other report in this
  project (no browser available in this sandbox). Open `reports/release_calendar.html` before trusting
  the filter/table interaction feel.

## Pending

- Add international-sourced series, `cred_ptc`, and the other gaps listed in
  `domain/release_calendar/CLAUDE.md`'s "Known gaps" once that research is done — this report will pick
  them up automatically the next time it's regenerated, no code change needed here.
- Not wired into `jobs/update_db.py` or any other routine job — this is a one-off/on-demand report, run
  manually when the calendar YAML changes.
- Open in a real browser to confirm the timeline's pan/zoom feel and that the table/chart stay in sync
  across filter changes.
