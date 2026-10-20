---
aliases: ["Gali 2015 - A Classical Monetary Model"]
---

# A Classical Monetary Model (Chapter 2) — Jordi Galí 2015

**Type:** book chapter
**Tags:** #classical-model #monetary-neutrality #price-level-determinacy #taylor-principle #money-in-the-utility-function #friedman-rule
**Source:** Chapter 2 of *Monetary Policy, Inflation, and the Business Cycle* (2nd ed.) (title from the tracker; the clean_md prints only "Chapter 2 / A Classical Monetary Model")
**Language:** English
**Source file:** [[monetary_policy/clean_md/classical_monetary_model_ch2 (Gali, 2015)]]

---

## Context and motivation

The chapter sets up a classical monetary economy — perfect competition and fully flexible prices in all markets — as a benchmark. Many of its predictions "are at odds with the evidence reviewed in chapter 1", but it introduces the notation, preferences and technology used throughout the book, and its failures are the motivation for the nominal frictions added from chapter 3 onward. Money plays only a unit-of-account role in sections 2.1–2.4 (a "cashless" economy, with an ad hoc money demand appended when policy is stated in terms of money); section 2.5 gives money an explicit role by putting real balances in the utility function.

## Core argument / thesis

In the baseline classical model, employment, output, the real interest rate and the real wage are determined by real factors alone: "monetary policy is neutral with respect to those real variables." Monetary policy matters only for nominal variables — and there what matters is whether the policy rule pins down a unique price level. Since household welfare depends only on real variables, "no policy rule is better than any other" in the cashless case, a result the text calls "clearly extreme and empirically unappealing". Adding money to the utility function makes the Friedman rule (a zero nominal rate) optimal and, with nonseparable utility, makes policy non-neutral — but by amounts that are very small and through a transmission mechanism still at odds with the evidence. "The overall assessment of the classical monetary model ... cannot be a favorable one."

## Key mechanisms / model

- **Households (2.1)**: a representative household maximizes expected discounted utility over consumption and hours, with a preference shifter Zt that acts as a shock to the effective discount factor (it affects intertemporal but not intratemporal choices). Optimality gives a labor supply schedule (9), `wt −pt = σct + ϕnt`, with ϕ the inverse Frisch elasticity, and a log-linear Euler equation (10) linking consumption to the real rate `it −Et{πt+1}` relative to the discount rate ρ ≡ −log β. A money demand of the form `mt −pt = ct −ηit` (11) is postulated when needed, with η the interest semielasticity.
- **Firms (2.2)**: a production function `Yt = AtN1−α t` (12) with AR(1) technology; profit maximization gives a labor demand schedule (15), the real wage equal to the marginal product of labor.
- **Equilibrium (2.3)**: combining both sides with goods market clearing `yt = ct` (16), employment (18), output (19), the real rate (20) and the real wage (21) are functions of technology only (and the real rate also of the preference shock). Output and the real wage always rise with productivity; the sign of the employment response depends on whether σ is above or below one (it is zero under log utility, σ = 1). The real rate falls after a positive technology shock and rises after an increase in zt.
- **Price level determination (2.4)**, using the Fisherian equation `it = Et{πt+1} + rt` (22):
  - *Exogenous nominal rate path* (2.4.1, rule (23) with an AR(1) policy shock vt): expected inflation is pinned down but actual inflation is not — any path differing by a shock ξt with Et−1{ξt} = 0 is an equilibrium. These are "sunspot shocks", and the equilibrium is "indeterminate"; the nominal wage inherits the indeterminacy.
  - *Simple inflation rule* (2.4.2), the rate responding to inflation's deviation from target π with coefficient φπ: if φπ > 1, difference equation (24) has a unique nonexplosive solution (25), inflation is a discounted sum of expected real-rate and policy-shock terms, and a larger φπ shrinks the effect of real shocks on inflation. If φπ < 1 the solution (26) again admits arbitrary shocks ξt. "The condition for a determinate price level, φπ > 1, requires that the central bank adjusts nominal interest rates more than one-for-one in response to any change in inflation, a property known as the Taylor principle."
  - *Exogenous money supply path* (2.4.3): substituting money demand into the Fisherian equation gives a forward-looking difference equation for the price level (27) whose solution (28)–(29) is always unique: "when the monetary policy rule takes the form of an exogenous path for the money supply, the equilibrium price level is always determined uniquely." Under an interest rate rule, by contrast, money supply "just adjusts endogenously" to money demand.
- **Money in the utility function (2.5)**: real balances enter utility; the budget constraint can be read as buying money services at a price 1 − Qt, which is approximately the nominal rate, so money demand (33)–(36) is the condition that the marginal utility of real balances relative to consumption equals that opportunity cost. With ν = σ the demand is unit-elastic in consumption, `mt −pt = yt −ηit` (36), the form "often maintained in subsequent chapters".
  - *Separable utility* (2.5.1): marginal utilities of consumption and labor do not depend on real balances, so the neutrality results of the cashless economy carry over unchanged.
  - *Nonseparable utility* (2.5.2): consumption and real balances form a composite index; the nominal rate now shifts labor supply through real balances (41), so output depends on the nominal rate, (43), with multiplier ψyi. In the "most plausible" case (ν > σ) a higher nominal rate lowers labor supply at any real wage, and output is inversely related to the nominal rate.
- **Optimal policy (2.4.4, 2.5.3)**: in the cashless case all rules are equally good. With money in utility, a planner equates the marginal utility of real balances to their social cost, assumed zero (50); privately the cost is the nominal rate, so efficiency requires `it = 0` for all t — "the policy prescription known as the Friedman rule" — implying steady-state deflation at the rate of time preference (π = −ρ). A rule `it = 0` leaves the price level indeterminate, but a rule `it = φ(rt−1 + πt)` with φ > 1 has the zero rate as its only stationary solution and makes inflation `πt = −rt−1`.

## Main results / findings

- **Responses to a monetary policy shock under the inflation rule (2.4.2)**: a tightening (positive vt) reduces inflation and, if persistent, lowers the nominal rate too; a liquidity effect appears "if and only if ηρv > 1". In contrast with the chapter 1 evidence, prices fall and there is "no effect on output or any other real variable."
- **Under an AR(1) money growth process (2.4.3)**, with no real shocks: as long as ρm > 0 (the empirically relevant case), the price level responds more than one-for-one to a money supply increase — "a prediction that contrasts starkly with the sluggish response of the price level" — and the nominal rate rises, so "the model implies the absence of a liquidity effect".
- **Size of non-neutrality under nonseparable utility (2.5.2)**, with σ = 1, ϕ = 5 and α = 1/4 (the chapter 3 baseline): the multiplier ψyi depends mainly on inverse velocity km. With the monetary base (km ≃ 0.3, postwar US) ψyi ≃ −0.04: a one percentage point (annualized) rise in the nominal rate lowers quarterly output by about 0.01 percent. With M2 (km ≃ 3) ψyi ≃ −0.4 and output falls by 0.1 percent — "while still very small", closer in order of magnitude to estimated effects.
- **Transmission still at odds with the data (2.5.2)**: for a tightening that raises the nominal rate and lowers output and money, real balances must fall, which by (48) requires the initial money decline to be followed by "persistently higher than average money growth" — contrary to the evidence, and independent of the specific policy rule. The real wage is predicted to move countercyclically after a policy shock, against the "mildly procyclical" response in Christiano, Eichenbaum, and Evans (2005).
- **Literature (2.6)**: Woodford (2003) and Walsh (2010) also conclude that, even with nonseparable real balances, "the real effects of monetary policy are quantitatively very small for plausible calibrations"; Cooley and Hansen (1989) find near-neutrality with a cash-in-advance constraint.

## Limitations and caveats

- **Equations are damaged throughout the extraction**: summation signs, fraction bars, hats and Greek capitals are lost, so most equations read as fragments spread over lines. In particular the utility function after (6), the forward solutions (25), (28), (29), the money growth process and price-level solution in 2.4.3 (the Δ on money growth is lost, so "mt = ρm mt−1" prints without it), the χ and ϖ definitions around (41), (44)–(45) (the multiplier symbol before (mt −pt) is missing) and (48) (the coefficient symbol is missing) are not readable as printed. They are described in words here, not restored.
- The chapter repeatedly contrasts its predictions with "the evidence reviewed in chapter 1"; chapter 1 is not in the file, so those empirical benchmarks cannot be checked here.
- The results are local: the Notes stress that uniqueness and indeterminacy refer only to bounded equilibria near the steady state; global multiplicity is discussed in other works cited there.
- The model has no investment, government or net exports (goods demand is consumption only), and in 2.5.2 preference shocks are dropped "to ease the algebra".
- Exercises 2.1–2.9 (price level targeting, partial-adjustment rules, welfare cost of inflation, cash-in-advance and shopping-time models) are posed but not solved in the file.

## Connections

- [[taylor_principle]] — derived here in its simplest form: in the classical model a rule with φπ > 1 gives a unique price level, φπ < 1 or an exogenous rate path gives sunspot indeterminacy (2.4.1–2.4.2), and the Friedman-rule peg is indeterminate too (2.5.3)
- [[monetary_targeting]] — an exogenous money supply path always determines the price level uniquely (28), but the price level overreacts to money shocks and there is no liquidity effect (2.4.3)
- [[friedman_rule]] (proposed) — a zero nominal rate equates the private and social cost of real balances; optimal with money in the utility function, implying deflation at the rate of time preference (2.5.3)
- [[monetary_neutrality]] (proposed) — real variables independent of monetary policy in the cashless and separable-utility cases; nonseparable utility breaks neutrality, but only by very small amounts (2.3, 2.5.2)
- [[monetary_policy/synthesis/basic_nk_model_ch3 (Gali, 2015)]] — the next chapter adds monopolistic competition and Calvo pricing to this benchmark, reusing its households, technology, calibration and money demand (36), to overcome the failures listed here
