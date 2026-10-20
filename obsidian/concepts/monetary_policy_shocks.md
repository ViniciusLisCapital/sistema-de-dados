# Monetary Policy Shocks

**Type:** Empirical concept / identification problem
**Tags:** #monetary-policy-shocks #identification #var #narrative-approach #impulse-response

---

## Definition

The part of a central bank's policy actions that is not a systematic response to the state of the economy. Christiano, Eichenbaum & Evans write the instrument (the funds rate or a monetary aggregate) as a linear feedback rule on the bank's information set plus a disturbance — the monetary policy shock (their equation 2.1). The shock matters not because policy is mostly random, but because it is a controlled experiment: the economy's response to it can be compared with the response of competing models to the same experiment. Policy actions themselves cannot serve, since they also reflect the shocks the bank is reacting to.

## Identification strategies

- **Recursiveness assumption (estimated feedback rule)**: the shock is orthogonal to the variables in the bank's information set, which do not respond to it within the period; the shock is the OLS residual of the instrument on that set, or equivalently a block-triangular VAR. It identifies the response to the policy shock but not to the other shocks, and the result does not depend on the ordering within blocks (Christiano, Eichenbaum & Evans, Proposition 4.1).
- **Non-recursive systems**: the bank may react to variables that respond to the shock within the period, so other restrictions are needed (Sims & Zha: money demand, and goods-market variables reacting only through commodity prices).
- **Narrative approach**: dates read from policy records when the bank deliberately tightened to fight inflation (Romer & Romer 1989), or a discrete stance index from FOMC minutes (Boschen & Mills).
- **Market-based surprises**: the funds rate minus the futures rate for the month (Rudebusch), which measures the unanticipated part of a move from market prices.
- **Long-run restrictions**: shocks assumed to have no long-run effect on activity (mentioned, not developed, by Christiano, Eichenbaum & Evans).
- **Selecting among schemes**: reject identifying assumptions whose impulse responses no candidate model can produce — in practice sign and shape restrictions.

## When it applies / when it fails

- **Confounding**: a scheme that omits information the bank had produces shocks contaminated by the bank's response to it. The **price puzzle** — prices rising for years after a tightening — appears when commodity prices, a leading indicator of inflation, are left out of a funds-rate VAR, and largely disappears when they are included.
- **Measurement error**: if shocks come from errors in preliminary data, the recursiveness assumption can fail when lagged errors and current errors are correlated.
- **Dates versus effects**: inference about the qualitative effects of a shock is robust across schemes, but inference about the stance of policy at a given date is not — two versions of the same model can disagree by tens of basis points in one quarter.
- **Shocks are not the systematic part**: a small contribution of shocks to output or price volatility says nothing about the importance of the feedback rule, and estimated rule coefficients are hard to interpret when the bank reacts to data the econometrician does not have.
- **Size changes over time**: the variance of shocks was larger in the early 1980s; the response to a shock of given size appears stable across subsamples.

## How it appears across sources

| Source | Role |
|---|---|
| [[monetary_policy/synthesis/monetary_policy_shocks_survey (Christiano, Eichenbaum & Evans, 1999)]] | The handbook survey: shocks as residuals of the feedback rule, recursive FF, NBR and NBR/TR benchmarks, Sims–Zha and narrative alternatives; consensus that after a tightening the funds rate rises, money, output and employment fall and prices respond very slowly; FF shocks account for 21%, 44% and 38% of the 4, 8 and 12 quarter output forecast error variance |
| [[monetary_policy/synthesis/new_measure_monetary_shocks (Romer & Romer, 2004)]] | Narrative-plus-forecast measure: intended funds rate changes at FOMC meetings, purged of the response to Greenbook forecasts; a one-percentage-point shock lowers industrial production by 4.3 percent and the price level by 5.9 percent after 48 months, while the actual funds rate gives smaller, slower effects and a price puzzle |
| [[monetary_policy/synthesis/policy_actions_vs_words (Gurkaynak, Sack & Swanson, 2005)]] | High-frequency surprises from federal funds futures in 30-minute windows around FOMC announcements, 1990–2004; a rank test rejects a single surprise measure and accepts two factors, a target factor and a path factor tied to FOMC statements |
| [[monetary_policy/synthesis/information_shocks_policy_surprises (Jarocinski & Karadi, 2020)]] | Sign restrictions on interest-rate and stock-price surprises split announcements into a policy shock (rate up, stocks down) and an information shock (both up); the purged policy shock lowers prices faster and tightens financial conditions more than standard high-frequency identification shows |

## BRL / application to the current analysis

The linked sources say nothing about Brazil: the evidence is for the United States, with a review of results for other G7 countries and Canada.

## Connections

- [[monetary_transmission_lags]] — the timing of the responses to an identified shock is what the lag literature measures
- [[credit_channel]] — VAR responses of loans, securities and borrowing by firm size are used to test credit-market theories
- [[uip]] — identified US shocks move exchange rates in ways that violate uncovered interest parity
- [[information_effect]] — a market-based surprise may carry news about fundamentals rather than a pure policy shock
- [[monetary_policy/synthesis/monetary_policy_shocks_survey (Christiano, Eichenbaum & Evans, 1999)]] — the reference survey of identification schemes and of the consensus responses
- [[monetary_policy/synthesis/new_measure_monetary_shocks (Romer & Romer, 2004)]] — shocks free of endogenous and anticipatory movements by construction, and evidence that conventional measures understate policy effects
- [[monetary_policy/synthesis/policy_actions_vs_words (Gurkaynak, Sack & Swanson, 2005)]] — intraday identification and the two-dimensional (target and path) structure of policy surprises
- [[monetary_policy/synthesis/information_shocks_policy_surprises (Jarocinski & Karadi, 2020)]] — purging high-frequency policy surprises of central bank information
