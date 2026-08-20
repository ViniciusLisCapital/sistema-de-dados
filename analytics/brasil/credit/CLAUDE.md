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
# Output: reports/Credit.html
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
  rather than describing a matrix in prose.
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
since 2011-Q2), Brazil's Senior Loan Officer Opinion Survey. Bespoke JS (`ptcState` +
`renderPtcTable`/`renderPtcChart`), same shape as Taxa & Spread: one tree, one pill, no basis toggle.
Built by `ptc_tab.py`, whose docstring is the spec.

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
- **Range is [−2, +2].** 19 of 960 points break ±1 — extremes −1,21 (`mpme_oferta_esperada`,
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

- Open `reports/Credit.html` in an actual browser and confirm table/expand/checkbox/toggle/chart
  interactions across all 6 data tabs, plus pan/zoom/quick-range behavior on every chart.
- `cred_credito_controle_capital`'s `saldo`/`provisoes` metrics are still unused (only `inadimplencia` is
  charted, in the Inadimplência tab's "Por Controle de Capital" group).
- `cred_credito_resumo`'s residual un-charted series (`icc`, `concessao_sa`, the Tabela 14 "crédito não
  rotativo" cut) — no tab surfaces them yet.
- PTC tab, possible next steps (none requested): a Selic or realized-credit-growth overlay (both
  explicitly declined for this round), and the observada-vs-esperada surprise
  (`observada(t) − esperada(t−1)`) as a derived read — worth little on its own, since the two agree in
  sign 47 of 52 quarters for `ge_oferta`.
