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
