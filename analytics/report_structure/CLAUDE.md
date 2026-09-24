# analytics/report_structure/ — Shared report-generation scaffolding

Build-time-only building blocks for the `/*REPORT_DATA*/`-template reports (`exchange_rate/`, `inflation/`) — extracted 2026-08 to stop hand-copy-pasting the same boilerplate into each new report. **Nothing here is ever loaded at runtime by a generated report** — `report.html` files stay plain, self-contained HTML/CSS/JS with no reference to this package. Only each project's own `generate_report.py` imports from it, at generation time, to assemble the final file. This preserves the "one emailable file" property `.claude/rules/lis-dashboards.md` and each report's own `CLAUDE.md` already document.

## What's here

| File | Contains | Marker it fills |
|---|---|---|
| `builder.py` | `render_report(template_path, data, output_path, extra_markers=None)` — reads the template, JSON-serializes `data`, substitutes markers, writes the output, **records the report's provenance** (see below), returns the resolved `Path` | — |
| `theme.css` | The shared LIS brand `:root` palette + universal reset/body rules (`--lis-azul`, `--lis-dourado`, etc. — see `project_lis_brand_colors` memory for the canonical hex values) | `/*THEME_CSS*/` |
| `y_autofit.js` | `_bindYAutofit()`/`_toComparableX()` — the Plotly rangeselector Y-refit helper described in `.claude/rules/lis-dashboards.md`'s "Plotly setup" section | `/*Y_AUTOFIT_JS*/` |
| `chart_head.css` / `chart_head.js` | The 3-line header every chart carries inside its own card — `describeChart(divId, traces, bits, unit, opts)`, `_ensureChartFrame()`, `fmtPeriodo()`. Added 2026-09-14, when a repo-wide sweep found five reports with no chart header at all | `/*CHART_HEAD_CSS*/`, `/*CHART_HEAD_JS*/` |
| `tree_helpers.py` | `leaf()`/`group()`/`direct()` — the node builders every hierarchical-table tab uses to assemble its `{key, label, seriesKey, children}` tree. **Not a marker: a plain runtime import**, unlike the other three files here | — (imported, not substituted) |

`render_report()` always substitutes `/*REPORT_DATA*/`; it only touches `/*THEME_CSS*/`/`/*Y_AUTOFIT_JS*/` if the template actually contains those markers, so a report can adopt one piece without adopting all of them.

`extra_markers` (added 2026-08 for `exchange_rate/`) covers templates with more than one JSON payload: `{"PPP_DATA": payload_or_None}` fills `/*PPP_DATA*/` with that payload's JSON, or the literal `null` when the value is `None`, so a section whose data wasn't built this run still has something valid to check against. Unlike `/*REPORT_DATA*/`, these substitute the **bare JSON value** — the template owns the `const X = ...;` declaration. Markers absent from the template are skipped silently, so passing a marker a report doesn't have is harmless.

**A marker the template declares and nobody substitutes is a syntax error, not an empty section** (`const X = /*X*/;` → `const X = ;`). If a report can skip building a payload, it must still pass that marker as `None`.

`tree_helpers.py` is the one exception to "build-time only" (see the last section): it's imported
normally at generation time, not pasted into a template. It landed here in 2026-08 with the
country-first rename — it had been living in `analytics/credit/` while `fiscal_policy/` and
`labor_market/` imported it across folders, which stopped being tenable once a `us/` branch could
need the same builders without reaching into `brasil/credit/`. The deflation/STL/growth transforms
did **not** move with it: `brasil/credit/transforms.py` chains an IPCA index and divides by a BCB
`atv_pib_mensal` denominator, so it is Brazil-specific by construction — a US report needs its own,
built on CPI.

## How a report uses it

In `report.html`, replace the old inline block with the marker, inside the same `<style>`/`<script>` tag it always lived in:

```html
<style>
  /*THEME_CSS*/
  /* ...report-specific CSS below, unchanged... */
</style>
...
<script>
  /*Y_AUTOFIT_JS*/
  // ...report-specific JS below, unchanged...
</script>
```

In `generate_report.py`, replace the manual `template.read_text()` / `json.dumps()` / `str.replace()` / `write_text()` sequence with:

```python
from analytics.report_structure.builder import render_report

def run(output: str = "reports/xxx.html") -> None:
    data = {...}
    out = render_report(_TEMPLATE, data, output)
    print(f"Relatorio salvo: {out}")
```

## Migration status

- **`inflation/`** — fully migrated 2026-08 (the pilot for this convention). Both markers (`/*THEME_CSS*/`, `/*Y_AUTOFIT_JS*/`) plus the `render_report()` harness.
- **`exchange_rate/`** — partially migrated 2026-08: `/*Y_AUTOFIT_JS*/` and the `render_report()` harness are in use, plus `extra_markers=` (the only report using it — its three model tabs, fused in from the ex-standalone PPP dashboard, carry their own payload markers). The `/*Y_AUTOFIT_JS*/` swap was verified byte-for-byte equivalent to the prior inline copy, including the `t.type === 'heatmap'` guard this report actually needs — `y_autofit.js` was widened to include that guard unconditionally, a no-op for `inflation/` since it never binds `_bindYAutofit` to a heatmap trace). **Theme CSS is deliberately NOT migrated** — `exchange_rate/report.html`'s `:root` predates the 2026-07 LIS-dashboard reskin (`inflation/CLAUDE.md`'s "Visual design"): navy header, `system-ui` font, no Barlow/JetBrains Mono import, different `--bg`/`--border`/`--text` values than `theme.css`. Swapping in `/*THEME_CSS*/` as-is would silently change the report's look without an actual design pass — that reskin is its own follow-up; do it, then point at the shared file.
- **`monetary_policy/`** — the old `report.html` (BCB-model replication) was deleted in 2026-08 without ever being migrated. The **new** one, scaffolded 2026-08-21, was built directly onto both markers plus `render_report()` — same as `economic_activity/`/`fiscal_policy/`, no migration step.
- **`economic_activity/`** — built directly onto both markers from day one (2026-08), the first report to start here rather than migrate here — no separate migration step was ever needed.
- **`fiscal_policy/`** — same as `economic_activity/`: built directly onto both markers from day one (2026-08), no migration needed.

## `chart_head.js` — what each report still owns

The shared file carries the *mechanism*; the report keeps the two things that are its own:

- **`CHART_META = {divId: {title, source}}`**, declared by the report. The shared file
  deliberately does not declare it, so the two can be inlined in any order without one
  overwriting the other (`_chMeta()` reads it through a `typeof` guard).
- **The call**, from inside the same function that redraws the chart, with the traces it
  just plotted and the **same string it gave the Y axis** as `unit`. Passing the unit
  rather than reading it back is what keeps axis and subtitle from drifting; passing a
  second copy of the string at the call site is what would let them drift, so each report
  routes the call through a one-line local wrapper that takes `yTitle` from the renderer.

`opts` covers what varies: `titulo` (a chart whose metric is a selector must derive its
title too — a fixed one starts lying on the first click), `fonte`, `freq`
(`mes`/`tri`/`ano`/`dia` — a quarterly axis labelled by month announces a month the chart
does not show), `compact` (a small panel inside a card that already names the variable),
`fmt` (a report in English passes its own month names) and `periodo` (a chart whose X is
**not** time: deriving the window from the abscissas would print a range of *values* on
the source line, read as if it were a period).

**A card whose markup already carries a `.chart-head` is reused, not given a second one** —
that is how `expectations`'s Boletim chart keeps the definition button on its title while
every other chart in the file goes through the shared path.

**Read the children through `Array.prototype.slice.call()`, never `card.children.filter()`.**
Both scans in `_ensureChartFrame()` (the one that finds a ready-made `.chart-head`, and the
one that picks its three lines out) walk a **live DOM collection**, and a browser's
`HTMLCollection` has no `Array` methods at all. Calling `.filter()` on it threw `TypeError`
on the first chart of every page from 2026-09-14 to 2026-09-17, so `describeChart()` never
wrote a single header — measured in Chrome, not inferred. The fix is `slice.call`, which
behaves identically on an `HTMLCollection` and on the plain `Array` the test harness used to
hand it. Full account, including why no test caught it: `.claude/rules/lis-dashboards.md`.

Coverage is enforced by `tests/test_chart_head_js.js`, which executes this file against a
fake DOM **and sweeps `analytics/**/report.html`** for a report that plots but has no
header. The sweep exists because the first time this rule was promoted the migration list
was written from memory and missed five reports — see `.claude/rules/lis-dashboards.md`.

Since 2026-09-17 that harness also guards the *instrument*: its stub returns an
`HTMLCollection`-shaped object for `children` (indexed + `length`, no `Array` methods), and
§1a asserts that it does — because while the stub handed back a real `Array`, every
assertion passed green against a page that threw on load. §4 adds the static half, scanning
`report_structure/*.js` and every `report.html` for an `Array` method on a live DOM
collection, with `NodeList` (has `forEach`) and `HTMLCollection` (has nothing) told apart.

## `render_report()` also records the report's provenance (2026-09-23)

After writing the file, `_registrar_procedencia()` records *what data the report was built
with* — the last observation of each declared dependency at that moment. That record is what
`domain/dashboards/status.py` compares against later to answer "is this report behind?"; the
file's own mtime says when it was written, never what was inside it.

**It lives here because this is the one place every HTML report passes through.** Until
2026-09-23 the record was written by `status.gerar()` — a separate step, taken only if the
report was generated *that* way, while the command documented in 10 of the 13 folder
`CLAUDE.md` files is `generate_report.run()`. Measured that day: 8 of 13 delivered reports had
no record or one from a different generation, so the status tab could not say anything about
most of the list. Full account, including the second half of the bug (a stale record being
used to accuse a report of missing data it already had):
[`domain/dashboards/CLAUDE.md`](../../domain/dashboards/CLAUDE.md).

Three properties worth knowing before touching that function:

- **It runs after `write_text`, never before** — the record stores the written file's
  `st_mtime_ns`, which is what later answers "is this record about *this* file?".
- **It never raises.** The record needs the database; a database that is down cannot cost the
  report, which is already on disk. Failure prints a line and the verdict degrades to "can't
  tell", which is the honest answer.
- **An output not declared in the manifest is skipped silently** — `real_rates_comparison.py`,
  for instance. The match is by *resolved path*, not filename, because Brazil and the US each
  ship an `Inflation.html`.

The import of `domain.dashboards.status` is local to the function on purpose: `analytics/`
should not require `domain/` to be importable just to assemble an HTML file, and
`status.gerar()` imports `generate_report`, which imports this module — closing that loop at
module level would be asking for a circular import.

## Why build-time, not a runtime shared module

A runtime-shared JS/CSS file (e.g. all three reports `<link>`/`<script src>`-ing a common asset) was considered and rejected: these reports are deliberately single self-contained files, sent by email/Dropbox with no server and no relative-path dependencies. `render_report()` inlines the shared pieces at generation time instead, so the dedup lives in the source tree, not in what gets shipped.
