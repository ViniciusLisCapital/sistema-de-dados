# analytics/brasil/economic_activity/ — Panorama de Atividade Econômica

Self-contained HTML report on Brazilian real-activity data: GDP (PIB), industrial production (PIM),
retail (PMC), services (PMS) and the BCB's monthly GDP proxy (IBC-Br) — all from `macro_brasil`, all
already kept current by `jobs/update_db.py`. Same `/*REPORT_DATA*/` marker-substitution pattern as the
other analytics reports, built directly on [`analytics/report_structure/`](../../report_structure/CLAUDE.md)
(no Jinja2, no build step, no migration needed — unlike `inflation/`/`exchange_rate/`).

Chart interaction (pan/zoom, quick-range buttons, period-selector dropdown, `_bindYAutofit`) follows the
repo-wide convention — see [`.claude/rules/lis-dashboards.md`](../../../.claude/rules/lis-dashboards.md),
not repeated here.

## Generate

```powershell
uv run python -c "from analytics.brasil.economic_activity.generate_report import run; run()"
# Output: reports/Economic Activity.html
```

No manual data-refresh step needed first — every source table is already in `jobs/update_db.py`'s
routine run.

## Architecture

`generate_report.py` reads MySQL tables via `MySQLDataRequester`, reshapes each into a flat
`{key: {dates, values}}` dict, and hands the result to `report_structure.builder.render_report()`. Seven
`REPORT_DATA` groups: `pib`, `pim`, `pmc`, `pms`, `ibcbr`, `pib_val`, `pib_taxas`.

- **Key-naming convention** (`pib`/`pim`/`pmc`/`pms`): every series key ends in `_sa`/`_nsa` regardless of
  which DB column carries that flag — `_load_suffixed()` appends the suffix at read time. `atv_ibcbr`
  already bakes it into `name`; `_load_flat()` just groups as-is. `pib_val`/`pib_taxas` are NSA-only/
  official-rate tables respectively and don't follow this convention (read via `annualWeight()`/
  `officialRate()`, not `ser(group, base + '_sa')`).
- **`pim` merges two IBGE aggregates into one group**: `atv_pim` (seções/atividades, Agregado 8888) and
  `atv_pim_uso` (categoria de uso — bens de capital/intermediários/consumo, Agregado 8887), concatenated
  in `_load_pim()` before the series dict is built. Their category names never collide, so `report.html`'s
  JS never needs to know which table a base came from.
- **All growth arithmetic (YoY, QoQ/MoM, Acum) happens in JS**, not Python, from raw index levels —
  `growthN(dates, values, n)` backs both `seriesYoY()` and `seriesPeriodSA()`; `seriesAcum12m()` is the
  monthly analogue of PIB's official `acum_4t`. **Exception: the PIB tab reads official rates directly**
  from `atv_pib_taxas` (`officialRate()`) instead of computing a ratio — see below.
- **SA/NSA convention** (matches how IBGE/BCB present their own releases): year-over-year always reads
  the NSA series; period-over-period (QoQ/MoM) always reads the SA series.

## PIB tab methodology

`atv_pib_taxas` provides IBGE's own *officially published* rates (`qoq`, `yoy`, `acum_4t`, `acum_ano` —
the last one fetched but not yet surfaced anywhere), used instead of a ratio computed from `atv_pib`'s
volume index. The growth-decomposition (contribution-to-growth) section implements Nota Técnica BCB
nº 46's **"método ad hoc"**:

```
contribuição_i(t) = peso_i(ano civil anterior a t) × variação_i(t, indicador)
peso_i(ano)        = valor_a_preços_correntes_i(ano) / valor_a_preços_correntes_PIB(ano)
```

`peso_i` comes from `atv_pib_valores_correntes` (nominal, NSA-only — annual weight, never charted
directly). Two things to *not* mistake for bugs if this section is ever touched again:

- **`impostos_liquidos` has no published QoQ rate at all** (`atv_pib_taxas`'s `qoq`, variável 6564, is
  `NULL` for every row of this category, confirmed empirically) — so the QoQ oferta chart's residual is
  labeled "Impostos e Discrepância" while the YoY chart's is just "Discrepância" (YoY *does* have a rate).
- **The demanda-side residual is large and volatile by construction, not a bug** — "Variação de
  Estoques" has no published real/volume growth rate anywhere in IBGE's system (only a nominal value),
  so its effect is structurally inseparable from the residual; Brazil's agro-harvest → inventory-build →
  later-export pattern makes this genuinely large and seasonal. Don't "fix" this by hunting for a
  smaller residual — NT-46's method reconciles to the official rate by construction regardless; what
  differs between methods is only how much gets explained by name vs. left in the plug.

NT-46's more precise "método proposto" and IPEA's demand-side domestic/imported-content split are both
citable alternatives, not implemented (see Pending).

## Tabs

Six tabs — PIB, Produção Industrial, Comércio, Serviços, IBC-Br, Apêndice — lazy-rendered on first
activation. Apêndice holds every long methodology note as a `<details>/<summary>` accordion, keeping the
data tabs uncluttered.

- **PIB** — 4-card KPI grid (QoQ/YoY/Acum-4T official rates + carrego estatístico); Gráfico 1
  (YoY↔Acum-4T toggle, up to 21 selectable oferta/demanda components) and Gráfico 2 (QoQ); a
  growth-decomposition section (4 stacked-bar charts, oferta×demanda × T/T×interanual); a momentum
  heatmap (2 panels, rolling 20-quarter/5y z-score). The only tab with growth-decomposition — the other
  four lack the official-rate + nominal-weight tables it needs (new IBGE data-collection work, not just
  report changes — see Pending).
- **Produção Industrial** — 4-card KPI grid (MoM/YoY/Acum-12m + carrego trimestral); Gráfico 1/2 across
  **30 selectable items** in 3 groups (Setores, Atividades da Transformação — 24 CNAE divisions —,
  Categorias de Uso); a Momentum × Nível scatter (25 points: 24 CNAE divisions + Indústrias Extrativas,
  single-colored — no cyclical/non-cyclical classification; one was built and then **removed at the
  user's own request**, "vou olhar com calma depois" — don't silently re-add it); a heatmap with
  click-to-expand rows (`ind_transformacao` and `bens_consumo` both expand two levels deep).
- **Comércio** — ampliado 4-card KPI grid + restrito 2-card row; Gráfico 1/2 (13 items: 12 segments +
  restrito); a Momentum × Nível scatter (9 of 12 segments — 3 drop out for lack of a recent SA series,
  see Gotchas — colored by a credit/income-sensitivity split **this report extrapolated from a public
  Itaú principle, not a literal Itaú list**, documented as such in the Apêndice); a heatmap over the raw
  IBGE hierarchy (including 2 rollup nodes the scatter excludes).
- **Serviços** — 4-card KPI grid; Gráfico 1/2 (25 items: 5 groups + 20 leaves); a Momentum × Nível
  scatter (11 of 20 segments — 9 drop out for lack of *any* SA series, see Gotchas — single-colored); a
  heatmap over the real 4-level hierarchy (3 mid-level rollups excluded from the scatter/Gráficos).
- **IBC-Br** — 4-card KPI grid; Gráfico 1/2 (5 components, including `ibcbr_impostos`, unchecked by
  default); a Momentum × Nível scatter (5 points, no exclusions — added for cross-tab parity, not an
  explicit request, see Pending); a flat 5-row heatmap.

`PMC_RANKING_LABELS`/`PMS_RANKING_LABELS` in `report.html` kept their original names from when they fed
a ranking bar chart — both now feed the scatter (`renderQuadrant()`) instead; `renderRanking()` itself
has been deleted (no callers left).

## Data map

| Tab | Table(s) | Categories |
|---|---|---|
| PIB | `atv_pib_taxas`, `atv_pib_valores_correntes` | `PIB_RATE_CATS` (16 oferta + 5 demanda) via `officialRate()`; decomposition weights from `PIB_OFERTA_BASES`/`PIB_DEMANDA_BASES` |
| Produção Industrial | `atv_pim` + `atv_pim_uso` | `PIM_CATS`/`PIM_TREE` — seções/atividades (24 CNAE `transf_*`) + categoria de uso (`bens_*`) merged |
| Comércio | `atv_pmc` | `PMC_CATS` (12 leaf segments) + `comercio_restrito_total`; `PMC_TREE` includes 2 rollup nodes the flat list excludes |
| Serviços | `atv_pms` | `PMS_CATS`/`PMS_TREE` — 5 groups + 20 leaves + 3 mid-level rollups (tree only) |
| IBC-Br | `atv_ibcbr` | `IBCBR_CATS` — 5 components, all reachable |

## Gotchas

- **Data gaps are real IBGE-source gaps, not ingestion bugs** — confirmed directly against the DB/API
  each time, not assumed: 3 of PMC's 12 segments (Móveis, Eletrodomésticos, Atacado Alim./Beb./Fumo) and
  9 of PMS's 20 leaf segments (Alojamento, Alimentação, and 7 others) have no seasonally-adjusted series
  at all — the connectors fetch SA/NSA identically for every category, so a script bug would fail
  uniformly, not selectively. `renderQuadrant()`'s scatter correctly drops these points and names them in
  its own caption; don't try to backfill or approximate around the gap.
- **`atv_pib` only goes back to 2016; `atv_pmc`/`atv_pms` only to 2023** — their own IBGE aggregates'
  start, not a project limitation. The 5a/10a quick-range buttons show "all available data" until more
  history accumulates.
- **Heatmap click-to-expand needs two listeners**: `plotly_click` (cell clicks only) *and* a DOM-level
  `click` listener delegating via `.closest('.ytick')` (axis-label-text clicks — what a user actually
  clicks — never fire `plotly_click` in real Plotly). Both resolve through the same per-div
  `_tabHeatmapCtx` cache (rebuilt every render, never captured by closure). `analytics/brasil/exchange_rate/
  report.html`'s BOP heatmap shares this same architecture and almost certainly has the same gap —
  never confirmed live there, check before trusting its click-to-expand rows.
- **No browser has visually confirmed any interaction in this report** — verification so far is a jsdom
  harness (ad hoc in scratchpad, not a repo dependency) evaluating the real generated `<script>` against
  real DB output: tabs activate, charts render with the right trace/point counts, toggles/checkboxes
  re-render, captions populate. Layout, real Plotly rendering, and pan/zoom feel are unconfirmed.

## Pending

- Open `reports/Economic Activity.html` in a real browser — the one verification step the sandbox
  can't do, across every tab/interaction in this file.
- Growth-decomposition not implemented for PIM/PMC/PMS/IBC-Br — needs an official-rates table and a
  nominal-weight table neither exists for these four series; would require new IBGE connector/table work.
- NT-46's "método proposto" (more precise than the ad hoc decomposition) not implemented — its OCR-
  extracted equations were too garbled to transcribe with confidence; revisit only with a cleaner copy
  of the PDF or a from-scratch derivation.
- IPEA's demand-side domestic/imported-content split not implemented — needs IO/TRU table data this
  project doesn't have.
- `atv_pib_taxas.acum_ano` fetched/stored but not surfaced anywhere — add if requested.
- IBC-Br's Momentum × Nível scatter was added for cross-tab parity, not an explicit request, and only has
  5 points — confirm with the user whether it's useful or should come back out.
- `analytics/brasil/exchange_rate/report.html`'s BOP heatmap likely needs the same click-listener backport (see
  Gotchas) — only touch if/when that report comes up specifically.
- No `agent_data.py`-style snapshot function yet (unlike `exchange_rate/`'s `get_fx_snapshot()`) — add if
  a future subagent needs quick latest-value/delta access instead of the full report payload.
