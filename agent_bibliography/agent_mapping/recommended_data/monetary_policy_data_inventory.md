# Monetary Policy Data Inventory

**Purpose:** maps the data the monetary policy agent needs to what already exists in the LIS database vs. what's missing — following the same pattern as `exchange_rate_data_inventory.md`. Built after the literature pass (`monetary_policy_bibliography_candidates.md`), per the agreed order.

**Two-tier structure, per the agreed architecture:** the monetary policy agent's central job is to synthesize inputs — largely following the Svensson (1997) forecast-targeting logic already in the bibliography — into a reaction-function-style read on the policy rate (expected/optimal Selic level or move). That means most of its inputs will eventually come from *other* specialist agents (inflation, activity, fiscal, exchange rate) that don't exist yet. So this inventory splits into:

- **Tier 1 — Owned data:** things irreducibly the monetary policy agent's own — the policy rate itself, market pricing of it, the central bank's own communications, and derived analytics (differentials, real/neutral rate). Buildable now, independent of any other agent.
- **Tier 2 — Consumed data:** structured, quantitative hand-offs the agent would need *from* other agents once they exist (an inflation-gap number, an output-gap number, etc.) — not prose summaries, since a reaction-function diagnostic needs numbers, not paragraphs. These are placeholders today; when each supplying agent is scoped, replace the placeholder with its actual table/column reference.

---

## Tier 1 — Owned data

### 1. Policy rate & COPOM decision history — ⚠️ GAP

There is no dedicated table recording COPOM decisions as discrete events (meeting date, rate before/after, change in bps, vote count/dissent). The Selic level only exists today embedded inside `macro_analytics.diferenciais_juros` (series `selic`, sourced from BCB SGS 432) as a continuous monthly series for computing rate differentials — it was never built to answer "what did COPOM actually decide, and how divided was the committee, at each meeting."

**Impact:** without this, the agent can't backtest a reaction function against actual historical decisions, or characterize dissent/unanimity patterns (directly relevant to reading credibility, per the Barro-Gordon/Rogoff literature already in the bibliography).

**Possible approach:** a `copom_decisions` table — `(meeting_date, selic_before, selic_after, change_bps, votes_for, votes_against, unanimous)` — sourced from BCB SGS 432 (which already carries COPOM meeting dates, not calendar dates) plus vote counts parsed from the Ata once §8 of the bibliography is acquired. No script built yet.

### 2. Interest rate differentials (carry)

| What we have | Table | Series |
|---|---|---|
| Selic, Fed Funds (raw) | `macro_analytics.diferenciais_juros` | `selic`, `fed_funds` |
| Nominal and real ex-post differentials | `macro_analytics.diferenciais_juros` | `diferencial_nominal`, `real_br_ex_post`, `real_us_ex_post`, `diferencial_real` |

Script: `domain/db/analytics/fred/diferenciais_juros.py`. Same table already documented from the FX angle in `exchange_rate_data_inventory.md` §2 — for monetary policy the read is different: this is the agent's primary evidence of *where policy stance sits relative to global conditions*, not just a carry-trade input.

**Gaps (same underlying ones as the FX inventory, restated for this agent's purposes):**
- History limited to ~36 months by default — needs full extension (Selic since 1996, Fed Funds since 1954).
- Ex-ante differentials (Focus-based) not implemented — see `CAMBIO.md` §1b/§2. For monetary policy specifically, `selic_ex_ante` (Focus Selic EOP 12m, already sitting in `macro_brasil.expectativas`) is close to the single most directly relevant missing series: it's the market's own forward-looking read on the same thing the agent is trying to compute.

### 3. Market-implied rate expectations

| What we have | Table | Note |
|---|---|---|
| Focus survey — Selic median/mean expectations | `macro_brasil.expectativas` | `indicador = 'Selic'`, various horizons; 2001 → today |
| Focus survey — IPCA, IGP-M expectations | `macro_brasil.expectativas` | same table, other `indicador` values |

Script: `domain/db/brasil/bcb/expectativas.py`. This is genuinely useful, already-available data — the agent can compare its own reaction-function output against what professional forecasters expect BCB to do, without waiting on any other agent.

**Gaps:**
- No DI futures curve (B3) — the *market-priced*, real-time-updating implied Selic path, as opposed to the survey-based Focus median. This is the same Bloomberg-dependent gap already flagged in `CAMBIO.md` §5 ("Cupom cambial + futuros B3 — Fase 3, requires `blpapi`/`xbbg`"). Focus is a usable substitute today but updates weekly and reflects survey consensus, not tradeable pricing.

### 4. Real interest rate & neutral rate (r*) — ⚠️ largely a GAP

| What we have | Table | Note |
|---|---|---|
| Real rate ex-post (Selic − realized IPCA 12m) | `macro_analytics.diferenciais_juros` | `real_br_ex_post` |

**Gaps:**
- No ex-ante real rate (Selic − *expected* IPCA, which is the theoretically correct measure of how restrictive/expansionary policy actually is right now) — same missing piece as item 2 above (needs Focus IPCA expectations, already available, just not yet combined).
- No neutral/equilibrium real rate (r*) estimate at all. This is precisely the gap the Muinhos & Nakane (2006) bibliography candidate addresses theoretically, but there's no data pipeline — no market-based proxy (e.g. long NTN-B real yields) and no BCB model-based estimate (which the RPM publishes as part of its projection exercise, once §8 of the bibliography is acquired). Without r*, the agent has no denominator for "how tight is policy," which is arguably the single most load-bearing number for a synthesis agent to have.

### 5. COPOM primary-source communications

Covered in `monetary_policy_bibliography_candidates.md` §8 (Comunicado, Ata, Relatório de Política Monetária). Not data in the numeric-series sense — text. Retention window and ingestion mechanism explicitly deferred in that file; not repeated here. Once acquired, the RPM in particular would also be the natural source for BCB's own r* assumption (see item 4).

### 6. Inflation target regime parameters — ⚠️ GAP, low effort to close

No table records the history of the target itself: the numeric target, tolerance band width, and target horizon, as set by CMN (Conselho Monetário Nacional) resolutions, which have changed several times since 1999 (target level, band width, and the horizon convention have all been revised over the years). This is small, slow-moving, easy to build (a short lookup table by year) but currently doesn't exist anywhere — without it, the agent can't correctly compute an inflation gap even once it has an inflation forecast, since "the target" isn't a fixed constant across the whole sample.

### 7. Global monetary conditions

| What we have | Table | Series |
|---|---|---|
| Fed Funds (raw, as part of the differential calc) | `macro_analytics.diferenciais_juros` | `fed_funds` |

**Gaps:** only the Fed is covered. No broader global policy-rate context (ECB, other EM central banks) for situating BCB within the "global financial cycle" framing central to the Rey (2013) / Obstfeld (2015) debate in the bibliography's `#global_spillovers_em_autonomy` cluster. Low priority unless a specific cross-country comparison becomes necessary.

---

## Tier 2 — Consumed data (placeholders, pending other agents)

None of this exists yet in any form — these are the structured outputs the monetary policy agent will need to request once each supplying agent is actually scoped and built. Listed here so the dependency is visible now rather than discovered later.

### From a future inflation agent
- Inflation gap / nowcast at the policy-relevant horizon (the actual forecast-targeting input Svensson's framework calls for)
- Core inflation decomposition and diffusion index (breadth of price pressure)
- Signal on whether inflation expectations are anchored or de-anchoring (distance of Focus 12m/24m from target, and its trend)

### From a future activity agent
- Output gap estimate (vs. `ibc_br`/`gdp`-based potential)
- Labor market slack (unemployment gap vs. NAIRU-type estimate)
- Credit growth / credit impulse read (ties to the `#transmission_channels_financial_frictions` bibliography cluster — how much of any given Selic move is actually reaching the real economy through credit)

### From a future fiscal agent
- Primary balance and debt trajectory signal
- A fiscal impulse measure (is fiscal policy net expansionary or contractionary right now)
- A fiscal-dominance / sustainability risk signal — directly operationalizes Blanchard (2004): is there a regime where hiking Selic further would raise, not lower, medium-term inflation risk through the debt/risk-premium channel?

### From the exchange rate agent (already substantially built — see `exchange_rate_data_inventory.md`)
This dependency is less hypothetical than the three above, since the underlying FX data pipeline already exists (`reservas`, `fluxo_cambial`, `reer`, `cot_fx`, `balanco_pagamentos`). What's still missing is the *packaging* into a monetary-policy-ready number:
- An FX pass-through estimate (how much of any BRL move shows up in inflation, and over what horizon)
- A REER over/undervaluation signal (already have raw REER in `macro_international.reer`; no "gap vs. equilibrium" estimate yet)
- A capital-flow-pressure read (from `balanco_pagamentos`/`cot_fx`) as a leading indicator of FX-driven imported-inflation risk

### From a possible future global/markets agent (not yet scoped at all)
- Global financial cycle stance / risk sentiment proxy (VIX, EM risk premia) — the empirical counterpart to the Rey/Obstfeld debate
- Commodity price cycle read (relevant both to terms of trade and to imported inflation)

---

## Gap summary (Tier 1 only — Tier 2 gaps are dependencies on unbuilt agents, not data gaps per se)

| Priority | Gap | Category |
|---|---|---|
| High | No COPOM decision history table (meeting-level rate changes, votes) | §1 |
| High | No neutral/equilibrium real rate (r*) — no proxy, no model estimate | §4 |
| Medium | Ex-ante real/nominal rate differentials not computed (inputs already exist in `expectativas`, just not combined) | §2, §4 |
| Medium | No inflation target regime parameter table (target/band/horizon history) | §6 |
| Medium | Full history of `diferenciais_juros` (same gap as FX inventory, ~36m today) | §2 |
| Low | No DI futures curve (Bloomberg-dependent) | §3 |
| Low | Global policy-rate context limited to Fed Funds only | §7 |

---

## How to update this inventory

**Tier 1:** when a new owned table/series is built (e.g. `copom_decisions`, an r* estimate), update the relevant section and remove/adjust the corresponding gap-summary row.

**Tier 2:** when a new specialist agent (inflation, activity, fiscal, or a global/markets agent) gets scoped, replace its placeholder bullet list with the actual table/column references that agent produces, the same way Tier 1 entries are documented — and note the hand-off format (e.g. a shared table, an API call, a structured file) once that's decided.
