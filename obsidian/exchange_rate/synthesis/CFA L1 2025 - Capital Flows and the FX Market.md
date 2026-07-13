# CFA L1 2025 — Capital Flows and the FX Market

**Type:** Curriculum reading (CFA Program, Level I)
**Tags:** #cfa #real-exchange-rate #fx-market-microstructure #impossible-trinity #currency-regimes #capital-flows
**Source:** CFA Institute, Level I curriculum, Learning Module 7 (Economics)
**Language:** English
**Raw file:** [[capital_flow_fx_market (CFA L1, 2025)]]

---

## Context and motivation

A practitioner-oriented survey of the FX market's institutional plumbing (participants, market composition) plus a policy-level treatment of currency regimes and the Impossible Trinity — filling a gap the rest of the vault's theory-heavy sources (Krugman, Dornbusch) don't cover in this much taxonomic/historical detail: who actually trades FX and why, and the full spectrum of regime choices between hard peg and free float.

## Core argument / thesis

Nominal exchange rates are one input; the real exchange rate (nominal rate adjusted for relative price levels) is what determines actual cross-border purchasing power and competitiveness — but even real exchange rates are, at best, a weak, noisy predictor of nominal FX moves, because capital flows (not trade flows) dominate short-to-medium-run exchange rate determination. Separately, every currency regime a country picks is a specific point on the Impossible Trinity spectrum, trading off exchange-rate stability, capital openness, and monetary independence.

## Key mechanisms / model

- **Real exchange rate formalization**: `R_(d/f) = S_(d/f) × (P_f/P_d)` — increasing in the nominal rate and the foreign price level, decreasing in the domestic price level. Approximation: `%ΔR ≈ %ΔS + %ΔP_f − %ΔP_d`. Worked example: India 2018 — INR/USD rose 6.7% (rupee nominal depreciation) but Indian inflation (4.7%) exceeded US inflation (2.5%) by more than that, so the *real* depreciation (≈4.5%) was smaller than the nominal one — India's competitiveness gain from nominal depreciation was partly eaten by relatively higher domestic inflation. Directly the same real-exchange-rate definition as [[ppp_balassa_samuelson]] and [[Krugman 2023 - Output and the Exchange Rate in the Short Run]], with a cleaner worked numerical example.
- **FX market participant taxonomy**: buy side (corporates, "real money" accounts [pension/insurance/mutual funds, low-leverage], leveraged accounts [hedge funds, CTAs, prop desks, HFT], retail, governments, central banks, sovereign wealth funds) vs. sell side (tier-1 global dealing banks vs. tier-2/3 regional banks who outsource liquidity access). Central banks and SWFs are flagged as holding ~USD 13 trillion in FX reserves (2021), ~60% in USD, ~20%+ in EUR — background context for why reserve-currency status matters at all (ties to [[Krugman 2023 - Fixed Exchange Rates and Foreign Exchange Intervention]]'s reserve-currency asymmetry).
- **Impossible Trinity**: formal statement and derivation — see [[currency_regimes]] for the full concept.
- **IMF currency regime taxonomy** (8 categories, dollarization → independent float): see [[currency_regimes]].
- **Historical currency-regime narrative**: classical gold standard (price-specie-flow mechanism) → Bretton Woods (1944–73) → post-1973 float (with the empirical surprise that exchange rates proved far more volatile than trade-flow-based models predicted — this volatility being read, in hindsight, as evidence of the asset-market/investment-flow logic later formalized as [[uip]] and [[overshooting]]) → European "snake"/ERM (1979) → 1992 UK/ERM crisis (self-fulfilling speculative attack, sterling forced out after only two years) → euro (1999).

## Main results / findings

- Real exchange rate movements are a weak predictor of future *nominal* FX moves — PPP-style reasoning "can deviate... for years at a time," reinforcing the same PPP-empirical-failure conclusion Krugman's Ch. 16 documents, from the practitioner (not academic) side.
- The 1992 ERM crisis is presented as a canonical real-world instance of the balance-of-payments-crisis mechanics in [[Krugman 2023 - Fixed Exchange Rates and Foreign Exchange Intervention]]: UK low rates (recession) vs. German high rates (reunification-driven Bundesbank tightening) pulled capital toward DM; BoE ran out of reserves defending sterling and was forced out of the ERM.
- Crawling pegs (passive and active variants) are explicitly tied to 1980s Latin American high-inflation experience, including Brazil — a direct historical precedent for BCB's later floating-with-intervention regime.

## Limitations and caveats

- The IMF regime taxonomy (Exhibit 6) is dated to April 2008 — treat country classifications as illustrative of regime *types*, not current status (many listed countries have since changed regime, e.g., Brazil is currently an independent floater, not shown historically as a crawling-peg country in the table itself though discussed in the crawling-peg narrative).
- No formal econometric evidence is presented for the real-exchange-rate/nominal-rate disconnect claim — it's asserted by reference to PPP's known empirical failure (documented with more rigor in [[Krugman 2023 - Price Levels and the Exchange Rate in the Long Run]]) rather than demonstrated in this reading.

## Connections

- [[currency_regimes]] — this reading is the primary source for the Impossible Trinity framework and the full IMF regime taxonomy (both created as a new concept page from this source)
- [[ppp_balassa_samuelson]] — identical real exchange rate definition and the same PPP-poor-predictor conclusion, with a cleaner worked numerical (India 2018) example
- [[Krugman 2023 - Fixed Exchange Rates and Foreign Exchange Intervention]] — the 1992 ERM/sterling crisis is a real-world instance of that chapter's balance-of-payments-crisis and capital-flight mechanics; reserve-currency asymmetry background for why FX reserves concentrate in USD/EUR
- [[uip]] / [[overshooting]] — the post-1973 "exchange rates move more than trade flows can explain" surprise is the empirical motivation for the asset-approach framework both those concepts formalize
- [[CFA L1 2025 - Exchange Rate Calculations]] — companion reading in the same learning module; that one covers the trading mechanics (cross-rates, forward points) that operate within whatever regime a currency sits in
