# Inflation — Conceptual Map

**Status (2026-10-22):** Partes 1–4 aprovadas pelo usuário em 2026-10-22 (central questions,
horizon, upside and downside, data list, outputs IN-S1 to IN-S10, and the pass-through row as an
input), with the boundaries of the first batch of seven agents (`SISTEMA_AGENTES.md` III.III.vii).
Layer 1 of this agent's literature comes after the first joint cycle, which runs without literature.

**What this file is.** This is the inflation agent's contract with the rest of the system. It says
what every report must answer (Part 1, central questions), what moves Brazilian consumer inflation
(Part 2), what this agent tells the others matters TO IT (Part 3, outputs), and what the others told
this agent matters TO THEM (Part 4, inputs). Part 5 is the index of concepts. In the first joint
cycle the agent runs **without literature** (`PLANO_AGENTES.md` (I)): it reads this map, its data
snapshot F(A) and the Structural Model, and nothing else. So this map has to stand on its own: every
mechanism the agent needs in that cycle is written here, in textbook form, without citing papers and
without historical numbers. A historical pattern ("food always rises in the first quarter", "the
tariff flag always turns in May") is data, never memory: it comes out of a G over the cycle's A,
with the window stated, or it is not written (`PRINCIPIOS_AGENTES.md` I.II.ix).

**How the parts connect to the rest of the vault.** `[[concept]]` links go to `concepts/`; a name in
`code` font is either a MySQL table or a concept with no page yet (concepts are listed in Part 5).
"Data" names tables of this agent's list (`SISTEMA_AGENTES.md`, section V.III). The
Structural Model's coefficients are named by the keys that `modelo.listar()` prints (`I.IS.is2` and
so on); their values are read in each cycle, never copied into this file.

**Outputs and inputs.** An output of agent A to agent B is what A tells B is important for A, coming
from B. An input of A from B is what B told A is important for B, coming from A. So this agent's
outputs (Part 3) are the other agents' inputs from inflation, and this agent's inputs (Part 4) are
the other agents' outputs to inflation. Rows of this map carry the prefix **IN**: `IN-S#` for
outputs (saídas), `IN-E#` for inputs (entradas). A row is a request; the content flows the other way.
An input gives emphasis and tells the agent what to flag; it never limits the analysis.

**Two layers.** What is written here is the **fixed** layer: what matters every cycle. On top of it,
each cycle has a **dynamic** layer, set by the theses of that cycle's reports. The dynamic layer lives
in the reports, not in this file.

**Data rule** (`SISTEMA_AGENTES.md` I.III.ix–x, III.III.vii, V.III). *Endogenous*: the IPCA and
IPCA-15 tables — the aggregates with cores and diffusion, the index as the IBGE publishes it, the
subitem and item decomposition, the BCB's classification of each subitem — and the IC-Br in reais,
the form in which commodities and the exchange rate reach the IPCA. The IPCA tables were TWA in the
monetary-policy list (V.II.iv) and are now this agent's. *Endogenous of another agent*, read for
consultation, with no conclusion drawn here — the position comes through Part 3: the exchange rate
(FX agent), the target and the Copom's projections (monetary policy), the output gap, services
activity and, provisionally, the labour market (activity), the Focus and the QPC (expectations),
Brent and the IC-Br in dollars (external). No TWA and no exogenous table: every table of the list now
has an agent. The table-by-table list, with why each table matters to this agent, is V.III.

---

## Part 1 — Central questions: what every report answers

**Approved by the user, 2026-10-22.** The questions are the floor, not the ceiling: the agent is expected to go
beyond them — new insights, alerts, anything the data or the other agents' reports raise. They are
kept in Portuguese, the language of the report.

The agent does not describe the month's IPCA print: it separates what is shock from what is trend,
says how much of today's inflation will propagate, and lists what is coming to the index before it
shows up there. Those three readings are what the monetary-policy agent needs (the Copom accommodates
the first round of a shock and reacts to the second), and they are what shape the distribution
around the model's central.

| # | Question | What the answer covers | Where to look |
|---|---|---|---|
| Q1 | O que explica a inflação corrente: quanto é choque e quanto é tendência? | The latest IPCA and IPCA-15 by the four groups and by subitem; cores, diffusion and underlying services against the headline; whether the pressure is concentrated in a few items (a relative-price shock) or spread across the basket; the seasonal pattern of the month, measured, not remembered | 2.1, 2.5–2.7 |
| Q2 | Quão persistente é a inflação, e o que a propaga? | Inertia and formal indexation, expectations against the target, wages and the gap behind services; whether a shock is passing through once (first round) or feeding into other prices and wages (second round) | 2.2, 2.3, 2.4 |
| Q3 | Que pressões estão chegando ao IPCA, grupo a grupo? | What is in the pipeline and not yet in the index: the exchange-rate path and its pass-through, commodity and food prices, the calendar of administered adjustments and tax changes, the climate, the demand gap; for each, which group it reaches, in which direction and when | 2.4–2.8 |
| Q4 | Qual o cenário prospectivo para o IPCA? | The report's thesis on the horizon below: central from the Structural Model's base scenario, distribution from the agent's tempero; the four groups' contribution to the central and where the asymmetry sits; where the path differs from the Copom's latest projection and from the Focus, and why | report §1, Part 2 |

- Q1 is about the **level and composition** of what has already been printed; Q2 about **how much of it
  stays**; Q3 about **what has not been printed yet**. Q4 puts them on the model's quarters.
- The Copom's relevant horizon falls today on the last of the model's six quarters; the agent's IPCA in
  that quarter is the number the monetary-policy agent sets against the Copom's projection.

### The horizon — approved by the user, 2026-10-22

The system's theses are per quarter of the Structural Model, six quarters from the current one, with
the variable measured at the close of the quarter (`SISTEMA_AGENTES.md` III.III.i).

1. **The thesis variable is the IPCA accumulated over 12 months, at the close of each of the six
   quarters** — the 12-month IPCA published for March, June, September and December. It is what the
   model produces (`ipca_12m`, "IPCA acumulado em 12 meses, no fim do trimestre"), what the continuous
   target is checked against month by month, what the Copom's projection and the Focus are written in,
   and what the expectations equation (E) of the model reads. One variable, full format: central, base
   range with probability, upside and downside tails with probability, asymmetry.
2. **The four groups — serviços, alimentação, bens industriais, monitorados — go with the thesis only
   as a decomposition of the central, not as four more theses.** For each quarter the report gives the
   model's contribution of each group to the 12-month IPCA (in p.p., `ipca_12m_servicos`,
   `ipca_12m_alimentacao`, `ipca_12m_industriais`, `ipca_12m_monitorados`, plus an aggregation residual
   while the window still holds observed quarters, all printed by `modelo.rodar()`) and says in which
   group the agent places the asymmetry of the headline distribution (where the upside tail would come
   from, where the downside would). No separate ranges or probabilities per group. *To revisit after
   the first joint cycle.*
3. **The central is the model's base scenario in every quarter, without adjustment**
   (`SISTEMA_AGENTES.md` IV.ix). In round 1 the agent runs the model with the exogenous paths it
   assumes; from round 2 on, the central comes from the joint run P, where each exogenous path is the
   one written by the agent with its tutela, as set in the "Exógenas" tab of `data_tracker.xlsx`
   (IV.ii, IV.vi). The distribution around it is the agent's. Every round, the agent writes its
   thesis by quarter (and the base path of any exogenous it writes) in
   `obsidian/ciclos/<date>/caminhos/inflacao_<r1|r2|rf>.json`; a path for an exogenous outside its
   tutela does not enter the P and is logged as a divergence, answered by the agent with the tutela in
   the next round.
4. **Scoreboard:** for each quarter that closed since the last cycle, the band in which the published
   12-month IPCA of the quarter's last month fell (it is published early in the following month;
   until then the quarter is not scored). For the four groups, the error of the central, without bands.
5. **Upside and downside:** upside is the IPCA above the central, downside below it — position only,
   with no judgement built in; the asymmetry is P(upside) − P(downside) (III.III.i). The report says in
   words whether a tail is good or bad for Brazil when it matters. Usually the upside is the bad one,
   but not always: a downside that comes from a tax cut, a frozen administered price or a subsidy
   leaves the underlying pressure unchanged and is often a deferred cost; a downside that comes from a
   sharp fall in demand is not good news for the other theses.
6. **The Selic, the exchange rate, the gap and expectations are not this agent's thesis variables.**
   They are endogenous variables of other agents, solved by the model in the same run; this agent never
   fixes them to reach an inflation path (`SISTEMA_AGENTES.md` IV.ix).

---

## Part 2 — Causal skeleton: what moves Brazilian consumer inflation

Section 2.1 is the accounting — how the index is built and read; 2.2–2.4 are what makes inflation
persist or build from inside (inertia, expectations, demand); 2.5–2.7 are the price shocks that come
from outside the domestic cycle (the exchange rate, commodities and food, administered prices); 2.8 is
how the Selic reaches all of this. At the end, a table of what the Structural Model carries, group by
group, and what it does not.

### How the model carries inflation (read this first)

Equation (I) of the Structural Model is a Phillips curve in four groups, in **inflation of the
quarter** (not annualized), each with its own equation, summed with the IPCA weights into the
headline; the 12-month figure is the four quarters chained, not a forecast of its own. In every group
the forward-looking anchor is the Focus expectation of the **headline** IPCA 12 months ahead, from the
previous quarter, divided by four; its weight is the remainder, one minus the group's inertia terms,
so the anchor holds in the long run whatever the coefficients. Each group also carries quarter
dummies that sum to zero over the year: seasonality is in the quarterly path and washes out of the
12-month reading. In the loop, the IPCA feeds the expectations equation (E), expectations feed the
interest-rate rule (R) and back into all four groups; the rate reaches the gap (H) and the exchange
rate (F), and both come back to inflation. The agent sees each coefficient's key, median and 90%
interval with `modelo.listar()` in its G.

**This agent owns equation (I)**, so the multipliers on its coefficients (tempero (i)) are this
agent's to apply: another agent that thinks, say, pass-through to food is stronger than estimated
argues it through its outputs, and this agent decides and applies `I.IA.ia3` × m. Multipliers on the
other equations are their owners' (`SISTEMA_AGENTES.md` III.III.vii); this agent argues for them
through Part 3. The commodity paths that (I) consumes (`icbr_agr_usd`, `icbr_met_usd`) are written by
whoever has their tutela, as set in the "Exógenas" tab (proposal: the external agent).

| Group | Inertia | Demand | Exchange rate | Commodities | Other |
|---|---|---|---|---|---|
| Serviços | own last quarter `I.IS.is1` and own 4-quarter average `I.IS.is1b` | gap `I.IS.is2` | — | — | — |
| Alimentação | own last quarter `I.IA.ia1` | gap `I.IA.ia4` | depreciation in the quarter `I.IA.ia3` | IC-Br agriculture in US$ `I.IA.ia2` | — |
| Bens industriais | own last quarter `I.II.ii1` and own 4-quarter average `I.II.ii1b` | gap `I.II.ii5` | depreciation of the previous quarter `I.II.ii4` | IC-Br metals in US$, this quarter `I.II.ii2` and the previous `I.II.ii3` | — |
| Monitorados | own last quarter `I.IM.im1` | — | — | — | headline IPCA of the previous quarter `I.IM.im2` (indexation) |

### 2.1 The index, its four groups, cores and diffusion

- **Mechanism.** The IPCA is a weighted average of several hundred subitems. The BCB classifies each
  subitem as administered (monitorados) or free, and splits the free ones into food at home, industrial
  goods and services; the four groups behave differently because their prices are set differently
  (contracts and regulators, crop and world prices, world goods and the exchange rate, wages and local
  demand). A monthly print mixes three things the agent separates: the seasonal pattern of the month,
  a relative-price shock in a few items, and the general trend. Cores (by exclusion, trimmed means,
  double weighting) and the diffusion index exist to see the trend through the first two; underlying
  services strip the most volatile services out of the group the Copom watches most. The IPCA-15 is
  the earliest read of the month being collected.
- **Read:** [[core_inflation]], [[administered_prices]]; `relative_price_shock`, `diffusion_index`,
  `seasonality`.
- **Data:** `inflc_agregados` (headline, IPCA-15, the four groups, tradables and non-tradables, the
  BCB cores, diffusion, `ipca_12m`), `inflc_indice_geral` (the index as the IBGE publishes it, the
  exact 12-month window), `inflc_decomposicao` and `inflc_decomposicao_item` (subitem and item:
  monthly change, weight, contribution), `inflc_dim` (the BCB classification of each subitem,
  including underlying services and the core flags).
- **Model:** (I), the four groups summed with the IPCA weights; their quarter dummies.
- **Trap.** The monthly series are not seasonally adjusted, and annualizing a single month blows up
  the seasonal pattern and the noise. A core is information about the trend, not the trend: two cores
  that disagree are the reading, not a contradiction to resolve by picking one. A 12-month rate moves
  as much by the month that leaves the window as by the month that enters it — say which one moved it.

### 2.2 Inertia and indexation

- **Mechanism.** Part of today's inflation is yesterday's, because some prices are reset looking
  backward and some are indexed by contract or by rule to past inflation (rents, school fees, health
  plans, utilities, the minimum wage). Staggered price setting spreads any shock over several quarters.
  Inertia is what turns a one-off shock into persistent inflation, and what makes disinflation costly;
  it is highest in services and administered prices. Inertia and expectations share the weight in
  the model: the more backward-looking a group, the less the target pulls it.
- **Read:** [[inflation_persistence]], [[calvo_pricing]], [[administered_prices]]; `indexation`,
  `second_round_effects`.
- **Data:** `inflc_agregados` (the groups and cores over time), `inflc_decomposicao` (the indexed
  subitems: rents, school fees, health plans, utilities), `inflc_indice_geral`.
- **Model:** the inertia terms of (I): `I.IS.is1`, `I.IS.is1b` (services' persistence is the average of
  the last year, not the last quarter), `I.IA.ia1`, `I.II.ii1`, `I.II.ii1b`, `I.IM.im1`; indexation of
  administered prices to the headline, `I.IM.im2`.
- **Trap.** The administered-price equation is the model's weakest: its indexation coefficient has the
  wrong sign and an interval that straddles zero, because the headline it is indexed to contains the
  administered prices themselves, and its fit is low (see `listar`). Read its central with that in mind:
  an administered path that departs from it is tempero (ii) (2.7), and a judgement on the coefficient
  goes to the report's section 6. Inertia measured on 12-month rates sampled quarterly is inflated by
  the overlap of the windows; the model works in quarterly inflation for that reason.

### 2.3 Expectations and the target

- **Mechanism.** Price setters who expect inflation to return to the target set prices accordingly, so
  anchored expectations pull every group toward the target and shorten the life of a shock;
  deanchored expectations do the opposite and make the same shock more persistent. Expectations in
  turn respond to realized inflation, so a run of high prints can drag them away from the target —
  this is the loop the Copom guards against. In the model, the expectation of the headline is the
  common anchor of all four groups.
- **Read:** [[inflation_targeting]], [[nk_phillips_curve]], [[inflation_forecast_targeting]];
  `inflation_expectations_anchoring`.
- **Data:** endogenous of the expectations agent, for consultation: `expc_focus` (IPCA 12 and 24 months
  ahead, and the five components — livres, administrados, serviços, bens industrializados, alimentação
  no domicílio — since 2021), `expc_focus_periodo` (IPCA and components by calendar year, IGP-M),
  `expc_qpc` (the market's IPCA projections before each Copom); endogenous of monetary policy:
  `inflc_meta`.
- **Model:** the expectation term of (I), whose weight is the remainder after inertia; equation (E),
  where the realized 12-month IPCA (this agent's variable) moves the Focus.
- **Trap.** Expectations are the expectations agent's (`SISTEMA_AGENTES.md` I.III.x): this agent reads
  them and asks (IN-S9, IN-S10). The model anchors all four groups to the headline expectation, which
  forces relative prices to be constant in the long run; the Focus by component shows where the market
  expects relative prices to move, and is the evidence for a tempero on one group.

### 2.4 Demand: the output gap, the labour market and services

- **Mechanism.** When demand runs above potential, firms face rising marginal costs and room to raise
  margins, and prices accelerate. Services feel it most: they are labour-intensive and not traded, so
  their price follows local demand and unit labour costs. A tight labour market raises wages; wages
  growing above productivity raise unit labour costs and feed services inflation, and through income
  they sustain demand. Goods respond less to the local gap, because their prices are set against world
  prices and the exchange rate.
- **Read:** [[nk_phillips_curve]], [[sticky_wages]], [[natural_rate_of_unemployment]],
  [[divine_coincidence]], [[real_time_data]]; `unit_labour_costs`.
- **Data:** endogenous of the activity agent, for consultation: `pm_hiato_produto` (the BCB's output
  gap), `atv_pms` (services volume), and the labour market, which the activity agent holds
  provisionally: `mt_pnad` (unemployment, real habitual earnings, wage bill), `mt_desocupacao_retro`
  (the BCB's long seasonally adjusted unemployment series), `mt_caged` (formal employment, monthly).
- **Model:** the gap terms `I.IS.is2` (the strong one), `I.II.ii5`, and `I.IA.ia4` (close to zero:
  food does not respond to the gap). Wages are **not** in the model.
- **Trap.** The gap is the activity agent's thesis (IN-S5); this agent never fixes it. It is
  unobserved and revised, so the services reading should not hang on one gap number. Wage pressure is
  a tempero (ii) only for the part the gap does not already carry — wages and the gap move together,
  and adding both for the same quarters is double counting. Wages respond to past inflation too, so
  rising wages after an inflation burst are partly propagation (2.2), not new demand.

### 2.5 The exchange rate and pass-through

- **Mechanism.** A depreciation raises the domestic price of imported goods, of imported inputs and of
  commodities priced in dollars. The pass-through to consumer prices is partial and spread over time:
  fastest in food and fuels, slower in industrial goods, small in services except through costs and
  indexation. It is larger when the move is seen as persistent, when demand is strong enough for firms
  to pass costs on, when inflation is already high and when expectations are loosely anchored; a
  transitory spike is mostly absorbed in margins. Through indexation, what passes to the headline
  returns later in administered prices and contracts.
- **Read:** [[exchange_rate_pass_through]], [[ppp_balassa_samuelson]]; `tradables_vs_nontradables`.
- **Data:** endogenous of the FX agent, for consultation: `cmb_ptax`; endogenous: `comm_icbr` (the
  IC-Br in reais, where commodities and the exchange rate arrive together, the form in which they
  reach the IPCA).
- **Model:** `I.IA.ia3` (depreciation in the same quarter, food) and `I.II.ii4` (previous quarter,
  industrial goods). Administered prices carry no exchange-rate term: the pass-through of a depreciation
  to fuels, energy and medicines is outside the model.
- **Trap.** The exchange-rate path is the FX agent's thesis, and whether a move is persistent comes from
  it (IN-S1, IN-S2); this agent judges how much of that path reaches prices. Pass-through to fuels and
  other administered prices is a tempero (ii); a stronger or weaker pass-through to food or industrial
  goods than estimated is a tempero (i) on `I.IA.ia3` or `I.II.ii4`, never (ii) — that channel is in the
  model. The model reads the average exchange rate of the quarter through a bridge from quarter-close
  rates, so the timing inside a quarter is approximate.

### 2.6 Commodities, food and climate

- **Mechanism.** Food at home is driven by supply: crop prices in world markets, the exchange rate,
  input costs (fertilizer, diesel), the domestic harvest and the climate, and animal-protein cycles.
  Demand for staples is inelastic, so supply shocks move prices a lot and the group is the most volatile
  and the most seasonal of the four. Industrial goods follow world goods and metal prices in dollars,
  with a lag through the production chain. Energy commodities reach consumers through administered
  fuels (2.7). An El Niño or La Niña episode changes harvests with a lag, and the sign depends on the
  crop and the region.
- **Read:** [[food_inflation_drivers]], [[exchange_rate_pass_through]]; `supply_shocks`.
- **Data:** endogenous: `comm_icbr` (the IC-Br and its agriculture, metal and energy sub-indices in
  reais); endogenous of the external agent, for consultation: `comm_icbr_usd` (the same in dollars),
  `comm_brent`. There is no climate series in the list: a climate or harvest reading is stated as a
  premise, with the gap declared.
- **Model:** `I.IA.ia2` (agriculture in US$, food) and `I.II.ii2`, `I.II.ii3` (metals in US$, industrial
  goods); the agriculture and metal paths are exogenous variables of the model (`icbr_agr_usd`,
  `icbr_met_usd`), written by whoever has their tutela in the "Exógenas" tab. Climate, the domestic
  harvest, animal-protein cycles and oil are **not** in the model.
- **Trap.** The commodity paths in dollars are the external agent's thesis (IN-S7); this agent judges
  their effect on food and goods. A food shock is the textbook first-round shock: the question for Q2 is whether it spreads
  (diffusion, services, expectations), not its size. Food's quarter dummies are the largest of the four
  groups, so a quarterly food path is read net of seasonality, and a seasonal claim comes from a G.

### 2.7 Administered prices, energy and taxes

- **Mechanism.** A large share of the IPCA is set by contract or regulator (its weight is read in the
  data, `inflc_dim` with `inflc_decomposicao`), each item with its own rule: fuels follow the state
  company's pricing, which tracks oil and the exchange rate with a policy lag; residential electricity follows annual tariff revisions plus a tariff flag that rises with the
  cost of generation (low reservoirs, thermal dispatch); health plans and medicines follow annual
  adjustments set by their regulators, largely indexed to past inflation; public transport, water and
  other utilities follow local decisions and contracts. Taxes on fuel and energy (federal and state)
  move these prices by decree. Most of the group is therefore predictable from a calendar and a
  formula, and the rest is policy. A cut by decree lowers measured inflation once and does not change
  the pressure underneath; its reversal comes back later.
- **Read:** [[administered_prices]], [[inflation_persistence]], [[exchange_rate_pass_through]];
  `energy_tariff_flag`.
- **Data:** `inflc_decomposicao` and `inflc_decomposicao_item` (gasoline, diesel, bottled gas,
  residential electricity, health plans, pharmaceuticals, public transport, water — by subitem and item
  code), `inflc_dim` (which subitems are monitorados), `comm_icbr` (energy sub-index in reais);
  endogenous of the external agent: `comm_brent`, `comm_icbr_usd` (energy sub-index in dollars).
- **Model:** (I) monitorados, inertia `I.IM.im1` and indexation `I.IM.im2` only. Oil, the exchange
  rate, the tariff flag, regulators' decisions and taxes are **not** in the model: they are tempero (ii),
  each with its indicator, direction, size and duration.
- **Trap.** This is where most of the agent's tempero (ii) lives, and where the evidence is a calendar
  of decisions that the data in F(A) does not carry: the agent says what it is assuming about each
  decision, and asks the fiscal agent for tax measures (IN-S6) and the monetary-policy agent for the
  Copom's own assumptions (IN-S4). The tariff flag and fuel prices can reverse within the horizon:
  a flag that raises a quarter usually gives back later, so a level change and a transitory swing are
  written apart.

### 2.8 The Selic, through the loop

- **Mechanism.** Monetary policy reaches inflation with long lags, through demand (credit and income,
  hence the gap and services) and faster through the exchange rate (goods and food), and through
  expectations. A tightening today mostly affects inflation several quarters ahead.
- **Read:** [[monetary_transmission_lags]], [[inflation_forecast_targeting]], [[taylor_rule]].
- **Data:** endogenous of monetary policy, for consultation: `pm_copom_projecoes` (the Copom's IPCA
  projections, reference and alternative scenarios, by quarter), `inflc_meta`.
- **Model:** (R) sets the Selic from the expectations deviation from target; the Selic reaches (H)
  through the real curve and (F) through carry, and both come back to (I). The inflation central of a
  run already contains the Copom's reaction as the model estimates it.
- **Trap.** The Selic path is the monetary-policy agent's (IN-S3); this agent does not argue the Copom's
  decision. With long lags, today's inflation is not the effect of today's Selic. The Copom's projection
  is conditional on paths set by its governance, not its forecast; the comparison in Q4 says which
  conditioning differs.

### What the model does not carry, in one place

Each item below is a tempero (ii) when it matters in a cycle — indicator, direction, size, duration —
and never a tempero (i), which is reserved for channels the model has (`SISTEMA_AGENTES.md` IV.ix):

- **Oil and fuels** (2.7): `comm_brent` and the gasoline and diesel subitems.
- **Administered decisions and the tariff flag** (2.7): the subitems of `inflc_decomposicao`.
- **Taxes and subsidies on prices** (2.7): from the fiscal agent (IN-S6).
- **Climate and the harvest** (2.6): no series in the list; a stated premise, with the gap declared.
- **Wages beyond the gap** (2.4): `mt_pnad`; mind the double counting.
- **Expectations by component** (2.3): the model's anchor is the headline for all four groups.

And three known weaknesses of (I) that the agent reads as weaknesses, not as news: the administered
equation (2.2), food's insensitivity to the gap (2.4), and the exchange-rate bridge (2.5). Proposals to
change the specification go to section 6 of the report.

### Where the agent reads the data

Every table of the list through `obsidian/ciclos/<date>/dados/F_inflacao.md`, fixed for the cycle
(`analytics/agent_system/dados/inflacao.py`, which declares the tables of `SISTEMA_AGENTES.md`
V.III). Besides the reading of each table, the F carries the IPCA and the four groups by quarter (the
model's unit, and the scoreboard), the last month against the same month of the previous ten years
(the seasonal pattern, measured), and the administered prices item by item. The model through
`analytics/agent_system/modelo.py` in a G: `listar()` for the keys, `rodar()` for a scenario. The
agent does not read the Copom's documents in this phase; what the Copom said about inflation arrives
through IN-S4.

Type of each table (V.III): endogenous — `inflc_agregados`, `inflc_indice_geral`,
`inflc_decomposicao`, `inflc_decomposicao_item`, `inflc_dim`, `comm_icbr`; FX — `cmb_ptax`; monetary
policy — `inflc_meta`, `pm_copom_projecoes`; activity — `pm_hiato_produto`, `atv_pms`, `mt_pnad`,
`mt_desocupacao_retro`, `mt_caged`; expectations — `expc_focus`, `expc_focus_periodo`, `expc_qpc`;
external — `comm_icbr_usd`, `comm_brent`.

---

## Part 3 — Outputs: what this agent tells the others matters to it

**Approved by the user, 2026-10-22.** What this agent needs from each of the other six agents, every
cycle. Each row becomes an input of that agent's map (its Part 4).

### 3.1 To FX

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| IN-S1 | **The exchange-rate path and whether the move is persistent or transitory**: the thesis by quarter (PTAX at the close), with the FX agent's judgement on persistence | Pass-through depends on persistence; a transitory spike is absorbed in margins, a level shift reaches food, goods and, through fuels and indexation, administered prices | A move the FX agent classifies as persistent, in either direction | 2.5, 2.6, 2.7 |
| IN-S2 | **Risk of a relevant depreciation** (the upside tail of the FX thesis, a higher PTAX, and what drives it), and whether a move is global or idiosyncratic | A depreciation with a domestic risk premium tends to come with weaker expectations, which raises pass-through and persistence; it is the main source of this agent's upside tail in goods and food | The FX upside tail gains probability, or an idiosyncratic depreciation dominates the month | 2.3, 2.5 |

### 3.2 To monetary policy

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| IN-S3 | **The Selic path** (the thesis, at each quarter close and meeting by meeting for the next two quarters) | The Selic reaches inflation through the gap and the exchange rate with long lags; it is the loop that pulls the central back toward the target | The thesis moves by a step or more against the previous cycle | 2.8 |
| IN-S4 | **What the Copom projects for inflation and on which assumptions**: the reference-scenario projection by quarter, the administered-prices projection, and the conditioning paths it states (oil, the tariff flag, the exchange rate), from the comunicado, the ata and the RPM | This agent does not read the Copom's documents; Q4 compares its path with the Copom's, and the Copom's assumptions on administered prices are the best public calendar of those decisions | The Copom changes an assumption on administered prices or the flag, or its projection at the relevant horizon moves | 2.7, 2.8, Q4 |

### 3.3 To activity

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| IN-S5 | **The output-gap path** (the thesis) and **where the demand pressure is**: services against goods, household consumption, income | The gap is the demand channel of services and industrial goods; services are the most persistent group and the one the Copom watches most | The gap changes sign in the horizon, or services activity diverges from the gap | 2.4 |

### 3.4 To fiscal

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| IN-S6 | **Measures that act directly on prices**: taxes on fuel and energy (federal and state), subsidies, administered-price interventions, the minimum-wage rule, social transfers — with dates | They move the IPCA by decree, outside the model, and often come back later; they are tempero (ii) and the agent needs their timing | A measure announced, approved or expiring inside the horizon | 2.7, 2.4 |

### 3.5 To external

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| IN-S7 | **The paths of the agricultural and metal commodity prices in dollars** (`icbr_agr_usd`, `icbr_met_usd`), by quarter, base and tails | They are exogenous inputs of the Phillips curve: food and industrial goods (who writes them: the "Exógenas" tab) | A move that changes the quarter's path by more than the agent's base range absorbs | 2.6 |
| IN-S8 | **Oil and global energy**: the Brent path and the state of the global goods and energy cycle | Oil reaches fuels and, through them, administered prices and transport costs; it is outside the model, so it is the agent's tempero (ii) | A sustained oil move, or a supply event | 2.7 |

### 3.6 To expectations

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| IN-S9 | **The path of the 12-month-ahead IPCA expectation** (the model variable, the expectations agent's thesis) and **the anchoring reading**: whether long horizons stay at the target | Expectations are the anchor of all four groups in the model; a deanchoring makes every shock more persistent | Long-horizon expectations move away from the target | 2.3 |
| IN-S10 | **Expectations by component** (services, administered, food, goods) against the headline | The model anchors all groups to the headline expectation; where the market expects relative prices to move is the evidence for a tempero on one group | One component's expectation moves while the headline does not | 2.3, 2.7 |

---

## Part 4 — Inputs: what the others told this agent matters to them

Mirror of the other agents' Part 3. The rest is filled when the other maps are adjusted to the batch
of seven (`PLANO_AGENTES.md`, Phase 8, item 5).

### 4.1 From monetary policy (approved by the user, 2026-10-22)

The pass-through row moves here from the FX map (its E3, mirrored as S3 in the monetary-policy map),
because the pass-through literature and the question are this agent's (`SISTEMA_AGENTES.md` IV.i).
The FX agent keeps telling the monetary-policy agent whether a move is persistent and whether it is
global or idiosyncratic; how far it reaches prices is answered here.

| # | Source row | What the monetary-policy agent needs | Why it matters to it | How this agent answers |
|---|---|---|---|---|
| IN-E1 | FX E3 / PM S3 | **Pass-through channel.** Which prices a depreciation reaches, and how fast: food, industrial goods, and administered prices through fuels, energy and medicines | The Copom projects free and administered prices separately, and their pass-through differs; it reacts to the second round, not the first | Q2 and Q3, channels 2.5 and 2.7: the model's coefficients `I.IA.ia3` and `I.II.ii4`, plus the tempero (ii) on administered prices, on the FX agent's path (IN-S1) |

---

## Part 5 — Concept index

Concept pages this agent reaches (the area has almost no literature yet; its layer 1 comes after the
first joint cycle, `PLANO_AGENTES.md` (VI)):

- [[core_inflation]], [[administered_prices]], [[inflation_persistence]] — the index, its groups and
  what persists (2.1, 2.2, 2.7).
- [[nk_phillips_curve]], [[calvo_pricing]], [[sticky_wages]], [[natural_rate_of_unemployment]],
  [[divine_coincidence]], [[real_time_data]] — demand, wages and the gap (2.4).
- [[inflation_targeting]], [[inflation_forecast_targeting]], [[taylor_rule]],
  [[monetary_transmission_lags]] — the target, the Copom and the loop (2.3, 2.8).
- [[exchange_rate_pass_through]], [[ppp_balassa_samuelson]] — the exchange rate (2.5).
- [[food_inflation_drivers]] — food and commodities (2.6); from
  [[inflation/synthesis/em_food_inflation (Goldman, 2026)]], the one source with a synthesis in this
  area so far (layer not decided).

Concepts with no page yet: `relative_price_shock`, `diffusion_index`, `seasonality`, `indexation`,
`second_round_effects`, `inflation_expectations_anchoring`, `unit_labour_costs`,
`tradables_vs_nontradables`, `supply_shocks`, `energy_tariff_flag`.
