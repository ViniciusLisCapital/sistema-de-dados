# Fiscal Policy Data Inventory

**Purpose:** maps the data the fiscal policy agent needs to what already exists in the LIS database vs. what's missing — following the same pattern as the exchange rate, monetary policy, inflation, economic activity, and labor market inventories. Built after the literature pass (`fiscal_policy_bibliography_candidates.md`), per the agreed order.

**This inventory is different in kind from the other four: there is currently no fiscal data pipeline at all.** A direct check of `domain/db/brasil/bcb/` and `domain/db/brasil/ibge/` (2026-07) confirms zero existing scripts for debt, fiscal result, revenue, or expenditure — every other agent's inventory documented a mix of owned tables and gaps; this one is close to 100% gap. To make that gap actionable rather than just naming it, every candidate series below was checked live against the BCB SGS API before being listed, the same verification standard used for `economic_activity_data_inventory.md` §4a's vehicle sales addition — so what follows is a **recommended build-out with confirmed codes**, not a wishlist.

**Two-tier structure, kept for consistency even though Tier 1 starts empty:**
- **Tier 1 — Owned data (recommended build-out):** debt stock, fiscal balance, and the other series this agent should ingest directly, each with a verified SGS code where one was found.
- **Tier 2 — Consumed data:** what this agent needs from other agents — thinner than usual to write today, since most of what it needs (the output gap for cyclical adjustment, a risk premium for debt-intolerance framing) is itself either a gap or a placeholder in those agents' own inventories.

---

## Tier 1 — Owned data (recommended build-out, nothing ingested yet)

### 1. Public debt stock

| Series | SGS code | Note |
|---|---|---|
| Dívida Bruta do Governo Geral (DBGG) — % GDP | 13762 | gross debt, general government, current methodology (post-2008) |
| Dívida Líquida do Setor Público (DLSP) — % GDP, total (federal government + central bank) | 4503 | |
| Dívida líquida do governo geral — % GDP | 4536 | narrower institutional scope than 4503 (excludes public enterprises/state-level nuances captured elsewhere) |
| Dívida Líquida do Setor Público — R$ million, total, consolidated public sector | 4478 | the level series behind the ratio series above — useful for reconciling with nominal GDP independently rather than trusting BCB's own ratio calculation |

All four confirmed live against the BCB SGS API (2026-07), current through May 2026. **This is the single most foundational gap in this inventory** — bibliography cluster 1 (debt sustainability arithmetic) and cluster 4 (debt intolerance) are both unusable for Brazil without a debt-stock series, and monetary policy's, inflation's, and economic activity's inventories all already list "a primary-balance/debt-trajectory signal" as a Tier 2 dependency on this agent.

**Gap within the gap:** DBGG (gross) and DLSP (net) are conceptually different and shouldn't be used interchangeably — gross debt doesn't net out financial assets (like BCB's own international reserves) the way net debt does, and international debt-sustainability comparisons (including Reinhart-Rogoff-Savastano's debt-intolerance thresholds, bibliography cluster 4) are usually framed in gross terms while Brazil's own domestic commentary has historically emphasized net debt — both should be ingested rather than picking one.

### 2. Fiscal balance (primary and nominal result)

| Series | SGS code | Note |
|---|---|---|
| NFSP sem desvalorização cambial — Resultado primário, % GDP, 12-month accumulated flow, consolidated public sector | 5793 | the standard "primary result" headline figure |
| NFSP sem desvalorização cambial — Resultado nominal, % GDP, 12-month accumulated flow, consolidated public sector | 5727 | primary result plus net interest payments — the figure that actually determines whether debt-to-GDP (§1) is rising or falling, given Domar's arithmetic (bibliography cluster 1) |
| NFSP sem desvalorização cambial — Resultado primário, current monthly flow, R$ million, consolidated public sector | 4649 | the monthly (not 12m-smoothed) series — needed for anything higher-frequency than the standard 12m headline read, e.g. seasonal patterns in tax collection/spending |

All three confirmed live (2026-07). "NFSP" = Necessidades de Financiamento do Setor Público, BCB's own public-sector-borrowing-requirement framework — "sem desvalorização cambial" means the exchange-rate-valuation effect on FX-denominated debt is stripped out, giving a cleaner read on the actual fiscal effort rather than a currency-move artifact.

**Gap within the gap:** BCB's "setor público consolidado" (consolidated public sector, the scope of all series above) bundles federal government, states, municipalities, and state-owned enterprises together — there is no breakdown by government level in what's ingested so far, which matters directly for bibliography cluster 6 (subnational federalism). Separately, **Tesouro Nacional's own monthly "Resultado do Tesouro Nacional" and "Resultado Primário do Governo Central" releases** are methodologically distinct from BCB's SGS figures (different institutional scope — central government only, not the full consolidated public sector) and are the more commonly-cited headline number in Brazilian financial-press coverage; whether Tesouro publishes this as its own SGS-accessible series or only via its own portal (Tesouro Transparente) wasn't confirmed in this pass.

### 3. Government revenue and expenditure breakdown — ⚠️ GAP, no codes identified yet

No series for tax revenue (by type — IRPF, IRPJ, COFINS, ICMS et al.) or expenditure (by function — Previdência, saúde, educação, custeio vs. investimento) was identified in this pass. This is a materially bigger gap than §1-§2: debt and the aggregate balance answer "how much and is it rising," but nothing here yet answers "why" — which specific revenue or spending line is driving a given month's fiscal outcome.

**Possible source:** likely Tesouro Nacional's own RREO (Relatório Resumido de Execução Orçamentária, monthly-ish) and RGF (Relatório de Gestão Fiscal, quarterly) releases, or the SIAFI/Tesouro Transparente portal directly — none of these were investigated for API accessibility in this pass, unlike the SGS-based series in §1-§2 which are confirmed straightforward.

### 4. Pension/social security balance (RGPS deficit) — ⚠️ GAP

Bibliography cluster 5 identifies pension spending as the dominant driver of Brazil's structural primary-spending growth, but no series specifically isolating the RGPS (Regime Geral de Previdência Social) actuarial or cash-flow deficit was identified or confirmed via SGS in this pass — this would sit *inside* §3's broader expenditure-by-function breakdown rather than as its own standalone series, but is flagged separately given how load-bearing it is for reading EC 103/2019's (2019 pension reform) actual realized effect, the same open gap already flagged in the bibliography file itself.

### 5. Fiscal rule compliance metrics (Teto de Gastos / Novo Arcabouço Fiscal) — ⚠️ GAP, likely a small lookup table rather than an SGS series

Neither the historical Teto de Gastos (EC 95/2016) ceiling levels nor the current Novo Arcabouço Fiscal's (LC 200/2023) expense-growth band (0.6%-2.5% real) and annually-set primary-result target (set via the LDO, per bibliography cluster 3) are tracked anywhere. Unlike §1-§2, this is very unlikely to be an SGS series — it's a small number of administratively-set parameters that change on a predictable (annual, for the LDO target) or rare (constitutional-amendment-level, for a rule replacement) cadence.

**Recommended approach:** a small lookup table — `(ano, meta_resultado_primario, banda_crescimento_despesa_min, banda_crescimento_despesa_max, regra_vigente)` — maintained by periodically checking the LDO and any rule amendments, the same "small, slow-moving, cheap once someone owns it" pattern already used for the proposed inflation-target-parameters table in `monetary_policy_data_inventory.md` §6 and the proposed minimum-wage table in `labor_market_data_inventory.md` §7.

**Why this matters beyond bookkeeping:** without it, the agent can report the primary result (§2) but can't say whether it's *compliant* with the rule currently in force — the entire point of a fiscal rule, per bibliography cluster 3's Kopits & Symansky framework, is that it's a benchmark to be measured against, not just a number to report in isolation.

### 6. Subnational (states and municipalities) debt and fiscal result — ⚠️ GAP

Bibliography cluster 6 (federalism/subnational debt, built around Rodden's *Hamilton's Paradox*) has no matching data — §1-§2's series are all consolidated-public-sector aggregates with no state/municipality-level breakdown. Given Rio de Janeiro's 2016-17 fiscal crisis is one of the bibliography's own flagged open gaps (a citation, not just data), this is a case where the literature and data gaps reinforce each other and are worth closing together.

**Possible source:** BCB SGS does publish some subnational-level debt series (state-level DLSP breakdowns) — not confirmed via live check in this pass, unlike §1-§2; STN (Secretaria do Tesouro Nacional) also publishes state-level fiscal data directly. Needs a dedicated verification pass before building.

### 7. Minimum wage and Previdência indexation — owned elsewhere, cross-referenced here

Already flagged as a gap from the labor market side in `labor_market_data_inventory.md` §7 (no series exists at all) — restated here only because the *fiscal* consequence of the minimum wage (its role as the indexing floor for Previdência and BPC benefit payments, bibliography cluster 6's Brazil relevance note) is this agent's concern even though the series itself would be owned by labor market, mirroring how `inflation_data_inventory.md` and `economic_activity_data_inventory.md` both reference `mt_pnad` from their own angle without owning it.

---

## Tier 2 — Consumed data (placeholders, pending other agents)

### From the economic activity agent
- Output gap / potential output estimate — needed to compute a cyclically-adjusted (structural) primary balance, the standard way of separating a genuine fiscal policy stance change from an automatic, cycle-driven revenue/spending swing. Flagged as a gap in `economic_activity_data_inventory.md` §6 itself — this agent inherits that same gap rather than duplicating it.
- Nominal GDP — needed as the denominator for every ratio series in §1-§2 above; `macro_brasil.atv_pib` already has this (owned by economic activity), so this is a straightforward existing dependency rather than a placeholder.

### From the exchange rate agent
- A sovereign risk premium proxy (EMBI-style spread, or CDS) — the market-priced complement to Reinhart-Rogoff-Savastano's debt-intolerance framing (bibliography cluster 4): does the market currently treat Brazil's debt level as risky, independent of what the arithmetic alone would say? Not currently identified as existing in `exchange_rate_data_inventory.md` either — a gap shared across two agents' inventories rather than resolved in either.

### From the monetary policy agent
- The real interest rate path (Selic real, already computed in `macro_international.diferenciais_juros`) — needed to project debt-service costs and to interpret the r-vs-g comparison (Domar 1944 / Blanchard 2019, bibliography cluster 1) using Brazil's actual, not a generic, r.

### From the labor market agent
- The minimum wage series and Previdência indexation rule itself, once built there (§7 above) — restated as a forward pointer rather than a fresh placeholder.

---

## Gap summary (Tier 1 only — Tier 2 gaps are dependencies on other agents' own unresolved gaps, not fresh ones)

| Priority | Gap | Category |
|---|---|---|
| High | No public debt stock series at all (gross and net) — verified SGS codes identified, purely an implementation gap | §1 |
| High | No fiscal balance series at all (primary and nominal result) — verified SGS codes identified, purely an implementation gap | §2 |
| Medium | No revenue/expenditure breakdown by type or function — no source confirmed yet, needs investigation beyond SGS | §3 |
| Medium | No fiscal rule compliance table (Teto de Gastos historical, Novo Arcabouço target/band vs. actual) | §5 |
| Medium | No subnational (state/municipality) debt or fiscal result breakdown | §6 |
| Low | No RGPS/Previdência-specific deficit series isolated from the broader expenditure breakdown | §4 |
| Low | Tesouro Nacional's own central-government-only result release not reconciled against BCB's consolidated-public-sector series | §2 |

---

## How to update this inventory

**Tier 1:** this entire section starts as a build-out plan, not a documentation of existing tables — as each script gets built (e.g. `domain/db/brasil/bcb/divida_publica.py`, `domain/db/brasil/bcb/resultado_fiscal.py`), move its description from "recommended" language to the same "what we have" framing used in the other four inventories, and remove the corresponding gap-summary row.

**Tier 2:** when economic activity's output-gap gap closes, or an exchange-rate risk-premium series gets built, replace the placeholder bullets here with the actual table/column references, mirroring the convention in the other four inventories.
