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

**Year rollover:** two things here are hardcoded to 2026 and will silently show the wrong year —
`_YAML_PATH` ([generate_report.py:24](generate_report.py#L24)) and the literal period label `Ago–Dez 2026`
([report.html:116](report.html#L116), plus the research-date note at line 171). Both are listed as steps in
[`domain/release_calendar/ROLLOVER.md`](../../domain/release_calendar/ROLLOVER.md) — read that before the
turn of the year; the recommended path (extend the window on the existing YAML rather than creating
`calendar_2027.yaml`) avoids needing to touch `_YAML_PATH` at all.

The BCB dates in that YAML are refreshed from BCB's own ICS feeds by
[`domain/release_calendar/update_calendar.py`](../../domain/release_calendar/CLAUDE.md#update_calendarpy).
Usual sequence — nothing chains them automatically:

```powershell
uv run python -m domain.release_calendar.update_calendar          # ve o drift
uv run python -m domain.release_calendar.update_calendar --write  # aplica no YAML
uv run python -c "from analytics.release_calendar.generate_report import run; run()"
```

## Update button + `serve.py` (2026-08-17)

Each release row has an **Atualizar** column that runs that release's ETL. A self-contained HTML file
can't execute Python, so one button covers two modes:

```powershell
uv run python analytics/release_calendar/serve.py          # modo servido: o botão roda o ETL
uv run python analytics/release_calendar/serve.py --port 9000 --no-browser
```

Or double-click [`abrir_calendario.bat`](../../abrir_calendario.bat) in the repo root — same thing
without the terminal, added because "do I have to type this every time?" is the obvious first
reaction. **The served page must be reached at `127.0.0.1:8765`**; double-clicking
`reports/release_calendar.html` yields file mode even while the server runs, since a `file://` page
can't call a localhost origin. That confusion has already happened once — the report's own mode badge
("modo arquivo" / "servido") exists so the answer is visible on the page instead of needing to be
explained.

- **Servido** — `serve.py` (stdlib `http.server`, no new dependency) serves the report from
  `http://127.0.0.1:8765` and exposes `GET /api/ping`, `GET /api/status`, `POST /api/run`. Clicking
  posts a group slug, the ETL runs, and the table re-renders from a fresh `/api/status` so **every row
  of that group** updates, not just the one clicked.
- **Arquivo** — opened as `file://` or emailed, the ping fails and the same button copies
  `uv run python jobs/update_db.py --group <slug>` to the clipboard. A shared report has no dead
  controls and no way to run anything on the recipient's machine. (Clipboard API needs a secure
  context, which `file://` isn't — hence the `execCommand` fallback, and a last resort that just
  displays the command to copy by hand.)

Four row states, from the release date plus `sync.py`'s verdict for the group:

| State | Shown | When |
|---|---|---|
| future | dimmed `—` | release date (or `date_end`) hasn't passed |
| late | **orange button** | released, and some table is behind → the only attention-grabbing state |
| ok | `✓ em dia` | released, data present |
| unknown | neutral button | released, but no verdict possible (file mode, DB down, or a group with no datable period like Copom/FOMC) |
| — | `sem tabela` | group feeds no table (`bcb_copom_ata`) — never offers a button |

**Security, and why each piece:** binds `127.0.0.1` only; the POST takes a **group slug and resolves
scripts through the YAML** — it never accepts a module name, path, or command from the page, and an
unknown slug is a 400; there is no shell anywhere in the path; and the `Host` header is checked, without
which any website open in the same browser could point a domain at `127.0.0.1` and fire POSTs (DNS
rebinding). All five are covered by `tests/test_serve_calendar.py`.

The slug→script resolution is [`domain/db/registry.py`](../../domain/db/CLAUDE.md) via
`jobs/update_db.py --group`; nothing about which script writes which table lives in this folder.

## Architecture

- `generate_report.py` — `_load_groups()` parses the YAML; `_flatten_entries()` denormalizes each
  group's `entries` into one flat list with institution/name/tables copied onto every row (what
  `report.html`'s table and stat cards consume directly, no lookup back into `groups` needed);
  `_recurring_groups()` pulls out groups with no dated `entries`. **Since 2026-08-17 that returns an
  empty list**: `bcb_focus` was the only member and now carries 19 itemized dates (BCB's own ICS feed
  shifts three of them off Monday for holidays, which a bare "every Monday" rule got wrong). The
  recurring strip auto-hides when empty (`report.html` checks `REPORT_DATA.recurring.length`), so no
  code change was needed — but the code path is now dormant rather than dead, and would light up again
  if a future group is added as a cadence rule without dates.
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
| Recurring-releases strip | `groups[]` with no `entries` list — **empty since 2026-08-17**, strip hidden |

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

## No longer purely forward-looking (2026-08-17)

The YAML was backfilled with the 10 BCB groups' **past** releases (May–Aug 2026), because
[`domain/release_calendar/sync.py`](../../domain/release_calendar/CLAUDE.md#syncpy--freshness-do-banco-contra-o-calendário)'s
freshness check reads the most recent release that already happened and was inert without
them. Entry count went 127 → 165. Nothing here needed changing — the month pills and
institution filters are computed from whatever is present — but the table now shows past
months, and the "próxima divulgação" stat card is still correct only because it's computed
against `reference_date`, not against the first row. The 15 non-BCB groups are still
future-only, so the past coverage is BCB-only and uneven by design, not by accident.

## Pending

- Add the remaining gaps listed in `domain/release_calendar/CLAUDE.md`'s "Known gaps" (international
  BIS/NOAA series, `atv_pib_usd`, `cmb_risco_pais`, `fisc_investimento`) once that research is done —
  this report picks them up automatically on the next regeneration, no code change needed here.
  `cred_ptc` is no longer pending: it's confirmed and charted as `bcb_ptc`.
- Not wired into `jobs/update_db.py` or any other routine job — this is a one-off/on-demand report, run
  manually when the calendar YAML changes.
- The update button's **served mode has not been confirmed in a real browser** — the interaction is
  covered by [`tests/test_release_calendar_js.js`](../../tests/test_release_calendar_js.js) (real
  script, stubbed DOM/fetch, click dispatched) and the endpoints by
  [`tests/test_serve_calendar.py`](../../tests/test_serve_calendar.py), but nobody has watched a
  button actually turn green in a browser window. Same standing caveat as every other report here.
- **A slow group blocks its own button with no progress feedback.** `POST /api/run` is synchronous, so
  `mte_caged_novo` (~50MB from the FTP, minutes) leaves the button on "rodando..." with nothing to
  watch. `ThreadingHTTPServer` means it doesn't block *other* requests, and closing the tab doesn't
  abort the run. If that becomes annoying, the fix is a job id + polling, not a timeout.
- Open in a real browser to confirm the three filters (institution/month/divulgação) compose correctly
  and the stat cards agree with the filtered table. Not yet done for the 2026-08-17 regeneration, whose
  entry count grew from ~108 to 127 and which hides the recurring strip for the first time.
