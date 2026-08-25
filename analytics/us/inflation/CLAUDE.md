# analytics/us/inflation/ — US Inflation report

First report under `analytics/us/`. Reads `macro_us` — `inflc_cpi` / `inflc_cpi_dim` /
`inflc_cpi_pesos` for the CPI, `inflc_pce` / `inflc_pce_dim` for the PCE — with no local CSV/Excel, and
writes `reports/us/Inflation.html` (5.9 MB).

```powershell
uv run python -c "from analytics.us.inflation.generate_report import run; run()"
```

**UI is in English**, unlike the Brazil reports. It is a US product read against US sources, and
`us_project/`'s notes are already in English. Say the word if it should be Portuguese instead — it is
a template-only change.

## What it is

Three data tabs — the CPI's two published trees and the PCE — all driven by the **same JS
hierarchy-table factory** (`makeHierTab`), the table-plus-chart structure `analytics/brasil/credit` and
`.../fiscal_policy` use and `analytics/brasil/inflation` does **not**. Testing that structure on US data
was the point of the first version.

| Tab | Tree | Shape |
|---|---|---|
| Release Tree | `inflc_cpi_dim`, `arvore='divulgacao'` | 37 published rows × 5 levels — Table 1 of the news release — **plus 163 drill-down rows** where the release stops (see below) |
| Expenditure Tree | `inflc_cpi_dim`, `arvore='despesa'` | 355 items × 10 levels — the full statistical structure, down to gasoline by grade |
| PCE | `inflc_pce_dim` | 368 lines × 9 levels (BEA tables 2.4.4U/2.4.5U) + the 34 addenda aggregates as a flat, collapsed block |
| Appendix | — | sources, method, and the caveats below |

Controls per tab: **Metric** (Index / Y-Y / M-M / 3M annualised / Contribution to Y-Y) × **Adjustment**
(SA / NSA). That second axis replaces credit's Nominal/Real/%PIB — for a price index the natural
second dimension is the seasonal adjustment, and it is a real dimension of the data (`ajuste` is in
`inflc_cpi`'s primary key because coverage differs: 273 items have NSA, 234 have SA). On the PCE tab the
NSA pill is present but **disabled**: the BEA publishes no unadjusted monthly counterpart, and a greyed
pill with a tooltip answers "where is NSA?" better than an absent control does. The CPI tabs' extra
**View** toggle (Series | Table 1) has no PCE equivalent — it renders the BLS news release's own column
set.

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
expenditure tree now continues underneath it: 163 further rows, three gasoline grades included. The tab
is still Table 1: the 37 published rows, their order and their partial decompositions are untouched.

Two invariants make that claim checkable, both asserted in the test suite:

- **The graft only goes below a leaf, never beside a published child.** Otherwise `decomposicao='partial'`
  would start lying — it means "the release omits siblings here", and pulling those omitted siblings in from
  another source would contradict `peso_nao_exibido`. *Motor fuel* therefore stays partial (*Other motor
  fuels* is a sibling of *Gasoline (all types)*, not a deeper level) while *Gasoline (all types)* opens
  into its three grades.
- **No node is duplicated.** A drill-down child whose code already exists in the release tree would show
  the same row twice; `_arvore` asserts on it rather than checking at review time. There is no such case
  today.

Payload cost is zero: those 163 series already travel in the expenditure tab, and `seriesSource` in the
template reads a code from whichever tab owns it. That works because both tabs' date grids end on the
same month — also asserted, since a mismatch would silently render every drill-down row as `—`.

## The Table 1 view

Each hierarchy tab has a **View** toggle: `Series` (the default — one metric across the last twelve months)
and `Table 1`, which replaces those twelve columns with the news release's own nine: relative importance,
three unadjusted index levels, two unadjusted percent changes, three seasonally adjusted monthly changes,
grouped under the same headers the release prints. Nothing new travels in the payload — all nine are
computed in the template from the levels and weights already there.

The interesting column is the relative importance, because **it is reconstructed, not loaded**. Table 1
dates it one month behind the reference month, and no file this database ingests carries it — the workbook
publishes December only. It is recovered the way the BLS updates a relative importance: the December weight
times the item's own NSA index ratio since that December, divided by the headline's ratio over the same
span. Two independent checks, both in the test suite:

- **Against the printed table**: all 37 relative importances of the July 2026 release come back within
  **0.0008**, inside the rounding of the printed figure. The other eight columns reproduce the *All items*
  row exactly — 323.048 / 333.952 / 333.918, 3.4% and 0.0% unadjusted, +0.5 / −0.4 / +0.1 adjusted.
- **Structurally**: the eight level-1 groups still sum to 100.000 after each is updated on its own, so the
  update cannot be silently rescaling anything.

Because it needs a December weight, the column fills for 265 of the 355 expenditure rows — blank for the 83
below the relative-importance table and for the 7 whose series stops before the reference month. The
Appendix carries the formula and the count, and the count is filled by the same function that fills the
column rather than by a number written into the prose.

One trap worth knowing: the payload's date grid holds full ISO dates (`YYYY-MM-DD`), so `monthIndex` keys
by `YYYY-MM`. The first version keyed by the whole string, the December anchor never resolved, and *every*
relative importance came back null — which the accuracy assertion happily passed, because a max-error over
an empty set is zero. The assertion now requires 37 values checked as well as the error bound.

## Two layers of detail, and only one of them has weights

The expenditure tree stopped at the relative-importance spreadsheet's own depth until 2026-08 — 267
items, no gasoline grades, no roasted-vs-instant coffee, no new-cars-vs-new-trucks. `cu.item` publishes
83 items below that line and every one of them has a real index series. They are grafted onto the tree
now (see `inflc_cpi_dim`'s docstring for the parent rule and its validation), which takes the tab to
**355 items over 10 levels**.

What separates the two layers is the weight, and the payload says so per node:

| | Items | Weight | Contribution | Relative importance |
|---|---|---|---|---|
| From the spreadsheet | 272 | published | yes | computed (see above) |
| Grafted from `cu.item` | 83 | none published | blank, by construction | blank |

So a no-weight row charts Index / Y-Y / M-M / 3M normally and goes blank in Contribution and Relative
importance only. Its siblings do not sum to the parent either — there is no weight to sum. Nineteen items
are also discontinued: series the BLS stopped publishing, kept with their history. That needs a
three-month gap so an item merely one month behind on release day is not mislabelled as dead. Neither
case is written into the row (see "No tags on the rows"); both are in the row's hover text.

Five further items used to vanish on a label mismatch alone (the spreadsheet writes "swimwear, and
accessories", `cu.item` writes it without the second comma) — 0.861 index points that had both a weight
and a series published. `_ALIAS` in `inflc_cpi_dim` fixes it, `inflc_cpi_pesos` imports the same dict so
the two tables cannot drift, and each pair was confirmed by position in the publication order rather
than by resemblance.

## The trap the report has to keep visible

In the release tree, levels 0, 1 and 2 each sum to 100.000 — complete partitions. Below that, 7 of the
13 parents show only their largest children, leaving **25.583 index points with no row** (11.721 inside
core services, 7.282 inside core goods). Contributions summed at level ≥ 3 do not add to the parent.

The dim carries this per node (`decomposicao` = complete/partial/leaf, `peso_nao_exibido`). Until
2026-08-20 the table printed it as a `−X.XXX pp` tag on the row; the tags were removed at the user's
request and the figure moved into the row's hover text, with the totals stated in the warning banner
above the table. Keep it reachable somehow — without it the tab silently loses a quarter of the index in
exactly the place under discussion.

## Methodology lives in the Appendix, not above the tables

**2026-08-20, at the user's request** ("this warning you could place in the appendix, it's too much
verbosity — methodology and that stuff just pollute"): each tree tab now carries a **single line** above
the controls — what the tab is, the row counts, and a pointer to the Appendix. The three explanatory
paragraphs and the "only levels 0–2 partition the index" warning banner moved into the Appendix verbatim,
under a new *How each tree is built* heading. The Table 1 view's own note shrank from a paragraph to one
line for the same reason.

Two things to keep in mind before editing that line:

- **The `<span id>` placeholders have to stay somewhere in the tab.** `rel-pointer-n`, `exp-n`,
  `exp-levels`, `exp-nw` and `exp-start` are written by the boot block with a bare
  `getElementById(...).textContent = ...`. Delete one and the whole script dies with a TypeError on load —
  a blank page, not a missing number. They are all folded into the surviving one-liners.
- **Nothing was deleted, only moved.** If a caveat needs to come back into view, the Appendix has the full
  text; don't rewrite it from memory.

## The Appendix is the one place methodology lives — keep it deduplicated

Cleaned out 2026-08-20 at the user's request ("make a clean in the appendix, there is shit there"). It had
grown a section per round, so the same fact was stated in two or three places. Now **five** sections:
*Where the data comes from* · *How the two trees are built* · *What the numbers are, and what they are not* ·
*The relative-importance column is reconstructed, not loaded* · *Limits*.

What was actually wrong, so the same drift is recognisable next time:

- **The same claim in two voices.** The "only levels 0–2 partition the index" banner and a *Contribution*
  bullet both said the release is not exhaustive below level 2. Now said once, in the banner, which also
  carries the 25.583 pp.
- **Sections that were continuations of another.** *Where the deepest items come from* and *The two
  re-parented nodes* were both about how the expenditure tree gets built — folded into that one section.
- **Two "known gaps" that were not gaps.** The monthly weight is reconstructed (it has its own section), and
  the three excluded `cu.item` entries are a method decision. *Limits* now holds four real ones: pre-2020
  weights, CPI-U only, SA 291 of 361, 19 discontinued series.
- **Maintenance history mistaken for reader method.** The five-item label-mismatch story is one sentence here
  now; the full account belongs in [`us_project/inflation_hierarchy.md`](../../../us_project/inflation_hierarchy.md)
  §1c and in `inflc_cpi_dim`'s docstring.

Every number in it was re-checked against the database in that pass: 340,907 rows, 392 dim rows = 355 + 37,
3,864 weight rows, 294 spreadsheet lines, 361 items with NSA and 291 with SA, 272 with a weight and 83
without, 7 of 13 release parents partial summing to 25.583 pp (11.721 + 7.282). One was being stated in a way
that invited a contradiction: the additivity proof covers the **90 parents the weight table reaches**, while
the loaded tree has **130** parents — the difference is the grafted layer, which has no weights to check. It
now says so.

## No tags on the rows

The rows used to carry small inline tags — `agg`, `detail`, `no weight`, `last <YYYY-MM>`,
`−X.XXX pp`. **Removed 2026-08-20 at the user's explicit request** ("I want you to remove all these
tag"), after they had read what each one was for. Do not put them back without being asked.

Nothing they said was dropped. Each row's label cell gets a `title` built from the same payload flags
(`special` / `detail` / `noWeight` / `stale` / `decomp`), which are unchanged, so the caveat is one hover
away; the aggregate facts (25.583 pp with no row, the 83-item layer, the 19 discontinued) stay written
into the notes and the warning banner above each table. The test suite asserts both halves: that the
string `badge` appears nowhere in the generated HTML, and that *Motor fuel* still says `0.119` on hover
while *Gasoline, unleaded regular* still says it has no relative importance and is not a Table 1 row.

## The PCE tab (2026-08-20)

Added at the user's request ("let's make a tab to the PCE"). It is the Fed's target index and it is a
**different statistic**, not a variant of the CPI: national-accounts weights instead of a household
survey, wider scope (it counts what employers and government pay on households' behalf, most visibly
health care), chained Fisher instead of a fixed-basket Laspeyres. The two are not meant to reconcile.

**No BEA API key was needed** — `us_project/inflation_fontes_dados.md` had "Get the BEA key" as an open
item for exactly this, and it turned out to be unnecessary. The BEA publishes the whole Section 2
*underlying detail* release as an open xlsx: 12 MB, 22 sheets, no auth, no quota. `U20404-M` is table
2.4.4U (price index, 2017=100) and `U20405-M` is 2.4.5U (nominal spending, US$ mn SAAR), both monthly
from 1959-01. The key would still buy vintages and other sections; it buys nothing for this.

Why this source is *better behaved* than the CPI's, which is worth knowing before comparing the tabs:

| | CPI expenditure tree | PCE tree |
|---|---|---|
| Parent/child | assembled from two sources, matched by **name** | published **indentation** of one file |
| Price ↔ weight join | different files, name-matched (5 items once lost to a comma) | same file, same 402 lines, joined by **line number** |
| Additivity proof | 90 of 130 parents (only the weight-table layer) | **122 of 122** checkable parents, all 810 months |
| Levels that partition exactly | release tree: 0–2 | **1–4**, and the 245 leaves sum to 100.0000% |
| Weight frequency | annual December snapshot, carried forward | **monthly**, published |
| Contribution error vs. headline | 0.0124 p.p. | **0.0009 p.p.** (M/M), 0.0114 (Y/Y) |

Four things about it that are not obvious:

- **The key is the BEA line number, not the series code.** 13 codes appear on two lines each (`Health
  care` under Household consumption *and* under Market-based PCE), so keying by code would collapse
  distinct rows of the tree. Values are identical in both positions — checked series by series — so the
  duplication costs nothing. `key` and `seriesKey` are both the line number.
- **Nineteen lines subtract, and only four say so.** Four rows start with `Less:`; the other fifteen are
  what sits *underneath* one and inherits the sign silently. The payload ships the weight **already
  signed**, so the JS needs no special case. Summing a level without this gives 116% of PCE instead of
  100% — which is exactly what the first version of the load did. Separately, a negative weight is not
  proof of a `Less:` line: `Employee reimbursement` has genuinely negative spending (−$1.7 bn) with an
  ordinary positive sign, so 19 lines are flagged `negativo` while 20 weights come out negative.
- **The weight is dated at the base of the change, not at the reference month.** A Y/Y change is weighted
  by the share **12 months earlier**: measured on this database, that rebuilds the published headline to
  0.0114 p.p. mean absolute error against 0.0202 using the current month's share. `weightAt` in the
  template dispatches on whether the tab carries a `weights` array — no CPI tab does, which is how the
  two conventions coexist without a flag.
- **The 34 addenda are a flat, collapsed block, not a subtree.** Control group, PCE food and energy, PCE
  excluding food and energy (the core), the market-based family. They overlap each other and must never
  be summed. They are flat because the BEA's own indentation there is inconsistent — `Market-based PCE`
  is printed *deeper* than the lines it heads — so giving them parentage would mean inventing it. They
  hang off a synthetic `ADDENDA` header row that has no series of its own (`noSeries`, so no checkbox)
  and opens collapsed (`startCollapsed`), since 34 non-tree rows would otherwise be most of the first
  screenful.

Two smaller facts: the tab is **SA only**, and two lines (`Net expenditures abroad by U.S. residents`,
`Net foreign travel`, marked `ZZZZZZ` by the BEA) have spending but **no price index** — they are nets of
two flows, so their price columns are blank while their weight is real. The PCE's last month also trails
the CPI's by a few weeks (2026-06 vs 2026-07 as of this writing), so `meta.ultimo_mes_pce` is separate
from `meta.ultimo_mes` and the tab's twelve columns come from its own grid.

**Payload cost**: the tab roughly doubled the file, 2.97 → 5.89 MB, because it ships 402 index arrays
*and* 402 weight arrays over 438 months. If that ever needs to come down, the lever is `_INICIO_PCE` (the
window start, currently 1990 to match the CPI expenditure tab) — not the weights, which would leave
contribution with a silent hole.

## Tests

`node tests/test_us_inflation_js.js` — 166 assertions. Evaluates the **real** `<script>` from the
generated HTML against a stubbed document/Plotly, initialises both hierarchy tabs, and asserts on what
was produced: that Y/Y reproduces the published 3.4 / 2.5 / 14.7 / 3.0, that M/M equals the level ratio,
that clicking a pill actually re-renders and changes the Y-axis title, that the 3y button calls
`Plotly.relayout` with a window ending at the last **real** data point, that the tree flattens and the
partial decompositions carry 25.583 pp, that the Table 1 view reproduces the printed release cell by
cell, and that no row renders a visible tag while the hover text still carries the caveat.

Section 14 covers the PCE tab. The assertion that earns its keep is the one that sums *Goods* +
*Services* contributions and checks they rebuild the headline Y/Y (worst month 0.098 p.p. over the last
five years) — it exercises the monthly weight, the base-period lag and the accumulated signs in one
shot, so a regression in any of the three fails it. Also: that the level matches FRED's `PCEPI`/`PCEPILFE`
to 0.0005, that the disabled NSA pill does nothing when clicked, that expanding the addenda block adds
exactly 34 rows whose hover warns they overlap, and that the PCE's last month is *not* the CPI's.
Written this way because of the lesson in
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
- **No expectations or PPI tabs.** `us_project/inflation_fontes_dados.md` has the rest of the branch
  mapped; the trimmed-mean/median cores (Dallas and Cleveland Fed) are on FRED and would be the cheapest
  next addition.
- **PCE: only prices and the nominal spending they need.** The same workbook carries the *real*
  counterparts at the identical 402-line granularity — 2.4.3U (quantity indexes, 810 months) and 2.4.6U
  (chained dollars, 234 months) — plus a coarse 46-line trio (2.3.4U/2.3.5U/2.3.6U, *by Major Type of
  Product and by Major Function*). Because all four 2.4.xU tables share the same 402 lines,
  `inflc_pce_dim` already fits them: adding volume is a new `medida` value, not a new dimension. But
  real PCE is **activity, not inflation** — by this project's theme-prefix rule it would be `atv_`-
  prefixed and belong to a US activity area, not to this report. The detailed by-function tree is table
  **2.5.x**, which is *not* in this workbook.
- **The KPI strip is still CPI-only.** Adding PCE headline/core to it was deliberately not done — the six
  cards carry no index label, so mixing two indices there would mislead. Either label all of them or
  leave it.
