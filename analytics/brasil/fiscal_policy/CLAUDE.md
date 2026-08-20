# analytics/brasil/fiscal_policy/ — Panorama Fiscal

Self-contained HTML report on Brazilian fiscal data (`reports/brasil/Fiscal Policy.html`). Same
`/*REPORT_DATA*/` marker-substitution pattern as the other reports in `analytics/` — no Jinja2, no
build step — built on [`analytics/report_structure/`](../../report_structure/CLAUDE.md) (`/*THEME_CSS*/`
and `/*Y_AUTOFIT_JS*/` markers).

## Generate the report

```powershell
uv run python -c "from analytics.brasil.fiscal_policy.generate_report import run; run()"
# Output: reports/brasil/Fiscal Policy.html
```

`fisc_efgg`, `fisc_rtn`, `fisc_investimento`, `atv_pib_valores_correntes`, `atv_pib_taxas`,
`atv_pib_mensal`, `inflc_agregados` are all in `jobs/update_db.py`'s routine run — no manual refresh
needed.

## Current state — 5 tabs

**1. Receitas e Despesas** — default tab, **two independent hierarchical table+chart pairs, one per
methodology** (do not reconcile with each other by design — see the Apêndice's "GFSM vs. RTN — Duas
Metodologias" note).

- **GFSM** (`gfsm_tab.py`): same interaction pattern as `analytics/brasil/credit/`'s Saldo/Concessão —
  checkbox to plot, ▸/▾ to expand a GFSM category into its subcodes. Tree: Receita/Despesa by
  economic nature (GFSM 2014). An **Esfera** dropdown swaps the whole tree between Governo Geral
  (consolidated)/União/Estados/Municípios (`fisc_efgg`'s `geral_`/`central_`/`estados_`/`municipios_`
  namespaces); row check/expand state survives the switch.
- **RTN** (`rtn_tab.py`): same mechanics, Governo Central only, classified by rubrica orçamentária
  (benefícios previdenciários, pessoal, discricionárias por função, etc.), monthly. Tree (restructured
  2026-08, at user request) has 3 root nodes: **Receita Líquida** (→ Receita Total [with its own
  RFB/RGPS/incentivos/não-administradas children] + Transferências por Repartição), **Despesa Total**
  (→ benefícios previdenciários/pessoal/outras obrigatórias/discricionárias, unchanged), and
  **Resultado Primário** (`resultado_primario_governo_central`, 2026-08, STN code 8055 — confirmed
  identical to `receita_liquida − despesa_total`). Default checked series: `receita_liquida` +
  `despesa_total` + `resultado_primario_governo_central` (not `receita_total` — see Gotchas).
- **3 independent metric axes (reorganized 2026-08, at user request — replaces the old "Nível/Y-Y/T-T
  (or M/M) × Nominal/Real/%PIB × Bruto/(Trimestral/)Acumulado" framing)**, all pre-computed in Python
  (`analytics/brasil/fiscal_policy/transforms.py`) and switched client-side via `<select>` dropdowns (converted
  from pill-buttons 2026-08, at user request — "click drop" for each axis; same forcing/disabling logic,
  now via `<option disabled>` instead of a `.pill.disabled` class, see `makeHierTab()`'s `wireControls()`),
  none replacing another:
  - **(a) Nível — aggregation frequency**: GFSM offers **Trimestral** (native quarterly value,
    `compute_variants()`) / **Acumulado 12m** (`compute_variants_ttm()`, 4-quarter rolling sum); RTN
    additionally offers **Mensal** (native monthly value, via
    `analytics.brasil.credit.transforms.compute_variants()`) alongside its own **Trimestral**
    (`compute_variants_quarterly_step()`, calendar-quarter sum, NOT rolling — the same non-overlapping
    3-month cut GFSM uses natively, added so the two tables compare quarter-to-quarter, see Gotchas
    "double-check 1T/2026") and **Acumulado 12m** (`compute_variants_monthly_ttm()`, 12-month rolling
    sum). A series' own native frequency caps which options exist — you can reduce frequency (RTN
    monthly → quarterly/12m) but never invent a higher one (GFSM has no Mensal). Internal dict keys
    unchanged from before the relabeling: GFSM `{"bruto": ..., "acum": ...}`, RTN `{"bruto": ...,
    "trimestral": ..., "acum": ...}` (`"bruto"` = Mensal/Trimestral-native, just relabeled in the UI).
    **RTN Trimestral display (fixed 2026-08)**: the underlying `quarterly_step_level()` still repeats
    each quarter's value across its 3 calendar months (needed so the Y/Y=12/T-T=3-month `pct_change()`
    lags stay correct) — but `report.html`'s `makeHierTab()` now collapses the DISPLAYED dates/values
    down to one column per quarter (first month only, e.g. Jul/25 — "like GFSM"), via
    `collapseToQuarterStart()` + `opts.quarterlyStepAccum: 'trimestral'` (RTN_TAB only). Before this fix
    the table showed the same quarterly figure 3× in a row (Jul/25, Ago/25, Set/25 all identical) —
    user-reported (screenshot), verified against an independent manual quarterly sum via a Node harness
    (see Gotchas).
  - **(b) Nominal ou Real** — whether the Nível value is IPCA-deflated. Orthogonal to (a) and (c).
  - **(c) Modelagem**: **Nível** (raw value, no transform), **Y/Y** (same period last year), **Marginal**
    (immediately preceding period — resolves in JS to the underlying `mom_sa` key at Nível=Mensal or
    `qoq_sa` at Nível=Trimestral; **disabled entirely at Nível=Acumulado 12m**, where the only
    comparison offered is Y/Y — a "Marginal" of the accumulated base would measure the acumulado's own
    acceleration, not the trimestre-vs-trimestre reading the label implies, deliberately not offered to
    avoid conflating the two), or **% PIB** (nominal only — forces Nominal/disables Real in the UI when
    selected). **% PIB's own denominator now depends on Nível** (2026-08 change, was always TTM/TTM
    before): at Mensal/Trimestral, it's the *same-period* GDP, no accumulation on either side
    (`compute_pct_pib_same_period()` — RTN denominator `atv_pib_mensal.pib_mensal`, SGS 4380, raw
    monthly, vs. the already-used `pib_acum_12m`/SGS 4382 for Acumulado; GFSM denominator
    `atv_pib_valores_correntes.pib_pm` raw quarterly, vs. the rolled `pib_4t` for Acumulado); at
    Acumulado 12m, still TTM/TTM (`compute_pct_pib_ttm()`, unchanged, matching `fisc_nfsp`/IEG's own
    convention elsewhere in this report — user confirmed keeping this at Acumulado 12m rather than
    dropping %PIB there entirely). See Gotchas for the `incentivos_fiscais` sign/outlier quirk, more
    visible under Acumulado.
  - **Open question, not yet decided** (user asked this be recorded): should % PIB, when Real is
    selected, divide by a *real* GDP instead of nominal? For now % PIB is nominal-only regardless of
    the Nominal/Real toggle (deflator would cancel if it did divide by real GDP, so today's nominal-only
    answer is already numerically equivalent to "real ÷ real" — the open question is only whether a
    distinct real-GDP-denominator framing is ever worth exposing, not a live bug).

**2. Dívida Líquida (DLSP)** (new 2026-08) — the conditioning factors of net public debt, from
`fisc_dlsp_fatores` (BCB's `Facdetp.xlsx` tabela especial, not in the SGS). **Nine sections, one per
fator, mirroring the workbook's nine sheets** (user's framing: "Separate the tables like in the excel:
Estoque, Primario and so on"): Estoques (month-end stock) + Primário, Juros, Ajuste Metodológico
Interno/Externo, Ajuste de Paridade, Ajuste Caixa-Competência, Reconhecimento de Dívidas, Privatizações
(monthly flows).

- **`dlsp_tab.py` builds the payload; `report.html`'s `makeDlspHierTab()` renders each section.** The 9
  sections are **generated in JS** from `D.dlsp.fatores` (`renderDlspTab()`), not hand-written — 9
  identical blocks differing only by fator, and their chart divs use a shared `.dlsp-chart` class in the
  CSS width/height rule rather than 9 more IDs (see Gotchas — a chart div missing from that rule collapses
  to zero width).
- **First section is "Balanço por Entidade" (2026-08)** — the same 95 items reorganized as
  **Entidade › Passivos | Caixa e equivalentes | Títulos e créditos › item**, with a **Fator** dropdown
  applying that tree to any of the 9 fatores, plus the usual Nível/% PIB. Built on two live-verified
  properties: `interna__X + externa__X = total__X` per entity and the 5 entities summing to the
  consolidated total, both **0.000000** deviation over all 295 months; and the three buckets being a
  *partition* of the same leaves, so `Passivos + Caixa + Créditos = Líquido` holds by construction —
  classification affects interpretation, never arithmetic (worst observed residual R$0.50mi, just the
  payload's 1-decimal rounding over ~20 summed items). `_CLASSE` in `dlsp_tab.py` is the hand-curated
  map of all ~86 leaves → bucket (+ optional label override); `build_entity_tree()` **raises** if a leaf
  is missing from it, so a new BCB line can't silently drop out of the balance sheet. Bucket aggregates
  are synthetic (`bal__{ent}__{bucket}`) since the BCB publishes no "total liabilities of the BCB";
  summing `level` and `pctpib` term-by-term is valid **only** because every item shares the same 12m-GDP
  denominator — if Y/Y or Real ever land here, that shortcut breaks.
  - **Why entity-first rather than consolidated** (this is the whole point, don't undo it): two item
    pairs are intra-government and cancel exactly — União⇄BCB (Conta Única ±R$2.06tri, carteira do Bacen
    ±R$2.97tri) and União⇄estados/municípios (Lei 9.496/MP 2.185 — sum of both sides is zero in *all* 295
    months —, Lei 8.727, dívidas reestruturadas). Per entity they're real positions (flagged `⇄` in the
    label) and the **nets still sum to DLSP automatically**, because the pairs cancel in the net. Never
    sum the gross column across entities: that gives R$18.4tri of liabilities vs R$12.0tri consolidated
    (91% of GDP), a ~40% gap nothing in the number signals.
  - **"Caixa" only exists in this view.** The Treasury's cash cushion *is* Conta Única (R$2.06tri, 15.6%
    of GDP) but it's a deposit at the BCB, so it nets to zero when consolidated — leaving ~R$54bn of
    commercial-bank demand deposits (0.4% of GDP). International reserves are **not** a separate line in
    `Facdetp.xlsx`: they're inside the BCB's net external position (footnote 15/, −R$1.81tri), classified
    as caixa with that spelled out in the label. A gross-reserves line would need `cmb_reservas_bc`.
  - 77 of the 86 leaves hold one sign across all 295 months. The 4 genuinely ambiguous ones (Previdência
    Social, Equalização Cambial ×2, Demais Contas do Bacen) are classified **by concept, not by observed
    sign**, so in an opposite-sign month they render as a negative value inside their own bucket rather
    than jumping buckets over time.
- **Two metrics only, by explicit scope** ("For now, the only metric should be Level and % GDP"): no
  Nominal/Real, no Y/Y, no Marginal, no frequency toggle. `Nível` = the value as published (R$ correntes);
  `% do PIB` = always over `atv_pib_mensal.pib_acum_12m`, but the **numerator differs by fator nature** —
  month-end stock for `estoque`, **12-month rolling sum** for the 8 flows. A raw monthly flow over a
  single month's GDP would be noise matching no publication; the 12m accumulation is the standard
  convention, is what `fisc_nfsp`'s `*_pct_pib_12m` already uses here, and preserves the identity in %GDP
  terms (Σ 8 flows accumulated 12m ÷ GDP 12m = the 12-month change in the stock as % of GDP).
- **Why a separate JS factory and not `makeHierTab()`**: same reason `makeImpulsoHierTab()` is separate —
  different axes. Also a different payload shape: all 855 series share one date grid and one tree, so
  `dates`/`tree` live once at the payload root and each series is a bare array pair, instead of the
  `{dates, values}`-per-variant shape `makeHierTab()` expects. That choice is why this tab costs 1.95 MB
  for 855 series while `rtn` costs 9.69 MB for 35 (see Pending).
- **Identically-zero series ship as the scalar `0`** (364 of 855 — the methodological/parity/cash-accrual
  adjustments only touch ~25 of the 95 items), expanded back to zeros by `dlspZeros()` in JS. Accepted
  side effect: on an identically-zero item, `% do PIB` shows 0,00% in the sample's first 11 months where a
  non-zero item shows "—" (the 12m window isn't full there, but a rolling sum of zeros is zero anyway).
- Default state per section: only the `total` root checked, and expanded into its 5 debtors — checking all
  three roots would plot the same aggregate twice (`total = interna + externa`), allowed but not the
  default.

**3. Investimento** (new 2026-08) — investimento do Governo Federal por GND, from `fisc_investimento`
(Tesouro's Tema 13, monthly, 2008-01→). **Two table+chart pairs, one per corte** (`funcao` = GND ×
função orçamentária, 60 series; `natureza` = GND × natureza da despesa, 18) — same GFSM/RTN layout as
tab 1, built by `investimento_tab.py`.

- **Why two tables and not a Corte dropdown** — the GFSM Esfera selector swaps the *namespace* of an
  identical taxonomy; here the two trees genuinely diverge below the GND, so switching corte would have
  to swap the tree too, and the user's check/expand state would point at keys the other corte doesn't
  have (`gnd4__funcao_saude` has no counterpart under `natureza`). Two tables avoid that without
  generalizing `makeHierTab()`'s tree handling.
- **Only the two capital GNDs exist in this source** — 4 Investimentos (creates a new asset) and 5
  Inversões Financeiras (only transfers title to an existing one). **Default checked is GND 4 + GND 5
  separately, not the `total`**, and that's the point of the tab: the 1.38%-of-GDP peak in 2020 is
  almost entirely GND 5 (0.83pp — pandemic capitalizations), a financial operation, not asset-creating
  investment. Summing them into one line hides exactly the distinction the GND cut exists to show.
- **4 Nível windows × 5 modelagens × Nominal/Real**, all pre-computed in Python: **Mensal** (raw month,
  STL `period=12` for M/M and T/T), **Trimestral** (calendar quarter step, `quarterlyStepAccum` collapses
  the display to one column per quarter), **Acum. 12m** (rolling), **Acum. no ano** (YTD, resets each
  January — `transforms.compute_variants_ytd()`/`ytd_sum()`). Audited against
  [`analytics/metric_layers.md`](../../metric_layers.md) in 2026-08; the three findings that pass are
  recorded there, the three that changed the tab are below.
- **% PIB uses convention B — denominator is always `atv_pib_mensal.pib_acum_12m` (SGS 4382)**, in all
  four Níveis, with only the numerator following the selected window (user choice, 2026-08, resolving
  `metric_layers.md`'s Open convention 1). Reads as an annualized share of output, which makes the four
  Níveis mutually comparable — Jun/26 GND 4: 0.054% Mensal / 0.157% Trimestral / 0.594% Acum. 12m /
  0.245% Acum. no ano. **This diverges from the GFSM/RTN tables in tab 1, which stay on convention A**
  (same window both sides), so the same report now serves both: a Trimestral % PIB here is ~4x smaller
  than one read in tab 1. The y-axis says `% do PIB 12m (<Nível>)` precisely so that gap is legible;
  the GFSM/RTN retrofit was offered and declined.
- **Trimestral T/T is seasonally adjusted at `period=4`** (2026-08) via
  `compute_variants_quarterly_step(seasonal=True)` → `quarterly_step_qoq_sa()`. RTN deliberately stays
  on the unadjusted default. This mattered more than expected: federal execution is systematically
  back-loaded (mean level 2008-2025 — T1 R$7.1bn, T4 R$16.0bn, 2.2x), so the raw T/T was mostly
  calendar — 2026-Q1 read −54.6% raw vs. +12.7% adjusted, 2026-Q2 +72.5% raw vs. +5.9% adjusted.
  **The STL runs on the collapsed quarterly series, not the monthly step** — `period=4` over a step
  that repeats each quarter 3× would treat four consecutive *months* as a cycle.
- **Two deliberate exclusions, enforced by the new `opts.metricAvailability` hook** (which disables
  `<option>`s per Nível, generalizing the legacy `marginal` rule — GFSM/RTN keep the old path
  unchanged): **M/M at Trimestral** (the value is a constant step inside the quarter, so month-on-month
  is 0% within it and an artificial jump at the turn) and **M/M + T/T at Acum. no ano** (both would
  cross the January reset, where a closed year becomes one month). **These are settled, not a judgment
  call** — `metric_layers.md`'s "Degenerate combinations to disable" table mandates exactly these two,
  and its YTD section gives the reason ("YTD offers **only** Y/Y"). The user's original instruction
  asked for M/M and T/T on every accumulation and I was about to enable all four cells on that basis;
  the spec settles it the other way. Don't re-open without changing the spec first.
- **8 of the 78 series cross zero, and keep their growth options anyway** (user choice, 2026-08).
  `ajuste_ordem_bancaria` is the extreme case — negative in 61 of 222 months, ranging −R$3.46bn to
  +R$3.42bn — plus isolated negative months in six GND 5 functions and `gnd5__demais`. A percent change
  on a sign-flipping base has no economic reading, and `metric_layers.md` says such flows should get no
  percent change at all; the user chose to document the caveat in the Apêndice rather than build the
  per-series mask the current per-Nível `metricAvailability` can't express. Recorded as Open convention 5
  in that file. A further 36 series contain at least one exact zero — those cells are `—` now, not
  `Infinity` (see Gotchas).
- **Divergence from RTN, on purpose — don't "fix" one to match the other**: M/M and T/T stay
  **enabled** at Acum. 12m here, where RTN disables its equivalent. Requested explicitly ("Y/Y, M/M and
  Q/Q growth ... for each acumulation"); the acceleration-of-the-window reading is spelled out in the
  chart caption and the Apêndice rather than hidden by disabling.
- **Payload uses the compact shared-dates shape** (`dates` once at the root, bare value arrays, scalar
  `0`/`null` for identically-zero/empty variants — 145 of 2,340 variants compress that way, mostly the
  28 orçamentária functions that never receive an inversão financeira). Measured: **3.63 MB vs. 15.31
  MB** in the `{dates, values}`-per-variant shape `makeHierTab()` natively expects — more than the whole
  rest of the report. `makeHierTab()` reads it via the new `opts.root`/`opts.sharedDates` hooks. This is
  the same problem the Pending item below records for `rtn`/`gfsm`; this tab was built without it.

**4. Impulso Fiscal (IEG)** — Resende & Pires' (FGV/Tesouro, 2024) Impulso Estrutural do Gasto: fixed
multipliers (Folha 1.32 / Transferências 1.46 / Investimentos 1.66 / Outras 0.64) applied to the
change (% of GDP) of 4 `fisc_efgg` spending categories — `generate_report.py`'s `_load_ieg()` /
`_ieg_contrib_for_esfera()`. Two variants per category, `{"acum4t": ..., "quarter": ...}` (see "Quarter
(T/T) methodology" below) — no standalone IEG chart anymore, only through "Visão Combinada" and "IEG por
Esfera e Categoria" below (the old standalone "IEG" line chart and "IEG × PIB" comparison chart were
**removed 2026-08** at user request, redundant with those two). Multipliers are the paper's own
published values, **not re-estimated** for this project's data.

**Visão Combinada** — single chart at the TOP of the tab, now overlaying **three impulse metrics on one
shared y-axis**: IEG (total), Impulso via Resultado Primário (total), and Impulso via Crédito a Inst.
Financ. Oficiais (% GDP, see below). Switchable via one "Comparação" dropdown
(`impulso-combinado-view-select`) between **4T/12m Acumulado (Y/Y)** and **Trimestre (T/T)** (genuinely
seasonally-adjusted since 2026-08, not a shortcut).

- **The GDP line was removed 2026-08 at user request** — with it went `yaxis2`, so this is a
  single-axis chart again. `atv_pib_taxas` is still loaded into `D.pib_yoy` (`acum_4t`/`qoq`/`yoy`) but
  nothing plots it; don't "restore" it without asking.
- **The three metrics share an axis but are not the same transformation.** IEG and the PB impulse are
  *changes* (p.p. of GDP between two annual windows); the credit metric is a *flow* accumulated over 12
  months as % of GDP. They share the axis because the order of magnitude matches and the sign means the
  same thing in all three (positive = expansionary) — spelled out in the chart caption so a reader
  doesn't take it for a common transformation.
- **The credit line is always the 12m accumulation**, regardless of the Comparação dropdown — the metric
  has no quarterly variant, and its trace name carries "acum. 12m" explicitly so that reads as
  deliberate rather than a bug. Asserted in the harness (switching to Trimestre changes IEG but leaves
  the credit line untouched).

**Quarter (T/T) methodology (2026-08, rewritten a second time)** — first version (see git history) used
a T/T-on-TTM shortcut (a lag-1/lag-3 diff on the already-accumulated series, no STL) for both IEG and
the PB impulse, chosen to avoid new data ingestion. User later rejected this after seeing the combined
chart ("the metrics [aren't] talking to each other") and asked for genuine seasonal adjustment on both,
since the underlying data (`fisc_efgg`'s native quarterly cadence; BCB's *monthly* primary-result flow)
supports it. Current implementation:
  - **IEG**: `_ieg_contrib_for_esfera()` computes each category's RAW (non-accumulated) quarterly %GDP
    (`pib_pm`, not the rolled `pib_4t`), runs `transforms.stl_seasonal_adjust(period=4)`, then
    `.diff(1)*mult` on the seasonally-adjusted series — `_stl_on_valid_window()` fits STL only over that
    category's own dense (non-NaN) date range, never a `.reindex()`-padded one (see Gotchas — this was a
    real bug found live, not a style choice).
  - **PB impulse**: `fisc_nfsp` only ever stored the 12m-accumulated %GDP series — 6 new BCB SGS codes
    (raw monthly flow, R$ mi, `resultado_primario_fluxo_mensal` + 5 esfera counterparts) were added to
    `domain/db/brasil/bcb/fisc_nfsp.py` and backfilled (`run(start="all")`), confirmed live both by
    catalog search AND numeric reconciliation (rolling-12m-sum of the new flow ÷ 12m GDP matches the
    existing `*_pct_pib_12m` columns to <0.01pp) and by an identity check (coarse 3-way codes = sum of
    the finer esfera codes, same pattern as the existing accumulated series). `_impulso_quarter_via_stl()`
    (`generate_report.py`) takes a rolling 3-month sum of flow and of GDP first (raw monthly flow is too
    noisy — one-off payments can swing a single month by R$100bn+ — a naive month-to-month STL diff
    produced implausible ±7pp swings before this smoothing was added), divides, STL-adjusts
    (`period=12`), then `pp_diff(3)`.
  - GDP's own "quarter" reading is unchanged — `atv_pib_taxas`'s official `qoq` indicador (already
    seasonally adjusted by IBGE).
  - **Seasonal factors are frozen at the last complete calendar year (2026-08, user request)** —
    `transforms.stl_seasonal_adjust()` fits STL only on the sample ending at the last year that has all
    `period` observations (`seasonal_cutoff_year()`), and extrapolates into the incomplete current year
    by carrying that year's fitted factor forward per season position. In-sample dates keep STL's own
    local (evolving) factor; only the extrapolation is frozen. Re-run once the year closes. This
    diverges on purpose from `analytics/brasil/credit/transforms.py`, which freezes the whole-sample *mean*
    per month — here the seasonal pattern trends strongly (PB flow: Jan factor 2.22 in 2021 → 3.80 in
    2025, ~8pp amplitude), so a whole-sample or 3-year mean lags it by up to ~0.7pp. Effect on the
    published numbers: negligible over history (median shift 0.04pp IEG / 0.01pp PB impulse) but
    material at the recent end (median ~0.9pp / ~0.3pp since 2024, up to ~2pp at the latest
    observation) — which is exactly the region the old full-sample fit was contaminating with the
    half-finished current year. Applies to the GFSM/RTN tabs' "Marginal" modelagem too (same helper).

**Reconciliation changed by this rework — read before trusting cross-sums under "Trimestre"**: the
**4T/12m Acumulado** variant is unaffected and still reconciles exactly (linear TTM diffs) — category
sums to esfera total, esfera sums to the consolidated total, all within SGS/JSON rounding. The
**Trimestre** variant does NOT carry the same guarantee across independent STL fits: within one esfera,
category-sum-to-total is still exact (the total is *defined* as that Python sum, not independently
fit); but **cross-esfera** sums are not — IEG's União+Estados+Municípios vs. Geral, and the PB impulse's
5-esfera sum vs. the consolidated total, can diverge by a median of ~0.2pp and up to ~1-2pp in some
quarters (STL is not a linear operator). Documented in both report captions and the Apêndice, not
treated as a bug — see Gotchas.

**Both decomposition sections below share one JS factory, `makeImpulsoHierTab()`** (2026-08, replaced
the old `makeIegHierTab()` + chart-only PB section). Table with checkbox-to-plot and ▸/▾ expand, one
**Nível** dropdown, chart = `renderRelativeBarWithLine()` (every checked row is a `barmode:'relative'`
bar; a fixed total line on top, independent of what's checked). **Deliberately does NOT reuse
`makeHierTab()`** — that function's Nominal/Real/%PIB axes don't fit already-weighted p.p.
contributions. Checking a parent *and* its children double-stacks the same value; that's the reader's
call, not blocked.

**IEG por Esfera e Categoria** — tree is **Esfera › Categoria de despesa** (2026-08, restructured at
user request — "the hierarchy should be: Sphere > Expenditure categories… maintain just the 'Nível'
click-dropdown"): 4 esfera roots (Geral/União/Estados/Municípios), each expanding into the 4 spending
categories. The **Esfera dropdown is gone** — the esfera became the tree's first level. Fixed line =
IEG Governo Geral; default checked = União+Estados+Municípios (they stack exactly onto it under 4T
Acumulado). `_load_ieg()`'s payload: `{dates, ieg, ieg_quarter, tree, series}` — `series` is keyed by
**both** the bare esfera (`"geral"`, the parent's own total) and `"{esfera}__{categoria}"` (the
children), 20 keys total; the separate `esfera_total` dict was folded into `series` so both tree levels
resolve through one `seriesKey`. **No Banco Central esfera here** (unlike the PB impulse below) —
`fisc_efgg`/EFGG only covers Governo Geral/Central/Estados/Municípios.

**Impulso via Resultado Primário por Esfera** — same table+chart, but a **flat sphere list, no second
level** ("the same… but only with the spheres") — the BCB publishes no expenditure-category cut inside
each sphere. `fisc_nfsp`'s 5 esfera series (governo_federal excl. Banco Central/banco_central/estados/
municipios/empresas_estatais, both the `*_pct_pib_12m` accumulated codes and the `*_fluxo_mensal` raw
codes) feed it via `_load_fiscal_impulse_nfsp()`'s `tree` + `esfera` payload; fixed line = the
consolidated-public-sector total. Nível toggles **Acum. 12m (Y/Y)** (exact reconciliation) and
**Trimestre (T/T)** (independent per-esfera STL, see reconciliation note above). Banco Central's own
contribution is consistently ~0 (confirmed live), included anyway for completeness — uncheck it in the
table to drop it.

**Impulso via Crédito a Inst. Financ. Oficiais** (new 2026-08, user request) — the **parafiscal channel**,
which neither of the two metrics above captures. When the Treasury lends to an official financial
institution (historically BNDES, in volume), it's a *financial* operation: it builds a Federal asset and
never touches above-the-line primary spending, yet it is expansionary. `_load_impulso_credito_oficial()`
takes the **`primario` fator only** of `fisc_dlsp_fatores`'s `interna__gov_federal__creditos_inst_fin_oficiais`
(plus its 2 published subcomponents, which sum to the parent exactly), rolls it **12 months**, and **flips
the sign** — in the workbook's convention lending makes the item *more negative* (the asset grows), and
lending is the impulse, so ×−1 puts it on this tab's `positive = expansionary` convention. Offered in
**Nível** (R$ mi) and **% PIB** (over `pib_acum_12m`, same TTM/TTM convention as the rest of the report),
via `makeDlspHierTab({dataKey:'credito_oficial', noFator:true})` — the factory was generalized (payload +
tree keys, optional fator layer, injectable yTitle) so this is its 11th instance rather than a 4th bespoke
table.

- **Validated against the known history of the channel, with no tuning**: peak **+4.65% of GDP in
  2010-05** (post-crisis BNDES capitalization), reversing to **−2.65% in 2018-08** (BNDES prepayments to
  the Treasury), **+0.67% in 2026-06**. Magnitudes are the same order as — in some years larger than —
  the IEG, which is the argument for the metric existing.
- Only `primario` is in scope: the same item also carries `juros` and `ajuste_met_interno` flows
  (deliberately excluded). And this is a **flow**, not the stock — the item's balance today is a ~R$204bn
  asset (1.5% of GDP), far below the cycle peak.

**5. Apêndice** — methodology notes for the four tabs above (accordion, `<details>`/`<summary>`).

**Historical, not current**: 3 earlier tabs (Visão Geral, Dívida Pública, Resultado Fiscal) were
deleted 2026-08 at the user's request to rebuild the report tab-by-tab; a separate, older RTN-based
Receita e Despesa tab was also deleted then and has since been reintroduced in a new form (`rtn_tab.py`,
above). `fisc_divida` (BCB SGS, DBGG/DLSP) is still untouched by `report.html` — updated by
`jobs/update_db.py` but not read here. `fisc_nfsp` now has 16 series total (10 `*_pct_pib_12m` +
6 `*_fluxo_mensal`, see above) — `resultado_nominal_pct_pib_12m`/`juros_nominais_pct_pib_12m` remain
unused by this report. Full detail on what the 3 still-deleted tabs looked like is in git history, not
duplicated here — see Pending.

## Excel audit workbook

`export_audit_excel.py` (`uv run python -c "from analytics.brasil.fiscal_policy.export_audit_excel import run; run()"`
→ `reports/brasil/fiscal_policy_audit.xlsx`) — original/adjusted series + every intermediate step of both
impulse metrics (IEG × 4 esferas × 4 categorias; PB impulso × 5 esferas + total), one sheet per
variant (Acumulado/Trimestre, both metrics) plus a Reconciliação sheet. Every pure-arithmetic step
(accumulation, %PIB ratio, diff, sign flip) is a **live Excel formula**, not a pasted number — only
the STL output itself is pasted (yellow-filled), since a LOESS decomposition isn't reproducible as a
native Excel formula. Deliberately duplicates `generate_report.py`'s computation (not imported wholesale)
so every intermediate has its own column instead of collapsing to the final result — but reuses the
same `transforms.py` primitives and `_stl_on_valid_window()`, and was verified cell-for-cell against
`_load_ieg()`/`_load_fiscal_impulse_nfsp()`'s actual output before shipping. Two rules the script must
keep:
- **Fit STL on each series' own native date window before aligning to the shared display grid** — same
  rule as the Gotchas entry above; aligning first would reintroduce that exact bug in the audit script
  itself. Go through `_stl_on_valid_window()` rather than `tf.stl_seasonal_adjust()` directly, or the
  leading NaNs of a rolling window get backfilled into the fit and the workbook stops matching the
  report.
- **A sheet's date grid must start early enough for its own lookback formulas to resolve.** The `PB
  Impulso - Trimestre (STL)` sheet deliberately runs on a *longer* grid than its Acum. 12m sibling (the
  union of the 6 monthly-flow series, 1998→, not `resultado_primario_pct_pib_12m`'s 2002-11→): its
  `SUM(...)`/`Δ3m` formulas look backwards **within the sheet**, so on the shorter grid the first 3
  rows came out blank even though the report publishes values there. An audit that can't reproduce the
  first published values isn't an audit.

## Data map

| Tab | Tables read |
|---|---|
| Receitas e Despesas — GFSM | `fisc_efgg` (all 27 GFSM codes × 4 esferas, 108 series), `atv_pib_valores_correntes.pib_pm` (%PIB denominator — raw quarterly for Nível=Trimestral, `rolling(4)` TTM for Nível=Acumulado 12m, see `_load_pib_4t()`/`_load_pib_pm_raw()`), `inflc_agregados.ipca` (Real deflator) |
| Receitas e Despesas — RTN | `fisc_rtn` (34 codes, Governo Central), `atv_pib_mensal` (both `pib_mensal`/SGS 4380 — raw monthly, %PIB denominator at Nível=Mensal/Trimestral — and `pib_acum_12m`/SGS 4382 — TTM, %PIB denominator at Nível=Acumulado 12m), `inflc_agregados.ipca` (Real deflator) |
| Dívida Líquida (DLSP) | `fisc_dlsp_fatores` (all 95 items × 9 fatores = 855 series, + 135 synthetic balance-sheet aggregates = 990), `atv_pib_mensal.pib_acum_12m` (%PIB denominator for both the stock and the 12m-accumulated flows) |
| Investimento | `fisc_investimento` (78 series = 60 `funcao` + 18 `natureza`), `atv_pib_mensal.pib_acum_12m` (SGS 4382 — the **only** %PIB denominator here, all four Níveis; convention B), `inflc_agregados.ipca` (Real deflator) |
| Impulso Fiscal — via Crédito a Inst. Financ. Oficiais | `fisc_dlsp_fatores` (`primario` fator of `interna__gov_federal__creditos_inst_fin_oficiais` + 2 subcomponents), `atv_pib_mensal.pib_acum_12m` |
| Impulso Fiscal — IEG | `fisc_efgg` (4 expense categories × 4 esferas), `atv_pib_valores_correntes` (`pib_pm` — both raw quarterly, for STL, and rolled TTM, for Acumulado), `atv_pib_taxas` (`acum_4t`+`qoq` indicadores — Visão Combinada; `yoy` loaded but unplotted) |
| Impulso Fiscal — via Resultado Primário (NFSP) | `fisc_nfsp` (`resultado_primario_pct_pib_12m` + 5 esfera `*_pct_pib_12m` — Acum. 12m; `resultado_primario_fluxo_mensal` + 5 esfera `*_fluxo_mensal` — Trimestre/STL), `atv_pib_mensal.pib_mensal` (raw monthly GDP, STL denominator) |
| Impulso Fiscal — Visão Combinada | Reads already-loaded `ieg`/`fiscal_impulse_nfsp`/`pib_yoy` payloads, no new table |

Full table schemas (SGS codes, PK patterns) are in [`domain/db/CLAUDE.md`](../../../domain/db/CLAUDE.md)
and each script's own docstring — not duplicated here.

## Gotchas

- **NFSP impulse vs. RTN Resultado Primário — different series, don't cross-check directly** (found
  2026-08, real user confusion, not a bug): the Impulso Fiscal tab's "Impulso via Resultado Primário"
  uses `fisc_nfsp` (BCB, setor público consolidado). The RTN tab's own "Resultado Primário" row
  (`resultado_primario_governo_central`, %PIB Acum. 12m) is a DIFFERENT series (Governo Central only).
  Live-verified both are internally correct for the same month: RTN showed +0,11%→−1,08% (Jun/2025→
  Jun/2026, delta −1,19pp), NFSP showed +0,15%→−1,19% (same months, delta −1,34pp, impulso +1,34%) — a
  user read the RTN figure expecting it to explain the NFSP impulse number and got a mismatch that
  looked like a calc bug but wasn't. Both captions (section + Apêndice) now spell this out explicitly
  with the verified numbers — if this confusion recurs, the fix is clearer UI copy, not the formula.
- **GFSM tab, Governo Geral totals only**: `Receita`/`Despesa` (root nodes) sum the three esferas
  cell-by-cell without netting intergovernmental transfers (FPE/FPM, SUS, royalties) — inflates
  **both** totals (confirmed live: transfers ≈ R$1.36tri over the last 4 quarters, ~10% of GDP) by
  the same mechanism on both sides of the ledger (a transfer is simultaneously the paying sphere's
  expense and the receiving sphere's revenue — summing all 3 spheres without netting double-counts it
  on whichever side you're reading) vs. a proper netted consolidation. União/Estados/Municípios
  selected individually don't have this problem. Documented in the report's own Apêndice; not fixed
  (see Pending).
- **GFSM "Governo Geral" (default Esfera) vs. RTN "Governo Central" is NOT scope-comparable — this is
  the single biggest source of "these two tables don't add up" confusion** (confirmed live, 2026-08,
  after a user-reported ~800bi RTN vs. ~1.7tri GFSM gap for 1T/2026 Receita, ~53% of quarterly GDP).
  Two causes stack: (1) GFSM's default view is **Geral** (all 3 government levels combined), while
  RTN only ever covers **Governo Central** — comparing Geral against Central compares scopes of very
  different size by design; (2) Geral is further inflated by the intergovernmental-transfer
  double-count above. Controlling for scope (GFSM **União**, not Geral, vs. RTN) narrows the gap from
  ~2.2x to ~18% (1T/2026: GFSM União receita_total = R$918.6bi vs. RTN receita_total = R$776.1bi) — a
  residual attributable to source/classification differences (SIAFI+Siconfi consolidated by STN,
  GFSM 2014 classification, vs. Tesouro's own Série Temporais by rubrica orçamentária) not
  investigated further. **Always switch GFSM's Esfera to União (never leave it on Geral) and use
  RTN's Trimestral toggle (see above) before comparing any value between the two tables** — spelled
  out with the full numbers in the report's own Apêndice.
- **BCB SGS's NFSP series (`fisc_nfsp`) use the opposite sign convention** from "resultado
  primário/nominal" as normally reported — `domain/db/brasil/bcb/fisc_nfsp.py` flips sign at ingestion
  (`_FLIP_SIGN`). If a new series from this same SGS family is ever added, check for this inversion
  before trusting the sign.
- **`fisc_dlsp_fatores` (new 2026-08, not consumed by this report yet) keeps the UNFLIPPED sign — the
  opposite of `fisc_nfsp`.** Its flows are debt-conditioning factors, so positive = *increases* net
  debt, i.e. `primario` positive = primary **deficit**. Deliberate: flipping would break the additive
  identity `estoque[t] − estoque[t−1] = Σ 8 fluxos[t]`, which is the whole reason that table exists.
  Confirmed live that `fisc_dlsp_fatores.primario` (item `total`) and
  `fisc_nfsp.resultado_primario_fluxo_mensal` are exact negatives of each other across all 295 shared
  months (max |sum| = 0.017 R$ mi, just SGS's 2-decimal rounding). Any chart mixing the two tables must
  flip one of them.
- **`fisc_rtn.incentivos_fiscais` (RTN 10.01.1.2) is a deduction, not a revenue** — measures tax
  revenue foregone under LRF art. 14 (isenções/anistias/remissões/créditos presumidos), so it's
  structurally ≤ 0, unlike its 3 sibling children of `receita_total`. Confirmed live over the full
  series (1997-01→2026-06, 354 obs): 98 negative, 254 exactly zero, only 2 positive (rounding-scale).
  From 2024-01 onward it's zero every month (one exception, -R$1.4mi in 2025-12) — effectively dead
  for ~2.5 years, cause unconfirmed. Also has an isolated outlier at 2017-12 (-R$1,356mi, ~9x any
  other month) — likely a year-end catch-up entry. Under the **Acumulado** toggle (see above) that
  single-month outlier smears across the following 12 months of the accumulated series instead of
  appearing as one isolated spike (under **Bruto**, the default, it's an isolated single-month value
  as normal). **The zero-base `Infinity` this series used to produce is FIXED (2026-08)** — because it
  has been exactly 0 every month since 2024-01, its Y/Y divided by that zero base from ~2025-01 onward
  and pandas' `pct_change()` emitted `inf`, which the old `np.isnan()` guard let through into the
  payload as a bare `Infinity`. Both copies of `pct_change()` (`credit/transforms.py`,
  `fiscal_policy/transforms.py`) now guard with `np.isfinite`, so the cell shows `—`. The audit that
  found it was much wider than this one series: **6,814 `Infinity` values were shipping** — 1,642 in
  `rtn` and 5,172 in `investimento` (36 of its 78 series contain an exact zero). Beyond the literal
  "Infinity%" cell, a single infinite point in a plotted trace collapses Plotly's y-autorange and
  `_bindYAutofit()`'s fitted range, so whole charts were unreadable rather than just one row. The
  harness now walks the entire payload asserting every number is finite.
- **RTN's `receita_total` (gross) is not comparable to `despesa_total`** — use `receita_liquida`
  (already net of revenue-sharing transfers to states/municipalities). `receita_total` reconciles to
  nothing when compared directly to `despesa_total`. This is why the RTN tab's chart defaults to
  `receita_liquida`, not `receita_total`.
- **GFSM and RTN's %PIB figures for the "same" category don't converge, and shouldn't** — at Nível=
  Acumulado 12m both use the same TTM/TTM annualization convention (confirmed live, 2026-06: Despesa
  Total RTN [Governo Central] ≈ 20% of GDP vs. GFSM's União Despesa Total ≈ 33-35% of GDP for the same
  period), but the underlying scope differs: GFSM classifies constitutional transfers to states/
  municipalities (FPM/FPE/IPI-EE) as an *expense* of the paying sphere (GFSM code 26); RTN nets the
  same transfers out on the *revenue* side instead (`receita_liquida`) — a real, expected gap from
  classification, not a bug. Don't try to reconcile GFSM and RTN line items against each other, at any
  Nível.
- **%PIB is no longer always TTM/TTM (2026-08 change)** — it now follows whichever Nível is selected:
  same-period (no accumulation either side) at Mensal/Trimestral, TTM/TTM only at Acumulado 12m. A
  %PIB value read off the Trimestral toggle will look different in scale from the same series' %PIB
  under Acumulado 12m — that's by design (matches "PIB do mesmo período" as the user specified), not
  a bug; don't average or compare %PIB values across different Nível selections.
- **DBGG and DLSP are not directly comparable** — DBGG excludes Banco Central and state enterprises,
  DLSP includes them. Don't "reconcile" the two into one number.
- **No SICONFI/subnational data** — this report never had individual states'/municipalities' own
  revenue/expenditure line items, only Governo Central (RTN) and BCB SGS aggregates plus (now) GFSM by
  esfera. Would need SICONFI's RREO/RGF API, a materially different integration. This is also the
  reason RTN's own "Receitas e Despesas" table has no Esfera selector (a user asked why, 2026-08,
  after seeing GFSM's Esfera dropdown right above it in the same tab) — RTN **is** the Tesouro's own
  budget-execution report, so it structurally only ever covers Governo Central; there's no
  Estados/Municípios cut to add without a different data source entirely. GFSM already has the
  esfera cut for revenue/expenditure (via `fisc_efgg`) — the report's own RTN section caption now
  says this explicitly and points back to the GFSM selector, instead of leaving it unexplained.
- **Fitting STL on a `.reindex()`-padded series silently distorts the result far past the padded
  region — found and fixed live, 2026-08.** `_ieg_contrib_for_esfera()` originally reindexed every
  esfera's raw category series onto the full shared date grid (`idx`, 2006+) *before* running STL.
  `central_` has real data back to 2006, but `geral_`/`estados_`/`municipios_` only exist from 2010 —
  reindexing gave the latter 3 an artificial ~16-quarter leading NaN block, which
  `stl_seasonal_adjust()`'s `interpolate(limit_direction="both")` backfills with the first real 2010
  value. That flat, artificial prefix skews STL's trend/seasonal fit over the *entire* series, not just
  near the padding — confirmed live: before the fix, União+Estados+Municípios came out ~4-5x different
  from Geral in some quarters (e.g. 2025-Q3: 0.40 vs. 1.85), not the small residual expected from STL's
  non-linearity alone. Fixed by `_stl_on_valid_window()` — dropna() and fit STL only over each series'
  own dense range, reindex back to the full grid only after. If a similar per-esfera/per-cut STL is
  ever added elsewhere in this project, replicate this pattern, not the reindex-first one.
- **A Plotly trace with `x`/`y` undefined renders as nothing, silently — found 2026-08, had been
  shipping broken.** `impulsoRPEsfera()` returned `D.fiscal_impulse_nfsp.esfera[key][variant]`, which is
  a **bare value array** (all esferas share the payload's top-level `dates`), while the caller read
  `.dates`/`.values` off it — so all 5 esfera bars of "Impulso via Resultado Primário por Esfera" were
  drawn with `x: undefined, y: undefined` and only the total line (which came from a correctly-shaped
  `impulsoRPTotal()`) appeared. Plotly throws nothing for this. It survived a full round of
  verification because the reconciliation checks ran against the **Python payload**, never against the
  traces the chart actually receives — the v5 Node harness now asserts on `Plotly.react`'s captured
  trace objects (count, names, and that the bars stack onto the line) precisely to close that gap.
  Whenever a payload stores parallel arrays against one shared date axis, re-wrap to `{dates, values}`
  at the accessor, and assert on traces, not on the payload.
- **Chart CSS sizing bug — found live, 2026-08**: `#chart-impulso-rp` (now removed) and
  `#chart-impulso-rp-esfera` were missing from the CSS selector list that gives chart divs an explicit
  `width`/`height` (`.chart-card #chart-* { width: 100%; height: 560px; }`) — a `<div>` with no CSS
  sizing collapses to near-zero width, which is likely why the user described the esfera chart as
  "not by sphere" (bars rendered too narrow to read, not a data/methodology bug). Whenever a new
  `chart-*` div is added to this report, it MUST be added to that same selector list or it silently
  renders broken.
- **`makeHierTab()` now reads TWO payload shapes** (2026-08, with the Investimento tab) — the original
  `{dates, values}`-per-variant one (`gfsm`/`rtn`) and the compact shared-dates one (`investimento`:
  `dates` once at the payload root, each variant a bare value array or the scalar `0`/`null`). Which one
  it uses is decided by whether `opts.sharedDates` is passed; `wrap()` re-expands the compact form.
  **A new instance must pick one and pass the matching opts** — feeding a compact payload without
  `opts.sharedDates` yields traces with `x: undefined` (the silent-blank-chart bug already documented
  below), and feeding a `{dates, values}` payload *with* it would put an object where a value array
  belongs. Same for `opts.root`: needed only when the block isn't directly at `D[dataKey]`.
- **Actual browser rendering has not been visually confirmed** for any tab — verification here is a
  live DB run + a Node stub-`document`/`Plotly` harness against the real generated `<script>`, no real
  browser available in this sandbox.

## Pending

- **Regenerate `reports/brasil/Credit.html`** — `analytics/brasil/credit/transforms.py`'s `pct_change()` was fixed in
  2026-08 (zero-base guard, see Gotchas) but only the fiscal report has been rebuilt since. That report
  shares the function, so it is presumed to be carrying `Infinity` values in any series that ever hits
  an exact zero; the count there has not been measured. Same applies to any other report built on
  `credit/transforms.py`.
- **Deflator for capital spending** — the Investimento tab deflates GND 4/5 by the IPCA, like every
  other tab. For works and equipment the INCC or the FBCF deflator would be more defensible. Raised
  2026-08, recorded in `metric_layers.md`'s Open conventions, not decided.
- **Convention split on `% PIB` inside this one report** — the Investimento tab moved to convention B
  (always 12m GDP) in 2026-08 while GFSM/RTN stayed on A (same window both sides). The retrofit was
  offered and declined at the time; until it happens, a reader comparing % PIB across tabs of this
  report is comparing two conventions, mitigated only by the y-axis label.
- **Rebuild the remaining deleted tabs (Visão Geral, Resultado Fiscal)** — not started, no design
  decided. `fisc_divida`/`fisc_nfsp`'s own series are still unread by this report except through the
  Impulso Fiscal tab (`fisc_nfsp`) — note that **Dívida Pública was effectively superseded** by the new
  Dívida Líquida tab, which covers the same ground from a better source (`fisc_dlsp_fatores` decomposes
  the stock *and* explains its variation, where `fisc_divida` only has 6 aggregate %PIB series).
- **Consolidado mode for the Balanço por Entidade** — deliberately not built. Proper consolidation drops
  both sides of each intra-government pair, which changes each entity's net (states' net would fall by
  their Lei 9.496 liability, the Union's would rise by its credit) while leaving the total unchanged — so
  it isn't a per-entity view at all, it's a single consolidated column (R$12.0tri liabilities / R$2.5tri
  assets). Adding it means a second tree shape, not a toggle. The `⇄` labels + Apêndice cover the gap for
  now.
- **Gross reserves as their own line** in the balance sheet — today they're inside the BCB's net external
  position (`externa__bacen`, footnote 15/), classified as caixa with the netting stated in the label.
  Splitting them out needs `cmb_reservas_bc` joined into `dlsp_tab.py`.
- **A stacked-bar conditioning-factors chart is the obvious next step for the Dívida Líquida tab** — one
  bar per fator summing exactly to the change in the stock for a chosen item, the visual form the identity
  is begging for. The current tab is 9 independent line charts, which shows each fator's own history well
  but never shows them adding up. Not built; would need a 10th section reading across `D.dlsp.series`
  (all the data is already in the payload, no new ingestion).
- **`rtn`'s payload is 9.69 MB of the report's ~15 MB** (measured 2026-08) — 35 series × 3 frequencies ×
  2 bases × 4 metrics, each carrying its own copy of the 354-date array. `gfsm` is 3.34 MB the same way.
  For comparison, the Dívida Líquida tab ships **855 series in 1.95 MB** because `dlsp_tab.py` puts
  `dates` once at the payload root and stores bare value arrays. Migrating `rtn`/`gfsm` to that shape
  would cut the file several-fold; not attempted (it means touching `makeHierTab()`'s accessor, shared by
  both tables).
- **Fix the GFSM Governo-Geral double-count** (see Gotchas) — needs `fisc_efgg.py`'s `_build_geral()`
  to net out intergovernmental transfers before summing; a dedicated reconciliation project, not a
  one-line fix.
- **Revenue-side fiscal-impulse multiplier — methodology undecided.** Data (`receita_*`, 44 series ×
  4 esferas) is ingested and charted in the GFSM tab, but there's no reliable multiplier to weight a
  revenue change into a combined fiscal-impulse index (the IEG paper itself excludes revenue —
  multipliers disagree even in sign across studies, endogeneity with the business cycle). Three options
  on the table, none chosen: borrow a published estimate, estimate our own (SVAR + narrative
  identification), or show revenue change as context only with no multiplier. See
  `analytics/brasil/fiscal_policy/reference/` for the underlying literature review.
- **IEG multiplier re-estimation** — deferred, not started. Current multipliers are Resende & Pires'
  own VAR estimate (sample 2010T1–2023T4); re-estimating against this project's own data would need its
  own VAR fit, no design decided.
- **MEFA** (Monitor de Expansão Fiscal Ampliada) — blocked on data sourcing (no live restos-a-pagar
  endpoint found as of 2026-08-06); re-verify live before trusting that verdict, since a prior "blocked"
  call on IEG turned out to be wrong.
- **Investimento tab — cuts not yet surfaced.** The tab covers both cortes the source publishes, so
  there's nothing missing from `fisc_investimento` itself. What's absent is any *derived* reading: no
  real-vs-nominal growth decomposition, no comparison against the IEG's `investimento` category
  (`fisc_efgg`, GFSM code, Governo Geral scope — a different universe, so it needs a scope note before
  being charted side by side), and no split of GND 4's asset-creating core from its capital transfers as
  a single "investimento próprio" line.
- **Not integrated into `analytics/oraculo/`'s macro thermometer.**
- Open the report in an actual browser and confirm interactions feel right (see Gotchas).
