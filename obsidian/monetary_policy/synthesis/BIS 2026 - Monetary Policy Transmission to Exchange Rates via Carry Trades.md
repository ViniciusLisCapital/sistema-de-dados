# BIS 2026 — Monetary Policy Transmission to Exchange Rates: The Role of Currency Carry Trades

**Type:** Central bank research bulletin
**Tags:** #carry-trade #monetary-policy #uip #cftc-positioning #deleveraging #chf #jpy
**Source:** BIS Bulletin No 124, 6 May 2026
**Language:** English
**Raw file:** [[monetary_policy_exchange_rates (BIS, 2026)]]

---

## Context and motivation

Addresses a puzzle practitioners see constantly: the same-size monetary policy surprise sometimes moves a currency sharply and sometimes barely at all. Uses four comparable SNB policy announcements (June 2010, March 2015, March 2020, June 2022) — chosen specifically because their impact on domestic interest rates was similar — to show the exchange rate response varied enormously (sharp CHF appreciation in June 2010/2022, almost no move in March 2015/2020). The Bulletin's contribution is identifying *why*: prior carry-trade positioning in the currency.

## Core argument / thesis

Monetary policy transmission to the exchange rate is **state-dependent** on how much the currency is being used to fund carry trades at the time. When speculators are heavily net short a currency (funding carry trades by borrowing it cheaply to invest elsewhere), a tightening shock forces deleveraging — unwinding those short positions — which mechanically drives sharp appreciation on top of whatever the "fundamental" UIP-based response would be. When the currency isn't being used as a funding currency, the same-size policy shock produces a muted response, because there's no leveraged position to unwind.

## Key mechanisms / model

- **Carry trade activity measure**: net positioning of *non-commercial* traders (no underlying hedging need — a proxy for speculators) in CME currency futures. Validated against a price-based measure: speculative positions turn more net-short exactly when the carry-to-risk ratio (interest rate differential ÷ option-implied volatility) rises — i.e., positioning tracks the incentive to carry-trade, as expected.
- **Historical carry-unwind episodes identified this way**: 2006–07 (unwound in the August 2007 "Quant Meltdown"), July 2010 (euro sovereign debt crisis), August 2024 (FX market turbulence) — CHF and JPY are the two canonical funding currencies throughout.
- **Local projections methodology**: cumulative exchange rate change from t−1 to t+h regressed on the monetary policy shock (first principal component of interest rate futures changes in a tight announcement window), interacted with dummies for whether carry trade activity was High or Low (split at the historical median — conservative, since funding-currency futures positioning is negative even at the median) going into the announcement, controlling for past FX changes and the VIX.
- **Central quantitative result**: during high-carry-activity periods, a 25bp monetary policy surprise produces a ~4% CHF move and an almost 10% JPY move; during low-activity periods, the same-size shock produces a statistically insignificant FX response. This is a roughly **an order of magnitude difference in exchange rate sensitivity to the identical policy surprise**, explained entirely by prior positioning.
- **Asymmetry — tightening, not easing, is what triggers the amplification**: significant appreciation follows *tightening* shocks specifically; depreciation following easing shocks is not statistically significant. This matches the deleveraging story directionally (short positions are vulnerable to unwind on a tightening surprise; there's no equivalent forced mechanism on an easing surprise) — it is not simply the mirror-image UIP response in both directions.
- **Direct confirmation via positioning data**: re-running the same local projections with net speculative futures positions (rather than the exchange rate) as the outcome variable confirms significant short-covering following tightening shocks *only* during high-carry periods — CHF net short positions shrink by over 60% of total open interest following a contractionary shock. The JPY result is directionally the same but only marginally significant, attributed to having fewer tightening events in the BOJ sample.

## Main results / findings

- The four-SNB-announcement example (Graph 1) is itself close to a controlled experiment: comparable-size rate surprises, wildly different FX outcomes, tracking almost exactly with pre-announcement CFTC-style net short positioning in CHF futures — carry positioning, not the policy surprise itself, is the marginal explanatory variable.
- The paper explicitly frames this as a **non-bank financial intermediation** channel adding uncertainty to monetary policy transmission — central banks need to account for the "heft of leveraged traders" when forecasting how their own policy moves will show up in the exchange rate.

## Limitations and caveats

- The measure (CME non-commercial futures positioning) is explicitly flagged by the authors as "reliable, if incomplete" — most carry trade activity happens OTC in spot/forwards, not in exchange-traded futures, so this is a proxy, not a direct measure of total carry positioning.
- Findings are specific to CHF and JPY, the two canonical low-rate funding currencies — the paper does not claim this generalizes to every currency's monetary policy transmission, only to those that structurally serve as carry-funding vehicles at a given point in time (a role that itself can shift, e.g., which currency is "the" funding currency changes across cycles).
- The JPY tightening-deleveraging result is only marginally significant due to a small number of BOJ tightening events in-sample — treat the JPY-specific magnitude with more caution than the CHF result.

## Connections

- [[carry_trade]] — direct, substantial extension: this paper shows *when* carry-trade crash risk is triggered by monetary policy specifically (tightening shocks in the funding currency), and quantifies the amplification (~4-10x normal FX sensitivity) versus low-carry-activity periods — refines this concept's existing "when carry fails" framework with a monetary-policy-specific trigger and a positioning-based early-warning measure (CFTC-style net shorts, carry-to-risk ratio)
- [[uip]] — shows *why* the simple "tightening → appreciation" UIP intuition is unreliable in magnitude, not just in sign: the same policy surprise produces wildly different FX responses depending on prior speculative positioning, a state-dependence UIP alone doesn't capture
- [[overshooting]] — the deleveraging-driven appreciation is a distinct, positioning-based overshooting mechanism, additive to (not a substitute for) the sticky-price/Dornbusch overshooting channel already documented
- [[risk_premium]] — carry-to-risk ratio (interest differential ÷ implied vol) is functionally a risk-adjusted carry measure, complementary to this vault's existing risk-premium framework for when carry positioning becomes crowded and fragile
