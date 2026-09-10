# analytics/us/labor_market/ — US Labor Market report

Second report under `analytics/us/`. Built 2026-09-01 with JOLTS only; the payroll and
household surveys plus the derived metrics were added the same day, and the productivity
release on 2026-09-03. Reads `mt_jolts`, `mt_ces`, `mt_cps`, `mt_produtividade` and the
two dimension tables; writes `reports/us/Labor Market.html` (12,1 MB, ~105 s).

```powershell
uv run python -c "from analytics.us.labor_market.generate_report import run; run()"
uv run python tests/test_jolts.py                 # 51 assercoes, precisa do banco
uv run python tests/test_produtividade.py         # 47 assercoes, precisa do banco
node tests/test_labor_market_us_js.js             # 389 assercoes, precisa do HTML gerado
```

**UI in English**, like `analytics/us/inflation/`. The three source releases live in
`referencia/` (the repo-wide convention: nothing reads that folder) —
`jolts_2026-07.pdf`, `employment_situation_2026-07.pdf` and
`productivity_costs_2026Q2R.pdf`, which are the documents every published literal
in the two test suites was read off.

## Six tabs, four surveys

| Tab | Cards | Source | Frequency |
|---|---|---|---|
| Payroll (default) | employment tree (839 industries), hours and earnings tree (94) | CES | monthly |
| Household | labour force status, rates by group, composition, U-1 to U-6 | CPS | monthly |
| JOLTS | industry, establishment size, region | JOLTS | monthly |
| Productivity | sector table + chart, business-cycle comparison | MSPC (`prod2`) | **quarterly** |
| Derived | vacancies per unemployed, gross flows, Beveridge, CES vs CPS | all three monthly | monthly |
| Appendix | 21 drawers | — | — |

Payload is 12,1 MB with the `{i0, v}` compression from `analytics/brasil/expectations`
(26 MB without it: the CES starts in 1939 and most industries in 1990, so a full array
per series was mostly the word `null`). Hours and earnings ship only to tree level 4 —
94 industries against 549, the granularity the release's own B-2/B-4 tables publish; the
database holds all of them.

## Productivity: the first quarterly tab, and the first whose pill picks a SERIES

`mt_produtividade` (BLS/MSPC, the `prod2` release) broke two assumptions the page had
carried since it was built, and both cost a parameter on `makeGenericTab` rather than a
second factory:

- **Quarterly, not monthly.** `opt.fmtCol` (column header), `opt.fmtHover` (the hover
  label) and `opt.nCols` replaced hardcoded month formatting. The hover label is built in
  JS rather than with Plotly's `%q` specifier, which is not in the 2.35.2 bundle as far as
  a grep can tell and cannot be verified here without a browser — so the column header and
  the hover come from the same function and a test compares both.
- **The reading pill selects a published series instead of computing one.**
  `opt.calcTransform: false` puts `state.transform` into `opt.chave()`, so clicking Y/Y
  reads the BLS's own year-over-year series. The source publishes all three readings for
  every quantity — they are the three panels of every table in the release.

The precision story here was measured, and the first version of these notes had it
**backwards**: the flat file carries the index at **three** decimals and the two growth
rates at one. Rebuilding a growth rate from the file's index agrees with the published one
to 0.0500 p.p. and never more — the residual is the rounding of the *published rate*.
What errs is rebuilding from the index **as printed in the release PDF** (1 decimal): mean
0.27, max **1.35 p.p.** So the reason to carry three series is that the published number
is the citable one, not that the arithmetic fails.

### Nothing on that tab adds up, for two independent reasons

The six sectors **contain** one another (business ⊃ nonfarm business ⊃ manufacturing and
nonfinancial corporations), and the one pair that genuinely partitions — durable +
nondurable = manufacturing — still does not add, because what is published is an index:
the ratio averages **2.02**. So stacked bars, "% of total" and the parent-becomes-a-line
rule are all off across the tab, with the reason on the disabled control. It is the
cleanest case in the repo of the rule that a control's validity is a property of the data.

### "Productivity = output − hours" is the release's own wording and errs by 15.9 p.p.

The text writes the identity as a subtraction, and 1.7 − 0.3 = 1.4 exactly. The true
relation is a ratio. Measured over 317 nonfarm quarters and 157 durable ones: subtraction
is off by 0.14 p.p. on average and **15.9 p.p.** at worst; the ratio form closes to 0.04 /
0.18. The worst case is durable manufacturing in 2020 Q3 — output +91.3%, hours +37.1%,
subtraction says +54.2%, published is **+39.5%**. Both forms are asserted, so a future
"simplification" to the subtraction fails instead of producing a plausible number.

### One "Output" row, two output concepts — and the catalogue says so

Measures 04/05/14 (value added) exist only for business, nonfarm business and nonfinancial
corporations; 21/22/23 (sectoral) only for the three manufacturing sectors. No sector
publishes both, so the release's prose warning that they are not comparable is visible in
which series exist. The table merges each pair into one slug and carries
`conceito_produto` on every row; the chart subtitle prints the warning **only when both
concepts are actually plotted**, which is the default view. Four more measures (profits,
unit profits, unit nonlabor costs, unit combined input costs) are nonfinancial-corporations
only — Table 6 — and their pills stay on screen disabled.

### The business-cycle card is the release's charts 3 and 4

Each bar is the annualized rate **between the endpoints** of its window, not the average of
the quarterly rates (which differs by ~0.06 p.p. on nonfarm productivity since 2019). Ten of
those rates are quoted in the release text and `_ciclos()` **refuses to build the payload**
unless it reproduces all ten — a wrong window produces a plausible number, so this is not a
test-only check. The long-term window starts at each sector's own first quarter (1947 Q1 for
business, 1987 Q1 for manufacturing), which is what the release quotes and what the axis
label prints; a fixed date would give manufacturing a span its data does not cover.

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

## The 7 metric layers — the two CES tabs (2026-09-04)

`Payroll employment — CES` and `Hours and earnings — CES` are on the layered control model from
[`design-system.md#metricas`](../../../.claude/skills/lis-dashboard/references/design-system.md#metricas).
The other 10 tabs still carry the old pill bar, deliberately, so the two models are comparable side
by side.

What the single `Reading` pill was doing wrong: it fused **three** layers into one single-select —
window (`12M total`), comparison (`M/M`, `Y/Y`) and smoothing (`3M avg`, `12M avg`). Because it was
single-select, picking `M/M` excluded `3M avg`, so *"the 3-month average of the monthly change"* —
the standard payroll read — **could not be asked for at all**, and nothing about the UI said so.

The tab now renders five `<select>`s: Adjustment · Denominator · Comparison · Smoothing · Chart.
Reachable states went from 20 to **48**, with no option invented — the gains are the compositions
(3M/12M average *of* a change or of a Y/Y), plus `Change Y/Y` in thousands of jobs, which the old
`Y/Y` never produced on a level, and `% M/M`, which the old `M/M` never produced either.

Four things this pilot established that the next tab should reuse:

- **The descriptor was already written and the JS ignored it.** `ces_tab.py` and `jolts_tab.py`
  declare `natureza` (estoque/fluxo/media/agregado/indice) and `aditivo`, but the controls keyed off
  the *absence of an axis label* (`y_acum: None`, `y_share: None`) instead. `opt.desc(state)` now
  builds the layer set from `natureza`/`aditivo`, and the labels are consequences rather than causes.
- **Two different reasons for an option not to be pickable, and they look different on screen.** A
  layer the data never offers renders **nothing** (Measure, because this family has one measure;
  Window, because employment is a stock; Basis, because it is not money) — that is what removes the
  lonely one-pill group and the permanently-greyed `12M total`. A layer whose option is invalid
  *given the other layers* renders **greyed with the reason** (`% M/M` while the denominator is a
  share).
- **Moving from pills to selects loses the tooltip.** A disabled `<button>` shows its `title`;
  a disabled `<option>` does not, in any browser. So the reason moved into the DOM, as a
  `.layer-why` line under the bar — which is also why it is now assertable instead of trusted.
- **The order assertion has to be written on a pair that does NOT commute.** Difference and moving
  average are linear time-invariant filters, so `MA3(Δx) == Δ(MA3(x))` in the interior (measured:
  1,049 months identical) — a test written on that pair passes in both orders. The pairs that do
  discriminate are denominator × smoothing (mean of a ratio ≠ ratio of means: 1,050 months differ)
  and window × comparison.

`tests/test_labor_market_us_js.js` §13b, 37 assertions.

### Hours and earnings added four things the first tab could not show

- **`aditivo` does not mean "already a percentage", and treating it as one was a live bug.** The
  report derived *"this series is a ratio"* from `not aditivo`, and those are different properties:
  average hourly earnings does not add across industries (it is an employment-weighted mean) and is
  measured in **US$**. Measured consequence on 9 of the 12 measures: the monthly and annual change
  came out as a *difference labelled "p.p. change"* for a figure in dollars — and worse than the
  label, **"average hourly earnings up 0.9% from a year earlier" was not obtainable on the page**;
  you got +0.31 called p.p. No CES measure is a percentage, so `razao` now comes from
  `natureza === 'taxa'` and `dif` declares the difference unit per measure (the old nature-switch
  said *"same unit as the level"*, which is true and useless on an axis).
- **The same question must not be answered in two places.** `camadasDe()` read the new descriptor
  while `normalizar()` still read the old `ehRazao`, so the bar *enabled* `% M/M` and the state
  handler *undid* the choice — no error, no visual tell. The emprego tab hid this because its one
  measure is additive, which made the old flag accidentally right.
- **Nominal and real are one measure in two bases, not two measures.** `ganho_hora_real` and
  `ganho_semana_real` left the measure list and became the Real option of layer 1, which renders
  only for those two measures. The precondition was measured first: the BLS publishes the real
  series for the **same 94 industries** as the nominal one, so there is no per-row availability
  problem the layer model could not express. Sticky by design — picking Real, switching to a
  measure with no real counterpart, and coming back keeps Real.
- **Moving a series into a basis layer silently drops it from the payload.** The CES query is driven
  by the measure list, so taking the two real keys out of `ORDEM_HORAS` cost **376 series** (94
  industries × 2 measures × 2 adjustments) and 0.68 MB — and the symptom is not an error: the Real
  option renders and the chart is empty. `ces_tab.medidas_carregadas()` now adds back whatever
  `bases` references.

Also worth keeping: **the measure selector stays outside the layer bar** — measure is upstream of the
pipeline (*entity × measure*, not a layer). §13c, 29 assertions.

### A measure that covers part of the tree needs the tree to say so (2026-09-04)

User report: `Overtime hours`, `Hourly earnings ex-overtime` and `Aggregate overtime hours` rendered
**empty**. The CES collects overtime only in manufacturing, so those three cover **21 of the 94 rows**
of this tab, and none of the default-checked rows (Total private, Goods-producing, Private services)
is among them. Two silent blanks, not one: a chart with no line at all, and a `% of total` that
offered to divide by a Total private overtime series **that does not exist**.

Pre-dates the layer migration — the measures were equally empty as pills. What the migration changed
is that the bar now reshapes per measure, which is what made it visible.

The fix is not to hide the measures but to let the visible tree follow the scope, and it reuses
`opt.filtro`, which existed unused: the tree collapses to the covered subtrees, the root becomes
Manufacturing (and the share denominator with it), the checked set falls back to rows that exist, and
the chart header prints *published only within Manufacturing*. Two things made this safe to derive
rather than declare: the covered set is a **complete single-rooted subtree** (measured: no dataless
child under a parent with data) and the three measures cover **exactly the same** 21 rows. The
assertion that proves the denominator moved is that the root reads exactly 100. §13e, 24 assertions.

### And the control's FORM follows its width (2026-09-04, user request)

From a screenshot of the 10 measure pills wrapping to a second line. A pill group must fit one line;
above that the control is a `<select>`, and the switch is **derived from the estimated width** rather
than chosen per tab, so adding an option tomorrow is enough for it to happen. Measured across the
report's 38 control groups: the widest that fits is **763px** (the 6 JOLTS measures, each with a
definition card), and the two that overflowed were **1,752px** (CES hours, 10 measures, 2 lines) and
**2,807px** (productivity, 19 measures, 3 lines) — so any cut between 800 and 1,700 gives the same
answer.

Two consequences worth not re-deriving: a `<select>` shows one option at a time, so it gets **one**
`i` button, for the selected item (an `<option>` hosts no button — without that step the switch
deletes 10 and 19 definition cards in silence); and the harness needed
`escolherNoGrupo(pref, grupo, rotulo)`, which resolves either form, because 15 call sites clicked a
pill that had become an option. §13d sweeps all 38 groups and requires none in pills to exceed the
budget — the defect starts as one option added to a group that fits today.


## The four household tables: the nature is a property of the ROW (2026-09-04)

Same layered model, and the CPS is the case that stretched it. In the CES a tab has one measure at
a time, so `natureza` is a property of the *measure*; here the same block mixes **counts in
thousands, rates in percent and durations in weeks**, and a chart has one Y axis. Three defects came
out of it, all pre-dating the migration and none of them raising anything.

**The label and the arithmetic disagreed, in both directions.** The value was computed per row
(percent change for a level, p.p. difference for a rate) and the axis title per *block* — nothing
reconciled them. In the three non-additive blocks the axis read *"p.p. change"* while the number was
a percent change (Job losers **−5.86%** in the last month); in the additive block it read
*"% change"* while the three rates were coming out in p.p. The fix is two flags rather than one:
`razao` requires **every** plotted row to be a percentage (that is what puts the difference in p.p.)
and `pctMotivo` needs only **one** to be (that is what bans the percent change, because the axis is
single). With mixed units the difference stays available — it is honest in both at once — and the
axis says *"mixed units"* instead of picking the unit of half the lines.

**`naoSoma` is not "is a percentage".** Average and median duration sum with nothing and are measured
in **weeks**, so a percent change of them is a real reading (**+7.35% y/y** in Aug 2026) and it was
being labelled p.p. Same conflation the hours tab had between `aditivo` and `razao`, reached from the
other side: the field now declares *"not a part of the total"* and the `unidade` column — read from
the database, not declared — decides p.p. versus %.

**And `% of total` in the adjusted view of the labour-force block plotted ZERO series.** The
population is the one line the BLS never seasonally adjusts, the adjusted view is the default, and
the division was by a series that does not exist — table and chart entirely blank. Same class as the
overtime case, third path to it. Layer 4 now requires the denominator to **exist in the current
adjustment**, and the greyed control names the way out ("switch to Not adjusted").

Two things measured while writing that, both reusable:

- **The source already publishes two of those ratios, so they are the answer key.** Labour force over
  population *is* the participation rate — matching within **0.069 p.p. across 943 months**, and 0.05
  of that is the source's own rounding (levels to the thousand, rates to one decimal). Employed over
  population *is* the employment-population ratio. This is the rule from
  `.claude/rules/lis-dashboards.md` ("before dividing two series, look for whether the source
  publishes the ratio") holding on the friendly side for once.
- **The denominator need not be a row of the table.** In the composition block the parts sum to the
  *unemployment level*, which lives in the first block; using the visible tree's root would title the
  axis "share of job losers" and make the four shares sum to **220%** (measured). So the block and
  each cut declare the total's key, and `opt.denKey` overrides the root.

Two cuts of unemployment do stack and one does not, and that was measured rather than assumed — the
same audit the CES tree needed:

| cut | raw data | seasonally adjusted |
|---|---|---|
| by reason → unemployed | worst 2k (0.034%), 0 of 391 months over 0.1% | worst 249k (**2.24%**), 340 of 391 over |
| by duration → unemployed | worst 1k (0.019%), 0 of 391 months over 0.1% | worst 384k (**3.09%**), 351 of 391 over |
| part-time status | does not close: the two indented lines are 2 of the 4 published reasons (worst gap 543k, 13.2%) | — |

So stacking and shares are on for the first two, off for the third with the reason on screen, and the
block note tells the reader the adjusted stack is a good picture and not an identity.

Two smaller things the port needed:

- **The checkbox now calls `tudo()`, not `renderTable()` + `renderChart()`.** Once the descriptor
  reads the ticked rows, ticking a rate has to rebuild the bar — otherwise the percent change stays
  clickable and the state is valid in the object and invalid on screen. That forced a guard in
  `normalizar`: the selection fallback fires on *"nothing in scope while something is ticked outside
  it"*, never on *"nothing ticked"*, or unticking the last row by hand re-ticks three by itself.
- **A pure-rate block names its base on the axis.** `% of the relevant base` answers nothing in a
  report with three different bases, so `ROTULO_PCT` carries one short definition per block
  (*"unemployed as a share of that group's labor force, %"*). The generic string stays as the
  fallback.

`Cut` stays in pills: a cut selects *which rows exist*, which is upstream of the pipeline, like the
measure pill on the CES tabs. Covered by §14b of `tests/test_labor_market_us_js.js` (76 assertions),
verified against 9 mutants — including one that only the checkbox path catches, which is why that
assertion fires the real `change` event instead of poking `state.checked`.

**The 6-month average** was added to layer 6 in the same round (user request). It is one line in
three places — the list, the pipeline and the axis label — precisely because that layer never
disables anything and never changes the unit; the 10 tabs still on the old pill bar do not have it
and will get it when they migrate.


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

📄 **Lista completa e datada das pendências, com o contexto para retomar cada uma:**
[`mds/pendencias_2026-09-03.md`](mds/pendencias_2026-09-03.md) — inclui um problema de
calendário achado nesta rodada que é de outra área (`bcb_credit_note` com um
`reference_period` derivado do mês da divulgação em vez do mês entregue, e 2026-05 sem
nenhuma entrada), mais os três erros da rodada e a regra que sai do terceiro deles (um
patch por script cujo texto de substituição contém a própria âncora não é idempotente).
O resumo abaixo fica como índice.

- **The layered bar is on the two CES tabs and the four CPS blocks.** Migrating the other 6 is open
  work: the JOLTS cuts are the interesting ones (a Window layer that genuinely renders, with
  `12M total` greyed only on job openings) and
  productivity is the case
  where the fused pill is *correct* — the source publishes each reading, so Comparison picks a
  series instead of computing. Two decisions are the user's, both recorded in the plan: whether
  `Change M/M` over a `12M total` stays pickable (it reads as acceleration of the window — RTN
  disables it, Investimento offers it with a caption) and whether productivity gains a Smoothing
  layer on top of the published readings.
- **Real-browser confirmation.** No browser in this environment. Worth checking in particular:
  the five selects on one line at narrow widths, the `.layer-why` line under the bar, and
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
- **Still missing from the branch**: weekly claims and the ECI. Claims would be the only
  **weekly** grid here (productivity, added 2026-09-03, is the first non-monthly one).
- **Productivity: the annual average is loaded and not shown.** `mt_produtividade` carries
  `periodicidade='anual'` (Q05, 16.555 rows, complete years only), and the tab reads the
  quarterly grid alone. Showing it needs a pill, not new data.
- **Total factor productivity is a different release** (`mp` survey, annual, published in
  March) and is not loaded. So is industry-level productivity (`ip`, 40 MB) — that one
  would be the first place this page could cross productivity with the CES industry tree.
- **Next cuts from JOLTS itself**: nothing else is published nationally, so expansion there
  means the other surveys, not more JOLTS.
