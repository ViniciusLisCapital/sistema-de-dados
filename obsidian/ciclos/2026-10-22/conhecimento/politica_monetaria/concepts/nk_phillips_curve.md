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
| [[monetary_policy/synthesis/implementing_it_brazil (Bogdanski, Tombini & Werlang, 2000)]] | Brazil 1999: hybrid estimates gave at least 60% weight to expected inflation, rejected by BCB staff as implying too much credibility and "almost no inertia"; an average of backward and forward curves was used instead |

## BRL / application to the current analysis

The sources linked here say nothing about Brazil yet.

## Connections

- [[natural_rate_of_interest]] — with the dynamic IS equation, the NKPC forms the non-policy block of the NK model; the output gap it reads is driven by the real rate's deviation from the natural rate
- [[taylor_rule]] — the policy rule that closes the NKPC + DIS system
- [[monetary_policy/synthesis/implementing_it_brazil (Bogdanski, Tombini & Werlang, 2000)]] — why a central bank may discount the forward-looking weight its own estimates give right after a regime change
