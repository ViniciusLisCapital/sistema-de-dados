---
aliases: ["Froot 1990 - Anomalies: Foreign Exchange"]
---

# Anomalies: Foreign Exchange — Froot & Thaler 1990

**Type:** paper (survey column, "Anomalies")
**Tags:** #forward-discount-bias #uip #risk-premium #peso-problem #market-efficiency #expectations #survey
**Source:** Journal of Economic Perspectives, Volume 4, Number 3, Summer 1990, Pages 179–192
**Language:** English
**Source file:** [[exchange_rate/clean_md/fx_anomalies_survey (Froot & Thaler, 1990)]]

---

## Context and motivation

The column catalogs results that are hard to rationalize within the rational-agent, market-clearing paradigm. Its anomaly here is in the market that should be the most efficient of all — foreign exchange, whose daily turnover (about $430 billion in mid-1989) dwarfs daily US GNP and world trade. Behind it lies the old debate between Friedman (speculation is stabilizing, pushing rates toward fundamentals) and Nurkse (speculation can be destabilizing and costly), sharpened by the temporary 65 percent appreciation of the dollar in the mid-1980s. The question matters more for currencies than for other assets because the exchange rate moves the prices of all foreign assets, goods and factors at once, so if speculation drives it away from fundamentals the case for intervention is strongest here. The authors narrow efficiency to a single test, the forward discount bias, chosen because it rejects the null so strongly that statistical power is not an issue.

## Core argument / thesis

Under risk neutrality and rational expectations, the interest differential (equivalently, the forward discount, by covered arbitrage) should be an unbiased forecast of the subsequent change in the exchange rate. It is not: high-interest currencies tend, if anything, to appreciate afterwards. The two rational explanations both fail. A time-varying risk premium would have to vary more than expected depreciation itself and with implausible size and sign; and expectational errors that are still "rational" — learning and peso problems — do not survive the breadth and persistence of the evidence. Survey data attribute the bias to expectational errors, not to risk. The authors therefore argue that explanations allowing for market inefficiency should be taken seriously, and offer one: some investors respond to interest-rate changes with a lag.

## Key mechanisms / model

- **The test.** Regress the realized percentage depreciation over k periods on the current k-period interest differential (domestic minus foreign), equation (1); unbiasedness means a slope of one (some authors also require a zero intercept). Replacing the differential by the forward discount gives the same test, since covered interest arbitrage equates the two — the "forward discount bias" is the failure of the slope to equal one.
- **Reading a slope below one as a risk premium.** If investors are risk averse and currency risk is not diversifiable, the differential equals expected depreciation plus a risk premium. A slope below one then means the risk premium on dollar assets rises with the differential; a negative slope means it rises by more than the differential. Following Fama (1984), this requires the risk premium to be more variable than both expected depreciation and the differential, and negatively correlated with expected depreciation. A negative correlation alone is plausible (higher expected US inflation may mean both more expected depreciation and riskier dollar assets); the hard part is why a change in rates should move the premium by even more.
- **Reading it as expectational errors.** With a constant premium, the bias must come from forecasts that are systematically wrong after the fact, without necessarily any exploitable inefficiency ex ante:
  - *learning* about a regime shift (Lewis: slow learning about a shift in the US money supply process explains about half the error of the forward rate in 1980–85) — but the errors should die out, and they do not;
  - *peso problems* — named after the 1955–76 Mexican peso, fixed against the dollar but always at a forward discount until the large devaluation finally came; a sample without the rare event mis-estimates the slope. Mussa's version: with a skewed distribution of inflation, samples without a hyperinflation make expected inflation (and so the interest differential) overpredict depreciation.
- **The authors' alternative: slow-responding investors.** Suppose some investors (they suggest "central banks" leaning against the wind) adjust to interest-rate changes only gradually, while others are rational but risk averse. A rise in the real interest differential then produces only part of its appreciation on impact and the rest afterwards, so the currency keeps appreciating after the differential rises — a negative short-run slope. The same story leaves the long-run relation intact. The assumption that carries it is that at least some changes in nominal differentials are changes in real differentials. Its testable implication is that past levels of the differential, added to equation (1), should enter with a positive coefficient near one; Froot (1990) is cited as supportive.

## Main results / findings

- **The bias is pervasive.** Across the published literature the slope is reliably below one and frequently below zero; of some 75 published estimates, none is equal to or greater than one (Froot, 1990). A slope of about minus one means a 1 percentage point higher US rate is followed by dollar appreciation of about 1 percent a year rather than the 1 percent depreciation unbiasedness predicts.
- **Risk-premium tests find nothing.** Statistical models of predictable excess returns find patterns but no evidence they are risk; measures of expected variance (ARCH, Domowitz and Hakkio) are uncorrelated with the bias; CAPM-based portfolio models (Frankel and later work) cannot reject a zero exchange risk premium. Survey expectations of FX traders (Froot and Frankel 1989) imply risk premia that are non-zero and move over time, but are uncorrelated with the forward discount: the risk component of the bias is small and insignificant, and the bias is attributed to expectational errors.
- **The 1980s dollar as a sensibility check.** From late 1980 to early 1985 the dollar stood at a forward discount yet appreciated at about 13 percent a year. A risk-premium reading requires investors to have given up around 16 percent a year to hold the "safer" foreign currencies — the opposite of the safe-haven story told at the time — and then, during the depreciation, about 6 percent a year to hold dollars. Premia this large and this unstable are hard to believe.
- **Peso problem nearly rejected for the dollar.** Assuming the market expected either continued 13 percent appreciation or a collapse back to the 1980 level, an expected depreciation equal to the interest differential implies a yearly collapse probability of 35 percent and a probability of five years without collapse of .12 — unlikely but not rejected at standard levels. Using survey expected depreciation instead of the differential, it falls to .03.
- **Where the bias weakens.** In the run-up to hyperinflations the slope is positive and nearer one, and across countries high-interest (high-inflation) currencies such as Italy's have depreciated secularly: the average level of differentials points the right way for long-run changes even when short-run correlations point the wrong way.
- **Can it be traded?** Bilson's rule (buy the high-interest currency), filter rules and technical rules show profits, not always significant. But for a single currency the risk-return trade-off is poor: with an annualized regression standard error of about 36 percent, $1 of expected monthly profit comes with a $15 standard deviation, before transaction costs; diversified versions may be costly or hard to execute.

## Limitations and caveats

- **Policy conclusions are deliberately thin.** Because the evidence for inefficiency is ambiguous and there is no good general equilibrium model of exchange rates, the authors say little about whether fluctuations are costly enough to justify intervention; transaction taxes and pegs carry welfare costs of their own.
- **Expectational errors are not identified.** The survey decomposition shows the bias is not risk, but cannot say whether it is learning, peso problems or inefficiency. The slow-investor story is offered as parsimonious, not tested here beyond a citation.
- **Peso and learning arguments can be kept alive** only by arguing the many estimates are not independent (or by invoking an event like "complete nuclear annihilation" that has not yet happened); the 1980–85 subsample used for the peso calculation is not randomly drawn, so those test statistics overstate significance (footnote 9).
- **Damaged passages.** Minus signs and relational symbols were lost in extraction: equation (1) prints the differential as "(i i*)" and garbles its subscripts; "β 1" (a missing relation sign) in the risk-premium section; "1 Π" in the peso-problem calculation; and the approximate-equality sign in the profit example. Two numbers are affected in a way the note cannot resolve: the average slope across the 75 estimates is printed as 0.88 although the surrounding text describes the estimates as frequently below zero and "approximately minus one", and the profit example is printed "with β = 1" while describing the wrong-signed case; neither figure should be relied on from this file. The reference list is not in the file.

## Connections

- forward_premium_puzzle — the anomaly itself: the slope of depreciation on the interest differential below one and often negative, and the case against risk-premium explanations
- [[uip]] — the unbiasedness hypothesis being tested is UIP with risk neutrality and rational expectations; covered interest parity links the forward-discount and interest-differential versions
- [[risk_premium]] — the time-varying risk premium as the main rational explanation, and the three families of tests that fail to support it
- carry_trade — Bilson's rule (buy the high-interest currency) is the trading strategy the bias implies, with its poor single-currency risk-return trade-off
