# New Keynesian Phillips Curve (NKPC)

**Type:** Inflation equation / structural relation
**Tags:** #nkpc #new-keynesian #inflation #sticky-prices #output-gap

---

## Definition

The inflation equation of the New Keynesian model: current inflation depends on expected next-period inflation and on the output gap (equivalently, on the gap between firms' average and desired markups, or on real marginal cost). In Galí's statement, `πt = βEt{πt+1} + κyt`, with y the output gap.

## Mechanism

Derived from staggered (Calvo) price setting: each period only a fraction 1−θ of firms can reset prices, so a resetting firm sets its price as a markup over a weighted average of current and expected marginal costs. Aggregating gives inflation as `πt = βEt{πt+1} − λµ̂t`, where µ̂t is the markup gap; the slope λ falls with price stickiness θ, with decreasing returns α and with the demand elasticity ϵ. Because the markup gap is proportional to the output gap, the same relation can be written in the output gap with slope κ. Solved forward, inflation is the discounted sum of expected future markup (or output) gaps: inflation is forward-looking, driven by expected cost conditions rather than by past inflation.

## When it applies / when it fails

- It is a log-linear approximation around a zero inflation steady state; with nonzero trend inflation the equation changes (literature cited in Galí's notes).
- Its empirical performance "has always been controversial" (Galí): the output gap is unobservable and the equation suffers from weak identification. Purely forward-looking inflation has no intrinsic persistence; extensions with indexation or backward-looking firms add lagged inflation (Galí's exercises 3.4 and 3.9).

## How it appears across sources

| Source | Role |
|---|---|
| [[monetary_policy/synthesis/basic_nk_model_ch3 (Gali, 2015)]] | Derivation from Calvo pricing: (17) in markups, (22) in the output gap; slope's dependence on θ, α, ϵ |
| [[monetary_policy/synthesis/forward_guidance_effects (Campbell et al., 2012)]] | Estimated DSGE: price Phillips curve slope "about an order of magnitude smaller than single-equation estimates", so higher inflation expectations barely move inflation over 3 years |
| [[monetary_policy/synthesis/science_of_monetary_policy (Clarida, Gali & Gertler, 1999)]] | The forward-looking curve (2.2)/(2.6) with a cost-push shock that creates the policy tradeoff; hybrid version with lagged inflation (6.2); real marginal cost rather than the gap as driving variable |
| [[monetary_policy/synthesis/staggered_prices (Calvo, 1983)]] | Continuous-time precursor: the rate of change of inflation falls with excess demand (a "higher-order" inverse Phillips curve), while in equilibrium inflation and excess demand move together in a policy-dependent way |
| [[monetary_policy/synthesis/information_effect_hf_identification (Nakamura & Steinsson, 2018)]] | Slope estimated "very flat" from high-frequency responses of real rates and break-even inflation; ignoring the information effect makes it flatter still |
| [[monetary_policy/synthesis/monetary_policy_rules_stability (Clarida, Gali & Gertler, 2000)]] | The forward-looking curve (6) in the calibrated model used to compare the pre- and post-1979 rules; a supply shock gives persistent inflation only under an accommodating rule |
| [[monetary_policy/synthesis/discretion_vs_commitment_ch5 (Gali, 2015)]] | Rewritten in the welfare-relevant output gap with a cost-push shock, (2); appendix 5.2 derives the shock from exogenous price- and wage-markup variations |
| [[monetary_policy/synthesis/sticky_wages_prices_ch6 (Gali, 2015)]] | Price and wage inflation equations in the output gap and the real wage gap, (18) and (20); a weighted average of the two (composite inflation) obeys an NKPC in the output gap, (36) |
| [[monetary_policy/synthesis/unemployment_nk_model_ch7 (Gali, 2015)]] | The New Keynesian Wage Phillips Curve (11): wage inflation depends on expected wage inflation and the unemployment gap, forward-looking and derived from first principles, unlike Phillips's original curve |
| [[monetary_policy/synthesis/open_economy_monetary_policy_ch8 (Gali, 2015)]] | Open-economy NKPC in domestic inflation (37), with slope depending on openness and the trade elasticity; equal to the closed-economy slope when σ = η = 1 |
| [[monetary_policy/synthesis/nk_small_open_economy (Gali & Monacelli, 2005)]] | Small open economy NKPC in domestic inflation (40): same form as the closed economy, slope κα depending on openness and the trade elasticity, flatter with more openness if ση > 1 |
| [[monetary_policy/synthesis/information_shocks_policy_surprises (Jarocinski & Karadi, 2020)]] | Hybrid NKPC (8) estimated by impulse-response matching: Calvo parameter 0.94 and indexation 0.91 under standard high-frequency identification, 0.88 and 0.00 once information shocks are purged — moderate rather than high nominal rigidity |
| [[monetary_policy/synthesis/implementing_it_brazil (Bogdanski, Tombini & Werlang, 2000)]] | Brazil 1999: hybrid estimates gave at least 60% weight to expected inflation, rejected by BCB staff as implying too much credibility and "almost no inertia"; an average of backward and forward curves was used instead |

## BRL / application to the current analysis

The sources linked here say nothing about Brazil yet.

## Connections

- [[natural_rate_of_interest]] — with the dynamic IS equation, the NKPC forms the non-policy block of the NK model; the output gap it reads is driven by the real rate's deviation from the natural rate
- [[taylor_rule]] — the policy rule that closes the NKPC + DIS system
- [[monetary_policy/synthesis/basic_nk_model_ch3 (Gali, 2015)]] — derivation of the NKPC in the basic New Keynesian model
- [[monetary_policy/synthesis/forward_guidance_effects (Campbell et al., 2012)]] — the very flat estimated price Phillips curve in the Chicago Fed DSGE
- [[monetary_policy/synthesis/science_of_monetary_policy (Clarida, Gali & Gertler, 1999)]] — the cost-push shock in the NKPC as the source of the output–inflation tradeoff, and the hybrid curve with inflation inertia
- [[monetary_policy/synthesis/staggered_prices (Calvo, 1983)]] — the staggered-pricing device the NKPC is derived from, and its own continuous-time inflation equation
- [[monetary_policy/synthesis/information_effect_hf_identification (Nakamura & Steinsson, 2018)]] — backward-looking (indexed) Phillips curve whose estimated slope depends on how much of a policy surprise is read as information
- [[monetary_policy/synthesis/monetary_policy_rules_stability (Clarida, Gali & Gertler, 2000)]] — the Phillips curve block of the model in which estimated rules are evaluated for determinacy and volatility
- [[monetary_policy/synthesis/discretion_vs_commitment_ch5 (Gali, 2015)]] — the NKPC with a cost-push shock as the constraint of the optimal policy problem
- [[monetary_policy/synthesis/sticky_wages_prices_ch6 (Gali, 2015)]] — price and wage Phillips curves with sticky wages, and the composite-inflation NKPC
- [[monetary_policy/synthesis/unemployment_nk_model_ch7 (Gali, 2015)]] — the wage Phillips curve in the unemployment gap
- [[monetary_policy/synthesis/open_economy_monetary_policy_ch8 (Gali, 2015)]] — the small open economy NKPC in domestic inflation
- [[monetary_policy/synthesis/nk_small_open_economy (Gali & Monacelli, 2005)]] — the canonical small open economy NKPC in domestic inflation and the output gap
- [[monetary_policy/synthesis/information_shocks_policy_surprises (Jarocinski & Karadi, 2020)]] — Phillips curve parameters depend on purging information from policy shocks
- [[monetary_policy/synthesis/implementing_it_brazil (Bogdanski, Tombini & Werlang, 2000)]] — why a central bank may discount the forward-looking weight its own estimates give right after a regime change
