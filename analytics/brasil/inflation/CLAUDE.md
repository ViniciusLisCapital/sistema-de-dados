# analytics/brasil/inflation/ — Panorama de Inflação

IPCA/IPCA-15 decomposition report: self-contained HTML that reads MySQL (`macro_brasil`) plus one local CSV. Same `/*REPORT_DATA*/` template pattern as `analytics/brasil/exchange_rate/` — no Jinja2. Since 2026-08 this is the pilot for `analytics/report_structure/` (shared build-time scaffolding — theme CSS, `_bindYAutofit`, the substitution/write-out plumbing); see [`../report_structure/CLAUDE.md`](../../report_structure/CLAUDE.md).

## Generate the report

```powershell
uv run python analytics/brasil/inflation/fetch_bcb.py               # refresh data/ipca_bcb_series.csv — NOT scheduled, run manually
uv run python -c "from analytics.brasil.inflation.generate_report import run; run()"
# Output: reports/brasil/Inflation.html (self-contained, ~99 MB as of the
# 2026-07 historical extension back to ago/1999 — up from ~14 MB, since the
# now much longer decomposition records embedded as inline JSON are the
# bulk of it. Flagged, not yet addressed: emailability is a real concern
# at this size.)
```

`inflc_decomposicao`/`inflc_dim` (MySQL) are already refreshed by `jobs/update_db.py` — only the BCB/SGS aggregates CSV needs the manual `fetch_bcb.py` step above.

## Architecture

`generate_report.py` reads two sources and hands the result to `analytics.report_structure.builder.render_report()`, which substitutes `/*REPORT_DATA*/` (plus `/*THEME_CSS*/`/`/*Y_AUTOFIT_JS*/`, see Visual design/Chart zoom-pan below) in `report.html` — no templating engine, just marker substitution:

- `_load_decomposicao()`: pulls `inflc_decomposicao` (facts) and `inflc_dim` (dimension) via `MySQLDataRequester`, joins them in pandas (`merge` on `subitem_codigo`, the PK — not the old text key) — not in SQL. Reconstructs the display `subitem` string (`"<codigo> <nome>"`, e.g. `"1101002 Arroz"`) right after the merge from `subitem_codigo` + `inflc_dim.nome` (always the current/latest IBGE wording) — `report.html` only ever consumes `subitem` as an opaque display/grouping string, so this reconstruction is invisible to the front end.
- `_load_bcb()`: reads `data/ipca_bcb_series.csv`; returns `{}` if the file is missing rather than raising — the report just skips BCB-sourced charts.
- `_compute_ipca15_nucleos()`: derives EX-0/EX-01/EX-02/EX-03/EX-FE (+ EX-03 subcomponents) for IPCA-15 from `_load_decomposicao()`'s already-merged dataframe (not a third MySQL read) — see Gotchas. Runs through `fetch_bcb._apply_stl_ma3()` (imported, not duplicated) and gets merged into the same `data["bcb"]` dict the CSV populates, so front-end code treats it exactly like a BCB series.
- `_compute_p55()`/`_compute_difusao()`: index-agnostic (take `indice` as a param), so the same function computes either full-IPCA or IPCA-15 — used to validate against BCB's official full-IPCA series before trusting the IPCA-15 output (see Gotchas/Pending). P55's result feeds the same `nucleos15`/STL/`computeYoY` pipeline as the exclusion núcleos; Difusão deliberately does not — it's not a price-change series, so `run()` stores it in `data["bcb"]` unprocessed for `report.html`'s existing `movingAvg()`-based display instead of `computeYoY`/`compute3mSAAR`.
- `_load_decomposicao_item()`/`_compute_ma()`/`_compute_ms()`/`_compute_dp()`: same index-agnostic-validate-then-trust pattern, but at the item (4-digit) level via the separate `inflc_decomposicao_item` table (see Gotchas for why item, not subitem). `_trim_20_80()` factors out the shared MA/MS trimming step (sort, cut 20%/80% by cumulative weight, correct the two boundary items' weights) since MS is just MA with one column (`var_ms`, the smoothed variation) swapped in for `var_mensal`. `_compute_dp()` takes an explicit `headline` param rather than always using the same índice's own — see Gotchas for why.
- `_compute_ipca15_grupos()`: Livres/Monitorados/Alimentação/Serviços/Industriais for IPCA-15, same `_weighted_avg_by_group()` basis as `_compute_ipca15_nucleos()` (both now share it) just keyed on `grupo`/`subgrupo` instead of `nucleo_*` flags. Feeds the "Componentes — 3M SAAR" chart and the Heatmap's "Grupos" section for IPCA-15 — see Gotchas for why this didn't exist before 2026-07.

## Report structure (`report.html`)

Four tabs since 2026-08, driven entirely by the JSON payload above (no server, no build step):

- **Decomposição** — a **hierarchy table** (see *The index tree* below, which replaced `chart-waterfall` and its click-to-drill navigation in 2026-08) plus the monthly contribution stacked bars, now driven by depth pills (`barmode:'relative'`, not `'stack'`, so negative-contribution categories render below zero correctly). Also has its own full-width scatter, "Dispersão — Momentum 3M × Variação 12M" (`computeScatterMomentum`/`renderScatterMomentum`, added 2026-08): one point per subitem, X = trailing-12M chained variation, Y = 3-month momentum annualized via the same MA(3)-then-`^12` formula as `compute3mSAAR` — but on the raw (non-seasonally-adjusted) weighted monthly rate, since running STL per subitem client-side isn't practical (~377-614 subitens). Points are colored by cycling `GROUP_COLORS`, not a fixed semantic mapping — a rough visual aid, not a legend. On-chart text labels are shown per-point via `scatterLabelVisibility()` (crowding-based, not a fixed point-count cutoff — a point's label is suppressed only if another point falls within a small radius of it, normalized by each axis's own data range; hover always shows the label regardless, via a separate `hovertext` field). **Real Plotly bug found and fixed 2026-08**: rendering used `Plotly.react()`, which silently fails to create any text nodes when transitioning FROM a trace whose `text` array is all empty strings (e.g. the initial "Todos" render, ~377 crowded points, every label suppressed) TO one with some non-empty entries (e.g. after switching Filtro BCB to a smaller, less-crowded category) — reproduced in an isolated minimal Plotly page outside this report, so it's a library diffing quirk, not a mistake in the trace construction. Fixed by using `Plotly.purge()` + `Plotly.newPlot()` instead of `react()` for this chart specifically (harmless here, unlike the time-series charts elsewhere that rely on `react()` + `_bindYAutofit` to preserve zoom/pan state — this chart has none worth preserving across re-renders). **Controls, redesigned 2026-08 (four rounds same day)**: level was originally a Grupo/Subgrupo/Item/Subitem dropdown, now fixed to Subitem only — the *set* of subitens shown is chosen instead via the same "Filtro BCB" category dropdown (`scatter-bcb-sel`/`scatterBcbKey`, `_YOY_BCB_FILTERS`) already used by the ranking table and Y/Y drilldown (see Data map below). An earlier version of this control was a 377-614-item checkbox multiselect (`scatterItems`, mirroring the Y/Y drilldown's "Componente" picker) — replaced same-day at user request in favor of the coarser, already-established category filter; its markup, CSS (`.multiselect-panel-actions`), and JS (`populateScatterItems`/`renderScatterItemsPanel`/`updateScatterItemsButtonLabel`) were all removed, not left dead. The anchor month (`scatterMonth`) is a styled `<select>` (`scatter-month-sel`, one `<option>` per calendar month formatted "Mmm/AAAA" via `formatMonthLabel()`/`_MESES_ABREV`, populated by `populateScatterMonthOptions()`) rather than a native `<input type="month">`, paired with quick-jump pills ("1a"/"3a"/"5a"/"10a"/"Tudo", `yearsBackDate()`/`earliestValidScatterAnchor()`/`clampScatterAnchor()`) that jump the anchor back N calendar years from the latest month ("Tudo" = the earliest month with a full 12-month trailing window) — adapted from the `quickRangeOptions()`/pill pattern in `.claude/skills/lis-dashboard/references/design-system.md`, which is written for a *range* (De/Até) rather than this chart's single anchor point, hence the reinterpretation as backward jumps instead of a `[from,to]` window. Selecting anchor/subitens still ignores the Período pills, same reasoning as the top KPI cards — a momentum snapshot at a chosen point in time, not a period aggregate. **A dashed OLS regression line was added, then removed the same day** at explicit user request, after discussion: R² in this cross-sectional (subitem-at-a-point-in-time) setting measures how tightly categories' trailing-12M inflation predicts their current 3M momentum — i.e. roughly a breadth/synchronization read (closer in spirit to the diffusion index in Núcleos & Difusão) — not a "gaining/losing momentum" dial; a rising R² can just as easily accompany a negative slope (broad-based deceleration) as a positive one, and it's unweighted (a 0.01%-peso subitem counts the same as a 5%-peso one) and unstable at low n. Judged not worth the misread risk for this report; `linearRegression()` was deleted rather than left dead in the code. **Known gotcha, fixed 2026-08**: an earlier version wrapped this chart in a portrait `.chart-card--vertical` (`max-width` + `margin:0 auto`) meant to make it taller-than-wide — misreading of a user request that actually meant the *waterfall's* bar orientation, not this chart's aspect ratio. That CSS combination, inside this report's `section { display:flex; flex-direction:column }`, interacted badly with the inner Plotly div's `width:100%` (a shrink-to-fit parent sizing against a percentage-width child is circular/indeterminate in CSS), leaving the container full-width but the actual rendered chart narrow and pinned to one side — a real rendering bug, not a design choice. Removed; the chart now uses a plain `.chart-card` like every other chart in the report. A second, unrelated bug from the same editing pass (JS `Plotly.react` layout height left at a stale value after the CSS height was tuned down) caused the chart to overflow past its card into the section below — fixed by keeping the two in sync; `.chart-card` also got `overflow:hidden` report-wide as a safety net against this exact class of bug recurring.
- **Núcleos & Difusão** — núcleo glossary, a núcleo-picker dropdown (3M SAAR + 12M side by side), and difusão-by-category using the official `nucleo_*` flags (not an approximation from grupo/subgrupo), plus a "Total (sem filtro)" option for the whole-index headline. For IPCA-15, the núcleo charts/dropdown switch to a separate list (`NUCLEO_ALL_15` in `report.html`) backed entirely by in-house series (`_media5`/EX-0…EX-FE/P55/MA/MS/DP, all seven — BCB publishes none of them for IPCA-15), with a disclaimer note (`#nuc15-note`) explaining they're computed, not BCB-published, and validated against the equivalent full-IPCA official series first.
- **Inércia** — subitens ranked by the 12th-order autocorrelation of their own y/y series and cut into five bands of ~20% of the index weight. See *The inertia tab* below.
- **Mapa de Calor** — heatmap of 3M SAAR for Grupos + Núcleos, last 12 months. Each series is z-scored against its own 60-month rolling mean/std (not a shared threshold) — same method as the FRED Blog inflation heatmap, chosen because BCB has no published equivalent to replicate. Index-aware since 2026-07 (`HEATMAP_ROWS`/`HEATMAP_ROWS_15` in `report.html`, see Gotchas) — before that it always showed full-IPCA data regardless of the active tab.

## The index tree (Decomposição tab, 2026-08)

Replaced the **"Decomposição por Período"** chart (`chart-waterfall`, a per-level ranking of bars
you clicked to drill into) with a **hierarchy table** in the same shape as
`analytics/brasil/credit` and `analytics/us/inflation` (`makeHierTab`): expandable row, a checkbox
that plots the series in the chart below, twelve month columns. Direct user request.

**Two trees, with a selector** — they are independent axes and neither derives from the other (a
subitem of "Alimentação e bebidas" can be Livre or Monitorado, and a Livre one can sit in any of
the IBGE's nine groups):

| pill | tree | levels |
|---|---|---|
| **Estrutura IBGE** (default) | the expenditure tree the IBGE publishes | 9 grupos → 19 subgrupos → 53 itens → 614 subitens |
| **Classificação BCB** | the NT-57 analytical one, what the waterfall drilled through | Livres/Monitorados → Alimentos/Serviços/Bens Industriais → durability and subjacência → subitem |

The IBGE one **was not in the database**: `inflc_dim.grupo/subgrupo/item` have always been the
BCB's classification, and the only trace of the IBGE structure was the code itself. Fixed with
three new columns on `inflc_dim` (`ibge_grupo`/`ibge_subgrupo`/`ibge_item`, added by `ALTER TABLE`,
the same route `comercializavel` took in 2026-08) — and **the parentage needed no lookup at all**:
the 7-digit code already carries it as a 1/2/4-digit prefix, the IBGE's own rule and the same one
`inflc_decomposicao.py` uses to detect the subitem level. Only the names come from the API, through
the same `listar_classificacoes()` that already resolved subitem names. Coverage checked: 9/19/53
names resolve all 614 subitens, no orphan prefix.

**The payload did not grow.** `generate_report.py::_ibge_nomes()` ships an 81-entry `prefix → name`
map (~4 KB) and the front end slices the code out of `r.subitem`; the alternative — three strings
on each of 262k records — would cost tens of MB in a file that is already 104.

**Núcleos are a flat block beside the tree, not a branch of it** — they overlap each other and do
not partition the index, so summing sibling rows there would not give the headline (same decision
as the PCE addenda block in `analytics/us/inflation`). The list comes from `activeNucleoList()`
(`NUCLEO_ALL`/`NUCLEO_ALL_15`), so this table cannot drift from the Núcleos tab, and the variation
it reads is BCB's own series — not a parallel reconstruction.

**Four metrics, and the cells that go blank.** Var. mensal (%), Contribuição (p.p.), Var. 12M (%)
and Peso (%). For a tree node all four come from that month's `sum(contribuicao)`/`sum(pesos)`. For
a núcleo, **Contribuição is always blank** (a núcleo is not an additive share of the headline) and
**Peso exists only for the seven exclusion núcleos**, computed from the `nucleo_*` flags the records
already carry — P55, Médias Aparadas and Dupla Ponderação are a percentile, a trim and a
volatility reweighting, not a fixed subset of subitens. Blank, never zero, and the reason sits in
the row's `title`.

**"Evolução Mensal" got depth pills** (Grupo/Subgrupo/Item/Subitem), which is what the waterfall's
drilldown used to do. But that drilldown did **two** things: pick the level *and* filter to one
branch — and it was the filter that kept the Subitem level readable (you arrived there with ~20
subitens of a single item). Without it, Subitem would stack 377-614 traces. Hence the **Top-14 +
"Outros"** cut: whatever falls outside becomes one bar, so the stack stays a complete partition of
the month and the Total line still equals the sum of the bars — asserted in the test for every
month, not just the last.

**Every metric shows two decimals** (user request, 2026-08) — and that has a measured cost, which
is why `decHover` exists beside `dec` in `TREE_METRICS`. Contribution and weight live on a much
smaller scale than a variation: at two decimals, **68.5% of contribution cells at the Subitem level
and 45.3% at the Item level render as "0,00"** (weight loses 11.6% at subitem; monthly variation
loses none). The number is not zero, it is just below half a thousandth of a p.p. — and the sign is
still printed, so a cell reads `+0,00` or `-0,00` and at least keeps the direction. The chart's
hover keeps **three** decimals for contribution and weight, so the precision the table rounds away
is one hover from the same row. If subitem contribution ever needs to be readable straight from the
table, the field to change is `dec`, not `decHover`.

**Reading the table: sign colour and the depth gradient** (both at the user's request, 2026-08).
Cells are **green above zero and red below** — and only on *Var. mensal* and *Contribuição*, where
flipping between a rise and a fall is the information. *Var. 12M* and *Peso* are deliberately
uncoloured: in practice every 12M row is positive, so the colour would be a uniform green wall that
separates nothing, and a weight has no sign. Note this is the **inverse** of the `td.pos`/`td.neg`
convention the ranking table further down the same tab uses (laranja for positive, "inflation
rising"), so the tree table carries its own `v-up`/`v-dn` classes rather than reusing those —
hanging two opposite meanings on one pair of names is how the next edit gets it backwards. **If the
ranking is ever flipped to match, flip the classes there, not here.**

Hierarchy is signalled twice: the indent, and a **background gradient plus label colour that fade
from the total down to the subitem** (`data-depth` on each `<tr>`, emitted from the node itself so
there is no second place to keep in sync). The indent alone was not enough — the table scrolls
inside a 640px card, so the level above scrolls out of view and two rows of similar depth become
ambiguous. Hover is a **gold** tint, not a deeper navy, precisely so it stays distinguishable from
every step of that gradient.

**Both charts put their legend underneath** (user request, 2026-08). The vertical right-hand legend
cost ~190px of plot width *and* truncated its own labels — "Média 5 Núcleos (BCB)" came out cut in
half. On `chart-timeseries` the original justification for the vertical legend (dozens of categories
would wrap a horizontal one across many rows) died with the Top-14 + "Outros" cut: it is at most 16
entries now. Two things the test pins, because both have bitten this report before: the legend must
sit *below* the quick-range pills rather than on top of them, and **the CSS height of the div must
equal the Plotly `layout.height`** — those drifted apart once already and the chart silently
overflowed its card into the next section.

**Node keys are namespaced by level on purpose.** In the BCB tree the label "Monitorados" is a
Grupo, a Subgrupo **and** an Item at once; keying by label alone would collapse the three into one
row. `root` is the only key the two trees share (it is the same index total), so switching trees
resets expanded/checked to the initial state instead of leaving a phantom selection.

**`makeTreeTab()` is a factory, one instance per tab.** It started with the DOM ids hardcoded
inside `renderTreeTable`/`renderTreeChart`; when the Inércia tab wanted the same table over a
**two-level** tree it became a factory in the shape of `analytics/brasil/credit`'s `makeHierTab()` —
per-instance state (source, metric, expanded, checked) and ids passed in. Two consequences worth
knowing: `buildTreeIndex(src)` is shared and caches **two** entries (both tabs can be rendered at
once), and a tree source now only declares how one record becomes a path — `TREE_SOURCES[src].path()`
returns keys and labels of arbitrary depth, plus an optional `ords` that the inércia tree uses to
keep Q1..Q5 in order instead of sorting by weight like the others.

**Verification.** `node --max-old-space-size=8192 tests/test_inflation_js.js` — 179 assertions, this
report's first JS harness. It evaluates the **real** `<script>` from the generated file against a
stubbed document/Plotly, clicks the pills, and asserts on the rows/cells produced and on the traces
the chart received — not on button definitions, per
[`.claude/rules/lis-dashboards.md`](../../../.claude/rules/lis-dashboards.md). The two that earn
their keep: **children sum to the parent in both contribution and weight, for every parent and
every month**, across all three tree × index combinations — the one place a subitem hung on the
wrong branch or counted twice shows up; and **Top-N + Outros closes against the Total line** in
every month. The root reproducing the published IPCA is the third (see Gotchas). Sections 13b/13c/13d cover the inércia tab (13d is the fixed-cut table) — including that the five bands plus the unclassified residual reconstruct the index in every month, and that the tab's note still carries the 24% figure. The *computation* has its own suite, `uv run python tests/test_inercia.py` (44 assertions, `--rapido` skips the database half).

## The inertia tab (2026-08)

A different cut of the same subitens: not what they *are* (IBGE expenditure, BCB analytical) but how
**persistent** their inflation has been. Each subitem is scored by

    r12(k) = corr( yoy_k(t), yoy_k(t−12) )

over a fixed 10-year window (120 y/y observations, 2016-08→2026-07), and the subitens are cut into
five bands carrying ~20% of the index **weight** each. `analytics/brasil/inflation/inercia.py`
computes it; nothing is written to the database — it travels in the payload as ~380 triples
`[r12, faixa, n_pares]`.

**Why the 12th lag of the y/y, and not of the monthly series.** All three alternatives were measured
before choosing, and each fails differently:

| basis | what it actually measures | evidence |
|---|---|---|
| lag-12 on **raw monthly** | seasonality, not inertia | top 8 are all education (Ensino médio 0.94, Ensino fundamental 0.93, Pré-escola 0.87) — items that reprice every February |
| lag-12 on **seasonally adjusted monthly** | almost nothing | mean falls to −0.06, the maximum from 0.94 to 0.29 |
| lag-1 on **y/y** | ~97% construction | consecutive 12-month windows share 11 months: real mean 0.921 against **0.895** on the shuffled series. What is left ranks by print volatility — the bottom is pepino, abobrinha, caranguejo |
| **lag-12 on y/y** ✓ | genuine annual persistence | the two windows are **disjoint**, so there is no mechanical overlap: real mean +0.017 against **−0.147** shuffled, range [−0.70, +0.67] |

Seasonality also disappears for free, because a 12-month window already contains each calendar month
once — there is no STL step in this tab at all. The lag-1 variant was **deliberately dropped** at the
user's request after seeing the measurement; if it comes back it should come back with the mechanical
floor subtracted per subitem, and `inercia.diagnostico()` already computes the benchmark that needs.

**The measure passes the nominal sanity check convincingly.** Q5 is Plano de saúde, Empregado
doméstico, Serviço bancário, Mão de obra, Dentista, Médico, Manicure — labour-intensive services on
annual contracts, the textbook Brazilian indexation set, and their monthly prints are visibly smooth
(Empregado doméstico: +0.51 / +0.53 / +0.55). Q1 is Gasolina (−0.44) and Energia elétrica residencial
(−0.56), which swing on commodities and the bandeira tarifária and revert. Both directions are
asserted in the tests, because an inverted sign would otherwise be invisible.

**Discontinued subitens are not a branch.** 614 subitens have existed since 1999; 377 are live in the
current index, and the other 237 (Vídeo-cassete, Disco laser, Telefone público, dozens of fish by
species) have no data at the end of the window, so no pair to correlate. They used to render as a
"Não classificado" node with 237 children showing nothing but em dashes — removed 2026-08 at the
user's request. They still bump the **root**, because the root is the published index, not the
classified subset; the difference root − bands is exactly that set, and both tables' tests close it
month by month.

### What the tab must keep saying, because it is the least convenient part

**The band is a label for a window, not a property of the product.** Re-estimated on 2006-2016 and
compared against 2016-2026, the correlation between the two estimates is **+0.30**, the same band
repeats in 32% of cases, and **Q5 stays Q5 in only 24%** — against 20% by pure chance. Either the
economy changed between the two decades or the estimator is too noisy to separate them; either way,
read it as "this is how these items behaved in the last ten years", never as "this item is
structurally inertial". On top of that, with ~108 pairs the standard error of each correlation is
~0.10, so the boundaries between Q2, Q3 and Q4 sit inside the noise and only the extremes carry
information. All of this is in the tab's own collapsible note, not just here, and
`tests/test_inercia.py` asserts the instability is still real — **if that assertion ever starts
failing, the note and this section need rewriting, not the test.**

**Inertia is not level.** By 12-month rate the bands do not line up monotonically: Q1 runs 6.48%, Q2
2.65%, Q3 4.29%, Q4 3.26%, Q5 5.52%, against 4.43% for the headline. That is not a defect — high
inertia means the rate persists, not that it is high — but anyone expecting "inertial runs hotter
than flexible" will not find it here. The measure that produced a monotonic gradient in testing was
the lag-1, which is the one that is 97% construction.

### Two cuts of the same r, side by side (2026-08)

The tab carries **two hierarchical tables**, both over the same `r12` and differing only in where
they cut. Neither shows the núcleos block (`semNucleos: true` on both `makeTreeTab` instances) — the
núcleos overlap rather than partition, and say nothing about persistence.

| | cut | bands | consequence |
|---|---|---|---|
| **Faixas de inércia** | equal **weight** (exact DP) | Q1..Q5, ~20% each | limits in `r` move with the sample |
| **Reversibilidade** | fixed limits at **±0,5** | 4 named bands | limits never move; **weight** comes out lopsided |

The fixed cut, measured 2026-08: 6,1% / 24,6% / **66,8%** / 2,5% of the index. Two thirds land in one
band because the distribution of `r` is unimodal around ~+0,02, not bimodal — ±0,5 only catches the
tails. That is a property of the data, and `tests/test_inercia.py` asserts the largest fixed band
still holds more than half the index: if that ever fails, the shape of the distribution changed and
the tab's copy needs rewriting.

**The fixed cut is the less stable of the two, and its own caption says so.** Re-estimated on
2006-2016, the two extreme bands retain **13,3%** and **4,2%** of their members (κ = +0,11 overall,
+0,22 on the sign alone), against 65,4% for the big middle band — which is trivial persistence, since
that band occupies most of the axis. The mechanism is regression to the mean, not noise in the
classifier: whoever clears ±0,5 in one decade is largely whoever caught a tail of the estimation
error, and comes back toward the middle in the next.

### The standard error in the hover understates it by 2-3×

`report.html` prints `1 / √n_pares` — the SE of `r` under H₀: ρ=0, which gives 0,096 at 108 pairs and
0,134 at 56. It is the number quoted throughout this file and in the tab's note as "~0,10". It
assumes **i.i.d. observations, and ours are not**: the y/y series is a 12-month rolling window, so
consecutive observations share 11 months and the effective sample is far below `n`.

Measured with a block bootstrap (blocks of 12, which preserves the overlap):

| | r | 1/√n | (1−r²)/√(n−1) | **block bootstrap** |
|---|---:|---:|---:|---:|
| Empregado doméstico | +0,447 | 0,096 | 0,077 | **0,283** |
| Gasolina | −0,442 | 0,096 | 0,078 | **0,158** |

`diagnostico()`'s shuffled distribution agrees independently: sd **0,242** under the null, not 0,10.
This *strengthens* every caveat above rather than weakening it — with SE around 0,25, the ±0,5 cuts
sit two standard errors from the centre of the distribution, which is exactly why the extremes do not
survive a decade. **Not yet fixed in the payload**: replacing `1/√n` with a per-subitem bootstrap sd
computed in `inercia.py` is a small change and is in Pending.

### Two implementation details worth not rediscovering

**The 48-pair threshold is measured, not chosen.** The distribution of available pairs across the 377
live subitens is **bimodal** — 108 (the whole window) for 315 of them, and exactly 56 for a block of
62. That block is the cohort introduced in the **jan/2020 weighting structure** (Combo de telefonia
at 1.43% of the index, Cabeleireiro 1.12%, Transporte por aplicativo), which only has 79 months of
history in the window. A threshold of 60 would have excluded them as a group and sent 6.75% of the
index to "não classificado" — not for being atypical, but for being new. `n_pares` therefore travels
per subitem and surfaces in the row's hover with the implied standard error, since two estimates in
the same band do not deserve the same confidence.

**Cutting bands by weight took three wrong algorithms before an exact one.** `int(cum/total*n)+1`
pushes every boundary item into the next band (bands of 16.5%–23.4%). A greedy per-boundary choice
improves it but is not globally optimal (21.9% against 18.0%). Coordinate descent on the *maximum*
deviation looked fine against real data (0.94 p.p.) and **failed the simplest possible case** — 100
equal-weight subitens came back as [21, 20, 19, 20, 20] — because on a minimax objective, once one
band sits at the worst deviation, moving any single other cut cannot lower the maximum, so no
individual move improves and the search stops. It is now an exact DP over the sum of squared
deviations, O(bands × n²). Worst real band: 0.94 p.p. off 20%, which is the granularity floor — a
single subitem can carry 5% of the index.

## Visual design

`report.html`'s CSS was rebuilt in 2026-07 onto the LIS Capital dashboard design system (`.claude/skills/lis-dashboard/references/design-system.md`): Barlow/Barlow Condensed/JetBrains Mono typography (Google Fonts), a light `--bg`/`--card-bg` theme replacing the previous full-navy header/tab-nav/footer bars, and the skill's card/label/pill conventions (`.kpi-card`, `.chart-card` headers, `.pill`, `.glossario-toggle`, mono table headers). Same LIS brand hex palette as before (`--lis-azul` `#1F2853`, `--lis-dourado` `#BB9B1D`, `--lis-verde` `#418791`, etc.) — only the chrome around it changed, not the colors themselves. The skill's design system is written for Chart.js dashboards; this report keeps Plotly. Only CSS/HTML chrome and the Plotly `layout.font.family` (now `'Barlow,sans-serif'`) were touched; chart-internal chrome colors (gridlines, rangeselector buttons) were left as literal hex, unrelated to this pass. Not yet applied to `analytics/brasil/exchange_rate/` — same reskin next time it is touched.

**Since 2026-08**, the `:root` palette + base reset/body rules are no longer inline here — `report.html` has a `/*THEME_CSS*/` marker instead, filled in at generation time from `analytics/report_structure/theme.css` (the single source of truth now; edit that file, not this one, to change the palette). See [`../report_structure/CLAUDE.md`](../../report_structure/CLAUDE.md).

## Chart zoom/pan

All Plotly charts here (except `chart-waterfall`, a vertical category-ranking bar chart with no time axis — deliberately excluded, and `chart-scatter-momentum`, whose axes are both plain % values rather than a time axis) support free pan/zoom on both axes: drag pans, scroll/pinch zooms, double-click resets, no box-zoom gesture. See `.claude/rules/lis-dashboards.md`'s "Plotly setup" section for the full model, its two-round history (X-only + Y-autofit, then widened to full XY at direct user request), and how it was verified. **Since 2026-08**, `_bindYAutofit()`/`_toComparableX()` are no longer inline in this `report.html` — a `/*Y_AUTOFIT_JS*/` marker is filled in at generation time from `analytics/report_structure/y_autofit.js` (edit that file, not this one; `exchange_rate/` still carries its own inline copy of the same function, not yet migrated — see [`../report_structure/CLAUDE.md`](../../report_structure/CLAUDE.md)). `_bindYAutofit` supersedes the older `_bindYRescale` (the same name change happened in all three reports of the time, the third being `monetary_policy/`, deleted in 2026-08) and now only fires when X changes *without* Y also changing in the same event (i.e. the rangeselector preset buttons only — a direct drag or scroll already moves Y correctly on its own via Plotly's native handling, and autofitting on top of that would fight the user's own gesture). One visible behavior change from the old `_bindYRescale`: line/scatter charts now autofit tightly to actual visible min/max with no forced zero floor (the old function always floored at 0); stacked-bar charts (`chart-timeseries`) still anchor at 0 when the preset buttons trigger the autofit, since that's a real correctness requirement for a stacked bar's baseline, not a style choice.

## Data map

| Source | Content | Script | Refresh |
|---|---|---|---|
| MySQL `inflc_decomposicao` | IPCA/IPCA-15 by subitem_codigo: var_mensal/pesos/contribuicao. Since 2026-07, covers ago/1999→hoje (IPCA) / mai/2000→hoje (IPCA-15) — walks 4 IBGE agregados per índice (`VIGENCIAS` dict), one per estrutura de ponderação vintage, not just the current one (7060/7062). Subitem IDs resolved dynamically via `listar_classificacoes()` + code-length filter, not hardcoded | `domain/db/brasil/ibge/inflc_decomposicao.py` | `run()` (vigência atual, via `jobs/update_db.py`) / `backfill()` (histórico completo, manual) |
| MySQL `inflc_dim` | subitem_codigo → nome canônico + **two independent classification axes**: the BCB analytical one (grupo/subgrupo/item/subjacente/**comercializavel**, added 2026-08) and the **IBGE expenditure one** (`ibge_grupo`/`ibge_subgrupo`/`ibge_item`, added 2026-08 — parentage from the code prefix, names from SIDRA) + 7 núcleo membership flags (dimension table, no time axis — every subitem gets the *most recent* vigência's classification it appears in, see Gotchas) | `domain/db/brasil/ibge/inflc_dim.py` | `jobs/update_db.py` (idempotent — rebuilds from `Vetores_NT_57.xlsx` + a live IBGE naming lookup every run, no manual xlsx anymore) |
| MySQL `inflc_decomposicao_item` | IPCA/IPCA-15 by item_codigo (4-digit, one level coarser than `inflc_decomposicao`'s subitem/7-digit): var_mensal/pesos/contribuicao. Same `VIGENCIAS`/agregados as `inflc_decomposicao`, just `len(code) == 4` instead of `== 7`. Feeds only MA/MS/DP (see Gotchas for why these need item, not subitem, level) | `domain/db/brasil/ibge/inflc_decomposicao_item.py` | `run()` (não está em `jobs/update_db.py` ainda — rodar manual) / `backfill()` (histórico completo, manual) |
| `data/ipca_bcb_series.csv` | BCB/SGS aggregates (headline, components, núcleos) + STL `_ma3_sa` variants | `fetch_bcb.py` | manual only |
| `data/Vetores_NT_57.xlsx` | BCB's official aggregation vector (Nota Técnica nº 57), one sheet per classification vintage back to jan/1991 — sole source of grupo/subgrupo/item (durabilidade + serviços-subjacente facets)/subjacente/núcleo flags, all uniform 1999→hoje. Moved back here from `referencia/` in 2026-07 (it's an active script input, not context) | read by `inflc_dim.py` | replace file if BCB republishes the NT |

`inflc_agregados` documents its own 33 SGS series natively — `SHOW CREATE TABLE inflc_agregados` (or the Workbench column editor) lists every series+code without needing to open any Python.

`referencia/` holds context nothing reads: `Nucleos_inflacao.pdf` (the NT-57 itself), `inflacao_servico.pdf` (services-reweighting box, see Pending), and — added 2026-07 while researching the pre-2020 extension — `EE069_*`/`EE070_*` (BCB's own notes on the jan/2020 weighting update), `RI2005-12_*` ×2 / `RI2006-03_*` (BCB "boxe"s on the jan/2006 ad hoc reclassification and the jul/2006 POF update) / `RI2011-12_*` (BCB boxe on the jan/2012 POF update), and `TD2056_IPEA_*` (Martinez/Ipea 2015 — subitem compatibilization 1999-2014, BCB-sourced, used only as a validation reference, see Gotchas). No BCB or IBGE primary source was found for the oldest boundary (ago/1999) despite an extensive search — see Pending.

## Gotchas

- **IPCA and IPCA-15 use different IBGE variable IDs, but those IDs are stable across every vintage.** IPCA is always var_mensal=63/pesos=66 (agregados 655/656/2938/1419/7060, ago/1999→hoje); IPCA-15 is always var_mensal=355/pesos=357 (agregados 1646/1387/1705/7062, mai/2000→hoje). Requesting the wrong variable ID for the wrong aggregate does not 404 — IBGE returns HTTP 500 (their bug), which reads like an oversized-payload error rather than an invalid-ID one. Confirm via `ibge.metadados(agregado).variaveis` before adding a new vintage to `VIGENCIAS`.

- **Subitem-level detection must use code length, never `nivel`.** `nivel` for the subitem level is inconsistent across the agregados in `VIGENCIAS` — 4 in some, 3 in others, and **-1 for every single row** in agregado 1419 (jan/2012-dez/2019), an IBGE metadata quirk. The only reliable rule, used uniformly in `inflc_decomposicao.py`/`inflc_dim.py`: extract the leading numeric code via regex `^(\d+)\.` from `categoria_nome`, subitem ⟺ `len(code) == 7`.

- **ago/1999-jun/2006 (IPCA) is the one vintage where var_mensal and pesos live in separate IBGE aggregates** (655 and 656, respectively — no single aggregate has both for that window). No special-case code needed: `_fetch_vigencia()` always fetches each column independently and merges on `(date, subitem_codigo)`, which works identically whether the two columns come from the same aggregate or not.

- **`inflc_dim`'s subitem key is the 7-digit IBGE code alone, not "code + name" text.** Around half of subitems that persist across vintages have different name *text* over time (e.g. "Feijão - macassar" in 1999 → "Feijão - macaçar (fradinho)" today) — a text-based key would silently fragment their history into two disconnected series. `nome` (display name) is resolved separately, always to the most recent wording IBGE has ever used for that code (`_nomes_por_vigencia()` in `inflc_dim.py`, walking `VIGENCIAS["IPCA"]` newest→oldest). **Trade-off, not a bug:** since `inflc_dim` has no time axis and coalesces "most recent vintage wins" per code, a subitem whose *classification* (not just its name) genuinely changed over time — e.g. the documented jan/2006 swap where ethanol left "administered" and medicines entered it (`referencia/RI2005-12_boxe_Alteracao_composicao_administrados_monitorados_jan2006.pdf`) — gets labeled by its **current** Grupo/Subgrupo for its **entire** history, including months when it was, at the time, actually classified the other way. A rarer, sharper version of the same trade-off: IBGE occasionally reuses a 7-digit code for a genuinely different product after full discontinuation (found while validating against IPEA — code `5101022` meant "Barco" through 2011, then "Transporte hidroviário" from 2012 on, no longer in the current structure at all) — the code-based join treats these as one continuous series regardless.

- **`inflc_dim`'s Grupo/Subgrupo/Item classification is a single source now, uniform 1999→hoje: `Vetores_NT_57.xlsx` alone**, plus one small hardcoded lookup in `inflc_dim.py` for the one facet that file doesn't cover (Alimentos processing-stage: in natura/semi-elaborado/industrializado — sourced from `referencia/EE069_*.pdf`, Tabela 5, defined by 4-digit IBGE Item name with one hardcoded subitem exception, code `1111004` "Leite longa vida"). The old `tabela_dimensao_ipca.xlsx` (manual grupo/subgrupo/item, only ever covered the 2012 and 2020 vintages) is fully superseded and gone — do not restore it. Found and fixed while validating against production data: the Item name in `Vetores_NT_57.xlsx` is "**Leites** e derivados" (plural — different from EE069's prose, same BCB spelling-inconsistency pattern as Administrados/Monitorados), and item `1110` "Aves e ovos" has no blanket rule in EE069 at all — only 3 of its subitens are individually named (`_ALIMENTOS_EXCECAO_SUBITEM`). **5 subitens still resolve `item=None`** as a result, all discontinued before 2020 with no source anywhere: Peito/Coxa/Asa de frango (the rest of "Aves e ovos", never named by EE069) and "Refeição pronta"/"Lanche para viagem" (item `1117`, which doesn't exist in the current 2020+ structure at all). Not a bug — just where the documentation runs out. **"Alimentos Subjacente" is the one label that has no source anywhere** (unlike Serviços/Bens Industriais Subjacente, which come from the official `EX3 Serviços`/`EX3 Industriais` NT-57 flags) — it was only ~34 hand-picked subitems in that now-deleted file. This label is simply unavailable; there is no fallback.

- **BCB/SGS aggregates live in two places that are NOT kept in sync automatically.** `data/ipca_bcb_series.csv` (`fetch_bcb.py`, uppercase names like `IPCA_nucleo_P55`) duplicates most of `macro_brasil.inflc_agregados` (lowercase, `ipca_nucleo_p55`). `fetch_bcb.py` carries one series with no DB counterpart (`IPCA_12m`, SGS 13522, used for the "12 Meses" KPI cross-check below). No migration is scheduled — adding a series to one does not update the other.

- **The IPCA-15 headline was the one series on the núcleo charts that lagged the release by a day — fixed 2026-08-26, found by a user report.** Every other IPCA-15 series on "Componentes/Núcleos — 3M SAAR" and the heatmap is computed in-house from `inflc_decomposicao`, so it lands the morning IBGE publishes; `IPCA15` itself came only from `data/ipca_bcb_series.csv` (SGS 7478), and **SGS mirrors the IBGE release with about a day of lag**. On release day that left `IPCA15_ma3_sa` one month short of the núcleos drawn beside it, with two visible symptoms and one silent: the dotted "IPCA-15 (ref.)"/"(total)" line stopped a month early, and — worse, because nothing about it looked wrong — **the entire heatmap lost its newest column for every row**, since its 12 columns are `compute3mSAAR('IPCA15').dates.slice(-12)`. `generate_report.py::_splice_headline_15()` now feeds `IPCA15` into `series15` as SGS-where-it-exists + `_compute_headline()` reconstruction for the not-yet-mirrored tail, so published history stays byte-identical to the official print (verified: 0 difference across all 315 SGS months) and only the newest month carries IBGE's subitem rounding (0.006 p.p. mean / 0.067 p.p. worst case over those 315 months, under 0.005 p.p. in the last 18 — below the 1-2 decimals anything displays), replaced by the official value on the next `fetch_bcb.py` run. Side effect: the "12 Meses" KPI for IPCA-15 now resolves at tier 2 of the fallback below instead of falling through to the tier-3 subitem reconstruction.

- **The tree's root reproduces the published headline only to IBGE's own publication precision, and that is measured, not assumed.** The table's root row is `sum(contribuicao)/sum(pesos)` over the subitens, while `D.bcb.IPCA` is BCB's mirror of IBGE's printed monthly rate. Measured 2026-08 across the full history: **IPCA mean 0.0070 p.p. over 319 months, worst 0.0719 in mai/2000; IPCA-15 mean 0.0059 over 316 months, worst 0.0674, also mai/2000** — and under 0.006 p.p. for both since 2021. That reproduces, from an independent measurement, exactly the figures `_splice_headline_15()` already recorded in `generate_report.py`. The error concentrates in 1999-2003 because monthly inflation was larger then: IBGE rounds **each subitem** to 2 decimals before we recombine ~380 of them, so the rounding is absolute while the rate is not. There is no more precise published input to fix it with. `tests/test_inflation_js.js` asserts three separate bounds (mean, worst-since-2021, worst-ever) rather than one loose ceiling, so a real regression cannot hide under the historical tail.

- **`fetch_bcb.py` has no scheduled run** — it is not in `jobs/update_db.py`. It has gone silently stale for a full month before with no visible error.

- **Núcleos por exclusão for IPCA-15 are computed in-house, not published by BCB.** BCB only publishes núcleo series (EX-0/EX-01/…/P55/MA/MS/DP) for the full IPCA; `inflc_agregados`/`fetch_bcb.py` only carry the IPCA-15 headline (SGS 7478). Since 2026-07, `generate_report.py::_compute_ipca15_nucleos()` derives EX-0/EX-01/EX-02/EX-03/EX-03-Serviços/EX-03-Industriais/EX-FE for IPCA-15 directly from `inflc_decomposicao` + `inflc_dim`'s official `nucleo_*` membership flags (same NT-57 vector already used for Difusão-by-núcleo) — weighted average of `contribuicao`/`pesos` among flagged subitems each month, then run through the same STL+MA3 pipeline as BCB series (`fetch_bcb._apply_stl_ma3`, now generalized to accept an explicit `series` set instead of only its own module-level `_SAAR_SERIES`) so the front-end's existing `compute3mSAAR`/`computeYoY` work unmodified — the computed series are merged into `data["bcb"]` under names like `IPCA15_nucleo_EX0` (see `NUCLEO_ALL_15` in `report.html`). **P55, Médias Aparadas (MA/MS), and Dupla Ponderação remain out of reach this way** — they need the full statistical methodology (percentile, tail-trimming, volatility weighting), not just a fixed exclusion filter; see Pending.

- **"12 Meses" KPI uses a 3-tier fallback**, in `report.html` JS: official BCB series (`IPCA_12m`/SGS 13522, IPCA only) → chaining the official monthly series (`computeYoY`, covers IPCA-15 too) → reconstruction from subitem data (`computeIpca`, last resort only). "IPCA Acumulado" reuses the same value when the selected window is exactly the last 12 months, so the two KPIs never disagree on the same window.

- **No 12-month variation stored in `inflc_decomposicao`** — deliberate: compute YoY/accumulated from `var_mensal` at the consumption layer instead of keeping a second source of truth in the DB.

- **STL ordering is deliberate**: `_apply_stl_ma3()` (`fetch_bcb.py`) seasonally adjusts the raw monthly series first, then takes MA(3) — not the reverse — matching BLS/X-13 convention. STL (not X-13ARIMA-SEATS) is used on purpose: X-13 needs a separate Census Bureau binary per machine, which would break `uv sync` reproducibility.

- **`pesos`/`contribuicao` round looser than `var_mensal`** in `_to_records()` (8 decimals vs. 5) — rounding low-weight subitems (~3e-6, e.g. "Fisioterapeuta") to 5 decimals zeroes them out, and the front-end's weighted-average chart divides by that weight, so it renders empty for those subitems.

- **"Média 5 Núcleos (BCB)" is a specific subset, not all núcleos**: EX-0, EX-03, Médias Aparadas (smoothed), Dupla Ponderação and P55 only — deliberately excludes EX-01/EX-02/EX-FE, mirroring how BCB itself summarizes núcleos (Estudo Especial 102).

- **Two real bugs found in the group/subgrupo/núcleo-15 weighted-average logic, both only caught by executing against real data (not by reading the code):**
  1. **100x scaling bug** (found 2026-07): `computeMonthlyFromRecords()` (`report.html`) and `_compute_ipca15_nucleos()` (`generate_report.py`) both did `sum(contribuicao)/sum(pesos) * 100` — wrong, because `contribuicao`/`var_mensal` are already on a "percent number" scale (e.g. `-1.49` means `-1.49%`) and `pesos` sums to ~1.0 across the full index, so the ratio already lands on that same scale; the extra `*100` made every group/núcleo-15 monthly value 100x too large. Fixed by dropping the `*100`.
  2. **Rounding-before-chaining bug** (found 2026-07, while double-checking subgroup 12m figures against an external BCB reference table): `computeYoYFromRecords()` (`report.html`) and the JS `computeYoY()` applied to Python-computed núcleo-15 series both compounded 12 *already-2-decimal-rounded* monthly values — correct for direct monthly display, but rounding intermediate months before chaining compounds that rounding into the final 12m figure. Monthly values already matched the reference exactly before this fix; 12m values were off by up to 0.02pp for Administrados/Livres/Industriais/Serviços. Fixed by adding `computeMonthlyRatioFromRecords()` (unrounded) as the shared basis — `computeMonthlyFromRecords()` rounds only for display, `computeYoYFromRecords()` chains the unrounded ratio and rounds only the final 12m result — and by removing the `.round(2)` on `_compute_ipca15_nucleos()`'s monthly value in Python (it now flows unrounded into both `compute3mSAAR` and, via `D.bcb`, the JS `computeYoY()` chain). Re-verified against the same reference table: 24/25 checked (group × month) 12m values now match exactly. **One residual, unexplained 0.01pp difference remains** (subgrupo=Alimentos, 12m ending 2026-03: we get 0.34, reference shows 0.35) — traced to the underlying unrounded product itself (0.342...), not a rounding-boundary artifact, so likely a source-data vintage difference between our live IBGE pull and whenever the reference table was generated, not a bug in this logic. Not investigated further.

- **Two report.html sections were hardcoded to full IPCA and silently ignored the IPCA-15 toggle — found 2026-07 by a user report, not by reading the code.**
  1. **"Componentes — 3M SAAR" showed full-IPCA data on the IPCA-15 tab.** `renderCompSAAR()`'s `COMP` array only ever listed `IPCA`/`IPCA_livres`/etc. On the IPCA-15 tab, `renderNucleosTab()` swapped this slot for a *different kind* of chart entirely (`renderCompContrib15()`, a monthly-contribution bar chart, last 18 months, 4 categories) under a different title — properly gated, but not an equivalent view, so there was never a 3M-SAAR-by-component trend chart for IPCA-15 at all. Fixed by making `renderCompSAAR()` itself branch on `currentIndex` (a `COMP15` array using the new `IPCA15_livres`/`_administrado`/`_alimentacao`/`_servicos`/`_industriais` series from `_compute_ipca15_grupos()`) and calling it unconditionally from `renderNucleosTab()`; `renderCompContrib15()` was deleted (superseded, and largely redundant with the Decomposição tab's own drilldown anyway).
  2. **"Mapa de Calor" never changed at all, for either tab or the toggle.** `renderHeatmap()`/`HEATMAP_ROWS`/`computeHeatmapRow()` were 100% hardcoded to full-IPCA series names, and the IPCA/IPCA-15 toggle handler had no `if (tabRendered.heatmap) renderHeatmap();` call (unlike the Núcleos tab, which did) — so even if the heatmap *had* been index-aware, switching indices while already on that tab wouldn't have re-rendered it. Fixed both: added `HEATMAP_ROWS_15` (mirrors `HEATMAP_ROWS`, no Comercializáveis/Não Comercializáveis row, same reason as `renderCompSAAR`'s IPCA-15 branch) and made `renderHeatmap()` pick between the two + the matching headline series based on `currentIndex`; added the missing re-render call.
  3. Neither fix needed new data for the Núcleos rows (already had `IPCA15_nucleo_*_ma3_sa` from earlier work), but did surface a separate pre-existing gap: `IPCA15`'s own headline had no `_ma3_sa` variant at all, so its "(Total)" row/line was empty in both new views. Root cause: `fetch_bcb.py` already lists `"IPCA15"` in `_SAAR_SERIES` in code, but `data/ipca_bcb_series.csv` on disk predated that addition (it had been restored from an old backup earlier in this same work). Fixed by rerunning `fetch_bcb.py` — not a code bug, a stale generated file.

- **MA/MS/DP's missing NT-57 proxy tables turned out to be immaterial in practice — measured, not assumed.** NT-57 defines explicit proxies (Tabelas 2-4 for DP, 6-8 for MS) to bridge the 11/48-month rolling window across a structural transition when an item's own definition changed at the boundary (e.g. "8104.Cursos diversos" vs. "curso técnico" shuffling into/out of it in jan/2020). `inflc_decomposicao_item.py`/`generate_report.py::_compute_ms`/`_compute_dp` don't implement these — they concatenate each item code's history across vigências plainly, the same trade-off already accepted for subitem-level retroactive relabeling in `inflc_dim.py`. Validating `_compute_ma`/`_compute_ms`/`_compute_dp` against BCB's official full-IPCA series across the *entire* backfilled history (not just one vintage) measured the actual cost of skipping this: MA and MS never exceed ~0.006pp anywhere (proxies don't matter for them in practice); DP's worst gap is 0.019pp, and it's not scattered — it clusters tightly around 2007-2010, exactly where a 48-month DP window would span the ago/2006→jul/2006 transition that Tabela 3's proxy addresses. Still under 0.02pp even there. Implementing the proxies would need per-item formulas mixing subitem- and item-level codes with explicit (+)/(-) signs (see the actual tables in `referencia/Nucleos_inflacao.pdf` §2.2/§2.4) — judged not worth it for a <0.02pp, single-window effect.

## `comercializavel` — subitem-level Comercializáveis/Não Comercializáveis (added 2026-08)

`inflc_dim`/`report.html`'s "Filtro BCB" dropdown (shared by the ranking table and the Y/Y drilldown, `_YOY_BCB_FILTERS`) previously only exposed BCB's Grupo/Subgrupo/Subjacente axis (Livres-Monitorados, Alimentos/Bens Industriais/Serviços × Subjacente). `IPCA_comercializaveis`/`IPCA_nao_comercializaveis` (BCB/SGS, `fetch_bcb.py`) already existed as aggregate index-level series, but there was no subitem-level breakdown to filter/drill by — until it was noticed that `Vetores_NT_57.xlsx` (already the sole source for grupo/subgrupo/item/subjacente/núcleo) also carries `Comercializáveis`/`Não comercializáveis` flag columns, uniform across all 5 vigência sheets 1999→hoje, same rollup mechanism (`_rollup()`) already used for every other facet. Added as `inflc_dim.comercializavel` (`"Comercializável"`/`"Não Comercializável"`/`NULL`, ~44/614 subitens null — same kind of gap as the 5 `item=None` subitens, not investigated further) via `ALTER TABLE` (existing table, not a fresh `CREATE TABLE`) + a new `optgroup` in both `report.html` dropdowns. Independent of Grupo/Subgrupo — a subitem's Comercializável/Não status doesn't imply which Grupo/Subgrupo it's in, or vice versa.

## Pending

### High priority

- Migrate `fetch_bcb.py` to read from `macro_brasil.inflc_agregados` instead of re-fetching BCB/SGS directly — would also fix the uppercase/lowercase naming mismatch.

- Add `fetch_bcb.py` to `jobs/update_db.py` (or equivalent) so the CSV cannot silently go stale again.

- ~~Núcleos for IPCA-15~~ — EX-0/EX-01/EX-02/EX-03/EX-03-Serviços/EX-03-Industriais/EX-FE done 2026-07, see Gotchas. ~~P55/Difusão for IPCA-15~~ — also done 2026-07 (`generate_report.py::_compute_p55`/`_compute_difusao`), both operate at subitem level like the exclusion núcleos so needed no new data; both validated against BCB's official full-IPCA series before being trusted for IPCA-15 (P55 exact match on all 318 months checked, Difusão within 0.005pp — BCB's own display rounding, not a methodology gap). ~~MA/MS/DP for IPCA-15~~ — done 2026-07. These three operate at the **item** level (4-digit IBGE code, e.g. `1101.Cereais, leguminosas e oleaginosas`), not subitem (7-digit) — confirmed independently from IBGE's own live SIDRA metadata (classification `315`'s own name is "Geral, grupo, subgrupo, item e subitem"; `nivel=3` rows are items, `nivel=4` rows are subitens), not just NT-57's terminology — so a new table, `inflc_decomposicao_item` (`domain/db/brasil/ibge/inflc_decomposicao_item.py`, same `VIGENCIAS`/agregados as `inflc_decomposicao`, just `len(code)==4`), was backfilled across all vintages for both indices. `generate_report.py::_compute_ma`/`_compute_ms`/`_compute_dp` validated against BCB's official full-IPCA series **across the entire backfilled history** (not just the current vintage): MA exact to within 0.005pp on 318/318 months; MS within 0.0056pp on 301/318 (rest excluded, no 12m window yet); DP within 0.019pp on 275/318 (rest excluded, no 48m window yet) — see Gotchas for where that DP gap comes from. DP diffs each item against **IPCA-15's own headline**, not full IPCA's, for the in-house version — NT-57's formula (written only for full IPCA, which is what was validated above) diffs against "a do IPCA cheio," but there's no official IPCA-15 DP to be consistent with, so this stays internally consistent instead.

- **Inércia — replace the hover's `1/√n` with a real standard error.** It assumes i.i.d. observations
  and the y/y windows overlap 11 of 12 months, so the printed "±0,10" is 2-3× too small; a block
  bootstrap (blocks of 12) gives 0,16-0,28 depending on the subitem, and `diagnostico()`'s shuffled
  distribution independently says 0,24. Compute it per subitem in `inercia.py`, send it in the payload
  next to `r` and `n_pares`, and the tab's note plus this file's "~0,10" mentions all need updating
  with it. Everything the tab says about instability gets *stronger*, not weaker.

- **Inércia — the lag-1 measure is deferred, not cancelled** (user, 2026-08: "Depois decido o outro").
  If it comes back it must come back with the mechanical floor subtracted per subitem — consecutive
  y/y windows share 11 months, so the raw statistic is ~97% construction (0,921 real against 0,895
  shuffled). `diagnostico()` already computes the benchmark that needs.

- Heat map by monthly variation (not 3M SAAR) with a selectable level (Grupo/Subgrupo/Item/Subitem) — today's "Mapa de Calor" tab only covers a fixed set of Grupo/núcleo rows.

- ~~Extend `inflc_decomposicao`/`inflc_dim` before 2020~~ — done 2026-07, back to ago/1999 (IPCA) / mai/2000 (IPCA-15). Validated against Ipea's independent compatibilization (`referencia/TD2056_IPEA_*`): 92% of subitems match within 0.01pp; residual differences are either genuine code-reuse-for-a-different-product cases (see Gotchas) or explained by Ipea's series being computed via formulas rather than republishing IBGE's official print. **Still open**: jan/1991-jul/1999 (IPCA only, IPCA-15 didn't exist yet). **Correction (2026-07):** a prior version of this note claimed no BCB/IBGE primary source existed for this boundary — false. `referencia/Nucleos_inflacao.pdf` (Nota Técnica do BCB nº 57, dez/2025, already in this repo) extends every BCB analytical series back to jan/1991 and documents the transition in full; `data/Vetores_NT_57.xlsx` (the file we already use for Grupo/Subgrupo/Item classification) even has a `jan91-jul99` sheet, sitting unused — `inflc_dim.py`'s `_VETOR_SHEETS` explicitly excludes it. The gap is real but narrower than previously stated: it's about IBGE SIDRA subitem-level *decomposição* data (var_mensal/pesos, classificação id 72 instead of 315, not yet confirmed fetchable that far back), not about classification/methodology. Left out of scope by explicit decision, not by information gap — ago/1999 remains the boundary for now.

- Subitem-level decomposition *within* a núcleo (not just within the full IPCA) — `nucleo_*` flags already give membership; needs weight renormalization + núcleo-specific contribution logic.

- Aggregates computed directly from the IBGE decomposition, not just BCB/SGS — would allow decomposing núcleos/aggregates that BCB itself does not publish a breakdown for.

### Medium priority

- Report is ~99 MB (see "Generate the report" above); consider paginating or compressing the inline JSON if email delivery becomes a problem.

- 12-month contribution view per subitem — deferred; if needed, compute by chaining `var_mensal` in `generate_report.py` rather than reintroducing a `var_12m` column in the DB.

- Services-inflation reweighting by production factor (`referencia/inflacao_servico.pdf`, BCB RI jun/2024 box) — not started; needs TRU/IBGE factor weights mapped to IPCA subitems.
