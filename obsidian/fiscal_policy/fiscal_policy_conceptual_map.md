# Fiscal Policy — Conceptual Map

**Status:** Partes 1–4 aprovadas pelo usuário em 2026-10-22 (a Parte 1 reescrita nas duas discussões e aprovada no mesmo dia).

**What this file is.** This is the fiscal agent's contract with the rest of the system. It says what
every report must answer (Part 1, central questions), what moves fiscal policy and its effects
(Part 2), what this agent tells the others matters TO IT (Part 3, outputs), and what the others told
this agent matters TO THEM (Part 4, inputs). Part 5 is a short index of the concept pages. In the
first joint cycle the agent runs **without literature** (`PLANO_AGENTES.md` I): it reads this map
and its data snapshot F(A), nothing else. So this map has to carry the reasoning on its own; the
concept pages are linked for later cycles, when a layer 1 exists.

**Two discussions** (user, 2026-10-22; `SISTEMA_AGENTES.md` III.III.vii). Fiscal policy is argued on
two levels, and both are registered here:

- **(ii) The effect of fiscal policy on activity and inflation — the priority now.** What matters is
  the stance: how fast spending grows in real terms, the fiscal impulse and how it is measured, how
  much government demand adds to GDP, and the channels from there to the output gap and to prices,
  including the parafiscal push through public banks and directed credit. Part 2, block A, and
  questions F1–F3.
- **(i) The accounts.** The size and composition of the debt, the structure of the budget (revenue
  and spending), the government's proposals and measures, the primary and nominal results, the
  fiscal rule. Registered and kept leaner: Part 2, block B, and question F4.

The price of sovereign risk (the CDS, and the 10-year real yield if this agent is given it) is
where the two meet, and it is today the thesis: Part 2, block C, and question F5.

**How the parts connect to the rest of the vault.** `[[concept]]` links go to `concepts/`; a name in
`code` font is a concept with no page yet (listed in Part 5). "Data" names MySQL tables of this
agent's list (`SISTEMA_AGENTES.md` V.V). No mental model of an asset manager exists for this area
yet.

**Outputs and inputs.** An output of agent A to agent B is what A tells B is important for A, coming
from B. An input of A from B is what B told A is important for B, coming from A
(`SISTEMA_AGENTES.md` I.III.vii). This agent's outputs carry the prefix **FS** plus the other
agent's code — CB (câmbio), PM (política monetária), IN (inflação), AT (atividade), EX (externo), EP
(expectativas) — so `FS-PM1` is the first thing this agent needs from monetary policy. Its inputs
will carry **FE** with the same codes. A row is a request; the content flows the other way. It gives
emphasis and tells the other agent what to flag; it never limits the analysis.

**Two layers.** What is written here is the **fixed** layer: what matters every cycle. On top of it
each cycle has a **dynamic** layer, set by the theses of that cycle's reports; it lives in the
reports, not here.

**Data rule** (`SISTEMA_AGENTES.md` I.III.ix–x, V.V). *Endogenous*: the fiscal tables (`fisc_*`) and
the 5-year CDS. *Endogenous of another agent*: the Selic and the B3 curves (PM), the gap and GDP
(atividade), the exchange rate and reserves (câmbio), the IPCA (inflação), the Focus and the QPC
(expectativas), global rates, risk appetite and oil (externo) — read for consultation; this agent
draws no conclusion about them, and their owners' positions arrive through Part 3. *TWA*: credit
(the parafiscal channel). Every number is traceable to table and date; every pattern stated as
historical comes out of a G over the cycle's A, with the window said, or does not enter
(`PRINCIPIOS_AGENTES.md` I.II.ix).

---

## Part 1 — Central questions: what every report answers

**Rewritten 2026-10-22 around the two discussions; approved by the user the same day.** The questions are the floor,
not the ceiling. They are kept in Portuguese, the language of the report.

The agent does not describe the fiscal accounts: it says what fiscal policy is doing to demand and
prices, what the accounts and the rule show, and what the market prices, and turns that into the
thesis.

| # | Question | What the answer covers | Where to look |
|---|---|---|---|
| | **(ii) Efeito sobre a atividade e a inflação — a prioridade** | | |
| F1 | Qual é a postura da política fiscal: ela está expandindo ou contraindo a demanda, e quanto? | Real growth of spending, by group (benefits and transfers, payroll, discretionary, investment); the fiscal impulse in its several measures, and where they agree or not; the parafiscal push; the direction and size of the stance against the last quarters | 2.1, 2.2, 2.5 |
| F2 | Por onde e quanto a política fiscal chega ao hiato e à inflação, agora e nos próximos seis trimestres? | Government demand in GDP (consumption and investment) and what transfers add to household income; taxes and administered prices that reach prices directly; the path of the impulse over the horizon, with the measures already decided or proposed; what the activity and inflation agents should take as fiscal premise (the agent does not conclude about the gap or the IPCA) | 2.3, 2.4, 2.5 |
| F3 | Como a postura fiscal se combina com a monetária? | The policy mix: fiscal expanding while monetary policy tightens, or the reverse; what it means for the rate needed for the same inflation and for the neutral; whether the Copom reads fiscal policy the same way (asked to PM) | 2.6 |
| | **(i) As contas — registrada, mais enxuta** | | |
| F4 | Como estão as contas e a dívida, e a regra fiscal está sendo cumprida? | Primary and nominal results, the structure of revenue and spending, one-offs; debt level, composition and what moved it (r − g, primary, adjustments); the government's proposals and measures; the rule's targets are not in the data: declare the gap and compare with the Focus | 2.7, 2.8 |
| | **O preço do risco — a tese** | | |
| F5 | O que o prêmio de risco precifica, e qual o cenário para o risco soberano? | How much of the CDS move (and of the 10-year real yield, if this agent has its tutela) is domestic fiscal and how much global; which fiscal path the market prices against F1–F4; signs of fiscal dominance; the thesis below, with the event or reading that motivates each path | 2.9–2.12, the horizon |

### The horizon and the thesis

The system's theses are per quarter of the Structural Model, six quarters from the current one, with
the variable measured as the model measures it (`SISTEMA_AGENTES.md` III.III.i). In a cycle dated
2026-10-22 that is 4T26 to 1T28.

1. **The thesis is the base path of the model's exogenous variables of which this agent has the
   tutela, per quarter, and the distribution around it** (`SISTEMA_AGENTES.md` IV.vi, 2026-10-22).
   The tutela of each exogenous variable is set by the user in the "Exógenas" tab of
   `repository/agent_mapping/data_tracker.xlsx`, not here. Proposal on the table: the 5-year CDS
   (`fiscal`) for this agent; the 10-year real yield (`rr_10a`) undecided between this agent and
   PM.
2. **The CDS** is measured at the close of each quarter, the last trading day, in basis points
   (`cmb_risco_pais`), the model's own convention (`modelo.CONVENCAO`: "fechamento"), so the path
   goes into the consolidation without translation. **`rr_10a`**, if this agent has its tutela, is
   the quarterly average of the NTN-B 120M vertex, also the model's convention.
3. **Central and distribution.** The model gives this agent no central (it has no endogenous
   variable). The central is the agent's own base path, which is what the consolidation (P1, P2,
   PF*) runs; the base range, the tail limits and the probabilities are also the agent's. Each tail
   says what leads to it ("acima de X se …").
4. **Upside and downside** are position only (`SISTEMA_AGENTES.md` III.III.i): upside is a CDS above
   the base range, downside below it; the asymmetry is P(upside) − P(downside). The report says in
   words when it matters that, for Brazil, a higher CDS is the bad tail.
5. **The primary result is not a thesis variable now.** It is argued in F4 and compared with the
   Focus. Registered for later (user, 2026-10-22): the fiscal agent will probably get variables of
   its own area (the impulse, government demand, the primary), and the activity agent's future GDP
   model will take government demand from this agent.
6. **Scoreboard:** for each closed quarter, the band in which the CDS close fell (and `rr_10a`, if
   it applies).

---

## Part 2 — Causal skeleton

**Where fiscal policy enters the Structural Model** (`analytics/agent_system/modelo.py`, `listar`).
The CDS (`fiscal`) is read **only by the FX equation (F)**, as the **change** of the quarter-close
CDS, contemporaneous, with a positive weight (a rising CDS depreciates the real). From (F) the
exchange rate reaches the Phillips curves (food and industrial goods), then expectations (E) and the
interest rate rule (R). The 10-year real yield (`rr_10a`) is read by the rule (R), where
`rr_10a + meta` is the anchor the Selic converges to, and by the IS curve (H), where the tightening
is `(Selic − meta) − rr_10a`, one quarter lagged. **No fiscal flow enters the model:** spending, the
impulse, government demand and the debt have no equation. So discussion (ii) reaches the system as
qualitative tempero of type (ii) on another agent's variable — the gap (atividade) and the IPCA
(inflação) — and the price of risk reaches it through the CDS and `rr_10a` paths (step 1 of the
premises, `SISTEMA_AGENTES.md` IV.ix).

### Block A — discussion (ii): the effect on activity and inflation

#### 2.1 Spending growth and the fiscal stance

- **Mechanism.** The stance is what fiscal policy is doing to demand now, not the size of the debt.
  Its first reading is how fast spending grows in real terms against the economy: spending growing
  above trend output adds demand, below it takes demand out. Composition decides how fast and where
  it lands: benefits and social transfers go to consumption quickly, payroll follows public hiring
  and wage decisions, discretionary spending and investment are the part the government can switch
  on and off, and are usually the first cut in a consolidation. Revenue moves the stance too: tax
  cuts and new taxes change disposable income and prices.
- **Read:** [[mundell_fleming_policy_mix]]; `fiscal_stance`.
- **Data:** `fisc_rtn` (central government revenue and spending by item, monthly); `fisc_efgg`
  (general government by economic nature: benefits, compensation of employees, use of goods and
  services, subsidies, investment); `fisc_investimento` (federal investment); consultation of
  `inflc_agregados` (the IPCA, to deflate) and `atv_pib_taxas` (real growth, the benchmark).
- **Model:** outside the model; enters as tempero (ii) through the activity and inflation agents
  (F2).
- **Trap.** Nominal growth is not real growth: deflate with a G and say by what. Twelve-month sums
  lag turning points; seasonality is strong in the monthly flows, so compare like with like. Court-
  ordered payments, extraordinary credits and one-off revenue move the totals without changing the
  stance: name them before reading a trend.

#### 2.2 The fiscal impulse and how to measure it

- **Mechanism.** The fiscal impulse is the change of the stance: a rise of the deficit that is not
  due to the cycle or to one-offs pushes demand, a fall pulls it back. It can be measured above the
  line (central government revenue and spending), below the line (the change in the public sector's
  primary, from the debt statistics), by economic nature (general government spending that reaches
  demand) and through credit to official financial institutions. The measures differ in coverage,
  timing and what they correct for; when they agree the reading is firm, when they disagree the
  disagreement is information. Correcting for the cycle needs the output gap, which is the activity
  agent's.
- **Read:** [[natural_rate_of_interest]]; `fiscal_impulse`, `structural_primary_balance`.
- **Data:** `fisc_rtn`, `fisc_nfsp` (the primary in % of GDP over 12 months and the monthly flow,
  for the quarter), `fisc_efgg`, `fisc_dlsp_fatores` (credits to official financial institutions);
  consultation of `pm_hiato_produto` (the BCB gap, endogenous of atividade), `atv_pib_mensal` (the
  denominator).
- **Model:** outside the model: the measured impulse, and its path over the horizon, is what this
  agent gives the activity agent as fiscal premise for the gap.
- **Trap.** A cyclical rise of revenue improves the primary without any decision: that is not a
  contractionary impulse. The sign convention differs by table: in `fisc_nfsp` a negative primary
  is a deficit, in `fisc_dlsp_fatores` a positive primary flow is a deficit. Say which measure each
  number is.

#### 2.3 Government demand in GDP

- **Mechanism.** Government consumption and public investment are components of GDP; transfers are
  not, but become household consumption. The share of government demand in GDP, and how fast it
  grows against the rest, says how much of growth the public sector is carrying. This is the check
  of the impulse from the national-accounts side, and the variable the activity agent's future GDP
  model will take from this agent.
- **Read:** [[mundell_fleming_policy_mix]].
- **Data:** consultation of `atv_pib` (government consumption and investment, volume, seasonally
  adjusted), `atv_pib_taxas` (their growth), `atv_pib_valores_correntes` (their share of GDP);
  `fisc_efgg` (the fiscal side of the same spending).
- **Model:** outside the model (F2).
- **Trap.** The national accounts' government consumption is mostly measured by volume of services
  (health, education, administration), not by spending in reais, so it can disagree with the fiscal
  accounts in the short run. GDP data are the activity agent's: read, do not conclude.

#### 2.4 From the stance to the gap and to inflation

- **Mechanism.** An expansionary stance raises demand and closes the gap (or widens a positive one),
  which reaches inflation through the Phillips curves, faster in services. Fiscal decisions also
  reach prices directly, without passing through demand: taxes on fuel and energy, administered
  prices, subsidies, tax cuts — first-round effects that the inflation agent separates from demand.
  Transfers raise household income and consumption; a consolidation does the opposite, with a lag.
- **Read:** [[natural_rate_of_interest]], [[credit_channel]].
- **Data:** consultation of `pm_hiato_produto` (gap), `inflc_agregados` (IPCA and administered
  prices), `expc_focus_periodo` (the consensus for government consumption, in the fiscal cut);
  `fisc_rtn` (subsidies, tax items).
- **Model:** outside the model. This agent measures the push and tells the owners: the activity
  agent decides a type (ii) tempero on the gap, the inflation agent on prices. It never sets the gap
  or the IPCA.
- **Trap.** The same measure can move demand and prices in opposite directions (a tax cut on fuel
  lowers the IPCA and raises disposable income). Say which effect each argument is about.

#### 2.5 Parafiscal: public banks and directed credit

- **Mechanism.** The government can push demand without touching the primary: lending by public
  banks, directed credit (BNDES, housing, rural), Treasury loans and capitalizations of official
  financial institutions, subsidized rates. These show up in the debt (as assets and liabilities),
  not in the primary, and the part of credit outside the market rate weakens monetary transmission.
  A primary that improves while parafiscal credit expands is a smaller consolidation than it looks.
- **Read:** [[credit_channel]]; `directed_credit`, `quasi_fiscal_operations`.
- **Data:** `fisc_dlsp_fatores` (the Treasury's credits to official financial institutions); TWA
  credit `cred_credito_controle_capital` (public against private banks),
  `cred_modalidade_direcionado_pj`, `cred_modalidade_direcionado_pf`, `cred_credito_resumo` (free
  against directed).
- **Model:** outside the model: tempero (ii) on the gap (activity agent) and on transmission (PM),
  told through the FE rows.
- **Trap.** Credit is TWA: the agent reads it and states its premises. Directed credit grows for
  reasons that are not policy (housing cycle, harvest); attribute only what a decision explains.

#### 2.6 The policy mix

- **Mechanism.** Fiscal and monetary policy act on the same demand. A fiscal expansion while the
  central bank tightens means a higher rate for the same inflation outcome, and a persistent
  expansion raises the neutral rate; a credible consolidation lets the same Selic be tighter against
  the demand to come. The stance of this agent (2.1–2.5) is half of that sentence; the Selic path
  and the Copom's reading of fiscal policy are PM's (FS-PM1, FS-PM2).
- **Read:** [[mundell_fleming_policy_mix]], [[natural_rate_of_interest]].
- **Data:** consultation of `pm_copom_reuniao`, `br_interest_rate` (Selic, nominal and real
  curves).
- **Model:** the model has no fiscal term in (H) or (R); the mix reaches it through `rr_10a` (2.10)
  and as tempero (ii) of PM and atividade.
- **Trap.** Do not conclude what the Copom will do: say what the fiscal stance asks of monetary
  policy, and let PM answer.

### Block B — discussion (i): the accounts (registered, leaner)

#### 2.7 The accounts, the rule and the proposals

- **Mechanism.** The fiscal rule promises a primary target and a limit on spending growth for the
  central government; what the market prices is the belief that it will be met and kept. The budget
  structure (rigid mandatory spending, little discretionary room) decides whether the rule is
  feasible. Proposals and measures — new revenue, cuts, changes to the rule, spending moved outside
  it — are the news.
- **Read:** [[time_inconsistency]], [[fiscal_dominance]]; `fiscal_rule_credibility`.
- **Data:** `fisc_rtn` (the rule's object, by item), `fisc_nfsp` (the consolidated result);
  consultation of `expc_focus_periodo` (the consensus for the primary and the nominal result),
  `expc_qpc` (the market's fiscal perception since the last Copom).
- **Model:** outside the model; the motive of the CDS path (2.9).
- **Trap.** **The rule's targets, bands and spending limit are not in the database.** In the first
  cycle the agent declares the gap and compares the primary with the Focus; it never writes a target
  from memory. The central government's primary (`fisc_rtn`, above the line) and the public sector's
  (`fisc_nfsp`, below the line) differ in coverage and method: say which one each claim uses.

#### 2.8 Debt dynamics and composition (r − g)

- **Mechanism.** Debt to GDP rises with the real interest rate on the debt above real growth times
  the debt, falls with the primary surplus, and moves with adjustments that are neither (the
  exchange rate on foreign-currency assets and liabilities, recognition of old debts,
  privatizations). Given r and g there is a primary that stabilizes the ratio. Gross debt (DBGG) and
  net debt (DLSP) tell different stories: net debt subtracts reserves and credits to public banks.
  The composition (floating, inflation-linked, fixed, foreign currency) decides how the Selic, the
  IPCA and the exchange rate reach the debt.
- **Read:** [[fiscal_dominance]]; `debt_dynamics`.
- **Data:** `fisc_divida`, `fisc_dlsp_fatores`, `fisc_nfsp` (interest and nominal result);
  consultation of `pm_copom_reuniao` (Selic), `inflc_agregados`, `atv_pib_mensal`,
  `atv_pib_valores_correntes`, `atv_pib_taxas`, `cmb_ptax`, `cmb_reservas_bc`.
- **Model:** outside the model.
- **Trap.** The sign and size of the exchange-rate effect on the net debt are read from
  `fisc_dlsp_fatores`, not assumed. The implicit rate on the debt is not the Selic: compute it (G).
  Gross debt is a consequence of other agents' variables; argue it, do not forecast it as thesis.

### Block C — the price of risk: where the two discussions meet (the thesis)

#### 2.9 The fiscal premium: the CDS and the long real yield

- **Mechanism.** Investors demand compensation for the risk that the debt is not honoured in real
  terms — by default, by inflation or by a change of rules. The CDS prices sovereign credit risk in
  dollars; the long real yield carries the expected real policy rate, a term premium and a fiscal
  premium; both also move with global risk appetite and global rates. A fiscal premium shows up as
  the CDS and the real rising **against peers** and together with the long real yield; a global move
  shows up across emerging markets at once. The stance (block A) and the accounts (block B) are what
  the premium prices.
- **Read:** [[risk_premium]], [[term_premium]], [[jurisdictional_uncertainty]],
  [[global_financial_cycle]].
- **Data:** `cmb_risco_pais` (the CDS); consultation of `br_interest_rate` (the real curve),
  `cmb_ptax`, `cmb_fx_latam` (the real against peers), `us_interest_rate`, `cmb_equity_us`,
  `cmb_dollar_index_em`.
- **Model:** the CDS is the exogenous `fiscal`, read by (F) as the quarterly change. **The level does
  not move the real in the model; the change does.** When the agent thinks the CDS weighs more or
  less on the real than estimated, it argues it to the câmbio agent (FS-CB rows, section 4 of the
  report); the multiplier on `F.b_fiscal` is the câmbio agent's to apply, because the equation is
  its.
- **Trap.** There is no peers' CDS or emerging-market sovereign spread in the database: the global
  component is read indirectly and through the externo agent (FS-EX1). The CDS load is a manual
  export, with a provisional stretch from another source: check the date of the last observation.

#### 2.10 The long real yield as the model's anchor (tutela per the Exógenas tab)

- **Mechanism.** In the model the 10-year real yield plus the target is the neutral nominal rate:
  the rule (R) pulls the Selic toward it and the IS curve (H) measures the tightening against it. A
  fall of the long real yield because the fiscal premium compresses is the market pricing a
  consolidation ahead — slower spending, less demand pressure, weaker growth and lower inflation —,
  so the same Selic becomes tighter against the demand to come and the model opens room to cut. A
  rise from a wider fiscal premium does the reverse in (R), while in (H) the same Selic becomes
  **less** tight. This is the reading the monetary-policy map asks fiscal to make: whether the
  consolidation the long rates price is credible and how much demand it takes out — it ties block C
  back to block A.
- **Read:** [[natural_rate_of_interest]], [[term_premium]], [[fiscal_dominance]].
- **Data:** consultation of `br_interest_rate` (NTN-B 120M; DI curve); FS-PM3, FS-EX2.
- **Model:** `rr_10a`, read by (R) and (H). If the Exógenas tab gives this agent its tutela, the path
  is written in step 1 with the CDS path, from the same fiscal scenario, split into the fiscal
  premium (this agent's), the expected real policy path and term premium (asked to PM) and the
  global real rate (asked to externo).
- **Trap.** There is no US real (TIPS) curve in the database, only nominal Treasuries. When the model
  moves the Selic through this anchor, the report tells the economic story first and only then where
  it disagrees (`PRINCIPIOS_AGENTES.md` I.III.vii).

#### 2.11 Politics and the calendar: events that motivate paths

- **Mechanism.** Elections, the budget calendar, proposals that change the rule, court-ordered
  payments and announced packages are the events that move the premium and the stance. An event is
  never a premise: it is the motive of a path (IV.ix), and one scenario can move the CDS and `rr_10a`
  together and change the impulse told to the activity agent.
- **Read:** [[time_inconsistency]], [[jurisdictional_uncertainty]].
- **Data:** none in the database: electoral data stay out while the system is in test
  (`SISTEMA_AGENTES.md` III.I.vii). The agent reads the event through the prices in the F(A), without
  polls or dates from memory.
- **Trap.** An event already priced is not news: read how much the CDS moved before saying what the
  event adds.

#### 2.12 Fiscal dominance: the tail

- **Mechanism.** Fiscal dominance is a spectrum, not a switch. At its far end a rate rise raises the
  perceived risk of the debt, the premium rises, the currency weakens and inflation rises: tighter
  money becomes inflationary. Its signs come in three sets: the monetary regime (is the central bank
  reacting as usual), fiscal sustainability (the debt path against the stabilizing primary, the
  rule's credibility) and the market (the premium, the exchange rate weakening on hikes, long
  expectations and implied inflation rising with fiscal news). This agent owns the fiscal side; the
  efficacy of monetary policy under it is PM's.
- **Read:** [[fiscal_dominance]], [[risk_premium]], [[term_premium]].
- **Data:** `cmb_risco_pais`, `fisc_divida`, `fisc_nfsp`; consultation of `br_interest_rate`
  (implied inflation, by a G), `cmb_ptax`, `expc_focus_periodo` (IPCA for the distant years); FS-PM4.
- **Model:** the model is linear and cannot produce the regime switch. In the tail the agent writes
  the CDS path of the dominance scenario and argues the probability of the regime; a stronger
  CDS → real link is argued to câmbio, which applies the multiplier on `F.b_fiscal`.
- **Trap.** A rising premium is not dominance by itself. State which of the three sets of signs is
  present and which is not.

### Where the agent reads the data

The agent reads every table of its list through `obsidian/ciclos/<date>/dados/F_fiscal.md`, fixed
for the cycle. The list and the type of each table are in `SISTEMA_AGENTES.md` V.V.

---

## Part 3 — Outputs: what this agent tells the others matters to it

**Approved by the user, 2026-10-22.** Each row is what this agent needs from that agent, every
cycle; it becomes an input row in that agent's map.

### 3.1 To câmbio

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| FS-CB1 | **Is the real pricing fiscal stress?** The global/idiosyncratic split of the real's move, and whether the real and the CDS moved together against peers | It is the market's confirmation that a CDS move is fiscal; a depreciation without the CDS, or shared with peers, is not | The idiosyncratic component dominates and the CDS moved with it | 2.9, 2.12 |
| FS-CB2 | **The exchange-rate path and the BCB's FX operations** (reserves, swaps) | The parity adjustment moves the net debt and the BCB's swap result moves the nominal result; gross and net debt diverge with them | A large move of the real or of the swap stock | 2.8 |

### 3.2 To política monetária

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| FS-PM1 | **The Selic path** at each quarter close (the PM thesis) | It sets the cost of the debt, the r of r − g, and the monetary half of the policy mix | The path moves the stabilizing primary materially | 2.6, 2.8 |
| FS-PM2 | **How the Copom described fiscal policy**, filtered from the comunicado, ata and RPM | Tells whether the Copom reads fiscal policy as a demand push, a premium or a neutral-rate question, and whether a fiscal move is already in its scenario | The Copom changes its fiscal language | 2.6, 2.10 |
| FS-PM3 | **The split of the long real yield**: the expected real policy path and the term premium, against the fiscal premium (needed if this agent has the tutela of `rr_10a`) | Writing `rr_10a` is splitting it; the policy part is PM's | The curve moves without a fiscal or global cause | 2.10 |
| FS-PM4 | **Credibility reading: is a hike read as credibility or as raising the risk of the debt?** | It is the monetary side of the fiscal-dominance test | A hike that comes with a wider premium or a weaker real | 2.12 |

### 3.3 To inflação

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| FS-IN1 | **The IPCA path** (quarter and 12 months) | It deflates spending (real growth, 2.1); nominal revenue, inflation-linked debt and indexed spending follow it | The path changes by enough to move real spending growth, the primary or the debt cost | 2.1, 2.8 |
| FS-IN2 | **Which government decisions the inflation path assumes** (administered prices, taxes on fuel and energy, subsidies) | The fiscal scenario and the inflation scenario must assume the same decisions | An administered-price or tax decision enters or leaves the path | 2.4 |

### 3.4 To atividade

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| FS-AT1 | **Real growth and the output gap** by quarter | The benchmark for real spending growth, the cycle correction of the impulse, the g of r − g | Growth or the gap moves enough to change the cyclically adjusted primary | 2.1, 2.2, 2.8 |
| FS-AT2 | **Government consumption and investment in the national accounts** | Checks the impulse from the demand side | The national accounts and the fiscal accounts disagree on the direction | 2.3 |

### 3.5 To externo

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| FS-EX1 | **Global risk appetite and emerging-market spreads** (the base path and the tails) | The global component of the CDS; without it, a global move is read as fiscal | A risk-off or risk-on move across emerging markets | 2.9 |
| FS-EX2 | **US long rates** (the 10-year Treasury path) | The global component of the long real yield and of the debt cost | A large move of US long rates | 2.10 |
| FS-EX3 | **Oil and commodity prices** | Royalties and state-firm dividends in the revenue; the commodity part of nominal GDP | A move large enough to change non-tax revenue | 2.7 |

### 3.6 To expectativas

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| FS-EP1 | **The consensus fiscal path**: Focus for the primary, the nominal result, net and gross debt and government consumption, and its revisions; the QPC's fiscal perception | Separates surprise from convergence and is the benchmark of F4 | The consensus revises the primary or the debt | 2.4, 2.7, 2.8 |
| FS-EP2 | **Long-horizon inflation expectations, and whether they move with fiscal news** | Deanchoring at long horizons on fiscal news is a market sign of fiscal dominance | Long expectations rise in a cycle of fiscal news | 2.12 |

**What this agent tells the others (their side, to be confirmed in their maps).** First, discussion
(ii): the stance, the impulse and its path, the parafiscal push (atividade, PM); the government
decisions that reach prices (inflação); the fiscal impulse and the fiscal-dominance reading (PM). Then the price of risk: the CDS path and
its reading (câmbio, PM, externo, expectativas), the fiscal-dominance reading (PM, câmbio), and `rr_10a` and its
split if this agent has the tutela (PM).

---

## Part 4 — Inputs: what the others told this agent matters to them

The mirror of what the other six maps ask of this agent in their Part 3 (2026-10-22), written from
this side; the source row carries the label in that map. The rows split as the two discussions do:
the impulse and the decisions that reach prices (discussion (ii), F1–F2) for activity, inflation and
monetary policy; the CDS path, its global part and the dominance reading (the price of risk, F5) for
FX, monetary policy, external and expectations. Two rows (FE-AT2, FE-EX2) are asked of whoever writes
`rr_10a`: they bind this agent only if the "Exógenas" tab gives it the tutela.

| # | Source row | What the other agent needs | Why it matters to it | How this agent answers |
|---|---|---|---|---|
| FE-CB1 | FX S6 | **The CDS path** (`fiscal`, base and tails) **and whether a move is fiscal**: the reading behind it (the primary, the debt path, the framework) | The CDS is the risk-premium input of (F); this agent writes its path and argues for its weight, and the FX agent applies the multiplier on that weight | The thesis of F5 (the CDS path by quarter, with what leads to each tail), channel 2.9 for the domestic and global parts, 2.7–2.8 for the reading behind it; an argument on `F.b_fiscal` goes in section 4 of the report; flag it when the path or its tails move, or when the agent argues the weight is larger or smaller than estimated |
| FE-CB2 | FX S7 | **The fiscal-dominance reading**: is the fiscal anchor credible, and is there a risk that a rate hike raises the premium instead of supporting the BRL | It decides the sign of the rate → FX link together with the monetary-policy agent's credibility reading | Channel 2.12: which of the three sets of signs is present and which is not, and the probability of the dominance tail; flag it when the adverse tail gains probability or the framework changes |
| FE-PM1 | PM S11 | **The fiscal premium in the long rates and the CDS path**: when the long rates move on the fiscal premium, is the consolidation they price credible, and how much demand does it take out; and the `rr_10a` path, if this agent has its tutela | `rr_10a` + meta is the anchor of the rule and of the IS curve: a compression of the premium tightens the same Selic and opens room to cut | F5, channels 2.9 and 2.10: the CDS path and, with the tutela, the `rr_10a` path from the same fiscal scenario, split into the fiscal premium (this agent's), the expected real policy path and term premium (FS-PM3) and the global real rate (FS-EX2); 2.10 ties the premium back to the demand it takes out (block A) |
| FE-PM2 | PM S12 | **The fiscal impulse and the fiscal-dominance reading**: the direction and size of the stimulus to demand, and whether the primary responds to the debt | Fiscal policy acts on demand in the short run; whether a global shock turns into a vicious circle depends on the primary responding to the debt | F1–F2 (channels 2.1, 2.2, 2.5) for the impulse and its path over the horizon; F4 and channels 2.8 and 2.12 for whether the primary responds to the debt; flag it when the impulse changes sign or the adverse tail gains probability |
| FE-IN1 | Inflation IN-S6 | **Measures that act directly on prices**: taxes on fuel and energy (federal and state), subsidies, administered-price interventions, the minimum-wage rule, social transfers — with dates | They move the IPCA by decree, outside the model, and often come back later; the inflation agent needs their timing | Channel 2.4 (with 2.11 for the calendar): the measures decided and proposed, with direction and date; events and dates are not in the database, so the agent states what the F(A) shows and declares the rest as a gap; flag a measure announced, approved or expiring inside the horizon |
| FE-AT1 | Activity S-FI1 | **The fiscal impulse per quarter**: direction and size of the stimulus to demand — government consumption and investment, transfers to households, parafiscal credit | (H) has no fiscal term; the impulse is the activity agent's tempero (ii) now and the government-demand input of its future GDP model | F1–F2, channels 2.1–2.5: the measured impulse and its path over the six quarters, by component, with the parafiscal push; flag it when the impulse changes sign or a transfer or credit programme is announced |
| FE-AT2 | Activity S-FI2 | **The path of the 10-year real yield and of the fiscal premium in it** (asked of whoever has the tutela of `rr_10a`) | `rr_10a` is the anchor of the tightening in (H): with the Selic given, a lower long real rate is a tighter policy, and its premium side is a cost of capital the model does not see | With the tutela, channel 2.10: the `rr_10a` path from the same scenario as the CDS, with the fiscal-premium part; without it, the fiscal-premium reading of 2.9, for whoever writes the path; flag it when the base path moves or its story changes between premium and neutral |
| FE-EX1 | External XS5 | **The CDS path, and the part of its move this agent attributes to global risk** | In (F) the S&P and `dxy_em` effects are conditional on the CDS: the risk-appetite block and the CDS path must tell one story, or the model double-counts or cancels it | Channel 2.9: the CDS path of F5 with its domestic and global parts, checked against the external agent's risk-appetite scenario (FS-EX1); flag it when the CDS moves while `dxy_em` and the S&P do not, or the reverse |
| FE-EX2 | External XS6 | **The `rr_10a` path, and how much of it this agent attributes to US long rates** (asked of whoever writes `rr_10a`) | Keeps the external agent's long-rate scenario consistent with the anchor that carries it into the gap | Only with the tutela of `rr_10a`: channel 2.10, the split of the path, with the global real rate taken from FS-EX2; flag it when `rr_10a` moves with the US long end flat, or the reverse |
| FE-EP1 | Expectations XS8 | **The fiscal risk reading and the CDS path**: is the debt path credible, is the framework under stress, is there a fiscal-dominance risk | Fiscal doubt reaches the long horizons of expectations first, outside the model's terms | F4–F5: channels 2.7 and 2.8 (the rule, and the debt path against the stabilizing primary), 2.9 (the CDS path) and 2.12 (dominance); flag it when the adverse tail gains probability or the framework changes |

---

## Part 5 — Concept index

- [[mundell_fleming_policy_mix]] — fiscal and monetary policy together (2.1, 2.3, 2.6).
- [[natural_rate_of_interest]] — the neutral, and how fiscal policy moves it (2.2, 2.4, 2.6, 2.10).
- [[credit_channel]] — credit outside the market rate (2.4, 2.5).
- [[fiscal_dominance]] — the spectrum and its three sets of signs (2.7, 2.8, 2.10, 2.12).
- [[risk_premium]] — the premium on Brazilian assets and its drivers (2.9, 2.12).
- [[term_premium]] — what the long yield carries beyond the expected policy path (2.9, 2.10).
- [[time_inconsistency]] — the rule as commitment (2.7, 2.11).
- [[jurisdictional_uncertainty]] — institutional risk in the premium (2.9, 2.11).
- [[global_financial_cycle]] — the global component of spreads (2.9).
- No page yet: `fiscal_stance`, `fiscal_impulse`, `structural_primary_balance`, `directed_credit`,
  `quasi_fiscal_operations`, `fiscal_rule_credibility`, `debt_dynamics`.

The area folder holds one source with a synthesis,
[[fiscal_policy/synthesis/fiscal_dominance (itau, 2025)]]; it is not read in the first cycle (no
literature), and this agent's layer 1 is chosen later.
