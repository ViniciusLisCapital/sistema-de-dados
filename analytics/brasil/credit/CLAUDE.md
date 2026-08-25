# analytics/brasil/credit/ — Panorama de Crédito

Self-contained HTML report on Brazilian bank credit, built on `cred_credito_amplo`, `cred_credito_resumo`,
`cred_credito_familias`, `cred_inadimplencia_pj`, the 4 `cred_modalidade_*` tables, `cred_credito_porte`,
`cred_credito_atividade_economica`, `cred_credito_tipo_cliente`, `cred_credito_controle_capital`, and
`cred_ptc` — all `macro_brasil`. Same `/*REPORT_DATA*/` marker-substitution pattern as the other analytics reports, built
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
- `report.html`'s `makeImpulseTab(opts)` — a second, simpler factory (one control group instead of two,
  no Nominal/Real/% PIB axis) instantiated 3× by the Impulso tab. Kept separate from `makeHierTab()`
  because the impulse is already a ratio to GDP, so there is no basis to select — only a read frequency.
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
- No browser has been used to visually confirm any interaction in this report — same standing sandbox
  limitation as every report in this project. Verification so far is a Node harness (stub
  `document`/`Plotly`, not jsdom) run against the real generated `<script>` and real DB output.

## Pending

- Open `reports/brasil/Credit.html` in an actual browser and confirm table/expand/checkbox/toggle/chart
  interactions across all 6 data tabs, plus pan/zoom/quick-range behavior on every chart.
- `cred_credito_controle_capital`'s `saldo`/`provisoes` metrics are still unused (only `inadimplencia` is
  charted, in the Inadimplência tab's "Por Controle de Capital" group).
- `cred_credito_resumo`'s residual un-charted series (`icc`, `concessao_sa`, the Tabela 14 "crédito não
  rotativo" cut) — no tab surfaces them yet.
- PTC tab, possible next steps (none requested): a Selic or realized-credit-growth overlay, both
  explicitly declined. The observada-vs-esperada surprise **was built in 2026-08** at user request —
  and it turned out to be worth more than the earlier note here guessed: the two horizons agreeing in
  *sign* 47 of 52 quarters does not make the *gap* small, since only 25% of deviations fall inside the
  1/N granularity band.
