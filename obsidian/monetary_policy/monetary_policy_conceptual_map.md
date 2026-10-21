# Monetary Policy — Conceptual Map

**Status (2026-10-21):** Parts 1 to 4 approved by the user on 2026-10-21 (central questions, horizon,
worst and best, outputs and inputs, mirrored in the exchange-rate map). Layer 1 of
this agent's material is chosen in a separate step (`PLANO_AGENTES.md`, Phase 2) and is not decided
here.

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
outputs to FX (Part 3) are the FX agent's inputs from monetary policy (FX map, Part 4, rows E1–E7),
and this agent's inputs from FX (Part 4) are the FX agent's outputs to monetary policy (FX map,
Part 3, rows S1–S4). Each row here carries its label in the FX map, so the mirror can be checked line
by line. A row is a request; the content flows the other way: the FX agent's reading of the exchange
rate reaches this agent through the rows of Part 3. An input gives emphasis and tells the agent what
to flag; it never limits the analysis.

**Two layers.** What is written here is the **fixed** layer: what matters every cycle. On top of it,
each cycle has a **dynamic** layer, set by the theses of that cycle's reports: an agent whose thesis
hinges on something asks for it explicitly in its report. The dynamic layer lives in the reports, not
in this file.

**Data rule** (`SISTEMA_AGENTES.md` I.III.ix–xii, V.II). *Endogenous*: the Copom's calendar,
decisions and projections, the BCB output gap and its vintages, the B3 curves and the inflation
target. *Endogenous of the FX agent*: the exchange-rate tables, read for consultation; this agent
draws no conclusion about them, and the FX agent's position arrives through Part 3. *TWA*
(temporarily without agent): expectations, inflation, activity, labour market, credit, fiscal and the
global data, used with the premises stated in the report. Inflation becomes the inflation agent's
when it exists (III.II.ii); expectations are not this agent's (I.III.xii). *Exogenous*: the CDS. The
table-by-table list, with why each table matters, is V.II.

Curation material (sources and their status, owners, clusters, gaps) lives in
`repository/agent_mapping/data_tracker.xlsx` (the Qual - Monetary Policy and Notes tabs), not here.

---

## Part 1 — Central questions: what every report answers

**Approved by the user, 2026-10-21.** The questions are the floor, not the ceiling: the agent
is expected to go beyond them, and nothing here limits what it may say. They are kept in Portuguese,
the language of the report.

| # | Question | What the answer covers | Where to look |
|---|---|---|---|
| Q1 | Qual é a função de reação do Copom, e a que ela está respondendo agora? | The projection at the relevant horizon against the target, the balance of risks, and which input is moving the decision (expectations, gap, supply shocks and their second-round effects, fiscal, exchange rate, external). Whether the Copom is acting as its usual reaction implies, or departing from it, and why | 2.1, 2.2–2.8 |
| Q2 | Quão restritiva está a política monetária, e contra qual juro neutro? | The ex-ante real Selic against the neutral the Copom uses, against the Structural Model's anchor and against the literature's range; what is moving the neutral (fiscal, directed credit, saving, global rates) | 2.5, 2.6, 2.8 |
| Q3 | A política monetária está chegando à inflação? | Credibility and transmission: whether expectations are re-anchoring, whether credit, activity and the labour market respond, and what weakens the channels (deanchoring, directed credit, fiscal stimulus) | 2.3, 2.4, 2.10, 2.6 |
| Q4 | Que trajetória de Selic o mercado precifica, e onde ela diverge da sinalização do Copom e da leitura do agente? | The DI curve meeting by meeting, the Focus and the QPC; expected path against premium; the room for surprise at the next meetings | 2.9, 2.1 |
| Q5 | Qual o cenário prospectivo para a Selic? | The report's thesis on the horizons below: central from the Structural Model's base scenario (equation R), distribution from the agent's tempero — for example, the rule reacting to the inflation deviation more strongly than estimated, as a multiplier on its coefficient (`SISTEMA_AGENTES.md` IV.ix) | report §1, 2.1 |

- Q2 and Q3 could be one question. They are split because the credibility reading of Q3 is an
  output the FX agent asked for (Part 4, E2), and because the Copom's current case for restriction is
  about expectations, not about the stance alone (ata of the 281st meeting, §10).
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
3. **The central still comes from the model, converted mechanically.** Equation (R) of the
   Structural Model works with the quarterly *average* Selic, while the FX equation (F) was estimated
   with the quarter *close* (`analytics/brasil/structural_model/CLAUDE.md`). The agent converts the
   model's base-scenario average path into a meeting path with a fixed G that places the steps on the
   meeting dates. The conversion is not tempero and does not move the central.
4. **Scoreboard**: for each closed quarter, the band in which the close fell; for each meeting, whether
   the decision was the step the agent gave the highest probability.
5. **Worst and best**: worst is the Selic above the central, best below it. A higher Selic than in the
   base scenario means inflation, expectations or fiscal worse than assumed. The caveat: a lower Selic
   from a lenient Copom (Verde §2.6, the BC "dócil") would score as best.
6. **The Fed funds rate is not a thesis variable of this agent.** It is a global (TWA) series, entered
   as an exogenous path in step 1 of the premises; FOMC meetings matter only as events.

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
  [[interest_rate_smoothing]], [[targeting_rules]], [[time_inconsistency]].
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
  [[core_inflation]], [[food_inflation_drivers]], [[divine_coincidence]], [[nk_phillips_curve]].
- **Mental models:** Verde §2.5 (supply shocks and calibration), §2.4 (lags), §2.6 (a target met by
  tax cuts is a deferred cost).
- **Data:** `pm_copom_projecoes`, `inflc_meta`; TWA inflation `inflc_agregados`,
  `inflc_decomposicao`, `inflc_decomposicao_item`, `inflc_dim`; TWA external `comm_brent`,
  `comm_icbr`.
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
  [[central_bank_communication]], [[inflation_targeting]]; `inflation_expectations_anchoring`.
- **Mental models:** Verde §1.1 (a promise of discipline without a framework holds only if decisions
  corroborate it), §2.6.
- **Data:** TWA expectations `expc_focus`, `expc_focus_periodo` (IPCA), `expc_qpc`; `br_interest_rate`
  (nominal and real, so implied inflation by a G); `inflc_meta`.
- **Trap.** Expectations are not this agent's (I.III.xii): it reads them and states its premises.
  Anchoring is judged two or three years ahead, free of the short-run effect of current shocks
  (RPM Sep/2026, 2.3); a short-horizon rise after a supply shock is not by itself deanchoring.

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
- **Data:** `pm_hiato_produto`, `pm_hiato_produto_vintages`; TWA expectations `expc_qpc` (the market's
  gap); TWA activity `atv_pib`, `atv_pib_taxas`, `atv_pib_valores_correntes`, `atv_ibcbr`, `atv_pim`,
  `atv_pim_uso`, `atv_pmc`, `atv_pms`; TWA labour `mt_pnad`, `mt_desocupacao_retro`, `mt_caged`,
  `mt_caged_setor`.
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
  real yield plus the target.
- **Read:** [[natural_rate_of_interest]], [[taylor_rule]], [[real_time_data]],
  [[jurisdictional_uncertainty]], [[term_premium]]; `directed_credit`.
- **Mental models:** Verde §1.1 (the structural Selic level is conditional on the fiscal anchor),
  §2.2 (a real rate too high does not last: inflation or the nominal rate adjusts).
- **Data:** `br_interest_rate`, `br_di_grade`, `inflc_meta`; TWA `expc_focus_periodo` (Selic),
  `expc_focus`, `cmb_real_rates` (peers), `atv_renda_poupanca`, `fisc_divida`.
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
- **Data:** TWA fiscal `fisc_nfsp`, `fisc_divida`, `fisc_dlsp_fatores`, `fisc_rtn`, `fisc_efgg`;
  exogenous `cmb_risco_pais`; TWA `atv_pib_mensal` (denominator).
- **Trap.** Fiscal dominance is a spectrum, not a switch. Blanchard's estimate is for 2002, with
  dollar-linked debt; in Segura-Ubiergo's panel gross debt is not a robust determinant of real rates
  while the fiscal balance is. Fiscal data are TWA: the report states its premises.

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
  `cmb_comex_fator_agregado`, `cmb_comex_pais`, `cmb_comex_produto`, `diferenciais_juros`; TWA
  `expc_focus_periodo` (câmbio); `pm_copom_projecoes`.
- **Trap.** This agent draws no conclusion about the exchange rate (I.III.x): persistence, global
  against idiosyncratic and the risk premium come from the FX agent (Part 3). The pass-through
  literature belongs to the inflation agent (IV.i). And the sign of the rate → exchange rate link is
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
- **Data:** TWA external `us_interest_rate`, `inter_interest_rate`, `cmb_real_rates`,
  `cmb_dollar_index`, `cmb_dollar_index_em`, `comm_brent`, `comm_icbr`; FX endogenous
  `diferenciais_juros`.
- **Trap.** Global data are TWA until an external agent exists; the Fed path is a stated premise, not
  a conclusion of this agent.

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
  `pm_copom_calendario`; TWA `expc_focus_copom`, `expc_focus_periodo` (Selic), `expc_qpc`.
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

The F(A) of this agent does not exist yet. When it is built (`analytics/agent_system/dados`, one
file declaring the tables of V.II), the agent reads every table of the list through
`obsidian/ciclos/<date>/dados/F_politica_monetaria.md`, fixed for the cycle. The special F for the DI
curve (the Selic priced meeting by meeting), the Focus, the calendar and the Copom's decisions and
projections already exists (`especiais.py`) and serves the FX agent today.

---

## Part 3 — Outputs: what this agent tells the others matters to it

### 3.1 To FX (fixed layer; approved by the user 2026-10-21)

What this agent needs from the FX agent, every cycle. These are the FX map's rows E1–E7, unchanged in
substance, written from this side. What the Copom cares about in the exchange rate is its effect on
inflation and expectations, not its level for its own sake (2.7).

| # | FX map | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|---|
| S1 | E1 | **Is the move persistent or transitory?** A judgement, with the reason, separating a level shift from noise | Pass-through depends on persistence; a transitory spike is looked through | A move the FX agent classifies as persistent, in either direction | 2.2, 2.7 |
| S2 | E2 | **Global or idiosyncratic?** The split of the FX agent's Q3 | An idiosyncratic depreciation usually comes with a higher risk premium, which also reaches expectations; a global one does not carry that signal | The idiosyncratic component dominates the month's move | 2.3, 2.6, 2.7 |
| S3 | E3 | **Pass-through channel.** Which prices a depreciation reaches, and how fast | The Copom projects free and administered prices separately, and their pass-through differs | Always, as context for S1 | 2.2 |
| S4 | E4 | **Where the BRL is relative to the Copom's conditioning assumption** (a recent rate, then PPP) | A gap between the market and that path is a risk to the projection | The gap widens in the direction the Copom lists as a risk | 2.1, 2.2 |
| S5 | E5 | **Risk premium reading.** Is the BRL pricing fiscal or institutional stress? | The same stress raises the neutral and weakens transmission (ata of the 281st meeting, §8) | CDS and BRL move together against peers | 2.5, 2.6 |
| S6 | E6 | **How much carry is supporting the BRL** | The exchange rate is one channel from the Selic to inflation; if carry stops working, that channel weakens | Carry and the BRL decouple | 2.10, 2.7 |
| S7 | E7 | **FX market functioning.** Liquidity, cupom cambial, central-bank intervention; whether there is dysfunction | Tells whether the BCB is using FX instruments rather than the rate, and whether an intervention answers dysfunction or defends the level (trigger of E4) | Intervention, a liquidity squeeze or a cupom cambial spike | 2.1, 2.7 |

**Decided by the user, 2026-10-21.**
- **S3 (E3) is provisional.** The pass-through literature belongs to the inflation agent (IV.i).
  Until it exists the FX agent answers this row; when it does, the row moves to inflation → this
  agent, and the FX agent tells the inflation agent about depreciation risk (I.III.xvii).
- **S7 (E7) keeps the cupom cambial.** The series is not in the data yet; it comes with the Bloomberg
  API (expected 2026-11-01). Until then the row is answered with reserves, interventions and the FX
  flow.

### 3.2 To other areas — not defined yet

Written when those agents exist. The ones that matter most to this area:
- **Inflation** — the drivers of the projection, persistence, services and administered prices (2.2).
  Pass-through is already decided to be the inflation agent's (IV.i); until it exists, inflation is TWA
  and S3 stays with FX.
- **Fiscal** — fiscal impulse, debt dynamics and the risk premium (2.5, 2.6). Blanchard (2004) stays
  with this agent because it asks about the efficacy of monetary policy under fiscal dominance
  (I.III.xvii); the fiscal agent will own the fiscal side of [[fiscal_dominance]].
- **External** — the Fed path and the global cycle (2.8).
- **Expectations**, if an agent is created (I.III.xii); **activity**, **labour market** and **credit**
  (2.4, 2.10).

---

## Part 4 — Inputs: what the others told this agent matters to them

### 4.1 From FX (fixed layer; approved by the user 2026-10-21)

What the FX agent needs from this agent, every cycle: the FX map's rows S1–S4, written from this side.

| # | FX map | What the FX agent needs | Why it matters to FX | How this agent answers |
|---|---|---|---|---|
| E1 | S1 | **Expected path of the Selic and the balance of risks**, as this agent reads it (not only the Focus median) | The forward carry, which supports the BRL, is the differential ahead, not today's | The thesis of Q5 in the horizon format of Part 1 (quarter close; meeting by meeting for the next two quarters) |
| E2 | S2 | **Credibility reading: is a hike read as credibility or as validating inflation?** | Decides the sign of the rate → FX link | Q3, channels 2.3 and 2.6 |
| E3 | S3 | **How the Copom described the exchange rate at the last meeting**, filtered from the comunicado, ata and RPM | Tells whether the FX move is already inside the Copom's scenario or is news to it | The Copom documents of layer 1 (II.III.ix); channel 2.7 |
| E4 | S4 | **Reaction function to a depreciation.** Would the Copom respond with the Selic, and by how much? **Trigger:** if the BCB's posture turns to defending the exchange rate (intervention without signs of dysfunction, or communication about the level of the BRL), the question widens to the BCB's whole reaction function, intervention included, answered by both agents with this agent leading | A credible response caps the depreciation; its absence removes the cap. Under a defense posture what matters is the BCB's reaction function, not the technical state of the market | Q1, channels 2.1 and 2.2 (the second-order-effects test); under the trigger, 2.1 and 2.7 with the FX agent's reading of dysfunction (S7) |

**Decided by the user, 2026-10-21.**
- **E4 (S4) is triggered.** While the BCB intervenes only against dysfunction, intervention is the FX
  agent's channel (FX map 2.7, `cmb_reservas_bc`), and judging dysfunction is its job (S7); this agent
  answers on the rate. If the BCB's posture turns to defending the exchange rate, the reaction
  function, intervention included, becomes a question for both, led by this agent.
- **E1 (S1) follows the approved horizon.** The FX equation of the Structural Model was estimated with
  the Selic at the quarter close and the simulator uses the average; the close is what this agent
  gives (Part 1, horizon, item 3).

### 4.2 From other areas — not defined yet

Inflation, fiscal policy, economic activity, credit, labour market, expectations and external. Each
is written when that agent's map is built, by that agent.

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
- [[calvo_pricing]] — random price reset; the pricing block of the NK model. *Other owner (inflation):* [[monetary_policy/synthesis/staggered_prices (Calvo, 1983)]]
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
- No synthesis yet: [[monetary_policy/clean_md/samba_dsge_brazil (de Castro et al., 2011)]], [[monetary_policy/clean_md/samba_dsge_brazil_update (Fasolo et al., 2023)]], [[monetary_policy/clean_md/monetary_channels_brazil_semi_structural (Minella & Souza-Sobrinho, 2013)]], [[monetary_policy/clean_md/directed_credit_monetary_transmission (Bonomo & Martins, 2016)]]; *other owner (FX):* [[monetary_policy/clean_md/monetary_policy_fx_puzzle_em (Kohlscheen, 2014)]].

### #neutral_rate — the neutral and the stance

- [[natural_rate_of_interest]] — a low-frequency r* tied to trend growth, estimated jointly with potential; global co-movement. [[monetary_policy/synthesis/natural_rate_measurement (Laubach & Williams, 2003)]], [[monetary_policy/synthesis/natural_rate_international (Holston, Laubach & Williams, 2017)]]
- [[natural_rate_of_interest]], [[real_time_data]] — Brazil's neutral falling with debt, risk and deepening; activist rules self-correct mismeasurement. [[monetary_policy/synthesis/neutral_rate_time_varying_brazil (Perrelli & Roache, 2014)]]
- [[natural_rate_of_interest]], [[fiscal_dominance]] — saving, public saving and a residual country premium in Brazil's high rates. [[monetary_policy/synthesis/high_interest_rates_puzzle_brazil (Segura-Ubiergo, 2012)]]
- No synthesis yet: [[monetary_policy/clean_md/neutral_rate_brazil (Muinhos & Nakane, 2006)]].

### #reaction_function_and_gradualism — how the rule is estimated and why it is inertial

- [[taylor_principle]], [[interest_rate_smoothing]] — pre-Volcker accommodation against a two-for-one response after; partial adjustment. [[monetary_policy/synthesis/monetary_policy_rules_stability (Clarida, Gali & Gertler, 2000)]]
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
- `inflation_expectations_anchoring` — no page. [[monetary_policy/synthesis/central_bank_communication_survey (Blinder et al., 2008)]]

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
- [[global_financial_cycle]] — US policy driving the global factor; floaters exposed. *Other owner (external):* [[monetary_policy/synthesis/us_monetary_policy_global_cycle (Miranda-Agrippino & Rey, 2020)]]
- [[risk_premium]], [[uip]] — international risk spillovers; free floats better insulated. *Other owner (FX):* [[monetary_policy/synthesis/us_policy_international_risk_spillovers (Kalemli-Ozcan, 2019)]]; `fear_of_floating` — no page.
- [[carry_trade]] — policy transmission to the exchange rate depends on carry positioning. *Other owner (FX):* [[monetary_policy/synthesis/monetary_policy_exchange_rates (BIS, 2026)]]
- No synthesis yet: [[monetary_policy/clean_md/two_targets_two_instruments (Ostry, Ghosh & Chamon, 2012)]]; *other owner (FX):* [[monetary_policy/clean_md/systematic_monetary_policy_forward_premium_puzzle (Tambakis & Tarashev, 2012)]].

### #institutional_framework and #brazil_policy_communication

- [[inflation_targeting]] — the legal frame: no synthesis yet for [[monetary_policy/clean_md/decreto_3088_metas_inflacao (Brazil, 1999)]], [[monetary_policy/clean_md/lc_179_autonomia_bcb (Brazil, 2021)]], [[monetary_policy/clean_md/decreto_12079_meta_continua (Brazil, 2024)]].
- The Copom's comunicados, atas and RPMs, in `clean_md/central_bank/`, outside the vault agent; their
  synthesis is an open design question (II.III.ix).
