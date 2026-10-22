# External — Conceptual Map

**Status (2026-10-22):** Parts 1–4 approved by the user on 2026-10-22 (central questions; thesis on
the seven exogenous variables, measured in the model's convention and written in three scenario
blocks; upside and downside; outputs). Part 4 is filled when the seven maps are approved.

**One agent, three blocks — and every report covers all three.** The user considered splitting this
area into two agents (the US and global conditions; commodities) and kept one (2026-10-22). The
condition is that nothing falls through: **every report has its own section for each of the three
blocks — US policy, risk and the dollar, commodities —, each with its reading, its scenarios and
its paths**, even when a block has no news (then the section says so, and why). Whether the area
splits into two agents is decided from the log of the first joint cycle.

**What this file is.** This is the external agent's contract with the rest of the system. It says
what every report must answer (Part 1, central questions), what moves the global environment as it
matters for Brazil and how each piece reaches Brazil (Part 2), what this agent tells the others
matters TO IT (Part 3, outputs), and what the others told this agent matters TO THEM (Part 4,
inputs). Part 5 is the index of concepts. The agent reads Parts 1–4 on every run.

**Scope.** "External" is the world as it reaches Brazil: US monetary policy and rates, US inflation
and activity, the global dollar, global risk appetite, commodity prices, and the policy cycle of the
emerging-market and Latin American peers. Brazil's own balance of payments, flows, positioning and
the BRL itself are the FX agent's; the Copom is the monetary-policy agent's; the CDS is data of the
fiscal agent, with this agent holding a voice on its global component (`SISTEMA_AGENTES.md`
I.III.ix); the IC-Br in reais, the form in which commodities reach the IPCA, is the inflation
agent's; the Focus and the QPC are the expectations agent's. The US expected-inflation curve is
this agent's (`SISTEMA_AGENTES.md` III.III.vii).

**No literature in the first cycle.** The first joint cycle runs without literature
(`PLANO_AGENTES.md`, I): this map and the cycle's F(A) are all the agent reads. So the map states
mechanisms in its own words and cites no paper, and it carries no historical number. Every
historical pattern the agent wants to use ("the dollar weakens when the Fed cuts", "commodities fall
when the dollar rises") is a G over the A, with the window stated, or it does not enter
(`PRINCIPIOS_AGENTES.md` I.II.ix). The `[[concept]]` links go to `concepts/`, which any agent may
read; a name in `code` font is a concept with no page yet (Part 5).

**Outputs and inputs.** An output of agent A to agent B is what A tells B is important for A, coming
from B. An input of A from B is what B told A is important for B, coming from A
(`SISTEMA_AGENTES.md` I.III.vii). This map labels its outputs **XS1, XS2…** and its inputs **XE1,
XE2…** (X for external), so they do not collide with the S/E rows of the FX and monetary-policy maps
when the mirrors are checked. A row gives emphasis and tells the agent what to flag; it never limits
the analysis.

**Two layers.** What is written here is the **fixed** layer. Each cycle adds a **dynamic** layer,
set by that cycle's theses: an agent whose thesis hinges on something asks for it in its report.

**Data rule** (`SISTEMA_AGENTES.md` I.III.ix–x, V.VI). *Endogenous*: the US rates, inflation,
expected inflation and labour market, the dollar indices, the S&P 500, the commodity prices in
dollars and the peers' policy and real rates. *Endogenous of another agent*: the LatAm currencies,
positioning, terms of trade and trade by partner (FX), the CDS (fiscal) and the QPC's external
block (expectations), read for consultation; the position comes from the owner. The table-by-table
list, with why each table matters, is V.VI.

**Which exogenous paths this agent writes** is set by the "Exógenas" tab of
`repository/agent_mapping/data_tracker.xlsx`, filled by the user (`SISTEMA_AGENTES.md` IV.ii); this
map does not assert it. The proposal on the table is the seven variables of Part 1. A path the agent
writes outside its tutela does not enter the P and is logged as a divergence; when another agent
writes a path different from this agent's for a variable under this agent's tutela, this agent
answers that divergence in the next round, and changes its path if the argument is good.

---

## Part 1 — Central questions: what every report answers

**Approved by the user, 2026-10-22.** The questions are the floor, not the ceiling. They are kept in
Portuguese, the language of the report. Q1 is answered in the US-policy section of the report, Q2 in
the risk-and-dollar section, Q3 in the commodities section; Q4 and Q5 cross the three.

The agent does not describe the world: for each block it says what it expects, what the market
prices, and where the two differ, and it ends every answer in the channel by which that reaches
Brazil.

| # | Question | What the answer covers | Where to look |
|---|---|---|---|
| Q1 | O que o Fed vai fazer, e para onde vão os juros americanos? | The agent's reading of the Fed's reaction function: US inflation against the Fed's objective and its persistence, the labour market, expected inflation; the policy path the agent expects against what the short end of the Treasury curve prices; the long end, the term premium and the real yield | 2.1, 2.2, 2.3 |
| Q2 | O ciclo financeiro global está a favor ou contra os emergentes? | The global dollar against developed and emerging currencies, risk appetite (the S&P 500), whether the LatAm currencies and the BRL move together (global) or apart, and where the peers are in their policy cycle | 2.4, 2.5, 2.7 |
| Q3 | O que as commodities relevantes para o Brasil vão fazer, e por quê? | Agriculture, metals and energy in dollars: demand (China), supply (weather, oil supply) and the dollar; which group drives the IC-Br; terms of trade as consequence | 2.6 |
| Q4 | Por quais canais o ambiente externo chega ao Brasil neste ciclo, e com que sinal? | For each block, the model variable that carries it and the agent who reads the effect (carry and the BRL → FX; commodities → inflation; long rates → whoever writes `rr_10a`; the CDS's global component → fiscal; the peers → monetary policy); what reaches Brazil outside the model | 2.8 |
| Q5 | Qual o cenário prospectivo para as variáveis externas do modelo? | The report's thesis: the base path of the seven exogenous variables by quarter, and the distribution around it, written as three scenario blocks (horizon below) | report §1, 2.1–2.6 |

### The horizon — approved by the user, 2026-10-22

**Thesis variables.** The paths of seven exogenous variables of the Structural Model — those this
agent has tutela over, per the "Exógenas" tab (the proposal is the seven below) —, in the exact
quarterly convention of `modelo.CONVENCAO`. The path must be typed in the convention the simulator
uses, or the model reads a different object:

| Key | Variable | Quarterly convention | Enters | Effect on Brazil inside the model |
|---|---|---|---|---|
| `ffr` | Fed funds, **effective** | average of the quarter's **last month** (FRED FEDFUNDS, in `diferenciais_juros`); not the target midpoint of `us_interest_rate`, not the quarter average | (F), through the carry `(Selic − ffr) ÷ vol`, in difference | higher → less carry → BRL weaker |
| `infl_us` | US CPI, change in the quarter | 100·Δlog from the last month of the previous quarter to the last month of this one; not annualized, not 12 months | (F), through the PPP offset (`infl_br − infl_us`, coefficient fixed at 1) | higher → mechanically less nominal depreciation |
| `dxy_em` | dollar against emerging currencies | quarter close (`cmb_dollar_index_em`) | (F), in difference | higher → BRL weaker |
| `sp500` | S&P 500 | quarter close (`cmb_equity_us`) | (F), log return | conditional sign, see 2.5 |
| `icbr_usd` | IC-Br in dollars, total | the last month of the quarter (`comm_icbr_usd`; the monthly index is already a monthly average) | (F), log return | higher → BRL stronger |
| `icbr_agr_usd` | IC-Br agriculture in dollars | average of the quarter's three months | (I), food | higher → more food inflation |
| `icbr_met_usd` | IC-Br metals in dollars | average of the quarter's three months | (I), industrial goods, current and lagged | higher → more industrial-goods inflation |

None of the seven enters the IS curve (H): the external environment reaches the output gap in the
model only through the anchor `rr_10a`, whose path this agent does not write (2.2, 2.8).

**Six quarters**, from the current one (in a cycle of October 2026: 4T26 to 1T28), as for every
agent (`SISTEMA_AGENTES.md` III.III.i). **Each variable is measured in its `CONVENCAO` convention**,
not strictly at the quarter close: four of the seven are not closes (`ffr`, `infl_us`,
`icbr_agr_usd`, `icbr_met_usd`), and measuring them any other way would score the agent on an
object the model does not read (approved, III.III.vii).

**Three scenario blocks, seven variables — each block a section of its own in every report.** The
seven are not independent, and seven separate distributions invite seven stories that contradict
each other. The agent writes **one set of scenarios (base, upside, downside, with probabilities)
per block**, and every variable of the block takes its value in each scenario. No block may be
skipped: a block with no news gets its section anyway, saying why its paths did not move.

1. **US policy** — `ffr` and `infl_us` (Q1; Part 2, 2.1–2.3). In each scenario the Fed path is what
   the agent's reading of the Fed's reaction function implies for that inflation path; a Fed behind
   or ahead of its own reaction is a stated part of the scenario, never an accident of two tables.
2. **Risk and the dollar** — `dxy_em` and `sp500`, always together (Q2; 2.4, 2.5, 2.7; 2.5 explains
   why the model punishes moving one alone). The fiscal agent's CDS path is checked against this
   block (Part 3, XS5).
3. **Commodities** — `icbr_usd`, `icbr_agr_usd`, `icbr_met_usd`, written from paths for agriculture,
   metals and energy (Brent) (Q3; 2.6). Two consistency rules, both measured by a G and never
   assumed: the total moves as its sub-indices combine (the combination is estimated on the A, with
   the window stated, since the IC-Br weights are not in the database); and the conventions differ
   — the total is the last month of the quarter, the sub-indices the quarter average — so a path
   that turns inside a quarter shows up in the total before it shows up in the averages.

The FOMC meeting by meeting, as the monetary-policy agent does for the Copom, is left for later
(no FOMC dates and no Fed funds futures in the database).

**Central and distribution** (`SISTEMA_AGENTES.md` IV.vi, 2026-10-22). This agent has no
endogenous variable in the model, so **the central is its own base path**, by quarter, in the
`CONVENCAO` convention, and the band and the tails around it are also its own. Every round it
writes `obsidian/ciclos/<date>/caminhos/externo_<r1|r2|rf>.json` with the base paths and the thesis
(the contract is in the docstring of `analytics/agent_system/consolidacao.py`); the P of the round
runs the model with the paths of whoever has the tutela of each variable. Consequences:
- No equation produces these variables, so there is no model central to defer to, in any round:
  the scoreboard measures the agent directly.
- The two-step premises (IV.ix) apply in a reduced form. Step 1 is the base path and the upside and
  downside paths of each block. Step 2 (i), a coefficient multiplier, belongs to the owner of the
  equation the channel moves (a stronger `dxy_em` effect on the BRL is applied by the FX agent, on
  the (F)); this agent argues for it through its outputs, never applies it (III.III.vii). Step 2
  (ii) is where this agent's qualitative factors live (2.2, 2.6, 2.7, the channels outside the
  model).
- The report shows what the agent's scenarios do to the endogenous variables (the P, and its own
  runs of `modelo.rodar` by G), as information for the owners, not as its thesis.

**Scoreboard.** For each quarter that closed since the last cycle, and for each of the seven, the
band in which the realized value fell, computed in the `CONVENCAO` convention (a G until the F
carries it).

**Upside and downside** (`SISTEMA_AGENTES.md` III.III.i, 2026-10-22). The tails are positions
only: **upside** is above the central, **downside** below; the asymmetry is P(upside) −
P(downside). Neither is "good" or "bad" by definition. When it matters, the report says in words
whether a tail is good or bad for Brazil, and through which channel — and for these variables the
answer often depends on the channel:

| Variable | Upside means | For Brazil, inside the model | Outside the model, worth saying |
|---|---|---|---|
| `ffr` | higher Fed funds | less carry, a weaker BRL | tighter financial conditions for emerging markets; less room for the Copom |
| `infl_us` | higher US inflation | mechanically a stronger BRL (PPP offset) | bad through the Fed: a higher `ffr` path, which the US-policy block must carry |
| `dxy_em` | stronger dollar against emerging currencies | a weaker BRL | dollar commodity prices often weaker (a G decides whether in this episode) |
| `sp500` | higher S&P | holding the CDS and `dxy_em`, a weaker BRL; in the joint risk-on scenario, a stronger one (2.5) | risk-on usually compresses the CDS (fiscal's path) |
| `icbr_usd` | higher commodity prices | a stronger BRL | better terms of trade, exports and fiscal revenue |
| `icbr_agr_usd` | higher agricultural prices | more food inflation | the same move improves the terms of trade |
| `icbr_met_usd` | higher metal prices | more industrial-goods inflation | the same move improves the terms of trade |

The commodity block is where the reading splits: a broad fall in commodity prices is the downside
of all three indices, **bad for Brazil through the BRL** (terms of trade, the `icbr_usd` channel)
and **good through inflation** (the two sub-indices in the Phillips curve). The report says both,
and which one dominates the endogenous variables in the P. The same split holds for `infl_us`
(good for the BRL mechanically, bad through the Fed) and for `sp500` alone (2.5).

---

## Part 2 — Causal skeleton: what moves the global environment, and how it reaches Brazil

Sections 2.1–2.7 are the blocks; 2.8 is the table of how each one reaches Brazil.

### 2.1 The Fed's reaction function and the policy rate

- **Mechanism.** The Fed sets the policy rate against its two objectives, price stability, read on
  PCE inflation, and maximum employment. What decides is the inflation it expects against its
  objective, its persistence (services and wages more than goods) and how much slack the labour
  market has; guidance and the projections of its members shape the path the market prices. The
  short end of the Treasury curve prices the expected path plus a premium; the agent's own expected
  path is its thesis, and the difference to the market's is the room for surprise.
- **Read:** [[taylor_rule]], [[taylor_principle]], [[interest_rate_smoothing]],
  [[forward_guidance]], [[central_bank_communication]], [[information_effect]],
  [[monetary_policy_shocks]], [[natural_rate_of_interest]], [[real_time_data]].
- **Data:** `us_interest_rate` (the target midpoint and the short Treasuries), `diferenciais_juros`
  (the effective Fed funds, the model's `ffr`), `inflc_pce`, `inflc_cpi`, `expc_inflacao`,
  `mt_ces`, `mt_cps`, `mt_jolts`.
- **Model:** `ffr` in (F), through the carry `(Selic − ffr) ÷ vol`, in difference: a cut that holds
  moves the BRL in the quarter it happens and not afterwards.
- **Trap.** The target midpoint of `us_interest_rate` is not the model's `ffr`: the model reads the
  effective rate, averaged over the quarter's last month, so a move at a meeting in that month lands
  partly in that quarter and partly in the next. There is no futures or OIS series in the database:
  the market's path is read from the 1M–1Y Treasuries, which carry a premium; say so when the
  difference matters.

### 2.2 The US curve, the term premium and long rates abroad

- **Mechanism.** The long end is the expected path of the policy rate plus a term premium, and the
  premium moves with inflation uncertainty, fiscal supply and risk. US long yields are the world's
  discount rate: they co-move with long rates in other countries whatever their exchange-rate
  regime, so a rise in the US long end can raise Brazil's long real rate with no change in Brazil.
  The real yield (nominal minus expected inflation) is what competes with emerging-market assets.
- **Read:** [[term_premium]], [[financial_trilemma]], [[global_financial_cycle]],
  [[unconventional_monetary_policy]], [[natural_rate_of_interest]].
- **Data:** `us_interest_rate` (the whole Treasury curve), `expc_inflacao` (the expected-inflation
  term structure, from which a G builds ex-ante real yields).
- **Model:** outside the model — no US long rate is in it. It reaches Brazil through `rr_10a`, the
  10-year NTN-B, whose path is written by whoever has its tutela in the "Exógenas" tab (fiscal or
  monetary policy): this agent tells that agent how much of a move in `rr_10a` is the US long end
  (Part 4 will carry it), and asks back how much it attributes to it (Part 3, XS6). Qualitative
  tempero, step 2 (ii).
- **Trap.** A long-end move with a flat short end is a premium story, not a Fed story; reading it
  as a Fed signal puts it in the wrong block.

### 2.3 US inflation and activity

- **Mechanism.** US inflation splits into goods, services and housing, with different persistence;
  wages against productivity and the tightness of the labour market (openings, quits, unemployment)
  tell how much of it is demand. Expected inflation tells whether the Fed's objective is anchored.
  Activity is read through the labour market and productivity: the database has no US GDP,
  industrial production, retail or survey data.
- **Read:** [[core_inflation]], [[nk_phillips_curve]], [[natural_rate_of_unemployment]],
  [[sticky_wages]], [[inflation_targeting]], [[real_time_data]].
- **Data:** `inflc_cpi` (headline, core, goods, services, shelter), `inflc_pce` (headline and core,
  the Fed's measure), `expc_inflacao`, `mt_ces` (payrolls, hourly earnings), `mt_cps` (unemployment,
  participation), `mt_jolts` (openings, hires, quits).
- **Model:** `infl_us` in (F), through the PPP offset `infl_br − infl_us` with its coefficient fixed
  at 1: higher US inflation means, mechanically, less nominal depreciation of the BRL. The effect
  that matters for Brazil goes through the Fed (2.1), and that link is not in the model: it is this
  agent's consistency rule inside the US-policy block.
- **Trap.** The model's `infl_us` is the CPI change in the quarter, not the 12-month rate the news
  quote and not the PCE the Fed targets; the agent reasons on PCE and core and writes the path in
  CPI, quarterly. The US data carry gaps from the 2025 appropriations lapse (October 2025 is missing
  in the CPS and in some CPI series): a 12-month change across that month is computed, not read.

### 2.4 The global dollar

- **Mechanism.** The dollar's cycle follows US rates relative to the rest of the world, US growth
  relative to the rest of the world, and risk appetite: in risk-off the dollar is the refuge. Against
  developed currencies (the DXY) it is mostly a euro and yen story; against emerging currencies it
  carries the risk-appetite and commodity stories as well, which is why the model reads the
  emerging-market index. The dollar also prices commodities: whether a stronger dollar is coming
  with weaker dollar commodity prices in the current episode is a G, not an assumption.
- **Read:** [[global_financial_cycle]], [[uip]], [[carry_trade]], [[international_risk_sharing]],
  [[currency_regimes]], [[risk_premium]].
- **Data:** `cmb_dollar_index`, `cmb_dollar_index_em`, `us_interest_rate`; for consultation, the
  LatAm currencies (`cmb_fx_latam`, FX's).
- **Model:** `dxy_em` in (F), in difference: a stronger dollar against emerging currencies weakens
  the BRL.
- **Trap.** The BRL is part of the emerging-market basket, so `dxy_em` contains a bit of the BRL; a
  move driven by Brazil can show up in the index. Whether a move is global or Brazilian is the FX
  agent's split (Part 3, XS1), not this agent's inference from the index.

### 2.5 Risk appetite and the global financial cycle

- **Mechanism.** A common global factor moves risky assets, credit spreads and capital flows
  across countries, and US monetary policy is one of its drivers. Emerging markets with floating
  currencies are exposed to it through flows and spreads; the BRL, liquid and carrying a high rate,
  tends to move more than its peers when the factor turns (a pattern the agent shows with a G, not
  from memory). The S&P 500 is the database's proxy for the factor.
- **Read:** [[global_financial_cycle]], [[risk_premium]], [[financial_trilemma]],
  [[capital_controls]], [[macroprudential_policy]], [[carry_trade]]; `global_risk_appetite`.
- **Data:** `cmb_equity_us`, `cmb_dollar_index_em`; for consultation, the CDS (`cmb_risco_pais`,
  fiscal's), positioning (`cmb_cot_fx`, FX's) and the LatAm currencies.
- **Model:** `sp500` in (F), as a log return, with a coefficient whose sign is **opposite** to the
  raw relation: holding the CDS and `dxy_em` fixed, a rising S&P weakens the BRL (capital competing
  for US equities); unconditionally, a rising S&P comes with a stronger BRL, because risk-on also
  compresses the CDS and weakens the dollar against emerging currencies. So a risk-off scenario
  written as "the S&P falls" alone makes the model appreciate the BRL. **Rule: `sp500` and `dxy_em`
  are written together, as one risk-appetite scenario, and the CDS path of the fiscal agent is
  checked against it (XS5).**
- **Trap.** The CDS is the price where global risk and Brazilian fiscal risk meet, and the database
  has no other country's CDS and no emerging-market spread index: the global component cannot be
  measured directly, only argued from `dxy_em`, the S&P and the LatAm currencies. The user's
  intention is that fiscal and external discuss the CDS together (I.III.ix); this agent states the
  global component it sees, the fiscal agent owns the path.

### 2.6 Commodities by group, and China

- **Mechanism.** Commodity prices in dollars are set by global demand, supply and the dollar, and
  each group has its own driver. **Metals** follow industrial demand, China above all (construction
  and infrastructure for iron ore). **Agriculture** follows harvests and weather (the El Niño cycle),
  stocks and Chinese imports. **Energy** follows oil supply decisions and global demand. Brazil is
  hit twice and in opposite directions: higher prices improve the terms of trade, the trade balance
  and the BRL, and raise food, industrial-goods and fuel prices at home. In dollars the index carries
  no exchange rate; in reais (how it reaches the IPCA) it carries the BRL, which is the FX agent's.
- **Read:** [[food_inflation_drivers]], [[balance_of_payments_approach]], [[administered_prices]];
  `terms_of_trade`. Pass-through to prices is the inflation agent's ([[exchange_rate_pass_through]]
  for the exchange-rate part).
- **Data:** `comm_icbr_usd` (total, agriculture, metals, energy), `comm_brent`; for consultation,
  the terms of trade (`cmb_termos_troca`) and exports by partner (`cmb_comex_pais`), FX's.
- **Model:** `icbr_usd` in (F) (higher → stronger BRL); `icbr_agr_usd` in (I), food;
  `icbr_met_usd` in (I), industrial goods, current and one quarter lagged. Energy is **outside the
  model**: it reaches the IPCA through fuels and administered prices, and the inflation agent reads
  it as tempero; this agent gives the Brent path (Part 4 will carry it), so no cycle has two oil
  paths.
- **Trap.** There is no China data in the database (activity, credit, property, import volumes):
  the China story is argued from metal prices and Brazil's exports to China, and the report says
  so. The IC-Br is monthly and published with a lag of about a month, so the first projected quarter
  usually has no observed month at all, and the agent's path starts from the last published month.

### 2.7 The policy cycle of emerging and Latin American peers

- **Mechanism.** The peers' policy rates and real rates show whether a move in Brazil's rates or
  currency belongs to a common cycle or to Brazil. When the peers ease while Brazil holds, Brazil's
  relative carry widens, and the reverse; the Copom's room against the Fed is also measured against
  how far the peers have moved. The peers' currencies (FX's data) are the comparison group for the
  global-versus-Brazil split.
- **Read:** [[financial_trilemma]], [[currency_regimes]], [[taylor_rule]], [[carry_trade]].
- **Data:** `inter_interest_rate` (policy rates of Mexico, Chile, Colombia and Peru),
  `cmb_real_rates` (ex-post real rates, Brazil included, on one method); for consultation,
  `cmb_fx_latam` (FX's).
- **Model:** outside the model. It reaches Brazil through the monetary-policy agent's reading of the
  Copom's room and through the relative-carry reading of the FX agent; qualitative tempero.
- **Trap.** The peers' real rates are ex-post (policy rate minus past 12-month inflation): a peer in
  disinflation looks tighter than it is. Argentina's series stopped in 2025 and is not a peer here.

### 2.8 How each block reaches Brazil

| Block | Model variable | Equation | Who reads the effect | Outside the model |
|---|---|---|---|---|
| Fed policy (2.1) | `ffr` | (F), carry | FX (the BRL), then inflation and monetary policy through the BRL | the Copom's room against the Fed (monetary policy) |
| US curve (2.2) | — | — | whoever writes `rr_10a` (fiscal or monetary policy, per the "Exógenas" tab) | long-rate co-movement; reaches the gap in the model only through `rr_10a` |
| US inflation and activity (2.3) | `infl_us` | (F), PPP offset | FX | external demand for Brazil's exports (activity) |
| Global dollar (2.4) | `dxy_em` | (F) | FX | dollar commodity prices (2.6) |
| Risk appetite (2.5) | `sp500` | (F) | FX | the CDS's global component (fiscal); flows and positioning (FX) |
| Commodities (2.6) | `icbr_usd`; `icbr_agr_usd`, `icbr_met_usd` | (F); (I) food, (I) industrial goods | FX; inflation | energy and fuels (inflation); terms of trade, exports and fiscal revenue (FX, activity, fiscal) |
| Peers (2.7) | — | — | monetary policy, FX | relative carry; the Copom's room |

The agent answers Q4 from this table each cycle: which rows moved, with what sign, and which owner
must hear it.

### Where the agent reads the data

The agent reads every table of its list through `obsidian/ciclos/<date>/dados/F_externo.md`, fixed
for the cycle (`analytics/agent_system/dados/externo.py`, which declares the tables of
`SISTEMA_AGENTES.md` V.VI, approved 2026-10-22).

---

## Part 3 — Outputs: what this agent tells the others matters to it

**Approved by the user, 2026-10-22.** What this agent needs from each of the others, every cycle. The
external variables do not depend on Brazil, so the list is short: what this agent needs is mostly
evidence on how the world is reaching Brazil, and the paths of the other owners that must be
consistent with its scenarios.

| # | To | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|---|
| XS1 | FX | **Global or idiosyncratic?** The FX agent's split of the BRL's recent move (its Q3), against the dollar indices and the LatAm peers | It is the direct evidence of whether the global block is what is moving Brazil; this agent should not infer it from `dxy_em`, which contains the BRL | The global component dominates, or the BRL moves against the global block | 2.4, 2.5, Q4 |
| XS2 | FX | **Flows and positioning as evidence of the global cycle in Brazil**: the financial FX flow and the speculative position in BRL futures | Tells whether the risk-appetite scenario is reaching Brazil through money actually moving, or only through prices | Flows or positioning turn against the risk-appetite scenario | 2.5 |
| XS3 | Monetary policy | **The Selic path** (its thesis) | Brazil's relative carry against the Fed and the peers, which decides whether Brazil gains or loses within the emerging-market carry trade | The Selic path diverges from the peers' cycle | 2.7, 2.1 |
| XS4 | Monetary policy | **How the Copom reads the external scenario** — its assessment, balance of risks and the external conditioning assumptions of the reference scenario | Tells whether this agent's scenario is already in the Copom's or would be news to it; this agent does not read the Copom's documents | The Copom changes its external assessment, or its conditioning departs from this agent's base | Q4, 2.1, 2.6 |
| XS5 | Fiscal | **The CDS path, and the part of its move the fiscal agent attributes to global risk** | In (F) the S&P and `dxy_em` effects are conditional on the CDS: the risk-appetite block and the CDS path must tell one story, or the model double-counts or cancels it | The CDS moves while `dxy_em` and the S&P do not (or the reverse) | 2.5 |
| XS6 | Whoever writes `rr_10a` (fiscal or monetary policy, per the "Exógenas" tab) | **The `rr_10a` path, and how much of it that agent attributes to US long rates** | Keeps the long-rate scenario of 2.2 consistent with the anchor that carries it into the gap | `rr_10a` moves with the US long end flat, or the reverse | 2.2 |
| XS7 | Inflation | **Which commodity paths the IPCA thesis depends on**: agriculture, metals or energy, and in which quarters | Tells this agent where precision on commodities pays; the commodity block is the one with the most variables | The inflation thesis hinges on a commodity tail | 2.6 |
| XS8 | Expectations | **The market's reading of the external environment** — the QPC's external-environment block and anything the expectations agent sees in the Focus that bears on it | The consensus against which this agent's external scenario is a view or a surprise | The QPC's external assessment shifts between meetings | Q2, Q4 |

**No fixed output to activity.** The flow goes the other way (external demand, commodity prices and
global rates reaching Brazil's activity), so the row belongs to the activity agent's map, as its
output to this agent. If the activity agent's reading of Brazil's exports turns out to be evidence
this agent needs (for instance on Chinese demand), the row is added in a dynamic layer first.

---

## Part 4 — Inputs: what the others told this agent matters to them

Mirror of the other agents' Part 3, filled when the seven maps are approved. Expected, from the
existing maps: from FX, the Fed path and the global dollar (FX map 2.3, 3.2); from monetary policy,
the Fed path and the global cycle (monetary-policy map 2.8, 3.2), which until now were TWA premises
of those two agents and, per the "Exógenas" tab, become paths this agent writes.

---

## Part 5 — Concept index

No literature is read in the first cycle; these are the concept pages the skeleton uses, which any
agent may read (`obsidian/concepts/`).

- **Fed and the policy rate:** [[taylor_rule]], [[taylor_principle]], [[interest_rate_smoothing]],
  [[forward_guidance]], [[central_bank_communication]], [[information_effect]],
  [[monetary_policy_shocks]], [[real_time_data]].
- **Rates and the curve:** [[term_premium]], [[natural_rate_of_interest]],
  [[unconventional_monetary_policy]], [[zero_lower_bound]].
- **Inflation and labour:** [[core_inflation]], [[nk_phillips_curve]],
  [[natural_rate_of_unemployment]], [[sticky_wages]], [[inflation_targeting]].
- **The global cycle and the dollar:** [[global_financial_cycle]], [[financial_trilemma]],
  [[capital_controls]], [[macroprudential_policy]], [[uip]], [[carry_trade]], [[risk_premium]],
  [[international_risk_sharing]], [[currency_regimes]].
- **Commodities and Brazil:** [[food_inflation_drivers]], [[administered_prices]],
  [[balance_of_payments_approach]], [[exchange_rate_pass_through]].
- **No page yet:** `global_risk_appetite` (the common factor behind risky assets, proxied here by the
  S&P 500), `terms_of_trade` (export over import prices, the channel by which commodities reach the
  BRL).
