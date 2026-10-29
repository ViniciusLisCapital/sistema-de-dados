---
aliases: ["Alves & Areosa 2005 - Targets and Inflation Dynamics"]
---

# Targets and Inflation Dynamics — Sergio A. L. Alves & Waldyr D. Areosa 2005

**Type:** paper (BCB Working Paper; theory plus estimation)
**Tags:** #nkpc #inflation-targeting #inflation-persistence #inflation-expectations #credibility #brazil
**Source:** Banco Central do Brasil, Working Paper Series n. 100, October 2005, p. 1-39
**Language:** English
**Source file:** [[inflation/clean_md/targets_inflation_dynamics (Alves & Areosa, 2005)]]

---

## Context and motivation

What does adopting an explicit inflation target do to inflation dynamics? Brazil adopted inflation targeting in mid-1999, after the float, and the earlier evidence (Minella et al., Cerisola and Gelos) was that the target anchored survey expectations and that inflation persistence fell. The standard tool for measuring persistence, the hybrid New Keynesian Phillips curve with indexation to lagged inflation, cannot tell whether the shift toward forward-looking pricing came from the target or from anything else that happened at the same time. The paper builds a Phillips curve in which the target enters directly, so its weight can be estimated, and tracks that weight through the 1999–2004 shocks.

## Core argument / thesis

In an inflation-targeting economy, firms that do not reoptimize their price have no reason to index only to past inflation: they can index to a weighted average of the official target and lagged inflation. The weight on the target then measures how much the target governs price setting. If it is positive and output gaps are stabilized, inflation converges to the target rather than to its own past; if it is zero the model collapses to the standard hybrid curve. The same weight shapes optimal policy (the welfare loss penalizes inflation's deviation from the target, not from zero) and expectations (with a high weight, exchange-rate and demand shocks barely move expected inflation). Estimated on Brazilian data, the weight is large and significant, falls when credibility is shaken and recovers after it.

## Key mechanisms / model

**Phillips curve with target indexation (Section 3.1, equations 5–7; derivation in Appendix B).** Calvo pricing: each period a fraction of firms reset prices optimally; the rest update by a rule of thumb, raising last period's price by a reference inflation rate equal to the weighted average of the current official target and last period's inflation. Inflation minus that reference rate depends on the output gap (or real marginal cost) and on expected next-period inflation minus next period's reference rate. Iterating forward, inflation equals the reference rate plus the discounted sum of expected output gaps. The key assumption is that the target is predetermined and outside the central bank's control — in Brazil it is set by the National Monetary Council at least a year ahead.

**Optimal policy (Section 3.2, equations 8–12; Appendix B).** A second-order approximation of household welfare gives the familiar quadratic loss, but in inflation's deviation from the reference rate (and so, with full weight on the target, from the target) rather than from zero — a microfoundation for the ad hoc loss functions of the literature. Minimizing it under commitment in the timeless perspective gives a targeting criterion: deviations of inflation from the reference rate are acceptable only if they are negatively proportional to the change in the output gap. With full indexation to lagged inflation (zero target weight), the best policy can do is keep inflation plus the scaled output-gap change constant over time (the Giannoni–Woodford result); with full weight on the target, that same combination must equal the official target.

**Small open economy (Section 4, equations 13–18).** Following Galí and Monacelli, firms set domestic-goods prices, and CPI inflation differs from domestic inflation by the change in the real exchange rate, scaled by a parameter inversely related to home bias. Replacing the output gap by real marginal cost, the real exchange-rate gap enters the marginal cost of domestically consumed goods, so it belongs in the consumer-price Phillips curve as well as unit labor cost.

**Expectations formation (Section 4.1, equation 19; Appendix C).** Solving the open-economy curve gives expected inflation as a function of lagged inflation, the target path, the current output gap and real exchange-rate change, and expected future gaps and exchange-rate changes. With the target weight at one, lagged inflation, the current gap and the current exchange-rate change drop out: expectations depend on the predetermined targets and on expected future conditions, which move smoothly. With the weight at zero, past inflation and current shocks drive expectations and the target is irrelevant. This is the mechanism behind the claim that a credible target shields expectations from exchange-rate shocks.

**What carries the result.** Calvo pricing with a rule-of-thumb share; a target fixed outside the central bank; and a time-invariant target weight. The authors stress that the weight is not a credibility measure: credibility should be policy- and state-dependent (a Lucas-critique concern), the lag between policy and its effects can lower the estimated weight even under full credibility, fiscal policy is absent, and policy credibility and target credibility are hard to separate.

**Estimation (Section 4.2, equation 21).** Quarterly, two-stage least squares, 1996Q1 to 2004Q4 (Table 1). Before 1999 a target series is constructed from the crawling peg — an intended nominal devaluation of 7.5 percent with a near-constant real exchange rate — and it is set to zero in 1999Q1–Q2, when there was no anchor; afterwards each quarter's target is a quarter of the annual one. Inflation is the IPCA, seasonally filtered with the Christiano–Fitzgerald band-pass filter; foreign inflation is the US export price index; the real exchange-rate gap is HP-detrended; unit labor cost is built from São Paulo data (Seade). Instruments include leads and lags of inflation, foreign inflation, the exchange rate, the target, unit labor cost and the C-Bond spread. The weight's evolution is traced by recursive estimation; a Kalman-filter time-varying version was tried and was "considerably unstable" (footnote 24).

## Main results / findings

- **The target matters for inflation.** The target weight is 0.689 and significant over 1996Q1–2004Q4 (Table 1). Short-run exchange-rate pass-through (A3) is low, 0.053 ("about 5 percent"), which the authors translate into a strong home bias in consumption — an economy "still essentially closed" (the derived parameter prints with a colon for the decimal point). The real exchange-rate gap (A5, 0.049) is significant; unit labor cost (A4) is not, though a Wald test does not reject the cross-restriction the structural curve implies (p-value = 0.25). The discount factor (A2, 0.297) comes out far below the expected value near one, which the authors attribute to correlated regressors (the target and expected inflation move together) rather than to impatience.
- **The weight tracks credibility episodes (Figure 5).** It rises from close to 0.50 in mid-1999 to approximately 0.75 at the end of 2000; nears its upper limit in mid-2001, falls to 0.75 at the end of 2001 (Argentina, the energy crisis, September 11), and collapses from almost 0.90 to 0.25 in the second half of 2002 (the pre-election confidence crisis); it recovers from 2003 to almost 0.75 at the end of 2004. It rises when expectations are close to the target.
- **Expectations behave as the model predicts.** The weight was low from 2002Q4 to 2003Q4, so expectations should have tracked exchange-rate changes and past inflation then; 12-month-ahead survey expectations adhere to the target throughout the sample except from September 2002 to July 2003 (Figure 6). This matches ad hoc regressions in Minella et al. (2003) — target coefficients around 1, low weight on past inflation, past inflation insignificant when the sample ends before mid-2002 — and the findings of Cerisola and Gelos and of Carvalho and Bugarin.
- **The restoration after 2002** followed the BCB's commitment (the open letter, the adjusted target for 2003, tightening in 2004–2005) and fiscal support (the primary surplus target); the authors say this link was "not formally tested". They also reject Blanchard's argument that tightening could raise inflation through debt dynamics, citing Bevilaqua and Loyo's finding that disinflation worked through aggregate demand.

## Limitations and caveats

- By the authors' account: the target weight is time-invariant in the model but should be state- and policy-dependent; it is not a direct credibility measure; fiscal policy is absent; and the result should be tested on other countries. The relevance of the target for expectations "followed" commitment and fiscal support but was not tested.
- What the text shows: the quarterly sample is short and spans a regime change, so the pre-1999 "target" is a construction from the crawling peg; the quarterly target is a quarter of the annual one by assumption; unit labor cost uses only São Paulo data and is insignificant; the discount factor is implausibly low; and the recursive weight is shown only in a figure, without standard errors in the text.
- Damaged passages: throughout the file the ligatures print as odd glyphs ("in‡ation", "…rms", "a¤ects", "o¢ cial") and the Greek letters are lost, including the symbol of the target weight itself (blank in Sections 3.1–4.6, in the title of Figure 5 and in the Table 1 discussion), the indexation parameter and the discount factor. As a result equations (1)–(53) survive only as fragments of Latin symbols and operators across lines, and the note describes them in words from the surrounding text. Figures 1–6 survive only as axis values and legends, Figures 7–8 (reproduced from Minella et al. 2003) only as titles; in Table 1 the R² values print with a colon for the decimal point. The reference list is not in the file.

## Connections

- [[nk_phillips_curve]] — generalizes the hybrid NKPC: non-optimizing firms index to a weighted average of the official target and lagged inflation, estimated for Brazil in an open-economy marginal-cost form
- [[inflation_persistence]] — the target weight separates indexation to the target from indexation to past inflation; persistence falls as the weight rises and returned in the 2002 crisis
- [[inflation_targeting]] — what an explicit, externally set target changes in price setting, optimal policy and expectations; Brazil 1999–2004 with the 2001–2002 stress test
- [[inflation_expectations_anchoring]] — a microfounded expectations rule in which a high weight on the target shields expected inflation from exchange-rate and demand shocks; survey expectations off target only from September 2002 to July 2003
- [[targeting_rules]] — the optimal target criterion under the target-indexed curve: inflation plus the scaled output-gap change equals the official target when the weight is one
- [[calvo_pricing]] — Calvo pricing with a rule-of-thumb share indexing to the target, the pricing block of the derivation (Appendix B)
- [[exchange_rate_pass_through]] — short-run pass-through estimated at 0.053 (Table 1); with a credible target current exchange-rate changes drop out of expected inflation
- [[monetary_policy/synthesis/it_credibility_fx_volatility (Minella et al., 2003)]] — the ad hoc expectations regressions and the reading of the 2002 crisis this paper's structural model is set against
- [[monetary_policy/synthesis/implementing_it_brazil (Bogdanski, Tombini & Werlang, 2000)]] — the 1999 design and the crawling peg from which the pre-1999 target series is constructed; there BCB staff discounted the forward weight of hybrid estimates, here the target weight is estimated directly
- [[monetary_policy/synthesis/nk_small_open_economy (Gali & Monacelli, 2005)]] — the small open economy model whose domestic-inflation NKPC the paper's open-economy curve follows
- [[monetary_policy/synthesis/fiscal_dominance_it_brazil (Blanchard, 2004)]] — the argument that tightening could raise inflation in Brazil 2002 through debt dynamics, which the authors reject citing Bevilaqua and Loyo
