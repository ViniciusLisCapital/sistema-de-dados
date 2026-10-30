# Monetary Policy — Conceptual Map

**Status (2026-10-22):** Parts 1 to 4 approved by the user on 2026-10-21 (central questions, horizon,
the tails, outputs and inputs with FX, mirrored in the exchange-rate map). Adjusted on 2026-10-22 to
the batch of seven agents (`SISTEMA_AGENTES.md` III.III.vii): the tails are upside and downside;
expectations, the output gap, the fiscal premium and the Fed path have owners now, and the readings
of channels 2.3, 2.4, 2.5–2.6 and 2.8 that belong to them come through the rows of 3.2; the
pass-through row (now S7, in 3.2) went to inflation. The rows of 3.2, with the other five agents, were approved by
the user on 2026-10-22. Layer 1 of this agent's material is chosen in a separate step
(`PLANO_AGENTES.md`, Phase 2) and is not decided here.

**What this file is.** This is the monetary-policy agent's contract with the rest of the system. It
says what every report must answer (Part 1, central questions), what moves the Selic decision
(Part 2), what this agent tells the others matters TO IT (Part 3, outputs), and what the others told
this agent matters TO THEM (Part 4, inputs). Part 5 is the index of concepts read out of the
literature. The agent reads Parts 1–4 on every run and uses Part 5, the concept pages, the syntheses
and `clean_md/` to go deeper.

**How the parts connect to the rest of the vault.** `[[concept]]` links go to `concepts/`; a name in
`code` font is a concept the literature uses that has no page yet (listed in Part 5). "Mental models"
cite section numbers of [[verde_mp_mental_models]] ("Verde §2.1"), read from the Verde letters of the
2021–2022 tightening cycle: frameworks, not current opinions; a view dated 2022 is a way of
reasoning, never a fact about today. "Data" names MySQL tables of this agent's approved list
(`SISTEMA_AGENTES.md`, section V.II). The Copom's own documents (comunicados, atas, RPM) are this
agent's bibliography, in `clean_md/central_bank/`; which of them a cycle reads is set in
`SISTEMA_AGENTES.md` II.III.ix.

**Outputs and inputs.** An output of agent A to agent B is what A tells B is important for A, coming
from B. An input of A from B is what B told A is important for B, coming from A. So this agent's
outputs to FX (Part 3) are the FX agent's inputs from monetary policy (FX map, Part 4, rows E1–E6),
and this agent's inputs from FX (Part 4) are the FX agent's outputs to monetary policy (FX map,
Part 3, rows S1–S4); the same holds with the other five agents of the batch (3.2, 4.2). Each row here
carries its label in the other map, so the mirror can be checked line by line. A row is a request;
the content flows the other way: the FX agent's reading of the exchange rate reaches this agent
through the rows of Part 3. An input gives emphasis and tells the agent what to flag; it never limits
the analysis.

**Two layers.** What is written here is the **fixed** layer: what matters every cycle. On top of it,
each cycle has a **dynamic** layer, set by the theses of that cycle's reports: an agent whose thesis
hinges on something asks for it explicitly in its report. The dynamic layer lives in the reports, not
in this file.

**Data rule** (`SISTEMA_AGENTES.md` I.III.ix–xii, III.III.vii, V.II; regrouped 2026-10-22).
*Endogenous*: the Copom's calendar, decisions and projections, the B3 curves and the inflation
target. *Endogenous of another agent*, read for consultation: this agent draws no conclusion about
them, and the owner's position arrives through Part 3 — FX (the exchange-rate tables); expectations
(the Focus and the QPC; the Selic the curve prices stays this agent's conclusion, Q3); inflation (the
IPCA, its decomposition and the IC-Br in reais); activity (the national accounts, the monthly
indicators, the BCB output gap and its vintages, which moved here from this agent's own data, and,
provisionally, the labour market); fiscal (the fiscal accounts and the CDS, which was the exogenous
example); external (US rates, the peers' policy rates and real rates, the dollar indices, Brent and
the IC-Br in dollars). On the gap this agent keeps how the Copom reads it and reacts. *TWA*
(temporarily without agent): credit only, used with the premises stated in the report. No exogenous
data is left. The table-by-table list, with why each table matters, is V.II.

**Exogenous paths of the model: the tutela is in the tracker, not here.** Who writes the path of each
exogenous input of the Structural Model (the target, the 10-year real yield, the CDS, the Fed funds,
…) is set by the user in the "Exógenas" tab of `repository/agent_mapping/data_tracker.xlsx`, one
level per agent. The consolidation (P) uses the path of whoever has the tutela; a path this agent
writes without it becomes a logged divergence, answered in the next round (`SISTEMA_AGENTES.md`
IV.ii). The multiplier on a coefficient of the interest-rate rule (R) is this agent's to apply,
because it owns the equation, even when another agent argues for it; a multiplier on another
equation (I, E, H, F) is argued here and applied by its owner (III.III.vii).

Curation material (sources and their status, owners, clusters, gaps) lives in
`repository/agent_mapping/data_tracker.xlsx` (the Qual - Monetary Policy and Notes tabs), not here.

---

## Part 1 — Central questions: what every report answers

**Approved by the user, 2026-10-21; refocused the same day after the first solo test.** The questions
are the floor, not the ceiling: the agent is expected to go beyond them, and nothing here limits what
it may say. They are kept in Portuguese, the language of the report.

The agent does not describe the Copom: it confronts three things — what it thinks the Copom **will**
do, what it thinks the Copom **should** do given the data, and what the **market** prices —, and the
Copom's own signalling is one more piece of evidence in that confrontation.

| # | Question | What the answer covers | Where to look |
|---|---|---|---|
| Q1 | O que o Copom vai fazer? | The agent's forecast of the decisions, read from the Copom's documents (the reaction function, the projection at the relevant horizon against the target, the balance of risks, the guidance) and from the data; which input is moving the decision, and whether the Copom is acting as its usual reaction implies or departing from it | 2.1, 2.2–2.8 |
| Q2 | O que o Copom deveria fazer, pelos dados? | The agent's own reading of what the data ask for: inflation against the target and its persistence; the gap; expectations and credibility (the reading the FX agent asks for, Part 4, E2); the stance, the ex-ante real Selic against the neutral the Copom uses, the Structural Model's anchor and the literature's range; transmission and what weakens it | 2.2–2.6, 2.10 |
| Q3 | O que o mercado precifica, e onde isso diverge do que o Copom vai fazer, do que deveria fazer e do que ele mesmo sinaliza? | The DI curve meeting by meeting, the Focus and the QPC; expected path against premium; against Q1, Q2 and the Copom's projections and conditioning paths; the room for surprise at the next meetings | 2.9, 2.1 |
| Q4 | Qual o cenário prospectivo para a Selic? | The report's thesis on the horizons below: central from the Structural Model's base scenario; distribution from the agent's tempero, shaped by Q1; the risk that comes from the distance between what the Copom will do and what it should do (Q1 against Q2) | report §1, 2.1 |

- The Copom's relevant horizon (first quarter of 2028 at the 281st meeting) falls today on the last
  of the model's six quarters; the projection there is what Q1 reads.

### The horizon — approved by the user, 2026-10-21

The system's theses are per quarter of the Structural Model, six quarters from the current one, with
the variable measured at the close of the quarter (`SISTEMA_AGENTES.md` III.III.i). The Selic does
not move inside a quarter as the PTAX does: it changes only at Copom meetings, about two per quarter,
and its value at the close of a quarter is the outcome of the meetings inside it. III.III.i allows an
exception for this agent. The rule:

1. **The thesis variable is the Selic target at the close of each of the six quarters**, i.e. the
   decision of the last meeting inside the quarter (`pm_copom_calendario`). It is comparable with the
   PTAX close, with the scoreboard and with what the FX agent asks for (Part 4, E1).
2. **The next two quarters are also written meeting by meeting, as discrete decisions**: for each
   meeting, the probability of each step (hold, −25, −50 bp, …). The decision is discrete, and a
   continuous range hides that. The quarters after that use the system's format (central, base range
   and tails with probabilities); their close is the sum of the steps.
3. **The central is the model's close in every quarter.** Equation (R) of the Structural Model works
   with the quarterly *average* Selic, while the FX equation (F) was estimated with the quarter
   *close*. The model's close is derived mechanically, the mean of this quarter's and the next one's
   average (`modelo.py`, "Selic, fechamento do trimestre (derivada)"). The meeting path of the first
   two quarters is the agent's, and it shapes the distribution around the central. The Copom's step
   size is not fixed (the 2021–2022 cycle moved 75, 100 and 150 p.b. per meeting), so a central far
   from today's Selic is not by itself out of reach.
4. **Scoreboard**: for each closed quarter, the band in which the close fell; for each meeting, whether
   the decision was the step the agent gave the highest probability.
5. **Upside and downside** (decided 2026-10-22 for every agent, replacing worst and best): upside is
   the Selic above the base range, downside below it — position only; the asymmetry is
   P(upside) − P(downside). The report says in words when a tail is good or bad for Brazil: an upside
   Selic usually means inflation, expectations or fiscal worse than assumed, and a downside from a
   lenient Copom (Verde §2.6, the BC "dócil") is not good news.
6. **The Fed funds rate is not a thesis variable of this agent.** It is the external agent's: its path
   comes from whoever has its tutela in the "Exógenas" tab, and the Fed path and the global cycle
   reach this agent through S13; FOMC meetings matter only as events.

---

## Part 2 — Causal skeleton: what moves the Selic decision

Section 2.1 is how the inputs combine into a decision; 2.2–2.10 are the inputs.

### 2.1 The reaction function: forecast targeting, rule and inertia

- **Mechanism.** Inflation targeting is in practice inflation-forecast targeting: the central bank
  sets the rate so that its projection at the control-lag horizon returns to the target, and the
  weight on activity only sets how fast (Svensson 1997, 2010); the BCB adopted that logic at the
  start (Bogdanski et al. 2000). Descriptively, the policy rate responds more than one-for-one to
  expected inflation, with strong inertia: BCB estimates for 1999–2004 show both (Minella et al.
  2002, 2003; Favero & Giavazzi 2004). Inertia can be optimal under commitment, because small
  persistent moves act on long rates (Woodford 1999). A rule is an input, not the decision: Taylor
  (1993) shows the literal rule giving the wrong answer to a temporary oil shock.
- **Read:** [[inflation_forecast_targeting]], [[taylor_rule]], [[taylor_principle]],
  [[interest_rate_smoothing]], [[targeting_rules]], [[time_inconsistency]], [[monetary_policy_shocks]],
  [[real_time_data]].
- **Mental models:** Verde §2.3 (the BC pushed by the curve), §2.6 (the "dócil" BC).
- **Data:** `pm_copom_reuniao`, `pm_copom_calendario`, `pm_copom_projecoes`, `inflc_meta`, and the
  Copom documents.
- **Trap.** An estimated rule mixes the Copom's behaviour with the forecasts it used
  (Christiano, Eichenbaum & Evans 1999), and real-time data give different coefficients from revised
  data (Orphanides 2001). Equation (R) of the Structural Model reacts to the Focus deviation from
  target and is anchored on the 10-year real yield plus the target: it is the model's reaction
  function, not the Copom's.

### 2.2 Inflation against the target at the relevant horizon

- **Mechanism.** The projection, not current inflation, decides. Supply shocks: the Copom
  accommodates their first-round effects and reacts to second-round effects (ata of the 281st
  meeting, §16; the BCB's "adjusted target" practice in Minella et al. 2002, 2003). Administered
  prices carry higher exchange-rate pass-through and backward indexation (Minella et al.); services
  are the most sensitive to the gap and the most inertial (RPM Sep/2026, 2.3). Since 2025 the target
  is continuous: 12-month IPCA checked every month, breached after six consecutive months outside the
  band (Decreto 12.079/2024, as described in the RPM's institutional section).
- **Read:** [[inflation_targeting]], [[inflation_persistence]], [[administered_prices]],
  [[core_inflation]], [[food_inflation_drivers]], [[divine_coincidence]], [[nk_phillips_curve]],
  [[exchange_rate_pass_through]].
- **Mental models:** Verde §2.5 (supply shocks and calibration), §2.4 (lags), §2.6 (a target met by
  tax cuts is a deferred cost).
- **Data:** `pm_copom_projecoes`, `inflc_meta`; inflation's, for consultation, `inflc_agregados`,
  `inflc_decomposicao`, `inflc_decomposicao_item`, `inflc_dim`, `comm_icbr`; external's `comm_brent`.
  The IPCA path, its persistence and what drives it come from the inflation agent (S8), and so does
  pass-through (S7).
- **Trap.** The reference-scenario projection is conditional on paths set by governance — the Focus
  Selic, a PPP exchange rate, oil futures — which "não necessariamente refletem o cenário mais
  provável" (RPM Sep/2026, 2.3). Read as the Copom's forecast, it confuses the conditioning with the
  view.

### 2.3 Expectations, anchoring and credibility

- **Mechanism.** Without commitment, discretion produces an inflation bias, which is why credibility
  needs institutions: rules, a conservative central banker, contracts (Kydland & Prescott 1977;
  Barro & Gordon 1983; Rogoff 1985; Walsh 1995). An announced target can de-link long-run
  expectations from news (Blinder et al. 2008; Svensson 2010). In Brazil the regime's first test was
  read on expectations converging to the target, and broke in late 2002 when its continuation was in
  doubt (Minella et al. 2002, 2003). The Copom's current reading: deanchored expectations require
  "restrição monetária maior e por mais tempo" (ata of the 281st meeting, §10).
- **Read:** [[time_inconsistency]], [[conservative_central_banker]], [[inflation_contract]],
  [[central_bank_communication]], [[inflation_targeting]], [[inflation_expectations_anchoring]].
- **Mental models:** Verde §1.1 (a promise of discipline without a framework holds only if decisions
  corroborate it), §2.6.
- **Data:** expectations', for consultation, `expc_focus`, `expc_focus_periodo` (IPCA), `expc_qpc`;
  `br_interest_rate` (nominal and real, so implied inflation by a G; the conclusion on the implied
  inflation is the expectations agent's, III.III.vii); `inflc_meta`.
- **Trap.** Expectations are not this agent's (I.III.xii): the anchoring reading — the path of the
  12-month expectation, the long horizons against the target — comes from the expectations agent
  (S9). What this agent keeps is how the Copom reacts to it. Anchoring is judged two or three years
  ahead, free of the short-run effect of current shocks (RPM Sep/2026, 2.3); a short-horizon rise
  after a supply shock is not by itself deanchoring.

### 2.4 Output gap, activity and labour market

- **Mechanism.** Demand above potential raises inflation (the New Keynesian Phillips curve); the gap
  is unobserved and revised, and the Copom's gap blends several methods with judgement (RPM
  Sep/2026, 2.2). Wages: with sticky wages, unemployment fluctuations and a wage Phillips curve in the
  unemployment gap (Galí 2015, ch. 6–7); the Copom watches wages growing above productivity (ata of
  the 281st meeting, §7).
- **Read:** [[nk_phillips_curve]], [[natural_rate_of_unemployment]], [[sticky_wages]],
  [[real_time_data]].
- **Mental models:** Verde §2.4 (real income loss and lags; the curve and the BC looking at current
  inflation).
- **Data:** all the activity agent's since 2026-10-22, for consultation: `pm_hiato_produto`,
  `pm_hiato_produto_vintages`, `atv_pib`, `atv_pib_taxas`, `atv_pib_valores_correntes`, `atv_ibcbr`,
  `atv_pim`, `atv_pim_uso`, `atv_pmc`, `atv_pms`, and, provisionally, the labour market `mt_pnad`,
  `mt_desocupacao_retro`, `mt_caged`, `mt_caged_setor`; expectations' `expc_qpc` (the market's gap).
  The gap path and its revision come from the activity agent (S10); this agent keeps how the Copom
  reads the gap and reacts to it (III.III.vii).
- **Trap.** Real-time gap estimates differ materially from revised ones (Orphanides 2001), so a gap
  revision changes the projection with no new data (`pm_hiato_produto_vintages`). Filters fold a long
  slump into potential (Krugman 1998). A slowdown is in the Copom's base scenario; only a faster one
  is a downside risk (RPM Sep/2026, 2.3).

### 2.5 Neutral rate and the stance

- **Mechanism.** The stance is the ex-ante real rate against the neutral. The neutral is latent,
  low-frequency and time-varying, tied to trend growth and other persistent factors, with a large
  global component (Laubach & Williams 2003; Holston, Laubach & Williams 2017). Brazil's fell in the
  decade to 2013 with lower public debt, lower sovereign risk, financial deepening and lower global
  rates (Perrelli & Roache 2014); public saving is the strongest lever, and a country premium remains
  unexplained (Segura-Ubiergo 2012). The Copom uses one value in its reference scenario, checks
  alternatives (RPM Sep/2026, 2.2), and holds that weaker fiscal discipline, directed credit and debt
  uncertainty raise it (ata of the 281st meeting, §8). The Structural Model's anchor is the 10-year
  real yield plus the target, and it reads the stance the way the Copom can: when the 10-year real
  yield falls because the fiscal risk premium compresses, the market is pricing a fiscal
  consolidation ahead — slower spending, less demand pressure, weaker growth and lower inflation —,
  so the same Selic becomes tighter against the demand to come and opens room to cut. Much of
  Brazil's very high real rate is the counterpart of fiscal demand pressure (Verde §1.1). When the
  model moves the Selic through this anchor, the report argues the economic story first, and only
  then says where it disagrees (user, 2026-10-21).
- **Read:** [[natural_rate_of_interest]], [[taylor_rule]], [[real_time_data]],
  [[jurisdictional_uncertainty]], [[term_premium]]; `directed_credit`.
- **Mental models:** Verde §1.1 (the structural Selic level is conditional on the fiscal anchor),
  §2.2 (a real rate too high does not last: inflation or the nominal rate adjusts).
- **Data:** `br_interest_rate`, `br_di_grade`, `inflc_meta`; for consultation, expectations'
  `expc_focus_periodo` (Selic) and `expc_focus`, external's `cmb_real_rates` (peers), activity's
  `atv_renda_poupanca`, fiscal's `fisc_divida`. The reading of the fiscal premium in the long rates —
  is the consolidation they price credible, how much demand it takes out — comes from the fiscal
  agent (S11); the `rr_10a` path, from whoever has its tutela.
- **Trap.** Every estimate is imprecise. A mismeasured neutral is costly under a passive rule and
  largely self-correcting under an activist one (Perrelli & Roache 2014, against Orphanides' result
  for the gap). The model's anchor is a market yield that carries term and fiscal premia, not the
  Copom's neutral: the two stances can disagree, and the report says which one it uses.

### 2.6 Fiscal policy and fiscal dominance

- **Mechanism.** Fiscal policy acts in the short run on demand and, structurally, on the perception
  of debt sustainability and the term premium (ata of the 281st meeting, §8). In the extreme, a rate
  rise raises default risk and depreciates the currency, so inflation targeting becomes perverse —
  more likely the higher the debt, its dollar share and risk aversion (Blanchard 2004); whether a
  global shock turns into a vicious circle depends on whether the primary surplus responds to debt
  (Favero & Giavazzi 2004). No fiscal dominance is a prerequisite of inflation targeting in emerging
  markets (Mishkin 2000).
- **Read:** [[fiscal_dominance]], [[risk_premium]], [[mundell_fleming_policy_mix]], [[term_premium]].
- **Mental models:** Verde §1.1 ("acelerador fiscal com freio monetário"), §1.2 (spending → debt and
  FX → inflation → rates), §2.1 (fiscal and electoral premium in the curve), §2.6.
- **Data:** fiscal's, for consultation, `fisc_nfsp`, `fisc_divida`, `fisc_dlsp_fatores`, `fisc_rtn`,
  `fisc_efgg`, `cmb_risco_pais` (the CDS, no longer exogenous); activity's `atv_pib_mensal`
  (denominator).
- **Trap.** Fiscal dominance is a spectrum, not a switch. Blanchard's estimate is for 2002, with
  dollar-linked debt; in Segura-Ubiergo's panel gross debt is not a robust determinant of real rates
  while the fiscal balance is. The fiscal reading is the fiscal agent's (S11, S12): the impulse,
  the debt dynamics, the CDS path and which fiscal path the market is pricing. A compression of the
  fiscal premium in the long rates is a demand story as well as a risk story (2.5). This agent keeps
  the efficacy of monetary policy under fiscal dominance (Blanchard 2004, I.III.xvii).

### 2.7 The exchange rate, read through inflation

- **Mechanism.** The exchange rate matters to the Copom through inflation and expectations: the
  reference scenario starts from a recent rate and follows PPP, and "uma taxa de câmbio
  persistentemente mais depreciada" is an upside risk (comunicado of the 281st meeting). In the BCB's
  original design the rate reaches inflation fastest through the exchange rate (Bogdanski et al.
  2000). In the open-economy New Keynesian model optimal policy stabilizes domestic inflation and
  accepts large exchange-rate swings (Galí & Monacelli 2005; Galí 2015, ch. 8); in emerging markets
  the exchange rate is not ignored but subordinated to the target (Mishkin 2000).
- **Read:** [[exchange_rate_pass_through]], [[uip]], [[carry_trade]], [[overshooting]],
  [[fx_intervention]], [[currency_regimes]].
- **Mental models:** Verde §1.2 (fiscal → exchange rate → inflation), §4.2 (the rate differential
  supporting the currency).
- **Data:** FX endogenous, for consultation: `cmb_ptax`, `cmb_fx_latam`, `cmb_reer`,
  `cmb_reservas_bc`, `cmb_cambio_contratado`, `cmb_balanco_pagmt`, `cmb_cot_fx`, `cmb_termos_troca`,
  `cmb_comex_fator_agregado`, `cmb_comex_pais`, `cmb_comex_produto`, `diferenciais_juros`;
  expectations' `expc_focus_periodo` (câmbio); `pm_copom_projecoes`.
- **Trap.** This agent draws no conclusion about the exchange rate (I.III.x): persistence, global
  against idiosyncratic and the risk premium come from the FX agent (Part 3). Pass-through, its
  literature and the question, belongs to the inflation agent (IV.i), and reaches this agent through
  S7. And the sign of the rate → exchange rate link is
  not given: under fiscal stress a hike can depreciate (2.6).

### 2.8 Global rates and spillovers

- **Mechanism.** US policy and global risk appetite move emerging-market risk premia, flows and long
  rates. A float keeps substantial short-rate independence but long rates co-move under any regime
  (Obstfeld 2015); Rey (2013) argues that with free capital the trilemma becomes a dilemma. The
  other-owner sources add the channel and the dispute: US tightening raises country risk and weakens
  the pass-through of the policy rate to market rates, with free floats better insulated than managed
  ones (Kalemli-Özcan 2019); floaters are as exposed in credit and flows (Miranda-Agrippino & Rey
  2020). The Copom cites external uncertainty and monetary policy in advanced economies (comunicado
  of the 281st meeting).
- **Read:** [[global_financial_cycle]], [[financial_trilemma]], [[capital_controls]],
  [[macroprudential_policy]], [[risk_premium]], [[uip]].
- **Mental models:** Verde §3.1–3.4 (global rates, central banks behind the curve, the
  inflation–growth pendulum, global rates as the discount rate), §4.2.
- **Data:** external's, for consultation, `us_interest_rate`, `inter_interest_rate`, `cmb_real_rates`,
  `cmb_dollar_index`, `cmb_dollar_index_em`, `comm_brent`, `comm_icbr_usd`; FX endogenous
  `diferenciais_juros`.
- **Trap.** The Fed path and the global cycle are the external agent's (S13): the Fed funds path in
  step 1 comes from whoever has its tutela, and it is not a conclusion of this agent.

### 2.9 Communication, the curve and the market's path

- **Mechanism.** Statements move the expected path and long yields more than the decision itself
  (Gürkaynak, Sack & Swanson 2005). Guidance can be a forecast (Delphic) or a commitment (Odyssean)
  (Campbell et al. 2012). A surprise can carry the central bank's information about the economy, and
  then markets move "the wrong way" (Nakamura & Steinsson 2018); the co-movement of rates and stocks
  separates the two (Jarociński & Karadi 2020). The term premium separates the expected path from
  compensation for risk (Adrian, Crump & Moench 2013). The Copom's current guidance: the size of the
  "ciclo de calibração" is set by new information (comunicado of the 281st meeting).
- **Read:** [[forward_guidance]], [[central_bank_communication]], [[information_effect]],
  [[monetary_policy_shocks]], [[term_premium]].
- **Mental models:** Verde §2.1 (premium in the curve above the expected cycle; "há prêmio
  suficiente?"), §2.2, §2.3.
- **Data:** `br_di_grade` (the Selic priced meeting by meeting), `br_interest_rate`,
  `pm_copom_calendario`; expectations', for consultation, `expc_focus_copom`, `expc_focus_periodo`
  (Selic), `expc_qpc`. The Selic the curve prices, against the survey, stays this agent's conclusion
  (Q3, III.III.vii); the expectations agent asks for it (4.2, E20).
- **Trap.** The DI path is not the expected path: it carries term and risk premia (Verde §2.1;
  Favero & Giavazzi find default risk in Brazilian swap term premia). The reference scenario uses the
  Focus Selic, not the Copom's intended path. A surprise is read with the other prices that moved
  with it, not with the curve alone.

### 2.10 Transmission: credit, financial conditions and lags

- **Mechanism.** Credit-market frictions amplify the rate: the external finance premium moves with
  the policy rate and with borrowers' net worth (Bernanke & Gertler 1995; Bernanke, Gertler & Gilchrist
  1999), and banks' loan supply is a channel of its own (Bernanke & Blinder 1988). Effects on prices
  take long, and longer where finance is more developed (Havranek & Rusnak 2013); the BCB staff put
  6–9 months through demand and a contemporaneous effect through the exchange rate in 2000 (Bogdanski
  et al.). Directed credit leaves part of the market outside the policy rate (Segura-Ubiergo 2012, a
  conjecture); the Copom notes free long-term credit falling while directed credit keeps growing (ata
  of the 281st meeting, §6).
- **Read:** [[credit_channel]], [[financial_accelerator]], [[monetary_transmission_lags]],
  [[macroprudential_policy]]; `directed_credit`.
- **Mental models:** Verde §4.1 (the Selic level and the discount rate of domestic assets), §2.4,
  §3.4.
- **Data:** TWA credit `cred_credito_resumo`, `cred_fluxo_financeiro`, `cred_ptc`,
  `cred_credito_familias`, `cred_credito_amplo`, `cred_modalidade_livre_pf`,
  `cred_modalidade_livre_pj`, `cred_modalidade_direcionado_pf`, `cred_modalidade_direcionado_pj`,
  `cred_credito_controle_capital`, `cred_inadimplencia_pj`.
- **Trap.** Credit aggregates are a weak test of the channel: conditions are measured by the premium,
  not by the quantity (Bernanke & Gertler 1995). The BCB's financial conditions index is not a measure
  of monetary stimulus and its link to inflation is ambiguous (RPM Sep/2026, 2.2, footnote 48). With
  long lags, today's inflation is not the effect of today's Selic.

### Reading a Copom document with this skeleton (checked on the 281st meeting, Sep/2026)

A check that the skeleton covers what the Copom says it watches, not content of the fixed layer; the
agent reads the current documents. Every element of the comunicado, the ata and the RPM of that
meeting has a channel:

| What the Copom cites | Channel |
|---|---|
| Projection at the relevant horizon (1Q28) in the reference scenario; Focus Selic, PPP exchange rate from a recent rate, oil futures and the tariff flag as conditioning | 2.1, 2.2, 2.7 |
| No reaction to the primary effects of supply shocks, firm reaction to second-order effects | 2.1, 2.2 |
| Expectations above target at every horizon; deanchoring requires more restriction for longer | 2.3 |
| Activity moderating, labour market tight, wages above productivity, positive gap expected to turn negative | 2.4 |
| Neutral rate used in the projections, below the ex-ante real Selic along the whole path | 2.5 |
| Fiscal: short-run demand and the structural premium; reforms, directed credit and debt uncertainty raise the neutral | 2.6, 2.5 |
| A persistently more depreciated exchange rate as an upside risk; the real depreciating as the rate differential narrows (RPM) | 2.7 |
| External uncertainty, advanced economies' policy, commodities, a sharper global slowdown as a downside risk | 2.8 |
| "Ciclo de calibração" whose size depends on new information; "serenidade e cautela" | 2.9, 2.1 |
| Transmission accumulating; free long-term credit falling, directed credit growing; financial conditions index | 2.10 |

### Where the agent reads the data

The agent reads every table of the list through `obsidian/ciclos/<date>/dados/F_politica_monetaria.md`,
fixed for the cycle (`analytics/agent_system/dados`, which declares the tables of V.II). Besides the
reading of each table, it carries the Selic priced meeting by meeting on the DI curve and in the
Focus, side by side, and the ex-ante real rate against the QPC's neutral.

---

## Part 3 — Outputs: what this agent tells the others matters to it

### 3.1 To FX (fixed layer; approved by the user 2026-10-21)

What this agent needs from the FX agent, every cycle. These are the FX map's rows E1–E6, unchanged in
substance, written from this side. What the Copom cares about in the exchange rate is its effect on
inflation and expectations, not its level for its own sake (2.7).

| # | FX map | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|---|
| S1 | E1 | **Is the move persistent or transitory?** A judgement, with the reason, separating a level shift from noise | Pass-through depends on persistence; a transitory spike is looked through | A move the FX agent classifies as persistent, in either direction | 2.2, 2.7 |
| S2 | E2 | **Global or idiosyncratic?** The split of the FX agent's Q3 | An idiosyncratic depreciation usually comes with a higher risk premium, which also reaches expectations; a global one does not carry that signal | The idiosyncratic component dominates the month's move | 2.3, 2.6, 2.7 |
| S3 | E3 | **Where the BRL is relative to the Copom's conditioning assumption** (a recent rate, then PPP) | A gap between the market and that path is a risk to the projection | The gap widens in the direction the Copom lists as a risk | 2.1, 2.2 |
| S4 | E4 | **Risk premium reading.** Is the BRL pricing fiscal or institutional stress? | The same stress raises the neutral and weakens transmission (ata of the 281st meeting, §8) | CDS and BRL move together against peers | 2.5, 2.6 |
| S5 | E5 | **How much carry is supporting the BRL** | The exchange rate is one channel from the Selic to inflation; if carry stops working, that channel weakens | Carry and the BRL decouple | 2.10, 2.7 |
| S6 | E6 | **FX market functioning.** Liquidity, cupom cambial, central-bank intervention; whether there is dysfunction | Tells whether the BCB is using FX instruments rather than the rate, and whether an intervention answers dysfunction or defends the level (trigger of E4) | Intervention, a liquidity squeeze or a cupom cambial spike | 2.1, 2.7 |

**Decided by the user, 2026-10-21.**
- **Pass-through was provisional, and moved on 2026-10-22.** The pass-through literature belongs to the
  inflation agent (IV.i); the row is now asked of the inflation agent (3.2), and the FX agent tells
  the inflation agent about depreciation risk (I.III.xvii; inflation map IN-S1, IN-S2).
- **S6 (E6) keeps the cupom cambial.** The series is not in the data yet; it comes with the Bloomberg
  API (expected 2026-11-01). Until then the row is answered with reserves, interventions and the FX
  flow.

### 3.2 To the other agents of the batch (approved by the user, 2026-10-22)

What this agent needs from the other five, every cycle. Each row becomes an input in that agent's
map (its Part 4). They carry the readings of Part 2 that have owners now: pass-through and the drivers
of the projection (2.2) from inflation, anchoring (2.3) from expectations, the gap (2.4) from
activity, the fiscal premium and fiscal dominance (2.5, 2.6) from fiscal, the Fed path (2.8 and item 6
of the horizon) from external. What this agent keeps in each channel is the Copom's reading and its
reaction.

| # | To | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|---|
| S7 | Inflation (its IN-E1; was FX E3) | **Pass-through channel.** Which prices a depreciation reaches, and how fast: food, industrial goods, and administered prices through fuels, energy and medicines | The Copom projects free and administered prices separately, and their pass-through differs; it reacts to the second round, not the first | Always, as context for S1 | 2.2, 2.7 |
| S8 | Inflation | **The IPCA path and what drives it**: persistence (cores, diffusion, underlying services), administered prices and food, first round against second round | The projection at the relevant horizon decides, and the Copom accommodates the first-round effects of supply shocks and reacts to the second round (2.2) | The thesis moves at the relevant horizon, or the inflation agent reads a shock as spreading | 2.2, Q2 |
| S9 | Expectations | **The anchoring reading**: the path of the 12-month-ahead expectation (the expectations agent's thesis), the long horizons against the target, and whether a move is deanchoring or a short-run reaction to a shock | Deanchored expectations require "restrição monetária maior e por mais tempo" (ata of the 281st meeting, §10), and the rule (R) reacts to the Focus deviation from the target | The long horizons move away from the target, or the expectations agent's upside tail gains probability | 2.3, 2.1, Q2 |
| S10 | Activity | **The output-gap path** (the activity agent's thesis) **and its revision** in the latest RPM, with the labour market (unemployment, wages against productivity) | The gap enters the Copom's projection, and a revision moves the projection with no new data; the Copom watches wages growing above productivity (ata of the 281st meeting, §7) | The gap changes sign in the horizon, or the RPM revises recent quarters | 2.4, Q2 |
| S11 | Fiscal | **The fiscal premium in the long rates and the CDS path**: when the long rates move on the fiscal premium, is the consolidation they price credible, and how much demand does it take out; and the `rr_10a` path, if the fiscal agent has its tutela | `rr_10a` + meta is the anchor of the rule and of the IS curve: a compression of the premium tightens the same Selic and opens room to cut (2.5). The user expects this exchange to sharpen the stance reading (2026-10-21) | The long real yield moves on the fiscal premium, or the CDS path changes | 2.5, 2.6, Q2, Q4 |
| S12 | Fiscal | **The fiscal impulse and the fiscal-dominance reading**: the direction and size of the stimulus to demand, and whether the primary responds to the debt | Fiscal policy acts on demand in the short run; whether a global shock turns into a vicious circle depends on the primary responding to the debt (Favero & Giavazzi 2004) | The impulse changes sign, or the fiscal agent's adverse tail gains probability | 2.6, 2.10 |
| S13 | External | **The Fed path and the global cycle**: the Fed funds (`ffr`) and US inflation paths by quarter, base and tails, global risk appetite and the peers' policy cycle | US policy and global risk move emerging-market premia, flows and long rates (2.8); the Fed funds is an exogenous input of the model, written by whoever has its tutela | A change in the Fed path, a global risk-off, or a turn in the peers' cycle | 2.8, 2.5, Q4 |

- **Blanchard (2004) stays with this agent** because it asks about the efficacy of monetary policy
  under fiscal dominance (I.III.xvii); the fiscal agent owns the fiscal side of [[fiscal_dominance]].
- **Credit** has no agent yet: its data stay TWA (2.10), used with the premises stated in the report.

---

## Part 4 — Inputs: what the others told this agent matters to them

### 4.1 From FX (fixed layer; approved by the user 2026-10-21)

What the FX agent needs from this agent, every cycle: the FX map's rows S1–S4, written from this side.

| # | FX map | What the FX agent needs | Why it matters to FX | How this agent answers |
|---|---|---|---|---|
| E1 | S1 | **Expected path of the Selic and the balance of risks**, as this agent reads it (not only the Focus median) | The forward carry, which supports the BRL, is the differential ahead, not today's | The thesis of Q4 in the horizon format of Part 1 (quarter close; meeting by meeting for the next two quarters) |
| E2 | S2 | **Credibility reading: is a hike read as credibility or as validating inflation?** | Decides the sign of the rate → FX link | Q2, channels 2.3 and 2.6 |
| E3 | S3 | **How the Copom described the exchange rate at the last meeting**, filtered from the comunicado, ata and RPM | Tells whether the FX move is already inside the Copom's scenario or is news to it | The Copom documents of layer 1 (II.III.ix); channel 2.7 |
| E4 | S4 | **Reaction function to a depreciation.** Would the Copom respond with the Selic, and by how much? **Trigger:** if the BCB's posture turns to defending the exchange rate (intervention without signs of dysfunction, or communication about the level of the BRL), the question widens to the BCB's whole reaction function, intervention included, answered by both agents with this agent leading | A credible response caps the depreciation; its absence removes the cap. Under a defense posture what matters is the BCB's reaction function, not the technical state of the market | Q1, channels 2.1 and 2.2 (the second-order-effects test); under the trigger, 2.1 and 2.7 with the FX agent's reading of dysfunction (S6) |

**Decided by the user, 2026-10-21.**
- **E4 (S4) is triggered.** While the BCB intervenes only against dysfunction, intervention is the FX
  agent's channel (FX map 2.7, `cmb_reservas_bc`), and judging dysfunction is its job (S6); this agent
  answers on the rate. If the BCB's posture turns to defending the exchange rate, the reaction
  function, intervention included, becomes a question for both, led by this agent.
- **E1 (S1) follows the approved horizon.** The FX equation of the Structural Model was estimated with
  the Selic at the quarter close and the simulator uses the average; the close is what this agent
  gives (Part 1, horizon, item 3).

### 4.2 From the other agents of the batch (2026-10-22)

The mirror of what the other five maps ask of this agent in their Part 3 (approved by the user on
2026-10-22, in each agent's approval window), written from this side; the source row carries the
label in that map. Most of them ask for the thesis (the Selic path) and for what the Copom said, so
the answer is written once, in the report, and each row points to it.

| # | Source row | What the other agent needs | Why it matters to it | How this agent answers |
|---|---|---|---|---|
| E5 | Inflation IN-S3 | **The Selic path**, at each quarter close and meeting by meeting for the next two quarters | The Selic reaches inflation through the gap and the exchange rate with long lags; it is the loop that pulls the central back to the target | The thesis of Q4 in the horizon format of Part 1 |
| E6 | Inflation IN-S4 | **What the Copom projects for inflation and on which assumptions**: the reference-scenario projection by quarter, the administered-prices projection, and the conditioning paths it states (oil, the tariff flag, the exchange rate) | The inflation agent does not read the Copom's documents; the Copom's assumptions on administered prices are the best public calendar of those decisions | The Copom documents of layer 1 (II.III.ix) and `pm_copom_projecoes`; channel 2.2, with the conditioning read as conditioning, not as forecast |
| E7 | Activity S-PM1 | **The Selic path and its balance of risks**: average and close of each quarter | The Selic of each quarter is the tightening of the next one in the IS curve (H); this agent's tails shape the activity agent's | The thesis of Q4 and its tails; the quarterly average is the model's, the close is the thesis |
| E8 | Activity S-PM2 | **The stance**: how restrictive policy is against the neutral the Copom uses and against the model's anchor | (H) measures the tightening against `rr_10a` + meta; if the anchor carries premia the neutral does not, the effective tightening differs from the model's | Q2, channel 2.5, saying which neutral and why |
| E9 | Activity S-PM3 | **How the Copom read activity and the gap at the last meeting**, with the revision of the gap in the latest RPM | The model's starting point and the activity agent's thesis variable are the BCB's gap; a revision moves both without new data | The Copom documents of layer 1; channel 2.4 |
| E10 | Fiscal FS-PM1 | **The Selic path** at each quarter close | It sets the cost of the debt, the r of r − g, and the monetary half of the policy mix | The thesis of Q4 |
| E11 | Fiscal FS-PM2 | **How the Copom described fiscal policy**, from the comunicado, the ata and the RPM | Tells whether the Copom reads fiscal policy as a demand push, a premium or a neutral-rate question, and whether a fiscal move is already in its scenario | The Copom documents of layer 1; channels 2.5 and 2.6 |
| E12 | Fiscal FS-PM3 | **The split of the long real yield**: the expected real policy path and the term premium, against the fiscal premium (needed if the fiscal agent has the tutela of `rr_10a`) | Writing `rr_10a` is splitting it, and the policy part is this agent's | Channels 2.5 and 2.9: the Selic path of the thesis, the curve and the term premium ([[term_premium]]) |
| E13 | Fiscal FS-PM4 | **Credibility reading: is a hike read as credibility or as raising the risk of the debt?** | It is the monetary side of the fiscal-dominance test | Q2, channels 2.3 and 2.6 (the same reading E2 gives the FX agent) |
| E14 | External XS3 | **The Selic path** | Brazil's relative carry against the Fed and the peers, which decides whether Brazil gains or loses within the emerging-market carry trade | The thesis of Q4 |
| E15 | External XS4 | **How the Copom reads the external scenario**: its assessment, its balance of risks and the external conditioning of the reference scenario | Tells the external agent whether its scenario is already in the Copom's or is news to it; that agent does not read the Copom's documents | The Copom documents of layer 1; channel 2.8 |
| E16 | External XS6 | **The `rr_10a` path, and how much of it is US long rates** — asked of whoever writes `rr_10a` (fiscal or this agent, per the "Exógenas" tab) | Keeps the external agent's long-rate scenario consistent with the anchor that carries it into the gap | Only when this agent's path is the one the P uses for `rr_10a`; channel 2.5 |
| E17 | Expectations XS1 | **The reaction function to expectations above the target**: would the Copom respond, and how much; the Selic thesis | The anchor holds only if a response is expected; the survey's Selic path is judged against it | Q1, channels 2.1 and 2.3 |
| E18 | Expectations XS2 | **What the Copom said about expectations at the last meeting**: which horizons it watches, whether it calls them deanchored, its projection at the relevant horizon against the Focus | The expectations agent does not read the Copom's documents | The Copom documents of layer 1; channel 2.3 |
| E19 | Expectations XS3 | **The path of the target (`meta_12m`)** and any risk of the CMN changing it | It is the anchor term of the expectations equation (E); a change moves its rest point | The `meta_12m` path, written under the tutela of the "Exógenas" tab, and the CMN's decisions |
| E20 | Expectations XS4 | **The Selic the curve prices against the survey**, and the premium between them | Separates what the survey expects of the Selic from what the market charges, for the expectations agent's credibility test | Q3, channel 2.9 (the curve meeting by meeting against the Focus) |
| E21 | Activity S-FI2 | **The path of the 10-year real yield and of the fiscal premium in it** — asked of whoever has the tutela of `rr_10a` (fiscal or this agent, per the "Exógenas" tab) | `rr_10a` is the anchor of the tightening in (H): with the Selic given, a lower long real rate is a tighter policy, and its premium side is a cost of capital the model does not see | Only when this agent's path is the one the P uses for `rr_10a`; channel 2.5 |

---

## Part 5 — Concept index from the literature

The concepts of the monetary-policy bibliography, by the tracker's clusters. Each bullet links the
concept page (or names the concept in `code` font when it has no page) and the synthesis notes it
comes from. Sources owned by another agent (I.III.xvii) are marked *other owner*; this agent reaches
them through the concepts. Sources with a `clean_md` and no synthesis yet are listed at the end of
their cluster.

### #policy_rules_and_credibility — rules, discretion and the inflation bias

- [[time_inconsistency]] — the optimal plan is inconsistent once agents act; discretion is consistent and suboptimal. [[monetary_policy/synthesis/time_inconsistency_optimal_plans (Kydland & Prescott, 1977)]]
- [[time_inconsistency]] (inflation bias) — the discretionary Nash equilibrium has the natural rate of unemployment and inflation above the rule's; reputation as a fragile substitute. [[monetary_policy/synthesis/positive_theory_monetary_policy (Barro & Gordon, 1983)]]
- [[conservative_central_banker]] — delegate to an agent with a larger but finite weight on inflation. [[monetary_policy/synthesis/optimal_commitment_intermediate_target (Rogoff, 1985)]]
- [[inflation_contract]] — a transfer linear in inflation removes the bias without distorting stabilization. [[monetary_policy/synthesis/optimal_contracts_central_bankers (Walsh, 1995)]]
- [[taylor_rule]] — the rate on inflation and the output gap, as an input to judgement, not a formula. [[monetary_policy/synthesis/taylor_rule (Taylor, 1993)]]
- [[natural_rate_of_unemployment]], [[natural_rate_of_interest]] — no permanent trade-off; the authority cannot peg a real quantity. [[monetary_policy/synthesis/the_role_monetary_policy (Friedman, 1968)]]
- [[monetary_targeting]] — a monetary total as the guide; steady money growth. [[monetary_policy/synthesis/the_role_monetary_policy (Friedman, 1968)]], [[monetary_policy/synthesis/optimal_commitment_intermediate_target (Rogoff, 1985)]]
- `lucas_critique`, `seigniorage` — no page. [[monetary_policy/synthesis/time_inconsistency_optimal_plans (Kydland & Prescott, 1977)]], [[monetary_policy/synthesis/positive_theory_monetary_policy (Barro & Gordon, 1983)]]

### #new_keynesian_transmission — the model behind the rule

- [[nk_phillips_curve]] — inflation from expected inflation and the gap; hybrid curves with persistence. [[monetary_policy/synthesis/basic_nk_model_ch3 (Gali, 2015)]], [[monetary_policy/synthesis/science_of_monetary_policy (Clarida, Gali & Gertler, 1999)]]
- [[calvo_pricing]] — random price reset; the pricing block of the NK model. *Other owner (inflation):* [[inflation/synthesis/staggered_prices (Calvo, 1983)]]
- [[natural_rate_of_interest]] — the flexible-price real rate; the gap depends on the real rate against it. [[monetary_policy/synthesis/basic_nk_model_ch3 (Gali, 2015)]]
- [[taylor_principle]] — more than one-for-one response to inflation for a determinate equilibrium. [[monetary_policy/synthesis/classical_monetary_model_ch2 (Gali, 2015)]], [[monetary_policy/synthesis/monetary_policy_design_nk_ch4 (Gali, 2015)]]
- [[divine_coincidence]] — stabilizing inflation closes the gap absent cost-push shocks; breaks with them and with sticky wages. [[monetary_policy/synthesis/monetary_policy_design_nk_ch4 (Gali, 2015)]], [[monetary_policy/synthesis/discretion_vs_commitment_ch5 (Gali, 2015)]], [[monetary_policy/synthesis/sticky_wages_prices_ch6 (Gali, 2015)]]
- [[time_inconsistency]], [[targeting_rules]] — discretion against commitment; stabilization bias. [[monetary_policy/synthesis/discretion_vs_commitment_ch5 (Gali, 2015)]], [[monetary_policy/synthesis/science_of_monetary_policy (Clarida, Gali & Gertler, 1999)]]
- [[sticky_wages]], [[natural_rate_of_unemployment]] — wage rigidity, wage Phillips curve, unemployment in the NK model. [[monetary_policy/synthesis/sticky_wages_prices_ch6 (Gali, 2015)]], [[monetary_policy/synthesis/unemployment_nk_model_ch7 (Gali, 2015)]]
- [[uip]], [[international_risk_sharing]], [[overshooting]], [[currency_regimes]] — the small open economy; domestic against CPI inflation targeting against a peg. [[monetary_policy/synthesis/nk_small_open_economy (Gali & Monacelli, 2005)]], [[monetary_policy/synthesis/open_economy_monetary_policy_ch8 (Gali, 2015)]]
- `monetary_neutrality`, `friedman_rule` — no page. [[monetary_policy/synthesis/classical_monetary_model_ch2 (Gali, 2015)]]

### #inflation_targeting_regimes — the regime and its implementation

- [[inflation_targeting]] — numerical target, forecast-based implementation, transparency; flexible in practice; emerging-market prerequisites. [[monetary_policy/synthesis/inflation_targeting_handbook (Svensson, 2010)]], [[monetary_policy/synthesis/inflation_targeting_em (Mishkin, 2000)]]
- [[inflation_forecast_targeting]] — the forecast at the control-lag horizon as the intermediate target; publishing a rate path. [[monetary_policy/synthesis/inflation_forecast_targeting (Svensson, 1997)]], [[monetary_policy/synthesis/inflation_targeting_handbook (Svensson, 2010)]]
- [[targeting_rules]] — target rules over instrument rules. [[monetary_policy/synthesis/inflation_forecast_targeting (Svensson, 1997)]]
- [[price_level_targeting]] — no base drift; automatic stabilizer at the zero bound. [[monetary_policy/synthesis/inflation_targeting_handbook (Svensson, 2010)]]
- `liability_dollarization` — no page. [[monetary_policy/synthesis/inflation_targeting_em (Mishkin, 2000)]]

### #brazil_monetary_policy — the Brazilian regime

- [[inflation_targeting]], [[inflation_forecast_targeting]], [[monetary_transmission_lags]] — the 1999 design and the BCB's small structural model. [[monetary_policy/synthesis/implementing_it_brazil (Bogdanski, Tombini & Werlang, 2000)]]
- [[administered_prices]], [[inflation_persistence]], [[core_inflation]], [[exchange_rate_pass_through]] — first-round accommodation, adjusted targets, credibility judged by expectations. [[monetary_policy/synthesis/it_lessons_and_challenges (Minella et al., 2002)]], [[monetary_policy/synthesis/it_credibility_fx_volatility (Minella et al., 2003)]]
- [[fiscal_dominance]], [[risk_premium]], [[uip]] — a hike raising default risk and depreciating the real; the fiscal rule and the vicious circle; Brazil 2002. [[monetary_policy/synthesis/fiscal_dominance_it_brazil (Blanchard, 2004)]], [[monetary_policy/synthesis/it_and_debt_brazil (Favero & Giavazzi, 2004)]]
- [[jurisdictional_uncertainty]], [[capital_controls]] — the anti-creditor bias as the common cause of high short rates and no long credit. [[monetary_policy/synthesis/credit_interest_jurisdictional_uncertainty (Arida, Bacha & Lara-Resende, 2005)]]
- `directed_credit` — no page. [[monetary_policy/synthesis/high_interest_rates_puzzle_brazil (Segura-Ubiergo, 2012)]]
- No synthesis yet: [[monetary_policy/clean_md/samba_dsge_brazil (de Castro et al., 2011)]], [[monetary_policy/clean_md/samba_dsge_brazil_update (Fasolo et al., 2023)]], [[monetary_policy/clean_md/monetary_channels_brazil_semi_structural (Minella & Souza-Sobrinho, 2013)]], [[monetary_policy/clean_md/directed_credit_monetary_transmission (Bonomo & Martins, 2016)]]; *other owner (FX):* [[exchange_rate/clean_md/monetary_policy_fx_puzzle_em (Kohlscheen, 2014)]].

### #neutral_rate — the neutral and the stance

- [[natural_rate_of_interest]] — a low-frequency r* tied to trend growth, estimated jointly with potential; global co-movement. [[monetary_policy/synthesis/natural_rate_measurement (Laubach & Williams, 2003)]], [[monetary_policy/synthesis/natural_rate_international (Holston, Laubach & Williams, 2017)]]
- [[natural_rate_of_interest]], [[real_time_data]] — Brazil's neutral falling with debt, risk and deepening; activist rules self-correct mismeasurement. [[monetary_policy/synthesis/neutral_rate_time_varying_brazil (Perrelli & Roache, 2014)]]
- [[natural_rate_of_interest]], [[fiscal_dominance]] — saving, public saving and a residual country premium in Brazil's high rates. [[monetary_policy/synthesis/high_interest_rates_puzzle_brazil (Segura-Ubiergo, 2012)]]
- No synthesis yet: [[monetary_policy/clean_md/neutral_rate_brazil (Muinhos & Nakane, 2006)]].

### #reaction_function_and_gradualism — how the rule is estimated and why it is inertial

- [[taylor_principle]], [[interest_rate_smoothing]] — pre-Volcker accommodation against a two-for-one response after; partial adjustment. [[external/synthesis/monetary_policy_rules_stability (Clarida, Gali & Gertler, 2000)]]
- [[real_time_data]], [[taylor_rule]] — prescriptions and coefficients change with the data available at the time. [[monetary_policy/synthesis/policy_rules_real_time_data (Orphanides, 2001)]]
- [[interest_rate_smoothing]] — inertia as optimal commitment; super-inertial rules. [[monetary_policy/synthesis/optimal_monetary_policy_inertia (Woodford, 1999)]]

### #policy_surprises_and_information_effect — measuring what a decision does

- [[monetary_policy_shocks]], [[monetary_transmission_lags]] — the identified-VAR consensus on the effects of a tightening. [[monetary_policy/synthesis/monetary_policy_shocks_survey (Christiano, Eichenbaum & Evans, 1999)]]
- [[monetary_policy_shocks]], [[real_time_data]] — narrative shocks purged of the Fed's forecasts. [[monetary_policy/synthesis/new_measure_monetary_shocks (Romer & Romer, 2004)]]
- [[monetary_policy_shocks]], [[forward_guidance]] — target and path factors; statements drive long yields. [[monetary_policy/synthesis/policy_actions_vs_words (Gurkaynak, Sack & Swanson, 2005)]]
- [[information_effect]] — surprises revealing the central bank's view; separating it by the stock-market response. [[monetary_policy/synthesis/information_effect_hf_identification (Nakamura & Steinsson, 2018)]], [[monetary_policy/synthesis/information_shocks_policy_surprises (Jarocinski & Karadi, 2020)]]

### #communication_and_forward_guidance

- [[central_bank_communication]] — creating news and reducing noise; predictability; anchoring. [[monetary_policy/synthesis/central_bank_communication_survey (Blinder et al., 2008)]]
- [[forward_guidance]] — Delphic against Odyssean guidance; thresholds. [[monetary_policy/synthesis/forward_guidance_effects (Campbell et al., 2012)]]
- [[inflation_expectations_anchoring]] — whether long expectations stay at the target. [[monetary_policy/synthesis/central_bank_communication_survey (Blinder et al., 2008)]]

### #term_structure_and_market_pricing

- [[term_premium]] — the fitted yield minus the risk-neutral yield; level risk carries its variation. [[monetary_policy/synthesis/term_structure_linear_regressions (Adrian, Crump & Moench, 2013)]]

### #transmission_channels_financial_frictions

- [[credit_channel]] — the external finance premium; balance-sheet and bank-lending channels. [[monetary_policy/synthesis/credit_channel_transmission (Bernanke & Gertler, 1995)]], [[monetary_policy/synthesis/credit_money_aggregate_demand (Bernanke & Blinder, 1988)]]
- [[financial_accelerator]] — net worth amplifying shocks in a quantitative model. [[monetary_policy/synthesis/financial_accelerator (Bernanke, Gertler & Gilchrist, 1999)]]
- [[monetary_transmission_lags]] — the price trough across 67 studies; slower with financial development. [[monetary_policy/synthesis/transmission_lags_meta_analysis (Havranek & Rusnak, 2013)]]

### #unconventional_policy_zlb — the zero bound (not binding in Brazil; kept for the theory of commitment)

- [[zero_lower_bound]], [[forward_guidance]], [[time_inconsistency]] — the trap as a credibility problem in reverse; optimal history-dependent commitment. [[monetary_policy/synthesis/liquidity_trap_japan (Krugman, 1998)]], [[monetary_policy/synthesis/zero_bound_optimal_policy (Eggertsson & Woodford, 2003)]]
- [[unconventional_monetary_policy]], [[term_premium]] — expectations, balance-sheet size and composition. [[monetary_policy/synthesis/zero_bound_alternatives (Bernanke, Reinhart & Sack, 2004)]]
- [[unconventional_monetary_policy]], [[financial_accelerator]] — central-bank credit when intermediaries are constrained. [[monetary_policy/synthesis/unconventional_policy_model (Gertler & Karadi, 2011)]]
- `ricardian_equivalence`, `portfolio_balance_channel` — no page. [[monetary_policy/synthesis/liquidity_trap_japan (Krugman, 1998)]], [[monetary_policy/synthesis/zero_bound_alternatives (Bernanke, Reinhart & Sack, 2004)]]

### #global_spillovers_em_autonomy — how much room the Copom has

- [[global_financial_cycle]], [[capital_controls]], [[macroprudential_policy]] — the trilemma as a dilemma. [[monetary_policy/synthesis/dilemma_not_trilemma (Rey, 2013)]]
- [[financial_trilemma]], [[currency_regimes]] — floating buys short-rate independence, not long-rate independence. [[monetary_policy/synthesis/trilemma_tradeoffs (Obstfeld, 2015)]]
- [[global_financial_cycle]] — US policy driving the global factor; floaters exposed. *Other owner (external):* [[external/synthesis/us_monetary_policy_global_cycle (Miranda-Agrippino & Rey, 2020)]]
- [[risk_premium]], [[uip]] — international risk spillovers; free floats better insulated. *Other owner (FX):* [[exchange_rate/synthesis/us_policy_international_risk_spillovers (Kalemli-Ozcan, 2019)]]; `fear_of_floating` — no page.
- [[carry_trade]] — policy transmission to the exchange rate depends on carry positioning. *Other owner (FX):* [[exchange_rate/synthesis/monetary_policy_exchange_rates (BIS, 2026)]]
- No synthesis yet: [[monetary_policy/clean_md/two_targets_two_instruments (Ostry, Ghosh & Chamon, 2012)]]; *other owner (FX):* [[exchange_rate/clean_md/systematic_monetary_policy_forward_premium_puzzle (Tambakis & Tarashev, 2012)]].

### #institutional_framework and #brazil_policy_communication

- [[inflation_targeting]] — the legal frame: no synthesis yet for [[monetary_policy/clean_md/decreto_3088_metas_inflacao (Brazil, 1999)]], [[monetary_policy/clean_md/lc_179_autonomia_bcb (Brazil, 2021)]], [[monetary_policy/clean_md/decreto_12079_meta_continua (Brazil, 2024)]].
- The Copom's comunicados, atas and RPMs, in `clean_md/central_bank/`, outside the vault agent; their
  synthesis is an open design question (II.III.ix).
