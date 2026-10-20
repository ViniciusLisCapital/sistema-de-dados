---
aliases: ["Gali 2015 - The Basic New Keynesian Model"]
---

# The Basic New Keynesian Model (Chapter 3) — Jordi Galí 2015

**Type:** book chapter
**Tags:** #new-keynesian #nkpc #dynamic-is #natural-rate #taylor-rule #calvo #monetary-transmission
**Source:** Chapter 3 of Galí's textbook (the clean_md prints only "Chapter 3"; the tracker row names the book *Monetary Policy, Inflation, and the Business Cycle*)
**Language:** English
**Source file:** [[monetary_policy/clean_md/basic_nk_model_ch3 (Gali, 2015)]]

---

## Context and motivation

The chapter builds the "baseline model that will be used as a reference framework in the remainder of the book" by making two departures from the classical monetary economy of chapter 2: (i) imperfect competition — each firm sells a differentiated good and sets its price facing a demand constraint; (ii) staggered price setting à la Calvo (1983), where only a fraction of firms can reset prices in a given period. The result is the "basic New Keynesian model", described as "the workhorse for the analysis of monetary policy, fluctuations, and welfare". Chapter 4 (policy design) and chapter 5 (discretion vs. commitment) build on it.

## Core argument / thesis

With sticky prices, "the equilibrium path of real variables cannot be determined independently of monetary policy. In other words, monetary policy is non-neutral." Inflation is no longer the residual of an equilibrium allocation that ignores nominal variables (the classical case); it "results from the aggregate consequences of purposeful price-setting decisions by firms, which adjust their prices in light of current and anticipated cost conditions." The whole non-policy block collapses into two forward-looking equations — the New Keynesian Phillips curve and the dynamic IS equation — plus an exogenous natural rate of interest; a monetary policy rule closes the model.

## Key mechanisms / model

- **Households (3.1)**: a CES consumption index over a continuum of goods gives an isoelastic demand schedule for each good (1), with price elasticity ϵ. The log-linear Euler equation (3) carries a preference ("discount rate") shifter zt. Money is not modeled explicitly (cashless limit); an ad hoc money demand `mt − pt = yt − ηit` (4) is added when needed.
- **Calvo price setting (3.2)**: each firm resets its price with probability 1−θ per period, independent of the time since the last change; θ is "a natural index of price stickiness". Aggregate inflation is `πt = (1 − θ)(p∗t − pt−1)` (8). A resetting firm sets its price as its desired markup over a weighted average of current and expected nominal marginal costs, weights proportional to θ^k times β^k (11), (16) — i.e. prices are set "in a forward-looking way".
- **Inflation equation (17)**: `πt = βEt{πt+1} − λµ̂t`, where µ̂t is the gap between the average and the desired markup, and λ is "strictly decreasing in the index of price stickiness θ, in the measure of decreasing returns α, and in the demand elasticity ϵ". Solved forward, inflation is the discounted sum of expected future markup gaps: inflation is positive when firms expect markups below the desired level.
- **Natural output and the output gap (18)–(21)**: the natural level of output is equilibrium output under flexible prices; it is "independent of monetary policy, and invariant to preference shocks". The markup gap is proportional to the output gap (21).
- **NKPC (22)**: inflation depends on its one-period-ahead forecast and the output gap, with κ defined as λ times a term in σ, ϕ and α. The text's own statement of the standard form, in exercise 3.6(e), is `πt = βEt{πt+1} + κyt` (y here the output gap).
- **Dynamic IS equation (23)**: the output gap depends on its expected next-period value and on the gap between the real rate (it − Et{πt+1}) and rⁿt, scaled by σ, where rⁿt is the natural rate of interest, "the real interest rate that would prevail in the flexible price equilibrium", given by (24) as a function of technology and preference shocks. Solved forward (25): the output gap is "inversely related to the sum of current and anticipated deviations between the real interest rate and its natural counterpart."
- **Closing the model — a Taylor-type rule (26)**: the nominal rate responds to inflation, to output's deviation from steady state, and to an AR(1) policy shock vt; the text calls it "broadly consistent with the rule proposed by Taylor (1993, 1999)". Footnote 5 gives Taylor's original rule, `i = 4 + 1.5(πt − 2) + 0.5(yt − y∗t)`, implying a 2 percent inflation target and a 2 percent steady-state real rate.
- **Determinacy (28)**: with non-negative coefficients, the equilibrium is locally unique if and only if `κ(φπ − 1) + (1 − β)φy > 0`; the economic interpretation is deferred to chapter 4. Under an exogenous money growth path (3.4.2) the equilibrium "is always determined" (based on numerical analysis of eigenvalues, footnote 14).

## Main results / findings

Baseline quarterly calibration (3.4.1.1): β = 0.99 (steady-state annualized real return of about 4 percent), σ = 1, ϕ = 5 (Frisch elasticity 0.2), α = 1/4, ϵ = 9 (markup M = 1.125, i.e. 12.5 percent), η = 4, θ = 3/4 (average price duration of four quarters), φπ = 1.5, φy = 0.5/4 (Taylor's coefficient divided by 4 for quarterly rates), ρv = 0.5. η comes from an OLS regression of log M2 inverse velocity on the 3 month T-bill rate over 1960:1–1988:1 (footnote 8).

Under the interest rate rule:
- **Monetary policy shock (Figure 3.1)** — a 25 basis point rise in εv (100 basis points annualized absent feedback): inflation, output, employment and the real wage fall; the nominal rate rises by less than its exogenous component; the real rate rises by more than the nominal rate; the money supply must fall sharply in the short run (a liquidity effect). If the shock is persistent enough, the nominal rate can *fall* while policy is still contractionary, because the real rate "goes up unambiguously". The responses are "similar, at least in a qualitative sense" to structural VAR estimates, but matching them quantitatively requires enriching the model (Christiano, Eichenbaum, and Evans 2005).
- **Discount rate shock (Figure 3.2)** — ρz = 0.5, initial shock of −0.5 percentage points, a one percentage point annualized rise in the natural rate on impact: output, employment, inflation and the real wage respond identically to the monetary shock, but the nominal and real rates fall, since this shock moves the natural rate and not the rule.
- **Technology shock (Figure 3.3)** — one percent, ρa = 0.9: output rises but by less than natural output, so the output gap and inflation fall; employment "experiences a large and persistent decline", matching the negative output–employment comovement estimated conditional on technology shocks (Galí 1999). The nominal and real rates fall, but not by enough to track the natural rate.

Under an exogenous money growth rule (3.4.2), ρm = 0.5: a money growth shock raises output by "about a third of a percentage point on impact" and the nominal rate rises slightly — no liquidity effect, which the text attributes to the calibration (σ = 1), not to the regime. A money growth rule is "effectively equivalent to an interest rate rule that targets the price level", so after discount-rate and technology shocks the price level returns to its original value and inflation must eventually turn positive (Figures 3.5, 3.6). With exogenous money the technology-shock output gap is much larger than under the interest rate rule, because the real rate rises instead of falling.

## Limitations and caveats

- **Equations are damaged throughout the extraction**: fraction bars, hats, tildes and several Greek capitals are lost, so many equations read as fragments and the output gap is printed with the same symbol as output; equations are described in words in this note except where the text prints them intact. Specifically: the bodies of (6) (technology process), the AR(1) processes for zt and vt, (20) (natural output), (22) (the NKPC) and (26) (the interest rate rule) are missing — only the equation numbers survive; (7), (11), (14), (18)–(19), (27) and the money-supply expression in 3.4.1.1 are garbled. The NKPC form quoted above is the one printed in exercise 3.6(e), not at (22). Footnote 12 reads "ϕya = 1" where the parameter is elsewhere ψya.
- **Figures 3.1–3.6** survive only as their captions and a dump of axis tick values; no response can be read off them. The caption and the opening of the discussion of Figure 3.4 (monetary shock under the money supply rule) are missing — the text resumes mid-sentence ("to a one percent increase, on impact, in the annualized rate of money growth").
- Text is cut in places: footnote 4 (the real marginal cost form of (17)), footnote 9, several citations in 3.5 Notes on the Literature, and the start of the reference list (it begins at Christiano et al. 2005).
- The model is closed-economy and cashless; all results are log-linear around a zero inflation steady state (the Notes cite Ascari 2004 and others for nonzero trend inflation). Empirical fit of the NKPC is which "has always been controversial", with weak identification and unobservability of the output gap as the main difficulties.
- In 3.4.2.3 the text compares Figure 3.6 with "figure 3.2 (corresponding to the analogous exercise under an interest rate rule)"; the analogous technology exercise is Figure 3.3. Flagged as written, not corrected.

## Connections

- [[nk_phillips_curve]] — derived here from Calvo pricing: (17) in markups, (22) in the output gap, with κ and λ defined and their dependence on θ, α, ϵ stated
- [[natural_rate_of_interest]] — defined as the flexible-price real rate (24); the DIS (23)/(25) makes the output gap the sum of expected deviations of the real rate from it
- [[taylor_rule]] — rule (26) closes the model, with Taylor's original rule in footnote 5 and the quarterly calibration φπ = 1.5, φy = 0.5/4
- [[taylor_principle]] (proposed) — determinacy condition (28), whose interpretation the text defers to chapter 4
- [[calvo_pricing]] (proposed) — the staggered price-setting device behind (8), (11), (16); θ as the stickiness index, mean price duration of four quarters
