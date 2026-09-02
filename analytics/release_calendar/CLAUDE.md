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

## Tab "Status dashboard" (2026-08-26)

The report gained a tab bar; the release table is now the first of two tabs. The second answers the
other half of the update question: the calendar button updates the **database**, and nothing was
regenerating the **reports** that read it — a release could land, the button go green, and every HTML
in `reports/` stay a week behind with no visible sign.

One card per dashboard, from
[`domain/dashboards/manifest.yaml`](../../domain/dashboards/CLAUDE.md): what it consumes, which table
each item lives in (or that it's **outside MySQL** — CSV, model artifact, YAML or live source), the
role it plays, and the last data available at the source. Verdict pill per dashboard: `em dia` /
`dado novo na fonte` / `sem stamp` / `nunca gerado`.

Both modes work off the same renderer, because `REPORT_DATA.dashboards` (embedded at generation) and
`GET /api/dashboards` (recomputed now) carry the same shape:

- **Servido** — live state, ~2s. `?live=1` also probes the external sources (FRED), one network call
  per series, which is why it's off by default.
- **Arquivo** — the snapshot from when the HTML was generated, and the hint says so. Without this the
  emailed report would show the dependency tree with an empty "último dado" column.

`_garantir_html()` generates through `status.gerar()` rather than `run()` so the calendar stamps
itself — otherwise its own row would sit permanently in "sem stamp".

**Each card has its own Regerar button** (`POST /api/gerar`, same key-allowlist shape as
`/api/run`'s slug allowlist — the page never sends a module path). One dashboard at a time, by
explicit decision: **there is no "regenerate all stale" control anywhere**, and a test enforces
its absence. The POST returns the regenerated dashboard's new state row only, so the card flips
to "em dia" without re-querying the other ten. In file mode the same button copies
`uv run python -m domain.dashboards.status --gerar <key>`.

So the two tabs split the work the way the update actually happens: **tab 1 updates the data
that was released, tab 2 regenerates whichever dashboards you care about right now.**

**Regerar also RECALCULATES (2026-08-31).** Direct user request, after the three-button version
of this — a per-procedure "Rodar" button — was judged confusing: *"Eu quero apenas dois botoes:
(i) Atualizar os dados na base de dados (ii) regenerar o dashboard (trazendo os dados novos,
recalculando as metricas, tudo que houver para atualizar e recalcular)."* So `status.gerar()`
now runs, before generating, whatever `procedures:` the manifest declares as **behind** — a model
estimation, a backtest — and `POST /api/gerar` returns in `procedimentos` what it ran, which the
card prints ("refez X (50.5s) e regerou em 15.8s"). The block inside the card is read-only:
it says what will be redone and how long that costs, so the button's time is announced before the
click (`~Xs para regerar (Ys de geração + Zs de recálculo)`).

What keeps this from becoming "run everything, always" is the `granularidade` of each step (see
[`domain/dashboards/CLAUDE.md`](../../domain/dashboards/CLAUDE.md)): the quarterly panel only falls
behind when a new quarter opens, so a typical click on Monetary Policy is ~55s of recalculation,
and once a quarter it is ~6 min. A step that fails does not block generation — the report comes
out with the old artifact and the card says so, in red.

### The card's prose is product text, not our conversation (2026-09-01)

Direct user correction, from a screenshot of the Monetary Policy card: *"você está transferindo
nossa conversa daqui para o dash, e eu não quero isso. Lá deve ser a explicação do que está
acontecendo ali, para alguém que nunca viu o dashboard."* And, on the procedures block's own
heading: *"'O Regerar refaz antes de gerar · nada atrasado' isso não significa nada."*

They were right, and the defect was systematic rather than one bad sentence: the notes and labels
had been written **in the same session that built the mechanism**, so they inherited its
vocabulary — `generate_report`, `procedures`, `granularidade`, "Desde 2026-08-31", "Segundos não
medidos". Every one of those is true and none answers the question the reader has.

Rewritten: the manifest's 10 `note:` fields, the procedures block heading and note, each step's
metadata line, all three `procVeredito()` verdicts, the tab's mode hint, and the freshness strip in
the monetary policy report. The four substitutions that cover almost every edit are written up in
[`.claude/rules/lis-dashboards.md`](../../.claude/rules/lis-dashboards.md) and were promoted into
the `lis-dashboard` skill; the two worth remembering here:

- **A mechanism's name is not an explanation of it.** `cada trimestre` was the *unit of comparison*
  between the step's cut and the source. It now reads "fica velho quando abre um trimestre novo",
  which is the same fact in the form that is useful. The word `granularidade` no longer appears on
  the page, and an assertion enforces that.
- **The block's heading names what the block contains** — "O que este dashboard calcula por conta
  própria" — and its note explains the *problem* (a number computed from older data than the
  database already has stays old inside a brand-new file) instead of the procedure.

The guard is what prevents relapse, and it is cheap: prose was the only content of the card that no
assertion looked at. `tests/test_release_calendar_js.js` pulls the `.dash-note`/`.proc-note`/
`.proc-hint` blocks out of the rendered HTML and rejects a term list. It runs **only in MODE=file**,
where the cards come from the real embedded payload — so it covers what is written in
`manifest.yaml`, not just what the template assembles — and it was verified against a mutant that
re-injects the old sentence.

### A second dashboard got its own recalculation step (2026-09-01)

User asked to extend the `procedures:` pilot to the other dashboards, "like the monetary policy one".
The survey is the result worth recording: of the 12 dashboards, **two** have a step to declare —
monetary policy's three (panels, estimation, forecast) and **inflation's one**, which is a *fetch*
rather than a calculation. `data/ipca_bcb_series.csv` is the only input that report reads from outside
MySQL, so **neither button reached it**: Atualizar writes to the database, and the generator only
reads. It was a month behind when measured (file through 2026-07, `inflc_decomposicao` already at
2026-08), invisible on every screen. Regerar now re-fetches it in ~18s when it is behind.

The other ten legitimately have nothing: they read the database and compute in-process, so the honest
card is the one they already show, with no block. Câmbio is the interesting near-miss — its two Ridge
caches are now **declared as dependencies** (they never were), but deliberately not as steps; the
reasons, including a `min`-vs-`max` trap that would have made a step recalculate forever, are in
[`analytics/brasil/exchange_rate/CLAUDE.md`](../brasil/exchange_rate/CLAUDE.md).

### The console encoding could fail a Regerar, and did (2026-09-01)

Found while wiring that step. `serve.py` inherits the console's encoding, and the Windows console
`abrir_calendario.bat` opens is **cp1252** — so a progress `print` carrying a character it cannot
encode raises `UnicodeEncodeError` *inside* the generator. The inflation report's own summary prints
an arrow (U+2192), which means clicking Regerar on that card returned an error and did not rebuild
the file, **for a reason with nothing to do with the data**.

Measured both ways: `status.gerar('brasil_inflation')` in a cp1252 shell dies on `'\u2192'`; with
`PYTHONIOENCODING=utf-8` it finishes in 19.9s. Fixed at the layer that owns the process's streams —
`utils/console.stdout_utf8()`, called first in `main()`, reconfigures stdout/stderr to UTF-8 with
`errors="replace"`, because a character the terminal cannot draw must never cost the operation.
Verified through the real server: `POST /api/gerar` for `brasil_inflation` returned ok in 17.8s with
zero tracebacks.

**Three entry points needed it, not one**, and the other two were already broken before this round:
`jobs/update_db.py` regenerates the dashboards it affects (since 2026-08-28), so
`--group ibge_ipca` finished the ETL and then died in the regeneration; `status.py --gerar` the same.
A test asserts all three call it, since the failure only shows up in a real cp1252 console.

## Pending

- Add the remaining gaps listed in `domain/release_calendar/CLAUDE.md`'s "Known gaps" (international
  BIS/NOAA series, `atv_pib_usd`, `cmb_risco_pais`, `fisc_investimento`) once that research is done —
  this report picks them up automatically on the next regeneration, no code change needed here.
  `cred_ptc` is no longer pending: it's confirmed and charted as `bcb_ptc`.
- Not wired into `jobs/update_db.py` or any other routine job — this is a one-off/on-demand report, run
  manually when the calendar YAML changes.
- **Confirmed in a real browser (2026-08-26)** — cards, dependency table and the Regerar button in
  served mode. What that round also caught: the button's label was following `DASH.ao_vivo` (did the
  state load?) instead of `LIVE.on` (is there a server?). The two only diverge when `/api/dashboards`
  fails on a served page — the button fell back to "Copiar cmd" and the hint said "modo arquivo",
  both wrong, while `/api/gerar` was up the whole time. Fixed, and the mode hint now has three
  states instead of two. Regression covered by the "SERVIDO SEM ESTADO" section of
  `tests/test_release_calendar_js.js`. Still unconfirmed visually: the two filter pill rows and the
  file-mode clipboard fallback.
- **Chaining the two tabs was considered and rejected** (2026-08-26): one click that updates a group
  *and* regenerates everything it feeds. The user wants to pick which dashboards get rebuilt, so the
  calendar button stays data-only. Don't "helpfully" add it back.
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
