# analytics/us/labor_market/ — US Labor Market report

Second report under `analytics/us/`. Built 2026-09-01 with JOLTS only; the payroll and
household surveys plus the derived metrics were added the same day. Reads `mt_jolts`,
`mt_ces`, `mt_cps` and their dimension tables; writes `reports/us/Labor Market.html`
(11,7 MB, ~95 s).

```powershell
uv run python -c "from analytics.us.labor_market.generate_report import run; run()"
uv run python tests/test_jolts.py                 # 51 assercoes, precisa do banco
node tests/test_labor_market_us_js.js             # 324 assercoes, precisa do HTML gerado
```

**UI in English**, like `analytics/us/inflation/`.

## Five tabs, three surveys

| Tab | Cards | Source |
|---|---|---|
| Payroll (default) | employment tree (839 industries), hours and earnings tree (94) | CES |
| Household | labour force status, rates by group, composition, U-1 to U-6 | CPS |
| JOLTS | industry, establishment size, region | JOLTS |
| Derived | vacancies per unemployed, gross flows, Beveridge, CES vs CPS | all three |
| Appendix | 16 drawers | — |

Payload is 11,7 MB with the `{i0, v}` compression from `analytics/brasil/expectations`
(26 MB without it: the CES starts in 1939 and most industries in 1990, so a full array
per series was mostly the word `null`). Hours and earnings ship only to tree level 4 —
94 industries against 549, the granularity the release's own B-2/B-4 tables publish; the
database holds all of them.

## The payroll tree is the hard part of this branch

**`display_level` + `sort_sequence` builds a WRONG tree for the CES.** The four
level-1 nodes are overlapping aggregates: Total private, Goods-producing,
Service-providing and Private service-providing add to **257% of total nonfarm**. And the
naive rule makes *Mining and logging* a child of *Private service-providing*. So the top
is declared in `mt_ces_dim._TOPO` and everything below derives — with a stack reset on the
declared nodes, without which `Government` (declared, and at display_level 2) does not
reset and *Federal* inherits *Other services*, taking that parent's coverage to 485%.

Two kinds of exception, and they are different:

- **A second axis cannot live in the tree.** `Service-providing` = private services +
  government crosses the Total private boundary; the ten `part 238` construction rows are
  a residential/non-residential cut of the same NAICS subsectors, and both cuts close on
  the same parent (163% stacked). They get `alternativo = 1` — still loaded, out of the
  hierarchy. Same treatment the FX report's BOP tree gave the line that crossed two
  functional categories.
- **A missing level has to be inserted**, and the data says where: `Health care` (621,2,3)
  is printed as a *sibling* of its own three children and is exactly their sum in 439
  months. Four such corrections live in `_CORRECOES`, and `_validar_correcoes()` re-derives
  each identity on every load — a declaration with a numeric guard, not a hand-list.

## Additivity is a raw-data guarantee only

The BLS seasonally adjusts each series **independently** and footnotes it. Measured over
the 284 parents:

| | worst excess of children over parent | parents over 0.05% |
|---|---|---|
| not adjusted | +0.068% | 1 |
| adjusted | +15.5% | 222 |

So the tree is validated on the raw series and the adjusted deviation is *stored*
(`desvio_sa`). Validating on the adjusted data fails a correct tree — that happened on the
first run, with 12 parents "overlapping" at 100.3-101.7%. The same effect shows up in the
CPS status block (employed + unemployed = 169,093 against a published 169,094), so its
stacked view is honest only to about a thousand, and the note says so.

Coverage is a column, not an exception: 260 of 284 parents close in every month, and in a
complete month the 555 leaves are **97.8%** of total nonfarm.

## Two things about the CES calendar and shape

**There is no single "last month".** The first release of a month carries the aggregates
and the detail arrives with the next one: levels 0-4 all have the newest month, level 5 has
54 of 241, levels 6-7 have none. So `_grade()`'s JOLTS rule — raise if the cuts do not
share a window — would reject a correct pass, and `_grade_simples()` exists for that. The
chart header prints how many of the 839 rows the newest month has.

**Only 4 of 13 measures add across industries** (employment and the three aggregates);
every average per worker and every index does not, so stacked bars and "% of total" are off
for them, with the reason on the disabled control. And **nothing accumulates over 12
months** — employment is a stock and the rest are weekly rates — so that reading is
disabled across the whole survey.

## The household survey: what the release check caught

Every one of the 43 CPS concepts is verified against the number printed in the release
before it is stored, and that found **three series whose names read right and whose
concepts are wrong**: "part time for noneconomic reasons" is the *at work 1-34 hours*
series (22,770) and not the similarly-named one (22,345); "15 to 26 weeks" is not the
series named "15 weeks & over" (1,157 vs 2,929); and marginally attached/discouraged have
seasonally adjusted versions, which is what the summary table prints (1,806 and 476 against
1,871 and 503). None would have raised an error.

**October 2025 does not exist in this survey** — the shutdown cancelled collection. That
kills *two* monthly changes, and `_mensal()` in `derivadas_tab` exists because `.diff()` on
a series with the month absent computes November minus September and labels it a monthly
change: 104 thousand where the quantity does not exist.

## The derived tab, and the one external answer key

Four metrics, each crossing surveys. Only the first can be checked against the source, and
**the published series is the reciprocal of the quoted one**: the BLS publishes *unemployed
persons per job opening*, so July 2009 reads 6.50 where vacancies per unemployed person was
0.153. `conferir_uo()` caught the inversion on its first run (mean error 1.58) and now
compares in the BLS's own direction, where the tolerance is not invented — the bureau
publishes one decimal, so the bound is 0.05, and the measured max is exactly 0.05. The
check earns its keep because **the ratio is near 1 today** (1.05 against a published 0.95),
where an inversion looks perfectly normal.

## Scope of the first round (JOLTS), kept for the record

*"Por enquanto, vamos somente pegar os dados. Na sequência vamos pegar os outros dados de
emprego e aí construímos métricas derivadas."* That is why the JOLTS tab still has no
derived metric of its own — the derivatives live in their own tab, built on all three
surveys, which was the point of waiting. **State estimates were offered and declined**
because all 51 series stop in December 2025.

**Two tabs: JOLTS and Appendix.** The JOLTS tab stacks the three cuts as three cards, each
its own table + chart:

| Card, in order | Tree | Root | Rows × levels |
|---|---|---|---|
| Industry | `mt_jolts_dim`, `corte='industria'` | Total nonfarm | 28 × 4 |
| Establishment size | `corte='tamanho'` | **Total private** | 7 × 2 |
| Region | `corte='regiao'` | Total US (nonfarm) | 5 × 2 |

All three run the same JS factory (`makeJoltsTab`), with five pill groups each: **Measure**
(the 6 published measures) × **Type** (Level / Rate / % of total) × **Adjustment** (SA /
NSA) × **Reading** (Monthly / M/M / 3M avg / 12M avg / 12M total / Y/Y) × **Chart** (Lines /
Stacked bars).

There is **no KPI strip** — it was removed at user request on 2026-09-01. The harness
asserts the CSS and `renderKpis()` do not come back as dead code.

They were three separate tabs until 2026-09-01, when the user asked for one. What the split
was carrying is **that the three cuts have different roots** — Total nonfarm, Total private,
Total US — so their totals are not the same quantity and a single set of controls over one
table would say they were. Stacked, each card keeps its own heading, its own note and its own
five pills, which is what preserves that; the thing to *not* do is factor the controls up to
the tab. `tests/test_labor_market_us_js.js` §1 asserts the three charts sit in one
`<section class="panel">`, that there are three cards, and that each still carries all five
pill groups — a card that escapes the panel disappears from the page with no error, and one
that loses a pill group still renders.

## Four things worth not re-deriving

**One measure is a stock and five are flows, and the controls have to know.** Job openings is
the position on the last business day of the month; the other five count everything that
passed through the payroll during the month. Summing 12 months of openings gives **12.0×** the
level (measured, asserted in the JS harness) and still looks like a plausible openings chart.
So `12M total` is disabled for openings — driven by `y_acum: None` in `jolts_tab.MEDIDAS`, not
by a `.replace()` on the axis title, which would fail silently and leave the monthly unit on
an accumulated chart. It is disabled for every rate too: adding twelve ratios produces no
ratio. Both disabled pills stay on screen with the reason in the `title`; the state falls back
to Monthly rather than sitting in an impossible combination.

**The three cuts share their root series, and a 1-to-1 map loses one.** `JTS100000000000000JOL`
(Total private) is a node of the industry tree *and* the root of the size tree;
`JTS000000000000000JOL` is the root of the industry tree *and* of the region tree. The first
load used `dict[series_id] → destino`, so `tamanho` and `regiao` overwrote `industria`, which
lost **Total private entirely** (7,392 rows) and kept a Total nonfarm of 308 rows — only the UO
series, the one no other cut claims. Nothing raised; the cut just came without a root.
`mt_jolts._long` now maps to a **list** of destinations, and `run()` asserts every dim category
has rows.

**The size-class root is Total private, not Total nonfarm** — the BLS produces that cut for the
private sector only, and the difference is 810 thousand government openings (asserted as an
exact literal in `tests/test_jolts.py`). That is also why the info-card keys are **namespaced**:
`00` is a category in two cuts meaning two different things, and a bare-key map would have one
table explain the other with no error at all.

**The rate denominators were measured, not paraphrased.** Implied employment comes out of
`hires level / (hires rate / 100)`, and with it `openings / (employment + openings)` reproduces
the published openings rate to **0.038 p.p.** mean absolute error over 8,624 cells, against
**0.150 p.p.** for `openings / employment` — 4× worse. The five flow rates reproduce as
`flow / employment` at 0.027–0.035 p.p. The residual is the rounding of the published
one-decimal rate. So the axis titles (`openings / (employment + openings), %`) are a tested
claim, and the Appendix prints the table.

## "% of total": the denominator is the tree's own root

Third value in the Type pill, added 2026-09-01 at user request (*"quanto Mining & logging
representa das vagas abertas"* — 0.30% of total nonfarm openings in July 2026). It is **not a
type in `mt_jolts`**: it is the level divided by the level of the root of the *same* tree,
derived in the browser under the synthetic series key `corte|cat|medida|share|ajuste`, which
is what lets `serieTransformada()` and its cache keep working without knowing the series is
derived.

Three things this got right that are worth not re-deriving:

- **The denominator is per tree, not per page.** Total nonfarm for industry, Total private for
  size class, Total US for region. A single shared denominator is the silent failure here: the
  six size classes would sum to **88.86%** instead of 100%, the missing 11.14% being government
  — a sector that cut does not cover. Nothing raises; the numbers just read low. Asserted three
  ways (root reads exactly 100, level-1 siblings sum to 100, and the size classes sum to 100
  and *not* to 88.86).
- **Stacked bars are valid for a share and not for a rate**, and the reason is the denominator:
  sibling shares all divide by the same root, so they add; sibling rates divide by each
  category's own employment, so they add to nothing. This is the first control on the page
  whose validity differs between the two ratio types.
- **The transforms apply to the share, not to the levels behind it.** A 3-month average is the
  mean of three shares, not the ratio of two means — the two differ in the fourth decimal on
  the current month, which is why the harness compares against both and requires the first.
  `12M total` stays disabled (adding twelve shares produces no share) and Y/Y is in **p.p.**

The axis title comes from `y_share` in `jolts_tab.MEDIDAS`, a template carrying `{raiz}`
resolved in JS against the tree's root label, so the axis names the denominator the series
actually used. `tests/test_jolts.py` requires the placeholder to be present in all six — an
axis that says only "share of the total" cannot tell the reader which total.

One honest caveat, measured: the BLS rounds every level to the thousand, so sibling shares sum
to 100 within **0.15 p.p.** everywhere except *other separations*, whose total falls to 168
thousand and whose worst month is **1.07 p.p.** (size classes, NSA, Nov 2024). The levels
behind it are inside the rounding tolerance the load enforces — the amplification is the small
denominator, not a defect. Stated in the Appendix.

## M/M is a DIFFERENCE, and that decides where stacked bars are legal

Added 2026-09-01 at user request, as a sixth Reading. It is `v[i] - v[i-1]` in all three
types — thousands for a level, percentage points for a rate or a share — and never a percent.
That is the release's own headline shape (job openings **+89** thousand in July 2026, hires
−278, quits −157, all asserted as literals) and it is the reading the removed KPI strip used
to show.

The reason it must not be a percent is legibility, not arithmetic: a level in thousands and a
percentage change of it are indistinguishable in a chart legend, and `+89` meaning *89
thousand more openings* versus *89% more* is a 100× misreading that looks perfectly normal.
The axis title carries the distinction (`change vs. the previous month, thousands` vs `p.p.
change vs. the previous month`) and the harness requires the level version to contain
"thousands" and **not** contain "%".

**Adding it forced the stacked-bar rule to be stated properly, and one branch of the old rule
was making a false claim to the reader.** Additivity across siblings is a property of the
base, and a *difference* of things that add also adds:

| | adds across siblings? |
|---|---|
| level | yes (and so does its mean, its sum and its M/M) |
| share of total | yes — every sibling divides by the same root, so M/M and Y/Y in p.p. add too |
| rate | never — the denominator is each category's own employment |
| **% change** of a level | no — the parts have no percentages that sum to the total's |

So `barrasOk()` is now three lines that say exactly that, and bars became available for a
share under Y/Y, where the previous rule blocked them and the tooltip explained the block with
*"percentage changes do not add across siblings"* — a sentence that is true of a level's Y/Y
and false of a share's, since that one is a p.p. difference. The bug was in the **stated
reason**, and it was visible on screen. Worth generalizing: a disabled control's tooltip is an
assertion about the data, and it ages the same way prose in a card does.

## The interaction model, and why the harness asserts on windows

Everything from `.claude/rules/lis-dashboards.md` is in place from the start: `dragmode:'pan'`
+ `scrollZoom:true`, `_bindYAutofit` from `analytics/report_structure/y_autofit.js` via the
`/*Y_AUTOFIT_JS*/` marker, HTML range buttons **below** the chart, and **no**
`xaxis.rangeselector` and no `autorange` anywhere.

Two details this report adds to the pattern:

- **The extent comes from `gd.data`**, never from the `dates` array the caller passes — a `y`
  of null still has an `x`, which is the "fourth face" of the range bug. The right edge is
  padded by **half the plotted series' own step** (15 days on a monthly series), because bars
  are centred on their `x` and a window ending exactly on the last point cuts the last bar in
  half.
- **The chart title is rebuilt on every render too**, not just the subtitle and the period. The
  measure is a selector here, so a fixed title would start lying on the first click. The rule
  is "no text a click can contradict", not "the title is sacred".

`tests/test_labor_market_us_js.js` (324 assertions) asserts on the window each button
*produces* and on the window the **first paint** applies — in a second, clean vm context, before
any click. Verified to fail on five mutants: `autorange` restored on first paint, the range bar
moved above the chart, `12M total` enabled for a stock, stacked bars enabled for rates, and a
duplicated palette entry.

## Colours

`assignSeriesColors` from position, root pinned to `PALETTE[0]` (brand navy), 14-colour palette
closing at ΔE2000 20.8. The industry tree has **28 rows**, so this is the first report here that
actually reaches past 13 series and exercises `line.dash` as the second channel — the harness
ticks all 28 and asserts more than one dash appears, because no default view gets there and a
test that only inspects the initial render passes with `dash` deleted.

## Pending

- **Real-browser confirmation.** No browser in this environment. Worth checking in particular:
  the stacked-bar view with the root drawn as a line over its own parts, the info card's
  position when the table is scrolled horizontally, and the pill `i` button's contrast on an
  active (navy) pill.
- **The `UO` series is loaded and not shown.** `mt_jolts` carries the BLS's own *unemployed
  persons per job opening* ratio (`medida='UO'`, `tipo='razao'`, SA only, national and by
  state). It is out of this page by scope decision — it depends on the household survey, which
  is the next data round. Its one gap (October 2025, the appropriations lapse) is already
  documented in the Appendix.
- **No standard errors.** The BLS publishes median standard errors for JOLTS separately
  (`www.bls.gov/jlt/jolts_median_standard_errors.htm`). A month-on-month move in a small
  industry — mining and logging is 22 thousand openings — is frequently inside them, and the
  report currently says so in prose without showing the number. Loading them would let the
  table grey out moves that are not significant.
- **Real-browser confirmation of the new tabs.** Same gap as the JOLTS round, now over
  more surface: the 839-row payroll tree scrolled and expanded, the Beveridge scatter (the
  only chart on the page whose X is not time, and the only one without a time ruler), and
  the CPS population row showing dashes in the adjusted view.
- **What the CES load leaves out, by scope decision**: production and non-supervisory
  workers (tables B-6 to B-9 — the earnings series that goes back to 1964 against 2006 for
  all employees), women employees (B-5), and the diffusion indexes. All three are in the
  same flat files, so adding them is a datatype in `mt_ces._MEDIDAS`, not new plumbing.
- **The CPS is loaded at headline depth only** — 43 concepts of 68,630 series. The
  demographic cross-tabs (race × sex × age × education × veteran × disability × nativity)
  are a project of their own and nothing on this page consumes them.
- **Still missing from the branch**: weekly claims, ECI, productivity. Claims are the only
  weekly series in the area and would be the first non-monthly grid here.
- **Next cuts from JOLTS itself**: nothing else is published nationally, so expansion there
  means the other surveys, not more JOLTS.
