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
report — see [`transforms.py`](transforms.py) for everything it needs: `variants_mensal`/
`variants_trimestral` for PNAD (just `pct_change`/`pp_diff` reused from
`analytics.brasil.fiscal_policy.transforms`) and `variants_caged_*` for CAGED (rolling/YTD sums).

IBGE (PNAD) came first, in 2026-08; CAGED/MTE was added later the same month — see "Emprego Formal"
below.

## PNAD tabs — 3 tabs, 12 tables

Restructured (2026-08, same day as the initial build) from a single "Indicadores" tab with one
monolithic tree into **3 topic tabs × 4 independent tables each**, at explicit user request ("let's
break the tables"). Every table is its own hierarchical table+chart pair — own `<select>` for
Nível/Var. Curto Prazo/Var. Anual, own checkbox/expand state, own Plotly chart — built by the same
`makeSimpleHierTab()` factory instantiated 12 times (`report.html`'s `buildPnadTableBlock()` creates the
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
Sexo/Idade + 5 unmerged mt_pnad-only leaves). **3 KPI cards** at the top of this tab (Desocupação/
Participação/Informalidade, level + Var. Anual in p.p.) — read straight off `series`, no separate calc.

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
why-no-percent + salary bands + the two taxonomies, the points-vs-percent convention, and header-only
rows (noting the CAGED tab has none).

Merging mensal × trimestral is still safe for the same reason as before: `mt_pnad`'s own `_SIMPLES` and
`mt_pnad_trimestral`'s `_VARS_CONDICAO_TAXAS`/`_VARS_SUBUTIL_TAXAS` name 8 headline vars **identically**
(confirmed by reading both scripts, not inferred) — cut by Sexo/Idade/Instrução/Cor ou Raça (5 condicao
vars) or Sexo/Idade only (3 subutil vars) — 111 series, curado from ~340 available (user chose "Curado"
over "Completo"). Rendimento/massa/população/horas by posição/atividade/ocupação (another ~230 series in
`mt_pnad_trimestral`) are **not** in this round — see Pending.

**Nível control** — one dropdown per table (12 total), same 3 options each (deliberately no Nominal/
Real/%PIB/Esfera axes like `fiscal_policy`'s `makeHierTab()` — this report has none of those concepts):
- **Nível** — raw value.
- **Var. Curto Prazo** — resolves to `mom` (month-over-month, `mt_pnad` rows) or `qoq`
  (quarter-over-quarter, `mt_pnad_trimestral` rows) depending on which key the row's series actually
  has; the JS doesn't need to know which table a row came from.
- **Var. Anual** — same period last year (lag 12 for `mt_pnad`, lag 4 for `mt_pnad_trimestral`).

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
  control order: PNAD's single control gives `level`/`curto`/`yoy`; CAGED's cut tables give
  `saldo__acum12m` and friends. `"curto"` is the one special case, falling back to `mom` (mt_pnad) or
  `qoq` (mt_pnad_trimestral) depending on what the series has.
- **`fmt`/`ytitle` come from the selected option**, last defined wins across controls. `fmt: "auto"`
  (PNAD) decides per series via `rate_keys`, because one PNAD table mixes % rates and mil-pessoas levels
  (e.g. Subutilização); CAGED's formatting is uniform per control, so it comes straight from the option.
- **`default_expanded`** — table keys to start expanded (CAGED's roots; PNAD uses none).

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
  `buildPnadTableBlock()` always prefixes DOM ids with `tabKey + '__' + table.key` (e.g.
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
