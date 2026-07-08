# Labor Market Data Inventory

**Purpose:** maps the data the labor market agent needs to what already exists in the LIS database vs. what's missing — following the same pattern as the exchange rate, monetary policy, inflation, and economic activity inventories. Built after the literature pass (`labor_market_bibliography_candidates.md`), per the agreed order.

**Ownership resolved:** per the user's decision, `macro_brasil.pnad` and `macro_brasil.caged` belong to this agent, not economic activity — both were previously referenced from the activity side as a Tier 2 dependency; `economic_activity_data_inventory.md` already treats them that way, so no change was needed there.

**Two-tier structure, per the established convention:** like inflation and economic activity, this agent is a **net producer**, not a consumer — `pnad` and `caged` together already give it real depth (unemployment, formal/informal split, wages, sectoral employment flow), and both the inflation and economic activity inventories already list wage growth, the wage bill, an unemployment gap, and "hours worked" as things they expect *from* this agent.

- **Tier 1 — Owned data:** the labor force survey (PNAD Contínua) and the formal-employment registry (CAGED), plus what's missing on the derived side (NAIRU/NAWRU, a minimum wage series, vacancy data for the Beveridge curve, regional breakdowns).
- **Tier 2 — Consumed data:** thin, by the same logic as inflation's inventory — this agent mostly supplies rather than consumes, so this section is short.

---

## Tier 1 — Owned data

### 1. Labor force condition and unemployment (PNAD Contínua)

| What we have | Table | Series | Note |
|---|---|---|---|
| Occupied, unemployed, out of labor force | `macro_brasil.pnad` | `ocupado`, `desocupado`, `fora_da_forca_trabalho` | the core unemployment-rate input, directly feeding cluster 3's NAIRU/NAWRU work and (once a vacancy series exists) cluster 2's Beveridge curve |

Script: `domain/db/brasil/ibge/pnad.py`. IBGE aggregado 6318. Coverage per `CLAUDE.md`: 2024 → today — driven by the script's `years_back=2` default; PNAD Contínua's actual series starts in 2012, so this is the same "short default window, deeper source available" pattern flagged repeatedly in the other three inventories (`diferenciais_juros`, `pmc`/`pms`).

**Structural limitation, not a pipeline gap:** the script hardcodes `region = "Brasil"` (IBGE locality `N1`, national level only) — no state or metro-region breakdown exists. This isn't just a missing convenience: Blanchflower & Oswald's wage curve (cluster 5) is fundamentally a *cross-region* empirical relationship, and can't be tested or replicated for Brazil at all without sub-national unemployment and wage data. This is the single highest-value structural extension identified in this inventory.

### 2. Formal/informal employment split (PNAD Contínua, by occupational position)

| What we have | Table | Series | Note |
|---|---|---|---|
| Occupied population by formal/informal position — private-sector with/without carteira, domestic worker with/without carteira, public-sector (military/civil) with/without carteira, employer/self-employed with/without CNPJ | `macro_brasil.pnad` | `ocup_priv_excl_domestico_com_carteira`, `ocup_priv_excl_domestico_sem_carteira`, `ocup_domestico_com_carteira`, `ocup_domestico_sem_carteira`, `ocup_pub_*`, `ocup_empregador_*`, `ocup_conta_propria_*`, `ocup_familiar_auxiliar` | the `com_carteira` (formal, signed labor card) vs. `sem_carteira` (informal) distinction across every category is already a genuine, usable formal/informal decomposition — directly relevant to cluster 7 (Ulyssea 2018, Meghir-Narita-Robin 2015) |
| Same, by main economic activity/sector | `macro_brasil.pnad` | `ocup_agropecuaria`, `ocup_industria_geral`, `ocup_construcao`, `ocup_comercio_rep_veiculo`, `ocup_transporte_armazenagem_correio`, `ocup_alojamento_alimentacao`, `ocup_inform_comun_financ_imob_prof_adm`, `ocup_admpub_educ_saude_segsoc`, `ocup_outros_servicos`, `ocup_servicos_domesticos` | |

**This is a genuinely strong existing asset** — no new ingestion is needed to start computing a headline informality *rate* (informal occupied / total occupied); the underlying components are already there, just not combined into a single derived series. Flagged as a gap below (§6) precisely because it's cheap to close.

### 3. Wages and income (PNAD Contínua)

| What we have | Table | Series | Note |
|---|---|---|---|
| Real and nominal aggregate wage bill ("massa de rendimentos") | `macro_brasil.pnad` | `massa_real_habitual`, `massa_nominal_habitual` | already cross-referenced from `inflation_data_inventory.md` §6 for the wage-price-spiral angle; this agent is the actual owner |
| Habitual average income, by formal/informal position and by sector | `macro_brasil.pnad` | `rend_*` (mirrors the `ocup_*` breakdown in §2), plus `rend_media_nacional` | |
| Effective average income — all jobs (real/nominal) and main job (real) | `macro_brasil.pnad` | `rend_efetivo_real_todos_trabalhos`, `rend_efetivo_nominal_todos_trabalhos`, `rend_efetivo_real_trabalho_principal` | "habitual" vs. "effective" income is PNAD's own distinction between usual/regular earnings and actual earnings received in the reference period — useful for capturing irregular-income effects (common in informal work) that a habitual-only measure would miss |

**This is the data underlying Borges (2022)'s NAWRU methodology** (bibliography cluster 3) — a wage-focused Phillips curve needs exactly this kind of wage series matched against unemployment (§1). No unit-labor-cost series is computed from it yet (same gap already flagged in `inflation_data_inventory.md` §6, restated here since this agent now owns the underlying series).

### 4. Formal employment flow (CAGED)

| What we have | Table | Series | Coverage |
|---|---|---|---|
| Net balance of admissions minus dismissals, total and by sector (14 series, CNAE 2.0: agriculture, extractive industry, manufacturing, utilities, waste management, construction, commerce, services, transport/storage/mail, lodging/food, information/communication, financial/insurance activities) | `macro_brasil.caged` | see `domain/db/brasil/bcb/caged.py` | 1992 → today (per `CLAUDE.md`), script default window `n_meses=24` |

BCB SGS (14 series). **The administrative-registry complement to PNAD's household survey** — CAGED only captures formal employment (it's built from the employer registry itself) and is typically released faster than PNAD, making it the more timely leading signal for formal job creation specifically, at the cost of missing the informal side entirely (which only PNAD, §2, can see).

**Gap:** same short-default-window pattern as §1 — `n_meses=24` default vs. a genuinely deep 1992+ source; a full backfill (`start="all"`) would materially extend this table's usefulness for any cycle-length or structural-break analysis (e.g. around the 2017 labor reform).

### 5. Vacancy data (for the Beveridge curve) — ⚠️ GAP, may not exist as public data at all

Bibliography cluster 2's Beveridge curve requires both unemployment (§1, already owned) *and* a vacancy/job-openings series — Brazil has no official equivalent to the US JOLTS survey. This is flagged distinctly from the other gaps in this inventory because it may be a **genuine data-availability gap**, not just an ingestion backlog.

**Possible proxies, none verified yet:**
- CAGED admissions (§4) as an imperfect flow-based proxy for hiring — captures realized hires, not open/unfilled positions, so it's a lagging substitute at best.
- Private job-board aggregate postings (e.g. Catho, InfoJobs, LinkedIn Brazil) — no public, systematically-collected series identified; would likely require a commercial data relationship rather than a public API.
- CNI (Confederação Nacional da Indústria) or FGV/IBRE business surveys sometimes ask firms about hiring intentions/difficulty filling positions as a qualitative diffusion index — not yet investigated as a possible source.

**Impact if unresolved:** any Beveridge curve constructed for Brazil would need to rely on one of the imperfect proxies above, or forgo the vacancy axis and use CAGED admissions/dismissals gross flows as a job-creation/job-destruction proxy instead (mirroring Mortensen & Pissarides 1994's framework, bibliography cluster 1, more than the Blanchard-Diamond 1989 unemployment-vacancy framing specifically).

### 6. Derived series not yet computed from existing owned data

Distinct from §5 above — these don't require any new source, only computation against data already sitting in `pnad`/`caged`:
- **Informality rate** — trivial to derive from §2's `com_carteira`/`sem_carteira` split (informal occupied ÷ total occupied), but not computed as a standalone series today.
- **Unemployment rate** — `desocupado` ÷ (`ocupado` + `desocupado`) from §1's raw counts; same situation, a one-line derivation not yet materialized as its own column/series.
- **NAWRU/NAIRU estimate** — Borges (2022)'s methodology (bibliography cluster 3) is fully specified (wage Phillips curve with unionization and capital/human-capital controls, 1996-2017 sample) but not implemented against current data.
- **Unit labor cost** — same gap already flagged in `inflation_data_inventory.md` §6, restated here since the underlying wage (§3) and — once available from economic activity — output/hours data would combine here.

### 7. Minimum wage (salário mínimo) — ⚠️ GAP, surprising given its institutional weight

No series for the minimum wage itself exists anywhere in the database. This is a small, slow-moving, single-number series (updated annually, occasionally more often historically) — genuinely cheap to build — but its absence is notable given bibliography cluster 6's point that Brazil's minimum wage is unusually consequential: it's simultaneously a labor-market price floor *and* the indexing base for a large share of pension (Previdência) and social-benefit (BPC) payments, entangling its labor-market and fiscal effects more than in most economies.

**Possible source:** likely a short, static lookup table (by effective date) rather than an API-driven series — similar in spirit to the inflation-target-parameters gap already flagged in `monetary_policy_data_inventory.md` §6 (small, slow-moving, easy once someone owns building it).

### 8. Unionization rate — ⚠️ GAP

Borges (2022)'s NAWRU methodology (bibliography cluster 3) explicitly uses `taxa de sindicalização` as a structural control variable — no such series exists in the database. IBGE's PNAD (both the older annual PNAD and the current PNAD Contínua, via its supplementary/annual modules) does ask about union membership, but it isn't currently among the aggregados the local `pnad.py` script queries.

**Possible source:** likely a specific IBGE PNAD Contínua supplementary-module aggregado (annual, not the core quarterly release) — not yet identified/confirmed.

---

## Tier 2 — Consumed data (placeholders, pending other agents)

Thin, for the same reason as inflation's inventory: this agent mostly supplies rather than consumes.

### From the economic activity agent
- Output gap / potential output estimate — useful to help interpret whether a given unemployment-gap reading is demand-driven (cyclical, closable by policy) or supply-side (structural, a NAIRU shift) — the labor-market mirror of the same ambiguity Gordon (1997, bibliography cluster 3) raises about the NAIRU itself moving over time.
- GDP/value-added growth — needed alongside this agent's own hours/employment data (§1-§3) to eventually compute a unit labor cost series (§6) or a labor-productivity read, complementing (not duplicating) `economic_activity_data_inventory.md`'s own productivity section, which currently only has BCB's and FGV/IBRE's static report snapshots.

### From a future fiscal agent
- Minimum wage policy decisions and the Previdência/BPC indexation rule — the policy driver behind §7's proposed minimum-wage series; without it, the agent can record the level but not the political-economy reasoning behind a given adjustment (echoing how `inflation_data_inventory.md` flags the same "series exists, policy driver doesn't" gap for administered prices).

### From a possible future global/markets agent (not yet scoped at all)
- Not much identified yet — the labor market agent is unusually domestic-facing relative to the other three agents built so far, which all have a meaningful international/cross-country component (exchange rate peers, DM/EM inflation comparison, world commodity shocks). Flagged here only for completeness, not because a specific gap was identified.

---

## Gap summary (Tier 1 only — Tier 2 gaps are dependencies on unbuilt agents, not data gaps per se)

| Priority | Gap | Category |
|---|---|---|
| High | No regional/state-level PNAD breakdown — blocks any Brazil replication of the wage curve (bibliography cluster 5) entirely, not just a nice-to-have | §1 |
| High | No vacancy/job-openings data for the Beveridge curve — may be a genuine data-availability gap, not just a pipeline backlog | §5 |
| Medium | No minimum wage series — small and cheap to build, surprising given its institutional weight (labor + fiscal) | §7 |
| Medium | No NAWRU/NAIRU estimate computed — Borges (2022) methodology fully specified, purely an implementation gap | §6 |
| Medium | No informality rate or unemployment rate computed as standalone derived series, despite raw components already existing | §6 |
| Low | No unionization rate series — needed as a Borges (2022) NAWRU control variable | §8 |
| Low | `pnad` defaults to 2024 → today despite PNAD Contínua existing since 2012 | §1 |
| Low | `caged` defaults to a 24-month window despite SGS history back to 1992 | §4 |
| Low | No unit labor cost series computed (same gap restated from `inflation_data_inventory.md` §6) | §3, §6 |

---

## How to update this inventory

**Tier 1:** when a new owned table/series is built (a minimum wage lookup table, a computed informality/unemployment rate, a NAWRU estimate, a regional PNAD extension), update the relevant section and remove/adjust the corresponding gap-summary row.

**Tier 2:** when economic activity's productivity work matures or a fiscal agent gets scoped, replace the placeholder bullets with actual table/column references, mirroring the convention in the other three inventories.
