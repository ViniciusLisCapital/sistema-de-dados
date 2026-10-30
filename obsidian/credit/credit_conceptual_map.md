# Credit — Conceptual Map

**Status:** Parts 1–4 approved by the user on 2026-10-30 (`coordenacao/B_novos_agentes.md`,
Decisões): boundaries, the six central questions, the ten channels, the outputs and inputs, and the
data list. The thesis variable stays **provisional, decided with the model** (`SISTEMA_AGENTES.md`
III.III.ix). Part 5 belongs to chat D.

**What this file is.** This is the credit agent's (`credito`, code **CR**) contract with the rest of
the system. It says what every report must answer (Part 1, central questions), what moves Brazilian
credit and how it reaches demand (Part 2), what this agent tells the others matters TO IT (Part 3,
outputs), and what the others told this agent matters TO THEM (Part 4, inputs). Part 5, the concept
index and the layer 1, comes later. In its first cycle the agent runs **without literature**
(`PLANO_AGENTES.md` I): it reads this map and its data snapshot F(A), nothing else. So the map carries
the reasoning on its own — the mechanism, its premises, when it holds and when it fails — and no
estimate from any paper enters as a current value (`PRINCIPIOS_AGENTES.md` I.I.vii).

**Where this agent comes from.** Until 2026-10-30 credit had no agent: its tables were TWA in
monetary policy (11 tables, channel 2.10), activity (8, channel 2.2) and fiscal (4, channel 2.5). The
boundaries now (III.III.ix):

- this agent owns **every `cred_*` table**: the eleven that were TWA, plus the cuts by firm size, by
  economic activity and by type of client, which no list carried;
- **credit × monetary policy — "credit: conditions; PM: stance".** This agent concludes on credit
  conditions (rates, spreads, concessions, supply and demand, defaults, leverage) and on how much of
  the Selic reaches them; PM concludes on the stance and the efficacy of policy, reading the credit
  condition this agent delivers;
- **credit × fiscal — "fiscal decides, credit measures".** The government decision and the size of the
  parafiscal stimulus (`fisc_dlsp_fatores`, fiscal's channel 2.5) stay with fiscal; this agent measures
  how much directed credit and the public banks grow, and what that does to transmission;
- **credit × activity — the impulse is credit's.** The credit impulse (`cred_fluxo_financeiro`) belongs
  to this agent; activity concludes on its effect on the output gap;
- the labour market belongs to MT: this agent consults `mt_*` and concludes nothing on it.

**How the parts connect to the rest of the vault.** `[[concept]]` links go to `concepts/`; a name in
`code` font is either a MySQL table of this agent's list or a concept with no page yet (to be listed
in Part 5). "Data" names tables of this agent's list (`SISTEMA_AGENTES.md` V, to be written when this
map is approved). No mental model of an asset manager exists for this area yet.

**Outputs and inputs.** An output of agent A to agent B is what A tells B is important for A, coming
from B. An input of A from B is what B told A is important for B, coming from A
(`SISTEMA_AGENTES.md` I.III.vii). This agent's outputs carry the prefix **CR** plus the other agent's
code — CB (câmbio), PM (política monetária), IN (inflação), AT (atividade), EX (externo), EP
(expectativas), FS (fiscal), MT (mercado de trabalho) — so `CR-PM1` is the first thing this agent
needs from monetary policy. Its inputs carry **CE** with the same codes (no other map uses CE). A row
is a request; the content flows the other way. It gives emphasis and tells the other agent what to
flag; it never limits the analysis.

**Two layers.** What is written here is the **fixed** layer: what matters every cycle. Each cycle
adds a **dynamic** layer in the reports, set by that cycle's theses.

**Data rule** (`SISTEMA_AGENTES.md` I.III.ix–x). *Endogenous*: the fourteen `cred_*` tables — the
BCB's credit statistics by resource, segment and modality, by bank control, firm size, activity and
type of client, the broad credit to the non-financial sector, household debt and debt service,
corporate defaults, the banks' survey (PTC) and the financial flow behind the BCB's credit impulse.
*Endogenous of another agent*, read for consultation, never concluded on: the Selic and the curves
(PM), the gap, GDP and the credit-sensitive indicators (atividade), the IPCA (inflação), employment
and income (mercado de trabalho), the parafiscal decisions and the equalization subsidies (fiscal),
the Focus (expectativas), the exchange rate (câmbio) — each owner's position arrives through Part 3.
No TWA and no exogenous table. Every number is traceable to table and date; every pattern stated as
historical — "public banks lend against the cycle", "defaults follow fast growth" — comes out of a G
over the cycle's A, with the window said, or does not enter (`PRINCIPIOS_AGENTES.md` I.II.ix). The
patterns in Part 2 are written as hypotheses for that G, not as findings.

---

## Part 1 — Central questions: what every report answers

**Decided by the user, 2026-10-30.** The questions are the floor, not the ceiling. They are kept in
Portuguese, the language of the report.

The agent does not describe the credit tables: it says whether credit is getting tighter or looser
and why, what the balance is made of and who is driving it, how much of the Selic is getting through,
what credit is adding to or taking from demand, and where leverage and defaults put a limit — and
turns that into the thesis and into what it tells monetary policy, activity and fiscal.

| # | Question | What the answer covers | Where to look |
|---|---|---|---|
| C1 | O crédito está apertando ou afrouxando, e por oferta ou por demanda? | Rates, spreads and concessions read together, price against quantity; the banks' own reading (PTC: supply standards and demand, observed and expected, and the surprise against what they expected); defaults and the banks' risk appetite as a cause of supply moves; the direction by segment (households, large firms, small firms, housing), with the reading told to PM as **the credit condition** | 2.1, 2.5, 2.9 |
| C2 | De que é feito o saldo e quem puxa o crescimento? | A real decomposition of the total balance and of its growth: free against directed and public against private banks (market against policy); households against firms and the modalities (consumption, investment, working capital, trade); firm size, activity and type of client; bank credit against the capital markets and external debt. What each cut says, and the contribution of each part to the total's growth | 2.2, 2.3, 2.4, 2.6 |
| C3 | A Selic está chegando ao crédito, e com que defasagem? | Lending rates against the policy rate and the curve, by modality; the spread and what moves it; new loans against the stock; the part of the book outside the market rate (directed, regulated rates, caps); the lag, measured with a G, never assumed. The reading of how much transmission is working, told to PM, which concludes on the stance | 2.5, 2.6 |
| C4 | Qual o impulso de crédito, e de onde ele vem? | The impulse in its two measures — off the financial flow (the BCB's) and off the stock — and where they disagree; its composition (households and firms, free and directed, public and private banks, firm size, activity); its path over the horizon, told to activity, which concludes on the gap | 2.7, 2.2, 2.3 |
| C5 | Endividamento, comprometimento de renda e inadimplência estão virando limite? | Household leverage and debt service against income, with and without mortgages; defaults and arrears by segment, modality, firm size and bank control; risk classification; whether the limit binds on demand (borrowers cannot take more) or on supply (banks will not lend more) | 2.8, 2.9 |
| C6 | Qual o cenário nos seis trimestres? | The thesis below: the path of the thesis variable by quarter, central, base band and tails, with what leads to each tail; the paths of conditions, of the impulse and of defaults over the horizon, for the agents that use them | the horizon; 2.1–2.10 |

### The horizon and the thesis — provisional, decided with the model

The system's theses are per quarter of the Structural Model, six quarters from the current one, with
the variable measured at the close of the quarter (`SISTEMA_AGENTES.md` III.III.i; in a cycle dated
2026-10-30, 4T26 to 1T28). Today **no credit variable enters the model**. Chat C has credit as a
candidate for a demand term outside the rate in the IS curve (H) — fiscal impulse, credit impulse or
financial flow, an intercept only if none fits —, parked until the result of the gap test
(`coordenacao/C_modelo.md`), and the user postponed the model decisions to before cycle 2. So the
thesis variable is **provisória, decide com o modelo**, with two candidates written down. **Until
the model decides, the thesis is (a), the credit impulse** (decided by the user, 2026-10-30): it is
what activity and the gap use, the same role the labour agent has; (b) stays as the alternative the
caller can choose (`tese=concessoes`).

1. **(a) The credit impulse, in the BCB's concept.** `cred_fluxo_financeiro` stores the **financial
   flow** of bank credit — concessions minus repayments, so only money that changed hands, without
   accrued interest, exchange-rate revaluation or write-offs — accumulated over 12 months, in % of GDP,
   total, households and firms. The impulse is its change over a year, `fluxo(t) − fluxo(t−12)`, in
   p.p. of GDP; at the close of a quarter it is the value of the quarter's last month. A negative flow
   is the normal state (borrowers repay more than they borrow); a rising flow is a positive impulse.
   **For:** it is the change in credit's contribution to spending, which is what moves demand, and it
   is the form an IS term would take. **Against:** it is not an SGS series but a chart of the RPM's
   statistical annex, published once a quarter with a lag and revised by vintage; the BCB does not
   publish the impulse itself; and **the Sep/2026 RPM came without the chart, so the series stops in
   2026-04** — today it can neither start the quarter in course nor be scored. The stand-in while it
   is stuck is the impulse off the stock, `[S(t) − S(t−12)]/PIB12m(t) − [S(t−12) − S(t−24)]/PIB12m(t−12)`
   on `cred_credito_resumo` with `atv_pib_mensal`: monthly and current, but a balance grows by accrued
   interest, revaluation of dollar-linked loans and the absence of write-offs too, so it can print an
   impulse with no new lending.
2. **(b) Real growth of new concessions.** Total concessions (`cred_credito_resumo`), deflated by the
   IPCA, the quarter's three months summed against the same quarter a year earlier, in %. **For:**
   monthly, current (to 2026-09), an SGS series with small revisions, and a direct read of new lending
   that responds to the Selic and to supply quickly. **Against:** concessions are gross — a refinancing
   or a renegotiation is a new concession and nothing changed hands net —; the published total leaves
   out card credit and debt renegotiation, which the modality tables carry; it is noisier and does not
   measure the net push to demand. **Method pending, decided with the model.**
3. **The central follows the model's design.** If the model gets a credit term as an exogenous path,
   this agent writes it, the central is its base path and the rule of the fiscal and external agents
   applies (tutela in the "Exógenas" tab of `repository/agent_mapping/data_tracker.xlsx`); if the
   model gets an equation for it, the central is the model's, without adjustment. **If credit does not
   enter the model**, the fiscal and external rule says the thesis is the base path of the exogenous
   variables this agent tutors — **none today**. For that case (decided 2026-10-30), the same
   as the labour map's: the agent writes its own central path of the chosen variable, outside the model
   and outside P, with base band and tails, scored the same way, so the report keeps a falsifiable
   number.
4. **Upside and downside** (position only, as for every thesis, `SISTEMA_AGENTES.md` III.III.i):
   upside is the variable above the base band — more credit pushing demand —, downside below it — credit
   contracting. The report says in words what each means for Brazil: the upside tail is more activity
   and more inflation pressure, and, when it comes from households borrowing against stretched income,
   it builds the limit of C5; the downside tail is a credit crunch for activity and the disinflationary
   one, worse when it comes from supply (banks retreating after defaults) than from demand.
5. **Scoreboard:** for (a), the value in the first RPM edition that publishes the quarter's last month
   (none while the chart is absent: the report says so); for (b), the first publication of the
   quarter's last month in `cred_credito_resumo`.
6. **What is this agent's whether or not anything enters the model:** the credit condition told to PM
   (C1, C3), the impulse and its composition told to activity (C4), and the directed and public-bank
   growth told to fiscal (C2) — every report, as readings.

---

## Part 2 — Causal skeleton

**Where credit enters the Structural Model** (`analytics/agent_system/modelo.py`, `listar`). Nowhere,
today. The IS curve (H) writes the gap as its own lag plus the tightening of the previous quarter —
the quarterly Selic minus the anchor `rr_10a + meta` —, so **the part of credit that is the Selic's own
effect is already inside the coefficient of the tightening (`H.h2`)**; there is no credit, spread or
financial-conditions term. This agent's readings therefore reach the system in two ways: as **tempero
of type (ii) on the gap**, for the part that is not the Selic's effect — a supply shock, directed
credit, a default cycle, a renegotiation programme —, which the activity agent decides; and as
**tempero of type (i)**, when the agent argues that transmission through credit is stronger or weaker
than the estimated `H.h2` (a larger directed share, a curve that already moved), which it argues to
activity, owner of (H), who applies it. Every argument says which of the two it is, or the same thing
is counted twice. The credit condition also reaches PM directly, as the reading behind its stance.

### Block A — conditions and composition (C1, C2)

#### 2.1 Credit conditions: supply against demand

- **Mechanism.** A credit condition is a price and a quantity, and the two together say who moved.
  Rates and spreads rising while concessions fall is supply tightening — banks charging more and lending
  less; rates falling while concessions fall is demand weakening — borrowers not wanting; rates and
  volumes rising together is demand pulling. Supply moves with the funding cost (the curve), with banks'
  capital and expected losses (defaults, 2.9), with regulation and with competition; demand moves with
  income, confidence, investment plans and the rate itself. The spread is the bank's margin over its
  funding: expected losses, taxes and reserve requirements, administrative cost and profit; a spread
  widening with stable funding is the supply side moving. The banks' survey (PTC) asks the question
  directly: how standards for approving credit changed and how demand changed, by segment, and what
  they expect for the next quarter. The surprise — what happened against what the panel itself expected
  one quarter earlier — says whether banks are being caught out.
- **Read:** [[credit_channel]], [[financial_accelerator]], [[financial_conditions_index]];
  `credit_supply_demand`.
- **Data:** `cred_credito_resumo` (rates, spreads, ICC, concessions seasonally adjusted, by resource
  and segment), `cred_ptc` (supply and demand by segment, observed and expected), the four
  `cred_modalidade_*` (rate and concession by modality), `cred_inadimplencia_pj` (rate and concessions
  of firms); consultation of `br_interest_rate` (the DI curve, the funding benchmark).
- **Model:** outside the model; the condition is told to PM (CE-PM1) and the part that is not the
  Selic's effect to activity (CE-AT1).
- **Trap.** Quantity alone is a weak test: read price and quantity together. The PTC is the
  **unweighted mean of answers coded −2 to +2**, not a share of banks; its panels are small and of
  different sizes by segment, so a move of one respondent is a visible step in a small panel — never
  compare amplitudes across segments. The expected value of quarter *t* is about *t+1*: the surprise
  pairs `observada(t)` with `esperada(t−1)`. The rate of new loans (`taxa_juros`) and the cost of the
  stock (ICC) are different things. Concessions are seasonal and nominal: use the adjusted series or
  the same month a year earlier, and deflate with a G that says by what.

#### 2.2 Free against directed, public against private banks: market against policy

- **Mechanism.** Brazilian credit has two halves priced in different places. **Free credit** is priced
  off the market curve plus a spread and allocated by banks' risk appetite: it carries the Selic and
  the cycle. **Directed credit** — housing, rural, the BNDES and microcredit — is funded by earmarked
  sources (savings deposits, a share of demand deposits, public funds and the Treasury) and priced at
  regulated or administered rates: it responds to government decisions and to the funding available,
  much less to the Selic. Funding links back to the rate: when the Selic is high, earmarked funding
  whose return is capped by rule can lose deposits and squeeze housing credit even with demand intact
  (a hypothesis to measure). **Public banks** hold most directed credit and can lend against the cycle
  by decision; private and foreign banks follow risk and return. So the split of growth between free
  and directed, and between public and private banks, says how much of the credit cycle is market and
  how much is policy — and how much of the book the Selic does not reach (2.6).
- **Read:** [[credit_channel]], [[natural_rate_of_interest]]; `directed_credit`,
  `quasi_fiscal_operations`.
- **Data:** `cred_credito_resumo` (balance, concessions, rate, spread and defaults by free and directed,
  households and firms; the share in GDP), `cred_modalidade_direcionado_pf`,
  `cred_modalidade_direcionado_pj` (housing and rural at market and regulated rates, BNDES by purpose,
  programmes for small firms, microcredit), `cred_credito_controle_capital` (balance, defaults and
  provisions of public, private national and foreign banks, since 1988).
- **Model:** outside the model; the measured growth is told to fiscal (CE-FS1) and to PM (CE-PM2).
- **Trap.** **The decision is fiscal's, the measure is this agent's**: the size of a programme, a
  Treasury loan to the BNDES or a capitalization comes from fiscal (CR-FS1); never attribute directed
  growth to a policy decision the data and fiscal do not show — harvests and the housing cycle move
  directed credit too. "Public banks lend against the cycle" is a pattern to measure with a G over
  `cred_credito_controle_capital`, with the episodes and the window, not to assert.

#### 2.3 Households against firms, and the modalities: consumption, investment, working capital

- **Mechanism.** The modality says what the credit finances, and so where it lands in demand. On the
  household side: payroll-deducted credit (to public servants, retirees and private employees) is cheap
  and low-risk because the instalment comes out of a wage or benefit, and is tied to holding a formal
  job or a benefit; non-payroll personal credit, vehicles and other goods finance durable consumption;
  card revolving and overdraft are the expensive credit people fall into, so their growth reads as
  distress more than as demand; housing (2.2) finances residential investment. On the firm side:
  working capital and receivables discounting finance production and trade and move with the cycle and
  with small firms' liquidity; investment credit (mostly BNDES, 2.2) finances capital formation; export
  advances (ACC) and import and export finance follow trade and the exchange rate. By firm size, large
  firms can replace bank credit with bonds and external debt (2.4), small ones cannot, so a supply
  squeeze shows in small firms first. By activity, credit to agriculture, industry and services, and to
  their subsectors, says which sectors are borrowing to invest or to survive. By type of client, credit
  to the public sector (federal, state and municipal) is a slice of the bank balance that is neither
  household nor firm.
- **Read:** [[credit_channel]], [[financial_accelerator]]; `household_leverage`.
- **Data:** `cred_modalidade_livre_pf`, `cred_modalidade_livre_pj` (balance, concessions, rate and
  defaults by modality, since 1994 for the balance), `cred_credito_porte` (small and medium against
  large firms: balance, defaults, risk classification), `cred_credito_atividade_economica` (firms'
  balance by sector and subsector), `cred_credito_tipo_cliente` (private households and firms against
  the public sector); consultation of `atv_pmc` (vehicles, furniture and appliances), `atv_pim_uso`
  (durables and capital goods), `atv_pib` (household consumption and investment).
- **Model:** outside the model; the composition of growth is part of C2 and of the impulse (C4).
- **Trap.** Contributions to growth add up only for balances (levels in R$), never for rates or
  default ratios. Small modalities swing by hundreds of percent on a tiny base: read them by level and
  weight. A modality total can overlap a cross-cutting aggregate (revolving and non-revolving rebuild
  the household total), so checking both double-counts. Dollar-linked modalities (export advances,
  external onlending) grow in reais when the real depreciates. The balance by size and by activity
  covers firms only, and its aggregate does not match the firms' total of the resource tables to the
  decimal.

#### 2.4 Beyond the banks: capital markets and external funding

- **Mechanism.** Bank credit is one source among several. Firms also borrow by issuing bonds at home
  (debentures, securitized paper) and abroad, and through external loans; when the bank channel
  tightens, or when the market prices debt more cheaply than the banks, large firms move to the market.
  So a bank balance falling with the broad credit stable is substitution, not tightening; both falling
  together is. External funding brings the global cycle and the exchange rate in: it is cheap when
  global conditions are loose and expensive in reais when the real weakens.
- **Read:** [[credit_channel]], [[global_financial_cycle]].
- **Data:** `cred_credito_amplo` (credit to the non-financial sector — government, firms and households
  — by instrument: loans of the financial system, other lenders and public funds, domestic bonds and
  securitization, external debt in the domestic and foreign markets, since 2013).
- **Model:** outside the model; part of C1 (substitution against tightening) and C2.
- **Trap.** The broad credit and the financial system's credit are different universes — the first
  includes government securities and external debt that never touch a bank — and do not reconcile.
  External debt in reais moves with the exchange rate (CR-CB1) without any new borrowing.

### Block B — transmission (C3)

#### 2.5 From the Selic to lending rates: pass-through, the spread and the lag

- **Mechanism.** A fixed-rate loan is priced off the curve at the loan's tenor, not off today's Selic,
  so lending rates move when the market prices the Selic path — often before the Copom acts — and the
  spread on top moves with risk and competition. Floating-rate credit, much of it to firms, reprices
  with the policy rate at once. The stock reprices slowly, as old loans mature and new ones come in at
  the new rate, so the average cost of the book lags the rate on new loans. From the rate to the
  quantity there is a second lag: demand and approvals adjust over months, and the effect on spending
  later still. Pass-through is incomplete or slow where rates are capped or regulated, where the loan
  is collateralized by a wage (payroll credit) and where banks hold market power; it can be larger
  than one for one in a tightening when expected losses rise with the rate (the financial accelerator).
- **Read:** [[credit_channel]], [[monetary_transmission_lags]], [[financial_accelerator]],
  [[term_premium]]; `interest_rate_pass_through`.
- **Data:** `cred_credito_resumo` (rates and spreads of new loans by resource and segment, the
  non-revolving cut, the ICC), the four `cred_modalidade_*` (rate by modality),
  `cred_inadimplencia_pj` (firms' rate, with the Selic alongside); consultation of `pm_copom_reuniao`
  (the Selic) and `br_interest_rate` (the DI curve at one and two years, the funding benchmark of most
  free credit).
- **Model:** the Selic's effect through credit is inside `H.h2`; the reading of how much of it is
  getting through is told to PM (CE-PM1), and a transmission stronger or weaker than the estimate is
  argued to activity as type (i) on `H.h2` (CE-AT1).
- **Trap.** **The lag is a measurement, not a number to remember**: a G over the cycle's A (lending
  rates against the Selic and the curve, by modality, over the Selic cycles in the data) gives it, with
  the window. Compare lending rates with the curve at the loan's tenor, not only with the Selic. The
  Selic stored in `cred_inadimplencia_pj` is PM's variable: read it, never conclude on its path. With
  long lags, today's credit is not the effect of today's Selic.

#### 2.6 The part the Selic does not reach: directed credit and the potency of policy

- **Mechanism.** Directed credit at regulated rates does not move with the Selic, so the larger its
  share of the book and of growth, the less a point of Selic does to total credit — and the higher the
  Selic needed for the same effect on demand, which is one reason the neutral rate is argued to be
  higher in Brazil. Parafiscal decisions (Treasury loans to the BNDES and public banks, equalization
  subsidies, programmes) expand that part by decision; a primary result that improves while parafiscal
  credit grows is a smaller consolidation than it looks (fiscal's 2.5). This agent measures the part
  and its growth; the decision and its size are fiscal's, and the conclusion on the stance and the
  neutral is PM's.
- **Read:** [[credit_channel]], [[natural_rate_of_interest]], [[fiscal_impulse]];
  `directed_credit`, `quasi_fiscal_operations`.
- **Data:** `cred_credito_resumo` (directed share in balance, concessions and growth),
  `cred_modalidade_direcionado_pf`, `cred_modalidade_direcionado_pj`,
  `cred_credito_controle_capital`; consultation of `fisc_dlsp_fatores` (the Treasury's credits to
  official financial institutions) and `fisc_rtn` (equalization subsidies to rural, export and
  investment credit).
- **Model:** outside the model; told to PM (CE-PM2), to fiscal (CE-FS1) and, as a weaker or stronger
  `H.h2`, to activity (CE-AT1).
- **Trap.** "Directed credit weakens transmission" is a mechanism; how much it did here is a G
  (free against directed rates and volumes over the Selic cycles). **Do not count the parafiscal push
  twice**: fiscal measures it from the Treasury side, this agent from the lending side; the activity
  agent gets one push, and the report says which measure it is.

### Block C — the impulse (C4)

#### 2.7 The credit impulse: what credit adds to demand, and where it comes from

- **Mechanism.** Spending financed by credit depends on the **flow** of new net credit, not on the
  stock; so the push to demand is the **change** of that flow — the credit impulse. A stock that keeps
  growing at a slower pace means a negative impulse: credit still finances spending, but less than a
  year before. Measured off the financial flow (the BCB's concept), the impulse counts only money that
  changed hands; measured off the stock, it also counts accrued interest, the revaluation of
  dollar-linked loans and the absence of write-offs, so a balance can grow without any new lending.
  Because the stock-based measure is linear in the balance and shares one denominator, it splits
  exactly into its parts — households and firms, free and directed, public and private banks, firm
  size, activity —, which is where it says **where the impulse comes from**. The impulse reaches the gap
  through consumption and investment, with lags; that effect is the activity agent's conclusion.
- **Read:** [[credit_channel]], [[fiscal_impulse]] (the same logic on the fiscal side),
  [[output_gap]]; `credit_impulse`.
- **Data:** `cred_fluxo_financeiro` (the financial flow in % of GDP over 12 months, total, households,
  firms), `cred_credito_resumo` and `cred_credito_porte`, `cred_credito_atividade_economica`,
  `cred_credito_controle_capital` (the stock-based impulse and its decompositions); consultation of
  `atv_pib_mensal` (nominal GDP over 12 months, the denominator).
- **Model:** outside the model today; the candidate for a demand term in (H) (Part 1, the horizon). The
  measured impulse and its path over the horizon are what this agent gives activity (CE-AT1).
- **Trap.** **`cred_fluxo_financeiro` stops in 2026-04**: the Sep/2026 RPM came without the chart, and
  the loader reloads the last edition that published it. Check the last observation every cycle; while
  it is stuck, use the stock-based impulse and say so, with its bias. The flow is negative in normal
  times: a negative flow is not a negative impulse. Two vintages of the flow chain with a seam; the
  impulse points whose window crosses it carry the revision. The stock-based impulse is only as current
  as `atv_pib_mensal`: with GDP a month behind, the last month is missing, not zero. The impulse is a
  24-month object (t, t−12, t−24): a Selic cycle read beside one point does not explain it.

### Block D — the limits (C5)

#### 2.8 Household leverage and debt service

- **Mechanism.** Households can keep borrowing as long as the debt service fits their income. Leverage
  (debt over income) moves slowly; the debt service (interest plus amortization over income) moves
  faster, with rates and maturities: a higher Selic raises the service of the floating and the new
  debt, a shorter maturity raises it for the same debt, and long mortgages lower it. When the service
  takes a high share of income, households cut new borrowing and consumption even if banks would lend —
  a limit on demand —, and defaults rise when income falls (employment, real wages: MT). Payroll credit
  shifts risk from income to the job, and expensive revolving credit grows when budgets are stretched.
- **Read:** [[credit_channel]], [[financial_accelerator]], [[natural_rate_of_unemployment]];
  `household_leverage`, `debt_service_ratio`.
- **Data:** `cred_credito_familias` (leverage over 12-month income, with and without mortgages; debt
  service, total, without mortgages, and interest only); `cred_modalidade_livre_pf` (revolving, overdraft,
  payroll); consultation of `mt_pnad` (the real wage bill), `mt_caged` (formal employment),
  `inflc_agregados` (the deflator).
- **Model:** outside the model; the limit on consumption is told to activity (CE-AT2) and the default
  outlook takes employment and income from MT (CR-MT1).
- **Trap.** The service ratio moves with rates and maturities, not only with leverage: decompose before
  calling it a leverage problem. The table runs a month behind the other credit tables. The income in
  the denominator is the BCB's measure, not the PNAD's wage bill: they will not match. Employment and
  income are MT's: read, never conclude.

#### 2.9 Defaults, provisions and the credit cycle

- **Mechanism.** Defaults lag the cycle: loans made in a boom go bad when income or rates turn, so
  rapid growth today is a candidate for defaults later — a hypothesis the agent checks with a G, not a
  rule. Rising expected losses raise spreads and tighten standards, which squeezes borrowers whose
  balance sheets are already weak — the financial accelerator — and can turn a slowdown into a credit
  crunch. Banks' provisions and capital decide how much loss they can absorb before cutting supply.
  Small firms, revolving household credit and unsecured personal credit show stress first; payroll and
  housing last. Early arrears (15 to 90 days) and the risk classification of the book are candidates
  for leading signals, to be measured before used as such.
- **Read:** [[financial_accelerator]], [[macroprudential_policy]], [[economic_uncertainty]];
  `credit_cycle`.
- **Data:** `cred_credito_resumo` (defaults above 90 days by resource and segment),
  `cred_inadimplencia_pj` (firms' defaults and 15–90 day arrears), `cred_credito_porte` (defaults and
  higher-risk balance by firm size), `cred_credito_controle_capital` (defaults and provisions by bank
  control), the four `cred_modalidade_*` (defaults by modality).
- **Model:** outside the model; part of C1 (supply) and C5, told to PM (CE-PM1) and activity
  (CE-AT1).
- **Trap.** **The higher-risk balance has a methodology break**: the old classification ends in
  2024-12 and the one under the new accounting rule starts in 2025-01, with no overlap — never splice
  them. A default ratio falls when the balance grows fast even with the same bad loans (denominator):
  read the level of bad loans too. Whether 15–90 day arrears lead the 90-day series is a G, not a fact.
  Defaults after a renegotiation programme can fall by reclassification, not by recovery.

### Block E — rules, programmes and events

#### 2.10 Regulation, government programmes and the calendar

- **Mechanism.** Credit moves by decision as well as by the cycle: reserve requirements and
  macroprudential measures (BCB), accounting and provisioning rules, caps on rates or charges of some
  modalities, the rules of payroll credit (who can borrow, the ceiling for retirees and pensioners, new
  forms for private employees), renegotiation programmes for indebted households, housing programmes,
  the crop plan's rural credit, the long-term rate of the BNDES, taxes on credit operations. Each one
  changes supply, demand or the measured numbers without passing through the Selic. An event is never a
  premise: it is the motive of a path, and its size comes from data or from the owner of the decision.
- **Read:** [[macroprudential_policy]], [[jurisdictional_uncertainty]]; `directed_credit`.
- **Data:** none in the database: the rules, caps, programmes and their dates are not stored. The agent
  reads their effect in the F(A) (a modality jumping, a default ratio falling on reclassification),
  asks fiscal for the government's programmes (CR-FS1, CR-FS2) and PM for what the Copom documents say
  (CR-PM2), and declares the rest as a gap.
- **Model:** outside the model; tempero (ii) on the gap through activity.
- **Trap.** Never write a rule, a cap or a programme's size from memory. A programme already in the
  numbers is not news: read how much the modality moved before saying what it adds.

### Where the agent reads the data

The agent reads every table of its list through `obsidian/ciclos/<date>/dados/F_credito.md`, fixed for
the cycle (module `analytics/agent_system/dados/credito.py`, to be built in chat B's B2). Besides each
table's reading, the F is meant to carry what no single table gives: the two impulses side by side,
with the date of the last observation of each (2.7); real concessions and their growth (Part 1, (b));
the decomposition of the balance's growth by resource × segment, by bank control, firm size and
activity (2.2, 2.3); the PTC surprise, observed against the previous quarter's expectation (2.1); and
lending rates against the DI curve at one and two years (2.5). The lag of pass-through and the leading
power of arrears stay a G until promoted.

---

## Part 3 — Outputs: what this agent tells the others matters to it

Each row is what this agent needs from that agent, every cycle; it becomes an input row in that
agent's map (window B3). The external agent gets no fixed row: global conditions reach credit through
the curve (PM) and the exchange rate (câmbio), and through firms' external debt in the broad credit; a
cycle that needs more asks in the report.

### 3.1 To política monetária

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| CR-PM1 | **The Selic path and what the curve prices** (the PM thesis, and the DI path at one and two years against it) | Fixed-rate lending rates price off the curve at the loan's tenor, floating ones off the Selic; transmission (C3) is read against both, and the path decides the debt service of the floating book (C5) | The path or the curve moves by a step or more, or the curve and the PM thesis diverge | 2.5, 2.8 |
| CR-PM2 | **How the Copom and the BCB read credit**: the Copom's language on credit, transmission and financial conditions (comunicado, ata, RPM, including the RPM's credit analyses and the fate of the financial-flow chart), and BCB measures that act on credit outside the Selic (reserve requirements, macroprudential, provisioning rules) | Confronts this agent's reading of conditions with the Copom's; a BCB measure changes supply without the Selic moving (2.10); the impulse's source depends on the RPM | The Copom changes its language on credit, the BCB announces a measure, or an RPM brings back or drops a credit chart | 2.1, 2.7, 2.10 |

### 3.2 To atividade

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| CR-AT1 | **The output-gap path and GDP growth by quarter**, with nominal GDP | Credit demand follows income and activity, defaults follow the cycle (2.9); nominal GDP is the denominator of every impulse and share of GDP (2.7) | The gap changes sign or is revised materially, or GDP is revised | 2.1, 2.7, 2.9 |
| CR-AT2 | **Household consumption and investment, and the credit-sensitive indicators** (vehicles, furniture and appliances, durables, capital goods) | They are what credit finances: the check of C2's composition and of whether the impulse is reaching spending | The credit-sensitive indicators move against the impulse, or investment turns | 2.3, 2.7 |

### 3.3 To fiscal

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| CR-FS1 | **The parafiscal decisions and their size**: Treasury loans and capitalizations to the BNDES and public banks, equalization subsidies, the crop plan, housing and credit programmes for firms, with dates | "Fiscal decides, credit measures": directed and public-bank growth (2.2, 2.6) is read against the decision behind it, and a decision is the motive of a path | A programme is announced, changes or ends, or a capitalization or Treasury loan is decided | 2.2, 2.6, 2.10 |
| CR-FS2 | **Government rules for household credit**: payroll-credit rules and ceilings, renegotiation programmes, taxes on credit operations | They move household supply, demand and defaults without the Selic (2.8, 2.10), and are not in the database | A rule or a programme is decided, changed or expires inside the horizon | 2.8, 2.9, 2.10 |

### 3.4 To mercado de trabalho

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| CR-MT1 | **Formal employment, unemployment and real income** (the thesis and the wage bill) | They drive household default and the capacity to borrow (C5); payroll credit depends on formal jobs, so a formal-job loss and a credit cut reinforce each other | Formal jobs fall or real income turns | 2.8, 2.9 |

### 3.5 To inflação

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| CR-IN1 | **The IPCA path** (quarter and 12 months) | It deflates concessions and balances (Part 1, (b)), turns nominal lending rates into real ones, and moves the income behind debt service | The path moves enough to change real credit growth or real lending rates | 2.1, 2.5, 2.8 |

### 3.6 To expectativas

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| CR-EP1 | **The consensus Selic and IPCA by year** (the Focus) and their revisions | The expected Selic and inflation price fixed-rate credit and give the ex-ante real lending rate; a revision moves lending rates before the Selic moves | The consensus revises the Selic or the IPCA for the next two years | 2.5 |

### 3.7 To câmbio

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| CR-CB1 | **The exchange-rate path and whether a move is persistent** | Dollar-linked loans (export advances, external onlending) and firms' external debt are revalued in reais: the stock-based impulse counts it as credit, and the broad credit moves with it (2.3, 2.4, 2.7) | A large or persistent move of the real | 2.4, 2.7 |

**What this agent tells the others (their side, to be confirmed in their maps in B3).** The credit
condition — supply against demand, by segment — and how much of the Selic reaches it, to PM; the
directed share and public-bank growth, for PM's stance and fiscal's parafiscal reading; the credit
impulse, its composition and its path, and the transmission argument on `H.h2`, to activity; household
leverage and debt service, to activity; credit supply to small and medium firms, to the labour
market.

---

## Part 4 — Inputs: what the others told this agent matters to them

The mirror of what the other maps ask of credit today, written from this side. Until now PM, activity
and fiscal read credit as TWA in a channel, with no row, because credit had no agent; those inputs are
**proposed** and marked so, and become rows in those maps in B3. The labour map, drafted the same day,
already has one row (MT-CR1; its household-credit row was removed with its credit channel by the
user, 2026-10-30). FX, inflation, external and expectations ask nothing of credit today (the
expectations map says so; FX and external read credit nowhere).

| # | Source row | What the other agent needs | Why it matters to it | How this agent answers |
|---|---|---|---|---|
| CE-PM1 | PM 2.10 (credit TWA, no row); **proposed** | **The credit condition and how much of the Selic is reaching it**: rates and spreads against the curve, concessions, the banks' reading of supply and demand, defaults, by segment | "Credit: conditions; PM: stance" — PM concludes on the stance and efficacy reading the condition this agent delivers; credit aggregates alone are a weak test of the channel | C1 and C3, channels 2.1, 2.5 and 2.9: the condition by segment, supply against demand, and the pass-through reading with its lag (G); flag it when conditions turn against the Selic's direction, or a supply squeeze starts without the Selic |
| CE-PM2 | PM 2.5 and 2.10 (directed credit and the neutral; the Copom's note on free long-term credit falling while directed grows); **proposed** | **The part of credit the Selic does not reach**: the directed share and public-bank growth, and their trend | A larger directed share weakens the potency of policy and is argued to raise the neutral | C2 and C3, channels 2.2 and 2.6: the share and the contribution of directed and public-bank credit to growth; flag it when directed credit accelerates while free credit slows, or a parafiscal programme changes |
| CE-AT1 | Activity 2.2 (credit TWA, "the credit impulse in the RPM's concept"; no row); **proposed** | **The credit impulse per quarter and its path**, by component, and the part of credit that is not the Selic's own effect (a supply shock, directed credit, a default cycle) | (H) has no credit term: the Selic's effect through credit is in `H.h2` and the rest is tempero (ii) on the gap; the activity agent concludes on the effect | C4, channel 2.7 (with 2.2–2.3 for the composition), saying which measure and its last date; the argument on `H.h2` from 2.5–2.6 as type (i); flag it when the impulse changes sign, or supply moves independently of the Selic |
| CE-AT2 | Activity 2.4 and 2.6 (household debt service; investment funding outside the banks and the BNDES); **proposed** | **Household debt service and leverage, and the funding of investment** (BNDES, bonds, external debt) | Debt service decides how long households can keep consuming; investment depends on funding as well as on the cost of capital | C5 and C2, channels 2.8, 2.4 and 2.2: leverage and service with and without mortgages; investment credit and the broad credit; flag it when debt service rises or investment funding dries up |
| CE-FS1 | Fiscal 2.5 (credit TWA, no row); **proposed** | **How much directed credit and the public banks grow**, against the decision behind it | "Fiscal decides, credit measures": a primary that improves while parafiscal credit grows is a smaller consolidation than it looks | C2, channels 2.2 and 2.6: growth and share of directed credit by modality and of public banks, measured on the lending side; flag it when directed or public-bank credit accelerates or slows sharply |
| CE-MT1 | Labour MT-CR1 (its sectoral channel 2.6) | **Credit supply to small and medium firms**: the banks' reading of supply for them, and working capital | When credit to small firms locks, the firms whose bank cut credit fire more — a composition effect the labour agent watches in its sectoral reading; the aggregate effect of rates and credit on jobs goes through growth (its Okun channel), not through this row | C1 and C2, channels 2.1 and 2.3: small and medium firms' supply in the PTC (observed, expected and the surprise), working-capital rate and concessions, balance and defaults in `cred_credito_porte`; flag it when supply to small firms tightens or working-capital rates jump |

---

## Part 5 — Concept index

Belongs to chat D (`coordenacao/D_conhecimento.md`): the concept index and the layer 1 of this
agent's literature come after Parts 1–4 are approved.
