# Economic Activity — Conceptual Map

**Status (2026-10-22):** Parts 1–4 approved by the user on 2026-10-22 (central questions, horizon,
thesis variable and its companion row, data list, outputs; Part 4, the mirror of the other maps'
Part 3, filled on 2026-10-22). Decisions of the first batch of seven agents: `SISTEMA_AGENTES.md` III.III.vii.

**What this file is.** This is the economic-activity agent's (`atividade`) contract with the rest of
the system. It says what every report must answer (Part 1, central questions), what moves Brazilian
activity and the output gap (Part 2), what this agent tells the others matters TO IT (Part 3,
outputs), and what the others told this agent matters TO THEM (Part 4, inputs). Part 5 is a short
index of the concept pages the map links. In the first joint cycle the agent runs **without
literature** (`PLANO_AGENTES.md` I): it reads this map and the cycle's data snapshot F(A), nothing
else. The map is therefore written to stand on its own: mechanisms are stated here, not delegated to
sources. The area has no syntheses and no mental model yet; its layer 1 comes later, by the normal
promotion path.

**How the parts connect to the rest of the vault.** `[[concept]]` links go to `concepts/`; a name in
`code` font is either a MySQL table of this agent's list or a concept with no page yet (listed in
Part 5). The concept pages carry the literature's reasoning; in a run without literature the agent
may open them, never the sources behind them.

**Outputs and inputs.** An output of agent A to agent B is what A tells B is important for A, coming
from B. An input of A from B is what B told A is important for B, coming from A. So this agent's
outputs (Part 3) become the other six agents' inputs from activity, and their outputs to activity
fill Part 4. A row is a request; the content flows the other way. An input gives emphasis and tells
the agent what to flag; it never limits the analysis.

**Two layers.** What is written here is the **fixed** layer: what matters every cycle. Each cycle
adds a **dynamic** layer in the reports: an agent whose thesis hinges on something asks for it
explicitly in its report.

**Data rule** (`SISTEMA_AGENTES.md` I.III.ix–x, III.III.vii; the list is V.IV). *Endogenous*: the
national accounts and the monthly activity indicators (`atv_*`), the BCB's output gap and its
vintages (moved from monetary policy: the gap is the variable this agent's thesis is about; monetary
policy keeps how the Copom reads the gap and reacts), and, provisionally, the labour market
(`mt_pnad`, `mt_desocupacao_retro`, `mt_caged`, `mt_caged_setor`), until a labour-market agent exists.
*Endogenous of another agent*, read for consultation, never concluded on: the Selic, the curve and
the target (monetary policy); the exchange rate and the trade detail (FX); the IPCA and the IC-Br in
reais (inflation); the fiscal accounts and the CDS (fiscal); the IC-Br in dollars (external); the
Focus and the QPC (expectations). Each owner's position arrives through Part 3. *TWA*: credit. No
exogenous table.

**The model.** This agent's model variable is the output gap, endogenous, and it owns equation (H)
that produces it: a multiplier on `H.h1` or `H.h2` (tempero type (i)) is this agent's to apply, and
another agent who thinks the tightening works harder or softer argues for it through its outputs.
Which agent writes the path of each exogenous variable is set by the user in the "Exógenas" tab of
`repository/agent_mapping/data_tracker.xlsx` (`SISTEMA_AGENTES.md` IV.ii), not here; the proposal on
the table gives this agent none. A path this agent writes for an exogenous variable outside its
tutela does not enter P: it becomes a logged divergence, answered by the agent with the tutela in the
next round. The gap's effect on inflation is a coefficient of the Phillips curve (I), the inflation
agent's equation: this agent argues for it, the inflation agent applies it. Every round, the agent
writes its thesis per quarter (and any base path it writes) to the cycle's JSON
(`obsidian/ciclos/<date>/caminhos/atividade_<r1|r2|rf>.json`, keys of `modelo.CONVENCAO`).

---

## Part 1 — Central questions: what every report answers

The questions are the floor, not the ceiling: the agent is expected to go beyond them, and nothing
here limits what it may say. They are kept in Portuguese, the language of the report.

The agent does not describe the national accounts: it says where activity is, why, how much slack
that leaves, and where it goes — and it confronts its reading with the BCB's gap, which is the
model's measure, and with the consensus.

| # | Question | What the answer covers | Where to look |
|---|---|---|---|
| Q1 | Onde está a atividade agora, e o que o dado mensal diz do trimestre em curso e do que acabou de fechar? | A nowcast: the monthly indicators inside the quarter against the previous quarter (IBC-Br, industry, retail, services, formal employment), the carry-over they already lock in, and the composition by supply (agriculture, industry, services) and demand (households, government, investment, external). It also says whether the BCB's estimate for the last quarter — the model's starting point — looks right given the data that came after it | 2.4, 2.5, 2.7, 2.8; Part 2 "Where the agent reads the data" |
| Q2 | O que está movendo a atividade, e por qual canal? | Which channels of Part 2 explain the recent move and which ones are turning: monetary tightening and its lags, credit, fiscal demand, household income, external demand and terms of trade, investment, supply shocks. Cyclical against one-off (a harvest, an oil platform, a strike): only the cyclical part says something about the gap | 2.1–2.7 |
| Q3 | Quanta folga há na economia? | The output gap and how sure anyone can be of it: the BCB's central estimate, the dispersion across its models, its latest revisions, the market's gap (QPC), and the cross-checks that are observed — labour slack against the market's NAIRU, the sectors that run hot or cold, services inflation as the price signal of the gap (asked of the inflation agent, S-IN2). Where the agent's reading departs from the BCB's, it says in which direction and why | 2.8, 2.4 |
| Q4 | Qual o cenário prospectivo para a atividade? | The report's thesis on the horizon below: the gap per quarter, central from the Structural Model's base scenario, distribution from the agent's tempero; and its translation into GDP growth. Which channels outside the model weigh on each tail | report §1; 2.1 for the model; 2.2–2.7 for the tempero |

### The horizon — approved by the user, 2026-10-22

The system's theses are per quarter of the Structural Model, six quarters from the current one, with
the variable measured at the close of the quarter (`SISTEMA_AGENTES.md` III.III.i; in the cycle of
2026-10-22, 4T26 to 1T28). The output gap has two features no other thesis variable has: it is
**unobserved** (an estimate, not a price or a published index) and it is **rewritten** by its source
every quarter. The proposal:

1. **The thesis variable is the output gap of each of the six quarters, as the BCB measures it**
   (`pm_hiato_produto`, central estimate, % of potential output). It is the model's endogenous
   variable: equation (H) produces it and the Phillips curve (I) reads it. The gap is a quarterly
   level, so "at the close of the quarter" means the quarter's value.
2. **The central is the model's** in every quarter: the base scenario of the agent's own run in
   round 1 and, from round 2 on, the joint run P (`SISTEMA_AGENTES.md` IV.vi). The distribution
   around it is the agent's tempero (IV.ix).
3. **A companion row, GDP growth over four quarters** (`atv_pib_taxas`, `yoy`, the official
   year-on-year rate of each quarter), so the thesis has a number anyone can check on the day IBGE
   publishes it. Its central is **derived mechanically**, not tempered: potential growth plus the
   change of the gap over four quarters from the model. Potential growth is the one the BCB's own gap
   implies: over the last four published quarters, GDP growth over four quarters minus the change of
   the gap over the same four quarters, both from the current edition. The year-on-year form is
   proposed over the quarter-on-quarter one because the published gap is smooth and the seasonally
   adjusted quarterly rate is not: the identity holds on average, and quarter by quarter the
   difference is noise that the four-quarter window averages out. The distribution of this row is
   the agent's, like the gap's.
4. **Scoreboard** (the user's choice, 2026-10-22, revised the same day). GDP growth: IBGE's first
   release for the quarter (`atv_pib_taxas`). The gap: the BCB's central estimate for that quarter in
   the **first RPM edition after IBGE publishes the quarter's GDP**, i.e. the edition at the close of
   the following quarter (the 3Q gap is scored with the December edition; `pm_hiato_produto_vintages`
   keeps every edition). It comes one quarter after the other scoreboards, but already includes the
   quarter's GDP, which cuts (without removing) the revision between the BCB's nowcast and later
   editions. Recent editions revised the gap upwards (4Q25: 0.17 in Dec/25, 0.74 in Sep/26), while
   the model projects on the scale of the current edition. Later revisions are not rescored; when one
   is large, the report says so. The user's goal for later: a model that regresses only the
   consolidated part of the BCB gap (up to two or three years ago, the part least likely to be
   revised) on GDP, unemployment, industry and other data, and uses those coefficients forward.
5. **Upside and downside** (`SISTEMA_AGENTES.md` III.III.i). Upside is the tail above the central (a
   higher gap, faster growth), downside the tail below; position only, no judgement, and the
   asymmetry is P(upside) − P(downside). Whether a tail is good or bad for Brazil the report says in
   words when it matters: an upside gap is more activity and more inflation pressure, so the same
   tail reads differently here and for the inflation and monetary-policy agents.
6. **The starting point is not this agent's to set.** The model starts from the BCB's estimate for
   the last quarter, which is itself a nowcast until IBGE publishes that quarter. When the monthly
   data say that estimate is off (Q1), the agent cannot move the central: the disagreement enters as
   asymmetry and as the limits of the first quarters' tails, and the report says how big it is.
7. **Registered for later** (the user's idea, 2026-10-22): decompose the gap into components —
   output, unemployment and others —, at which point the gap would belong to more than one agent
   (the labour-market agent, when it exists, among them). Not in this plan.

---

## Part 2 — Causal skeleton: what moves Brazilian activity

Section 2.1 is the only channel equation (H) of the Structural Model carries; 2.2–2.7 are outside
the model and reach the thesis through the tempero; 2.8 is how the gap is measured. Two rules hold
for every section:

- **The model's channel enters only through the tempero of type (i)** (a coefficient stronger or
  weaker than estimated), never as a qualitative factor (`SISTEMA_AGENTES.md` IV.ix).
- **A factor outside the model enters as type (ii) only for the part that is not already the
  Selic's effect.** Credit slowing because the Selic is high is the tightening of 2.1, already in
  (H); credit slowing because banks cut supply, or growing because directed credit expanded, is
  2.2. The report says which part is which, or it counts the same thing twice.

### 2.1 Monetary policy: the tightening and its lags

- **Mechanism.** A policy rate above the neutral raises the cost of credit and the return on saving,
  depresses asset prices and the demand for durables and investment, and appreciates the currency;
  activity responds with lags, and the economy's slack opens before inflation falls. Equation (H) of
  the Structural Model writes the whole of it as one line: the gap of a quarter depends on the gap of
  the quarter before (persistence) and on the **tightening of the quarter before**, measured as the
  quarterly average Selic minus the anchor `rr_10a + meta_12m` — the 10-year real yield (NTN-B) plus
  the inflation target, the same anchor as the interest-rate rule (R). Two crisis dummies (2008–2009
  and 2020) are zero in every projected quarter. There is no intercept: with policy at the anchor and
  no shock, the gap returns to zero.
- **What the model does with it.** The Selic comes from (R), the monetary-policy agent's variable;
  who writes the paths of `meta_12m` and `rr_10a` is set in the "Exógenas" tab of the tracker (the
  proposal: the target to monetary policy, the 10-year yield undecided between fiscal and monetary
  policy). Its lever on 2.1 is type (i), on its own equation: `H.h2` (how much a point of tightening
  takes off the gap) and `H.h1` (how long a gap lasts), with the posterior ranges printed by
  `modelo.listar`.
- **Read:** [[monetary_transmission_lags]], [[natural_rate_of_interest]], [[term_premium]].
- **Data:** `pm_hiato_produto`; for consultation `pm_copom_reuniao`, `br_interest_rate` (the NTN-B
  10-year and the Selic), `inflc_meta`; the most rate-sensitive parts of activity, where the
  tightening shows first — retail of vehicles and of furniture and appliances (`atv_pmc`), durable
  and capital goods (`atv_pim_uso`), investment (`atv_pib`, `fbcf`).
- **Trap.** The anchor is a market yield that carries a term premium and a fiscal premium; it is the
  model's neutral, not a cost of capital. In the model a **higher** `rr_10a`, with the Selic given,
  is **less** tightening and a higher gap; for a firm deciding to invest, a higher long real rate is
  the opposite. When the long rate moves on a fiscal premium, the model reads the neutral moving
  while the economy feels the cost of capital moving (2.6). The report tells the economic story of
  the model's channel before disagreeing with it (`PRINCIPIOS_AGENTES.md` I.III.vii), and a
  proposal to split the anchor into neutral and premium goes to section 6, "Sobre o modelo".
  And one quarter of lag in the equation is not the length of the transmission: persistence carries
  the effect over many quarters, so today's activity is not the effect of today's Selic.

### 2.2 Credit and financial conditions

- **Mechanism.** Most of the policy rate reaches spending through credit: new lending, spreads,
  household debt service, firms' working capital. Frictions amplify it — the premium on external
  finance moves with the policy rate and with borrowers' net worth, and banks' willingness to lend
  is a channel of its own. Directed credit (housing, rural, the BNDES) is priced off other rates and
  responds little to the Selic; a larger directed share weakens the transmission. Defaults and the
  share of income committed to debt service decide how long households can keep consuming.
- **What the model does with it.** Nothing directly: (H) has no credit or financial-conditions term.
  The part that is the Selic's own effect is already in 2.1; the rest — a credit supply shock, a
  change in directed lending, a default cycle — is tempero (ii).
- **Read:** [[credit_channel]], [[financial_accelerator]], [[macroprudential_policy]];
  `directed_credit`.
- **Data (TWA credit):** `cred_credito_resumo` (concessions, rates, spreads, defaults),
  `cred_fluxo_financeiro` (the credit impulse in the RPM's concept), `cred_ptc` (banks' reading of
  supply and demand), `cred_credito_familias` (household debt and debt service),
  `cred_credito_amplo` (credit including bonds and external debt), `cred_modalidade_livre_pf`,
  `cred_modalidade_livre_pj`, `cred_modalidade_direcionado_pj`.
- **Trap.** Credit has no agent: the agent states its premises. Quantities are a weak test of the
  channel — conditions are measured by the price (rates, spreads) and by the banks' own reading, not
  by the stock.

### 2.3 Fiscal policy and government demand

- **Mechanism.** The government acts on activity directly — its own consumption and investment, and
  transfers that become household income (2.4) — and indirectly, through the fiscal premium in the
  long rates and the exchange rate. The fiscal impulse is the change in the stance, not its level: a
  large deficit that stops growing is no longer a stimulus.
- **What the model does with it.** The direct demand effect is outside (H) and enters as tempero
  (ii). The indirect effect is inside, through `rr_10a` in the anchor (2.1), and only through it:
  a fiscal story already moving the long rate in the base scenario cannot also enter as a demand
  factor for the same effect. *Registered for later, not in this plan:* this agent's own GDP model,
  taking government demand from the fiscal agent.
- **Read:** [[fiscal_dominance]], [[mundell_fleming_policy_mix]], [[risk_premium]]; `fiscal_impulse`.
- **Data (endogenous of the fiscal agent, for consultation):** `fisc_efgg` (general government by
  economic nature, the base of the impulse), `fisc_rtn` (central government, monthly, including
  transfers), `fisc_nfsp` (primary result); `atv_pib` (`consumo_adm_publica`).
- **Trap.** The size and timing of the impulse are the fiscal agent's (S-FI1); this agent judges what
  it does to activity. Electoral-year transfers raise household income without showing as government
  consumption in the national accounts.

### 2.4 Household income and the labour market

- **Mechanism.** Household consumption is the largest component of demand and follows disposable
  income: employment times the real wage (the wage bill), plus transfers, minus debt service.
  Inflation erodes it; a tight labour market sustains it and raises wages. The labour market is also
  the best observed measure of slack: unemployment against the rate that does not accelerate wages
  is a cross-check on the gap (2.8).
- **What the model does with it.** Outside (H): tempero (ii), for the part that is not the Selic's
  effect (a wage bill held up by transfers, a minimum-wage rise, a fall in inflation that lifts real
  income).
- **Read:** [[natural_rate_of_unemployment]], [[sticky_wages]], [[nk_phillips_curve]].
- **Data (endogenous, provisionally, until a labour-market agent exists):** `mt_pnad` (unemployment,
  participation, real income, real wage bill, informality), `mt_desocupacao_retro` (the BCB's
  seasonally adjusted unemployment rate, back to 2004), `mt_caged` (formal employment stock),
  `mt_caged_setor` (net hires by sector); for consultation `inflc_agregados` (the deflator of real
  income), `cred_credito_familias` (debt service).
- **Trap.** The PNAD is a three-month moving window, so a monthly reading overlaps two thirds of the
  previous one; the CAGED counts only formal jobs. A tight labour market and slowing activity can
  coexist for a while, because employment lags output.

### 2.5 The external side: demand abroad, terms of trade and the exchange rate

- **Mechanism.** Exports follow partner demand (China, the United States, Argentina) and the
  harvest; imports follow domestic demand and the real exchange rate, and leak part of every demand
  impulse abroad. Better terms of trade raise national income above GDP (the income gained on the
  same volume) and feed profits, investment and consumption in the commodity sectors. A depreciation
  helps tradables and squeezes real income through imported prices. Global financial conditions
  reach domestic credit and the long rates.
- **What the model does with it.** Not in (H). The commodity indices enter the Phillips curve and the
  FX equation, the exchange rate is endogenous in (F); their effect on activity is tempero (ii).
- **Read:** [[balance_of_payments_approach]], [[global_financial_cycle]],
  [[mundell_fleming_policy_mix]]; `terms_of_trade_income`.
- **Data:** `atv_pib` (`exportacao`, `importacao`), `atv_renda_poupanca` (gross national income
  against GDP); for consultation `cmb_termos_troca`, `cmb_comex_produto` (price and volume of the main
  commodity exports), `cmb_comex_pais` (exports by partner), `cmb_ptax` (FX agent);
  `comm_icbr_usd` (external agent), `comm_icbr` (inflation agent).
- **Trap.** A terms-of-trade gain raises income more than output, so it shows in consumption and
  investment before it shows in GDP. Net exports often move against domestic demand (imports fall
  when demand falls), so a positive external contribution can be a weak-demand signal. The FX path
  and its persistence are the FX agent's (S-CB1); the global cycle is the external agent's.

### 2.6 Investment, the long rate and uncertainty

- **Mechanism.** Investment depends on expected demand, on the long real cost of capital, on
  funding (BNDES, capital markets, external debt) and on uncertainty — fiscal, regulatory,
  institutional. It is the most volatile component of demand, and capital goods production and
  imports lead it. Investment also builds potential output (2.8).
- **What the model does with it.** The long rate is in the model only as the neutral (2.1), with the
  opposite sign of a cost of capital. The cost-of-capital and uncertainty channels are tempero (ii).
- **Read:** [[term_premium]], [[jurisdictional_uncertainty]], [[natural_rate_of_interest]].
- **Data:** `atv_pib` (`fbcf`), `atv_pim_uso` (`bens_capital`), `atv_renda_poupanca` (gross capital
  formation and saving), `cred_credito_amplo`, `cred_modalidade_direcionado_pj`; for consultation
  `br_interest_rate` (NTN-B).
- **Trap.** The investment series in the national accounts is revised heavily and includes imported
  equipment that can come in lumps (an oil platform registered in one quarter). Read the trend, not
  one quarter.

### 2.7 Supply: agriculture, extraction and other shocks

- **Mechanism.** A record or a failed harvest, an oil field coming online, a drought, a flood, a
  strike or an epidemic move GDP with little relation to demand. Weather patterns (El Niño and La
  Niña) shift harvests in different regions in different directions. Agriculture weighs more in some
  quarters than in others, so the same harvest moves quarterly GDP unevenly through the year.
- **What the model does with it.** Nothing: the crisis dummies are zero in every projected quarter.
  What a supply shock does to the **gap** depends on how the BCB treats it (a supply shock can move
  potential as much as output); what it does to **GDP growth** is direct. It enters the companion row
  more than the gap row, as tempero (ii).
- **Read:** [[food_inflation_drivers]] (weather and harvests on the price side).
- **Data:** `atv_pib` (`agropecuaria`), `atv_ibcbr` (agriculture and ex-agriculture),
  `atv_pim` (`ind_extrativas`); for consultation `comm_icbr` (inflation agent). The ENSO index
  (`clima_oni`) is in the database but out of every list until a job updates it.
- **Trap.** Separate the one-off from the cycle before reading the gap: activity ex-agriculture
  (`atv_ibcbr`) is the measure for the cycle. A supply shock is also the inflation agent's (food,
  energy), and the same shock reads as good news on one side and bad on the other.

### 2.8 Potential output and the measurement of the gap

- **Mechanism.** The gap is the distance between output and potential, and potential is not
  observed: it is estimated from trends, from the labour force, the capital stock and productivity,
  or from what inflation reveals. Every estimate is revised as data arrive; the latest quarters are
  the most uncertain, and a long slump tends to be absorbed into potential. The BCB's estimate blends
  several models with judgement and publishes their dispersion. Observed cross-checks: unemployment
  against the market's NAIRU, sectors running hot or cold, services inflation (2.4; S-IN2).
- **What the model does with it.** Everything rests on it: (H) is estimated on the BCB's **current**
  edition of the gap, a two-sided smoothed series rewritten every quarter, not on what the BCB said
  at the time; the projection starts from the BCB's estimate for the last quarter; and (I) reads the
  gap in services and industrial goods, so a different gap is a different inflation. The persistence
  `H.h1` is a type (i) lever; a starting point the agent believes wrong enters as asymmetry
  (Part 1, horizon, item 6).
- **Read:** [[real_time_data]], [[natural_rate_of_unemployment]], [[nk_phillips_curve]];
  `potential_output`, `okun_law`.
- **Data:** `pm_hiato_produto` (central and the dispersion across models: minimum, p25, p75,
  maximum), `pm_hiato_produto_vintages` (every edition: what the BCB said when); `atv_pib`,
  `atv_pib_taxas`; for consultation `expc_qpc` (the market's gap, potential growth and NAIRU);
  `mt_pnad`, `mt_desocupacao_retro`.
- **Trap.** A revision of the gap changes the model's starting point and the inflation projection
  with no new data, and only `pm_hiato_produto_vintages` shows it. The BCB's methodology changed
  between the 2024-06 and 2024-09 editions: only the central estimate is comparable across them. The
  market's gap and the BCB's are different estimates of the same unobserved thing; neither is the
  data.

### Where the agent reads the data

The agent reads every table of its list (`SISTEMA_AGENTES.md` V.IV, written when this map is
approved) through the cycle's F(A), fixed for the whole cycle (`analytics/agent_system/dados`, module
`atividade`). Besides the reading of each table, the F is meant to carry what Q1 needs and no single
table gives: the monthly indicators of the quarter in course against the previous quarter, with the
carry-over; the BCB's gap with its dispersion and the last revision of each recent quarter; and the
Focus and QPC readings for growth, the gap, potential and the NAIRU side by side. The model run is
`analytics/agent_system/modelo.py` (`listar`, `rodar`), with the coefficients of (H) under `H.`.

---

## Part 3 — Outputs: what this agent tells the others matters to it

What this agent needs from each of the other six, every cycle. Labels: `S-` (output of this agent)
plus the other agent's code — PM (monetary policy), CB (FX), IN (inflation), FI (fiscal), EXT
(external), EXP (expectations). When the other maps are approved, each row reappears there as an
input, under that map's own label.

### 3.1 To monetary policy

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| S-PM1 | **The Selic path and its balance of risks**: average and close of each quarter, as the monetary-policy agent reads it | The Selic of each quarter is the tightening of the next one in (H); the Selic is endogenous, but the monetary-policy agent's distribution (a longer hold, a faster cut) shapes this agent's tails | The agent's distribution leans away from the model's central in the first two quarters | 2.1 |
| S-PM2 | **The stance: how restrictive is policy, read against the neutral the Copom uses** and against the model's anchor | (H) measures the tightening against `rr_10a + meta`; if the anchor carries premia that the neutral does not, the effective tightening is larger or smaller than the model's, which is a type (i) tempero on `H.h2` | The two readings disagree on whether policy is restrictive, or by how much | 2.1, 2.6 |
| S-PM3 | **How the Copom read activity and the gap at the last meeting**, from the comunicado, the ata and the RPM, with the revision of the gap in the latest edition | The model's starting point and the thesis variable are the BCB's gap; a revision moves both without new data, and the Copom's narrative is the benchmark this agent confronts in Q3 | The RPM revised the gap of recent quarters, or the Copom changed its reading of activity or the labour market | 2.8, Part 1 |

### 3.2 To FX

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| S-CB1 | **The FX path and whether the move is persistent** | A persistent real depreciation changes tradables' competitiveness and imported-goods prices, so real income; outside (H), tempero (ii) | A move the FX agent classifies as persistent | 2.5 |
| S-CB2 | **Terms of trade: price against volume**, from the trade detail | Terms-of-trade gains raise national income above GDP and feed demand in the commodity sectors before GDP shows it | A persistent move in the terms of trade, or a volume shock in a main export | 2.5, 2.7 |

### 3.3 To inflation

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| S-IN1 | **The IPCA path and its distribution, with food and administered prices** | Inflation deflates the wage bill and the transfers; food and administered prices weigh most on lower-income consumption | The inflation agent's distribution leans well above the model's central | 2.4 |
| S-IN2 | **Is the gap showing in prices?** The reading of underlying services against what the gap implies | Services are the gap's price signal in (I); services running persistently above or below what the gap explains is evidence that the gap measure is off | Services diverge from the gap's implied path for more than one quarter | 2.8, Q3 |

### 3.4 To fiscal

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| S-FI1 | **The fiscal impulse per quarter**: direction and size of the stimulus to demand — government consumption and investment, transfers to households, parafiscal credit | (H) has no fiscal term; the impulse is tempero (ii) now and the government-demand input of this agent's future GDP model | The impulse changes sign, or a transfer or credit programme is announced | 2.3, 2.4 |
| S-FI2 | **The path of the 10-year real yield and of the fiscal premium in it** (to whichever agent has the tutela of `rr_10a` in the "Exógenas" tab; the proposal is fiscal or monetary policy) | `rr_10a` is the anchor of the tightening in (H): with the Selic given, a lower long real rate is a tighter policy, and its premium side is a cost of capital the model does not see | The base path of `rr_10a` moves, or its story changes between premium and neutral | 2.1, 2.6 |

### 3.5 To external

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| S-EXT1 | **Demand abroad**: growth of the main partners and the global cycle, with the probability of a global recession | Exports and the commodity cycle; a global recession is this agent's downside tail and the model's crisis dummies are zero in projection | The global outlook changes, or a recession probability rises | 2.5, Part 1 |
| S-EXT2 | **Commodity prices in dollars** (agriculture, metals, energy) | Farm and mining income, investment in the extractive sectors; the indices enter (I) and (F), not (H), so their effect on activity is tempero (ii) | The base paths move materially | 2.5, 2.7 |
| S-EXT3 | **Global financial conditions**: the Fed path and risk appetite | They reach domestic credit, the long rates and flows | A risk-off episode or a change in the Fed path | 2.2, 2.5 |

### 3.6 To expectations

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| S-EXP1 | **The consensus for activity**: the Focus for GDP (quarterly and annual, by component) and unemployment; the QPC for quarterly GDP and the gap | Separates surprise from convergence; the market's gap is the second estimate to confront with the BCB's in Q3 | The consensus is revised materially, or the thesis departs from it | Q1, Q3, Q4 |
| S-EXP2 | **The market's structural readings**: potential growth and NAIRU from the QPC | Inputs to the slack cross-check and to the GDP translation of the thesis | A QPC edition changes potential growth or the NAIRU | 2.8, Part 1 |

---

## Part 4 — Inputs: what the others told this agent matters to them

The mirror of what the other six maps ask of this agent in their Part 3 (2026-10-22), written from
this side; the source row carries the label in that map, and this map's inputs are labelled E1, E2…
Every row asks for the gap path, so the answer is the thesis of Q4, written once, and each row points
to it. The FX and external maps register no fixed output to this agent: there the flow goes the
other way, and it is in this map's Part 3 (S-CB1, S-CB2, S-EXT1–S-EXT3).

| # | Source row | What the other agent needs | Why it matters to it | How this agent answers |
|---|---|---|---|---|
| E1 | PM S10 | **The output-gap path** (this agent's thesis) **and its revision** in the latest RPM, with the labour market (unemployment, wages against productivity) | The gap enters the Copom's projection, and a revision moves the projection with no new data; the Copom watches wages growing above productivity | The thesis of Q4 by quarter; Q3 with the revision of recent quarters (`pm_hiato_produto_vintages`); channel 2.4 for the labour market (`mt_pnad`, `mt_caged`); flag it when the gap changes sign in the horizon or the RPM revises recent quarters |
| E2 | Inflation IN-S5 | **The output-gap path and where the demand pressure is**: services against goods, household consumption, income | The gap is the demand channel of services and industrial goods; services are the most persistent group and the one the Copom watches most | The thesis of Q4, and Q1–Q2 with the composition by sector and by demand (the monthly services and retail indicators, household consumption and income, channel 2.4); flag it when the gap changes sign or services activity diverges from the gap |
| E3 | Fiscal FS-AT1 | **Real growth and the output gap** by quarter | The benchmark for real spending growth, the cycle correction of the impulse, the g of r − g | The thesis of Q4 with its companion row, GDP growth over four quarters (`atv_pib_taxas`); flag a revision of growth or of the gap large enough to change the cycle correction |
| E4 | Fiscal FS-AT2 | **Government consumption and investment in the national accounts** | Checks the impulse from the demand side | Q1, the composition by demand of the national accounts (`atv_pib`, channel 2.3); flag it when government demand in the national accounts moves against the direction of the impulse the fiscal agent gives (S-FI1) |
| E5 | Expectations XS9 | **The gap path and whether demand is pressing services** | It reaches expectations through inflation (I), the services expectation first | The thesis of Q4 and channel 2.4; flag it when the gap turns, or services activity rises with a positive gap |

---

## Part 5 — Concept index

The area has no literature in the vault yet; its layer 1 comes later (`PLANO_AGENTES.md` VI). The
concept pages the map links, by channel:

- **Monetary transmission (2.1, 2.2):** [[monetary_transmission_lags]], [[natural_rate_of_interest]],
  [[credit_channel]], [[financial_accelerator]], [[macroprudential_policy]], [[term_premium]].
- **Fiscal (2.3):** [[fiscal_dominance]], [[mundell_fleming_policy_mix]], [[risk_premium]].
- **Income and labour (2.4):** [[natural_rate_of_unemployment]], [[sticky_wages]],
  [[nk_phillips_curve]].
- **External (2.5):** [[balance_of_payments_approach]], [[global_financial_cycle]].
- **Investment (2.6):** [[jurisdictional_uncertainty]].
- **Supply (2.7):** [[food_inflation_drivers]].
- **Measurement (2.8):** [[real_time_data]].
- **No page yet:** `potential_output`, `okun_law`, `fiscal_impulse`, `terms_of_trade_income`,
  `directed_credit`.
