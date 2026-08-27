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

Two data tabs — the CPI and the PCE — driven by the **same JS hierarchy-table factory**
(`makeHierTab`), the table-plus-chart structure `analytics/brasil/credit` and `.../fiscal_policy` use and
`analytics/brasil/inflation` does **not**. Testing that structure on US data was the point of the first
version. The CPI's two published trees are a **selector inside the CPI tab**, not two tabs (2026-08-26).

| Tab | Tree | Shape |
|---|---|---|
| CPI · Release | `inflc_cpi_dim`, `arvore='divulgacao'` | 37 published rows × 5 levels — Table 1 of the news release — **plus 163 drill-down rows** where the release stops (see below) |
| CPI · Expenditure | `inflc_cpi_dim`, `arvore='despesa'` | 355 items × 10 levels — the full statistical structure, down to gasoline by grade |
| PCE | `inflc_pce_dim` | 368 lines × 9 levels (BEA tables 2.4.4U/2.4.5U) + the 34 addenda aggregates as a flat, collapsed block |
| Appendix | — | sources, method, and the caveats below |

The CPI tab carries **three sections**: the hierarchy table and its chart, then *Largest contributions*
and *12-month change — component drill-down*, both added 2026-08-26 and both following the tab's Tree and
Adjustment pills.

Controls per tab: **Metric** (Y-Y / M-M / 3M annualised / Contribution to Y-Y / Contribution to M-M)
× **Adjustment**
(SA / NSA). That second axis replaces credit's Nominal/Real/%PIB — for a price index the natural
second dimension is the seasonal adjustment, and it is a real dimension of the data (`ajuste` is in
`inflc_cpi`'s primary key because coverage differs: 273 items have NSA, 234 have SA). On the PCE tab the
NSA pill is present but **disabled**: the BEA publishes no unadjusted monthly counterpart, and a greyed
pill with a tooltip answers "where is NSA?" better than an absent control does. The CPI tab adds a
**Tree** pill group (Release | Expenditure); the PCE has one tree and gets none.

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

## One tab, two trees (2026-08-26)

The Expenditure tree stopped being its own tab and became a **view of the same table**, picked with the
Tree pills — the arrangement `analytics/brasil/inflation` uses for its two trees (IBGE expenditure
structure and the BC's analytical one). `makeHierTab` takes `opts.trees` as a list: the CPI tab passes two
keys and gets the pill group, the PCE passes one and gets none.

One thing to not get wrong when touching this: **ticks and open branches are kept per tree**, in a
`per[dataKey]` map. Both trees call *All items* `SA0` and share hundreds of item codes, so a single
`checked` map would carry a selection into a tree where the same code sits at a different depth under a
different parent. Asserted: tick an extra row in Release, switch to Expenditure and back, the tick is
still there and Expenditure still shows its own four defaults.

The h2, the note under it and the label of the name column all come from `TREE_INFO` in the template, not
from the HTML — they have to move with the pills. That also retired the `<span id>` placeholders the boot
block used to fill (`rel-pointer-n`, `exp-n`, `exp-levels`, `exp-nw`, `exp-start`, `pce-n`, `pce-levels`,
`pce-add`, `pce-start`).

## The Table 1 view was removed (2026-08-26)

`Series | Table 1` toggle, gone at the user's request — it reprinted a table the BLS itself publishes on
release day. `table1Cols`, `renderHeadT1` and `fmtT1` went with it, along with the two-row header CSS.

**The arithmetic did not go with it, on purpose.** `riAt` now fills the *Weight* column of the
contributions table and `levelAt`/`pctBetween` fill its *Change* column, so the reconciliation against the
printed release survives the view that motivated it — and it stays a live code path rather than a
test-only one. The test asserts both directions: that `table1Cols` and `fmtT1` are gone (no dead code) and
that `pctBetween` and `riAt` are still functions.

The relative importance is worth understanding, because **it is reconstructed, not loaded**. Table 1
dates it one month behind the reference month, and no file this database ingests carries it — the workbook
publishes December only. It is recovered the way the BLS updates a relative importance: the December weight
times the item's own NSA index ratio since that December, divided by the headline's ratio over the same
span. Two independent checks, both in the test suite:

- **Against the printed table**: all 37 relative importances of the July 2026 release come back within
  **0.0008**, inside the rounding of the printed figure. The levels behind them reproduce the *All items*
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

## The two readings below the table (2026-08-26)

Both are ports of `analytics/brasil/inflation`, and both differ from the original in one measured way.

**Largest contributions** — Brazil's *Maiores Contribuições no Período*. Rank pills (Leaves / Level 1-3),
Window pills (1/3/6/12M), sortable headers, top-20 ↔ all. Two things are not cosmetic:

- **The contribution over a window is weight × change across the window, not the sum of the monthly
  contributions.** The sum was written first and does not survive the data: **October 2025 was never
  published**. It is the only hole in `inflc_cpi` — 613 of 634 series blank that month, 21 with a value —
  from the US government shutdown, and one missing index kills *two* monthly changes (its own and the next
  month's), so a 12-month window would have left the whole column blank. Taking the ratio of the two
  endpoints steps over it. It also means the column carries the same weight conventions and the same
  measured error as the chart's contribution metrics, because it is literally `weightAt` at a different lag.
- **The table prints its own coverage, and that line is the point.** Brazil's ranks the 614 subitems, which
  partition the IPCA exactly, so it can stay silent. Nothing here partitions: not the leaves of either tree
  (release-tree leaves carry **60.0** of the index), and no release-tree level below 2. Measured on the July
  2026 vintage: release level 2 = 100.0 coverage and +3.28 p.p. against a +3.30% headline; expenditure
  level 3 = 99.6 and +3.19. The line says so under every configuration.

**12-month change — component drill-down** — Brazil's *Variação 12M — Drilldown de Componentes*. Level
pills plus a checkbox dropdown, one filled area when a single component is picked. The simplification the
source allows: Brazil has to **reconstruct** a level's aggregate (weighted average of subitem monthly
changes, chained into an index) because the IBGE publishes only at subitem level; the BLS publishes an
index for every node, so the plotted line is the node's own published Y/Y. The test asserts that
equality **exactly**, no tolerance — that is what says nothing is being reconstructed.

Both use **depth in the rendered tree**, never `node.level`. The two do not line up: a drill-down row
carries the expenditure tree's level number while sitting at release-tree depth, so filtering by
`node.level` would mix the two cuts into one "level".

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

So a no-weight row charts Y-Y / M-M / 3M normally and goes blank in both Contributions and in Relative
importance. Its siblings do not sum to the parent either — there is no weight to sum. Nineteen items
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

- **That one-liner is now built in JS, not written in HTML.** Since the two trees became one table
  (2026-08-26) the note has to move with the Tree pills, so it comes from `TREE_INFO[tree].note()` into an
  empty `<p id="cpi-note">`. The old `<span id>` placeholders are gone; edit `TREE_INFO`, not the HTML.
- **Nothing was deleted, only moved.** If a caveat needs to come back into view, the Appendix has the full
  text; don't rewrite it from memory.

## The Appendix is the one place methodology lives — keep it deduplicated

Cleaned out 2026-08-20 at the user's request ("make a clean in the appendix, there is shit there"). It had
grown a section per round, so the same fact was stated in two or three places. It went down to five that
day and is back at **eight** — the three added since are the release calendar, the PCE tree and the two
readings below the table, each documenting a feature that did not exist in August:
*Where the data comes from* · *Release calendar* · *How the CPI's two trees are built* ·
*What the numbers are, and what they are not* · *The weight column is reconstructed, not loaded* ·
*The two readings below the table* · *The PCE tree* · *Limits*.

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

## The Appendix is eight drawers, not eight headings (2026-08-26)

At the user's request. Each `<h3>` section became a `<details class="acc">` whose `<summary>` carries the
title **and a one-line summary of what is inside**. That second half is the point of the change: eight
stacked headings have no closed state, so ~2,700 words were always fully expanded; eight drawers that each
say what they hold are an index of what is documented. Only the first (*Where the data comes from*) ships
open, as a worked example of the gesture; **Expand all** / **Collapse all** sit above them, and Expand all
is what to press before printing, since a collapsed `<details>` does not print.

**The references elsewhere in the report became real links.** They used to read "method and caveats in the
**Appendix**" and leave the reader to find which of eight sections that meant. Now each is an `axLink()`
that calls `goAppendix(id)`: switch to the Appendix tab, open that drawer, scroll to it, and flash its
border for 1.4 s. The flash is not decoration — landing on a drawer that was already open is otherwise
indistinguishable from the click doing nothing.

Four things to keep in mind before editing this:

- **`mostrarAba(nome)` was extracted from the tab-button click handler** so the link and the button share
  one path. Add a tab and it needs an entry in `PANEL_CHARTS` as before; nothing else changed.
- **`axLink` escapes the quote as `&#39;`, deliberately.** The `onclick` attribute is built inside a JS
  string already delimited by single quotes; the entity is decoded before the handler's JS is parsed, so
  no backslash escaping is involved anywhere.
- **Six of the eight drawers have an inbound link; `ap-sources` and `ap-limits` do not**, because no
  statement on the page refers to them specifically. That is asserted, so it reads as a decision rather
  than an oversight. `ap-numbers` is the target for "only levels 0–2 partition the index" — the warning
  banner lives there, not in the tree-construction drawer, which is where the link pointed first.
- **A renamed drawer id breaks the build.** The test scans the generated HTML for every `goAppendix(...)`
  and `axLink(...)` target and requires each to exist as a drawer, so a rename leaves a failing test
  rather than a link that clicks and does nothing.

Two CSS bugs surfaced while doing this, both pre-existing and both invisible until the content moved:
`.appx p` never had a vertical margin (the global reset zeroes it), so appendix paragraphs ran together —
tolerable in a wall of headings, not inside a drawer where a whole section is one block; and `.appx ul`
had no `padding-left`, which put the `<li>` markers outside the content box, where `details`'
`overflow: hidden` would now have clipped them.

## Design-system pass against the `lis-dashboard` skill (2026-08-26)

Audited against
[`.claude/skills/lis-dashboard/references/design-system.md`](../../../.claude/skills/lis-dashboard/references/design-system.md)
at the user's request and brought into line. What actually changed:

- **Plotly 2.32.0 → 2.35.2.** This was the only one of the nine analytics reports still on 2.32.0.
- **One `PLOTLY_CONFIG` and one `mkLayout(extra)`**, replacing a config object and a layout object that
  had been hand-copied into each of the two chart renderers and had already started to drift. The test
  asserts the three charts pass the *same* config object, not merely an equal one.
- **Config gained what the reference specifies**: `displayModeBar: 'hover'` (it was `false`),
  `displaylogo: false`, and `lasso2d`/`select2d`/`autoScale2d` removed from the modebar.
- **Axes and hover restyled to the reference**: X loses its gridlines for a base line only
  (`showgrid:false` + `showline` + `linecolor`), ticks become JetBrains Mono 10 in `#7A88A8`, Y's grid
  moves to `rgba(31,40,83,0.06)`, the tooltip becomes navy/Barlow 12, and paper/plot backgrounds go
  transparent so the card underneath paints.
- **Quick-range buttons**: added `1y`, and **`All` now sends an explicit `[first, last]` pair** instead of
  `xaxis.autorange: true`. Autorange returns the range *with Plotly's own padding*, which on a series
  starting in 1913 is a visible empty band after the last real point — the same class of bug the
  reference's warning box is about, just reached from the other direction.
- **`Values on chart`** — the reference's mandatory "Dados no gráfico" toggle. Off by default, flips trace
  `mode` between `'lines'` and `'lines+text'` via `Plotly.restyle` (no re-render), and thins labels with
  the reference's own step rule (>60 points → every 5th), without which 1,363 months of CPI print as a
  smear. **Disabled on the contribution charts on purpose**: up to 14 stacked bar series, one number per
  segment, is not readable.
- **Brand mark and footer**, which the report simply lacked while every sibling report had both.
- `.rb` restyled to the reference's `.range-pill` (mono 11px, pill radius), and `.chart` to the
  prescribed `position: relative; height: 480px`.

**Four of the skill's rules are deliberately not applied**, because they describe a different genre — a
single-asset NAV/price dashboard built from one CSV — and applying them here would make the report worse,
not more compliant:

| Rule | Why not |
|---|---|
| BR decimal formatting (`fmtLabel`, comma decimal, `R$`) | A US report with an English UI. `3,4%` is not how a CPI print is read, and the source publishes with a decimal point. |
| Three stats cards — last / max / min | The KPI strip carries the published headline / core / food / energy figures, which is the equivalent reading for a price index. Max and min of a CPI *index level* are the last and first months — the series is near-monotonic, so the cards would be noise. |
| Single navy spline with `fill:'tozeroy'` and green/red per-point markers | That is the one-series trace. These charts plot up to 14 comparable series, each with its own palette colour, plus a stacked-bar decomposition; one navy fill would erase the comparison the chart exists for. |
| `.month-btn` period filters | The period control here is the quick-range bar, which the reference itself prescribes. |

If any of those four should in fact be adopted, they are additions rather than rewrites — but each needs
a decision first, which is why they are listed rather than silently skipped.

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

**The routine load is API-only** (2026-08-26). Values come from the BEA API (`inflc_pce`, dataset
`NIUnderlyingDetail`, needs `BEA_API_KEY`). The tree exists only in the Section 2 *underlying detail*
xlsx — but it is loaded into `inflc_pce_dim` once and thereafter **re-read from MySQL and re-proved
against the API**, so the 12 MB file is fetched only when the structure actually moves. `U20404-M` is
table 2.4.4U (price index, 2017=100) and `U20405-M` is 2.4.5U (nominal spending, US$ mn SAAR), both
monthly from 1959-01.

It started as xlsx-only, because `us_project/inflation_fontes_dados.md` had "Get the BEA key" as an open
item and the xlsx turned out not to need it. **But "not needed" is not the same as "better", and the
first version of this note conflated them.** The key arrived on 2026-08-26, the two doors were measured
against each other, and the load moved to the API for everything the API can serve —
`tests/test_bea_api.py`, 60 assertions. Where it landed:

- **Values: the API is the better contract, and the two agree exactly.** 608,442 observations compared
  one by one (both tables, full history), **0 differing, max difference 0**, nothing present on only one
  side, labels identical after the same `_limpar_rotulo()`. Typed JSON beats a parser leaning on `"Line"`
  in cell A8, two spaces per level and `.....` for missing — and the cross-check is what makes that a
  measured claim rather than an assertion, the same way `connectors/bls.py` cross-checks the BLS API
  against the flat file.
- **Structure: the API is useless, because it publishes no hierarchy at all.** Measured on the `GetData`
  record: ten fields (TableName, SeriesCode, LineNumber, LineDescription, TimePeriod, METRIC_NAME,
  CL_UNIT, UNIT_MULT, DataValue, NoteRef), none of them a parent, level or indent; `LineDescription`
  arrives *without* the column-B spaces and `LineNumber` is order, not depth. The tree is what makes this
  tab exist — drill-down, contribution roll-up and the partition test all need parentage. So
  `TabelaNipa.fonte` exists and `inflc_pce_dim` refuses anything but `"xlsx"`; fed the API it would build
  a flat, all-level-0 tree without raising.
- So the design is **hybrid, not a switch**: structure from the xlsx, values cross-checkable against the
  API. Two documentation errors found while measuring: the field is `METRIC_NAME` (the guide writes
  `Metric_Name`) and `NoteRef` is a tenth field the guide omits. "vintage" appears zero times in the
  guide, so the earlier claim that a key would buy vintages had no basis.

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

## Release schedule strip (2026-08-26)

A band under the header shows, per series, the **last** and **next** release with date, time in both
zones and the reference month it delivers. It reads `payload["releases"]`, filled by
`domain.release_calendar.sync.agenda_das_tabelas(_TABELAS_AGENDA)` — no date is written anywhere in
this folder.

Adding a series to the strip is two declarations, no code: the table goes in `_TABELAS_AGENDA`
(`generate_report.py`) and its release becomes a group with a `us:` block in
`domain/release_calendar/calendar_2026.yaml`. The whole schedule layer — the three sources, why each
agency needs a different one, and the format traps — lives in
[`connectors/us_agenda.py`](../../../connectors/us_agenda.py) and
[`domain/release_calendar/CLAUDE.md`](../../../domain/release_calendar/CLAUDE.md).

Three decisions worth keeping:

- **Both clocks, always.** 08:30 ET is the published fact; 09:30/10:30 BRT is when to be at the
  screen. The two drift apart twice a year — the US keeps DST, Brazil dropped it in 2019 — so the
  YAML stores the source's zone and converts per date. A single converted value would be wrong for
  half the year, silently.
- **The countdown is computed in the browser**, not baked into the payload. These files get emailed
  and opened days later; a frozen "in 16 days" would be a confident lie. *Past due* therefore means
  the file is stale, which is what a reader needs to know before trusting the latest month above it.
- **The reference month is read, never derived.** BEA's own 2026 calendar breaks "release month minus
  one" five times running (Jan 22, Feb 20, Mar 13, Apr 9 *and* Apr 30, catching up on a delayed
  schedule).

Both agencies publish one year at a time, so the *next* line runs dry at the end of the year until
they post the following one — neither had 2027 as of this build.

## Tests

`uv run python tests/test_bea_api.py` — 60 assertions, needs `BEA_API_KEY` and network (`--rapido`
trims it from the full history to the last 3 years, ~7 MB instead of ~150 MB). It is the **source** test,
not a report test, and it closes a triangle: the two BEA doors against each other value by value, then
both against FRED's `PCEPI`/`PCEPILFE`. The first pair catches errors of *reading* — a cosmetic reformat
of the workbook, which is what the whole parser leans on, shows up as a diff instead of as a silently
wrong tree. The FRED leg catches what that pair structurally cannot: an error of *identification*. If
line 374 were not the core, both BEA doors would agree on the wrong line just as happily. Currently exact
on 19 months, difference 0.

It also pins the facts the design rests on: that the API still has no hierarchy field (if that ever
fails, it is good news and the dim should be revisited), that error responses arrive with **HTTP 200** in
one of two different nodes, that the error message never echoes the key back (the API returns it inside
`Request.RequestParam`), that the series codes — not just the labels — match across doors, and that
`inflc_pce` refuses to write when the two disagree. Without a key it prints SKIP naming what went
unchecked rather than passing quietly.

**One lesson from it worth keeping.** The BEA revises prior months on every monthly release — June 2026
moved from 131.392 to 131.454 between 20 and 26 Aug 2026 — so any test that hardcodes a level for a fixed
month has a shelf life. Two assertions in the JS suite did exactly that and broke on their own; the
"does this match the world" question moved to the FRED leg above, where it can be asked live, and the JS
anchors now only guard the payload→display path. A third assertion broke for a related reason: it
required the PCE's last month to differ from the CPI's, which is true only in the fortnight between the
two releases, not after the PCE catches up. It now asserts the real invariant — the PCE is never *ahead*
of the CPI.

`node tests/test_us_inflation_js.js` — 340 assertions. Evaluates the **real** `<script>` from the
generated HTML against a stubbed document/Plotly, initialises both hierarchy tabs, and asserts on what
was produced: that Y/Y reproduces the published 3.4 / 2.5 / 14.7 / 3.0, that M/M equals the level ratio,
that clicking a pill actually re-renders and changes the Y-axis title, that the contribution metrics
produce **bars plus one line** rather than lines (and that the ticked headline lands in the line, never as a
fourth bar — the PCE tab ships that case by default), that the 3y button calls
`Plotly.relayout` with a window ending at the last **real** data point, that the tree flattens and the
partial decompositions carry 25.583 pp, that the reconstructed relative importance still matches the
printed release, and that no row renders a visible tag while the hover text still carries the caveat.

Sections 15-17 cover the 2026-08-26 round: that the Expenditure tab and panel are gone from the HTML and
the Tree pills replaced them, that ticks survive a round trip between trees, that the ranking's level-1
weights sum to 100 and its contributions rebuild the headline, that the drill-down plots the published
index exactly, and — pinned on its own because it decided the window formula — **that October 2025 has no
headline index, and that one missing month blanks two M/M values while leaving Y/Y intact**.

Section 18 covers the appendix drawers: that the eight exist with the ids the links use, that no `<h3>`
survived and the CSS rule for it went with them, that exactly one ships open, that the three `<span>`s the
script fills are still inside drawers, that every link target resolves to a real drawer, that
`goAppendix` switches tab *and* opens *and* flashes, that an unknown id neither throws nor blocks the tab
switch, and that Expand/Collapse all move all eight. The drawer ids are read from the HTML itself, not
listed in the test, so renaming one in the template fails the suite instead of producing an empty stub
that passes.

Section 19 is the design-system conformance pass: the CDN version and the absence of Chart.js/Hammer,
no `<canvas>` anywhere, the three fonts in the Google Fonts link, the config's five fields **and that all
three charts pass the same object**, `mkLayout()`'s gesture/hover/axis/background fields including the two
negatives that matter (no `fixedrange`, no `xaxis.rangeselector`), that an `extra` merges into an axis
rather than replacing it, the six range buttons with `All` sending real endpoints and never `autorange`,
and the Values toggle across its whole life — off at start, text arrays already on the traces, the step
rule thinning 1,350 points to 270, restyle on click, and dead while the contribution chart is up.

That last group needed a **stub fix that was really a fidelity bug**: `createElement` returned an element
whose `id` was never registered, so a button the script creates *and names itself* existed twice — the
product mutating the one it built, the test reading an empty one the registry invented on lookup. `id` is
now an accessor that registers, which is what a browser does.

One harness trap that cost a round: switching trees redraws the table *and* notifies the two sections
below, so `reactCalls[last]` is the drill-down's chart, not the table's. Assertions about the main chart
have to filter for `div === 'chart-cpi'`.
The last section covers the release strip: both clocks present and labelled, the ET→BRT gap being an
hour or two and never zero, the reference month preceding the release month, the countdown matching
the harness's own clock, and the strip hiding itself when the payload carries no schedule.

`uv run python tests/test_us_agenda.py` — the schedule layer itself: the ICS/HTML parsers against
fixtures, then the three live sources checked against each other. See
[`connectors/CLAUDE.md`](../../../connectors/CLAUDE.md).

Section 14 covers the PCE tab. The assertion that earns its keep is the one that sums *Goods* +
*Services* contributions and checks they rebuild the headline Y/Y (worst month 0.098 p.p. over the last
five years) — and, since 2026-08-26, the same for M/M, where the monthly weight shows what it is worth:
worst month **0.0027 p.p.**, against ~0.014 for the CPI's December snapshot — it exercises the monthly weight, the base-period lag and the accumulated signs in one
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
- **The decomposition chart has no residual bar.** Built in 2026-08-26: both contribution metrics
  render as stacked bars plus a headline line, and the anchor is excluded from the stack so a ticked
  headline becomes the line instead of doubling the chart. What is still missing is an *Other* bar
  closing the gap between the stack and the line — without it the stack reconciles only when the ticked
  rows partition the index, which the note under the table says but the picture does not show. It was
  left out on purpose (it invents a category the sources do not publish, and with overlapping addenda
  ticked it would go negative), so adding it is a decision, not a fix.
- **CPI-U only.** CPI-W and C-CPI-U are supported by the schema and the loader, not loaded.
- **The monthly weight** (release column, 37 rows) isn't used — it would tighten the reconciliation but
  has to be harvested release by release. The blocker named here is gone: the release-date calendar
  now exists (`bls_cpi` in `calendar_2026.yaml`, dates back to 1948 via `FREDReleases.dates(10)`), so
  what remains is the harvesting itself. See `us_project/inflation_hierarchy.md` §2.
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
