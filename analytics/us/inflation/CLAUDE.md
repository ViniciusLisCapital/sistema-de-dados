# analytics/us/inflation/ — US Inflation report

First report under `analytics/us/`. Reads `macro_us` (`inflc_cpi` / `inflc_cpi_dim` /
`inflc_cpi_pesos`) — no local CSV/Excel — and writes `reports/us/Inflation.html`.

```powershell
uv run python -c "from analytics.us.inflation.generate_report import run; run()"
```

**UI is in English**, unlike the Brazil reports. It is a US product read against US sources, and
`us_project/`'s notes are already in English. Say the word if it should be Portuguese instead — it is
a template-only change.

## What it is

Two tabs, one per CPI tree, both driven by the **same JS hierarchy-table factory** (`makeHierTab`) —
the table-plus-chart structure `analytics/brasil/credit` and `.../fiscal_policy` use and
`analytics/brasil/inflation` does **not**. Testing that structure on US data was the point of the
first version.

| Tab | Tree | Shape |
|---|---|---|
| Release Tree | `arvore='divulgacao'` | 37 published rows × 5 levels — Table 1 of the news release — **plus 163 drill-down rows** where the release stops (see below) |
| Expenditure Tree | `arvore='despesa'` | 355 items × 10 levels — the full statistical structure, down to gasoline by grade |
| Appendix | — | sources, method, and the caveats below |

Controls per tab: **Metric** (Index / Y-Y / M-M / 3M annualised / Contribution to Y-Y) × **Adjustment**
(SA / NSA). That second axis replaces credit's Nominal/Real/%PIB — for a price index the natural
second dimension is the seasonal adjustment, and it is a real dimension of the data (`ajuste` is in
`inflc_cpi`'s primary key because coverage differs: 273 items have NSA, 234 have SA).

## Two decisions worth not re-litigating

**Levels ship; variations are computed in the browser.** The payload carries the index level per
(item, adjustment) and nothing else. Y/Y, M/M, 3M-annualised and contribution are all derived in JS,
cached per (tab, item, adjustment, metric). Shipping four pre-computed metrics × two adjustments would
be ~8× the numbers for information the level already implies, and would let stored and displayed
values drift apart. Two further compressions, both from `analytics/brasil/fiscal_policy/dlsp_tab.py`:
one shared monthly date grid per adjustment at the payload root (series are bare arrays aligned to
it), and **two history windows** — the 37 release rows carry full history (1913), the 355 expenditure
items start at `_INICIO_DETALHE` (1990). Full history for all 355 is ~1M mostly-null numbers, since
most detail items begin in the 1990s anyway. The database keeps 1913 onwards regardless; this is a
payload window, not a data window. Result: 2.4 MB.

**Contribution is an approximation and the tab says so.** Weight × variation, with the weight joined
at read time: for a month in year Y, the December snapshot of Y−1, falling back to the nearest earlier
one. That is BLS's own construction (`2025.xlsx` has reference period Dec-2025 and prices 2026) and
measured to be the better choice — using each year's snapshot instead of one fixed vector cuts the
headline reconciliation error ~30% (0.0183 → 0.0124 p.p. mean absolute, measured against this
database). It still will not close exactly, for two independent reasons: ~0.015 p.p. is irreducible
(relative importance is a December snapshot of a continuously price-updated quantity — *not* a
seasonal-adjustment artefact, since NSA is slightly worse), and **the release tree only partitions the
index down to level 2**.

## The release tab drills through into the expenditure tree

Table 1 is 37 rows and stops at *Gasoline (all types)* and *Electricity*. Twice in a row that read as
"the sub-items are missing" — so wherever a release row is a **leaf**, the matching branch of the
expenditure tree now continues underneath it: 163 further rows, flagged `detail`, three gasoline grades
included. The tab is still Table 1: the 37 published rows, their order and their `partial` badges are
untouched.

Two invariants make that claim checkable, both asserted in the test suite:

- **The graft only goes below a leaf, never beside a published child.** Otherwise a `partial` badge would
  start lying — it means "the release omits siblings here", and adding the omitted siblings from another
  source would contradict the number in the badge. *Motor fuel* therefore stays `partial` (*Other motor
  fuels* is a sibling of *Gasoline (all types)*, not a deeper level) while *Gasoline (all types)* opens
  into its three grades.
- **No node is duplicated.** A drill-down child whose code already exists in the release tree would show
  the same row twice; `_arvore` asserts on it rather than checking at review time. There is no such case
  today.

Payload cost is zero: those 163 series already travel in the expenditure tab, and `seriesSource` in the
template reads a code from whichever tab owns it. That works because both tabs' date grids end on the
same month — also asserted, since a mismatch would silently render every drill-down row as `—`.

## Two layers of detail, and only one of them has weights

The expenditure tree stopped at the relative-importance spreadsheet's own depth until 2026-08 — 267
items, no gasoline grades, no roasted-vs-instant coffee, no new-cars-vs-new-trucks. `cu.item` publishes
83 items below that line and every one of them has a real index series. They are grafted onto the tree
now (see `inflc_cpi_dim`'s docstring for the parent rule and its validation), which takes the tab to
**355 items over 10 levels**.

What separates the two layers is the weight, and the payload says so per node:

| | Items | Weight | Contribution | Badge |
|---|---|---|---|---|
| From the spreadsheet | 272 | published | yes | — |
| Grafted from `cu.item` | 83 | none published | blank, by construction | `no weight` |

So a `no weight` row charts Index / Y-Y / M-M / 3M normally and goes blank in Contribution only. Its
siblings do not sum to the parent either — there is no weight to sum. Nineteen items also carry a
`last <YYYY-MM>` badge: series the BLS stopped publishing, kept with their history. The badge needs a
three-month gap so an item merely one month behind on release day is not mislabelled as dead.

Five further items used to vanish on a label mismatch alone (the spreadsheet writes "swimwear, and
accessories", `cu.item` writes it without the second comma) — 0.861 index points that had both a weight
and a series published. `_ALIAS` in `inflc_cpi_dim` fixes it, `inflc_cpi_pesos` imports the same dict so
the two tables cannot drift, and each pair was confirmed by position in the publication order rather
than by resemblance.

## The trap the report has to keep visible

In the release tree, levels 0, 1 and 2 each sum to 100.000 — complete partitions. Below that, 7 of the
13 parents show only their largest children, leaving **25.583 index points with no row** (11.721 inside
core services, 7.282 inside core goods). Contributions summed at level ≥ 3 do not add to the parent.

The dim carries this per node (`decomposicao` = complete/partial/leaf, `peso_nao_exibido`), and the
table renders `partial` as a `−X.XXX pp` badge with the explanation in its tooltip. Don't remove it —
without it the tab silently loses a quarter of the index in exactly the place under discussion.

## Tests

`node tests/test_us_inflation_js.js` — 50 assertions. Evaluates the **real** `<script>` from the
generated HTML against a stubbed document/Plotly, initialises both hierarchy tabs, and asserts on what
was produced: that Y/Y reproduces the published 3.4 / 2.5 / 14.7 / 3.0, that M/M equals the level ratio,
that clicking a pill actually re-renders and changes the Y-axis title, that the 3y button calls
`Plotly.relayout` with a window ending at the last **real** data point, that the tree flattens and the
badges carry 25.583 pp. Written this way because of the lesson in
[`.claude/rules/lis-dashboards.md`](../../../.claude/rules/lis-dashboards.md): two rounds of interaction
bugs shipped in `economic_activity` precisely because the tests asserted on button *definitions* and
never on what a click did.

## Pending

- **Not confirmed in a real browser** — no browser in this environment. The JS is verified behaviourally
  (above), the visual rendering is not.
- **The 34 special aggregates are not loaded** — `Durables`, `Nondurables`, `Services less rent of
  shelter`, `All items less shelter` and the rest of the cuts that overlap each other. 28 of them have
  published weights in the spreadsheet's second section. They are a *third* tree, not a deeper level of
  this one, and the published indentation of that section is unusable (it nests `Energy commodities`
  inside `Commodities less food and energy commodities`), so a flat list is the honest shape. Six
  already appear in the release tree.
- **Contribution is blank before 2020**, because weights start there. BLS publishes annual December
  weights back to **1947** in two older formats; see `inflc_cpi_pesos`' docstring. Parsing gap, not data gap.
- **No waterfall / contribution-decomposition chart yet.** The natural next chart is a stacked
  contribution-to-headline bar at level 1 or 2, where the partition is exact — deliberately not at
  level ≥ 3 without a residual bar.
- **CPI-U only.** CPI-W and C-CPI-U are supported by the schema and the loader, not loaded.
- **The monthly weight** (release column, 37 rows) isn't used — it would tighten the reconciliation but
  needs the release-date calendar to harvest. See `us_project/inflation_hierarchy.md` §2.
- **No expectations/PCE/PPI tabs.** This is the CPI only; `us_project/inflation_fontes_dados.md` has the
  rest of the branch mapped.
