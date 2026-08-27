# analytics/brasil/labor_market/ — Panorama de Mercado de Trabalho

Self-contained HTML report (`reports/brasil/Labor Market.html`). Same `/*REPORT_DATA*/`
marker-substitution pattern as the other reports in `analytics/` — no Jinja2, no build step — built
directly on [`analytics/report_structure/`](../../report_structure/CLAUDE.md) from day one (both markers),
same as `fiscal_policy/`/`economic_activity/`.

## Generate

```powershell
uv run python -c "from analytics.brasil.labor_market.generate_report import run; run()"
# Output: reports/brasil/Labor Market.html
```

`mt_pnad`/`mt_pnad_trimestral` are not yet in `jobs/update_db.py` (see root `CLAUDE.md`'s
"Jobs de rotina incompletos") — run `domain/db/brasil/ibge/mt_pnad.py`/`mt_pnad_trimestral.py`
manually first if the data looks stale. The CAGED tables (`mt_caged_setor`/`_uf`/`_salario` via
`mt_caged_novo`, and `mt_caged`) **are** in the routine job.

## Scope — pure visualization, no derived metric

Built at explicit user request to skip any derived metric ("For now, I don't want to create metrics
like Okun, just visualize the data"). No STL/dessazonalização, deflação or %PIB anywhere in this
report — see [`transforms.py`](transforms.py) for everything it needs: `variants_pnad_mensal`/
`variants_pnad_trimestral` for PNAD (just `pct_change`/`pp_diff` reused from
`analytics.brasil.fiscal_policy.transforms`, plus `to_quarterly`) and `variants_caged_*` for CAGED
(rolling/YTD sums).

IBGE (PNAD) came first, in 2026-08; CAGED/MTE was added later the same month — see "Emprego Formal"
below.

## PNAD tabs — 3 tabs, 12 tables

Restructured (2026-08, same day as the initial build) from a single "Indicadores" tab with one
monolithic tree into **3 topic tabs × 4 independent tables each**, at explicit user request ("let's
break the tables"). Every table is its own hierarchical table+chart pair — own selects, own checkbox/expand
state, own Plotly chart, own range buttons — built by the same
`makeSimpleHierTab()` factory instantiated 12 times (`report.html`'s `buildTableBlock()` creates the
DOM for one table and wires it up; `renderPnadTab(tabKey, containerId)` does this for all 4 tables of a
tab, lazily on first tab activation, same lazy-render-per-tab pattern as before).

`pnad_tab.py`'s `TABS` list replaces the old flat `TREE`: `[{key, label, tables: [{key, label, tree,
default_checked}, ...]}, ...]` — 3 tabs, 4 tables each, every table with its own independent `tree` (a
list of root nodes, no longer wrapped in a single shared tree). All 12 tables still resolve `seriesKey`
against the **same flat `series` dict** (`D.pnad.series`, unchanged) — splitting the tree only changed
how rows are grouped for display, not how data is stored or computed.

**1. Taxas** — 4 tables: Taxa de Desocupação, Taxa de Participação na Força de Trabalho, Taxa de
Informalidade (each a single indicator node — "Total" root + Sexo/Idade/Instrução/Cor ou Raça children
from `mt_pnad_trimestral`), and Subutilização da Força de Trabalho (3 merged rate indicators by
Sexo/Idade + 5 unmerged mt_pnad-only leaves).

**2. Ocupação** — 4 tables: Ocupação e Desocupação (Níveis) (nivel_ocupacao/nivel_desocupacao merged +
`ocupado`/`desocupado`/`fora_da_forca_trabalho` mt_pnad-only leaves), Ocupação por Posição na Ocupação
(12 flat leaves, mt_pnad-only), Ocupação por Atividade (10 flat leaves, mt_pnad-only), and Informalidade
e Previdência (2 unrelated flat leaves — `ocup_informal` and `pct_contribuintes_previdencia` — grouped
together only because both are one-off mt_pnad series with no natural home elsewhere).

**3. Rendimento** — 4 tables: Rendimento Médio (5 flat leaves: habitual/efetivo × real/nominal × todos
os trabalhos/trabalho principal), Rendimento por Posição na Ocupação (11 flat leaves), Rendimento por
Atividade (10 flat leaves), Massa de Rendimento (4 flat leaves) — all mt_pnad-only, no
`mt_pnad_trimestral` counterpart in this round (see Pending).

## Emprego Formal (CAGED/MTE) — 1 tab, 5 tables

Added 2026-08 after an explicit evaluation of "how does MTE/CAGED fit the current dashboard — new tab
or increment the existing ones?". **Answer was a separate tab**, and the reasoning is the load-bearing
part of this section: CAGED and PNAD measure different universes and can't share a chart. PNAD is a
household survey (~103M employed, includes informal, reported as level/rate); CAGED is an
administrative register of formal CLT employment (~48M stock) and what it publishes is a **flow**
(hires, separations, net balance, in people/month). These tables plot every checked row on one axis,
so mixing `ocupado` (mil pessoas) with `saldo` (pessoas/mês) would misread by construction. Window
(2020-01 vs. 2012-03) and CAGED's retroactive revision reinforce the split. See `caged_tab.py`'s
docstring and the report's own Apêndice.

`caged_tab.py` exports a flat `TABLES` list (not `TABS` — the tab is single), same
`{key, label, tree, default_checked}` contract as `pnad_tab.py` plus two new fields, `controls` and
`default_expanded`.

| Table | Source | Tree |
|---|---|---|
| Nacional | sum of any cut | 3 leaves: Saldo / Admissões / Desligamentos (metric is a *row*, so only the Período control) |
| Por Setor | `mt_caged_setor` | Total Brasil → 22 CNAE 2.0 sections |
| Por UF | `mt_caged_uf` | Total Brasil → 5 IBGE regions → UFs, plus `NI` as a loose leaf (belongs to no region) |
| Por Faixa Salarial | `mt_caged_salario` | Total Brasil → 10 SM-multiple bands + não identificado |
| Estoque | `mt_caged` (BCB) | 3-level BCB taxonomy: Total → sectors, with SIUP and Serviços as intermediate aggregates |

**No header-only rows here** — unlike the PNAD tabs. Every group node has a real value: the CAGED ones
because summing movement counts across categories is valid (they're partitions of one universe, never
ratios), the estoque ones because the BCB publishes an SGS code for each aggregate.

**Controls: why no percent change.** Saldo is a net flow that crosses zero — verified live: all 22 CNAE
sections cross, and the national saldo's YoY% reaches **696%**. Percent change on a sign-flipping series
is numerical noise, not a poor reading. The four flow tables use **Mensal / Acum. 12m / Acum. no ano**
(how the MTE itself publishes) instead. Estoque never crosses zero, so it keeps **Nível / Var. Mensal
(pessoas) / Var. Anual (%)** — and its Var. Mensal *is* the saldo reading of that series.

**Two sector taxonomies that don't reconcile** — deliberately in separate tables: the microdata's 22
CNAE 2.0 sections vs. the BCB's own 3-level tree (SIUP, Serviços as intermediate aggregates, no 1:1
mapping; Serviços is only partially decomposed since not every subsector has its own SGS code).

## Apêndice

5 accordion notes: sources/scope (all 6 tables), CAGED × PNAD non-comparability, CAGED revision +
why-no-percent + salary bands + the two taxonomies, **"Como ler as tabelas"** (the two controls, the
measured monthly-to-quarterly alignment, points-vs-percent, the unit convention and the two corrected
denominators — this is where the removed on-page note went), and header-only rows (noting the CAGED
tab has none).

Merging mensal × trimestral is still safe for the same reason as before: `mt_pnad`'s own `_SIMPLES` and
`mt_pnad_trimestral`'s `_VARS_CONDICAO_TAXAS`/`_VARS_SUBUTIL_TAXAS` name 8 headline vars **identically**
(confirmed by reading both scripts, not inferred) — cut by Sexo/Idade/Instrução/Cor ou Raça (5 condicao
vars) or Sexo/Idade only (3 subutil vars) — 111 series, curado from ~340 available (user chose "Curado"
over "Completo"). Rendimento/massa/população/horas by posição/atividade/ocupação (another ~230 series in
`mt_pnad_trimestral`) are **not** in this round — see Pending.

**Two controls per PNAD table** (2026-08-27), Frequência × Métrica — the variant key is the two values
joined, `mensal__yoy`. Deliberately no Nominal/Real/%PIB/Esfera axes like `fiscal_policy`'s
`makeHierTab()`; this report has none of those concepts.

**Frequência: Mensal | Trimestral.** Added at user request ("como temos dados mensais e trimestrais,
separe a visualização — quando clico mensal vejo somente a taxa de desemprego mensal, quando clico
trimestral vejo todas as linhas disponíveis, sem os meses com travessão"). Mensal shows only `mt_pnad`
rows; Trimestral shows everything on a quarterly axis, with the `mt_pnad` rows resampled by
`to_quarterly()`. The filter is **by absence of data, not by a flag on the tree**: a
`mt_pnad_trimestral` series only carries `trimestral__*` keys, so `seriesFor()` comes back empty in the
Mensal view and `visibleDeep()` drops the whole row (and its dimension-group parent). No node declares
which frequency it lives in, and no row ever renders as a line of em-dashes.

**The two surveys date their periods differently, and the alignment was measured, not assumed**:
`mt_pnad_trimestral` dates a quarter by its **first** month (2026-04 = Q2), `mt_pnad` dates a moving
quarter by its **last**, so closed Q2 (Apr-Jun) sits in `mt_pnad` under 2026-06. Reconstructing the
national unemployment rate from `mt_pnad_trimestral`'s own sex breakdown (weighting população ×
participation rate) and comparing against `mt_pnad`: **MAE 0.038 p.p. over 57 quarters** (max 0.097)
against the last month — the source's own 1-decimal rounding — versus 0.499 p.p. (max 1.426) against
the first, 13× worse. Hence `to_quarterly()` harvests months 3/6/9/12 and **re-dates to the quarter's
first month**. That is also what lets the Trimestral view show a "Total" row at all: `mt_pnad_trimestral`
excludes every "Total" category by design, since it is covered nationally by `mt_pnad`.

**Métrica: Nível | year-over-year**, with the a/a label varying by table because the unit does —
**Diff Y/Y** on all-rate tables, **Var. % Y/Y** on level/R$ tables, **Var. Y/Y** on mixed ones (where
`ymode: "diff"` makes the JS resolve p.p.-vs-% per row). Lag 12 in the monthly view, lag 4 in the
quarterly.

**Var. Curto Prazo (m/m, t/t) was removed** 2026-08-27 at explicit user request ("pode retirar a
métrica de curto prazo de todos os gráficos") — the `mom`/`qoq` variants are gone from the payload too,
not just hidden from the dropdown.

**Indicator roots start expanded** (`default_expanded`, set in a loop over `TABS`) so the Trimestral
view reveals which cuts exist without a click. One level only — opening the dimension groups too would
put all 18 desocupação categories on screen at once. Costs nothing in the Mensal view, where those
children do not exist and the node does not even render a ▸.

## Units — the axis says what the series measures

At user request (2026-08-27): "a taxa de desocupação mede o que? O percentual de desempregados vis a
vis a força de trabalho — coloque algo como (desocupados/força de trabalho, %) ... não é para escrever
um livro no gráfico". Each leaf carries `unit` (short, for the table) and `def` (the definition, for the
Y axis), set by `pnad_tab.py`'s `_leaf()` from the `_UNITS` map. The axis title is composed at render
time from the selected metric **plus the plotted series** — so a year-over-year view reads "p.p. contra
o mesmo período do ano anterior", never the level's unit. That was the reported bug: `"Pessoas Ocupadas
(mil pessoas)"` had the unit baked into the **label**, and a label shows in the legend under every
metric.

## Every chart carries its own header

User request (2026-08-27): "se eu enviar o gráfico para alguém, a pessoa não fará a mínima ideia do que
se passa, terá que ler os eixos". So each of the 17 chart cards opens with a three-line header — title,
subtitle, source and period — built by `renderChartHead()` and **recomputed on every render**, since a
static caption would go stale the moment someone flips a selector. It sits inside the chart card, above
the plot, because that is the region a screenshot captures: the card's `h2` is separated from the chart
by the control bar and the whole table.

```
Taxa de Desocupação — Brasil
Mensal (trimestre móvel) · desocupados / força de trabalho, %
Fonte: IBGE, PNAD Contínua · mar/2012 a jul/2026
```

Only `chart_title`/`chart_source` are declared per table; everything else is derived — the checked
series, the selected controls, the Y-axis unit, and the real extent of the plotted data (so the a/a view
correctly reports starting a year later, and the quarterly view prints `1T12 a 2T26`).

**The interesting part is what the subtitle leaves out.** The same fact reaches it by three routes —
the control's option label, the series name, and the axis title — and the first draft printed all three
("Taxa de Desocupação · Mensal · Taxa · desocupados / força de trabalho, %"). Two rules fix it: an
option contributes its label only when it has neither `ymode: "unit"` (the level view, where "Taxa"
adds nothing the unit doesn't say) nor `ypart` (CAGED, where the label is already inside the axis
title); and any remaining fragment already contained in the axis title is dropped. The series name is
also dropped when it is just the chart title again.

## Short row labels + a definition card

User request (2026-08-27): "algumas linhas poderiam ter um nome mais simples com um card descritivo
quando passa o mouse por cima ... assim não precisa escrever tudo na linha e deixar a tabela
deformada". So a row's `label` is the **short display name**, and two optional fields carry the rest:
`full` (the source's official variable name) and `desc` (a short explanation of the concept). A row
that has either gets a small `i` button after its label; hovering opens a card, clicking pins it,
clicking away or Esc closes.

**52 of the rows have one** — 37 PNAD, 15 CAGED — declared in an `_INFO` dict per module
(`seriesKey -> (official name, explanation)`). Rows whose label already says everything get no button;
the affordance is meant to be sparse. The PNAD official names come from the IBGE metadata API
(aggregates 6379-6441, 8513, 3919, 6318, 6438, 6320/6323, 6389/6391, 6390/6392), not from memory.

Implementation notes worth keeping: `full` is only attached when it actually differs from the
displayed label, so the card never repeats the row; there is **one** `.info-pop` in the document,
repositioned on open, rather than one per row; and the card's last line reuses the node's `def`, so
the unit definition and the axis title can't drift apart. The short label is also what the chart
legend uses — which was half the point, since names like "Taxa Combinada (Desocupação + Subocupação
por Insuficiência de Horas)" ate the legend as well as the column.

Labels shortened in this round: the three subutilização combined rates, subocupação, desalentados,
the 12 posição-na-ocupação rows ("Setor privado (exceto doméstico), com carteira" → "Privado, com
carteira"), the two long PNAD activity sections, five CAGED CNAE sections, and SIUP.

## Units

The short unit appears beside a row's label only when it disambiguates — a table with two or more
distinct units, in the Nível view. An all-percent table does not repeat "%" on every row.

**The denominators were reconstructed from `mt_pnad`'s own level series and checked**, not copied from
IBGE documentation — all 10 rates close with MAE ~0.025 p.p. (the source's 1-decimal rounding). Two came
out different from the obvious guess: `taxa_subocupacao_horas` divides by **ocupados** (MAE 0.024) and
not by força de trabalho (0.604) or força ampliada (0.949); and `nivel_ocupacao`/`nivel_desocupacao`
divide by **população 14+**, which is why `nivel_desocupacao` ≠ `taxa_desocupacao`. Re-verify the same
way before adding a rate.

**Points vs. percent** — `pnad_tab.py`'s `_RATE_VARS` (the same 11 names as `mt_pnad.py`'s `_SIMPLES`)
marks which series are already percentages. Their Curto/Anual variants are **point differences**
(`pp_diff`, e.g. "taxa foi de 7,5% para 7,0%" → "−0,5 p.p.", never "−6,7%"). Everything else (levels in
mil pessoas or R$) uses normal **percent change** (`pct_change`). The payload carries this as a flat
`rate_keys` list (`D.pnad.rate_keys` in `report.html`) so the JS never has to re-derive it — global to
the whole report, unaffected by which table a series appears in.

**Header-only rows** — group/dimension headers (e.g. the "Sexo" node under an indicator) have a
`seriesKey` that deliberately doesn't exist in `series` — expandable, but checking them plots nothing,
same convention `analytics/brasil/credit/CLAUDE.md` already documents for its own no-native-total cuts. 26 such
nodes across the 12 tables (5 indicators × 4 dims + 3 indicators × 2 dims) — live-verified, see Gotchas.

## Data map

| Tab | Tables | Tables read |
|---|---|---|
| Taxas | Desocupação, Participação, Informalidade, Subutilização | `mt_pnad` (8 series), `mt_pnad_trimestral` (curado, dims of the same 8) |
| Ocupação | Níveis, Posição, Atividade, Informalidade e Previdência | `mt_pnad` only, except Níveis' 2 merged indicators |
| Rendimento | Médio, Posição, Atividade, Massa | `mt_pnad` only — no trimestral counterpart this round |
| Emprego Formal | Nacional, Setor, UF, Faixa Salarial, Estoque | `mt_caged_setor`/`_uf`/`_salario` (microdata) + `mt_caged` (BCB) |

PNAD: 71 `mt_pnad` + 111 `mt_pnad_trimestral` = 182 series (`D.pnad.series`). CAGED: 86 series
(`D.caged.series`) — 61 category series across the 3 cuts, 3 cut totals, 5 region subtotals, 3 national
rows and 14 estoque series. The two dicts stay **separate** on purpose (`opts.series` picks which one a
table resolves against) — a shared dict would make it too easy to accidentally put a PNAD and a CAGED
row in the same table. See Gotchas for the live-verification method.

## Shared JS factory

`report.html`'s `makeSimpleHierTab(opts)` is instantiated **17 times** (12 PNAD + 5 CAGED) by
`buildTableBlock()`, which also builds each table's DOM (ctrl-bar, table card, chart card) from the
table's own `controls` list — so a 2-select table needs no bespoke markup.

- **`opts.controls`** — 1+ selects. The variant key is the selected values joined with `"__"`, in
  control order: PNAD gives `mensal__yoy`, CAGED's cut tables give `saldo__acum12m`. No special cases
  left — the `"curto"` fallback went with the short-term metric.
- **`fmt` comes from the selected option**, last defined wins across controls. `fmt: "auto"` (PNAD)
  decides per series via `rate_keys`, because one PNAD table mixes % rates and mil-pessoas levels
  (e.g. Subutilização); CAGED's formatting is uniform per control, so it comes straight from the option.
- **The Y-axis title has two mechanisms**, because the problem differs by source: CAGED options carry
  literal `ypart` strings, concatenated across controls (`admissões — pessoas, acum. 12 meses`); PNAD
  options carry `ymode` (`unit`/`diff`) and the JS derives the title from the **plotted nodes** — their
  `def` in the Nível view, p.p.-vs-% by `rate_keys` in the a/a view.
- **Row visibility** — `visibleDeep(node)` hides any row with no series in the current frequency and no
  visible descendant. That is the whole implementation of the Mensal/Trimestral split.
- **`default_expanded`** — table keys to start expanded (CAGED's roots; PNAD's indicator roots).
- **Range buttons live below each chart**, in the same card — HTML pills calling `Plotly.relayout()`
  with a `[from, to]` computed from the plotted traces (`renderRangeBar`/`_dataExtent`), never
  `xaxis.rangeselector`, and "Tudo" sends the real extent rather than `autorange: true`. User request,
  2026-08-27; see `.claude/rules/lis-dashboards.md`.
- **Charts are 600 px tall** (`.pnad-chart` + the height passed to `renderLineChart`), full card
  width. Was 420 px until 2026-08-27.
- **No KPI cards and no on-page methodology paragraph** — both removed 2026-08-27 at user request. The
  methodology moved into the Apêndice accordion "Como ler as tabelas".

## Gotchas

- **`mt_pnad`'s "condição na força de trabalho" columns have NO `forca_` prefix**, despite the script's
  own module docstring listing them under a `forca_*` header — the actual column names are `ocupado`/
  `desocupado`/`fora_da_forca_trabalho` (see `mt_pnad.py`'s own inline comment on `_FORCA`: "nomes ja
  unicos"). Found live (2026-08) via the same "check DB_NAMES against what the table actually has"
  verification this report's Pending item below recommends doing for any future addition — the first
  draft of `pnad_tab.py` used `forca_ocupado`/etc. and silently orphaned the 3 real columns while
  referencing 3 nonexistent ones (`build()` just skips a missing key, no exception). If another
  `mt_pnad` family is ever added to the tree, verify its real column names against a live
  `_load_flat("mt_pnad")` call, not just the script's docstring/comments.
- **No browser has been used to visually confirm** table/expand/checkbox/toggle/chart interactions —
  same standing sandbox limitation as every report in this project. Verification so far is a live DB
  run (182/182 PNAD series matched, no orphans either direction) + a direct plausibility check on the
  computed output (taxa_desocupacao 5.4%, taxa_participacao 62.1%, women's desocupação 7.3% vs. men's
  5.1% — right direction/magnitude for Brazil, 2026-06) + a **jsdom harness** (2026-08, with the CAGED
  tab) that runs the real generated `<script>` against a stubbed Plotly, clicks each tab, flips the
  selects and asserts on the resulting rows/traces/cell formatting. That harness is stronger than the
  stub-`document` approach `analytics/brasil/credit/` uses — `buildTableBlock()` sets `innerHTML` and then
  looks its own selects up by id, which a hand-rolled stub can't model. It confirmed: 4/4/4/5 charts per
  tab, the composite `desligamentos__acum12m` variant resolving correctly, `fmt` switching between
  pessoas and %, `default_expanded`, and (regression) that PNAD's `curto`→`mom` fallback and its
  per-series p.p.-vs-% split still work inside one table.
- **`mt_caged` (BCB) is a STOCK, not a saldo** — its docstring claimed otherwise until 2026-08. Fixed
  there and documented in the table's native MySQL `COMMENT`. Confirmed live: SGS 28763 reads 48,032,308
  for 2026-06, and its month-over-month difference is **exactly** the microdata saldo (145,161) — the
  same universe seen from two independent sources, which is now the cross-check the Apêndice cites.
  `analytics/oraculo/brasil/scores.py` was already treating it correctly (`diff_1m`), so nothing
  downstream needed changing — only the labeling lied.
- **The 3 CAGED cuts must sum to the same national total** — they're partitions of one universe.
  `caged_tab.build()` computes each cut's total from its own categories and **raises** if they diverge
  by more than half a person on any cell, rather than trusting one cut and reusing it. That turns the
  documented invariant into a load-time assertion; it would fire on a partial load of any one table.
- **`mt_caged_setor` has gaps** (5,103 rows vs. the 5,148 of 22×3×78) — a section with no movements in a
  month simply produces no row. `generate_report.py`'s `_load_caged_cut()` reindexes every category onto
  a common monthly axis with `fill_value=0`; without that, the cut sums would misalign in time and the
  12-month rolling windows would slip. Zero is the right fill for an event count (it's "no movements",
  not "unknown"), which is *not* true of the PNAD tables — don't copy this reindexing there.
- **Table keys (`table.key` in `pnad_tab.py`'s `TABS`) only need to be unique within their own tab, not
  globally** — e.g. `ocupacao`'s and `rendimento`'s tables both use the key `"posicao"`. `report.html`'s
  `buildTableBlock()` always prefixes DOM ids with `tabKey + '__' + table.key` (e.g.
  `"ocupacao__posicao"` vs. `"rendimento__posicao"`), so this collision is harmless by construction — but
  if a table is ever moved between tabs or a new table added, don't assume `table.key` alone is
  DOM-unique. Verified live (2026-08) after the 1-tab→3-tab/12-table restructure: 12 tables, 208 distinct
  `seriesKey` references across all trees, of which 26 are header-only dimension-group nodes (5
  indicators × 4 dims + 3 indicators × 2 dims — the arithmetic matches exactly) and the remaining 182
  resolve 1:1 against `series`, with zero `DB_NAMES_MENSAL`/`DB_NAMES_TRIMESTRAL` entries left unreferenced
  by any table.

## Pending

- **CAGED microdata cuts not yet modelled** — município, ocupação (CBO), sexo/idade/instrução/raça. All
  live in the same microdata already downloaded; adding one is a sibling table in `domain/db/brasil/mte/`
  with the same `categoria`/`metrica` shape, then a 6th table here. No migration involved.
- **Pre-2020 formal employment flow** — the Novo CAGED microdata starts 2020-01, so the four flow tables
  do too. Only the Estoque table reaches back to 1992. The old CAGED (different layout) stays out of
  scope; BCB/IPEA would be the path if a long saldo series is ever needed.
- **`mt_pnad_trimestral`'s remaining ~230 series** (rendimento/massa/população/horas by posição/
  atividade/ocupação, and by Sexo/Idade/Instrução/Raça for those same families) — deferred at this
  round's explicit scope decision ("Curado" over "Completo"), not a technical limitation.
- **Nível UF/N3** — out of scope in `mt_pnad_trimestral` itself (see `domain/db/CLAUDE.md`), not
  something this report could add regardless.
- **No derived/modeling metric** (hiato, Okun's law, etc.) — explicitly out of scope this round, at
  user request. Revisit only after the base visualization is validated.
- Open `reports/brasil/Labor Market.html` in an actual browser and confirm interactions (see Gotchas).
