# analytics/brasil/credit/ — Panorama de Crédito

Self-contained HTML report on Brazilian bank credit, built on `cred_credito_amplo`, `cred_credito_resumo`,
`cred_credito_familias`, `cred_inadimplencia_pj`, the 4 `cred_modalidade_*` tables, `cred_credito_porte`,
`cred_credito_atividade_economica`, `cred_credito_tipo_cliente`, `cred_credito_controle_capital`, and
`cred_ptc` and `cred_fluxo_financeiro` — all `macro_brasil`. Same `/*REPORT_DATA*/` marker-substitution pattern as the other analytics reports, built
directly on [`analytics/report_structure/`](../../report_structure/CLAUDE.md) (no Jinja2, no build step).

Replaces `analytics/credit_stress/` (deleted by the user, along with its `insolv_falencia_rj` table and
`connectors/datajud.py` — see root `CLAUDE.md`'s Pendências if that history is ever needed). Scope is
bank credit only — no bankruptcy/insolvency data.

## Generate

```powershell
uv run python -c "from analytics.brasil.credit.generate_report import run; run()"
# Output: reports/brasil/Credit.html
```

All source tables are already in `jobs/update_db.py`'s routine run — no manual refresh needed first.

## Data source

The BCB workbook in this folder (`202607_Tabelas_de_estatisticas_monetarias_e_de_credito.xlsx`, "Tabelas
de Estatísticas Monetárias e de Crédito") is the map of what's SGS-available for this theme.
[`fontes_dados.md`](fontes_dados.md) has the full per-tabela inventory (what's in the database, what
isn't, and why) — don't re-derive that mapping here. Tabela 2 is the only credit tab left out of the
database entirely (fully redundant with Tabelas 3+4+5). The 3 monetary-aggregate tabs (base monetária,
fatores condicionantes, M1-M4) are a different theme and out of scope for this report.

**Unit**: `cred_credito_resumo`'s `saldo`/`concessao`/`concessao_sa` come from SGS in **R$ milhões**, not
R$ bilhões as the workbook's own headers claim — `report.html`'s `toBi()`/`toTri()` convert client-side.
Percentage-type metrics (`taxa_juros`, `spread`, `icc`, `inadimplencia`, `pct_pib`) need no conversion.

## Shared toolkit

- `analytics/brasil/credit/transforms.py` — `stl_seasonal_adjust()` (STL, frozen-factor "amostra anual"
  convention, same as `analytics/brasil/inflation/fetch_bcb.py`), `pct_change()`, `deflate_series()` (IPCA,
  chained to constant reais of the latest available IPCA month), `compute_pct_pib()`, `moving_average()`,
  and `compute_variants()`/`compute_variants_ma3()` — pre-compute every Nível/Y-Y/M-M/T-T ×
  Nominal/Real/% PIB combination in Python so the browser only reads, never computes.
- `analytics/report_structure/tree_helpers.py` — `leaf()`/`group()`/`direct()` build the hierarchical trees shared
  by every tab. A node only becomes an expandable "group" when the BCB actually publishes an SGS code
  for that rollup; a structural cut with no native total (e.g. porte, controle de capital) gets its total
  as a Python-side `sum_series()` **only when summing a level (R$) is valid** — never for growth-rate or
  percentage children, since summing a ratio across groups is not mathematically valid.
- `report.html`'s `makeHierTab(opts)` — one JS factory (table + expand/collapse + checkbox + chart) reused
  by the Saldo and Concessão tabs; Taxa & Spread, Inadimplência and PTC are bespoke JS instead (their
  shape — a data-source switch, an overlay checkbox, no growth/deflation math — diverges enough that
  forcing them into the factory would add more special-casing than it saves). The three bespoke blocks
  are near-identical in structure, so a new one is written by copying the closest existing one, not by
  generalizing the factory.
- The Apêndice item for PTC is the only one in this report carrying HTML tables (the 5-level scale and
  the per-segment panel size). `.appendix-body table` was already styled in the template — reuse it
  rather than describing a matrix in prose. It runs to **17 numbered points** since 2026-08 (14 is the
  surprise, 15 the σ band and the `1/N` retraction, 16 the 4Q MA, 17 the data corrections) — the harness
  asserts the count, so adding one means bumping it.
- `report.html`'s `makeImpulseTab(opts)` — a second, simpler factory (no Nominal/Real/% PIB axis)
  instantiated 4× by the Impulso tab. Kept separate from `makeHierTab()` because the impulse is
  already a ratio to GDP, so there is no basis to select — only a read frequency. It takes **two
  payload shapes**, and which one applies is decided by whether `opts.treeKey` is set: with it, the
  group holds `trees`/`anchors` maps and series are `[key][freq]` (tables a-c); without it, the group
  holds a single `tree`/`anchor` and series are `[key][variant][freq]` (table d, `fluxo`|`impulso`).
  Table d also passes `variantMeta`, which feeds the Y-axis title, the hover unit and the chart
  header from one place — the unit changes with the selector, so three copies of it would drift.
- **Background bands = the Selic cycle** (2026-08-28, user request; Impulso first, then Saldo).
  Red for a hiking cycle, gray for a hold, blue for a cutting cycle, ~10% alpha, `layer: 'below'`.
  The classification is Python (`impulso_tab.build_ciclos()` over `pm_copom_reuniao`, emitted once as
  the **top-level `D.ciclos`** — it belongs to the report, not to a tab); the colours are `CICLO_CORES`
  in the HTML, mirrored by `.ciclo-legend i` in the CSS (the harness asserts the two strings are
  identical, since nothing else keeps them in sync). Five things not to re-derive:
  - **No smoothing parameter, and that was measured.** Absorbing a run of holds into the surrounding
    cycle when both sides move the same way reads more like market narrative (32 segments instead of 50)
    but swallows the **14-month plateau at 6,50% between mai/2018 and jul/2019**, painting it as a
    continuation of the 2016-2020 easing. A plateau over a year long is the one thing the gray band
    exists to show. Cost of refusing it, also measured: 6 single-meeting bands in the whole series, all
    pre-2005 and so outside every chart's window.
  - **The clip is per chart, not per payload.** The charts share one `ciclos` list but start in
    different years (saldo 2007, impulso/recurso 2002, porte and atividade 2012, fluxo 2015), and a
    `shape` with `xref: 'x'` enters Plotly's autorange — emitting the 2000 band on the porte chart drags
    its axis back 12 years and opens it with colour and no data. Caught by the harness on its first run;
    `_ciclosShapes(dates)` derives the window from the plotted traces, per the rule in
    `.claude/rules/lis-dashboards.md`.
  - **The last cycle extends forward to the end of the data, on purpose** — the report is almost always
    generated between two meetings, so the regime decided at the last one is still in force. That is why
    the segment closes at `fim` and not at its own start date.
  - **`comCiclos` is opt-in per call, never a default.** `renderLineChart()` draws Saldo, Crédito
    Ampliado, Concessão, Taxa & Spread and Inadimplência — turning bands on by default would paint all
    five. They are off on Taxa & Spread (the Y axis is itself an interest rate) and on Inadimplência
    (which already overlays the Selic); Concessão was simply not asked for. The harness asserts the
    negative case too, precisely because Saldo and Concessão come out of the same factory.
  - **On Saldo the Y axis is a stock**, so in `Nível` the band says under which regime that balance was
    accumulated; only the growth metrics put it next to something moving on the decision's own horizon.
    Said in the tab's note rather than left for the reader to work out.
- **Definition cards on every row** (2026-08-28, user request, pointing at
  `analytics/brasil/fiscal_policy`'s: *"coloque essas tag de explicação/definição nos itens"*). The
  row label is the short name; the BCB's official name and an explanation open in a card on hover and
  pin on click — the `lis-dashboard` pattern, fifth report to get it. 165 entries in `NODE_INFO`
  cover **378 of the 409 rows** across the 11 tables. Five things not to re-derive:
  - **The key is namespaced, and here that is load-bearing, not tidiness.** `saldo_livre_pj` is a
    stock in the Saldo tab and a *contribution to the impulse* in the Impulso tab; `porte__mpme` lives
    in three tabs measuring three things. A bare-key map makes one table explain another and **nothing
    throws** — the card opens, with the wrong text. Each table declares its namespaces in order
    (`['saldo','modal']`, `['imp']`, `['spread','modal']`…) and `infoOf()` walks them.
  - **The `modal:` namespace is what makes 51 entries cover ~200 rows.** The BCB's modality tree
    repeats identically in Saldo, Concessão, Taxa & Spread and Inadimplência under four prefixes
    (`livre_pj__`/`livre_pf__`/`direcionado_pj__`/`direcionado_pf__`), so the lookup also tries the
    suffix after the last `__`. It works because the card describes **what the modality is** while the
    unit line says what is being measured — one text for four metrics. Full key beats suffix inside
    the same namespace, which is how `modal:ativ__outros` avoids inheriting `modal:outros`.
  - **`unit` per entry, overriding the table's unit function** — new in this port. The Inadimplência
    tree carries three units at once: inadimplência (>90d), *saldo de maior risco* (% of the PJ
    balance, Res. 2.682 and 4.966) and *atraso 15-90 dias*. The honest fix is a per-row override, not
    a mixed-unit axis string. Everywhere else the unit comes from the same function that titles the
    Y axis, so the selectors (Nível/Nominal-Real/%PIB, Fluxo/Impulso) move both together.
  - **Writing the cards exposed a unit that was already wrong.** `renderTaxaChart()` titled both trees
    `% a.a.`, but the spread is a *difference between two rates* and is measured in p.p. — the card
    would have contradicted the axis. Both now read `taxaYTitle()`, and the harness asserts they do.
  - **Three card sentences were measured before being written**, and one of them came out backwards
    from the obvious text: *Atraso 15-90 dias PJ* does **not** lead the >90d series — correlation
    peaks at lag 0 (0,51 over 185 months) and decays monotonically. Also measured: `total_rotativo`
    is a cross-cutting aggregate that reconstitutes the PF total together with `total_nao_rotativo`
    (702,3 = 702,3 R$ bi in jul/2026), so checking it alongside the modalities double-counts; and the
    published *concessão* total excludes card revolving/instalment and *composição de dívidas* — the
    PF leaves add to R$ 407 bi against R$ 345 bi published.
  Covered by `tests/test_credit_info_js.js` (69 assertions), which resolves every map entry against
  the real trees (**zero orphans** — a typo produces a button that never appears, with no error and
  no visible gap), requires the same key to read differently in two namespaces, and checks the unit
  follows each selector. Verified to fail on an injected typo and on an injected namespace collision.
  One trap it hit first: matching rendered rows to tree nodes **by label** gives false positives —
  "Outros", "Pessoa Jurídica" and "Pessoa Física" repeat dozens of times — so it matches by position
  with the tree fully expanded.
- Every interactive tab clips series to `_TAB_MIN_DATE = "2000-01-01"` before building — most
  modality-level codes only start 2007-03, so a shared start keeps every row on a comparable window.
  PTC is the one exception, and only vacuously: `cred_ptc` starts 2011-04, already inside the window,
  so `_load_ptc_tab_data()` skips the clip rather than applying a no-op.

## Tabs

**Saldo** — hierarchical table (Livre/Direcionado × PJ/PF × modalidade, 67 modalidades + 7
`cred_credito_resumo` totals), plus 3 more top-level groups (Por Porte de Empresa, Por Atividade
Econômica, Por Tipo de Cliente — all PJ-only, `saldo` metric, totals synthesized via `sum_series()` where
no native SGS total exists) and a second hierarchical table below for Crédito Ampliado
(`cred_credito_amplo`, Governo/Empresas/Famílias by instrument — all 4 totals synthesized). Toggles:
Nível/Y-Y/M-M(SA)/T-T(SA) × Nominal/Real/% PIB (% PIB is level-only, by explicit user decision — picking
it disables the other metric pills).

**Concessão** — same tree shape as Saldo, `metrica='concessao'`. Differences from Saldo: the "Nível"
itself is STL+MM3M-smoothed (concessão is a noisy flow, not a stock); only M/M and T/T (no Y/Y); Crédito
Livre PJ's "Cartão de Crédito" has 1 child instead of 3 (the BCB doesn't publish a concessão code for
parcelado/rotativo there — confirmed from the actual SGS codes, not assumed from Saldo's tree).

**Impulso** — credit impulse in p.p. of GDP: `I(t) = [Saldo(t)−Saldo(t−12)]/PIB12m(t) −
[Saldo(t−12)−Saldo(t−24)]/PIB12m(t−12)`. Biggs, Mayer & Pick (2009) as applied to Brazil by the
Blog do IBRE/FGV (Borça Jr., Furtado & Barbosa-Filho, 2021). Three tables, all built by
`impulso_tab.py` + `makeImpulseTab()`: (a) Livre/Direcionado × PJ/PF nested under Total Geral,
(b) porte (MPME/Grande), (c) atividade econômica (Agro/Indústria/Serviços/Outros — only the 4 top
branches, the fine sectoral detail stays in Saldo). One control per table, `Mensal (12m)` vs
`Anual (dez)` — **the same series, not two calculations**: in December the monthly formula already
collapses into the annual one the IBRE publishes.

A **fourth table (d)** carries the *other* impulse — the BCB's own, off the financial flow — see its
own block below. Everything from "Background bands" to "Series start" describes (a)-(c).

- **Background bands = the Selic cycle** — shared with the Saldo tab, documented under Shared
  toolkit. Reading caveat specific to this tab: the band is a **point-in-time** state and the
  impulse is a **24-month window** (the formula uses t, t−12, t−24), so the band does not explain
  the bar above it — it says which cycle that point was observed in. Printed in the tab's note.
- **The decompositions are exact.** The metric is linear in the stock and every row shares the GDP
  denominator, so children sum to their parent with no residual — verified live at ~2e-4 p.p. across
  the whole series, and re-asserted on the *rendered* table by the Node harness.
- **Chart = stacked bars (components) + line (total).** Uses **`barmode: 'relative'`, never
  `'stack'`** — impulse components routinely carry opposite signs (Livre negative while Direcionado is
  positive right now), and Plotly's `'stack'` piles everything in one direction regardless of sign, so
  the stack top would stop matching the total. `'relative'` puts positives above zero and negatives
  below, which is the only way the net stack top coincides with the total line. `_bindYAutofit` already
  handles both modes. The tree root is the line; every other checked node is a bar, **except** a node
  that has a checked descendant (finest level wins) — otherwise checking Livre together with its PJ/PF
  children would double-count the stack. A non-exhaustive selection deliberately leaves a visible gap
  between stack and line. Harness asserts stack-top == line to 2e-4 p.p. over all 208 points (that
  bound is the payload's own 4-decimal rounding, not a modelling residual).
- Replication validated against IBRE's published figures: 2016 total −5,30 (published −5,3), 2020
  públicos +2,78 (+2,8), monthly series crossing zero in nov/2021 (+0,08). The 2020 total (+4,29 vs
  +4,4) differs by BCB revisions to saldo/PIB since the post, not by method.
- **This measure does not strip interest, FX revaluation or write-offs** from the balance change —
  the very critique BCB's EE 110/2021 makes of Biggs et al. Its clean SCR-based version was
  deliberately left out (explicit user decision, 2026-08): BCB doesn't publish the juros/câmbio/baixas
  inputs. A row can print a positive impulse purely from repricing.
- Tables (b) and (c) partition the **same** PJ aggregate, so their totals coincide by construction
  (≤R$5mi apart on R$2,76tri). That aggregate is not exactly `saldo_total_pj` from Tabelas 3-5 — up to
  ~R$37bn (1,3%) apart at the 2020 peak — so (a) does not reconcile to the decimal with (b)/(c).
- Series start: recurso×segmento 2009-03, porte/atividade 2014-01 (the formula eats 24 months of
  history). The table always shows the last 12 observations *with a value*, never leading blanks.

**Impulso — table (d): fluxo financeiro and the BCB's own impulse** (2026-08-28, user request:
"eu quero ver o fluxo financeiro e o impulso"). A different *metric*, not another cut of the same one,
and the difference is exactly the critique BCB's EE 110/2021 makes of Biggs et al.: (a)-(c) start from
the change in the **stock**, so accrued interest, FX revaluation and write-offs count as new credit;
this one starts from the **financial flow** — concessões minus pagamentos —, which is only money that
changed hands. Two readings behind one `Fluxo | Impulso` pill: `Fluxo` is the published level, in
**% of GDP accumulated over 12 months**; `Impulso` is `Fluxo(t) − Fluxo(t−12)`, in **p.p. of GDP**,
derived in `impulso_tab.build_fluxo()` (the table stores what was published, the report computes the
metric — same split as everywhere else here). Tree: Total → PJ/PF, additive and exact, jan/2015 to the
current edition. Source: `cred_fluxo_financeiro` — see
[`domain/db/brasil/bcb/cred_fluxo_financeiro.py`](../../../domain/db/brasil/bcb/cred_fluxo_financeiro.py).
Five things worth not re-deriving:

- **The sign reads backwards at first.** Negative flow = households and firms paid the banking system
  *more* than they borrowed, which is the normal state. The 2024 impulse of +1,2 p.p. happened with the
  flow negative all year (−1,9% → −0,7%), and it reproduces the "+1,1% do PIB" the mar/2025 box prints
  (the 0,1 gap is vintage revision, not method).
- **Three series and only three, and that is a constraint, not a scope preference.** Total/PJ/PF is what
  *both* sources publish: the recurring flow chart in every edition, and the mar/2025 box, which carries
  the same three back to jan/2015 and is therefore what makes 2015-2017 possible at all. The box also
  publishes a Livre/Direcionado split, and that stays **out** — with two sources publishing *different
  sets*, the newer edition overwrites the parent and not the child, the two land on different vintages
  and **additivity stops closing** (0,095 p.p. on PJ, 0,196 on PF, the size of the revision between
  editions; caught by the harness on its first run, and invisible otherwise — the chart's stack would
  simply have stopped touching the total line). With both sources on the same three, an edition writes
  all of them for all of its months at once and the problem cannot arise. Re-adding the split means
  re-deriving a splice rule (*one edition per month*), not just loading more columns.
- **The impulse itself is not a published series.** It came in a *boxe*, twice in the 20 editions with
  an annex (set/2021 and mar/2025), and footnote 1 of the first says there is "no intention of
  calculating these series recurrently or systematically". The flow is what recurs; the impulse is
  derived here.
- **The two sources chain, measured.** Same definition, same unit, 85 overlapping months
  (jan/2018–jan/2025) differing only by vintage revision: PJ 0,038 p.p. mean / 0,095 max, PF 0,059 /
  0,196, Total 0,090 / 0,241. No level correction is applied. Since the current edition wins on overlap,
  the visible seam sits where its window starts (mar/2018 today) and the step there is **0,343 p.p. on
  the total** — the 79th percentile of the series' own monthly steps, inside a stretch rising from
  −5,92 to −4,60, so it does not read as a break. It matters in the *impulse*, where the 12 points whose
  12-month window crosses it carry that revision. Only the **% of GDP** reading is loaded: the same
  recurring chart came out in R$ deflated to the edition's own month through dez/2025, and chaining
  editions there needs a rebasing that does not close (implied factor 1,2655 against 1,2208 of IPCA
  between set/2021 and mar/2025, R² 0,996). `_PADRAO_RECORRENTE` requires "acumulado em 12 meses" in the
  title so an older edition raises instead of silently loading R$ as if it were %.
- **This chart carries a header** (title · what it measures in what unit · source and window), rebuilt
  on every render, per [`.claude/rules/lis-dashboards.md`](../../../.claude/rules/lis-dashboards.md).
  It is the only chart in this report that has one — the others predate the convention — and it is the
  case that most needs it: with a selector that swaps the *unit*, a fixed caption starts lying on the
  first click. `tests/test_credit_fluxo_js.js` (59 assertions) asserts axis title, hover unit and header
  move together, recomputes the impulse from the flow in the payload, and pins the scope — a fourth
  series means the box's split came back, which needs the splice rule redone.

**Taxa & Spread** — a `Taxa Média | Spread` source switch, not a metric/basis toggle (no STL/deflation/%
PIB — already percentages). Taxa Média has smaller modality coverage than Saldo (no "Outros" rate
published anywhere; Livre PJ/PF also missing "Cartão — À Vista"). Spread has no modality breakdown at
all — the BCB never publishes it below recurso×segmento. Independent "Mostrar Selic" checkbox overlays
`cred_inadimplencia_pj.selic` regardless of which rows are checked.

**Inadimplência** — one tree reuniting every cut that publishes inadimplência (>90d, %), not just the
dedicated `cred_inadimplencia_pj` series: the 7 `cred_credito_resumo` totals, modality-level data from all
4 `cred_modalidade_*` tables (smaller coverage than Saldo — Livre PJ's "Cartão" is a single code, Livre
PF's has no "à vista" split), `cred_credito_porte` and `cred_credito_controle_capital` (neither publishes
a native total for this metric, and summing a ratio isn't valid — both render as **header-only rows**:
expandable, but no checkbox/value of their own since their `seriesKey` deliberately doesn't exist in
`series`), and `cred_inadimplencia_pj.atraso_pj` (15-90d, a different metric, kept as an isolated leaf).
Same "Mostrar Selic" pattern as Taxa & Spread.

- **Saldo de Maior Risco** (risk-rating classification, not realized delinquency) lives in this tab as
  two independent top-level groups: `saldo_maior_risco` (pre-4.966 methodology) and
  `saldo_maior_risco_res4966` (current). Confirmed live against the database: **zero date overlap** — the
  old methodology ends 2024-12, the new one starts 2025-01. Never concatenate these into one series —
  splicing would fabricate a level jump that reflects a classification-rule change, not an actual change
  in credit risk.

**PTC** — the BCB's Pesquisa Trimestral de Condições de Crédito (`cred_ptc`, 16 series, quarterly
since 2011-Q2, 61 quarters through 2026-Q2), Brazil's Senior Loan Officer Opinion Survey. Bespoke JS (`ptcState` +
`renderPtcTable`/`renderPtcChart`), same shape as Taxa & Spread: one tree, one pill, no basis toggle.
Built by `ptc_tab.py`, whose docstring is the spec. **Two table+chart pairs since 2026-08**: the level
read, and the surprise (`renderPtcDesvioTable`/`renderPtcDesvioChart`, `ptcDesvioState`) — see the
Surpresa bullets below.

- **Official methodology: BCB Trabalhos para Discussão 245**, Annibal & Koyama (2011),
  [*Pesquisa Trimestral de Condições de Crédito no Brasil*](https://www.bcb.gov.br/pec/wps/port/TD245.pdf),
  §2.3/§2.6 — plus the "Introdução" of any quarterly PTC report. **The reports' own footnote cites
  "TD 254", which is a BCB typo** (254 is an unrelated macroprudential paper). Read TD 245 before
  touching anything about the scale.
- **The value is an unweighted arithmetic mean of responses coded −2..+2**, not a net balance:
  `I = (1/N) · Σ resposta_b`, `resposta_b ∈ {−2,−1,0,+1,+2}`, N = institutions answering that
  question that quarter. The report states it verbatim — "as avaliações são convertidas em valores
  entre -2 e 2 e são apresentadas as médias não ponderadas das respostas". Because the levels carry
  weight 1 and 2, direction *and intensity* live in the same number, so magnitude reads directly:
  |I| ≈ 1 = "the average bank said *moderadamente*", |I| ≈ 2 = "*consideravelmente*". A −0,32 is
  **not** "32% of banks tightened". The tab carries a `.scale-legend` strip spelling the 5 levels out.
- **Range is [−2, +2].** 19 of 976 points break ±1 — extremes −1,21 (`mpme_oferta_esperada`,
  2016-Q1) and +1,57 (`pfh_demanda_observada`, 2020-Q4). The MySQL COMMENT used to say ±1;
  **corrected by `ALTER TABLE` in 2026-08**, and the −2..+2 scale plus the unweighted-mean
  definition now live in the `value` column's own COMMENT. Y axis is left on autoscale: the
  theoretical ±2 would flatten every series against zero.
- **No market-share weighting, deliberately.** TD 245 records this as the dominant international
  practice "pelo fato de que as pesquisas já seriam naturalmente direcionadas às maiores
  instituições financeiras" — the panel covered 92,4%–99,7% of each segment's credit in the first
  round. So absent weights are not a gap to fix.
- **Panel size bounds the granularity, and it's small.** A simple mean over N responses can only
  take multiples of `1/N`. Recovering the implicit N from the series itself (smallest N explaining
  all 4 indicators of a segment in a quarter, given 2-decimal rounding) reproduces the BCB's
  published participant counts: **22** (GE), **28** (MPME), **17** (PF consumo), **7** (PF
  habitacional, 8 in 2011). PF Habitacional therefore moves in ~0,14 steps — a 0,14 move there is
  *one* bank changing its mind, not a regime change, against ~0,04 in MPME. Never compare amplitude
  across segments without this. Each row's label shows `N≈` for that reason (`tree` nodes carry `n`).
- **Sign trap in TD 245**: the demand questionnaire lists options from "substancialmente mais forte"
  (1) to "substancialmente mais fraca" (5) — the *reverse* of the published numeric mapping. In the
  series, positive = stronger demand. Confirmed against 2020-Q2 (GE demanda +0,91 while oferta is
  −0,77). Don't "fix" the sign from the paper's option ordering.

- **Tree = Oferta / Demanda on top, 4 segments under each** (GE, MPME, PF Consumo, PF Habitacional) —
  explicit user choice, 2026-08, so segments are compared side by side within a direction (how the
  Fed's SLOOS reads).
- **No total row, by construction.** The BCB publishes no all-segments aggregate, in SGS or in the
  reports. And averaging the 4 segments here would not reproduce the BCB's own calculation: its
  simple mean runs over *institutions within a segment*, with that segment's panel and
  questionnaire. A cross-segment mean would mix panels of 7 to 28 respondents and credit universes
  of very different sizes, yielding an object that is nobody's index (explicit user decision,
  2026-08: don't synthesize one). So both top nodes are
  **header-only**: `seriesKey` suffixed `_header`, deliberately absent from `series`, no checkbox and no
  value column. Same mechanism as "Por Porte de Empresa" in Inadimplência.
- **Horizonte is a pill, not a tree level** — `series[key] = {observada, esperada}`, the same
  variant-dict payload shape `impulso_tab.py` uses for Mensal|Anual. Keeps the table at 8 data rows.
- Sign convention confirmed live against known episodes: 2015-16 oferta at −1,08/−1,12 with demanda also
  negative; 2020-Q2 oferta negative in all 4 segments while GE demanda jumps to +0,91 and PF-consumo
  collapses to −0,90 (the corporate dash-for-cash against household retrenchment).
- Own chart renderer (not `renderLineChart`): `lines+markers`, because 60 quarterly points leave each
  survey observation unidentifiable on a bare line. Zero line comes from `mkTimeseriesLayout`.
- No STL, no deflation, no % PIB, no growth rates — a diffusion index takes none of them (the survey
  question is *already* relative to the previous quarter). `_load_ptc_tab_data()` also skips
  `_TAB_MIN_DATE` clipping: the series starts 2011-04, already inside the window.
- **Surpresa (2026-08, user request)** — a second table+chart inside the same tab, showing **only**
  `desvio(t) = observada(t) − esperada(t−1)`: the realized quarter against what the banks themselves
  predicted one quarter earlier *about that quarter*. Positive = came in above what the panel
  expected (looser approval, or stronger demand).
  - **The lag is not optional.** `observada(t) − esperada(t)` is not a surprise at all — the
    `esperada` of quarter *t* is a forecast about *t+1*, so the contemporaneous difference compares
    two different periods. `ptc_tab._trimestre_anterior()` steps back by calendar month (−3, with
    jan → oct of the prior year), not by list index, so a future hole in the series yields a missing
    deviation instead of a wrong pair. The harness asserts the contemporaneous version would differ
    on >300 of the 480 points, i.e. the lag is actually load-bearing.
  - **60 points, not 61** — 2011-Q2 has no prior expectation. Its `ref_date` window is therefore
    computed off the `desvio` series, not off `observada`.
  - **"Em linha" is `|MA 4T| ≤ σ₀ of the MA`**, centred on zero — **the MA's limit, not the quarterly
    one**, because the table shows the MA and the two must agree, and because the quarterly one (roughly
    double) would swallow the MA. It runs 0,057 (`pfc_oferta`) to 0,197 (`pfh_demanda`), a 3,4× spread,
    which is why the criterion is **per series and never shared**: one band would classify a series by
    another's standard.
    - **`σ₀` is the RMS about ZERO** — `sqrt(mean(v²))` in `ptc_tab._desvio_rms()`, on the payload as
      `.desvio.rms` / `.desvio_ma4.rms`; the browser only reads it. **This was a bug until 2026-08**
      (user caught it: "validate if the interval, for some seems wrong"): the width came from a
      population sd about the series' *mean* while the band is centred on *zero*, and mixing the two
      centres makes a biased series flag almost everything. `pfc_demanda`'s MA had mean −0,09 against
      width 0,09 — the whole bias fitted inside one σ — so 8 of its 12 visible cells fell outside,
      all negative, purely for the series being itself. RMS fixes it by construction, since
      `RMS² = mean² + variance`. Measured effect: band coverage went from 49%-68% across the eight
      series to **61%-70%** (clustered near the ~68% "1σ" implies) and painted cells in the visible
      window from 31 to **23 of 96**. Signal survived: `pfh_oferta` still has 9 of 12 outside, because
      there the positive surprise is real (last-12 mean +0,11 vs band 0,10).
    - **Don't rename it back to `sd`.** The payload key was `sd` before; a name that says "standard
      deviation" for a number measured about zero is exactly what let the mismatch hide. The harness
      asserts `.sd` is *absent*.
    - Centred on zero rather than on the mean deviation deliberately — zero is the no-surprise point;
      centring on the mean would answer "in line with the usual bias", a different question. A robust
      scale about zero (median |v| ÷ 0,6745) lands within 0,04, so 2015-16 and 2020 aren't inflating it.
    - **The cell tint compares the numbers *as displayed*, 2 decimals** — `Math.abs(Math.round(v*100))`
      against `Math.round(lim*100)`, i.e. `fmtDiffusion`'s own rounding *including* JS's asymmetric
      `Math.round(-6.5) === -6`. Classifying at full precision printed a cell tinted "outside" next to
      a row label showing the identical number (13 of 456 cells contradicted themselves), and using
      `Math.round(Math.abs(v))` instead reintroduces it for exact negative half-cents (`−0,0650` prints
      `−0,06`, must stay grey against a 0,06 limit). The **chart** band stays at full precision — no
      rounding there, and the ≤0,003 disagreement is sub-pixel.
    - It shows in three places: the cell tint (`dv-pos`/`dv-neg`/`dv-flat`), the row label
      (`σ₀ 4T ±0,20`), and a band per checked series on the chart (`layout.shapes` rects,
      `xref:'paper'` so they sweep the plot without entering the x autorange, `layer:'below'` so lines
      stay on top).
    - **Each band is dotted in its own series' colour** (2026-08, same round). They used to be
      identical grey rects deduplicated by σ value: with 2+ series checked they nested with nothing
      saying which was whose, and two of the eight limits are 0,0002 apart — not even distinguishable
      as two bands. The fill only appears when exactly **one** series is checked; with several, nested
      translucent rects darken the middle of the plot and read worse. One annotation only — with 3-4
      nearby limits the per-band labels would collide — giving the value for a single series and the
      range otherwise, and naming the colour convention.
  - **This replaced a `1/N` band in 2026-08, and the retraction is the point.** The first version
    called `|desvio| ≤ 1/N` "in line" on the grounds that such a deviation "fits inside one institution
    changing its mind". The user pushed back and was right: `1/N` is the index's *resolution* at fixed
    N, not a floor on relevance — a `1/N` net is merely *consistent* with one respondent moving, and
    comes just as easily from five moving up against four moving down, which is a lot of churn. Worse,
    the `1/N` grid only exists if N is equal in both quarters, and it isn't: **if N were always 7 in PF
    Habitacional, 100% of its deviations would be multiples of 1/7; 52-58% are.** (GE's 90% is not
    counter-evidence — with N=22 the 0,045 step is close to the published 0,01 rounding, so nearly
    anything passes; where the test has power it refutes the grid.) And there is no sampling model to
    call anything noise — the panel is a census of itself. **Don't reintroduce a `1/N` threshold.** Its
    one correct use is the opposite bound, now in the chart's hover: `ceil(|desvio| × N)` is the
    *minimum* number of respondents that must have changed level (GE's +0,26 in 2026-Q2 needs ≥6 of
    22). A lower bound, never a count — offsetting moves are invisible to it.
  - Side finding, deliberately not overstated: the mean deviation is negative in three of the four
    *demanda* series (−0,06 to −0,09) and ≈0 in *oferta* — banks lean slightly optimistic on demand.
    With 60 autocorrelated quarters this is **not** called significant anywhere in the report.
  - **Lines, two per series, never bars** (user request, 2026-08 — the tab shipped with grouped bars
    for one round). Quarterly: `lines+markers`, `width: 1`, `opacity: 0.4`. MA: `lines`, `width: 2.5`,
    full opacity. Same colour and same `legendgroup` per series, names suffixed `(trim.)` / `(MA 4T)`.
    No `barmode` in the layout at all. Bars were dropped partly on request and partly because two
    overlaid series per segment would leave grouped bars too thin to read the MA against — but if bars
    ever come back, they must be `'group'` and never stacked: the segments don't sum (there is no PTC
    total), unlike Impulso where `'relative'` is required *because* the parts do sum.
  - **Own `checked`/`expanded` state, not shared with `ptcState`** — it's an independent read, and
    coupling them would make a click on the level table silently change what the surprise shows. The
    harness asserts the horizonte pill / collapse / checkbox on the level table leave it untouched.
    Default selection is GE oferta + GE demanda (the level table's is the 4 oferta segments).
  - **The primary read is the 4Q moving average, not the raw quarterly deviation** (user request,
    2026-08). `ptc_tab._ma4()` → `series[key].desvio_ma4`: trailing, so the point at *t* is the mean of
    *t−3..t* (the last closed year, never looking forward), 57 points instead of 60, and it only
    aggregates windows of 4 **consecutive** calendar quarters (checked via `_trimestre_anterior`) so a
    future hole yields a dropped window instead of a mean over points a year-plus apart. The table shows
    the MA and tints against the MA's σ; the chart shows **both** — quarterly thin/faded, MA thick.
    - **The MA's σ₀ is ~half the quarterly σ₀** (measured ratios 0,38–0,69, mean 0,51), so the
      band had to be recomputed: the quarterly σ would keep the MA inside the band almost always. Which
      means the thin line *does* leave the band often — correct, and documented in the caption, since the
      band describes the typical variation of the *mean*.
    - **0,50 is what you'd get from independent deviations** (`σ/√4`), and the measured AR(1) of the
      quarterly deviations runs −0,23 to +0,21 — near-zero persistence. So this MA is mostly averaging
      approximately independent noise, **not** revealing a slow cycle. It's good for accumulated bias
      (GE demanda's MA went +0,07 → −0,14 over four quarters, a full year of demand undershooting the
      banks' own forecast), not for extrapolating trend. Both the caption and Apêndice point 16 say so.
    - **Adjacent cells share 3 of their 4 quarters**, so MA points are strongly autocorrelated by
      construction — never read two neighbouring cells as independent observations.
    - The raw quarterly number left the table but not the tab: it's the thin line, and the MA line's
      hover shows the MA *and* that quarter's raw deviation side by side.
  - Payload: two derived variants on the same dict, `series[key].desvio` and `.desvio_ma4` — the pill
    still only switches `observada`/`esperada`, and `generate_report`'s console count excludes both
    (it iterates `ptc_tab.HORIZONTES`, so adding a variant can't inflate the "16 series" line).

**Apêndice** — accordion of methodology notes for each tab above (small-base noise in near-extinct
modalities, coverage gaps, the % PIB/unit conventions, the Saldo de Maior Risco break).

## Gotchas

- Crédito ampliado (~R$19.7tri) and crédito do sistema financeiro (~R$7.3tri) are different universes and
  shouldn't reconcile — `cred_credito_amplo` includes government securities and external debt that never
  touch a bank balance sheet.
- `cred_ptc`'s 4 obsolete SGS codes (21397/21399/21401/21403) are **frozen since 2022-10** — the BCB
  never discontinued the survey, it just moved to new codes. An earlier version of this report read the
  frozen ones via `cred_inadimplencia_pj.ptcc_*`; those were removed. Never reintroduce them.
- Small-base modalities (e.g. "Arrendamento Mercantil — Veículos", ~R$5-13mi saldo) can show
  thousands-of-percent swings month to month — mathematically correct, not a bug; read by level, not
  growth rate, documented in the Apêndice.
- **The Impulso tab is only as current as `atv_pib_mensal`, and it truncates silently.** The formula
  needs GDP at t, so a credit series reaching July against a `pib_acum_12m` stopping in June yields
  `None` for July — and `makeImpulseTab()`'s `refDates()` takes the last 12 **non-null** observations,
  so the table just shows a window ending a month earlier, with no gap and no warning. Hit for real on
  2026-08-28: the credit note was loaded and the dashboard regenerated, and Impulso still ended in
  jun/2026 while every other tab showed jul/2026. `atv_pib_mensal` was in **no** calendar group at all
  (the `--coverage` audit had been listing it); it is now in `bcb_credit_note` **and** in
  `bcb_external_sector_note`, which is where the monthly-GDP block actually lands — a day earlier, and
  the only one of BCB's three M-1 notes that needs GDP in dollars (SGS 4385/4192). It is not tied to
  the IBC-Br, contrary to the natural guess: the IBC-Br runs a 2-month lag (2026-08-17 delivered
  2026-06) while the four GDP series already held 2026-07, so monthly GDP is a month **ahead** of the
  activity index. If Impulso ever looks a month behind again, check `atv_pib_mensal`'s `MAX(date)`
  before anything else.
- No browser has been used to visually confirm any interaction in this report — same standing sandbox
  limitation as every report in this project. Verification so far is a Node harness (stub
  `document`/`Plotly`, not jsdom) run against the real generated `<script>` and real DB output.

## Pending

- Open `reports/brasil/Credit.html` in an actual browser and confirm table/expand/checkbox/toggle/chart
  interactions across all 6 data tabs, plus pan/zoom/quick-range behavior on every chart.
- **Confirm the cycle bands in a real browser** (2026-08-28, Impulso and Saldo): whether ~10% alpha
  reads as "subtle but visible" both under stacked bars (Impulso) and under thin lines (Saldo),
  and whether 26-47 bands across ~20 years look like a regime map or like stripes. If it's too
  busy, the lever is the alpha in `CICLO_CORES` + `.ciclo-legend i` (keep the two in sync — the
  harness asserts it), not the classification.
- `cred_credito_controle_capital`'s `saldo`/`provisoes` metrics are still unused (only `inadimplencia` is
  charted, in the Inadimplência tab's "Por Controle de Capital" group).
- `cred_credito_resumo`'s residual un-charted series (`icc`, `concessao_sa`, the Tabela 14 "crédito não
  rotativo" cut) — no tab surfaces them yet.
- PTC tab, possible next steps (none requested): a Selic or realized-credit-growth overlay, both
  explicitly declined. The observada-vs-esperada surprise **was built in 2026-08** at user request —
  and it turned out to be worth more than the earlier note here guessed: the two horizons agreeing in
  *sign* 47 of 52 quarters does not make the *gap* small, since only 25% of deviations fall inside the
  1/N granularity band.
