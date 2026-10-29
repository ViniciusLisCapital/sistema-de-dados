# Forward Premium Puzzle (Forward Discount Bias)

**Type:** Empirical anomaly
**Tags:** #forward-discount-bias #uip #risk-premium #peso-problem #market-efficiency

---

## Definition

The failure of the interest differential — or, equivalently by covered interest arbitrage, the forward discount — to be an unbiased predictor of the subsequent change in the exchange rate. Regressing realized depreciation on the differential should give a slope of one under risk neutrality and rational expectations (uncovered interest parity with unbiased expectations). Estimates are reliably below one and frequently negative: currencies with high interest rates tend, over the following months, to appreciate rather than depreciate by the differential.

## Mechanism — the candidate explanations

The bias is a joint rejection of risk neutrality and rational expectations, so explanations relax one of the two:

- **Time-varying risk premium (rational expectations kept).** The differential equals expected depreciation plus a premium. A slope below one means the premium on the high-rate currency rises with the differential; a negative slope means it rises by more than the differential, which requires the premium to be more variable than expected depreciation and negatively correlated with it (Fama 1984, as reported by Froot & Thaler).
- **Expectational errors (constant premium).** Forecasts are systematically wrong ex post: *learning* about a regime shift, or *peso problems* — a rare event (a devaluation, a collapse) that is priced but absent from the sample, so the slope is mis-estimated in samples where it does not occur.
- **Market inefficiency.** Some investors adjust to interest-rate changes with a lag, so part of the appreciation caused by a higher real differential happens after the differential rises — a negative short-run slope with the long-run relation intact (Froot & Thaler's proposal).

## When it applies / when it fails

- It holds across subsamples, currencies, forecast horizons and asset markets in the literature Froot & Thaler survey, which is what undermines sample-specific explanations (peso problems, learning).
- It weakens or disappears where differentials are large and driven by inflation: in the build-up to hyperinflations the slope is positive and nearer one, and across countries high-interest, high-inflation currencies depreciate secularly. The level of the differential points the right way for long-run changes even when short-run correlations point the wrong way.
- Risk-premium explanations have found no direct support: expected-variance measures, CAPM-based portfolio models and survey-based decompositions do not link the premium to the forward discount (Froot & Thaler).
- Trading on it is possible in principle (buy the high-interest currency) but, for a single currency, the expected profit is small relative to its volatility.

## How it appears across sources

| Source | Role |
|---|---|
| [[exchange_rate/synthesis/fx_anomalies_survey (Froot & Thaler, 1990)]] | Survey of the evidence: none of some 75 published slope estimates reaches one; risk-premium tests and survey expectations attribute the bias to expectational errors, not risk; peso problems nearly rejected for the 1980–85 dollar; a slow-responding-investor explanation proposed |
| [[external/synthesis/us_mp_spillovers_bond_markets (Albagli et al., 2018)]] | Argues its spillover results need only that fixed-income flows follow yield differentials, not that UIP holds; a policy surprise beyond fundamentals can depreciate the dollar on impact while a low-rate environment raises foreign-currency risk premia (citing Lustig, Roussanov & Verdelhan and Karnaukh) |

## BRL / application to the current analysis

The source linked here says nothing about Brazil; its evidence is on advanced-economy currencies against the dollar.

## Connections

- [[uip]] — the puzzle is the empirical failure of UIP with unbiased expectations
- [[risk_premium]] — the leading rational explanation, which the survey evidence does not support
- [[carry_trade]] — the strategy that profits from the bias
- [[exchange_rate/synthesis/fx_anomalies_survey (Froot & Thaler, 1990)]] — the anomaly, the tests of its explanations and the case for inefficiency
- [[external/synthesis/us_mp_spillovers_bond_markets (Albagli et al., 2018)]] — why US policy-surprise days may fit interest arbitrage better than other days, and why the spillover mechanism does not hinge on UIP
