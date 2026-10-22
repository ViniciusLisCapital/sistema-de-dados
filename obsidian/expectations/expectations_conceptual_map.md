# Expectations — Conceptual Map

**Status (2026-10-22):** Partes 1–4 aprovadas pelo usuário em 2026-10-22 (central questions, horizon,
outputs; Part 4, the mirror of the other maps' Part 3, filled on 2026-10-22). **The user registered that he still has
doubts about this agent** (`SISTEMA_AGENTES.md` III.III.vii): its existence and scope are reviewed
after the first joint cycle, on what its reports added that the other agents did not.

**What this file is.** This is the expectations agent's contract with the rest of the system. It
says what every report must answer (Part 1, central questions), what moves expectations in Brazil
(Part 2), what this agent tells the others matters TO IT (Part 3, outputs), and what the others told
this agent matters TO THEM (Part 4, inputs). Part 5 is the short index of concept pages. The agent
reads Parts 1–4 on every run and uses the concept pages to go deeper.

**Why the agent exists.** Expectations were TWA in the lists of the FX and monetary-policy agents
(`SISTEMA_AGENTES.md` I.III.xii: they are not monetary policy's). Since 2026-10-22 they have an
agent of their own: it reads what the surveys and the market expect, and it owns the expectations
variable of the Structural Model, the 12-month-ahead Focus inflation expectation that equation (E)
produces and that equations (I) and (R) consume.

**What this agent reads, in this plan.** The first joint cycle runs without literature (`PLANO_AGENTES.md`
I): this agent reads only this map, the concept pages it links and its data snapshot F(A). It has no
literature of its own yet, no asset-manager mental model and does not read the Copom's documents;
what the Copom said about expectations arrives from the monetary-policy agent (Part 3, XS2). So the
mechanisms below are written as the reasoning the agent applies, without sources, and **every
historical pattern the agent asserts comes from a G over the cycle's A, with the window stated, never
from memory** (`PRINCIPIOS_AGENTES.md` I.II.ix). Expectation data are shown as **expectation and
price, not forecast**: the agent never scores the survey or the curve against realized inflation
(no hit rate, no RMSE).

**How the parts connect to the rest of the vault.** `[[concept]]` links go to `concepts/`; a name in
`code` font is either a MySQL table or a concept with no page yet (listed in Part 5). "Data" names
tables of this agent's list (`SISTEMA_AGENTES.md`, section V.VII).
"Model" names the Structural Model's equation and variable that carry the channel, or says the channel
is outside the model and enters only as qualitative tempero of type (ii) (`SISTEMA_AGENTES.md`
IV.ix).

**Outputs and inputs.** An output of agent A to agent B is what A tells B is important for A, coming
from B. An input of A from B is what B told A is important for B, coming from A. This map labels its
rows with the prefix **X** (for expectativas): outputs **XS1…**, inputs **XE1…**, so the mirror in
the other six maps can be checked line by line. A row is a request; the content flows the other way.
An input gives emphasis and tells the agent what to flag; it never limits the analysis.

**Two layers.** What is written here is the **fixed** layer: what matters every cycle. On top of it,
each cycle has a **dynamic** layer, set by the theses of that cycle's reports. The dynamic layer lives
in the reports, not in this file.

**Data rule** (`SISTEMA_AGENTES.md` I.III.ix–x). *Endogenous*: the expectation tables (`expc_focus`,
`expc_focus_periodo`, `expc_focus_copom`, `expc_qpc`), classified by what the data are (surveys of
expectations), not by who reads them; the other agents consult them (decided 2026-10-22, III.III.vii).
*Endogenous of another agent*: the inflation target, the Copom's projections and the yield curves
(monetary policy), realized inflation (inflation), the exchange rate (FX), the CDS (fiscal): read for
consultation; this agent draws no conclusion about them, and the owner's position arrives through
Part 3. Two boundaries decided on 2026-10-22: the **inflation implied in the curve** is this agent's
conclusion, while the curve stays monetary policy's data; the **Selic path the curve prices** is
monetary policy's conclusion (its Q3). The US inflation expectation (`expc_inflacao`) is the external
agent's. No TWA and no exogenous table. The table-by-table list is V.VII.

---

## Part 1 — Central questions: what every report answers

**Approved by the user, 2026-10-22**, with two additions to Q1 and Q2. The questions are the floor,
not the ceiling. They are kept in Portuguese, the language of the report.

The agent does not describe the Focus: it says whether expectations are anchored and how far off
that is against history, what is moving them and in which pieces, where the survey and the market
disagree, and where the 12-month expectation goes over the six quarters.

| # | Question | What the answer covers | Where to look |
|---|---|---|---|
| Q1 | As expectativas de inflação estão ancoradas na meta? | The distance to the target at each horizon (12 and 24 months ahead; each calendar year from the current one to the last one the survey asks), and which horizons are moving. Anchoring is judged at the long horizons; the short ones carry the current shocks. **And how large today's de-anchoring is against history**: where the distance to the target, at each horizon, sits among all the readings since the series began, measured by the F or by a G with the window stated, never from memory | 2.1, 2.2, 2.7 |
| Q2 | O que está movendo as expectativas, e o movimento é de nível ou de ruído? | The driver of the recent revisions (realized inflation and its composition, the Copom, fiscal, the exchange rate, commodity and administered-price shocks), read across horizons; **the breakdowns of the survey**: inflation by component (free, administered, services, industrial goods, food at home) and GDP by sector and by demand component; whether the move is broad (median, mean, dispersion and fresh answers moving together) or a few respondents | 2.1–2.5, 2.9 |
| Q3 | Onde a pesquisa, o mercado e o Copom divergem, e o que isso diz da credibilidade? | Focus against the QPC, against the inflation implied by the curve and against the Copom's projection at the relevant horizon; whether the survey's own Selic and inflation paths are coherent with the target being met (the credibility test) | 2.2, 2.6, 2.8 |
| Q4 | Qual o cenário prospectivo para as expectativas? | The report's thesis on the horizon below: central from the Structural Model's base scenario, distribution from the agent's tempero; what the path implies for the Selic through the rule (R), stated as a fact of the model and not as a Selic view | report §1, 2.1 |

### The horizon — approved by the user, 2026-10-22

1. **The thesis variable is the model's expectations variable**: the median of the Focus survey for
   IPCA inflation over the **next 12 months**, smoothed series, 30-day calculation base, general
   consensus (`expc_focus`: `indicador = 'IPCA'`, `horizonte = '12m'`, `suavizada = 'S'`,
   `base_calculo = 0`, `tipo_calculo = 'geral'`), taken as the **average of the quarter**. It is
   `pi_e` in the simulator and `focus_12m` in the output of `modelo.rodar` and in the JSON of paths.
2. **Six quarters**, from the current one (`SISTEMA_AGENTES.md` III.III.i), one line per quarter.
3. **Measured as the quarter average, not the close** (the model's convention; an exception to
   III.III.i decided on 2026-10-22). The close of a weekly survey median differs from the quarter's
   average by an amount that is not small next to a typical quarterly move, so comparing a close
   with the model's average would score the conversion, not the thesis.
4. **The central is the model's base scenario, in every quarter**; from round 2 on, the one from the
   consolidation (P). The distribution around it is this agent's (IV.ix).
5. **Scoreboard**: for each closed quarter, the band in which the quarter's average of the variable
   above fell. Shown as an expectation, never as a forecast of inflation.
6. **Upside and downside** (III.III.i, 2026-10-22): upside is the expectation above the central,
   downside below it; position only, and the asymmetry is P(upside) − P(downside). The report says in
   words when a tail is good or bad for Brazil: an expectation rising away from a target below it is
   de-anchoring; one falling well below the target is de-anchoring too, the other way, and the report
   says so when it happens.
7. **Two readings every report gives without being thesis variables**, because they are what
   anchoring is judged on: the long-horizon calendar-year medians against the target, and the
   inflation implied by the curve (2.6, 2.7).

**How the tempero works for this variable** (IV.ix; III.III.vii). Type (i): the multipliers of (E),
`E.e1` (the inertia of the expectation) and `E.e2` (the weight of 12-month inflation); the target
weight is what is left, `1 − e1 − e2`, so a stronger inertia or a stronger weight on realized
inflation **is** a weaker anchor in the model. (E) is this agent's equation, so these multipliers are
this agent's to apply. A coefficient of another equation that reads the expectation (the weight of
the expectation in (I), the reaction of (R) to its deviation from the target) belongs to that
equation's owner: this agent argues for it through Part 3 and the owner applies it. Type (ii): every
channel that reaches expectations outside (E)'s three terms (2.3–2.6, 2.9).

**Step 1 and the exogenous.** Who writes the path of each exogenous of the model is the tutela in the
"Exógenas" tab of `repository/agent_mapping/data_tracker.xlsx`, filled by the user; the proposal gave
this agent none. With no tutela, it uses the paths of those who have it. A tail that needs a different
path of an exogenous outside its tutela (the CDS, the target) writes that path as the condition of
the tail; written in the JSON of paths, it does not enter the P and becomes a divergence that the
tutor answers in the next round (IV.ii).

---

## Part 2 — Causal skeleton: what moves expectations

Section 2.1 is the model's equation and how the agent reads it; 2.2–2.9 are the channels.

### 2.1 Formation: inertia, realized inflation and the target (equation E)

- **Mechanism.** A survey expectation of the next 12 months is partly the previous one carried
  forward, partly a reaction to inflation already observed, partly the pull of the target. The model
  writes exactly that: `E(t) = e1·E(t−1) + e2·I12(t) + (1 − e1 − e2)·Meta(t)`, where `I12` is IPCA
  inflation over the last 12 months and `Meta` is the CMN target over the 12-month horizon. The
  weights sum to one, so at rest the expectation returns to the target **if inflation does**; when
  inflation stays above the target, the expectation settles above it, in proportion to `e2`. The
  expectation then feeds back: (I) reads it, lagged, as the anchor of each price group, and (R)
  reacts to its deviation from the target. Expectations are a link in the model's loop, not an
  endpoint.
- **Read:** [[inflation_persistence]], [[nk_phillips_curve]], [[inflation_targeting]],
  [[core_inflation]].
- **Data:** `expc_focus` (IPCA 12 months ahead, smoothed); endogenous of inflation `inflc_agregados`
  (12-month IPCA, cores, diffusion); endogenous of monetary policy `inflc_meta`.
- **Model:** (E), coefficients `e1`, `e2`; variable `pi_e`; the target `meta_12m` is an exogenous
  of the model, whose path comes from the tutela in the "Exógenas" tab (the proposal gave it to
  monetary policy).
- **Trap.** The anchoring in (E) is imposed, not estimated: the equation cannot produce a
  de-anchoring that is not already in the inflation path. A loss of anchor beyond what inflation
  explains enters as type (i), through `e1`/`e2`, with the justification the posterior's tail
  demands. And a 12-month expectation moves mechanically when a high or low month enters or leaves
  the window: that is arithmetic, not a change of belief, and the agent separates the two before
  calling a move.

### 2.2 The target, the Copom and credibility

- **Mechanism.** The target is an anchor only as long as the public believes the central bank will
  bring inflation back to it. The test is not the level of the short-horizon expectation but whether
  the long horizons stay at the target while the short ones absorb a shock, and whether the survey's
  expected Selic is consistent with its expected inflation converging. A hike can lower expectations
  (credibility) or leave them untouched or higher (the hike read as news of worse inflation, or as
  insufficient). The Copom's communication moves the expected path and can move expectations by
  itself.
- **Read:** [[time_inconsistency]], [[conservative_central_banker]], [[inflation_contract]],
  [[inflation_forecast_targeting]], [[central_bank_communication]], [[forward_guidance]],
  [[information_effect]]; `inflation_expectations_anchoring`.
- **Data:** `expc_focus_periodo` (IPCA, each calendar year to the last one asked), `expc_qpc` (the
  balance of risks for the IPCA and, since the 281st meeting, the projection at the relevant horizon
  with the probability of a deviation from it); endogenous of monetary policy `inflc_meta`,
  `pm_copom_projecoes`, `pm_copom_reuniao`, `pm_copom_calendario`.
- **Model:** the target weight in (E) (type (i), through `e1` and `e2`); the deviation `pi_e −
  meta_12m` that (R) reacts to. A change of the target is a path of `meta_12m`, the monetary-policy
  agent's exogenous.
- **Trap.** This agent does not read the Copom's documents in this plan: what the Copom said about
  expectations, and which horizon it judges, comes from the monetary-policy agent (XS2). The
  credibility reading is this agent's evidence, the reaction function is not: whether the Copom
  will respond is the monetary-policy agent's Q1.

### 2.3 Fiscal policy and the risk premium

- **Mechanism.** A fiscal path that looks unsustainable raises the expectation that inflation will
  eventually do part of the adjustment, and it does so at the long horizons first. The same stress
  shows in the sovereign risk premium and in the inflation priced in the curve.
- **Read:** [[fiscal_dominance]], [[risk_premium]].
- **Data:** endogenous of fiscal `cmb_risco_pais` (CDS); the curve's implied inflation (2.6).
- **Model:** (E) has no fiscal term. The CDS reaches expectations only through the exchange rate
  (F) and inflation (I). A direct fiscal effect on expectations is **outside the model**: tempero of
  type (ii).
- **Trap.** Counting twice: the part of a fiscal shock that passes through the exchange rate into
  inflation is already in the model; only what moves expectations beyond that path is type (ii).
  Whether the fiscal stress is real comes from the fiscal agent (XS8).

### 2.4 The exchange rate and supply shocks

- **Mechanism.** Expected pass-through of a depreciation, fuel and electricity tariffs, food prices:
  shocks the respondents can see coming move the short horizons of the survey, and the administered
  and food components first. A shock that is read as one-off should leave the long horizons alone; if
  it does not, it is becoming a second-round problem.
- **Read:** [[exchange_rate_pass_through]], [[administered_prices]], [[food_inflation_drivers]].
- **Data:** `expc_focus` and `expc_focus_periodo` by component (administered, free, services,
  industrial goods, food at home), `expc_focus_periodo` (câmbio, as consultation of the exchange rate
  the survey assumes); endogenous of FX `cmb_ptax`.
- **Model:** (E) has no exchange-rate term; the exchange rate reaches it through (I). A direct
  effect is **outside the model**, type (ii), under the same double-counting rule as 2.3.
- **Trap.** The FX reading (persistent or transitory, global or idiosyncratic) is the FX agent's
  (XS7); the inflation path is the inflation agent's (XS5). This agent reads only how the survey
  reacted.

### 2.5 The survey's own dynamics: who answers, how fresh, how dispersed

- **Mechanism.** The median of a survey is sticky: it moves when a large share of respondents
  revises. Four readings separate a real move from noise: dispersion (standard deviation, minimum
  and maximum) widening before the median moves; the mean leaving the median (a tail of respondents);
  the 4-business-day base (`base_calculo = 1`, fresh answers) moving ahead of the 30-day base; and the
  number of respondents. The smoothed 12-month series interpolates between calendar years, so a
  change of year in the window moves it without anyone revising.
- **Read:** [[real_time_data]]; `survey_expectations_dispersion`.
- **Data:** `expc_focus` and `expc_focus_periodo` (median, mean, standard deviation, minimum, maximum,
  respondents; base 0 and, in `expc_focus`, base 1).
- **Model:** outside (E): it changes how the measured variable behaves, not what drives it. Enters
  as type (ii) only when the measurement itself is the risk (a revision under way that the median
  has not shown).
- **Trap.** The survey was reformulated more than once and the panel changes: a series that starts
  in a given year is not a missing history. A revision of the calendar-year expectation is not a
  revision of the 12-month one.

### 2.6 Survey against market: the inflation implied in the curve

- **Mechanism.** The nominal and the real curves together price an inflation, by ratio, not by
  difference: `(1 + nominal)/(1 + real) − 1` at the same maturity. It is a price, not a survey: it
  carries an inflation risk premium and liquidity effects, and it moves every day. When the implied
  inflation moves and the survey does not, either the premium moved or the survey is late; the
  agent says which, and with what evidence.
- **Read:** [[term_premium]], [[risk_premium]]; `breakeven_inflation`.
- **Data:** endogenous of monetary policy `br_interest_rate` (`DIPRE` and `NTNBJS`, the same
  maturities); `expc_focus`, `expc_focus_periodo` (IPCA).
- **Model:** outside (E), which explains the survey. Type (ii) when the market leads the survey.
- **Trap.** The curves are the monetary-policy agent's data. This agent concludes on the inflation
  the curve implies (an expectation measure) and never on the stance or the Selic path the curve
  prices, which is the monetary-policy agent's Q3 (decided 2026-10-22: the split is by question,
  not by table).

### 2.7 Short and long horizons

- **Mechanism.** The short horizons (the next months, the current calendar year, 12 months ahead)
  absorb shocks already visible; the long ones (two or more calendar years ahead) are where the
  target is or is not believed. A rise in the short horizons with the long ones at the target is a
  shock being looked through; the long ones rising is de-anchoring.
- **Read:** [[inflation_targeting]], [[inflation_persistence]].
- **Data:** `expc_focus` (12 and 24 months), `expc_focus_periodo` (monthly, quarterly and annual
  IPCA).
- **Model:** (E) holds only the 12-month horizon. The long horizons are the evidence for the tempero
  of type (i) on the target weight.
- **Trap.** The calendar-year horizons shorten as the year passes: the current year's expectation
  late in the year is mostly realized inflation. Compare horizons at the same distance, not the same
  label.

### 2.8 Selic expectations against inflation expectations

- **Mechanism.** The survey states a Selic path meeting by meeting and per calendar year, and the QPC
  asks what the Copom will do and should do, plus the neutral real rate. Read against the survey's
  own inflation path, these give the expected real rate and the expected stance, and they say
  whether the respondents believe the Copom will do enough. A survey that expects cuts with inflation
  expectations above the target is a credibility signal, in either direction.
- **Read:** [[taylor_rule]], [[natural_rate_of_interest]], [[forward_guidance]].
- **Data:** `expc_focus_copom`, `expc_focus_periodo` (Selic), `expc_qpc` (decision blocks, neutral
  rate); endogenous of monetary policy `pm_copom_calendario`.
- **Model:** outside (E); the Selic is (R), the monetary-policy agent's variable.
- **Trap.** This agent does not conclude on the Selic path. Where the curve prices the Selic against
  the survey (the premium), the reading is the monetary-policy agent's Q3 (XS4).

### 2.9 The breakdowns: inflation by component, GDP by sector and by demand

- **Mechanism.** The headline median hides where the respondents see the pressure. By component, a
  revision concentrated in administered prices or food is a shock the survey sees as dated; one in
  services or in the free prices as a whole is closer to the persistent pressure that de-anchors.
  By GDP, growth expected from household consumption and investment is demand the respondents think
  will press prices; growth expected from agriculture or exports is not, or much less. The two
  breakdowns read together say whether the survey's inflation view is coherent with its own growth
  view.
- **Read:** [[core_inflation]], [[administered_prices]], [[food_inflation_drivers]],
  [[nk_phillips_curve]].
- **Data:** `expc_focus` and `expc_focus_periodo` (the five IPCA components); `expc_focus_periodo`
  (GDP: total, agriculture, industry, services, household and government consumption, investment,
  exports, imports).
- **Model:** outside (E), which reads only headline 12-month inflation; the gap is (H), the activity
  agent's variable. Type (ii) when the composition says more than the headline.
- **Trap.** The survey's GDP expectation is evidence about the respondents, not a reading of
  activity: the gap and growth themselves are the activity agent's (XS9). Components entered the
  survey in a later reformulation, so their history is shorter than the headline's.

### Where the agent reads the data

The agent reads every table of its list through `obsidian/ciclos/<date>/dados/F_expectativas.md`,
fixed for the cycle (`analytics/agent_system/dados`, declaring the tables of `SISTEMA_AGENTES.md`
V.VII).

---

## Part 3 — Outputs: what this agent tells the others matters to it

**Approved by the user, 2026-10-22.** What this agent needs from each of the other six, every cycle.

### 3.1 To monetary policy

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| XS1 | **The reaction function to expectations above the target.** Would the Copom respond, and how much; the Selic thesis | The anchor holds only if a response is expected; the survey's Selic path is judged against it | The monetary-policy agent sees the Copom not reacting to a widening gap | 2.2, 2.8 |
| XS2 | **What the Copom said about expectations at the last meeting**: which horizons it watches, whether it calls them de-anchored, its projection at the relevant horizon against the Focus | This agent does not read the Copom's documents in this plan; the Copom's reading is evidence for Q1 and Q3 | The Copom's wording on expectations changes | 2.2 |
| XS3 | **The path of the target (`meta_12m`)** and any risk of the CMN changing it | It is the anchor term of (E); a change moves the variable's rest point | A target change is discussed | 2.1, 2.2 |
| XS4 | **The Selic the curve prices against the survey**, and the premium between them (its Q3) | Separates what the survey expects of the Selic from what the market charges, for the credibility test of Q3 | The curve and the survey diverge by more than a meeting's step | 2.8 |

### 3.2 To inflation

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| XS5 | **The inflation path by quarter and its composition**: persistent pressure against one-off shocks (administered, food), and what leaves the 12-month window | 12-month inflation is the regressor of (E); a one-off shock should not move the long horizons | A shock the inflation agent reads as persistent, or a large month entering or leaving the window | 2.1, 2.4, 2.7 |
| XS6 | **Surprises against the survey's own short-horizon expectation** (the next prints against the monthly Focus) | Surprises are what makes respondents revise | A print or a component far from the survey's monthly median | 2.5 |

### 3.3 To FX

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| XS7 | **Is the move persistent, and global or idiosyncratic?**, and the FX thesis by quarter | A persistent, idiosyncratic depreciation carries a risk premium that reaches the long horizons; a global one usually does not | A persistent idiosyncratic depreciation | 2.3, 2.4 |

### 3.4 To fiscal

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| XS8 | **The fiscal risk reading and the CDS path**: is the debt path credible, is the framework under stress, is there a fiscal-dominance risk | Fiscal doubt reaches the long horizons first, outside the model's terms (2.3) | The fiscal agent's adverse tail gains probability, or the framework changes | 2.3 |

### 3.5 To activity

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| XS9 | **The gap path and whether demand is pressing services** | It reaches expectations through inflation (I), the services expectation first | The gap turns, or services pressure rises with a positive gap | 2.1, 2.4 |

### 3.6 To external

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| XS10 | **Commodity price paths (oil, agricultural, metals) and global inflation** | They reach fuel, electricity and food, the components that move the short horizons | A commodity shock the external agent reads as persistent | 2.4 |

Credit has no agent and this agent asks it nothing; the labour market is read by the activity agent,
provisionally (III.III.vii), and reaches this agent through XS9.

---

## Part 4 — Inputs: what the others told this agent matters to them

The mirror of what the other six maps ask of this agent in their Part 3 (2026-10-22), written from
this side; the source row carries the label in that map. Two rows ask for the anchoring reading
(the thesis of Q4 and Q1), the rest for the survey's consensus on another agent's variable. Some
of the cuts asked for are not in this agent's list yet (V.VII) — the Focus for unemployment and for the
fiscal results, and the QPC's blocks on potential, the NAIRU, fiscal policy and the external
environment —; the agent that asked reads them in its own F for now, and the rows stay as its
request until the cuts of `expc_focus_periodo` and `expc_qpc` are unified here.

| # | Source row | What the other agent needs | Why it matters to it | How this agent answers |
|---|---|---|---|---|
| XE1 | FX S10 | **The consensus for the exchange rate**: the Focus for the BRL at each year-end and its revisions, and the IPCA and Selic the survey expects | Separates surprise from convergence; the expected IPCA enters prospective PPP and the expected Selic the expected carry | `expc_focus_periodo` (exchange rate, IPCA and Selic at each year-end), with revisions and dispersion (channels 2.4, 2.5, 2.8); flag it when the survey revises its year-end exchange rate, IPCA or Selic in the direction of the BRL's move |
| XE2 | PM S9 | **The anchoring reading**: the path of the 12-month-ahead expectation (this agent's thesis), the long horizons against the target, and whether a move is de-anchoring or a short-run reaction to a shock | De-anchored expectations require more restriction for longer, and the rule (R) reacts to the Focus deviation from the target | The thesis of Q4 by quarter (`focus_12m`) and Q1: the long calendar years against the target, with their position in history (channels 2.1, 2.2, 2.7); flag it when the long horizons move away from the target or the upside tail gains probability |
| XE3 | Inflation IN-S9 | **The path of the 12-month-ahead IPCA expectation** (the model variable) **and the anchoring reading**: whether long horizons stay at the target | Expectations are the anchor of all four groups in the model; a de-anchoring makes every shock more persistent | The same answer as XE2: the thesis of Q4 and Q1 (channels 2.1, 2.7); flag it when the long horizons move away from the target |
| XE4 | Inflation IN-S10 | **Expectations by component** (services, administered, food, goods) against the headline | The model anchors all groups to the headline expectation; where the market expects relative prices to move is the evidence for a tempero on one group | Q2, channel 2.9: the five components of `expc_focus` and `expc_focus_periodo` against the headline, at the same horizons; flag it when one component moves while the headline does not |
| XE5 | Activity S-EXP1 | **The consensus for activity**: the Focus for GDP (quarterly and annual, by component) and unemployment; the QPC for quarterly GDP and the gap | Separates surprise from convergence; the market's gap is the second estimate to confront with the BCB's | Q2, channel 2.9: `expc_focus_periodo` (GDP total, by sector and by demand component, annual and quarterly), with its revisions; the unemployment cut and the QPC's GDP and gap blocks are not in this agent's list (see above); flag a material revision of the consensus |
| XE6 | Activity S-EXP2 | **The market's structural readings**: potential growth and NAIRU from the QPC | Inputs to the activity agent's slack cross-check and to the GDP translation of its thesis | Not in this agent's list: the QPC's potential and NAIRU blocks are the activity agent's consultation (V.VII); this agent adds only the QPC's neutral rate (channel 2.8) when it moves with them |
| XE7 | Fiscal FS-EP1 | **The consensus fiscal path**: Focus for the primary, the nominal result, net and gross debt and government consumption, and its revisions; the QPC's fiscal perception | Separates surprise from convergence and is the fiscal agent's benchmark for the accounts (F4) | Government consumption from `expc_focus_periodo` (GDP by demand component, channel 2.9); the fiscal cut of the Focus and the QPC's fiscal perception are not in this agent's list (see above) |
| XE8 | Fiscal FS-EP2 | **Long-horizon inflation expectations, and whether they move with fiscal news** | De-anchoring at long horizons on fiscal news is a market sign of fiscal dominance | Q1 and Q2, channels 2.3 and 2.7: the long calendar years against the target, and the inflation implied in the curve (2.6), read around the fiscal events the fiscal agent names; flag it when long expectations rise in a cycle of fiscal news |
| XE9 | External XS8 | **The market's reading of the external environment**: the QPC's external-environment block and anything in the Focus that bears on it | The consensus against which the external agent's scenario is a view or a surprise | From the Focus, the year-end exchange rate (channel 2.4) and the components that commodity prices reach first (administered, food, 2.9); the QPC's external block is not in this agent's list (see above); flag it when the survey's exchange rate or those components move on an external shock |

---

## Part 5 — Concept index

No literature of its own yet: these are the concept pages the skeleton links, and the ones that have
no page.

- Formation and persistence: [[inflation_persistence]], [[nk_phillips_curve]], [[core_inflation]] (2.1).
- The regime and credibility: [[inflation_targeting]], [[inflation_forecast_targeting]],
  [[time_inconsistency]], [[conservative_central_banker]], [[inflation_contract]] (2.2, 2.7).
- Communication: [[central_bank_communication]], [[forward_guidance]], [[information_effect]] (2.2, 2.8).
- Fiscal and risk: [[fiscal_dominance]], [[risk_premium]] (2.3).
- Shocks: [[exchange_rate_pass_through]], [[administered_prices]], [[food_inflation_drivers]] (2.4).
- Measurement: [[real_time_data]] (2.5).
- Market pricing: [[term_premium]] (2.6).
- The Selic side: [[taylor_rule]], [[natural_rate_of_interest]] (2.8).
- No page yet: `inflation_expectations_anchoring`, `survey_expectations_dispersion`,
  `breakeven_inflation`.
