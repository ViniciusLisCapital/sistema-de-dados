# analytics/report_structure/ — Shared report-generation scaffolding

Build-time-only building blocks for the `/*REPORT_DATA*/`-template reports (`exchange_rate/`, `inflation/`, `monetary_policy/`) — extracted 2026-08 to stop hand-copy-pasting the same boilerplate into each new report. **Nothing here is ever loaded at runtime by a generated report** — `report.html` files stay plain, self-contained HTML/CSS/JS with no reference to this package. Only each project's own `generate_report.py` imports from it, at generation time, to assemble the final file. This preserves the "one emailable file" property `.claude/rules/lis-dashboards.md` and each report's own `CLAUDE.md` already document.

## What's here

| File | Contains | Marker it fills |
|---|---|---|
| `builder.py` | `render_report(template_path, data, output_path, extra_markers=None)` — reads the template, JSON-serializes `data`, substitutes markers, writes the output, returns the resolved `Path` | — |
| `theme.css` | The shared LIS brand `:root` palette + universal reset/body rules (`--lis-azul`, `--lis-dourado`, etc. — see `project_lis_brand_colors` memory for the canonical hex values) | `/*THEME_CSS*/` |
| `y_autofit.js` | `_bindYAutofit()`/`_toComparableX()` — the Plotly rangeselector Y-refit helper described in `.claude/rules/lis-dashboards.md`'s "Plotly setup" section | `/*Y_AUTOFIT_JS*/` |

`render_report()` always substitutes `/*REPORT_DATA*/`; it only touches `/*THEME_CSS*/`/`/*Y_AUTOFIT_JS*/` if the template actually contains those markers, so a report can adopt one piece without adopting all of them.

`extra_markers` (added 2026-08 for `exchange_rate/`) covers templates with more than one JSON payload: `{"PPP_DATA": payload_or_None}` fills `/*PPP_DATA*/` with that payload's JSON, or the literal `null` when the value is `None`, so a section whose data wasn't built this run still has something valid to check against. Unlike `/*REPORT_DATA*/`, these substitute the **bare JSON value** — the template owns the `const X = ...;` declaration. Markers absent from the template are skipped silently, so passing a marker a report doesn't have is harmless.

**A marker the template declares and nobody substitutes is a syntax error, not an empty section** (`const X = /*X*/;` → `const X = ;`). If a report can skip building a payload, it must still pass that marker as `None`.

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
- **`monetary_policy/`** — not migrated at all yet (explicitly deferred). Still carries its own inline theme CSS and `_bindYAutofit` copy.
- **`economic_activity/`** — built directly onto both markers from day one (2026-08), the first report to start here rather than migrate here — no separate migration step was ever needed.
- **`fiscal_policy/`** — same as `economic_activity/`: built directly onto both markers from day one (2026-08), no migration needed.

## Why build-time, not a runtime shared module

A runtime-shared JS/CSS file (e.g. all three reports `<link>`/`<script src>`-ing a common asset) was considered and rejected: these reports are deliberately single self-contained files, sent by email/Dropbox with no server and no relative-path dependencies. `render_report()` inlines the shared pieces at generation time instead, so the dedup lives in the source tree, not in what gets shipped.
