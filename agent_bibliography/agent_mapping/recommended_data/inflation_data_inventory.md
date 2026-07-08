# Inflation Data Inventory

**Purpose:** maps the data the inflation agent needs to what already exists in the LIS database vs. what's missing — following the same pattern as `exchange_rate_data_inventory.md` and `monetary_policy_data_inventory.md`. Built after the literature pass (`inflation_bibliography_candidates.md`), per the agreed order.

**Two-tier structure, per the architecture already established for monetary policy:** unlike monetary policy (mostly a *consumer* of other agents' outputs), the inflation agent is closer to a **net producer** — `macro_brasil.inflacao` and `macro_brasil.expectativas` already give it an unusually rich owned base, and monetary policy's own inventory already lists "inflation gap/nowcast," "core decomposition and diffusion," and "anchoring signal" as things it expects to receive *from* this agent (`monetary_policy_data_inventory.md`, Tier 2). So this file still splits the same way for consistency, but the balance is inverted:

- **Tier 1 — Owned data:** the price indices themselves, their disaggregation, and market-based inflation expectations. Mostly already buildable, several gaps closeable without depending on any other agent.
- **Tier 2 — Consumed data:** structured hand-offs the inflation agent needs *from* other agents (a wage/labor-cost signal, a spot FX series for pass-through, a commodity price for cost-push) — placeholders until those agents are scoped, mirroring the convention set in `monetary_policy_data_inventory.md`.

---

## Tier 1 — Owned data

### 1. Headline and disaggregated IPCA

| What we have | Table | Series | Note |
|---|---|---|---|
| Headline (IPCA, IPCA-15) and diffusion index | `macro_brasil.inflacao` | `IPCA`, `IPCA15`, `IPCA_indice_difusao` | SGS 433 / 7478 / 21379 |
| Administered vs. free (market) prices | `macro_brasil.inflacao` | `IPCA_administrado`, `IPCA_livres` | direct input for cluster 3 (cost-push/pass-through) and cluster 7 (fiscal dominance via administered-price policy) |
| By type of good/service (industrial, food, services, durables/semi/non-durables) | `macro_brasil.inflacao` | `IPCA_industriais`, `IPCA_alimentacao`, `IPCA_servicos`, `IPCA_bens_*` | |
| By COICOP-style expenditure group (9 groups: food, housing, apparel, transport, communication, health, personal expenses, education, home goods) | `macro_brasil.inflacao` | `IPCA_grupo_*` | |
| Core measures (8 methodologies: trimmed means, EX0/EX01/EX02/EX03, DP, P55, EXFE) | `macro_brasil.inflacao` | `IPCA_nucleo_*` | directly operationalizes cluster 6 (`#inflation_measurement_and_core_measures`) — EXFE and the trimmed-means series are the two BCB currently emphasizes in its own communication |

Script: `domain/db/brasil/bcb/inflacao.py`. Coverage per `CLAUDE.md`: 1980 → today for headline, though the core-measure and component series individually start later (each SGS code has its own inception date — not verified series-by-series here).

**This is the single richest owned dataset across any LIS agent's inventory so far** — 28 series spanning headline, administered/free split, sectoral/expenditure breakdown, and 8 distinct core methodologies, with no equivalent depth yet in the exchange rate or monetary policy inventories.

**Gaps — verified against Banco Central do Brasil, Nota Técnica nº 57 (December 2025), "Núcleos de inflação e outras séries analíticas derivadas do IPCA: metodologia consolidada"** (the current, authoritative SGS code reference — this note should be added to the bibliography's cluster 6 alongside da Gama Machado 2024, WP 602, which it postdates and supersedes for code-level detail):
- No confirmed start date per individual series (the core measures in particular were introduced at different points — the consolidated methodology now backdates most series to Jan/1991, except MS from Dec/1991 and DP from Jan/1995) — low-effort fix now that NT 57 documents the uniform start dates.
- **Missing "tradable vs. non-tradable" split:** `Comercializáveis` (SGS 4447) and `Não comercializáveis` (SGS 4448) are current, actively-maintained BCB series not currently ingested — a different cut than the administered/free split already owned, useful for cost-push/pass-through analysis (bibliography cluster 3) since tradables are the segment most exposed to FX pass-through and commodity prices.
- **Missing "Núcleo MA" under its correct, current code:** the local script's `IPCA_nucleo_medias_aparadas` (SGS 4466) is actually **Núcleo MS** (trimmed mean *with* smoothing) per NT 57's Table 11, not the generic "médias aparadas" the column name implies — the unsmoothed trimmed mean (**Núcleo MA**) is a distinct series now published under SGS 11426 and is not ingested at all. Recommend both fixing the misleading column name and adding the missing MA series.
- **Missing EX3 Serviços (SGS 29683) and EX3 Industriais (SGS 29684)** — brand new as of this note, previously analyzed in Relatório de Política Monetária boxes (RI set/2016 for services, RI jun/2018 for industrials) but not available in SGS until now. These are BCB's own "underlying services" and "underlying industrial goods" indicators (the services/goods components of Núcleo EX3) — the closest official BCB analogue to the "supercore services" concept used in the U.S. debate (cluster 1's Hooper-Mishkin-Sufi discussion) and a direct, higher-priority addition given the recency of their publication.

### 2. IPCA sub-item detail (diffusion/breadth decomposition) — ⚠️ WIP, not production

| What we have | Status |
|---|---|
| `domain/db/brasil/ibge/subcomponents.py` | Work-in-progress script targeting IBGE aggregado 7060 (hundreds of IPCA sub-items via classification 315) — already flagged as a pending item in `CLAUDE.md` ("Média prioridade") |

**This is conceptually distinct from `IPCA_indice_difusao` in §1** — the SGS series is BCB's own single summary diffusion statistic (% of items rising), while aggregado 7060 is the underlying item-level granularity needed to *compute your own* breadth/diffusion measures, replicate a Coibion-Gorodnichenko-style decomposition, or identify which specific sub-items are driving a given month's surprise.

**Blockers to production:** script still uses the old `ibge_get(url, start, end, freq)` connector rather than the current `connectors/ibge.py` v3 client; no schema defined yet; classification-code list (`315[...]`) hardcoded as a raw URL rather than passed as a parameter.

**Impact if left unbuilt:** the agent can say "diffusion is rising" (from the one SGS series) but not "diffusion is rising, driven specifically by services ex-education" — a materially weaker read during exactly the kind of episode (broad-based vs. narrow/idiosyncratic price pressure) the diffusion literature is meant to distinguish.

### 2a. Labor-intensive services inflation ("serviços intensivos em trabalho") — ⚠️ GAP, bespoke methodology, not an SGS series

BCB's Monetary Policy Report has, in recent years, tracked services inflation reweighted by labor intensity as a direct gauge of domestic demand/labor-market pressure on prices — conceptually the Brazilian analogue to the "supercore services" framing that became prominent in the 2022-23 U.S. debate. **This is not published as a standalone SGS series** — confirmed by checking BCB's own Nota Técnica nº 57 (Dec 2025), which consolidates every IPCA-derived analytical series BCB currently publishes via SGS and does not include it. Its methodology instead appears only in two Relatório de Política Monetária boxes: **"Inflação de serviços reponderada por fatores de produção"** and **"Dinâmica recente da inflação de serviços,"** both June 2024.

**Impact:** the agent cannot currently reproduce or track this metric at all — it would need to be built from scratch, by reweighting the item-level services components of the IPCA by their labor intensity (a production-factor classification, not a standard IBGE weight). This is a natural extension of, and blocked by the same prerequisite as, **§2 above**: it requires the same item-level detail (IBGE aggregado 7060) that `subcomponents.py` targets but hasn't reached production. Building §2 first would make this a realistic follow-on rather than a separate research project.

**Possible source for the labor-intensity classification itself:** not yet identified — would need to trace how the June 2024 RPM boxes define "labor-intensive" at the item level (likely IBGE's own value-added/production-factor tables, or a BCB-internal mapping); worth extracting directly from the two RPM boxes once prioritized.

### 2b. Full services-inflation sub-decomposition family (June 2024 RPM boxes) — ⚠️ DEFERRED, needs dedicated analytical work before any DB implementation

**Kept as its own box, separate from §2a, because this is materially bigger than "add one missing series."** Reading both June 2024 boxes in full ("Dinâmica Recente da Inflação de Serviços" and "Inflação de Serviços Reponderada por Fatores de Produção," *Relatório de Inflação*, Volume 26, Nº 2, June 2024, pp. 56-65) surfaces **12 distinct series across two unrelated methodologies**, none of them in SGS (confirmed against NT 57) and none reducible to a simple ingestion task — each requires its own sourcing and, in one case, an entirely new data source not used anywhere else in the LIS pipeline. Recorded here in full so the scope is visible before anyone starts implementation, rather than discovering the size of the task mid-build.

**Methodology 1 — simple exclusion/grouping cuts of IPCA services sub-items** (from "Dinâmica Recente da Inflação de Serviços"):
| Series | Definition | IPCA weight |
|---|---|---|
| Serviços ex-passagem aérea | services excluding the airfare sub-item (chosen for its volatility) | 34.6-34.8% |
| Serviços — MS / DP / P55 | the three general core-inflation methodologies (§1) applied to the services segment only, not the whole basket | n/a |
| Serviços ligados à ociosidade | sub-items classified as sensitive to economic slack | not stated |
| Serviços ligados à inércia | sub-items classified as inertia-sensitive | not stated |
| Serviços intensivos em trabalho | labor-intensive services — **not new to 2024**, originally defined in a *December 2013* RI box; the 2024 box re-analyzes it | 6.1% |
| Intensivos em trabalho ex-domésticos | the above, with domestic-worker sub-items stripped out — this specific cut *is* new to the 2024 box | 2.8% |

All six are also presented as 3-month seasonally-adjusted annualized rates (MM3M a.s.) alongside the standard 12-month change — a transformation `inflacao.py` doesn't compute for any series today (it stores raw index levels only), which is itself a prerequisite piece of work independent of sourcing the underlying series.

**Methodology 2 — production-factor reweighting via national accounts input-output data** (from "Inflação de Serviços Reponderada por Fatores de Produção," a genuinely new approach, not a refinement of Methodology 1): each IPCA services sub-item is mapped to an economic activity in IBGE's *Tabela de Recursos e Usos* (TRU — national accounts input-output tables), and reweighted by that activity's 2010-2019 average factor share of production. This produces five subindices that partition "Serviços ex-passagem aérea":

| Subindex | Factor | IPCA weight (May 2024) |
|---|---|---|
| Trabalho | labor | 14.6% |
| Capital | capital | 6.8% |
| CI-Alimentos | intermediate consumption, food inputs | 2.5% |
| CI-Bens | intermediate consumption, goods inputs | 2.4% |
| CI-Outros | intermediate consumption, other inputs | 8.6% |

**Why this needs dedicated analytical work, not just a new connector:**
- Both methodologies sit on top of the same item-level IPCA sub-item detail already blocked on §2 (`subcomponents.py`, IBGE aggregado 7060) — so neither is buildable until that WIP script reaches production.
- Methodology 1's groupings ("ligados à ociosidade," "ligados à inércia") are BCB-internal classifications of which IPCA sub-items belong to each bucket — this mapping isn't published as a downloadable table in either box (would need manual extraction from the box text/appendix, or a request to BCB).
- Methodology 2 requires an entirely new data source never touched elsewhere in this codebase — IBGE's TRU (national accounts input-output tables) — plus replicating BCB's own item-to-activity correspondence table (Anexo Tabela A2 in the box) and the 2010-2019 factor-share averaging step. This is a multi-week research/replication project on its own, not a data-pipeline addition.
- Given all of this, recommend treating §2b as a candidate for a **future, separate research pass** once §2 is in production — not something to schedule alongside the more mechanical gaps elsewhere in this inventory (EX3 Serviços/Industriais, IGP-M, IPP).

### 3. Inflation expectations (Focus survey)

| What we have | Table | Series | Note |
|---|---|---|---|
| IPCA 12m and 24m — mean, median, std. dev., min, max, number of respondents | `macro_brasil.expectativas` | `indicador = 'IPCA'`, `horizonte = '12m'/'24m'` | 2001 → today |
| IGP-M 12m — same fields | `macro_brasil.expectativas` | `indicador = 'IGP-M'`, `horizonte = '12m'` | |

Script: `domain/db/brasil/bcb/expectativas.py`. Same underlying table monetary policy's inventory documents for the Selic side — for inflation, the load-bearing columns are different: **`DesvioPadrao` and the respondent count are already captured**, which means the dispersion/anchoring measures central to cluster 2 (Gaglianone 2017, Bevilaqua-Mesquita-Minella 2007) are computable *today* without any new data work — this is a materially better position than monetary policy's own r*/neutral-rate gap.

**Gaps:**
- No 3-year or 5-year-ahead IPCA expectations (Focus does publish beyond 24m for some horizons) — would be useful for a longer-run anchoring read distinct from the 12m/24m already captured.
- No breakdown by respondent type (banks vs. independent consultancies vs. asset managers) — Focus microdata supports this segmentation but it isn't queried; would let the agent distinguish sell-side consensus from buy-side positioning views on inflation.
- No realized IGP-M series to compare the IGP-M expectation against (see §4) — currently the agent could track *forecast* IGP-M but not forecast-vs-actual error.

### 4. Wholesale/general price index (IGP-M, IGP-DI) — ⚠️ GAP

No realized IGP-M or IGP-DI series is stored anywhere in the database — only the Focus *expectation* for IGP-M (§3). This matters specifically for Brazil's indexation cluster (bibliography cluster 4/8): a meaningful share of rent contracts, some regulated tariffs, and a handful of financial contracts are still indexed to IGP-M rather than IPCA, so a gap between the two series is itself a live signal of relative price pressure (commodities/wholesale vs. retail) with direct pass-through implications for future IPCA-administered-price readings.

**Possible source:** FGV (IBRE) publishes IGP-M/IGP-DI directly — not a BCB SGS series, so this would need a new connector rather than reusing `connectors/bcb.py`. Not yet scoped.

### 5. Producer prices (IPP — Índice de Preços ao Produtor) — ⚠️ GAP

No producer/wholesale price index from IBGE is ingested. This is the standard upstream-pressure series in the cost-push cluster (bibliography cluster 3) — a rise in producer prices ahead of a rise in consumer prices is a classic early-warning read on pipeline inflation pressure that the agent cannot currently form, since it only has the CPI (IPCA) side of the pass-through chain.

**Possible source:** IBGE SIDRA aggregado for IPP (exact aggregado number not confirmed) — could reuse `connectors/ibge.py` v3 client once identified.

### 6. Wage and labor-cost data — usable today, but owned by another domain

| What we have | Table | Series | Note |
|---|---|---|---|
| Real and nominal average income, by formal/informal position and by economic sector | `macro_brasil.pnad` | `rend_*` (e.g. `rend_priv_excl_domestico_com_carteira`, `rend_media_nacional`) | |
| Real and nominal aggregate wage bill ("massa de rendimentos") | `macro_brasil.pnad` | `massa_real_habitual`, `massa_nominal_habitual` | directly usable for a wage-price-spiral read (bibliography cluster 8, Weber & Wasner) without waiting on a separate labor/activity agent |

Script: `domain/db/brasil/ibge/pnad.py`. This table is conceptually "owned" by a future activity/labor agent, but the specific wage-growth series are already sitting in the database today and don't require any new ingestion work for the inflation agent to start using them.

**Gap:** no unit labor cost measure (wage growth relative to productivity) — would need a productivity proxy (e.g. GDP/`gdp` table vs. hours worked from `pnad`) combined manually; nothing computes this today.

### 7. International comparison: Latin America and developed-market inflation (headline and core) — ⚠️ GAP, new category

No cross-country inflation series exists anywhere in the database today — headline or core, Latin America or developed markets — beyond the one ad hoc byproduct noted below. This is a real gap for reading Brazil's inflation *relative to peers*: is a given disinflation episode BCB-specific (credibility, Selic path) or part of a broader regional/global wave (global slack, commodity cycle, per bibliography cluster 1's Borio-Filardo argument)?

| What we have | Table | Series | Coverage |
|---|---|---|---|
| US CPI 12m, consumed inside the rate-differential calculation | `macro_analytics.diferenciais_juros` | `cpi_12m_us` | ~36m rolling (script's default window) |

This is the only existing cross-country inflation data point, and it's a byproduct of the FRED differentials script rather than a dedicated inflation table — limited to a ~36-month rolling window, same gap already flagged in the exchange rate and monetary policy inventories. See `CLAUDE.md`'s "US — expandir dados" pending item (no persistent `macro_us` schema yet).

**Possible source, no new connector needed:** FRED's OECD Main Economic Indicators dataset carries harmonized headline and core (ex food & energy) CPI, year-over-year, for essentially every relevant peer — reusable directly via the existing `connectors/fred.py` (`FredMultFrame`) client already used for `diferenciais_juros`. Suggested peer set:
- **Latin America:** Mexico, Chile, Colombia — matching the peer set already established in `macro_international.reer`, for direct cross-reference against the existing REER series; Peru and Argentina as secondary additions if headline/core CPI is confirmed available on FRED for both.
- **Developed markets:** US (upgrade from the current ~36m byproduct to full history), Euro Area, UK, Japan — the core DM peer set most relevant to the global "low-flation" and post-pandemic-surge narratives already in bibliography clusters 1 and 8.

**Where it should live:** `macro_international` alongside `reer` and `cot_fx`, not `macro_brasil` — this is fundamentally cross-country data, not a Brazil series, and reusing that schema keeps the LatAm peer set consistent with what the REER table already tracks.

---

## Tier 2 — Consumed data (placeholders, pending other agents)

### From a future activity/labor agent
- Output gap estimate (the standard demand-side input to any Phillips curve specification in bibliography cluster 1) — `macro_brasil.ibc_br`/`gdp` exist today but no potential-output/gap estimate is computed from them.
- Unemployment gap vs. a NAIRU-type estimate (same role as the output gap, labor-market version) — raw unemployment already in `pnad` (§6 above), but no natural-rate estimate exists.
- Already-partially-satisfied by §6 above (wage growth, wage bill) — flagged here only as a reminder that the *ownership* of `pnad` sits with a future activity/labor agent even though the specific series are usable now.

### From the exchange rate agent (substantially built, per `exchange_rate_data_inventory.md`)
- Spot BRL series (PTAX) — flagged as a high-priority gap in that agent's own inventory too; without it, this agent can't directly regress pass-through against the actual depreciation, only against REER (`macro_international.reer`, already available) or indirectly via `fluxo_cambial`/`balanco_pagamentos`.
- A REER over/undervaluation signal — same gap noted in `monetary_policy_data_inventory.md`; relevant here as a slower-moving pass-through input alongside spot moves.

### From a future fiscal agent
- Administered-price policy signal (are regulated tariffs — energy, fuel, public transport — being adjusted on schedule or politically delayed) — directly relevant given `IPCA_administrado` is already an owned series (§1) but the *policy driver* behind its moves is not.
- Fiscal dominance / sustainability risk signal — same placeholder already listed in `monetary_policy_data_inventory.md`; for this agent specifically it would inform how much weight to put on the FTPL-style price-level channel (bibliography cluster 7) versus the standard Phillips-curve channel (cluster 1) when accounting for a given inflation surprise.

### From a possible future global/markets agent (not yet scoped at all)
- Commodity price indices (oil, agricultural, metals) — the standard cost-push/imported-inflation input (bibliography cluster 3, Blanchard & Gali 2007) and a direct driver of Brazil's own terms-of-trade-linked food/energy inflation episodes (e.g. the 2021 drought/energy shock flagged as an open gap in bibliography cluster 8). Today the closest proxy in the database is the aggregate terms-of-trade index in `macro_brasil.termos_de_troca`, which is too coarse to isolate a specific commodity shock.
- Global Supply Chain Pressure Index or equivalent — the empirical counterpart to di Giovanni et al. (2022) in bibliography cluster 8; no domestic or global proxy exists in the database today.

---

## Gap summary (Tier 1 only — Tier 2 gaps are dependencies on unbuilt agents, not data gaps per se)

| Priority | Gap | Category |
|---|---|---|
| High | IPCA sub-item detail (IBGE 7060) stuck in WIP — needed for any real diffusion/breadth decomposition | §2 |
| High | EX3 Serviços / EX3 Industriais ("underlying services"/"underlying industrial goods") not ingested — newly available in SGS as of Dec 2025 | §1 |
| Medium | No realized IGP-M/IGP-DI series (only the Focus expectation exists) | §4 |
| Medium | No producer price index (IPP) — no upstream/pipeline-pressure read | §5 |
| Medium | No Latin America / developed-market headline+core CPI for cross-country comparison | §7 |
| Medium | Labor-intensive services inflation ("serviços intensivos em trabalho") has no data pipeline at all — bespoke RPM methodology, blocked on §2 | §2a |
| Low | Missing `Comercializáveis`/`Não comercializáveis` split, and the misnamed/missing Núcleo MA series (SGS 11426 vs. the currently-ingested MS under SGS 4466) | §1 |
| Low | No per-series inception-date confirmation for the 28 `inflacao` columns (largely resolved — NT 57 documents Jan/1991 start for most) | §1 |
| Low | No 3-5y Focus horizon or respondent-type segmentation for expectations | §3 |
| Low | No unit labor cost measure (wage growth vs. productivity) | §6 |
| Low | `cpi_12m_us` limited to ~36m rolling (same cross-agent gap as FX/monetary policy inventories) | §7 |
| **Deferred** | **Full 12-series services sub-decomposition family (two methodologies, one requiring new IBGE TRU data) — a dedicated research/replication project, not a pipeline addition; do not schedule alongside the rows above** | §2b |

---

## How to update this inventory

**Tier 1:** when a new owned table/series is built (e.g. IPCA sub-item detail moves from WIP to production, an IGP-M or IPP connector is added), update the relevant section and remove/adjust the corresponding gap-summary row.

**Tier 2:** when a new specialist agent (activity/labor, fiscal, exchange rate's remaining gaps, or a global/markets agent) gets scoped, replace its placeholder bullet list with the actual table/column references that agent produces, the same way Tier 1 entries are documented — and note the hand-off format once that's decided, mirroring the convention in `monetary_policy_data_inventory.md`.
