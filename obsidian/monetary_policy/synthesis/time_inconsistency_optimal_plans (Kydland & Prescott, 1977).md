---
aliases: ["Kydland 1977 - Rules Rather than Discretion: The Inconsistency of Optimal Plans"]
---

# Rules Rather than Discretion: The Inconsistency of Optimal Plans — Finn E. Kydland & Edward C. Prescott 1977

**Type:** paper
**Tags:** #time-inconsistency #rules-vs-discretion #rational-expectations #inflation-bias #lucas-critique #credibility
**Source:** The Journal of Political Economy, Vol. 85, No. 3 (Jun., 1977), pp. 473-492 (JSTOR copy)
**Language:** English
**Source file:** [[monetary_policy/clean_md/time_inconsistency_optimal_plans (Kydland & Prescott, 1977)]]

---

## Context and motivation

Optimal control theory selects, at each date, the best decision given the current situation and given that future decisions are selected the same way, and many had proposed applying it to economic planning. The authors set out to show its applicability in a rational-expectations world and ended up, partly prompted by Sims's criticism (footnote), with "the radical conclusions of this essay": control theory "is not the appropriate tool for economic planning even when there is a well-defined and agreed-upon, fixed social objective function". The argument for rules does not rest, as Friedman's (1948) did, on ignorance of the timing and magnitude of policy effects.

## Core argument / thesis

"Economic planning is not a game against nature but, rather, a game against rational economic agents." Current decisions of agents depend on their expectations of future policy, and those expectations are not invariant to the plan chosen. A policy that is best given the current situation — a *consistent* policy — ignores the effect of future policy choices on agents' earlier decisions, so it does not maximize the social objective; the optimal plan, in turn, is *inconsistent*: once agents have acted, it is no longer optimal to continue with it. Hence discretion "either results in consistent but suboptimal planning or in economic instability", and policymakers should follow rules — "not that they are stupid or evil" but because discretion means choosing the best action given the current situation.

## Key mechanisms / model

- **Definitions (section II)**: with policies π and agents' decisions x over T periods, a social objective (1) and agents' decisions depending on all policy decisions and their own past decisions (2), the optimal policy maximizes (1) subject to (2). A policy is *consistent* if, for each period t, π_t maximizes (1) taking previous decisions as given and assuming future policies are selected the same way. In the two-period case the consistent choice of π2 ignores its effect on x1; it is optimal only if that effect is zero or if x1's total effect on the objective is zero. This is Pollak's (1968) solution concept for intergenerational planning (the feedback solution of a dynamic game; footnote: for dominant-player games the open-loop solution is inconsistent).
- **Two illustrations**: flood plains — absent a law prohibiting building, people build because they know the government will then build dams and levees; patents — once the invention exists the efficient policy is no patent protection, which is why the question is posed as the optimal patent life, a rule chosen for its operating characteristics.
- **Inflation-unemployment example (section III)**: unemployment falls with the gap between actual and expected inflation, linearly (5), with u* the natural rate; Phelps and Taylor (1975) obtain the relation from prices and wages set before demand is realized. Expectations are rational. Policy maximizes a social objective in inflation and unemployment subject to (5). In Figure 1 the consistent equilibrium is where an indifference curve is tangent to a Phillips curve on the vertical axis (point C): expectations are rational and policy is best given the situation, but inflation is excessive. If policymakers "were compelled to maintain price stability and did not have discretionary powers", unemployment would be no higher and the economy would reach the optimal point O on a higher indifference curve.
- **Infinite horizon (section IV)**: for recursive structures, consistency is defined over policy rules. Agents' decision rules depend on the future policy rule — "changes in policy rule ... change the functional form" of agents' rules, the Lucas (1976) critique — so the best current rule is a function of the rule expected in the future, and a stationary consistent rule is a fixed point of that mapping. Policymakers who take agents' decision rules as given will likely converge to the consistent but suboptimal rule. The suboptimality "is not due to myopia": "there is no mechanism to induce future policymakers to take into consideration the effect of their policy, via the expectations mechanism, upon current decisions of agents."
- **Investment-tax-credit example (section V)**: a rational-expectations equilibrium model of investment with a time-to-build lag (plans in t become productive in t + 2, spending split between t and t + 1), convex adjustment costs, a linear inverse demand with an autoregressive demand shock, and a quadratic social loss over output, investment, their total, prices and the credit. The policymaker starts from a passive policy, estimates the investment function, chooses an optimal rule by control theory assuming the function is invariant, then re-estimates after the economy shifts, and so on. The appendix gives the computation of competitive equilibria and consistent policies by backward induction with quadratic value functions.

## Main results / findings

- The iteration of policy rule → investment function → policy rule "typically" converged, to a consistent rule; in every converging case the authors "searched for and found linear feedback policy rules which were superior to this consistent rule, typically by a substantial amount". Within linear feedback rules the best rule depended on initial conditions, so the optimal policy was inconsistent.
- In one example (autoregressive demand parameter 0.6) optimal control first improved performance for two iterations, then deteriorated after the third; the consistent limit was "decidedly inferior to the passive policy" of an unvaried tax credit, by roughly variables "10 percent on average away from their targets".
- In another (parameter −0.6) the process did not converge: changes in the policy rule induced ever larger changes in the investment function, and fluctuations grew with each iteration — "current practice, if continued, could conceivably result in even greater fluctuations".
- Lessons: optimal control "is hazardous and could very well increase economic fluctuations or even make a stable economy unstable"; even when it works, a simple feedback rule does better.
- **Policy conclusion (section VII)**: until there is a tested theory of fluctuations, active stabilization "may very well be dangerous"; "a constant growth in the money supply and constant tax rates constitute a safer course of action". With that understanding, follow rules chosen by evaluating alternative rules with economic theory (Lucas 1976), preferably simple ones, "so it is obvious when a policymaker deviates"; one institutional option is for Congress to legislate monetary and fiscal rules effective only after a 2-year delay. Section VI extends the logic to a dominant-firm oligopoly, to constitutions limiting expropriation, and to oil investment deterred by expected price controls or windfall taxes.

## Limitations and caveats

- **Many equations are missing from the extraction**: (2), (3), (4), the consistent-policy recursion and first-order conditions of section II, the rules (6)–(7) and the social objective of section IV, the cash-flow function (8), the firm's objective, the inverse demand and shock process and the social loss of section V, and most of the appendix (A2), (A3), (A5) are absent or reduced to fragments. Equation (5) prints as "u, = i,(x: - x,) + u*," and the Phillips-curve slope in the text as "-K1". The note describes the models in words and restores none of them.
- **Figure 1** survives only as its caption ("Consistent and optimal equilibrium").
- **Footnote 9's parameter list and the loss weights of the two examples are partly garbled** (symbols and subscripts replaced: "j~ = 0.03", "fl = fl, = 0.9, = 0.3", "o, = 10", "0, = 20"), so they are not reproduced; only the autoregressive parameter of each example, which the text states, is cited. Footnote numbers are mostly lost or merged into the text.
- The extraction starts with a JSTOR cover page and has no reference list.
- Author's caveats: the structures "are far from a tested theory of economic fluctuations"; uncertainty "is not the central issue"; uniqueness of equilibrium in the infinite-period problem is "as yet unsolved" (the examples appeared unique); the quantitative results are summarized briefly ("Space constraints preclude more than a brief summary"), with details in the working paper.

## Connections

- [[time_inconsistency]] — the source of the concept: consistent vs. optimal policy, the two-period proof, the inflation-bias example (point C vs. point O), and the case for rules
- [[lucas_critique]] (proposed) — section IV and the tax-credit experiment: policy rules change agents' decision rules, so re-estimating and re-optimizing can fail to converge or destabilize the economy
- [[monetary_policy/synthesis/science_of_monetary_policy (Clarida, Gali & Gertler, 1999)]] — restates the inflationary bias in a New Keynesian model and adds that commitment pays even without an output target above potential
- [[monetary_policy/synthesis/taylor_rule (Taylor, 1993)]] — draws its analytical distinction between rules and discretion from this paper, but defines a rule broadly enough to be operated with judgment
- [[monetary_policy/synthesis/forward_guidance_effects (Campbell et al., 2012)]] — Odyssean forward guidance as a promise exposed to exactly this inconsistency
