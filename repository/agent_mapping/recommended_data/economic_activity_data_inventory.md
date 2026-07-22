# Economic Activity Data Inventory

**Purpose:** maps the data the economic activity agent needs to what already exists in the LIS database vs. what's missing — following the same pattern as `exchange_rate_data_inventory.md`, `monetary_policy_data_inventory.md`, and `inflation_data_inventory.md`. Built after the literature pass (`economic_activity_bibliography_candidates.md`), per the agreed order.

**Two-tier structure, per the established convention:** like inflation, economic activity is closer to a **net producer** than a consumer — `macro_brasil` already has GDP, IBC-Br, and three monthly surveys (industrial, retail, services) with real depth, and both the monetary policy and inflation inventories already list an output gap, a wage/hours signal, and a credit-impulse read as things they expect to receive *from* this agent. So this file keeps the same split for consistency, with the balance skewed toward Tier 1:

- **Tier 1 — Owned data:** GDP, IBC-Br, and the monthly activity surveys, plus what's still missing on the *derived* side (output gap, potential growth/TFP, cycle dating, leading indicators) even though the raw series feeding them mostly already exist.
- **Tier 2 — Consumed data:** structured hand-offs this agent needs *from* other agents (a labor-market signal for the "hours worked" half of potential growth, a fiscal-impulse read, commodity/global shocks) — placeholders until those agents are scoped.

---

## Tier 1 — Owned data

### 1. Quarterly GDP (Contas Nacionais Trimestrais)

| What we have | Table | Series | Note |
|---|---|---|---|
| Supply side — agriculture, industry (+ extractive/manufacturing/utilities/construction), services (+ commerce/transport/info-comm/finance/real estate/other/public admin) | `macro_brasil.atv_pib` | `agropecuaria`, `industria`, `ind_extrativas`, `ind_transformacao`, `eletricidade_gas_agua`, `construcao`, `servicos`, `comercio`, `transporte_correio`, `informacao_comunicacao`, `financeiras_seguros`, `imobiliarias`, `outros_servicos`, `adm_saude_educacao_pub` | NSA and SA |
| Demand side — household consumption, government consumption, gross fixed capital formation, exports, imports | `macro_brasil.atv_pib` | `consumo_familias`, `consumo_adm_publica`, `fbcf`, `exportacao`, `importacao` | NSA and SA |
| Aggregates | `macro_brasil.atv_pib` | `pib_pm`, `valor_adicionado`, `impostos_liquidos` | NSA and SA |

Script: `domain/db/brasil/ibge/atv_pib.py`. IBGE aggregados 1620 (NSA)/1621 (SA), volume-index series. **This is a genuinely complete both-sides-of-GDP dataset** — supply and demand decomposition together, which many countries' own statistical agencies don't publish this readily disaggregated.

**Gaps:**
- Coverage per `CLAUDE.md`: 2016 → today. IBGE's own Contas Nacionais Trimestrais series goes back to 1996 — the ~2016 starting point is a script default (`years_back`), not a source limitation, so a full-history backfill (`periodos="all"`) is a low-effort extension, same pattern as the ~36-month rolling windows flagged repeatedly in the other three inventories.

### 2. IBC-Br (monthly GDP proxy)

| What we have | Table | Series | Coverage |
|---|---|---|---|
| Total, and by sector (agriculture, industry, services, ex-agriculture, taxes) | `macro_brasil.atv_ibcbr` | `ibcbr_nsa`/`ibcbr_sa`, `ibcbr_agropecuaria_*`, `ibcbr_industria_*`, `ibcbr_servicos_*`, `ibcbr_ex_agropecuaria_*`, `ibcbr_impostos_*` | 2003 → today, NSA and SA |

Script: `domain/db/brasil/bcb/atv_ibcbr.py`. BCB SGS. Directly matches the methodology documented in bibliography cluster 7 (the 2010 launch box, 2016 revision, 2018 GDP-comparison study) — worth cross-checking the local column set against that methodology once those three sources are processed into the conceptual map, the same way inflation's inventory flagged doing for its núcleo series against NT 57.

**Gaps:** none identified at the raw-series level — this table is essentially complete relative to what BCB itself publishes for IBC-Br.

### 3. Monthly industrial production (PIM)

| What we have | Table | Series | Coverage |
|---|---|---|---|
| General industry, extractive industry, manufacturing | `macro_brasil.atv_pim` | `industria_geral`, `ind_extrativas`, `ind_transformacao` | 2002 → today, NSA and SA |

Script: `domain/db/brasil/ibge/atv_pim.py`. IBGE aggregado 8888.

**Gap:** only the 3 highest-level categories are ingested — IBGE's PIM also publishes by broad sectoral/use-based category (capital goods, intermediate goods, durable/semi-durable/non-durable consumer goods) and by specific industrial sector (CNAE divisions), neither of which is captured here. This is the PIM-side equivalent of the disaggregation IPCA already has in the inflation agent's inventory — useful for identifying *which* part of industry is driving a given month's move, not just the aggregate.

### 4. Monthly retail trade (PMC)

| What we have | Table | Series | Coverage |
|---|---|---|---|
| Restricted and expanded retail totals | `macro_brasil.atv_pmc` | `comercio_restrito_total`, `comercio_ampliado_total` | NSA and SA |
| 14 retail segments (fuel, supermarkets, apparel/footwear, furniture/appliances, pharma, books, IT equipment, other personal/household, vehicles, construction materials, wholesale food) | `macro_brasil.atv_pmc` | segment-level series (see `domain/db/brasil/ibge/atv_pmc.py`) | NSA and SA |

Script: `domain/db/brasil/ibge/atv_pmc.py`. IBGE aggregados 8880/8881/8883.

**Gap — short history:** coverage per `CLAUDE.md`: 2023 → today only, driven by the script's `years_back=3` default. IBGE's PMC series (both restricted and expanded) go back to the late 1990s/2000s depending on the exact series — a full backfill would materially improve this table's usefulness for anything beyond the most recent cycle.

### 4a. Vehicle sales/licensing (Fenabrave via BCB SGS) — ⚠️ GAP, verified codes, not yet ingested

A confirmed, currently-active family of BCB SGS series, sourced from Fenabrave (the dealer federation) and distinct from anything already in PMC — the `veiculos_motocicletas_pecas` segment in `macro_brasil.atv_pmc` §4 tracks retail *revenue* for vehicle dealers, while this family tracks actual *unit sales volumes* by vehicle type. Vehicle sales/licensing is one of the most-watched high-frequency consumer-durables activity signals in Brazil, comparable to auto sales data in the US — checked live against the BCB SGS API on 2026-07 and all four series are current through May 2026:

| Series | SGS code | Note |
|---|---|---|
| Automóveis (passenger cars) | 7384 | |
| Comerciais leves (light commercial vehicles) | 7385 | |
| Caminhões (trucks) | 7386 | |
| Ônibus (buses) | 7387 | |

**Related, not yet ingested — vehicle-purchase credit** (ties this section to §10's credit table): `Concessões de crédito com recursos livres — Pessoas físicas — Aquisição de veículos` (SGS 20673) and the corresponding average interest rates for individuals (SGS 25471) and legal entities (SGS 20728) — a directly relevant credit-conditions overlay for interpreting vehicle sales moves (are sales rising because of demand, or because auto-loan rates fell).

**Note on discontinued predecessor codes:** SGS 1381 and 1385 (an older vehicle-sales series pair) return data only through December 2020 — superseded by the 7384-7387 family above; don't use them for new ingestion.

**Possible source:** straightforward addition via the existing `connectors/bcb.py` SGS client, same pattern as `atv_ibcbr.py` or `cred_credito_amplo.py` — no new connector needed, just a new script (e.g. `domain/db/brasil/bcb/vendas_veiculos.py`) with these 7 codes (4 sales + 3 credit/rate).

### 5. Monthly services (PMS)

| What we have | Table | Series | Coverage |
|---|---|---|---|
| Total services, plus 4 main groups (services to families, information/communication, professional/administrative, transport/mail) and their sub-segments (lodging, food service, telecom, IT services, road/air/water transport, real estate, etc.) | `macro_brasil.atv_pms` | `servicos_total`, `servicos_familias`, `informacao_comunicacao`, `prof_adm_complementares`, `transportes_correio`, plus ~20 sub-segment columns | NSA and SA |

Script: `domain/db/brasil/ibge/atv_pms.py`. IBGE aggregado 8688. **Genuinely deep disaggregation** — likely the most granular single table in `macro_brasil` outside of `inflacao`.

**Gap — same short-history issue as PMC:** coverage per `CLAUDE.md`: 2023 → today only (`years_back=3` default), while IBGE's PMS series go back further. Same low-effort fix as §4.

### 6. Output gap and potential growth — ⚠️ GAP, now unblocked by the literature pass

No output gap or potential-output series is computed anywhere in the database — this is the same gap already flagged in `monetary_policy_data_inventory.md` §4 ("no neutral/equilibrium real rate... no output gap") from the monetary policy side. What's changed since that inventory was written: **the methodology is no longer missing** — `economic_activity_bibliography_candidates.md` cluster 5 now has both the general toolkit (HP filter, Blanchard-Quah SVAR, Kuttner unobserved-components) and two Brazil-specific applications (Cusinato-Minella-Pôrto Júnior 2010, BCB WP 203; Souza Júnior 2005, IPEA TD 1130) with real, replicable methodology. The blocker is now purely implementation — computing any of these against `macro_brasil.atv_pib` (§1) and/or `atv_ibcbr` (§2), which are already sufficient inputs.

**Recommended starting point:** the HP filter is the cheapest to implement and the most-replicated in the literature, but per Hodrick & Prescott's own paper (and its well-known end-of-sample bias) should be flagged as a first-pass estimate, not a final one — the Harvey-Clark unobserved-components approach from Cusinato et al. (2010) is more defensible but requires more implementation work.

### 7. Productivity and TFP — ⚠️ GAP, data exists externally but isn't ingested

`economic_activity_bibliography_candidates.md` cluster 9 identifies exactly where Brazilian productivity data lives: BCB's own labor-productivity study (Estudo Especial 27/2018) is a one-off report, not an ongoing series, and FGV/IBRE's own annual TFP series (Veloso, Matos & Peruchetti, 2020a/b) is published on the **Observatório da Produtividade Regis Bonelli** (ibre.fgv.br/observatorio-produtividade) — a portal, not an SGS-style API.

**Impact:** the agent cannot today track Brazilian TFP or labor productivity as a time series at all — every existing reference is a static report snapshot.

**Possible source:** would require either (a) a lightweight scraper against the Observatório da Produtividade portal (structure and update cadence not yet investigated), or (b) manually re-entering the annual series from Veloso, Matos & Peruchetti's published tables once that source is acquired and processed. Not yet scoped either way.

### 8. Business cycle dating (CODACE) — ⚠️ GAP

No table records Brazil's own business-cycle turning points. This is the direct analogue of the "no COPOM decision history table" gap already flagged in `monetary_policy_data_inventory.md` §1 — CODACE (FGV/IBRE's dating committee, cluster 6 of the bibliography) publishes peak/trough dates on an irregular basis, and nothing here captures them as discrete, queryable events.

**Impact:** the agent can describe the *current* IBC-Br/GDP trend but can't answer "how does the current slowdown compare, in depth and duration, to the last N recessions" without manually looking up CODACE's own bulletins each time.

**Possible approach:** a small `codace_ciclos` table — `(data_pico, data_vale, duracao_contracao_meses, duracao_expansao_meses)` — sourced by periodically checking CODACE's published chronology (ibre.fgv.br). No script built yet; low data volume (a handful of cycles since CODACE's chronology starts in the 1980s) makes this cheap once someone owns the periodic check.

### 9. Leading/coincident composite indicators and financial conditions — ⚠️ GAP

Beyond IBC-Br itself (§2, which is BCB's own coincident index), none of the other indicators identified in bibliography cluster 6 are ingested:
- No replication of the Duarte-Issler-Spacov (2004) coincident/leading index methodology.
- No **Indicador de Condições Financeiras (ICF)** — BCB's own daily financial-conditions leading indicator (Estudo Especial 76/2020, 26 variables across 7 groups via PCA) is published but not stored anywhere in `macro_brasil`.
- No **economic policy uncertainty index** for Brazil (Estudo Especial 65/2019's Baker-Bloom-Davis-style methodology) — not ingested.

**Possible source for ICF specifically:** BCB may publish the ICF itself via SGS (unconfirmed — would need a quick check of the Estudo Especial 76/2020 for a series code, the same way NT 57 documented exact codes for the inflation núcleos); if not on SGS, it would need to be replicated from the 26 underlying inputs, a much larger task.

### 10. Credit (activity/financial-conditions input, owned but cross-referenced)

| What we have | Table | Series | Note |
|---|---|---|---|
| Broad non-financial-sector credit by instrument and institutional sector (government, corporates, households — 17 series) | `macro_brasil.cred_credito_amplo` | see `domain/db/brasil/bcb/cred_credito_amplo.py` | Owned by this agent — credit growth/impulse is a standard leading/coincident activity signal, not primarily a monetary-policy series despite living alongside monetary-policy-relevant data |

**Gap:** no credit *impulse* measure computed (the change in new credit flow as a share of GDP, the standard "credit impulse" concept from the financial-accelerator literature already in monetary policy's bibliography) — only the raw stock/flow series exist today.

### 11. Household financial conditions (context, partially owned)

| What we have | Table | Series |
|---|---|---|
| Household debt-to-income, interest burden, debt-service burden (interest + amortization) as % of income | `macro_brasil.cred_credito_familias` | 3 series, see `domain/db/brasil/bcb/cred_credito_familias.py` |

Relevant as a consumption-capacity constraint (household deleveraging/releveraging cycles) but more directly tied to credit conditions than to activity measurement itself — flagged here for completeness rather than as a priority.

---

## Tier 2 — Consumed data (placeholders, pending other agents)

### From a future labor market agent (the split the user is actively considering)
- Hours worked / employment-rate / participation-rate decomposition — the "hours worked" half of the standard potential-growth decomposition (potential growth = labor productivity growth + hours-worked growth) referenced in BCB's own June 2024 RPM chapter on growth projections. Without this, cluster 9's productivity work (§7) can be computed but can't be combined into a full potential-growth read.
- Unemployment gap / NAIRU-type estimate — the labor-market-side companion to this agent's own output gap (§6); the two are usually estimated jointly or at least cross-checked against each other.
- Wage growth and wage bill — already sitting in `macro_brasil.mt_pnad` today (per `inflation_data_inventory.md` §6, which documents the same table from the wage-price-spiral angle) — usable by this agent too without new ingestion, once formally scoped as a labor-agent-owned, activity-agent-consumed series.

### From the monetary policy agent (reciprocal dependency, already documented from that side)
`monetary_policy_data_inventory.md` already lists this agent's expected output-gap and credit-impulse deliverables as its own Tier 2 gap — so the dependency here runs the other way too: this agent would want the real Selic/real rate stance (already computed in `macro_international.diferenciais_juros`) to interpret whether a given activity reading reflects tight or loose policy, not just describe the reading in isolation.

### From a future fiscal agent
- Government investment execution pace and fiscal impulse — needed to properly interpret the `consumo_adm_publica` and public-investment components already owned in `macro_brasil.atv_pib` §1; today those series exist but there's no read on whether a given move is discretionary policy or automatic/base-effect.

### From the exchange rate agent (substantially built already)
- REER (`macro_international.cmb_reer`) and terms of trade (`macro_brasil.cmb_termos_troca`) already exist and are directly usable for bibliography cluster 8's Dutch-disease/commodity-cycle work without waiting on any new agent — flagged here only so the cross-reference is explicit, mirroring how `inflation_data_inventory.md` treats the same two tables.

### From a possible future global/markets agent (not yet scoped at all)
- Commodity price indices — same gap already flagged in `inflation_data_inventory.md`'s Tier 2 section; relevant here for the Fernández-Schmitt-Grohé-Uribe (2017) "how much of the cycle is the world commodity cycle" framework in bibliography cluster 8.
- A common World/EM business-cycle factor (à la Fernández, Schmitt-Grohé & Uribe) — no domestic or international proxy exists in the database today.

---

## Gap summary (Tier 1 only — Tier 2 gaps are dependencies on unbuilt agents, not data gaps per se)

| Priority | Gap | Category |
|---|---|---|
| High | No output gap / potential output estimate computed — methodology now available (bibliography cluster 5), purely an implementation gap | §6 |
| High | No CODACE business-cycle dating table — same class of gap as monetary policy's missing COPOM decision history | §8 |
| Medium | No Brazilian TFP/productivity time series ingested — data exists (FGV/IBRE portal) but requires a scraper or manual re-entry | §7 |
| Medium | PMC and PMS limited to 2023 → today (script defaults) despite IBGE series going back much further | §4, §5 |
| Medium | No BCB Indicador de Condições Financeiras (ICF) or economic-policy-uncertainty index ingested | §9 |
| Medium | Vehicle sales/licensing (SGS 7384-7387) and vehicle-purchase credit (SGS 20673/25471/20728) not ingested — verified live codes, cheap to add, high-frequency consumer-durables leading indicator | §4a |
| Low | GDP table defaults to 2016 → today despite Contas Nacionais Trimestrais data existing since 1996 | §1 |
| Low | PIM ingests only the 3 top-level categories, not the use-based or CNAE-division breakdowns IBGE also publishes | §3 |
| Low | No credit impulse measure computed from the raw `cred_credito_amplo` series | §10 |
| Low | No replication of the Duarte-Issler-Spacov coincident/leading index methodology | §9 |

---

## How to update this inventory

**Tier 1:** when a new owned table/series is built (e.g. an output gap estimate, a `codace_ciclos` table, a TFP scraper), update the relevant section and remove/adjust the corresponding gap-summary row.

**Tier 2:** when the labor market vs. economic activity split is finalized, and when fiscal/global-markets agents get scoped, replace each placeholder bullet list with the actual table/column references those agents produce, the same way Tier 1 entries are documented — mirroring the convention in `monetary_policy_data_inventory.md` and `inflation_data_inventory.md`.
