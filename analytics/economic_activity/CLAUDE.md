# analytics/economic_activity/ — Panorama de Atividade Econômica

Self-contained HTML report on Brazilian real-activity data: GDP (PIB), industrial production (PIM),
retail (PMC), services (PMS) and the BCB's monthly GDP proxy (IBC-Br) — all from `macro_brasil`, all
already kept current by `jobs/update_db.py` (see [`domain/db/CLAUDE.md`](../../domain/db/CLAUDE.md)'s
Active tables table). Same `/*REPORT_DATA*/` marker-substitution pattern as `analytics/inflation/` and
`analytics/exchange_rate/` — no Jinja2, no build step — and built directly onto
[`analytics/report_structure/`](../report_structure/CLAUDE.md) from the start (both `/*THEME_CSS*/` and
`/*Y_AUTOFIT_JS*/` markers), unlike `inflation/`/`exchange_rate/` which migrated onto it after the fact.

**PIB tab (2026-08, second pass, per explicit user guidelines)** goes further than the other five
tabs: it uses the IBGE's own *officially published* growth rates (`atv_pib_taxas`) instead of a
ratio computed from the volume index, adds the accumulated-4-quarters rate, and adds a full
growth-decomposition (contribution-to-growth) section following the BEA/IBGE methodology also used
by BCB and IPEA in their own conjuntura commentary — see "PIB tab methodology" below. The other five
tabs (Produção Industrial, Comércio, Serviços, IBC-Br, and the Visão Geral aggregation of all of
them) still use the original ratio-on-volume-index approach described in "Architecture" below — the
user's guidelines for those are still pending.

## Generate the report

```powershell
uv run python -c "from analytics.economic_activity.generate_report import run; run()"
# Output: reports/economic_activity_latest.html
```

No manual data-refresh step needed first (unlike `inflation/`'s `fetch_bcb.py`) — `atv_pib`,
`atv_pib_encadeado`, `atv_pib_taxas`, `atv_pim`, `atv_pmc`, `atv_pms`, and `atv_ibcbr` are all already
in `jobs/update_db.py`'s routine run.

## Architecture

`generate_report.py` reads MySQL tables via `MySQLDataRequester`, reshapes each into a flat
`{key: {dates, values}}` dict (`_series_dict()`), and hands the combined result to
`analytics.report_structure.builder.render_report()`. Every table load is independently try/excepted —
one missing/broken table degrades only that group's charts (empty `{}` in `REPORT_DATA`), not the whole
report, same convention as the other two reports. Seven `REPORT_DATA` groups in total: `pib`, `pim`,
`pmc`, `pms` (all via `_load_suffixed()`, see key-naming convention below), `ibcbr` (via `_load_flat()`),
plus two PIB-only groups added in the second pass — `pib_enc` (`atv_pib_encadeado`, also via
`_load_suffixed()`, same shape as `pib`) and `pib_taxas` (`atv_pib_taxas`, via the dedicated
`_load_pib_taxas()`, different key format — see "PIB tab methodology" below).

**Key-naming convention, deliberately uniform across `pib`/`pim`/`pmc`/`pms`/`ibcbr`/`pib_enc`**: every
series key in the JSON payload ends in `_sa` (seasonally adjusted) or `_nsa` (not adjusted), regardless
of which DB column actually carries that information —
- `atv_pib`/`atv_pib_encadeado`/`atv_pim`/`atv_pmc`/`atv_pms` store SA/NSA in a separate `seasonal_adjs`
  column (`"Y"`/`"N"`) with an unsuffixed `name` (e.g. `pib_pm`) — `generate_report.py` appends the
  `_sa`/`_nsa` suffix itself at read time (`_load_suffixed()`).
- `atv_ibcbr` already bakes the suffix into `name` itself (e.g. `ibcbr_sa`, `ibcbr_agropecuaria_nsa` —
  see `domain/db/brasil/bcb/atv_ibcbr.py`) — `generate_report.py` just groups by `name` as-is
  (`_load_flat()`), no suffix added, since the result already matches the same `_sa`/`_nsa` convention.

This means `report.html`'s JS never needs to know which table a series came from to find its SA/NSA
pair — `ser(group, base + '_sa')` / `ser(group, base + '_nsa')` works identically for all six of those
groups. `pib_taxas` is deliberately NOT part of this convention (see below) — it's read through a
separate helper, `officialRate()`, not `ser(group, base + '_sa'/'_nsa')`.

All growth-rate arithmetic (YoY, QoQ/MoM) for `pim`/`pmc`/`pms`/`ibcbr` happens in `report.html`'s JS
from the raw index levels, not in Python — same division of labor as `inflation/`'s `computeYoY`, just
simpler here: these are IBGE chain-linked volume indices, so growth is a plain ratio
(`value[t]/value[t-n] - 1`), not a chained-percentage sum like IPCA's `contribuicao`. `growthN(dates,
values, n)` is the one shared function behind both `seriesYoY()` (n = `PERIODS_PER_YEAR[group]`, 4 for
`pib`, 12 for the rest) and `seriesPeriodSA()` (n = 1). **The `pib` group specifically no longer uses
this ratio approach for its own tab** (see "PIB tab methodology") — `seriesYoY`/`seriesPeriodSA` on
`pib` are still used by the Visão Geral tab's cross-indicator comparison, which is why they're still
here and not deleted.

**SA/NSA convention, matching how IBGE/BCB present their own releases**: year-over-year comparisons
(`seriesYoY`) always read the **NSA** series (seasonal effects cancel naturally over 4 quarters / 12
months); period-over-period comparisons (`seriesPeriodSA`, i.e. QoQ for PIB, MoM for everything else)
always read the **SA** series (removing the seasonal effect is the entire point of a period-over-period
reading). Every KPI card and chart title says explicitly which one it's showing. The official
`atv_pib_taxas` rates follow the exact same convention by construction — see below.

## PIB tab methodology (2026-08, per explicit user guidelines)

Four requirements, all now implemented on the PIB tab specifically:

1. **Growth T/T (dessazonalizado)** and **2. Growth Y/Y (sem ajuste de sazonalidade)** — now read
   directly from `atv_pib_taxas` (`officialRate(base, 'qoq'|'yoy')`) instead of being computed as a
   ratio on `atv_pib`'s volume index. This is the IBGE's own published rate (Agregado 5932), not an
   approximation — removes any question of whether a simple ratio on a chain-linked index exactly
   matches what IBGE prints (in practice it's very close, e.g. our old ratio-based YoY for 2026 T1 was
   1.84% vs. the official 1.8%, a rounding-level gap — but "very close" isn't "the actual published
   number," and now it's the actual published number).
3. **Growth decomposition, T/T and Y/Y** — a full contribution-to-growth section, both by ótica da
   oferta (Agropecuária/Indústria/Serviços) and ótica da demanda (Consumo das Famílias/Governo, FBCF,
   Exportações, Importações), for both the QoQ and YoY windows (4 stacked-bar charts total). Method
   researched from IBGE's own Contas Nacionais Trimestrais methodology, which BCB and IPEA both
   replicate in their own conjuntura commentary — same as the BEA's "contribution to percent change in
   real GDP": for each category, `contribuição = (valor_encadeado[t] − valor_encadeado[t−n]) /
   valor_encadeado_PIB[t−n] × 100`, using `atv_pib_encadeado` (chain values in R$ milhões a preços de
   1995 — IBGE Agregados 6612/6613) rather than the volume index, because monetary values are additive
   across categories near the reference year while an index with a category-specific arbitrary base
   (100 in 1995) is not. `n=1` on the SA series for T/T, `n=4` on the NSA series for interanual.
   Importações get `sign: -1` (rising imports subtract from GDP). Each chart's stacked bars are closed
   out with an explicit residual bar (see Gotchas for what it captures) so the bars always sum exactly
   to the official rate, which is overlaid as a black line+diamond-marker series for visual
   verification — this is deliberately the same "contribution bars + total-growth line" presentation
   BCB/IPEA charts use, not just a stylistic choice.
4. **Accumulated 12m growth** — for a quarterly series, the equivalent concept is "acumulado em 4
   trimestres" (sum of the last 4 quarters vs. the prior 4), which IBGE publishes directly as its own
   rate (`acum_4t`) in the same Agregado 5932 — added as both a 3rd KPI card and its own trend chart
   (`chart-pib-acum4t`), not just a single number.

`atv_pib_taxas` also carries a 4th official rate, `acum_ano` ("acumulada ao longo do ano," i.e.
year-to-date vs. the same year-to-date last year) — fetched and stored since it was essentially free
alongside the other three, but not surfaced anywhere in the report yet (not part of the user's stated
requirements). Available in `D.pib_taxas` under `<base>__acum_ano` if ever needed.

**Verified against real data before shipping** (see last Gotcha for the full verification history):
the implied QoQ/YoY ratio from `atv_pib_encadeado`'s chain values matches the official
`atv_pib_taxas` rate to the penny (e.g. 1.1% QoQ, 1.84%→1.8% YoY for 2026 T1 — the tiny YoY gap is
`atv_pib_taxas`'s own 1-decimal rounding, not a bug), and re-running `computeContribution()` directly
against the real generated payload confirmed every decomposition chart's contributions + residual sum
back to the official total to within ±0.01pp (individual-component display rounding, not a
reconciliation failure) across the last several quarters, for all 4 chart variants (oferta/demanda ×
T/T/interanual).

## Report structure (`report.html`)

Six tabs, lazy-rendered on first activation (`tabRendered` flag, same pattern as `inflation/`'s
`renderNucleosTab`/`renderHeatmap` — Plotly needs a visible, non-zero-width div, so charts on tabs that
have never been opened aren't rendered until the user clicks that tab):

- **Visão Geral** — a 5-card KPI grid (PIB, IBC-Br, PIM, Varejo Ampliado, Serviços — each YoY/NSA as the
  headline number, period-SA change in the subtext), a mixed-frequency YoY comparison chart across all
  five indicators, and a "Nível de Atividade" chart rebasing PIB-SA and IBC-Br-SA to 100 at each one's
  own first observation, side by side — a visual check that the BCB's monthly proxy actually tracks the
  quarterly PIB it's meant to approximate.
- **PIB** — a 3-card KPI grid (QoQ SA, YoY NSA, acumulado-4T NSA, all official rates), an
  acumulado-4T trend chart, supply side (agropecuária/indústria/serviços + headline) and demand side
  (consumo das famílias/governo, FBCF, exportação, importação + headline) YoY(NSA) line charts, the
  standard "PIB var. trimestral dessazonalizada" bar chart, and a growth-decomposition section with 4
  contribution-to-growth stacked-bar charts (oferta × demanda, T/T × interanual) — see "PIB tab
  methodology" above for what's different here vs. the other five tabs.
- **Produção Industrial** — indústria geral/extrativa/transformação YoY(NSA), plus a headline MoM(SA) bar.
- **Comércio** — restrito vs. ampliado YoY(NSA) line chart, a ranking bar of the 12 PMC segments by
  latest YoY(NSA) reading (excludes `hipermercados_supermercados`, a redundant subset already counted
  inside `hiper_super_alim_bebidas_fumo` — see Gotchas), and a headline (ampliado) MoM(SA) bar.
- **Serviços** — a fixed 6-line YoY(NSA) chart (total + the 5 top-level PMS groups), a ranking bar of 20
  leaf-level PMS subsegments by latest YoY(NSA) reading, and a headline MoM(SA) bar.
- **IBC-Br** — total + 4 components (agropecuária/indústria/serviços/ex-agropecuária) YoY(NSA), plus a
  headline MoM(SA) bar.

The two "Ranking por Segmento/Subsegmento" horizontal bar charts (Comércio/Serviços tabs) are
deliberately excluded from the pan/zoom/`_bindYAutofit` treatment every other chart gets — same
precedent as `inflation/report.html`'s `chart-waterfall`: a category axis, not a time axis, so
TradingView-style navigation doesn't apply.

## Data map

| Report section | Table | Categories charted |
|---|---|---|
| PIB (rates/lines) | `atv_pib_taxas` | Oferta: `agropecuaria`/`industria`/`servicos`/`pib_pm`. Demanda: `consumo_familias`/`consumo_adm_publica`/`fbcf`/`exportacao`/`importacao`/`pib_pm`. All via the `yoy`/`qoq`/`acum_4t` indicadores |
| PIB (decomposição) | `atv_pib_encadeado` | Same categories as above, chain values (R$ mi a preços de 1995) — used only to compute p.p. contributions, never charted as levels |
| Produção Industrial | `atv_pim` | `industria_geral`/`ind_extrativas`/`ind_transformacao` |
| Comércio | `atv_pmc` | Totais: `comercio_ampliado_total`/`comercio_restrito_total`. Ranking: 12 segments (see Gotchas for the 2 excluded) |
| Serviços | `atv_pms` | Grupos: `servicos_total`/`servicos_familias`/`informacao_comunicacao`/`prof_adm_complementares`/`transportes_correio`/`outros_servicos`. Ranking: 20 leaf-level subsegments |
| IBC-Br | `atv_ibcbr` | `ibcbr`/`ibcbr_agropecuaria`/`ibcbr_industria`/`ibcbr_servicos`/`ibcbr_ex_agropecuaria` (`ibcbr_impostos` loaded but not charted — see Gotchas) |

`atv_pib` (the volume-index table, `D.pib`) is still loaded — the PIB tab itself no longer reads it
(fully switched to `atv_pib_taxas`/`atv_pib_encadeado`), but Visão Geral's cross-indicator YoY
comparison and level-rebasing charts still use it via the generic `seriesYoY`/`seriesPeriodSA`/
`rebaseTo100` path shared with `pim`/`pmc`/`pms`/`ibcbr`.

Full table schemas (IBGE aggregate/variable IDs, SGS codes, PK patterns) are in
[`domain/db/CLAUDE.md`](../../domain/db/CLAUDE.md) and each script's own docstring
(`domain/db/brasil/ibge/atv_pib.py` etc.) — not duplicated here.

## Gotchas

- **The decomposition residual bar is doing real, expected work, not just plugging a rounding gap** —
  measured directly against real data (2026-08): for the QoQ/SA decomposition, the residual is small
  (≤0.2pp in the quarters checked); for the interanual/NSA decomposition it can be meaningfully larger
  (e.g. −0.37pp for demanda at 2026 T1). Two genuinely different things get folded into one residual
  bar, and which one dominates depends on the chart:
  1. **Missing categories the IBGE classification itself doesn't separate here.** `atv_pib_encadeado`'s
     SA table (Agregado 6613) has no `impostos_liquidos_sa` at all (IBGE doesn't publish a
     seasonally-adjusted taxes-net-of-subsidies series under this classification) — so on the **oferta**
     side, `impostos_liquidos`'s contribution is never separated out, in *either* the T/T or interanual
     chart (kept symmetric on purpose, even though the NSA table does have the category, so both charts'
     residual is labeled "Impostos e Discrepância"). On the **demanda** side, there is no "Variação de
     Estoques" (inventory change) category anywhere in classificação 11255 at all — it's a real,
     structural gap in this SIDRA table, not something `atv_pib_encadeado.py` failed to fetch — so
     inventory swings are permanently inseparable from statistical discrepancy in the demanda-side
     residual ("Var. Estoques e Discrepância").
  2. **Chain-link non-additivity.** `atv_pib_encadeado`'s R$-million values are "a preços de 1995" —
     additive by construction only exactly at that reference year, and increasingly approximate the
     further a quarter is from 1995 (30 years, as of 2026) — this is the textbook chain-volume-measure
     caveat, and IBGE's own methodology note acknowledges it directly (it's *why* the values-at-fixed-
     year series is offered specifically for near-term contribution math, not as the headline PIB
     measure — that's `atv_pib`'s chain-linked index). Measured directly: agropecuária + indústria +
     serviços (NSA, 2026 T1) summed to 297,452 vs. `valor_adicionado`'s own published 292,918 — a ~1.5%
     gap, larger than plain rounding, plausibly worsened by agro's large NSA seasonal swings interacting
     with 30-year-old relative-price weights. This is folded into the same residual bar as (1) above —
     the two are not separated in the chart because the DB doesn't let us distinguish them; documenting
     both here is the only way to know which one to blame if a residual ever looks unexpectedly large.
- **`atv_pib_taxas.qoq` (agregado 5932, variável 6564) has no value at all for the very first quarter
  in the DB (1996 T1)** — there's no T-1 to compare against. Same expected `NULL`-at-the-start pattern
  as any lagged transform; `officialRate()`/`lastValid()` handle it the same way `growthN()` already
  does elsewhere (skip nulls, never crash).
- **PMC's ranking bar deliberately omits `hipermercados_supermercados`** (a subset already counted
  inside `hiper_super_alim_bebidas_fumo`) — the other 12 PMC categories are all mutually exclusive
  leaves, so this is the one PMC exception. **PMS's ranking bar omits every rollup at every level**:
  `servicos_total` (grand total) and the 5 top-level groups (`servicos_familias`,
  `informacao_comunicacao`, `prof_adm_complementares`, `transportes_correio`, `outros_servicos` — already
  the fixed lines in the YoY chart above it) plus the 3 mid-level rollups one step below those
  (`alojamento_alimentacao`, `tic`, `transporte_terrestre`) — keeping only the 20 true leaf categories.
  Including a rollup alongside its own children in the same ranking would double-count the same
  movement under two different bars. `PMC_RANKING_LABELS`/`PMS_RANKING_LABELS` in `report.html` are the
  actual sets used; check those objects directly rather than assuming every DB category appears
  somewhere in the report.
- **`atv_ibcbr.ibcbr_impostos` is loaded into `REPORT_DATA` (nothing filters it out in
  `generate_report.py`) but never charted** — BCB's own IBC-Br releases don't emphasize this component
  either (it exists mainly so `ibcbr_ex_agropecuaria` + `ibcbr_agropecuaria` + `ibcbr_impostos` ≈
  `ibcbr` reconciles), and it isn't intuitive on its own without that reconciliation framing. Could be
  added as a 6th line to the IBC-Br chart if ever needed — the data is already in the payload.
- **`atv_pib` only goes back to 2016** (IBGE 1620/1621's own start — see `domain/db/CLAUDE.md`), much
  shorter than `atv_ibcbr`/`atv_pim` (2002-2003). The "Nível de Atividade" chart's `rebaseTo100()` starts
  each series at its own first observation independently for exactly this reason — a shared PIB-anchored
  base date would have cut off most of IBC-Br's longer history.
- **`atv_pmc`/`atv_pms` only go back to 2023** (their IBGE aggregates' own start) — by far the shortest
  history of the five tables here. The `10a`/`5a` rangeselector buttons on their charts will show "all
  available data" rather than a true 5/10-year window until more history accumulates.
- **Verification history**: first built and checked with no MySQL access at all (`_series_dict()`
  key-naming logic against a synthetic DataFrame; the full extracted `<script>` block, with the real
  `y_autofit.js` spliced in matching what `render_report()` actually produces, executed under Node
  against a stubbed `document`/`Plotly` — caught one real bug, a missing `.on()` stub, before this note
  was written). **Since then, `generate_report.py` has been run against the live database twice**: the
  first pass (5 tables, 6 tabs, no PIB-specific methodology yet — 44 PIB series/5,324 obs, 6 PIM/1,764,
  32 PMC/10,072, 58 PMS/10,730, 12 IBC-Br/3,372, matching each table's expected category count exactly,
  e.g. PMS's 29 categories × 2 SA/NSA = 58) and the second pass adding `atv_pib_encadeado`/
  `atv_pib_taxas` for the PIB-tab rework (44 more `pib_enc` series, 88 `pib_taxas` series = 22
  categories × 4 indicadores). Both times the same Node-stub harness was re-run against the *real*
  generated `<script>` block (not synthetic data) — 15 charts across 6 tabs the first time, 20 charts
  the second (5 new PIB charts) — all executed with no exceptions and produced sane, correctly dated
  KPI values (e.g. PIB 2026 T1, official rates: +1.10% T/T dessaz. / +1.80% interanual / +2.00% acum.
  4T). The second pass also called `computeContribution()` directly against the real payload and
  confirmed every decomposition chart's contributions + residual reconcile to the official rate (see
  "PIB tab methodology" above). **What none of this covers: actual visual rendering in a browser** —
  layout, Plotly's real chart drawing, and hands-on pan/zoom/rangeselector interaction have still not
  been eyeballed (no browser available in this sandbox; the Node harness only proves the JS logic runs
  clean against real data, not that it looks right).

## Pending

- **User guidelines for the other five tabs (Produção Industrial, Comércio, Serviços, IBC-Br, Visão
  Geral) have not been given yet** — the user explicitly said they'd write those separately after the
  PIB pass. Don't assume the PIB tab's official-rates-plus-decomposition treatment should be copied to
  the others until asked; wait for those guidelines.
- Open `reports/economic_activity_latest.html` in an actual browser and confirm the charts render and
  the pan/zoom/rangeselector/tab-switching interactions feel right — the one verification step the
  sandbox environment can't do (see last Gotcha above).
- Consider adding `ibcbr_impostos` as an explicit reconciliation note or 6th line once the IBC-Br chart
  has been seen in practice (see Gotchas).
- `atv_pib_taxas.acum_ano` is fetched/stored but not surfaced in the report (see "PIB tab
  methodology") — add if ever requested.
- No `agent_data.py`-style snapshot function yet (unlike `exchange_rate/`'s `get_fx_snapshot()`) — add
  one if a future subagent needs quick activity-data access (latest value + deltas) rather than the full
  report payload.
