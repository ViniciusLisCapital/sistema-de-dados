# Krugman 2023 — Exchange Rates and the Foreign Exchange Market: An Asset Approach

**Type:** Textbook chapter (International Economics, 12th ed., Ch. 14)
**Tags:** #textbook #fx-market #asset-approach #uip #cip #carry-trade #forward-rate
**Source:** Krugman, Obstfeld & Melitz, *International Economics: Theory and Policy*, 12th ed. (2023), Part Three
**Language:** English
**Raw file:** [[exchange_rate_foreign_exchange_market (Krugman, 2023)_raw]]

---

## Context and motivation

Opens Part Three's treatment of exchange rates by establishing the "asset approach": since an exchange rate is the relative price of two monies, and money is a form of wealth, exchange rate behavior should follow the same logic as other asset prices — today's value is tied to expectations of future value. This chapter is foundational groundwork for everything downstream in the textbook (monetary approach, PPP, Dornbusch overshooting): it derives the equilibrium condition (UIP) that later chapters take as given.

## Core argument / thesis

The foreign exchange market is in equilibrium only when the (uncovered) interest parity condition holds — deposits of all currencies must offer the same *expected* rate of return once measured in a common currency. Today's spot exchange rate is the variable that adjusts to enforce this condition, given interest rates and the expected future exchange rate.

## Key mechanisms / model

- **Exchange rate as relative price + international transactions**: appreciation/depreciation mechanically raises/lowers the relative price of a country's exports and imports (textbook jeans/sweater example).
- **FX market structure**: commercial banks (interbank trading dominates), corporations, nonbank financial institutions, central banks. Most transactions route through the dollar as vehicle currency (88.3% in 2019 vs. 39%→32.3% for EUR, 16.8% JPY).
- **Instrument taxonomy**: spot vs. forward rates; FX swaps (spot sale + forward repurchase); futures (exchange-traded, can be resold) vs. forward contracts (bilateral, binding) vs. options (right, not obligation).
- **Asset return logic**: savers care about expected *real* return, but nominal (currency-denominated) comparisons work as long as both sides are measured in the same currency. Risk and liquidity are set aside as secondary for the baseline model (revisited in later chapters).
- **UIP derivation**: dollar return on a euro deposit ≈ euro interest rate + expected dollar depreciation rate against the euro. Interest parity: `R$ = R€ + (E^e − E)/E`. Equilibrium diagram: vertical schedule (R$, fixed) intersects downward-sloping schedule (expected euro return, function of today's E) — today's E is the only variable that moves to clear the market.
- **Comparative statics**: a rise in R$ appreciates the dollar today (given unchanged expectations); a rise in R€ (or a rise in the expected future E) depreciates the dollar today. Newspaper intuition ("high rates → strong currency") only holds when expectations are held fixed — a caveat the chapter flags explicitly, since real-world rate changes usually come bundled with a shift in expectations.
- **Covered interest parity (CIP)**: `R$ = R€ + (F − E)/E`, using the *forward* rate F instead of the expected future spot rate. CIP is a pure arbitrage condition (no expectations involved) and historically held very tightly — until it broke down persistently after the 2007–08 crisis (Du, Tepper & Verdelhan finding: not explained by default risk; balance-sheet/collateral constraints on arbitrageurs are the leading explanation, left as an open puzzle for later chapters).
- **UIP + CIP together** imply `F = E^e` (forward rate = market's expected future spot rate) — but this equivalence only holds if UIP holds, which the chapter already flags as empirically shaky.

## Main results / findings

- Carry trade case study (AUD funded in JPY, 2000s): UIP predicts zero expected carry profit, but the trade was persistently profitable until the 2008 AUD/JPY crash (¥100→¥65 in six months). Framed as a peso-problem: small-probability large-crash distribution (90% chance of +1%, 10% chance of −40% → expected return still slightly negative) generates exactly this "steady gains, occasional crash" return profile without abandoning UIP in expectation.
- CIP held closely pre-2008 but has not since — an unresolved puzzle attributed to arbitrage capacity/balance-sheet constraints rather than credit risk.

## Limitations and caveats

- Deliberately brackets risk and liquidity motives ("risk differences do not influence demand for foreign currency assets") to isolate the pure expected-return mechanism — the textbook's own foreshadowing that this is a simplification revisited later (their Ch. 18/20).
- The comparative-statics results (rate hikes → appreciation) are conditional on expectations being held fixed, which the text itself warns is often unrealistic.
- Textbook-level treatment: no empirical UIP-failure discussion (forward premium puzzle) beyond the carry trade anecdote — that empirical case is made more rigorously elsewhere in the vault (Fama-type tests, per [[uip]]'s "See also").

## Connections

- [[uip]] — this chapter is the formal derivation of the UIP equilibrium condition and the equilibrium diagram; also documents CIP as the covered analogue and the post-2008 CIP breakdown puzzle
- [[carry_trade]] — AUD/JPY case study is a textbook-level illustration of the carry trade and its crash risk, complementary to the vault's existing risk-premium framing
- [[Dornbusch 1976 - Expectations and Exchange Rate Dynamics]] — this chapter's UIP condition is the same equation Dornbusch uses as his rational-expectations building block for overshooting
