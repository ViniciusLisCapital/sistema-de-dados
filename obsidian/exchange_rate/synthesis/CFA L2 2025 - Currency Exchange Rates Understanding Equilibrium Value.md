# CFA L2 2025 — Currency Exchange Rates: Understanding Equilibrium Value

**Type:** Curriculum reading (CFA Program, Level II)
**Tags:** #cfa #uip #cip #ppp #real-interest-rate-parity #mundell-fleming #portfolio-balance #currency-crisis #carry-trade
**Source:** CFA Institute, Level II curriculum, Learning Module 1 (Economics)
**Language:** English
**Raw file:** [[exchange_rate_understanding_equilibrium (CFA L2, 2025)]]

---

## Context and motivation

The Level II synthesis of the vault's core theoretical apparatus (UIP, CIP, PPP, Dornbusch overshooting) into one integrated practitioner framework, plus three genuinely new pieces not otherwise in the vault: the Mundell-Fleming capital-mobility-conditioned policy-mix table, the portfolio balance approach to sustained fiscal deficits, and a compiled empirical currency-crisis-indicator checklist (with the 2008 Iceland case study). Opens by quoting Greenspan on the humility exchange-rate forecasting demands — the reading's own framing is "understand long-run equilibrium, don't try to predict short-run moves."

## Core argument / thesis

No single model explains exchange rates. International parity conditions (CIP, UIP, PPP, real interest rate parity, forward rate parity) are the theoretical skeleton, but only CIP is arbitrage-enforced and reliably holds; the others require risk-neutral speculation or long horizons to show up empirically. Layered on top: balance-of-payments/portfolio-balance channels (driven by debt stocks and current-account trends) and monetary/fiscal policy transmission (Mundell-Fleming), whose *sign* itself depends on a country's capital mobility. Currency crises are the discontinuous failure mode when these mechanisms interact with a fragile banking sector or an unsustainable peg.

## Key mechanisms / model

- **Bid-offer/triangular arbitrage mechanics**: same CIP arithmetic as [[CFA L1 2025 - Exchange Rate Calculations]], extended to two-sided (bid/offer) quotes and dealer-tier microstructure (interbank vs. client spreads, spread determinants: pair liquidity, time-of-day session overlap, volatility, size, client relationship).
- **CIP → UIP → forward rate parity chain**: CIP (arbitrage-enforced) + UIP (risk-neutral-speculation-enforced, not arbitrage) together imply `F = S^e` — forward rate parity. Since UIP is not arbitrage-enforced, forward rate parity inherits UIP's empirical fragility. Directly the same logic as [[uip]]'s CIP/UIP variants table, with the missing "why does UIP even hold at all if not by arbitrage" mechanism made explicit: risk-neutral speculators betting on the gap between F and their expected S.
- **Real interest rate parity / international Fisher effect**: combining ex ante PPP (`%ΔS^e = π_f^e − π_d^e`) with UIP (`%ΔS^e = i_f − i_d`) gives `i_f − i_d = π_f^e − π_d^e` (international Fisher effect) ⟹ real rates equalize across countries (`r_f = r_d`) — the same real interest parity result as [[Krugman 2023 - Price Levels and the Exchange Rate in the Long Run]], reached via a different combination of primitives (ex ante PPP + UIP here, vs. real-exchange-rate demand/supply there). Both flag that unequal currency risk (EM risk premium) breaks the equality — same [[risk_premium]] wedge.
- **PPP empirical evidence — horizon-dependence, formally shown**: Exhibit 2 plots inflation differential vs. exchange rate change across 1/5/10/15-year windows (1990–2020) — no relationship at 1 year, a clear positive (PPP-consistent) relationship by 5+ years. Exhibit 3 is the single most Brazil-relevant data point in this reading: the BRL/USD rate 1977–1993 tracked Brazil's hyperinflationary inflation differential almost exactly even at a 1-year horizon — PPP holds fast whenever the inflation gap is *large*, and only slowly when it's small. This reconciles the "PPP fails" (Krugman Ch. 16) and "PPP works over long horizons" findings: it's not that PPP is horizon-dependent in the abstract, it's that PPP's *signal-to-noise ratio* rises with the size of the inflation gap.
- **Mundell-Fleming policy-mix**: see [[mundell_fleming_policy_mix]] for the full high/low-capital-mobility tables. Real-world case: Germany 1990–92 (expansionary fiscal for reunification + Bundesbank tightening) → DM appreciation, the textbook "expansionary fiscal + restrictive monetary" cell.
- **Monetary models of exchange rate determination**: distinguishes the "pure" monetary approach (assumes PPP holds always, so Ms → P proportionally → E proportionally) from Dornbusch's modified version (short-run sticky prices → overshooting) — explicitly cites Dornbusch (1976) by name as the source of the overshooting mechanism, consistent with [[overshooting]] and [[Dornbusch 1976 - Expectations and Exchange Rate Dynamics]].
- **Balance-of-payments and portfolio-balance approaches**: see [[balance_of_payments_approach]].
- **Carry trade reinforcement — Turkish lira 2002–2010**: sustained ~1,000bp TRY-USD spread; Turkish authorities intervened to prevent lira appreciation (capping the *spot* leg of carry returns), yet the carry trade was still highly profitable over the period purely from the accumulated yield differential — a clean empirical illustration that carry can pay off through the *yield* channel alone even when the *currency* leg is suppressed by policy, complementing [[carry_trade]]'s AUD/JPY and BRL framings.
- **Currency crisis indicators + Iceland (2008) case study**: see [[currency_crisis_indicators]].

## Main results / findings

- Only CIP is unconditionally reliable (arbitrage-enforced); UIP/ex ante PPP/forward rate parity hold better over long horizons than short — a "patience premium" runs through nearly every parity condition in this reading.
- The Brazil 1977–1993 hyperinflation episode is presented as the clearest possible confirmation of relative PPP precisely because the inflation differential was so large it swamped all the confounding noise that usually obscures PPP at short horizons.

## Limitations and caveats

- The Mundell-Fleming policy-mix tables (Exhibits 4–6) are stylized qualitative predictions from a simplified aggregate-demand model with no price adjustment — treat as a rule-of-thumb heuristic, not a calibrated forecasting tool; the reading itself flags multiple "indeterminate" cells.
- The nine currency-crisis indicators are compiled from "one or more studies" without attribution to a single canonical source in this excerpt — useful as a checklist, not as a tested predictive model with known false-positive rates.

## Connections

- [[uip]] / [[CFA L1 2025 - Exchange Rate Calculations]] — same CIP/UIP/forward-rate-parity chain, now with the risk-neutral-speculation mechanism for why UIP holds at all (absent arbitrage)
- [[ppp_balassa_samuelson]] — same PPP failure/recovery pattern as Krugman Ch. 16, now with explicit empirical exhibits (horizon-dependence; Brazil 1977–93 hyperinflation as the cleanest confirming case)
- [[Krugman 2023 - Price Levels and the Exchange Rate in the Long Run]] — same real interest rate parity result via a different derivation path (ex ante PPP + UIP here vs. real-exchange-rate demand/supply there)
- [[overshooting]] / [[Dornbusch 1976 - Expectations and Exchange Rate Dynamics]] — explicitly cites Dornbusch (1976) as the source of the sticky-price overshooting mechanism, distinguishing it from the "pure" monetary approach
- [[mundell_fleming_policy_mix]] — new concept page built from this source's capital-mobility-conditioned policy tables
- [[balance_of_payments_approach]] — new concept page combining this source's BOP/debt-sustainability and portfolio-balance channels
- [[currency_crisis_indicators]] — new concept page: the nine-indicator checklist and the Iceland 2008 case study
- [[carry_trade]] — Turkish lira 2002–2010 case: carry profits sustained through the yield channel even when FX intervention caps the spot-appreciation channel
- [[currency_regimes]] — reinforces "fixed/quasi-fixed regimes are more crisis-prone" with the Iceland case alongside that concept's existing 1992 UK/ERM case
